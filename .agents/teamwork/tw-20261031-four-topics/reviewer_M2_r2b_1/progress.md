# progress — reviewer_M2_r2b_1

- 2026-11-01T01:22Z — DISPATCH.md and BRIEFING.md written; read role, runtime adapters, ORIGINAL_REQUEST, ACCEPTANCE, RESUME note, challenger_M2_r1_1 handoff, card, addenda 03 and 04. Next: baseline hash checks and test runs.

Last visited: 2026-11-01T01:22Z
- 2026-11-01T01:40Z — Baseline: C1 rc 0 (67 OK); output/add02/add03/add04 pins rc 0; card hash matches; code freeze 26 OK + launcher FAILED (pre-disclosed). Suites on production tree: topic3 88 passed, old 86 passed, topic1 88 passed (verification/reviewer_M2_r2b_1/tests/). Own copied tree (118 files, verified) control 88 passed. Own 36-mutant run in progress (background).

Last visited: 2026-11-01T01:40Z
- 2026-11-01T01:55Z — Own mutant run 1 (36 mutants, 6 parallel): 18 survivors on the final 88-test suite, incl. V01 (primary uses raw p, not Holm), P01/P02/P03 (CI wiring at paired_log_contrast call site), A01 (A2/D3 NeuroSTORM positions -> first 25 rows), V10, A04, X01/X02 (script wiring). Incident: earlyoom SIGTERM to pool workers at 10:31:47 KST hung 3 first-wave jobs in test_token_job_driver (mp.Pool.map waits forever); I killed only my own hung PIDs, record in verification/reviewer_M2_r2b_1/incidents/; those 3 are rerun in run 2. Estimand probe: addendum 03 items 1-3 numbers confirmed; 16/25 NeuroSTORM positions >= 25 (A01 non-equivalent on real data). Worker receipts consistent (run1 0/69 logs match = disclosed overwrite; run2/run3 69/69; runner snapshot hashes match). Layout lint PASS. HEAD 7430043 holds final addendum_04 a1828b38. Run 2 (reruns, repeats, challenger replay, demo-test kills) in progress, 3 parallel.

Last visited: 2026-11-01T01:55Z
- 2026-11-01T02:05Z — Run 2 done: challenger N02/N05/N06/N08-N11/N17 all KILLED (replay); V01/P01/P02/P03/A01/V10/A04/V04 survive again; demo tests kill V01/P01/P02/P03/A01. Real-data reruns reproduce pinned Family A/B exactly; A01 changes 78 A2 numbers, D3 unchanged. Final C1 rc 0 (identical to baseline), pins rc 0, ID grep rc 1, copied trees deleted, no processes left. handoff.md written. Verdict REQUEST_CHANGES.

Last visited: 2026-11-01T02:05Z
