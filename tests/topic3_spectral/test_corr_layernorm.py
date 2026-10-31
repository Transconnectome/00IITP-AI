"""LayerNorm confound fixtures: corrPR is invariant to per-channel affine maps, covPR is not;
per-token LN0; layer_3 reshape; dynamic range of corrPR after LN0 at the primary shape."""
import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT  # noqa: F401
from src.topic3_spectral.estimators import (layer3_tokens, layernorm0, pr_corr, pr_cov,
                                            standardize_columns)


def _lowrank_tokens(n, d, rank, noise, seed, scale_sigma=1.5):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((n, rank)) @ rng.standard_normal((rank, d)) + noise * rng.standard_normal((n, d))
    return Z * np.exp(scale_sigma * rng.standard_normal(d)) + rng.standard_normal(d)


def test_corrpr_exactly_invariant_to_per_channel_gain_and_bias_covpr_not():
    rng = np.random.default_rng(0)
    X = layernorm0(_lowrank_tokens(160, 1536, 10, 0.3, seed=1))
    g = np.exp(1.0 * rng.standard_normal(1536)) * rng.choice([-1.0, 1.0], 1536)
    b = rng.standard_normal(1536)
    Y = X * g + b
    assert standardize_columns(X)[1] == 0 and standardize_columns(Y)[1] == 0
    assert pr_corr(Y) == pytest.approx(pr_corr(X), abs=1e-9)
    assert abs(pr_cov(Y) - pr_cov(X)) / pr_cov(X) > 0.2


def test_a_large_variance_floor_would_break_gain_invariance():
    """Why the card fixes the floor at 1e-3 x median SD (dead-channel guard only)."""
    rng = np.random.default_rng(0)
    X = layernorm0(_lowrank_tokens(160, 1536, 10, 0.3, seed=1))
    Y = X * np.exp(1.0 * rng.standard_normal(1536))
    assert abs(pr_corr(Y, 0.1) - pr_corr(X, 0.1)) > 1e-3


def test_pooled_layernorm_output_is_per_channel_affine_of_pooled_ln0():
    """mean over tokens of (g * LN0(h) + b) = g * mean(LN0(h)) + b, so pooled-L3 corrPR removes g, b."""
    rng = np.random.default_rng(2)
    subj = [layernorm0(rng.standard_normal((160, 64)) + rng.standard_normal(64)) for _ in range(30)]
    g, b = np.exp(rng.standard_normal(64)), rng.standard_normal(64)
    P0 = np.stack([s.mean(0) for s in subj])
    P1 = np.stack([(s * g + b).mean(0) for s in subj])
    assert pr_corr(P1) == pytest.approx(pr_corr(P0), abs=1e-9)


def test_layernorm0_rows_have_zero_mean_unit_variance():
    X = layernorm0(_lowrank_tokens(50, 300, 5, 0.1, seed=3))
    np.testing.assert_allclose(X.mean(1), 0, atol=1e-10)
    np.testing.assert_allclose(X.var(1), 1, atol=1e-3)


def test_variance_floor_drops_dead_channels():
    rng = np.random.default_rng(4)
    X = rng.standard_normal((100, 50))
    X[:, :3] *= 1e-6
    Z, nd = standardize_columns(X, 0.1)
    assert nd == 3 and Z.shape == (100, 47)


def test_layer3_reshape_matches_model_token_order():
    """ver11 builds layer_3 as x(L=(t,d,h,w), C).view(c,t,d,h,w).permute(c,d,h,w,t)."""
    C, T, D, H, W = 6, 20, 2, 2, 2
    tokens = np.arange(T * D * H * W * C, dtype=float).reshape(T * D * H * W, C)   # (L, C), L in (t,d,h,w) order
    dump = tokens.T.reshape(C, T, D, H, W).transpose(0, 2, 3, 4, 1)              # (C, D, H, W, T)
    back = layer3_tokens(dump)
    assert back.shape == (160, 6)
    np.testing.assert_array_equal(back, tokens)
    assert layer3_tokens(np.zeros((1536, 2, 2, 2, 20))).shape == (160, 1536)


def test_corrpr_after_ln0_tracks_rank_at_primary_shape():
    """Dynamic-range fixture at the primary analysis shape (7 frames x 160 tokens = 1120 x 1536):
    corrPR after LN0 increases monotonically with planted rank and stays far below the ceiling."""
    v = {r: pr_corr(layernorm0(_lowrank_tokens(1120, 1536, r, 0.3, seed=r))) for r in (3, 12, 40)}
    assert 2.0 <= v[3] <= 6.0
    assert 7.0 <= v[12] <= 14.0
    assert v[40] > v[12] + 2.0 > v[3] + 4.0
    assert max(v.values()) < 0.05 * 1119
