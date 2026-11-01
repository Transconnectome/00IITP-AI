# BRIEFING — 2026-11-01T14:40Z

## Mission
FU_C (Topic 2 follow-up C: 8 seeds x 3 arms, E36, 140k samples, df 7, cap 13 GPU-h): give the worker a concrete verifiable strategy; lens = adversarial pre-mortem. Recommend only, no production code.

## 🔒 My Identity
- Archetype: explorer (Teamwork, General route), explorer 3 of 3 for FU_C r1
- Roles: explorer (investigation + synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_C_r1_3/
- Probe dir (outside metadata): /home/juke/git/00IITP-AI/verification/explorer_FU_C_r1_3/ ; B300 /scratch/iitp4/explorer_FU_C_r1_3/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_C
- Host: claude-code; tools Bash/Read/Write/Edit; no nested spawning; final report = StructuredOutput

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- C1-C8; no participant IDs/tokens printed or written (counts/booleans only); no git writes; no installs on DGX-Spark
- Every B300 GPU use via Slurm (sbatch/srun), ledgered under flock; my smoke cap 0.25 GPU-h
- Never touch other FU teams' /scratch/iitp4 dirs; r1 dirs read-only
- No reading ~/.claude/settings.json or secrets; sealed material never copied into repo

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: run docs (ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME); topic2 card, result report, addenda 01-04; M3_r2_gate_record (challenger_M3_r2_2); scripts/topic2_verdict.py, stats.py, train.py, topic2_train.py, build_partitions, launch_wave, ledger, b300_env; B300 Slurm state
- **Key findings**: see progress.md / handoff.md
- **Unexplored areas**: TBD

## Key Decisions Made
- Probe with synthetic Fplus partial rerun + HCP h-token data-dir mapping/load check in one Slurm job (<=0.2 GPU-h)

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report
