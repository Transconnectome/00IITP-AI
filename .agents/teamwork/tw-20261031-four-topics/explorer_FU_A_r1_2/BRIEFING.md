# BRIEFING — 2026-11-01T14:50Z

## Mission
FU-A (Topic 2 follow-up A, lower-noise 12 mm target) explorer 2 of 3: feasibility and failure modes; give the worker a concrete, verifiable strategy (card, code, fixtures, Slurm logistics, cost). Recommend only.

## 🔒 My Identity
- Archetype: explorer (Teamwork General route, workflow C)
- Roles: explorer (investigation, synthesis)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_FU_A_r1_2/
- Probe dir: /home/juke/git/00IITP-AI/verification/explorer_FU_A_r1_2/ ; B300: /scratch/iitp4/explorer_FU_A_r1_2/ (b300-01 and b300-02)
- Original parent: root coordinator, Claude session 5fddb83e
- Milestone: FU_A

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code; no git writes
- C1–C8; no participant IDs printed/written; frozen r1 code/card untouched; sealed material never copied to repo
- B300 GPU only via Slurm; ≤0.25 GPU-h ledgered smoke; ledger rows under flock
- Local python: PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; ≤2 pytest procs, timeout 900

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Investigation State
- **Explored paths**: r1 card, result report §7, train.py, data.py, fixtures.py, metrics.py, model.py, stats.py, scripts/topic2_train.py, topic2_verdict.py, topic2_launch_wave.py, topic2_preprocess_hcp.py, b300_env, M3_r2 gate record, addendum 05, r1 run.json/train_log, ledger; B300 Slurm/sinfo, /scratch layout on 4 nodes
- **Key findings**: (1) r1-shaped FU-A = 12 gate + 15 Stage-1 runs x 0.433 GPU-h = 11.7 GPU-h > cap 8 (§7 6.5 excludes the gate); (2) HCP raw + r1 preprocessed data + venv exist ONLY on b300-01 local /scratch; other FU teams contend for b300-01; (3) r1 cellmeans.npy already exist (4096x1200 per subject) -> compact 12 mm target store ~1.7 GB, movable to any node; (4) train.run uses x as input AND target, so the zero-code-change design is input = target = transformed volume; (5) r1 launcher is direct-launch (forbidden now) -> sbatch needed; (6) repo split.json is sanitized (h00..h87) -> name FU-A derived subject dirs by the positional token so records carry no pseudonym; (7) ssh to B300 needs -J connectome (configured double jump times out)
- **Unexplored areas**: co-location throughput (smoke pending), cell-target predictability on train subjects (probe pending), venv build off b300-01 (pending)

## Key Decisions Made
- Recommend target = per-cell re-standardised 12 mm cell means, input = target, compact cell store; smoothed BOLD rejected for cost/logistics

## Artifact Index
- verification/explorer_FU_A_r1_2/probe_target_alignment.py (+ .out.json) — alignment/idempotence/compact-source probe, mutant killed
- verification/explorer_FU_A_r1_2/b300_probe_cellmean_predictability.py — B300 CPU probe (train subjects, aggregates only)
- verification/explorer_FU_A_r1_2/b300_smoke_colocate.py — B300 GPU synthetic smoke (co-location)
