# Handoff (Hard) — reviewer_M2H2_r2_1, M2H2 r2 gate (Topic 3 H2 random-init control, iteration 2)
Written 2026-11-01T21:12Z. Parent: root coordinator 5fddb83e. Verdict: **APPROVE** (no blocking issues).

## 1. Observation
All probes/logs in /home/juke/git/00IITP-AI/verification/reviewer_M2H2_r2_1/.
- O1 C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` rc 0 at start (20:03Z, 67 OK; logs/../c1_start.log) and end (21:11Z; logs/c1_end.log).
- O2 Receipts: results/topic3/2026-11-02_h2/output_sha256.txt (61) rc 0; addendum_07_sha256.txt rc 0; r2/addendum_08_sha256.txt rc 0 (5 OK; covers addendum 08 3bb27032… and the 4 new tests); 2026-10-31 addendum_02..06 + output_sha256 rc 0; card_sha256.txt rc 1 (known trailing "frozen" token; hash 683374565d80… equals the card) and code_sha256_at_freeze.txt rc 1 (known, addendum 01) — both pre-existing.
- O3 Tests (my runs): tests/topic3_h2 167 passed, 0 skipped (200 s; logs/pytest_topic3_h2.log); old suite STRICT_E2E=1 (tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e) 86 passed; tests/topic3_spectral 138 passed; tests/topic1_lagmotif 88 passed.
- O4 Freeze order (H1′): addendum 07 sha 09b45220… frozen 15:57:40Z; checkpoint commit 35d10a5 (16:05:25Z) holds identical bytes; gate job record started 16:22:21Z, random job 16:32:21Z.
- O5 Gate (H2′): gate_record G1 399 windows all_pass (max rel_fro 7.8e-7 vs tol 1e-5), G5 three controls all fail G1, gate_decision PASS with G1–G5 ok; random_record 10 distinct seed hashes, none = trained, rebuild identical.
- O6 Independent label recheck (recheck_labels.py, own §6 transcription, own Holm/stability arithmetic): 0/24 label mismatches; T subject-level A1 reproduces pinned Family A exactly (5.343854531110546 / 6.038808669990018); δ-sensitivity transitions C1 0.158/1.018, C2 0.4585/1.1115, C3 0.5485/1.2915, C4 0.664/1.206 (grid 0.0005) = addendum 08 E1; single-seed labels (E8) C1 EQ s1,5,8 / TE+ s4,7,9,10 / INC s2,3,6, C2 TE+ s4,5,7,9,10, C3/C4 TE+ all = addendum 08; random D1 cov per seed 0.06–0.42, mean 0.255; E2 (−1.61 [−3.77,+0.56], −0.74 [−3.18,+1.71]) and E3 (L0 subject INC numbers) match h2_results.json.
- O7 Union evidence: union_mutants.out.json (sha 2f38f617…) tallies 115/115 KILLED by extended suite, 37 r1 survivors SURVIVED shipped 8-file suite and KILLED by new files alone, all restored; baselines 71 / 167 passed. Spot reproduction (spot_r1_survivors.py, copied tree): baseline 43 passed; N26 killed by test_h2r2_family_oracle.py alone (3 failed); N53 killed by regression+guards alone (3 failed).
- O8 Novel mutants (novel_mutants.py, 46 edits not in the union, FULL extended suite, copied trees, baselines 167 passed ×2, production h2_results/gate_decision unchanged, all restored; out.json sha 515364c7…): 34 KILLED, 12 SURVIVED.
  - Killed: all 14 h2stats verdict-path edits (Holm p swapped/sorted, C4 with C3 δ, pooled subject seed effects, CI95 seed, G8 map, R1 pair, D1 corr robust, token-level seed, decide guards, Family L subject estimator, EQ-before-TE); 11/13 stats-script edits (G1 all_pass, G2/G4/G5 forced ok, TF32 one-on, seed subset, rebuild check, trained hash vs keys, positions length-only, R0-vs-T abs, LN0L2 perturbed); comparator K02–K05; reduce Q03; driver J02, J03, J04, J08.
  - Survived: S01 `_dump` BIDS-prefix guard disabled; S08 T-A1 reproduction tolerance 1e-9→1e-3; K01 zero-norm stored dump passes G1; K06 shape-mismatch cell keeps ok; Q01 e1_full corr computed as cov; Q02 α q25↔q75; driver J01 G2 row-order ignored, J05 G4 ignores ckpt sha, J06 rebuild flag trivially True, J07 seed-distinct flag trivially True, J09 gate contrast seed stride, J10 in-job G1 ok forced True.
- O9 Ledger: prev snapshot (sha 9f9843eb…) is a byte prefix of the current ledger (append-only); correction rows for 218063/218064 present; M2H2 total 0.458+0.058+0.303 = 0.819 GPU-h ≤ 6.
- O10 Governance: no "sub-" bytes in results/topic3/2026-11-02_h2/; 6-digit hits in new files are Slurm job ids only; synthetic "sub-SYN" names in a test are in-memory. Layout lint PASS, 571 files, findings [] (logs/audit_layout.log). No src/topic3_h2, scripts/topic3h2_*, or shipped test file changed during the review.

## 2. Logic Chain
1. O4+O5 → H1′ and H2′ hold (freeze before any random-init result; replication gate PASS before random arm).
2. O3+O6 → H3′ holds numerically: tests pass, shipped labels follow from the shipped outputs under the frozen rule; errata E1–E3, E8 in addendum 08 are numerically correct.
3. O7+O8 → the r1 blocking class (verdict-path wiring and stats-script guards untested) is closed: every r1 survivor is killed with attributable kills, and 25/25 novel edits on the verdict path / label-bearing stats-script code are killed. Surviving novel edits are (a) job-side in-job flag construction in driver.py/compare.py that only matters on a future GPU rerun (same "driver job path" class r1 called nonblocking; for the shipped run O5 and five r1 GPU reruns refute them), (b) descriptive-only outputs (E1/α), (c) a near-equivalent tolerance (S08), (d) a defensive C4 guard (S01) whose target condition is independently verified absent (O10).
4. O1+O2+O3+O9+O10 → no regression, no C1/C4 breach, ledger append-only, no integrity concern (tests run the code under test from the tree under test; oracle is independent numpy; regression compares behaviour not hashes).

## 3. Caveats
- No GPU rerun (0 GPU-h): the r2 change is tests-only and five r1 verifier reruns (seeds 1,3,4,7,8) already reproduce the random arms; driver runtime paths rest on that evidence.
- The worker-proposed gate scope (addendum 08 §7) and δ (addendum 08 §8) are not PI-confirmed; I judged novel survivors nonblocking by analogy to PI decision 6, which root/PI may overrule.
- Tests were written after results (regression guards, not pre-registration) — disclosed.
- I did not rerun the 6265 s union harness; I verified its output and reproduced the two label-flipping kills.

## 4. Conclusion
APPROVE M2H2 r2. Blocking: none. Nonblocking: (1) PI to confirm δ (C3 TE+ holds only for f ≤ 0.548) and the r2 gate scope; (2) driver/compare job-side guard gaps J01, J05, J06, J07, J09, J10, K01, K06 — add offline tests before any GPU rerun of H2; (3) S01 BIDS-prefix guard in scripts/topic3h2_stats.py `_dump` untested; (4) Q01/Q02 descriptive E1/α job reductions untested; (5) S08 tolerance untested (near-equivalent); (6) result report §4 R1 bullet ("at least as large") is a point-estimate statement — integrated report should use E2 wording; (7) integrated R1 report must quote addendum 08 errata E1–E8; (8) addendum 08 lives in results/…/r2/, root may copy byte-identically to docs/; (9) connectome dirs and local probe trees / src/topic3_h2/__pycache__ cleanup left to root.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt results/topic3/2026-11-02_h2/r2/addendum_08_sha256.txt
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. nice timeout 900 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic3_h2   # 167 passed
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M2H2_r2_1/recheck_labels.py   # mismatches []
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M2H2_r2_1/spot_r1_survivors.py   # N26, N53 rc 1
# novel mutants (~55 min, detached; requires verification/reviewer_M2H2_r2_1/trees absent; overwrites novel_mutants.out.json):
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 setsid nohup nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M2H2_r2_1/novel_mutants.py > verification/reviewer_M2H2_r2_1/logs/novel_mutants.log 2>&1 &
```
Invalidation: any change to a file in output_sha256.txt / addendum_08_sha256.txt; a union mutant surviving the extended suite; a verdict-path novel mutant surviving; label mismatch in recheck_labels.out.json.
