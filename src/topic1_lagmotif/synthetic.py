"""Synthetic generators with known ground truth (used by fixtures and the
spurious-direction characterization). All return arrays shaped (T, N)."""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfiltfilt
from scipy.stats import gamma


def ar1(T: int, phis: np.ndarray, rng: np.random.Generator, burn: int = 200) -> np.ndarray:
    phis = np.asarray(phis, dtype=float)
    N = phis.size
    x = np.zeros((T + burn, N))
    e = rng.standard_normal((T + burn, N))
    for t in range(1, T + burn):
        x[t] = phis * x[t - 1] + e[t]
    return x[burn:]


def planted_cycles(T: int, N: int, n_cycles: int, gain: float, rng: np.random.Generator,
                   burn: int = 200) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    """Recursive VAR(1) x_t = gain * P x_{t-1} + e_t where P encodes n_cycles disjoint
    directed 3-cycles a->b->c->a on randomly chosen nodes (white background).
    gain = 0 gives the matched no-injection control (pure white noise)."""
    if 3 * n_cycles > N:
        raise ValueError("not enough nodes for disjoint cycles")
    nodes = rng.permutation(N)[: 3 * n_cycles].reshape(n_cycles, 3)
    P = np.zeros((N, N))
    cycles = []
    for a, b, c in nodes:
        P[b, a] = 1.0; P[c, b] = 1.0; P[a, c] = 1.0   # b(t) <- a(t-1), etc.
        cycles.append((int(a), int(b), int(c)))
    x = np.zeros((T + burn, N))
    e = rng.standard_normal((T + burn, N))
    for t in range(1, T + burn):
        x[t] = gain * (P @ x[t - 1]) + e[t]
    return x[burn:], cycles


def bandlimited_sources(duration_s: float, n: int, dt: float, f_hi: float,
                        rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Independent band-limited (< f_hi Hz) Gaussian sources on a fine time grid."""
    T = int(round(duration_s / dt))
    sos = butter(6, f_hi, btype="low", fs=1.0 / dt, output="sos")
    s = sosfiltfilt(sos, rng.standard_normal((T + 2000, n)), axis=0)[1000:1000 + T]
    s /= s.std(axis=0)
    return np.arange(T) * dt, s


def canonical_hrf(dt: float, peak_shift_s: float = 0.0, length_s: float = 32.0) -> np.ndarray:
    t = np.arange(0, length_s, dt) - peak_shift_s
    t = np.clip(t, 0, None)
    h = gamma.pdf(t, 6) - gamma.pdf(t, 16) / 6.0
    return h / np.abs(h).sum()


def shared_driver_latency(duration_s: float, N: int, tr: float, latency_sd_s: float, shared: float,
                          rng: np.random.Generator, dt: float = 0.1, f_hi: float = 0.2) -> np.ndarray:
    """No directed neural coupling.  Each ROI = shared * (common driver shifted by its own
    latency delta_i ~ N(0, latency_sd_s)) + private band-limited noise, then sampled at TR.
    latency_sd_s = 0 with shared > 0 is a zero-lag shared (global) signal."""
    t, src = bandlimited_sources(duration_s + 40.0, N + 1, dt, f_hi, rng)
    drv = src[:, 0]
    priv = src[:, 1:]
    delta = rng.normal(0.0, latency_sd_s, size=N) if latency_sd_s > 0 else np.zeros(N)
    X = np.empty_like(priv)
    for i in range(N):
        X[:, i] = shared * np.interp(t - delta[i], t, drv) + priv[:, i]
    keep = slice(int(20.0 / dt), int(20.0 / dt) + int(round(duration_s / dt)))
    X = X[keep]
    step = int(round(tr / dt))
    return X[::step]


def hrf_peak_delay(duration_s: float, N: int, tr: float, peak_sd_s: float, shared: float,
                   rng: np.random.Generator, dt: float = 0.1) -> np.ndarray:
    """No neural delay: a common neural driver plus private noise is convolved with an
    ROI-specific HRF whose peak is shifted by ~N(0, peak_sd_s), then sampled at TR."""
    t, src = bandlimited_sources(duration_s + 60.0, N + 1, dt, 0.25, rng)
    drv, priv = src[:, 0], src[:, 1:]
    shifts = rng.normal(0.0, peak_sd_s, size=N)
    X = np.empty_like(priv)
    for i in range(N):
        h = canonical_hrf(dt, peak_shift_s=max(shifts[i] + 0.0, -4.0))
        neural = shared * drv + priv[:, i]
        X[:, i] = np.convolve(neural, h)[: neural.size]
    keep = slice(int(40.0 / dt), int(40.0 / dt) + int(round(duration_s / dt)))
    return X[keep][:: int(round(tr / dt))]
