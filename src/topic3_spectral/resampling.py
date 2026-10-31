"""References, nulls and resampling for Topic 3 (numpy only, Python 3.8 compatible).

Design rules (frozen in the analysis card):
- Uncertainty for a PR computed on ONE matrix: jackknife (estimators.jackknife_pr) or
  paired m-out-of-n subsampling WITHOUT replacement. Never a with-replacement row
  bootstrap inside a PR (duplicated rows lower the rank and bias PR down).
- Per-subject token-level values (subject = unit): paired sign-flip permutation test and a
  subject-level percentile bootstrap of the mean difference (resampling subjects, which is
  valid because each subject contributes one scalar).
"""
import numpy as np

from .estimators import pr_cov


def iid_reference(n, d, reps, seed, estimator=pr_cov):
    """PR of iid standard-normal n x d matrices (Marchenko-Pastur reference at the real shape)."""
    rng = np.random.default_rng(seed)
    vals = np.array([estimator(rng.standard_normal((n, d))) for _ in range(reps)])
    return vals


def column_permutation_null(X, reps, seed, estimator=pr_cov):
    """PR after independently permuting each column across rows: keeps every column's
    marginal values, destroys cross-column dependence."""
    X = np.asarray(X, dtype=np.float64)
    rng = np.random.default_rng(seed)
    n, d = X.shape
    out = np.empty(reps)
    for b in range(reps):
        idx = np.argsort(rng.random((n, d)), axis=0)
        out[b] = estimator(np.take_along_axis(X, idx, axis=0))
    return out


def subsample_indices(n, m, S, seed):
    """S index sets of size m drawn WITHOUT replacement from range(n); shared across
    representations so the comparison is paired."""
    if not 1 < m < n:
        raise ValueError("need 1 < m < n")
    rng = np.random.default_rng(seed)
    return np.stack([rng.choice(n, m, replace=False) for _ in range(S)])


def paired_subsample_delta(XA, XB, m, S, seed, estimator=pr_cov, index_sets=None):
    """Stability interval for Delta_m = E[PR_m(A)] - E[PR_m(B)] on the same rows.

    Point = mean over S subsamples of PR(A[idx]) - PR(B[idx]); SE = sd * sqrt(m / (n - m))
    (finite-population subsampling rate, Politis-Romano style); interval = point +- 1.96 SE.
    Returns dict with point, se, lo, hi, frac_positive, m, S.
    """
    XA = np.asarray(XA, dtype=np.float64)
    XB = np.asarray(XB, dtype=np.float64)
    if XA.shape[0] != XB.shape[0]:
        raise ValueError("paired comparison needs the same rows")
    n = XA.shape[0]
    if index_sets is None:
        index_sets = subsample_indices(n, m, S, seed)
    d = np.array([estimator(XA[idx]) - estimator(XB[idx]) for idx in index_sets])
    point = float(d.mean())
    se = float(d.std() * np.sqrt(m / (n - m)))
    return {"point": point, "se": se, "lo": point - 1.96 * se, "hi": point + 1.96 * se,
            "frac_positive": float(np.mean(d > 0)), "m": int(m), "S": int(len(index_sets))}


def subsample_mean(X, m, S, seed, estimator=pr_cov, index_sets=None):
    """Mean and stability SE of PR at subsample size m (for matched-n comparisons)."""
    X = np.asarray(X, dtype=np.float64)
    n = X.shape[0]
    if index_sets is None:
        index_sets = subsample_indices(n, m, S, seed)
    v = np.array([estimator(X[idx]) for idx in index_sets])
    return {"mean": float(v.mean()), "se": float(v.std() * np.sqrt(m / (n - m))), "m": int(m), "S": int(len(index_sets))}


def sign_flip_test(diffs, reps, seed):
    """Two-sided paired sign-flip permutation p-value for mean(diffs) = 0.
    p = (1 + #{|mean*| >= |mean_obs|}) / (1 + reps)."""
    d = np.asarray(diffs, dtype=np.float64)
    rng = np.random.default_rng(seed)
    obs = abs(float(d.mean()))
    signs = rng.choice(np.array([-1.0, 1.0]), size=(reps, d.size))
    null = np.abs((signs * d).mean(axis=1))
    return float((1 + np.sum(null >= obs - 1e-15)) / (1 + reps))


def subject_bootstrap_ci(values, reps, seed, level=0.95):
    """Percentile bootstrap CI of the mean of per-subject scalars (subjects resampled)."""
    v = np.asarray(values, dtype=np.float64)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, v.size, size=(reps, v.size))
    means = v[idx].mean(axis=1)
    a = (1 - level) / 2
    return float(np.quantile(means, a)), float(np.quantile(means, 1 - a))


def holm(pvals):
    """Holm step-down adjusted p-values (same order as input)."""
    p = np.asarray(pvals, dtype=np.float64)
    k = p.size
    order = np.argsort(p)
    adj = np.empty(k)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (k - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj
