# BRIEFING — 2026-10-31T08:25Z

## Mission
Recommend a concrete, verifiable worker strategy for M2 (Topic 3 layerwise PR / spectral rerun, ACCEPTANCE T3.1–T3.4), with cheap-probe evidence on risky choices. Read-only; no production code.

## 🔒 My Identity
- Archetype: explorer (Teamwork General route)
- Roles: explorer (investigation + synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M2_r1_2/
- Original parent: root coordinator (run tw-20261031-four-topics)
- Milestone: M2 Topic 3

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes only in /home/juke/git/00IITP-AI/verification/explorer_M2_r1_2/
- C1 protected hashes (old src/spectral_rg_flow_diagnostic.py and src/empirical_connectome_ablation.py are protected: never edit)
- C4 no participant IDs printed/written; npz `ids` key never printed; no git writes; no installs on DGX-Spark
- C6 VRABES patient-derived data stays on lab machines (connectome, DGX-Spark); never B300
- C7 external repos (VRABES, SwiFT_v2) read-only
- No real-data results beyond reproduction of already-public numbers before the M2 card is frozen

## Current Parent
- Conversation ID: root coordinator
- Updated: not yet

## Investigation State
- Explored: old estimators (spectral_rg_flow_diagnostic.py, empirical_connectome_ablation.py), VRABES pooled npz (keys/shapes/hashes, ID alignment as booleans), pool_E192_layersweep.py, SwiFT ver11 hook, connectome frame dumps + zoo, connectome env.
- Key findings: handoff.md O1–O13 (repro exact; MLE biased at N57; LN needs corrPR on tokens; row bootstrap biased; graph metrics track rank; dumps re-pool to npz; numpy loader works on connectome; link ~0.3 MB/s)
- Unexplored: dgx1 env; swift_zoo_ses-02; VRABES extraction preprocessing; internet on connectome for uv venv

## Key Decisions Made
- Probes synthetic-only except exact reproduction of public report/json numbers and schema reads.

## Artifact Index
- handoff.md — 5-section report
- /home/juke/git/00IITP-AI/verification/explorer_M2_r1_2/probe_*.py/.out.* — probes
