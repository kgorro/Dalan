"""Keyword router, a Python port of router.js. Runs in microseconds and needs no model.

Routes:
  kb        confident match, answer straight from the knowledge base
  llm       some signal, let the local LLM compose an answer from the top entries
  fallback  nothing relevant
"""
import math
import re
import unicodedata

STOP = set("a an the is are am i me my we you your to of in on at for and or do does did can could how what where when "
           "which who why it this that there be with from go get near about any some please tell know want like ba ang "
           "sa ug ni nga ko mo".split())


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9\s-]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def stem(t: str) -> str:
    if len(t) > 4 and t.endswith("es"):
        return t[:-2]
    if len(t) > 3 and t.endswith("s"):
        return t[:-1]
    return t


def toks(s: str):
    return [stem(t) for t in re.split(r"[\s-]+", norm(s)) if t and t not in STOP]


class KeywordRouter:
    def __init__(self, kb: dict, hi: float = 6.0, lo: float = 2.5):
        self.hi, self.lo = hi, lo
        self.fallback = next(e for e in kb["entries"] if e["id"] == "fallback")
        self.docs = []
        for e in kb["entries"]:
            if e["id"] == "fallback":
                continue
            self.docs.append(dict(
                e=e,
                title=set(toks(e["title"])),
                kw={t for k in e["keywords"] for t in toks(k)},
                q={t for q in e["questions"] for t in toks(q)},
                phrases=[norm(k) for k in e["keywords"] if " " in norm(k)],
            ))
        df = {}
        for d in self.docs:
            for t in d["title"] | d["kw"] | d["q"]:
                df[t] = df.get(t, 0) + 1
        n = len(self.docs)
        self.idf = {t: math.log(1 + n / c) for t, c in df.items()}
        self.n = n

    def rank(self, query: str):
        qn = f" {norm(query)} "
        qt = set(toks(query))
        north = bool(re.search(r"\bnorth|amihanan\b", qn))
        south = bool(re.search(r"\bsouth|habagatan\b", qn))
        out = []
        for d in self.docs:
            s = 0.0
            for t in qt:
                w = self.idf.get(t, math.log(2))
                if t in d["kw"]:
                    s += 3 * w
                elif t in d["title"]:
                    s += 2 * w
                elif t in d["q"]:
                    s += w
            for p in d["phrases"]:
                if f" {p} " in qn:
                    s += 4
            r = d["e"]["region"]
            if north and r == "north":
                s += 1.5
            if south and r == "south":
                s += 1.5
            if r == "north" and south and not north:
                s -= 2
            if r == "south" and north and not south:
                s -= 2
            out.append((s, d["e"]))
        out.sort(key=lambda x: -x[0])
        return out

    def route(self, query: str):
        ranked = self.rank(query)
        top_s, top = ranked[0]
        if top_s < self.lo:
            return dict(route="fallback", entry=self.fallback, score=top_s, context=[])
        margin = top_s - ranked[1][0]
        name = "kb" if (top_s >= self.hi or margin >= 3) else "llm"
        return dict(route=name, entry=top, score=top_s, context=[e for _, e in ranked[:3]])
