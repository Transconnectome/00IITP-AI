# Hard handoff — challenger_r2_2 (run tw-20261030-topic1, M1, iteration 2)

Verdict: **CONFIRMED.** My independent probes found no correctness failure in production, and no A2-listed fixture that fails to catch its targeted defect. They did find test-coverage gaps and one loader contract that the card states but no code enforces. These are nonblocking and are listed as hard requirements before step 5.

Probe directory: /home/juke/git/00IITP-AI/verification/challenger_r2_2/ (artifact hashes in SHA256SUMS.txt).

## 1. Observation

### Baselines
- Protected hashes, at start and at end: 44 OK, rc=0 (protected_start.log, protected_final.log).
- Card:
  - sha256 1e589f0b…75aa matches card_sha256.txt;
  - the §12 block gives 10/10 OK.
- `test_production_entry_point.py`:
  - byte-identical (cmp) to verification/explorer_r2_3/proposed_tests/;
  - sha256 d1c287e0…04d.
- Production src, tests, scripts and topic1 docs: 21/21 unchanged between my start and my end (start_hashes.txt).
- New suite: 53 passed (new_suite.log).
- Old suite: 86 passed, 7 warnings, 230 s, rc=0 (old_suite_86.log). The run was slow because of machine load.

### P1: networkx oracle on the production ensemble path (p1.log)
- 8 graphs, all OK:
  - N=304 / m=4606 (shared-driver-latency, white noise);
  - N=304 / m=2303 (planted cycles);
  - dense N=12 (d 0.9), N=8 (d 1.0) and N=6 (d 0.5);
  - out-star N=10;
  - three disjoint 3-cycles.
- What was checked:
  - `census()` equals `nx.triadic_census` for all 5 classes, with all 9 mutual classes zero and the total triad count correct;
  - per-null 030T/030C from `null_counts` equal the nx census of `sample_null_graph` with the same seed: 0 mismatches over 30-200 nulls per graph;
  - for every null graph, by plain numpy: degrees identical, 0 mutual edges, 0 self-loops, edge count m, entries in {0,1}. 0 violations;
  - all 5 null moments equal the nx-census moments;
  - the rank-2 identity holds.

### P2: end-to-end time reversal through `NpyCohort.load` → `subject_flow`, at all 7 on-disk TRs (p2_p3.log)
- Fake files were built so that the post-trim valid portions are exact reverses of each other.

| TR | Result |
|---|---|
| 2.0 | max\|F_rev + F\| = 8.5e-15; `topk(F_rev) == topk(F).T` exactly |
| other 6 TRs | corr(F_rev, −F) ≥ 0.99986; top-k edges flipped 0.987-1.000 |

- At every TR, the padded copy gives an identical F, and all 20 planted lead pairs flip orientation.

### P3: adversarial loader inputs (fake cohort, TR 2.0)
- Correctly raise:
  - leading zero rows;
  - a 1-D array;
  - NaN padding;
  - a zero-variance ROI;
  - an object/pickle array (MissingSubjectError);
  - a stray non-directory entry in the npy dir (it raises "no metadata row", so no silent shift).
- **Load silently and produce features:**
  - a transposed (304, T) file gives F 180×180 with m=1611;
  - (T, 303) gives F 303×303;
  - (T, 305) gives F 305×305;
  - (T, 12) gives F 12×12.
- `PARAMS["n_roi"] = 304` is never checked: grep finds no enforcement in data.py or pipeline.py. The card §1 says "ROIs | All 304".
- Also, a file with valid_T = 25 at TR 2.0 passes. The only length floor is 20 native samples after the head trim.

### P4: null mixing at production scale (N=304, m=4606, 200 nulls per factor; p4.log)
- Shift of the af=20 null mean vs af=400, in units of the af=400 null SD:

| Graph | Acceptance | 030T shift | 030C shift |
|---|---|---|---|
| latency sd 1 s | 0.449 | +0.14 sd (+1.4 MC-SE) | +0.03 sd |
| latency sd 2 s | 0.657 | −0.11 sd | −0.05 sd |
| HRF sd 1 s (max k_out 199) | 0.181 | +0.22 sd (+2.1 MC-SE) | +0.05 sd |
| white | 0.787 | −0.04 sd | +0.01 sd |

- When |Z030T| is large (40-80), Z changes by a few units across af. That is driven by Monte Carlo noise in sd_null (relative SE about 5% at 200 nulls), not by a drift of the mean.

### P5: own mutation test (33 mutants, all disjoint from worker_r2's 23; mutants.py, mutation_r2_2.json, mutants_run.log)
- Control: 53 passed. No mirror broke isolation. **21 of 33 killed.**
- **Killed:**
  - listdir_reverse_sorted, checker_mutual_disabled;
  - new_edges_no_pairwise_equal, new_edges_no_reverse_dir_check;
  - orientation_swapped, C_time_reversed;
  - interior_zero_check_removed, density_floor, topk_smallest_abs, gradient_potential_col_mean;
  - degenerate_flag_always_false, census_030C_no_div3, count030_c_no_div3, ensemble_same_seed_all_nulls;
  - padding_not_stripped, head_trim_from_end, rotation_never_used;
  - e2_from_sp, zero_var_check_removed, missing_file_fallback_zeros, chain_one_attempt.
- **Survived (12):**
  - e1_alias_is_030T (`"E1_Z030C": Z["030T"]`);
  - z_uses_null_mean_of_030T_for_all. The name is wrong: this mutant actually divides every class's Z by sd_null(030T);
  - curl_returns_F, curl_plus_gradient, pipeline_curl_channel_uses_F;
  - seeds_drop_position;
  - checker_degree_disabled;
  - sp_sum_not_nansum;
  - log_ratio_uses_030T;
  - min_len_check_removed;
  - max_tr_3. This is masked: `resample_to_grid` raises for any TR > 2.0 anyway;
  - new_edges_no_pairwise_reverse. This is equivalent: P6 enumerates every 2-swap and 3-rotation on 5 labelled nodes and finds 0 reachable pairwise-reversed new edges.

### P5b: my own check that the iteration-1 blocker is closed (mutants_blocker.py, mutation_blocker_r2_2.json, mutants_blocker_run.log)
- I wrote 4 entry-point wiring defects myself; the edit strings differ from worker_r2's:
  - `subject_flow` passes 2.0 as TR;
  - lag `round(lag_s / series.tr)` applied on the grid;
  - `grid_dt = series.tr` (no grid, lag-1 native);
  - head trim recomputed at TR 2.0 inside `prepare_series`.

| Mode | Control | Result |
|---|---|---|
| full | 53 passed | **4/4 KILLED** (7-16 failures each) |
| old_only (entry-point file deleted) | 29 passed | **4/4 SURVIVE** |

- This reproduces the iteration-1 gap and shows that the new file closes it.
- Combined total of my mutants: 37, of which 25 are killed and 12 survive (1 equivalent, 1 masked).

### P6: direct production correctness on every surviving surface (p6.log; all OK)
- E1 == Z030C and E2 == Z030C − Z030T, on 2 graphs.
- Hodge decomposition:
  - G equals an independent least-squares solve on the edge-incidence matrix (N=7 and 25, atol 1e-12);
  - the curl part is divergence-free and orthogonal to G;
  - the share matches.
- The curl channel in `flow_features` uses F − G, and differs from broadband.
- The seed rule gives 24/24 distinct streams across position, channel and density, and is deterministic.
- SP with degenerate 030T is renormalized over the finite classes {021C, 030C}, and E2 is NaN.
- Z for all 5 classes equals (obs − mean)/sd(ddof 1), computed from an independent nx census of the same-seed nulls (80 nulls).

### P6b: A3 rerun on 5 real subjects (verification/challenger_r2_2/a3/)
- I derived the positions independently, using the stated rule and metadata only: [1578, 1228, 932, 0, 57].
- The TR counts match the proposal: 43 / 96 / 104 / 119 / 39 / 110 / 1195.
- My own comparator: **0 mismatches in 225 deterministic fields vs both r1 and r2**. The fields are tr, raw_valid_T, n_trim, valid_T, duration_s, m, acceptance, degenerate flags, every |dZ|, and params/params_sha256.
- Wall time: mine/r1 = [2.76, 1.01, 1.01, 1.00, 1.00]. Subject 1 ran at load average about 31, while my mutation harness was also running. Wall times are therefore not a valid estimate.
- Extrapolated cost (추정): 16.96 CPU-h all units, 3.58 CPU-h primary unit. Peak RSS 288 MB.

### Safety
- Count-only ID scan: 2,095 IDs held in memory, 707 files scanned, 0 content hits, 0 filename hits (id_scan.log).
- No `__pycache__`, `.pyc` or `.pytest_cache` newer than my start in src, tests, enigma or my directory.
- Nothing newer than my start in src, tests, scripts, results or topic1 docs.
- In enigma, only `logs/coordinator.log` and `experiments/.job_status/` (mtime 22:25 KST) are newer than my start. They belong to another process's coordinator; I only `np.load`ed (mmap) 5 npy files read-only and read the metadata CSV.

## 2. Logic chain
1. The core correctness surfaces all pass independent oracles: census, null invariants, null-count equality, moments and the Z formula against networkx at production scale (P1, P6.7). So A1's null and census contract holds.
2. The flow chain is correct end to end at all 7 TRs through the production loader (P2). This closes the worker's admitted reversal gap empirically, though there is still no committed fixture for it. The A2 padding, two-TR and reversal properties hold.
3. Each A2-listed defect class has at least one mutant that the suite kills:
   - time reversal: C_time_reversed;
   - null invariants: pairwise_equal, reverse_dir, mutual_disabled, plus the worker's raise path;
   - padding: padding_not_stripped;
   - lag/TR: the worker's set;
   - 3-cycle detection: census and count div3, chain_one_attempt, same_seed.
   No A2 fixture failed to catch its target. My own restatement of the 4 iteration-1 blocking wiring defects is killed only when the new entry-point file is present (P5b). The gate blocker is therefore closed on independent evidence, not only on the worker's harness.
4. The survivors are on surfaces A2 does not list: endpoint aliases and denominators, the curl channel, the seed rule, the guard self-tests, SP NaN policy, log_ratio and the length floor. P6 shows production is correct on every one of them. They are coverage gaps, not defects.
5. The missing n_roi check is a real gap between card and code, not a defect on the present data. The survey reports every npy as (T_raw, 304), and the 5 A3 subjects loaded with 304 ROIs. I did not re-read all 1,706 headers; that decision is the root's.
6. Mixing at af=20 shows at most a 0.22 SD bias in the 030T null mean on the most skewed synthetic graph (max k_out 199). That is small next to the effect scale, and it is a disclosed parameter-adequacy issue (addendum item 30).
7. A3 is exactly reproducible.

Therefore: CONFIRMED, with nonblocking requirements.

## 3. Caveats
- My 37 mutants (33 + 4 blocker restatements) are hand-written and not exhaustive. The worker's other 19 mutants were not re-run by me. `spurious.py`, `synthetic.py` and the timing script were not mutation-tested.
- P4 uses synthetic graphs. Real-subject feature values were not inspected, as required. The real |dZ030T| = 0.909 at position 57 is consistent with Monte Carlo noise in sd_null at large |Z|, but I cannot confirm that without looking at the value.
- The P3 transposed-file finding uses a fake cohort only. I did not scan real headers.
- A3 wall times are confounded by load and by my concurrent harness.
- DISPATCH.md quotes the dispatch verbatim except the embedded worker JSON, which it summarizes. The full worker text is at worker_r2/handoff.md, and the root holds the exact dispatch.
- I did not read the peer challenger_r2_1's outputs, to stay independent.

## 4. Conclusion
CONFIRMED for M1 iteration 2. Before the step-5 cohort script, add these hard requirements, highest priority first:
1. A numeric fixture pinning `E1_Z030C == Z030C` and the per-class Z denominator. Both mutants survive today, and the endpoints are the pre-registered primaries.
2. Enforce `X.shape[1] == PARAMS["n_roi"]` (304) in the loader or in `subject_flow`. A transposed or short-ROI file currently yields features silently.
3. A fixture for the curl channel (`curl_component` = F − G, divergence-free).
4. Positional distinctness of null seeds, and a degree-violation self-test for `_check_invariants`.
5. A minimum valid duration in seconds, as also listed by the worker.
6. Optionally, an SP NaN-policy test and a log_ratio test.
7. A committed end-to-end reversal fixture through `NpyCohort.load`. P2 can serve as the template.

## 5. Verification method
- `cd /home/juke/git/00IITP-AI`
- For every Python command below, use `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/juke/superclaude-env/bin/python3 -B`.
- Probes:
  - `verification/challenger_r2_2/p1_census_null_oracle.py` → expect `ALL_OK 8 / 8`;
  - `verification/challenger_r2_2/p2_p3_loader_reversal.py` → expect `P2 ALL_OK`, and P3 lines showing `transposed_304_by_T: LOADED`;
  - `verification/challenger_r2_2/p6_untested_surfaces.py` → expect `P6 ALL_OK`;
  - `verification/challenger_r2_2/p4_mixing.py` → shifts within about 0.25 sd.
- Mutation run: `verification/challenger_r2_2/mutants.py <out.json> full` → expect 21/33 killed, with the 12 survivors listed above. The harness rebuilds `verification/challenger_r2_2/mut`.
- Blocker restatement: `verification/challenger_r2_2/mutants_blocker.py <out.json> full old_only` → expect full 4/4 KILLED and old_only 4/4 SURVIVE (it rebuilds `mut_blocker`).
- A3 comparison: `verification/challenger_r2_2/compare_a3_own.py verification/challenger_r2_2/a3/a3_timing.json results/topic1/2026-10-30/a3_timing.json results/topic1/2026-10-30/a3_r2/a3_timing.json` → expect 0 mismatches.
- Protected hashes: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261030-topic1/sentinel/PROTECTED_HASHES.txt` → expect rc 0.
- Invalidation: any edit to src/topic1_lagmotif, tests/topic1_lagmotif, scripts/topic1_timing.py or the card.
