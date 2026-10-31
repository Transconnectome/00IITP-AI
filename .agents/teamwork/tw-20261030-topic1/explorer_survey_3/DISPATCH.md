## 2026-10-30T11:20:00Z (approx; dispatch received from workflow script / root coordinator — coordination event, not user text)

You are explorer_survey_3, a Teamwork Explorer (Survey step of the General/Project route) in run tw-20261030-topic1.

Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/explorer.md
Runtime adapters (read first; they override tool names): /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Your exclusive metadata directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/explorer_survey_3  (create it; write DISPATCH.md there FIRST containing this entire prompt verbatim, then BRIEFING.md, progress.md, report.md, handoff.md). Metadata only — no code/data there.
Executable probes (if any) only under: /home/juke/git/00IITP-AI/verification/explorer_survey_3/
Parent: root coordinator (virtual Project Orchestrator). Nested spawning is NOT available to you; if you need more work dispatched, write the request in handoff.md. SendMessage to parent is not available in this runtime: your final structured return value plus handoff.md is your report.

Read before anything else (do not summarize away): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/ORIGINAL_REQUEST.md, /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/sentinel/APPROVED_PROPOSAL.md, /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/sentinel/ACCEPTANCE.md.

Task (Survey): investigate the authoritative sources (repo /home/juke/git/00IITP-AI, read-only external repo /home/juke/git/enigma_ocd_mbbn and its data/, other local repos only if relevant) and enumerate ALL features, constraints and dependencies required to satisfy ACCEPTANCE.md A1–A6. Prioritize sources over prior knowledge. Emphasis for you: code & testing lens (existing src/mbbn_connectome_biomarker.py and tests, reusable pieces vs defects, performance of triad census at 304 nodes x many nulls, test design that fails on each targeted defect, ownership/layout, the existing MBBN baseline numbers and where they are recorded). Still report anything you find outside your emphasis. Verify facts empirically where cheap; mark anything unverified as unverified. Recommend strategies but do NOT implement production code.

Hard constraints: read-only everywhere except your metadata dir and /home/juke/git/00IITP-AI/verification/explorer_survey_3/. Do not modify any file under /home/juke/git/00IITP-AI/src, /home/juke/git/00IITP-AI/tests, /home/juke/git/00IITP-AI/docs, HANDOFF.md, 그랜트아이디어.md, 아이디어.txt, or any external repo. No GPU, no ssh/Slurm, no git commit/push, no network uploads. Never print participant IDs in your report (use counts or positional indices). Do not read ~/.claude/settings.json or any secrets file. You are not alone in the codebase. Preserve others' changes and adapt to them; do not revert unrelated work.

Return: report_path, handoff_path, feature_inventory (each with source file:line or command evidence), constraints, risks, dependency_order.
