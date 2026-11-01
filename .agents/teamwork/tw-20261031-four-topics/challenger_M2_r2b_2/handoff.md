# challenger_M2_r2b_2 — handoff (Hard), M2 Topic 3 iteration 2 (r2b gate), 2026-11-01

All probes, logs and harnesses are in `/home/juke/git/00IITP-AI/verification/challenger_M2_r2b_2/` (called `V/` below). I wrote no production file and made no git write. The copied trees were deleted after use; `V/make_tree.sh` rebuilds them, and the manifests are kept.

## Challenge Summary

**Verdict: REFUTED (scoped). Overall risk: MEDIUM.**

**What holds (CONFIRMED). None of it needs a rerun.**
- **Numbers.** I reran the shipped code in a copied tree. Every Family A and Family B number reproduces bit for bit: 0 of 338 + 532 JSON leaves differ. An independent from-scratch recompute, with my own sign-flip test (B = 200 000), my own bootstrap and my own Holm, gives the same means and CIs and both verdicts:
  - H1a "holds": the two NewUAH checkpoints agree;
  - H1b "not replicated": only L5e-5 agrees.
- **Freeze order.** The card was frozen before every governed result, on three clocks:
  - file mtimes;
  - the `started_utc` fields in the pinned run records;
  - git: commit `24fe976` holds the card at its frozen hash at 08:46:25Z, and it is the card's only commit. Family A started at 08:49:18Z.

  Every run record's `code_sha256` equals `code_sha256_at_freeze.txt`.
- **T3.1** reproduces exactly.
- **Addendum 03 item 1** (ceiling 7, about 8 near-static spatial cells at L2/LN0L2/L3) is correct.
- **Iteration-1 finding (ii), closed as it was defined.** I extracted the specs by AST from the original harness sources, not from the worker's summary. All 8 iteration-1 survivors are killed by the shipped 88-test suite: N02, N05, N06, N08, N09, N10, N11, N17. MM 06 is killed, and only by `test_verdict_rules_r2b.py`.

**What is refuted.**

**R-1. The decision logic is not guarded beyond the assigned mutant set.** The claim is that the decision logic "is now guarded against all 67 assigned mutants". That is true for the assigned set, and the worker scoped it that way. But a fresh set of 34 verdict-path mutants still leaves non-equivalent, reachable survivors on the path the shipped verdict actually goes through:
- **A07.** `paired_log_contrast` stores `ci95` as `[hi, lo]`. This makes the primary "CI excludes 0" condition vacuous, which is the same decision effect as iteration-1's N06. N06 is now killed only because the rule tests use hand-built records that bypass the producer. Concrete witness:
  - Setup: Holm p = 0.0479 and CI [−0.00016, +0.0264].
  - The shipped rule gives "killed".
  - Mutant A07 gives "holds".
  - A07 still survives when the analysis is actually rerun.
- **A08.** `replication_verdict` takes the primary as the first dict entry and ignores `primary_label`. This is equivalent under the current call order only.
- **A06 / S03.** The A2/D3 matched-25 subset ignores the NeuroSTORM positions; only 9 of the 25 positions are shared. On real data, NeuroSTORM−BrainLM ΔPR₁₂ moves from +3.36 to +4.57. After a rerun, 79 Family A numbers differ from the pinned JSON. The suite still passes, and D3 is unchanged.

My witness tests pass on the shipped code (3 passed), and each one fails on its mutant. So every gap is real and can be closed with an additive test. **None of these changes a real verdict today**, because every real primary CI excludes 0 by a wide margin and D3 stays true.

**R-2. Addendum 03 §2 (H4 row) misdescribes Family B's H4 ceiling at L0.** It says the H4 profile "compares effective ceilings of 383 (D-limited), 63, 7 and 7". But H4 takes 160 tokens per frame (`token_job.py:82–87`), and `centered_eigs` returns at most min(n−1, D) eigenvalues. So the L0 H4 value has **at most 159** eigenvalues; it is n-limited, not D-limited.
- Synthetic full-rank frames with the real shapes: the 160-token-subsample L0 value returns 159 eigenvalues and PR ≤ 112, against a full-frame PR of 370.
- If the cells are near-static, a 160-token draw covers on average 138 of the 512 L0 cells and 59.6 of the 64 L1 cells.
- The conclusion ("cannot be read as dimensionality changing with depth") stands; the real L0 H4 maximum is 3.18.
- Addendum 04 §6 checked items 1, 3 and 5 plus the item-2 figure "77–88%". It did not check the item-2 H4 row.

This is LOW (descriptive), but it is an uncorrected Family B description error.

**Blocking, in my assessment: A07 alone.**
- It meets the MM 06 standard: it is non-equivalent, it is reachable at B = 9999 (Holm p 0.0479, CI [−0.00016, +0.0264]), and it flips "killed" to "holds".
- It survives a real rerun.
- Its witness test passes on the shipped code and fails on the mutant.
- It is the same kind of gap that blocked iteration 1 (N06): decision logic left untested at the interface the real verdict passes through.

**Not blocking:**
- A06/S03, rated MEDIUM. It is an unguarded verdict input that shifts the real D3 numbers by about 36%, though D3 is unchanged.
- A08, rated LOW. It is equivalent under the current callers.
- R-2. One erratum line fixes it.

One additive test file closes A07, A08 and A06 together (see §4). The gate decision belongs to the PI.

## 1. Observation

**O1. Integrity before work** (`V/baseline/`, 01:25Z)
- C1 `sha256sum -c PROTECTED_HASHES.txt`: rc 0, 67 OK.
- `output_sha256.txt`: 42 OK. `addendum_02`: 1 OK. `addendum_03`: 3 OK. `addendum_04`: 2 OK.
- The card equals `683374565d80…d1b8e0`.
- `code_sha256_at_freeze.txt`: only `scripts/topic3_launch_connectome.py` FAILS, which addendum 01 #2 discloses.

**O2. Freeze order** (`V/probe_freeze_order.py`, `.out.json`)

| Time (UTC) | Event |
|---|---|
| 08:31:12 | T3.1 reproduction |
| 08:40:02 | α calibration |
| 08:43:40 | card mtime |
| 08:46:25 | git `24fe976` holds the card at the frozen hash; it is the card's only commit (`git show 24fe976:<card> \| sha256sum`) |
| 08:48:29 | `card_sha256.txt` and `code_sha256_at_freeze.txt` |
| 08:49:18 | Family A `started_utc` |
| 08:53–08:58 | token jobs |
| 09:01:59 | Family B `started_utc` |
| 09:08:07 | `output_sha256.txt` |

- Both local run records carry `card_sha256_verified` equal to the frozen hash.
- The `code_sha256` maps of all 6 run records (8 + 8 + 4×7 files) match the freeze list with 0 mismatches.
- The result JSONs are untracked in git, so git can date the card but not the results. Their timing rests on `started_utc` inside pinned files, and on mtimes.

**O3. Shipped-code full rerun** (`V/rerun_shipped.sh`, `V/logs/rerun_shipped.log`, `V/logs/compare_rerun_shipped.json`)
- Ran in a copied tree whose 103-file manifest equals production. The copy also contained new `src/topic4_resu/*` files from the M4 team; all Topic 3 files are identical.
- `topic3_token_stats.py`: 19 s. `topic3_subject_level.py`: 24 s.
- Family A: 0 of 338 leaves differ. Family B: 0 of 532 leaves differ. The only exclusions are `started_utc`, `runtime_s` and `host`.
- D1 = "drop robust and not a per-channel-scale effect"; D3 = true; H1a "holds"; H1b "not replicated".

**O4. Independent Family B recompute** (`V/probe_numbers.py`, `.out.json`)
- All inputs match their pins.
- PR recomputed from the stored float32 eigenvalues equals the stored PR to a relative 5.2e-8.
- The means equal the JSON exactly (|Δ| = 0).
- My bootstrap CIs (B = 20 000, own seed) agree with the JSON to within 5e-4.
- My sign-flip p is at most 1.5e-5 everywhere, and my Holm p is at most 1.5e-5.
- My own card-rule implementation gives the same agreeing checkpoints and the same verdicts as the JSON.
- Every JSON Holm p is 0.0002.

**O5. Addendum 03/04 numbers** (same probe; all are post hoc and descriptive)
- Values that verify as printed:

  | Quantity | Value |
  |---|---|
  | top-7 energy minimum at L2/LN0L2/L3 | 0.9999416 |
  | max \|log cat − log mean-frame\| | 1.13e-4 |
  | H4/frame ratio at L2, LN0L2, L3 | exactly 1.0 |
  | primary medians, covPR L2 / L3 | 5.412 / 5.672 |
  | primary medians, corrPR L2 / L3 | 5.881 / 6.144 |
  | eigenvalue counts above 1e-5 × max | L2/LN0L2/L3 median 7, max 7–10; L1 29–60 (primary 50–55); L0 64–209 |
  | checkpoint variance ratio (ddof = 1) | 13.36 (H1a), 5.84 (H1b) |
  | CI half-widths | 0.00203–0.01442 |

- The worker's three mismatches are confirmed:
  - L1 top-63 minimum is 0.99993998, not ≥ 0.99994;
  - CIs are "±0.002–0.014", not "about ±0.002";
  - the JSON path lacks `results/`.
- The within/between SD ratio is 0.0030–0.0048 with worker_M2_r2's definition (median of the within-subject SDs). It is 0.0032–0.0059 with the mean. This is definitional, not a mismatch.
- **New text slip:** the pinned report §5 (line 166) still says "CIs of about ±0.003". The real half-widths are 0.002–0.014, and no addendum corrects that line.

**O6. H4 ceiling** (same probe, `h4` block)
- On synthetic full-rank frames with the real dump shapes, run through the package's `token_job.subject_summary`:
  - L0: the 160-token-subsample PR maximum is 112.4 against a frame PR of 370.1, with 159 eigenvalues returned;
  - L1: 131.8 against 479.5, also with 159 eigenvalues.
- `centered_eigs` on a 160×384 matrix returns 159 values.
- The stored concatenated L0 spectra hold 384 eigenvalues.
- The real 160-token-subsample L0 maximum is 3.18 in the primary.

**O7. My mutants, shipped 88-test suite** (`V/run_mutants_c2.py`, `V/logs/run_c2_A.json`, raw logs in `V/logs/run_c2_A/`)
- Setup: 01:29–01:37Z, 4 workers. Each mutant ran on a fresh copy with the full suite and no `-x`. Controls: 88 passed at start and at end. All 43 patches applied exactly once.
- **Re-check set (W), all killed:**

  | Mutant | Failing tests |
  |---|---|
  | N02 | 1 |
  | N05 | 7 |
  | N06 | 1 |
  | N08 | 3 |
  | N09 | 1 |
  | N10 | 1 |
  | N11 | 3 |
  | N17 | 1 |
  | MM06 | 2, both `test_verdict_rules_r2b` |

- **Own set: 7 killed, 27 survived.**
  - Killed: A02 (primary `<=`), A18 (Holm→Bonferroni), A19, A20, R02, R05, E01.
  - The survivors, with my classification:

  | Class | Mutants | Evidence and impact |
  |---|---|---|
  | **Producer / wiring** | **A07** ci95 `[hi, lo]` (**blocking**); A06 A2 first 25 rows and S03 script passes positions 0..24 (MEDIUM, not blocking); A08 primary = first key (LOW, equivalent under the current callers) | Witness tests (O8) and real impact (O9). A07 survives even after a rerun (O10). |
  | Equivalent | A15 (direction label for sign 0), A16 (`!= -sign`), R04 (Holm uncapped) | A mean of exactly 0 cannot have Holm p < 0.05. A Holm p above 1 never passes α. |
  | Measure-zero boundary | A01 (primary CI `>=`/`<=`), A03/A05 (D1 `lo >= 0`), A04 (D3 `lo >= 0`), R03 (sign-flip strict ties) | Unlike MM06's discrete Holm grid, `lo` = point − 1.96·SE and a percentile-bootstrap bound reaching exactly 0.0 are float coincidences of measure zero. Exact sign-flip ties need all-± flips (2⁻⁵⁶ at n = 57). LOW. |
  | Unpinned card parameters | A09 (m 28→27), A10 (S 2000→200), A11 (bootstrap B 9999→999), A12 (seed), A13 (m 12→13); R01 (bootstrap level 0.95→0.99) | Only `holm_alpha`, `replication_min_zoo_agree` and `signflip_B` are pinned by tests. The rest are guarded only by `code_sha256_at_freeze`. No real verdict changes (O10). MEDIUM-LOW. |
  | Decision threshold | A14 (D2 `< 0.025` → `< 0.05`) | Every real `colperm_p_low` is 0.001, so no real D2 can flip. D2 decides no layer claim (card §6). LOW. |
  | Descriptive | A21 (A1b orientation swapped), T01 (H4 never subsamples) | A1b is cited as the basis of the R2 row of the report. LOW. |
  | Script level, no unit tests | S01 (verdict with HCP as primary), S02 (seed shift), S04 (HCP dropped), S05 (`verify_card` disabled), S06 (npz hash guard off), S07 (re-pool guard off) | No test runs `topic3_token_stats.py`, `topic3_subject_level.py` or `verify_card`. S01 would flip real H1a to "not replicated" (O9). But once the script is re-executed, the shipped regression tests kill S01 and S04 (O10). S02 survives even after a rerun. S05–S07 are the C3/G2 guards; they have no test, and on valid inputs they are equivalent. LOW–MEDIUM, guarded by output and code hashes. |

**O8. Witness tests** (`V/witness/test_witness_c2.py`, `V/run_witness.py`, `V/logs/witness_summary.json`)
- Each run used a fresh copy of the tree.
- Shipped code: 3 passed.
- Mutant A06: only `test_A06_matched25_uses_the_neurostorm_positions` fails.
- Mutant A07: only `test_A07_primary_ci_covering_zero_is_killed_through_the_producer` fails.
- Mutant A08: only `test_A08_primary_label_is_used_even_when_not_first` fails.

**O9. Real-data impact** (`V/probe_survivor_impact.py`, `.out.json`)
- **A06.** The shipped recompute equals the pinned A2 values exactly: BrainJEPA−BrainLM point 2.0839, lo 0.7679; NeuroSTORM−BrainLM 3.3626 and 1.7174. Under the mutant, these become 2.9567 / 1.3226 and 4.5718 / 3.0069. D3 is true both ways.
- **S01.** Using HCP_N400 as the primary on the pinned per-checkpoint JSON:
  - H1a: "not replicated" with 0 agreeing (shipped: "holds", 2 agreeing);
  - H1b: "not replicated", 1 agreeing.
- **A07.** The synthetic witness is above (rng 11, trial 2416).

**O10. Rerun-then-test protocol** (`V/run_rerun_mutants.py`, `V/logs/rerun_c2_B.json` and `.progress.log`, raw logs in `V/logs/rerun_c2_B/`)
- For each mutant I re-executed both stats scripts in the mutated copy, then compared the output with the pinned JSON and ran the suite.
- Run window 01:43–02:00Z, 4 workers.
- Control: both scripts rc 0; Family A and Family B leaves equal the pinned JSON (0 differ); 88 passed.
- In every mutant row, "leaves ≠ pinned" includes 1 leaf for the changed `code_sha256` of the mutated file.

| Mutant | Suite after rerun | Family A leaves ≠ pinned (max \|Δ\|) | Family B leaves ≠ pinned (max \|Δ\|) | Verdicts / D3 |
|---|---|---|---|---|
| A06 A2 first 25 rows | **survived** (88 passed) | 79 (6.23) | 1 (hash only) | unchanged |
| A07 ci95 [hi, lo] | **survived** | 1 | 41 (0.032; the CI ends swapped) | unchanged |
| A08 primary = first key | survived (equivalent in context) | 1 | 1 | unchanged |
| A09 m 28→27 | survived | 34 (0.32) | 44 (0.16) | unchanged |
| A10 S 2000→200 | survived | 70 (0.21) | 44 (0.11) | unchanged |
| A11 bootstrap B 999 | survived | 2 | 42 (0.001) | unchanged |
| A12 seed | survived | 145 (0.11) | 76 (0.093) | unchanged |
| A13 m 12→13 | survived | 38 (0.57) | 2 | unchanged |
| A14 D2 < 0.05 | survived (no real effect; every p_low = 0.001) | 1 | 1 | unchanged |
| A21 A1b orientation | survived | 1 | 17 (15.3) | unchanged |
| R01 bootstrap level 0.99 | survived | 1 | 41 (0.006) | unchanged |
| S01 HCP as primary | **killed** (`test_frozen_family_b_verdicts_recomputed…`) | 0 | 5 | **H1a → "not replicated"** |
| S02 seed shift | survived | 0 | 42 (0.006) | unchanged |
| S03 script positions 0..24 | **survived** | 79 (6.23) | 0 | unchanged |
| S04 HCP dropped | **killed** (`test_frozen_family_b_h1b_is_sign_limited…`) | 0 | 146 (0.0005) | unchanged |

Reading of the table:
- Once the scripts are actually re-executed, the shipped regression tests do catch the two script mutants that would change a verdict or the checkpoint set (S01, S04).
- Every other mutant that changes a number still passes the suite after a real rerun.
- A "rerun reproduces the pinned JSON values" check (the control shows it is exact, and it takes about 45 s) would kill all of them except A08 and A14.

**O11. Provenance claims in addendum 04 / the worker handoff**
- `git show 0db0336:<addendum_03>`: sha `725d5077…`, with 1 literal BIDS-prefix token. `ef27b71`: sha `73489661…`, with 0. The working copy has 0 and so does addendum 04.
- I confirm that the root edit was needed for the ID-scan tests: they fail on any occurrence of the BIDS prefix bytes.
- Commits touching addendum 04:
  - `e8c795e` (10:01 KST) holds `1a5ecb77…`;
  - `7430043` (10:16:26 KST, after the worker's handoff) holds the final `a1828b38…`.

  So the worker's "working copy differs from HEAD" is now stale.
- `test_verdict_rules_r2b.py` is still untracked.
- Every commit since `0db0336` that touches a Topic 3 path is either `0db0336` or `ef27b71` (root), or a "docs(iitp): checkpoint four-topics teamwork documents" commit (`e8c795e`, `7430043`). I found none I could not attribute to those sources.
- The worker's attribution of `a18006d` and `bd1f991` to addendum 04 is imprecise: only `e8c795e` and `7430043` touch it.

**O12. Housekeeping**
- I never printed or wrote subject identifiers. The alignment positions stayed in memory, and only counts were printed.
- My logs redact the BIDS prefix at write time.
- GPU use was 0. Nothing was sent to B300, and there was no connectome job.

## 2. Logic Chain

1. O1–O4 show that the pinned outputs come from the frozen code and card, that they reproduce exactly, and that the verdicts follow card §5 from scratch. The claims "numbers correct", "card before results" and "verdict follows card" are therefore CONFIRMED.
2. The W rows of O7 kill every iteration-1 survivor named in challenger_M2_r1_1's invalidation condition ("If a rule-logic test is added and N05/N06/N08–N11 are killed, finding 3 is closed"). The condition is met, and MM06 needs the r2b file.
3. The dispatch also asks whether the decision logic is guarded at all. For that I used the same standard the worker applied to MM06: a mutant counts if it is non-equivalent, reachable at the card's resolution, and able to change a decision.
   - A07 meets it (O8, O9 witness).
   - A08 meets it in principle. It is equivalent only while every caller puts the primary first.
   - A06/S03 change the real D3 inputs by about 36% at the NeuroSTORM−BrainLM point (3.36 → 4.57; O9) without any test failing. They are verdict inputs, and the verdict stays the same.
   - So the decision layer is guarded at the rule (`replication_verdict` on hand-built records) but not at the producers that build its inputs (`paired_log_contrast`, the A2 subset) or at the wiring (`primary_label`, the script calls). The uncovered paths are the ones the real verdict goes through. Iteration 1's N06 gap reappears one function upstream, so finding (ii), read as "verdict logic guarded by tests", is only partly closed. Hence R-1.
4. The equivalent and measure-zero survivors (O7) are not findings, and I do not count them.
   - The parameter survivors mean that card §4's parameter list is tied to the code only by a hash. That is acceptable for the shipped run, which O2 verifies, but it gives no regression protection.
   - The script survivors are guarded by the output and code pins and partly by the regression test after a rerun (O10).
5. O6 refutes the "383 (D-limited)" text for H4 at L0, which R-2 describes. The reading drawn from it stands, because all the observed values sit far below every ceiling. So R-2 is a non-blocking erratum.
6. Severity.
   - No finding changes a number, a frozen rule outcome or a real verdict.
   - Within R-1, A07 is a test-coverage gap of exactly the kind that blocked iteration 1 (N06), and it is cheap to close. A06/S03 (MEDIUM) and A08 (LOW) are the same class without a decision effect.
   - R-2 is text only.
   - Hence REFUTED (scoped), with A07 blocking and A06/S03, A08 and R-2 non-blocking.

## 3. Caveats

- I did not rerun the old 86-test suite or `tests/topic1_lagmotif`. Other verifiers were loading the host (load 25–50), and M1 is another team's milestone. I reran C1 and the topic3 suite in copies.
- The connectome token job was not rerun. Family B was rerun from the saved spectra npz.
- I did not directly re-measure time invariance at L2; challenger_M2_r1_1 probed L3 on connectome. The "8 near-static cells" reading at L2 rests on the rank-7 evidence (O5) plus that probe.
- "Blocking" is my recommendation. The worker's 67/67 claim was correctly scoped to the assigned set, and addendum 04 §7 discloses the unrun boundary siblings. A01/A03–A05 are those siblings, and I classify them as measure-zero, not as findings.
- A08 is equivalent under the current callers. I list it with A07 because the same additive test file closes it, not because it can change a result today.
- I ran my mutant set once. The controls passed at start and end, and the witness tests re-confirm the A06/A07/A08 kills deterministically.
- DISPATCH.md reproduces the dispatch verbatim except the worker's embedded structured-handoff JSON. I summarised that part in brackets, because the identical full text is in `worker_M2_r2b/handoff.md`. This is a deviation from "this prompt verbatim".

## 4. Conclusion

**REFUTED (scoped).**

Confirmed:
- T3.1, T3.2 and T3.4 (numbers and verdicts);
- iteration-1 finding (i), the Family B ceiling 7, for items 1 and 2 except the H4 L0 ceiling;
- iteration-1 finding (ii) as defined by its invalidation condition.

Refuted:
- **R-1:** "the verdict logic is guarded by tests". Producer and wiring mutants survive the shipped 88-test suite: A07 (reachable decision flip, blocking), A06/S03 (MEDIUM) and A08 (LOW).
- **R-2:** addendum 03 §2's H4 ceiling text.

**Recommended additive fixes** (no frozen file needs editing):
- (a) A new test file, in the spirit of `V/witness/test_witness_c2.py`:
  - the `paired_log_contrast` CI order, plus an end-to-end case where p < 0.05 but the CI covers 0, giving "killed";
  - a `replication_verdict` call where the primary is not the first key;
  - an A2 subset spy that checks the NeuroSTORM positions are used.
- (b) A test that pins `analysis.PARAMS` to the card §4 values.
- (c) Optionally, a regression test that reruns both stats scripts in a temp copy (about 45 s) and compares the JSON values with the pinned outputs. It would kill every rerunnable producer, parameter and script mutant in O10 that changes a number.
- (d) An addendum-05 erratum:
  - H4 at L0 is n-limited at ≤ 159 (about 138 distinct cells if the cells are near-static), not "383 (D-limited)";
  - report §5 "±0.003" should read "0.002–0.014".

Then record the new test hashes in an addendum, as before.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # rc 0, 67 OK
for f in output_sha256.txt addendum_02_sha256.txt addendum_03_sha256.txt addendum_04_sha256.txt; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/$f; done
git show 24fe976:docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md | sha256sum  # 683374565d80...
V=verification/challenger_M2_r2b_2; P=/home/juke/superclaude-env/bin/python3
bash $V/make_tree.sh                                       # rebuilds $V/tree_base, manifest == production
PYTHONDONTWRITEBYTECODE=1 $P -B -I $V/probe_freeze_order.py # timeline + code binding
PYTHONDONTWRITEBYTECODE=1 $P -B -I $V/probe_numbers.py      # Family B recompute, addendum numbers, H4 ceiling
PYTHONDONTWRITEBYTECODE=1 $P -B -I $V/probe_survivor_impact.py   # A06 real impact, S01, A07 witness
PYTHONDONTWRITEBYTECODE=1 $P -B -I $V/probe_t31.py          # T3.1
PYTHONDONTWRITEBYTECODE=1 $P -B $V/run_witness.py           # needs no logs/witness_summary.json; shipped 3 passed; A06/A07/A08 each 1 failed
PYTHONDONTWRITEBYTECODE=1 $P -B $V/run_mutants_c2.py <new_logdir> 4      # survivors as in O7; W_* all killed
PYTHONDONTWRITEBYTECODE=1 $P -B $V/run_rerun_mutants.py <new_logdir> 4   # O10
```

**Invalidation conditions.**
- R-1 is withdrawn if a shipped test fails under A07 (patch `"ci95": [lo, hi]` → `"ci95": [hi, lo]` in `analysis.py`), under A08, and under A06.
- The end-state check `sha256sum -c verification/challenger_M2_r2b_2/tree_base.manifest_sha256.txt`, run from the project root, gave rc 0. All 95 Topic 3 production files are unchanged since 01:28Z.
- R-2 is withdrawn if H4 at L0 is shown to use more than 160 rows per frame.
