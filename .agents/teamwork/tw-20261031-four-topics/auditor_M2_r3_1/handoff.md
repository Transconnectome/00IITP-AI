# auditor_M2_r3_1 — handoff (Hard). Forensic integrity audit, M2 (Topic 3) iteration 3, 2026-11-01T07:15Z

## Forensic Audit Report

- **Work product:** worker_M2_r3's iteration-3 deliverables:
  - `tests/topic3_spectral/test_verdict_rules_r3.py` (58c64ccb…)
  - `tests/topic3_spectral/test_token_stats_wiring_r3.py` (b091b0b8…)
  - `docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_05.md` (a4001f09…)
  - `results/topic3/2026-10-31/addendum_05_sha256.txt` (1e542da7…)
  - `verification/worker_M2_r3/`
- **Profile:** General Project. The integrity mode is Development: ORIGINAL_REQUEST.md has no "from scratch" or "must not delegate" constraint.
- **Verdict: CLEAN.**

I ran every check myself. My evidence is in `/home/juke/git/00IITP-AI/verification/auditor_M2_r3_1/`.

### Phase results

| Check | Result | Evidence |
|---|---|---|
| Deliverable hashes = claimed | PASS | All 4 deliverables plus MUTANTS_SUMMARY, S88_v2.json, FULL_v2.json, union_specs.py, run_union.py and the S88 runner snapshot match the claimed sha256. |
| C1 protected hashes | PASS | 67 OK, rc 0, at start and at end (`runs/post_c1.log`). |
| Topic 3 receipts | PASS | output 42, addendum_02 1, addendum_03 3, addendum_04 2, addendum_05 3, all OK at start and end (`runs/post_*.log`). |
| src/scripts/pinned tests unchanged | PASS | `git diff HEAD` is empty for tracked src/topic3_spectral, scripts/topic3_*.py and tests/topic3_spectral. code_sha256_at_freeze has 26/27 OK; the one mismatch, `scripts/topic3_launch_connectome.py`, predates this iteration and is disclosed in addendum 01 item 2. |
| Hardcoded results / facade | PASS | No src or scripts change. The new tests compute through the shipped producer or use hand-built records with stated expectations. I reran Family A and Family B in my own copied tree: 300/300 and 508/508 leaves are bit-identical to the pinned outputs, the code hashes are identical, and so are the verdicts (`runs/rerun_compare.txt`). |
| Tests that cannot fail / pass vacuously | PASS | See the production run and the mutation runs below. The only skip path is `needs_vrabes`, and it is not triggered on this host (0 skipped). |
| Fabricated or dangling evidence | PASS | Every path in addendum_05 and handoff.md exists, except items explicitly described as deleted. All 9 harness sha256 prefixes in addendum_05 §4 match. All 302 raw mutant logs exist; each sha256 equals MUTANTS_SUMMARY, each mtime falls inside its run window, and the statuses agree with the run JSONs. The runner hashes itself at runtime (run_union.py:173). The S88 and FULL base-tree manifests match production for all 20 shipped code and test files. Run JSONs were written only by the runner; no post-run edit appears in the transcript. |
| Results before card freeze | PASS (N/A this iteration) | Iteration 3 produced no new result. Earlier ordering: card frozen 08:48:29Z; Family A started 08:49:18Z; Family B written at 09:02Z. |
| Silent fallbacks | PASS, with a note | The skipif is visible as a skip, not silent. If VRABES were absent, 5 of the 6 wiring tests would skip (non-blocking N2). |
| Participant-ID leakage | PASS | I loaded the 57 real IDs from the pinned VRABES npz `ids` arrays in memory, never printed them, and scanned for them. 0 matches in the r3 tests, addendum_05, the receipt, `verification/worker_M2_r3/` (1076 files), the worker metadata, the worker's full native transcript, `/tmp/pytest-of-juke` (48,835 files), and my own outputs and metadata (150 files, scanned last). The spectra npz hold numeric arrays only, with no ids key. |
| Writes to protected or production paths, incl. bytecode | PASS | The full-text transcript scan shows production writes only to the worker's own 4 deliverables. Since 02:57Z, the only other changed files are the GPU ledger (M3) and topic2/topic4 files (workflow B). No .pyc or __pycache__ in src, scripts, tests, docs or results is newer than iteration start. The iteration-2 pyc files from 00:39:14Z remain and are not this worker's. |
| ENIGMA on B300 | N/A, PASS | M2 never touches ENIGMA; C6 was relaxed by PI decision 5. |
| GPU use | PASS | The transcript has no ssh, nvidia-smi or B300 call. The GPU ledger has no M2 row. |
| Git writes by agents | PASS | The transcript's git calls are log and show only. All commits in the 02:57–06:24Z window follow the root checkpoint loop's cadence (PID 3270989, `autocommit.sh`, started 10-31 16:31:23 KST). |
| Layout lint (whole run root) | PASS | 236 files, findings []; after my metadata writes, 242 files, findings [] (`runs/audit_layout_run_root.log`, `runs/audit_layout_run_root_final.log`). |
| C2 old suite and topic1 (production, run by me) | PASS | `STRICT_E2E=1 … pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` gives 86 passed, 7 warnings (`runs/old_suite.log`, `.junit.xml`); `pytest tests/topic1_lagmotif` gives 88 passed (`runs/topic1.log`). Both ran concurrently with PYTHONDONTWRITEBYTECODE=1 and timeout 900. Afterwards, find -newer shows no production file and no bytecode written. |

## 1. Observation

- **O1.** In production, `PYTHONDONTWRITEBYTECODE=1 … pytest -p no:cacheprovider -rs tests/topic3_spectral` gives **121 passed in 69.34s**. JUnit shows tests=121, failures=0, errors=0, **skipped=0**, and 33 r3 tests collected (27 + 6). Files: `runs/prod_topic3.log`, `runs/prod_topic3.junit.xml`. No production file or bytecode was written (find -newer, before and after).
- **O2. Own mutation run** `runs/MUT_A.json` (sha256 ea01d6d1…, runner `mut_runner_a.py` 1c3a43ef…). It used my own copied tree, my own patch applier and timeout 900, with 2 jobs. Controls passed: 88 (s88) and 121 (full). There were 0 INVALID and 0 NOT_APPLIED.
  - **13 union patches** were taken verbatim from the FULL_v2 record. I confirmed each one verbatim in the original verifier harness files:
    - U057 (V01), U066 (V05), U070/U071/U072/U105 (CI producer), U078 (A01), U090 (X01/V29), U091 (X02), U118 (V26), U120 (V28), U139 (S03): every one **SURVIVED** the shipped 88 and was **KILLED** by the full suite. Only r3 tests failed (0 other failures).
    - U127 (A15) SURVIVED both, as the worker reported.
  - **13 fresh mutants I wrote**, hitting the same rules with different syntax:
    - `min(p_holm, p_signflip)`;
    - producer returning (hi, lo);
    - bootstrap of the median;
    - CI seed +2;
    - CI of the raw difference;
    - zoo CI-product condition;
    - `len(agree) >`;
    - m25 rows reversed;
    - ZOO tuple reordered;
    - primary = ZOO[1];
    - verdict drops ZOO[2];
    - subject script positions reversed;
    - Bonferroni at the call site.

    **All 13 were KILLED** by the full suite. 10 of the 13 SURVIVED the shipped 88, so r3 tests alone killed them. Table: `runs/MUT_A_table.txt`.
  - Kills are real assertion failures, not crashes. A sweep of MUT_A.json finds that all 28 KILLED entries (25 full, 3 s88) have rc 1, JUnit failures > 0 and 0 errors. Three sampled logs: U057 gives `assert True is False`; U072 gives "40 of 508 values differ from the pinned output" plus CI asserts; U091 fails a verdict-JSON mismatch.
- **O3. Evidence chain of the worker's runs.**
  - S88_v2: 101 KILLED / 50 SURVIVED. FULL_v2: 150 KILLED / 1 SURVIVED. Both recounted from the run JSONs (153 entries each, including 2 controls).
  - 302 logs, 0 missing, 0 sha mismatches, 0 mtimes outside 03:38–04:03Z (S88) and 04:31–05:56Z (FULL).
  - runner_sha256: S88 = 6614112d…, which equals runs/S88_v2_runner_snapshot.py; FULL = 369b62e8…, which equals the current run_union.py.
- **O4. Worker native transcript** `subagents/workflows/wf_c7ee9ab8-f5e/agent-ad2c5862ed1faddd3.jsonl`: 226 tool calls, full-text scan (`probes/worker_r3_tool_inputs_full.jsonl`).
  - There are 0 git write subcommands and 0 ssh, nvidia-smi or 61.107.201 calls.
  - The only production redirects are to `results/topic3/2026-10-31/addendum_05_sha256.txt`: created at 06:05:39.603Z under a `test ! -e` guard (this explains the dir mtime of 06:05:39.8Z) and rewritten at 06:16:17, 06:18:19 and 06:18:52.
  - The Python writes target the worker's own addendum_05, run_union.py, the S88 snapshot and its own metadata.
  - All deletions are inside `verification/worker_M2_r3/`. There are 0 reads of secrets.
- **O5. Numbers recomputed** from the pinned JSON and from the test builders in my tree. All match addendum_05:
  - H1b geometric-mean ratio − 1: HCP −10.7%, L1e-4 −3.2%, primary +4.6%, L5e-5 +8.2%. H1a: −12.8%, +2.3%, +3.9%, +5.0%.
  - CI half-widths 0.00203–0.01442 (H1a 0.0020–0.0096, H1b 0.0039–0.0144).
  - Class-1 fixture: raw p 0.0326, Holm p 0.0652, CI lower bound 0.00069; the shipped verdict is "killed".
  - Class-2 fixture: Holm p 0.0321 / 0.0308, CI lower bound −0.00144 / −0.00142.
  - Git: addendum_03 is in 4ce1917 and ef27b71 only; 0db0336 does not touch it.
- **O6. Git (read-only).**
  - The four addendum_05 drafts (70bd178, 6bf2de7, 55ba1e0, 08f7b6f) and the final bytes in a910c53 (15:31:28 KST, after the worker's last edit at 06:18:52Z) are root checkpoint commits.
  - The r3 .py files and the receipt are untracked.
  - The same loop also committed my metadata (cb10a30, 16:01 KST). That is not my git write.

## 2. Logic Chain

1. No src or scripts byte changed (O1 diff, freeze receipt), and my independent reruns reproduce the pinned outputs bit for bit (rerun_compare). So no real-data verdict changed, and the pinned results are genuine outputs of the frozen code, not hardcoded values.
2. The r3 tests pass on shipped code with 0 skips (O1). Each blocking-class defect, in both the verifiers' original form and my own different-syntax variants, makes r3 tests fail with assertion errors (O2). So the tests can fail and are not vacuous for the targeted rules.
3. The worker's mutation evidence is internally consistent, hash-bound to logs written inside the run windows, and produced by a runner that hashes itself (O3). My independent run reproduces its classification for every patch I sampled (O2). So the evidence is not fabricated.
4. The transcript shows no git writes, no remote or GPU calls, and no writes outside the worker's own deliverables and verification folder (O4). The bytecode and file-change scans agree (Phase table). So none of the conduct constraints (C4, C5, C7, pinned files) was violated.
5. 0 real-ID matches across all outputs, the transcript and the temp copies, so C4 identifiers held.
6. No check failed, so the verdict is CLEAN.

## 3. Caveats

- **ID scan scope.** I matched the full `sub-…` strings of the 57 pinned IDs. The ID cores are shorter than 6 characters, so I did not run a prefix-less core search (too many false positives). The project's own `sub-` and `ids`-array tests also pass.
- **Mutation sample.** I sampled 13 of the 151 union patches, plus 13 fresh ones. I did not rerun all 151; the remaining classification rests on the worker's hash-bound logs (O3).
- **U127 classification.** I did not adjudicate it beyond the note under Non-blocking.
- **Root conduct.** The root checkpoint loop and root conduct (commits that include protected files, from earlier gates) are outside this worker's scope and were not re-audited.
- **Other agents.** Other r3 verifiers were running at the same time. `/tmp/pytest-of-juke` changed during my scan; the scanner skipped files that vanished mid-scan.

## 4. Conclusion

**CLEAN.** I found no integrity violation in iteration 3. Non-blocking items for the root and PI:

- **N1. U127 (A15) "equivalent".** The changed `direction` label for a zero mean can be reached (a = b) and does appear in the output JSON. It is equivalent only with respect to the card-defined verdict. The classification is disclosed honestly; it is a judgment call, not an integrity issue.
- **N2. `needs_vrabes`.** If VRABES is absent, 5 of the 6 wiring tests skip, which would silently remove the class-5 guard on such a host. On this host 0 are skipped.
- **N3. Real-data re-derivation.** The wiring tests rerun `topic3_token_stats.py` on the real pinned spectra in every suite run, and copies of the spectra are left in pytest's basetemp under /tmp. The worker also ran a disclosed timing probe of the real-data script in a copied tree. PI decision 1 said "no rerun". Both re-derive and discard the output and are disclosed, but the PI may want to confirm that this reading is acceptable.
- **N4. Latent bytecode hazard.** `test_subject_level_script_passes_the_neurostorm_alignment_positions` calls `exec_module` on the production `scripts/topic3_subject_level.py`. If the suite runs without PYTHONDONTWRITEBYTECODE, that writes `scripts/__pycache__/topic3_subject_level.cpython-312.pyc`. It has not happened (no topic3 pyc in scripts/__pycache__). The same class of hazard already exists for the src imports.
- **N5.** The iteration-2 `src/topic3_spectral/__pycache__/*.pyc` (00:39:14Z) still exist. They are not this worker's, and deleting them is the root's decision.
- **N6.** The S88_v2 base tree was deleted; only its manifest remains. The manifest proves byte identity for the shipped code, so S88 is reproducible by rebuilding the tree.
- **N7. Git state.** The r3 tests and the receipt are untracked, so they are pinned only by the receipt. addendum_05's final bytes were committed by the root loop (a910c53).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt         # 67 OK
for r in output addendum_02 addendum_03 addendum_04 addendum_05; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD OMP_NUM_THREADS=2 nice -n 10 timeout 900 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -rs -q tests/topic3_spectral   # 121 passed, 0 skipped
V=verification/auditor_M2_r3_1
bash $V/make_tree_a.sh $PWD/$V/tree_base          # rebuild the mutation base (manifest-checked); then:
cd $V && PYTHONDONTWRITEBYTECODE=1 nice -n 5 /home/juke/superclaude-env/bin/python3 -B mut_runner_a.py $PWD/runs/MUT_B.json   # expect the MUT_A_table.txt classification
```

This verdict is invalidated if any of the following happens:
- a receipt fails;
- an r3 test file differs from 58c64ccb… or b091b0b8…;
- a union blocking mutant survives the full suite;
- a production run skips any of the wiring tests;
- a real-ID match appears in any iteration-3 output.

## Deviations (mine)

- DISPATCH.md first recorded the worker's inline JSON as a bracketed summary. The verbatim JSON from the native journal was appended at 06:4xZ.
- I reran `scripts/topic3_subject_level.py` and `scripts/topic3_token_stats.py` once in my own copied tree (`tree_rerun`, now deleted). This is allowed: under 15 min CPU, with OUT ROOT-relative. The outputs were kept only as verification artifacts (`runs/rerun_family_*.json`) and are not results.
- I deleted the copied trees after the runs; their manifests are kept. I wrote no bytecode and made no git write. GPU use was 0.
