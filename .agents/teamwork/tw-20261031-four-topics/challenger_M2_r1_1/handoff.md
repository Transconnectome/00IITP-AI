# challenger_M2_r1_1 — handoff (Hard), M2 Topic 3 (T3.1–T3.4), 2026-10-31 ~11:50Z

Probes and logs: `/home/juke/git/00IITP-AI/verification/challenger_M2_r1_1/`. No production file was written. The copied tree used for test and mutant runs (`verification/challenger_M2_r1_1/tree/`, 50 MB) and the scratch mutant trees have been deleted.

## Challenge Summary

**Verdict: REFUTED, scoped.**

What holds, so nothing needs rerunning:
- Every headline number reproduces independently.
- The card was frozen before every real-data result.
- Every verdict follows the card's rules.

What is refuted:
- (i) **The Family B estimand description**:
  - card §5 "1120×1536 (ceiling 1119)";
  - report §3 "about 6 of a possible 1119" and "2–5% increase in within-window dimensionality";
  - the worker handoff "Token PR is about 6 of a 1119 ceiling".

  The token matrices have rank 7 (8 spatial positions) and are time-invariant to 1e-6–1e-5.
- (ii) **The claim that the fixtures guard the verdict logic.** Six verdict-path mutants survive (N05, N06, N08, N09, N10, N11), and N05 flips the real H1b verdict.

**Overall risk: MEDIUM.** Both fixes are additive: a dated addendum 03, and new rule tests whose hashes are recorded in an addendum.

## 1. Observation

**O1. Integrity**
- C1 `sha256sum -c PROTECTED_HASHES.txt`: rc 0 with 67 OK, both before and after my work (`c1_before.log`, `c1_after.log`).
- `output_sha256.txt`: all OK (`output_pins_after.log`).
- `addendum_02_sha256.txt`: OK.
- `code_sha256_at_freeze.txt`: all OK except `scripts/topic3_launch_connectome.py`, which addendum 01 #2 discloses.

**O2. Tests.** `tests/topic3_spectral` on a byte copy gives 54 passed (`pytest_topic3_copy.log`; 509 s on a loaded host).

**O3. Family A, recomputed independently** (`probe_family_A.py/.log/.out.json`)
- Method: SVD of the centered matrix, my own standardisation, and my own subsample draws (seeds 777/999).
- E1 covPR and corrPR equal the frozen JSON to ≤ 1.1e-14 for all 7 matrices.
- Replaying the package's index sets gives the same A1 L2−L3 point (|Δ| = 0).
- My independent subsets:

  | Contrast | covPR | corrPR |
  |---|---|---|
  | L2−L3 | +5.39 [3.22, 7.55] | +6.07 [4.27, 7.88] |
  | BrainJEPA−BrainLM | +2.12 [0.80, 3.43] | |
  | NeuroSTORM−BrainLM | +3.41 [1.74, 5.07] | |

- D1 and D3 conclusions are identical to the frozen ones. Distance from the decision boundary (|point|/SE): L2−L3 4.9, BrainJEPA−BrainLM 3.2, NeuroSTORM−BrainLM 4.0.

**O4. T3.1 / J1.** Uncentered PR from my SVD equals `empirical_results.json` `participation_ratio_PR` to 4 dp for all 7 matrices (1.0014 … 1.0102). The mean-vector energy fraction is 0.9645–0.9992.

**O5. Family B, recomputed independently from the saved spectra npz** (`probe_family_B.py/.log/.out.json`)
- PR recomputed from the saved float32 eigenvalues matches the saved PR scalars (max relative difference 1e-7).
- Per-checkpoint mean log ratios equal the frozen values (|Δ| = 0).
- My own tests: 200k-flip sign-flip, bootstrap and Holm.
  - H1a: all four checkpoints p < 1e-5.
  - H1b: all four checkpoints p ≤ 1e-5. Deep L1e-4 had 1 extreme flip out of 200k.
- My from-scratch card §5 rule gives H1a **holds** (agreeing: both deep checkpoints) and H1b **not replicated** (agreeing: L5e-5 only). Both match the frozen verdicts.
- A1b corr point estimates are within 0.05 of the frozen values on independent subsets, and all are negative.
- The primary `pooled__L0..L3` match the local pinned npz (max |Δ| 4.8e-7).

**O6. Freeze order** (`freeze_order_check.log`; times are UTC from mtime and `started_utc`)

| Event | Time |
|---|---|
| card last written | 08:43:40 |
| `card_sha256.txt` written | 08:48:29 |
| alpha calibration (synthetic) | 08:40:02 (before freeze) |
| T3.1 reproduction | 08:31:12 (before freeze) |
| Family A start | 08:49:18 |
| token job tasks (sbatch `.out`) | 08:51:32–08:58:52 |
| Family B start | 09:01:59 |

- The `code_sha256` maps in all 6 run records (Family A, Family B and 4 token jobs) equal `code_sha256_at_freeze.txt`. There are 0 mismatches.
- The only frozen-list file modified after the freeze is the launcher (08:51:02, disclosed).
- The token job does not re-verify the card itself. Report §1 discloses this.

**O7. Mutation testing** (`mutants_challenger.py`, `mutants_challenger.out.json`, `mutants_challenger.progress.log`)
- 28 mutants of my own design. The control is clean: 54 passed.
- 20 were killed and **8 survived**:

  | Mutant | Change |
  |---|---|
  | N02 | sign-flip p without +1 |
  | **N05** | replication rule ignores sign agreement |
  | **N06** | rule ignores the primary CI |
  | **N08** | rule uses raw p instead of Holm |
  | **N09** | D1 uses `hi > 0` instead of `lo > 0` |
  | **N10** | D3 uses `any` instead of `all` |
  | **N11** | H1a wired to L3 vs L2 instead of L3 vs LN0(L2) |
  | N17 | jackknife SE without the (n−1)/n factor |

- Note: my first mutant run was INVALID, because my harness did not copy the protected old `src/*.py` modules and the control failed. It is kept as `run1_INVALID_harness_*`.
- **Real-data impact** (`probe_N05_real_impact.py/.log`). I applied N05 to the frozen per-checkpoint results:
  - H1b flips from **"not replicated" (1 agreeing) to "holds" (3 agreeing)**.
  - H1a stays "holds" (3 agreeing).
  - N06 changes nothing on the real data.
- The only rule test (`tests/topic3_spectral/test_analysis.py::test_token_contrast_and_replication_rule`, lines 60–70) has no fixture with a zoo checkpoint that is significant in the opposite direction. The real data contain exactly that case: HCP_N400 for H1a and H1b, and deep L1e-4 for H1b.

**O8. The token-level structure is degenerate**
- From the saved eigenvalues (`cat_cov_eigs__*`), the number of eigenvalues above 1e-5 × max, median over subjects, is **7** for L2, LN0L2 and L3 in all 4 checkpoints, and the top 10 eigenvalues carry 1.000 of the variance.
- L1 has 50–58 such eigenvalues and L0 has 81–203.
- This matches the number of spatial positions minus 1:
  - L2/L3: 2×2×2 = 8, so at most 7;
  - L1: 4×4×4 = 64, so at most 63.
- **Direct check on connectome** (`probe_connectome_time_invariance.py/.log`):
  - Setup: own torch-free reader, piped via stdin through `srun -p debug -w node2`, nothing written on connectome, positions 0/28/56, primary and HCP_N400.
  - In a single frame, the share of L3 token variance that lies across the 20 time steps at a fixed spatial position is **1.0e-6 (primary) and 0.9–1.1e-5 (HCP_N400)**.
  - Single-frame numerical rank: L2 = L3 = 7; L1 = 50–54.
  - Frame 0 vs frame 3 relative difference: 0.1–0.5% at L2/L3.
- Within-subject SD of log token PR across the 7 frames is about 3e-5–2e-4. The between-subject SD is 0.007–0.05.
- The Slurm job left nothing behind: `squeue -n chal_m2_probe` returns 0.

**O9. Variance ratio for H1a**
- Between-checkpoint variance of the per-checkpoint means is 0.00762.
- The mean within-checkpoint between-subject variance is 0.00057.
- The ratio is about 13.
- The log-eigenvalue profile correlation is 0.998–0.9998 within a checkpoint and 0.989–0.9995 across checkpoints.

**O10. Housekeeping**
- I grepped my verification and metadata folders for the subject-ID pattern `sub-[A-Za-z0-9]` and found no hits (rc 1).
- The layout lint over the run metadata root returns `findings: []`.

## 2. Logic Chain

1. **Computation and order.** O3–O6 show that the numbers are reproducible by independent code, that the card preceded every governed result, and that the frozen code ran. The claims of computation correctness and card-before-results are therefore CONFIRMED.
2. **Verdicts.** By O3 and O5, the from-scratch D1, D3 and H1 rules reproduce every verdict. "Verdict follows card" is CONFIRMED.
3. **Rule logic is untested (O7).** The suite does not protect the decision logic. Six verdict-path mutants survive, and one (N05) would silently flip a real verdict. The production code is correct today, as shown by O5. But C3/T3.3's "fixtures that fail on the targeted defect" is not met for the replication, D1 and D3 rules or for the H1a wiring.
   - The worker's "Mutants 9/9 killed" is true for its own set. That set targets estimators and IO, not decisions.
4. **Family B measures spatial-position geometry (O8).** Family B's token matrices have at most 8 distinct directions per frame, one per spatial position, and are constant over time to 1e-6–1e-5. So the token PR at L2/LN0L2/L3 is the PR of 8 spatial-position embedding vectors, and its ceiling is **7, not 1119**. In the primary, the observed PR of 5.4–6.1 is 77–87% of that ceiling. Every checkpoint sits near the rank-7 ceiling; the deep checkpoints are at about 3.2–4.8 (H4 table).
   - Several statements are therefore factually wrong about the data:
     - card §5 "1120×1536 (ceiling 1119)";
     - report §3 "about 6 of a possible 1119";
     - report §3 "2–5% increase in within-window dimensionality";
     - the dynamic-range fixture's planted ranks 12 and 40, which are unattainable here.
   - "7 frames concatenated" adds essentially no information over a single frame. H4's "removes token-count dependence" does nothing at L2/L3, where each frame already has 160 tokens.
5. **The precise p-values do not show generalisation (O9).** Subject-level p = 0.0002 and CIs of about ±0.002 measure how precisely each checkpoint's quantity is estimated. The between-checkpoint spread is about 13× the between-subject variance, so the informative replication unit is the checkpoint: n = 3 zoo checkpoints, confounded by depth and training family (addendum 02). This does not change the card verdict, which is a rule outcome. It does limit what "H1a holds" can mean.
6. **Severity and scope.** Points 3–5 change no frozen number or rule outcome, so the computations and rule outcomes stand. But two things are refuted:
   - Point 4 refutes a stated headline, the token-PR ceiling and "within-window dimensionality".
   - Point 3 refutes the fixture-coverage claim for decision logic: a silent mutation flips a real verdict.

   Hence the verdict is REFUTED (scoped), and both points are blocking until the additive fixes land. Point 5 is non-blocking.
7. **Jackknife check.** The jackknife SEs used in report R1 reproduce exactly with my SVD leave-one-out (`probe_jackknife.log`: L1 3.5767, L2 1.2955, L3 0.2856). The surviving N17 therefore does not affect a cited number; it is LOW.
   - Nuance: L1's SE comes from a **single** subject. Leaving that subject out raises PR from 2.78 to 6.39. Report §2 says "a few subjects".

## 3. Caveats

- The time-invariance probe covered 3 subject positions × 2 checkpoints × frames 0 and 3, not all 57 × 4 × 7. The saved-spectra evidence (rank 7 for all subjects and checkpoints, frame SD at the 1e-4 level) is complete, so the generalisation rests on that.
- I did not determine why the deep tokens are time-invariant. It could be the model, the preprocessing, or the input normalisation.
- The "distinct rows" counter in the connectome probe used a tolerance that was too tight to merge rows, and it is uninformative. Rank and the variance share are the valid measures.
- I did not rerun the 86-test old suite or topic1. Other agents' pytest runs were active on the host. C1 and the topic3 suite were rerun.
- I did not re-derive the alpha calibration or the Clauset estimator beyond the mutation kills (N18 and N19 were killed).
- Subsampling SE formula: it matches the card as written (sd·√(m/(n−m))), and N15 was killed. I did not test its coverage.

## 4. Conclusion

**REFUTED (scoped).**

Confirmed, no rerun needed:
- T3.1: J1 is an artefact, reproduced exactly.
- T3.2: the card was frozen before results, verified by hash and time.
- T3.3 for the PR, α and centering fixtures.
- T3.4: the numbers and rule outcomes, including H1a "holds" and H1b "not replicated".

Refuted:
- (i) The Family B estimand description, in the card §5 ceiling statement, report §3 and the worker handoff.
- (ii) Fixture coverage of the verdict logic: N05, N06, N08, N09, N10 and N11 survive, and N05 flips real H1b.

**Fixes recommended to root** (all additive; nothing frozen needs editing):
- (a) Add rule-logic fixtures, then record the new test hashes in an addendum, because the tests are pinned in `code_sha256_at_freeze.txt`. Cases:
  - a significant opposite-sign zoo checkpoint must not count as agreement;
  - primary p < 0.05 but CI covering 0;
  - Holm vs raw p;
  - a D1 null with hi > 0 and lo < 0;
  - D3 with one contrast failing;
  - H1a pair wiring.
- (b) Write addendum 03 that corrects the Family B estimand. Token PR at L2/LN0L2/L3 is the PR of the 8 spatial-position vectors: ceiling 7, time-invariant to 1e-6 (primary) and 1e-5 (HCP). Restate H1a as "the stage-3 blocks make the 8 spatial-position embeddings slightly more isotropic in 3 of 4 checkpoints", not as "within-window dimensionality".
- (c) In that addendum, also state:
  - the replication evidence is n = 3 confounded checkpoints, with between-checkpoint variance about 13× the between-subject variance;
  - the L1 jackknife SE is driven by one subject.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt     # rc 0, 67 OK
LC_ALL=C sha256sum -c results/topic3/2026-10-31/output_sha256.txt                               # all OK
V=verification/challenger_M2_r1_1
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 $V/probe_family_A.py           # compare_to_frozen ~1e-14; D1/D3 true
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 $V/probe_family_B.py           # verdicts_indep == frozen; rank evidence
# mutation run needs a byte copy of the tree at $V/tree first (cp -a src scripts tests results/topic3/2026-10-31 docs/03_empirical_analysis/topic3)
/home/juke/superclaude-env/bin/python3 $V/mutants_challenger.py <scratch_dir> 7                # survivors: N02 N05 N06 N08 N09 N10 N11 N17
/home/juke/superclaude-env/bin/python3 $V/probe_N05_real_impact.py                               # also needs $V/tree; N05 flips H1b
ssh connectome 'cd /tmp && srun -p debug -w node2 -c 2 --mem=8G --time=00:15:00 --nice=100 python3 -' < $V/probe_connectome_time_invariance.py
```

**Invalidation conditions:**
- If a rule-logic test is added and N05/N06/N08–N11 are killed, finding 3 is closed.
- If the token npz eigenvalue rank is not 7 under a re-extraction, or the time-variance share at a fixed position is greater than 1e-3, finding 4 is withdrawn.
