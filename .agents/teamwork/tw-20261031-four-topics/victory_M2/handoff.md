# victory_M2 handoff — M2 (Topic 3) victory audit after the PI-fixed final iteration r4 (Hard handoff)

Written 2026-11-01 ~13:45Z by victory_M2. Verdict: **VERIFIED_COMPLETE** (VICTORY CONFIRMED), with nonblocking items listed in §4.
All probes, logs and runners are under `/home/juke/git/00IITP-AI/verification/victory_M2/`. Nothing in the production tree was edited; no git write; 0 GPU.

## 1. Observation

O1. **Pins and C1** (production, before and after all runs). `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: 67 OK, rc 0 (logs `c1_check.log`, `c1_check_post.log`). Receipts: `output_sha256.txt` 42 OK; `addendum_02/03/04/05/06_sha256.txt` 1/3/2/3/3 OK. `code_sha256_at_freeze.txt`: 26 OK, 1 FAILED = `scripts/topic3_launch_connectome.py` (disclosed in addendum 01 item 2). The card hashes to `683374565d80…b1e0`, equal to `card_sha256.txt` and to the card blob in commit `24fe976` (2026-10-31T08:46:25Z).

O2. **Timeline** (file mtimes plus git). The card was committed at 08:46:25Z and frozen at 08:48:29Z (`card_sha256.txt` and `code_sha256_at_freeze.txt`, both 08:48:29Z). `family_A_subject_level.json` was written at 08:49:44Z, the token job outputs at 08:53–08:58Z and `family_B_token_level.json` at 09:02:23Z. The r4 tests were written at 2026-11-01T08:13:57Z; the worker's first evidence log is from 08:24:32Z. No `.pyc` under src/, scripts/ or tests/ is newer than 2026-11-01T00:39Z (`snap/pyc_pre.txt` = `snap/pyc_post.txt`).

O3. **Producer provenance.** In all 4 `token_job/*_token_job.json` files, `code_sha256` equals both `code_sha256_at_freeze.txt` and the current bytes for all 7 files (src/topic3_spectral/*.py and scripts/topic3_token_job.py). The npz sha256 equals each record. Primary checks: pins ok, row order ok, 7/7 frames, re-pool allclose with max |Δ| from 9.9e-8 to 4.8e-7.

O4. **Suites in production** (`bin/run_suite.sh`, PYTHONDONTWRITEBYTECODE=1, 2 threads, timeout 900, nice; junit in `suites/*/junit.xml`):
- `tests/topic3_spectral`: tests=138, failures=0, errors=0, skipped=0 (87.7 s). That is 121 shipped plus 17 r4.
- Old suite (`STRICT_E2E=1 tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed, 0 skipped.
- `tests/topic1_lagmotif`: 88 passed.

O5. **Rerun in a copied tree, with OUT following the copy.** The tree's manifest (125 files) was checked byte-identical to production. An import canary placed `src.topic3_spectral` inside the copy. All four scripts returned rc 0: `topic3_provenance_repro`, `topic3_alpha_calibration`, `topic3_subject_level` and `topic3_token_stats` (`rerun_logs/`). A value comparison against the pinned JSONs (`bin/compare_json.py`) gave:
- Family A: 300 of 300 `results` leaves equal (max rel 0).
- Family B: 466 of 466 non-run, non-jobs leaves equal. The jobs block is equal except `runtime_s`.
- Alpha calibration: 204 of 204 leaves equal.
- Provenance: equal except 3 path strings and `runtime_s`. `report_reproduced` and `json_reproduced` are both true.

The outputs are kept in `rerun_outputs/` with `SHA256SUMS.txt`.

O6. **Independent recomputation** (`probes/indep_recompute.py`; does not import src/, uses its own seeds 777 and 31337; output in `indep_recompute.out.json`).
- **E1 values.** covPR and corrPR of all 7 matrices equal the pinned values to 4 decimals. The uncentered PR is 1.0014–1.0743, as in the old json.
- **Alignment.** The six 57-row files share one row order. The 25 NeuroSTORM rows form an increasing subset.
- **Intervals at my own seeds.**
  - A1 L2−L3: cov [+3.16, +7.69], corr [+4.31, +7.91].
  - L2−L1: cov [+2.90, +6.40].
  - L1−L0: covers 0.
  - D3 at n = 25: BrainJEPA−BrainLM [+0.85, +3.44], NeuroSTORM−BrainLM [+1.87, +5.02].

  The signs and robustness are the same as pinned.
- **Family B.** The H1a–H1e means equal the pinned values exactly, in all 4 checkpoints. My own sign-flip, bootstrap and Holm give the same significance pattern.
- **Replication rule by hand.** H1a holds (L3 higher, 2 of 3 zoo checkpoints agree). H1b is not replicated (1 of 3).
- **Spectra identities** in the pinned npz. The trace of the correlation eigenvalues equals D exactly for every subject, variant and checkpoint. The stored covPR equals the PR of the stored covariance eigenvalues within 4e-8 relative. |log covPR − log corrPR| ≥ 0.028 per subject (minimum 0.0288, HCP LN0L2). So CR3_T01/T02-type cov/corr swaps did not occur in the real producer output.

O7. **The named mutants of PI decision 6, run myself.**
- **Specs.** `bin/my_specs.py` reads them from the four r3 harness files. Their sha256 prefixes match addendum 06 §4.1: `17a30dca63a1`, `ca6d7381474c`, `d5f73f38e358` and `0be048a3a82c`. The extractor evaluates only top-level literals.
- **Runner.** `bin/run_mutants.py` makes a fresh copy of my own production-identical base tree for each job and applies one patch (old string exactly once). It runs under timeout 900 with at most 2 jobs at a time. Each process group is killed after its job.
- **r4 run** (`mutants/RUN_r4_required.json`). The control passed 17 of 17. **26 of 26 required ids were KILLED**, all with 17 tests, 0 skipped and attempt 1.
  - Class (a), 20 ids: each fails both FA-real and FA-synth, except FA11, which fails FA-synth only.
  - Class (b): CR3_T01, CR3_T02 and TJ03 fail TJ-direct and TJ-pack.
  - Class (c): N01 fails 8 tests (6 hand-built cases and 2 computed cases).
  - Class (d): VA01 and VA02 fail D1-table and D1-computed.
- **Shipped-suite sample** (`mutants/RUN_shipped_sample.json`, 121 tests, control 121 of 121 passed). N01, CR3_T01, CR3_T02, VA01 and B_A2_iid_at_n25 all SURVIVE the shipped suite. So in these five cases the r4 tests are what kills them.

O8. **My own in-class probes, not named by the r3 gate** (`mutants/RUN_full_extra.json`, full 138-test suite, control 138 of 138 passed). 8 of 10 were KILLED. Two SURVIVED:
- **VX04** (`analysis.py:191`): `prim_ok` reads max(Holm p of both primaries) < α, so one primary's significance depends on the other primary's Holm p.
- **VX06** (`token_job.py:96`): concatenated `corr_eigs(Xcat, 1e-2)`, a dead-column floor 10× the card's 1e-3 at the call site.

O9. **Worker evidence.** All 399 log and JUnit sha256 values recorded in `verification/worker_M2_r4/runs/EVID_named_r4{.json.partial,_v2b.json.partial,_v3.json}` and `EVID_union_r4_{v3ff.json.partial,v3c.json}` match the files on disk. The JUnit test counts match the records. The union totals 150 KILLED and 1 SURVIVED (U127), with controls OK.

O10. **C4 and C7.** `probes/id_scan.py` loads the 57 real id strings in memory only. Across 2383 files (tests/topic3_spectral, src/topic3_spectral, scripts, results/topic3, docs topic3, verification/worker_M2_r4/r3/r2b and worker_M2_r4 metadata) it found **0 real-ID hits**. The prefix-plus-alphanumeric pattern occurs only as synthetic `SYN…` names in the shipped `test_token_job_driver.py` and its copies, and in the superseded addendum 06 v1. My own outputs give 0 / 0. The VRABES inputs are dated 2026-10-18, and VRABES `git status --porcelain` is empty. SwiFT ver11 sha256 `de132387…052a`: the last stage has `downsample=None` (line 1068), and `BasicLayer.forward` runs the blocks, then the downsample.

O11. **Layout and side effects.** `audit_layout.py` on the run metadata root gives PASS (281 files, 0 findings). My production snapshots are unchanged before vs after for code, tests, docs, results and pyc. `git status` changed only because the root checkpoint loop made commits `55576fb` (13:16:30Z) and `c622609` (13:31:30Z), which included my metadata `.md` files. Neither commit is mine.

## 2. Logic chain

1. PI decision 6 limits the gate to three things: (i) the four classes are closed, meaning the named mutants are killed; (ii) no regression across all suites, pins and C1; (iii) integrity. New mutants outside the classes are nonblocking.
2. (i) O7 shows that all 26 named ids die to r4 tests of their own class in my own runner and tree. The shipped-suite sample shows these tests are what closes the gap.
3. (ii) O1 and O4 show C1 at 67 OK, every receipt OK and the suites at 138/86/88 with 0 skipped. These match the claims in addendum 06 §7.
4. (iii) Integrity:
   - src/ and scripts/ are unchanged (O1, O3).
   - The results reproduce exactly from the frozen code (O5) and from my own independent code (O6).
   - The worker's evidence files match their hashes (O9).
   - No IDs leaked (O10).
   - The r4 tests are not self-certifying. The class (a) synthetic, (b) and (d) tests re-derive values with independent numpy code. The class (a) real-data test is the regression against the receipt-checked pin that decision 6(a) explicitly requires.
5. T3.1–T3.4:
   - **T3.1.** The inputs are pinned and read-only, and their provenance is documented. The PR≈1 artefact is resolved by the centering fixture and reproduced (O5, O6).
   - **T3.2.** The card was committed and frozen before the first real-data result it governs (O2). It states hypotheses, centered estimators, α methods (OLS rank slope; Clauset MLE with KS xmin), nulls and controls (iid reference, column-permutation "shuffled" null, checkpoint replication; random-init deferred as H2) and decision rules (D1, D2, D3, replication).
   - **T3.3.** The tests contain exact-rank PR (k ∈ {1, 5, 20, 56}), analytic unequal spectra, α_rank exact on a power law, Clauset recovery of an iid Pareto exponent within 0.05, and the old uncentered PR < 1.1 against the new PR = k. All pass.
   - **T3.4.** The real rerun has dated outputs, a report and verdicts per claim. No GPU was needed.
6. VX04 and VX06 are new mutants (O8). Neither is named by the r3 gate, and neither can act on the real data: both primaries have Holm p = 0.0002, and no real token column falls under the 1e-3 floor. Whether any column falls between 1e-3 and 1e-2 × median SD cannot be checked without the connectome frames. By decision 6 they are nonblocking and are reported.
7. Therefore: VICTORY CONFIRMED / VERIFIED_COMPLETE.

## 3. Caveats

- I did not rerun the connectome token job; the frames stay on connectome. Producer correctness on the real frames rests on three things: the code hashes recorded by the job (O3), the eigenvalue identities in the pinned spectra (O6), and the class (b) synthetic tests. The job JSON is self-reported by the job on connectome.
- I ran the 26 named mutants against the two r4 files only (17 tests). The full-suite attribution claim (0 pre-existing failures) was checked for a 5-mutant sample, not for all 26.
- I did not rerun the 151-patch union; I checked the worker's union evidence by hash (O9).
- I read the r4 gate verifiers' handoffs only after my verdict was formed: reviewer_M2_r4_1 APPROVE, auditor_M2_r4_1 CLEAN, both consistent with mine. I did not read worker handoffs.
- H2 (random-init control) is untested by design (card §6).
- C4 scan coverage. The byte scan (`probes/id_scan.py`) finds UTF-8/ASCII id strings only. Binary coverage comes from `probes/npz_dtype_scan.py`, which opened every .npz/.npy under the same roots plus the r3/r4 verifier folders (83 files) and found 10 string arrays, all synthetic test fixtures, with 0 real-ID hits; the 1 refused object array is the deliberate `test_object_arrays_refused` fixture. A pass over the shared /tmp/pytest-of-juke (9156 npz/npy, 7917 string arrays) also gave 0 real-ID hits; the byte scan of that 5.5 GB tree did not finish within 300 s and is not claimed. Unprefixed id tokens shorter than 6 characters were not searched, to avoid false positives.

## 4. Conclusion

M2 is **VERIFIED_COMPLETE** under ORIGINAL_REQUEST, ACCEPTANCE (C1–C8, T3.1–T3.4) and PI decisions 1 and 6.

**Nonblocking items the PI should know:**
- (1) H2, the random-init control, is untested.
- (2) VX04 and VX06 survive the full suite; neither is active on the real data.
- (3) VB02, the label for one unreachable case, the untested halts (N06/N12/GD01–GD03), the tie-only mutants (FA13/FA14) and U127 remain open, as addendum 06 §5 lists.
- (4) The Family B wiring tests and the class (a) real-data test skip without VRABES. Class (a) keeps the synthetic guard; Family B wiring has no VRABES-independent guard.
- (5) The token-level reading limits of addenda 02–03 apply: replication is across checkpoints confounded by depth and training family, and the effective ceiling of the PR is 7.
- (6) Report errata: +3.23 should read +3.22, and −3.29 should read −3.28 (addendum 03).

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for r in output addendum_02 addendum_03 addendum_04 addendum_05 addendum_06; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
verification/victory_M2/bin/run_suite.sh <tag> -- tests/topic3_spectral          # expect 138 passed, 0 skipped
verification/victory_M2/bin/run_suite.sh <tag> STRICT_E2E=1 -- tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e   # 86
/home/juke/superclaude-env/bin/python3 -I -B verification/victory_M2/probes/indep_recompute.py
# mutants: rebuild mutants/tree_base from production (see bin/run_mutants.py header; the base tree was deleted after the run, manifest kept in mutants/tree_base.manifest_sha256.txt), then
/home/juke/superclaude-env/bin/python3 -I -B verification/victory_M2/bin/my_specs.py verification/victory_M2/mutants/required_specs.json
/home/juke/superclaude-env/bin/python3 -I -B verification/victory_M2/bin/run_mutants.py verification/victory_M2/mutants/required_specs.json <out.json> r4
```

**Invalidation conditions:**
- any receipt or C1 line fails;
- any src/ or scripts/topic3_* byte changes;
- a named mutant survives the r4 files;
- the topic3 suite shows a skip or a count other than 138;
- a real-ID hit appears in the scan.
