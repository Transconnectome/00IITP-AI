# BRIEFING — 2026-11-01T15:45Z

## Mission
Explorer 2 of 3 for milestone M2H2 (Topic 3 random-init control H2; ACCEPTANCE H1'-H3'): give the worker a concrete, verifiable strategy, lens = feasibility and failure modes, evidence from cheap probes. Recommend only; no production code.

## 🔒 My Identity
- Archetype: explorer
- Roles: explorer (read-only investigation, synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M2H2_r1_2/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: M2H2

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- Probes/copies only under /home/juke/git/00IITP-AI/verification/explorer_M2H2_r1_2/
- C1-C8: protected hashes, receipts, frozen cards never edited, no participant IDs printed/written, no git writes, no installs on DGX-Spark shared envs, never read ~/.claude/settings.json
- connectome: never find/du/grep -r/ls -R over /storage or /scratch; labfind only
- Frames and per-subject representations never leave connectome
- No random-init result on REAL data before addendum_07 is frozen (so: random init only on synthetic input in my probes)
- GPU: at most one 0.25 GPU-h ledgered Slurm smoke; ledger under flock
- pytest <= 2 concurrent, timeout 900; PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: card, provenance, result report, addenda 01-06; VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh; VRABES/swift_extraction_code (snapshot of perlmutter extraction code); SwiFT_v2 commit cd87338 (seungju_perlmutter tip); connectome /storage/bigdata/VRABES/{03_MNI_to_TRs,04_embedding,05_pooled_embedding}; Slurm/QoS on connectome; scripts/topic3_token_job.py; src/topic3_spectral.
- **Key findings**: (1) local SwiFT_v2 HEAD ver11 is NOT the extraction function (default flags differ by O(1); legacy flags still differ ~1e-3 rel in attention); use cd87338 ver11. (2) trained ckpt has all 567 encoder keys (17 missing = decoder/mask only). (3) random-init on time-static synthetic input already gives token PR <= 7 at L2/L3 (~5.8-6.3), near the trained real medians -> ceiling/input-structure confound for token-level H2. (4) frozen token job writes per-subject pooled vectors into its npz -> must not be copied back under the H2 rule. (5) node1 is the only up GPU node (8xA5000), limit_qos 4 GPU/user, homes node-local.
- **Unexplored areas**: GPU timing for a full 57-subject pass (peers measured 0.27 s/window); uv/py3.12 venv build outcome.

## Key Decisions Made
- No own GPU smoke: peers explorer_M2H2_r1_1 (job 218004) and _r1_3 already ran the trained-dump replication smoke on connectome; a third would duplicate. CPU synthetic probes instead.

## Artifact Index
- verification/explorer_M2H2_r1_2/probes/probe_ver11_cpu.py (+ .out.json, .log) — random-init ver11 on synthetic input; code-version equivalence
- verification/explorer_M2H2_r1_2/probes/probe_ver11_localize.py (+ .out.txt) — where local HEAD ver11 departs
- verification/explorer_M2H2_r1_2/probes/probe_fixtures_cpu.py (+ .out.json) — fixture margins
- verification/explorer_M2H2_r1_2/probe_pkg/swift_cd87338/ — git archive of cd87338 project/module/models (read-only copy)
- connectome:/home/connectome/connectome1/iitp4_m2h2/explorer_M2H2_r1_2/ — probe venv build (to be removed)
