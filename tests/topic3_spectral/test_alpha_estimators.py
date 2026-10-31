"""Decay-exponent fixtures: code correctness on exact laws / iid Pareto, and the finite-n bias guard
that forbids subject-level alpha claims."""
import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT  # noqa: F401
from src.topic3_spectral.estimators import centered_eigs, clauset_mle, rank_slope


@pytest.mark.parametrize("a", [0.5, 1.0, 1.7, 3.0])
def test_rank_slope_exact_on_exact_power_law(a):
    lam = 4.2 * np.arange(1, 301, dtype=float) ** (-a)
    assert rank_slope(lam) == pytest.approx(a, abs=1e-10)


@pytest.mark.parametrize("alpha", [1.5, 2.0, 3.0])
def test_clauset_mle_recovers_iid_pareto_density_exponent(alpha):
    rng = np.random.default_rng(int(alpha * 10))
    est = [clauset_mle(1.0 * (1 - rng.random(2000)) ** (-1.0 / (alpha - 1)))["alpha"] for _ in range(20)]
    assert np.mean(est) == pytest.approx(alpha, abs=0.05)


def test_clauset_on_exact_rank_law_gives_one_plus_one_over_a():
    for a in (0.5, 1.0, 2.0):
        lam = np.arange(1, 5001, dtype=float) ** (-a)
        assert clauset_mle(lam)["alpha"] == pytest.approx(1 + 1 / a, abs=0.05)


def test_finite_n_bias_guard_subject_level_alpha_not_estimable():
    """Sampled 57 x 1536 rows with l_i = i^-0.5: Clauset is far from the population value,
    so subject-level alpha must not carry a claim (stated limitation; card forbids it)."""
    rng = np.random.default_rng(5)
    lam = np.arange(1, 1537, dtype=float) ** (-0.5)
    pop = clauset_mle(lam[:56])["alpha"]
    est = np.mean([clauset_mle(centered_eigs(rng.standard_normal((57, 1536)) * np.sqrt(lam)))["alpha"]
                   for _ in range(10)])
    assert abs(est - pop) > 0.15


def test_rank_slope_window_validation():
    with pytest.raises(ValueError):
        rank_slope(np.array([1.0, 0.5, 0.2]))
