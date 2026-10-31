"""T1.2 / T1.3 fixtures for the cohort scripts (run tw-20261031-four-topics, worker_M1_r1).

scripts/topic1_cohort_stats.py implements frozen card sections 3-7; scripts/topic1_run_cohort.py the manifest
and variant extraction.  Each test names the defect it catches.  Synthetic data only; no real-data read.
The scripts are loaded by file path relative to this repository checkout (ROOT/scripts).
"""
import importlib.util
import itertools
import math
import os

import numpy as np
import pandas as pd
import pytest

import tests.topic1_lagmotif.conftest_helpers as H


def _load(name):
    path = os.path.join(H.ROOT, "scripts", name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = _load("topic1_cohort_stats")
RC = _load("topic1_run_cohort")


def _design(seed=0):
    return S._synth_design(seed=seed)


# ---------------------------------------------------------------------------------- Freedman-Lane oracles
def test_permutations_stay_within_site_and_are_permutations():
    D = _design()
    sc = D["site"].values
    P = S.within_site_permutations(sc, 50, np.random.default_rng(0))
    assert P.shape == (50, len(D))
    for b in range(P.shape[0]):
        assert np.array_equal(np.sort(P[b]), np.arange(len(D)))      # a permutation
        assert np.array_equal(sc[P[b]], sc)                          # defect caught: permuting across sites
    assert not np.array_equal(P[0], np.arange(len(D)))


def test_vectorised_freedman_lane_equals_statsmodels_refit():
    import statsmodels.api as sm
    D = _design(1)
    rng = np.random.default_rng(3)
    y = 0.4 * D["dx"].values + rng.standard_normal(len(D)) + pd.Categorical(D["site"]).codes * 0.3
    Z = S.nuisance_matrix(D["age"], D["sex2"], D["logdur"], D["site"].values)
    fl = S.FreedmanLane(D["dx"].values, Z)
    P = S.within_site_permutations(D["site"].values, 15, np.random.default_rng(4))
    Xf = np.column_stack([D["dx"].values, Z])
    red = sm.OLS(y, Z).fit()                                          # reduced model: NO dx
    naive = [sm.OLS(red.fittedvalues + red.resid[P[b]], Xf).fit().tvalues[0] for b in range(15)]
    assert np.allclose(fl.t_perm(y, P), naive, atol=1e-9, rtol=0)
    assert fl.t_obs(y) == pytest.approx(sm.OLS(y, Xf).fit().tvalues[0], abs=1e-9)
    fe = S.fe_ols(y, D["dx"].values, Z)
    assert fe["t"] == pytest.approx(fl.t_obs(y), abs=1e-9)


def test_full_enumeration_matches_brute_force_on_tiny_design():
    """2 sites x 4 subjects: all 4!*4! = 576 within-site permutations; exact FL p equals brute force."""
    import statsmodels.api as sm
    site = np.array(["a"] * 4 + ["b"] * 4)
    dx = np.array([1, 1, 0, 0, 1, 0, 0, 0], float)
    age = np.array([20, 31, 44, 25, 38, 29, 50, 41], float)
    sex2 = np.array([0, 1, 0, 1, 1, 0, 1, 0], float)
    logdur = np.log(np.array([300, 300, 300, 300, 360, 360, 300, 360], float))
    y = np.array([1.2, 0.7, -0.3, 0.1, 0.9, -0.2, 0.4, -0.8])
    Z = S.nuisance_matrix(age, sex2, logdur, site)[:, [0, 1, 2]]   # site FE + age (keep df > 0)
    fl = S.FreedmanLane(dx, Z)
    perms = [np.array(pa + tuple(4 + i for i in pb))
             for pa in itertools.permutations(range(4)) for pb in itertools.permutations(range(4))]
    P = np.array(perms)
    tb = fl.t_perm(y, P)
    t0 = fl.t_obs(y)
    red = sm.OLS(y, Z).fit()
    Xf = np.column_stack([dx, Z])
    brute = np.array([sm.OLS(red.fittedvalues + red.resid[p], Xf).fit().tvalues[0] for p in perms])
    assert np.allclose(tb, brute, atol=1e-9)
    assert np.mean(np.abs(tb) >= abs(t0) - 1e-12) == pytest.approx(np.mean(np.abs(brute) >= abs(t0) - 1e-12))


def test_tested_regressor_in_nuisance_space_stops():
    """Defect caught: dx collinear with site (one site all OCD, the other all HC) -> no within-site contrast."""
    site = np.array(["a"] * 20 + ["b"] * 20)
    dx = np.array([1.0] * 20 + [0.0] * 20)
    rng = np.random.default_rng(0)
    Z = S.nuisance_matrix(rng.uniform(10, 60, 40), (rng.random(40) < 0.5).astype(float),
                          np.full(40, math.log(300.0)), site)
    with pytest.raises(S.StopForReview):
        S.FreedmanLane(dx, Z)


# ---------------------------------------------------------------------------------- effect size and Mundlak
def test_planted_effect_recovered_with_card_d_and_sign_is_ocd_minus_hc():
    rng = np.random.default_rng(11)
    D = pd.concat([S._synth_design(seed=s) for s in range(4)], ignore_index=True)
    D["site"] = [f"{s}_{i // 340}" for i, s in enumerate(D["site"])]   # 32 sites, n = 1360
    sc = pd.Categorical(D["site"]).codes
    u = math.sqrt(0.3 / 0.7) * rng.standard_normal(sc.max() + 1)[sc]
    y = 0.30 * D["dx"].values + u + rng.standard_normal(len(D))
    r = S.dx_effect(y, D, B=499)
    se_d = math.sqrt(1 / D["dx"].sum() + 1 / (1 - D["dx"]).sum())
    assert r["d"] > 0 and r["t_fe"] > 0                                    # sign OCD - HC
    assert abs(r["d"] - 0.30) < 4 * se_d
    assert r["mundlak_equality_ratio"] < 0.01                              # card stop rule satisfied
    assert r["d"] == pytest.approx(r["beta_lmm"] / r["sigma_eps_lmm"])
    r2 = S.dx_effect(-y, D, B=499)
    assert r2["d"] == pytest.approx(-r["d"], rel=1e-6)
    assert r["p_fl"] == r2["p_fl"] == pytest.approx(1 / 500)     # two-sided: a negative effect is as significant


def test_mundlak_lmm_beta_equals_site_fe_beta():
    D = _design(5)
    rng = np.random.default_rng(5)
    ocdfrac = D.groupby("site")["dx"].transform("mean").values
    y = 2.0 * ocdfrac + 0.2 * D["dx"].values + rng.standard_normal(len(D))   # site effect aligned with dx
    lm = S.mixedlm_mundlak(y, D["dx"], D["age"], D["sex2"], D["logdur"], D["site"])
    fe = S.fe_ols(y, D["dx"].values, S.nuisance_matrix(D["age"], D["sex2"], D["logdur"], D["site"].values))
    assert abs(lm["beta"] - fe["beta"]) / fe["se"] < 1e-6
    lm0 = S.mixedlm_mundlak(y, D["dx"], D["age"], D["sex2"], D["logdur"], D["site"], mundlak=False)
    assert abs(lm0["beta"] - fe["beta"]) / fe["se"] > 1e-3     # without Mundlak terms the equality is not exact


def test_truncation_row_drops_log_duration_constant_within_site():
    """Defect caught: adjusting the common-200 s row for the full-series duration.  After truncation the analysed
    duration is constant within site, so keeping log duration makes the design rank-deficient (stop), and the
    row must be fitted without it (Mundlak equality still holds)."""
    D = _design(7).copy()
    D["logdur"] = D["site"].map({s: math.log(200.0 + i) for i, s in enumerate(sorted(D["site"].unique()))})
    rng = np.random.default_rng(7)
    y = 0.3 * D["dx"].values + rng.standard_normal(len(D))
    with pytest.raises(S.StopForReview):
        S.dx_effect(y, D, B=99)
    r = S.dx_effect(y, D, B=99, include_logdur=False)
    assert r["include_logdur"] is False and r["mundlak_equality_ratio"] < 0.01


def test_gradient_share_row_fits_the_card_lmm_with_its_mundlak_mean():
    """Defect caught: the covariate-adjusted sensitivity row silently falling back to an FE-sigma d."""
    D = _design(8)
    rng = np.random.default_rng(8)
    g = rng.uniform(0.1, 0.9, len(D)) + 0.3 * D["dx"].values
    y = 0.3 * D["dx"].values + 1.5 * g + rng.standard_normal(len(D))
    r = S.dx_effect(y, D, B=99, extra=g)
    assert "d_source" not in r and r["mundlak_equality_ratio"] < 0.01
    assert r["d"] == pytest.approx(r["beta_lmm"] / r["sigma_eps_lmm"])
    Z = S.nuisance_matrix(D["age"], D["sex2"], D["logdur"], D["site"].values, extra=g)
    assert r["beta_fe"] == pytest.approx(S.fe_ols(y, D["dx"].values, Z)["beta"])


def test_nan_endpoint_must_coincide_with_degeneracy_flag():
    U = pd.DataFrame({"E1": [0.1, np.nan, 0.3], "E2": [0.2, np.nan, np.nan],
                      "deg_E1": [False, True, False], "deg_E2": [False, True, True]})
    S.check_nan_flag_agreement(U)
    U.loc[2, "deg_E2"] = False
    with pytest.raises(S.StopForReview):
        S.check_nan_flag_agreement(U)


def test_card_count_check_stops_on_changed_metadata():
    n = 1706
    D = pd.DataFrame({"site": [f"s{i % 23}" for i in range(n)], "dx": [1.0] * 869 + [0.0] * 837,
                      "ybocs": [10.0] * 856 + [np.nan] * (n - 856),
                      "med": [1] * 203 + [2] * 212 + [3] * (869 - 415) + [np.nan] * 837})
    assert S.card_count_check(D)["n_ocd_code1"] == (869, 869)
    D.loc[0, "dx"] = 0.0                                   # e.g. a re-coded diagnosis column
    with pytest.raises(S.StopForReview):
        S.card_count_check(D)


# ---------------------------------------------------------------------------------- decision rules
def test_holm_and_bh_values():
    assert np.allclose(S.holm([0.01, 0.04]), [0.02, 0.04])
    assert np.allclose(S.holm([0.04, 0.01]), [0.04, 0.02])
    assert np.allclose(S.holm([0.03, 0.02]), [0.04, 0.04])     # monotone step-down
    assert np.allclose(S.holm([0.6, 0.7]), [1.0, 1.0])
    assert np.allclose(S.bh([0.01, 0.04]), [0.02, 0.04])
    assert np.allclose(S.bh([0.03, 0.02]), [0.03, 0.03])


@pytest.mark.parametrize("p_holm,d,expected", [(0.049, 0.151, True), (0.049, 0.149, False), (0.050, 0.4, False),
                                               (0.001, -0.16, True), (0.001, -0.149, False)])
def test_survival_boundaries(p_holm, d, expected):
    assert S.endpoint_survives(p_holm, d) is expected


def test_primary_verdict_kill_rule_uses_holm_not_raw_p():
    # raw p 0.03 for both: Holm gives 0.06 / 0.06 -> neither survives although raw p < 0.05 and |d| large
    v = S.primary_verdict({"E1": {"p_fl": 0.03, "d": 0.4}, "E2": {"p_fl": 0.03, "d": 0.4}})
    assert v["topic1_killed"] and not v["endpoints"]["E1"]["survives"]
    v = S.primary_verdict({"E1": {"p_fl": 0.001, "d": 0.2}, "E2": {"p_fl": 0.5, "d": 0.5}})
    assert not v["topic1_killed"] and v["endpoints"]["E1"]["survives"] and not v["endpoints"]["E2"]["survives"]
    v = S.primary_verdict({"E1": {"p_fl": 0.001, "d": 0.10}, "E2": {"p_fl": 0.001, "d": -0.12}})
    assert v["topic1_killed"]


def _unit(d030c, d030t):
    return {"degenerate": {"030C": d030c, "030T": d030t}}


def test_degeneracy_rates_and_fallback_boundary():
    units = [_unit(False, False)] * 89 + [_unit(True, False)] * 5 + [_unit(False, True)] * 6
    r = S.degeneracy_rates(units)
    assert r["n"] == 100 and r["rate_E1"] == pytest.approx(0.05) and r["rate_E2"] == pytest.approx(0.11)
    assert S.fallback_decision(r)["primary_density"] == 0.15           # E2 > 10 % triggers
    r9 = S.degeneracy_rates([_unit(False, False)] * 91 + [_unit(True, True)] * 9)
    assert S.fallback_decision(r9)["primary_density"] == 0.10
    r10 = S.degeneracy_rates([_unit(False, False)] * 90 + [_unit(False, True)] * 10)
    assert S.fallback_decision(r10)["fallback_triggered"] is False      # "more than 10 %"


def test_raw_welch_is_labelled_descriptive_and_fl_is_the_primary_p():
    D = _design(2)
    rng = np.random.default_rng(2)
    ocdfrac = D.groupby("site")["dx"].transform("mean").values
    y = 8.0 * ocdfrac + rng.standard_normal(len(D))                      # pure site confound, no dx effect
    r = S.dx_effect(y, D, B=999)
    assert r["welch_p_DESCRIPTIVE"] < 1e-4                               # pooled Welch is fooled by site
    assert r["p_fl"] > 0.01                                              # site-adjusted FL is not
    assert "p_fl" in r and "raw_cohen_d_DESCRIPTIVE" in r


def test_assoc_effect_standardised_beta():
    D = _design(3)
    rng = np.random.default_rng(3)
    x = rng.standard_normal(len(D))
    y = 2.0 * x + rng.standard_normal(len(D))
    r = S.assoc_effect(y, x, D, B=199)
    assert r["beta"] == pytest.approx(2.0, abs=0.3)
    assert r["std_beta"] == pytest.approx(r["beta"] * np.std(x, ddof=1) / np.std(y, ddof=1))
    assert r["p_fl"] == pytest.approx(1 / 200)


# ---------------------------------------------------------------------------------- runner: variants, truncation
@pytest.mark.parametrize("tr", [0.7, 0.8, 0.85, 1.0, 1.73, 1.8, 2.0])
def test_200s_truncation_gives_exactly_100_grid_samples(tr):
    from src.topic1_lagmotif.preprocess import preprocess
    L = RC.trunc_samples(tr)
    X = np.random.default_rng(0).standard_normal((L, 5)) + 1e4
    assert preprocess(X, tr).shape[0] == 100
    # the rejected ceil rule gives 101 at some TRs; floor must never exceed 200 s
    assert L * tr <= 200.0 + 1e-9


def test_variant_specs_change_the_params_hash_and_primary_has_no_overrides():
    from src.topic1_lagmotif.pipeline import params_sha256
    prim = RC.variant_spec("primary", None)
    assert prim["kw"] == {} and params_sha256(prim["params"]) == RC.FROZEN_PARAMS_SHA256
    hashes = {params_sha256(RC.variant_spec(v, 0.10)["params"]) for v in ("dct128", "af40")}
    assert RC.FROZEN_PARAMS_SHA256 not in hashes and len(hashes) == 2
    vs = {RC.variant_sha(v, RC.variant_spec(v, 0.10)) for v in RC.VARIANTS}
    assert len(vs) == 4
    assert RC.variant_sha("trunc200", RC.variant_spec("trunc200", 0.10)) != \
        RC.variant_sha("trunc200", RC.variant_spec("trunc200", 0.15))


def test_cohort_digest_detects_a_remapped_listing():
    names = [f"n{i:04d}" for i in range(10)]
    d0 = RC.cohort_digest(names)
    assert RC.cohort_digest(list(names)) == d0
    assert RC.cohort_digest(names[:-1]) != d0
    assert RC.cohort_digest(names[:3] + ["x"] + names[3:9]) != d0


def test_exclusions_are_counted_by_class_group_and_site():
    """Defect caught (card 3: 'both counts are reported by group and site'): an exclusion class (failed
    extraction, missing covariate, degenerate endpoint) being dropped from the by-group / by-site report."""
    D_all = pd.DataFrame({"site": ["A", "A", "A", "B", "B", "B"], "dx": [1.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                          "age": [20.0, np.nan, 30.0, 40.0, 50.0, 60.0], "sex2": [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                          "logdur": [5.0] * 6}, index=pd.Index(range(6), name="position"))
    recs = {0: {"ok": True}, 1: {"ok": True}, 2: {"ok": True}, 3: {"ok": False}, 4: {"ok": True}, 5: {"ok": True}}
    U = pd.DataFrame({"deg_E1": [False, False, False, True], "deg_E2": [True, False, False, True]},
                     index=pd.Index([0, 2, 4, 5], name="position"))
    x = S.exclusions_by(D_all, recs, U, "broadband@0.10")
    assert x["total"] == {"n": 6, "extraction_failed": 1, "covariate_missing": 1, "degenerate_E1": 1,
                          "degenerate_E2": 2}
    assert x["by_group"]["HC"] == {"n": 3, "extraction_failed": 1, "covariate_missing": 1, "degenerate_E1": 1,
                                   "degenerate_E2": 1}
    assert x["by_site"]["A"]["covariate_missing"] == 1 and x["by_site"]["B"]["extraction_failed"] == 1
    assert x["by_site_group"]["A|OCD"]["degenerate_E2"] == 1
