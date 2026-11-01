# reviewer_M2_r4_1 — handoff (Hard), M2 Topic 3 iteration 4, fixed-scope gate (PI decision 6), 2026-11-01

**Verdict: APPROVE** (advisory; the gate decision belongs to the root/PI, per sci-pipeline §2).

All four fixed-scope classes (a)–(d) are closed. I took the 26 named mutants verbatim from the four r3 harness files, applied them one per job with my own runner in my own copied tree, and every one is killed by an r4 test of its own class. The same 26 patches survive the shipped 121-test suite, so each kill is attributable to the r4 tests alone. Nothing regressed: production topic3 138 passed (0 skipped), old suite 86, topic1 88, C1 67/67, all six receipts OK, and no new bytecode. I found no integrity problem. Out-of-scope items are listed as nonblocking (§3).

Evidence root: `/home/juke/git/00IITP-AI/verification/reviewer_M2_r4_1/` (bin/, runs/, logs/, probes/, baseline/, tree_base/ with `tree_base.manifest_sha256.txt`).

## 1. Observation

O1. **Artifacts under review** (sha256 measured 12:26Z, unchanged at 13:01Z):
- `tests/topic3_spectral/test_regression_r4.py` `ecceb13422531ee5a41e48b04763f02607b9427d242a3b1baface17ed2e0fbed` (7 tests; classes (a), (d));
- `tests/topic3_spectral/test_token_level_r4.py` `ab99b2b152515ea6ad8a5e0cb05d65af61d84ce4ca8c3efd36eab4b73e4a68d1` (10 tests; classes (b), (c));
- `docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_06.md` `19b6218ffdd57fc9293e3659e78de9abbb717e14a7545dfd3715c597cd312756`;
- `results/topic3/2026-10-31/addendum_06_sha256.txt` `6191bd5acb77f77cf8bbbcbd3555d838d8c73b2121a614355dc66314ff05d510`, which pins the three files above.
All match the worker's claims.

O2. **Additivity** (`logs/final_additivity.txt`). Each of the 31 files `tests/topic3_spectral/*.py` (18), `src/topic3_spectral/*.py` (6) and `scripts/topic3_*.py` (7) matches, by exact hash and path, a line in `output_sha256.txt`, `code_sha256_at_freeze.txt` or `addendum_0{3,4,5,6}_sha256.txt` (31 PINNED, 0 UNPINNED). `code_sha256_at_freeze.txt` mismatches only `scripts/topic3_launch_connectome.py`. That change predates this iteration: addendum 01 (`2026-10-31_topic3_addendum.md`) line 8, item 2, discloses it, and `output_sha256.txt` pins it.

O3. **Named mutants: my own extraction.** `bin/run_mutants.py` parses the four r3 harness files with `ast` and imports or executes none of them. Their hashes match the expected values:
- reviewer_M2_r3_1 `my_mutants.py` `17a30dca…`;
- reviewer_M2_r3_2 `run_mutants.py` `ca6d7381…`;
- challenger_M2_r3_1 `mutants/specs.py` `d5f73f38…`;
- challenger_M2_r3_2 `mutants/my_specs.py` `0be048a3…`.

The extraction gives 26 REQUIRED ids (the dispatch's list) and 21 unique patched files. Each `old` string occurs exactly once in the base file. Each id ran as its own job, with no merging.

O4. **Tree.** `bin/build_tree.py` byte-copies 171 production files into `tree_base`: `src/**/*.py`, `scripts/*.py`, `tests/__init__.py`, `tests/topic3_spectral/*.py`, `results/topic3/**` and `docs/03_empirical_analysis/topic3/**`. Every copy is hash-checked (manifest `c8c8672e…`), and the tree has no `__pycache__`.
- `tests/topic3_spectral/helpers.py:5` resolves ROOT from the file's own location, so a mutant in the copied tree reaches the class (a) real-data test, which copies `src/topic3_spectral` from ROOT.
- `io_contract.VRABES_RA` is absolute (`io_contract.py:22`), so the real-data test runs in the copied tree.

O5. **r4 suite per mutant** (`runs/R4_named.json` `2bfec2f5…`; runner v1 `13774d60…`, preserved as `bin/run_mutants_v1_used_for_R4_named.py`). The control gave 17/17 passed.

Each job checks that the module the tests import is the patched file (`import_ok` true for all 26), then runs the two r4 files with `timeout 900 nice -n 10`, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, a per-job `--basetemp`, an absolute `--junitxml`, and at most 2 at a time.

**Result: 26/26 KILLED.** In every job:
- every failing test belongs to the mutant's own class, and 0 tests fail outside it;
- 0 tests error, 0 are skipped (the real-data test ran in all 26), and there were no retries.

Per class:
- **(a) 20 ids.** Both class (a) tests fail on value or key-set assertions. Examples: B_E1_iid_wrong_n gives "56 of 300 values differ"; CR3_A02 and FA08 fail the key-path assertion at `test_regression_r4.py:78`.
  - FA11 is the exception: it fails only the synthetic test ("2 of 298 values differ", `pr_corr`), as designed, because it changes no real-data value.
- **(b) T01, T02, TJ03.** Both `test_subject_summary_matches_card_definitions_for_every_variant` (lines 161/162, the L2 or L3 value) and `test_packed_spectra_feed_the_card_contrasts` (line 180) fail.
- **(c) N01.** All 8 class (c) cases fail: 6 hand-built and 2 computed (`assert False is True` on `primary_significant`).
- **(d) VA01, VA02.** Exactly the corr-only stub case fails (`[-0.3-0.4-drop not robust]`), and so does the computed witness. VA01 gives "drop robust in cov only…" and VA02 "drop robust and not a per-channel-scale effect".

O6. **Shipped 121-test suite per mutant** (`runs/SHIPPED_named.json` `cdfb72a1…`; runner v2 `fd58777f…`, which adds only own-process-group cleanup). The control gave 121/121 passed, and **all 26 SURVIVE** (rc 0, 121 passed, 0 failed, 0 skipped). This reproduces the r3 finding that the shipped suite misses them, and attributes each kill in O5 to r4 tests only.

O7. **Production regression** (`bin/prod_checks.sh prod1`, 12:41:00–12:42:38Z):
- `tests/topic3_spectral`: 138 passed, 0 failed, 0 errors, 0 skipped (`logs/prod1_topic3.junit.xml`);
- old suite (`STRICT_E2E=1`, `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed, 7 warnings;
- `tests/topic1_lagmotif`: 88 passed;
- C1: 67/67 OK, rc 0;
- receipts: output 42, addendum_02 1, 03 3, 04 2, 05 3, 06 3 — all OK, rc 0.

The checks were repeated at 13:01Z (`logs/final_*`) with identical results.

O8. **Bytecode** (`baseline/pyc_listing_start.txt` taken 12:31Z; `logs/prod1_pyc_diff.txt` and `logs/final_pyc_diff.txt` are both empty).
- No `.pyc` under `src/`, `scripts/` or `tests/` is newer than the r4 start (07:34Z).
- Pre-existing `__pycache__` folders are present in `src/` and `scripts/`:
  - `src/__pycache__`: 10 files, 2026-10-30;
  - `src/topic1_lagmotif/__pycache__`: 9 files, 2026-10-31T23:29:58Z;
  - `src/topic3_spectral/__pycache__`: 3 files, 2026-11-01T00:39:14Z, from iteration 2;
  - `scripts/__pycache__`: 4 files, including 2 topic1 files from 2026-10-31T23:29:58Z.
- There is no `scripts/__pycache__/topic3_*`. No production file under `src`, `scripts`, `tests`, `results/topic3` or `docs/03_empirical_analysis/topic3` is newer than my start at 12:25Z.

O9. **Witness numbers** (`probes/witness_numbers.out.json` `984e4801…`, run on the unmutated tree):
- (c) H1a raw = Holm 0.0380 (Bonferroni 0.076), CI [0.000622, 0.01074]; H1b raw = Holm 0.0347 (Bonferroni 0.0694), CI [0.000622, 0.01085]. The other primary has raw p 1e-4 in both cases. The verdict is "holds" with 3 agreeing.
- (d) cov [−2.94206, −1.66048] and corr [+13.87694, +15.44039] at S = 2000, m = 28, giving "drop not robust".

These equal the worker's and addendum 06 §3's numbers.

O10. **Skip path** (`bin/skip_probe.sh`, `logs/skip_*`). In a copied tree with `VRABES_RA` pointed at a nonexistent directory:
- the class (a) real-data test is SKIPPED ("a pinned VRABES pooled input is absent") and the other 16 pass;
- with FA01 also applied, the synthetic class (a) test still fails (1 failed, 15 passed, 1 skipped).

O11. **Genuineness of the tests** (read in full).
- **Source of the expected values.** They come from card literals (`test_regression_r4.py:54`, `test_token_level_r4.py:48`), from independent numpy code (D×D covariance against the shipped Gram path, `np.corrcoef` against standardize+eig, the textbook jackknife, a direct LN0), and from the receipt-checked pinned JSON (`_pinned_family_a`, which asserts its hash against `output_sha256.txt`).
- **What is replayed.** Only the Monte Carlo draw method and the seed schedule (iid draws, column permutation, index sets) are replayed. This is needed for an rel-1e-9 comparison of MC quantities, and addendum 06 §6 discloses it.
- **No hardcoded outputs.** No expected value is taken from the module under test. The one exception is a precondition: class (c) checks the hand-built records' Holm consistency against the shipped `resampling.holm` (`test_token_level_r4.py:210-211`). The expected Holm values themselves are hand-written literals.
- **Production safety.** The real-data test writes only inside `tmp_path`, asserting the output path at line 149 and checking at line 130 that the output did not exist beforehand. It runs the script as a subprocess with `PYTHONDONTWRITEBYTECODE=1` and imports no production script.
- **Consistency with the r3 requests.** The tests implement exactly the additive fixes the r3 verifiers asked for:
  - reviewer_M2_r3_2 handoff:107;
  - challenger_M2_r3_1 handoff:155-157;
  - challenger_M2_r3_2 handoff:150-155, items 1–3, except the VB02 part of item 3, which is out of scope;
  - reviewer_M2_r3_1 handoff:39-44.

O12. **Worker evidence spot-checks.**
- `EVIDENCE_MANIFEST_final_sha256.txt`: 657/657 OK.
- The records N001 (N01), N012 (T01), N022 (FA11) and N024 (VA01) were checked against their raw files: the junit and log sha256 match the records, and each recorded failing list equals the failures in the raw junit (8, 2, 1 and 2, all in the r4 files).
- The superseded addendum v1/v2 and receipts are kept byte-identical in `verification/worker_M2_r4/superseded/` (hashes `af805513`, `46527e6a`, `4c1df35e`, `db88f543`), with a README.
- I found no BIDS subject prefix in either r4 test or in addendum 06. flake8 (max-line-length 120) is clean.

O13. **Layout lint** (`logs/audit_layout_mid.log`, 12:45Z, whole-run metadata root): PASS, 276 files, no findings.

## 2. Logic Chain

1. **Classes closed.** The gate asks whether every named mutant is killed by the new tests in my own copied tree. O3–O5 show that all 26 are, with verbatim triples, verified patched imports and in-class failures only. O6 shows the same patches survive the shipped 121. So each class (a)–(d) is closed as PI decision 6 defines it, and the closure is due to the r4 tests.
2. **Kills are not artefacts.**
   - The r4 control (17/17) and the shipped control (121/121) on the unmutated tree are green.
   - Every kill is a value or key assertion, not an error or collection failure.
   - The real-data test ran in every job, with 0 skips.
3. **The class (a) requirement as dispatched is met.** O4 and O11 show that the unmodified script runs in tmp_path with OUT redirected, and that all 300 non-run leaves, plus the deterministic run fields, are compared at rel 1e-9 with the receipt-checked pin. O10 shows the test skips cleanly without VRABES while the synthetic guard remains.
   - **Class (b).** All 5 variants' cat_covpr and cat_corrpr are checked, together with the dropped count, the eigenvalues, the frame, H4 and pooled values, and the floor case.
   - **Class (c).** Hand-built cases and computed B = 9999 cases are both present (O9).
   - **Class (d).** A truth table and the computed witness are both present (O9).
4. **No regression.** The checks in O7 pass, as does O8 read as "no bytecode created by this iteration". O2 shows that no pinned file changed. Nothing in production changed during my review (O8).
5. **The work is genuine.** O11 and O12 show independent expected values, no hardcoded outputs, verbatim mutants, and records consistent with their raw logs. The worker's disclosures (fixture change before freeze, INVALID runs, superseded addenda) are recorded and consistent with the files.
6. Therefore: **APPROVE**.

## 3. Caveats

- **The pycache clause.** The dispatch lists "no __pycache__ in src/ or scripts/". Taken literally, that is false today (O8). I read it as "none created" because:
  - every folder predates r4;
  - the worker may not delete files it does not own;
  - nothing new appeared during r4 or my runs.

  If the root intends the literal reading, those folders (none created by r4) must be deleted by their owner. That is a root action, not an r4 defect.
- **Not rerun by me:**
  - the worker's 16 EXTRA-id statuses (VB02, N06, N12, FA13, FA14, GD01–03 survive; N03, N04, A03, A04, A06, A09/MC02 and MC01 are killed);
  - the 151-patch union.

  Neither is in the gate criterion. I take them as worker-reported and check them only through the 4 spot-checks in O12.
- **Scope of the evidence.** My per-mutant r4 runs use only the two r4 files. Attribution comes from the separate shipped-121 run (O6), not from a single 138-test run per mutant.
- **The real-data comparison** passed at OMP_NUM_THREADS=2. I did not test other BLAS thread counts.
- **tree_base is kept.** It contains byte copies of `results/topic3` (pinned, position-keyed outputs and spectra, no identifiers) so that my runs can be reproduced. It can be deleted and rebuilt from its manifest.

## 4. Conclusion

APPROVE for the M2 r4 fixed-scope gate. Classes (a), (b), (c) and (d) are closed: 26/26 REQUIRED mutants are killed in-class by the r4 tests and survive the shipped 121. There is no regression: 138/86/88, C1 67, receipts 42/1/3/2/3/3 including addendum_06, and no new bytecode. The work is genuine.

**Nonblocking (out of scope; for root/PI):**
1. The literal pycache clause and the pre-existing `__pycache__` folders (O8).
2. VB02, the untested halts (N06, N12, GD01–03), the tie-only mutants FA13/FA14, and U127 survive, per the worker. They are listed in addendum 06 §5.
3. The class (b) fixtures have n > D, so the Gram path (n < D, which the real 1120×1536 token matrices take) is not exercised at token level. It is exercised by the synthetic Family A test; addendum 06 §6 discloses this.
4. The class (a) real-data test reruns the frozen Family A script on the real inputs in every suite run and leaves a position-keyed JSON in pytest's basetemp. PI confirmation of the "no rerun" reading is pending (addendum 06 §6).
5. The class (a) real-data guard skips without VRABES. The synthetic guard remains (O10).
6. **Brittleness, failing closed.**
   - The class (c) computed witness's CI lower bound is about 6.2e-4: a legitimate seed or bootstrap change would trip the test's precondition and fail it, never pass it falsely.
   - The synthetic replay of the seed schedule likewise fails on a legitimate draw-order refactor (disclosed in §6).
7. Addendum 06 §5 items 2, 9–13 and 15 carry over unchanged: the label misnomer, the inconsistent r3 hand-built record, the Family B skip without VRABES, the basetemp residue, the r3 `exec_module`, the Pool deadlock, and the stale notes.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # 67 OK
for r in output addendum_02 addendum_03 addendum_04 addendum_05 addendum_06; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
V=verification/reviewer_M2_r4_1
bash $V/bin/prod_checks.sh <newtag>                    # topic3 138 / old 86 / topic1 88 + C1 + receipts + pyc diff
cd $V/bin   # fresh output names; the runner refuses to overwrite
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B run_mutants.py --suite r4 --control --out ../runs/CHECK_r4.json        # expect CONTROL_OK + 26 KILLED
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B run_mutants.py --suite shipped --control --out ../runs/CHECK_sh.json   # expect CONTROL_OK + 26 SURVIVED
bash skip_probe.sh                                     # logs/skip_novrabes*.log: 16 passed 1 skipped; FA01 variant 1 failed
```

The conclusion is invalidated by any of the following:
- a hash change of either r4 test, addendum 06 or its receipt;
- any REQUIRED mutant surviving the r4 files;
- any of the 26 failing the shipped 121, which would mean the kill is not attributable to r4;
- a failing or skipped test in production topic3;
- any change under `src/topic3_spectral` or `scripts/topic3_*.py`;
- any `.pyc` newer than 2026-11-01T07:34Z.

## Own deviations

- DISPATCH.md copies the dispatch verbatim up to the worker JSON's `frozen_artifacts_sha256` field and summarises its remaining fields in brackets. This is disclosed inside the file.
- progress.md first gave the additivity file count as 33; the correct count is 31. A correction line was appended, and the original line was not edited.
- My runner was edited after the R4 run (v2 adds process-group cleanup). The bytes used for R4 are preserved as `bin/run_mutants_v1_used_for_R4_named.py` (`13774d60…`).
- I wrote one scratch file, `allpins.txt` (a receipt concatenation), to the session scratchpad, which other agents also use. No other agent's files reference that name. I removed it at close-out, and its result is kept in `logs/final_additivity.txt`.
- No git command was run. 0 GPU. No production file was edited or written.
