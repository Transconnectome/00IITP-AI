"""Per-subject token-level spectra for SwiFT ver11 E192 frame dumps (numpy only, Python 3.8).

One subject = 7 frame dumps; each frame is a dict with
  layer_0 (10240, 384), layer_1 (1280, 768), layer_2 (160, 1536), layer_3 (1536, 2, 2, 2, 20).
Variants analysed: L0, L1, L2, LN0L2 (parameter-free per-token LayerNorm of layer_2 tokens),
L3 (post-final-LayerNorm tokens). Primary unit: the subject (7 frames concatenated).

Outputs are keyed by subject POSITION only (sorted directory order); no names.
"""
import numpy as np

from .estimators import (centered_eigs, corr_eigs, layer3_tokens, layernorm0,
                         pr_from_eigs)

VARIANTS = ("L0", "L1", "L2", "LN0L2", "L3")
SUBSAMPLE_TOKENS = 160          # H4: common token count per frame for the L0->L3 profile
EXPECTED_FRAMES = 7
EXPECTED_SHAPES = {"layer_0": (10240, 384), "layer_1": (1280, 768), "layer_2": (160, 1536),
                   "layer_3": (1536, 2, 2, 2, 20)}


def frame_tokens(frame, expected_shapes=EXPECTED_SHAPES):
    """dict of float64 token matrices per variant for one frame; raises on schema violation."""
    for k in ("layer_0", "layer_1", "layer_2", "layer_3"):
        if k not in frame:
            raise KeyError("frame lacks %s" % k)
        if expected_shapes is not None and tuple(frame[k].shape) != tuple(expected_shapes[k]):
            raise ValueError("unexpected shape for %s: %s" % (k, tuple(frame[k].shape)))
    L2 = np.asarray(frame["layer_2"], dtype=np.float64)
    toks = {
        "L0": np.asarray(frame["layer_0"], dtype=np.float64),
        "L1": np.asarray(frame["layer_1"], dtype=np.float64),
        "L2": L2,
        "LN0L2": layernorm0(L2),
        "L3": layer3_tokens(np.asarray(frame["layer_3"], dtype=np.float64)),
    }
    for v, X in toks.items():
        if not np.all(np.isfinite(X)):
            raise ValueError("non-finite tokens in %s" % v)
    return toks


def pooled_vector(frame, variant_tokens):
    """Pooling exactly as VRABES pool_E192_layersweep.py: token mean for layers 0-2,
    mean over (D, H, W, T) for layer_3 (identical to the token mean of the reshaped tokens)."""
    return variant_tokens.mean(axis=0)


def subject_summary(frames, position, seed, expected_frames=EXPECTED_FRAMES,
                    expected_shapes=EXPECTED_SHAPES, subsample_tokens=SUBSAMPLE_TOKENS):
    """Compute per-frame and concatenated spectra for one subject.

    Returns dict:
      pooled[v]            (D,) mean over frames of the per-frame token means
      frame_covpr[v]       (n_frames,) per-frame centered covariance PR
      frame_corrpr[v]      (n_frames,)
      sub_covpr[v], sub_corrpr[v]  (n_frames,) PR after subsampling `subsample_tokens` tokens
                                   per frame without replacement (seeded per position/frame)
      cat_cov_eigs[v], cat_corr_eigs[v]  eigenvalues on the 7 frames concatenated
      cat_covpr[v], cat_corrpr[v], cat_corr_dropped[v]
    """
    if len(frames) != expected_frames:
        raise ValueError("expected %d frames, got %d" % (expected_frames, len(frames)))
    out = {"position": int(position), "pooled": {}, "frame_covpr": {}, "frame_corrpr": {},
           "sub_covpr": {}, "sub_corrpr": {}, "cat_cov_eigs": {}, "cat_corr_eigs": {},
           "cat_covpr": {}, "cat_corrpr": {}, "cat_corr_dropped": {}}
    per_frame = {v: [] for v in VARIANTS}
    pooled = {v: [] for v in VARIANTS}
    fcov = {v: [] for v in VARIANTS}
    fcor = {v: [] for v in VARIANTS}
    scov = {v: [] for v in VARIANTS}
    scor = {v: [] for v in VARIANTS}
    for fi, frame in enumerate(frames):
        toks = frame_tokens(frame, expected_shapes)
        rng = np.random.default_rng([int(seed), int(position), int(fi)])
        for v in VARIANTS:
            X = toks[v]
            per_frame[v].append(X)
            pooled[v].append(pooled_vector(frame, X))
            fcov[v].append(pr_from_eigs(centered_eigs(X)))
            fcor[v].append(pr_from_eigs(corr_eigs(X)[0]))
            if X.shape[0] > subsample_tokens:
                Xs = X[np.sort(rng.choice(X.shape[0], subsample_tokens, replace=False))]
            else:
                Xs = X
            scov[v].append(pr_from_eigs(centered_eigs(Xs)))
            scor[v].append(pr_from_eigs(corr_eigs(Xs)[0]))
    for v in VARIANTS:
        out["pooled"][v] = np.mean(np.stack(pooled[v]), axis=0)
        out["frame_covpr"][v] = np.asarray(fcov[v])
        out["frame_corrpr"][v] = np.asarray(fcor[v])
        out["sub_covpr"][v] = np.asarray(scov[v])
        out["sub_corrpr"][v] = np.asarray(scor[v])
        Xcat = np.concatenate(per_frame[v], axis=0)
        ce = centered_eigs(Xcat)
        re_, nd = corr_eigs(Xcat)
        out["cat_cov_eigs"][v] = ce
        out["cat_corr_eigs"][v] = re_
        out["cat_covpr"][v] = pr_from_eigs(ce)
        out["cat_corrpr"][v] = pr_from_eigs(re_)
        out["cat_corr_dropped"][v] = int(nd)
        per_frame[v] = None
    return out


def pack_summaries(summaries, variants=VARIANTS):
    """Stack per-subject summaries (sorted by position) into flat arrays for np.savez."""
    summaries = sorted(summaries, key=lambda s: s["position"])
    arrs = {"positions": np.array([s["position"] for s in summaries], dtype=np.int64)}
    for v in variants:
        arrs["pooled__" + v] = np.stack([s["pooled"][v] for s in summaries]).astype(np.float64)
        for key in ("frame_covpr", "frame_corrpr", "sub_covpr", "sub_corrpr"):
            arrs[key + "__" + v] = np.stack([s[key][v] for s in summaries])
        for key in ("cat_covpr", "cat_corrpr", "cat_corr_dropped"):
            arrs[key + "__" + v] = np.array([s[key][v] for s in summaries])
        for key in ("cat_cov_eigs", "cat_corr_eigs"):
            arrs[key + "__" + v] = np.stack([s[key][v] for s in summaries]).astype(np.float32)
    return arrs
