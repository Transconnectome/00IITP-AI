# Handoff (Hard) — explorer_M2H2_r2_3, M2H2 iteration 2, lens: adversarial pre-mortem
Written 2026-11-01T17:55Z. Host claude-code (Opus 5.5). No GPU used. No production file written.

**Summary.** The iteration-1 science reproduces. The gate failed on test coverage only (challenger_M2H2_r1_2): the verdict-path wiring and the guards in `scripts/topic3h2_stats.py` have no tests. Iteration 2 should therefore add tests and errata and nothing else:
- new test files only;
- a dated errata file;
- ledger correction rows;
- no change to src/, scripts/, addendum 07, the result report or any shipped output; no GPU.

Two of my probes back this up:
- **Exact reproduction.** Rerunning `gate` and `final` in a copied tree reproduces both shipped JSONs exactly. The only leaves that change are `run.*` and `gate_decision_sha256`.
- **What a regression test catches.** A full-output regression that ignores those leaves kills N26, N27, N53, N11, N30, N38, N40, N41 and N59. It cannot kill N32, N50, N55 or the other guard mutants; those need negative-input tests.

Separately, auditor mutant A09 was claimed equivalent, but it is killable.

## 1. Observation
O1. Receipts and pins.
- `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries) pins:
  - the result report `docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md`;
  - all of `src/topic3_h2/*.py` (vendor included);
  - `scripts/topic3h2_*.py`;
  - the 8 existing `tests/topic3_h2/test_*.py`;
  - all gate, random and log files and `h2_results.json`.
- Checked now: C1 rc 0, output_sha256 rc 0, addendum_07_sha256 rc 0 (LC_ALL=C).
- Job records (gate_record.json, random_record.json, h2_results.json `run.code_sha256`) hash the files matched by `src/topic3_h2/*.py`, `src/topic3_spectral/*.py` and the script.

O2. Survivors. `verification/challenger_M2H2_r1_2/mutants_ch2.out.json`: 53 mutants, 27 killed, 26 survived:
- N11, N26, N27, N30, N31, N32, N33, N35, N38, N40, N41, N42;
- N50–N59;
- N71–N74.

`survivor_impact.out.txt`:
- N26 → C1 INC→EQ.
- N53 → C1 EQ and 7/10 Family L token labels change.
- Labels computed from a single seed only, for C1 across seeds 1..10: EQ, INC, INC, TE+, EQ, INC, TE+, EQ, TE+, TE+.

That harness ran most mutants on a test SUBSET (`FAST` = decision_rule, compare, endpoints, driver_offline, provenance_governance; `DRVT` = FAST + model_init), not the full suite (mutants_ch2.py lines 19–24).

O3. Other r1 survivors and where they are defined (I have read their harness lines):
- reviewer_M2H2_r1_1 `rev_mutants.py`:
  - X04 (= N50);
  - X09 (`d1["cov"]["lo"] > 0` → `>= -1e9`);
  - X14 (= N40);
  - X15 (`e.max() < -delta` → `<= -delta + 1e-9`).
- reviewer_M2H2_r1_2 `extra_mutants.py`:
  - X06 (= N30);
  - X10 (= N55);
  - X11 (= N50);
  - X13 (= N73);
  - X14 (`if tuple(seeds) != prov.SEEDS:` → `if False:`).
- challenger_M2H2_r1_1 `script_wiring_mutants.py`:
  - W3 (all arms read R1 scalars, ≈ N53);
  - W6 (= N50).
- auditor_M2H2_r1_1 `aud_mutants.py`:
  - A05 (= N40);
  - A09 (duplicate-window check removed in driver.run_arms; called "effectively equivalent").

O4. Probe: copied tree `verification/explorer_M2H2_r2_3/tree/` running `scripts/topic3h2_stats.py final` (3.3 s), then `gate`, then `final`.

| Output | Leaves that differ (`diff_json.py`) |
|---|---|
| h2_results.json, first `final` | `/run/runtime_s`, `/run/started_utc` |
| gate_decision.json | `/run/started_utc` |
| h2_results.json, `final` after `gate` | the same two, plus `/gate_decision_sha256` |

Everything else is bit-equal, including `run.code_sha256`, host and versions. The labels are C1 INC, C2 INC, C3 TE+, C4 TE+.

O5. Probe `probe_regression_mutants.py` (out: `probe_regression_mutants.out.txt`). Each mutant was applied to the copied tree, then `gate` and `final` were run, and non-run leaves were compared with the shipped JSONs (ignoring `/run/**` and `/gate_decision_sha256`):

| Mutant | gate | final |
|---|---|---|
| N26 | — | 34 leaves differ |
| N27 | — | 32 leaves differ |
| N53 | — | 694 leaves differ |
| N11 | — | 42 leaves differ |
| N30 | 30 leaves differ | — |
| N38 | 7 leaves differ | — |
| N40 | — | rc 1 ("T subject-level A1 does not reproduce the pinned Family A") |
| N41 | — | rc 1 (same message) |
| N59 | — | 1 leaf differs (`addendum07_sha256`) |
| N32 | 0 | 0 |
| N50 | 0 | 0 |
| N55 | 0 | 0 |

After the tree was restored, the baseline was again 0/0.

O6. Probe (copied tree, `tests/topic3_h2/test_probe_a09.py`, tree only). `driver.run_arms(..., loader[:1] + loader, ...)` is a duplicate window that arrives before its subject has all 7 windows:
- original code: raises, so the test passes;
- A09 mutant: the test fails.

So A09 is killable. The shipped test `test_duplicate_or_missing_windows_raise` appends the duplicate at the END (`loader + loader[:1]`). That case is caught by the "incomplete subjects" path, which is why A09 survived.

O7. Probe `delta_sensitivity.py` relabels the SHIPPED intervals and seed effects with the shipped `decide()`, over δ = f × |trained effect|. The label changes at these values of f:

| Endpoint | TE+ while f < | INC while f in | EQ from f ≥ |
|---|---|---|---|
| C1 | 0.158 | [0.158, 1.018) | 1.018 |
| C2 | 0.459 | [0.459, 1.112) | 1.112 |
| C3 | 0.549 | [0.549, 1.292) | 1.292 |
| C4 | 0.664 | [0.664, 1.206) | 1.206 |

Frozen f = 0.5. C1 seed effects range from 0.0036 to 0.0232 against δ = 0.0114.

O8. Result report (`2026-11-02_topic3_h2_result_report.md`):
- **§6 item 1** says "The label for C1 sits on the δ boundary". Per O7, C1 is the most robust of the four and C3 is the least.
- **§3** says the L0 between-subject PR "is set by the input and the patch embedding, not by training", but L0 subject cov and corr are INC.
- **§5, R1 row**: "cannot be read as a training product".
- **§5, R2 row**: "It is not an architecture or input artefact". That is only relative to the constructor's default init.
- **§3 and §4** call R0 numbers "trained" (2.78/11.02/3.58, α medians).
- **§7** lists `scripts/topic3h2_stats.py gate|final` with `cd /home/juke/git/00IITP-AI`, i.e. in the production tree. Following it literally rewrites `gate/gate_decision.json` and `h2_results.json` and breaks the output_sha256 receipt. The prose below the commands says to use a copied tree.

O9. GPU ledger:
- Lines 93 and 103 (closing rows of jobs 218063 and 218064) carry KST times in the UTC columns, labelled "(KST)".
- All M2H2 jobs 218004, 218007, 218041 and 218063–218069 have start and closing rows.

O10. Script facts:
- `scripts/topic3h2_stats.py` sets the module global `OUT = prov.OUT` (= `results/topic3/2026-11-02_h2`), and `_dump` writes there.
- `prov.verify_addendum07(addendum=ADDENDUM07, receipt=ADDENDUM07_RECEIPT)` binds its defaults at definition time, so monkeypatching `prov.ADDENDUM07` has no effect.
- `src/topic3_spectral/io_contract.py` reads the pinned pooled matrices from the absolute path `/home/juke/git/VRABES/RemissionAnalysis` (hash-checked).
- `driver._run` imports `torch` and `from src.topic3_h2 import model as M` inside the function, and needs `torch.cuda.get_device_name(0)`.

O11. Existing tests:
- The family-C wiring test (`tests/topic3_h2/test_endpoints.py:110–131`) builds K seeds with `_tok_arm(rng, base)` and default noise 0.01, i.e. nearly identical seeds. That is why "seed 1 for all" (N26/N27) passes.
- `test_no_bids_prefix_anywhere_in_h2_outputs_and_docs` scans every file under `results/topic3/2026-11-02_h2/**` and `docs/03_empirical_analysis/topic3/2026-11-02_*`. The pinned `tests/topic3_spectral/test_outputs_no_ids.py` scans `results/topic3/**` and `docs/.../topic3/**` for the BIDS subject-prefix bytes.
- Torch tests use `importorskip`. They run on DGX-Spark (71 passed, 0 skipped per r1).
- No existing test checks `output_sha256.txt` of the H2 dir.

O12. Workflow C (`orchestrator/workflow_C_script.js.txt` lines 71–118):
- MAX_ITER = 3.
- Iteration 2 again uses the full strict gate: 2 reviewers, 2 challengers and 1 auditor, all required to pass. Challengers are told to run mutation tests.
- Worker ownership for M2H2 lists the docs only as `2026-11-02_topic3_addendum_07_h2_card.md` and `2026-11-02_topic3_h2_result_report.md`. The results dir `results/topic3/2026-11-02_h2/` is owned.

O13. Hygiene and integrity:
- `src/topic3_h2/__pycache__/` and `src/topic3_h2/vendor/swift_cd87338_models/__pycache__/` (cpython-312) were created at 2026-11-01T17:08:20Z by an unknown process.
- Auditor N1: the r1 worker's connectome code dir was partly overwritten at 16:39:09Z (stale `driver.py` 197192b7, truncated pinned npz).
- Auditor N7: hung `find /storage` processes of user connectome1 have been running since 2026-10-30.

## 2. Logic chain
L1. Why src and scripts must stay unchanged (O1):
- Any edit to `src/topic3_h2/*.py` or `scripts/topic3h2_stats.py` breaks `output_sha256.txt` (a C-constraint receipt).
- It also breaks the "code that produced the results = repo code" chain the verifiers checked (job-record code_sha256).
- Adding a NEW module under `src/topic3_h2/` changes the glob set hashed by `_run_record`. That changes `run.code_sha256` in any rerun and breaks the reviewers' "0 mismatches" claim.
- So: tests only, in NEW files under `tests/topic3_h2/`, plus errata. If a new test exposes a REAL defect, that is a different path: preserve the old bytes, write a dated addendum, rerun the stats locally (aggregates exist, no GPU), and report both.

L2. Why a full-output regression is the right test (O4, O5):
- The stats pipeline is deterministic and reproduces exactly.
- A regression of `gate` and `final` against the shipped JSONs therefore kills every wiring mutant that changes any number, including the two blocking label-flippers N26 and N53.
- It must ignore `run.*` and `gate_decision_sha256`. Comparing `run.code_sha256` would "kill" every mutant by hash rather than by behaviour, so no kill would be attributable to behaviour. Verifiers will attack that.

L3. Why guard mutants need their own tests (O5, O2):
- Guard mutants (N50–N58, X14r2, N55/X10, N56, N57) are invisible on valid shipped inputs.
- Each needs a negative-input test: corrupt one input in a tmp copy and assert SystemExit, or a FAIL verdict with the right failed check.

L4. Why the regression must test the tree it runs in (O10):
- The regression must locate the repo from `__file__`, never from a hard-coded `/home/juke/git/00IITP-AI`. Otherwise, inside a mutation tree it tests production code, and mutants falsely survive.
- It must write only to `tmp_path`. If it monkeypatched `prov.OUT` instead of the script's own global, or ran in place, it would overwrite shipped outputs. The current suite would not notice that (O11: no H2 output_sha256 test).
- Hence two requirements: a guard (`mod.OUT != prov.OUT`, plus an assertion that the production sha of h2_results.json and gate_decision.json is unchanged), and a new receipt test.

L5. Driver-path mutants:
- N71 (G5 `all` → `any`), N73 (= X13), N35 (REPOOL_TOL) and N33 are in pure-numpy functions (`gate_checks`, `negative_controls`, `compare`). They can be killed offline with monkeypatched I/O.
- A09 is killable (O6).
- N72 and N74 sit in `driver._run`. They need a fake model module and stubbed cuda calls (O10). That is feasible but fiddly. If it is not done, they must be documented as offline-unreachable. The runtime evidence is the encoder hashes of seeds 1, 3, 4, 7 and 8, independently reproduced by four verifiers' GPU reruns, plus the G4 load record.
- N42 is equivalent by construction: `returnable_scalars` builds `out` only from `positions` and SCALAR_KEYS×VARIANTS, none of which match the forbidden predicates.

L6. Mutation evidence that will survive scrutiny (O2, O12):
- Under a strict 5-verifier gate with mutation-testing challengers, the worker should re-create every r1 survivor verbatim (O2, O3) and show two things:
  - (a) it survives the SHIPPED suite, run in FULL. The r1 survival evidence was partly on subsets.
  - (b) it is killed by the NEW test files alone (attributable kill).
- A kill on a subset is a valid kill; a survival on a subset is not proof of survival.

L7. Errata (O8, O1, O12, O11):
- The result report is pinned and cannot be edited, so its errors (O8) go into a dated errata.
- The owned location is under `results/topic3/2026-11-02_h2/`, because the docs path for an addendum_08 is not in the ownership list (O12).
- Every new file there and in docs is scanned for the BIDS subject-prefix bytes (O11). Words like hyphenated "sub" compounds would turn the pinned topic3_spectral test red.

L8. δ (O7):
- The shipped labels depend on δ, which the worker chose, not the PI.
- Re-deciding with a new δ after the results would be post-hoc. The errata gives the descriptive sensitivity table, and the PI's confirmation is listed as owed.
- C3, the headline "learned" label, has the thinnest margin: 0.549 vs 0.5.

L9. Seed variance:
- The token-level CI ignores seed variance, and single-seed C1 labels span EQ, INC and TE+ (O2).
- The shipped rule handles this through the all-seeds condition, which is why C1 is INC.
- The errata and the integrated report must not cite the narrow token CI as the total uncertainty.

## 3. Caveats
- I did not read the peer r2 explorers, the r1 worker handoff, or addendum 07 in full. I relied on the code, the receipts and the verifier reports.
- I re-ran only 12 mutants in the regression probe, using simple stats-script rerun loops, not pytest. N31 is expected to be killed by the gate regression (missing keys), but I did not run it.
- I did not test the fake-model `_run` approach for N72 and N74.
- Restoring JSON in my tree used `json.dumps(indent=1)`, which is the same as the script's `_dump`. The tree is a copy, so production was never touched.
- My copied tree `verification/explorer_M2H2_r2_3/tree/` (22 MB: copies of repo src, results/topic3/2026-10-31 and 2026-11-02_h2, docs) could not be deleted: `rm -rf` was denied by the permission system. I did not work around it. Root may delete it.
- The tree's `results/topic3/2026-10-31` copy contains the pinned npz with per-subject pooled vectors. These are copies of files already in the repo, not new data.
- No connectome or B300 access; 0 GPU-h.

## 4. Conclusion (recommendation for worker_M2H2_r2)
Must do (each item names the mutants or issues it closes):
1. **NEW** `tests/topic3_h2/test_stats_script_regression_r2.py`:
   - Copy, into `tmp_path`, the tree rooted at `Path(__file__).parents[2]`: src/, scripts/topic3h2_stats.py, docs/.../2026-11-02_topic3_addendum_07_h2_card.md, results/topic3/2026-10-31, results/topic3/2026-11-02_h2.
   - Run `sys.executable scripts/topic3h2_stats.py gate`, then `final`, with cwd = the tmp tree, `PYTHONPATH` = the tmp tree and `PYTHONDONTWRITEBYTECODE=1`.
   - Require rc 0 for both.
   - Compare every non-`/run` leaf, and every leaf except `/gate_decision_sha256`, for exact equality with the shipped gate_decision.json and h2_results.json, read from the test's own tree.
   - Assert that the shipped files' sha256 is unchanged afterwards.
   - Kills: N26, N27, N53/W3, N11, N30/X06, N31, N38, N40/A05/X14r1, N41, N59, X09.
2. **NEW** guard tests (in-process: `importlib` load of the script, `monkeypatch.setattr(mod, "OUT", tmp_copy)`, assert `mod.OUT != prov.OUT`). Corrupt one input each and assert SystemExit with a message, or FAIL with the named check:

   | Corrupted input | Expected | Kills |
   |---|---|---|
   | gate_decision FAIL | refusal | N50/X04/X11/W6 |
   | `seed_hashes_distinct` False | refusal | N51 |
   | `rebuild_same_seed_identical` False | refusal | N51 |
   | the 9-seed set | refusal | X14r2 |
   | trained hash placed among the seed hashes | refusal | N58 |
   | `h2stats.pinned_deltas` monkeypatched off-frozen | refusal | N54 |
   | `reduce.card_index_sets` monkeypatched to seed+101 | refusal | N52 |
   | `verify_addendum07.__defaults__` pointed at a tmp addendum with a wrong receipt | refusal | N59 behaviourally |
   | R0_scalars perturbed 1e-5 relative | G3 FAIL | N55/X10 |
   | tf32 [True, False]; `vendor_ok` False | G4 FAIL | N56 |
   | `n_windows` 398 | G1 FAIL | N57 |
3. **NEW** driver and compare tests:
   - `gate_checks` with monkeypatched `io.load_X` / `io.ids_order_matches_names`:
     - re-pool offset 1e-3 → G2 FAIL; 5e-6 → PASS (kills N35);
     - `compare.contrast_status` patched so R0 ≠ T → G3 FAIL (kills N73/X13).
   - `negative_controls` with patched `data.vrabes_dataset`, `_loader`, `_fwd`, `_stored`, `shift_windows`, `pad_value_override`, where one control matches → G5 FAIL (kills N71).
   - `contrast_status` with CI (−0.3, −0.1) → excludes 0 (kills N32).
   - A direct call `negative_control_fails_g1({"n_windows":0,"n_fail_cells":1})` is False (kills N33).
   - `run_arms(loader[:1]+loader)` raises (kills A09; disproves its equivalence).
   - `decide` with `e.max() == -delta` → INC (kills X15).
   - Family C/L synthetic tests with HETEROGENEOUS seeds, so that a single-seed collapse changes a label (N26/N27 attributable at unit level). For N11, check that the level-key order equals the addendum order.
   - N72/N74: either a fake-`M` test of `_run`, or documented as offline-unreachable with the runtime evidence (L5).
   - N42: equivalence proof.
4. **NEW** receipt test: `LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt` returns rc 0, so an in-place rewrite is detected.
5. **Mutation evidence.** Write `verification/worker_M2H2_r2/` with:
   - every r1 survivor re-created verbatim (O2, O3), including A09;
   - for each: shipped suite FULL → survives; new test files alone → killed (attributable);
   - a baseline that passes fully in the copied tree (copy the challenger_2 COPY list);
   - 2 trees in parallel, timeout 900, detached, with a progress log.

   Equivalents need a proof (N42). Offline-unreachable mutants need runtime evidence (N72/N74).
6. **Errata** (new file, owned path), e.g. `results/topic3/2026-11-02_h2/r2/2026-11-02_h2_errata_r2.md`, with no BIDS subject-prefix bytes and its own sha256 receipt. It must:
   - (a) correct §6.1 with the O7 table (C3 is the thinnest margin; C1 is robust);
   - (b) withdraw the L0 "set by input" reading (INC ≠ EQ);
   - (c) R1 row → "descriptive", with the CIs;
   - (d) qualify R2 "not an architecture artefact" to "relative to the constructor default init";
   - (e) relabel the R0 numbers in §3/§4 as R0 (≤ 6.4e-7 from T);
   - (f) §7: run the stats commands only in a copied tree;
   - (g) record auditor N1 (remote overwrite) and its remediation, plus N4 (driver does not hash-check the addendum);
   - (h) state that seed variance is not in the token CIs;
   - (i) state that no rule, label or number changes.
7. **Ledger.** Append UTC correction rows for 218063 (16:22:19Z–16:30:24Z) and 218064 (16:32:19Z–16:51:39Z), under flock. Never edit existing rows.
8. **No GPU, no reruns.** Keep the connectome worker venv until victory, because verifiers reuse it read-only. Re-ship the remote code dir so it matches `logs/ship_manifest_sha256.txt`, or delete only its `code/` subdir after recording hashes; record which. Do not touch explorer or reviewer dirs or the hung `find` processes; escalate those to root.
9. Run the old 86, tests/topic3_h2 (new count), tests/topic3_spectral 138 and tests/topic1_lagmotif. Then run C1, every receipt, an ID scan of the new files and the whole-run `audit_layout.py`. Report the skip count (must be 0).

PI-owed (root, not worker): confirm or replace δ. Any change goes into a new dated addendum with the post-hoc label stated; the shipped labels stay as frozen.

## 5. Verification method
- Rebuild a copied tree (my `tree/` remains if root has not deleted it):
  `cd /home/juke/git/00IITP-AI/verification/explorer_M2H2_r2_3 && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=tree nice /home/juke/superclaude-env/bin/python3 tree/scripts/topic3h2_stats.py final`
  Then compare against shipped with `python3 -I diff_json.py <shipped h2_results.json> tree/results/topic3/2026-11-02_h2/h2_results.json`. Expect only `/run/*` to differ.
- `python3 -I probe_regression_mutants.py <shipped h2_results.json> <shipped gate_decision.json>`. Run it on a copy saved first, since the script restores from those files. Expect the table in O5.
- `python3 -I delta_sensitivity.py tree tree/results/topic3/2026-11-02_h2/h2_results.json` → O7.
- A09: `tree/tests/topic3_h2/test_probe_a09.py`. It passes on the original and fails with the A09 patch.
- Invalidation: if `output_sha256.txt` no longer verifies, or the shipped JSONs differ from the rerun in any non-run leaf, the reproduction premise fails and the plan must be revisited.
