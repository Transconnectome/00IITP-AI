# Handoff (Hard) — explorer_r2_1, run tw-20261030-topic1, M1, iteration 2

**Summary.** Iteration 1 failed for one reason. No test drives the production entry point (`prepare_series` / `NpyCohort.load` → `pipeline.subject_flow`) at any TR other than 2.0 s, so pipeline wiring defects pass all 29 tests. The production code itself is correct.

The fix is **tests only**. Add one new file, `tests/topic1_lagmotif/test_production_entry_point.py`, with 18 tests. The proposed file is at `/home/juke/git/00IITP-AI/verification/explorer_r2_1/proposed_tests/test_production_entry_point.py`, ready to copy verbatim.

- On production: 18 passed. Full mirror suite: 47 passed.
- On the union of every surviving mutant reported in iteration 1, plus extras: 38/38 mutants are killed. 13 of them pass the current 29 tests and are killed only by the new file.
- Nothing in `src/`, `scripts/` or the frozen card changes, so card §12 hashes and `params_sha256` stay valid. No re-freeze and no A3 re-run are needed.

## 1. Observation

**O1. Production code** (read-only).
- `src/topic1_lagmotif/pipeline.py:66-69` `subject_flow` calls `preprocess(series.X, series.tr, detrend_type=params["detrend"], padtype=params["padtype"], ...)`, then `lagged_net_flow(Z, lag_seconds_to_samples(params["lag_s"], params["grid_dt_s"]))`. This is correct.
- `data.py:71-84` `prepare_series` uses `head_trim_samples(tr, trim_s)`.
- `data.py:127-139` `NpyCohort.load` uses `analysis_tr(site)`.

**O2. Current tests**, all in `tests/topic1_lagmotif/`.
- Every `subject_flow` / `extract_subject` call runs at TR 2.0:
  - `test_flow_chain.py:86-102`: `prepare_series(raw, 2.0, ...)`;
  - `test_tr_and_loader.py:225-271`: fake site `Yale-Gruner`, TR 2.0.
- The two-TR test and the time-reversal test (`test_flow_chain.py:50-74`) call `preprocess` + `lagged_net_flow(·, 1)` directly, not `subject_flow`.
- `test_defect_sensitivity.py` re-creates defects inside the test body instead of mutating production code.
- `head_trim_samples` is unit-tested (`test_tr_and_loader.py:288-292`), but `prepare_series` at TR ≠ 2 is not.
- No test pins `params_sha256`, the NaN-on-SD-0 rule, the null 021x formulas, or restart-per-null.

**O3. Proposed file on production** (`log_proposed_on_production.txt`): `18 passed in 1.76s`. Of that, 1.16 s is the numba compile.

**O4. Mutation union** (`probes/p1_mutants_union.py`; v2 log `log_p1_mutants_union_v2.txt`; JSON `p1_mutants_summary_all.json`).
- The mutant table is challenger_r1_1's `p4_mutants.py` M-dict, copied with sha256 recorded in `provenance_mutant_table.sha256`. I added 7 survivors named by challenger_r1_2, reviewer_r1_1 and reviewer_r1_2.
- Each mutant runs in an isolated mirror with an isolation-guard conftest. Every edit must match exactly once.
- Control: 47 passed. The 25 mutants that the old tests kill fail in the mirror, which shows the mirror imports its own mutated copies.
- **Killed only by the new file (old suite passes all 29):**

| Mutant | Old failures | New failures |
|---|---|---|
| pipeline_no_resample_tr_ignored (challenger_r1_1 blocking) | 0 | 7 |
| pipeline_lag1_native_no_grid (challenger_r1_1 blocking) | 0 | 7 |
| lag_native_samples (challenger_r1_1 blocking) | 0 | 6 |
| pipeline_lag_doubled (= r1_2 n, reviewer_r1_2 M10) | 0 | 4 |
| no_zscore (r1_2 p) | 0 | 5 |
| params_detrend_none (r1_2 r) | 0 | 6 |
| pipeline_detrend_none_literal (reviewer_r1_1 no_detrend) | 0 | 5 |
| pipeline_padtype_constant | 0 | 3 |
| head_trim_in_samples | 0 | 5 |
| z_ddof0_no_nan | 0 | 2 |
| null_021C_missing_t | 0 | 1 |
| no_restart_per_null (r1_2 h) | 0 | 2 |
| loader_tr_fixed_2 | 0 | 1 |

- The other 25 mutants are killed by the old suite, as before. **Survivors: 0.**
- The v1 harness run mislabelled every mutant as surviving: its regex lacked `re.M`. It is preserved unchanged in `failed_v1_regex/`, with SHA256SUMS and a README, and is superseded by v2.

**O5. A3 mixing diagnostic** (`results/topic1/2026-10-30/a3_timing.json`, positional indices only).
- `abs_dZ030T_factor` (factor 40 vs 20) reaches 0.909 at position 57 and 0.455 at position 1228.
- Card §10 reports only |ΔZ030C|, which is 0.04–0.33. challenger_r1_2's nonblocking item is confirmed.

**O6. N=304 planted cycles at the frozen 10%** (`log_p2_planted_n304.txt`; 6 seeds, 200 nulls, about 1 s per graph).

| Cycles | Injected mean (min) | Control mean (max) |
|---|---|---|
| 20 | 4.86 (2.74) | −0.44 (0.37) |
| 40 | 7.98 (4.76) | 0.13 (1.69) |

**O7. Safety.**
- `sha256sum -c sentinel/PROTECTED_HASHES.txt`: 44 OK, rc=0.
- Card §12 hashes still match the current src/scripts (diff differs only in line order).
- No file in src/ or tests/ is newer than my start. No new .pyc in enigma. No `__pycache__` in my tree.
- ID scan of my 799 files (including mirrors) against the npy directory names, count only: 0 hits.
- I loaded no real subject series.

## 2. Logic chain

1. **What the REFUTED verdict asks for.** A2 requires fixtures that would FAIL on the defect they target, with the lag-in-seconds defect located in the production entry point (O2). The verdict is cleared only by a test that runs `subject_flow` at a resampled TR. The challenger's ratio test does that (kills 3/3 of its mutants, O4).
2. **Why the ratio test is not enough.** A ratio between two TRs that both go through the same mutated pipeline cannot see defects common to both TRs: lag doubled, no z-score, detrend off. These are exactly the r1_2 and reviewer survivors.
3. **How to pin the entry point.** Use an independent oracle (scipy `detrend` → `resample_poly` with a hard-coded ratio → z-score → literal lag 1) plus a pinned `params_sha256`. Neither takes its values from PARAMS, so a mutant that rewires or ignores PARAMS fails. O4 confirms this: all 7 pipeline/PARAMS mutants are killed.
4. **The remaining survivors.** Each gets a cheap, deterministic test that guards a frozen rule:
   - head trim in seconds (card §1);
   - the degenerate → NaN exclusion (card §3 line 51);
   - null 021x formulas checked against the census of the same null graphs drawn one at a time;
   - restart per null (PARAMS `attempts_factor` comment);
   - site → TR wiring in the loader.
   All pass on production (O3).
5. **Why tests only.** Any edit to `src/` or `scripts/` breaks card §12 and/or `params_sha256`. The read-only card would then be stale, and A3 would no longer be at the frozen configuration. A tests-only change keeps A1, A3 and A4 exactly as the verifiers approved them and fixes the one A2 gap.
6. **Nonblocking items.** None requires a code change for M1. Some are disclosures (O5, density provenance, wording); the rest are requirements for the cohort-statistics script before step 5. They belong in an append-only section of OPEN_ISSUES, not in the frozen card (§12 lists no tests and no test count, so no card edit is needed).

## 3. Caveats

- The mutants are textual and finite: 38 mutants, all synthetic. Killing them does not prove the absence of other wiring defects.
- The oracle test requires agreement to atol 1e-10 with scipy `resample_poly(padtype='line')`. A scipy upgrade that changes padding numerics would fail it. That is a deliberate tripwire, but note it.
- The restart test assumes the frozen design "each null is an independent restart". If a later design adopts a continuing chain, the test must change with the card.
- The degenerate fixtures are tiny graphs. They pin the NaN rule; they do not estimate the real-data degeneracy rate.
- P2 (N=304) uses 6 seeds. The control maximum of 1.69 at 40 cycles shows why any N=304 fixture should assert on means, not per seed.
- I did not re-verify the survey's or the card's data facts; four r1 verifiers already did. I ran no A3 timing.
- Other r2 explorers may recommend `src` changes, such as an acceptance floor. That would conflict with the frozen card, and in my view it is not needed for the gate.

## 4. Conclusion

Worker r2, in this order:

1. **Copy the test file.** Copy `verification/explorer_r2_1/proposed_tests/test_production_entry_point.py` verbatim to `tests/topic1_lagmotif/test_production_entry_point.py`, as a NEW file. Do not edit worker_r1's five test files or `conftest_helpers.py`. Do NOT add an unprobed N=304 fixture. Record O6 in OPEN_ISSUES instead. If one is added anyway, use exactly the probed configuration and thresholds: `synthetic.planted_cycles(200, 304, 20, g, np.random.default_rng([304, 20, s]))` for s in 0..5, nulls `np.arange(200) + 1000*s`, factor 20, p_rot 0.2, density 0.10, about 13 s; assert injected mean > 3, |control mean| < 1, injected min > control max (observed: min 2.74 > max 0.37).
2. **Change nothing else in code.** No edits to `src/topic1_lagmotif/*`, `scripts/topic1_timing.py`, PARAMS or the card. Verify with card §12 `sha256sum -c`, which must give 10/10, and `params_sha256() == 86863ffa…5c6`.
3. **Re-run and log to new dated files** (keep the r1 logs untouched):
   - new suite: 47 passed expected, written to `results/topic1/2026-10-30/new_tests_r2.log`;
   - old suite (86 passed), written to `old_suite_86_r2.log`;
   - `sha256sum -c PROTECTED_HASHES.txt`.
4. **Append to OPEN_ISSUES.** Add a dated section "Iteration-2 additions (post-freeze, pre-results; card unchanged)" to `docs/03_empirical_analysis/topic1/2026-10-30_OPEN_ISSUES.md`. Append only; existing items stay byte-identical. Contents:
   - (a) The A2 production-entry gap and its fix: new test file, mutant evidence.
   - (b) |ΔZ030T| at factor 40 vs 20 is up to 0.909 (position 57) and 0.455 (position 1228), which bears on E2. Card §10 reported only ΔZ030C.
   - (c) **Errata to card wording, non-substantive.**
     - §1 overstates the density provenance: pipeline.py was written before spurious_direction.json. Real-scale planted detection at N=304 is 6.14/4.48/3.52 at 5/10/15% (challenger_r1_1) and 4.86 at 10% (O6), so 10% over 5% rests on degeneracy risk.
     - The ± in §9 is an SE.
     - "No diagnosis label was loaded" should read "no label was joined with any real-data feature".
     - The probable origin of "≈0.63" is enigma HANDOFF.md:21 (0.628, medicated-OCD vs HC subset).
   - (d) The reported acceptance rate counts 2-swap no-ops (shared endpoint).
   - (e) **Cohort-script requirements before step 5.**
     - acceptance rate by group and site, plus an acceptance-stratified sensitivity analysis (or an accepted-moves floor), labelled as a post-freeze, non-pre-registered addition;
     - degenerate rate by group and site;
     - a minimum length on the 2 s grid;
     - a positional manifest pin: count plus a salted digest of `sorted(listdir)`;
     - E2 bias under AR mismatch (about −1.2) treated as known.
   - (f) For the root: the survey-stage QC read of all 1,706 series (auditor_r1_1).
5. **Do NOT** add a test that the current code fails. In particular, do not add an "E2 calibrated under AR mismatch" test: E2 is about −1.2 there. Do not change the density, attempts or n_null: that would be tuning after A3. Do not write to verifier folders.

## 5. Verification method

- **Proposed file on production:**
  `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q verification/explorer_r2_1/proposed_tests/test_production_entry_point.py`
  Expect 18 passed.
- **Mutation union:**
  `cd /home/juke/git/00IITP-AI/verification/explorer_r2_1/probes && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B p1_mutants_union.py`
  Takes about 3 min and rebuilds `../mut/`. Expect control 47 passed and 0 SURVIVES, with the 13 mutants of O4 marked `killed_only_by_new`. To verify without overwriting, copy the directory first.
- **After the worker's change:**
  - `pytest tests/topic1_lagmotif -q` gives 47 passed;
  - the old suite gives 86 passed;
  - card §12 `sha256sum -c` gives 10/10;
  - the protected-hash check gives rc=0.
- **Invalidation conditions:** any `src/` or `scripts/` edit; a different `params_sha256`; or the proposed file failing on production.
- **Manifest:** `verification/explorer_r2_1/SHA256SUMS.txt` (excludes `mut/`).
