# progress — challenger_FU_D_r1_2
Last visited: 2026-11-01T19:20:06Z
- [x] read role, adapters, ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME, card, result report
- [ ] receipts, freeze timing, recompute headline, verdict reimpl + mutation, records/meta checks, ledger, C4
Last visited: 2026-11-01T19:25:45Z
- [x] C1 rc0; receipts card 1/1 code 29/29 out 34/34; r1 freeze 33/33
- [x] card git commit 34f4b303 at 15:50:24Z with frozen sha, before first job submit 16:13:50Z
- [x] recomputed F+ NMSE from per-subject terms: exact; gains 0.003631/0.006546
- [~] B300 Slurm job 574 (re-eval checkpoints) submitted 19:25:24Z, ledger started row written; PENDING
- [ ] verdict reimpl/fuzz, mutation, records edge cases, smoke equiv, C4
Last visited: 2026-11-01T19:34:33Z
- [x] job 574 COMPLETED 50 s (0.014 GPU-h, ledger closed): 3 checkpoints re-evaluated, test NMSE bit-exact, perm buffers = pinned keys, perm-swap -> NMSE 1.10-1.12
- [x] verdict oracle fuzz 40000 cases 0 mismatches; 24 adversarial e2e script cases (2 gaps: NaN test_nmse accepted; unplanned dirs ignored when gate fails)
- [x] C4 scan 76 files: 0 IDs (one 6-digit hit = merge.py hash prefix)
- [~] own mutants M01-M29 running
