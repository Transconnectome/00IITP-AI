# Handoff — challenger_FU_D_r1_1 (FU_D, Topic 2 follow-up D, E192). Type: Hard.

## Challenge Summary
**Verdict: REFUTED (narrow).** The test-suite guard is refuted. The scientific result is not.
- The FU-D verdict `inconclusive` (F+ gate failed) holds under every independent check.
- The gate numbers reproduce bit-for-bit from the saved checkpoints on B300.
- The card was frozen before any result.
- But one constant can be mutated so that the shipped verdict flips while the whole suite stays green.

**Overall risk: MEDIUM.** The shipped verdict is correct today. The defect is a missing guard, and the fix is additive tests only.

## 1. Observation
- **Receipts.** card 1/1, code 29/29, outputs 34/34 OK. C1 PROTECTED_HASHES rc 0. r1 code freeze 33/33 OK. Checked at start and again at the end.
- **Freeze before results.**
  - Card mtime 2026-11-01T15:40:57Z; receipts written 16:06:07Z.
  - Autocommit 34f4b30 (15:50:24Z) holds the card with sha256 `1b7fee6c…036001b`, the frozen value.
  - First FU-D job (511) was submitted at 16:13:50Z, after the freeze. The gate runs started 17:46–17:52Z (sacct).
- **Gate numbers recomputed from raw per-group terms** (`runs/Fplus_*_s0/run.json` test_num/test_den, exact Fractions):
  - NMSE: E 0.6558494816918741, C 0.653467876277415, S 0.6577736746995909.
  - Gains: (E−C)/E = 0.0036313, (S−C)/S = 0.0065460, both < δ 0.01, so the gate fails.
  - Margins to δ are 0.637 and 0.345 percentage points.
  - C beats E in all 16 eval groups (+0.21 to +0.53 %). Dens are identical across arms.
- **Oracle verdict** (`verification/challenger_FU_D_r1_1/oracle_verdict.py`, no FU-D code imported): `inconclusive`.
  - Re-running `scripts/topic2fu_d_verdict.py` gives output identical to the shipped `verdict.json`.
- **B300 re-evaluation, Slurm job 575** (debug, b300-01; 83 s, 0.024 GPU-h; ledgered; no g3t-G-E0-* job at submission).
  - Saved checkpoints re-scored with the frozen `evaluate_fixture` (seed 7002).
  - All three NMSEs equal run.json exactly (max relative num diff 0.0; dens equal).
  - The saved M0 perm buffers equal the pinned perms (sha `b83e23eb…`, `72f72d1e…`, `d540c76a…`).
  - n_params is 474,226,176.
  - Perm-swap probes: C weights with the E gather give 1.102, E weights with the C gather 1.124, C weights with the S gather 1.090, against about 0.65 with the right gather. The gather is live and the arms differ.
  - Fresh eval seeds 7003/7004: C-vs-E 0.295 % / 0.293 %, C-vs-S 0.576 % / 0.585 %. The gate still fails, so test-window noise is not the issue.
  - Output: `verification/challenger_FU_D_r1_1/b300/reeval.json`.
- **Run provenance.**
  - fud_meta FU-D code hashes match the FU-D freeze, the wrapper sha matches `d598989b…`, and the frozen train script sha matches the r1 freeze.
  - run.json r1 code hashes match the r1 freeze.
  - B300 code copy: every present file matches its freeze hash.
  - argv carries exactly the card §5 values. post_checks_ok is true for all three runs.
  - Training logs: losses are finite and decreasing; the C<E<S ordering holds at all 4 val steps.
- **Ledger.**
  - sacct ElapsedRaw 4230/4248/4246 s → 1.175/1.180/1.180 GPU-h (matches).
  - Explorers 0.097. FU-D total 3.672; run total 30.665 at the 536 close (recomputed with `seedplan.ledger_totals` up to that row).
- **C4.** Count-only scan of 76 FU-D files: 0 six-digit tokens, 0 `sub-` labels.
- **Tests.** `pytest tests/topic2_fu_d`: 129 passed in 97 s.
- **Mutation.** Own harness `verification/challenger_FU_D_r1_1/mutation/run_mutants.py`: 50 mutants on a copied tree, 120-test suite without the slow E192 build and the output scan (neither references δ). Baseline is green.
  - 45 killed, 5 survived (`mutants.out.json`):
    - **X45** `config.DELTA = 0.01 → 0.0036`. On the real records the verdict script then gives gate `pass: True` → `no_verdict` ("seed plan missing"). The shipped verdict flips with the suite green. `grep DELTA|0.01 tests/topic2_fu_d` outside test_verdict.py finds nothing; the worker's 62 mutants never mutate config.DELTA.
    - **X22** the JOINT_READING text for `inconclusive` changed. On the real records `joint_reading_with_r1` becomes "null replicates at E192", a wrong scientific reading, with the suite green. No test checks the shipped verdict.json or the inconclusive reading.
    - **X35** the records `perm_file_sha256` check removed. Partly redundant (perm_sha per key and the wrapper precheck remain).
    - **X37** the 16-term length check removed (a record with fewer terms is accepted).
    - **X49** the r1-agreement assert removed. Behaviourally equivalent today, since the rules are identical.

## 2. Logic Chain
1. Receipts, the git snapshot and the sacct times show the card and code were fixed before any FU-D real-data or gate result → F1/C3 hold.
2. Raw terms, the checkpoint re-evaluation and the perm buffers give the same numbers → the headline numbers are genuine, with no arm mix-up.
3. The gains are below δ on both criteria → card §8 step 2 → `inconclusive`. Oracle and script agree → the verdict follows the card.
4. The swap probes show the gather is active at E192, so the small gain is not a dead-code artefact.
5. But X45 shows the suite does not pin the decision constant. A plausible edit (δ, or the reading text, X22) changes the shipped verdict or its reading with the suite green. This is the same defect class that blocked earlier gates in this run (M2 r3 T01/T02, M3 r2 V-mutants: "flip if code changed").
6. Therefore: the scientific claims are CONFIRMED, and the worker's claim that the tests guard the verdict path ("62/62 killed") is REFUTED for X45/X22.

## 3. Caveats
- The single-seed F+ gate is pre-registered (card §7.1). I did not re-run training: one E192 run is 1.18 GPU-h, above the 1 GPU-h verifier cap. Seed-noise robustness of the 0.36 % is untested beyond eval-seed noise.
- smoke/equiv.json stores only booleans for the per-subject equality. The pooled r1 NMSE match is exact, but the per-subject arrays are not in the repo to recheck. This does not matter for the decision, because Stage 1 was not run.
- Card §7.1 calls "+3.06 % / +2.93 %" the two E36 F+ seeds. They are the r1 seed-mean C-vs-E and C-vs-S gate gains; the per-seed C-vs-E gains are 2.77 % and 3.35 %. This is a wording slip in the frozen card and does not affect the decision.
- The report's "a larger model … closes it further" is descriptive and rests on 1 seed per scale.
- An F+ failure could also be read substantively ("at E192, grouping is irrelevant even for planted structure"). The card pre-registers `inconclusive`, and the worker follows the card.
- **My own procedural slip.** A flock syntax error released job 575 before its ledger "started" row existed. I wrote the row while the job was still PENDING (0 GPU-h used by then). The closing row records the true submit time 19:26:10Z.
- **Leftovers.** `verification/challenger_FU_D_r1_1/mutation/__pycache__/` remains, because the cleanup rm was denied; I did not work around it. On B300, `/scratch/iitp4/challenger_FU_D_r1_1` (24 KB, scripts and outputs) also remains.

## 4. Conclusion
- **REFUTED**, narrow and blocking only for the test guard.
- **Fix** (additive, no frozen-file edits):
  - a test pinning `config.DELTA == 0.01` and `fplus_gate` behaviour at the shipped values;
  - a regression test that runs `scripts/topic2fu_d_verdict.py` on the shipped records (or copies of them) and asserts `inconclusive`, the reason, the gains and the exact joint-reading text;
  - optional tests for X35/X37.
- The FU-D scientific verdict (`inconclusive`, measurement capacity; r1 stop stands alone) and all numbers are CONFIRMED and need no change.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_d/{card_sha256.txt,code_sha256_at_freeze.txt,output_sha256.txt} | LC_ALL=C sha256sum -c
/home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r1_1/oracle_verdict.py        # inconclusive
cd verification/challenger_FU_D_r1_1/mutation && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 run_mutants.py /tmp/x.json X45,X22   # both SURVIVE today
cat verification/challenger_FU_D_r1_1/b300/reeval.json   # job 575 re-eval
```
Invalidation: a new test that kills X45 and X22 closes the blocking item. Any change to the shipped verdict.json or the receipts voids this report.
