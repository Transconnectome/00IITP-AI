# explorer_M2_r2_3 — handoff (Hard), M2 Topic 3 iteration 2, 2026-10-31 ~12:06Z

**Summary.** The M2 iteration-1 gate failed on two scoped, additive defects raised by challenger_M2_r1_1. No number, freeze order or rule outcome was refuted. (i) The verdict logic has no tests guarding it. (ii) The Family B estimand is described wrongly: the token matrices have rank equal to the number of spatial positions minus 1 and do not change over time, so "ceiling 1119" and "within-window dimensionality" are false. Fix (ii) with a new dated addendum 03 and fix (i) with one new test file plus a receipt. Do not re-freeze, rerun or rebuild anything. I drafted the test file and showed it kills all 21 surviving mutants from the four verifier harnesses, run on copies only.

Probes: `/home/juke/git/00IITP-AI/verification/explorer_M2_r2_3/` (hashes in `sha256_explorer_artifacts.txt`).

## 1. Observation

**O1. Gate record.** `FAIL (challenger_M2_r1_1 REFUTED)`.
- The other verifiers passed: reviewer_M2_r1_1 APPROVE, reviewer_M2_r1_2 APPROVE, challenger_M2_r1_2 CONFIRMED, auditor_M2_r1_1 CLEAN.
- challenger_M2_r1_1's two blocking items are in `../challenger_M2_r1_1/handoff.md` §4:
  - (a) six verdict-path mutants survive; N05 flips the real H1b verdict;
  - (b) Family B is token PR over 8 spatial-position vectors, so its ceiling is 7, not 1119.
- Its stated invalidation conditions: kill N05/N06/N08–N11; or show the eigenvalue rank is not 7, or the time-variance share is > 1e-3.

**O2. Frozen state unchanged at 11:57Z.** No topic3 file is newer than 20:15 KST (11:15Z).
- C1 rc 0, all lines OK (`c1_check.log`).
- `output_sha256.txt` all OK (LC_ALL=C), `addendum_02_sha256.txt` OK.
- No `addendum_03` or `test_verdict_rules.py` exists yet.
- The tests are pinned: `code_sha256_at_freeze.txt` lines 14–23 and `output_sha256.txt` lines 32–42 list every existing `tests/topic3_spectral/*.py`. A new file is in neither list.

**O3. Verdict code** (`src/topic3_spectral/analysis.py`).
- `replication_verdict` (end of file) applies sign, Holm p and primary CI.
- D1 (`out["D1"]`, `lo > 0` for cov and corr) and D3 (`all(... lo > 0)`) are inline in `subject_level`.
- `TOKEN_PRIMARY` holds the H1a/H1b pair wiring.
- The only rule test is `tests/topic3_spectral/test_analysis.py::test_token_contrast_and_replication_rule`. It has no zoo checkpoint that is significant in the opposite direction, no "CI covers 0 but p is small" case, and no raw-vs-Holm case.
- `test_subject_level_null_does_not_claim_l2_gt_l3` asserts the interval but never the D1 flag.

**O4. Surviving mutants across all four verifier harnesses** (patterns taken verbatim from `verification/{challenger_M2_r1_1/mutants_challenger.py, reviewer_M2_r1_1/reviewer_mutants.py, auditor_M2_r1_1/auditor_mutants.py, challenger_M2_r1_2/probes/p6_mutants.py}`).

| Group | Mutants |
|---|---|
| Sign ignored | N05 = R1 |
| Primary CI ignored | N06 = R3 = X12 |
| Raw p instead of Holm | N08 |
| Holm α 0.5 | R8 |
| D1 uses hi or point | N09, M20 |
| D1 corr check ignored | X06 |
| D3 any | N10 = M22 |
| H1a wrong pair | N11 = R9 |
| Jackknife factor | N17, R7 (= M13 = X09) |
| Subsample SE | M14, R4 |
| LN eps | M15, R11 |
| Sign-flip +1 | N02 (= M18) |
| Rank-slope window | M10 |
| iid reference uniform | X13 |

**O5. Kill demo** (`kill_demo.py`, output `kill_demo.out.json`).
- 21 mutants plus a control. Each ran on a fresh copy of `src/topic3_spectral`, `tests/topic3_spectral`, `tests/__init__.py` and the pinned `family_B_token_level.json`, with `proposed_test_verdict_rules.py` installed as `tests/topic3_spectral/test_verdict_rules.py`, running only that file.
- **Control: 27 passed in 1.90 s. Survivors: none. Errors: none.**
- Two notes on the patterns:
  - reviewer R4's original pattern matched nothing. I re-expressed it with a valid pattern (`R4_..._fixedpattern`), and it is killed.
  - X13 first survived. It was killed after I added a deterministic pin of the iid-reference draw.
- The scratch trees were deleted afterwards. The production tree was never written.

**O6. Probe A** (`probe_a_saved_spectra_rank.py` / `.out.json`). This is a local read of the 4 pinned token npz files. They are keyed by position, and only aggregates were printed.

| Layer | Eigenvalues > 1e-5·max (min–max over subjects, all 4 checkpoints) | Energy in top (positions − 1) eigenvalues |
|---|---|---|
| L2 / LN0L2 / L3 | 7–10 | ≥ 0.99994 in the top 7 |
| L1 | 29–60 | ≥ 0.99994 in the top 63 (D = 768, so this is informative) |
| L0 | — | Uninformative: D = 384 < 511 |

- For every layer and checkpoint, |log cat PR − mean log frame PR| ≤ 1.1e-4 (mostly ≤ 2e-5). The within-subject SD of log frame PR is 4e-5–3e-4, against a between-subject SD of 0.01–0.07.
- Primary median cat covPR: L2 5.41, LN0L2 5.54, L3 5.67, i.e. 77–81% of 7.
- At the 1e-6 threshold, HCP_N400 has more small eigenvalues (medians 38/50/19 for L2/LN0L2/L3, against 7–9 elsewhere). I note this and do not interpret it.

**O7. Report wording now contradicted by the data** (`docs/03_empirical_analysis/topic3/2026-10-31_topic3_result_report.md`):
- line 102: "about 6 of a possible 1119", plus the dynamic-range fixture sentence (planted ranks 3/12/40);
- line 114: "2–5% increase in within-window dimensionality";
- line 154 (R2): "not the dimensionality of the token representation";
- card §5: "1120×1536 (ceiling 1119)", and H4 "removes the token-count dependence".

**O8. Non-blocking items carried by the other verifiers.**
- (a) reviewer_M2_r1_2: the addendum 02 copy list leaves out `docs/03_empirical_analysis/empirical_results.json` and `tests/__init__.py`.
- (b) challenger_M2_r1_2 N3: two rounding slips (A1 L2−L3 cov lo 3.2250 reported as +3.23; A1b L5e-5 corr −3.2849 reported as −3.29).
- (c) auditor: `test_outputs_no_ids.py` ends with `assert n >= 0`, which passes on an empty tree.
- (d) challenger_M2_r1_1 O9: between-checkpoint variance of the H1a means is about 13× the between-subject variance (0.00762 vs 0.00057), so the replication unit is n = 3 confounded checkpoints.
- (e) the L1 jackknife SE comes from one subject (PR 2.78 → 6.39 when that subject is left out).
- (f) `results/gpu_ledger_2026-10-31.md` does not exist. M2 used 0 GPU-h.
- (g) the human's "3번" (push) and the root's automatic checkpoint commits are a run-level C4 item, not M2's.

## 2. Logic Chain

1. By O1 and O2, both blocking items are about *interpretation and guards*. Every frozen number and rule outcome was independently confirmed by four verifiers and by challenger_M2_r1_1 itself. So the fix must be additive, and any recompute or re-freeze is out of scope. A second card written after the results would break C3's card-before-results order.
2. **Item (i).** By O3, the decision logic is untested at exactly the configurations the real data contain: significant zoo checkpoints of opposite sign; HCP_N400 for H1a and H1b; deep L1e-4 for H1b. O4 shows that the four harnesses found overlapping but different survivors. A fix aimed at only challenger_1's six would leave R8, X06, M20, M14, M15, M10 and X13 for the next challenger. O5 shows one new file kills the full union (21/21), with no change to src and no change to any pinned file. Closing (i) therefore means installing that file and re-running the union, plus the full suite.
3. **Item (ii).** O6 reproduces challenger_1's rank-7 finding from the complete saved spectra, not a 3-subject probe. It also extends the finding to L1, where the ceiling is 63 out of D = 768. So the defect is not only in H1a/H1b: the H4 L0→L3 profile, and R1's token-level support, compare PRs bounded by 383, 63, 7 and 7 (different numbers of spatial positions). That comparison cannot be read as layerwise dimensionality. Time-invariance (O6, cross-frame; challenger_1 O8, within-frame) means that concatenating 7 frames adds nothing. Hence the O7 sentences are false and must be superseded in a new addendum. The rule outcomes stay, because H1a/H1b are defined as those contrasts.
4. Challenger_1's invalidation condition for (ii) needs rank ≠ 7 or time share > 1e-3; O6 meets neither. Its *cause* (static anatomy-dominated input versus model behaviour) is not needed to close (ii). Probing it would add a new real-data exposure, so the addendum should say "cause not determined".
5. O8 items can be folded into the same addendum at no extra cost. Doing so removes known targets for the iteration-2 verifiers.

## 3. Caveats

- The kill demo ran only the proposed file, not the full 54-test suite, so interactions with existing tests are unverified. The worker must run the full topic3 suite, the old 86-test suite and topic1 in the production tree after installing the file.
- The D1/D3 tests stub `analysis.paired_subsample_delta` and identify pairs by matrix width. This is coupled to the current call signature; it is fine while src stays frozen.
- The real-data regression test reads the pinned `family_B_token_level.json`. That ties the test to frozen outputs, which is intended for a frozen milestone.
- X13 (uniform vs Gaussian iid reference) is pinned by draw-replay, which is an implementation pin rather than a statistical test. The reference decides no claim.
- I did not verify the O8(b) rounding slips myself, and I did not probe connectome. The within-frame time-invariance evidence is challenger_1's (3 positions × 2 checkpoints); the cross-frame and rank evidence is mine (all 57 × 4).
- The "3번. A" meaning is taken from worker_M2_r1's reading of root's transcript (3 = push, A = reuse saved results). The fix plan is the same under either reading.

## 4. Conclusion

Recommended fix for iteration 2. Additive only; it needs a new worker identity (e.g. `worker_M2_r2`), not `worker_M2_r1`.

1. **Install the test file.** Copy `verification/explorer_M2_r2_3/proposed_test_verdict_rules.py` (sha256 69fbd923…cad6) to `tests/topic3_spectral/test_verdict_rules.py`. Edit it only if the worker's review finds a defect. Do not edit src or any pinned test.
2. **Run the full suites in the production tree.** Run the topic3 suite (expect 54 + 27 = 81 passed), the old 86 under STRICT_E2E, and topic1. Then re-run the union of mutants on copies: `kill_demo.py`, adapted to the worker's own folder. Also run the full suite under every mutant, in copies only. Target: 0 survivors.
3. **Write addendum 03** as a new file, `docs/03_empirical_analysis/topic3/2026-10-31_topic3_addendum_03.md`, plus a new receipt `results/topic3/2026-10-31/addendum_03_sha256.txt` holding the hashes of the addendum and the new test file. Do NOT touch `output_sha256.txt` or `code_sha256_at_freeze.txt`. The addendum states:
   - (a) The Family B estimand. At L2/LN0L2/L3, token PR is the PR of the 8 spatial-position vectors, with ceiling 7 and primary at 77–81% of it. At L1 the ceiling is 63. Tokens are time-invariant both within and across frames.
   - (b) The superseded sentences: report lines 102, 114 and 154, card §5 "ceiling 1119", H4 "removes token-count dependence" (a no-op at L2/L3), and the dynamic-range fixture's relevance.
   - (c) The restated reading of the verdicts, with outcomes unchanged:
     - H1a "holds" = in 3 of 4 checkpoints the stage-3 blocks make the 8 spatial-position embeddings slightly more isotropic, with the norm matched;
     - R2's token-level part = no evidence of collapse in spatial-position geometry, and within-window temporal dimensionality cannot be measured here;
     - H4 / R1 token profile = not interpretable across layers, because the ceilings differ.
   - (d) The replication unit is n = 3 checkpoints, confounded by depth and family; the ratio is about 13×.
   - (e) The L1 jackknife SE comes from one subject.
   - (f) The rounding slips, the copy-list omission, and that M2 used 0 GPU-h.
   - (g) An exposure log of the post-freeze quantities: the verifiers' recomputations and probe A.
   - (h) The cause of time-invariance (input vs model) is not determined.
   - (i) No new card or rerun for Family B, because re-specifying it after these results would be post hoc. A future H2 or other card must list all of this as exposure.
4. **Send iteration 2 to a fresh review panel** (2 reviewers, 2 challengers, 1 auditor). Give them addendum 03, the new test file, and the safe-reproduction rule (copied trees only).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # rc 0
LC_ALL=C sha256sum -c results/topic3/2026-10-31/output_sha256.txt                                  # all OK
V=verification/explorer_M2_r2_3; LC_ALL=C sha256sum -c $V/sha256_explorer_artifacts.txt
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I $V/probe_a_saved_spectra_rank.py   # ranks 7 at L2/LN0L2/L3, energy>=0.99994
/home/juke/superclaude-env/bin/python3 -I $V/kill_demo.py $V/_scratch && rmdir $V/_scratch            # control 27 passed; survivors []
```

**Invalidation conditions:**
- the kill demo control fails, or any listed mutant survives;
- installing the file breaks any existing topic3, old-86 or topic1 test;
- re-extracted token spectra show rank > 7 at L2/L3, or a time-variance share > 1e-3;
- a pinned file changes before the worker starts.
