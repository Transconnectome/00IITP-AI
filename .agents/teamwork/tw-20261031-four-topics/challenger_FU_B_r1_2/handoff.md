# Handoff Report — challenger_FU_B_r1_2 (Hard Handoff)

- **Milestone:** `FU_B_r1` (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds (§7 ≈26 GPU-h; cap 33)`)
- **Challenger Verdict:** **`CONFIRMED`**
- **Timestamp:** `2026-11-02T04:06:30Z`

---

## 1. Observation

1. **Receipt, Protected-File, and Test-Suite Verification (C1, C2, C3, F1, F2):**
   - `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: **67/67 OK** (`rc = 0`).
   - `grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c`: **31/31 OK** (`rc = 0`).
   - `grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c`: **50/50 OK** (`rc = 0`).
   - Sequential pytest runs (single process at a time, CPU only):
     - `tests/topic2_fu_b` (128) + `tests/topic2_rgpool` (116): **244 passed in 146.27s** (`rc = 0`).
     - `STRICT_E2E=1` `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`: **86 passed in 46.99s** (`rc = 0`).
     - `tests/topic1_lagmotif`: **88 passed in 7.25s** (`rc = 0`).
   - `scripts/topic2fu_b_verdict.py results/topic2/2026-11-02_fu_b/b300/runs` reproduces `results/topic2/2026-11-02_fu_b/verdict.json` **byte-identically** (`cmp -s` `rc = 0`).

2. **Task 1 — Mutation Coverage & Challenger Adversarial Probes (`/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_2/adversarial_mutants.py` → `adversarial_mutants.out.json`):**
   - Verified `verification/worker_FU_B_r1/mutation/mutants_v2.out.json` (sha256 `72c2474b54bc43a9efe5182d4527f229d2874d045569d7f7a067eb257b218a0e`): **44/44 worker mutants killed** (`survived: []`, `errors: []`). All 6 mutants that had survived in `mutants_v1.out.json` (`V11b_fail_branch_falls_through`, `V08b_stage1_missing_ignored`, `dup_last_wins`, `rerun_after_valid_allowed`, `stall_ge_to_gt`, `ledger_counts_started_rows`) were killed after the worker expanded `tests/topic2_fu_b/` from 125 to 128 tests before freezing the card.
   - Executed 34 mutants in an isolated temporary copy (`/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_2/_work_tree`, removed in `finally:`):
     - **Group A (12 worker critical & v1-survivor mutants re-tested independently):** **12/12 killed** (`W_V07_missing_gate_not_no_verdict`, `W_V07b_gate_missing_state_dropped`, `W_caseA_gate_fail_gives_no_verdict`, `W_V11_stage1_read_after_gate_fail`, `W_V11b_fail_branch_falls_through`, `W_V08_status_not_checked`, `W_V08b_stage1_missing_ignored`, `W_V09_order_check_removed`, `W_dup_last_wins`, `W_rerun_after_valid_allowed`, `W_stall_ge_to_gt`, `W_ledger_counts_started_rows`).
     - **Group B (14 new challenger adversarial mutants on governing verdict/record/wrapper/budget paths):** **13/14 killed** (`C01_gate_single_arm_ce_only`, `C03_stage1_resolve_skips_errors_check`, `C04_perm_file_sha_not_checked`, `C05_n_train_windows_not_checked`, `C06_distinct_test_tokens_not_checked`, `C07_batch_not_checked`, `C08_warmup_frac_not_checked`, `C09_lr_not_checked`, `C10_unrecognised_dir_ignored`, `C11_out_of_design_seed_ignored`, `C12_split_order_ignored_in_view`, `C13_wrapper_gate_role_allows_custom_subdir`, `C14_g3t_running_not_blocking`). The single survivor in Group B, `C02_stage1_errors_ignored_in_decide` (`src/topic2_fu_b/verdict.py:81`), is a defense-in-depth equivalent mutant in `run_verdict()` because `run_verdict()` (`verdict.py:153`, guarded by `C03`) omits `stage1["inference"]` whenever `res["errors"]` is non-empty, causing `decide()` (`verdict.py:85`, `if not inf.get("order_ok"):`) to still return `{"verdict": "no_verdict", "rule": 3}`.
     - **Group C (8 challenger probes targeting secondary/descriptive helpers & edge conditions):** Identified 8 non-blocking test-coverage gaps (`C15`–`C22`) where the implementation code is verified correct on all real records (`0.0` error in `audit_fu_b.out.json`) and cannot alter the governing verdict, but `tests/topic2_fu_b/` does not assert those specific helper internals:
       - `C15_fminus_inherited_reads_Fplus_instead_of_Fminus` & `C16_fminus_inherited_hardcodes_true_after_sha` (`src/topic2_fu_b/verdict.py:51`): `_fm_file()` in `test_verdict.py` modifies the file without re-pinning `DS.R1_VERDICT_SHA256`, so modified files exit at line 47 (`if sha != DS.R1_VERDICT_SHA256:`), and line 51 only runs on the real pinned `r1/verdict.json` where both `Fminus.pass` and `Fplus.pass` are `True`.
       - `C17_stall_sensitivity_does_not_drop_stalled_seed` & `C18_stall_sensitivity_min_seeds_5_skips_intervals` (`src/topic2_fu_b/verdict.py:109-114`): `test_stalled_run_is_counted_and_only_flagged` asserts `sens["seeds_kept"] == [0, 2, 3, 4]`, not `sens["I1_t"]` or `sens["verdict_if_governing"]`.
       - `C19_r1_pairing_disabled_in_run_verdict` & `C20_r1_pairing_manipulation_check_inverted` (`src/topic2_fu_b/verdict.py:118-137, 168`): `test_verdict.py` calls `run_verdict(..., r1_runs_dir=None)`, leaving the descriptive `r1_pairing()` helper untested in pytest.
       - `C21_records_test_den_length_unchecked` & `C22_records_val_curve_finite_unchecked` (`src/topic2_fu_b/records.py:96, 109`): `test_records.py` tests `test_den` with a zero element (which also changes `sum(num)/sum(den)`) and `val_nmse_curve` with wrong step keys, rather than preserving `sum(den)` while changing `len(den)` or putting `NaN` in `val_nmse_curve` values.

3. **Task 2 — B300 Provenance, 35,000-Step Schedule, and Hash Audit (`/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_2/audit_fu_b.py` → `audit_fu_b.out.json`):**
   - `b300/view_check.json`: `n_orig = 88`, `sanitized_manifest_is_positional_in_order = true`, `split_check` (`train: true`, `val: true`, `test: true`, `disjoint: true`, sizes `64/8/16`), `r1_files_modified_after_cut = 0`, `preconditions_ok = true`, `links_made = 176`, `links_conflicting = 0`.
   - `b300/c4_scan_b300.json`: `n_tokens_in_memory = 176`, `n_text_files_scanned = 108`, `n_hits = 0`, `n_files_with_hits = 0`. Independent challenger scan of all 123 FU-B result/doc files confirmed `n_bids_prefix_hits = 0`, and all `test_pseudonyms` in `hcp_*` `run.json` match the 16 positional tokens `h13..h85` in `results/topic2/2026-11-01/split.json["test"]`.
   - `slurm/jobs.json` & `results/gpu_ledger_2026-10-31.md`: Gate array job `509` (`0-2`) and Stage-1 array job `516` (`0-14%4`, `dependency: "afterany:509"`), all 18 tasks in `closed`. Total FU-B GPU-h = **30.72 GPU-h** (explorers `0.14` + smoke `0.07` + gate `5.07` + Stage 1 `25.44`) ≤ **33.0 GPU-h** cap.
   - Freeze and gate ordering:
     - `card_sha256_v2.txt` frozen at `2026-11-01T16:20:25Z` < earliest gate task start `2026-11-01T16:20:43Z` (`Fplus_E_s0_a1`).
     - Latest gate task completion `2026-11-01T18:16:15Z` (`Fplus_S_s0_a1`) < earliest Stage-1 task start `2026-11-01T19:19:08Z` (`hcp_E_s0_a1`), with `gate_state_at_start == "pass"` verified in all 15 Stage-1 `job_meta.json` files.
   - All 18 runs (`Fplus_{E,C,S}_s0_a1` and `hcp_{E,C,S}_s{0..4}_a1`) inspected across `run.json`, `job_meta.json`, and `train_log.jsonl`:
     - Every run has `status == "completed"`, `cfg == "E36_d2262"`, `steps == 35000`, `batch == 16`, `lr == 0.0002`, `wd == 0.05`, `warmup_frac == 0.05`, `mask_ratio == 0.6`, `n_params == 38712096`.
     - Every `train_log.jsonl` has exactly **350 `"train"` events** at steps `100, 200, ..., 35000`, **1 `"throughput_probe"` event** at step `200` (with `samples_per_s == round(16 / per_step, 2)` confirming batch 16), **4 `"val"` events** at steps `8750, 17500, 26250, 35000` (`max_val_abs_err = 0.0` vs `run.json["val_nmse_curve"]`), and **1 `"done"` event** (`max_nmse_abs_err = 0.0` vs `sum(test_num)/sum(test_den)`).
     - Across all `18 × 350 = 6,300` logged `"train"` events, the logged learning rate matches the frozen 35,000-step schedule (linear warmup over `1,750` steps to `2e-4`, cosine decay to `0.0` at step `35,000`) with **`max_lr_abs_err = 0.0`**.
     - Every run's `code_sha256` (all 13 files of `src/topic2_rgpool/`), `perm_file_sha256`, `perm_key`, `perm_sha256` (recomputed from `perms_hcp.npz` / `perms_Fplus.npz`), and (for HCP) `split_file_sha256` (`cc521b08...c75a`) and `n_train_windows == 7616` match the frozen pins.

4. **Task 3 — Independent Verdict and Metric Recomputation (`audit_fu_b.py` → `audit_fu_b.out.json`):**
   - Recomputed directly from raw `b300/runs/*/run.json` (`test_num`, `test_den`, `val_nmse_curve`) and `results/topic2/2026-11-01/runs/*/run.json`:
     - **4× F+ gate (seed 0):** `NMSE_E = 0.6550988103`, `NMSE_C = 0.6306915097`, `NMSE_S = 0.6549144352`; `gain_C_vs_E = +3.725743%` (`>= 1%`), `gain_C_vs_S = +3.698640%` (`>= 1%`) → `pass = True`, `state = "pass"` (`gate_gain_ce_diff = 0.0`, `gate_gain_cs_diff = 0.0`).
     - **Inherited 1× F− gate:** `results/topic2/2026-11-01/verdict.json` sha256 matches `59af05e5...af68`, `Fminus.pass is True`.
     - **Stage-1 primary 95 % t-intervals (df = 4):**
       - `I1_t`: `mean = +0.0006313784` (`+0.063%`), `se = 0.0013032023` (`0.130%`), `lo = -0.0029868912` (`-0.299%`), `hi = +0.0042496480` (`+0.425%`) (`I1_t_max_diff = 0.0`).
       - `I2_t`: `mean = -0.0009249384` (`-0.092%`), `se = 0.0019948155` (`0.199%`), `lo = -0.0064634343` (`-0.646%`), `hi = +0.0046135574` (`+0.461%`) (`I2_t_max_diff = 0.0`).
     - **Hierarchical bootstrap (`B = 10,000, seed = 0`):** `I1 = [-0.0779%, +0.3376%]` (median `+0.0605%`), `I2 = [-0.4963%, +0.2281%]` (median `-0.0872%`) (`boot_I1_max_diff = 0.0`, `boot_I2_max_diff = 0.0`).
     - **Stalls & sensitivity (dropping stalled `E_s0`, `seeds_kept = [1, 2, 3, 4]`, df = 3):** `I1_t = -0.0671% [-0.0909%, -0.0432%]`, `I2_t = +0.0911% [-0.2295%, +0.4116%]`, `verdict_if_governing = "stop"` (`sens_I1_t_max_diff = 0.0`, `sens_I2_t_max_diff = 0.0`).
     - **`r1_pairing` & manipulation check:** `E_seed_mean_r1 = 0.98892224` → `E_seed_mean_fub = 0.98811092` (`E_improved = True`); 13/15 `(arm, seed)` pairs have lower test NMSE at 4× budget (`r1_diff_max_err = 0.0`, `delta_I1_max_err = 0.0`).
     - **Governing Verdict (Card §8 Rule 4):** Gate state is `"pass"`, Stage 1 is complete with `order_ok = True`, and `I1_t["hi"] = 0.00424965 < delta = 0.01` → **`stop`** (killed). Every number in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` matches `verdict.json` and `gate_4x.json`.

---

## 2. Logic Chain

1. **Card Freeze and Precedence Integrity (F1, F2, C3):** `card_sha256_v2.txt` was frozen (`16:20:25Z`) prior to the earliest gate task start (`16:20:43Z`), and all 31 pinned files remain byte-identical after execution. Both the worker's 44-mutant suite (`44/44` killed) and our 26 governing-path adversarial mutants (`25/26` killed, 1 defense-in-depth equivalent `C02`) confirm that all V01–V11 / Case A verdict-path defect classes are closed.
2. **B300 Execution and Governance Integrity (F3, C4, C5, C6):** All 18 training runs (`3` gate + `15` Stage-1) ran via Slurm on `b300-01` within the 33.0 GPU-h cap (`30.72 GPU-h` used), accessed HCP tensors exclusively via the verified positional view (`h00..h87`, zero C4 hits), and completed all 35,000 steps with batch 16, linear warmup over 1,750 steps, and cosine decay to 0.0 at step 35,000 (`max_lr_abs_err = 0.0`).
3. **Verdict Validity (F3, C8):** Independent recomputation from the raw `run.json` numerator/denominator arrays reproduces `gate_4x.json` and `verdict.json` with `0.0` numerical error. Because the 4× F+ gate passed (`+3.73%` C vs E, `+3.70%` C vs S) and the Stage-1 upper 95% t-bound for `I1` (`+0.425%`) is strictly below `δ = 1.00%`, the frozen card's precedence rule 4 requires **`stop` (killed)**.

---

## 3. Caveats

- No full 35,000-step GPU re-training was executed by the challenger (verifier GPU cap is ≤ 1 GPU-h and all 18 runs have complete 350-step `train_log.jsonl` traces, `job_meta.json`, and pre-freeze smoke reproduction anchors).
- The 8 surviving challenger mutants in Group C (`C15`–`C22`) are in non-governing descriptive helpers (`r1_pairing`, `stall_sensitivity` interval check) or secondary defense-in-depth checks (`fminus_inherited` post-sha JSON field, `records.py` `len(den)` and `val_nmse_curve` finiteness). They do not affect any shipped number or the governing verdict.

---

## 4. Conclusion

## Challenge Summary

**Overall risk assessment**: LOW  
**Challenger Verdict**: **`CONFIRMED`**

## Challenges

### [Low / Non-Blocking] Challenge 1: Unasserted descriptive helpers (`r1_pairing` and `stall_sensitivity` intervals) in `tests/topic2_fu_b/test_verdict.py`
- **Assumption challenged**: That `tests/topic2_fu_b/` guards the descriptive outputs in `verdict.json["stage1"]["r1_pairing"]` and `verdict.json["stage1"]["stall_sensitivity"]["I1_t"]`.
- **Attack scenario**: Mutants `C17`–`C20` in `adversarial_mutants.py` disable `r1_pairing`, invert `E_improved`, or skip dropping stalled seeds in `stall_sensitivity`; `pytest tests/topic2_fu_b` still passes (128 passed).
- **Blast radius**: Descriptive-only fields in `verdict.json` (`r1_pairing`, `stall_sensitivity`). Cannot affect the governing verdict (`verdict.json["verdict"]`). Furthermore, our independent recomputation (`audit_fu_b.py`) verified that the shipped `r1_pairing` and `stall_sensitivity` implementations and outputs in `verdict.json` have `0.0` error.
- **Mitigation**: Optional future test addition asserting `r1_pairing` and `stall_sensitivity["I1_t"]` in `test_verdict.py`.

### [Low / Non-Blocking] Challenge 2: Secondary validation checks (`C15`, `C16`, `C21`, `C22`)
- **Assumption challenged**: That `test_verdict.py` and `test_records.py` independently exercise every individual clause of `fminus_inherited` and `records.validate`.
- **Attack scenario**: Mutants `C15`/`C16` alter `fminus_inherited` after the SHA-256 check on `r1/verdict.json`; `C21` removes `len(den) == DS.N_TEST` (while `len(num) == DS.N_TEST` and `test_nmse == sum(num)/sum(den)` remain checked); `C22` removes finiteness check on `val_nmse_curve` values (while keys `(8750, 17500, 26250, 35000)` remain checked).
- **Blast radius**: Negligible. `DS.R1_VERDICT_SHA256` cryptographically pins the exact `r1/verdict.json` bytes, and all 18 real `run.json` files were independently verified to have 16 positive finite `test_den` values and 4 finite `val_nmse_curve` values.
- **Mitigation**: None required for FU-B acceptance.

## Stress Test Results

- `W_V07..W_ledger` (12 worker critical & v1-survivor mutants) → expected: killed → actual: **12/12 killed** → **PASS**
- `C01..C14` (14 challenger governing-path mutants) → expected: killed or proven equivalent → actual: **13/14 killed, 1 (`C02`) proven defense-in-depth equivalent** → **PASS**
- `audit_fu_b.py` B300 provenance & 6,300-step LR schedule audit across all 18 runs → expected: 35,000 steps, batch 16, warmup 1,750, cosine decay to 0.0, all hashes match → actual: **`all_18_runs_valid: true`, `max_lr_abs_err: 0.0`** → **PASS**
- `audit_fu_b.py` independent raw-record verdict & bootstrap recomputation → expected: exact match to `verdict.json` (`stop`, rule 4) → actual: **`0.0` discrepancy across all metrics** → **PASS**

## Unchallenged Areas

- Full 35,000-step GPU re-training on B300 (out of scope for a challenger; verified via `train_log.jsonl`, `job_meta.json`, and pre-freeze smoke anchors).

---

## 5. Verification Method

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_B_r1_2/audit_fu_b.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_B_r1_2/adversarial_mutants.py
```

---

## 6. Structured JSON Summary

```json
{
  "verdict": "CONFIRMED",
  "full_report": "/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_B_r1_2/handoff.md",
  "blocking_issues": [],
  "nonblocking_issues": [
    "N1 (descriptive/secondary test coverage): In verification/challenger_FU_B_r1_2/adversarial_mutants.out.json, 8 challenger mutants on non-governing descriptive helpers or SHA-pinned/secondary clauses survive tests/topic2_fu_b (C15-C16 on fminus_inherited post-SHA JSON lookup, C17-C18 on stall_sensitivity interval calculation, C19-C20 on descriptive r1_pairing, C21-C22 on len(test_den)==16 when sum(test_den) matches and val_nmse_curve value finiteness). None affects the governing verdict path, and verification/challenger_FU_B_r1_2/audit_fu_b.out.json confirms 0.0 error on all shipped outputs.",
    "N2 (defense-in-depth equivalent mutant C02): In src/topic2_fu_b/verdict.py:81, removing stage1.get('errors') from decide() is equivalent in run_verdict() because run_verdict() (line 153, guarded by killed mutant C03) omits stage1['inference'] whenever res['errors'] is non-empty, causing decide() line 85 (if not inf.get('order_ok')) to still return no_verdict (rule 3)."
  ],
  "commands_run_and_results": [
    {
      "cmd": "LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt",
      "rc": 0,
      "summary": "67/67 protected files OK"
    },
    {
      "cmd": "grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c && grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c",
      "rc": 0,
      "summary": "31/31 card_sha256_v2 files OK; 50/50 output_sha256 files OK"
    },
    {
      "cmd": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_b tests/topic2_rgpool -q",
      "rc": 0,
      "summary": "244 passed (128 topic2_fu_b + 116 topic2_rgpool) in 146.27s"
    },
    {
      "cmd": "STRICT_E2E=1 CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q",
      "rc": 0,
      "summary": "86 passed in 46.99s"
    },
    {
      "cmd": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q",
      "rc": 0,
      "summary": "88 passed in 7.25s"
    },
    {
      "cmd": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_B_r1_2/audit_fu_b.py",
      "rc": 0,
      "summary": "All 18 B300 runs valid (35,000 steps, batch 16, warmup 1,750, cosine decay to 35,000 with max_lr_abs_err=0.0, code/perm/split hashes match, freeze precedes runs, gate precedes stage1, 30.72 GPU-h <= 33.0 cap, 0 C4/BIDS hits); independent verdict recomputation matches verdict.json (stop, rule 4) with 0.0 diff"
    },
    {
      "cmd": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_B_r1_2/adversarial_mutants.py",
      "rc": 0,
      "summary": "Verified 44/44 worker mutants killed; ran 34 challenger mutants in temporary copied tree (cleaned up): 12/12 worker critical/v1-survivors killed, 13/14 new governing-path mutants killed (1 equivalent C02), 8 secondary/descriptive test-coverage gaps logged as nonblocking"
    }
  ],
  "tested_artifact_sha256": {
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md": "994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae",
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_addendum_01.md": "4acafa5b5746d1771d85d8403727d58ff6ecc2d27475f5d5b8ec7534edd80817",
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md": "9c533a786d450eee1bd6f1d988669fd986bda7e53ffa13f9657678af61490617",
    "results/topic2/2026-11-02_fu_b/card_sha256.txt": "6d741c5a2fad8333b4301eff869077ab62bba4d85a8eb6aba95e55a3c31b75cc",
    "results/topic2/2026-11-02_fu_b/card_sha256_v2.txt": "bcd232ac9f1edb19906dc2c80c0a934dd7164901b579ade9631fec84288379c5",
    "results/topic2/2026-11-02_fu_b/output_sha256.txt": "30a566355a05f72df0c43637c07c5eb9d77f85ae2e0c2394ae641de033581b7b",
    "results/topic2/2026-11-02_fu_b/gate_4x.json": "8c1bc7e21c7531c9a2d44f364c36e14be7d603217ca88e9be997911dd8889af7",
    "results/topic2/2026-11-02_fu_b/verdict.json": "262b9c793af333af1658f95dfc96de3769c95d3fdddc300dd667813ee5f1e142",
    "results/topic2/2026-11-02_fu_b/slurm/jobs.json": "c4f919a54c0b24ab9642eafadc9459cfbe2ee6dddaf66f29981d56bfe1d04f02",
    "results/topic2/2026-11-02_fu_b/b300/view_check.json": "9476ddfe8436dbdb4bac2ccabd33e9e0f29e18036caf6ebb3c9acb52755e5676",
    "results/topic2/2026-11-02_fu_b/b300/c4_scan_b300.json": "d11ed2fe25980ab9d99689fa10913de3a42d208a240d29ef64aa1940895d713f",
    "verification/worker_FU_B_r1/mutation/mutants_v2.out.json": "72c2474b54bc43a9efe5182d4527f229d2874d045569d7f7a067eb257b218a0e",
    "verification/challenger_FU_B_r1_2/audit_fu_b.py": "40b66bd63e06c8bb98750d35f911e2dcfa985b4b1d6d510014b292081bdda13b",
    "verification/challenger_FU_B_r1_2/audit_fu_b.out.json": "b970b3968933e35e5155224270a06d60cab4b178e897d24bbc6f2f083b84c586",
    "verification/challenger_FU_B_r1_2/adversarial_mutants.py": "cd5ba7b5da68e14f4e24d884dbf8a9d148d9710f687d56f2b85eca7eee85d4b4",
    "verification/challenger_FU_B_r1_2/adversarial_mutants.out.json": "245a873fbe08176debd90ef788d49bda640e35657e2dda7b556db8d53a9cb940"
  },
  "uncovered_requirements": []
}
```
