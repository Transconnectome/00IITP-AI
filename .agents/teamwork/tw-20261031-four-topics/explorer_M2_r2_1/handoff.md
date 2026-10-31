# Handoff — explorer_M2_r2_1 (M2 Topic 3, iteration 2: failure analysis and fix strategy)

**Summary.** The M2 gate failed on challenger_M2_r1_1's two blocking issues, and I confirmed both from primary sources.
1. The tests do not guard the verdict logic.
2. The Family B estimand is described wrongly: the effective ceiling is 7 spatial cells, not 1119.

Neither issue makes a shipped number or verdict wrong. Both fixes are additive and need no rerun and no re-freeze:
- a new test file that kills every surviving verdict-path mutant;
- a dated addendum 03 that restates what Family B measures;
- a receipt for both.

## 1. Observation

**O1. Verdict code is correct today.** `src/topic3_spectral/analysis.py`:
- `replication_verdict` (lines 184–199) checks three things:
  - the sign, at line 193;
  - the Holm p of the zoo checkpoints, at line 194;
  - the primary checkpoint's Holm p and CI, at line 191.
- D1 (lines 72–77) uses `lo` for both cov and corr. D3 (line 99) uses `all(... lo > 0)`. TOKEN_PRIMARY (lines 142–143) pairs H1a = (L3, LN0L2) corrPR and H1b = (L3, L2) covPR.

**O2. The only rule test cannot see those conditions.**
- `tests/topic3_spectral/test_analysis.py:60-70` has three cases: all-planted, all-null, and mixed (2 planted, 2 null zoo). None has a zoo checkpoint that is significant in the opposite direction, and none has a primary checkpoint that is significant with its CI covering 0.
- `_arrs` (lines 46–57) draws `cat_corrpr__L2` and `cat_corrpr__LN0L2` independently from the same distribution. An H1a rewired to L3 vs L2 therefore still gives a mean of about `effect`, which is why N11/R9 survive.
- `test_subject_level_null_does_not_claim_l2_gt_l3` (lines 38–43) asserts `lo <= 0 <= hi` but never asserts that `D1[...]` is False.

**O3. Real-data impact (my probe).** `verification/explorer_M2_r2_1/probe_r2_a.log`:
- The shipped `replication_verdict` on the frozen `family_B_token_level.json` per_checkpoint gives H1a holds and H1b not replicated, matching the frozen verdicts.
- For both H1a and H1b, all 3 zoo checkpoints have Holm p = 0.0002.
- H1b signs: primary +0.0447; zoo −0.113, −0.033, +0.079. Dropping the sign condition gives 3 agreeing checkpoints, so H1b would become "holds". This matches challenger_1's probe_N05_real_impact.log.

**O4. Surviving mutants across all four verifier harnesses: 14 distinct.**

| Group | Mutant (ids) | What it breaks |
|---|---|---|
| Verdict path, blocking | replication ignores sign (N05, R1) | the H1b flip in O3 |
| | primary CI ignored (N06, R3, X12) | |
| | zoo uses raw p instead of Holm (N08) | |
| | D1 tests `hi` (N09) or `point` (M20) instead of `lo` | |
| | D3 uses `any` (N10, M22) | |
| | H1a wired to L3 vs L2 (N11, R9) | |
| Verdict path, also | primary Holm threshold 0.5 (R8) | |
| | D1 ignores the corr check (X06) | |
| | subsampling SE without √(m/(n−m)) (M14) | `lo` drives D1 and D3 |
| Cited numbers | jackknife without (n−1)/n (N17, R7, M13, X09) | the report's SEs |
| | sign-flip p without +1 (N02, M18) | |
| Near-equivalent | LN eps = 0 (M15) | |
| | rank-slope window = r (M10) | descriptive α only |
| | iid reference uniform (X13) | |

Sources:
- verification/challenger_M2_r1_1/mutants_challenger.out.json
- verification/challenger_M2_r1_2/probes/p6_mutants.out.json
- verification/reviewer_M2_r1_1/reviewer_mutants.out.json
- verification/auditor_M2_r1_1/auditor_mutants.out.json

The exact patch strings are in the corresponding .py harnesses.

**O5. Family B is a static PR over spatial cells.** From my probe on the pinned `token_job/*_token_spectra.npz`; it reads only spectra and PR keys, never `ids`.

*Numerical rank, counting eigenvalues > 1e-5 × max, per subject:*

| Layer | Primary and L5e-5 | Other zoo checkpoints |
|---|---|---|
| L2, LN0L2, L3 | 7 in every subject | 7 in most subjects, maximum 8–10 |
| L1 (64 cells, ceiling 63) | 50–58 | 29–60 overall |
| L0 (D = 384) | 64–209 overall | |

- The energy criterion is cleaner: the top 7 eigenvalues hold ≥ 0.99994 of the variance at L2 and L3 in all subjects and checkpoints. This is challenger_2's p1d_spectrum.out.txt, and it agrees with my counts.
- Concatenated PR equals the mean per-frame PR to ≤ 2e-4 relative difference in every checkpoint, layer and estimator. Within-subject frame-to-frame SD is 0.16–0.55% of between-subject SD.
- On connectome, challenger_1's probe_connectome_time_invariance.log measured that, at a fixed spatial cell, the share of L3 variance across time is 1e-6 (primary) and 1e-5 (HCP_N400).

**O6. Wrong wording, all in pinned files.**
- Card §5 line 80: "L2, LN0L2, L3: 1120×1536 (ceiling 1119)".
- Report line 102: "very low-dimensional: about 6 of a possible 1119. The dynamic-range fixture … planted ranks of 3, 12 and 40".
- Report line 114: "a 2–5% *increase* in within-window dimensionality".
- Report line 154, row R2: "A token-level collapse FAILS".
- Card §5, H4: "160 tokens … removes the token-count dependence". That is a no-op at L2/L3, where each frame has exactly 160 tokens.
- The card, the report and every test file are pinned in `results/topic3/2026-10-31/output_sha256.txt`. The test files are also pinned in `code_sha256_at_freeze.txt`.

**O7. Minor items from the verifiers, still open.**
- Report rounding. The JSON gives 3.2250 for the A1 lower bound, which the report shows as +3.23; the correct rounding is +3.22. A1b L5e-5 is −3.2849, shown as −3.29; correct is −3.28.
- The addendum 02 copy list leaves out `docs/03_empirical_analysis/empirical_results.json` and `tests/__init__.py`.
- `test_outputs_no_ids.py` ends with `assert n >= 0`, which passes even when nothing is scanned.
- There is no mapping to the G8 labels.
- `results/gpu_ledger_2026-10-31.md` does not exist.
- Run-level C4: root's background auto-commit and push. This is root's issue, not M2's.

## 2. Logic chain

1. The production rules follow card §5 (O1), and the frozen verdicts reproduce (O3). So no result is wrong, and a rerun would gain nothing: the C3 order is already satisfied, and rerunning only risks the pins.
2. The fixtures cannot tell the correct rule from broken ones (O2, O4), and one broken rule would flip a real verdict (O3). That fails C3's requirement that fixtures fail on the targeted defect. The fix is tests only.
3. The pinned test files cannot be edited (O6). New tests must go in a new file under `tests/topic3_spectral/`. Existing `sha256sum -c` checks list only the old files, so a new file leaves every pin valid. A new receipt pins the new file.
4. Each surviving mutant needs a fixture that separates it from the correct code:
   - Sign: significant zoo checkpoints of the opposite sign.
   - Primary CI: p_holm < 0.05 with the CI covering 0.
   - Raw p vs Holm: a zoo checkpoint with p_signflip < 0.05 ≤ p_holm.
   - Threshold 0.5: a primary with 0.05 ≤ p_holm < 0.5.
   - D1 and D3: stub the interval function so lo < 0 < point < hi, use cov lo > 0 with corr lo ≤ 0, and use one D3 pair failing.
   - H1a wiring: an exact TOKEN_PRIMARY assertion, plus a behavioural case where L2 is systematically shifted from LN0L2.
   - SE factor: an analytic oracle at m far from n/2.
   - Jackknife: on the mean estimator, the jackknife SE equals sd(ddof=1)/√n exactly.
   - Sign-flip: on extreme d, p = 1/(B+1) exactly.
   The real-JSON regression test kills N05 and N08 on the real case. N06 and R8 never change the real outcome, so they need synthetic fixtures.
5. Family B: under O5, the per-subject PR at L2, LN0L2 and L3 is the PR of about 8 near-static spatial-cell vectors, so its effective ceiling is 7. That changes how H1a and the R2 row read, but not the rule outcomes, because H1a and H1b are defined as exactly these contrasts. The pinned report cannot be edited, so a dated addendum 03 must supersede the quoted sentences. New derived numbers in it are post-hoc descriptive exposures, labelled as such; they need no new card.
6. O5 also limits how far that restatement goes. The "cells − 1" pattern is exact only at L2, LN0L2 and L3:
   - L1 has numerical rank 50–58, below its ceiling of 63.
   - At L0, D = 384 < 511 cells.
   challenger_2's "511/63/7 in all four layers" overstates this. Repeating it in the addendum would invite a new refutation.

## 3. Caveats

- I did not re-read the VRABES frames on connectome. The time-invariance figure (1e-6) is challenger_1's measurement, covering 3 positions × 2 checkpoints × frames 0 and 3. My evidence is indirect: stored rank, and concatenated PR equal to per-frame PR.
- I did not determine why the tokens are static: input (BOLD fluctuation ≈ 1% of the static signal under znorm_minback), model, or extraction. The addendum must say "cause not determined".
- I relied on challenger_1 for two figures and did not recompute either: between-checkpoint variance about 13× within-checkpoint, and the L1 jackknife SE driven by one subject.
- I did not rerun any mutant harness. Survivor lists come from the verifiers' .out.json files.
- I did not interpret "3번. A". The worker_M2_r1 re-dispatch read it as "resume; reuse saved results", which matches this additive plan.
- Three mutants are near-equivalent: X13 (Marchenko–Pastur universality makes uniform ≈ Gaussian PR), M15 (eps 1e-5 is negligible at real token variances) and M10 (descriptive α only). They can be documented rather than killed, though cheap white-box tests exist for each.

## 4. Conclusion: recommended fix (for a new worker identity, e.g. worker_M2_r2)

1. **New test file** `tests/topic3_spectral/test_verdict_rules.py`; do not edit any existing test or helpers.py.
   - Replication rule, built as hand-made per_ckpt dicts with keys `mean_log_ratio`, `p_holm`, `p_signflip` and `ci95`. Cases:
     - (a) primary significant and positive; zoo: 1 positive significant, 2 negative significant. Expect "not replicated".
     - (b) primary p_holm 0.01 with CI [−0.01, 0.03], and 3 agreeing zoo. Expect "killed (primary CI includes 0)".
     - (c) primary p_holm 0.2 with CI excluding 0. Expect not "holds".
     - (d) 2 agreeing zoo with p_signflip 0.03 but p_holm 0.06. Expect "not replicated".
     - (e) exactly 2 agreeing zoo. Expect "holds"; with exactly 1, "not replicated".
     - (f) direction label for a negative sign.
   - Holm in `token_level_checkpoint`: monkeypatch `analysis.sign_flip_test` to return [0.03, 0.04] and assert both p_holm == 0.06.
   - TOKEN_PRIMARY equals the exact tuples. Add a behavioural H1a case: L2 = LN0L2 × e^{+0.5}, L3 = LN0L2 × e^{−0.5}; assert mean ≈ −0.5 for H1a and −1.0 for H1b.
   - D1 and D3: monkeypatch `analysis.paired_subsample_delta`, `describe_matrix` and `subsample_mean` with stubs returning controlled point, lo and hi. Cases:
     - lo < 0 < point → D1 False;
     - cov lo > 0 with corr lo < 0 → corr False and the "per-channel gain" verdict string;
     - one D3 pair failing → False.
   - Real regression: run `replication_verdict` on `family_B_token_level.json["per_checkpoint"]` with primary "E192_primary"; assert H1a holds and H1b not replicated, and that the H1b zoo agreement count is 1.
   - Numeric oracles:
     - `paired_subsample_delta` at n = 20, m = 15 with explicit index_sets and a column-0-mean estimator: se == sd·√3.
     - `jackknife_pr` with a column-mean estimator: se == sd(ddof=1)/√n.
     - `sign_flip_test` on 57 equal positive values with B = 999: p == 1/1000.
   - Optional white-box tests: iid_reference reproduces `default_rng(seed).standard_normal` draws; layernorm0 eps on a near-constant row; rank_slope window on a kinked spectrum. Otherwise list these three as equivalent mutants with a one-line reason each.
   - Effective-ceiling fixture: 8 random cell vectors, each repeated 140 times plus 1e-6 noise (1120×1536). Assert covPR and corrPR ≤ 7 + 1e-3, and that the concatenated PR equals the single-copy PR.
   - The ID test strengthened in the same new file: scan `results/topic3` for `sub-\d` and assert more than 0 files scanned.
2. **Mutant proof.** Copy the four harnesses into `verification/worker_M2_r2/`:
   - challenger_M2_r1_1/mutants_challenger.py, which needs its `tree` byte copy recreated;
   - challenger_M2_r1_2/probes/p6_mutants.py;
   - reviewer_M2_r1_1/reviewer_mutants.py;
   - auditor_M2_r1_1/auditor_mutants.py.
   Rewrite every output, tree and work path to the worker's own folder. Do not run them in place: they write receipts and rmtree inside the verifiers' folders.
   - The control must pass.
   - **Pass criterion:** every verdict-path mutant in O4 is killed (N05/R1, N06/R3/X12, N08, N09/M20, N10/M22, N11/R9, R8, X06, M14), plus N17 and N02. Only the documented equivalents may survive.
3. **Addendum 03** `docs/03_empirical_analysis/topic3/2026-10-31_topic3_addendum_03.md`. It must:
   - (i) quote and supersede card line 80, report lines 102, 114 and 154 (R2 row), and card §5 H4's "removes token-count dependence". At L2/L3 that subsample is the whole frame;
   - (ii) restate Family B at L2, LN0L2 and L3 as the isotropy of the 8 spatial-cell vectors, which are near-static over time and frames. Effective ceiling 7, stated as top-7 energy ≥ 0.99994. Give medians as a fraction of 7, post hoc: covPR L2 0.77, L3 0.81; corrPR 0.84, 0.88. State that L1 sits below its 63 ceiling (rank 50–58) and that L0 is limited by D = 384;
   - (iii) read H1a as "a 2–5% increase in spread among spatial cells through the stage-3 blocks, norm-matched". Read R2 as "no reduction in spatial-cell spread at token level". The dynamic-range fixture (ranks 12 and 40) does not apply at this shape;
   - (iv) state that replication rests on n = 3 checkpoints, and that between-checkpoint variance is about 13× within-checkpoint. Keep addendum 02's depth confound;
   - (v) state that the L1 jackknife SE is driven by one subject;
   - (vi) correct the rounding: +3.22 and −3.28;
   - (vii) complete the addendum 02 copy list with `empirical_results.json` and `tests/__init__.py`;
   - (viii) map the verdict labels to G8: holds → keep; not replicated → inconclusive; FAILS or killed → stop; untestable or untested → inconclusive (measurement capability);
   - (ix) list every post-freeze real-data quantity with its source probe path. This is the exposure log;
   - (x) say "cause of static tokens not determined";
   - (xi) say that the new tests were added after the results, as guard tests, not as pre-registration.
4. **Receipt** `results/topic3/2026-10-31/addendum_03_sha256.txt`: sha256 of addendum 03 and of the new test file(s). Then rerun every existing `sha256sum -c` check and C1. Run `pytest tests/topic3_spectral`, the old 86-test suite and topic1.
5. **Not in scope:** no new real-data analysis (a time-resolved or within-cell estimand would need a new card and is exploratory); no H2; no GPU; no connectome writes.

## 5. Verification method

- `PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_M2_r2_1/probe_r2_a_verdict_regression_and_rank.py` reproduces O3 and O5. It is read-only and never touches `ids`.
- `sed -n 184,199p src/topic3_spectral/analysis.py` and `sed -n 46,70p tests/topic3_spectral/test_analysis.py` show O1 and O2.
- `grep -n -E "1119|within-window|token-level collapse" docs/03_empirical_analysis/topic3/*.md` shows O6.
- After the fix:
  - `sha256sum -c results/topic3/2026-10-31/{output_sha256,code_sha256_at_freeze,addendum_02_sha256,addendum_03_sha256}.txt`. Only the disclosed launcher line may fail.
  - The copied harnesses report 0 verdict-path survivors.
  - The H1b sign test fails when the line-193 condition is removed from a copy.
- Invalidation: if any existing pinned file changes, or if a fixture passes on a mutant listed in step 2, the fix is incomplete.
