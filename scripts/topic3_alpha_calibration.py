"""Topic 3 — SYNTHETIC-ONLY calibration of the decay-exponent estimators at every real analysis shape.

Decides, before the card is frozen, at which (n, D) an alpha may be reported at all.
Population spectrum l_i = i^-a (i = 1..D), a in PARAMS["alpha_test_rank_exponents"]; rows are
iid Gaussian with that covariance. For each estimator the bias is
  sampled-data estimate - estimate on the population spectrum truncated to rank r = min(n-1, D).
A shape is ESTIMABLE for an estimator iff |mean bias| <= PARAMS["alpha_bias_tol"] for every a.
No real data are read.

Run: cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=8 \
     nice -n 10 /home/juke/superclaude-env/bin/python3 scripts/topic3_alpha_calibration.py
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

from src.topic3_spectral.analysis import PARAMS  # noqa: E402
from src.topic3_spectral.estimators import centered_eigs, clauset_mle, rank_slope  # noqa: E402

SHAPES = {
    "subject_57x384": (57, 384, 20), "subject_57x768": (57, 768, 20), "subject_57x1536": (57, 1536, 20),
    "subject_25x288": (25, 288, 20), "subject_25x768": (25, 768, 20),
    "token_cat_L0_71680x384": (71680, 384, 3), "token_cat_L1_8960x768": (8960, 768, 3),
    "token_cat_L2L3_1120x1536": (1120, 1536, 4),
}
VARIANT_SHAPE = {"L0": "token_cat_L0_71680x384", "L1": "token_cat_L1_8960x768",
                 "L2": "token_cat_L2L3_1120x1536", "LN0L2": "token_cat_L2L3_1120x1536",
                 "L3": "token_cat_L2L3_1120x1536"}


def main():
    t0 = time.time()
    rng = np.random.default_rng(PARAMS["seed"] + 7)
    tol = PARAMS["alpha_bias_tol"]
    out = {"label": "SYNTHETIC calibration (no real data)", "tol": tol, "shapes": {}}
    for name, (n, d, reps) in SHAPES.items():
        r = min(n - 1, d)
        rec = {"n": n, "D": d, "reps": reps, "by_a": {}}
        ok = {"rank_slope": True, "clauset": True}
        for a in PARAMS["alpha_test_rank_exponents"]:
            lam = np.arange(1, d + 1, dtype=np.float64) ** (-a)
            pop_rs = rank_slope(lam[:r])
            pop_cl = clauset_mle(lam[:r])["alpha"]
            rs, cl = [], []
            for _ in range(reps):
                X = rng.standard_normal((n, d)) * np.sqrt(lam)
                ev = centered_eigs(X)
                rs.append(rank_slope(ev))
                cl.append(clauset_mle(ev)["alpha"])
                del X
            b_rs = float(np.mean(rs) - pop_rs)
            b_cl = float(np.mean(cl) - pop_cl)
            rec["by_a"][str(a)] = {"pop_rank_slope": pop_rs, "mean_rank_slope": float(np.mean(rs)), "bias_rank_slope": b_rs,
                                   "pop_clauset": pop_cl, "mean_clauset": float(np.mean(cl)), "bias_clauset": b_cl}
            ok["rank_slope"] &= abs(b_rs) <= tol
            ok["clauset"] &= abs(b_cl) <= tol
        rec["estimable_rank_slope"] = bool(ok["rank_slope"])
        rec["estimable_clauset"] = bool(ok["clauset"])
        rec["estimable_both"] = bool(ok["rank_slope"] and ok["clauset"])
        out["shapes"][name] = rec
        print(name, rec["estimable_rank_slope"], rec["estimable_clauset"], round(time.time() - t0, 1), flush=True)
    out["token_variant_alpha_reportable"] = {
        v: {"rank_slope": out["shapes"][s]["estimable_rank_slope"], "clauset": out["shapes"][s]["estimable_clauset"]}
        for v, s in VARIANT_SHAPE.items()}
    out["runtime_s"] = round(time.time() - t0, 1)
    path = os.path.join(ROOT, "results", "topic3", "2026-10-31", "alpha_calibration_synthetic.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out["token_variant_alpha_reportable"]), path)


if __name__ == "__main__":
    main()
