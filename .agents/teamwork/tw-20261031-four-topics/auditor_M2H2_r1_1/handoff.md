# Handoff (Hard): auditor_M2H2_r1_1, forensic integrity audit of M2H2 (Topic 3 H2 random-init control)
Written 2026-11-01T17:26Z. Verdict: **CLEAN** (no integrity violation). Integrity mode inferred: Development (ORIGINAL_REQUEST has no from-scratch / no-delegation constraint).

## 1. Observation

**Freeze before results (H1′).**
- `addendum_07_sha256.txt` verifies (sha 09b45220…d84b). The file is read-only, mtime 2026-11-01T15:57:27Z, and the receipt says 15:57:40Z.
- Independent evidence: the host autocommit snapshot 35d10a5 (16:05:25Z) already holds the addendum at sha 09b45220…d84b.
- sacct on connectome: gate job 218063 started 16:22:19Z; random job 218064 started 16:32:19Z. Both are after the freeze.
- Explorer probes before the freeze (verification/explorer_M2H2_r1_{1,2,3}): random init ran only on `torch.randn` synthetic input; real frames went through trained weights only. This matches addendum §10.

**Compute, ledger, cap.**
- `sacct -u connectome1` since 2026-11-01T11:00Z shows exactly these M2H2 GPU jobs: 218004 (66 s), 218007 (61 s), 218041 (74 s), 218063 (485 s) and 218064 (1160 s). All ran on debug/node1 with gres/gpu=1. 218032 and 218042 were CPU-only.
- All have start and closing rows in results/gpu_ledger_2026-10-31.md, and the GPU-h match ElapsedRaw.
- M2H2 total: 0.516 GPU-h, plus 0.064 for this audit (job 218067). The cap is 6.
- There are no M2H2 or topic3 job names on B300 sacct.
- The venv is project-local, under /home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/venv.

**Authenticity of the results.**
- All 24 returned files (gate/R0_*, random/R1..R10_*, both records) and both Slurm logs are byte-identical to the files the jobs wrote on connectome.
- The `code_sha256` in gate_record.json and random_record.json (20 files each) equals the current local repo files.
- **Independent rerun, Slurm 218067:** seed 3 alone through the shipped code. The code is byte-identical to the repo (20 files), and the index sets were generated in the job.
  - R3_scalars, R3_subsets and E1 all give max relative diff **0** against the worker's job 218064.
  - The encoder hash, the index-set hash and the code hashes are equal.
  - Control: worker R3 vs R8 differ by 7.8%, so the comparison can discriminate.
  - Output: verification/auditor_M2H2_r1_1/seed3_rerun_compare.txt.
- **Independent recomputation:** verification/auditor_M2H2_r1_1/recompute_h2.py. It uses my own PR, corrPR, index sets, sign-flip, bootstrap, Holm and decision rule, written from the addendum text.
  - δ equals the addendum values exactly.
  - T's subject-level A1 L2−L3 reproduces pinned Family A to 1e-12.
  - Family C max |diff| 1.8e-15. Labels C1 INC, C2 INC, C3 TE+, C4 TE+.
  - All 20 Family L labels match. Seeds at or below δ: C2 seeds 3 and 8; C1 seeds 1, 5, 6 and 8.
- Report numbers spot-checked against h2_results.json, all matching: Family L ratios, E1 values (2.78 / 11.02 / 3.58), the R1 secondary, and seed 4 H1a (−0.04%, p 0.52).

**Code, tests, hygiene.**
- No hardcoded results or facades. `FROZEN_DELTAS` are the addendum's constants, and they are checked at runtime against the pinned JSON. The gate verdict fails closed on any missing check, and the comparator returns inf on a shape mismatch.
- `tests/topic3_h2`: 71 passed (288 s). The old suite: 86 passed. The tests use synthetic planted-effect fixtures, and none of them echo the shipped numbers.
- Worker mutants: mutants.out.json shows baseline rc 0 and 32/32 killed.
- My 10 extra mutants (aud_mutants.out.json): 8 killed, 2 survived (A05, A09; see §3).
- C1 rc 0 (checked at 17:05Z and 17:25Z). h2 output_sha256 (61 files) rc 0. 2026-10-31 receipts rc 0, except the known card_sha256.txt trailing-token case; its hash matches 683374565d80….
- Pinned src/topic3_spectral, tests/topic3_spectral and scripts/topic3_*.py are unmodified, and no new scripts/topic3_* file was added.
- Git: only "Chavis Autocommit" commits in the window, and none of them touch .py, .json or .npz files.
- IDs: the `sub-` hits are the synthetic `sub-SYN..` fixtures and the docstring word "sub-modules". Returned npz files hold no string, name or ids arrays. There are no 6-digit runs in the results JSON/TXT.
- Layout lint on the run root: findings [].

## 2. Logic chain
1. The freeze precedes every random-init forward on real frames. The receipt, the file mtime, the independent git snapshot and sacct all agree (O-H1′). So no result was computed before the card was frozen.
2. The returned aggregates equal the job-written files, and one seed reproduces bit-exactly through code identical to the repo. So the random-arm data are genuine, not fabricated, and the recorded code is the code that ran.
3. An independent implementation reproduces every statistic and label from those aggregates and the pinned inputs. So the verdicts follow the frozen rule, and there is no hidden fallback in the stats path.
4. The GPU use is all Slurm on connectome, ledgered, and far under cap. There are no ID leaks, no pinned or protected edits and no agent git writes. So no governance check fails.

## 3. Caveats (nonblocking findings)
- **N1, an undisclosed late overwrite of the worker's remote code dir.** At 2026-11-01T16:39:09Z, during random job 218064, every remote file except h2stats.py and index_sets_J.npy was rewritten (remote ctime evidence). The rewrite came from a tree snapshot dated about 16:01–16:05Z:
  - `driver.py` was replaced by an older version (sha 197192b7…, 13622 B; it has no SUMMARY_KW and no try/finally work-dir deletion);
  - `pinned_trained_spectra.npz` was replaced by a truncated, non-zip file (1,022,976 of 4,767,212 B, sha bbe65642…).
  - The most likely cause is the stalled early upload that the worker's progress log mentions ("explicit ProxyCommand stalls uploads >160 KB") finishing late.
  - **No effect on results.** The random job hashed its code and the pinned npz at 16:32:21Z. Its worker pool is `fork`, all imports happen at start, and the random arm never re-reads the pinned npz. The seed-3 rerun reproduces bit-exactly.
  - What still needs action: the remote dir no longer matches logs/ship_manifest_sha256.txt, and the handoff does not mention this. Any reuse would run the old driver; it would fail closed on the pinned-hash check. Re-ship or delete that dir before any reuse.
- **N2, a test gap (A05).** Changing the card index-set seed (+100 → +101) passes the tests. In production it is guarded: `topic3h2_stats.py final` halts unless T reproduces pinned Family A, and the job records `index_sets_equal_job_generated`.
- **N3, an equivalent mutant (A09).** Removing the duplicate-window check still raises, through the "incomplete subjects" path.
- **N4, minor record inaccuracies.**
  - The worker's progress.md puts the mutation run at 17:00–17:15Z, but mutants.out.json is dated 16:36Z.
  - The report says "every script that touches H2 data verifies this hash"; the driver itself does not, only the launcher and the stats script do.
- **N5, δ and K were chosen by the worker.** The worker disclosed this. δ is PI-owned (sci-pipeline), and C1 sits on the δ boundary.
- **N6, exposure claim scope.** The lab's connectome bundle `main_embedding_extraction.py` has a `--random_init` "TSO probe" option. Addendum §10's "no random-init statistic on real frames computed by anyone" can only be vouched for this run's agents.
- **N7, out of M2H2 scope, for root.**
  - connectome user connectome1 has hung `find /storage…` processes from 2026-10-30 (PIDs 257218/257219, 259389/259390, 259475/259476). They predate this milestone and conflict with the admin rule.
  - `src/topic3_h2/__pycache__` (cpython-312) was created at 17:08:20Z by an unknown process. It is untracked, and not part of any recorded hash.
- Not investigated: I did not rerun the gate arm (trained re-extraction); the worker's G1–G5 records and my R0-vs-T subset check (6.4e-7) stand. I did not audit the internals of the vendored fork code beyond its pins.

## 4. Conclusion
**CLEAN.** None of the forensic checks failed. The M2H2 results are authentic: there is a bit-exact independent seed rerun, and an independent recomputation matches every number and label. The rule was frozen before the results, and compute and governance comply. Nonblocking: N1 (disclose; re-ship or delete the worker's remote code dir before any reuse), N2 (add a test for the index-set seed), and N5 (PI confirms δ).

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/addendum_07_sha256.txt results/topic3/2026-11-02_h2/output_sha256.txt
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 verification/auditor_M2H2_r1_1/recompute_h2.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 verification/auditor_M2H2_r1_1/aud_mutants.py   # ~3 min
ssh connectome 'sacct -j 218063,218064,218067 -X -o JobID,Start,End,ElapsedRaw,State'
ssh connectome 'cd /home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/code && find . -type f -printf "%C+ %p\n" | sort'   # N1 ctimes
```
- Seed rerun: /home/connectome/connectome1/iitp4_m2h2/auditor_M2H2_r1_1/ (aud.sbatch, code, logs, returned_218067; the work dir was deleted in the job). The comparison output is in verification/auditor_M2H2_r1_1/seed3_rerun_compare.txt.
- Invalidation conditions: any change to the hashes in output_sha256.txt; a rerun of any seed that is not bit-identical; evidence of a random-init forward on real frames before 15:57:40Z.
