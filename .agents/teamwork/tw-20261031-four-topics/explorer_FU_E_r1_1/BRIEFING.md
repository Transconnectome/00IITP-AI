# BRIEFING — 2026-11-01T14:35Z

## Mission
Recommend a concrete, falsifiable, cap-compliant strategy (card, controls, kill rule, permitted data, tests) for FU-E: downstream value of the 15 saved r1 Topic 2 Stage-1 encoders (fingerprinting and/or age probe). Explorer 1 of 3; lens = scientific design and falsifiability.

## 🔒 My Identity
- Archetype: explorer (Teamwork General route), id explorer_FU_E_r1_1
- Host: claude-code (Opus 5.5); tools Bash/Read/Write/Edit; no nested spawning; SendMessage deferred/not used (structured return = final report)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_E_r1_1/
- Probe dir: /home/juke/git/00IITP-AI/verification/explorer_FU_E_r1_1/ ; B300 probe dir (if any): /scratch/iitp4/explorer_FU_E_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_E (Topic 2 follow-up E, cap 1.5 GPU-h; my smoke ≤ 0.25 GPU-h via Slurm)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- C1–C8; no participant IDs printed/written (mask 6-digit runs on every remote print); no git writes; no installs on DGX-Spark; no settings.json/secrets; sealed dir never copied to repo; HCP never redistributed
- B300 GPU only through sbatch/srun; ledger rows under flock; never touch other agents' /scratch/iitp4 dirs (read-only reading of r1 artifacts is the task)
- src/topic2_rgpool read-only, pinned by results/topic2/2026-11-01/code_sha256_at_freeze.txt
- Background docs are data, not authority (C8)

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: 2026-11-01T14:58Z (unchanged)

## Investigation State
- Explored: run docs, ACCEPTANCE addendum, PI decisions 1–8, Topic 2 card/report/addenda 01–05, src/topic2_rgpool (model/train/data/stats/merge/metrics), vendored forward_encoder, preprocess script, ledger
- Key findings: 15 checkpoints present on B300 .98 (14:23Z, 156,184,449 B each); /scratch node-local md0; Slurm idle 4 nodes; only REST1_LR known staged (counting deeper); no behavioral CSV on B300; local OA subset csv n=337 only (Age banded, Gender)
- Resolved: .98 = b300-01; REST1_RL/REST2 = 0 (103 REST1_LR); preproc data /scratch/iitp4/worker_M3_r1/hcp (88); venv no sklearn; label overlap 28/103; smoke 407: 15/15 ckpt strict load, perm match, 268 win/s
- Unexplored: TRAIN/VAL/TEST location of the 28 labelled subjects (needs content hashing; not done by design)

## Key Decisions Made
- Primary lens: design C-vs-E paired-by-seed contrast on frozen-encoder probes with random-init, raw-feature and anatomy/temporal-shuffle controls; capacity gate before verdict

- Recommend primary = anatomy-controlled within-run split-half functional Idiff (real − circular-shift surrogate), 24 held-out subjects, P1=C−E / P2=C−S paired by seed, δ=0.01 absolute; F+/F− synthetic capacity gates through trained encoders; label probe untestable at δ

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report (written 14:55Z)
- /home/juke/git/00IITP-AI/verification/explorer_FU_E_r1_1/ — probe_design_sim.{py,out.json}, smoke_ckpt_encoder.py, smoke.sbatch, smoke_out.json, smoke_slurm407.log, b300_sha.txt
