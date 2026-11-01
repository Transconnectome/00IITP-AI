# BRIEFING — 2026-11-01T14:20Z

## Mission
FU-A (Topic 2 follow-up A, lower-noise reconstruction target): recommend a concrete, verifiable, falsifiable strategy (card, target definition, controls, gates, kill rule, permitted data, compute fit within 8 GPU-h) for the FU-A worker. Primary lens: scientific design and falsifiability.

## 🔒 My Identity
- Archetype: explorer (read-only investigation)
- Roles: explorer
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_A_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_A
- Host: claude-code (Opus 5.5 subagent); nested spawning not available; SendMessage not exposed -> structured return is the final report

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code; probes only under verification/explorer_FU_A_r1_1/
- C1–C8; no participant IDs; no git writes; no installs into shared envs on DGX-Spark; never read ~/.claude/settings.json
- B300 GPU only via Slurm; at most 0.25 GPU-h smoke, ledgered under flock; never touch other teams' /scratch/iitp4 dirs
- Frozen r1 code (src/topic2_rgpool, scripts/topic2_*.py) read-only; r1 verdict stop stands
- Local python: PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; <=2 concurrent pytest, timeout 900

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: run docs (ORIGINAL_REQUEST, ACCEPTANCE+addendum, PI_DECISIONS 1-8, GATE_STATUS, RESUME); r1 card, result report, architecture, addenda 02/04/05; src/topic2_rgpool/{train,data,fixtures,metrics,stats,model,merge}.py; scripts/topic2_{verdict,train,launch_wave,preprocess_hcp}.py; M3_r2_gate_record (challenger_M3_r2_2 V01–V11 + case A)
- **Key findings**: see progress.md / handoff.md
- **Unexplored areas**: B300 data location under Slurm; per-run GPU-h; packing; synthetic fixture probes

## Key Decisions Made
- Do not read peer FU-A explorers' folders (independence)

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report
- /home/juke/git/00IITP-AI/verification/explorer_FU_A_r1_1/ — probes
