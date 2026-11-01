# BRIEFING — 2026-11-01T17:38Z

## Mission
Empirically challenge FU-E (Topic 2 follow-up E, frozen-encoder within-run identifiability) worker_FU_E_r1 claims; return CONFIRMED / REFUTED.

## 🔒 My Identity
- Archetype: challenger (roles critic, specialist)
- Host: claude-code (Opus 5.5), subagent of workflow C; nested spawning not available
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_E_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e
- Milestone: FU_E
- Instance: 1 (challenger_FU_E_r1_1)

## 🔒 Key Constraints
- Review-only; do NOT modify production code/results/docs. Probes only under /home/juke/git/00IITP-AI/verification/challenger_FU_E_r1_1/
- C1–C8; no participant IDs; no git writes; no installs; never read ~/.claude/settings.json; sealed material never copied back
- B300 GPU only via Slurm, ≤1 GPU-h, ledger rows under flock, squeue g3t-G-E0-* check first
- PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice, ≤2 pytest, timeout 900

## Current Parent
- Conversation ID: root 5fddb83e; Updated: 2026-11-01T17:58Z (final: CONFIRMED, handoff.md written)

## Review Scope
- Files: src/topic2_fu_e/*, scripts/topic2fu_e_*.py, tests/topic2_fu_e/*, results/topic2/2026-11-02_fu_e/*, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_{card,result_report}.md
- Contracts: sentinel/ACCEPTANCE.md F1–F3, C1–C8; card §3–§8
- Criteria: verdict follows card; numbers reproducible; freeze-before-results; fixtures/tests catch defects

## Key Decisions Made
- Independent recompute w/o src imports (recompute/recompute.py, descriptives.py)
- GPU re-evaluation not planned unless CPU evidence leaves a gap

## Attack Surface
- Hypotheses tested: freeze-before-results (holds); numbers reproducible (exact, 1.4e-14); F+ failure robust to null choice (holds); verdict per card §8 (holds; overdetermined); mutants 52 (40 killed)
- Vulnerabilities found (nonblocking, no shipped-verdict effect): readout wiring untested (V08/V09), card constants unpinned (I05/V11/V12), F- mean bound (V05), G3 guards (V06/V07), G0 run.json perm leg + rel num tol (PV02/PV03), canonical subject-order guard absent, Idiff_E=0 order ambiguity
- Untested angles: GPU re-extraction (job 557 cancelled while PENDING, 0 GPU-h); extract script has no CPU test (read-reviewed)

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (methodology reference; frozen card before results, synthetic ground truth, verdict taxonomy). Not copied (read in place).

## Artifact Index
- verification/challenger_FU_E_r1_1/recompute/ — independent recompute (+ .out)
- verification/challenger_FU_E_r1_1/rerun/ — verdict script rerun
