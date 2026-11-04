# Topic 3 H2 — addendum 08 (iteration 2): test closure of the r1 gate, errata to the H2 result report, disclosures

Date 2026-11-02 (written 2026-11-01 UTC by worker_M2H2_r2, run tw-20261031-four-topics, workflow C). Dated addendum to
`docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md` (sha256 `09b45220…dd84b`, unchanged) and to
the H2 result report `docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md` (sha256 `bb1ef63e…b103`,
unchanged). Receipt: `results/topic3/2026-11-02_h2/r2/addendum_08_sha256.txt` (this file and the four new test files).

**Location.** This addendum sits in the owned results path `results/topic3/2026-11-02_h2/r2/` and not in
`docs/03_empirical_analysis/topic3/`, because the M2H2 ownership list names only addendum 07 and the result report in
that docs folder, and both are pinned. Root may copy it there byte-identically if wanted; its receipt hash then still
applies.

## 1. What this addendum changes and what it does not

- **Changed: nothing that existed.** No file listed in `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries:
  src/topic3_h2/**, scripts/topic3h2_*.py, the 8 shipped test files, addendum 07, the result report, every output) was
  edited, and no module was added under `src/topic3_h2/`. The 2026-10-31 receipts and C1 files are untouched.
- **Added:** four test files in `tests/topic3_h2/` (§3), this addendum and its receipt, two UTC correction rows in the
  GPU ledger (§7), and probes / mutation evidence under `verification/worker_M2H2_r2/`.
- **No rule, δ, K, label or number changes.** No GPU job, no connectome access, no rerun of any job. The frozen labels
  stand: gate G PASS; C1 INC, C2 INC, C3 TE+, C4 TE+; the 20 Family L labels as shipped.
- **The new tests were written after the H2 results existed.** They are regression guards for the shipped code, not
  a pre-registration (sci-pipeline G7: agents do not edit evaluation code or shipped tests; additions only).

## 2. Why: the r1 gate

Five r1 verifiers: reviewer_M2H2_r1_1 APPROVE, reviewer_M2H2_r1_2 APPROVE, challenger_M2H2_r1_1 CONFIRMED, auditor_M2H2_r1_1
CLEAN, challenger_M2H2_r1_2 **REFUTED** (gate FAIL). All five reproduced the shipped verdict independently (four
recomputations, 24/24 labels; five GPU reruns of seeds 1, 3, 4, 7, 8 bitwise or within 2.3e-15). The REFUTED verdict
was on test coverage only: the verdict-path wiring and every guard of `scripts/topic3h2_stats.py` had no test, so
plausible one-line mutants that flip the primary C1 label (N26, N53) survived the 71-test suite.

## 3. New tests (additive files; tests/topic3_h2: 71 → 167 tests, 0 skipped)

| File | sha256 | What it guards |
|---|---|---|
| `tests/topic3_h2/test_h2r2_stats_regression.py` | `3ac6331e721fa8d79f53035671fabb0a6cf55427a125681c4619e90de6845e8f` | Copies the unmodified `scripts/topic3h2_stats.py`, `src/topic3_h2`, `src/topic3_spectral`, addendum 07 and the shipped / pinned inputs from the tree under test (`Path(__file__).parents[2]`) into `tmp_path` and runs the script there as a subprocess. `gate` must reproduce the shipped `gate_decision.json`; `final` fed the byte-identical shipped gate decision must reproduce the shipped `h2_results.json`; `final` after the fresh `gate` must reproduce it too. Every leaf except the top-level `run` record is compared (labels, strings, ints, bools exactly; floats at rel ≤ 1e-12; code hashes are not compared, so kills are behavioural). A copied addendum 07 with one appended byte makes both commands refuse and write nothing. The output entries of `output_sha256.txt` must still verify. |
| `tests/topic3_h2/test_h2r2_stats_guards.py` | `cedb50eac5d9264911bc8500b849c96d53c423cedce9b6c81b2eecc914d18f22` | Loads the script with importlib, redirects its module global `OUT` to a staging copy of the shipped `gate/` and `random/` aggregates (asserted ≠ the shipped results dir, whose files are hash-checked after every test), and corrupts exactly one input per test. `final`: gate FAIL / missing verdict, seed 10 missing, seed 11 added, seed hashes not distinct, rebuild not identical, a seed hash equal to the trained hash, one seed's positions out of order, δ off the frozen values by 1e-9, card index sets with seed + 101: each must raise SystemExit with its own message and write no `h2_results.json`. `gate`: one R0 cell off by rel 1e-5 (3 keys), in-job G3 not ok, TF32 on (matmul or cudnn), vendor not ok, in-job G4 not ok, 398 windows, G1 not all-pass, G2 not ok, G5 not ok or missing: each must give FAIL naming exactly that check. Positive controls: the unmodified staging copy passes / writes. |
| `tests/topic3_h2/test_h2r2_family_oracle.py` | `221cb3c7b53ea735fdcb61693b047f030410497b645985b2ccfae6f09c5bbed6` | Families C and L and the per-seed D1 secondary on synthetic arms whose K = 10 seeds differ by construction, against a hand-written oracle (independent numpy; only the frozen card §3 resampling primitives are reused, with card literals). In C1 and C3 the full-K label is INC while seed 1 alone gives EQ, so an arm collapse is visible in labels, points, seed effects and intervals. Family L keys must come in the addendum 07 §5.3 order with test seed 20268131 + 10·k each. Per-seed D1 "robust" iff the 95% lower bound > 0. `decide`: a seed effect exactly at ±δ gives INC (strict inequalities). |
| `tests/topic3_h2/test_h2r2_gate_components.py` | `1f201b447e914c902a5565d33040786198596fa9aebfaa8362d8e29009ac5ac7` | `compare.stats_match` relative (not absolute) tolerance; every one of the 30 STAT_KEY × variant cells and the 5 dropped counts (key lists written from addendum 07 §4, not read from the module); CI wholly below 0 excludes 0; a control with 0 windows does not discriminate. `reduce.card_index_sets(57)` equals `subsample_indices(57, 28, 2000, 20261031 + 100)` and the `index_sets_sha256` recorded by both connectome jobs; `subset_prs` corr values are pr_corr (oracle) and differ from cov; the forbidden-key guard raises if SCALAR_KEYS ever named a forbidden key. Offline driver paths with fakes (no GPU, no checkpoint, no data): G2 re-pool tolerance 1e-5; G3 fails when R0 is within the statistics tolerance but on the other side of 0 for the H1a CI lower bound (a real-arithmetic construction); G5 needs every control to fail G1; a duplicate window before its subject is complete raises; `_run` with a fake model module records each random seed's own encoder hash and loads the checkpoint into the gate model. |

## 4. Mutation evidence (closure of the r1 gate class)

Harness: `verification/worker_M2H2_r2/union_mutants.py`, output `verification/worker_M2H2_r2/union_mutants.out.json`
(sha256 `2f38f617ccdad3371c27bf46fce001adefdd142cebc0f4f8805201bec53cbc6e`), log `verification/worker_M2H2_r2/logs/union_mutants.log`.
The mutant definitions are read verbatim from the six r1 harness files (worker_M2H2_r1 `mutants.py`, challenger_M2H2_r1_2
`mutants_ch2.py`, challenger_M2H2_r1_1 `script_wiring_mutants.py`, reviewer_M2H2_r1_1 `rev_mutants.py`, reviewer_M2H2_r1_2
`extra_mutants.py`, auditor_M2H2_r1_1 `aud_mutants.py`); only the tree root and the test lists changed. Copied trees use
challenger_M2H2_r1_2's COPY list. Baselines in both trees: shipped 8 files 71 passed, extended suite 167 passed.

- 125 definitions, 115 distinct edits, **115/115 killed by the extended suite**, 0 not applied, 0 invalid runs
  (no timeout, no rc ∉ {0, 1}), every mutated file restored byte-identically, shipped `h2_results.json` and
  `gate_decision.json` unchanged (sha256 checked before and after; 6265 s).
- **All 37 edits that survived in r1** (36 reported survivors, of which N40 = X14 (reviewer 1) = A05 and N50 = W6 = X11 are the same
  edit, plus W4 and W7, which challenger_M2H2_r1_1 defined but did not run) **survive the shipped 8-file suite run in FULL
  and are killed by the four new files alone**:

| r1 mutant (aliases) | What it breaks | First new test that fails |
|---|---|---|
| N26 | family C token arm = seed 1 for all K | `test_family_c_matches_the_oracle_for_every_endpoint[C1]` |
| N27 | family C subject arm = seed 1 for all K | `…_for_every_endpoint[C3]` |
| N11 | Family L key order | `test_family_l_keys_in_card_order_and_each_key_has_its_own_test_seed` |
| X09 | per-seed D1 robust always true | `test_secondary_per_seed_d1_robust_flag_is_the_lower_bound_rule` |
| X15 | TE− seed boundary `<= −δ + 1e-9` | `test_te_minus_needs_every_seed_effect_strictly_below_minus_delta` |
| N30, X06 | G3 absolute instead of relative tolerance | `test_stats_match_tolerance_is_relative_not_absolute` |
| N31, N38 | G3 skips sub_corrpr / LN0L2 | `test_stats_match_checks_every_key_variant_cell[…]` |
| N32 | one-sided CI-excludes-0 | `test_contrast_status_ci_wholly_below_zero_excludes_zero` |
| N33 | control with 0 windows discriminates | `test_negative_control_with_no_windows_does_not_discriminate` |
| N35 | G2 tolerance 1e-2 | `test_gate_checks_g2_repool_tolerance[100.0-False]` |
| N73, X13 | G3 ignores contrast status | `test_gate_checks_g3_requires_equal_h1a_h1b_contrast_status` |
| N71 | G5 any instead of all | `test_one_control_that_does_not_fail_g1_fails_g5[…]` |
| N72 | random arm hash of the wrong seed | `test_random_arm_records_each_seeds_own_encoder_hash` |
| N74 | gate arm without checkpoint load | `test_gate_arm_loads_the_checkpoint_into_the_model_it_runs` |
| A09 | duplicate-window check removed | `test_duplicate_window_before_its_subject_is_complete_raises` |
| N40 = X14 (rev. 1) = A05 | card index-set seed + 101 | `test_card_index_sets_are_the_job_recorded_ones` |
| N41 | corr subsets computed as cov | `test_subset_prs_use_pr_cov_and_pr_corr_per_index_set` |
| N42 | forbidden-key check off | `test_returnable_scalars_guard_raises_if_a_forbidden_key_is_ever_listed` |
| N50 = W6 = X11, X04 | `final` ignores a gate FAIL | `test_final_refuses_on_one_corrupted_input[gate_verdict_FAIL]` |
| N51 | seed hygiene ignored | `…[rebuild_not_identical]` |
| X14 (rev. 2) | seed-set check off | `…[seed_10_missing]` |
| N52 | T-A1 reproduction check off | `…[index_sets_seed_plus_101]` |
| N53, W3 | every arm reads R1 scalars | `…[seed_positions_incomplete]` (also the full-output regression) |
| N54 | check_deltas removed | `…[deltas_off_frozen]` |
| N58 | trained hash allowed among seeds | `…[seed_hash_equals_trained]` |
| N55, X10, W7 | gate drops the local G3 recheck | `test_gate_fails_with_the_check_the_corrupted_record_belongs_to[R0_…]` |
| N56 | gate ignores TF32 / vendor | `…[cudnn_tf32_on]` |
| N57 | gate ignores the window count | `…[G1_398_windows]` |
| N59 | `final` skips the addendum receipt | `test_final_command_reproduces_every_shipped_h2_result_value` (leaf `addendum07_sha256`) and the modified-addendum test |
| W4 | T arm replaced by R0 | `test_final_command_reproduces_every_shipped_h2_result_value` |

- **N42** is equivalent with respect to the shipped constants (returnable_scalars only ever builds `positions` plus
  SCALAR_KEYS × VARIANTS, none of which is forbidden, so the guard's list is always empty). The guard is a defence
  against a future SCALAR_KEYS edit; the new test exercises it by patching SCALAR_KEYS and so kills the mutant.
- **N72 and N74** are killed offline (fake model module in `_run`); they were also refuted at runtime in r1 by the
  verifier reruns of seeds 1, 3, 4, 7 and 8 (recorded hashes reproduced) and by G1 passing on all 399 windows.
- The other 78 edits (killed in r1) stay killed; 53 of them are also killed by the new files alone.
- New mutants beyond these classes were not searched for by this worker; if a later verifier finds one, it is new
  evidence, not a reopening of these classes.

## 5. Errata to the H2 result report (the report itself is pinned and not edited)

E1. **§6 item 1, δ boundary.** The sentence "The label for C1 sits on the δ boundary" is wrong, and the statement that a
different δ "would change C1 and C2" is incomplete. Descriptive δ sensitivity (shipped intervals, Holm p values and
seed effects, shipped `decide()`, δ = f × |pinned trained effect|, frozen f = 0.5; `verification/worker_M2H2_r2/delta_sensitivity.py`):

| Endpoint | Frozen label | TE+ for f below | INC for f in | EQ from f |
|---|---|---|---|---|
| C1 (H1a DiD) | INC | 0.1575 | [0.1575, 1.0175) | 1.0175 |
| C2 (H1b DiD) | INC | 0.458 | [0.458, 1.1115) | 1.1115 |
| C3 (D1 cov DiD) | TE+ | 0.5483 | [0.5483, 1.2912) | 1.2912 |
| C4 (D1 corr DiD) | TE+ | 0.6636 | [0.6636, 1.2057) | 1.2057 |

C1's INC is the most robust label. The label closest to the frozen δ is **C3**: its TE+ (the "learned" reading of the R2
subject-level drop) holds only for f ≤ 0.548, a margin of about 10%. C3's margin is set by the width of the trained arm's
own index-set interval (lo95 2.93 against a trained effect 5.34); the init drop is small in every seed (0.26 on average, 0.06–0.42 across the 10 seeds). C4 holds
for f ≤ 0.664; C2 would be TE+ for f ≤ 0.458. These are descriptive; the labels stay at the frozen δ (§8).

E2. **§5, R1 row.** Replace "Descriptively, the untrained network shows an equal or larger subject-level L1 → L2 rise,
so the 'expansion' cannot be read as a training product" by: *Stays descriptive. Trained minus init L2 − L1 at subject
level is −1.61 [−3.77, +0.56] (cov) and −0.74 [−3.18, +1.71] (corr); both intervals include 0, so H2 supports no
training reading of the L1 → L2 rise either way.* (addendum 07 §7: R1 "stays descriptive".)

E3. **§3, L0 reading.** "The L0 between-subject PR is set by the input and the patch embedding, not by training" treats an
INC cell as equivalence. L0 subject level is INC for both estimators (cov −0.061, 95% [−0.330, +0.208], 90%
[−0.287, +0.165]; corr −0.131, 95% [−0.396, +0.135], 90% [−0.353, +0.092]; both reach ±log 1.10). Correct reading: *at
L0 the H2 comparison is unresolved.*

E4. **§3 and §4, values labelled "trained".** The full-n subject-level covPR values "2.78, 11.02 and 3.58" (§3) and the
"Trained" token α medians (§4) were taken from the R0 arm (the trained checkpoint re-extracted on connectome), not from
the pinned T arm. Addendum 07 §2 never substitutes R0 for T. For E1 the pinned T values (Family A `E1_full`, L1 2.7782,
L2 11.0202, L3 3.5786) equal the R0 values to the printed precision (G3: R0 vs T per-subject statistics within 7.3e-8;
index-set PRs within 6.4e-7). Read both as "R0 (re-extracted trained)". No label uses them.

E5. **Header, hash claim.** "Every script that touches H2 data verifies this hash" is too broad. The launcher
(`scripts/topic3h2_connectome.py submit`) and the stats script (`scripts/topic3h2_stats.py gate|final`) verify the
addendum 07 hash; the connectome job driver `src/topic3_h2/driver.py` does not (auditor_M2H2_r1_1 N4). The jobs were
launched only through the launcher.

E6. **§5, R2 row.** "It is not an architecture or input artefact" holds relative to the extraction constructor's
default initialization only (report §6 item 2; §6 D2 below), not to every possible untrained network.

E7. **§7, reproduction.** The two stats commands, run as printed (`cd` into the production tree), rewrite the shipped
`gate_decision.json` and `h2_results.json` and break `output_sha256.txt`. Run them only in a copied tree, as
`test_h2r2_stats_regression.py` does.

E8. **§6 item 5, seed variance.** Token-level CIs are subject-sampling intervals and exclude seed variance; seeds enter
only through the per-seed condition. Descriptively, C1 computed against one seed at a time (K = 1, frozen δ;
`verification/worker_M2H2_r2/single_seed_labels.py`) is EQ for seeds 1, 5, 8, TE+ for seeds 4, 7, 9, 10 and INC for
seeds 2, 3, 6 (C2: TE+ for 4, 5, 7, 9, 10, INC otherwise; C3 and C4 TE+ for every seed). The H1a / H1b reading is
therefore seed-sensitive, and K = 10 with the every-seed condition is what keeps C1 / C2 at INC.

None of E1–E8 changes a rule, a label or a shipped number.

## 6. Disclosures

D1. **Remote code dir overwritten during job 218064 (auditor_M2H2_r1_1 N1).** At 2026-11-01T16:39:09Z, while the
random-arm job ran, `/home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/code` on connectome was partly overwritten by
a stale tree (driver.py replaced by an older version, sha256 `197192b7…`; `pinned_trained_spectra.npz` replaced by a
truncated non-zip file); most likely the stalled early upload that the r1 worker logged. No effect on results: the job
had hashed its code and pinned inputs at 16:32:21Z (equal to the repo code), the worker pool was forked before, the
random arm never re-reads the npz, and the auditor's seed-3 rerun reproduced the shipped seed-3 aggregates bitwise. The
remote dir no longer matches `logs/ship_manifest_sha256.txt`. Iteration 2 used no connectome access; the dir was neither
re-shipped nor deleted. It must not be reused without a re-ship; deletion is left to root after the victory audit.

D2. **What "random init" contains.** The constructor's own init is `trunc_normal_(std = 0.02)` with torch's default
ABSOLUTE bounds a = −2, b = 2 (±100 sd). torch's inverse-CDF sampler clamps a few draws to the bound: a synthetic local
probe (torch 2.11, `verification/worker_M2H2_r2/trunc_normal_clamp_probe.py`) gives 23 of 4·10⁸ draws exactly at −2.0
(none at +2.0; every other draw |w| ≤ 0.106), i.e. about 27 per 474 M weights; challenger_M2H2_r1_1 observed max |w| =
2.0 in the built network. This is faithful to the frozen "constructor's own init" (addendum 07 §3), but such outlier
weights are part of what H2's random arm is. Their effect on PR was not measured.

D3. **C1 seed heterogeneity** (E8): the reason K = 10 and the every-seed condition matter.

D4. **GPU ledger.** The completed rows of jobs 218063 and 218064 give sacct local KST times in the UTC columns. Two
correction rows were appended under flock (existing rows not edited): 218063 2026-11-01T16:22:19Z–16:30:24Z, 218064
2026-11-01T16:32:19Z–16:51:39Z (0 GPU-h each; the GPU-h stay counted once). Iteration 2 used 0 GPU-h; M2H2 total
remains 0.819 of its 6 GPU-h cap (worker 0.458, explorers 0.058, verifiers 0.303).

D5. **Left for root:** the connectome dirs under `/home/connectome/connectome1/iitp4_m2h2/` (worker_M2H2_r1 venv, code,
logs, returned aggregates; explorer and verifier dirs) and the verification trees listed by the r2 explorers.

## 7. Scope of the r2 gate (proposed, for root / the PI)

Closure criterion used here: every r1 survivor class above is killed by the extended suite in a copied tree whose
baseline is green; N42 is killed (and is equivalent w.r.t. the shipped constants); N72 / N74 are killed offline and
refuted at runtime. Mutants beyond these classes would be reported as nonblocking, as in PI decision 6. This is a
proposal; it binds only if root / the PI confirm it.

## 8. PI question (via root)

"δ = 0.5 × |trained effect| for C1–C4 and log 1.10 for levels was set by the worker and frozen before any random-init
result (addendum 07). sci-pipeline treats δ as a PI choice. Do you accept it as a recorded deviation, with the
sensitivity table in §5 E1 published (recommended)? Any other δ would be reported as a post-hoc sensitivity, not a
verdict. Note that C3 TE+ holds only for δ ≤ 0.548 × |trained effect|." No δ was re-chosen here, and no label moves.

## 9. Checks (2026-11-01, local DGX-Spark, CPU only)

- `tests/topic3_h2`: 167 passed, 0 skipped (71 shipped + 96 new); `tests/topic3_spectral` 138 passed;
  old suite (STRICT_E2E=1, `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`) 86 passed;
  `tests/topic1_lagmotif` 88 passed.
- C1 protected hashes rc 0; `results/topic3/2026-11-02_h2/output_sha256.txt` (61) rc 0; `addendum_07_sha256.txt` rc 0;
  the 2026-10-31 receipts as before this run (card_sha256.txt fails `sha256sum -c` only on its known trailing token;
  code_sha256_at_freeze.txt only on the launcher difference disclosed in addendum 01).
- No BIDS prefix bytes in this file or in any file under `results/topic3/2026-11-02_h2/`; no participant identifier
  printed or written; no git writes; no installs.
