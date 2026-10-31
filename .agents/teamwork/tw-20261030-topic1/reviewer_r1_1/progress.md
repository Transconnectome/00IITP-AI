# reviewer_r1_1 progress (2026-10-30)
- Read role/runtime adapters, ORIGINAL_REQUEST, APPROVED_PROPOSAL, ACCEPTANCE, PROJECT.
- Read all production code/tests/script/results/card/OPEN_ISSUES.
- Re-ran: new tests 29 passed; old 86 passed (rc=0); protected hashes 44/44 OK; card sha256 matches; card §12 10/10 OK; params_sha256 matches.
- Verified from files: cohort counts, TR distribution, absent-by-site, Y-BOCS, medication counts and contradictory coding lines, baseline AUROCs, no motion columns, cache order == sorted listdir.
- ID scan of 30 new files: 0 hits.
- Mutation probe (12 mutants): 10 killed, 2 survived (invariant raise disabled in null_counts = equivalent unless chain broken; pipeline detrend wiring not tested at a resampled TR).
- Reruns: spurious_direction.json reproduced exactly (max diff 0); A3 timing reproduced deterministically (same positions, acceptance, |dZ|), wall time 1.43x slower under concurrent load.
- Probes at N=304: white-noise H0 calibration of Z030C/Z030T/E2 within ~2 SE across T=100..3000 (no consistent bias); factor 20 vs 100 converged (|dZ030C| <= 0.2) incl. gradient-dominated graphs.
- Verdict: APPROVE (non-blocking issues listed in structured return).
