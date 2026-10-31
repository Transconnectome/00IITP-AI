"""Topic 3 (layerwise participation ratio / spectral diagnostics) rerun package, 2026-10-31.

Modules: estimators (centered covariance/correlation PR, per-token LayerNorm, layer_3 reshape,
rank-slope and Clauset MLE decay exponents, jackknife), resampling (iid and column-permutation
references, paired m-out-of-n subsampling without replacement, sign-flip test, subject bootstrap,
Holm), io_contract (sha256-pinned npz loader returning X only, in-memory positional alignment,
restricted torch-free .pt reader), token_job (per-subject token-level spectra on frame dumps).
numpy only and Python 3.8 compatible so it runs on connectome system python.
"""
