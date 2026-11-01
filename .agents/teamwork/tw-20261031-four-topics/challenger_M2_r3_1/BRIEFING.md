# BRIEFING — 2026-11-01T06:30Z

## Mission
Empirically challenge M2 (Topic 3) iteration 3: try to break the r3 guard tests with my own verdict-path and producer-path mutants in copied trees; recompute headline/addendum numbers from saved raw outputs; check card-before-results and card-rule verdicts; check addenda 03–05. Return CONFIRMED or REFUTED with evidence.

## 🔒 My Identity
- Archetype: challenger (roles: critic, specialist)
- Host: claude-code (Opus 5.5 subagent spawned by workflow script); nested spawning not available
- Working directory (metadata): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_M2_r3_1/
- Probe/copied-tree directory: /home/juke/git/00IITP-AI/verification/challenger_M2_r3_1/
- Original parent: root coordinator (workflow harness; native ID not exposed to me)
- Milestone: M2 Topic 3, iteration 3 gate
- Instance: challenger 1 of the r3 5-verifier gate

## 🔒 Key Constraints
- Review-only: never edit production files (src/, scripts/, tests/, docs/, results/ pinned files).
- No git writes of any kind; 0 GPU; no participant IDs printed or written.
- Python /home/juke/superclaude-env/bin/python3 with PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice.
- ≤2 concurrent pytest, each under `timeout 900`; timeout/OOM = INVALID (rerun), never a kill.
- Never run scripts/topic3_*.py in the production tree (topic3_common.py:12 hardcodes OUT); only in copied trees.
- Metadata dir: metadata only. Code/data/copied trees only under verification/challenger_M2_r3_1/.
- A survivor refutes only if reachable on inputs the card's procedure can produce AND can change a verdict or reported number.

## Current Parent
- Root coordinator; updated: not yet

## Review Scope
- Files: src/topic3_spectral/*, scripts/topic3_*.py, tests/topic3_spectral/* (incl. new test_verdict_rules_r3.py, test_token_stats_wiring_r3.py), results/topic3/2026-10-31/*, docs/03_empirical_analysis/topic3/* (card, provenance, report, addenda 01–05)
- Criteria: ACCEPTANCE C1–C8, T3.1–T3.4; r2b gate blocking classes; card §4/§5 rules

## Key Decisions Made
- Build my own byte-copied tree; run control suite; write new mutants not in worker's 151-patch union.
- Priority targets: Family A reported numbers (no real-data regression test seen), token-level producer of primary inputs (cat_corrpr L3, cat_covpr L2), Holm variants.

## Attack Surface
- Hypotheses tested:
  - r2b blocking classes closed: yes. 5 union jobs reproduced; U127 is equivalent.
  - Family B headline: recomputed exactly.
  - Addendum 05 corrections: verified.
  - Card frozen before results: yes (git 24fe976 at 08:46:25Z).
  - Verdicts follow the card's rules: yes.
- Vulnerabilities found (2026-11-01T06:56Z):
  - (i) Token-job producer: `cat_corrpr__L3` and `cat_covpr__L2` are untested. T02 flips H1b to "holds"; T01 reverses H1a.
  - (ii) Family A reported numbers have no real-data regression: A01, A02, A05, A07 and A08 move printed numbers.
  - Both survive all 121 tests. No real verdict is affected.
- Untested angles:
  - full 151-patch union rerun (only 5 reproduced);
  - connectome rerun (a counterfactual was used instead).

## Status
- Verdict: REFUTED. handoff.md is final.

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; not copied — metadata dir holds metadata only)
- Core methodology: frozen card before results, synthetic ground-truth fixtures, run records, verdict taxonomy, independent review.

## Artifact Index
- DISPATCH.md — dispatch record
- progress.md — heartbeat
- handoff.md — final 5-component report
