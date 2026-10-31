# Handoff (Hard): worker_r1, run tw-20261030-topic1, M1

## 1. Observation

**Files created.** All are new; none existed before this run.
- src/topic1_lagmotif/: __init__.py, tr_table.py, data.py, preprocess.py, flow.py, motifs.py, pipeline.py, synthetic.py, spurious.py
- tests/topic1_lagmotif/: __init__.py, conftest_helpers.py (a plain helper module, not a pytest conftest), test_tr_and_loader.py, test_flow_chain.py, test_null_and_census.py, test_synthetic_ground_truth.py, test_defect_sensitivity.py
- scripts/topic1_timing.py
- results/topic1/2026-10-30/: a3_timing.json, a3_timing_raw.log, spurious_direction.json, card_sha256.txt, old_suite_86.log, old_suite_86_final.log, new_tests.log
- docs/03_empirical_analysis/topic1/: 2026-10-30_topic1_analysis_card.md (read-only, sha256 1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa), 2026-10-30_OPEN_ISSUES.md

**Tests.**
- New suite: `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m pytest -p no:cacheprovider tests/topic1_lagmotif -q` → 29 passed in 4.44 s.
- Old suite: `PYTHONDONTWRITEBYTECODE=1 STRICT_E2E=1 PYTHONPATH=... python -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` → 86 passed, 7 warnings (61.6 s, then 62.7 s at the end).
- Protected hashes: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` → rc=0, 44/44 OK.

**Verified data facts** (aggregates only, 2026-10-30):
- 1,706 directories, each holding one file named <dir>.npy; all 1,706 match metadata Unique_ID.
- OCD 1: 869 / 2: 837.
- Sex: 1 = 819, 2 = 887. By diagnosis, sex1: 393 OCD / 426 HC and sex2: 476 OCD / 411 HC.
- Y-BOCS non-null: 856 in code 1, 123 in code 2.
- Medication within OCD: 203 (code 1) / 212 (code 2) / 447 (code 3) / 7 NaN. HC: 405 / 177 / 255 NaN.
- Absent subjects: 389 = 388 from TR>2 sites + 1 Vancouver.
- TR counts: 0.7: 43, 0.8: 96, 0.85: 104, 1.0: 119, 1.73: 39, 1.8: 110, 2.0: 1,195.
- Baselines:
  - table1 baseline: 0.6512 ± 0.0318, 26 evaluated + 4 checkpoint_missing.
  - track_b: Remediated_Baseline 0.6606 ± 0.0262, Linear_SVM_static_FC 0.6420 ± 0.0125.
  - site_driver_analysis.csv: mean 0.6519, N-weighted 0.6477, median 0.6707.

**New finding: the medication coding is contradictory.**
- medication_confound_analysis.py:23 says 1 = medicated, 2 = unmedicated.
- site_driver_analysis.py:239 says 1 = drug-free, 2 = medicated.

**A3 timing**, 5 positional subjects [1578, 1228, 932, 0, 57] at TRs 0.7, 0.85, 1.0, 1.8 and 2.0:
- Mean unit cost (1 channel × 1 density, 1,000 nulls, 20·m attempts) is 4.38 s. By density: 2.4 s at 5%, 4.8 s at 10%, 5.9 s at 15%.
- Mean per subject for all 6 units: 26.3 s. Load + preprocess: about 0.01 s.
- Peak RSS 292 MB; numba compile 0.78 s.
- Extrapolations (추정): 12.5 CPU-h for all units; 2.3 CPU-h for the primary unit only.
- Subject 1578 had a degenerate null at 5% and an acceptance rate of 0.074.
- |ΔZ030C| between factor 40 and factor 20: 0.04–0.33.

**Spurious-direction characterization** (spurious_direction.json; values at 10%, mean ± SE):
- AR φ mismatch: Z030C −0.38 ± 0.35, Z030T +0.82.
- Latency SD 1 s: Z030T −7.57, E2 +7.26; curl Z030C −5.09.
- Latency SD 2 s: Z030C −1.86, E2 +6.91.
- Planted cycles: +9.63 ± 0.22; white control: +0.24 ± 0.27.

**Privacy.** A programmatic scan of all new code and results for the 1,706 directory names found 0 hits. No .pyc files were written into enigma or into the new directories.

## 2. Logic chain

**A1 (extractor).**
- The loader is positional and read-only (`np.load(mmap_mode='r')`, then copied).
- It strips trailing zero rows, raises on interior zero rows, NaN or zero-variance ROIs, and trims ceil(40 s/TR) samples. It returns valid_T and duration_s.
- Missing subjects raise `MissingSubjectError("position i ...")` for a missing file, an out-of-range index or a missing metadata row. Tests assert that the fake ID is absent from the message. There is no fallback.
- The lag is 2 s on a common 2.0 s grid: detrend, then resample_poly with exact ratios and padtype='line'. All 304 ROIs are used.
- The graph uses exact top-k.
- The null preserves in/out degrees, rejects new edges that exist in either direction or are self-loops, and has invariants asserted on every null.
- SP is restricted to the 5 oriented connected classes; this is documented in the motifs.py docstring.

**A2 (fixtures).** Each fixture passes, and test_defect_sensitivity / the v1-swap test show that it fails on its target defect.
- Injection: mean Z030C > 4, control |mean| < 1, and per-seed min(injected) > max(control) + 1.
- Time reversal: exact to 1e-10 at TR 2; corr > 0.999 at TR 0.7 and 1.73.
- Null invariants: 40 nulls checked, plus the checker catches mutual edges from a v1-style swap.
- Padding: identical F through the loader.
- Two-TR: |F| ratio in [0.85, 1.15], with matching signs. The lag-in-samples defect falls outside that range.
- AR calibration: within tolerance.
- Latency bias: characterized and reported as a limitation.
- Further tests: rotation reachability (2-swap alone cannot reach the reversed triangle) and χ² uniformity on a fully enumerated N=5 class.

**A3.** Timing ran on 5 subjects, with a raw log and JSON. No IDs, no diagnosis labels and no feature values were recorded.

**A4.** The card was frozen after A3. PARAMS (sha 86863ffa…) was fixed before A3, and nothing in PARAMS was changed afterwards. The card holds no cohort result.

**A5.** Old 86 tests pass, protected hashes are OK, and there were no external writes or git operations.

**A6.** OPEN_ISSUES lists 24 items.

## 3. Caveats

- **Primary density 10% is my choice and deviates from PROJECT.md's 15%.** The justification is synthetic only (explorer r1_1 dilution and degeneracy evidence; advisor concurred). It is documented in the card and in pipeline.py.
- **n_null 1,000 and factor 20** follow explorers r1_2 and r1_3. Explorer r1_1 suggested 200 nulls and 30·m.
- **The move set is 2-swap + 3-edge rotation**, as proposed by r1_2. Rotation includes triangle reversal and the path move. Irreducibility is not proven.
- **The old-suite command was run with PYTHONDONTWRITEBYTECODE=1 and -p no:cacheprovider added** (hygiene), not exactly as dispatched.
- **The A3 diagnostic kept |ΔZ| values** (differences, not feature values). Feature values were computed during timing but never logged.
- **The cohort statistics script (LMM/permutation/LOSO) is not implemented**; it is out of scope for steps 1–4. The card defines it.
- **DISPATCH.md is not fully verbatim.** The explorer JSON was not re-copied (disclosed inside the file).
- **Not done:** the survey-3 prototype was not re-run, and the failing tests were not re-run against v1 itself. The defects were re-created inside the tests instead.
- **The advisor was rate-limited at the final check**, so the card was frozen without a second review.

## 4. Conclusion

M1 deliverables for A1–A6 exist and pass their tests. This is ready for independent review and verification. The card is frozen; any change needs a new dated card.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q        # 29 passed
PYTHONDONTWRITEBYTECODE=1 STRICT_E2E=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q   # 86 passed
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt   # rc 0
sha256sum docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md            # 1e589f0b...75aa
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 scripts/topic1_timing.py --outdir <new dir>   # re-time the same 5 subjects (about 3.5 min)
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -m src.topic1_lagmotif.spurious --out <new file> --n-seeds 12 --n-null 300
```

These conclusions are invalidated by any of the following: a code hash differing from card §12; a test failing on rerun; IDs found in results; or a re-timing that differs by more than 2× (machine load).
