# Topic 2 follow-up A (FU-A) result report: 12 mm cell-mean target

Date: 2026-11-02 KST (2026-11-01 UTC). Author: worker_FU_A_r1, run tw-20261031-four-topics, workflow C.
Governing card: `2026-11-02_topic2_fu_a_card.md`, sha256 `72be3e83c43f17990d6ed4ab8e2f254894c083f697dfe18557866866623618fb`, frozen 2026-11-01T16:06:01Z (`results/topic2/2026-11-02_fu_a/card_sha256.txt`, `freeze_time.json`), before any FU-A run. No addendum: nothing governed changed after the freeze.
All numbers come from this follow-up's dated outputs in `results/topic2/2026-11-02_fu_a/` or, where marked "r1", from `results/topic2/2026-11-01/` (C8). None come from `EMPIRICAL_ANALYSIS_REPORT.md` or the consolidated status file.

## 0. Verdict

**`inconclusive` (measurement capacity), by card §7.3 and §8.3 step 2.** The training-loop gate failed. With a planted connectome signal and voxel noise calibrated to the HCP TRAIN data, connectome boxes lowered the fixture test NMSE by only **+0.55 %** against PatchMergingV2's cubes. The card requires at least δ = 1 %.

- As the card requires, **Stage 1 on HCP was not run**. No real-data FU-A model was trained, and no HCP number governs anything here.
- **Meaning.** At this model size (E36) and budget (140k samples), on the 12 mm cell-mean target at realistic noise, this pipeline did not turn a planted connectome signal into a gain of 1 % NMSE or more. A Stage-1 `stop` would therefore not have been interpretable. The question of option A ("do connectome boxes beat cubes when the target is not noise-dominated?") is **not answered** by this follow-up.
- **The r1 verdict stays `stop`** (I1 +0.147 % [−0.068 %, +0.361 %] < δ 1 %), unchanged, with the scope its report states. FU-A neither weakens nor strengthens it on HCP; it adds a gate result (§5).
- **Prediction.** The card pre-registered "`stop` or `inconclusive`", based on the r1 Stage-0 prior. The outcome is `inconclusive`, but for the gate reason, not because of HCP data.

## 1. What was built (F1, F2)

**Card.** A new dated card was frozen with sha256 receipts before any FU-A run. It defines:
- the target exactly;
- the single changed factor relative to r1;
- noise-calibrated fixtures;
- a budget-constrained gate (a declared deviation from r1 §7.2);
- a table-driven verdict with premise check M and a stall clause.

**Code** (own paths only; the frozen r1 package is imported, never edited; r1 `code_sha256_at_freeze.txt` still 33/33):

| path | role |
|---|---|
| `src/topic2_fu_a/target.py` | block means over the brain voxels of each 6³ cell, broadcast back with one global κ |
| `src/topic2_fu_a/sources.py` | `CellHCPSource` (reads r1 `cellmeans.npy` + `mask.npy`; halts on contract violations); `CellFixtureSource` (r1 generator + voxel noise σ_v → same block-mean path) |
| `src/topic2_fu_a/run.py` | runs the frozen r1 `train.run` unchanged, with its two source classes rebound for the call and restored afterwards; adds FU-A fields to `run.json`; refuses non-positional tokens |
| `src/topic2_fu_a/calib.py` | TRAIN design statistics (Q, κ, NF) and the σ_v calibration |
| `src/topic2_fu_a/verdict.py`, `scripts/topic2fu_a_verdict.py` | table-driven verdict; δ and all thresholds frozen, no CLI override |
| `scripts/topic2fu_a_{prepare_b300,build_fixture_perms,train,submit,token_scan}.py` | positional data view and design stats; fixture partitions; training CLI; Slurm arrays with the B300 sharing rule; count-only C4 scan |

**Tests.** `tests/topic2_fu_a/` has 70 tests: 69 pass and 1 is skipped by design (the Stage-1 token-scan check, because no Stage 1 ran; the gate token-scan check runs and passes). The tests cover:
- block means equal the frozen r1 `cell_means` on HCP-format arrays;
- a pad-offset misalignment is detected;
- the field is cell-constant on the brain and zero outside it;
- the voxel NMSE equals the n_c-weighted cell NMSE plus the within-cell term, and predicting 0 gives 1;
- the HCP cell source returns exactly the block-mean field of the frozen r1 `HCPSource` batch;
- the fixture cell noise variance is σ_v²/n_c;
- every tensor the frozen loop trains and evaluates on is cell-constant, while the r1 stream fed to the same loop is rejected (this catches a wrapper that fails to rebind);
- sources are restored after an error;
- non-positional tokens are refused before training;
- the Stage-0 fixtures at σ_v (§3);
- the Slurm sharing rule;
- the count-only scan;
- the halt of the preparation script;
- receipts, and C4 on all FU-A outputs.

**Verdict-code mutation check.** `verification/worker_FU_A_r1/mutation/run_mutants.py` killed **31 of 31** one-line mutants of `verdict.py`, and the unmutated control passes. The mutants include every r1 defect class named in the dispatch:
- a missing F+ gate counted as pass (M07);
- failed runs counted (M09);
- the F+ failure reported as `no_verdict` instead of `inconclusive` (M08);
- F− downgrading keep only (M12);
- `≥` against `>` at each boundary (M01–M06, M16, M17).

The rest cover extra runs, test order, foreign or r1 records, the premise, the stall clause and δ. Boundary tests use exactly representable values: (100 − 99)/100 equals δ.

## 2. Pre-freeze design statistics (TRAIN only; Slurm job 492, CPU)

**Data checks** (`design_stats_train.json`; booleans and counts only). All of these held:
- 88 subjects;
- manifest order equals the sorted directory names;
- 5 burned development subjects excluded;
- 88 QC passes and 0 failures;
- the positional repo split equals the r1 original split mapped through the token map;
- 64/8/16 disjoint.

**Reproduction.** A rerun with the frozen script (`fua-prep-repro`, after the freeze) gave identical checks and statistics (`logs/b300/design_stats_repro_frozen_script.json`).

| quantity | value | meaning |
|---|---|---|
| Q | 0.030780 | the cell-mean field holds 3.08 % of the per-voxel variance |
| κ = 1/√Q | 5.699892 | unit mean-square target; NMSE does not depend on it |
| NF | 0.20851 | share of the cell-mean energy that independent voxel noise would contribute |
| σ_v (fixtures) | 6.545925 | voxel noise that gives the fixtures the same noise share |
| cell lag-1 autocorrelation | median 0.253, mean 0.313 | descriptive |

## 3. Fixtures at the calibrated noise (CPU; card §7.1–7.2)

**Fixture partitions.** Built on block means of the noisy fixture-train samples (`partitions/fixture_build.json`):
- κ_fix = 0.970840;
- F+ purity of C against the planted networks: 1.00 (E 0.31, S_seed0 0.25, G 0.25, R 0.25);
- realized noise share of the fixture cell-mean energy: 0.248. This is slightly noisier than the TRAIN calibration of 0.209, because the realized fixture signal variance is 0.80.

**Stage-0 checks.** Held-out samples, PCA basis fitted on separate fixture-train samples (`verification/worker_FU_A_r1/probe_stage0_fixture_numbers.out.json`; the same seeds as `tests/topic2_fu_a/test_fixture_stage0.py`, 4/4 pass):

| fixture | E r | C r | G r | rule | result |
|---|---|---|---|---|---|
| F+ | 0.071 | **0.338** (purity 1.00) | 0.059 | purity ≥ 0.95; r_C ≥ max(E, G) + 0.10 | pass |
| F− | **0.486** | 0.416 | 0.421 | r_C ≤ r_G + 0.02 and ≤ r_E + 0.02 | pass |
| NULL | — | — | — | \|r\| ≤ 0.02 | pass |
| premise | single voxels keep < 25 % of the cell-level C − E advantage | | | | pass |

The planted structure is therefore present and recoverable at Stage 0 at this noise level, and the box builder finds it.

## 4. Training-loop gate (card §7.3; B300 Slurm job 507, b300-01, 2 × 1 GPU)

Both runs completed with status `completed` and no rerun:
- full budget, 8,750 steps × 16;
- 1,477.5 s and 1,476.4 s of wall time inside the loop (sacct ElapsedRaw 1,480 s and 1,479 s);
- throughput probe at step 200: 0.1707 s per step, 93.7 samples/s.

**Integrity checks** in each `run.json` (records in `results/topic2/2026-11-02_fu_a/runs/Fplus_{E,C}_s0/`):
- `fua_checks` max within-cell spread 0.0, so the loop trained on the cell-mean field;
- `fua_rebound_sources_restored` true;
- permutation sha256 E `b83e23eb…`, C `e32b7599…` (1,327 cells moved), identical to `fixture_build.json`;
- 38,712,096 parameters in both arms;
- device NVIDIA B300, torch 2.15.0+cu134.

| run | test NMSE (16 × 32 windows, eval seed 7002) | VAL 2188 | VAL 4375 | VAL 6562 | VAL 8750 |
|---|---|---|---|---|---|
| Fplus_E_s0 | 0.774678 | 0.79860 | 0.78188 | 0.77634 | 0.77458 |
| Fplus_C_s0 | **0.770409** | 0.78952 | 0.78119 | 0.77314 | 0.77098 |
| gain (E − C)/E | **+0.551 %** | +1.14 % | +0.09 % | +0.41 % | +0.46 % |

**Gate rule (card §7.3):** F+ passes iff (E − C)/E ≥ δ = 1 %. With +0.551 % < 1 %, **F+ fails** (`results/topic2/2026-11-02_fu_a/verdict.json`, `scripts/topic2fu_a_verdict.py`).

**Descriptive, governs nothing.**
- C is lower than E in all 16 evaluation groups.
- The absolute difference is 0.00427 NMSE, which is 1.9 % of E's explained variance (1 − NMSE_E = 0.2253).
- The gain does not grow with training: VAL gain is +1.14 % at a quarter of the budget, then +0.09 %, +0.41 % and +0.46 %. In the r1 F+ gate the gain grew with training.
- The irreducible noise share is about 0.25. Arm E captures about (1 − 0.775)/(1 − 0.248) ≈ 30 % of the predictable fixture energy, close to the ≈ 32 % of r1's near-noise-free F+ (1 − 0.677).

**Comparison with the r1 F+ gate** (2 mm voxel target, voxel noise 0.1, the same planted generator; r1 seeds 0 and 1):
- r1: E 0.6769 / 0.6803, C 0.6582 / 0.6575, gain +3.06 %.
- FU-A seed 0: gain +0.55 %.

At the noise level of real HCP cell means, the same planted grouping signal gives about a fifth of the r1 gain.

## 5. What FU-A adds to the r1 stop verdict

1. **The r1 gate overstated sensitivity at realistic noise.** The r1 F+ gate passed at +3.06 % on fixtures with almost no voxel noise. Its own report says that gate "says nothing about sensitivity on real 2 mm BOLD".
   - FU-A measures that gap for the less noisy 12 mm target. With the fixture noise share set to the HCP TRAIN value (0.21; realized 0.25), the gain drops to +0.55 %, below δ.
   - It follows that a voxel-level F+ gate at HCP noise (voxel R² of a few %) would almost certainly fail too. This is an inference, not run here. So the r1 `stop` should be read as "no gain ≥ 1 % was found by a pipeline whose capacity to find a planted 1 % gain at real noise levels was not established". This is a scope statement, not a change of the r1 verdict category, which stays `stop` under its own frozen card.
2. **The noise-free r1 gate does not transfer to the lower-noise target.** "Reconstruct the cell means instead of voxels", the cheapest option in result report §7, does not by itself restore measurement capacity at E36 and 140k samples.
3. **No new HCP evidence.** The r1 Stage-0 prior (C − E pca2 −0.052, 0/16 subjects) remains the only real-data evidence on this representation, and it is descriptive.

## 6. Compute (C5) and data handling (C4, C6)

**GPU use.**
- Slurm job 507 used 0.822 GPU-h (2 tasks × 1 GPU; ledger start and closing rows in `results/gpu_ledger_2026-10-31.md`).
- The FU-A explorer smokes (jobs 403 and 427) used 0.130 GPU-h.
- FU-A total: **0.952 GPU-h of the 8 GPU-h cap**.
- Stage 1 (15 runs, projected ≈ 6.3 GPU-h at the measured 0.416 h per run) was not launched, because the card rule says so after an F+ failure, not because of budget.

**Slurm and environment.**
- CPU-only Slurm steps: 489 (venv build), 492 (data view and design statistics), and the post-freeze reproduction step `fua-prep-repro`.
- No GPU job ran outside Slurm.
- The B300 sharing rule was checked immediately before the submission: 0 `g3t-G-E0-*` jobs.
- Project-local venv at `/scratch/iitp4/fu_a/env/venv` (recipe `scripts/b300_env/build_env.sh`). No install on DGX-Spark.

**C4 and C6.**
- HCP-YA Open Access, public under PI decision 2.
- The HCP files were read only by the CPU steps (`cellmeans.npy`, and `mask.npy` of TRAIN subjects). The gate itself is synthetic.
- Nothing derived per subject left B300.
- The B300 count-only token scan (88 r1 subject tokens plus 1,084 HCP directory names held in memory) found **0 hits** in 14 text files before copy-back (`token_scan_b300_gate.json`).
- The copied-back files are byte-identical to the B300 originals (14 of 14 sha256 values).
- Every repo output passes `tests/topic2_fu_a/test_receipts_and_c4.py`: no ID-bearing path shapes and no 16-hex subject tokens.

## 7. Process notes and deviations

Recorded for audit; none of these changed a governed computation after the freeze.

**Declared in the card before any run.**
- The gate is 2 runs instead of r1's 12, on a single seed, with no F+ S arm and no F− (card §7.3; cap).
- F− failure downgrades keep and modify, not keep only.
- The stall clause and premise check M were added.

**Pre-freeze facts.**
- The first copy-back of `design_stats_train.json` hung. The local file was rewritten from the job's own printed JSON, and its sha256 (`694c31ca…`) was then confirmed equal to the B300 original.
- `scripts/topic2fu_a_prepare_b300.py` received a lint-only refactor after job 492 and before the freeze. The frozen version reproduces job 492's output exactly.
- The fixture partitions were built on local CPU (synthetic only) because the B300 ssh route timed out from about 15:40Z to 16:03Z.
- One B300 CPU launch of the same build never started.

**Not done.**
- Stage 1 (by rule);
- the unfunded gates (F+ S, F−);
- no new Stage 0 (r1 already scored this representation).

## 8. Limitations

- **Single-seed gate.** r1 per-seed F+ gains ranged from +2.8 % to +3.4 % (seed spread ≈ ±0.3 %). At +0.55 %, a second seed is very unlikely to reach δ, but the rule is applied to seed 0 as frozen.
- **Calibration model.** The noise calibration assumes independent unit-variance voxel noise, which gives an upper bound on the noise share. Spatially correlated real noise would make real cell means noisier than this, not cleaner.
  - The fixture's planted signal (8-cell networks carrying about 42 % of each cell's signal variance) is a design choice inherited from r1. A stronger planted effect would pass more easily, but that would test a different, less realistic, question.
- **One setting only.** E36, 140k samples, untuned hyperparameters, as in r1.

## 9. Costed plan (not run; each needs its own new dated card and a PI decision; FU-A cap remaining ≈ 7.0 GPU-h)

Measured cost on B300: 0.416 h per E36 run of 140k samples.

| option | change | gate first | est. GPU-h |
|---|---|---|---|
| A′1 | gate replication: F+ E/C seed 1 on the same frozen design (tells whether +0.55 % is seed noise; cannot overturn this verdict) | — | 0.84 |
| A′2 | 4× budget (560k samples, the FU-B setting) on the cell target: F+ E/C gate, then Stage 1 only if it passes | 2 × 1.70 | 3.4 (+ 25.5 for Stage 1) |
| A′3 | E192 scale on the cell target: F+ E/C gate, then Stage 1 | 2 × 1.2–1.36 | 2.5–2.7 (+ 18–20) |
| A′4 | the unfunded gate arms (F+ S s0, F− E/C s0) | — | 1.25 (meaningful only once a gate passes) |

## 10. Reproduce / verify

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_a/card_sha256.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_a/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_a/output_sha256.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-01/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_a -q
/home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs /tmp/fua_verdict_check.json
/home/juke/superclaude-env/bin/python3 -B verification/worker_FU_A_r1/mutation/run_mutants.py      # 31/31 killed
```

On B300 b300-01, the frozen code tree and both gate runs are kept in `/scratch/iitp4/fu_a/{code,runs,logs}`. The gate is reproduced by `scripts/topic2fu_a_submit.py --jobs /scratch/iitp4/fu_a/logs/jobs_gate.json --name fua-gate --base /scratch/iitp4/fu_a`, after checking `squeue` for `g3t-G-E0-*` jobs.
