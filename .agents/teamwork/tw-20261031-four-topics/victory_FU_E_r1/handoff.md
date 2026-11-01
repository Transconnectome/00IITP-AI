# handoff — victory_FU_E_r1 (Hard handoff, victory audit of milestone FU_E)
Written 2026-11-01T19:40Z. Verdict: **VERIFIED_COMPLETE (VICTORY CONFIRMED)**. Shipped FU-E scientific verdict: **inconclusive** (synthetic F+ measurement-capacity gate failed on hcp_S_s2), reproduced independently.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` rc 0 (67 entries), at start and at end.
- Receipts rc 0: `results/topic2/2026-11-02_fu_e/card_sha256.txt` (card 072553b0…, pins, code freeze, smoke sbatch); `code_sha256_at_freeze.txt` (17 files); `output_sha256.txt` (12 files); r1 `results/topic2/2026-11-01/code_sha256_at_freeze.txt`.
- Timeline (UTC mtimes): FU-E code 15:30–15:46Z → card 16:21:26Z → freeze receipts 16:22:56Z → job 524 submit 16:24:31Z (sacct) → start 17:03:57Z → end 17:20:40Z → verdict.json 17:25:19Z → report 17:27:13Z → ID scan 17:29:59Z → output receipt 17:32:30Z. Smoke job 499 (synthetic only) 16:04:04–16:04:12Z, before freeze.
- B300: `/scratch/iitp4/fu_e/main/extract.json` sha 1921b044… = repo copy; sacct 499 debug 8 s, 524 gpu 1003 s, both COMPLETED 0:0 on b300-01; all 15 checkpoint sha256 on B300 = pins; B300 FU-E code tree sha = freeze receipt; extract.json code hashes = freeze; rgpool_freeze_ok True.
- `pytest tests/topic2_fu_e`: 71 passed (verification/victory_FU_E_r1/logs/pytest_fu_e.txt).
- `scripts/topic2fu_e_verdict.py run_524/extract.json` → verdict.json byte-identical (sha d4d92a98…), stdout identical.
- Independent CPU recompute (own code, no FU-E import; verification/victory_FU_E_r1/cpu/indep_recompute.{py,out}): F+ S_s2 Idiff 5.76 ≤ p95 10.59 (alt null seed 777: 10.97) → F+ FAIL; other 14 pass (E_s2 marginal 11.29 vs 11.00); seed means E 16.02 / C 22.71 / S 16.48; F− pass (means −2.91/−0.86/−1.29 < 5.46/3.48/6.28); G2 pass (E mean 61.07); G3 64.13 > 5.91, acc 1.0; J1 mean 0.081 [−0.066, 0.228] (SD 0.1185); J2 0.150 [0.098, 0.202]; verdict inconclusive; counterfactual with F+ passing = inconclusive.
- Independent GPU re-execution, Slurm job 570 (debug, b300-01, 59 s, 0.017 GPU-h, ledgered): own half-z/cov2/similarity on F+ (S_s2, E_s2, C_s0, S_s0) and main (E_s0, C_s0, S_s2, E_s3): max |dR| ≤ 0.0031, Idiff within 0.014 of job 524; S_s2 F+ 5.760 ≤ p95 10.57 confirmed; common-mask voxels 190382 = 524.
- Own C4 scan on B300 (names in memory: 1084 HCP download names + 88 r1 subject dirs) over 1392 FU-E files (results, docs, src, tests, scripts, verification/*FU_E*, metadata *FU_E*): 0 hits.
- Own mutants (verification/victory_FU_E_r1/mut/results_v2.json): 20 KILLED, 4 SURVIVED (X04 fixture-problems override removed; X14 fixture gates read pooled; X15 main reads pooled; X22 F− uses min not mean). None changes the shipped verdict (cpu/survivor_impact.out).
- sacct: no `g3t-G-E0-*` job since 2026-11-01 20:00 KST (smoke-job share-check deviation had no conflict).
- Ledger: FU-E 0.297 GPU-h (explorers 0.015 + smoke 0.003 + main 0.279) of cap 1.5; sacct elapsed × 1 GPU matches.
- Report numbers (§0–§4) all match verdict.json / my recompute.

## 2. Logic Chain
1. Card frozen (sha receipt) before any real-data FU-E statistic (timeline above) → F1/C3 satisfied.
2. Code is in FU-E-only paths; nothing outside per-milestone dirs written in the worker window; r1 freeze holds; C1 holds → F2 path discipline, no regression.
3. Shipped verdict = deterministic function of extract.json (byte-identical rerun) and my independent code agrees on every gate and interval → verdict not fabricated or miscomputed.
4. extract.json R matrices are genuine: B300 copy identical, and my independent GPU recompute reproduces them for 8 (condition, encoder) pairs including the decisive S_s2 F+ slot.
5. Card §7–8 applied: F+ requires every (arm, seed) above null; S_s2 fails → inconclusive. Even with F+ passing, J1 straddles 0 and δ → inconclusive. Verdict robust.
6. Compute within cap, Slurm-only, ledgered; C4/C6 respected (0 ID hits; HCP data on B300 only; aggregates only copied back).

## 3. Caveats
- Surviving mutants X04/X14/X15/X22 are test-coverage gaps (readout-key wiring, F− mean aggregation, duplicate fixture records), nonblocking because none flips the shipped verdict and none is a V06–V10-class defect.
- The decisive F+ failure is on hcp_S_s2, the r1 run already known (card §0, r1 addendum 04) to sit at the trivial solution; the every-seed rule made this outcome foreseeable at freeze. Not post hoc; disclosed.
- "Fingerprinting" here is within-run split-half identifiability (REST1_LR only); age/sex probe not run (card §10, untestable at δ). Milestone text says "and/or", so acceptable.
- Init-twin "bit-identical to r1 step-0 weights" claim not verified (descriptive only).
- Report wording: init twins "identify every held-out subject (accuracy 1.00)" — seed-mean accuracy is 0.996 (rounding).
- Deviations live in the result report §3, not in a dated addendum; none is a post-freeze departure from the card.
- I did not run the old 86-test suite; C1 byte-identity of old src/tests plus r1 freeze covers no-regression for FU-E (which touched no shared file).
- Leftover temp copy verification/victory_FU_E_r1/mut/vfe_mut_ylj42ttp (src/tests/scripts copy from killed v1 harness; deletion refused by the harness). B300 /scratch/iitp4/victory_FU_E_r1/ (code + aggregate probe output, 172K + json) left as evidence.

## 4. Conclusion
FU_E is VERIFIED_COMPLETE. F1, F2, F3 and C1–C8 are met; the shipped FU-E verdict `inconclusive` (F+ capacity gate failed on S_s2) is correct per the frozen card and independently reproduced on CPU and GPU. r1 `stop` unchanged; the downstream identifiability question remains open.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-02_fu_e/output_sha256.txt | LC_ALL=C sha256sum -c
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q
/home/juke/superclaude-env/bin/python3 -I verification/victory_FU_E_r1/cpu/indep_recompute.py results/topic2/2026-11-02_fu_e/run_524/extract.json
/home/juke/superclaude-env/bin/python3 -I verification/victory_FU_E_r1/cpu/compare_probe.py
```
Invalidation: any receipt mismatch; a changed extract.json; a GPU re-execution with max |dR| ≫ 0.01 or S_s2 F+ Idiff above its null.
