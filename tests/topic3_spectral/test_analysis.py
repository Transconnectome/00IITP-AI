"""Frozen-card analysis functions on synthetic inputs with planted effects and nulls."""
import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT  # noqa: F401
from src.topic3_spectral import analysis
from src.topic3_spectral.analysis import paired_log_contrast, replication_verdict, token_level_checkpoint

FAST = dict(analysis.PARAMS, iid_reps=30, colperm_reps=30, subsample_S=60, signflip_B=999, bootstrap_B=999)


def _mats(rng, a_l2=0.6, a_l3=1.6):
    def m(n, d, a):
        return rng.standard_normal((n, d)) * np.arange(1, d + 1, dtype=float) ** (-a / 2) + 5.0
    return {"L0": m(57, 96, 1.5), "L1": m(57, 128, 1.5), "L2": m(57, 192, a_l2), "L3": m(57, 192, a_l3),
            "BrainLM": m(57, 128, 1.4), "BrainJEPA": m(57, 128, 0.7), "NeuroSTORM": m(25, 64, 0.7)}


def test_subject_level_detects_planted_l2_gt_l3_and_cross_model_order():
    rng = np.random.default_rng(0)
    ns = sorted(rng.choice(57, 25, replace=False).tolist())
    out = analysis.subject_level(_mats(rng), ns, FAST)
    assert out["D1"]["L2_gt_L3_cov_robust"] is True
    assert out["A2_matched25"]["NeuroSTORM"]["n"] == 25 and out["A2_matched25"]["L2"]["n"] == 25
    assert out["D3"]["ordering_reproduces_cov"] is True
    # independent heterogeneous-variance columns: no structure beyond independent columns
    assert out["E1_full"]["L2"]["D2_structure_beyond_independent_columns"] is False


def test_d2_flags_cross_column_dependence():
    rng = np.random.default_rng(9)
    X = rng.standard_normal((57, 3)) @ rng.standard_normal((3, 192)) + 0.3 * rng.standard_normal((57, 192))
    d = analysis.describe_matrix(X, 1, dict(FAST, colperm_reps=200))
    assert d["D2_structure_beyond_independent_columns"] is True
    assert d["pr_cov"] < d["colperm_null_q025"]


def test_subject_level_null_does_not_claim_l2_gt_l3():
    rng = np.random.default_rng(1)
    ns = sorted(rng.choice(57, 25, replace=False).tolist())
    out = analysis.subject_level(_mats(rng, a_l2=1.0, a_l3=1.0), ns, FAST)
    r = out["A1_swift_pairs"]["L2_minus_L3"]["cov"]
    assert r["lo"] <= 0 <= r["hi"]


def _arrs(rng, n, effect):
    base = {}
    for v in ("L0", "L1", "L2", "LN0L2", "L3"):
        for k in ("cat_covpr", "cat_corrpr"):
            base["%s__%s" % (k, v)] = np.exp(rng.normal(2.5, 0.2, n))
        for k in ("sub_covpr", "sub_corrpr", "frame_covpr", "frame_corrpr"):
            base["%s__%s" % (k, v)] = np.exp(rng.normal(2.0, 0.2, (n, 7)))
        base["cat_corr_dropped__" + v] = np.zeros(n, dtype=int)
        base["cat_cov_eigs__" + v] = np.sort(rng.random((n, 30)), axis=1)[:, ::-1]
    base["cat_corrpr__L3"] = base["cat_corrpr__LN0L2"] * np.exp(rng.normal(effect, 0.2, n))
    base["cat_covpr__L3"] = base["cat_covpr__L2"] * np.exp(rng.normal(effect, 0.2, n))
    return base


def test_token_contrast_and_replication_rule():
    rng = np.random.default_rng(2)
    per = {c: token_level_checkpoint(_arrs(rng, 57, -0.5), 5, FAST) for c in ("primary", "z1", "z2", "z3")}
    v = replication_verdict(per, "primary", FAST)
    assert v["H1a_blocks_LN_matched_corr"]["verdict"] == "holds"
    assert v["H1a_blocks_LN_matched_corr"]["direction"] == "L3 lower"
    per_null = {c: token_level_checkpoint(_arrs(rng, 57, 0.0), 6, FAST) for c in ("primary", "z1", "z2", "z3")}
    vn = replication_verdict(per_null, "primary", FAST)
    assert vn["H1a_blocks_LN_matched_corr"]["verdict"] != "holds"
    mixed = {"primary": per["primary"], "z1": per["z1"], "z2": per_null["z2"], "z3": per_null["z3"]}
    assert replication_verdict(mixed, "primary", FAST)["H1a_blocks_LN_matched_corr"]["verdict"] == "not replicated"


def test_paired_log_contrast_is_log_ratio():
    a = np.array([2.0, 4.0, 8.0])
    r = paired_log_contrast(a, a / 2, 0, FAST)
    assert r["mean_log_ratio"] == pytest.approx(np.log(2))
    assert r["ratio_geomean"] == pytest.approx(2.0)
