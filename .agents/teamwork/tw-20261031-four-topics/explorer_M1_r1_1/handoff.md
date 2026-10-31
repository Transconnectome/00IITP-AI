# Handoff — explorer_M1_r1_1 (M1: Topic 1 hardening + full-cohort step 5), 2026-10-31

**Summary.**
- **T1.1.** A tests-only file of 5 tests, `verification/explorer_M1_r1_1/proposed_tests/test_extract_contract.py` (sha256 `c4c8d629…282b3d`), kills all 26 mutants in my own mirror: the 20 + 4 from the auditor plus 2 new seed-rule mutants. The control passes 59/59. Without the file, the 5 auditor survivors and the 2 new mutants all survive, which reproduces the auditor's result.
- **T1.2.**
  - On the real 1,706 × 23-site design with synthetic outcomes, the vectorised Freedman–Lane statistic equals a naive statsmodels refit to 1e-13.
  - MixedLM (ML) with Mundlak means gives β_dx equal to β_FE to within about 1e-13·SE.
  - In a probe, Freedman–Lane FPR is 0.0575 in two hard null scenarios (R = 400, B = 999); Welch gives 1.0 and 0.085.
  - Two findings change what the worker implements:
    - MixedLM routinely lands on the site-variance boundary and emits ConvergenceWarnings.
    - The card's 200 s truncation needs floor(200/TR) native samples, not ceil.
- **T1.3.** Every series has a non-zero last row, so there is no trailing padding. The minimum grid length is 100 and the minimum duration is 200.0 s, so a 200 s floor keeps all 1,706 subjects.

## 1. Observation

O1. Frozen state is intact.
- `sha256sum -c sentinel/PROTECTED_HASHES.txt` returns rc 0 (67 entries, checked at start and end).
- Card §12 hashes match 10/10. The card sha256 is `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`.
- `audit_layout.py` on the run root reports 0 findings.

O2. `pipeline.extract_subject`, pipeline.py lines 89–95, returns `gradient_share` and `results["{ch}@{d:.2f}"]`, which is the `motif_statistics` dict with keys observed, null_mean, null_sd, Z, SP, E1_Z030C, E2_Z030C_minus_Z030T, log_ratio_030C, degenerate{030T,030C}, acceptance_mean, n_attempts, m and n_null. It also returns position, tr, valid_T, n_trim, duration_s, raw_valid_T and params_sha256.
- `flow_features` accepts the keyword arguments `channels`, `densities`, `n_null` and `attempts_factor`. The §7 variant "attempts factor 40" needs no code change.
- `highpass_cutoff_s` is a PARAMS key. The DCT 128 s variant is `extract_subject(s, params={**PARAMS, "highpass_cutoff_s": 128.0})`, which gives a different params_sha256 that must be recorded.
- Truncation has no hook. It must be applied to the raw array before `prepare_series`.

O3. Mutation harness. The auditor's `verification/victory_auditor_1/mutants.py` hardcodes `BASE = …/victory_auditor_1/mut`, calls rmtree on each mirror, and writes `victory_auditor_1/mutation_results.json`. `mutants_extra.py` writes `mutation_results_extra.json`.
- My harness `verification/explorer_M1_r1_1/mutants_rerun_probe.py` loads mutants.py through importlib without running its `__main__`. It sets `M.BASE` to my own folder and writes only into my folder.
- The auditor's receipts are unchanged: `mutation_results.json` sha256 `b9b74cac…2bb09a`, mtime 2026-10-30 23:02; `mutation_results_extra.json` sha256 `1fdfa486…07edf`, mtime 23:15.

O4. Mutation results.
- `mutation_rerun_with_new_24.json` and `.log`: control 59 passed; 24/24 killed; survivors [].
  - `roi_subsample_80` is killed by 3 tests, `curl_returns_F` by 1, `seeds_ignore_position` by 2, `sp_not_normalised` by 1 and `extract_subject_drops_valid_T` by 1.
- `mutation_rerun_without_new.json`: control 54 passed. The 5 auditor survivors survive again, and so do the 2 new mutants `seeds_ignore_channel` and `seeds_ignore_density`.
- `mutation_rerun_with_new_seed2.json`: those 2 new mutants are killed (1 and 2 failing tests), with control 59 passed.
- The proposed file passes on production code in 1.6 s; the full topic1 suite plus the file takes about 6 s.

O5. Truncation rule, from `probe_truncation_and_lengths.out.json`, run through the frozen `preprocess()`:

| TR | floor(200/TR) n | grid length | ceil(200/TR) n | grid length |
|---|---|---|---|---|
| 0.7 | 285 | 100 | 286 | 101 |
| 0.8 | 250 | 100 | 250 | 100 |
| 0.85 | 235 | 100 | 236 | 101 |
| 1.0 | 200 | 100 | 200 | 100 |
| 1.73 | 115 | 100 | 116 | 101 |
| 1.8 | 111 | 100 | 112 | 101 |
| 2.0 | 100 | 100 | 100 | 100 |

Card §7 says "Common 200 s truncation (the first 100 grid samples after the head trim)".

O6. Lengths, label-free, from the same probe. It read each npy header shape and the content of its last row.
- 1,706 files; 0 have an all-zero last row.
- Grid length minimum, median and maximum are 100, 160 and 340.
- Minimum duration is 200.0 s, at Bellvitge-ANTIGA and Bellvitge-PROV.
- 0 subjects have a grid length under 100, and 0 have a duration under 200 s.
- Duration varies within only 7 of the 23 sites: Amsterdam, Bangalore, Bellvitge-ANTIGA, Braga-act, Dresden and the two NYSPI sites.

O7. Statistics on the real design with synthetic outcomes, from `probe_stats_design.out.json`. Design ranks are 26/26 (full), 26/26 (Y-BOCS subset, n = 856, 23 sites, minimum site n 10) and 14/14 (medication subset).
- The medication subset is OCD subjects with codes 1 or 2, restricted to the 11 sites that have both codes: n = 301, 180 code 1 vs 121 code 2. Log duration varies within 4 of those 11 sites.
- Vectorised Freedman–Lane t* vs the naive OLS refit of Ŷ_red + e_red[P]: max |Δ| = 1.1e-13. Observed t vs statsmodels: 3.9e-14.
- Mundlak MixedLM (ML, `reml=False`) vs site-FE OLS: |β_LMM − β_FE|/SE ≤ 2e-13 in all 4 scenarios.
  - In 3 of the 4, site_var = 0, and the fit emits 7 warnings: "Maximum Likelihood optimization failed to converge", "Retrying MixedLM optimization with lbfgs", "Hessian … not positive definite", "MLE may be on the boundary", "Random effects covariance is singular". It still reports converged = True.
  - σ_LMM is 0.9756 against σ_FE 0.9835 in the iid scenario, a ratio of about 0.992 (ML divides by n).
- Null FPR (R = 400, B = 999; 2·MC SE = 0.022):

| Scenario | Freedman–Lane | Welch |
|---|---|---|
| Site effect aligned with site OCD fraction, ICC 0.3 | 0.0575 | 1.000 |
| ICC 0.1, site SD ratio up to 3×, t(4) noise | 0.0575 | 0.085 |

  Each scenario takes about 18 s. The Python loop that builds the per-site permutation indices dominates the time.
- Planted d = 0.15 under the aligned confound, R = 200. This used the FE σ, not the LMM σ.
  - Mean d̂ is 0.158 and SD 0.050, so about 2.3 MC SE above the planted value.
  - P(|d̂| ≥ 0.15) = 0.575.
- 192 subjects are under 18.

O8. Card facts that bear on the design.
- §3: the fallback triggers if more than 10% of subjects are degenerate for E1 or E2 at 10%. Exclusion is per endpoint ("degenerate … for that endpoint").
- §4: d = β̂/σ̂_ε, using the same MixedLM. The stop rule is |β_LMM − β_FE| < 0.01·SE.
- §6.1 gives only an AUROC with a CI, no p-value.
- §6.3 says "restricted to sites containing both codes".
- §7: sensitivity analyses are interpreted only for endpoints that survive.
- §10/§11: 1 thread per process; seeds 20261030, 20261031 and 20261032.

O9. Addendum r2.
- F.34–F.38 require: acceptance by group and site; degeneracy by group and site; per-subject grid length plus a floor in seconds; a pinned manifest; and the E2 AR(φ) bias stated.
- Item 31 says `acceptance` counts 2-swap no-ops, which `motif_statistics` cannot separate out.
- G.39 records an earlier full read of all 1,706 series as an item for the root to adjudicate.

O10. Old-suite command: `STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<repo> python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` gives 86 passed. Its AST/backprop scans glob only `src/*.py`; `scripts/` is only checked to exist.

## 2. Logic Chain

L1 (O1, O2). Card §12 hashes every file in `src/topic1_lagmotif/*.py` and `scripts/topic1_timing.py`, so an edit to any of them voids the card. T1.1 must therefore be tests only. The cohort tools must be new `scripts/topic1_*` files that call `extract_subject` and the other frozen functions unchanged. All 6 carded units and the 3 extraction-level §7 variants can be reached that way (O2).

L2 (O3, O4).
- The proposed file kills each survivor through `extract_subject`.
- `seeds_ignore_position` is invisible at position 0, so the tests use positions 7 and 1311 and compare against an independent `SeedSequence([20261030, p, ch, round(1000·d)])` oracle.
- `curl_returns_F` needs a fixture in which the top-k graphs of curl(F) and F differ. A shared-driver latency signal provides that, and the test asserts it so the fixture cannot pass without being informative.
- A TR of 1.8 gives n_trim = 23 > 0, which separates valid_T from raw_valid_T.
- Because the auditor's harness copies `tests/topic1_lagmotif` into each mirror, landing the file byte-identical in that directory and rerunning a redirected harness gives T1.1's "0 survivors" receipt.

L3 (O5). Card §7 defines the truncation as exactly 100 grid samples.
- Truncating the native series to floor(200/TR + 1e-9) samples after the head trim gives exactly 100 grid samples at all 7 TRs, spanning at most 200 s, and goes through the unmodified frozen chain.
- Survey_1's ceil rule gives 101 grid samples at 4 TRs, which contradicts the card text. The floor rule overrides survey_1 gap (g).
- Slicing after `preprocess` instead would z-score and detrend over the full series, so it is not the same estimand. Reject it.

L4 (O6). Every subject has a grid length of at least 100 and a duration of at least 200 s, and no series has trailing padding.
- A floor stated as "grid length ≥ 100", an integer test, keeps all 1,706 subjects. It avoids a float comparison at exactly 200.0 s, and any higher floor would drop whole sites.
- This closes survey_1 gap (i). The manifest can be built from header shapes. `NpyCohort.load` still enforces the interior-zero and zero-variance contract during extraction.

L5 (O7, O8).
- The equality β_LMM = β_FE holds to machine precision, so the card's stop rule works as a bug detector.
- On data where the Mundlak means absorb the site effects, statsmodels lands on site_var = 0 and warns. If the worker treats warnings as errors, or silently retries another optimizer until the warnings go away, the result depends on the optimizer path in ways the card never specified.
- So the pre-label addendum must say four things:
  - boundary fits are accepted;
  - the warnings and `mle_retvals` are logged;
  - the optimizer is fixed (statsmodels default, `reml=False`);
  - only the β-equality check stops the run.
- σ_LMM(ML) ≠ σ_FE (about −0.8%), and the card defines d with σ_LMM. Fixtures must compute d the same way the real analysis does. Using σ_FE moves d by about 1%, which matters only at the |d| = 0.15 boundary, but it is the card's definition.

L6 (O7). The vectorised Freedman–Lane is exact:
- t* = (x̃ᵀv)/‖x̃‖² ÷ sqrt(RSS*/(n−p)/‖x̃‖²);
- RSS* = ‖v‖² − ‖Q_Zᵀv‖² − (x̃ᵀv)²/‖x̃‖²;
- v = permuted reduced residuals;
- the observed t is the identity permutation.

  So B = 9,999 is cheap. Precomputing the permutations per site removes the loop cost. R = 2,000 × B = 9,999 should take about 15 min per scenario at the probe's speed (about 0.045 s per R at B = 999, scaling linearly with B; 추정). It runs faster with vectorised permutation generation or with scenarios run in parallel. Welch FPR = 1.0 in the aligned scenario is a ready-made "raw d / Welch" defect fixture.

L7 (O7). The designs for the secondary analyses are full rank now. In the medication subset, log duration is identified within only 4 of 11 sites, and exclusions could remove that. Gap (d) is therefore a guard rule: a deterministic QR rank check; drop the redundant nuisance column; log the drop. It is not an expected event.

L8 (O8, O9). The fallback rule needs no labels. Per-group and per-site degeneracy and acceptance rates (T1.3, F.34/F.35) do need labels. The order must therefore be:
1. extraction;
2. pooled degeneracy rates, the fallback decision, and the hash;
3. extraction-level §7 variants at the decided primary density;
4. review of the stats script and its sha256;
5. the label join;
6. group and site breakdowns and the inferential statistics.

L9 (O2, O9). Counting no-ops would mean changing `motifs._run_chain` or reimplementing the chain. The first voids the card; the second creates an unverified twin. Reporting `acceptance_mean` as defined, with the item-31 caveat, together with an acceptance-stratified sensitivity declared post-freeze, satisfies F.34 and T1.3.

## 3. Caveats

- **Data reads, disclosed for the root, in the same category as addendum G.39.**
  - `probe_truncation_and_lengths.py` opened all 1,706 npy files read-only with mmap. It read their shapes and the content of each last row only.
  - `probe_stats_design.py` joined those header-derived durations with real dx, age, sex, site, Y-BOCS presence and medication codes from metadata, all held in memory, to build a design with synthetic outcomes.
  - No imaging feature was computed, no real outcome was used, and nothing per subject was printed or written. Only aggregates per site or per subset appear in my outputs.
- The FPR evidence is a probe: R = 400 and B = 999, not the R ≥ 2,000 and B = 9,999 that T1.2 needs. Only 2 null scenarios were tested.
- The planted-recovery probe used the FE σ, and its mean is 2.3 MC SE above the planted d. That is plausibly chance, since β̂ is unbiased and 1/σ̂ has only O(1/df) bias. A fixture with a 2-SE tolerance will fail about 5% of the time by chance, so use a fixed seed with 3 SE, or a larger R.
- Not checked:
  - interior zero rows or zero-variance ROIs in the real data (extraction will raise; the survey reported 0 all-zero ROIs);
  - real degeneracy rates, which are unknown until extraction;
  - connectome or B300; I recommend local CPU;
  - MixedLM behaviour on the real outcome distributions;
  - the §6.1 static-FC memory footprint (about 1,706 × 46,056 values, about 315 MB as float32; 추정).
- I did not read the M1 peer explorers (r1_2, r1_3), to keep independence.
- DISPATCH.md replaces the embedded survey JSON with a pointer to the three survey handoffs, as stated in its header. The rest is verbatim.
- I deleted my mutation mirrors, which were code copies, after the runs. The JSON and log receipts remain.

## 4. Conclusion (recommended strategy for the M1 worker)

**Phase A, label-free, can run in parallel.**
1. **T1.1.**
   - Copy `verification/explorer_M1_r1_1/proposed_tests/test_extract_contract.py` byte-identical (sha256 `c4c8d629c88ecf519fd6aa37309b697f2ebc41151c1d1857077dd8c108282b3d`) to `tests/topic1_lagmotif/test_extract_contract.py`. Alternatively, write an equivalent file and re-earn the mutation receipt.
   - Copy `mutants_rerun_probe.py` into the worker's own verification folder and change `HERE`. It already includes the 2 extra seed mutants. Run it with `with_new` and `without_new`.
   - Expected: control 59 passed; 26/26 killed with the file; 7 survivors without it.
   - Put the receipts under `results/topic1/2026-10-31/`. Never run the auditor's scripts in place.
2. **T1.3 manifest, `scripts/topic1_manifest.py`.**
   - Record the count 1,706 and a digest of the sorted names over the whole cohort. A cohort-level digest reveals nothing about individual IDs.
   - Per position, record: site, TR, T, n_trim, valid_T, grid_len and duration_s.
   - Do not write per-position ID hashes unless they are HMACs keyed with a secret stored outside the repo. Short structured IDs make an unsalted per-ID hash brute-forceable.
   - Floor: grid_len ≥ 100 (equivalent to duration ≥ 200 s). All are kept now.
   - The runner asserts the count and digest before extraction.
3. **T1.4a, `scripts/topic1_cohort_extract.py`.**
   - Call `NpyCohort.load` → `extract_subject` with the frozen PARAMS.
   - Run locally: setsid nohup, nice 10, 12–14 processes, `NUMBA_NUM_THREADS=OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`.
   - Write resumable JSONL keyed by position, with params_sha256 per record. Catch `InvalidSeriesError` and `MissingSubjectError` per subject and log only the position and the exception class.
   - Run all 6 units. Expect about 12.5–13.1 CPU-h, about 1 h wall at 14 processes (추정, A3).
4. **Fallback decision, `scripts/topic1_fallback.py`.**
   - Compute pooled degeneracy at broadband@0.10:
     - E1: sd030C == 0.
     - E2: sd030C == 0 or sd030T == 0.
     - Denominator: subjects with a successful extraction. Fix this in the addendum.
   - Trigger if E1 > 10% or E2 > 10%. Write the decision JSON and its sha256 before any label is read.
   - Then extract the §7 variants at the decided primary density:
     - DCT 128 through the `params` override, which gives a new params hash;
     - 200 s truncation: `prepare_series(arr[: n_trim + floor(200/TR + 1e-9)], …)`, asserting grid_len == 100;
     - `attempts_factor=40`.

     That is about 9 CPU-h (추정). Running all variants label-blind removes any compute decision that depends on the outcome.
5. **T1.2, `scripts/topic1_cohort_stats.py`, plus tests in `tests/topic1_lagmotif/test_cohort_stats.py`.** Implement card §4–§6 exactly:
   - FE OLS t;
   - vectorised Freedman–Lane, as in `probe_stats_design.py` `fl_t`. Permute the reduced residuals within site, B = 9,999. Each analysis starts with a fresh `default_rng(20261031)`. Write down the exact permutation-generation algorithm, for example per b, sorted sites, `rng.permutation`.
   - MixedLM, `reml=False`, with the Mundlak means of dx, Age, sex dummy and log duration;
   - d = β_LMM/sqrt(scale_LMM);
   - stop if |β_LMM − β_FE| ≥ 0.01·SE;
   - Holm over E1 and E2;
   - survive if p_Holm < 0.05 and |d| ≥ 0.15;
   - the kill rule;
   - the §6 families with BH-FDR within each family, where family 1 is descriptive (gap f);
   - raw d and Welch labelled descriptive.

   Synthetic validation on the real design: null scenarios with aligned ICC 0.1 and 0.3, heteroscedastic sites, t(4) noise, and site- and group-correlated exclusions, at R ≥ 2,000, B = 9,999, with |FPR − 0.05| ≤ 2·sqrt(0.0475/R). Planted d = 0.15 and 0.30, computed with the LMM σ. Defect fixtures: cross-site permutation, Welch or raw d, Holm omitted, total-SD σ, flipped sign, 9% vs 11% at the fallback boundary, and the boundaries of the kill rule.

**Phase B, serial.**
6. Review of the stats script by someone other than its author. Record its sha256.
7. A dated pre-label addendum, `docs/03_empirical_analysis/topic1/2026-10-31_ADDENDUM_prelabel.md`, frozen with its sha256 recorded. It settles survey gaps a–i:
   - (g) the floor rule (L3);
   - (i) grid_len ≥ 100;
   - (d) the QR rank guard;
   - the MixedLM boundary and warning rule (L5);
   - the fallback denominator;
   - (b) the density of the secondary analyses after a fallback;
   - (a) what happens if 15% is also degenerate;
   - (c) the permutation stream for each endpoint;
   - (e) standardised β = β·SD(E)/SD(Y-BOCS) within the analysis sample;
   - (h) complete cases, with the same subjects for the comparator;
   - the acceptance-stratified sensitivity, labelled post-freeze.
8. Label join, then:
   - rates by group and site for degeneracy and acceptance, plus grid length;
   - primary statistics, then the verdict for each endpoint, stated exactly by card §5;
   - the §9 spurious-direction limitation and the degeneracy rates placed next to the verdict;
   - §7 analyses only for endpoints that survive;
   - §6 secondary analyses.

   Outputs go to `results/topic1/2026-10-31/` and `docs/03_empirical_analysis/topic1/2026-10-31_topic1_result_report.md`.
9. **T1.5.** Record every deviation, including the fallback if it triggers, in a dated addendum, never in the card. Report both densities if the fallback triggers.

## 5. Verification Method

- Protected files: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt --quiet; echo $?` should print 0.
- Card §12: `sed -n '/^```$/,/^```$/p' docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md | grep -v '```' | sha256sum -c` should give 10 OK.
- T1.1:
  - `sha256sum tests/topic1_lagmotif/test_extract_contract.py` should equal `c4c8d629…282b3d` if the file was copied.
  - `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 python3 -m pytest -p no:cacheprovider -q tests/topic1_lagmotif` should report 59 passed.
  - From the redirected harness: `python3 -B <worker_dir>/mutants_rerun_probe.py with_new` should end with `SURVIVORS: []`, and the `without_new` run should list 7 survivors.
- The auditor's receipts must be untouched: `sha256sum verification/victory_auditor_1/mutation_results*.json` should give `b9b74cac…2bb09a` and `1fdfa486…07edf`.
- Lengths and truncation: rerun `verification/explorer_M1_r1_1/probe_truncation_and_lengths.py`, which writes `.out.json`. Expect `n_last_row_all_zero` = 0, `grid_len_min` = 100, `n_dur_lt_200` = 0, and floor-rule grid_len = 100 at every TR.
- Statistics: rerun `verification/explorer_M1_r1_1/probe_stats_design.py`, about 1 min. Expect `fl_vectorised_vs_naive_maxabs` < 1e-10, every `mundlak.*.ratio_diff_to_se` < 1e-6, and FL_FPR within 0.05 ± 0.022.
- Invalidation conditions:
  - any change to the npy directory listing (count or digest);
  - any edit to `src/topic1_lagmotif`;
  - a statsmodels or numpy upgrade, which would require rerunning the MixedLM equality check;
  - an extraction exception rate high enough to change the fallback denominator.
- The probe hashes are recorded in O3 and in the structured return.
