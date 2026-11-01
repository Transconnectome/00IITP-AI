# progress — explorer_FU_E_r1_2
Last visited: 2026-11-01T14:50Z
- 14:32Z DISPATCH.md + BRIEFING.md written; role/adapters + run docs read.
- 14:40Z result report §0-§8, frozen train.py/model.py/topic2_train.py read: HCP runs (waves 3-4) used --save-model -> model_final.pt under /scratch/iitp4/worker_M3_r1/runs/hcp_*/ on .98.
- 14:45Z B300 ssh timed out twice (dgx1 hop timed out); peers report banner timeouts too. Retrying in background.
Last visited: 2026-11-01T14:50Z
- 14:38Z B300 read-only: all 15 r1 hcp_* model_final.pt present (156,184,449 B each, mtimes 13:10-14:09 KST); 88 prepped subjects; Slurm up.
- 14:45Z B300 counts only: HCP dir has REST1_LR ONLY (no REST2, no RL); 103 complete REST1_LR files now (88 r1 + 15 incl. 5 burned); no behavioral CSV on B300.
- 14:46Z local CPM-tutorial unrestricted CSV (n=337, binned Age, Gender) found; in-memory overlap with B300: 28 labelled subjects total (r1 split: test 5, val 2, train 17; new <=4).
- 14:48Z ledger started row + sbatch job 412 (debug, 1 GPU, 12 min) submitted: ckpt integrity, anchor, strict=False failure mode, embedding cost.
