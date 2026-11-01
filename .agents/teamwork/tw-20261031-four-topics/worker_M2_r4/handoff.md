# worker_M2_r4 — handoff (Hard), M2 Topic 3 iteration 4 (final, PI decision 6 fixed scope), 2026-11-01

Status: DONE. All four fixed-scope classes are closed by additive tests. All 26 named mutants the dispatch requires are killed by the new tests in copied trees, and every pre-existing test passes under each of them. The 151-patch union shows no regression: U127 is the only survivor, as in FULL_v2. No src/ or scripts/ change, no production rerun, no git write, 0 GPU.

Deliverables (production):
- `tests/topic3_spectral/test_regression_r4.py`, sha256 `ecceb13422531ee5a41e48b04763f02607b9427d242a3b1baface17ed2e0fbed`: 7 tests, classes (a) and (d).
- `tests/topic3_spectral/test_token_level_r4.py`, sha256 `ab99b2b152515ea6ad8a5e0cb05d65af61d84ce4ca8c3efd36eab4b73e4a68d1`: 10 tests, classes (b) and (c).
- `docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_06.md`, sha256 `19b6218ffdd57fc9293e3659e78de9abbb717e14a7545dfd3715c597cd312756` (v3; see O7).
- `results/topic3/2026-10-31/addendum_06_sha256.txt`, sha256 `6191bd5acb77f77cf8bbbcbd3555d838d8c73b2121a614355dc66314ff05d510` (v3). It pins the three files above.

Evidence: `/home/juke/git/00IITP-AI/verification/worker_M2_r4/`, with subfolders `bin/`, `runs/`, `probes/`, `logs/` and `final/`. The manifest is `EVIDENCE_MANIFEST_final_sha256.txt` (657 files; the earlier `EVIDENCE_MANIFEST_sha256.txt` predates addendum v3 and fc6, see `EVIDENCE_MANIFEST_README.txt`).

## 1. Observation

O1. **The four classes and their tests** (addendum 06 §3 has the full mapping).
- (a) Family A full output:
  - `test_subject_level_script_reproduces_every_pinned_family_a_value` runs the unmodified `scripts/topic3_subject_level.py` in `tmp_path`, with OUT redirected by the script's own location. It compares the key sets, then all 300 `results` leaves, with the receipt-checked pinned `family_A_subject_level.json` at rel 1e-9, plus the deterministic run fields. It skips only when a pinned input is absent. It takes about 21 s.
  - `test_subject_level_matches_card_definitions_on_synthetic_matrices` re-derives every Family A quantity with independent numpy code on synthetic matrices that include a dead column. This is what catches FA11.
- (b) Token producer:
  - `test_subject_summary_matches_card_definitions_for_every_variant` checks the concatenated covPR, corrPR, dropped count and eigenvalues, the per-frame and H4 values and the pooled vectors, for all 5 variants, against independent numpy code. The fixtures include a near-dead L3 gain channel (γ = 1e-5) and a small live one.
  - `test_packed_spectra_feed_the_card_contrasts` checks pack → `token_level_checkpoint` for the H1a–H1e mean log ratios.
- (c) Primary-side Holm vs Bonferroni:
  - `test_primary_whose_holm_p_equals_its_raw_p_counts_as_significant`: 6 hand-built cases, Holm-consistent.
  - `test_primary_holm_equal_to_raw_p_holds_end_to_end_at_card_resolution[H1a, H1b]`: B = 9999, seed 2000, t = 2.15. H1a raw = Holm p = 0.0380; H1b raw = Holm p = 0.0347; the CI lower bound is about 0.00062 for both.
- (d) D1 corr-only branch:
  - `test_d1_verdict_follows_the_card_for_all_four_interval_cases`: 4 stubbed cases.
  - `test_d1_corr_only_case_computed_by_the_shipped_procedure`: challenger_2's witness at m = 28, S = 2000. It gives cov [−2.942, −1.660] and corr [+13.877, +15.440], so the verdict must be "drop not robust".

O2. **Shipped code (production), the r4 bytes frozen at 08:13:57Z.**
- `final/pre_topic3_b.log`: 138 passed, 0 skipped. The earlier `pre_topic3` attempt was cut by the Bash tool's 120 s limit (rc 143, 52%, no failure); it is INVALID and documented.
- In development, the first dev-tree run failed 1 test. The failure was in my own fixture precondition (the floor changed L3 corrPR by 4.4e-4, below my 1e-3 margin). No shipped-code comparison had run. I fixed the fixture, not a tolerance. Margins are in `probes/margins_r4.out.json`: cov/corr log ratio 0.24–0.98, floor effect 3.2%, Family A floor effect 1.8%.

O3. **Named mutants**, reproduced verbatim by AST extraction (`bin/named_specs.py`) from the four r3 harness files. Their sha256: RV31 `17a30dca…`, RV32 `ca6d7381…`, CH31 `d5f73f38…`, CH32 `0be048a3…`.
- 26 REQUIRED ids and 16 EXTRA ids merge into 32 jobs, by byte-identical patched file.
- All 32 have a valid record with 138 tests and 0 skipped. The records are in `runs/EVID_named_r4.json.partial` (v1), `runs/EVID_named_r4_v2b.json.partial` and `runs/EVID_named_r4_v3.json`.
- **All 26 REQUIRED ids are KILLED, with `failing_other` = []**, so they survive the shipped 121 and are killed by r4 tests only. Per-job tests are in addendum 06 §4.2 and `runs/SUMMARY_r4_tables.md`.
- Of the 16 EXTRA ids, 8 are now KILLED: N03, N04, CR3_A03, A04, A06, A09 = MC02, and MC01. The other 8 SURVIVE: N06, N12, VB02, FA13, FA14, GD01, GD02 and GD03.

O4. **Union.** worker_M2_r3's `union_specs.py` was copied byte-identical (sha `706ef81b…`). It gives the same 151 ids and triples as FULL_v2.
- Runner v3 ran in fail-fast mode, with the 16 test files in fast-first order. The records are `runs/EVID_union_r4_v3ff.json.partial` (29 jobs) and `runs/EVID_union_r4_v3c.json` (122 jobs).
- Result: 150 KILLED and 1 SURVIVED (U127, 138 passed); 0 INVALID; all controls passed with 138.
- No job's status differs from FULL_v2. For the 119 jobs whose first failure is a pre-existing test, that test is in FULL_v2's failing set for the job. The other 31 hit an r4 test first. The summary is `runs/SUMMARY_r4.json`.

O5. **Final checks before the addendum existed** (`final/fc1_summary.txt`).
- topic3: 138 passed. Old suite (STRICT_E2E): 86 passed. topic1: 88 passed.
- C1: 67 OK. Receipts: output 42, ad02 1, ad03 3, ad04 2, ad05 3 OK.
- `.pyc` listing unchanged from the start. Layout lint PASS (269 files).
- BIDS-prefix scan: only the synthetic names in the byte copies of the shipped `test_token_job_driver.py`.
- **Post-receipt final state.**
  - fc2 failed 2 topic3 tests (O7).
  - fc3: topic3 and the old suite were SIGTERMed by earlyoom (rc 143, INVALID; `final/fc3_INVALID_README.txt`).
  - fc4 (`bin/final_checks_v2.sh`, memory gate): old suite 86 passed; topic1 88 passed; C1 67 OK; receipts output 42 / ad02 1 / ad03 3 / ad04 2 / ad05 3 / ad06 3 OK; pyc unchanged. Its topic3 run was SIGTERMed again (INVALID; `final/fc4_topic3_INVALID_README.txt`).
  - fc5: topic3 138 passed, 0 skipped (`final/fc5_topic3.*`), with addendum v2 and receipt v2 in place; pyc unchanged.
  - Addendum v3 corrected two now-inaccurate v2 §7 statements: the rerun-log pointer and the identifier-scan hit list. v2 is kept in `superseded/`. The receipt was regenerated.
  - **fc6, with v3 in place (`final/fc6_summary.txt`), is the final valid run:** topic3 138 passed, 0 skipped; old suite 86 passed; topic1 88 passed; C1 67 OK; receipts output 42 / ad02 1 / ad03 3 / ad04 2 / ad05 3 / ad06 3 OK; pyc unchanged.
  - Final layout lint PASS (270 files, `logs/audit_layout_final2.log`). `EVIDENCE_MANIFEST_final_sha256.txt` covers 657 files (self-check OK).

O6. **Host memory pressure.** Other workloads held MemAvailable at about 7–15% of 120 GiB.
- 19 of my pytest attempts ended with rc −15, at times when `journalctl -u earlyoom` logged SIGTERMs. 17 were in v1 and 2 in v2b. All are INVALID and were rerun.
- v1 left 15 hung Pool processes from `test_token_job_driver.py`. I terminated them by PID (`logs/orphans_killed_0848.txt`).
- Runner v2/v3 added a memory gate, own-session process-group cleanup and automatic retry. Each stop is documented in `runs/*_STOPPED_README.txt`.

O7. **A C4 guard caught a defect in my own addendum.**
- The first post-receipt run (`final/fc2_*`) had 2 failures in topic3: the shipped `test_outputs_no_ids.py` and `test_outputs_scanned_nonempty.py`.
- Cause: addendum 06 v1 §7 quoted the synthetic subject names of the shipped driver test with the literal BIDS prefix, which those guards forbid in every Topic 3 doc.
- No identifier was involved, but the guards were right. I kept the v1 bytes in `verification/worker_M2_r4/superseded/` (addendum v1 `af805513…`, receipt v1 `4c1df35e…`; later also v2 `46527e6a…` / `db88f543…`; with a README), removed the prefix, disclosed the incident in §7, regenerated the receipt and reran everything (`final/fc3_*`).
- The checkpoint loop or the daemon may have committed v1 in between. That would be a root or daemon commit, not my git write.

## 2. Logic Chain

1. Each new test passes on the shipped code (O2, O5), so no possible real defect was found and the STOP condition did not trigger.
2. For each REQUIRED id, the patch applied verbatim from the verifier's harness produces a run in which all 121 pre-existing tests pass and at least one r4 test fails (O3). The mutant therefore survives the shipped suite, which reproduces the verifier's finding, and is killed by the new tests. This closes classes (a)–(d) as PI decision 6 defines them.
3. The killing tests are defect-specific:
   - The Family A mutants fail both the real-data regression and the synthetic re-derivation. FA11 fails only the synthetic test, by design, since it changes no real value.
   - T01, T02 and TJ03 fail the producer tests.
   - N01 fails both the hand-built and the computed Holm = raw cases.
   - VA01 and VA02 fail the corr-only stub and the computed witness.
4. The union under the 138-test suite matches FULL_v2 job for job (O4). Adding r4 broke no collection and changed no classification. U127 is the only survivor, as expected.
5. Every production pin and suite verifies (O5), and no src/ or scripts/ byte changed. The deliverables are pinned in the new receipt.

## 3. Caveats

- **Fail-fast union.** The union ran in fail-fast mode with a fast-first file order. That keeps the status comparison complete, but its per-job failure lists are not complete; FULL_v2 holds those. The named set ran without `-x`.
- **Split and restarted runs.** The evidence runs were split and restarted because of memory pressure from other workloads (O6). Each part ran on the same `tree_base_r4`, with the same specs and the same classification. Runner v2 and v3 changed only execution; diffs are reproducible from `bin/`.
- **The real-data test's output.** The class (a) real-data test reruns the frozen Family A script on the real pinned inputs in every suite run. Its output JSON (positions only) is left in pytest's base temporary directory. The dispatch asked for this test; addendum 06 §6 flags it for PI confirmation, like auditor_M2_r3_1 N3.
- **Exact replay.** The synthetic class (a) test replays the frozen seed schedule. It will fail on a seed or draw-order change even if the statistics stay correct, which is why MC01 and A09 = MC02 are now killed.
- **Token-level shapes.** The token-level fixtures have n > D, so the n < D Gram path is not exercised at token level. The synthetic Family A test exercises it.
- **Open items.** The r3 nonblocking findings are listed in addendum 06 §5 and are not fixed: VB02, the label misnomer, untested halts, tie-only mutants, N02, U127, skip-without-VRABES, basetemp residue, the production-script `exec_module`, the Pool deadlock, the stray bytecode and the stale notes.
- **Stray bytecode.** `src/topic3_spectral/__pycache__` (iteration 2) and `tests/topic3_spectral/__pycache__` (10-31T23:29:58Z) are untouched. They are the root's decision.
- **Git state.** It is the root's domain. The two r4 tests, addendum 06 and its receipt are new and uncommitted by me. The checkpoint loop or daemon may commit the `.md`/`.txt` files.
- **My own deviations.**
  - A first README for the stopped v2 run said no job had started; in fact the control had run. It was corrected in place, and the correction is marked inside the file.
  - One heredoc expanded backticks in a draft step. Nothing was written by it, and the step was redone from a script file.

## 4. Conclusion

M2 iteration 4 is complete within PI decision 6's fixed scope. Classes (a)–(d) are closed: all 26 named mutants are killed by r4 tests only, the union shows no regression, every suite, pin and C1 verify, and integrity holds (additive tests, verbatim mutants, raw logs with hashes, no production rerun). Next step for the root: the one-reviewer and one-auditor gate, then the victory audit.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt          # 67 OK
for r in output addendum_02 addendum_03 addendum_04 addendum_05 addendum_06; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=$PWD timeout 900 nice -n 10 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic3_spectral   # 138 passed
V=verification/worker_M2_r4; (cd $V && LC_ALL=C sha256sum -c --quiet EVIDENCE_MANIFEST_final_sha256.txt)      # evidence intact
# reproduce named kills (fresh output names; the runner refuses to overwrite):
cd $V/bin && /home/juke/superclaude-env/bin/python3 -B run_jobs_v3.py --set named --base ../tree_base_r4 --logs ../runs/CHECK_$(date +%s)_logs --out ../runs/CHECK_$(date +%s).json --expect-tests 138 --jobs 2 --min-avail-gib 14 --only N001,N012,N013,N022,N023,N024,N025
#   expect KILLED with failing_other == [] for every job
/home/juke/superclaude-env/bin/python3 -B -c "import json;print(json.load(open('../runs/SUMMARY_r4.json'))['summary'])"
```

The conclusion is invalidated by any of the following:
- a hash mismatch for the r4 tests (`ecceb134…`, `ab99b2b1…`);
- a REQUIRED mutant surviving the 138-test suite;
- any pre-existing test failing under a REQUIRED mutant, which would mean the kill is not attributable to r4;
- a union job whose status differs from FULL_v2;
- any change under `src/topic3_spectral` or `scripts/topic3_*.py`.
