# progress — challenger_M2H2_r1_2
Last visited: 2026-11-01T17:16Z
- 17:02Z read role/runtime/acceptance/PI decisions/gate status/resume; DISPATCH.md written
- 17:05Z independent recompute: 24/24 family C/L labels match, numbers identical to 1.8e-15
- 17:06Z C1 rc 0; output_sha256 OK; addendum_07 receipt OK; 2026-10-31 receipts OK except known card_sha256.txt format
- 17:10Z submitted connectome Slurm job 218068 (seed-8 independent rerun), ledger start row appended
- 17:13Z tests/topic3_h2: 71 passed (375 s; host load ~70)
- 17:14Z launched mutation harness (53 mutants, 2 trees) detached; log verification/challenger_M2H2_r1_2/mutants_ch2.log
- 17:15Z GPU probe 218068 COMPLETED (274 s, 0.077 GPU-h): independent seed-8 rerun (own code from git + own numpy PR) reproduces shipped R8 scalars/subsets to rel <= 2.3e-15; encoder hash equal; ledger closing row appended; own connectome dir deleted
- 17:16Z fuzz of decide(): 200k cases incl. exact boundaries, 0 mismatches vs independent transcription
- 17:16Z result-report secondary numbers spot-checked against h2_results.json (E1, per-seed D1/H1a, R1/A1b, medians, alpha): all match
Last visited: 2026-11-01T17:16Z
