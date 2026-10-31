# handoff — challenger_M1_r1_1 (M1 Topic 1 hardening + full-cohort step 5) — Hard handoff

**Verdict: CONFIRMED.** The Topic 1 KILLED verdict follows card §5 from correctly joined, bit-reproducible features. Every headline number reproduces independently. T1.1–T1.5 hold. Four non-blocking issues are listed in §4. The most important is that the analyze-path wiring has no gating test.

Probes and outputs: /home/juke/git/00IITP-AI/verification/challenger_M1_r1_1/ (SHA256SUMS.txt lists 20 files, sha c6797d9b…).

## 1. Observation

**Hashes and C1/C2**

| Check | Result |
|---|---|
| C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` from the repo root | rc 0 |
| Card §12 code hashes | 10/10 OK |
| Card sha | 1e589f0b…75aa |
| `results/topic1/2026-10-31/RESULTS_SHA256SUMS.txt` | all OK |
| Hashes of the 12 governing artifacts | equal to the worker's `frozen_artifacts_sha256`: stats script 33e27576…, jsonl 948961c8…, stats_results 1713e370…, addendum 7ccb983e…, report 1542055d…, and the others |
| `pytest tests/topic1_lagmotif` | 88 passed (c2_topic1.log) |
| Old suite, STRICT_E2E | 86 passed, 7 warnings (c2_old.log) |

**P1 — join integrity on all rows** (p1_join_structure.out.json).
- I built my own name → (Sample, OCD, Age, Sex) map from the CSV and `sorted(os.listdir)`. Result: 1706 names, all present in the metadata, IDs unique, OCD 869, HC 837, NaN 0.
- I read raw lengths straight from the npy files. `raw_valid_T` equals both manifest.json and the jsonl for all 1706 rows (a per-file fingerprint).
- jsonl: 1706 lines and 1706 unique positions, exactly 0..1705. All rows ok, and every row carries params hash 86863ffa….
- site, tr (via tr_table), n_trim, valid_T, duration and grid_len match the manifest and the rules.
- Over 10,236 unit rows:
  - E1 == Z030C exactly;
  - E2 == Z030C − Z030T exactly;
  - the rank-2 identity holds to a maximum deviation of 3.3e-13;
  - |ΣSP² − 1| ≤ 6.7e-16;
  - n_null = 1000 and m = round(d·46056) everywhere;
  - Z recomputed from obs, mean and sd differs by 0.0;
  - each degeneracy flag equals the sd = 0 condition.
- The script's `load_design` gives dx, site, age, sex and logdur identical to my map (dx vector sha 67515809…).

**P2 — re-extraction of 10 positions** (55, 57, 654, 1103, 1104, 1280, 1332, 1530, 1578, 1599).
- Chosen label-free: one per TR (0.7 to 2.0), A3 subject 57, the lowest-acceptance subject, and one degenerate@0.05 subject.
- Run with frozen PARAMS. 10/10 bit-identical to the saved rows (`json.dumps` equality of all 6 units, gradient_share and the length fields) (p2_reextract.out.json).

**P3 — independent statistics, script not imported** (p3_independent_stats.out.json).

| | E1 | E2 |
|---|---|---|
| β_FE (numpy; matches statsmodels `C(site)+C(sex)`) | 0.548815 | 0.343871 |
| d from my own numpy ML random-intercept LMM with Mundlak terms | 0.1131306 | 0.0376887 |
| d from statsmodels | 0.1131307 | 0.0376888 |
| Freedman–Lane by explicit refit, card seed stream | p = 0.0223 (exact) | p = 0.4416 (exact) |
| Freedman–Lane, independent seed 777 | 0.0233 | 0.4424 |

- Holm gives 0.0446 for E1, and the verdict is KILLED.
- My secondary analyses reproduce the worker's:
  - Family 2: n = 856, 23 sites, std β 0.0319 / 0.0288.
  - Family 3: codes 180 / 121 in 11 sites, β −0.552 / −2.162, d_FE −0.086 / −0.199.
  - Acceptance-stratified: n = 1535.
  - Gradient-share means: OCD 0.217, HC 0.233.

**P4 — production `analyze` rerun on a copy of the outdir** (analyze_copy/).
- `stats_results.json` is identical except elapsed_s.
- Every number in the result report matches the saved output, including:
  - AUROC 0.5157 [0.468, 0.560] and 0.5630 [0.524, 0.600];
  - log ratio d 0.0897, p 0.0665;
  - acceptance-stratified E1 d 0.1296, p 0.0143;
  - 0 exclusions in every class.

**P5 — 17 NEW stats mutants, full topic1 suite** (p5_stats_mutants.out.json).
- **Killed (8):** holm→bh in the verdict, Manly raw-y permutation, nuisance omits age, nuisance omits logdur, d sign flip, D_MIN 0.10, ALPHA 0.10, rank guard disabled.
- **Survived (9):** `endpoint_value` E1/E2 swap, dx coding flipped in `load_design`, `reml=True`, Mundlak stop disabled, degenerate NaN filled with 0, outcome reversed against the design (misalignment), primary unit = curl, B_PERM 999, family-1 Z030C/Z030T swap.
- The worker's analyze smoke probe (`verification/worker_M1_r1/probe_analyze_smoke.py`) prints results but asserts nothing.

**P6 — runtime guard for the dx flip.** `card_count_check` on the real metadata, labels only, raises StopForReview for a mutated `load_design`. The 5 mismatched counts include n_ocd and n_hc.

**T1.1 rerun** (t11/).
- Adapted copies of the auditor harnesses; their mutant definitions are AST-equal to `verification/victory_auditor_1/`.
- With the new tests: control 89 passed, 19/19 + 4/4 killed.
- Without them: roi_subsample_80 plus the 4 extra mutants survive, which reproduces the 5 audit survivors.

**P7 — ID scan.** 2095 IDs (min length 16), token and substring match, over 184 files of M1 outputs, tests, worker probes, my probes and both metadata folders: 0 files with a hit.

**P8 — non-blocking calibration check.** Freedman–Lane null FPR at B = 9,999 on the real design, R = 1000:

| Scenario | FPR at α = 0.05 | 3-SE band |
|---|---|---|
| S1 aligned | 0.044 | [0.029, 0.071] |
| S5 adversarial (OCD noise SD 1.3× HC) | 0.047 | same |

The worker's V2b value of 0.077 at R = 300 was chance.

**P9 — planted-effect recovery on the real design, own numpy ML-LMM, script not imported, 200 reps per cell** (p9_planted_own_lmm.out.json).

| Site effects | Planted d = 0 | 0.15 | 0.30 |
|---|---|---|---|
| Independent | −0.005 | 0.152 | 0.298 |
| Aligned with site OCD fraction | −0.005 | 0.156 | 0.300 |

- Every cell is within 3 MC-SE of its planted value.
- At a true d of 0.15, 52.5% of runs reach |d̂| ≥ 0.15. This matches the operating characteristic disclosed in card §5 (about 50%).

**Validation and run-log chain.**
- `stats_validation_final.json` binds script 33e27576 and has all_pass true. Its numbers:
  - V1: maximum |t_vec − t_sm| = 2.2e-13;
  - V2 FPR: 0.0545, 0.0525 and 0.0435;
  - V2b: 0.0767 at R = 300;
  - V3: 0.0005, 0.1426 and 0.3031;
  - V4: pass.
- `extract_primary.log` line `09:27:48Z finished ok=1706 err=0 … jsonl_sha256=948961c8…`. The header json carries card 1e589f0b, params 86863ffa and manifest 063513c9.
- `fallback_decision.json` (11:14:54Z) and `stats_results.json` embed the same jsonl sha 948961c8 and script sha 33e27576.

**Freeze provenance** (git checkpoint commits, made by an external auto-checkpoint process and not by the worker).

| Item | External anchor |
|---|---|
| Card 1e589f0b | committed e694dae at 2026-10-31 07:31Z, before the extraction started (08:16Z) |
| Addendum (substance) | commit 3bdbc9c at 11:01:25Z, before the label join; it already contains all P/V/G/D items |
| Addendum (frozen bytes 7ccb983e) | first committed 7497e6a at 11:16:25Z, which is 82 s after `analyze` started (11:15:03Z) |
| Stats script 33e27576 | none: untracked. Only its mtime (09:08Z, before the extraction finished at 09:27Z) and the worker-written `stats_script_sha256.txt` (11:14:46Z) |

- The diff 3bdbc9c → 7ccb983e is freeze bookkeeping only: the timestamp line and the hash list.
- Order on disk: `fallback_decision.json` 11:14:54Z, then analyze.log 11:15:03Z, then the result 11:16:21Z.
- No worker probe before 11:14:46Z joined labels to features. probe_card_counts reads labels only; probe_analyze_smoke is fully synthetic.

**Worker timestamps.** `worker_M1_r1/progress.md` has mtime 11:33:32Z but contains entries stamped "11:40Z" and "Last visited 11:40Z". The result report's actual mtime is 11:32:48Z.

## 2. Logic Chain

1. The kill rests on E1 |d| = 0.113 < 0.15. E1's p_Holm of 0.0446 already passes, so p calibration cannot change the verdict.
2. The failure that could fake a kill is position ↔ file ↔ label misalignment, or wrong features. P1 rules out misalignment: an independent map, raw-length fingerprints on all 1706 rows, no duplicates. P2 rules out non-reproducible or wrong saved features for 10 diverse positions.
3. P3 recomputes d with an LMM fitted without statsmodels and gets 0.11313. That is 0.037 below the bar. P3 and P4 also reproduce p_FL, Holm and every secondary number. So the verdict follows card §5 from correct inputs.
4. Card-rule details checked against code and outputs:
   - d = β_LMM/√scale, ML fit, Mundlak means of dx, age, sex and logdur;
   - Freedman–Lane within site with B = 9999, seed 20261031, p = (1+#)/(B+1);
   - Holm over exactly E1 and E2;
   - the fallback rule is strict, and 0/1706 subjects are degenerate;
   - §7 analyses are skipped because nothing survived.
5. The P5 survivors show that the analyze wiring is not gated by the test suite. Point 3 shows that this run's wiring is correct, so this is a coverage gap for future reruns and edits, not a defect in the delivered result.
6. Freeze order is supported by mtimes, by the internal records and by the 11:01Z commit of the addendum substance. The final frozen bytes and the script hash have no pre-join git anchor. Under C4 (no commits allowed) none could exist, and point 3 makes the verdict independent of post-hoc script edits.

## 3. Caveats

- I did not re-review statistical design choices that card §4–§6 already fixes, nor the §9 latency / global-signal confound. The confound is a limitation of interpretation, which the worker reports, not an implementation error.
- I re-extracted 10 of 1706 subjects. The other rows are checked structurally and by raw-length fingerprint only.
- The site-bootstrap and PCA classification are reproduced by rerunning the production code (P4), not by an independent re-implementation.
- The npy preprocessing provenance (GSR, slice timing) and the 833/873 vs 869/837 count conflict are open upstream issues and were not investigated.
- The checkpoint commits that include M1 docs and metadata (author shown as the user's account, every 15 min) are not the worker's. Whether they were pushed was not checked. results/ and scripts/ are untracked.
- I used `git show <commit>:<path> | sha256sum` and `git grep -l` on M1 paths only, never `--stat` or `--name-only`.

## 4. Conclusion

**CONFIRMED.** Topic 1 is KILLED under card §5 at broadband@0.10:
- E1: d 0.113 (fails |d| ≥ 0.15), p_FL 0.0223, p_Holm 0.0446.
- E2: d 0.038, p_Holm 0.44.
- n = 1706 (869 / 837), 23 sites, 0 exclusions, no fallback.

T1.1–T1.5 are satisfied as claimed.

Non-blocking findings for the root:

| ID | Severity | Finding | Mitigation |
|---|---|---|---|
| N1 | medium, test coverage | 9 of 17 new mutants in the cmd_analyze / run_primary / `_units_frame` / `endpoint_value` / `load_design` wiring survive the full suite, because the smoke probe has no assertions. | Add an end-to-end synthetic analyze test with a planted E1-only effect. Assert the E1/E2 values and signs, the unit key broadband@0.10, n_excluded_degenerate, B = 9999, `reml` ML (scale = RSS_GLS/n), and the Mundlak-stop firing. |
| N2 | low, provenance | The stats script sha and the final addendum bytes have no external anchor before the label join (substance anchored 11:01Z). | None needed for this verdict. Future cards should anchor hashes outside worker-writable storage before the join. |
| N3 | low | Future-dated entries (11:40Z) in worker_M1_r1/progress.md. | — |
| N4 | info | The card §12 independent-review requirement was only partly met by the worker; this challenge is one fresh native review of that chain. | — |

## 5. Verification Method

From `/home/juke/git/00IITP-AI`, using `/home/juke/superclaude-env/bin/python3` with `PYTHONDONTWRITEBYTECODE=1`:
- `verification/challenger_M1_r1_1/p1_join_structure.py` (about 4 s)
- `p2_reextract.py` (about 3 min, 10 processes)
- `p3_independent_stats.py` (about 16 s)
- production analyze on a copy: `scripts/topic1_cohort_stats.py analyze --outdir verification/challenger_M1_r1_1/analyze_copy`, then `p4_diff_analyze.py`
- `p5_stats_mutants.py` (about 40 s)
- `p6_dxflip_guard.py`
- `p7_id_scan.py`
- `p8_fpr_b9999.py 1000` (about 2 min, 8 processes); `p9_planted_own_lmm.py` (about 6 s)
- T1.1: in `t11/`, run `TAG=x python3 -B mutants.py` and `mutants_extra.py`, with and without `EXCLUDE_NEW=1`

**Invalidation:** any change to the jsonl (948961c8), manifest (063513c9), stats script (33e27576), metadata CSV, or `src/topic1_lagmotif` (card §12) invalidates this report.
