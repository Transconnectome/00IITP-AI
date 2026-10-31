# reviewer_r1_1 handoff — Review Summary

**Verdict: APPROVE.** Every criterion A1–A6 is met, with evidence I reproduced myself. No integrity violation was found. The non-blocking issues listed below should be fixed before step 5 (the cohort statistics script and the cohort run).

## Verified claims
- **New tests:** 29 passed (3.58 s).
- **Old suite:** 86 passed, rc=0, run on the explicit file list with STRICT_E2E=1.
- **Protected hashes:** `sha256sum -c` reports 44/44 OK.
- **Card hashes:**
  - The card's sha256 is 1e589f0b…75aa. It matches card_sha256.txt and OPEN_ISSUES. The file is mode r--r--r--.
  - The §12 code hashes check 10/10 OK.
  - `params_sha256()` returns 86863ffa…c6, as stated.
- **Data facts checked against the files** (counts only):
  - 2,095 metadata rows, 1,706 on disk, 389 absent. Of the absent, 388 come from the 6 sites with TR > 2 s and 1 from Vancouver.
  - OCD 869 / HC 837.
  - Y-BOCS non-null: 856 OCD and 123 HC.
  - Medication within OCD: 203 / 212 / 447 / 7 NaN. Within HC: 405 / 177 / 255 NaN.
  - The TR distribution matches the card. There are 23 sites. There is no motion column.
  - The medication coding contradiction is confirmed:
    - medication_confound_analysis.py:23 says 1 = medicated.
    - site_driver_analysis.py:239 says 1 = drug-free.
  - The diagnosis-coding lines :22 and :235 are confirmed.
- **Baselines:**
  - table1 baseline: 26 evaluated rows and 4 checkpoint_missing; mean 0.6512, SD 0.0318.
  - Remediated_Baseline 0.6606 ± 0.0262; Linear_SVM_static_FC 0.6420 ± 0.0125.
  - LOSO auroc_scratch_mean: mean 0.6519, median 0.6707, 23 sites.
- **Privacy:** I scanned 30 new files for the 1,706 participant directory names and found 0 hits. The cache subject order equals `sorted(listdir)`.
- **Spurious-direction rerun:** reproduced exactly, with a maximum difference of 0 across 42 keys.
- **A3 timing rerun:** reproduced deterministically.
  - Positions, valid_T, acceptance, |dZ| and degenerate flags are identical.
  - Wall time was 1.43× longer. I ran it at the same time as my other probes, so the slowdown is my own contention, not an error in the worker's numbers.
- **Code checks by hand:**
  - The census formulas are correct.
  - The Hodge potential p = row-mean(F) is the least-squares solution.
  - The 2-swap and the 3-rotation each preserve degrees, and each is symmetric: the inverse of a rotation is the same move with the triple ordered (i, k, j). The uniform distribution is therefore stationary on the reachable component.
  - The new-edge test rejects an edge that exists in either direction.
  - Each null starts afresh from its own seed and has its invariants checked.

## Mutation probe (verification/reviewer_r1_1/mutation_probe.sh)
Of 12 mutants, 10 were killed: reciprocal edges allowed, no padding strip, no resampling, F not antisymmetric, wrong 030T census, chain that never moves, no rotation move, flipped orientation, rotation dst bug, zero lag.

Two survived:
- **The invariant raise in null_counts disabled.** This mutant is equivalent unless the chain itself is broken. The same check is exercised through sample_null_graph.
- **detrend ignored inside pipeline.subject_flow.** No fixture runs subject_flow at a resampled TR on trended raw-scale input.

## Extra probes at N = 304, density 0.10 (the dimension of the real analysis)
- **White-noise calibration under H0:**
  - T sweep (8 seeds per T, T = 100–3000): Z030C, Z030T and E2 stay within about 2 SE of 0, with no consistent sign.
  - 24 fresh seeds at T = 100, 130 and 1000: the same result. The per-subject SD is 0.8–2.1, which confirms the overdispersion.
- **Planted cycles, 8 seeds** (an earlier single-seed probe was inconclusive):
  - 20 cycles: Z030C +4.93 ± 0.60, minimum +2.89.
  - Matched control: −0.21 ± 0.30, maximum +0.86.
  - 100 cycles: +17.1.
- **Chain convergence:** comparing attempts factor 20 with 100, |ΔZ030C| ≤ 0.2 on white noise, planted cycles and latency-dominated graphs, including an acceptance rate of 0.48.

## Non-blocking issues
1. **Fixture gap: no end-to-end test through subject_flow/PARAMS at a resampled TR with trend and offset.** The two-TR and detrend fixtures call preprocess() directly. Add one fixture at TR 0.7 that goes through subject_flow.
2. **The A2 fixtures run only at N = 60.** My N = 304 probes show the pipeline is calibrated and detects planted cycles there. A small fixture at N = 304 would lock that in.
3. **Density provenance overstated.**
   - pipeline.py (mtime 21:00 KST) predates spurious_direction.json (21:06 KST).
   - Yet card §1 cites that JSON, including the 12/12 and 6/12 degenerate counts, as a basis for fixing density at 10%.
   - The worker's own JSON shows mild dilution only: planted Z030C is 20.1 at 5%, 9.6 at 10% and 8.2 at 15%. The case for 10% over 5% rests on the degeneracy risk.
   - This changes from PROJECT.md's 15% are disclosed, and the choice was made without labels. No data-driven tuning was found.
4. **The CPU-hour figure is the uncontended best case.** 12.5 CPU-h was measured on an idle machine. Under load my rerun extrapolated to 17.9 CPU-h. Plan a margin of about 1.5×.
5. **Near-degenerate nulls.** A very small but nonzero null SD gives extreme Z values. The card does pre-register a rank-INT sensitivity analysis and a log-ratio secondary.
6. **Acceptance rate may differ between groups.** It ranges from 0.07 to 0.75, and differential mixing could bias Z. Record the acceptance rate and keep the factor-40 sensitivity analysis.
7. **Process items:**
   - The worker's DISPATCH.md is not verbatim (disclosed).
   - The card was frozen without the advisor's second check (disclosed); this review partly fills that gap.
   - The cohort statistics script is not implemented; it needs review before step 5.

## Safety notes (A5)
- **enigma files modified during the run** (experiments/.job_status, logs/coordinator.log, mtime 21:20–21:25):
  - coordinator.log is a periodic "IC Loss" job tracker with entries dating back to 2026-03-21 and 886k lines.
  - It is unrelated to this run.
- **The ssh connectome process started at 21:08:49 KST:**
  - It is an orphan whose cwd is /home/juke/git/PGSTWFA-3DCNN-testbed-wt-challenge, belonging to another Claude session (TMUX_PANE %30).
  - It is not from this run. No ssh appears in any topic1 code.
- **My own action:** I ran a read-only `git status` in enigma_ocd_mbbn. It may have refreshed .git/index, which would explain the .git mtime of 21:20:53. No tracked content was touched.
