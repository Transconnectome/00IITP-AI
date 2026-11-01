# BRIEFING — 2026-11-01T17:05Z

## Mission
Empirically challenge milestone M2H2 (Topic 3 H2 random-init control): CONFIRMED or REFUTED with evidence.

## 🔒 My Identity
- Archetype: challenger (roles: critic, specialist)
- Host: claude-code (Opus 5.5); nested spawning not available; structured return = final report
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_M2H2_r1_1/
- Probe dir: /home/juke/git/00IITP-AI/verification/challenger_M2H2_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: M2H2; Instance: 1 (r1)

## 🔒 Key Constraints
- Review-only: never edit production files (src/topic3_h2, tests/topic3_h2, scripts/topic3h2_*, results/, docs/)
- Pinned: src/topic3_spectral, tests/topic3_spectral, scripts/topic3_*.py; no new scripts/topic3_ files
- C1 protected hashes; all *_sha256.txt receipts; frozen cards never edited
- No participant IDs printed/written; no git writes; no installs on DGX-Spark; no secrets/settings.json
- Python: /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; <=2 concurrent pytest, timeout 900
- connectome: never find/du/grep -r/ls -R over /storage or /scratch; GPU only via Slurm, ledgered, <=1 GPU-h for me
- Metadata only in this folder

## Current Parent
- root 5fddb83e; Updated: 2026-11-01T17:25Z (unchanged)

## Review Scope
- Files: src/topic3_h2/, tests/topic3_h2/, scripts/topic3h2_*.py, results/topic3/2026-11-02_h2/, docs/.../2026-11-02_topic3_addendum_07_h2_card.md (sha 09b45220…), 2026-11-02_topic3_h2_result_report.md
- Criteria: freeze-before-results, verdict follows card §6, headline numbers recomputed from saved raw outputs, mutation robustness

## Claims to verify (from worker handoff)
- card frozen 15:57:40Z before first random-init forward (job 218064 16:32:19Z)
- gate PASS (G1 max rel_fro 7.8e-7; G2 7.0e-7; G3 7.3e-8; G4; G5 controls fail, min 4.6e-4)
- C1 INC +0.0124 [0.0104,0.0145] δ .0114; C2 INC +0.0295 [0.0256,0.0334]; C3 TE+ +5.09 [2.93,7.25]; C4 TE+ +5.79 [4.01,7.57]
- Family L labels; 71 tests; 32/32 mutants killed; output_sha256 61 entries; 0.458 GPU-h

## Key Decisions Made
- Recompute from saved npz independently (no use of h2stats arithmetic)

## Attack Surface
- Hypotheses tested: freeze order (holds); headline recomputation from npz with own code (holds, 2.7e-14); report numbers (hold);
  ID leak (clean, boundary-aware real-label scan); connectome probe 218069: R0 G1 recheck pos 5/17/40 (7.65e-7, 0 fail),
  seeds 4/1 hash = shipped and scalars bitwise = shipped; baseline 71 tests pass
- Vulnerabilities found: (1) scripts/topic3h2_stats.py (writes h2_results/labels) has zero tests; copy-paste mutant
  "all arms read R1" flips C1 INC->EQ + 4 L labels (sim); harness run pending. (2) δ sensitivity: C3 TE+ only for
  δ/|T| <= 0.548 (frozen 0.5); C2 TE+ for <= 0.458; report §6.1 misattributes boundary to C1 (C1 INC robust 0.16-1.0)
  (3) ledger closing rows of worker jobs in KST not UTC (minor)
- Untested angles: driver.py negative-control mutants (needs GPU); explorer exposure taken from handoffs

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; no copy needed for review)
- Core methodology: frozen card before results, synthetic fixtures, run records, G8 verdict taxonomy

## Artifact Index
- DISPATCH.md, BRIEFING.md, progress.md, handoff.md (this folder)
