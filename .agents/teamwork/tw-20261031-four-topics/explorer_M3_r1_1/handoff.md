# handoff — explorer_M3_r1_1 (M3 / Topic 2; lens: scientific design). Type: Hard.
Written 2026-11-01T02:05Z. Read-only investigation plus probes; no production code. Probes: `/home/juke/git/00IITP-AI/verification/explorer_M3_r1_1/`. B300 use: 0.008 GPU-h (ledger rows 01:44:33Z/01:44:41Z).

## Summary
- **T2.1.** Code (SwiFT_v2 f0dc7aca, ver11) shows three spatial merges, all 2×2×2, none temporal: 16³→8³ (12→24 mm), 8³→4³ (24→48 mm), 4³→2³ (48→96 mm). There is none after stage 3, so the "layer_2→layer_3 PatchMerging" premise is false.
- **Insertion point.** The only point with enough in-brain cells is **M0 (16³→8³)**. In HCP it has 235 brain-touching blocks and 1,189 signal cells.
- **The one changed factor** should be the gather index π that picks which 8 fine cells feed each output cell. With identity π the module is bit-exact PatchMergingV2, so parameters, tokens and FLOPs match by construction. Boxes must be octant-local, because windows, M1/M2 and the decoder are octant-local.
- **Data.** Permitted and usable: HCP REST1_LR (public) on B300 .98, 88 runs. No UKB fMRI is usable: it exists only under `~/enigma_ocd`.
- **Cost.** Measured: SimMIM E36-d2262 trains at about 100 samples/s per B300, with no gather overhead. A 3-arm × 5-seed pilot costs about 9–10 GPU-h, so T2.3 is testable within the cap.
- **Exploratory dev evidence, 5 burned subjects, governs nothing.** FC boxes beat a dispersion-matched FC-shuffle null by a wide margin. They do not beat 2×2×2 cubes on held-out within-box coherence (5/5 folds slightly lower). A kill is plausible; the frozen card must decide it on fresh subjects.

## 1. Observation

### T2.1 architecture (from code)
| # | Observation | Evidence |
|---|---|---|
| O1 | `PatchMergingV2` concatenates `x[:, :, i::2, j::2, k::2, :]` over (i,j,k)∈{0,1}³ (spatial only), then `reduction(norm(x))` = LayerNorm(8C) followed by Linear(8C→2C, bias=False) | `SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py:41-88` (sha256 `de132387…95052a`; last commit 6061dc6d; `git diff --quiet` clean; repo HEAD f0dc7aca) |
| O2 | `downsample = PatchMergingV2 if i_layer < num_layers-1 else None`; `RoPE4DBasicLayer.forward` runs the blocks, then the downsample | ver11 `:1036-1070`, `:914-923` |
| O3 | Built at the VRABES geometry (img 96³×20, patch 6,6,6,1, window 4,4,4,10, c_mult 2), hooks give: patch grid (T,D,H,W) = (20,16,16,16). Merges M0: 81920→10240 tokens (E→2E); M1: 10240→1280; M2: 1280→160. stage3.downsample = None. layer_3 = (C,2,2,2,20) | `verification/explorer_M3_r1_1/probe_t21_shapes.py` → `.out.json` |
| O4 | E192 merge parameters: M0 Linear 1536→384 (592,896 incl. LN); M1 3072→768 (2,365,440); M2 6144→1536 (9,449,472). Physical cell edge, at 2 mm MNI voxels × patch 6: M0 12→24 mm, M1 24→48 mm, M2 48→96 mm | same `.out.json` (`E192_merges`) |
| O5 | `use_post_norm=True` crashes: LayerNorm(2C) is applied to the 8C input (`RuntimeError … normalized_shape=[16]`) | same `.out.json` (`use_post_norm_True_runs`) |
| O6 | Downstream geometry is octant-aligned. Stage-1 spatial window 4³ on the 8³ grid gives 8 non-shifted windows, which are the 8 octants. Stage-2 window = the whole 4³ grid. M2 output = one token per octant. The decoder actually built is `decoder_type='mlp'` (hard-coded, `:1112`). It runs a per-token MLP, then `decoder_spatial_expand` Linear(C→48³), then `PixelShuffle4D(spatial_scale=48)` (`:1118-1146`, `:91-123`). Probe: perturbing final token (0,0,0) at t=3 changes only voxels [0..47]³ at t=3 (0 voxels outside), so each final token decodes only its own octant. The `'linear'` branch at `:1113-1116` is dead code. E36-d2262 params: encoder layers 5.33 M; `decoder_spatial_expand` 31.96 M of 38.71 M total (82.6%) | ver11 `:860-871`, `:1083-1146`, `:1337-1360`; `verification/explorer_M3_r1_1/probe_decoder_params.py` → `.out.txt` |
| O7 | The SwiFT HCP recipe crops `[7:85,7:103,0:84]`, pads X 10/8 and Z 3/9 to 96³, and uses the mask mean>0 with in-brain global z-norm | `SwiFT_v2/project/module/utils/data_preprocess_and_load/preprocessing_HCP_v2.py:20-44`; `datasets.py:191-222` |

### Data permitted and usable (C6), read-only checks at ~00:50–01:10Z
| # | Observation | Evidence |
|---|---|---|
| D1 | B300: 32/32 GPUs idle at 00:47Z and 01:44Z | nvidia-smi |
| D2 | .98 `/scratch/data/hcp/download_HCP_REST1_filtered/`: 88 × `rfMRI_REST1_LR_hp2000_clean.nii.gz` (HCP open access; MNINonLinear 2 mm; 1200 TRs) plus 1 in-progress hidden temp file. The set is still changing | find (IDs redacted) |
| D3 | .101 `/scratch/data/openneuro/openneuro-derivatives/fmriprep/`: ds000001 (48 runs), ds000114 (100), ds000228 (155, Pixar movie), MNI152NLin2009cAsym res-2 (CC0). `.99`: `ukb_dmri_fp16` (dMRI npz only); `ukb_raw` and `hcp` are empty on .99 | find |
| D4 | No UKB fMRI exists on B300 outside `~/enigma_ocd/data/ukb` (per survey 2). I did not list or read `~/enigma_ocd` | dispatch C6 |
| D5 | connectome holds public HCP S1200: REST1 (1,084 subjects), REST2 (1,206), HCP-MMP1 360-ROI series (1,088 × 2 runs × (1200,360) float32). No HCP restricted/family file was found by bounded search | `ls`/`find -maxdepth 2` |
| D6 | connectome→DGX-Spark ssh transfer ran at ~0.33 MB/s (165 MB in 8m20s). connectome Slurm: node4 python3 has no numpy; node1 rejects CPU-only jobs | `verification/explorer_M3_r1_1/connectome_attempts/` |

### Probes
| # | Observation | Evidence |
|---|---|---|
| P1 | `GatherPatchMerging` (index buffer of shape (512,8), then concat, LN, Linear). The identity index reproduces ver11 PatchMergingV2 **bit-exactly** (`torch.equal`). It is permutation-equivariant, gradient reaches all 8 child slots, and params are equal (672=672). An octant-local C partition placed by Hungarian assignment is a bijection with every box in its output cell's octant; 37.1% of rows change vs E (ellipsoid mask) | `probe_gather_merge.py` → `.out.json` |
| P2 | Synthetic Stage-0 fixtures (cell level, ellipsoid mask; held-out r / pca2). F+ (planted scattered 8-cell networks): C 0.418/0.580, E 0.111/0.449, G 0.096/0.380, R 0.039/0.339; C purity vs planted = 1.00. F− (smooth field): E 0.696 > G 0.609 ≈ C 0.596 ≫ R 0.217. NULL: all ≈0.000 held-out (C in-sample 0.020) | `probe_stage0_synthetic.py` → `.out.json` (algo dense/mean) |
| P3 | **Algorithm defect caught by F+:** greedy min-diameter growth with periphery seeding gives C held-out r 0.121 and purity 0.40, with 0 pure boxes. Periphery seeding picks the unnetworked leftover cells first, and max-diameter growth from them takes one cell from each planted network | `v1_stage0_synthetic/NOTE.md`; `probe_stage0_synthetic.out.json` (`Fplus|periphery-max`) |
| P4 | HCP dev geometry (5 subjects, SwiFT crop and mask, median nvox): 12 mm cells touching brain 1,455/4,096; signal cells (≥54/216 voxels) 1,189; M0 E-blocks touching brain 235/512 (24–40 per octant). At 24 mm: 235 cells touch brain, 163 signal; M1 blocks touching brain 50/64 | `probe_stage0_hcp_dev.out.json` (`geometry`) |
| P5 | HCP FC vs distance (12 mm cells): r = 0.270 (adjacent), 0.182 (√2), 0.128 (2–2.5), 0.099 (2.5–4), ≈0.084 beyond 6 cells | same, `fc_vs_distance_5subj` |
| P6 | **EXPLORATORY** leave-one-subject-out (train 4 / held-out 1, octant-local). Held-out within-box r: E .2275, C .2216, C_global .2282, G .2053, S .1519, R .1055. pca2: E .505, G .449, C .445, C_global .441, S .412, R .371. Per fold: C−E r −.0001 to −.0128 (5/5 < 0); C−S r +.062 to +.080 (5/5); C_global−E r −.003 to +.0035 (mixed), pca2 −.055 to −.070. C in-sample r .245 vs held-out .222. Dispersion (cells): E .78, G 1.10, C 1.59, S 1.76, C_global 2.92 | `probe_stage0_hcp_dev.out.json`, `probe_stage0_hcp_dev_v2.out.json` |
| P7 | B300 .98 GPU 5, torch 2.15.0+cu134, bf16 autocast, flash SDPA, random tensors, SimMIM step incl. AdamW. Peak memory 10–24 GiB in all configs: <br>• E36-d2262 (38.7 M params, decoder-dominated): bs8 0.088 s, 90.9 samples/s; bs16 100.6 samples/s, 19.7 GiB. <br>• E36 with permuted gather merge: bs8 0.0872 s (no overhead). <br>• E48-d2262: bs16 98.6 samples/s. <br>• E192-d22182 (474 M): bs4 28.6 samples/s, 24.4 GiB | `smoke_b300_steptime.py` → `.log`; ledger 0.008 GPU-h |
| P8 | C1 `sha256sum -c PROTECTED_HASHES.txt`: 67/67 OK, rc 0 (01:57Z). `src/rg_box_pooling.py` and `tests/test_empirical_four_topics.py` are protected. The old AST audit scans only top-level `src/*.py` and fails on any torch import there (except two exempt files) | `tests/test_pilot_connectome.py:158-185` |

## 2. Logic Chain
1. **Where pooling can act.** From O1–O4, the merges sit at M0/M1/M2, and layer_2 and layer_3 share the 2³×20×1536 grid with no merge between them. A redesign must therefore act at a real merge.
   - P4: M1 has only about 6 brain-touching blocks per octant, and M2 has 8 outputs in total.
   - So **M0** is the only point where re-grouping has room: 235 blocks and 1,189 signal cells.
2. **What must stay fixed.** From O6, everything after M0 is octant-local: windows, M1/M2 and the decoder.
   - A box that mixes octants moves information away from the final token that must decode it, so the architecture penalizes it. This is unrelated to connectivity.
   - Hence: **octant-local boxes** plus Hungarian placement inside the octant (P1).
   - The penalty is not what blocks C in the dev data: C_global ties E on r and loses on pca2 (P6).
3. **Matching by construction.** From P1, a gather-index merge keeps the PatchMergingV2 weights, LN, token count and FLOPs identical, and identity π reproduces it bit-exactly. The only manipulated factor is π (sci-pipeline G5: one changed element).
4. **Choice of null.** In F− (P2), any greedy non-grid grouping (G, C) is less compact than 2×2×2 cubes and loses to E even with no FC information.
   - A C>E win could therefore come from FC, and a C<E loss could come from compactness.
   - The dispersion-matched **S** null isolates FC specificity: S keeps FC vs distance and destroys pair identity; dispersion C 1.59 vs S 1.76.
   - G is mask-aware and compact. R is scattered.
5. **The algorithm must be validated before use.** P3 shows a plausible box-growth heuristic failing on planted structure (purity 0.40). F+ purity ≥0.95 must be a unit test, otherwise C may be noise-grouping.
6. **Data.** From D2–D6 and C6:
   - HCP REST1 on .98 is the only permitted voxel rest dataset on B300 that is staged and usable now. OpenNeuro is short task/movie data.
   - UKB fMRI is unusable (forbidden path). Re-staging from connectome is impractical at 0.33 MB/s.
   - The connectome used for boxes is the group FC of **train-split HCP subjects** (permitted data), never ENIGMA.
7. **Cost.** From P7, a 140k-sample run at about 100 samples/s takes ≈0.39 GPU-h. With 1.5× overhead for data and eval that is ≈0.6 GPU-h. 15 runs ≈ 9 GPU-h, plus fixtures ≈ 1 GPU-h, so ≤12 GPU-h fits the 64 GPU-h cap.
   - The survey-2 estimate of "voxel-level not testable / hundreds of GPU-h" was unmeasured and is superseded.
   - Even E192 is ≈2 GPU-h per run.
8. **What the dev evidence means.**
   - P6: FC carries pair-specific information (C ≫ S). At 12 mm, local coherence dominates (P5), so C does not beat E with 4 training subjects.
   - With about 59 training subjects, C's held-out value may rise toward its in-sample value (.245 > E .2275). The dev probe therefore does not settle C vs E, and the frozen Stage 0 on new subjects is informative.

## 3. Caveats
- **Dev probe scope.** It is exploratory, on n=5 burned subjects with train n=4. It uses only cell-mean BOLD, a scalar per 12 mm cell, whereas the merge compresses 8×C learned features. pca2 and r are mechanism proxies, not model performance.
- **Ordering disclosure.** The Stage-0 primary metric (pca2) is recommended after seeing the dev numbers. Both pca2 and r show C<E there, and pca2 does so more strongly, so the choice does not favor C. A reviewer may prefer r; report both.
- **Family structure.** HCP family relations are restricted and none were found. Relatives may cross splits, which slightly favors C because the graph comes from train FC. Disclose this. Its direction is conservative for a kill.
- **Perlmutter fork.** The NERSC fork (`/pscratch/.../SwiFT_v2_perlmutter`) that produced the VRABES dumps was not inspected. T2.1 is stated for local ver11 f0dc7aca.
- **Smoke-test scope.** It used random tensors and no data loader. Real data needs RAM or page-cache residency: 83 subjects ≈175 GB fp16 at 96³×1200. Use one shared memmap, not a copy per process.
- **The HCP set on .98 is still downloading** (one temp file). Pin a manifest at freeze.
- **HCP Open Access terms.** Processing on NIPA cloud is assumed to be covered by C6 "public datasets". The PI may want to confirm this.
- **Grant alignment.** The NIPA §7 grant-alignment risk (survey 2) is unchanged. B300 time is SwiFT-7T allocation.
- **Mask in the dev probe.** The group mask (median nvox) included the held-out subject. That is label-free and exploratory, but it differs from the train-only rule prescribed for the card.
- **Salt next to hashes (flag for root).** `verification/explorer_M3_r1_1/dev_subject_salt.txt` sits next to the salted hashes, inside a repo the host autocommit daemon may snapshot. HCP IDs live in a ~10⁶ space, so salt + hash can be brute-forced back to IDs. This is literal C4 compliance only; root should decide whether to move the salt off-repo.
- **Independence.** explorer_M3_r1_2 used B300 GPU 7 (ledger 0.134 GPU-h). I did not read its outputs.
- **Footprint.** My B300 env and data remain in `/scratch/iitp4/explorer_M3_r1_1/` (5.5 GB, ephemeral). It holds no participant data copies; the derived arrays were in RAM only. Delete it or let VM stop wipe it.
- **Unverified throughput.** I did not measure SimMIM convergence speed, so whether 140k samples is enough for a meaningful pilot is unknown. The card makes the comparison at a fixed budget and adds a learning-curve secondary.

## 4. Conclusion — recommended strategy for the worker

### T2.1 deliverable
Write `docs/03_empirical_analysis/topic2/2026-11-01_topic2_architecture.md`. It should contain:
- O1–O7 with line citations;
- the corrected statement: "no merge between layer_2 and layer_3; the 1536-d arises at M2 inside stage 2";
- mm sizes from O4 (survey 2's "4³ cubes of 24 mm" is wrong: M2 input cells are 48 mm);
- the `use_post_norm` crash;
- the perlmutter caveat.

Reproduce with `probe_t21_shapes.py` (CPU, ~1 min).

### T2.2 design (card content; freeze sha256 before ANY confirmatory real-data number, Stage 0 included)
- **Mode.** CONFIRMATORY. The development subjects are the 5 burned ones in `verification/explorer_M3_r1_1/dev_subjects_BURNED.md`; exclude them.
- **Question.** In SwiFT ver11, trained by SimMIM from scratch on HCP REST1_LR, does connectome box grouping at M0 lower held-out-subject masked in-brain reconstruction NMSE versus PatchMergingV2 and versus a dispersion-matched FC-shuffle null? Everything else is identical: parameters, tokens, FLOPs, data order, masks, init, steps and seeds.
- **Changed element.** Only π at M0. Arms:
  - **E**: identity, bit-exact PatchMergingV2.
  - **C**: octant-local, size-8 boxes on correlation distance √(2(1−r)) of the train-split group FC of 12 mm cell means. Algorithm: dense-core seeding plus mean-linkage balanced growth. This is the named deviation from Song box covering, needed to keep box size 8; unequal boxes break token and parameter matching.
  - **S**: the same algorithm on FC permuted within exact-distance bins inside each octant, with a fixed seed.
  - Stage 0 adds G (same algorithm, Euclidean distance), R (random) and C_global (descriptive only).
  - Signal cells: ≥54/216 voxels. Filler cells use the same nearest-centroid rule in every arm.
  - Placement: Hungarian assignment inside the octant. Canonical child order: Hungarian match of members to the 8 octant offsets.
  - Graph and mask (median nvox) are built from train subjects only.
- **Data and split.**
  - Manifest: the .98 HCP REST1_LR set, pinned at freeze. Each file must pass a nibabel load with shape (91,109,91,1200) and finite values. Exclude the 5 burned subjects (by salted hash).
  - Split by salted-hash order into test 16 / val 8 / the rest train (≈59 if 83 are usable).
  - Preprocess with the SwiFT recipe (O7). Windows are 20 TRs: train stride 10, eval non-overlapping.
  - Val is used for training-health checks only. There is no model selection, no early stopping and no tuning.
- **Model and training (fixed).**
  - ver11 copied into `src/topic2_rgpool/ver11_copy.py`, with the source sha recorded and `use_post_norm=False`.
  - Config: E36, depths 2,2,6,2, heads 3,6,12,24, window 4,4,4,10, patch 6,6,6,1, mask patch 6,6,6,2, mask ratio 0.8.
  - Optimisation: bf16, bs16, 8,750 steps (140k samples), AdamW lr 1e-4, wd 0.05, cosine schedule with 5% warmup. Fix all of these in the card.
  - Seeds 0–4; the data-order seed and the mask seed (keyed by sample index) are shared across arms.
  - **Init pairing is not automatic.** Build every arm through ONE code path: the gather merge is constructed inside `RoPE4DBasicLayer` in place of PatchMergingV2, with E = identity index. The index is precomputed, so it consumes no RNG.
  - Never swap the module after construction, as my smoke script did for its timing-only purpose. A swap consumes extra RNG, gives C a different M0 init and breaks pairing.
- **Stage 0 (CPU mechanistic analysis, pre-registered).**
  - On test subjects, compute per-subject pca2 (primary; top-2 PCs with the basis fit on train) and r_mean (secondary) for E, C, S, G, R.
  - Contrasts C−E, C−S, C−G with a paired subject-bootstrap 95% CI (B=10,000, fixed seed).
  - Prediction: C>S. C vs E is open.
- **Stage 1 (GPU pilot).** 3 arms (E, C, S) × 5 seeds = 15 runs.
  - Primary metric: test-subject masked in-brain-voxel NMSE at the final step, on a fixed evaluation-mask set.
  - Improvements: I1 = (NMSE_E − NMSE_C)/NMSE_E and I2 = (NMSE_S − NMSE_C)/NMSE_S.
  - Inference: average over test subjects within each seed, then a t-interval over the 5 paired seed means (df 4). A within-seed subject bootstrap is secondary.
  - SESOI δ = 1% relative. This is recommended; the δ choice is the PI's decision before freeze.
- **Verdict mapping (G8).**
  - **keep**: I1 ≥ δ, lower CI(I1) > 0 and lower CI(I2) > 0.
  - **modify**: I1 survives but I2 does not. The gain is then not attributable to FC; mask or shape could explain it.
  - **stop (killed)**: upper CI(I1) < δ. This includes C worse than E.
  - **inconclusive**: anything else, reported with the CI width.
  - Software or integrity failure is reported as a failure, not as a null.
  - Joint Stage-0/Stage-1 reading, pre-registered:

    | Stage 0 (C vs E) | Stage 1 (C vs E) | Reading |
    |---|---|---|
    | C>E | C>E | supported |
    | C≤E | C>E | effect without the stated mechanism |
    | C>E | C≤E | mechanism not exploited by training |
    | C≤E | C≤E | killed |

- **Secondary outcomes (labelled secondary).**
  - NMSE learning curve at 25/50/75%.
  - Split-half (first vs last 600 TRs) fingerprinting top-1 among test subjects.
  - Centered PR of M0 outputs (descriptive; links to M2).
- **Seed count (costed option).** 5 seeds give df 4, t=2.78. 8 seeds × 3 arms = 24 runs ≈ 14 GPU-h, one node with 8 GPUs, df 7, t=2.36. Fix the count in the card before freeze.
- **Recommended option B: run Stage 1 regardless of Stage 0.** It costs ≈9–10 GPU-h, and T2.3 requires trained evidence.
  - Option A instead makes Stage 0 a go/no-go gate (GO iff lower CI of pca2 for C−E > 0 and for C−S > 0), saving ≈9 GPU-h of SwiFT-7T time.
  - Choose A or B **in the card, before Stage 0 runs**.

### T2.2 implementation and tests (`src/topic2_rgpool/`, a subpackage, so the top-level AST audit stays green; `tests/topic2_rgpool/`)

**Unit tests:**
1. Identity π equals copied PatchMergingV2 under `torch.equal`.
2. π is a bijection (sorted flatten == arange(4096)).
3. Each box sits in a single octant, and that octant equals its output cell's octant.
4. Permutation equivariance.
5. Gradient is nonzero in all 8 child slots of `reduction.weight`.
6. Parameter count and `FlopCounterMode` FLOPs are identical across arms (CPU tiny config).
7. π is unchanged when val/test data are perturbed (hash of π).
8. π is deterministic given train data and seed.
9. Arms share the same set of output cells.
10. The step-0 `state_dict` is equal across arms, excluding the `index` buffer (same seed).
11. The full E-arm model's forward is bit-identical to stock ver11 on the same weights and input. This catches layer-wiring errors that the module-level identity test cannot.

**Fixtures:**
- Stage-0 level: F+ requires C purity ≥0.95 and C−max(E,G) ≥0.1 held-out r. F− requires C not above G+0.02. NULL requires |r| ≤0.02 for every arm.
- Each fixture must fail on its targeted defect. Example: the periphery/max algorithm must fail F+ (P3).
- Training-loop fixtures on synthetic 4D volumes built from the same F+/F−/NULL cell generators: F+ ⇒ NMSE_C < NMSE_E, S; F− ⇒ C not better than S. Use short GPU or CPU runs and log them in the ledger.

### T2.3 execution
- **Env.** Build your own under `/scratch/iitp4/<worker-id>/` with uv; recipe in `verification/explorer_M3_r1_1/b300_build_env.sh`: torch 2.15.0+cu134, numpy 2.5.4, nibabel 5.4.2, monai 1.6.1, einops. Never use `~/envs/swiftllm`, and never list or touch `~/enigma_ocd`.
- **Data.** Preprocess HCP from the .98 staged copy read-only into your own dir as a single fp16 memmap.
- **Launch protocol.**
  - Run nvidia-smi immediately before every launch and use only idle GPUs; one node and up to 8 parallel runs is fine.
  - Write a ledger "started" row, then a "completed" row, under `flock results/gpu_ledger_2026-10-31.md.lock`.
  - M3 sub-cap: 12 GPU-h. Abort if the measured real-data throughput implies more.
- **Copy-back.** Copy logs and results back to `results/topic2/2026-11-01/` and write a dated result report. /scratch is wiped on VM stop.
- **If the pilot is not run** (option A gate stop, or a throughput or data failure): deliver the card, implementation, fixtures, Stage-0 result and the costed plan above, and say so explicitly (T2.3 escape clause).

## 5. Verification Method
- **T2.1.**
  ```
  cd /home/juke/git/00IITP-AI/verification/explorer_M3_r1_1
  PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B probe_t21_shapes.py
  ```
  Output begins with model prints; parse from the first `{`. Also `sed -n 41,88p;900,923p;1036,1070p /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py`.
- **Decoder.** `… -B probe_decoder_params.py` should give `decoder_type mlp`, spatial multiplier 48, the changed-voxel bbox [0,0,0,3]–[47,47,47,3], and 0 voxels outside it.
- **Gather merge.** `… -B probe_gather_merge.py` must report T1/T2 true, T3 8×true, T4 equal, and T5 three times true.
- **Synthetic fixtures.** `… -B probe_stage0_synthetic.py` (~10 s) must reproduce `.out.json`, including the `periphery-max` F+ failure.
- **HCP dev probes (B300 .98 CPU, read-only data).**
  ```
  cd /scratch/iitp4/explorer_M3_r1_1/probe && ../venv/bin/python -B probe_stage0_hcp_dev.py $(cat <local>/dev_subject_salt.txt)
  ```
  Then `… probe_stage0_hcp_dev_v2.py`, ~1 min each. Compare the `JSON_OUT` lines with the local `.out.json` files.
- **Ledger.** Check `grep explorer_M3_r1_1 /home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md`; the total should be 0.008 GPU-h.
- **C1.**
  ```
  cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
  ```
  Expected: rc 0.
- **Invalidated if:**
  - ver11 differs from sha `de132387…` or the perlmutter fork differs;
  - the .98 HCP set is replaced, or is shown not to be HCP open access;
  - effective real-data throughput, including data loading and eval, is below about 50 samples/s, which would push 15 runs plus fixtures above 12 GPU-h;
  - Stage-0 C−S is not positive on the confirmatory split, which would mean the FC signal itself is absent.
