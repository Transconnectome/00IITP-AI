# Topic 2 follow-up B (FU-B) analysis card: 4× training budget at E36, arms E/C/S, 5 seeds

Status: **FROZEN** when its sha256 is written to `results/topic2/2026-11-02_fu_b/card_sha256.txt`, before any FU-B real-data run (the 4× F+ gate included). Later changes go in dated addenda `2026-11-02_topic2_fu_b_addendum_NN.md`; this file is never edited.
Author: worker_FU_B_r1, run tw-20261031-four-topics, workflow C, milestone FU_B. Date 2026-11-02 (KST); written 2026-11-01 ~15:3x UTC.
Mode: **CONFIRMATORY follow-up** under PI decision 7 (result report `2026-11-01_topic2_result_report.md` §7, option B). One manipulated factor relative to the r1 card: the training budget.
Parent card: `2026-11-01_topic2_card.md` (r1, sha256 `c9bfc60a…41f5`). Everything not stated here is as in the r1 card, and is reused by importing the frozen r1 code (`src/topic2_rgpool`, pinned by `results/topic2/2026-11-01/code_sha256_at_freeze.txt`).
The r1 verdict (**stop**, I1 +0.147 % [−0.068 %, +0.361 %] < δ 1 %) stays as recorded. FU-B is a new experiment; its verdict sits beside the r1 verdict and never re-reads it.

## 0. Data seen before freezing (disclosure)

- **All r1 results are known** to the author: the r1 verdict, the per-seed test NMSE, the val curves (r1 report §3), the fixture-gate numbers (§2.2), the stalled `hcp_S_s2` run and addenda 01–05.
- **FU-B explorer smokes (Slurm jobs 402, 413, 419; 0.14 GPU-h)** measured only:
  - throughput of the 35,000-step configuration (projected 1.70–1.71 h per run, about 91 samples/s), peak GPU memory (≈145–152 GiB of 268), checkpoint size;
  - that 300-step partial runs at the **r1 8,750-step schedule** reproduce the r1 training-loss log lines at steps 100 and 200 bit-identically (an r1 number, not an FU-B outcome);
  - that the per-subject test denominators through the positional view equal r1's (weight-independent);
  - the learning rate at step 100 of the 35,000-step schedule.
- **FU-B worker smoke before this freeze (Slurm job 490, 0.07 GPU-h; `verification/worker_FU_B_r1/smoke_490_fetch.txt`)**, through the FU-B wrapper and the positional view: test denominators equal r1's exactly (max relative difference 0.0); 201-step anchors of hcp_E_s0, hcp_C_s0 and Fplus_E_s0 at the **r1** schedule reproduce r1's loss lines at steps 100 and 200 exactly (difference 0.0); with the FU-B defaults the run projects 1.69 h and the step-100 learning rate equals 2e-4 · 100/1750. Positional view check (`view_check.json`): 88 subjects, 176 hard links, split lists equal, 0 r1 files modified.
- No FU-B training was run past step 300, no FU-B val or test number exists, and no FU-B contrast was computed.
- **Prior expectation: stop.** The r1 val curves were still slowly decreasing at step 8,750 (E 0.9912 → 0.9910 between 6,562 and 8,750), which is the reason this option exists; the explorer operating-characteristic probe (r1 seed noise) gives P(stop) ≈ 1 if the true I1 at 4× stays ≤ 0.15 %.

## 1. Question, estimand, unit

**Q.** Is the r1 null explained by under-training? With 4× the training samples (560k instead of 140k) and everything else as in r1, does grouping the 12 mm stage-0 cells into connectome boxes at M0 (arm C), instead of PatchMergingV2's 2×2×2 cubes (arm E), lower the held-out masked in-brain NMSE by at least δ?

- **Practical claim (C vs E):** I1 = (NMSE_E − NMSE_C) / NMSE_E.
- **Connectome-specific claim (C vs S):** I2 = (NMSE_S − NMSE_C) / NMSE_S, S = same box builder on the distance-binned FC surrogate.
- **Unit of inference:** the training seed; NMSE_arm,s pooled over all test subjects and evaluation windows (r1 card §6).
- **δ = 0.01** (1 % relative NMSE; PI decision 3).

## 2. The single change: training budget, and how the longer run is handled

| item | r1 | FU-B |
|---|---|---|
| steps × batch | 8,750 × 16 = 140,000 samples | **35,000 × 16 = 560,000 samples** (≈ 73.5 passes over the 7,616 training windows) |
| learning-rate schedule | frozen `lr_at(step, steps, 2e-4, 0.05)` | **the same frozen function with steps = 35,000**: linear warmup over 5 % = 1,750 steps, cosine decay to 0 at step 35,000, peak 2e-4. One schedule, no restart. |
| optimiser | AdamW (0.9/0.999), wd 0.05, clip 1.0, bf16 | unchanged |
| val points | 25/50/75/100 % of steps | **8,750 / 17,500 / 26,250 / 35,000** (same quarters) |
| test | once, at the last step | once, at step 35,000 |
| throughput abort | `--max-run-hours 0.75` (default) | **`--max-run-hours 2.2`** (the default would abort every 35,000-step run at step 200) |

**Learning-rate handling (stated limitation).** The peak, warmup fraction and decay shape are kept, not re-tuned for the longer run. This isolates the budget, but the r1 recipe may be sub-optimal at 4×; FU-B therefore answers "more samples with the same recipe", not "best achievable at 560k". The step-8,750 val point of FU-B is **not** a replicate of r1's endpoint: there the FU-B learning rate is still 1.79e-4, whereas r1 had decayed to 0.

**Same data stream.** The window-order (1000+s), training-mask (2000+s) and init (s) streams do not depend on the number of steps, so the first 140k samples of every FU-B seed are exactly r1's samples in r1's order with r1's masks (only the learning rate differs). Continuing from r1's final checkpoints was rejected: they hold no optimiser state, their schedule has decayed to 0, and it would be a different experiment.

**Checkpoint cadence.** No intermediate checkpoint and no resume (the frozen trainer has none; B300 Slurm has PreemptMode OFF and the gpu partition allows 2 days, against ≈1.7 h runs). Final weights are saved with `--save-model` and stay on B300 only (`/scratch/iitp4/fu_b/runs/*/model_final.pt`; never copied back; usable by a later FU-E-style probe). An interrupted run is a software failure (§10) and is rerun from scratch; the frozen trainer is deterministic given its seeds, so a rerun reproduces the same computation up to GPU non-determinism.

Nothing else changes: model E36_d2262 (38,712,096 parameters), SimMIM mask (ratio 0.6, 1 cell × 2 frames), loss, eval masks (7001 val, 7002 test), arms, partitions, data, split.

## 3. Arms (unchanged from r1 §3)

E (identity π, stock PatchMergingV2), C (connectome boxes on the train-split group FC), S (same builder on the surrogate FC; surrogate seed = training seed). Partitions are the r1 files, not rebuilt:
- HCP: `results/topic2/2026-11-01/partitions/perms_hcp.npz` (sha256 `ec05b796…2b34`), keys `E`, `C`, `S_seed{s}`;
- F+ fixture: `…/perms_Fplus.npz` (sha256 `b288a5ad…796b`), keys `E`, `C`, `S_seed0`, `labels`.

Seeds s = 0–4 for Stage 1; seed 0 for the gate.

## 4. Data and split (C4, C6)

- **Data:** the r1 preprocessed HCP-YA S1200 Open Access REST1_LR tensors (88 subjects; 5 explorer development subjects excluded by r1), on B300 node b300-01 only (`/scratch` is node-local; the other nodes hold no HCP data). Public under PI decision 2; read-only; never redistributed; nothing but aggregate run records leaves B300. No re-preprocessing (it would need the sealed salt and recreate unsalted tokens).
- **Positional view (C4).** The r1 tensors sit in directories named by the old unsalted content tokens, and the frozen trainer writes the data-directory names into `run.json` (`test_pseudonyms`). FU-B therefore trains only through a hard-link view `/scratch/iitp4/fu_b/hcp/subjects/hNN/` built by `scripts/topic2fu_b_make_view.py` from the r1 B300 manifest order (position i → `h%02d`, the r2 sanitize rule). The script prints counts and booleans only, never a token.
- **Split:** the repo's sanitized `results/topic2/2026-11-01/split.json` (sha256 `cc521b08…c75a`): the same 64/8/16 assignment and order as r1, tokens renamed. Before any training the view script must confirm on B300: sanitized manifest positional and in order; the r1 original split mapped by position equals the repo split for train, val and test; disjoint; 0 r1 data files modified after 2026-11-01T03:10Z; 0 conflicting links. Any failure stops FU-B before the gate.
- Family structure (restricted data) is unavailable, as in r1.

## 5. Model, training and run records

Frozen `scripts/topic2_train.py` / `src/topic2_rgpool/train.run`, launched by the FU-B in-job wrapper `scripts/topic2fu_b_run.py`, which only (a) resolves (source, arm, seed) from the role and Slurm array index, (b) applies the Stage-1 gate rule of §7, (c) refuses to start if the allocated GPU is not empty or the attempt directory exists, (d) writes `job_meta.json` (job id, host, GPU UUID) and (e) runs the frozen trainer with exactly: `--cfg E36_d2262 --steps 35000 --batch 16 --lr 0.0002 --wd 0.05 --warmup-frac 0.05 --mask-ratio 0.6 --val-mask-seed 7001 --test-mask-seed 7002 --probe-steps 200 --max-run-hours 2.2 --save-model`, plus `--data-dir /scratch/iitp4/fu_b/hcp --split-file …/in/split.json` for HCP.

Each attempt writes `runs/<source>_<arm>_s<seed>_a<attempt>/` (`run.json`, `train_log.jsonl`, `stdout.log`, `job_meta.json`).

## 6. Primary outcome (unchanged from r1 §6)

NMSE_arm,s = Σ_i num_i / Σ_i den_i over the 16 test subjects, 60 non-overlapping windows each, fixed eval masks (seed 7002).

## 7. Gates

### 7.1 F+ measurement-capacity gate at the 4× budget (NEW; governs Stage 1)

**Why a new gate.** The r1 F+ pass certifies capacity at 140k samples only. The F+ advantage of C could be a sample-efficiency effect: the M0 `Linear(8C→2C)` can in principle carry the planted signals of all 8 cells, so E might catch up with 4× training. A Stage-1 stop at 4× is interpretable only if the pipeline still converts a strong planted grouping signal into a ≥ δ gain at 4×.

**Runs.** F+ fixture stream, arms E, C, S × seed 0 (`perms_Fplus.npz` keys E, C, S_seed0), the full §2 FU-B recipe (35,000 steps). Outcome: test NMSE over 16 × 32 fixed synthetic windows (eval seed 7002), as r1 §7.2. One seed, not two: two seeds (≈ 10.5 GPU-h) or a full 12-run gate (≈ 21 GPU-h) do not fit the 33 GPU-h cap with Stage 1. Single-seed gate noise is a stated limitation (r1's two F+ seeds differed by ≤ 0.5 % NMSE).

**Rule (frozen `stats.gate_fixture`, kind Fplus):** passes iff (E−C)/E ≥ δ **and** (S−C)/S ≥ δ.

**States** (`src/topic2_fu_b/verdict.gate_state`):
- `missing`: any of the three runs has no valid attempt after failure handling (§10), or any integrity error → FU-B verdict `no_verdict`.
- `fail`: computed and failed → FU-B verdict **`inconclusive` (measurement capacity at 4×)**; Stage 1 is not read.
- `pass` → Stage 1 governs.

**Stage-1 launch.** For wall-clock reasons (B300 share rule, §10) the 15 Stage-1 jobs may be queued as a Slurm array with `--dependency=afterany:<gate job>`, before the gate finishes. Each Stage-1 task, at its start on B300, recomputes the gate state from the gate run records with the frozen FU-B code and **exits without training unless the state is `pass`** (skip marker in `/scratch/iitp4/fu_b/skipped/`). So Stage 1 never trains unless the 4× gate passed. If the gate is `missing` after a software failure, the gate run is rerun (§10) and the Stage-1 array is submitted again.

### 7.2 F− bias gate (inherited from r1; NOT rerun at 4×)

A 4× F− gate (3 runs, ≈ 5.2 GPU-h) does not fit the cap together with the F+ gate and Stage 1. F− is inherited from r1: the value `fixture_gates.Fminus.pass` of `results/topic2/2026-11-01/verdict.json`, read only if that file's sha256 is `59af05e5…af68`, and counted as a pass **only if it is literally `true`** (anything else, including a sha mismatch or a missing file, is "not certified"). F− can only downgrade a would-be `keep` to `inconclusive`; it never changes `stop`, `modify` or `inconclusive`. Limitation: the bias check is certified at 140k, not at 560k. If the verdict is `keep`, the report states this limitation in the same sentence as the verdict and gives the costed 4× F− check.

## 8. Inference and verdict (`src/topic2_fu_b/verdict.py`, `scripts/topic2fu_b_verdict.py`)

The frozen `scripts/topic2_verdict.py` is **not** used for FU-B: it hard-codes F+ seeds (0, 1), counts a missing F− as a pass and returns `no_verdict` when F+ fails. FU-B uses its own wiring around the frozen `src/topic2_rgpool/stats.py` functions (`t_interval`, `relative_gain`, `hierarchical_bootstrap`, `gate_fixture`, `verdict`), imported unchanged.

**Record validity.** An attempt is valid iff `status == "completed"` and: cfg, steps = 35,000, batch, lr, wd, warmup_frac, mask_ratio and n_params equal §2/§5; `perm_key` = the r1 key for (arm, seed); `perm_file_sha256` and `perm_sha256` equal the pinned partition files; `code_sha256` equals the r1 freeze pins for every module of `src/topic2_rgpool`; 16 finite test terms with den > 0 and `test_nmse` = Σnum/Σden; val curve at exactly the four §2 steps; for HCP also `split_file_sha256` = `cc521b08…`, 7,616 training windows and 16 distinct positional `hNN` test tokens. Per (source, arm, seed): attempts numbered 1..n with n ≤ 2; a later attempt only after an invalid one; exactly one valid attempt is used; two valid attempts are an integrity error (never last-wins). Failed or invalid attempts never enter the inference.

**Precedence (applied in this order):**

| # | condition | FU-B verdict |
|---|---|---|
| 1 | F+ gate state `missing` (or unknown) | **no_verdict** (software, not a scientific null) |
| 2 | F+ gate state `fail` | **inconclusive** (measurement capacity at 4×); Stage 1 not read |
| 3 | any of the 15 Stage-1 (arm, seed) without a valid attempt, any integrity error, or test-subject order differing between runs | **no_verdict** |
| 4 | otherwise: frozen `stats.verdict(I1_t, I2_t, δ, fplus_gate_pass = (gate state == pass), fminus_gate_pass = (inherited F− is True))` | stop / keep / modify / inconclusive per the r1 table |

The r1 table (unchanged): **stop** iff the upper 95 % t bound of I1 < δ; **keep** iff mean I1 ≥ δ, lower bound I1 > 0 and lower bound I2 > 0; **modify** iff mean I1 ≥ δ and lower bound I1 > 0 but lower bound I2 ≤ 0; otherwise **inconclusive**; keep with F− not certified → inconclusive. Boundaries are exactly as written (strict < for stop, ≥ for the mean, strict > 0 for the lower bounds).

**Primary inference:** two-sided 95 % t interval (df 4) over the five seed-level contrasts, paired by seed. **Secondary:** hierarchical bootstrap (B = 10,000, seed 0), never overriding.

**No interim verdict.** All Stage-1 tasks are queued in one array; no contrast is computed before all 15 attempts are terminal; no launch decision depends on Stage-1 outcomes. Copied-back records are checked only for status/integrity before that.

## 9. Secondary and descriptive outcomes (no decision rides on them)

- Gate gains (C vs E, C vs S) at 4× next to r1's 1× gains.
- Hierarchical bootstrap; per-seed I1/I2; val curves (health only).
- **Paired budget contrast with r1** per (arm, seed): FU-B − r1 test NMSE; per-seed ΔI1 = I1_FU-B − I1_r1 (same seeds, same first 140k samples, same test subjects and masks).
- **Manipulation check:** is FU-B's seed-mean E NMSE below r1's (computed from the r1 run records)? If not, more training did not improve the baseline and FU-B cannot speak to under-training; this is reported next to the verdict.
- **Stalls.** A completed run with val NMSE ≥ 0.999 at all four val points is "stalled" (cf. r1 `hcp_S_s2`). It is a valid run, counted in the primary inference, never rerun or dropped. Pre-registered non-governing sensitivity: drop every seed with any stalled arm and recompute the t intervals (if ≥ 2 seeds remain), labelled "sensitivity".
- Multiplicity: FU-A…FU-E are separate questions under separate cards; no correction is applied across them, and the report says so.

## 10. Compute, Slurm, budget guard and failure policy (C5)

- **Slurm only:** `sbatch -p gpu -w b300-01 --gres=gpu:1 -c 8 --mem=64G --time=02:30:00`; gate = array 0–2; Stage 1 = array 0–14 with throttle `%4` (≤ 4 concurrent FU-B GPUs within the shared 8-GPU per-user QoS); reruns = single jobs. Rendered by `src/topic2_fu_b/slurm.py`, submitted by `scripts/topic2fu_b_slurm.py`; a copy of every submitted sbatch file is kept in `results/topic2/2026-11-02_fu_b/slurm/`.
- **B300 share rule:** immediately before every submission, `squeue` is checked; no submission while any `g3t-G-E0-*` job is PENDING or RUNNING (waits are recorded; they are not failures).
- **Ledger:** a `started` row per submission (job id) and a `completed` row per finished task with GPU-h = sacct ElapsedRaw × GPUs / 3600, rounded up to 0.01, times from `TZ=UTC sacct` (sacct prints KST by default).
- **Budget guard (cap 33 GPU-h):** before every submission, FU-B used GPU-h (closing ledger rows of explorer_FU_B_r1_1/2/3 and worker_FU_B_r1) + (active FU-B tasks + new tasks) × max(1.75 h, the observed maximum per run) must be ≤ 33. Plan: explorers 0.14 + worker smoke ≈ 0.1 + gate 3 × ≈1.72 + Stage 1 15 × ≈1.72 ≈ 31.2 GPU-h, leaving room for about one rerun. A launch the guard rejects is not made.
- **Software failure** = run.json status `started` (crash, Slurm TIMEOUT / NODE_FAIL / OUT_OF_MEMORY / CANCELLED), `failed_nonfinite_loss` or `aborted_throughput`; an unreadable run.json; a completed record failing the §8 validity checks (launch error); or the wrapper refusing a busy GPU. Handling: **one identical rerun** of that (source, arm, seed) as attempt 2 in a new directory, if the guard admits it; the failed attempt is kept and listed. A second failure, or a rerun the guard rejects, leaves that (arm, seed) without a valid attempt → **no_verdict** (§8 rules 1/3), with a costed plan. A failure is never relabelled inconclusive.
- **Stalled-but-completed runs are not failures** (§9).
- **VM wipe:** `/scratch` can be wiped on VM stop. Code and env recipe live in the repo (`scripts/b300_env/`); run records are copied back after each wave; lost runs are reruns (same rules). Model weights are not backed up.
- Cleanup at the end: no FU-B job or process left; `/scratch/iitp4/fu_b/` kept (weights, view) and documented.

## 11. Pre-registered reading of each verdict

| FU-B verdict | reading, and what it adds to the r1 stop |
|---|---|
| **stop** | Within 4× the r1 budget (same recipe), a practical gain ≥ 1 % of C over PatchMergingV2 is excluded. The r1 null is not explained by under-training up to 560k samples at this target and model size. Strengthens the r1 stop; says nothing about other targets/scales (FU-A, FU-D). |
| **modify** | At 560k, C gives a ≥ δ gain with a positive lower bound, but it is not attributable to FC specificity (I2 lower bound ≤ 0). The r1 stop at 140k stands as recorded; the gain is budget-dependent and not connectome-specific. |
| **keep** | At 560k, C gives a ≥ δ gain over the cubes and beats the FC-shuffle null. The r1 stop stands for 140k; the r1 null was budget-limited. Stated with the F− (140k-only) limitation and the costed 4× F− check. |
| **inconclusive** (intervals) | The I1 interval straddles δ or 0: budget dependence unresolved at this seed count. Intervals reported in full. |
| **inconclusive** (F+ gate failed at 4×) | With 4× training the pipeline no longer converts a planted cell-level grouping signal into a ≥ δ gain, i.e. the r1 F+ advantage was (at least partly) a sample-efficiency effect. The HCP comparison at 4× would not be interpretable, so it is not run/read. |
| **no_verdict** | Software failure or cap exhaustion; not a scientific null. Costed plan given. |

## 12. Frozen inputs

- This card; code sha256 of every file in `src/topic2_fu_b/`, `scripts/topic2fu_b_*.py` and `tests/topic2_fu_b/` at freeze; the r1 inputs it reuses (`perms_hcp.npz`, `perms_Fplus.npz`, sanitized `split.json` and `hcp_manifest.json`, r1 `verdict.json`, r1 `code_sha256_at_freeze.txt`); B300 env recipe `scripts/b300_env/build_env.sh` + `lock.txt` (the FU-B venv at `/scratch/iitp4/fu_b/venv` reproduced `lock.txt` exactly). All in `results/topic2/2026-11-02_fu_b/card_sha256.txt`.
- The frozen r1 code is checked against `results/topic2/2026-11-01/code_sha256_at_freeze.txt` before copying it to B300, and every run record's `code_sha256` must equal those pins (§8).

## 13. Limitations (stated before results)

- Same recipe, not re-tuned for 4× (§2). One gate seed. F− certified at 1× only. Five seeds (df 4).
- One small model (E36), one target (2 mm voxel z-scored BOLD with NMSE ≈ 0.99 in r1), one dataset; 64 training subjects, so 4× budget means ≈ 73 passes and possible over-fitting, which the val curves describe but do not govern.
- HCP family structure unavailable; relatives may straddle splits (r1 limitation).
