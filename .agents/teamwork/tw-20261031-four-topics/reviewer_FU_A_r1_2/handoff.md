# Handoff (hard) — reviewer_FU_A_r1_2, milestone FU_A (Topic 2 follow-up A), 2026-11-01T17:45Z

## Review Summary
**Verdict: APPROVE.** FU-A reaches a properly evidenced escape outcome. Its card was frozen before any result. The F+ training-loop gate ran on B300 via Slurm and failed: +0.551 % < δ 1 %. By the card, the verdict is `inconclusive` (measurement capacity) and Stage 1 is not run. The verdict is reproduced, costed and reported against the r1 stop. No blocking issues; 5 nonblocking findings below.

## 1. Observation
- C1: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives rc 0, 67/67 OK (verification/reviewer_FU_A_r1_2/c1.txt). Rechecked at the end of the review: 0 non-OK.
- FU-A receipts: card_sha256.txt 8/8, code_sha256_at_freeze.txt 21/21 and output_sha256.txt 21/21 all OK. The r1 code_sha256_at_freeze.txt is 33/33 OK.
- Tests (mine):
  - tests/topic2_fu_a: 69 passed, 1 skipped (the Stage-1 token scan, "wave not run"), rc 0.
  - Old suite with STRICT_E2E=1 (tests/test_empirical_four_topics.py, tests/test_pilot_connectome.py, tests/e2e): 86 passed.
  - tests/topic2_rgpool: 116 passed. The FU-B-card failure that the worker reported is no longer present.
- Card sha256 72be3e83…18fb. freeze_time.json gives 16:06:01Z. Independent evidence: the host autocommit 35d10a5 (2026-11-02T01:05:25+09:00 = 16:05:25Z) contains the card, and `git show 35d10a5:<card> | sha256sum` gives 72be3e83…. The first gate run started at 16:12:33Z, so the card came first.
- Run records (results/topic2/2026-11-02_fu_a/runs/Fplus_{E,C}_s0/run.json):
  - Σnum/Σden equals test_nmse exactly (E 0.7746782345624923, C 0.7704092658872178). The gain (E−C)/E = 0.0055106 is recomputed.
  - C is lower than E in 16/16 groups, and the test denominators are identical across arms (same evaluation data).
  - fua_target is cell12_kappa, the card sha matches, and κ, σ_v, κ_fix equal fua_constants.json.
  - perm_file_sha256 = perms_fua_Fplus.npz (629a699b…); perm sha E b83e23eb… and C e32b7599… equal fixture_build.json.
  - fua_code_sha256 equals the freeze receipts and the current files; the r1 code_sha256 entries equal the r1 freeze pins.
  - fua_checks max_within_cell_spread is 0.0, and the sources were restored.
- Frozen loop path (src/topic2_rgpool/train.py, run and evaluate_fixture): training, VAL and test all call `fsrc.sample`, where fsrc is built from the module-global `FixtureSource`, which run.py rebinds. So the test NMSE is measured on the cell-mean field.
- B300, read-only via ssh (dgx1,node1 jump):
  - The /scratch/iitp4/fu_a/runs/*/{run.json, train_log.jsonl} sha256 values equal the repo copies (4/4).
  - sacct lists exactly three FU-A GPU jobs: 403 (199 s), 427 (266 s) and 507_0/507_1 (1480/1479 s, gpu partition, COMPLETED). The others are CPU-only.
  - 0 `g3t-G-E0-*` jobs exist since 2026-11-01, so the sharing rule was not breached. No FU-A job is queued or running now.
- Ledger: results/gpu_ledger_2026-10-31.md lines 78 (start) and 101 (close) for job 507, 0.822 GPU-h. Explorer jobs: 403 (lines 41/52, 0.056) and 427 (lines 62/64, 0.074). FU-A total 0.952 of the 8 GPU-h cap.
- Verdict: results/topic2/2026-11-02_fu_a/verdict.json gives `inconclusive`, reason "measurement-capacity gate failed". src/topic2_fu_a/verdict.py implements the card §8.3 order: step 2 returns before any Stage-1 check.
- r1 numbers quoted by the FU-A report:
  - r1 F+ test NMSE E 0.6769/0.6803, C 0.6582/0.6575; gains 2.77 % / 3.35 %, mean 3.06 %. Verified from results/topic2/2026-11-01/runs.
  - r1 Stage-0 C−E r_mean +0.0039 [0.0005, 0.0074], 11/16; pca2 −0.0516 [−0.0535, −0.0498], 0/16. Verified from stage0_hcp.json.
- Calibration recomputed: κ = 1/√Q = 5.699891773354029 and σ_v = √(NF·n̄/(1−NF)) = 6.545925453832064 (n̄ = 162.65), both exact.
  - F+-only realized noise share on fresh samples: 0.2189 / 0.2198 / 0.2204 (3 seeds, 48 windows × 20 frames each) and 0.221 (4 × 100 frames).
  - Planted in-brain cell fraction 0.789 gives an analytic share of 0.224.
- Mutation probe (verification/reviewer_FU_A_r1_2/mutants/run_mutants_rv.py, results.json sha 2ad860b2…): 30 new mutants against the shipped tests (receipt test excluded), control passes, 27 killed.
  - Killed: all 12 verdict.py mutants (gate sign flip, gate seed, gate checks E only, card sha unchecked, premise inverted, 4 seeds, keep with C-vs-S fail, premise from C, I1/I2 swapped, F− gain flipped, stall on C only, F+ fail falls through); 5 run.py mutants (fixture/HCP not rebound, no restore, token regex, target id); 6 sources.py mutants; 4 target.py mutants.
  - **Survivors: C01 (n̄ over all cells), C02 (floor over all cells), C03 (κ = √Q), all in calib.py.**
- Worker mutation results: verification/worker_FU_A_r1/mutation/results.json gives 31/31 killed and control passes (read, not rerun; its harness writes a pinned file).
- C4: a count-only scan of 94 FU-A files (src, tests, scripts, docs, results, worker verification and metadata) found no standalone 6-digit or 16-hex tokens outside the synthetic test literals in tests/topic2_fu_a/test_scripts.py and test_run.py. The only `sub-` token is a 1-letter word. The B300 token scan (token_scan_b300_gate.json) reports 0 hits.
- Layout: whole-run audit_layout.py gives PASS, 428 files, findings [] (verification/reviewer_FU_A_r1_2/layout_lint_run_root.txt).

## 2. Logic Chain
1. F1 is met. The card was frozen (receipt, plus the independent git snapshot at 16:05:25Z) before the gate (16:12:33Z). It reuses the r1 gates, nulls and verdict machinery and states the change, arms E/C/S, 5 seeds, E36, 140k samples, δ = 0.01 and the kill rule. The gate deviation (2 runs instead of 12) is declared in the card before any run, and its consequences are fixed.
2. F2 is met. The code is only in FU-A paths, and the r1 pins pass 33/33. The tests use synthetic fixtures that fail on the targeted defects (r1 voxel stream rejected, rebinding, cell order, noise variance, block mean). The verdict code covers the V06–V10 classes (worker M07, M09, M11, M12; my V03, V12). 58 of 61 combined mutants are killed; the 3 survivors are in pre-freeze calibration code only (see finding 1).
3. F3 is met. Only Slurm GPU use (sacct). 0.952 GPU-h ≤ 8. Ledger start and close rows exist. Records are byte-identical to B300. The result report gives the verdict per card and what it adds to r1 (§5), with a costed plan (§9).
4. Correctness of the outcome: the evaluation path really uses the cell-mean field, the gain is recomputed, and the gate rule applies to seed 0 as frozen. So `inconclusive` follows mechanically, and not running Stage 1 is required by card §7.3, not optional.
5. C1–C8: C1 OK. C2 OK (86 + new suites). C3 OK: no post-freeze deviation needs an addendum (I found none; finding 2 requires one). C4 clean. C5 Slurm and caps OK. C6 HCP public under PI decision 2, nothing per-subject left B300 (the gate is synthetic). C7 no external repo touched. C8: the numbers come from dated outputs.
6. Integrity: no hardcoded results. The verdict is computed from records that are byte-identical to B300, and sacct confirms the jobs. No hidden extra runs (sacct shows only 403, 427 and 507 GPU jobs). Facade code is excluded by my rebinding and source mutants. So there is no integrity violation.

## 3. Caveats
- NF (0.2085) could not be recomputed independently: it needs HCP TRAIN cell means on B300. I relied on job 492 and the frozen-script reproduction (job 510, CPU, logs/b300/design_stats_repro_frozen_script.json). calib.py is unguarded by tests (finding 1).
- I did not rerun any GPU job (0 GPU-h used). Gate determinism across reruns is not established.
- I did not rerun the worker's 31-mutant harness: it overwrites a pinned receipt. I ran my own 30 instead.

## 4. Conclusion
APPROVE. Nonblocking findings, ranked:
1. [Minor, test-coverage] src/topic2_fu_a/calib.py has no direct tests; mutants C01, C02 and C03 survive. The constants are frozen and κ and σ_v were recomputed exactly, so no shipped number is affected. Suggestion: add hand-computed tests for subject_terms, pooled and sigma_v_from_nf.
2. [Minor, factual] Card §7.1 and report §3, §4 and §5.1 call 0.248 the "realized noise share of the fixture". That value is Q_fix pooled over the F+ and F− fixture-train samples. The F+ stream the gate trained on has about 0.22 (measured 0.219–0.221; analytic 0.224). The gate therefore ran closer to the TRAIN NF of 0.209 than reported, which strengthens the "realistic noise" reading. The descriptive "≈30 % of predictable energy" becomes ≈29 %. Fix: dated addendum or erratum; do not edit the frozen card.
3. [Minor, claim scope] Report §5.1 says "a voxel-level F+ gate at HCP noise would almost certainly fail too" and suggests rereading the scope of the r1 stop. This is labelled as inference, but it is speculative. It should stay a hypothesis, costed under §9, and should not be carried into the integrated report as a finding.
4. [Minor, hardening] verdict.index_records checks only fua_target and the card sha. A fixture record run with another σ_v, κ_fix or perm file under the same card would be accepted. The shipped records match the constants (verified), so the verdict is unaffected.
5. [Info] Single-seed gate, declared in the card. At 0.55 % against the r1 seed spread of about ±0.3 %, the outcome is not borderline. A′1 (0.84 GPU-h) is costed.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256 code_sha256_at_freeze output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_a/$f.txt | LC_ALL=C sha256sum -c; done
git show 35d10a5:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md | sha256sum   # 72be3e83…
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_a -q -rs
/home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_A_r1_2/mutants/run_mutants_rv.py   # 27/30, survivors C01-C03
/home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs <tmp>/v.json
```
B300 (read-only): `sacct -j 507 -X`; `sha256sum /scratch/iitp4/fu_a/runs/*/run.json`.
Invalidation: any change to the FU-A card, code or run records, an unreported FU-A GPU job in sacct, or a `g3t-G-E0-*` job overlapping 16:12Z.
