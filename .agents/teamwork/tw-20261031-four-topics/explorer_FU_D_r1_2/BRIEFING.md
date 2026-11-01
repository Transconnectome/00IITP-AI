# BRIEFING — 2026-11-01T15:10Z (updated)

## Mission
FU_D (Topic 2 follow-up D, E192 d2-2-18-2 scale): give the worker a concrete, verifiable strategy covering F1–F3 + C1–C8, with cheap-probe evidence. Lens: feasibility and failure modes. Recommend only.

## 🔒 My Identity
- Archetype: explorer (Teamwork General route), explorer 2 of 3 for FU_D
- Roles: explorer (read-only investigation + synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_D_r1_2
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_D
- Host: claude-code (Opus 5.5 subagent); no nested spawning; final report = StructuredOutput

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes only under /home/juke/git/00IITP-AI/verification/explorer_FU_D_r1_2/
- C1–C8; no participant IDs printed/written; no git writes; no installs on DGX-Spark; no secrets
- B300 GPU only via Slurm sbatch/srun; ≤0.25 GPU-h ledgered smoke; ledger under flock
- src/topic2_rgpool frozen (import only); r1 card frozen; never touch other teams' /scratch/iitp4 dirs
- local python: PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; ≤2 pytest, timeout 900

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: run docs (ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME); topic2 card, architecture, result report §7; src/topic2_rgpool merge/model/train/stats; scripts/topic2_verdict.py, topic2_launch_wave.py; M3_r2_gate_record (V01–V11); explorer_M3_r1_1/2 E192 smoke numbers; VRABES E192 script args
- **Key findings**: E192 reuses r1 perms/geometry unchanged (CPU probe); measured 0.481 s/step bs16, 1.20 GPU-h/run, peak 198/268 GiB (Slurm 396, 0.03 GPU-h); HCP + iitp4 only on b300-01; frozen topic2_verdict.py mislabels all reduced designs (probe); gate_fixture KeyError for 2-arm F-; train.run writes original tokens (C4); default --max-run-hours 0.75 aborts E192
- **Unexplored areas**: real-HCP E192 trainability; 8-job node contention; topic2 test suite not run

## Key Decisions Made
- Smoke used synthetic data only + a dummy GPU allocation equal to HCPSource size (done, job 396)
- Recommend: F+ 1 seed (3 runs) -> cost-only seed rule (5/4/stop) -> 15 Stage-1 -> F- (E,C s0) iff would-be keep; own verdict script with tri-state gates

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report (Hard)
- /home/juke/git/00IITP-AI/verification/explorer_FU_D_r1_2/ — probes, smoke_fud.json, slurm-396.out, stage manifest
