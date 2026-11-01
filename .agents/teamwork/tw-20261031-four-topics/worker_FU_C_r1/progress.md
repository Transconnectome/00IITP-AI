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
