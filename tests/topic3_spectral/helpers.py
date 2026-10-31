"""Shared helpers for topic3_spectral tests (plain module, not a pytest conftest)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
sys.dont_write_bytecode = True

import numpy as np  # noqa: E402


def exact_spectrum_matrix(n, singular_values, d, seed, offset_sd=0.0):
    """n x d matrix whose CENTERED singular values are exactly `singular_values` (k <= n-1),
    plus an optional constant row offset of `offset_sd` times the largest column SD."""
    rng = np.random.default_rng(seed)
    k = len(singular_values)
    U = rng.standard_normal((n, k))
    U -= U.mean(axis=0)                      # columns orthogonal to the ones vector
    U, _ = np.linalg.qr(U)                   # orthonormal and still centered
    V, _ = np.linalg.qr(rng.standard_normal((d, k)))
    X = (U * np.asarray(singular_values, dtype=float)) @ V.T
    if offset_sd:
        sd = X.std(axis=0).max()
        X = X + offset_sd * sd * (1.0 + rng.random(d))
    return X
