# progress — challenger_M2H2_r2_1
Last visited: 2026-11-01T20:35Z

- 20:03Z DISPATCH/BRIEFING written; role/adapters/governance docs read.
- 20:10Z C1 rc 0; output_sha256 (61) rc 0; addendum_07/08 receipts rc 0; 2026-10-31 receipts as known (card_sha256 / code_sha256_at_freeze rc 1, pre-existing).
- 20:12Z Freeze timing: addendum 07 frozen 15:57:40Z, autocommitted 16:05:25Z (git 35d10a5, same sha 09b45220); gate job 16:22:19Z, random job 16:32:19Z. Job code hashes = repo code (20/20).
- 20:20Z Independent recomputation (verification/challenger_M2H2_r2_1/independent_recompute.py): 24/24 labels and all values equal shipped within 1e-12; δ recomputed from raw T equals frozen.
- 20:25Z Report number audit vs h2_results.json: all checked numbers match.
- 20:30Z Copied trees tree_a/tree_b built; baseline 167 (after adding scripts/topic3_* + tests/topic3_spectral copies needed by a receipt test).
- next: fresh mutation harness.
- (time correction: the clock read 20:15Z when the harness launched; the 20:35Z header above was an estimate)
- 20:15Z fresh-mutant harness launched detached (run_fresh.sh tree_a 0 / tree_b 1); baselines 167 passed in both trees (20:21Z).
- 20:17Z E1/E8 independently checked (single_seed_and_delta.py): E8 exact; E1 boundaries exact, but E1's "label closest to frozen δ is C3" is wrong: C2 (f 0.4580, distance 0.042) is closer than C3 (0.5483, distance 0.048).
- 20:19Z guard probe (tree_c): `final` does not check that the random job used the card index sets (record flag/hash ignored; permuted R subsets accepted). Shipped hashes equal card J -> nonblocking.
- 20:20Z ID scan clean; ledger append-only vs worker snapshot (prefix sha 9f9843eb); M2H2 GPU sum 0.819 verified.
Last visited: 2026-11-01T20:22Z
- 20:25Z gate record numbers (G1-G5) re-read: match report §1.
- 21:02Z fresh mutants 34/51 done; survivors so far are guard/defensive or in-job descriptive paths (F06, F07, F20, F21, F22, F42, F53, F55, ...). Waiting.
Last visited: 2026-11-01T21:03Z
