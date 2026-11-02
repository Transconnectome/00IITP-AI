# Handoff — `numbers_audit_report_r2` (`paper-numbers-auditor`, Round 2)

- **Run ID**: `tw-20261031-four-topics`
- **Workflow / Phase**: Workflow C, Phase `Report` (Round 2)
- **Target Document**: `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` (`sha256 = 4906922badcdeda97ba9a3d58d876ba1ef38f91b6849d1dcbe4678de624ca917`)
- **Audit Script & Output**:
  - `verification/numbers_audit_report/audit_numbers_r2.py`
  - `verification/numbers_audit_report/audit_numbers_r2.out.json`
- **Verdict**: **`APPROVE`**

---

## 1. Observation

We performed the Round 2 programmatic read-only numbers audit (`verification/numbers_audit_report/audit_numbers_r2.py` -> `verification/numbers_audit_report/audit_numbers_r2.out.json`) on `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` (`sha256 = 4906922badcdeda97ba9a3d58d876ba1ef38f91b6849d1dcbe4678de624ca917`):

- **Numeric Checks (`309 / 309` PASS, `0` failures)**:
  - **All 4 Round-1 Blocking Issues (`BLOCKING-1`..`BLOCKING-4`) and `BLOCKING-R2-1` are 100% RESOLVED**:
    1. **`BLOCKING-1` (Topic 1 §2.5 line 69)**: `log_ratio_030C_secondary` raw group means now read `OCD -0.2020 ± 0.5344, HC -0.2224 ± 0.5415`, matching `results/topic1/2026-10-31/stats_results.json::log_ratio_030C_secondary` (`mean_ocd = -0.201962, sd_ocd = 0.534402`, `mean_hc = -0.222442, sd_hc = 0.541526`).
    2. **`BLOCKING-2` (Topic 3 §4.5 Table 4.5a lines 256–259)**: `L0..L3` column-permutation null means now read `45.43 (q025 = 44.77)`, `50.07 (q025 = 49.30)`, `53.76 (q025 = 53.61)`, `53.21 (q025 = 52.97)` (with unsupported upper quantiles removed), and `L1` LOO reads `pr_cov = 6.3898 [6.39], SE 0.1488 [0.149]`, matching `results/topic3/2026-10-31/family_A_subject_level.json` and `verification/worker_M2_r2/probes/probe_addendum03_numbers.out.json`.
    3. **`BLOCKING-3` (Topic 3 §4.4 line 246 & §4.5 line 263)**: `A2_matched25` $m=12$ `covPR` means now read `LM 4.40 (4.395), JEPA 6.48 (6.479), STORM 7.76 (7.758)` with $m=12$ ratios `1.47x, 1.77x` and full $n=25$ `covPR` `5.36 / 9.66 / 12.51` (ratios `1.80x, 2.34x`), matching `results/topic3/2026-10-31/family_A_subject_level.json::results.A2_matched25`.
    4. **`BLOCKING-4` & `BLOCKING-R2-1` (Topic 3 §4.5c lines 286–287)**:
       - Line 286 (`E1_per_arm` & `family_L.subject`): `R1..R10` full-sample ($n=57$) centered `pr_cov` at `L1` is `17.61–20.87 (17.6128–20.8686)`, `L2` is `31.93–34.02 (31.9–34.0)`, `L3` is `30.95–33.12 (31.0–33.1)`, and all 10 subject-level $m=28$ log-ratios (`L1_cov -1.424`, `L1_corr -1.049`, `L2_cov -0.869`, `L2_corr -0.706`, `LN0L2_cov -0.872`, `LN0L2_corr -0.703`, `L3_cov -1.839`, `L3_corr -1.549` [`8 TE-`], plus `L0_cov -0.061`, `L0_corr -0.131` [`2 INC`]) match `results/topic3/2026-11-02_h2/h2_results.json::family_L.subject`.
       - Line 287 (`family_L.token`, `10` cells = `2 TE-`, `4 EQ`, `4 INC`): `L1_cov -0.2770 [-0.2932, -0.2599]` (`p_Holm=0.001, TE-`), `L1_corr -0.3055 [-0.3180, -0.2919]` (`p_Holm=0.001, TE-`), `L2_corr -0.0745 [-0.0771, -0.0716]` (`EQ`), `LN0L2_corr -0.0556 [-0.0582, -0.0529]` (`EQ`), `L3_cov -0.0707 [-0.0743, -0.0670]` (`EQ`), `L3_corr -0.0431 [-0.0456, -0.0406]` (`EQ`), `L0_cov -0.0556 [-0.0634, -0.0465]` (`p_Holm=0.001, INC`), `L0_corr -0.0091 [-0.0161, -0.0013]` (`p_Holm=0.0149, INC`), `L2_cov -0.1002 [-0.1040, -0.0963]` (`INC`), and `LN0L2_cov -0.0754 [-0.0791, -0.0717]` (`INC`) match `results/topic3/2026-11-02_h2/h2_results.json::family_L.token` and `docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md` (§3 Table lines 54–62).
  - **All Topic 1 (`M1`), Topic 2 (`M3`, `FU-A`..`FU-E`), Topic 3 (`M2`, `M2H2`), Topic 4 (`M4`), and GPU Ledger (§6.1) numbers (`309 / 309`) match the canonical dated result files.**
- **Governance & Hygiene Checks**:
  - **C1 (`PROTECTED_HASHES.txt`)**: `67 / 67 OK` (`pass = true`).
  - **C4 Hygiene**: `0` BIDS subject prefixes, `0` 6-digit HCP subject IDs, `0` unsalted 16-hex content hashes (`pass = true`).
  - **C8 Compliance**: `pass = true` (zero numbers sourced from legacy `EMPIRICAL_ANALYSIS_REPORT.md` or `2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md`).

---

## 2. Logic Chain

1. Every numeric claim in `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` (`sha256 = 4906922badcdeda97ba9a3d58d876ba1ef38f91b6849d1dcbe4678de624ca917`) has been programmatically cross-checked against its canonical dated JSON/Markdown source in `results/` and `docs/03_empirical_analysis/topic{1,2,3,4}/`.
2. All `309 / 309` numeric checks pass with `0` failures, `C1` is `67/67 OK`, `C4` has `0` hits, and `C8` is satisfied.
3. Per `workflow_C_script.js.txt` line 157, the required verdict is `APPROVE`.

---

## 3. Caveats

- None. All blocking and non-blocking items from Round 1 have been verified resolved.

---

## 4. Conclusion

**Verdict: `APPROVE`**.

---

## 5. Verification Method

Run:
```bash
/home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers_r2.py
```
which outputs:
`Audit complete: 309/309 numeric checks passed, C1=True (67/67), C4=True, C8=True, verdict=APPROVE`

```json
{
  "agent": "numbers_audit_report_r2",
  "role": "paper-numbers-auditor",
  "milestone": "Report",
  "verdict": "APPROVE",
  "report_sha256": "4906922badcdeda97ba9a3d58d876ba1ef38f91b6849d1dcbe4678de624ca917",
  "c1_protected_hashes_ok": true,
  "c4_hygiene_ok": true,
  "c8_compliance_ok": true,
  "total_numeric_checks": 309,
  "passed_numeric_checks": 309,
  "failed_numeric_checks": 0,
  "blocking_issues": []
}
```
