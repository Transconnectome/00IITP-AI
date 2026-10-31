# Topic 3 addendum 03: what Family B measures, verdict-logic tests, reading limits and errata (2026-10-31)

Written 2026-10-31 at about 12:30Z by worker_M2_r2 (M2 iteration 2). It is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report, and addenda 01 and 02 are unchanged and stay pinned in `results/topic3/2026-10-31/output_sha256.txt` and `addendum_02_sha256.txt`. The sha256 of this file and of the two new test files is in `results/topic3/2026-10-31/addendum_03_sha256.txt`.

**No verdict changes.** No code in `src/topic3_spectral/` or `scripts/topic3_*.py` was changed, nothing was rerun, and no card was re-frozen. Every rule outcome in report §4 still follows from card §4–§5 applied to the pinned JSON. This addendum restricts how two of those outcomes may be read (items 1–2), records the reading limits found in review (item 3), adds guard tests (item 4), and corrects four text errors (item 5).

Every real-data number below was computed **after** the freeze and after the results were known. All of them are **post hoc and descriptive**. None of them governs a verdict. Their sources are listed in the exposure log (item 7).

## 1. Family B at L2, LN0L2 and L3 measures the spread of about 8 near-static spatial-cell vectors

**What the token matrix contains.** At L2, LN0L2 and L3 each window has 8 spatial cells × 20 time steps = 160 tokens. A subject's 7 frames give 1120 × 1536.

**What the saved spectra show** (`results/topic3/2026-10-31/token_job/*_token_spectra.npz`, all 57 subjects × 4 checkpoints; probe `verification/worker_M2_r2/probes/probe_addendum03_numbers.py`):

| Quantity at L2 / LN0L2 / L3 | Value |
|---|---|
| Share of variance in the top 7 eigenvalues | ≥ 0.99994 in every subject and checkpoint (minimum 0.999942) |
| Eigenvalues above 1e-5 × max | median 7 in every checkpoint; maximum 7 (primary, L5e-5 at L2/LN0L2), up to 8–10 in the other zoo checkpoints |
| \|log concatenated covPR − log mean per-frame covPR\| | ≤ 1.2e-4 (maximum over subjects, layers, checkpoints) |
| Within-subject SD of per-frame covPR ÷ between-subject SD | 0.003–0.005 |
| H4 160-token value ÷ per-frame value | exactly 1.0000 (the subsample is the whole frame) |

An independent direct check on the raw frames on connectome (challenger_M2_r1_1, `verification/challenger_M2_r1_1/probe_connectome_time_invariance.py`; 3 subject positions × 2 checkpoints) found that, at a fixed spatial cell, about 1e-6 (primary) and about 1e-5 (HCP_N400) of the L3 token variance lies across the 20 time steps.

**Reading.** Token PR at L2, LN0L2 and L3 is, to within 6e-5 of the variance, the PR of the 8 spatial-cell embedding vectors. These vectors barely change across time steps or across the 7 frames. The effective ceiling of this PR is **7** (cells − 1), not 1119. Concatenating 7 frames adds almost nothing.

Against that ceiling, the primary checkpoint's medians are (post-hoc descriptive fractions of 7):

| | L2 | L3 |
|---|---|---|
| covPR | 5.41 (0.77 of 7) | 5.67 (0.81 of 7) |
| corrPR | 5.88 (0.84 of 7) | 6.14 (0.88 of 7) |

**Other layers.** The "cells − 1" reading applies only at L2, LN0L2 and L3.
- L1 (64 cells, D = 768): ≥ 0.99994 of the variance lies in the top 63 eigenvalues in every subject and checkpoint. The count above 1e-5 × max is 29–60 (primary 50–55), so L1 sits below its 63 ceiling.
- L0 (512 cells, D = 384): the rank is limited by D = 384. The cell count gives no informative ceiling. The count above 1e-5 × max is 64–209.

**Cause not determined.** I did not determine why the tokens are almost constant over time: the input, the preprocessing or the model. Finding out would need a new real-data exposure and its own card.

## 2. Passages superseded (the pinned files themselves are not edited)

| Location | Pinned text | Superseded reading |
|---|---|---|
| Card §5, line 80 | "L2, LN0L2, L3: 1120×1536 (ceiling 1119)" | The shape is 1120 × 1536. The effective ceiling of the PR is 7, the 8 near-static spatial cells minus 1 (item 1). |
| Card §5, line 98 (H4) | "… which removes the token-count dependence" | At L2, LN0L2 and L3 the 160-token subsample is the whole frame, so H4 removes nothing there. It subsamples only at L0 and L1. The L0→L3 H4 profile compares effective ceilings of 383 (D-limited), 63, 7 and 7, so it cannot be read as dimensionality changing with depth. |
| Report §3, line 102 | "Within-window token representations are very low-dimensional: about 6 of a possible 1119." | The primary sits at 77–88% of its effective ceiling of 7 (item 1). "Very low-dimensional" is not supported. |
| Report §3, line 102 | "The dynamic-range fixture shows that corrPR at this shape can resolve planted ranks of 3, 12 and 40." | The fixture is correct but does not apply: the real matrices have rank about 7, so ranks 12 and 40 cannot occur. |
| Report §3, line 114 | "a 2–5% *increase* in within-window dimensionality through the stage-3 blocks, with the norm matched" | A 2–5% increase in the spread (isotropy) of the 8 spatial-cell vectors through the stage-3 blocks, with the norm matched, in the primary and the two deep NewUAH checkpoints. Within-window *temporal* dimensionality is not measurable with these data. |
| Report §4, line 154 (R2 row) | "A token-level collapse FAILS." / "not the dimensionality of the token representation" | No reduction in the spread of the spatial-cell vectors at token level (3 of 4 checkpoints; the depth-matched HCP_N400 reduces it by 13%, see addendum 02). Nothing is shown about temporal dimensionality. |

**Rule outcomes stand.** H1a and H1b are defined as exactly these contrasts, so "H1a holds" and "H1b not replicated" are unchanged. Only their wording changes.

## 3. Reading limits

- **The replication unit is the checkpoint, n = 3.** Per-subject log ratios within one checkpoint are very precise (Holm p 0.0002, CIs about ±0.002). Between checkpoints the means vary much more. The variance of the checkpoint means, divided by the mean within-checkpoint variance between subjects, is 13.4 for H1a and 5.8 for H1b (probe, `checkpoint_variance`). So subject-level precision says nothing about generalisation. The replication rests on 3 zoo checkpoints, and addendum 02 shows they confound depth with training family: the two that agree on H1a are `2 2 42 4` NewUAH models, and the only depth-matched one (HCP_N400) reverses H1a and H1b.
- **One subject drives the L1 jackknife SE.** Report §2 line 49 says L1 "is driven by a few subjects". The full-sample L1 covPR is 2.78 and the jackknife SE is 3.58. One leave-one-out value is 6.39; the next highest is 2.84 and the median is 2.75. Without that single term the SE would be 0.149. So it is one subject, not a few (probe, `l1_jackknife`; external input `VRABES/RemissionAnalysis/pooled_E192_layers/layer_1.npz`, array key only).
- **Label for one unreachable case.** Card §5 names "killed" only for "the primary CI includes 0". `analysis.replication_verdict` gives that same label to any primary that is not significant, including Holm p ≥ 0.05 with a CI that excludes 0. The label is imprecise for that case. It does not arise in the real data: every primary Holm p is 0.0002 and every primary CI excludes 0. The code is not changed.

## 4. Verdict-logic guard tests (added after the results)

Two new files, written **after** the real-data results existed. They guard against regressions; they are not a pre-registration. No existing test and no `src/` file was edited.

- `tests/topic3_spectral/test_verdict_rules.py`: 30 tests. Base: explorer_M2_r2_3's draft (sha256 `69fbd923e5b33c6393f15fcc02a26dc0126a444fd4508948c27c7892be95cad6`), extended by worker_M2_r2. It pins:
  - the card §5 replication rule, using hand-built per-checkpoint inputs: a significant zoo checkpoint of the opposite sign does not count; a primary CI covering 0 kills even when p is small; Holm p is used, not raw p; the boundary at Holm α = 0.05; 2 of 3 agreeing zoo checkpoints vs 1 of 3; the primary is not its own replicate;
  - the literal H1a/H1b/H1c–e pair wiring, and a functional orientation case with L2 shifted away from LN0L2 in both the corr and cov families;
  - Holm applied within each checkpoint;
  - card §4 D1 (lower bound, not point or upper bound; corr checked as well as cov; the "per-channel gain" branch) and D3 (all pairs, cov), through a stub of `paired_subsample_delta`;
  - the descriptive formulas: jackknife (n−1)/n factor and bias correction; subsampling SE √(m/(n−m)) at m ≠ n/2; the sign-flip 1/(B+1) floor; LN eps; the rank-slope window; the iid reference as Gaussian draws;
  - a regression on the pinned `family_B_token_level.json`: the shipped rule reproduces "H1a holds" (2 of 3 zoo checkpoints agree) and "H1b not replicated" (1 of 3), and all 3 zoo checkpoints are Holm-significant for H1b, so only the sign condition keeps H1b from "holds";
  - the effective-ceiling fixture of item 1: 8 cell vectors × 140 copies plus 1e-6 noise give PR ≤ 7, equal to the PR of one static copy.
- `tests/topic3_spectral/test_outputs_scanned_nonempty.py`: 1 test. The pinned `test_outputs_no_ids.py` ends with `assert n >= 0`, which also passes on an empty tree. This companion requires a non-empty scan (the family B JSON and ≥ 4 npz files present) and repeats the BIDS subject-ID prefix check on the text files.

Mutation evidence (verifier harnesses rerun from copies in `verification/worker_M2_r2/mutants/`) is recorded in that folder's `MUTANTS_SUMMARY.json` and in the worker_M2_r2 handoff.

## 5. Errata (text only)

| Location | Printed | JSON value | Correct rounding |
|---|---|---|---|
| Report §2 line 55, A1 L2 − L3 covPR lower bound | +3.23 | 3.2249865 (`family_A_subject_level.json`, `A1_swift_pairs/L2_minus_L3/cov/lo`) | +3.22 |
| Report §2 line 68, A1b L5e-5 ΔcorrPR | −3.29 | −3.2848924 (`family_B_token_level.json`, `A1b_ln_matched_subject_level/zoo_NewUAH_deepE192_L5e-5/L3_minus_LN0L2_corr/point`) | −3.28 |
| Report §2 line 49 | "driven by a few subjects" | — | driven by one subject (item 3) |
| Addendum 02 §2, step 1 copy list | `src/`, `scripts/`, `tests/`, `docs/03_empirical_analysis/topic3/`, `results/topic3/2026-10-31/` | — | Also copy `docs/03_empirical_analysis/empirical_results.json`, which `scripts/topic3_provenance_repro.py` reads, and make sure `tests/__init__.py` comes along (it does if all of `tests/` is copied; harnesses that copy only `tests/topic3_spectral/` must add it). |

## 6. Mapping to the sci-pipeline G8 labels

| Card / report label | G8 label |
|---|---|
| holds / HOLDS | keep |
| not replicated | inconclusive |
| killed / FAILS | stop |
| untested / UNTESTABLE | inconclusive (failure type: measurement capability) |
| NOT SUPPORTED (R4, R6) | stop |
| reproduces descriptively, no verdict (R1); not comparable (R7) | inconclusive |

Applied to the M2 outcomes: H1a keep, but per items 1–3 it means a small increase in the spread of 8 spatial-cell vectors, replicated only in the two deep NewUAH checkpoints. H1b inconclusive. H2 inconclusive. J1 stop. R2 mechanism stop; subject-level drop keep; token-level part restated in item 2. The PI decides whether the gate passes.

## 7. Exposure log: real-data quantities computed after the freeze (08:48:29Z)

All are post hoc and descriptive. None changed a verdict.

| Who | What | Source |
|---|---|---|
| explorer_M2_r1_3 | seed-7 subsampling of L2 − L3, leave-one-subject-out influence, full-n LN-matched corrPR contrast, Family B means | `verification/explorer_M2_r1_3/probe_e_r2_independent_recompute.py` |
| reviewer_M2_r1_1 | independent recomputation of all subject-level PRs and H1 means; raw-frame spot check of 2 subject positions on connectome | `verification/reviewer_M2_r1_1/indep_recompute.py`, `connectome_spotcheck.py` |
| reviewer_M2_r1_2 | full rerun in a copied tree; covPR from stored eigenvalues | `verification/reviewer_M2_r1_2/r2_1117/` (`compare.py`, `npz_consistency.py`, `rerun_outputs/`) |
| challenger_M2_r1_1 | Family A/B recomputation, jackknife, the N05 effect on the real verdict, raw-frame time invariance on connectome | `verification/challenger_M2_r1_1/probe_family_A.py`, `probe_family_B.py`, `probe_jackknife.py`, `probe_N05_real_impact.py`, `probe_connectome_time_invariance.py` |
| challenger_M2_r1_2 | independent Family A/B, per-frame and between-subject spread, top-7 energy, T3.1 check | `verification/challenger_M2_r1_2/probes/p1_familyB_indep.py`, `p1b_frames.py`, `p1c_between.py`, `p1d_spectrum.py`, `p4_familyA_indep.py`, `p7_t31_and_affine.py` |
| auditor_M2_r1_1 | copied-tree rerun and JSON comparison; own L1 jackknife and H1 means | `verification/auditor_M2_r1_1/compare_json.py`, `rerun_outputs/` |
| explorer_M2_r2_1 | verdicts with and without the sign condition; numerical rank per layer | `verification/explorer_M2_r2_1/probe_r2_a_verdict_regression_and_rank.py` |
| explorer_M2_r2_2 | rank and energy ceilings, checkpoint variance ratio, L1 leave-one-out | `verification/explorer_M2_r2_2/probe_rank_ceiling.py`, `probe_checkpoint_variance.py`, `probe_l1_jackknife.py` |
| explorer_M2_r2_3 | rank and energy from the saved spectra | `verification/explorer_M2_r2_3/probe_a_saved_spectra_rank.py` |
| worker_M2_r2 | every number in items 1, 3 and 5 of this addendum | `verification/worker_M2_r2/probes/probe_addendum03_numbers.py` (output `probe_addendum03_numbers.out.json`) |

No new real-data estimand (time-resolved or within-cell) was computed for this addendum. Any such analysis would need its own frozen card.

## 8. Compute

0 GPU-hours. Nothing was sent to B300. No connectome job was run for this addendum. Local CPU only: one probe, pytest runs and mutant runs in copied trees, all under nice.
