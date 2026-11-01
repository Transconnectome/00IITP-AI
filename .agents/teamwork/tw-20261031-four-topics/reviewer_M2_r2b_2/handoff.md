# reviewer_M2_r2b_2 — handoff (Hard), M2 Topic 3 gate r2b, 2026-11-01 ~01:40Z

## Review Summary

**Verdict: REQUEST_CHANGES.** There is one blocking issue, and it is narrow and additive.

**What is correct (confirmed):**
- Every computed number and both card verdicts reproduce. I recomputed them from scratch from the pinned spectra and JSON.
- The card preceded every governed result.
- C1, C2 and C4–C8 hold.
- The Family B estimand description (iteration-1 blocker i) is closed by addendum 03 §1–2. The numbers in it are correct.

**What blocks:** the iteration-1 blocker (ii), "verdict logic unguarded by tests", is closed only for the mutants that were assigned. A new verdict-path mutant survives the full shipped 88-test suite:
- **V01** reads the primary checkpoint's significance from the raw sign-flip p instead of the Holm p.
- It is reachable, and it flips the outcome from "not holds" to "holds" on a synthetic input that the card's own B = 9999 sign-flip test produced.
- Card §5 line 89 requires the Holm p for the primary.
- Addendum 03 §4 says the tests pin "Holm p is used, not raw p". In fact only the zoo side is pinned.

## 1. Observation

**O1. Integrity checks** (`verification/reviewer_M2_r2b_2/baseline/`, `final/`)

| Check | Result |
|---|---|
| C1 (`LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`) | rc 0, 67 OK before and after; the two logs are identical |
| `output_sha256.txt` | rc 0, 42 OK |
| `addendum_02_sha256.txt` | rc 0, 1 OK |
| `addendum_03_sha256.txt` | rc 0, 3 OK |
| `addendum_04_sha256.txt` | rc 0, 2 OK |
| Card (`card_sha256.txt`, after stripping the trailing annotation) | OK, `683374565d80…` |
| `code_sha256_at_freeze.txt` | 26 OK; `scripts/topic3_launch_connectome.py` FAILED, which is pre-existing and disclosed in addendum 01 |
| `audit_layout.py` on the whole run root | PASS, findings [], 152 files inspected, rc 0 (`final/audit_layout.log`) |

**O2. Suites on the production tree** (no cache, no bytecode; `verification/reviewer_M2_r2b_2/suites/`)

| Suite | Result |
|---|---|
| `tests/topic3_spectral` | 88 passed |
| Old suite (STRICT_E2E; `tests/test_empirical_four_topics.py`, `tests/test_pilot_connectome.py`, `tests/e2e`) | 86 passed, 7 warnings |
| `tests/topic1_lagmotif` | 88 passed |

**O3. Own mutation run on copied trees.**
- Runner: `verification/reviewer_M2_r2b_2/mutants/run_mutants_rev2.py` (sha `b9831339…`).
- Results: `mutants/logs_run1/RESULTS.json` (sha `1780e71a…`), with a raw log and JUnit file for each job.
- Method: full suite, no `-x`, a fresh copy of the base tree for each job. The copied trees were deleted afterwards.

| Group | Result |
|---|---|
| Controls | 88 passed (current suite); 85 passed (suite without `test_verdict_rules_r2b.py`) |
| Iteration-1 challenger_M2_r1_1 survivors, patch strings verbatim (N02, N05, N06, N08, N09, N10, N11, N17) | all killed by the current suite |
| MM06 (zoo `<=`) | survives the 85-test suite; killed by the 88-test suite (2 failed). This confirms the worker's claim. |
| New V-mutants, killed (12 of 16) | V05 (primary counted as its own replicate), V06 (`holds` uses `or`), V07 (labels swapped), V08 (Holm with k = 3), V09 (log contrast swapped), V11 (D1 corr reads the cov interval), V12 (D3 uses corr), V14 (primary CI checked on the lower side only), V18 (bootstrap CI endpoints swapped), V19 (H1b orientation swapped), V25 (zoo sign for H1b taken from H1a), V27 (Holm zip reversed) |
| **New V-mutants, surviving the full 88-test suite** | **V01**, `analysis.py:191` `prim["p_holm"]` changed to `prim["p_signflip"]`; also survives the 85-test suite. V02 (`ci95[0] >= 0 or ci95[1] <= 0`), V03 (D1 `lo >= 0`), V04 (D3 `lo >= 0`). |

**O4. Why V01 survives** (`tests/topic3_spectral/test_verdict_rules.py`)
- `_rec` (lines 33–35) sets `p_signflip = p_holm` whenever `p_raw` is omitted. So every primary-side test gives the primary identical raw and Holm p, including `test_primary_holm_p_at_or_above_alpha_is_not_significant` (lines 92–97).
- The only test with `p_raw` different from `p_holm` is `test_zoo_agreement_uses_holm_not_raw_p` (lines 100–105). It covers the zoo side only.
- In the r2b test and in the real-data regressions, both primary p-values are far below 0.05.

**O5. V01 consequence** (`probes/probe_V01_primary_raw_p.py`, `.out.json`; synthetic inputs only)
- Hand-built case: the primary has raw p 0.03 for H1a and 0.20 for H1b, so the Holm p are 0.06 and 0.20. The H1a CI is [0.005, 0.055]. Three zoo checkpoints agree.
  - Shipped code: `primary_significant` False, outcome "killed (primary CI includes 0)", which is the imprecise label already disclosed in addendum 03 §3.
  - V01: `primary_significant` True, outcome **"holds"**.
- Computed case: 57 per-subject d values, with the card's own `sign_flip_test` at B = 9999. Raw p is 0.0348, the bootstrap CI is [0.022, 0.481] and excludes 0, and the Holm p paired with 0.5 is 0.0696. The outcome again flips from not-holds to **holds**.

**O6. Family B estimand, independent recomputation** (`probes/probe_family_b_estimand.py`, `.out.json`; pinned npz and JSON only; the 4 npz pins are OK)

| Quantity | My value | Addendum 03 / 04 |
|---|---|---|
| Top-7 variance share at L2/LN0L2/L3, minimum over all subjects and checkpoints | 0.99994165 (L5e-5 L3) | "minimum 0.999942" ✓ |
| Count of eigenvalues above 1e-5 × max: median / primary maximum / zoo maximum | 7 / 7 / 8–10 | ✓ |
| L1 top-63 share, minimum | 0.99993998 (HCP) | "≥ 0.99994" is 2.4e-8 short; addendum 04 §6 corrects this |
| L1 counts | 29–60; primary 50–55 | ✓ |
| Primary medians, covPR L2 / L3 | 5.41 / 5.67 | ✓ |
| Primary medians, corrPR L2 / L3 | 5.88 / 6.14 | ✓ |
| Concatenated vs per-frame, maximum \|Δlog\| | 1.1e-4 | ≤ 1.2e-4 ✓ |
| Checkpoint-variance ratios, H1a / H1b | 13.36 / 5.84 | ✓ |
| PR recomputed from stored eigenvalues | max relative error 4e-8 | — |

- The rule recomputed from scratch on the pinned `per_checkpoint` p_holm and CI values gives:
  - H1a **holds**, agreeing checkpoints NewUAH L1e-4 and L5e-5;
  - H1b **not replicated**, agreeing checkpoint L5e-5.
  Both equal the pinned verdicts.
- My within/between SD ratio is 0.0017–0.0055. It uses a different definition (ddof 0, mean within-subject SD), so it is not a mismatch.

**O7. Freeze order** (spot check)
- Card mtime 08:43:40Z, then `card_sha256.txt` 08:48:29Z.
- Family A run `started_utc` 08:49:18Z, Family B 09:01:59Z. Both records carry the card sha `683374565d80…`.

**O8. Addendum 03 provenance**
- `git diff 0db0336 ef27b71` on addendum 03, with masking: one line changed. The literal prefix token in backquotes became "BIDS subject-ID prefix". No number or claim changed. The pre-edit sha is `725d5077…`; the post-edit sha is `73489661…`, which is the pinned one.
- Addendum 03 §4 line 73 and §8 claim mutation evidence in `verification/worker_M2_r2/mutants/` and "mutant runs in copied trees". Neither exists. Addendum 04 §2 discloses this and supersedes both sentences.

**O9. Worker mutation evidence** (`verification/worker_M2_r2b/mutants/`)

| Run | Log hashes matching the record | Survivors | JUnit agrees with the "killed" field |
|---|---|---|---|
| RUN1 | 0 of 69 (overwrite, disclosed) | MM__06 | yes, 0 anomalies |
| RUN2 | 69 of 69 | none | yes |
| RUN3 | 69 of 69 | MM__06 | yes |

- The runner snapshot sha256 values equal the `runner_sha256` recorded in each run's `_meta`.
- The run-3 MM06 log ends "85 passed".

**O10. ID scan.** `grep -rlE 'sub-[A-Za-z0-9]'` over the M2 results, docs, src, scripts, `worker_M2_r2b` and my outputs finds hits only in `tests/topic3_spectral/test_token_job_driver.py`. Those are synthetic names (SYNA01-type), in a test pinned since iteration 1, and so are their transient copies in my copied trees, which are now deleted.

**O11. Context** (not M2 findings)
- The 15-minute checkpoint commits continue. `206681d` (10:31:26 KST) took in my DISPATCH, BRIEFING and progress files. I made no git write.
- Addendum 04 is committed, but `tests/topic3_spectral/test_verdict_rules_r2b.py` and `addendum_04_sha256.txt` are still untracked.
- `src/topic3_spectral/__pycache__/` (cpython-312) was created at 2026-11-01 00:39:14Z by another process, before my work.
- `results/gpu_ledger_2026-10-31.md` now exists. It was created at 01:11:55Z by explorer_M3_r1_2 for M3 B300 smoke and probe jobs and has no M2 rows. So the resume note's "0 GPU-hours" is outdated for the run, but still true for M2.
- The `GATE_STATUS.md` M2 line is stale; addendum 04 §1 says so.
- The CONSOLIDATED_STATUS M2 numbers I checked (ΔcovPR 5.34, ΔcorrPR 6.04) equal the pinned JSON.

## 2. Logic Chain

1. **Computation and verdicts are sound.** By O1, O6 and O7, the pinned outputs are byte-identical, the card preceded the results, and the H1 rule from scratch reproduces both verdicts. Nothing needs rerunning, and no verdict is in doubt.
2. **Blocker (i), the Family B estimand, is closed.**
   - Addendum 03 §1 gives the effective ceiling of 7, near-static spatial cells, a concatenation that adds nothing, and the H4 caveat.
   - §2 supersedes every passage challenger_M2_r1_1 listed: card line 80, card line 98, report line 102 (twice), report line 114, and the R2 row on report line 154.
   - §3 adds the n = 3 confounded checkpoints and the single-subject L1 jackknife.
   - O6 reproduces these numbers independently. The three wording slips are corrected in addendum 04 §6.
3. **Blocker (ii), the verdict-logic guard, is not fully closed.**
   - Card §5 line 89 conditions HOLDS on "the primary checkpoint has Holm p < 0.05 with its CI excluding 0".
   - By O3 and O4, no test fails when the primary reads the raw p.
   - By O5, that defect is reachable on ordinary data: any primary raw p in [0.025, 0.05) that is the smaller of the pair, which is a much larger region than MM06's exact tie. It flips not-holds to holds.
   - That is the same class as iteration-1 N08 (the zoo-side raw p) and as N05 (a silent verdict flip). The worker itself treated MM06, a smaller and tie-only case, as requiring a new test.
   - Addendum 03 §4's "Holm p is used, not raw p" is therefore overbroad.
   - So C3 ("fixtures that fail on the targeted defect") is not met for the primary significance condition of the replication rule.
4. **Why this differs from the challenger's literal closure condition.**
   - challenger_M2_r1_1 wrote: "If a rule-logic test is added and N05/N06/N08–N11 are killed, finding 3 is closed." That condition is met (O3).
   - But it was shorthand for the mutants that challenger happened to run. The dispatch and C3 ask whether the verdict logic is guarded.
   - This explains why my verdict can differ from a peer APPROVE that relied on the challenger's condition.
5. **Severity.**
   - The blast radius on the current results is zero: `analysis.py:191` is correct and hash-pinned, and the real primary p_holm is 0.0002.
   - It is still a reachable, verdict-flipping hole in the regression guard. The dispatch says APPROVE only if every criterion is met.
   - The fix is one additive test file plus an addendum receipt. It needs no code edit, rerun or card change.
6. **V02–V04 are practically unreachable.** They need an interval endpoint exactly equal to 0.0 from continuous bootstrap or subsampling statistics. This is unlike MM06, whose 0.05 tie is reachable on the discrete p lattice. They are non-blocking siblings that the same new test can cover.
7. **Not an integrity violation.**
   - The dangling pointer in addendum 03 (O8) fabricated no artifact. It was a forward claim by a writer interrupted 10 s later, and addendum 04 §2 discloses and supersedes it.
   - The worker's run-1 log overwrite is disclosed, and RUN3 reproduces it with hash-matching logs (O9).
   - No hard-coded results or facade logic were found.

## 3. Caveats

- I did not rerun the full Topic 3 analysis. I recomputed the rule and the estimand numbers from the pinned npz and JSON, and the iteration-1 verifiers had already rerun it.
- My mutant set is 25 mutants, not exhaustive. Areas I did not probe with new mutants:
  - `scripts/topic3_token_stats.py` wiring (PRIMARY label, seeds). These are hash-pinned and already ran, and the outputs are pinned.
  - Estimator internals beyond the earlier sets.
- I accept T3.1 (provenance and J1), T3.2 and T3.3 on the strength of the passing fixtures plus the iteration-1 verifiers' independent work, which I spot-checked through the freeze order and the tests.
- Random-init control H2 is pre-specified and still UNTESTED (card §6). T3.2 says "such as", and the card does carry a column-permutation (shuffled) null and an iid reference. I treat this as a disclosed limitation, not a blocker.
- The two interruption times stay root-reported. Addendum 03's header says "about 12:30Z", but the root reports 12:17:16Z (minor).
- Other r2b verifiers (reviewer_M2_r2b_1, auditor_M2_r2b_1, challenger_M2_r2b_1/2) ran in parallel. I did not read their outputs.

## 4. Conclusion

**REQUEST_CHANGES.**

**Blocking issue:** add a regression test, then record its sha256 in a dated addendum receipt. The test:
- primary record with `p_signflip` < 0.05 ≤ `p_holm`, for example raw 0.03 and Holm 0.06, with a CI excluding 0;
- three agreeing, significant zoo checkpoints;
- assert `primary_significant is False` and that the verdict is not "holds", for both H1a and H1b.

It must pass on the shipped code and kill V01. Optional additions to the same file are V02, V03 and V04: a primary CI with lower bound exactly 0.0, and D1/D3 intervals with lo exactly 0.0, which must count as not excluding 0.

**Non-blocking issues:**
- (a) Addendum 03 §4's "Holm p is used, not raw p" should be scoped to the zoo side in the next addendum.
- (b) Addendum 03 §2's R2 restatement ("No reduction … 3 of 4 checkpoints") holds only for the norm-matched H1a. Under H1b (raw covPR L3 vs L2), HCP_N400 falls by about 11% and L1e-4 by about 3%.
- (c) The addendum 03 header time "about 12:30Z" differs from the root-reported 12:17:16Z.
- (d) The git state is inconsistent: addendum 04 is committed but its test and receipt are not (root's domain).
- (e) There is a stray `__pycache__` in `src/topic3_spectral`.

Everything else in M2 is verified: numbers, verdicts, freeze order, estimand correction, C1/C2/C4–C8 and layout.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt          # rc 0, 67 OK
for f in output_sha256.txt addendum_02_sha256.txt addendum_03_sha256.txt addendum_04_sha256.txt; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/$f; done
bash verification/reviewer_M2_r2b_2/suites/run_suites.sh      # topic3 88, old 86, topic1 88
# mutants (copied trees only; refuses to overwrite an existing logs dir)
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_M2_r2b_2/mutants/run_mutants_rev2.py logs_run2 5
#   expect survivors_88 = [V01_primary_uses_raw_p, V02_primary_ci_closed, V03_D1_cov_lo_ge, V04_D3_lo_ge]; survivors_85 = [MM06, V01]
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_M2_r2b_2/probes/probe_V01_primary_raw_p.py      # shipped not-holds, V01 holds
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_M2_r2b_2/probes/probe_family_b_estimand.py      # rule_from_scratch == pinned
python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py .agents/teamwork/tw-20261031-four-topics   # PASS
```

**Invalidation conditions:**
- If a test with primary raw p < 0.05 ≤ Holm p is added and kills V01 (the runner above, with that file in the base tree), the blocking issue is closed.
- If V01 is shown to be killed by the current 88-test suite, this finding is withdrawn.
