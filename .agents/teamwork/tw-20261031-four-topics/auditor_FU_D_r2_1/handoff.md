# Handoff — auditor_FU_D_r2_1 (forensic audit, FU_D iteration 2) — Hard handoff

## Forensic Audit Report
**Work Product**: FU_D r2 gate repair by worker_FU_D_r2 — tests/topic2_fu_d/test_fud_r2_guards.py, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_01.md, results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt, verification/worker_FU_D_r2/** — plus the frozen FU-D artifacts it relies on.
**Profile**: General Project. Integrity mode inferred as Development (ORIGINAL_REQUEST has no from-scratch / no-delegation constraint).
**Verdict**: CLEAN

### Phase Results
- C1 protected hashes: PASS. rc 0, 67/67 OK, at start and at end.
- FU-D receipts: PASS. card 1/1, code_sha256_at_freeze 29/29, output 34/34, addendum_01 23/23, 0 non-OK at start and at end. verdict.json sha f6b295d9…59fc is unchanged.
- Hardcoded results / self-certifying tests: PASS.
  - The new test file pins card values as literals: δ, the §9(c) strings, the shipped gains and reason.
  - It also has an independent exact-fraction oracle computed from the raw num/den.
  - The card-literal tests check the card text itself, for example "δ = 0.01" and the 4 joint-reading clauses.
  - There is no skip, xfail or importorskip.
- Facades: PASS. No production code was added or changed. The 29 frozen files match their receipt.
- Tests can fail: PASS. My own 20-mutant probe ran on a copied tree against the final suite: 19 killed. These include X45-type δ changes (constant, decide default, script early-gate δ), X22-type joint-reading changes, and gate and/or, gain denominator, tolerance, post-checks, token regex, mask seed, floor, s1present, order check, F− boundary, JSON indent, wrapper sha, stall threshold and reason text. The one survivor, P19, replaces `K.DELTA` with the literal 0.01, which is the same value, so it is equivalent.
- Mutation evidence authentic: PASS.
  - union.out.json is internally consistent: 423 results, 404 KILLED (all rc 1, each with a FAILED line) and 19 SURVIVED. The 121 output-changing mutants are all KILLED. The median run is 13.6 s and the total 4896 s, which matches the ~82 min claim.
  - The base tree is copied once at the start, so the mid-run test edits did not leak into run 1.
  - I reran the 19-survivor run with the worker's harness and got the same result: 11 killed, 8 survive.
- Equivalence proofs (Q08, Q19/S207, Q21, S023/S025, S160, S181): PASS. I checked each against the frozen code:
  - Q08: a dead assignment after `return`.
  - Q19/S207: `validate_completed` forces the token order to equal the split order.
  - Q21: a `failed_pending_rerun` entry always has `rec` = None.
  - S023/S025: keep ⇔ the "(keep pending F-)" reason when F− is missing.
  - S160: `parse_dir` allows only attempts 0 and 1, and "rerun of a completed run" raises first.
  - S181: the absent/incomplete distinction is not read by `decide` and is not written to the output.
- Verdict reproducible: PASS. My regeneration is byte-identical to the shipped verdict.json. Exact fractions give (E−C)/E = 0.003631 and (S−C)/S = 0.006546, both < 1/100, so the verdict is inconclusive.
- Erratum numbers: PASS.
  - W1: the r1 per-seed gains are 2.772/3.348 % and 2.900/2.970 %, with means 3.06/2.93 %.
  - W2: job 418 (0.001 GPU-h) is in the ledger, and 0.03 + 0.03 + 0.036 + 0.001 = 0.097.
- Results before card freeze: N/A for r2 (no new results). The r1 ordering is card 16:06Z, then the first real-data job at 16:39Z.
- Silent fallbacks: none were introduced. The frozen-code gaps E1–E4 are disclosed with reading rules, and shipped-data invariants pin the shipped inputs outside them.
- C4 participant IDs: PASS.
  - 29 r2 files: 0 standalone 6-digit tokens and 0 `sub-` labels.
  - All 25 distinct 64-hex strings are known repo file or receipt hashes.
  - Both daemon-committed versions of the addendum: 0 hits.
  - Tests use only positional hNN tokens.
- Writes outside ownership: PASS. The repo files modified in the r2 window (04:59–06:52 KST) are exactly the declared r2 files. Other matches are other teams' own paths or reviewer copies under their own verification dirs.
- GPU: PASS. B300 sacct is cluster-wide: the last FU-D job (576) ended 19:34Z, before r2 started at 19:59Z. /scratch/iitp4/fu_d is unchanged since 04:10 KST. The ledger has no r2 rows. The FU-D total is about 3.7 GPU-h against a cap of 25.
- Git writes by agents: PASS. The only commits in the window are by "Chavis Autocommit" (`docs(auto)`, .md only). No .py, .json or receipt file from r2 is tracked.
- Layout: PASS. Whole-run audit_layout status PASS, 647 files, findings [].

## 1. Observation
- verification/auditor_FU_D_r2_1/c1.out: 67 lines, all OK. The receipt loop returned 0 non-OK, twice.
- pytest (STRICT_E2E=1, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, PYTHONPATH=.):
  - tests/topic2_fu_d: "195 passed, 2 warnings in 53.17s" (pytest_fud.out).
  - Old suite: "86 passed" (pytest_old86.out).
- probe_mutants.log: CTRL SURVIVED with 189 passed; P01–P18 and P20 KILLED; P19 SURVIVED.
- rerun19.log summary: {"n": 19, "killed": 11, "survived": [S023, S025, S160, S181, S207, U064, U075, U077]}.
- regen_verdict.json sha256 is f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc, the same as the shipped file.
- B300 sacct: jobs 574/575/576 (FU-D r1 verifiers) ended by 04:34 KST. No FU-D job after that.
- `git log --since 19:55Z`: 8 commits, all by Chavis Autocommit.

## 2. Logic Chain
1. The receipts and C1 are intact, so nothing frozen or protected was edited (Obs: c1, receipts).
2. The new tests fail on targeted defects, shown by independent mutants that I designed and that are not in the worker's lists. So they are not facades and not tautological as a whole (Obs: probe).
3. The worker's mutation logs are internally consistent and reproducible, and its survivor rerun reproduces exactly. So the evidence is not fabricated (Obs: union.out.json checks, rerun19).
4. The shipped verdict regenerates byte-identically, and an independent exact recomputation agrees. So the result is real and unchanged (Obs: regen).
5. There are no ID tokens, no GPU use, no out-of-ownership writes and no agent git writes. So there is no C4, C5 or C7 violation.
6. Therefore none of the prohibited patterns is observed: the verdict is CLEAN.

## 3. Caveats
- No snapshot of the 50-test version used in run 1 was kept. The claim that tests were only added between run 1 and the final file cannot be checked byte for byte. My independent probe against the final file mitigates this.
- Some assertions in `test_joint_reading_literals_follow_the_frozen_card_clauses` are self-referential: they check the test's own JOINT literal. The meaningful guards are the card-text checks and the table-equality test. This is nonblocking.
- The worker's disclosed deviation of 3 concurrent pytest processes for about 4 s is a procedural resource rule, not an integrity matter.
- Out of FU-D scope: some receipts of other milestones currently report mismatches when checked naively from the repo root. Examples: results/topic2/2026-11-02_fu_c/output_sha256.txt 6/160, results/topic2/2026-11-02_fu_b/card_sha256.txt 1, results/topic2/2026-11-01/output_sha256.txt 17 (superseded by output_sha256_r2.txt), topic3 code_sha256_at_freeze 1, topic4 output 1. No FU-D or r2 file is involved. Root should route these to the owners.
- I did not re-run the full 423-mutant union, and I did not re-examine the r1 training records on B300; r1 verifiers re-scored the checkpoints.

## 4. Conclusion
CLEAN. FU_D iteration 2 is an additive, test-and-addendum-only repair with genuine, failing-capable tests and authentic, reproducible mutation evidence. The shipped verdict `inconclusive` (measurement capacity) is unchanged and reproducible. It used 0 GPU-h, touched no protected or frozen file, leaked no IDs and made no agent git writes.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- `for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt addendum_01_sha256.txt; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done` → 0 each
- `python3 verification/auditor_FU_D_r2_1/probe_mutants.py /home/juke/git/00IITP-AI <work> <out.json>` → 19/20 killed, P19 equivalent
- `python3 verification/worker_FU_D_r2/mutation/run_union.py /home/juke/git/00IITP-AI <work> <out> verification/worker_FU_D_r2/mutation/survivors_r1.json verification/worker_FU_D_r2/mutation/empty_sweep.json` → 11 killed, 8 survive
- `PYTHONPATH=. python3 scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989b…b84e --out <tmp>` and then `cmp` with results/topic2/2026-11-02_fu_d/verdict.json
- Invalidation: any receipt mismatch, a non-equivalent survivor found by a new mutant, or an FU-D sacct job or ledger row dated after 19:59Z attributed to r2.
