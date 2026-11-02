# Topic 2 follow-up B (FU-B) result report: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds

Date: 2026-11-02 KST (runs 2026-11-01T15:31Z – 2026-11-02T02:08Z). Author: worker_FU_B_r1, run tw-20261031-four-topics, workflow C, milestone FU_B (PI decision 7; r1 result report `2026-11-01_topic2_result_report.md` §7, option B).

**Governing card.** `2026-11-02_topic2_fu_b_card.md` (v2 sha256 `994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae`, governed with `2026-11-02_topic2_fu_b_addendum_01.md` sha256 `4acafa5b5746d1771d85d8403727d58ff6ecc2d27475f5d5b8ec7534edd80817`).
- **Freeze order:** v1 of the card (sha256 `a9c4cab03ac99305e44b0aa2ab550fbe402f7f4b74ac3c239d082021e76e0726`) and all 21 FU-B code/test files plus 8 pinned inputs were frozen at `2026-11-01T16:05:18Z` (`results/topic2/2026-11-02_fu_b/card_sha256.txt`). Before any gate or Stage-1 task started (`sacct` at `16:19:52Z`: jobs 509 and 516 PENDING, ElapsedRaw 0), one hyphenated English word in card §2 that tripped the frozen r1 BIDS-prefix regex was replaced (`2026-11-02_topic2_fu_b_addendum_01.md`), and v2 was frozen at `2026-11-01T16:20:25Z` (`results/topic2/2026-11-02_fu_b/card_sha256_v2.txt`). The first gate task (`509_0`) started at `2026-11-01T16:20:41Z`.
- **No post-freeze changes:** every file in `card_sha256_v2.txt` verifies unmodified after all runs completed. No `addendum_02.md` was needed.

**Sources (C8).** Every number below comes from `results/topic2/2026-11-02_fu_b/verdict.json` (rendered by `verification/worker_FU_B_r1/report_numbers.py`), `results/topic2/2026-11-02_fu_b/gate_4x.json`, `results/topic2/2026-11-02_fu_b/b300/runs/*/run.json`, and `results/gpu_ledger_2026-10-31.md`. No number is taken from `EMPIRICAL_ANALYSIS_REPORT.md` or `2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md`.

**r1 is unchanged.** The r1 verdict (`stop`; I1 `+0.147 %` `[−0.068 %, +0.361 %]`, df 4, at 140k samples) stays as recorded. FU-B is a new confirmatory experiment alongside r1.

---

## 0. Executive Summary and Verdict

**`stop` (killed) under the frozen FU-B card (precedence rule 4: upper 95 % t bound of I1 < δ = 1.00 %).**

- **Question (card §1):** Is the r1 null explained by under-training? With 4× the training budget (`35,000 × 16 = 560,000` samples, ≈ 73.5 passes over the 7,616 training windows) at SwiFT ver11 E36 on HCP-YA REST1_LR, does grouping 12 mm stage-0 cells into connectome boxes at M0 (arm C), instead of PatchMergingV2's 2×2×2 cubes (arm E), lower held-out masked in-brain NMSE by at least δ = 1.00 %?
- **Practical claim, I1 = (NMSE_E − NMSE_C) / NMSE_E:**
  - Mean **+0.06 %** (`+0.063 %`), two-sided 95 % t interval **[−0.30 %, +0.42 %]** (`[−0.299 %, +0.425 %]`, df = 4, SE = `0.130 %`).
  - The upper 95 % t bound (`+0.425 %`) is strictly below δ = `1.00 %` (`I1_survives: false`).
  - Secondary hierarchical bootstrap (B = 10,000, seed 0): median `+0.06 %` (`+0.060 %`), 95 % interval **[−0.08 %, +0.34 %]** (`[−0.078 %, +0.338 %]`).
- **Connectome-specific claim, I2 = (NMSE_S − NMSE_C) / NMSE_S:**
  - Mean **−0.09 %** (`−0.092 %`), two-sided 95 % t interval **[−0.65 %, +0.46 %]** (`[−0.646 %, +0.461 %]`, df = 4, SE = `0.199 %`; `I2_lower_gt_0: false`).
  - Secondary hierarchical bootstrap: median `−0.09 %` (`−0.087 %`), 95 % interval **[−0.50 %, +0.23 %]** (`[−0.496 %, +0.228 %]`).
- **Gates (card §7):** The new 4× F+ measurement-capacity gate (`fplus_gate_4x`, job 509, seed 0) **passed** with C vs E gain **+3.73 %** and C vs S gain **+3.70 %** (both ≥ δ = 1.00 %). The inherited 1× F− bias gate (`fminus_inherited`) is certified `true` (`sha_ok: true`).
- **Manipulation check and stall structure (card §9):**
  - 4× training lowered seed-mean arm-E test NMSE relative to r1 (`0.98811` vs `0.98892`, `E_improved: true`), and lowered test NMSE in **13 of 15** `(arm, seed)` pairs (all 12 pairs on seeds 1–4 across arms E, C, S, plus `S_s0`).
  - Only 1 of 15 runs stalled (`E_s0`, test NMSE `1.00000`). On all four non-stalled seeds (seeds 1–4), arm E beat arm C (`I1` between `−0.05 %` and `−0.08 %`); the pre-registered non-governing sensitivity analysis dropping seed 0 (df = 3) gives **I1 = −0.07 % [−0.09 %, −0.04 %]** and verdict `stop`.
- **Pre-registered reading (card §11):** Within 4× the r1 budget under the same recipe, a practical gain ≥ 1 % of connectome boxes over PatchMergingV2 is excluded. The r1 null is not explained by under-training up to 560k samples at this target and model size.

---

## 1. Gate Results (`fplus_gate_4x` and `fminus_inherited`, card §7)

### 1.1 F+ measurement-capacity gate at the 4× budget (Slurm job 509)

Three runs on B300 (`b300-01`, Slurm job `509`, tasks `509_0..2`): synthetic F+ fixture stream, arms E, C, S at seed 0 (`perms_Fplus.npz` keys `E`, `C`, `S_seed0`), trained for the full FU-B budget of 35,000 steps × batch 16 (560k samples) and evaluated on 16 × 32 fixed synthetic windows (eval mask seed 7002). Output saved in `results/topic2/2026-11-02_fu_b/gate_4x.json` and embedded in `verdict.json["fplus_gate_4x"]`.

| gate run | budget | E test NMSE | C test NMSE | S test NMSE | gain C vs E | gain C vs S | rule (both ≥ 1.00 %) | state |
|---|---|---|---|---|---|---|---|---|
| **FU-B 4× F+ (seed 0)** | 35,000 × 16 (560k) | 0.65510 | **0.63069** | 0.65491 | **+3.73 %** (`+3.726 %`) | **+3.70 %** (`+3.699 %`) | pass (`True`) | **`pass`** |
| r1 1× F+ (seed 0, ref.) | 8,750 × 16 (140k) | 0.67693 | 0.65817 | 0.67783 | +2.77 % | +2.90 % | pass (`True`) | `pass` |
| r1 1× F+ (seeds 0–1 mean, ref.) | 8,750 × 16 (140k) | 0.67862 | 0.65785 | 0.67774 | +3.06 % | +2.93 % | pass (`True`) | `pass` |

- **Interpretation:** At 4× budget, all three arms achieve lower F+ NMSE than at 1× (`0.6551 / 0.6307 / 0.6549` vs `0.6786 / 0.6578 / 0.6777`), and arm C's relative gain over both E (`+3.73 %`) and S (`+3.70 %`) is larger than at 1× (`+3.06 %` and `+2.93 %`). Arm E does not catch up to arm C with 4× training when a genuine cell-level network signal is planted. Measurement capacity at 560k samples is certified (`state == "pass"`), so Stage 1 governs.

### 1.2 F− bias gate (`fminus_inherited`, card §7.2)

- Read from `results/topic2/2026-11-01/verdict.json` after verifying its sha256 against `DS.R1_VERDICT_SHA256` (`59af05e53239511b2b07462f38eb56bfa2d0e99efdec0568f0cef6e5c85caf68`): `sha_ok = true`, `pass = true` (1× budget, 140k samples, r1 seeds 0–1: C vs E `−1.74 %`, C vs S `+0.10 %`).
- Under card §7.2 and §8, `fminus_inherited` can only downgrade a would-be `keep` to `inconclusive`; because the FU-B verdict is `stop`, `fminus_inherited` does not affect the decision.

---

## 2. Stage-1 Results at 4× Budget (560k samples, 35,000 steps; card §8–§9)

All 15 Stage-1 runs (`hcp_{E,C,S}_s{0..4}_a1`, Slurm job `516`, tasks `516_0..14`) completed on `b300-01` and passed all record-validity checks (`missing: []`, `errors: []`, `order_ok: true`).

### 2.1 Per-seed test NMSE (16 test subjects × 60 windows, eval mask seed 7002)

| seed | E test NMSE | C test NMSE | S test NMSE | I1 = (E − C) / E | I2 = (S − C) / S | stalled (E / C / S) |
|---|---|---|---|---|---|---|
| 0 | 1.00000 (`1.000000`) | 0.99416 (`0.994161`) | 0.98601 (`0.986008`) | +0.58 % (`+0.584 %`) | −0.83 % (`−0.827 %`) | **y** / n / n |
| 1 | 0.98507 (`0.985070`) | 0.98559 (`0.985586`) | 0.98558 (`0.985581`) | −0.05 % (`−0.052 %`) | −0.00 % (`−0.001 %`) | n / n / n |
| 2 | 0.98555 (`0.985547`) | 0.98611 (`0.986106`) | 0.99000 (`0.989997`) | −0.06 % (`−0.057 %`) | +0.39 % (`+0.393 %`) | n / n / n |
| 3 | 0.98508 (`0.985077`) | 0.98590 (`0.985902`) | 0.98571 (`0.985713`) | −0.08 % (`−0.084 %`) | −0.02 % (`−0.019 %`) | n / n / n |
| 4 | 0.98486 (`0.984860`) | 0.98560 (`0.985602`) | 0.98551 (`0.985515`) | −0.08 % (`−0.075 %`) | −0.01 % (`−0.009 %`) | n / n / n |
| **mean** | **0.98811** (`0.988111`) | **0.98747** (`0.987472`) | **0.98656** (`0.986563`) | **+0.06 %** (`+0.063 %`) | **−0.09 %** (`−0.092 %`) | 1 / 0 / 0 |

Absolute differences in seed-mean test NMSE:
- `NMSE_E − NMSE_C = +0.00064` (`+0.000639`)
- `NMSE_S − NMSE_C = −0.00091` (`−0.000909`)

### 2.2 Primary t-intervals (df = 4) and secondary hierarchical bootstrap (B = 10,000, seed 0)

| contrast | mean | SE | 95 % t interval (df = 4) | hierarchical bootstrap 95 % (median) | threshold | decision |
|---|---|---|---|---|---|---|
| **I1 (C vs E, practical)** | **+0.06 %** (`+0.063 %`) | 0.130 % | **[−0.30 %, +0.42 %]** (`[−0.299 %, +0.425 %]`) | **[−0.08 %, +0.34 %]** (`[−0.078 %, +0.338 %]`; med `+0.060 %`) | δ = +1.00 % | **`stop`** (`hi < δ`) |
| **I2 (C vs S, specificity)** | **−0.09 %** (`−0.092 %`) | 0.199 % | **[−0.65 %, +0.46 %]** (`[−0.646 %, +0.461 %]`) | **[−0.50 %, +0.23 %]** (`[−0.496 %, +0.228 %]`; med `−0.087 %`) | > 0 | `lo ≤ 0` (`false`) |

### 2.3 Validation learning curves (8 val subjects × 60 windows, eval mask seed 7001; health check)

Seed-mean validation NMSE at the four quarter checkpoints (`25 % / 50 % / 75 % / 100 %` of 35,000 steps):

| arm | step 8,750 | step 17,500 | step 26,250 | step 35,000 |
|---|---|---|---|---|
| **E** (5-seed mean) | 0.9916 | 0.9907 | 0.9903 | 0.9903 |
| **C** (5-seed mean) | 0.9916 | 0.9910 | 0.9908 | 0.9898 |
| **S** (5-seed mean) | 0.9908 | 0.9893 | 0.9890 | 0.9890 |

Per-run validation NMSE curves (`verdict.json["stage1"]["val_curves"]`):

| run | step 8,750 | step 17,500 | step 26,250 | step 35,000 | final train loss (last 100) | stalled (≥ 0.999 all 4) |
|---|---|---|---|---|---|---|
| `hcp_E_s0_a1` | 1.00001 | 1.00000 | 1.00000 | 1.00000 | 1.00174 | **True** |
| `hcp_E_s1_a1` | 0.98858 | 0.98814 | 0.98791 | 0.98792 | 0.97599 | False |
| `hcp_E_s2_a1` | 0.99242 | 0.98946 | 0.98826 | 0.98817 | 0.98167 | False |
| `hcp_E_s3_a1` | 0.98897 | 0.98800 | 0.98786 | 0.98784 | 0.97612 | False |
| `hcp_E_s4_a1` | 0.98821 | 0.98804 | 0.98765 | 0.98768 | 0.97295 | False |
| `hcp_C_s0_a1` | 1.00001 | 1.00000 | 1.00000 | 0.99521 | 0.99702 | False |
| `hcp_C_s1_a1` | 0.98897 | 0.98848 | 0.98824 | 0.98821 | 0.97737 | False |
| `hcp_C_s2_a1` | 0.99072 | 0.98893 | 0.98866 | 0.98858 | 0.98083 | False |
| `hcp_C_s3_a1` | 0.98928 | 0.98840 | 0.98860 | 0.98847 | 0.97580 | False |
| `hcp_C_s4_a1` | 0.98890 | 0.98902 | 0.98833 | 0.98829 | 0.97535 | False |
| `hcp_S_s0_a1` | 0.98942 | 0.98879 | 0.98867 | 0.98857 | 0.97802 | False |
| `hcp_S_s1_a1` | 0.99070 | 0.98850 | 0.98825 | 0.98820 | 0.98260 | False |
| `hcp_S_s2_a1` | 0.99446 | 0.99209 | 0.99177 | 0.99163 | 0.98776 | False |
| `hcp_S_s3_a1` | 0.99006 | 0.98861 | 0.98833 | 0.98829 | 0.97970 | False |
| `hcp_S_s4_a1` | 0.98940 | 0.98862 | 0.98818 | 0.98814 | 0.97796 | False |

### 2.4 Stalls and pre-registered stall sensitivity (card §9, non-governing)

- **Stall criterion (card §9):** val NMSE ≥ `0.999` at all four validation checkpoints (`8,750`, `17,500`, `26,250`, `35,000`).
- **Observed stalls (`stall_flags`):** Exactly 1 of 15 runs stalled (`E_s0: true`; all other 14 runs `false`). Notably, `C_s0` stayed near `1.00000` through step 26,250 before escaping in the last quarter (`0.99521` at step 35,000), while `S_s2` (which had stalled throughout r1's 8,750 steps) already escaped by step 8,750 (`0.99446`) and finished at `0.99163` val / `0.99000` test.
- **Pre-registered sensitivity (`stall_sensitivity`, dropping seed 0 → `seeds_kept = [1, 2, 3, 4]`, df = 3):**
  - **I1 (C vs E):** mean **−0.07 %** (`−0.067 %`), SE `0.0075 %`, 95 % t interval **[−0.09 %, −0.04 %]** (`[−0.091 %, −0.043 %]`).
  - **I2 (C vs S):** mean **+0.09 %** (`+0.091 %`), SE `0.101 %`, 95 % t interval **[−0.23 %, +0.41 %]** (`[−0.229 %, +0.412 %]`).
  - **`verdict_if_governing`: `stop`.**
  - **Reading:** Without the stalled seed 0, the seed-to-seed spread of I1 collapses (SE `0.0075 %`), and arm C is slightly *worse* than PatchMergingV2 on every remaining seed (`−0.052 %`, `−0.057 %`, `−0.084 %`, `−0.075 %`). The positive sign of the 5-seed primary mean (`+0.06 %`) is an artifact of `E_s0` stalling while `C_s0` escaped late.

---

## 3. Paired Comparison with r1 (`r1_pairing`, card §9)

Every FU-B seed shares the initial weights, window-order stream (`1000 + s`), training-mask stream (`2000 + s`), partition, split, and evaluation masks with the corresponding r1 seed; the first 140k samples of FU-B are identical to r1's except for the stretched learning-rate schedule (1,750-step warmup and 35,000-step cosine decay vs r1's 438-step warmup and 8,750-step decay). `same_test_order_as_r1` is `true` across all 15 runs.

### 3.1 Manipulation check (card §9)

- **Seed-mean arm E test NMSE:** r1 (1×, 140k samples) = **`0.98892`** (`0.988922`) → FU-B (4×, 560k samples) = **`0.98811`** (`0.988111`), difference `−0.00081`, **`E_improved = true`**.
- On the four non-stalled seeds (seeds 1–4), seed-mean arm E test NMSE dropped from `0.98844` in r1 to `0.98514` in FU-B (`−0.00330`), increasing explained masked variance `1 − NMSE` from `1.16 %` to `1.49 %` (+28 % relative).

### 3.2 Per-(arm, seed) test NMSE change (`FU-B − r1`) and per-seed `ΔI1`

| seed | E (r1 → FU-B) | ΔNMSE_E | C (r1 → FU-B) | ΔNMSE_C | S (r1 → FU-B) | ΔNMSE_S | I1_r1 | I1_FU-B | ΔI1 (FU-B − r1) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.99087 → 1.00000 | +0.00913 | 0.98855 → 0.99416 | +0.00562 | 0.99096 → 0.98601 | −0.00495 | +0.23 % (`+0.235 %`) | +0.58 % (`+0.584 %`) | **+0.35 %** (`+0.349 %`) |
| 1 | 0.98759 → 0.98507 | −0.00251 | 0.98690 → 0.98559 | −0.00131 | 0.98982 → 0.98558 | −0.00424 | +0.07 % (`+0.069 %`) | −0.05 % (`−0.052 %`) | **−0.12 %** (`−0.122 %`) |
| 2 | 0.99262 → 0.98555 | −0.00707 | 0.98862 → 0.98611 | −0.00251 | 1.00000 → 0.99000 | −0.01000 | +0.40 % (`+0.403 %`) | −0.06 % (`−0.057 %`) | **−0.46 %** (`−0.460 %`) |
| 3 | 0.98669 → 0.98508 | −0.00162 | 0.98704 → 0.98590 | −0.00114 | 0.98949 → 0.98571 | −0.00378 | −0.03 % (`−0.035 %`) | −0.08 % (`−0.084 %`) | **−0.05 %** (`−0.049 %`) |
| 4 | 0.98685 → 0.98486 | −0.00199 | 0.98623 → 0.98560 | −0.00063 | 0.99060 → 0.98551 | −0.00509 | +0.06 % (`+0.062 %`) | −0.08 % (`−0.075 %`) | **−0.14 %** (`−0.137 %`) |
| **mean** | 0.98892 → 0.98811 | −0.00081 | 0.98747 → 0.98747 | +0.00000 | 0.99218 → 0.98656 | −0.00561 | +0.15 % (`+0.147 %`) | +0.06 % (`+0.063 %`) | **−0.08 %** (`−0.084 %`) |

- **13 of 15 pairs improved with 4× budget:** Every seed 1–4 run across all three arms E, C, S (12/15 runs) and `S_s0` (total **13/15** runs) achieved strictly lower test NMSE at 560k samples than at 140k samples. The only 2/15 pairs where FU-B had higher test NMSE than r1 are `E_s0` (`+0.00913`, stalled at `1.00000`) and `C_s0` (`+0.00562`, late plateau escape at `0.99416`), reflecting sensitivity of early plateau escape on seed 0 to the longer warmup/decay schedule (card §2 limitation).
- **Why I1 did not grow with budget:** In r1 (1×), arm E and arm S suffered slower plateau escape than arm C on several seeds (e.g., `E_s2` at `0.99262`, `S_s2` stalled at `1.00000`), creating a small positive point estimate for I1 (`+0.147 %`) and I2 (`+0.473 %`). With 4× training, once E and S escape the plateau and converge on seeds 1–4, E slightly outperforms C (`0.98486–0.98555` vs `0.98559–0.98611`) and S matches C (`0.98551–0.98601`). Thus the small 1× advantage of C was a transient plateau-escape effect, not an asymptotic capacity advantage.

---

## 4. Implementation, Unit Tests, and Mutation Coverage (F2)

- **Code and reuse (`src/topic2_fu_b/`, `scripts/topic2fu_b_*.py`):**
  - Training and statistical primitives are imported unchanged from the frozen r1 package `src/topic2_rgpool` (all 13 Python modules verified equal to `results/topic2/2026-11-01/code_sha256_at_freeze.txt` on disk and in every `run.json["code_sha256"]`).
  - `src/topic2_fu_b/verdict.py` and `records.py` implement the FU-B precedence table (card §8) and strict record validation, explicitly closing the r1 verdict-script defect classes documented in `.agents/teamwork/tw-20261031-four-topics/orchestrator/M3_r2_gate_record.json` (`challenger_M3_r2_2` V01–V11, case A):
    1. Missing or invalid F+ gate returns `no_verdict` (rule 1), never `pass`.
    2. Failed F+ gate returns `inconclusive` (rule 2: measurement capacity), never `no_verdict`, even when Stage 1 is absent, and never reads Stage 1 when present.
    3. Incomplete Stage 1, failed/aborted runs, duplicate valid attempts, wrong-budget (`steps != 35000`) records, code/partition/split hash drift, or test-order mismatch returns `no_verdict` (rule 3).
    4. Inherited F− requires sha-verified `verdict.json` and literal `True`, and only downgrades `keep` (never `modify` or `stop`).
    5. Exact card boundary operators (`hi < delta` for `stop`, `mean >= delta` and `lo > 0` for `keep`/`modify`).
- **Test suite (`tests/topic2_fu_b/`):** 128 unit tests (all passing on CPU in ~3.2 s), plus a cross-check test (`test_wiring_reproduces_r1_verdict_on_r1_records`) verifying that with r1's parameters patched in, the FU-B verdict wiring reproduces the shipped r1 `verdict.json` (`I1_t`, `I2_t`, `hier_bootstrap`, `Fplus` gate, and `stop` verdict) exactly.
- **Mutation testing (`verification/worker_FU_B_r1/mutation/mutants_v2.out.json`):** 44 targeted mutants across `verdict.py`, `records.py`, `budget.py`, `view.py`, `slurm.py`, `design.py`, and `topic2fu_b_run.py` — **44/44 killed (100 %)**, 0 survived, 0 errors.

---

## 5. Compute, Slurm, and GPU Ledger Accounting (C5) & Data Governance (C4, C6)

### 5.1 Slurm execution and GPU-hour accounting (cap 33.0 GPU-h)

Every B300 GPU job was submitted via `sbatch` to node `b300-01` (`61.107.201.98`), with copies of the rendered scripts stored in `results/topic2/2026-11-02_fu_b/slurm/` and job state tracked in `results/topic2/2026-11-02_fu_b/slurm/jobs.json`. Every submission and task completion was recorded under flock in `results/gpu_ledger_2026-10-31.md` using `TZ=UTC sacct` `ElapsedRaw` rounded up to 0.01 GPU-h.

| phase / agent | Slurm job(s) | tasks × GPUs | wall time (`ElapsedRaw`) | GPU-h | status |
|---|---|---|---|---|---|
| `explorer_FU_B_r1_1` | `413` (`debug`) | 1 × 1 GPU | 231 s | 0.065 | COMPLETED |
| `explorer_FU_B_r1_2` | `402` (`debug`) | 1 × 1 GPU | 198 s | 0.060 | COMPLETED |
| `explorer_FU_B_r1_3` | `419` (`debug`) | 1 × 1 GPU | 52 s | 0.015 | COMPLETED |
| `worker_FU_B_r1` pre-freeze smoke | `490` (`debug`) | 1 × 1 GPU | 234 s | 0.070 | COMPLETED |
| `worker_FU_B_r1` 4× F+ gate | `509` (`0-2`, `gpu`) | 3 × 1 GPU | 6,056–6,076 s | 5.070 (`3 × 1.69`) | COMPLETED (`3/3`) |
| `worker_FU_B_r1` Stage 1 | `516` (`0-14%4`, `gpu`) | 15 × 1 GPU | 6,058–6,109 s | 25.440 (`6 × 1.69 + 9 × 1.70`) | COMPLETED (`15/15`) |
| **FU-B total** | | **22 tasks** | | **30.720 GPU-h** | **≤ 33.0 GPU-h cap** |

- **Zero failures or reruns:** All 18 post-freeze training tasks (`509_0..2` and `516_0..14`) succeeded on attempt 1 (`_a1`).
- **B300-share rule and administrative hold window (`GATE_STATUS.md`):**
  - Before every `sbatch` submission (`490`, `509`, `516`), `squeue` was checked by `scripts/topic2fu_b_slurm.py preflight`; no `g3t-G-E0-*` job was pending or running at submission (`g3t_blockers: []`).
  - At `2026-11-01T22:52:35Z` (~07:50 KST), while `516_0..7` were completed and `516_8..11` were running on `b300-01`, the root coordinator placed an administrative Slurm hold (`JobHeldAdmin`) on pending tasks `516_[12-14]` under the ACCEPTANCE C5 B300-share rule to yield cluster capacity to `g3t-G-E0` jobs (`588` and `589`) on `b300-04`.
  - After job `588` completed and job `589` was moved to `QOS=whole`, root released `516_[12-14]` by `2026-11-01T23:57Z` (~08:55 KST). Tasks `516_12..14` started at `2026-11-02T00:23:34Z–00:26:52Z` as `516_8..10` freed slots under the `%4` throttle, and completed at `2026-11-02T02:04:37Z–02:08:39Z`.

### 5.2 Data and identifier governance (C4, C6)

- **C6 (HCP-YA Open Access):** Preprocessed HCP-YA S1200 Open Access REST1_LR tensors on `b300-01` (`/scratch/iitp4/worker_M3_r1/hcp`, 88 subjects; 5 explorer development subjects excluded by r1) were accessed read-only under PI decision 2. No subject tensor or model checkpoint (`model_final.pt`) was copied off B300.
- **C4 (Positional view and leak scans):**
  - Training read HCP tensors exclusively through the positional hard-link view `/scratch/iitp4/fu_b/hcp/subjects/hNN/` created by `scripts/topic2fu_b_make_view.py`. Preconditions recorded in `results/topic2/2026-11-02_fu_b/b300/view_check.json`: `n_orig = 88`, `sanitized_manifest_is_positional_in_order = true`, train/val/test split lists identical to repo `results/topic2/2026-11-01/split.json` (`64 / 8 / 16`, `disjoint = true`), `r1_files_modified_after_cut = 0`, `links_made = 176`, `links_conflicting = 0`.
  - Every HCP `run.json` contains only positional `hNN` labels (`h13..h85`) in `test_pseudonyms`.
  - On B300, `scripts/topic2fu_b_c4scan.py` scanned all 108 text files in `/scratch/iitp4/fu_b/{runs,logs,smoke}` against the 176 in-memory r1 manifest tokens (`pseudonym` and `content_sha256`): **`n_hits = 0`, `n_files_with_hits = 0`** (`results/topic2/2026-11-02_fu_b/b300/c4_scan_b300.json`).
  - Note on `topic2fu_b_slurm.py sync` console output: `sync` prints a diagnostic counter `standalone_16hex_strings` using the unquoted character class `[0-9a-f]{16}`, which matches 16-digit decimal fractional parts of standard IEEE-754 floats (e.g., `1.0000091020588155` after `.`) in `train_log.jsonl` and `run.json`. Zero hex identifier tokens exist in `results/topic2/2026-11-02_fu_b/`, as verified by `c4_scan_b300.json` (`n_hits = 0`) and `tests/topic2_rgpool/test_outputs_no_ids.py`.

---

## 6. Deviations, Limitations, and Reproduction

### 6.1 Deviations and operational notes

1. **Pre-run card wording fix (`2026-11-02_topic2_fu_b_addendum_01.md`):** Before any FU-B gate or Stage-1 task started (`509` and `516` still PENDING at `16:19:52Z`), one hyphenated English word in card §2 was replaced with `"not be optimal"` so that `tests/topic2_rgpool/test_outputs_no_ids.py`'s BIDS-prefix detector stays green, and the card was re-frozen as `card_sha256_v2.txt` at `16:20:25Z` (v1 bytes preserved in `verification/worker_FU_B_r1/card_v1_frozen_20261101T160518Z.md.txt`).
2. **Operational waits (no design impact):** The root-administered B300-share hold on `516_[12-14]` (`22:52:35Z–23:57Z`) and the worker session continuation after a transient API rate limit (`01:55:36Z`, while `516_12..14` finished normally on B300 by `02:08:39Z`) required no rerun and altered no file or parameter.

### 6.2 Limitations (card §13)

- **Recipe not re-tuned for 4×:** Peak learning rate (`2e-4`), warmup fraction (`5 % = 1,750` steps), and cosine decay shape were held fixed to isolate the training budget. As seen on seed 0 (`E_s0` stalled, `C_s0` escaped late), the 1,750-step warmup can delay or prevent escape from the predict-zero plateau on individual seeds.
- **Single-seed 4× F+ gate and inherited 1× F− gate:** Chosen to fit within the 33.0 GPU-h cap alongside the 15 Stage-1 runs (`30.72 GPU-h` total).
- **Sample size and scope:** Five seeds (`df = 4`, `t_crit = 2.776`) on a fixed 16-subject test split, one model scale (`E36_d2262`, 38.7M parameters), and one high-noise reconstruction target (2 mm voxel z-scored BOLD, where test NMSE is `0.985–0.990`). With 64 training subjects (7,616 windows), 560k samples correspond to ≈ 73.5 passes over the same subjects.
- **HCP family structure:** Restricted data unavailable; relatives may straddle splits (as in r1).

### 6.3 Reproduce and verify

```bash
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_b_verdict.py results/topic2/2026-11-02_fu_b/b300/runs /tmp/fub_verdict_check.json
cmp -s results/topic2/2026-11-02_fu_b/verdict.json /tmp/fub_verdict_check.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_b tests/topic2_rgpool -q
```
