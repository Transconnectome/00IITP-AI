# progress — worker_M1_r1
Last visited: 2026-10-31T08:10:12Z
- 08:10Z read role/runtime/acceptance/card/open issues; metadata created.
- 08:25Z T1.1 done: new test installed (58 passed); mutants with: 19/19 + 4/4 killed, controls 59 passed; without: 5 survivors reproduced. Receipts in results/topic1/2026-10-31/t1_1_mutation/
- 08:16Z manifest built (1706 ok, 0 below floor, sha 063513c9…); primary extraction launched PGID 3858561, 14 workers nice 10
- 08:40Z stats script + tests written; stats mutants 20/20 killed; T1.1 v2 receipts (control 85 passed); validate launched (R=2000,Rc=300,Rp=300)
- 2026-10-31T08:38:01Z validate run1 aborted (script amended: family-1 literal 0.10 report on fallback; unused import); synthetic analyze smoke probe passed; validate run2 launched on sha f2589105…; extraction 450/1706
- 2026-10-31T10:56Z (resumed in a new context) found: primary extraction finished 09:27Z (1706 ok, 0 err, jsonl sha 948961c8…); validation receipt binds f2589105… but script now 33e27576… (post-Trinity amendments 09:08Z). Plan: re-validate final bytes, v3 mutation receipts, fix addendum, freeze, decide, analyze.
Last visited: 2026-10-31T10:56Z
- 2026-10-31T11:05Z added test_exclusions_are_counted_by_class_group_and_site (tests/topic1_lagmotif now 88); label-only card-count probe all 7 match; v3 receipts: T1.1 control 89 passed, 19/19+4/4 killed, without-new 5 survivors reproduced; stats v3 control 31 passed 24/24 killed; receipts copied to results/topic1/2026-10-31/t1_1_mutation/v3_final_tree/. Addendum V4/P14-P17/D2/D4 corrected (not yet frozen). Final validate running PID 844552.
Last visited: 2026-10-31T11:06Z
- 2026-10-31T11:13Z final validate on 33e27576 all_pass (identical numbers to run 2 except timings); old 86 passed; C1 rc0; card12 rc0.
- 2026-10-31T11:14:46Z FREEZE: stats_script_sha256.txt (33e27576), prelabel addendum sha 7ccb983e (chmod a-w), stats script chmod a-w.
- 2026-10-31T11:14:54Z decide (label-free): 0/1706 degenerate at broadband@0.10 -> no fallback, primary 0.10.
- 2026-10-31T11:15:03Z analyze (first label join): Topic 1 KILLED. E1 d=0.113 p_FL=0.0223 p_Holm=0.0446 (fails |d|>=0.15); E2 d=0.038 p_Holm=0.44. sensitivity: not run (no survivor).
- 2026-10-31T11:25Z deviations addendum + result report written; ID scan strict/all 0 hits; layout lint 0 findings; topic1 88 passed.
- DONE. No process of mine running.
Last visited: 2026-10-31T11:30Z
- 2026-10-31T11:31Z analyze reproduced on a copy (verification/worker_M1_r1/repro_analyze, removed after): stats_results.json identical except elapsed_s.
- 2026-10-31T11:40Z final edits (report provenance line + per-site table; handoff push caveat corrected); validation diff confirmed timings-only; ID scan 0/0, RESULTS_SHA256SUMS ok, C1 rc0, card12 rc0, lint 0 findings. Result report sha 1542055d…
Last visited: 2026-10-31T11:40Z
