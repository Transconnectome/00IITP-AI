# progress — explorer_FU_A_r1_1

Last visited: 2026-11-01T14:19:03Z

- 14:16Z dispatch saved; governing docs + r1 Topic 2 artifacts + code read.
- 14:41Z B300 checks (read-only, 0 GPU-h): Slurm idle; .98 = b300-01; /scratch node-local; r1 split maps to repo h-tokens by rank (p01 all true); cellmeans present for 88.
- Ledger: 11.99 GPU-h completed; FU_A_r1_3 runs the FU-A throughput/packing smoke (job 403) -> I do not duplicate (0 GPU-h).
- p02 smoothing-bias probe done: block mean unbiased/no leak; Gaussian 6/12 mm -> spurious E>C r +0.043/+0.128, leak 0.085/0.186.
Last visited: 2026-11-01T14:41:41Z
- p03 calibrated fixture probe: sigma_v 4.74; F+ 12mm purity 1.0, +0.297; single voxel +0.006; F- never favours C.
- r1 val curves: F+ gain grows with training; F- bias shrinks -> reduced-budget gates invalid.
- p04 verdict sketch 22/22 cases, 15/15 mutants killed.
- C1 rc 0; code freeze 33/33; output_r2 156/156; B300 probe dir removed.
- handoff.md written (Hard). 0 GPU-h used.
Last visited: 2026-11-01T14:52:13Z
