"""Spectral estimators for Topic 3 (layerwise participation ratio / spectral decay).

All estimators CENTER the data (column means removed) before any spectrum is taken.
This is the fix for the defect in the protected src/spectral_rg_flow_diagnostic.py
(compute_participation_ratio takes the SVD of the uncentered matrix, so the mean
vector dominates and PR comes out near 1).

Python 3.8 / numpy 1.22 compatible (runs on connectome system python): no
PEP 585 generics, no 3.9+ APIs, numpy only.
"""
import math

import numpy as np

LN_EPS = 1e-5            # torch.nn.LayerNorm default eps (ver11 uses nn.LayerNorm defaults)
VAR_FLOOR_FRAC = 1e-3    # corrPR: drop only numerically dead columns (SD <= 1e-3 * median SD);
                         # a larger floor would break exact invariance to per-channel gain
EIG_REL_TOL = 1e-10      # eigenvalues below tol * max are treated as exact zeros


def _as_2d_float64(X):
    X = np.asarray(X, dtype=np.float64)
    if X.ndim != 2:
        raise ValueError("expected a 2-D matrix (rows = samples, cols = dims), got ndim=%d" % X.ndim)
    if X.shape[0] < 2:
        raise ValueError("need at least 2 rows")
    if not np.all(np.isfinite(X)):
        raise ValueError("non-finite values in input")
    return X


def centered_eigs(X):
    """Non-negative eigenvalues (descending) of the centered covariance (1/n) Xc^T Xc.

    Uses the Gram trick (1/n) Xc Xc^T when n < D; both share the same non-zero
    eigenvalues. Returns at most min(n - 1, D) values (centering removes one rank).
    """
    X = _as_2d_float64(X)
    n, d = X.shape
    Xc = X - X.mean(axis=0, keepdims=True)
    if n < d:
        M = Xc @ Xc.T / n
    else:
        M = Xc.T @ Xc / n
    ev = np.linalg.eigvalsh(M)[::-1]
    ev = np.clip(ev, 0.0, None)
    r = min(n - 1, d)
    return ev[:r].copy()


def pr_from_eigs(ev):
    """Participation ratio (sum l)^2 / sum l^2 of a non-negative spectrum."""
    ev = np.asarray(ev, dtype=np.float64)
    s2 = float(np.sum(ev ** 2))
    if s2 <= 0.0:
        raise ValueError("all-zero spectrum: PR undefined")
    return float(np.sum(ev) ** 2 / s2)


def pr_cov(X):
    """Centered covariance participation ratio."""
    return pr_from_eigs(centered_eigs(X))


def standardize_columns(X, floor_frac=VAR_FLOOR_FRAC):
    """Center and scale columns to unit SD; drop columns with SD <= floor_frac * median SD.

    Returns (Z, n_dropped). The variance floor protects against dividing by
    near-zero SD (dead channels inflating corrPR).
    """
    X = _as_2d_float64(X)
    Xc = X - X.mean(axis=0, keepdims=True)
    sd = Xc.std(axis=0)
    med = float(np.median(sd))
    if med <= 0.0:
        raise ValueError("median column SD is zero")
    keep = sd > max(floor_frac * med, 1e-12)
    Z = Xc[:, keep] / sd[keep]
    return Z, int(np.sum(~keep))


def corr_eigs(X, floor_frac=VAR_FLOOR_FRAC):
    """Eigenvalues of the correlation matrix (column-standardized covariance)."""
    Z, n_drop = standardize_columns(X, floor_frac)
    return centered_eigs(Z), n_drop


def pr_corr(X, floor_frac=VAR_FLOOR_FRAC):
    """Correlation-matrix participation ratio. Exactly invariant to per-column affine maps
    x_j -> g_j x_j + b_j (g_j != 0), e.g. the LayerNorm gain/bias applied to pooled vectors."""
    ev, _ = corr_eigs(X, floor_frac)
    return pr_from_eigs(ev)


def layernorm0(X, eps=LN_EPS):
    """Parameter-free per-row (per-token) LayerNorm: (x - mean_row) / sqrt(var_row + eps)."""
    X = _as_2d_float64(X)
    mu = X.mean(axis=1, keepdims=True)
    var = X.var(axis=1, keepdims=True)
    return (X - mu) / np.sqrt(var + eps)


def layer3_tokens(t):
    """ver11 layer_3 dump (C, D, H, W, T) -> token matrix (T*D*H*W, C) in the model's
    native token order (t, d, h, w): the model builds the dump as
    view(b, c, t, d, h, w).permute(0, 1, 3, 4, 5, 2), so permute(4, 1, 2, 3, 0) inverts it."""
    t = np.asarray(t)
    if t.ndim != 5:
        raise ValueError("layer_3 dump must be 5-D (C, D, H, W, T)")
    c = t.shape[0]
    return np.ascontiguousarray(np.transpose(t, (4, 1, 2, 3, 0))).reshape(-1, c)


def nonzero_eigs(ev, rel_tol=EIG_REL_TOL):
    ev = np.asarray(ev, dtype=np.float64)
    if ev.size == 0 or ev[0] <= 0:
        return ev[:0]
    return ev[ev > rel_tol * ev[0]]


def rank_slope(ev, kmin=2, kmax=None):
    """Rank-decay exponent a from OLS of log l_k on log k over k in [kmin, kmax] (1-based).

    Descriptive only. kmax defaults to floor(r / 2), r = number of non-zero eigenvalues.
    Exact on an exact power law l_k = c k^-a.
    """
    ev = nonzero_eigs(ev)
    r = ev.size
    if kmax is None:
        kmax = r // 2
    kmax = min(int(kmax), r)
    if kmax - kmin + 1 < 5:
        raise ValueError("fewer than 5 eigenvalues in the fit window")
    k = np.arange(kmin, kmax + 1, dtype=np.float64)
    y = np.log(ev[kmin - 1:kmax])
    slope = np.polyfit(np.log(k), y, 1)[0]
    return float(-slope)


def clauset_mle(x, min_tail=10):
    """Continuous power-law MLE with KS-chosen xmin (Clauset, Shalizi & Newman 2009).

    For each candidate xmin (each distinct value leaving >= min_tail points in the tail),
    alpha_hat = 1 + n_tail / sum(log(x / xmin)); the xmin with minimum KS distance between
    the empirical tail CDF and the fitted CDF is chosen. Returns dict(alpha, xmin, n_tail, ks).
    alpha is the DENSITY exponent p(x) ~ x^-alpha. For a rank law l_k ~ k^-a the density
    exponent is 1 + 1/a.
    """
    x = np.sort(np.asarray(x, dtype=np.float64))
    x = x[x > 0]
    n = x.size
    if n < min_tail:
        raise ValueError("fewer than min_tail positive values")
    logx = np.log(x)
    # suffix sums of log x for O(1) tail sums
    suffix = np.cumsum(logx[::-1])[::-1]
    best = None
    for i in range(0, n - min_tail + 1):
        if i > 0 and x[i] == x[i - 1]:
            continue
        xmin = x[i]
        nt = n - i
        denom = suffix[i] - nt * logx[i]
        if denom <= 0:
            continue
        alpha = 1.0 + nt / denom
        tail = x[i:]
        emp = np.arange(nt, dtype=np.float64) / nt          # empirical CDF just below each point
        emp_hi = np.arange(1, nt + 1, dtype=np.float64) / nt
        fit = 1.0 - (tail / xmin) ** (1.0 - alpha)
        ks = float(max(np.max(np.abs(emp - fit)), np.max(np.abs(emp_hi - fit))))
        if best is None or ks < best["ks"]:
            best = {"alpha": float(alpha), "xmin": float(xmin), "n_tail": int(nt), "ks": ks}
    if best is None:
        raise ValueError("no valid xmin")
    return best


def jackknife_pr(X, estimator=pr_cov):
    """Leave-one-row-out jackknife for a PR estimator: returns (estimate, jackknife SE, bias-corrected).
    Never resamples rows with replacement (duplicated rows shrink PR)."""
    X = _as_2d_float64(X)
    n = X.shape[0]
    full = estimator(X)
    loo = np.array([estimator(np.delete(X, i, axis=0)) for i in range(n)])
    mean_loo = float(loo.mean())
    se = math.sqrt((n - 1) / n * float(np.sum((loo - mean_loo) ** 2)))
    bc = n * full - (n - 1) * mean_loo
    return float(full), float(se), float(bc)


def mean_energy_fraction(X):
    """Share of the UNCENTERED second moment carried by the column-mean vector:
    n * ||mean||^2 / ||X||_F^2. Near 1 => uncentered spectra are dominated by the mean."""
    X = _as_2d_float64(X)
    mu = X.mean(axis=0)
    return float(X.shape[0] * np.sum(mu ** 2) / np.sum(X ** 2))
