# BRIEFING — 2026-11-01T01:42Z

## Mission
M3 (Topic 2) explorer 2 of 2: feasibility + failure-mode strategy for connectome box-covering RG pooling vs Euclidean PatchMergingV2 in SwiFT (T2.1–T2.3). Recommend only.

## 🔒 My Identity
- Archetype: explorer (Teamwork General route)
- Roles: explorer (read-only investigation, synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M3_r1_2/
- Original parent: root coordinator (workflow B, run tw-20261031-four-topics)
- Milestone: M3 Topic 2 redesign

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code; probes only in /home/juke/git/00IITP-AI/verification/explorer_M3_r1_2/
- C1 protected hashes; C4 no participant IDs, no git writes, no installs into DGX-Spark shared envs
- C6: never read/copy/move ~/enigma_ocd/data on B300; no ENIGMA-derived files on B300; boxes from public atlas or permitted data
- B300: nvidia-smi before any GPU use; idle GPUs only; ≤0.25 GPU-h smoke, ledger results/gpu_ledger_2026-10-31.md under flock; ~/envs/swiftllm must NOT be used; env under /scratch/iitp4/
- Local CPU: ≤4 procs, nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1
- Background docs' numbers are not results (C8)

## Current Parent
- Conversation ID: root coordinator
- Updated: not yet

## Investigation State
- **Explored paths**: ver11 code (merge/stage/decoder/hook), all local ver11 variants, SwiFT S1200 crop/pad, B300 4 nodes (GPUs, /scratch/data, env lock), FSL MNI mask + Schaefer-400 token map
- **Key findings**: merges only at ends of stages 0-2; only 16^3->8^3 viable (85 permutable parents vs 8 at 8^3->4^3); permutation wrapper exact-matches params/FLOPs, 5/5 mutants caught; random boxes not locality-matched (51 vs 20 mm), rotation null matched; operator-level realistic gain tiny; masked NMSE has capacity on F+strong (0.927 vs 0.996/1.001); e24 B=32 201 samples/s -> ~1 GPU-h/run; pilot 14-25 GPU-h fits cap; HCP C6 'public' status is the gating PI decision
- **Unexplored areas**: perlmutter fork; subject-level masks; multi-seed fixture gate; B>32/multi-GPU throughput

## Key Decisions Made
- Recommend 16^3->8^3 only; BoxPermutedMerge operator; A1 Euclidean / A2 FC box-cover / A3 rotation null; primary metric held-out masked NMSE; HCP primary, ds000228 fallback
- Used 0.134 GPU-h on B300 (.98 GPU7), ledger rows written

## Artifact Index
- DISPATCH.md — verbatim dispatch
- progress.md — heartbeat
- handoff.md — final 5-component report
- /home/juke/git/00IITP-AI/verification/explorer_M3_r1_2/ — probes + logs
- /home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md — ledger (created by me)
- B300 .98 /scratch/iitp4/explorer_M3_r1_2/ — probe env (5.5 GB), logs
