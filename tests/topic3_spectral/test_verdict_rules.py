"""Post-results guard tests for the frozen Topic 3 decision logic (added 2026-10-31 by worker_M2_r2,
iteration 2 of M2). These tests were written AFTER the real-data results existed; they are guards
against regressions in the shipped code, not a pre-registration. No file in src/topic3_spectral was
changed; analysis.py is byte-identical to the frozen code (results/topic3/2026-10-31/code_sha256_at_freeze.txt).

Base: verification/explorer_M2_r2_3/proposed_test_verdict_rules.py
(sha256 69fbd923e5b33c6393f15fcc02a26dc0126a444fd4508948c27c7892be95cad6), extended by worker_M2_r2 with
(i) an explicit H1a/H1b orientation-and-wiring case with L2 shifted away from LN0L2 in both families,
(ii) the effective-ceiling fixture for the token matrices (8 near-static spatial-cell vectors), and
(iii) the H1b sign-check consequence on the pinned real-data summary.

Pins the frozen-card decision logic (card section 4 D1/D3, section 5 replication rule and H1 pair wiring)
and the descriptive uncertainty formulas (card section 3) that the 2026-10-31 verifier mutants showed were
unguarded. Rule tests use hand-built inputs so the expected verdict is known exactly; D1/D3 use a stub for
paired_subsample_delta keyed by matrix width, so the rule is tested independently of sampling noise.
"""
import json
import math
import os

import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT
from src.topic3_spectral import analysis, estimators, resampling
from src.topic3_spectral.analysis import replication_verdict

H1A, H1B = "H1a_blocks_LN_matched_corr", "H1b_total_stage3_raw_cov"
FAST = dict(analysis.PARAMS, iid_reps=20, colperm_reps=20, subsample_S=40, signflip_B=499, bootstrap_B=499)


# ---------------------------------------------------------------- replication rule (card §5)
def _rec(m, p_holm, ci, p_raw=None):
    return {"mean_log_ratio": m, "p_holm": p_holm, "p_signflip": p_holm if p_raw is None else p_raw,
            "ci95": list(ci)}


def _ck(h1a, h1b=None):
    return {"primary": {H1A: h1a, H1B: h1b if h1b is not None else h1a}}


SIG_POS = _rec(+0.03, 0.0002, (0.02, 0.04))
SIG_NEG = _rec(-0.10, 0.0002, (-0.12, -0.08))


def test_primary_pair_wiring_is_the_card_pairs():
    assert analysis.TOKEN_PRIMARY == {H1A: ("cat_corrpr__L3", "cat_corrpr__LN0L2"),
                                      H1B: ("cat_covpr__L3", "cat_covpr__L2")}
    assert analysis.TOKEN_SECONDARY == {"H1c_per_token_norm_corr": ("cat_corrpr__LN0L2", "cat_corrpr__L2"),
                                        "H1d_total_stage3_corr": ("cat_corrpr__L3", "cat_corrpr__L2"),
                                        "H1e_blocks_LN_matched_cov": ("cat_covpr__L3", "cat_covpr__LN0L2")}
    assert analysis.PARAMS["holm_alpha"] == 0.05 and analysis.PARAMS["replication_min_zoo_agree"] == 2


def test_significant_opposite_sign_zoo_does_not_count_as_agreement():
    # the real-data configuration: one agreeing zoo checkpoint, two significant in the OTHER direction
    per = {"primary": _ck(SIG_POS), "z1": _ck(SIG_NEG), "z2": _ck(SIG_POS), "z3": _ck(SIG_NEG)}
    v = replication_verdict(per, "primary")[H1A]
    assert v["n_other_checkpoints_agreeing"] == 1
    assert v["verdict"] == "not replicated"
    assert v["direction"] == "L3 higher"


def test_two_of_three_same_sign_significant_holds_one_does_not():
    assert replication_verdict({"primary": _ck(SIG_NEG), "z1": _ck(SIG_NEG), "z2": _ck(SIG_NEG),
                                "z3": _ck(SIG_POS)}, "primary")[H1A]["verdict"] == "holds"
    assert replication_verdict({"primary": _ck(SIG_NEG), "z1": _ck(SIG_NEG), "z2": _ck(SIG_POS),
                                "z3": _ck(SIG_POS)}, "primary")[H1A]["verdict"] == "not replicated"


def test_primary_is_not_counted_as_its_own_replicate():
    v = replication_verdict({"primary": _ck(SIG_POS), "z1": _ck(SIG_POS), "z2": _ck(SIG_NEG),
                             "z3": _ck(SIG_NEG)}, "primary")[H1A]
    assert v["n_other_checkpoints_agreeing"] == 1 and v["n_other_checkpoints"] == 3


def test_primary_ci_covering_zero_kills_even_when_p_is_small():
    prim = _rec(+0.03, 0.001, (-0.001, 0.06))
    v = replication_verdict({"primary": _ck(prim), "z1": _ck(SIG_POS), "z2": _ck(SIG_POS),
                             "z3": _ck(SIG_POS)}, "primary")[H1A]
    assert v["primary_significant"] is False
    assert v["verdict"] == "killed (primary CI includes 0)"


def test_primary_ci_excluding_zero_on_either_side_counts():
    for prim in (SIG_POS, SIG_NEG):
        z = SIG_POS if prim is SIG_POS else SIG_NEG
        v = replication_verdict({"primary": _ck(prim), "z1": _ck(z), "z2": _ck(z), "z3": _ck(z)}, "primary")[H1A]
        assert v["primary_significant"] is True and v["verdict"] == "holds"


@pytest.mark.parametrize("p_holm", [0.05, 0.06, 0.2, 0.49])
def test_primary_holm_p_at_or_above_alpha_is_not_significant(p_holm):
    prim = _rec(+0.03, p_holm, (0.02, 0.04))
    v = replication_verdict({"primary": _ck(prim), "z1": _ck(SIG_POS), "z2": _ck(SIG_POS),
                             "z3": _ck(SIG_POS)}, "primary")[H1A]
    assert v["primary_significant"] is False and v["verdict"] != "holds"


def test_zoo_agreement_uses_holm_not_raw_p():
    # raw sign-flip p < 0.05 but Holm-adjusted p >= 0.05: must NOT count as agreement
    z_raw_only = _rec(+0.03, 0.06, (0.01, 0.05), p_raw=0.03)
    v = replication_verdict({"primary": _ck(SIG_POS), "z1": _ck(z_raw_only), "z2": _ck(z_raw_only),
                             "z3": _ck(SIG_POS)}, "primary")[H1A]
    assert v["n_other_checkpoints_agreeing"] == 1 and v["verdict"] == "not replicated"


@pytest.mark.parametrize("p_holm", [0.06, 0.3])
def test_nonsignificant_same_sign_zoo_does_not_count(p_holm):
    z = _rec(+0.03, p_holm, (-0.01, 0.07))
    v = replication_verdict({"primary": _ck(SIG_POS), "z1": _ck(z), "z2": _ck(z), "z3": _ck(SIG_POS)},
                            "primary")[H1A]
    assert v["n_other_checkpoints_agreeing"] == 1


def test_holm_is_applied_to_the_two_primary_contrasts_within_a_checkpoint():
    rng = np.random.default_rng(3)
    n = 57
    arrs = {}
    for v in ("L0", "L1", "L2", "LN0L2", "L3"):
        for k in ("cat_covpr", "cat_corrpr"):
            arrs["%s__%s" % (k, v)] = np.exp(rng.normal(2.5, 0.2, n))
        for k in ("sub_covpr", "sub_corrpr", "frame_covpr", "frame_corrpr"):
            arrs["%s__%s" % (k, v)] = np.exp(rng.normal(2.0, 0.2, (n, 7)))
        arrs["cat_corr_dropped__" + v] = np.zeros(n, dtype=int)
        arrs["cat_cov_eigs__" + v] = np.sort(rng.random((n, 30)), axis=1)[:, ::-1]
    # H1a pair (L3 vs LN0L2) carries an effect; L3 vs L2 (the wrong pair) carries none
    arrs["cat_corrpr__LN0L2"] = arrs["cat_corrpr__L2"] * np.exp(rng.normal(0.5, 0.05, n))
    arrs["cat_corrpr__L3"] = arrs["cat_corrpr__LN0L2"] * np.exp(rng.normal(-0.5, 0.05, n))
    res = analysis.token_level_checkpoint(arrs, 11, FAST)
    p = [res["primary"][k]["p_signflip"] for k in (H1A, H1B)]
    assert [res["primary"][k]["p_holm"] for k in (H1A, H1B)] == pytest.approx(list(resampling.holm(p)))
    assert res["primary"][H1A]["mean_log_ratio"] == pytest.approx(
        float(np.mean(np.log(arrs["cat_corrpr__L3"]) - np.log(arrs["cat_corrpr__LN0L2"]))))
    assert res["primary"][H1A]["mean_log_ratio"] < -0.4


def test_frozen_family_b_verdicts_recomputed_from_saved_per_checkpoint_results():
    """Regression on the pinned real-data summary (no IDs): the shipped rule must reproduce the
    recorded verdicts. Under 'ignore sign' H1b would flip to 'holds'."""
    p = os.path.join(ROOT, "results", "topic3", "2026-10-31", "family_B_token_level.json")
    d = json.load(open(p))
    v = replication_verdict(d["per_checkpoint"], "E192_primary")
    assert v[H1A]["verdict"] == "holds" and v[H1A]["n_other_checkpoints_agreeing"] == 2
    assert v[H1B]["verdict"] == "not replicated" and v[H1B]["n_other_checkpoints_agreeing"] == 1
    for k in (H1A, H1B):
        assert v[k]["verdict"] == d["H1_replication_verdicts"][k]["verdict"]


# ---------------------------------------------------------------- D1 / D3 (card §4)
WIDTH = {"L0": 96, "L1": 128, "L2": 192, "L3": 160, "BrainLM": 112, "BrainJEPA": 144, "NeuroSTORM": 80}


def _mats():
    rng = np.random.default_rng(5)
    return {k: rng.standard_normal((25 if k == "NeuroSTORM" else 57, w)) for k, w in WIDTH.items()}


def _run_with_intervals(monkeypatch, table):
    """table[(width_a, width_b, kind)] = (lo, point, hi); missing pairs get a null interval."""
    def stub(XA, XB, m, S, seed, estimator=None, index_sets=None):
        kind = "cov" if estimator is analysis.pr_cov else "corr"
        lo, pt, hi = table.get((XA.shape[1], XB.shape[1], kind), (-1.0, 0.1, 1.2))
        return {"point": pt, "se": (hi - lo) / 3.92, "lo": lo, "hi": hi, "frac_positive": 0.5, "m": m, "S": 1}
    monkeypatch.setattr(analysis, "paired_subsample_delta", stub)
    rng = np.random.default_rng(6)
    ns = sorted(rng.choice(57, 25, replace=False).tolist())
    return analysis.subject_level(_mats(), ns, FAST)


L23, JL, NL = (192, 160), (144, 112), (80, 112)


def test_d1_both_lower_bounds_positive(monkeypatch):
    out = _run_with_intervals(monkeypatch, {L23 + ("cov",): (0.5, 2.0, 3.5), L23 + ("corr",): (0.4, 2.0, 3.6)})
    assert out["D1"]["L2_gt_L3_cov_robust"] is True and out["D1"]["L2_gt_L3_corr_robust"] is True
    assert out["D1"]["verdict"] == "drop robust and not a per-channel-scale effect"


def test_d1_uses_lower_bound_not_point_or_upper(monkeypatch):
    # point > 0 and hi > 0, but lo < 0: NOT robust
    out = _run_with_intervals(monkeypatch, {L23 + ("cov",): (-0.2, 1.5, 3.2), L23 + ("corr",): (-0.1, 1.5, 3.1)})
    assert out["D1"]["L2_gt_L3_cov_robust"] is False and out["D1"]["L2_gt_L3_corr_robust"] is False
    assert out["D1"]["verdict"] == "drop not robust"


def test_d1_cov_only_is_attributed_to_gain(monkeypatch):
    out = _run_with_intervals(monkeypatch, {L23 + ("cov",): (0.5, 2.0, 3.5), L23 + ("corr",): (-0.1, 1.5, 3.1)})
    assert out["D1"]["L2_gt_L3_cov_robust"] is True and out["D1"]["L2_gt_L3_corr_robust"] is False
    assert out["D1"]["verdict"] == "drop robust in cov only: attributable to per-channel gain (final LN)"


def test_d3_requires_both_cross_model_pairs(monkeypatch):
    both = _run_with_intervals(monkeypatch, {JL + ("cov",): (0.3, 1.0, 1.7), NL + ("cov",): (0.2, 1.0, 1.8)})
    assert both["D3"]["ordering_reproduces_cov"] is True
    one = _run_with_intervals(monkeypatch, {JL + ("cov",): (0.3, 1.0, 1.7), NL + ("cov",): (-0.2, 1.0, 2.2)})
    assert one["D3"]["ordering_reproduces_cov"] is False
    corr_only = _run_with_intervals(monkeypatch, {JL + ("corr",): (0.3, 1.0, 1.7), NL + ("corr",): (0.2, 1.0, 1.8)})
    assert corr_only["D3"]["ordering_reproduces_cov"] is False


# ---------------------------------------------------------------- descriptive formulas (card §3)
def test_jackknife_se_matches_textbook_formula():
    rng = np.random.default_rng(7)
    X = rng.standard_normal((15, 30)) * np.arange(1, 31) ** -0.7
    full, se, bc = estimators.jackknife_pr(X)
    loo = np.array([estimators.pr_cov(np.delete(X, i, axis=0)) for i in range(15)])
    assert se == pytest.approx(math.sqrt(14 / 15 * float(np.sum((loo - loo.mean()) ** 2))), rel=1e-12)
    assert bc == pytest.approx(15 * full - 14 * loo.mean(), rel=1e-12)


@pytest.mark.parametrize("n,m", [(57, 12), (57, 28), (25, 12)])
def test_subsample_se_uses_finite_population_rate(n, m):
    rng = np.random.default_rng(8)
    A, B = rng.standard_normal((n, 40)), rng.standard_normal((n, 40)) * np.arange(1, 41) ** -0.5
    idx = resampling.subsample_indices(n, m, 30, 9)
    r = resampling.paired_subsample_delta(A, B, m, 0, 0, estimators.pr_cov, index_sets=idx)
    d = np.array([estimators.pr_cov(A[i]) - estimators.pr_cov(B[i]) for i in idx])
    assert r["se"] == pytest.approx(float(d.std() * math.sqrt(m / (n - m))), rel=1e-12)
    assert r["lo"] == pytest.approx(r["point"] - 1.96 * r["se"]) and r["hi"] == pytest.approx(r["point"] + 1.96 * r["se"])


def test_sign_flip_p_has_plus_one_floor():
    d = np.full(25, 1.0)  # every flip except all-plus gives a smaller |mean|; P(all-plus) = 2^-25
    assert resampling.sign_flip_test(d, 199, 0) == pytest.approx(1.0 / 200)


def test_layernorm0_eps_is_torch_default_and_used():
    assert estimators.LN_EPS == 1e-5
    X = np.array([[1.0, 1.0, 1.0, 1.0], [0.0, 1e-3, 0.0, 1e-3]])
    Y = estimators.layernorm0(X)
    assert np.all(np.isfinite(Y)) and np.allclose(Y[0], 0.0)
    expect = (X[1] - X[1].mean()) / math.sqrt(X[1].var() + 1e-5)
    assert np.allclose(Y[1], expect, rtol=1e-12, atol=0)


def test_rank_slope_default_window_is_half_the_nonzero_rank():
    k = np.arange(1, 41, dtype=float)
    ev = np.where(k <= 20, k ** -1.0, 20.0 ** -1.0 * (k / 20.0) ** -4.0)  # kink after r/2 = 20
    assert estimators.rank_slope(ev) == pytest.approx(1.0, abs=1e-9)


def test_iid_reference_is_gaussian_marchenko_pastur_draws():
    # card §3/§6: the iid reference is iid standard-normal at the real (n, D); pin the draw distribution
    vals = resampling.iid_reference(12, 30, 3, 123)
    rng = np.random.default_rng(123)
    expect = [estimators.pr_cov(rng.standard_normal((12, 30))) for _ in range(3)]
    assert list(vals) == pytest.approx(expect, rel=1e-12)


# ---------------------------------------------------------------- additions by worker_M2_r2
def _token_arrs_shifted(n=40, seed=21):
    """L2 sits systematically ABOVE LN0L2 (x e^{+0.5}) and L3 BELOW it (x e^{-0.5}), in both the corr and
    cov families, so every wrong wiring/orientation of H1a/H1b gives a different mean log ratio."""
    rng = np.random.default_rng(seed)
    arrs = {}
    for v in ("L0", "L1", "L2", "LN0L2", "L3"):
        for k in ("sub_covpr", "sub_corrpr", "frame_covpr", "frame_corrpr"):
            arrs["%s__%s" % (k, v)] = np.exp(rng.normal(2.0, 0.2, (n, 7)))
        arrs["cat_corr_dropped__" + v] = np.zeros(n, dtype=int)
        arrs["cat_cov_eigs__" + v] = np.sort(rng.random((n, 30)), axis=1)[:, ::-1]
    for fam in ("cat_corrpr", "cat_covpr"):
        base = np.exp(rng.normal(2.5, 0.2, n))
        arrs[fam + "__LN0L2"] = base
        arrs[fam + "__L2"] = base * np.exp(0.5 + rng.normal(0.0, 0.01, n))
        arrs[fam + "__L3"] = base * np.exp(-0.5 + rng.normal(0.0, 0.01, n))
        arrs[fam + "__L0"] = base * np.exp(rng.normal(0.0, 0.2, n))
        arrs[fam + "__L1"] = base * np.exp(rng.normal(0.0, 0.2, n))
    return arrs


def test_h1a_h1b_orientation_and_wiring_with_l2_shifted_from_ln0l2():
    arrs = _token_arrs_shifted()
    res = analysis.token_level_checkpoint(arrs, 31, FAST)
    # H1a = log corrPR(L3) - log corrPR(LN0L2) = -0.5 ; wired to L2 it would be -1.0, swapped +0.5
    assert res["primary"][H1A]["mean_log_ratio"] == pytest.approx(-0.5, abs=0.01)
    # H1b = log covPR(L3) - log covPR(L2) = -1.0 ; wired to LN0L2 it would be -0.5, swapped +1.0
    assert res["primary"][H1B]["mean_log_ratio"] == pytest.approx(-1.0, abs=0.01)
    # secondary contrasts keep their card orientation too
    assert res["secondary"]["H1c_per_token_norm_corr"]["mean_log_ratio"] == pytest.approx(-0.5, abs=0.01)
    assert res["secondary"]["H1d_total_stage3_corr"]["mean_log_ratio"] == pytest.approx(-1.0, abs=0.01)
    assert res["secondary"]["H1e_blocks_LN_matched_cov"]["mean_log_ratio"] == pytest.approx(-0.5, abs=0.01)
    per = {c: res for c in ("primary", "z1", "z2", "z3")}
    v = replication_verdict(per, "primary")
    assert v[H1A]["direction"] == "L3 lower" and v[H1A]["verdict"] == "holds"


def test_frozen_family_b_h1b_is_sign_limited_not_significance_limited():
    """On the pinned summary all three zoo checkpoints are Holm-significant for H1b; only the sign
    condition keeps H1b at 'not replicated' (a rule that ignored sign would report 'holds')."""
    p = os.path.join(ROOT, "results", "topic3", "2026-10-31", "family_B_token_level.json")
    per = json.load(open(p))["per_checkpoint"]
    zoo = [c for c in per if c != "E192_primary"]
    assert len(zoo) == 3
    assert all(per[c]["primary"][H1B]["p_holm"] < 0.05 for c in zoo)
    s0 = np.sign(per["E192_primary"]["primary"][H1B]["mean_log_ratio"])
    assert sum(np.sign(per[c]["primary"][H1B]["mean_log_ratio"]) == s0 for c in zoo) == 1
    v = replication_verdict(per, "E192_primary")
    assert v[H1B]["verdict"] == "not replicated" and v[H1B]["direction"] == "L3 higher"
    assert v[H1A]["direction"] == "L3 higher"


def test_effective_ceiling_of_near_static_spatial_cell_tokens_is_cells_minus_one():
    """Token matrix shape of L2/LN0L2/L3: 8 spatial cells x 20 time steps x 7 frames = 1120 rows. If the
    8 cell vectors barely change over time, the centered spectrum has <= 7 non-negligible eigenvalues,
    PR <= 7 (not 1119), and concatenating frames leaves PR equal to that of one static copy."""
    rng = np.random.default_rng(41)
    cells = rng.standard_normal((8, 1536)) * np.arange(1, 1537) ** -0.3
    one_copy = np.repeat(cells, 20, axis=0)                          # one frame: 160 tokens
    cat = np.tile(one_copy, (7, 1)) + 1e-6 * rng.standard_normal((1120, 1536))
    ev = estimators.centered_eigs(cat)
    assert float(ev[:7].sum() / ev.sum()) > 1 - 1e-9
    pr_cat, pr_one = estimators.pr_cov(cat), estimators.pr_cov(one_copy)
    assert pr_cat <= 7.0 + 1e-9
    assert pr_cat == pytest.approx(pr_one, rel=1e-6)
    assert estimators.pr_corr(cat) <= 7.0 + 1e-9
