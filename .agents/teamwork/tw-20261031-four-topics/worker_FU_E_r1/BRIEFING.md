# BRIEFING — 2026-11-01T15:25Z (worker_FU_E_r1)

## Mission
FU-E (Topic 2 follow-up E): downstream value of the saved r1 Stage-1 encoders — frozen-encoder within-run split-half identifiability ("fingerprinting"); age/sex probe judged untestable. New dated card frozen before any real-data result; B300 via Slurm; cap 1.5 GPU-h.

## 🔒 My Identity
- Archetype: teamwork worker (General route), roles implementer + qa + specialist (sci-pipeline)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_FU_E_r1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_E
- Host: claude-code (Opus 5.5 subagent); no nested spawning; final report = StructuredOutput return

## 🔒 Key Constraints
- C1 protected hashes rc 0; all *_sha256.txt receipts; frozen cards never edited (addenda only)
- No participant IDs/pseudonyms printed or written (positional index only); HCP never leaves B300 except aggregates
- No git writes; no installs into shared envs; never read ~/.claude/settings.json / secrets; sealed dir never copied
- Every B300 GPU use via sbatch/srun; squeue check for g3t-G-E0-* before each submission (wait if pending/running)
- Ledger rows (start + close) under flock; FU-E cap 1.5 GPU-h
- Write ownership: src/topic2_fu_e/, tests/topic2_fu_e/, scripts/topic2fu_e_*.py, results/topic2/2026-11-02_fu_e/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_*.md, B300 /scratch/iitp4/fu_e/, ledger rows
- Local python: /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice; ≤2 pytest, timeout 900

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Task Summary
- What to build: card (frozen) → package src/topic2_fu_e (features, preprocessing, Idiff, gates, verdict) → tests (fixtures + verdict mutants) → B300 job → result report
- Success criteria: ACCEPTANCE F1–F3, C1–C8
- Code layout: new paths only; r1 code imported read-only

## Key Decisions Made
- (see handoff/card) primary = within-run split-half Idiff of cov2 readout of final encoder layer, held-out 24 subjects, common mask + per-half re-z-score; J1/J2 relative contrasts, δ=0.01; age/sex probe not run

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md — gates G1–G9: frozen card before results, synthetic fixtures (planted/null), run records, verdict taxonomy, software failure ≠ null. Read in place (not copied).

## Change Tracker
- Files modified: none yet
- Build status: n/a
- Pending issues: B300 ssh flaky (retry helper verification/worker_FU_E_r1/b300ssh.sh)

## Artifact Index
- DISPATCH.md, progress.md, handoff.md (this dir)
