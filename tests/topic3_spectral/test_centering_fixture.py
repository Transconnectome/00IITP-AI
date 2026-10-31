"""T3.1/T3.3: the centering defect behind empirical_results.json PR~1 is caught by a fixture."""
import numpy as np
import pytest

from tests.topic3_spectral.helpers import exact_spectrum_matrix
from src.topic3_spectral.estimators import centered_eigs, pr_cov, pr_from_eigs, mean_energy_fraction


@pytest.mark.parametrize("k", [1, 5, 20, 56])
def test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one(k):
    from src.spectral_rg_flow_diagnostic import compute_participation_ratio as old_uncentered
    from src.empirical_connectome_ablation import estimate_powerlaw_alpha as old_centered
    X = exact_spectrum_matrix(57, [3.0] * k, 1536, seed=k, offset_sd=30.0)
    assert pr_cov(X) == pytest.approx(k, rel=1e-9)
    assert old_centered(X)[1] == pytest.approx(k, rel=1e-6)       # report's estimator is centered
    assert old_uncentered(X) < 1.1                                  # json's estimator collapses to ~1
    assert mean_energy_fraction(X) > 0.95


def test_prescribed_unequal_singular_values_give_analytic_pr():
    s = np.array([5.0, 3.0, 2.0, 1.0, 0.5])
    X = exact_spectrum_matrix(40, s, 300, seed=3)
    lam = s ** 2
    assert pr_cov(X) == pytest.approx(lam.sum() ** 2 / (lam ** 2).sum(), rel=1e-9)


def test_pr_invariant_to_row_permutation_mean_shift_and_rotation():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((57, 200)) * np.linspace(3, 0.1, 200)
    base = pr_cov(X)
    assert pr_cov(X[rng.permutation(57)]) == pytest.approx(base, rel=1e-10)
    assert pr_cov(X + 100.0 * rng.standard_normal(200)) == pytest.approx(base, rel=1e-8)
    Q, _ = np.linalg.qr(rng.standard_normal((200, 200)))
    assert pr_cov(X @ Q) == pytest.approx(base, rel=1e-8)


def test_pr_bounded_by_n_minus_one_and_gram_trick_matches_direct():
    rng = np.random.default_rng(1)
    for n, d in [(25, 288), (57, 1536), (300, 50)]:
        X = rng.standard_normal((n, d))
        ev = centered_eigs(X)
        assert ev.size == min(n - 1, d)
        Xc = X - X.mean(0)
        direct = np.clip(np.linalg.eigvalsh(Xc.T @ Xc / n)[::-1], 0, None)[:min(n - 1, d)]
        np.testing.assert_allclose(ev, direct, rtol=1e-8, atol=1e-10)
        assert pr_from_eigs(ev) <= n - 1 + 1e-9


def test_iid_pr_matches_wishart_moment_formula():
    """For iid N(0,1) rows, PR ~ p d / (p + d + 1) with p = n - 1 (Wishart moments)."""
    from src.topic3_spectral.resampling import iid_reference
    for n, d in [(57, 1536), (25, 288), (57, 384)]:
        v = iid_reference(n, d, 200, seed=11)
        p = n - 1
        assert v.mean() == pytest.approx(p * d / (p + d + 1), abs=0.6)


def test_pr_raises_on_degenerate_input():
    with pytest.raises(ValueError):
        pr_cov(np.ones((10, 5)))
    with pytest.raises(ValueError):
        pr_cov(np.array([[np.nan, 1.0], [0.0, 1.0]]))
