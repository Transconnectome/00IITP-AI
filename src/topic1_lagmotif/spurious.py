"""Spurious-direction characterization (ACCEPTANCE A2, last bullet).

Scenarios WITHOUT any directed neural coupling, run through the full v2 chain
(detrend -> resample -> z -> lag-2 s flow -> oriented graph -> oriented null):
  * ar_mismatch      independent AR(1) ROIs with heterogeneous phi ~ U(0.1, 0.9)
  * shared_zero_lag  zero-lag shared (global) signal, no latency
  * latency_sd_1s / latency_sd_2s  shared driver with per-ROI latency ~ N(0, sd)
  * hrf_peak_sd_1s   common neural driver, ROI-specific HRF peak shifts ~ N(0, 1 s)
plus the matched positive control (planted recursive 3-cycles).  For each the
mean over seeds of Z030C, Z030T, E2 = Z030C - Z030T and the gradient share are
reported, with NaN (degenerate-null) counts.  Run as a module to write JSON:

    PYTHONDONTWRITEBYTECODE=1 python -m src.topic1_lagmotif.spurious --out <file.json>
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np

from . import synthetic
from .flow import curl_component, gradient_share, lagged_net_flow, oriented_topk_graph
from .motifs import motif_statistics
from .preprocess import preprocess


def run_scenario(make, n_seeds: int, density: float, n_null: int, attempts_factor: float = 20,
                 p_rot: float = 0.2, tr: float = 2.0, base_seed: int = 7, curl: bool = False) -> dict:
    e1, e2, zt, gs = [], [], [], []
    n_nan = 0
    for s in range(n_seeds):
        rng = np.random.default_rng([base_seed, s])
        X = make(rng)
        F = lagged_net_flow(preprocess(X, tr), 1)
        gs.append(gradient_share(F))
        A = oriented_topk_graph(curl_component(F) if curl else F, density)
        seeds = np.random.SeedSequence([base_seed, s, 99]).generate_state(n_null, dtype=np.uint32).astype(np.int64)
        r = motif_statistics(A, n_null, attempts_factor, p_rot, seeds)
        if not (np.isfinite(r["Z"]["030C"]) and np.isfinite(r["Z"]["030T"])):
            n_nan += 1
            continue
        e1.append(r["Z"]["030C"]); zt.append(r["Z"]["030T"]); e2.append(r["E2_Z030C_minus_Z030T"])

    def summ(v):
        v = np.asarray(v, float)
        if v.size == 0:
            return {"mean": float("nan"), "sd": float("nan"), "se": float("nan"), "n": 0}
        sd = float(v.std(ddof=1)) if v.size > 1 else float("nan")
        return {"mean": float(v.mean()), "sd": sd, "se": sd / np.sqrt(v.size) if v.size > 1 else float("nan"),
                "n": int(v.size)}
    return {"Z030C": summ(e1), "Z030T": summ(zt), "E2": summ(e2), "gradient_share": summ(gs),
            "n_degenerate_excluded": n_nan, "n_seeds": n_seeds}


def scenarios(N: int = 60, T: int = 200):
    dur = T * 2.0
    return {
        "ar_mismatch": lambda rng: synthetic.ar1(T, rng.uniform(0.1, 0.9, N), rng),
        "planted_cycles_20_g0.8": lambda rng: synthetic.planted_cycles(T, N, 20, 0.8, rng)[0],
        "white_control": lambda rng: synthetic.planted_cycles(T, N, 20, 0.0, rng)[0],
        "shared_zero_lag_0.6": lambda rng: synthetic.shared_driver_latency(dur, N, 2.0, 0.0, 0.6 ** 0.5 / (1 - 0.6) ** 0.5, rng),
        "latency_sd_1s": lambda rng: synthetic.shared_driver_latency(dur, N, 2.0, 1.0, 1.0, rng),
        "latency_sd_2s": lambda rng: synthetic.shared_driver_latency(dur, N, 2.0, 2.0, 1.0, rng),
        "hrf_peak_sd_1s": lambda rng: synthetic.hrf_peak_delay(dur, N, 2.0, 1.0, 1.0, rng),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-seeds", type=int, default=12)
    ap.add_argument("--n-null", type=int, default=300)
    ap.add_argument("--densities", type=float, nargs="+", default=[0.05, 0.10, 0.15])
    a = ap.parse_args(argv)
    t0 = time.time()
    out = {"description": __doc__.strip().splitlines()[0], "N": 60, "T_grid": 200, "tr": 2.0,
           "n_seeds": a.n_seeds, "n_null": a.n_null, "attempts_factor": 20, "p_rot": 0.2, "results": {}}
    for name, make in scenarios().items():
        for d in a.densities:
            for curl in (False, True):
                key = f"{name}@{d:.2f}{'/curl' if curl else ''}"
                out["results"][key] = run_scenario(make, a.n_seeds, d, a.n_null, curl=curl)
    out["elapsed_s"] = time.time() - t0
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: (v["Z030C"]["mean"], v["Z030T"]["mean"], v["E2"]["mean"], v["n_degenerate_excluded"])
                      for k, v in out["results"].items()}, indent=0))


if __name__ == "__main__":
    main()
