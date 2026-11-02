# DISPATCH — reviewer_FU_D_r3_2

## 2026-11-02T04:48:35Z (received from parent coordinator 78a86a60-03cb-452a-896e-fb2a0120898a)

Note: Literal BIDS prefix token in the dispatch constraint notice is written below as `BIDS subject-prefix` to strictly obey the C4 rule against writing that 4-character prefix anywhere in metadata.

You are reviewer_FU_D_r3_2, a Teamwork reviewer in run tw-20261031-four-topics (General route), workflow C.
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/reviewer.md
Runtime adapters: /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else:
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md

Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_FU_D_r3_2/ — write DISPATCH.md, BRIEFING.md, progress.md, handoff.md there. Probes only under /home/juke/git/00IITP-AI/verification/reviewer_FU_D_r3_2/.
Read-only on all production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`). ZERO git writes (`git add`/`commit`/`push` forbidden). Never print or write HCP 6-digit IDs, BIDS subject-prefix strings (even hyphenated English words starting with that prefix), or 16-hex content hashes.
Python: `/home/juke/superclaude-env/bin/python3` with `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`. Run at most 1 pytest process at a time.

Task (Reviewer 2 of 2 for Milestone FU_D_r3):
Independently review correctness and completeness of Milestone FU_D Iteration 3 (`Topic 2 follow-up D: E192 scale (d2-2-18-2), 140k samples, arms E/C/S, 5 seeds (§7 ≈20 GPU-h at 1.36 h/run; cap 25)`) vs ACCEPTANCE C1–C8, the milestone criteria (F1–F3), and the iteration-2 gate failure (`challenger_FU_D_r2_2` B1 and B2 in `.agents/teamwork/tw-20261031-four-topics/challenger_FU_D_r2_2/handoff.md`).
Check `2026-11-02_topic2_fu_d_addendum_02.md` against `verification/worker_FU_D_r3/mutation/union_r3.out.json` and `verification/worker_FU_D_r3/probes/errata_probe.out.json`, verify that B1 and B2 and all r2 verifier / r3 explorer findings are closed with evidence, and re-run tests and receipt/hash checks yourself.
IMPORTANT: When you finish, call `send_message` to your parent coordinator (`78a86a60-03cb-452a-896e-fb2a0120898a`) and output your structured JSON verdict (`APPROVE` or `REQUEST_CHANGES`, `full_report`, `blocking_issues`, `nonblocking_issues`, `commands_run_and_results`, `tested_artifact_sha256`, `uncovered_requirements`).
