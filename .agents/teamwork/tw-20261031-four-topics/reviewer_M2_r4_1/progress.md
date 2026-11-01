# progress — reviewer_M2_r4_1

Last visited: 2026-11-01T12:31Z

- 12:25Z dispatch received; DISPATCH.md written.
- 12:25-12:30Z read role/runtime/adapters, ORIGINAL_REQUEST, ACCEPTANCE, RESUME, PI_DECISIONS, GATE_STATUS, r3 gate record, worker handoff, both r4 test files, analysis.py, token_job.py, subject-level scripts, helpers.py, the 4 r3 harness files (26 mutant triples).
- 12:30Z advisor consulted; BRIEFING.md written; pyc baseline taken (verification/reviewer_M2_r4_1/baseline/pyc_listing_start.txt).
- 12:31Z additivity: all 33 tests/topic3_spectral, src/topic3_spectral, scripts/topic3_* files pinned by a receipt; C1 67/67 OK; receipts output 42 / ad02 1 / ad03 3 / ad04 2 / ad05 3 / ad06 3 OK (logs/*_pre.log); code_sha256_at_freeze differs only for scripts/topic3_launch_connectome.py (addendum 01 item 2 discloses).
- 12:33Z built tree_base (171 files, byte-identical manifest, no __pycache__); wrote bin/run_mutants.py (own AST extraction from the 4 r3 harness files; 26 ids, 21 unique patched files, each old occurs once).
- 12:34Z launched runs/R4_named (control + 26 mutants, suite = 2 r4 files, 2 concurrent). Control 17/17 OK.
- 12:36Z worker evidence manifest 657/657 OK; spot-checked N001/N012/N022/N024 records: junit + log hashes match, failing lists match raw junit.
Last visited: 2026-11-01T12:38Z
- 12:40:30Z R4_named finished: CONTROL_OK (17/17) + 26/26 KILLED, every kill in-class only, 0 out-of-class failures, 0 skips (real-data test ran in all), import of patched bytes verified per job. FA11 killed by the synthetic class (a) test only (as designed). VA01/VA02 fail exactly the corr-only stub case + the computed witness.
- 12:41Z probe probes/witness_numbers.py reproduces worker numbers: (c) H1a raw=Holm 0.0380, H1b 0.0347, Bonferroni 0.076/0.069, CI lo ~0.00062, verdict holds; (d) cov [-2.942,-1.660], corr [+13.877,+15.440] -> drop not robust.
- 12:41-12:42:38Z prod checks (bin/prod_checks.sh prod1): topic3 138 passed 0 skipped; old suite 86; topic1 88; C1 67 OK; receipts 42/1/3/2/3/3 OK; pyc listing unchanged vs baseline.
- 12:44Z runner v1 bytes preserved (bin/run_mutants_v1_used_for_R4_named.py, 13774d60…); v2 adds own-process-group cleanup (fd58777f…). Launched SHIPPED_named (control + 26, shipped 121 tests).
- 12:45Z BIDS scan of own outputs: no hits outside the byte copy of the shipped driver test (synthetic SYN names). Layout lint PASS (276 files, no findings).
Last visited: 2026-11-01T12:46Z
