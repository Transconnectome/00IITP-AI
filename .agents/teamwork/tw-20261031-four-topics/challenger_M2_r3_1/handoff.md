# handoff — challenger_M2_r3_1 (M2 Topic 3, iteration-3 gate) — Hard handoff

Verdict: **REFUTED**. Two new survivor classes are reachable through the card's own procedure, and the shipped 121-test suite does not see them:
- **Token-job producer.** Of the four primary inputs, `cat_corrpr__L3` and `cat_covpr__L2` are not checked. Mutant T02 turns H1b from "not replicated" into "holds". Mutant T01 reverses the direction of H1a.
- **Family A reported numbers.** No real-data regression covers them. Several mutants change numbers that the result report prints.

The real verdicts are not affected: the pinned spectra and JSON were produced by the frozen code. Neither class is one of the five r2b blocking classes. Those five are closed (§1 O10, O12). The fixes are cheap, additive tests (§4).

All evidence is under `/home/juke/git/00IITP-AI/verification/challenger_M2_r3_1/`. Paths below are relative to it unless absolute.

## 1. Observation

**O1. Copied tree and control.**
- `bin/make_tree.sh` built `tree_base/`: 121 files, and the manifest `tree_base.manifest_sha256.txt` equals production.
- Control run: `tests/topic3_spectral` gave 121 passed in 64.6 s, rc 0, with no `__pycache__` (`logs/control_start.{log,xml}`).

**O2. My own mutants.** There are 14, in `mutants/specs.py`.
- None is among the worker's 151 union patches (`probes/union_patch_list.txt`), and each old string occurs exactly once.
- Runner: `bin/run_mutants.py`. Each job gets a fresh copy, a compile check, the full suite under `timeout -k 15 900` in its own session, and at most 2 at a time.
- A job counts as KILLED only when rc is 1 and the JUnit file has a `<failure>`.
- Results are in `logs/RUN1_own.json` and the per-job `jobs/<id>/{patch.diff,junit.xml,pytest.log}`. All 14 ran 121 tests; 0 were INVALID.

| id | target | full 121 suite |
|---|---|---|
| CR3_T01 | token_job.py: `cat_corrpr` of L3 computed from the covariance eigenvalues | **SURVIVED** |
| CR3_T02 | token_job.py: `cat_covpr` of L2 computed from the correlation eigenvalues | **SURVIVED** |
| CR3_A01 | analysis.py A2: calibration iid reference at (25, D), not (12, D) (card §4 A2) | **SURVIVED** |
| CR3_A02 | analysis.py: SWIFT_PAIRS gives L1−L2 instead of L2−L1 (card §4 A1) | **SURVIVED** |
| CR3_A03 | E1: covPR/n instead of covPR/(n−1) | SURVIVED |
| CR3_A04 | E1: iid q97.5 computed as q95 | SURVIVED |
| CR3_A05 | E1: column-permutation null q2.5 computed as q5 | **SURVIVED** |
| CR3_A06 | E1: covPR/iid uses the median instead of the mean | SURVIVED |
| CR3_A07 | E1: jackknife SE of corrPR instead of covPR | **SURVIVED** |
| CR3_A08 | A2: calibration mean uses corrPR instead of covPR | **SURVIVED** |
| CR3_A09 | A1 index-set seed offset +1 (Monte Carlo only) | SURVIVED |
| CR3_V01 | zoo agreement reads the primary's Holm p | KILLED (10 failures) |
| CR3_V02 | bootstrap CI of the median | KILLED (8) |
| CR3_V03 | sign-flip on the median | KILLED (6) |

**O3. T01/T02 consequences on the real data (exact counterfactual).**
- Method: `bin/famB_counterfactual.py` transforms the pinned npz of all 4 checkpoints inside a fresh copy. T01 sets `cat_corrpr__L3 := cat_covpr__L3` and `cat_corr_eigs__L3 := cat_cov_eigs__L3`. T02 sets `cat_covpr__L2 := cat_corrpr__L2`. It updates the job-json hashes in the same way as the r3 `_rewrite_npz`, then runs the unmodified `scripts/topic3_token_stats.py` in the copy (`logs/famB_counterfactual.json`).
- Control (NONE): the primary blocks equal the pinned file, and the verdicts equal the pinned verdicts.
- The mapping is exact. On synthetic frames, the mutated `token_job` gives transform(shipped) for all 51 packed arrays, and changes only the named arrays (`bin/check_counterfactual_mapping.py`, `logs/counterfactual_mapping_check.log`).
- **T02**: H1b goes from **"not replicated"** (L3 higher, 1 of 3) to **"holds"** (L3 lower, 3 of 3). The primary H1b mean goes from +0.0447 [0.0408, 0.0485] to −0.0383 [−0.0412, −0.0355], and every zoo mean becomes negative.
- **T01**: H1a stays "holds", but the **direction reverses**: L3 higher with 2 of 3 agreeing becomes L3 lower with 3 of 3. Means change as follows:
  - primary +0.0228 → −0.0567;
  - HCP −0.137 → −0.249;
  - L1e-4 +0.038 → −0.185;
  - L5e-5 +0.049 → −0.074.

  Report §3 ("2–5% increase") and the token-level part of the R2 verdict ("A token-level collapse FAILS … opposite sign") would invert.

**O4. Reachability and provenance.**
- `src/topic3_spectral/token_job.py` is the card §9 step-2 producer. Its `subject_summary` is the only source of `cat_corrpr__L3` and `cat_covpr__L2`.
- `scripts/topic3_token_stats.py::load_checkpoint` (lines 71–82) checks only "halted", "outputs", the spectra sha256 and the positions. The job's recorded `code_sha256` is never compared with `code_sha256_at_freeze.txt`.
- What the shipped tests check:
  - `test_token_job.py::test_subject_summary_matches_direct_computation_and_pooling_rule` checks only `pooled` L3/L0, `cat_corrpr` LN0L2 and `cat_covpr` L3.
  - `test_planted_stage3_compression…` is an inequality.
  - `test_token_job_driver.py` checks shapes.
  - The r3 Family B wiring tests start from the pinned npz.
- The pinned job jsons record code hashes equal to `code_sha256_at_freeze.txt` for all 7 files. Current src equals freeze; only `scripts/topic3_launch_connectome.py` differs, as disclosed in addendum 01 #2. So the pinned spectra came from the frozen code.

**O5. Family A on the real data.**
- `bin/famA_rerun.py` runs `scripts/topic3_subject_level.py` in a fresh copy, writing to the copy's own OUT. Each run takes about 27 s and reads the VRABES inputs read-only.
- Unmutated: 300 of 300 leaves equal the pinned `family_A_subject_level.json` at rel 1e-9 (`logs/famA_control.json`).
- Mutants (`logs/famA_mutants.json`). Every run kept D1 and D3 the same.

| Mutant | What changes | Leaves |
|---|---|---|
| A01 | The A2 calibration column printed in report §2 (BrainLM / BrainJEPA / NeuroSTORM) goes from 0.406 / 0.598 / 0.734 to 0.189 / 0.279 / 0.351 | 7 |
| A02 | The R1 basis "ΔPR₂₈(L2 − L1) = +4.67 [+2.96, +6.39]" (report §4) is replaced by L1−L2 | 14 keys |
| A05 | The report §2 "column-permutation null q2.5" column, e.g. L0 goes from 44.77 to 44.87 | 14 |
| A07 | The report §2 jackknife SE column: L1 goes from 3.577 to 4.609 (the 3.58 is cited in R1), and L0 from 0.276 to 0.725 | 28 |
| A08 | The calibration column: 0.406 / 0.598 / 0.734 → 0.540 / 0.700 / 0.812 | 14 |
| A03, A04 | JSON-only card E1 quantities | 14 each |
| A06 | Changes fall below the printed precision | 14 |
| A09 | Monte Carlo seed only | 27 |

- Addendum_05 §6 discloses: "Family A numbers other than the A2 row identity are not re-derived by the r3 tests".

**O6. Independent Family B recompute.**
- `bin/recompute_famB.py`, run with `-I` and without importing src, gives `recompute/famB_independent.json`.
- With the code's seed schedule it matches the pinned per-checkpoint mean, CI, raw p and Holm p with max |Δ| = 0 for all 8 primary cells.
- With independent seeds and B = 99999 the verdicts are the same: H1a holds (L3 higher, 2 of 3) and H1b not replicated (1 of 3).
- The report §3 table matches.

**O7. Addendum 05 §5 corrections, each verified.**
- H1b: HCP −10.68% and L1e-4 −3.24%. H1a: HCP −12.78%, primary +2.30%, L1e-4 +3.85%, L5e-5 +5.01%.
- H4 L0 ceiling: 159, with an observed maximum of 3.18. `cat_cov_eigs__L0` has 384 columns.
- Primary CI half-widths are 0.0020–0.0144 overall: H1a 0.0020–0.0096 and H1b 0.0039–0.0144.
- The addendum_03 Write is at 12:17:16.770Z (`verification/auditor_M2_r2b_1/probes/p01_worker_r2_transcript_timeline.log:35`). Git first commit is 4ce1917 at 2026-10-31T12:31:25Z, with blob sha256 725d50771c83…. Commit 0db0336 carries the same blob unchanged, so addendum_04 §1's attribution is corrected correctly.
- The r3 fixture gives raw p 0.0326, Holm p 0.0652 and CI [0.0007, 0.0103]; the skewed fixture gives Holm p 0.0321 / 0.0308 and CI lower bounds −0.00144 / −0.00142.
- Addenda 03 and 04 are otherwise accurate as corrected.

**O8. The card was frozen before the results.**
- The card bytes, sha 683374565d80…, are already in root checkpoint commit 24fe976 at 2026-10-31T08:46:25Z (blob cea00a77 equals the working file).
- `card_sha256.txt` records the freeze at 08:48:29Z.
- Family A `started_utc` is 08:49:18Z, the token-job outputs are 08:53–08:58Z, and Family B is 09:01:59Z. All run records carry `card_sha256_verified` = 683374….

**O9. The verdicts follow the card's rules (from the pinned JSON).**
- D1: the cov lo is 3.22 and the corr lo is 4.28, both above 0, giving "drop robust and not a per-channel-scale effect".
- D3: the lo values are 0.77 and 1.72, both above 0, giving true.
- D2: p_low = 0.001 < 0.025 for all 7 matrices.
- H1a: holds, 2 of 3. H1b: not replicated, 1 of 3, with every zoo checkpoint Holm-significant.

**O10. The five r2b blocking classes.** I independently reproduced 5 of the worker's union kills and survivors (`logs/RUN2_union_repro.json`): U057 (V01), U072 (ci95 [hi, lo]), U091 (X02), U118 (V26) and U127. See §1 O12 for the outcome. U127: a mean of exactly 0 gives a sign-flip p of 1.0 (probe), so the verdict is "killed" either way, and I accept it as equivalent.

**O11. C1 and receipts.** C1 gives rc 0 with 67 OK (`logs/c1_check.log`). The receipts output / 02 / 03 / 04 / 05 give 42 / 1 / 3 / 2 / 3 OK, all rc 0.

**O12. Union reproduction outcome** (`logs/RUN2_union_repro.json`, 121 tests per job, 0 INVALID). All five match the worker's FULL_v2 classification and its killing tests:
- U057 KILLED: `test_primary_raw_p_below_alpha…` and `test_primary_holm_rule_end_to_end…`, both for H1a and H1b.
- U072 KILLED: 6 failures, including `test_paired_log_contrast_ci_and_p…` and `test_token_stats_script_reproduces_pinned_family_b…`.
- U091 KILLED: `test_token_stats_script_uses_the_card_primary_when_every_choice…`.
- U118 KILLED: both wiring tests.
- U127 SURVIVED. It is equivalent (O10).

**O13. Hygiene at the end.**
- The `tree_base` manifest is intact.
- The `.pyc` listing of src, scripts and tests is identical to my start baseline (`logs/pyc_diff.txt` is empty).
- No job trees are left and no process of mine is running.
- C1 at the end gives rc 0 with 67 OK, and all five receipts verify.
- The whole-run `audit_layout.py` gives rc 0 with findings [] (`logs/audit_layout.log`).
- The BIDS-prefix scan of my verification and metadata folders finds only the literal prefix in the shipped code and the synthetic `sub-SYN*` names in the copied shipped test.
- 0 GPU. No git writes.

## 2. Logic chain

1. The dispatch criterion has two parts: the survivor must be reachable on inputs the card's procedure can produce, and it must be able to change a verdict or a reported number.
2. T02 survives all 121 tests (O2). The card §9 step 2 runs `token_job.subject_summary` on the real frames. The stats script accepts any spectra whose sha256 matches its own job json, so a rerun with the T02 defect would be accepted (O4). The exact counterfactual turns the H1b verdict from "not replicated" into "holds" (O3). Both parts of the criterion are met: REFUTED.
3. T01 is the same case. It reverses the H1a direction and every primary mean (O3), so it changes both reported numbers and the direction stated in the verdict.
4. A01, A02, A05, A07 and A08 survive all 121 tests (O2). They run on the real pinned inputs in the card's own Family A script (26 s), and they change numbers that the result report prints (O5). That is the same class the r2b gate treated as blocking for A01: the reported A2 numbers changed while D3 stayed true and the suite stayed green. The worker closed only the row-identity variant, and addendum 05 §6 discloses the remaining gap.
5. Weaker cases:
   - A03, A04 and A06 change only JSON fields, or values below the printed precision.
   - A09 is a Monte Carlo seed offset that the card does not pin.

   I do not use any of these to refute.
6. The r2b classes themselves are closed. My kills of the reproduced union mutants agree with the worker's FULL_v2 (O10/O12), and the independent recompute (O6) and the corrections (O7) hold. The defect is not in what iteration 3 added. It is in two producer and descriptive layers that no test re-derives.

## 3. Caveats

- T01 and T02 are hypothetical code defects. No real result was produced with them (O4). Their real-data effect is an exact counterfactual built from the pinned npz (O3), validated on synthetic frames. It was not a connectome rerun.
- All my tests ran in copied trees under host load. The load average rose to about 47 from other workflows. Each job ran all 121 tests, and none timed out.
- I wrote 14 mutants and reproduced 5 union jobs. I did not rerun the full 151-patch union.
- DISPATCH.md summarises, in brackets, the worker's embedded JSON beyond its OBSERVATION section, instead of copying it verbatim. The full text is in `/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2_r3/handoff.md` and in the harness task. This is a deviation.
- Nonblocking card gap: when Holm p ≥ 0.05 and the CI excludes 0, the shipped code labels the result "killed (primary CI includes 0)". That label is factually wrong for this case, and card §5 defines no outcome for it. Addendum 05 §5 records it, and it is unreachable on the real data (Holm p = 0.0002).
- `src/topic3_spectral/__pycache__` (3 files from iteration 2, 2026-11-01 09:39 KST) is still in production. I did not touch it.

## 4. Conclusion

**REFUTED** for iteration 3 as a whole.
- The five r2b blocking classes are closed, and the addenda 03–05 numbers are accurate.
- Two new classes survive the full suite and meet the dispatch criterion:
  - **(i) Token-job producer.** Of the four primary inputs, `cat_corrpr__L3` and `cat_covpr__L2` are unchecked. T02 flips H1b to "holds", and T01 reverses H1a.
  - **(ii) Family A reported numbers.** They have no real-data regression: A01, A02, A05, A07 and A08 move printed numbers.
- No real verdict changes. The fixes are additive tests only, with no src/scripts change and no rerun:
  1. **Family A.** Copy `scripts/topic3_subject_level.py`, `src/topic3_spectral`, the card and its hash into `tmp_path`, run the script there, and compare all 300 result leaves with the pinned `family_A_subject_level.json`. This mirrors `test_token_stats_script_reproduces_pinned_family_b…` and costs about 27 s. It kills A01–A08, and A09 too.
  2. **Token job.** Extend the `subject_summary` direct-computation test to all four primary inputs and the secondary inputs: `cat_corrpr` L3 / L2 / LN0L2 and `cat_covpr` L2 / L3 / LN0L2, plus the stored eigenvalue arrays, each against `pr_from_eigs(corr_eigs / centered_eigs(concatenated tokens))`. This kills T01 and T02.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI/verification/challenger_M2_r3_1
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B bin/run_mutants.py logs/RERUN.json --only CR3_T01_cat_corrpr_L3_from_cov_eigs,CR3_T02_cat_covpr_L2_from_corr_eigs,CR3_A01_a2_calib_iid_at_n25,CR3_A07_e1_jackknife_on_corrpr
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B bin/famB_counterfactual.py logs/FB.json NONE T01 T02
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B bin/famA_rerun.py logs/FA.json NONE CR3_A01_a2_calib_iid_at_n25 CR3_A07_e1_jackknife_on_corrpr
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B bin/check_counterfactual_mapping.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B -I bin/recompute_famB.py recompute/X.json
```

The finding is invalidated if any of the following holds:
- a shipped or r3 test fails on T01 or T02 in a fresh copy;
- the counterfactual control (NONE) differs from the pinned file;
- the unmutated Family A rerun does not reproduce the pinned 300 leaves.

## 6. Measured artifact hashes (sha256 of the production files, 2026-11-01T06:57Z; all equal the worker's claims)
- `58c64ccbc66e825b5e66e4322894e61d02ea5bddad8c3029c3be480dd0acd80b` tests/topic3_spectral/test_verdict_rules_r3.py
- `b091b0b861dc212d2972ed5a9bb64cfe42d41361e1bd6bde05f9476681ac6a1c` tests/topic3_spectral/test_token_stats_wiring_r3.py
- `a4001f09ff7d8ccb401e5015ade37e887fbad5e3f17a15019a9c3d8695163bd1` docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_05.md
- `1e542da7705d78000961faca75c11f8236473442e9fecaf9e181056c8e2905d6` results/topic3/2026-10-31/addendum_05_sha256.txt
- `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0` the card
- `f285b0afe46b5bd36c9055e5457a6ec656d5d02a2609d5c9795cf47948ee9949` family_A_subject_level.json
- `ab00ea33557c5e251d70359a6c483720c839a003fe836eae274cf31afd9b8a68` family_B_token_level.json
- `a0fc8022953275fb5e02c6f7c4f777641fd9fb9d3a23877a6256797d4687ebf8` src/topic3_spectral/token_job.py (= freeze)
- `c46608872f24a64316331c8dfb9397f7e58e10e7975f7367bfd97159333d5a12` src/topic3_spectral/analysis.py (= freeze)

Final report delivery: the dispatch makes my structured return the final report. Nested spawning and messaging to the parent are not used.
