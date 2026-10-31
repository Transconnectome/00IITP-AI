"""A2 ground-truth fixtures at the frozen primary density (PARAMS['density_primary']):
planted lagged 3-cycles detected / absent in control; AR(phi) mismatch calibrated;
spurious direction from shared-driver latency characterized (bias, NOT controlled)."""
import numpy as np

import tests.topic1_lagmotif.conftest_helpers  # noqa: F401
from src.topic1_lagmotif import synthetic
from src.topic1_lagmotif.pipeline import PARAMS
from src.topic1_lagmotif.spurious import run_scenario

D = PARAMS["density_primary"]
N, T = 60, 200


def test_planted_cycles_detected_and_absent_in_matched_control():
    inj = run_scenario(lambda r: synthetic.planted_cycles(T, N, 20, 0.8, r)[0], 8, D, 200, base_seed=101)
    ctl = run_scenario(lambda r: synthetic.planted_cycles(T, N, 20, 0.0, r)[0], 8, D, 200, base_seed=101)
    assert inj["n_degenerate_excluded"] == 0 and ctl["n_degenerate_excluded"] == 0
    assert inj["Z030C"]["mean"] > 4.0
    assert abs(ctl["Z030C"]["mean"]) < 1.0


def test_planted_cycles_per_seed_separation():
    zi, zc = [], []
    for s in range(6):
        from src.topic1_lagmotif.flow import lagged_net_flow, oriented_topk_graph
        from src.topic1_lagmotif.motifs import motif_statistics
        from src.topic1_lagmotif.preprocess import preprocess
        for g, sink in ((0.8, zi), (0.0, zc)):
            X, cyc = synthetic.planted_cycles(T, N, 20, g, np.random.default_rng([55, s]))
            A = oriented_topk_graph(lagged_net_flow(preprocess(X, 2.0), 1), D)
            if g > 0:  # most planted cycle edges are recovered with the right orientation
                hit = sum(A[a, b] + A[b, c] + A[c, a] for a, b, c in cyc)
                assert hit >= 0.8 * 3 * len(cyc)
            sink.append(motif_statistics(A, 200, 20, 0.2, np.arange(200) + 1000 * s)["Z"]["030C"])
    assert min(zi) > max(zc) + 1.0


def test_autocorrelation_mismatch_is_calibrated_by_oriented_degree_preserving_null():
    """Independent AR(1) ROIs, phi ~ U(0.1, 0.9): no coupling.  Mean Z over 16 seeds must be
    within 3*1.5/sqrt(16) = 1.125 of 0 (overdispersed per-subject Z; never a per-seed 1.96 cut).
    The v1 null (reciprocal edges allowed) gave +2.47 here (survey probe)."""
    r = run_scenario(lambda rng: synthetic.ar1(T, rng.uniform(0.1, 0.9, N), rng), 16, D, 200, base_seed=303)
    tol = 3 * 1.5 / np.sqrt(16)
    assert r["n_degenerate_excluded"] == 0
    assert abs(r["Z030C"]["mean"]) < tol
    assert abs(r["Z030T"]["mean"]) < tol


def test_shared_driver_latency_produces_spurious_direction_bias_characterization():
    """Characterization, not a control: no neural coupling, per-ROI latency sd 1 s.  The oriented
    null does NOT remove this; the magnitude is reported in results/topic1/2026-10-30/
    spurious_direction.json and OPEN_ISSUES.  If this ever passes as 'unbiased', revisit the claim."""
    r = run_scenario(lambda rng: synthetic.shared_driver_latency(400.0, N, 2.0, 1.0, 1.0, rng), 8, D, 200,
                     base_seed=404)
    assert r["gradient_share"]["mean"] > 0.5
    assert r["Z030T"]["mean"] < -2.0
    assert r["E2"]["mean"] > 2.0
