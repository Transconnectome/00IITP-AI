# progress — challenger_FU_E_r1_1
Last visited: 2026-11-01T17:38Z
- 17:34Z read role/adapters/run docs; C1 PROTECTED_HASHES rc 0
- 17:35Z all FU-E receipts OK (card 4/4, code 18/18, output 12/12, r1 freeze 0 non-OK)
- 17:36Z independent recompute from extract.json: all governed numbers match verdict.json (max abs diff 1.4e-14); F+ S_s2 fail robust (5 alt null seeds p95 10.3–11.1, derangement p95 10.87, MC p 0.19)
- 17:37Z verdict script rerun byte-identical; descriptive table audited, matches
- 17:38Z tests/topic2_fu_e 71 passed
- next: mutation testing; timeline/freeze check; C4 scan; ledger check
Last visited: 2026-11-01T17:50Z
- 17:40Z mutation harness launched detached (52 own mutants; verification/challenger_FU_E_r1_1/mutants/)
- 17:44Z B300 probe job 557 submitted (G3T_CHECK none 17:44:14Z), debug, synthetic only; ledger started row appended under flock; PENDING QOSMaxGRESPerUser (8 user GPUs busy, ~36 pending)
- 17:47Z edge-case records (edge/edge_cases.out): duplicated/reordered/wrong-pool subject labels in governed main pool not caught (verdict keep instead of no_verdict); Idiff_E=0 maps to inconclusive (card order step 2 says no_verdict). Shipped record verified canonical in all 6 conditions -> no effect on shipped verdict
- git: card committed by autocommit 16:35Z with frozen hash 072553b0 (before job 524 start 17:03:57Z); pre-freeze version (16:05Z) differs only by the smoke-499 disclosure
