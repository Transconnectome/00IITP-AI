# explorer_survey_2 — handoff (survey; primary M2 Topic 3 + M3 Topic 2)
Written 2026-10-31 (~17:20 KST). Read-only investigation; no production code written. Probes: /home/juke/git/00IITP-AI/verification/explorer_survey_2/2026-10-31/.

**Summary.** The Topic 3 report table (PR 11.02 for layer 2, 3.58 for layer 3) and empirical_results.json (PR ≈ 1.0) come from two different scripts: the report comes from a centered-covariance estimator in `src/empirical_connectome_ablation.py`, the json from an uncentered SVD in `src/spectral_rg_flow_diagnostic.py`. The premise "PatchMerging between layer_2 and layer_3 collapses PR" is false in code: SwiFT ver11 has no merge between the layer_2 and layer_3 dumps, and the last merge happens inside stage 2, before the layer_2 dump. Topic 4's forecast R² = 1.0 is a zero-padding artifact. **Escalation:** ENIGMA-OCD participant data already sits on all four B300 nodes, put there by another workstream (C6).

## 1. Observation

### Topic 3 (M2)
- O3.1 `src/spectral_rg_flow_diagnostic.py:52-60` `compute_participation_ratio`: `s = svd(X)`, `PR = (Σs²)²/Σs⁴`, no centering. `fit_htsr_powerlaw_alpha` (`:63-104`) uses `eigs = s²/N` of the uncentered X and fits a log-log rank slope over ranks 2..round(0.5·nnz).
- O3.2 `src/empirical_connectome_ablation.py:143-160` `estimate_powerlaw_alpha`: `Xc = X - mean(X,0)`, cov eigenvalues, PR from them, and a slope fit over `eigs[1:k_max]` with `k_max = max(10, D//2)` and `vals > 1e-10`. `run_analysis_3_foundation_model_rg_flow` (`:375-438`) reads the same 7 VRABES npz files.
- O3.3 Timestamps (`ls --full-iso`): ablation.py 10-30 15:47 → REPORT.md 15:50 → spectral_rg_flow_diagnostic.py 17:00 → run_all_empirical_experiments.py 17:02 → empirical_results.json 18:40. `run_all…py:129-157` writes both `topic3_spectral_rg_flow_diagnostic` and the "backward-compatible" `analysis_3_foundation_model_rg_flow` from the uncentered code. The json therefore contains no output of the centered code.
- O3.4 The report table's d_B, R_hub and r columns match the json exactly, e.g. layer 2 = 2.8009 / 2.9925 / −0.0652. These metrics come from row-cosine similarity, which centering does not affect. Only PR and α differ: layer 2 is 11.0202/1.5980 in the report and 1.0743/1.4074 in the json.
- O3.5 Synthetic fixture (`probe_t3_centering_fixture.py` → `.out.json`). For rank-k signal plus a mean offset, uncentered PR → 1.02 at offset 10, for k = 1, 5 and 20. Centered PR stays at 1.0 / 4.61 / 15.0. With iid Gaussian data of the real shape 57×1536, both estimators give PR ≈ 54–55 (bounded by N−1 = 56). The α values come out 0.13 (U) and 0.22 (C), which the code's regime table labels "Over-compressed (Rank Collapse)" even though the input is pure noise. A rank-decay slope a = 1 corresponds to a density exponent of 1 + 1/a = 2.0 (MLE 2.008).
- O3.6 Real inputs (keys and shapes only; IDs not printed): `VRABES/RemissionAnalysis/pooled_E192_layers/layer_{0..3}.npz` X = (57,384), (57,768), (57,1536), (57,1536); BrainLM and BrainJEPA (57,768); NeuroSTORM (25,288); also `pooled_E192/whole_brain_layer3_matrix.npz` (57,1536), ses02 (51,1536), and pooled_E96 (25,768)×3.
- O3.7 Producer: `VRABES/RemissionAnalysis/pool_E192_layersweep.py`. It takes the mean over tokens, or over (C,D,H,W,T) for layer_3, then the mean over 7 frames, giving one vector per subject. Frame-level dumps: connectome `/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES/` holds 399 frame*.pt files (= 57×7, 8.1 GB, group `connectome` readable). One file holds layer_0 (10240,384), layer_1 (1280,768), layer_2 (160,1536) and layer_3 (1536,2,2,2,20), all float32. Also `04_embedding/swift_zoo_ses-01/` holds other checkpoints with 399 files each: HCP_N400_T2400_E192, NewUAH_deepE192_L1e-4/L5e-5, NewUAH_E36; and partial sets: E96 287, E192 147, E96_SL60 114, HCP_N800 34. Frames `03_MNI_to_TRs/` are patient images and stay on the lab server only.
- O3.8 Pooling differs by model. BrainLM uses the CLS token (`extract_brainlm_embeddings.py:95`, ckpt under `MDD_treatment_response_fMRI/`). BrainJEPA uses the token mean (`:108`). NeuroSTORM uses global average pooling with N = 25 (`extract_neurostorm_embeddings.py`). SwiFT uses the token + frame mean.
- O3.9 `spectral_rg_flow_diagnostic.py:207-221`: if a file is missing, the code silently substitutes `rng.randn` data under the real layer name. `:262` hard-codes `"optimal_ood_layer_identified": "SwiFT_E192_Layer2"`. The OOD score (`:166-174`) is an ad-hoc weighted formula, and no OOD data is used anywhere.
- O3.10 The existing test `tests/test_empirical_four_topics.py:562-580` checks PR only on rank-1 and isotropic zero-mean matrices, so it cannot catch the centering defect.
- O3.11 `SwiFT-LLM-isotok/data/neuroprior_aligned/npe_mine.npz` key `npe_pca200` (450,200) is already PCA-reduced, so its spectrum is shaped by the PCA truncation.

### Topic 2 (M3)
- O2.1 Model used for the VRABES dumps: `--model simmim_swin4d_ver11 --embed_dim 192 --depth 2 2 18 2 --num_heads 6 12 24 48 --patch_size 6 6 6 1 --window_size 4 4 4 10 --img_size 96 96 96 20 --c_multiplier 2` (`VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` lines 71-87).
- O2.2 `SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py`:
  - `PatchMergingV2` (`:41-88`) concatenates the 8 spatial children (`i::2, j::2, k::2` over D,H,W), applies LayerNorm(8C), then Linear(8C → 2C). Time is never merged (`:70` comment "Skip dimension reduction on the temporal dimension").
  - The stage loop (`:1038-1070`) uses `downsample = PatchMergingV2 if i_layer < num_layers-1 else None`, and `RoPE4DBasicLayer.forward` (`:914-923`) applies the blocks and then the downsample, so the merge is inside the stage.
  - `_forward_hook_embedding` (`:1382-1412`) records `layer_i` = output of stage i, including its merge. Only the last stage gets the final `self.norm` (LayerNorm).
- O2.3 Resulting geometry: input 96³×20 → patch 6 → 16³×20 tokens, dim 192. Stage 0 + merge gives layer_0 at 8³×20 = 10240 tokens, 384-d. Stage 1 + merge gives layer_1 at 4³×20 = 1280, 768-d. Stage 2 (18 blocks) + merge gives layer_2 at 2³×20 = 160, 1536-d (Linear output, no post-LN). Stage 3 (2 blocks, no merge) + final LayerNorm gives layer_3 (1536,2,2,2,20). This matches the shapes in O3.7.
- O2.4 SwiFT v2.5 (`swin4d_transformer_ver12.py:529-585`, `AsymmetricTemporalPatchMerging`, `temporal_merge_stages=(True,True,False)`) also merges time, but the VRABES dumps do not use it. No a-SwiFT repo or module was found locally: `ls ~/git | grep -i swift` and grep in SwiFT_v2 both return 0 hits. "a-SwiFT" appears only in 00IITP-AI docs.
- O2.5 `src/rg_box_pooling.py`:
  - The "Euclidean_Contiguous_PatchMerging" arm (`:368-372`) slices ROI indices 0..303 into contiguous runs. It does not merge a spatial grid.
  - The RG boxes (`:162-224`) are a greedy l_B=2 box covering, followed by a Fiedler-coordinate ordering, followed by contiguous slicing into 76 groups.
  - `ConnectomeRGPooling` (`:227-326`) computes S^T X (mean-like) and then Linear(C → 2C). PatchMerging uses concat-8 with Linear(8C → 2C), so parameter count and within-box information differ.
  - The real-data runner (`:433+`) reads ENIGMA `vmd_cache_4ch_464_head.mmap[i,0]`.
- O2.6 Circularity probe on iid Gaussian data (`probe_t2_circularity.out.json`, 8 seeds): all three schemes give var_ret ≈ 0.250, coherence ≈ 0 and recon R² ≈ 0.372, both in-sample and with boxes built from the other half. My double-dipping hypothesis is therefore not supported on null data.
- O2.7 Real-data rank probe (positions 0–2, `probe_t2_vmd_rank.out.json`): VMD channel 0 has numerical rank 99 / 69 / 113, and 100% of its energy is in the top 76 components. Channel 4 has rank 1 and is the validity mask (corroborated by `verification/explorer_survey_3/probe_cache_layout.log`). The old real-data `reconstruction_R2 = 1.0` in all arms therefore comes from the low effective rank of the input, not from pooling.
- O2.8 B300, all 4 nodes checked read-only at ~16:35 KST:
  - GPUs: 8 per node, all at 0% / 0 MiB.
  - `/scratch`: 28 TB md0, no `/scratch/iitp4`.
  - Env: `~/envs/swiftllm/bin/python` with torch 2.15.0+cu134. The system python has no torch.
  - Data on .98: `/scratch/data/hcp` (38 GB, 40 REST1 .nii.gz in MNINonLinear; raw, not SwiFT frames) and `hcp_dmri` (53 GB). On .101: `/scratch/data/openneuro` (68 GB).
  - UKB: `~/enigma_ocd/data/ukb/UKB_ROI/` holds 40,792 subject dirs, each with `schaefer_400Parcels_17Networks_*.npy` of shape (490,400) float32. `manifests/ukb_schaefer400.sha256` exists. No UKB phenotype file was found by a `find / -maxdepth 4` name search.
- O2.9 Schaefer-400 17-network atlas, public and local: `/home/juke/nilearn_data/schaefer_2018/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_2mm.nii.gz` and `…_order.txt`.
- O2.10 `SwiFT-LLM-b300-integration/docs/B300_READINESS_AUDIT_20261031.md` §2 records that B300 throughput was never measured, that the NIPA notice §7 sanctions unauthorized or unclear-purpose GPU use, and that PI decision 1 (grant alignment) and decision 2 (data-use scope on B300: storage-only approved at the time) were open. It also lists another live B300 teamwork, `SwiFT-LLM-b300-openneuro` `b300-openneuro-20261031T1640`.
- O2.11 **C6 conflict (pre-existing, not created by this run).** `connectome@61.107.201.98:~/enigma_ocd/data/enigma_palm_20261029/data/` contains `MBBN_data_304_ROIs_0.25/` with 1,706 .npy files, site-named subject directories, `metadata/` with a csv, `splits/` and `vmd_cache_4ch_464_head*.mmap` (11 GB). Directories of similar size exist on .99, .101 and .103 (`~/enigma_ocd`, 55–96 GB, ~42.5k .npy each, dated 10-31 01:3x–15:4x). Listing was done with IDs redacted; nothing was read or changed.

### Topic 4 (M4)
- O4.1 `src/fractal_motif_resu.py:470-480` uses the input `mmap[i,0]` (VMD ch0, 464 rows, padded), 48 ROIs and a column z-score. `:415-425` splits at `int(0.7*(T-1)) = 325` and computes `R² = 1 − ss_res/max(ss_tot, 1e-8)`.
- O4.2 `probe_t4_padding.out.json`, positions 0–4: validT = 177 (from mask channel 4), the test segment starts at row 325 (entirely padding), test ss_tot ≈ 2e-45, so the denominator floor 1e-8 is hit. R² = 1 − ~0/1e-8 = 1.0 for any predictor, including C0. Persistence R² is also 1.0 on every channel (`probe_t4_persistence.out.json`).
- O4.3 Topic 4's `effective_dim_PR` uses the same uncentered `compute_participation_ratio` (`:409-410`) on nonnegative rectified outputs, so PR ≈ 1.00 is the O3.5 artifact again.

### Common
- C1 check: `LC_ALL=C sha256sum -c …/sentinel/PROTECTED_HASHES.txt` gives 67 OK, rc = 0. No source, test or doc files were modified.

## 2. Logic Chain
1. O3.1 + O3.2 + O3.3 → the report and the json were produced by different estimators at different times, and the json's `analysis_3` was overwritten by the uncentered path.
2. O3.4: the centering-invariant columns agree and the centering-sensitive columns disagree. Together with O3.5, where uncentered PR → 1 whenever the mean dominates, this makes the uncentered SVD the most likely cause of PR ≈ 1. The α discrepancy has two causes: centering and the different fit window (2..~28 vs 2..~56).
3. O2.2–O2.3 → layer_2 and layer_3 have the same 2³×20 token grid and 1536-d. What separates them is 2 Swin blocks plus the final LayerNorm, not a PatchMerging. The "layer 3 PatchMerging collapse" claim (REPORT lines 81 and 120) is false in code. Any layer2 → layer3 PR change is also confounded by the LayerNorm, which layer_2 lacks.
4. O3.5 (PR ≤ N−1 = 56 for subject-pooled matrices) + O3.8 (different pooling, N = 25 vs 57) → cross-model PR comparisons such as "JEPA/NeuroSTORM 2.7× BrainLM" are not interpretable without a matched N, a matched subject set and a matched pooling.
5. O3.5 (rank slope vs density exponent) → the HTSR regime cut-offs (1.5–2.0 critical, > 4 under-trained) belong to the eigenvalue density exponent of weight matrices. Applying them to rank slopes of representation spectra is a category error. Noise gets labelled "rank collapse".
6. O2.5 → the old Topic 2 "Euclidean" arm was not Euclidean, and the RG module is not parameter-matched to PatchMergingV2. O2.6 shows the old pipeline is not biased on null data, so the old results are uninformative rather than circular. O2.7 shows the R² metric carried no information.
7. O4.2 → the T4.1 diagnosis is a zero-padding test window plus the denominator floor. It is not "the task is too easy" in a scientific sense. This holds for positions 0–4 with validT = 177. Positions 5–11 used by the old run were not checked (probe cap ≤ 5).
8. O2.8 + O2.10 + C6 → on B300 the only usable non-synthetic data for a trainable Topic 2 test is the UKB Schaefer-400 ROI series. HCP is 40 raw runs and would need full preprocessing. Third-party SwiFT checkpoints are not redistributable (VRABES README table), so a voxel-SwiFT fine-tune on B300 is out. The UKB copy sits inside another workstream's `~/enigma_ocd` tree, next to the ENIGMA data from O2.11.

## 3. Caveats
- I did not compute centered PR or α on the real 57-subject matrices. That would reveal values the M2 card will govern. Whether the centered formula in O3.2 reproduces 11.0202 / 3.5786 / 4.3188 / 11.7851 / 12.5070 exactly is therefore unverified. The M2 worker should run this reproduction as the first card-listed step, either after freezing or explicitly labelled "reproduction of already-public numbers".
- The ENIGMA-on-B300 finding is based on directory and file names, counts and sizes. I did not check whether a PI approval exists for that separate workstream. The ACCEPTANCE C6 text (root, 10-31 16:28) forbids it for this run regardless.
- B300 GPU-h numbers below are analytic estimates. Real B300 throughput is unmeasured (O2.10).
- The UKB ROI column order vs the Schaefer `_order.txt` label order is assumed from the filename, not verified.
- No UKB phenotypes are on B300, so Topic 2 downstream metrics must be self-supervised or label-free.
- Topic 1 coverage is thin: I relied on the GATE_STATUS and victory-auditor handoff.
- The advisor tool was rate-limited and was not consulted.

## 4. Conclusion (recommendations, scoped)

### K-list (facts for root)
- K1 Topic 3 provenance: report = `empirical_connectome_ablation.py` (centered); json = `spectral_rg_flow_diagnostic.py` (uncentered). T3.1 can be closed with the O3.5 fixture plus an exact-reproduction step.
- K2 There is no PatchMerging between layer_2 and layer_3. The last merge (4³ → 2³, 768 → 1536) happens inside stage 2, before the layer_2 dump. layer_3 = stage 3 (2 blocks) + final LayerNorm. Time is never merged in ver11.
- K3 Real representation inputs:
  - Subject-pooled npz files in VRABES (local, N = 57/25).
  - Token-level frame dumps on connectome `/storage/bigdata/VRABES/04_embedding/` (lab-only), including a 4-checkpoint "zoo" with complete 399-file sets.
  - Raw frames on the lab server only.
- K4 Topic 4 R² = 1.0 is a padding artifact (test window inside zero padding) plus the denominator floor. PR ≈ 1 is the uncentered-PR artifact.
- K5 **Escalate:** ENIGMA-OCD participant data is present on all four B300 nodes in `~/enigma_ocd/data/` (O2.11). This run must not read, copy or move it, and must not co-locate new ENIGMA files there. Root should report it to the human.

### M2 Topic 3: card recommendations (T3.2/T3.3)
- **Estimators to freeze**
  - Centered PR = (tr C)²/tr C², with C the covariance of row-centered data.
  - Report it two ways: (a) subject-level, on the N×D pooled matrix, as PR and PR/(N−1); (b) token-level, per subject × window, on the frame dumps (layer_0 10240×384, layer_1 1280×768, layer_2 160×1536, layer_3 160×1536), summarized over the 57×7 windows. Option (b) removes the N = 57 ceiling and is CPU-only. Run it on connectome or copy the 8.1 GB locally; never to B300 unless the files are de-identified (the filenames contain subject IDs).
- **α**
  - State one method. Primary: a Clauset-style MLE of the eigenvalue density tail, with xmin chosen by KS distance.
  - Secondary: the rank-decay slope over a fixed rank window [2, min(N−1, 50)], with the conversion α_dens ≈ 1 + 1/a stated.
  - Drop the HTSR regime labels and the OOD score entirely (O3.9).
- **Controls**
  - (i) Column-wise permutation across subjects (keeps marginals, destroys covariance).
  - (ii) Gaussian / Marchenko–Pastur reference at the same N and D.
  - (iii) Subject bootstrap CIs.
  - (iv) A LayerNorm-matched comparison: apply parameter-free per-token LayerNorm to layer_2 before comparing it with layer_3.
  - (v) Random-init representations: a ver11 forward pass with the same config and a fixed seed on the same VRABES frames. This needs a GPU on connectome (A5000, lab data, no checkpoint needed), about 57×7 forward passes at batch 1, ≲ 1 GPU-h. It is not allowed on B300 (patient frames, C6).
  - (vi) For cross-model claims: an identical subject subset (the intersection with NeuroSTORM's 25) and the pooling recorded per model.
- **Hypotheses (falsifiable)**
  - H1: token-level centered PR(layer_3) < PR(layer_2) after LN-matching. Killed if the bootstrap CI includes 0, or if the random-init difference has the same sign and size.
  - H2: trained PR ≠ random-init PR at each layer.
  - H3: the old cross-model ordering (JEPA, NeuroSTORM > BrainLM) holds at matched N, subjects and pooling.
- **Fixtures (T3.3)**
  - Known-rank k + large mean offset: centered PR ≈ k and uncentered PR → 1. Fail the build if the production estimator returns < k/2.
  - Synthetic power-law spectra with known a: the MLE recovers the density exponent 1 + 1/a within tolerance.
  - The missing-file path must raise, not fall back to synthetic data.
- **Old claims expected to fail or be untestable:** "layer 3 PatchMerging collapse" (architecturally false); "optimal OOD layer" (hard-coded, no OOD data); regime labels (category error). The "layer 2 PR explodes" and "JEPA > BrainLM" claims need the rerun.

### M3 Topic 2: what is true (T2.1) and a redesign (T2.2/T2.3)
- **True architecture:** see K2 and O2.3. Spatial merging happens at the end of stages 0, 1 and 2 (16³ → 8³ → 4³ → 2³). Each merge is a concat of 8 children, then LN, then Linear(8C → 2C). At the last merge only 64 → 8 spatial tokens exist, so a connectome-guided merge at the voxel level would act on 4³ token cubes of 24 mm, not on anatomical ROIs.
- **Recommended falsifiable question.** In a hierarchical ROI-token transformer trained self-supervised on UKB Schaefer-400 rest fMRI, does replacing spatial-proximity token merging with graph-partition merging improve held-out masked-ROI reconstruction? The partition comes from group FC on the training split only, and the comparison holds parameters, FLOPs, data, seeds and steps identical. Does the gain beat a random-partition control with the same box sizes?
- **Arms.** All arms use the same merge operator, concat of 4 children (canonical order within box) + LN + Linear(4C → 2C), applied 400 → 100 → 25. Only the partition differs:
  - A0: flat, no merge (reference).
  - A1: Euclidean, balanced 4-ROI groups from Schaefer centroid k-means/agglomeration (hemisphere-respecting).
  - A2: connectome, balanced graph partition of group FC from train subjects. The level-2 partition uses the coarse-grained graph S^T A S. Name the algorithm in the card: either Song box covering + balancing (as in `build_balanced_rg_boxes`) or balanced spectral/METIS-style partitioning.
  - A3: random balanced partition.
- **Metrics.**
  - Primary: test-subject NMSE of masked-ROI reconstruction (mask fraction frozen in the card).
  - Secondary: within-scan half-split fingerprinting top-1 accuracy among test subjects (label-free); centered PR per stage (links to M2).
  - Kill rule: kill A2 if the paired Δ(A1−A2) 95% CI (subjects × 5 seeds, paired bootstrap) includes 0 or favours A1, or if A2 does not beat A3. A2 survives only if it beats both.
- **Splits.** Subject-level train / val / test (e.g. 8k / 1k / 2k from the 40,792), sealed test. The FC graph is built from train only, and a unit test asserts that S is unchanged when test data are perturbed.
- **Synthetic fixtures.**
  - F+: latent sources tied to spatially scattered communities (e.g. the 17 networks); A2 should beat A1.
  - F−: spatially smooth random fields over the centroids, with the graph from noise; A1 ≥ A2 ≈ A3.
  - Invariants: partition covers each ROI exactly once; permutation equivariance (permute ROIs and S rows together); gradient reaches all reduction weights; shapes.
- **Cost (estimate, unmeasured hardware).** About 5M params, a 40-TR window (temporal patch 4) and 4000 tokens at stage 0 give ≈ 50 GFLOP per sample for forward + backward. 8k subjects × 12 windows × 30 epochs ≈ 2.9M samples ≈ 1.5e17 FLOP, i.e. ~0.2–1 GPU-h per run on one B300 at 10–2% effective utilization. 4 arms × 5 seeds = 20 runs gives ≈ 5–20 GPU-h, plus a 0.5 GPU-h throughput calibration logged first, plus ≈ 1 GPU-h smoke. The budget should be capped at ≤ 22 GPU-h of the 64. The voxel-level alternative (replace stage-2 PatchMergingV2 in ver11, pretrain from scratch) is not testable within the cap or on allowed B300 data. Deliver it as a costed plan only (hundreds of GPU-h).
- **B300 preconditions.**
  - Create `/scratch/iitp4/` with its own venv, or reuse `~/envs/swiftllm` read-only; do not modify it.
  - Copy UKB_ROI read-only into `/scratch/iitp4/data/` and verify against `manifests/ukb_schaefer400.sha256`.
  - Run `nvidia-smi` before each job and log every job in `results/gpu_ledger_2026-10-31.md`.
  - Note the NIPA §7 grant-alignment risk (O2.10) next to the user's "학습 필요하면 b300 이용" ("use B300 if training is needed") authorization.
  - Coordinate with the live `b300-openneuro` run (other users may claim GPUs at any time).

### M4 Topic 4: redesign pointers (T4.2/T4.3)
- Use valid-length handling (mask channel or raw `MBBN_data_304_ROIs_0.25`). Raw BOLD is preferable to the VMD-head cache. Split time within the valid segment, or split by subject.
- Add a guard: fail if test ss_tot < ε.
- Report multi-step forecast skill (h = 1..5 TR) relative to persistence and ridge-VAR(p) baselines (skill = 1 − MSE/MSE_AR), plus a fixed random-W reservoir baseline.
- Compute PR with centering.
- CPU is enough (local or connectome). ENIGMA must not go to B300; if B300 is wanted, use UKB ROI series instead.

### M1 Topic 1 (secondary)
- Per `tw-20261030-topic1/orchestrator/GATE_STATUS.md`, the open items are the 5 surviving mutants (ROI loss `roi_subsample_80`, valid_T drop, curl, seed rule, SP normalisation), the missing cohort-stats script and the unverified connectome CPU env.
- The same ENIGMA cohort exists on B300 (K5). M1 must run locally or on connectome only, as T1.4 states.

## 5. Verification Method
- Provenance: `grep -n "Xc = X - np.mean" /home/juke/git/00IITP-AI/src/empirical_connectome_ablation.py` should return line 145. `sed -n 52,60p …/src/spectral_rg_flow_diagnostic.py` should show no centering. `sed -n 129,157p …/src/run_all_empirical_experiments.py` should show analysis_3 sourced from t3_results.
- Fixtures: `cd /home/juke/git/00IITP-AI/verification/explorer_survey_2/2026-10-31 && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 probe_t3_centering_fixture.py` should match `probe_t3_centering_fixture.out.json`. Likewise `probe_t2_circularity.py` (≈ 1–2 min), `probe_t2_vmd_rank.py`, `probe_t4_padding.py` and `probe_t4_persistence.py`. The last three read ENIGMA positions 0–4 read-only.
- Architecture: `sed -n 41,88p;1036,1070p;900,923p;1382,1412p /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py`.
- Token shapes: on connectome, load one `frame*.pt` from `/storage/bigdata/VRABES/04_embedding/swift_E192/…` and print shapes only.
- B300 ENIGMA presence (do not open files): `ssh -J dgx1,connectome connectome@61.107.201.98 'ls ~/enigma_ocd/data/enigma_palm_20261029/data | sed -E "s/[0-9]{3,}/N/g"'`.
- C1: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`, expected rc 0.
- What would invalidate this report: the centered reproduction fails to give 11.0202 for layer 2, which means a third, unseen producer exists; the ENIGMA-on-B300 directories turn out to hold synthetic or derived non-participant data; the UKB ROI order differs from the Schaefer order.

Probe sha256 (2026-10-31/):
- d52ca76b…d785 probe_t2_circularity.py
- 9a9f6d84…0b6a56 probe_t2_vmd_rank.py
- cfd36fdf…60651a probe_t3_centering_fixture.py
- e4c79170…3af96c probe_t4_padding.py
- 6ce9de08…58dc5cc probe_t4_persistence.py
