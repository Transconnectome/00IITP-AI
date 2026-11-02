# Hard handoff — auditor_FU_B_r1_1 (Forensic Integrity Audit, Milestone FU_B, Iteration 1)

## Forensic Audit Report

**Work Product**: Milestone FU_B (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds`) as delivered by `worker_FU_B_r1`: `/home/juke/git/00IITP-AI/src/topic2_fu_b/`, `/home/juke/git/00IITP-AI/scripts/topic2fu_b_*.py`, `/home/juke/git/00IITP-AI/tests/topic2_fu_b/`, `/home/juke/git/00IITP-AI/results/topic2/2026-11-02_fu_b/`, `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_*.md`, `/home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md`, and B300 `/scratch/iitp4/fu_b/`.
**Profile**: General Project (Development Mode inferred from `ORIGINAL_REQUEST.md`: no "from scratch" or "do not delegate" constraints).
**Verdict**: **CLEAN**

Audit window: `2026-11-02T03:49:28Z` to `2026-11-02T04:06:00Z`. I used `0.00 GPU-h`, added no ledger rows, made zero git writes, and modified zero production files. All probes and outputs are under `/home/juke/git/00IITP-AI/verification/auditor_FU_B_r1_1/`.

### Phase Results
- **C1 Protected Hashes & Pinned Receipts**: **PASS**
  - `PROTECTED_HASHES.txt`: `rc=0`, `67/67 OK` at audit start (`probes/c1_start.log`) and at audit end (`probes/c1_end.log`).
  - `results/topic2/2026-11-01/code_sha256_at_freeze.txt`: `rc=0`, `33/33 OK` (`probes/r1_code_sha256.log`), confirming all 13 Python modules of `src/topic2_rgpool` are untouched.
  - `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt`: `rc=0`, `31/31 OK` (`probes/card_sha256_v2.log`).
  - `results/topic2/2026-11-02_fu_b/output_sha256.txt`: `rc=0`, `50/50 OK` (`probes/output_sha256.log`).
  - `results/topic2/2026-11-02_fu_b/card_sha256.txt` (v1): `28/29 OK`; only `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md` line 41 differs (replacing one ordinary English hyphenated word that tripped the frozen r1 BIDS-prefix regex with `"not be optimal"`), with exact v1 bytes preserved at `verification/worker_FU_B_r1/card_v1_frozen_20261101T160518Z.md.txt` (sha256 `a9c4cab03ac99305e44b0aa2ab550fbe402f7f4b74ac3c239d082021e76e0726`).
- **Card Freeze Order vs Slurm Execution (C3 / F1)**: **PASS**
  - Card v1 was frozen at `2026-11-01T16:05:18Z` (`card_sha256.txt`, git anchor `35d10a555706e1367683f68a3f83a157f210dfa1` committed `2026-11-01T16:05:25Z`).
  - Card v2 + `addendum_01.md` was frozen at `2026-11-01T16:20:25Z` (`card_sha256_v2.txt`, git anchor `e5fa8de1d4443aa951ea6ce1f0018d11930a6566` committed `2026-11-01T16:20:26Z`).
  - Although `jobs.json` records `sbatch` submission of job `509` at `16:12:37Z` and job `516` (`--dependency=afterany:509`) at `16:14:13Z` (and Slurm queued job `516` at `17:58:26Z` while waiting on dependency/resources), `TZ=UTC sacct` on B300 (`probes/b300_sacct_and_hashes.json`) and `job_meta.json` / `train_log.jsonl` (`probes/freeze_and_ledger.json`) prove that the earliest gate task (`509_0`) started at `2026-11-01T16:20:41Z` (first training log entry `16:21:04Z`) and the earliest Stage-1 task (`516_0`) started at `2026-11-01T19:19:08Z` (first training log entry `19:19:30Z`). All 18 post-freeze training tasks started strictly after both v1 (`16:05:18Z`) and v2 (`16:20:25Z`) freezes, and zero code/test files changed after `16:05:18Z`.
- **Source Code Inspection (Hardcoded Results, Facades, Silent Fallbacks)**: **PASS**
  - Full inspection of `src/topic2_fu_b/{__init__,budget,design,records,slurm,verdict,view}.py` and `scripts/topic2fu_b_{c4scan,make_view,run,slurm,smoke,verdict}.py` found zero hardcoded output values, zero facade functions, and zero silent fallbacks.
  - `records.validate()` and `records.resolve()` fail closed on any incomplete status, parameter drift, partition/split/code hash mismatch, non-finite or mismatched `test_nmse != sum(num)/sum(den)`, duplicate valid attempts, or non-positional test tokens.
  - `verdict.decide()` implements the exact 4-rule precedence table of card §8 using the frozen `src/topic2_rgpool/stats.py` primitives.
- **Authenticity of B300 Run Records & Independent Re-computation**: **PASS**
  - On B300 (`connectome@61.107.201.98`), `TZ=UTC sacct` confirms all 22 FU-B tasks (`402`, `413`, `419`, `490`, `509_0..2`, `516_0..14`) ran on `b300-01` and finished `COMPLETED` (`probes/b300_sacct_and_hashes.json`).
  - All 39 result files on B300 (`18 × run.json`, `18 × train_log.jsonl`, `view_check.json`, `smoke_result.json`, `c4_scan_b300.json`) are byte-identical (`39/39` sha256 match) to the copies in `results/topic2/2026-11-02_fu_b/b300/`.
  - All 18 `runs/*/model_final.pt` checkpoints exist on B300 (`/scratch/iitp4/fu_b/runs/*/model_final.pt`, each `154,992,434` bytes, ~155 MB) with mtimes matching the Slurm completion times, and zero `.pt`/`.npy` files were copied into the local repository (`forbidden_binary_files_in_local_results: []`).
  - Re-running `scripts/topic2fu_b_verdict.py` reproduces `results/topic2/2026-11-02_fu_b/verdict.json` byte-for-byte (sha256 `262b9c793af333af1658f95dfc96de3769c95d3fdddc300dd667813ee5f1e142`).
  - My independent script `verification/auditor_FU_B_r1_1/scripts/indep_verdict.py` (importing only Python stdlib, `numpy`, and `scipy.stats`) verified all 18 `run.json` and `train_log.jsonl` records (`0` issues) and reproduced every metric in `verdict.json` and `gate_4x.json` with `0.0` absolute difference across all 16 quantities (`all_diffs_zero_to_machine_eps: true`):
    - 4× F+ gate (seed 0): `E = 0.655099`, `C = 0.630692`, `S = 0.654914`; gains `+3.726 %` (C vs E) and `+3.699 %` (C vs S) ≥ `1.00 %` → `pass`.
    - Stage 1 (5 seeds, df = 4): `I1 = +0.063 % [−0.299 %, +0.425 %]` (`hi = 0.0042496 < δ = 0.01`), `I2 = −0.092 % [−0.646 %, +0.461 %]`; hierarchical bootstrap `I1 [−0.078 %, +0.338 %]`, `I2 [−0.496 %, +0.228 %]`; stall sensitivity (dropping `E_s0`, seeds 1–4, df = 3) `I1 = −0.067 % [−0.091 %, −0.043 %]` → governing verdict **`stop`** (rule 4).
  - `verification/auditor_FU_B_r1_1/scripts/check_report_numbers.py` verified `44/44` quantitative values in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` against `verdict.json` and `gate_4x.json` (`0` mismatches).
- **C4 Participant-ID, BIDS Prefix, and 16-Hex Content-Hash Scan**: **PASS**
  - `verification/auditor_FU_B_r1_1/scripts/c4_scan.py` scanned `results/topic2/2026-11-02_fu_b/` (120 files), `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_*.md` (3 files), FU-B code/tests (20 files), and FU-B teamwork metadata (16 files):
    - **Positional tokens**: All 22 `run.json` files (18 main + 4 smoke) use strictly positional `hNN` tokens (`h13..h85`, `bad_pseudonym_files: []`).
    - **BIDS four-character prefix**: `0` hits across all 159 scanned files (`bids_hit_files: []`).
    - **16-hex content hashes**: `0` non-float hits in `results/`, `docs/`, and metadata (`hex16_non_float_hits: []`). All `7,528` regex matches of `[0-9a-f]{16}` in `results/topic2/2026-11-02_fu_b/` are verified to be 16-character decimal/scientific-notation fractional parts immediately following `.` in standard floats (e.g., `1.0000091020588155` or `7.47994307121662e-05`). In `tests/`, the single match is the synthetic negative test fixture `"0123456789abcdef"` in `tests/topic2_fu_b/test_records.py:27`.
    - **HCP 6-digit IDs**: Across all 159 files, the 27 unique standalone 6-digit integers (timestamps `160518`/`161237`/`161413`, sample count `560000`, and 6-decimal NMSE fractions `984860..994161`) were tested in memory on B300 against the `1,084` staged HCP directory names in `/scratch/data/hcp/download_HCP_REST1_filtered`: **`hits = 0`** (`pos_control_hit = 1`, `neg_control_hit = 0`).
- **C5 GPU Ledger Accounting & Project-Local Venv**: **PASS**
  - In `results/gpu_ledger_2026-10-31.md`, all 22 FU-B GPU tasks (`402`, `413`, `419`, `490`, `509_0..2`, `516_0..14`) were launched via Slurm `sbatch` on `b300-01` and have closing `completed` rows whose GPU-h values match `ceil(ElapsedRaw * 1 / 36) / 100`: explorers `0.06 + 0.065 + 0.015 = 0.14 GPU-h`, worker smoke `0.07 GPU-h`, gate `3 × 1.69 = 5.07 GPU-h`, Stage 1 `6 × 1.69 + 9 × 1.70 = 25.44 GPU-h` → **FU-B total = `30.72 GPU-h <= 33.0 GPU-h` cap** (whole-run completed total `59.278 GPU-h <= 95.0 GPU-h` ceiling).
  - Project-local venv `/scratch/iitp4/fu_b/venv` on B300 was verified (`python 3.12`, `torch 2.15.0+cu134`, matching `scripts/b300_env/lock.txt`).
- **Test Suites, Mutation Spot-Check & Git/Layout Hygiene**: **PASS**
  - Sequential pytest runs (1 process at a time, `CUDA_VISIBLE_DEVICES=""`):
    - `tests/topic2_fu_b`: `128 passed in 5.13s`
    - `tests/topic2_rgpool`: `116 passed in 114.08s`
    - Old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`, `STRICT_E2E=1`): `86 passed in 42.75s`
    - `tests/topic1_lagmotif`: `88 passed in 8.73s`
  - Isolated mutation spot-check (`verification/auditor_FU_B_r1_1/scripts/spot_mutants.py`): 18 mutants tested in an isolated copy; `17/17` non-equivalent mutants across `verdict.py`, `records.py`, `budget.py`, `view.py`, and `topic2fu_b_run.py` were killed (`M01`–`M11`, `M13`–`M18`); the single survivor (`M12_duplicate_last_wins`, changing `elif len(valid) == 1:` to `elif len(valid) >= 1:` after `if len(valid) > 1:`) is an unreachable equivalent branch because `len(valid) > 1` is already caught by the preceding `if` statement (and removing that `if` guard is killed in `worker_FU_B_r1`'s `dup_last_wins` mutant).
  - Git history (`probes/git_commits_since_14z.log`): all 48 commits since `2026-11-01T14:00:00Z` are automated `Chavis Autocommit` snapshots or root `checkpoint four-topics teamwork documents` commits (`0` agent git commits).
  - Metadata layout lint (`audit_layout.py`): `PASS` (`711` inspected files, `0` findings).

---

## 1. Observation
- `probes/c1_start.log` & `probes/c1_end.log`: `rc=0`, `67/67 OK`.
- `probes/r1_code_sha256.log`: `rc=0`, `33/33 OK`.
- `probes/card_sha256_v2.log`: `rc=0`, `31/31 OK`.
- `probes/output_sha256.log`: `rc=0`, `50/50 OK`.
- `probes/freeze_and_ledger.json`: `card_v1_sha256 = a9c4cab03ac99305e44b0aa2ab550fbe402f7f4b74ac3c239d082021e76e0726`, `card_v2_sha256 = 994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae`, `n_card_diffs = 1` (line 41 only), `earliest_gate_start_utc = 2026-11-01T16:20:41Z`, `earliest_stage1_start_utc = 2026-11-01T19:19:08Z`, `all_runs_after_v1_freeze = true`, `all_runs_after_v2_freeze = true`, `fub_total_gpuh = 30.72`.
- `probes/b300_sacct_and_hashes.json`: `n_sacct_rows = 22`, `n_remote_files_hashed = 39`, `n_local_byte_identical = 39`, `mismatches = []`, `n_checkpoints_on_b300 = 18`, `all_checkpoints_nonempty = true`, `forbidden_binary_files_in_local_results = []`.
- `probes/indep_verdict.json`: `cli_byte_identical_to_shipped_verdict_json = true`, `verdict_indep = "stop"`, `all_diffs_zero_to_machine_eps = true`, `issues = []`.
- `probes/report_numbers_check.json`: `n_checks = 44`, `n_passed = 44`, `failed = []`.
- `probes/c4_scan.json`: `bids_hit_files = []`, `hex16_non_float_hits = []` (in results/docs/meta), `b300_hcp_6digit_membership = {"n_staged_hcp_6digit": 1084, "n_query": 27, "hits": 0, "pos_control_hit": 1, "neg_control_hit": 0}`, `bad_pseudonym_files = []`.
- `probes/spot_mutants.json`: `baseline = {"rc": 0, "tail": "128 passed in 6.86s"}`, `n_mutants = 18`, `killed = 17`, `survived = ["M12_duplicate_last_wins"]` (equivalent `elif` branch).

## 2. Logic Chain
1. Because `card_sha256.txt` (`16:05:18Z`, git commit `35d10a55` at `16:05:25Z`) and `card_sha256_v2.txt` (`16:20:25Z`, git commit `e5fa8de1` at `16:20:26Z`) both precede the start of the earliest gate job (`509_0` at `16:20:41Z`) and Stage-1 job (`516_0` at `19:19:08Z`) in B300 `sacct` and `train_log.jsonl`, and all 31 entries in `card_sha256_v2.txt` verify with `rc=0`, the analysis card and FU-B code were genuinely frozen before any FU-B outcome was computed (C3, F1).
2. Because all 39 result files on B300 match the repo copies byte-for-byte, all 18 `model_final.pt` checkpoints exist on B300 with mtimes matching `sacct` completion times, and `indep_verdict.py` reproduces every gate and Stage-1 statistic (`I1`, `I2`, t-intervals, hierarchical bootstrap, stall sensitivity, and `stop` verdict) to machine precision (`0.0` difference) from the raw `run.json` and `train_log.jsonl` files, the results are authentic and not hardcoded or fabricated.
3. Because all 4 pytest suites pass (`128 + 116 + 86 + 88 = 418` tests) and 17/17 non-equivalent mutants in an isolated workspace cause test failures, the test suite is genuine and capable of failing on targeted defects (F2).
4. Because C4 scans confirm positional `hNN` tokens only, 0 BIDS prefixes, 0 hex content hashes, and 0/27 6-digit matches against the 1,084 staged HCP subject directories on B300, and C5 ledger checks confirm all 22 FU-B Slurm tasks are logged at `30.72 GPU-h <= 33.0 GPU-h` using `/scratch/iitp4/fu_b/venv`, all data and compute governance rules (C1–C8, F1–F3) hold. Therefore the forensic verdict is **CLEAN**.

## 3. Caveats
- **No GPU re-training executed during audit:** Under the ≤1 GPU-h verifier cap, full 35,000-step runs (~1.70 GPU-h each) cannot be re-run from scratch by an auditor. Authenticity of the B300 runs is established via B300 `sacct` records, checkpoint file sizes/timestamps on `/scratch/iitp4/fu_b/runs/*/model_final.pt`, bit-identical 200-step anchor reproduction in job `490`, and byte-identity between B300 and repo records.
- **Equivalent mutant `M12_duplicate_last_wins`:** In `spot_mutants.py`, mutating `elif len(valid) == 1:` to `elif len(valid) >= 1:` in `src/topic2_fu_b/records.py:187` cannot change behavior because `if len(valid) > 1:` on line 185 already catches all `len(valid) > 1` cases. Removing the `if len(valid) > 1:` guard itself is killed by `tests/topic2_fu_b/test_records.py::test_rerun_after_a_valid_attempt_is_an_integrity_error_not_last_wins`.

## 4. Conclusion
**CLEAN.** Milestone FU_B (`worker_FU_B_r1`) exhibits zero integrity violations. All frozen card, code, test, C1, C4, and C5 constraints are satisfied, and the governed verdict **`stop` (killed; `I1 = +0.06 % [−0.30 %, +0.42 %] < δ = 1.00 %`)** is authentic and independently reproduced.

## 5. Verification Method
```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_b/card_sha256_v2.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_b/output_sha256.txt
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_FU_B_r1_1/scripts/check_freeze_and_ledger.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_FU_B_r1_1/scripts/check_b300.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_FU_B_r1_1/scripts/indep_verdict.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_FU_B_r1_1/scripts/c4_scan.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_FU_B_r1_1/scripts/check_report_numbers.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_FU_B_r1_1/scripts/spot_mutants.py
/home/juke/superclaude-env/bin/python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics
```
This audit is invalidated if any receipt in `PROTECTED_HASHES.txt`, `code_sha256_at_freeze.txt`, `card_sha256_v2.txt`, or `output_sha256.txt` fails, if `indep_verdict.py` reports any discrepancy against `verdict.json`, or if `c4_scan.py` reports any non-zero hit.
