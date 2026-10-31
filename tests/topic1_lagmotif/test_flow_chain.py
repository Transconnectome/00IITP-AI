"""A1/A2: lag in seconds, detrend-before-resample, time reversal, two-TR consistency, 304 ROIs, top-k."""
import numpy as np
import pytest

import tests.topic1_lagmotif.conftest_helpers  # noqa: F401
from src.topic1_lagmotif import synthetic
from src.topic1_lagmotif.data import prepare_series
from src.topic1_lagmotif.flow import (gradient_component, gradient_share, lag_seconds_to_samples, lagged_net_flow,
                                      oriented_topk_graph)
from src.topic1_lagmotif.pipeline import PARAMS, subject_flow
from src.topic1_lagmotif.preprocess import preprocess, resample_ratio


def _lead_lag_signal(duration_s, n_pairs, rng, lead_s=2.0, dt=0.05):
    """Continuous band-limited signals; ROI 2k+1 follows ROI 2k by lead_s seconds."""
    t, s = synthetic.bandlimited_sources(duration_s + 20, 2 * n_pairs, dt, 0.2, rng)
    X = s.copy()
    shift = int(round(lead_s / dt))
    for k in range(n_pairs):
        X[shift:, 2 * k + 1] = 0.8 * s[:-shift, 2 * k] + 0.6 * s[shift:, 2 * k + 1]
    X = X[int(10 / dt): int(10 / dt) + int(duration_s / dt)]
    return X


def _sample(X, tr, dt=0.05):
    return X[:: int(round(tr / dt))]


def test_resample_ratios_are_exact():
    assert resample_ratio(0.7) == (7, 20)
    assert resample_ratio(0.85) == (17, 40)
    assert resample_ratio(1.73) == (173, 200)
    assert resample_ratio(2.0) == (1, 1)
    assert lag_seconds_to_samples(PARAMS["lag_s"], PARAMS["grid_dt_s"]) == 1
    with pytest.raises(ValueError):
        lag_seconds_to_samples(3.0, 2.0)


def test_two_tr_sampling_gives_consistent_flow_magnitude_and_direction():
    rng = np.random.default_rng(11)
    X = _lead_lag_signal(1200.0, 6, rng)
    F20 = lagged_net_flow(preprocess(1.15e4 + 30 * _sample(X, 2.0), 2.0), 1)
    F07 = lagged_net_flow(preprocess(1.15e4 + 30 * _sample(X, 0.7), 0.7), 1)
    pairs = [(2 * k, 2 * k + 1) for k in range(6)]
    a20 = np.array([F20[i, j] for i, j in pairs]); a07 = np.array([F07[i, j] for i, j in pairs])
    assert np.all(a20 > 0) and np.all(a07 > 0)      # ROI 2k leads ROI 2k+1 at both TRs
    ratio = np.mean(np.abs(a07)) / np.mean(np.abs(a20))
    assert 0.85 <= ratio <= 1.15, ratio


def test_time_reversal_negates_flow_through_full_chain():
    rng = np.random.default_rng(5)
    X = _lead_lag_signal(600.0, 5, rng)
    raw20 = 1.15e4 + 30 * _sample(X, 2.0) + 0.01 * np.arange(300)[:, None]
    F = lagged_net_flow(preprocess(raw20, 2.0), 1)
    Fr = lagged_net_flow(preprocess(raw20[::-1], 2.0), 1)
    assert np.allclose(Fr, -F, atol=1e-10, rtol=0)            # exact at TR 2.0 (no resampling)
    for tr in (0.7, 1.73):
        raw = 1.15e4 + 30 * _sample(X, tr)
        F = lagged_net_flow(preprocess(raw, tr), 1)
        Fr = lagged_net_flow(preprocess(raw[::-1], tr), 1)
        iu = np.triu_indices(F.shape[0], 1)
        assert np.corrcoef(Fr[iu], -F[iu])[0, 1] > 0.999, tr


def test_detrend_before_resample_makes_offset_and_linear_trend_irrelevant():
    rng = np.random.default_rng(3)
    X = _sample(_lead_lag_signal(400.0, 4, rng), 0.7)
    trend = np.linspace(0, 50, X.shape[0])[:, None] * rng.uniform(0.5, 1.5, X.shape[1])
    F0 = lagged_net_flow(preprocess(X, 0.7), 1)
    F1 = lagged_net_flow(preprocess(1.15e4 + X + trend, 0.7), 1)
    assert np.allclose(F0, F1, atol=1e-8)


def test_full_chain_uses_all_304_rois_and_exact_edge_count():
    rng = np.random.default_rng(4)
    raw = 1.15e4 + 30 * rng.standard_normal((180, 304))
    s = prepare_series(raw, 2.0, PARAMS["head_trim_s"], position=0)
    F = subject_flow(s)
    assert F.shape == (304, 304)
    assert np.allclose(F, -F.T)
    for d, m in ((0.05, 2303), (0.10, 4606), (0.15, 6908)):
        A = oriented_topk_graph(F, d)
        assert int(A.sum()) == m
        assert int((A * A.T).sum()) == 0 and int(np.trace(A)) == 0
        iu = np.triu_indices(304, 1)
        # every kept pair has |F| >= every dropped pair
        kept = (A + A.T)[iu] > 0
        assert np.abs(F[iu])[kept].min() >= np.abs(F[iu])[~kept].max()
        src, dst = np.nonzero(A)
        assert np.all(F[src, dst] > 0)


def test_gradient_share_is_one_for_pure_potential_flow_and_zero_for_pure_cycle():
    p = np.random.default_rng(0).standard_normal(20)
    Fg = p[:, None] - p[None, :]
    assert gradient_share(Fg) == pytest.approx(1.0)
    assert np.allclose(gradient_component(Fg), Fg)
    Fc = np.zeros((3, 3)); Fc[0, 1] = Fc[1, 2] = Fc[2, 0] = 1.0; Fc = Fc - Fc.T
    assert gradient_share(Fc) == pytest.approx(0.0, abs=1e-12)
