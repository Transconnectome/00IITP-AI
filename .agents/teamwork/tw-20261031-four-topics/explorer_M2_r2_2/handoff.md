# handoff — explorer_M2_r2_2 (M2, iteration 2) — Hard handoff, 2026-10-31T12:22Z

**Summary.** The M2 iteration-1 gate failed on two blocking items from challenger_M2_r1_1. I confirmed both independently.
- No test pins the verdict logic.
- Family B is described with the wrong ceiling (1119 instead of an effective 7).

Neither item is a wrong number or a wrong verdict, and both have additive fixes.
- One new test file. A draft is here; it kills 18 of 18 targeted mutants in a scratch copy, and the control passes.
- A dated addendum 03 with its own sha receipt. A draft is here.

No code, frozen file, rerun or GPU is needed.

## 1. Observation

**O1. Verdict code is correct but unguarded.**
- `src/topic3_spectral/analysis.py:184-199` (`replication_verdict`) implements the card §5 rule. Line 191 checks Holm p and that the primary CI excludes 0. Lines 192–194 check sign agreement and the zoo Holm p. Line 195 requires ≥ 2 agreeing checkpoints.
- D1 is at lines 72–77 and D3 at line 99.
- The only rule test is `tests/topic3_spectral/test_analysis.py:60-70`. It uses synthetic checkpoints that all share one sign, or are null. No zoo checkpoint in it is significant with the opposite sign, which is exactly the real-data case.
- That explains the mutant survivors reported by 4 verifiers (gate record): reviewer_M2_r1_1 R1/R3/R7/R8/R9; reviewer_M2_r1_2 R1; challenger_M2_r1_1 N02/N05/N06/N08/N09/N10/N11/N17; challenger_M2_r1_2 M10/M13/M14/M15/M18/M20/M22; auditor X06/X09/X12/X13.

**O2. Proposed test file kills them.**
- File: `verification/explorer_M2_r2_2/proposed_test_verdict_rules.py`, 13 tests, run on a scratch copy of `src/topic3_spectral` and `tests/` with the file added.
- Control: `13 passed in 0.33s`.
- `mini_mutants.py` applies 18 mutants, one at a time, to the scratch copy. Result: **18/18 KILLED**, and the control passes before and after. Log: `verification/explorer_M2_r2_2/mini_mutants.log`.
- Mutants killed:
  - Replication rule: N05/R1 ignore sign; N06/R3/X12 ignore primary CI; N08 raw p; R8 Holm threshold 0.5 (primary and zoo); zoo `<=`; min-agree `>`.
  - D1 and D3: N09 D1 hi>0; M20 D1 point>0; X06 D1 verdict ignores corr; N10/M22 D3 any.
  - Wiring and Holm: N11/R9 H1a wired to L2; H1a orientation swapped; direction label flipped; Holm removed inside the checkpoint.
  - Descriptive formulas: N17/R7/X09/M13 jackknife without (n−1)/n; M14 SE without √(m/(n−m)); N02/M18 sign-flip without +1.
- The scratch `analysis.py` is byte-identical to production afterwards (`cmp` OK).
- The D1/D3 tests monkeypatch `analysis.paired_subsample_delta`, `describe_matrix`, `iid_reference` and `subsample_mean` inside the test only, so the decision branches get exact lo/hi inputs.

**O3. Effective rank of the saved token spectra.**
- Source: `verification/explorer_M2_r2_2/probe_rank_ceiling.log`, reading `results/topic3/2026-10-31/token_job/*_token_spectra.npz`. The npz keys are position-keyed summaries; there is no ids key.
- L2, LN0L2 and L3, all 4 checkpoints:
  - eigenvalues above 1e-5·max: median 7, min 7, max 7–10;
  - top-7 energy: median ≥ 0.99997;
  - concatenated PR / mean per-frame PR: 1.000000–1.000006.
- L1: top-63 energy ≥ 0.99996 (63 = 4³ − 1).
- L0: the eigenvalue array has length 384, so D caps the rank.
- At L2+, the H4 160-token subsample over the per-frame PR is 1.0000, i.e. it changes nothing.
- This agrees with challenger_M2_r1_1's direct connectome probe (`verification/challenger_M2_r1_1/probe_connectome_time_invariance.log`): the time share of L3 variance at a fixed cell is 1e-6 (primary) and 1e-5 (HCP).
- **Correction to challenger_M2_r1_2 N1.** It said "L0 511": L0 cannot exceed 384, because D = 384.

**O4. Wording that the observation contradicts.**
- Card §5, line 80: "1120×1536 (ceiling 1119)".
- Report line 102: "very low-dimensional: about 6 of a possible 1119. The dynamic-range fixture shows that corrPR at this shape can resolve planted ranks of 3, 12 and 40".
- Report line 114: "2–5% *increase* in within-window dimensionality".
- Report line 154, R2 row: "A token-level collapse FAILS … the within-window dimension does not drop".

**O5. The replication unit is the checkpoint.**
- Source: `probe_checkpoint_variance.log`.
- H1a: the variance of the checkpoint means is 0.00762, against a mean within-checkpoint subject variance of 0.00057. Ratio 13.4.
- H1b: ratio 5.8.

**O6. One subject drives the L1 jackknife SE.**
- Source: `probe_l1_jackknife.log`, reading only key `X` of `VRABES/RemissionAnalysis/pooled_E192_layers/layer_1.npz`.
- n = 57, full PR 2.7782, jackknife SE 3.5767.
- The largest leave-one-out PR is 6.39; the next are 2.84 and 2.82.
- Without that one term the SE would be 0.149.
- Report line 49 says "driven by a few subjects".

**O7. Rounding slips.**
- `family_A_subject_level.json` A1 L2_minus_L3/cov/lo is 3.2249864…, reported as "+3.23" (report line 55).
- `family_B_token_level.json` A1b zoo_NewUAH_deepE192_L5e-5 L3_minus_LN0L2_corr/point is −3.2848924…, reported as "−3.29" (report line 68).

**O8. Pins and placement.**
- `tests/topic3_spectral/test_analysis.py` and every other existing topic3 test are pinned in both `code_sha256_at_freeze.txt` and `output_sha256.txt`.
- A new file in `tests/topic3_spectral/` touches no pin. `test_outputs_no_ids.py` globs only `results/`, so it is unaffected.
- No Topic 3 file is newer than addendum_02 (20:15 KST).

**O9. Harness path hazards for re-killing the verifiers' mutants.**
- `challenger_M2_r1_2/probes/p6_mutants.py:3-4` hard-codes TREE and WORK as absolute paths inside challenger_M2_r1_2's folder, and rmtrees WORK at line 38.
- `reviewer_M2_r1_2/r2_1117/mutants_rev.py:27` writes `mutants_rev.out.json` to the current directory.
- challenger_M2_r1_1, reviewer_M2_r1_1 and the auditor write next to the script (`HERE`). The auditor also imports `verification/worker_M2_r1/mutants.py` read-only.

## 2. Logic Chain

1. **Blocking item 1 is real (O1).** The decision functions are correct today, but a sign-agnostic replication rule (N05) would turn H1b into "holds" on the real data, as challenger_M2_r1_1 showed in `probe_N05_real_impact.log`, and every existing test would still pass. That breaks T3.3 ("fixtures … fail on the targeted defect"), and C3 asks for the same.
2. **Exact fixtures fix it (O2).** Fixtures built from hand-made inputs (per-checkpoint dicts; monkeypatched lo/hi) make each rule boundary deterministic. They kill all 18 mutants without touching `analysis.py`. Because the shipped code passes them, the existing verdicts are also certified by tests now, not only by reviewers deriving them by hand.
3. **Blocking item 2 is real (O3, O4).** With rank 7 everywhere and concatenation adding nothing, Family B's per-subject PR is the PR of 8 time-invariant spatial-cell vectors. The 1119 ceiling, "within-window dimensionality", the dynamic-range-fixture sentence and the R2 token-level phrasing all describe a different estimand.
4. **The rule outcomes still stand.** H1a and H1b are defined as exactly these contrasts, and changing a verdict after the results would be post hoc (C3). So the correct fix restricts the interpretation in a new dated addendum. The frozen card and the pinned report stay unedited (C3 says "deviations recorded in a dated addendum, never by editing a frozen card").
5. **O5–O7 belong in the same addendum.** They are non-blocking reading limits and errata from the same verifiers, and fixing them costs nothing.
6. **The next gate needs evidence on the verifiers' own mutant sets, not just mine.** So the worker must rerun copied harnesses with the paths repointed (O9), on a complete copied tree with a passing control. challenger_M2_r1_1's run 1 was invalid because its tree was incomplete.

## 3. Caveats

- My mutants re-implement the verifiers' descriptions; I did not run their harnesses. Exact mutant text may differ, so the worker's copied-harness receipts are the authoritative evidence.
- Equivalent or descriptive mutants that my file does not target: X13 (uniform iid reference), M15 (LN eps = 0), M10 (rank-slope window). I recommend declaring them equivalent or descriptive-only with a reason. An optional extra test could pin LN eps through a constant-token row, where eps = 0 gives NaN.
- I did not determine why tokens are time-invariant (input normalisation or model). The addendum must state this as unknown.
- The time-invariance evidence on connectome is challenger_M2_r1_1's. My own evidence is the saved spectra only; I read no frames.
- Card gap, not a bug: card §5 does not name the outcome "primary p_holm ≥ 0.05 with CI excluding 0". The code labels it "killed (primary CI includes 0)". My test asserts only that it is not "holds" and not significant. The addendum may note that the label is imprecise.
- Out of my scope, left for root: H2 (random-init), the meaning of "3번. A" (worker_M2_r1 resolved it as "resume and reuse saved results"), the run-level auto-commit and push (C4), and the missing GPU ledger.

## 4. Conclusion

Recommended fix for worker_M2_r2. Use a new identity, additive writes only, 0 GPU-h, CPU only.
1. **Tests.** Add `tests/topic3_spectral/test_verdict_rules.py`, starting from `verification/explorer_M2_r2_2/proposed_test_verdict_rules.py`; the worker owns the final text. Do not edit `test_analysis.py` or any `src/topic3_spectral/*`.
   - If any new test fails on the shipped code, stop and report. Do not change code to make it pass.
2. **Mutant receipts.** Copy every verifier harness into `verification/worker_M2_r2/`, repoint every output and work path there (O9), and confirm the control on the copied tree. The control count should be 54 + new tests (67 with my draft). Then run each copy.
   - Target: every verdict-path survivor killed.
   - Descriptive survivors must be killed or declared equivalent, each with a reason.
   - Also rerun `worker_M2_r1/mutants.py` from a copy.
3. **Addendum 03.** Write `docs/03_empirical_analysis/topic3/2026-10-31_topic3_addendum_03.md`, starting from `verification/explorer_M2_r2_2/proposed_2026-10-31_topic3_addendum_03.md`. Record its sha256 and the new test file's sha256 in the new file `results/topic3/2026-10-31/addendum_03_sha256.txt`. Do not modify `output_sha256.txt`.
   - The worker must recompute the numbers with its own probe on the saved spectra.
   - Contents:
     - Family B estimand: effective ceiling 7 (L1: 63), time and frame invariance, superseded phrases, the H4 no-op;
     - the checkpoint replication unit (variance ratio about 13);
     - L1 SE driven by one subject;
     - 2 rounding errata;
     - the post-hoc test disclosure;
     - "no verdict changes".
4. **Final checks.**
   - C1 rc 0.
   - `sha256sum -c` on `card_sha256.txt`, `output_sha256.txt`, `addendum_02_sha256.txt` and `addendum_03_sha256.txt`: all OK.
   - `code_sha256_at_freeze.txt`: only the launcher fails, as already disclosed.
   - pytest: topic3 (54 + new), the old 86 and topic1 all pass.
   - ID grep shows nothing.
   - Layout lint over the whole run root is clean.
5. **Re-review.** Run fresh reviewers, challengers and an auditor on the M2 deliverable plus addendum 03 and the new tests.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
# rank / ceiling evidence (saved summaries only)
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/explorer_M2_r2_2/probe_rank_ceiling.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/explorer_M2_r2_2/probe_checkpoint_variance.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/explorer_M2_r2_2/probe_l1_jackknife.py
# proposed tests + mutants on a scratch copy (never the real tree)
S=$(mktemp -d); mkdir -p $S/src $S/tests; cp -r src/topic3_spectral $S/src/; cp tests/__init__.py $S/tests/; cp -r tests/topic3_spectral $S/tests/
cp verification/explorer_M2_r2_2/proposed_test_verdict_rules.py $S/tests/topic3_spectral/test_verdict_rules.py
/home/juke/superclaude-env/bin/python3 -I verification/explorer_M2_r2_2/mini_mutants.py $S    # expect CONTROL 13 passed; 18 KILLED
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
```
**Invalidation conditions.**
- Any token_job npz no longer matches `output_sha256.txt`.
- `analysis.py` changes.
- The proposed tests fail on the unmodified code.
- A verifier harness, run on a complete tree, shows a verdict-path survivor against the added file.
