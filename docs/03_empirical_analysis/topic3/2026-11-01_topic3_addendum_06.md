# Topic 3 addendum 06: M2 iteration 4 (final, fixed scope) — guard tests for the four blocking classes of the r3 gate, named-mutant and union runs, known open items (2026-11-01)

Written 2026-11-01 (UTC) by worker_M2_r4, the iteration-4 worker of M2. The PI fixed the scope of this last iteration on 2026-11-01 (`.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md`, decision 6; §2 below). This addendum is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report and addenda 01–05 are unchanged. They stay pinned in `results/topic3/2026-10-31/output_sha256.txt` and `addendum_02/03/04/05_sha256.txt`, and all five receipts verify (§7). The sha256 of this file and of the two new test files is in `results/topic3/2026-10-31/addendum_06_sha256.txt`.

**No verdict changes.**
- No file in `src/` or `scripts/` was changed. No card was re-frozen. No new estimand was computed.
- No real-data analysis was rerun in the production tree. One new test (class (a), §3) runs the unmodified Family A script on the pinned inputs inside pytest's temporary directory and compares its output with the pinned file. That output stays in pytest's temporary directory (§6), and nothing is written to the production tree.
- The verdicts in report §4 stand: H1a holds, H1b not replicated, D1 robust and not a per-channel-scale effect, D3 ordering reproduces, J1 artefact, H2 untested. Every r3 verifier independently reproduced the pinned numbers. The gate failed on missing guards, not on a wrong result.

## 1. Outcome of the r3 gate (iteration 3)

Source: `.agents/teamwork/tw-20261031-four-topics/orchestrator/M2_r3_gate_record.json` and each agent's `handoff.md`.

| Agent | Verdict | Blocking items |
|---|---|---|
| worker_M2_r3 | DONE | none (its claim: the five r2b classes closed; 150 of 151 union patches killed, U127 equivalent) |
| reviewer_M2_r3_1 | REQUEST_CHANGES | B1: the primary-side Holm guard is one-sided. N01 (`analysis.py:191` reads `min(1, 2 p_signflip)`, i.e. Bonferroni) survives the 121-test suite and turns "holds" into "killed" at B = 9999 when the key contrast is the larger p |
| reviewer_M2_r3_2 | REQUEST_CHANGES | The Family A E1/A2 columns printed in report §2 are unguarded: B_A2_iid_at_n25, B_E1_iid_wrong_n and B_E1_null_q05 change printed cells on the real inputs; B_E1_pr_over_n changes JSON-only values |
| challenger_M2_r3_1 | REFUTED | (i) Token-job producer: CR3_T02 (covPR of L2 from the correlation eigenvalues) turns H1b into "holds" and CR3_T01 (corrPR of L3 from the covariance eigenvalues) reverses H1a, both on an exact counterfactual of the pinned spectra. (ii) Family A has no real-data regression: CR3_A01 / A02 / A05 / A07 / A08 move printed numbers |
| challenger_M2_r3_2 | REFUTED | (1) D1 corr-only branch: VA01 / VA02 output a robust-drop verdict when cov lo ≤ 0 < corr lo. (2) Family A numbers: FA01–FA10. (3) Low severity: the dead-column floor at two call sites (TJ03, FA11) and VB02 |
| auditor_M2_r3_1 | CLEAN | none |

## 2. PI decision 6: the fixed scope of this iteration

PI decision 6 (2026-11-01, about 16:4x KST) chose "범위 고정 마지막 1회 (권장)": one final M2 iteration whose scope is fixed to four r3 blocking classes:
- (a) Family A full-output regression;
- (b) the token_job producer's per-layer inputs;
- (c) primary-side Holm vs Bonferroni (N01);
- (d) the D1 corr-only verdict branch (VA01 / VA02).

The gate checks only three things: those four classes are closed (the named mutants are killed), nothing regresses (all suites, pins, C1), and integrity. New mutants beyond these classes are reported as nonblocking, not as gate failures. There is no M2 iteration after this one.

The dispatch assigns the two dead-column-floor mutants of challenger_M2_r3_2's low-severity item to these classes: TJ03 to (b) and FA11 to (a). VB02, from the same item, is outside the fixed scope and is listed in §5.

## 3. The four classes and the tests that close them

Two new files, written **after** the real-data results existed (17 tests; the suite now has 138):
- `tests/topic3_spectral/test_regression_r4.py` (7 tests): classes (a) and (d).
- `tests/topic3_spectral/test_token_level_r4.py` (10 tests): classes (b) and (c).

No existing test, no `tests/topic3_spectral/helpers.py`, and no `src/` or `scripts/` file was edited. Every test passed on the shipped code before any mutant was run (§7). Each named mutant is reproduced verbatim from the verifier's own harness file and shown in copied trees to be killed by the r4 tests, with every pre-existing test passing (§4).

| Class (card rule) | Named mutants | r4 tests |
|---|---|---|
| (a) Family A output equals the frozen procedure's output (card §4 E1 / A1 / A2; report §2 tables and the R1 / R3 bases) | reviewer_2: B_A2_iid_at_n25, B_E1_iid_wrong_n, B_E1_null_q05, B_E1_pr_over_n; challenger_1: CR3_A01, A02, A05, A07, A08; challenger_2: FA01–FA11 | `test_subject_level_script_reproduces_every_pinned_family_a_value`: copies `scripts/topic3_subject_level.py`, `scripts/topic3_common.py`, `src/topic3_spectral`, the card and `card_sha256.txt` from the tree under test into `tmp_path` and runs the unmodified script there (OUT follows the script location, `scripts/topic3_common.py:12`). The 7 pooled inputs are read in place under their sha256 pins. The key sets must be equal first; then all 300 leaves of `results` must equal the pinned `family_A_subject_level.json` (checked against `output_sha256.txt`) at rel 1e-9, abs 1e-12, and the deterministic run fields (card hash, PARAMS, input hashes, alignment) must be equal. About 21 s. Skips only if one of the 7 pinned inputs is absent; a hash mismatch fails it. `test_subject_level_matches_card_definitions_on_synthetic_matrices`: re-derives every E1 / D2 / A1 / D1 / A2 / D3 value of `subject_level` from the card §3/§4 definitions with independent numpy code (D × D covariance, `np.corrcoef` with the card floor, textbook jackknife) on synthetic matrices, with reduced reps and S but the card's m, floor and the frozen seed offsets. One L0 column has SD about 1e-5 × the median, so the floor matters (corrPR changes by 1.8% without it); this is the only test that sees FA11, which changes no real-data value |
| (b) The token-job producer returns the card §3/§5 per-layer values | challenger_1: CR3_T01, CR3_T02; challenger_2: TJ03 | `test_subject_summary_matches_card_definitions_for_every_variant`: 5 synthetic subjects × 7 frames in the ver11 dump layout (small dims). For all 5 variants it compares, with independent numpy code, the concatenated covPR and corrPR (the H1a/H1b primary inputs and the H1c–H1e secondary inputs), the dropped-column count, the stored eigenvalues, the per-frame values, the H4 values (seed (20261031, position, frame)) and the pooled vectors. Preconditions: \|log covPR − log corrPR\| > 0.05 for L2 and L3 (observed 0.24–0.98 in every subject); the L3 final-LN gain has a near-dead channel (γ = 1e-5, SD about 2e-5 × median: dropped, count 1) and a small live one (about 0.02 × median: kept); keeping the dead channel would change L3 corrPR by about 3.2%. `test_packed_spectra_feed_the_card_contrasts`: the same subjects through `pack_summaries` → `token_level_checkpoint`; each of the 2 primary and 3 secondary mean log ratios must equal the mean of the card §5 log ratios of the directly computed values |
| (c) The primary needs **Holm** p < 0.05, also when its contrast is the larger p (card §5) | reviewer_1: N01 | `test_primary_whose_holm_p_equals_its_raw_p_counts_as_significant[p = 0.026, 0.04, 0.049; H1a, H1b]`: hand-built records, checked against `resampling.holm` for consistency. The other primary has raw p 1e-4, so the key contrast's Holm p equals its raw p (< 0.05) while Bonferroni would give 2p ≥ 0.05. CI (0.005, 0.055); 3 agreeing zoo checkpoints. Must give `primary_significant` True and "holds". `test_primary_holm_equal_to_raw_p_holds_end_to_end_at_card_resolution[H1a, H1b]`: the shipped `token_level_checkpoint` at B = 9999 (seed 2000, t = 2.15, from `verification/worker_M2_r4/probes/seed_search_n01.out.json`). H1a raw = Holm p = 0.0380, CI [0.00062, 0.0107]; H1b raw = Holm p = 0.0347, CI [0.00062, 0.0108]; 3 strongly agreeing zoo checkpoints; must give "holds". Both start from reviewer_M2_r3_1's demo test (sha256 `e09ff20c…`), which had the computed case for H1b only |
| (d) D1: "L2 > L3 robust" iff the covPR interval lo > 0, whatever corrPR shows (card §4 D1) | challenger_2: VA01, VA02 | `test_d1_verdict_follows_the_card_for_all_four_interval_cases[4 cases]`: stubbed L2−L3 intervals (identified by matrix identity and estimator), including the corr-only case (cov lo −0.3, corr lo +0.4), which must give "drop not robust" with `L2_gt_L3_cov_robust` False and `L2_gt_L3_corr_robust` True. `test_d1_corr_only_case_computed_by_the_shipped_procedure`: challenger_2's witness construction (L2 = independent columns with SD j⁻¹, L3 = rank-6 structure with equal column SDs) through the shipped `subject_level` at the card's m = 28, S = 2000 and floor (only the E1 reps are reduced; D1 does not read them). The computed intervals are cov [−2.942, −1.660] and corr [+13.877, +15.440], the same as the challenger's card-parameter witness, so the verdict must be "drop not robust" |

## 4. Named mutants and the union run

### 4.1 Method

- **Specs, verbatim.** `verification/worker_M2_r4/bin/named_specs.py` reads each named mutant's (file, old, new) from the verifier's own harness source with `ast`. It evaluates only top-level literal assignments and the target variable, with no builtins except `dict`, and imports or executes no harness module. The four harness files and their sha256:
  - reviewer_M2_r3_1 `my_mutants.py` `SPECS` (`17a30dca63a1…`);
  - reviewer_M2_r3_2 `run_mutants.py` `MUTANTS` (`ca6d7381474c…`);
  - challenger_M2_r3_1 `mutants/specs.py` `MUTANTS` (`d5f73f38e358…`);
  - challenger_M2_r3_2 `mutants/my_specs.py` `SPECS` (`0be048a3a82c…`).
- **Merging.** Ids whose patched file is byte-identical are run as one job and reported under every source id. Two examples: B_A2_iid_at_n25 = CR3_A01 = N03, and B_E1_null_q05 = CR3_A05 = FA03. This gives 32 jobs: 26 REQUIRED ids (the dispatch's list) and 16 EXTRA ids, which are the r3 survivors the verifiers called nonblocking, run only to report their status.
- **Union.** The union is worker_M2_r3's own `union_specs.py`, copied byte-identical (sha256 `706ef81b…`, equal to `FULL_v2.json` `_meta.union_specs_sha256`). It yields the same 151 job ids and the same (file, old, new) triples as FULL_v2, read from the same 9 source files with the same sha256.
- **Tree.** `tree_base_r4` is a byte copy of production made by `bin/make_tree.sh` (a copy of challenger_M2_r3_1's script). It has 123 files, the manifest checks against production, and it contains the two frozen r4 tests (`ecceb134…`, `ab99b2b1…`).
- **One job (named set).** Each job runs on a fresh copy of the tree with one patch applied (the old string must occur exactly once). It then runs the full `tests/topic3_spectral` suite (138 tests), without `-x`, under `timeout 900 nice -n 10`, with `PYTHONDONTWRITEBYTECODE=1`, 2 BLAS threads, and `--basetemp`/`TMPDIR` inside the copy. At most 2 jobs run at a time. The union differs only in using `-x` and a fast-first order of the test files (§4.3).
- **Classification.** KILLED means rc 1 with at least one failing test. SURVIVED means rc 0. INVALID means anything else, a test count other than 138 (in the fail-fast union: a SURVIVED job with fewer than 138), or any skipped test. An INVALID job is rerun and never counts as a kill.
- **Attribution.** `failing_other` lists the failing tests outside the two r4 files. A KILLED job with `failing_other` = [] ran all 121 pre-existing tests and passed them, so the same patch **survives the shipped 121-test suite** and is killed by r4 tests only. One run therefore shows both directions.
- **Host memory pressure (execution, not results).**
  - During the first run (runner v1, `bin/run_jobs.py`), other workloads held MemAvailable at 7–10% of 120 GiB. 17 pytest processes of this worker ended with rc −15 (SIGTERM) at times when earlyoom logged SIGTERMs (`journalctl -u earlyoom`); they are INVALID. The SIGTERM left 15 hung `topic3_token_job.py` Pool processes from `test_token_job_driver.py` behind; they were terminated by PID (`logs/orphans_killed_0848.txt`). This is the deadlock hazard of §5 item 13.
  - The v1 run was stopped. Its 15 valid records (the control and 14 KILLED jobs, each with 138 tests, 0 skipped) are kept (`runs/EVID_named_r4.json.partial`).
  - The other jobs and the union were run with runner v2 (`bin/run_jobs_v2.py`) and runner v3 (`bin/run_jobs_v3.py` = v2 plus an optional fail-fast mode, used only for the union). Their changes are confined to execution, and patching, suite, classification and attribution are unchanged:
    - an attempt starts only when MemAvailable is at or above a gate, one launch at a time and 20 s apart. The gate was 15.5 GiB for the named reruns (v2b, v3), and 15.5 then 14.0 GiB for the union (§4.3). A first v2 run with an 18 GiB gate passed its control and was stopped while waiting (`runs/EVID_named_r4_v2_STOPPED_README.txt`);
    - pytest runs in its own session, and the whole process group is terminated after each attempt;
    - an INVALID attempt is retried automatically, on a fresh copy, under its own log names.
  - Every stop and restart is documented in `runs/*_STOPPED_README.txt` and `runs/EVIDENCE_batch.log`.

### 4.2 Named mutants: all 26 required ids are killed by the r4 tests only

All 32 jobs have a valid record. Each record has 138 tests and 0 skipped. Every control passed with 138 tests: v1 start, v2b start, and v3 start and end. "Pre-existing failing" counts failures among the 121 shipped tests. For every KILLED job it is 0, so each of these patches **survives the shipped 121-test suite** and is killed by r4 tests only. Run tags: v1 = `runs/EVID_named_r4.json.partial`, v2b = `runs/EVID_named_r4_v2b.json.partial`, v3 = `runs/EVID_named_r4_v3.json`. Each record names its raw log and JUnit file, with their sha256.

| Class | Job | Source ids (byte-identical patched file) | Status (run) | Pre-existing failing | r4 tests failing |
|---|---|---|---|---|---|
| (a) | N002 | reviewer_2 B_A2_iid_at_n25 = challenger_1 CR3_A01 (= reviewer_1 N03, extra) | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N006 | reviewer_2 B_E1_iid_wrong_n | KILLED (v2b) | 0 | FA-real, FA-synth |
| (a) | N007 | reviewer_2 B_E1_null_q05 = challenger_1 CR3_A05 = challenger_2 FA03 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N008 | reviewer_2 B_E1_pr_over_n = challenger_2 FA01 (= challenger_1 CR3_A03, extra) | KILLED (v2b) | 0 | FA-real, FA-synth |
| (a) | N009 | challenger_1 CR3_A02 = challenger_2 FA08 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N010 | challenger_1 CR3_A07 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N011 | challenger_1 CR3_A08 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N014 | challenger_2 FA02 (= challenger_1 CR3_A04, extra) | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N015 | challenger_2 FA04 (= challenger_1 CR3_A06, extra) | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N017 | challenger_2 FA05 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N018 | challenger_2 FA06 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N019 | challenger_2 FA07 | KILLED (v1) | 0 | FA-real, FA-synth |
| (a) | N020 | challenger_2 FA09 | KILLED (v2b) | 0 | FA-real, FA-synth |
| (a) | N021 | challenger_2 FA10 | KILLED (v2b) | 0 | FA-real, FA-synth |
| (a) | N022 | challenger_2 FA11 | KILLED (v2b) | 0 | FA-synth only (FA11 changes no real-data value) |
| (b) | N012 | challenger_1 CR3_T01 | KILLED (v1) | 0 | TJ-direct, TJ-pack |
| (b) | N013 | challenger_1 CR3_T02 | KILLED (v1) | 0 | TJ-direct, TJ-pack |
| (b) | N023 | challenger_2 TJ03 | KILLED (v2b, 2nd attempt) | 0 | TJ-direct, TJ-pack |
| (c) | N001 | reviewer_1 N01 | KILLED (v1) | 0 | all 6 hand-built cases and both computed cases (8 failures) |
| (d) | N024 | challenger_2 VA01 | KILLED (v2b) | 0 | D1-table (corr-only case), D1-computed |
| (d) | N025 | challenger_2 VA02 | KILLED (v2b) | 0 | D1-table (corr-only case), D1-computed |

Abbreviations: FA-real = `test_subject_level_script_reproduces_every_pinned_family_a_value`; FA-synth = `test_subject_level_matches_card_definitions_on_synthetic_matrices`; TJ-direct = `test_subject_summary_matches_card_definitions_for_every_variant`; TJ-pack = `test_packed_spectra_feed_the_card_contrasts`; D1-table = `test_d1_verdict_follows_the_card_for_all_four_interval_cases`; D1-computed = `test_d1_corr_only_case_computed_by_the_shipped_procedure`.

**EXTRA ids (the r3 nonblocking survivors; status report only).**
- KILLED, by FA-real and FA-synth, with 0 pre-existing failures: reviewer_1 N03 (N002) and N04 (N003); challenger_1 CR3_A03 (N008), CR3_A04 (N014), CR3_A06 (N015) and CR3_A09 = challenger_2 MC02 (N016); challenger_2 MC01 (N027).
- SURVIVED, with all 138 tests passing: reviewer_1 N06 (N004) and N12 (N005); challenger_2 VB02 (N026), FA13 (N028), FA14 (N029), GD01 (N030), GD02 (N031) and GD03 (N032). These are §5 items 1, 3 and 4.

**Attempts.**
- 17 v1 records are INVALID: rc −15 (SIGTERM), at times when earlyoom logged SIGTERMs (§4.1).
- Under v2b, TJ03 (N023) and MC01 (N027) each had one INVALID attempt (rc −15) before the valid one.
- None of these attempts counts as a kill.

### 4.3 Union run: no regression; U127 is again the only survivor

worker_M2_r3's 151-patch union was rerun on `tree_base_r4` with the full 138-test suite. To keep the run feasible under the host memory pressure (§4.1), it used runner v3 in **fail-fast mode** (`pytest -x`). The 16 test files were passed in fast-first order, by ascending per-file duration measured on production (`final/pre_topic3_b.junit.xml`).
- **Coverage.** The tests are independent (each uses its own `tmp_path` or `monkeypatch`), and every job still collects all 138 tests.
- **Validity.** A SURVIVED job must run and pass all 138. A KILLED job stops at its first failing test. A collection error (rc 2) would have been INVALID.
- **Records.** The run was split in two because the first part's 15.5 GiB gate stalled: `runs/EVID_union_r4_v3ff.json.partial` (29 jobs, gate 15.5 GiB) and `runs/EVID_union_r4_v3c.json` (the other 122, gate 14.0 GiB). Every control passed with 138 tests (v3ff start; v3c start and end). No attempt was INVALID.

| | worker_M2_r3 FULL_v2 (121 tests, no `-x`) | this run (138 tests, `-x`) |
|---|---|---|
| KILLED | 150 | 150 |
| SURVIVED | 1 (U127) | 1 (U127, 138 passed) |
| INVALID / NOT_APPLIED | 0 / 0 | 0 / 0 |

- **Status per job.** No job differs from FULL_v2.
- **First failing test.** For each of the 119 jobs whose first failing test is a pre-existing one, that test is among the tests FULL_v2 recorded as failing for the same job.
- **Jobs stopped first by an r4 test.** For the other 31 jobs, the first failing test is an r4 test, because `test_token_level_r4.py` comes early in the fast-first order. FULL_v2 already shows each of the 31 killed by pre-existing tests.
- **Summary file.** `runs/SUMMARY_r4.json` (built by `bin/summarize.py` from the raw records).

U127 (challenger_M2_r2b_2 A15, `sign < 0` → `sign <= 0`) changes only the `direction` label of a primary whose mean log ratio is exactly 0, a case the card does not define. Its verdict and agreement count are unchanged, and the shipped sign-flip test gives p = 1 for an exactly-zero mean. It stays classified as equivalent (§5 item 6).

## 5. Known open items (r3 nonblocking findings, not fixed here)

PI decision 6 fixes the scope, so these items are recorded, not fixed. The status after iteration 4 is the result of the runs in §4 where the item is a mutant.

| # | Item (where reported) | Status after iteration 4 |
|---|---|---|
| 1 | **VB02**: the direction and agreement sign taken from the CI midpoint instead of mean d (`analysis.py:190`). In a "killed" record with mean d +0.002 it changes `direction` and `n_other_checkpoints_agreeing` (0 → 3). It never flips a verdict and is inactive on the real data (challenger_M2_r3_2, low-severity item 3) | SURVIVES (job N026, all 138 tests pass). Outside the fixed scope (§2) |
| 2 | **Label for one case.** A primary with Holm p ≥ 0.05 and a CI that excludes 0 is labelled "killed (primary CI includes 0)"; card §5 names no outcome for it (all four r3 verifiers; addenda 03 §3 and 05 §5) | Open. It is a `src/` label and src is frozen. It is unreachable on the real data (every primary Holm p is 0.0002) |
| 3 | **Halts left untested.** The card §2 halts in `topic3_subject_level.py` (N06: `same_order` check off; N12: BrainJEPA left out of the order check; GD02: row-order halt removed) and the `topic3_token_stats.py` halts GD01 (primary pooled-L3 identity) and GD03 (positions) (reviewer_M2_r3_1 N2, challenger_M2_r3_2) | All SURVIVE (all 138 tests pass): N06 (N004), N12 (N005), GD01 (N030), GD02 (N031) and GD03 (N032). All are equivalent on valid inputs: the pinned hashes and job checks make the halted states unreachable |
| 4 | **Tie-only mutants.** FA13 (p_low counts strict ties) and FA14 (`frac_positive` with ≥) differ only at exact ties; `frac_positive` is not a card quantity (challenger_M2_r3_2) | Both SURVIVE (all 138 tests pass): FA13 (N028) and FA14 (N029). |
| 5 | **The zoo-side Bonferroni twin N02.** It is killed only incidentally, by the r3 skewed fixture (Holm p = raw p = 0.032 / 0.031); there is no deliberate zoo-side Holm = raw test (reviewer_M2_r3_1 N4) | Killed by the r3 suite in reviewer_M2_r3_1's run 2 (`verification/reviewer_M2_r3_1/MY_MUTANTS_run2.json`). Additive tests cannot revive it. Not rerun here, and no zoo-side test was added (class (c) is primary-side) |
| 6 | **U127** (challenger_M2_r2b_2 A15, `sign < 0` → `sign <= 0`): changes only the `direction` label of a primary whose mean is exactly 0, a label the card does not define. Every r3 verifier accepted it as equivalent | Still the only union survivor (§4.3: 138 of 138 tests pass). Equivalent with respect to every card-defined verdict, as all r3 verifiers agreed |
| 7 | **Addendum 05 §6 wording.** "the card parameters that define them are pinned by `test_params_equal_frozen_card`" is inaccurate: pinning PARAMS does not pin how a parameter is used (FA09 halves `iid_reps` at the call site with PARAMS unchanged) (challenger_M2_r3_2) | The text stays as pinned. FA09 is now killed by both class (a) tests (§4) |
| 8 | **Addendum 05 omissions.** It does not mention `tests/topic3_spectral/__pycache__/` (3 `.pyc`, 2026-10-31T23:29:58Z) or worker_M2_r3's real-data timing probe of `topic3_token_stats.py` in a copied tree (reviewer_M2_r3_2) | Recorded here. Both bytecode folders (`src/topic3_spectral/__pycache__/`, 3 files from 2026-11-01T00:39:14Z, and the `tests/` one) are still present and unchanged; this worker neither created nor removed them, and the root decides whether to delete them |
| 9 | **An inconsistent hand-built record.** `test_primary_raw_p_below_alpha_but_holm_p_not_is_not_significant` pairs Holm p 0.06 with an "other" record whose raw p is 1e-4, which Holm would not give. It is immaterial, because the rule reads only the per-key fields (reviewer_M2_r3_2) | The r3 file is pinned and unchanged. The r4 hand-built records are Holm-consistent, and the test asserts this against `resampling.holm` |
| 10 | **Guards that skip without VRABES.** The Family B wiring and refusal tests skip when the VRABES checkout is absent (reviewer_M2_r3_2; auditor_M2_r3_1 N2). The new class (a) real-data test does the same when a pinned input is absent | Open. Class (a) keeps a VRABES-independent guard (the synthetic test, §6). The Family B wiring and refusal tests have none |
| 11 | **Real-data-derived files in pytest's base temporary directory** (spectra copies and the Family B output from the r3 tests; auditor_M2_r3_1 N3). The class (a) real-data test adds a Family A output JSON there | Open; disclosed in §6. No identifiers (positions only) |
| 12 | **Bytecode from importing a production script.** `test_subject_level_script_passes_the_neurostorm_alignment_positions` calls `exec_module` on the production `scripts/topic3_subject_level.py`, which would write `scripts/__pycache__/` if the suite ran without `PYTHONDONTWRITEBYTECODE` (auditor_M2_r3_1 N4) | Open. The r4 tests import no production script: the class (a) test runs a copy in `tmp_path` as a subprocess with `PYTHONDONTWRITEBYTECODE=1` |
| 13 | **A possible deadlock.** `test_token_job_driver.py` can hang if a Pool worker is OOM-killed (reviewer_M2_r3_2) | Open (a test edit is out of scope). It happened in this iteration. Under host memory pressure from other work, pytest processes of v1 were SIGTERMed, and 15 Pool processes of this test were left hung until this worker terminated them (§4.1). Runners v2 and v3 terminate each job's process group. After that, no attempt hung or reached the 900 s timeout |
| 14 | **Family A descriptive survivors reported as nonblocking in r3**: CR3_A03 / A04 / A06 / A09 (challenger_M2_r3_1), N03 / N04 (reviewer_M2_r3_1 N1), MC01 / MC02 (challenger_M2_r3_2) | Now KILLED by both class (a) tests, with 0 pre-existing failures: N03 (N002), N04 (N003), CR3_A03 (N008), CR3_A04 (N014), CR3_A06 (N015), CR3_A09 = MC02 (N016) and MC01 (N027). The seed-offset mutants (CR3_A09 = MC02, MC01) die because the tests replay the frozen seed schedule (§6), not because the card fixes the offsets. |
| 15 | **Stale notes and records.** The note "addendum_05 modified vs HEAD" is stale (root checkpoint `a910c53` holds the final bytes `a4001f09…`). A fifth checkpoint draft of addendum 05 (`b91143c`) is missing from worker_M2_r3's list. The S88_v2 base tree was deleted and only its manifest kept. Some verifier logs echo the literal BIDS prefix from the shipped test source, which is not an identifier (reviewers 1–2, challenger_2, auditor) | Informational; no action |
| 16 | **H2** (random-init control) | Untested, as card §6 pre-specified |

## 6. Limits of these tests

- All 17 tests were written **after** the real-data results existed. They are regression guards for the shipped code, not a pre-registration.
- **Real-data test.** The class (a) real-data test needs the 7 pinned VRABES pooled inputs (read in place, read-only, sha256-pinned) and skips if one is absent, like the Family B wiring tests. The synthetic class (a) test does not skip: in the §4 runs it alone fails on every named class (a) mutant (FA11 included), so the class stays guarded without VRABES, though not on the real inputs.
- **What the real-data test leaves behind.** It reruns the Family A script on the real pinned inputs in every suite run (about 21–30 s). Its output, a subject-level summary JSON keyed by position with no identifiers, is left in pytest's base temporary directory (`/tmp/pytest-of-juke/…`) until pytest prunes it, like the Family B outputs and spectra copies of the r3 wiring tests (auditor_M2_r3_1 N3). The dispatch for this iteration asked for exactly this test. The PI may still want to confirm that this reading of "no rerun" (PI decisions 1 and 6) is acceptable.
- **Exact replay.** The synthetic class (a) test and the class (b) H4 check pin the frozen seed schedule and draw method (iid draws, column-permutation method, subsample index sets), not only the statistics' definitions. A future seed or draw-order change would fail them even if the statistics stayed correct, which is intended while the card is frozen. This is why the seed-offset mutants CR3_A09 = MC02 and MC01 are now killed (§5). The card fixes only the base seed.
- **Determinism.** The real-data comparison uses rel 1e-9, abs 1e-12 with 2 BLAS threads. The r3 verifiers' unmutated reruns at 2 threads matched all 300 leaves: exactly for challenger_M2_r3_2 (`reruns/famA_CONTROL.json`, max rel diff 0.0), and at rel 1e-9 for challenger_M2_r3_1 (`logs/famA_control.json`, 0 of 300 differ). The documented production command used OMP_NUM_THREADS=4. This test asserts only the rel 1e-9 agreement.
- **Synthetic shapes.** The class (b) fixtures have more tokens than channels, so the Gram path of `centered_eigs` (n < D, which the real 1120 × 1536 token matrices take) is not exercised at token level. The synthetic Family A test does exercise it (A2 subsamples of 12 rows, n = 25 with D up to 36).
- **Hand-built and stubbed records.** The class (c) hand-built records and the class (d) stubs reach the rule directly. The computed tests show that each case also arises through the shipped producer at the card's resolution. They say nothing about how often it arises.
- H2 (random-init control) remains untested, as card §6 pre-specified.

## 7. Checks, compute and conduct

These checks ran on the production tree on 2026-11-01 from 11:24:59Z to 11:27:14Z, after every mutant run had ended and before this file and its receipt existed (`verification/worker_M2_r4/bin/final_checks.sh fc1`, logs `verification/worker_M2_r4/final/fc1_*`). The same script was rerun after the receipt was written. In that run (`final/fc2_*`) the shipped C4 guards `test_outputs_no_ids.py` and `test_outputs_scanned_nonempty.py` failed on the first version of this file: §7 quoted the synthetic subject names of the shipped `test_token_job_driver.py` with the literal BIDS subject prefix, a byte string those guards forbid in every Topic 3 doc. No identifier was involved, but the guards are right to fail. The text was corrected, the receipt regenerated, and the checks rerun.
- **The reruns.** earlyoom SIGTERMed the fc3 topic3 and old-suite runs and the fc4 topic3 run (rc 143, INVALID; `final/fc3_INVALID_README.txt`, `final/fc4_topic3_INVALID_README.txt`). The valid post-correction evidence is `final/fc4_*` (old suite, topic1, C1, receipts, bytecode; `bin/final_checks_v2.sh`, which waits for memory before each suite) and `final/fc5_topic3.*` (topic3).
- **This version (v3).** It corrects two statements of v2 §7: this pointer to the rerun logs, and the hit list of the identifier scan below. The checks are rerun once more with v3 in place (`final/fc6_*`).
- **Superseded bytes.** v1 (sha256 `af805513…`, receipt `4c1df35e…`) and v2 (`46527e6a…`, receipt `db88f543…`) are kept in `verification/worker_M2_r4/superseded/` with a README. Between versions, the 15-minute checkpoint loop or the host daemon may have committed v1 or v2; that is not this worker's git write.
- **Suites.**
  - `tests/topic3_spectral`: 138 passed, 0 skipped (121 shipped + 17 r4). The class (a) real-data test took 20–21 s; the 17 r4 tests add about 25 s to the suite.
  - The old suite (`STRICT_E2E=1`, `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed.
  - `tests/topic1_lagmotif`: 88 passed.
  - Before any mutant run, the topic3 suite with the r4 files in place also passed: 138 passed, 0 skipped (`final/pre_topic3_b.*`). An earlier attempt was cut at 52% by the shell tool's 120 s limit, with no failure; it is INVALID and documented in `final/pre_topic3_INVALID_README.txt`.
- **C1.** `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives 67 OK, rc 0.
- **Receipts.** `output_sha256.txt` 42 OK, `addendum_02` 1 OK, `addendum_03` 3 OK, `addendum_04` 2 OK, `addendum_05` 3 OK. `code_sha256_at_freeze.txt` differs only for `scripts/topic3_launch_connectome.py`, which is pre-existing, disclosed in addendum 01 item 2 and pinned in `output_sha256.txt`. So no file in `src/` or `scripts/` changed.
- **Bytecode.** The `.pyc` listing of `src/`, `scripts/` and `tests/` was taken before any work (`verification/worker_M2_r4/logs/pyc_list_start.txt`) and is unchanged after all runs (`final/fc1_pyc_diff_vs_start.txt` is empty). Every pytest, script and probe run used `PYTHONDONTWRITEBYTECODE=1` and/or `python -B`. The r4 tests import no production script.
- **Participant identifiers.** None printed or written. A scan with no exclusions, for the literal BIDS subject prefix followed by a letter or digit, covers the two r4 tests, `verification/worker_M2_r4/` and this worker's metadata. It finds three files, all with synthetic placeholder names only (`SYN…`):
    - the byte copies of the shipped `test_token_job_driver.py` inside the two copied trees;
    - the superseded v1 of this addendum, kept for provenance (`superseded/…v1_af805513.md.txt`).
  - The bare prefix, with nothing after it, also occurs in code and logs that search for or redact it: the runners, the copies of the shipped guards and token-job script, and the fc2 failure log.
  - The runners redact the prefix in the raw logs at write time.
  - The class (a) real-data test runs the frozen script, which reads the pinned `ids` arrays in memory to check row order. Its output is keyed by position only.
  - Mutant-job outputs lived inside each job's copied tree and were deleted with it.
- **Compute.** 0 GPU-hours. Nothing was sent to B300 or connectome. Everything ran on local CPU under `nice`, with at most 2 pytest processes at a time.
- **Host memory pressure and conduct.**
  - 19 pytest attempts of this worker ended with rc −15 (SIGTERM): 17 in v1 and 2 in v2b; none in v3, v3ff or v3c. Each coincides with earlyoom SIGTERMs in `journalctl -u earlyoom`. All were classified INVALID and rerun, and none is counted as a kill.
  - This worker terminated, by PID, only its own processes: the 15 orphaned Pool processes listed in `logs/orphans_killed_0848.txt`, and its own stopped runs (`runs/*_STOPPED_README.txt`, including one corrected wording). No other process on the host was touched.
- **Development.** The first dev-tree run of the r4 drafts had 1 failure. It was in a fixture precondition of this worker's own test: dropping the dead channel changed L3 corrPR by 4.4e-4, below the 1e-3 margin. No shipped-code comparison had run yet. The fixture was changed so that the near-dead channel carries its own signal (effect about 3.2%). No tolerance of a shipped-vs-direct comparison was changed. A smoke run of the 32 named jobs on the dev tree with only the r4 files is labelled SMOKE and is not used as evidence. The r4 bytes were frozen at 2026-11-01T08:13:57Z, before every evidence run.
- **Git.** No git write of any kind. The checkpoint commits on this machine are not this worker's.
- **Layout.** The lint of the run metadata root (`audit_layout.py`) gives PASS with no findings: 269 files at fc1 (`logs/audit_layout_fc1.log`) and 270 at the end (`logs/audit_layout_final.log`).
- **Everything written by this iteration.** The two test files, this addendum, `results/topic3/2026-10-31/addendum_06_sha256.txt`, `verification/worker_M2_r4/` and `.agents/teamwork/tw-20261031-four-topics/worker_M2_r4/`.
