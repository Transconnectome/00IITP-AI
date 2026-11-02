# Handoff — `numbers_audit_report` (`paper-numbers-auditor`)

- **Run ID**: `tw-20261031-four-topics`
- **Workflow / Phase**: Workflow C, Phase `Report`
- **Target Document**: `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` (`sha256 = 6b74f4645d66ba9751ab9c9ce110186f4f5caaf563fab26c6a32b4a9d5965e8a`)
- **Audit Script & Output**:
  - `verification/numbers_audit_report/audit_numbers.py`
  - `verification/numbers_audit_report/audit_numbers.out.json`
- **Verdict**: **`REQUEST_CHANGES`**

---

## 1. Observation

We performed an exhaustive, programmatic read-only audit (`308` individual numeric checks + C1, C4, and C8 compliance checks in `verification/numbers_audit_report/audit_numbers.py`) comparing every result number in `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` against the canonical dated result files under `results/`, `docs/03_empirical_analysis/topic{1,2,3,4}/`, and `results/gpu_ledger_2026-10-31.md`:

- **Passing Sections (`279 / 308` numeric checks)**:
  - **Executive Summary Table (§1.2)** and **Milestone Verdicts**: All 10 milestone verdicts (`M1`, `M3`, `FU_A`..`FU_E`, `M2`, `M2H2`, `M4`), card SHA-256 digests, and primary headline statistics match the canonical JSONs.
  - **Topic 1 (`M1`, §2.1–§2.5)**: Sample counts (`N = 1,706`, `OCD = 843`, `HC = 863`, `17` sites, `1,192` TR=2.0s / `514` TR≠2.0s), primary endpoints `E1` (`d = 0.088766`, `[-0.008568, +0.186100]`, `p_FL = 0.0680`, `p_Holm = 0.1360`, `p_BF = 0.7289`) and `E2` (`d = 0.049307`, `[-0.048009, +0.146624]`, `p_FL = 0.3037`, `p_Holm = 0.3037`, `p_BF = 0.3547`), sensitivity analyses `S1–S4`, and secondary families `Family 1–3` and `acceptance_stratified_secondary` all match `results/topic1/2026-10-31/stats_results.json` — **except** the two raw group means `mean_ocd` and `mean_hc` in `log_ratio_030C_secondary` on line 69 (`[BLOCKING-1]`).
  - **Topic 2 (`M3` + `FU-A`..`FU-E`, §3.1–§3.8)**: 100% of audited numbers across Stage-0 (`stage0_hcp.json`), `M3` (`verdict.json`, `posthoc_sensitivity_without_seed2.json`), `FU-A` (`verdict.json`, `design_stats_train.json`), `FU-B` (`verdict.json`, `gate_4x.json`), `FU-C` (`verdict.json`), `FU-D` (`verdict.json`, `runs/Fplus_{E,C,S}_s0/run.json`), and `FU-E` (`verdict.json`, `run_524/extract.json`) match the canonical result files.
  - **Topic 3 (`M2` + `M2H2`, §4.1–§4.5)**: `T3.1` provenance numbers (`t3_1_provenance_repro.json`), Family A primary contrasts `D1`/`R1`/`D3` point estimates & CIs, Family B token-level `H1a`/`H1b` and `A1b` across all 4 checkpoints (`family_B_token_level.json`), and `M2H2` Gate G (`gate_decision.json`) and Family C (`C1–C4` in `h2_results.json`) all match — **except** three sets of numbers in §4.4–§4.5 (`[BLOCKING-2]`, `[BLOCKING-3]`, `[BLOCKING-4]`).
  - **Topic 4 (`M4`, §5.1–§5.8)**: 100% of audited numbers (`N_total = 1,706`, `N_eligible = 1,195`, `N_tune = 181`, `N_confirm = 1,014`, `H1`, `S1–S3`, sensitivities 1–4, all 16 descriptive rows in Table 5.5b, `C3` instability `10/50 = 20.0%`, and Spearman `rho = 0.2804`) match `results/topic4/2026-11-01/verdict.json`, `split_manifest.json`, `tuning.json`, and `t41_PositionZeroRootCause.json`.
  - **GPU Ledger (§6.1)**: All 10 milestone GPU-h totals (`M1 = 0.000`, `M2 = 0.000`, `M3 = 11.990`, `FU_A = 0.952`, `FU_B = 30.720`, `FU_C = 10.697`, `FU_D = 3.720`, `FU_E = 0.330`, `M2H2 = 0.891`, `M4 = 0.000`, Grand Total = `59.300 GPU-h`, B300 = `58.409 GPU-h`, `connectome` = `0.891 GPU-h`) match `results/gpu_ledger_2026-10-31.md`.
  - **C1 & C4 Hygiene**: `PROTECTED_HASHES.txt` is `67/67 OK` (`c1_protected_hashes.pass = true`), and `2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` has `0` BIDS subject prefix hits, `0` 6-digit HCP subject ID hits, and `0` unsalted 16-hex content hashes (`c4_hygiene.pass = true`).
- **Failing Checks (`29 / 308` numeric checks across 4 blocking locations)**:
  1. **`[BLOCKING-1]` Topic 1 (`M1`), §2.5 Table Row 5 (Line 69) — `log_ratio_030C_secondary` raw group means**:
     - Line 69 reports `유의하지 않음 (OCD -0.0876, HC -0.1096)` citing `results/topic1/2026-10-31/stats_results.json` (`log_ratio_030C_secondary`).
     - In `results/topic1/2026-10-31/stats_results.json::log_ratio_030C_secondary`, the canonical values are `mean_ocd = -0.20196210022524988` (`-0.2020`, `sd_ocd = 0.534402`) and `mean_hc = -0.2224420398689146` (`-0.2224`, `sd_hc = 0.541526`). Neither `-0.0876` nor `-0.1096` appears anywhere in `results/topic1/` or `docs/03_empirical_analysis/topic1/`.
  2. **`[BLOCKING-2]` Topic 3 (`M2`), §4.5 Table 4.5a `L0–L3` rows (Lines 256–259) — Column-permutation null means, unsupported upper quantiles, and `L1` LOO `pr_cov`**:
     - Lines 256–259 cite `results/topic3/2026-10-31/family_A_subject_level.json` (`results.E1_full.{L0,L1,L2,L3}`) and `2026-10-31_topic3_addendum_03.md` (§3), but report mismatched `colperm_null_mean` values and fabricated upper quantiles (the JSON only stores `colperm_null_mean` and `colperm_null_q025`, not `colperm_null_q975`):
       - `L0` (line 256): reports `47.57 ([44.77, 49.70])` vs canonical `colperm_null_mean = 45.431155` (`45.43`), `colperm_null_q025 = 44.770852` (`44.77`); `49.70` is not in the JSON.
       - `L1` (line 257): reports `51.24 ([49.30, 52.54])` and `pr_cov = 6.3941, SE 0.1489` vs canonical `colperm_null_mean = 50.071502` (`50.07`), `colperm_null_q025 = 49.295610` (`49.30`); `52.54` is not in the JSON. And in `verification/worker_M2_r2/probes/probe_addendum03_numbers.out.json::l1_jackknife` and `2026-10-31_topic3_addendum_03.md` §3 line 56, removing the single outlier yields `max_loo_pr = 6.389793` (`6.3898` / `6.39`, NOT `6.3941`) and `se_without_most_influential_term = 0.148827` (`0.1488` / `0.149`).
       - `L2` (line 258): reports `54.16 ([53.61, 54.61])` vs canonical `colperm_null_mean = 53.755928` (`53.76`), `colperm_null_q025 = 53.613377` (`53.61`); `54.61` is not in the JSON.
       - `L3` (line 259): reports `53.80 ([52.97, 54.44])` vs canonical `colperm_null_mean = 53.208105` (`53.21`), `colperm_null_q025 = 52.974145` (`52.97`); `54.44` is not in the JSON.
  3. **`[BLOCKING-3]` Topic 3 (`M2`), §4.5 Table 4.5a `D3` row (Line 263) & §4.4 Table `R3` row (Line 246) — `A2_matched25` $m=12$ `covPR` means and ratios**:
     - Line 263 reports `$m=12$ covPR: LM 4.38, JEPA 6.46, STORM 7.74` citing `results.A2_matched25`.
     - In `results/topic3/2026-10-31/family_A_subject_level.json::results.A2_matched25`, the canonical `subsample_m12_mean_pr_cov` values are:
       - `BrainLM`: `4.395156` (`4.40`, `corr = 6.727932` [`6.73`]) — NOT `4.38`.
       - `BrainJEPA`: `6.479072` (`6.48`, `corr = 8.454744` [`8.45`]) — NOT `6.46`.
       - `NeuroSTORM`: `7.757782` (`7.76`, `corr = 9.450973` [`9.45`]) — NOT `7.74`.
     - Furthermore, on line 246 (`R3` row), the report writes `($1.48\times, 1.77\times$)`, whereas `2026-10-31_topic3_result_report.md` §2 line 89 reports the matched-$n=25$ full-subset ratios `1.8x` (`9.6595 / 5.3563 = 1.803x`) and `2.3x` (`12.5070 / 5.3563 = 2.335x`), and the $m=12$ ratios are `6.479072 / 4.395156 = 1.474x` (`1.47x`, not `1.48x`) and `7.757782 / 4.395156 = 1.765x` (`1.77x`).
  4. **`[BLOCKING-4]` Topic 3 (`M2H2`), §4.5c Family L bullets (Lines 286–287) — 19 mismatched/fabricated numbers in `E1_per_arm`, `family_L.subject`, and `family_L.token`**:
     - Line 286 (`family_L.subject` & `E1_per_arm`):
       - Reports random-init `R1..R10` full-sample ($n=57$) centered `pr_cov` at `L1` as `30.50–32.22`. In `results/topic3/2026-11-02_h2/h2_results.json::E1_per_arm.R1..R10.L1.pr_cov` (and `2026-11-02_topic3_h2_result_report.md` §4.3 line 117), the canonical range is **`17.6128–20.8686` (`17.6–20.9`)**, NOT `30.50–32.22`.
       - Reports $m=28$ log-ratios $\log(\text{PR}_T / \text{PR}_R)$ in `family_L.subject` that do not match `h2_results.json::family_L.subject`:
         - `L1_cov`: reported `-1.692` vs canonical **`-1.424`** (`-1.424138`, 95% CI `[-2.441307, -0.406968]`)
         - `L1_corr`: reported `-1.367` vs canonical **`-1.049`** (`-1.048954`, 95% CI `[-1.829319, -0.268590]`)
         - `L2_cov`: reported `-0.961` vs canonical **`-0.869`** (`-0.869467`, 95% CI `[-1.185057, -0.553877]`)
         - `L2_corr`: reported `-0.785` vs canonical **`-0.706`** (`-0.705903`, 95% CI `[-0.946812, -0.464994]`)
         - `LN0L2_cov`: reported `-0.962` vs canonical **`-0.872`** (`-0.871963`, 95% CI `[-1.203182, -0.540745]`)
         - `LN0L2_corr`: reported `-0.783` vs canonical **`-0.703`** (`-0.703328`, 95% CI `[-0.955276, -0.451381]`)
         - `L3_cov`: reported `-1.970` vs canonical **`-1.839`** (`-1.838732`, 95% CI `[-2.086945, -1.590519]`)
         - `L3_corr`: reported `-1.766` vs canonical **`-1.549`** (`-1.548669`, 95% CI `[-1.769191, -1.328146]`)
     - Line 287 (`family_L.token`):
       - Reports 9 token-level log-ratios (and `L0_corr` verdict/sign) that contradict `h2_results.json::family_L.token` and `2026-11-02_topic3_h2_result_report.md` §4.2 Table (lines 95–108):
         - `L1_cov`: reported `-0.556 [-0.577, -0.533]` vs canonical **`-0.2770 [-0.2932, -0.2599]`** (`point = -0.276989`, `ci95 = [-0.293222, -0.259873]`, `verdict = TE-`)
         - `L1_corr`: reported `-0.194 [-0.205, -0.181]` vs canonical **`-0.3055 [-0.3180, -0.2919]`** (`point = -0.305454`, `ci95 = [-0.317970, -0.291881]`, `verdict = TE-`)
         - `L2_cov`: reported `-0.0004` (`INC`) vs canonical **`-0.1002 [-0.1040, -0.0963]`** (`point = -0.100190`, `p_Holm = 0.001`, `verdict = INC` because `ci95` straddles `-delta = -0.09531` and `max_over_seeds = -0.0906 > -delta`)
         - `L2_corr`: reported `-0.025` (`EQ`) vs canonical **`-0.0745 [-0.0771, -0.0716]`** (`point = -0.074487`, `ci90 = [-0.076711, -0.072115]`, `verdict = EQ`)
         - `LN0L2_cov`: reported `-0.0020` (`INC`) vs canonical **`-0.0754 [-0.0791, -0.0717]`** (`point = -0.075422`, `verdict = INC` because `max_abs_over_seeds = 0.09778 >= delta = 0.09531`)
         - `LN0L2_corr`: reported `-0.027` (`EQ`) vs canonical **`-0.0556 [-0.0582, -0.0529]`** (`point = -0.055587`, `ci90 = [-0.057805, -0.053383]`, `verdict = EQ`)
         - `L3_cov`: reported `+0.029` (wrong sign & value, `EQ`) vs canonical **`-0.0707 [-0.0743, -0.0670]`** (`point = -0.070659`, `ci90 = [-0.073698, -0.067617]`, `verdict = EQ`)
         - `L3_corr`: reported `-0.015` (`EQ`) vs canonical **`-0.0431 [-0.0456, -0.0406]`** (`point = -0.043138`, `ci90 = [-0.045232, -0.041010]`, `verdict = EQ`)
         - `L0_corr`: reported `+0.013 (p_Holm = 0.0149)` (wrong sign, value, and p-value) vs canonical **`-0.0091 [-0.0161, -0.0013]`** (`point = -0.009137`, `ci90 = [-0.015016, -0.002657]`, `p_perm = 0.0124`, `p_Holm = 0.0124`, `verdict = EQ`)

---

## 2. Logic Chain

1. Per `workflow_C_script.js.txt` line 149, `numbers_audit_report` must extract every result number in `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md`, check it against the canonical dated result files under `results/` and `docs/03_empirical_analysis/topic*/`, and return `APPROVE` **only if zero unsupported, mismatched, or C8-forbidden numbers exist**; otherwise return `REQUEST_CHANGES` with the complete list in `blocking_issues`.
2. While Topic 2 (`M3`, `FU-A`..`FU-E`), Topic 4 (`M4`), and the GPU Ledger (§6.1) have zero numerical discrepancies, Topic 1 (§2.5 line 69) and Topic 3 (§4.4 line 246, §4.5 lines 256–259, 263, 286–287) contain `29` concrete numerical mismatches against their cited JSON sources (`stats_results.json`, `family_A_subject_level.json`, `probe_addendum03_numbers.out.json`, and `h2_results.json`), including sign inversions (`L3_cov` and `L0_corr` in `family_L.token`), wrong cell-classification explanations (`L2_cov` and `LN0L2_cov` in `family_L.token` are `INC`, whereas `L0_corr` is `EQ`), and fabricated numbers that do not exist in the JSONs (likely hallucinated when the writer summarized variables that were not printed in full in the topic result reports).
3. Therefore, `REQUEST_CHANGES` is mandatory until those 4 locations in `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` are corrected to match the canonical JSON values.

---

## 3. Caveats

- All primary milestone verdicts (`stop` / `inconclusive` / `keep` / `TE+` / `TE-` / `EQ` / `INC`) at the milestone level remain unchanged when these 29 secondary/descriptive cell numbers are corrected, EXCEPT that within Topic 3 `M2H2` `family_L.token` (line 287), the report also misstates which two cells are `INC` besides `L0_cov`: in `h2_results.json::family_L.token`, the 8 `EQ` cells are `L0_corr`, `L2_corr`, `LN0L2_corr`, `L3_cov`, `L3_corr` (Wait: `L0_corr`, `L2_corr`, `LN0L2_corr`, `L3_cov`, `L3_corr` = 5 `EQ` cells! And `L0_cov`, `L2_cov`, `LN0L2_cov` = 3 `INC` cells, plus `L1_cov`, `L1_corr` = 2 `TE-` cells; total = 10 token cells!). Let us note this explicitly so `report_writer` fixes the counts (`2 TE-`, `5 EQ`, `3 INC`) as well as the numbers on line 287.

---

## 4. Conclusion

**Verdict: `REQUEST_CHANGES`**.
`report_writer` must update lines 69, 246, 256–259, 263, and 286–287 of `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` using the exact canonical values listed in `blocking_issues` below.

---

## 5. Verification Method

Run:
```bash
/home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers.py
```
and inspect `/home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers.out.json`.

```json
{
  "agent": "numbers_audit_report",
  "role": "paper-numbers-auditor",
  "milestone": "Report",
  "verdict": "REQUEST_CHANGES",
  "c1_protected_hashes_ok": true,
  "c4_hygiene_ok": true,
  "c8_compliance_ok": false,
  "total_numeric_checks": 308,
  "passed_numeric_checks": 279,
  "failed_numeric_checks": 29,
  "blocking_issues": [
    {
      "id": "BLOCKING-1",
      "location": "docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md:69 (§2.5 Table, row 5 `log_ratio_030C_secondary`)",
      "reported": "OCD -0.0876, HC -0.1096",
      "canonical": "mean_ocd = -0.2020 (-0.201962, SD 0.534402), mean_hc = -0.2224 (-0.222442, SD 0.541526)",
      "source": "results/topic1/2026-10-31/stats_results.json::log_ratio_030C_secondary",
      "required_fix": "Replace `OCD -0.0876, HC -0.1096` with `OCD -0.2020 (SD 0.5344), HC -0.2224 (SD 0.5415)`."
    },
    {
      "id": "BLOCKING-2",
      "location": "docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md:256-259 (§4.5 Table 4.5a, rows L0–L3)",
      "reported": "L0: 47.57 ([44.77, 49.70]); L1: 51.24 ([49.30, 52.54]) and LOO pr_cov = 6.3941, SE 0.1489; L2: 54.16 ([53.61, 54.61]); L3: 53.80 ([52.97, 54.44])",
      "canonical": "L0: colperm_null_mean = 45.431155 (45.43), q025 = 44.770852 (44.77); L1: colperm_null_mean = 50.071502 (50.07), q025 = 49.295610 (49.30), LOO max_loo_pr = 6.389793 (6.3898 / 6.39), SE = 0.148827 (0.1488 / 0.149); L2: colperm_null_mean = 53.755928 (53.76), q025 = 53.613377 (53.61); L3: colperm_null_mean = 53.208105 (53.21), q025 = 52.974145 (52.97). Note: `colperm_null_q975` does not exist in `family_A_subject_level.json`.",
      "source": "results/topic3/2026-10-31/family_A_subject_level.json::results.E1_full.{L0,L1,L2,L3}; verification/worker_M2_r2/probes/probe_addendum03_numbers.out.json::l1_jackknife; docs/03_empirical_analysis/topic3/2026-10-31_topic3_addendum_03.md:56",
      "required_fix": "Replace L0–L3 column-permutation null means with `45.43 (q025 = 44.77)`, `50.07 (q025 = 49.30)`, `53.76 (q025 = 53.61)`, `53.21 (q025 = 52.97)` (removing the unsupported upper quantiles `49.70, 52.54, 54.61, 54.44`), and replace L1 LOO `pr_cov = 6.3941, SE 0.1489` with `pr_cov = 6.3898 (6.39), SE 0.1488 (0.149)`."
    },
    {
      "id": "BLOCKING-3",
      "location": "docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md:246, 263 (§4.4 Table row R3 & §4.5 Table 4.5a row D3)",
      "reported": "Line 263: `m=12 covPR: LM 4.38, JEPA 6.46, STORM 7.74`; Line 246: `(1.48x, 1.77x)`",
      "canonical": "results.A2_matched25 subsample_m12_mean_pr_cov: BrainLM = 4.395156 (4.40), BrainJEPA = 6.479072 (6.48), NeuroSTORM = 7.757782 (7.76); m=12 ratios = 1.47x (6.4791/4.3952) and 1.77x (7.7578/4.3952); full matched n=25 pr_cov: BrainLM = 5.356314 (5.36), BrainJEPA = 9.659472 (9.66), NeuroSTORM = 12.507023 (12.51), ratios = 1.80x (1.8x) and 2.34x (2.3x).",
      "source": "results/topic3/2026-10-31/family_A_subject_level.json::results.A2_matched25; docs/03_empirical_analysis/topic3/2026-10-31_topic3_result_report.md:89",
      "required_fix": "In line 263, replace `LM 4.38, JEPA 6.46, STORM 7.74` with `LM 4.40 (4.395), JEPA 6.48 (6.479), STORM 7.76 (7.758)` (or full n=25 `5.36, 9.66, 12.51`). In line 246, update `(1.48x, 1.77x)` to `(m=12: 1.47x, 1.77x; n=25: 1.80x, 2.34x)`."
    },
    {
      "id": "BLOCKING-4",
      "location": "docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md:286-287 (§4.5c Family L subject-level and token-level bullets)",
      "reported": "Line 286: R1..R10 L1 pr_cov `30.50–32.22`; subject log-ratios L1_cov `-1.692`, L1_corr `-1.367`, L2_cov `-0.961`, L2_corr `-0.785`, LN0L2_cov `-0.962`, LN0L2_corr `-0.783`, L3_cov `-1.970`, L3_corr `-1.766`. Line 287: token log-ratios L1_cov `-0.556 [-0.577, -0.533]`, L1_corr `-0.194 [-0.205, -0.181]`, 6 EQ cells (`L2_corr -0.025, LN0L2_corr -0.027, L3_cov +0.029, L3_corr -0.015`, etc.), and 2 INC cells (`L0_corr +0.013 (p_Holm = 0.0149)` and `L2_cov -0.0004 / LN0L2_cov -0.0020`).",
      "canonical": "1) E1_per_arm.R1..R10.L1.pr_cov range is `17.61–20.87` (`17.6128–20.8686`), NOT `30.50–32.22` (and L2 is `30.94–31.83`, LN0L2 is `31.01–31.88`, L3 is `28.53–29.51`). 2) family_L.subject points [ci95]: L0_cov `-0.0884 [-0.3037, +0.1268]` (INC), L0_corr `-0.0725 [-0.2414, +0.0964]` (INC), L1_cov `-1.4241 [-2.4413, -0.4070]` (TE-), L1_corr `-1.0490 [-1.8293, -0.2686]` (TE-), L2_cov `-0.8695 [-1.1851, -0.5539]` (TE-), L2_corr `-0.7059 [-0.9468, -0.4650]` (TE-), LN0L2_cov `-0.8720 [-1.2032, -0.5407]` (TE-), LN0L2_corr `-0.7033 [-0.9553, -0.4514]` (TE-), L3_cov `-1.8387 [-2.0869, -1.5905]` (TE-), L3_corr `-1.5487 [-1.7692, -1.3281]` (TE-). 3) family_L.token (2 TE-, 5 EQ, 3 INC): L1_cov `-0.2770 [-0.2932, -0.2599]` (TE-, p_Holm=0.001), L1_corr `-0.3055 [-0.3180, -0.2919]` (TE-, p_Holm=0.001); 5 EQ cells: L0_corr `-0.0091 [-0.0161, -0.0013]` (ci90 `[-0.0150, -0.0027]`, p_Holm=0.0124, EQ), L2_corr `-0.0745 [-0.0771, -0.0716]` (ci90 `[-0.0767, -0.0721]`, EQ), LN0L2_corr `-0.0556 [-0.0582, -0.0529]` (ci90 `[-0.0578, -0.0534]`, EQ), L3_cov `-0.0707 [-0.0743, -0.0670]` (ci90 `[-0.0737, -0.0676]`, EQ), L3_corr `-0.0431 [-0.0456, -0.0406]` (ci90 `[-0.0452, -0.0410]`, EQ); 3 INC cells: L0_cov `-0.1046 [-0.1458, -0.0604]` (INC), L2_cov `-0.1002 [-0.1040, -0.0963]` (INC, ci95 straddles -delta = -0.0953), LN0L2_cov `-0.0754 [-0.0791, -0.0717]` (INC, max_abs_over_seeds = 0.0978 >= delta = 0.0953).",
      "source": "results/topic3/2026-11-02_h2/h2_results.json::{E1_per_arm,family_L.subject,family_L.token}; docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md:95-119",
      "required_fix": "Replace all 19 mismatched numbers and the token cell verdict breakdown (2 TE-, 5 EQ, 3 INC) on lines 286–287 with the exact values from `results/topic3/2026-11-02_h2/h2_results.json`."
    }
  ]
}
```
