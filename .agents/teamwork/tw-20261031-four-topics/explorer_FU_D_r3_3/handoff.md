# handoff — explorer_FU_D_r3_3 (FU_D iteration 3, explorer 3 of 3, lens: adversarial pre-mortem) — Hard handoff

**Summary.** The shipped FU-D verdict (`inconclusive`, F+ gate failed at E192) is not in doubt, and fixing the r2 gate
failure needs 0 GPU-h. The real risk is procedural. r3 is the **last** iteration (`workflow_C_script.js.txt`:
`MAX_ITER = 3`), and the gate passes only if all five verifiers are positive. Two fresh challengers will each write
60+ new mutants. If r3 only closes the named mutants (C12, alias), it will very likely fail again in the same way. My probes show
the defect class is wider than C12: 6 of the 8 sibling stall-rule mutants and 3 of the 6 stall-arm mutants survive today.
After a 35-test proposal kills all 30 targeted mutants, a 758-mutant sweep over operator classes that the r2 sweep
never generated still leaves 87 survivors. About 50 of them are not equivalent, none changes the shipped output, and
most are unpinned `verdict.json` fields on the Stage-1 path.

## 1. Observation

Integrity at end: C1 rc 0. FU-D receipts card 1/1, code_sha256_at_freeze 29/29, output 34/34 and addendum_01 23/23
are all OK. `verdict.json` sha256 is f6b295d9…59fc (unchanged). Whole-run `audit_layout.py`: rc 0, 690 files,
findings []. 0 GPU-h, no git writes, no repo file written outside my two directories.

O1. The iteration limit is `const MAX_ITER = 3` (orchestrator/workflow_C_script.js.txt:10). The gate (lines
106–114) passes only if the auditor is CLEAN, both reviewers APPROVE and both challengers are CONFIRMED. It has no
"blocking vs nonblocking" filter: any REFUTED fails it.

O2. Frozen step 7, src/topic2_fu_d/verdict.py:96: `if c2 != cat:`. The only flip test,
tests/topic2_fu_d/test_verdict.py:134, covers just all-seed ≠ stop with stall-dropped = stop. The script stall test,
test_verdict_script.py:122, stalls only arm S.

O3. Targeted run of 30 mutants vs the current suite (verification/explorer_FU_D_r3_3/mut/targeted_current.log;
control 189 passed): **19 SURVIVED / 11 KILLED.**
- Survivors:
  - T01 (= C12/CV09), T03–T07: the stall-flip conjunct restrictions `and c2 != "inconclusive"|"keep"|"modify"`,
    `and cat != "stop"|"keep"|"modify"`;
  - T09–T11: stall arms "S", "CS", "ES" (= CP01/CP02 plus one sibling);
  - T15 (S11/R31), T16 (CV15), T17 (CV19), T18 (CR01), T19 (CR13/R07), T20 (S05);
  - T21–T24 (CP03/CP04/CP05/CP11: bootstrap seed, B default, num/den order, seed-mean axis).
- Killed: T02, T08, T12–T14, T25–T30.

O4. Proposal verification/explorer_FU_D_r3_3/proposed_test_fud_r3_guards.py (35 tests, sha256 5bbd4453…9031):
- The control passes with it added (224 passed, 1 deselected), so it is green on frozen code.
- Targeted run vs current + proposal (mut/targeted_proposed.log): **30/30 KILLED.**
- The first proposal run was INVALID: the file was copied under its `proposed_` name and not collected. Its log is
  kept as `targeted_proposed_INVALID_file_not_collected.log`; the runner was fixed and the run repeated.

O5. Sweep (mut/gen_sweep.py → sweep3.json, 758 mutants over verdict.py, records.py, design.py and
scripts/topic2fu_d_verdict.py).
- Operator classes: statement deletion, dict-entry deletion, call-keyword deletion, bool-op operand drop,
  output-string change, numeric +1/×2 and "ECS"-subset. The r2 worker's sweep generated none of these.
- Run against the current suite + proposal (mut/sweep3_proposed.out.json, control 224 passed, 2 at a time, -x).
- **671 KILLED, 87 SURVIVED.** 241 mutants change the shipped verdict.json and all 241 are killed: **0 shipped-changing
  survivors.**
- Classified survivors, non-equivalent and killable:

| group | mutants | what escapes |
|---|---|---|
| record pins | W351, W352 (HP_FIELDS entries dropped: a record with a wrong `wd` / `warmup_frac` / `mask_ratio` is accepted); W365 (`isfinite(pooled)` dropped → NaN pooled accepted); W369 (wrapper check made unconditional); W413 (non-str token → TypeError instead of RecordError); W417/W419 (`perm_key` arm check removed) | card §8 "records violating the pins … are protocol errors" |
| decide outputs | W037 (`stall_sensitivity.category=None` dropped), W051/W139 (`n_seeds`), W076/W212 (`fminus_gate`), W100/W123 (`primary_reason`), W166/W167 (stall I1_t/I2_t), W196 | verdict.json leaves on the Stage-1 path unpinned |
| script outputs | W569, W646, W690, W746 (F− protocol flag also raised on a would-be keep); W601, W640, W723, W725–W727 (`val_curves` dropped/renamed/arm subset); W643 (`n_boot` not forwarded; visible only with `--n-boot` ≠ 10000); W703 (`group_state` "failed" literal → fully failed gate reported as "not run"); W560 (`os.path.isdir(rdir)` dropped → crash when `runs/` is absent) | descriptive outputs, a reason text, a crash where no_verdict is due |
| stdout summary | W498, W621, W658–W662, W697–W702, W737–W739, W753–W757 | the printed summary is never asserted (cosmetic, cheap to pin) |

- Equivalent or effect-free (proof sketches in §2): W105–W107, W149, W184, W185 (needs_fminus, S023/S025 class);
  W296; W335/W342 (S160); W373; W376; W499; W512/W522 (Q19); W529; W542–W544, W623 (argparse);
  W563/W564/W593/W594/W596/W677/W678/W751 (S181 class / unread initial keys); W644 (frozen default seed = 0);
  W667/W709 (placeholder `rec` never read); W671; exception-message-only strings W152, W193, W211, W235, W664, W682.

O6. B2 is wider than the gate path (probes/alias_and_terms.out.json, frozen code, tmp dirs).
- With a gate pass, a 5-seed plan and canonical Stage-1 records the verdict is `stop`.
- Adding alias dirs `hcp_C_s00…` (content seed 0) gives verdict `inconclusive` with rc 0 and
  `used_dir hcp_C_s0 → hcp_C_s00`. An alias can change a real category.
- `validate_completed` also accepts an inf denominator (test_nmse becomes 0.0) and negated terms (test_nmse −0.66).

O7. The shipped sidecars' `fud_code_sha256` (8 files) and `wrapper_sha256` all equal code_sha256_at_freeze.txt for
E/C/S. No record check and no test pins this; records.py never reads `fud_code_sha256`.

O8. addendum_01 §4 (pinned by addendum_01_sha256.txt) states "each of the 8 is equivalent" and the worker's headline
says "0 non-equivalent survivors remain". C12 refuted the general reading of that claim. addendum_01 cannot be edited,
because its receipt pins it.

## 2. Logic chain

1. O1: r3 is the final iteration, and one REFUTED from either challenger ends FU_D as INCOMPLETE (a PI decision). The
   cost of under-closing is therefore the whole milestone, not one more round.
2. O3: closing only C12 would leave T03–T07 and T09–T11, the same "verdict changes if the code changes" class that
   REFUTED r2. A step-7 decision-table test over all 16 category pairs, plus per-arm script stall tests, kills them
   all (O4).
3. O5: each of the r2 verifiers found survivors because each used an operator class nobody had swept. The 87 sweep
   survivors show that this is still true after O4. The largest group is unpinned output structure. The M2 precedent
   (PI decision 6, "Family A full-output regression") fixed exactly this class with full-output comparisons. The r3
   equivalent is whole-`verdict.json` pinning for a set of synthetic scenarios, with values from an independent
   oracle.
4. O6, O7: card §8 makes duplicate, mismatching and pin-violating records protocol errors. The frozen loader departs
   from this for alias names (gate *and* Stage-1 paths), non-finite and negative terms, and unchecked FU-D code
   hashes. These cannot be fixed in frozen code. They must be stated as errata with reading rules, and the shipped
   inputs pinned outside them by tests. This is the E1–E4 pattern.
5. O8: an uncorrected false claim in a pinned document is an integrity target. addendum_02 must correct it explicitly
   and state every new mutation claim only for its own evidence set ("for these N mutants in these classes").
6. Equivalence proofs are themselves attacked. A mutant that some input can distinguish (CV15 via a non-default δ,
   CV19 via the reason text, CR01 via a custom expectation, W643 via `--n-boot`) must be killed, not argued away.
   Only all-input equivalences go in the proof table, and "unreachable on shipped data" is a separate label.

## 3. Caveats

- I ran the sweep only against current + proposal. Survivors against the current suite alone are ≥ 87 (by
  monotonicity), but that number was not measured. My first run against the current suite was stopped by me after 9
  mutants to reorder the work; its log is kept as `mut/sweep3_current_ABORTED_reorder.log`.
- I did not rerun the worker's 423-mutant union or the r2 verifiers' lists (about 227) against the proposal. The r3
  worker should run all of them in one final run.
- The step-7 table test monkeypatches `V.primary_category`. A verifier may call that "testing a stub". It is paired
  with a no-monkeypatch C12 witness, and `primary_category` is pinned elsewhere by boundary tests.
- The classification of the 87 survivors comes from reading the code. I wrote no tests for the O5 groups; they are
  recommendations.
- Leftovers: `verification/explorer_FU_D_r3_3/mut/work_s/` (`_base`, W008, W009) are copied trees from the aborted
  run, and work_sp, work_t, work_tp and work_tp2 are empty dirs. My `rm` was denied by the harness and I did not work
  around it. Root may remove them. The copies hold only the repo's FU-D code and results and the sanitized r1 results
  (positional tokens), the same content as other agents' trees.
- I did not check B300 or the GPU ledger (not needed: 0 GPU-h, no runs).

## 4. Conclusion (recommended r3 strategy)

The scope stays a gate repair: 0 GPU-h, no reruns, verdict `inconclusive` unchanged. No edit to the card, src,
scripts, any existing test file (including test_fud_r2_guards.py), addendum_01, the result report, verdict.json or any
receipt. Aim for mutation adequacy, not named-mutant closure:

A. **New test file** `tests/topic2_fu_d/test_fud_r3_guards.py`, starting from my proposal. It contains:
   - the step-7 16-pair table and the C12 real-data witness;
   - per-arm script stall tests (E, C, S) and a two-stalled-seeds case;
   - an incomplete gate with plan + Stage-1 records → no_verdict, rc 0;
   - δ forwarded (decide with δ = 0.02);
   - floor reason wins and no `stall_sensitivity` is written;
   - hNN token width;
   - `post_checks_ok` missing / None / 1 / "true";
   - a failed-F− flag;
   - bootstrap B = 10,000 / seed 0 / num-den order and the per-subject seed-mean axis, checked against the frozen r1
     function called with card literals;
   - exact reason text for all 14 decide branches;
   - the shipped canonical-ASCII dir names, and positive finite terms.

   Then add the O5 kills:
   - per-field HP pin rejection (parametrize all six fields);
   - NaN in num → RecordError; `exp.wrapper_sha256 = None` accepts;
   - non-str token → RecordError; `perm_key("X", 0)` raises;
   - fully failed gate (attempt 0 and `_a1` both failed) → the exact "F+ gate run failed" reason;
   - no `runs/` dir → no_verdict, rc 0;
   - would-be keep with F− completed → no `protocol_flag_fminus`;
   - `--n-boot 200` vs the oracle with n_boot = 200;
   - `val_curves` key set and values;
   - script stdout summary JSON;
   - shipped sidecar `fud_code_sha256` and `wrapper_sha256` equal to the freeze receipt (O7).

B. **Full-output pinning.** For 6–8 synthetic scenarios (stop, keep + F− pass, modify, inconclusive, stall flip,
   floor, F− fail, F− not run, gate incomplete), compare the whole `verdict.json` from the script (`--out` in
   tmp_path) with an expected dict:
   - exact key sets at every level;
   - decision strings as literals;
   - numbers from an independent oracle (per-seed I1/I2 by hand arithmetic; t intervals from `scipy.stats.t.ppf`
     with df n−1; seed means with `sum/len`).
   Never generate the expected JSON by running the code under test.

C. **addendum_02** `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md` (post hoc, verdict
   unchanged):
   - §1 the r2 gate record: B1 C12, B2 alias, and the challenger_1 nonblocking list;
   - §2 an explicit correction of addendum_01's "0 non-equivalent survivors" (true only for its 423-mutant set);
   - §3 new errata, each with a reading rule and a shipped invariant:
     - **E5** alias run dirs (zero-padded / non-ASCII digits) override the canonical record on gate and Stage-1
       paths, under strict=True as well; reading rule: any dir name ≠ `run_name(key, att)` is a protocol error;
     - **E6** an inf denominator or a negative or zero term is accepted (P3/P4; generalises E2);
     - **E7** the `seed_plan.json` "seeds" list is not checked against `n_seeds` (P5);
     - **E8** the sidecar `fud_code_sha256` is not validated (O7);
     - **W4** with a gate pass, a plan and Stage 1 never launched (cost guard), the reason says "software failure"
       where card §10.3 says missing (cost) (reviewer_r2_1 finding 3);
   - §4 the card clause audit: every protocol-error clause of card §8, §9 and §10.4 listed as implemented + tested, or
     erratum + invariant;
   - §5 mutation evidence and the equivalence table (all-input proofs only), with "unreachable on shipped data" as a
     separate label;
   - §6 no-regression.

D. **Receipt** `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt` for the addendum, the new test file and the
   evidence. Existing receipts stay untouched.

E. **One final mutation run**, on copies, with the test directory globbed. Mutants:
   - the r2 union (423);
   - all r2 verifier lists (challenger_r2_1 65, challenger_r2_2 62, reviewer_r2_1 44, reviewer_r2_2 36,
     auditor_r2_1 20);
   - my targeted.json (30) and sweep3.json (758);
   - the worker's own new classes.

   Rules:
   - deselect **both** belt tests (r2 and any r3 belt), otherwise every kill is fake;
   - control first;
   - shipped output recomputed per mutant;
   - at most 2 concurrent pytest processes, timeout 900, run detached, with a test-file snapshot per run kept in an
     immutable version dir.

   Expected wall time is about 2 h for ~1,400 mutants at ~5 s each.

   Pass criterion: 0 survivors that change any shipped output; 0 non-equivalent survivors in the decision path;
   cosmetic survivors (exception text, stdout) killed or listed by name. State the claim only for this set.

F. **Hygiene.** No 16-hex literals and no free-standing 6-digit integers in new files; avoid hyphenated "sub-" words
   (the word "sub-cap" tripped the scanner before). Run the frozen C4 scan plus a count-only scan of the r3 paths,
   `tests/topic2_rgpool/test_outputs_no_ids.py` and `test_c4_outputs.py`. Run C1, all receipts, all suites,
   audit_layout, and a byte-identical `--out` regeneration of verdict.json.

G. **For root.** If r3 still fails only on new non-shipped-path mutants, the precedent is PI decision 6 (a
   fixed-scope gate). A further FU_D iteration, or running Stage 1 or more F+ seeds (≈7.1 GPU-h, 21.3 GPU-h of the
   cap unused), needs a PI decision and, for any new run, a new card. Neither the worker nor root may do that
   unilaterally.

## 5. Verification method

- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- Targeted, current suite: `cd verification/explorer_FU_D_r3_3/mut && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -I run_sweep.py /home/juke/git/00IITP-AI $PWD/work_x targeted.json out.json`
  gives 19 SURVIVED. With `EXTRA=/home/juke/git/00IITP-AI/verification/explorer_FU_D_r3_3/proposed_test_fud_r3_guards.py`
  it gives 30 KILLED and control 224 passed.
- Sweep: the same command with `sweep3.json` and `EXTRA=…` gives 671/87 (about 64 min).
- Alias and terms probe: `PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r3_3/probes/alias_and_terms.py`
- Artifact hashes: verification/explorer_FU_D_r3_3/artifact_sha256.txt.
- Invalidation: any change to src/topic2_fu_d, scripts/topic2fu_d_verdict.py or tests/topic2_fu_d changes the
  mutant offsets (the runner reports NOT_APPLIED) and the survivor set.
