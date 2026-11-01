# Topic 2 — T2.1: where SwiFT ver11 actually merges space (from code)

Date: 2026-11-01. Author: worker_M3_r1 (run tw-20261031-four-topics, milestone M3). Mode: documentation of code; no data.

**Source.** `simmim_swin4d_transformer_ver11.py` in SwiFT_v2, commit f0dc7aca (HEAD), last changed in 6061dc6d.
Its sha256 is `de132387f64d98cbe9b15876351a7b33f9bec112df3df8f4718327d06e95052a`, and `git diff` is clean.
A byte-identical copy is in `src/topic2_rgpool/vendor_swift_ver11/`; `SOURCE.md` there records the provenance.
The line numbers below refer to that file.
The claims are pinned by tests: `tests/topic2_rgpool/test_model_pairing.py` and `test_merge.py`.

## 1. The broken premise

The old Topic 2 text (`EMPIRICAL_ANALYSIS_REPORT.md` lines 81 and 120) says this:
> "Euclidean PatchMerging between Layer 2 → 3 collapses PR 11.02 → 3.58."

The premise is false. The code has **no merge between `layer_2` and `layer_3`**.
- Line 1068 passes `downsample=down_sample_mod if (i_layer < self.num_layers - 1) else None`. Only stages 0, 1 and 2 end with a merge.
- `RoPE4DBasicLayer.forward` (lines 914–923) runs the blocks first and then `self.downsample` (line 922).
- The hook `_forward_hook_embedding` (lines 1382–1412) therefore labels its outputs as follows:
  - `layer_0`, `layer_1` and `layer_2` are the outputs *after* merges M0, M1 and M2.
  - `layer_3` is `layer_2` passed through the stage-3 blocks and the final LayerNorm (line 1327).
- In the E192 checkpoints, `layer_2` and `layer_3` are both 1536-d on the same 2³×20 grid.

Topic 3 reached the same conclusion: `docs/03_empirical_analysis/topic3/2026-10-31_topic3_provenance.md` §"Consequence" and result report R2.

The old "analysis 2" Euclidean arm is something else again. It sliced contiguous ROI indices of an ENIGMA 304-ROI series and was not SwiFT's merge. C8 bars citing its numbers.

## 2. What is true: three 2×2×2 spatial merges, never in time

`PatchMergingV2` (lines 41–88):
- It reshapes the tokens to (B, t, d, h, w, C).
- It concatenates the 8 children `x[:, :, i::2, j::2, k::2]` in slot order `(i, j, k) ∈ product(range(2), repeat=3)` (line 81), giving 8C channels.
- It applies `reduction(norm(x))` (line 85): LayerNorm(8C), then `Linear(8C → 2C, bias=False)` (line 72).
- Time is never merged. The comment says so, and `t_out = t_in` in every stage.

Construction (lines 1036–1076):
- Stage *i* has input resolution `(T_p, D_p/2^i, H_p/2^i, W_p/2^i)` (lines 1042–1048) and width `embed_dim·2^i` (line 1049).
- A non-string `downsample` is used as given (line 1036) and called as `downsample(input_resolution, dim, norm_layer, use_post_norm)` (line 904). This is the hook Topic 2 uses (§4).

Stage table. It covers the pilot config E36 (embed 36, depths 2,2,6,2, heads 3,6,12,24, window (4,4,4,10), patch (6,6,6,1), input 96³×20) and the E192 configs behind the old dumps (embed 192):

| stage | input grid (T × D×H×W), cell size | width (E36 / E192) | windows in this stage (lines 853–871) | merge at stage end | output (hook name) |
|---|---|---|---|---|---|
| 0 | 20 × 16³, 12 mm cells (6³ voxels of 2 mm) | 36 / 192 | spatial 4³; shift (2,2,2) on odd blocks; temporal 10, shift 5 on odd blocks | **M0: 16³→8³ (12→24 mm)**, Linear 288→72 / 1536→384 | 20×8³, 72 / 384 (`layer_0`) |
| 1 | 20 × 8³, 24 mm | 72 / 384 | spatial 4³: unshifted windows = the 8 octants; shifted blocks cross octants | **M1: 8³→4³ (24→48 mm)**, Linear 576→144 | 20×4³, 144 / 768 (`layer_1`) |
| 2 | 20 × 4³, 48 mm | 144 / 768 | window 4³ = whole grid; no shift, because `min(res) <= window` (line 868) | **M2: 4³→2³ (48→96 mm)**, Linear 1152→288 | 20×2³, 288 / 1536 (`layer_2`) |
| 3 | 20 × 2³, 96 mm | 288 / 1536 | window 2³ = whole grid, no shift | **none** (line 1068) | 2³×20, 288 / 1536 after the final LayerNorm (`layer_3`) |

`test_pilot_config_stage_table_and_bit_identity` asserts the E36 input resolutions, merge Linear shapes, missing stage-3 merge, hook shapes and total parameter count (38,712,096).

## 3. Decoder locality: each final token reconstructs only its own octant

- `decoder_type` is hard-coded to `'mlp'` (line 1112); the `'linear'` branch (lines 1113–1116) is dead code.
- The `'mlp'` decoder (lines 1118–1148, `forward_decoder` lines 1337–1360) applies to every final token separately:
  - a temporal MLP, then `Linear(8E → 8E·1)` (temporal multiplier 20/20 = 1, line 1121);
  - a spatial MLP, then `Linear(8E → 48³)` (lines 1136–1147);
  - `PixelShuffle4D(48)` (lines 91–123, line 1148).
- So every voxel of a 48³ octant at frame t is decoded from that octant's one final token at frame t.
  - `test_decoder_reconstructs_each_octant_from_its_own_final_token` confirms this: perturbing one token changes voxels only inside its own octant and frame.
  - In E36, `decoder_spatial_expand` holds 31.96 M of the 38.71 M parameters.

## 4. Where regrouping can matter, and the consequence for the redesign

**Insert at M0 only.**
- M0 is the only merge with room to regroup, because its 16³ grid of 12 mm cells holds about 10³ in-brain cells.
- Explorer measurements, used as geometry facts rather than results:
  - On a 5-subject development mask, explorer_M3_r1_1 found 235/512 brain-touching M0 blocks and 1,189 signal cells.
  - On the FSL MNI mask, explorer_M3_r1_2 found 85 fully in-brain parents at 16³→8³ but only 8 at 8³→4³. M2 has 8 outputs in total.
- The training-split counts for the pilot are recorded in `results/topic2/2026-11-01/partitions/partitions_hcp.json`.

**Boxes must stay inside one octant.**
- After M0, the unshifted stage-1 windows, merges M1/M2 and the decoder are all organised by octant.
- A box that crosses octants would be penalised for reasons unrelated to connectivity.

**The token grid must stay regular.**
- Stages 1–3 assume a regular grid: windowed attention, RoPE positions, and the `L == T·D·H·W` assert at line 717.
- So a pooling with a variable number of output boxes cannot be dropped in. The old `src/rg_box_pooling.py` `ConnectomeRGPooling` (mean + Linear, 76 boxes) is such a pooling, and it is also not parameter-matched.

**Redesign.**
- At M0, a **parameter-free per-frame gather π** reorders the 16³ cells so that each 2×2×2 block of the reordered grid is one connectome box. The unchanged `PatchMergingV2` then merges those blocks.
- With π = identity the module is `PatchMergingV2` exactly (bit-identical; test `test_identity_perm_is_bit_exact_patchmergingv2`).
- Parameters, tokens and FLOPs are equal by construction (`test_no_extra_parameters_and_equal_flops`).

## 5. Other code facts

- `use_post_norm=True` crashes. Line 73 builds `LayerNorm(2C)`, but line 85 applies it to the 8C concatenation (`test_use_post_norm_true_crashes_in_ver11`). The pilot freezes `use_post_norm=False`, the ver11 default.
- SwiFT's SimMIM defaults are `mask_ratio 0.6` and `mask_patch_size 6,6,6,2` (`project/module/pl_classifier.py` lines 1082–1083). With 6³×1 patches, one mask unit is 1 cell × 2 frames.
- The SwiFT HCP recipe:
  - crops `[7:85, 7:103, 0:84]` (`preprocessing_HCP_v2.py` line 22);
  - pads (x 10/8, y 0/0, z 3/9) to 96³ (`datasets.py`, S1200 `__getitem__`);
  - takes the brain mask as temporal mean > 0.
- Not inspected: the perlmutter fork that produced older VRABES dumps. The statements above are about ver11 at f0dc7aca only.
