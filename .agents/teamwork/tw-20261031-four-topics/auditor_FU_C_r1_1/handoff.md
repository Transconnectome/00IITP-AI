# Hard handoff — auditor_FU_C_r1_1 (forensic integrity audit, milestone FU_C)

Written 2026-11-01T20:05Z.
- Host: claude-code; no native spawning.
- Integrity mode: Development. Inferred from ORIGINAL_REQUEST.md, which has no "from scratch" or "must not delegate" constraint.
- Profile: General Project.

## Forensic Audit Report

**Work Product**: FU-C (Topic 2 follow-up C). It comprises:
- `src/topic2_fu_c/`, `tests/topic2_fu_c/`, `scripts/topic2fu_c_*.py`
- `results/topic2/2026-11-02_fu_c/`
- the card, addendum 01 and result report in `docs/03_empirical_analysis/topic2/`
- B300 `/scratch/iitp4/fu_c/`
- the worker_FU_C_r1 ledger rows

**Profile**: General Project (Development mode)

**Verdict**: INTEGRITY VIOLATION. It is narrow: one C4 breach. Every scientific, provenance and compute check is clean.

### Phase Results
- **C1 protected hashes: PASS.** `PROTECTED_HASHES.txt` gives rc 0 with 0 failures (67 lines), checked both before and after my test runs.
- **FU-C receipts: PASS.** card (36 lines), code (15), presentation (1) and output (160) all give rc 0 with 0 non-OK lines.
- **Freeze order: PASS.**
  - Receipt mtimes: card 16:13:23Z, code 16:31:53Z, presentation 16:36:10Z.
  - Git snapshots of worker progress.md (e5fa8de 16:20Z, cd1e43e 16:35Z, 4578b81 16:50Z) record the freeze before any run started.
  - sacct: the first Stage-1 start is 16:35:09Z (job 512).
  - All 24 run.json `start_utc` values are later than 16:13:23Z.
  - B300 has no run file older than the first start.
- **Results before freeze: PASS.**
  - The explorers touched only r1 seeds 0 and 5 and built partitions for S seeds 10..17 (no outcomes).
  - Anchor job 501: `has_test_outcome` and `has_val_outcome` are false, and it used r1 seeds only.
  - Seeds 10..17 were never trained before the freeze.
- **Hardcoded results / facades: PASS.** `verdict.py`, `receipts.py` and the CLI contain no result literals. The verdict is computed from `run.json` through the frozen `stats`.
- **Independent recompute: PASS.** My own script (`verification/auditor_FU_C_r1_1/recompute_verdict.py`, scipy t, df 7, using the card's perm table rather than the worker code) gives:
  - I1 −0.1132 % [−0.4985 %, +0.2721 %]
  - I2 +0.0083 % [−0.5200 %, +0.5366 %]
  - verdict stop
  - drop-stall I1 +0.0400 % [−0.2126 %, +0.2925 %]
  - F+ +3.061 % / +2.935 %; F− −1.737 %
  - stalled runs C s16 and S s15; the escape steps equal the report.
  - All 24 records pass the provenance checks: settings, perm key/sha/file, split, h-tokens, test order, Σnum/Σden, start after freeze, and code vs the r1 pins (13/13).
- **CLI recompute: PASS.** `scripts/topic2fu_c_verdict.py --out verification/auditor_FU_C_r1_1/verdict_recomputed.json` is identical, leaf by leaf, to the shipped `verdict.json` (bootstrap included).
- **Records authentic: PASS.**
  - The 48 run.json and train_log.jsonl files in the repo are byte-identical to the B300 originals.
  - B300 mtimes equal the sacct end times, and each run.json start/end lies inside its sacct window.
  - The 24 sbatch scripts are identical apart from arm and seed. They call the frozen `scripts/topic2_train.py` in `/scratch/iitp4/fu_c/venv`.
  - All 16 B300 training-path files equal `results/topic2/2026-11-01/code_sha256_at_freeze.txt`.
  - B300 npz and split shas equal the pins.
- **Tests: PASS.** All of these run green: tests/topic2_fu_c, the old suite (86), and tests/topic2_rgpool (116, regression). Counts and timing:

  | suite | passed | time |
  |---|---|---|
  | tests/topic2_fu_c | 109 | 1.03 s |
  | old suite | 86 | 33 s |
  | tests/topic2_rgpool | 116 | 54 s |

  - The tests use synthetic planted effects at 6 points and check rule boundaries on both sides.
  - Mutation harness rerun (byte-identical copy, mirror under my verification dir): 51 of 54 mutants killed, 0 invalid. The survivors V07c, V12 and F11 are the same as the worker's. Reading the code confirms they are equivalent.
- **Compute: PASS.**
  - sacct shows 25 FU-C worker jobs (anchor 501 plus 24 Stage-1), all COMPLETED, 1 GPU each, on b300-01.
  - Each job has exactly one started row and one closing row in the ledger. Closing GPU-h = ElapsedRaw/3600 (±0.0015), and the closing start/end equal sacct converted to UTC.
  - Worker total 10.422 GPU-h; explorers 0.14 + 0.072 + 0.05 = 0.262; FU-C total 10.684, within the cap of 13.
  - jobs.json admission `projected_worst` ≤ 13 for every job.
  - No g3t-G-E0-* job exists in sacct since 2026-11-01 12:00 KST.
  - The venv is project-local (`/scratch/iitp4/fu_c/venv`, include-system-site-packages = false).
- **Git writes by agents: PASS.** Since 14:00Z the only commit authors are the Chavis Autocommit daemon (19 commits) and the root checkpoint loop (5 commits, "docs(iitp): checkpoint…"). No FU-C code file is tracked. There are no stashes.
- **Layout: PASS.** `audit_layout.py` on the run root: 551 files, 0 findings, rc 0.
- **C4 participant IDs: FAIL.** Details below.

### C4 finding (the violation)
- `tests/topic2_fu_c/test_gate_and_records.py:182` contains a literal 6-digit string in the parametrize list, with the comment `# HCP-ID shape`.
- It is the well-known HCP-YA example subject, and a count-only check on B300 confirms it is a real participant ID in this run's data. The command printed only counts:
  - it equals one of the 1,084 staged HCP subject directory names: `ls /scratch/data/hcp/download_HCP_REST1_filtered | grep -cx <literal>` → 1;
  - it is not in the 88-subject r1 manifest (count 0).
- In the whole repo it occurs, as a standalone ID-shaped token, only in this file. The only other match is a float in topic1 results.
- The file is pinned in `code_sha256_before_results.txt` and `output_sha256.txt`. It is not tracked by git, so the ID has not entered git history.
- C4 (ACCEPTANCE) says "No participant IDs printed or written". The dispatch says "HCP 6-digit IDs … positional index or HMAC with an off-repo key only".
- The result report §4 states "No participant ID was printed or written", which is false by the letter of C4.
- Why it was missed: the worker's C4 scanners covered only `results/topic2/2026-11-02_fu_c/` (repo test) and the copy-back tree (B300 scan). Neither covered tests/ or src/.
- I do not reproduce the literal in any file I wrote. My probe files contain 0 occurrences.

### Evidence
Raw files are in `/home/juke/git/00IITP-AI/verification/auditor_FU_C_r1_1/`:

| file | content |
|---|---|
| `sacct_fuc.txt` | sacct rows for the FU-C jobs |
| `b300_runs_listing.txt`, `b300.sha`, `repo.sha` | B300 originals vs repo copies (48 identical) |
| `b300_code.txt`, `b300_r1code.sha`, `r1_code_pins.txt` | B300 code vs r1 freeze pins (16/16 OK) |
| `recompute_verdict.py` | independent recompute |
| `ledger_vs_sacct.py` | ledger rows vs sacct: 25 jobs, 0 mismatches |
| `verdict_recomputed.json`, `verdict_cli.out` | CLI recompute |
| `pytest_fuc.out`, `pytest_old86.out`, `pytest_rgpool.out` | test runs |
| `mutants_auditor.out.json`, `mutants_auditor.log`, `run_mutants_copy.py` | mutation harness rerun |

## 1. Observation
See Phase Results. Key commands and results:
- `LC_ALL=C sha256sum -c …/PROTECTED_HASHES.txt` → rc 0.
- The four `grep -v '^#' <receipt> | sha256sum -c` checks → rc 0.
- `diff b300.sha repo.sha` → identical.
- `ledger_vs_sacct.py` → "jobs in ledger 25 sum closing GPU-h 10.422; mismatches []".
- Mutation summary → `{'n': 55, 'killed': 51, 'survived': ['baseline','V07c…','V12…','F11…'], 'invalid': []}`.
- B300 count check → `n_dirs=1084 in_staged_dirs=1 in_r1_manifest_lines=0`.

## 2. Logic Chain
1. Receipts verify, and the mtimes plus the git snapshots of progress.md place the freeze before the first run (sacct). So FU-C results were not computed before the card freeze.
2. The records are byte-equal to B300 files that Slurm jobs wrote inside their sacct windows, running frozen code in the project venv. So the logs are not fabricated.
3. The independent and CLI recomputes reproduce every headline number and the verdict. So there is no hardcoding.
4. The tests fail on 51 of 54 behavioural mutants, and the 3 survivors are equivalent. So they are not tests that cannot fail.
5. Ledger rows equal sacct for all 25 jobs, the total is ≤ the cap, and nothing ran outside Slurm. So C5 is clean.
6. A real HCP participant ID is written in a repo file, contrary to C4 and the dispatch rule. Under the role rule ("a single failure = INTEGRITY VIOLATION"), the verdict is INTEGRITY VIOLATION, scoped to C4 only.

## 3. Caveats
- **Severity of the C4 breach is low.**
  - The string is HCP's publicly documented example subject.
  - It is used only as a negative shape fixture.
  - It is not linked to any token, record or the 88-subject cohort.
  - It is not in git.
  - The PI/root may judge it de minimis; I report it because C4 is stated as categorical.
- **No historical squeue log.** The per-submission g3t check results were not logged. The code blocks on a hit (`scripts/topic2fu_c_slurm.py:163`), and sacct shows no g3t-G-E0 job ever existed, so the rule could not have been triggered.
- **No GPU-h used by me.** I did not re-run any training or re-evaluate a checkpoint on GPU. The records' authenticity rests on byte-equality with B300 files and the sacct windows.
- **mtimes are not cryptographic proof.** The freeze-order evidence is corroborated by git snapshots of progress.md, not by a git commit of the card itself.
- **No SendMessage.** The parent is a workflow script and reads the structured return.

## 4. Conclusion
- **Verdict: INTEGRITY VIOLATION, narrow (C4).**
- **Science is authentic.** The FU-C result (`stop`; I1 −0.113 % [−0.499 %, +0.272 %], df 7) is genuine, reproducible and correctly frozen. No hardcoding, fabrication, pre-freeze results or compute violations were found.
- **Remediation for root.** None of these steps changes the verdict:
  1. Replace the literal at test_gate_and_records.py:182 with a synthetic 6-digit string. Before using it, confirm count-only on B300 that it is absent from the 1,084 HCP names.
  2. Because the file is pinned, record the change in a dated FU-C addendum with a new test receipt. Do not edit the old receipts.
  3. Extend the repo-side C4 scan to tests/topic2_fu_c and src/topic2_fu_c.
  4. Correct the report's "No participant ID was printed or written" in the addendum.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in results/topic2/2026-11-02_fu_c/*sha256*.txt; do grep -v '^#' $f | LC_ALL=C sha256sum -c; done
/home/juke/superclaude-env/bin/python3 -I verification/auditor_FU_C_r1_1/recompute_verdict.py
/home/juke/superclaude-env/bin/python3 -I verification/auditor_FU_C_r1_1/ledger_vs_sacct.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
grep -rnP '(?<![0-9A-Za-z_.\-])[1-9][0-9]{5}(?![0-9A-Za-z_])' tests/topic2_fu_c src/topic2_fu_c   # C4 lead
```
Invalidation: any receipt failure; B300 records differing from the repo copies; a 6-digit hit confirmed (count-only) against the B300 HCP name list.
