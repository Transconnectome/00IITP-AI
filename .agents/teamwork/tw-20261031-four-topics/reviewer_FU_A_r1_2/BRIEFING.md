# BRIEFING — 2026-11-01T16:48Z

## Mission
Independent review (reviewer + critic) of milestone FU_A (Topic 2 follow-up A: 12 mm cell-mean target) vs ACCEPTANCE C1–C8 and F1–F3; verdict APPROVE / REQUEST_CHANGES.

## 🔒 My Identity
- Archetype: reviewer (roles reviewer, critic)
- Host: claude-code 2.1.316; tools exposed: Bash/Read/Write/Edit; no Agent spawning (nested spawning not available)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_FU_A_r1_2/
- Probe dir: /home/juke/git/00IITP-AI/verification/reviewer_FU_A_r1_2/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_A
- Instance: reviewer 2 of FU_A r1 gate (r1_2)

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code, results, cards, ledger rows
- C1 protected hashes; all *_sha256.txt receipts; frozen cards never edited
- C4: no participant IDs printed/written; no git writes; no installs on DGX-Spark; never read ~/.claude/settings.json/secrets
- Sealed material never copied into repo; HCP never redistributed
- pytest ≤2 concurrent, timeout 900, PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice
- B300 GPU only via Slurm, ≤1 GPU-h, ledgered, squeue g3t-G-E0-* check before submission
- connectome: never find/du/grep -r/ls -R on /storage or /scratch

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Review Scope
- Files: src/topic2_fu_a/, tests/topic2_fu_a/, scripts/topic2fu_a_*.py, results/topic2/2026-11-02_fu_a/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_*.md, ledger rows
- Contracts: sentinel/ACCEPTANCE.md (C1–C8, F1–F3), PI_DECISIONS 1–8
- Criteria: correctness, completeness, card-before-result, verdict rule, compute, C4

## Key Decisions Made
- [TBD]

## Review Checklist
- Items reviewed: [pending]
- Verdict: pending
- Unverified claims: all worker claims

## Attack Surface
- Hypotheses tested: [pending]
- Vulnerabilities found: [pending]
- Untested angles: [pending]

## Artifact Index
- DISPATCH.md — dispatch record
