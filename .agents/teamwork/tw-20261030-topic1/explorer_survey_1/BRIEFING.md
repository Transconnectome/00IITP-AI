# BRIEFING — 2026-10-30T11:13Z

## Mission
Survey (data & infrastructure lens): enumerate all features, constraints, dependencies needed for ACCEPTANCE A1–A6 of Topic 1 (ENIGMA-OCD directed lag motif, steps 1–4).

## 🔒 My Identity
- Archetype: explorer
- Roles: explorer (survey), synthesis
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/explorer_survey_1
- Original parent: root coordinator (virtual Project Orchestrator), run tw-20261030-topic1
- Milestone: Survey

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Writes only: this metadata dir; probes only in /home/juke/git/00IITP-AI/verification/explorer_survey_1/
- No edits in src/, tests/, docs/, HANDOFF.md, 그랜트아이디어.md, 아이디어.txt, external repos
- No GPU, no ssh/Slurm, no git commit/push, no network uploads
- Never print participant IDs; no secrets files

## Current Parent
- root coordinator; Updated: not yet

## Investigation State
- **Explored paths**: enigma data/ (npy, mmap, metadata), datasets.py, time_series_utils.py, post_hoc_analyses results, manuscript methods, 00IITP-AI src/mbbn_connectome_biomarker.py, tests, LOCAL_REPO_INTEGRATION_SPEC.md
- **Key findings**: see progress.md + structured return; probes in verification/explorer_survey_1
- **Unexplored areas**: ROI identity (no label table), FD (not on disk), report-vs-JSON not re-verified

## Key Decisions Made
- Probes run with /home/juke/superclaude-env/bin/python3, read-only mmap

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- report.md — survey report
- handoff.md — 5-component handoff
- report.md/handoff.md not written (harness refused report files); findings in structured return
