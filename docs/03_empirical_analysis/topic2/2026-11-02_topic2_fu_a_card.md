# Topic 2 follow-up A (FU-A) analysis card: connectome boxes vs cubes at M0 with the 12 mm cell-mean field as the SimMIM signal

Status: **FROZEN** when its sha256 is written to `results/topic2/2026-11-02_fu_a/card_sha256.txt`. Later changes go in dated addenda (`2026-11-02_topic2_fu_a_addendum_NN.md`); this file is never edited.
Author: worker_FU_A_r1, run tw-20261031-four-topics, workflow C, milestone FU_A (ACCEPTANCE addendum F1–F3), 2026-11-02 (KST).
Mode: **CONFIRMATORY follow-up** under PI decision 7 (result report §7 option A of `2026-11-01_topic2_result_report.md`). It is a NEW experiment. The r1 verdict (`stop`, I1 +0.147 % [−0.068 %, +0.361 %] < δ 1 %, card `2026-11-01_topic2_card.md`) stays exactly as recorded; nothing here re-reads it.
Governing r1 documents reused by reference: card `2026-11-01_topic2_card.md` (sections cited as r1 §n), architecture note `2026-11-01_topic2_architecture.md`, addendum 05 (positional tokens).

## 0. Data seen before freezing (disclosure)

Real data, all from r1 or from TRAIN-only design statistics; **no FU-A model was trained or evaluated on real data before the freeze**:
- All r1 results (result report; verdict stop; every arm reconstructs ≈ 1 % of masked per-voxel variance, NMSE 0.987–0.992).
- **r1 Stage 0 was computed on exactly the representation FU-A trains on** (the 12 mm cell series of the same 16 TEST subjects, `results/topic2/2026-11-01/stage0_hcp.json`): C − E held-out within-box r +0.004 [0.0005, 0.0074] (11/16 subjects); C − E pca2 −0.052 [−0.053, −0.050] (0/16). pca2 is the share a linear 8C→2C reduction can keep. **This prior predicts `stop` or `inconclusive` for FU-A**, and that is the pre-registered prediction (§8.4).
- TRAIN-only design statistics computed by this worker on B300 (Slurm job 492, CPU, 64 TRAIN subjects, no model, no VAL/TEST subject read; formulas written in the worker's progress log at 15:32Z before computing): see §2.3 and `results/topic2/2026-11-02_fu_a/design_stats_train.json`.
- Reported by other agents and not re-derived here: challenger_M3_r1_2 signal check on 4 TRAIN subjects (voxel R² on its own cell mean 0.047; cell-mean lag-1 autocorrelation 0.33); explorer_FU_A_r1_2 CPU probe on 8 TRAIN subjects (median cell lag-1 autocorrelation 0.243; NMSE of copying the nearest visible frame 1.49; of a 2-feature least-squares predictor 0.864/0.875). These are arm-independent.
- Other follow-up teams (FU-B…FU-E) ran smokes on the r1 voxel target or on synthetic data. This worker has seen no real-data number for the cell-mean target from any model.

Synthetic data: the CPU fixtures (tests), the FU-A fixture partitions and the fixture target scale (§7) were built before freezing. Throughput smokes by explorers (Slurm jobs 403 and 427, synthetic only) measured ≈ 0.18 s per step for this target, and at most 1.04–1.08× aggregate gain from packing several runs on one GPU.

**Nothing in this card is changed after any result.** No hyperparameter, budget or threshold is tuned.

## 1. Question, estimand, unit

**Q.** Train SwiFT ver11 E36 from scratch with SimMIM on HCP-YA REST1_LR exactly as in r1, but let the signal that SimMIM sees and reconstructs be the 12 mm cell-mean field (§2) instead of the 2 mm per-voxel BOLD. Does grouping the stage-0 cells into connectome boxes at M0 (arm C), instead of PatchMergingV2's 2×2×2 cubes (arm E), lower the held-out masked in-brain NMSE? This asks whether the r1 null was a sensitivity limit of a noise-dominated target (r1 NMSE ≈ 0.99).

- **Practical claim.** I1 = (NMSE_E − NMSE_C) / NMSE_E.
- **Connectome-specific claim.** I2 = (NMSE_S − NMSE_C) / NMSE_S (S = the r1 distance-binned FC-shuffle null).
- **Unit of inference.** The training seed; NMSE pooled over the 16 TEST subjects × 60 evaluation windows per seed (§6). Baseline = arm E (stock ver11).

## 2. The single changed factor relative to r1: the SimMIM signal

### 2.1 Definition
For a subject with per-voxel temporally z-scored BOLD z (r1 §4 preprocessing, unchanged), padded to 96³, and brain mask b (r1 mask), the 16³ grid of 6³-voxel cells c (cell index (d·16 + h)·16 + w):
- m_c,t = mean of z over the subject's brain voxels of cell c at frame t (= frozen `src/topic2_rgpool/data.py` `cell_means`, stored for every subject on B300 as `cellmeans.npy`, float32); n_c = number of the subject's brain voxels in c; m_c,t = 0 when n_c = 0.
- **y_v,t = κ · m_c(v),t for every brain voxel v, 0 outside the brain**, with one global constant κ (§2.3).
- y is both the SimMIM **input** and the **reconstruction target** (SimMIM reconstructs its input). Implementation: `src/topic2_fu_a/target.py` (`block_mean_volume`, `broadcast_cells`), `src/topic2_fu_a/sources.py` (`CellHCPSource` reads `cellmeans.npy` + `mask.npy`).
- Because y is constant on each (cell, frame) and the SimMIM mask unit is one cell × 2 frames (r1 §5), the frozen masked in-brain NMSE of y equals the **n_c-weighted cell-level NMSE** Σ n_c (p̄_c,t − y_c,t)² / Σ n_c y_c,t² plus the within-cell spread of the prediction (which the optimum sets to 0). κ cancels in the NMSE. Equivalently, FU-A's NMSE is r1's NMSE of the block-mean projection of the r1 target: the within-cell voxel residual (the part that made r1 noise-dominated) is removed and nothing else changes.

### 2.2 Everything else is r1, byte for byte
FU-A calls the frozen r1 loop `src/topic2_rgpool/train.py` `run()` itself, unchanged and pinned (`results/topic2/2026-11-01/code_sha256_at_freeze.txt`, 33/33). `src/topic2_fu_a/run.py` rebinds the loop's two source classes (`HCPSource`, `FixtureSource`) to the FU-A sources for the duration of a run and restores them afterwards. The frozen loop uses the source tensor as model input and as target, so input and target change together and nothing else does: model `E36_d2262` (38.7 M parameters), M0 permutations (`results/topic2/2026-11-01/partitions/perms_hcp.npz`, sha256 `ec05b796…2b34`, keys E, C, S_seed{s}), weight-init / window-order / training-mask seeds (s, 1000+s, 2000+s), evaluation-mask seeds 7001 (val) / 7002 (test), windows (20 TRs; training stride 10; evaluation non-overlapping), AdamW, schedule, budget 8,750 steps × batch 16 = 140,000 samples, bf16, gradient clipping, throughput abort, evaluation code.
Every run records a patch-constancy check of its first batch (`fua_checks`; must be 0 up to float rounding) and the FU-A code hashes; tests show that a wrapper that failed to rebind would be caught (`tests/topic2_fu_a/test_run.py`).

### 2.3 Design statistics (TRAIN only; fixed before freezing)
From the 64 TRAIN subjects (`design_stats_train.json`): Q = Σ n_c Σ_t m² / Σ n_c T = **0.030780** (the cell-mean field holds 3.08 % of the per-voxel variance; r1's models explained ≈ 1.1 %); **κ = 1/√Q = 5.699892** (so y has unit mean square over TRAIN brain voxel-frames, like the r1 target); noise floor share NF = Σ #{c: n_c > 0}·T / Σ n_c Σ_t m² = **0.20851** (the share of the cell-mean energy that independent unit-variance voxel noise would contribute; an upper bound under that model); descriptive cell lag-1 autocorrelation median 0.253, mean 0.313.

### 2.4 Alternatives considered and rejected before freezing
- **Gaussian-smoothed 2 mm BOLD** (the other option named in result report §7): under a pure null on the real TRAIN mask with the real E/C/S permutations it gives cubes a spurious advantage (E−C within-box r +0.043 at FWHM 6 mm, +0.128 at 12 mm, against the entire real Stage-0 C−E of +0.004) and leaks masked-cell content into visible neighbours (correlation 0.085 / 0.186), because ver11 masks whole cell × frame tokens (explorer_FU_A_r1_1 probe p02, synthetic iid data). It also adds a free FWHM. Rejected.
- **Per-cell re-z-scoring** of the cell means: a second change (re-weights low-coherence, noise-rich cells). Rejected; one global κ.
- **2 mm input with a 12 mm target**: adds a denoising objective (two changes) and needs a forked loop. Rejected.

## 3. Arms
Identical to r1 §3 and the same files: E (identity), C (balanced greedy box growth on the TRAIN group FC of the 12 mm cell means), S (same builder on a distance-binned FC surrogate, surrogate seed = training seed s). The partitions were built in r1 from the TRAIN cell means, i.e. from the very representation FU-A trains on (FC is invariant to κ).

## 4. Data and split (C4, C6)
- HCP-YA S1200 Open Access REST1_LR, public under PI decision 2 (HCP Data Use Terms; no redistribution, no re-identification). The r1 preprocessed subjects exist only on B300 node b300-01 (`/scratch/iitp4/worker_M3_r1/hcp/subjects/`, 88 QC-passed subjects, the 5 burned development subjects already excluded in r1). They are read in place; nothing is copied off B300 except aggregate run records.
- **Positional view** (`scripts/topic2fu_a_prepare_b300.py`): `/scratch/iitp4/fu_a/data/subjects/hNN/{cellmeans.npy, mask.npy}` symlinks, hNN = position in the r1 manifest's subject list (sorted by content sha256; addendum 05 token map). Checks run before freezing, booleans only: manifest order = sorted directory names; 88 subjects; manifest records 5 burned exclusions, 88 QC passes, 0 failures; the repo split (`results/topic2/2026-11-01/split.json`, positional, sha256 `cc521b08…c75a`) equals the r1 original split (sha256 `c13b5f21…0262`, sealed) mapped through the token map; lists disjoint, 64/8/16. Original directory names are never printed or written.
- Split, VAL use (health check and premise M only; no model selection, no early stopping) and the HCP family-structure limitation are inherited from r1 §4.

## 5. Model and training
r1 §5 unchanged (§2.2). Script `scripts/topic2fu_a_train.py` (r1 arguments and defaults plus `--constants results/topic2/2026-11-02_fu_a/fua_constants.json` and `--card-sha256`). One run = one arm × one seed on one B300 GPU under Slurm.
A run is a software failure if it hits the hard timeout (3,300 s), a non-finite loss, the throughput abort (projected > 0.75 h at step 200), or a crash. A failed run is rerun once with the identical command only if the projected GPU total stays within the cap (§10); the failure stays in the ledger. A second failure, or no budget for the rerun, leaves the run missing and the verdict is `no_verdict`.

## 6. Primary outcome
For each TEST subject i and run (arm, s): num_i = Σ over the 60 evaluation windows of Σ over masked in-brain voxels of (ŷ − y)²; den_i = Σ y² over the same voxels (frozen `evaluate_hcp` / `masked_sq_terms`). NMSE_arm,s = Σ_i num_i / Σ_i den_i. Predicting 0 gives exactly 1.

## 7. Synthetic fixtures (G6), adapted to the new target

### 7.1 Noise calibration and fixture partitions (built before freezing)
The r1 fixtures had almost no voxel noise (0.1), so their cell means were ≈ pure signal. FU-A's target is a cell mean whose noise share is set by the TRAIN data, so the fixtures get voxel noise σ_v chosen to give the same noise share of the cell-mean energy: the fixture signal has unit variance per cell, so its share is σ_v² N / (Σ nvox + σ_v² N); equating it to NF = 0.20851 on the fixture ellipsoid gives **σ_v = 6.545925** (`src/topic2_fu_a/calib.py`). Under this calibration the fixture cell-mean lag-1 autocorrelation is ≈ 0.5 × (1 − noise share) ≈ 0.38–0.40 (r1 fixture AR(1) 0.5), against the real median 0.25 / mean 0.31.
Fixture partitions `results/topic2/2026-11-02_fu_a/partitions/perms_fua_{Fplus,Fminus}.npz` (`scripts/topic2fu_a_build_fixture_perms.py`): the r1 fixture recipe (planted labels seed 31; generator seeds 41/42; 20 fixture-train samples × 400 frames; frozen `partition.build_perm`) with the FC estimated from the FU-A signal of the noisy fixture-train samples (block means of the noisy voxel volumes), i.e. the path the gate trains on. Fixture target scale κ_fix = 1/√Q_fix from the same samples. Values (`partitions/fixture_build.json`): κ_fix = 0.970840 (Q_fix 1.06097); F+ purity against the planted networks C 1.00, E 0.31, S_seed0 0.25, G 0.25, R 0.25. The realized fixture signal variance is 0.80 rather than the nominal 1, so the realized noise share of the fixture cell-mean energy is 0.248 (> NF 0.209): the fixtures are slightly noisier than the calibration target, which is conservative for F+. CPU Stage-0 numbers at σ_v on held-out fixture samples (`verification/worker_FU_A_r1/probe_stage0_fixture_numbers.out.json`, same seeds as the tests): F+ within-box r E 0.071, C 0.338, G 0.059; F− r E 0.486, C 0.416, G 0.421.

### 7.2 CPU Stage-0 fixtures (`tests/topic2_fu_a/test_fixture_stage0.py`; held-out fixture samples at σ_v, through the FU-A path)
| fixture | pass condition (r1 §7.1 thresholds) |
|---|---|
| F+ planted networks | pinned C purity ≥ 0.95; held-out within-box r of C ≥ max(E, G) + 0.10 |
| F− smooth field | r_C ≤ r_G + 0.02 and r_C ≤ r_E + 0.02 |
| NULL iid | \|held-out r\| ≤ 0.02 in every arm |
| premise (voxel level) | with the same stream and noise, single voxels keep < 25 % of the cell-level C − E advantage |

### 7.3 Training-loop gate (full budget, B300)
**Runs.** F+ stream (r1 generator, labels from `perms_fua_Fplus.npz`), arms **E and C, seed 0**, with the §5 budget and settings; test NMSE over 16 × 32 fixed synthetic windows (eval seed 7002; frozen `evaluate_fixture`). 2 runs.
**F+ passes** iff (E − C)/E ≥ δ. If F+ fails, **Stage 1 is not run** and the verdict is `inconclusive` (measurement capacity at realistic noise), with a costed plan.
**Deviation from r1 §7.2 (budget, declared here):** r1 ran F+ and F− × E/C/S × seeds {0, 1} (12 runs ≈ 5.2 GPU-h). Under the FU-A cap (§10) only 2 gate runs fit beside the 15 Stage-1 runs. Not run: F+ arm S (C-vs-S capacity) and F− arms E, C (bias check). Consequences, fixed now: a result that would be **keep** needs F+ C-vs-S ≥ δ **and** F− passed; one that would be **modify** needs F− passed (F− passes iff (E − C)/E < δ on seed 0). Without these runs such a result is `inconclusive` (pending gates). They can be run later only under a raised cap, with exactly these definitions (runs `Fplus_S_s0`, `Fminus_E_s0`, `Fminus_C_s0`; F− partitions `perms_fua_Fminus.npz`, S key `S_seed0`). A stop result needs neither (r1 rule: F− only flags a spurious C advantage).

## 8. Inference and verdict (`src/topic2_fu_a/verdict.py`, `scripts/topic2fu_a_verdict.py`)

### 8.1 Constants
δ = 0.01 (1 % relative NMSE reduction; PI decision 3), a frozen constant with no command-line override. Primary inference: two-sided 95 % t interval (df 4) over the five seed-level I1_s and I2_s, paired by seed (frozen `stats.t_interval`, `stats.relative_gain`). Secondary: hierarchical bootstrap (B = 10,000, seed 0; frozen `stats.hierarchical_bootstrap`), descriptive only.

### 8.2 Premise check M
The option's premise is that the target is not noise-dominated. **M passes iff the seed-mean final VAL NMSE of arm E ≤ 1/(1 + 10δ) = 0.90909**, i.e. δ is at most 10 % of arm E's explained variance. A `stop` requires M; if M fails, a would-be stop is `inconclusive (premise)`. keep/modify do not require M (they are guarded by the gates).

### 8.3 Verdict rules, applied in this order
| step | condition | verdict |
|---|---|---|
| 0 | a run record lacks `fua_target = cell12_kappa` or this card's sha256, or is duplicated (e.g. an r1 voxel-target record) | no_verdict |
| 1 | F+ gate run missing or not completed (after the one permitted rerun) | no_verdict |
| 2 | F+ completed and (E − C)/E < δ | **inconclusive** (measurement capacity), whatever Stage 1 shows |
| 3 | Stage 1 (E, C, S × seeds 0–4) has a missing, failed or extra run, a test-subject order that differs between runs, or Σnum/Σden ≠ test_nmse | no_verdict |
| 4 | upper bound of I1 < δ | **stop (killed)** if M passes, else inconclusive (premise) |
| 4 | mean I1 ≥ δ, lower bound of I1 > 0, lower bound of I2 > 0 | **keep** (subject to step 5) |
| 4 | mean I1 ≥ δ, lower bound of I1 > 0, lower bound of I2 ≤ 0 | **modify** (subject to step 5) |
| 4 | anything else | inconclusive |
| 5 | keep or modify with F− failed (bias flag) or F− not run; keep with F+ C-vs-S not run or < δ | inconclusive; a started-but-incomplete gate run → no_verdict |
| 6 | stall: any Stage-1 run with final VAL NMSE ≥ 0.999 → drop that seed from every arm and recompute steps 4–5; fewer than 3 seeds left, or a different category | inconclusive (stall-sensitive) |

Boundaries (pinned by tests with exactly representable values): F+ gains pass at ≥ δ; F− passes at < δ (strict); stop at hi < δ (strict); keep/modify at mean ≥ δ and lower bounds > 0 (strict); M at ≤ 0.90909; stall at ≥ 0.999.
**Deliberate deviation from r1 §7.2/§8:** an F− failure downgrades **keep and modify** (r1: keep only), because both claim C < E in NMSE; a stall clause is added (r1 hcp_S_s2 stalled at 1.0000). The verdict code is new and table-driven; tests kill 31 named mutants including the r1 defect classes (missing gate counted as pass, failed runs counted, F+ failure reported as no_verdict, ≥ vs > boundaries, F− handling of modify).

### 8.4 Pre-registered prediction and joint reading with r1
Prediction (from §0): `stop` or `inconclusive`. Reading of each FU-A outcome next to the r1 stop (which is unchanged in every row):
| FU-A verdict | reading |
|---|---|
| stop | the r1 null extends to a target that is not noise-dominated: at M0, connectome boxes are worth < 1 % NMSE even on the 12 mm cell-mean field |
| keep / modify | not reachable without the unfunded gates (§7.3); would mean r1's stop reflected a target-sensitivity limit |
| inconclusive (capacity) | F+ failed at realistic noise: this pipeline cannot resolve δ on a planted effect; no statement about HCP |
| inconclusive (premise) | the cell-mean target is still noise-dominated for this model and budget (arm E explains < 10 δ) |
| inconclusive (other) / no_verdict | as labelled; software failure is not a scientific null |

## 9. Secondary and descriptive outcomes (no decision rides on them)
Validation learning curves; explained variance 1 − NMSE per arm; absolute ΔNMSE; hierarchical bootstrap; per-subject seed-mean NMSE; stall sensitivity even when it does not change the verdict; fixture purity and Stage-0 fixture numbers. No new Stage 0 is run (r1 Stage 0 already scored this representation, §0).

## 10. Compute budget, sequencing and abort rules (C5)
- **Hardware.** B300 b300-01 only (the only node with the data), Slurm partition `gpu`, one GPU per run (`--gres=gpu:1 -c 8 --mem=64G -t 01:00:00`, inner `timeout 3300`), `sbatch` arrays (`scripts/topic2fu_a_submit.py`), venv `/scratch/iitp4/fu_a/env/venv`. Before every submission the B300 sharing rule is applied (no submission while any `g3t-G-E0-*` job is pending or running). Ledger rows (start and close, Slurm job id, sacct elapsed) under flock.
- **Cap.** FU-A 8 GPU-h (PI decision 7), counting the FU-A explorer smokes already used (jobs 403 and 427: 0.130 GPU-h). Measured r1 cost: 1,506–1,655 s per run (mean 1,555 s ≈ 0.43 GPU-h); planned 2 + 15 = 17 runs ≈ 7.4–7.9 GPU-h including the explorer smokes. The r1-shaped gate (12 runs) or any 2-seed gate would exceed the cap; packing runs on one GPU gains ≤ 8 %.
- **Sequencing.** Gate wave (2 runs) first. Stage 1 (15 runs, ≤ 5 concurrent) is launched only if F+ passes **and** 0.130 + (gate GPU-h used) + 15 × (largest gate per-run GPU-h) ≤ 8.0. Otherwise Stage 1 is not launched: verdict `no_verdict` (not run: budget) with a costed plan.
- **Copy-back.** Before anything leaves B300, a count-only scan for the 88 r1 subject tokens and the HCP directory names (`scripts/topic2fu_a_token_scan.py`) must report 0 hits. Run records come back; checkpoints are not saved.

## 11. Frozen inputs (receipts in `results/topic2/2026-11-02_fu_a/`)
- `card_sha256.txt`: this card, `fua_constants.json`, `design_stats_train.json` (sha256 `694c31ca…1a12`, equal to the file written by Slurm job 492 on B300), `partitions/perms_fua_Fplus.npz`, `partitions/perms_fua_Fminus.npz`, `partitions/fixture_build.json`, and the r1 inputs reused (`perms_hcp.npz`, positional `split.json`).
- `code_sha256_at_freeze.txt`: every file of `src/topic2_fu_a/`, `scripts/topic2fu_a_*.py`, `tests/topic2_fu_a/`; the r1 pins (`results/topic2/2026-11-01/code_sha256_at_freeze.txt`) must still pass.
- B300 environment: `scripts/b300_env/build_env.sh` + `lock.txt` (torch 2.15.0+cu134), rebuilt at `/scratch/iitp4/fu_a/env/venv` (Slurm job 489).
