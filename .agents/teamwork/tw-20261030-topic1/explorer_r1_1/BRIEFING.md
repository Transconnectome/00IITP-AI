# BRIEFING — 2026-10-30T11:55Z

## Mission
M1 strategy for the worker: concrete, verifiable implementation plan covering Feature Inventory 1-13 and ACCEPTANCE A1-A6, with cheap synthetic probes on the riskiest design choices.

## 🔒 My Identity
- Archetype: explorer (read-only investigation)
- Roles: explorer
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261030-topic1/explorer_r1_1/
- Original parent: root coordinator (virtual Project Orchestrator), run tw-20261030-topic1
- Milestone: M1
- Host: claude-code; no Agent/SendMessage exposed to me; final report = StructuredOutput

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes only under /home/juke/git/00IITP-AI/verification/explorer_r1_1/
- No real-subject time-series loading by me (5-subject limit belongs to worker A3 / verifiers); synthetic probes only
- No GPU/ssh/Slurm/git writes/installs/uploads; enigma repo read-only; protected hashes must stay OK
- Never print/write participant IDs

## Current Parent
- Conversation ID: root coordinator
- Updated: not changed

## Investigation State
- Explored paths: run docs, survey_results_flat.txt, survey probes, enigma time_series_utils.py:5-75
- Key findings:
  1. Null: 2-swap is reducible (N=5: 7,862/12,382 classes). Adding 3-cycle reversal and the path move leaves 60 reducible at N=5 and 0/60 at N=6. Null moments are equal at N=60 and N=304 within MC SE (P1, P1e).
  2. Detrend BEFORE resample_poly: resampling raw-scale data first gives corr 0.00. Drift barely matters for F (P2).
  3. 200 nulls suffice: MC SD of Z ≈ √((1+Z²/2)/n). A swap factor of 20–30 is enough (P3).
  4. Density: at 15%, sparse planted cycles are invisible (N=304 ΔZ 0.05 vs 2.96 at 5%; N=60 min Z −0.32 vs 11.1). Degenerate nulls (SD=0) are common at 5% in latency-dominated graphs (P4b, P8).
  5. HRF latency gives Z030T down to −6 at 15%. Curl-only is also biased. AR-φ mismatch is calibrated (P5, P5b, P8).
  6. d/p: raw pooled d with Welch p gives a 19.5% false-positive rate; site-FE, LMM and permutation are calibrated. Use Freedman–Lane with covariates (P6).
  7. Fixture tolerances: exact time reversal holds only at TR 2.0. Padding is exact if truncation comes first. Two-TR: use the |F| ratio, not sign agreement (P7).
- Unexplored areas: real-data density/degeneracy (worker A3), complete irreducible move set, covariate-adjusted permutation calibration

## Key Decisions Made
- Synthetic-only probes (respect 5-subject rule)
- Recommend 5% primary density + degeneracy fallback rule; mixed null kernel p=0.1; 200 nulls; Freedman–Lane p

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-part report (= structured return full_report)
- /home/juke/git/00IITP-AI/verification/explorer_r1_1/*.py,*.log — probes
