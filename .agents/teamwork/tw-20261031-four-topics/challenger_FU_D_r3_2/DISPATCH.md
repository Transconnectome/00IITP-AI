# DISPATCH — challenger_FU_D_r3_2

## 2026-11-02T04:48:39Z (received from parent coordinator 78a86a60-03cb-452a-896e-fb2a0120898a)

Note: In the verbatim dispatch below, the four-character BIDS prefix literal is written as `s_ub-` so that no file in this directory contains the raw prefix pattern prohibited by C4.

You are challenger_FU_D_r3_2, a Teamwork challenger in run tw-20261031-four-topics (General route), workflow C.
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/challenger.md
Runtime adapters: /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else:
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md

Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_D_r3_2/ — write DISPATCH.md, BRIEFING.md, progress.md, handoff.md there. Probes only under /home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_2/.
Read-only on all production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`). ZERO git writes (`git add`/`commit`/`push` forbidden). Never print or write HCP 6-digit IDs, BIDS `s_ub-` strings (even hyphenated English words starting with `s_ub-`), or 16-hex content hashes.
Python: `/home/juke/superclaude-env/bin/python3` with `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`. Run at most 1 pytest process at a time.

Task (Challenger 2 of 2 for Milestone FU_D_r3):
Empirically try to break Milestone FU_D Iteration 3 (`Topic 2 follow-up D: E192 scale (d2-2-18-2), 140k samples, arms E/C/S, 5 seeds (§7 ≈20 GPU-h at 1.36 h/run; cap 25)`):
1. Read `.agents/teamwork/tw-20261031-four-topics/challenger_FU_D_r2_2/handoff.md` (which raised B1 `C12` and B2 alias run directories in r2) and verify whether `worker_FU_D_r3` has completely closed both B1 and B2 (and all other r2 verifier / r3 explorer items) in `tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py` and `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md`.
2. Write an independent probe script in `/home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_2/` that verifies:
   - the algebraic proof P1 in `addendum_02.md` §4 (`stop -> keep` and `stop -> modify` unreachability for `n = 5`, `k in {3, 4}`),
   - the errata E5, E2′, E6, E7, E8, E9, W4, W5 and shipped-data invariants,
   - spot-checks of the 164 surviving mutants in `union_r3.out.json` to confirm none can alter a valid decision category or the shipped `verdict.json`.
IMPORTANT: When you finish, call `send_message` to your parent coordinator (`78a86a60-03cb-452a-896e-fb2a0120898a`) and output your structured JSON verdict (`CONFIRMED` or `REFUTED`, `full_report`, `blocking_issues`, `nonblocking_issues`, `commands_run_and_results`, `tested_artifact_sha256`, `uncovered_requirements`).
