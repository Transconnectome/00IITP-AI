# Progress — challenger_FU_B_r1_1
Last visited: 2026-11-02T04:06:30Z

- [x] Read role file, runtime adapters, ORIGINAL_REQUEST.md, ACCEPTANCE.md, PI_DECISIONS_2026-11-01.md, GATE_STATUS.md.
- [x] Created DISPATCH.md, BRIEFING.md, progress.md.
- [x] Inspected worker_FU_B_r1 handoff, FU_B card, addendum, result report, verdict.json, scripts, and tests.
- [x] Ran independent recomputation script `p01_v3_recompute_metrics.py` (`rc = 0`): all 18 raw run.json and train_log.jsonl files verified, all FU-B headline metrics and r1_pairing numbers reproduced to machine precision (`max_diff = 0.0`). Identified a non-blocking 5th-decimal-place discrepancy (max diff `6.3e-5`) in the two historical `r1 1x F+ (ref.)` rows of Table 1.1 in `2026-11-02_topic2_fu_b_result_report.md` (where `Fplus_E_s0` val step 8750 `0.67687` was written instead of test NMSE `0.67693`, and 4-decimal rounded r1 numbers were averaged instead of exact r1 seed-mean NMSEs).
- [x] Ran freeze and provenance verification `p03_v2_verify_freeze_and_provenance.py` (`rc = 0`): verified `card_sha256.txt` (28/29 + v1 preserved card exact match), `card_sha256_v2.txt` (31/31), `output_sha256.txt` (50/50), `code_sha256_at_freeze.txt` (33/33), `PROTECTED_HASHES.txt` (67/67), C4 hygiene (0 hits), and strict temporal order (`freeze_v1 16:05:18Z < freeze_v2 16:20:25Z < earliest run start 16:20:41Z`; `latest gate end 18:16:15Z < earliest stage1 start 19:19:08Z`). Also noted a minor non-blocking log formatting quirk in `src/topic2_fu_b/slurm.py` line 36 (`+%%FT%%TZ` unformatted in the `start` echo line of `.sbatch`).
- [x] Completed `p02_adversarial_verdict_and_mutants.py` (`rc = 0`): 19,440 exhaustive boundary cases (0 mismatches), 5 direct adversarial scenario probes (all PASS including `python3 -O`), CLI byte-identical reproduction of `verdict.json`, and 15/15 challenger mutants killed by `tests/topic2_fu_b`.
- [x] Ran pytest on `tests/topic2_fu_b` and `tests/topic2_rgpool` (`244 passed in 134.68s`, `rc = 0`).
- [x] Writing `handoff.md`, running `audit_layout.py`, and reporting to parent `78a86a60-03cb-452a-896e-fb2a0120898a`.
