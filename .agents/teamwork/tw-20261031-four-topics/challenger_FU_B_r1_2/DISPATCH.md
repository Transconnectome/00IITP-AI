# Dispatch Log — challenger_FU_B_r1_2

## 2026-11-02T03:49:26Z

Sender: 78a86a60-03cb-452a-896e-fb2a0120898a

You are challenger_FU_B_r1_2, a Teamwork challenger in run tw-20261031-four-topics (General route), workflow C.
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/challenger.md
Runtime adapters: /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else:
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md

Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/challenger_FU_B_r1_2/ — write DISPATCH.md, BRIEFING.md, progress.md, handoff.md there. Probes only under /home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_2/.
Read-only on all production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`). ZERO git writes (`git add`/`commit`/`push` forbidden). Never print or write HCP 6-digit IDs, BIDS subject-prefix strings, or 16-hex content hashes.
Python: `/home/juke/superclaude-env/bin/python3` with `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`. Run at most 1 pytest process at a time.

Task (Challenger 2 of 2 for Milestone FU_B_r1):
Empirically try to break Milestone FU_B (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds (§7 ≈26 GPU-h; cap 33)`):
1. Verify mutation coverage (`verification/worker_FU_B_r1/mutation/mutants_v2.out.json`) and test your own adversarial probes/mutants in a copied tree under `/home/juke/git/00IITP-AI/verification/challenger_FU_B_r1_2/` against `src/topic2_fu_b/` and `tests/topic2_fu_b/` (clean up any large temporary tree copies when done, keeping your probe script and JSON output).
2. Check B300 provenance (`b300/view_check.json`, `b300/c4_scan_b300.json`, `slurm/jobs.json`, `b300/runs/*/train_log.jsonl`) and verify that every Stage-1 and gate run actually ran 35,000 steps with batch 16, warmup 1,750, cosine decay to 35,000, and matching code/partition/split hashes.
3. Recompute verdict from raw records and verify that the verdict follows the frozen card's rules.
Return `CONFIRMED` if it holds or `REFUTED` with evidence in a structured JSON-compatible summary (`verdict`, `full_report`, `blocking_issues`, `nonblocking_issues`, `commands_run_and_results`, `tested_artifact_sha256`, `uncovered_requirements`).
