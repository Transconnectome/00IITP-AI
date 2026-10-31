# Hard handoff: reviewer_r2_2, run tw-20261030-topic1, M1 iteration 2

**Verdict: APPROVE.** A1–A6 are each met, with evidence I produced myself. There are no blocking issues. The non-blocking items are listed in §4.

## 1. Observation

All times are UTC on 2026-10-30. Probe directory: `/home/juke/git/00IITP-AI/verification/reviewer_r2_2/`.

**Protected files**
- `sha256sum -c sentinel/PROTECTED_HASHES.txt` gave 44 OK, rc 0, at the start (`protected_start.log`) and again after all my runs (`protected_final.log`).
- Branch: `feature/topic1-lag-motif-v2`.

**New suite.** Command: `PYTHONDONTWRITEBYTECODE=1 OPENBLAS/OMP/MKL=1 python3 -B -m pytest -p no:cacheprovider tests/topic1_lagmotif -q`.
- Result: 53 passed in 9.57 s, rc 0 (`new_tests.log`).

**Old suite.** Command: `PYTHONDONTWRITEBYTECODE=1 STRICT_E2E=1 PYTHONPATH=. python3 -B -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q`.
- Result: 86 passed, 7 warnings, in 134.49 s, rc 0 (`old_suite_86.log`).

**Copy fidelity.** `cmp tests/topic1_lagmotif/test_production_entry_point.py verification/explorer_r2_3/proposed_tests/test_production_entry_point.py` reports the files identical. sha256 `d1c287e0…0d04d`.

**Card**
- sha256 `1e589f0b…75aa` matches `card_sha256.txt`.
- The §12 code-hash block passes 10/10, both at the start and after my runs.
- `params_sha256` is pinned by a test that passes.

**Card facts, re-derived from files** (`card_facts.py`/`.log`, counts only)
- Population: 1,706 npy directories against 2,095 metadata rows; 23 sites on disk; dx 1:869 and 2:837.
- TR counts: 0.7: 43, 0.8: 96, 0.85: 104, 1.0: 119, 1.73: 39, 1.8: 110, 2.0: 1,195.
- Absent rows: Seoul 95, Chiba-CHBSRPB 89, Shanghai 84, Chiba-CHBC 53, Chiba-CHB 42, Kyoto1.5T 25 (388 in total), plus Vancouver 1.
- Clinical columns:
  - No motion-like column exists.
  - Y-BOCS is non-null in 856 code-1 and 123 code-2 subjects.
  - Medication: OCD {3: 447, 2: 212, 1: 203, NaN: 7}; HC {1: 405, NaN: 255, 2: 177}.
- Baselines, re-aggregated from the enigma CSVs:
  - `table1` baseline: 26 evaluated rows plus 4 `checkpoint_missing`; 0.6512 ± 0.0318; N_test 255.
  - `track_b`: Remediated_Baseline 0.6606 ± 0.0262; Linear_SVM_static_FC 0.6420 ± 0.0125.
  - `site_driver_analysis.csv` `auroc_scratch_mean`: mean 0.6519, median 0.6707, N_total-weighted 0.6477, 23 sites.
- Citation lines checked with read-only `grep`/`sed`:
  - `medication_confound_analysis.py:22` gives OCD 1/2, and `:23` gives medication 1 = medicated.
  - `site_driver_analysis.py:235` gives OCD, `:237` gives sex 1 = male, and `:239` gives medication 1 = drug-free.
  - `site_driver_analysis.py:160` begins the hard-coded LOSO dict.
  - enigma `HANDOFF.md:21` gives 0.6285 for medicated OCD vs HC.
  - `time_series_utils.py:5-79` holds `repetition_time`.
- Every number and citation I checked matches the card, OPEN_ISSUES and the addendum.

**Code read in full:** `tr_table`, `data`, `preprocess`, `flow`, `motifs`, `pipeline`, `spurious`, `synthetic`, `scripts/topic1_timing.py` and all 8 test files.
- The F convention (F[i,j] > 0 means i leads j) is correct.
- The Hodge potential p = row-mean of F is the least-squares potential on K_N.
- In the 2-swap, a new edge is rejected if it exists in either direction (motifs.py:75), and the rotation move preserves degrees.
- `_count_030` agrees with the closed form.
- Z is NaN when sd = 0.
- The loader raises `MissingSubjectError` and uses `from None`, so no path is chained into the error.
- I found no fallback.

**My own mutation harness**
- Files: `mutants_rv.py` (sha256 `f3b9eb60…a9eb`), a copy of `verification/worker_r2/mutants.py` with HERE set to my directory. Result: `mutation_rv.json` (sha256 `835720ce…a9eb`).
- Mutant set: the worker's 23 plus 16 new independent `rv_*` mutants.
  - Null: allow mutual edges; disable rotation.
  - Orientation: reversed graph orientation; F sign flipped.
  - Data contract: no trailing-zero strip; floor instead of ceil trim; synthetic fallback for a missing file; interior zero row accepted.
  - TR: loader TR fixed at 2.0; TR > 2 cap off.
  - Graph and census: Hodge potential from column mean; 030C without /3; top-k keeps the weakest pairs.
  - Statistics and resampling: degenerate flag off; FFT resample; seeds ignore position.
- Every mirror kept the isolation guard intact (`isolation_broken` false everywhere).

| Mode | Control | Killed | Survivors |
|---|---|---|---|
| full | 53 passed | 38/39 | `rv_seed_ignores_position` |
| old_only | 29 passed | 16/39 | 23, listed in the JSON |

- On the worker's 23 mutants in old_only, the killed set is exactly {e2_sign_swapped, resample_before_detrend, resample_ratio_coarse}. That reproduces the worker's 3/23, so the iteration-1 gap was real and is now closed.
- The `failed_tests` for `rv_missing_fallback`, `rv_null_allows_mutual` and `rv_no_trailing_strip` name the targeted fixtures.

**Probe `probe_reversal_and_tr.py` / `.log`** (synthetic only; through `prepare_series` → `subject_flow` at all 7 TRs; 3 seeds)
- Time reversal: corr(Fr, −F) ≥ 0.99998, and max |Fr + F| = 5e-15 at TR 2.0.
- 2 s pairs: the F ratio to TR 2.0 lies in 0.994–1.007, and orientation is correct at every TR.
- Each 2 s lead is more than 2× the 4 s lead.
- max |F| is 1.071–1.073 at every TR.

**A3 outputs**
- Ran `verification/worker_r2/compare_a3.py` on the r1 and r2 JSONs and read both files.
- Same positions [1578, 1228, 932, 0, 57] at TRs [0.7, 0.85, 1.0, 1.8, 2.0]; the same params sha.
- Per-unit time, peak RSS and CPU-h are all labelled 추정.
- The deterministic fields are identical between r1 and r2.
- r1 summary: mean unit 4.38 s, 12.47 CPU-h for all units, 2.27 CPU-h for the primary unit only, RSS 292 MB.

**Privacy and bytecode**
- Count-only ID scan (`id_scan.py`/`.log`) over src, tests, the script, results/topic1, docs/topic1, verification/{reviewer_r2_2, worker_r2 including mut/} and the worker_r2 and reviewer_r2_2 metadata: 2,095 IDs in memory, 3,040 files, 0 content hits, 0 filename hits.
- `find` found 0 `__pycache__`, `.pyc` or `.pytest_cache` entries newer than my start in src, tests, scripts, results/topic1 or the enigma repo.
- `audit_layout.py` on the run root: 84 files, findings [].

## 2. Logic Chain

**A1 (loader and extractor) is met.**
- The production code implements every requirement:
  - only the valid portion, with valid_T reported;
  - lag fixed at 2 s on a 2 s grid with exact resample ratios;
  - all 304 ROIs;
  - an oriented, degree-preserving null with invariants checked on every null;
  - SP over the 5 oriented classes, with the restriction documented;
  - read-only npy access;
  - an explicit error, not a fallback, for a missing subject.
- Tests support each point. Mutants that break any of these (fallback, padding, mutual-edge null, TR wiring) are killed.

**A2 (fixtures pass and fail on their defects) is met.**
- All six A2 bullets have passing fixtures.
- "Would FAIL on defect" is now shown for defects placed in the production code itself, through the production entry point at TR ≠ 2.0. This was the iteration-1 blocker.
- It is reproduced independently: old_only reproduces 3/23 exactly, and full kills all 23 worker mutants plus 15 of my 16 independent ones.
- The spurious-direction bullet is satisfied by quantification plus an explicit limitation (OPEN_ISSUES item 12), which ACCEPTANCE allows.
- The one survivor, seed independence, is not an A2 target.

**A3 (timing) is met.**
- Five real subjects, 1 thread, n_null 1,000.
- Reported: per-unit time for each channel × density, peak RSS, and extrapolated CPU-h labelled 추정.
- The raw log exists, and the output carries positional indices only.

**A4 (frozen card) is met.**
- Every listed element is present and file-backed, and the card's sha256 is recorded in two places.
- The "≈0.63" baseline is correctly replaced by file-verified values, which I reproduced.
- The card's freeze time (12:12Z) is after A3 (12:10Z) and before any cohort result. No cohort script exists.

**A5 (safety) is met.** 86 passed; 44/44 protected files OK after my runs; no bytecode; 0 ID hits. No GPU, ssh or git writes are evident from the worker's artifacts or from mine.

**A6 (open issues) is met.** OPEN_ISSUES records the report-vs-JSON discrepancy (item 1) and 23 further issues. The addendum adds 25–39.

**Integrity.** I found no hard-coded results and no facade:
- the oracle is an independent re-implementation of the spec;
- the mutation evidence reproduces under my own harness;
- the worker's JSON production hashes match the current files.

## 3. Caveats
- I did not re-run the A3 timing on real subjects, because of the ≤ 5-subject rule. I verified A3 from the JSON and logs and with `compare_a3`.
- I did not re-run the worker's no_pin mode. It concerns only 2 config-value mutants.
- I ran a plain `git -C /home/juke/git/enigma_ocd_mbbn status`, which may have refreshed that repo's `.git/index` stat cache. That is the only possible write by a reviewer. No tracked content changed.
- enigma `logs/coordinator.log` and `experiments/.job_status` have mtimes after my start. They come from another process, not from this run's code.
- Other iteration-2 verifiers ran concurrently, so my timings were measured under load.
- The 39 mutants are hand-written and not exhaustive.
- Mixing adequacy on real graphs is not established. It is disclosed in addendum items 30–32.

## 4. Conclusion
**APPROVE M1 iteration 2.** None of the following blocks:

1. **No test checks the null seeds.** `rv_seed_ignores_position` survives, so nothing checks that the seeds vary by position, channel or density as card §11 specifies.
   - Recommendation: add a seed-rule test before the cohort run.
2. **The `max|F| <= 1.0` assertion holds only for its seed.** The assertion in `test_flow_is_invariant_to_offset_scale_and_linear_drift_at_tr_07` passes only for that seeded fixture. My probe measured 1.073, and the general bound is 2T/(T−1). See addendum item 28.
3. **No time-reversal fixture runs through `subject_flow`.** My probe closes this empirically (corr ≥ 0.99998, exact at TR 2.0). See addendum item 29.
4. **Mixing statistics overstate or fall short of real moves.**
   - Acceptance counts no-op moves.
   - The mixing budget is set in attempts, not accepted moves.
   - |ΔZ030T| for factor 40 vs 20 is up to 0.909.
   - All three are disclosed in addendum items 30–32.
5. **E2 is biased under AR mismatch** (about −1.2), and no fixture asserts E2 calibration (item 38).
6. **Two config-only mutants are caught only by the hash pin.**
7. **Short series are allowed.** The minimum is 20 native samples, about 7 grid samples (item 36).
8. **The cohort script and step 5 remain unauthorized and unwritten.**

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` → expect 44 OK.
- New suite command as in §1 → expect 53 passed. Old suite command as in §1 → expect 86 passed.
- `awk '/^```/{f=!f;next} f' docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md | grep -E '^[0-9a-f]{64}  ' | LC_ALL=C sha256sum -c` → expect 10/10.
- `python3 -B verification/reviewer_r2_2/mutants_rv.py <out.json> full old_only` → expect 38/39 in full (only `rv_seed_ignores_position` survives) and 16/39 in old_only.
  - Note: the script rebuilds `verification/reviewer_r2_2/mut`. Copy it and change HERE first.
- `python3 -B verification/reviewer_r2_2/probe_reversal_and_tr.py` (synthetic).
- The verdict is invalidated by any edit to `src/topic1_lagmotif/*`, `scripts/topic1_timing.py`, `tests/topic1_lagmotif/*` or the card.
