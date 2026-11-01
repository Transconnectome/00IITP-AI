# progress — challenger_M3_r2_2
Last visited: 2026-11-01T09:31Z
- 09:27Z dispatch recorded; role/runtime/acceptance/resume/PI decisions read.
- 09:31Z BRIEFING written; starting orientation on artifacts.
Last visited: 2026-11-01T09:42Z
- 09:31Z C1 67/67 OK; code freeze 33/33; r2 pins 156 OK; sanitized pins 19 OK; old pins fail exactly 2+16 (as disclosed). c01_baseline_checks.txt
- 09:31Z seal_check repo all_ok (c02). Frozen verdict script reproduces verdict.json + stdout byte-identically (verdict_repro/).
- 09:32Z p01 independent verdict recomputation (own t quantile, own rules): stop; diffs <1e-16; gates pass.
- 09:35Z p02 on B300: independent semantic check of the 19 sanitized files vs sealed originals: all equal; num/den unchanged; split recomputes.
- 09:40Z p04: the 5 burned dev-subject salted hashes (verification/explorer_M3_r1_1, untracked) are reversible from repo content alone: 5/5 in 0.37 s (count only).
- 09:41Z p03 hash-set scan (worktree + all git blobs) running detached; log p03_scan.progress.log.
Last visited: 2026-11-01T09:52Z
- 09:41Z p03 hash-set scan done (136 s): 16,352 worktree files (2.89 GB) + 1,482 reachable git blobs: tok16 0, tokpart 0, csha64 0, fbytes 0; hcpname 34 entries / nvox 3 all coincidences (digits inside hex digests, float integer parts, PDF binary); sec uninformative.
- 09:44Z p05 new verdict-path mutants: 3 positive controls killed, baseline survives; 11 of 13 new mutants SURVIVE (boundary ops, F+ missing/failed-run handling, F- downgrading modify, stop under F+ failure, status/test-order guards). None changes the shipped verdict.
- 09:44Z local full suite: 14 files; test_partition.py and test_pipeline_guards_r2.py SIGTERMed by earlyoom (rc 143, host memory); all others pass; old86 86 passed; topic1 88 passed. Stopped local heavy runs (earlyoom also hit others' processes in the window).
- 09:50Z connectome: project-local CPU venv + full topic2 suite via srun (debug) launched; log ~/iitp4_verify/challenger_M3_r2_2/run.log on connectome.
Last visited: 2026-11-01T10:24Z
- 09:58Z p06 frozen verdict script on synthetic records: F+ fails + Stage 1 not run -> no_verdict (card: inconclusive); F- missing -> keep (disclosed erratum 8).
- 10:01Z connectome venv (project-local, /storage/connectome1/iitp4_verify/challenger_M3_r2_2, uv-managed py3.12, torch 2.15.0+cpu) built; full suite 92 passed; code sha 38/38 = local.
- 10:20Z p07 full-suite mutants on connectome: baseline survives; 11/11 new survive; 42/42 r1 survivors killed.
- 10:22Z cleanup: B300 /scratch/iitp4/challenger_M3_r2_2 removed; connectome dir removed; no jobs/processes left. p03 output redacted. handoff.md written.
Last visited: 2026-11-01T10:30Z — handoff.md final (Hard); layout lint PASS (267 files, 0 findings, c05_audit_layout.txt); no processes/jobs left on DGX-Spark, B300 or connectome; StructuredOutput next (REFUTED).
