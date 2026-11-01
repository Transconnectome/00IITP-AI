# BRIEFING — reviewer_M4_r1_2

## Identity
- Archetype: reviewer (roles: reviewer, critic), role file /home/juke/git/chavis/skills/teamwork/references/roles/reviewer.md
- Host: claude-code (Claude Opus 5.5 subagent spawned by workflow script). Nested spawning not available. No SendMessage path used; structured return is the final report.
- Actual parent: root coordinator, run tw-20261031-four-topics, workflow B (M3+M4).
- Metadata dir (exclusive): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_M4_r1_2/
- Probe dir (exclusive): /home/juke/git/00IITP-AI/verification/reviewer_M4_r1_2/

## Immutable constraints
- Read-only on all production files (src/topic4_resu, tests/topic4_resu, scripts/topic4_*, results/topic4, docs topic4). Old src/*.py, old tests, protected files C1: read-only.
- No git writes of any kind. No installs. No participant IDs printed or written.
- Local CPU: nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1, <=4 processes. Reruns on copies only (receipts must not be overwritten).
- No B300 use planned (Topic 4 uses ENIGMA, C6 forbids B300). 0 GPU-h.

## Task
Independent review of M4 (T4.1–T4.3) against ACCEPTANCE C1–C8. Re-run tests and protected hash check. Verdict APPROVE only if every criterion is met with evidence; else REQUEST_CHANGES with blocking issues.

## Current phase
Started 2026-11-01T02:34Z. Phase: orientation/verification.
