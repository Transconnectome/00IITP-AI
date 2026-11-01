# BRIEFING — 2026-11-01T02:40Z

## Mission
Empirically challenge worker_M4_r1's Topic 4 (M4) delivery (ACCEPTANCE T4.1–T4.3): break it with independent recomputation, adversarial inputs and mutants; CONFIRMED or REFUTED with evidence.

## 🔒 My Identity
- Archetype: challenger (roles: critic, specialist)
- Host: claude-code; model Opus 5.5; nested spawning NOT available; no SendMessage to parent required (structured return is the final report)
- Working directory (metadata): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_M4_r1_1/
- Probe directory (code/data probes): /home/juke/git/00IITP-AI/verification/challenger_M4_r1_1/
- Original parent: root coordinator (run tw-20261031-four-topics, workflow B)
- Milestone: M4 (Topic 4 redesign)
- Instance: 1 of 1 (challenger_M4_r1_1)

## 🔒 Key Constraints
- Review-only: do NOT modify production code/results/docs (src/topic4_resu, tests/topic4_resu, scripts/topic4_*, results/topic4, docs/.../topic4).
- C1 protected hashes; C4 no participant IDs printed/written, no git writes, no installs; C6 ENIGMA data stays on DGX-Spark (never B300).
- Local CPU: nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1, <=4 processes; rerun budget <20 min CPU.
- Temp/cache: own subfolder of session scratchpad; delete ENIGMA-derived caches when done; no orphan processes.
- Never rerun worker harnesses in place (they overwrite receipts); use copies under my probe dir.

## Current Parent
- Root coordinator; updated: not yet

## Review Scope
- Files: src/topic4_resu/**, tests/topic4_resu/**, scripts/topic4_*.py, results/topic4/2026-11-01/**, docs/03_empirical_analysis/topic4/**
- Contracts: sentinel/ACCEPTANCE.md T4.1–T4.3, frozen card 2b535c39…5934
- Criteria: correctness, card conformance, freeze-before-results, fixture strength, verdict per rules

## Key Decisions Made
- Freeze chronology checked from ledger + file birth times (git has no pre-result commit of these files).

## Attack Surface
- Hypotheses tested: (filled in progress.md / handoff.md)
- Vulnerabilities found: TBD
- Untested angles: TBD

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; no local dump needed — read-only reference)
- Core methodology: 9 gates (G1–G9); frozen card before results; synthetic fixtures; run ledger; verdict taxonomy; author never passes own gate.

## Artifact Index
- DISPATCH.md — dispatch (verbatim except condensed worker JSON)
- progress.md — heartbeat
- handoff.md — final 5-component report
