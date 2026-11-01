# BRIEFING — 2026-11-01T00:40Z

## Mission
M3 / Topic 2 redesign (connectome box-covering RG pooling for SwiFT), ACCEPTANCE T2.1–T2.3: give the worker a concrete, verifiable strategy. Primary lens: scientific design (falsifiable question, card, controls, kill criterion, permitted/usable data). Recommend only; no production code.

## 🔒 My Identity
- Archetype: Teamwork explorer (read-only investigation + synthesis)
- Roles: explorer_M3_r1_1 (explorer 1 of 2 for M3, round 1)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M3_r1_1/
- Original parent: root coordinator (workflow B, M3+M4), launched 2026-11-01; native parent ID not exposed to me
- Milestone: M3 (Topic 2)
- Host: claude-code (Opus 5.5); nested spawning NOT available; final report = StructuredOutput return

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Metadata only in this dir; probes only under /home/juke/git/00IITP-AI/verification/explorer_M3_r1_1/
- C1 protected hashes; C4 no participant IDs printed/written, no git writes, no installs on DGX-Spark shared envs, never read ~/.claude/settings.json
- C6: never read/copy/move/delete ~/enigma_ocd/data on B300; no ENIGMA-derived file on B300; box connectome must not be ENIGMA-on-B300
- C7 external repos read-only (SwiFT*, VRABES, enigma_ocd_mbbn)
- C8 old report numbers not citable as results
- Local CPU: PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice, ≤4 processes
- B300: nvidia-smi before any launch; idle GPUs only; ≤0.25 GPU-h smoke, logged under flock in results/gpu_ledger_2026-10-31.md; ~/envs/swiftllm NOT usable; env under /scratch/iitp4/
- ≤5 real subjects read-only for probes

## Current Parent
- Conversation ID: root coordinator (ID not exposed)
- Updated: not yet

## Investigation State
- **Explored paths**: runtime/role files; ORIGINAL_REQUEST, ACCEPTANCE, RESUME; survey handoffs 1–3
- **Key findings**: (from surveys, to re-verify) ver11 PatchMergingV2 merges 2x2x2 spatial only at end of stages 0–2; no merge between layer_2/layer_3; UKB Schaefer-400 ROI copy on B300 sits inside ~/enigma_ocd/data/ukb (C6 hazard)
- **Unexplored areas**: own verification of ver11 code; B300 current data state; UKB data provenance/location; topic3 docs; old rg_box_pooling.py

## Key Decisions Made
- [TBD]

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report (pending)
