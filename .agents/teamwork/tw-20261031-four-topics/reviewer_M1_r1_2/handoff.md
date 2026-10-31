# reviewer_M1_r1_2 handoff (Hard) — M1 Topic 1 hardening + full-cohort step 5

Verdict: **APPROVE** (advisory; under sci-pipeline G9 the gate decision belongs to the PI / root).
Probes and receipts: `/home/juke/git/00IITP-AI/verification/reviewer_M1_r1_2/`. No production file was edited.

## 1. Observation

**C1, protected files.** `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0 with 67/67 OK (`protected_hash_check.log`). The card sha is `1e589f0b…75aa`. The src/topic1_lagmotif hashes (9) and scripts/topic1_timing.py match card §12: 10/10.

**C2, tests.**
- `pytest tests/topic1_lagmotif`: 88 passed (`pytest_topic1.log`).
- `STRICT_E2E=1 pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`: 86 passed, 7 warnings (`pytest_old_suite.log`).
- The 8 pre-existing tests/topic1_lagmotif files are byte-identical to `results/topic1/2026-10-30/test_hashes_r2.txt`. Only 2 files were added: `test_extract_contract.py` (9d7121e4…) and `test_cohort_stats.py` (891f83eb…).

**T1.1, mutation testing.** I reran the victory auditor's mutants from adapted copies in my folder: `mutants.py` and `mutants_extra.py`, diffs limited to BASE, the output path and a scripts copy.
- `mutants_rev.log`: control 89 passed, 19/19 mutants killed. `roi_subsample_80` fails 4 tests.
- `mutants_extra_rev.log`: control 89 passed, 4/4 killed. `curl_returns_F` and `seeds_ignore_position` are killed by the new contract tests, as are `sp_not_normalised` and `extract_subject_drops_valid_T`.
- The worker's v3 "without new tests" receipts show the 5 original survivors at rc 0. `SHA256SUMS.txt` verifies from the repo root.

**T1.2, statistics script.**
- I read the whole of `scripts/topic1_cohort_stats.py` (sha 33e27576…). The Freedman–Lane algebra is exact: t depends only on M_Z·P·e_r, with dfres = n − p_Z − 1.
  - Permutations stay within site, B = 9,999, seed 20261031, and p = (1 + #) / (B + 1).
  - The MixedLM is fit by ML with a site random intercept and Mundlak means of dx, age, sex and log duration.
  - d = β_LMM / √scale. Holm and BH are correct. survive = p_Holm < 0.05 AND |d| ≥ 0.15. The fallback comparison is strict (> 0.10).
- `stats_validation_final.json` binds script_sha256 33e27576… with all_pass true:
  - V1: vectorised t* matches a statsmodels refit to 2.2e-13.
  - V2 null FPR: 0.0545, 0.0525 and 0.0435, all inside the band [0.0354, 0.0646]. Welch has FPR 0.9995 in S1.
  - V2b (B = 9,999, R = 300): FPR 0.0767, inside the band [0.012, 0.088].
  - V3 planted d: 0.0005, 0.1426 and 0.3031, each within 3 MC-SE. The 0.15 case is about −2.5 SE.
  - V4 rules pass.
- `stats_script_sha256.txt` was recorded at 11:14:46Z, and `analyze.log` starts at 11:15:03Z with the same sha. `analyze` refuses to run on any other bytes (`_check_recorded_hashes`).

**T1.3, manifest.** 1,706 positions, a cohort-level salted digest only, and 0 manifest-vs-jsonl field mismatches. grid_len runs from 100 to 340 against a floor of 100. The report gives per-group, per-site and site × group acceptance and degeneracy. All 23 site rows in the report match `stats_results.json` exactly, and they sum to 1,706.

**T1.4, extraction.**
- `extract_primary.log`: start 08:16:15Z with params_sha256 86863ffa…; finished ok=1706 err=0, with jsonl sha 948961c8…, matching the file.
- Bit-for-bit re-extraction of 7 positions (`reextract_probe.json`) called `extract_subject` directly. The 7 cover both degenerate-at-0.05 subjects, the first TR 0.7 subject, the lowest-acceptance subject and 5 random ones. All are bit-identical, including the static-FC rows.
- Integrity of the full table (`independent_primary.json` → integrity), recomputed for all 1,706 × 6 units:
  - m, n_null, Z, SP, degenerate flags and log ratio: 0 bad.
  - E1/E2 definitions: 2 mismatches, both NaN == NaN at broadband@0.05, where the subjects are degenerate. They are not defects.

**T1.4, statistics.**
- Rerunning `analyze` on a copy gives `stats_results.json` identical to the saved one except elapsed_s.
- My **independent reimplementation** uses statsmodels formulas, patsy and my own permutation code; it does not import the script.

  | Endpoint | t | p_FL (card permutation rule) | p_FL (other generator, seed 777) | d_LMM | d_FE | Mundlak ratio | p_Holm | Survives |
  |---|---|---|---|---|---|---|---|---|
  | E1 | 2.2502 | 0.0223 | 0.0203 | 0.11313 | 0.11304 | 2e-14 | 0.0446 | no |
  | E2 | 0.7495 | 0.4416 | 0.4468 | 0.03769 | — | — | 0.4416 | no |

  - E1 d is 0.1130 under REML and 0.11313 with the Powell optimizer. **Topic 1 is killed.**
  - Family 2: n = 856; std β 0.0319 and 0.0288; p_FL 0.3073 and 0.3609.
  - Family 3: 180 vs 121 in 11 sites; p_FL 0.5682 and 0.155.
  - Log ratio: d 0.0897, p_FL 0.0665.
  - All of these match the report.

**Pre-label integrity (D1).**
- I scanned `verification/` recursively for scripts that join labels with features. Only `verification/worker_M1_r1/probe_analyze_smoke.py` (09:08Z) predates 11:15Z, and it fabricates its design and features.
- The only `stats_results*.json` from before 11:15Z is the synthetic smoke output.
- The extractor reads metadata through `NpyCohort.from_metadata`, which uses `usecols=["Unique_ID","Sample"]` (data.py:106).

**C4, participant IDs.** I matched against all 2,095 metadata Unique_IDs plus the on-disk names (min length 16) over 185 files: the M1 results, the topic1 docs, both scripts, the tests, `verification/worker_M1_r1`, my folder, and the worker and my metadata. **0 hits** (`id_scan.log`).

**C4, git.**
- The M1 artifacts contain no `git commit/add/push`. The only hits are the worker's disclosure of a foreign push.
- **Run-level finding:** `feature/topic1-lag-motif-v2` receives automatic commits titled "docs(iitp): checkpoint four-topics teamwork documents" every 15 min (…3a56070 17:01 → 14031f5 20:46 KST; author is the user identity). Each commit holds `.agents/teamwork/tw-20261031-four-topics/**` and dated docs, including the M1 prelabel addendum, deviations addendum and result report.
- `snuprivate/feature/topic1-lag-motif-v2` is at 3bdbc9c, so at least one of these commits was pushed.
- None is in the user's crontab. The source was not identified, and it is not attributable to M1.

**C7, external repos.** The enigma data dir has 0 files modified today. Today's changes under enigma `.git/objects`, `.git/worktrees` and `logs/coordinator.log` coincide with a `enigma_ocd_mbbn-palm` worktree [feat/palm-neuroprior]. That belongs to another project, and the M1 artifacts contain no enigma git commands.

**C5/C6.** M1 ran on CPU locally (extraction header and log); 0 GPU.

**Layout lint.** `audit_layout.py` on the run root: PASS, 82 files, 0 findings.

## 2. Logic Chain

1. All frozen inputs are byte-identical (C1, card §12), and every primary row carries the frozen params hash. 7 re-extracted subjects match bit-for-bit. Together these mean the feature table is the frozen pipeline's output, not edited.
2. The script sha was locked before the first label/feature join (timestamps, the hash guard in the code, and the recursive scan). The prelabel addendum was frozen at 11:13:52Z and recorded at 11:14:46Z. So the analysis rules were fixed before any result (C3, T1.2).
3. An independent reimplementation reproduces t, p_FL (exactly, under the card's permutation rule), d, Holm and survival. So the verdict does not depend on the reviewed code alone.
4. E1 fails on |d| = 0.113 < 0.15 whatever the estimator (ML, REML, Powell, FE). E2 fails on both conditions. So the kill holds even if the permutation p were mildly miscalibrated (V2b +2 SE) or another permutation stream were used.
5. The fallback (0/1,706 degenerate at 0.10), the exclusions (0) and the §9 limitation are reported beside the verdict, as T1.4 and T1.5 require. The deviations are in a dated addendum (C3).
6. T1.1 has 0 survivors on my own rerun, and the old tests are unchanged, so the hardening is additive.

## 3. Caveats

- **Card §12 independent review "before execution" was not met.** The Trinity review was incomplete; this is disclosed as deviation 1 / D4 per C3.
  - This review is the native independent audit of the frozen bytes 33e27576 that the worker said was still owed. I reimplemented the primary model, families 2 and 3, the log ratio and the degeneracy counts.
  - I read family 1 (LOGO classification, site bootstrap, static FC) and the descriptives, but did not reimplement them. I checked their reported values against `stats_results.json`, and the exact rerun reproduced them.
  - Non-blocking: the script was sha-locked before labels, I found no defect, so no change after the result and no forking path exists.
- V2b FPR 0.077 (R = 300) is inside the pre-registered band but about +2 SE. The planted d = 0.15 recovery is about −2.5 SE. Both pass the pre-set criteria. Neither affects the verdict, because E1 fails on d.
- I did not rerun `validate`, the stats mutants (24/24) or the T1.1 "without" arm. I read their receipts.
- The checkpoint-commit source is unattributed, and I avoided `git show --stat/--name-only` per the ID rule (directory-aggregated counts only).
- **Wording (sci-pipeline G8).** "KILLED" is the card's own term. Under the G8 taxonomy this is "stop", with failure type "effect below the pre-registered bar". The CI for d, [0.015, 0.212], contains 0.15, so it is also precision-limited. The report already says "not evidence that the effect is absent". Mapping it explicitly to G8 is optional.

## 4. Conclusion

**APPROVE M1.** T1.1–T1.5 and C1–C8 are met with evidence. The verdict "Topic 1 KILLED (E1 d = 0.113 < 0.15; E2 d = 0.038, p_Holm = 0.44)" is reproduced independently.

Two run-level issues go to root. They do not block M1:
- (a) the 15-minute checkpoint commit and push loop on the working branch (C4 at run level);
- (b) foreign git activity in the enigma repo `.git` from the palm worktree (C7, not M1).

## 5. Verification Method

- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q` → 88 passed
- `verification/reviewer_M1_r1_2/run_mutants.sh` → `mutants_rev.log`, `mutants_extra_rev.log`
- `python3 verification/reviewer_M1_r1_2/independent_primary.py` → `independent_primary.json`
- `python3 verification/reviewer_M1_r1_2/reextract_probe.py` → `reextract_probe.json` (all_bit_identical true)
- `python3 verification/reviewer_M1_r1_2/id_scan.py` → 0 files with hits

Invalidation: any change to `scripts/topic1_cohort_stats.py`, `extract_primary.jsonl`, `stats_results.json`, the card, the addenda or src/topic1_lagmotif after these hashes.
