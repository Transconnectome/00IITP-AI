# worker_M2_r2b — handoff (Hard), M2 Topic 3 iteration 2 (resumed), 2026-11-01 ~01:08Z

**Summary.** I reran the mutants against the shipped topic3 suite (85 tests): the challenger_M2_r1_1 harness N01–N28 (the dispatch named N01–N19; all 28 were run), explorer_M2_r2_2's 18 and explorer_M2_r2_3's 21. That is 67 mutants, 56 distinct patches, all run on copied trees.
- **66 killed, 1 survivor:** `MM 06 zoo <= instead of <`. It is a verdict-rule mutant and not equivalent: card §5 says "Holm p < 0.05", and with B = 9999 a Holm p of exactly 0.05 can occur.
- **New file:** `tests/topic3_spectral/test_verdict_rules_r2b.py` (3 tests). It passes on the shipped code and kills MM 06. Run 2 (88 tests): 67/67 killed.
- **Addendum 03 number check:** 35 quoted claims, 32 agree, 3 text-level mismatches, 0 verdict impact. One extra binding check (PR from stored eigenvalues = stored PR, 4.3e-8 relative) is not counted as a claim.
- **Written:** `docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_04.md`, pinned in `results/topic3/2026-10-31/addendum_04_sha256.txt`.
- **Incident:** my run 2 overwrote run 1's raw logs. I disclosed it in addendum 04 §3 and repeated run 1 as run 3, which reproduced run 1 for 67/67 mutants.
- **Final checks:** all suites and pins pass.

## 1. Observation

**O1. Baseline** (`verification/worker_M2_r2b/baseline/`, 00:35Z)
- C1: rc 0, 67 OK.
- `output_sha256`, `addendum_02_sha256`, `addendum_03_sha256`: rc 0.
- Card hash: OK once the trailing "frozen …" annotation is stripped. `sha256sum -c` on the raw file fails on format only.
- `code_sha256_at_freeze`: only `scripts/topic3_launch_connectome.py` FAILED, which is already disclosed.

**O2. Interruption facts I could verify**
- worker_M2_r2 left DISPATCH, BRIEFING and progress only, with a last heartbeat of 12:12Z.
- Its two tests were written at 12:13:28Z (mtime). Its probe ran 12:14:36–12:15:14Z. Its suite log reads "85 passed" at 12:15:20Z.
- `verification/worker_M2_r2/mutants/` was absent at 00:25Z.
- The pre-edit addendum 03 (in `0db0336`, sha `725d5077…`) contains 1 literal BIDS-prefix token; `ef27b71` (`73489661…`) contains 0.
- On a copy holding the pre-edit addendum, `test_outputs_no_ids.py` and `test_outputs_scanned_nonempty.py` both FAIL (`verification/worker_M2_r2b/probes/pre_edit_addendum03_idscan.log`). The root's one-line edit is what keeps the suite green.
- `addendum_03_sha256.txt` was written by the root: mtime 23:35:15Z, first commit `ef27b71`.
- The 12:17:16Z (addendum written) and 12:17:26Z (interrupted) times are root-reported. The addendum's mtime was overwritten by the root edit, so I could not check them.
- `GATE_STATUS.md` (12:17:50Z) says the "r2 worker … did NOT fix tests". That does not match worker_M2_r2's files.

**O3. Mutation runs** (`verification/worker_M2_r2b/mutants/`). Patches were extracted by AST from the source harnesses (verbatim), each applied to a fresh base-tree copy, and the full suite run without `-x`.

| Run | Suite | Controls (start / end) | Killed | Survivors |
|---|---|---|---|---|
| 1 | shipped, 85 tests | 85 / 85 passed | 66 / 67 | `MM__06_zoo_instead_of` |
| 2 | shipped + r2b, 88 tests | 88 / 88 passed | 67 / 67 | none |
| 3 | shipped, 85 tests (repeat of run 1, separate logs) | 85 / 85 passed | 66 / 67 | same; killed status and failing-test set identical to run 1 for all 67 |

- All 67 patterns applied exactly once. No job returned an rc other than 0 or 1.
- The production tree matched the base-tree manifest after the runs. `make_trees.sh` later rebuilt both trees from production and both manifests were "all OK" (`make_trees_check.log`).

**O4. Log incident.** Run 2 wrote its logs to the same `logs/<job>.*` names as run 1.
- 0 of 69 run-1 logs match the sha256 recorded in `MUTANTS_RUN1.json`; 69 of 69 run-2 logs match theirs.
- Run 3 regenerated shipped-suite raw logs in `logs_run3_shipped/`.
- The runner now refuses to write into an existing log directory. Byte snapshots of the runner versions used for runs 1 and 2 are kept, and their sha256 equal the recorded `runner_sha256`.

**O5. Survivor analysis**
- Card line 90: "≥ 2 of the 3 zoo checkpoints show the same sign with Holm p < 0.05".
- `holm([(1+249)/(1+9999), 0.3])[0] == 0.05` is True. So the `<=` mutant changes the agreement count for a reachable input, and the mutant is not equivalent.
- Real data: every Holm p is 0.0002, so no real verdict changes.

**O6. New test** (`tests/topic3_spectral/test_verdict_rules_r2b.py`, sha `ede1166c…2219`)
- On shipped code: 3 passed (`new_test_on_shipped_code.log`).
- In run 2 it kills MM 06 (2 failed, 86 passed). It also fails under 10 other mutants that the shipped suite already kills.

**O7. Number check (c)** (`probes/check_addendum03_numbers.{py,log,out.json}`)
- All inputs match their pins.
- 35 quoted claims: 32 agree, 3 mismatch, 0 quotes missing.
- Probe (P), pinned JSON (J) and my independent recompute from the pinned npz (I) agree to within 2e-15 (absolute) wherever comparable.
- Mismatches:
  - (i) item 1 L1: "≥ 0.99994 in the top 63". The minimum is 0.99993998 (HCP_N400), 2.4e-8 below.
  - (ii) item 3: "CIs about ±0.002". The half-widths are 0.0020–0.0144; only the primary H1a CI is ±0.002.
  - (iii) item 5: the path omits the top-level `results` key of `family_A`.
- Notes, not mismatches:
  - L5e-5 reaches a count of 9 at L3, which the text covers only implicitly.
  - Both reduced-jackknife conventions give 0.149.

**O8. Final checks** (`verification/worker_M2_r2b/final/`)

| Check | Result |
|---|---|
| topic3 | 88 passed |
| old suite (STRICT_E2E) | 86 passed, 7 warnings |
| topic1_lagmotif | 88 passed |
| C1 | rc 0, 67 OK, identical to baseline |
| `output_sha256` | 42 OK |
| `addendum_02` | 1 OK |
| `addendum_03` | 3 OK |
| `addendum_04` | 2 OK (re-run 01:11Z on the final bytes) |
| card | OK |
| freeze list | only the launcher differs |
| ID grep (BIDS prefix + alphanumeric) over my outputs | 0 hits |
| the two ID-scan tests, re-run on the final addendum 04 bytes | 2 passed |
| `audit_layout.py` on the run root | PASS, 130 files, `findings: []` |

**O9. Git context (not my writes)**
- Commits `a18006d` (09:31:26 KST), `bd1f991` (09:46:26) and `e8c795e` (10:01:26), all titled "docs(iitp): checkpoint four-topics teamwork documents", run on a 15-minute cadence.
- They included my DISPATCH, BRIEFING and progress files and addendum 04.
- `e8c795e` holds an earlier addendum 04 (sha `1a5ecb77…`). I then corrected the §6 claim count, so the final pinned version is `a1828b38…`. Until the next checkpoint commit the working copy differs from HEAD.
- The r2b test and `addendum_04_sha256.txt` are still untracked.
- I cannot tell whether these commits came from the root's checkpoint job or from chavis-autocommit (900 s). I made no git command that writes.

## 2. Logic Chain

1. O1 and O3 (control passes; production equals the manifest) mean the mutation results describe the shipped bytes.
2. O3 run 1 and run 3 show that the shipped suite kills every mutant except MM 06. That includes every iteration-1 survivor from challenger_M2_r1_1 (N02, N05, N06, N08–N11, N17) and those carried in `kill_demo.py`.
3. By O5, MM 06 is a verdict-rule mutant that is not equivalent. So under the dispatch's conditional ownership I created the r2b test file. By O6 it passes on shipped code (the dispatch's stop condition is not triggered) and kills MM 06, so finding 3 of challenger_M2_r1_1 is closed for the assigned mutant set.
4. By O2, addendum 03's §4 pointer and its §8 "mutant runs" have no receipts. Addendum 04 supersedes them with the real evidence location, as the dispatch asked in (d).
5. By O7, addendum 03's numbers are correct apart from 3 text-level slips. None of them touches a verdict or the Family B reading.
6. By O4, the run-1 raw-log bytes are lost. Run 3 reproduces run 1 exactly, so the shipped-suite conclusion rests on run-3 logs plus the run-1 JSON record. The incident is disclosed, not hidden.

## 3. Caveats

- **Mutant scope** is the assigned three sets. The other verifiers' full harnesses (reviewer_M2_r1_1/2, auditor_M2_r1_1, challenger_M2_r1_2 p6, worker_M2_r1) were not rerun; their r1 survivors are included via `kill_demo.py`. I did not run boundary siblings of MM 06 (`lo >= 0` in D1/D3, `>= 0` in the primary CI, primary `<=`). The primary 0.05 boundary is exercised by an existing shipped test, but the mutant itself was not run.
- **The timeline** relies on root-reported times for 12:17:16Z and 12:17:26Z.
- **Excluded from the copied tree:** `scripts/chrome_user_data*`, which are git-ignored browser profiles that no test reads. This was a deliberate safety choice, recorded in addendum 04 §3.
- **Log redaction:** the runner redacts the BIDS-prefix-plus-alphanumeric pattern in logs at write time. There were 0 replacements, and the only occurrences of the bare prefix are quoted test source.
- **Another team (M1)** works in parallel. The topic1 suite passed at 01:05Z, but their files may change afterwards.
- **"Verdict-path" classification** (rule / input / descriptive) is my labelling. It does not affect the outcome, because every mutant was either killed or would have needed handling regardless.

## 4. Conclusion

M2 iteration 2 deliverables are complete and additive:
- Mutation evidence: `verification/worker_M2_r2b/mutants/MUTANTS_SUMMARY.json` plus run JSONs and logs.
- One guard test file, for the single non-equivalent survivor.
- Addendum 04, covering the timeline, the dangling pointer, the root edit, the evidence location, the 67-row mutant table, the new test, the (c) mismatches and the log incident.
- The receipt `addendum_04_sha256.txt`.

No verdict changes, no src/scripts edits, no pinned-file edits, 0 GPU. Ready for the r2b verifier gate. For that gate, verifiers should re-derive MM 06's non-equivalence and check that run 3 reproduces run 1.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # rc 0, 67 OK
for f in output_sha256 addendum_02_sha256 addendum_03_sha256 addendum_04_sha256; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/$f.txt; done
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic3_spectral   # 88 passed
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q   # 86 passed
V=verification/worker_M2_r2b
bash $V/make_trees.sh                                     # both manifests "all OK" (rebuilds tree_base, tree_base_r2b)
cd $V/mutants && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 run_mutants.py MUTANTS_RUNX.json --jobs 6 --base ../tree_base --logs logs_runX   # expect survivors == ['MM__06_zoo_instead_of']
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 run_mutants.py MUTANTS_RUNY.json --jobs 6 --base ../tree_base_r2b --logs logs_runY --only MM__06_zoo_instead_of   # expect killed
cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I $V/probes/check_addendum03_numbers.py   # 32 OK, 3 MISMATCH, 1 INFO
```

(Delete the rebuilt trees and the `logs_runX`/`logs_runY` folders afterwards.)

**Invalidation conditions:**
- Any pinned file changes.
- `analysis.py` changes.
- The r2b test fails on unmodified code.
- A rerun of run 1 shows a different survivor set.
- `holm([0.025, 0.3])[0] != 0.05`, which would make MM 06 equivalent at the card's resolution.
