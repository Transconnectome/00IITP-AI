# worker_M2_r3 — handoff (Hard), M2 Topic 3 iteration 3, 2026-11-01T06:15Z

Evidence lives in `/home/juke/git/00IITP-AI/verification/worker_M2_r3/`. The deliverables:
- `tests/topic3_spectral/test_verdict_rules_r3.py` (27 tests, sha256 58c64ccb…)
- `tests/topic3_spectral/test_token_stats_wiring_r3.py` (6 tests, b091b0b8…)
- `docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_05.md` (060b8c15…)
- `results/topic3/2026-10-31/addendum_05_sha256.txt` (6efd73ad…)

No `src/` or `scripts/` file was changed and no pinned file was edited. I made no git write and used 0 GPU.

## 1. Observation

**O1. r2b gate blocking classes.** I read each of these from its primary source:
- `orchestrator/M2_r2b_gate_record.json`;
- the five verifier `handoff.md` files;
- the harness files.

The blocking classes are: V01; the CI producer (P01–P03 / V06–V08 / A07); V05; A2/D3 rows (A01 / V13 / V28 / A06 / S03); and the token_stats wiring (V26 / V29 / X01 / X02).

**O2. Union of mutant sets.** `verification/worker_M2_r3/mutants/union_specs.py` reads the sets from 9 harness files by AST plus restricted eval:
- worker_M2_r2b's 67 (C 28 + MM 18 + KD 21);
- RV1 35, RV1R 8, RV2 25, CH1 29, CH2 34, AU 23.

That is 221 rows, merged into **151 unique patches**.

**O3. The shipped 88-test suite reproduces the verifiers' survivors** (`mutants/runs/S88_v2.json`, sha256 34da3012…, 03:38:59–04:03:23Z):
- 101 KILLED, 50 SURVIVED, 0 INVALID, 0 NOT_APPLIED;
- controls 88 passed;
- all 50 survivors are among those the verifiers reported.

**O4. The full suite (88 + 33 r3)** (`mutants/runs/FULL_v2.json`, e222e7f2…, 04:31:41–05:56:06Z, base tree `tree_base_v3` with the final r3 bytes):
- **150 KILLED, 1 SURVIVED, 0 INVALID, 0 NOT_APPLIED**;
- controls 121 passed, 0 skipped.
- 49 of the 50 shipped-suite survivors are killed. Every one of the 49 has at least one r3 test among its failing tests.
- The survivor is U127, challenger_2 A15 (the direction label for a mean of exactly 0). It is classified as equivalent in `mutants/survivor_classification.json`.
- The summary is `mutants/MUTANTS_SUMMARY.json` (fa7017ac…). The raw logs are in `runs/S88_v2_logs/` and `runs/FULL_v2_logs/`, with each log's sha256 recorded in the summary.

**O5. The new tests pass on shipped code.**
- In copied trees: `logs/dev_r3_draft2_shipped.log` and `logs/dev_r3_wiring_v3_shipped.log`, plus both FULL_v2 controls.
- On production (`final/post_pytest_topic3.log`): **121 passed**.

**O6. Final checks on production** (`final/post_*`, after the receipt was written):

| Check | Result |
|---|---|
| Old suite (`STRICT_E2E=1`) | 86 passed |
| topic1 | 88 passed |
| C1 | 67 OK, rc 0 |
| `output_sha256.txt` | 42 OK |
| `addendum_02_sha256.txt` | 1 OK |
| `addendum_03_sha256.txt` | 3 OK |
| `addendum_04_sha256.txt` | 2 OK |
| `addendum_05_sha256.txt` | 3 OK |
| `.pyc` diff vs `pycache_baseline_start.txt` | 0 added. 7 `src/topic4_resu` pyc were removed by another team; the 3 iteration-2 pyc in `src/topic3_spectral/__pycache__` are unchanged |
| `audit_layout.py` on the run root | PASS, findings [] |
| ID scan (BIDS prefix) over my outputs | no hits |
| Leftover processes | none |

**O7. Numeric corrections** (`probes/check_corrections.out.json`, from pinned JSON/npz only):
- H1b geometric-mean ratio − 1: HCP −10.7%, L1e-4 −3.2%, primary +4.6%, L5e-5 +8.2%. H1a: HCP −12.8%, primary +2.3%, L1e-4 +3.9%, L5e-5 +5.0%.
- CI half-widths of the primary contrasts: 0.00203–0.01442.
- `centered_eigs` on a 160×384 matrix returns 159 values; `cat_cov_eigs__L0` has 384 columns.

**O8. Git, read-only.** Addendum 03's commits are `4ce1917` (2026-10-31T12:31:25Z, the first) and `ef27b71`. `0db0336` does not touch addendum 03; it only carries the blob `725d5077…` unchanged.

**O9. Incidents** (both are runner problems, not test results; each has a README):
- `S88_v1` was aborted. The runner wrote the literal `<job tree>` into the JUnit XML, which broke the XML parser at U022.
- `FULL_v1` was stopped after its 50 priority jobs. X02 survived there, so a second wiring test was added and everything was rerun as FULL_v2.

Both runs' files are kept unchanged and are not used as evidence. I killed only my own processes.

**O10. Root checkpoint commits picked up drafts.** The root's 15-minute checkpoint loop committed four drafts of addendum_05 (`70bd178`, `6bf2de7`, `55ba1e0`, `08f7b6f`). None equals the final bytes 060b8c15…, so `git status` shows the file as modified. The receipt and the two tests are untracked. This was not my git write.

## 2. Logic Chain

1. **Blocking class 1 (V01).** The iteration-2 `_rec` set raw p = Holm p. The new tests use explicit raw p 0.03 < 0.05 ≤ Holm p 0.06, both hand-built and through the shipped producer at B = 9999, for H1a and H1b. FULL_v2 kills U057 with 4 r3 failures (O4).
2. **Blocking class 2 (CI producer).**
   - The CI test compares `ci95` with an independently written percentile bootstrap at the card's B = 9999 and level 0.95, using literal constants, not `PARAMS`. It checks the [lo, hi] order, the log scale (lo < mean < hi) and the 95% width.
   - The end-to-end fixture (skewed data, seed 50002) has a shipped Holm p of 0.031–0.032, a computed CI lower bound of −0.0014, and the verdict "killed".
   - U070, U071, U072 and U105 are all killed (O4).
3. **Blocking class 3 (V05).** Two tests, one hand-built and one computed, place a zoo checkpoint whose CI covers 0 and whose Holm p is < 0.05; it must count, giving "holds" with 2 of 3. U066 is killed.
4. **Blocking class 4 (A2/D3 rows).**
   - A row-identity spy on `paired_subsample_delta`, plus the A2 E1 values, kills U078.
   - The script-level spy on `topic3_subject_level.main()` (synthetic loaders, `dump` guarded, nothing written) kills U120 (V28) and U139 (S03).
5. **Blocking class 5 (token_stats wiring).**
   - The unmodified script runs in `tmp_path` on the pinned npz and must reproduce the pinned output.
   - The primary is identified from the data, the checkpoints are the 3 card zoo names, and the verdicts are recomputed with the card primary.
   - This kills V26 and X01. X02 is output-identical on the pinned data (O4/FULL_v1), so a re-signed-spectra run in which every primary choice gives a distinct verdict pair is required. It kills U091.
6. **Nonblocking classes named by ≥ 2 verifiers.**
   - D2 (a null of chosen size, so p_low = 0.02, 0.03 or 0.025) kills U081 and U126.
   - The closed boundaries (hand-built primary CI; identical matrices giving an interval of exactly [0, 0] for D1/D3) kill U059, U060, U093, U104, U079, U080, U108, U122, U123 and U143.
   - Because constructed fixtures reach the boundaries, none is classified as measure-zero.
   - The cheap one-verifier extras (PARAMS pin, first key, Holm cap, zero-mean sign, H4 seed rule, refusals, ties, exact replays) kill the remaining s88 survivors except A15.
7. **A15 is the one survivor.** It changes only the direction label of a primary whose mean is exactly 0. Card §5 defines no direction for a zero mean, and through the producer such a mean has p = 1, so the verdict is the same. That makes it equivalent with respect to all card outputs, and testing it would mean inventing a label.
8. **No real verdict changes.** The wiring test reproduces all 508 non-run leaves of the pinned Family B output within rel 1e-9, and the production suite passes.

## 3. Caveats

- All 33 tests were written after the results existed. They are regression guards, not a pre-registration.
- The boundary fixtures are constructed. Real continuous bounds practically never equal 0.0.
- The exact-replay tests pin the frozen seed schedule and draw order on purpose.
- The Family B wiring tests need the VRABES `layer_3.npz` and skip if it is absent, like `test_io_contract.py`. They add about 46 s to the suite.
- The Family A script is not rerun. Its wiring is checked in-process with synthetic loaders.
- The first wiring test detects behaviour, not code bytes; run-record code hashes are excluded from its comparison.
- The S88_v2 runner snapshot (`runs/S88_v2_runner_snapshot.py`) was reconstructed by removing the later `--priority` addition. Its sha256 matches the `runner_sha256` recorded in S88_v2.json (6614112d…).
- I did not delete the iteration-2 pyc in `src/topic3_spectral/__pycache__`. They are not mine; the owner decides.
- Verifier statements used in addendum_05 §5 were re-checked where they are numeric (O7) or git-based (O8). The transcript times (12:17:16Z) rest on auditor_M2_r2b_1's native-transcript evidence.

## 4. Conclusion

All five blocking classes of the r2b gate are closed by additive tests. Each listed mutant was reproduced verbatim from the verifier's harness and shown to survive the shipped 88-test suite and to be killed by the r3 tests in copied trees.

Across the union of 151 unique patches, 150 are killed and 1 is equivalent (A15). There are 0 INVALID and 0 NOT_APPLIED.

Addendum 05 records:
- the gate outcome;
- the class-by-class test mapping;
- the mutant table;
- the verifier-found corrections to addenda 03/04 and the report;
- the stray iteration-2 bytecode.

It is pinned with both test files in `addendum_05_sha256.txt`. The next step belongs to the root: the 5-verifier gate for iteration 3, then the victory audit.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # 67 OK
for r in output addendum_02 addendum_03 addendum_04 addendum_05; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${r}_sha256.txt; done
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD OMP_NUM_THREADS=2 nice -n 10 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic3_spectral   # 121 passed
V=verification/worker_M2_r3
bash $V/make_tree.sh $PWD/$V/tree_check            # copied tree, manifest vs production
cd $V/mutants && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I run_union.py --base ../tree_check \
   --logs runs/CHECK_logs --out runs/CHECK.json --suite full --jobs 2 --only U057,U072,U078,U091,U118,U120,U066
#   expect all KILLED with r3 tests failing; with --suite s88 the same jobs SURVIVE
/home/juke/superclaude-env/bin/python3 -I union_specs.py list | tail -151           # the 151 patches and their sources
```

Invalidation conditions:
- any receipt fails;
- the r3 test files differ from 58c64ccb… / b091b0b8…;
- a mutant listed as KILLED survives a rerun with the r3 tests;
- a test fails on unmutated production.
