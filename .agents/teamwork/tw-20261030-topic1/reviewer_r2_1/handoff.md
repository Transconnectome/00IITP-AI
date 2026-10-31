# Hard handoff — reviewer_r2_1 (run tw-20261030-topic1, M1, iteration 2)

**Verdict: APPROVE.** Each of A1–A6 is met, and I checked the evidence myself. I found no integrity violation. The non-blocking findings are in §3 and §4.

## 1. Observation

### 1.1 Runs I made myself (logs in /home/juke/git/00IITP-AI/verification/reviewer_r2_1/)

**Protected hashes.** I ran `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` at the start and again at the end. Both runs gave 44 OK, rc=0 (`protected_start.log`, `protected_final.log`).

**New suite.**
- Command: `PYTHONDONTWRITEBYTECODE=1 OPENBLAS/OMP/MKL=1 python -B -m pytest -p no:cacheprovider tests/topic1_lagmotif -q -rA`.
- Result: 53 passed in 4.04 s, rc=0.
- That is 29 iteration-1 tests plus 24 in `test_production_entry_point.py`.

**Old suite.**
- Command: `PYTHONDONTWRITEBYTECODE=1 STRICT_E2E=1 PYTHONPATH=<repo> python -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q`.
- Result: 86 passed, 7 warnings, 189.09 s, rc=0 (`old_suite_86.log`).

**Frozen card and code hashes.**
- The card's sha256 is `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`. It matches `results/topic1/2026-10-30/card_sha256.txt` and OPEN_ISSUES.md line 3. The file is mode r--r--r--.
- The card §12 block passes `sha256sum -c` with 10/10 OK, so `src/topic1_lagmotif/*` and `scripts/topic1_timing.py` are unchanged since the freeze.
- `params_sha256()` returns `86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6`.
- `cmp` finds `tests/topic1_lagmotif/test_production_entry_point.py` identical to `verification/explorer_r2_3/proposed_tests/test_production_entry_point.py`. Both have sha256 `d1c287e0…d04d`.
- The test-file hashes in `results/topic1/2026-10-30/test_hashes_r2.txt` all verify. That list was written by the worker, so on its own it is self-consistency only.
- I also checked the 7 iteration-1 test files against hashes recorded independently in iteration 1: `verification/auditor_r1_1/tested_artifacts.sha256` (21:29 KST) and `verification/challenger_r1_1/prod_hashes_before.txt` (21:20 KST). All 7 are OK against both (`r1_test_hash_check.log`). The iteration-1 tests were not loosened in iteration 2.

**Independent mutation probe.** `my_mutants.py` → `my_mutants_result.json` and `my_mutants_run.log`.
- I chose 26 mutants myself. They target code the worker's 23 mutants never edit: the null move set, chain rollback, the invariant checker, the census closed form, top-k orientation and edge count, the flow sign, the loader (padding strip, interior-zero check, trim side, synthetic fallback, default site, name order), the TR gate, the seeds, SP, the log-ratio and valid_T.
- Each mutant ran in an isolated mirror copy with an isolation-guard conftest. The control gave 53 passed. None of the isolation guards fired.
- Result: 22/26 killed. The four survivors are:
  - `curl_returns_F` (curl channel = broadband);
  - `seeds_ignore_position` (the same null seeds for every subject);
  - `sp_not_normalised`;
  - `logratio_wrong`.
- All four touch only secondary, descriptive or reproducibility outputs. The primary endpoints E1 = Z030C and E2 = Z030C − Z030T at broadband@0.10 are not affected.

**Independent A3 rerun.** I ran `scripts/topic1_timing.py --outdir verification/reviewer_r2_1/a3_rerun` and compared with my own code (`a3_compare.txt`).
- The positions were the same, [1578, 1228, 932, 0, 57].
- I compared 220 deterministic fields against r1 and found 0 mismatches. The fields were tr, raw_valid_T, n_trim, valid_T, duration_s, m, acceptance, the degenerate flags, all |dZ| values, n_null and attempts_factor.
- params_sha256 is equal across r1, r2 and my run.
- My wall times are higher (mean unit 5.70 s against 4.38 s for r1, 16.2 CPU-h 추정) because my mutation probe ran concurrently and the machine load average was 22–26. Peak RSS was 289 MB.

**Independent probes.** `probe_review.py` → `probe_review.out.json` and `p6_recheck.txt`.

| Probe | What it checks | Result |
|---|---|---|
| P1 | Time reversal end-to-end through `prepare_series → subject_flow` at all 7 TRs | Exact at 2.0 s (max\|F_rev+F\| 6e-15). corr(F_rev, −F) ≥ 0.99997 elsewhere. All leader→follower signs flip. |
| P2 | Padding at TR 0.7 through `NpyCohort.load` with 200 zero rows appended | F and the observed census are identical. |
| P3 | Second N=5 degree class (21 states) | All 21 states reached. χ² p = 0.44. |
| P4 | N=304 with the frozen PARAMS | m = 4,606, acceptance 0.78, invariants hold, rank-2 identity holds. |
| P5 | Cohort aggregates (counts only) | 2,095 metadata rows; 1,706 on disk, all matched; 23 sites. TR counts 43/96/104/119/39/110/1,195. Diagnosis codes 869 (code 1) / 837 (code 2). 388 absent rows have TR > 2. No FD, motion or DVARS column. All match card §3/§4. |
| P6 | Baselines in card §6 | table1 baseline test_AUROC is 0.6512 ± 0.0318 (26 evaluated, 4 checkpoint_missing, N_test = 255). Remediated_Baseline is 0.6606 ± 0.0262. Linear_SVM_static_FC is 0.6420 ± 0.0125. LOSO `auroc_scratch_mean` is 0.6519 (median 0.6707, 23 sites). All match card §6. My first P6 pass picked the wrong column (val_AUROC_peak); I corrected it in p6_recheck.txt. |
| P7 | `spurious_direction.json` | Matches card §9 and OPEN_ISSUES item 12: AR mismatch Z030C −0.38 (SE 0.35), Z030T +0.82, E2 −1.20; latency 1 s Z030T −7.57, E2 +7.26; latency 2 s Z030C −1.86; curl −5.09/−4.69; planted +9.63; white +0.24. |

**ID scans (count only).** `id_scan.py` held 2,095 IDs in memory, with a minimum length of 16 characters.
- Production outputs, docs, tests, src, scripts and worker metadata: 43 files, 0 content hits, 0 name hits.
- My own verification and metadata files: 561 files, 0 hits.

**Bytecode and caches.** No `__pycache__`, `.pyc`, `.pytest_cache` or numba cache file is newer than my start time in src, tests, scripts, results/topic1, verification/reviewer_r2_1 or the enigma repo. The existing `tests/__pycache__` dates from 18:31 KST, before this run.

**Metadata layout lint.** `audit_layout.py` on the run root inspected 85 files and returned findings [], rc=0.

**Git.** HEAD is still e380802 (2026-03-09), so nothing was committed during this run.

### 1.2 Source review (file:line)

**`data.py`** (A1 valid portion, explicit errors, no fallback)
- Line 50–64: strips trailing zero rows and raises on interior zero rows or NaN.
- Line 67–84: head trim of ceil(40/TR) samples, then the zero-variance check.
- Line 127–139: a missing file, missing metadata row or out-of-range position raises `MissingSubjectError` with the position only.
- Line 135: the data are opened with `mmap_mode="r"` and copied.
- I found no fallback path.

**`preprocess.py`** (lag in seconds)
- Line 60–74: detrend → `resample_poly` with the exact Fraction ratio and padtype 'line' → z-score.

**`flow.py`**
- Line 13–20: F = C − Cᵀ.
- Line 35–53: exact top-k by |F|, oriented by sign.

**`motifs.py`**
- `census`, line 53–66: I re-derived 030C, 030T, 021D/U and 021C for oriented graphs and they are correct.
- Move proposals, line 86–121: the 2-swap and the 3-rotation are symmetric. The inverse of rotation (i,j,k) is drawn as (i,k,j).
- `_new_edges_ok`: rejects a new edge if it is a self-loop or exists in either direction.
- Every null is checked by `_check_invariants` (line 125–154), and `null_counts` raises on any flag (line 234–236).
- Z = NaN when sd = 0 (line 253).

**`pipeline.py`**
- Line 66–69: `subject_flow` passes `series.tr` and the lag in seconds through PARAMS.

## 2. Logic chain

1. **A1.** The loader, preprocessing, flow, graph and null code implements every A1 bullet (§1.2).
   - The SP restriction to 5 classes is documented in the `motifs.py` docstring and card §1.
   - Real-data read-only operation is shown by the A3 rerun on the npy directory, which reproduced deterministically.
   - Mutants that add a synthetic fallback or a default site are killed.
2. **A2.** Every fixture bullet has a test that passes, and seeding a defect in a production copy makes it fail:
   - planted cycles vs control;
   - time reversal;
   - null invariants on every null;
   - padding;
   - two-TR consistency through the production loader;
   - spurious direction, quantified and reported.

   Evidence for the fail-on-defect half:
   - The worker reports 23/23 kills, including the iteration-1 blockers `pipeline_tr_ignored`, `lag_native_samples` and `pipeline_lag1_native_no_grid`.
   - My own different set of 26 production mutants gave 22 kills.
   - The 4 survivors are outside the A2 bullet list.
   - The iteration-1 gate gap (the production entry point untested at TR ≠ 2.0) is closed: the spec oracle at all 7 TRs and the 2 s vs 4 s loader test now exercise `subject_flow`.
3. **A3.** The timing artifacts exist, contain no IDs, label the extrapolation 추정 and report per-unit times, peak RSS and CPU-h. My rerun reproduces every deterministic field.
4. **A4.** I checked every required card element against the file and against independent recomputation (P5, P6):
   - hypotheses; primary E1/E2; population 1,706 with the TR > 2 exclusion; LMM site random intercept plus Mundlak terms;
   - age, sex and log duration; FD absence; LOSO CV; kill rule; file-backed baselines with paths; Y-BOCS;
   - medication within OCD, with the contradiction cited and HC coding flagged; CSTC dropped; Holm across the 2 endpoints;
   - sha256 recorded.

   The order was PARAMS → A3 (12:10Z) → card freeze (12:12Z), and the card states that no cohort result exists. No cohort output exists under results/topic1.
5. **A5.** 86 passed; 44 protected OK; no external edits attributable to this run (see caveats); no commit; no GPU, ssh or Slurm; no IDs written.
6. **A6.** OPEN_ISSUES (items 1–24) and the addendum (items 25–39) record the report-vs-JSON discrepancy and the limitations found.

## 3. Caveats

**Non-blocking findings**
1. **Untested secondary outputs.** The curl channel, the seed rule, SP normalisation and the 030C log-ratio have no fail-on-defect test (my 4 surviving mutants). They are secondary, descriptive or reproducibility items, and none is listed in A2. A cohort-script review should add tests for them before step 5.
2. **Near-degenerate nulls.** When the null SD is tiny but not zero (low acceptance or few distinct null values, e.g. position 1578 with acceptance 0.074), the Z values become extreme and are not flagged. The pre-registered rule flags only sd == 0. I recommend reporting the number of distinct null values per subject in the cohort script; this would be labelled post-freeze.
3. **Time reversal in the suite.** Time reversal through `subject_flow` is still not part of the test suite (addendum item 29). My P1 probe confirms that the production behaviour is correct.
4. **Known items already disclosed by the worker:**
   - the `max|F| <= 1.0` comment;
   - no-op moves counted in the acceptance rate;
   - |dZ030T| of 0.909/0.455 under the attempts factor;
   - card wording errata;
   - irreducibility of the move set not established;
   - the uncontrolled latency/HRF spurious-direction bias.

**Other caveats**
- **Enigma repo activity.** In the enigma repo, `experiments/.job_status` and `logs/coordinator.log` have mtime 22:20:11 KST. Those writes come from another process. They are not attributable to this review or to the worker.
- **My own write to the enigma repo.** I ran `git status` in the read-only enigma repo. That was a reviewer breach, made by me and not by the worker. The `.git` directory's mtime changed to 22:20:55, consistent with a transient index.lock. `.git/index` itself still has mtime 2026-10-19 18:15, so the index was not rewritten and no tracked content changed. I ran no further git commands there.
- **Addendum item 39 and A5.** explorer_survey_1 read all 1,706 series once, at the survey stage, before the ≤5-subject rule applied. It was a NaN and zero-row/ROI scan only: no features were extracted and no labels were joined. My ruling is that this is not the "full-cohort run" that A5 or step 5 forbids, and it is outside the worker's product. It is non-blocking, and the root should still adjudicate it as item 39 asks.
- **Scope of my reads.** I did not re-verify medication or Y-BOCS counts. I read only the diagnosis-code counts, in aggregate.
- **Wall times.** My A3 wall times are inflated by concurrent load.
- **DISPATCH.md.** It summarises the embedded worker JSON rather than copying all of it character for character.

## 4. Conclusion

APPROVE M1 iteration 2. A1–A6 are each met with evidence I verified. No blocking issue remains. Step 5 is still not authorized.

## 5. Verification method

- Rerun the suites with the commands in §1.1. Expect 53 passed and 86 passed.
- Run `sha256sum -c` on PROTECTED_HASHES. Expect 44 OK.
- Check the card sha256 and run the card §12 block through `sha256sum -c`. Expect 10/10.
- Run `python -B verification/reviewer_r2_1/my_mutants.py <out.json>`. It rebuilds `verification/reviewer_r2_1/mut/`; copy it to a new identity directory first. Expect 22/26 killed, with the 4 named survivors.
- `a3_compare.txt` should show 0 mismatches.
- Invalidated by any edit to `src/topic1_lagmotif`, `scripts/topic1_timing.py`, `tests/topic1_lagmotif` or the card.
