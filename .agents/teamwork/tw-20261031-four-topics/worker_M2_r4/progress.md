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
