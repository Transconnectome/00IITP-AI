# Handoff — reviewer_FU_D_r3_1 (Milestone FU_D Iteration 3, Reviewer 1 of 2)

- **Run**: `tw-20261031-four-topics` (General route, Workflow C)
- **Milestone / Iteration**: `FU_D` Iteration 3 (`FU_D_r3`)
- **Role**: `reviewer_FU_D_r3_1` (Independent Reviewer 1 of 2)
- **Verdict**: **`APPROVE`** (`0` blocking issues, `0` non-blocking issues)

---

## 1. Observation

1. **Pre-freeze & Receipt Integrity (`C1`, `C5`, `F1`)**:
   - `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: `sha256sum -c` exited with `rc=0` (`67/67 OK`).
   - `results/topic2/2026-11-02_fu_d/card_sha256.txt`: `rc=0` (`1/1 OK`, `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md` = `1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b`).
   - `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`: `rc=0` (`29/29 OK`; all 7 modules in `src/topic2_fu_d/`, all 9 scripts in `scripts/topic2fu_d_*.py`, and all 13 pre-freeze test files in `tests/topic2_fu_d/` are byte-identical to the pre-GPU freeze).
   - `results/topic2/2026-11-02_fu_d/output_sha256.txt`: `rc=0` (`34/34 OK`; `verdict.json` = `f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`, `2026-11-02_topic2_fu_d_result_report.md` = `3e34f3db128bb8a24ddaa1b118a3f9edef46a6a00d5d4455d9886da8db0c457b`).
   - `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`: `rc=0` (`23/23 OK`; `2026-11-02_topic2_fu_d_addendum_01.md` = `71d8a3f348528b775258d9bbff05a9894366b026589dc8b7bb278f3c6674a6cf`).
   - `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt`: `rc=0` (`102/102 OK`; `2026-11-02_topic2_fu_d_addendum_02.md` = `8742bc4eb5d59c5b2572b05a0b481b761f12d4dfbc22bc88eb0935ff7e4aa6b8`).
   - Topic 2 r1 receipts (`results/topic2/2026-11-01/code_sha256_at_freeze.txt` `33/33 OK`, `output_sha256_r2.txt` `156/156 OK`, `addendum_06_sha256.txt` `31/31 OK`) are untouched.

2. **Test Suites Re-executed Sequentially (1 pytest process at a time, CPU-only)**:
   - `tests/topic2_fu_d`: `rc=0`, **`389 passed, 2 warnings in 79.59s`** (up from 195 in r2 via +194 additive tests across `test_fud_r3_guards.py` [153], `test_fud_r3_oracle.py` [22], and `test_fud_r3_full_output.py` [19]).
   - `tests/topic2_rgpool`: `rc=0`, **`116 passed, 24 warnings in 109.76s`**.
   - Old suite (`STRICT_E2E=1`, `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): `rc=0`, **`86 passed, 7 warnings in 32.85s`**.
   - `tests/topic1_lagmotif`: `rc=0`, **`88 passed in 5.24s`**.

3. **Headline Metrics, Provenance & Verdict Regeneration (`F1`, `F2`, `F3`, `C2`, `C3`, `C6`, `C7`, `C8`)**:
   - Independent recomputation from raw `results/topic2/2026-11-02_fu_d/runs/Fplus_{E,C,S}_s0/run.json` (`verification/reviewer_FU_D_r3_1/audit_r3.py` -> `audit_r3.out.json`) confirms:
     - Pooled `test_nmse = sum(test_num) / sum(test_den)` matches shipped `run.json` and `verdict.json` (`E = 0.65585`, `C = 0.65347`, `S = 0.65777` to 5 d.p.; exact float equality verified in `audit_r3.py`).
     - Relative gains: `g(C vs E) = (E - C)/E = 0.00363` (`0.363%`, `|diff| < 1e-15` vs `verdict.json`), `g(C vs S) = (S - C)/S = 0.00655` (`0.655%`, `|diff| < 1e-15` vs `verdict.json`).
     - Both gains are strictly below `delta = 0.01` (`1.0%`), so the F+ measurement-capacity gate fails (`gate_pass = False`), Stage 1 on HCP was not run (`seed_plan.json` absent; `runs/` holds only `Fplus_C_s0`, `Fplus_E_s0`, `Fplus_S_s0`), and the card verdict is `inconclusive` (measurement capacity at E192).
     - Regenerating `verdict.json` into an isolated temp path via `scripts/topic2fu_d_verdict.py` yields byte-for-byte identical JSON (`sha256 = f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc`).
     - CPU smoke-equivalence (`results/topic2/2026-11-02_fu_d/equiv_check.json`) is exact (`max_abs_diff = 0.0`, identical state-dict SHA-256 across all 3 arms).
     - Compute ledger (`results/compute_ledger.jsonl`): FU-D used `3.672 GPU-h` total across r1 (`<= 25 GPU-h` cap) and `0 GPU-h` in r2 and r3.

4. **Closure of r2 Gate Failure `B1` (`C12` / `CV09` and sibling class)**:
   - In r2, `challenger_FU_D_r2_2` found that mutating `src/topic2_fu_d/verdict.py:130` (`if cat in ("keep", "modify") and c2 != cat:` -> `if cat in ("stop", "modify") and c2 != cat:`, mutant `C12` = `CV09`) survived `pytest tests/topic2_fu_d`.
   - In r3, `worker_FU_D_r3` added 3 additive test files (`test_fud_r3_guards.py`, `test_fud_r3_oracle.py`, `test_fud_r3_full_output.py`) and audited the 1,675-mutant union across all 5 prior agents (`worker_FU_D_r2`, `reviewer_FU_D_r2_1`, `reviewer_FU_D_r2_2`, `challenger_FU_D_r2_1`, `challenger_FU_D_r2_2`) plus the r3 explorer (`verification/worker_FU_D_r3/mutation/union_r3.out.json`).
   - Our independent audit (`audit_r3.py` and `mut_probe.py`) confirms:
     - All 28 reachable `(stalled_seeds, cat_all, cat_wo)` pairs for 1 and 2 stalled seeds (`n = 5`) are tested against an independent `scipy.stats.t.ppf(0.975, df)` oracle at both `_stage1_category` and `decide`.
     - The algebraic boundary proof `P1` in Addendum 02 §2.1 holds (`k = 4`: `2 * t_crit(df=4) / 5 - 3/4 = +0.3553 > 0`; `k = 3`: `2 * sqrt(2/3) * t_crit(df=4) / 5 - 3/5 = +0.2801 > 0`), confirming why `stop -> keep` and `stop -> modify` are unreachable for `n = 5` and thus why `28 = 2 * 14` of the `2 * 16 = 32` table pairs are reachable on real inputs while all `16` pairs are covered via unit-level table injection.
     - Across the 1,675 distinct applicable mutants in `union_r3.out.json`, `1,511` are killed (`34` killed exclusively by the 3 new r3 test files, including `cha2_2:C12` / `cha2_1:CV09`, `cha2_1:CP01`, `cha2_1:CP02`, `rev2_1:R31` / `cha2_2:S11`, `rev2_1:R34` / `cha2_2:S07`, `rev2_2:R35`, `cha2_1:CV15`, `cha2_1:CV19`, `cha2_2:R04`, `cha2_2:R07`, `cha2_2:S08`, `cha2_1:CP05` / `cha2_2:S05`, `cha2_2:S09`, `cha2_1:CP12`, `cha2_1:CP14`, `cha2_2:C23`), and the `164` survivors partition exhaustively (`61 + 41 + 9 + 9 + 6 + 3 + 6 + 14 + 7 + 8 = 164`) into the 10 verified classes in Addendum 02 §2.5 with **zero** survivors changing the shipped `verdict.json` (`515/515` output-changing mutants killed).
     - Our independent live mutation probe (`verification/reviewer_FU_D_r3_1/mut_probe.py` -> `mut_probe.out.json`) ran `pytest` in an isolated temp tree against 22 targeted single-line mutants spanning `C12` and all Step-7 / stall-arm / secondary-bootstrap / record-validation / delta-forwarding branches: **`22/22 KILLED` (`0 SURVIVED`)**.

5. **Closure of r2 Gate Failure `B2` (alias run directories) & Errata**:
   - In r2, `challenger_FU_D_r2_2` found (`B2`) that `parse_dir` in `src/topic2_fu_d/design.py:25` uses `int(m.group(3))` without rejecting leading zeros or non-ASCII digits (`\d+` + `re.Z`), allowing an alias directory such as `Fplus_C_s00` to map to `("Fplus", "C", 0)` and overwrite `Fplus_C_s0` in `R.load_runs` under lexicographic `sorted(os.listdir(runs_dir))`.
   - Because `src/topic2_fu_d/design.py` and `src/topic2_fu_d/records.py` are frozen in `code_sha256_at_freeze.txt`, `worker_FU_D_r3` properly documented this departure as Erratum `E5` in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md` §3.1 (alongside widened `E2'`, `E6`, `E7`, `E8`, `E9`, `W4`, `W5`, and the mandatory §3.9 reuse condition for any future card), corrected Addendum 01 §4's unscoped mutation-survivor statement in Addendum 02 §2, provided a reproducible script (`verification/worker_FU_D_r3/probes/errata_probe.py` -> `errata_probe.out.json`), and added shipped-data invariant tests in `tests/topic2_fu_d/test_fud_r3_guards.py` (`test_shipped_runs_dir_has_only_canonical_names_and_no_duplicate_keys`, `test_shipped_records_have_finite_positive_terms_and_r1_denominators`, `test_shipped_sidecars_match_code_sha256_at_freeze`).
   - Our independent probe (`verification/reviewer_FU_D_r3_1/errata_verify.py` -> `errata_verify.out.json`) re-executed `errata_probe.py` in an isolated temp directory, verified exact bit-for-bit reproduction of `errata_probe.out.json`, and confirmed that `results/topic2/2026-11-02_fu_d/runs/` contains only the 3 canonical directories `["Fplus_C_s0", "Fplus_E_s0", "Fplus_S_s0"]` with bijective `name == run_name(parse_dir(name)[0])`.

6. **C4 Participant-ID Hygiene & Layout Audit**:
   - `scripts/topic2fu_d_c4scan.py`: `n_files = 84`, `token_hits = 0`, `bids_hits = 0`.
   - `verification/worker_FU_D_r3/c4_scan_r3.py`: `n_files = 36`, `token_hits = 0`, `bids_hits = 0`, `six_digit_hits = 0`.

---

## 2. Logic Chain

1. **Pre-freeze and receipt preservation (`C1`, `C5`, `F1`)**: Because every hash in `PROTECTED_HASHES.txt`, `card_sha256.txt`, `code_sha256_at_freeze.txt`, `output_sha256.txt`, `addendum_01_sha256.txt`, and `addendum_02_sha256.txt` verifies with `rc=0`, all frozen code, pre-GPU card commitments, GPU run outputs, and prior reports are provably unmodified in Iteration 3.
2. **Class-level closure of `B1`**: Because (a) `test_fud_r3_guards.py` tests every reachable `(stalled_seeds, cat_all, cat_wo)` pair for `1` and `2` stalled seeds (`28` pairs) against an independent `scipy.stats.t.ppf(0.975, df)` oracle at both `_stage1_category` and `decide`, plus all `16` pairs via unit injection and script-level per-arm (`E`, `C`, `S`) and multi-seed stall scenarios, (b) `test_fud_r3_oracle.py` validates `V.decide()` against an independent card-section-8 oracle across `3,000` seeded scenarios, (c) `test_fud_r3_full_output.py` validates deep equality of the entire `verdict.json` and stdout summary across `17` synthetic scenarios, and (d) all `22/22` live mutation probes and all `1,511` killable mutants in the `1,675`-mutant union sweep are killed while the `164` survivors are exhaustively partitioned into `10` verified classes (equivalent, boundary-equivalent, or documented frozen-code errata), `B1` (`C12` / `CV09` and its sibling class) is closed at class level.
3. **Closure of `B2` and frozen-code errata under the C1/code-freeze constraint**: Because `src/topic2_fu_d/` is frozen by `code_sha256_at_freeze.txt`, the only protocol-compliant response to a frozen-code validation gap on unshipped synthetic inputs (`E5` alias directories, `E2'` non-finite/negative terms, `E6`–`E9`, `W4`–`W5`) is to (i) document the exact mechanism and scope in an addendum (`2026-11-02_topic2_fu_d_addendum_02.md` §3) with a reproducible witness (`errata_probe.out.json`), (ii) correct the over-broad survivor claim from Addendum 01 §4 (done in Addendum 02 §2), (iii) prove via automated tests on the shipped artifacts (`test_fud_r3_guards.py`) that the shipped `results/topic2/2026-11-02_fu_d/` tree lies strictly outside every departure, and (iv) record a mandatory code-fix checklist before any future card reuses `src/topic2_fu_d/` (Addendum 02 §3.9). All four steps are complete and independently verified.
4. **Therefore**, all common criteria (`C1`–`C8`), all milestone criteria (`F1`–`F3`), and both iteration-2 blocking findings (`B1`, `B2`) are satisfied with zero remaining blocking or non-blocking issues.

---

## 3. Caveats

1. **Frozen-code departures (`E1`–`E9`, `W1`–`W5`) remain in `src/topic2_fu_d/` and `scripts/topic2fu_d_verdict.py` by design**: Modifying those files would violate the pre-GPU code freeze (`code_sha256_at_freeze.txt`). They cannot affect the shipped FU-D verdict because the shipped `results/topic2/2026-11-02_fu_d/` artifacts satisfy the stricter canonical invariants enforced by `test_fud_r3_guards.py`. If a future milestone reuses `src/topic2_fu_d/`, Addendum 02 §3.9 requires fixing `E1`–`E9` and `W1`–`W5` before that future card's code freeze.
2. **External r2 mutation line `rev2_1:R42` (`1` of `1,676` distinct union mutants)**: As documented in `union_r3.out.json` (`not_applied = ["rev2_1:R42"]`), `rev2_1:R42` targets a pre-truncated substring from `reviewer_FU_D_r2_1`'s probe that does not appear verbatim in `scripts/topic2fu_d_verdict.py`, whereas its exact functional equivalents (`rev2_1:R31` and `cha2_2:S11`) apply cleanly and are killed by `test_fud_r3_guards.py::test_missing_gate_run_with_plan_and_stage1_keep_data_is_no_verdict_and_unread`.

---

## 4. Conclusion

- **Verdict**: **`APPROVE`**
- **Blocking issues**: None (`[]`)
- **Non-blocking issues**: None (`[]`)
- **Uncovered requirements**: None (`[]`)

---

## 5. Verification Method

All independent verification commands and probes were executed CPU-only (`CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3`) with logs and JSON outputs saved under `/home/juke/git/00IITP-AI/verification/reviewer_FU_D_r3_1/`:
- `verification/reviewer_FU_D_r3_1/logs/c1_start.out` and `c1_end.out`: `sha256sum -c` on `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` (`67/67 OK`).
- `verification/reviewer_FU_D_r3_1/logs/receipts_fud.out`: `sha256sum -c` on `card_sha256.txt` (`1/1`), `code_sha256_at_freeze.txt` (`29/29`), `output_sha256.txt` (`34/34`), `addendum_01_sha256.txt` (`23/23`), `addendum_02_sha256.txt` (`102/102`), plus r1 receipts (`33/33`, `156/156`, `31/31`).
- `verification/reviewer_FU_D_r3_1/logs/pytest_fud.out`: `pytest tests/topic2_fu_d` (`389 passed, 2 warnings in 79.59s`).
- `verification/reviewer_FU_D_r3_1/logs/pytest_rgpool.out`: `pytest tests/topic2_rgpool` (`116 passed, 24 warnings in 109.76s`).
- `verification/reviewer_FU_D_r3_1/logs/pytest_old86.out`: `STRICT_E2E=1 pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` (`86 passed, 7 warnings in 32.85s`).
- `verification/reviewer_FU_D_r3_1/logs/pytest_topic1.out`: `pytest tests/topic1_lagmotif` (`88 passed in 5.24s`).
- `verification/reviewer_FU_D_r3_1/audit_r3.py` -> `audit_r3.out.json`: Independent recomputation of F+ gate NMSE and gains, byte-identical regeneration of `verdict.json`, provenance/sidecar/ledger audit, algebraic verification of `P1`, and audit of the `1,675`-mutant union sweep (`union_r3.out.json`).
- `verification/reviewer_FU_D_r3_1/mut_probe.py` -> `mut_probe.out.json`: Independent live execution of `22` single-line mutants in an isolated temp tree (`22/22 KILLED`, `0 SURVIVED`).
- `verification/reviewer_FU_D_r3_1/errata_verify.py` -> `errata_verify.out.json`: Independent reproduction of `errata_probe.out.json` (`exact = True`) and canonical bijection check on `results/topic2/2026-11-02_fu_d/runs/`.
- `verification/reviewer_FU_D_r3_1/logs/c4scan_fud.json` & `c4scan_r3.json`: C4 hygiene scans (`0` hits across `84` and `36` files).

---

## Structured Verdict JSON

```json
{
  "verdict": "APPROVE",
  "full_report": "Independent review of Milestone FU_D Iteration 3 (reviewer_FU_D_r3_1) confirms that all ACCEPTANCE criteria (C1-C8), all milestone criteria (F1-F3), and both Iteration 2 Challenger 2 blocking findings (B1: C12/CV09 Step-7 stall-sensitivity branch and sibling class; B2: parse_dir / load_runs alias run-directory resolution and frozen-code errata) are fully resolved. All pre-freeze and receipt manifests (PROTECTED_HASHES.txt 67/67, card_sha256.txt 1/1, code_sha256_at_freeze.txt 29/29, output_sha256.txt 34/34, addendum_01_sha256.txt 23/23, addendum_02_sha256.txt 102/102, and r1 receipts 33/33, 156/156, 31/31) pass sha256sum -c with rc=0. All four pytest suites pass sequentially on CPU (tests/topic2_fu_d: 389 passed; tests/topic2_rgpool: 116 passed; old suite 86 with STRICT_E2E=1: 86 passed; tests/topic1_lagmotif: 88 passed). Independent probes (audit_r3.py, mut_probe.py [22/22 live mutants killed], errata_verify.py [exact reproduction of errata_probe.out.json and canonical bijection on shipped runs/]) and C4 hygiene scans (0 hits) all pass.",
  "blocking_issues": [],
  "nonblocking_issues": [],
  "commands_run_and_results": [
    {
      "command": "sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt",
      "rc": 0,
      "summary": "67/67 OK (verified at start and end of review)"
    },
    {
      "command": "cd results/topic2/2026-11-02_fu_d && sha256sum -c card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt addendum_01_sha256.txt addendum_02_sha256.txt",
      "rc": 0,
      "summary": "1/1 OK, 29/29 OK, 34/34 OK, 23/23 OK, 102/102 OK"
    },
    {
      "command": "cd results/topic2/2026-11-01 && sha256sum -c code_sha256_at_freeze.txt output_sha256_r2.txt addendum_06_sha256.txt",
      "rc": 0,
      "summary": "33/33 OK, 156/156 OK, 31/31 OK"
    },
    {
      "command": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q",
      "rc": 0,
      "summary": "389 passed, 2 warnings in 79.59s"
    },
    {
      "command": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool -q",
      "rc": 0,
      "summary": "116 passed, 24 warnings in 109.76s"
    },
    {
      "command": "STRICT_E2E=1 CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q",
      "rc": 0,
      "summary": "86 passed, 7 warnings in 32.85s"
    },
    {
      "command": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic1_lagmotif -q",
      "rc": 0,
      "summary": "88 passed in 5.24s"
    },
    {
      "command": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_D_r3_1/audit_r3.py",
      "rc": 0,
      "summary": "Recomputed F+ NMSE/gains, regenerated byte-identical verdict.json, verified P1 algebra and 1675-mutant union (1511 killed, 164 classified survivors, 0 output-changing survivors)"
    },
    {
      "command": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_D_r3_1/mut_probe.py",
      "rc": 0,
      "summary": "Control passed (383 passed); 22/22 live single-line mutants KILLED (0 SURVIVED)"
    },
    {
      "command": "CUDA_VISIBLE_DEVICES=\"\" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_D_r3_1/errata_verify.py",
      "rc": 0,
      "summary": "Bit-for-bit reproduction of errata_probe.out.json and canonical bijection check on shipped runs/"
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_d_c4scan.py --out verification/reviewer_FU_D_r3_1/logs/c4scan_fud.json && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/worker_FU_D_r3/c4_scan_r3.py verification/reviewer_FU_D_r3_1/logs/c4scan_r3.json",
      "rc": 0,
      "summary": "84 files (0 token/BIDS hits) and 36 files (0 token/BIDS/6-digit hits)"
    }
  ],
  "tested_artifact_sha256": {
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md": "1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b",
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_result_report.md": "3e34f3db128bb8a24ddaa1b118a3f9edef46a6a00d5d4455d9886da8db0c457b",
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_01.md": "71d8a3f348528b775258d9bbff05a9894366b026589dc8b7bb278f3c6674a6cf",
    "docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_addendum_02.md": "8742bc4eb5d59c5b2572b05a0b481b761f12d4dfbc22bc88eb0935ff7e4aa6b8",
    "results/topic2/2026-11-02_fu_d/verdict.json": "f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc",
    "results/topic2/2026-11-02_fu_d/runs/Fplus_E_s0/run.json": "e8dd406f85017c83f2a0ab7a21a1e8f9a192a460ba601cfbd7d1f6f51b8cd696",
    "results/topic2/2026-11-02_fu_d/runs/Fplus_C_s0/run.json": "89477c50d3fa25699597f71bd266041763d485ba126619d8d0a125db5624e5b2",
    "results/topic2/2026-11-02_fu_d/runs/Fplus_S_s0/run.json": "bf4da2e9ec87d719c979a966052ce829ffbb8080a94f3fa2da41715f909aa7d4",
    "tests/topic2_fu_d/test_fud_r3_guards.py": "ba46e52d8a17d457f61de34c00202e881a5cf95aa7ab8d8b7d93a1ab8a5f17c1",
    "tests/topic2_fu_d/test_fud_r3_oracle.py": "c2f59fa3e7ae08c06fb4397028199bc3bc640e94c8bd80da1db6d544c8044e65",
    "tests/topic2_fu_d/test_fud_r3_full_output.py": "3395271f7c4f415518e3b97fd788a1242b3c2dd65710fc6468d5f3e7b6a154d9",
    "verification/worker_FU_D_r3/mutation/union_r3.out.json": "003e310a7efdb1f67e1918442f01532d6352abcf96775a4e935a4a7180c0d1cb",
    "verification/worker_FU_D_r3/probes/errata_probe.out.json": "076640d53fd2c9d7bb9634be465d85be772441bcbb76eb60a3324b4cf0062e23"
  },
  "uncovered_requirements": []
}
```
