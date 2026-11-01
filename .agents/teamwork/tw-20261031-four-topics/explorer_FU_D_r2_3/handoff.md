# Handoff — explorer_FU_D_r2_3 (FU_D iteration 2, lens: adversarial pre-mortem). Type: Hard.

**Summary.** The r1 gate failed on test coverage, not on science. Every verifier reproduced the shipped verdict (`inconclusive`, F+ gate failed at E192). The fix for r2 is additive only:
- one new test file in `tests/topic2_fu_d/`;
- one dated FU-D addendum with errata;
- one new sha256 receipt.

No frozen file is touched and no GPU is used. I wrote that test file as a probe. It passes on the unmutated code and kills all 14 survivors that the r1 verifiers reported as non-equivalent, including the two blocking ones, X45 and X22. The 3 survivors that the verifiers already called equivalent or redundant (Q08, Q19, Q21) still survive, as expected.

## 1. Observation
- O1. **Receipts.** C1 rc 0. The FU-D receipts all pass: code 29/29, outputs 34/34, card 1/1. `tests/topic2_fu_d/*.py` (12 files) are pinned in `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`. Editing any existing test, helper or src/scripts file therefore breaks that receipt. Adding a new file does not.
- O2. **Shipped verdict.** `scripts/topic2fu_d_verdict.py --wrapper-sha256 <freeze value> --out verification/explorer_FU_D_r2_3/verdict_rerun.json` regenerates the shipped `verdict.json` byte for byte (`cmp`; sha256 f6b295d9…59fc). Without `--out` the script writes into `results/.../verdict.json`, which output_sha256.txt pins (script line `out_p = a.out or os.path.join(a.results, "verdict.json")`).
- O3. **Where δ reaches the code.** `src/topic2_fu_d/verdict.py` does `from .config import DELTA`. That value is the default `delta` argument of `fplus_gate`, `fminus_gate`, `primary_category`, `decide` and `needs_fminus`. The script calls `V.decide(...)` and `V.fplus_gate(...)` without passing δ and writes `"delta": K.DELTA`. The existing tests pass δ explicitly, and their F+ fixtures use large margins (`tests/topic2_fu_d/test_verdict_script.py` gate e=0.70, c=0.66, a 5.7 % gain). So a δ mutant anywhere between the shipped gains (0.36 % and 0.65 %) and 1 % survives the suite, but flips the shipped verdict to `no_verdict` ("seed plan missing").
- O4. **Joint reading.** `JOINT_READING` in the verdict script is a paraphrase of card §9(c) line 97 ("FU-D inconclusive / no_verdict → FU-D adds no decision; the r1 stop stands alone"). No test reads it or compares it with the card.
- O5. **Union of r1 survivors**, from the verifier harness files. Harness ids are given with their source:
  - X22, X35, X37, X45, X49: challenger_1 run_mutants.py;
  - Q03, Q05, Q08, Q09, Q14, Q15, Q16, Q17, Q19, Q20, Q21, Q24: reviewer_1 reviewer_mutants.py;
  - M12, M19, M21: challenger_2 mut/run_mutants.py;
  - A02, A05, A11, A13: auditor heldout_mutants.py;
  - A04: reviewer_2 run_mutants_rev.py.
  - After merging identical edits this leaves 17 distinct mutants (16 reported plus one δ default-argument variant I added). 3 of them were declared equivalent or redundant in r1 (Q08, Q19, Q21).
- O6. **Probe result.** `verification/explorer_FU_D_r2_3/proposed_test_fud_r2_pins.py` (sha256 b33baea5…ad25) has 15 tests and passes on an unmutated copy of the tree (`tree/`, 15 passed in 1.15 s).
  - `run_survivor_mutants.py` applies each mutant to the copy, one file at a time, and restores the bytes afterwards.
  - Result: X45, Q09/M19/A02/A04, the default-argument variant X45b, X22/Q20/A13, X35/Q16, X37, Q14/M21/A11, M12, Q15, Q17, Q03, X49/Q05, A05 and Q24 are all **killed**. Q08, Q19 and Q21 **survive** (equivalent or redundant).
  - Output: `survivor_mutants.out.json` (sha256 52062d7b…bb15).
  - The full copied suite plus the proposal gives 143 passed and 1 failed. The failure is `test_real_ledger_parses_and_r1_worker_total_is_11_73`, which needs `results/gpu_ledger_2026-10-31.md`; I did not copy the ledger into the tree. Nothing else failed.
- O7. **Card-vs-code gaps, from the r1 verifiers, confirmed by reading the code.**
  - G2: when the gate fails, `R.load_runs(..., strict=False)` silently skips unplanned directories. Card §8 line 70 says they are protocol errors.
  - G1: `records.validate_completed` accepts `test_nmse = NaN` because `abs(pooled - nan) > tol` is False.
  - Neither path is reachable on the shipped tree. It holds exactly `Fplus_{C,E,S}_s0`, and loading it with `strict=True` against `all_possible_runs(None)` succeeds (probe test 4). All three test_nmse values are finite and equal Σnum/Σden exactly.
  - The eval masks are not validated by the records, but the sidecar argv carries `--val-mask-seed 7001 --test-mask-seed 7002`, and `test_den` equals the r1 E36 `Fplus_*_s0` records (probe test 5).
- O8. **C4 scanner coverage.** `scripts/topic2fu_d_c4scan.py` PATHS cover results/…fu_d, `verification/worker_FU_D_r1`, the r1 worker's metadata, src/tests and the fu_d docs glob. They do NOT cover any r2 agent's verification or metadata directory. `tests/topic2_fu_d/` is covered, so a new test file there must contain no quoted 16-hex string and no unquoted 16-hex run that contains a letter.
- O9. **Provenance chain.** Each shipped `fud_meta.json` records `fud_code_sha256` (hashes of src/topic2_fu_d) and `wrapper_sha256`. Today these equal the current files and the freeze receipt. Editing src/topic2_fu_d would break that equality for the shipped records.
- O10. **Precedent.** M3 r3 (`docs/.../2026-11-02_topic2_addendum_06.md` and `results/topic2/2026-11-01/addendum_06_sha256.txt`) closed the same class of gate failure. It added one new test file and an errata addendum, and pinned both plus its verification evidence in a new receipt. Existing receipts stayed unchanged.
- O11. **Count-only C4 scan of my own paths.** 197 files, 0 token hits, 1 BIDS-pattern hit: the plain word "sub-cap" in a copy of the repo's r1 `gpu_hours_m3.txt`, not an ID. Whole-run audit_layout: findings [], 542 files. C1 rc 0 and outputs 34/34 at the end.

## 2. Logic chain
1. The gate failed only on challenger_1's X45 and X22 (O3, O4). Each is a "flips if code changed, suite green" gap, not a wrong result (O2). So r2 needs guards, not reruns.
2. Changing src or scripts after the result would break the freeze receipt (O1) and the sidecar provenance (O9). It would also be a post-result code change that verifiers attack as rigging. So the fix must be additive tests (O10 precedent).
3. Pinning `K.DELTA` alone misses the default-argument variant X45b. The guard therefore needs three parts:
   - a constant pin, checked against the card text "δ = 0.01" (card line 68; PI decision 3, which predates every result);
   - signature-default pins on all five functions;
   - a behavioural test with default δ and gains of 0.5 %, which lies inside every mutant window from 0.0036 to 0.005.
   O6 shows these kill both δ variants.
4. A byte-identical regression of the shipped verdict, written to tmp_path (O2), catches every mutation that changes any byte of the shipped output: gains, reason, delta, joint reading, run states. It writes nothing into results/. Its inputs are first checked against output_sha256.txt, so a failure points at the cause.
5. X22 is killed in two ways. The test pins the JOINT_READING table, and it checks that the card §9(c) clauses it paraphrases exist in the frozen card. It also asserts that the inconclusive and no_verdict texts never contain "replicates".
6. The other survivors need negative tests or wrapper tests, which O6 shows work: validator rejections, mean versus median, an injected r1-mapping disagreement, a base path inside `worker_M3_r1`, and an exit code with failed post-checks. That leaves only Q08, Q19 and Q21. Each has a short equivalence or redundancy argument (§4.4).
7. G1 and G2 are real card-vs-code gaps, the class named in the dispatch, but tests cannot kill them without a code change. The honest closure follows the M3 r3 E1 pattern: an erratum, a reading rule, and shipped-tree guards showing that neither could have affected the shipped verdict (O7).

## 3. Caveats
- I ran the 17 mutants against the proposed test file only. Because a suite that contains the proposal fails whenever the proposal fails, that is enough to show kills. I did not run the union of all r1 mutant sets (about 190) against the full suite plus the proposal. The worker should.
- The copied tree omits the ledger, so one existing test fails there (O6). In the real repo it passes, per the r1 reports.
- New r2 verifiers will write new mutants, mostly in Stage-1, F− and seed-plan paths that the shipped data cannot reach. I cannot rule out new survivors there. §4.5 recommends a pre-emptive sweep.
- I used 0 GPU-h. I did not re-check B300 state; three r1 verifiers already re-scored the checkpoints bit-exactly (jobs 574/575/576).
- My copied tree (3.2 MB) stays under `verification/explorer_FU_D_r2_3/tree/` as probe evidence. A delete command was refused by the permission system, so I did not retry it. Root may remove the tree.
- The DISPATCH.md I wrote summarises the roughly 60 KB inline gate JSON instead of copying it, as worker_FU_D_r1 did.

## 4. Conclusion: recommended r2 fix strategy
1. **Scope.** Gate repair only. No GPU, no reruns, no edits to the card, src/topic2_fu_d, scripts/topic2fu_d_*, existing tests/helpers, verdict.json, the result report or any receipt. The verdict stays `inconclusive`. Root or PI owns any further E192 compute; see dead ends.
2. **New test file.** Add exactly one file, `tests/topic2_fu_d/test_fud_r2_guards.py`, adapted from the probe. Keep it fast and unmarked so that every mutation harness runs it. It contains:
   - (a) the δ constant, card text and signature-default pins;
   - (b) a default-δ gate inside the mutant window;
   - (c) the pinned JOINT_READING table, cross-checked against card §9(c);
   - (d) the byte-identical shipped-verdict regression into tmp_path, with input pins checked first and the results bytes unchanged afterwards;
   - (e) the shipped tree is exactly the 3 planned dirs, has no seed plan, loads with `strict=True`, and has finite test_nmse equal to Σnum/Σden;
   - (f) eval masks 7001/7002 in the sidecar argv, and test_den equal to the r1 F+ records;
   - (g) validator rejections: perm_file sha, 15 terms, a 1e-9 NMSE mismatch, missing val steps, sidecar cfg drift;
   - (h) a mean-not-median check, and an injected r1-mapping disagreement that must raise;
   - (i) wrapper checks: a base inside `worker_M3_r1` must be refused, and failed post-checks must give exit code 3.

   Read the wrapper sha from the freeze receipt, not from the current file. Write no 16-hex literals.
3. **Addendum.** Write `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_01.md`, headed post hoc, 0 GPU-h, verdict unchanged. It contains:
   - §1 why: the gate record and X45/X22;
   - §2 errata, each with a reading rule and the shipped-tree evidence:
     - G2: unplanned dirs are skipped when the gate fails;
     - G1: a NaN test_nmse is accepted;
     - eval masks are not record-validated;
     - card §7.1 "+3.06 % / +2.93 %" are the r1 seed-mean gains, not per-seed values;
     - card §0 omits explorer job 418 (0.001 GPU-h);
     - result report §0/§2 "closes it further" rests on n = 1 per scale and is descriptive only; the r1 inter-seed spread of that gain is 0.58 pt;
   - §3 the mutant table: every id, killed or equivalent, with proof;
   - §4 the integrity checks.
4. **Equivalence and redundancy arguments** for the addendum:
   - Q08 assigns plan_n just before a return that does not read it.
   - Q19: `validate_completed` rejects every hcp record whose tokens differ from `exp["test_tokens"]`, so the orders set always has size 1.
   - Q21 rewrites only `failed_pending_rerun` entries that have a record, and such entries always have `rec=None`.
5. **Mutation evidence.**
   - Rerun the 17 ids above against the full suite plus the new file.
   - Then rerun every r1 harness's full list (worker 62, X01–X50, Q01–Q26, M01–M29, A01–A13, reviewer_2's A01–A19) against the new suite, on copies only, never in place. Require 0 non-equivalent survivors.
   - Add a quick automatic sweep (comparison flips, constant changes, `if` → `if False`) over verdict.py, records.py and the verdict script, and classify every survivor as killed, equivalent with proof, or "unreachable on shipped data; covered by a synthetic test".
6. **Receipt.** Write `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt` pinning the addendum, the new test file and the r2 mutation evidence. Run the existing FU-D C4 detector by import over the r2 worker's own verification and metadata dirs and record the result; the frozen PATHS miss them (O8). Do not make the test suite scan directories that other agents write into, because that makes it non-hermetic.
7. **Checks.** Before handoff run:
   - C1;
   - all FU-D receipts (card 1/1, code 29/29, outputs 34/34);
   - r1 receipts (code 33/33, output_sha256_r2) and addendum_06;
   - `tests/topic2_fu_d` (129 + new) and the old 86 suite;
   - the C4 scan;
   - audit_layout;
   - `cmp` of the shipped verdict.json against a fresh `--out` regeneration.

## 5. Verification method
- `cd /home/juke/git/00IITP-AI/verification/explorer_FU_D_r2_3/tree && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=$PWD timeout 900 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d/test_r2_pins_proposed.py -q` → 15 passed.
- `cd /home/juke/git/00IITP-AI/verification/explorer_FU_D_r2_3 && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 run_survivor_mutants.py` → 14 killed; Q08, Q19, Q21 survive.
- `cd /home/juke/git/00IITP-AI && W=$(awk '$2=="scripts/topic2fu_d_train.py"{print $1}' results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt) && python3 scripts/topic2fu_d_verdict.py --wrapper-sha256 $W --out /tmp/claude-1000/v.json && cmp /tmp/claude-1000/v.json results/topic2/2026-11-02_fu_d/verdict.json`
- What would invalidate this: any FU-D receipt failing; the byte regression differing (meaning a pinned input changed, e.g. r1 verdict.json, which the script reads for r1_reference); an r2 verifier finding a reachable survivor among the 17 ids.
