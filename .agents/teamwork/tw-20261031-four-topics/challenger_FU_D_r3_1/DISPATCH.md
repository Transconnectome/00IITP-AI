# DISPATCH — challenger_FU_D_r3_1

## 2026-11-02T04:48:37Z (received from parent coordinator 78a86a60-03cb-452a-896e-fb2a0120898a)

You are challenger_FU_D_r3_1, a Teamwork challenger in run tw-20261031-four-topics (General route), workflow C.
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/challenger.md
Runtime adapters: /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else:
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md

Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_D_r3_1/ — write DISPATCH.md, BRIEFING.md, progress.md, handoff.md there. Probes only under /home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/.
Read-only on all production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`). ZERO git writes (`git add`/`commit`/`push` forbidden). Never print or write HCP 6-digit IDs, BIDS prefix strings, or 16-hex content hashes.
Python: `/home/juke/superclaude-env/bin/python3` with `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`. Run at most 1 pytest process at a time.

Task (Challenger 1 of 2 for Milestone FU_D_r3):
Empirically try to break Milestone FU_D Iteration 3 (`Topic 2 follow-up D: E192 scale (d2-2-18-2), 140k samples, arms E/C/S, 5 seeds (§7 ≈20 GPU-h at 1.36 h/run; cap 25)`):
1. Independently recompute all FU-D gate statistics (`Fplus_{E,C,S}_s0/run.json` → `verdict.json`) and verify that `inconclusive` (measurement capacity at E192, gains `0.363%` and `0.655% < 1.00%`) holds and matches `2026-11-02_topic2_fu_d_result_report.md` and `addendum_02.md`.
2. Independently test the r2 blocking mutants (`C12`/`CV09`, `CP01`, `CP02`, and siblings) in a temporary copy under `/home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/` (clean up temporary tree copies when done, keeping your probe scripts and JSON outputs) to verify they are genuinely killed by `tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py`.
3. Audit `verification/worker_FU_D_r3/mutation/union_r3.out.json` (1,675 distinct mutants) and the 164-survivor classification in `2026-11-02_topic2_fu_d_addendum_02.md` §5.
IMPORTANT: When you finish, call `send_message` to your parent coordinator (`78a86a60-03cb-452a-896e-fb2a0120898a`) and output your structured JSON verdict (`CONFIRMED` or `REFUTED`, `full_report`, `blocking_issues`, `nonblocking_issues`, `commands_run_and_results`, `tested_artifact_sha256`, `uncovered_requirements`).
