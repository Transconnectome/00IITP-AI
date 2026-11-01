# Handoff — challenger_M4_r1_1 (M4 / Topic 4), Hard handoff, 2026-11-01T03:25Z

**Verdict: CONFIRMED.** The worker's T4.1–T4.3 claims hold under independent recomputation, adversarial inputs and new mutants.
- H1 stop, S1 killed, S2 supported, S3 non-inferior.
- No blocking defect was found.
- Four non-blocking findings are listed below.

Probe code and outputs are in `/home/juke/git/00IITP-AI/verification/challenger_M4_r1_1/`. Nothing in production paths was modified (git-status snapshots before and after; see §5).

## Challenge Summary
**Overall risk assessment: LOW.** It is not zero: fixture coverage of the verdict machinery is weak, but none of the gaps changes a number or a verdict in this run.

## 1. Observation

### O1. Freeze chronology
- The card `docs/03_empirical_analysis/topic4/2026-11-01_topic4_analysis_card.md` was born at 02:03:57Z and has the same modify time, so it was never edited. Its sha256 is `2b535c39…5934`, and the file is mode r--r--r--.
- `card_sha256.txt` and `code_sha256_at_freeze.txt` were born at 02:04:41Z.
- The first rows of `run_ledger.jsonl` (born 02:04:52Z) are:
  - `tuning_start` 02:04:52Z;
  - `confirm_start` 02:07:43Z.
- Both rows carry the card sha.
- No earlier ledger exists, and `verification/worker_M4_r1/probe_2_smoke.py` uses synthetic VARs only.
- `LC_ALL=C sha256sum -c card_sha256.txt code_sha256_at_freeze.txt docs_sha256.txt` gives 0 non-OK lines, both before and after my work.
- Git: the first commit containing these files is a post-result root checkpoint (c967f7c, 11:16 KST = 02:16Z).

### O2. Integrity guard really refuses
- `scripts/topic4_run.py::verify_integrity` on temp copies returns:
  - `clean ACCEPTED`;
  - card-hash tamper → `REFUSED: card sha256 mismatch`;
  - `local/psp.py` hash tamper → `REFUSED: code changed since the card was frozen`;
  - manifest tamper → `REFUSED: split manifest sha256 mismatch`.

### O3. Raw outputs untouched
- All 55 `confirm/*.json` match the `output_sha256` recorded in their ledger rows (0 mismatches).
- Their mtimes fall between 02:08:14Z and 02:14:21Z.
- `confirm_summary.json` reports 55/55 ok.
- **Finding F1:** `LC_ALL=C sha256sum -c results/topic4/2026-11-01/output_sha256.txt` prints `results/topic4/2026-11-01/logs/analyze.log: FAILED`.
  - The recorded hash is `e3b0c442…b855`, the hash of an empty file.
  - The current file is 1055 bytes, with hash `774d9f94…6313`.

### O4. Independent data path and reference arms (`indep_refs.py`, `indep_refs.out.json`)
This script does not import `src.topic4_resu`. It uses its own loader (csv module), the Topic 1 TR table, its own split hashing, its own least-squares detrend, and its own ridge and R².
- Population, sites, valid_T, raw_valid_T and the role/fold split all equal the manifest: n_primary 1195, 13 sites, 0 errors.
- Per-subject R² of constant, persistence, identity ridge and PCA-24 match the saved `fold*_refs.json` at both horizons, with max |Δ| ≤ 9.5e-15. λ choices are identical.
- Persistence mean at 2 s: −0.28623.
- Per-site lag-1 autocorrelation ranges from 0.149 (Braga-1.5T) to 0.481 (Yale-2014). No site is an outlier.

### O5. Independent statistics (`indep_stats.py`, `indep_stats.out.json`)
Own assembly; own crossed bootstrap (PCG64 seed 987654321, B = 4000); card §6 rules re-typed from the card text.
- Point estimates are identical to `verdict.json`. CI endpoints agree within |Δ| ≤ 2.1e-4.
- Verdicts agree: H1 stop, S1 killed, S2 supported, S3 non-inferior.

| Contrast | Point | Independent CI | Level |
|---|---|---|---|
| H1 | −0.002231 | [−0.00411, −0.00029] | 95% |
| S1 | −0.001597 | [−0.00362, +0.00051] | 98.33% |
| S2 | +0.030616 | [0.02880, 0.03230] | 98.33% |
| S3 | −0.004669 | [−0.00502, −0.00429] | 98.33% |

- The H1 point is negative in every fold: −0.0024, −0.0015, −0.0024, −0.0020, −0.0028.
- C4 > C1 in only 12.3% of subjects.
- Unstable runs: C3 10/50; every other class 0.

### O6. Determinism rerun (`rerun_subset.py`)
- The worker's frozen code was run into my own outdir and cache, and `verify_integrity` passed.
- 14 tasks were rerun: psp:C1 and psp:C4 × 5 folds, psp:C3 fold 2, psp:C4DP fold 0, mlp:0 fold 0 (torch) and refs fold 0.
- All 14 outputs are byte-identical to the saved ones.
- The C3 failures reproduced at the same updates (steps_done 261, 46, 54).

### O7. Independent PSP engine (`indep_psp.py`, `indep_psp.out.json`)
- Built from the card §4 equations, with a Cholesky lateral solve, my own data path and masks from the PROTECTED legacy generator.
- Instances checked: C1 g0, C4 g0, C5 g0 (fold 0); C1 g7, C4 g7 (fold 3); C4 g29 (fold 2).
- All match the saved per-subject R² at h = 1 and h = 2, with max |Δ| ≤ 4.3e-11. λ and rank(F) are identical (C1 rank 5, C4 rank 4–5, C5 rank 24).

### O8. Stability monitor on real data (`indep_c3_stability.py`)
- My own per-update ρ(I − D⁻¹M) / λ_min check on fold-2 C3:
  - g2, g4 and g6 first fail at updates 260, 45 and 53, with ρ 1.5326, 1.0339 and 1.4538. These equal the saved monitor values;
  - g0 and g1 stay below 1.
- **Finding F3:** for stable g0, my max ρ is 0.8318 versus 0.8620 saved.
  - Cause: my preprocessing differs from the worker's by ≤ 1.26e-12 (lstsq versus scipy detrend; all 1195 subjects differ at that level).
  - On the identical input matrix, my loop and the worker's `MaskedPSP` are bit-identical (max ρ 0.8620, final W relative difference 0.0).
  - So the C3 trajectory amplifies a 1e-12 input perturbation to a 0.03 change in max ρ. C1, C4 and C5 move by ≤ 4e-11 in R² under the same perturbation.

### O9. T4.1 every-subject check (`t41_vmd_rows.out.json`)
- Source: VMD cache `/home/juke/git/enigma_ocd_mbbn/data/vmd_cache_4ch_464_head.mmap`, rows 0–11. The legacy run used 10 rows (`src/run_all_empirical_experiments.py:47`, `fractal_motif_resu.py:473–475`).
- Every row has exactly 177 valid rows, as a prefix.
- Every row has 0 test-target rows (index ≥ 325) inside the valid portion.
- Test ss_tot ranges from 9.2e-46 to 8.1e-45.
- `src/fractal_motif_resu.py:425` is `forecast_r2 = float(max(-1.0, 1.0 - ss_res / max(ss_tot, 1e-8)))`.
- The legacy `empirical_results.json` reports future_bold_forecast_R2 mean 1.0, std 0.0, for n = 10.
- Context: only 362 of 1706 cache rows have any test row inside their valid portion.

### O10. Topologies
- C1, C2 and C4 each give 30 distinct graphs, and `make_mask` equals the protected generator for all g.
- C4DP versus C4 differs in 82, 96 (median) and 104 (min/median/max) of 138 possible pairs, with identical degrees.
- C4DP has 1–5 designated-hub edges, against C4's 0.

### O11. `topic4_analyze.py` end to end (`planted_analyze.py`, `planted/planted_report.json`)
- The unmodified script ran on copies of the real confirm outputs with planted C4, C4DP or MLP scores.
- It returned the card-expected verdict in 8 of 8 scenarios:
  - keep;
  - modify;
  - null → stop;
  - 13.3% unstable → "inconclusive (execution integrity)";
  - exactly 10% unstable → keep (the rule says "more than 10%");
  - inconclusive (point 0.005, CI [−0.0024, 0.0125]);
  - S3 inferior;
  - −0.02 → stop.

### O12. New mutants against the FULL 67-test suite (`mutants/run_mutants_ch.py`, `mutants/mutation_results_ch.json`)
- Control: 67 passed.
- **Killed (7):**
  - boot_never_resamples_instances;
  - class_scores_impute_failed_as_zero;
  - pairs_cross_subject_boundary;
  - lambda_selected_on_test;
  - persistence_uses_target;
  - c4_ignores_instance_seed (caught only incidentally, by the C4DP test);
  - guard_eps_negligible.
- **Survived (9) — Finding F2:**
  - `stats.py`: boot_ignores_site_strata, h1_keep_rule_lo_gt_delta, superiority_drops_point_clause, noninferiority_uses_point;
  - `pipeline.py`: readout_not_refit_on_val;
  - `topologies.py`: c4dp_single_swap_sham;
  - `local/psp.py`: eta_schedule_no_decay;
  - `diagnostics.py`: monitor_lax_threshold (ρ < 1.5 and no λ_min check);
  - `baselines/backprop.py`: mlp_early_stopping_on_train. The F11 docstring says early stopping must use inner-val, but the test does not check it.
- `scripts/topic4_analyze.py` has no fixture at all.

### O13. Report numbers
- Every number in `2026-11-01_topic4_result_report.md` §1 and §3 equals `verdict.json` or my recompute.
- The C3 per-fold failure counts 2, 2, 3, 1, 2 match the ledger.
- **Finding F4:** report §2 says "So the rule recovers the principal subspace on real BOLD". The evidence is equal R² (0.1369 versus 0.1370) and rank 24. Subspace alignment was not measured on real data.

### O14. Hygiene
- Tests: `tests/topic4_resu` 67 passed; old suite (STRICT_E2E=1) 86 passed; `tests/topic1_lagmotif` 88 passed.
- PROTECTED_HASHES rc 0, before and after.
- Participant-ID scan of 334 files (Topic 4 code, outputs, docs, worker and challenger verification, both metadata folders): 0 hits.
- `audit_layout.py` on the run root: 186 files, 0 findings.
- My ENIGMA-derived cache (scratchpad) is deleted, and none of my processes are left.
- 0 GPU-h. No B300 contact.

### O15. Analysis rerun on an unmodified copy (`verification/challenger_M4_r1_1/analyze_rerun_on_copy.log`)
- `scripts/topic4_analyze.py --outdir <copy of results/topic4/2026-11-01>` returned rc 0.
- The resulting `verdict.json` is byte-identical to the saved one (sha 437161ed…5c22). The copy was deleted afterwards.

### O16. No-backprop evidence (T4.3)
- My run of `tests/topic4_resu` (67 passed) includes the three-part proof: the AST scan of `local/`, the runtime-block subprocess with torch, jax and the other frameworks set to None, and target-shuffle invariance of the engine digest.
- Stronger, output-level evidence comes from O7. My numpy-only engine was written from the card §4 equations, takes no targets and imports no autograd library, and it reproduces the saved PSP per-subject R² to ≤ 4.3e-11. The saved local-engine outputs therefore equal a computation that is backprop-free by construction.
- One more point: in the confirm pool the MLP tasks ran first (`topic4_run.py:199`), so torch was already imported in some forked workers when they later ran PSP tasks. The output-level reproduction makes this irrelevant.

### O17. Metadata deviation (mine)
- `DISPATCH.md` holds the computed task text verbatim, except the worker's ~12k-character handoff JSON, which is condensed to its verifiable claims and labelled as condensed.
- I did not attempt a verbatim re-copy, to avoid producing a "verbatim" file that contains transcription errors. The full JSON is in the root coordinator's dispatch and in `worker_M4_r1/handoff.md`.

## 2. Logic Chain
1. O4 and O7 reproduce, with independent code, the per-subject scores of the arms that enter H1, S2 and the references, to ≤ 4e-11. The worker's own recompute (`verification/worker_M4_r1/independent_recompute.py`) only re-read the same JSONs. My check reaches back to the raw npy, so the saved scores are correct, not just consistent.
2. O6 shows that the remaining saved arms (C4DP, MLP, C3) come deterministically from the frozen code. O3 shows that none was altered after the run.
3. O5 applies the card §6 rules, re-typed from the card, to those scores. Every verdict matches `verdict.json`.
   - H1's CI_hi of about −0.0003/−0.0004 lies far below δ = 0.01, and is below 0. The stop verdict therefore holds for every positive δ.
   - It is also robust to the declared anti-conservatism of the cross-fitted CI. The upper half-width is 0.0018 (hi −0.00042 minus point −0.00223). Reaching δ would need a half-width of 0.0122, about 6.7 times wider.
   - O15 adds that the saved `verdict.json` is byte-identical to a fresh run of the frozen `topic4_analyze.py` on an unmodified copy. It is the script's output, not an edited file.
   - The per-fold signs (5/5 negative) agree.
4. O1 and O2 show the card and code hashes were fixed before tuning (02:04:52Z) and confirm (02:07:43Z), and that the run script enforces them. The card was frozen before results; the evidence is filesystem and ledger only (see Caveats).
5. O9 shows that all 10 (indeed 12) legacy subjects had their entire chronological test window inside zero padding, with ss_tot ≈ 1e-45, plus the floor at :425. This explains R² = 1.0 for every condition. T4.1 holds for every subject the legacy run used, not only position 0.
6. O11 shows that the untested analysis script implements the card's decision logic on all branches, including the 10% integrity boundary. O12's surviving mutants therefore indicate weak fixtures, not wrong code. For each survivor, the real behaviour was confirmed independently:
   - refit-on-val and the η schedule, by O4/O7 exact matches;
   - the strata bootstrap, by O5's stratified CIs within Monte Carlo error;
   - the verdict rules, by O5 and O11;
   - sham strength, by O10;
   - the monitor threshold, by O8;
   - MLP early stopping, by code (`src/topic4_resu/baselines/backprop.py:61` uses `xv, zv`) and the byte-identical rerun.
7. Hence CONFIRMED, with non-blocking findings F1–F4.

## 3. Caveats
- **Freeze evidence.** Under C4 there are no agent git commits, so no git commit anchors the card before results; sci-pipeline G5 asks for a protocol commit before the result commit. The chronology rests on inode birth times and the append-only ledger. These are consistent, but they are not tamper-evident in the way a commit is.
- **Partial rerun.** Only 14 of 55 confirm tasks were rerun. C2, C0, C5 and mlp seeds 1–2 rely on O3 (hashes) and on code identity, not on regeneration.
- **PSP subset.** The independent PSP check covered 6 of 150+ PSP instances (C1, C4, C5). C4DP and C2 were not re-implemented independently.
- **MLP baseline.** Not independently re-implemented. Its adequacy rests on the worker's Q5/F11 and the byte-identical rerun.
- **Wider scientific questions not addressed.** Whether a 6000-update budget, the ROI subset or a different δ would change the scientific conclusion. The card declares these as limitations.
- **No external review.** The independent pipeline-reviewer / sci-pipeline §6 review is still not done. The gate decision belongs to the PI.

## 4. Conclusion

| Criterion | Status | Basis |
|---|---|---|
| T4.1 | **CONFIRMED** | Padding + floor artefact verified for all legacy subjects (O9). |
| T4.2 | **CONFIRMED** | Non-saturating task (persistence −0.286, identity 0.153, reproduced from raw npy); card frozen before tuning and confirm (O1, O2). |
| T4.3 | **CONFIRMED** | Scores reproduced (O4, O6, O7); stability monitored and reproduced (O8); verdicts follow the card (O5, O11). |

Non-blocking findings:

**F1 (Low).** Re-pin `logs/analyze.log` in a dated receipt, without editing the frozen card. The current `output_sha256.txt` fails its own `sha256sum -c`.

**F2 (Medium, fixture coverage).** Add the following tests:
- planted-verdict tests for `topic4_analyze.py`;
- boundary cases for `verdict_h1`, `verdict_superiority` and `verdict_noninferiority`:
  - point < δ with lo > 0;
  - point > −δ with lo < −δ;
- a strata-dependence test for the bootstrap;
- a monitor threshold test (ρ just above 1 must fail);
- a C4DP minimum-rewiring test;
- an η-schedule test;
- refit-on-val and early-stopping-on-inner-val checks.

None changes this run's results.

**F3 (Low).** C3's stable or unstable status is numerically fragile, at the 1e-12 input level. The C3 failure count (10/50), its descriptive R², and the exploratory Spearman +0.28 that C3 drives are platform-dependent. This supports the integrity exclusion; no verdict uses C3.

**F4 (Low, wording).** Report §2 should say "consistent with recovering the principal subspace (equal R² to PCA-24, rank 24)". Subspace alignment was not measured on real data.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
PY=/home/juke/superclaude-env/bin/python3; V=verification/challenger_M4_r1_1; R=results/topic4/2026-11-01
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?   # 0
LC_ALL=C sha256sum -c $R/card_sha256.txt $R/code_sha256_at_freeze.txt $R/docs_sha256.txt | grep -vc ': OK$'        # 0
LC_ALL=C sha256sum -c $R/output_sha256.txt | grep -v ': OK$'          # F1: analyze.log FAILED (only line)
nice $PY $V/indep_refs.py /tmp/x_refs.json                            # max_abs_diff <= 1e-14, *_equal true
$PY -I $V/indep_stats.py $R /tmp/x_stats.json                         # verdicts stop/killed/supported/non-inferior
nice $PY $V/indep_psp.py /tmp/x_psp.json                              # max_abs_diff <= 5e-11
nice $PY $V/indep_c3_stability.py /tmp/x_c3.json                      # g2/g4/g6 fail at 260/45/53
nice $PY $V/planted_analyze.py                                        # 8/8 match (rewrites $V/planted/)
cd $V/mutants && nice $PY run_mutants_ch.py 3                         # control 67 passed; 7 killed / 9 survived
```
- `rerun_subset.py OUTDIR CACHE` needs a fresh outdir and an own cache directory. Afterwards, `cmp` each `OUTDIR/confirm/*.json` against `$R/confirm/`.
- Delete the cache after running.

The conclusion is invalidated if any of the following holds:
- `indep_refs` or `indep_psp` differences exceed 1e-8;
- any `indep_stats` verdict differs from `verdict.json`;
- any rerun file differs;
- the freeze hashes fail;
- a VMD row among 0–9 has more than 325 valid rows.

## Stress Test Results
- Re-implemented the reference arms from raw npy → expected equal → max |Δ| 9.5e-15 → **pass**
- Re-implemented the PSP engine (6 instances) → expected equal → max |Δ| 4.3e-11 → **pass**
- Bootstrap with an independent RNG → expected within Monte Carlo error → max |Δ| 2.1e-4 → **pass**
- Determinism rerun (14 tasks) → expected byte-identical → identical → **pass**
- Tampered card, code or manifest hash → expected refused → refused → **pass**
- Planted keep, modify, stop, inconclusive, execution integrity, 10% boundary, inferior → expected card verdicts → 8/8 → **pass**
- T4.1 on all legacy rows → expected 0 valid test rows → 0 for rows 0–11 → **pass**
- C3 monitor on real data → expected the same failure steps → 260/45/53 → **pass**
- 1e-12 input perturbation → expected stable outputs → C1/C4/C5 stable, C3 max ρ shifts by 0.03 → **F3**
- Full-suite mutants → expected killed → 9 of 16 survive → **F2**

## Unchallenged Areas
- C2, C0 and C4DP were not re-implemented independently; they rely on the byte-identical rerun of C4DP fold 0 and on output hashes.
- The MLP's internal training was not re-implemented.
- The qualification (Q1–Q6) values in `qualification.json` were not recomputed.
- Topic 1 and other milestones are out of scope.
