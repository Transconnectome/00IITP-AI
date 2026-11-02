# Topic 2 follow-up C (FU-C) analysis card: 8 fresh training seeds at the r1 setting

Status: **FROZEN** when its sha256 is written to `results/topic2/2026-11-02_fu_c/card_sha256.txt`. Later changes go in dated addenda (`2026-11-02_topic2_fu_c_addendum_NN.md`); this file is never edited.
Author: worker_FU_C_r1, run tw-20261031-four-topics, workflow C, milestone FU_C (PI decision 7, option C of the r1 result report §7).
Mode: **CONFIRMATORY replication.** The r1 experiment (card `2026-11-01_topic2_card.md`, sha256 `c9bfc60a…41f5`) is repeated with 8 new training seeds; nothing else changes. Every decision below is fixed before any FU-C Stage-1 number exists. The r1 verdict (`stop`) stays as recorded; FU-C is a new experiment and never re-reads r1.

## 0. Data and results seen before freezing (disclosure)

- **All r1 results are known** to the author: r1 I1 = +0.147 % [−0.068 %, +0.361 %] (df 4), I2 = +0.473 % [+0.001 %, +0.946 %], verdict `stop`; per-seed I1/I2; the stalled run `hcp_S_s2`; the r1 fixture gates (F+ gains +3.06 % / +2.93 %, F− gain −1.74 %); r1 addenda 01–05.
- **Explorer probes** (explorer_FU_C_r1_1/2/3, 0.262 GPU-h, ledgered) ran on B300 before this card. They re-scored r1 checkpoints, reran short prefixes (≤ 1,700 steps, no test evaluation) of already-reported r1 runs (hcp E/C seed 0, F+ C seed 0) and built S surrogates for seeds 5..17 from train-only data. explorer_FU_C_r1_1 also trained arm S with **seed 5** for 300 steps (training loss only). No FU-C seed in §2 (10..17) has ever been trained by anyone; that is why the seed set starts at 10.
- **Power and stall simulations** by the explorers, from r1 aggregates only (§12).
- **Built by this worker before freezing, from train-only inputs (no outcome):** the FU-C venv (§3.4), the positional data view (§3.2), and the partitions `perms_fu_c.npz` (§3.3).
- **Environment anchor** (§3.5): 300-step prefixes of three already-reported r1 configurations, aborted by the frozen throughput probe; no validation or test number was computed.

Prediction stated before any FU-C result: **`stop`** (§12). Its value is precision: whether the r1 stop survives on independent seeds, and how narrow I1 and I2 become.

## 1. Question, estimands, unit

**Q.** At the r1 setting (SwiFT ver11 E36_d2262 trained from scratch with SimMIM on HCP-YA REST1_LR; 140,000 samples; 64 train / 16 test subjects), does grouping 12 mm cells into connectome boxes at M0 (arm C), instead of PatchMergingV2's 2×2×2 cubes (arm E), lower held-out masked in-brain NMSE by at least δ = 1 %, over 8 new training seeds?

- Practical claim: I1_s = (NMSE_E,s − NMSE_C,s) / NMSE_E,s.
- Surrogate contrast: I2_s = (NMSE_S,s − NMSE_C,s) / NMSE_S,s; S = the same builder on a distance-binned FC surrogate. I2 is confounded with box compactness (r1 addendum 05 item 4) and is **not** read as FC specificity.
- Unit of inference: the training seed. NMSE_arm,s = Σ_i num_i / Σ_i den_i over the 16 test subjects and their 60 non-overlapping evaluation windows (r1 card §6, unchanged).

**Falsification statement.** The r1 stop is *not replicated* if FU-C returns `keep`, `modify`, or `inconclusive` (an I1 upper bound ≥ δ). It is *replicated* if FU-C returns `stop`. `no_verdict` means not assessed.

## 2. What changes relative to r1: the seeds, and nothing else

| item | r1 | FU-C |
|---|---|---|
| training seeds s | 0..4 | **10, 11, …, 17 (8 fresh seeds)** |
| weight init / window order / training masks | s / 1000+s / 2000+s | same rule, s ∈ 10..17 |
| S surrogate seed | s | s (S_seed10..S_seed17, new) |
| eval masks | val 7001, test 7002, per-subject generators | unchanged (identical for every run) |
| E and C partitions | r1 `perms_hcp.npz` | identical arrays (sha pins §3.3) |
| data, split, dev-subject exclusion | r1 §4 | identical subjects and split (positional view, §3.2) |
| model, masking, loss, optimiser, budget | r1 §5 | identical (E36_d2262; mask 0.6; AdamW; lr 2e-4, wd 0.05, warmup 5 %, cosine; 8,750 × 16) |

**Why fresh seeds and not 5 r1 seeds + 3 new.** Training is bitwise deterministic per seed (§3.5), so reusing seeds 0..4 re-reads data whose verdict is known. In the explorers' simulation (§12), pooling 5 seen + 3 new seeds returns `stop` 96 % of the time when the true I1 equals δ and never returns `keep` at a true I1 of 1.5 %; 8 fresh seeds return `stop` 2.4 % of the time at I1 = δ (nominal 2.5 %). The 5 r1 seeds are **not** reused in the primary analysis; a pooled 13-seed analysis is reported only as a labelled descriptive secondary (§7). No seed is ever substituted.

## 3. Data, partitions, environment

### 3.1 Data (C4, C6)
HCP-YA S1200 Open Access `rfMRI_REST1_LR_hp2000_clean`, counted as public under PI decision 2 (HCP Data Use Terms: no redistribution, no re-identification). FU-C reads the r1 preprocessed tensors of the 88 QC-passed subjects (r1 card §4: the 5 burned explorer development subjects were excluded there; FU-C inherits the exclusion and never reads the sealed salt). Data exist only on B300 node b300-01 (node-local `/scratch`); they never leave B300. No ENIGMA data are used.

### 3.2 Positional data view and split
`scripts/topic2fu_c_make_datadir.py` hard-links (never symlinks) the r1 subject files into `/scratch/iitp4/fu_c/hcp_pos/subjects/hNN`, NN = position in the r1 original manifest (sha `26ba34a9…`, sorted by content hash; r1 addendum 05 §2). Runs use the repo's sanitized `results/topic2/2026-11-01/split.json` (sha `cc521b087a97a6669fe6f94041dac2c2c0c0987741ac698203309af1ced2c75a`). The check `results/topic2/2026-11-02_fu_c/env/datadir_check.json`: the relabelled r1 split (sha `c13b5f21…`) equals the sanitized split for train, val and test (64/8/16); 88/88 positions complete. Every FU-C run.json therefore carries only h-tokens.

### 3.3 Partitions
`scripts/topic2fu_c_build_perms.py` imports the frozen `scripts/topic2_build_partitions.py` unchanged, sets its constant `S_SEEDS_HCP` to (0..4, 10..17) in memory only, and calls the frozen `hcp_mode` (train subjects only). The FU-C file is written only if every rebuilt r1 item equals its r1 pin; result `results/topic2/2026-11-02_fu_c/partitions/perms_fu_c.json`: self-check 25/25 true (train FC float32 sha `e2912ee9…`, 1,195 signal cells, 229,304 group-mask voxels, E, C, G, R and S_seed0..4 equal to r1 by sha and by array, nvox and group mask equal), new surrogates distinct from each other and from r1.

`perms_fu_c.npz` sha256 `f9e32ab76fdc7daed8c70a5cb855076d28346638bd2f2dcefa5a32e04b532bca`. Permutation sha256 per key (the verdict requires these exactly; key for arm S and seed s is `S_seed<s>`):

| key | perm sha256 | rows changed | dispersion (cells) |
|---|---|---|---|
| E | b83e23eb1db808bf694ae4894d62b50c9840bcd869ba7ac2456f40ddf0530bf3 | 0 | 0.784 |
| C | 21e4e239cc8811c58630809695596f35d54151a75195d8e79892dfa1cfd9bb45 | 231 | 1.469 |
| S_seed10 | ad8b3a0e291a9d3623867caa8317efa596fb2453c2808fec0018074745cd2820 | 232 | 1.584 |
| S_seed11 | e6cb0bfb8e440bd126b6ccb3811c358ed491eadbbb88e38e65df95d9ed127f8c | 232 | 1.599 |
| S_seed12 | 6f9c725f1c683646cff609a927c42abf7cfd00563d3813c6f21e5c0e7fa0d0ac | 232 | 1.626 |
| S_seed13 | f6d85644b84b5104d2134bac1a76aae19ee5f0f4a9965ad77a0393711d1729dc | 232 | 1.610 |
| S_seed14 | 8fae9319f3a946f0aabbf1a7dc59ec1297043cfe0cf380767091b1c8464b6df1 | 232 | 1.618 |
| S_seed15 | 59952df99308ced5ba91eb4242e4f5315d20b842b9e37942a92ac47080137c85 | 232 | 1.620 |
| S_seed16 | bf56c822c52ce3ffe82272f8535e0446d99dd95c1af59a313f6275adf852e5a4 | 232 | 1.653 |
| S_seed17 | 5a31c4f81327a06a6537cd87bc2a73af975ebc2e0586da314af0e30f40efb7e4 | 232 | 1.647 |

### 3.4 Environment
Project-local venv `/scratch/iitp4/fu_c/venv` built by `scripts/topic2fu_c_build_env.py` from the r1 lock itself (`scripts/b300_env/lock.txt`, sha `ae664dc9…`; torch 2.15.0+cu134, numpy 2.5.4, scipy 1.18.1). Its `uv pip freeze` equals the lock line for line (38/38; `env/env_check.json`). The training path is the frozen r1 code (`src/topic2_rgpool/**`, `scripts/topic2_train.py`), copied to `/scratch/iitp4/fu_c/code`; all 16 files equal `results/topic2/2026-11-01/code_sha256_at_freeze.txt`.

### 3.5 Environment anchor and reuse of the r1 training-loop gate
Slurm job 501 (debug, b300-01, 1 GPU, 210 s, 0.058 GPU-h, ledgered) ran r1 hcp E seed 0, hcp C seed 0 and F+ C seed 0 in the FU-C venv and data view, with the full 8,750-step schedule, until the frozen throughput probe aborted them at step 300 (`anchor/anchor.json`). The logged training-loss means at steps 100 and 200 equal the r1 logs **exactly** in all 6 comparisons (e.g. hcp E s0: 1.0545948070287705 / 1.0033420294523239). No validation or test number was computed.

**Gate reuse.** The r1 card §7.2 training-loop gate (arms E, C, S × seeds 0, 1 × F+ and F−; both passed) is reused **by reference**, not rerun: same frozen code (pins), same lock, bitwise-identical training under the FU-C environment, and a rerun (12 runs ≈ 5.2 GPU-h) does not fit the 13 GPU-h cap together with Stage 1. The FU-C verdict recomputes the gate from the 12 r1 fixture `run.json` files after checking each file's sha256 against `results/topic2/2026-11-01/output_sha256.txt`, with the r1 rules: F+ passes iff (E−C)/E ≥ δ and (S−C)/S ≥ δ on seed-mean NMSE; F− passes iff (E−C)/E < δ.

## 4. Runs

24 Stage-1 runs: arms E, C, S × seeds 10..17, one Slurm job per run (`scripts/topic2fu_c_slurm.py`):
`topic2_train.py --source hcp --arm A --seed s --perm-file perms_fu_c.npz --perm-key <E|C|S_seed<s>> --data-dir hcp_pos --split-file split.json --max-run-hours 0.55 --save-model`, all other arguments at the r1 defaults (cfg E36_d2262, 8,750 steps, batch 16, lr 2e-4, wd 0.05, warmup 0.05, mask 0.6, val/test mask seeds 7001/7002, throughput probe at step 200). Final weights stay on B300. Validation at steps 2188/4375/6562/8750 (health only, no selection); test once at step 8750.

## 5. Primary inference and verdict (fixed order; implemented in `src/topic2_fu_c/verdict.py`)

δ = 0.01 (PI decision 3). Primary: two-sided 95 % t interval over the 8 seed-level contrasts I1_s and I2_s, paired by seed, **df = 7** (any other df → `no_verdict`).

Evaluation order:
1. The card receipt and pinned inputs must verify → else `no_verdict`.
2. r1 gate evidence: each of the 12 fixture records must exist, match its pin, be a completed run of its (source, arm, seed) and carry the frozen code hashes → else `no_verdict` (missing evidence is never a pass).
3. F+ gate failed → `inconclusive` (measurement capacity), whether or not Stage-1 records exist.
4. Stage 1 must hold exactly one completed attempt per (arm, seed ∈ 10..17), as the last of at most 2 attempts, with no unexpected or duplicate record, and every provenance field as pinned (§8) → else `no_verdict`. A test-order mismatch is a `no_verdict`, never an exception.
5. Rules (r1 card §8, unchanged; strict where marked):

| verdict | rule |
|---|---|
| **stop** | upper bound of I1 **<** δ |
| **keep** | mean I1 **≥** δ, lower bound of I1 **>** 0, lower bound of I2 **>** 0 |
| **modify** | mean I1 ≥ δ and lower bound of I1 > 0, but lower bound of I2 ≤ 0 |
| **inconclusive** | anything else; or F+ failed; or keep with an F− failure |
| no_verdict | §5 items 1, 2, 4 |

An F− failure downgrades `keep` only (never `modify`). `stop` carries a pre-worded qualifier: lower bound of I1 > 0 → "stop; gain positive but below δ"; upper bound < 0 → "stop; C worse than E"; otherwise "stop; gain below δ, sign unresolved (interval contains 0)".

## 6. Stalled runs

A run is **stalled** iff its logged 100-step training-loss mean never falls below 0.995 (r1 addendum 05 item 5: the predict-zero plateau, as `hcp_S_s2` in r1). A stall is a property of (arm, seed) under deterministic training, not a software failure: it is **a valid run in the primary analysis**, is not rerun and is not excluded. Reported: a stall table by arm, and a descriptive sensitivity analysis that drops every seed (all three arms) with a stalled run and recomputes the intervals at df = n − 1 (not computed if fewer than 2 seeds remain). The sensitivity never changes the verdict.

## 7. Secondary and descriptive outcomes (never decision-making)

- Hierarchical bootstrap (frozen `stats.hierarchical_bootstrap`, B = 10,000, seed 0) of I1 and I2.
- Pooled 13-seed analysis: r1 seeds 0..4 (sanitized repo records) + FU-C seeds 10..17, t interval df 12, **labelled as including already-seen data**.
- I1_s against the step at which E (and C) left the plateau (first logged loss < 0.995), per seed.
- I2 with the compactness confound stated, beside the S and C dispersions of §3.3.
- Validation learning curves; absolute seed-mean NMSE differences.

## 8. Run integrity, reruns, provenance

- A run is a **software failure** if Slurm ends it before `status: completed` (time limit, node failure, crash, OOM), if the loss becomes non-finite, or if the frozen throughput probe aborts it (projected > 0.55 h). Its (arm, seed) is rerun **once** with the identical command in a new attempt directory (`hcp_<arm>_s<seed>_a2`); the failed attempt stays in the ledger and in `slurm/jobs.json`. A second failure leaves the run missing → `no_verdict`. A stalled run is not a failure (§6). No seed is substituted.
- Every selected record must have: source hcp; arm and seed matching its directory; the §4 settings; `perm_key` and `perm_sha256` as in §3.3; `perm_file_sha256` = `f9e32ab7…`; `code_sha256` = the r1 freeze pins; `split_file_sha256` = `cc521b08…`; 16 test tokens matching `^h\d{2}$` in the split's test order; 16 finite per-subject error terms with `test_nmse` = Σnum/Σden; `start_utc` later than the freeze time in the card receipt.
- Result-access rule: no Stage-1 `run.json`, training log or Slurm output is copied off B300 or read for its numbers before the FU-C verdict code is pinned (`results/topic2/2026-11-02_fu_c/code_sha256_before_results.txt`). Until then, monitoring uses Slurm states and the `status` / `projected_run_hours` fields only.

## 9. Compute (C5) and the cap rule

- B300 via Slurm only: `sbatch -p gpu -w b300-01 --gres=gpu:1 -c 8 --mem=64G -t 00:36:00` (data exist only on b300-01). Immediately before every submission: `squeue` for jobs named `g3t-G-E0-*`; if any is PENDING or RUNNING, do not submit, wait (polls ≥ 5 min apart) and record the wait. ≤ 8 concurrent GPUs for the whole Slurm user; other teams' jobs are never touched.
- Ledger: a `started` row at submission (job held until the row is written, then released) and a closing row from `sacct` (GPU-h = ElapsedRaw × GPUs; sacct prints KST, converted to UTC), via the frozen `scripts/topic2_ledger.py` under flock.
- **FU-C cap 13 GPU-h**, including the explorers' 0.262 and the anchor's 0.058. A submission of n jobs is admitted only if used + open reservations + n × 0.6 + (planned runs not yet submitted) × 0.46 ≤ 13 (`src/topic2_fu_c/budget.admit`). Otherwise the jobs are not launched, and the shortfall is reported (verdict `no_verdict` if Stage 1 stays incomplete). Expected total ≈ 0.32 + 24 × 0.44 ≈ 10.9 GPU-h.

## 10. C4

Run records carry positional h-tokens only (§3.2). Before any copy-back, `scripts/topic2fu_c_scan_b300.py` scans the copy-back tree on B300 for the 1,084 HCP directory names and the 88 original r1 content-hash tokens (held in memory only, count-only output); only a 0-hit tree is copied. Checkpoints never leave B300. A repo-side test scans `results/topic2/2026-11-02_fu_c/`.

## 11. Reading FU-C next to r1 (fixed before results)

| FU-C verdict | reading |
|---|---|
| stop | r1 stop replicated on 8 independent training seeds (with the §5 qualifier) |
| keep / modify | r1 stop contradicted: a practical gain ≥ δ is established on independent seeds |
| inconclusive | r1 stop not replicated: the I1 interval reaches δ but no gain is established |
| no_verdict | replication not assessed |

The r1 verdict and its numbers are never changed by FU-C.

## 12. Predicted operating characteristics (explorer simulations, from r1 aggregates; not results)

Source: `verification/explorer_FU_C_r1_1/probe_power/probe_power_stall.out.json` (20,000 simulations per cell; seed sd from the 5 r1 seeds) and `verification/explorer_FU_C_r1_2/local/p05_stall_sensitivity.out.json`. For 8 fresh seeds: true I1 = +0.15 % (r1 mean) → P(stop) = 1.00 without stalls, 0.975 at the r1 stall rate (1/15 runs); true I1 = δ → stop 0.024, keep 0.50, inconclusive 0.48; true I1 = 1.5 % → keep 1.00. Expected I1 half-width ≈ 0.144 % (r1: 0.215 %). Two stalled E runs give `inconclusive` with probability ≈ 0.20; stalls in C or S do not change the verdict. The seed sd rests on 5 seeds and the stall rate on 1 event in 15 runs.

## 13. What FU-C cannot answer

- FC specificity: I2 is confounded with compactness; there is no G arm in Stage 1.
- Generalisation over subjects: the same 16 test subjects and masks as r1.
- Any other target, budget or scale (options A, B, D, E are separate cards).

## 14. Frozen inputs and receipts

`results/topic2/2026-11-02_fu_c/card_sha256.txt` (written at freeze, with `# frozen_utc:`) pins, as **governing** lines that the verdict re-verifies (any failure → `no_verdict`): this card, `src/topic2_fu_c/design.py`, `partitions/perms_fu_c.npz` and `.json`, `env/env_check.json`, `env/freeze.txt`, `env/datadir_check.json`, `anchor/anchor.json`, the sanitized split, `scripts/b300_env/lock.txt`, the r1 code-freeze list and the 12 r1 fixture run.json files. It also pins, **for the record**, the run-path tools (`scripts/topic2fu_c_slurm.py`, `src/topic2_fu_c/budget.py`, `src/topic2_fu_c/perms.py`, `scripts/topic2fu_c_build_env.py`, `topic2fu_c_make_datadir.py`, `topic2fu_c_build_perms.py`, `topic2fu_c_anchor.py`); an operational change to them (ssh transport, retries) is recorded in an addendum and is not a verdict input, because the training command, settings and partitions are checked inside every run.json (§8). The verdict code (`src/topic2_fu_c/verdict.py`, `logs.py`, `scripts/topic2fu_c_verdict.py`) and its tests are pinned in `code_sha256_before_results.txt` before any Stage-1 result is read (§8); they implement §5–§7 and may not change those rules.
