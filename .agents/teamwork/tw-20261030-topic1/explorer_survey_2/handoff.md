# Handoff (Hard) — explorer_survey_2, run tw-20261030-topic1

Full report: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/explorer_survey_2/report.md
Probes (read-only, nothing written to disk): /home/juke/git/00IITP-AI/verification/explorer_survey_2/{probe_data_structure,probe_cohort,probe_graph_methods,probe_spurious_direction,probe_hodge,probe_null_numba,probe_checks}.py

## 1. Observation
- **Cache channels.** `enigma_ocd_mbbn/data_preprocess_and_load/datasets.py:224-239`: arr[0..3] are `fmri_imf1..4_sequence` and `'mask': torch.from_numpy(arr[4])`. There is no broadband channel. `src/mbbn_connectome_biomarker.py:378` wrongly says "Channel 0: broadband".
- **Mask and valid T.** The mask is binary and uniform across ROIs. Valid T = min(T_raw−20, 464) in 60/60 subjects. Cohort: 300 truncated, 1,406 padded, min T=100, duration 200–572 s. Group medians are equal (320 s, MWU p=0.50). T is near-constant within site.
- **Raw spectrum.** Raw npy carries ≤1.2% of its power above 0.25 Hz at all TRs.
- **Null defect (real data).** The existing null at 10·m swaps produced 51/177/322 reciprocal edges and nonzero 111D…210 classes. The real graph had 0 reciprocal edges, m=6,909 fixed, and nonzero classes {003, 012, 021D, 021U, 021C, 030T, 030C}.
- **Analytic census and SP degeneracy.** The analytic census equals nx.triadic_census. Under a degree-preserving, reciprocity-free null: Z = [021D 6.870, 021U 6.870, 021C 7.936, 030T −6.870, 030C −3.697].
- **Fast null.** The numba orientation-preserving swap costs 0.040 s per null at 100·m attempts. Degree, reciprocity and diagonal post-checks pass. 030C/030T plateau by about 10·m attempts.
- **Lag in seconds.** For a 2 s lead, lag-1TR at TR 0.7 gives F=+0.118 vs +0.339 at TR 2.0. After resample_poly(7,20) F=+0.333, with 100% sign agreement.
- **Spurious direction.**
  - Shared source with a smoothed copy: F=+0.21 to +0.32, lagging in 100% of replicates. Prewhitened: +0.10 to +0.23.
  - The real edge cutoff (85th percentile |F|) is 0.14–0.18.
  - Real per-ROI ac1 spread at TR 2 is p5–p95 0.03–0.61.
  - Spearman ρ(ac1, net out-degree) = −0.14 / −0.08 / −0.12 (n=3 subjects).
- **Gradient vs curl.** Latency-only synthetic: gradient share 0.988, 030C=0. Real: gradient share 0.47/0.17/0.08 with raw 030C 379/2,217/4,764. Curl-only 030C: 6,640/5,230/6,192.
- **Baselines.**
  - table1 baseline 0.6512±0.0318 (n=26)
  - Track-B Remediated_Baseline 0.6606±0.0262
  - Linear_SVM_static_FC 0.6420±0.0125
  - LOSO per-site mean 0.6519 (`results/site_driver_analysis.csv`)
  - 0.6285/0.6336 are medication-subgroup AUROCs
- **TR sources.** site_characteristics.csv TR contradicts `repetition_time()` at ≥10 sites. Chiba-CHBSRPB substring bug (2.3 vs 2.5).
- **Metadata.** No FD/motion column. Medication codes are documented at `medication_confound_analysis.py:23-24`. HC medication values are implausible. Sex 2=female (inferred). No ROI label table exists. A secondary-source audit says the 304 ROIs are cortical-only.
- **Packages.** neuroCombat and neuroHarmonize are missing. statsmodels, pingouin, numba and sklearn are present. CPU: 20 cores; ~68 GB available RAM.
- **Safety.** Protected hashes all OK (`sha256sum -c sentinel/PROTECTED_HASHES.txt`). The src/ and enigma `__pycache__` mtimes are unchanged by my probes.

## 2. Logic Chain
1. Real-graph reciprocity is impossible (antisymmetric F plus a positive threshold) and the existing null creates reciprocal edges. So the null must forbid both directions, and SP must be restricted to {021D, 021U, 021C, 030T, 030C} (A1).
2. In/out degree sums are invariant, so 021D/021U/021C are affine in 030T/030C. Hence Z(021D)=Z(021U)=−Z(030T) (verified). The primary should therefore be Z_030C and Z_030C−Z_030T, not SP_030C (A4).
3. TR-dependent autocorrelation, plus the lag-1TR inconsistency, plus a lossless 2.0 s grid (D7), lead to: lag = 2 s on a common 2.0 s resampled grid (A1, A2 lag test).
4. Cache IMFs are subject-specific bands near Nyquist with oscillatory autocorrelation, and there is no broadband channel. So the primary channel = raw npy broadband. This fixes the "planned channels" for A3.
5. Smoothing-type bias exceeds the edge cutoff, and real autocorrelation heterogeneity is wide. So A2 must report the bias magnitude as an open limitation, with an autocorrelation-matched surrogate for the independent case. The time-reversal flip is only an identity check.
6. Per-ROI latency generates gradient flow, which is acyclic. Real 030C tracks gradient share, so a group effect on 030C is confounded by lag ordering. Pre-register gradient share as a covariate and a curl-only sensitivity analysis.
7. The "≈0.63" baseline is not a main-cohort file number, and existing folds are not the new folds. The card cites exact paths and numbers and computes an in-house static-FC baseline on identical site-held-out folds.
8. ComBat is not installed, and with diagnosis protected it would leak under LOSO. Use LMM site random intercept plus within-site permutation; harmonize or scale only within training folds.
9. Duration is site-collinear, so a duration covariate alone is weak. Add common-200 s truncation as a sensitivity analysis or as the primary (the card decides).

## 3. Caveats
- Irreducibility of 2-swaps (Rao 1996; Berger & Müller-Hannemann 2010) and the Hodge framing (Jiang et al. 2011) are literature recall, not verified in-session.
- The cortical-only atlas claim rests on a prior agent audit (secondary source); I found no label table to confirm or refute it.
- Spurious-direction magnitudes come from stylized synthetic models. The real-data ρ(ac1, net degree) uses n=3 subjects.
- The timing projection comes from probes with the numba kernel. It is not the A3 measurement and assumes the worker adopts a comparably fast kernel.
- The "0.25" directory-name interpretation is unverified.
- The npy preprocessing pipeline (nuisance regression, GSR, slice timing) is unverified.
- The HANDOFF numbers for BNT/BERT/BrainLM/XGBoost were not checked against CSVs.
- The LOSO baseline comes from the pre-remediation `results/` directory.
- One exploratory `ls` displayed three participant-ID folder names in my session output only. They appear in no file I wrote.
- I did not re-verify the report-vs-JSON discrepancy; it is taken from APPROVED_PROPOSAL.md.

## 4. Conclusion
A1–A6 are satisfiable with on-disk data and installed packages. Recommended frozen parameters for the worker and card:
- **Input:** raw npy broadband, using the valid part (frames 20 onward; full length, not capped at 464). Exception for missing subjects: raise an error.
- **Preprocessing:** linear detrend, then resample_poly to 2.0 s, then z-score.
- **Flow:** lag τ = 2 s.
- **Graph:** A = [F > 85th percentile of |F|] (density 0.075).
- **Null:** numba 2-swap plus directed-triangle reversal, rejecting both reciprocal directions and self-loops. Assert zero reciprocal edges and equal in/out degrees for every null. Use ≥1,000 nulls (40 s each).
- **Statistics:** SP over 5 classes, documented as rank-2. Primary statistics Z_030C and Z_030C − Z_030T (Holm across 2). Gradient share reported; curl-only sensitivity.
- **Fixtures:** IAAFT/phase surrogate for the autocorrelation-matched null. HRF-smoothing bias reported as an open limitation.
- **Group inference:** LMM with site random intercept plus age, sex and duration, with p from within-site permutation.
- **Classification:** LOSO (23 folds) with train-only scaling, against an in-house static-FC baseline on the same folds.
- **Kill criterion:** |d| < 0.15 or p ≥ .05, with d and its direction defined.
- **Baselines cited:** 0.6519 (LOSO, `results/site_driver_analysis.csv`), 0.6512 and 0.6606 (random split), 0.6420 (SVM static FC).
- **Medication:** within OCD only (203 vs 212) with a site term. HC medication flagged.
- **CSTC:** dropped or marked exploratory.
- **FD:** stated absent.
- **Disclosure:** prior d=0.08 exposure.

No further dispatch requested. Suggested optional extra job: a reviewer verifies the M5 literature claim and checks multi-seed null convergence.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI/verification/explorer_survey_2 && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I <probe>.py` for each probe. They read data only and print counts or indices only.
- Inspect enigma `data_preprocess_and_load/datasets.py:224-239`, `time_series_utils.py:5-79,132-156`, `post_hoc_analyses/medication_confound_analysis.py:21-26`, `post_hoc_analyses/results_remediated/{table1_true_test_performance,track_b_10split_remediation_summary,medication_confound_remediated}.csv`, `post_hoc_analyses/results/site_driver_analysis.csv`.
- Inspect `src/mbbn_connectome_biomarker.py:42-47,150-169,213-214,374-403,412-419,444,522`.
- Invalidation conditions:
  - A ROI label table is found (this would change the CSTC decision).
  - Npy files turn out to be already resampled or differently filtered (this would change D7).
  - The worker's null kernel differs (timing projection void).
  - The existing src/tests change (the line references shift).
