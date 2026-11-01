# handoff — victory_M1_b (victory audit of M1, run tw-20261031-four-topics)

Type: Hard (task complete). Written 2026-11-01T00:58Z. Probes and logs: /home/juke/git/00IITP-AI/verification/victory_M1_b/

```
=== VICTORY AUDIT REPORT ===

VERDICT: VICTORY CONFIRMED  (milestone M1: Topic 1 hardening T1.1–T1.3 + full-cohort step 5 T1.4–T1.5)

PHASE A — TIMELINE:
  Result: PASS
  Anomalies: none attributable to the M1 team. Context leads (root / other sessions), listed under Caveats C-1..C-6.

PHASE B — INTEGRITY CHECK:
  Result: PASS
  Details: no hardcoded results, facades, fabricated outputs or self-certifying tests found; results reproduce from
  saved inputs; 8 subjects re-extract bit-identical; mutants killed; C1 rc 0 (x3); layout lint PASS; 0 ID hits.

PHASE C — INDEPENDENT TEST EXECUTION:
  Test command: cd /home/juke/git/00IITP-AI && STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI
                /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py
                tests/test_pilot_connectome.py tests/e2e -q        ; and  ... -m pytest -p no:cacheprovider tests/topic1_lagmotif -q
  Your results: 86 passed (rc 0); 88 passed (rc 0); mutants 19/19 + 4/4 killed (0 survivors), without the new tests the
                5 original survivors return; stats mutants 24/24 killed; analyze rerun identical except elapsed_s;
                validate rerun identical except timing fields; independent reimplementation: KILLED.
  Claimed results: 86 passed; topic1 suite pass (89 in mutant mirror = 88 + guard); 19/19 + 4/4; 24/24;
                KILLED with E1 d=0.113 p_Holm=0.0446, E2 d=0.038 p_Holm=0.4416.
  Match: YES
```

## 1. Observation

Governing inputs (sha256): ORIGINAL_REQUEST.md 1513540b…; ACCEPTANCE.md c316c8de…; PROTECTED_HASHES.txt 9b5ca8fb…;
card `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md` 1e589f0b…75aa (= expected).

O1 Hash chains. Card §12 code hashes 10/10 OK. Pre-label addendum freeze list 12/12 OK
(`verification/victory_M1_b/addendum_freeze_hashes.txt`). `results/topic1/2026-10-31/RESULTS_SHA256SUMS.txt` 18/18 OK.
`t1_1_mutation/v3_final_tree/SHA256SUMS.txt` 11/11 OK. prelabel addendum 7ccb983e…, fallback_decision.json be784654… OK.
Re-run at the end of the audit: C1 rc 0, card12 rc 0, results sums rc 0, freeze list rc 0; no file newer than my start in
victory_auditor_1, worker_M1_r1, results/topic1, docs/…/topic1, src/topic1_lagmotif, scripts, tests/topic1_lagmotif.

O2 C1. `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0 (67 OK) at 00:26Z, after the old suite (00:30Z) and final (00:57Z).

O3 Tests. Old suite: `86 passed, 7 warnings in 41.59s`, rc 0 (`old_suite.log`). tests/topic1_lagmotif: `88 passed in 5.91s`, rc 0.

O4 T1.1 mutants (adapted copies of verification/victory_auditor_1/mutants.py 0b7b655c… and mutants_extra.py 78fbcee4…;
only BASE/output paths changed, the cohort scripts copied unchanged into the mirror, mirror script copy chmod 644 because
production is 0444). With current tests: control 89 passed; all 19 mutants rc 1 (incl. roi_subsample_80: 4 failed);
extra: curl_returns_F, seeds_ignore_position, sp_not_normalised, extract_subject_drops_valid_T all rc 1 → 0 survivors.
Without test_extract_contract.py + test_cohort_stats.py: control 54 passed; roi_subsample_80 and the 4 extra survive (rc 0)
= the 5 original audit survivors. Logs `mutants_{with,without}.log`, `mutants_extra_{with,without}.log`.

O5 Stats mutants (adapted copy of verification/worker_M1_r1/stats_mutants_v3.py): control 31 passed; 24/24 killed
(`stats_mutants.log`).

O6 Label-free JSONL recount (`probe_jsonl_integrity.out.json`): 1,706 rows, positions 0–1705 unique, all ok, all params
86863ffa…; m = 2303/4606/6908 per density; degenerate (null SD 0) broadband@0.10: E1 0, E2 0; broadband@0.05: 2 (030C);
other units 0; flags agree with SD; Z, E1, E2, log-ratio recomputed from observed/null_mean/null_sd: 0 mismatches;
rank-2 identity holds; manifest vs JSONL per-position fields: 0 disagreements.

O7 Re-extraction (`probe_reextract.out.json`): positions 0, 311, 642, 977, 1104, 1288, 1578, 1705 (includes both 5 %-degenerate
positions and the lowest-acceptance one) with frozen PARAMS, no keyword overrides: all 6 units, all scalars and the
static-FC row bit-identical to the saved values; FC equals np.corrcoef to ≤1.1e-15.

O8 analyze rerun on a copy of the saved inputs (`rerun_analyze/`): guard passed (script 33e27576…); stats_results.json
deep-compare vs saved: 1 difference, `/elapsed_s` (77.8 vs 165.2).

O9 Independent reimplementation (`probe_independent_stats.py`, does not import the team script; own label join; statsmodels
formula OLS with C(site), C(sex); loop-refit Freedman–Lane, B = 9,999, own seed 424242; own MixedLM call, ML):
E1 β_FE 0.548815, t 2.2502, d_LMM 0.11313067751337895 (identical to saved), p_FL 0.0200 (saved 0.0223; MC SE ≈0.0014 each),
p_Holm 0.040; E2 d 0.03768877 (identical), p_FL 0.4505 (saved 0.4416), p_Holm 0.4505; log-ratio d 0.0897, p 0.071
(saved 0.0897, 0.0665); Mundlak ratio ~1e-14; REML d 0.11301 / 0.03765. → neither endpoint survives; Topic 1 KILLED.

O10 Validation receipt rerun (detached, PID 89133, exited): stats_validation_rerun.json vs stats_validation_final.json:
5 differences, all timing (`sec` ×3, `elapsed_s`, `started_utc`). Receipt values: FPR 0.0545 / 0.0525 / 0.0435
(band 0.0354–0.0646), B = 9,999 confirmation 0.0767 (R = 300; band 0.012–0.088), Welch defect 0.9995, planted d
0.0005 / 0.1426 / 0.3031 (3-SE pass), V4 rule checks pass.

O11 Saved verdict (`stats_results.json`): primary_unit broadband@0.10, fallback false; E1 p_fl 0.0223, p_holm 0.0446,
d 0.11313, survives false, reason "|d| < 0.15"; E2 p_fl 0.4416, p_holm 0.4416, d 0.03769, reason "p_Holm >= 0.05; |d| < 0.15";
topic1_killed true; LMM converged both, 0 warnings; card count checks 7/7 equal; exclusions 0 of every class.
stats_sensitivity.json: no surviving endpoint, §7 not run. Report tables vs JSON: 23/23 site rows, group, density,
cell and secondary numbers match (`report_vs_json.txt`).

O12 Timeline (UTC, 2026-10-31). Card committed e694dae 07:31:10Z. Manifest 08:15:20Z. Extraction 08:16:15Z–09:27:48Z
(host spark-3a4c, 14 workers, nice 10, runner ae69aee2…). Final stats bytes mtime 09:08:21Z. Final validation 10:58:47Z on
33e27576…. Commit 3bdbc9c 11:01:25Z holds the addendum with P1–P17/V1–V4 (pushed 11:12:39Z). Worker transcript
(agent-a73b451e…jsonl): stats_script_sha256.txt written 11:14:45Z; `decide` 11:14:52Z; `analyze` launched 11:15:02Z;
analyze.log single start line 11:15:03Z, end 11:16:21Z; 7497e6a (11:16:25Z) commits the frozen addendum 7ccb983e.
All 70 transcript files of wf_59fa8ec4-d01 plus the root transcript, 08:16:15Z–11:15:03Z, every tool type: no call joined
real features with labels before 11:14:45Z; the one pre-freeze inline read of extract_primary.jsonl (10:58:23Z) counted
positions/ok/params hashes/unit keys only; label reads were design-only (synthetic outcomes) or labels-only count probes.

O13 C4/C5/C6/C7. ID scan (2,095 metadata IDs + 1,706 names + 1,998 subject suffixes + `sub-` tokens): 0 hits in 449 M1
files (results, docs, scripts, tests, worker/reviewer/challenger/auditor/explorer M1 dirs); 0 full/suffix hits in 377
run-window committed blobs (sub- token hits are words/placeholders/synthetic fixture). No git write by any M1 agent
(transcript scan). No GPU ledger; no B300/ssh/CUDA references in M1 code or results; enigma data + metadata dirs: 0 files
newer than 2026-10-31 16:28. Layout lint: PASS, 128 files, 0 findings.

## 2. Logic Chain

L1 (O1, O2) Frozen card and code unchanged; protected files unchanged before, during and after the audit → C1 met, T1.4
"card sha unchanged" met.
L2 (O3) Both canonical suites pass on my execution → C2 met.
L3 (O4) The 5 mutants that survived the 2026-10-30 victory audit are killed by the current tests and survive without
them; all other mutants killed → T1.1 met; the new tests are the cause.
L4 (O5, O8, O9, O10) The stats script implements card §4–§6 (independent code gives identical d and p within MC error);
validation on the real design with synthetic outcomes reproduces deterministically and meets the FPR/planted criteria;
24 targeted defects are caught → T1.2 implementation and validation met.
L5 (O12) Hash 33e27576… written 11:14:45Z, decide 11:14:52Z, analyze 11:15:02Z; no earlier feature×label join in any
transcript; analyze refuses unless the recorded hash matches → "script sha256 recorded BEFORE first real-label analysis"
met. The git anchor for the hash block is later (7497e6a, 11:16:25Z); the git anchor for the rules is earlier (3bdbc9c,
committed 11:01:25Z, pushed 11:12:39Z).
L6 (O6, O7, O11) Manifest pinned (positions + one salted digest), 100-sample floor, 0 below floor, per-group/site
acceptance and degeneracy reported → T1.3 met. Saved features are what the frozen code produces (8/8 bit-identical)
→ T1.4 extraction genuine.
L7 (O6, O11) Degeneracy 0 % at broadband@0.10 → fallback (card §3, ">10 %") correctly not triggered; no second primary
density owed → T1.5 fallback branch not applicable; deviations recorded in a dated addendum → T1.5 met.
L8 (O9, O11) E1 fails |d| ≥ 0.15 (0.113); E2 fails both (0.038, 0.44); |d| is computed deterministically and is binding, so
permutation MC error cannot change the verdict → "KILLED by card §5" follows the card's rules exactly.
L9 (O13) No IDs, no M1 git writes, CPU-only local run, no ENIGMA data off-machine → C4–C7 met for M1; C8 met (L4/O11).

## 3. Caveats

C-1 Card §12 says the cohort script "is subject to independent review before execution". This requirement was NOT met
before execution: the only pre-execution review was an incomplete Trinity run (deviations addendum item 1). Native
independent reviews (r1 verifiers 20:35–21:13 KST, and this audit) are post-execution. I classify it as a disclosed,
unmet requirement, not a blocker: ACCEPTANCE C3/T1.5 handle deviations by a dated addendum (done), the script was
hash-frozen before analysis so it could not be edited after results, and this audit's independent reimplementation
found no defect. The PI should decide whether this is acceptable.
C-2 Push: root session Bash 10:51:26Z `git push -u snuprivate feature/topic1-lag-motif-v2` (PID 732435), reflog
"update by push" 2026-10-31 20:12:39 KST at 3bdbc9c. Not in the dispatch's git-history note. Not an M1 action.
C-3 Root checkpoint loop (session 1157b38c `scratchpad/autocommit/autocommit.sh`, PID 3270989, no STOP file) is still
running: commit a18006d (2026-11-01 09:31:26 KST) added this auditor's DISPATCH/BRIEFING/progress and worker_M2_r2b
metadata. It will commit this handoff too. RESUME note's "16:31–21:31" window is incomplete.
C-4 d654ec8 (2026-10-31 23:04:11 KST) commits a protected `docs/qa_prep_*` file; author not in the run transcripts; the blob
equals the protected hash 2c17ffac… recorded at 16:28, so content predates the run (C1 holds).
C-5 Stray read-only process PID 3787900 `tail -n +1 -f verification/explorer_M1_r1_3/probe_stats_fpr.log` (~17 h). Not mine;
not killed.
C-6 src/topic1_lagmotif/__pycache__ dated 2026-11-01 08:29 KST (pre-audit; not in the hashed set).
C-7 Not done by design: full-cohort re-extraction (forbidden); 8/1,706 positions verified. Family-1 AUROC reproduced only by
rerunning the frozen script, not reimplemented. Transcript scan covers workflow wf_59fa8ec4-d01 and the root transcript only.
C-8 Validation detail: planted d = 0.15 recovered at 0.1426 (2.55 MC-SE low, inside the 3-SE criterion); B = 9,999 FPR 0.077 at
R = 300 (inside band, ~2 SE above 0.05); the across-site permutation defect is not FPR-detectable (disclosed D3; checked
structurally).
C-9 ACCEPTANCE T1.5 says "card §2 degeneracy fallback"; the rule is in card §3.
C-10 Auditor disclosure: while attributing the push I read a ~600-character excerpt of the worker's journaled return
(orchestrator/journal_wf_59fa8ec4-d01.jsonl line 65); it matched the worker BRIEFING's PID note. No team handoff.md was read.

## 4. Conclusion

M1 is complete as claimed. T1.1–T1.5 and C1–C8 are met on independent execution, and the headline reproduces:
Topic 1 is KILLED by card §5 at broadband@0.10 (E1 Z030C d = 0.113, p_Holm = 0.0446, fails |d| ≥ 0.15; E2 d = 0.038,
p_Holm = 0.44). The kill is a decision under the pre-registered rule, not evidence of no effect (E1 Wald 95 % CI for d
[0.015, 0.212] contains 0.15). One card requirement (§12 pre-execution independent review) was met only after execution
and is disclosed; the PI should accept or reject that deviation explicitly.

## 5. Verification Method

- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- `LC_ALL=C sha256sum -c verification/victory_M1_b/card_s12_hashes.txt verification/victory_M1_b/addendum_freeze_hashes.txt`;
  `(cd results/topic1/2026-10-31 && sha256sum -c RESULTS_SHA256SUMS.txt)`
- The two pytest commands in Phase C.
- `cd verification/victory_M1_b && VM1B_TAG=with python3 -B mutants_adapted.py` (and `VM1B_TAG=without
  VM1B_DROP=test_extract_contract.py,test_cohort_stats.py`), same for `mutants_extra_adapted.py`; `python3 -B stats_mutants_adapted.py`.
- `python3 -I verification/victory_M1_b/probe_independent_stats.py 9999 <seed>` — any seed should give |d_E1| 0.1131, KILLED.
- `python3 -B verification/victory_M1_b/probe_reextract.py` — all_identical true.
- `python3 scripts/topic1_cohort_stats.py analyze --outdir verification/victory_M1_b/rerun_analyze` then
  `python3 verification/victory_M1_b/compare_json.py results/topic1/2026-10-31/stats_results.json verification/victory_M1_b/rerun_analyze/stats_results.json` — only elapsed_s differs.
- Invalidation: any change to the card, src/topic1_lagmotif, scripts/topic1_cohort_stats.py (33e27576…), extract_primary.jsonl
  (948961c8…), or a discovered feature×label join before 2026-10-31T11:14:45Z.

## 6. Post-verdict comparison with the team's claims (Phase C step 7)

worker_M1_r1/progress.md and handoff.md were read after the verdict was fixed (00:59Z): no conflicting claim. Freeze 11:14:46Z,
decide 11:14:54Z, analyze 11:15:03Z, T1.1 v3 (89 / 19+4 / 0 survivors; without: 5), stats v3 (31 / 24/24), 88 tests, and the
KILLED numbers all equal this audit's results. The worker's open item ("whether another process committed these paths was not
checked") is closed here: M1 docs were committed only by the root checkpoint loop (.md/.txt), scripts/src/tests only by root
commit 0db0336 (2026-11-01 08:32 KST), results/topic1/2026-10-31 never committed; committed run-window blobs have 0 ID hits.
The worker's request for "a fresh native auditor" of scripts/topic1_cohort_stats.py is satisfied post-execution by this audit;
it cannot retroactively satisfy card §12's "before execution".

Root checkpoint loop stop path (for the human; not touched by this auditor):
/tmp/claude-1000/-home-juke/1157b38c-6f5e-4f5a-acc0-a813c00b17be/scratchpad/autocommit/STOP
Final layout lint (after handoff written): PASS, 129 files, 0 findings (verification/victory_M1_b/layout_lint_final.log).
