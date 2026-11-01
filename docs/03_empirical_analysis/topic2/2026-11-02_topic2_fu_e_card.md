# Topic 2 follow-up E (FU-E) analysis card: downstream identifiability of the frozen r1 Stage-1 encoders

Status: **FROZEN** when its sha256 is written to `results/topic2/2026-11-02_fu_e/card_sha256.txt`. Later changes go in dated addenda `2026-11-02_topic2_fu_e_addendum_NN.md`; this file is never edited.
Author: worker_FU_E_r1, run tw-20261031-four-topics, workflow C, milestone FU_E (PI decision 7, r1 result report §7 option E). Written 2026-11-01 (UTC) / 2026-11-02 (KST).
Mode: **CONFIRMATORY**, one new experiment. It does not re-read the r1 verdict. The r1 verdict (`stop`: I1 +0.147 % [−0.068 %, +0.361 %] < δ 1 %) stands as recorded.

## 0. What was seen before freezing (disclosure)

- **All r1 results** (card, result report, addenda 01–05, verdict.json). They include that every r1 Stage-1 model reconstructs very little (test NMSE 0.986–1.000), and that run hcp_S_s2 stayed at the trivial solution (r1 addendum 04).
- **The three FU-E explorers' reports** (explorer_FU_E_r1_1/2/3 handoffs):
  - checkpoint integrity smokes (Slurm jobs 407 and 420), which **re-scored r1 TEST positions 0–1 for 2 checkpoints and reproduced the recorded r1 terms exactly** (relative error 0.0). These are r1 numbers, not an FU-E statistic;
  - encoder throughput, 0.004 s per 20-TR window per model;
  - staging counts: 103 complete REST1_LR files on B300 (r1's 88, the 5 burned development subjects and 10 later arrivals); no REST1_RL, REST2_LR or REST2_RL file staged;
  - open-access label counts (explorer-reported, not re-verified by this worker): 28 of the 103 staged subjects appear in the only open-access behavioural file found (a third-party n = 337 row subset of the HCP unrestricted table, banded age, gender). Of these 28, TEST 5, VAL 2, TRAIN 17, others ≤ 4. Explorer 1 reported 13 M / 15 F and age bands 22–25: 4, 26–30: 12, 31–35: 12;
  - synthetic probes (tiny random-init models only) that chose this design: a full-run z-score makes the two half-means exact negatives; subject mask outlines identify subjects; a mean-pooled readout misses planted FC identity while a second-order readout finds it.
- **This worker's own probe** (`verification/worker_FU_E_r1/cpu/probe_tiny_fixtures.{py,out}`): synthetic only, `tiny_test` random-init encoders, N = 12. cov2 Idiff on F+ was about +12 (null p95 about 4). On F− with the common mask it was about −0.6. On F− with subject masks it was about +48 (the anatomy confound). After seeing this, the F− gate was changed **before freezing** from a fixed |Idiff| < 1.0 bound to the one-sided comparison with its permutation null in §7.
- **B300 facts checked by this worker (counts only):**
  - all 15 checkpoints exist, 156,184,449 B each, and their sha256 values (§2) equal explorer_FU_E_r1_1's;
  - /scratch/iitp4/worker_M3_r1/hcp/subjects holds 88 subject directories;
  - the original split.json (sha256 `c13b5f21…`) has 64 TRAIN, 8 VAL and 16 TEST subjects;
  - perms_hcp.npz on B300 equals the repo copy (sha256 `ec05b796…`).

**No real-data FU-E statistic has been computed by anyone:** no embedding, similarity, Idiff or label join on real data.

## 1. Question, estimand, unit

**Q.** The r1 pilot found no reconstruction gain from connectome box grouping at M0 (`stop`). FU-E asks a second question of the same frozen encoders. Do arm C's encoders carry more subject-specific information than arm E's, measured as **within-run split-half identifiability** of held-out subjects?

**Why not cross-session fingerprinting.** Only REST1_LR is staged on B300, so Finn-style REST1-vs-REST2 fingerprinting is **untestable** here. This card measures identifiability between two halves of **one** run, separated by a 40-TR gap. It is not test–retest fingerprinting, and the values are not comparable with literature fingerprinting numbers.

**Estimand.** For each trained encoder (arm a, seed s): Idiff_a,s, computed on the 24 held-out subjects (§6).

**Contrasts** (unit = training seed, paired by seed, 5 seeds):
- **J1_s = (Idiff_C,s − Idiff_E,s) / Idiff_E,s** — practical claim, C vs stock PatchMergingV2.
- **J2_s = (Idiff_C,s − Idiff_S,s) / Idiff_S,s** — connectome-specific claim, C vs the distance-binned FC-shuffle arm S.

**δ = 0.01**, a relative 1 % change. This is decision 3's "1 %" applied to the relative contrast, which is the same form as r1's I1/I2. The capacity gate G2 (§7) keeps the denominators away from 0.

## 2. Encoders (read-only inputs on B300 b300-01, /scratch/iitp4/worker_M3_r1)

**Trained encoders.** The 15 r1 Stage-1 checkpoints `runs/hcp_{E,C,S}_s{0..4}/model_final.pt`. They are pinned by sha256 in `results/topic2/2026-11-02_fu_e/checkpoint_sha256_pins.txt` (recomputed 2026-11-01T15:36:36Z):

| run | sha256 |
|---|---|
| hcp_E_s0 | e670530783482529077a89222786d17754f769eebf0e5ebb63db45d827a9a635 |
| hcp_E_s1 | 5d861f67e5a6d849119d183265ca12ac368e39a44cf70f93fefa18fe39af4036 |
| hcp_E_s2 | 8d9b49616b7ce1b98e8238f1bc29d6e7c2935b662e1e6777d9e546cd5eaddea1 |
| hcp_E_s3 | fa50e76a65a84ef5071d153dea8b3e66f96ca6ec53a8294364f60a02094903b7 |
| hcp_E_s4 | c914b375553f25accdd19401b35bc4fb17d047b88391418a305a750992a8543f |
| hcp_C_s0 | 1fdf0ea92e5703a0795cea1fdc2b6c11fd5c39075e8d35c1c398fc3b5740d4e4 |
| hcp_C_s1 | 57581b9589feeadee59d290c7c8ea80ff1adf0fc022246197802dfabbd46f918 |
| hcp_C_s2 | ae106e7fc35c1f8774c31740afda6fea46b294fae05344cebbaa95202a7e353a |
| hcp_C_s3 | dca8ea3e65907106e853926e637ae29f5ef4209dcf4083e6989ab5006dc99d25 |
| hcp_C_s4 | f621f7ff76a181f999b0364712b30d587f6ac4cb86cea02b51fd6154fef5b8d6 |
| hcp_S_s0 | f2a1280ad46f5eb5e651cacc10edc1c6ae1a32eec7b7ca734cb2dc60915c76c6 |
| hcp_S_s1 | 073323cb97f5793a4c19440743d0c5c382f43c7569a2c23b0e614fa286706e4e |
| hcp_S_s2 | 44cd1a1467e4f354859029ba3e1c311e799a94e40e3036996f560ebf7db66f0d |
| hcp_S_s3 | 23f89222bdd831799536af69cb04a50196a6ea04ffedeb49a3d4447b2765bd26 |
| hcp_S_s4 | 0a60de5b60e97ce294fae9d374fb489c9ea67cd7f8ddc3db86cb30c0ceb60a6c |

**Loading.** `build_simmim(E36_d2262, perm_arm, seed=s, use_flashattn=True)` followed by `load_state_dict(strict=True)`. Here perm_arm is perms_hcp.npz key E, C or S_seed{s}.

**Seed-matched random-init twins** (descriptive only, §9). `build_simmim(E36_d2262, perm_arm, seed=s)` with no load. These are bit-identical to the r1 step-0 weights.

**hcp_S_s2** is a valid run (r1 addendum 04) and is included. A sensitivity analysis without seed 2 is descriptive only.

**Retraining is out of scope.** It would cost about 6.5 GPU-h against a 1.5 GPU-h cap.

## 3. G0 provenance gate (`src/topic2_fu_e/provenance.py`)

Checks for each of the 15 checkpoints:
- (a) the file exists;
- (b) its sha256 equals the pin;
- (c) its r1 run.json status is `completed`;
- (d) its single persistent buffer `layers.0.downsample.perm` hashes to the run.json `perm_sha256` **and** to the expected perms_hcp.npz array. Strict loading overwrites the builder's permutation, so this is the arm-identity guard;
- (e) it loads with strict=True;
- (f) re-scoring the 16 TEST positions with the frozen r1 `train.evaluate_hcp` (mask seed 7002, ratio 0.6, bf16, flash attention) reproduces the recorded per-subject `test_num` and `test_den` within a relative tolerance of 1e-5. The run.json test order must also equal split.json TEST.

Outcomes:
- Any file missing → **untestable_checkpoints_lost**.
- Any other check failing → **no_verdict**.
- The 33-file r1 code freeze must hold for every `src/topic2_rgpool` file imported. Otherwise → **no_verdict**.

## 4. Subjects and input preparation (`src/topic2_fu_e/prep.py`)

**Primary pool.** The 24 r1 held-out subjects: TEST 16 + VAL 8, in split.json list order. Records label them positionally only, as `test:k` and `val:k`.
- No encoder ever saw them: r1 training used only TRAIN windows, and VAL was used only for health curves.
- The 5 burned development subjects are not in the r1 split.
- The 10 files staged after the r1 manifest are **excluded**. They were never QC'd, and verifying the burned-subject exclusion would require sealed material.
- Relatives may straddle splits (HCP family structure is restricted), as in r1.

**Secondary pool** (descriptive only). TRAIN 64 (`train:k`). The encoders were trained on their full runs, so this is a memorisation reading.

**Data.** The r1 preprocessed files under `/scratch/iitp4/worker_M3_r1/hcp/subjects` (88 dirs): `bold_z_fp16.npy` (1200, 78, 96, 84) and `mask.npy`. They are read-only, and HCP data never leave B300.

**Input steps**, identical for every encoder:
1. Zero-pad to 96³ with the r1 rule (`data.pad96_torch`).
2. **Common mask** = logical AND of the 88 r1 subject masks. Every voxel outside it is 0.
3. **Halves**: TR [0, 580) and [620, 1200), a 40-TR gap, 29 non-overlapping 20-TR windows each.
4. Each half is **re-z-scored per voxel** over its own frames inside the common mask (population sd). Voxels with sd 0 are set to 0.

Step 4 is needed because the stored full-run z-score makes the two half-means exact negatives.

## 5. Readouts (`src/topic2_fu_e/readout.py`)

**Forward pass.** `forward_encoder(x, mask = 0)` in eval mode with bf16 autocast. This is the final normed encoder output z of shape (B, 288, 2, 2, 2, 20). It equals the last layer of `_forward_hook_embedding`, as the tests check.

**Primary: `cov2`.**
- Per window, center each of the 288 channels over its 160 tokens and scale it to unit norm.
- Take the 288 × 288 channel correlation matrix and keep its upper triangle: 41,328 values.
- Average over the 29 windows of a half.

**Descriptive: `pooled`.** The mean of z over all tokens and windows (288 values).

**Raw baseline: `cellfc`.**
- 12 mm cell means of the z-scored half, taken over common-mask voxels.
- Only cells with ≥ 54 of their 216 voxels in the common mask are used.
- Pearson FC over the half's 580 frames, upper triangle.

Every encoder gets byte-identical inputs: subject-outer, model-inner loop (`src/topic2_fu_e/pipeline.py`).

## 6. Metric and inference (`src/topic2_fu_e/ident.py`, `verdict.py`)

**Similarity matrix.** For a pool of N subjects, let A[i] be the half-0 vector and B[i] the half-1 vector.
- Each feature is z-scored across the 2N vectors; features with zero sd are dropped.
- Each vector is then standardised across features.
- R[i, j] = Pearson(A[i], B[j]).

**Metrics.**
- **Idiff = 100 × (mean diag R − mean off-diag R)**.
- Identification accuracy (top-1, both directions) is descriptive only. One flip at N = 24 is about 0.02, which is coarser than δ.

**Primary inference.**
- J1_s and J2_s (§1) from the trained cov2 Idiff of the main condition.
- Two-sided 95 % t interval over the 5 seeds (df 4), using r1 `stats.t_interval`.

**Permutation null of an R.** Idiff of R with its columns randomly reassigned: 1000 draws, seed 20261102. p95 = its 95th percentile.

**Power statement (fixed now).** The t interval half-width is 1.24 × SD_seed(J1). If the true J1 is 0, `stop` needs SD_seed(J1) below about 0.008. A larger between-seed spread makes **inconclusive** the likely honest outcome.

## 7. Gates (`verdict.py`; every gate is tri-state, and a missing or non-finite result is never a pass)

| gate | data | pass rule (strict where written) | on failure |
|---|---|---|---|
| **F+** `Fplus_ident` | synthetic, 24 subjects; r1 ellipsoid brain; each subject has its own planted octant-local 8-cell networks (r1 `plant_networks` / `cell_signals` "Fplus", seeds 4101..4124), the same in both halves; T = 1200, same pipeline; 15 trained encoders | every (arm, seed): Idiff **>** its null p95; and for every arm the seed-mean Idiff **≥ 2.0** | **inconclusive** (measurement capacity) |
| **F−** `Fminus_anat` | synthetic, 24 subjects with identical planted networks (label seed 4200) but subject-specific jittered ellipsoid masks (centre and radii ±2 voxels, jitter seed 4207); common mask = AND of these masks; 15 trained encoders | for every arm, the seed-mean Idiff **<** the seed-mean of its null p95 values | a would-be **keep** becomes **inconclusive** (bias flag). modify and stop are unaffected |
| **G2** real capacity | main condition | every seed: Idiff_E > p95 and Idiff_S > p95 (the denominators); and seed-mean Idiff_E ≥ 2.0 | **inconclusive** (measurement capacity) |
| **G3** data control | main condition, raw `cellfc` | Idiff_cellfc > its null p95 | **inconclusive** (data) |

The CPU tests (`tests/topic2_fu_e/test_fixtures_g6.py`) show the machinery on random-init `tiny_test` encoders:
- F+ passes;
- F− passes under the common mask, and **fails** when subject masks are kept (the targeted defect);
- iid noise stays at chance;
- the circular-shift surrogate removes planted FC identity.

## 8. Verdict rules, applied in this order (`verdict.classify`)

| order | condition | verdict |
|---|---|---|
| 1 | any of the 15 checkpoint files missing | **untestable_checkpoints_lost** |
| 2 | G0 integrity not established (any check in §3, or the code freeze); any governed extraction (main condition, 15 trained encoders) failed after one rerun, duplicated, malformed (not 24 × 24) or in a different subject order; any gate result missing; contrasts not computable | **no_verdict** (software or integrity failure ≠ scientific null) |
| 3 | F+ fails, G2 fails, or G3 fails | **inconclusive** |
| 4 | upper(J1) **<** δ | **stop**: an identifiability gain of C over E of ≥ 1 % is excluded |
| 4 | mean(J1) **≥** δ and lower(J1) **>** 0 and lower(J2) **>** 0 | **keep** |
| 4 | mean(J1) ≥ δ and lower(J1) > 0 and lower(J2) **≤** 0 | **modify**: the gain is not attributable to FC specificity |
| 4 | anything else | **inconclusive** |
| 5 | keep with F− failed | **inconclusive** (bias flag) |

**Notes.**
- Gate failures (step 3) are measurement or data failures. They are labelled **inconclusive in both this card and the code**, never no_verdict.
- The F− downgrade applies to **keep only**.

**What each verdict adds to r1.**
- **stop**: the grouping changed neither reconstruction nor the representations' held-out identifiability. This strengthens the r1 stop.
- **keep or modify**: a new finding that the representations differ despite an equal NMSE. It is never a re-reading of r1.
- **inconclusive**: the downstream question stays open.

## 9. Descriptive outputs (no decision rides on them)

- Init twins: Idiff per arm and seed, trained − init ("training value"), and init-encoder J1/J2.
- The pooled readout and identification accuracy.
- Sensitivity without seed 2 (df 3).
- Subject jackknife SE of the seed-mean J1.
- `surrogate` condition: each voxel circularly shifted within each half (seed 9000 + 100 × held-out position + half). Identical for every encoder; trained encoders and cellfc.
- `subjmask` condition: subject's own mask instead of the common mask (the anatomy confound); trained encoders and cellfc.
- `train64` condition: TRAIN subjects, trained and init encoders (memorisation reading). It stops if 60 min of job time have elapsed; the stop is recorded.
- Raw cellfc Idiff and accuracy for every condition.

## 10. Age / sex probe: **not run (untestable at δ)**

**The data cannot support it.**
- The only open-access label source found holds banded age (effectively 3 bands across ages 22–35) and gender for 28 staged subjects, of whom ≤ 7 are held out.
- An AUC on 24–34 subjects has a sampling SD of about 0.09–0.1, against δ = 0.01.
- Precise age, and any restricted HCP table (for example the HCP_1200 precise-age files referenced in SwiFT code), are forbidden.

**What is done instead.** No label is joined and no descriptive probe is run. A labelled probe needs a new card with an approved open-access label source.

## 11. Compute (C5) and abort rules

**Job layout.**
- One Slurm job on B300 `-p gpu -w b300-01 --gres=gpu:1 --time 75 min`, using the r1 project venv `/scratch/iitp4/worker_M3_r1/venv` read-only.
- Code is copied to `/scratch/iitp4/fu_e/code`; outputs go to `/scratch/iitp4/fu_e/` only.
- The order inside the job is: G0, F+, F−, held-out main / surrogate / subjmask, then TRAIN-64 (descriptive, deadline-guarded).
- The record is dumped after each stage, so a late failure keeps the governed stages.

**Budget.**
- Planned ≤ 1.25 GPU-h.
- Plus a synthetic-only smoke job (≤ 0.25 GPU-h, run before freezing, no subject data).
- Plus the explorers' 0.015 GPU-h.
- The FU-E cap is 1.5 GPU-h. A rerun is launched only if it fits inside the remaining cap. Otherwise the result is no_verdict and is reported as such.

**Submission rules.**
- Before every submission, `squeue` is checked for `g3t-G-E0-*` jobs, and submission waits while any is pending or running.
- Ledger rows marked started and completed are written under flock, with GPU-h counted from sacct elapsed time × GPUs.

**Outputs.**
- Only the aggregate record leaves B300: similarity matrices indexed by position, provenance and timings.
- The r1 B300 ID scan (`scripts/topic2_id_scan.py`, names held in memory) is run on the copied-back FU-E outputs.

## 12. Frozen inputs

**Code.** The sha256 of every file under `src/topic2_fu_e/`, `scripts/topic2fu_e_*.py` and `tests/topic2_fu_e/` at freeze, in `results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt`. The r1 code is imported read-only and pinned by `results/topic2/2026-11-01/code_sha256_at_freeze.txt`.

**Data and pins.** The checkpoint pins file, and r1 perms_hcp.npz (sha256 `ec05b796a450d78b646172cb84031f04758fef6965e085db87a75c6b620f2b34`). The original split.json (sha256 `c13b5f21b67f456fb39a258d7f8279b06a69b061f79de627ed884a5923140262`) is checked on B300 by the job.

**Constants.**
- δ 0.01; floors F+ 2.0 and G2 2.0; null 1000 draws with seed 20261102; rescore rtol 1e-5.
- Half spec 580 / 40 / 580 at window 20; fixture seeds F+ 4100 (subjects 4101..4124) and F− 4200.
- Surrogate seed 9000 + 100·position + half.
