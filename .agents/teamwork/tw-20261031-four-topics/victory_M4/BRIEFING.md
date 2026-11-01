# BRIEFING — victory_M4

- Identity: victory_M4 (victory-auditor; roles critic/specialist/auditor/victory_verifier), run tw-20261031-four-topics, workflow B, General route.
- Host: claude-code 2.1.316; model claude-opus-5-5. Nested spawning not available; structured return = final report. SendMessage not used (parent reads structured return).
- Actual parent: root coordinator (workflow script).
- Ownership: metadata dir .agents/teamwork/tw-20261031-four-topics/victory_M4/ (md only); probes under verification/victory_M4/. No production edits.
- Immutable constraints: C1 protected hashes; C4 no participant IDs, no git writes, no installs on DGX-Spark, no secrets; C5 B300 via ledger only (this audit does not plan GPU use); C6 no ENIGMA on B300; ≤4 local CPU procs, nice, OMP_NUM_THREADS=2; no team handoff.md reads before verdict.
- Mission: verify claimed completion of M4 (Topic 4 FM-ReSU redesign; ACCEPTANCE T4.1–T4.3 + C1–C8) from raw artifacts; verdict VERIFIED_COMPLETE or REJECTED.
- Phase: started 03:18Z — orientation.

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (methodology reference named in dispatch). Local copy: none (read in place). Core methodology: 9 gates — estimand, stopping data contract, participant-level split/leakage, sealed confirm split, frozen card, synthetic ground-truth fixtures, run records, verdict taxonomy, state separation; independent review.

## Attack Surface
(filled as audit proceeds)
