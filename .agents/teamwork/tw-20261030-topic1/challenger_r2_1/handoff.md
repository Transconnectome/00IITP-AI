# Hard handoff — challenger_r2_1 (run tw-20261030-topic1, M1 iteration 2)

Verdict: CONFIRMED (blocking issues: none). Under every one of my independent probes the implementation was correct. I found no reproduced failure of any A1 or A2 requirement, and no wiring defect or sign defect. Five non-blocking issues are listed in §4. One of them is scientifically important and must be resolved before step 5: card §9 states the spurious-direction magnitude at N=60, and at N=304 it is about 8x larger.

## 1. Observation

All probes are under /home/juke/git/00IITP-AI/verification/challenger_r2_1/. Their hashes are in SHA256SUMS.txt there.

### 1.1 Byte binding

- I hashed 35 files at 13:2xZ (`hashes_start.txt`): src/topic1_lagmotif, tests/topic1_lagmotif, scripts/topic1_timing.py, docs/03_empirical_analysis/topic1 and results/topic1/2026-10-30.
- I re-checked them at the end: all OK, nothing changed during my run.
- Card sha256 = 1e589f0b…75aa, equal to card_sha256.txt. Card §12: 10/10 OK.
- test_production_entry_point.py is byte-identical (`cmp`) to verification/explorer_r2_3/proposed_tests/test_production_entry_point.py.
- Protected hashes: 44 OK, rc 0, at start and at end.

### 1.2 Test suites (my own runs)

- New suite: 53 passed, rc 0 (`new_suite.log`).
- Old suite: 86 passed, 7 warnings, 106.65 s, rc 0 (`old_suite.log`).

### 1.3 P1: census and null oracle against networkx (`p1.log`)

Inputs:
- 65 graphs: random oriented graphs with N from 3 to 60 and density up to 1.0, plus 5 adversarial graphs (regular tournament T7, transitive tournament, out-star, in-star, single 3-cycle).
- 7,800 null graphs at (factor, p_rot) = (20, 0.2), (5, 0.0) and (5, 1.0).

Results:
- census() vs nx.triadic_census: 0 mismatches.
- Mutual triad classes are 0 in every graph and every null.
- Each null was checked independently with networkx for in/out degree, self-loops, mutual edges and binary entries: 0 failures.
- Per-null 030T/030C from null_counts vs networkx census of sample_null_graph(seed): 0 mismatches.
- Null mean and SD (ddof=1) of all 5 classes vs motif_statistics: 0 mismatches.
- The rank-2 identity Z021D = Z021U = −Z030T held in every case.
- census() raises on a graph with a mutual edge.

### 1.4 P2/P2b: null uniformity by exhaustive enumeration (`p2.log`, `p2b.log`)

Every reachable component equalled the full degree class (21, 24 and 160 graphs).

| Graph | Attempts | χ² | df | p |
|---|---|---|---|---|
| N=5, m=6 | 20·m (frozen) | 540 | 20 | 1e-102 |
| N=5, m=6 | 200·m | 16.3 | 20 | 0.70 |
| N=5, m=6 | 2000·m | 25.8 | 20 | 0.17 |
| N=5, m=7 | 20·m (frozen) | 3240 | 23 | ≈0 |
| N=5, m=7 | 200·m | 16.1 | 23 | 0.85 |
| N=5, m=7 | 2000·m | 14.3 | 23 | 0.92 |
| N=6, two 3-cycles | 20·m (frozen) | 161.5 | 159 | 0.43 |

So the stationary distribution is uniform, as claimed, but the frozen budget under-mixes on very small graphs.

### 1.5 P3/P3b: mixing at the analysis scale (N=304, density 0.10, m=4606) (`p3.log`, `p3b.log`, JSON)

Setup: 11 synthetic regimes (white with planted cycles, AR mismatch, shared-driver latency, HRF peak delay), acceptance from 0.10 to 0.78; factors 20, 40, 80, 160, 320 and 1,280, each with independent seeds.

- **Null mean drift.** At factor 20 the null means of 030C and 030T are within ≤0.2 null SD of the factor-320 reference (P3). In P3b they also agree with factor 1,280 within MC noise. Example, hrf1.0: acceptance 0.10, m030T = 2219±18.8 at factor 20 vs 2219±15.7 at 1,280.
- **Edge overlap.** The overlap of the null graph with the observed graph already reaches its plateau at factor 20, e.g. 0.633 at 20 vs 0.631 at 1,280.
- **Monte Carlo noise at large |Z|.** With 200 nulls, Z030T for one fixed graph ranged from −72 to −91 across seed sets, and E2 from 25 to 47. Split-half |dZ030T| reached 13.9.
- **Degenerate case.** One HRF regime (gradient share 0.977, acceptance 0.029) has null SD = 0. Z comes out NaN and the degenerate flag is set. At this acceptance almost every accepted 2-swap is a no-op: the analytic no-op proposal probability is 0.016–0.026.

### 1.6 P4: full production chain on a fake npy directory (`p4.log`)

Setup: synthetic data with fake names S000–S006 and one real site string per TR (0.7, 0.8, 0.85, 1.0, 1.73, 1.8, 2.0). Each series has a 1.15e4 offset, ×50 scale and linear drift, and is zero-padded to 464 rows or by +25 rows. It goes through NpyCohort.load → subject_flow.

- **Padding.** max|ΔF| between the padded file and the unpadded series = 0.0 exactly, at all 7 TRs.
- **Lead–lag.** The sign is correct at every TR for every true lead (+1, +2, +3, +4, +6 s and −2 s). This includes the sub-grid 1 s lead.
- **Time reversal through subject_flow.**
  - TR 1.8 and 2.0: max|F_rev + F| ≤ 8e-15, so the flip is exact.
  - TR 0.7, 0.8, 0.85, 1.0 and 1.73: corr(F_rev, −F) ≥ 0.99981, max|F_rev + F| ≤ 0.0086, and 98.7–100% of top-k edges transpose.
- **Head-phase drop.** Dropping 1–3 native samples gives corr(F_k, F) ≥ 0.9976 and top-k edge overlap ≥ 0.936.
- **Error paths.** Each of these raises an explicit error, with no fallback:
  - out of range, missing file, missing metadata row, corrupt (truncated) file → MissingSubjectError;
  - internal zero row, NaN, constant ROI → InvalidSeriesError;
  - TR 3.5 site → UnsupportedTRError.
- **Stray file.** A stray file in the npy directory shifts every later position: len = 8 instead of 7. The stray entry itself raises at load. The real directory has 1,706 entries, all directories (count only).

### 1.7 P5: my own 21 production mutants (`p5.log`, `p5_mutants.json`)

These are distinct from worker_r2's 23. Each runs in an isolated mirror under `mut/<name>/` with an import-isolation guard; the guard never tripped. Each is scored with the full 53-test suite. The control passes.

**Killed: 19/21.**
- Sign and orientation: flow_sign_flip, orientation_flip_topk, topk_signed_not_abs.
- Census and counting: density_floor, count030C_div2, census_030T_uses_AT.
- Null move checks: reverse_check_dropped, reverse_check_dropped_and_checker_off, selfloop_check_dropped_and_checker_off, rotation_degree_breaking_checker_off.
- Null statistics: all_nulls_same_seed, null_sd_ddof0.
- Loader and trim: valid_portion_keeps_padding, missing_file_synthetic_fallback, no_head_trim.
- Other: gradient_potential_axis0, tr_bergen_wrong, E1_uses_log_ratio.

Note that the "checker_off" double mutants are killed by tests that verify invariants independently of production's own checker.

**Survived: 2/21.**
- seeds_ignore_position: the null seeds drop the position term.
- curl_channel_is_broadband: the curl unit uses F instead of curl_component(F).

### 1.7b P5b: targeted time-reversal mutants, and the A2 bullet → fixture → killing mutant map (`p5b.log`)

Two more mutants in flow.py both kill `test_time_reversal_negates_flow_through_full_chain` itself:
- reversal_no_antisymmetrization: `F = C - C.T` → `F = C.copy()`;
- `F = C - 0.5*C.T`.

A global sign flip cannot test reversal, because F_rev = −F still holds under it.

The map below was grepped from `mut/*/pytest_out.txt`. Every A2 bullet has its own named fixture killed by a defect aimed at that bullet.

| A2 bullet | Fixture that fails | Mutants that fail it |
|---|---|---|
| Planted 3-cycle detected, absent in control | test_planted_cycles_detected_and_absent_in_matched_control; test_planted_cycles_per_seed_separation | topk_signed_not_abs, all_nulls_same_seed, reverse_check_dropped, reversal_no_antisymmetrization; per-seed test also flow_sign_flip, orientation_flip_topk |
| Time reversal flips F | test_time_reversal_negates_flow_through_full_chain | reversal_no_antisymmetrization, reversal_lag_uses_future_minus_past_half |
| Null: no mutual edges or self-loops, degrees kept | test_every_null_graph_preserves_degrees_and_has_no_mutual_edges_or_self_loops | reverse_check_dropped, reverse_check_dropped_and_checker_off, selfloop_check_dropped_and_checker_off, rotation_degree_breaking_checker_off |
| Padding | test_padding_rows_are_stripped_by_loader_and_features_identical | valid_portion_keeps_padding (also no_head_trim) |
| Lag in seconds at two TRs | test_two_tr_sampling_gives_consistent_flow_magnitude_and_direction; test_subject_flow_lag_is_two_seconds_through_loader | flow_sign_flip, plus worker_r2's lag_native_samples, pipeline_tr_ignored and lag_two_grid_samples |
| Spurious direction (calibration and characterization) | test_autocorrelation_mismatch_is_calibrated…; test_shared_driver_latency_produces_spurious_direction_bias_characterization | topk_signed_not_abs, count030C_div2, census_030T_uses_AT, all_nulls_same_seed, reverse_check_dropped, … |
| A1 missing subject → error | test_missing_subject_raises_without_participant_id | missing_file_synthetic_fallback |

### 1.7c P7: cause of the inexact reversal at TR ≠ 2 (`p7.log`)

At every TR in 0.7, 0.8, 0.85, 1.0, 1.73 and 1.8, I compared native lengths T with (T−1)·up/down an integer (grid end aligned) against lengths that are not:
- aligned (T = 601): max|F_rev + F| ≤ 8e-16;
- T = 602 or 604: 0.0027–0.029.

So the inexact reversal comes entirely from resampling-grid phase, not from a chain defect.

### 1.7d Uniformity-test budget

`tests/topic1_lagmotif/test_null_and_census.py:110` samples uniformity with `sample_null_graph(A, 200, 0.2, s)`, which is 200·m and not the frozen 20·m.

### 1.8 P6: spurious-direction scaling (`p6.log`)

Same generators as spurious.scenarios; T_grid 200, TR 2.0, density 0.10, 4 seeds, 200 nulls.

| Scenario | N=60 E2 | N=304 E2 | N=60 Z030T | N=304 Z030T | N=304 Z030C |
|---|---|---|---|---|---|
| latency SD 1 s | +7.63 | +58.07 | −8.14 | −61.39 | −3.33 |
| latency SD 2 s | +6.41 | +60.38 | −8.14 | −78.36 | −17.98 |
| AR mismatch | −0.77 | −0.49 | | | |
| white control | +0.63 | +0.80 | | | |

Planted cycles (20, gain 0.8): Z030C = 10.81 at N=60 vs 3.69 at N=304.

Card §9 quotes only the N=60 numbers: Z030T ≈ −7.6 and E2 ≈ +7.3 for SD 1 s; E2 ≈ +6.9 for SD 2 s.

### 1.9 A3 rerun (same 5 positional subjects, 1 thread, into verification/challenger_r2_1/a3/)

- Positions [1578, 1228, 932, 0, 57]. params_sha256 is 86863ffa…5c6 in all three runs.
- My own comparison script vs r1 and r2: 450 deterministic fields compared (tr, raw_valid_T, n_trim, valid_T, duration_s, m, acceptance, degenerate flags, all |dZ| diagnostics, n_null, attempts_factor), 0 mismatches. This is exact float equality.
- Timing:
  - mean unit time: 4.49 s (r1 4.38, r2 4.61);
  - full cohort, all units: 12.78 CPU-h (추정);
  - primary unit only: 2.29 CPU-h (추정);
  - peak RSS: 290 MB (time -v: 296,764 kB);
  - wall clock: 3:27.
- Load average was 17–31, so the wall-time ratios of 1.00–1.09 are noise-level.

### 1.10 Other checks

- **Card baseline.** I verified the baseline against the file: table1_true_test_performance.csv, condition=baseline gives 26 evaluated rows, mean test_AUROC 0.6512, SD 0.0318, n_test 255. This matches card §6.
- **ID scan (count only).** 2,095 IDs held in memory; 453 files scanned in my verification and metadata directories; 0 content hits, 0 name hits.
- **Bytecode.** No .pyc, __pycache__ or .pytest_cache newer than my START_MARKER in src, tests, my verification directory or the enigma repo.

## 2. Logic chain

1. **Census and null are correct (A1 null and SP; A2 null invariants).** An independent oracle (networkx) agrees on census, per-null counts and moments, across 7,800 nulls that include adversarial dense and degenerate graphs (1.3). Exhaustive enumeration confirms the stationary distribution is uniform (1.4).
2. **The frozen budget of 20·m is adequate at the analysis scale.** At N=304 the null moments do not drift with the attempt factor up to 64x, even at acceptance 0.10 (1.5). Under-mixing appears only on 5-node graphs (1.4). That is outside the analysis regime, but the card's "uniformity verified on small classes" holds only at budgets ≥200·m.
3. **The chain is correctly wired at every on-disk TR (A1; A2 padding, lag-in-seconds and reversal).**
   - Padding invariance is exact (1.6).
   - Lead–lag direction is correct at all 7 TRs and for leads of 1–6 s (1.6).
   - Time reversal flips F exactly at TR 1.8 and 2.0, and approximately (corr ≥ 0.9998) at the other TRs.
   - P7 shows the flip is exact (≤8e-16) at every TR once the native length aligns the 2 s grid end. The residual is therefore resampling-grid phase: a disclosed limitation, not a defect.
   - (I retract an earlier head-drop argument: dropping samples at TR 2.0 also moves F, so that comparison cannot isolate phase.)
   - Every A2 bullet's own fixture fails under a defect aimed at it (1.7b).
4. **No synthetic fallback can silently replace a real subject (A1).** Every error path raises (1.6). The fallback mutant is killed (1.7).
5. **A2 fail-on-defect holds for defects the worker did not write.** 21 of my 23 mutants are killed (19/21 in 1.7 plus 2/2 in 1.7b), including sign, orientation, census, reciprocal, self-loop and degree defects with production's own checker disabled. The 2 survivors are a seed-rule defect and a sensitivity-channel defect; neither touches E1/E2 on the primary channel.
6. **A3 is reproducible (1.9).**
7. **The card is internally consistent on the baseline (1.10).** But its §9 spurious-direction magnitude was measured at N=60, and at N=304 the same mechanism gives about 8x larger Z030T/E2 while planted-cycle Z030C shrinks (1.8). The A2 spurious bullet is satisfied in form: the bias is quantified and declared uncontrolled. The quoted magnitude, however, is not the one the cohort analysis faces.

## 3. Caveats

- **Synthetic generators.** The mixing and spurious probes use the production synthetic generators; real F matrices may differ. Real Z magnitudes are not logged, so I cannot map MC noise onto real subjects.
- **Effect sizes.** Z magnitudes do not translate directly into a between-group d. The N=304 spurious numbers bound the per-subject artefact, not the group effect.
- **Sample sizes.** P6 used 4 seeds and 200 nulls; P3 and P3b used 200–400 nulls per factor (60 at factor 1,280).
- **Uniformity.** It was tested only on 3 tiny classes. Irreducibility at N=304 is not proven: whether the reachable component equals the full class is unknown.
- **Not mutation-tested by me:** spurious.py, synthetic.py, the timing script.
- **p2 probe edit.** After p2.log was produced I edited p2_null_uniformity.py to add a main guard for re-use by p2b. Logic unchanged, pre-edit bytes not preserved. The p2.log results were reproduced by p2b at factor 20 (identical χ² of 540.46).
- **Concurrency.** The A3 rerun ran concurrently with my mutation harness.

## 4. Conclusion

CONFIRMED for M1 iteration 2. None of these issues blocks; I list them most important first.

1. **(High, scientific; card §9 and the step-5 plan.) Does not block M1, but gates step-5 authorization until an addendum restates §9 at N=304.**
   - The spurious-direction magnitude must be restated at N=304 before any cohort run. Shared-latency SD 1–2 s gives E2 ≈ +58 to +60 and Z030T ≈ −61 to −78, against planted-cycle Z030C ≈ 3.7.
   - The quoted "E2 AR-mismatch bias about −1.2" is roughly scale-stable (−0.5 at N=304). The latency bias is not.
2. **(Medium) Z precision.** MC noise of Z at large |Z| is several units even at 1,000 nulls; E2 inherits both terms. A cohort script should report the per-subject MC SE of Z, or use the log ratio or the null-SD-normalized count difference as a sensitivity.
3. **(Medium) Card wording on mixing.**
   - Card §9 says "uniformity verified on small, fully reachable classes", but the test behind it runs at 200·m (test_null_and_census.py:110), not the frozen 20·m.
   - At 20·m the null is measurably non-uniform on 5-node classes: χ² p = 1e-102 and ≈0.
   - Adequacy at N=304 rests on factor-stability evidence instead, which my P3/P3b supports (≤0.2 null SD drift).
4. **(Low) Test gaps.** No test pins that null seeds depend on position, or that the curl unit actually uses curl_component.
5. **(Low) Loader fragility.** NpyCohort positions come from sorted(os.listdir) with no directory filter. A stray file would silently shift positions and seeds.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
PY="/home/juke/superclaude-env/bin/python3 -B"; export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1
$PY -m pytest -p no:cacheprovider tests/topic1_lagmotif -q                                   # 53 passed
$PY verification/challenger_r2_1/probes/p1_census_null_oracle.py                              # all mismatch counters 0
$PY verification/challenger_r2_1/probes/p2b_uniformity_vs_budget.py                           # af20 p<1e-100; af200 p>0.5
$PY verification/challenger_r2_1/probes/p3b_low_acceptance.py                                 # null means stable across factors
$PY verification/challenger_r2_1/probes/p4_full_chain.py                                      # padding 0.0, signs correct, errors raise
$PY verification/challenger_r2_1/probes/p6_spurious_scaling.py                                # N304 latency E2 ~ +60
$PY verification/challenger_r2_1/probes/p5_mutants.py   # rebuilds verification/challenger_r2_1/mut; 19/21 killed
LC_ALL=C sha256sum -c verification/challenger_r2_1/hashes_start.txt
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt
```

Everything here is invalidated by any edit to src/topic1_lagmotif, tests/topic1_lagmotif, scripts/topic1_timing.py or the card (check against hashes_start.txt).
