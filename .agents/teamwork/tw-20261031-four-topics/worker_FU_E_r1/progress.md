# progress — worker_FU_E_r1
Last visited: 2026-11-01T15:25Z
- 15:16Z read role, adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addenda), PI decisions, GATE_STATUS, RESUME, r1 card/report/addendum 04, r1 code, explorer handoffs
- 15:18Z B300 check: 15/15 checkpoints present (156,184,449 B each); squeue empty; sinfo idle
- 15:24Z DISPATCH.md written
- 15:28Z ssh control master to b300-01 (flaky proxy); r1 tree inspected (counts only): 88 subject dirs, split 64/8/16, perms/split sha equal repo/sealed pins
- 15:36Z 15 checkpoint sha256 recomputed on B300 = explorer_FU_E_r1_1 values; pins file written
- 15:33Z src/topic2_fu_e (prep, readout, ident, synth, provenance, pipeline, verdict) + scripts topic2fu_e_extract.py / topic2fu_e_verdict.py written
- 15:38Z tiny-config CPU synthetic probe (verification/worker_FU_E_r1/cpu/probe_tiny_fixtures.out): F+ cov2 Idiff ~12 > null; F- common-mask ~-0.6; F- subject-mask mutant ~48 (confound). F- gate changed to one-sided vs null p95 (before freeze)
- 15:45Z tests/topic2_fu_e 72 passed; verdict mutants 29/29 killed (verification/worker_FU_E_r1/mutants/mutants_v2.json)
Last visited: 2026-11-01T15:46Z (times approximate to the minute)
- 15:56Z smoke job 499 submitted (synthetic only). DEVIATION: the pre-submit g3t-G-E0 squeue check in that command chain failed (ssh broken pipe) and the chain still submitted; sacct later showed no g3t-G-E0 job since 23:00 KST, so no conflict occurred. Main submission made idempotent with the g3t check inside the same remote command.
- 16:04Z job 499 COMPLETED (8 s, 0.003 GPU-h; ledger closed)
- 16:22:56Z CARD FROZEN: results/topic2/2026-11-02_fu_e/card_sha256.txt (card 072553b0…); code receipt 18 files
- 16:24:31Z g3t-G-E0 check none; main job 524 submitted (gpu partition, b300-01, 75 min); ledger start row written
Last visited: 2026-11-01T16:36Z
- 16:37Z job 524 PENDING (QOSMaxGRESPerUser: 8/8 user GPUs in use; FU-C jobs 513-520 queued earlier). Waiting is not a failure (C5 share rule).
- 17:04Z job 524 RUNNING on b300-01 (waited 40 min in queue: QOSMaxGRESPerUser)
- 17:20:40Z job 524 COMPLETED (1003 s, 0.279 GPU-h; ledger closed). FU-E total 0.297 GPU-h incl. explorers
- 17:3xZ verdict.json (frozen script, reproduced byte-identically): INCONCLUSIVE — synthetic F+ failed on S_s2 (5.76 <= p95 10.59); F-, G2, G3, G0 pass; J1 [-0.066, +0.228], J2 [+0.098, +0.202] (not governed)
- B300 ID scans (r1 script, 1084 names in memory): 45 then 47 files, 0 hits (results/topic2/2026-11-02_fu_e/id_scan_b300.json)
- result report docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_result_report.md; output_sha256.txt 12 lines OK
- final: tests/topic2_fu_e 71 passed; old 86 passed; tests/topic2_rgpool 116 passed; C1 0 non-OK; receipts OK; layout lint 0 findings
Last visited: 2026-11-01T17:50Z (approx)
