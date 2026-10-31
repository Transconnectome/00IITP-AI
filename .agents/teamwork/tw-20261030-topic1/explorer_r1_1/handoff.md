# Handoff (Hard) — explorer_r1_1, run tw-20261030-topic1, milestone M1

**Summary.** The survey design mostly holds, with five changes that alter code or the card:
1. Remove the mean (linear detrend) BEFORE `resample_poly`. Resampling raw-scale data first destroys F (corr 0.00).
2. 15% density hides sparse planted cycles at N=304 (paired ΔZ030C 0.05, versus 2.96 at 5%), and at N=60 (min Z 11.1 at 5% vs −0.32 at 15%). The card must justify its primary density from synthetic power, and 5% is recommended. A pre-registered degeneracy rule is needed, because null SD = 0 is common in latency-dominated graphs at 5%.
3. Use 200 nulls, not 1,000. Monte Carlo (MC) SD of Z is about 0.10, which matches √((1+Z²/2)/n).
4. Raw pooled d with a Welch p gives 19.5% false positives under site structure. Use d and p from a site-adjusted model with a within-site (Freedman–Lane) permutation p.
5. HRF-latency bias at the graph level is several Z units. Neither the oriented null nor the curl-only variant removes it, so it is an open limitation backed by a characterization fixture.

On the null: the 2-swap-only chain is provably reducible on small oriented graphs. At N=60 and N=304, however, its null mean and SD match those of a richer move set within MC error. Recommendation: implement the richer move set as cheap insurance, and document the residual risk.

All probes are synthetic. No real subject time series was loaded by this explorer. Probes and logs are in /home/juke/git/00IITP-AI/verification/explorer_r1_1/.

## 1. Observation (probe → verbatim result)

| Probe (verification/explorer_r1_1/) | Result |
|---|---|
| p1_irreducibility_exhaustive.log (all 59,049 oriented graphs, N=5) | 2-swap only (both directions rejected, 4 distinct nodes): **7,862 / 12,382** non-singleton degree classes reducible. 2,920 of them have components with different 030C counts. With 3-cycle reversal added: 1,146 reducible. N=6, 40 sampled classes: 21 → 2 reducible. |
| p1b_cycle_reversal_closure.log | Adding 4-cycle and 5-cycle reversal still leaves N=5 at 1,096 reducible. Cycle reversals alone are not enough. |
| p1c_example.log | Minimal stuck pair: {1→4, 4→2, 2→3} and {1→2, 2→4, 4→3}. Moving between them requires the "middle-edge path move" a→b→c→d ⇒ a→c→b→d. |
| p1d_path_move_closure.log | 2-swap + 3-cycle reversal + path move: N=5 **60 / 12,382** reducible; N=6 **0 / 60** sampled classes reducible. |
| p1e_null_bias.log (600/200 independent chains from the observed graph, 2-swap vs mixed moves) | Null-mean difference / SE: N60 planted −0.53 (030T), −0.73 (030C); N60 latency 1.35, −0.27; N304 (m=6908) latency 0.25, −0.57; N304 planted 0.06, 1.26. SD ratio 0.92–1.06. Accepted moves per m (mixed, p_tri = p_path = 0.25): 3-cycle 0.001–0.016, path 0.003–0.015. Time per chain at N=304, 30m attempts: 8.8 ms (2-swap) vs 10.3 ms (mixed). |
| p2_detrend_resample.log (N=30, raw scale 1.15e4, random-walk drift 9–14% of power below 0.01 Hz, truth = drift-free population F) | **Resample raw, then z-score: corr(F, F_true) = 0.000** at TR 0.7 (200 s) and 0.019 (600 s). Constant-1.15e4 input gives first samples 7763.6, 12391.8 (edge transient). Demean, linear, quadratic or high-pass 0.01 Hz BEFORE resampling: corr 0.652–0.660 (200 s) and 0.828–0.832 (600 s). No-drift reference: 0.661. Edge trimming does not help (0.648–0.652). |
| p34_nullcount_threshold.log (N=304, m=6908, 2,000 nulls) | MC SD of Z030C: n=50 0.227 (formula 0.208); n=100 0.144 (0.147); n=300 0.063 (0.085); n=1000 0.020 (0.047, only 2 blocks). Swap factor 5/10/30/100: Z030C −1.66/−1.52/−1.43/−1.59, i.e. no drift beyond MC error. 8.6 ms per null at 30m. The percentile rule gave m=6909 and exact top-k gave 6908. |
| p4b_injection_vs_density.log (N=304, T=160, 3 seeds, paired planted vs control) | 60 planted 3-cycles, c=0.5: **paired ΔZ030C 2.96 at 5% density, 0.35 at 10%, 0.05 at 15%**. 20 cycles: 0.74 / 0.04 / −0.49. |
| p5_spurious_graph_level.log (N=60, TR 2, 150 samples, NO directed coupling, shared 3-factor driver with random-sign loadings, per-node delay SD σ) | σ=0: Z030C −1.75 (sd 1.60), Z030T −2.33. σ=0.5: −2.93 / −5.06. σ=2: −0.12 / −0.16. The response is non-monotone. Independent AR(1) with φ~U(0.05, 0.9): **Z030C 0.09 (SE 0.18)**, Z030T 0.43. |
| p5b_positive_loading.log (same, positive global loading) | σ=1 s: Z030C −1.03, **Z030T −6.76 (sd 3.32)**, contrast +5.73, **curl-only Z030C −4.95**. σ=2 s: Z030C −4.25, curl-only −6.68. At σ=0.25 and 0.5 s some nulls had **SD(030C) = 0, so Z was NaN** (RuntimeWarning: invalid value in divide). AR calibration: Z030C −0.02 (SE 0.24). |
| p6_d_p_definitions.log (real per-site dx counts 869/837 over 23 sites, from survey JSON aggregates; site ICC 0.5; heteroscedastic sites) | No effect: **raw pooled d / Welch P(p<.05) = 0.195**. Site-FE OLS Wald 0.053; FE with within-site permutation (499) 0.060; MixedLM 0.067. Site means aligned with site OCD fraction: raw 0.427 vs FE 0.045. True within-site δ=0.2: FE mean d 0.158, P(p<.05 & \|d\|≥.15) = 0.568; raw d 0.129, 0.385. |
| p7_fixture_tolerances.log | Time reversal through the full chain: TR 2.0 max\|F_rev+F\| = 7.7e-14 (exact). TR 0.7: 7.2e-3, corr 0.99999. TR 1.73: 1.3e-2, corr 0.99995. Padding with valid_T: max\|dF\| = 0.0; without truncation 0.87–0.90. Two-TR \|F\| ratio on top edges: resampled 1.075, lag-in-samples defect 0.593. **Sign agreement is 1.00 for both.** |
| p8_density_fixture_check.log (N=60, mixed kernel p_tri=p_path=0.1, 100 nulls; density 5/10/15%) | AR calibration mean Z030C: 0.16 (SE 0.29) / 0.40 (0.33) / −0.02 (0.25), degenerate 0/16 at every density. 20 planted cycles, Z030C mean (min) vs control mean (max): **13.55 (11.13) vs −0.01 (1.27)** at 5%; 5.48 (4.17) vs 0.23 (1.84) at 10%; **2.33 (−0.32) vs 0.57 (1.87) at 15%**, where a min/max fixture would FAIL. Latency σ=1 s, mean Z030T over 10 subjects: −2.05 (sd 1.15) / −4.37 / −6.13; curl-only Z030C: −2.30 / −4.01 / −4.85. **Degenerate nulls (SD of 030C or 030T = 0):** 7/10 subjects at σ=0 and 9/10 at σ=0.5 at 5%; 8/10 at σ=0.5 at 10%; 5/10 at σ=0.5 at 15%; curl-only graphs 0/10 everywhere. |
| enigma time_series_utils.py:5-75 | Ordered `if 'X' in site` chain. 'Chiba-CHB' (2.3) matches before 'Chiba-CHBSRPB' (2.5), and 'Braga-UMinho-Braga-1.5T' matches before '-act' (both 2, harmless). |
| Env | `python -I` ignores PYTHONDONTWRITEBYTECODE (-I implies -E). My probe dir got a `__pycache__`, which I removed. Survey dirs 2 and 3 also have `__pycache__`. No new pycache appeared in enigma, src or tests (find -newer ORIGINAL_REQUEST.md: none). Protected hashes: 0 failures at 2026-10-30T11:45Z. |

## 2. Logic Chain
1. Exhaustive enumeration (P1/P1b/P1d) shows the survey's 2-swap kernel is not irreducible on oriented graphs, and that cycle reversal alone does not fix it. The path move fixes almost all small cases.
2. At realistic sizes the null moments agree across move sets within MC error (P1e). So the 2-swap null is not demonstrably biased at N=304. The richer set costs about 15% and removes a reviewer objection. Implement it, and document that irreducibility is not proven.
3. Z's MC SD follows √((1+Z²/2)/n) (P3). Between-subject SD of Z is 1–3 even in homogeneous synthetic subjects (P5). At n=200, MC variance is ≤1–2% of the total, so 1,000 nulls buy nothing. A swap factor of 20–30 is enough.
4. The null 030C mean grows roughly with density³ while the planted contribution stays fixed. The planted Z therefore falls by about density^1.5, which matches P4b: 2.96 at 5% and 0.05 at 15%. A 15% primary density would likely miss sparse cyclic structure. The card must fix the primary density from this synthetic criterion before any real results (5% recommended), with 10% and 15% as sensitivity analyses.
5. resample_poly zero-pads. With a raw mean of about 1.15e4 that injects edge transients that dominate the z-scored series (P2 V0). Detrending before resampling is therefore mandatory, and its order needs a test. Drift barely affects antisymmetric F, because slow components contribute almost symmetrically to C_lag. Linear detrend is enough, and the high-pass filter is an optional sensitivity analysis.
6. The degree-preserving oriented null calibrates independent heterogeneous-φ nodes (P5/P5b AR rows). It does not calibrate shared-driver latency, or even zero-lag shared factors at σ=0 (P5: −1.75). The curl-only variant also stays biased (P5b). A2's last bullet is met by an AR calibration test plus an HRF-latency characterization test whose numbers go into the open issues. Neither should be called a control.
7. Under the real site/dx imbalance, an iid pooled d/Welch test is miscalibrated (P6). Site-adjusted d (β/σ_within) with a within-site permutation p is calibrated without covariates. With covariates, use Freedman–Lane. The card must define d and p this way and state the denominator, because d_FE is larger than raw d for the same effect.
8. Only the |F| ratio detects lag defined in samples (P7: sign agreement 1.00 either way). Exact time-reversal equality holds only at TR 2.0. Padding invariance is exact if truncation comes first.

## 3. Caveats
- All results are synthetic, and the model choices (AR noise, coupling 0.5, 3-factor driver, delay distributions) set the magnitudes. The real-data Z distribution and real power at each density are unknown. The worker's A3 timing on 5 subjects must not be used to choose density, because that would be peeking.
- Irreducibility: for the move set "2-swap + 3-cycle + path", N=5 still has 60 reducible classes. I did not find or test the complete move set and did not check literature. P1e compared means and SDs, not full distributions or higher moments.
- P4b used only 3 seeds and 150 nulls. The density trend is large and consistent with the scaling argument, but the exact ΔZ values are noisy.
- P6 used no covariates and a Gaussian outcome. Real Z may be heavy-tailed, so a rank-based sensitivity analysis is advised. The LMM and permutation rows have only 150 replicates (MC SE about 0.018 for a 5% rate).
- I did not re-verify the report-vs-JSON discrepancy, baseline numbers, cohort counts or the channel layout. I took them from the survey.
- Trim rule (20 samples vs 20 s) is a judgment call. No evidence probe was run.

## 4. Conclusion — worker strategy by Feature Inventory row

1. **Loader** (`src/topic1_lagmotif/data.py`):
   - Build the index from `sorted(os.listdir(npy_dir))`; positional index i equals mmap row i (survey).
   - Read with `np.load(path, mmap_mode='r')` and convert to float64.
   - Lead-in trim: `n_trim = ceil(20 s / TR)` (alternatively the cache's 20 samples). Freeze this in the card.
   - Return `valid_T`, `duration_s = valid_T·TR`, `n_trim`, TR and site.
   - Raise `MissingSubjectError(f"position {i}")` and include no ID. The test asserts that the ID string is not in `str(exc)`.
   - Raise on NaN, on all-zero ROI columns, and on interior all-zero rows.
   - Cache path: only a `valid_T_from_mask(mask)` helper. Do not use IMF channels in the primary.
2. **TR**: `tr_table.py` holds a copied ordered list citing `enigma_ocd_mbbn/time_series_utils.py:5-75`.
   - Raise on an unknown site, and raise if TR > 2.0.
   - The test compares the table with enigma `repetition_time` for all 23 cohort sites. Load enigma via `importlib.util.spec_from_file_location` with `sys.dont_write_bytecode = True`, and skip only if the enigma path is absent.
3. **Detrend**: linear detrend per ROI on the truncated native-TR series, BEFORE resampling. A 0.01 Hz Butterworth (sosfiltfilt, order 2) high-pass is an optional card sensitivity analysis. Order test: input with a 1.15e4 offset must give F with corr > 0.99 to the same data demeaned at TR 0.7. This test fails if the code resamples first (P2: 0.00).
4. **Resample and flow**:
   - `Fraction(TR/2).limit_denominator(1000)`, giving 7/20, 2/5, 17/40, 1/2, 173/200, 9/10, then `resample_poly(axis=0)`.
   - Z-score over valid samples, lag = 1 sample = 2 s, F = C − Cᵀ.
   - Document that a 2 s lag is phase-wrap-free for content at or below 0.25 Hz.
5. **Graph**: exact top-k by |F_upper| with a stable argsort, k = round(density·46,056), orientation from the sign of F.
   - **Primary density 5% (k=2303)** is recommended on P4b and P8; 10% and 15% are sensitivity analyses. The root or card owner decides this, but the choice must be frozen with its synthetic rationale.
   - Pre-register a **degeneracy rule** in the card, because P8 shows that gradient-dominated graphs often have null SD = 0, especially at 5%:
     - Z is missing for that subject, and the count is reported.
     - If more than 10% of the cohort is degenerate at the primary density, the frozen fallback primary is 10%.
     - Report a degeneracy-safe secondary statistic, log((obs+1)/(null_mean+1)).
   - The A3 timing JSON may report the degeneracy count for the 5 subjects. It is structural and carries no dx labels.
   - Every fixture threshold must be calibrated at the frozen density. Survey and P8 thresholds differ by density.
6. **Null**: numba (`cache=False`) mixed kernel (see `verification/explorer_r1_1/nullkernel.py`, probe-only):
   - 2-swap rejecting edges in either direction, with 4 distinct nodes;
   - 3-cycle reversal: uniform edge plus uniform node;
   - path move: uniform edge plus 2 uniform nodes.
   - Move probabilities fixed at p_tri = p_path = 0.1. All proposals are symmetric, so the uniform distribution is stationary.
   - Tested: the P1e equal-moments comparison against 2-swap ran at 0.25; the P8 calibration and invariants ran at 0.1.
   - Each null is an independent chain from the observed graph with 30·m attempts. **n_null = 200.**
   - Assert per null: no reciprocal edges, empty diagonal, identical in/out degrees.
   - Seeds: `np.random.SeedSequence([base, subj_idx, channel, density_code]).spawn(n_null)`, then integer seeds.
   - **Guard SD = 0, so that Z = NaN with a flag; never divide by zero (P5b).**
   - Also record the raw counts and null means.
7. **Census**: closed form. networkx `triadic_census` serves as the oracle in tests. SP over the 5 classes, with Z021D = Z021U = −Z030T and the 021C dependency documented. Primary statistics: Z030C and Z030C − Z030T.
8. **Hodge**: p = row-mean of F, G = pᵢ − pⱼ, gradient share = ‖G‖²/‖F‖². Report it as a covariate. The curl-only variant is a sensitivity analysis only; P5b shows it is still latency-biased.
9. **Fixtures** (`tests/topic1_lagmotif/`, with `__init__.py`, N ≤ 60, each check under about 2 s):

   | Fixture | Pass condition | How the defect shows |
   |---|---|---|
   | Null invariants | Hold for every null | v1 swap creates 250+ reciprocal edges |
   | Identity Z021D + Z030T | 0 (atol 1e-9) | |
   | Closed-form census | Equals nx on random oriented graphs | |
   | AR(1) calibration (φ~U(0.05, 0.9), 16 subjects, N=60) | \|mean Z030C\| < 0.75 | v1 null gives +2.47 |
   | ≥20 disjoint planted cycles at N=60 | Detected: P8 at 5% gives Z mean 13.6, min 11.1 vs control max 1.27. At 15% my generator FAILS (min −0.32); survey 3's generator reached 8.3 | Calibrate at the frozen density |
   | Padding, with valid_T | Exact equality | |
   | Time reversal | Exact at TR 2.0 (atol 1e-10); corr(F_rev, −F) > 0.999 at TR 0.7 and 1.73 | |
   | Two-TR \|F\| ratio on top edges | In [0.85, 1.15] | Defect gives 0.59 |
   | Missing subject | Raises; message is ID-free | |
   | Detrend-order test | See row 3 | |

   **HRF-latency characterization** (positive-loaded shared driver, σ ∈ {1, 2} s; avoid σ ≤ 0.5, which produced degenerate nulls):
   - Use the mean over ≥8 fixed-seed subjects with NaN excluded and counted. At 5% density P8 measured Z030T −2.05 (σ=1) and −3.26 (σ=2); curl-only Z030C −2.30 and −1.48.
   - Assert mean Z030T(σ=2) < −1 and mean curl-only Z030C(σ=1) < −1 at 5%. Re-measure if the density changes.
   - Write the values to `results/topic1/2026-10-30/spurious_direction.json` and to the open issues.
   - The test fails if someone claims the bias is controlled.
10. **Old suite**: run it by explicit file list as in the PROJECT.md contract (86 expected). Also run `sha256sum -c PROTECTED_HASHES.txt`. Use `-B` or `PYTHONDONTWRITEBYTECODE=1`, never `-I` alone.
11. **A3 timing** (`scripts/topic1_timing.py`), at the frozen configuration: broadband, the density set, 200 nulls, factor 30, mixed kernel, plus curl-only if registered.
    - Subjects: 5 positional indices chosen by a stated rule spanning TRs, e.g. the first index of the sites with TR 0.7, 0.85, 1.0, 1.8 and 2.0.
    - Record per-stage time (load, detrend, resample, flow, null, census), numba compile time separately, and peak RSS (`resource.getrusage`).
    - Run factor 30 vs 60 on the same subject.
    - Extrapolation is labelled 추정. The probe suggests about 2 s per subject-density, i.e. about 1 CPU-h per density for 1,706 subjects.
    - The JSON must contain no IDs, no dx labels and no group statistics.
12. **Card** (additions to the PROJECT.md row 12):
    - **d = β_dx / σ̂_within**: the dx coefficient from OLS `Z ~ dx + age + sex + log(duration_s) + C(site)` divided by the residual SD; dx = 1 for OCD (CSV code 1). Sign = OCD − HC. Two-sided.
    - **p = Freedman–Lane permutation p** of the t-statistic for β_dx, 9,999 permutations: fit the reduced model without dx, permute its residuals within site, add them back, refit the full model.
      - Plain dx permutation is not guaranteed calibrated with covariates correlated with dx: sex is 476F/393M in OCD vs 411F/426M in HC.
      - P6 tested only the covariate-free case.
    - **Holm across the 2 primaries** (Z030C and the contrast) at the primary density.
    - Kill rule: an endpoint survives only if Holm p < .05 AND |d| ≥ .15. The study is killed if neither survives.
    - Sensitivity: MixedLM with a site random intercept (Wald), and a rank-inverse-normal outcome.
    - Raw pooled d may be reported descriptively but is not used for the kill rule. Welch p is not used, because P6 measured false-positive rates of 19.5% and 42.7%.
    - State that |d| ≥ .15 is a point-estimate bar: survival is only about 55% at true d ≈ 0.16.
    - Add the density rationale (P4b), a shared-factor bias note (P5 σ=0), and the HRF bias numbers (P5b).
13. **Open issues**: add these to the survey list:
    - 2-swap reducibility, and residual reducibility of the mixed set at N=5;
    - density dilution;
    - shared-zero-lag-factor Z bias;
    - HRF latency bias not removed by curl-only;
    - degenerate nulls with SD = 0;
    - the repetition_time substring order (Chiba 2.3 vs 2.5);
    - detrend-before-resample;
    - `-I` disabling PYTHONDONTWRITEBYTECODE.

## 5. Verification Method
- Re-run any probe: `cd /home/juke/git/00IITP-AI/verification/explorer_r1_1 && OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -I -B <probe>.py`. Runtimes: P1 scripts about 22 s each, p1e about 2 min, p34 45 s, p4b 33 s, p5 about 1–2 min, p5b 9 s, p6 13 s, p7 under 2 s, p8 10 s. Compare the output with the matching .log file.
- These findings are invalidated if:
  - real-data A3 shows null SD = 0 is common at the chosen density (then raise the density or change the statistic);
  - the mixed kernel's null means differ from 2-swap beyond 3 SE on real graphs;
  - npy data turn out to contain content above 0.25 Hz at fast TRs (then resample_poly is lossy and the phase-wrap claim fails);
  - a ROI label table is found.
- Safety check: `cd /home/juke/git/00IITP-AI && sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` gave 0 failures at 11:45Z. `find /home/juke/git/enigma_ocd_mbbn -name '*.pyc' -newer .agents/teamwork/tw-20261030-topic1/ORIGINAL_REQUEST.md` returned nothing.
