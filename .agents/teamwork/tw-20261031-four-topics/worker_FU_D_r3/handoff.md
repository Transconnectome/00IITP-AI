# Handoff — worker_FU_D_r3 (FU_D iteration 3, final) — Hard handoff

## 1. Observation
- The FU-D r2 gate failed because `challenger_FU_D_r2_2` returned `REFUTED` on two blocking items while the other four verifiers passed (`reviewer_FU_D_r2_1` APPROVE, `reviewer_FU_D_r2_2` APPROVE, `challenger_FU_D_r2_1` CONFIRMED, `auditor_FU_D_r2_1` CLEAN):
  - **B1 (`C12` / `CV09` and siblings):** In `src/topic2_fu_d/verdict.py::_stage1_category`, line 96 (`if c2 != cat:`) mutated to `if c2 != cat and c2 != "inconclusive":` survived the 195-test suite because card §8 step 7 was tested only in the `inconclusive -> stop` direction. At the script level (`scripts/topic2fu_d_verdict.py:90`), stall detection was tested only in arm `S` at a single seed (`CP01`, `CP02`).
  - **B2 (alias run directories):** `design.DIR_RE` (`\d+` and `$`) with `int()` maps non-canonical directory names (`Fplus_C_s00`, `Fplus_C_s000`, Arabic-Indic/full-width digits, trailing newline) to planned keys, and `records.load_runs` lets the later-sorted alias overwrite the canonical record even under `strict=True`. This frozen-code departure from card §8 was missing from `addendum_01` errata.
- All 29 frozen FU-D code/test files (`code_sha256_at_freeze.txt`), the frozen card (`card_sha256.txt`), the shipped outputs (`output_sha256.txt`, `verdict.json` sha256 `f6b295d9…59fc`), and `addendum_01` (`addendum_01_sha256.txt`) remain 100 % untouched.
- Added three additive test files (194 new tests total; `tests/topic2_fu_d` grows from 195 passed to 389 passed):
  - `tests/topic2_fu_d/test_fud_r3_guards.py` (174 tests): 28 reachable `(stalled_seeds, all_seed_cat, dropped_seed_cat)` fixtures across 1 and 2 stalled seeds verified by an independent `scipy.stats.t.ppf(0.975, df)` oracle at `_stage1_category` and `decide`, an exhaustive 16-pair step-7 decision table, a direct `C12` witness, per-arm (`E`, `C`, `S`) and multi-seed script stall tests, gate-isolation and missing-`runs/` guards, `HP_FIELDS` / NaN-term / token / `post_checks_ok` / `perm_key` guards, F− protocol-flag and would-be-`keep` rules, secondary bootstrap (`B = 10,000`, `seed = 0`, `num/den` order, `--n-boot`, per-subject seed-mean axis, `val_curves`) and stdout JSON summary checks, all 17 `decide()` reason branches, explicit `delta` forwarding, capacity-floor short-circuiting, and shipped-data invariants for E5, E2′, E6, E7, and E8.
  - `tests/topic2_fu_d/test_fud_r3_oracle.py` (2 tests): clean-room card-§8 step 1–8 oracle compared against `V.decide()` across 3,000 seeded scenarios covering all 5 verdicts, all 4 primary categories, floor, stall flips, and F− states.
  - `tests/topic2_fu_d/test_fud_r3_full_output.py` (18 tests): whole-`verdict.json` and stdout-summary deep equality against independently computed expectations across 17 synthetic script scenarios plus a discriminating self-test.
- Union mutation (`verification/worker_FU_D_r3/mutation/union_r3.out.json`):
  - `raw = 2051` (1,518 collected from all 11 r1/r2/r3 lists + 533 AST-located mutants in `sweep_r3.json`); `not_applied = 1` (`rev2_1:R42`, which targeted the wrong file for `needs_fminus`, covered in `verdict.py` by `rev2_1:R43` and `exp3_3:W107`); `distinct = 1675`.
  - Baseline control (`CTRL`): `SURVIVED` (`383 passed, 1 deselected` in Leg A; `189 passed, 1 deselected` in Leg B; `shipped_changed = False`).
  - `killed = 1511`, `survived = 164`, `invalid = 0` (`[]`).
  - `shipped_changing = 515` (all 515 killed in Leg A); **`survivors_changing_shipped_output = 0` (`[]`)**.
  - `killed_only_by_r3_files = 34` distinct listed mutants (91 raw aliases), including `cha2_1:CV09`/`cha2_2:C12`, `cha2_1:CP01`, `cha2_1:CP02`, all non-equivalent r2 verifier survivors (`R31`/`S11`, `R34`/`CP03`/`S07`, `R35`, `CV15`, `CV19`, `CR01`/`R04`, `CR13`/`R07`, `CP04`/`S08`, `CP05`, `CP07`/`S05`, `CP11`/`S09`, `CP12`, `CP14`, `C23`), and all r3 explorer targeted mutants (`E7a`–`E7f`, `E7i`, `W1`, `W2`, `N01`, `N04`–`N09`, `N12`, `N14`, `N18`, `N19`, `T01`–`T24`). In addition, all 50 non-equivalent `exp3_3:W*` sweep survivors from `explorer_FU_D_r3_3` O5 are killed in Leg A.
  - All 164 surviving distinct mutants are partitioned into 10 exact classes in `addendum_02.md` §5 (61 Boolean `==` implies `!=` tautologies, 41 disjoint-domain `!=` conjuncts, 9 `needs_fminus` equivalences, 9 unread non-completed `stage1` dict fields, 6 token-order checks subsumed by `validate_completed`, 3 unreachable second-completed-attempt checks, 6 Stage-1 arm-length subsets subsumed by `contrasts`, 14 dead/unreachable/commutative/pinned-constant identities, 7 `argparse` default/help equivalences, and 8 internal exception message strings or stdout `json.dumps` indentation changes).

## 2. Logic Chain
1. Neither B1 nor B2 affects the shipped FU-D verdict (`inconclusive`, F+ gate gains 0.363 % and 0.655 % < δ = 1 %; Stage 1 not run), which every r1 and r2 verifier reproduced. Therefore 0 GPU-h and no code edits to frozen files are warranted.
2. B1 is closed at class level rather than by a single witness: `test_fud_r3_guards.py` pins all 28 reachable `(stalled_seeds, cat_all, cat_wo)` fixtures against an independent `scipy` t-interval oracle, proves in `addendum_02` §4 (P1) why `stop -> keep` and `stop -> modify` are algebraically unreachable for `n = 5` with 1–2 seeds dropped, tests all 16 pairs via a `primary_category` decision table, tests stall detection in each arm (`E`, `C`, `S`) and multi-seed combinations at script level, and adds the 3,000-scenario oracle (`test_fud_r3_oracle.py`) and 17-scenario full-output regression suite (`test_fud_r3_full_output.py`).
3. B2 and the additional frozen-code departures (`E5` alias run dirs including trailing newline, `E2′` non-finite/negative/zero error terms, `E6` unchecked `seed_plan.json` `seeds` list, `E7` F− flag vs stop, `E8` unchecked sidecar `fud_code_sha256`, `E9` minor type/symlink/prefix checks, `W4` floor suppressing `stall_sensitivity`, `W5` cost-guard reason wording) cannot be fixed by editing receipt-pinned code or by writing failing tests. They are reproduced in `verification/worker_FU_D_r3/probes/errata_probe.py` (`errata_probe.out.json`), disclosed with explicit reading rules and a future-card reuse condition in `addendum_02.md` §3, and paired with shipped-data invariant tests proving the shipped data lie strictly outside every departure.
4. Addendum 01 §4's unscoped statement ("0 non-equivalent survivors remain") is explicitly corrected in `addendum_02.md` §2 without modifying the receipt-pinned `addendum_01.md`.

## 3. Caveats
- Leg B (suite without the 3 new `test_fud_r3_*.py` files) was run only for listed (non-sweep) mutants killed in Leg A (`m["listed"] == True`), not for automatic sweep mutants (`wr2:S*`, `exp3_3:W*`, `r3:*`).
- `rev2_1:R42` is recorded in `not_applied` because `reviewer_FU_D_r2_1` specified `scripts/topic2fu_d_verdict.py` for a line in `src/topic2_fu_d/verdict.py::needs_fminus`; the intended `verdict.py` mutation is included and evaluated as `rev2_1:R43` and `exp3_3:W107`.
- `test_e192_model.py` (CPU E192 model build) and the r2 receipt belt test are excluded from the mutation runner by design; both pass in the full 389-test `tests/topic2_fu_d` run.
- Eight surviving `exp3_3:W*` / `r3:*` mutants alter only internal `ValueError` / `AssertionError` / `SystemExit` message text or stdout `json.dumps` indentation (`indent=1` vs `None`/`2`); they are listed explicitly in row 10 of the `addendum_02.md` §5 table rather than called strictly equivalent.

## 4. Conclusion
FU_D iteration 3 is complete at 0 GPU-h with all frozen artifacts untouched:
- Verdict unchanged: **`inconclusive` (measurement capacity at E192)**; F+ gate gains (E−C)/E = 0.363 % and (S−C)/S = 0.655 %, both < δ = 1 %; Stage 1 not run; the r1 E36 `stop` stands alone.
- Additive test suite (`tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py`, 194 new tests, 389 total in `tests/topic2_fu_d`), `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md`, and `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt` (102 pinned files) are in place and verified.
- Ready for the final 5-verifier gate.

## 5. Verification Method
```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt addendum_01_sha256.txt addendum_02_sha256.txt; do
  grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'
done
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool tests/topic1_lagmotif -q
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_d_c4scan.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/worker_FU_D_r3/c4_scan_r3.py /tmp/c4_r3_check.json
```
Invalidation: any edit to a frozen or prior-receipt-pinned FU-D file, any change to `verdict.json`, any C1/receipt/C4 failure, or any non-equivalent verdict-path mutant that survives the 389-test suite.
