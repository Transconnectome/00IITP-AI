# BRIEFING — 2026-11-01T14:33Z

## Mission
FU_E (Topic 2 follow-up E): recommend a concrete, verifiable strategy for downstream value of the saved r1 Stage-1 encoders (frozen-encoder fingerprinting and/or age probe; cap 1.5 GPU-h). Lens: feasibility and failure modes.

## 🔒 My Identity
- Archetype: explorer (General route), explorer 2 of 3
- Roles: explorer
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_E_r1_2/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_E

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes only under /home/juke/git/00IITP-AI/verification/explorer_FU_E_r1_2/
- No git writes; no participant IDs printed/written; no installs into shared envs; no secrets reads
- B300 GPU only via Slurm; smoke test <= 0.25 GPU-h, ledgered under flock
- Never touch other teams' /scratch/iitp4 dirs; connectome: no find/du/grep -r/ls -R on /storage,/scratch
- C8: do not cite EMPIRICAL_ANALYSIS_REPORT.md / CONSOLIDATED_STATUS numbers

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: run docs; topic2 result report/card; frozen src/topic2_rgpool (train, model, merge, data, vendor encoder API); r1 wave jobs; B300 r1 dir, HCP staging, Slurm; local CPM unrestricted CSV; gate record V01-V11
- **Key findings**: 15 ckpts intact + anchor exact; REST1_LR only (no REST2); 28 labelled subjects (<=11 held-out); held-out pool 34; cost 0.004 s/window/model; strict=False drift; layer_0-2 are (B,L,C); anatomy confound; float boundary fixtures fragile
- **Unexplored areas**: real seed variance of identification accuracy; uncached I/O; full ConnectomeDB unrestricted CSV

## Key Decisions Made
- Primary = within-session split-half fingerprinting (gap) on 34 encoder-unseen subjects; J=acc diff, delta 0.01 abs; r1-mirrored rules
- Age/sex = untestable (labels); descriptive only
- Smoke via Slurm only (jobs 412 failed/420 ok), 0.010 GPU-h total

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final report (Hard)
- /home/juke/git/00IITP-AI/verification/explorer_FU_E_r1_2/{b300,cpu}/ — probes + outputs
