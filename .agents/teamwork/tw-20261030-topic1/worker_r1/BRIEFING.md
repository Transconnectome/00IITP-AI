# BRIEFING — 2026-10-30T12:05Z

## Mission
Implement M1 (Topic 1 lag-motif extractor v2 + fixtures + 5-subject timing + frozen card) to satisfy ACCEPTANCE A1–A6.

## 🔒 My Identity
- Archetype: worker (implementer primary; qa)
- Roles: implementer, qa
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/worker_r1/
- Original parent: root coordinator (virtual Project Orchestrator); no SendMessage
- Milestone: M1

## 🔒 Key Constraints
- No GPU/ssh/Slurm/full-cohort; <=5 real subjects (A3 timing only); no git commit/push/stash/reset/checkout; no installs; no uploads.
- enigma_ocd_mbbn read-only; protected files byte-identical (sentinel/PROTECTED_HASHES.txt).
- Never print/write participant IDs (npy dir/file names). Positional index only.
- Exclusive write: src/topic1_lagmotif/, tests/topic1_lagmotif/, scripts/topic1_timing.py, results/topic1/2026-10-30/, docs/03_empirical_analysis/topic1/.
- PYTHONDONTWRITEBYTECODE=1; BLAS threads pinned to 1 for timing.

## Current Parent
- root coordinator; Updated: not yet

## Task Summary
- What to build: package src/topic1_lagmotif (tr_table, data, preprocess, flow, graph, census, null, hodge, pipeline, spurious), tests, timing script, card, open issues.
- Success criteria: sentinel/ACCEPTANCE.md A1–A6.
- Interface contracts: orchestrator/PROJECT.md

## Key Decisions Made
- See PARAMS in src/topic1_lagmotif/pipeline.py (frozen before A3). Density 10% primary (5%/15% sensitivity), n_null 1000, 20·m attempts per independent restart, 2-swap + 3-edge rotation (p_rot 0.2), detrend→resample_poly(padtype=line)→z→lag 2 s, head trim 40 s.

## Artifact Index
- handoff.md, progress.md (this folder)
