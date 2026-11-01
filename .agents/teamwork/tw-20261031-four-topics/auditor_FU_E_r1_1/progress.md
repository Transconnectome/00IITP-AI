# progress — auditor_FU_E_r1_1
Last visited: 2026-11-01T17:35:18Z
- started; DISPATCH/BRIEFING written
- 17:36Z C1 rc 0 (67 OK); FU-E receipts card 4/4, code 18/18, output 12/12 OK
- 17:38Z independent CPU re-derivation of verdict from extract.json: 0 mismatches; F+ fails only S_s2 under 3 independent null seeds; verdict inconclusive (also inconclusive if all gates passed)
- 17:39Z verdict script rerun: byte-identical; tests/topic2_fu_e 71 passed; old 86 passed
- 17:40Z B300 sacct: 499/524 GPU jobs via Slurm, 549/551 CPU-only; no g3t-G-E0 jobs ever; B300 outputs sha = repo; code copy 10/10; venv no files newer than 2026-11-02 00:00 KST
- 17:42Z GPU repro probe NOT submitted: normal QoS has 8/8 user GPUs running + 37 pending; debug QoS would exceed the 8-GPU share rule
- 17:43Z submitted CPU-only Slurm job 556 (debug, no gres): ckpt sha re-hash + real-data cellfc reproduction (main/surrogate/subjmask)
Last visited: 2026-11-01T17:43:37Z
- 17:54Z job 556 done: cellfc main/surrogate/subjmask reproduce (max diff <=4.5e-9); ckpt sha 15/15; mutants 16/20 killed (3 equivalent, A04 gap); layout lint PASS; B300 dir removed, ssh closed; handoff written; verdict CLEAN
Last visited: 2026-11-01T17:54:39Z
