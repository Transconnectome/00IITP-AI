# Handoff — explorer_FU_C_r3_3 (FU_C iteration 3, explorer 3 of 3, lens: adversarial pre-mortem) — Hard handoff

**Summary.** The single r2 blocking item has been closed by root: the peer near-copy was moved to the sealed store at 21:43Z. My count-only rescan afterwards finds 0 near-copies in the working tree (raw or JSON-escaped) and 0 in git blobs. Iteration 3 is the LAST FU_C iteration (workflow C `MAX_ITER = 3`), and the gate still needs all 5 fresh verifiers to pass. So the main risk is no longer the r2 defect. It is that the r3 worker adds new attack surface, or breaks a pinned r2 artifact, while doing extra work. My recommendation is a minimal, fixed-scope r3: no edits to any r2-pinned file, behaviour-only additive tests, one new addendum and one new receipt, and 0 GPU-h.

## 1. Observation

| # | Observation | Evidence |
|---|---|---|
| O1 | workflow C sets `MAX_ITER = 3`. If an iteration's gate fails, the milestone ends INCOMPLETE and a PI decision is needed. The gate requires worker DONE, both reviewers APPROVE, both challengers CONFIRMED and the auditor CLEAN. Verifiers receive only the worker's handoff, not the r2 gate record. | `orchestrator/workflow_C_script.js.txt` lines 10, 71–115 |
| O2 | ACCEPTANCE gained a root addendum, "FU_C r2 near-copy containment". It records the move of `verification/explorer_FU_C_r2_2/{tree,mut_work,code_receipt_subset_derived.view}` and of the auditor's offset output to `~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02/` (MANIFEST.sha256, 302 lines). It also sets new writing rules: summarise the gate record, never write offsets, digit shape or shape-tied counts. | `sentinel/ACCEPTANCE.md` tail; `ls` at 21:45Z |
| O3 | Sealed store: `sha256sum -c MANIFEST.sha256` gives 0 failures. The top directory is 0700, but the moved files inside are not 0400 (302 of 302) and 87 subdirectories are not 0700. The precedent stores (fu_c_c4, dev-salt) use 0400/0700. Effective protection holds, because the parent is 0700. | p-checks 21:47Z |
| O4 | Footprint probe before the move: exactly 1 near-copy at 99.3 % long-line overlap (the known peer file). After the move: 22,731 worktree files gave 0 near-copies at ≥10 % overlap, raw or JSON-escaped. 2,125 git blobs gave 0 near-copies, 0 standalone literal and 0 literal-derived tokens (L, L±1, L−10^5, L−10^5+1, the counter forms the r2 self-incidents used). The only worktree hits for derived tokens are 3 copies of the Topic-1 `extract_primary.jsonl` float coincidence that is already known. No `*gate_and_records*` file (incl. `.pyc`) exists anywhere in the repo. | `verification/explorer_FU_C_r3_3/probes/p1_footprint*.out.json`; `find` |
| O5 | C1: rc 0 (67 lines). `tests/topic2_fu_c`: 180 passed. `scripts/topic2fu_c_check_receipts_r2.py`: `"ok": true`, still true after the root move, because no FU-C receipt pins a file under `verification/explorer_FU_C_r2_2`. | commands in §5 |
| O6 | `supersession.check_receipts` globs every `*sha256*.txt` in `results/topic2/2026-11-02_fu_c/`. Any failing line that is not declared in the hard-coded `SUPERSEDED` dict sets `ok = False`. `output_sha256_r2.txt` pins 27 r2 files: supersession.py, c4scan.py, the r2 tests, addendum_02, the result report and others. `test_every_fu_c_receipt_fails_on_exactly_the_declared_superseded_lines` asserts `ok` and that `output_sha256_r2.txt` has 0 failures. | `src/topic2_fu_c/supersession.py`; `tests/topic2_fu_c/test_supersession_r2.py` |
| O7 | `c4scan.SCOPES` includes `verification/worker_FU_C_r*` and `docs/.../2026-11-02_topic2_fu_c_*.md`. Its rules: SIX `(?<![0-9.])[1-9][0-9]{5}(?![0-9])`; SUB `sub-[A-Za-z]*[0-9]`, which also flags ordinary words such as "sub" + "-r3"-style words; HEX16 for a standalone 16-hex token, which also flags a 16-character sha prefix. The scan runs inside the FU-C suite. | `src/topic2_fu_c/c4scan.py` |
| O8 | `budget.FU_C_AGENTS` lists only r1 agents. FU-C ledger use is 10.697 GPU-h (r2 verifier sums), so 2.303 GPU-h of the 13 GPU-h cap remain. | `src/topic2_fu_c/budget.py:16`; r2 reviewer_2 ledger parse |
| O9 | Git anchor for the freeze order. Daemon commit e5fa8de, committed 2026-11-01T16:20:26Z, contains a worker_FU_C_r1 progress line: "16:13:23Z CARD FROZEN … sha fc2d0672…". That commit time is before the first Stage-1 start (16:35:12Z). Commit cd1e43e (16:35:27Z) contains the line "16:31:53Z verdict code + tests pinned … No Stage-1 job had started", which predates the first Stage-1 end (17:01Z). The full verdict.py sha first appears in git at 20:05Z, after results. | `git log -S`, `git show` |
| O10 | Committed handoffs from r2 (explorer_FU_C_r2_1/_2/_3, auditor_FU_C_r2_1) point to the literal as "the integer part of a float in the Topic-1 extract_primary.jsonl". That file is untracked. My p2 confirms that the literal is among its 6-digit integer parts (boolean only). This is a weak narrowing pointer and cannot be removed from history (no git writes). Several committed .md files also describe the subject as HCP's public documentation example. | p2; `git log` of those handoffs |

## 2. Logic Chain

1. **The r2 defect is closed, but only by root.** By O2 and O4, the one blocking item that all 5 r2 verifiers raised is gone, and nothing else in the repo or in git re-creates it. Every r2 verifier said they would approve once it was removed, with no worker change.
2. **The r3 verifiers are fresh, so the threat model changes.** By O1, they see only the r3 worker's handoff and audit the whole milestone again. r3 therefore fails only if (a) a fresh verifier escalates an r2 nonblocking item, (b) the r3 worker regresses something, or (c) a new C4 exposure appears.
3. **Regression trap (b).** By O6, editing any r2-pinned file makes `output_sha256_r2.txt` fail on an undeclared line. Then `check_receipts` returns ok False and the r2 test goes red. "Fixing" that means editing the pinned supersession.py, which cascades. So r3 must not touch the result report, addendum_02, supersession.py, c4scan.py, the r2 driver or checker, or any r2 test. New work goes only in new files, pinned by a new `output_sha256_r3.txt`. `check_receipts` picks that file up automatically and requires it to verify fully.
4. **Tripwire trap (b and c).** By O7, any r3 evidence under `verification/worker_FU_C_r3/` or a new FU-C doc is scanned by the suite. A 6-digit count such as 900,000 written without separators, a 16-hex sha prefix, or a "sub" + "-r3"-style word turns the suite red. The worker must use full 64-hex shas or ≤8-hex prefixes, digit separators, and no "sub-<letters><digit>" words, and must run the FU-C suite last, after all evidence is written.
5. **Escalation risk (a).**
   - The most attackable r2 nonblocking items lie on the canonical reproduction path, which became canonical in r2 once the frozen CLI returned no_verdict by design:
     - `reproduce_verdict` clearing ctx problems (S07) survives behaviourally;
     - the r2 driver's identity check and its refusal to overwrite (DR01/DR02, D01/D02) are untested;
     - `check_receipts` subset-vs-equality checks (SS02–SS05, SS12, CK01, S01–S03, S08, S11) are untested.
   - C413 also matters for C4: a SIX rule of `[2-9]` would miss every ID starting with 1, which is the most common HCP-YA leading digit, and the only 6-digit positive control is the all-nines token.
   - A fresh challenger can reasonably call any of these "the guard cannot fail".
   - Additive tests that are behaviour-only (synthetic tmp roots, no real-receipt hashes) and that PASS on the shipped code kill these mutants without touching pinned files. Tests that would FAIL on shipped code (the c4scan blind spots `.`+ID and the 8+ hex-run masking) must not be "fixed" in pinned c4scan.py. They are documented as known limitations, covered by the broad count-only membership checks.
6. **Mutation-evidence trap.** The union harness collects every test in `tests/topic2_fu_c`. New tests must not read real receipts or pinned hashes; otherwise mutants get "killed" by hash mismatch, which is inflation. The worker reruns the harness and shows that the deselected count is unchanged (5) and that the r2 table plus any new kills come from behaviour.
7. **C4 residuals that a fresh auditor may raise (c).**
   - By O10, committed text already narrows the literal weakly. That cannot be undone without git writes and is low severity, because the subject is public.
   - The rule therefore has to be: r3 adds no further pointer. No offsets, shape, candidate counts, timings of an early-stopping brute force, or loop counters. By O4, the r2 self-incidents left nothing in repo or git.
   - Recoverability probes must scan the full space, print booleans only, and never print elapsed time or a match index.
   - The sealed store modes (O3) are a cosmetic finding that root can fix with chmod.
8. **Freeze-order attack.** By O9, a fresh auditor's "no git anchor" claim is rebutted for the card: a commit before any run start carries its sha prefix. Code-freeze evidence rests on a committed progress claim (16:35:27Z, before any run ended), plus the receipt and mtimes. The worker should cite O9 in addendum_03 rather than leave "no git anchor" standing.
9. **GPU.** By O8, nothing needs GPU. Any r3 GPU use would also be invisible to budget.py, so r3 must use 0 GPU-h.

## 3. Caveats

- I did not read the other r3 explorers' reports, to stay independent. I saw only that root acted after explorer_FU_C_r3_1's report.
- I did not rerun the union mutation harness or the r2 challengers' surface-mutant harnesses. The kill and survivor claims in §2.5 come from the r2 challenger reports.
- I made no B300 membership check: my files contain 0 tokens of the shape [1-9]\d{5}, so there was nothing to send.
- Near-copy detection uses long-line overlap (≥40 chars, ≥10 %). A heavily re-formatted copy (for example re-indented or base64) would escape it. Agent transcripts and off-repo locations (`/tmp`, `~/.claude/projects`) are out of repo scope.
- The pointer analysis in O10 is qualitative on purpose. I wrote no candidate counts.
- Whether the committed "public example subject" wording is acceptable under C4 is a root or PI judgement.

## 4. Conclusion

1. **S0, root, done.** Near-copy contained (21:43Z). Optional: `chmod -R a-w,go-rwx` on the new sealed store to match the 0400/0700 precedent, and record that in GATE_STATUS.
2. **Worker r3 scope (fixed).**
   - **Do not edit:**
     - any file pinned by `output_sha256_r2.txt`, `code_sha256_before_results.txt`, `card_sha256.txt` or `output_sha256.txt`;
     - the result report, addendum_02, src/topic2_fu_c/*.py or scripts/topic2fu_c_*.py;
     - any peer folder.
   - **Add:**
     - (a) `tests/topic2_fu_c/test_r3_guards.py`: behaviour-only tests on synthetic tmp roots. They kill S07 (reproduce_verdict must return non-empty problems and a no_verdict result when a pinned verdict-path file is altered in a tmp copy), the check_receipts equality/MISSING/undeclared-receipt mutants, DR01/DR02 (drive `scripts/topic2fu_c_verdict_r2.py` with a tmp `--out` and with the shipped path; it must refuse), and C413/C401/C402/C404/C409. For the last group, use positive controls built at run time for every leading digit 1–9 (`str(d) + "0"*5`), a letter-led `sub-` label and the `.` lookbehind, plus scope-membership asserts. Each test must pass on the shipped code.
     - (b) `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_addendum_03.md`. It records: the r2 residual §7 item 1 closed by root containment (path class, time, sealed store, manifest line count; no offsets or shape); O9 as the freeze anchor; the c4scan blind spots as documented limitations; and the dispositions of the r2 nonblocking items. No 6-digit token, no 16-hex token, no "sub-<letters><digit>" word.
     - (c) `results/topic2/2026-11-02_fu_c/output_sha256_r3.txt`, pinning (a) and (b) and the r3 evidence files, with a real r3 frozen_utc.
   - **Evidence goes in** `verification/worker_FU_C_r3/`.
3. **Return DONE only if all of the following hold:**
   - the post-move near-copy rescan is 0 (rerun my p1 or the r2 reviewers' sweeps);
   - suites are green: FU-C ≥180 plus new, old 86, topic2_rgpool 116, topic1_lagmotif 88;
   - C1 rc 0;
   - check_receipts ok, with r3 pins 0 failing;
   - the r2 driver reproduces the verdict byte-identically;
   - the union harness reruns with the unchanged deselect count;
   - the c4scan test passes over the r3 evidence;
   - 0 GPU-h.
   The verdict stays `stop`; no number changes.

## 5. Verification Method

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. timeout 900 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q   # 180 passed (r2 state)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_check_receipts_r2.py   # "ok": true
PYTHONDONTWRITEBYTECODE=1 timeout 900 nice /home/juke/superclaude-env/bin/python3 -I verification/explorer_FU_C_r3_3/probes/p1_footprint.py "$PWD" ~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/test_gate_and_records.py   # near_copies_ge_10pct [] ; git_* 0
find . -path ./.git -prune -o -iname '*gate_and_records*' -print   # empty
git log --all --reverse --format='%h %cI' -S'fc2d0672' | head -1   # e5fa8de 2026-11-02T01:20:26+09:00
(cd ~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02 && LC_ALL=C sha256sum -c MANIFEST.sha256 | grep -vc ': OK$')   # 0
```

This handoff is invalidated if any of the following holds:
- a near-copy is re-created, for example by a mirror built from the sealed original;
- any r2-pinned file changes;
- the suite or `check_receipts` goes red;
- a new `*gate_and_records*` file appears.
