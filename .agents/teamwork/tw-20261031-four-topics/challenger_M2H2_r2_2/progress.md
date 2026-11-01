# progress — challenger_M2H2_r2_2
Last visited: 2026-11-01T20:10Z
- 20:02Z dispatch received; read role/adapters, ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME, sci-pipeline.
- 20:05Z C1 rc 0; output_sha256 / addendum_07 / addendum_08 receipts rc 0. Card frozen 15:57:40Z, committed 35d10a5 16:05:25Z; gate job 16:22Z.
- 20:10Z plan: (1) suites; (2) independent recompute of C/L + errata; (3) test-the-test (corrupt shipped oracle); (4) new mutants outside r1 union; (5) ID scan, ledger append-only.
- 20:08Z suites: tests/topic3_spectral 138 passed; tests/topic3_h2 167 passed (185.8 s).
- 20:09Z independent recompute (verification/challenger_M2H2_r2_2/recompute_independent.py, no src/topic3_h2 import): 24/24 labels equal shipped, max abs diff 1.8e-15; E1 transitions, E8 single-seed labels, E2 R1 numbers, E3 L0 numbers reproduced.
- 20:11Z launched new_mutants.py detached (44 new mutants + 6 oracle mutations, 2 trees).
- 20:12Z gate record consistent with card §4 (G1 max rel_fro 7.8e-7, G5 all 84 cells fail per control). Report §3 "one seed's effect (-0.079)" at L2 cov token is inaccurate: 5 seeds' effects >= -log1.10 (not in errata).
Last visited: 2026-11-01T20:13Z
