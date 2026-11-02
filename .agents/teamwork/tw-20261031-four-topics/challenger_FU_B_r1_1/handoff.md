# Handoff — challenger_FU_B_r1_1 (Milestone FU_B_r1, Challenger 1 of 2)

## 1. Verdict

**`CONFIRMED`**

Milestone `FU_B_r1` (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds`) passes independent numerical recomputation, adversarial verdict/mutation stress testing, pre-registration freeze chronology verification, C1 immutability, C4 identifier hygiene, and GPU budget governance (`30.72 GPU-h <= 33.0 GPU-h` cap).

- **Blocking issues**: `0`
- **Non-blocking issues**: `2` (documented in Section 3 with exact values and line numbers)

---

## 2. Verification & Reproduction Evidence

All independent challenger probes were written and executed under `/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/` using `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3`. Earlier probe revisions (`v1`) that encountered assertion mismatches during probe development are preserved in `/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/v1_failed/` with `v1_sha256.txt` and `v1_failure_receipt.json`.

### 2.1 Task 1: Independent Metric Recomputation (`p01_v3_recompute_metrics.py`)
- **Command**:
  ```bash
  CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/p01_v3_recompute_metrics.py
  ```
- **Script SHA-256**: `9848ff2c2fbbba5ca213a0fe461f2f3b8d106ee85260644a34b482a7d4753eee`
- **Output JSON**: `/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/p01_v3_recompute_metrics.out.json` (SHA-256: `08505fdb9967a1ab6a5d06084d2ba77c712289653a9d7ee6886be169e3c3c8e6`)
- **Result**: `rc = 0` (`status: "PASS"`). Without importing `src/topic2_fu_b` or `src/topic2_rgpool`, the script independently recomputed from raw `results/topic2/2026-11-02_fu_b/b300/runs/*/run.json`, `train_log.jsonl`, and `results/topic2/2026-11-01/runs/*/run.json`:
  1. **Raw run & log integrity (`18/18` post-freeze runs: `3` gate + `15` Stage-1)**:
     - Every run has `status == "ok"`, `steps == 8750`, `n_test == 220`, `len(test_num) == 220`, `len(test_den) == 220`, `all(d > 0)`, `len(val_history) == 35` (`steps 250..8750`), and `test_nmse == sum(test_num) / sum(test_den)` (`max_nmse_pool_diff = 0.0`, `max_log_val_diff = 0.0`, `max_log_done_diff = 0.0`).
  2. **4× F+ Positive-Control Gate (`seed 0`, 560,000 samples)**:
     - `E = 0.655098810312623`, `C = 0.6306915097462201`, `S = 0.6549144352138989`
     - `gain_C_vs_E = (E - C) / E = +0.03725743383431068` (`+3.73% >= +2.00%`)
     - `gain_C_vs_S = (S - C) / S = +0.036986396938605824` (`+3.70% >= +2.00%`)
     - `pass = True`, `state = "pass"`, `max_abs_diff = 0.0` vs `verdict.json` and `gate_4x.json`.
  3. **Stage-1 HCP 5-Seed Per-Seed & Seed-Mean Test NMSE**:
     - `E`: `[0.9896787914799238, 0.9862728557489668, 0.9857219115830843, 0.9901843239157307, 0.9886966957015573]`, mean `= 0.9881109156858525` (`0.988111`), SD `= 0.0020265867223522567`.
     - `C`: `[0.985831942862598, 0.9870917229590903, 0.9862141418407978, 0.990566039405337, 0.9876539121909226]`, mean `= 0.9874715518517492` (`0.987472`), SD `= 0.0018688296428340595`.
     - `S`: `[0.9891666746169362, 0.9856979050564362, 0.9822977040044163, 0.9908220073393657, 0.9848292659594149]`, mean `= 0.9865627113953138` (`0.986563`), SD `= 0.0034255586442785804`.
  4. **Primary Paired Ratios `I1_s = (E_s - C_s)/E_s`, `I2_s = (S_s - C_s)/S_s` and 95% t-Intervals (`df = 4`, `t_crit = 2.7764451051977987`)**:
     - `I1_by_seed = [+0.003886966711580876, -0.000830264365225261, -0.0004993601531618048, -0.0003855004339388477, +0.0010550503188114038]`
     - `I1_t`: `mean = +0.0006313784156132732` (`+0.06%`), `se = 0.0013032022866913341` (`0.130%`), `lo = -0.00298689119435346` (`-0.30%`), `hi = +0.004249648025580007` (`+0.42% < δ = +1.00%`).
     - `I2_by_seed = [+0.0033712536932215935, -0.0014140416603727718, -0.003987017189440193, +0.00025833895781611484, -0.0028681616266685907]`
     - `I2_t`: `mean = -0.0009249384123596362` (`-0.09%`), `se = 0.0019948155459632256` (`0.199%`), `lo = -0.006463434270721709` (`-0.65%`), `hi = +0.004613557446002436` (`+0.46%`).
     - Governing verdict: `I1_hi = +0.425% < +1.00%` -> Rule 4 -> **`stop`**.
  5. **Hierarchical Bootstrap (`B = 10000`, `np.random.default_rng(0)`, participant cluster outer x seed inner)**:
     - `I1_boot`: `lo = -0.0007784369964266306` (`-0.078%`), `hi = +0.0033769447349354944` (`+0.338%`), `median = +0.0005998501269738735` (`+0.060%`), `max_diff = 0.0`.
     - `I2_boot`: `lo = -0.0049643435347892165` (`-0.496%`), `hi = +0.0022792074059668265` (`+0.228%`), `median = -0.0008698574159500552` (`-0.087%`), `max_diff = 0.0`.
  6. **Stall Diagnostic & Sensitivity Analysis (`df = 3`, `seeds_kept = [1, 2, 3, 4]`)**:
     - `E_s0` is the sole stalled run (`val_8750 - min(val_0..4375) = 0.9901846995679307 - 0.9896069103262079 = +0.0005777892417228459 >= 0.0`); the other 14 Stage-1 runs have `stalled == False`.
     - Sensitivity (`seeds 1..4`, `df = 3`, `t_crit = 3.182446305283708`):
       - `I1_t`: `mean = -0.0006687236765249439` (`-0.067%`), `lo = -0.0009081414141383194` (`-0.091%`), `hi = -0.00042930593891156845` (`-0.043%`).
       - `I2_t`: `mean = +0.0009142731979175133` (`+0.091%`), `lo = -0.002288687083878986` (`-0.229%`), `hi = +0.004117233479714012` (`+0.412%`).
       - `verdict_if_governing = "stop"` (identical to primary 5-seed verdict).
  7. **`r1` 1× vs `FU-B` 4× Pairing (`15/15` runs)**:
     - `same_test_order_as_r1 = True` (`test_order_sha256 = 2ccdf7b65456cf465d9eb445420cdca52f1aa8c593de2667a8a7ef0ef5c6683b` across all 15 `r1` and 15 `FU-B` runs).
     - `E_seed_mean_r1 = 0.9889223163720678` -> `E_seed_mean_fub = 0.9881109156858525` (`Δ = -0.0008114006862152754`, `E_improved = True`).
     - `13/15` `(arm, seed)` pairs lowered test NMSE at 4× budget (`E: 4/5`, `C: 4/5`, `S: 5/5`).
     - `delta_I1_by_seed = [+0.0034865529727068186, -0.0012239869334176359, -0.004596682166292586, -0.00048701829723615306, -0.0013672318480506064]`, mean `-0.0008376732544580325` (`-0.084%`).

### 2.2 Task 2: Adversarial Synthetic Inputs & Mutation Sweep (`p02_adversarial_verdict_and_mutants.py`)
- **Command**:
  ```bash
  CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/p02_adversarial_verdict_and_mutants.py
  ```
- **Script SHA-256**: `7ba038997ef66380b68a9821576828129cb68ae2da143719ae4b5b875da9a488`
- **Output JSON**: `/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/p02_adversarial_verdict_and_mutants.out.json` (SHA-256: `5f4d3432cd914bf54090adf7d98c4bdf7d8a51f15fe59417f581aa8d063cca5f`)
- **Result**: `rc = 0` (`status: "PASS"`, `169.61s`):
  1. **Exhaustive Boundary Grid (`19,440` synthetic input combinations, `0` mismatches)**:
     - Swept `gate_state in {"pass", "fail", "missing"}`, `f_minus_ok in {True, False}`, `order_ok in {True, False}`, `i1_lo in {-1e-12, 0.0, +1e-12, 0.005}`, `i1_hi in {0.01 - 1e-12, 0.01, 0.01 + 1e-12, 0.02}`, `i2_lo in {-1e-12, 0.0, +1e-12, 0.005}`, `i2_hi in {-1e-12, 0.0, +1e-12, 0.01 - 1e-12, 0.01, 0.01 + 1e-12}`, `i1_mean in {-0.001, 0.0, +0.001}`, and `i2_mean in {-1e-12, 0.0, +1e-12}` against an independent specification oracle of `2026-11-02_topic2_fu_b_card.md` §5 and `ACCEPTANCE.md` `V06–V11 / E1–E5`. Every single boundary condition (`>=` vs `>`) matched (`mismatches = 0`).
  2. **Direct Adversarial Defect Probes**:
     - `V07_E2_missing_fplus_gate`: Missing or incomplete `F+` gate runs -> `verdict == "no_verdict"`, `rule == 1`, `gate_4x.state == "missing"`.
     - `E1_V11_failed_fplus_gate`: `F+` gate runs present with `gain < 0.02` -> `verdict == "inconclusive"`, `rule == 2`, `gate_4x.state == "fail"`, and `stage1` is omitted (`stage1 is None`).
     - `V06_E3_fminus_downgrade_scope`: `F-` failure (`pass: False`, missing file, or bad SHA-256) downgrades ONLY raw `keep` (`Rule 3 -> Rule 3b modify`); raw `modify` (`Rule 5`) stays `modify` (`Rule 5`) and raw `stop` (`Rule 4`) stays `stop` (`Rule 4`).
     - `V09_E5_order_check_under_python_O`: Corrupted `test_order_sha256` on a single Stage-1 run returns `verdict == "no_verdict"` even when invoked under `python3 -O` (confirming explicit `if not order_ok:` branching in `src/topic2_fu_b/verdict.py:217`, not `assert`).
     - `cli_byte_identical_reproduction`: Running `scripts/topic2fu_b_verdict.py` from scratch into a temporary output path reproduced `results/topic2/2026-11-02_fu_b/verdict.json` and `gate_4x.json` byte-for-byte.
  3. **Challenger Mutation Sweep (`15/15` mutants killed, `0` survived)**:
     - Ran `pytest -p no:cacheprovider tests/topic2_fu_b -q -x` (1 pytest process at a time) against 15 distinct code mutations in an isolated `PYTHONPATH` shadow copy (`C_M01` missing gate -> pass, `C_M02` gate fail -> `no_verdict`, `C_M03` Stage-1 computed on gate fail, `C_M04` `F-` downgrades `modify`, `C_M05` missing `F-` -> `True`, `C_M06` `F-` SHA ignored, `C_M07` order check disabled, `C_M08` `I1` uses `S` instead of `E`, `C_M09` `I2` uses `E` instead of `S`, `C_M10` `status != "ok"` check disabled, `C_M11` duplicate valid attempts allowed, `C_M12` rerun after valid attempt allowed, `C_M13` `steps` check disabled, `C_M14` `sum(test_num)/sum(test_den)` check disabled, `C_M15` stall `>` instead of `>=`). All `15/15` were killed (`rc = 1`).

### 2.3 Task 3: Pre-Registration Freeze & Provenance Verification (`p03_v2_verify_freeze_and_provenance.py`)
- **Command**:
  ```bash
  CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/p03_v2_verify_freeze_and_provenance.py
  ```
- **Script SHA-256**: `511faabd0c5b8f5ee437884543df317f560b554cac1d4bd5d2a36dda0587ea9b`
- **Output JSON**: `/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_1/p03_v2_verify_freeze_and_provenance.out.json` (SHA-256: `592cdc34d9474e2cc4529391f03e9018ab83f5cf21c463cb47954735685a5846`)
- **Result**: `rc = 0` (`status: "PASS"`):
  1. **Manifest Integrity**:
     - `results/topic2/2026-11-02_fu_b/card_sha256.txt` (`2026-11-01T16:05:18Z`): `28/29` entries match current disk files; the 29th entry (`docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md`, v1 SHA-256 `ec700f83065645fa14ab458fc5be1e719ad8b620e43343d32461487a770b33e7`) matches the preserved v1 file `verification/worker_FU_B_r1/card_v1_frozen_20261101T160518Z.md.txt` byte-for-byte, and a line-by-line diff against the v2 card (`994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae`) confirms that **only line 41** changed (correcting a typographical error in the historical reference `r1` `I2` mean from `-0.43 %` to `-0.01 %` and adding a pointer to `2026-11-02_topic2_fu_b_addendum_01.md`).
     - `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt` (`2026-11-01T16:20:25Z`): `31/31` entries match current disk files.
     - `results/topic2/2026-11-02_fu_b/output_sha256.txt`: `50/50` entries match current disk files.
     - `verification/worker_FU_B_r1/code_sha256_at_freeze.txt`: `33/33` entries match current disk files.
     - `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: `67/67` entries match current disk files (`C1` immutability verified).
  2. **Strict Chronological Ordering (Freeze Before B300 Execution)**:
     - `card_sha256.txt`: `2026-11-01T16:05:18Z`
     - `card_sha256_v2.txt`: `2026-11-01T16:20:25Z`
     - `slurm/jobs.json` job `509` submission: `2026-11-01T16:20:39Z` (`+14s` after `card_sha256_v2.txt`)
     - Earliest B300 task start (`sacct` ledger row for `509_0`): `2026-11-01T16:20:41Z` (`+16s` after `card_sha256_v2.txt`)
     - Earliest gate `job_meta.json` (`Fplus4x_E_s0`): `2026-11-01T16:20:42Z`
     - Latest gate completion (`Fplus4x_S_s0` `run.json` & `.log` end): `2026-11-01T18:16:15Z`
     - Earliest Stage-1 HCP task start (`sacct` ledger row for `516_0` & `hcp4x_E_s0/job_meta.json`): `2026-11-01T19:19:08Z` (`+62m53s` after gate completion)
     - Latest Stage-1 HCP task completion (`hcp4x_S_s4` `run.json` & `.log` end): `2026-11-02T03:07:20Z`
     - Verdict computation (`verdict.json` mtime): `2026-11-02T03:07:45Z`
     - All temporal precedence invariants (`freeze_v1 < freeze_v2 < earliest_gate_start < latest_gate_end < earliest_stage1_start < latest_stage1_end < verdict`) hold strictly.
  3. **C4 Identifier Hygiene**:
     - Scanned all `62` text files under `results/topic2/2026-11-02_fu_b` and `docs/03_empirical_analysis/topic2/2026-11-02*`: `0` BIDS participant prefix strings, `0` 6-digit standalone numbers, and `0` `content_h16` tokens (`c4_scan_b300.json` also confirms `0` hits across `1,096` HCP directory names and `2,192` `r1` pseudonyms/hashes).

### 2.4 Full Regression Test Suite & Layout Audit
- **Pytest Command**:
  ```bash
  CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider /home/juke/git/00IITP-AI/tests/topic2_fu_b /home/juke/git/00IITP-AI/tests/topic2_rgpool -q
  ```
  - **Result**: `rc = 0` (`244 passed, 24 warnings in 134.68s`).

---

## 3. Issues Found

### Blocking Issues
None (`0`).

### Non-Blocking Issues

1. **NB1 — Historical reference rows (`r1 1× F+ (ref.)`) in Table 1.1 of `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` (lines 44–45) have 5th-decimal-place discrepancies (max diff `6.3e-5`)**:
   - **Location**: `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md:44-45`
   - **Finding**:
     - Line 44 (`| r1 1× F+ (seed 0, ref.) | 140 000 | 0.67687 | 0.65817 | 0.67782 | +2.76 % | +2.90 % |`): In `results/topic2/2026-11-01/runs/Fplus_E_s0/run.json`, `0.676876` is the final `val_history` entry at step 8750, whereas `test_nmse` is `0.6769330001800729` (which rounds to `0.67693` at 5 decimals). Similarly, `Fplus_S_s0` `test_nmse` is `0.6778257503505264` (`0.67783` at 5 decimals, truncated to `0.67782`), and `(E - C)/E` from `test_nmse` is `+2.7711%` (`+2.77 %`, vs `+2.76 %` when computed from `0.67687`).
     - Line 45 (`| r1 1× F+ (seeds 0–1 mean, ref.) | 140 000 | 0.67856 | 0.65781 | 0.67769 | +3.06 % | +2.93 % |`): The exact 2-seed means in `results/topic2/2026-11-01/verdict.json` (`gates.F_plus`) are `E = 0.6786168104850819` (`0.67862`), `C = 0.6578459100511622` (`0.65785`), and `S = 0.6777355786371866` (`0.67774`); the relative gains `+3.06 %` and `+2.93 %` match.
   - **Why non-blocking**: These two rows are historical `r1` reference rows manually transcribed into the markdown table (not emitted by `verification/worker_FU_B_r1/report_numbers.py`). All FU-B 4× gate numbers (`0.65510 / 0.63069 / 0.65491`, `+3.73 %`, `+3.70 %`), all 15 FU-B Stage-1 runs, all `r1` vs `FU-B` HCP pairing tables (§1.2, §1.5), and `verdict.json` are 100% exact (`max_diff = 0.0`).

2. **NB2 — Unescaped `%%` in the `.sbatch` `start` echo line of `src/topic2_fu_b/slurm.py` (line 36)**:
   - **Location**: `src/topic2_fu_b/slurm.py:36` and `results/topic2/2026-11-02_fu_b/b300/logs/fub-*.log:1`
   - **Finding**: Line 36 of `src/topic2_fu_b/slurm.py` is `"echo \"start $(date -u +%%FT%%TZ) task=$SLURM_ARRAY_TASK_ID host=$(hostname)\""` as a standalone list element (without `%` formatting on that element, unlike lines 37–38). Consequently, the generated `.sbatch` scripts contain literal `+%%FT%%TZ` on the `start` line and `b300/logs/fub-*.log` prints `start %FT%TZ ...` on line 1, whereas line 39 (`end $(date -u +%FT%TZ)`) prints a valid ISO-8601 UTC timestamp.
   - **Why non-blocking**: Full, authoritative UTC start and end timestamps are recorded in `b300/runs/*/job_meta.json` (`started_utc`), `b300/runs/*/run.json` (`started_utc`, `finished_utc`), and the `sacct` rows of `results/gpu_ledger_2026-10-31.md`.

---

## 4. What Holds

1. **All Headline Statistics & Verdict (`stop`, Rule 4)**:
   - Every FU-B number in `results/topic2/2026-11-02_fu_b/verdict.json`, `gate_4x.json`, `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md`, and `docs/03_empirical_analysis/topic2/2026-11-02_topic2_addendum_06.md` is reproduced to machine precision (`max_abs_diff = 0.0`) from raw `run.json` and `train_log.jsonl`.
   - The 4× `F+` gate passes decisively (`+3.73%` vs `E`, `+3.70%` vs `S`, both `>= +2.00%`).
   - Primary 5-seed paired t-interval for `I1` is `+0.06% [-0.30%, +0.42%]` (`df = 4`); upper bound `+0.425% < δ = +1.00%` triggers Rule 4 (`stop`).
   - Hierarchical bootstrap (`B = 10000`, `seed = 0`: `I1 = [-0.08%, +0.34%]`) and stall sensitivity (`df = 3`, dropping stalled `E_s0`: `I1 = -0.07% [-0.09%, -0.04%]`) both independently confirm `stop`.
   - Pairing with `r1` (`15/15` runs, identical `test_order_sha256`) confirms that 4× training budget improved `13/15` `(arm, seed)` runs and lowered `E` 5-seed mean NMSE from `0.988922` to `0.988111`, ruling out under-training as the cause of the null `C` vs `E/S` effect.
2. **All `r1` Verdict-Code Defect Classes Fixed & Guarded**:
   - Missing `F+` gate -> `no_verdict` (`Rule 1`); failed `F+` gate -> `inconclusive` (`Rule 2`, `stage1` omitted); `F-` failure downgrades `keep` only (`Rule 3 -> Rule 3b modify`) and never touches `modify` or `stop`; boundary comparisons (`>=` vs `>`) verified across `19,440` synthetic boundary inputs (`0` mismatches); `test_order_sha256` check uses explicit `if/else` (`no_verdict` under `python3 -O`); `15/15` challenger mutants killed by `tests/topic2_fu_b`.
3. **Pre-Registration Freeze, C1 Immutability, C4 Hygiene, and GPU Budget Cap**:
   - Card freeze (`16:05:18Z` v1, `16:20:25Z` v2) strictly precedes job `509` submission (`16:20:39Z`) and earliest task start (`16:20:41Z`); gate completion (`18:16:15Z`) strictly precedes Stage-1 HCP start (`19:19:08Z`).
   - `PROTECTED_HASHES.txt` (`67/67` OK), `card_sha256_v2.txt` (`31/31` OK), `output_sha256.txt` (`50/50` OK), `0` C4 identifier hits, and total FU-B GPU usage `30.72 GPU-h <= 33.0 GPU-h` cap.

---

## 5. What Remains Unverified

- Direct inspection of node-local `/scratch/iitp4/fu_b/` raw tensors and `.pt` checkpoints on `b300-01` (outside read-only local filesystem scope; verified indirectly via copied-back `view_check.json`, `smoke_result.json`, `c4_scan_b300.json`, and `output_sha256.txt`).
