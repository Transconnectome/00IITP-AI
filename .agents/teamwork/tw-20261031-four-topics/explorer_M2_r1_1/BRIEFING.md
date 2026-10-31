# BRIEFING — 2026-10-31T08:05Z

## Mission
M2 (Topic 3) strategy: concrete, verifiable plan for T3.1-T3.4 (layerwise centered PR / spectral rerun), with cheap probes flagging risky choices. No production code.

## 🔒 My Identity
- Archetype: explorer (General route)
- Roles: explorer
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M2_r1_1/
- Original parent: root coordinator (workflow wf_59fa8ec4-d01)
- Milestone: M2 Topic 3

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes only in /home/juke/git/00IITP-AI/verification/explorer_M2_r1_1/
- C1 protected hashes; C4 never print/write participant IDs (npz `ids` key); no git writes; no installs
- C6 VRABES/ENIGMA patient-derived data never to B300; C7 external repos read-only
- Do not reveal governed real-data values before card freeze beyond what surveys already printed

## Current Parent
- Conversation ID: root coordinator
- Updated: not yet

## Investigation State
- **Explored paths**: VRABES/RemissionAnalysis npz x7 + pool/extract scripts; SwiFT_v2 ver11 merge/norm; eca/srg estimators; connectome token dumps + zoo + env; dgx1; synthetic estimator probes
- **Key findings**: report = eca centered (exact 4dp x5), json = srg uncentered (exact x7); old graph metrics mean-dominated (cos 0.97-0.9995, Jaccard 0.26-0.46); layer_3 = post-final-LN (token std 1.006); percentile bootstrap undercovers (0.06) vs subsampling w/o replacement valid (0.95/0.96); alpha biased at N=57; token work must run on connectome (0.2 MB/s transfer); 3 extra full E192 zoo checkpoints
- **Unexplored areas**: perlmutter fork diff; LN beta/gamma (ckpt on NERSC); frames->npz re-pool match; random-init feasibility

## Key Decisions Made
- Recommend token-level (connectome, CPU venv) as primary layerwise test; subject-level re-estimates old claims; alpha descriptive only
- Do not edit protected srg/eca; new loader raises on missing file

## Artifact Index
- handoff.md — final 5-section report
- /home/juke/git/00IITP-AI/verification/explorer_M2_r1_1/ — probes P1,P2,P2b,P3,P3b + outputs
