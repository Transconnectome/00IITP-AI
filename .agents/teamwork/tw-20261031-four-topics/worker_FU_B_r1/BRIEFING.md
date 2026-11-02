# BRIEFING — worker_FU_B_r1 (updated 2026-11-01T15:33Z)

## Mission
FU-B: Topic 2 follow-up B — 4x training budget (35000 steps x 16 = 560k samples) at E36, arms E/C/S, 5 seeds, new frozen card, Slurm on B300 b300-01, verdict per card, cap 33 GPU-h.

## 🔒 My Identity
- Archetype: teamwork worker (General route), roles implementer/qa/specialist (implementer primary)
- Host: claude-code (Claude Code subagent of a workflow script; no Agent/SendMessage spawning used); model Opus 5.5
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_FU_B_r1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_B

## 🔒 Key Constraints
- Write only: src/topic2_fu_b/, tests/topic2_fu_b/, scripts/topic2fu_b_*.py, results/topic2/2026-11-02_fu_b/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_*.md, B300 /scratch/iitp4/fu_b/, append-only ledger rows; probes in verification/worker_FU_B_r1/.
- src/topic2_rgpool, tests/topic2_rgpool, scripts/topic2_*.py, r1 results/docs are read-only (frozen; M3 r3 team works there).
- C1 protected hashes; receipts; no IDs/tokens printed or written; no git writes; no installs on DGX-Spark; never read settings.json/secrets; sealed material never copied to repo.
- Every B300 GPU use via sbatch; squeue g3t-G-E0-* guard before every submission; ledger start/close rows under flock; FU-B cap 33 GPU-h (explorers' 0.14 counted).
- Card frozen (sha receipt) before any FU-B real-data run incl. the 4x gate.
- Python local: /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice; <=2 pytest procs, timeout 900.

## Current Parent
- Conversation ID: root 5fddb83e (workflow C). Updated: not yet

## Task Summary
- What to build: card + FU-B verdict/records/budget/view/slurm code + tests; B300 positional view + env; smoke; 4x F+ gate (seed 0, E/C/S); Stage 1 (15 runs); verdict + result report.
- Success criteria: ACCEPTANCE C1–C8, F1–F3; old 86 tests + topic2 suites pass.

## Key Decisions Made
- 4x F+ gate on seed 0 (explorers 1+2); F- inherited from sha-pinned r1 verdict.json (literal True only), only downgrades keep.
- No resume/checkpoints; frozen trainer unchanged; --max-run-hours 2.2, Slurm --time 02:30:00.
- Stage-1 array may be queued afterany the gate; each task recomputes the gate on B300 and skips unless pass.
- Own verdict wiring (src/topic2_fu_b/verdict.py) around frozen stats.py; never scripts/topic2_verdict.py.

## Artifact Index
- docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md — frozen card (v2 receipt card_sha256_v2.txt; v1 receipt card_sha256.txt; addendum_01)
- docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md — final result report
- results/topic2/2026-11-02_fu_b/{verdict.json,gate_4x.json,output_sha256.txt,slurm/jobs.json,b300/runs/*}
- src/topic2_fu_b/{design,records,verdict,budget,view,slurm}.py; scripts/topic2fu_b_{run,make_view,smoke,verdict,slurm,c4scan}.py
- tests/topic2_fu_b/ (128 passing; 44/44 mutants killed in verification/worker_FU_B_r1/mutation/mutants_v2.out.json)
- verification/worker_FU_B_r1/stage_v1 (+ sha lists) — code bundle copied to B300
- B300 /scratch/iitp4/fu_b/{venv,code,in,hcp/subjects(hNN hard links),view_check.json,c4_scan_b300.json,runs}

## Change Tracker
- Files modified: only new files in owned paths.
- Build status: tests/topic2_fu_b + tests/topic2_rgpool 244 passed; old 86 passed; C1 PROTECTED_HASHES 67/67 OK.
- Pending: none (complete; verdict STOP).

## Quality Status
- Build/test result: pass (2026-11-02T03:45Z).
- Tests added: design/pins, records, verdict precedence/boundaries/r1 reproduction, budget/share rule, slurm/view/wrapper (128 tests, 44/44 mutants killed).

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (methodology: frozen card before results, synthetic ground truth, run records, verdict taxonomy). Not copied locally (read in place; deviation: the role asks for a local dump).
