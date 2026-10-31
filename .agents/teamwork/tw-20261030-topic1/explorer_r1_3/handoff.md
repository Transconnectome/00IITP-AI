# handoff — explorer_r1_3 (M1 strategy), Hard handoff, 2026-10-30T11:55Z

**Summary.** The survey architecture holds. Synthetic probes change five worker-facing specs:
1. Count chain ATTEMPTS, not accepted swaps.
2. Use Q=10 restarts, not Q=1.
3. Demean or detrend BEFORE resample_poly.
4. Never use raw pooled d with Welch p for the kill gate. Use the site-adjusted β/SD with a within-site permutation p.
5. Curl-only has no power. Gradient share is the needed nuisance covariate, and it does not remove a latency-spread confound.

All probes are synthetic except one aggregate read of the metadata table. No imaging data were read, and no IDs were printed or written.

## 1. Observation

Probe directory: `/home/juke/git/00IITP-AI/verification/explorer_r1_3/`. Each probe has a `.py`, a `.log` and, where relevant, `.out.json`. Failed attempts are preserved in `failed_v1/` and `failed_v2/`.

| # | Probe | Key raw result (verbatim numbers) |
|---|---|---|
| O1 | probe_irreducibility_exhaustive (N=4,5 all oriented graphs) | N=5: 12382 degree classes (size ≥2). 2-swap-only reducible in 7862; +3-cycle reversal 1146; +4-cycle reversal 1096. N=4 example out=[1,1,0,1], in=[1,1,1,0] stays 2 components under all three move sets. Accepted-swap (jump-chain) weighting shifts E[030C] by mean 0.23 (max 0.36) class-SD in 460 small classes. |
| O2 | probe_irreducibility_size_trend | Mass outside the largest swap+tri component: N=5 size 2–9 0.041, size 10–99 0.024. N=6 (sampled): size 10–99 0/71 reducible; size 100–999 1/10 reducible, mass 0.001. |
| O3 | probe_null_mixing_n304 (N=304, exact 15% → m=6908, structured synthetic graph) | Null mean 030C, 2swap attempts: Q=1 1632.4; Q=3 1614.1; Q=10 1613.1; Q=30 1613.2; Q=100 1612.1 (null sd ≈45). Long-chain reference 1614.5. So Z030C is 2.35 at Q=1 vs 2.77–2.90 at Q≥10. Accepted-counted means: 1619.9 / 1619.0 / 1622.6 / 1617.0 / 1615.4. +tri (p=0.1): 1628.8 / 1613.9 / 1608.0 / 1622.6 / 1613.5; long chain 1616.2. Z021D+Z030T ≈ 1e-14 in every setting. Cost per null (incl. census): 1.8 ms at Q=1, 3.7 ms at Q=10, 18.9 ms at Q=100. MC SD of Z030C vs n (subsampled from 2000): 50→0.349, 100→0.193, 200→0.141, 500→0.084, 1000→0.050. Contrast: 0.503 / 0.302 / 0.200 / 0.097 / 0.059. Between-subject SD under the same generator: Z030C 1.01, contrast 1.68. |
| O4 | probe_uniformity_fixture + _thinned | F1, N=4 class 3-cycle + isolated node (2 states): swap-only visits 1 state in 20000 steps; swap+tri visits both (0.479/0.521). F2, N=5 class of 7 states (move-degree max/min 4.0), thinned every 25 steps, 4000 samples: attempts-counted χ² p=0.548, freq max/min 1.10. Accepted-counted p=1.3e-210, max/min 4.16. |
| O5 | probe_detrend_highpass part A (raw scale mean 1.15e4, TR 0.7→2.0) | resample_poly with default zero padding on raw-scale data: edge deviation 173.6 SD, interior 10.7 SD. Demeaned 2.5/4.2; linear-detrended 1.66/3.53; padtype='line' 2.14/3.49. The last three are indistinguishable (≈ max of about 24 Gaussian draws). |
| O6 | probe_detrend_highpass part B (N=120, drift at 10% of power, 2 s grid) | Share of F variance explained by drift-only F: none 0.004, linear 0.002–0.003, DCT 0.01 Hz 0.000, Butterworth 0.000 (T=100 and T=250). No-coupling Z030C mean −0.4…+0.3, SD 1.52–1.88 under every option. Planted-cycle power was too weak to rank the options (0.3–0.9). |
| O7 | probe_spurious_latency_curl (N=120, T=150, global source a=0.8 seen with per-ROI latency) | No coupling, raw Z030C by latency SD: 0→−0.14±1.35; 0.25→−0.33±1.26; 0.5→−0.52±1.77; 1.0→−1.72±0.53. Curl-only stays 0.11/0.04/−0.00/0.06. Gradient share 0.337 at latency 0 with a=0.8, vs 0.016 with a=0 (no global). 30 planted cycles, no latency: raw 1.57±0.80, curl 0.11±1.09. AR φ U(0.1,0.9) vs φ=0.4, no global: Z030C 0.34±1.37 vs 0.02±1.22. |
| O8 | probe_curl_diag / diag2 | Planted-edge recall: raw 0.69, curl 0.849 (a=0.8). Curl-graph 030C ≈ 285–303 with null SD ≈ 15, and planted cycles do not raise it (303/287/285 with vs 287/297/286 without). Raw-graph 030C is 22–65 with null SD 5–7. The printed `sd(kout-kin)` values are uint8 underflow garbage; ignore them. |
| O9 | probe_group_bias_n200 (200/group, SE≈0.10, no neural difference) | (A) latency SD 0.5 vs 0.6 s: d Z030C −0.222, Z030T +0.140, contrast −0.212, grad share +0.224, Z030C after grad-share adjustment −0.168. (B) global amp 0.8 vs 1.0: d Z030C −0.197, Z030T +0.455, contrast −0.412, grad share +1.399, Z030C adjusted +0.015. |
| O10 | probe_threshold_density (N=120, 10 seeds) | Latency 1 s raw Z030C: 5% −0.40±0.54; 10% −0.59; 15% −1.16; 20% −1.18; 30% −2.37. Planted 30 cycles: 2.88 / 1.78 / 0.90 / 1.09 / 1.59. No coupling: −0.62±0.23 / −0.93 / −0.92±0.99 / −1.04 / −0.19±1.49. Z scale differs by density, so these are not comparable across densities. |
| O11 | probe_d_p_calibration (real site×dx of 1,706 on-disk subjects + real age/sex in memory; outcome simulated; 400 reps) | H0, ICC 0.1 random site effects: Welch-on-raw rejects 0.100, site-FE OLS 0.0625, within-site perm 0.0575. ICC 0.3 random: 0.2175 / 0.0475 / 0.0475. Site effect aligned with site OCD fraction, ICC 0.1: 0.6525 / 0.05 / 0.05; ICC 0.3: 0.9825 / 0.055 / 0.0575. Under that last H0, raw d mean 0.199 and P(\|d_raw\|≥0.15)=0.865, vs adjusted 0.003. True d=0.15: d_adj mean ≈0.15, P(\|d_adj\|≥0.15) 0.48–0.53. MixedLM H0 (ICC 0.3 confounded, 60 reps): reject 0.05; mean \|β_LMM−β_FE\| 0.0064. n=1706, OCD 869, 23 sites, site OCD fraction 0.18–0.82, SE(d)≈0.0484, d at p=.05 ≈0.095. |
| O12 | enigma time_series_utils.py:1-2 | Imports only scipy.signal and numpy. Lines 5-70: ordered substring `if/elif`. Importing it from pytest without `dont_write_bytecode` would write `__pycache__` into the read-only repo. |
| O13 | Protected hashes | `sha256sum -c sentinel/PROTECTED_HASHES.txt` gave all 44 lines 성공 (OK) at 11:32Z (start). The rerun at the end is in §5. |

## 2. Logic chain → worker spec per Feature Inventory row and ACCEPTANCE item

**Row 1 Loader (A1).**
- Primary source is the npy directory. Use `sorted(os.listdir(npy_dir))` positional index `pos` as the only identifier exposed. Survey: this equals the mmap row order.
- Map pos → Unique_ID → Sample through the metadata CSV in memory. Drop ID columns immediately (pattern in probe_d_p_calibration.py `load_design`).
- Read with `np.load(path, mmap_mode='r')`, then `np.array(..., dtype=float64)`.
- Validity rules:
  - Raise `MissingSubjectError(f"positional index {pos}: file missing")`. The message must contain no path or ID.
  - Strip trailing all-zero rows. Raise if any all-zero row, NaN or inf remains in the interior, or if any ROI has zero variance.
  - Head trim is fixed in seconds: `ceil(t_trim_s/TR)` samples, with `t_trim_s` frozen in the card. Suggested 40 s, which equals the MBBN 20-sample convention at TR 2.0 (1,195 subjects).
- Return a dataclass `(X_valid, tr, site, valid_T, duration_s, pos)`.
- The cache path is optional and exploratory only: valid_T = `mask[:,0].sum()`, then slice before anything else.
- No fallback anywhere.

**Row 2 TR.**
- Use a cited constant dict for the 23 on-disk sites, matched by EXACT string, not substring.
- A test asserts equality with `repetition_time()`. The test sets `sys.dont_write_bytecode = True` before an importlib file-path load (O12). This keeps the enigma repo unchanged even if PYTHONDONTWRITEBYTECODE is unset.
- Unknown site raises.

**Row 3 Detrend / high-pass.**
- Primary: per-ROI `scipy.signal.detrend(type='linear')` at native TR, BEFORE resampling. This is mandatory because zero-padded resample_poly on raw scale gives a 173 SD edge artefact (O5). Drift explains under 0.5% of F variance (O6), so the high-pass choice is low-stakes.
- Pre-registered sensitivity: DCT high-pass at 0.01 Hz by regression (K = floor(2·T·dt·fc)) on the 2 s grid.
- Claim no superiority between DCT and Butterworth (O6 power too weak).

**Row 4 Resample + lag.**
- `Fraction(str(TR))/2` gives up/down (7/20, 2/5, 17/40, 1/2, 173/200, 9/10, 1/1). Skip resampling at TR 2.0.
- Lag: k = lag_s/2.0; assert it is an integer (k=1).
- Z-score over the full valid resampled series, then compute `C = Z[:-k].T@Z[k:]/(T-k)`, `F = C - C.T`, diag 0. Use all 304 ROIs.

**Row 5 Threshold.**
- Exact top-m: m = round(0.15·N(N−1)/2) = 6908 for N=304, via `np.argpartition` on |F| in the upper triangle. The edge direction is sign(F). Reference: r13lib.thr_exact.
- The percentile rule gave 6909 in the survey. Exact-m guarantees an identical m and is immune to ties.
- Assert m is identical for all subjects.
- Primary density 15% (continuity with v1). Pre-registered sensitivities 10% and 20%.
- Density changes both power and latency bias (O10), and the Z scale differs by density, so Z must never be compared or pooled across densities.

**Row 6 Null.**
- Numba kernel as in r13lib._chain. Use an edge-index matrix so triangle reversal can update the edge list.
- Rules:
  - 2-swap with 4 distinct nodes. Reject a new edge that already exists in EITHER direction.
  - Directed 3-cycle reversal, with proposal probability p_tri=0.1 (edge × uniform node).
  - Count ATTEMPTS, not accepted moves. Accepted counting is non-uniform (O1, O4 F2) and the survey prototype counts accepted moves.
- Use independent restarts from the real graph with Q=10·m attempts. Q=1 is biased by 0.4 null-SD (O3).
- Run A3 again at Q=10 vs Q=30 on the 5 real subjects.
- Seeds: `SeedSequence(card_seed, spawn_key=(pos, channel_id)).generate_state(n_null)`.
- Per-null assertions in int64 (in/out degrees equal, `(A&A.T).sum()==0`, `trace==0`, `A.sum()==m`) run on EVERY null; the cost is negligible.
- Document: "uniform on the component reachable from the observed graph; irreducibility of these moves on oriented graphs is not established." Evidence: O1/O2 counts. No literature was verified.

**Null count.**
- MC SD of Z ≈ sqrt((1+Z²/2)/n). This matches O3 after a finite-population correction.
- Use a rule, not a number: choose n_null so that the MC SD is at most 0.1 × the between-subject SD of the endpoint, using real |Z| measured on the 5 A3 subjects. Default 1000. For |Z|≈7.9, n=1000 gives 0.18, so 2000–5000 may be needed.
- Cost is about 3.7 ms per null at Q=10 (synthetic; A3 must re-measure).

**Row 7 Census / Z / SP.**
- Closed-form 5-class census (r13lib.census5); `nx.triadic_census` is the test oracle.
- Z = (obs − mean)/sd(ddof=1). If sd=0, return NaN with a flag.
- SP over the 5 oriented classes, with documented identities Z021D = Z021U = −Z030T and 021C determined by the other two.
- Endpoints: E1 = Z030C, E2 = Z030C − Z030T.

**Row 8 Hodge.**
- Gradient share = ‖G‖²/‖F‖², with G_ij = p_i − p_j and p = row mean of F. Make it a MANDATORY per-subject output and covariate.
- It is also produced by global signal × finite sample with zero latency (O7: 0.337 vs 0.016). GSR status of the npy files is unknown, so this goes in the open issues.
- Dissent from PROJECT row 8 framing: compute curl-only as descriptive only and label it low-powered. Planted cycles were not detected (O7, O8), so a null curl-only result cannot be read as "artefact".
- Suggested mechanism, an unverified hypothesis: under fixed density the planted edges displace cycle-rich background edges.

**Row 9 Fixtures (A2).** Each fixture should fail on its target defect. Named failure-on-defect evidence:
- (a) Null invariants on every null. v1 swap gave 250+ reciprocal pairs (survey).
- (b) Z021D + Z030T == 0 to 1e-9. v1 gave 5.4 (survey). O3 gives about 1e-14.
- (c) F1: triangle reversal must visit both states of the 3-cycle+isolated-node class. Swap-only visits 1 (O4).
- (d) F2: thinned visit frequencies on the 7-state N=5 class must pass χ² p>0.01 when counting attempts. Accepted counting gives p=1e-210 (O4). Use a fixed seed and record the class.
- (e) Injection: use the survey design, N=60, ≥20 disjoint lag-1 cycles, NO global signal (survey: Z mean 8.3, min 4.4 vs control max 0.99). Adding global a=0.8 cut recall 0.86→0.69 (diag).
- (f) No-injection calibration averages over ≥16 seeds. Assert |mean Z030C| < 3·SD/√n_seeds with SD≈1.5 (O6/O7 overdispersion). Never assert per-subject |Z| < 1.96.
- (g) Padding: assert exact equality of F (atol 1e-12) between X and vstack(X, zeros). Also F(X + 1.15e4) == F(X) and F(X + linear trend) ≈ F(X). These fail if detrending happens after resampling (O5).
- (h) Two-TR: one continuous signal sampled at 0.7 and 2.0 s. Assert the |F| ratio is in [0.85, 1.15] (survey: v1 0.409, v2 1.021) and sign agreement ≥ 0.9.
- (i) Time reversal through the full chain: at TR 2.0 assert F_rev == −F exactly. At TR 0.7 assert corr(F_rev, −F) > 0.99, because polyphase alignment is not exact.
- (j) Missing subject: raises, and the message contains no ID or path.
- (k) Spurious direction, quantification and test:
  - AR φ heterogeneity, no global: mean Z030C ≈ 0 within tolerance (controlled in mean, overdispersed).
  - Latency-only with global signal: assert raw Z030C mean < −1 at latency SD 1 s (bias exists, direction known).
  - Write the magnitudes to results JSON, and cite O9 (d −0.22 latency, −0.20 global; adjustment fixes global only) as the open limitation.
  - Keep the survey 2-ROI HRF-delay numbers (frac a→b 0.84 at 0.5 s).

**Row 10 Old tests.** Run tests/test_empirical_four_topics.py, tests/test_pilot_connectome.py and tests/e2e separately from the new suite (86 expected), and run `sha256sum -c`.

**Row 11 Timing (A3).**
- 5 subjects chosen by a stated rule spanning TRs: positional indices, one per TR group from {0.7, 0.85, 1.0, 1.8, 2.0}.
- Pin BLAS threads to 1. Record per-stage wall time (load, detrend, resample, flow, threshold, nulls, census), numba compile time separately, peak RSS (resource.getrusage), n_null, Q, and acceptance rate.
- Compare Q=10 vs 30 on the same subjects. Measure real |Z| to apply the n_null rule.
- Extrapolate CPU-h for 1706 × channels, labelled 추정.
- Log positional indices only.

**Row 12 Card (A4).** Definitions this explorer recommends freezing:
- **d** = β̂_dx (OCD − HC) from OLS with site fixed effects + age + sex + valid duration (s), divided by the pooled within-group SD of the raw endpoint.
  - State it explicitly. Total vs within-site SD changes d by 1/√(1−ICC).
  - The same β from statsmodels MixedLM (REML, site random intercept) is reported. β_LMM ≈ β_FE (O11).
- **p** = two-sided within-site label-permutation p of the FE t (B=10,000, seed in card). Equivalently the LMM Wald p as a secondary; both are calibrated in O11.
- Holm across E1 and E2.
- **Kill:** an endpoint passes only if |d| ≥ 0.15 AND p_Holm < 0.05. Topic 1 is killed if neither passes.
  - Disclose that |d| ≥ 0.15 is the binding condition (p=.05 ↔ d≈0.095).
  - Disclose that a true d=0.15 is killed about 50% of the time (O11).
- **Raw Cohen's d and Welch p are descriptive only.** Under site-confounded H0 they would reject 65–98% of the time and would pass the gate 87% (O11).
- **Mandatory sensitivity models:** + gradient share; DCT high-pass; densities 10%/20%; common 200 s truncation. Curl-only is descriptive.
- **Interpretation rule:** an effect that falls below |d|<0.15 after gradient-share adjustment is "not separable from hemodynamic/global nuisance". Latency-spread confounding survives adjustment (O9 A: −0.17), so a passing result still carries that stated limitation.
- **Per-subject Z** is not a calibrated z-score (no-coupling SD 1.2–1.9).
- **Classification:** LOSO across 23 sites with features [Z030C, Z030T] (rank 2); scaler fit on training folds; in-house static-FC baseline on identical folds.
- Plus the survey items (population, baselines, medication, sex, FD, CSTC, prior exposure).

**Row 13 Open issues (A6).** Add to the survey list:
- Global-signal/GSR status unknown; it drives gradient share.
- Latency-spread confound not removable (O9).
- Per-subject Z overdispersion.
- Irreducibility not established.
- Survey prototype counted accepted swaps.
- resample_poly zero-pad hazard.
- Density sensitivity of bias and power.
- Curl-only low power.
- Substring-order bug in repetition_time (Chiba; does not affect on-disk sites).

**A5.** The probes wrote only under verification/explorer_r1_3 and in this metadata directory. No __pycache__ was found in the probe directory.

## 3. Caveats
- Every Z-, bias- and power-related number is from synthetic generators of my own design: N=120 or 304, AR noise, a single global source with latency, lag-1 planted cycles. Real-data magnitudes may differ. The A3 subjects should be used to calibrate n_null and Q.
- O10 density results come from N=120 with Z scales that are not comparable across densities. They show that density matters, not which density is better.
- The no-coupling bias level at latency 0 is unstable across seed sets (−0.14 vs −0.92, n=10 each). Do not cite a bias level for it; cite only the latency-1 s value (−1.72±0.53) and the O9 group d values.
- Irreducibility evidence is exhaustive only for N≤6 (N=6 sampled). Behaviour at N=304 is inferred from the size trend plus the agreement between restart and long-chain means (O3). It is not proven.
- The accepted-vs-attempts difference at N=304 was only suggestive in O3 (about +5 in mean, under 0.15 SD). The correction is justified by exactness (O4), not by the size of the effect.
- In O11 the outcome is simulated. Only the site×dx structure, age and sex are real (metadata, in memory, aggregate output only).
- I did not re-verify the survey's real-data facts (npy shapes, TR edge, baselines), and I read no imaging data.
- Manifest hygiene: `failed_v1/SHA256SUMS` was generated by a glob that included itself (an empty-file hash line), and it was later regenerated. `failed_v1/SHA256SUMS.v2` lists the four preserved files correctly.
- `failed_v1/` holds the first failures of two probes: the detrend `ptp` crash and the d/p syntax error. `failed_v2/` holds the d/p broadcasting failure.

## 4. Conclusion
The survey architecture is correct. The worker should implement it with the specific corrections in §2:
1. Count attempts, with Q=10 restarts and p_tri=0.1.
2. Use the n_null rule.
3. Detrend before resample.
4. Use exact top-m.
5. Make gradient share mandatory.
6. Treat curl-only as descriptive.

The card must define d and p as site-adjusted β/SD with a within-site permutation p and Holm across 2 endpoints. Raw d must be banned from the gate. The card must disclose the 50% kill probability at true d=0.15 and the latency-spread confound magnitude (d≈−0.2 without any neural difference, and only partly removed by adjustment). That confound is the largest scientific risk to interpreting a Topic 1 result, and it belongs in the A6 open issues.

## 5. Verification Method
- Re-run any probe: `cd /home/juke/git/00IITP-AI/verification/explorer_r1_3 && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 <probe>.py`. Use `-I` for probe_d_p_calibration.py. All are seeded.
- Runtimes: under 60 s each, except about 50 s for group_bias_n200 and about 30 s for null_mixing_n304.
- Invalidation conditions:
  - The worker's real-data A3 shows Q=10 vs Q=30 Z differences > 0.1·SD_between → raise Q.
  - Real |Z| makes the MC SD exceed 0.1·SD_between at n=1000 → raise n_null.
  - Any null fails the int64 invariant asserts.
- Protected-file check: `cd /home/juke/git/00IITP-AI && sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt`. Final run result: see progress.md.
