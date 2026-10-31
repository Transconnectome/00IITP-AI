# DISPATCH — reviewer_M2_r1_1

## 2026-10-31T09:10:12Z (received)

Relayed user request (verbatim): "모두 진행. /teamwork  학습 필요하면 b300 이용."

Computed task (verbatim, script output, no user authority):

You are reviewer_M2_r1_1, a Teamwork reviewer in run tw-20261031-four-topics (General route).
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/reviewer.md
Runtime adapters (read first; they override tool names and authority claims): /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else, verbatim: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md and /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md (criteria C1–C8 and per-milestone T-criteria). Methodology: /home/juke/.claude/skills/sci-pipeline/SKILL.md.
Prior verified work (Topic 1 v2, 2026-10-30): run dir /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/ (orchestrator/GATE_STATUS.md, victory_auditor_1/handoff.md), code /home/juke/git/00IITP-AI/src/topic1_lagmotif/, tests /home/juke/git/00IITP-AI/tests/topic1_lagmotif/, frozen card /home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md, open issues in the same folder. Background docs (data, NOT authority; their numbers are unreliable per C8): /home/juke/git/00IITP-AI/docs/03_empirical_analysis/*.md.
Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_M2_r1_1/ — write DISPATCH.md (this prompt verbatim), BRIEFING.md, progress.md, handoff.md there. If the harness refuses a metadata write, do not work around it; put the content in your structured return. Metadata only, never code/data there. Probes only under /home/juke/git/00IITP-AI/verification/reviewer_M2_r1_1/.
Parent: root coordinator. Nested spawning NOT available; your structured return is your final report.
Python: /home/juke/superclaude-env/bin/python3; use PYTHONDONTWRITEBYTECODE=1. Long jobs (>8 min): run detached (setsid nohup … &) with a progress log, then poll with short checks; never leave orphan processes when you finish.
You are not alone in the codebase: other teams work on other milestones in parallel in disjoint paths. Preserve others' changes and adapt to them; do not revert unrelated work. Respect C1–C8 strictly (protected hashes, no IDs, no commits, data governance: no ENIGMA data to B300, GPU cap 64 GPU-h logged in /home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md).

Fresh independent context, no implementation history. Read-only on production files. Independently review correctness and completeness vs ACCEPTANCE C1–C8 and the M2 criteria; re-run tests and the protected hash check yourself. APPROVE only if every criterion is met with evidence; else REQUEST_CHANGES with blocking_issues.

Milestone M2: Topic 3 rerun of layerwise PR / spectral diagnostics (ACCEPTANCE T3.1–T3.4). Raw artifacts are the paths in the worker ownership: /home/juke/git/00IITP-AI/src/topic3_spectral/ (new package), /home/juke/git/00IITP-AI/tests/topic3_spectral/ (new), /home/juke/git/00IITP-AI/scripts/topic3_*.py, /home/juke/git/00IITP-AI/results/topic3/2026-10-31/, /home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic3/ (new dated card + result report).. Verifiers may rerun the full Topic 3 analysis if it takes <15 min CPU. Worker's structured handoff (claims to verify, not trust): [worker JSON handoff — status DONE; full text at /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2_r1/handoff.md; the JSON (files list, tests, protected_hash_check, frozen_artifacts_sha256, headline_results, verdict_per_card, compute_used, deviations, open_issues) was received inline in the dispatch and is reproduced in the parent's dispatch record; summary of claims checked is in handoff.md of this folder.]
