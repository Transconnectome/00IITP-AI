# Handoff — auditor_FU_D_r3_1 (Forensic Audit, Milestone FU_D Iteration 3) — Hard Handoff

## Forensic Audit Report

**Work Product**: Milestone FU_D Iteration 3 gate repair (`worker_FU_D_r3`):
- `tests/topic2_fu_d/test_fud_r3_guards.py` (174 tests)
- `tests/topic2_fu_d/test_fud_r3_oracle.py` (2 tests, 3,000 seeded scenarios)
- `tests/topic2_fu_d/test_fud_r3_full_output.py` (18 tests)
- `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md`
- `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt` (102 entries)
- `verification/worker_FU_D_r3/**` (incl. `mutation/union_r3.out.json`, `probes/errata_probe.out.json`, `c4_scan_r3.py`)
plus all frozen and receipt-pinned FU-D and Topic 2 r1 artifacts.

**Profile**: General Project (Development mode inferred from `ORIGINAL_REQUEST.md`: no from-scratch or no-delegation constraint).
**Verdict**: **CLEAN**

### Phase Results
- **C1 Protected Hashes (`sentinel/PROTECTED_HASHES.txt`)**: **PASS** — `rc=0`, 67/67 OK.
- **Frozen / Receipt-Pinned Files**: **PASS** — 100% untouched and verified (`rc=0`, 0 mismatches):
  - `results/topic2/2026-11-02_fu_d/card_sha256.txt`: 1/1 OK (`1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b`)
  - `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`: 29/29 OK
  - `results/topic2/2026-11-02_fu_d/output_sha256.txt`: 34/34 OK (`verdict.json` sha256 `f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`)
  - `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`: 23/23 OK
  - `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt`: 102/102 OK
  - `results/topic2/2026-11-01/code_sha256_at_freeze.txt`: 33/33 OK
- **Hardcoded Outputs / Facade Detection / Self-Certifying Tests**: **PASS** — No production code in `src/topic2_fu_d/` or `scripts/topic2fu_d_*.py` was modified (all 29 freeze-pinned files are byte-identical to their pre-result freeze receipt). The three new test files (`test_fud_r3_guards.py`, `test_fud_r3_oracle.py`, `test_fud_r3_full_output.py`) contain zero `skip`, `xfail`, or `importorskip` calls, compute expected values from independent `scipy.stats.t.ppf(0.975, df)` t-quantiles, hand arithmetic, card literals (`delta = 0.01`, `floor = 0.999`, `B = 10000`, `seed = 0`), and the frozen r1 `stats.hierarchical_bootstrap`, and always write script outputs into `tmp_path`. `test_fud_r3_full_output.py::test_the_expectation_builder_is_discriminating` also self-tests that single-leaf mutations of the expected dict raise `AssertionError`.
- **Behavioral Verification & Independent Mutant Probe (Tests Can Fail)**: **PASS** —
  - `tests/topic2_fu_d`: `389 passed, 2 warnings in 82.50s` (`rc=0`).
  - `tests/topic2_rgpool tests/topic1_lagmotif`: `204 passed, 24 warnings in 115.49s` (`rc=0`).
  - Old 86 suite (`STRICT_E2E=1`): `86 passed, 7 warnings in 34.11s` (`rc=0`).
  - Independent 12-mutant probe (`verification/auditor_FU_D_r3_1/probe_r3_mutants.py`) executed sequentially against the 3 new r3 test files alone on a copied work tree: baseline `CTRL` `SURVIVED` (`194 passed in 15.21s`), and **12/12 targeted mutants were `KILLED`** (`M01_B1_C12`, `M02_B1_conj_keep_stop`, `M03_B1_stall_arm_E_dropped`, `M04_B1_stall_single_seed`, `M05_gate_incomplete_stage1`, `M06_post_checks_truthy`, `M07_token_regex_3digit`, `M08_fminus_flag_dropped`, `M09_secondary_boot_seed`, `M10_per_subject_axis`, `M11_delta_forwarding`, `M12_floor_vs_stall_order`).
- **Mutation Record Authenticity (`verification/worker_FU_D_r3/mutation/union_r3.out.json`)**: **PASS** —
  - Re-running the exact deduplication logic over `collected.json` (1,518 entries) + `sweep_r3.json` (533 entries) against the repo files reproduces `raw = 2051`, `not_applied = ["rev2_1:R42"]`, and `distinct = 1675` identically.
  - `CTRL` baseline survived (`383 passed, 1 deselected in 34.45s`, `shipped_changed = false`).
  - All 1,511 `KILLED` entries have `rc in (1, 2)` and a concrete `FAILED`/`ERROR` test line; all 164 `SURVIVED` entries have `rc == 0` and `"383 passed"` in `A.tail`; `invalid = 0` (`[]`).
  - All 515 `shipped_changing` mutants are `KILLED` (`survivors_changing_shipped_output = []`).
  - All 50 non-equivalent `exp3_3:W*` sweep survivors from `explorer_FU_D_r3_3` O5 are `KILLED`.
  - The 10-class partition in `addendum_02.md` §5 (`61 + 41 + 9 + 9 + 6 + 3 + 6 + 14 + 7 + 8 = 164`) is pairwise disjoint and matches the exact 164 surviving UIDs in `union_r3.out.json` with 0 missing and 0 extra. Inspection of the frozen code confirms every class's equivalence or decision/output invariance.
  - `verification/worker_FU_D_r3/mutation/run1_test_snapshot/` preserves snapshots of all 3 r3 test files, and all 3 match the shipped SHA-256 hashes.
- **Output & Errata Reproduction**: **PASS** —
  - Independent regeneration of `verdict.json` (`scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989b…b84e --out verification/auditor_FU_D_r3_1/regen_verdict.json`) is byte-identical to `results/topic2/2026-11-02_fu_d/verdict.json` (sha256 `f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`).
  - Independent exact `Fraction` arithmetic over `runs/Fplus_{E,C,S}_s0/run.json` yields `(E - C)/E = 0.003631` and `(S - C)/S = 0.006546`, both `< 0.01`, confirming `inconclusive` (measurement capacity at E192).
  - Independent re-execution of `verification/worker_FU_D_r3/probes/errata_probe.py` into `verification/auditor_FU_D_r3_1/errata_repro.json` matches `errata_probe.out.json` identically across `E5`, `E2'`, `E6`, `E7`, `E8`, `W4`, `W5`, and `E9`.
- **C4 Participant-ID / BIDS / 16-Hex Scan**: **PASS** —
  - `scripts/topic2fu_d_c4scan.py`: `{"n_files": 84, "token_hits": 0, "bids_hits": 0, "files_with_hits": []}` (`rc=0`).
  - `verification/worker_FU_D_r3/c4_scan_r3.py`: `{"n_files": 36, "token_hits": 0, "bids_hits": 0, "six_digit_hits": 0, "files_with_token_or_bids_hits": [], "files_with_six_digit_hits": []}` (`rc=0`).
- **C5 GPU Ledger (`results/gpu_ledger_2026-10-31.md`)**: **PASS** —
  - `0.0` GPU-h used in FU-D r3 (`0` rows for `*_FU_D_r3*`).
  - FU-D worker + explorer total = `3.672` GPU-h (`0.097` explorer + `3.575` worker; `3.720` GPU-h including `0.048` r1 verifiers), well within the `25.0` GPU-h cap.
- **Git Writes & Layout Compliance**: **PASS** —
  - `git log --since="2026-11-01T23:30:00Z"` shows only host `Chavis Autocommit` commits (`docs(auto)`). Zero agent git writes.
  - Whole-run `audit_layout.py` on `.agents/teamwork/tw-20261031-four-topics`: `status: PASS`, `findings: []`.

---

## 1. Observation
- **C1 & Receipt Hashes** (`verification/auditor_FU_D_r3_1/receipts_check.log`):
  - `PROTECTED_HASHES.txt`: `rc=0 lines=67 non_ok=0`
  - `results/topic2/2026-11-02_fu_d/card_sha256.txt`: `rc=0 total=1 ok=1 bad=0`
  - `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`: `rc=0 total=29 ok=29 bad=0`
  - `results/topic2/2026-11-02_fu_d/output_sha256.txt`: `rc=0 total=34 ok=34 bad=0`
  - `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`: `rc=0 total=23 ok=23 bad=0`
  - `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt`: `rc=0 total=102 ok=102 bad=0`
  - `results/topic2/2026-11-01/code_sha256_at_freeze.txt`: `rc=0 total=33 ok=33 bad=0`
- **Test Suites** (`verification/auditor_FU_D_r3_1/pytest_{fud,rgpool_topic1,old86}.out`):
  - `tests/topic2_fu_d`: `389 passed, 2 warnings in 82.50s (0:01:22)`, `rc=0`
  - `tests/topic2_rgpool tests/topic1_lagmotif`: `204 passed, 24 warnings in 115.49s (0:01:55)`, `rc=0`
  - `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` (`STRICT_E2E=1`): `86 passed, 7 warnings in 34.11s`, `rc=0`
- **Independent 12-Mutant Probe on the 3 New r3 Test Files** (`verification/auditor_FU_D_r3_1/probe_r3_mutants.out.json`):
  - `CTRL`: `SURVIVED (17.43s) 194 passed in 15.21s`
  - `M01_B1_C12` (`verdict.py:96` `if c2 != cat:` -> `if c2 != cat and c2 != "inconclusive":`): `KILLED (2.94s)`
  - `M02_B1_conj_keep_stop` (`verdict.py:96` `keep -> stop` exemption): `KILLED (2.89s)`
  - `M03_B1_stall_arm_E_dropped` (`topic2fu_d_verdict.py:90` `"ECS"` -> `"CS"`): `KILLED (3.32s)`
  - `M04_B1_stall_single_seed` (`topic2fu_d_verdict.py:90` `[:1]` slice on `stalled`): `KILLED (4.16s)`
  - `M05_gate_incomplete_stage1` (`topic2fu_d_verdict.py:66` `if gate_failed:`): `KILLED (5.06s)`
  - `M06_post_checks_truthy` (`records.py:87` `is not True` -> `not ...`): `KILLED (6.62s)`
  - `M07_token_regex_3digit` (`records.py:19` `^h\d{2}$` -> `^h\d{2,3}$`): `KILLED (6.64s)`
  - `M08_fminus_flag_dropped` (`topic2fu_d_verdict.py:110` `if False:`): `KILLED (6.87s)`
  - `M09_secondary_boot_seed` (`topic2fu_d_verdict.py:98` `seed=0` -> `seed=1`): `KILLED (9.67s)`
  - `M10_per_subject_axis` (`topic2fu_d_verdict.py:102` `.mean(0)` -> `.mean(1)`): `KILLED (10.26s)`
  - `M11_delta_forwarding` (`verdict.py:133` `delta` -> `DELTA`): `KILLED (11.04s)`
  - `M12_floor_vs_stall_order` (`verdict.py:79` `and not stalled_seeds`): `KILLED (2.80s)`
- **Mutation Audit & Errata Reproduction** (`verification/auditor_FU_D_r3_1/audit_checks.out.json`):
  - `recomputed_raw = 2051`, `recomputed_distinct = 1675`, `recomputed_not_applied = ["rev2_1:R42"]`, `matches_summary_counts = true`.
  - `killed_count = 1511`, `survived_count = 164`, `invalid_count = 0`, `bad_killed = []`, `bad_surv = []`.
  - `shipped_changing_count = 515`, `surv_changing_count = 0`, `o5_50_all_killed = true`.
  - `class_sizes = [61, 41, 9, 9, 6, 3, 6, 14, 7, 8]`, `class_sum = 164`, `partition_exact_match = true`.
  - `verdict_byte_identical = true`, `verdict_sha256 = "f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc"`, `errata_probe_identical = true`.
- **C4 & C5 Checks**:
  - `c4scan_frozen.json`: 84 files, 0 token hits, 0 BIDS hits.
  - `c4scan_r3.json`: 36 files, 0 token hits, 0 BIDS hits, 0 six-digit hits.
  - `c5_gpu_ledger`: `fud_worker_and_explorer_gpuh = 3.672`, `fud_including_r1_verifiers_gpuh = 3.72`, `fud_r3_gpuh = 0.0`, `within_25_gpuh_cap = true`.

## 2. Logic Chain
1. All protected hashes (C1, 67/67) and all six freeze/output/addendum receipts (`card_sha256.txt` 1/1, `code_sha256_at_freeze.txt` 29/29, `output_sha256.txt` 34/34, `addendum_01_sha256.txt` 23/23, `addendum_02_sha256.txt` 102/102, r1 `code_sha256_at_freeze.txt` 33/33) verify with zero mismatches, proving that no frozen or receipt-pinned artifact was modified (Obs: `receipts_check.log`).
2. The three new r3 test files (`test_fud_r3_{guards,oracle,full_output}.py`) use independent `scipy` t-quantiles, exact card literals, and independent arithmetic without self-certifying calls to the FU-D code under test, and our independent 12-mutant probe against those 3 files alone killed 12/12 targeted defects while `CTRL` survived with 194 passed. Thus the tests are genuine and capable of failing on every targeted defect class (Obs: source inspection, `probe_r3_mutants.out.json`).
3. `union_r3.out.json` is internally consistent, matches our independent recomputation of the 2,051 -> 1,675 deduplication and the `run1_test_snapshot` hashes, kills all 515 output-changing mutants and all 50 `explorer_FU_D_r3_3` O5 sweep survivors, and partitions all 164 surviving distinct mutants into 10 verified equivalence/decision-invariance classes (Obs: `audit_checks.out.json`).
4. Both `verdict.json` and `errata_probe.out.json` reproduce identically from the frozen code, C4 scans report 0 hits across all frozen and r3 paths, C5 GPU usage is 0 GPU-h in r3 and 3.672 GPU-h total (`<= 25` GPU-h cap), `audit_layout.py` passes with 0 findings, and `git log` confirms zero agent git writes (Obs: `audit_checks.out.json`, `c4scan_*.json`, `audit_layout.out`, `git_log_r3.out`).
5. Therefore, Milestone FU_D Iteration 3 exhibits zero integrity violations and merits a **CLEAN** verdict.

## 3. Caveats
- Two minor nonblocking documentation precision notes in `addendum_02.md` §5:
  1. Line 190 states `Baseline control (CTRL): SURVIVED (383 passed, 1 deselected in Leg A; 189 passed, 1 deselected in Leg B; shipped_changed = False)`. In `run_union_r3.py:134`, Leg B is executed only when `rec["A"]["status"] == "KILLED"`, so the `control` object in `union_r3.out.json` records Leg A and `shipped` only (`189 passed, 1 deselected` is the pre-r3 suite count when the 3 r3 files are ignored).
  2. Line 196 states that the 34 distinct `killed_only_by_r3_files` mutants represent `91 raw aliases across the r2 verifier and r3 explorer lists`. Across all 11 collected lists + `sweep_r3.json`, those 34 distinct mutants have 120 total aliases (`114` in `collected.json` including `wr2:*` + `6` in `sweep_r3.json`); excluding `wr2:*` and `exp3_3:W*` sweep aliases gives the 91 targeted verifier/explorer aliases.
- I did not re-execute all 1,675 mutants from scratch; instead, I verified the deduplication and JSON structure of all 1,675 entries, verified `run1_test_snapshot`, audited all 164 surviving mutants across the 10 classes, and ran an independent 12-mutant probe against the 3 r3 test files.

## 4. Conclusion
**CLEAN**. Milestone FU_D Iteration 3 is a genuine, additive test-and-addendum gate repair (`389 passed` in `tests/topic2_fu_d`, `194` new tests) with authentic mutation and errata-probe evidence, 100% intact receipts and protected hashes, zero C4 leaks, zero r3 GPU usage (`3.672` GPU-h FU-D total <= `25` GPU-h cap), and zero agent git writes. The shipped verdict **`inconclusive` (measurement capacity at E192)** is unchanged and byte-identically reproducible.

## 5. Verification Method
```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for r in results/topic2/2026-11-02_fu_d/{card_sha256,code_sha256_at_freeze,output_sha256,addendum_01_sha256,addendum_02_sha256}.txt results/topic2/2026-11-01/code_sha256_at_freeze.txt; do
  grep -v '^#' "$r" | LC_ALL=C sha256sum -c | grep -vc ': OK$'
done
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/auditor_FU_D_r3_1/audit_checks.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/auditor_FU_D_r3_1/probe_r3_mutants.py /tmp/probe_r3_check.json
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
```
Invalidation: any mismatch in C1 or the 6 receipts, any non-equivalent verdict-path mutant surviving the 389-test suite, or any C4/C5 violation.
