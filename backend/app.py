"""Sugbo Guide backend: fast local tourism bot for Cebu.

Pipeline per question (cheapest first):
  1. Exact cache            normalized question seen before          ~0 ms
  2. Semantic cache         embedding close to a past question       ~5-20 ms (only with USE_EMBEDDINGS=1)
  3. Router
       ROUTER=dalan (default)  DALAN: code-switch normalization, lexical + character channels, calibrated
                               confidence and per-language risk-controlled thresholds (see docs/ALGORITHM.md)
       ROUTER=hybrid           earlier keyword + embedding rule with fixed thresholds
     Router actions:
       skip      answer straight from the knowledge base (no LLM)
       generate  local LLM writes the answer from the top 3 entries
       abstain   off-topic -> guided reply, never a made-up answer

The LLM is any OpenAI-compatible server running locally:
  Ollama:     LLM_BASE_URL=http://localhost:11434/v1  LLM_MODEL=qwen2.5:7b-instruct
  llama.cpp:  llama-server -m model.gguf --port 8080  LLM_BASE_URL=http://localhost:8080/v1
  vLLM:       vllm serve <model> --port 8000          LLM_BASE_URL=http://localhost:8000/v1
"""
import json
import os
import time
from pathlib import Path

import httpx
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse
from pydantic import BaseModel

import sys

from router import KeywordRouter, norm

ROOT = Path(__file__).parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO))
KB = json.loads((REPO / "kb" / "kb.json").read_text(encoding="utf-8"))
ROUTER = os.getenv("ROUTER", "dalan")

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b-instruct")
EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-small")
USE_EMBEDDINGS = os.getenv("USE_EMBEDDINGS", "0") == "1"   # optional semantic cache / hybrid router
CACHE_SIM = float(os.getenv("CACHE_SIM", "0.93"))      # semantic cache threshold
KB_SIM = float(os.getenv("KB_SIM", "0.86"))            # embedding score that counts as confident

SYSTEM_PROMPT = (
    "You are Sugbo Guide, a friendly local tourism assistant for Cebu, Philippines. "
    "Answer ONLY from the CONTEXT. If the context does not contain the answer, say you are not sure and suggest "
    "asking the local tourism office. Keep answers short (under 120 words), practical, and in the same language "
    "as the question (English, Cebuano, Tagalog, Korean, Japanese, or Chinese). Mention that prices and schedules "
    "should be verified. When relevant, recommend local products and buying directly from farmers and makers."
)

kw_router = KeywordRouter(KB)
dalan_router = None
if ROUTER == "dalan":
    from dalan import DALANRouter

    _calib = [json.loads(l) for l in (REPO / "data" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    dalan_router = DALANRouter(KB, eps=float(os.getenv("DALAN_EPS", "0.05"))).fit(_calib)
entries = [e for e in KB["entries"] if e["id"] != "fallback"]
fallback = next(e for e in KB["entries"] if e["id"] == "fallback")

# ------------------------------------------------------------------ embeddings
embedder = None
entry_vecs = None
if USE_EMBEDDINGS:
    from sentence_transformers import SentenceTransformer

    embedder = SentenceTransformer(EMBED_MODEL)

    def embed(texts, is_query):
        prefix = "query: " if is_query else "passage: "  # e5 convention
        return embedder.encode([prefix + t for t in texts], normalize_embeddings=True)

    docs = [f"{e['title']}. {' '.join(e['questions'])} {e['answer']}" for e in entries]
    entry_vecs = embed(docs, is_query=False)

exact_cache: dict[str, dict] = {}
sem_cache_vecs: list[np.ndarray] = []
sem_cache_vals: list[dict] = []


def retrieve(question: str) -> dict:
    """Routing decision. Returns route (kb / llm / fallback), answer entry, and LLM context."""
    if dalan_router is not None:
        d = dalan_router.route(question)
        name = {"skip": "kb", "generate": "llm", "abstain": "fallback"}[d["action"]]
        qv = embed([question], is_query=True)[0] if embedder is not None else None
        return dict(route=name, entry=d["entry"], score=d["p"], context=d["context"], qv=qv)
    kw = kw_router.route(question)
    if embedder is None:
        return kw
    qv = embed([question], is_query=True)[0]
    sims = entry_vecs @ qv
    order = np.argsort(-sims)
    best, best_sim = entries[order[0]], float(sims[order[0]])
    context = [entries[i] for i in order[:3]]
    # Agreement between keyword and embedding top hit is the strongest signal.
    if kw["route"] == "kb" or (best_sim >= KB_SIM and kw["entry"]["id"] == best["id"]):
        return dict(route="kb", entry=kw["entry"] if kw["route"] == "kb" else best,
                    score=max(kw["score"], best_sim), context=context, qv=qv)
    if kw["route"] == "fallback" and best_sim < 0.78:
        return dict(route="fallback", entry=fallback, score=best_sim, context=[], qv=qv)
    # Merge keyword and embedding context for the LLM.
    merged = {e["id"]: e for e in (kw.get("context") or []) + context}
    return dict(route="llm", entry=best, score=best_sim, context=list(merged.values())[:3], qv=qv)


def cache_lookup(question: str, qv=None):
    key = norm(question)
    if key in exact_cache:
        return exact_cache[key], "exact"
    if qv is not None and sem_cache_vecs:
        sims = np.stack(sem_cache_vecs) @ qv
        i = int(np.argmax(sims))
        if sims[i] >= CACHE_SIM:
            return sem_cache_vals[i], "semantic"
    return None, None


def cache_store(question: str, value: dict, qv=None):
    exact_cache[norm(question)] = value
    if qv is not None:
        sem_cache_vecs.append(qv)
        sem_cache_vals.append(value)


def build_messages(question: str, context: list[dict]):
    ctx = "\n\n".join(f"[{e['title']}]\n{e['answer']}" for e in context)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {question}"},
    ]


async def llm_complete(question: str, context: list[dict]) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{LLM_BASE_URL}/chat/completions", json=dict(
            model=LLM_MODEL, messages=build_messages(question, context),
            temperature=0.2, max_tokens=300))
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()


async def llm_stream(question: str, context: list[dict]):
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", f"{LLM_BASE_URL}/chat/completions", json=dict(
                model=LLM_MODEL, messages=build_messages(question, context),
                temperature=0.2, max_tokens=300, stream=True)) as r:
            async for line in r.aiter_lines():
                if not line.startswith("data: ") or line.endswith("[DONE]"):
                    continue
                delta = json.loads(line[6:])["choices"][0]["delta"].get("content")
                if delta:
                    yield delta


# ------------------------------------------------------------------ API
app = FastAPI(title="Sugbo Guide")


class Ask(BaseModel):
    question: str


async def answer(question: str) -> dict:
    t0 = time.perf_counter()
    cached, kind = cache_lookup(question)
    if cached:
        return {**cached, "route": f"cache-{kind}", "ms": round((time.perf_counter() - t0) * 1000, 2)}
    r = retrieve(question)
    qv = r.pop("qv", None)
    cached, kind = cache_lookup(question, qv)
    if cached:
        return {**cached, "route": f"cache-{kind}", "ms": round((time.perf_counter() - t0) * 1000, 2)}
    if r["route"] == "llm":
        try:
            text = await llm_complete(question, r["context"])
        except Exception:
            text = r["entry"]["answer"]  # LLM down: degrade gracefully to best KB entry
            r["route"] = "kb-degraded"
    else:
        text = r["entry"]["answer"]
    out = dict(answer=text, title=r["entry"]["title"], entry_id=r["entry"]["id"],
               sources=[e["id"] for e in r.get("context", [])], route=r["route"])
    if r["route"] != "fallback":
        cache_store(question, out, qv)
    out["ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return out


@app.post("/chat")
async def chat(body: Ask):
    return await answer(body.question)


@app.post("/chat/stream")
async def chat_stream(body: Ask):
    """Streams tokens for the LLM route so the first words appear immediately."""
    r = retrieve(body.question)
    r.pop("qv", None)
    if r["route"] != "llm":
        return PlainTextResponse(r["entry"]["answer"])
    return StreamingResponse(llm_stream(body.question, r["context"]), media_type="text/plain")


@app.get("/products")
def products(region: str | None = None):
    return [p for p in KB["products"] if region in (None, p["region"])]


@app.get("/", response_class=HTMLResponse)
def home():
    return (REPO / "web" / "sugbo-guide.html").read_text(encoding="utf-8")


# ------------------------------------------------------------------ Facebook Messenger
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN", "")


@app.get("/messenger")
def messenger_verify(request: Request):
    p = request.query_params
    if p.get("hub.mode") == "subscribe" and p.get("hub.verify_token") == FB_VERIFY_TOKEN:
        return PlainTextResponse(p.get("hub.challenge", ""))
    return PlainTextResponse("forbidden", status_code=403)


@app.post("/messenger")
async def messenger_webhook(request: Request):
    data = await request.json()
    async with httpx.AsyncClient(timeout=20) as client:
        for entry in data.get("entry", []):
            for ev in entry.get("messaging", []):
                text = ev.get("message", {}).get("text")
                if not text:
                    continue
                res = await answer(text)
                await client.post("https://graph.facebook.com/v19.0/me/messages",
                                  params={"access_token": FB_PAGE_TOKEN},
                                  json={"recipient": {"id": ev["sender"]["id"]},
                                        "message": {"text": res["answer"][:1990]}})
    return {"ok": True}
