# Handoff (Hard): worker_r2, run tw-20261030-topic1, M1, iteration 2

**Status: DONE.** I fixed the iteration-1 gate blocker (challenger_r1_1 REFUTED: A2 fail-on-defect was never exercised at the production entry point at TR ≠ 2.0) by adding tests only.

src/topic1_lagmotif/*, scripts/topic1_timing.py, the frozen card, OPEN_ISSUES.md and worker_r1's test files are all byte-identical to what the iteration-1 verifiers hashed.

## 1. Observation

**Start state.**
- At 12:57Z, `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gave 44 OK, rc=0.
- The card `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md` has sha256 `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`. That equals `results/topic1/2026-10-30/card_sha256.txt`. The file is mode r--r--r-- and its mtime is 21:12:10 KST.
- Card §12 block: `sha256sum -c` gave 10/10 OK.
- `params_sha256()` returned `86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6`.

**Root cause, confirmed in code.** `pipeline.py:66-69` `subject_flow` is correct. In iteration 1, every test that calls `subject_flow` or `NpyCohort.load` used a TR 2.0 site.

**Change: one new file.**
- `tests/topic1_lagmotif/test_production_entry_point.py` is a byte-for-byte copy of `verification/explorer_r2_3/proposed_tests/test_production_entry_point.py`.
- Its sha256 is `d1c287e08f0d998f46493dd90ab21dfba8ff9d384d5673790a8d61b2f420d04d`, the same as the source file and the entry in explorer_r2_3's SHA256SUMS.
- It holds 24 tests.

**New suite.** `results/topic1/2026-10-30/new_tests_r2.log`: 53 passed in 4.34 s, rc=0.

**Old suite.** `results/topic1/2026-10-30/old_suite_86_r2.log`: 86 passed, 7 warnings, in 108.96 s, rc=0. It ran while the machine was loaded.

**Production mutation check.**
- Harness: `verification/worker_r2/mutants.py`, my own adaptation; I did not run explorer_r2_3's harness in place.
- Results: `results/topic1/2026-10-30/mutation_check_r2.json`, with mirrors in `verification/worker_r2/mut/<mode>/<name>/pytest_out.txt`.
- Method:
  - There are 23 mutants. Each makes one or two exact textual edits to a mirror copy of the current src, and each edit must match exactly once.
  - Each mirror has an isolation guard: its conftest asserts that the imported package lives inside the mirror. No mirror tripped it.
  - Verdicts are parsed from the final pytest summary line.

| Mode | Control | Killed |
|---|---|---|
| full suite | 53 passed | 23 of 23 |
| old_only (new file removed from the mirror) | 29 passed | 3 of 23 |
| no_pin (`test_frozen_params_are_the_carded_params` deselected) | 52 passed | 23 of 23 |

- old_only kills only resample_ratio_coarse, resample_before_detrend and e2_sign_swapped.
- 20 mutants are killed only when the new file is present. They include every iteration-1 survivor:
  - pipeline_tr_ignored, pipeline_lag1_native_no_grid, lag_native_samples (the three blocking mutants);
  - lag_two_grid_samples, no_zscore, params_detrend_none, pipeline_ignores_detrend;
  - head_trim_in_samples, z_ddof0_no_nan, null_021C_missing_t;
  - chain_not_restarted, null_counts_raise_disabled.
- In no_pin, params_n_null_500 and params_density_primary_005 are killed only by the `params_sha256` assert inside the loader test, which is also a hash check. Every other mutant fails at least one behavioural or oracle test.

**A3 rerun.**
- Command: `scripts/topic1_timing.py --outdir results/topic1/2026-10-30/a3_r2`. `--outdir` is a required argument, and I gave a new directory, so the r1 files are untouched.
- Same positions as r1: [1578, 1228, 932, 0, 57].
- `verification/worker_r2/compare_a3.py` found 0 deterministic mismatches against r1 (tr, raw_valid_T, n_trim, valid_T, duration_s, m, acceptance, degenerate flags, all three |ΔZ| values). params_sha256 is equal.
- The nulls_s ratio r2/r1 was 1.00–1.10, under load average 42.7 at the start and 26.0 at the end, on 20 cores.

| Quantity | r2 | r1 |
|---|---|---|
| mean unit time | 4.61 s | 4.38 s |
| CPU-h, all units (추정) | 13.10 | 12.47 |
| CPU-h, primary unit (추정) | 2.39 | 2.27 |
| peak RSS | 287 MB | 292 MB |
| numba compile | 0.96 s | 0.78 s |

- Saved: `a3_r2/{a3_timing.json, a3_timing_raw.log, run_conditions_and_compare_r2.txt}`.

**Disclosures.** I wrote them to a NEW file, `docs/03_empirical_analysis/topic1/2026-10-30_OPEN_ISSUES_addendum_r2.md` (sha256 `edcecd69751ad210428b1dc40b9129436830e3bda6ee27ff7e1c2c678893a3b9`, 0 control characters). OPEN_ISSUES.md still has sha `23ca…e5d2`.
- I read `abs_dZ030T_factor` 0.909 at position 57 and 0.455 at position 1228 directly from the r1 a3_timing.json.
- pipeline.py has mtime 21:00:54 and spurious_direction.json 21:06:35 (stat).
- HANDOFF.md:21 reads 0.628 (grep).

**Hashes.** `results/topic1/2026-10-30/test_hashes_r2.txt` lists all 8 test files. The 7 worker_r1 test files match the reviewer_r1_2 hashes. The file also covers the r2 result files.

**r1 results untouched.** The 7 r1 result files and scripts/topic1_timing.py pass `sha256sum -c` against the hashes reviewer_r1_2 recorded.

**Final checks.**
- Protected hashes: 44 OK, rc=0 (`verification/worker_r2/protected_final.log`).
- ID scan (count only): 2,095 IDs, 1,435 files, 0 content hits and 0 filename hits (`verification/worker_r2/id_scan.log`).
- No __pycache__, .pyc or .pytest_cache files newer than my start in src, tests, verification/worker_r2, results/topic1 or enigma.
- audit_layout.py on the run root: 72 files, findings [].

**prev_snapshot.** No existing test or probe was changed (only a new test file was added), so `verification/worker_r2/prev_snapshot/` was not needed and does not exist.

**Metadata.** The harness accepted every write: DISPATCH.md, BRIEFING.md, progress.md and handoff.md. DISPATCH.md holds the dispatch verbatim (204,294 chars), extracted by script from my own transcript `subagents/workflows/wf_81aa0128-bbf/agent-a22579d271f5362e2.jsonl`. Its sha256 and length are recorded inside the file.

## 2. Logic chain

1. The gate failed on a single blocker, test coverage at the entry point. Production is correct: challenger_r1_1 P5 and challenger_r1_2 P2 both found it correct at all 7 TRs. So the fix belongs in the tests.
2. **Why a verbatim copy of r2_3 instead of a merge of the three proposals.**
   - Explorer mutation evidence is bound to exact bytes; a merged file would have been unprobed.
   - r2_3's file is the only one that:
     - discriminates a 2 s lead from a 4 s lead behaviourally, which catches lag doubling without relying on the oracle;
     - runs the spec oracle at all 7 TRs;
     - covers the raise path.
   - I then re-proved its kill power myself against the file as installed. That proof is the full-mode row of the mutation table.
3. A2's requirement that tests "would FAIL on the defect they target" is now shown with defects placed in production code, not simulated inside tests:
   - old_only reproduces the iteration-1 survivors: 20/23 survive.
   - full mode kills 23/23.
   - no_pin shows the kills do not depend on the PARAMS pin, except for two pure config-value mutants.
4. src/ and scripts/ are unchanged, so the card's §12 hashes (10/10) and params_sha256 still hold. The freeze order PARAMS → A3 → card is intact, so the card needs no re-freeze. The A3 rerun reproduces r1 exactly in every deterministic field.
5. A1, A3, A4 and A6 were already approved by 4 of 5 verifiers on these same bytes. The A5 evidence (old suite 86, protected 44/44, no bytecode, no IDs) is refreshed. A6 gains the addendum.

## 3. Caveats

- The 23 hand-written mutants are not exhaustive. spurious.py, synthetic.py and the timing script were not mutation-tested.
- The copied file asserts `max|F| <= 1.0` with a comment saying this bound is general. The only general bound is 2T/(T−1). The assertion holds for its seeded fixture, and I kept it unchanged to stay byte-bound (addendum item 28).
- Time reversal is still not tested end-to-end through `subject_flow` (addendum item 29).
- The oracle reuses the scipy primitives `detrend` and `resample_poly`, so a defect shared with scipy would pass.
- A3 wall times were measured under heavy machine load from other users. My mutation harness ran concurrently, one pytest process at a time. Absolute seconds are about 5% above r1.
- Two config-only mutants are killed only by hash checks.
- I did not re-verify the card's data facts (cohort counts, baselines). Four r1 verifiers did.
- The cohort statistics script still does not exist. Step 5 is not authorized and was not run.

## 4. Conclusion

M1 iteration 2 is ready for independent review:
- the blocking A2 entry-point gap is closed, with evidence from defects placed in production;
- A1–A6 evidence is refreshed;
- the frozen card is unchanged and still valid.

The card path and sha are as stated in §1 (unchanged; not re-written).

## 5. Verification method

- New suite: `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider tests/topic1_lagmotif -q` → 53 passed.
- Old suite: `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 STRICT_E2E=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` → 86 passed.
- Protected hashes: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` → rc 0.
- Card: `sha256sum <card>` should give 1e589f0b…75aa. `awk '/^```/{f=!f;next} f' <card> | grep -E '^[0-9a-f]{64}  ' | LC_ALL=C sha256sum -c` should give 10/10.
- Test bytes: `cmp tests/topic1_lagmotif/test_production_entry_point.py verification/explorer_r2_3/proposed_tests/test_production_entry_point.py`.
- Mutation check: copy `verification/worker_r2/mutants.py` to your own identity directory and change `HERE`, since it rebuilds `HERE/mut`. Then run `python -B mutants.py <out.json> full old_only no_pin`. Expect:
  - full: 23/23 killed, control 53 passed;
  - old_only: 3/23 killed, control 29 passed;
  - no_pin: 23/23 killed.
- A3 determinism: `python -B verification/worker_r2/compare_a3.py results/topic1/2026-10-30/a3_timing.json results/topic1/2026-10-30/a3_r2/a3_timing.json` → 0 mismatches.
- These results are invalidated by any edit to src/topic1_lagmotif, scripts/topic1_timing.py, the card or tests/topic1_lagmotif/*.
