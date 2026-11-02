# Handoff — `challenger_FU_D_r3_1` (Milestone `FU_D_r3`, Challenger 1 of 2)

- **Run**: `tw-20261031-four-topics` (General route, Workflow C)
- **Role**: `challenger_FU_D_r3_1` (Challenger 1 of 2 for Milestone `FU_D_r3`)
- **Timestamp**: `2026-11-02T05:13:00Z`
- **Verdict**: **`CONFIRMED`** (`0` blocking issues, `3` nonblocking documentation notes, `0` uncovered requirements)
- **GPU-h used**: `0.000` (`CUDA_VISIBLE_DEVICES=""` across all probes and pytest runs)

---

## 1. Observation

We executed an independent empirical challenge of Milestone `FU_D` Iteration 3 (`Topic 2 follow-up D: E192 scale (d2-2-18-2), 140k samples, arms E/C/S, 5 seeds (§7 ≈20 GPU-h at 1.36 h/run; cap 25)`) across four standalone probe scripts under `/home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/` and full regression test suites:

1. **Independent Gate Statistics, Receipts, Algebraic Proof, and Smoke/Ledger Audit (`probe1_gate_and_receipts.py` → `probe1_gate_and_receipts.out.json`)**:
   - **SHA-256 Receipt Verification**: Independently verified all 9 SHA-256 receipt manifests line-by-line from raw file bytes (`0` mismatches, `0` missing files):
     - `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: `67 / 67` passed (C1 intact).
     - `results/topic2/2026-11-02_fu_d/card_sha256.txt`: `1 / 1` passed.
     - `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`: `29 / 29` passed.
     - `results/topic2/2026-11-02_fu_d/output_sha256.txt`: `34 / 34` passed.
     - `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`: `23 / 23` passed.
     - `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt`: `102 / 102` passed.
     - `results/topic2/2026-11-01_r1/code_sha256_at_freeze.txt`: `33 / 33` passed.
     - `results/topic2/2026-11-01_r1/output_sha256_r2.txt`: `156 / 156` passed.
     - `results/topic2/2026-11-01_r1/addendum_06_sha256.txt`: `31 / 31` passed.
   - **Pre-registration Chronology**: Confirmed `card.md` freeze timestamp (`1762003152`) < `code_sha256_at_freeze.txt` (`1762003198`) < `smoke/run.json` (`1762003684`) < `Fplus_E_s0` (`1762007978`) < `Fplus_C_s0` (`1762011722`) < `Fplus_S_s0` (`1762015524`) < `verdict.json` (`1762015551`).
   - **Independent Exact-Rational (`fractions.Fraction`) Gate Recomputation**: Recomputed per-arm `F+` seed-0 test NMSE directly from raw `test_num[i]` and `test_den[i]` arrays in `results/topic2/2026-11-02_fu_d/runs/Fplus_{E,C,S}_s0/run.json` (each having `n_test_subjects = 50`, `steps = 3000`, `wall_sec <= 7200`, `peak_vram_gb <= 22.0`, `train_samples_seen = 140,000 (140k)`, `embed_dim = 192`, `depths = [2, 2, 18, 2]`):
     - `NMSE(E) = 0.6558494816918741` (`abs_diff_vs_run_json = 0.0`)
     - `NMSE(C) = 0.653467876277415` (`abs_diff_vs_run_json = 0.0`)
     - `NMSE(S) = 0.6577736746995909` (`abs_diff_vs_run_json = 0.0`)
     - `gain_C_vs_E = 1 - NMSE(C)/NMSE(E) = 0.0036313292621888414` (`0.363% < 1.00%`)
     - `gain_C_vs_S = 1 - NMSE(C)/NMSE(S) = 0.006546018163682844` (`0.655% < 1.00%`)
     - `pass = (gain_C_vs_E >= 0.01) and (gain_C_vs_S >= 0.01) = False`
     - `verdict = "inconclusive"`, `reason = "measurement-capacity gate failed (F+ fixture at E192); Stage 1 not read"`, `I1_t = null`, `I2_t = null`.
     - Regenerated `verdict.json` via `scripts/topic2fu_d_verdict.py --results results/topic2/2026-11-02_fu_d` into a temporary file: SHA-256 `f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`, byte-identical to shipped `results/topic2/2026-11-02_fu_d/verdict.json` and matching `2026-11-02_topic2_fu_d_result_report.md` and `2026-11-02_topic2_fu_d_addendum_02.md`.
     - Verified that no `runs/hcp_*` or `runs/Fminus_*` directories exist on disk (`stage1_dirs_present = []`, `fminus_dirs_present = []`).
   - **Independent Proof P1 Verification (`addendum_02.md` §4)**: Re-derived the variance inequality $(n-k) s_k^2 \le (n-1) s_n^2 - \frac{k(n-k)}{n} d^2$ for $n=5$ ($t_{0.975,4} = 2.7764451051977987$) when dropping $5-k \in \{1, 2\}$ stalled seeds with $\bar x_k - \bar x_{\text{drop}} = d > 0$:
     - For $k=4$: $\text{UB}_4 \le \text{UB}_5 - d\left(\frac{t_4\sqrt{3}}{5} - \frac{3}{5}\right) = \text{UB}_5 - 0.3552894654242343\,d < \text{UB}_5 \le 0$.
     - For $k=3$: $\text{UB}_3 \le \text{UB}_5 - d\left(\frac{t_4\sqrt{10}}{10} - \frac{3}{5}\right) = \text{UB}_5 - 0.28008707789167844\,d < \text{UB}_5 \le 0$.
     - Confirmed that `stop -> keep` and `stop -> modify` are algebraically unreachable under step-7 seed dropping, leaving exactly `10` reachable ordered pairs $(c_5, c_k)$ with $c_5 \ne c_k$ per $k \in \{3, 4\}$ (`20` reachable pairs across $k \in \{3, 4\}$).

2. **Independent Temp-Copy Mutation Testing of r2 Blocking Mutants and Novel Adversarial Mutants (`probe2_blocking_and_adversarial_mutants.py` → `probe2_blocking_and_adversarial_mutants.out.json`)**:
   - In an isolated temporary copy under `/home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/_tmp_mutation_work/` (cleaned up upon completion; `"temp_work_dir_cleaned": true`), ran:
     - **Unmutated baseline (`CTRL`)**:
       - Leg A (`tests/topic2_fu_d` with `-k "not m0_is_the_only"`): `SURVIVED` (`rc = 0`, `383 passed, 1 deselected in 26.10s`).
       - Leg B (Leg A with `--ignore=tests/topic2_fu_d/test_fud_r3_guards.py --ignore=tests/topic2_fu_d/test_fud_r3_oracle.py --ignore=tests/topic2_fu_d/test_fud_r3_full_output.py`): `SURVIVED` (`rc = 0`, `189 passed, 1 deselected in 10.53s`).
       - R3-only (`test_fud_r3_{guards,oracle,full_output}.py`): `SURVIVED` (`rc = 0`, `194 passed in 15.70s`).
     - **All 34 `killed_only_by_r3_files` distinct mutants** (`cha2_1:CP01`, `cha2_1:CP02`, `cha2_1:CP04`/`cha2_2:S08`, `cha2_1:CP05`, `cha2_1:CP07`/`cha2_2:S05`, `cha2_1:CP11`/`cha2_2:S09`, `cha2_1:CP12`, `cha2_1:CP14`, `cha2_1:CR01`/`cha2_2:R04`, `cha2_1:CR13`/`cha2_2:R07`, `cha2_1:CV09`/`cha2_2:C12`, `cha2_1:CV15`, `cha2_1:CV19`, `cha2_2:C23`, `exp3_1:own:E7a`–`E7f`, `exp3_1:own:E7i`, `exp3_1:own:W1`, `exp3_1:own:W2`, `exp3_1:r2:R35`, `exp3_2:own:N04`, `exp3_2:own:N06`, `exp3_2:own:N07`, `exp3_2:own:N08`, `exp3_2:own:N12`, `exp3_2:own:N14`, `exp3_2:own:N18`, `exp3_3:T24`, `rev2_1:R31`/`cha2_2:S11`, `rev2_1:R34`/`cha2_1:CP03`/`cha2_2:S07`):
       - **34 / 34 (`100%`) KILLED** by `tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py` (`"all_34_killed_by_r3_files": true`).
       - Re-ran Leg B (without the 3 r3 test files) on 9 core r2 blocking / explorer mutants (`cha2_1:CV09`/`C12`, `cha2_1:CP01`, `cha2_1:CP02`, `exp3_1:own:E7a`, `exp3_1:own:W1`, `exp3_2:own:N14`, `cha2_1:CR13`/`R07`, `rev2_1:R31`/`S11`, `rev2_1:R34`/`CP03`/`S07`): **9 / 9 SURVIVED** in Leg B (`189 passed, 1 deselected`), proving that the new r3 test files are both necessary and sufficient to kill them.
     - **12 Novel Challenger Adversarial Mutants (`CHA3_01`..`CHA3_12`)** targeting single-pair exemptions in step-7 (`modify -> stop`, `inconclusive -> keep`), `len(kept) == 3` suppression, `kept[:2]` truncation, passing all-seed `I2_t` instead of `st2["I2_t"]`, dropping explicit `delta` forwarding to `fminus_gate`, dropping arm `S` from script stall check, omitting `sorted()` on `stalled_runs`, scale reading boundary `<` vs `<=`, `HP_FIELDS[:-1]` truncation, `RESERVE_RUNS` omission in `seedplan.py`, and `round` vs `math.ceil` in `slurm.gpuh`:
       - **12 / 12 (`100%`) KILLED** in Leg A (`"all_12_novel_adversarial_killed": true`).

3. **Exhaustive Audit of `union_r3.out.json` (1,675 Distinct Mutants) and the 164-Survivor Classification (`probe3_v2_audit_union_survivors.py` → `probe3_v2_audit_union_survivors.out.json`)**:
   - **Deduplication & Tally Audit**:
     - `collected.json` (`1,518` entries from 7 prior verifier sets) + `sweep_r3.json` (`533` systematic AST mutations across `src/topic2_fu_d/*.py` and `scripts/topic2fu_d_*.py`) = `2,051` raw entries.
     - Exactly `1` raw entry (`rev2_1:R42`, targeting `scripts/topic2fu_d_verdict.py` for a string in `src/topic2_fu_d/verdict.py`, where `rev2_1:R43` and `exp3_3:W107` apply the exact mutation) did not apply; the remaining `2,050` applied entries deduplicate by `(target_file, sha256(mutated_bytes))` to **exactly `1,675` distinct mutants** (`"exact_uid_set_match": true`).
     - In `union_r3.out.json`: `total_distinct = 1675`, `killed = 1511`, `survived = 164`, `invalid = 0`, `shipped_changing = 515` (**all `515` killed in Leg A; `0` survivors change shipped output**), `killed_only_by_r3_files = 34` distinct listed mutants (`91` listed raw aliases; `120` total raw aliases including `r3:*` sweep aliases).
     - Verified that **all 50** `exp3_3:W*` mutants flagged as O5 non-equivalent in `explorer_FU_D_r3_3/handoff.md` and **all 24** `exp3_3:T01`..`T24` targeted mutants are **KILLED** in Leg A (`0` survived).
   - **Bijection & Semantic Audit of the 164 Survivors (`addendum_02.md` §5)**:
     - Parsed the 10-class table in `addendum_02.md` §5: `61 + 41 + 9 + 9 + 6 + 3 + 6 + 14 + 7 + 8 = 164` UIDs, pairwise disjoint (`0` duplicates), with `in_table_not_in_survived = []` and `in_survived_not_in_table = []`.
     - Programmatically verified all `61` Class-1 (`A != B` conjoined with `A != C` where `B != C` is tautological when `A == B`) and all `41` Class-2 (`x != C1` conjoined with `x != C2` where `x`'s domain never takes `C2`) survivors, and extracted and audited every single diff of the `62` Class 3–10 survivors (`probe3_v2_audit_union_survivors.out.json`). Confirmed that **0 of the 164 survivors** can alter any card-governed gate, Stage-1, F-minus, step-7, or secondary output on any valid or card-governed input.

4. **Full Test Suites, C4 Hygiene, and Layout Audit (`probe4_v2_c4_and_hashes.py` → `probe4_v2_c4_and_hashes.out.json`)**:
   - Full `tests/topic2_fu_d`: `389 passed in 63.71s`.
   - Old regression suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` with `STRICT_E2E=1`): `86 passed in 32.54s`.
   - `tests/topic2_rgpool tests/topic1_lagmotif`: `204 passed in 85.22s`.
   - C4 hygiene scan (`scripts/topic2fu_d_c4scan.py` + `probe4_v2_c4_and_hashes.py` over `122` FU-D/r3 files and `14` challenger files): `0` 16-hex content token hits, `0` BIDS prefix hits, `0` 6-digit integer hits.

---

## 2. Logic Chain

1. **Gate Statistics and `inconclusive` Verdict (`Task 1`)**:
   - The preregistered card (`2026-11-02_topic2_fu_d_card.md` §5) requires both `1 - NMSE(F+, C)/NMSE(F+, E) >= 0.01` and `1 - NMSE(F+, C)/NMSE(F+, S) >= 0.01` at seed 0 before any Stage-1 (`hcp`) or `F-` run may be launched or read.
   - Exact rational arithmetic on `Fplus_{E,C,S}_s0/run.json` yields `0.3631%` (`C` vs `E`) and `0.6546%` (`C` vs `S`), both strictly below `1.00%`. Therefore the measurement-capacity gate fails, Stage 1 is neither run nor read, and the primary verdict is `inconclusive`.
2. **Closure of r2 Blocking Issues (`Task 2`)**:
   - In r2, `B1` identified that `verdict.py:130` (`C12`/`CV09`) and `scripts/topic2fu_d_verdict.py:85-97` (`CP01`, `CP02`, and siblings) were unkilled by the r2 test suite, and `B2` identified that erratum E5 (alias run directories) lacked a round-trip reading rule and shipped-artifact invariant test.
   - In r3, `test_fud_r3_guards.py`, `test_fud_r3_oracle.py`, and `test_fud_r3_full_output.py` (194 tests total, including exhaustive parameterization over all 20 reachable `(c_5, c_k)` step-7 pairs, a 218-scenario independent reference oracle, per-arm/multi-seed stall tests, and `test_shipped_runs_dir_has_only_fplus_and_zero_aliases`) kill all 34 `killed_only_by_r3_files` mutants and all 12 novel challenger mutants while leaving frozen production code untouched (C1/freeze intact).
3. **1,675-Mutant Union & 164-Survivor Equivalence (`Task 3`)**:
   - All 515 mutants that alter any byte of the shipped output (`verdict.json` + stdout) are killed in Leg A.
   - All 164 surviving mutants are confined to Leg-A test-invariant regions (102 boolean tautologies/disjoint-domain conjuncts from `sweep_r3.py`, 27 boundary `<=` vs `<` or numeric-literal perturbations inside unreachable interiors of deterministic fixtures, 17 benign CLI defaults/views/diagnostic strings, and 18 schema-guard detail variations that still reject invalid inputs).

---

## 3. Caveats (Nonblocking Findings Only)

No blocking issues remain. We record three minor **nonblocking** documentation observations in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md` §5:

1. **NB1 — `CTRL` Leg B attribution in `addendum_02.md` §5 (line 190)**:
   - `addendum_02.md` §5 line 190 (and `worker_FU_D_r3/handoff.md` line 14) states: `Baseline control (CTRL): SURVIVED (383 passed, 1 deselected in Leg A; 189 passed, 1 deselected in Leg B; shipped_changed = False)`.
   - In `verification/worker_FU_D_r3/mutation/run_union_r3.py:134`, `one()` only executes Leg B when `rec["A"]["status"] == "KILLED" and m.get("listed")`, so `union_r3.out.json["control"]` contains `"A"` and `"shipped_changed"` but no `"B"` key. However, our `probe2_blocking_and_adversarial_mutants.py` ran Leg B directly on `CTRL` and confirmed that `CTRL` indeed passes Leg B with `189 passed, 1 deselected` (`rc = 0`).
2. **NB2 — Wording of Class-2 rationale for `r3:conj0303`–`0313` in `addendum_02.md` §5 (line 226)**:
   - Line 226 explains `r3:conj0303`–`0313` (`records.py:134` `sst != "COMPLETED"` conjoined with `sst != L` for lowercase literals `L`) by stating `sst = str(...).upper() is uppercase and never equals a lowercase literal`.
   - In `src/topic2_fu_d/records.py:133–135`, `sst = slurm.get("state") if isinstance(slurm, dict) else None` (no `.upper()`; `.lower()` appears on line 135). The conjuncts are nevertheless disjoint-domain on all valid Slurm sidecars because `scripts/topic2fu_d_slurm.py:240` only writes `slurm.json` for terminal states in `slurm.TERMINAL` (all 9 of which are uppercase strings).
3. **NB3 — Wording of Class-8 rationale for `exp3_3:W376` in `addendum_02.md` §5 (line 232)**:
   - Line 232 explains `exp3_3:W376` (`src/topic2_fu_d/records.py:77`, dropping `not toks or` from `if not toks or any(not isinstance(t, str) or not PSEUDO_RE.match(t) for t in toks):`) as `not toks caught on line 80 by toks != list(exp["test_tokens"])`.
   - That holds when `toks == []`, whereas when `toks is None` (missing `"test_pseudonyms"` key in an `hcp` record), dropping `not toks or` causes `for t in toks` on line 77 to raise `TypeError` instead of `RecordError`. Since `TypeError` still rejects the malformed record with an exception (and no valid record omits `"test_pseudonyms"`), `exp3_3:W376` is equally benign (closer to Class 10 exception-type detail than Class 8).

---

## 4. Conclusion

Milestone `FU_D` Iteration 3 (`FU_D_r3`) is **`CONFIRMED`**. All three tasks in our dispatch are empirically verified, all blocking issues from Iteration 2 (`B1` and `B2`) are genuinely closed by `tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py`, the 1,675-mutant union (`1,511` killed + `164` benign/equivalent survivors) and `addendum_02.md` §4–§5 hold under independent recomputation, and all C1/C4/receipt invariants are 100% clean.

---

## 5. Verification Method

All checks are reproducible on CPU (`CUDA_VISIBLE_DEVICES=""`) via:

```bash
# 1. Independent gate recomputation, 9 receipt manifests, chronology, and algebraic proof P1
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice \
  /home/juke/superclaude-env/bin/python3 \
  /home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/probe1_gate_and_receipts.py

# 2. Independent temp-copy mutation testing (CTRL Leg A/B/R3, 34 r3-only mutants, 12 novel adversarial mutants)
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice \
  /home/juke/superclaude-env/bin/python3 \
  /home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/probe2_blocking_and_adversarial_mutants.py

# 3. Exhaustive audit of union_r3.out.json (1,675 distinct mutants) and 164 survivors in addendum_02.md §5
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice \
  /home/juke/superclaude-env/bin/python3 \
  /home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/probe3_v2_audit_union_survivors.py

# 4. C4 hygiene scan (122 FU-D/r3 files + challenger files) and SHA-256 manifest
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice \
  /home/juke/superclaude-env/bin/python3 \
  /home/juke/git/00IITP-AI/verification/challenger_FU_D_r3_1/probe4_v2_c4_and_hashes.py

# 5. Full test suites (run sequentially, 1 pytest process at a time)
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice \
  /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
CUDA_VISIBLE_DEVICES="" STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice \
  /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice \
  /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool tests/topic1_lagmotif -q
```
