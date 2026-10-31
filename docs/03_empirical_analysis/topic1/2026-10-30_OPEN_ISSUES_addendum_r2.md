# Topic 1: open issues, iteration-2 addendum (run tw-20261030-topic1, worker_r2, 2026-10-30)

This file adds to `2026-10-30_OPEN_ISSUES.md` (sha256 `23ca483dbdc5e8713e5354734a7aea4264dad99c4b1ac00bf27715de0983e5d2`, unchanged) and does not replace it. Everything here was written after the card freeze and before any cohort result.

The frozen card `2026-10-30_topic1_analysis_card.md` is unchanged: sha256 `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`, read-only. Its §12 code hashes still pass (10/10), and `params_sha256` is still `86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6`. No file in `src/topic1_lagmotif/` or `scripts/topic1_timing.py` was changed in iteration 2.

Nothing below is pre-registered. The items under F are requirements for the cohort script before step 5. Any analysis that comes from them must be labelled post-freeze.

## D. Iteration-2 fix: A2 fail-on-defect at the production entry point

25. **Gap closed: no test ran the production entry point at TR ≠ 2.0 s.** challenger_r1_1 found this in iteration 1 (verdict REFUTED).
    - The iteration-1 two-TR and time-reversal fixtures called `preprocess` and `lagged_net_flow(·, 1)` directly.
    - Every `subject_flow` and loader test used a TR 2.0 site.
    - `test_defect_sensitivity.py` re-creates defects inside the test body.
    - So pipeline-wiring defects passed all 29 tests.
26. **The fix adds tests only.** New file `tests/topic1_lagmotif/test_production_entry_point.py` (24 tests), copied byte-for-byte from `verification/explorer_r2_3/proposed_tests/` (sha256 `d1c287e08f0d998f46493dd90ab21dfba8ff9d384d5673790a8d61b2f420d04d`). It covers:
    - a pin on the carded `params_sha256`;
    - head trim in seconds at all 7 on-disk TRs;
    - `subject_flow` equals a spec oracle at all 7 TRs (atol 1e-12). The oracle uses scipy/numpy only, with card constants hard-coded; it reads no PARAMS and calls no production helpers;
    - a lead-lag signal loaded through `NpyCohort.load` at TR 0.7, 0.85, 1.0 and 1.73 against a TR 2.0 site. It checks orientation, an |F| ratio in [0.85, 1.15], and a 2 s lead that beats a 4 s lead by more than 2×, then runs `extract_subject`;
    - invariance to offset, scale and linear drift at TR 0.7;
    - a degenerate null gives NaN for Z, E1 and E2, with its flag set;
    - null moments for all 5 classes equal the census of the null graphs drawn independently with the same seeds;
    - each null is a restart;
    - the `NullInvariantError` raise path.
27. **Evidence: defects placed into copies of the production code.**
    - Harness: `verification/worker_r2/mutants.py`. Result: `results/topic1/2026-10-30/mutation_check_r2.json`.
    - Setup: 23 one-edit mutants, each in an isolated mirror with an isolation guard.

    | Mode | Control | Mutants killed |
    |---|---|---|
    | full suite | 53 passed | 23 of 23 |
    | iteration-1 tests only | 29 passed | 3 of 23 |
    | full suite with the PARAMS pin test deselected | 52 passed | 23 of 23 |

    - The iteration-1 tests kill only `resample_ratio_coarse`, `resample_before_detrend` and `e2_sign_swapped`.
    - Twenty mutants are killed only once the new file is present.
    - Two mutants with the pin deselected, `params_n_null_500` and `params_density_primary_005`, are still killed only by a hash comparison: the `params_sha256` assert inside the loader test. These are config-value changes with no behaviour the fixtures can see. Every other mutant fails at least one behavioural or oracle test.
28. **Minor test-text note (no behaviour change).** `test_flow_is_invariant_to_offset_scale_and_linear_drift_at_tr_07` asserts `max|F| <= 1.0`, with a comment that calls this bound general.
    - The only general bound is |F| ≤ 2T/(T−1): explorer_r2_2 observed 1.096 on another signal at TR 1.73.
    - The assertion holds for this seeded fixture.
    - It was kept unchanged so that the mutation evidence stays bound to the reviewed bytes.
29. **Time reversal is still not tested through `subject_flow`.** The iteration-1 reversal fixture calls `preprocess` and `lagged_net_flow` directly.
    - The production chain is verified by challenger_r1_2 (P2: exact at 2.0; corr ≥ 0.99993 elsewhere).
    - The spec-oracle equality at all 7 TRs pins the chain that reversal runs through.
    - A dedicated end-to-end reversal fixture is not present (explorer_r2_2's file has one).

## E. Disclosures about frozen-card numbers (no analysis change)

30. **|ΔZ030T| for attempts factor 40 vs 20 is not in card §10.** Card §10 and item 14 report only |ΔZ030C| (0.04–0.33). On the same A3 subjects, `results/topic1/2026-10-30/a3_timing.json` (primary unit `broadband@0.10`) gives `abs_dZ030T_factor`:
    - 0.909 at position 57;
    - 0.455 at position 1228;
    - 0.02–0.03 for the other three.

    This bears on E2 = Z030C − Z030T. challenger_r1_2's synthetic probes suggest Monte Carlo noise in sd_null that grows with |Z|, not under-mixing, but this is not shown on the real graphs.
31. **The acceptance rate counts 2-swap no-ops.** In `motifs._run_chain`, a 2-swap with u == w or v == z passes `_new_edges_ok` and is counted as accepted, although it leaves the graph unchanged.
    - challenger_r1_2 measured this at 0.011–0.028 per 2-swap attempt, about 25% of accepted moves when acceptance is near 0.08.
    - The reported `acceptance` therefore overstates real moves for hub-heavy graphs.
32. **The mixing budget is set in attempts, not accepted moves.**
    - Position 1578 had acceptance 0.074 at the primary unit, so 20·m attempts give about 1.5·m accepted moves (fewer real ones, see item 31).
    - Agreement between 20·m and 40·m does not prove mixing.
    - Low acceptance tracks gradient dominance, which may differ between groups (reviewer_r1_2).
33. **Card wording errata.** None of these is substantive, and the card is not edited.
    - **§1 density provenance.** `pipeline.py` (mtime 21:00:54 KST, density 0.10 already set) predates `spurious_direction.json` (21:06:35). The JSON cannot have been an input to the choice; it is consistent with it.
      - At real scale (N = 304, T = 150, 20 planted cycles), detection falls as density rises: Z030C 6.14 / 4.48 / 3.52 at 5 / 10 / 15% (challenger_r1_1).
      - explorer_r2_1 measured 4.86 at 10% over 6 seeds.
      - So the case for 10% over 5% rests on the risk of degenerate nulls at 5%, not on dilution.
    - **§9.** The ± in "Z030C −0.38 ± 0.35" is a standard error (sd 1.22, n = 12), as item 12 says.
    - **Preamble (line 4), "No diagnosis label was loaded in this run".** This is true of the worker code path. For the run as a whole, the precise statement is: no label was joined with any real-data feature. Labels were read for counts only (auditor_r1_1).
    - **§6 "≈0.63".** The likely origin is enigma `HANDOFF.md:21`: AUROC 0.628 for the medicated-OCD vs HC subset, which is not a main-cohort number.

## F. Requirements for the cohort script before step 5 (not pre-registered; label as post-freeze)

34. **Report acceptance by group and site.** Add either an acceptance-stratified sensitivity analysis or a floor on accepted moves (items 31–32). The primary attempts factor stays at 20.
35. **Report the degenerate-null rate for E1 and E2 by group and site.** Excluding degenerate subjects is informative missingness, because degeneracy correlates with gradient share.
36. **Report the per-subject length on the 2.0 s grid, and set a floor in seconds.** `prepare_series` requires only 20 native samples after the head trim, which is about 7 grid samples at TR 0.7.
37. **Pin the positional manifest.** Positions index `sorted(os.listdir)`, and adding or removing a directory silently remaps positions and seeds. Record the count (1,706) and a salted digest of the sorted names, and check both at load.
38. **Acknowledge the E2 bias under AR(φ) mismatch** (about −1.2 at 10%, item 12). It is characterized but not controlled, and no fixture asserts E2 calibration.

## G. For the root to adjudicate

39. **Survey-stage QC read of all 1,706 series.** `verification/explorer_survey_1/probe_data_survey.py` loaded every npy series for a NaN/zero-ROI scan, before the iteration-level "≤ 5 real subjects" rule applied (auditor_r1_1). No features were extracted and no labels were joined. It is outside the worker's work product.

## Verification

- A3 was re-run in iteration 2 into `results/topic1/2026-10-30/a3_r2/` on the same 5 positions.
  - It shows 0 mismatches against the r1 run in the deterministic fields: tr, valid_T, n_trim, m, acceptance, degenerate flags and all |ΔZ|.
  - Wall time was 1.00–1.10× r1, under machine load average 26–43 on 20 cores.
  - Full-cohort estimate (추정): 13.1 CPU-h for all units vs 12.5 in r1.
- Logs: `new_tests_r2.log` (53 passed), `old_suite_86_r2.log` (86 passed), `test_hashes_r2.txt`. The r1 logs are untouched.
