"""Stage C and D of DALAN: confidence calibration and risk-controlled, language-conditioned thresholds.

Stage C  A logistic calibrator maps routing features to p = P(fused top-1 answer is correct).
         The features include code-switch statistics and their interaction with channel scores, so the model
         learns that the same lexical score is less trustworthy for a heavily code-switched or OOV-heavy query.

Stage D  Thresholds are chosen per language bucket g (en, cs) on calibration data:
           tau_skip(g)  smallest threshold whose SKIP set keeps precision >= 1 - eps   (risk control)
           tau_abs(g)   largest threshold that abstains on at most delta of the answerable queries
         Buckets with too little calibration data back off to global thresholds.
"""
import numpy as np

FEATURE_NAMES = [
    "lex_top_sat", "lex_margin", "char_top", "char_margin", "agree", "fused_margin",
    "csi", "oov", "log_len", "lex_hit", "csi_x_lex", "oov_x_char", "lex_char_rankgap",
]


def features(lex, char, fused, nq):
    lo = np.sort(lex)[::-1]
    co = np.sort(char)[::-1]
    fo = np.sort(fused)[::-1]
    l1, l2 = lo[0], lo[1]
    c1, c2 = co[0], co[1]
    top_l, top_c, top_f = int(np.argmax(lex)), int(np.argmax(char)), int(np.argmax(fused))
    lex_top_sat = l1 / (l1 + 5.0)
    rank_of_ltop_in_c = int((char > char[top_l]).sum())
    return np.array([
        lex_top_sat,
        (l1 - l2) / (l1 + 1e-6) if l1 > 0 else 0.0,
        c1,
        c1 - c2,
        1.0 if top_l == top_c else 0.0,
        (fo[0] - fo[1]) / (fo[0] + 1e-9),
        nq.csi,
        nq.oov,
        np.log1p(nq.n_tokens),
        nq.lex_hit,
        nq.csi * lex_top_sat,
        nq.oov * c1,
        1.0 / (1 + rank_of_ltop_in_c),
    ])


class LogisticCalibrator:
    def __init__(self, l2=1.0, iters=3000, lr=0.1):
        self.l2, self.iters, self.lr = l2, iters, lr

    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y, float)
        self.mu = X.mean(0)
        self.sd = X.std(0) + 1e-6
        Z = (X - self.mu) / self.sd
        n, d = Z.shape
        w = np.zeros(d)
        b = 0.0
        for _ in range(self.iters):
            p = 1 / (1 + np.exp(-(Z @ w + b)))
            g = p - y
            w -= self.lr * (Z.T @ g / n + self.l2 * w / n)
            b -= self.lr * g.mean()
        self.w, self.b = w, b
        return self

    def predict(self, X):
        Z = (np.atleast_2d(np.asarray(X, float)) - self.mu) / self.sd
        return 1 / (1 + np.exp(-(Z @ self.w + self.b)))


def skip_threshold(p, correct, eps, min_support=5):
    """Smallest tau such that precision of {p >= tau} >= 1 - eps with at least min_support items."""
    order = np.argsort(-p)
    ps, cs = p[order], np.asarray(correct, float)[order]
    cum = np.cumsum(cs) / np.arange(1, len(cs) + 1)
    best = 1.0 + 1e-9  # skip nothing by default
    for i in range(len(ps)):
        if i + 1 >= min_support and cum[i] >= 1 - eps:
            best = ps[i]
    return best


def abstain_threshold(p, answerable_in_ctx, delta):
    """Largest tau such that the share of answerable-in-context queries with p < tau is <= delta."""
    pa = np.sort(p[np.asarray(answerable_in_ctx, bool)])
    if len(pa) == 0:
        return 0.0
    k = int(np.floor(delta * len(pa)))
    return float(pa[k]) if k < len(pa) else 1.0


class BucketThresholds:
    def __init__(self, eps=0.05, delta=0.05, min_bucket=15):
        self.eps, self.delta, self.min_bucket = eps, delta, min_bucket
        self.t = {}

    def fit(self, p, correct, in_ctx, buckets):
        p, correct, in_ctx, buckets = map(np.asarray, (p, correct, in_ctx, buckets))
        self.t["_global"] = (skip_threshold(p, correct, self.eps), abstain_threshold(p, in_ctx, self.delta))
        for g in set(buckets.tolist()):
            m = buckets == g
            if m.sum() >= self.min_bucket:
                self.t[g] = (skip_threshold(p[m], correct[m], self.eps), abstain_threshold(p[m], in_ctx[m], self.delta))
        return self

    def get(self, bucket):
        tau_skip, tau_abs = self.t.get(bucket, self.t["_global"])
        return tau_skip, min(tau_abs, tau_skip)  # abstain band never overlaps the skip band
