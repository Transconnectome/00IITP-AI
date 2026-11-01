# progress — worker_M2_r4

Last visited: 2026-11-01T07:46Z

- 07:34Z DISPATCH.md written (verbatim task text).
- 07:35–07:45Z Read role/runtime/claude-code adapters, ORIGINAL_REQUEST, ACCEPTANCE, RESUME, PI_DECISIONS (decision 6), GATE_STATUS, M2_r3_gate_record.json, the four r3 verifier handoffs, sci-pipeline SKILL, card, src/topic3_spectral, scripts/topic3_*, existing r3 tests, verifier harness sources.
- 07:45Z pycache baseline recorded (verification/worker_M2_r4/logs/pyc_*_start.txt). BRIEFING written.
- Next: probes for fixture seeds/preconditions, then write the two r4 test files.
- 07:50Z probe seed_search_n01 (verification/worker_M2_r4/probes/seed_search_n01.out.json): s=2000, t=2.15 gives Holm p = raw p in [0.025,0.05) for H1a (0.038) and H1b (0.0347).
- 07:55Z dev_tree_1 built (bin/make_tree.sh; manifest 121 files OK vs production). Wrote r4 test drafts in dev_tree_1 only.
- 07:57Z first dev run: 16 passed / 1 failed — the failure was MY fixture precondition (no-floor vs floor L3 corrPR differed by 4.4e-4 < my 1e-3 margin), before any shipped-code comparison. Fixed the fixture (near-dead L3 channel now carries its own signal: effect ~3.2%); no tolerance on shipped-vs-direct comparisons changed. Rerun: 17/17 pass. Margins in probes/margins_r4.out.json.
- 08:01Z named_specs.py (AST extraction from the 4 r3 harnesses; 26 REQUIRED + 16 EXTRA ids -> 32 jobs) and run_jobs.py written. SMOKE run (r4 files only, dev tree, not evidence) started.
Last visited: 2026-11-01T08:02Z
- 08:09Z SMOKE (r4 files only, dev tree; not evidence): 26/26 REQUIRED ids KILLED; 8 EXTRA nonblocking survivors (N06, N12, VB02, FA13, FA14, GD01-03).
- 08:12Z lint (flake8 --max-line-length 120, ruff): clean after line wraps (formatting only).
- 08:13:57Z FROZE r4 test bytes into production: test_regression_r4.py ecceb134..., test_token_level_r4.py ab99b2b1... (logs/r4_tests_sha256_frozen.txt).
- 08:15Z production tests/topic3_spectral: first attempt INVALID (Bash tool 120 s timeout, rc 143 at 52%, no failures; final/pre_topic3_INVALID_README.txt); rerun pre_topic3_b: 138 passed, 0 skipped, rc 0; no new .pyc.
- 08:19Z tree_base_r4 built (123 files, manifest OK vs production); union list == FULL_v2 (151 ids, identical triples, same source sha). Evidence batch launched (bin/run_evidence.sh): named set then union, full 138-test suite, 2 jobs.
Last visited: 2026-11-01T08:20Z
Last visited: 2026-11-01T08:27:53Z (evidence batch running: named set)
Last visited: 2026-11-01T08:38:30Z (named set running; earlyoom INVALIDs to rerun later)
- 08:27–08:38Z earlyoom (host memory ~9-10% available, other workloads: agy 19.6 GB etc.) SIGTERMed 5 named jobs (rc -15) -> INVALID, never counted as kills. journalctl -u earlyoom shows the SIGTERMs.
- 08:42Z wrote bin/retry_invalid.py + bin/run_retries_after_batch.sh (waits for "union rc=" then reruns INVALID jobs per set, up to 4 rounds, new log names per round); launched in background.
Last visited: 2026-11-01T08:43Z
- 08:42–08:46Z earlyoom SIGTERMed nearly every job (17 named INVALID). Found 15 orphaned hung topic3_token_job.py Pool processes (test_token_job_driver) from SIGTERMed pytest parents in my work dirs; terminated by PID (logs/orphans_killed_0848.txt). Stopped my v1 batch + retry waiter (runs/EVID_named_r4_v1_STOPPED_README.txt). v1 partial keeps CONTROL_OK + 14 valid KILLED named jobs.
- 08:55Z runner v2 (bin/run_jobs_v2.py): memory gate (MemAvailable >= 18 GiB), own session + process-group cleanup, INVALID auto-retry (<=4, per-attempt logs). Launched run_evidence_v2.sh: 18 pending named jobs, then the 151 union.
Last visited: 2026-11-01T08:56Z
- 08:49–09:05Z v2 (gate 18 GiB): gate held ~12 min, CONTROL passed (138) at 09:02:46Z, then N003 waited at the gate; stopped (runs/EVID_named_r4_v2_STOPPED_README.txt, incl. a correction of its first wording). No job process or work copy left.
- 09:06Z launched v2b (gate 15.5 GiB, same runner v2, new log names): 18 pending named, then 151 union.
- Pre-checks (non-pytest): C1 67 OK; receipts output 42 / ad02 1 / ad03 3 / ad04 2 / ad05 3 OK; code_sha256_at_freeze: only topic3_launch_connectome.py differs (pre-existing, addendum 01 item 2).
Last visited: 2026-11-01T09:07Z
Last visited: 2026-11-01T09:29:08Z (v2b named running)
- 09:27Z gated rate measured at ~2.4 min/job (memory hovering 13.5-15.5 GiB) -> full-mode union would take ~6 h. Union switched to runner v3 fail-fast (-x; SURVIVED still needs all 138 tests; skipped must be 0); v2b union step cancelled by pre-creating runs/EVID_union_r4_v2b_logs/README_CANCEL.txt. bin/run_evidence_v3.sh waits for v2b, then runs the union (EVID_union_r4_v3ff).
Last visited: 2026-11-01T09:33Z
Last visited: 2026-11-01T09:54:12Z (named v2b finishing)
- 09:57Z all 26 REQUIRED named ids have valid KILLED records (v1 partial + v2b partial). Stopped v2b (only EXTRA N029-N032 left) and the waiting v3 driver; no leftovers (runs/EVID_named_r4_v2b_STOPPED_README.txt).
- 09:59Z launched bin/run_evidence_v3b.sh: named EXTRA N029-N032 full mode, then the 151 union with runner v3 --failfast and the 16 test files in fast-first order (estimated union test time ~19 min vs ~2.3 h alphabetical; survivors still run all 138).
Last visited: 2026-11-01T10:00Z
Last visited: 2026-11-01T10:32:16Z (union v3ff running)
- 10:14Z named v3 (N029-N032, full mode): all 4 SURVIVED (138 passed); controls OK. Named set complete: 32/32 valid; 24 KILLED (all r4-only, 0 pre-existing failures; covers all 26 REQUIRED ids), 8 SURVIVED (all EXTRA).
- 10:14-10:37Z union v3ff (failfast, fast-first, gate 15.5): 29 valid records, then stopped (5-min gate stalls; runs/EVID_union_r4_v3ff_STOPPED_README.txt). 10:38Z launched v3c for the 122 pending (gate 14.0 GiB).
Last visited: 2026-11-01T10:40Z
Last visited: 2026-11-01T10:59:13Z (union v3c running)
Last visited: 2026-11-01T11:09:02Z (union v3c running)
Last visited: 2026-11-01T11:19:13Z (union v3c running)
- 11:24Z union v3c DONE: 121 KILLED + 1 SURVIVED (U127). Merged union 150 KILLED / 1 SURVIVED, no status diff vs FULL_v2 (runs/SUMMARY_r4.json).
- 11:27Z fc1 (pre-addendum): topic3 138, old 86, topic1 88, C1 67, receipts OK, pyc unchanged. Layout lint PASS. ID scan clean.
- 11:4xZ addendum 06 v1 + receipt written; fc2: topic3 2 FAILED (C4 guards: literal BIDS prefix in addendum §7). Preserved v1 bytes (verification/worker_M2_r4/superseded/), wrote v2 (46527e6a...), regenerated receipt (db88f543...), fc3 rerun started.
Last visited: 2026-11-01T11:50Z
- 11:24Z union v3c DONE: 121 KILLED + 1 SURVIVED (U127). Merged union 150 KILLED / 1 SURVIVED, no status diff vs FULL_v2 (runs/SUMMARY_r4.json).
- 11:27Z fc1 (pre-addendum): topic3 138, old 86, topic1 88, C1 67, receipts OK, pyc unchanged. Layout lint PASS. ID scan clean.
- 11:4xZ addendum 06 v1 + receipt written; fc2: topic3 2 FAILED (C4 guards: literal BIDS prefix in addendum §7). Preserved v1 bytes (verification/worker_M2_r4/superseded/), wrote v2 (46527e6a...), regenerated receipt (db88f543...), fc3 rerun started.
Last visited: 2026-11-01T11:50Z
Last visited: 2026-11-01T11:56:02Z (fc4 gated final checks)
