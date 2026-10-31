"""Resampling fixtures: subsampling is without replacement and covers; the with-replacement row
bootstrap is shown to bias PR; sign-flip test size/power; Holm; nulls preserve marginals."""
import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT  # noqa: F401
from src.topic3_spectral.estimators import pr_cov
from src.topic3_spectral.resampling import (column_permutation_null, holm, paired_subsample_delta,
                                            sign_flip_test, subject_bootstrap_ci, subsample_indices)


def _pair(rng, n, d, la, lb):
    Z = rng.standard_normal((n, d))
    return Z * np.sqrt(la), (0.7 * Z + np.sqrt(0.51) * rng.standard_normal((n, d))) * np.sqrt(lb)


def test_subsample_indices_are_without_replacement_and_reproducible():
    I = subsample_indices(57, 28, 300, seed=3)
    assert I.shape == (300, 28)
    assert all(len(set(row.tolist())) == 28 for row in I)
    np.testing.assert_array_equal(I, subsample_indices(57, 28, 300, seed=3))
    with pytest.raises(ValueError):
        subsample_indices(10, 10, 5, seed=0)


def test_with_replacement_row_bootstrap_biases_pr_downward():
    """Why the card forbids it: duplicated rows lower the rank of the centered matrix."""
    rng = np.random.default_rng(7)
    lam = np.arange(1, 769, dtype=float) ** (-0.7)
    X = rng.standard_normal((57, 768)) * np.sqrt(lam)
    full = pr_cov(X)
    boot = np.mean([pr_cov(X[rng.integers(0, 57, 57)]) for _ in range(200)])
    assert boot < 0.85 * full


def test_paired_subsampling_interval_covers_zero_under_null():
    """Null: both representations share the population spectrum, so Delta_m = 0.
    Coverage of the 95% stability interval within 2 MC SE of 0.95 at R = 200."""
    rng = np.random.default_rng(20261031)
    n, d, m = 57, 256, 28
    lam = np.arange(1, d + 1, dtype=float) ** (-1.0)
    R, cover = 200, 0
    for r in range(R):
        A, B = _pair(rng, n, d, lam, lam)
        res = paired_subsample_delta(A, B, m, 150, seed=r)
        cover += res["lo"] <= 0.0 <= res["hi"]
    se = np.sqrt(0.95 * 0.05 / R)
    assert abs(cover / R - 0.95) <= 2 * se + 0.01


def test_paired_subsampling_detects_planted_spectral_difference():
    rng = np.random.default_rng(1)
    n, d, m = 57, 256, 28
    A, B = _pair(rng, n, d, np.arange(1, d + 1, dtype=float) ** (-0.6), np.arange(1, d + 1, dtype=float) ** (-1.4))
    res = paired_subsample_delta(A, B, m, 300, seed=2)
    assert res["lo"] > 0


def test_sign_flip_size_and_power():
    rng = np.random.default_rng(3)
    rej = sum(sign_flip_test(rng.standard_normal(57), 999, seed=i) < 0.05 for i in range(300))
    assert abs(rej / 300 - 0.05) <= 2 * np.sqrt(0.05 * 0.95 / 300) + 0.01
    assert sign_flip_test(rng.standard_normal(57) - 0.6, 999, seed=1) < 0.01


def test_subject_bootstrap_ci_contains_true_mean_most_of_the_time():
    rng = np.random.default_rng(4)
    hits = 0
    for i in range(200):
        lo, hi = subject_bootstrap_ci(rng.standard_normal(57) + 0.3, 999, seed=i)
        hits += lo <= 0.3 <= hi
    assert hits / 200 >= 0.89


def test_holm_matches_hand_computation():
    np.testing.assert_allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
    np.testing.assert_allclose(holm([0.5, 0.001]), [0.5, 0.002])


def test_column_permutation_null_preserves_each_column_and_breaks_dependence():
    rng = np.random.default_rng(5)
    z = rng.standard_normal((57, 1))
    X = z @ rng.standard_normal((1, 100)) + 0.05 * rng.standard_normal((57, 100))
    null = column_permutation_null(X, 50, seed=0)
    assert pr_cov(X) < 1.5 and null.min() > 20
