# handoff — reviewer_M1_r1_1 (Hard handoff) — 2026-10-31T11:55Z

**Verdict: APPROVE** (M1, T1.1–T1.5, C1–C8). No blocking issue. Nonblocking issues are listed in §4.
This review also serves as the post-hoc independent audit that card §12 required before execution and that the worker could not obtain (deviation item 1).

## 1. Observation

All commands were run by me; probes are in `/home/juke/git/00IITP-AI/verification/reviewer_M1_r1_1/`.

- **C1:** `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives rc 0 (67 lines, 0 not OK). It was rerun at the end with rc 0 again. Card sha256 is `1e589f0b…75aa`. Card §12 code hashes: 10/10 OK. `results/topic1/2026-10-31/RESULTS_SHA256SUMS.txt`: 18/18 OK.
- **C2:**
  - `pytest tests/topic1_lagmotif`: 88 passed.
  - Old suite (`STRICT_E2E=1 … tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed, 7 warnings.
  - The 8 pre-existing topic1 test files are byte-identical to `results/topic1/2026-10-30/test_hashes_r2.txt`, so the change is additive only.
- **T1.1:** I reran the victory auditor's `mutants.py` and `mutants_extra.py` as copies. I changed only the output paths, the mirror copy of the two cohort scripts, and an `EXCLUDE_NEW` toggle; the diff was printed and checked.
  - With the new tests: control 89 passed; 19/19 + 4/4 killed.
  - roi_subsample_80 is killed by `test_all_304_rois_reach_the_graph` and 3 others.
  - Without the new tests: survivors are roi_subsample_80 and all 4 extra mutants, which reproduces the auditor's original result.
- **T1.2, independent recomputation** (`probe_stats_independent.py`). It uses its own metadata join, statsmodels formula FE-OLS and MixedLM with Mundlak means, and a Freedman–Lane test that refits the full model explicitly per permutation.
  - E1/E2 β_FE, t and d_LMM match stats_results.json to ≤ 9e-14.
  - p_FL with the same seed is identical: 0.0223 and 0.4416.
  - p_FL with another seed (777): 0.0209 and 0.4508.
  - Holm 0.0446 and 0.4416. Verdict: KILLED.
  - Families 2 and 3: p_FL, std β, β and n (301; 180 vs 121) are identical.
  - Card counts 869/837/23/856/203/212 are reproduced.
  - On all 1706 rows: E1 = Z030C, E2 = Z030C − Z030T, and site and duration agree between jsonl, manifest and metadata. The rank-2 identity holds to a relative error of 8e-14.
- **T1.2, validation receipt** (`stats_validation_final.json`): binds the script sha `33e27576…`, `started_utc` 10:58:47Z (before the 11:14:46Z freeze), all_pass true.
- **T1.2, my larger null probe** (`probe_null_fpr.py`, production FreedmanLane on the real design):
  - S1 aligned at B = 9,999, R = 1,200: FPR 0.0558 (z = 0.93).
  - New scenario S5 (aligned, heteroscedastic, skewed noise, duration effect) at B = 999, R = 2,000: FPR 0.044 (z = −1.23).
  - Planted d = 0.15 with R = 600 MixedLM fits: 0.1464 (z = −1.77).
  - High-R check (`probe_planted_fe.py`, R = 20,000): d_FE is 0.1498 at 0.15 (z = −0.57) and 0.3000 at 0.30. d_LMM/d_FE averages 1.001.
  - So the worker's 0.077 at R = 300 and 0.1426 are MC noise.
- **Code read**, `scripts/topic1_cohort_stats.py` (33e27576…, read in full):
  - Freedman–Lane algebra: M_Z ŷ_r = 0, so the residual permutation is exact.
  - Within-site permutations; p = (1+#)/(B+1).
  - Mundlak means of dx, age, sex2 and logdur; the 0.01·SE stop rule.
  - d = β_LMM/√scale.
  - Holm and BH; the survival rule `p_holm < 0.05 and |d| >= 0.15`; the strict `>` 0.10 fallback.
  - Everything matches card §3–§6 and pre-label addendum P1–P17.
- **T1.3:**
  - The manifest has 1706 rows: site, TR, raw_valid_T, n_trim, valid_T, duration_s, grid_len and contract status. There is one salted cohort digest and no per-position hashes.
  - grid_len ranges 100–340 (median 160); 0 are below the floor.
  - The report gives a 23-site table plus by-group acceptance and degeneracy. All 23 site rows match `descriptives_primary_unit.by_site` exactly (mechanical check).
- **T1.4, extraction:**
  - 10 positions (0, 27, 78, 171, 273, 437, 477, 740, 1336, 1705) were re-extracted through the production `_work` path. JSON rows are identical except elapsed_s, and the static-FC rows are bit-identical (`probe_reextract.out.json`).
  - The extraction log reports 1706 ok, 0 errors, jsonl `948961c8…`.
  - Every primary row carries params_sha256 `86863ffa…`. The production analyze checks this.
- **T1.4, analyze:** the production `analyze` was rerun on a copy of the results. stats_results.json is identical except elapsed_s, including the family-1 AUROCs (0.5157 [0.468, 0.560] and 0.5630 [0.524, 0.600]). The copy was deleted afterwards.
- **T1.4/T1.5, order:**
  - `stats_script_sha256.txt` was recorded at 11:14:46Z, `fallback_decision.json` at 11:14:54Z (labels_read false), and analyze started at 11:15:03Z. It is the only analyze run in the log.
  - **Git anchor:** the checkpoint commit `3bdbc9c` (11:01:25Z) already contains the full pre-label addendum. The diff to the frozen `7ccb983e…` covers only the status line and the hash block.
  - The worker's analyze-smoke probe replaced `load_design` with a synthetic design.
  - The labels-only probe read no features.
- **T1.5:** the deviations addendum lists 7 items and says the fallback was not triggered (0/1706 degenerate at broadband@0.10; 2/1706 at 0.05).
- **C4:**
  - My ID scan (`probe_id_scan_rv.py`) covered all metadata Unique_IDs and on-disk names, matched with word boundaries and as substrings, over 156 M1 files. **0 true-ID hits.**
  - 6 files matched 3 strings. These were classified by `probe_id_scan_classify.py` as stem-only artefacts: prefixes of dotted site names created by my `splitext`, not IDs.
  - M1 made no commits.
- **C6:**
  - The Trinity bundle `verification/worker_M1_r1/review_bundle_stats.md` was checked line by line. It contains only card text and an earlier version of the script; 9 leftover lines are headers or old code. No participant data was sent to external providers.
  - The derived static FC is in `results/…/derived/` with a `.gitignore`.
  - No scp, rsync or ssh appears in the worker's scripts.
- **Layout lint** (`audit_layout.py` on the run root): PASS, 81 files, 0 findings.

## 2. Logic Chain

1. The protected hashes and card §12 hashes hold (C1). Both suites pass and the old tests are unchanged (C2). `src/topic1_lagmotif/` is unchanged.
2. T1.1 is met: rerunning the auditor's original mutants myself gives 0 survivors with the new tests, and the 5 survivors without them. The kills come from genuine oracle tests, not collection errors, because the control passes.
3. T1.2 is met:
   - The script implements card §4–§6 (code read).
   - An independent implementation reproduces every primary and secondary number exactly.
   - The null FPR is within MC error at the production B (my R = 1,200 run, and a new harder scenario).
   - The planted effect is unbiased (R = 20,000).
   - The script sha was recorded before the first label read.
4. T1.3 is met (manifest, floor, and per-group/site rates checked against the JSON).
5. T1.4 is met:
   - The extraction is reproducible bit for bit on 10 subjects.
   - Statistics reproduce from the saved table.
   - The verdict follows card §5 exactly: E1 d 0.113 < 0.15 with p_Holm 0.0446; E2 d 0.038 with p_Holm 0.44. So Topic 1 is KILLED.
   - The §9 limitation and degeneracy rates are stated beside the verdict.
6. T1.5 is met: the fallback was not triggered and the deviations are recorded in a dated addendum.
7. The card §12 pre-execution review was not met and cannot be met retroactively. It does not block, for this reason: my card-faithful reimplementation reproduces the verdict exactly. It uses its own join, statsmodels formulas, an explicit-refit Freedman–Lane and a second seed. So the verdict does not rest on unreviewed code. The freeze chain is mostly self-attested (the script is untracked; its hash block was first committed at 11:16:25Z). The git anchor covers only the addendum's rules, at 11:01Z.

## 3. Caveats

- **DISPATCH.md abbreviates the worker's structured-handoff JSON.** Everything else is verbatim. The full JSON was in the dispatch turn, and its claims are covered in §1.
- **Not rerun:**
  - the stats-script mutants (24/24 is the worker's receipt);
  - the full validate subcommand (I ran a larger targeted null and planted-effect probe instead).
- **Not reimplemented:** family 1 classification. It was reproduced only by rerunning the production code.
- **Extraction coverage:** only 10 of 1706 subjects were re-extracted (the dispatch limit). The other rows rely on that sample, the log, the params hash and the sha chain.
- **Static-FC comparator:** it has no StandardScaler before PCA. The card names standardisation for the lag-motif model only, so the comparator matches the card literally. It is descriptive.
- **Timestamps:** the freeze rests on file contents, logs and mtimes, apart from the git anchor for the addendum.

## 4. Conclusion

**APPROVE.**

Nonblocking items for root:
- (a) Card §12 pre-execution review was not met. This review is the post-hoc independent audit, and it confirms the implementation.
- (b) `results/gpu_ledger_2026-10-31.md` does not exist. M1 used 0 GPU-h, so it needs no entry, but the file C5 names is absent.
- (c) A user-authored 15-minute checkpoint job (`docs(iitp): checkpoint four-topics teamwork documents`) is committing the M1 dated docs on `feature/topic1-lag-motif-v2`, and a push to snuprivate was observed. These are not M1 commits, and the committed docs contain no IDs.
- (d) The E1 nominal signal (approximate CI [0.015, 0.212]) is a kill under the rule, not evidence of no effect. The report says so correctly.

## 5. Verification Method

From `/home/juke/git/00IITP-AI`:
```
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q        # 88 passed
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/reviewer_M1_r1_1/probe_stats_independent.py           # exact match to stats_results.json
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/reviewer_M1_r1_1/probe_reextract.py                   # ALL_IDENTICAL True (~2 min)
bash verification/reviewer_M1_r1_1/run_mutants_rv.sh                                                                                   # mutants: 0 survivors with new tests
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/reviewer_M1_r1_1/probe_null_fpr.py                    # ~3 min
```

**Invalidation:** any change after 11:14:46Z to any of the following:
- `scripts/topic1_cohort_stats.py` (sha 33e27576…);
- the pre-label addendum (7ccb983e…);
- `extract_primary.jsonl` (948961c8…);
- `manifest.json` (063513c9…);
- `stats_results.json` (1713e370…).
