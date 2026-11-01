# BRIEFING — 2026-11-01T03:25Z

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
- Framework of explorer_M3_r1_1 (gather pi at M0, arms E/C/S, octant-local, Hungarian placement) with explorer_M3_r1_2's parameter-free wrapper around stock PatchMergingV2 (paired init by construction).
- Subject pseudonym = sha256 of file content (16 hex); burned exclusion in memory on B300.
- Data: HCP-YA open access REST1_LR on .98 (C6 position stated in card; PI to confirm; fallback ds000228).
- delta = 0.01 worker-set pending PI; primary = t interval over 5 seed contrasts; Option B (Stage 0 descriptive only).
- Card frozen 03:14:34Z (sha c9bfc60a…41f5). Fixture gate F+ must pass before Stage 1.

## Artifact Index
- scripts/b300_env/build_env.sh + lock.txt — B300 env recipe/lock (/scratch/iitp4/worker_M3_r1/venv)
- docs/03_empirical_analysis/topic2/2026-11-01_topic2_architecture.md — T2.1
- docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md — frozen card
- results/topic2/2026-11-01/{card_sha256.txt, code_sha256_at_freeze.txt, hcp_manifest.json, split.json, partitions/}
- B300: /scratch/iitp4/worker_M3_r1/{hcp, partitions, runs, logs, code}

## Change Tracker
- Files: src/topic2_rgpool/* (new pkg), tests/topic2_rgpool/* (new), scripts/topic2_*.py (new), scripts/b300_env/* (new), docs/.../topic2/*, results/topic2/2026-11-01/*
- Build status: 51 new tests pass (03:13Z)
- Pending issues: wave 1 fixture gate running; Stage 1; verdict; report; final checks

## Quality Status
- Build/test result: tests/topic2_rgpool 51 passed (pre-freeze)
- Lint status: n/a
- Tests added: merge invariants+mutants, partition, model pairing, data, stats, stage-0 fixtures, leakage, provenance, loop smoke, ID scan

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md
- Local copy: none (read in place; metadata dir holds no copies)
- Core methodology: 9 gates; freeze card before results; synthetic ground-truth fixtures; run ledger; verdict taxonomy keep/modify/stop/inconclusive.
