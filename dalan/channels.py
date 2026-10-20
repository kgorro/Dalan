"""Stage B of DALAN: two independent retrieval channels plus rank fusion.

LexicalChannel  IDF-weighted field matching over CSN tokens (keywords x3, title x2, questions x1, phrase bonus).
CharChannel     TF-IDF cosine over character 3-5 grams. Robust to typos and spelling variants
                (bantayn, osmenia, kawassan) that the lexical channel misses.
DenseChannel    optional multilingual sentence embeddings (e.g. intfloat/multilingual-e5-small); a drop-in
                replacement or third channel when sentence-transformers and the model are available.

Both channels return a score for every entry; fuse() combines their rankings with reciprocal rank fusion.
"""
import math
from collections import Counter

import numpy as np

from .normalize import fold, stem_en, STOP


def entry_text(e):
    return " ".join([e["title"], " ".join(e["keywords"]), " ".join(e["questions"])])


class LexicalChannel:
    def __init__(self, entries):
        self.entries = entries
        self.docs = []
        for e in entries:
            tk = lambda s: {stem_en(w) for w in fold(s).replace("-", " ").split() if w not in STOP}
            self.docs.append(dict(
                title=tk(e["title"]),
                kw=set().union(*[tk(k) for k in e["keywords"]]) if e["keywords"] else set(),
                q=set().union(*[tk(q) for q in e["questions"]]) if e["questions"] else set(),
                phrases=[fold(k) for k in e["keywords"] if " " in fold(k)],
            ))
        df = Counter()
        for d in self.docs:
            df.update(d["title"] | d["kw"] | d["q"])
        n = len(self.docs)
        self.idf = {t: math.log(1 + n / c) for t, c in df.items()}
        self.default_idf = math.log(2)

    def scores(self, nq):
        qt = set(nq.tokens)
        qn = f" {nq.folded} "
        north = " north " in qn or "north" in qt or " amihanan " in qn
        south = " south " in qn or "south" in qt or " habagatan " in qn
        out = np.zeros(len(self.docs))
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in qt:
                w = self.idf.get(t, self.default_idf) * nq.weights.get(t, 1.0)
                if t in d["kw"]:
                    s += 3 * w
                elif t in d["title"]:
                    s += 2 * w
                elif t in d["q"]:
                    s += w
            for p in d["phrases"]:
                if f" {p} " in qn:
                    s += 4
            r = self.entries[i]["region"]
            if north and r == "north":
                s += 1.5
            if south and r == "south":
                s += 1.5
            if r == "north" and south and not north:
                s -= 2
            if r == "south" and north and not south:
                s -= 2
            out[i] = s
        return out


def char_grams(text, lo=3, hi=5):
    grams = Counter()
    for w in text.split():
        if w in STOP:
            continue
        w = f"#{w}#"
        for n in range(lo, hi + 1):
            for i in range(len(w) - n + 1):
                grams[w[i:i + n]] += 1
    return grams


class CharChannel:
    def __init__(self, entries):
        docs = [char_grams(fold(entry_text(e))) for e in entries]
        df = Counter()
        for d in docs:
            df.update(d.keys())
        n = len(docs)
        self.idf = {g: math.log((1 + n) / (1 + c)) + 1 for g, c in df.items()}
        self.vecs = [self._vec(d) for d in docs]

    def _vec(self, grams):
        v = {g: (1 + math.log(c)) * self.idf.get(g, 0.0) for g, c in grams.items()}
        v = {g: x for g, x in v.items() if x > 0}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {g: x / norm for g, x in v.items()}

    def scores(self, nq):
        q = self._vec(char_grams(nq.char_text))
        return np.array([sum(w * d.get(g, 0.0) for g, w in q.items()) for d in self.vecs])


class DenseChannel:
    """Optional. Requires sentence-transformers and a downloaded model."""

    def __init__(self, entries, model_name="intfloat/multilingual-e5-small"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        texts = ["passage: " + entry_text(e) + " " + e["answer"] for e in entries]
        self.mat = self.model.encode(texts, normalize_embeddings=True)

    def scores(self, nq):
        v = self.model.encode(["query: " + nq.raw], normalize_embeddings=True)[0]
        return self.mat @ v


def ranks(scores):
    order = np.argsort(-scores, kind="stable")
    r = np.empty(len(scores), dtype=int)
    r[order] = np.arange(len(scores))
    return r


def fuse(score_lists, weights=None, k=10):
    """Weighted reciprocal rank fusion. Returns fused score per entry."""
    weights = weights or [1.0] * len(score_lists)
    fused = np.zeros(len(score_lists[0]))
    for s, w in zip(score_lists, weights):
        fused += w / (k + 1 + ranks(s))
    return fused
