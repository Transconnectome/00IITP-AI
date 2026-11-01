# Handoff (Hard) — auditor_M2H2_r2_1, forensic audit of M2H2 iteration 2
Written 2026-11-01T20:27Z (UTC). Parent: root coordinator 5fddb83e. Verdict: **CLEAN**.

## Forensic Audit Report
**Work Product**: worker_M2H2_r2 additions: tests/topic3_h2/test_h2r2_{stats_regression,stats_guards,family_oracle,gate_components}.py; results/topic3/2026-11-02_h2/r2/ (addendum 08 and its receipt); 2 ledger correction rows; verification/worker_M2H2_r2/*. I also re-checked the pinned H2 artifacts: src/topic3_h2, scripts/topic3h2_*, results/topic3/2026-11-02_h2, addendum 07 and the result report.
**Profile**: General Project. Integrity mode is Development: ORIGINAL_REQUEST.md has no from-scratch or no-delegation constraint.
**Verdict**: CLEAN

### Phase Results
- Hardcoded results / facades: PASS. The new files are tests only, and no src or scripts file changed.
  - Regression tests compare against the shipped JSON. They say plainly that they are regression guards and not a pre-registration.
  - The family oracle is independent numpy code. Its seed effects are set by construction.
  - The δ literals are the frozen addendum 07 values.
- Tests that cannot fail: PASS. I wrote my own replay harness (verification/auditor_M2H2_r2_1/probes/replay_mutants.py) and ran it in copied trees with a green baseline (167 passed ×2):
  - r1 survivors N26, W4 and N55, with their text checked against the r1 harness files: each SURVIVED the shipped 8-file suite run in full (71 passed) and was KILLED by the 4 new files.
  - 4 mutants I designed, outside the r1 union (Holm significance forced true; subject endpoint uses the last seed; EQ rule uses CI95; reversed seed order in `final`): all KILLED by the extended suite.
  - All files were restored, and the shipped outputs are unchanged.
- Fabricated logs / mutation evidence: PASS.
  - union_mutants.out.json has 125 definitions, 115 edits, 37 r1 survivors new=KILLED/ext=KILLED/shipped=SURVIVED, 53+25 others ext=KILLED, and every file restored.
  - It is consistent with the 120-line log. The summed run times divided by 2 trees, plus the baselines, come to ≈6202 s, against a meta runtime of 6265 s.
  - My replays match its entries.
  - The worker's pytest logs show 167/138/86/88.
- Test execution (mine): PASS. tests/topic3_h2 167 passed, 0 skipped; tests/topic3_spectral 138 passed; old suite (STRICT_E2E=1) 86 passed; tests/topic1_lagmotif 88 passed.
- Receipts / C1: PASS. Checked at 20:07Z and again after all my runs (20:25Z):
  - PROTECTED_HASHES rc 0; H2 output_sha256.txt (61 entries) rc 0; addendum_07 rc 0; addendum_08 (5 entries) rc 0; 2026-10-31 output and addendum_02–06 rc 0.
  - The two known exceptions remain: card_sha256.txt fails only on its trailing token (the hash 683374565d80… matches the card), and code_sha256_at_freeze.txt fails only on the launcher change disclosed in addendum 01.
- Writes to pinned or protected paths: PASS.
  - The only files newer than 17:53Z (r2 start) under src/topic3_spectral, tests/topic3_spectral, tests/topic3_h2, scripts, src/topic3_h2, docs/…/topic3 and results/topic3 are the 4 tests and the r2/ files.
  - No file in src/topic3_h2 is missing from the receipt, and there is no new scripts/topic3_* file.
  - The r1 harness dirs are unmodified.
- Results before card freeze: PASS. Addendum 07 was frozen at 15:57:40Z. Jobs 218063/218064 started at 16:22:19Z/16:32:19Z (sacct). The explorer smokes before the freeze ran random init on synthetic iid noise only (I read their output JSONs).
- Addendum 08 numbers: PASS. I recomputed them independently from h2_results.json:
  - E1 δ-boundaries 0.1575/1.0175, 0.4580/1.1115, 0.5483/1.2912, 0.6636/1.2057;
  - E2 R1 −1.607 [−3.769, +0.555] (cov) and −0.736 [−3.181, +1.709] (corr);
  - E3 L0 INC values;
  - E8 single-seed labels (C1 EQ for seeds 1, 5, 8, TE+ for 4, 7, 9, 10, INC for 2, 3, 6; C2 TE+ for 4, 5, 7, 9, 10; C3 and C4 TE+ for all seeds);
  - result-report sha bb1ef63e…b103.
  - No rule, label or number changed.
- GPU / Slurm / ledger / cap: PASS.
  - I ran `TZ=UTC sacct -u connectome1 -S 2026-11-01T14:00:00`. Its only GPU jobs are 218004, 218007, 218041 and 218063–218069, and every one has started and completed ledger rows.
  - The correction rows match sacct UTC (16:22:19–16:30:24Z and 16:32:19–16:51:39Z). There are no jobs after 218071 and no file on connectome under iitp4_m2h2 newer than 17:53Z, so r2 used 0 GPU-h.
  - The ledger's first 55484 bytes are byte-identical to the worker's prev_snapshot (sha 9f9843eb…), so it is append-only.
  - M2H2 total is 0.819 GPU-h against its 6 GPU-h cap.
- Participant IDs: PASS.
  - I loaded the 57 real IDs (format: sub- prefix plus 4 digits) in memory only and scanned 95 M2H2 files for full labels and standalone 4-digit cores: 0 hits.
  - The test names are synthetic ("sub-SYN%02d", in memory only), and no hashed forms were found.
- Git writes: PASS. Every commit since 17:50Z is "Chavis Autocommit" (the host daemon), and contains only .md/.txt files. Nothing is staged and there is no stash.
- Other envs / installs: PASS. Everything ran locally with superclaude-env, and r2 made no connectome access.
- Layout: PASS. audit_layout.py on the run root: findings [] (572 files).

## 1. Observation
- The worker's handoff.md has mtime 2026-11-01T20:01:15Z, but its header says "Written 2026-11-01T20:05Z". Its structured return says C1 was checked "at the end (20:05Z)", and progress.md has a 20:05Z entry. The addendum 08 mtime is 19:59:56Z. My clock at the first check read 20:04:05Z.
- src/topic3_h2/__pycache__ and vendor/__pycache__ have mtime 17:08:20Z, before r2 started at 17:53Z. r1 verifiers had already disclosed them.
- Raw evidence:
  - verification/auditor_M2H2_r2_1/logs/{pytest_topic3_h2,pytest_topic3_spectral,pytest_old86,pytest_lagmotif,replay_mutants}.log
  - verification/auditor_M2H2_r2_1/replay_mutants.out.json
  - verification/auditor_M2H2_r2_1/probes/{id_scan.py,id_scan2.py,single_seed_check.py,replay_mutants.py}

## 2. Logic Chain
1. All receipts pass, and only the declared files are newer than the r2 start. So r2 changed no pinned file, and it added no code that could alter the verdict.
2. My own mutant replays reproduce the union harness's per-mutant labels. The harness log, its timings and its JSON agree with each other. So the mutation evidence was produced by real runs and is not fabricated.
3. Novel mutants outside the r1 union are also killed, so the new tests are not tuned only to the named mutants and can fail.
4. sacct, the connectome mtimes and the byte-prefix check of the ledger agree with the worker's 0 GPU-h claim and with its append-only claim.
5. The 20:05Z timestamps are about 4 minutes after the files were actually written. Every claim attached to them (C1, receipts, suite counts) I re-ran myself with the same result. So this is imprecise metadata. It is not fabricated evidence and changes no result.

## 3. Caveats
- I did not search for new mutants beyond 4 novel edits; that is the challengers' remit. I did not rerun any GPU job, because r2 used no GPU and the r1 runtime evidence was audited in r1.
- The regression tests (test_h2r2_stats_regression.py) by design cannot detect a defect that was already in the shipped outputs. The oracle file and the r1 independent recomputations cover that risk.
- δ (0.5×|trained effect|, log 1.10) was chosen by the worker and frozen before the results. It still needs PI confirmation (addendum 08 §8). This is a governance item, not an integrity one. C3 TE+ holds only for f ≤ 0.548.
- The ID scan covers the 57 E192 pinned IDs. It does not cover arbitrary other cohorts.
- I can attribute git status changes made during my audit only to other agents' metadata. Each path was checked against the declared r2 additions.

## 4. Conclusion
CLEAN. I found no hardcoded results, facade, test that cannot fail, fabricated log, write to a pinned or protected path, result before card freeze, unledgered or non-Slurm GPU use, participant-ID leak, or agent git write in M2H2 iteration 2. The H2 verdict is unchanged and reproduced by the shipped code in copied trees: gate PASS; C1 INC, C2 INC, C3 TE+, C4 TE+.

Nonblocking items:
- (a) The worker metadata timestamps are forward-rounded (20:05Z against file mtimes of 19:59:56–20:01:15Z).
- (b) The δ question for the PI is still open.
- (c) Connectome cleanup is owed: /home/connectome/connectome1/iitp4_m2h2/*. The worker_M2H2_r1/code dir no longer matches the ship manifest.
- (d) Untracked __pycache__ dirs under src/topic3_h2 date from 17:08:20Z, before r2.
- (e) Addendum 08 sits in results/…/r2/ and not in docs/. The worker disclosed this.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && for f in .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt results/topic3/2026-11-02_h2/output_sha256.txt results/topic3/2026-11-02_h2/r2/addendum_08_sha256.txt results/topic3/2026-11-02_h2/addendum_07_sha256.txt; do LC_ALL=C sha256sum -c $f >/dev/null; echo $? $f; done`
- `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. nice timeout 900 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q -rs tests/topic3_h2` → 167 passed
- `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/auditor_M2H2_r2_1/probes/replay_mutants.py`. It needs logs/pytest_topic3_h2.log to contain EXIT=, and verification/auditor_M2H2_r2_1/trees must not exist. It takes about 16 min.
- `ssh connectome 'TZ=UTC sacct -X -u $(whoami) -S 2026-11-01T14:00:00 -E now --format=JobID,JobName%40,AllocTRES%45,Start,End,ElapsedRaw,State -P'`
- Invalidation: a changed sha of any receipt-listed file; a new connectome GPU job without ledger rows; a non-daemon commit; any hit from `probes/id_scan2.py <paths>`.
