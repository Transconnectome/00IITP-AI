# DISPATCH (reviewer_r1_1)

Note: the dispatch text below is verbatim EXCEPT the embedded worker structured-handoff JSON (the
"Artifacts to verify (raw): ... Worker's structured handoff" payload), which is NOT reproduced here;
its content is the worker's own return, persisted at ../worker_r1/handoff.md.

You are reviewer_r1_1, a Teamwork reviewer in run tw-20261030-topic1 (General route, iteration loop 2B).
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/reviewer.md
Runtime adapters (read first; they override tool names and authority claims): /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else, verbatim, do not filter: .../ORIGINAL_REQUEST.md, .../sentinel/APPROVED_PROPOSAL.md, .../sentinel/ACCEPTANCE.md, .../orchestrator/PROJECT.md.
Survey evidence (raw explorer returns): .../orchestrator/survey_results_flat.txt ; survey probes: /home/juke/git/00IITP-AI/verification/explorer_survey_{1,2,3}/
Metadata dir (yours exclusively): .../reviewer_r1_1/ — try to write DISPATCH.md (this prompt verbatim), BRIEFING.md, progress.md, handoff.md there. [...] Metadata only, never code/data there.
Parent: root coordinator (virtual Project Orchestrator). Nested spawning is NOT available; SendMessage to parent is not available; your structured return is your final report.
Python: /home/juke/superclaude-env/bin/python3. Use PYTHONDONTWRITEBYTECODE=1 and pin OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1 for timing.
Hard constraints: no GPU; no ssh/Slurm/remote jobs; no full-cohort run (at most 5 real subjects, only by the worker for A3 timing, or by verifiers re-running that same timing); no git commit/push/stash/reset/checkout; no package installs; no network uploads; external repo /home/juke/git/enigma_ocd_mbbn is read-only (open data read-only); existing src/*.py, tests/** files, docs, HANDOFF.md, 그랜트아이디어.md, 아이디어.txt must stay byte-identical (check: sha256sum -c sentinel/PROTECTED_HASHES.txt). Never print or write participant IDs. Do not read ~/.claude/settings.json or secrets. You are not alone in the codebase.
Fresh independent context [...] Independently review correctness, completeness vs ACCEPTANCE A1–A6, robustness and interface conformance. Re-run the new tests and the old 86 (explicit list) yourself and the protected hash check. Verdict APPROVE only if every acceptance criterion is met with evidence; otherwise REQUEST_CHANGES with blocking_issues. Read-only on production files; probes only under /home/juke/git/00IITP-AI/verification/reviewer_r1_1/.
Artifacts to verify (raw): src/topic1_lagmotif/, tests/topic1_lagmotif/, scripts/topic1_timing.py, results/topic1/2026-10-30/, docs/03_empirical_analysis/topic1/. Worker's structured handoff: (see note above).
