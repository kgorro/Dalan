"""Experiments for the DALAN router.

Protocol
  Repeated stratified 5-fold cross-validation (10 repeats, strata = language x in/out-of-domain).
  For trained methods, everything is fit on the training folds only: the gloss weight gamma (grid search),
  the calibrator, and the thresholds. Fixed-threshold baselines need no training.

Outcome model (per query, given the router's action)
  SKIP      correct if top-1 is gold; otherwise a SILENT ERROR (confident wrong answer, the worst case)
  GENERATE  the local LLM answers from the top-k context:
              gold in context  -> correct with probability rho      (reader accuracy)
              gold not present -> declines with probability rho_d, else hallucinates (wrong)
  ABSTAIN   correct for out-of-domain queries; a safe miss for answerable ones
  rho and rho_d are stated assumptions (main: 0.9 / 0.7, oracle: 1 / 1). Replace them with measured values once
  the local LLM is run on the same queries (see README).

Run:  python experiments/run_experiments.py   -> results/results.md, results/*.csv, results/*.png
"""
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dalan.calibrate import BucketThresholds, LogisticCalibrator, FEATURE_NAMES  # noqa: E402
from dalan.router import DALANRouter, bucket_of  # noqa: E402

RES = ROOT / "results"
RES.mkdir(exist_ok=True)
KB = json.loads((ROOT / "kb" / "kb.json").read_text(encoding="utf-8"))
Q = [json.loads(l) for l in (ROOT / "data" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
N = len(Q)
LANGS = ["en", "ceb", "tl", "mix"]
GAMMAS = [0.4, 0.6, 0.8, 1.0]
K_CTX = 3
RHO, RHO_D = 0.9, 0.7
T_LLM = {"gpu_7b_4bit": 1500.0, "cpu_3b_4bit": 8000.0}  # ms per generated answer (assumed, see README)
REPEATS, FOLDS, SEED = 10, 5, 7
CS_FEATS = [FEATURE_NAMES.index(f) for f in ["csi", "oov", "lex_hit", "csi_x_lex", "oov_x_char"]]

ood = np.array([q["gold"] == ["OOD"] for q in Q])
lang = np.array([q["lang"] for q in Q])


# ------------------------------------------------------------------ cached analysis per configuration
class Analysis:
    """Runs the DALAN front half (CSN + channels + fusion + features) once per query for one configuration."""

    def __init__(self, use_csn, use_char, gamma=0.6):
        r = DALANRouter(KB, use_csn=use_csn, use_char=use_char)
        r.norm.gamma = gamma
        self.ids = r.ids
        X, top1, inctx, buckets, lex1, char1, ms = [], [], [], [], [], [], []
        for q in Q:
            t0 = time.perf_counter()
            nq, x, order = r._analyze(q["q"])
            ms.append((time.perf_counter() - t0) * 1000)
            lex = r.lex.scores(nq)
            ch = r.char.scores(nq) if r.char else np.zeros_like(lex)
            gold = set(q["gold"])
            top = [r.ids[i] for i in order[:K_CTX]]
            X.append(x)
            top1.append(top[0] in gold)
            inctx.append(bool(gold & set(top)))
            buckets.append(bucket_of(nq))
            lex1.append((np.sort(lex)[::-1][:2], int(np.argmax(lex)) == int(np.argmax(ch))))
            char1.append(np.sort(ch)[::-1][0])
        self.X = np.array(X)
        self.top1 = np.array(top1)
        self.inctx = np.array(inctx)
        self.buckets = np.array(buckets)
        self.lex_top = np.array([l[0][0] for l in lex1])
        self.lex_margin = np.array([l[0][0] - l[0][1] for l in lex1])
        self.agree = np.array([l[1] for l in lex1])
        self.char_top = np.array(char1)
        self.ms = np.array(ms)


print("analyzing queries ...", flush=True)
CFG = {}
for csn in (False, True):
    for ch in (False, True):
        for g in (GAMMAS if csn else [1.0]):
            CFG[(csn, ch, g)] = Analysis(csn, ch, g)


# ------------------------------------------------------------------ decision rules
def fixed_lexical(a, idx):
    """Prototype rule: skip if lexical >= 6 or margin >= 3, abstain if lexical < 2.5, else generate."""
    act = np.full(len(idx), "generate", dtype=object)
    act[(a.lex_top[idx] >= 6) | ((a.lex_margin[idx] >= 3) & (a.lex_top[idx] >= 2.5))] = "skip"
    act[a.lex_top[idx] < 2.5] = "abstain"
    return act


def fixed_hybrid(a, idx, hi=6.0):
    """Prototype backend rule: lexical OR (strong char score AND agreement); abstain if both weak."""
    act = np.full(len(idx), "generate", dtype=object)
    lex_ok = (a.lex_top[idx] >= hi) | ((a.lex_margin[idx] >= 3) & (a.lex_top[idx] >= 2.5))
    act[lex_ok | ((a.char_top[idx] >= 0.5) & a.agree[idx])] = "skip"
    act[(a.lex_top[idx] < 2.5) & (a.char_top[idx] < 0.3)] = "abstain"
    return act


def always_rag(a, idx):
    return np.full(len(idx), "generate", dtype=object)


def train_calibrated(a, tr, eps, delta, per_language, mask_cs):
    X = a.X.copy()
    if mask_cs:
        X[:, CS_FEATS] = 0.0
    cal = LogisticCalibrator().fit(X[tr], a.top1[tr])
    p_tr = cal.predict(X[tr])
    b = a.buckets if per_language else np.array(["all"] * N)
    th = BucketThresholds(eps=eps, delta=delta).fit(p_tr, a.top1[tr], a.inctx[tr], b[tr])
    return cal, th, X, b


def calibrated(a, tr, te, eps=0.05, delta=0.05, per_language=True, mask_cs=False):
    cal, th, X, b = train_calibrated(a, tr, eps, delta, per_language, mask_cs)
    p = cal.predict(X[te])
    act = np.empty(len(te), dtype=object)
    for j, i in enumerate(te):
        ts, ta = th.get(b[i])
        act[j] = "skip" if p[j] >= ts else ("generate" if p[j] >= ta else "abstain")
    return act, p


def pick_gamma(use_char, tr):
    accs = {g: CFG[(True, use_char, g)].top1[tr][~ood[tr]].mean() for g in GAMMAS}
    return max(accs, key=lambda g: (accs[g], -abs(g - 0.6)))


# ------------------------------------------------------------------ outcome model
def outcomes(a, idx, act, rho=RHO, rho_d=RHO_D):
    """Returns per-query expected correct and expected wrong, plus action indicators."""
    c = np.zeros(len(idx))
    w = np.zeros(len(idx))
    for j, i in enumerate(idx):
        if ood[i]:
            if act[j] == "abstain":
                c[j] = 1
            elif act[j] == "skip":
                w[j] = 1
            else:
                c[j], w[j] = rho_d, 1 - rho_d
        else:
            if act[j] == "skip":
                c[j], w[j] = (1, 0) if a.top1[i] else (0, 1)
            elif act[j] == "generate":
                if a.inctx[i]:
                    c[j], w[j] = rho, 1 - rho
                else:
                    c[j], w[j] = 0, 1 - rho_d
    return c, w


def metrics(a, idx, act, rho=RHO, rho_d=RHO_D):
    c, w = outcomes(a, idx, act, rho, rho_d)
    skip = act == "skip"
    gen = act == "generate"
    abst = act == "abstain"
    ans = ~ood[idx]
    silent = skip & ((ood[idx]) | (~a.top1[idx]))
    route_ms = a.ms[idx].mean()
    m = dict(
        accuracy=c.mean(), wrong=w.mean(), silent_err=silent.mean(),
        skip_rate=skip.mean(), llm_rate=gen.mean(), abstain_rate=abst.mean(),
        skip_precision=(a.top1[idx][skip & ans].sum() / max(1, skip.sum())),
        ood_abstain_recall=(abst & ood[idx]).sum() / max(1, ood[idx].sum()),
        answerable_abstain=(abst & ans).sum() / max(1, ans.sum()),
        route_ms=route_ms,
    )
    for k, t in T_LLM.items():
        m[f"latency_{k}_ms"] = route_ms + gen.mean() * t
    return m


# ------------------------------------------------------------------ cross-validation
def folds(rng):
    strata = defaultdict(list)
    for i in range(N):
        strata[(lang[i], ood[i])].append(i)
    fold_of = np.zeros(N, int)
    for ids in strata.values():
        ids = rng.permutation(ids)
        for k, i in enumerate(ids):
            fold_of[i] = k % FOLDS
    return [(np.where(fold_of != f)[0], np.where(fold_of == f)[0]) for f in range(FOLDS)]


METHODS = {
    "B0 Always-RAG (LLM for every query)": lambda tr, te: (CFG[(False, False, 1.0)], always_rag(CFG[(False, False, 1.0)], te)),
    "B1 Lexical, fixed thresholds (prototype)": lambda tr, te: (CFG[(False, False, 1.0)], fixed_lexical(CFG[(False, False, 1.0)], te)),
    "B2 Hybrid lexical+char, fixed thresholds": lambda tr, te: (CFG[(False, True, 1.0)], fixed_hybrid(CFG[(False, True, 1.0)], te)),
    "B3 CSN + hybrid, fixed thresholds": lambda tr, te: (lambda g: (CFG[(True, True, g)], fixed_hybrid(CFG[(True, True, g)], te)))(pick_gamma(True, tr)),
    "A1 DALAN without CSN": lambda tr, te: (CFG[(False, True, 1.0)], calibrated(CFG[(False, True, 1.0)], tr, te)[0]),
    "A2 DALAN without char channel": lambda tr, te: (lambda g: (CFG[(True, False, g)], calibrated(CFG[(True, False, g)], tr, te)[0]))(pick_gamma(False, tr)),
    "A3 DALAN without code-switch features": lambda tr, te: (lambda g: (CFG[(True, True, g)], calibrated(CFG[(True, True, g)], tr, te, mask_cs=True)[0]))(pick_gamma(True, tr)),
    "A4 DALAN with global thresholds": lambda tr, te: (lambda g: (CFG[(True, True, g)], calibrated(CFG[(True, True, g)], tr, te, per_language=False)[0]))(pick_gamma(True, tr)),
    "DALAN (full)": lambda tr, te: (lambda g: (CFG[(True, True, g)], calibrated(CFG[(True, True, g)], tr, te)[0]))(pick_gamma(True, tr)),
}

print("cross-validating ...", flush=True)
rng = np.random.default_rng(SEED)
per_fold = defaultdict(list)          # method -> list of metric dicts (one per fold)
per_lang = defaultdict(lambda: defaultdict(list))
oracle = defaultdict(list)
gammas_chosen = []
splits = [s for _ in range(REPEATS) for s in folds(rng)]
for tr, te in splits:
    gammas_chosen.append(pick_gamma(True, tr))
    for name, fn in METHODS.items():
        a, act = fn(tr, te)
        per_fold[name].append(metrics(a, te, act))
        oracle[name].append(metrics(a, te, act, rho=1.0, rho_d=1.0))
        for L in LANGS:
            m = lang[te] == L
            per_lang[name][L].append(metrics(a, te[m], act[m]))


def agg(lst, key):
    v = np.array([d[key] for d in lst])
    return v.mean(), v.std()


# ------------------------------------------------------------------ significance (paired over folds)
from scipy.stats import wilcoxon  # noqa: E402

full = "DALAN (full)"
sig = {}
for name in METHODS:
    if name == full:
        continue
    out = {}
    for key in ("accuracy", "wrong", "llm_rate"):
        a = np.array([d[key] for d in per_fold[full]])
        b = np.array([d[key] for d in per_fold[name]])
        diff = a - b
        out[key] = wilcoxon(a, b).pvalue if np.any(diff != 0) else 1.0
    sig[name] = out


# ------------------------------------------------------------------ calibration quality (pooled out-of-fold)
def ece(p, y, bins=10):
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (p >= lo) & (p < hi) if hi < 1 else (p >= lo) & (p <= hi)
        if m.any():
            e += m.mean() * abs(p[m].mean() - y[m].mean())
    return e


cal_report = {}
for label, mask_cs in (("DALAN (full)", False), ("A3 without code-switch features", True)):
    ps, ys, bs = [], [], []
    for tr, te in splits[:FOLDS]:
        g = pick_gamma(True, tr)
        a = CFG[(True, True, g)]
        _, p = calibrated(a, tr, te, mask_cs=mask_cs)
        ps.append(p)
        ys.append(a.top1[te].astype(float))
        bs.append(a.buckets[te])
    p, y, b = np.concatenate(ps), np.concatenate(ys), np.concatenate(bs)
    cal_report[label] = {
        "ECE all": ece(p, y), "Brier all": float(np.mean((p - y) ** 2)),
        "ECE code-switched": ece(p[b == "cs"], y[b == "cs"]), "ECE english": ece(p[b == "en"], y[b == "en"]),
    }


# ------------------------------------------------------------------ Pareto sweep: LLM call rate vs wrong-answer rate
print("sweeping operating points ...", flush=True)
pareto = defaultdict(list)
sweep_splits = splits[:FOLDS * 3]
for eps in [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]:
    ms = []
    for tr, te in sweep_splits:
        g = pick_gamma(True, tr)
        a = CFG[(True, True, g)]
        act, _ = calibrated(a, tr, te, eps=eps)
        ms.append(metrics(a, te, act))
    pareto["DALAN (eps sweep)"].append((eps, np.mean([m["llm_rate"] for m in ms]), np.mean([m["wrong"] for m in ms]), np.mean([m["accuracy"] for m in ms])))
for hi in [3, 4, 5, 6, 8, 10, 12, 15, 20]:
    ms = []
    for tr, te in sweep_splits:
        a = CFG[(False, True, 1.0)]
        ms.append(metrics(a, te, fixed_hybrid(a, te, hi=hi)))
    pareto["B2 hybrid (threshold sweep)"].append((hi, np.mean([m["llm_rate"] for m in ms]), np.mean([m["wrong"] for m in ms]), np.mean([m["accuracy"] for m in ms])))
    ms = []
    for tr, te in sweep_splits:
        g = pick_gamma(True, tr)
        a = CFG[(True, True, g)]
        ms.append(metrics(a, te, fixed_hybrid(a, te, hi=hi)))
    pareto["B3 CSN + hybrid (threshold sweep)"].append((hi, np.mean([m["llm_rate"] for m in ms]), np.mean([m["wrong"] for m in ms]), np.mean([m["accuracy"] for m in ms])))

with open(RES / "pareto.csv", "w") as f:
    f.write("method,param,llm_rate,wrong_rate,accuracy\n")
    for name, pts in pareto.items():
        for prm, lr, wr, acc in pts:
            f.write(f"{name},{prm},{lr:.4f},{wr:.4f},{acc:.4f}\n")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=160)
    styles = {"DALAN (eps sweep)": ("#0b6a70", "o"), "B2 hybrid (threshold sweep)": ("#c2502e", "s"),
              "B3 CSN + hybrid (threshold sweep)": ("#7a6a2a", "^")}
    for name, pts in pareto.items():
        pts = sorted(pts, key=lambda t: t[1])
        col, mk = styles[name]
        ax.plot([p[1] * 100 for p in pts], [p[2] * 100 for p in pts], marker=mk, color=col, label=name, lw=1.6, ms=5)
    ax.set_xlabel("LLM call rate (% of queries)")
    ax.set_ylabel("Wrong-answer rate (%)")
    ax.set_title("Cost vs safety: lower-left is better")
    ax.grid(alpha=.3)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(RES / "pareto.png")
except Exception as ex:  # plotting is optional
    print("plot skipped:", ex)


# ------------------------------------------------------------------ write report
def pct(x):
    return f"{x * 100:.1f}"


lines = []
lines.append("# DALAN experiment results\n")
lines.append(f"Seed evaluation set: {N} queries ({(~ood).sum()} answerable, {ood.sum()} out-of-domain); "
             f"languages: " + ", ".join(f"{L}={int((lang == L).sum())}" for L in LANGS) + ".")
lines.append(f"Protocol: {REPEATS} x {FOLDS}-fold stratified CV ({len(splits)} folds). Mean +/- SD over folds. "
             f"Reader assumptions rho={RHO}, rho_d={RHO_D}. eps=delta=0.05 for DALAN.\n")
lines.append("## Main results\n")
lines.append("| Method | Accuracy % | Wrong % | Silent err % | LLM calls % | Skip % | Abstain % | OOD abstain recall % | Latency GPU ms | Latency CPU ms |")
lines.append("|---|---|---|---|---|---|---|---|---|---|")
for name in METHODS:
    L = per_fold[name]
    row = [name]
    for key in ("accuracy", "wrong", "silent_err", "llm_rate", "skip_rate", "abstain_rate", "ood_abstain_recall"):
        m, s = agg(L, key)
        row.append(f"{pct(m)} +/- {pct(s)}")
    row.append(f"{agg(L, 'latency_gpu_7b_4bit_ms')[0]:.0f}")
    row.append(f"{agg(L, 'latency_cpu_3b_4bit_ms')[0]:.0f}")
    lines.append("| " + " | ".join(row) + " |")
lines.append("\nLatency = measured routing time + LLM call rate x assumed generation time "
             f"({T_LLM['gpu_7b_4bit']:.0f} ms GPU 7B 4-bit, {T_LLM['cpu_3b_4bit']:.0f} ms CPU 3B 4-bit).")
lines.append(f"Mean routing time for DALAN: {CFG[(True, True, 0.6)].ms.mean():.2f} ms per query (Python, single core).\n")

lines.append("## Accuracy by language (DALAN vs baselines)\n")
lines.append("| Method | " + " | ".join(f"{L} acc %" for L in LANGS) + " | " + " | ".join(f"{L} wrong %" for L in LANGS) + " |")
lines.append("|---|" + "---|" * (2 * len(LANGS)))
for name in ["B1 Lexical, fixed thresholds (prototype)", "B2 Hybrid lexical+char, fixed thresholds",
             "B3 CSN + hybrid, fixed thresholds", "A1 DALAN without CSN", "DALAN (full)"]:
    accs = [pct(agg(per_lang[name][L], "accuracy")[0]) for L in LANGS]
    wrs = [pct(agg(per_lang[name][L], "wrong")[0]) for L in LANGS]
    lines.append(f"| {name} | " + " | ".join(accs) + " | " + " | ".join(wrs) + " |")

lines.append("\n## Oracle reader (rho = rho_d = 1)\n")
lines.append("| Method | Accuracy % | Wrong % | LLM calls % |")
lines.append("|---|---|---|---|")
for name in METHODS:
    lines.append(f"| {name} | {pct(agg(oracle[name], 'accuracy')[0])} | {pct(agg(oracle[name], 'wrong')[0])} | {pct(agg(oracle[name], 'llm_rate')[0])} |")

lines.append("\n## Paired Wilcoxon signed-rank tests vs DALAN (full), p-values over folds\n")
lines.append("| Compared with | Accuracy | Wrong-answer rate | LLM call rate |")
lines.append("|---|---|---|---|")
for name, d in sig.items():
    lines.append(f"| {name} | {d['accuracy']:.2g} | {d['wrong']:.2g} | {d['llm_rate']:.2g} |")
lines.append("\nFolds from repeated CV are not independent, so treat these p-values as indicative; "
             "confirm on a held-out real-query test set.")

lines.append("\n## Calibration quality (pooled out-of-fold predictions, first repeat)\n")
lines.append("| Calibrator | ECE all | Brier all | ECE code-switched | ECE English |")
lines.append("|---|---|---|---|---|")
for k, v in cal_report.items():
    lines.append(f"| {k} | {v['ECE all']:.3f} | {v['Brier all']:.3f} | {v['ECE code-switched']:.3f} | {v['ECE english']:.3f} |")

lines.append("\n## Operating points (Pareto sweep, see pareto.png / pareto.csv)\n")
lines.append("| Method | param | LLM calls % | Wrong % | Accuracy % |")
lines.append("|---|---|---|---|---|")
for name, pts in pareto.items():
    for prm, lr, wr, acc in pts:
        lines.append(f"| {name} | {prm} | {pct(lr)} | {pct(wr)} | {pct(acc)} |")

vals, cnts = np.unique(gammas_chosen, return_counts=True)
lines.append("\nGloss weight gamma chosen on training folds: " + ", ".join(f"{v}: {c} folds" for v, c in zip(vals, cnts)) + ".")

(RES / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
with open(RES / "summary.csv", "w") as f:
    keys = ["accuracy", "wrong", "silent_err", "llm_rate", "skip_rate", "abstain_rate", "ood_abstain_recall",
            "latency_gpu_7b_4bit_ms", "latency_cpu_3b_4bit_ms"]
    f.write("method," + ",".join(f"{k}_mean,{k}_sd" for k in keys) + "\n")
    for name in METHODS:
        f.write(name + "," + ",".join(f"{agg(per_fold[name], k)[0]:.5f},{agg(per_fold[name], k)[1]:.5f}" for k in keys) + "\n")
print((RES / "results.md").read_text())
