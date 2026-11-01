# progress — victory_M4

- 03:18Z started; read role, runtime adapters, ORIGINAL_REQUEST, ACCEPTANCE, RESUME, sci-pipeline SKILL, card, T4.1 diagnosis, result report, addendum_01.
- 03:19Z C1 `sha256sum -c PROTECTED_HASHES.txt` rc 0 (67/67 OK). Card sha 2b535c39…5934 matches card_sha256.txt. `code_sha256_at_freeze.txt` all OK (35 entries; file list equals current src/topic4_resu, tests/topic4_resu, scripts/topic4_*).
- 03:20Z launched detached independent rerun (tuning → confirm --procs 3 → analyze) into verification/victory_M4/rerun with a fresh cache in scratchpad (deleted by the driver at end). Tuning reproduced identically (identity 0.1455351933281345, persistence −0.3084737703364419, η0 0.02).
- Code read: psp.py, diagnostics.py, pipeline.py, metrics.py, stats.py, split.py, topologies.py, data.py, baselines, topic4_run.py, topic4_analyze.py, build_split; all tests in tests/topic4_resu. Card §4–§6 rules match code.
- output_sha256.txt: 72/73 OK; logs/analyze.log mismatch = recorded empty-file hash (log written by the analyze process's own stdout after hashing; benign). docs_sha256.txt 13/13 OK. Ledger output_sha256 55/55 match.
- Pre-freeze real-data access sweep: only explorer probes on burned positions 0 and 932 (TR 1.8 / 1.0); worker probes and smoke synthetic; no other tuning/ledger on real data before 02:04:41Z.
- PI_DECISIONS: δ = 0.01 confirmed for M4 (report/addendum "pending" wording is stale).
- Pending: rerun completion + byte/numeric diff; pytest (old 86, topic1_lagmotif, topic4_resu); adapted mutant harness (18 original + 8 own); mask checks; T4.1 counterfactual rerun + positions 0–9 padding counts; ID scan.
