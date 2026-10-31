"""Frozen-card analysis logic for Topic 3 (2026-10-31). Pure functions on arrays; the scripts in
scripts/topic3_*.py only do I/O. Parameters live in PARAMS and are copied verbatim into the card.
"""
import math

import numpy as np

from .estimators import clauset_mle, jackknife_pr, pr_corr, pr_cov, rank_slope
from .resampling import (column_permutation_null, holm, iid_reference, paired_subsample_delta,
                         sign_flip_test, subject_bootstrap_ci, subsample_indices, subsample_mean)

PARAMS = {
    "seed": 20261031,
    "var_floor_frac": 1e-3,
    "ln_eps": 1e-5,
    "iid_reps": 1000,
    "colperm_reps": 1000,
    "subsample_m_57": 28,
    "subsample_m_25": 12,
    "subsample_S": 2000,
    "signflip_B": 9999,
    "bootstrap_B": 9999,
    "alpha_bias_tol": 0.15,
    "alpha_test_rank_exponents": [0.5, 1.0, 2.0],
    "holm_alpha": 0.05,
    "replication_min_zoo_agree": 2,
    "token_subsample_per_frame": 160,
}

SWIFT_PAIRS = (("L2", "L3"), ("L2", "L1"), ("L1", "L0"))
CROSS_MODEL_PAIRS = (("BrainJEPA", "BrainLM"), ("NeuroSTORM", "BrainLM"))


def describe_matrix(X, seed, params=PARAMS):
    """Subject-level description of one pooled matrix (E1)."""
    n, d = X.shape
    pc = pr_cov(X)
    pk = pr_corr(X, params["var_floor_frac"])
    _, se, bc = jackknife_pr(X, pr_cov)
    iid = iid_reference(n, d, params["iid_reps"], seed)
    null = column_permutation_null(X, params["colperm_reps"], seed + 1)
    p_low = float((1 + np.sum(null <= pc)) / (1 + null.size))
    return {
        "n": int(n), "D": int(d), "pr_cov": pc, "pr_corr": pk, "pr_cov_over_nminus1": pc / (n - 1),
        "jackknife_se_pr_cov": se, "jackknife_bias_corrected_pr_cov": bc,
        "iid_ref_mean": float(iid.mean()), "iid_ref_q025": float(np.quantile(iid, 0.025)),
        "iid_ref_q975": float(np.quantile(iid, 0.975)), "pr_cov_over_iid_mean": pc / float(iid.mean()),
        "colperm_null_mean": float(null.mean()), "colperm_null_q025": float(np.quantile(null, 0.025)),
        "colperm_p_low": p_low,
        "D2_structure_beyond_independent_columns": bool(p_low < 0.025),
    }


def subject_level(mats, ns_positions, params=PARAMS, ln_matched=None):
    """Family A. mats: dict name -> X (57-row SwiFT L0-L3, BrainLM, BrainJEPA; NeuroSTORM 25-row).
    ns_positions: positions of the NeuroSTORM rows inside the 57-row order.
    ln_matched: optional dict {'LN0L2': X57, 'L3': X57} re-pooled on connectome (A1b)."""
    seed = params["seed"]
    out = {"E1_full": {}, "A1_swift_pairs": {}, "A2_matched25": {}, "A2_pairs": {}, "A1b_ln_matched": None}
    for i, (name, X) in enumerate(mats.items()):
        out["E1_full"][name] = describe_matrix(X, seed + 10 * i, params)
    n57 = mats["L2"].shape[0]
    idx57 = subsample_indices(n57, params["subsample_m_57"], params["subsample_S"], seed + 100)
    for a, b in SWIFT_PAIRS:
        out["A1_swift_pairs"]["%s_minus_%s" % (a, b)] = {
            "cov": paired_subsample_delta(mats[a], mats[b], params["subsample_m_57"], 0, 0,
                                          pr_cov, index_sets=idx57),
            "corr": paired_subsample_delta(mats[a], mats[b], params["subsample_m_57"], 0, 0,
                                           lambda Z: pr_corr(Z, params["var_floor_frac"]), index_sets=idx57),
        }
    r = out["A1_swift_pairs"]["L2_minus_L3"]
    out["D1"] = {"L2_gt_L3_cov_robust": bool(r["cov"]["lo"] > 0),
                 "L2_gt_L3_corr_robust": bool(r["corr"]["lo"] > 0)}
    out["D1"]["verdict"] = ("drop robust and not a per-channel-scale effect" if out["D1"]["L2_gt_L3_cov_robust"]
                            and out["D1"]["L2_gt_L3_corr_robust"] else
                            "drop robust in cov only: attributable to per-channel gain (final LN)"
                            if out["D1"]["L2_gt_L3_cov_robust"] else "drop not robust")
    if ln_matched is not None:
        out["A1b_ln_matched"] = ln_matched_subject_level(ln_matched["L3"], ln_matched["LN0L2"], params)
    pos = np.asarray(ns_positions, dtype=int)
    m25 = {}
    for name, X in mats.items():
        m25[name] = X if X.shape[0] == pos.size else X[pos]
    n25 = pos.size
    idx25 = subsample_indices(n25, params["subsample_m_25"], params["subsample_S"], seed + 200)
    for i, (name, X) in enumerate(m25.items()):
        d = describe_matrix(X, seed + 1000 + 10 * i, params)
        iid_m = iid_reference(params["subsample_m_25"], X.shape[1], params["iid_reps"], seed + 2000 + i)
        sm = subsample_mean(X, params["subsample_m_25"], 0, 0, pr_cov, index_sets=idx25)
        d["subsample_m12_mean_pr_cov"] = sm["mean"]
        d["subsample_m12_over_iid"] = sm["mean"] / float(iid_m.mean())
        out["A2_matched25"][name] = d
    for a, b in CROSS_MODEL_PAIRS:
        out["A2_pairs"]["%s_minus_%s" % (a, b)] = {
            "cov": paired_subsample_delta(m25[a], m25[b], params["subsample_m_25"], 0, 0, pr_cov, index_sets=idx25),
            "corr": paired_subsample_delta(m25[a], m25[b], params["subsample_m_25"], 0, 0,
                                           lambda Z: pr_corr(Z, params["var_floor_frac"]), index_sets=idx25),
        }
    out["D3"] = {"ordering_reproduces_cov": bool(all(v["cov"]["lo"] > 0 for v in out["A2_pairs"].values())),
                 "attribution": "untestable: models differ in pooling (CLS / token mean / GAP), D and training data"}
    return out


def ln_matched_subject_level(L3, LN0L2, params=PARAMS):
    """A1b: pooled L3 (= g * mean LN0(h) + b) vs pooled per-token-LN0(L2), on the same 57 rows.
    corrPR removes the final-LN gain/bias exactly, so the corr contrast isolates stage-3 blocks."""
    n = L3.shape[0]
    idx = subsample_indices(n, params["subsample_m_57"], params["subsample_S"], params["seed"] + 100)
    corr = lambda Z: pr_corr(Z, params["var_floor_frac"])  # noqa: E731
    return {
        "pr_corr_L3": corr(L3), "pr_corr_LN0L2": corr(LN0L2), "pr_cov_L3": pr_cov(L3), "pr_cov_LN0L2": pr_cov(LN0L2),
        "L3_minus_LN0L2_corr": paired_subsample_delta(L3, LN0L2, params["subsample_m_57"], 0, 0, corr, index_sets=idx),
        "L3_minus_LN0L2_cov": paired_subsample_delta(L3, LN0L2, params["subsample_m_57"], 0, 0, pr_cov, index_sets=idx),
    }


def alpha_estimates(ev):
    """Descriptive decay exponents of one spectrum."""
    out = {"rank_slope": float("nan"), "clauset_alpha": float("nan"), "clauset_n_tail": 0}
    try:
        out["rank_slope"] = rank_slope(ev)
    except ValueError:
        pass
    try:
        c = clauset_mle(ev)
        out["clauset_alpha"] = c["alpha"]
        out["clauset_n_tail"] = c["n_tail"]
    except ValueError:
        pass
    return out


def paired_log_contrast(a, b, seed, params=PARAMS):
    """Per-subject d_i = log a_i - log b_i; sign-flip p (two-sided), subject bootstrap CI."""
    d = np.log(np.asarray(a, dtype=np.float64)) - np.log(np.asarray(b, dtype=np.float64))
    p = sign_flip_test(d, params["signflip_B"], seed)
    lo, hi = subject_bootstrap_ci(d, params["bootstrap_B"], seed + 1)
    return {"n": int(d.size), "mean_log_ratio": float(d.mean()), "ratio_geomean": float(math.exp(d.mean())),
            "ci95": [lo, hi], "p_signflip": p, "frac_negative": float(np.mean(d < 0))}


TOKEN_PRIMARY = {"H1a_blocks_LN_matched_corr": ("cat_corrpr__L3", "cat_corrpr__LN0L2"),
                 "H1b_total_stage3_raw_cov": ("cat_covpr__L3", "cat_covpr__L2")}
TOKEN_SECONDARY = {"H1c_per_token_norm_corr": ("cat_corrpr__LN0L2", "cat_corrpr__L2"),
                   "H1d_total_stage3_corr": ("cat_corrpr__L3", "cat_corrpr__L2"),
                   "H1e_blocks_LN_matched_cov": ("cat_covpr__L3", "cat_covpr__LN0L2")}


def token_level_checkpoint(arrs, seed, params=PARAMS, alpha_ok=None):
    """Family B for one checkpoint. arrs: packed arrays from token_job.pack_summaries."""
    res = {"primary": {}, "secondary": {}, "profile": {}, "alpha": {}}
    for i, (k, (a, b)) in enumerate(TOKEN_PRIMARY.items()):
        res["primary"][k] = paired_log_contrast(arrs[a], arrs[b], seed + 10 * i, params)
    adj = holm([res["primary"][k]["p_signflip"] for k in TOKEN_PRIMARY])
    for k, pa in zip(TOKEN_PRIMARY, adj):
        res["primary"][k]["p_holm"] = float(pa)
    for i, (k, (a, b)) in enumerate(TOKEN_SECONDARY.items()):
        res["secondary"][k] = paired_log_contrast(arrs[a], arrs[b], seed + 100 + 10 * i, params)
    for v in ("L0", "L1", "L2", "LN0L2", "L3"):
        res["profile"][v] = {
            "cat_covpr_median": float(np.median(arrs["cat_covpr__" + v])),
            "cat_corrpr_median": float(np.median(arrs["cat_corrpr__" + v])),
            "sub160_covpr_mean": float(np.mean(arrs["sub_covpr__" + v])),
            "sub160_corrpr_mean": float(np.mean(arrs["sub_corrpr__" + v])),
            "frame_covpr_mean": float(np.mean(arrs["frame_covpr__" + v])),
            "frame_corrpr_mean": float(np.mean(arrs["frame_corrpr__" + v])),
            "cat_corr_dropped_max": int(np.max(arrs["cat_corr_dropped__" + v])),
        }
        ok = (alpha_ok or {}).get(v, {})
        rec = {}
        if ok.get("rank_slope") or ok.get("clauset"):
            ests = [alpha_estimates(ev) for ev in np.asarray(arrs["cat_cov_eigs__" + v], dtype=np.float64)]
        for est, key in (("rank_slope", "rank_slope"), ("clauset", "clauset_alpha")):
            if ok.get(est):
                vals = np.array([e[key] for e in ests])
                rec[est] = {"median": float(np.nanmedian(vals)), "q25": float(np.nanquantile(vals, 0.25)),
                            "q75": float(np.nanquantile(vals, 0.75))}
            else:
                rec[est] = "not estimable at this shape (synthetic calibration failed)"
        res["alpha"][v] = rec
    return res


def replication_verdict(per_ckpt, primary_label, params=PARAMS):
    """Card rule: an H1 effect HOLDS iff the primary checkpoint has Holm p < alpha with CI excluding 0,
    and >= replication_min_zoo_agree of the other checkpoints have the same sign with Holm p < alpha."""
    verdicts = {}
    for k in TOKEN_PRIMARY:
        prim = per_ckpt[primary_label]["primary"][k]
        sign = np.sign(prim["mean_log_ratio"])
        prim_ok = prim["p_holm"] < params["holm_alpha"] and (prim["ci95"][0] > 0 or prim["ci95"][1] < 0)
        agree = [c for c, r in per_ckpt.items() if c != primary_label
                 and np.sign(r["primary"][k]["mean_log_ratio"]) == sign
                 and r["primary"][k]["p_holm"] < params["holm_alpha"]]
        holds = bool(prim_ok and len(agree) >= params["replication_min_zoo_agree"])
        verdicts[k] = {"primary_significant": bool(prim_ok), "direction": "L3 lower" if sign < 0 else "L3 higher",
                       "n_other_checkpoints_agreeing": len(agree), "n_other_checkpoints": len(per_ckpt) - 1,
                       "verdict": "holds" if holds else ("not replicated" if prim_ok else "killed (primary CI includes 0)")}
    return verdicts
