# progress — worker_M3_r2
Last visited: 2026-11-01T09:09:37Z
- 07:15Z DISPATCH.md written byte-for-byte from own transcript (count scan: 1 six-digit = 48^3 constant, 4 hex16 = float digits).
- 07:20Z read role/runtime/adapter, ORIGINAL_REQUEST, ACCEPTANCE, orchestrator (no R1/R2 ruling, no durable sealed dir), explorer r2 handoffs, code.
- 07:24Z advisor consulted: R1 positional, fail-closed sequence (preflight -> seal -> sanitize in scratch -> verify -> replace).
- 07:21Z preflight: C1 67/67 rc0; card pins 8/8; output pins 43/43; code freeze 33/33; PROTECTED_HASHES has 0 topic2 lines.
- 07:27Z C4 incident (own): a structure probe of logs/preprocess.log masked digits BEFORE hex runs, so one masked line
  showed the letter positions (6 of 16 chars) of one pseudonym in local tool output. Not written to any file. Disclose.
- 07:28Z sealed 19 originals to B300 .98 /scratch/iitp4/worker_M3_r2/sealed_c4 (19/19 sha OK, 18/18 old-pin lines OK).
- 07:30Z sanitized copies in scratchpad: frozen verdict script -> verdict.json byte-identical (59af05e5); frozen 55 tests pass on mirror.
- 07:31Z positive-control token scan (count only): exactly the 19 files + 3 Topic-4 numeric coincidences; pattern detector exactly 19 files.
- 07:33Z replaced 19 files in repo (os.replace); new pins c4_sealed_originals_sha256.txt, c4_sanitized_sha256.txt; seal_check repo mode all_ok.
- 07:39Z sealed-mode check on B300 (system python3, stdlib): S1-S5 all OK (19/19, 18/18, resanitize 19/19, provenance, split 64/8/16).
- 07:45Z new tests: test_c4_tokens_r2.py (8), test_verdict_path_guards_r2.py (10), test_pipeline_guards_r2.py (18) all pass on frozen code.
- 07:51Z local mutation run v1 INVALID: host memory ~91%, earlyoom SIGTERM (rc -15) incl. baseline; stopped by PID; kept in mutation/v1_local_earlyoom/.
- 08:05Z B300 venv: verdict bytes differ only in scipy t quantile (<=9e-13 rel, scipy 1.18 vs 1.15) -> shipped-verdict test compares numbers to 1e-9.
- 08:14Z mutation run v2 on B300 .98 CPU (6 jobs, CUDA hidden, pytest 8.4.2 in /scratch/iitp4/worker_M3_r2/pydeps).
- 08:25Z m18 (build_boxes default algo) survived v2 -> added test_build_boxes_default_is_the_deterministic_dense_mean_rule (kills it locally).
- 08:27Z git history scan: 176 patterns fed, 50 revisions, 0 hits (rc 1); positive control 33 hits.
- 08:28Z addendum_05 drafted (docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_05.md).
- 08:35Z B300 v3: baseline 92 passed, m18 KILLED -> 102/102 mutants killed overall.
- 08:40-09:05Z local topic2 suite killed by earlyoom 3x (host memory, other workloads; journal kept); old 86 passed; topic1_lagmotif 88 passed.
- 08:45Z frozen verdict script on repo runs -> verdict.json + stdout byte-identical (local env).
- 08:52Z output_sha256_r2.txt (156 lines) written; seal_check repo all_ok (R1-R5); audit_layout PASS 249 files; C1 67/67; freeze 33/33.
- 09:01Z final B300 CPU run on final bundle: 92 passed; frozen ID scan 1084 names, 193 files, 0 hits; B300 code = repo.
- 09:06Z scratchpad removed; B300 stale copies removed (sealed_c4, check, final, mutout, pydeps kept); no leftover processes.
