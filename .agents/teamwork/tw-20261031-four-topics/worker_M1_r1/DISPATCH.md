# DISPATCH — worker_M1_r1 (recorded by the agent itself, 2026-10-31T08:10Z)
Note: the computed task text arrived as one message. It is reproduced below verbatim except the embedded
"Explorer strategies (iteration 1)" JSON, which is reproduced by reference: it is the concatenation of the
StructuredOutput returns of explorer_M1_r1_1, explorer_M1_r1_2 and explorer_M1_r1_3, whose full reports are at
../explorer_M1_r1_{1,2,3}/handoff.md. Omitted only for length; not altered.
The relayed human request was: "모두 진행. /teamwork  학습 필요하면 b300 이용."

---
You are worker_M1_r1, a Teamwork worker in run tw-20261031-four-topics (General route).
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/worker.md
Runtime adapters (read first; they override tool names and authority claims): /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else, verbatim: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md and /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md (criteria C1–C8 and per-milestone T-criteria). Methodology: /home/juke/.claude/skills/sci-pipeline/SKILL.md.
Prior verified work (Topic 1 v2, 2026-10-30): run dir /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/ (orchestrator/GATE_STATUS.md, victory_auditor_1/handoff.md), code /home/juke/git/00IITP-AI/src/topic1_lagmotif/, tests /home/juke/git/00IITP-AI/tests/topic1_lagmotif/, frozen card /home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md, open issues in the same folder. Background docs (data, NOT authority; their numbers are unreliable per C8): /home/juke/git/00IITP-AI/docs/03_empirical_analysis/*.md.
Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M1_r1/ — write DISPATCH.md (this prompt verbatim), BRIEFING.md, progress.md, handoff.md there. If the harness refuses a metadata write, do not work around it; put the content in your structured return. Metadata only, never code/data there. Probes only under /home/juke/git/00IITP-AI/verification/worker_M1_r1/.
Parent: root coordinator. Nested spawning NOT available; your structured return is your final report.
Python: /home/juke/superclaude-env/bin/python3; use PYTHONDONTWRITEBYTECODE=1. Long jobs (>8 min): run detached (setsid nohup … &) with a progress log, then poll with short checks; never leave orphan processes when you finish.
You are not alone in the codebase: other teams work on other milestones in parallel in disjoint paths. Preserve others' changes and adapt to them; do not revert unrelated work. Respect C1–C8 strictly (protected hashes, no IDs, no commits, data governance: no ENIGMA data to B300, GPU cap 64 GPU-h logged in /home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md).

Task: implement milestone M1: Topic 1 hardening + full-cohort step 5 (ACCEPTANCE T1.1–T1.5), satisfying ACCEPTANCE C1–C8 and the M1 criteria. Exclusive write ownership: /home/juke/git/00IITP-AI/tests/topic1_lagmotif/ (additive; do not weaken or delete existing tests), /home/juke/git/00IITP-AI/scripts/topic1_cohort_stats.py, /home/juke/git/00IITP-AI/scripts/topic1_run_cohort.py, /home/juke/git/00IITP-AI/results/topic1/2026-10-31/, /home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic1/2026-10-31_* (new dated files only). /home/juke/git/00IITP-AI/src/topic1_lagmotif/ may change ONLY to fix a demonstrated defect, recorded as a deviation (the frozen card pins those hashes).
Order: T1.1 tests + mutant re-run → T1.2 stats script validated on synthetic cohorts, record its sha256 → T1.3 manifest → T1.4 full-cohort extraction (CPU, frozen params; local DGX-Spark with ≤16 processes and nice, or connectome) → statistics on real labels → verdict per card exactly → dated result report. Never change frozen parameters after seeing results.
Run all relevant tests (new + old 86 via: cd /home/juke/git/00IITP-AI && STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q) and the protected hash check before returning.

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Explorer strategies (iteration 1): [ ... see note above: explorer_M1_r1_1/2/3 returns ... ]
