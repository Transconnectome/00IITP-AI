# BRIEFING — 2026-10-31 (hand-typed stamp; approx. 08:55Z)

## Mission
M2 Topic 3: rerun layerwise PR / spectral diagnostics (ACCEPTANCE T3.1–T3.4) under C1–C8.

## 🔒 My Identity
- Archetype: worker (implementer + qa + specialist[sci-pipeline])
- Roles: implementer, qa, specialist
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2_r1/
- Original parent: root coordinator (workflow wf_59fa8ec4-d01)
- Milestone: M2 (Topic 3)

## 🔒 Key Constraints
- Do not edit protected files (C1; 67 pins). No IDs written (positions only). No git writes. No installs on DGX-Spark.
- Nothing to B300 (VRABES patient-derived). GPU-h used: 0. Token compute in place on connectome (node2, CPU, Slurm).
- Card frozen BEFORE new real-data computation; deviations only in dated addendum.
- Write ownership: src/topic3_spectral, tests/topic3_spectral, scripts/topic3_*.py, results/topic3/2026-10-31, docs/03_empirical_analysis/topic3.

## Current Parent
- Conversation ID: root coordinator; Updated: not yet

## Task Summary
- What to build: provenance → fixtures → frozen card → real rerun (Family A local, Family B connectome) → dated report with per-claim verdicts.
- Success criteria: ACCEPTANCE T3.1–T3.4, C1–C8; old 86 + topic1 + new tests pass; C1 rc 0.
- Code layout: orchestrator/PROJECT.md

## Key Decisions Made
- corrPR variance floor 1e-3×median (larger floor breaks gain invariance; fixture shows it).
- Subject-level α not estimable (synthetic calibration); token α: L0/L1 both estimators, L2/LN0L2/L3 rank slope only.
- Graph metrics out of scope; random-init H2 pre-specified but deferred → untested.
- Card sha 683374565d80… frozen 08:48:29Z.
- Deviation: cluster policy refused node1 (GPU-only) → node2 (CPU); launcher fixed (% escape, node2 staging) after freeze.

## Artifact Index
- docs/03_empirical_analysis/topic3/2026-10-31_topic3_{provenance,analysis_card}.md
- results/topic3/2026-10-31/{t3_1_provenance_repro,alpha_calibration_synthetic,family_A_subject_level}.json, card_sha256.txt, code_sha256_at_freeze.txt
- verification/worker_M2_r1/{mutants.py,mutants.out.json,py38_compat_*}

## Change Tracker
- Files: all new in owned paths (see Artifact Index + src/topic3_spectral/*.py, tests/topic3_spectral/*.py, scripts/topic3_*.py)
- Build status: 54 topic3 tests pass (pre-freeze)
- Pending: token job 217845, Family B stats, report, addendum, final test suite

## Quality Status
- Tests added: centering, LN/corr, alpha, resampling, io contract, token job, driver e2e, analysis, no-ids
- Mutants: 9/9 killed

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; no local copy) — gates G1–G9: frozen card before results, synthetic ground truth, run records, verdict taxonomy.
