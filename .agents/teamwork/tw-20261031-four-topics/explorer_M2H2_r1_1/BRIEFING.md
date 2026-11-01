# BRIEFING — 2026-11-01T15:05Z

## Mission
Explorer 1/3 for milestone M2H2 (Topic 3 random-init control H2; ACCEPTANCE H1'-H3'). Lens: scientific design and falsifiability. Recommend a concrete verifiable strategy; no production code.

## 🔒 My Identity
- Archetype: explorer (General route, workflow C)
- Roles: explorer (investigation + synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M2H2_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e
- Milestone: M2H2

## 🔒 Key Constraints
- Read-only investigation; do NOT implement production code. Probes only under verification/explorer_M2H2_r1_1/ (local) and an explorer-owned dir on connectome.
- C1-C8; no IDs printed/written; no git writes; no installs into shared envs on DGX-Spark; frames/per-subject reps never leave connectome.
- connectome: never find/du/grep -r/ls -R over /storage or /scratch; use labfind.
- GPU: <=0.25 GPU-h smoke via Slurm, ledgered under flock.

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- Explored paths: card/provenance/report/addenda 01-06; src/topic3_spectral; VRABES extract_vrabes_swift_E192.sh, pool_E192_layersweep.py, swift_extraction_code snapshot (Oct-18 copy); connectome bundle /storage/connectome/swift_v2_extraction_bundle; ckpt on connectome.
- Key findings: bundle ver11 (5bc44469) + snapshot preprocessing reproduce stored trained dump to 7.7e-7 (smoke 218004); local SwiFT_v2 ver11 (de132387, cited by provenance) is a different net (double MLP, summed RoPE); TF32 must be off; H2 feasible ~1.5-2.5 GPU-h.
- Unexplored areas: full 57x7 replication; unexpected ckpt key name; zoo checkpoints; other explorers' exposure

## Key Decisions Made
- Build explorer-owned py3.8 torch 2.4.0+cu121 venv in connectome node1 home (~/iitp4_m2h2/explorer_M2H2_r1_1).

## Artifact Index
- handoff.md — final 5-component report with H1'-H3' strategy
- verification/explorer_M2H2_r1_1/probes/smoke_replicate.py, smoke_out_218004.json, smoke_218004.log.txt, ship_sha256.txt, venv_freeze_connectome.txt, bundle_copy_manifest_sha256.txt
- connectome: /home/connectome/connectome1/iitp4_m2h2/explorer_M2H2_r1_1/ (venv, ship, smoke outputs)
- verification/explorer_M2H2_r1_1/probes/ckpt_keys_probe.{py,out} — ckpt structure without torch
- verification/explorer_M2H2_r1_1/copied/bundle — copy of connectome bundle code (read-only reference)
- verification/explorer_M2H2_r1_1/labfind_code.txt — labfind results
