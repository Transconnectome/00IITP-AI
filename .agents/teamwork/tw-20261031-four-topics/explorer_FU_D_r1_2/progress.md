# progress — explorer_FU_D_r1_2
- 14:16Z dispatch saved; required docs read.
- 14:25Z read topic2 card/architecture/report/code; verdict defects V01–V11 read. B300 ssh banner timeout (retrying in background).
Last visited: 2026-11-01T14:25Z
- 14:30Z CPU probe verification/explorer_FU_D_r1_2/probe_e192_cpu.py rc 0: E192 config registers from outside src (same CONFIGS dict), geometry g16/octant8 same as E36, M0 = ConnectomeRGBoxPooling(PatchMergingV2 LN1536, Linear 1536->384), params 474,226,176 E==C, step-0 weights bit-identical, gather exact at dim 192.
- 14:35Z B300 facts: Slurm 4 nodes idle at 14:2xZ; /scratch is node-local md0; only b300-01 (.98) holds /scratch/iitp4 and HCP raw (1084 dirs, counted only); other 3 nodes have neither; GPU 275040 MiB.
- 14:37:50Z ledger started row; Slurm job 396 (debug, b300-01, 1 GPU) released 14:38:11Z; other FU explorers' smokes (398,401,402,403) running on b300-01 concurrently.
Last visited: 2026-11-01T14:38Z
- 14:39:46Z Slurm 396 COMPLETED (97 s); smoke_fud.json + slurm-396.out copied back, sha match; ledger completed row 0.03 GPU-h; B300 dir /scratch/iitp4/explorer_FU_D_r1_2 removed.
- 14:5xZ probe_frozen_verdict_reuse.py: frozen verdict script A inconclusive / B keep (missing F- = pass) / C no_verdict (4 seeds) / D no_verdict (F+ fail) -> FU-D needs own verdict code.
- 15:05Z handoff.md written (Hard). gate_fixture KeyError on 2-arm F- confirmed.
Last visited: 2026-11-01T15:10Z
