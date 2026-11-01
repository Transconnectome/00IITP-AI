# BRIEFING — 2026-11-01T15:30Z (worker_FU_A_r1)

## Mission
Topic 2 follow-up A (FU-A): new dated frozen card + implementation + fixtures + B300 Slurm runs + verdict + result report for
"do connectome boxes beat cubes at M0 when the SimMIM target is the 12 mm cell-mean field (not noise-dominated)?"

## 🔒 My Identity
- Archetype: worker (Teamwork General route), roles implementer + qa + specialist (sci-pipeline methodology)
- Host: claude-code (Opus 5.5); no nested spawning; structured return = final report
- Working directory (metadata only): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_FU_A_r1/
- Probe dir: /home/juke/git/00IITP-AI/verification/worker_FU_A_r1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_A (ACCEPTANCE addendum F1–F3)

## 🔒 Key Constraints
- Write only: src/topic2_fu_a/, tests/topic2_fu_a/, scripts/topic2fu_a_*.py, results/topic2/2026-11-02_fu_a/,
  docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_*.md, B300 /scratch/iitp4/fu_a/, append-only ledger rows.
- r1 code/docs/results read-only (src/topic2_rgpool pinned by code_sha256_at_freeze.txt). Import, never edit.
- Card frozen (sha256 receipt in results dir) BEFORE any real-data FU-A result. Deviations only in dated addenda.
- C4: no participant IDs / unsalted content-hash tokens in any output; positional hNN only; never print B300 dir names.
- No git writes. No installs on DGX-Spark. Never read ~/.claude/settings.json / secrets. Sealed material stays off-repo.
- B300 GPU only via sbatch/srun; before EVERY submission squeue check for g3t-G-E0-* (if PENDING/RUNNING: wait ≥5 min, log).
- ≤8 concurrent GPUs for the whole Slurm user connectome. FU-A cap 8 GPU-h (incl. explorer smokes, counted conservatively).
- Local python: PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; ≤2 concurrent pytest, timeout 900.

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Task Summary
- What to build: FU-A card, src/topic2_fu_a (cell-mean sources reusing frozen train.run, verdict), tests, scripts, runs, report.
- Success criteria: ACCEPTANCE C1–C8, F1–F3; old 86 tests + new tests pass; C1 rc 0; receipts OK.

## Key Decisions Made
- Target: y = kappa * broadcast(cell means of r1 per-voxel z-scored BOLD) on the subject brain mask; input = target.
  kappa = one global constant from TRAIN (no per-cell z-scoring) -> FU-A NMSE = r1 NMSE of the block-mean projection.
- Reuse frozen train.run by rebinding its two source classes (context manager, restored after); loop is r1's own code.
- Fixture voxel noise sigma_v calibrated by matching the iid-voxel-noise energy share of the cell-mean target (NF) to TRAIN.
- Gate under the 8 GPU-h cap: F+ arms E,C seed 0 at full budget (2 runs); F- and F+ S not run (budget) -> keep/modify
  can only become inconclusive (pending gates). 17 runs total ≈ 7.7 GPU-h.

## Artifact Index
- verification/worker_FU_A_r1/b3.sh, b3cp.sh, sync_code.sh — B300 ssh/scp/sync helpers (private ssh master /tmp/fua_b3_cm)
- docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md — FROZEN 2026-11-01T16:06:01Z, sha 72be3e83…18fb
- results/topic2/2026-11-02_fu_a/{card_sha256.txt, code_sha256_at_freeze.txt, freeze_time.json, fua_constants.json,
  design_stats_train.json, partitions/}
- verification/worker_FU_A_r1/mutation/ — verdict mutation harness (31/31 killed)
- B300: /scratch/iitp4/fu_a/{env/venv, code, data/subjects/hNN (symlinks), runs, logs}

## Change Tracker
- Files created: src/topic2_fu_a/* (6), scripts/topic2fu_a_* (6), tests/topic2_fu_a/* (9), card, results receipts
- Build status: FU-A tests 63 + receipts tests; flake8 clean
- Pending issues: gate (Slurm 507) running; Stage 1 only if F+ passes and budget rule holds

## Quality Status
- Build/test result: 63 passed pre-freeze (receipts deselected)
- Tests added/modified: tests/topic2_fu_a (target, sources, run, verdict, fixture_stage0, scripts, receipts_and_c4)

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place, not copied)
- Core methodology: frozen card before results; synthetic ground-truth fixtures; run records; verdict taxonomy; stop rules.
