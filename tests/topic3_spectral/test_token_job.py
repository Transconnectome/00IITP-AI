"""Token-level pipeline fixtures on synthetic frames with the real dump layout (small dims)."""
import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT  # noqa: F401
from src.topic3_spectral.estimators import corr_eigs, centered_eigs, layer3_tokens, layernorm0, pr_from_eigs
from src.topic3_spectral.token_job import pack_summaries, subject_summary

SHAPES = {"layer_0": (640, 12), "layer_1": (320, 24), "layer_2": (160, 48), "layer_3": (48, 2, 2, 2, 20)}


def _frame(rng, rank2=6, rank3=2):
    l2 = rng.standard_normal((160, rank2)) @ rng.standard_normal((rank2, 48)) + 0.1 * rng.standard_normal((160, 48))
    t3 = rng.standard_normal((160, rank3)) @ rng.standard_normal((rank3, 48)) + 0.1 * rng.standard_normal((160, 48))
    l3 = layernorm0(t3) * 2.0 + 0.5
    dump3 = l3.T.reshape(48, 20, 2, 2, 2).transpose(0, 2, 3, 4, 1)
    return {"layer_0": rng.standard_normal((640, 12)), "layer_1": rng.standard_normal((320, 24)),
            "layer_2": l2, "layer_3": dump3}


def test_subject_summary_matches_direct_computation_and_pooling_rule():
    rng = np.random.default_rng(0)
    frames = [_frame(rng) for _ in range(7)]
    s = subject_summary(frames, position=3, seed=1, expected_shapes=SHAPES)
    pooled_l3 = np.mean([f["layer_3"].mean(axis=(1, 2, 3, 4)) for f in frames], axis=0)   # VRABES rule
    np.testing.assert_allclose(s["pooled"]["L3"], pooled_l3, atol=1e-12)
    np.testing.assert_allclose(s["pooled"]["L0"], np.mean([f["layer_0"].mean(0) for f in frames], axis=0))
    cat = np.concatenate([layernorm0(f["layer_2"]) for f in frames])
    assert s["cat_corrpr"]["LN0L2"] == pytest.approx(pr_from_eigs(corr_eigs(cat)[0]), rel=1e-10)
    cat3 = np.concatenate([layer3_tokens(f["layer_3"]) for f in frames])
    assert s["cat_covpr"]["L3"] == pytest.approx(pr_from_eigs(centered_eigs(cat3)), rel=1e-10)
    assert s["sub_covpr"]["L0"].shape == (7,)


def test_planted_stage3_compression_is_seen_in_ln_matched_contrast():
    rng = np.random.default_rng(1)
    s = subject_summary([_frame(rng, rank2=8, rank3=2) for _ in range(7)], 0, 1, expected_shapes=SHAPES)
    assert s["cat_corrpr"]["L3"] < 0.5 * s["cat_corrpr"]["LN0L2"]


def test_wrong_frame_count_and_shape_halt():
    rng = np.random.default_rng(2)
    with pytest.raises(ValueError):
        subject_summary([_frame(rng) for _ in range(6)], 0, 1, expected_shapes=SHAPES)
    bad = _frame(rng)
    bad["layer_2"] = bad["layer_2"][:100]
    with pytest.raises(ValueError):
        subject_summary([bad] + [_frame(rng) for _ in range(6)], 0, 1, expected_shapes=SHAPES)


def test_pack_has_positions_and_no_identifier_keys():
    rng = np.random.default_rng(3)
    sums = [subject_summary([_frame(rng) for _ in range(7)], p, 1, expected_shapes=SHAPES) for p in (2, 0, 1)]
    arrs = pack_summaries(sums)
    np.testing.assert_array_equal(arrs["positions"], [0, 1, 2])
    assert "ids" not in arrs
    assert all(np.asarray(v).dtype.kind in "fiu" for v in arrs.values())
    assert arrs["cat_corr_eigs__L3"].shape[0] == 3
