# Handoff — explorer_FU_D_r3_2 (FU_D iteration 3; explorer 2 of 3; lens: feasibility and failure modes). Type: Hard

**Summary.** The r2 gate failed on two items: B1 (a test-coverage gap in card §8 step 7) and B2 (a frozen-loader departure from the card that the errata do not list). Neither touches the shipped verdict, which stays `inconclusive` (F+ gains 0.363 % / 0.655 % < δ 1 %). Both can be closed without editing anything frozen: add tests, write addendum_02 errata and a new receipt, using 0 GPU-h. The probes behind this:
- My proposed files kill 24 of the 30 mutants that r2 verifiers reported as survivors. The other 6 were already classed as equivalent.
- They also kill all 20 mutants I designed myself. The shipped suite misses 11 of those 20.
- Shipped verdict outputs are unchanged under every mutant.

## 1. Observation

**Integrity** (22:20Z and again at the end, 2026-11-01):
- C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0.
- FU-D receipts: card 1/1, code_sha256_at_freeze 29/29, output 34/34, addendum_01 23/23.
- `verdict.json` sha256 starts f6b295d9 (unchanged).
- No repo file outside my two directories was written. No git command was run, 0 GPU-h were used and B300 was not touched.
- Count-only C4 scan of my 18 files with the frozen `scripts/topic2fu_d_c4scan.py` detector: 0 token hits, 0 BIDS hits.

**B1 code reality**
- `src/topic2_fu_d/verdict.py:96` reads `if c2 != cat:`. Here `cat` is the step-5 category with all seeds and `c2` is the category without the stalled seeds.
- Existing step-7 tests:
  - `tests/topic2_fu_d/test_verdict.py:134-141` covers only all-seed `inconclusive` → dropped `stop`.
  - `:144-151` covers the unchanged case and n_left = 1.
  - `test_fud_r2_guards.py:516-536` covers exactly 2 seeds left and no stall.
- No test covers any pair whose dropped category is `inconclusive`. That gap is why C12/CV09 survive.

**Probe `probes/stall_matrix_search.py`** (seeded grid search):
- It uses an independent card-§8 oracle with literal t quantiles.
- Space: n = 5, stalled {4} and {3,4}, giving 32 ordered (all, dropped) pairs.
- 26 pairs were realised on the 0.1 % grid. `probes/stall_matrix_unrealised.py` (continuous search, 3·10⁶ draws) adds keep→stop and modify→stop for stalled {4}.
- The frozen `_stage1_category` equals the oracle on all 28 fixtures.
- 4 pairs were never realised: stop→keep and stop→modify, for both stall patterns.

**Script wiring**
- `scripts/topic2fu_d_verdict.py:90` reads `for arm in "ECS"`.
- The only script stall test (`test_verdict_script.py:121-134`) stalls arm S at one seed. So CP01/CP02 (`"S"`, `"CS"`) and my N09 (`"ES"`) survive, and so does N14 (`stalled_seeds=stalled[:1]`).

**Probe `probes/alias_variants.py`** (synthetic records; frozen loader with `strict=True`, over the gate keys and over all keys):
- These names all parse to ('Fplus','C',0), attempt 0, and are ACCEPTED with `used_dir` = the alias, overriding the canonical gate-failing record:
  - `Fplus_C_s00`
  - `Fplus_C_s000`
  - Arabic-Indic digit zero
  - full-width digit zero
  - **`"Fplus_C_s0\n"` (trailing newline)**
- The trailing-newline case is new; challenger_FU_D_r2_2 did not list it. `design.DIR_RE` ends in `$`, and Python's `$` also matches before a final `\n`.
- An alias of `_a1` raises "rerun of a completed run".
- None of these names round-trips: `run_name(*parse_dir(name)) != name`.

**Mutation probe** (`mutation/run.py`, adapted from the worker_FU_D_r2 approach; copied trees, never symlinked; at most 2 pytest at a time; timeout 900):
- Run 1 was INVALID. A relative work path broke the shipped-output step and the control aborted. Its log and output are preserved in `invalid_run1/`.
- Run 2 control: 314 passed with both proposed files and 189 with the shipped suite (minus the E192 build test and the r2 belt test). Shipped output unchanged.
- Run 2 covered 50 mutants:
  - the 30 survivors reported by r2 verifiers: reviewer_1 R31/R34/R36/R40/R43; reviewer_2 R35; challenger_1 the 14 CP/CV/CR mutants; challenger_2 C12/C23/R04/R07/S05/S07/S08/S09/S11; auditor P19;
  - 20 of my own: N01–N20.
- Run 2 results:
  - With the proposed files, 7 survive: R36, R40, R43, CR01, R04, P19, N14.
  - The shipped suite alone lets 41 of the 50 survive. 0 invalid, 0 not applied, 0 shipped outputs changed.
- I added a two-seed script stall test. Run 3 then killed N14 (control 315 passed).
- Run 4 measured what the oracle file adds on its own, against the 41 mutants the shipped suite misses.
  - With only `proposed_test_fud_r3_oracle.py` added, it kills 9: CV09, C12, N01, N04, N05, N06, N08, N18, N19. These are every category-changing mutant of `verdict.py` in the set.
  - It does not kill the script-wiring, string, record or secondary mutants. The targeted file is needed for those.

**Oracle prototype** (`proposed_test_fud_r3_oracle.py`):
- 3000 seeded scenarios, 0.06 s.
- 0 disagreements between `decide()` and the card-§8 oracle.
- All 5 verdicts are reached, including 21 step-7 flips.

**Compute.** The FU-D ledger total stays at 3.672 of the 25 GPU-h cap. This iteration needs 0 GPU-h.

## 2. Logic Chain

1. B1 is a coverage gap of the same "flip if code changed" class as X45/X22 (r1) and V01–V11 (M3). Step 7 is a pre-registered rule; card §8 makes every ordered pair (a ≠ b) map to inconclusive. A guard that tests one direction cannot see a mutant that exempts other pairs, as C12/CV09/N01/N04/N05/N06 do.
   → Fix: test every realisable pair, at function level and through `decide`.
2. The 4 unrealised pairs (stop → keep/modify) are mathematically unreachable, not a search failure.
   - Card step 5 says stop means hi_n(I1) < δ, so in particular mean_n < δ.
   - The kept seeds would need mean_k ≥ δ. Then the dropped seeds have mean < δ.
   - The sample variance over n seeds is at least the between-group part, k(n−k)/(n(n−1))·(mean_k − mean_drop)².
   - That gives hi_n ≥ mean_k − (n−k)/n·d + t·sd/√n with d = mean_k − mean_drop. For n = 5, k = 4 the t term (2.776/5·d) is larger than the mean shift (d/5), so hi_n > mean_k ≥ δ. The same holds for k = 3. This contradicts stop.
   → A mutant that exempts only those pairs is equivalent; the addendum should carry this proof.
3. The step-7 stall input comes from `scripts/…:90` over all three arms and all stalled seeds. A test that stalls only arm S at one seed cannot detect restriction to "S", "CS" or "ES", or truncation of the stalled list.
   → Fix: one script test per arm, plus one two-seed, two-arm test.
4. B2: card §8 makes duplicate records a protocol error, but the frozen `DIR_RE` + `int()` + dict overwrite lets a non-canonical name silently replace the canonical record. The trailing-newline variant shows that E5 cannot be worded as "zero-padded digits". The general rule is that every run directory name must round-trip exactly through `run_name(parse_dir(name))`.
   The frozen code cannot be changed without a new card. A test asserting rejection would fail on frozen code, and skip/xfail is not allowed.
   → Fix: erratum E5 with that rule, plus a shipped-data test showing that every shipped name round-trips, is ASCII, and is the `used_dir`.
5. The remaining r2 nonblocking survivors are cheap to kill, and a new r3 challenger would raise them first. They are R31/S11, R34/S07/S08/CP03/CP04/CP05/CP11/S09, R07/CR13, S05/CP07/CP14, CP12, R35, CV15, C23/CV19. Run 2 shows each one killed by a targeted test.
6. Iterations r1 and r2 each closed only the listed mutants, and each new challenger then designed fresh mutants nearby. Run 4 shows that an independent oracle over generated scenarios kills every category-changing `verdict.py` mutant tried, whichever line it touches. It costs nothing to run, so it guards the whole class rather than one mutant at a time.

## 3. Caveats

- I did not rerun the worker's 423-mutant union or the full r2 verifier lists (about 227). I ran only their 30 reported survivors plus 20 of my own. Adding tests cannot un-kill a mutant, but the r3 worker must run the full union against the final files.
- I accepted the verifiers' equivalence classes for R36/R40/R43/CR01/R04/P19 after reading the code; I did not prove each one formally:
  - R36 is the Q19 class (token order is already forced).
  - R40 is value-identical on the pinned r1 verdict.
  - R43: the "(keep pending F-)" conjunct forces the keep path.
  - CR01/R04: the exact split-order check subsumes the regex.
  - P19 is value-identical.
- The step-7 fixtures use a fixed E level (0.70); they test category logic, not floor interplay. Floor interplay is covered by the reason table and by `test_capacity_floor_short_circuits_the_stall_check`.
- The oracle uses random floats with a fixed seed. Exact-boundary ties are improbable and do not occur at that seed (0 disagreements). Boundaries are pinned elsewhere by literal tests.
- Further card departures I noticed but did not probe:
  - a record `seed` of `0.0` or `False` compares equal to 0;
  - a symlinked run directory is followed;
  - `s1present` also counts plain files named `hcp_*`.
  All three are minor and unreachable on the shipped data. They are worth one sentence in E5.
- Whether the r3 gate should be scoped like PI decision 6 (named classes closed + no regression + integrity) is a root/PI decision. I only flag the risk that a third open-ended challenger will again find new mutants in Stage-1 code that the shipped verdict never reaches.

## 4. Conclusion

Recommended r3 work, all additive: 0 GPU-h, no edits to the card, src, scripts, the 13 existing tests, the runs, verdict.json, the report or any receipt.
1. **Tests.** Add `tests/topic2_fu_d/test_fud_r3_guards.py` and `tests/topic2_fu_d/test_fud_r3_oracle.py`, adapted from my proposed files.
2. **Addendum.** Write `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md` (the name follows the card's addendum_NN rule) with:
   - E5: aliases, under the round-trip rule, naming all variants including the trailing newline;
   - an E2 broadening to any non-finite term (inf den, P3);
   - E6: negative NMSE accepted (P4);
   - E7: the `seeds` list is not checked against `n_seeds` (P5);
   - the stop→keep/modify infeasibility proof;
   - equivalence proofs, the kill table and the mutation evidence;
   - a file-set statement: freeze 12 + r2 1 + r3 2.
3. **Receipt.** Write `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt`.
4. **Union mutation.** Run the worker r2 lists, all five r2 verifier lists in full, the r3 explorer probes and a class sweep, against the globbed test dir on copied trees. Require 0 non-equivalent survivors.
5. **Checks.** C4, C1, all receipts and all suites.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r3_2/probes/alias_variants.py /tmp/alias.json   # 5 aliases accepted, used_dir = alias
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r3_2/probes/stall_matrix_search.py /tmp/sm.json   # 26 realised; frozen == oracle
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/explorer_FU_D_r3_2/mutation/run.py \
  /home/juke/git/00IITP-AI /tmp/fud_r3_work verification/explorer_FU_D_r3_2/proposed_test_fud_r3_guards.py,verification/explorer_FU_D_r3_2/proposed_test_fud_r3_oracle.py \
  verification/explorer_FU_D_r3_2/mutation/mutants.json /tmp/fud_r3_out.json    # expect A_survived = R36, R40, R43, CR01, R04, P19 only
```

The evidence is pinned in `verification/explorer_FU_D_r3_2/artifact_sha256.txt` (22 files). The proposed guards file has sha256 d6c793aa…34f0 and the proposed oracle file a0551a11…dd4b.

These conclusions no longer hold if:
- a full-union run against the final r3 files leaves a non-equivalent survivor;
- the shipped `verdict.json` changes under any mutant;
- C1 or any receipt fails.
