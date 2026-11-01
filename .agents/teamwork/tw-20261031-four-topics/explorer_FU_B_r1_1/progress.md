# progress — explorer_FU_B_r1_1

Last visited: 2026-11-01T14:40Z

- 14:16Z DISPATCH.md written; role/runtime/run docs read.
- 14:25Z r1 card, report, addenda, train/verdict/stats code, r1 run timings read.
- 14:35Z B300 probes (read-only, counts only): Slurm partitions gpu/interactive/debug on b300-[01-04]; .98 = b300-01 (cloud-S1HDe3); /scratch node-local md0 ext4; r1 preprocessed HCP (88 subjects, 126G) and venv (torch 2.15.0+cu134) present under /scratch/iitp4/worker_M3_r1.
- Next: Slurm smoke (reproduction anchor + 35k-step throughput projection), synthetic verdict-defect probe, handoff.
- 14:50Z Slurm smoke job 413 (debug, b300-01, 1 GPU) 14:50:02-14:53:53Z, 0.065 GPU-h, ledger start+close rows; r1 anchor bit-identical; 35k projection 1.694 h.
- 15:0xZ CPU probes: frozen verdict on FU-B layout (3/4 wrong), reference wrapper + mutants (18/19 killed, V11 equivalent), operating characteristic.
- 15:1xZ B300 scratch dir removed; ssh masters closed; C1 rc 0; code freeze 33 OK; output_sha256_r2 OK.
- handoff.md written (Hard). DONE.
Last visited: 2026-11-01T15:20Z
