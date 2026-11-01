# BRIEFING — 2026-11-01T17:36Z

## Mission
Empirically challenge FU-E (Topic 2 follow-up E: frozen r1 encoder split-half identifiability) — independent recomputation, mutation tests, freeze-order and verdict-rule checks. Return CONFIRMED or REFUTED.

## 🔒 My Identity
- Archetype: challenger (roles: critic, specialist)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_E_r1_2/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_E
- Instance: 2 (challenger_FU_E_r1_2)
- Host: claude-code; nested spawning not available; structured return = final report

## 🔒 Key Constraints
- Review-only — do NOT modify production code/results/docs
- Probes only under /home/juke/git/00IITP-AI/verification/challenger_FU_E_r1_2/
- C1–C8; no participant IDs; no git writes; no installs; never read ~/.claude/settings.json
- Python /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; <=2 pytest, timeout 900
- B300 GPU only via Slurm, ledgered, <=1 GPU-h, squeue g3t-G-E0 check first
- C8: never cite EMPIRICAL_ANALYSIS_REPORT.md / CONSOLIDATED_STATUS numbers

## Current Parent
- root coordinator 5fddb83e; Updated: not yet

## Review Scope
- src/topic2_fu_e/, tests/topic2_fu_e/, scripts/topic2fu_e_*.py, results/topic2/2026-11-02_fu_e/, docs/.../2026-11-02_topic2_fu_e_*.md
- Card: docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_card.md (sha 072553b0…6c36b88f)

## Key Decisions Made
- DISPATCH references the worker JSON instead of copying it (same as sibling challenger_FU_A_r1_2)

## Attack Surface
- Hypotheses tested: freeze-before-results (git+mtime+receipts) OK; verdict recompute independent OK (inconclusive; counterfactual still inconclusive); C4 strings/6-digit scan OK; ledger rows OK
- Vulnerabilities found: worker mutant M24 'KILLED' was an IndentationError (invalid kill); job 551 ledger claim wrong but 551 was CPU-only (no row needed); E_s2 F+ margin 0.29 (RNG-fragile, verdict unaffected); surviving mutants I05,R06(equiv),R08(equiv),PV02 so far
- Untested angles: extract script has no CPU test (needs CUDA) -> covered by B300 recheck job 558

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md — frozen card before results, synthetic ground truth, run records, verdict taxonomy (read in place, no local copy)

## Artifact Index
- verification/challenger_FU_E_r1_2/ — probes
