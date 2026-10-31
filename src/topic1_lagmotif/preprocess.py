"""Native-TR series -> z-scored series on the common 2.0 s grid.

Order (mandatory; see OPEN_ISSUES "detrend before resample"):
  1. per-ROI linear detrend at native TR (removes the ~1.15e4 raw offset and
     linear drift; resampling raw-scale data first produces large edge
     transients because resample_poly pads),
  2. ``scipy.signal.resample_poly`` to dt = 2.0 s with exact rational ratio
     up/down = Fraction(TR)/Fraction(2.0) (0.7->7/20, 0.8->2/5, 0.85->17/40,
     1.0->1/2, 1.73->173/200, 1.8->9/10, 2.0 -> no resampling),
     ``padtype='line'``,
  3. optional DCT high-pass (sensitivity analysis only),
  4. per-ROI z-score (ddof=0).
The raw npy series are already low-passed near 0.25 Hz (survey), which is the
Nyquist frequency of the 2.0 s grid, so the anti-aliasing filter removes little.
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.signal import detrend, resample_poly

GRID_DT = 2.0


def resample_ratio(tr: float, grid_dt: float = GRID_DT) -> tuple[int, int]:
    fr = (Fraction(str(tr)) / Fraction(str(grid_dt))).limit_denominator(1000)
    return fr.numerator, fr.denominator


def resample_to_grid(X: np.ndarray, tr: float, grid_dt: float = GRID_DT, padtype: str = "line") -> np.ndarray:
    up, down = resample_ratio(tr, grid_dt)
    if up == down:
        return np.array(X, dtype=np.float64, copy=True)
    if up > down:
        raise ValueError(f"TR {tr} s is slower than the {grid_dt} s grid")
    return resample_poly(np.asarray(X, dtype=np.float64), up, down, axis=0, padtype=padtype)


def dct_highpass(X: np.ndarray, dt: float, cutoff_s: float) -> np.ndarray:
    """Regress out DCT-II basis functions with period > cutoff_s (SPM convention)."""
    T = X.shape[0]
    K = int(np.floor(2.0 * T * dt / cutoff_s)) + 1
    if K <= 1:
        return X - X.mean(axis=0)
    n = np.arange(T)
    basis = np.stack([np.cos(np.pi * k * (2 * n + 1) / (2 * T)) for k in range(K)], axis=1)
    beta, *_ = np.linalg.lstsq(basis, X, rcond=None)
    return X - basis @ beta


def zscore(X: np.ndarray) -> np.ndarray:
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    if np.any(sd <= 0):
        raise ValueError("zero-variance ROI after preprocessing")
    return (X - mu) / sd


def preprocess(X: np.ndarray, tr: float, detrend_type: str = "linear", padtype: str = "line",
               highpass_cutoff_s: float | None = None, grid_dt: float = GRID_DT) -> np.ndarray:
    """Return the z-scored series on the common grid. ``detrend_type='none'`` exists only so that
    the order fixture can demonstrate the defect it guards against."""
    Y = np.asarray(X, dtype=np.float64)
    if detrend_type == "linear":
        Y = detrend(Y, axis=0, type="linear")
    elif detrend_type == "constant":
        Y = Y - Y.mean(axis=0)
    elif detrend_type != "none":
        raise ValueError(f"unknown detrend_type {detrend_type}")
    Y = resample_to_grid(Y, tr, grid_dt, padtype=padtype)
    if highpass_cutoff_s is not None:
        Y = dct_highpass(Y, grid_dt, highpass_cutoff_s)
    return zscore(Y)
