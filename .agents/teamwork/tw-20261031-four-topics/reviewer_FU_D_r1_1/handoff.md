# Handoff — reviewer_FU_D_r1_1 (Hard) — milestone FU_D

## Review Summary
**Verdict: APPROVE** (with nonblocking findings). FU-D's verdict `inconclusive (measurement capacity)` under the frozen FU-D card §8 step 2 is correctly derived, reproducible from the saved records, and pre-registered. The escape (Stage 1 not run) is evidenced and costed (report §5). No integrity violation was found.

## 1. Observation
- C1: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives rc 0, 67/67 OK (`verification/reviewer_FU_D_r1_1/c1.log`).
- Receipts: `grep -v '^#' results/topic2/2026-11-02_fu_d/{card_sha256,code_sha256_at_freeze,output_sha256}.txt | LC_ALL=C sha256sum -c` gives 1/1, 29/29 and 34/34 OK. `results/topic2/2026-11-01/code_sha256_at_freeze.txt` gives 33/33 OK.
- Tests:
  - `tests/topic2_fu_d`: 129 passed, rc 0.
  - Old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed, rc 0.
  - `tests/topic1_lagmotif`: 88 passed, rc 0.
- Verdict rerun: `scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989b…b84e --out verification/reviewer_FU_D_r1_1/verdict_rerun.json` is identical (==) to the shipped `verdict.json`: inconclusive, gain_C_vs_E 0.0036313, gain_C_vs_S 0.0065460.
- Gate records (`runs/Fplus_{E,C,S}_s0/run.json`) compared with the r1 `results/topic2/2026-11-01/runs/Fplus_*_s0/run.json`:
  - Only cfg (E36_d2262 → E192_d22182), n_params (38,712,096 → 474,226,176), timing, cuda_visible, test/val numbers and train loss differ.
  - perm_file_sha256, perm_key, perm_sha256, n_cells_moved, all hyperparameters and the 13 frozen-code sha256 are identical.
  - test_nmse equals sum(test_num)/sum(test_den) exactly for E/C/S: 0.6558495 / 0.6534679 / 0.6577737.
- r1 F+ per seed (`results/topic2/2026-11-01/runs/Fplus_*`): s0 E 0.67693, C 0.65817, S 0.67783 (+2.77 %); s1 C-vs-E +3.35 %. The r1 seed-mean gains are +3.06 % (C vs E) and +2.93 % (C vs S); these are the figures card §7.1 quotes.
- Provenance and timing:
  - Host daemon commit 34f4b30 (Chavis Autocommit, 2026-11-01T15:50:24Z) contains the card with sha256 1b7fee6c…6001b, identical to the freeze receipt.
  - B300 sacct (KST − 9 h): smoke 511 submitted 16:13:47Z; gate jobs 534/535/536 submitted 16:39:57Z / 16:40:43Z / 16:41:10Z. All COMPLETED; ElapsedRaw 144 / 4230 / 4248 / 4246 s, matching the ledger and slurm.json.
  - env_check 15:28Z (data-free venv build, disclosed); view_check 16:11Z.
- Smoke `smoke/equiv.json`: reproduced r1 hcp_E_s0 test NMSE 0.9908706340280367, abs_diff 0.0; per-subject num/den and order equal.
- Ledger: `seedplan.ledger_totals` gives FU-D 3.672 GPU-h (explorers 0.03 + 0.03 + 0.001 + 0.036; worker 0.04 + 1.175 + 1.18 + 1.18) of the 25 cap. The run total is now 31.528 of 95 (all teams).
- B300 read-only (ssh, no GPU):
  - 0 `fud-*` jobs in squeue; 3 `model_final.pt` (1,898,355,817 B each) present.
  - B300 run.json sha256 equals the repo copies.
- C4:
  - My count-only scan of 88 FU-D files (results, docs, src, tests, scripts, worker/explorer metadata, worker verification) found 0 BIDS tokens. The 5 six-digit matches are sha256 hex prefixes and one GPU MiB figure, not IDs.
  - The B300 scans (`logs/scan/*.json`) and `logs/c4scan_local.json` all show 0 hits.
  - Git status of FU-D code/results: untracked, so no git writes. The only git trace is the daemon's .md snapshot.
- Layout: `audit_layout.py` on the run root gives PASS, 513 files, findings [] (`audit_layout.log`).
- Independent mutation probe (`verification/reviewer_FU_D_r1_1/reviewer_mutants.py`, `.out.json`): 26 new mutants plus control C00 (C00 survives, 124 passed). 14 killed, 12 survive:
  - Q03: seed-mean via median.
  - Q05: r1 agreement assert removed.
  - Q08: equivalent.
  - **Q09: config `DELTA = 0.003`.**
  - Q14: the 16-term check relaxed.
  - Q15: val-step check removed.
  - Q16: perm-file sha check removed (the per-key perm sha is still checked).
  - Q17: sidecar cfg dict check relaxed.
  - Q19: cross-run order check (redundant with the per-record split-order check).
  - Q20: inconclusive joint-reading text.
  - Q21: equivalent (rec is None when not completed).
  - Q24: wrapper exit code ignores post-checks (records still reject via post_checks_ok).
- Q09 in memory: `V.decide` on the shipped gate NMSE gives δ=0.01 → inconclusive (gate pass False) and δ=0.003 → no_verdict "seed plan missing" (gate pass True).

## 2. Logic Chain
1. The card was frozen (receipt; daemon-commit bytes at 15:50:24Z) before any FU-D real-data or gate job (first submission 16:13:47Z) → C3/F1 pre-registration holds.
2. The gate runs differ from r1's F+ runs only in the manipulated factor (scale), with the same perms, hyperparameters and frozen code. The gate gains recompute exactly from the per-subject terms. So the gate failure is not a software or config artefact → the inconclusive (measurement capacity) mapping of card §8 step 2 is correct.
3. Card §8 prescribes no Stage 1, no seed plan and no F− after an F+ failure. None exists → the escape is pre-registered. Report §5 costs the follow-ups (≈7.1 / ≈12 / ≈86 GPU-h) → the "untestable/escape outcome properly evidenced and costed" condition holds.
4. All GPU use went through Slurm, is ledgered, and is within the caps (3.672 ≤ 25; the run total ≤ 95). The share-rule check is enforced in code (`cmd_submit` → `share_blockers`) and logged in the worker's progress.md → C5 holds.
5. The data stayed on b300-01. The copy-backs are aggregates with positional tokens and scanned clean → C4 and C6 hold. C8: the report cites only FU-D outputs and the r1 dated outputs.
6. F2: the verdict code is tested against the V06–V10 classes (worker harness 62/62, incl. V12 F−-downgrades-modify, V10/V21 missing-gate, R04 failed-runs, R10 order). My new probe found a further gap (Q09): the δ constant is not pinned by any test, and it is reachable on the shipped data. The verdict actually shipped was produced by config.py, which is pinned in the verified 29/29 freeze receipt, and I recomputed it independently with δ = 0.01. The gap is therefore test coverage, not a wrong result → nonblocking.

## 3. Caveats
- I did not re-evaluate the checkpoints on a GPU (0 GPU-h used). The gate values are reproducible from the saved per-subject terms, and the B300 run.json equal the repo copies. A GPU re-evaluation would only re-test determinism of the frozen evaluate code.
- I did not check external repos (C7) for modification; FU-D reads only r1 data and the repo.
- The share-rule squeue results are recorded only in the worker's progress.md, not in jobs.jsonl.
- The scientific reading "gain shrinks with scale" rests on one seed at E192 (gain +0.36 %, below the r1 inter-seed spread of 0.58 pt). The report marks it as descriptive.

## 4. Conclusion
APPROVE. Nonblocking:
- (N1) Add an additive test (via a dated addendum, since the tests are frozen) asserting `K.DELTA == 0.01` and that the verdict script on the shipped results gives `inconclusive`. This kills Q09/Q20 if any further FU-D work is done.
- (N2) The other surviving validator mutants (Q03, Q05, Q14–Q17, Q24) are not reachable on the shipped data.
- (N3) Report §0/§2 single-seed wording ("closes it further", "right direction") should be read as single-seed descriptive.
- (N4) Card §7.1's "+3.06 % / +2.93 %" are seed-mean C-vs-E / C-vs-S gains, not per-seed margins. This is a wording issue only, and the card is frozen.
- (N5) The 5.7 GB of checkpoints remain on b300-01 /scratch/iitp4/fu_d, for root cleanup after the audits.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256 code_sha256_at_freeze output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f.txt | LC_ALL=C sha256sum -c; done
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989bd93666c36b821448bbde0cbbb10b5eb822b454a4ff90b9a03185b84e --out verification/reviewer_FU_D_r1_1/verdict_rerun.json
/home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_D_r1_1/reviewer_mutants.py $PWD $PWD/verification/reviewer_FU_D_r1_1/mut_work OUT.json
git show 34f4b30:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md | sha256sum   # 1b7fee6c…
```
Invalidation conditions:
- any change to the 29 frozen FU-D files or the 3 gate run.json files;
- any new run directory under results/topic2/2026-11-02_fu_d/runs;
- a seed_plan.json appearing.
