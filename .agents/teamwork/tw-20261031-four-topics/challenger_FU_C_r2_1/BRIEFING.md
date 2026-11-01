# BRIEFING — 2026-11-01T21:08Z

## Mission
Empirically challenge worker_FU_C_r2 (FU-C iteration 2, C4 remediation) and the FU-C `stop` verdict; return CONFIRMED or REFUTED with evidence.

## 🔒 My Identity
- Archetype: challenger (roles: critic, specialist)
- Host: claude-code (Claude Opus 5.5), fresh non-fork agent; nested spawning not available
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_C_r2_1/
- Probe dir: /home/juke/git/00IITP-AI/verification/challenger_FU_C_r2_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_C (Topic 2 follow-up C), iteration r2
- Instance: 1 of 2 challengers (challenger_FU_C_r2_2 is the peer)

## 🔒 Key Constraints
- Review-only: never modify production files (src/, tests/, scripts/, results/, docs/)
- C1 protected hashes; all *_sha256.txt receipts; frozen cards never edited
- C4: never print/write participant IDs (HCP 6-digit, sub- labels, ENIGMA IDs); count-only checks
- No git writes; no installs; never read ~/.claude/settings.json; never copy sealed material into repo
- ≤2 concurrent pytest, timeout 900, nice, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2
- B300 GPU only via Slurm, ≤1 GPU-h, ledgered, squeue g3t-G-E0-* check first; connectome no find/du over /storage
- C8: never cite EMPIRICAL_ANALYSIS_REPORT.md / consolidated status numbers

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Review Scope
- Files: src/topic2_fu_c/, tests/topic2_fu_c/, scripts/topic2fu_c_*.py, results/topic2/2026-11-02_fu_c/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_*.md
- Contracts: card (fc2d0672…), ACCEPTANCE C1–C8 + F1–F3, PI decisions 1–8
- Criteria: verdict follows card; card frozen before results; C4 closed; receipts/supersession sound; tests catch mutants

## Claims under test (from worker_FU_C_r2 structured return)
- verdict stop, I1 −0.113 % [−0.499 %, +0.272 %], df 7; byte-identical reproduction via derived view
- exactly 5 receipt lines fail (code 13,16; output 141,162,164); output_sha256_r2 27/27 OK
- literal in 0 repo files; c4scan 0 hits; B300 membership 0 hits
- mutation union 146/149 killed; 52 r1-verifier survivors killed
- suites: fu_c 180, old 86, rgpool 116, lagmotif 88

## Key Decisions Made
- DISPATCH.md references embedded worker JSON instead of re-typing (precedent of worker_FU_C_r1/r2)

## Attack Surface
- Hypotheses tested: [TBD]
- Vulnerabilities found: [TBD]
- Untested angles: [TBD]

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md — Core: frozen card before results, synthetic ground truth, run records, verdict taxonomy (read in place; no local copy)

## Artifact Index
- DISPATCH.md, BRIEFING.md, progress.md, handoff.md (this folder)
