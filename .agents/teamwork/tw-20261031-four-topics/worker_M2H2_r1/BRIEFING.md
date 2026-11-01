# BRIEFING — 2026-11-01T16:10Z (worker_M2H2_r1)

## Mission
Milestone M2H2: Topic 3 random-init control H2 (card §6; ACCEPTANCE H1′–H3′): freeze addendum_07 (H2 rule) → replication gate on connectome → K random-init seeds → stats → report.

## 🔒 My Identity
- Archetype: worker (implementer + qa + specialist)
- Roles: implementer, qa, specialist (sci-pipeline methodology)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2H2_r1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: M2H2

## 🔒 Key Constraints
- C1 protected hashes; all *_sha256.txt receipts; frozen cards never edited (addenda only).
- No participant IDs anywhere (no "sub-" bytes under results/topic3/** or docs/03_empirical_analysis/topic3/**).
- No git writes; no installs into shared envs on DGX-Spark; never read ~/.claude/settings.json or secrets.
- Write ownership: src/topic3_h2/, tests/topic3_h2/, scripts/topic3h2_*.py, results/topic3/2026-11-02_h2/,
  docs/.../topic3/2026-11-02_topic3_addendum_07_h2_card.md + 2026-11-02_topic3_h2_result_report.md,
  connectome /home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/, ledger rows (append, flock).
- PINNED: src/topic3_spectral, tests/topic3_spectral, scripts/topic3_*.py (never edit, never add scripts/topic3_ prefix).
- Frames + per-subject representations never leave connectome. connectome: no find/du/grep -r/ls -R over /storage,/scratch.
- GPU cap M2-H2 6 GPU-h on connectome (Slurm, -w node1). Local python: superclaude-env, PYTHONDONTWRITEBYTECODE=1, OMP 2, nice; ≤2 pytest procs, timeout 900.
- Freeze addendum_07 (with receipt) BEFORE any random-init forward on real frames.

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Task Summary
- What to build: src/topic3_h2 (vendored fork ver11 cd87338 + snapshot datasets.py, model/driver/stats/verdict), scripts/topic3h2_connectome.py, scripts/topic3h2_stats.py, tests/topic3_h2
- Success: H1′ frozen before results; H2′ gate (element-wise rel_fro ≤1e-5 all 57×7×4) passes or H2 = untestable; H3′ tests; report.

## Key Decisions Made
- Code: fork ver11 5bc44469 + patchembedding c889eebb (SwiFT_v2 cd87338), snapshot VRABES datasets.py 74316574 used verbatim.
- K = 10 seeds (1..10); δ = 0.5×|pinned trained effect| for contrast DiDs; δ = log 1.10 for levels.
- Shared-loader in-memory driver; frozen subject_summary in-job; only position-keyed scalars + subset PR vectors return.

## Artifact Index
- DISPATCH.md, progress.md, handoff.md (this dir)
- verification/worker_M2H2_r1/ — probes, mutants
