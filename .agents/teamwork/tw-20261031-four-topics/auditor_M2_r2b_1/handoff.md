# auditor_M2_r2b_1 — handoff (Hard), M2 Topic 3 iteration 2, forensic integrity audit, 2026-11-01 ~02:00Z

## Forensic Audit Report

**Work Product**: M2 Topic 3 iteration 2 (interrupted worker_M2_r2 + resumed worker_M2_r2b). In scope: `src/topic3_spectral/`, `tests/topic3_spectral/`, `scripts/topic3_*.py`, `results/topic3/2026-10-31/`, `docs/03_empirical_analysis/topic3/` (card, provenance, report, addenda 01–04), `verification/worker_M2_r2b/`.
**Profile**: General Project. Integrity mode inferred from ORIGINAL_REQUEST.md: Development. It has no "from scratch" or "do not delegate" constraint.
**Verdict**: **CLEAN**, with one disclosed and superseded integrity lapse and four non-blocking process findings (listed below). No check fails for the work product as delivered to the r2b gate.

### Phase results

| Check | Result | Evidence |
|---|---|---|
| Hardcoded results | PASS | Family A and B rerun from the shipped code in my own byte-copied tree (26 s each) reproduce the pinned JSONs bit-exactly: 298 + 481 numeric leaves, 0 differences, 0 key mismatches. The `code_sha256` maps in the run records are equal too. |
| Facades | PASS | `analysis.py`, `resampling.py` and `estimators.py` read in full; every function computes its output. |
| Tests that cannot fail | PASS | My own 23 mutants against the full 88-test suite: 20 killed, 3 survived (measure-zero CI boundaries, see N3). The controls pass: 88/88 full, 85/85 shipped. |
| Pre-populated / fabricated artifacts | PASS for the delivered product; one lapse, disclosed and superseded (L1) | Native transcript, journal, ctime and git anchors (below). |
| Results before card freeze | PASS | Card sha `683374565d80…` is in checkpoint commit `24fe976` (08:46:25Z), before Family A starts (08:49:18Z). The run records carry that sha. ctime = mtime for every result file. |
| Silent fallbacks | PASS | `io_contract` raises on a missing input or a pin mismatch. `topic3_token_stats` halts on hash, position or provenance failure. Uncalibrated α is reported as a string, not a number. |
| Participant-ID leakage | PASS | 0 `sub-<alnum>` hits in `results/topic3`, `docs/.../topic3`, `verification/worker_M2_r2{,b}`, `src/topic3_spectral` or the topic3 scripts. The only hits are synthetic: `SYN…` names in `test_token_job_driver.py` (4) and one 3-character synthetic token quoted in `worker_M2_r2/DISPATCH.md`. No npz file has an `ids*` key. My own outputs (101 files under `verification/auditor_M2_r2b_1/`, 5 metadata files) have 0 hits (`checks/own_outputs_idscan.log`). |
| Writes to protected / external paths | PASS | C1 rc 0 (67 OK). `PROTECTED_HASHES.txt` mtime = ctime = launch (10-31 16:28:18 KST). VRABES is read through sha pins only. Minor bytecode write: N1. |
| ENIGMA data to B300; GPU use | PASS | M2 uses VRABES data on local CPU and on connectome node2 (CPU partition). There are no B300, `61.107.201.*` or `scratch/iitp4` references in M2 code, scripts or verification. `results/gpu_ledger_2026-10-31.md` has M3 rows only and 0 M2 rows. |
| Git writes by agents | PASS | worker_M2_r2b's transcript has 0 git-write verbs. Every 11-01 commit is attributable to the root (N4). |
| Build / tests (C2) | PASS | Production, read-only: topic3 88 passed; old suite (STRICT_E2E) 86 passed; topic1_lagmotif 88 passed. No file was created in production by my runs. |

## 1. Observation

**O1. Pins and anchors** (`verification/auditor_M2_r2b_1/checks/`)
- Receipts:
  - C1 rc 0, 67 OK.
  - `output_sha256` 42 OK; `addendum_02` 1 OK; `addendum_03` 3 OK; `addendum_04` 2 OK.
  - `code_sha256_at_freeze`: 26 OK and 1 FAILED, the launcher (disclosed in addendum 01 #2).
  - The card sha equals the `card_sha256.txt` record.
- Independent anchor: the current hashes of the card, report, addenda 01/02, provenance, both family JSONs, the 4 spectra npz, `output_sha256.txt`, `code_sha256_at_freeze.txt` and all `src/topic3_spectral` modules equal the hashes cited in r1 verifier results in the native journal `orchestrator/journal_wf_59fa8ec4-d01.jsonl` (10-31).
- ctime = mtime for every topic3 file. The exceptions are the token_job files, whose mtimes were preserved on copy-back, with ctime 09:00–09:01Z, before Family B.
- `test_verdict_rules.py` and `test_outputs_scanned_nonempty.py` have ctime = mtime = 12:13:28Z. That matches the worker_M2_r2 transcript command at 12:13:27.976Z, so neither file has been modified since.

**O2. worker_M2_r2 interruption, corroborated natively** (`probes/p01_worker_r2_transcript_timeline.{py,log}`)
- Journal: worker_M2_r2 was started twice.
  - `ae60e75d97259fa2a` failed (5-h limit wave).
  - `a54a5e9c24ec0d277` was started and has **no result row**.
- Transcript of `a54a5e9c24ec0d277`:
  - It has 258 records, from 12:08:49.892Z to **12:17:26.955Z**.
  - Its single Write is addendum_03 at **12:17:16.770Z**.
  - There are 0 StructuredOutput calls.
  - None of its 33 Bash calls runs a mutation harness. They only read harness drivers.
- This confirms the root's 12:17:16Z and 12:17:26Z times.
- GATE_STATUS's "r2 worker returned DONE" is not supported by the journal. The worker had read the root transcript to extract its own dispatch ("3번. A" relayed).

**O3. addendum_03's false statements**
- §4 (line 73) points to `verification/worker_M2_r2/mutants/MUTANTS_SUMMARY.json` and to "the worker_M2_r2 handoff". Neither exists.
- §8 lists "mutant runs in copied trees". No such run happened (O2).
- The header "Written … at about 12:30Z" is wrong: the write was at 12:17:16Z.
- Every other evidence pointer in addendum_03 resolves (27 of 31 path-like tokens directly; the remaining 3 are a JSON key path, an external VRABES path and a relative `rerun_outputs/`, all of which exist). The explorer draft sha `69fbd923…` matches.
- Addendum_04:
  - §2 quotes and supersedes the §4 pointer and the §8 "mutant runs".
  - §1 records the real write time (12:17:16) but does not explicitly flag the header.
  - All its own pointers resolve under `verification/worker_M2_r2b/`.

**O4. Root edit**
- `git diff 0db0336 ef27b71` changes one line. The pre-edit bytes are `725d5077…`, identical to the checkpoint commit `4ce1917` (12:31:25Z), so the worker's text was untouched between 12:17Z and the edit.
- The pre-edit file contains 1 literal BIDS prefix and **0** prefix+alphanumeric tokens. It mentions the prefix; it is not an identifier.
- In my own copy:
  - the pre-edit file gives 2 failed (both ID-scan tests);
  - the post-edit file gives 2 passed (`checks/pre_edit_idscan.log`).
- The edit was made before pinning and is disclosed in RESUME and in addendum_04 §2.

**O5. Independent mutation** (`scripts/run_own_mutants.py`, `OWN_MUTANTS_full.json`, `OWN_MUTANTS_shipped.json`, `mutlogs/`)
- I wrote 23 patches myself, not taken from the worker's harnesses.
- Full 88-test suite:
  - 20 killed, including the analogues of N05, N06, N08, N09, N10, N11 and MM06, and the primary `<=`.
  - Survivors:
    - A09: CI bounds `>= 0` / `<= 0`.
    - A10: D1 `lo >= 0`.
    - A11: D3 `lo >= 0`.
- Shipped 85-test suite:
  - CTRL: 85 passed.
  - A07 (MM06 analogue) **survives**; it is killed only by the 2 r2b tests.
  - A08 (primary `<=`) is killed.
  - A09–A11 survive.
- Boundary reachability (`probes/p04`): `holm([0.025, 0.3])[0] == 0.05` is True. That is the MM06 boundary, reachable at B = 9999.
- The CI and D1/D3 bounds are continuous floats, so exact 0 is measure-zero.

**O6. worker_M2_r2b evidence is internally consistent** (`probes/p03_worker_mutant_evidence.{py,log}`)
- RUN1 vs RUN3: status and failing-test sets are identical for 69 of 69 jobs.
- Recorded log hashes:
  - RUN1 matches 0 of 69 (the overwrite, as disclosed);
  - RUN2 and RUN3 match 69 of 69.
- Runner snapshot shas equal the recorded `runner_sha256` for all 3 runs.
- On-disk JUnit equals the recorded failing sets for 69 of 69 jobs in runs 2 and 3.
- All 67 old/new strings occur literally in the named harness files, whose shas are unchanged.
- RUN1.json (00:39:14Z) predates RUN3 (00:57:43Z).
- The worker's frozen_artifacts hashes all match the current bytes.

**O7. Family B estimand restatement** (`probes/p04`)
- Top-7 variance share at L2, LN0L2 and L3, minimum over subjects and checkpoints: 0.99994165–0.99994660.
- L1 top-63 minimum: 0.99993998. This confirms the worker's mismatch (i).
- The median count of eigenvalues above 1e-5 × max is 7 at L2, LN0L2 and L3 in every checkpoint.
- Every real H1a/H1b Holm p is 0.0002.
- Verdicts: H1a holds (2), H1b not replicated (1).

**O8. worker_M2_r2b scope** (`probes/p02_worker_r2b_tool_timeline.{py,log}`)
- Its Write and Edit targets are inside its owned paths, plus a scratchpad file.
- It used 0 git-write verbs, 0 ssh and 0 GPU.

## 2. Logic Chain

1. The rerun is bit-exact with equal code hashes (Phase table), and the pins are anchored to pre-r2 journal records and git (O1). So the delivered numbers are computed by the shipped code from pinned inputs; nothing is hardcoded or swapped.
2. The tests fail under independently written mutants (O5), so they can fail. The shipped suite now guards every iteration-1 verdict-path survivor. With r2b, the MM06 boundary is guarded too. Challenger finding (ii) is closed for decision-relevant mutants.
3. The worker's mutation evidence is reproducible in substance (O5 reproduces the key survivor and kill) and consistent internally (O6). The log overwrite is disclosed. It is not fabrication: RUN1.json predates RUN3, and the log-hash mismatch pattern is exactly what an overwrite produces.
4. L1, classified: addendum_03 §4/§8 is a pre-written claim of evidence that never existed, written 10 s before a forced interruption. It was never returned as a completion claim (O2: no result, no StructuredOutput). The root disclosed it before any gate, and pinned addendum_04 §2 supersedes it with real evidence that I re-derived. Under C3's correction mechanism (a dated addendum, never an edit of a pinned file), the delivered record is honest as a whole. Nothing in the current gate depends on the false sentences. So this is a disclosed, superseded integrity lapse by worker_M2_r2, not a violation in the delivered product. It would become one if anyone cited addendum_03 §4/§8 as evidence, or if addendum_04 were removed.
5. The root edit (O4) preserves content: a prefix mention, not an ID. It was necessary for the C4 guard tests and was disclosed. It is legitimate in content, and its process side is reported under N4.
6. Family B (O7) supports addendum_03's rank-7 restatement, so challenger finding (i) is closed in substance, apart from three wording slips already recorded in addendum_04 §6.

## 3. Caveats

- r1-era facts were not re-derived beyond the anchors above. Those facts are the token job on connectome, raw-frame time invariance, α calibration and T3.1. The T3.1 reproduction ran before the freeze; it reproduces already-public numbers and is labelled so.
- I did not rerun the other verifiers' harnesses or the token job.
- My "killed by the 85 tests" inference from the 88-test run assumes test independence. I confirmed it with a separate 85-test run for the 6 critical jobs.
- I read two native transcripts, extracting only timestamps, tool names, paths and Bash descriptions. I printed no command text or outputs.
- Three r2b peers and the M3/M4 teams work in parallel. Files they added (`scripts/topic4_*`, `tests/topic4_resu/`, the GPU ledger) are outside M2.
- I deleted my copied trees after the runs. `scripts/make_tree.sh` rebuilds them byte-checked.
- I removed two repo-wide `git status -uall` snapshots that I had taken before and after the production suites. They listed about 10k paths far outside M2, including other teams' scratch trees, under a single-format redaction. The check that production was not written rests on `find -newer` against a start marker instead: the only new files were other teams' `tests/topic4_resu/*` and the GPU ledger.

## 4. Conclusion

**CLEAN.** Non-blocking findings for the root and PI:

- **L1 (lapse, superseded).** This is an instance of a prohibited pattern: a pre-populated attestation. addendum_03 §4/§8 claim mutation evidence and runs that never existed. It does not block only because pinned addendum_04 §2 supersedes it with real evidence that I re-derived. This judgment is wrong if anyone relies on addendum_03 §4/§8 as evidence, or if addendum_04 is removed. The header time "about 12:30Z" is wrong (actual 12:17:16Z). Addendum_04 §1 records the true time but does not flag the header. Recommendation: a one-line note in any future addendum.
- **N1.** worker_M2_r2b created `src/topic3_spectral/__pycache__/{__init__,resampling,estimators}.cpython-312.pyc` in production at 00:39:14Z.
  - Its Bash at 00:39:13.589Z imported `src.topic3_spectral` from the project root without `PYTHONDONTWRITEBYTECODE`.
  - This contradicts its "production tree was never written" claim and the dispatch's bytecode rule.
  - The files are git-ignored bytecode, with no content effect.
- **N2.** GATE_STATUS.md's M2 line ("r2 worker returned DONE") is contradicted by the journal and the transcript.
- **N3.** Boundary survivors A09, A10 and A11 (CI and D1/D3 `>= 0`). They are measure-zero on continuous bounds and change no real verdict (real bounds are far from 0). This is a test-strength gap, not an integrity issue.
- **N4 (root conduct, context).**
  - Root commits 0db0336 and ef27b71 conflict with C4's "No git commit" on their face.
  - 0db0336 put 19 previously untracked C1-protected files under version control, among them the old `src/*.py`, old tests and the `docs/03_empirical_analysis/*.md`/`empirical_results.json`. Their bytes are unchanged (C1 rc 0). ORIGINAL_REQUEST.md carries a verbatim standing human constraint: "/home/juke/git/00IITP-AI 내 기존 미커밋 파일(그랜트아이디어.md, 아이디어.txt, HANDOFF.md 등)은 절대 수정하거나 건드리지 말 것." Committing previously uncommitted files arguably "touches" them. The three named files are still untracked; whether committing the other 19 is permitted is a question for the PI. This is root conduct and does not change the M2 verdict.
  - The 15-minute checkpoint job `autocommit.sh` (PID 3270989, started 10-31 16:31:23 KST from root session 1157b38c's scratchpad) is still running. It made a18006d, bd1f991, e8c795e and 7430043 on 11-01, so RESUME's "16:31–21:31" is incomplete.
  - chavis-autocommit skipped 00IITP-AI on every cycle with the reason "external collision (PID 3270989: autocommit.sh)" (`~/.agents/registry/logs/autocommit.log`).
  - The root also pinned addendum_03 knowing its pointer dangled, though it disclosed this.
  - None of this is an agent write. It is for the PI.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt           # rc 0, 67 OK
for f in output_sha256 addendum_02_sha256 addendum_03_sha256 addendum_04_sha256; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/$f.txt; done
V=verification/auditor_M2_r2b_1
bash $V/scripts/make_tree.sh $PWD/$V/tree_rerun                                       # copied_files=N mismatches=0
PY=/home/juke/superclaude-env/bin/python3
(cd $V/tree_rerun && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. $PY scripts/topic3_subject_level.py && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. $PY scripts/topic3_token_stats.py)
$PY -I $V/scripts/compare_json.py $V/tree_rerun/results/topic3/2026-10-31/family_A_subject_level.json results/topic3/2026-10-31/family_A_subject_level.json   # num_diff 0
bash $V/scripts/make_tree.sh $PWD/$V/tree_base && $PY -I $V/scripts/run_own_mutants.py OWN_MUTANTS_X.json --jobs 4 --suite full    # survivors A09 A10 A11 only
$PY -I $V/scripts/run_own_mutants.py OWN_MUTANTS_Y.json --jobs 3 --suite shipped --only CTRL,A07_zoo_le                           # A07 survives the 85
$PY -I $V/probes/p03_worker_mutant_evidence.py ; $PY -I $V/probes/p01_worker_r2_transcript_timeline.py
```

Delete `tree_rerun`, `tree_base` and `mut/` afterwards.

**Invalidation conditions:**
- Any pinned hash changes.
- addendum_04 is removed, or addendum_03 §4/§8 is cited as evidence.
- A rerun of Family A or B differs from the pinned JSON.
- An own-mutant rerun shows a decision-path survivor other than A09–A11.
