# BRIEFING — 2026-11-01T01:20Z

## Mission
Implement M4 (Topic 4 redesign): T4.1 diagnosis+fixtures → T4.2 frozen card → T4.3 local-learning implementation, fixtures, CPU run, verdict per card.

## 🔒 My Identity
- Archetype: worker (roles: implementer, qa, specialist[sci-pipeline])
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M4_r1/
- Original parent: root coordinator (workflow B, run tw-20261031-four-topics)
- Milestone: M4 (Topic 4)

## 🔒 Key Constraints
- C1 protected hashes (old src/*.py, old tests, docs/03_empirical_analysis/*.md read-only).
- Write only: src/topic4_resu/, tests/topic4_resu/, scripts/topic4_*.py, results/topic4/2026-11-01/, docs/03_empirical_analysis/topic4/, verification/worker_M4_r1/ (probes), this metadata dir.
- No participant IDs printed/written (positions or salted hashes only). No git writes. No installs.
- ENIGMA data: CPU only on DGX-Spark (or connectome); never B300 (C6). 0 GPU-h planned.
- ≤4 local CPU procs, nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1. Long jobs detached with progress log.
- Card frozen (sha256) before any real-data result it governs (incl. tuning). Deviations → dated addendum.
- Do not cite old report numbers as results (C8).

## Current Parent
- Conversation ID: root coordinator; Updated: not yet

## Task Summary
- What to build: see DISPATCH.md; success = ACCEPTANCE T4.1–T4.3 + C1–C8.
- Code layout: orchestrator/PROJECT.md (topic4 → src/topic4_resu …)

## Key Decisions Made
- [TBD after engine probes + advisor]

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; no local copy needed — metadata only)
- Core methodology: 9 gates; frozen card before results; synthetic fixtures with known truth; run ledger; verdict taxonomy keep/modify/stop/inconclusive/no_candidate.

## Change Tracker
- Files modified: none yet
- Build status: n/a
- Pending issues: none

## Quality Status
- Build/test result: baseline C1 rc=0 at 01:13Z
- Tests added: none yet

## Artifact Index
- DISPATCH.md — assignment
