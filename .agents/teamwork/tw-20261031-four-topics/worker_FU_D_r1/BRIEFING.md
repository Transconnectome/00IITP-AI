# BRIEFING — 2026-11-01T19:26Z

## Mission
FU_D: Topic 2 follow-up D — SwiFT ver11 E192 (d2-2-18-2) at the r1 budget (140k samples), arms E/C/S, new dated
frozen card, own code/tests/verdict, Slurm runs on B300 within the 25 GPU-h cap, result report.

## 🔒 My Identity
- Archetype: worker (implementer + qa + specialist), General route, workflow C
- Roles: implementer, qa, specialist
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_FU_D_r1/
- Original parent: root coordinator, Claude session 5fddb83e
- Milestone: FU_D

## 🔒 Key Constraints
- Own paths only: src/topic2_fu_d/, tests/topic2_fu_d/, scripts/topic2fu_d_*.py, results/topic2/2026-11-02_fu_d/,
  docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_*.md, B300 /scratch/iitp4/fu_d/, append-only ledger rows.
- Probes only under verification/worker_FU_D_r1/. Metadata only here.
- src/topic2_rgpool and scripts/topic2_*.py frozen (code_sha256_at_freeze.txt); import, never edit.
- Card frozen (sha256 receipt) BEFORE any FU_D real-data result. Deviations → dated addendum.
- C1 protected hashes; all *_sha256.txt receipts must stay OK. No git writes. No installs on DGX-Spark.
- C4: no participant IDs/tokens printed or written; positional hNN only; sealed material never copied to repo.
- B300: every GPU use via sbatch/srun, --nodelist=b300-01 (HCP only there); squeue check for g3t-G-E0-* before
  EVERY submission (if PD/R: wait ≥5 min, log in progress.md); whole Slurm user ≤ 8 GPUs; never cancel others' jobs.
- Ledger: started + completed rows under flock (scripts/topic2_ledger.py --agent worker_FU_D_r1), GPU-h from sacct
  (sacct prints KST → convert to UTC).
- FU-D cap 25 GPU-h; run ceiling 95. Job that would exceed cap is not launched.
- Local python: PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice; ≤2 concurrent pytest, timeout 900.

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Task Summary
- What to build: card + E192 wrapper + positional view + seed plan + verdict code + Slurm launcher + tests; run F+ gate
  (E/C/S seed 0), seed plan, Stage 1 (3n runs), conditional F−; verdict; report.
- Success: ACCEPTANCE C1–C8, F1–F3.

## Key Decisions Made
- Design per explorer consensus: single change = model scale E36→E192; r1 §5 hyperparameters verbatim; r1 perms
  byte-identical; reduced gate (F+ seed 0, 3 runs); cost-only seed rule n∈{5,4} else not run; conditional F− (E,C s0)
  only for would-be keep; own verdict code with tri-state gates; positional hard-link view on b300-01.
- Own venv /scratch/iitp4/fu_d/venv from r1 lock (freeze identical).
- Card + code frozen 16:06:07Z (card sha 1b7fee6c…001b; 29 code files). Mutants 62/62 killed pre-freeze.
- Positional hard-link view /scratch/iitp4/fu_d/hcp (88 subj, 176 links, same inode).
- Order: smoke job (equiv + HCP cost) -> F+ gate (3 jobs) -> seed_plan.json -> Stage 1 (3n) -> F- if would-be keep -> verdict -> report.
- QoS: whole Slurm user capped at 8 GPUs; queue is crowded (FU-A/B/C, GARD, t3).
- OUTCOME: F+ gate failed at E192 (+0.36% / +0.65% < 1%) -> verdict inconclusive (measurement capacity); Stage 1 not run; 3.672 GPU-h FU-D total. Handoff written.

## Artifact Index
- DISPATCH.md — assignment verbatim
- progress.md — heartbeat
- handoff.md — final report (Hard, written)
- docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_{card,result_report}.md
- results/topic2/2026-11-02_fu_d/ (receipts, runs, verdict.json, logs)

## Change Tracker
- Files created: src/topic2_fu_d/* (8), scripts/topic2fu_d_*.py (9), tests/topic2_fu_d/* (11), card, results/topic2/2026-11-02_fu_d/{card_sha256.txt,code_sha256_at_freeze.txt,logs/}
- Build status: FU-D 129 passed; old 86 passed; C1 rc 0
- Pending issues: none

## Quality Status
- Build/test result: FU-D 129 passed; old 86 passed; C1 rc 0
- Lint status: layout lint findings []
- Tests added/modified: tests/topic2_fu_d (11 files); mutants 62/62 killed

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (methodology; frozen card before results, fixtures, run
  records, verdict taxonomy). Local copy: not dumped (read in place).
