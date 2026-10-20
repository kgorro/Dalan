"""Run with:  python -m pytest tests   (or: python tests/test_dalan.py)"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dalan import DALANRouter, Normalizer, kb_vocab  # noqa: E402
from dalan.normalize import lemmatize  # noqa: E402

KB = json.loads((ROOT / "kb" / "kb.json").read_text(encoding="utf-8"))
Q = [json.loads(l) for l in (ROOT / "data" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]


def test_affix_stripping():
    assert lemmatize("makapalit") == "palit"
    assert lemmatize("bumili") == "bili"           # Tagalog infix
    assert lemmatize("pag-adto") == "adto"
    assert lemmatize("kanus-a") == "kanusa"
    assert lemmatize("komosta") == "kumusta"       # e/i, o/u vowel variants
    assert lemmatize("papuntang") == "papunta"     # Tagalog linker -ng
    assert lemmatize("island") is None             # English words are not damaged


def test_projection_and_csi():
    n = Normalizer(kb_vocab(KB))
    nq = n("Asa ko makapalit og danggit?")
    assert "buy" in nq.tokens and "danggit" in nq.tokens
    assert nq.csi > 0.5
    assert n("How do I get to Bantayan island").csi == 0.0


def test_router_actions():
    r = DALANRouter(KB).fit(Q)
    assert r.route("Asa ko makapalit og danggit?")["entry"]["id"] == "p-danggit"
    assert r.route("How do I get to Bantayan?")["action"] == "skip"
    assert r.route("who won the nba finals")["action"] == "abstain"
    tau_skip, tau_abs = r.th.get("cs")
    assert tau_abs <= tau_skip


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
