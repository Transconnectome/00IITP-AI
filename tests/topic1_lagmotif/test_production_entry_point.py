"""A2 fail-on-defect at the PRODUCTION entry point (NpyCohort.load / prepare_series -> pipeline.subject_flow
-> extract_subject / motif_statistics), at TRs other than 2.0 s.

Proposed by explorer_r2_3 (iteration 2) to close the challenger_r1_1 REFUTED item: in iteration 1 every
subject_flow / extract_subject test used a TR 2.0 site, and the two-TR / reversal fixtures called preprocess()
and lagged_net_flow() directly, so pipeline-wiring defects (TR not passed, lag in native samples, lag 4 s,
detrend off, z-score off, head trim in samples) passed all 29 tests.

Design rules:
  * The spec oracle below is written from the FROZEN CARD TEXT (section 1) with scipy/numpy primitives only;
    it does not import preprocess/flow helpers and does not read PARAMS, so a PARAMS or wiring change in
    production cannot also change the oracle.
  * The physical tests use a continuous lead-lag signal with known lead (2 s vs 4 s) sampled at several TRs.
"""
import math

import numpy as np
import pytest
from scipy.signal import detrend as sp_detrend
from scipy.signal import resample_poly as sp_resample_poly

import tests.topic1_lagmotif.conftest_helpers  # noqa: F401
from src.topic1_lagmotif import synthetic
from src.topic1_lagmotif.data import NpyCohort, prepare_series
from src.topic1_lagmotif.motifs import census, motif_statistics, null_counts, sample_null_graph
from src.topic1_lagmotif.pipeline import PARAMS, extract_subject, params_sha256, subject_flow

# Card section 1 constants (hard-coded on purpose; see module docstring).
CARD_TRIM_S = 40.0
CARD_RATIO = {0.7: (7, 20), 0.8: (2, 5), 0.85: (17, 40), 1.0: (1, 2), 1.73: (173, 200), 1.8: (9, 10), 2.0: (1, 1)}
CARD_N_TRIM = {0.7: 58, 0.8: 50, 0.85: 48, 1.0: 40, 1.73: 24, 1.8: 23, 2.0: 20}
CARD_PARAMS_SHA = "86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6"
SITE_AT_TR = {0.7: "Yale-Pittinger-HCP-Trio", 0.8: "Dresden", 0.85: "NYSPI-Columbia-Adults", 1.0: "New-York",
              1.73: "Cape-Town-UCT-Skyra", 1.8: "Bergen", 2.0: "Yale-Gruner"}
DT = 0.05  # fine grid of the continuous synthetic signal


def _spec_oracle_flow(X_valid, tr):
    """Card section 1: linear detrend at native TR -> resample_poly(up, down, padtype='line') to 2.0 s ->
    z-score (ddof 0) -> C[i,j] = mean_t z_i(t) z_j(t+1) -> F = C - C^T, diag 0."""
    Y = sp_detrend(np.asarray(X_valid, dtype=np.float64), axis=0, type="linear")
    up, down = CARD_RATIO[tr]
    if (up, down) != (1, 1):
        Y = sp_resample_poly(Y, up, down, axis=0, padtype="line")
    Z = (Y - Y.mean(axis=0)) / Y.std(axis=0)
    C = Z[:-1].T @ Z[1:] / float(Z.shape[0] - 1)
    F = C - C.T
    np.fill_diagonal(F, 0.0)
    return F


def _lead_signal(duration_s, leads_s, rng, gain=0.8, own=0.6):
    """Continuous band-limited sources; for each lead L in leads_s a pair (2k, 2k+1) with ROI 2k+1 following
    ROI 2k by L seconds. Returns the fine-grid series (dt = DT)."""
    n = 2 * len(leads_s)
    _, s = synthetic.bandlimited_sources(duration_s + 40, n, DT, 0.2, rng)
    X = s.copy()
    for k, L in enumerate(leads_s):
        sh = int(round(L / DT))
        X[sh:, 2 * k + 1] = gain * s[:-sh, 2 * k] + own * s[sh:, 2 * k + 1]
    return X[int(20 / DT): int(20 / DT) + int(duration_s / DT)]


def _raw_at(X, tr, rng=None):
    """Sample at TR and put on raw scale with an offset and a per-ROI linear drift (as the npy data are)."""
    x = X[:: int(round(tr / DT))]
    drift = np.linspace(0.0, 40.0, x.shape[0])[:, None] * np.linspace(0.5, 1.5, x.shape[1])[None, :]
    return 1.15e4 + 30.0 * x + drift


def test_frozen_params_are_the_carded_params():
    assert params_sha256() == CARD_PARAMS_SHA


@pytest.mark.parametrize("tr", sorted(CARD_RATIO))
def test_prepare_series_trims_in_seconds_at_every_on_disk_tr(tr):
    rng = np.random.default_rng(int(tr * 100))
    raw = 1.15e4 + 30 * rng.standard_normal((300, 6))
    padded = np.vstack([raw, np.zeros((40, 6))])
    s = prepare_series(padded, tr, PARAMS["head_trim_s"], position=0)
    assert CARD_N_TRIM[tr] == math.ceil(CARD_TRIM_S / tr - 1e-9)
    assert s.n_trim == CARD_N_TRIM[tr]
    assert s.raw_valid_T == 300 and s.valid_T == 300 - CARD_N_TRIM[tr]
    assert np.array_equal(s.X, raw[CARD_N_TRIM[tr]:])
    assert s.duration_s == pytest.approx((300 - CARD_N_TRIM[tr]) * tr)


@pytest.mark.parametrize("tr", sorted(CARD_RATIO))
def test_subject_flow_equals_card_spec_oracle_at_every_on_disk_tr(tr):
    rng = np.random.default_rng(7)
    raw = _raw_at(_lead_signal(700.0, [2.0, 4.0, 2.0], rng), tr)
    s = prepare_series(raw, tr, PARAMS["head_trim_s"], position=0)
    F = subject_flow(s)
    F_ref = _spec_oracle_flow(raw[CARD_N_TRIM[tr]:], tr)
    assert F.shape == F_ref.shape
    assert np.allclose(F, F_ref, atol=1e-12, rtol=0), float(np.max(np.abs(F - F_ref)))


@pytest.mark.parametrize("tr", [0.7, 0.85, 1.0, 1.73])
def test_subject_flow_lag_is_two_seconds_through_loader(tmp_path, tr):
    """Same continuous signal written as two fake subjects (a TR-`tr` site and a TR-2.0 site) and loaded with
    NpyCohort.load (the production loader). Pair A has a 2 s lead, pair B a 4 s lead, pair C a 2 s lead in the
    opposite direction. A lag of 2 s gives |F_A| >> |F_B|; lag 4 s, lag in native samples or no resampling
    break the |F| ratio to TR 2.0, the 2s-vs-4s ordering, or both."""
    rng = np.random.default_rng(11)
    X = _lead_signal(1200.0, [2.0, 4.0, 2.0], rng)
    X[:, [4, 5]] = X[:, [5, 4]]   # pair C reversed: ROI 5 leads ROI 4
    d = tmp_path / "npy"
    d.mkdir()
    names = {}
    for t, nm in ((2.0, "FAKEsubjTRtwo0"), (tr, "FAKEsubjTRx001")):
        (d / nm).mkdir()
        np.save(d / nm / f"{nm}.npy", _raw_at(X, t))
        names[nm] = SITE_AT_TR[t]
    coh = NpyCohort(str(d), names, trim_s=PARAMS["head_trim_s"])
    order = sorted(names)  # positional index = sorted(listdir)
    s2 = coh.load(order.index("FAKEsubjTRtwo0"))
    sx = coh.load(order.index("FAKEsubjTRx001"))
    assert s2.tr == 2.0 and sx.tr == tr
    F2, Fx = subject_flow(s2), subject_flow(sx)
    for F in (F2, Fx):
        assert F[0, 1] > 0 and F[2, 3] > 0 and F[5, 4] > 0       # leader -> follower orientation
        assert F[0, 1] > 2.0 * F[2, 3]                            # lag 2 s, not 4 s
        assert F[5, 4] > 2.0 * F[2, 3]
    for (i, j) in ((0, 1), (5, 4)):
        assert 0.85 <= Fx[i, j] / F2[i, j] <= 1.15, (tr, i, j, Fx[i, j] / F2[i, j])
    feats = extract_subject(sx, densities=[0.10], channels=["broadband"], n_null=20)
    assert feats["tr"] == tr and feats["n_trim"] == CARD_N_TRIM[tr]
    assert feats["params_sha256"] == CARD_PARAMS_SHA


def test_flow_is_invariant_to_offset_scale_and_linear_drift_at_tr_07():
    rng = np.random.default_rng(3)
    x = _lead_signal(500.0, [2.0, 2.0], rng)[:: int(round(0.7 / DT))]
    t = np.arange(x.shape[0])[:, None]
    F0 = subject_flow(prepare_series(1.0 + x, 0.7, PARAMS["head_trim_s"], position=0))
    F1 = subject_flow(prepare_series(1.15e4 + 37.0 * x + 0.05 * t * np.arange(1, 5)[None, :], 0.7,
                                     PARAMS["head_trim_s"], position=0))
    assert np.allclose(F0, F1, atol=1e-10, rtol=0)
    assert np.max(np.abs(F0)) <= 1.0   # z-scored lag-1 cross-correlations are bounded


def _transitive_tournament(n):
    A = np.zeros((n, n), np.int8)
    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = 1
    return A


def test_degenerate_null_gives_nan_z_and_flag_never_a_finite_number():
    """Card section 3 excludes a subject when its primary null is degenerate ('Z NaN'): a transitive tournament
    has a unique graph in its degree class, so every null equals the observed graph."""
    A = _transitive_tournament(7)
    r = motif_statistics(A, 30, 20, PARAMS["p_rot"], np.arange(30))
    assert r["degenerate"]["030C"] and r["degenerate"]["030T"]
    assert math.isnan(r["Z"]["030C"]) and math.isnan(r["Z"]["030T"])
    assert math.isnan(r["E1_Z030C"]) and math.isnan(r["E2_Z030C_minus_Z030T"])
    assert np.isfinite(r["log_ratio_030C"])


def test_null_moments_of_all_five_classes_equal_census_of_independent_null_graphs():
    """Per-null counts from the production ensemble path must equal census() of the null graph drawn with the
    same seed by sample_null_graph; the 021C/021D/021U moments are then checked against that census."""
    rng = np.random.default_rng(21)
    Z = rng.standard_normal((300, 40))
    from src.topic1_lagmotif.flow import lagged_net_flow, oriented_topk_graph  # graph construction only
    A = oriented_topk_graph(lagged_net_flow((Z - Z.mean(0)) / Z.std(0), 1), 0.15)
    seeds = np.arange(100, 160)
    r = motif_statistics(A, len(seeds), 20, PARAMS["p_rot"], seeds)
    cs = [census(sample_null_graph(A, 20, PARAMS["p_rot"], int(s))) for s in seeds]
    for k in ("021D", "021U", "021C", "030T", "030C"):
        v = np.array([c[k] for c in cs], dtype=float)
        assert r["null_mean"][k] == pytest.approx(float(v.mean()), abs=1e-9), k
        assert r["null_sd"][k] == pytest.approx(float(v.std(ddof=1)), abs=1e-9), k


def test_each_null_is_an_independent_restart_from_the_observed_graph():
    rng = np.random.default_rng(5)
    Z = rng.standard_normal((300, 40))
    from src.topic1_lagmotif.flow import lagged_net_flow, oriented_topk_graph
    A = oriented_topk_graph(lagged_net_flow((Z - Z.mean(0)) / Z.std(0), 1), 0.15)
    nc = null_counts(A, 4, 20, PARAMS["p_rot"], np.array([9, 9, 9, 9]))
    assert len(set(nc["030T"].tolist())) == 1 and len(set(nc["030C"].tolist())) == 1


def test_null_counts_raises_when_any_null_violates_an_invariant(monkeypatch):
    """The per-null invariant flags must stop the run (reviewer_r1_1: disabling the raise survived all tests)."""
    from src.topic1_lagmotif import motifs
    A = _transitive_tournament(5)
    real = motifs._null_ensemble

    def broken(*args):
        t, c, acc, flags = real(*args)
        flags = flags.copy()
        flags[-1] = 3  # pretend the last null acquired a mutual edge
        return t, c, acc, flags

    monkeypatch.setattr(motifs, "_null_ensemble", broken)
    with pytest.raises(motifs.NullInvariantError):
        motifs.null_counts(A, 5, 20, PARAMS["p_rot"], np.arange(5))
    with pytest.raises(motifs.NullInvariantError):
        motif_statistics(A, 5, 20, PARAMS["p_rot"], np.arange(5))
