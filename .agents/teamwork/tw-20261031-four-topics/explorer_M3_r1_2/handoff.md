# Handoff — explorer_M3_r1_2 (M3 / Topic 2, explorer 2 of 2, lens: feasibility and failure modes)
Written 2026-11-01T01:35Z. Type: Hard (explorer analysis report). No production code was written. Probe code is in /home/juke/git/00IITP-AI/verification/explorer_M3_r1_2/. B300 GPU use: 0.134 GPU-h, logged in results/gpu_ledger_2026-10-31.md (I created the file). No real-data values were read: on HCP I read one NIfTI header and listed files.

**Summary.** Testing M3 within the cap is feasible. The pilot should run on HCP-YA REST1 on B300 .98, but it needs one PI gate first: is HCP Open Access "public" under C6? If not, use ds000228 (PDDL) as the fallback.

- **Insertion point.** The only usable merge is 16³→8³ (stage-0 PatchMergingV2). There, 85 parent cells (680 tokens) are fully in brain. The 8³→4³ merge has only 8 such cells.
- **Operator.** A parameter-free spatial permutation in front of the unchanged PatchMergingV2 gives exactly matched parameters and FLOPs. On B300 it costs +0.2–0.6% step time. With the Euclidean partition it reduces bitwise to PatchMergingV2, and 5 of 5 targeted mutants are caught.
- **Null partition.** A fully random box partition is the wrong control: it moves tokens 2.5× further than connectome boxes. A rotation null is locality-matched, provided the rotated tokens are reassigned one-to-one with Hungarian matching (21.2 mm vs 20.2 mm).
  - My first null used a nearest-neighbour snap. That was not a bijection: only 461–505 of 680 tokens were hit. Its numbers are kept as `*_v1_nnsnap.*` and superseded.
- **Measurement capacity.** At a tiny budget, held-out masked NMSE does detect a planted scattered-network partition effect (A2 0.927 vs rotation null 0.996 vs Euclidean 1.001). It also shows Euclidean winning on smooth fields. This was 1 seed, 1200 steps, and A3 there used the old snapped null.
- **Expected effect is small.** With realistic atlas geometry, the expected operator-level advantage is +0.003 to +0.021 retention. "Inconclusive" is therefore a likely outcome.
- **Seeds drive power.** Inference must treat the seed as the primary unit (hierarchical bootstrap). 5 seeds is the default.
- **Cost.** Measured cost is about 1 GPU-h per e24 run at B=32 for 20k steps. The capacity gate must run at the same step budget as the real test. The full design (gate plus real, 5 seeds, 20k steps) is ≈45–50 GPU-h, under the 64 GPU-h cap but tight. The cheaper matched option at 10k steps is ≈25 GPU-h.

---

## 1. Observation

### O-A. Architecture from running code (T2.1)
Source: `/home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py`, sha256 `de132387…052a`, SwiFT_v2 commit f0dc7aca, copied read-only into `verification/explorer_M3_r1_2/swift_ver11_copy/` (SOURCE_SHA256.txt). Probe `probe_t21_t22_wrapper.py` → `.out.json`.

| Item | Evidence |
|---|---|
| PatchMergingV2 concatenates the 8 spatial children `x[:, :, i::2, j::2, k::2, :]` (time untouched) → LayerNorm(8C) → Linear(8C→2C, bias=False) | ver11.py:41-88 (`:70` "Skip dimension reduction on the temporal dimension", `:72` reduction, `:80-83` gather, `:81` slicing) |
| The merge is the last op of RoPE4DBasicLayer.forward, at the end of stages 0, 1 and 2. Stage 3 has `downsample=None` | ver11.py:914-923, :1066-1068 |
| Running-code stage table (96³×20 input, patch 6,6,6,1, window 4,4,4,10): stage 0 = 20×16³ tokens, dim C, 4³ windows, shift 2 → merge to 8³. Stage 1 = 20×8³, 2C, 4³ windows, shift 2 → merge to 4³. Stage 2 = 20×4³, 4C, window covers the whole grid (global spatial attention, no shift) → merge to 2³. Stage 3 = 20×2³, 8C, global, no merge, then final LayerNorm. Temporal window 10, shift 5, at every stage | `.out.json` → `A_tiny_config.stages`, `A_E192_config.stages` |
| Hook outputs are POST-merge: layer_0 (1, 10240, 2C), layer_1 (1, 1280, 4C), layer_2 (1, 160, 8C) (after the 4³→2³ merge, no LayerNorm), layer_3 (8C, 2, 2, 2, 20) (2 blocks + final LayerNorm) | `A_tiny_hook_shapes`; ver11.py:1382-1412 |
| E192 VRABES config (embed 192, depths 2,2,18,2): merge parameters are 592,896 / 2,365,440 / 9,449,472. Total model 474,226,176 parameters. Decoder spatial expansion multiplier is 48 | `A_E192_config` |
| SimMIM MLP decoder: each final 2³ token is linearly expanded into its own 48³-voxel octant, so reconstruction is spatially anchored | ver11.py:1111-1148, 1337-1360 |
| PatchMergingV2 is byte-identical across the 4 local ver11 variants: SwiFT_v2/SwiFT-7T/SwiFT-LLM `de132387`, SwiFT-LLM-b300-* `f127858e`, master-unified/cobre `24ef251f`, nipa `5bc44469`. They differ only in the `use_post_norm` argument and a hard-coded decoder `2**3` | diff in this session |
| Old premise text that is false in code: EMPIRICAL_ANALYSIS_REPORT.md:81 ("Layer 3에서 Euclidean PatchMerging이 한 번 더 적용", i.e. "PatchMerging is applied once more at Layer 3") and :120 ("Layer 2→3 유클리드 PatchMerging", i.e. "Euclidean PatchMerging at Layer 2→3"). Analysis 2 (:47-59) calls ROI-index slicing on ENIGMA 304 ROIs "SwiFT식 Euclidean PatchMerging" ("SwiFT-style Euclidean PatchMerging") (`src/rg_box_pooling.py:368-372`, per survey_2 O2.5) | grep in this session; numbers there are not cited (C8) |

### O-B. Parameter-free permutation wrapper (T2.2 operator)
`BoxPermutedMerge` gathers stage-0 tokens per frame with a fixed spatial permutation, then calls the unchanged PatchMergingV2 (`probe_t21_t22_wrapper.py`).

| Check | Result |
|---|---|
| T0 Euclidean boxes → perm == arange | true |
| T1 identity wrapper is bitwise equal to PatchMergingV2 | true |
| T2 parameter count equal | true |
| T3 each parent's output == Linear(LN(concat of its box's 8 members in slot order)) (64 boxes, atol 1e-5) | true |
| T4 perturbing frame t changes output only at frame t | true |
| T5 every merge parameter and every input token gets a nonzero gradient | true |
| T6 perm is a bijection | true |
| T7 RG perm ≠ identity (guards against a silent fallback) | true |
| Mutants: identity (T3, T7 fail), time_mixing (T3, T4, T5 fail), inverse (T3 fails), post_merge (T3, T5 fail), drop_token (T5, T6 fail) | 5/5 caught |
| Tiny full SimMIM model, wrapper at stage 0 | params 11,337,696 vs 11,337,696; fwd+bwd FLOPs 17,984,471,040 vs 17,984,471,040; output shape (1,1,96,96,96,20) in both; backward OK |

### O-C. Token map with the public atlas (no participant data)
Probes: `probe_t22_tokenmap_fixtures.py`, `probe_t22_addon.py`. Inputs: FSL MNI152_T1_2mm_brain_mask and Schaefer-400 17-network 2 mm, with the SwiFT S1200 crop/pad applied: `data[7:85, 7:103, 0:84]` from `SwiFT_v2-preprocessing-sdk-handoff/.../preprocessing_HCP_v2.py:20`, and `F.pad(..., (3,9, 0,0, 10,8))` from `SwiFT_v2/.../datasets.py:222`. Result is 96³ with 0 brain voxels lost. The atlas and mask affines match the HCP sform (−2, 2, 2; 90, −126, −72).

| Quantity (12 mm tokens at 16³ unless stated) | Value |
|---|---|
| In-brain tokens (≥50% brain) | 1061 |
| Parent cells whose 8 children are all in brain ("permutable") | 85 (680 tokens). The other 381 in-brain tokens are in boundary cells. Threshold 0.25 → 98/784; threshold 1.0 → 26/208 |
| Permutable tokens with a cortical Schaefer label (≥25% labelled voxels) | 434 / 680 (the rest are WM or subcortical) |
| 8³→4³ merge: in-brain 24 mm tokens / permutable parents | 128 / **8** (64 tokens) |
| Box geometry (atlas proxy), as intra-box spread mm / network homogeneity / fraction crossing the midline / mean token displacement mm | Euclidean 10.4 / 0.379 / 0.0 / 0.0 · atlas box-covering 20.2 / 0.632 / 0.576 / 20.2 · **random 47.7 / 0.181 / 0.988 / 51.0** · **rotation null (bijective, Hungarian spin reassignment) 21.1 / 0.304 / 0.459 / 21.2** |
| Superseded v1 null (nearest-neighbour snap) | not a bijection: 461–505 unique targets of 680 over 8 rotation seeds. Its geometry (19.8 / 0.307 / 0.459 / 19.6) is kept in `probe_t22_tokenmap_fixtures_v1_nnsnap.out.json` |
| Builder time (680 nodes, greedy) | 0.11 s |

### O-D. Operator-level fixtures (top-2-of-8 linear retention per box; PCA fitted on train time, scored on test time; 3 seeds; synthetic only)
| Fixture | Euclidean | FC box-covering (train FC) | rotation null | random |
|---|---|---|---|---|
| F+ realistic (Schaefer-17 sources, SNR 1) | 0.4738 ±0.0035 | 0.4950 ±0.0038 | 0.3839 ±0.0015 | 0.3518 |
| F+ realistic, SNR 2 | 0.6562 ±0.0009 | 0.6588 ±0.0027 | 0.5174 ±0.0158 | — |
| F+ strong (scattered random network labels) | 0.3287 ±0.008 | **0.6172** ±0.0025 | 0.3372 ±0.0039 | — |
| F− (smooth field, σ = 1.5 tokens) | **0.8446** | 0.8269 | 0.8038 ±0.0038 | 0.4304 |
| F0 (iid) | 0.2502 | 0.2506 | 0.2511 | 0.2509; LEAK mutant (FC from test) **0.2508**, i.e. no detectable signature |

### O-E. B300 (read-only checks 00:40–00:55Z; GPU use 01:12–01:28Z)
| Item | Evidence |
|---|---|
| All 4 nodes: 8/8 GPUs at 0 MiB / 0%, 0 compute processes. /scratch/iitp4 absent at 00:40Z | b300_state_readonly.log |
| .98 HCP: `download_HCP_REST1_filtered/` has 1084 subject dirs, **88** complete `rfMRI_REST1_LR_hp2000_clean.nii.gz` (0.967–1.017 GB) and 1 partial temp file. An rsync into /scratch/data/hcp has been running for 1 day 9 h 56 min, so the set is still growing | b300_98_hcp_readonly.log, b300_lock_readonly.log |
| HCP header: 91×109×91×1200, 2 mm, TR 0.72 s, float32, sform code 4, LAS (srow x = −2) | b300_98_hcp_header.log (stdlib parser) |
| .101 OpenNeuro fMRIPrep: ds000228 155 subjects (1 run each, `space-MNI152NLin2009cAsym_res-2`, 97×115×97×168, TR 2 s, int16, RAS), ds000001 16 subjects (48 runs), ds000114 10 subjects (100 runs). Licenses: ds000228 **PDDL**, ds000001 CC0, ds000114 empty field. participants.tsv for ds000228 has Age / AgeGroup / Child_Adult / Gender columns (header line only was read) | b300_101_*.log |
| .99: only ukb_dmri_fp16 (dMRI, 170 GB, rsync running) and empty hcp/ and ukb_raw/ | b300_99_data_readonly.log |
| Env recipe: `/scratch/tmp/requirements.lock` (SwiFT-LLM's, read-only) pins torch==2.15.0+cu134, numpy 2.5.4, einops 0.8.2, monai 1.6.1, scipy 1.18.1, nibabel 5.4.2 | b300_lock_readonly.log |
| My project-local env: `/scratch/iitp4/explorer_M3_r1_2/venv`, built with `build_env.sh` via uv in about 1 min (00:53:43–00:54:36Z). Freeze sha `edcced28…7371`; torch 2.15.0+cu134 (CUDA 13.4), device "NVIDIA B300 SXM6 PC" | build_env.log |

### O-F. Measured B300 throughput (.98 GPU 7; bf16 autocast; AdamW; random tensors on GPU, so no I/O)
| Config | B | sec/step | samples/s | peak GiB | params |
|---|---|---|---|---|---|
| e24, depths 2,2,6,2, heads 2,4,8,16 | 8 / 32 | 0.0569 / 0.1592 | 140 / **201** | 8.7 / 33.9 | 24,356,544 |
| e48, depths 2,2,6,2 | 8 / 32 | 0.0708 / 0.2211 | 113 / 145 | 11.7 / 44.6 | 54,556,032 |
| E192, depths 2,2,18,2 (VRABES) | 1 / 4 | 0.0782 / 0.1265 | 12.8 / 31.6 | 12.4 / 25.5 | 474,226,176 |
| Permuted arm vs identity | — | +0.2% to +0.6% | — | identical | identical |
(smoke_b300.log)

### O-G. Measurement-capacity probe (trained model; synthetic; 1 seed; e24; B=8; 1200 steps; same data stream for every arm; held-out masked NMSE at steps 300/600/900/1200). **A3 here used the superseded nearest-neighbour-snap null.** The script is now patched to the bijection; the GPU run was not repeated
| Fixture | A1 Euclidean | A2 FC box-covering | A3 rotation null |
|---|---|---|---|
| F+ strong (85 planted scattered 8-groups; FC boxes recover them with purity 1.0) | 1.0017 / 1.0009 / 1.0002 / **1.0007** | 1.0016 / 0.9701 / 0.9493 / **0.9273** | 1.0018 / 1.0009 / 0.9997 / **0.9965** |
| F− smooth | 0.3052 / 0.2647 / 0.2399 / **0.2300** | 0.3182 / 0.2878 / 0.2571 / **0.2465** | 0.3206 / 0.2965 / 0.2582 / **0.2450** |
72 s of training per arm (synthetic generation on the GPU dominates). fixture_train_probe.log.

### O-H. Hygiene
- C1 `sha256sum -c PROTECTED_HASHES.txt`: rc=0, 67 OK (01:33Z).
- No git writes.
- No processes left on B300 (ps count 0) or locally.
- Probe logs scanned for `sub-…` and 6-digit IDs: none (HCP and OpenNeuro listings were redacted at source).
- I created `results/gpu_ledger_2026-10-31.md` and its flock file `results/gpu_ledger_2026-10-31.md.lock`.
- I left `/scratch/iitp4/explorer_M3_r1_2/` on .98 (5.5 GB; venv, logs, copies of probes). It is safe to delete, or the worker can reuse it after checking the freeze sha.
- A peer created `/scratch/iitp4/explorer_M3_r1_1/`. I did not read it.

## 2. Logic Chain
1. O-A → T2.1 is closed from code. Spatial merging happens only at the ends of stages 0–2 (16³→8³→4³→2³). layer_2 and layer_3 share the 2³×20 grid and 8C width. They differ by 2 blocks plus the final LayerNorm, not by a merge. The old "PatchMerging between layer_2 and layer_3" premise is false. Old "analysis 2" did not test SwiFT's merge at all.
2. O-A (window and RoPE assumptions, `L == T·D·H·W` assert at ver11.py:717) → any pooling that outputs tokens off the regular grid, or a variable number of them, breaks stages 1–3. So a box pool must produce exactly one token per coarse cell from exactly 8 children. The old `ConnectomeRGPooling` (mean + Linear(C→2C), 76 variable boxes) fails this and is not parameter-matched.
3. O-B → a fixed per-frame spatial permutation in front of the unchanged PatchMergingV2 meets T2.2's matching requirements by construction: the same parameters, FLOPs, tokens, decoder, windows and RoPE (all measured equal). The Euclidean arm is literally the stock module. The unit-test list is already shown to fail on the five defects most likely to slip in.
4. O-C → at 8³→4³ only 8 boxes could change, so any effect would be diluted below detection. 4³→2³ is worse. The 16³→8³ merge (85 boxes, 680 of 1061 in-brain tokens, 12 mm, about Schaefer-400 parcel scale) is the only merge where pooling can plausibly matter.
5. O-C (geometry) → fully random boxes displace tokens by 51 mm against 20 mm for connectome boxes. "RG beats random" would therefore partly measure locality cost. A bijective rotation null (21.2 mm, homogeneity 0.304 against 0.632) matches locality and scrambles network identity, so it is the right primary null. Euclidean is the practical baseline.
6. O-D → at the operator level, realistic network geometry leaves little headroom. Euclidean 24 mm cubes already retain almost as much as FC boxes (+0.021 at SNR 1, +0.003 at SNR 2). The headroom is large only when networks are spatially scattered (+0.29). The real-data effect is expected to be small. Neither the kill rule nor the report may read a non-significant Δ as "no effect".
7. O-D (F0 leak mutant) → a statistical leak signature is invisible. Leakage of test data into the partition must be tested structurally: the partition hash is unchanged when test-split data are perturbed.
8. O-G → the primary metric has measurement capacity. With a planted scattered effect, held-out masked NMSE separates A2 from both A1 and A3 within 1200 steps on 1 seed. With smooth fields it ranks Euclidean first. This is a single-seed, small-budget probe, and its A3 used the superseded non-bijective null. The worker's gate must repeat it with 5 seeds at the real step budget.
9. O-A (decoder anchoring) + O-C (A2 crosses the midline in 58% of boxes, A3 in 46%) → the SimMIM objective penalises non-local merges. The A2 vs A1 contrast is therefore conservative for RG. The A2 vs A3 contrast shares most of the penalty. Both must be stated in the card.
10. O-E → the permitted fMRI on B300 is HCP-YA (.98) and OpenNeuro fMRIPrep (.101). HCP has 1200 TRs per subject, which suits 20-frame windows, but it is still downloading and sits under the HCP Open Access DUT. ds000228 is PDDL (unambiguously public) but has 168 TRs, a pediatric sample, the NLin2009cAsym template and RAS orientation. The HCP-space token map must never be reused on it.
11. O-F → e24 at B=32 runs 201 samples/s. Each step computes 32 windows of 20 frames, so 20k steps = 640k windows ≈ 0.89 GPU-h. The arms differ by less than 1%. The 60-subject HCP train set in fp16 is 60 × 1200 × 96³ × 2 B ≈ 127 GB, which fits in one B300's 275 GB with the model, so data loading can be avoided. E192 at that sample count is ≈ 5.6 GPU-h per run, so a 9-run design would exceed the cap.

## 3. Caveats
- The VRABES dumps came from the NERSC perlmutter fork, which was not inspected. All 4 local ver11 variants have an identical PatchMergingV2.
- My first rotation null (v1, nearest-neighbour snap) was not a bijection, and all rotation-null numbers were recomputed with the Hungarian version. The v1 outputs are kept as `verification/explorer_M3_r1_2/*_v1_nnsnap.*`. The B300 run O-G used v1 for A3 and was not repeated.
- Operator-level retention (O-D) is linear, and only an upper-bound proxy. O-G is 1 seed, 1200 steps, e24, B=8, with fresh synthetic data each step and no overfitting regime. Neither is a result.
- Brain-mask geometry used the FSL MNI152 template, not subject masks. Real per-subject masks (mean > 0 after S1200 crop/pad) may change the permutable count somewhat. The worker should fix the rule on the template, or on train subjects only, before results.
- HCP family structure (twins and siblings) is restricted data and unavailable, so a family-aware split is impossible. The paired arm contrast is less sensitive to this than absolute levels.
- Throughput excludes data loading, eval and checkpointing; budget about +10–20%. B>32 and multi-GPU were not measured.
- I did not read explorer_M3_r1_1's findings (only its progress.md, for B300 activity), as the task's independence requirement asks.
- The HCP rsync on .98 belongs to another workstream. It still writes, so file counts will change.

## 4. Conclusion (recommendation to the worker; not implemented)

**T2.1 (document; reuse O-A).**
- Write `docs/03_empirical_analysis/topic2/2026-11-0X_topic2_architecture_from_code.md` with the stage table, the file:line citations and the false-premise lines.
- Add a test that instantiates the vendored ver11 at 96³×20 and asserts the per-stage `input_resolution`, the merge Linear shapes, `downsample is None` at stage 3, and the hook shapes. (`probe_t21_t22_wrapper.py` Part A is the template.)

**T2.2 card (freeze sha256 before any HCP value is touched).**
- **Question.** In SwiFT ver11 SimMIM (96³×20, patch 6), replace the stage-0 (16³→8³) Euclidean grouping of the 680 permutable in-brain tokens with connectome boxes. Hold parameters, FLOPs, tokens, data, seeds and steps identical. Does held-out-subject masked-voxel NMSE improve (a) against unmodified PatchMergingV2 (A1) and (b) against a locality-matched rotation null (A3)?
- **Arms.**
  - A1 = stock ver11 (identity permutation).
  - A2 = fixed-size-8 greedy radius-1 box covering on train-split token-level group FC. Name it as a deviation from Song et al. 2005 (variable boxes, l_B).
  - A3 = the same builder on FC whose node identities are remapped by a fixed random rigid rotation, a different one per seed. The reassignment must be a BIJECTION (Hungarian on rotated vs original coordinates), not a nearest-neighbour snap.
  - Placement: Hungarian box→parent, then Hungarian member→slot (identity for Euclidean). Background and boundary tokens stay identity.
  - Optional descriptive arm only: fully random boxes, labelled not locality-matched.
- **Connectome.** Mean BOLD per 6³-voxel token for train subjects only → Pearson → Fisher z → mean → positive part. Public-atlas alternative: Yeo-17 boxes, as a sensitivity arm only if budget remains.
- **Metric.** Primary: masked-voxel NMSE on sealed test subjects, with fixed eval windows and mask seeds, paired per subject. Secondary, descriptive only: merge-level ridge retention, and centered PR per stage (link to M2).
- **Verdict rules.** Δ_E = A2 − A1 and Δ_N = A2 − A3, each paired within seed.
  - **Inference unit.** The seed is the primary unit. Use a hierarchical bootstrap: resample seeds, then test subjects within each resampled seed, B = 10,000. The alternative is a seed-paired test on per-seed subject means. A subject-level bootstrap of seed-averaged differences is NOT allowed: with models trained from scratch, between-seed variance dominates, so with 3 seeds the effective n is about 3, not 20.
  - **Two claims, two rules.**
    - (i) Practical claim (A2 vs A1): keep if upper CI(Δ_E) < −δ. Stop if lower CI(Δ_E) > −δ. Otherwise inconclusive.
    - (ii) Connectome-specific claim (A2 vs A3): keep if upper CI(Δ_N) < 0. Stop if lower CI(Δ_N) ≥ 0. Otherwise inconclusive.
    - The outcome "A2 beats A3 but not A1" means (ii) keep and (i) stop or inconclusive. The realistic-geometry probe (O-D) predicts that (ii) is the easy bar and (i) the binding one.
  - δ is `UNSET`, a PI decision (suggested 1% relative NMSE).
  - Any fixture, parameter or FLOP mismatch, or NaN is an execution-integrity failure, not a null.
- **Confounds to state.** Decoder octant anchoring penalises A2 and A3. Midline crossing differs (A2 58%, A3 46% in the atlas proxy). Report the actual values. There is no family-aware split.
- **Seeds and budget.** 5 seeds by default; the number of seeds drives power. Every arm uses the same seed set. A3 uses a different fixed rotation per seed, so the variability of the null enters the seed variance without adding arms. e24, depths 2,2,6,2, B=32, 20k steps, AdamW, bf16, mask ratio frozen in the card.
- **Split.** Pin a manifest of the complete HCP files (hashed positions, size, sha256, `gzip -t`), excluding partials. Subject-level train/val/test, e.g. 60/8/20, with test sealed. Per-subject brain-voxel z-score.

**Implementation and tests** (`src/topic2_rgpool/`, `tests/topic2_rgpool/`; never `src/*.py`, because of the old AST audit and C2).
- Vendor ver11 with its sha.
- Port checks T0–T7 and the 5 mutants from `probe_t21_t22_wrapper.py`.
- Add these tests:
  - partition train-only: perturb test frames → partition hash unchanged;
  - builder determinism;
  - builder equivariance on tie-free random graphs only;
  - background and boundary tokens untouched;
  - arm parameter and FLOP equality;
  - grid assert.
- Synthetic fixtures through the actual training loop. Port `fixture_train_probe.py`.
  - Gate: run at the SAME step budget and batch as the real test. A tiny-budget A2 lead (O-G) can be a learning-speed effect that shrinks once stage-2 global attention catches up. F+strong must give A2 < A1 and A2 < A3, with CIs from the same hierarchical bootstrap excluding 0.
  - The rotation null must be a bijection: assert `len(unique(remap)) == N`. The v1 nearest-neighbour snap fails this assert.
  - F−smooth must give A2 ≥ A1 − tol.
  - If F+strong fails, stop before real data. Verdict "measurement capacity insufficient" → T2.3 escape clause.

**T2.3 cost.** Use one node (.98, where HCP sits), 8 GPUs, and detached jobs with `timeout`. Run nvidia-smi before each launch. Write ledger started/completed rows under flock.
- Design A, recommended (20k steps, B=32, 5 seeds):
  - real: 3 arms × 5 seeds × about 1.0 GPU-h ≈ 15 GPU-h;
  - gate at the same budget: 2 fixtures × 3 arms × 5 seeds × 1.0 ≈ 30 GPU-h;
  - **total ≈ 45 GPU-h, ≈ 50 with 10–20% I/O, eval and checkpoint overhead.**
- Design B, cheaper matched option (10k steps for gate and real alike): ≈ 22.5 GPU-h, ≈ 25–27 with overhead.
- Design C (gate 3 seeds + real 5 seeds at 20k): ≈ 33 GPU-h, ≈ 36–40 with overhead. The gate then has less power than the real test, which must be stated.
- Explorer use so far: 0.134 GPU-h.
- Everything fits the 64 GPU-h cap. Design A leaves ≈ 14 GPU-h for every other milestone, so root or the PI should choose A, B or C.
- E192-scale replication (about 5.6 GPU-h per run, ≥50 GPU-h) belongs in a costed plan for PI approval only.
- Env: copy `build_env.sh` plus pins (add nibabel 5.4.2) into the repo as `scripts/b300_env/`. Build `/scratch/iitp4/venv`. Never use `~/envs/swiftllm`, never touch `~/enigma_ocd`. Preprocess HCP frames to `/scratch/iitp4/` and keep the train set on the GPU. Copy results back (/scratch is wiped on VM stop).

**Gating decision for root/PI.** Does HCP-YA Open Access (DUT-governed, staged on NIPA B300 by another workstream) count as "public" under C6?
- If yes: HCP pilot as above.
- If no: ds000228 (PDDL) with its own token map (97×115×97 crop at datasets.py:459, RAS orientation). It is weaker (168 TR, mostly children), so re-cost it and expect lower power.
- If neither is acceptable: deliver card + implementation + fixtures + this costed plan under the T2.3 escape clause.

## 5. Verification Method
```bash
cd /home/juke/git/00IITP-AI/verification/explorer_M3_r1_2
PY=/home/juke/superclaude-env/bin/python3; export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2
nice $PY probe_t21_t22_wrapper.py        # A: stage table/hook shapes; B: T0-T7 true, mutants all caught; C: params/FLOPs equal (~10 s)
nice $PY probe_t22_tokenmap_fixtures.py  # 1061 in-brain, 85 permutable parents; geometry table; retention table (~5 s)
nice $PY probe_t22_addon.py              # 8^3->4^3: 8 parents; F+strong 0.617 vs 0.329
grep -n "x\[:, :, i::2, j::2, k::2" /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py   # line 81
cat smoke_b300.log fixture_train_probe.log          # B300 measurements (copied back)
cat /home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md
cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt; echo rc=$?
```
Reproduce O-G on B300 (≈0.12 GPU-h; check nvidia-smi first and log it): `cd /scratch/iitp4/explorer_M3_r1_2 && CUDA_VISIBLE_DEVICES=<idle> timeout 780 ./venv/bin/python fixture_train_probe.py permutable_16cube_thr0.5.json 1200 8 cuda`.

**Invalidation conditions.** This report is wrong or stale if any of the following holds:
- the perlmutter fork's PatchMergingV2 differs from local ver11;
- subject-level brain masks give far fewer than 85 fully in-brain parents;
- the F+strong separation does not reproduce across ≥3 seeds;
- B300 GPUs are occupied, or `/scratch` was wiped (VM stop);
- the HCP file set changes before the manifest is pinned;
- the PI rules HCP not permitted under C6.
