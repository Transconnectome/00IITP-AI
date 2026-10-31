"""T1.1 (run tw-20261031-four-topics): return contract of pipeline.extract_subject, the cohort entry point.

PROPOSAL by explorer_M1_r1_2 (probe file, not installed). Closes the five victory-audit survivors:
roi_subsample_80, extract_subject_drops_valid_T, curl_returns_F, seeds_ignore_position, sp_not_normalised.

Oracles are written from the frozen card text (sections 1 and 11) with numpy only:
  * k = round(density * N(N-1)/2) with N = 304          (card section 1, "Graph")
  * valid_T = raw_valid_T - ceil(40 s / TR)              (card section 1, "Valid portion")
  * curl = F - G, G[i,j] = p_i - p_j, p = row mean of F  (card section 1, "Channels" / "Per-subject covariate")
  * seeds = SeedSequence([20261030, position, channel_code, round(1000*d)]).generate_state(n, uint32)  (card 11)
  * SP = Z / ||Z|| over the 5 classes                     (card section 1, "Z / SP")
The null itself (motif_statistics) is production code; only its seed input is replaced by the oracle.
"""
import math

import numpy as np
import pytest

import tests.topic1_lagmotif.conftest_helpers  # noqa: F401
from src.topic1_lagmotif.data import prepare_series
from src.topic1_lagmotif.flow import oriented_topk_graph
from src.topic1_lagmotif.motifs import census, motif_statistics
from src.topic1_lagmotif.pipeline import PARAMS, extract_subject, subject_flow

N_ROI = 304
TR = 0.8                      # n_trim = ceil(40/0.8) = 50 > 0, resampling ratio 2/5 (not identity)
T_NATIVE = 400                # 320 s
N_PAD = 37                    # trailing zero rows (padding) -> raw_valid_T != array length
N_NULL = 12                   # small, for speed; the contract does not depend on n_null
AF = 2.0                      # small attempts factor, for speed
CARD_K = {0.05: 2303, 0.10: 4606, 0.15: 6908}
CLASSES = ("021D", "021U", "021C", "030T", "030C")
CH_CODE = {"broadband": 0, "curl": 1}


def _raw_series(seed=5):
    """Shared slow driver with a per-ROI latency (large gradient share) plus independent noise, raw scale,
    then N_PAD trailing zero rows."""
    rng = np.random.default_rng(seed)
    fine = 0.1
    n_fine = int((T_NATIVE * TR + 60) / fine)
    drv = np.convolve(rng.standard_normal(n_fine), np.ones(60) / 60.0, mode="same")
    lat = rng.uniform(0.0, 4.0, N_ROI)
    t = np.arange(T_NATIVE) * TR + 30.0
    X = np.stack([np.interp(t - L, np.arange(n_fine) * fine, drv) for L in lat], axis=1)
    X = 1.15e4 + 40.0 * (X / X.std() + 0.7 * rng.standard_normal(X.shape))
    return np.vstack([X, np.zeros((N_PAD, N_ROI))])


def _series(position):
    return prepare_series(_raw_series(), TR, PARAMS["head_trim_s"], position=position, site="Dresden")


def _oracle_curl(F):
    p = F.mean(axis=1)
    G = p[:, None] - p[None, :]
    np.fill_diagonal(G, 0.0)
    return F - G


def _oracle_seeds(position, channel, d, n):
    ss = np.random.SeedSequence([20261030, int(position), CH_CODE[channel], int(round(d * 1000))])
    return ss.generate_state(n, dtype=np.uint32).astype(np.int64)


@pytest.fixture(scope="module")
def feats7():
    return extract_subject(_series(7), n_null=N_NULL, attempts_factor=AF)


@pytest.fixture(scope="module")
def flow7():
    return subject_flow(_series(7))


def test_all_304_rois_reach_the_graph(feats7, flow7):
    assert flow7.shape == (N_ROI, N_ROI)
    for d, k in CARD_K.items():
        for ch in ("broadband", "curl"):
            r = feats7["results"][f"{ch}@{d:.2f}"]
            assert r["m"] == k, (ch, d, r["m"])
            assert sum(r["observed"].values()) > 0
    obs = feats7["results"]["broadband@0.10"]["observed"]
    assert obs == census(oriented_topk_graph(flow7, 0.10))


def test_reported_valid_T_is_after_head_trim(feats7):
    n_trim = math.ceil(40.0 / TR)
    assert feats7["raw_valid_T"] == T_NATIVE                 # padding stripped
    assert feats7["n_trim"] == n_trim == 50
    assert feats7["valid_T"] == T_NATIVE - n_trim == feats7["raw_valid_T"] - feats7["n_trim"]
    assert feats7["duration_s"] == pytest.approx((T_NATIVE - n_trim) * TR, abs=1e-9)
    assert feats7["position"] == 7 and feats7["tr"] == TR


def test_curl_channel_is_F_minus_its_gradient_part(feats7, flow7):
    assert feats7["gradient_share"] > 0.2                    # fixture has a real gradient part
    Fc = _oracle_curl(flow7)
    for d in CARD_K:
        A = oriented_topk_graph(Fc, d)
        got = feats7["results"][f"curl@{d:.2f}"]
        assert got["observed"] == census(A), d
        ref = motif_statistics(A, N_NULL, AF, PARAMS["p_rot"], _oracle_seeds(7, "curl", d, N_NULL))
        assert got["null_mean"] == ref["null_mean"], d
    assert (feats7["results"]["curl@0.10"]["observed"]
            != feats7["results"]["broadband@0.10"]["observed"])


def test_null_seeds_follow_card_rule_with_position(feats7, flow7):
    for ch in ("broadband", "curl"):
        Fx = flow7 if ch == "broadband" else _oracle_curl(flow7)
        for d in CARD_K:
            A = oriented_topk_graph(Fx, d)
            ref = motif_statistics(A, N_NULL, AF, PARAMS["p_rot"], _oracle_seeds(7, ch, d, N_NULL))
            got = feats7["results"][f"{ch}@{d:.2f}"]
            assert got["null_mean"] == ref["null_mean"], (ch, d)
            assert got["null_sd"] == ref["null_sd"], (ch, d)
    other = extract_subject(_series(8), channels=["broadband"], densities=[0.10], n_null=N_NULL,
                            attempts_factor=AF)["results"]["broadband@0.10"]
    same = feats7["results"]["broadband@0.10"]
    assert other["observed"] == same["observed"]                 # same series, same graph
    assert other["null_mean"] != same["null_mean"]               # different position -> different null


def test_sp_is_unit_norm_z_over_the_five_classes(feats7):
    for key, r in feats7["results"].items():
        z = np.array([r["Z"][k] for k in CLASSES], dtype=float)
        sp = np.array([r["SP"][k] for k in CLASSES], dtype=float)
        fin = np.isfinite(z)
        assert fin.any(), key
        assert np.array_equal(np.isfinite(sp), fin), key
        assert np.sum(sp[fin] ** 2) == pytest.approx(1.0, rel=1e-12), key
        assert np.allclose(sp[fin], z[fin] / np.sqrt(np.sum(z[fin] ** 2)), rtol=1e-12, atol=0), key
        assert r["E1_Z030C"] == r["Z"]["030C"] or (np.isnan(r["E1_Z030C"]) and np.isnan(r["Z"]["030C"]))
