# handoff — worker_M1_r1 (Hard handoff, M1 complete) — 2026-10-31T11:30Z

## 1. Observation
- Resumed in a new context at 10:54Z. Found the primary extraction finished at 09:27Z: `results/topic1/2026-10-31/extract_primary.log` says "finished ok=1706 err=0 … jsonl_sha256=948961c8…". There were 1706 unique positions, all with params_sha256 86863ffa….
- `stats_validation.json` bound script f2589105…, but the script on disk was 33e27576… (edited 09:08Z after the Trinity review). Validation was rerun on the final bytes: `stats_validation_final.json`, all_pass true, sha 88aec0ac…. The numbers are identical to run 2 except the timings.
- T1.1 v3 receipts (`results/topic1/2026-10-31/t1_1_mutation/v3_final_tree/`):

| Run | Control | Mutants killed | Survivors |
|---|---|---|---|
| With the new tests | 89 passed | 19/19 + 4/4 | 0 |
| Without them | — | — | the 5 audit survivors (roi_subsample_80 + 4 extra) |
| Stats mutants v3 | 31 passed | 24/24 | 0 |

- The stats mutants include 4 new ones for P14–P16 and the gradient-row LMM.
- Added test `test_exclusions_are_counted_by_class_group_and_site` (tests/topic1_lagmotif goes from 87 to 88 passed).
- A label-only probe (`verification/worker_M1_r1/probe_card_counts_labels_only.out.json`) matched all 7 card counts. Medication is float64.
- Freeze at 11:14:46Z:
  - `stats_script_sha256.txt` (first token 33e27576…);
  - `prelabel_addendum_sha256.txt` (7ccb983e…);
  - the addendum and the stats script set read-only.
- `decide` at 11:14:54Z: 0/1706 degenerate for E1 and E2 at broadband@0.10, so no fallback and the primary density is 0.10 (`fallback_decision.json` be784654…).
- `analyze` at 11:15Z: "Topic 1 KILLED (neither endpoint survives)". `stats_results.json` 1713e370….

| Endpoint | d | p_FL | p_Holm | Fails on |
|---|---|---|---|---|
| E1 | 0.113 | 0.0223 | 0.0446 | \|d\| < 0.15 |
| E2 | 0.038 | 0.4416 | 0.4416 | p_Holm ≥ 0.05 and \|d\| < 0.15 |

  - Mundlak equality held to 1e-13·SE. The LMM converged with 0 warnings.
- `sensitivity`: "no endpoint survives … not run". No variant extraction was done.
- Final checks: tests/topic1_lagmotif 88 passed; old suite 86 passed; C1 rc 0; card §12 rc 0; auditor receipts OK; layout lint 0 findings; ID scan in strict and all modes 0 files with hits.

## 2. Logic Chain
1. The card requires the script hash to be recorded before the label join. The bytes on disk were not the validated bytes, so the work order was: re-validate, re-run the mutants, freeze, then join labels.
2. The fallback was decided from label-free outputs after the freeze, so the rates could not shape the addendum.
3. Card §5: survival needs p_Holm < 0.05 AND |d| ≥ 0.15. E1 fails on d and E2 on both, so Topic 1 is killed. §7 is not interpreted.

## 3. Caveats
- The independent review is incomplete: the Trinity log is truncated and codex failed. **A fresh native auditor must still review `scripts/topic1_cohort_stats.py` (33e27576…) and the result.** See deviations addendum item 1.
- The E1 approximate 95 % CI for d is [0.015, 0.212] (derived, descriptive), so the kill is not evidence of no effect. The §9 latency/global-signal confound cannot be ruled out: there are no motion data and the preprocessing is unknown.
- Acceptance includes no-ops. The acceptance-stratified refit is post-freeze and descriptive.
- I observed PID 732435 `git push -u snuprivate feature/topic1-lag-motif-v2` running from this repo at 10:54Z. It was not mine, I did not touch it, and it later exited. Results may therefore exist on a remote; the ID scan is clean.
- The first part of this assignment (08:10–09:10Z) was done in an earlier context. Its receipts are kept (v1/v2 mutation receipts, `stats_validation.json`).

## 4. Conclusion
M1 is done under card §5: **Topic 1 is KILLED at broadband@0.10** (E1 d 0.113, p_Holm 0.0446; E2 d 0.038, p_Holm 0.44).
- No fallback was triggered, and degeneracy was 0 %.
- Secondary analyses: none BH-significant. Lag-motif AUROC was 0.516 against 0.563 for static FC (descriptive).
- T1.1–T1.5 are met, except that the independent review is only partial.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- `cd results/topic1/2026-10-31 && sha256sum -c RESULTS_SHA256SUMS.txt`, and `sha256sum scripts/topic1_cohort_stats.py`, which should give 33e27576….
- Re-run the analysis: `cp -r` the results dir into a scratch outdir, then `python3 scripts/topic1_cohort_stats.py analyze --outdir <copy>`. It is deterministic (seed 20261031) and should reproduce stats_results.json except elapsed_s and paths.
- Tests: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q` (88), plus the old-86 command.
- Invalidation: any change to the stats script, the addendum, the manifest or the extraction JSONL after 11:14:46Z.
