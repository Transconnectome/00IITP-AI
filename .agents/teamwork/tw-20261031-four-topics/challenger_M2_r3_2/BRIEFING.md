# BRIEFING — 2026-11-01T06:35Z

## Mission
Empirically challenge M2 (Topic 3) iteration 3: write my own verdict-path / producer-path mutants, run them against the shipped suite in copied trees, recompute headline + addendum numbers from raw outputs, check card-freeze ordering and verdict rule conformance, check addenda 03-05 accuracy. Return CONFIRMED or REFUTED.

## 🔒 My Identity
- Archetype: challenger (roles: critic, specialist)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_M2_r3_2/
- Original parent: root coordinator (workflow harness); no native ID supplied to me
- Milestone: M2 Topic 3, iteration 3 gate
- Instance: challenger 2 of 2 (r3 gate)
- Host: claude-code; nested spawning NOT available; final report = StructuredOutput

## 🔒 Key Constraints
- Review-only: never edit production files (src/, scripts/, tests/, docs/, results/). Pinned files never edited.
- Probes/copied trees only under /home/juke/git/00IITP-AI/verification/challenger_M2_r3_2/
- Metadata only in this folder.
- PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice; python /home/juke/superclaude-env/bin/python3
- <=2 concurrent pytest, each under timeout 900; timeout/OOM = INVALID (rerun), never a kill
- Never run scripts/topic3_*.py in production tree (OUT hardcoded); only in copied trees
- No participant IDs printed/written; no git writes; 0 GPU
- Survivor refutes only if reachable on inputs the card's procedure can produce AND changes a verdict or reported number

## Current Parent
- root coordinator; Updated: not yet

## Review Scope
- Files: src/topic3_spectral/*, scripts/topic3_*.py, tests/topic3_spectral/* (esp. test_verdict_rules_r3.py, test_token_stats_wiring_r3.py), results/topic3/2026-10-31/*, docs/03_empirical_analysis/topic3/* (card, report, addenda 01-05)
- Criteria: ACCEPTANCE C1-C8, T3.1-T3.4; r2b gate blocking classes closed

## Key Decisions Made
- Independence: not reading other r3 gate members' folders (auditor_M2_r3_1, challenger_M2_r3_1, reviewer_M2_r3_1)
- Own tree: verification/challenger_M2_r3_2/tree_base (manifest = production, 84 files); controls 121/88 passed, 0 skipped
- Survivor classification: VERDICT change on reachable synthetic input = blocking; cited Family A number change on real data = blocking (r2b B3 precedent); MC seed reshuffles and killed-record label changes = nonblocking

## Attack Surface
- Hypotheses tested: r3 tests close r2b classes (CF01-CF07 re-written by me); D1/D3 verdict branches fully guarded; Family A reported numbers guarded; Family B headline reproducible independently; addenda numbers accurate; card frozen before results.
- Vulnerabilities found: D1 corr-only branch unguarded (VA01/VA02 survive 121, witness flips D1 verdict at card params); Family A reported numbers unguarded (FA01-FA08 survive 121 and change pinned values on real-data rerun, e.g. L1 jackknife SE 3.58->4.61, A2 calibration 0.406->~0.19); VB02 changes direction/agree count in killed records.
- Untested angles: token_job producer on real frames (connectome only); old 86-suite and topic1 not rerun by me.

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; not copied, metadata dir is metadata-only)
- Core methodology: frozen card before results, synthetic ground truth, run records, verdict taxonomy, independent review

## Artifact Index
- DISPATCH.md — dispatch record
- progress.md — heartbeat
- handoff.md — final 5-component report
