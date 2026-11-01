# Handoff — reviewer_FU_D_r2_2 (FU_D iteration 2 gate) — Hard handoff

**Verdict: APPROVE.** 0 GPU-h used. No production file touched. Probes are in /home/juke/git/00IITP-AI/verification/reviewer_FU_D_r2_2/.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0 (67/67), at the start and again after all test runs.
- FU-D receipts all pass: addendum_01_sha256.txt 23/23, card_sha256.txt 1/1, code_sha256_at_freeze.txt 29/29, output_sha256.txt 34/34 (this one pins the result report).
- r1 receipts code_sha256_at_freeze 33/33, output_sha256_r2 156/156 and addendum_06 31/31 pass.
- Three r1 receipts fail: card_sha256 (2 lines), output_sha256 (16) and c4_sealed_originals (20). These failures predate FU-D and are expected; M3 addendum_05 documents them (C4 sanitisation).
- verdict.json sha256 is f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc (unchanged). The card is 1b7fee6c…001b, frozen 16:06:07Z, before smoke job 511 was submitted at 16:13:50Z.
- pytest, each under timeout 900, nice, OMP_NUM_THREADS=2:
  - tests/topic2_fu_d: 195 passed
  - old suite: 86 passed
  - tests/topic2_rgpool: 113 passed, 3 skipped
  - tests/topic1_lagmotif: 88 passed
- Independent exact-fraction oracle on runs/Fplus_{E,C,S}_s0/run.json: gains 0.0036313 and 0.0065460, both < 1/100. The gate fails, so card §8 step 2 gives `inconclusive`.
- Worker evidence union.out.json:
  - 423 mutants: 404 KILLED, 19 SURVIVED.
  - All 121 mutants with shipped.changed are KILLED.
  - X45 (U030) is killed by test_delta_constant_is_the_card_value. X22 (U019) is killed by test_script_gate_gains_of_half_a_percent_are_inconclusive.
  - Survivor rerun: 11 killed, 8 survived.
- My own probe (mut/run_mutants.py, mutants.json, results.json sha256 ab4e4fc6…): 36 mutants of my own design, run on a copied tree, sequentially, excluding the E192 build test and the belt test.
  - The control survived (189 passed).
  - 34 killed and 1 survived: R35, a rewording of the stop-reason string.
  - All 11 mutants that change the shipped output are killed: δ = 0.0036, 0.005 and 0.0065; the X22 replica; the joint-reading key; δ at the decide call site; the S-gain denominator; gate failure → no_verdict; gate skipped; r1 median; and one more.
  - The defect classes V06–V10 (missing gate counted as pass, failed runs counted as missing, the F− keep paths, boundaries) are all killed.
- audit_layout over the run root: PASS, 646 files, findings [].
- Ledger: no worker_FU_D_r2 rows. FU-D rows total 3.672 GPU-h plus the r1 verifier probes (about 0.05), well under the 25 GPU-h cap.
- C4: the new addendum and test file contain no `sub-` labels. The only 6-digit hits are substrings of sha256 hex.

## 2. Logic Chain
1. The two blocking items of the r1 gate are now each killed by the new test file: X45 (δ unpinned) and X22 (joint-reading text unpinned). Both my replicas and the worker's evidence show this, and so do the variants (other δ values, δ at the call site, a changed lookup key).
2. Regeneration is byte-identical, and the exact oracle agrees, so the shipped verdict `inconclusive` follows from the card §8 rules on genuine records. Three r1 verifiers had already re-scored the checkpoints on B300.
3. The changes are additive only: the frozen code, card, result report and verdict pass their receipts, and prev_snapshot is empty. C3 is met: the post hoc addendum_01 is dated and pinned, and the frozen-code departures E1–E4 are recorded as errata. Each erratum has a reading rule, and the shipped data are pinned to lie outside it.
4. I checked the 8 equivalence proofs (S023/S025, S160, S181, S207, Q08, Q19, Q21) against the code and they hold. For example, needs_fminus has `reason.endswith("(keep pending F-)")` ⇔ category keep when F− is missing. In load_runs, a completed attempt 0 next to an attempt 1 raises before attempt 1 is read. Every hcp token order equals the split order through validate_completed.
5. F1–F3 are met with an escape outcome under the card: the gate was pre-registered, its failure gives `inconclusive`, Stage 1 is not run, and the options are costed in result report §5. C5 compute is within the cap via Slurm, and C1, C2 and C4 pass.

## 3. Caveats
- I did not re-score the B300 checkpoints. The r1 verifiers did that, and this gate repair adds no new run.
- test_e192_model.py was not mutated (CPU model build).
- Nonblocking:
  - R35: the stop-reason text is not pinned. It is not on the shipped path and does not change the category.
  - The frozen defects E1 (unplanned dirs skipped when the gate fails) and E2 (NaN test_nmse accepted) remain in the code by design. They are handled by the addendum's reading rules.
  - X45 is killed only by the new file and the belt test; the r1 shipped tests alone do not kill it.
  - The worker briefly ran 3 concurrent pytest processes (disclosed).

## 4. Conclusion
APPROVE. The FU-D iteration-2 repair closes X45 and X22 with genuine, card-literal tests and causes no regression. The verdict `inconclusive` (measurement capacity at E192) is correct under the card, and the r1 E36 stop stands alone.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in results/topic2/2026-11-02_fu_d/*_sha256*.txt; do grep -v '^#' $f | LC_ALL=C sha256sum -c --quiet; done
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
PYTHONDONTWRITEBYTECODE=1 nice /home/juke/superclaude-env/bin/python3 verification/reviewer_FU_D_r2_2/mut/run_mutants.py verification/reviewer_FU_D_r2_2/mut/mutants.json /tmp/out.json
```
Invalidated if any receipt fails, if verdict.json changes, or if any of R01–R34 survives.
