# BRIEFING — 2026-11-01T17:00Z

## Mission
Independent review (reviewer + critic) of milestone FU_A (Topic 2 follow-up A, 12 mm cell-mean target) against ACCEPTANCE C1–C8 and F1–F3; verdict APPROVE / REQUEST_CHANGES.

## 🔒 My Identity
- Archetype: reviewer
- Roles: reviewer, critic
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_FU_A_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_A
- Instance: reviewer_FU_A_r1_1 (1 of the FU_A r1 verifier set)
- host=claude-code; nested spawning not available; structured return = final report

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code, results, docs, ledger
- Probes only under /home/juke/git/00IITP-AI/verification/reviewer_FU_A_r1_1/
- No git writes; no installs on DGX-Spark; no participant IDs printed/written; never read settings.json / secrets / sealed dir
- ≤2 concurrent pytest, timeout 900, nice, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2
- B300 GPU only via Slurm, ≤1 GPU-h, ledgered, after g3t-G-E0 squeue check (not needed so far: read-only ssh only)

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Review Scope
- **Files to review**: src/topic2_fu_a/, tests/topic2_fu_a/, scripts/topic2fu_a_*.py, results/topic2/2026-11-02_fu_a/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_{card,result_report}.md, ledger rows
- **Interface contracts**: sentinel/ACCEPTANCE.md (C1–C8, F1–F3), PI_DECISIONS 1–8
- **Review criteria**: correctness, completeness, card-before-result, integrity, C4/C5

## Key Decisions Made
- No GPU probe needed: gate records verified via B300 sacct + sha256 (read-only ssh) and local recomputation.

## Artifact Index
- verification/reviewer_FU_A_r1_1/c1_check.txt — C1 67/67 OK rc 0
- verification/reviewer_FU_A_r1_1/{old_suite,fua_tests,topic1_tests,rgpool_tests}.txt — test logs
- verification/reviewer_FU_A_r1_1/verdict_recomputed.json — verdict rerun, identical to shipped
- verification/reviewer_FU_A_r1_1/mutation_worker_copy/ — worker verdict harness rerun
- verification/reviewer_FU_A_r1_1/mutation_extra/ — 16 extra mutants on target/sources/run/calib

## Review Checklist
- **Items reviewed**: card, report, src, verdict, run records, receipts, ledger, B300 sacct
- **Verdict**: pending
- **Unverified claims**: token scan on B300 (count-only, not rerun)

## Attack Surface
- **Hypotheses tested**: rebinding works in frozen loop (yes, module-global lookup); card before runs (git 16:05:25Z, run 16:12:33Z); fixture noise share claim (0.248 is pooled F+/F−; F+ alone ≈ 0.220)
- **Vulnerabilities found**: see handoff
- **Untested angles**: Stage 1 HCP path never exercised on GPU
