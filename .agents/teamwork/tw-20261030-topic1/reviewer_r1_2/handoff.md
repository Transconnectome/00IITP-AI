# reviewer_r1_2 handoff — M1 review (Hard handoff)

**Verdict: APPROVE.** A1–A6 are each met, with evidence I reproduced myself. There are no blocking issues. The non-blocking findings are listed below; the cohort-stats script or the next dated card should address them.

## 1. Observation

### Commands run, and results

- **New tests.** `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q`
  - Result: 29 passed in 3.57s, rc=0 (log: verification/reviewer_r1_2/new_tests.log).
- **Old suite.** `PYTHONDONTWRITEBYTECODE=1 STRICT_E2E=1 PYTHONPATH=/home/juke/git/00IITP-AI ... -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q`
  - Result: 86 passed, 7 warnings in 64.69s, rc=0 (log: verification/reviewer_r1_2/old_suite.log).
- **Protected files.** `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives 44/44 OK and rc=0, both at the start and at the end (12:29Z).
  - Every pre-existing src/tests .py file is covered by the hash list.
  - The only files modified since run start (outside .agents and verification) are the two new docs/03_empirical_analysis/topic1 files.
  - git shows `M docs/qa_prep_…` from 2026-03-09. That file is in the protected list with OK, so it was not touched in this run.
- **Bytecode and caches.** No __pycache__, .pyc or .pytest_cache appeared during the run outside verification/. Survey-era caches exist only under verification/explorer_survey_{2,3}.
- **Analysis card hash.** `sha256sum` on the card gives 1e589f0b…75aa, which matches card_sha256.txt and OPEN_ISSUES. The file mode is r--r--r--.
- **Card §12 code hashes.** `sha256sum -c` on the 10 listed files: all 10 OK.
- **PARAMS hash.** `params_sha256()` gives 86863ffa…c15c6, which matches the card and a3_timing.json.
- **Freeze order.** pipeline.py mtime is 21:00:54 KST, A3 started at 21:06:45, and the card was frozen at 21:12:10.

### Reproductions

- **spurious_direction.json** was regenerated from code (`-m src.topic1_lagmotif.spurious`). All 42 result entries are identical (0 mismatches). The card and OPEN_ISSUES numbers match the JSON:
  - AR mismatch at 10%: Z030C −0.38±0.35, Z030T +0.82, E2 −1.20.
  - Latency SD 1 s: Z030T −7.57, E2 +7.26, 2/12 degenerate. Curl variant: Z030C −5.09.
  - Latency SD 2 s: Z030C −1.86, E2 +6.91.
  - Planted cycles: +9.63±0.22. White noise: +0.24.
  - Shared zero-lag at 5%: 12/12 degenerate.
  - HRF peak shift at 10%: 11/12 degenerate.
- **A3 timing** was re-run on the same 5 positional subjects (into verification/reviewer_r1_2/timing_rerun/).
  - Positions, TR, valid_T, n_trim, acceptance, degenerate flags and both |ΔZ| diagnostics are identical (0 mismatches). The params sha is the same.
  - Mean unit time was 4.51 s (worker: 4.38 s). Extrapolated full cohort, all units: 12.82 CPU-h (worker: 12.47). Peak RSS 293 MB.

### Data facts recomputed read-only (counts only; no IDs printed)

- 2,095 metadata rows; 1,706 on disk; OCD code 1: 869, code 2: 837; 23 sites.
- Absent: 389 = Seoul 95, Chiba-CHBSRPB 89, Shanghai 84, Chiba-CHBC 53, Chiba-CHB 42, Kyoto1.5T 25, Vancouver 1.
- Y-BOCS non-null: 856 in OCD, 123 in HC. OCD medication codes: 3: 447, 2: 212, 1: 203, NaN: 7.
- No FD, motion or DVARS column exists. Age and Sex have no NaNs.
- Medication coding lines:
  - medication_confound_analysis.py:22 is "OCD: 1 = OCD patient, 2 = HC" and :23 is "Medication: 1 = medicated…";
  - site_driver_analysis.py:235/237/239 say OCD 1 = OCD, Sex 1 = male, Medication 1 = drug-free.
  - The contradiction the worker reported is confirmed.
- Baselines recomputed:
  - table1 baseline: 26 evaluated + 4 checkpoint_missing, mean 0.6512, SD 0.0318;
  - Remediated_Baseline 0.6606±0.0262; Linear_SVM_static_FC 0.6420±0.0125;
  - site_driver_analysis.csv auroc_scratch_mean: 23 sites, mean 0.6519, median 0.6707.
- enigma HANDOFF.md:21 contains "복용 OCD vs HC AUROC=0.628" (the medicated-OCD vs HC subset). This is probably where "≈0.63" came from. It is not a main-cohort number, so the card is right not to use it.
- ID leak scan: 952 files across the new src/tests/scripts/results/docs and worker metadata, checked against the 1,706 directory names, gave 0 hits.

### Code reading (correctness checked by hand)

- **Census.** The closed form is correct for oriented graphs: 030C = tr(A³)/3, 030T = Σ A∘A², and 021D/021U/021C from degree sums. It also matches networkx in the tests.
- **2-swap.** It preserves in- and out-degree, and it rejects a new edge that exists in either direction, a self-loop, or a new pair that is duplicated or reversed.
- **3-edge rotation.** (u1→v2, u2→v3, u3→v1) preserves degrees. Its inverse is the ordered triple (i,k,j), so the proposal is symmetric.
- **Per-null checks.** Every null is checked in int64 (motifs.py:124-154, 233-236).
- **Hodge potential.** p_i = mean_j F_ij is the correct least-squares potential on the complete graph.
- **Loader.**
  - It strips trailing zero rows.
  - It raises on an interior zero row, NaN, or a zero-variance ROI.
  - Exception messages contain the position only, and are raised `from None`.
  - There is no fallback path.

### Mutation probes

The package and tests were copied to verification/reviewer_r1_2/mutants/; production was not modified. 10 of 11 mutants are killed:

| Mutant | Killed by |
|---|---|
| no reverse-direction check | test_every_null_graph… |
| no resampling | test_two_tr… and test_resampling_raw_scale… |
| keep padding | padding test |
| 030C without /3 | networkx oracle |
| orientation flipped | full-chain test |
| no rotation move | rotation test |
| F = C + Cᵀ | time-reversal test |
| degenerate guard removed | padding test |
| no head trim | padding test |

**M10 survived**: `subject_flow` using lag = 2 grid samples (4 s) still passes all 29 tests. The identity mutant (M0) also passes, as a control should.

### Edge probe (verification/reviewer_r1_2/probe_edge_cases.py)

- The null is deterministic for fixed seeds.
- On a star graph and on a 4-node transitive tournament (unique graphs), it gives degenerate → Z NaN, flagged.
- Resample ratios are exact for all 7 on-disk TRs.
- 40 random N=5 oriented classes were all fully reached in 300 samples.
- A 20-native-sample series at TR 0.7 (about 7 grid samples) still returns a flow matrix.

### External repo

- enigma .git has 9 loose blobs with mtime 20:22 KST, during the survey phase, before the worker's first file at 20:58.
- .git/index mtime is 2026-10-19, the only stash dates from 2026-04-05, and no refs changed. One blob, ff5351f, is already referenced by the unchanged index.
- So the blobs are inert, and they are not from the worker.
- logs/coordinator.log is appended every 5 minutes by an unrelated user cron (ic_coordinator.py).

## 2. Logic chain

- **A1 is met.**
  - Valid portion plus valid_T and duration_s: data.py, with the padding test.
  - Lag in seconds: 2.0 s grid with exact resample_poly ratios and lag 1 grid sample. The two-TR test checks a ratio in [0.85, 1.15] with matching direction.
  - All 304 ROIs: full-chain test with exact m.
  - Null: degree-preserving and orientation-preserving, with no mutual edges or self-loops, asserted on every null.
  - SP over the 5 oriented classes, documented in the motifs docstring and card §1.
  - Real npy read-only (mmap_mode="r").
  - Missing subject raises an explicit positional error.
- **A2 is met.**
  - Every listed fixture exists and passes.
  - Fail-on-defect is shown by the worker's defect tests and independently by my mutants.
  - Spurious direction is quantified and recorded as a limitation, and the numbers reproduce from code.
- **A3 is met.**
  - Per-unit wall time at n_null = 1,000, peak RSS, 추정-labelled CPU-h, and a raw log are all present.
  - Positional indices only.
  - The deterministic fields reproduce exactly.
- **A4 is met.** The card is frozen before any cohort result and contains every required element:
  - hypotheses; E1 and E2;
  - population, with the TR > 2 s exclusion;
  - LMM site random effect plus Mundlak, age, sex, log valid duration (equivalent to valid T given the site terms);
  - FD stated as absent;
  - LOSO CV;
  - kill rule |d| < 0.15 or p_Holm ≥ 0.05;
  - static FC and file-verified MBBN baselines, with ≈0.63 honestly rejected;
  - Y-BOCS; medication within OCD, with both conflicting sources cited and HC flagged;
  - CSTC dropped; Holm across the 2 primary endpoints;
  - sha256 recorded outside the card.
- **A5 is met.** 86 passed; 44/44 protected files OK; no external edits by the worker; no cohort, GPU, ssh or git mutation evidence.
- **A6 is met.** OPEN_ISSUES lists the report-vs-JSON discrepancy and 23 further items.
- **Integrity.** I found no hardcoded expected outputs, facade implementations or fabricated logs. Both result artifacts reproduce byte-for-byte or deterministically from code.

## 3. Caveats

- The report-vs-JSON discrepancy (A6 item 1) was not re-verified by the worker or by me. A6 requires it to be recorded, not fixed.
- I did not prove irreducibility of the move set; nobody claims it.
- The cohort-level statistics script does not exist, so its conformance to card §4–§6 cannot be reviewed yet.
- Choosing the primary density of 10% (PROJECT.md said 15% top-|F|) is a pre-registration decision made from synthetic evidence. ACCEPTANCE does not fix the density. In the rerun JSON, planted Z030C is 20.1 at 5%, 9.6 at 10% and 8.2 at 15%, so "diluted at 15%" is mild. The real argument for 10% over 5% is degeneracy. The root or the user may want to note this deviation.
- The timing rerun loaded the same 5 real subjects. The dispatch permits this.

## 4. Conclusion

**APPROVE M1.** There are no blocking issues.

Non-blocking findings, ranked:

1. **(Major) The mixing budget is fixed in attempts, not in accepted moves.**
   - Position 1578 accepts 0.074 of attempts, so 20·m attempts give about 1.5·m accepted moves. That is below the 6·m-attempt regime OPEN_ISSUES 14 shows to be non-uniform.
   - A small |ΔZ| between 20·m and 40·m does not prove mixing: two chains stuck near the observed graph can agree.
   - Low acceptance goes with gradient-dominated graphs, which may differ by group.
   - Recommendation: the cohort script or the next dated card should add an accepted-moves floor, or an acceptance-stratified sensitivity analysis.
2. **No test guards E2 under AR(φ) mismatch.** E2 is about −1.2 there. The fixture asserts only Z030C and Z030T, although E2 is a primary endpoint. It is disclosed in OPEN_ISSUES 12.
3. **Mutant M10 survives.** No test binds `subject_flow` to lag = 1 grid sample. The card §12 hash freeze limits the risk.
4. **The minimum series length is 20 native samples, not a floor in seconds or grid samples.** The real minimum (about 100 samples, about 200 s) makes this moot for the current data.
5. **Excluding degenerate nulls is informative missingness.**
   - Degeneracy correlates with gradient share.
   - The fallback rule (more than 10% degenerate → 15%) and the log-ratio secondary only partly mitigate it.
   - Report the degenerate rate by group in the cohort run.
6. **Minor wording.** The card does not name HANDOFF.md:21 (0.628, medicated-OCD vs HC subset) as the probable origin of "≈0.63".
7. **Process.** The worker's DISPATCH.md is not verbatim. It says so.
8. **Run-level.** The enigma .git has inert loose blobs from the survey phase (20:22 KST). Not the worker's.

## 5. Verification method

- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` should give 44 OK.
- Run the two pytest commands in §1: expect 29 passed and 86 passed.
- `sha256sum docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md` should give 1e589f0b….
- Extract the card's §12 hash block and run `sha256sum -c` on it.
- Reproduce spurious_direction.json: `PYTHONDONTWRITEBYTECODE=1 ... python -B -m src.topic1_lagmotif.spurious --out <tmp>`, then compare the results entries. Expect identity.
- Re-run the mutation probes with `verification/reviewer_r1_2/run_mutants.sh`.
- Invalidation conditions:
  - any change to src/topic1_lagmotif/*.py or scripts/topic1_timing.py, because the §12 hashes break;
  - any edit of the card;
  - any PROTECTED_HASHES failure.
