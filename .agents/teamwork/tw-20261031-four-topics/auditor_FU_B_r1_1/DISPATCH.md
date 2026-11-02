# DISPATCH — auditor_FU_B_r1_1

## 2026-11-02T03:49:28Z (received from parent 78a86a60-03cb-452a-896e-fb2a0120898a; note: literal four-character BIDS prefix in the prohibition clause is written as `<bids-prefix>` below to strictly honor the rule against writing that four-character string)

You are auditor_FU_B_r1_1, a Teamwork auditor in run tw-20261031-four-topics (General route), workflow C.
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/auditor.md
Runtime adapters: /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else:
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md

Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/auditor_FU_B_r1_1/ — write DISPATCH.md, BRIEFING.md, progress.md, handoff.md there. Probes only under /home/juke/git/00IITP-AI/verification/auditor_FU_B_r1_1/.
Read-only on all production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`). ZERO git writes (`git add`/`commit`/`push` forbidden). Never print or write HCP 6-digit IDs, BIDS `<bids-prefix>` strings (even hyphenated English words starting with `<bids-prefix>`), or 16-hex content hashes.
Python: `/home/juke/superclaude-env/bin/python3` with `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`. Run at most 1 pytest process at a time.

Task (Forensic Auditor for Milestone FU_B_r1):
Forensic integrity audit of Milestone FU_B (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds (§7 ≈26 GPU-h; cap 33)`) per your role:
- Check for hardcoded results, facades, tests that cannot fail, fabricated/non-reproducible logs, results computed before card freeze (`2026-11-01T16:05:18Z` v1 / `16:20:25Z` v2 vs Slurm job 509 start `16:20:41Z` and job 516 start `17:58:26Z`), silent fallbacks.
- Check participant-ID leakage (C4: positional `hNN` tokens only, no 6-digit HCP IDs, no BIDS `<bids-prefix>` labels, no 16-hex content hashes in `results/topic2/2026-11-02_fu_b/` or `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_*.md`).
- Check writes to protected/pinned/external paths (`PROTECTED_HASHES.txt`, `results/topic2/2026-11-01/code_sha256_at_freeze.txt`, `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt`, `output_sha256.txt`).
- Check C5 GPU ledger accounting (`results/gpu_ledger_2026-10-31.md`: all FU-B jobs `413`, `402`, `419`, `490`, `509_0..2`, `516_0..14` via Slurm `sbatch`, total `30.72 GPU-h <= 33.0 GPU-h` cap, project-local venv under `/scratch/iitp4/fu_b/`).
Treat heuristics as leads needing corroboration. Return `CLEAN` or `INTEGRITY_VIOLATION` with evidence in a structured JSON-compatible summary (`verdict`, `full_report`, `blocking_issues`, `nonblocking_issues`, `commands_run_and_results`, `tested_artifact_sha256`, `uncovered_requirements`).
