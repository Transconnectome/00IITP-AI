# victory_auditor_1 — Hard handoff (run tw-20261030-topic1, milestone M1)

```
=== VICTORY AUDIT REPORT ===

VERDICT: VERIFIED COMPLETE  (role-file wording: VICTORY CONFIRMED)

PHASE A — TIMELINE:
  Result: PASS
  Anomalies: none that invalidate the claim.
   - Order on disk (KST):
     src 20:58–21:01 -> tests 21:02–21:04 -> timing script 21:05 -> spurious JSON 21:06
     -> A3 timing 21:06–21:10 -> test_flow_chain.py and test_defect_sensitivity.py edited 21:10:39
     -> card frozen 21:12 (r--r--r--) -> card_sha256.txt 21:12:22 -> OPEN_ISSUES 21:13
     -> r2 tests-only 21:59 -> a3_r2 22:03 -> mutation_check_r2 22:09 -> addendum 22:12.
     No backdating. The 21:10 test edits fall between A3 and the freeze. That is harmless: tests are not in card §12,
     and the §12 code hashes still pass.
   - A3 (5 real subjects) ran before the card file was written. The card discloses this. Only computational fields
     were logged, and no labels were joined.
   - LAUNCH_HASHES 4/5 OK. Only sentinel/BRIEFING.md changed, and it is mutable sentinel metadata.
     ORIGINAL_REQUEST, ACCEPTANCE and APPROVED_PROPOSAL are unchanged, so the criteria were not altered mid-run.

PHASE B — INTEGRITY CHECK (General profile; Development mode, because ORIGINAL_REQUEST has no from-scratch constraint):
  Result: PASS
  Details:
   - No hardcoded results and no facades.
     - The census is closed-form. It equals networkx on synthetic graphs and on two real 304-node graphs.
     - The null is a real numba MCMC with per-null invariant checks.
   - No fabricated artifacts.
     - spurious_direction.json re-executed at 0.10: 14/14 entries bit-identical.
     - The 5% degeneracy counts cited in the card (12/12 and 6/12) were confirmed from the file.
     - a3_timing.json re-executed for real positions 1578 and 57, 12 units: m, acceptance, degenerate flags,
       tr, raw_valid_T, n_trim and valid_T are all exactly equal. Wall time is +0.4–1.2%.
   - The tests are not self-certifying.
     - My own 19 mutants were written before I read the team's full mutant list; the addendum, which I had read,
       names 5 of theirs. 18/19 were killed.
     - Plus 4 extra mutants on surfaces a reviewer flagged as non-blocking: all 4 survived.
     - Every survivor is a test-coverage gap; the current code is correct (see Discrepancies).

PHASE C — INDEPENDENT TEST EXECUTION:
  Test command (new): cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q
  Your results: 53 passed (3.62 s; rerun 4.00 s)
  Test command (old): STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
  Your results: 86 passed, 7 warnings in 70.01 s
  Protected hashes: rc 0 (44/44), at start and again at end of audit
  Layout lint: PASS, 0 findings (99 files, then 100 after my handoff), exit 0
  Claimed results: 53 passed; 86 passed; protected 44/44; layout PASS
  Match: YES
```

## Per-criterion verdicts
- **A1 PASS.**
  - Valid portion: code verified and mutant killed; on 2 real subjects, zero rows appended give bit-identical X and F.
  - Lag: 2 s on a 2.0 s grid with exact resample_poly ratios, documented. Lag mutants (native samples, 4 s,
    no detrend, head trim in samples) all killed.
  - 304 ROIs: confirmed through extract_subject, m = 2303/4606/6908.
  - Null:
    - The 2-swap and 3-rotation moves reject an edge that exists in either direction, and reject self-loops.
    - Every null is checked.
    - Reciprocal, self-loop and degree mutants were all killed.
    - On real 304-node graphs, my own numpy check of 10 nulls passes.
    - SP is restricted to the 5 connected oriented classes, documented.
  - Real data is read-only: 0 files under enigma/data are newer than the run start.
  - No synthetic fallback: both fallback mutants were killed.
- **A2 PASS.**
  - All 6 bullets are covered by passing tests. Each one fails on its defect in my mutation run:
    planted-cycle detection, time reversal, null invariants, padding, two-TR, spurious direction.
  - Planted cycles vs control: Z030C +9.63±0.22 vs +0.24±0.27 (reproduced).
  - Spurious direction is quantified and reported as an open limitation, which A2 permits.
- **A3 PASS.**
  - Per-unit time: 4.38 s per (channel, density) at 1000 nulls. Peak RSS: 292 MB.
  - CPU-h, labelled 추정: 12.47 for all units, 2.27 for the primary unit. The arithmetic is verified.
  - The raw log is saved and uses positional indices only. Reproduced on 2 subjects.
- **A4 PASS, with one deviation from the literal wording.**
  - Hash: card sha 1e589f0b…75aa matches card_sha256.txt, the card is read-only, §12 is 10/10, and params_sha256 is 86863ffa…15c6.
  - Every factual number was recomputed from the source files and matches.
  - All required sections are present.
  - Deviation: A4 asked for the "existing MBBN AUROC≈0.63" with its source verified from a file. No main-cohort file has
    it. The card replaces it with file-backed values (0.6512±0.0318 n=26, 0.6606±0.0262, 0.6420±0.0125, LOSO 0.6519)
    and says why. The human must accept this substitution.
  - Valid T enters as log(duration_s) = log(valid_T·TR), which is equivalent to valid T within site.
- **A5 PASS, with three disclosed deviations.**
  - Core checks: 86/86, protected 44/44, PRE_RUN 8/8. git HEAD is unchanged, with no commit or stash.
  - ID scan: 0 hits, both word-bounded and without word boundaries, across all run outputs, metadata,
    all of verification/, and my own outputs.
  - Command classification: across 950 other-agent and 69 root Bash commands, no executed ssh, Slurm, network or
    git-write command falls inside the run window. The only GPU-related call is a read-only `nvidia-smi` process query.
  - No full-cohort feature extraction anywhere: every multi-subject probe loop uses fake cohorts.
  - Deviation (a): explorer_survey_1 read all 1,706 series for a NaN/zero-ROI QC scan, plus 40 cache rows and
    spectra for 20 subjects. Labels were used for counts only and never joined to features (addendum G.39).
  - Deviation (b): before the run, during the proposal phase at 10:22Z and 10:27Z (the run began about 11:09Z),
    the root session ran read-only ssh reachability checks on connectome and dgx1: hostname, sinfo, squeue count,
    df, an nvidia-smi query and ls. No job was submitted.
  - Deviation (c): my own `git status` in the enigma repo updated the mtime of its `.git` directory (index.lock).
    No content changed, and I ran no further git commands there.
  - Not part of this run: an orphan `ssh connectome python3 -` process (pid 1328408, 21:08:49) belongs to another Claude
    session (cwd PGSTWFA-3DCNN-testbed-wt-challenge, scratchpad session 2d4db8d5). The enigma coordinator.log and
    .job_status changes come from a pre-existing 5-minute cron job.
- **A6 PASS.** OPEN_ISSUES (24 items) and the addendum (items 25–39) record:
  - the report-vs-JSON discrepancy;
  - the count conflict, the medication-coding contradiction and the 0.63 provenance;
  - the spec errors;
  - every v2 limitation.

## Discrepancies between claims and artifacts (none falsifies a criterion)
1. **Team mutant coverage.** The team's "23/23 mutants killed" did not cover the cohort entry point's output contract.
   - These mutants survive all 53 tests: `roi_subsample_80` (ROI loss inside `extract_subject`), `extract_subject_drops_valid_T`
     (reports raw_valid_T as valid_T), `curl_returns_F`, `seeds_ignore_position` (card §11 seed rule) and `sp_not_normalised`.
   - The current code is correct for all five.
   - A reviewer had already listed curl, seeds, SP and logratio as non-blocking. The two `extract_subject` gaps are new.
2. **Card §1 density provenance.** The card cites spurious_direction.json (21:06) as the basis for the density choice,
   but PARAMS was set at 21:00:54. Disclosed as errata in addendum item 33.
3. **Card §10 omits |ΔZ030T|.** Factor 40 vs 20 gives up to 0.909 at position 57 and 0.455 at position 1228.
   Disclosed in addendum item 30.
4. **Card preamble "No diagnosis label was loaded in this run".** This is true only of the worker code path. Survey and
   audit probes read labels for counts. No label was ever joined to real features (addendum item 33).
5. **"MBBN AUROC≈0.63".** No main-cohort file contains it. The likely source is the medicated-subset AUROC of 0.6285
   in enigma HANDOFF.md:21.

## Caveats
- **Order of reading.** I read no handoff.md before forming my verdicts. I did read context fragments from the
  orchestrator journals while grepping for forbidden commands, and those fragments supplied two leads: the orphan ssh
  process and the reviewer's list of untested surfaces. I verified both independently (/proc; my own extra mutants).
  I also opened mutation_check_r2.json only to compare mutant coverage.
- **What the command evidence covers.** It comes from transcripts and greps, the current process table and hashes.
  A command run outside these sessions cannot be excluded.
- **Mutation evidence.** The mirrors were deleted after the runs; `mutants.py` rebuilds them. Hashes:
  - mutants.py 0b7b655c…a7b5
  - mutation_results.json b9b74cac…b09a
  - mutants_extra.py 78fbcee4…f8ee9
  - mutation_results_extra.json 1fdfa486…7edf

## Conclusion — what the human must know before approving step 5
1. **Spurious-direction bias is uncontrolled.**
   - With no neural coupling, a 1 s per-ROI latency spread gives E2 ≈ +7.3 and Z030T ≈ −7.6.
   - Neither the oriented null nor curl-only removes it.
   - AR(φ) mismatch shifts E2 by about −1.2.
   - So group differences in HRF latency, slice timing or global signal could pass the |d| ≥ 0.15 bar.
   - The HRF peak-shift and shared zero-lag scenarios were 11/12 and 10/12 degenerate at 10%. Their bias was never
     measured, which is not the same as being small.
   - Real-scale degeneracy rates are known only from 5 subjects.
2. **Null mixing is weak on some subjects.**
   - The move set's irreducibility is not established.
   - Position 1578 has acceptance 0.074, and the acceptance figure includes no-op moves.
   - |ΔZ030T| between factor 40 and factor 20 reaches 0.91.
   - Near-degenerate nulls, where sd is tiny but not 0, are not flagged.
3. **The cohort statistics script (card §4–§6) is unwritten and unreviewed.** Before step 5 it also needs:
   - addendum F.34–F.38: acceptance and degeneracy by group and site, a minimum length on the 2.0 s grid, and a pinned
     positional manifest;
   - tests for the `extract_subject` output contract: 304 ROIs, valid_T, the curl channel and the seed rule.
4. **Data gaps.**
   - Medication coding is contradictory in the source repo; the codebook needs confirming.
   - The 869/837 vs 833/873 count conflict is open.
   - There is no FD/motion data.
   - The npy preprocessing provenance (GSR, slice timing) is unknown.
   - The ROI labels are unknown, so CSTC is dropped.
5. **Compute estimates are local only (추정).** 12.5–13.1 CPU-h for all units and 2.3 CPU-h for the primary unit, measured
   on DGX-Spark. numba 0.62 and scipy availability and speed on the connectome CPU nodes are unverified.
6. **The ≈0.63 baseline was replaced** by file-backed values. The human must accept this.
7. **EMPIRICAL_ANALYSIS_REPORT.md T1–T4 numbers stay unusable** until rerun, because of the report-vs-JSON discrepancy.

## Verification Method
- Canonical checks: `/home/juke/git/00IITP-AI/verification/victory_auditor_1/run_checks.sh` runs the new suite, the old suite,
  the protected hashes and the layout lint.
- Mutation runs:
  - `python -B verification/victory_auditor_1/mutants.py` (all mutants, no arguments). Expected: control 54 passed,
    18/19 killed, survivor `roi_subsample_80`.
  - `python -B verification/victory_auditor_1/mutants_extra.py`. Expected: 4/4 survive.
- Spurious-direction re-run: `python -B -m src.topic1_lagmotif.spurious --out <f> --densities 0.10`, then diff against
  results/topic1/2026-10-30/spurious_direction.json. Expected: 0 mismatches.
- Probes:
  - `probe_real_a3.py`: 2 real subjects, deterministic fields only.
  - `probe_card_facts.py` and `probe_baselines.py`: card facts and baselines.
  - `probe_id_scan2.py strict <dirs>` and `probe_id_scan3_noboundary.py strict <dirs>`: ID scans.
- Invalidation: this verdict is void if src/topic1_lagmotif, scripts/topic1_timing.py, tests/topic1_lagmotif, the card or any
  protected file changes, or if any cohort-level output appears.
