# BRIEFING — 2026-11-01T14:30Z

## Mission
FU_C (Topic 2 follow-up C: 8 seeds x 3 arms at E36, 140k samples, df-7 t interval; cap 13 GPU-h): give the worker a concrete, verifiable strategy (card, controls, kill criterion, permitted data), with evidence from cheap probes. Explorer 1 of 3, lens = scientific design and falsifiability. Recommend only.

## 🔒 My Identity
- Archetype: Teamwork explorer (General route), host=claude-code (Claude Code subagent; Agent/SendMessage not exposed to me; nested spawning not available)
- Roles: explorer (read-only investigation + synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_C_r1_1/
- Probe directory: /home/juke/git/00IITP-AI/verification/explorer_FU_C_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_C (Topic 2 follow-up C)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code; probes only under verification/explorer_FU_C_r1_1/
- C1 protected hashes; all *_sha256.txt receipts stay valid; frozen r1 card/code never edited
- C4: no participant IDs / HCP tokens printed or written; no git writes; no installs on DGX-Spark; never read settings.json/secrets; sealed material never copied into repo
- B300 GPU only via Slurm sbatch/srun; ledger rows under flock; my smoke cap 0.25 GPU-h; FU-C cap 13 GPU-h
- connectome: no find/du/grep -r/ls -R over /storage or /scratch
- Local python: /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; <=2 pytest procs
- C8: never cite EMPIRICAL_ANALYSIS_REPORT.md / CONSOLIDATED_STATUS numbers

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: run docs (request, acceptance, PI decisions, gate status, resume); r1 card, result report, addenda 01-05; scripts/topic2_verdict.py, src/topic2_rgpool/stats.py, data.py, train.py (grep), build_partitions.py; r1 run.json timings; ledger tail; M3_r2_gate_record (challenger_M3_r2_2 V01-V11)
- **Key findings**: see handoff.md
- **Unexplored areas**: B300 live state (ssh banner timeout at 14:2xZ, retrying)

## Key Decisions Made
- [TBD]

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-section report
