# Forensic Audit Report — auditor_r2_1 (run tw-20261030-topic1, M1 iteration 2)

**Work Product**: src/topic1_lagmotif/, tests/topic1_lagmotif/ (8 files incl. new test_production_entry_point.py),
scripts/topic1_timing.py, results/topic1/2026-10-30/, docs/03_empirical_analysis/topic1/
**Profile**: General Project. Integrity mode read from ORIGINAL_REQUEST.md: no "from scratch" or "do not delegate" constraint,
so Development Mode applies. In addition, the run's hard constraints (A5 and the dispatch) were audited as violation classes.
**Verdict**: CLEAN

## Phase results
1. Hardcoded output detection: PASS.
   - All 9 src modules and the timing script were read in full. No literal expected outputs, no PASS strings, no constant returns.
   - The census is closed form. I checked it by hand: each 030T has exactly one out-star pair and one 2-path; each 030C has three 2-paths.
   - The census is tested against networkx.triadic_census at N = 30, 60, 120 and 304. My mutant A_census_030C_div2 is killed (6 failed).
   - The constants in tests are spec values: card §1 ratios and n_trim, and the PARAMS sha pin. The pin is declared, and the
     no_pin mode shows that behavioural tests carry the kills.
2. Facade detection: PASS.
   - Every function performs real computation: loader, valid portion, detrend/resample/zscore, lagged net flow, top-k orientation,
     the numba null chain with a per-null invariant checker, Z/SP, and Hodge decomposition.
   - No NotImplementedError and no delegation to a reference implementation.
3. Pre-populated or fabricated artifacts: PASS. Each artifact was corroborated by re-execution, not by timestamps.
   - The A3 timing re-run on the same 5 positions [1578, 1228, 932, 0, 57] gives 0 deterministic mismatches against r1 and
     against r2: tr, raw_valid_T, n_trim, valid_T, duration_s, m, acceptance, degenerate flags, all |dZ| values.
   - Wall-time ratio mine/r1 is 1.00–1.04, and mine/r2 is 0.91–1.04. Estimated CPU-h for all units: mine 12.55 (추정), r1 12.47, r2 13.10.
   - spurious_direction.json: 3 keys re-run (ar_mismatch@0.10, latency_sd_1s@0.10, planted_cycles_20_g0.8@0.05/curl). Means and
     degenerate counts are identical to 6 decimals.
   - mutation_check_r2.json: per-mutant pytest_out.txt files exist for all 23 mutants plus a control in 3 modes, and they match the
     JSON (full 23/23, old_only 3/23, no_pin 23/23).
   - My own mirror harness, of independent design, killed 11/11 mutants (control 53 passed, no isolation breach):
     - re-runs of worker mutants: W_pipeline_tr_ignored (9 failed), W_lag_native_samples (7 failed), W_no_zscore (8 failed);
     - new mutants: A_flow_sign_flipped (13), A_null_allows_reversed_edge (10), A_topk_smallest (4), A_padding_not_stripped (8),
       A_silent_synthetic_fallback (1), A_census_030C_div2 (6), A_rotation_disabled (1), A_z_over_variance (3).
   - Lead noted: the src files were all written within about 3 minutes (20:58–21:01). They are corroborated as genuine by the
     re-execution and mutation results above, so this is not evidence of copying.
4. Build and run: PASS. New suite: 53 passed in 8.57 s. Old suite: 86 passed, 7 warnings, in 229 s (rc 0, load average about 38).
   A pre/post file snapshot shows that neither suite wrote any file outside verification/; the only changes were other agents' metadata.
   test_tr_and_loader.py has pytest.skip branches for an absent enigma repo or absent data. The run reports 53 passed and 0 skipped,
   so the real-data TR-table and loader tests actually executed and are not tests that cannot fail.
5. Output verification: PASS.
   - The new test file is byte-identical to verification/explorer_r2_3/proposed_tests/ (sha d1c287e0…).
   - Its oracle does not import PARAMS or production helpers.
   - test_hashes_r2.txt: 14/14 OK.
6. Dependency audit: not applicable in Development Mode. scipy, numpy, numba and networkx are auxiliary; networkx is used only as a test oracle.

## Run-constraint checks
- Protected files: `sha256sum -c PROTECTED_HASHES.txt` gives 44 OK, rc 0, at both the start and the end of my audit.
  - The protected list omits the pre-existing docs/03_empirical_analysis/*.md and json files. Their mtimes (15:50–19:08) all
    predate the run start (20:09), and none of them changed.
  - The one tracked `M` file (docs/qa_prep_…) has an mtime of 2026-03-09 and its protected hash matches.
- Git: HEAD is e380802; the last reflog entry is the 20:09 checkout to the feature branch. There are no commits since and 0 stashes.
- External repo (enigma_ocd_mbbn, read-only inspection):
  - The only files newer than the run start are logs/coordinator.log and experiments/.job_status. Both are written by a
    pre-existing cron coordinator, which has logged "IC Loss Progress" 122,745 times since March. Unrelated to this run.
  - Its `M HANDOFF.md` has an mtime of 10-21. Its .pytest_cache is from 19:23, before the run.
  - No npy file has been modified, and no __pycache__ appears after 20:09.
- Bytecode: no __pycache__, .pyc or .pytest_cache newer than 20:09 in src, tests, scripts, results, docs or enigma.
- Silent synthetic fallback: none. data.NpyCohort.load raises MissingSubjectError (position-only message) when the file is
  missing, unreadable, or has no metadata row. My fallback mutant is caught by test_missing_subject_raises_without_participant_id.
- Participant IDs: own count-only scanner, 2,095 IDs (metadata ∪ npy dir names; minimum length 16).
  - 7,510 files scanned across src/topic1_lagmotif, tests/topic1_lagmotif, results/topic1, docs/…/topic1, all of verification/
    and the run metadata tree.
  - 0 content hits, 0 filename hits.
- Group-level cohort result: none present.
  - The results files contain only computational quantities by position.
  - The card contains:
    - the disclosed v1 prior result (d = 0.0804, p = 0.757, AUROC 0.4756), verified in empirical_results.json;
    - file-backed baselines (0.6512 ± 0.0318, n = 26), verified in table1_true_test_performance.csv.
  - The only code that reads diagnosis columns:
    - reviewer_r1_1/baselines_counts_probe.py: cohort counts;
    - explorer_r1_3/probe_d_p_calibration.py: the real design with a SIMULATED outcome and no imaging data;
    - explorer_survey_1/probe_data_survey.py: demographic counts.
  - No label is joined with any lag-motif feature.
  - The addendum's numbers are timing diagnostics (|dZ| of 0.909 at position 57 and 0.455 at 1228, acceptance 0.074 at 1578,
    all reproduced by my re-run) or synthetic values (6.14/4.48/3.52).
- GPU, remote and commit activity:
  - The run code (src, tests, scripts, all of verification/ except mutant mirrors) has no torch, cupy, cuda, sbatch, srun, ssh or
    git-write call. numba is CPU-only `@njit(cache=False)`.
  - nvidia-smi shows 0 compute processes now.
  - Historical GPU or ssh use cannot be observed after the fact. That limitation is stated, not a finding.
- Full-cohort run: none of the topic1 extractor. The A3 run was 5 subjects, and my re-run used the same 5.

## Non-blocking observations
1. The survey-stage probe explorer_survey_1/probe_data_survey.py:54 (written 20:16) loaded all 1,706 npy series.
   - What it did: data-contract QC (lengths, NaN, all-zero ROIs) plus demographic counts. No feature was extracted and no label
     was joined with a feature.
   - Dispatch evidence: I checked explorer_survey_{1,2,3}/DISPATCH.md (20:12). None of them carries a subject cap. Their hard
     constraints are "read-only everywhere …, No GPU, no ssh/Slurm, no git commit/push, no network uploads. Never print
     participant IDs". There is no "5 real subjects" or "full-cohort" term.
   - Relation to A5: ACCEPTANCE.md A5 (20:11) says "no full-cohort run". Read plainly, that means the analysis run deferred as
     step 5, and a contract QC read without feature extraction is not that run.
   - Not a breach by worker_r2. The root may adjudicate.
2. File access times cannot show which real subjects were read during this run. The filesystem is mounted relatime, and all
   1,706 npy atimes are 10-29 23:37–23:39.
3. The protected list does not cover the pre-existing docs/03_empirical_analysis files. I verified them by mtime only, and no
   baseline hash exists for them.
4. reviewer_r1_2's r1 result hashes are recorded only in abbreviated form, so I could not run a full `sha256sum -c` against them.
   Corroboration: all r1 result-file mtimes (21:06–21:14) predate worker_r2's start, and my re-run reproduces a3_timing.json exactly.
5. Methodological caveats the worker already disclosed (not integrity issues):
   - acceptance counts 2-swap no-ops;
   - the max|F| <= 1 comment;
   - the oracle shares scipy primitives with production;
   - irreducibility of the null move set is not established;
   - spurious.py, synthetic.py and the timing script are not mutation-tested.

## Commands run (key)
- `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt`: 44 OK, rc 0 (start and end).
- Card: `sha256sum` gives 1e589f0b…75aa; `awk … | sha256sum -c` on its §12 block gives 10/10 OK.
- `sha256sum -c results/topic1/2026-10-30/test_hashes_r2.txt`: 14/14 OK. `cmp` new test vs explorer_r2_3 copy: identical.
- New suite (`pytest tests/topic1_lagmotif -q`, -B, no cacheprovider, BLAS 1 thread): 53 passed in 8.57 s.
- Old suite (STRICT_E2E=1, the three paths): 86 passed, 7 warnings, in 229.35 s, rc 0.
- `verification/auditor_r2_1/audit_mutants.py`: 11/11 killed, control 53 passed.
- `scripts/topic1_timing.py --outdir verification/auditor_r2_1/a3`, then `cmp_a3.py`: 0 mismatches against r1 and r2.
- `id_scan_audit.py`: 7,510 files, 0 hits.
- spurious run_scenario re-run on 3 keys: identical.
- git log, reflog and stash; enigma git status and find -newermt; nvidia-smi.

## Evidence files
- `verification/auditor_r2_1/`: `audit_mutants.py`, `audit_mutants.json`, `mut/<name>/pytest_out.txt`, `old_suite.log`, `a3/`,
  `cmp_a3.py`, `id_scan_audit.py`, `SHA256SUMS_tested.txt`, `SHA256SUMS_own.txt`.
