# auditor_M2_r4_1 — handoff (Hard), M2 Topic 3 iteration 4 fixed-scope gate (PI decision 6), 2026-11-01

## Forensic Audit Report

**Work Product**: worker_M2_r4 deliverables — `tests/topic3_spectral/test_regression_r4.py` (ecceb134…ed2e0fbed),
`tests/topic3_spectral/test_token_level_r4.py` (ab99b2b1…e4a68d1),
`docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_06.md` (19b6218f…12756),
`results/topic3/2026-10-31/addendum_06_sha256.txt` (6191bd5a…d05d510); evidence `verification/worker_M2_r4/`.
**Profile**: General Project. Integrity mode: Development (ORIGINAL_REQUEST.md has no "from scratch"/"must not delegate" constraint).
**Verdict**: CLEAN

### Phase Results
- Deliverable hashes = worker claims and = addendum_06 receipt: PASS
- Hardcoded output detection: PASS — expectations come from the receipt-checked pinned JSON (class a real), independent numpy re-derivation (class a synthetic, class b), Holm-consistent hand-built records checked against `resampling.holm` plus computed preconditions (class c), stub truth table plus computed witness with asserted preconditions (class d). Numbers quoted in the addendum (D1 witness, p values, CI bounds) are not asserted as literals in the tests.
- Facade detection: PASS — no src/ or scripts/ change (code_sha256_at_freeze 26 OK; the one mismatch, `scripts/topic3_launch_connectome.py`, is pre-existing, disclosed in addendum 01, pinned in output_sha256.txt).
- Pre-populated / fabricated artefacts: PASS — 384 worker attempt records cross-checked against raw log and JUnit sha256 and JUnit failing lists: 0 problems; worker manifest 657 files OK; my own independent runs reproduce every REQUIRED status and every per-test kill pattern the addendum §4.2 table reports; all addendum numbers I recomputed match exactly.
- Build and run (my own tree + production): PASS — see Observation O2–O4.
- Writes to production / pinned paths: PASS — C1 67 OK and all 6 receipts OK before and after; no production file newer than my DISPATCH.md; topic3 mtimes unchanged; pyc listing unchanged.
- Participant IDs: PASS — 0 BIDS-prefix hits in the 4 deliverables; only synthetic `SYN…` names in byte copies of the shipped driver test; committed addendum_06 drafts (v2, v3) contain no prefix.
- Git writes: PASS — r4 `.py` tests never committed; addendum_06 committed only by the root checkpoint loop.

## 1. Observation

O1. Hashes (sha256sum, 12:27Z): the four deliverables match the worker's frozen_artifacts_sha256 and `addendum_06_sha256.txt` (3 lines). Test files mtime 2026-11-01 17:13:57 KST = 08:13:57Z (worker's freeze time).

O2. My own tree and mutants (independent tooling, `verification/auditor_M2_r4_1/bin/`):
- `build_tree.py` copied 122 production files (src/**/*.py, tests/__init__.py, tests/topic3_spectral/*.py, scripts/topic3_*.py, docs/03_empirical_analysis/topic3/*, results/topic3/**) into `tree_base`, byte-checked, manifest `tree_base.manifest_sha256.txt` (36333ea3…). Import probe: `helpers.ROOT`, `analysis.__file__`, `token_job.__file__` resolve inside my tree.
- `my_specs.py` (AST + literal_eval; no harness imported) extracted the 26 REQUIRED ids from the four r3 harness files (sha256 RV31 17a30dca…, RV32 ca6d7381…, CH31 d5f73f38…, CH32 0be048a3…) → 21 unique patched programs (merged when byte-identical: B_A2_iid_at_n25 = CR3_A01; B_E1_null_q05 = CR3_A05 = FA03; B_E1_pr_over_n = FA01; CR3_A02 = FA08).
- `run_jobs.py`: full `tests/topic3_spectral` (no -x), `timeout 900 nice -n 10`, PYTHONDONTWRITEBYTECODE=1, OMP 2, PYTHONPATH = job tree only, ≤2 at once, memory gate, own process group. Record `runs/MUTANTS_r4_audit.json` (f95af99d…), 12:32:27Z–12:49:21Z.
- J00_CONTROL: SURVIVED, 138 passed, 0 skipped.
- All 21 programs KILLED, each: tests 138, skipped 0, rc 1, failing_other = [] (all 121 pre-existing tests pass), 1 attempt, 0 INVALID, 0 leftover processes:
  - (a) B_A2_iid_at_n25/CR3_A01, B_E1_iid_wrong_n, B_E1_null_q05/CR3_A05/FA03, B_E1_pr_over_n/FA01, CR3_A02/FA08, CR3_A07, CR3_A08, FA02, FA04, FA05, FA06, FA07, FA09, FA10 → killed by BOTH `test_subject_level_script_reproduces_every_pinned_family_a_value` (real data) and `test_subject_level_matches_card_definitions_on_synthetic_matrices`. FA11 → killed by the synthetic test only (real-data test passes: FA11 changes no real-data leaf, as claimed).
  - (b) CR3_T01, CR3_T02, TJ03 → killed by `test_subject_summary_matches_card_definitions_for_every_variant` and `test_packed_spectra_feed_the_card_contrasts`.
  - (c) N01 → 8 failures: all 6 hand-built cases and both computed B = 9999 cases.
  - (d) VA01, VA02 → the corr-only stub case `[-0.3-0.4-drop not robust]` and `test_d1_corr_only_case_computed_by_the_shipped_procedure`.
  This matches addendum 06 §4.2 row for row.

O3. Numeric spot check without pytest (`bin/probe_numbers.py` → `logs/probe_numbers.out.json`), shipped code in my tree:
- D1 witness (m 28, S 2000): cov [−2.94206, −1.66048], corr [+13.8769, +15.4404], verdict "drop not robust" — identical to challenger_M2_r3_2's card-reps output (`verification/challenger_M2_r3_2/probes/witness_shipped.out.json`).
- Class (c), seed 2000, t 2.15, B 9999: H1a p_raw = p_holm = 0.0380, CI [0.000622, 0.01074]; H1b p_raw = p_holm = 0.0347, CI [0.000622, 0.01085]; other primary 1e-4; Bonferroni 0.076 / 0.069; zoo Holm p 2e-4 ×3; shipped verdict "holds".
- Hand-built Holm: holm([p, 1e-4]) = [p, 2e-4] for p = 0.026/0.04/0.049 (Bonferroni 0.052/0.08/0.098).
- Class (b) fixture margins: |log covPR/corrPR| 0.24–0.98 (L2, L3); L3 floor effect 3.18–3.26%; dropped count L3 = 1, others 0. Class (a) synthetic L0 floor effect 1.84%. Pinned Family A `results` has 300 leaves.

O4. Production and skip path:
- Skip probe (copied tree with `io_contract.VRABES_RA` → nonexistent path; r4 files only): `16 passed, 1 skipped`, SKIPPED reason "a pinned VRABES pooled input is absent" (`probes/skip_probe.log`).
- Production `tests/topic3_spectral`: 138 passed, 0 skipped, 0 failures (84.2 s; `logs/prod_topic3.{log,junit.xml}`).
- Old suite (STRICT_E2E=1, test_empirical_four_topics + test_pilot_connectome + e2e): 86 passed, 7 warnings. topic1_lagmotif: 88 passed.
- C1 pre and post: 67 OK, rc 0. Receipts pre and post: output 42, ad02 1, ad03 3, ad04 2, ad05 3, ad06 3 OK, rc 0.
- pyc listing before/after: identical (53 files), and identical to `verification/worker_M2_r4/logs/pyc_list_start.txt`. Newest pyc anywhere in src/scripts/tests: 2026-11-01 09:39:14 KST (iteration 2). No production file under src/, scripts/, tests/, docs/03_empirical_analysis/, results/ is newer than my DISPATCH.md (21:25:52 KST); topic3 mtimes unchanged.

O5. Git (read-only, GIT_OPTIONAL_LOCKS=0, no --stat/--name-only, no git status): `git log` for the two r4 test files → no commits. addendum_06 appears only in root checkpoint commits "docs(iitp): checkpoint four-topics teamwork documents" (a550237/07cda0c/e459552 hold v2 46527e6a…, 5b36496 holds v3 19b6218f… = HEAD = working copy). The receipt is uncommitted. v1 (literal BIDS prefix with synthetic names) was never committed. All commits since 07:30Z are the 15-minute checkpoint loop.

O6. Worker evidence integrity: `verification/worker_M2_r4/EVIDENCE_MANIFEST_final_sha256.txt` 657 files OK; 384 attempt records in EVID_named_r4{,_v2b,_v3} and EVID_union_r4_{v3ff,v3c}: every log/JUnit sha256 matches, every recorded failing list equals the JUnit file, no KILLED without a failure, no SURVIVED/CONTROL with a failure. npz copies in the worker's trees are byte copies of the pinned token_job npz, which contain no id/name arrays.

O7. Layout lint `audit_layout.py` on the whole run root (12:43Z): PASS, 276 files, 0 findings, rc 0.

## 2. Logic Chain

1. The control passes 138/138 with 0 skipped in my tree (O2), so every kill in my tree is attributable to the patch, not the environment.
2. Every REQUIRED id's patch, extracted independently from the verifiers' own harness files, makes ≥1 r4 test fail while all 121 pre-existing tests pass (O2). So each named mutant survives the shipped suite and is killed by the new tests: classes (a)–(d) are closed as PI decision 6 defines them.
3. The killing tests are the ones the dispatch specifies: the class (a) real-data test (unmodified script in tmp_path, OUT redirected, compare 300 leaves at rel 1e-9) kills every class (a) mutant except FA11, which is killed by the VRABES-independent synthetic test; the class (a) test skips cleanly without VRABES (O4).
4. The tests are not vacuous: each fails under a named mutant (O2); preconditions are asserted (dead column dropped; Holm = raw; CI excludes 0; cov lo ≤ 0 < corr lo), and my recomputation shows the preconditions hold with the margins the addendum states (O3).
5. Expected values come from pinned outputs or direct computation, not from literals copied from the run (Phase 1 above; O3).
6. No regression: all suites pass, C1 and all receipts verify before and after, no pyc or production byte changed (O4).
7. The worker's evidence is consistent with its raw logs (O6), and my independent run reproduces its table (O2). No fabrication found. No IDs, no git writes (O5, Phase results).
8. Hence CLEAN.

## 3. Caveats

- I did not rerun the 151-patch union or the 16 EXTRA ids (outside the fixed scope); I only checked the worker's union records for internal consistency against raw logs (O6).
- My runner ran one control at the start, not at the end; the production topic3 run after all mutants (138 passed) serves as the end check on shipped code.
- Pre-existing `__pycache__` exists in src/ (`src/__pycache__`, `src/topic1_lagmotif/__pycache__`, `src/topic3_spectral/__pycache__` from iteration 2) and in `scripts/__pycache__` (topic1 pyc 08:29 KST and older). The literal condition "no __pycache__ in src/ or scripts/" is therefore false, but iteration 4 created none (O4). Root's decision.
- Integrity mode was inferred as Development; under any mode the observations contain no flagged pattern.
- My own deviations: DISPATCH.md summarises the long worker JSON fields in brackets (disclosed in the file); early progress.md times were estimates, corrected by an appended note; after the runs I removed pytest basetemps (synthetic torch frames, copies of pinned spectra, the real-data-derived Family A output JSON) and per-job copied trees (16 GB) — listed in `verification/auditor_M2_r4_1/logs/removed_temp_dirs.txt`; logs, JUnit, patch.txt, records, `tree_base` and manifests are kept.

## 4. Conclusion

CLEAN. The four fixed-scope classes are closed: all 26 named mutants (21 unique programs) are killed by the new r4 tests in my own copied tree, each with all 121 pre-existing tests passing. No regression: topic3 138 passed / 0 skipped, old suite 86, topic1 88, C1 67 OK, all six receipts OK including addendum_06, no new bytecode, no production write. The work is genuine. Out-of-scope items go to nonblocking.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
sha256sum tests/topic3_spectral/test_regression_r4.py tests/topic3_spectral/test_token_level_r4.py   # ecceb134… ab99b2b1…
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt         # 67 OK
for r in output addendum_02 addendum_03 addendum_04 addendum_05 addendum_06; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
V=verification/auditor_M2_r4_1; (cd $V && LC_ALL=C sha256sum -c --quiet EVIDENCE_MANIFEST_sha256.txt)
# rerun my mutant set (new output name; runner refuses to overwrite; job trees are rebuilt from tree_base):
cd $V/bin && nice -n 10 /home/juke/superclaude-env/bin/python3 -B run_jobs.py ../runs/CHECK_$(date +%s).json
#   expect J00_CONTROL SURVIVED (138, 0 skipped) and every J01–J21 KILLED with failing_other == []
```
Invalidated by: a REQUIRED id surviving; any pre-existing test failing under a REQUIRED patch; a control failure; a hash change in src/topic3_spectral, scripts/topic3_*.py or the r4 tests; C1 or a receipt failing.
