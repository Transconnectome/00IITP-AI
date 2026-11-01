# progress — explorer_M3_r3_2
Last visited: 2026-11-01T14:19Z
- 14:18Z read adapters, role, ORIGINAL_REQUEST, ACCEPTANCE (+addendum), PI_DECISIONS 1–8, GATE_STATUS, RESUME; r2 gate record (challenger_M3_r2_2 full); challenger p05/p06/p07; frozen stats.py + topic2_verdict.py; existing verdict tests; card §7–§8.
- next: baseline checks (C1, receipts), salt-containment scan, probe tests + local mutant matrix.
Last visited: 2026-11-01T14:27Z
- 14:20Z baseline: C1 67/67 rc0; code freeze 33/33; output_sha256_r2 156/156; c4_sanitized 19/19; c4_sealed_originals 19/19 against root's durable sealed copy (fails in repo by design); old card_sha256 2 / output_sha256 16 fail exactly on the disclosed sanitized files.
- 14:21Z s01 salt containment (counts only): salt file sha == root record; salt/head12/tail12 0 hits in 17,667 worktree files and 0/1,568 git blobs (all objects); 5 hashes only in 3 files of verification/explorer_M3_r1_1; 0/5 recoverable without the sealed salt.
- 14:25Z m02: shipped verdict.json byte-identical under baseline + V01-V11 (stop).
- 14:22Z m01 attributable-kill matrix running (detached).
- Found: FU teams write docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_*.md, which the shipped C4 scanners (test_c4_tokens_r2, test_outputs_no_ids) scan -> cross-team failure mode.
Last visited: 2026-11-01T14:45Z
- 14:31Z m01 v1 done: V01-V11 A SURVIVED / B KILLED, each attributed.
- 14:36Z m03 sweep: W04-W08, W12 survived shipped+proposed -> 6 guards added -> only W09 (equivalent, proof) survives.
- 14:40Z m01 v2 with the extended file (20 tests): V01-V11 attribution unchanged; baseline 14/20 pass.
- 14:42Z draft addendum_06 passes the shipped C4 scanners; old 86 passed; C1 rc0; pins unchanged; audit_layout rc0; work dir removed; no procs.
- 14:45Z handoff.md written (Hard). DONE.
