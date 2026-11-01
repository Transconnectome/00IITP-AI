# Handoff — explorer_FU_D_r3_1 (FU_D iteration 3; explorer 1 of 3; lens: scientific design and falsifiability). Type: Hard

**Summary.** The r2 gate failed on test coverage and disclosure. The science was not at fault. The shipped verdict `inconclusive` (F+ gains 0.363 % / 0.655 % < δ 1 %) is untouched by either B1 or B2.
- **B1 is a whole rule tested in one direction.** Card §8 step 7 ("the category … differs") is tested only for the pair inconclusive → stop. In my probe, 8 of 9 step-7 variants survive the current 195-test suite: C12/CV09 and my E7a–f and E7i.
- **B2 is broader than reported.** The aliases cover zero-padded, Unicode-digit and also trailing-newline directory names.
- **There are more card departures that addendum_01 does not list.**
- **The fix:**
  - one additive test file;
  - one dated addendum_02 with errata;
  - one new receipt;
  - a union mutation run;
  - 0 GPU-h.
- **The proposed tests:** 34 tests, about 3.5 s.
  - They kill all 31 probe mutants: every r2-verifier survivor plus 11 of my own. 29 of the 31 survive the current suite.
  - They pass on frozen code.
- **Gate scope.** Root should get the r3 gate scope fixed in advance, as in PI decision 6, or the loop will not converge.

## 1. Observation

Integrity, checked at start and end:
- C1 rc 0.
- FU-D receipts card / code_sha256_at_freeze / output / addendum_01 have 0 non-OK lines.
- 0 GPU-h used. No git writes. No repo file outside my two directories was touched.
- C4 count-only scan of my 12 files: 0 `sub-` labels. One 6-digit hit, which is the loop count `400000` in probe_step7_cases.py, not an ID.
- I removed my copied trees myself, and none of my processes are left.

**O1 (B1). `src/topic2_fu_d/verdict.py::_stage1_category`, the line `if c2 != cat:`.**
- The only shipped step-7 flip test is `tests/topic2_fu_d/test_verdict.py:134-141`, with dropped category `stop`. The script-level stall test, `test_verdict_script.py:122-134`, stalls arm S only.
- I searched for synthetic seed-gain vectors with an independent scipy-t oracle (`verification/explorer_FU_D_r3_1/probe_step7_cases.py` → `step7_cases.out.json`).
- 14 of the 16 ordered pairs (all-seed category, stall-dropped category) can be built with n = 5 and seed 4 stalled. The 2 not found are stop → keep and stop → modify. An algebra sketch says they are unreachable with 1–2 seeds dropped, but this is not proven.

**O2. Mutation probe** (`run_probe_mutants.py`; evidence `probe_mutants.out.json`, sha256 8d651769…259f; log `probe_mutants.log`).
- Setup: copied trees, tests/topic2_fu_d minus test_e192_model and the belt test, one mutant at a time.
- Control: 189 passed on the current suite, and 222 passed with the proposed file added.
- Of 31 mutants, 29 survive the current suite and **0 survive with the proposed file**.
- The 29 that survive the current suite:
  - c2: C12, C23, R07, S05, S07, S08, S09, S11
  - c1: CV15, CV19, CP01, CP02, CP05, CP07, CP12, CP14, CR13
  - rev1: R31, R34
  - rev2: R35
  - own: E7a–f, E7i, W1 (stall detection restricted to arms "ES"), W2 (bootstrap B capped at 5000)
- E7g and E7h are already killed by the current suite.
- The mutant texts were typed again from the verifiers' lists. Those files were read, never run.
- The run used the 33-test version of the proposed file. I then added one shipped-data invariant test (34 tests, which pass on frozen code). That test kills no mutant, because it checks only shipped records.

**O3 (B2). `design.DIR_RE = r"^(hcp|Fplus|Fminus)_([ECS])_s(\d+)(_a1)?$"` together with `int()`.**
- Probe: `probe_alias_names.out.json`.
- Accepted as aliases of planned keys:
  - `Fplus_C_s00`
  - `hcp_E_s01`
  - Arabic-Indic, fullwidth and Devanagari digits
  - `Fplus_C_s0\n`, because `$` matches before a final newline; this one is new
  - `Fplus_C_s00_a1`
- `records.load_runs` uses `found.setdefault(key, {})[att] = …`, so the later-sorted alias overwrites the real record, in strict and non-strict loads alike. challenger_FU_D_r2_2 P1b showed this turns a failing gate into a passing one.
- Shipped `runs/` holds exactly the 3 canonical ASCII names (r2 test plus my round-trip test).

**O4. Card departures not in addendum_01**, checked against the code and the frozen card text:
- **(a) E2 is wider than NaN.** P3 (challenger_2): an inf denominator with test_nmse 0 is accepted, and the gate passes. P4: a negative NMSE is accepted. Shipped: every num is ≥ 0, every den is > 0 and finite, and 0 < test_nmse < 1.
- **(b) `seed_plan.json` `seeds` is never checked against `n_seeds`** (P5). Card §10.2 says "Seeds are always 0..n−1". Shipped: no seed plan exists.
- **(c) F− records when Stage 1 is not a would-be keep are flagged (`protocol_flag_fminus`), not stopped.** Card §8 says the planned set includes "the F− condition", and unplanned directories are protocol errors. With a failed gate, F− directories are silently skipped (E1 path). Shipped: no F− directories.
- **(d) With the capacity floor active, `_stage1_category` returns before computing the stall sensitivity.** Card §9(a) says "The stall sensitivity … is reported". The category is unaffected. This is mutant C23.
- **(e) Wrong reason text for cost-guard runs.** If the gate passes and Stage-1 runs are missing because of the cost guard (card §10.3: "missing"), the reason says "(software failure)" (reviewer_FU_D_r2_1 finding 3). The category (`no_verdict`) is the same.

**O5. The claim does not hold as written.** addendum_01 §4 says "0 survivors change a shipped decision output" and "8 survive; each … equivalent". O2 shows non-equivalent survivors in the verdict machinery. They change Stage-1 categories (C12, E7a–f: inconclusive ↔ stop/keep/modify), not shipped outputs.

## 2. Logic Chain

1. **The shipped verdict is not in question.** All 5 r2 verifiers reproduced it, and B1 and B2 are unreachable on the shipped data (Stage 1 was not run, and the directory listing is pinned). Changing the verdict, rerunning, or using GPU would be wrong.
2. **Step 7 is a pre-registered card rule (§8 step 7, §12 item 4).** A rule tested in one direction is not falsified by the suite in the other. O1 and O2 show that 6 more one-line variants, beyond C12, survive. So the defect is a class, and closing it needs the truth table, not one witness case.
   - Each case's premise must be checked by an oracle independent of the FU-D code. Otherwise a fixture drift silently stops exercising the pair.
3. **CP01/CP02/W1 are the same class at the script level** (which arm's stall is detected). The fix is one stall test per arm.
4. **B2 cannot be fixed by additive tests.**
   - A test asserting RecordError on aliases would fail on frozen code.
   - A test asserting the alias behaviour would encode a defect, as `test_non_strict_skips_unplanned_dirs` already does.
   - Fixing it in code would be a post-result change to receipt-pinned code.
   - The right instrument is erratum E5 with a reading rule, plus a shipped-data invariant (canonical round-trip, ASCII, no whitespace).
5. **O4 (a)–(c) are in the same disclosure class that made B2 blocking:** card departures that are missing from the errata. If they stay unlisted, the next challenger can REFUTE on them. (a) can invert a gate. They should all be disclosed now, with shipped-data evidence. (d) and (e) are wording or reporting errata.
6. **Convergence.** Each r2 verifier designed 36–65 fresh mutants, mostly on Stage-1, F− and seed-plan paths. Those paths are dead under this card once F+ failed: card §7.1 says Stage 1 is not run.
   - Without a scope rule, every iteration can find new dead-path survivors.
   - Decision 6 is the PI precedent for a fixed-scope final iteration.
   - The verdict code may be reused by a future card (report §5: D′, D-gate-seeds, D-mid). That justifies closing the reported classes now. It does not justify open-ended mutation of dead paths, because any reuse needs a new card, which should replace the loader anyway.

## 3. Caveats
- I did not rerun the worker's 423-mutant union or every r2 verifier list against the proposed file. My probe covers every reported r2 survivor plus 11 of my own variants.
- The equivalence of R36, R40 and R43 (reviewer_1) and of R04/CR01 is taken from the verifiers. I did not prove it again.
- stop → keep and stop → modify were not found by random search (400k draws per configuration). They are plausibly unreachable, but not proven.
- The bootstrap test in the proposed file compares the script output with a direct call of the frozen `stats.hierarchical_bootstrap` using literal card parameters (B = 10,000, seed 0). This tests the wiring, not the frozen function, which the r1 receipts pin.
- The floor test asserts only the reason, as card step order (6 before 7) requires. It deliberately does not assert that `stall_sensitivity` is absent, because that absence is departure O4(d).
- Whether the r3 gate scope may be fixed in advance is a root/PI decision. I only recommend it.

## 4. Conclusion

Fixed-scope, additive r3. 0 GPU-h, no rerun, no frozen file edited. The verdict stays `inconclusive`.

1. **New test file** `tests/topic2_fu_d/test_fud_r3_guards.py`, adapted from `verification/explorer_FU_D_r3_1/proposed_test_fud_r3_guards.py` (sha256 cde99459…f990). It contains:
   - the step-7 truth table (14 pairs, with an independent oracle as a premise check, exact reasons);
   - no-stall equals the step-5 category for all 4 categories;
   - floor applied before stall;
   - `decide` forwards δ;
   - literal reason strings for steps 1–5;
   - `post_checks_ok` must be literally True (missing, None, 1, "True" and False are all rejected);
   - stall detection in each of arms E, C and S;
   - an incomplete gate with completed Stage-1 records gives `no_verdict` with nothing read;
   - F− flag conditions (failed F− flagged; a would-be keep with a failing F− is not flagged);
   - a non-seed-0 stray `hcp_` directory is flagged;
   - secondary pins (B = 10,000, seed 0, num/den order, per-subject seed-mean axis);
   - shipped names canonical;
   - shipped error terms finite and positive.
2. **Addendum** `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md`, post hoc, verdict unchanged. It records:
   - **E5:** aliases (zero-pad, Unicode digits, trailing newline; strict too; they can override the real record and flip the gate). *Reading rule:* every directory in `runs/` must equal `run_name(*parse_dir(name))` and be ASCII, or the verdict is a protocol error.
   - **E2′:** widened to non-finite or negative num, non-positive den, and test_nmse outside [0, ∞) (P3, P4).
   - **E6:** the seed plan's `seeds` is not checked against `n_seeds` (P5).
   - **E7:** F− records without a would-be keep are flagged, not stopped, and are skipped on the failed-gate path.
   - **W4:** the floor suppresses the §9(a) stall-sensitivity report.
   - **W5:** the reason text for cost-guard-missing Stage-1 runs.
   - **A correction of addendum_01 §4:** "0 non-equivalent survivors" held only for that harness's mutant set.
   - **A reuse condition:** any future card that reuses `src/topic2_fu_d` must replace `load_runs`/`validate_completed` for E1, E2′, E5, E6 and E7 in new code under its own freeze.
   - **Shipped evidence for each item.**
3. **Receipt** `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt`. Existing receipts stay untouched.
4. **Union mutation** on copies, globbing tests/topic2_fu_d. The mutants to include:
   - the worker's 423;
   - all r2 verifier lists (c1 65, c2 62, rev1 44, rev2 36, auditor 20);
   - my 11;
   - a step-7/stall sweep (each category literal in the `c2`/`cat` condition, each arm subset in the script's stall loop).

   Require 0 non-equivalent survivors, with an equivalence proof for each survivor that remains.
5. **Root:** before dispatching the r3 verifiers, get a written gate scope (decision-6 style). The proposed rule:
   - **Blocking:** the reported r2 classes not closed; a regression; an integrity failure; any mutant that changes a shipped `verdict.json` leaf; a card departure reachable on shipped data that is not disclosed.
   - **Nonblocking:** new survivors only on paths that are unreachable under this card after the F+ failure.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r3_1/probe_alias_names.py /tmp/alias.json   # zero-pad / unicode / newline accepted
# proposed tests on a copied tree (never in the repo):
setsid nohup env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 \
  verification/explorer_FU_D_r3_1/run_probe_mutants.py $PWD <new empty work dir> <out.json> > <log> 2>&1 &
# expect: CTRL green both ways; survive_with_proposed == []; ~14 min
```
**Invalidation.** Any of these would invalidate the conclusion:
- a mutant in `MUTANTS` that survives with the proposed file;
- a premise assertion that fails, meaning the oracle and the code disagree on a fixture;
- a shipped `runs/` name that is not canonical;
- a shipped record with a non-positive denominator.
