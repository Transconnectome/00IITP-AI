# handoff — challenger_M2_r3_2 (M2 Topic 3, iteration-3 gate) — Hard handoff, 2026-11-01T07:35Z

Verdict under the dispatch criterion: **REFUTED**. No real-data verdict changes; the five r2b blocking classes ARE closed;
but two further classes on the frozen decision/report path are unguarded by the 121-test suite (blocking 1–2), plus a
lower-severity producer-path gap (blocking 3).

## Challenge Summary
Overall risk assessment: MEDIUM. The pinned results are correct and reproducible; the gap is in the regression guards
that iteration 3 was meant to complete (a future edit/rerun of Family A, or of the D1 rule, would pass the suite while
changing a card verdict or report-cited numbers).

## 1. Observation
All evidence under `/home/juke/git/00IITP-AI/verification/challenger_M2_r3_2/` (my own folder). No production file written.

O1 Own tree `tree_base` built by `tools/make_tree.sh` (byte copy; manifest `tree_base.manifest_sha256.txt`, 84 files, checked
   against production: all OK). Controls: shipped 121 suite → 121 passed, 0 failures, 0 errors, **0 skipped**
   (`logs/ctrl_full.{log,xml}`); shipped 88 suite → 88 passed, 0 skipped (`logs/ctrl_s88.*`).
O2 My own 36 mutants (`mutants/my_specs.py` sha256 0be048a3…; runner `mutants/run_my_mutants.py` 16577550…), each in a
   fresh copy, `timeout 900`, 2 jobs at a time, KILLED only with rc 1 + named failing test in JUnit.
   121 suite (`mutants/RUN_full.json` 5934355e…): **14 KILLED, 22 SURVIVED, 0 INVALID, 0 NOT_APPLIED**.
   Shipped 88 suite on the r2b-class representatives + VA01/02 (`mutants/RUN_s88.json` baaa9cfd…): 9 SURVIVED.
O3 r2b blocking classes, re-written by me from the gate-record descriptions (not copied from any harness):
   CF01 V01 primary raw p; CF02 A07 ci95 [hi, lo]; CF03 V05 zoo needs CI; CF04 A01 first 25 rows; CF05 V26 ZOO[0] primary;
   CF06 X02 ZOO[2] primary; CF07 V29 HCP zoo dropped → all 7 SURVIVE the shipped 88 and are KILLED by the 121 suite, each
   by named r3 tests (e.g. CF01 by test_primary_raw_p_below_alpha_but_holm_p_not_is_not_significant[H1a,H1b] and
   test_primary_holm_rule_end_to_end_at_card_resolution; CF06 by test_token_stats_script_uses_the_card_primary_…).
O4 **D1 corr-only branch (card §4 D1)** — survivors of the 121 suite:
   - VA01 `analysis.py:77` `if out["D1"]["L2_gt_L3_cov_robust"] else "drop not robust")` → `if (cov_robust or corr_robust) else …`
   - VA02 `analysis.py:74` first branch keyed on `L2_gt_L3_corr_robust` instead of `L2_gt_L3_cov_robust`.
   Witness `probes/witness_d1_corr_only.py` through the shipped `analysis.subject_level` at the card PARAMS
   (iid/colperm 1000, m = 28, S = 2000), synthetic 57-row matrices (L2 = independent heterogeneous-SD columns, L3 = rank-6
   equal-SD columns):
   - D = 64: L2−L3 cov interval lo −2.94, corr lo +13.88 (`probes/witness_*.out.json`);
   - real shape 57×1536: cov lo −3.84, corr lo +20.73 (`probes/witness_d1_D1536.out.jsonl`).
   Shipped D1 verdict "drop not robust" (= card: robust iff cov lo > 0); VA01 → "drop robust in cov only: attributable to
   per-channel gain (final LN)"; VA02 → "drop robust and not a per-channel-scale effect". No existing test has cov lo ≤ 0
   with corr lo > 0 (iteration-2 D1 tests cover both / neither / cov-only; r3 covers [0, 0]).
O5 **Family A reported numbers** — survivors of the 121 suite whose real-data rerun changes pinned values. Harness
   `reruns/rerun_family_a.py` reruns the (mutated) `scripts/topic3_subject_level.py` in a copied tree (OUT redirected by
   script location), compares the 300 non-run leaves with the pinned `family_A_subject_level.json`.
   Control (unmutated, OMP 2): 300/300 identical, max rel diff 0.0 (`reruns/famA_CONTROL.json`). Mutants (`reruns/famA_*.json`):
   | Mutant (analysis.py) | changed leaves | example (pinned → mutant) | cited in report? |
   |---|---|---|---|
   | FA05 jackknife on corrPR (l.39) | 28 | L1 jackknife SE 3.577 → 4.609; L0 0.276 → 0.725; BrainLM 0.767 → 0.846 | yes: §2 table, R1 basis "unstable L1 (jackknife SE 3.58)", addendum 03 §3 |
   | FA06 A2 calibration iid at n = 25 not m = 12 (l.88) | 7 | BrainLM 0.406 → 0.189; BrainJEPA 0.598 → 0.279; NeuroSTORM 0.734 → 0.351 | yes: §2 A2 "m = 12 mean covPR / iid(12, D)" |
   | FA07 A2 m = 12 mean on corrPR (l.89) | 14 | BrainLM 0.406 → 0.540; BrainJEPA 0.598 → 0.700 | yes (same column) |
   | FA03 colperm q2.5 → q5 (l.48) | 14 | L0 44.77 → 44.87; BrainLM 43.92 → 44.01; NeuroSTORM 21.67 → 21.72 | yes: §2 "column-permutation null q2.5" |
   | FA09 iid reps halved at the call (l.40) | 56 | L0 iid mean 48.769 → 48.778 | yes: §2 "iid reference mean" |
   | FA08 SWIFT_PAIRS ("L2","L1") → ("L1","L2") (l.30) | 14 (key renamed, sign flipped) | L2−L1 +4.67 [+2.96, +6.39] → L1−L2 −4.67 [−6.39, −2.96] (read from a retained rerun; exact mirror) | yes: R1 basis |
   | FA01 covPR/(n−1) → /n (l.44) | 14 | 4% change | no (JSON only) |
   | FA02 iid q97.5 → q95 (l.47) | 14 | ≤0.2% | no (JSON only) |
   | FA04 covPR/iid by median (l.47) | 14 | ≤0.04% (below printed precision) | column cited, value unchanged at 3 d.p. |
   | FA10 A2 calibration by median (l.91) | 7 | ≤0.04% | column cited, value unchanged at 3 d.p. |
   D1/D2/D3 stay equal to the pinned verdicts in every case. Addendum 05 §6 itself states "Family A numbers other than the
   A2 row identity are not re-derived by the r3 tests". The positive control of this harness: CF04 (A01) changes exactly
   the 78 A2 leaves the r2b reviewer reported.
O6 **Dead-column floor wiring** — survivors: TJ03 (`token_job.py:96` `corr_eigs(Xcat)` → `corr_eigs(Xcat, 0.0)`) and FA11
   (`analysis.py:38` `pr_corr(X, 0.0)`). Real data: 0 changed leaves (all `cat_corr_dropped` = 0; Family A FA11 0 diffs).
   Witness `probes/witness_tj03_dead_channel.py`: synthetic frames whose L3 = LN0(t)·γ + β with γ₀ = 1e-5 (a near-dead final-LN
   channel, card §3 floor case): shipped cat_corr_dropped L3 = 1, cat_corrpr L3 18.809, H1a d −0.1959; TJ03 dropped 0,
   18.953, d −0.1883 (`probes/witness_TJ03.out.jsonl`). FA11 witness `probes/witness_fa11_dead_column.py` (57×64, column 0
   SD 1e-5 × median): shipped E1 corrPR 5.0948, FA11 5.1180 (`probes/witness_FA11.out.jsonl`).
O7 Other survivors (nonblocking, see Logic): VB02 (`analysis.py:190` sign from CI midpoint) — witness
   `probes/witness_vb02_direction.py`: mean d +0.002, CI [−0.0701, +0.0538], Holm p 0.944: verdict "killed" either way, but
   direction "L3 higher" → "L3 lower" and n_other_checkpoints_agreeing 0 → 3 (`probes/witness_VB02.out.jsonl`).
   MC01/MC02 (Family A seed offsets; 42/27 leaves change on rerun, MC-only). FA13/FA14 (tie-only; 0 real diffs).
   GD01/GD02/GD03 (removed halts for states the pinned hashes / job checks make unreachable; 0 real diffs).
   Killed: VA03, VB01, FA12, PB01, PB02, TJ01, TJ02, CF01–CF07.
O8 Headline recomputed with my own code (`probes/recompute_family_b.py`, does not import src): from the 4 pinned npz, frozen
   seed schedule → **0 mismatches** with the pinned per-checkpoint means, raw p, Holm p, CIs, frac_negative; H1a "holds"
   (2 of 3), H1b "not replicated" (1 of 3). With unrelated seeds the verdicts are the same. Pinned D1/D3/D2 follow the card
   rules from the pinned intervals: L2−L3 cov lo 3.225, corr lo 4.277; D3 lo 0.768 and 1.717; every p_low 0.000999.
O9 Addendum checks: addendum 05 §5 figures reproduce (H1b −10.68 / −3.24 / +4.57 / +8.24 %; H1a −12.78 / +2.30 / +3.85 /
   +5.01 %; CI half-widths H1a 0.0020–0.0096, H1b 0.0039–0.0144; 508 leaves; cat_cov_eigs__L0 57×384; 160×384 → 159
   eigenvalues). Addendum 05 fixture numbers reproduce (class 1: raw p 0.0326, Holm 0.0652, CI [0.0007, 0.0103]; class 2:
   Holm 0.0321/0.0308, CI lo −0.0014). Addendum 03 numbers reproduce (`probes/check_addenda_numbers.out.json`): L1 jackknife
   SE 3.577, LOO max 6.390 / next 2.838 / median 2.750, SE without that value 0.149; checkpoint variance ratio 13.36 / 5.84;
   top-7 share min 0.999942; within/between SD 0.0030–0.0048 (median within) [0.0032–0.0059 with mean, as r2b noted].
   Git claims of addendum 05 §5 verified read-only (path-restricted): addendum 03 commits only 4ce1917 (2026-10-31T12:31:25Z,
   blob 725d5077…) and ef27b71 (73489661…); 0db0336 does not touch addendum 03 and adds the two iteration-2 tests.
O10 Freeze order: card blob committed in 24fe976 at 2026-10-31T08:46:25Z with the frozen sha256 683374565d80…; card_sha256
   record "frozen 08:48:29Z"; Family A run started 08:49:18Z, Family B 09:01:59Z (run records); src and scripts equal
   `code_sha256_at_freeze.txt` except `scripts/topic3_launch_connectome.py` (disclosed, addendum 01 item 2).
O11 Final production checks (after all my runs): C1 67 OK rc 0 (`logs/final_c1.log`); receipts output/02/03/04/05 all rc 0;
   0 `.pyc` newer than my start under src/topic3_spectral, scripts, tests/topic3_spectral; no process of mine left.

## 2. Logic Chain
L1 (from O1, O3) The r2b gate's five blocking classes are closed: my independently written representatives of each class
   survive the shipped 88 and die under the 121 suite, killed by the r3 tests named in addendum 05 §2.
L2 (from O4) Card §4 D1: "L2 > L3 robust" iff covPR lo > 0; "not a per-channel-scale effect" iff corrPR lo > 0 as well;
   cov passes/corr fails → per-channel gain. When cov fails the card verdict is "not robust" regardless of corr. VA01/VA02
   output a robust-drop verdict in that case, on inputs the shipped producer itself generates at card parameters and at the
   real 57×1536 shape. They pass all 121 tests. This is the same kind of gap the r1 and r2b gates failed on (verdict branch
   unguarded, reachable through the producer), now on the D1 rule instead of the H1 rule → refutes (verdict change).
L3 (from O5) Family A has no output-regression test: the only Family A wiring test stubs `subject_level`, and the r3 unit
   test pins only the A2 row identity. Ten semantic Family A mutants pass all 121 tests and, ON THE REAL PINNED INPUTS,
   change 7–56 pinned values, including values the report cites in §2 and as the basis of R1 (L1 jackknife SE 3.58;
   ΔPR L2−L1 +4.67) and of R3's D-calibration (0.406 / 0.598 / 0.734). That meets the dispatch criterion directly
   ("can change ... a reported number"; here it is reached on the actual inputs, not only on synthetic ones) → refutes.
   The parallel with r2b B3 (A01, 78 A2 numbers) is partial: A01 also fed D3's inputs, whereas FA03/05/06/07/09 feed no
   verdict. The blocking claim rests on the criterion, not on the analogy.
L4 (from O6, O7) Low-severity tier, same classification for all three: (a) the card §3 dead-column floor is passed
   explicitly at two call sites (token_job.py:96, analysis.py:38) that no test exercises with a near-dead column; removing
   it changes reported corrPR / dropped counts (and the H1a log ratio) on a reachable input (final-LN gain near 0);
   (b) VB02 changes the reported `n_other_checkpoints_agreeing` (0 → 3) and `direction` of a 'killed' record whose mean d is
   nonzero (card §5 defines the sign there), through the shipped producer at B = 9999. None is shown to flip a verdict and
   none is active on the frozen inputs (max dropped 0; every primary CI excludes 0). They meet the criterion (reachable,
   change a reported number) → low-severity blocking.
L5 (from O7) Not refuting: MC01/MC02 reshuffle Monte-Carlo draws (card fixes only the base seed); FA13/FA14 differ only at
   exact ties of fields the card does not define; GD01–03 remove halts for states unreachable under the pinned hashes.
   U127 (worker's lone survivor) is equivalent as stated in addendum 05 (zero-mean direction label; a zero mean has p = 1
   through the producer, so verdict and agreement count are unchanged); I concur. VB02 is not equivalent in that sense.
L5b (from O5, FA09) Addendum 05 §6 accuracy: it says Family A numbers are not re-derived but "the card parameters that define
   them are pinned by test_params_equal_frozen_card". FA09 (`iid_reps // 2` at the call site, PARAMS unchanged) shows that
   pinning PARAMS does not pin how a parameter is used; FA05/06/07 change the estimator or reference without touching
   PARAMS. Nonblocking text inaccuracy; every other addendum 03/05 number I checked is correct.
L6 (from O8–O10) The real-data verdicts, the headline numbers and the addendum 03/05 corrections are accurate and reproduce
   independently; the card was frozen and committed before any result. The defects are in test coverage only.

## 3. Caveats
- All survivors concern regression guards; none changes a pinned result or a real-data verdict. The pinned outputs are
  protected by receipts, so the risk is to future edits/reruns, which is the risk iteration 3 was asked to guard.
- The D1 witness uses constructed synthetic matrices (not real data), at card parameters; same standard as the r2b V01/A07
  witnesses. The TJ03 witness uses small synthetic frame shapes (test_token_job layout).
- "Cited in report" was judged by matching report §2/§4 tables and text; FA04/FA10 changes are below the printed precision.
- I did not rerun the old 86-test suite or tests/topic1_lagmotif, the token job on real frames (connectome), or the worker's
  151-patch union; I confirmed the five classes with my own 7 representatives instead.
- Two `mutants/logs/TJ01_*` files contain the literal BIDS subject-prefix token (no identifier) from the echoed assertion source of
  test_token_job_driver.py (no identifier).
- Independence: I did not read the other r3 gate members' folders.
- Deviation (own): DISPATCH.md first section abbreviated five fields of the worker JSON; an appended section (07:30Z) now
  holds them verbatim. Hashes of everything I tested: `verification/challenger_M2_r3_2/logs/tested_artifacts_sha256.txt`.
- Not covered by me: old 86-test suite and tests/topic1_lagmotif (not rerun); token job on real frames (connectome);
  the worker's full 151-patch union (sampled by my 7 class representatives); T3.1/T3.3 fixtures not re-audited beyond
  passing in the suite.
- Minor (worker handoff, not pinned): O10 of worker_M2_r3/handoff.md lists four checkpoint drafts of addendum 05; a fifth
  (b91143c, 06:16:28Z, sha256 f2ede991…) predates its handoff, and a910c53 (06:31:28Z) now holds the final bytes a4001f09…,
  so "modified against HEAD" is stale.
- Pre-existing, disclosed: the label "killed (primary CI includes 0)" is also given when Holm p ≥ 0.05 and the CI excludes 0
  (addendum 03 §3 / 05 §5); card §5 does not name that case.

## 4. Conclusion
REFUTED for M2 iteration 3 as a closure of the decision/report path. What holds: the five r2b blocking classes are closed;
every real-data verdict (H1a holds, H1b not replicated, D1 robust and not a per-channel-scale effect, D3 reproduces, J1 artefact,
H2 untested) and every checked headline/addendum number reproduces; the card was frozen before results. What fails:
1. D1 corr-only branch unguarded (VA01, VA02 survive 121; witness flips the D1 verdict at card parameters and real shape).
2. Family A reported numbers unguarded (FA01–FA10 survive 121; real-data rerun changes 7–56 pinned leaves incl. cited values).
3. Low severity: dead-column floor call sites unguarded (TJ03, FA11) and VB02 (killed-record agreement count/direction);
   reachable witnesses change reported numbers; inactive on the frozen inputs; no verdict flip shown.
Cheap additive fixes (no src/scripts change, no rerun of record): (1) a D1 test with cov lo ≤ 0 and corr lo > 0 (stub table
or my witness construction) asserting "drop not robust"; (2) a Family A analogue of the Family B wiring test: run the
unmodified topic3_subject_level.py in tmp_path (≈26 s) and compare all 300 non-run leaves with the pinned
family_A_subject_level.json (kills FA01–FA10, MC01/MC02); (3) a token_job / describe_matrix fixture with one near-dead column
(SD ≈ 1e-5 × median) asserting it is dropped and counted, and a killed-record fixture asserting direction/agreement follow
the sign of mean d (kills VB02).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI/verification/challenger_M2_r3_2
# the runner reads ./tree_base; to rebuild it: mv tree_base tree_base.old && ./tools/make_tree.sh $PWD/tree_base
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 mutants/run_my_mutants.py $PWD/mutants/RERUN.json full \
    VA01_D1_cov_only_branch_also_on_corr_only VA02_D1_first_branch_needs_corr_only FA05_jackknife_on_corrpr FA06_A2_calibration_iid_at_n25_not_m12
    # expect SURVIVED, 121 tests, 0 skipped
cd probes && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=../tree_base /home/juke/superclaude-env/bin/python3 witness_d1_corr_only.py 7
    # shipped: "drop not robust"; apply VA01/VA02 from mutants/my_specs.py to a copy and rerun → robust-drop verdicts
cd ../reruns && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 rerun_family_a.py CONTROL   # n_diff 0
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 rerun_family_a.py FA05_jackknife_on_corrpr  # n_diff 28
cd ../probes && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I recompute_family_b.py      # mismatches 0
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../tree_base /home/juke/superclaude-env/bin/python3 check_addenda_numbers.py
cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
```
Invalidation: any change to src/topic3_spectral, scripts/topic3_*.py, tests/topic3_spectral or the pinned results; a new test
that kills VA01/VA02 and FA01–FA10 would close blocking 1–2.
