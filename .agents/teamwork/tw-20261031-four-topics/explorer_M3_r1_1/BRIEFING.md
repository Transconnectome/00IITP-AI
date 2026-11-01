# BRIEFING — 2026-11-01T02:08Z (created 00:40Z)

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
- **Explored paths**: ver11 code (f0dc7aca); SwiFT HCP preprocessing; B300 /scratch/data on 4 nodes (read-only); connectome HCP holdings; old src/rg_box_pooling.py head; AST audit test
- **Key findings**: merges M0/M1/M2 only (12->24->48->96 mm); M0 is the only roomy point (235 blocks); octant-local downstream; gather-index merge bit-exact for identity; HCP REST1 .98 (88) usable; ~100 samples/s E36 SimMIM on B300; dev (burned 5): C>>S but C<E on held-out coherence
- **Unexplored areas**: perlmutter fork; SimMIM convergence on real data; HCP family structure
## Key Decisions Made
- Merge point M0 with octant locality (decided on architecture grounds before real-data preview, progress 01:05Z)
- Single changed factor = gather index pi; arms E/C/S for GPU, +G/R/C_global for Stage 0
- Recommend Stage 1 run regardless of Stage 0 (option B, ~9-10 GPU-h); option A gate offered
- Box algorithm dense-core + mean-linkage (periphery/max fails F+)
## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report
- /home/juke/git/00IITP-AI/verification/explorer_M3_r1_1/ — probes, outputs, burned-subject list, env recipe
- /scratch/iitp4/explorer_M3_r1_1/ on B300 .98 — own venv + probe copies (ephemeral)
