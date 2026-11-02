# Handoff — challenger_FU_D_r3_2 (FU_D iteration-3 gate). Type: Hard. Verdict: CONFIRMED

Both blocking items raised by `challenger_FU_D_r2_2` in iteration 2 (**B1** `C12` step-7 stall-sensitivity mutant and **B2** alias run directory overwrite) — together with every non-equivalent survivor from all five r2 verifiers and all three r3 explorers — are completely closed in Milestone FU_D Iteration 3 (`worker_FU_D_r3`). All frozen FU-D code, card, result report, `verdict.json` (`f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`), and prior receipts are untouched. The shipped verdict **`inconclusive` (measurement capacity at E192)** (`gain_C_vs_E = 0.363 %`, `gain_C_vs_S = 0.655 %`, both `< δ = 1 %`) reproduces byte-for-byte.

## 1. Observation

**Integrity & Receipts (verified before and after all probes):**
- **C1 protected hashes:** `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` → `rc = 0`, `67/67 OK`.
- **FU-D receipts (`results/topic2/2026-11-02_fu_d/`):**
  - `card_sha256.txt`: `1/1 OK` (`1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b`)
  - `code_sha256_at_freeze.txt`: `29/29 OK`
  - `output_sha256.txt`: `34/34 OK` (`verdict.json` sha256 `f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`)
  - `addendum_01_sha256.txt`: `23/23 OK`
  - `addendum_02_sha256.txt`: `102/102 OK`
- **Topic 2 r1 receipts (`results/topic2/2026-11-01/`):** `code_sha256_at_freeze.txt` `33/33 OK`, `output_sha256_r2.txt` `156/156 OK`, `addendum_06_sha256.txt` `31/31 OK`.

**Test Suites (executed sequentially, 1 pytest process at a time, CPU only):**
- `tests/topic2_fu_d`: `389 passed, 2 warnings in 80.88s` (129 freeze + 66 r2 + 194 new r3 tests across `test_fud_r3_guards.py` [174], `test_fud_r3_oracle.py` [2], and `test_fud_r3_full_output.py` [18]).
- `tests/topic2_rgpool tests/topic1_lagmotif`: `204 passed, 24 warnings in 89.23s` (116 + 88).
- Old suite (`STRICT_E2E=1`, `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): `86 passed, 7 warnings in 32.40s`.

**Independent Probe Results (`verification/challenger_FU_D_r3_2/probe_r3_challenge_v2.py` → `probe_r3_challenge_v2.out.json`):**
1. **Headline Recomputation & Shipped-Data Invariants (`1_shipped_and_invariants`):**
   - Exact `Fraction` sums from `runs/Fplus_{E,C,S}_s0/run.json` (`test_num`/`test_den`, 16 terms each):
     - `E = 0.6558494816918741`, `C = 0.653467876277415`, `S = 0.6577736746995909` (abs diff `<= 1e-16` vs recorded `test_nmse`).
     - `gain_C_vs_E = 0.003631329262188746` (`0.363 % < 1 %`), `gain_C_vs_S = 0.00654601816368273` (`0.655 % < 1 %`), `gate_pass = False`.
   - Regenerating `verdict.json` via `scripts/topic2fu_d_verdict.py` into a temporary file yields `sha256 = f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc` (`byte_identical = True`).
   - Shipped-data invariants for E5, E2′, E6, E7, E8, E9 all hold: `runs/` contains only the 3 real ASCII directories `["Fplus_C_s0", "Fplus_E_s0", "Fplus_S_s0"]` (no symlinks, no plain files, exact `run_name(*parse_dir(nm)) == nm`, `used_dir == nm`); `type(rec["seed"]) is int`; all 16 `test_num >= 0` and finite; all 16 `test_den > 0` and finite; `0 < test_nmse < 1`; all 3 `fud_meta.json` files have `post_checks_ok is True`, `wrapper_sha256` matching `code_sha256_at_freeze.txt`, and `fud_code_sha256` matching all 8 `src/topic2_fu_d/*.py` freeze hashes; no `seed_plan.json`, `Fminus_*`, or `hcp_*` exists.
2. **Algebraic Proof P1 (`2_algebraic_proof_P1`, `addendum_02.md` §4):**
   - Verified the exact between-group variance identity $(n-1)s_n^2 = \sum_{i\in K}(x_i - \bar x_k)^2 + \sum_{j\in D}(x_j - \bar x_{\text{drop}})^2 + \frac{k(n-k)}{n}d^2$ across 4,000 random vectors (`max_variance_decomposition_error = 2.17e-18`).
   - For $n = 5, k = 4$: $t_{0.975, 4}\sqrt{4/(25\cdot 4)} = 0.55528902 > 1/5 = 0.20$ (`net_d_multiplier = +0.35528902 > 0`).
   - For $n = 5, k = 3$: $t_{0.975, 4}\sqrt{6/(25\cdot 4)} = 0.68008738 > 2/5 = 0.40$ (`net_d_multiplier = +0.28008738 > 0`).
   - When $d = \bar x_k - \bar x_{\text{drop}} > 0$, $\text{hi}_n \ge \bar x_k + (\text{net\_d\_multiplier})\cdot d > \bar x_k \ge \delta$; when $d \le 0$, $\bar x_n = \bar x_k - \frac{n-k}{n}d \ge \bar x_k \ge \delta$ and $s_n \ge 0$, so $\text{hi}_n \ge \bar x_n \ge \delta$ as well.
   - Multi-start Nelder-Mead adversarial optimization (80 random starts per $k$) and Monte Carlo draws (`46,932` valid `keep`/`modify` subsets for $k=4$; `42,750` for $k=3$) found `min_observed_hi_n_given_kept_survives = 0.01001255` ($k=4$) and `0.01000905` ($k=3$), both strictly `>= δ = 0.01`.
   - All 28 reachable fixtures in `test_fud_r3_guards.py::STALL_MATRIX` were verified against the independent `scipy.stats.t.ppf(0.975, df)` oracle.
3. **Errata E5, E2′, E6, E7, E8, E9, W4, W5 (`3_errata_and_departures`):**
   - Independently executed `verification/worker_FU_D_r3/probes/errata_probe.py` into a temporary file: output matched `errata_probe.out.json` identically.
   - Confirmed an additional Unicode alias (`Fplus_C_s०` with Devanagari zero `'०'`) parses to `(('Fplus', 'C', 0), 0)` and is caught by the E5 round-trip reading rule (`run_name(*parse_dir(name)) == name`).
   - Confirmed `rec["seed"] = 0.0` (float) is accepted as `0` by `validate_completed`, covered by E9's integer-seed reading rule.
4. **Closure of B1/r2 Survivors & Spot-Check of All 164 Surviving Mutants (`4_union_and_164_survivors` + `verify_r2_survivors_killed.py`):**
   - Audited `union_r3.out.json`: `raw = 2051`, `distinct = 1675`, `not_applied = ["rev2_1:R42"]`, `killed = 1511`, `survived = 164`, `invalid = []`, `shipped_changing = 515` (all 515 killed), `survivors_changing_shipped_output = []`.
   - Verified all 124 listed non-equivalent mutants from r2 verifiers and r3 explorers (`cha2_2:C12`, `C23`, `R04`, `R07`, `S05`, `S07`, `S08`, `S09`, `S11`; `cha2_1:CV09`, `CP01`–`CP05`, `CP07`, `CP11`, `CP12`, `CP14`, `CR01`, `CR13`, `CV15`, `CV19`; `rev2_1:R31`, `R34`; `rev2_2:R35`; `exp3_1:own:E7a`–`E7f`, `E7i`, `W1`, `W2`; `exp3_2:own:N01`, `N04`–`N09`, `N12`, `N14`, `N18`, `N19`; `exp3_3:T01`–`T30`; and all 50 `exp3_3:W*` O5 sweep survivors) are `KILLED` in `union_r3.out.json`.
   - In `verify_r2_survivors_killed.py` (`verify_r2_survivors_killed.out.json`), we did not run `verification/challenger_FU_D_r2_2/mut/run_mut.py` directly because lines 55–60 of that script write to `challenger_FU_D_r2_2/mut/{mut.log,mut.out.json}`. Instead, we ran an isolated copy in `/tmp` (1 pytest process at a time) against `test_fud_r3_guards.py`: `CONTROL` survived (`174 passed in 9.14s`) and **all 9 `challenger_FU_D_r2_2` survivors (`C12`, `C23`, `R04`, `R07`, `S05`, `S07`, `S08`, `S09`, `S11`) were KILLED (`rc = 1`)**.
   - Verified that the 10-class table in `addendum_02.md` §5 (`61 + 41 + 9 + 9 + 6 + 3 + 6 + 14 + 7 + 8 = 164`) is an exact partition of `summary["survived"]` with 0 missing and 0 extra UIDs.
   - Dynamically executed all 164 surviving distinct mutants:
     - All 55 surviving `src/topic2_fu_d/verdict.py` mutants produced identical `decide()` outputs on all 3,000 scenarios of `test_fud_r3_oracle.py` and identical `needs_fminus()` outputs on all completed Stage-1 scenarios.
     - All 38 surviving `src/topic2_fu_d/records.py` mutants produced identical `load_expectations()` and strict `load_runs()` results on the shipped gate records.
     - All 71 surviving `scripts/topic2fu_d_verdict.py` mutants were executed via subprocess on a synthetic 5-seed Stage-1 results directory (and verified on shipped runs): 71/71 exited `rc = 0` and produced 100 % identical `verdict.json` dicts and parsed stdout JSON dicts (the 2 stdout-indent mutants `exp3_3:W621` and `exp3_3:W702` change only whitespace formatting in stdout).

## 2. Logic Chain
1. Because C1 (67/67), all 5 FU-D receipts, and the 3 Topic 2 r1 receipts pass with 0 mismatches, Iteration 3 is strictly additive and preserves all frozen artifacts and the shipped `verdict.json` (`f6b295d9…59fc`).
2. **B1 (`C12` and step-7 / stall-wiring class) is completely closed:** `test_fud_r3_guards.py` pins all 28 reachable `(stalled_seeds, cat_all, cat_wo)` fixtures against an independent `scipy` t-quantile oracle, proves P1 for the 4 unreachable `stop -> keep/modify` pairs (verified algebraically and numerically in our probe), exercises all 16 pairs via a decision table, tests per-arm (`E`, `C`, `S`) and multi-seed script stall detection, and adds the 3,000-scenario oracle (`test_fud_r3_oracle.py`) and 18 full-output tests (`test_fud_r3_full_output.py`). Both `union_r3.out.json` and our direct run in `verify_r2_survivors_killed.py` confirm `C12` and all 8 other `challenger_FU_D_r2_2` survivors are killed.
3. **B2 (alias run directories) and all other frozen-code departures are completely closed:** `addendum_02.md` §3 discloses `E5` (zero-padded, Unicode digits, trailing newline on both gate and Stage-1 paths under `strict=True`, with the exact round-trip reading rule `run_name(*parse_dir(name)) == name`), `E2′`, `E6`, `E7`, `E8`, `E9`, `W4`, `W5`, and the future-card reuse condition; `addendum_02.md` §2 explicitly corrects `addendum_01.md` §4's unscoped survivor claim; and `test_fud_r3_guards.py` pins the shipped data outside every departure.
4. Our dynamic execution and 10-class audit of all 164 surviving mutants in `union_r3.out.json` confirm that 0 survivors can alter any valid decision category or the shipped `verdict.json`.

## 3. Caveats
- 0 GPU-h used (no B300 or connectome jobs launched).
- In accordance with the `claude-code.md` evidence preservation rule, the initial version of our probe (`verification/challenger_FU_D_r3_2/probe_r3_challenge.py`, which passed synthetic `EXP["wrapper_sha256"] = "w"*64` instead of the real freeze `WRAPPER_SHA` when calling `load_runs` on the shipped `runs/` at line 513) and its verbatim traceback are preserved untouched in `verification/challenger_FU_D_r3_2/v1_preserved_log.txt`, and the repaired probe was written to `verification/challenger_FU_D_r3_2/probe_r3_challenge_v2.py`.

## 4. Conclusion
**CONFIRMED.** Milestone FU_D Iteration 3 completely closes B1, B2, and all r2 verifier / r3 explorer items with 0 blocking issues and 0 regressions.

## 5. Verification Method
```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt addendum_01_sha256.txt addendum_02_sha256.txt; do
  grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'
done
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r3_2/probe_r3_challenge_v2.py /tmp/chal_r3_2_probe.json
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r3_2/verify_r2_survivors_killed.py /tmp/chal_r3_2_r2mut.json
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
```
Invalidation conditions: any failure of C1 or the 5 FU-D receipts, any modification to `verdict.json`, or any non-equivalent verdict-path mutant surviving the 389-test `tests/topic2_fu_d` suite.
