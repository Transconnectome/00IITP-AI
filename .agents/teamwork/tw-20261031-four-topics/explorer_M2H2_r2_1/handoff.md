# Handoff — explorer_M2H2_r2_1 (M2H2 iteration 2; lens: scientific design and falsifiability) — Hard handoff, 2026-11-01T17:55Z

**Summary.** The r1 gate failed on test coverage only. Every verifier reproduced the shipped H2 result independently, and nothing in the frozen design is wrong enough to change a label. Gate PASS stands, as do C1 INC, C2 INC, C3 TE+ and C4 TE+ and all 20 Family L labels.

The fix is additive and needs no GPU:
- new test files that guard the verdict wiring and every stats-script guard;
- a dated addendum_08 that records those tests, the mutation evidence, and errata to the pinned result report;
- a new receipt.

I ran a feasibility probe. Running `scripts/topic3h2_stats.py gate` and then `final` in a copied tree reproduces the shipped `gate_decision.json` and `h2_results.json` with 0 differing leaves at relative tolerance 0 (excluding `run` / `gate_decision_sha256`), in 3.5 s. Both negative paths I tried halt as designed. So a full-output regression plus negative-path tests can kill N53 and N50–N59.

One PI question remains: δ was chosen by the worker, not the PI. The C3 TE+ label, which carries the main R2 consequence, holds only for δ ≤ 0.548× the trained effect; the frozen value is 0.5×.

## 1. Observation

**O1. What failed.** Gate record in the dispatch: "FAIL (challenger_M2H2_r1_2 REFUTED)". Its two blocking issues, verbatim:
- (i) "Mutant N26 … and mutant N53 … both survive the 71-test suite and flip the primary label C1 from INC to EQ on the real data … no test runs cmd_final or cmd_gate";
- (ii) "Every guard in the stats script is untested; mutants N50–N59 all survive".

Evidence: `verification/challenger_M2H2_r1_2/mutants_ch2.out.json` gives `_meta` killed 27, survived 26. `survivor_impact.out.txt` reads "N53 … {'C1': 'EQ', …} {'L0_cov': 'EQ', 'L0_corr': 'EQ', … 'L2_cov': 'EQ', … 'LN0L2_cov': 'EQ' …}".

All 26 survivors: N11, N26, N27, N30, N31, N32, N33, N35, N38, N40, N41, N42, N50–N59, N71–N74.

Other verifiers' survivors, from their handoffs and harnesses:

| Verifier | Survivors |
|---|---|
| challenger_M2H2_r1_1 | W3 (= N53), W6 (= N50) |
| reviewer_M2H2_r1_1 | X04 (= N50); X09 (`h2stats.py` per-seed D1 `lo > 0` → `lo >= -1e9`); X14 (index-set seed +100 → +101, = N40); X15 (`e.max() < -delta` → `<= -delta + 1e-9`) |
| reviewer_M2H2_r1_2 | X06 (= N30), X10 (= N55), X11 (= N50), X13 (= N73), X14 (seed-set check in `final` disabled) |
| auditor_M2H2_r1_1 | A05 (= N40); A09 equivalent |

The challenger_r1_1 harness baseline was not clean: 1 failed, 70 passed. The failing test was `test_provenance_governance.py::test_pinned_2026_10_31_outputs_and_h2_receipt_verify`, because the copied tree lacked the receipt targets (`script_wiring_mutants_v2.log` line 1).

**O2. What is pinned.** `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries) pins:
- all of `src/topic3_h2/*.py` and its vendor files;
- `scripts/topic3h2_connectome.py` and `scripts/topic3h2_stats.py`;
- the 8 existing `tests/topic3_h2/*.py`;
- addendum 07;
- the H2 result report;
- every H2 output.

My check at about 17:40Z:
- C1: `LC_ALL=C sha256sum -c PROTECTED_HASHES.txt` gives rc 0.
- Receipts with rc 0: addendum_07, output_sha256 (H2), the 2026-10-31 output_sha256, and addenda 02–06.

So any edit to src, scripts, existing tests or the report breaks a receipt (C3, sci-pipeline G7: "평가 코드·테스트 해시 고정(에이전트 수정 시 FAIL)").

**O3. How the code is structured.**
- `scripts/topic3h2_stats.py` has `OUT = prov.OUT`. `provenance.py` has `ROOT = dirname×3(__file__)` and `OUT = ROOT/results/topic3/2026-11-02_h2`. So a copy of the tree writes only inside the copy.
- `verify_addendum07(addendum=ADDENDUM07, receipt=ADDENDUM07_RECEIPT)` takes its defaults when the function is defined. Monkeypatching `prov.ADDENDUM07` after import therefore has no effect; mutate the copied files instead.
- `cmd_final` contains these guards:
  - gate PASS;
  - seeds == `prov.SEEDS`;
  - `seed_hashes_distinct` / `rebuild_same_seed_identical`;
  - trained hash not among the seed hashes;
  - `check_deltas`;
  - T-A1 reproduces the pinned Family A to 1e-9.
- `cmd_gate` contains these guards:
  - a local G3 recheck;
  - `tf32_off` and `vendor_ok`;
  - the G1 window count.
- `pinned_T()` calls `reduce.card_index_sets` and `reduce.subset_prs` at call time. So the runtime T-A1 check makes `final` exit when N40 or N41 is present.

**O4. Feasibility probe.** Script: `verification/explorer_M2H2_r2_1/stats_regression_probe.py`; output: `stats_regression_probe.out.json`. It copies 9 paths (the stats script, `src/topic3_h2`, `src/topic3_spectral`, addendum 07, the H2 results dir and 4 pinned 2026-10-31 inputs) and runs the script there.

| Run | Result |
|---|---|
| `gate` | rc 0, PASS |
| `final` | rc 0, 3.5 s. Every non-`run`, non-`gate_decision_sha256` leaf equals the shipped file: 0 diffs at rel 0, 0 at rel 1e-9. Same for `gate_decision.json` |
| Negative path 1: `gate_verdict` set to FAIL | `final` rc 1 with "gate did not pass: H2 untestable…"; h2_results.json not rewritten |
| Negative path 2: in-process prelude `h2stats.FROZEN_DELTAS['C1'] += 1e-6` before `runpy.run_path(scripts/topic3h2_stats.py)` | rc 1 with "delta differs from addendum 07" |

**O5. δ sensitivity** (from the shipped `h2_results.json`; same as `verification/challenger_M2H2_r1_1/delta_sensitivity.out.txt`):

| Endpoint | point | CI95 | seed-effect range | frozen δ | TE+ holds for δ/\|trained\| | INC range |
|---|---|---|---|---|---|---|
| C1 H1a | 0.01245 | [0.01038, 0.01448] | 0.00358…0.02315 | 0.01138 (0.5×) | ≤ 0.157 | 0.158–1.017 |
| C2 H1b | 0.02953 | [0.02562, 0.03341] | 0.02046…0.04965 | 0.02234 | ≤ 0.458 | 0.459–1.111 |
| C3 D1 cov | 5.088 | [2.930, 7.247] | 4.927…5.285 | 2.672 | ≤ 0.548 | 0.549–1.199 |
| C4 D1 corr | 5.787 | [4.007, 7.567] | 5.537…5.937 | 3.019 | ≤ 0.663 | 0.664–1.199 |

- C3's binding constraint is lo95 (2.93); its seed effects are not binding (min 4.93). The fragility therefore comes from the precision of T's own index-set interval (SE 1.08), not from a drop present at init: the init drop is about 0.26 in every seed.
- C1's INC is the least δ-sensitive label of the four.
- Report §6 item 1 says the opposite: "A different δ would change C1 and C2 … The label for C1 sits on the δ boundary."

**O6. Seed heterogeneity of C1.** In `survivor_impact.out.txt`, using a single seed for Family C token gives:
- C1 = EQ for seeds 1, 5 and 8;
- TE+ for seeds 4, 7, 9 and 10;
- INC for seeds 2, 3 and 6.

So K = 1 would be unreliable. K = 10 with the per-seed condition is what makes C1 INC honest, and the N26/N53 class (collapse to one seed) is exactly the defect that would fabricate a confident label.

**O7. Report overreach.** The H2 result report is pinned, so it cannot be edited.

| Location | Claim | Issue |
|---|---|---|
| §5, R1 row | "the 'expansion' cannot be read as a training product" | Goes beyond addendum 07 §7 "Stays descriptive". The DiD is −1.61 [−3.77, +0.56] (cov) and −0.74 [−3.18, +1.71] (corr), with both intervals including 0 |
| §3 | "the L0 between-subject PR is set by the input and the patch embedding, not by training" | L0 subject-level cov and corr are INC: CI90 [−0.287, +0.165] and [−0.353, +0.092] reach ±log 1.10. Reads INC as EQ |
| §3 / §4 | full-n E1 2.78 / 11.02 / 3.58 and the α medians are called "trained" | They come from R0 (addendum 07 §2: R0 is "never substituted for T"); the numerical effect is ≤ 6.4e-7 |
| Header | "Every script that touches H2 data verifies this hash" | `driver.py` does not; only the launcher and the stats script do (auditor N4) |

**O8. An init artefact no one quantified.** challenger_r1_1's `seed_hash_check.out.json` shows `linear_w_absmax: 2.0` for 474,226,176 params (seeds 1, 3, 8, local torch 2.11). My synthetic probe `trunc_normal_outlier_probe.py` (no data) ran `torch.nn.init.trunc_normal_(std=0.02)` with the default absolute bounds a = −2, b = 2 over 474,226,176 draws:
- 33 values at exactly −2.0 (100 sd), 0 at +2.0, and no other value beyond 10 sd;
- the expected count if P(uniform draw = −1) = 2^−24 is 28.3.

Mechanism: torch's inverse-CDF sampler maps an exact −1 draw to −inf, which the clamp turns into −2. This is faithful to "the constructor's own init" that addendum 07 §3 froze. The trained net's own init is unknown anyway. Its effect on random-init PR is unmeasured: each outlier weight makes one output channel's pre-activation variance roughly 13× typical. This is an interpretive caveat, not a defect.

**O9. Compute so far.** The ledger has M2H2 rows for 218004, 218007, 218041, 218063, 218064 and 218065–218069. Total 0.819 GPU-h of the 6 GPU-h cap. The worker's closing rows for 218063 and 218064 (ledger lines 93 and 103) carry KST times in the UTC columns; the UTC values are 16:22:19Z–16:30:24Z and 16:32:19Z–16:51:39Z. The fix needs 0 GPU-h.

**O10. Integrity carry-forwards** (auditor N1, N7; reviewers N5/N6):
- The worker's connectome code dir was partly overwritten at 16:39:09Z by a stale upload (`driver.py` 197192b7, a truncated `pinned_trained_spectra.npz`). There was no effect on results, but it is undisclosed.
- connectome dirs remain to be deleted: the worker venv, explorer_r1_1/2, and reviewer_r1_1/2 (which includes a copy of the pinned spectra).
- connectome1 has hung `find /storage` processes from 2026-10-30. They are not from this run.
- An untracked `src/topic3_h2/__pycache__` (cpython-312) appeared at 17:08Z. It is not in any receipt.

## 2. Logic Chain

1. **The verdict stands.**
   - O1: every verifier reproduced the labels (four recomputations, 24/24 labels; five independent GPU reruns of seeds 1, 3, 4, 7, 8 matching bitwise or to 2.3e-15).
   - O4: the shipped script regenerates its own output exactly.
   - So the failure is "verdict path unguarded", not "verdict wrong". Per sci-pipeline G8, a software-guard failure is not a scientific null and does not change labels.
2. **The fix must be additive.**
   - O2: changing src, scripts or existing tests breaks receipts and G7.
   - Precedent: addenda 04–06 (M2) closed the same class with new test files plus a new receipt.
   - Hence: new test files, addendum_08, a new `addendum_08_sha256.txt`, and `output_sha256.txt` untouched.
3. **Which tests kill which mutants.**
   - O3 and O4: a copied-tree full-output regression of `gate` and `final` detects any mutant that changes a number or label: N53 (W3), N11, and N40/N41 (via the runtime T-A1 exit). The copied-tree run is bit-exact and takes 3.5 s.
   - Guard-removal mutants leave the output unchanged on clean inputs, so each needs a negative-path test that corrupts one input in the copy and expects a halt: N50–N52, N54–N59, X14 (rev2). O4 shows both negative paths work.
   - The Family C seed-collapse mutants (N26, N27) need a synthetic fixture with heterogeneous seeds and an independent oracle. O6 shows why: on real data seed choice alone moves C1 across all three labels.
4. **Two oracles are needed.**
   - A regression against the shipped JSON only pins current behaviour; it would enshrine a wrong output.
   - The independent recomputations (O1) validate the shipped output today, but the new tests should also carry their own oracle: hand-computed synthetic Family C/L values. This guards against the case where shipped output and code are wrong together.
5. **The design gaps are about reporting, not the rule.**
   - O5: C3's TE+ margin is narrow and comes from T's own interval width. δ was not PI-confirmed.
   - Changing δ now would be post-result. The frozen labels must stand. The sensitivity table must be published, and the PI should decide whether to accept the deviation.
   - O7: three report sentences read INC or "descriptive" cells as conclusions. They need errata in addendum_08, and the integrated R1 report must use the corrected wording.
   - O8: the init artefact belongs in the "what random init means" caveat.
6. **Driver GPU-path mutants are refuted by runtime evidence, not tests.**
   - N72: the independent reruns rebuilt seeds 1, 3, 4, 7, 8 and got the recorded hash for that seed.
   - N74: G1 passes on all 399 windows; an unloaded random model cannot pass it.
   - N71 and N73/X13 can be tested offline with monkeypatched fakes (`gate_checks` and `negative_controls` are plain functions; `driver.py` imports torch only inside `_run`). They are worth adding; N72/N74 stay nonblocking.

## 3. Caveats

- I did not prototype the driver-path offline tests (N71, N73) or the heterogeneous-seed Family C fixture. Their feasibility rests on reading `driver.py:132–204` and `h2stats.py:126–140`.
- I did not rerun any mutation harness. The kill predictions for N40/N41 follow from code reading (O3); they still need the actual rerun.
- The outlier count (O8) is from local torch 2.11 on a synthetic tensor, not from the job's torch 2.4 model. The two use the same algorithm, but the exact count per seed is unverified. Its effect on PR is not measured.
- I read the r1 verifier handoffs and harness files. I did not read any r2 peer explorer report; none existed at 17:36Z.
- My two copied probe trees remain at `verification/explorer_M2H2_r2_1/tree_20261101T174248Z` and `tree_20261101T174248Z_neg`. The permission system refused to delete them, and I did not work around it. They hold copies of repo files only: H2 aggregates, the pinned 2026-10-31 inputs including `E192_primary_token_spectra.npz` with its `pooled__*` arrays, and code. Nothing has left the machine. They contain .md/.txt copies that a host autocommit daemon could pick up. **Root: please delete both.**

## 4. Conclusion — recommended fix strategy (for worker_M2H2_r2)

**Scope, stated before work** (record it in progress.md with a timestamp):
- No GPU and no rerun.
- No edit to any file listed in `output_sha256.txt`, the 2026-10-31 receipts or C1.
- No re-freeze of addendum 07; no change of δ, K or labels.

**Closure criterion:** every named mutant listed below is killed by the extended suite in a copied-tree harness with a clean baseline. N42 needs either a kill or an equivalence proof. N72 and N74 are covered by runtime evidence. New mutants beyond this list are reported as nonblocking. That mirrors PI decision 6; root should confirm it with the PI if it wants to make it binding.

**Step 1. New test files** (names are suggestions; all new, none skip):
- (a) `tests/topic3_h2/test_stats_regression_r2.py`
  - Build a copy of the tree in `tmp_path`, using paths taken from `Path(__file__).resolve().parents[2]` and never the hard-coded repo path, so that mutation trees test themselves. Copy the 9 paths from O4.
  - First verify the shipped `h2_results.json` / `gate_decision.json` against their lines in `output_sha256.txt`.
  - Run `gate` and then `final` with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<copy>`.
  - Compare every leaf except `run` and `gate_decision_sha256`: strings, ints and labels exact; floats at rel ≤ 1e-9.
  - Kills: N53/W3, N11, N40/A05/X14 (rev1) and N41.
- (b) Negative-path tests in the same file. Each corrupts one input in a fresh copy and expects rc ≠ 0, the guard's message, and no rewritten output:

  | Corruption | Kills |
  |---|---|
  | `gate_verdict` FAIL | N50/W6/X04/X11 |
  | `seed_hashes_distinct` False, and separately `rebuild_same_seed_identical` False | N51 |
  | one seed key removed from `random_record.json` | X14 (rev2) |
  | a seed hash set to `trained_encoder_sha256` | N58 |
  | one byte appended to the copied addendum 07 (expect both `gate` and `final` to refuse) | N59 |
  | prelude `h2stats.FROZEN_DELTAS['C1'] += 1e-6` | N54 |
  | prelude monkeypatching `reduce.card_index_sets` to seed + 101 (expect "does not reproduce the pinned Family A") | N52 |
  | `gate`: one `cat_covpr__L2` cell of R0_scalars.npz × (1 + 1e-5) with the in-job G3 left ok (expect FAIL with G3 failed) | N55/X10 |
  | `gate`: `tf32_matmul_cudnn` [True, False], and separately `vendor_ok` False | N56 |
  | `gate`: G1 `n_windows` 398 | N57 |

- (c) `tests/topic3_h2/test_endpoints_r2.py`
  - K = 10 synthetic arms with deliberately different per-seed shifts, so that the seed mean ≠ seed 1, e.g. shifts spread across ±δ.
  - Assert, against a hand-written oracle (numpy mean / std arithmetic plus the frozen resampling calls), that for C1–C4: `point`, `random_mean`, each `seed_effects[s]` = mean_i(t_i − r_si) and `ci95` match.
  - Construct the case so that collapsing to seed 1 changes the label (INC → EQ), as on the real data.
  - Kills N26 and N27.
  - Also: the per-seed D1 `robust` flag equals `lo > 0` on one case with lo < 0 and one with lo > 0 (X09); `e.max() == −δ` exactly gives INC (X15).
- (d) `tests/topic3_h2/test_compare_r2.py`:

  | Test | Kills |
  |---|---|
  | `stats_match` fails on b = 1e-3, a = b(1 + 1e-5) (abs diff 1e-8) and passes on b = 1e4, a = b + 1e-3 (rel 1e-7) | N30/X06 |
  | parametrised over all 6 STAT_KEYS × 5 variants: a single-cell rel 1e-5 change fails, and dropped-count inequality fails | N31/N38 |
  | `contrast_status` with hi < 0 gives `ci_excludes_0` True | N32 |
  | `negative_control_fails_g1({'n_windows': 0, 'n_fail_cells': 1})` is False | N33 |
  | `REPOOL_TOL == STAT_REL_TOL*10 == 1e-5`, pinned against the addendum 07 §4 text | N35 |
  | monkeypatch `reduce.SCALAR_KEYS` to add `cat_cov_eigs`; `returnable_scalars` must raise. This makes N42 killable instead of "equivalent" | N42 |
- (e) `tests/topic3_h2/test_driver_gate_offline_r2.py`
  - `driver.gate_checks` with `io.load_X`, `io.ids_order_matches_names` and `prov.REMOTE_NPZ_ROOT` monkeypatched to synthetic tmp npz.
  - A packed R0 whose H1a contrast sign differs from the pinned one, with stats otherwise matching, must give G3 ok False (N73/X13).
  - Optionally `negative_controls` with fake dataset/loader/forward, where one control passes G1, must give G5 ok False (N71).

**Step 2. Mutation evidence.**
- Copy each r1 harness unchanged into `verification/worker_M2H2_r2/`: `mutants_ch2.py`, `script_wiring_mutants.py`, `rev_mutants.py`, `extra_mutants.py`, `aud_mutants.py`, plus the worker's own 32.
- Change only the tree-root path and the test lists, adding the new files to FAST/FULL. Use challenger_r1_2's COPY list so the baseline is green; a red baseline is invalid.
- Run at most 2 trees in parallel, detached, under timeout 900 per pytest.
- Report per-mutant status before and after. Shipped `h2_results.json` must be unchanged (output_sha256 rc 0).

**Step 3. `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_08_h2_r2.md`** (additive). Contents:
- §1 the r1 gate outcome;
- §2 the tests and the named-mutant table;
- §3 errata to the pinned report: the δ-sensitivity table from O5, replacing report §6.1; the R1 row reworded to "descriptive; DiD −1.61 [−3.77, +0.56] / −0.74 [−3.18, +1.71], no training reading either way"; L0 subject level INC = unresolved, not "set by input"; the R0-vs-T labels; the driver-hash claim;
- §4 disclosures: the remote overwrite at 16:39:09Z; the trunc_normal −2.0 clamp artefact (O8) as a meaning-of-init caveat; seed heterogeneity of C1 (O6) as why K = 10 matters;
- §5 the PI question on δ;
- §6 checks.

Receipt: `results/topic3/2026-11-02_h2/addendum_08_sha256.txt` covering addendum_08 and the new test files.

**Step 4. Ledger.** Append, under flock, two correction rows (never edit) for 218063 (16:22:19Z–16:30:24Z) and 218064 (16:32:19Z–16:51:39Z).

**Step 5. Checks:**
- tests/topic3_h2 (71 + new), tests/topic3_spectral 138, the old 86 (STRICT_E2E), tests/topic1_lagmotif 88;
- C1;
- every receipt;
- the "sub-" scan;
- layout lint on the run root.

**PI question for root** (only the PI can set δ): "H2 δ = 0.5 × |trained effect| (C1–C4) and log 1.10 (levels) were set by the worker and frozen before any random-init result. Accept as a recorded deviation, with the sensitivity table published? (Recommended.) Otherwise any other δ is reported as a post-hoc sensitivity, not a verdict." Also tell the PI that C3 TE+ (the 'learned' reading of the R2 subject-level drop) holds only for δ ≤ 0.548×.

**Integrated report (R1).** Cite C1 INC, C2 INC, C3/C4 TE+ "at the frozen δ = 0.5×, which the PI has or has not confirmed", and use the corrected wording from addendum_08 §3.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt            # rc 0
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt                                    # rc 0 (61)
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -I \
    verification/explorer_M2H2_r2_1/stats_regression_probe.py   # gate/final rc 0, 0 leaf diffs, both negative paths rc 1
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -I \
    verification/explorer_M2H2_r2_1/trunc_normal_outlier_probe.py   # ~30 values at exactly -2.0 per 474M draws
cat verification/challenger_M2H2_r1_2/survivor_impact.out.txt       # N26/N53 flip C1; single-seed labels vary EQ/INC/TE+
cat verification/challenger_M2H2_r1_1/delta_sensitivity.out.txt     # C3 TE+ only for delta <= 0.548x
grep -n "21806[34]" results/gpu_ledger_2026-10-31.md                 # closing rows carry KST
```

**Invalidation conditions:**
- the probe reports nonzero leaf diffs, which would mean the regression is not deterministic, so the tolerance or the copied set must change;
- any listed mutant survives the new suite in a clean-baseline tree;
- `output_sha256.txt` or C1 fails after the r2 work;
- a new test reads from `/home/juke/git/00IITP-AI` instead of its own tree root.
