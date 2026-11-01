# BRIEFING — 2026-11-01T02:32Z (DONE)

## Mission
Implement M4 (Topic 4 redesign): T4.1 diagnosis+fixtures → T4.2 frozen card → T4.3 local-learning implementation, fixtures, CPU run, verdict per card.

## 🔒 My Identity
- Archetype: worker (roles: implementer, qa, specialist[sci-pipeline])
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M4_r1/
- Original parent: root coordinator (workflow B, run tw-20261031-four-topics)
- Milestone: M4 (Topic 4)

## 🔒 Key Constraints
- C1 protected hashes (old src/*.py, old tests, docs/03_empirical_analysis/*.md read-only).
- Write only: src/topic4_resu/, tests/topic4_resu/, scripts/topic4_*.py, results/topic4/2026-11-01/, docs/03_empirical_analysis/topic4/, verification/worker_M4_r1/ (probes), this metadata dir.
- No participant IDs printed/written (positions or salted hashes only). No git writes. No installs.
- ENIGMA data: CPU only on DGX-Spark (or connectome); never B300 (C6). 0 GPU-h planned.
- ≤4 local CPU procs, nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1. Long jobs detached with progress log.
- Card frozen (sha256) before any real-data result it governs (incl. tuning). Deviations → dated addendum.
- Do not cite old report numbers as results (C8).

## Current Parent
- Conversation ID: root coordinator; Updated: not yet

## Task Summary
- What to build: see DISPATCH.md; success = ACCEPTANCE T4.1–T4.3 + C1–C8.
- Code layout: orchestrator/PROJECT.md (topic4 → src/topic4_resu …)

## Key Decisions Made
- Single engine: masked-lateral PSP (Pehlevan 2018), linear, minibatch local Hebbian/anti-Hebbian; equilibrium by solve (fixture: = local relaxation); stability monitored (rho(I-D^-1M)<1), never enforced; diag guard rejected (probe_1: kills dense recovery).
- eta0 chosen by stability only (ladder 0.02/0.01/0.005), never by skill (skill rewards unconverged sparse engines, probe_2).
- TR=2.0 only (1195 subj, 13 sites); 15% tuning + 5-fold cross-fitting (deviation from LOSO example, recorded in card s10).
- H1 = C4-C1 (delta 0.01, PI confirmation pending); S1 C4-C4DP, S2 C5-randlin24, S3 C5-MLPenc (Bonferroni 98.33%).
- Card frozen 02:04:41Z sha 2b535c39...5934 (read-only chmod). Code hashes in results/topic4/2026-11-01/code_sha256_at_freeze.txt.

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; no local copy needed — metadata only)
- Core methodology: 9 gates; frozen card before results; synthetic fixtures with known truth; run ledger; verdict taxonomy keep/modify/stop/inconclusive/no_candidate.

## Change Tracker
- Files created: src/topic4_resu/** (12 py), tests/topic4_resu/** (14 py), scripts/topic4_{qualify,t41_counterfactual,build_split,run,analyze}.py, docs/03_empirical_analysis/topic4/{card,T41_diagnosis}.md, results/topic4/2026-11-01/*
- Build status: new 67 passed; old 86 passed (pre-freeze)
- Pending: none (delivered; see handoff.md)

## Quality Status
- Build/test result: C1 rc=0 at 01:13Z; new 67/67, old 86/86 at 02:02Z
- Tests added: T4.1 F1-F4, data contract, split, topologies, PSP engine (F5/F6/F8, equivariance), no-backprop (AST/runtime/target invariance), VAR Bayes, train-only, MLP adequacy, stats, output ID scan
- Mutation: 17/17 killed (verification/worker_M4_r1/mutants/mutation_results.json)

## Artifact Index
- DISPATCH.md — assignment
- docs/03_empirical_analysis/topic4/2026-11-01_topic4_analysis_card.md — frozen card
- docs/03_empirical_analysis/topic4/2026-11-01_topic4_T41_diagnosis.md — T4.1
- results/topic4/2026-11-01/ — qualification, t41, split manifest, tuning, confirm/, run_ledger, verdict
- verification/worker_M4_r1/ — probes 1-2, smoke, mutants
