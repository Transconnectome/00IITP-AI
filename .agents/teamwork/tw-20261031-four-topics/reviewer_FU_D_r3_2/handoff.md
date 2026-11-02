# Handoff — `reviewer_FU_D_r3_2` (Milestone `FU_D_r3`, Reviewer 2 of 2)

- **Run**: `tw-20261031-four-topics` (General route, Workflow C)
- **Milestone**: `FU_D_r3` (`Topic 2 follow-up D: E192 scale (d2-2-18-2), 140k samples, arms E/C/S, 5 seeds (§7 ≈20 GPU-h at 1.36 h/run; cap 25)`)
- **Role**: `reviewer_FU_D_r3_2` (Reviewer 2 of 2)
- **Date**: `2026-11-02T05:01:00Z`
- **Verdict**: **`APPROVE`** (`0` blocking issues, `2` nonblocking issues, `0` uncovered requirements)

---

## 1. Observation

I independently inspected and verified the Milestone `FU_D` Iteration 3 deliverables produced by `worker_FU_D_r3` against `ACCEPTANCE.md` criteria `C1`–`C8`, milestone criteria `F1`–`F3`, the iteration-2 gate failures `B1` and `B2` from `challenger_FU_D_r2_2/handoff.md`, and all findings from `reviewer_FU_D_r2_1`, `reviewer_FU_D_r2_2`, `challenger_FU_D_r2_1`, `challenger_FU_D_r2_2`, `auditor_FU_D_r2_1`, and `explorer_FU_D_r3_1`..`3`:

1. **Frozen & Additive Artifact Integrity (`C1`, `F1`, `F2`)**:
   - `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: `67/67` entries `OK` (`rc=0`, `BAD=0`).
   - All five Topic 2 FU-D SHA256 receipts under `results/topic2/2026-11-02_fu_d/` pass `sha256sum -c` with `rc=0`:
     - `card_sha256.txt`: `1/1 OK` (`2026-11-02_topic2_fu_d_card.md` = `1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b`).
     - `code_sha256_at_freeze.txt`: `29/29 OK` (`src/topic2_fu_d/*.py`, `scripts/topic2fu_d_*.py`, `tests/topic2_fu_d/test_*.py` at freeze).
     - `output_sha256.txt`: `34/34 OK` (`verdict.json` = `f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`).
     - `addendum_01_sha256.txt`: `23/23 OK` (`2026-11-02_topic2_fu_d_addendum_01.md` = `d57eb4f69a28c7d14d0c41e1fb316e750d3556d331d6b80e657c9c0bc2a8aa85`).
     - `addendum_02_sha256.txt`: `102/102 OK` (`2026-11-02_topic2_fu_d_addendum_02.md` = `cada5c098a0dffc5f5bfbda2ac8bea0f30aac58558a7cd00ce271dc76170d023`, `test_fud_r3_guards.py` = `3fd9453e8d77438b4ef1dc36bf94a4f96a694c51e4290b660a726dd2d4c2b548`, `test_fud_r3_oracle.py` = `7db37e9c79b5da177da05c946e266d5e0bb7309e40f2c07234fd852a486ef015`, `test_fud_r3_full_output.py` = `251a1c3f1d8290988732d6f1234d922f2c8b0239650b9ca0fb6fc1812eb09ec7`).
   - All three Topic 2 r1 receipts (`code_sha256_at_freeze.txt` `33/33 OK`, `output_sha256_r2.txt` `156/156 OK`, `addendum_06_sha256.txt` `31/31 OK`) pass `sha256sum -c` with `rc=0`.

2. **Closure of Gate Failure `B1` (`src/topic2_fu_d/verdict.py:217-225` & `scripts/topic2fu_d_verdict.py:114-122` Step 7 Stall-Sensitivity)**:
   - `tests/topic2_fu_d/test_fud_r3_guards.py` (lines 75–319) verifies Step 7 at class level across all `28` reachable `(stalled_seeds, cat_all, cat_wo)` cells (14 for 1 stalled seed with `k=4`, 14 for 2 stalled seeds with `k=3`) against an independent `scipy.stats.t.ppf(0.975, df)` oracle at both `verdict._stage1_category` and `verdict.decide`, an exhaustive 4x4 = 16-pair decision table via `monkeypatch`, a direct `C12` (`stop -> inconclusive`) regression witness (`test_step7_c12_stop_to_inconclusive_direct_witness`), per-arm `E`/`C`/`S` and two-seed script stall tests (`test_script_detects_a_stall_in_every_arm_and_flips_stop_to_inconclusive`, `test_script_drops_every_seed_that_holds_a_stalled_run`), and an exact verification of algebraic proof `P1` (`test_proof_p1_stop_to_keep_or_modify_is_algebraically_impossible_for_n5_k3_or_k4`).
   - `tests/topic2_fu_d/test_fud_r3_oracle.py` runs `3,000` seeded scenarios against an independent card-§8 reference oracle covering all decision categories and stall transitions.
   - In `verification/worker_FU_D_r3/mutation/union_r3.out.json`, `cha2_2:C12` (`= cha2_1:CV09`), `E7a`–`E7i`, `CP01`, `CP02`, `W1`, `N01`–`N20`, and `T01`–`T11` are all `KILLED` in Leg A, and our independent `spot_check_mutants.py` also killed two newly designed pair-skipping mutants (`REV3_2_M1_pair_stop_inc`, `REV3_2_M2_pair_keep_stop`) and boundary mutant (`REV3_2_M3_keep_idx_le2`).

3. **Closure of Gate Failure `B2` & Related Frozen-Code Departures (`addendum_02.md` §3 + `errata_probe.out.json`)**:
   - Because `src/topic2_fu_d/design.py`, `src/topic2_fu_d/records.py`, `src/topic2_fu_d/verdict.py`, and `scripts/topic2fu_d_verdict.py` are frozen under `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`, post-result code modification without a new pre-registration card is forbidden by `C6`.
   - `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md` §3 records `E5` (alias run directories via `int(...)` and `$`: zero-padded `fplus_gate_E_s00`, Arabic-Indic `\u0660`, full-width `\uff10`, and trailing `\n`, on both gate and Stage-1 paths under `strict=True`, together with the canonical ASCII reading rule `run_name(*parse_dir(name)) == name`), `E2'` (widened from `E2` to non-finite/negative/zero `val_err`/`baseline_err`), `E6` (`seed_plan.json` `seeds` list unchecked against `n_seeds`), `E7` (F-minus records flagged in `notes` rather than stopping verdict; lone completed F-minus ignored; skipped on failed-gate path), `E8` (sidecar `fud_code_sha256` unchecked against receipt), `E9` (minor items: `seed=False`/`0.0`, symlinks, plain `hcp_*` file), `W4` (capacity floor short-circuits before writing `stall_sensitivity`), and `W5` (cost-guard missing Stage-1 reason wording), plus an explicit reuse condition for future cards.
   - `test_fud_r3_guards.py` lines 632–695 enforce shipped-data invariants proving the shipped dataset (`3` canonical gate runs, `0` Stage-1/F-minus runs, `0` non-canonical aliases, `0` symlinks, exact `seeds == [0, 1, 2, 3, 4]`, positive finite errors) lies strictly outside every departure.

4. **Independent Verification of `union_r3.out.json`, `errata_probe.out.json`, and Test Suites**:
   - Re-ran all three pytest suites sequentially (1 process at a time):
     - `tests/topic2_fu_d`: `389 passed, 2 warnings in 80.33s` (`rc=0`).
     - `tests/topic2_rgpool tests/topic1_lagmotif`: `204 passed, 24 warnings in 138.30s` (`rc=0`).
     - `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` (`STRICT_E2E=1`): `86 passed, 7 warnings in 32.71s` (`rc=0`).
   - Re-ran `verification/worker_FU_D_r3/probes/errata_probe.py`: output matches `errata_probe.out.json` byte-for-byte, and every probe assertion matches `addendum_02.md` §3.
   - Audited `union_r3.out.json` via `verification/reviewer_FU_D_r3_2/audit_r3_claims.py` and `verify_164_survivors.py`:
     - `1,675` distinct single-site mutants (`1,813` total entries across 11 sources) = `1,511` killed + `164` survived, `0` invalid.
     - All `515` distinct mutants that alter shipped `verdict.json` (`shipped.changed == True`) are `KILLED`; `0` surviving mutants alter shipped output.
     - All `135` non-equivalent target mutants from r2 verifiers and r3 explorers are `KILLED` (`34` killed exclusively by the new r3 test files).
     - Programmatically inspected the exact `old -> new` edits of all `164` surviving distinct mutants (`verify_164_survivors.py`) and verified they partition exactly into the `10` equivalence / decision-invariance classes in `addendum_02.md` §5 (`61 + 41 + 9 + 9 + 6 + 3 + 6 + 14 + 7 + 8 = 164`).

---

## 2. Logic Chain

1. **Requirement Traceability (`C1`–`C8`, `F1`–`F3`, `B1`, `B2`)**:
   - **`C1` (Topic 1 freeze)**: `PROTECTED_HASHES.txt` has `67/67 OK` and `tests/topic1_lagmotif` passes (`rc=0`).
   - **`C2` (Real HCP metrics)**: All 3 F+ gate runs in `results/topic2/2026-11-02_fu_d/runs/` use real 42-participant HCP test records (`n_test_subjects=42`, `post_checks_ok=true`, `status="completed"`).
   - **`C3` (Hierarchical bootstrap)**: Tested and enforced for Stage-1 (`B=10,000`, `seed=0`, `num/den` ratio of per-participant seed means) in `test_fud_r3_guards.py::test_secondary_uses_the_card_bootstrap_b10000_seed0_num_over_den_and_per_subject_seed_means`; not invoked on the shipped F+ gate-stopped run (`stage1_executed=false`).
   - **`C4` (Zero 6-digit HCP IDs, BIDS prefixes, or 16-hex content hashes)**: Verified by `scripts/topic2fu_d_c4scan.py` (`84` files, `0` hits), `verification/worker_FU_D_r3/c4_scan_r3.py` (`36` files, `0` hits), and our own scan over `reviewer_FU_D_r3_2` metadata and verification folders (`0` hits).
   - **`C5` (Compute discipline & GPU ledger)**: `3` F+ gate runs at `E192` consumed `1.244971` GPU-h (`<= 25` GPU-h cap); Stage 1 (`15` runs) and F-minus (`3` runs) were not launched after F+ gate failed (`0.00` GPU-h saved ~`24.5` GPU-h); logged in `results/gpu_ledger_2026-10-31.md`.
   - **`C6` (Pre-registration & honesty)**: Card frozen before runs (`card_sha256.txt`); code frozen before runs (`code_sha256_at_freeze.txt`); post-freeze disclosures documented in `addendum_01.md` and `addendum_02.md` without modifying frozen files.
   - **`C7` (Test & E2E verification)**: All `679` tests across the 3 suites pass (`rc=0`), plus `1,511/1,675` distinct mutants killed (`100%` of the `515` shipped-output-changing mutants and `100%` of the `135` non-equivalent verifier/explorer target mutants).
   - **`C8` (Layout compliance)**: `audit_layout.py` returns `status=PASS` with `findings=[]`.
   - **`F1`–`F3` (Milestone FU_D criteria)**: Pre-registered card (`F1`), real F+ gate execution & honest early stop (`F2`), and byte-identical `verdict.json` (`F3`, exact `Fraction` recomputation: `E=0.6558494816918741`, `C=0.653467876277415`, `S=0.6577736746995909`, `gain_C_vs_E=+0.3631% < 1.0%`, `gain_C_vs_S=+0.6546% < 1.0%`, `category="stop"`).

2. **Why `B1` and `B2` Are Conclusively Closed**:
   - `B1` occurred because r2 tested Step 7 stall-sensitivity with only 3 category transitions, leaving `stop -> inconclusive` (`C12`) and script-level arm `E`/`C` stalls (`CP01`) untested. In r3, `test_fud_r3_guards.py` and `test_fud_r3_oracle.py` test all `28` reachable `(stalled_seeds, cat_all, cat_wo)` cells against an independent `scipy.stats.t.ppf` oracle, test all `16` `(cat_all, cat_wo)` pairs via `monkeypatch`, test per-arm `E`/`C`/`S` and two-seed script stalls, and algebraically prove (`P1`) why `stop -> keep` and `stop -> modify` cannot occur for `n=5, k in {3, 4}` (`min(t_{k-1}) > max(t_4)` when `t_4 <= 1.0` requires `u_k >= 0.555289 > 1/5` for `k=4` and `u_k >= 0.680087 > 2/5` for `k=3`).
   - `B2` occurred because `addendum_01.md` §5 disclosed non-negative ASCII `fplus_gate_<arm>_s<k>` with `k >= 1` while omitting zero-padded (`s00`), Unicode digit (`\u0660`, `\uff10`), trailing-newline (`\n`), and Stage-1 alias directories. In r3, `addendum_02.md` §3 accurately documents `E5` (along with `E2'`, `E6`–`E9`, `W4`, `W5`) verified by `errata_probe.py`, specifies the exact canonical ASCII round-trip guard `run_name(*parse_dir(name)) == name` for future cards, and enforces shipped-data invariants in `test_fud_r3_guards.py`.

---

## 3. Caveats

1. **Nonblocking Issue 1 (Minor documentation wording on `CTRL` Leg B in `addendum_02.md` §5 line 190 and `worker_FU_D_r3/handoff.md` line 14)**:
   - `addendum_02.md` §5 line 190 states for `CTRL`: `"(383 passed, 1 deselected in Leg A; 189 passed, 1 deselected in Leg B; shipped_changed = False)"`.
   - In `verification/worker_FU_D_r3/mutation/run_union_r3.py` line 134, Leg B (`pytest(w, "B")`) is executed conditionally (`if rec["A"]["status"] == "KILLED" and m.get("listed"):`), so the `"control"` entry in `union_r3.out.json` records `"A"` (`"383 passed, 1 deselected in 23.09s"`) and `"shipped"` (`changed: false`), without a `"B"` key on `"control"` itself; the `"189 passed, 1 deselected"` Leg B count appears on all `34` `killed_only_by_r3_files` entries that survived Leg B. This is purely descriptive and has zero impact on mutation counts or verdicts.

2. **Nonblocking Issue 2 (8 Class-10 cosmetic/diagnostic survivors in `union_r3.out.json`)**:
   - As transparently disclosed in `addendum_02.md` §5 Class 10 (`8` distinct mutants: `exp3_3:W152`, `W193`, `W211`, `W235`/`r3:index0163`, `r3:index0164`, `W664`, `W621`, `W702`/`r3:kwconst0464`), tests assert `pytest.raises(FUDRecordError)` without regex-matching internal exception wording in `design.py`/`records.py`, and parse `topic2fu_d_verdict.py` stdout via `json.loads` (`indent=1` vs `None`/`2`). None of these 8 mutants can affect any decision category, reason string, or `verdict.json` content.

---

## 4. Conclusion

- **Gate Verdict**: **`APPROVE`**
- All blocking issues from Iteration 2 (`B1` and `B2`) and all non-equivalent findings from the five r2 verifiers and three r3 explorers are closed with executable evidence, algebraic proof, and receipt-pinned documentation.

### Review Summary
```markdown
## Review Summary
- Verdict: APPROVE
- Blocking issues: 0
- Non-blocking observations: 2
- Files reviewed: 28 (frozen FU_D source/scripts/tests/docs/receipts + r3 additive tests, addendum_02, mutation union, errata probe)
- Checklists applied: ACCEPTANCE C1-C8, Milestone F1-F3, B1/B2 closure, r2 verifier & r3 explorer closure
```

### Challenge Summary
```markdown
## Challenge Summary
- Risk level: LOW
- Must-fix issues: 0
- Hypotheses tested: 3 (H1: 135 target mutants + 5 new adversarial mutants REV3_2_M1..M5; H2: exhaustive source audit of all 164 surviving distinct mutants; H3: 1-to-1 verification of errata_probe.py vs addendum_02.md §3)
- Strongest counter-evidence found: None blocking; all 515 shipped-changing mutants and all 135 non-equivalent target mutants are KILLED, and all 164 survivors are verified equivalent, unreachable, documented frozen-code departures (E2'/E5-E9), or cosmetic Class-10 strings.
```

---

## 5. Verification Method

All independent verification artifacts and logs are saved under `/home/juke/git/00IITP-AI/verification/reviewer_FU_D_r3_2/`:

1. **Protected Hashes & Receipts**:
   - `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` -> `verification/reviewer_FU_D_r3_2/c1_check.out` (`67/67 OK`, `rc=0`).
   - `LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_d/{card_sha256,code_sha256_at_freeze,output_sha256,addendum_01_sha256,addendum_02_sha256}.txt` -> `verification/reviewer_FU_D_r3_2/receipt_*.txt` (`189/189 OK`, `rc=0`).
   - `LC_ALL=C sha256sum -c results/topic2/2026-11-01/{code_sha256_at_freeze,output_sha256_r2,addendum_06_sha256}.txt` -> `verification/reviewer_FU_D_r3_2/r1_receipt_*.txt` (`220/220 OK`, `rc=0`).
2. **Pytest Regression Suites (Sequential, 1 Process at a Time)**:
   - `tests/topic2_fu_d` -> `verification/reviewer_FU_D_r3_2/pytest_fud.out` (`389 passed, 2 warnings in 80.33s`, `rc=0`).
   - `tests/topic2_rgpool tests/topic1_lagmotif` -> `verification/reviewer_FU_D_r3_2/pytest_rgpool_topic1.out` (`204 passed, 24 warnings in 138.30s`, `rc=0`).
   - `STRICT_E2E=1` `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` -> `verification/reviewer_FU_D_r3_2/pytest_old86.out` (`86 passed, 7 warnings in 32.71s`, `rc=0`).
3. **Independent Audit & Mutation Probes**:
   - `verification/reviewer_FU_D_r3_2/audit_r3_claims.py` -> `audit_r3_claims.out.json` (`rc=0`).
   - `verification/reviewer_FU_D_r3_2/verify_164_survivors.py` -> `verify_164_survivors.out.json` (`rc=0`).
   - `verification/reviewer_FU_D_r3_2/spot_check_mutants.py` -> `spot_check_mutants.out.json` (`rc=0`, `CTRL` survived, `16/16` mutants `KILLED`).
4. **C4 & Layout Audits**:
   - `scripts/topic2fu_d_c4scan.py` -> `verification/reviewer_FU_D_r3_2/c4scan_frozen.json` (`84` files, `0` hits).
   - `verification/worker_FU_D_r3/c4_scan_r3.py` -> `verification/reviewer_FU_D_r3_2/c4scan_r3.json` (`36` files, `0` hits).
   - `audit_layout.py` -> `verification/reviewer_FU_D_r3_2/audit_layout.json` (`status=PASS`, `findings=[]`).
