# progress — challenger_FU_D_r1_1
Last visited: 2026-11-01T19:20:15Z
- 19:19Z dispatch recorded; governing docs read; card + report + verdict.json read
Last visited: 2026-11-01T19:27:10Z
- receipts card 1/1, code 29/29, outputs 34/34 OK; C1 rc 0; r1 code 33/33 OK
- card in autocommit 34f4b30 (15:50:24Z) with sha 1b7fee6c… = frozen; first FU-D job 511 submitted 16:13:50Z; gate runs started 17:46Z → freeze-before-results holds
- recomputed F+ NMSE from per-group num/den: exact; gains 0.0036313 / 0.0065460 → fail
- run fud_meta/run.json code hashes = FU-D freeze + r1 freeze; perms sha match fixtures json
- pytest tests/topic2_fu_d: 129 passed (97 s)
- B300: Slurm job 575 (debug, re-eval of 3 checkpoints) submitted 19:26:10Z held→released; g3t-G-E0 check: none. PROCEDURAL SLIP: flock syntax error → job released before ledger row; row appended 19:2xZ while job still PENDING (0 GPU-h used at that time)
