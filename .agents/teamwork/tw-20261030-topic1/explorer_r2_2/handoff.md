# Handoff (Hard): explorer_r2_2, run tw-20261030-topic1, M1, iteration 2

**Summary.** The iteration-1 gate failed for one reason only: the A2 fail-on-defect tests did not exercise the production entry point. Production code was judged correct by all five verifiers, and nothing I found contradicts that. The fix is therefore one new test file, `tests/topic1_lagmotif/test_production_entry_point.py`, with no change to any `src/` or `scripts/` file. Because the source is untouched, the frozen card (sha256 1e589f0b…75aa), its §12 code hashes and `params_sha256` all stay valid; the card lists no test files.

I wrote and verified the file at `/home/juke/git/00IITP-AI/verification/explorer_r2_2/proposed/test_production_entry_point.py` (sha256 60150cfe…a425a55).
- 18 tests; they pass against the real production package (1.61 s).
- In isolated mirror copies they kill **17/17** mutants. These are every survivor that challenger_r1_1, challenger_r1_2, reviewer_r1_1 and reviewer_r1_2 reported, plus 4 related ones.
- The existing 29-test suite kills **1/17** (M15).

## 1. Observation

### Gate record (input)
- `gate: FAIL (challenger_r1_1 REFUTED)`. Its single blocking issue reads: "A2 fail-on-defect is not met for the lag-in-seconds bullet at the production entry point. Three mutants of pipeline.subject_flow pass all 29 tests".
- reviewer_r1_1, reviewer_r1_2 and challenger_r1_2 returned APPROVE/CONFIRMED but listed further survivors:
  - reviewer_r1_1: no_detrend in the pipeline; invariant raise off in null_counts.
  - reviewer_r1_2: M10, lag 2 grid samples.
  - challenger_r1_2: a, TR 2.0 passed in place of series.tr; n, lag 4 s; p, no z-score; r, PARAMS detrend none; h, no restart.
  - challenger_r1_1 also listed: null_021C_missing_t, head_trim_in_samples, z_ddof0_no_nan.
- auditor_r1_1: CLEAN. No INTEGRITY_VIOLATION was reported.

### Code read
- `src/topic1_lagmotif/pipeline.py:65-68`: `subject_flow` calls `preprocess(series.X, series.tr, detrend_type=params["detrend"], padtype=params["padtype"], highpass_cutoff_s=..., grid_dt=...)`, then `lagged_net_flow(Z, lag_seconds_to_samples(params["lag_s"], params["grid_dt_s"]))`.
- `tests/topic1_lagmotif/test_flow_chain.py`:
  - The two-TR test (`test_two_tr_sampling_gives_consistent_flow_magnitude_and_direction`), the time-reversal test and the detrend test all call `preprocess` and `lagged_net_flow(·,1)` directly.
  - `test_full_chain_uses_all_304_rois_and_exact_edge_count` calls `subject_flow` only at TR 2.0.
- `tests/topic1_lagmotif/test_tr_and_loader.py`: `_fake_cohort(..., site="Yale-Gruner")` is TR 2.0. `test_head_trim_is_defined_in_seconds` unit-tests only `head_trim_samples`, never `prepare_series` or `NpyCohort.load` at another TR.
- `tests/topic1_lagmotif/test_defect_sensitivity.py`: each defect is simulated inside the test code rather than injected into production.
- `src/topic1_lagmotif/motifs.py:247-249`: the null 021C formula is `nc["p2"] - 3.0*c - t`. Z uses `ddof=1` and is NaN when sd = 0. The `if bad.size: raise` in `null_counts` was not exercised by any test.
- Card `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md`:
  - r--r--r--; its §12 hashes cover src/ and scripts/ only.
  - Line 16 pins `params_sha256 = 86863ffa…bfea15c6`.
  - Line 51 excludes subjects whose primary null is degenerate ("Z NaN").

### Probes (all synthetic; no real subject series loaded; positional indices only)
**P1. Proposed test file run against production** (`proposed_vs_production.log`):
- Command: `PYTHONDONTWRITEBYTECODE=1 OPENBLAS/OMP/MKL=1 python3 -B -m pytest -p no:cacheprovider -q verification/explorer_r2_2/proposed/test_production_entry_point.py`
- Result: **18 passed in 1.61 s.**

**P2. Mutation harness** (`mutation_harness.py`, `mutation_results.json`, `mutation_run_v2.log`):
- Each mutant is a copy of src/topic1_lagmotif plus tests under `verification/explorer_r2_2/mut/<name>/`, with exactly one string replacement; the harness asserts the target string occurs exactly once.
- An isolation guard asserts the imported `pipeline.__file__` lies inside the mutant directory.
- For each mutant, the existing suite was run with the proposed file hidden, then the proposed file was run on its own.

| Mutant | Existing 29 | Proposed 18 | Behavioural killer in proposed file (besides the oracle) |
|---|---|---|---|
| M00 control | 29 passed | 18 passed | – |
| M01 subject_flow passes grid_dt instead of series.tr (no resample) | passed | 4 failed | lag_is_in_seconds[0.7, 0.85] |
| M02 lag 1 native sample, no grid | passed | 4 failed | lag_is_in_seconds[0.7, 0.85] |
| M03 lag = round(lag_s/TR) grid samples | passed | 3 failed | lag_is_in_seconds[0.7, 0.85] |
| M04 lag doubled to 4 s | passed | 3 failed | reference oracle only (both TRs shift equally) |
| M05 no z-score | passed | 5 failed | invariant_to_offset_scale_drift[0.7, 1.73] |
| M06 PARAMS detrend "none" | passed | 7 failed | invariance, PARAMS hash pin |
| M07 subject_flow detrend "none" | passed | 5 failed | invariance[0.7, 1.73] |
| M08 null 021C missing −t | passed | 1 failed | per-null oracle |
| M09 head trim with TR 2.0 at every site | passed | 4 failed | loader_head_trim_in_seconds[0.7, 0.85, 1.73] |
| M10 Z=(obs−mean)/(sd+1e−12), no NaN | passed | 1 failed | degenerate_null_gives_nan_z |
| M11 Z with ddof 0 | passed | 1 failed | per-null oracle |
| M12 chain not restarted between nulls | passed | 1 failed | per-null oracle |
| M13 invariant raise disabled in null_counts | passed | 1 failed | null_counts_raises (monkeypatched flags) |
| M14 pipeline padtype "constant" | passed | 2 failed | reference oracle |
| M15 E2 sign swapped | 1 failed | 1 failed | per-null oracle |
| M16 pipeline high-pass on (128 s) | passed | 3 failed | reference oracle |
| M17 density_primary 0.05 | passed | 2 failed | PARAMS hash pin |

**P3. The 18 tests in the proposed file:**
1. PARAMS hash pinned to the card value, plus key values.
2. Loader head trim in seconds through `NpyCohort.load` at TR 0.7, 0.85, 1.73 and 2.0, on fake IDs and real site names (4 tests). Expected n_trim: 58, 48, 24, 20. valid_T, duration_s and the X slice are exact, and padding is stripped.
3. `subject_flow` equals an independent scipy/numpy reference chain (detrend → resample_poly with Fraction ratio, padtype line → z-score → 1-grid-sample lag) to atol 1e-12, at TR 0.7, 1.73 and 2.0, on trended raw-scale padded input (3 tests).
4. Challenger_r1_1's lag-in-seconds fixture, extended to TR 0.85 and routed through `NpyCohort.load` (3 tests).
5. Time reversal through `subject_flow`: exact at 2.0; corr > 0.999 at 0.7 and 1.73.
6. Invariance of `subject_flow` to offset, per-ROI gain and per-ROI linear drift at TR 0.7 and 1.73 (2 tests).
7. `motif_statistics` null mean, null SD and Z for all 5 classes equal an oracle built from independent `sample_null_graph` restarts with the same seeds (ddof 1); E2 equals Z030C − Z030T.
8. A regular 7-tournament gives NaN Z with degenerate flags, and E1 and E2 are NaN.
9. `null_counts` raises `NullInvariantError` when any null's flag is nonzero.
10. `extract_subject` at TR 0.7 records tr, n_trim 58, the frozen hash and m.

**P4. Safety** (at end):
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: 0 failures.
- `prod_hashes_before.txt` (19 files: 9 src, 7 tests, the timing script and the 2 topic1 docs): 0 failures.
- No `*.pyc`, `__pycache__` or `.pytest_cache` newer than my DISPATCH.md in src, tests, my verification directory or enigma.
- Whole-run `audit_layout.py`: 67 files, `findings: []`, rc 0 (`layout_lint.log`).

**P5. A3 JSON check** (`results/topic1/2026-10-30/a3_timing.json`, numeric fields only):
- `abs_dZ030T_factor` is 0.909 at position 57 and 0.455 at position 1228; the card reports only ΔZ030C.
- Acceptance at 10% is 0.074 at position 1578; the other positions are 0.62–0.75.

## 2. Logic chain
1. The gate failed on one requirement: A2's "would FAIL on the defect" was not met at the production entry point (gate record). Approvals from the other verifiers do not override a REFUTED challenger.
2. Every survivor in the gate record is a missing test, not a production defect. This rests on: challenger_r1_1 P5 (corr 1.000 at all 7 TRs); challenger_r1_2 P1/P2; reviewer and auditor reproductions; and my P1, 18/18 passing on unmodified production.
3. A tests-only fix leaves the card §12 hashes (src/ and scripts/) and the card's own sha valid; the card lists no tests (Observation). Editing src/ would invalidate the freeze and need a new dated card, at no benefit.
4. The proposed file kills all 17 mutants (P2). Each A2 bullet now has a behavioural, requirement-level killer, not only the oracle. Lag-in-seconds is covered by M01–M03, detrend order and z-score by M05–M07, padding and head trim by M09, the degenerate rule by M10. The reference oracle and the PARAMS hash pin cover what behavioural tests cannot see, such as a lag doubled consistently at every TR (M04), padtype and high-pass.
5. The non-blocking items from iteration 1 do not need code. They are disclosures or rules for step 5, so they belong in an open-issues addendum and must not be applied as edits to the frozen card.

## 3. Caveats
- Mutants are string edits I chose; I cannot exclude other defect classes (for example in `oriented_topk_graph` or the census) that no test catches. Iteration 1 already killed many of those (challenger_r1_1: 24 killed).
- The reference-oracle test is an independent reimplementation using the same scipy primitives. A shared defect in scipy, or a shared misreading of the spec, would pass it. Its tolerance (1e-12) assumes the same floating-point operations; across BLAS builds it might need about 1e-10. Here it passed with BLAS pinned to 1 thread.
- Provenance: `mutation_run.log` came from an earlier 16-test version of the proposed file. I then added the invariance test, two parametrised cases, to make 18, and `mutation_run_v2.log` and `mutation_results.json` come from the final 18-test bytes. The 16-test bytes were not kept; they are the final file without `test_subject_flow_is_invariant_to_offset_roi_scale_and_linear_drift`. An earlier draft also had a wrong bound, `max|F| < 1`, which failed on control at TR 1.73 (1.096). I corrected it to `<= 2` (|C_ij − C_ji| ≤ 2) before any mutation run.
- I did not rerun the old 86-test suite, A3 timing or spurious_direction; none of them change under a tests-only fix.
- I did not read the peer explorers' (r2_1, r2_3) outputs, to keep this work independent.
- The `mut/` directories (2.4 MB of source copies) are retained under my verification directory for reproducibility.

## 4. Conclusion (strategy for the iteration-2 worker)
**Must do (blocking):**
1. Copy `verification/explorer_r2_2/proposed/test_production_entry_point.py` byte-for-byte to `tests/topic1_lagmotif/test_production_entry_point.py`, or write an equivalent file covering the same 10 behaviours. Make **no edits** to any file in `src/topic1_lagmotif/`, `scripts/topic1_timing.py`, the card, or the existing test files.
2. Run the new suite and expect **47 passed** (29 + 18). Save the log as a **new** file, `results/topic1/2026-10-30/new_tests_r2.log`; do not overwrite `new_tests.log`.
3. Rerun the old 86-test suite. Save its log as `results/topic1/2026-10-30/old_suite_86_r2.log`.
4. Run the protected-hash check, verify the card sha and the §12 `sha256 -c`, and confirm `params_sha256`.
5. Record the sha256 of every file in `tests/topic1_lagmotif/*` in `results/topic1/2026-10-30/test_hashes_r2.txt`, because the card §12 does not hash tests.
6. Optionally re-run `verification/explorer_r2_2/mutation_harness.py` from a copied identity directory. Do not run it in place; it rebuilds `mut/` and overwrites its results JSON.

**Should do (non-blocking; disclosure only, in a NEW file `docs/03_empirical_analysis/topic1/2026-10-30_OPEN_ISSUES_addendum_r2.md`; do not edit the frozen card or rewrite the reviewed OPEN_ISSUES bytes 23ca…):**
- Factor-40 vs factor-20 |ΔZ030T| reaches 0.909 (position 57) and 0.455 (position 1228). This bears on E2; the card reported only ΔZ030C.
- The acceptance rate counts 2-swap no-ops as accepted (challenger_r1_2: 0.011–0.028 per attempt). Mixing at low acceptance (0.074) is limited, so step 5 should pre-specify an acceptance-stratified sensitivity analysis, or a floor on accepted moves.
- Positional indices are not pinned. Before step 5, record the count and a salted digest of the sorted directory listing at load time, in the cohort script.
- There is no minimum valid length on the 2.0 s grid (the floor is 20 native samples, about 7 grid samples at TR 0.7). Pre-specify one in seconds before step 5.
- At real scale (N=304, T=150) planted-cycle Z030C falls with density: 6.14 / 4.48 / 3.52 at 5 / 10 / 15% (challenger_r1_1 P6). Keep the 10% primary; the stated reason is degeneracy at 5%.
- Degenerate-null exclusion is informative missingness; report the degenerate rate by group and by site.
- Wording errata, which change no analysis:
  - card §1 "No diagnosis label was loaded" should read "no label was joined with any real-data feature";
  - the ± in card §9 is an SE;
  - the probable origin of "≈0.63" is enigma HANDOFF.md:21 (0.628, medicated-OCD subset).
- For root adjudication: the survey-stage full QC load of all 1,706 npy series (auditor_r1_1).
- The E2 bias under AR mismatch (about −1.2) is recorded but not asserted. An E2 characterisation assertion is optional.

## 5. Verification method
- Production pass: `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q verification/explorer_r2_2/proposed/test_production_entry_point.py` → 18 passed.
- After the worker copies the file: `... -m pytest -p no:cacheprovider tests/topic1_lagmotif -q` → 47 passed.
- Mutation evidence: copy `verification/explorer_r2_2/` to a new identity directory, then run `python3 -B mutation_harness.py` there. Expect M00 to pass and all of M01–M17 to fail with the proposed file; with the existing suite alone, only M15 fails.
- Integrity: `sha256sum -c verification/explorer_r2_2/SHA256SUMS.txt`; `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt`; `LC_ALL=C sha256sum -c verification/explorer_r2_2/prod_hashes_before.txt` (it must still pass after the worker's change, because only a new test file is added).
- Invalidation: any edit to `src/topic1_lagmotif/*`, PARAMS or the card. The first two change `params_sha256` or the §12 hashes, and the proposed hash-pin test then fails by design. Also invalid if the control (M00) fails on another host because the 1e-12 tolerance is too tight.
