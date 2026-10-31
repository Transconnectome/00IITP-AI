# Handoff (Hard): challenger_r1_2, run tw-20261030-topic1, M1

**Verdict: CONFIRMED.** I found no correctness defect in production. I found nonblocking gaps in the fixtures and in the reporting.

## Challenge Summary
**Overall risk assessment: LOW** for correctness. **MEDIUM** for fixture coverage, because the frozen pipeline entry point is not exercised at TR ≠ 2.

## 1. Observation

All probes are under /home/juke/git/00IITP-AI/verification/challenger_r1_2/ and their raw logs are in logs/.

**Baseline checks**
- **New suite:** 29 passed in 3.66 s, rc 0 (logs/new_tests.log).
- **Old suite:** 86 passed, 7 warnings in 258.95 s under machine load, rc 0 (logs/old_tests.log).
- **Protected hashes:** 44/44 OK, rc 0, both at the start and at the end (logs/protected_final.log).
- **Card:** sha256 = 1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa, which matches. All 10 card §12 code hashes verify, with 0 failures.
- **Bytecode:** 0 new .pyc files in the new directories, in my tree, or in enigma.

**P1, census and null oracle (p1_census_null.py)**
- Graphs: 105 in total. 96 are random oriented graphs with N from 3 to 40 and p from 0.1 to 1.0. The other 9 are adversarial: a transitive and a regular tournament, out-stars and in-stars, disjoint 3-cycles, a bipartite DAG, dense and sparse random graphs, and a path.
- Three counts were compared: my own brute-force triad classifier, networkx `triadic_census`, and production `census`, plus the numba `_count_030`.
- On each graph, 15 nulls were checked with numpy and networkx for mutual edges, self-loops, in/out degrees and binary entries. The ensemble path and the single-seed path were also checked against each other.
- **Result: 0 failures.** The rank-2 identity holds whenever Z030T is finite. NaN always comes with a degenerate flag, and E2 is NaN whenever 030C is degenerate.
- Degenerate cases are correct. A transitive or regular tournament has 030C and 030T fixed by its score sequence. In a path, 030T is structurally 0.

**P2, full chain prepare_series → pipeline.subject_flow at all 7 on-disk TRs (p2_full_chain_tr.py)**
- Input: one continuous lead-lag signal with a raw-scale offset and drift added.
- At every TR (0.7, 0.8, 0.85, 1.0, 1.73, 1.8, 2.0):
  - all 10 planted pairs have the correct sign;
  - the |F| ratio to TR 2.0 is between 0.998 and 1.001;
  - corr(F, F at TR 2.0) = 1.000;
  - overlap of the 10% graph edges is 0.974–1.000.
- Defect contrast, lag = 1 native sample: the ratio is 0.547 at TR 0.7 and 0.734 at TR 1.0.
- **Time reversal** through prepare_series and subject_flow:
  - exact at TR 2.0 (max|F_rev + F| = 5.7e-15);
  - corr(F_rev, −F) ≥ 0.99993 at the other TRs;
  - the graph is exactly reversed at TR 2.0 and 1.73, and differs only at the margin elsewhere. This is consistent with OPEN_ISSUES #20.
- **Padding** through `NpyCohort.load` at TR 0.7, 1.73 and 2.0 with fake sites: F is exactly equal with 0, 1 or 164 zero rows appended. An interior zero row raises InvalidSeriesError, and the message contains no ID.

**P3 and P3b, null mixing at production scale (N = 304, m = 4,606; synthetic only)**
- Factors tested: 5/10, 20, 40, 100, 200, 400 and 1,000/2,000.
- The graphs were latency-driven (gradient share 0.52–0.85, acceptance 0.44–0.62), 60 planted cycles, white noise, and near-gradient graphs (gradient share 0.29–0.91, acceptance 0.083–0.69).
- **The null means plateau by factor 5–10 in every case.** For example, at acceptance 0.083 the mean 030T is 3768.6 at factor 5, 3764.5 at 20 and 3764.2 at 2,000, with sd ≈ 10. I see no attenuation at the frozen factor 20.
- The factor-to-factor variation in Z is consistent with Monte Carlo error in sd_null, which scales with |Z|.
- At the near-gradient setting with acceptance 0.083, 030C is structurally 0, so Z030C is degenerate (NaN).
- The 2-swap no-op probability (shared source or shared target, which still counts as "accepted") is 0.011–0.028 per 2-swap attempt. At acceptance 0.083 that is roughly a quarter of the accepted moves.

**P4, mutation test: 19 mutants on a mirror copy of src and tests (p4_mutation.py, logs/p4_mutation.log)**
- The unmutated mirror passes 29/29.
- **Killed (14):**
  - (b) no resampling, so lag is in native samples: 2 tests fail;
  - (c) null allows a reverse edge: 8;
  - (c2) the same, with the checker's mutual check also removed: 3;
  - (d) padding not stripped: 2;
  - (e) head trim counted in samples: 1;
  - (f) resample before detrend: 1;
  - (g) rotation disabled: 1;
  - (i) F sign flipped: 2;
  - (j) 030C off by one: 4;
  - (k) top-k by signed F: 4;
  - (l) same seed for all nulls: 5;
  - (m) synthetic fallback for a missing subject: 1;
  - (o) 80-ROI subsample: 1;
  - (q) swap does not update dst: 8.
- **SURVIVED (5):**
  - (a) `subject_flow` passes TR 2.0 instead of `series.tr`;
  - (n) the pipeline lag is doubled to 4 s;
  - (p) no z-score;
  - (r) PARAMS detrend = "none";
  - (h) the chain is not restarted per null. This one is a design variant, not a defect.

**P5, exhaustive reachability of the production move set (independent re-implementation, p5_irreducibility.py)**
- N = 4: 556 degree classes, 0 reducible.
- N = 5: 24,123 classes, of which 12,382 contain more than one graph; 60 are reducible. This confirms the explorers' 60/12,382.
- New: in all 60 reducible classes, (030C, 030T) is identical across components. At N ≤ 5, reducibility therefore cannot bias the census.

**P6, A3 timing re-run on the same 5 positional subjects (timing/, logs/p6_compare_timing.log)**
- The positions are [1578, 1228, 932, 0, 57] and params_sha256 matches.
- **0 mismatches** in the deterministic fields: tr, raw_valid_T, n_trim, valid_T, duration_s, m, acceptance, degenerate flags, and every abs_dZ value.
- Wall-time ratio to the worker's run: 1.00–1.01 for 4 subjects and 1.29 for position 57, with load average 8–18 on 20 cores.
- Mean unit time 4.66 s vs the worker's 4.38 s. CPU-h (추정): 13.3 vs 12.5 for all units, and 2.5 vs 2.3 for the primary unit. Peak RSS 293 MB vs 292 MB. **Within 2×.**
- No Z, SP or count values for any real subject were printed or inspected.

**Other checks**
- **Spurious-direction JSON:** re-running `spurious` with default arguments gives a file bit-identical to results/topic1/2026-10-30/spurious_direction.json, apart from elapsed_s.
- **Hodge decomposition (P7):** gradient_component equals an explicit least-squares solve to 1e-14, and the curl part has zero row sums.
- **Data facts, counts only:**
  - OCD 869 / HC 837;
  - Y-BOCS non-null: 856 in OCD and 123 in HC;
  - medication within OCD: 203 / 212 / 447 / 7 NaN;
  - 23 sites;
  - the medication-coding contradiction (medication_confound_analysis.py:23 vs site_driver_analysis.py:239) is confirmed verbatim.
- **Baselines from file:**
  - table1 baseline 0.6512 ± 0.0318 (26 evaluated + 4 checkpoint_missing, test N = 255);
  - track_b Remediated_Baseline 0.6606 ± 0.0262 and Linear_SVM_static_FC 0.6420 ± 0.0125;
  - site_driver auroc_scratch_mean: mean 0.6519, median 0.6707, 23 sites.
- **Privacy scan (P8):** 415 files scanned in my tree, the worker's outputs and this metadata directory, with 0 participant-ID hits.

## 2. Logic chain
1. A1 and A2 correctness:
   - The census, the null invariants and the Z/SP algebra agree with independent oracles on 105 graphs (P1).
   - The production pipeline handles every on-disk TR, padding and the loader correctly (P2).
   - The move rules are faithful to my independent re-implementation (P5), and the chain mixes at factor 20 even at acceptance 0.083 (P3b).
   - Therefore I found no correctness defect.
2. A2 "would FAIL on the defect":
   - The fixtures kill every defect named in ACCEPTANCE: reciprocal null edges, padding, lag in samples, detrend order and fallback.
   - However, the fixtures test `preprocess` and `lagged_net_flow` directly. Every `subject_flow` / `extract_subject` test uses a TR 2.0 fake site.
   - So defects at the frozen-pipeline entry point survive: wrong TR passed (a), wrong lag constant (n), detrend switched off in PARAMS (r) and z-score removed (p).
   - Production does not have these defects (P2), so this is a coverage gap, not a wrong result.
   - The mirror really did import its own copies. Mutant o (pipeline.py) and mutant b (preprocess.py) were both killed in the mirror, so the survivors are not an import artifact.
   - Why this is MEDIUM and not blocking:
     - pipeline.py and preprocess.py are pinned by the card's §12 hashes.
     - Any later edit that introduced one of these defects would also break those hashes.
     - The frozen code is verified correct at all 7 TRs (P2).
3. A3 is reproduced exactly (P6). The spurious-direction characterization is reproduced exactly.
4. The A4 card's factual claims that I checked match the files. These are the counts, the baselines, the coding contradiction and the hashes.

## 3. Caveats
- Irreducibility was checked exhaustively only for N ≤ 5. For N = 304 it is supported only by the factor plateau on synthetic graphs (P3, P3b). I did not probe real-subject graph mixing beyond the authorized timing re-run, whose |ΔZ| fields are reproduced exactly.
- I did not compute the minimum valid length across the full cohort; that would require reading cohort data. Very short series at TR 0.7 can become short on the grid: the floor of 20 native samples is only 7 grid samples. This should be checked in step 5.
- The cohort statistics script (LMM, Freedman–Lane, LOSO) does not exist, so it was not tested.
- Timing ran under machine load from other agents (load average 8–27).
- I did not review the scientific interpretation of the card, beyond the facts I checked.

## 4. Conclusion
CONFIRMED. Recommended nonblocking follow-ups:
- **(1)** Add one pipeline-level fixture: `extract_subject` / `subject_flow` through a fake TR 0.7 site against TR 2.0 on the same continuous signal. It should assert the |F| ratio and the sign, and pin PARAMS lag, detrend and z-score. This would kill mutants a, n, p and r.
- **(2)** The card §10 and OPEN_ISSUES #14 report only |ΔZ030C| as the factor diagnostic. |ΔZ030T| reached 0.909 (position 57) and 0.455 (position 1228). That bears on primary endpoint E2 and should be disclosed. My synthetic probes suggest it is Monte Carlo noise in sd_null that scales with |Z|, not under-mixing.
- **(3)** The reported "acceptance" includes 2-swap no-ops, up to about 25% of accepted moves for hub-heavy graphs. This is cosmetic.
- **(4)** In step 5, check the minimum grid length per subject.

## 5. Verification method
**Do not re-run in place.**
- p4 deletes and rebuilds mut/<name>/ and overwrites logs/p4_mutation_results.json.
- A timing re-run overwrites timing/.
- The tee logs are overwritten in the same way.
- First copy verification/challenger_r1_2/ to a new directory, such as verification/<new identity>/, and run from that copy with its outdir paths adjusted.
- The sha256 values of my receipts are in the structured return (tested_artifact_sha256).

```
cd /home/juke/git/00IITP-AI/verification/challenger_r1_2
PY=/home/juke/superclaude-env/bin/python3; export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
$PY -B p1_census_null.py        # expect: census/null failures=0 rank/nan failures=0
$PY -B p2_full_chain_tr.py      # sign_ok True at all TRs; ratios ~1.0; padding exact
$PY -B p3_null_mixing.py; $PY -B p3b_low_acceptance.py   # null means plateau by factor 10
$PY -B p4_mutation.py           # survivors: a, h, n, p, r
$PY -B p5_irreducibility.py 5   # reducible=60, differing (030C,030T)=0
$PY -B p6_compare_timing.py     # after the timing re-run into timing/: deterministic mismatches 0
$PY -B p8_privacy_scan.py       # id_hits=0
```
These conclusions are invalidated by any of the following: a change to any §12 code hash or to the test-file hashes listed in the structured return; a nonzero deterministic mismatch on a re-run.
