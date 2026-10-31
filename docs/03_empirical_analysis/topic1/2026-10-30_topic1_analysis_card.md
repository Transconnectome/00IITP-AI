# Topic 1 analysis card (pre-registration): ENIGMA-OCD directed lag-motif enrichment

- Card date: 2026-10-30 (run tw-20261030-topic1, worker_r1). Frozen when written. Its sha256 is not stored in this file, because a file cannot contain its own hash. The hash is in `docs/03_empirical_analysis/topic1/2026-10-30_OPEN_ISSUES.md` and `results/topic1/2026-10-30/card_sha256.txt`.
- **No full-cohort result existed when this card was written.** Only the 5 A3 timing subjects (positional indices 1578, 1228, 932, 0, 57) were run on real data. Their feature values (counts, Z, SP) were computed as part of the timing, then discarded unlogged and never inspected. Only computational quantities were recorded: time, RAM, acceptance rate, degenerate-null flags, and |ΔZ| between two null settings of the same subject. No diagnosis label was loaded in this run.
- **Prior exposure, disclosed.** A v1 result from a defective pipeline is on record: `docs/03_empirical_analysis/empirical_results.json`, key `topic1_mbbn_connectome_biomarker`.
  - n = 60 (30/30, 57 of them from one site); IMF1 channel; 80 subsampled ROIs; a null that allows reciprocal edges; StratifiedKFold.
  - d(z_cycle3) = 0.0804, p = 0.757; AUROC 0.4756.
  - This card was not tuned to it. The v1 pipeline is not reused.
- Any change to the items below requires a new dated card. This card is not edited.

## 1. Frozen pipeline

| Item | Frozen value |
|---|---|
| Code | `src/topic1_lagmotif/` (sha256 per file in §12) |
| Parameters | `PARAMS` in `src/topic1_lagmotif/pipeline.py`, `params_sha256 = 86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6` |
| Input | Raw npy series in `/home/juke/git/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25/` (broadband, unpadded, raw scale), read only. The VMD cache IMF channels are **not** used: they contain no broadband channel, and their lag is ill-posed. |
| Subject index | Positional index into `sorted(os.listdir(npy_dir))`. The site comes from the metadata `Unique_ID → Sample` mapping, and the TR from `tr_table.repetition_time`, a cited copy of enigma `time_series_utils.py:5-79` tested for equality. |
| Valid portion | Trailing all-zero rows are stripped. Any interior zero row, NaN/inf or zero-variance ROI raises an error; no repair and no fallback. Then a head trim of ceil(40 s / TR) samples (20 at TR 2.0). valid_T and duration_s are recorded. |
| Preprocessing order | Per-ROI linear detrend at native TR → `resample_poly` to a 2.0 s grid with exact ratio Fraction(TR)/2 and `padtype='line'` → per-ROI z-score. No high-pass in the primary analysis. |
| Lag | 2.0 s = 1 grid sample. C[i,j] = mean_t z_i(t) z_j(t+1); F = C − Cᵀ, with F[i,j] > 0 read as "i leads j". |
| ROIs | All 304 |
| Graph | Exact top-k by \|F\| with stable sort, oriented by sign(F). Primary density 10% of unordered pairs: k = round(0.10·46,056) = 4,606. Sensitivity densities: 5% (2,303) and 15% (6,908). |
| Null | Orientation- and degree-preserving lazy chain counted by attempts. Moves: 2-swap, plus a 3-edge target rotation with p_rot = 0.2, which includes triangle reversal and the path move. A new edge is rejected if it exists in either direction or is a self-loop. Each null is an independent restart from the observed graph, with 20·m attempts. n_null = 1,000. Invariants are asserted on every null: in/out degrees, no mutual edge, no self-loop, m unchanged. Seeds: `SeedSequence([20261030, position, channel_code, density_code])`. |
| Census | Closed form over the 5 connected oriented classes {021D, 021U, 021C, 030T, 030C}. The 8 classes that need a mutual edge are structurally zero and excluded. networkx `triadic_census` is the test oracle. |
| Z / SP | Z = (obs − mean_null) / sd_null (ddof = 1). If sd_null = 0, Z is NaN and flagged ("degenerate"). SP = Z/‖Z‖ over the 5 classes. Rank-2 identity: Z021D = Z021U = −Z030T exactly. |
| Channels | `broadband` (primary). `curl` = F minus its Hodge gradient part, a descriptive sensitivity analysis only. |
| Per-subject covariate | Gradient share ‖G‖²/‖F‖², with G[i,j] = p_i − p_j and p = row mean of F |

Choice of density. The density was fixed from synthetic evidence only (explorer probes r1_1, r1_2 and r1_3, and `results/topic1/2026-10-30/spurious_direction.json`), before any real-subject run:
- At 15%, sparse planted cycles are diluted.
- At 5%, latency- or global-dominated graphs give degenerate nulls much more often. In the synthetic data, 12/12 degenerate for a shared zero-lag signal and 6/12 for a 1 s latency spread, at N = 60.
- One of the 5 A3 subjects was degenerate at 5% and none at 10%. This was observed after the freeze and changed nothing.
- Z values are never pooled or compared across densities.

## 2. Hypotheses (two-sided)

- **H1.** At the primary density, the broadband lag-2 s directed 3-cycle enrichment Z030C (E1) differs between OCD and HC. Theory motivating it: recurrent CSTC loops, which would predict OCD > HC. The test is nevertheless two-sided, and the 304 cortical ROIs cannot localize CSTC (§8).
- **H2.** The cyclic-vs-feed-forward contrast E2 = Z030C − Z030T differs between OCD and HC.
- Secondary hypotheses (§6) cover Y-BOCS association within OCD, medication-code contrast within OCD, and site-held-out classification. None of them can rescue a killed primary endpoint.

## 3. Population

- N ceiling = 1,706 subjects with data on disk, from 23 sites, TR 0.7–2.0 s. Counts per TR: 0.7: 43, 0.8: 96, 0.85: 104, 1.0: 119, 1.73: 39, 1.8: 110, 2.0: 1,195. Diagnosis from metadata `OCD`: code 1 = 869, code 2 = 837.
- The metadata has 2,095 rows, so 389 are absent from disk:
  - 388 are from the 6 sites with TR > 2.0 s: Chiba-CHB 42, Chiba-CHBC 53, Chiba-CHBSRPB 89, Kyoto-KPU-Kyoto1.5T 25, Seoul-SNU 95, Shanghai-SMCH 84. These sites are excluded by design, because the 2.0 s grid cannot represent them.
  - 1 is a Vancouver-BCCHR subject (TR 2.0) missing for an unknown reason.
- Diagnosis coding: 1 = OCD, 2 = HC. Sources: the `medication_confound_analysis.py:22` docstring and `site_driver_analysis.py:235`. The coding is corroborated by Y-BOCS being non-null in 856 code-1 vs 123 code-2 subjects. Counts verified 2026-10-30. The enigma manuscript and the spec give 833/873; this conflict is open (OPEN_ISSUES).
- Exclusions during the cohort run:
  - a subject whose series violates the data contract (error raised);
  - a subject whose primary-endpoint null is degenerate (Z NaN) for that endpoint.
  - Both counts are reported by group and site. Nothing is imputed.
- Degenerate fallback, pre-registered: if more than 10% of subjects are degenerate for E1 or E2 at 10%, the primary density becomes 15%, and 10% is reported as a sensitivity analysis. The log ratio log((obs+1)/(null_mean+1)) for 030C is always reported as a degeneracy-safe secondary.

## 4. Confound handling and primary model

- **Site.** ComBat is not used: neither neuroCombat nor neuroHarmonize is installed (installing them is not authorized), and ComBat leaks labels under site-held-out CV. Site is instead handled by:
  - a **linear mixed model with a site random intercept** (statsmodels MixedLM, ML fit);
  - **Mundlak** site means of every within-site regressor. With these means included, β_dx equals the site fixed-effects (within) estimator. This equality is checked numerically: |β_LMM − β_FE| < 0.01·SE is required, otherwise the run stops for review.
- **Covariates:**
  - dx (1 = OCD, 0 = HC);
  - age (linear);
  - sex (categorical codes 1/2; the meaning, 1 = male per `site_driver_analysis.py:237`, is not codebook-verified and does not matter for adjustment);
  - log(duration_s) of the valid portion.
  - TR is constant within site and is absorbed by the site terms. Duration is nearly collinear with site and cannot be interpreted separately.
- **Motion.** Framewise displacement / motion is NOT available: there is no FD, DVARS or motion column in `ENIGMA_QC_final_subject_list.csv`, and no file on local disk. Motion cannot be controlled, and this is a stated limitation.
- **Effect size.** d = β̂_dx / σ̂_ε, where σ̂_ε = sqrt(residual (level-1) variance) of the same MixedLM. Sign = OCD − HC.
- **p-value.** A two-sided Freedman–Lane permutation p for the t-statistic of dx in the equivalent site-FE OLS model (Y ~ dx + age + C(sex) + log duration + C(site)):
  - permute the reduced-model residuals **within site**;
  - B = 9,999, seed 20261031;
  - p = (1 + #{|t*| ≥ |t|}) / (B + 1).
  - The LMM Wald p is reported as secondary.
- Raw pooled Cohen's d and Welch p are **descriptive only**. Under the real site × diagnosis imbalance they are miscalibrated: explorer probes show a 19.5% false-positive rate at H0, and up to 98% when site means align with site OCD fraction.

## 5. Primary decision rule (kill criterion)

- Two primary endpoints at broadband@0.10: E1 = Z030C and E2 = Z030C − Z030T.
- **Multiple comparisons.** Holm–Bonferroni across exactly these 2 endpoints, at α = 0.05. The 5 SP components are not independent (rank 2) and are never counted as separate tests.
- An endpoint **survives** only if p_Holm < 0.05 **and** |d| ≥ 0.15.
- **Topic 1 is killed** if neither endpoint survives, i.e. |d| < 0.15 or p_Holm ≥ 0.05 on each.
- **Operating characteristics, disclosed.**
  - SE(d) ≈ 0.048 at n ≈ 869/837, so p_Holm < 0.05 corresponds to roughly |d| ≥ 0.11, and the |d| ≥ 0.15 bar is binding.
  - |d| is a point-estimate bar: a true d of 0.15 is killed about 50% of the time.
  - Synthetic probes give a minimum detectable d ≈ 0.149 at 80% power with α = 0.025.
- Sensitivity analyses (§7) are interpreted only for endpoints that survive. They cannot revive a killed endpoint.

## 6. Secondary analyses (each family: BH-FDR q < 0.05 within family)

1. **Site-held-out classification (OCD vs HC).**
   - Folds: LeaveOneGroupOut over the 23 sites.
   - Features: [Z030C, Z030T, gradient share] at broadband@0.10.
   - Model: L2 logistic regression, C = 1; standardization fit on training folds only; no harmonization.
   - Metrics: pooled out-of-fold AUROC, with a 95% CI from a site-level bootstrap (2,000 resamples), plus the mean per-site AUROC.
   - **In-house comparator** on identical folds: static FC, i.e. the upper-triangle Pearson correlations of the same preprocessed 2.0 s-grid series, with PCA (fit on training folds, 50 components) and L2 logistic regression.
   - External file-backed baselines, cited for context only. They are not comparable folds unless stated:

     | Baseline | AUROC | Source |
     |---|---|---|
     | MBBN baseline, random split, 26 evaluated seeds (4 rows `checkpoint_missing`), test N = 255 | 0.6512 ± 0.0318 | `enigma_ocd_mbbn/post_hoc_analyses/results_remediated/table1_true_test_performance.csv`, condition=baseline |
     | MBBN Remediated_Baseline, 10 random splits | 0.6606 ± 0.0262 | `.../results_remediated/track_b_10split_remediation_summary.csv` |
     | Linear_SVM_static_FC, 10 random splits | 0.6420 ± 0.0125 | same file |
     | MBBN LOSO, pre-remediation, notebook-sourced | per-site mean 0.6519 (N-weighted 0.6477, median 0.6707, 23 sites) | `.../post_hoc_analyses/results/site_driver_analysis.csv`, column `auroc_scratch_mean` (also hard-coded at `site_driver_analysis.py:160-184`) |

   - The often-quoted "MBBN AUROC ≈ 0.63" matches no main-cohort file and is **not** used. All numbers above were re-aggregated from the files on 2026-10-30.
2. **Y-BOCS (within OCD only).**
   - Sample: code-1 subjects with non-null Y-BOCS (856).
   - Model: Y-BOCS ~ E + age + C(sex) + log duration + C(site), for each of E1 and E2.
   - Report standardized β with a within-site Freedman–Lane permutation p.
   - Y-BOCS in HC (123 non-null) is not used.
3. **Medication (within OCD only).**
   - Contrast: code 1 (n = 203) vs code 2 (n = 212). Excluded: code 3 (447) and NaN (7).
   - Restricted to sites containing both codes, with site fixed effects.
   - **The coding direction is contradictory in the source repo.**
     - `post_hoc_analyses/medication_confound_analysis.py:23`: 1 = medicated, 2 = unmedicated, 3 = unknown.
     - `post_hoc_analyses/site_driver_analysis.py:239`: 1 = drug-free, 2 = medicated, 3 = unknown.
   - The analysis is therefore reported as "code 1 vs code 2". No medication interpretation is made until the data owner confirms the codebook.
   - HC medication codes (1: 405, 2: 177, NaN: 255) are flagged as unreliable and never used.

## 7. Pre-registered sensitivity analyses (for surviving endpoints only)

- Densities 5% and 15%.
- Gradient share added as a covariate. Interpretation rule: an effect that disappears after this adjustment is reported as "not separable from hemodynamic-latency/global-signal nuisance". A latency-spread confound can survive the adjustment (see §9).
- Curl-only channel. This is descriptive, has low power for planted cycles in synthetic probes, and is **not** a latency control.
- DCT high-pass at 128 s after resampling.
- Common 200 s truncation (the first 100 grid samples after the head trim).
- Rank-inverse-normal outcome.
- MixedLM without the Mundlak terms.
- 030C log-ratio statistic.
- Leave-one-site-out influence on β_dx.
- Excluding participants younger than 18.
- Attempts factor 40 instead of 20 (A3 diagnostic below).

## 8. Anatomy and CSTC

- There is no label table for the 304 ROIs on local disk. The enigma methods text calls the set a cortical-only Schaefer-400 subset, which is unverified.
- `DEFAULT_CSTC_ROIS` in `src/mbbn_connectome_biomarker.py:41-47` has no source.
- **The CSTC subnetwork analysis is dropped.** Any ROI-level description is exploratory and is labelled only as "ROI index i".

## 9. Known limitations (details and numbers in OPEN_ISSUES)

- **Spurious direction without neural coupling.** Synthetic, N = 60, 12 seeds, primary density; `results/topic1/2026-10-30/spurious_direction.json`.
  - Heterogeneous AR(1) φ is calibrated for Z030C (mean −0.38 ± 0.35), but shows a Z030T shift of about +0.8.
  - A shared driver with per-ROI latency SD 1 s gives Z030T ≈ −7.6 and E2 ≈ +7.3. With SD 2 s: Z030C ≈ −1.9 and E2 ≈ +6.9.
  - The oriented null does not remove this, and neither does curl-only (curl Z030C ≈ −5).
  - A group difference in regional hemodynamic latency, or in global-signal amplitude, could therefore produce an E1/E2 group effect.
- Irreducibility of the null move set on oriented graphs is not established. Uniformity is verified only on small, fully reachable classes, and 2-swap-only chains are shown to be reducible.
- Per-subject Z is not a calibrated z-score: it is overdispersed under the null.
- The npy preprocessing provenance is unknown: GSR, nuisance regression and slice-timing correction are unverified. Slice-timing differences alone can create per-ROI latency.
- No motion data.

## 10. Compute plan (추정, from A3; the cohort run is a separate approval, step 5, NOT authorized here)

- **Measured.** `results/topic1/2026-10-30/a3_timing.json`: 5 subjects, 1 thread each, 1,000 nulls, factor 20.
  - About 4.4 s per (channel, density) unit; 2.4 s at 5%, 4.8 s at 10%, 5.9 s at 15%.
  - Load, preprocess and Hodge take about 0.01 s per subject.
  - Peak RSS 292 MB; numba compile 0.78 s per process.
- **Extrapolated, 1,706 subjects (추정).**
  - All 6 planned units (2 channels × 3 densities): about 12.5 CPU-h.
  - Primary unit only: about 2.3 CPU-h.
  - About 0.8 h wall time on 16 cores.
- **Mixing diagnostic at the primary unit** (|ΔZ030C| between factor 40 and factor 20): 0.04–0.33 across the 5 subjects. Split-half (500 vs 500 nulls): 0.02–0.70.
- One subject had a low acceptance rate (0.074 vs 0.62–0.75 for the others). For the cohort run, the attempts factor is fixed at 20 and the factor-40 analysis is a sensitivity analysis (§7). No change is made from these diagnostics.

## 11. Reproducibility

- Seeds: SeedSequence([20261030, position, channel_code, density_code]) for nulls; 20261031 for permutations; 20261032 for the bootstrap.
- Threads are pinned to 1 per process, and processes run in parallel across subjects.
- Outputs record params_sha256, the positional index, valid_T, duration_s, n_trim, TR, the degenerate flags and the acceptance rate. They contain no participant IDs.

## 12. Code hashes at freeze (sha256)

```
cb0b70ae8500c847bea59f57960e90e4496d4e9971fc99f74f49c9a279d1e1d2  src/topic1_lagmotif/__init__.py
d320bfe4afdd81fca5005c0aef6677f8aed0395e3e1146b98108e5599a9695e9  src/topic1_lagmotif/data.py
bead276472e5594c99d55c55f4a949e58ddb1070131730be8b745f19c121686c  src/topic1_lagmotif/flow.py
ab6997b97bee16b694f53dd6557aa5afe970c4141b062b6778fef838ba8de627  src/topic1_lagmotif/motifs.py
99bfc9f12e5406997a40a6d0285dcac54400701f9c41017c370ff5b79123be94  src/topic1_lagmotif/pipeline.py
1520aef9c8a6ea69abfa052b198bf3ac34de6d82eef3f192b7f4b1c30f70d65f  src/topic1_lagmotif/preprocess.py
b246356c374e07ed200a303c359778386b6d61bc3cbad6a7b8befa3959991067  src/topic1_lagmotif/spurious.py
64f29139c22dedad02cec52e56156893d4f2bbdae7a576d6cda713d6769b9550  src/topic1_lagmotif/synthetic.py
a3837b151b44dac5a144cb1fcf7f2286d3b944dc830d5fcfd76e5f92b2886b8d  src/topic1_lagmotif/tr_table.py
1e5224b1b5eb618cc0d2fe321675dd4348cffe3fa6a4081d44aa7435c97a0eec  scripts/topic1_timing.py
```

The cohort-level analysis script (models in §4–§6) is not part of this run. It must implement exactly these definitions and is subject to independent review before execution.
