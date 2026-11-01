# progress — explorer_FU_B_r1_2
Last visited: 2026-11-01T14:45Z
- 14:16Z dispatch recorded; read role/adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addendum), PI decisions 1-8, GATE_STATUS, RESUME.
- 14:20-14:40Z read r1 card/report/code; C1 rc 0; code freeze 33/33 OK; probed B300 Slurm (PreemptMode OFF, gpu MaxTime 2d, debug 30 min) and /scratch on 4 nodes (HCP raw+prepped only on b300-01 = .98).
- next: Slurm smoke on b300-01 (frozen code, 35k-step projection + 400-step full cycle + checkpoint size/time).
- 14:38-14:41Z Slurm job 402 (debug, b300-01, 1 GPU): projected 1.703 h/35k-step run; peak GPU 151874 MiB; ckpt 466 MB/0.43 s; ledger started+completed rows (0.06 GPU-h).
- 14:4xZ p01 (CPU determinism + schedule) and p02 (frozen verdict on FU-B layouts) done.
- 14:45-15:05Z .98 sshd flaky; cleanup of my B300 dir done via srun CPU step from .99 (1.4 MB code+logs left, 0 symlinks).
- handoff.md written. Done.
Last visited: 2026-11-01T15:10Z
