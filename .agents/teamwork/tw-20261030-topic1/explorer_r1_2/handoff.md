# handoff — explorer_r1_2 (Hard handoff, M1 strategy)

Summary. The survey architecture holds. Six design choices need explicit decisions that are backed by probes:
- Null: 2-swap plus 3-edge rotation, counted by attempts, factor 20, K=1000.
- Preprocessing: demean or detrend before `resample_poly`, then a 128 s DCT high-pass on the 2 s grid.
- Threshold: fixed m by `argpartition`, 15% primary with 10% and 20% sensitivity.
- Main confound: shared (global) signal strength biases raw Z030C−Z030T by up to −5 to −7, with no latency and no HRF differences. Gradient share as a covariate and curl-only endpoints must be pre-specified.
- Effect estimate: d and p come from a within-site estimator. The naive pooled d has a type-I rate of 0.99 under site confounding.
- Fixtures: concrete specs below, including an aligned-T trick that makes time reversal exact at fast TRs.

Real data: no real subject data was read by this explorer. All probes are synthetic, under /home/juke/git/00IITP-AI/verification/explorer_r1_2/ (SHA256SUMS.txt there). Protected hashes check: rc=0 at start and at end.

## 1. Observation

All values come from probe logs and JSON files in verification/explorer_r1_2/.

### P1a/P1b — irreducibility on small oriented graphs

Exhaustive check: probe_irreducibility_small.out.json and probe_irreducibility_3swap.out.json.

**N=5, all 59,049 oriented graphs:** 24,123 degree classes, of which 12,382 have size ≥2.
- 2-swap only: 7,862 of 12,382 classes are reducible.
- 2-swap + directed-triangle reversal: 1,146 reducible.
- 2-swap + 3-edge target rotation: 60 reducible. The rotation is (u1→v1, u2→v2, u3→v3) → (u1→v2, u2→v3, u3→v1), and it includes triangle reversal as a special case.

**N=6, 80 sampled classes:** with 2-swap + 3-rotation, 0 of 80 are reducible. In a separate sample of 66 classes, 2-swap only left 41 reducible, and the worst largest-component fraction was 0.071.

Concrete obstruction at N=5: the paths 1→0→2→3 and 1→2→0→3 cannot be reached from each other by any 2-swap, because every candidate creates a mutual edge. One 3-rotation connects them.

### P1c — large N (N=304, m=6,908 via argpartition)

probe_mixing_large.log, realistic regime chosen by probe_calibrate_regime.log. Raw 030C runs from about 130 to 2,200. Real-subject raw 030C reported by the survey: 379–4,764.

Null means, 2-swap versus 2-swap+rot(p=0.2), at factor 20 (attempts per edge):
- drive 0.3: 030C 1885.9 vs 1885.1 (sd about 46); 030T 15744 vs 15747 (sd about 110).
- drive 0.6: 030C 134.1 vs 134.6 (sd about 15); 030T 19970 vs 19970 (sd about 190).

Convergence by factor:
- Factor 2 is not converged: drive 0.6 030T is 20,080, against about 19,960 at factors 5, 20 and 50. That is about +0.6 null sd.
- Factors 5, 20 and 50 agree within Monte Carlo (MC) noise.

Cost per null (numba, one thread):
- 2-swap: 0.0048–0.0051 s at factor 20; 0.010 s at factor 50.
- 2-swap+rot: 0.0063–0.0066 s at factor 20; about 35% extra.

### MC SD of Z versus K

Real Z030C about −4.1, Z030T about +3.3. Rows are MC-SD of Z030C / MC-SD of Z030T:
- K=50: 0.44 / 0.38
- K=100: 0.30 / 0.23
- K=200: 0.19 / 0.18
- K=500: 0.10 / 0.08

### P2 — preprocessing

**Edge transients** (probe_detrend_resample.log, part a). `resample_poly(x, 7, 20)` on raw-scale data (mean 1.15e4, sd 34):
- `padtype='constant'` (the default): edge deviation 110.2 SD.
- `'mean'` or `'line'`: 0.83–0.84 SD.
- Demean first, then `'constant'`: 0.88 SD.

**Drift removal with non-DCT drift** (probe_detrend_v2.log). Values are corrF/Jaccard against the drift-free F.
- FFT drift below 0.01 Hz, T=160, drift fraction 0.3: none 0.980/0.747; linear 0.984/0.762; quadratic 0.988/0.783; Butterworth 0.01 Hz order 2 filtfilt 0.995/0.857; DCT 128 s 0.996/0.876.
- AR(0.995)+linear drift: all methods within 0.01–0.04 Jaccard of each other. DCT and Butterworth are best at fraction 0.3. Butterworth is slightly worst at fraction 0.1, T=286 (0.816 vs 0.834).
- The first drift probe (probe_detrend_resample, part b) built its drift from the DCT basis and is NOT valid evidence for ranking the methods. Its Z030C columns carry no information.

### P3 — density

probe_threshold.log.
- **Latency/shared regime at N=304:** the contrast is −3.5 / −7.0 / −7.0 / −8.1 / −6.3 at densities 5 / 10 / 15 / 20 / 30%. The bias is present at every density.
- **Injection fixture at N=60:** injected minimum Z030C is 17.4 / 6.6 / 3.5 / 2.9 / 1.3 at the same densities. Control maximum |Z| is 1.4–2.0.

### P5 — spurious direction

**Heterogeneous AR(1) without coupling** (probe_spurious_curl.log; N=60, T=150, φ~U(0.1,0.9), 20 seeds):
- Mean Z030C 0.13 (sd 1.15); mean contrast 0.37 (sd 1.67).
- Fraction with |Z030C| > 1.96: 0.05.
- Conclusion: the oriented degree-preserving null controls this case.

**Shared signal, equal HRF, N=304** (probe_shared_signal.log, 4 seeds each):

| shared | gradient share | raw Z030C | raw Z030T | raw contrast | curl-only contrast |
|---|---|---|---|---|---|
| 0 | 0.008 | −0.08 | 0.52 | −0.60 (sd 2.4) | −0.49 |
| 0.3 | 0.16 | — | — | +1.29 | −1.5 |
| 0.6 | 0.43 | −1.82 | 3.36 | −5.17 | −0.88 (sd 2.6) |
| 0.9 | 0.76 | −0.68 | 5.25 | −5.93 (sd 0.6) | +1.81 (sd 2.25) |

The bias needs a shared component. It appears with no latency or HRF differences, as a finite-sample cross-term between the shared signal and private noise that has a gradient form.

**HRF peak spread, N=304** (probe_spurious_curl.log): raw contrast −7.2 for peaks 4.5–5.5 s and −7.5 for 4–6 s. Curl-only gives −1.8 and +0.4, with sd 2–3.7.

**Injection fixture design** (probe_injection_recursive.log). Recursive injection g=0.8, 20 disjoint cycles, N=60, T=200, 15%, K=200, 8 seeds:
- White background: injected mean 8.69 (min 3.84); control mean 0.19 (max 2.13). Curl-only injected mean 8.57 (min 4.31).
- Heterogeneous-AR background: injected minimum 0.65. Do not use this background.
- AR+latency background: injected minimum 3.38; control maximum 2.58.
- Feed-forward injection (probe_injection_curl.log) is weak: mean about 1.7–3.5. Do not use it.

### P6 — d and p

probe_stats_dp.log. Synthetic cohort with the ENIGMA site sizes, OCD fraction 0.18–0.82 by site, and site intercept correlated with OCD fraction; 150 reps.

| estimator | mean d (true 0) | type-I at 0.05 | mean d (true 0.15) | power at 0.05 | power at 0.025 |
|---|---|---|---|---|---|
| naive pooled | 0.305 | 0.993 | — | — | — |
| MixedLM random intercept | 0.006 | 0.033 | 0.165 (biased up) | 0.90 | — |
| OLS site fixed effects | −0.004 | 0.053 | 0.154 | 0.82 | 0.71 |
| MixedLM + Mundlak site-mean(dx) | identical to fixed effects | | | | |

Other results:
- MixedLM fit: 0.015 s.
- Within-site permutation using FWL with OLS-FE: 2,000 permutations in 1.34 s.
- Two-sample power at d=0.15 (869/837): 0.872 at α=0.05; 0.804 at α=0.025. MDD at 80% power and α=0.025: 0.149.

### P7 — time reversal through the full chain

Chain: linear detrend → `resample_poly(padtype='line')` → DCT 128 s → z-score → lag-1 F.
- probe_time_reversal_chain.log: exact at TR 2.0 (max|F+Frev| = 3.9e-13). Inexact at TR 0.7 / 0.85 / 1.73 (0.069 / 0.037 / 0.022).
- probe_time_reversal_aligned.log: exact (≤1.6e-11) whenever (T−1)·TR/2 is an integer. Examples: TR 0.7 with T=21, 41, 201, 401; TR 0.85 with T=41, 401; TR 1.73 with T=201, 401; TR 1.8 with T=11, 101. The same probe gives 0.056 for TR 0.7 at T=400.
- probe_time_reversal_chain also has `padding_truncate_first_maxdiff=0`. That holds BY CONSTRUCTION (I sliced with the known T), so it is not evidence.

### Survey facts used but NOT re-verified by r1_2

Source: survey_results_flat.txt.
- Valid T and mask rule; npy files unpadded.
- TR map via `time_series_utils.repetition_time`, and the resample ratios.
- Cohort counts 869/837; 389 absent = 388 + 1.
- Baselines 0.6512 / 0.6606 / 0.6420 / LOSO 0.6519.
- Medication coding 203/212; no FD column; no ROI label table.
- Closed-form census matches networkx.
- Reciprocal edges created by the v1 null; v1 calibration bias +2.47.
- Real gradient share 0.08–0.47.

## 2. Logic Chain

1. **Irreducibility.** Small-N enumeration shows that 2-swaps alone fragment most oriented degree classes. Rotation moves fix almost all of them, but not every class (60 of 12,382 at N=5). Irreducibility therefore cannot be claimed. At N=304 and 7.5% density, the null moments of the two move sets agree within MC SE. Rotation moves are cheap insurance (about 35% extra), plus an empirical agreement check. Never write "irreducible".

2. **Stationarity.** With symmetric proposals, a lazy chain where a rejected attempt counts as a step has the uniform distribution on each class as its stationary distribution. Counting only accepted swaps instead samples states in proportion to the number of valid moves. v1 and the survey-3 prototype both use `while done < n_swaps`. This point is theory and was not probed; the magnitude is expected to be small at N=304. Use attempt counting.

3. **Null count and factor.**
   - Factor ≥5 converges and factor 2 does not. Choose 20 for margin, and check 20 vs 50 on the 5 timing subjects.
   - K=1000 gives MC-SD of about 0.07 for |Z|≈4. Extrapolated from K=500 at 0.10 with a √K law; not measured directly.
   - Cost is 6.5 s per subject-channel, about 3.1 CPU-h per 1,706 subjects per variant (추정).
   - The worker's A3 run must record the between-subject SD of Z (positional indices only, no group statistics). From that, report the attenuation factor sqrt(1 + MC_var / between_var). It is expected to be ≥0.99 if the between-subject SD is ≥1.

4. **Resampling.** `resample_poly`'s default zero padding at raw scale gives 110 SD edge spikes. This must be a hard rule: detrend before resampling, plus `padtype='line'`.

5. **High-pass.** DCT regression at a 128 s cutoff is the best or tied-best option for non-DCT drift, and it has no filtfilt edge transient on 100-sample scans. Linear detrend before resampling (needed for item 4) plus DCT 128 s after resampling on the 2 s grid is consistent across sites.

6. **Shared-signal confound.** The shared signal produces a gradient-dominated F. Under the degree-preserving null this gives Z030T > 0, Z030C < 0 and contrast −5 to −8. Shared-signal or global-signal strength can differ by site preprocessing (GSR unknown) and by group, and motion is unmeasured. So the raw primary contrast is confounded by a quantity that has nothing to do with cycles.
   - Curl-only (F minus its least-squares gradient, p = F.mean(0)) removes most of the bias, but it is noisy (sd 2–3.7).
   - Planted cycles survive curl-only: injected mean 8.57 vs 8.69 raw.
   - Therefore the card must pre-specify gradient share as a reported covariate, and curl-only Z030C and contrast as a pre-registered sensitivity analysis with an interpretation rule.

7. **d and p.** The naive pooled d is grossly biased under site confounding. The random intercept is slightly biased, while fixed effects and Mundlak are unbiased. Choose a within-site estimator. ACCEPTANCE names an "LMM random effect", which MixedLM + Mundlak satisfies with fixed-effect-identical estimates. The 0.15 cutoff equals the MDD, so a true d of 0.15 is killed about 50% of the time. Disclose this, but do not change the approved criterion.

8. **Fixtures.** Calibration claims must use means over fixed seeds, because the per-seed control maximum reaches 2.1–2.6. Detection must use a white or low-AR background with recursive injection. Time reversal is exact only at aligned T.

## 3. Caveats

- All probes are synthetic. The generators (shared driver, HRF gamma, AR) are stylised. Gradient shares 0.16–0.76 cover the survey's real range of 0.08–0.47, but realism is unproven.
- The curl-only results come from 4 seeds each with large sd. "Removes most of the bias" is qualitative.
- The N=5 and N=6 irreducibility results do not prove anything about N=304. That large-N agreement covers 2 synthetic graphs only.
- Jump-chain bias (Logic item 2) was not probed.
- The d/p simulation uses one site-confounding strength and a Gaussian endpoint. Real Z may be heavy-tailed: a rank-based or robust sensitivity analysis is advisable but was not probed.
- The drift probe's planted cycles were feed-forward and weak. Only corrF and Jaccard are interpretable.
- Provenance disclosures:
  - probe_mixing_large.py was edited in place after its first run. probe_mixing_large_v1_reconstructed.py is RECONSTRUCTED from tool input by reverse sed and is not the observed bytes. The first-run output is probe_mixing_large_degenerate_regime.out.json, renamed from probe_mixing_large.out.json.
  - probe_injection_curl.py and probe_threshold.py were each rewritten once before their first execution. The earlier versions never ran.
  - probe_core.py was appended to (`_null_chain3`, `synth_subject`) before any probe that uses them ran.
- I did not re-verify the survey data facts listed above.

## 4. Conclusion — worker strategy by Feature Inventory row and acceptance item

Package src/topic1_lagmotif/ with modules: `loader.py`, `preprocess.py`, `flow.py`, `null.py`, `census.py`, `hodge.py`, `pipeline.py`. Add `__init__.py`, and give `pipeline.py` a `PARAMS` dict that the card cites by sha256.

**FI1 loader (A1).**
- Index the subjects as `sorted(os.listdir(npy_dir))`. Positional index i is equal to the mmap row (survey).
- `load(i)` uses `np.load(path, mmap_mode='r')`, then `.astype(float64)`, then drops the lead-in.
  - Recommend the lead-in in seconds: 20 s, i.e. round(20/TR) samples. This differs from the cache's 20 samples. Either is acceptable if documented; record trim_s.
- Optional cache path: valid T = `mask[4,:,0].astype(bool).sum()`. Assert that the mask is a contiguous prefix and that rows past T are exactly 0.
- Return valid T, TR and duration in seconds, before and after resampling.
- A missing index or path raises `SubjectNotFound(f'positional index {i}')`. No ID or path appears in the message.
- No fallback.
- Fixture: monkeypatch a temporary npy dir with fake names. Assert that it raises, and that the message contains neither the fake name nor the directory.

**FI2 TR (A1).** Import `time_series_utils.repetition_time` read-only, with `sys.path` and PYTHONDONTWRITEBYTECODE=1, or copy the table with a citation. Pin the 7-value cohort table in a test. The Chiba substring quirk is irrelevant because those sites are absent (survey).

**FI3 detrend and high-pass (A1 docs).** Order, per subject on the valid portion:
1. Linear detrend per ROI at native TR, which also demeans.
2. `resample_poly(up, down, padtype='line')` to dt = 2.0 s.
3. DCT high-pass, 128 s cutoff, by least-squares regression on the 2 s grid: k = floor(2·T·dt/128) + 1 basis vectors including the constant.
4. Z-score per ROI.
- Document the reasons: P2 edge spikes (110 SD); P2b ranking; no filtfilt transient.
- Sensitivity option: none or linear-only.

**FI4 lag-in-seconds flow (A1).**
- Exact ratios from Fraction(TR/2): 7/20, 2/5, 17/40, 1/2, 173/200, 9/10, 1/1. lag = 1 sample = 2 s.
- F = C − Cᵀ, where C_ij = Σ_t z_i[t]·z_j[t+1] / (T−1). The diagonal is 0. All 304 ROIs.
- Fixture "two-TR": generate one continuous signal at 0.1 s with a 2 s lead, sample it at TR 0.7 and 2.0, and run the chain. Assert sign agreement ≥0.95 AND |F|(0.7)/|F|(2.0) in [0.85, 1.15]. The survey reported 1.021 with resampling vs 0.409 for v1 lag-in-samples. Only the ratio catches the defect.

**FI5 threshold (A1).**
- Use `argpartition` on |F_upper| to get exactly m = round(0.15·N(N−1)/2) pairs; for N=304 that is 6,908 (the v1 percentile rule gave 6,909; either is fine if fixed and documented). Orient each pair by sign(F).
- Assert A·Aᵀ = 0, trace 0, sum = m.
- 15% is primary; 10% and 20% are pre-registered sensitivity (P3).

**FI6 null (A1, A2).**
- numba lazy chain counted by attempts. The 2-swap rejects a new edge that exists in either direction, requires 4 distinct nodes, and allows no self-loop. Add 3-edge target rotation with p_rot = 0.2. Its rejections: self-loop; new edge present in either direction among the remaining edges; duplicates or a mutual pair among the new edges. Reference implementation: verification/explorer_r1_2/probe_core.py `_null_chain3`.
- Factor 20 attempts per edge; K = 1000.
- Seeds: SeedSequence([base, subject_pos, channel_idx, variant_idx]).spawn(K).
- Assert per null: in/out degrees identical, A·Aᵀ = 0, trace 0. The cost is negligible.
- Document: "irreducibility not proven: small-N counts …; empirical agreement at N=304".
- Fixture "move-set agreement": at N=60, the null mean of 030C and 030T under 2-swap vs 2-swap+rot must agree within 4 MC SE (K=300).

**FI7 census (A1).**
- Closed form, with `nx.triadic_census` as the oracle in tests, on random oriented graphs (N=30, 5 seeds).
- Z and SP over the 5 classes {021D, 021U, 021C, 030T, 030C}. Assert the identities Z021D = Z021U = −Z030T exactly (≤1e-9).
- Document the rank-2 result and that the 8 mutual classes are structurally 0.
- Handle a null sd of 0 explicitly (return NaN and flag it); never divide silently.

**FI8 Hodge (now required, not optional).**
- p = F.mean(axis=0); G = p[None, :] − p[:, None]; gradient share = ‖G‖²/‖F‖²; F_curl = F − G. Run the same threshold, null and census on F_curl.
- Fixture: an exact gradient F = p_j − p_i (plus 1e-6 noise) gives gradient share > 0.999, and raw 030C = 0 on the thresholded graph.
- Fixture: planted cycles survive curl-only (injected mean ≥5 over seeds).

**FI9 fixtures (A2).** Each fixture targets one defect; the expected failure is in brackets.
- **(a) Null invariants and the identity.** [Fails on the v1 swap.]
- **(b) No-injection calibration.** White N=60, T=200, 8 fixed seeds: |mean Z030C| < 0.75 and |mean contrast| < 1.0. Heterogeneous AR, φ~U(0.1,0.9), N=60, T=150, 20 seeds: |mean Z030C| < 0.75 and fraction |Z| > 1.96 ≤ 0.15. [Fails on the v1 null: +2.47 per survey.]
- **(c) Detection.** Recursive injection g=0.8, 20 disjoint cycles, N=60, T=200, white, 8 fixed seeds, K=200: min(injected) > max(control) + 1.0, and mean(injected) > 5. Observed: 3.84 vs 2.13, mean 8.69. Re-verify on the worker's exact seeds. [Fails if the census or threshold breaks orientation.]
- **(d) Padding.** Pass the padded array through the loader's own valid-T inference (cache-style mask channel, or explicit valid_T metadata), never a test-supplied slice. Assert F is exactly equal (atol 1e-12) to the unpadded F. [Fails on v1: max dF 6e-3.]
- **(e) Two-TR ratio.** As in FI4.
- **(f) Time reversal through the full chain.** Exact (atol 1e-9) at TR 2.0 with any T, and at fast TRs with aligned T: TR 0.7, T=201; TR 0.85, T=401; TR 1.73, T=201. Document that production data are not grid-aligned, so the production reversal asymmetry is about 0.02–0.07 in max|F+Frev|. Do NOT trim production data to align. [Fails if any stage breaks reversal symmetry, e.g. a causal filter.]
- **(g) Missing-subject error.** No ID in the message.
- **(h) Spurious direction.** Write the quantities to results/topic1/2026-10-30/spurious_bias.json.
  - AR-φ mismatch: controlled; reuse (b).
  - Shared driver, equal HRF, N=304, shared 0.6, 4 fixed seeds, K=100: assert raw mean contrast < −2 (bias quantified, a documented limitation). Assert curl-only |mean contrast| < raw |mean contrast| / 2.
  - HRF peak spread 4–6 s with no neural delay: record the pairwise fraction where the later-peak ROI appears as the receiver. Survey: 0.84 at 0.5 s, 0.93 at 1 s.
  - Runtime about 10–20 s; mark it slow if needed. Keep the seeds fixed, because these thresholds are calibrated on means.

**FI10 (A5).**
- Old suite by explicit list: `STRICT_E2E=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` → 86 passed.
- New suite separately.
- Run `sha256sum -c sentinel/PROTECTED_HASHES.txt`.
- Use PYTHONDONTWRITEBYTECODE=1. Note: src/__pycache__ and tests/__pycache__ already exist; do not delete them, they are not this run's.

**FI11 timing (A3).**
- scripts/topic1_timing.py, with threads pinned to 1 before the numpy import.
- 5 positional indices chosen by a stated rule that spans TR groups, e.g. the first index in sorted order whose site TR ∈ {0.7, 0.85, 1.0, 1.8, 2.0}. Choosing from metadata is fine; log positional indices only.
- Per stage: load, preprocess, flow, threshold, nulls ×K for both raw and curl, census. Also numba compile time separately; peak RSS (psutil); factor 20 vs 50 Z difference; MC-SD of Z by split-half nulls (K=500 vs 500); per-subject Z030C/Z030T/gradient share/valid T/m.
- Positional indices only; no group statistics, no diagnosis labels.
- CPU-h extrapolation for 1 and 5 channels × {raw, curl}, labelled 추정. Prior estimate (추정, synthetic): about 6.5 s per subject-channel-variant, i.e. about 3.1 CPU-h per variant.

**FI12 card (A4)** — additions to the survey list:
- **Primary model:** MixedLM with site random intercept + dx + site-mean(dx) (Mundlak) + age + sex + valid duration (s). Report the fixed-effects (OLS site FE) estimate as an identical-check.
- **d definition:** d = β_dx / SD_pooled-within-diagnosis of the unadjusted endpoint. This is conservative; the residual-SD version is secondary. State the choice explicitly, because a TR or site variance component makes the residual-SD d larger.
- **p definition:** two-sided Wald p from that model, confirmed by within-site label permutation (B = 10,000; about 7 s at the FWL speed measured).
- **Holm:** across the 2 primaries (Z030C and Z030C−Z030T), raw broadband, 15%.
- **Kill rule (approved criterion, made precise):** an endpoint is "killed" if |d| < 0.15 OR Holm-adjusted p ≥ 0.05. The hypothesis is rejected if both primaries are killed.
- **Operating characteristics to disclose:** MDD 0.149 at 80% power and α=0.025; at true d = 0.15 the point estimate falls below 0.15 about 50% of the time.
- **Pre-registered sensitivity analyses:** curl-only endpoints; gradient-share covariate; densities 10% and 20%; detrend none or linear; common 200 s truncation; factor 50.
- **Interpretation rule:** if the raw primary passes but curl-only does not, the result is attributed to a gradient or latency/shared-signal effect and not to cyclic motifs.
- **Forbidden:** the naive pooled d, and ComBat without train-only fitting.
- **Disclose:** prior exposure to v1 d=0.08. MC-noise attenuation from the A3 measurement.

**FI13 open issues (A6).** Survey list plus:
- Shared-signal gradient bias.
- Curl-only noise.
- Irreducibility not proven.
- Jump-chain bias in v1 (counting accepted swaps).
- Production time-reversal asymmetry at unaligned T.
- Lead-in trim convention (20 samples vs seconds).
- GSR status of the npy unknown, which matters for the shared-signal bias.

## 5. Verification Method

- Re-run any probe: `cd /home/juke/git/00IITP-AI/verification/explorer_r1_2 && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 <probe>.py`, then compare with `<probe>.log` / `.out.json`. Hashes: `sha256sum -c SHA256SUMS.txt`. SHA256SUMS.txt was regenerated at the end and includes the reconstructed file.
- Key claims and the probe that tests each:
  - Irreducibility: probe_irreducibility_small.py and _3swap.py, about 3–20 min.
  - Shared-signal bias: probe_shared_signal.py.
  - Aligned-T reversal: probe_time_reversal_aligned.py.
  - Edge spikes: probe_detrend_resample.py, part a.
  - d/p: probe_stats_dp.py.
- Invalidation conditions:
  - Real-data gradient share or between-subject Z SD in A3 falls far outside the synthetic ranges.
  - The worker's fixture seeds do not reproduce the margins: recalibrate on means, never loosen silently.
  - A label table for the ROIs appears: then CSTC can be revisited.
- Safety: `cd /home/juke/git/00IITP-AI && sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` gave rc=0.
