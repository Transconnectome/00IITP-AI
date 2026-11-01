# Handoff (Hard) — explorer_FU_D_r2_1, FU_D iteration 2, lens: scientific design and falsifiability

**Summary.** The r1 science holds. The only blocking defect is in the tests: no test pins the decision constant δ (X45) or the shipped joint reading (X22). The verdict, the card and the runs need no change.

The fix is purely additive:
- one new test file;
- one dated FU-D addendum (`2026-11-02_topic2_fu_d_addendum_01.md`) with errata for the latent card-vs-code gaps;
- a new receipt, `addendum_01_sha256.txt`;
- a union mutation run over every verifier's mutant set.

No rerun is needed and no GPU is used.

I wrote a proposed test file and ran it against 13 mutants. All 13 survive the current suite (124 passed each) and all 13 are killed by the proposed file. The baseline is valid: 124 passed and 22 passed.

## 1. Observation

- **Gate record (inline in the dispatch).** challenger_FU_D_r1_1 returned REFUTED with two blocking items:
  - **X45:** `src/topic2_fu_d/config.py` `DELTA = 0.01 → 0.0036` gives the shipped verdict `no_verdict` with the suite green.
  - **X22:** in `scripts/topic2fu_d_verdict.py`, `JOINT_READING["inconclusive"]` changed to "null replicates at E192", with the suite green.
  - The other 4 verifiers passed (APPROVE, APPROVE, CONFIRMED, CLEAN), and all 5 reproduced `inconclusive`.
  - Nonblocking survivors across the verifiers:
    - X35/Q16: perm_file check removed;
    - X37 and M21/Q14/A11: 16-term check;
    - M12: tolerance 1e-12 → 1e-3;
    - Q15: val-curve steps;
    - Q17: sidecar cfg dict;
    - Q03: mean → median;
    - Q05/X49: r1-agreement assert;
    - Q24: wrapper exit code;
    - A05: near-equivalent;
    - Q08 and Q21: equivalent;
    - Q19: redundant.
  - Defects G1 and G2 from challenger_FU_D_r1_2.
- **Frozen inputs.** Card sha `1b7fee6c…6001b`. Its §13 pins "every file under `src/topic2_fu_d/`, `scripts/topic2fu_d_*.py` and `tests/topic2_fu_d/`" in `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt` (29 files). The card header says later changes go in `2026-11-02_topic2_fu_d_addendum_NN.md`.
- **Shipped `verdict.json`.**
  - `decision.fplus_gate` = {gain_C_vs_E 0.0036313292621888414, gain_C_vs_S 0.006546018163682844, pass false};
  - verdict `inconclusive`;
  - joint reading "E192 adds no decision; the r1 E36 stop stands alone";
  - seed_plan null; needs_fminus false.
  - The runs directory holds only `Fplus_{E,C,S}_s0`.
- **Gate wiring.** The verdict script calls `V.fplus_gate(...)` with the default `delta = DELTA` from config.py (verdict.py `def fplus_gate(nmse, delta=DELTA)`). So δ in config.py is decision-relevant on the shipped path.
- **Existing tests.** No test asserts `K.DELTA == 0.01`, the shipped verdict.json, or the JOINT_READING table. `tests/topic2_fu_d/test_verdict_script.py` checks the reading only for `stop` and `keep` (prefix match).
- **Verifier harnesses.**
  - The worker, both reviewers, challenger_2 and the auditor copy and run the whole `tests/topic2_fu_d` directory, except test_e192_model.
  - challenger_FU_D_r1_1's harness runs an explicit list of 8 test files (`run_mutants.py` TESTS), so a new file is invisible to it unless it is re-run with the new file added.
- **Probe 1** `verification/explorer_FU_D_r2_1/probe_mutants_a01.py` → `probe_mutants_a01.out.json` (sha `5f9b2232…`).
  - Each mutant runs on a fresh copy, with the proposed file placed at `tests/topic2_fu_d/test_shipped_verdict_a01.py`.
  - Baseline: old suite 124 passed; proposed file 22 passed; shipped verdict `inconclusive`.
  - Results:

| mutant (r1 ids) | old suite | proposed file | shipped verdict / reading under the mutant |
|---|---|---|---|
| X45 δ 0.0036 | SURVIVED | KILLED | **no_verdict** (flips) |
| Q09/A04/A02/M19 δ 0.003 | SURVIVED | KILLED | **no_verdict** (flips) |
| δ 0.02 (upward) | SURVIVED | KILLED | inconclusive |
| X22/Q20/A13 inconclusive text | SURVIVED | KILLED | reading **"null replicates at E192"** (flips) |
| no_verdict text | SURVIVED | KILLED | unchanged |
| X35/Q16, X37, M21/Q14/A11, M12, Q15, Q17, Q03, Q05/X49 | SURVIVED (all) | KILLED (all) | unchanged |

  - Attempt 1 had an invalid baseline: the copy lacked `docs/…/2026-11-02_topic2_fu_d_*`, so `test_c4_outputs.py::test_scan_covers_the_fud_paths` failed. I stopped my own process (PID 700048) and kept the log as `probe_mutants_a01_attempt1_invalid_baseline.log`. I fixed the copy and reran.
- **Probe 2** `probe_g1_g2.py` → `.out.json` confirms both latent defects in frozen code:
  - G1: `validate_completed` accepts `test_nmse = NaN`, because `abs(pooled − nan) > tol` is False.
  - G2: `load_runs(..., strict=False)` on the gate path silently ignores `junk_dir` and `Fplus_C_s1`. Card §8 says unplanned directories are protocol errors. Also, `tests/topic2_fu_d/test_records.py::test_non_strict_skips_unplanned_dirs` asserts this skipping as intended behaviour.
- **Shipped-data invariants** (they pass on the real tree and sit in the proposed file):
  - the shipped runs dir equals exactly the 3 planned names;
  - every value in the shipped records is finite: 16 terms, and test_nmse = Σnum/Σden exactly;
  - the sidecar argv has `--val-mask-seed 7001 --test-mask-seed 7002 --steps 8750`;
  - `test_den` is identical to the r1 E36 `Fplus_*_s0` test_den. records.py does not check the eval mask seeds; challenger_2 flagged this.
- **Descriptive context.**
  - r1 E36 F+ NMSE: seed 0 E 0.67693, C 0.65817, S 0.67783; seed 1 E 0.68030, C 0.65752, S 0.67765.
  - E192 seed 0: E 0.65585, C 0.65347, S 0.65777.
  - So C is nearly unchanged across scale, while E improves about 3 %.
- **Integrity at end.** C1 rc 0; FU-D card, code and output receipts OK; whole-run `audit_layout.py`: 543 files, findings [] (`verification/explorer_FU_D_r2_1/audit_layout.out`). 0 GPU-h, no git writes, no IDs, none of my processes left.

## 2. Logic chain

1. **The decision rule needs no change.** All five r1 verifiers reproduced the gate gains (0.363 % and 0.655 %, both < δ). Three of them re-scored the checkpoints bit-exactly on GPU. So the verdict `inconclusive` (card §8 step 2) is correct, and the card's decision rule needs no change.
2. **The failure class is "flip if code changed".** The shipped decision depends on a constant (δ) and on a text table that no test pins. Probe 1 shows that δ 0.0036 or 0.003 flips the shipped verdict to `no_verdict`, and the inconclusive text mutant flips the scientific reading, all with 124 tests green. M2 r3 and M3 r2 failed their gates on the same class. Falsifiability argument: a verdict is only as falsifiable as the tests that would detect a change in its decision inputs. The kill rule, δ and the reading must be pinned by literals, not by comparing the code with itself.
3. **Additive tests are the fix, and they are sufficient.** The tests write the card values as literals:
   - `K.DELTA == 0.01`;
   - an exact-fraction oracle on the shipped per-group terms with δ = 1/100;
   - a deep-equality regression of the script's output on a tmp copy of the shipped records against the pinned `verdict.json`;
   - the exact five-entry JOINT_READING table.

   They kill X45, X22 and every listed survivor (Probe 1). The δ-band tests (0.36 %, 0.99 %, 1.01 %, 2 %) also kill δ mutants in either direction.
4. **The new file belongs inside `tests/topic2_fu_d/`, not in a new directory.**
   - Five of the six r1 harnesses run that directory, so the same tools that found the defect see the fix.
   - The only cost is that the card §13 file set (29 files at freeze) no longer equals the directory listing. The addendum records this: "freeze set ∪ addendum_01 set == files on disk". addendum_01_sha256.txt pins the new file. M3 r3 used the same precedent (`tests/topic2_rgpool/test_verdict_path_guards_r3.py` plus `addendum_06_sha256.txt`, gate- and victory-accepted).
   - The existing receipts stay valid (`sha256sum -c` checks the listed files only).
5. **G1 and G2 must not be fixed in frozen code.** They are real departures from card §8 ("records violating the pins… unplanned directories… are protocol errors"). A code change after the result would be a post-hoc analysis change. On the shipped inputs neither is reachable: the records are finite and there is no unplanned directory. The scientifically correct handling is therefore:
   - (a) errata in addendum 01 (card governs; code departs in latent cases);
   - (b) shipped-data invariant tests that would fail if the shipped inputs ever entered either defect domain.

   A test asserting "NaN is rejected" would fail on frozen code. Marking it xfail would hide a defect, which the rules forbid.
6. **Wording errors in frozen documents go into addendum 01, not into edits.** None changes a category:
   - Card §7.1: "+3.06 % / +2.93 %" are the r1 2-seed means of the C-vs-E and C-vs-S gains (per seed C-vs-E 2.772/3.348 %, C-vs-S 2.900/2.970 %), not "both F+ seeds".
   - Card §0: the explorer job list omits 418 (0.001 GPU-h), which is included in the 0.097 total.
   - Report §0/§2: "the gain shrinks with scale… a larger model closes it further" rests on n = 1 seed per scale. The E192 gain (+0.36 %) lies 2.41 points below the E36 seed-0 value, against an E36 inter-seed spread of 0.58 points. So the direction of a scale effect is suggested, not estimated: no interval exists.

   The addendum should state the reading rule: "descriptive, one seed per scale; no scale trend is claimed".
7. **No further GPU work is in scope.** Running F+ seeds 1–2 now (≈7.1 GPU-h) would be gate-shopping: a re-test chosen after seeing the gate fail, with no pre-registered combination rule. Running Stage 1 anyway (D′) is forbidden by the card. Either needs a new card and a PI decision (report §5). "Completion" under the root interpretation (ORIGINAL_REQUEST steering) means a gated, victory-audited verdict. `inconclusive` is a legitimate pre-registered terminal verdict.
8. **What the gate failure means scientifically.** "Measurement capacity" is the conservative label, and it is correct. The F+ gate cannot tell "the apparatus cannot detect a δ-sized grouping benefit at E192" apart from "M0 grouping genuinely stops mattering at E192". In both cases a Stage-1 `stop` would be uninterpretable. The addendum should not upgrade this into a mechanistic claim; report §2 already labels it "not tested".

## 3. Caveats

- I ran only the 13 decision-relevant survivors, not the full union of about 199 mutants from all six r1 harnesses. The worker must run the union (see the verification method). Fast-suite cost measured here is about 7–13 s per mutant, so the union takes about 25–45 min serial, or less with 2 workers.
- I did not write a test for Q24 (wrapper exit code ignores post-checks). It needs monkeypatching the frozen-script import inside `main()`. It is unreachable for the verdict, because records reject `post_checks_ok != True` (records.py). The worker may add it or document it as unreachable.
- Equivalence and redundancy of Q08, Q21 and Q19, and the near-equivalence of A05, are taken from the r1 verifiers' reports. I did not re-prove them; the addendum needs a one-line proof for each.
- explorer_FU_D_r2_2 is running its own probes in parallel (its PIDs, not mine). I did not read its outputs; this report is independent.
- The proposed test hard-codes the wrapper sha d598989b… and the five reading strings as they were shipped. Card §9(c) is paraphrased in the code, not quoted. The pin is to the shipped text, plus semantic checks ("adds no decision", "r1 E36 stop stands alone", no "replicates" for inconclusive or no_verdict).

## 4. Conclusion (recommended fix strategy for worker_FU_D_r2)

1. **Do not change** the card, the 29 frozen code files, the runs, verdict.json, the result report or any receipt. Do not rerun. Use 0 GPU-h.
2. **Add `tests/topic2_fu_d/test_shipped_verdict_a01.py`.** Start from `verification/explorer_FU_D_r2_1/proposed_test_shipped_verdict_a01.py` (22 tests; sha `8bcbe61e…`). The tests:
   - pin δ;
   - check the δ band at the function and script level;
   - run the shipped-verdict deep regression on a tmp copy (`--out` in tmp, never into results/);
   - run an exact-fraction oracle with a literal δ;
   - check the exact JOINT_READING table;
   - check the G1/G2/eval-mask shipped invariants;
   - check record guards: perm file, 15/17/1 terms, 1e-9 nmse offset, missing val step, sidecar cfg dict;
   - check mean versus median;
   - check that the r1-agreement assert fires.
3. **Write `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_01.md`** (post hoc, verdict unchanged) with these sections:
   - why it exists (the r1 gate record);
   - errata, card governs:
     - G1: NaN accepted;
     - G2: unplanned directories skipped on the gate path, and `test_non_strict_skips_unplanned_dirs` encodes that departure;
     - eval mask seeds not validated by records.py;
   - wording errata: card §7.1, card §0 job 418, and the report §0/§2 single-seed reading rule;
   - the new test file and its kill list;
   - one-line proofs for the equivalent/redundant mutants (Q08, Q21, Q19, A05, Q24 unreachable);
   - mutation evidence;
   - no-regression evidence;
   - file-set note: card §13 freeze set ∪ addendum_01 set == files under tests/topic2_fu_d.
4. **Write the receipt `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`.** It pins the addendum, the new test file and the mutation and union evidence.
5. **Union mutation evidence.** Run every mutant list from the six r1 harnesses:
   - worker 62;
   - reviewer_1 26, plus control C00;
   - reviewer_2 19;
   - challenger_1 50;
   - challenger_2 29;
   - auditor 13.

   Read the lists read-only and do not edit others' scripts. Run each on a fresh copy that includes `docs/…/2026-11-02_topic2_fu_d_*`, `results/topic2/2026-11-01`, `results/topic2/2026-11-02_fu_d` and the ledger; copy them, do not symlink, so a mutant cannot write into results. The suite is the whole `tests/topic2_fu_d` with the new file, minus test_e192_model. For every mutant, also record the shipped verdict, reason, gains and joint reading on the copy.

   Gate criterion: 0 surviving mutants that change any shipped decision output. Every other survivor must be killed or proven equivalent or unreachable in the addendum. Baseline must be green; any timeout or OOM is invalid and must be rerun.
6. **No regression.** Check:
   - C1;
   - all FU-D receipts (1/1, 29/29, 34/34) plus the new receipt;
   - the r1 freeze (33/33);
   - tests/topic2_fu_d in full (129 + new);
   - old suite 86; tests/topic1_lagmotif;
   - the C4 scan over the new files;
   - whole-run audit_layout;
   - shipped verdict.json sha still `f6b295d9…`.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
# proposed tests pass on the real tree (22 passed)
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=$PWD timeout 900 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q verification/explorer_FU_D_r2_1/proposed_test_shipped_verdict_a01.py
# survivors reproduce on the old suite and die on the proposed file (≈4 min; writes probe_mutants_a01.out.json)
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r2_1/probe_mutants_a01.py /tmp/x.json
# latent defects G1/G2 present in frozen code
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r2_1/probe_g1_g2.py
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-02_fu_d/output_sha256.txt | LC_ALL=C sha256sum -c
```

**Invalidation conditions.**
- Any of the 13 mutants survives the proposed file.
- The baseline of the old suite is not green in the copy.
- The shipped verdict.json no longer matches its output receipt.
- A union mutant that changes the shipped outputs survives the final suite.
