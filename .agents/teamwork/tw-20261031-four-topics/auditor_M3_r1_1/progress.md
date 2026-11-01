# progress — auditor_M3_r1_1
Last visited: 2026-11-01T05:45Z
- 05:39Z DISPATCH.md written; role/runtime/acceptance/resume/PI decisions/sci-pipeline read.
- 05:42Z C1 rc 0 (67/67); card_sha256 rc 0; card first committed by host checkpoint 51609c1 at 03:16:27Z with sha c9bfc60a (= frozen).
- next: code-freeze vs run.json code hashes; verdict recompute; test run; source review; ledger audit; B300 forensic checks; ID scan; git writes.
- 05:50Z probe_runs: 27 run.json consistent (code hash = freeze, perms, split, recomputed NMSE, launch/GPU match, train_log/stdout match); independent t-intervals + verdict = stop; 0 problems.
- 05:52Z B300: 27 run.json byte-identical to local copies; code copy = frozen hashes; 15 checkpoints present; venv = project-local uv (no system site-packages); no enigma names under /scratch/iitp4; no topic2 processes. Partitions built 03:17Z, stage0 03:24Z (after freeze).
- 05:55Z tests: topic2 55 passed; old 86 passed.
- 06:00Z burned-subject exclusion verified on B300 (5 match, 0 in manifest/split); 93 files pre-manifest, later arrivals unused.
Last visited: 2026-11-01T06:01Z
- 06:00Z output_sha256 pins: 43/43 OK. Local ID scan (282 files incl. all docs/03_empirical_analysis): 0 hits.
- 05:56–05:57Z B300 .98 GPU 7: checkpoint re-eval (ledger rows started/completed 0.02 GPU-h). 15/15 perm buffers = claimed arm; hcp_E_s2, C_s2, S_s2, C_s0 test NMSE reproduced bit-exactly; facade diff > 0. Own B300 dir removed.
- 06:00Z mutation probe running on copies under verification/auditor_M3_r1_1/mut/.
Last visited: 2026-11-01T06:02Z
- 06:08Z git: all commits 02:00Z–06:01Z are host checkpoint cadence (:01/:16/:31/:46 +27 s), reflog has only those commits, no stash/reset/checkout. Report pre-result versions (04:01Z, 04:31Z) carried STAGE1_VERDICT_PLACEHOLDER (no pre-written verdict). Addendum 02 committed 04:01:27Z, before first HCP test value (04:10:48Z).
- 06:09Z ledger completed rows total 11.943 GPU-h (worker 11.73; cap 64). Whole-run audit_layout rc 0, 207 files, 0 findings.
- 06:10Z mutants so far: caught stop-rule, keep-ignores-I2, merge-ignores-perm, C-uses-euclid, partition-reads-test; SURVIVED relative_gain sign flip and NMSE-ignores-mask (test gaps; computation verified independently).
Last visited: 2026-11-01T06:10Z
- 06:18Z mutants done: 6 caught / 5 survived (relative_gain sign, NMSE mask, train-loss mask, split rule, HCP eval-mask seed); survivors verified directly (code lines, independent recompute, split recompute, identical test_den across runs).
- 06:20Z handoff.md written (verdict CLEAN + 4 non-blocking). Final local ID scan incl. own outputs/metadata: 308 files, 0 hits (id_scan_local_final.out.txt).
Last visited: 2026-11-01T06:21Z
- 06:25Z handoff relabelled (vacuous tests PASS; coverage gaps note), C4-print ruling + DISPATCH note added; scratch burned.txt deleted. Last visited: 2026-11-01T06:25Z
