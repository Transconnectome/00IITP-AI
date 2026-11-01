# handoff — challenger_M3_r3_2 (M3 / Topic 2 r3 gate, T2.4) — Hard handoff
Written 2026-11-01T17:5xZ. Verdict: **CONFIRMED** (worker_M3_r3's T2.4 claims hold under independent re-execution).
Evidence dir: /home/juke/git/00IITP-AI/verification/challenger_M3_r3_2/ (c00–c08, prev_versions/). 0 GPU-h; all CPU, local DGX-Spark, at most 2 concurrent pytest.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0 (start and end of my run). Receipts: addendum_06 31/31, code_sha256_at_freeze 33/33, output_sha256_r2 156/156, c4_sanitized 19/19; old card_sha256 fails exactly hcp_manifest.json + split.json, old output_sha256 fails exactly stage0_hcp.json + the 15 hcp run.json (the disclosed set).
- Frozen script rerun on shipped runs: output byte-identical to results/topic2/2026-11-01/verdict.json (sha 59af05e5…af68), verdict stop.
- c03 (independent recomputation from raw run.json, no project imports): 27 files / 27 keys, all completed, 1 test order over 15 hcp runs, 16 test subjects; test_nmse == Σnum/Σden exactly. I1 mean +0.1468 %, t95 [−0.0677 %, +0.3614 %]; I2 mean +0.4733 %, t95 [+0.00098 %, +0.9455 %]; F+ gains 3.061 % / 2.935 %; F− gain C vs E −1.737 %. Max abs diff vs verdict.json = 0.0. Independent card coding → stop.
- Card freeze: card_sha256.txt header 2026-11-01T03:14:34Z, card sha c9bfc60a…41f5 unchanged; first run start 03:16:17Z; last F+ end 03:42:08Z; first hcp start 03:44:51Z; last F− end 04:10:11Z.
- c01 (own harness, own mirror with results/docs COPIED, not symlinked; V01–V11 read verbatim from verification/challenger_M3_r2_2/p07_specs.json): new file alone — baseline 24 passed; **V01–V11 all KILLED**, each by the tests named in addendum_06 §4.
- c00/c01/c02: 20 novel mutants N01–N20 (not in the worker's 24 specs: I2 CI from I1, I2 vs E, default δ 2 %, F+ gate `or` / C-vs-E-only, one-sided t, ddof 0, FIX_SEEDS (0,), swapped fp/fm, hcp need without S, verdict(ci2, ci1), fm from F+, stop `<=`, modify without lo>0, order check E-only, F− gate as not-F+, g_cs with E denominator, stop on mean, F− downgrade dropped, keep needs I2 mean ≥ δ). New file alone kills 10; the other 10 are killed by the union suite (shipped 12 + new). **0 survivors of 20.**
- Union baseline (13 test files, FU cards of other teams excluded from the docs copy): 116 passed. First baseline attempt and the N11 attempt returned rc −15 (SIGTERM from outside, likely the host memory guard; free RAM was ~35 GB); recorded INVALID and rerun: baseline 116 passed, N11 KILLED.
- W09 (worker: equivalent): t_interval gives hi = m + q·se with q > 0, se ≥ 0, and float addition of a non-negative number never decreases m, so hi ≥ m; hi < δ ⇒ m < δ ⇒ I1_survives false. NaN makes both conditions false. Equivalence holds on every t_interval output; I agree.
- c04 (frozen script, synthetic records): E1 confirmed (F+ failed, no hcp runs → no_verdict "Stage 1 incomplete"); E5 confirmed (mis-ordered test list: plain rc 1 with the assert message; `python -O` rc 0 and verdict keep); E4 confirmed (duplicate key completed vs failed: verdict follows whichever record glob lists last, 4/4 layouts).
- c06 (independent card coding of §5/§7.2/§8, strict E3): 27 scenarios, 12 differ from the frozen label (E1 2, E2 6, E3 4) — same as addendum_06 §2.6.
- c05 (salt containment, counts only): sealed salt sha matches root's record; modes 0400/0700/0700; not in a git work tree; old repo path gone. 6 salt variants: 0 hits in 19,978 working-tree files (2.33 GB) and 0 in 1,786 git blobs (3,330 objects). Positive control 5/5. Burned hashes in 3 working-tree files. Unsalted / public-salt schemes recover 0/5. 0 six-digit names whose hash window (any of the 49 windows of sha256(name); prefix/suffix of 5 other schemes) occurs among 2,472,462 distinct 16-hex windows in the tree and blobs.
- c05b/c05c (new; the worker said a plain-text scan "needs the B300 listing" — for the 5 dev IDs it does not, the sealed salt suffices): every standalone 6-digit token of the tree and blobs hashed with the frozen burned scheme. Hits: 3 dev IDs in the working tree, 1 in blobs. Attribution (contexts with every 6-digit token masked): **0 hits in any M3-owned file** (addendum_06, test_verdict_path_guards_r3.py, verification/worker_M3_r3/). Non-coincidental: verification/challenger_M3_r3_1/p06_c4_scan_r3_outputs.py (as an "HCP range" bound) and tests/topic2_fu_c/test_gate_and_records.py (as a "real-token shape" pseudonym). Coincidental numbers: results/topic1/2026-10-31/extract_primary.jsonl (float null means) and a proposal PDF (PDF object numbers; also the 1 blob hit).
- Regression: tests/topic1_lagmotif 88 passed. Old 86 (STRICT_E2E=1): 85 passed + 1 failed without PYTHONPATH (test_pilot_python_module_cli_execution: `ModuleNotFoundError: No module named 'src'` in a subprocess); 86 passed with PYTHONPATH=repo root. That is an environment dependency of an old protected test, not an M3 change.
- Full tests/topic2_rgpool in the real repo with the current docs dir: **116 passed**, rc 0 (c08). The worker's open issue (FU-B card turns test_outputs_no_ids red) no longer reproduces: the FU-B card was rewritten at 01:20 KST, after the worker's run.
- Whole-run audit_layout.py: PASS, rc 0, 0 findings (405 files).
- GPU ledger: no row for worker_M3_r3, which matches its 0 GPU-h claim.

## 2. Logic Chain
1. T2.4(a) asks that new tests kill V01–V11 or prove a mutant equivalent. My own harness, with specs read verbatim from the upstream challenger file, kills all 11 using the new file alone (c01). Satisfied.
2. The worker's extra set (K1, K2, W04–W08, W12) and W09: I re-derived the W09 equivalence (§1). For robustness beyond the enumerated set, 20 new verdict-path mutants were all killed by the union suite (c02/c02b). No gap found in the verdict path.
3. T2.4(b) asks for the card-vs-code erratum in an addendum. E1 holds as stated (c04), and the 27-scenario table reproduces (c06). E4 and E5 hold (c04). The script and card are unchanged (receipts).
4. T2.4(c) asks to confirm dev-salt containment. The salted-hash channel is closed: c05 independently gives 0 salt hits, 0/5 recovered without the salt, and 0 hash-window hits. M3-owned files hold no plaintext dev ID (c05c). Literal dev-ID tokens do exist in two files from other teams (c05c). Neither file labels the token as a dev subject, so these are not a salted-hash recovery route.
5. No regression: C1 rc 0, all receipts, topic1 88, old 86 (with PYTHONPATH), full topic2 116 in the real repo, layout PASS. The shipped verdict reproduces byte-identically, and my independent recomputation gives the same numbers and stop.
6. So the worker's T2.4 claims hold → CONFIRMED.

## 3. Caveats
- Mutation testing covers the 11 + 20 mutants I ran (plus the worker's set, which I did not rerun one by one except V01–V11). It does not prove that every possible mutant is killed.
- Model/training-loop tests in the union run with CUDA hidden. GPU-visible skips in test_pipeline_guards_r2 (carried-forward note) were not exercised.
- I did not rerun the worker's connectome legs A/C. My union legs ran locally, on the same code (sha-pinned receipts OK).
- Positional residual ("positions 0-4 of the sorted listing", disclosed by the worker): c05c shows the dev IDs coincide with tokens other agents chose as a generic HCP range bound and as an example HCP-shaped token. So the residual probably needs only widely known HCP subject numbering, not the B300 listing. Not verified further, because that would mean handling IDs. This is a PI/root ruling, nonblocking for T2.4 as scoped by addendum_06 §5.
- The E2/E3 card readings are interpretive. Mine match the addendum's strict reading.
- The first c05 run deadlocked on a pipe, a bug in my probe. It was preserved in prev_versions/ (sha recorded), fixed (stdin fed from a thread) and rerun. Killing that hung probe of mine was not a pytest timeout.

## 4. Conclusion
CONFIRMED. T2.4 is satisfied as scoped:
- V01–V11 are killed by additive tests on frozen code.
- W09 is equivalent.
- E1 is recorded and true; E2–E5 are reproduced.
- The salted-hash dev-ID channel is closed.
- No regression is attributable to M3.
- The shipped verdict stays stop: I1 t95 upper bound 0.361 % < δ = 1 %, independently recomputed.

Nonblocking items for root:
- (i) Two other-team files contain a literal token equal to a dev-subject HCP ID: tests/topic2_fu_c/test_gate_and_records.py (FU-C) and verification/challenger_M3_r3_1/p06_c4_scan_r3_outputs.py. Ask the owners to use a non-HCP placeholder (C4 hygiene).
- (ii) The worker's FU-B open issue is stale: the full suite is 116 passed now.
- (iii) The old-86 pilot e2e test needs PYTHONPATH=repo root.
- (iv) The positional residual ruling stays with the PI.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`; `grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c`
- `PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q tests/topic2_rgpool` → 116 passed
- `cd verification/challenger_M3_r3_2 && python3 c00_build_specs.py && python3 c01_mutants.py c00_specs.json <scratch> out.json --tests tests/topic2_rgpool/test_verdict_path_guards_r3.py --jobs 2` → V01–V11 KILLED
- `python3 c03_recompute.py`, `c04_errata_probes.py`, `c06_reading_rule_grid.py`, `c05_salt_scan.py`, `c05b_dev_id_plaintext_scan.py`, `c05c_dev_id_attribution.py` (counts and masked contexts only)
- Invalidated if: any frozen file or receipt changes; the new test file changes (sha 40149a12…808a); verdict.json changes (59af05e5…af68).
- Message to parent: none sent. The dispatch says the structured return is the final report.
