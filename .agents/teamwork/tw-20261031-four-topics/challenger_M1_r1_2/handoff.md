# challenger_M1_r1_2 — handoff (Hard), 2026-10-31T12:00Z

Verdict: **CONFIRMED.** "Topic 1 is KILLED by card §5 at broadband@0.10" holds. No defect was found in the computation chain. There are test-coverage gaps (nonblocking) and one process requirement that remains unmet (card §12 review before execution).

## 1. Observation

All probes are in /home/juke/git/00IITP-AI/verification/challenger_M1_r1_2/. Production files were only read, never edited.

**Re-extraction.** `reextract_probe.py` re-extracted 10 positions through the production path: 1579, 1124, 1229, 933, 1085, 2, 479, 990, 1705 and 800. They cover all 7 TRs, the minimum grid_len (100) and the maximum (340).
- Each JSONL row was identical to the saved row, ignoring elapsed_s.
- Each static-FC row was identical too (`reextract.log`, `reextract_<pos>.json`).

**Independent primary analysis.** `indep_primary.py` (output `indep_primary.json`) does not import the stats script. It uses statsmodels formula OLS, MixedLM with ML and Mundlak means, and my own within-site Freedman–Lane with seed 777 and B = 9999. It also recomputes Z from observed, null_mean and null_sd.

| Endpoint | β_FE | d_LMM | p_FL (seed 777) | p_Holm | Saved p_FL | Saved p_Holm |
|---|---|---|---|---|---|---|
| E1 | 0.5488 | 0.11313067751337895 (bit-equal to saved) | 0.0203 (MC SE 0.0014) | 0.0406 | 0.0223 | 0.0446 |
| E2 | — | 0.03768876757961704 (bit-equal) | 0.4468 | 0.4468 | 0.4416 | 0.4416 |

- The recomputed E1 and E2 equal the saved values (max |diff| = 0).
- The rank-2 identity |Z021D + Z030T| holds to ≤ 1.1e-13.
- Neither endpoint survives, so the result is killed.
- n = 1706 (869 OCD, 837 HC), 23 sites. The raw OCD − HC mean of E1 is +0.444, which confirms the sign.

**Reproducibility.** I ran the production `analyze` on a copy (`analyze_copy/`). Its stats_results.json is identical to the saved file except for elapsed_s.

**Secondary families.** `indep_secondary.py` (output `indep_secondary.json`) recomputed them with my own code:
- Y-BOCS: std β 0.0319 / 0.0288, p_FL 0.307 / 0.364.
- Medication: n = 301 in 11 sites, β −0.552 / −2.162, p_FL 0.570 / 0.154.
- LOGO AUROC for lag motif: 0.51568 (identical). Static FC with full-SVD PCA: 0.5624, against 0.5630 saved with randomized PCA.

All of these match the saved stats_results.json. None is BH-significant.

**Freedman–Lane null calibration on real outcomes** (real E1/E2, labels shuffled within site, B = 999):

| Endpoint | Run | FPR |
|---|---|---|
| E1 | R = 400 | 0.065 |
| E1 | seeds 11/12/13, R = 500 each | 0.054 / 0.052 / 0.040 |
| E1 | pooled, 99/1900 | 0.052 (MC SE 0.005) |
| E2 | R = 400 | 0.0525 |

FL is calibrated on the real feature distribution.

**Degeneracy, counted directly.** null_sd == 0 at broadband@0.10: 0 of 1706 for 030C and 0 of 1706 for 030T. The fallback correctly did not trigger.

**Validation receipts.** stats_validation.json (bytes f2589105) and stats_validation_final.json (bytes 33e27576) are identical after stripping sec, elapsed_s, started_utc and script_sha256.

**T1.1 rerun.** I copied the victory-audit mutants (definitions identical to victory_auditor_1/mutants.py) to `va/`.
- With the new tests: control 89 passed; 19/19 and 4/4 killed.
- Without them: the 5 audit survivors return (roi_subsample_80, curl_returns_F, seeds_ignore_position, sp_not_normalised, extract_subject_drops_valid_T).

**My own mutants** (`my_mutants.py`, output `my_mutation_results_all.json`):
- src: 15 of 15 killed, including seeds_ignore_channel, seeds_ignore_density, roi_drop_last (303 ROIs), z_ddof0, head_trim_floor and padtype_constant.
- Stats script: 21 of 28 killed.
- The 7 survivors: st_survive_strict_d, st_mundlak_tol_loose, st_dx_flipped, st_reml, st_boot_subjects, st_ybocs_swapped, st_med_all_sites.

**Test suites and integrity checks.**
- tests/topic1_lagmotif: 88 passed.
- Old suite (STRICT_E2E=1): 86 passed, 7 warnings.
- C1 PROTECTED_HASHES: rc 0. Card §12 hashes: 10/10. Card sha: 1e589f0b…75aa.
- RESULTS_SHA256SUMS: rc 0.
- The 2026-10-30 topic1 test files are unchanged; their hashes match the prior-run records.
- Layout lint on the run root: 84 files, 0 findings.
- ID scan (victory_auditor_1 probe, strict and all modes) over the M1 outputs and my files: 0 files with hits.

**Freeze timeline.**

| Time (Z) | Event | Source |
|---|---|---|
| 09:08:21 | Stats script mtime (file is read-only) | mtime |
| 10:56 | Worker progress line naming script prefix "33e27576…" as the final bytes | in git commit 3bdbc9c (11:01:25Z, before analyze) |
| 11:01:25 | Commit 3bdbc9c already contains the pre-label addendum's P1–P17, V and D | git |
| 11:13:52 | Addendum mtime | mtime |
| 11:14:46 | Hash receipts written | receipt files |
| 11:14:54 | decide | fallback_decision.json |
| 11:15:03 | Only "analyze start" line | analyze.log (append mode; exactly one start line) |
| 11:16:25 | Frozen addendum bytes 7ccb983e first anchored | git commit 7497e6a |

- The diff between 3bdbc9c and 7497e6a for the addendum is 17 insertions and 6 deletions. It touches only the status lines and the hash block.
- cmd_decide reads only the JSONL. The analyze smoke probe used fabricated inputs.

**Checkpoint commits (C4-relevant, not M1's doing).** Automated commits every 15 min, author = the user's git identity, at 17:46, 20:01, 20:16, 20:31 and 20:46 KST. They include the 2026-10-31 topic1 docs and the worker_M1_r1 metadata. results/, scripts/topic1_* and src/topic1_lagmotif are untracked.

## 2. Logic Chain

1. The verdict rule (card §5) needs p_Holm and |d|. d is deterministic and reproduced bit-for-bit by an independent fit. E1 |d| = 0.113 < 0.15, so E1 fails on d whatever the p-value.
2. E2 fails on both conditions, under independent p (0.447) and under saved p (0.442).
3. So neither endpoint survives and the result is killed. The same holds with d_FE (0.113 and 0.038).
4. The inputs to steps 1–3 are trustworthy:
   - the saved features reproduce bit-for-bit for 10 diverse subjects;
   - Z/E1/E2 are internally consistent;
   - the design join reproduces every card count;
   - the fallback input (0 degenerate) was counted directly.
5. The p-value machinery is sound:
   - it agrees with an independent implementation within MC error;
   - it is calibrated on the real outcomes;
   - the tests catch the across-site, Manly, one-sided and no-+1 mutants.
6. Freeze before results: the rules were in git before the label join, and only bookkeeping changed afterwards. The script bytes were named final in a pre-join commit. analyze ran once.
7. T1.1: confirmed by an independent rerun, plus 15 further src mutants, all killed.
8. T1.3 and T1.5:
   - the manifest is pinned (cohort digest; per-position site/TR/lengths; the 100-sample floor gives 0 below);
   - per-group and per-site acceptance and degeneracy are reported, and the report's numbers match stats_results.json;
   - the deviations addendum lists the 7 deviations and that the fallback was not triggered.

## 3. Caveats

**Freeze anchor.**
- The exact final addendum bytes are git-anchored only 82 s after analyze. Before analyze, the content is shown only up to hash-list edits.
- The stats-script bytes have no git anchor, only the 8-hex prefix in a pre-join commit. Other timestamps are self-attested (mtimes, receipts).

**Card §12 review before execution: not met** (disclosed as deviation 1). This review is post hoc: it confirms the computation but cannot satisfy "before execution".

**Test-coverage gaps in test_cohort_stats.py** (7 surviving stats mutants). None is a production defect:
- st_dx_flipped: the runtime P14 card_count_check would stop it, and my recompute confirms the coding.
- st_reml: the bytes say reml=False, and my ML refit gives the identical d.
- st_ybocs_swapped and st_med_all_sites: my recompute reproduces the production values.
- st_mundlak_tol_loose: observed ratio about 1e-13.
- st_boot_subjects: affects a descriptive CI only.
- st_survive_strict_d: affects only d of exactly 0.15.
- The worker's "24/24 killed" is true for its own mutant set, not full coverage.

**Wording.** The report and the deviations addendum say fallback_decision.json was written "before any label was read". In fact, real dx labels were read earlier by validate and by the count probe (disclosed in D2). It was written before any label was joined to a feature.

**Not covered here.**
- §9 confound (latency or global signal): not tested; it is a scientific limitation, not a defect.
- §7 rows: not run, as the rule requires.
- Trinity log: not re-examined.
- The 5 frozen A3 timing subjects: not re-extracted.
- The V2b Freedman–Lane FPR of 0.077 at B = 9999 (R = 300): not re-run at B = 9999. Pooled real-outcome calibration at B = 999 is 0.052.

## 4. Conclusion

M1 claims T1.1–T1.5 are **CONFIRMED** for correctness:
- Topic 1 is KILLED under card §5: E1 d = 0.113 (< 0.15), p_Holm ≈ 0.04; E2 d = 0.038, p_Holm ≈ 0.44.
- n = 1706, 23 sites, 0 degenerate, no fallback.

Recommendations (nonblocking):
- Add unit tests for: load_design dx coding, reml=False, the family-2 and family-3 regression direction and site restriction, the Mundlak stop tolerance, the site-level bootstrap, and the boundary at exactly d = 0.15.
- Fix the "before any label was read" wording in a new dated note.
- Record that card §12's pre-execution review was not met; this post-hoc audit stands in for it.
- Root should check whether the 15-min checkpoint committer is authorised under C4.

## 5. Verification Method

From /home/juke/git/00IITP-AI, using /home/juke/superclaude-env/bin/python3 with PYTHONDONTWRITEBYTECODE=1:
- `python3 verification/challenger_M1_r1_2/indep_primary.py 9999` → indep_primary.json. d is bit-equal to the saved value; p_FL within about 2 MC SE of saved.
- `bash verification/challenger_M1_r1_2/run_reextract.sh` → reextract.log: 10 rows, all identical.
- `TAG=x python3 -B verification/challenger_M1_r1_2/my_mutants.py` → my_mutation_results_x.json.
- `cd verification/challenger_M1_r1_2/va && TAG=with python3 -B mutants.py`, and `TAG=without EXCLUDE_NEW=1` for the run without the new tests.
- `python3 scripts/topic1_cohort_stats.py analyze --outdir <copy>`. The copy needs manifest, jsonl, fallback files, stats_script_sha256.txt and derived/. Compare to the saved file without elapsed_s.
- `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` → rc 0.

**Invalidated if** any of these hashes changes: stats script 33e27576…, extract_primary.jsonl 948961c8…, manifest 063513c9…, card 1e589f0b….
