# Handoff — explorer_FU_D_r2_2 (FU_D iteration 2; lens: feasibility and failure modes) — Hard

**Summary.** The r1 gate failed only because the shipped FU-D suite does not pin the decision constant δ or the shipped verdict and joint-reading text (X45, X22). The science result is not in question. I wrote one proposed test file as a probe. A clean copy passes it (136 passed). It kills all 22 probe mutants: 18 of them survive the shipped suite, 4 do not. The 22 are the r1 verifier survivors plus 10 of my own, which reach the same flip through other code paths. The two remaining gaps (G1: a NaN test_nmse is accepted; G2: unplanned directories are ignored when the gate fails) are real code-vs-card deviations in frozen code. Additive tests cannot close them in code. The fix is an erratum in a dated addendum, plus guards on the shipped data. No GPU and no rerun are needed.

## 1. Observation
- Receipts at start and end: C1 rc 0. FU-D card 1/1, code 29/29, outputs 34/34. r1 freeze OK. audit_layout PASS, findings [].
- `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt` pins all 12 files under `tests/topic2_fu_d/` as well as src and scripts. `output_sha256.txt` line 34 pins `verdict.json` and line 35 pins `docs/.../2026-11-02_topic2_fu_d_result_report.md`. So the result report cannot be edited; wording fixes go in an addendum.
- Card line 3: later changes go in `2026-11-02_topic2_fu_d_addendum_NN.md`. Card §8: "Unplanned directories … are protocol errors (the verdict script stops)."
- Rerunning `scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989b… --out verification/explorer_FU_D_r2_2/verdict_rerun.json` takes 0.5 s, and its output is byte-identical to the shipped verdict.json (sha256 f6b295d9…59fc).
- `src/topic2_fu_d/verdict.py`: `fplus_gate`, `fminus_gate`, `primary_category`, `decide` and `needs_fminus` all default `delta = DELTA` from config. The script calls `V.decide(...)` without δ, and it computes `gate_failed` a second time, early, through `V.fplus_gate(...)` with its default.
- `records.validate_completed`: `if not math.isfinite(pooled) or abs(pooled - rec["test_nmse"]) > tol`. A NaN `test_nmse` passes, because `abs(x - nan) > tol` is False. The script loads the gate with `load_runs(..., strict=False)`, which silently skips unplanned directories.
- **Probe 1: mutation run** (`verification/explorer_FU_D_r2_2/run_probe_mutants.py`).
  - Setup: copied trees; the same 8 non-slow test files as challenger_FU_D_r1_1; `-k "not freeze_receipt"`.
  - The 22 mutants are 12 r1 survivors and 10 of mine:
    - r1 survivors: X45, Q09, X22, Q03, X49, Q14, X37, M12, Q15, X35, Q17, Q24.
    - Mine: D1/D2 (δ default changed in fplus_gate/decide), D3 (δ passed to decide in the script), D4 (δ only in the script's early gate read), D5 (fminus default), J1–J4 (the other joint-reading strings and the lookup), R1 (reason text).
  - orig mode, shipped suite: baseline 120 passed. 18/22 SURVIVE; only J1, J3, J4 and R1 are killed.
  - new mode, plus `proposed_test_r2_regression.py`: baseline 136 passed. 22/22 KILLED (`mutants_new.out.json`).
  - My first version of the test file left D4 alive (`mutants_new_v1.log`). D4 is killed only after adding a script test with gate gain 0.5 % plus stray Stage-1 records. Without that test, D4 would get through.
- **Probe 2: G1/G2** (`probe_g1_g2_frozen_gaps.py`, synthetic data only, output in `probe_g1_g2.out.json`).
  - G1: a NaN test_nmse is accepted, and the end-to-end verdict is **inconclusive** with the normal "measurement-capacity gate failed" reason. That is the shipped verdict category.
  - G2: with a failing gate, the unplanned directories `Fplus_C_s1` and `junk_dir` are ignored (rc 0, inconclusive). With a passing gate, the same directory raises RecordError.
- The frozen `scripts/topic2fu_d_c4scan.py` PATHS cover only the worker_FU_D_r1 directories. A worker_FU_D_r2's verification and metadata directories are not scanned. Its UNQUOTED16 regex flags any free-standing 16-hex string, so abbreviated hashes of exactly 16 hex characters in a new addendum would be hits.
- The r1 C4 test `tests/topic2_rgpool/test_outputs_no_ids.py` scans docs/…/topic2 for the BIDS pattern. FU-B's addendum 01 shows that an ordinary English word with that hyphenated prefix trips it.
- The challenger_FU_D_r1_1 harness hard-codes its TESTS list. Rerunning it unchanged would not pick up a new test file, so X45 would still "survive".

## 2. Logic Chain
1. The blocking items X45 and X22 are test-coverage gaps on CPU-only verdict code. The shipped verdict reproduces byte for byte, and four verifiers recomputed it independently. So the fix is additive tests; there is no rerun and no GPU use. (§1 rerun; r1 gate record.)
2. Pinning only `K.DELTA == 0.01` is not enough. D1–D4 flip the same decision without touching config.DELTA. The tests must pin every δ default and check the shipped verdict end to end against an oracle that uses its own literal δ = 1/100. D4 needs a dedicated script-level case. (Probe 1, v1 vs v2.)
3. The frozen tests and code are pinned by the code receipt. So new tests must go in NEW files, for example `tests/topic2_fu_d/test_r2_regression.py`, pinned by a new receipt. Editing the 12 pinned test files would break `code_sha256_at_freeze.txt`. (§1 receipts.)
4. G1 and G2 cannot be made card-correct without editing frozen src or scripts. A test asserting the card behaviour would fail on the frozen code. G1 is decision-relevant in kind: a corrupted record yields exactly the shipped category. So the shipped data needs explicit guards: every shipped number finite with exactly 16 terms and recomputable, and the runs/ directory holding exactly the 3 planned gate directories. The deviation itself goes in an erratum, following the T2.4 precedent ("erratum without editing the frozen script"). (Probe 2.)
5. The result report is receipt-pinned. So the nonblocking wording items (N3 "closes it further" rests on n = 1 per scale; N4 card §7.1 "+3.06 % / +2.93 %" are r1 seed-mean gains, not per-seed values; card §0 lists jobs 396/404/430 but its 0.097 GPU-h also counts job 418) go in the addendum, not into edits. (§1.)
6. Verifiers will rerun their own harnesses. The worker must therefore ship one union harness over the full suite, including the new file, and report kills or equivalence proofs for every r1-verifier mutant. Otherwise a fixed TESTS list reproduces the REFUTED result. (§1 harness observation.)

## 3. Caveats
- My probe covered 22 mutants, not the full union of about 180 (worker 62, reviewer 26, challenger_1 50, challenger_2 29, auditor 13). Equivalence claims for Q08, Q21, Q19 and A05 come from the r1 verifiers; I did not recheck them.
- I did not run the slow E192 model test or the C4 output test in the mutation copies, and I did not run the proposed file inside the real repo tree (only in copies).
- The proposed Q24 test monkeypatches `importlib.util.spec_from_file_location` with a pass-through for every path except scripts/topic2_train.py. It works under pytest 3.12 here; a simpler variant is acceptable.
- The receipt "belt" test (`test_fud_code_matches_freeze_receipt`) kills any code change wholesale. It was excluded from the semantic mutation run, so the 22/22 kills are not inflated by it.
- I did not judge whether root wants extra F+ seeds (about 7.1 GPU-h). That is a new card plus a PI decision, outside this fix.

## 4. Conclusion (recommended fix strategy for worker_FU_D_r2)
1. **No new runs, no GPU, verdict unchanged** (`inconclusive`, measurement capacity at E192). Do not edit the frozen card, report, src, scripts or the 12 pinned test files.
2. **Write `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_01.md`** (C3 deviations record).
   - (a) Added tests, with the r1 verifier mutant IDs each one kills.
   - (b) Erratum G1: a NaN test_nmse is accepted by `records.validate_completed`.
   - (c) Erratum G2: `strict=False` ignores unplanned directories when the gate fails, against card §8.
   - (d) Shipped data does not reach either gap (shown by the new guards).
   - (e) Wording notes N3, N4 and the card §0 job list.
   - (f) No change to the verdict or numbers.
   - Avoid free-standing 16-hex abbreviations and the hyphenated BIDS-like prefix in the text.
3. **Add `tests/topic2_fu_d/test_r2_regression.py`.** Start from `verification/explorer_FU_D_r2_2/proposed_test_r2_regression.py` (sha256 84243d2d…7114). It contains:
   - δ pins: the constant and all 5 defaults;
   - a gate case with gains between 0.3 % and 1 %;
   - a shipped-inputs receipt check;
   - a check that the runs directory holds only the 3 planned dirs;
   - a check that shipped records are finite, have 16 terms and validate;
   - a shipped-verdict reproduction with the `--out` tmp path, equal to the shipped JSON, against an exact Fraction oracle with literal δ = 1/100 and the exact reason and joint text;
   - the D4 script case;
   - the JOINT_READING table pinned for all 5 verdicts;
   - record guards: 15 terms, a 1e-9 test_nmse mismatch, validation steps, the permutation-file sha, the sidecar config dict;
   - seed mean versus median;
   - the r1-agreement assertion via monkeypatch;
   - the wrapper exit code 3;
   - the freeze-receipt belt.

   Never write into results/ (always pass `--out tmp_path`).
4. **New receipt `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`** for the addendum and the new test file(s). Leave the three existing receipts untouched. State in the addendum that the on-disk test set is now the freeze list plus the listed files.
5. **One union mutation harness** (in verification/worker_FU_D_r2/). Every r1 verifier mutant, about 180, runs against the full non-slow suite including the new file (glob the directory, not a fixed list), with a no-change control. Require 0 survivors except documented equivalents (Q08, Q21, Q19, A05: give a proof for each). At about 8–15 s per mutant this is about 30–45 min; run it detached with ≤ 2 concurrent pytest.
6. **C4 checks.**
   - The FU-D c4scan PATHS cannot be changed (frozen), so run a count-only scan that also covers the r2 directories: verification/worker_FU_D_r2, its metadata, the addendum and the new test.
   - Run `tests/topic2_rgpool/test_outputs_no_ids.py` and `tests/topic2_fu_d/test_c4_outputs.py` after writing the addendum.
7. **Final checks.** Run:
   - the full suites: tests/topic2_fu_d (expect 129 plus the new tests), the old suite (86) and topic2_rgpool;
   - C1;
   - all receipts, old and new;
   - audit_layout.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r2_2/run_probe_mutants.py orig /tmp/o.json` should show 18 SURVIVED. With the `new` mode argument it should show 22 KILLED and a baseline of 136 passed. It works on copies only.
- `PYTHONPATH=. python3 verification/explorer_FU_D_r2_2/probe_g1_g2_frozen_gaps.py out.json` should give G1 accepted=true, inconclusive; G2 rc 0 when the gate fails and RecordError when it passes.
- `cmp verification/explorer_FU_D_r2_2/verdict_rerun.json results/topic2/2026-11-02_fu_d/verdict.json` should report the files identical.
- Invalidation: if any FU-D receipt fails, or if the runs/ directory gains entries, the shipped-data guards and this plan must be re-derived.
- GPU use: 0. B300 not touched. No git writes. No repo file outside my verification and metadata directories was written. No orphan processes; the debug tree was removed.
