# BRIEFING — 2026-11-01T14:20Z

## Mission
Recommend a concrete, verifiable strategy for FU_D (Topic 2 follow-up D: SwiFT ver11 E192 d2-2-18-2, 140k samples, arms E/C/S, 5 seeds, cap 25 GPU-h) — lens: scientific design & falsifiability (card, controls, kill criterion, permitted data).

## 🔒 My Identity
- Archetype: explorer (read-only investigation)
- Roles: explorer_FU_D_r1_1 (1 of 3)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_D_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e
- Milestone: FU_D

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes only under /home/juke/git/00IITP-AI/verification/explorer_FU_D_r1_1/
- C1–C8; no participant IDs; no git writes; no installs on DGX-Spark; never read ~/.claude/settings.json
- B300 GPU only via Slurm; ≤0.25 GPU-h ledgered smoke; ledger under flock
- src/topic2_rgpool read-only (code_sha256_at_freeze.txt); frozen r1 card never edited
- connectome: no find/du/grep -r/ls -R on /storage or /scratch

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: run docs (ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME); topic2 card, report, architecture, addenda 01-05; M3_r2 gate record (challenger_M3_r2_2)
- **Key findings**: r1 E36 0.43 GPU-h/run; §7 D estimate 1.36 h/run from explorer-measured 28.6 samples/s; 15 runs ≈ 20.4 GPU-h leaves ≈4.6 GPU-h for fixture gate + smoke — a full 12-run E192 fixture gate (≈16 GPU-h) does NOT fit.
- **Explored (cont.)**: src model/train/merge/stats, frozen verdict script, perms npz, VRABES E192 script, B300 Slurm + data (b300-01 only), ledger
- **Key findings (cont.)**: smoke job 404: 1.23 GPU-h/HCP run, 1.20/fixture run, peak 198 GiB; M0 at E192 = stage-0 16^3->8^3, Linear 1536->384, gather unchanged; frozen verdict script misfits FU_D (3 cases); positional symlink view feasible; n=3 too weak
- **Unexplored areas**: B300 .101/.103 (timeout); real-data stall risk

## Key Decisions Made
- F+ gate at E192 with 1 seed (3 runs) before Stage 1; pre-registered seed rule n=5 else 4 else not_run; conditional F- only if keep; new FU_D verdict script; positional symlink data view
- Smoke on synthetic tensors only (no real data before card freeze)

## Artifact Index
- DISPATCH.md — verbatim dispatch
- handoff.md — Hard handoff (5 sections)
- progress.md — heartbeat
- /home/juke/git/00IITP-AI/verification/explorer_FU_D_r1_1/ — probes + outputs
