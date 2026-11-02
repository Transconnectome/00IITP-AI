# DISPATCH — auditor_FU_D_r3_1

## 2026-11-02T04:48:40Z (received from parent coordinator 78a86a60-03cb-452a-896e-fb2a0120898a)

You are auditor_FU_D_r3_1, a Teamwork auditor in run tw-20261031-four-topics (General route), workflow C.
Role file (read fully and follow): /home/juke/git/chavis/skills/teamwork/references/roles/auditor.md
Runtime adapters: /home/juke/git/chavis/skills/teamwork/references/runtime.md and /home/juke/git/chavis/skills/teamwork/references/claude-code.md
Read before anything else:
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/ORIGINAL_REQUEST.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
- /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md

Metadata dir (yours exclusively): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/auditor_FU_D_r3_1/ — write DISPATCH.md, BRIEFING.md, progress.md, handoff.md there. Probes only under /home/juke/git/00IITP-AI/verification/auditor_FU_D_r3_1/.
Read-only on all production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`). ZERO git writes (`git add`/`commit`/`push` forbidden). Never print or write HCP 6-digit IDs, BIDS `sub-` strings (even hyphenated English words starting with `sub-`), or 16-hex content hashes.
Python: `/home/juke/superclaude-env/bin/python3` with `CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`. Run at most 1 pytest process at a time.

Task (Forensic Auditor for Milestone FU_D_r3):
Forensic integrity audit of Milestone FU_D Iteration 3 (`Topic 2 follow-up D: E192 scale (d2-2-18-2), 140k samples, arms E/C/S, 5 seeds (§7 ≈20 GPU-h at 1.36 h/run; cap 25)`) per your role:
- Check that all frozen / receipt-pinned files (`card_sha256.txt`, `code_sha256_at_freeze.txt`, `output_sha256.txt`, `addendum_01_sha256.txt`, `results/topic2/2026-11-01/code_sha256_at_freeze.txt`, `PROTECTED_HASHES.txt`) are 100% untouched, and that `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt` (102 entries) verifies completely.
- Check `tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py`, `verification/worker_FU_D_r3/mutation/union_r3.out.json`, and `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md` for any hardcoded facades, tests that cannot fail, fabricated mutation records, or C4 participant-ID / BIDS / 16-hex leaks.
- Check C5 GPU ledger (`results/gpu_ledger_2026-10-31.md`: 0 GPU-h used in r3; FU-D total 3.672 GPU-h <= 25 GPU-h cap).
Treat heuristics as leads needing corroboration.
IMPORTANT: When you finish, call `send_message` to your parent coordinator (`78a86a60-03cb-452a-896e-fb2a0120898a`) and output your structured JSON verdict (`CLEAN` or `INTEGRITY_VIOLATION`, `full_report`, `blocking_issues`, `nonblocking_issues`, `commands_run_and_results`, `tested_artifact_sha256`, `uncovered_requirements`).
