# Topic 3 addendum 05: M2 iteration 3 — guard tests for the blocking classes of the r2b gate, union mutation run, corrections to addenda 03/04 and the report (2026-11-01)

Written 2026-11-01 (UTC) by worker_M2_r3, the iteration-3 worker of M2. The PI approved iteration 3 on 2026-11-01 (`.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md`, decision 1). This addendum is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report and addenda 01–04 are unchanged. They stay pinned in `results/topic3/2026-10-31/output_sha256.txt` and `addendum_02/03/04_sha256.txt`, and all four receipts verify (§7). The sha256 of this file and of the two new test files is in `results/topic3/2026-10-31/addendum_05_sha256.txt`.

**No verdict changes.**
- No file in `src/` or `scripts/` was changed. No card was re-frozen. No new real-data estimand was computed.
- No real-data analysis was rerun to produce a result. One new test re-derives the pinned Family B output inside pytest's temporary directory and compares it with the pinned file (§2, class 5). That output is discarded with the temporary directory, and nothing is written to the production tree.
- The verdicts in report §4 stand: H1a holds, H1b not replicated, D1 robust and not a per-channel-scale effect, D3 ordering reproduces, J1 artefact, H2 untested.

## 1. Outcome of the r2b gate (iteration 2)

Source: `.agents/teamwork/tw-20261031-four-topics/orchestrator/M2_r2b_gate_record.json` and each agent's `handoff.md`.

| Agent | Verdict | Blocking items |
|---|---|---|
| worker_M2_r2b | DONE | none (its claim: 67 of 67 assigned mutants killed after adding `test_verdict_rules_r2b.py`) |
| reviewer_M2_r2b_1 | REQUEST_CHANGES | B1 primary uses raw p (V01); B2 the CI produced by `paired_log_contrast` is untested (P01 ratio scale, P02 50% level, P03 [hi, lo]); B3 A2/D3 rows (A01); B4 addendum 03 §4 overstates "Holm p is used, not raw p" |
| reviewer_M2_r2b_2 | REQUEST_CHANGES | V01 |
| challenger_M2_r2b_1 | REFUTED | V01; V06/V07/V08 (CI [hi, lo], ratio scale, 50%); V05 (zoo also needs its CI to exclude 0); V26 (`topic3_token_stats.py` passes a zoo checkpoint as the primary; flips the real H1a with the suite green) and V29 (one zoo checkpoint dropped) |
| challenger_M2_r2b_2 | REFUTED | A07 (ci95 stored as [hi, lo]) |
| auditor_M2_r2b_1 | CLEAN | none |

The gate failed. MAX_ITER = 2 had been reached, so the root stopped for the PI. The PI's decision 1 allows iteration 3: additive guard tests and this addendum, with no `src/` or `scripts/` change and no rerun, followed by a 5-verifier gate and the victory audit.

## 2. The five blocking classes and the tests that close them

Two new files, written **after** the real-data results existed (33 tests; the suite now has 121):
- `tests/topic3_spectral/test_verdict_rules_r3.py` (27 tests): unit-level guards.
- `tests/topic3_spectral/test_token_stats_wiring_r3.py` (6 tests): driver-script wiring.

No existing test, no `tests/topic3_spectral/helpers.py`, and no `src/` or `scripts/` file was edited. Each mutant below is reproduced verbatim from the verifier's own harness file (§4) and shown in copied trees to **survive** the shipped 88-test suite and to be **killed** by the r3 tests. Union job ids (Unnn) refer to `verification/worker_M2_r3/mutants/MUTANTS_SUMMARY.json`.

| Class (card rule) | Mutants (union job: harness ids) | r3 tests that fail on them |
|---|---|---|
| 1. The primary needs **Holm** p < 0.05 (card §5 replication rule) | U057: reviewer_1 V01 = reviewer_2 V01 = challenger_1 V01 (`analysis.py:191` reads `p_signflip`) | `test_primary_raw_p_below_alpha_but_holm_p_not_is_not_significant[H1a, H1b]` (hand-built: raw p 0.03, Holm p 0.06, CI (0.01, 0.05), 3 agreeing zoo checkpoints; must give `primary_significant` False and not "holds"); `test_primary_holm_rule_end_to_end_at_card_resolution[H1a, H1b]` (the shipped producer at B = 9999: raw p 0.0326, Holm p 0.0652, CI lower bound 0.0007 > 0) |
| 2. The CI the rule reads is the 95% subject-bootstrap CI of mean d, d = log a − log b (card §5 "Test") | U070: reviewer_1 P01 = challenger_1 V07 (CI of exp(d)); U071: reviewer_1 P02 (50% at the call site); U105: challenger_1 V08 (`level=0.5`); U072: reviewer_1 P03 = challenger_1 V06 = challenger_2 A07 (`ci95` stored as [hi, lo]) | `test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio` (`ci95` equals an independently written B = 9999 percentile bootstrap of mean d in [lo, hi] order; lo < mean < hi; half-width within 10% of 1.96·sd/√n; `p_signflip` equals an independently written sign-flip p); `test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end[H1a, H1b]` (skewed log ratios through `token_level_checkpoint`: Holm p 0.032 / 0.031 from the shipped code, computed CI lower bound −0.0014, 3 agreeing zoo checkpoints, verdict must be "killed (primary CI includes 0)") |
| 3. A zoo checkpoint agrees on same sign and Holm p < 0.05 only; its CI is not required to exclude 0 | U066: reviewer_1 V10 = challenger_1 V05 | `test_zoo_with_holm_p_below_alpha_counts_even_if_its_ci_covers_zero[H1a, H1b]` (hand-built); `test_computed_zoo_with_ci_covering_zero_counts_end_to_end[H1a, H1b]` (the computed class-2 checkpoint in a zoo slot: "holds", 2 of 3) |
| 4. A2/D3 use the 25 NeuroSTORM positions (card §4 A2) | U078: reviewer_1 A01 = challenger_1 V13 = challenger_2 A06 (`X[pos]` → `X[:pos.size]`); U120: challenger_1 V28 and U139: challenger_2 S03 (`topic3_subject_level.py` passes positions 0..24) | `test_a2_d3_use_the_neurostorm_positions_not_the_first_rows` (row identity: both cross-model pairs, for cov and corr, receive BrainJEPA/BrainLM restricted to the positions, and NeuroSTORM; every A2 E1 covPR equals covPR of those rows; at least 8 of the 25 positions are above 24); `test_subject_level_script_passes_the_neurostorm_alignment_positions` (the script, loaded from the tree under test with synthetic stand-ins for the pinned loaders, must pass the alignment's positions to `subject_level`; nothing is written) |
| 5. `topic3_token_stats.py` uses the card primary and all 3 zoo checkpoints (card §2, §5, §9) | U118: challenger_1 V26 = challenger_2 S01 (`ZOO[0]` as primary); U091: reviewer_1 X02 (`ZOO[2]` as primary); U090: reviewer_1 X01 = challenger_1 V29 = challenger_2 S04 (HCP zoo dropped) | `test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo` (see below); `test_token_stats_script_uses_the_card_primary_when_every_choice_gives_a_different_verdict` (kills X02, see below) |

**Class 5 in detail.** The first test copies the script, `src/topic3_spectral/*.py`, the frozen card and its hash record, the alpha calibration and the pinned token-job npz/json files from the tree under test into pytest's `tmp_path`. The pinned `family_B_token_level.json` is not copied. It then runs the unmodified script there. Because `scripts/topic3_common.py:12` derives `OUT` from the script's own location, the output lands in `tmp_path`. The test asserts that:
- the script exits 0 and prints a path inside `tmp_path`;
- the primary, identified **from the data**, is used. That is the one checkpoint whose pooled L3 equals the pinned `layer_3.npz` at atol = rtol = 1e-5, which is card §2's re-pool provenance proof;
- the checkpoints are exactly that primary plus `zoo_<name>` for the 3 names in card §2;
- the output verdicts equal `replication_verdict` applied with that primary, have `n_other_checkpoints` = 3, and equal the pinned verdicts (H1a holds, H1b not replicated);
- all 508 values outside the `run` block equal the pinned file at rel 1e-9 (the pinned file's sha256 is checked against `output_sha256.txt` first). Code hashes in `run` are deliberately not compared, so the test detects behaviour changes, not byte changes.

**Why a second class-5 test was needed.** With reviewer_1's X02 (L5e-5 as the primary), the script's output on the pinned spectra is identical to the shipped output: L5e-5 also has H1a agreement from 2 of 3 others and H1b agreement from 1 of 3, in the same direction. So the first test cannot see X02; the first full mutant pass showed it survive (`verification/worker_M2_r3/mutants/runs/FULL_v1_SUPERSEDED_README.txt`). The second test re-signs the copied spectra inside `tmp_path`. Within a checkpoint it swaps the two arrays of a contrast, which maps d to −d with the same |d|, the same p and a mirrored CI, and updates the job record's hash. The target design for (H1a, H1b) is primary (+, +), HCP_N400 (+, −), L1e-4 (−, +) and L5e-5 (−, −). On it each of the 4 possible primaries gives a different verdict pair (asserted as a precondition), and the script's verdicts must be those for the card primary. Zoo pooled matrices are cut to 8 columns there, because they only feed the descriptive A1b.

## 3. Nonblocking classes closed in the same files

The dispatch asked to close cheaply the classes named by two or more verifiers. The remaining one-verifier survivors were closed when a small test sufficed.

| Class | Mutants (union job: harness ids) | r3 test |
|---|---|---|
| D2 threshold 0.025, strict (card §4 D2) | U081: reviewer_1 A04 = challenger_1 V14; U126: challenger_2 A14 | `test_d2_is_p_low_strictly_below_0_025[…]`: the column-permutation null is replaced by one of chosen size and count, so p_low is exactly 0.02 (True), 0.03 (False) or 1/40 = 0.025 (False). The shipped iteration-1 test used `colperm_reps = 30`, where p_low ≥ 1/31 > 0.025 and the threshold could not be tested. `test_d2_p_low_is_computed_from_the_seeded_column_permutation_null` checks the formula on a real seeded null. |
| Primary CI touching 0 (card §5 "excluding 0") | U059: reviewer_1 V03 = challenger_1 V03; U060: reviewer_1 V04; U104: challenger_1 V04; U093: reviewer_2 V02 = challenger_2 A01 = auditor A09 | `test_primary_ci_touching_zero_does_not_exclude_zero[…]` (hand-built [0.0, 0.05] and [−0.05, 0.0] with Holm p 0.001: killed) |
| D1 lower bound touching 0 (card §4 D1 "lo > 0") | U079: reviewer_1 A02 = reviewer_2 V03 = challenger_1 V11 = auditor A10; U122: challenger_2 A03; U123: challenger_2 A05 (corr) | `test_d1_interval_touching_zero_is_not_robust` (identical L2 and L3 through the shipped producer give the interval exactly [0, 0] for cov and corr; asserted as a precondition: "drop not robust") |
| D3 lower bound touching 0 | U080: reviewer_1 A03 = reviewer_2 V04 = challenger_2 A04; U108: challenger_1 V12; U143: auditor A11 | `test_d3_needs_both_lower_bounds_strictly_above_zero` (BrainJEPA = BrainLM gives exactly [0, 0], while NeuroSTORM − BrainLM has lo > 0: D3 False) |
| Card §4 parameters | U109–U113: challenger_1 V15–V19 (U110–U113 are also challenger_2 A11, A10, A12, A13); U125: challenger_2 A09 | `test_params_equal_frozen_card`. It checks the card bytes against `card_sha256.txt`, checks that each parameter phrase is present in the card text, and checks that `analysis.PARAMS`, `token_job.SUBSAMPLE_TOKENS`, `estimators.VAR_FLOOR_FRAC` and `LN_EPS` equal the card values. |
| Primary taken by label, not by dict order | U068: reviewer_1 V12; U124: challenger_2 A08 | `test_primary_is_taken_by_label_not_by_dict_order` |
| Statistic definitions and seeds (one verifier each) | U073: reviewer_1 P04 (sign-flip on ratio − 1); U077: reviewer_1 S01 and U133: challenger_2 R03 (ties excluded); U114: challenger_1 V21 (bootstrap never draws the last subject); U115: challenger_1 V22 (tie tolerance 1e-3); U131: challenger_2 R01 (99% level) | `test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio`; `test_sign_flip_p_counts_ties_with_the_observed_statistic` (d = 0.5 × 5: ties for 2 of 32 sign patterns, p about 1/16) |
| Holm p capped at 1 | U134: challenger_2 R04 | `test_holm_adjusted_p_is_a_probability` |
| Zoo mean of exactly 0 has no sign | U065: reviewer_1 V09; U128: challenger_2 A16 | `test_zoo_with_zero_mean_does_not_share_the_primary_sign[…]` (constructed record; through the producer an exactly-zero mean has raw p = 1) |
| H4 subsample: 160 tokens, seed (20261031, position, frame) (card §5 H4) | U088: reviewer_1 J02 (seed ignores the frame); U137: challenger_2 T01 (never subsamples) | `test_h4_subsample_is_160_tokens_seeded_by_seed_position_frame` (7 identical frames; per-frame values must equal an exact replay of the seeded draw) |
| A1b orientation; script seed shift | U082: reviewer_1 A05 = challenger_2 A21; U138: challenger_2 S02 | the full-value comparison in `test_token_stats_script_reproduces_pinned_family_b_…` |
| Card §9 refusals of `topic3_token_stats.py` | U117: challenger_1 V25 and U140: challenger_2 S05 (`verify_card` bypassed); U141: challenger_2 S06 (npz hash guard off); U119: challenger_1 V27 = challenger_2 S07 (re-pool halt removed) | `test_token_stats_refuses_an_edited_card`, `…_a_spectra_hash_mismatch`, `…_a_failed_repool_provenance_check` (each in a full copied tree, so that a bypassed guard leads to rc 0 and a written output, which the test rejects) |

## 4. Union mutation run

**What was run.** The union of every mutant set named in the iteration-3 dispatch, read directly from the harness source files by `verification/worker_M2_r3/mutants/union_specs.py`. That script parses each file with `ast` and evaluates only its string constants and the mutant literal, with no builtins except `dict`; no harness is imported or executed.

| Set | Harness file (sha256 prefix) | Rows |
|---|---|---|
| worker_M2_r2b's 67: C | `verification/challenger_M2_r1_1/mutants_challenger.py` (`4a63b8b6f5a5`) | 28 |
| worker_M2_r2b's 67: MM | `verification/explorer_M2_r2_2/mini_mutants.py` (`8f899e6fa700`) | 18 |
| worker_M2_r2b's 67: KD | `verification/explorer_M2_r2_3/kill_demo.py` (`869b0b581db5`) | 21 |
| reviewer_M2_r2b_1 | `verification/reviewer_M2_r2b_1/mutants/run_my_mutants.py` (`5f2cf23b24e9`) | 35 |
| reviewer_M2_r2b_1, run 2 (challenger replay) | `verification/reviewer_M2_r2b_1/mutants/run_my_mutants_run2.py` (`b501813e2106`) | 8 |
| reviewer_M2_r2b_2 | `verification/reviewer_M2_r2b_2/mutants/run_mutants_rev2.py` (`b983133993e5`) | 25 |
| challenger_M2_r2b_1 | `verification/challenger_M2_r2b_1/mutants/mutant_specs.py` (`b9d5d099fcb8`) | 29 |
| challenger_M2_r2b_2 (own set; its re-check set W is read from the C and MM files above) | `verification/challenger_M2_r2b_2/run_mutants_c2.py` (`724a36a89e32`) | 34 |
| auditor_M2_r2b_1 | `verification/auditor_M2_r2b_1/scripts/run_own_mutants.py` (`1f1a1893d8aa`) | 23 |

That is 221 rows. Identical (file, old, new) patches are merged into one job that keeps every source id, which leaves **151 unique patches**. (reviewer_M2_r2b_1's handoff says its set has 36 mutants; the harness file defines 35, and its `MY_MUTANTS_RUN1.json` records `n_mutants` 35.)

**How.** `verification/worker_M2_r3/mutants/run_union.py`. Each job runs in a fresh copy of the base tree `verification/worker_M2_r3/tree_base_v3`, a byte copy of production built by `make_tree.sh` with its manifest checked. The job applies one patch (the old string must occur exactly once), then runs the topic3 suite with no `-x` under `timeout 900`, 2 jobs at a time, with `PYTHONDONTWRITEBYTECODE=1`. The runner counts a job as KILLED only when rc = 1 and the JUnit report lists at least one failing test. A timeout, a signal or a crash would count as INVALID; none occurred. Two passes were made:
- **s88**: the shipped 88-test suite (the r3 files `--ignore`d). Run 2026-11-01T03:38:59Z–04:03:23Z, `runs/S88_v2.json` (sha256 `34da3012…`). Controls: 88 passed at start and end.
- **full**: the shipped 88 + the 33 r3 tests. Run 04:31:41Z–05:56:06Z, `runs/FULL_v2.json` (sha256 `e222e7f2…`), with the base tree's r3 files at sha256 `58c64ccb…` and `b091b0b8…` (= the pinned files). Controls: 121 passed at start and end, 0 skipped. The base tree also carried a draft of this addendum (it was copied from production while being written). Its bytes can only affect the shipped ID-scan tests, which pass on the draft and on the final file (§7), so the run was not repeated.

| Pass | KILLED | SURVIVED | INVALID | NOT_APPLIED |
|---|---|---|---|---|
| s88 (shipped 88) | 101 | 50 | 0 | 0 |
| full (88 + r3) | 150 | 1 | 0 | 0 |

All 50 s88 survivors are survivors that the r2b verifiers reported, so each was reproduced from the verifier's own harness. 49 of them are killed by r3 tests, and in every one of the 49 at least one r3 test is among the failing tests. The table lists them; the 101 patches killed in both passes are omitted here and listed in `verification/worker_M2_r3/mutants/MUTANTS_SUMMARY.json` (sha256 `fa7017ac…`), which also holds each job's raw-log path and log sha256 (raw logs in `runs/S88_v2_logs/` and `runs/FULL_v2_logs/`).

| Job | Source ids (harness:id) | File | Shipped 88 | 88 + r3 | Killing r3 tests |
|---|---|---|---|---|---|
| U091 | RV1:X02_script_primary_label | scripts/topic3_token_stats.py | SURVIVED | KILLED | test_token_stats_script_uses_the_card_primary_when_every_choice_gives_a_different_verdict |
| U057 | RV1:V01_primary_uses_raw_p; RV2:V01_primary_uses_raw_p; CH1:V01_primary_uses_raw_p | analysis.py | SURVIVED | KILLED | test_primary_holm_rule_end_to_end_at_card_resolution, test_primary_raw_p_below_alpha_but_holm_p_not_is_not_significant |
| U059 | RV1:V03_ci_lo_ge0; CH1:V03_primary_ci_lo_ge0 | analysis.py | SURVIVED | KILLED | test_primary_ci_touching_zero_does_not_exclude_zero |
| U060 | RV1:V04_ci_hi_le0 | analysis.py | SURVIVED | KILLED | test_primary_ci_touching_zero_does_not_exclude_zero |
| U065 | RV1:V09_zoo_zero_mean_agrees | analysis.py | SURVIVED | KILLED | test_zoo_with_zero_mean_does_not_share_the_primary_sign |
| U066 | RV1:V10_zoo_also_needs_ci; CH1:V05_zoo_also_requires_ci | analysis.py | SURVIVED | KILLED | test_computed_zoo_with_ci_covering_zero_counts_end_to_end, test_zoo_with_holm_p_below_alpha_counts_even_if_its_ci_covers_zero |
| U068 | RV1:V12_primary_is_first_key | analysis.py | SURVIVED | KILLED | test_primary_is_taken_by_label_not_by_dict_order |
| U070 | RV1:P01_ci_on_ratio_scale; CH1:V07_ci_on_ratio_scale | analysis.py | SURVIVED | KILLED | test_computed_zoo_with_ci_covering_zero_counts_end_to_end, test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U071 | RV1:P02_ci_level_050_call_site | analysis.py | SURVIVED | KILLED | test_computed_zoo_with_ci_covering_zero_counts_end_to_end, test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U072 | RV1:P03_ci_bounds_swapped; CH1:V06_ci_bounds_swapped; CH2:A07_ci95_order_swapped | analysis.py | SURVIVED | KILLED | test_computed_zoo_with_ci_covering_zero_counts_end_to_end, test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U073 | RV1:P04_p_on_ratio_minus_one | analysis.py | SURVIVED | KILLED | test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U077 | RV1:S01_signflip_ties_excluded | resampling.py | SURVIVED | KILLED | test_sign_flip_p_counts_ties_with_the_observed_statistic |
| U078 | RV1:A01_ns_alignment_first_rows; CH1:V13_A2_rows_first_25; CH2:A06_A2_first25_rows_not_ns_positions | analysis.py | SURVIVED | KILLED | test_a2_d3_use_the_neurostorm_positions_not_the_first_rows |
| U079 | RV1:A02_D1_cov_lo_ge0; RV2:V03_D1_cov_lo_ge; CH1:V11_D1_cov_lo_ge0; AU:A10_D1_cov_lo_ge | analysis.py | SURVIVED | KILLED | test_d1_interval_touching_zero_is_not_robust |
| U080 | RV1:A03_D3_lo_ge0; RV2:V04_D3_lo_ge; CH2:A04_D3_lo_ge | analysis.py | SURVIVED | KILLED | test_d3_needs_both_lower_bounds_strictly_above_zero |
| U081 | RV1:A04_D2_threshold_005; CH1:V14_D2_threshold_005 | analysis.py | SURVIVED | KILLED | test_d2_is_p_low_strictly_below_0_025 |
| U082 | RV1:A05_A1b_orientation; CH2:A21_A1b_orientation_swapped | analysis.py | SURVIVED | KILLED | test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U088 | RV1:J02_subsample_seed_no_frame | token_job.py | SURVIVED | KILLED | test_h4_subsample_is_160_tokens_seeded_by_seed_position_frame |
| U090 | RV1:X01_script_drops_hcp_zoo; CH1:V29_token_stats_zoo_drops_one; CH2:S04_stats_drops_HCP | scripts/topic3_token_stats.py | SURVIVED | KILLED | test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo, test_token_stats_script_uses_the_card_primary_when_every_choice_gives_a_different_verdict |
| U093 | RV2:V02_primary_ci_closed; CH2:A01_primary_ci_boundary_ge; AU:A09_primary_ci_closed | analysis.py | SURVIVED | KILLED | test_primary_ci_touching_zero_does_not_exclude_zero |
| U104 | CH1:V04_primary_ci_hi_le0 | analysis.py | SURVIVED | KILLED | test_primary_ci_touching_zero_does_not_exclude_zero |
| U105 | CH1:V08_ci_level_50 | analysis.py | SURVIVED | KILLED | test_computed_zoo_with_ci_covering_zero_counts_end_to_end, test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U108 | CH1:V12_D3_lo_ge0 | analysis.py | SURVIVED | KILLED | test_d3_needs_both_lower_bounds_strictly_above_zero |
| U109 | CH1:V15_param_m57_29 | analysis.py | SURVIVED | KILLED | test_params_equal_frozen_card, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U110 | CH1:V16_param_bootstrapB_999; CH2:A11_PARAMS_bootB_999 | analysis.py | SURVIVED | KILLED | test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_params_equal_frozen_card, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U111 | CH1:V17_param_S_200; CH2:A10_PARAMS_S_200 | analysis.py | SURVIVED | KILLED | test_params_equal_frozen_card, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U112 | CH1:V18_param_seed; CH2:A12_PARAMS_seed | analysis.py | SURVIVED | KILLED | test_params_equal_frozen_card, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U113 | CH1:V19_param_m25_13; CH2:A13_PARAMS_m25_13 | analysis.py | SURVIVED | KILLED | test_params_equal_frozen_card |
| U114 | CH1:V21_bootstrap_never_draws_last | resampling.py | SURVIVED | KILLED | test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U115 | CH1:V22_signflip_tie_tolerance_1e-3 | resampling.py | SURVIVED | KILLED | test_computed_zoo_with_ci_covering_zero_counts_end_to_end, test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_holm_rule_end_to_end_at_card_resolution, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U117 | CH1:V25_verify_card_bypassed | scripts/topic3_common.py | SURVIVED | KILLED | test_token_stats_refuses_an_edited_card |
| U118 | CH1:V26_token_stats_wrong_primary; CH2:S01_stats_primary_label_HCP | scripts/topic3_token_stats.py | SURVIVED | KILLED | test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo, test_token_stats_script_uses_the_card_primary_when_every_choice_gives_a_different_verdict |
| U119 | CH1:V27_token_stats_repool_gate_removed; CH2:S07_stats_repool_guard_disabled | scripts/topic3_token_stats.py | SURVIVED | KILLED | test_token_stats_refuses_a_failed_repool_provenance_check |
| U120 | CH1:V28_subject_script_wrong_positions | scripts/topic3_subject_level.py | SURVIVED | KILLED | test_subject_level_script_passes_the_neurostorm_alignment_positions |
| U122 | CH2:A03_D1_cov_lo_ge | analysis.py | SURVIVED | KILLED | test_d1_interval_touching_zero_is_not_robust |
| U123 | CH2:A05_D1_corr_lo_ge | analysis.py | SURVIVED | KILLED | test_d1_interval_touching_zero_is_not_robust |
| U124 | CH2:A08_primary_is_first_checkpoint | analysis.py | SURVIVED | KILLED | test_primary_is_taken_by_label_not_by_dict_order |
| U125 | CH2:A09_PARAMS_m57_27 | analysis.py | SURVIVED | KILLED | test_params_equal_frozen_card, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U126 | CH2:A14_D2_threshold_0p05 | analysis.py | SURVIVED | KILLED | test_d2_is_p_low_strictly_below_0_025 |
| U127 | CH2:A15_direction_label_le | analysis.py | SURVIVED | SURVIVED | **equivalent**: changes only the 'direction' label of a primary whose mean log ratio is exactly 0 ('L3 higher' -> 'L3 lower'). Card §5 defines no direction for a zero mean, so no card-defined output changes; through the shipped producer an exactly-zero mean has raw sign-flip p = 1, so primary_significant, the agreement count and the verdict ('killed') are the same either way. challenger_M2_r2b_2 classified it 'expected equivalent'. Not tested, because any expected label for a zero mean would be invented. |
| U128 | CH2:A16_agree_sign_not_opposite | analysis.py | SURVIVED | KILLED | test_zoo_with_zero_mean_does_not_share_the_primary_sign |
| U131 | CH2:R01_bootstrap_level_0p99 | resampling.py | SURVIVED | KILLED | test_paired_log_contrast_ci_and_p_are_the_card_statistics_of_the_log_ratio, test_primary_holm_rule_end_to_end_at_card_resolution, test_primary_with_computed_ci_straddling_zero_is_killed_end_to_end, test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U133 | CH2:R03_signflip_strict_ties | resampling.py | SURVIVED | KILLED | test_sign_flip_p_counts_ties_with_the_observed_statistic |
| U134 | CH2:R04_holm_no_cap | resampling.py | SURVIVED | KILLED | test_holm_adjusted_p_is_a_probability |
| U137 | CH2:T01_H4_never_subsample | token_job.py | SURVIVED | KILLED | test_h4_subsample_is_160_tokens_seeded_by_seed_position_frame |
| U138 | CH2:S02_stats_seed_shift | scripts/topic3_token_stats.py | SURVIVED | KILLED | test_token_stats_script_reproduces_pinned_family_b_with_card_primary_and_all_zoo |
| U139 | CH2:S03_subject_level_wrong_ns_positions | scripts/topic3_subject_level.py | SURVIVED | KILLED | test_subject_level_script_passes_the_neurostorm_alignment_positions |
| U140 | CH2:S05_verify_card_disabled | scripts/topic3_common.py | SURVIVED | KILLED | test_token_stats_refuses_an_edited_card |
| U141 | CH2:S06_stats_npz_hash_guard_disabled | scripts/topic3_token_stats.py | SURVIVED | KILLED | test_token_stats_refuses_a_spectra_hash_mismatch |
| U143 | AU:A11_D3_lo_ge | analysis.py | SURVIVED | KILLED | test_d3_needs_both_lower_bounds_strictly_above_zero |

**The one survivor.** U127 (challenger_2 A15, `"L3 lower" if sign < 0` → `if sign <= 0`) is **equivalent** with respect to every card-defined output. It changes only the direction label of a primary whose mean log ratio is exactly 0. Card §5 defines no direction for a zero mean. Through the shipped producer an exactly-zero mean has raw sign-flip p = 1, so `primary_significant`, the agreement count and the verdict ("killed") are the same either way. challenger_M2_r2b_2 already classified it as "expected equivalent". The changed `direction` string does appear in the output JSON, and its input is reachable: a = b gives d = 0 exactly, the same construction used for D1/D3. It is not tested, because any expected label for a zero mean would have to be invented. No survivor is classified as measure-zero: every closed-boundary sibling is killed by a constructed fixture (§3).

**Runs not used as evidence** (kept unchanged, each with a README in `runs/`):
- `S88_v1` was aborted at about 03:33Z by a runner bug. The runner wrote the literal `<job tree>` into the JUnit XML, which made it malformed at U022; the main thread then stopped recording while the pool kept running. The fixed runner reran everything as S88_v2.
- `FULL_v1` (base tree with an earlier version of the r3 files) was stopped at about 04:30Z after its 50 priority jobs. In it X02 survived (§2, class 5), the second wiring test was added, and FULL_v2 reran all 151 jobs on the final test files.
- `SMOKE_v2` is a 2-job runner check.

## 5. Corrections found by the r2b verifiers in addenda 03/04 and the report

The pinned files are not edited. The superseded readings are listed here.

| Location | Pinned text | Correction | Found by / evidence |
|---|---|---|---|
| Addendum 03 §4, list of what `test_verdict_rules.py` pins | "Holm p is used, not raw p" | True only for the **zoo** checkpoints (`test_zoo_agreement_uses_holm_not_raw_p`). No test separated raw from Holm p on the **primary** side, because the iteration-2 helper `_rec` sets `p_signflip = p_holm` by default. The primary side is now guarded (§2, class 1). | reviewer_M2_r2b_1 B4, reviewer_M2_r2b_2, challenger_M2_r2b_1 |
| Addendum 03 §2, R2 row | "No reduction in the spread of the spatial-cell vectors at token level (3 of 4 checkpoints; the depth-matched HCP_N400 reduces it by 13% …)" | Holds for the norm-matched **H1a** (log corrPR(L3) − log corrPR(LN0 L2)) only. Under **H1b** (log covPR(L3) − log covPR(L2)), 2 of 4 checkpoints reduce it: HCP_N400 by 10.7% and NewUAH L1e-4 by 3.2% (geometric-mean ratio − 1 from the pinned `family_B_token_level.json`; primary +4.6%, L5e-5 +8.2%). For H1a the figures are HCP_N400 −12.8%, primary +2.3%, L1e-4 +3.9%, L5e-5 +5.0%. | reviewer_M2_r2b_2 (b); recomputed in `verification/worker_M2_r3/probes/check_corrections.out.json` |
| Addendum 03 §2, H4 row | "effective ceilings of 383 (D-limited), 63, 7 and 7" | At L0 the H4 value is computed per frame on 160 subsampled tokens (`src/topic3_spectral/token_job.py` lines 82–86), so it has at most **159** eigenvalues: the ceiling is n-limited, not D-limited. The concatenated L0 matrix stores 384 eigenvalues, not 383 (`cat_cov_eigs__L0` has 384 columns). The reading ("cannot be read as dimensionality changing with depth") stands. challenger_M2_r2b_2 adds that, if the cells are near-static, a 160-token draw covers on average about 138 of the 512 L0 cells and 59.6 of the 64 L1 cells. | challenger_M2_r2b_1 (H4 row), challenger_M2_r2b_2 R-2; `check_corrections.out.json` (`centered_eigs` on 160 × 384 returns 159 values) |
| Addendum 03 header | "Written 2026-10-31 at about 12:30Z" | Written at **12:17:16Z** (the native transcript has the single Write at 12:17:16.770Z, 10 s before the interruption at 12:17:26Z). Git gives an independent upper bound: the file first entered git in root checkpoint `4ce1917` (2026-10-31T12:31:25Z). | auditor_M2_r2b_1 O2 and L1; reviewer_M2_r2b_1/2; challenger_M2_r2b_1 O12 |
| Addendum 03 §3, heading "Label for one unreachable case" | the "killed (primary CI includes 0)" label given to a primary with Holm p ≥ 0.05 and a CI that excludes 0 | The case is reachable on synthetic inputs at the card's B = 9999: `test_primary_holm_rule_end_to_end_at_card_resolution` builds one (raw p 0.0326, Holm p 0.0652, CI [0.0007, 0.0103]). It does not arise in the real data, where every primary Holm p is 0.0002. The code is not changed, and the r3 test asserts only "not holds". | challenger_M2_r2b_1 O8 |
| Report §5, line 166 | "very precise (CIs of about ±0.003 in log ratio)" | The CI half-widths of the primary contrasts are **0.0020–0.0144** across the 4 checkpoints (H1a 0.0020–0.0096, H1b 0.0039–0.0144). Addendum 04 §6 already corrected addendum 03's "about ±0.002"; the report line had not been corrected. | reviewer_M2_r2b_1, challenger_M2_r2b_2; `check_corrections.out.json` |
| Addendum 04 §1, row "23:32:58 … root session commit `0db0336` (69 files) includes addendum 03 and both new tests" (also §2, table row "as written by worker_M2_r2 (in `0db0336`)") | | `0db0336` adds the two iteration-2 test files but does not touch addendum 03. `git log` on addendum 03 lists only `4ce1917` (2026-10-31T12:31:25Z, a root checkpoint commit, which first added it) and `ef27b71` (the root's one-line edit). The pre-edit bytes `725d5077…` are the blob first committed in `4ce1917`; `0db0336` only carries it unchanged. | challenger_M2_r2b_1 O12; re-checked read-only with `git log` and `git show <commit>:<path> \| sha256sum` |

Two further context items from the verifiers, recorded here for completeness:
- worker_M2_r2b's handoff (not addendum 04) attributes checkpoint commits `a18006d` and `bd1f991` to addendum 04. Only `e8c795e` and `7430043` touch it (challenger_M2_r2b_2 O11).
- **Stray bytecode from iteration 2.** `src/topic3_spectral/__pycache__/{__init__,estimators,resampling}.cpython-312.pyc` was written into the production tree at 2026-11-01T00:39:14Z, when worker_M2_r2b imported `src.topic3_spectral` from the project root without `PYTHONDONTWRITEBYTECODE` (auditor_M2_r2b_1 N1; reviewer_M2_r2b_1 and _2 saw the same files). These are git-ignored bytecode with no content effect. This worker did not create or remove them; it is the owner's decision whether to delete them. Iteration 3 wrote no bytecode under `src/` or `scripts/` (§7).

## 6. Limits of these tests

- All 33 tests were written **after** the real-data results existed. They are regression guards for the shipped code, not a pre-registration.
- The closed-boundary tests (§3) reach an end point of exactly 0 only with constructed inputs: hand-built records for the primary CI, identical matrices for D1/D3. For real continuous bootstrap or subsampling bounds an exact 0.0 is practically unreachable. The tests pin the card's rule ("excluding 0", "lo > 0", "< 0.025") at the boundary; they say nothing about how often the boundary occurs.
- The D2 threshold test replaces the column-permutation null with one of chosen size and count (so p_low is exactly 0.02, 0.03 or 0.025). A second test checks, on a real seeded null, that p_low is computed by the card formula.
- The exact-replay tests (`_card_bootstrap_ci`, `_card_signflip_p`, the H4 subsample) pin the frozen seed schedule and draw order, not just the statistics' definitions. A future change of seeds or draw order would fail them even if the statistics stayed correct; that is intended while the card is frozen.
- The Family B wiring tests need the pinned VRABES `layer_3.npz` (read-only, sha256-pinned): the first identifies the primary from it, and the script itself compares the primary's pooled L3 with it. They skip if the VRABES checkout is absent, like the existing `test_io_contract.py`. The two script runs add about 16 s and 13 s to the suite, and the three refusal tests about 17 s (only the re-pool refusal runs the full statistics before it halts).
- The Family A script (`topic3_subject_level.py`) is not rerun. Its wiring is checked in-process with synthetic stand-ins for the two pinned loaders, so that test reads no real data. Family A numbers other than the A2 row identity are not re-derived by the r3 tests; the card parameters that define them are pinned by `test_params_equal_frozen_card`.
- H2 (random-init control) remains untested, as card §6 pre-specified.

## 7. Checks, compute and conduct

Run on the production tree on 2026-11-01 at about 06:00Z, with this addendum in place except for this section and without its receipt (logs `verification/worker_M2_r3/final/pre_*`). The same checks were rerun after this file and its receipt were final (`verification/worker_M2_r3/final/post2_*`; an earlier `post_*` run preceded a last wording change in this section and in §4), and those are the results reported to the gate.
- `tests/topic3_spectral`: 121 passed (88 shipped + 33 r3).
- Old suite (`STRICT_E2E=1`, `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed. `tests/topic1_lagmotif`: 88 passed.
- C1 (`LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`): 67 OK, rc 0.
- `output_sha256.txt` 42 OK; `addendum_02_sha256.txt` 1 OK; `addendum_03_sha256.txt` 3 OK; `addendum_04_sha256.txt` 2 OK; `addendum_05_sha256.txt` 3 OK in the post2 run.
- Bytecode: the `.pyc` listing of `src/`, `scripts/` and `tests/` was taken before any work (`verification/worker_M2_r3/pycache_baseline_start.txt`) and again after. No `.pyc` was added. Seven `src/topic4_resu` files that were present at the start have since been removed by another team, and the three iteration-2 files in `src/topic3_spectral/__pycache__` are unchanged (§5). Every pytest and script run used `PYTHONDONTWRITEBYTECODE=1`. One helper call (`python3 -I -c 'import run_union'`; `-I` ignores that variable) left `verification/worker_M2_r3/mutants/__pycache__/run_union.cpython-312.pyc` in this worker's own verification folder; it was deleted. Nothing was written under `src/` or `scripts/`.
- Participant identifiers: none printed or written. A BIDS-prefix scan with no exclusions over this addendum, its receipt, the two new tests, `verification/worker_M2_r3/` and this worker's metadata hits exactly one file: `verification/worker_M2_r3/tree_base_v3/tests/topic3_spectral/test_token_job_driver.py`, the byte copy of the shipped test inside the FULL_v2 base tree, whose names are synthetic. During the runs, each job's temporary copy held the same file; those copies are deleted. The Family B wiring tests read only the pinned spectra npz and the `X` array of the pinned `layer_3.npz`. The Family A wiring test reads no real data.
- Compute: 0 GPU-hours, nothing sent to B300 or connectome; local CPU only, under `nice`, at most 2 pytest processes at a time.
- No git write of any kind. The 15-minute checkpoint commits on this machine are not this worker's. `git log` and `git show` were used read-only for §5.
- Layout lint of the run metadata root (`audit_layout.py`): PASS, no findings.
- Everything written by this iteration: the two test files, this addendum, `results/topic3/2026-10-31/addendum_05_sha256.txt`, `verification/worker_M2_r3/` and `.agents/teamwork/tw-20261031-four-topics/worker_M2_r3/`.
