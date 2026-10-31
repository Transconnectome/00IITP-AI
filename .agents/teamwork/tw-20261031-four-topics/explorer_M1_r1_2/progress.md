# progress — explorer_M1_r1_2
- 2026-10-31 (start) read role/runtime/claude-code adapters, ORIGINAL_REQUEST, ACCEPTANCE, orchestrator PROJECT.md. Wrote DISPATCH.md.
Last visited: 2026-10-31 start
- 17:00 proposed_tests/test_extract_contract.py: 5 passed on production (2.1 s)
- 17:02 mut_harness (copies, repointed): without proposed: control+5 survivors all rc=0 (54 passed). With proposed: control 59 passed; 19/19 + 4/4 killed
- 17:05 probe_stats_design: rank OK (27/27, ybocs 26/26, med 15/15, n_med=301 180/121); FL within FPR .0425 (R=400,B=999); across .035; dxperm .04; Welch 1.0; Mundlak max ratio 4e-13; B=9999 FL 1.6 s
- 17:07 probe_fl_across_adversarial: across-site FPR .06/.053 vs within .043/.047 (R=300) -> not detectable by FPR
- 17:08 probe_trunc200_lengths: native ceil(200/TR) -> 101 grid samples at TR .7,.85,1.73,1.8
Last visited: 2026-10-31 17:10 KST
- 17:20 wrote handoff.md (probes: trunc floor -> 100 at all TRs; RE path re_var>0, beta eq 1e-13, total-SD defect 0.257 vs 0.293 at ICC .3); ID scan 0 hits; mirrors removed; protected rc 0; §12 10/10
Last visited: 2026-10-31 17:07 KST
