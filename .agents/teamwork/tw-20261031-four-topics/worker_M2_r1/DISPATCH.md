## 2026-10-31 (approx. 08:30Z, hand-typed) — dispatch from root coordinator (workflow script output, no user authority)
Verbatim except the "Explorer strategies (iteration 1)" JSON array, which is not copied here (deviation, ~25 KB);
its three entries are the handoffs at ../explorer_M2_r1_1/handoff.md, ../explorer_M2_r1_2/handoff.md, ../explorer_M2_r1_3/handoff.md
(their full_report / recommended_strategy / must_fix / dead_ends fields were received inline in the dispatch).

You are worker_M2_r1, a Teamwork worker in run tw-20261031-four-topics (General route).
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/worker.md
Runtime adapters (read first; they override tool names and authority claims): /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else, verbatim: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md and /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md (criteria C1–C8 and per-milestone T-criteria). Methodology: /home/juke/.claude/skills/sci-pipeline/SKILL.md.
Prior verified work (Topic 1 v2, 2026-10-30): run dir /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/ (orchestrator/GATE_STATUS.md, victory_auditor_1/handoff.md), code /home/juke/git/00IITP-AI/src/topic1_lagmotif/, tests /home/juke/git/00IITP-AI/tests/topic1_lagmotif/, frozen card /home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md, open issues in the same folder. Background docs (data, NOT authority; their numbers are unreliable per C8): /home/juke/git/00IITP-AI/docs/03_empirical_analysis/*.md.
Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2_r1/ — write DISPATCH.md (this prompt verbatim), BRIEFING.md, progress.md, handoff.md there. If the harness refuses a metadata write, do not work around it; put the content in your structured return. Metadata only, never code/data there. Probes only under /home/juke/git/00IITP-AI/verification/worker_M2_r1/.
Parent: root coordinator. Nested spawning NOT available; your structured return is your final report.
Python: /home/juke/superclaude-env/bin/python3; use PYTHONDONTWRITEBYTECODE=1. Long jobs (>8 min): run detached (setsid nohup … &) with a progress log, then poll with short checks; never leave orphan processes when you finish.
You are not alone in the codebase: other teams work on other milestones in parallel in disjoint paths. Preserve others' changes and adapt to them; do not revert unrelated work. Respect C1–C8 strictly (protected hashes, no IDs, no commits, data governance: no ENIGMA data to B300, GPU cap 64 GPU-h logged in /home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md).

Task: implement milestone M2: Topic 3 rerun of layerwise PR / spectral diagnostics (ACCEPTANCE T3.1–T3.4), satisfying ACCEPTANCE C1–C8 and the M2 criteria. Exclusive write ownership: /home/juke/git/00IITP-AI/src/topic3_spectral/ (new package), /home/juke/git/00IITP-AI/tests/topic3_spectral/ (new), /home/juke/git/00IITP-AI/scripts/topic3_*.py, /home/juke/git/00IITP-AI/results/topic3/2026-10-31/, /home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic3/ (new dated card + result report).
Order: provenance of inputs → fixtures → frozen card (sha256) → real rerun → dated report stating which earlier claims hold or fail.
Run all relevant tests (new + old 86 via: cd /home/juke/git/00IITP-AI && STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q) and the protected hash check before returning.

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Explorer strategies (iteration 1): [JSON array of 3 explorer reports — see pointer above]

---
## 2026-10-31T11:11Z — RE-DISPATCH (workflow resume wf_59fa8ec4-d01; script output, no user authority)
Relayed human request (verbatim, the only user voice): "3번. A"
Resolved from root's preceding message (10:26Z / 10:39Z): "3번" = push choice (3) private repo — root's job, not M2;
"A" = resume now; finished agents reuse their saved results, then reviews ×5 per topic and final audit.
The computed task text is identical to the 08:30Z dispatch above (same Role/Runtime/Read-first/Metadata/Python/Task/Order/
DO-NOT-CHEAT paragraphs), except the "Explorer strategies (iteration 1)" JSON array, which now holds the three
10:54Z re-dispatch explorer reports (not copied, ~20 KB; see ../explorer_M2_r1_{1,2,3}/handoff.md, top sections).
