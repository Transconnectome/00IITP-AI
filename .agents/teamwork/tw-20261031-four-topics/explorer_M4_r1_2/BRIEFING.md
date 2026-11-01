# BRIEFING — 2026-11-01T00:40Z

## Mission
M4 (Topic 4 FM-ReSU redesign): give the worker a concrete, verifiable strategy for T4.1–T4.3, with feasibility/failure-mode evidence from cheap probes. Recommend only; no production code.

## 🔒 My Identity
- Archetype: explorer (Teamwork)
- Roles: explorer 2 of 2 for M4, lens = feasibility and failure modes (code reality, compute/data logistics, fixtures that must fail on the targeted defect, budget)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M4_r1_2/
- Probe directory: /home/juke/git/00IITP-AI/verification/explorer_M4_r1_2/
- Original parent: root coordinator (workflow B, run tw-20261031-four-topics)
- Milestone: M4 Topic 4

## 🔒 Key Constraints
- Read-only investigation; do NOT implement production code. Probes only under verification/explorer_M4_r1_2/.
- C1 protected hashes; C4 no participant IDs printed/written, no git writes, no installs on DGX-Spark; C6 no ENIGMA data or derivatives on B300 (and do not touch ~/enigma_ocd/data there); C7 external repos read-only; C8 old report numbers not citable.
- Local CPU: /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice, ≤4 procs. ≤5 real subjects read-only.
- B300: read-only checks; ≤0.25 GPU-h smoke only if useful, ledger under flock. M4 data are ENIGMA → M4 runs NOT on B300.
- Work independently of explorer_M4_r1_1.

## Current Parent
- Root coordinator; updated: not yet

## Investigation State
- **Explored paths**: ORIGINAL_REQUEST, ACCEPTANCE, RESUME, survey_2/3 handoffs (M4 sections), PROJECT.md layout, sci-pipeline SKILL
- **Key findings**: see progress.md / handoff.md
- **Unexplored areas**: src/fractal_motif_resu.py, src/local_learning_engine.py, data loaders, cohort TR/valid_T distribution, old tests' AST audit, connectome env

## Key Decisions Made
- M4 compute = local CPU / connectome only (ENIGMA, C6).

## Artifact Index
- DISPATCH.md — dispatch verbatim
- progress.md — heartbeat
- handoff.md — final 5-component report
