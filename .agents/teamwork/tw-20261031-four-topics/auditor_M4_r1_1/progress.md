# progress — auditor_M4_r1_1
Last visited: 2026-11-01T02:41Z
- 02:34Z dispatch received; role/runtime/ORIGINAL_REQUEST/ACCEPTANCE/RESUME/sci-pipeline read; DISPATCH.md, BRIEFING.md written.
- 02:36Z C1 sha256sum -c PROTECTED_HASHES rc 0 (67 lines); card/code/docs/split freeze hashes all OK; frozen code list == current file set.
- 02:37Z tests/topic4_resu 67 passed (26 s); old 86 passed; topic1_lagmotif 88 passed (logs in verification/auditor_M4_r1_1/logs/).
- 02:40Z launched detached independent rerun (tuning+confirm+analyze) on a copy: verification/auditor_M4_r1_1/rerun/ (4 procs, nice, cache in scratchpad).
- Lead under investigation: tuning stage window (ledger 02:04:52Z -> tuning.json 02:05:08Z, elapsed 15.3 s) leaves <=~1.7 s for load_series -> possible pre-existing cache (pre-freeze real-data preprocessing). Needs corroboration.
- 02:41Z rerun tuning reproduced tuning.json exactly (all fields except elapsed_s). Cache-from-scratch took ~1.6 s -> the pre-existing-cache lead is NOT corroborated (timing consistent with fresh build).
- 02:43Z independent recompute (own code, own bootstrap RNG) on production confirm files: points identical, CIs within MC error, verdicts identical, integrity counts identical.
- 02:44Z independent population/split check (own TR lookup via M1 table, own valid_T, own salted-hash rule): manifest matches exactly; burned positions not in primary.
- 02:45Z ID leak scan (full names + distinctive tokens) over 374 M4 files: 0 hits.
- 02:46Z worker transcript (Bash commands only, targeted regex): tuning first invoked 02:04:49Z (after freeze 02:04:41Z), confirm 02:07:42Z; no git writes, no ssh/scp/rsync, no installs, no /scratch or B300 paths.
- 02:47Z gpu_ledger: no M4 rows (M3 explorers only, 0.142 GPU-h total).
Last visited: 2026-11-01T02:55Z
