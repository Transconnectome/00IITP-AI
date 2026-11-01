# BRIEFING — 2026-11-01T16:48Z

## Mission
Empirically challenge worker_FU_A_r1's FU-A deliverable (Topic 2 follow-up A, lower-noise 12 mm cell-mean target); CONFIRMED or REFUTED with evidence.

## 🔒 My Identity
- Archetype: challenger (critic, specialist)
- Roles: critic, specialist
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_A_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_A
- Instance: 1 of [TBD]
- Host: claude-code; nested spawning not available

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code / production files
- Probes only under /home/juke/git/00IITP-AI/verification/challenger_FU_A_r1_1/
- C1–C8; no participant IDs; no git writes; no installs on DGX-Spark; never read settings.json/secrets
- PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; ≤2 concurrent pytest, timeout 900
- B300 GPU only via Slurm, check squeue for g3t-G-E0-* first, ≤1 GPU-h, ledger rows under flock

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Review Scope
- Files: src/topic2_fu_a/, tests/topic2_fu_a/, scripts/topic2fu_a_*.py, results/topic2/2026-11-02_fu_a/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_*.md
- Criteria: ACCEPTANCE F1–F3, C1–C8; card rules

## Key Decisions Made
- No GPU rerun (B300 queue saturated; no checkpoints); 0 GPU-h used
- Verdict: CONFIRMED (handoff.md)

## Attack Surface
- Hypotheses tested: freeze-before-results; record genuineness; verdict-vs-card (oracle 60k cases); target code; fixture calib; mutants X01-X22
- Vulnerabilities found: N1 F+ noise share 0.220 not 0.248 (card/report text); N2 seed-noise overstatement; N3 5 surviving mutants (non-shipped paths)
- Untested angles: GPU rerun; HCP TRAIN design stats recompute

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place, not copied)
- Core methodology: frozen card before results, synthetic ground truth, run records, verdict taxonomy

## Artifact Index
- DISPATCH.md, progress.md, handoff.md (this folder)
