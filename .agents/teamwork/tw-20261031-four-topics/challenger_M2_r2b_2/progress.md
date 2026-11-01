# progress — challenger_M2_r2b_2

Last visited: 2026-11-01T01:26Z

- 01:20Z dispatch recorded; read role, runtime adapters, ORIGINAL_REQUEST, ACCEPTANCE, RESUME note.
- 01:22Z read iteration-1 REFUTED (challenger_M2_r1_1), card, hash receipts, analysis/resampling/estimators/token_job, scripts, verdict tests, addenda 03 and 04.
- Next: sci-pipeline skill, report/addenda 01–02, worker_M2_r2b handoff; then integrity baseline, copied tree, own mutants, recompute, freeze-order check.

Last visited: 2026-11-01T01:36Z
- 01:25Z baseline: C1 rc0 67 OK; output/add02/add03/add04 pins rc0; card hash OK; code freeze only launcher differs (disclosed).
- 01:27Z freeze order: card mtime 08:43:40Z, git 24fe976 (08:46:25Z) holds card at frozen hash (only commit), card_sha256 08:48:29Z, Family A started 08:49:18Z, token jobs 08:53-08:58Z, Family B 09:01:59Z; all run-record code_sha256 == freeze.
- 01:28Z copied tree (95 files, manifest == production); control 88 passed.
- 01:29Z own mutant run run_c2_A launched (34 own + 9 AST re-checks, 4 workers).
- 01:33Z probe_numbers: Family B means/CIs/verdicts reproduce independently; addendum numbers check; L1 top-63 min 0.99993998 (worker mismatch confirmed); H4 L0 ceiling is 159 (160-token subsample), not 383 -> addendum 03 §2 error.
- 01:35Z probe_survivor_impact: A07 reachable witness (killed -> holds); A06 non-equivalent, no D3 flip; S01 flips H1a if script rerun.

Last visited: 2026-11-01T01:48:20Z
- run_c2_A done: controls 88/88; 27 survivors of 34 own (classified in handoff); W_ re-check 9/9 killed (MM06 only by r2b file).
- witness tests: shipped 3 passed; A06/A07/A08 each fail their witness.
- full shipped rerun in copied tree: Family A/B JSON identical to pinned (0 diff leaves), 43 s.
- T3.1 check OK; git provenance of addenda checked.
- rerun-then-test protocol (rerun_c2_B) running.
