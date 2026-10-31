# progress — challenger_r2_2

Last visited: 2026-10-30T13:45Z

- [x] Read role, adapters, ORIGINAL_REQUEST, APPROVED_PROPOSAL, ACCEPTANCE, PROJECT; production src/tests/script
- [x] Baselines: protected 44 OK; card sha + §12 10/10; entry-point copy identical; new suite 53 passed; old suite 86 passed rc=0
- [x] A3 rerun (verification/challenger_r2_2/a3): positions independently derived [1578,1228,932,0,57]; 0/225 deterministic mismatches vs r1 and r2
- [x] P1 networkx oracle N=304 ensemble path: 8/8 OK
- [x] P2 end-to-end reversal via NpyCohort.load at 7 TRs: ALL_OK
- [x] P3 adversarial loader: n_roi not enforced (transposed/303/305/12-ROI files load silently)
- [x] P4 mixing af 20..400: <=0.22 sd null-mean shift
- [x] P5 own 33 mutants: 21 killed, 12 survive (1 equivalent, 1 masked)
- [x] P5b own 4 iteration-1 blocker wiring mutants: full 4/4 KILLED, old_only 4/4 SURVIVE (total 37: 25 killed)
- [x] P6 production correct on every surviving surface: ALL_OK
- [x] Final: protected 44 OK rc=0; prod 21/21 unchanged; no pycache; ID scan 0 hits
- [x] handoff.md written; verdict CONFIRMED (nonblocking requirements before step 5)
