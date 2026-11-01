# BRIEFING — 2026-11-01T02:20Z

## Mission
M3 / Topic 2: T2.1 (ver11 merge locations from code) → T2.2 (falsifiable question, frozen card, ConnectomeRGBoxPooling + tests + 2 synthetic fixtures) → T2.3 (B300 pilot within cap, verdict per card, or escape clause).

## 🔒 My Identity
- Archetype: worker (roles implementer + qa + specialist[sci-pipeline])
- Host: claude-code; nested spawning NOT available; final report = StructuredOutput
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M3_r1/
- Original parent: root coordinator (workflow B, run tw-20261031-four-topics)
- Milestone: M3 (Topic 2 redesign)

## 🔒 Key Constraints
- C1 protected hashes (sentinel/PROTECTED_HASHES.txt); old src/rg_box_pooling.py + old tests read-only.
- C3 card frozen (sha256) BEFORE any real-data result incl. Stage 0; deviations only in dated addenda.
- C4 no participant IDs printed/written; no git writes; no installs into DGX-Spark shared envs.
- C5 B300: nvidia-smi before every launch, idle GPUs only, never touch others' procs; project-local env under /scratch/iitp4/; ledger rows (started/completed) under flock in results/gpu_ledger_2026-10-31.md; cap 64 GPU-h run-wide (M3 target <= ~14).
- C6 never read/list ~/enigma_ocd on B300; no ENIGMA-derived file on B300; HCP open access on .98 read-only.
- C7 SwiFT_v2 read-only (ver11 sha de132387…052a, commit f0dc7aca); vendored copy with provenance.
- C8 no old report numbers cited as results.
- Write ownership: src/topic2_rgpool/, tests/topic2_rgpool/, scripts/topic2_*.py, scripts/b300_env/, results/topic2/2026-11-01/, docs/03_empirical_analysis/topic2/, ledger (append), /scratch/iitp4/ (mine: /scratch/iitp4/worker_M3_r1/). Probes: verification/worker_M3_r1/.
- Local CPU: <=4 procs, nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1.
- Exclude 5 burned dev subjects (verification/explorer_M3_r1_1/dev_subjects_BURNED.md).

## Current Parent
- Root coordinator; updated: not yet

## Task Summary
- What to build: gather-index merge at M0 (16^3->8^3); arms E (identity = PatchMergingV2 bit-exact), C (octant-local FC boxes), S (distance-binned FC-shuffle null); SimMIM E36 d2262 pilot on HCP REST1_LR.
- Success criteria: ACCEPTANCE T2.1–T2.3, C1–C8; 86 old tests pass; new tests pass.

## Key Decisions Made
- (pending advisor) follow explorer_M3_r1_1 framework; use file-content sha256 as subject pseudonym (no ID-derived hashes written).

## Artifact Index
- scripts/b300_env/build_env.sh — B300 env recipe (build started 02:18Z on .98 into /scratch/iitp4/worker_M3_r1/venv)

## Change Tracker
- Files modified: scripts/b300_env/build_env.sh (new)
- Build status: n/a
- Pending issues: design, card, implementation

## Quality Status
- Build/test result: not run yet
- Lint status: n/a
- Tests added/modified: none yet

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md
- Local copy: none (read in place; metadata dir holds no copies)
- Core methodology: 9 gates; freeze card before results; synthetic ground-truth fixtures; run ledger; verdict taxonomy keep/modify/stop/inconclusive.
