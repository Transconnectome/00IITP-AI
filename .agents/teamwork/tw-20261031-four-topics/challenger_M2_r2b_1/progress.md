# progress — challenger_M2_r2b_1
Last visited: 2026-11-01T01:27Z
- 01:21Z dispatch recorded; role/runtime/acceptance/resume/card/report/addenda 01-04/challenger_M2_r1_1 handoff/source/tests read.
- next: freeze-order check (git + mtimes + hashes), C1 baseline, copied tree, own mutants, recompute numbers.
Last visited: 2026-11-01T01:40Z
- 01:2xZ C1 rc0 (67 OK); output/add02/add03/add04 pins rc0; code_sha256_at_freeze only launcher FAILED (disclosed).
- Freeze order: card blob in git 24fe976 (08:46:25Z) = 68337456…; sha file 08:48:29Z; family A 08:49:18Z; token jobs 08:53-08:58Z; family B 09:01:59Z. CONFIRMED.
- Family B independent recompute + exact replay = frozen (|d|=0); own-seed verdicts H1a holds / H1b not replicated. Family A E1 1.2e-14, replay 1.8e-15; D1/D3 true with own subsets.
- Mutant run1 ABORTED (driver-test mp.Pool hang; my SIGKILL of hung procs produced 3 false kills) — receipts kept, README in verification/.../mutants/. run2 launched 01:40Z with 1 BLAS thread + timeouts.
Last visited: 2026-11-01T02:15Z
- 01:47Z mutant run2 done: 29 mutants, controls 88/88 start+end, 6 killed, 23 survived (0 hangs). Iteration-1 survivors rerun (8/8 killed).
- 01:49-01:53Z copied-tree full rerun: 0 value differences vs frozen; mutant-tree reruns: V26 flips real H1a (holds -> not replicated).
- reachability: V01 (seeds 1000-1002), V06/V07/V08 (50001-50003), V05 (scenario C) flip verdicts on synthetic data.
- incidents disclosed: run1 aborted (false kills from my SIGKILL), rerun stdout logs deleted by rm glob.
- final: C1 rc0, pins identical, 68 topic3 production files unchanged, ID grep none, layout PASS. Handoff written. Verdict REFUTED (scoped).
