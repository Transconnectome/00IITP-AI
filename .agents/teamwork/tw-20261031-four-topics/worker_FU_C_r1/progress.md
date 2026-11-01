# progress — worker_FU_C_r1
Last visited: 2026-11-01T15:20Z
- 15:15Z read role/runtime/claude-code adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addenda incl. B300 sharing rule), PI decisions, GATE_STATUS, RESUME, sci-pipeline.
- 15:16Z DISPATCH.md, BRIEFING.md written.
- 15:18Z ssh master to B300 b300-01 OK; squeue: only job 443 gard-t2-fold4 (b300-02). No g3t-G-E0-* job seen.
Last visited: 2026-11-01T16:06Z
- 15:28Z B300 venv /scratch/iitp4/fu_c/venv built from r1 lock; uv pip freeze == lock.txt (sha ae664dc9, 38/38).
- 15:4xZ code staged to /scratch/iitp4/fu_c/code (16/16 frozen files == code_sha256_at_freeze pins).
- 15:4xZ positional hard-link data view hcp_pos (88/88; relabelled r1 split == repo sanitized split; train/val/test 64/8/16).
- 15:5xZ perms_fu_c.npz built by frozen builder (S_SEEDS override in memory): self-check 25/25 (FC sha, counts, E/C/G/R/S0..4 == r1); S_seed10..17 distinct; npz sha f9e32ab7…
- 16:04:50Z anchor Slurm job 501 submitted (debug, -w b300-01, 1 GPU, 15 min); squeue g3t-G-E0-* check: none; admission 11.55 <= 13. Ledger started row written.
- ssh: banner timeouts / scp hang -> persistent master + base64 transfer.
Last visited: 2026-11-01T16:17Z
- 16:08Z anchor job 501 COMPLETED (210 s, 0.058 GPU-h, closing ledger row): 6/6 loss comparisons bitwise equal to r1; no val/test computed.
- 16:10Z pre-freeze artifacts copied back (sha verified): env/, partitions/, anchor/.
- 16:13:23Z CARD FROZEN: docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_card.md sha fc2d0672…; receipt results/topic2/2026-11-02_fu_c/card_sha256.txt (41 lines, 0 failures).
- 16:13:51–16:15:20Z wave 1 submitted (jobs 512-515, 517-520): g3t-G-E0-* check none; admission 12.48 <= 13.
Last visited: 2026-11-01T16:35Z
- 16:2xZ verdict layer src/topic2_fu_c/verdict.py + receipts.py + CLI; tests/topic2_fu_c 109 passed; flake8 clean.
- 16:2xZ mutation harness verification/worker_FU_C_r1/mutants: r1 44/55 killed -> added 6 tests -> r2 51/54 killed (3 equivalent: V07c, V12, F11; baseline survives).
- 16:31:53Z verdict code + tests pinned: results/topic2/2026-11-02_fu_c/code_sha256_before_results.txt. No Stage-1 job had started (all PENDING, QOSMaxGRESPerUser).
- CLI dry run (no runs dir) -> no_verdict (fail closed).
