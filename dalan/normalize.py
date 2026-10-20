"""Stage A of DALAN: Code-Switch Normalization (CSN).

Turns a raw tourist query that may mix English, Cebuano, and Tagalog into:
  - tokens: original stemmed tokens plus English concept tokens projected from the lexicon
  - char_text: folded text plus glosses, for the character channel
  - code-switch statistics used by the calibrator (CSI, OOV rate, lexicon hit rate)

Steps:
  A1 orthographic folding   lowercase, strip diacritics, collapse letter runs, expand clitics (asa'y -> asa ang)
  A2 vowel-variant keying   Cebuano e/i and o/u alternate freely in chat (komosta, kumusta), so lexicon lookup
                            uses a phonetic key that merges them
  A3 lexicon-guided affix   strip Cebuano/Tagalog affixes (maka-, gi-, -on, -um- infix) ONLY when the remainder
     stripping              is a known lemma, so English words are never damaged
  A4 concept projection     append English gloss tokens of every recognized lemma, keeping the original token
"""
import math
import re
import unicodedata
from dataclasses import dataclass, field

from .lexicon import CONTRACTIONS, LEXICON, PREFIXES, SUFFIXES

STOP = set("a an the is are am i me my we you your to of in on at for and or do does did can could how what where "
           "when which who why it this that there be with from go get near about any some please tell know want "
           "like have has should would will".split())
# English words that must never be treated as Cebuano/Tagalog even if they look like a lemma
EN_GUARD = {"man", "pier", "terminal", "plano", "dad", "init", "mura", "dala", "ting", "uli", "pulis", "lugar"}


def phon_key(w: str) -> str:
    return w.replace("e", "i").replace("o", "u").replace("-", "")


LEX_BY_KEY = {}
for _lemma in LEXICON:
    LEX_BY_KEY.setdefault(phon_key(_lemma), _lemma)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"(\w)['’]y\b", r"\1 ang", s)          # asa'y -> asa ang
    s = re.sub(r"[^a-z0-9\s-]", " ", s)
    s = re.sub(r"([a-z])\1{2,}", r"\1", s)            # pleaseee -> please
    return re.sub(r"\s+", " ", s).strip()


def stem_en(t: str) -> str:
    if len(t) > 4 and t.endswith("es"):
        return t[:-2]
    if len(t) > 3 and t.endswith("s"):
        return t[:-1]
    return t


def lookup(tok: str):
    """Return lemma if tok (or its vowel-variant key) is a known lemma."""
    if tok in LEXICON:
        return tok
    return LEX_BY_KEY.get(phon_key(tok))


def lemmatize(tok: str):
    """Lexicon-guided affix stripping. Returns lemma or None."""
    hit = lookup(tok)
    if hit:
        return hit
    if len(tok) < 4:
        return None
    if "-" in tok:                                     # pag-adto, kanus-a, lakaw-lakaw
        joined = tok.replace("-", "")
        hit = lookup(joined) or lemmatize(joined)
        if hit:
            return hit
        parts = [p for p in tok.split("-") if p]
        if parts and parts[-1] == parts[0]:
            return lemmatize(parts[0])
        return lookup(parts[-1]) if parts else None
    half = len(tok) // 2
    if len(tok) % 2 == 0 and tok[:half] == tok[half:]:  # reduplication
        hit = lookup(tok[:half])
        if hit:
            return hit
    cands = [tok]
    for p in PREFIXES:
        if tok.startswith(p) and len(tok) - len(p) >= 3:
            cands.append(tok[len(p):])
    more = []
    for c in cands:
        for s in SUFFIXES:
            if c.endswith(s) and len(c) - len(s) >= 3:
                more.append(c[: -len(s)])
    cands += more
    m = re.match(r"^([bcdfghklmnprstvwy])(um|in)([a-z]{3,})$", tok)  # Tagalog infix: bumili -> bili
    if m:
        cands.append(m.group(1) + m.group(3))
    for c in cands[1:]:
        hit = lookup(c)
        if hit:
            return hit
    return None


@dataclass
class NormQuery:
    raw: str
    folded: str
    tokens: list = field(default_factory=list)      # expanded tokens for lexical channel
    weights: dict = field(default_factory=dict)      # token -> evidence weight (surface 1.0, projected gloss gamma)
    char_text: str = ""                              # text for character channel
    tags: list = field(default_factory=list)         # (surface, lang) per content token
    csi: float = 0.0                                 # code-switch index: share of ceb/tl tokens
    oov: float = 0.0                                 # share of tokens unknown to lexicon and KB vocab
    lex_hit: float = 0.0                             # share of tokens resolved through the lexicon
    n_tokens: int = 0


class Normalizer:
    def __init__(self, en_vocab: set, use_lexicon: bool = True, use_affix: bool = True, gamma: float = 0.6):
        self.en_vocab = en_vocab
        self.gamma = gamma
        self.use_lexicon = use_lexicon
        self.use_affix = use_affix

    def __call__(self, query: str) -> NormQuery:
        f = fold(query)
        words = []
        stack = f.split()[::-1]
        while stack:
            w = stack.pop()
            exp = CONTRACTIONS.get(w) if self.use_lexicon else None
            if exp is None or exp == w:
                words.append(w)
            elif exp:
                stack.extend(exp.split()[::-1])
        tokens, tags, glosses, weights = [], [], [], {}
        n_local = n_en = n_oov = n_lex = 0
        for w in words:
            if w in STOP:
                continue
            base = stem_en(w)
            in_en = w in self.en_vocab or base in self.en_vocab
            lemma = None
            if self.use_lexicon and (w in EN_GUARD and in_en) is False:
                lemma = lemmatize(w) if self.use_affix else lookup(w)
            if lemma:
                lang, gl = LEXICON[lemma]
                tokens.append(w)
                tokens.append(lemma)
                weights[w] = weights[lemma] = 1.0
                for g in gl:
                    for x in g.split():
                        if x in STOP:
                            continue
                        x = stem_en(x)
                        tokens.append(x)
                        weights[x] = max(weights.get(x, 0.0), self.gamma)
                glosses.extend(gl)
                tags.append((w, lang))
                n_local += 1
                n_lex += 1
            else:
                tokens.append(base)
                weights[base] = 1.0
                if in_en:
                    tags.append((w, "en"))
                    n_en += 1
                else:
                    tags.append((w, "unk"))
                    n_oov += 1
        n = max(1, n_local + n_en + n_oov)
        nq = NormQuery(raw=query, folded=f, tokens=tokens, tags=tags, weights=weights,
                       char_text=f + (" " + " ".join(glosses) if glosses else ""),
                       csi=n_local / max(1, n_local + n_en), oov=n_oov / n, lex_hit=n_lex / n,
                       n_tokens=n_local + n_en + n_oov)
        return nq


def kb_vocab(kb: dict) -> set:
    v = set(STOP)
    for e in kb["entries"]:
        text = " ".join([e["title"], " ".join(e["keywords"]), " ".join(e["questions"]), e["answer"]])
        for w in fold(text).split():
            v.add(w)
            v.add(stem_en(w))
    for w in "how much many price fee best good where when what places place day days month cheap safe help " \
             "number money food eat buy bring market beach island mountain falls church city town go ride".split():
        v.add(w)
    # remove words that are Cebuano lemmas but appear in KB answers as quoted phrases
    for w in ["salamat", "palihug", "lami", "maayong", "lugar", "buntag", "hapon", "gabii", "asa", "pila", "wala"]:
        v.discard(w)
    return v
