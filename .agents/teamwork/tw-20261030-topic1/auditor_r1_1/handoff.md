# auditor_r1_1 — Forensic Audit Report (Hard handoff)

**Work Product**: M1 — src/topic1_lagmotif/, tests/topic1_lagmotif/, scripts/topic1_timing.py, results/topic1/2026-10-30/, docs/03_empirical_analysis/topic1/
**Profile**: General Project. Integrity mode: none is stated in ORIGINAL_REQUEST.md, so Development (lenient) is inferred.
**Verdict**: CLEAN

## 1. Observation

Probes and logs are in /home/juke/git/00IITP-AI/verification/auditor_r1_1/. Artifact hashes are in tested_artifacts.sha256.

### Protected files and repository state
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gave 44/44 OK and rc=0, checked at the start, after the tests and at the end.
  - PRE_RUN_HASHES: 8/8 OK.
  - LAUNCH_HASHES: 4/5 OK. Only sentinel/BRIEFING.md differs. It is the sentinel's own mutable working file (mtime 20:30, after launch at 20:11), not a worker file.
- 00IITP-AI git:
  - branch is feature/topic1-lag-motif-v2; HEAD is e380802 (Mar 9);
  - the reflog shows only the checkout at 2026-10-30 20:09:54;
  - no commits, no stash.
  - The one tracked modification, docs/qa_prep_차지욱_20260309.md, is in PROTECTED_HASHES and matches, so it predates the run.
- enigma repo:
  - HEAD 0429816 (Oct 19); `.git/index` mtime is Oct 19, so the index was not rewritten.
  - The only files newer than ORIGINAL_REQUEST are experiments/.job_status and logs/coordinator.log. Both are written by a pre-existing `*/5` crontab entry (ic_coordinator.py).
  - The `.git` directory mtime changed at 21:17:39 (my own `git status`, which creates and removes index.lock) and again at 21:20 (consistent with another verifier's `git status`). Neither changed any content.
  - No __pycache__ or .pyc files were created after the run started.

### Tests
- The new suite gave 29 passed in 3.64 s, 0 skipped. The real-data TR-equality and positional tests actually ran.
- The old suite gave 86 passed, 7 warnings, in 261 s, rc=0. The box was loaded by concurrent verifiers; the worker's run took 62 s.
- No file outside the verifiers' own directories was written by the tests.

### Mutation probe (verification/auditor_r1_1/mutation_probe.py)
- The suite was run against private mirror copies, each with one defect injected.
- The control (no defect) passed 29/29. **All 16 defects were caught (rc=1):**

  | Injected defect | Tests failed |
  |---|---|
  | null allows reverse edge | 8 |
  | invariant checker facade (`return 0`) | 1 |
  | both of the above | 3 |
  | no resampling (lag in native samples) | 2 |
  | no detrend | 1 |
  | padding not stripped | 2 |
  | census 030C wrong | 6 |
  | orientation flipped | 2 |
  | Z sign flipped | 3 |
  | silent synthetic fallback for a missing subject | 1 |
  | rotation move disabled | 1 |
  | wrong TR table entry | 1 |
  | head trim in samples | 1 |
  | flow not antisymmetric | 1 |
  | null makes no moves | 8 |
  | 80-ROI subsample | 1 |

### Source code
- **No facades.**
  - The census is a real closed form and is checked against networkx.
  - The numba chain does real 2-swap and 3-rotation moves, with int64 invariant checks on every null.
  - The constant `return` values in motifs.py are error codes of a real checker.
- **No hardcoded results.**
  - Expected values in the tests are either derived (for example edge counts 2303, 4606 and 6908 = round(d·46,056)) or come from external oracles (networkx, enigma `repetition_time`).
  - The two `pytest.skip` calls are conditional, and neither fired.
- **No GPU, ssh, subprocess, network or git calls** in any new code.
- **No synthetic fallback.** The loader raises MissingSubjectError and InvalidSeriesError. Mutation M10, which adds a fallback, is caught.

### A3 timing re-run
- Command: `scripts/topic1_timing.py --outdir verification/auditor_r1_1/a3_rerun`. Load average was about 15–18 during the run and 9.8 after it.
- Positions were identical: [1578, 1228, 932, 0, 57]. I also derived them independently with enigma's `repetition_time` and sorted listdir. The cache subject order equals sorted listdir.
- **0 mismatches in any deterministic field**: m, acceptance, both degenerate flags, all three |ΔZ| diagnostics, tr, raw_valid_T, n_trim, valid_T, duration_s.
- Wall-time ratio, auditor to worker: 1.004–1.048.

  | Quantity | Worker | Auditor |
  |---|---|---|
  | mean unit time | 4.384 s | 4.477 s |
  | full cohort, all units (추정) | 12.47 CPU-h | 12.73 CPU-h |
  | peak RSS | 292.3 MB | 291.7 MB |
  | numba compile | 0.784 s | 0.836 s |

- The params sha256 equals 86863ffa…c15c6 in both runs and matches the recomputed `params_sha256()`.

### Spurious-direction re-run
- `python -m src.topic1_lagmotif.spurious --out verification/auditor_r1_1/spurious_rerun/…` reproduces all 42 result keys bit-identically.
- The numbers in the card and OPEN_ISSUES match the JSON. The "±" values are SE (sd/√12). OPEN_ISSUES labels them; the card's §9 does not.

### Analysis card
- sha256 is 1e589f0b…75aa, matching card_sha256.txt and OPEN_ISSUES. Mode is r--r--r--, mtime 21:12:10 KST.
- The §12 code hashes are 10/10 OK.
- PARAMS (pipeline.py, mtime 21:00:54) predates the spurious JSON (12:06:35Z) and the A3 run (12:06:45–12:10:06Z).

### Group-level results
- No group-level outcome result exists for any real-data feature. The card contains:
  - demographic and availability counts;
  - file-backed baselines, re-verified by me: 0.6512 ± 0.0318 (26 evaluated + 4 checkpoint_missing); 0.6606 ± 0.0262; 0.6420 ± 0.0125; LOSO mean 0.6519, median 0.6707, 23 sites;
  - the disclosed earlier v1 value (d = 0.08) from a pre-existing file.

### Data facts verified independently
- 1,706 on disk: OCD 869 / HC 837.
- 389 absent: 388 from TR > 2 s sites (with the exact per-site counts in the card) and 1 from Vancouver.
- 23 sites; TR counts as stated in the card.
- Y-BOCS non-null: 856 / 123.
- Medication in OCD: 203 / 212 / 447 / 7 NaN. In HC: 405 / 177 / 255 NaN.
- The medication coding conflict is confirmed at medication_confound_analysis.py:23 and site_driver_analysis.py:239.

### Participant-ID leakage
- I checked against the 2,095 metadata IDs plus the npy directory names (minimum length 16).
- 646 files scanned (production paths, the run metadata tree and all verification/ dirs): 0 hits, and 0 IDs in any filename.
- My own 32 files: 0 hits.

### Label × real-feature joins
- Probes that use labels are of two kinds:
  - counts only: explorer_survey_1/2 and reviewer_r1_1;
  - real design with simulated outcome and no imaging read: explorer_r1_3/probe_d_p_calibration (all 3 versions) and explorer_r1_1/p6.
- explorer_survey_2/probe_cohort.py compares scan duration (T, a data-quality covariate) between OCD and HC with a Mann–Whitney test. This is not a lag-motif endpoint.
- No lag-motif, flow or Z feature computed on real subjects was ever joined with diagnosis.

## 2. Logic Chain
1. The protected and pre-run hashes match, git shows no commits, and enigma content is unchanged (index untouched, only cron-written files changed). Therefore there were no writes to protected or external paths and no commit activity.
2. All tests pass, and 16/16 targeted defects make them fail, including the facade checker and the silent-fallback mutants. Therefore the tests can fail and are not self-certifying.
3. The source review found real algorithms with external oracles and no constant-return logic. Therefore there are no facades and no hardcoded results.
4. The A3 re-run reproduces every seeded deterministic field exactly, with wall time within 5%. The spurious JSON is bit-identical. Therefore the timing and characterization logs are genuine and reproducible, not fabricated.
5. The ID scan found 0 hits, and the timing outputs contain only computational keys. Therefore there is no ID leakage.
6. No real-feature × label contrast exists anywhere, and the card's numbers trace to source files. Therefore no group-level cohort result predates or contaminates the frozen card.
7. Under Development mode, none of the 🔴-flag patterns is observed. Therefore the verdict is CLEAN.

## 3. Caveats
- **Non-blocking.** Card §1 says "No diagnosis label was loaded in this run." This is true of the worker's code path (the A3 script and loader read only Unique_ID and Sample). For the run as a whole it is imprecise: the worker and the explorers read the OCD, Y-BOCS and Medication columns for counts, and explorer_survey_2 tested scan duration by group. None of this involves an endpoint, so the card's freeze claim stands. Suggest that future cards say "no label was joined with any real-data feature".
- **Non-blocking.** explorer_survey_1/probe_data_survey.py (survey stage, 20:16) fully read all 1,706 npy series for a NaN/zero-ROI QC scan, and 20 series for spectra. No features were extracted and no labels were joined. The survey dispatch had no subject cap, but this is wider than the "≤5 real subjects" rule given to iteration agents. Reported for the root's adjudication.
- **Non-blocking.** Card §9 reports "−0.38 ± 0.35" without saying it is an SE (the sd is 1.22). OPEN_ISSUES does label it as SE.
- **Non-blocking.** Card §12 hashes the code but not the test files; I hashed the tests here.
- **Non-blocking.** The test_defect_sensitivity.py fixtures re-create defects inside the test code rather than mutating production code. My mutation probe covers that gap.
- **Not investigated:** scientific validity (irreducibility of the null, adequacy of the density choice). That is reviewer and challenger scope.
- **Concurrent load:** other verifiers were running at the same time as my A3 re-run, which explains the slight slowdown and the slower old suite.
- **My DISPATCH.md** is not verbatim: it points to worker_r1/handoff.md for the embedded worker JSON instead of copying it. This is the same deviation as the worker's.
- I am a Claude Code subagent with no SendMessage available, so this structured return is my final report.

## 4. Conclusion
CLEAN. No integrity violation was found in M1. All forensic checks pass with direct evidence.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt          # 44 OK
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q   # 29 passed
/home/juke/superclaude-env/bin/python3 -B verification/auditor_r1_1/mutation_probe.py            # 16/16 mutants rc=1
/home/juke/superclaude-env/bin/python3 -B verification/auditor_r1_1/compare_a3.py                # 0 deterministic mismatches
sha256sum -c verification/auditor_r1_1/card_s12_hashes.txt                                       # 10 OK
sha256sum -c verification/auditor_r1_1/tested_artifacts.sha256                                  # artifacts unchanged since audit
```
Invalidation: any change to a hashed artifact, or a later real-data run that joins features with labels before a new card is frozen.
