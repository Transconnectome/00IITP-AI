# Handoff (Hard): explorer_r2_3, run tw-20261030-topic1, M1, iteration 2

**Summary.** The iteration-1 gate failed for one reason: the test suite never ran the production entry point (NpyCohort.load / prepare_series → pipeline.subject_flow) at a TR other than 2.0 s. As a result, pipeline-wiring defects passed all 29 tests. The production code itself is correct (challengers P2/P5: |F| ratio 0.997–1.001 at all 7 TRs).

The fix is **tests only**:
- Add one test file, `tests/topic1_lagmotif/test_production_entry_point.py`. A ready, verified copy is at `/home/juke/git/00IITP-AI/verification/explorer_r2_3/proposed_tests/test_production_entry_point.py`, sha256 d1c287e0…d04d, 24 test functions = 24 collected cases, run together with the 29 existing ones, 53 in total.
- On isolated mirrors of production, the current 29-test suite kills **2 of 20** mutants. With the proposed file it kills **20 of 20**, and every mutant fails at least one behavioural test besides the PARAMS-hash pin.
- `src/` and `scripts/` must stay byte-identical. The frozen card (§12 hashes 10/10 OK) and the A3 timing then remain valid, so no new card and no A3 rerun are needed.

## 1. Observation

### O1. Root cause, from the code
- `tests/topic1_lagmotif/test_flow_chain.py`:
  - `test_two_tr_sampling…` and `test_time_reversal…` call `preprocess()` and `lagged_net_flow(·, 1)` directly.
  - `test_full_chain_uses_all_304_rois…` calls `subject_flow` only at TR 2.0.
- `test_tr_and_loader.py::_fake_cohort` uses the default site "Yale-Gruner" (TR 2.0).
- `test_defect_sensitivity.py` re-creates defects inside the test, for example `Fbad = lagged_net_flow(zscore(_sample(X, 0.7)), 1)`; it never mutates production.
- `pipeline.py:subject_flow` therefore sits between tested parts without being tested itself.

### O2. Mutation runs: `probes/mutants.py {base|proposed}`
Each run copies `src/topic1_lagmotif` and `tests/topic1_lagmotif` to `verification/explorer_r2_3/mut/<mode>/<name>/`, applies one textual edit (asserting exactly one match), and runs pytest with an isolation guard. The production tree is never touched. Logs: `logs_mutants_base.txt`, `logs_mutants_proposed_final.txt`, `mutants_*.json`, `mut/*/*/pytest_out.txt`.

Column key:
- **base** = current 29 tests.
- **proposed** = 29 + 24 new; "K n" means killed, with n failed cases.
- **killer** = the new tests that fail. *oracle* = `test_subject_flow_equals_card_spec_oracle…`; *loader2s* = `test_subject_flow_lag_is_two_seconds_through_loader`; *trim* = `test_prepare_series_trims_in_seconds…`; *invar* = `test_flow_is_invariant_to_offset_scale…`; *pin* = `test_frozen_params_are_the_carded_params`.

| mutant (my name) | iteration-1 name(s) | base | proposed | killer (new tests) |
|---|---|---|---|---|
| control | — | 29 passed | 53 passed | — |
| pipeline_tr_ignored | c1_1 `pipeline_no_resample_tr_ignored`; c1_2 (a) | survives | K 9 | oracle, loader2s |
| pipeline_lag1_native_no_grid | c1_1 same name | survives | K 9 | oracle, loader2s |
| lag_native_samples | c1_1 same name | survives | K 7 | oracle, loader2s |
| lag_two_grid_samples | c1_2 (n); r1_2 M10 | survives | K 11 | oracle, loader2s |
| no_zscore | c1_2 (p) | survives | K 8 | oracle, invar |
| params_detrend_none | c1_2 (r) | survives | K 13 | oracle, invar, loader2s, pin |
| pipeline_ignores_detrend | r1_1 `no_detrend` (pipeline wiring) | survives | K 8 | oracle, invar |
| head_trim_in_samples | c1_1 same name | survives | K 16 | trim, oracle, loader2s |
| z_ddof0_no_nan | c1_1 same name | survives | K 1 | `test_degenerate_null_gives_nan_z…` |
| null_021C_missing_t | c1_1 same name | survives | K 1 | `test_null_moments_of_all_five_classes…` |
| chain_not_restarted | c1_2 (h) | survives | K 2 | `test_each_null_is_an_independent_restart…`, moments |
| null_counts_raise_disabled | r1_1 `invariant_check_off` | survives | K 1 | `test_null_counts_raises_when_any_null_violates…` |
| params_padtype_constant | new | survives | K 11 | oracle, loader2s, pin |
| params_highpass_on | new | survives | K 12 | oracle, loader2s, pin |
| resample_ratio_coarse (`limit_denominator(10)`) | new | K 1 | K 4 | oracle, plus existing ratio test |
| resample_before_detrend | new | K 1 | K 8 | oracle, invar, plus existing order test |
| zscore_ddof1 | new | survives | K 7 | oracle |
| C_normalised_by_T | new | survives | K 7 | oracle |
| params_n_null_500 | new | survives | K 5 | pin, plus the sha assert inside loader2s (config value only) |
| trim_s_ignored_20_samples | new | survives | K 16 | trim, oracle, loader2s |

Base kills 2 of 20 (resample_ratio_coarse and resample_before_detrend); proposed kills 20 of 20.
- Every behavioural mutant is killed by a test other than *pin*.
- `params_n_null_500` is a pure configuration value, so only hash checks catch it: *pin* and the `params_sha256` assert inside *loader2s*.

### O3. Fixture margins, synthetic only (`probes/margins.py`, `logs_margins.txt`; 4 seeds × 7 TRs, production code)
- The |F| ratio to TR 2.0 is 0.999–1.005 at every TR.
- The ratio |F(2 s lead)| / |F(4 s lead)| is 3.3–7.7. Its minimum is 3.3, at seed 14, TR 1.73.
- I first used a 3× threshold. After this margin measurement I lowered it to **2×**. The file uses seed 11, where the ratio is 7.0–7.7. This was measured on synthetic data only; no real data and no mutant outcome were involved in the choice. The lag mutants are still killed at 2×, as the rerun shows.
- At TR 1.73, *loader2s* does not catch the tr-ignored and native-sample mutants, because 1 native sample is 1.73 s ≈ 2 s. The oracle test catches them at 1.73, and loader2s catches them at 0.7, 0.85 and 1.0. This is physics, not a gap.

### O4. Tolerance and threads (`logs_oracle_maxdiff.txt`, `logs_unpinned_threads.txt`)
- max|F − F_oracle| = 0.0, bit-exact, at all 7 TRs.
- The 53-test mirror suite passes twice without the OPENBLAS/OMP/MKL pins (11.7 s and 9.5 s).
- `atol=1e-12` is therefore safe under the PROJECT.md test command. 1e-10 is an acceptable portability margin; every wiring mutant deviates by far more.

### O5. Freeze state, checked now
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: 44 OK, rc=0.
- Card §12 block: 10/10 OK.
- The card file is mode r--r--r--. Card §12 hashes src and the timing script only; there are no test hashes.

### O6. Hygiene
- No `__pycache__` or `.pyc` under `verification/explorer_r2_3`.
- No new `.pyc` in `src/topic1_lagmotif`, `tests/topic1_lagmotif` or the enigma repo.
- Participant-ID scan of my 837 files (mirrors, logs, metadata) against the npy directory names: 0 hits.
- No real subject series was loaded. The mirrored existing tests list the npy directory and read metadata only, as they do in production.

### O7. Smaller facts that bear on the nonblocking items
- The `motifs._run_chain` 2-swap does not reject u==w or v==z. Such an attempt is a no-op, yet `_new_edges_ok` passes it and it is counted as "accepted". This matches challenger_r1_2's 0.011–0.028 per 2-swap attempt.
- `data.prepare_series` floor: `X.shape[0] < 20` native samples.
- `NpyCohort.__init__` takes `sorted(os.listdir)` and pins no manifest.

## 2. Logic chain
1. A2 requires each fixture to "FAIL on the defect it targets". O1 shows that for the lag-in-seconds bullet, the defect site (`subject_flow` wiring at TR≠2) was not exercised. That is exactly challenger_r1_1's REFUTED finding, and O2's base column reproduces it independently: 18 of 20 survive.
2. The new file adds two complementary kinds of check:
   - A **spec oracle**. It is written from card §1 using only scipy/numpy primitives and hard-coded card constants. It never reads PARAMS or calls preprocess/flow helpers, so a wiring or PARAMS change in production cannot move the oracle with it.
   - **Physical tests.** One runs through the real `NpyCohort.load` with fake sites at TR 0.7/0.85/1.0/1.73 against a 2.0 site. It discriminates a 2 s lead from a 4 s lead, so it catches lag-4 s, which a ratio-only test misses. The other checks invariance to offset, scale and linear drift.
   - Together these kill every wiring mutant (O2).
3. The remaining iteration-1 survivors (Z NaN rule, null 021C, restart, invariant raise) get direct tests. Card §3's exclusion rule ("Z NaN") is now tested.
4. Because only a test file is added, the card §12 hashes and `params_sha256` stay valid (O5). The card stays frozen, the A3 timing stays valid, and the freeze order (PARAMS → A3 → card) is preserved. Any src edit would break this (card: "Any change … requires a new dated card").
5. The iteration-1 nonblocking items that would need src changes (O7, plus |ΔZ030T| disclosure and wording errata) therefore belong in a dated OPEN_ISSUES addendum. They can then be implemented in the step-5 cohort runner, which does not exist yet and is not frozen. They must not go into src now.

## 3. Caveats
- Mutation testing covers 20 hand-written mutants, not exhaustive mutation. Untested areas I know of: `spurious.py` and `synthetic.py` internals, and `scripts/topic1_timing.py`.
- *pin* (`params_sha256 == card value`) kills any PARAMS edit by construction. I kept it because PARAMS is the frozen configuration contract. Every behavioural mutant is also killed without it (O2), so verifiers should judge behavioural coverage with *pin* deselected.
- I did not run challenger_r1_1's or challenger_r1_2's harnesses, because they write into those agents' folders. Their expected outcomes are in §5.
- All margins are from synthetic band-limited signals with a 0.2 Hz cutoff. Real data were never used to set thresholds.
- I did not re-verify the scientific choices (10% density, n_null, factor 20); iteration-1 reviewers approved them.
- The harness gave each mutant one fresh mirror. The `failed=[]` field in the summary JSON is a regex artefact; per-test failures are in each `pytest_out.txt`.

## 4. Conclusion: recommended worker actions, iteration 2

**Blocking (fixes the REFUTED gate):**
1. Copy `verification/explorer_r2_3/proposed_tests/test_production_entry_point.py` verbatim to `tests/topic1_lagmotif/test_production_entry_point.py`, or reimplement it equivalently and keep every test.
   - Use the 2× threshold, seed 11 and atol 1e-12 (1e-10 is acceptable).
   - Keep the oracle independent: no PARAMS, no preprocess/flow helpers inside `_spec_oracle_flow`.
2. **Do not edit any file in `src/topic1_lagmotif/` or `scripts/topic1_timing.py`, and do not edit the card.**
   - Gate: `awk '/^```/{f=!f;next} f' <card> | grep -E '^[0-9a-f]{64}  ' | LC_ALL=C sha256sum -c` must give 10/10 OK.
   - `params_sha256()` must equal 86863ffa…c15c6.
3. Run the tests and record the logs as new files under `results/topic1/2026-10-30/`, without overwriting the iteration-1 logs:
   - new suite: expect 53 passed;
   - old 86-test suite;
   - protected hashes.
4. Record a production mutation check and correct A2's evidence claim:
   - Correct the claim to: "defects put back into production code are caught", backed by the mutation table, not by `test_defect_sensitivity.py`. Keep that file, but describe it as in-test demonstrations.
   - Harness location: `tests/topic1_lagmotif/mutation_harness.py`, which pytest does not collect because it has no `test_` prefix. Writing to `scripts/` would need the root's ownership approval.
   - Output: `results/topic1/2026-10-30/mutation_check_r2.json`.
   - My harness `verification/explorer_r2_3/probes/mutants.py` can be adapted: change `HERE` and drop the "proposed" copy step.

**Nonblocking, documentation only. Put these in a new dated `docs/03_empirical_analysis/topic1/2026-10-30_OPEN_ISSUES_addendum_r2.md` that cites the card sha; do not edit the card:**
1. Disclose |ΔZ030T| for factor 40 vs 20 on the A3 subjects: up to 0.909 at position 57 and 0.455 at position 1228. Card §10 reports only |ΔZ030C|, and E2 depends on Z030T. These values are already in `results/topic1/2026-10-30/a3_timing.json`; read them from that file and do not rerun anything on real data.
2. The acceptance rate counts 2-swap no-ops (u==w or v==z); see O7.
3. Mixing is budgeted in attempts, not accepted moves: position 1578 had acceptance 0.074, about 1.5·m accepted moves. For the step-5 runner: record acceptance per subject, report it by group, and keep the factor-40 sensitivity.
4. Positional index is not pinned to a manifest. Step-5 runner: assert n=1706 and a salted-hash digest of sorted(listdir) at start.
5. The minimum length floor is 20 native samples, about 7 grid samples at TR 0.7. Step-5 runner: report the minimum grid length per subject.
6. Degenerate-null exclusion is informative missingness. Report it by group and site, as card §3 already says.
7. Errata, wording only:
   - card §1 "No diagnosis label was loaded": the label columns were read for counts only, and no label was joined with any real-data feature (auditor);
   - card §1 density rationale: pipeline.py predates spurious_direction.json; the real-scale N=304 result is 20 cycles Z030C 6.14/4.48/3.52 at 5/10/15% (challenger_r1_1);
   - card §9: ± is an SE;
   - card §6: name enigma HANDOFF.md:21 (0.628, medicated-OCD subset) as the probable origin of "≈0.63".
8. The survey stage loaded all 1,706 npy series for QC (auditor); no features were computed and no labels were joined. This needs the root's ruling and is not a worker action.

## 5. Verification method
- **Re-run my mutation check** (about 3 min; it overwrites only `verification/explorer_r2_3/mut/`):
  `cd /home/juke/git/00IITP-AI/verification/explorer_r2_3 && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B probes/mutants.py base` (expect 18 survivors), then the same command with `proposed` (expect control 53 passed and all 20 killed).
- **After the worker copies the file:**
  - `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider tests/topic1_lagmotif -q` → 53 passed.
  - challenger_r1_1 `probes/p4_mutants.py pipeline_no_resample_tr_ignored pipeline_lag1_native_no_grid lag_native_samples null_021C_missing_t head_trim_in_samples z_ddof0_no_nan` → all 6 should now FAIL. That harness rebuilds from the current production tests.
  - challenger_r1_2 `p4_mutation.py` survivors a, n, p, r and h → all should now FAIL.
  - reviewer_r1_1 `invariant_check_off` and `no_detrend` → FAIL; reviewer_r1_2 M10 → FAIL.
- **Freeze:** card §12 `sha256sum -c` 10/10; `params_sha256()` unchanged; protected hashes 44/44.
- **Invalidation:** this analysis no longer holds if any src file or the timing script changes, if the proposed file is altered so that an oracle helper calls production preprocess/flow or reads PARAMS, or if the 2× threshold is raised without new synthetic margin evidence.
