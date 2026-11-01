# Handoff — explorer_M2H2_r2_2 (M2H2 iteration 2, explorer 2 of 3; lens: feasibility and failure modes)

**Summary.** The r1 gate failed only on test coverage: the shipped science reproduces exactly, and every verifier reproduced it. The fix is additive, offline and costs no GPU. Two places need new tests in new files. First, `scripts/topic3h2_stats.py` (`gate` and `final`): a full-output regression run in `tmp_path`, plus one refusal test per guard. Second, a family C / L fixture whose K seeds really differ. Optionally, add comparator, reduce and driver fake-harness tests. I wrote a 58-test probe of exactly this design in my verification dir and ran it against the union of every surviving r1 mutant (32 mutant runs). The probe kills 29 of 31 survivor mutants. The other two are N42, which is provably equivalent, and A09, which the probe does not cover; a kill design for it is in §4. The probe runs in about 8 s; `final` alone takes 3.9 s and `gate` 0.1 s. Nothing in src/, scripts/, the frozen addendum 07, the result report or the shipped results needs to change, and none can change without breaking pinned receipts.

## 1. Observation

O1. Gate record (dispatch): FAIL, set by challenger_M2H2_r1_2 REFUTED. The blocking issues are:
- (B1) N26 / N27 / N53 survive and flip C1 INC→EQ on the real data. Cause: the family C fixtures use near-identical seeds, and no test runs `cmd_final` or `cmd_gate`.
- (B2) The stats-script guards N50–N59 are all untested.

All the other verifiers either approved or rated the same class nonblocking:
- reviewer_1: X04, X09, X14, X15 survive;
- reviewer_2: X06, X10, X11, X13, X14 survive;
- challenger_1: W3 and W6 survive (its own JSON labels them "KILLED" only because its copied-tree baseline already failed one test);
- auditor: A05 survives, A09 is equivalent.

Every verifier reproduced every shipped label and number independently. The one exception is the deliberate 1-subject-scope job reruns, which reproduced bitwise.

O2. `scripts/topic3h2_stats.py`:
- `OUT = prov.OUT` (line 30) is a module global used for both reading and writing (`_dump` line 50; `cmd_gate` line 76; `cmd_final` lines 103 and 106). Monkeypatching `mod.OUT` after `importlib` loading redirects the whole command to `tmp_path`.
- The guards sit at lines 104 (gate PASS), 109 (seed set), 111 (seed hygiene), 114 (trained hash), 119 (`check_deltas`), 127 (T reproduces pinned Family A A1), 81 (G1 window count), 86 (local G3) and 91 (tf32 / vendor).
- `prov.verify_addendum07` takes its default arguments at definition time (provenance.py line 105). To test the refusal, either monkeypatch the function or set its `__defaults__`. Changing `prov.ADDENDUM07` has no effect.

O3. Cost and determinism (probe, copied tree `verification/explorer_M2H2_r2_2/tree_v1`, superclaude-env python 3.12.3, numpy 2.3.5, which is the same environment as the shipped `final` run per `h2_results.json` run):
- `final`: wall 3.86 s, max RSS 53.6 MB.
- `gate`: 0.10 s.
- `deep_diff.py` of the rerun outputs against the shipped `h2_results.json` and `gate_decision.json`: `n_diff_leaves 0`, with the top-level `run` leaf excluded.
- `pinned_T` reads the pooled matrices from `/home/juke/git/VRABES/RemissionAnalysis`, which is local and read-only, the same as the shipped run.

O4. Ordering trap, observed. After I reran `gate` in the tree, rerunning `final` differed in exactly one leaf, `/gate_decision_sha256`. `h2_results.json` records the sha256 of whatever `gate_decision.json` it read, and `gate_decision.json` contains a timestamped `run` leaf. Restoring the shipped `gate_decision.json` made the probe pass.

O5. `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries) pins:
- the result report `bb1ef63e…`;
- all 8 existing `tests/topic3_h2/*.py`;
- `src/topic3_h2/**` and both `scripts/topic3h2_*.py`.

`LC_ALL=C sha256sum -c` gives rc 0, and C1 PROTECTED_HASHES also gives rc 0 (both checked by me). Editing any of these files breaks the receipt. sci-pipeline G7 also says "평가 코드·테스트 해시 고정(에이전트 수정 시 FAIL)".

O6. `tests/topic3_h2/test_provenance_governance.py`:
- line 56–60 fails on the bytes `sub-` in any file under `results/topic3/2026-11-02_h2/**` and in `docs/03_empirical_analysis/topic3/2026-11-02_*`;
- line 64–69 fails on any npz there with keys starting `pooled__` / `cat_cov_eigs__` / `cat_corr_eigs__`, equal to `ids`, or containing `name`, and on any `.pt`.

A new addendum that quotes the BIDS prefix literally, or a probe output saved under H2_OUT, would fail an existing pinned test.

O7. `tests/topic3_h2/test_endpoints.py::test_family_c_wiring_each_endpoint_reads_its_own_card_contrast` builds all K seeds from one `base` with noise 0.01 (lines 101–104). So "every arm = seed 1" (N26 / N27) leaves the labels and points unchanged within the test tolerances. Likewise, `test_family_l_logs_before_seed_mean_and_holm_over_ten` checks seeds by position (`[... for k in out["token"]] == [20268131 + 10k]`), so a reordered `level_keys` (N11) keeps the list equal.

O8. Driver job paths are testable offline. The names `driver.data`, `driver._loader`, `driver._stored`, `driver._fwd`, `driver.io.load_X`, `driver.io.ids_order_matches_names` and `driver.analysis.paired_log_contrast` are module attributes. `_run` imports `torch` and `from src.topic3_h2 import model as M` inside the function (driver.py lines 230–231), so a fake `M` in `sys.modules` plus monkeypatched `torch.cuda.get_device_name` / `max_memory_allocated` lets `_run` write a record on CPU. My probe does this.

O9. Probe results. `verification/explorer_M2H2_r2_2/probe_tests/test_probe_r2.py` has 58 tests and passes in 7.8 s on the clean tree. The mutation run is `verification/explorer_M2H2_r2_2/probe_mutants.py`, which applies each mutant in place and restores the bytes (sha256 asserted); its output is `probe_mutants.out.json` and `probe_mutants.log`. Results are in O10.

O10. Mutation probe result (`probe_mutants.out.json`): the baseline passes before and after (58 passed), all 31 mutants applied, and every tree file was restored byte-identical (`cmp`, checked).
- **KILLED (29):** N11, N26, N27, N30, N31, N32, N33, N35, N38, N40, N41, N50, N51, N52, N53, N54, N55, N56, N57, N58, N59, N71, N72, N73, N74, W3, X09, X14r2, X15.
- **SURVIVED (2):**
  - N42 is equivalent: `reduce.returnable_scalars` builds `out` only from `positions` and SCALAR_KEYS×VARIANTS, so `bad` is always empty.
  - A09 has no probe test. Kill design: insert a duplicate (position 0, start 0) window carrying different data before subject 0 completes. The shipped code raises; the mutant silently keeps the later window.
- **Aliases** (same edit under another verifier's id): W6 = X04 = X11 = N50, X10 = N55, X06 = N30, X13 = N73, X14(reviewer_1) = A05 = N40.

O11. Ledger (`results/gpu_ledger_2026-10-31.md`):
- The completed M2H2 rows sum to 0.819 GPU-h of the 6 GPU-h cap.
- The closing rows for jobs 218063 (line 93) and 218064 (line 103) put sacct KST local times in the "end UTC" / "start UTC" columns, labelled KST: 01:22:19–01:30:24 and 01:32:19–01:51:39 KST, which are 16:22:19Z–16:30:24Z and 16:32:19Z–16:51:39Z.

O12. Result report (`docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md`, pinned):
- line 90 says C1 "sits on the δ boundary";
- line 84 says the expansion "cannot be read as a training product";
- line 65 says the L0 PR "is set by the input and the patch embedding, not by training";
- line 65 and §4 use the R0 values as "trained";
- line 80 says "More than half of it is absent", while the init drop is 0.26 against the trained 5.34. This phrase is copied from the frozen addendum 07 §7 consequence table, so it is a true lower bound and not an erratum; the addendum may add the measured fraction.

Three verifiers independently computed δ sensitivity: C1 INC over 0.158–1.017×; C2 TE+ only at ≤0.458×; C3 TE+ only at ≤0.548×; C4 TE+ only at ≤0.663×.

## 2. Logic Chain

L1 (O1, O7). The defect is a fixture design defect, not a code defect: K nearly equal seeds make "one seed for all" indistinguishable from "mean over seeds". The repair is a fixture whose seeds differ by a lot (spread ≥ 0.3 in log units at the contrast layers), plus an exact assertion of the seed-mean arithmetic and a non-zero spread of `seed_effects`.

L2 (O2, O3). Running the real commands on the real shipped aggregates is cheap (seconds) and deterministic in the project env. So a full-output regression is the strongest single test: any wiring mutant that changes any number (N26, N27, N53 / W3, N11, N40, N41, N59's sha leaf) fails it. Compare labels and strings exactly and floats at rel ≤ 1e-12, not by bitwise equality, so that a numpy upgrade is reported as a numeric drift instead of passing unnoticed or failing for no reason.

L3 (O2). A guard that is only a `sys.exit` on a condition the shipped data never meets is invisible to a regression test. Each guard needs its own refusal case: edit a copied `gate_decision.json` / `random_record.json` / `gate_record.json` / `R0_scalars.npz` in `tmp_path`, or monkeypatch the one dependency (`verify_addendum07`, `pinned_deltas`, `card_index_sets`). Then assert both `SystemExit` (or gate FAIL naming the check) and that no output file was written.

L4 (O4). The regression must feed `final` the byte-identical shipped `gate_decision.json`, and run `gate` in a separate `tmp_path`. A test that runs `gate` then `final` in one directory will always differ in `gate_decision_sha256`.

L5 (O5, O6). All new material must be NEW files:
- new test files under `tests/topic3_h2/`;
- a new dated addendum;
- a new receipt pinning the new tests and the addendum.

The worker must not edit addendum 07, the result report, `output_sha256.txt`, existing tests, src or scripts. The new addendum and any file under H2_OUT must not contain the BIDS prefix bytes; for example, write "the BIDS subject prefix" instead.

L6 (O8). The driver-path survivors (N71–N74, A09) can be killed offline with fakes, so they are not a hardware limitation. They were rated nonblocking. Covering them is cheap and closes the "same class as earlier M2 gates" argument before a verifier makes it.

L7 (O9/O10). The probe is evidence that the design kills the named mutants. It is not the production test: the worker should write its own tests and rerun the full union harness against the full `tests/topic3_h2` suite in a tree whose baseline passes.

L8 (O1, O12). The δ issue is a G5 gap (δ is PI-only per sci-pipeline §3), not a code defect. Choosing a new δ after the results are known would be a forking path. The clean route is for root to ask the PI to ratify the frozen δ = 0.5 × |trained effect|. The sensitivity table goes into the new addendum as descriptive material, and the labels are cited as "worker-set δ, PI-ratified" (or "not ratified" if the PI declines). This does not need to block the r2 test gate.

## 3. Caveats

- The probe was run in a minimal copied tree (scripts, src, the addendum 07 doc, pinned 2026-10-31 inputs, H2 gate/random). It was not run against the full suite, so the kill counts show that the probe design kills these mutants, not how the full suite will behave. The worker's production tests may differ.
- The fake-`M` `_run` harness skips `run_arms`, `arm_outputs` and `gate_checks` inside `_run` (empty sums). It covers seed-hash recording and checkpoint loading only; G1/G2/G3 inside `_run` stay covered by the separate `gate_checks` test.
- The regression test depends on the local VRABES pooled files and the pinned 2026-10-31 outputs. It must fail, not skip, if they are missing.
- I did not contact connectome. The stale remote dir reported by the auditor (N1) and the 5 GB venvs remain; deleting other agents' dirs is not mine to do (a reviewer's `rm` was refused by the permission system).
- I did not read the other r2 explorers' reports.
- No real-data random-init quantity was computed by me beyond rerunning the shipped `final` / `gate` on the shipped aggregates; no new GPU or connectome use.

## 4. Conclusion

Recommended r2 scope: additive tests, a dated addendum and a receipt. No src or scripts change, no rerun, no GPU.
1. `tests/topic3_h2/test_stats_script_regression.py`: `final` and `gate` in `tmp_path` against the shipped JSON (labels exact, floats rel ≤ 1e-12, `run` leaf excluded, gate fed the byte-identical shipped `gate_decision.json`).
2. `tests/topic3_h2/test_stats_script_guards.py`: one refusal case per guard (gate FAIL, seed set, hash distinct, rebuild identical, trained hash, addendum receipt, deltas, index sets / T-A1) and gate FAIL cases (local G3 tamper, tf32, vendor, n_windows, G1, G5), each asserting that no output was written.
3. `tests/topic3_h2/test_family_wiring_r2.py`: seeds with real spread; exact seed-mean arithmetic for C1–C4; non-zero `seed_effects` spread; explicit family L key→test-seed mapping; D1-robust False without a drop (X09); strict TE− seed boundary (X15).
4. `tests/topic3_h2/test_gate_components_r2.py`:
   - stats_match parametrised over all 30 key×variant cells, with the small-magnitude relative case and the large-magnitude absolute case (N30 / N31 / N38);
   - contrast_status negative CI (N32);
   - negative control requires windows (N33);
   - card_index_sets sha256 equals the job-recorded `cd020fe8…` (N40);
   - subset corr is pr_corr (N41);
   - gate_checks G2 tolerance and G3 contrast wiring with fakes (N35, N73);
   - negative_controls all-three (N71);
   - fake-`M` `_run` for the seed hash (N72) and the checkpoint load (N74);
   - duplicate window inserted before subject completion (A09).
5. N42: record as equivalent with proof (`returnable_scalars` builds only `positions` + SCALAR_KEYS×VARIANTS, so `bad` is always empty).
6. New dated addendum 08 (e.g. `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_08_h2_r2.md`) recording:
   - the test additions and mutant table;
   - report errata (δ sensitivity, R1 wording, L0 INC reading, R0-as-T labels);
   - the auditor's remote-dir overwrite (N1) disclosure;
   - ledger UTC correction rows appended, never edited.

   Pin it, together with the new tests, in a new receipt `results/topic3/2026-11-02_h2/addendum_08_sha256.txt`.
7. Root asks the PI to ratify δ (sensitivity table attached). Results stay labelled with the frozen δ.

## 5. Verification Method

- Probe: `cd /home/juke/git/00IITP-AI/verification/explorer_M2H2_r2_2 && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 TREE=$PWD/tree_v1 PYTHONPATH=$PWD/tree_v1 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q probe_tests/test_probe_r2.py` gives 58 passed.
- Mutation probe: `nice /home/juke/superclaude-env/bin/python3 -I probe_mutants.py` gives `probe_mutants.out.json` (summary block; baseline before and after rc 0).
- Determinism: `python3 -I deep_diff.py <rerun json> shipped_copy/<json>` gives `n_diff_leaves 0`.
- Integrity: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` (rc 0) and `LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt` (rc 0).
- Invalidation: the strategy is wrong if a production regression test cannot reproduce the shipped JSON at rel 1e-12 in the project env (then a code or environment drift exists and must be reported, not tolerated), or if any shipped-label change is required.
