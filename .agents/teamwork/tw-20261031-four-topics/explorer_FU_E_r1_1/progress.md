# progress — explorer_FU_E_r1_1
Last visited: 2026-11-01T14:43Z

- 14:20Z read role/runtime/adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addendum), PI decisions 1–8, GATE_STATUS, RESUME; DISPATCH.md written
- 14:23Z B300 .98 read-only: 15/15 r1 checkpoints present (156,184,449 B each)
- 14:30Z Slurm: 4 nodes idle; .98 = b300-01 (cloud-S1HDe3); /scratch node-local md0. REST1_LR staged for 103 subjects (88 r1 + 5 burned + 10 new); REST1_RL/REST2_* = 0. r1 venv: torch 2.15, numpy 2.5.4, scipy 1.18.1, NO sklearn
- 14:35Z labels: only OA subset n337 (unrelated subjects; Subject/Gender/Age banded) found locally; in-memory overlap with 103 REST1_LR subjects = 28 (13 M/15 F; ages 4/12/12/0)
- 14:38Z synthetic design probe run: verification/explorer_FU_E_r1_1/probe_design_sim.out.json
- 14:41Z Slurm smoke job 407 submitted (debug, b300-01, 1 GPU, 12 min limit); ledger started row appended
- next: poll 407, close ledger row, copy aggregate output, write handoff
- 14:41:28Z job 407 COMPLETED (15 s, 0.005 GPU-h); ledger completed row appended; outputs copied (sha256 3/3 OK) to verification/explorer_FU_E_r1_1/{smoke_out.json,smoke_slurm407.log,smoke.sbatch,b300_sha.txt}
- 14:55Z handoff.md written; C1 rc 0 (67/67); code freeze 33/33; output_sha256_r2 0 failures; whole-run audit_layout: 344 files, 0 findings
- 14:58Z B300 dir /scratch/iitp4/explorer_FU_E_r1_1 removal requested (first ssh timed out; retry in flight)
Last visited: 2026-11-01T14:58Z
- 15:00Z B300 dir /scratch/iitp4/explorer_FU_E_r1_1 removed (confirmed); 0 fue_e_smoke jobs in squeue. DONE.
Last visited: 2026-11-01T15:00Z
