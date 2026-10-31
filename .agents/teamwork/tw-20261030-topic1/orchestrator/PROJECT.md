# Project: Topic 1 lag-motif extractor v2 (run tw-20261030-topic1)
Scope document of the virtual Project Orchestrator (root). Inputs: ../ORIGINAL_REQUEST.md, ../sentinel/APPROVED_PROPOSAL.md,
../sentinel/ACCEPTANCE.md. Survey evidence: survey_results_flat.txt, survey_journal_wf_9669a9bf-f92.jsonl (3 explorers,
agent IDs ab984d7e37e0e6347, a9e637ec16caed75f, ad0e82385c9a121ac), probes under /home/juke/git/00IITP-AI/verification/explorer_survey_{1,2,3}/.

## Assessment
Scope = one tightly coupled milestone (loader → flow → graph/null/census → fixtures → timing → card). ≤5 new modules.
Decision: 2B single Explorer→Worker→Reviewer iteration loop (no sub-orchestrators, no separate E2E track; the synthetic
fixtures are requirement-driven tests owned by the worker and independently re-run by reviewers/challengers).

## Architecture (survey consensus; explorers recommend, worker decides implementation details)
- Data source for primary (broadband) analysis: raw npy /home/juke/git/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25/ (3/3).
  VMD cache channels are [IMF1..IMF4 low→high, mask]; there is NO broadband channel (3/3). IMF channels exploratory or excluded.
- Lag in seconds: resample to common 2.0 s grid (resample_poly exact ratios), lag = 2 s (3/3).
- Graph: antisymmetric net flow, fixed density (top 15% |F|, m identical across subjects), all 304 ROIs (3/3).
- Null: degree-preserving, orientation-preserving swaps (reject new edge if it exists in EITHER direction; no self-loops) (3/3);
  irreducibility concern → triangle-reversal moves and/or multi-seed convergence check (2/3, literature unverified).
- Census: closed-form oriented 5-class census; networkx as test oracle (3/3). BLAS threads pinned to 1 (2/3).
- Endpoints: Z(030C) and Z(030C)−Z(030T); SP over 5 oriented classes has rank 2 (Z021D=Z021U=−Z030T) (3/3).
- Confounds (single/dual-explorer finds kept): HRF peak-delay differences create spurious direction not removable by
  surrogates → explicit limitation; Hodge gradient share covariate + curl-only sensitivity (explorer 2); drift: npy not
  high-passed → detrend/high-pass (explorer 1); duration/TR collinear with site; no FD/motion data.

## Feature Inventory
| # | Feature | Milestone | Source |
|---|---------|-----------|--------|
| 1 | Read-only loader from npy (and optional cache), valid-portion only, valid T + duration reported, explicit error on missing subject, no IDs in messages | M1 | survey 1/2/3 |
| 2 | Site→TR via enigma time_series_utils.repetition_time (read-only import or cited copy) | M1 | survey 1/2/3 |
| 3 | Detrend / high-pass choice documented | M1 | survey 1 |
| 4 | Resample to 2.0 s grid; lag-in-seconds net flow on 304 ROIs | M1 | survey 1/2/3 |
| 5 | Fixed-density oriented graph | M1 | survey 1/2/3 |
| 6 | Oriented degree-preserving null with per-null invariant assertions; seeds via SeedSequence | M1 | survey 1/2/3 |
| 7 | Closed-form 5-class census; Z, SP(5) with rank-2 identity documented | M1 | survey 1/2/3 |
| 8 | Optional gradient(Hodge) share + curl-only variant | M1 | survey 2 |
| 9 | Fixtures (fail-on-defect): null invariants, Z021D+Z030T==0, no-injection calibration, ≥20 planted cycles detection, padding (exact F), two-TR |F| ratio, time reversal through full chain, missing-subject error, spurious-direction quantification (AR φ mismatch, HRF delay) | M1 | ACCEPTANCE A2; survey 2/3 |
| 10 | Old 86 tests by explicit file list + protected hash check | M1 | A5; survey 1/2/3 |
| 11 | Timing on 5 real subjects (positional indices), pinned threads, per-stage wall time, peak RSS, swap-factor sensitivity, CPU-h extrapolation (추정) | M1 | A3; survey 1/2/3 |
| 12 | Frozen analysis card with sha256 (population 1,706 = OCD 869 / HC 837, 389 absent = 388 TR>2 s + 1 Vancouver; LMM site RE + within-site permutation; LOSO CV; ComBat leakage caveat; file-backed baselines 0.6512/0.6606/0.6420 random-split and LOSO 0.6519 — NOT "≈0.63"; Holm across 2 primary; kill |d|<0.15 or p≥0.05 with d/p definitions; medication within OCD 203 vs 212; HC coding unreliable; sex coding unverified; FD absent; CSTC dropped/exploratory; prior exposure to v1 d=0.08 disclosed) | M1 | A4; survey 1/2/3 |
| 13 | Open-issues log (A6): report-vs-JSON, spec errors, cohort-count conflict 869/837 vs 833/873, site_characteristics TR errors, v1 defects, HRF/phase-wrap/null-mixing limitations, npy preprocessing provenance unknown | M1 | A6; survey 1/2/3 |

All features assigned to M1 (cross-check passed).

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Topic 1 extractor v2 + fixtures + timing + frozen card | Features 1–13 | none | IN_PROGRESS (iteration loop) |

## Code Layout (exclusive worker ownership)
- src/topic1_lagmotif/ (new package), tests/topic1_lagmotif/ (new, with __init__.py), scripts/topic1_timing.py,
  results/topic1/2026-10-30/, docs/03_empirical_analysis/topic1/ (card + open issues).
- Read-only: everything else in repo (src/*.py, tests/* existing, docs/* existing, HANDOFF.md, 그랜트아이디어.md, 아이디어.txt), enigma repo.
- Probes: verification/<identity>/ only.

## Interface contracts
- Tests run: `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -m pytest tests/topic1_lagmotif -q`
- Old suite: `STRICT_E2E=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` → 86 passed expected.

## Runtime deviation noted by survey
Harness refused subagent writes of report.md ("Subagents should return findings as text"); full reports are in structured
returns persisted by root. Iteration agents: return complete reports in structured output; metadata file writes best-effort.
