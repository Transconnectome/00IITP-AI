# handoff — explorer_M1_r1_3 (M1 Topic 1, T1.1–T1.5)

**Summary.** All 5 surviving mutants can be killed with 5 assertions made through `extract_subject`. The draft tests are written and were checked against all 24 mutants: 24 killed, controls 59 passed. Four new risks need handling in the worker's scripts, because `src/` is frozen and cannot absorb them:
- a params-hash provenance trap for keyword overrides;
- the 200 s truncation rule (survey_1's `ceil` rule contradicts the card);
- MixedLM ML fits that always report non-convergence even though the Mundlak β equality is exact;
- a mutant harness that copies only `src/` and `tests/`.

Probe-backed recommendations are below. Probes and logs are in `/home/juke/git/00IITP-AI/verification/explorer_M1_r1_3/`.

## 1. Observation

O1. **Mutant kill probe.**
- Draft tests: `verification/explorer_M1_r1_3/probe_extract_contract_tests.py`. They have 5 tests and use synthetic 304-ROI series only.
- Harness: adapted copies `verification/explorer_M1_r1_3/mutants.py` and `mutants_extra.py`. The changes are BASE → `verification/explorer_M1_r1_3/mut`, the output JSONs moved into my folder, the probe test copied into each mirror as `test_zz_probe_extract_contract.py`, and the extra control renamed `control_extra` so the two mirror directories cannot collide.
- Results (`mutants_probe.log`, `mutants_extra_probe.log`, `mutation_results.json`, `mutation_results_extra_probe.json`):
  - `control` rc=0 "59 passed"; `control_extra` rc=0 "59 passed".
  - All 19 other base mutants have rc=1. `roi_subsample_80` gave "3 failed" (it was a survivor before).
  - `curl_returns_F` fails test_curl_channel_is_curl_of_F.
  - `seeds_ignore_position` fails test_seed_rule_uses_position and test_curl.
  - `sp_not_normalised` fails test_sp_unit_norm.
  - `extract_subject_drops_valid_T` fails test_valid_T_is_post_trim.
  - So 0 of 24 non-control mutants survive.
- The probe file passes on the unmutated code: "5 passed in 1.78s".
- The `mut/` mirrors were deleted afterwards.

O2. **What the harness copies.** `verification/victory_auditor_1/mutants.py:build()` copies only `src/topic1_lagmotif`, `tests/topic1_lagmotif` and `tests/__init__.py` into the mirror.
- `scripts/` has no `__init__.py`.
- The repo has no pytest.ini, pyproject.toml, setup.cfg or tox.ini, so a repo-wide `pytest` collects every `test_*.py` under `verification/`, including any leftover `mut/` mirrors.

O3. **Params-hash trap** (`probe_provenance.log`).
- `extract_subject(s, attempts_factor=40.0, …)` records `params_sha256 = 86863ffad95c…`, the frozen hash, while running n_attempts = 184,240 (40·m).
- `extract_subject(s, params=dict(PARAMS, attempts_factor=40), …)` records `87f645287e81…`.
- Cause, `pipeline.py:65-79`: keyword overrides of `n_null`, `attempts_factor`, `densities` and `channels` bypass `PARAMS`, and `extract_subject` hashes only `params`.

O4. **200 s truncation** (`probe_provenance.log`). Native truncation to `ceil(200/TR)` samples, followed by the frozen `preprocess`, gives this many grid samples:

| TR | ceil rule | floor rule |
|---|---|---|
| 0.7 | 101 | 100 |
| 0.8 | 100 | 100 |
| 0.85 | 101 | 100 |
| 1.0 | 100 | 100 |
| 1.73 | 101 | 100 |
| 1.8 | 101 | 100 |
| 2.0 | 100 | 100 |

The floor rule is `floor(200/TR + 1e-9)` native samples. Card §7 says "the first 100 grid samples after the head trim".

O5. **Cohort lengths, label-free** (`probe_design.log`).
- 1,706 loaded with 0 contract errors, in 13 s, across 23 sites.
- Grid length ranges from 100 to 340, with median 160. No subject is below 100; 200 subjects are at ≤ 101 (Bellvitge-ANTIGA has minimum 100, Bellvitge-PROV is all 100).
- 16 of 23 sites have a single duration value, so log duration varies within only 7 sites: Amsterdam, Bangalore, Bellvitge-ANTIGA, Braga-act, Dresden, NYSPI-Adults and NYSPI-Pediatric. In the Y-BOCS subset only 5 sites vary.
- Counts:
  - dx: 869 OCD, 837 HC. Age and sex have no missing values.
  - OCD with Y-BOCS: 856.
  - Medication within OCD: code 1 = 203, code 2 = 212. Eleven sites have both codes, with n = 301.
  - Under 18, by site: Barcelona-HCPB 52/64, Dresden 32/35, NYSPI-Pediatric 33/34, Vancouver 41/45, Yale-Gruner 29/29.
- Site OCD fraction ranges from 0.175 to 0.817.

O6. **Freedman–Lane implementation check** (`probe_stats_check.log`).
- Vectorised t = 1.078999, the same value as statsmodels `ols("y ~ dx + age + C(sex) + ld + C(site)")`; df 1679 in both.
- The within-site permutation keeps site and is a true permutation.
- The reduced design has rank 26 with 26 columns: age, sex, log duration and 23 site dummies.

O7. **Mundlak MixedLM, ML fit** (`probe_mundlak.log`). 40 reps per cell, real design, synthetic Y.
- max |β_LMM − β_FE|/SE_FE is between 7.7e-13 and 1.03e-12 in every cell. This holds for null S1 (aligned site effects, ICC 0.3), null S2 (site-dependent noise SD) and planted d = 0.15 and 0.30.
- `all_conv = False` in every cell, with 225–283 ConvergenceWarnings per 40 reps ("Maximum Likelihood optimization failed to converge", "Retrying MixedLM optimization with lbfgs").
- lm.scale / fe.scale = 0.988.

| Cell | mean d_LMM | mean d_FE | mean d without Mundlak terms |
|---|---|---|---|
| S1 null | 0.000032 | 0.000040 | 0.0116 |
| S1, d = 0.15 | 0.1513 | 0.1504 | 0.1621 |
| S1, d = 0.30 | 0.3025 | 0.3008 | 0.3126 |
| S2 null | −0.0075 | −0.0074 | 0.0133 |

- The SD of d_LMM is 0.057 under S1 (n = 40 reps, so it is noisy) and 0.051 under S2.
- Each fit takes about 0.09 s.

O8. **Turnover probe** (`probe_turnover.log`).
- `sample_null_graph(A, 20, p_rot, seeds[r])` reproduces null r of `null_counts` exactly: 030C and 030T are equal for r = 0..4.
- Edges moved, defined as |A_null ∧ ¬A_obs|, range from 4,319 to 4,352 of m = 4,606 for a white-noise subject.

O9. **FPR at H0** (`probe_stats_fpr.log`). R = 2000 reps, B = 199, real design. Results: see §6 (appended when the run finished).

O10. **Gates.**
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0 with 0 non-OK lines (`protected.log`).
- Card §12 hashes: 10 of 10 OK (`card_s12.log`). The card sha256 starts 1e589f0ba5a8.
- `audit_layout.py` on the run root: 33 files, `findings: []`.

## 2. Logic chain

L1 (O1, O2). T1.1 is solvable with tests only, so the card stays valid. The draft file can move as-is to `tests/topic1_lagmotif/test_extract_contract.py`. That keeps the mirror copy automatic.

There is one hazard. If any new test in `tests/topic1_lagmotif` imports `scripts/topic1_*` (for example, cohort-stats tests), the mirror cannot import it. Every mirror, including control, then fails, and "0 survivors" becomes vacuous. The worker must therefore do one of two things:
- adapt `build()` to also copy `scripts/topic1_*.py`, and require control rc 0; or
- keep stats tests out of the mirror run, for example by passing an explicit file list.

The control pass count must equal the real-suite count.

L2 (O3). Card §7's factor-40 variant, if run through keyword arguments, writes output whose params hash is identical to the primary run's. The two then cannot be told apart by provenance (C3, T1.4 "raw run log with params hash"). `pipeline.py` is frozen, so the runner in `scripts/` must enforce this:
- pass every variant as a modified PARAMS dict, with `highpass_cutoff_s=128` and `attempts_factor=40`;
- record `n_null`, `densities` and `channels` explicitly next to the hash;
- add a "variant" field and a `variant_sha` over (params, kwargs, truncation rule);
- assert at write time that the primary rows carry `86863ffa…` and that no kwargs are present.

L3 (O4). Survey_1's gap (g), "cut to ceil(200/TR)", does not reproduce the card's "first 100 grid samples" at 4 of the 7 TRs. `floor(200/TR + 1e-9)` native samples, cut after the head trim, gives exactly 100 grid samples at every on-disk TR and needs no change to the frozen chain.

The truncated series must be rebuilt with `dataclasses.replace(s, X=s.X[:n], valid_T=n, duration_s=n*tr)`. Detrend and z-score are then computed on the truncated window, which is the natural reading of "common truncation". Assert that the grid length is 100, and record the rule in the pre-label addendum. This disagrees with survey_1.

L4 (O5). A 200 s floor (100 grid samples) excludes nobody. Any higher floor removes Bellvitge-PROV entirely. Log duration is identified from 7 sites only (5 in Y-BOCS). It is not collinear with the site dummies (rank 26/26), but it carries little information and is not interpretable. That is acceptable, because it is a nuisance covariate. Gap (d) applies to subsets: medication within OCD has 11 sites and a small n, so a rank check of the design is still required per analysis. Rule: drop a column only if it is exactly collinear, and log it.

L5 (O7).
- The Mundlak/FE β equality is exact to machine precision, so the card's stop rule is a meaningful bug detector.
- statsmodels reports non-convergence in essentially every fit, probably because the site variance goes to the boundary once the Mundlak means absorb the aligned site effects. If the worker treats a ConvergenceWarning or `converged == False` as fatal, the run stops for no reason. If the worker suppresses warnings silently, provenance is lost.
- The pre-label addendum must therefore say: the card's |Δβ| < 0.01·SE check is the stop rule; `converged`, `mle_retvals` and the site variance are logged; a warning alone is not fatal.
- ML σ_ε² is about 0.988 × the OLS scale, so d_LMM is about 0.6% larger than d_FE (0.1513 vs 0.1504 at a true 0.15). Keep the card's d and report d_FE beside it. Near |d| = 0.15 the two can fall on different sides of the bar, and the card's d governs.

L6 (O7). The §7 "MixedLM without Mundlak terms" sensitivity is biased by about +0.012 under aligned site effects. Report it as a known-biased sensitivity analysis, never as corroboration.

L7 (O8). Addendum items 31, 32 and 34 ask for a measure of real moves. The frozen code returns only attempts accepted, no-ops included. Edge turnover can be computed without touching `src/` by calling `sample_null_graph` on the first few seeds, which reproduce the ensemble nulls exactly. Five nulls per subject at broadband@0.10 add about 0.5% compute. Report the edges-moved fraction by group and site next to acceptance, labelled post-freeze descriptive (addendum F).

L8 (O9). See §6.

## 3. Caveats

- The FPR probe uses B = 199, not the card's 9,999. A within-site permutation test is exact at any B, so B affects only resolution. The first attempt at B = 999 was stopped for time; its log `probe_stats_fpr_B999_killed.log` is empty.
- `probe_stats_fpr.json` was first written by a 20-rep smoke run. It is overwritten only if the R = 2000 run completes; check its contents against the log.
- The Mundlak probe used 40 reps per cell. That is enough for the equality and bias checks, not for power. The SD of d_LMM (0.057) is noisy.
- Synthetic scenarios S1–S5 are my choices. They are not exhaustive: there is no informative-exclusion scenario, and no Y-BOCS or medication subsets were probed.
- I did not time real extraction. The compute estimate is the card's A3 figure: about 12.5–13.1 CPU-h for 6 units, plus about 9 CPU-h for the §7 variants (survey_1, 추정). Load average at 17:01 KST was 7.3 on 20 cores.
- **Disclosure for the root to adjudicate.**
  - `probe_design.py` loaded all 1,706 series through `NpyCohort.load` to compute lengths. It also joined OCD, Age, Sex, Y-BOCS and Medication in memory, by name, to compute per-site counts and to hold the real design for synthetic-outcome probes.
  - No lag-motif feature was computed on any real subject. No label was joined with any real feature. No participant-level data was written to disk; only per-site aggregates were printed.
  - This mirrors addendum item 39 (a survey-stage full read).
- **Independence.** I read only explorer_M1_r1_2's DISPATCH.md, to copy its convention of omitting the survey array. I did not read its report.
- I did not check connectome or B300. M1 needs no GPU, and C6 forbids sending ENIGMA data to B300.

## 4. Conclusion: recommended M1 plan

**Phase 1 (label-free; can run in parallel)**

1. **T1.1**
   - Move `probe_extract_contract_tests.py` to `tests/topic1_lagmotif/test_extract_contract.py`, with content unchanged.
   - Copy `mutants.py` and `mutants_extra.py` into the worker's verification folder and change BASE and the two output paths. Rename the extra control to `control_extra`, or run the two harnesses sequentially.
   - If any new test imports `scripts/topic1_*`, also copy those scripts into the mirror.
   - Pass condition: control rc 0 with the full current test count, and all 24 others rc ≠ 0.
   - Afterwards, `rm -rf` your own `mut/`, and name no probe `test_*.py` outside `tests/`.
   - Rerun C2: the old 86-test suite, plus `tests/topic1_lagmotif`.
2. **T1.3 manifest (`scripts/topic1_manifest.py`)**
   - Record: count 1706, a salted sha256 of the sorted name list (keep the salt outside results, or record only its hash), and per position {site, TR, raw_valid_T, n_trim, valid_T, grid_len, duration_s}.
   - Floor: 200 s (100 grid samples), which excludes 0 subjects.
   - The runner asserts the count and digest at startup.
3. **T1.4a extraction (`scripts/topic1_cohort_extract.py`)**
   - Run on local CPU: `setsid nohup nice -n 10`, 12–14 processes, thread pins set to 1.
   - Write resumable JSONL keyed by position, with no labels.
   - Primary job: 6 carded units, with the frozen PARAMS and no kwargs.
   - Variant job: DCT 128, `floor(200/TR)` truncation and factor 40. Each variant is passed as a PARAMS dict, with variant_sha, and gets its own file.
   - Add edge turnover for 5 seeded nulls per subject at broadband@0.10.
   - Then make the degeneracy fallback decision (E1: 030C sd = 0; E2: 030C or 030T sd = 0; threshold > 10% at 0.10) from the JSONL alone. Write it and its sha256 into the pre-label addendum.
4. **T1.2 stats (`scripts/topic1_cohort_stats.py`)**, exactly per card §4–§6:
   - Freedman–Lane permutation of reduced-model residuals within site, with t computed by QR. My vectorised form matches statsmodels.
   - B = 9,999 and a fresh `default_rng(20261031)` per analysis.
   - MixedLM ML fit with Mundlak means of dx, age, sex and log duration. Stop if |Δβ| ≥ 0.01·SE_FE. Log `converged` but do not treat it as fatal.
   - d = β_LMM/√scale, with d_FE alongside.
   - Holm over E1 and E2; an endpoint survives only if p_Holm < 0.05 and |d| ≥ 0.15.
   - §6 secondaries with BH within each family. Medication uses the 11 sites with both codes (n = 301).
   - Synthetic validation uses the real design with synthetic Y:
     - null FPR within 0.05 ± 2·√(0.05·0.95/R) for R ≥ 2000;
     - planted d = 0.15 and 0.30 recovered;
     - defect fixtures that fail: Welch/raw d, σ taken from the total SD, sign flip, Holm omitted, the 9% vs 11% fallback boundary, and the kill-rule boundaries at 0.149 and 0.151.
   - For "permuting across sites", use a scenario that actually breaks it; see §6. If none does, test it as a structural assertion (the permuted index keeps site) rather than through FPR.

**Phase 2 (serial)**

1. Independent review of the stats script.
2. Record its sha256 in the pre-label addendum, together with gaps a–i, the truncation rule (floor), the convergence policy and the turnover metric.
3. Join labels.
4. Run the statistics.
5. Report: verdict per endpoint, the spurious-direction limitation, degeneracy, acceptance and turnover rates by group and site, and exclusions. Results go to `results/topic1/2026-10-31/` and `docs/03_empirical_analysis/topic1/2026-10-31_*`.
6. **T1.5**: if the fallback triggers, report both densities in the addendum.

## 5. Verification method

- Mutant kill:
  ```
  cd /home/juke/git/00IITP-AI/verification/explorer_M1_r1_3 && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B mutants.py && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B mutants_extra.py; rm -rf mut
  ```
  Expect both controls at rc 0 (59 passed) and every other entry at rc 1.
- Draft tests on unmutated code:
  ```
  cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q verification/explorer_M1_r1_3/probe_extract_contract_tests.py
  ```
  This path is not collected under the default `test_*.py` pattern, so pass it explicitly.
- Hash trap and truncation lengths: run `probe_provenance.py`.
- Mundlak equality and convergence: run `probe_mundlak.py` with `-W ignore`.
- FPR: `probe_stats.py 2000 199 S1_aligned_icc03,S4_dx_hetero_sd,S5_dx_hetero_by_site,S2_site_hetero_sd`.
- Turnover reproducibility: run `probe_turnover.py`.
- Gates: the protected-hash check, the card §12 hashes and `audit_layout.py` on the run root.
- These conclusions are invalidated if any `src/topic1_lagmotif` hash changes, or if `pipeline.py` is edited to hash kwargs. In that case L2 is moot, and the card must be re-frozen.

## 6. FPR probe result (O9, appended when the run finished)

Source: `probe_stats_fpr.log` / `.json`. Settings: R = 2000, B = 199, real design, synthetic Y with β_dx = 0. The MC band is 0.05 ± 0.0097, i.e. [0.0403, 0.0597]. The dx-permutation-within-site column uses R = 200 (band ±0.031).

| Scenario | FL within site (card) | FL across sites | Parametric FE t | Welch, raw pooled | Permute dx within site |
|---|---|---|---|---|---|
| S1: aligned site effect, ICC 0.3 | 0.047 | 0.0495 | 0.0555 | **1.000** | 0.055 |
| S2: noise SD varies by site, aligned with OCD fraction | 0.056 | **0.030** | **0.0335** | **0.91** | 0.055 |
| S4: OCD noise SD 2× HC | 0.0465 | 0.047 | 0.0515 | **0.982** | 0.050 |
| S5: OCD/HC SD ratio varies by site | **0.001** | **0.0005** | **0.0005** | **0.50** | 0.000 |

L8. What the table shows:
1. The card's within-site Freedman–Lane test is calibrated in S1, S2 and S4.
2. Welch on raw pooled data is unusable: FPR 0.5–1.0. This confirms that card §4 treats it as descriptive only.
3. Permuting across sites shows up as a defect only under site-heteroscedastic noise (S2). There it is **conservative** (0.030), so the defect fixture needs a **two-sided** band check in S2. A one-sided "FPR ≤ 0.0597" check would pass it.
4. In S5 every method becomes very conservative (about 0.001). That costs power, not validity. Report it as a limitation if residual variance ratios differ by group and site. The worker can compute per-site, per-group residual SDs, a label-dependent descriptive, after the join.
5. Permuting dx within site was calibrated in these scenarios. It is still not the card's method, so do not substitute it.
