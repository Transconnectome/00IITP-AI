# Topic 3 addendum 05: M2 iteration 3 — guard tests for the blocking classes of the r2b gate, union mutation run, corrections to addenda 03/04 and the report (2026-11-01)

Written 2026-11-01 (UTC) by worker_M2_r3, the iteration-3 worker of M2. Iteration 3 was approved by the PI on 2026-11-01 (`.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md`, decision 1). This addendum is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report and addenda 01–04 are unchanged. They stay pinned in `results/topic3/2026-10-31/output_sha256.txt` and `addendum_02/03/04_sha256.txt`, and all four receipts verify (§7). The sha256 of this file and of the two new test files is in `results/topic3/2026-10-31/addendum_05_sha256.txt`.

**No verdict changes.**
- No file in `src/` or `scripts/` was changed. No card was re-frozen. No new real-data estimand was computed.
- No real-data analysis was rerun to produce a result. One new test re-derives the pinned Family B output inside pytest's temporary directory and compares it with the pinned file (§2, class 5). Its output is discarded with the temporary directory; nothing is written to the production tree.
- The verdicts in report §4 stand: H1a holds, H1b not replicated, D1 robust and not a per-channel-scale effect, D3 ordering reproduces, J1 artefact, H2 untested.

[[SECTIONS]]
