# handoff — challenger_r1_1 (Hard handoff, M1 empirical challenge)

All probes: /home/juke/git/00IITP-AI/verification/challenger_r1_1/probes/ ; logs: /home/juke/git/00IITP-AI/verification/challenger_r1_1/logs_*.txt ;
mutants: /home/juke/git/00IITP-AI/verification/challenger_r1_1/mut/<name>/ (each has pytest_out.txt) ; timing rerun: /home/juke/git/00IITP-AI/verification/challenger_r1_1/timing/

## 1. Observation
- Hygiene: protected hashes 44/44 OK before and after; the 26 production files (src/topic1_lagmotif, tests/topic1_lagmotif, scripts/topic1_timing.py, results/topic1/2026-10-30, docs/03_empirical_analysis/topic1) are byte-identical before and after (prod_hashes_before.txt, `sha256sum -c` 0 failures). No new .pyc in enigma; no __pycache__ in the new dirs. A participant-ID scan of the 643 files I wrote found 0 hits.
- Suites (my run): new 29 passed in 3.71 s; old 86 passed, 7 warnings in 72.15 s.
- Provenance: params_sha256() = 86863ffa…5c6 (matches). Card sha256 = 1e589f0b…aa (matches). Card §12 code hashes all pass `sha256sum -c`. Baselines checked against enigma files (read-only): table1 condition=baseline has 26 test_AUROC values, 0.6512 ± 0.0318 (4 rows missing); site_driver_analysis.csv auroc_scratch_mean over 23 sites has mean 0.6519 and median 0.6707. Both match the card.
- P1 (logs_p1.txt): closed-form census = networkx triadic_census = my own brute-force classifier on 11 adversarial or random oriented graphs (empty, tournament, transitive tournament, out-star, single cycle, random N 5–40). census() rejects mutual edges and self-loops. Production path `null_counts` (_null_ensemble/_count_030), compared per null with networkx or matrix census of `sample_null_graph` (same seeds), at N=60 and N=304 for d 0.05/0.10/0.15: 0 count mismatches and 0 invariant violations (my own checker: mutual, self-loop, kin, kout, binary, m), and every null moved.
- P2/P2b (logs_p2.txt, logs_p2b.txt): attempts sweep at N=304 over 5–400·m (P2) and 2–500·m (P2b):
  - At acceptance 0.24–0.88, null means and SDs are stable; Hamming saturates by 5·m.
  - At acceptance 0.04–0.07 (near-potential flow), Z030T drifts 1.10 → 1.78 → 2.12 → 1.99 (2·m → 20·m → 100·m → 500·m; d=0.15). That is about 0.3 Z, or about 0.1 null SD of the mean; Hamming at 20·m reaches about 93% of its saturation.
  - Near-potential graphs give 030C null SD = 0 even at 500·m while about 1,100 edges moved. This looks structural (an acyclic-forcing degree class), but it is not proven.
- P3 (logs_p3.txt): the cache .subjects.txt order equals sorted(listdir) (n=1706, booleans only). Simulating removal of one directory silently remaps position 57 to another subject; nothing pins a manifest at load time.
- P4 mutation (logs_p4.txt, logs_p4_extra.txt, mut_failed_tests.txt): control copy 29/29 passed; the isolation guard was proven active; there were no collection errors.
  - KILLED (24):
    - null: no reverse check (8 failed), no self-loop check (9), no reverse check + checker off (3), degree-breaking move (8), asymmetric rotation i<j<k (2), p_rot ignored (1), all nulls one seed (5), no null moves (8);
    - loader and preprocessing: no trailing-zero strip (2), resample_ratio→(1,1) (3), causal filter added (2), no detrend (1), no head trim (1), interior zero allowed (1), missing subject → synthetic fallback (1);
    - flow and graph: C transposed (2), top-k orientation flipped (2), top-k smallest (4), density ×0.9 (1), gradient ×0.5 (2);
    - census and statistics: census 021C missing −030T (4), Z sign flip (3), null_counts swapping 030T/030C (3);
    - TR table: Chiba fixed (2), wrong NYSPI TR (1).
  - SURVIVED (6):
    - `pipeline_no_resample_tr_ignored`: subject_flow passes grid_dt instead of series.tr to preprocess, so there is no resampling and the lag is 1 native sample (29 passed);
    - `pipeline_lag1_native_no_grid`: subject_flow = lagged_net_flow(zscore(detrend(X)), 1) (29 passed);
    - `lag_native_samples`: lag = round(lag_s/TR) grid samples (29 passed);
    - `null_021C_missing_t`: null 021C = p2 − 3c (29 passed);
    - `head_trim_in_samples`: trim computed with TR 2.0 for every site (29 passed);
    - `z_ddof0_no_nan`: Z = (obs − mean)/(sd + 1e−12) instead of NaN when SD = 0 (29 passed).
- P5 (logs_p5.txt): the production chain prepare_series → subject_flow on one continuous signal sampled at 0.7/0.8/0.85/1.0/1.73/1.8/2.0 s gives corr(F_TR, F_2.0) = 1.000, sign agreement 1.000 and |F| ratio 0.997–1.000. Trailing padding at TR 0.7 is exact; a partial-zero last row is kept. Reversal through prepare_series has corr 0.998 (not exact, because the head trim cuts the other end; this is expected).
- P6 (logs_p6.txt): planted cycles at N=304, T=150 are detected at every density. For 20 cycles, Z030C is 6.14 / 4.48 / 3.52 at 5/10/15% (control 0.34 / 0.15 / −0.21; per-seed SD about 2). At real scale, detection decreases with density (5% best), unlike the N=60 rationale.
- P7 (logs_p7.txt): 5 keys of spurious_direction.json reproduce bit-exactly (ar_mismatch, latency_sd_1s, latency_sd_1s/curl, planted_cycles_20, white_control, all @0.10).
- P8 (logs_p8.txt): white noise at N=304, T 100–600, d 5/10%, 16 seeds: every mean Z030C, Z030T and E2 lies within about 1 SE of 0, with no trend in T.
- P9 (logs_p9.txt): timing rerun on the same positions [1578, 1228, 932, 0, 57]. 0 mismatches in deterministic fields (m, acceptance, degenerate flags, |dZ| diagnostics, valid_T, n_trim). nulls_s ratio challenger/worker 1.00–1.05 (load average 10–16 on 20 cores). Summary: 12.61 vs 12.47 CPU-h (추정); 292 MB peak RSS in both runs.
- P10/P10b (logs_p10.txt, logs_p10b.txt): exhaustive uniformity on 9 N=5/6 classes; all reached (0 reducible). One class (N=5, m=8, |class|=4) failed χ² at 100·m (p=1.7e−9, the start graph over-represented 467 vs about 375). It passes at 1000·m (p=0.10) and 10000·m (p=0.92), and with p_rot=0 the chain is stuck at the start. Cause: slow mixing for transitions that only a specific 3-edge rotation reaches; the attempt probability scales about 1/m³.

## 2. Logic chain
1. P1 + P4 null mutants + P10 at long chains → census, null invariants (on the production path) and the stationary law are correct.
2. P5 → the production chain is correct for lag-in-seconds at every on-disk TR, and for padding. P7/P9 → the results are reproducible and deterministic. P8 → calibrated under no coupling at real scale.
3. P4 survivors 1–3 → A2's "fixtures … would FAIL on the defect they target" is not met for the lag-in-seconds bullet at the production entry point. The two-TR fixture calls preprocess + lagged_net_flow(·,1) directly. No fixture runs subject_flow/extract_subject at TR ≠ 2.0, so removing resampling or the seconds-to-samples conversion from pipeline.py passes all 29 tests. The worker's claim "lag counted in native samples gives an |F| ratio outside [0.85,1.15]" is a simulation inside the test, not a put-back into production code.
4. Survivors 4–6 are untested parts of frozen rules: the SP/021C null, the head trim at TR ≠ 2, and the NaN-on-degenerate Z rule the card's fallback relies on. No acceptance bullet names them, so they are lower severity.
5. P2b/P10b confirm the disclosed mixing/irreducibility limitation and bound it: about 0.3 Z drift at acceptance below 0.07 at 20·m on N=304. Not a refutation by itself.

## 3. Caveats
- Synthetic graphs only for mixing; the real low-acceptance subject (position 1578) was not swept beyond 40·m (would require feature computation on real data beyond the timing replay).
- Structural vs mixing degeneracy (030C SD 0) not proven.
- Old suite verified by me once (86 passed); I did not inspect the card's statistical plan in depth (auditor/reviewer scope).
- Machine was shared (load 10–33), timing ratios rather than absolute seconds are meaningful.

## 4. Conclusion
- The production code is correct under every probe: census, null invariants, uniformity at long chains, TR consistency, padding, reproducibility, timing.
- Blocking issue (A2 fail-on-defect): add a fixture that runs the production entry point (prepare_series → subject_flow or extract_subject) on the same continuous signal at TR 0.7 (and 1.73) vs 2.0. It should assert sign agreement and an |F| ratio within [0.85, 1.15]; it would kill the 3 surviving pipeline mutants.
- Non-blocking:
  - fixtures for the null 021C/SP;
  - prepare_series n_trim at TR ≠ 2;
  - the NaN-on-SD-0 rule;
  - a manifest (count + salted-hash digest) pinned at load time;
  - a note that at N=304 the 5% density detected planted cycles best;
  - the 20·m attempts budget is about 0.3 Z away from convergence at acceptance below 0.07; consider an acceptance-adaptive budget.

## 5. Verification method
- `cd /home/juke/git/00IITP-AI/verification/challenger_r1_1 && /home/juke/superclaude-env/bin/python3 -B probes/p4_mutants.py pipeline_no_resample_tr_ignored pipeline_lag1_native_no_grid lag_native_samples null_021C_missing_t head_trim_in_samples z_ddof0_no_nan` → all six "29 passed" until fixtures are added.
- `PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 probes/p1_census_null_equiv.py` → TOTAL_FAILS 0; `probes/p5_flow_chain.py`, `probes/p7_spurious_repro.py`, `probes/p9_timing_compare.py` (after rerunning scripts/topic1_timing.py --outdir verification/challenger_r1_1/timing).
- Invalidation: any change to src/topic1_lagmotif (card §12 hashes) requires rerunning P1, P4, P5.

## Addendum (12:36Z) — proposed fixture verified
- /home/juke/git/00IITP-AI/verification/challenger_r1_1/proposed_fixture/test_production_lag_in_seconds.py
  (prepare_series → subject_flow, TR 0.7 and 1.73 vs 2.0, sign agreement + |F| ratio ∈ [0.85,1.15]).
- logs_proposed_fixture.txt: control 2 passed; pipeline_no_resample_tr_ignored, pipeline_lag1_native_no_grid, lag_native_samples each
  1 failed (the TR 0.7 case), 1 passed (1.73 ≈ 2 s, so a native lag of 1 sample there is nearly correct).
- Null 021C formula checked on 20 null graphs: 0 mismatches (logs_021C_null.txt). The survivor is test coverage only.
- Card line 51 excludes subjects whose primary null is degenerate by "Z NaN". The NaN-on-SD-0 rule (survivor z_ddof0_no_nan)
  therefore feeds a frozen exclusion rule, but no test covers it. Non-blocking; it should be tested before step 5.
