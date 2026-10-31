"""A2 'would FAIL on the defect it targets': each block re-creates a known v1-style defect and
shows that the corresponding fixture criterion rejects it (while v2 passes, see other files)."""
import numpy as np

import tests.topic1_lagmotif.conftest_helpers  # noqa: F401
from src.topic1_lagmotif.flow import lagged_net_flow
from src.topic1_lagmotif.preprocess import preprocess, zscore
from tests.topic1_lagmotif.test_flow_chain import _lead_lag_signal, _sample


def test_lag_in_samples_defect_fails_two_tr_ratio_criterion():
    rng = np.random.default_rng(11)
    X = _lead_lag_signal(1200.0, 6, rng)
    F20 = lagged_net_flow(preprocess(_sample(X, 2.0), 2.0), 1)
    # defect: lag = 1 native sample (0.7 s) instead of 2 s, no common grid
    Fbad = lagged_net_flow(zscore(_sample(X, 0.7)), 1)
    pairs = [(2 * k, 2 * k + 1) for k in range(6)]
    ratio = np.mean([abs(Fbad[i, j]) for i, j in pairs]) / np.mean([abs(F20[i, j]) for i, j in pairs])
    assert not (0.85 <= ratio <= 1.15), ratio


def test_resampling_raw_scale_without_detrend_fails_offset_criterion():
    rng = np.random.default_rng(3)
    X = _sample(_lead_lag_signal(400.0, 4, rng), 0.7)
    F0 = lagged_net_flow(preprocess(X, 0.7), 1)
    Fbad = lagged_net_flow(preprocess(1.15e4 + X, 0.7, detrend_type="none", padtype="constant"), 1)
    assert not np.allclose(F0, Fbad, atol=1e-8)
    iu = np.triu_indices(F0.shape[0], 1)
    assert np.corrcoef(F0[iu], Fbad[iu])[0, 1] < 0.99


def test_keeping_zero_padding_fails_padding_criterion():
    rng = np.random.default_rng(1)
    base = 1.15e4 + 30 * rng.standard_normal((160, 12))
    padded = np.vstack([base, np.zeros((144, 12))])
    F_ok = lagged_net_flow(preprocess(base, 2.0), 1)
    F_bad = lagged_net_flow(preprocess(padded, 2.0), 1)  # defect: padding not stripped
    assert not np.array_equal(F_ok, F_bad)
