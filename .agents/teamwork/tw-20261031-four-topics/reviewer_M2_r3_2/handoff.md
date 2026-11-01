# reviewer_M2_r3_2 — handoff (Hard), M2 Topic 3 iteration-3 gate, 2026-11-01T07:05Z

**Verdict: REQUEST_CHANGES.** There is one blocking class, and it is new: it is outside the r2b set. Iteration 3 closes every r1 and r2b blocking class, and no real verdict or reported number is wrong.

Evidence is in `/home/juke/git/00IITP-AI/verification/reviewer_M2_r3_2/`:
- `logs/`: production checks and independent recomputes;
- `runs/`: my mutation batches;
- `probes/`: real-input reachability.

## 1. Observation

O1. **Pins and receipts.**
- C1 gives 67 OK, rc 0, both before and after my work (`logs/c1_pre.log`, `logs/c1_post.log`).
- The Topic 3 receipts give output 42, addendum_02 1, addendum_03 3, addendum_04 2 and addendum_05 3 OK, all rc 0, before and after.
- addendum_05_sha256.txt (1e542da7…) pins addendum 05 (a4001f09…), test_verdict_rules_r3.py (58c64ccb…) and test_token_stats_wiring_r3.py (b091b0b8…).
- code_sha256_at_freeze.txt gives 26 of 27 OK. The exception is scripts/topic3_launch_connectome.py: it changed after the freeze, this is disclosed in addendum 01 item 2, and its current hash is pinned in output_sha256.txt:27. So iteration 3 changed no file in src/ or scripts/.

O2. **Production tests** (PYTHONDONTWRITEBYTECODE=1, -p no:cacheprovider, timeout 900, nice; `logs/prod_*.log`):
- tests/topic3_spectral: **121 passed, 0 skipped** (60 s);
- old suite with STRICT_E2E=1: **86 passed**;
- tests/topic1_lagmotif: **88 passed**.

The .pyc listing of src/, scripts/ and tests/ is identical before my work, after it, and at the end.

O3. **Hygiene.**
- audit_layout.py on the whole run metadata root: PASS, 234 files, findings [] (`logs/audit_layout.log`).
- The two r3 tests, addendum 05 and its receipt contain no `sub-` token. The hits in verification/worker_M2_r3 are the bare literal or synthetic `sub-SYN…` names.

O4. **Independent recomputes.** My own code imports nothing from src/ except the hash-checked loader and the positions.
- Family B primary statistics (mean log ratio, 95% bootstrap CI, two-sided sign-flip p, Holm) for all 4 checkpoints: max abs diff **0.0** against the pinned file.
- Family A, all within rel ≤ 1.4e-14 (`logs/indep_familyA*.log`):
  - D1 cov and corr intervals and the two D3 intervals: exact;
  - all 7 A2 m12/iid(12, D) ratios;
  - every E1 column: covPR, /(n−1), iid mean and q2.5, covPR/iid, null mean and q2.5, p_low/D2, jackknife SE.
- Addendum 05 numbers re-derived from the pinned files all match:
  - H1b gm−1: HCP −10.7%, L1e-4 −3.2%, primary +4.6%, L5e-5 +8.2%;
  - H1a: −12.8%, +2.3%, +3.9%, +5.0%;
  - CI half-widths 0.00203–0.01442;
  - fixture V01: raw 0.0326, Holm 0.0652, CI [0.0007, 0.0103];
  - skewed fixture: Holm 0.0321 / 0.0308, lower bound −0.00144;
  - 508 non-run leaves.
- Git (read-only): addendum 03's history is 4ce1917 (blob 725d5077…) then ef27b71, and 0db0336 does not touch it, as addendum 05 §5 states.

O5. **Worker evidence.**
- S88_v2.json (34da3012…), FULL_v2.json (e222e7f2…) and MUTANTS_SUMMARY.json (fa7017ac…) have the claimed hashes.
- 302 of 302 raw-log sha256 values match.
- Controls passed at start and end: 88/88 and 121/121, 0 skipped.
- The counts are 101/50 and 150/1. The spot-checked logs (U057, U091) are genuine pytest output.

O6. **My own mutation runs.** These are my own runner and my own patch text, in my own byte-copied tree (`build_tree.sh`, manifest 121 files OK; the manifest was re-verified after the batches, so the tree was not contaminated).
- **s88**, the shipped 88 tests (`runs/S88.json(.classified.json)`):
  - CONTROL: 88 passed;
  - all 10 r2b-class mutants **SURVIVE**: V01, P03, P01, P02, V05, A01, V28, V26, X02, X01.
- **full**, 121 tests (`runs/FULL.json(.classified.json)`):
  - CONTROL: 121 passed;
  - all 10 r2b-class mutants **KILLED**, each with ≥ 1 r3 test failing;
  - the r1 mutants N05, N06, N08, N09, N10 and N11 **KILLED**;
  - my new verdict-path mutants **KILLED**: D3 checking only the first pair (`test_d3_requires_both_cross_model_pairs`), A2 pair 1 orientation, the A1 corr interval computed with covPR (`test_d1_cov_only_is_attributed_to_gain`), and the bootstrap drawn without replacement;
  - **4 new mutants SURVIVE**: B_A2_iid_at_n25, B_E1_iid_wrong_n, B_E1_null_q05 and B_E1_pr_over_n.
- **v2-runner confirmation** (`runs/V2CHECK.json`, JUnit-based): V01 KILLED by the same 4 r3 tests; B_A2_iid_at_n25 SURVIVED.

O7. **Survivors on the card's real inputs.** `probe_familyA_mutant.py` runs `subject_level` at the card PARAMS on the pinned matrices in a separate copied tree. The CONTROL run reproduces all 300 pinned Family A leaves (n_diff 0).

| Survivor | Card definition broken | Pinned leaves changed | Printed in the result report? |
|---|---|---|---|
| B_A2_iid_at_n25 | §4 A2: "divided by the iid reference at (12, D)"; the mutant uses (25, D) | 7 (e.g. BrainJEPA 0.598 → 0.279) | yes, A2 table column "m = 12 mean covPR / iid(12, D)" (3 rows) |
| B_E1_iid_wrong_n | §4 E1: "iid-Gaussian reference at the same (n, D)"; the mutant uses (n−1, D) | 56 (iid mean, q2.5, q97.5, covPR/iid; about 4%) | yes, E1 table columns "iid reference mean" and "covPR / iid" (7 rows) |
| B_E1_null_q05 | the column labelled q2.5 computed as q5 | 14 | yes, E1 table column "column-permutation null q2.5" |
| B_E1_pr_over_n | §4 E1: "covPR/(n−1)"; the mutant uses covPR/n | 14 | no, JSON only |

D1 and D3 are unchanged under all four mutants. Family A's script runtime is 26.2 s (`run.runtime_s`).

Printed-precision check (`logs/printed_precision_check.log`): every report cell that a survivor touches changes at the report's printed precision.
- B_A2_iid_at_n25: 3 of 3 A2 cells (BrainLM 0.406 → 0.189, BrainJEPA 0.598 → 0.279, NeuroSTORM 0.734 → 0.351).
- B_E1_iid_wrong_n: 14 of 14 E1 cells (e.g. L2 iid mean 54.00 → 53.07).
- B_E1_null_q05: 7 of 7 E1 cells (e.g. L0 44.77 → 44.87).
- B_E1_pr_over_n: no printed cell (JSON only), so nonblocking on its own.

O8. **Other findings.**
- `tests/topic3_spectral/__pycache__/` holds 3 .pyc files from 2026-10-31T23:29:58Z. They predate iteration 3 but are not mentioned in addendum 05, which lists only the src/ ones.
- The worker's real-data timing probe (handoff deviation 1) is not disclosed in addendum 05.
- Since root checkpoint commit a910c53 (06:31:28Z), HEAD holds the final addendum 05 (a4001f09). The worker's note that addendum 05 is "modified vs HEAD" is therefore stale. This was not a worker git write.

## 2. Logic Chain

1. **r2b classes 1–5 are closed.** O6 shows each named mutant surviving the shipped 88 tests and killed by the 121, with r3 tests among the failures. This is an independent reproduction, with my own patch text and runner, of the worker's S88_v2/FULL_v2 result (O5).
2. **r1 class 1** (verdict logic unguarded: N05, N06, N08, N09, N10, N11) is killed (O6).
3. **r1 class 2** (Family B estimand described wrongly) is restated in addendum 03 §1: the ceiling is 7, and the measure is the spread of 8 near-static spatial cells. Addendum 05 §5 refines it: the H4 L0 ceiling is 159, and the R2 statement holds for H1a only. The numbers check (O4).
4. **No verdict and no reported number is wrong today.** My independent recomputes match the pinned Families A and B exactly (O4), and the receipts verify (O1).
5. **The Family A descriptive columns are not guarded.** Three surviving mutants each break an explicit card or report definition, are reachable on the card's own real inputs, and change numbers printed in the result report (O7). By the dispatch's materiality rule ("can change a verdict or a reported number") they meet the blocking bar. The r2b gate set the same precedent: reviewer_1's B3/A01 blocked although D3 was unchanged, because 78 A2 numbers moved. The worker disclosed the gap ("Family A numbers other than the A2 row identity are not re-derived by the r3 tests"), but disclosure does not close it.
6. **The fix is small and fits PI decision 1** (additive tests, no src/ or scripts/ change, no rerun to produce a result). Add a Family A analog of the class-5 wiring test: run the unmodified scripts/topic3_subject_level.py in tmp_path with OUT redirected (≈ 26 s), and compare every non-run leaf with the pinned family_A_subject_level.json (receipt-checked). My CONTROL probe shows that this comparison is exact and deterministic (300 of 300 leaves), and that each of the 4 survivors changes ≥ 7 leaves. One test therefore kills all four.
7. **U127 (A15)** changes `"L3 lower" if sign < 0` to `sign <= 0`. It differs only when mean_log_ratio is exactly 0. In that case the shipped sign-flip test gives p = 1, so the primary is not significant, and a zoo checkpoint with mean 0 also has p = 1, so the agreement count is unchanged. The verdict is "killed" either way. Only the `direction` label of a zero-mean primary changes, and the card defines none for that case. I accept it as equivalent.

## 3. Caveats

- My new mutant set is 8 hand-designed mutants, not an exhaustive search. Areas not stressed beyond the union: token_job.py (the connectome path) and estimators.py edge cases.
- **My runner v1 had a JUnit path bug** (my own deviation). The path was relative while the pytest cwd was the job tree, so the XML was lost and rc = 1 jobs were labelled INVALID. Those jobs were reclassified from the text logs (rc + `-rf` FAILED lines + the pytest summary) by `classify_from_logs.py`. v2 (absolute paths) confirms both directions (O6). Disclosure: `runs/RUNNER_V1_JUNIT_BUG_README.txt`; the v1 bytes are in `runs/run_mutants_v1_snapshot.py`.
- **Real-input probes and recomputes.** They were run in my copied trees or in memory and wrote nothing outside `verification/reviewer_M2_r3_2/`. The dispatch allows verifiers to do this (< 15 min CPU).
- **My DISPATCH.md** summarizes the embedded worker JSON in brackets instead of copying it verbatim.
- **Timestamps.** The progress.md times for three early lines are approximate; this is noted there.
- **Host load** reached about 40 on 20 cores during the batches, with no OOM or timeout. 0 INVALID remain after reclassification.

## 4. Conclusion

REQUEST_CHANGES on one Major blocking class (no integrity violation): **Family A E1/A2 descriptive columns printed in the result report are not guarded by any test.**
- The surviving mutants are B_A2_iid_at_n25, B_E1_iid_wrong_n and B_E1_null_q05, plus the JSON-only B_E1_pr_over_n.
- **Required (additive):** a Family A wiring test that reruns the unmodified topic3_subject_level.py in tmp_path and compares every non-run leaf with the pinned family_A_subject_level.json.
- **Then:** record its sha256 in a dated addendum receipt, and show that the 4 mutants are killed in copied trees.

Everything else meets C1–C8 and T3.1–T3.4 with evidence, and all r1 and r2b blocking issues are closed.

Nonblocking items:
- addendum 05 omits the tests/topic3_spectral/__pycache__ files and the worker's timing probe;
- `test_primary_raw_p_below_alpha…` pairs Holm 0.06 with an "other" record whose raw p is 0.0001. This is internally inconsistent but immaterial, because the rule reads the per-key fields only;
- the Family B wiring tests skip silently without VRABES;
- the shipped label "killed (primary CI includes 0)" is also applied when Holm p ≥ 0.05 and the CI excludes 0. src/ is frozen, and this is already recorded in addendum 05 §5;
- the test_token_job_driver Pool deadlock hazard persists;
- H2 is untested, as the card pre-specified.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt     # 67 OK
for r in output addendum_02 addendum_03 addendum_04 addendum_05; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD OMP_NUM_THREADS=2 timeout 900 nice -n 10 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic3_spectral   # 121 passed
V=verification/reviewer_M2_r3_2; cd $V && ./build_tree.sh $PWD/tree_base && ./build_tree.sh $PWD/tree_probe
/home/juke/superclaude-env/bin/python3 -B -I run_mutants.py $PWD/tree_base runs/RECHECK.json full 2 B_A2_iid_at_n25,B_E1_iid_wrong_n,B_E1_null_q05,A_V01_primary_raw_p
#   expect: 3 B_* SURVIVED (until the Family A wiring test exists), A_V01 KILLED
/home/juke/superclaude-env/bin/python3 -B -I probe_familyA_mutant.py B_A2_iid_at_n25 probes/recheck.json   # n_diff 7
```

Invalidation:
- the reviewed files' hashes differ from 58c64ccb…, b091b0b8…, a4001f09… or 1e542da7…;
- a new Family A wiring test exists and kills the 4 survivors, which resolves the blocking class;
- the B_* survivors are shown not to change printed report values. They do: see O7.
