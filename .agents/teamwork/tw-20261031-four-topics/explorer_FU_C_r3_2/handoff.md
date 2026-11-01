# Handoff (Hard) — explorer_FU_C_r3_2, FU_C iteration 3, lens: feasibility and failure modes

**Summary.** The single r2 blocking item, the recoverable peer near-copy, was contained by root at about 2026-11-01T21:43Z, while this exploration was running. My count-only sweep afterwards finds 0 near-copies and 0 named copies of the retired file, so B1 is closed in the working tree. No science, receipt or code change is needed for it.

Iteration 3 is the last one (workflow_C_script.js.txt line 10, `MAX_ITER = 3`). What remains is to make the r3 gate robust:
- record the containment;
- close the r2-surface behavioural gaps that a fresh r3 challenger could escalate;
- avoid the concrete self-inflicted failure modes listed in §2.

All of this is additive. No file pinned by output_sha256_r2.txt changes, and 0 GPU-h are needed.

## 1. Observation

All checks are count-only. No literal, derived counter or old-file sha prefix was printed or written.

| # | Observation | Evidence |
|---|---|---|
| O1 | At 21:40Z, `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` existed: overlap 0.993 of the 135 long lines, equal size, the differing bytes inside one 6-byte window, recoverable = true (boolean). | probes/p1.out.json |
| O2 | At 21:44Z, `verification/explorer_FU_C_r2_2/` holds only 7 small probe files; tree/, mut_work/ and code_receipt_subset_derived.view are gone. A new sealed dir `~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02/` (0700, mtime 06:43 KST) holds MANIFEST.sha256 plus a verification/ subtree. Inside it, files are 0664 and subdirs 0775; the parent 0700 still blocks other users. GATE_STATUS.md has no entry for this action yet. | ls -la outputs |
| O3 | Post-containment sweep over 22,600 working-tree files: near_copies [], named_copies []. The literal occurs only in 1 file, as the integer part of a float (the known Topic-1 extract_primary.jsonl coincidence). | probes/p1_after_containment.out.json |
| O4 | Counter-encoding check (literal ± 1, ± 99,999, ± 100,000 as maximal digit runs) in FU_C verification and metadata dirs: 1 remaining hit, in verification/auditor_FU_C_r1_1/repo_runs.sha, inside a hex run (a sha digest coincidence). The 4 pre-containment hits were 3 hex-run coincidences and 1 in the now-sealed tree. | p1/p2 out.json |
| O5 | git log -p --all since 2026-11-01 (83 commits, 5.3 MB of patches): 0 maximal-run occurrences of the literal. | probes/p2.out.json |
| O6 | No repo file and no git patch since 10-31 contains a sha256, sha1 or md5 digest (full, or its 16-hex prefix) of the literal-bearing line; checked with and without newline and stripped. Matches for other lines are generic-line digests in run.json and receipt files and are irrelevant. | probes/p4.out.json (files_with_literal_line_digest 0) |
| O7 | Baseline now: C1 rc 0; `tests/topic2_fu_c` 180 passed (1.4 s); `scripts/topic2fu_c_check_receipts_r2.py` ok true (card 36/0, code 15/2, presentation 1/0, output 160/3, output_sha256_r2 27/0). | commands in §5 |
| O8 | Worker ownership for r3 = fuOwn('c') (script line 48): src/topic2_fu_c, tests/topic2_fu_c, scripts/topic2fu_c_*.py, results/topic2/2026-11-02_fu_c, docs/.../2026-11-02_topic2_fu_c_*.md, B300 /scratch/iitp4/fu_c, plus ledger rows. It does not include other agents' verification dirs or the sealed store. | workflow_C_script.js.txt:48 |
| O9 | `supersession.check_receipts` globs `results/topic2/2026-11-02_fu_c/*sha256*.txt`. Every receipt not in SUPERSEDED must verify completely; off-repo receipts are skipped by name (c4_sealed_originals_sha256.txt). | src/topic2_fu_c/supersession.py:65-86 |
| O10 | c4scan SCOPES include `verification/worker_FU_C_r*`, so the r3 worker's own verification dir is scanned by the shipped r2 test `test_no_identifier_shaped_token_in_any_fu_c_path`. SIX = `(?<![0-9.])[1-9][0-9]{5}(?![0-9])`, and the allowlist is exact (path, token). | src/topic2_fu_c/c4scan.py:21-26; tests/topic2_fu_c/test_c4_and_guards_r2.py:36-49 |
| O11 | The r2 mutation harness mirror copies src/topic2_rgpool, src/topic2_fu_c and tests/topic2_fu_c, and symlinks results/, docs/ and scripts/ to the real repo. | verification/worker_FU_C_r2/mutants/run_mutants_r2.py:54-61 |
| O12 | Driver refusal is `os.path.realpath(a.out) == os.path.realpath(shipped)` followed by sys.exit. The shipped verdict.json is chmod a-w. | scripts/topic2fu_c_verdict_r2.py:25-27 |
| O13 | r2 challenger behavioural survivors on the r2 surfaces, nonblocking in r2. challenger_FU_C_r2_1: SS02, SS03, SS04, SS05, SS07, SS12, DR01, DR02, CK01, C401, C402, C404, C405, C409, C413. challenger_FU_C_r2_2: S01, S02, S03, S07, S08, S11, C02, C03, C08, D01, D02 (C10 equivalent). The tables are loadable from their harness sources. | verification/challenger_FU_C_r2_1/mutants_r2_surfaces.out.json; verification/challenger_FU_C_r2_2/out/r2code_mutants_behavioural.out.json |
| O14 | B300 membership of every maximal 6-digit run in my own files: 0 hits; controls valid (positive 1, negative 0); 3 ssh calls took 46 s. | probes/p3.out.json |

## 2. Logic Chain

1. B1 in r2 needed both a near-copy and the immutable old pin (O1). The near-copy is now sealed off-repo (O2). With no other near-copy (O3), no line-level digest (O6) and no git occurrence (O5), no repo content recovers the literal. The receipts may keep the old pin unchanged.
2. B1 was outside worker ownership (O8), and root has already acted. So the r3 worker has nothing to delete. It must verify and record, and it must not copy anything back from the sealed dir.
3. All 5 r2 verifiers said they would approve once the near-copy was removed, with no worker change. But r3 uses 5 fresh verifiers on the final iteration, and the challenger instruction requires "mutation tests that each fixture/verdict rule must catch". The 26 behavioural survivors (O13) are the most likely re-block. Closing them is cheap, additive and synthetic.
4. Any edit to an r2-pinned file (supersession.py, c4scan.py, r2 tests, driver, checker, addendum 02, the result report) breaks output_sha256_r2.txt. check_receipts then fails (O9), which forces a new supersession declaration and so another edit of supersession.py. Everything in r3 must therefore be additive, with a new fully verifying output_sha256_r3.txt. The globbing check accepts it with no code change (O9).
5. Self-inflicted failure modes:
   - (a) Any 6-digit run in verification/worker_FU_C_r3 turns the shipped C4 test red (O10). This includes brute-force bounds such as 10^5 written in digits, counts like 900k, byte sizes and timings.
   - (b) A driver or receipt test that passes real results/ paths runs, inside a mutation mirror, against the real repo through the symlinks (O11). A DR01-type mutant would then try to write the real verdict.json. Only chmod a-w stops it, and the resulting PermissionError makes the mutant look killed for the wrong reason (O12).
   - (c) Hash- or real-data-dependent new tests that are not deselected in the r3 harness inflate kills. This is the stale --deselect class.
   - (d) Mutating scripts/ through the symlinked mirror mutates the production file. Scripts must be copied, not symlinked, when they are mutation targets; challenger_FU_C_r2_1 did this (mutants_r2_surfaces.py:80-93).
6. Some of the c4scan survivors are real blind spots, not test gaps: C409/C02 ('.'-preceded IDs, hex-adjacent IDs). A test that asserts flagging there fails on the shipped c4scan. Fixing c4scan.py breaks the r2 pin (step 4). The feasible path is a new strict scanner module plus the maximal-digit-run B300 membership check as the catch-all, with the c4scan.py limits documented.

## 3. Caveats

- I did not see root's own record of the containment. I infer root from the sealed path and mtime: the sealed store is root-held, and the r2 verifiers all said "root or owner". I did not read the sealed MANIFEST or the files inside it.
- I did not read the other r3 explorers' or the M3 r3 team's outputs (worked independently).
- Membership was checked only against the 1,084 staged HCP names, and only for my own files. The r2 verifiers' broad scans (0 hits) are their claims, which I did not re-run.
- Agent transcripts and B300 /scratch/iitp4 were not re-scanned. r2 verifiers reported 0 copies on B300.
- The survivor lists in O13 come from the challengers' out.json files. I did not rerun those harnesses.
- p4's "any line digest" list is dominated by generic-line digests, for example of an empty line. Only the literal-line count (0) matters.

## 4. Conclusion (recommendation for worker_FU_C_r3)

Fixed scope, additive only, 0 GPU-h, about 1 h CPU.

- **R0, root, outside the worker.**
  - Append to GATE_STATUS.md the containment record: what moved, from where to where, when, and the manifest sha. Verifiers need an authoritative line.
  - chmod the new sealed subtree to files 0400 and dirs 0700, to match the fu_c_c4 convention that the r2 auditors checked.
- **R1, verify containment, count-only.**
  - Rerun a near-copy and named-copy sweep against the sealed original, read in memory.
  - Record: near_copies [], named_copies [], literal only as the Topic-1 float, git 0, line-digest 0.
  - Never copy, mirror or diff the sealed near-copy.
- **R2, no edit to r2-pinned files.**
  - New files only:
    - tests/topic2_fu_c/test_r3_surfaces.py
    - src/topic2_fu_c/c4scan_strict.py (optional)
    - scripts/topic2fu_c_c4_sweep_r3.py
    - docs/.../2026-11-02_topic2_fu_c_addendum_03.md
    - results/.../output_sha256_r3.txt (post-result, non-governing, all lines verify)
  - check_receipts_r2 must stay ok, with output_sha256_r2 27/0 and output_sha256_r3 n/0.
- **R3, behavioural tests on synthetic roots** (tmp_path; never the real results/ paths):
  - check_receipts: equality, not subset; MISSING ≠ OK; undeclared receipts must fully verify; a missing declared receipt → not ok; the off-repo skip list; the checker exit code. Kills SS02/03/04/05/12, CK01, S01/02/03/08/11.
  - reproduce_verdict fail-closed: inject a context problem through monkeypatched RC.build_context; the result must be no_verdict and the problems kept. Kills SS07/S07.
  - driver: load the script via importlib, set module ROOT to a tmp root holding a fake verdict.json, monkeypatch SS.reproduce_verdict. Cases:
    - --out equal to the fake shipped path → SystemExit "refusing", fake file unchanged;
    - identical canned text → exit 0, byte_identical true;
    - different text → exit 1, byte_identical false.
    Kills DR01/DR02, D01/D02.
  - c4scan controls built at run time: a leading-'1' 6-digit, an alphanumeric 'sub-' label, the '.'-fraction negative, the hex-mask threshold, and SCOPES entries asserted. Kills C401/402/404/405/413, C03, C08.
  - The real blind spots (C409/C02: `run.<ID>_3T`, `fe<ID>`) go to a strict r3 scanner, tested positive and negative. Document that c4scan.py itself keeps those limits.
- **R4, mutation evidence.**
  - verification/worker_FU_C_r3/mutants/run_mutants_r3.py loads the r2 union table plus both r2 challenger surface tables.
  - The mirror copies any scripts/ that are mutation targets.
  - DESELECT is the 5 r2 hash tests plus every new real-data/hash test, count-checked against the baseline.
  - Run detached (≈ 10–15 min at 2 jobs), with a progress log.
  - Required: 0 invalid; survivors ⊆ {baseline, V07c, V12, F11, C10, plus any proven equivalent}.
- **R5, C4 hygiene for all r3 outputs.**
  - No raw 6-digit runs anywhere in verification/worker_FU_C_r3 or the r3 docs; write bounds as 10**5 and keep counts below 6 digits or as words.
  - Run the shipped C4 test after each write.
  - Final B300 membership pass over every r3 file plus metadata, via ssh stdin, count-only.
- **R6, addendum 03.**
  - Records the containment (by root; time; sealed path; no sha prefix of the old file), the sweep results, the r3 tests, the mutation results, the unchanged receipt state and the new receipt.
  - No number, verdict or reading changes.
  - Do not edit the result report; addendum 02 §7 already names the residual, and addendum 03 closes it.
- **R7, rerun.**
  - FU-C suite, old 86, topic2_rgpool, topic1_lagmotif, C1, check_receipts_r2, verdict_r2 --out (byte-identical), whole-run audit_layout.
  - Give the frozen CLI an explicit --out only.

## 5. Verification Method

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 -I \
  verification/explorer_FU_C_r3_2/probes/p1_footprint_nearcopy.py $PWD \
  ~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/test_gate_and_records.py /tmp/p1.json
# expect near_copies [] and named_copies []; literal_files 1 with literal_all_float_intpart [true]
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. timeout 900 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q   # 180 passed
PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_check_receipts_r2.py   # ok true
ls verification/explorer_FU_C_r2_2/   # no tree/, mut_work/, code_receipt_subset_derived.view
```

Invalidation conditions:
- any near-copy, or any file named test_gate_and_records*, reappears under verification/ or .agents/;
- any r2-pinned file changes;
- check_receipts_r2 is not ok;
- the FU-C suite is not green.
