# Topic 3 addendum 04: completion of M2 iteration 2 — mutation evidence on the shipped tests, one added guard test, number check of addendum 03 (2026-11-01)

Written 2026-11-01 (UTC) by worker_M2_r2b, the resumed iteration-2 worker of M2. It is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report, and addenda 01, 02 and 03 are unchanged; they stay pinned in `results/topic3/2026-10-31/output_sha256.txt`, `addendum_02_sha256.txt` and `addendum_03_sha256.txt`, and all three receipts verify (`verification/worker_M2_r2b/final/`). The sha256 of this file and of the one new test file is in `results/topic3/2026-10-31/addendum_04_sha256.txt`.

**No verdict changes.** No file in `src/` or `scripts/` was changed, nothing was rerun on real data, and no card was re-frozen. This addendum (i) records how iteration 2 was interrupted and where its mutation evidence actually is, (ii) reports the mutation runs against the shipped tests, (iii) adds one guard test file for the one mutant that survived, and (iv) records the result of checking the numbers in addendum 03 items 1, 3 and 5.

## 1. Interruption timeline (UTC)

Sources: file modification times, `git log` per file, and the root's resume note `.agents/teamwork/tw-20261031-four-topics/orchestrator/RESUME_2026-11-01.md`. Times marked *root-reported* come from that note (the root read the native transcript); they could not be checked from files, because the root's later edit overwrote the addendum's modification time.

| Time (UTC) | Event | Evidence |
|---|---|---|
| 2026-10-31 12:10:21 | worker_M2_r2 dispatch saved | mtime of `worker_M2_r2/DISPATCH.md` |
| 12:11:14–12:11:28 | worker_M2_r2 start snapshot, BRIEFING and progress; the last heartbeat reads "Last visited: 2026-10-31T12:12Z" | `verification/worker_M2_r2/prev_snapshot/`, `worker_M2_r2/progress.md` |
| 12:13:28 | `tests/topic3_spectral/test_verdict_rules.py` and `test_outputs_scanned_nonempty.py` written | mtimes |
| 12:14:36–12:15:14 | number probe written and run | `verification/worker_M2_r2/probes/probe_addendum03_numbers.{py,log,out.json}` |
| 12:15:20 | topic3 suite on the production tree: "85 passed in 88.72s" | `verification/worker_M2_r2/pytest_topic3_prod.log` |
| 12:17:16 | addendum 03 written | *root-reported* |
| 12:17:26 | worker_M2_r2 interrupted | *root-reported* |
| 12:17:50 | root `GATE_STATUS.md` written. Its M2 line ("r2 worker returned DONE but did NOT fix tests") does not describe worker_M2_r2's files above and is stale for this question | mtime and text of `orchestrator/GATE_STATUS.md` |
| about 12:2x | workflow wf_59fa8ec4-d01 stopped by the root at weekly usage 94% | `GATE_STATUS.md`, resume note |
| 23:32:58 (2026-11-01 08:32:58 KST) | root session commit `0db0336` (69 files) includes addendum 03 and both new tests | `git log` |
| 23:34:57 | root edit of addendum 03 (one line, §2 below) | mtime of the addendum |
| 23:35:15 | `results/topic3/2026-10-31/addendum_03_sha256.txt` written by the root, not by worker_M2_r2 | mtime; first and only commit `ef27b71` |
| 23:35:29 | root session commit `ef27b71` | `git log` |

worker_M2_r2 left no `handoff.md`, no structured return, and no `verification/worker_M2_r2/mutants/` directory; at 2026-11-01T00:25Z that directory did not exist. The suite run at 12:15:20 happened before the addendum was written, so it never covered the addendum.

These commits were made by the root session, not by a run agent. A host autocommit daemon (chavis-autocommit) is also running on this machine and may commit document files, this addendum included. worker_M2_r2b made no git write of any kind.

## 2. The dangling evidence pointer in addendum 03 and the root's one-line edit

**Dangling pointer.** Addendum 03 §4 (line 73) says: "Mutation evidence (verifier harnesses rerun from copies in `verification/worker_M2_r2/mutants/`) is recorded in that folder's `MUTANTS_SUMMARY.json` and in the worker_M2_r2 handoff." Neither the folder nor the handoff exists. Its §8 lists "mutant runs in copied trees"; no receipt of any such run exists for iteration 2. Those two sentences are superseded by §3–§5 of this addendum.

**Root edit, 2026-11-01 08:34 KST** (`git diff 0db0336 ef27b71 -- docs/03_empirical_analysis/topic3/2026-10-31_topic3_addendum_03.md`). One line changed, in the description of `test_outputs_scanned_nonempty.py` (§4, line 71): the literal BIDS subject-ID prefix token, which had been printed in backquotes, was replaced by the words "BIDS subject-ID prefix". No number, claim or verdict changed.

| Version | sha256 | Literal prefix token in file |
|---|---|---|
| as written by worker_M2_r2 (in `0db0336`) | `725d50771c83988407cfa4778c7437f9caea9bfa7075fb6455e544a32f5cd425` | 1 |
| after the root edit (in `ef27b71`, pinned in `addendum_03_sha256.txt`) | `73489661113bab08736276a23e3e454a9c7a134f060947822cdd09d7893416cf` | 0 |

The edit was necessary for the suite, not cosmetic. On a copied tree holding the pre-edit addendum, both ID-scan tests fail: `test_outputs_no_ids.py::test_no_sub_prefix_strings_and_no_ids_arrays` and `test_outputs_scanned_nonempty.py::test_id_scan_covers_a_nonempty_results_tree_without_sub_prefix` (2 failed; `verification/worker_M2_r2b/probes/pre_edit_addendum03_idscan.log`). So the addendum as worker_M2_r2 wrote it would have turned the topic3 suite red, and the 85-passed receipt from 12:15:20 did not show this because it was earlier. The token was the prefix string itself, quoted as text, not a participant identifier.

## 3. Where the mutation evidence is now

All under `verification/worker_M2_r2b/`:

- `mutants/MUTANTS_SUMMARY.json` — merged result per mutant: source harness and id, file, exact `old` and `new` strings, identical-patch grouping, "what it changes", the failing tests in each run, and log paths.
- `mutants/MUTANTS_RUN1.json`, `MUTANTS_RUN1.progress.log` — run 1, the **shipped** suite (85 tests).
- `mutants/MUTANTS_RUN2.json`, `MUTANTS_RUN2.progress.log` — run 2, the shipped suite plus the new file of §5 (88 tests).
- `mutants/MUTANTS_RUN3.json`, `MUTANTS_RUN3.progress.log` — run 3, a repeat of run 1 (shipped suite, same base tree) made only to regenerate raw logs; see the incident note below.
- `mutants/logs/<job>.log` and `<job>.junit.xml` — raw pytest output and JUnit report of every **run 2** job (69 jobs: 2 controls + 67 mutants).
- `mutants/logs_run3_shipped/<job>.log` and `<job>.junit.xml` — the same for every **run 3** job (69 jobs).
- `mutants/run_mutants.py` (run 3 version), `run_mutants_RUN1_snapshot.py` and `run_mutants_RUN2_snapshot.py` (byte copies of the versions that made runs 1 and 2; their sha256 equal the `runner_sha256` recorded in `MUTANTS_RUN1.json` and `MUTANTS_RUN2.json`), and `build_summary.py`. Between versions only command-line options were added (`--base`, then `--logs` with a refusal to overwrite an existing log directory).
- `tree_base_manifest_sha256.txt` and `tree_base_r2b_manifest_sha256.txt` — sha256 of every file in the two copied trees (144 and 145 files); `make_trees.sh` rebuilds both trees and checks them against these manifests.
- `baseline/` and `final/` — C1 and pin checks before and after the work.

**Incident: run 2 overwrote the raw logs of run 1.** Runs 1 and 2 wrote to the same file names in `mutants/logs/`, so every run-1 log and JUnit file was replaced by its run-2 counterpart (0 of 69 run-1 logs still match the sha256 recorded in `MUTANTS_RUN1.json`; 69 of 69 run-2 logs match). The run-1 per-job record (return code, every failing test, the summary line and the sha256 of the overwritten log) is intact in `MUTANTS_RUN1.json`, but the run-1 log bytes cannot be recovered. Run 3 repeated run 1 with logs in a separate directory: for all 67 mutants its killed/survived status and its set of failing tests equal run 1's (`run3_reproduces_run1` = 67 of 67 in `MUTANTS_SUMMARY.json`), and its controls again gave 85 passed. The raw evidence for the shipped suite is therefore the run-3 logs.

**Method.** Mutant specifications were read from the three source harnesses by parsing their source (`ast`), not retyped, so every `old`/`new` string is verbatim: challenger_M2_r1_1 `mutants_challenger.py` (28 mutants N01–N28; the dispatch named N01–N19, all 28 were run), explorer_M2_r2_2 `mini_mutants.py` (18) and explorer_M2_r2_3 `kill_demo.py` (21; it carries the verbatim patterns of the r1 survivors from reviewer_M2_r1_1, auditor_M2_r1_1 and challenger_M2_r1_2). That is 67 mutants, 56 distinct patches. For each job the runner made a fresh copy of a base tree, applied one patch (the `old` string had to occur exactly once; all 67 did), ran the **full** suite without `-x` so that every failing test is recorded, and deleted the copy. The base tree is a byte copy of `src/`, `scripts/`, all of `tests/` (with `tests/__init__.py`), `docs/03_empirical_analysis/topic3/`, `docs/03_empirical_analysis/empirical_results.json` and `results/topic3/2026-10-31/`; inside it, `output_sha256.txt`, `addendum_02_sha256.txt`, `addendum_03_sha256.txt` and the card hash verify. Two exclusions: `__pycache__` folders, and `scripts/chrome_user_data*` (git-ignored browser profiles, not code, which no test reads). The production tree was never written; after the runs every file in it matched the base-tree manifest. The copied trees were deleted after the runs; `make_trees.sh` rebuilds them.

## 4. Results

| Run | Suite | Control at start / end | Mutants applied | Killed | Survived |
|---|---|---|---|---|---|
| 1 | shipped `tests/topic3_spectral` | 85 passed / 85 passed | 67 of 67 | 66 | 1: `MM 06 zoo <= instead of <` |
| 2 | shipped + `test_verdict_rules_r2b.py` | 88 passed / 88 passed | 67 of 67 | 67 | 0 |
| 3 | shipped `tests/topic3_spectral` (repeat of run 1, separate logs) | 85 passed / 85 passed | 67 of 67 | 66 | 1: `MM 06`; identical to run 1 for every mutant |

No mutant was declared equivalent. Every challenger_M2_r1_1 survivor of iteration 1 (N02, N05, N06, N08, N09, N10, N11, N17) is killed by the shipped suite, and so is every r1 survivor carried in `kill_demo.py` (R1, R3, R4, R7, R8, R11, X06, X12, X13, M10, M14, M15, M20).

**The one survivor is not equivalent.** `MM 06` changes the zoo condition in `analysis.replication_verdict` from `p_holm < holm_alpha` to `p_holm <= holm_alpha`. Card §5 (line 90) says the zoo checkpoints must "show the same sign with Holm p < 0.05", strictly. The boundary can occur: with the card's sign-flip B = 9999 every raw p is a multiple of 1/10000, and Holm over the two primary contrasts maps a raw p of 250/10000 to exactly 0.05 (equal to the float 0.05). A zoo checkpoint at that value would count as agreeing under the mutant but not under the card, so the agreement count and possibly the verdict would change. On the real data it changes nothing: every Holm p in `family_B_token_level.json` is 0.0002.

"Path" in the table: *verdict rule* = the decision code (`replication_verdict`, D1, D3, D2, `TOKEN_PRIMARY`, the Holm step in `token_level_checkpoint`); *verdict input* = a statistic a decision reads (p-values, Holm, intervals, PR estimators, LayerNorm, token pooling); *descriptive* = reported but not read by any decision (jackknife SE, α estimators, iid reference, mean-energy fraction). Test names are shortened to `file::test` (file without `test_`); the full lists are in `MUTANTS_SUMMARY.json`.

| # | Mutant (set, id) | What it changes | Path | Killed by (failing tests) |
|---|---|---|---|---|
| 1 | C N01_signflip_one_sided | sign_flip_test: one-sided statistic (obs = mean, not \|mean\|) | verdict input | `analysis::test_token_contrast_and_replication_rule`, `resampling::test_sign_flip_size_and_power`, `verdict_rules::test_h1a_h1b_orientation_and_wiring_with_l2_shifted_from_ln0l2` |
| 2 | C N02_signflip_no_plus_one | sign_flip_test: p = #{>=}/B instead of (1+#)/(1+B) | verdict input | `verdict_rules::test_sign_flip_p_has_plus_one_floor` |
| 3 | C N03_holm_wrong_multiplier | holm: multiplier rank+1 instead of k-rank | verdict input | `resampling::test_holm_matches_hand_computation` |
| 4 | C N04_holm_no_monotone | holm: drops the running max (no step-down monotonicity) | verdict input | `resampling::test_holm_matches_hand_computation` |
| 5 | C N05_rule_ignores_sign | replication_verdict: zoo agreement ignores sign | verdict rule | `verdict_rules::test_significant_opposite_sign_zoo_does_not_count_as_agreement`, `verdict_rules::test_two_of_three_same_sign_significant_holds_one_does_not`, `verdict_rules::test_primary_is_not_counted_as_its_own_replicate` (+2 more) |
| 6 | C N06_rule_ignores_primary_ci | replication_verdict: primary needs only Holm p (CI ignored) | verdict rule | `verdict_rules::test_primary_ci_covering_zero_kills_even_when_p_is_small` |
| 7 | C N07_rule_one_zoo_enough | replication_verdict: 1 agreeing zoo checkpoint enough (not 2) | verdict rule | `analysis::test_token_contrast_and_replication_rule`, `verdict_rules::test_significant_opposite_sign_zoo_does_not_count_as_agreement`, `verdict_rules::test_two_of_three_same_sign_significant_holds_one_does_not` (+3 more) |
| 8 | C N08_rule_uses_raw_p | replication_verdict: zoo uses raw sign-flip p, not Holm p | verdict rule | `verdict_rules::test_zoo_agreement_uses_holm_not_raw_p` |
| 9 | C N09_D1_uses_hi | subject_level D1 (cov): hi > 0 instead of lo > 0 | verdict rule | `verdict_rules::test_d1_uses_lower_bound_not_point_or_upper` |
| 10 | C N10_D3_any | subject_level D3: any() instead of all() over cross-model pairs | verdict rule | `verdict_rules::test_d3_requires_both_cross_model_pairs` |
| 11 | C N11_H1a_wrong_pair | TOKEN_PRIMARY: H1a wired to L3 vs L2 instead of L3 vs LN0L2 | verdict rule | `verdict_rules::test_primary_pair_wiring_is_the_card_pairs`, `verdict_rules::test_holm_is_applied_to_the_two_primary_contrasts_within_a_checkpoint`, `verdict_rules::test_h1a_h1b_orientation_and_wiring_with_l2_shifted_from_ln0l2` |
| 12 | C N12_floor_vs_max_sd | standardize_columns: variance floor 0.2 x max SD instead of 1e-3 x median | verdict input | `corr_layernorm::test_corrpr_exactly_invariant_to_per_channel_gain_and_bias_covpr_not`, `corr_layernorm::test_pooled_layernorm_output_is_per_channel_affine_of_pooled_ln0` |
| 13 | C N13_ln0_column_axis | layernorm0: normalises columns instead of rows | verdict input | `corr_layernorm::test_corrpr_exactly_invariant_to_per_channel_gain_and_bias_covpr_not`, `corr_layernorm::test_pooled_layernorm_output_is_per_channel_affine_of_pooled_ln0`, `corr_layernorm::test_layernorm0_rows_have_zero_mean_unit_variance` (+1 more) |
| 14 | C N14_ln0_big_eps | LN_EPS 1e-5 -> 10 | verdict input | `corr_layernorm::test_layernorm0_rows_have_zero_mean_unit_variance`, `verdict_rules::test_layernorm0_eps_is_torch_default_and_used` |
| 15 | C N15_subsample_se_m_over_n | paired_subsample_delta: SE sd*sqrt(m/n)/4 instead of sd*sqrt(m/(n-m)) | verdict input | `analysis::test_subject_level_null_does_not_claim_l2_gt_l3`, `resampling::test_paired_subsampling_interval_covers_zero_under_null`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-12]` (+2 more) |
| 16 | C N16_unpaired_subsets | paired_subsample_delta: A and B on different index sets (unpaired) | verdict input | `resampling::test_paired_subsampling_interval_covers_zero_under_null`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-12]`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-28]` (+1 more) |
| 17 | C N17_jackknife_no_factor | jackknife_pr: SE without the (n-1)/n factor (divides by n) | descriptive | `verdict_rules::test_jackknife_se_matches_textbook_formula` |
| 18 | C N18_clauset_missing_one | clauset_mle: alpha = n/denom (drops the 1 +) | descriptive | `alpha_estimators::test_clauset_mle_recovers_iid_pareto_density_exponent[1.5]`, `alpha_estimators::test_clauset_mle_recovers_iid_pareto_density_exponent[2.0]`, `alpha_estimators::test_clauset_mle_recovers_iid_pareto_density_exponent[3.0]` (+1 more) |
| 19 | C N19_rank_slope_sign | rank_slope: returns +slope | descriptive | `alpha_estimators::test_rank_slope_exact_on_exact_power_law[0.5]`, `alpha_estimators::test_rank_slope_exact_on_exact_power_law[1.0]`, `alpha_estimators::test_rank_slope_exact_on_exact_power_law[1.7]` (+2 more) |
| 20 | C N20_colperm_joint_rows | column_permutation_null: one row permutation for all columns | verdict input | `analysis::test_d2_flags_cross_column_dependence`, `resampling::test_column_permutation_null_preserves_each_column_and_breaks_dependence` |
| 21 | C N21_pool_median | token_job pooling: median instead of mean over tokens | verdict input | `token_job::test_subject_summary_matches_direct_computation_and_pooling_rule` |
| 22 | C N22_cat_first_frame_only | token_job: concatenated matrix = first frame only | verdict input | `token_job::test_subject_summary_matches_direct_computation_and_pooling_rule`, `token_job_driver::test_driver_writes_position_keyed_outputs_without_names` |
| 23 | C N23_corr_eigs_cov | corr_eigs: eigenvalues of X instead of standardized Z | verdict input | `corr_layernorm::test_corrpr_exactly_invariant_to_per_channel_gain_and_bias_covpr_not`, `corr_layernorm::test_pooled_layernorm_output_is_per_channel_affine_of_pooled_ln0` |
| 24 | C N24_eigs_keep_extra | centered_eigs: keeps min(n, d) values instead of min(n-1, d) | verdict input | `centering_fixture::test_pr_bounded_by_n_minus_one_and_gram_trick_matches_direct`, `token_job_driver::test_driver_writes_position_keyed_outputs_without_names` |
| 25 | C N25_mean_energy_no_n | mean_energy_fraction: drops the factor n | descriptive | `centering_fixture::test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one[1]`, `centering_fixture::test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one[5]`, `centering_fixture::test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one[20]` (+1 more) |
| 26 | C N26_bootstrap_half_level | subject_bootstrap_ci: default level 0.50 instead of 0.95 | verdict input | `resampling::test_subject_bootstrap_ci_contains_true_mean_most_of_the_time` |
| 27 | C N27_pr_formula_sq | pr_from_eigs: (sum sqrt l)^2 / sum l instead of (sum l)^2 / sum l^2 | verdict input | `centering_fixture::test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one[1]`, `centering_fixture::test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one[5]`, `centering_fixture::test_rank_k_plus_offset_gives_pr_k_and_old_uncentered_gives_one[20]` (+7 more) |
| 28 | C N28_D2_wrong_tail | describe_matrix D2: upper tail (null >= PR) instead of lower tail | verdict rule | `analysis::test_d2_flags_cross_column_dependence` |
| 29 | MM 01 N05/R1 replication ignores sign (same patch as C N05 rule ignores sign) | replication_verdict: zoo agreement ignores sign | verdict rule | `verdict_rules::test_significant_opposite_sign_zoo_does_not_count_as_agreement`, `verdict_rules::test_two_of_three_same_sign_significant_holds_one_does_not`, `verdict_rules::test_primary_is_not_counted_as_its_own_replicate` (+2 more) |
| 30 | MM 02 N06/R3/X12 primary ignores CI | replication_verdict: primary CI condition deleted | verdict rule | `verdict_rules::test_primary_ci_covering_zero_kills_even_when_p_is_small` |
| 31 | MM 03 N08 zoo uses raw p (same patch as C N08 rule uses raw p) | replication_verdict: zoo uses raw sign-flip p, not Holm p | verdict rule | `verdict_rules::test_zoo_agreement_uses_holm_not_raw_p` |
| 32 | MM 04 R8 Holm threshold 0.5 | replication_verdict: primary Holm threshold 0.5 | verdict rule | `verdict_rules::test_primary_holm_p_at_or_above_alpha_is_not_significant[0.05]`, `verdict_rules::test_primary_holm_p_at_or_above_alpha_is_not_significant[0.06]`, `verdict_rules::test_primary_holm_p_at_or_above_alpha_is_not_significant[0.2]` (+1 more) |
| 33 | MM 05 R8b zoo threshold 0.5 | replication_verdict: zoo Holm threshold 0.5 | verdict rule | `verdict_rules::test_zoo_agreement_uses_holm_not_raw_p`, `verdict_rules::test_nonsignificant_same_sign_zoo_does_not_count[0.06]`, `verdict_rules::test_nonsignificant_same_sign_zoo_does_not_count[0.3]` |
| 34 | MM 06 zoo <= instead of < | replication_verdict: zoo p_holm <= alpha instead of < alpha | verdict rule | **survived the shipped suite** (runs 1 and 3); killed in run 2 by `verdict_rules_r2b::test_zoo_checkpoint_at_exactly_holm_alpha_does_not_count_as_agreement[H1a_blocks_LN_matched_corr]`, `verdict_rules_r2b::test_zoo_checkpoint_at_exactly_holm_alpha_does_not_count_as_agreement[H1b_total_stage3_raw_cov]` |
| 35 | MM 07 min agree > instead of >= | replication_verdict: len(agree) > 2 instead of >= 2 | verdict rule | `verdict_rules::test_two_of_three_same_sign_significant_holds_one_does_not`, `verdict_rules::test_frozen_family_b_verdicts_recomputed_from_saved_per_checkpoint_results` |
| 36 | MM 08 N09 D1 hi>0 (same patch as C N09 D1 uses hi) | subject_level D1 (cov): hi > 0 instead of lo > 0 | verdict rule | `verdict_rules::test_d1_uses_lower_bound_not_point_or_upper` |
| 37 | MM 09 M20 D1 point>0 | subject_level D1 (corr): point > 0 instead of lo > 0 | verdict rule | `verdict_rules::test_d1_uses_lower_bound_not_point_or_upper`, `verdict_rules::test_d1_cov_only_is_attributed_to_gain` |
| 38 | MM 10 X06 D1 verdict ignores corr | subject_level D1 verdict string ignores the corr flag | verdict rule | `verdict_rules::test_d1_cov_only_is_attributed_to_gain` |
| 39 | MM 11 N10/M22 D3 any | subject_level D3: any() instead of all() | verdict rule | `verdict_rules::test_d3_requires_both_cross_model_pairs` |
| 40 | MM 12 N11/R9 H1a wired to L2 | TOKEN_PRIMARY: H1a wired to L3 vs L2 | verdict rule | `verdict_rules::test_primary_pair_wiring_is_the_card_pairs`, `verdict_rules::test_holm_is_applied_to_the_two_primary_contrasts_within_a_checkpoint`, `verdict_rules::test_h1a_h1b_orientation_and_wiring_with_l2_shifted_from_ln0l2` |
| 41 | MM 13 H1a swapped orientation | TOKEN_PRIMARY: H1a orientation swapped (LN0L2 vs L3) | verdict rule | `analysis::test_token_contrast_and_replication_rule`, `verdict_rules::test_primary_pair_wiring_is_the_card_pairs`, `verdict_rules::test_holm_is_applied_to_the_two_primary_contrasts_within_a_checkpoint` (+1 more) |
| 42 | MM 14 direction label flipped | replication_verdict: direction label flipped | verdict rule | `analysis::test_token_contrast_and_replication_rule`, `verdict_rules::test_significant_opposite_sign_zoo_does_not_count_as_agreement`, `verdict_rules::test_h1a_h1b_orientation_and_wiring_with_l2_shifted_from_ln0l2` (+1 more) |
| 43 | MM 15 Holm removed in checkpoint | token_level_checkpoint: p_holm = raw p (Holm removed) | verdict rule | `verdict_rules::test_holm_is_applied_to_the_two_primary_contrasts_within_a_checkpoint` |
| 44 | MM 16 N17/R7/X09/M13 jackknife no (n-1)/n | jackknife_pr: SE factor 1 instead of (n-1)/n | descriptive | `verdict_rules::test_jackknife_se_matches_textbook_formula` |
| 45 | MM 17 M14 SE no sqrt(m/(n-m)) | paired_subsample_delta: SE = sd (no sqrt(m/(n-m))) | verdict input | `verdict_rules::test_subsample_se_uses_finite_population_rate[57-12]`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-28]`, `verdict_rules::test_subsample_se_uses_finite_population_rate[25-12]` |
| 46 | MM 18 N02/M18 sign-flip no +1 | sign_flip_test: numerator without +1 (denominator 1+B) | verdict input | `verdict_rules::test_sign_flip_p_has_plus_one_floor` |
| 47 | KD N05_rule_ignores_sign (same patch as C N05 rule ignores sign) | replication_verdict: zoo agreement ignores sign | verdict rule | `verdict_rules::test_significant_opposite_sign_zoo_does_not_count_as_agreement`, `verdict_rules::test_two_of_three_same_sign_significant_holds_one_does_not`, `verdict_rules::test_primary_is_not_counted_as_its_own_replicate` (+2 more) |
| 48 | KD R1_replication_ignores_sign | replication_verdict: sign line deleted | verdict rule | `verdict_rules::test_significant_opposite_sign_zoo_does_not_count_as_agreement`, `verdict_rules::test_two_of_three_same_sign_significant_holds_one_does_not`, `verdict_rules::test_primary_is_not_counted_as_its_own_replicate` (+2 more) |
| 49 | KD N06_rule_ignores_primary_ci (same patch as C N06 rule ignores primary ci) | replication_verdict: primary needs only Holm p (CI ignored) | verdict rule | `verdict_rules::test_primary_ci_covering_zero_kills_even_when_p_is_small` |
| 50 | KD R3_primary_ignores_ci | replication_verdict: primary CI condition deleted | verdict rule | `verdict_rules::test_primary_ci_covering_zero_kills_even_when_p_is_small` |
| 51 | KD X12_verdict_ignores_primary_ci | replication_verdict: primary needs only Holm p (CI ignored) | verdict rule | `verdict_rules::test_primary_ci_covering_zero_kills_even_when_p_is_small` |
| 52 | KD N08_rule_uses_raw_p (same patch as C N08 rule uses raw p) | replication_verdict: zoo uses raw sign-flip p, not Holm p | verdict rule | `verdict_rules::test_zoo_agreement_uses_holm_not_raw_p` |
| 53 | KD R8_holm_alpha_threshold_0p5 | replication_verdict: primary Holm threshold 0.5 | verdict rule | `verdict_rules::test_primary_holm_p_at_or_above_alpha_is_not_significant[0.05]`, `verdict_rules::test_primary_holm_p_at_or_above_alpha_is_not_significant[0.06]`, `verdict_rules::test_primary_holm_p_at_or_above_alpha_is_not_significant[0.2]` (+1 more) |
| 54 | KD N09_D1_uses_hi (same patch as C N09 D1 uses hi) | subject_level D1 (cov): hi > 0 instead of lo > 0 | verdict rule | `verdict_rules::test_d1_uses_lower_bound_not_point_or_upper` |
| 55 | KD M20_D1_point_not_lo | subject_level D1 (cov): point > 0 instead of lo > 0 | verdict rule | `verdict_rules::test_d1_uses_lower_bound_not_point_or_upper` |
| 56 | KD X06_D1_corr_ignored | subject_level D1: corr flag forced True | verdict rule | `verdict_rules::test_d1_uses_lower_bound_not_point_or_upper`, `verdict_rules::test_d1_cov_only_is_attributed_to_gain` |
| 57 | KD N10_D3_any (same patch as C N10 D3 any) | subject_level D3: any() instead of all() over cross-model pairs | verdict rule | `verdict_rules::test_d3_requires_both_cross_model_pairs` |
| 58 | KD N11_H1a_wrong_pair (same patch as C N11 H1a wrong pair) | TOKEN_PRIMARY: H1a wired to L3 vs L2 instead of L3 vs LN0L2 | verdict rule | `verdict_rules::test_primary_pair_wiring_is_the_card_pairs`, `verdict_rules::test_holm_is_applied_to_the_two_primary_contrasts_within_a_checkpoint`, `verdict_rules::test_h1a_h1b_orientation_and_wiring_with_l2_shifted_from_ln0l2` |
| 59 | KD N17_jackknife_no_factor (same patch as C N17 jackknife no factor) | jackknife_pr: SE without the (n-1)/n factor (divides by n) | descriptive | `verdict_rules::test_jackknife_se_matches_textbook_formula` |
| 60 | KD R7_jackknife_no_scaling | jackknife_pr: SE factor 1/n instead of (n-1)/n | descriptive | `verdict_rules::test_jackknife_se_matches_textbook_formula` |
| 61 | KD M14_subsample_se_unscaled | paired_subsample_delta: SE = sd (no sqrt(m/(n-m))) | verdict input | `verdict_rules::test_subsample_se_uses_finite_population_rate[57-12]`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-28]`, `verdict_rules::test_subsample_se_uses_finite_population_rate[25-12]` |
| 62 | KD R4_subsample_se_sqrt_m_over_n_fixedpattern | paired_subsample_delta: SE sd*sqrt(m/n)*0.5 | verdict input | `resampling::test_paired_subsampling_interval_covers_zero_under_null`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-12]`, `verdict_rules::test_subsample_se_uses_finite_population_rate[57-28]` (+1 more) |
| 63 | KD M15_ln_eps_zero | layernorm0: eps removed | verdict input | `verdict_rules::test_layernorm0_eps_is_torch_default_and_used` |
| 64 | KD R11_ln0_eps_large | LN_EPS 1e-5 -> 0.1 | verdict input | `corr_layernorm::test_layernorm0_rows_have_zero_mean_unit_variance`, `verdict_rules::test_layernorm0_eps_is_torch_default_and_used` |
| 65 | KD N02_signflip_no_plus_one (same patch as C N02 signflip no plus one) | sign_flip_test: p = #{>=}/B instead of (1+#)/(1+B) | verdict input | `verdict_rules::test_sign_flip_p_has_plus_one_floor` |
| 66 | KD M10_rank_slope_window_full | rank_slope: default window r instead of r // 2 | descriptive | `verdict_rules::test_rank_slope_default_window_is_half_the_nonzero_rank` |
| 67 | KD X13_iid_reference_uniform | iid_reference: uniform draws instead of standard normal | descriptive | `verdict_rules::test_iid_reference_is_gaussian_marchenko_pastur_draws` |

## 5. New test file

`tests/topic3_spectral/test_verdict_rules_r2b.py`: 3 tests, written **after** the real-data results existed. It is a regression guard for the shipped decision code, not a pre-registration. No existing test and no `src/` or `scripts/` file was edited.

- `test_holm_alpha_boundary_is_reachable_at_card_resolution`: with `PARAMS["signflip_B"] == 9999`, a raw p of (1 + 249)/(1 + B) = 0.025 is Holm-adjusted (paired with 0.3) to exactly `PARAMS["holm_alpha"]` = 0.05.
- `test_zoo_checkpoint_at_exactly_holm_alpha_does_not_count_as_agreement`, for H1a and for H1b: the primary and one zoo checkpoint are significant and positive, one zoo checkpoint is significant and negative, and one zoo checkpoint has the same sign with Holm p exactly 0.05. The shipped rule counts 1 agreeing checkpoint and returns "not replicated"; under `MM 06` it counts 2 and returns "holds".

On the shipped, unmutated code: 3 passed (`verification/worker_M2_r2b/new_test_on_shipped_code.log`). In run 2 these tests kill `MM 06` (2 failed, 86 passed) and also fail under 10 other mutants that the shipped suite already kills (N03, N05, N07, N08 and their duplicates, R1, R8b).

## 6. Check of the numbers in addendum 03 items 1, 3 and 5

Check script: `verification/worker_M2_r2b/probes/check_addendum03_numbers.py` (output `check_addendum03_numbers.out.json`, log `.log`). For each number, the quoted text must occur in the pinned addendum 03, and the value is compared with (P) `verification/worker_M2_r2/probes/probe_addendum03_numbers.out.json`, (J) the pinned `family_A_subject_level.json` and `family_B_token_level.json` where the quantity is stored there, and (I) an independent recomputation by the check script from the pinned token-spectra npz files (and, for the L1 leave-one-out details that exist only in P, from the external pooled `layer_1.npz`, array key only). All inputs matched their pins.

**Result: 35 quoted claims checked (34 from items 1, 3 and 5, plus the item-2 restatement "77–88%" of an item-1 number), 32 agree, 3 mismatch, 0 quotes missing.** One further binding check, not a quote, confirmed that the PR recomputed from the stored float32 eigenvalues equals the stored PR to within 4.3e-8 (relative). Wherever P, J and I could be compared they agree to within 2e-15 (absolute). The three mismatches are text-level. None changes a verdict, and none changes the reading in addendum 03.

| Item | Addendum 03 text | Finding | Correct text |
|---|---|---|---|
| 1 (L1) | "≥ 0.99994 of the variance lies in the top 63 eigenvalues in every subject and checkpoint" | The minimum is 0.99993998 (HCP_N400), 2.4e-8 below 0.99994. The statement holds only after rounding to 5 decimals. | "≥ 0.99993", or "0.99994 after rounding to 5 decimals" |
| 3 | "Holm p 0.0002, CIs about ±0.002" | Holm p is 0.0002 in every checkpoint for H1a and H1b. The CI half-widths are 0.0020–0.0144; only the primary checkpoint's H1a CI is about ±0.002. The point of the sentence stands: these CIs are narrow next to the spread of the checkpoint means (−0.137 to +0.049 for H1a). | "CI half-widths 0.002–0.014" |
| 5 | path `A1_swift_pairs/L2_minus_L3/cov/lo` in `family_A_subject_level.json` | The value 3.2249865 is correct, but the key sits under the top-level key `results`. | `results/A1_swift_pairs/L2_minus_L3/cov/lo` |

Two notes, not mismatches:
- Item 1, "maximum 7 (primary, L5e-5 at L2/LN0L2), up to 8–10 in the other zoo checkpoints": the L5e-5 checkpoint reaches 9 at L3, which the sentence covers only implicitly.
- Item 3, "the SE would be 0.149": both conventions for the reduced jackknife give 0.149 (factor (n−1)/n: 0.148851; factor (n−2)/(n−1): 0.148827).

Verified as printed: the top-7 energy minimum 0.999942 and "within 6e-5"; median count 7 at L2/LN0L2/L3; max |log concatenated − log mean per-frame covPR| 1.13e-4 ≤ 1.2e-4; within/between SD ratio 0.0030–0.0048; H4 ratio exactly 1; primary medians 5.41/5.67 (covPR) and 5.88/6.14 (corrPR) with fractions of 7 of 0.77/0.81/0.84/0.88 and the 77–88% range; L1 counts 29–60 (primary 50–55); L0 counts 64–209; variance ratios 13.4 (H1a) and 5.8 (H1b); the H1a agreeing checkpoints being the two NewUAH ones, and HCP_N400 reversing H1a and H1b; L1 full covPR 2.78, jackknife SE 3.58, largest leave-one-out 6.39, next 2.84, median 2.75; "every primary Holm p is 0.0002 and every primary CI excludes 0"; the item 5 values 3.2249865 and −3.2848924 and their roundings +3.22 and −3.28; the printed report values at lines 49, 55 and 68; and the addendum 02 copy list lacking `empirical_results.json`.

## 7. Scope and limits of this evidence

- The mutant set is the one assigned: challenger_M2_r1_1's harness and the two explorer sets. The other verifiers' complete harnesses (reviewer_M2_r1_1, reviewer_M2_r1_2, auditor_M2_r1_1, challenger_M2_r1_2, and worker_M2_r1's `mutants.py`) were not rerun. Their iteration-1 survivors are covered through `kill_demo.py`. The mutants they killed in iteration 1 were killed by tests that are still in the shipped suite, unchanged; that was not re-run here.
- Boundary mutants of the same kind as `MM 06` but outside the assigned set (for example `lo >= 0` instead of `lo > 0` in D1/D3, or `>= 0` in the primary CI condition) were not run, and neither was a primary-side `<=` Holm mutant. The shipped test `test_primary_holm_p_at_or_above_alpha_is_not_significant[0.05]` already feeds the primary a Holm p of exactly 0.05 and requires "not significant", so it exercises that boundary.
- A mutant is counted as killed when pytest exits with rc 1 (one or more failing tests). No job had any other non-zero code.
- Logs: the runner replaces the BIDS subject-ID prefix followed by a letter or digit with `sub_REDACTED_` at write time. There were 0 replacements: the tests create only synthetic names, and the only occurrences of the bare prefix in the logs are quoted test-source lines inside tracebacks.

## 8. Compute

0 GPU-hours. Nothing was sent to B300 and no connectome job was run. Local CPU only, under `nice -n 10`: three mutant runs of 69 jobs each, 6 in parallel (about 7, 5 and 5 minutes), the number check, and the final test runs.
