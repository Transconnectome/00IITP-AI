# progress — auditor_FU_D_r1_1

- 19:19Z DISPATCH.md, BRIEFING.md written; governing docs, role, adapters, sci-pipeline read.
- 19:20-19:27Z C1 rc 0 (67 lines OK); FU-D receipts card 1/1, code 29/29, outputs 34/34 OK; r1 code freeze 33/33 OK; code file set == freeze list; all code mtimes < freeze, all outputs > freeze.
- Tests: tests/topic2_fu_d 129 passed (88 s); old suite 86 passed.
- B300 sacct: FU-D GPU jobs = 511, 534, 535, 536 only (+ explorer 396/404/418/430); ledger rows match sacct ElapsedRaw; B300 files sha256 == local copies.
- 19:28:15Z submitted own probe Slurm job 576 (debug, 1 GPU, 20 min): re-score 3 F+ checkpoints; ledger started row written (flock, scripts/topic2_ledger.py); share check 0 g3t-G-E0 jobs.
Last visited: 2026-11-01T19:29Z
