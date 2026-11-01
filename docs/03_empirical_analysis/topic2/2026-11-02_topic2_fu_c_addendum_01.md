# Topic 2 FU-C card — addendum 01 (worker_FU_C_r1; written 2026-11-01 ~19:45Z, AFTER all FU-C results)

The frozen card is `2026-11-02_topic2_fu_c_card.md` (sha256 `fc2d0672…4ecb`, frozen 16:13:23Z). It is not edited. This addendum records operational facts and small deviations. **None changes a governed decision, a run, or the verdict** (`results/topic2/2026-11-02_fu_c/verdict.json`: `stop`).

## 1. Timeline (UTC; sacct prints KST, converted)

| event | time | evidence |
|---|---|---|
| environment anchor job 501 (no outcome) | 16:04:53–16:08:23 | `anchor/anchor.json`, ledger |
| card frozen | 16:13:23 | `card_sha256.txt` |
| first Stage-1 submission (job 512, held until its ledger row) | 16:13:51 | `slurm/jobs.json`, ledger |
| verdict code + tests pinned | 16:31:53 | `code_sha256_before_results.txt` |
| first Stage-1 start / last start | 16:35:12 / 19:08:03 | run.json `start_utc` |
| report-table renderer pinned | 16:36:10 | `code_sha256_presentation_before_results.txt` |
| last job closed | 19:38:35 | ledger |
| copy-back of the 24 records (first time any Stage-1 number was read) | 19:39:46 | this addendum; `c4_scan_b300.json` |

## 2. Operational notes and deviations

1. **Rolling submission.** The card's cap rule (§9) was applied per submission. It admitted 8 jobs (wave 1), then 3 (wave 2a), then one job each time a running job closed (13 more). This is the card rule applied as written, not a deviation. Before every submission, `squeue` was checked for `g3t-G-E0-*`: none was PENDING or RUNNING at any submission, so there was no wait. The polls were ≥ 5 min apart (`scripts/topic2fu_c_slurm.py submit`).
2. **Slurm state is not run status.** The sbatch script ends with an `echo`, so Slurm reports COMPLETED even if Python failed. The verdict therefore uses `run.json` `status`, as the card §8 requires. All 24 records have `status: completed` (24/24), so no rerun was needed and no attempt `_a2` exists.
3. **`projected_run_hours` is not visible mid-run.** The frozen `train.run` writes the throughput projection into `run.json` only at the end of the run. During the runs, monitoring used Slurm states and the `status` field only (card §8). No run was aborted by the 0.55 h probe; the wall times were 1,546–1,562 s.
4. **Report renderer pinned separately.** `scripts/topic2fu_c_report_tables.py` (presentation only; it formats `verdict.json` into the report tables) was written after the verdict-code receipt. It got its own receipt at 16:36:10Z, still before any result existed.
5. **Ledger wording.** The closing row of the anchor job (501) and of each Stage-1 job carries a short purpose (`FU-C <run name>`). The full purpose is in the matching `started` row. The ledger is append-only, so the rows were not reworded.
6. **Stalled runs.** Two runs meet the card §6 stall definition: `hcp_C_s16` (test NMSE 1.00000) and `hcp_S_s15` (1.00000). As the card requires, both are **valid runs in the primary analysis**; they were not rerun and not excluded. The stall rate is 2/24 (r1: 1/15). The pre-registered drop-stalled-seed sensitivity (seeds 15 and 16 removed, df 5) gives `stop` as well (descriptive).
7. **C4 copy-back.** Only `run.json`, `train_log.jsonl` and the Slurm output of each run were copied (72 files; the 24 checkpoints stay on B300).
   - On B300, the scan for the 1,084 HCP directory names and the 88 original tokens and content hashes found 0 hits. The scanner was validated on control files beforehand (positive 2/2 detected, negative 0; `verification/worker_FU_C_r1/scan_controls/`).
   - The archive sha256 is `5f3593ef…aec74`; it was verified after transfer.

## 3. Things not done or not checked

- The r1 F+/F− gate was reused by reference, as the card says. It was not rerun.
- Bitwise determinism of the FU-C environment was checked only to step 200 (anchor). The full-run equality to r1 was not re-tested, and nothing depends on it.
- `/scratch/iitp4/explorer_FU_C_r1_2` (explorer leftover, not owned by this worker) still exists on B300.
