# progress — explorer_FU_D_r1_1
Last visited: 2026-11-01T14:55Z
- 14:16Z dispatch saved; run docs, role/runtime read.
- 14:2xZ topic2 card/report/architecture/addenda 01-05, gate record (V01-V11), src (model/train/merge/stats), verdict script read.
- 14:3xZ B300: Slurm idle b300-[01-04]; HCP preprocessed 88 subjects only on b300-01 (.98) /scratch/iitp4/worker_M3_r1/hcp (node-local md0); .99 has none.
- next: Slurm smoke E192 bs16 memory/step time (synthetic HCP-format tensors), seed-rule design, handoff.
- 14:42Z Slurm smoke job 404 (b300-01, 1 GPU, 92 s, 0.03 GPU-h ledgered): E192 bs16 0.491 s/step, peak 198.3/222.9 GiB alloc/reserved; proj 1.23 h/HCP run, 1.20 h/fixture run.
- 14:5xZ CPU probes: power/seed-rule simulation; E192 structure (M0 = stage-0 downsample, 16^3 -> 8^3, Linear 1536->384, gather applies unchanged; C init bit-identical to stock).
