"""Frozen parameters and the per-subject feature extractor.

PARAMS is frozen BEFORE the A3 timing run and is cited (with this file's
sha256) by the analysis card.  Nothing in PARAMS was chosen from real-subject
output.

Density choice (synthetic evidence only, from explorer probes r1_1/r1_2/r1_3):
  10 % of unordered pairs (k = 4,606 at N=304) is the primary.  At 15 % sparse
  planted cycles are diluted (r1_1: N=60 planted min Z -0.32 at 15 % vs 4.17 at
  10 %); at 5 % latency-dominated graphs produce degenerate nulls (null SD 0)
  much more often.  5 % and 15 % are pre-registered sensitivities.  Z values
  are never pooled or compared across densities.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np

from .data import SubjectSeries
from .flow import (curl_component, gradient_share, lag_seconds_to_samples, lagged_net_flow,
                   oriented_topk_graph)
from .motifs import motif_statistics
from .preprocess import GRID_DT, preprocess

PARAMS: dict = {
    "version": "topic1_lagmotif v2.0 (2026-10-30)",
    "source": "raw npy MBBN_data_304_ROIs_0.25 (broadband); VMD cache IMF channels not used",
    "n_roi": 304,
    "head_trim_s": 40.0,              # ceil(40/TR) samples; = 20 samples at TR 2.0 (MBBN convention)
    "detrend": "linear",              # per ROI, native TR, BEFORE resampling
    "grid_dt_s": GRID_DT,             # common grid
    "resample": "scipy.signal.resample_poly, exact Fraction(TR)/2 ratio, padtype='line'",
    "padtype": "line",
    "highpass_cutoff_s": None,        # primary: none; sensitivity: DCT 128 s
    "lag_s": 2.0,                     # = 1 grid sample
    "density_primary": 0.10,
    "density_sensitivity": [0.05, 0.15],
    "channels": ["broadband", "curl"],  # curl = F minus Hodge gradient (descriptive sensitivity only)
    "n_null": 1000,
    "attempts_factor": 20,            # attempts per null = 20 * m, independent restart per null
    "p_rot": 0.2,                     # probability of a 3-edge rotation move per attempt
    "base_seed": 20261030,
    "seed_rule": "SeedSequence([base_seed, position, channel_code, density_code]).generate_state(n_null)",
    "z_rule": "Z = (obs - mean_null)/sd_null(ddof=1); NaN and flagged if sd_null == 0",
    "endpoints": ["E1 = Z030C", "E2 = Z030C - Z030T"],
}

CHANNEL_CODE = {"broadband": 0, "curl": 1}


def density_code(d: float) -> int:
    return int(round(d * 1000))


def params_sha256(params: dict = PARAMS) -> str:
    return hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()


def null_seeds(base_seed: int, position: int, channel: str, density: float, n_null: int) -> np.ndarray:
    ss = np.random.SeedSequence([int(base_seed), int(position), CHANNEL_CODE[channel], density_code(density)])
    return ss.generate_state(n_null, dtype=np.uint32).astype(np.int64)


def subject_flow(series: SubjectSeries, params: dict = PARAMS) -> np.ndarray:
    Z = preprocess(series.X, series.tr, detrend_type=params["detrend"], padtype=params["padtype"],
                   highpass_cutoff_s=params["highpass_cutoff_s"], grid_dt=params["grid_dt_s"])
    return lagged_net_flow(Z, lag_seconds_to_samples(params["lag_s"], params["grid_dt_s"]))


def flow_features(F: np.ndarray, position: int, params: dict = PARAMS, channels=None, densities=None,
                  n_null: int | None = None, attempts_factor: float | None = None) -> dict:
    channels = list(params["channels"]) if channels is None else list(channels)
    densities = ([params["density_primary"]] + list(params["density_sensitivity"])
                 if densities is None else list(densities))
    n_null = int(params["n_null"] if n_null is None else n_null)
    af = float(params["attempts_factor"] if attempts_factor is None else attempts_factor)
    out = {"gradient_share": gradient_share(F), "results": {}}
    for ch in channels:
        Fc = F if ch == "broadband" else curl_component(F)
        for d in densities:
            A = oriented_topk_graph(Fc, d)
            seeds = null_seeds(params["base_seed"], position, ch, d, n_null)
            out["results"][f"{ch}@{d:.2f}"] = motif_statistics(A, n_null, af, params["p_rot"], seeds)
    return out


def extract_subject(series: SubjectSeries, params: dict = PARAMS, **kw) -> dict:
    F = subject_flow(series, params)
    feats = flow_features(F, series.position, params, **kw)
    feats.update({"position": series.position, "tr": series.tr, "valid_T": series.valid_T,
                  "n_trim": series.n_trim, "duration_s": series.duration_s,
                  "raw_valid_T": series.raw_valid_T, "params_sha256": params_sha256(params)})
    return feats
