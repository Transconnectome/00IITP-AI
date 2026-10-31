# Topic 3 provenance and the PR≈1 diagnosis (T3.1), 2026-10-31

Evidence file: `results/topic3/2026-10-31/t3_1_provenance_repro.json`, written by `scripts/topic3_provenance_repro.py`.

This file reproduces numbers that were already published. It is not a new result (C8).

## 1. Inputs

All seven pooled matrices are read in place from `/home/juke/git/VRABES/RemissionAnalysis/`, which is read-only. The sha256 values are verified on every load, and the full pins are in `src/topic3_spectral/io_contract.py`.

Every file has the keys `['X', 'ids']`. X is float32, has no constant columns and no non-finite values.

| Name | File | Shape | Producer | Pooling |
|---|---|---|---|---|
| L0–L3 | `pooled_E192_layers/layer_{0..3}.npz` | 57×384 / 768 / 1536 / 1536 | `pool_E192_layersweep.py` (sha 0e408552…). It ran at NERSC on the frame dumps of checkpoint `NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4`. Frames came from `extract_vrabes_swift_E192.sh` (sha b979a682…) with ver11. | Layers 0–2: token mean per frame. Layer 3: mean over (D,H,W,T). Then the mean over 7 frames. |
| BrainLM | `pooled_brainlm_matrix.npz` | 57×768 | `extract_brainlm_embeddings.py` (sha 67348ff1…) | CLS token (`last_hidden_state[:,0,:]`) |
| BrainJEPA | `pooled_brainjepa_matrix.npz` | 57×768 | `extract_brainjepa_embeddings.py` (sha 832c74cf…) | Token mean |
| NeuroSTORM | `pooled_neurostorm_matrix.npz` | 25×288 | `extract_neurostorm_embeddings.py` (sha a028716b…) | Global average pool, then the mean over segments |

**Row order.** All six 57-row files share one row order. The 25 NeuroSTORM rows are an exact subset of it, at increasing positions. The check was done in memory and its output is positions only.

**Connectome copies.** `/storage/bigdata/VRABES/05_pooled_embedding/` holds copies of the SwiFT layer files. The token job re-verifies those copies against the same pins before using them.

**Frame dumps.** These are on connectome only, under `/storage/bigdata/VRABES/04_embedding/`:
- primary checkpoint `swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES`: 57 subjects × 7 frames;
- three complete zoo E192 checkpoints with the same subject set: `swift_zoo_ses-01/{HCP_N400_T2400_E192, NewUAH_deepE192_L1e-4, NewUAH_deepE192_L5e-5}`.

## 2. Architecture facts used by the card

Source: `/home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py`, sha de132387…052a, read-only.

**Stages 0–2 end in a merge.** `BasicLayer.forward` (lines 914–923) runs the blocks and then `downsample` (`PatchMergingV2`). Line 1068 sets `downsample=… if (i_layer < self.num_layers - 1) else None`, so the last stage has no merge.

**The merge itself.** `PatchMergingV2` (lines 41–86) is `reduction(norm(x))`, a pre-norm LayerNorm(8C) followed by Linear. Its default `use_post_norm=False`. So the layer_0–2 dumps are raw Linear outputs.

**The dump hook.** `_forward_hook_embedding` (lines 1382–1412) applies the final `self.norm` only after the last stage. It then reshapes `view(b,c,t,d,h,w).permute(0,1,3,4,5,2)` to (C,D,H,W,T). `self.norm` is `norm_layer(encoder_out_dim)`, and `norm_layer` defaults to `nn.LayerNorm` with eps 1e-5.

**Consequence.** No PatchMerging sits between `layer_2` and `layer_3`. Both are 1536-d on the same 2³×20 grid of 160 tokens. layer_3 is layer_2 after the 2 stage-3 Swin blocks plus the final LayerNorm.

**Caveat.** The NERSC fork used for extraction (SwiFT_v2_perlmutter) was not diffed against this local ver11. The token job's re-pool check (card §2) is what ties the dumps to the npz.

## 3. Why the json says PR≈1 while the report says 2.8–12.5

Reproduction to 4 decimals, from `t3_1_provenance_repro.json`:

| Input | Report PR (centered; `empirical_connectome_ablation.estimate_powerlaw_alpha`) | Report old α | json PR (uncentered; `spectral_rg_flow_diagnostic.compute_participation_ratio`) | json α (uncentered HTSR fit) | Mean-vector energy fraction |
|---|---|---|---|---|---|
| L0 | 2.7773 ✓ | 1.4717 ✓ | 1.0014 ✓ | 1.4656 ✓ | 0.9992 |
| L1 | 2.7782 ✓ | 0.9887 ✓ | 1.0050 ✓ | 1.2551 ✓ | 0.9973 |
| L2 | 11.0202 ✓ | 1.5980 ✓ | 1.0743 ✓ | 1.4074 ✓ | 0.9645 |
| L3 | 3.5786 ✓ | 1.8411 ✓ | 1.0327 ✓ | 1.9928 ✓ | 0.9832 |
| BrainLM | 4.3188 ✓ | 1.4580 ✓ | 1.0028 ✓ | 1.6910 ✓ | 0.9985 |
| BrainJEPA | 11.7851 ✓ | 1.8807 ✓ | 1.0581 ✓ | 1.5000 ✓ | 0.9721 |
| NeuroSTORM | 12.5070 ✓ | 1.1960 ✓ | 1.0102 ✓ | 0.8856 ✓ | 0.9948 |

✓ means the value recomputed by the protected old function equals the published number to 4 decimals.

**Diagnosis.** `compute_participation_ratio` (`src/spectral_rg_flow_diagnostic.py:55-64`) takes the SVD of the uncentered X. The column-mean vector carries 96–99.9% of the second moment, so the first singular value dominates and PR → 1. This is an estimator defect, not a property of the representations.

`estimate_powerlaw_alpha` (`src/empirical_connectome_ablation.py:143-159`) centers the data first and gives the report's values.

**Fixture.** `tests/topic3_spectral/test_centering_fixture.py` builds a rank-k matrix plus a 30-SD row offset for k ∈ {1, 5, 20, 56}. It checks four things:
- the new centered PR equals k to 1e-9;
- the old centered function also gives k;
- the old uncentered function returns < 1.1;
- the mean-energy fraction exceeds 0.95.

**The silent fallback is not reused.** The protected `spectral_rg_flow_diagnostic.py:229-243` silently substitutes random data for a missing file. That cannot be edited, because of C1. The new loader instead raises on a missing file or a hash mismatch, and `tests/topic3_spectral/test_io_contract.py` covers this.
