# handoff — challenger_FU_D_r2_1 (FU_D iteration 2 gate; Hard handoff)

**Verdict: CONFIRMED.** The FU-D verdict `inconclusive` (measurement capacity at E192) follows the frozen card. The card was frozen and committed before any FU-D run. The headline gains recompute exactly. The r1 blocking mutants X45 and X22 are now killed. The 8 equivalence proofs hold. Nothing regressed.
Nonblocking: 14 of my 65 independently designed mutants survive the 195-test suite. None of them changes the shipped output. Three of them (CV09, CP01, CP02) turn a card-correct Stage-1 `inconclusive (stall-sensitive)` into `stop (killed)` on synthetic data. That path is unreachable under this card, because the F+ gate failed and Stage 1 is never run.

## 1. Observation

All paths are repo-relative to /home/juke/git/00IITP-AI. Logs and probes are in verification/challenger_FU_D_r2_1/.

- **C1 and receipts.**
  - `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` returns rc 0, 67/67. I checked at the start and at the end.
  - From the repo root, `grep -v '^#' <receipt> | sha256sum -c` passes for card_sha256.txt 1/1, code_sha256_at_freeze.txt 29/29, output_sha256.txt 34/34 and addendum_01_sha256.txt 23/23.
  - verdict.json sha256 = f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc (unchanged).
  - The only FU-D code file not in the freeze receipt is tests/topic2_fu_d/test_fud_r2_guards.py, which is pinned by addendum_01_sha256.txt.
- **Card frozen before results.**
  - The card_sha256.txt header says "2026-11-01T16:06:07Z (before any FU-D real-data run)".
  - `git show 34f4b30:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md | sha256sum` gives 1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b. Commit 34f4b30 is dated 2026-11-02 00:50:24 +0900 (= 15:50:24Z), and it is the only commit touching the card.
  - logs/jobs.jsonl: smoke 511 was submitted at 16:13:50Z and the F+ jobs 534/535/536 at 16:39:57–16:41:11Z.
  - run slurm.json: the jobs ran from 17:46:39Z to 19:03:29Z on b300-01, all COMPLETED. The output receipt is dated 19:13:37Z.
- **Independent recompute** (probes/recompute_gate.py, exact Fractions from raw test_num/test_den; no FU-D code imported).
  - Pooled test NMSE: E = 0.6558494816918741, C = 0.653467876277415, S = 0.6577736746995909. Each equals the recorded test_nmse within 6e-17.
  - Gains: (E−C)/E = 0.003631329262188746 and (S−C)/S = 0.00654601816368273. Both are < 1/100, so the gate fails.
  - All 3 records have status completed, Slurm COMPLETED, cfg E192_d22182, n_params 474226176, steps 8750, batch 16, lr 2e-4, mask 0.6, 16 terms, and post_checks_ok True.
  - The sidecar wrapper sha d598989b…b84e equals the freeze receipt and the current file. The sidecar argv carries --val-mask-seed 7001 and --test-mask-seed 7002.
- **Addendum claims checked against r1 raw records** (probes/r1_compare.py).
  - W1: r1 E36 F+ per seed, C-vs-E 2.772 % / 3.348 % and C-vs-S 2.900 % / 2.970 %. The means are 3.060 % / 2.935 %, so the card's "+3.06 / +2.93 %" are means, as the addendum states.
  - E3: the FU-D gate test_den equals the r1 Fplus_*_s0 test_den for E, C and S (16 each).
- **Errata reproduced with the frozen code on synthetic records** (probes/errata_probe.py).
  - E1: a failed gate plus an unplanned `Fplus_C_s1` dir gives rc 0, `inconclusive`, no flag. With a passing gate the same dir raises RecordError "unexpected run directory".
  - E2: a NaN test_nmse is accepted and gives `inconclusive`.
  - E4: a wrong sidecar wrapper sha is accepted without --wrapper-sha256 and rejected with it.
  - The addendum describes all three accurately.
- **Tests** (logs/).
  - tests/topic2_fu_d: 195 passed.
  - Old suite: 86 passed.
  - tests/topic2_rgpool: 113 passed, 3 skipped.
  - tests/topic1_lagmotif: 88 passed.
- **r1 blocking items, rechecked directly** (mutation/run2.log). Each mutant was killed, and each also changed the shipped output:
  - CX45 (DELTA = 0.0036) and CX45u (DELTA = 0.02): killed by test_delta_constant_is_the_card_value.
  - CX22 (the inconclusive JOINT_READING string set to the "null replicates" text) and CX22b (inconclusive mapped to the stop reading at the lookup): killed by test_script_gate_gains_of_half_a_percent_are_inconclusive.
- **Own mutation run** (mutation/mutants.py, run_mutants.py, run1.out.json; 65 mutants designed independently over verdict.py, records.py, the verdict script, seedplan.py, slurm.py and design.py).
  - The control was green: 189 passed, 1 deselected, shipped output unchanged.
  - 51 killed, 14 survived, 0 invalid, 0 not applied. **0 survivors change the shipped verdict.json.**
  - The survivors:
    - CV09: the stall rule ignores a category change when the category without stalled seeds is `inconclusive`.
    - CP01 / CP02: stall detection loops over arm S only, or C+S only.
    - CV15: decide does not pass δ to fplus_gate. Equivalent at the default δ; the script never passes another value.
    - CV19: the floor branch no longer short-circuits the stall check. Only the reason changes; the category stays inconclusive.
    - CR01: the token regex is loosened to `h\d+`. Equivalent, because the token list must equal the split tokens.
    - CR13: `post_checks_ok is False` instead of `is not True`, so a sidecar with the key missing or None is accepted.
    - CP03 / CP04 / CP05 / CP11: the secondary hierarchical bootstrap seed 0→1, B 10000→1000, num/den swapped, and per-subject seed-mean over the wrong axis. All are descriptive outputs that are never asserted.
    - CP07 / CP12 / CP14: protocol-flag conditions. Only the flags change.
- **Demonstration that CV09/CP01/CP02 can flip a category** (probes/stage1_stall_demo.py, .out).
  - Setup: synthetic gate pass, n = 5 plan, hcp_E_s4 stalled at 0.9995, C/S at seed 4 at 0.9989, seeds 0–3 I1 = 0, 0, 0.05 %, 1.0 %.
  - All seeds: hi(I1) = 0.00763, so stop. Seeds 0–3 only: hi = 0.01046, so inconclusive.
  - The repo code gives `inconclusive`, "stall-sensitive: category stop with all seeds, inconclusive without stalled seeds", which is card §8 step 7.
  - CV09, CP01 and CP02 each give `stop`, "upper 95% bound of I1 < delta … (killed)", with joint reading "null replicates at E192", while the suite stays green.
- **Equivalence proofs (addendum §4) checked by reading the code.**
  - Q08: the assignment comes after a return, so it is dead.
  - Q19 / S207: validate_completed forces every hcp token order to equal the split order.
  - Q21: load_runs sets rec only for the chosen completed attempt, so a failed_pending_rerun entry always has rec None.
  - S023 / S025: in needs_fminus, with F− missing, a Stage-1 `keep` implies verdict inconclusive and the reason "(keep pending F-)", and that reason implies `keep`. So A∨(B∧C) = (A∧B)∨C = A.
  - S160: attempt 0 completed with an attempt 1 present raises "rerun of a completed run" first.
  - S181: decide reads only `state != "completed"`, and the state is not written out.
  - All 8 hold.
- **C4.**
  - probes/c4_crosscheck.py reads the off-repo sealed r1 manifest and split in memory and prints counts only. Against 105 FU-D/r2 text files: 0 matches with the 132 sealed 6-digit numbers and 0 with the 88 sealed 16-hex tokens.
  - My own outputs (24 files): 0 sealed 6-digit or 16-hex matches, 0 16-hex token shapes, 0 BIDS labels.
- **Compute.** 0 GPU-h, with no B300 or connectome job and no ledger row. Probes ran on local CPU with nice and OMP_NUM_THREADS=2, at most 2 pytest processes at a time.

## 2. Logic chain

1. The card hash at freeze equals the content committed at 15:50Z. Every FU-D job was submitted after 16:13Z, so the card governs (Obs. C1/freeze).
2. Card §8 step 2 says that if F+ is computed and fails, the verdict is `inconclusive` and Stage 1 is not read. The recomputed gains 0.363 % and 0.655 % are both < δ = 1 %, so the gate fails and the verdict is `inconclusive`. Card §9(c) then gives "E192 adds no decision; the r1 E36 stop stands alone". Both match verdict.json (Obs. recompute).
3. The r1 gate failed only on X45/X22. The direct δ-down, δ-up, string and lookup mutants are now killed by literal-pinned tests (Obs. run2), so the gate defect is closed.
4. The worker's "0 non-equivalent survivors" refers to its 423-mutant union. My independent set finds 14 more survivors (Obs. own mutation), so that statement does not cover the whole verdict code. None of the 14 alters the shipped output, though, and no FU-D claim depends on it.
5. CV09, CP01 and CP02 can produce a false `stop` on Stage-1 data (Obs. demo). Stage 1 under this card runs only after an F+ pass, and the F+ gate is computed and failed. Card §7.1 and addendum §6 say any further E192 run needs a new card. So these paths cannot produce any verdict under this card. By the r1 gate standard (shipped-path flips are blocking), they are nonblocking. They become blocking for any new card that reuses src/topic2_fu_d/verdict.py or scripts/topic2fu_d_verdict.py.
6. The errata E1/E2/E4 are real frozen-code departures, as the addendum states. The shipped inputs lie outside them: 3 planned dirs, finite records, verdict regenerated with the freeze wrapper sha. So they do not change the verdict.

## 3. Caveats

- I used no GPU re-evaluation of the saved checkpoints. r1 verifiers (Slurm 574/575/576) already re-scored them bit-exactly, and r2 changed no run. My recompute starts from the copied-back num/den, not from the checkpoints.
- My mutation set is independent but not exhaustive (65 + 4 mutants). test_e192_model.py and the receipt belt test were excluded from mutation runs; they were run in the full suite.
- stage1_stall_demo.py was run once with gains that did not flip the category (all four trees gave stop). I then changed only the g1 line by sed, to grid-searched values, and reran. The first output was overwritten. The parameter change is noted in the file comment.
- mutants.py had 4 mutants appended after run 1. The run-1 file sha is in mutation/mutants_run1.sha256.
- `rm` was denied by the harness, so `verification/challenger_FU_D_r2_1/mutation/__pycache__/` (my own bytecode) and scratchpad copies remain. They are not in metadata and not in production paths.
- I did not judge the scientific interpretation beyond the card. The F+ gate cannot separate "apparatus cannot detect δ at E192" from "grouping stops mattering at E192" (addendum §6). E improved more from E36 to E192 (0.677→0.656) than C did (0.658→0.653).

## 4. Conclusion

CONFIRMED for FU_D iteration 2: the verdict, numbers, freeze order, X45/X22 closure, errata, equivalence proofs and no-regression all hold.

Nonblocking carry-forward: before any new card reuses the FU-D verdict code, add tests that do two things:
- (a) a stalled E or C run is detected by the script (kills CP01/CP02);
- (b) a stall whose drop makes the category `inconclusive` yields `inconclusive (stall-sensitive)` (kills CV09).

Optionally also:
- pin `post_checks_ok` missing → RecordError (CR13);
- pin the secondary bootstrap (B = 10,000, seed 0, num/den order) and the per-subject seed-mean axis (CP03/04/05/11);
- pin the protocol-flag conditions (CP07/12/14).

## 5. Verification method

- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- For each receipt in results/topic2/2026-11-02_fu_d/: `grep -v '^#' <receipt> | sha256sum -c`
- `git show 34f4b30:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md | sha256sum` → 1b7fee6c…001b
- `PYTHONDONTWRITEBYTECODE=1 python3 -I verification/challenger_FU_D_r2_1/probes/recompute_gate.py`
- `STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q` → 195 passed
- `python3 verification/challenger_FU_D_r2_1/mutation/run_mutants.py /home/juke/git/00IITP-AI <workdir> <out.json> CV09,CP01,CP02` → 3 SURVIVED
- `python3 verification/challenger_FU_D_r2_1/probes/stage1_stall_demo.py <workdir>` → repo `inconclusive`, mutants `stop`
- Invalidation: any change to verdict.json, the receipts, or the FU-D src/scripts/tests voids this report.
