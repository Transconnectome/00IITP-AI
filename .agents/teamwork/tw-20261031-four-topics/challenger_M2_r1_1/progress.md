# progress — challenger_M2_r1_1
Last visited: 2026-10-31T11:19:42Z
- read role/runtime, ORIGINAL_REQUEST, ACCEPTANCE, card, code, report, addenda, worker handoff.
Last visited: 2026-10-31T11:39:10Z
- C1 rc0 (67 OK); output/code/addendum_02 pins OK (launcher differs, disclosed).
- topic3 suite in copied tree: 54 passed (509 s, loaded host).
- Family A independent recompute: matches frozen to <=1e-14; independent subsets give same D1/D3.
- T3.1: uncentered PR == json PR (4 dp) for all 7; centered == report.
- Family B independent recompute: means exact; own 200k sign-flip + bootstrap + Holm; rule -> H1a holds, H1b not replicated (matches).
- Freeze order: card sha file 08:48:29Z; Family A 08:49:18Z, token job 08:51:32-08:58:52Z, Family B 09:01:59Z; code hashes in all 6 run records == freeze list.
- NEW: token matrices L2/LN0L2/L3 have numerical rank 7 (=8 spatial positions - 1); connectome probe: L3 variance over 20 time steps at fixed position = 1e-6 (primary) / 1e-5 (HCP) of total. Token PR = PR of 8 spatial-position vectors; "ceiling 1119" misdescribes the data.
- mutation run 1 INVALID (harness omitted protected old src modules; control failed); relaunched 11:37Z.
Last visited: 2026-10-31T11:43:47Z
- mutation run 2: control 54 passed; 28 mutants, 20 killed, 8 survived (N02 N05 N06 N08 N09 N10 N11 N17); N05 flips real H1b verdict.
- connectome probe done (srun node2, stdin only, no files there); squeue empty.
- cleanup: tree/ and scratch mutant trees removed; C1 rc0 after; pins OK after; ID grep no hits; layout lint findings [].
- handoff.md written.
