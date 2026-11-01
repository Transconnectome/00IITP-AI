# BRIEFING — 2026-11-01T15:20Z

## Mission
FU-C (Topic 2 follow-up C): new dated frozen card + fail-closed verdict code + 8 fresh seeds x 3 arms (E, C, S) at r1 settings on B300 via Slurm, within 13 GPU-h; verdict per the new card; result report.

## 🔒 My Identity
- Archetype: worker (implementer + qa + specialist[sci-pipeline])
- Roles: implementer, qa, specialist
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_FU_C_r1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_C
- Host: claude-code; tools Bash/Read/Write/Edit; no nested spawning; final report = StructuredOutput

## 🔒 Key Constraints
- C1 protected hashes rc 0; all *_sha256.txt receipts must keep passing; frozen r1 card/code never edited.
- C4: no participant IDs (HCP 6-digit, r1 content-hash tokens) printed or written; repo carries h-tokens only.
- No git writes; no installs on DGX-Spark shared envs; never read ~/.claude/settings.json; sealed dir never copied to repo.
- Write ownership only: src/topic2_fu_c/, tests/topic2_fu_c/, scripts/topic2fu_c_*.py, results/topic2/2026-11-02_fu_c/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_*.md, B300 /scratch/iitp4/fu_c/, append-only ledger rows.
- Every B300 GPU use via sbatch/srun; before EVERY submit check squeue for g3t-G-E0-* (if pending/running: wait, poll >=5 min, record in progress.md). <=8 GPUs for whole Slurm user connectome.
- FU-C cap 13 GPU-h incl. explorer smokes (0.072+0.05+0.14=0.262). A job that would exceed the cap is not launched.
- Local python: /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; <=2 pytest procs, timeout 900.
- Card frozen (sha256 receipt in results/topic2/2026-11-02_fu_c/) BEFORE any FU-C real-data result.

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Task Summary
- What to build: card, src/topic2_fu_c (verdict + perms + C4 helpers), scripts/topic2fu_c_*.py (env, perms, slurm launch, collect/sanitize, verdict), tests, 24 runs, verdict, report.
- Success criteria: ACCEPTANCE C1–C8 + F1–F3.

## Key Decisions Made
- Fresh seeds 5..12 (not reuse of r1 0..4): explorers 1/3 power + determinism evidence.
- r1 F+/F- fixture gate reused by reference (12 run.json sha-verified) after an env anchor in own venv; rerun costs ~5.2 GPU-h (> cap).
- Positional data dir (hardlinks) + repo sanitized split.json (cc521b08…) → run.json carries h-tokens only.

## Artifact Index
- DISPATCH.md, BRIEFING.md, progress.md, handoff.md (this dir)

## Change Tracker
- Files modified: none yet
- Build status: n/a
- Pending issues: none

## Quality Status
- Build/test result: n/a
- Lint status: n/a
- Tests added/modified: none yet

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; not copied — metadata dir holds no copies)
- Core methodology: frozen card before results, synthetic ground truth fixtures, run records, verdict taxonomy, state separation.
