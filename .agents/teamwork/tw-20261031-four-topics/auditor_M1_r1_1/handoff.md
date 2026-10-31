# handoff — auditor_M1_r1_1 (forensic integrity audit of M1, worker_M1_r1) — 2026-10-31T12:05Z

## Forensic Audit Report

**Work Product**: M1 Topic 1 hardening + full-cohort step 5 (tests/topic1_lagmotif, scripts/topic1_cohort_stats.py, scripts/topic1_run_cohort.py, results/topic1/2026-10-31/, docs/03_empirical_analysis/topic1/2026-10-31_*)
**Profile**: General Project. Integrity mode: none stated in ORIGINAL_REQUEST.md → Development Mode (inferred).
**Verdict**: CLEAN

### Phase Results
- Hardcoded output detection: PASS. Verdict, d and p are computed (independent own-code recomputation agrees). Only literals: card counts and frozen params hash, used as STOP guards and equal to card values.
- Facade detection: PASS. Freedman–Lane, MixedLM+Mundlak, Holm/BH, LOGO classification, fallback rule are real implementations; unit tests compare against statsmodels refits and brute-force enumeration.
- Tests that cannot fail: PASS. Mutants (own copies of victory_auditor_1 harness, mirrors only): with new tests 19/19 + 4/4 killed (control 89 passed); without the new tests the 5 audit survivors survive (control 54). 8 pre-existing topic1 test files byte-identical to 10-30 recorded hashes.
- Fabricated / non-reproducible logs: PASS. analyze rerun on a copy → stats_results.json identical except elapsed_s. 6 positional subjects (0, 57, 333, 932, 1228, 1650) re-extracted bit-identical incl. static-FC rows. Extraction JSONL: 1706 unique positions, unsorted (imap_unordered), per-subject elapsed sums to 16.63 CPU-h (claim 16.7), log timestamps monotone.
- Results before freeze: PASS. Only one real-label stats_results.json predates verifiers (11:16:21Z, after the 11:14:46Z freeze). Auto-checkpoint commit snapshots (independent timestamps) show no result text before freeze; frozen addendum 7ccb983e first committed 20:16:25 KST and unchanged; last pre-freeze draft → frozen diff is bookkeeping only. Worker smoke analysis is synthetic (corr with real E1 0.002, 0 exact matches; planted d 0.41).
- Silent fallbacks: PASS. Exclusions counted by class/group/site (all 0); NaN↔degeneracy agreement enforced; fallback decided label-free (0/1706 degenerate).
- Participant-ID leakage: PASS. Own scan, 2095 tokens (metadata Unique_ID + full listing names), 0 hits over 155 M1 files (335 MB) and 22 committed versions of tracked M1 docs/metadata.
- Protected/external writes: PASS. C1 rc 0; card §12 10/10; card sha unchanged; src/topic1_lagmotif unchanged; 16 worker-claimed hashes rc 0; RESULTS_SHA256SUMS rc 0.
- ENIGMA on B300 / GPU: PASS for M1. Extraction host spark-3a4c, 14 workers; no ssh/scp/B300/CUDA references in M1 artifacts.
- Commits: PASS for M1 (no attribution to worker). Commits are a 15-min automated checkpointer (docs/metadata only, from 16:31:10 KST); code/results/tests untracked.
- Build/tests: topic1 88 passed; old suite 86 passed (STRICT_E2E=1).

### Follow-up checks (12:05–12:15Z)
- Stats tests can fail: PASS. Own independent stats mutants (7: D_MIN 0.10, Holm→raw p, across-site perms, wrong d denominator, fallback ≥, BH non-monotone, signed d) are all killed by assertion failures; control 31 passed. Production script still a-w, sha 33e27576.
- Content-based pre-freeze search: PASS. Files with markers topic1_killed / p_holm / beta_lmm / "p_fl" and mtime 08:16Z–11:14:46Z were searched in the repo and /tmp/claude-1000 (same filesystem). The only hits are the code-only review bundle, the synthetic smoke outputs and M2 files. The label-only probe reads metadata only, never features.
- Anti-tuning: the stats script's mtime is 09:08:21Z, before the full feature table existed (extraction finished 09:27:48Z).
- Commit attribution: the first checkpoint commit (e694dae, 16:31:10 KST) predates the worker's dispatch (08:10Z = 17:10 KST), so the worker is not the committer. No checkpoint commit ever touched the user-protected files (0 commits). This is an unresolved run-level C4 item for root.
- Subject-fragment ID pass: one 7-letter common word that is also a fragment of one ID. It appears in the protected 10-30 card and an old test, so it is a word collision, not a leak. The full-token scan remains at 0.
- src/topic1_lagmotif holds exactly the 9 pinned modules.
- Small-R validate rerun (R=200, Rc=20, Rp=20): all_pass false, as expected at this R. This shows all_pass is computed, not hardwired. V1 and V4 pass.

## 1. Observation
Raw outputs are in /home/juke/git/00IITP-AI/verification/auditor_M1_r1_1/ (indep_primary.out, analyze_copy.stdout, reextract_strdiff.out, mutants_*.log, id_scan_v2.out, id_scan_classify.out, worker_claimed_hashes.txt).

## 2. Logic Chain
Same numbers from independent code → not hardcoded. Bit-identical rerun of extraction and analysis → logs not fabricated. Timestamps from three independent sources (file mtimes, analyze.log, git snapshots) agree on freeze → label join order → not results-before-freeze.

## 3. Caveats (non-blocking)
- Card §12 independent pre-execution review was only partial (Trinity codex failed). The worker disclosed it. This audit is a post-hoc review and finds the script faithful to card §4–§6.
- The validation's across-site-permutation defect fixture does not separate (FPR ≈ 0.05); all_pass does not use it, and it is reported honestly. The B = 9999 confirmation gives FPR 0.077 at R = 300, inside a wide 3-SE band.
- results/gpu_ledger_2026-10-31.md does not exist. M1 used no GPU, so this concerns the other milestones.
- The auto-checkpoint committer pushes docs to remote `snuprivate`; its source was not identified (not crontab/systemd timers). It is not M1's.
- Orphan `tail -f` process (PID 3787900, since 17:03 KST) on verification/explorer_M1_r1_3/probe_stats_fpr.log, left by an explorer, not the worker.
- Ad-hoc interactive label peeks that leave no files cannot be excluded by forensics. No evidence of any was found.

## 4. Conclusion
CLEAN. The KILLED verdict (E1 d 0.113, p_Holm 0.0446; E2 d 0.038, p_Holm 0.44) is reproduced independently.

## 5. Verification Method
See the commands in the structured return. Invalidation: any change to the stats script, the addendum, the manifest or the JSONL after 11:14:46Z.
