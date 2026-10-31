# Topic 1: pre-label addendum for the full-cohort run (step 5)

- Date: 2026-10-31. Run tw-20261031-four-topics, worker_M1_r1.
- This file adds to the frozen card `2026-10-30_topic1_analysis_card.md` (sha256 `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`, unchanged) and to its open-issues files. It does not change any frozen item.
- **Written before any diagnosis label was joined with any real-data feature.** Its sha256 is recorded in `results/topic1/2026-10-31/prelabel_addendum_sha256.txt`, which is written before `analyze` runs. Any later change goes into a new dated file.
- The card leaves some details open. This addendum settles them; the code that implements each item cites its number.
- Status when it was written:
  - The label-free primary extraction was still running (`results/topic1/2026-10-31/extract_primary.log`).
  - No feature value had been looked at. The only things seen were per-subject run status (ok/error) and timings.
  - The degeneracy fallback had not yet been decided.
- Status at freeze (2026-10-31, about 11:30Z; the lines above are kept as written at 08:39Z):
  - The primary extraction had finished: 1,706 rows, all ok, all with the frozen params hash.
  - Still no feature value had been inspected, and no label had been joined to any feature.
  - `decide` had not been run. It runs after this file's sha256 is recorded.

## M. Manifest and data floor

**M1. Pinned manifest.** `results/topic1/2026-10-31/manifest.json` was written by `scripts/topic1_run_cohort.py manifest`.
- Count: 1,706.
- Cohort digest: one sha256 of a public salt plus the sorted directory names, `6a0c408b…5afe`. There are no hashes per position.
- For each position it records site, TR, raw_valid_T, n_trim, valid_T, duration_s, grid_len (the length of the frozen preprocessed series on the 2.0 s grid) and the data-contract status.
- The extractor checks the count and the digest before it starts. A remapped listing stops the run.

**M2. Minimum length.** grid_len ≥ 100, which is 200 s on the 2.0 s grid. The test is an integer comparison. Observed: grid_len runs from 100 to 340 (median 160), so 0 subjects fall below the floor. All 1,706 pass the data contract.

**M3.** Contract errors would be recorded by class only. There are none.

## P. Statistics (scripts/topic1_cohort_stats.py)

**P1. Samples.**
- Complete cases on dx (OCD code 1 → 1, code 2 → 0), age, sex and log duration. None of these is missing in the 1,706.
- For each endpoint, subjects whose Z is NaN (degenerate) are excluded from that endpoint only.
- Secondary family 1 uses the same subjects for the lag-motif model and the static-FC comparator. These are the subjects with finite Z030C and Z030T at the decided density.

**P2. Degeneracy and the fallback (card §3).**
- E1 is degenerate when the null SD of 030C is 0. E2 is degenerate when the null SD of 030C or of 030T is 0.
- Denominator: every subject with a successful primary extraction, which is every included subject.
- The fallback triggers when rate_E1 > 0.10 or rate_E2 > 0.10 at broadband@0.10. The comparison is strict: exactly 10 % does not trigger it.
- When it triggers, the primary density becomes 0.15, and the full primary analysis at 0.10 is also reported as a sensitivity analysis (T1.5).
- Gap (a): if 0.15 is also more than 10 % degenerate, there is no further fallback. 0.15 stays primary, and its rates are reported.
- The decision is computed by `topic1_cohort_stats.py decide`, which reads only the primary extraction JSONL and no metadata. It is written to `fallback_decision.json`, and its sha256 to `fallback_decision_sha256.txt`, before `analyze`. `analyze` refuses to run if that file has changed.

**P3. Permutations (gap c).**
- Freedman–Lane:
  1. Fit the reduced model y ~ age + sex + log duration + site dummies, without the tested regressor.
  2. Form y* = ŷ_r + P e_r.
  3. Take the OLS t of the tested regressor in the full model.
- The implementation is vectorised. Because M_Z ŷ_r = 0, it is exact.
- Within-site permutations: for each site, argsort of uniform keys drawn from the analysis's generator.
- Each analysis gets its own `numpy.random.default_rng(20261031)`: each endpoint, each secondary test and each sensitivity row. E1 and E2 therefore use the same stream even though their samples can differ.
- B = 9,999, and p = (1 + #{|t*| ≥ |t|}) / (B + 1).

**P4. Rank guard (gap d).**
- The full design [x, Z] must have full column rank (numpy matrix_rank), and the tested regressor must not lie in the column space of the nuisance terms. Otherwise the run stops for review.
- No column is dropped silently. The only planned exception is P9.

**P5. MixedLM policy.**
- Fit: statsmodels 0.14.6 `MixedLM`, `reml=False`, default optimizer, site random intercept, and Mundlak site means of dx, age, sex and log duration.
- `converged`, the warnings, `mle_retvals`, the site variance and the ratio of the LMM scale to the FE scale are all recorded.
- **Neither a ConvergenceWarning nor converged = False (or True) stops the run.** The only stop rule is the card's |β_LMM − β_FE| ≥ 0.01·SE_FE.
- d = β_LMM / sqrt(MixedLM scale). d_FE = β_FE / σ_FE is reported beside it.

**P6. Standardised β (gap e).** For family 2, β_std = β · SD(E) / SD(Y-BOCS), with both SDs computed with ddof = 1 on the analysed subjects. For family 3, the script reports β for code 1 − code 2, d_FE = β/σ_FE and the Freedman–Lane p.

**P7. Family 1 (gap f; also gap b).**
- Family 1 is descriptive: it has no p-value and is not part of a BH family.
- After a fallback, all secondary families use the decided primary density. Because card §6 names broadband@0.10 literally, the family-1 result at 0.10 is also reported in that case.
- Lag-motif model: StandardScaler, then `LogisticRegression(C=1, L2, max_iter=5000)`.
- Comparator: `PCA(50, svd_solver='randomized', random_state=20261032)`, then the same logistic regression.
- Both use LeaveOneGroupOut over sites.
- Metrics: pooled out-of-fold AUROC, a site-bootstrap 95 % CI (2,000 resamples, seed 20261032; resamples with one class only are dropped and counted), and the mean AUROC per site over sites that have both classes.
- The static FC is the upper triangle of the Pearson correlation of the frozen preprocessed 2.0 s series. It is computed in the primary extraction pass and stored in `results/topic1/2026-10-31/derived/`, which is git-ignored.

**P8. Families 2 and 3.**
- BH runs over {E1, E2} within each family.
- Family 2: OCD subjects with non-null Y-BOCS. Model: Y-BOCS ~ E + age + sex + log duration + site.
- Family 3: OCD subjects with medication codes 1 and 2, in sites that have both codes. Model: E ~ (code = 1) + age + sex + log duration + site. It is reported only as "code 1 vs code 2".

**P9. Sensitivity analysis with the common 200 s truncation.**
- Every analysed series is 200 s long, so log duration is constant within site and collinear with the site terms. That row is therefore fitted without log duration and without its Mundlak mean.
- Every other row keeps the card's covariates.

**P10. Acceptance-stratified sensitivity analysis.** This is post-freeze, required by addendum r2 item 34, and descriptive. The primary endpoints are refitted after excluding subjects at or below the pooled 10th percentile of `acceptance_mean` at the primary unit. It cannot change the verdict. Acceptance includes 2-swap no-ops (r2 item 31).

**P11. Descriptive rates, computed after the label join.** By group, by site and by site × group:
- degenerate rates for E1 and E2;
- mean and 10th percentile of acceptance;
- grid length;
- gradient share.

These are given for the primary unit and, by group, for all six units.

**P12.** The 030C log ratio (degeneracy-safe) is always reported with the primary model as a secondary outcome. Raw pooled Cohen's d and Welch p are attached to every row, labelled DESCRIPTIVE.

**P13. Verdict.** The verdict follows card §5 exactly:
- Holm over the two endpoints;
- an endpoint survives if p_Holm < 0.05 and |d| ≥ 0.15;
- Topic 1 is killed if neither survives.

The §9 spurious-direction limitation and the degeneracy rates are reported beside the verdict.

The following items were added after the code review in D4. Each of them can only stop the run or add a report; none of them changes the estimator, the p-value or the decision rule.

**P14. Card count stop rule.** `analyze` stops for review unless the metadata joined to the 1,706 on-disk positions reproduces the card §3/§6 counts exactly: 1,706 on disk, 869 code 1, 837 code 2, 23 sites, 856 non-null Y-BOCS in code 1, and medication codes 1 and 2 in code 1 at 203 and 212 (`card_count_check`). This protects against a changed or mis-typed metadata file, for example Medication read as text.

**P15. NaN and degeneracy flag stop rule.** Card §3 excludes a subject as "degenerate (Z NaN)", while P2 defines degeneracy by null SD = 0. For each primary endpoint at each analysed density, the non-finite endpoint values must coincide exactly with the P2 flags; otherwise the run stops (`check_nan_flag_agreement`).

**P16. Exclusions by group and site (card §3).** Every exclusion class is counted in total, by group, by site and by site × group, at the primary unit (`exclusions_by`):
- extraction failure, which covers data-contract errors;
- a missing covariate (dx, age, sex or log duration);
- degenerate for E1;
- degenerate for E2.

P2's fallback denominator (all successful extractions) and the analysed set coincide here, because no subject has a missing covariate (D2).

**P17. Reported beside the verdict, descriptive.**
- The MixedLM `converged` flag for each endpoint.
- Whether the same §5 rule, applied with d_FE instead of d_LMM, gives the same survival.

Neither of them changes the verdict.

## V. Card §7 extraction variants

These run only for surviving endpoints, at the decided primary density, on the broadband channel.

**V1–V3. Variant definitions.** Each variant is a full PARAMS dict or a stated truncation rule. A `variant_sha` covers its params hash, its keyword restrictions and the truncation rule. Keyword overrides of `extract_subject` are not used for parameter changes, because they would keep the frozen params hash.

| Variant | Definition |
|---|---|
| V1 `dct128` | `{**PARAMS, "highpass_cutoff_s": 128.0}` |
| V2 `af40` | `{**PARAMS, "attempts_factor": 40}` |
| V3 `trunc200` | Frozen PARAMS on the head-trimmed native series cut to floor(200/TR + 1e-9) samples |

- For V3, `grid_len == 100` is asserted for every subject. The ceil rule was rejected because it gives 101 grid samples at TR 0.7, 0.85, 1.73 and 1.8, which contradicts card §7 ("the first 100 grid samples after the head trim").
- Seeds follow the frozen rule, so a variant shares its seed with the primary for the same position, channel and density.

**V4. Other §7 rows.** These come from the primary extraction:
- the other two densities;
- gradient share as a covariate. This row is fitted with the card's MixedLM, with gradient share added both as a regressor and as its own Mundlak site mean. The same 0.01·SE equality stop applies, and d = β_LMM/√scale as in the primary row. The FE OLS model behind the Freedman–Lane p gets gradient share as an extra nuisance column;
- curl, descriptive;
- the rank-inverse-normal outcome;
- MixedLM without Mundlak terms. This row is known to be biased under aligned site effects (explorer_M1_r1_3);
- the log ratio;
- leave-one-site-out β_FE;
- age ≥ 18 only.

## G. How the survey gaps are settled

| Gap | Settled by |
|---|---|
| (a) | P2 |
| (b) | P7 |
| (c) | P3 |
| (d) | P4 and P9 |
| (e) | P6 |
| (f) | P7 |
| (g) | V3 (floor rule, not ceil) |
| (h) | P1 |
| Grid floor | M2 |

## D. Disclosures and deviations

**D1. Order.**
- The label-free primary extraction was started before the stats script was final. This saved wall time, since the extraction takes about 1 h.
- No label was read by the extraction.
- No feature value was inspected before this addendum and the script hash were recorded.

**D2. Validation read the real design.**
- `topic1_cohort_stats.py validate` read the real metadata design (dx, age, sex and site) and the manifest durations, and combined them with synthetic outcomes only. ACCEPTANCE T1.2 requires the real site × diagnosis structure.
- No imaging feature was read.
- A smoke run with small R was also done (`verification/worker_M1_r1/smoke_stats/`).
- The analyze-path smoke probe (`verification/worker_M1_r1/probe_analyze_smoke.py`) used a fully synthetic design and fabricated features. It read no real file. It ran on the final script bytes (`33e27576…`), with `card_count_check` stubbed out.
- Because the smoke probe stubbed that check, `verification/worker_M1_r1/probe_card_counts_labels_only.py` then ran `load_design` and `card_count_check` on the real metadata.
  - It read labels only: no imaging feature, and no extraction output.
  - It printed aggregate counts only. All seven card counts matched, Medication was read as float64, and no age or sex value was missing, so the complete-case design is all 1,706.
  - Its output is `probe_card_counts_labels_only.out.json` in the same folder.

**D3. The across-site permutation defect is checked structurally.** Every permutation must keep each index within its site, and the vectorised t* must equal a statsmodels refit. It is not checked by null FPR, because that defect stays near nominal on this design (explorer_M1_r1_2).

**D4. Review.** No native independent agent was available to the worker, because nested spawning is not provided.

A Trinity review was run on the stats script, code only, from a bundle of script bytes `fcf5480a…`. Its log is `verification/worker_M1_r1/trinity_review.log`.
- **The review is incomplete.** The codex provider failed twice. Only the claude and antigravity providers answered, and the saved log stops partway through the claude provider's round-1 answer, so any later findings are lost.
- These findings in the saved part led to script changes before the freeze:
  - convergence cannot be checked through the Mundlak identity → P17 (flags reported beside the verdict);
  - the gradient-share row skipped the LMM → V4 (card LMM with a Mundlak mean);
  - exclusions were not reported by group and site → P16;
  - the NaN rule and the flag rule could disagree → P15;
  - there was no cardinality check → P14;
  - family-1 features sat at the decided primary unit rather than the literal 0.10 → P7 (the literal 0.10 result is reported too).
- The findings did not change the primary t, the p-value or the decision rule. The review itself confirmed these against statsmodels (`multipletests`) and an explicit refit.

**Script versions and validation.**
- Validation run 2 (`stats_validation.json`) bound bytes `f2589105…`, before the review amendments.
- The final bytes were therefore validated again, into `stats_validation_final.json`.
- The mutation receipts were also rerun on the final scripts and tests (v3, with 4 extra mutants for P14–P16 and V4).
- Both runs and their sha256 values are listed in `results/topic1/2026-10-31/stats_script_sha256.txt`.
- An independent review by a fresh native agent is still owed to the parent coordinator (no nested spawning was available).

**D5.** The large static-FC array lives under `results/topic1/2026-10-31/derived/`, with a `.gitignore`.

## Hashes recorded with this addendum

These are filled in at freeze time, before `analyze`:

- stats script: see `results/topic1/2026-10-31/stats_script_sha256.txt`
- validation output: same file
- manifest: `063513c99122e849407c598b95dda24b2f946493095b7ed11d27bf15beb537f6`
