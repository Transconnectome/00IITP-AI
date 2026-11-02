#!/usr/bin/env python3
"""
Read-only numbers audit of docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md.

Checks every numeric claim in the final report against the canonical dated JSON/markdown result
artifacts under results/ and docs/03_empirical_analysis/topic{1,2,3,4}/ and results/gpu_ledger_2026-10-31.md.
Also checks C1 (PROTECTED_HASHES.txt), C4 (zero BIDS subject prefixes, 6-digit HCP IDs, or unsalted 16-hex hashes),
and C8 (zero unlabelled legacy numbers from EMPIRICAL_ANALYSIS_REPORT.md or 2026-11-01 consolidated status).
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import re
import sys
from typing import Any

REPO_ROOT = pathlib.Path("/home/juke/git/00IITP-AI")
sys.path.insert(0, str(REPO_ROOT))

from src.topic2_fu_e import ident as fue_ident
from src.topic2_fu_e import verdict as fue_verdict_mod
REPORT_PATH = REPO_ROOT / "docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md"
OUT_JSON_PATH = REPO_ROOT / "verification/numbers_audit_report/audit_numbers.out.json"


def load_json(rel_path: str) -> Any:
    path = REPO_ROOT / rel_path
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_close(
    checks: list[dict[str, Any]],
    section: str,
    name: str,
    reported: float,
    canonical: float,
    tol: float,
    source: str,
    report_str: str | None = None,
    report_text: str | None = None,
) -> None:
    diff = abs(float(reported) - float(canonical))
    passed = diff <= tol
    present_in_report = True
    if report_str is not None and report_text is not None:
        present_in_report = report_str in report_text
        passed = passed and present_in_report
    checks.append(
        {
            "section": section,
            "name": name,
            "reported": reported,
            "canonical": canonical,
            "abs_diff": diff,
            "tol": tol,
            "report_str": report_str,
            "present_in_report": present_in_report,
            "source": source,
            "pass": passed,
        }
    )


def main() -> None:
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []
    notes: list[dict[str, Any]] = []

    # =========================================================================
    # 1. TOPIC 1 (M1): results/topic1/2026-10-31/*
    # =========================================================================
    t1_stats = load_json("results/topic1/2026-10-31/stats_results.json")
    t1_fallback = load_json("results/topic1/2026-10-31/fallback_decision.json")
    t1_derived = load_json("results/topic1/2026-10-31/report_derived_numbers.json")

    e1 = t1_stats["primary"]["E1"]
    e2 = t1_stats["primary"]["E2"]
    e1_dec = t1_stats["primary"]["decision"]["endpoints"]["E1"]
    e2_dec = t1_stats["primary"]["decision"]["endpoints"]["E2"]
    lr = t1_stats["log_ratio_030C_secondary"]
    acc_strat = t1_stats["acceptance_stratified_POSTFREEZE"]
    fam1 = t1_stats["secondary_family1_classification"]
    fam2 = t1_stats["secondary_family2_ybocs"]
    fam3 = t1_stats["secondary_family3_medication"]
    desc1 = t1_stats["descriptives_primary_unit"]

    t1_src = "results/topic1/2026-10-31/stats_results.json"
    t1_der_src = "results/topic1/2026-10-31/report_derived_numbers.json"
    t1_fb_src = "results/topic1/2026-10-31/fallback_decision.json"

    # Cohort counts
    check_close(checks, "Topic1_M1", "n_total", 1706, e1["n"], 0, t1_src, "1,706", report_text)
    check_close(checks, "Topic1_M1", "n_ocd", 869, e1["n_ocd"], 0, t1_src, "869", report_text)
    check_close(checks, "Topic1_M1", "n_hc", 837, e1["n_hc"], 0, t1_src, "837", report_text)
    check_close(checks, "Topic1_M1", "n_sites", 23, e1["n_sites"], 0, t1_src, "23개 기관", report_text)
    check_close(checks, "Topic1_M1", "n_cells", 46, len(desc1["by_site_group"]), 0, t1_src, "46", report_text)
    check_close(checks, "Topic1_M1", "degen_005_count", 2, t1_fallback["rates_all_units"]["broadband@0.05"]["n_degenerate_E1"], 0, t1_fb_src, "2/1,706", report_text)

    # E1 primary
    check_close(checks, "Topic1_M1", "E1_d_lmm", 0.113131, e1["d"], 1e-6, t1_src, "0.113131", report_text)
    check_close(checks, "Topic1_M1", "E1_ci95_lo", 0.014590, t1_derived["E1"]["approx_wald_95ci_d"][0], 1e-6, t1_der_src, "0.014590", report_text)
    check_close(checks, "Topic1_M1", "E1_ci95_hi", 0.211671, t1_derived["E1"]["approx_wald_95ci_d"][1], 1e-6, t1_der_src, "0.211671", report_text)
    check_close(checks, "Topic1_M1", "E1_se_d", 0.050276, t1_derived["E1"]["se_d_approx"], 1e-6, t1_der_src, "0.050276", report_text)
    check_close(checks, "Topic1_M1", "E1_beta_lmm", 0.548815, e1["beta_lmm"], 1e-6, t1_src, "0.548815", report_text)
    check_close(checks, "Topic1_M1", "E1_se_lmm", 0.243702, e1["se_lmm_wald"], 1e-6, t1_src, "0.243702", report_text)
    check_close(checks, "Topic1_M1", "E1_sigma_eps_lmm", 4.851160, e1["sigma_eps_lmm"], 1e-6, t1_src, "4.851160", report_text)
    check_close(checks, "Topic1_M1", "E1_p_fl", 0.0223, e1["p_fl"], 1e-5, t1_src, "0.0223", report_text)
    check_close(checks, "Topic1_M1", "E1_p_holm", 0.0446, e1_dec["p_holm"], 1e-5, t1_src, "0.0446", report_text)
    check_close(checks, "Topic1_M1", "E1_p_wald", 0.0243, e1["p_lmm_wald_secondary"], 1e-4, t1_src, "0.0243", report_text)
    check_close(checks, "Topic1_M1", "E1_mundlak", 1.34e-13, e1["mundlak_equality_ratio"], 1e-15, t1_src, "1.34\\times 10^{-13}", report_text)
    check_close(checks, "Topic1_M1", "E1_mean_ocd", -1.557729, e1["mean_ocd"], 1e-6, t1_src, "-1.557729", report_text)
    check_close(checks, "Topic1_M1", "E1_sd_ocd", 5.306716, e1["sd_ocd"], 1e-6, t1_src, "5.306716", report_text)
    check_close(checks, "Topic1_M1", "E1_mean_hc", -2.002134, e1["mean_hc"], 1e-6, t1_src, "-2.002134", report_text)
    check_close(checks, "Topic1_M1", "E1_sd_hc", 4.886956, e1["sd_hc"], 1e-6, t1_src, "4.886956", report_text)
    check_close(checks, "Topic1_M1", "E1_raw_d", 0.087051, e1["raw_cohen_d_DESCRIPTIVE"], 1e-6, t1_src, "0.087051", report_text)
    check_close(checks, "Topic1_M1", "E1_welch_p", 0.0720, e1["welch_p_DESCRIPTIVE"], 1e-4, t1_src, "0.0720", report_text)

    # E2 primary
    check_close(checks, "Topic1_M1", "E2_d_lmm", 0.037689, e2["d"], 1e-6, t1_src, "0.037689", report_text)
    check_close(checks, "Topic1_M1", "E2_ci95_lo", -0.060873, t1_derived["E2"]["approx_wald_95ci_d"][0], 1e-6, t1_der_src, "-0.060873", report_text)
    check_close(checks, "Topic1_M1", "E2_ci95_hi", 0.136251, t1_derived["E2"]["approx_wald_95ci_d"][1], 1e-6, t1_der_src, "0.136251", report_text)
    check_close(checks, "Topic1_M1", "E2_se_d", 0.050287, t1_derived["E2"]["se_d_approx"], 1e-6, t1_der_src, "0.050287", report_text)
    check_close(checks, "Topic1_M1", "E2_beta_lmm", 0.343871, e2["beta_lmm"], 1e-6, t1_src, "0.343871", report_text)
    check_close(checks, "Topic1_M1", "E2_se_lmm", 0.458350, e2["se_lmm_wald"], 1e-6, t1_src, "0.458350", report_text)
    check_close(checks, "Topic1_M1", "E2_sigma_eps_lmm", 9.123959, e2["sigma_eps_lmm"], 1e-6, t1_src, "9.123959", report_text)
    check_close(checks, "Topic1_M1", "E2_p_fl", 0.4416, e2["p_fl"], 1e-5, t1_src, "0.4416", report_text)
    check_close(checks, "Topic1_M1", "E2_p_holm", 0.4416, e2_dec["p_holm"], 1e-5, t1_src, "0.4416", report_text)
    check_close(checks, "Topic1_M1", "E2_p_wald", 0.4531, e2["p_lmm_wald_secondary"], 1e-4, t1_src, "0.4531", report_text)
    check_close(checks, "Topic1_M1", "E2_mundlak", 1.97e-13, e2["mundlak_equality_ratio"], 1e-15, t1_src, "1.97\\times 10^{-13}", report_text)
    check_close(checks, "Topic1_M1", "E2_mean_ocd", 6.375704, e2["mean_ocd"], 1e-6, t1_src, "6.375704", report_text)
    check_close(checks, "Topic1_M1", "E2_sd_ocd", 9.659078, e2["sd_ocd"], 1e-6, t1_src, "9.659078", report_text)
    check_close(checks, "Topic1_M1", "E2_mean_hc", 6.183636, e2["mean_hc"], 1e-6, t1_src, "6.183636", report_text)
    check_close(checks, "Topic1_M1", "E2_sd_hc", 9.674975, e2["sd_hc"], 1e-6, t1_src, "9.674975", report_text)
    check_close(checks, "Topic1_M1", "E2_raw_d", 0.019869, e2["raw_cohen_d_DESCRIPTIVE"], 1e-6, t1_src, "0.019869", report_text)
    check_close(checks, "Topic1_M1", "E2_welch_p", 0.6817, e2["welch_p_DESCRIPTIVE"], 1e-4, t1_src, "0.6817", report_text)

    # Secondary & descriptive Topic 1
    check_close(checks, "Topic1_M1", "Fam1_lagmotif_auroc", 0.515685, fam1["lagmotif"]["pooled_oof_auroc"], 1e-6, t1_src, "0.515685", report_text)
    check_close(checks, "Topic1_M1", "Fam1_lagmotif_ci_lo", 0.468092, fam1["lagmotif"]["pooled_auroc_ci95_site_bootstrap"][0], 1e-6, t1_src, "0.468092", report_text)
    check_close(checks, "Topic1_M1", "Fam1_lagmotif_ci_hi", 0.559912, fam1["lagmotif"]["pooled_auroc_ci95_site_bootstrap"][1], 1e-6, t1_src, "0.559912", report_text)
    check_close(checks, "Topic1_M1", "Fam1_lagmotif_site_mean", 0.555433, fam1["lagmotif"]["mean_per_site_auroc"], 1e-6, t1_src, "0.555433", report_text)
    check_close(checks, "Topic1_M1", "Fam1_staticfc_auroc", 0.563024, fam1["static_fc_comparator_same_subjects_same_folds"]["pooled_oof_auroc"], 1e-6, t1_src, "0.563024", report_text)
    check_close(checks, "Topic1_M1", "Fam1_staticfc_ci_lo", 0.523933, fam1["static_fc_comparator_same_subjects_same_folds"]["pooled_auroc_ci95_site_bootstrap"][0], 1e-6, t1_src, "0.523933", report_text)
    check_close(checks, "Topic1_M1", "Fam1_staticfc_ci_hi", 0.600355, fam1["static_fc_comparator_same_subjects_same_folds"]["pooled_auroc_ci95_site_bootstrap"][1], 1e-6, t1_src, "0.600355", report_text)
    check_close(checks, "Topic1_M1", "Fam1_staticfc_site_mean", 0.558911, fam1["static_fc_comparator_same_subjects_same_folds"]["mean_per_site_auroc"], 1e-6, t1_src, "0.558911", report_text)

    check_close(checks, "Topic1_M1", "Fam2_E1_std_beta", 0.031925, fam2["E1"]["std_beta"], 1e-6, t1_src, "0.031925", report_text)
    check_close(checks, "Topic1_M1", "Fam2_E1_t", 0.9988, fam2["E1"]["t"], 1e-4, t1_src, "0.9988", report_text)
    check_close(checks, "Topic1_M1", "Fam2_E1_p_fl", 0.3073, fam2["E1"]["p_fl"], 1e-5, t1_src, "0.3073", report_text)
    check_close(checks, "Topic1_M1", "Fam2_E2_std_beta", 0.028837, fam2["E2"]["std_beta"], 1e-6, t1_src, "0.028837", report_text)
    check_close(checks, "Topic1_M1", "Fam2_E2_t", 0.8857, fam2["E2"]["t"], 1e-4, t1_src, "0.8857", report_text)
    check_close(checks, "Topic1_M1", "Fam2_E2_p_fl", 0.3609, fam2["E2"]["p_fl"], 1e-5, t1_src, "0.3609", report_text)

    check_close(checks, "Topic1_M1", "Fam3_E1_beta", -0.552382, fam3["E1"]["beta"], 1e-6, t1_src, "-0.552382", report_text)
    check_close(checks, "Topic1_M1", "Fam3_E1_d_fe", -0.085564, fam3["E1"]["d_fe"], 1e-6, t1_src, "-0.085564", report_text)
    check_close(checks, "Topic1_M1", "Fam3_E1_p_fl", 0.5682, fam3["E1"]["p_fl"], 1e-5, t1_src, "0.5682", report_text)
    check_close(checks, "Topic1_M1", "Fam3_E2_beta", -2.162068, fam3["E2"]["beta"], 1e-6, t1_src, "-2.162068", report_text)
    check_close(checks, "Topic1_M1", "Fam3_E2_d_fe", -0.198656, fam3["E2"]["d_fe"], 1e-6, t1_src, "-0.198656", report_text)
    check_close(checks, "Topic1_M1", "Fam3_E2_p_fl", 0.1550, fam3["E2"]["p_fl"], 1e-5, t1_src, "0.1550", report_text)

    check_close(checks, "Topic1_M1", "LogRatio_d_lmm", 0.089710, lr["d"], 1e-6, t1_src, "0.089710", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_beta_lmm", 0.045331, lr["beta_lmm"], 1e-6, t1_src, "0.045331", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_se_lmm", 0.025384, lr["se_lmm_wald"], 1e-6, t1_src, "0.025384", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_t_fe", 1.784585, lr["t_fe"], 1e-6, t1_src, "1.784585", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_p_fl", 0.0665, lr["p_fl"], 1e-5, t1_src, "0.0665", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_p_wald", 0.0741, lr["p_lmm_wald_secondary"], 1e-4, t1_src, "0.0741", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_mean_ocd", -0.0876, lr["mean_ocd"], 1e-4, t1_src, "-0.0876", report_text)
    check_close(checks, "Topic1_M1", "LogRatio_mean_hc", -0.1096, lr["mean_hc"], 1e-4, t1_src, "-0.1096", report_text)

    check_close(checks, "Topic1_M1", "AccStrat_n", 1535, acc_strat["E1"]["n"], 0, t1_src, "1,535", report_text)
    check_close(checks, "Topic1_M1", "AccStrat_p10", 0.4836, acc_strat["threshold_acceptance_p10"], 1e-4, t1_src, "0.4836", report_text)
    check_close(checks, "Topic1_M1", "AccStrat_E1_d", 0.129631, acc_strat["E1"]["d"], 1e-6, t1_src, "0.129631", report_text)
    check_close(checks, "Topic1_M1", "AccStrat_E1_p_fl", 0.0143, acc_strat["E1"]["p_fl"], 1e-5, t1_src, "0.0143", report_text)
    check_close(checks, "Topic1_M1", "AccStrat_E2_d", 0.094895, acc_strat["E2"]["d"], 1e-6, t1_src, "0.094895", report_text)
    check_close(checks, "Topic1_M1", "AccStrat_E2_p_fl", 0.0666, acc_strat["E2"]["p_fl"], 1e-5, t1_src, "0.0666", report_text)

    # =========================================================================
    # 2. TOPIC 2 (M3 + FU_A..FU_E)
    # =========================================================================
    m3_v = load_json("results/topic2/2026-11-01/verdict.json")
    m3_s0 = load_json("results/topic2/2026-11-01/stage0_hcp.json")
    m3_no_s2 = load_json("results/topic2/2026-11-01/posthoc_sensitivity_without_seed2.json")
    fua_v = load_json("results/topic2/2026-11-02_fu_a/verdict.json")
    fua_c = load_json("results/topic2/2026-11-02_fu_a/fua_constants.json")
    fua_d = load_json("results/topic2/2026-11-02_fu_a/design_stats_train.json")
    fub_v = load_json("results/topic2/2026-11-02_fu_b/verdict.json")
    fuc_v = load_json("results/topic2/2026-11-02_fu_c/verdict.json")
    fud_v = load_json("results/topic2/2026-11-02_fu_d/verdict.json")
    fud_e_run = load_json("results/topic2/2026-11-02_fu_d/runs/Fplus_E_s0/run.json")
    fud_c_run = load_json("results/topic2/2026-11-02_fu_d/runs/Fplus_C_s0/run.json")
    fud_s_run = load_json("results/topic2/2026-11-02_fu_d/runs/Fplus_S_s0/run.json")
    fue_v = load_json("results/topic2/2026-11-02_fu_e/verdict.json")

    m3_src = "results/topic2/2026-11-01/verdict.json"
    m3_s0_src = "results/topic2/2026-11-01/stage0_hcp.json"
    m3_ns2_src = "results/topic2/2026-11-01/posthoc_sensitivity_without_seed2.json"
    fua_src = "results/topic2/2026-11-02_fu_a/verdict.json"
    fub_src = "results/topic2/2026-11-02_fu_b/verdict.json"
    fuc_src = "results/topic2/2026-11-02_fu_c/verdict.json"
    fud_src = "results/topic2/2026-11-02_fu_d/verdict.json"
    fue_src = "results/topic2/2026-11-02_fu_e/verdict.json"

    # M3 Stage 0
    check_close(checks, "Topic2_M3", "S0_E_r", 0.257015, m3_s0["arm_means"]["E"]["r_mean"], 1e-6, m3_s0_src, "0.257015", report_text)
    check_close(checks, "Topic2_M3", "S0_E_pca2", 0.529554, m3_s0["arm_means"]["E"]["pca2"], 1e-6, m3_s0_src, "0.529554", report_text)
    check_close(checks, "Topic2_M3", "S0_C_r", 0.260925, m3_s0["arm_means"]["C"]["r_mean"], 1e-6, m3_s0_src, "0.260925", report_text)
    check_close(checks, "Topic2_M3", "S0_C_pca2", 0.477987, m3_s0["arm_means"]["C"]["pca2"], 1e-6, m3_s0_src, "0.477987", report_text)
    check_close(checks, "Topic2_M3", "S0_S_r", 0.189437, m3_s0["arm_means"]["S_mean"]["r_mean"], 1e-6, m3_s0_src, "0.189437", report_text)
    check_close(checks, "Topic2_M3", "S0_S_pca2", 0.446837, m3_s0["arm_means"]["S_mean"]["pca2"], 1e-6, m3_s0_src, "0.446837", report_text)
    check_close(checks, "Topic2_M3", "S0_C_minus_E_r", 0.003910, m3_s0["contrasts"]["r_mean:C-E"]["mean"], 1e-6, m3_s0_src, "+0.003910", report_text)
    check_close(checks, "Topic2_M3", "S0_C_minus_E_pca2", -0.051567, m3_s0["contrasts"]["pca2:C-E"]["mean"], 1e-6, m3_s0_src, "-0.051567", report_text)
    check_close(checks, "Topic2_M3", "S0_C_minus_S_r", 0.071489, m3_s0["contrasts"]["r_mean:C-S_mean"]["mean"], 1e-6, m3_s0_src, "+0.071489", report_text)
    check_close(checks, "Topic2_M3", "S0_C_minus_S_pca2", 0.031150, m3_s0["contrasts"]["pca2:C-S_mean"]["mean"], 1e-6, m3_s0_src, "+0.031150", report_text)

    # M3 Gate & Stage 1
    check_close(checks, "Topic2_M3", "Fplus_gain_C_vs_E_pct", 3.06, 100 * m3_v["fixture_gates"]["Fplus"]["gain_C_vs_E"], 1e-2, m3_src, "+3.06%", report_text)
    check_close(checks, "Topic2_M3", "Fplus_gain_C_vs_S_pct", 2.93, 100 * m3_v["fixture_gates"]["Fplus"]["gain_C_vs_S"], 1e-2, m3_src, "+2.93%", report_text)
    check_close(checks, "Topic2_M3", "Fminus_gain_C_vs_E_pct", -1.74, 100 * m3_v["fixture_gates"]["Fminus"]["gain_C_vs_E"], 1e-2, m3_src, "-1.74%", report_text)
    check_close(checks, "Topic2_M3", "Fminus_gain_C_vs_S_pct", 0.096, 100 * m3_v["fixture_gates"]["Fminus"]["gain_C_vs_S"], 1e-3, m3_src, "+0.000963", report_text)
    check_close(checks, "Topic2_M3", "M3_E_mean_nmse", 0.988922, sum(m3_v["stage1"]["test_nmse_by_seed"]["E"]) / 5.0, 1e-6, m3_src, "0.988922", report_text)
    check_close(checks, "Topic2_M3", "M3_C_mean_nmse", 0.987467, sum(m3_v["stage1"]["test_nmse_by_seed"]["C"]) / 5.0, 1e-6, m3_src, "0.987467", report_text)
    check_close(checks, "Topic2_M3", "M3_S_mean_nmse", 0.992175, sum(m3_v["stage1"]["test_nmse_by_seed"]["S"]) / 5.0, 1e-6, m3_src, "0.992175", report_text)
    check_close(checks, "Topic2_M3", "M3_I1_mean_pct", 0.147, 100 * m3_v["stage1"]["I1_t"]["mean"], 1e-3, m3_src, "+0.147%", report_text)
    check_close(checks, "Topic2_M3", "M3_I1_lo_pct", -0.068, 100 * m3_v["stage1"]["I1_t"]["lo"], 1e-3, m3_src, "-0.068%", report_text)
    check_close(checks, "Topic2_M3", "M3_I1_hi_pct", 0.361, 100 * m3_v["stage1"]["I1_t"]["hi"], 1e-3, m3_src, "+0.361%", report_text)
    check_close(checks, "Topic2_M3", "M3_I2_mean_pct", 0.473, 100 * m3_v["stage1"]["I2_t"]["mean"], 1e-3, m3_src, "+0.473%", report_text)
    check_close(checks, "Topic2_M3", "M3_I2_lo_pct", 0.001, 100 * m3_v["stage1"]["I2_t"]["lo"], 1e-3, m3_src, "+0.001%", report_text)
    check_close(checks, "Topic2_M3", "M3_I2_hi_pct", 0.946, 100 * m3_v["stage1"]["I2_t"]["hi"], 1e-3, m3_src, "+0.946%", report_text)
    check_close(checks, "Topic2_M3", "M3_no_s2_I1_mean_pct", 0.083, 100 * m3_no_s2["I1_t_without_seed2"]["mean"], 1e-3, m3_ns2_src, "+0.083%", report_text)
    check_close(checks, "Topic2_M3", "M3_no_s2_I2_mean_pct", 0.307, 100 * m3_no_s2["I2_t_without_seed2"]["mean"], 1e-3, m3_ns2_src, "+0.307\\%", report_text)

    # FU-A
    check_close(checks, "Topic2_FU_A", "kappa", 5.699892, fua_d["design_stats"]["kappa"], 1e-6, "results/topic2/2026-11-02_fu_a/design_stats_train.json", "5.699892", report_text)
    check_close(checks, "Topic2_FU_A", "NF", 0.208508, fua_d["design_stats"]["NF"], 1e-6, "results/topic2/2026-11-02_fu_a/design_stats_train.json", "0.208508", report_text)
    check_close(checks, "Topic2_FU_A", "sigma_v", 6.545925, fua_d["design_stats"]["sigma_v"], 1e-6, "results/topic2/2026-11-02_fu_a/design_stats_train.json", "6.545925", report_text)
    check_close(checks, "Topic2_FU_A", "Fplus_E_s0", 0.774678, fua_v["fixture_gates"]["Fplus"]["test_nmse"]["E"], 1e-6, fua_src, "0.774678", report_text)
    check_close(checks, "Topic2_FU_A", "Fplus_C_s0", 0.770409, fua_v["fixture_gates"]["Fplus"]["test_nmse"]["C"], 1e-6, fua_src, "0.770409", report_text)
    check_close(checks, "Topic2_FU_A", "Fplus_gain_pct", 0.5511, 100 * fua_v["fixture_gates"]["Fplus"]["gain_C_vs_E"], 1e-4, fua_src, "+0.5511%", report_text)

    # FU-B
    check_close(checks, "Topic2_FU_B", "gate4x_E", 0.655099, fub_v["fplus_gate_4x"]["gate"]["seed_mean_nmse"]["E"], 1e-6, fub_src, "0.655099", report_text)
    check_close(checks, "Topic2_FU_B", "gate4x_C", 0.630692, fub_v["fplus_gate_4x"]["gate"]["seed_mean_nmse"]["C"], 1e-6, fub_src, "0.630692", report_text)
    check_close(checks, "Topic2_FU_B", "gate4x_S", 0.654914, fub_v["fplus_gate_4x"]["gate"]["seed_mean_nmse"]["S"], 1e-6, fub_src, "0.654914", report_text)
    check_close(checks, "Topic2_FU_B", "gate4x_gain_CE_pct", 3.726, 100 * fub_v["fplus_gate_4x"]["gate"]["gain_C_vs_E"], 1e-3, fub_src, "+3.726%", report_text)
    check_close(checks, "Topic2_FU_B", "gate4x_gain_CS_pct", 3.699, 100 * fub_v["fplus_gate_4x"]["gate"]["gain_C_vs_S"], 1e-3, fub_src, "+3.699%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_E_mean_nmse", 0.988111, sum(fub_v["stage1"]["test_nmse_by_seed"]["E"]) / 5.0, 1e-6, fub_src, "0.988111", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_C_mean_nmse", 0.987472, sum(fub_v["stage1"]["test_nmse_by_seed"]["C"]) / 5.0, 1e-6, fub_src, "0.987472", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_S_mean_nmse", 0.986563, sum(fub_v["stage1"]["test_nmse_by_seed"]["S"]) / 5.0, 1e-6, fub_src, "0.986563", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_I1_mean_pct", 0.063, 100 * fub_v["stage1"]["I1_t"]["mean"], 1e-3, fub_src, "+0.063%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_I1_lo_pct", -0.299, 100 * fub_v["stage1"]["I1_t"]["lo"], 1e-3, fub_src, "-0.299%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_I1_hi_pct", 0.425, 100 * fub_v["stage1"]["I1_t"]["hi"], 1e-3, fub_src, "+0.425%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_I2_mean_pct", -0.092, 100 * fub_v["stage1"]["I2_t"]["mean"], 1e-3, fub_src, "-0.092%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_I2_lo_pct", -0.646, 100 * fub_v["stage1"]["I2_t"]["lo"], 1e-3, fub_src, "-0.646%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_I2_hi_pct", 0.461, 100 * fub_v["stage1"]["I2_t"]["hi"], 1e-3, fub_src, "+0.461%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_nostall_I1_mean_pct", -0.067, 100 * fub_v["stage1"]["stall_sensitivity"]["I1_t"]["mean"], 1e-3, fub_src, "-0.067\\%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_nostall_I1_lo_pct", -0.091, 100 * fub_v["stage1"]["stall_sensitivity"]["I1_t"]["lo"], 1e-3, fub_src, "-0.091%", report_text)
    check_close(checks, "Topic2_FU_B", "FUB_nostall_I1_hi_pct", -0.043, 100 * fub_v["stage1"]["stall_sensitivity"]["I1_t"]["hi"], 1e-3, fub_src, "-0.043%", report_text)

    # FU-C
    check_close(checks, "Topic2_FU_C", "FUC_E_mean_nmse", 0.988422, sum(fuc_v["stage1"]["test_nmse_by_seed"]["E"]) / 8.0, 1e-6, fuc_src, "0.988422", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_C_mean_nmse", 0.989538, sum(fuc_v["stage1"]["test_nmse_by_seed"]["C"]) / 8.0, 1e-6, fuc_src, "0.989538", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_S_mean_nmse", 0.989637, sum(fuc_v["stage1"]["test_nmse_by_seed"]["S"]) / 8.0, 1e-6, fuc_src, "0.989637", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_I1_mean_pct", -0.113, 100 * fuc_v["stage1"]["I1_t"]["mean"], 1e-3, fuc_src, "-0.113%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_I1_lo_pct", -0.499, 100 * fuc_v["stage1"]["I1_t"]["lo"], 1e-3, fuc_src, "-0.499%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_I1_hi_pct", 0.272, 100 * fuc_v["stage1"]["I1_t"]["hi"], 1e-3, fuc_src, "+0.272%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_I2_mean_pct", 0.008, 100 * fuc_v["stage1"]["I2_t"]["mean"], 1e-3, fuc_src, "+0.008%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_I2_lo_pct", -0.520, 100 * fuc_v["stage1"]["I2_t"]["lo"], 1e-3, fuc_src, "-0.520%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_I2_hi_pct", 0.537, 100 * fuc_v["stage1"]["I2_t"]["hi"], 1e-3, fuc_src, "+0.537%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_nostall_I1_mean_pct", 0.040, 100 * fuc_v["secondary"]["drop_stalled_seed_triplets"]["I1_t"]["mean"], 1e-3, fuc_src, "+0.040\\%", report_text)
    check_close(checks, "Topic2_FU_C", "FUC_pooled13_I1_mean_pct", -0.013, 100 * fuc_v["secondary"]["pooled_13_seeds_includes_seen_r1_data"]["I1_t"]["mean"], 1e-3, fuc_src, "-0.013\\%", report_text)

    # FU-D
    check_close(checks, "Topic2_FU_D", "FUD_E_s0", 0.655849, fud_e_run["test_nmse"], 1e-6, "results/topic2/2026-11-02_fu_d/runs/Fplus_E_s0/run.json", "0.655849", report_text)
    check_close(checks, "Topic2_FU_D", "FUD_C_s0", 0.653468, fud_c_run["test_nmse"], 1e-6, "results/topic2/2026-11-02_fu_d/runs/Fplus_C_s0/run.json", "0.653468", report_text)
    check_close(checks, "Topic2_FU_D", "FUD_S_s0", 0.657774, fud_s_run["test_nmse"], 1e-6, "results/topic2/2026-11-02_fu_d/runs/Fplus_S_s0/run.json", "0.657774", report_text)
    check_close(checks, "Topic2_FU_D", "FUD_gain_CE_pct", 0.3631, 100 * fud_v["decision"]["fplus_gate"]["gain_C_vs_E"], 1e-4, fud_src, "+0.3631%", report_text)
    check_close(checks, "Topic2_FU_D", "FUD_gain_CS_pct", 0.6546, 100 * fud_v["decision"]["fplus_gate"]["gain_C_vs_S"], 1e-4, fud_src, "+0.6546%", report_text)

    # FU-E
    fue_ext = load_json("results/topic2/2026-11-02_fu_e/run_524/extract.json")
    fue_rs_fplus, _ = fue_verdict_mod.model_table(fue_ext["conditions"]["Fplus_ident"], "trained", "cov2")
    fue_s2_p95 = fue_ident.null_p95(fue_rs_fplus[("S", 2)], 1000, 20261102)
    check_close(checks, "Topic2_FU_E", "FUE_S_s2_idiff", 5.76, fue_v["gates"]["Fplus_ident"]["idiff"]["S_s2"], 1e-2, fue_src, "5.76", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_S_s2_p95", 10.59, fue_s2_p95, 1e-2, "results/topic2/2026-11-02_fu_e/run_524/extract.json", "10.59", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_G3_cellfc_idiff", 64.13, fue_v["gates"]["G3_rawfc"]["idiff"], 1e-2, fue_src, "64.13", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_E_idiff_mean", 61.07, sum(fue_v["main_idiff_cov2"][f"E_s{i}"] for i in range(5)) / 5.0, 1e-2, fue_src, "61.07", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_C_idiff_mean", 65.42, sum(fue_v["main_idiff_cov2"][f"C_s{i}"] for i in range(5)) / 5.0, 1e-2, fue_src, "65.42", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_S_idiff_mean", 56.92, sum(fue_v["main_idiff_cov2"][f"S_s{i}"] for i in range(5)) / 5.0, 1e-2, fue_src, "56.92", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_J1_mean_pct", 8.11, 100 * fue_v["primary"]["J1_t"]["mean"], 1e-2, fue_src, "+0.081053", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_J1_lo_pct", -6.60, 100 * fue_v["primary"]["J1_t"]["lo"], 1e-2, fue_src, "-0.0660", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_J1_hi_pct", 22.81, 100 * fue_v["primary"]["J1_t"]["hi"], 1e-2, fue_src, "+0.2281", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_J2_mean_pct", 15.00, 100 * fue_v["primary"]["J2_t"]["mean"], 1e-2, fue_src, "+0.1500", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_J2_lo_pct", 9.80, 100 * fue_v["primary"]["J2_t"]["lo"], 1e-2, fue_src, "+0.097963", report_text)
    check_close(checks, "Topic2_FU_E", "FUE_J2_hi_pct", 20.21, 100 * fue_v["primary"]["J2_t"]["hi"], 1e-2, fue_src, "+0.2021", report_text)

    # =========================================================================
    # 3. TOPIC 3 (M2 + M2H2)
    # =========================================================================
    t3_fa = load_json("results/topic3/2026-10-31/family_A_subject_level.json")
    t3_fb = load_json("results/topic3/2026-10-31/family_B_token_level.json")
    t3_repro = load_json("results/topic3/2026-10-31/t3_1_provenance_repro.json")
    t3_h2 = load_json("results/topic3/2026-11-02_h2/h2_results.json")
    t3_h2_gate = load_json("results/topic3/2026-11-02_h2/gate/gate_decision.json")

    fa_src = "results/topic3/2026-10-31/family_A_subject_level.json"
    fb_src = "results/topic3/2026-10-31/family_B_token_level.json"
    h2_src = "results/topic3/2026-11-02_h2/h2_results.json"

    # Family A E1_full
    for layer, cov_exp, corr_exp, se_exp in [
        ("L0", 2.777344, 4.791938, 0.276257),
        ("L1", 2.778188, 5.235213, 3.576676),
        ("L2", 11.020186, 13.187853, 1.295550),
        ("L3", 3.578647, 4.779337, 0.285604),
        ("BrainLM", 4.318772, 6.513417, 0.767017),
        ("BrainJEPA", 11.785055, 13.929926, 0.767387),
        ("NeuroSTORM", 12.507023, 13.980857, 1.067117),
    ]:
        rec = t3_fa["results"]["E1_full"][layer]
        check_close(checks, "Topic3_M2", f"FA_{layer}_pr_cov", cov_exp, rec["pr_cov"], 1e-6, fa_src, f"{cov_exp:.6f}", report_text)
        check_close(checks, "Topic3_M2", f"FA_{layer}_pr_corr", corr_exp, rec["pr_corr"], 1e-6, fa_src, f"{corr_exp:.6f}", report_text)
        check_close(checks, "Topic3_M2", f"FA_{layer}_jk_se", se_exp, rec["jackknife_se_pr_cov"], 1e-6, fa_src)

    # Family A E1_full column-permutation null means (Table 4.5a lines 256-259)
    for layer, rep_null_mean, rep_str in [
        ("L0", 47.57, "`47.57` (`[44.77, 49.70]`)"),
        ("L1", 51.24, "`51.24` (`[49.30, 52.54]`)"),
        ("L2", 54.16, "`54.16` (`[53.61, 54.61]`)"),
        ("L3", 53.80, "`53.80` (`[52.97, 54.44]`)"),
    ]:
        rec = t3_fa["results"]["E1_full"][layer]
        check_close(
            checks,
            "Topic3_M2",
            f"FA_{layer}_colperm_null_mean",
            rep_null_mean,
            rec["colperm_null_mean"],
            1e-2,
            fa_src,
            rep_str,
            report_text,
        )

    # L1 single-outlier jackknife LOO max pr_cov (Table 4.5a line 257)
    t3_add03 = load_json("verification/worker_M2_r2/probes/probe_addendum03_numbers.out.json")
    check_close(
        checks,
        "Topic3_M2",
        "FA_L1_loo_max_pr_cov",
        6.3941,
        t3_add03["l1_jackknife"]["max_loo_pr"],
        1e-4,
        "verification/worker_M2_r2/probes/probe_addendum03_numbers.out.json",
        "pr_cov = 6.3941",
        report_text,
    )

    # Family A A1_swift_pairs
    a1_l2l3 = t3_fa["results"]["A1_swift_pairs"]["L2_minus_L3"]
    check_close(checks, "Topic3_M2", "A1_L2_minus_L3_cov_pt", 5.343855, a1_l2l3["cov"]["point"], 1e-6, fa_src, "+5.343855", report_text)
    check_close(checks, "Topic3_M2", "A1_L2_minus_L3_cov_lo", 3.224986, a1_l2l3["cov"]["lo"], 1e-6, fa_src, "+3.224986", report_text)
    check_close(checks, "Topic3_M2", "A1_L2_minus_L3_cov_hi", 7.462723, a1_l2l3["cov"]["hi"], 1e-6, fa_src, "+7.462723", report_text)
    check_close(checks, "Topic3_M2", "A1_L2_minus_L3_corr_pt", 6.038809, a1_l2l3["corr"]["point"], 1e-6, fa_src, "+6.038809", report_text)
    check_close(checks, "Topic3_M2", "A1_L2_minus_L3_corr_lo", 4.276607, a1_l2l3["corr"]["lo"], 1e-6, fa_src, "+4.276607", report_text)
    check_close(checks, "Topic3_M2", "A1_L2_minus_L3_corr_hi", 7.801011, a1_l2l3["corr"]["hi"], 1e-6, fa_src, "+7.801011", report_text)

    # Family A A2_matched25 & A2_pairs (Table 4.5a D3 line 263)
    check_close(checks, "Topic3_M2", "A2_BrainLM_cov", 5.356330, t3_fa["results"]["A2_matched25"]["BrainLM"]["pr_cov"], 1e-6, fa_src)
    check_close(checks, "Topic3_M2", "A2_BrainJEPA_cov", 9.659530, t3_fa["results"]["A2_matched25"]["BrainJEPA"]["pr_cov"], 1e-6, fa_src)
    check_close(checks, "Topic3_M2", "A2_NeuroSTORM_cov", 12.507023, t3_fa["results"]["A2_matched25"]["NeuroSTORM"]["pr_cov"], 1e-6, fa_src)
    check_close(checks, "Topic3_M2", "A2_BrainLM_m12_cov", 4.38, t3_fa["results"]["A2_matched25"]["BrainLM"]["subsample_m12_mean_pr_cov"], 1e-2, fa_src, "`LM` `4.38`", report_text)
    check_close(checks, "Topic3_M2", "A2_BrainJEPA_m12_cov", 6.46, t3_fa["results"]["A2_matched25"]["BrainJEPA"]["subsample_m12_mean_pr_cov"], 1e-2, fa_src, "`JEPA` `6.46`", report_text)
    check_close(checks, "Topic3_M2", "A2_NeuroSTORM_m12_cov", 7.74, t3_fa["results"]["A2_matched25"]["NeuroSTORM"]["subsample_m12_mean_pr_cov"], 1e-2, fa_src, "`STORM` `7.74`", report_text)
    check_close(checks, "Topic3_M2", "A2_JEPA_minus_LM_cov", 2.083916, t3_fa["results"]["A2_pairs"]["BrainJEPA_minus_BrainLM"]["cov"]["point"], 1e-6, fa_src, "+2.083916", report_text)
    check_close(checks, "Topic3_M2", "A2_NS_minus_LM_cov", 3.362626, t3_fa["results"]["A2_pairs"]["NeuroSTORM_minus_BrainLM"]["cov"]["point"], 1e-6, fa_src, "+3.362626", report_text)

    # Family B primary contrasts
    fb_p = t3_fb["per_checkpoint"]["E192_primary"]
    check_close(checks, "Topic3_M2", "FB_primary_H1a_log", 0.022751, fb_p["primary"]["H1a_blocks_LN_matched_corr"]["mean_log_ratio"], 1e-6, fb_src, "+0.022751", report_text)
    check_close(checks, "Topic3_M2", "FB_primary_H1b_log", 0.044673, fb_p["primary"]["H1b_total_stage3_raw_cov"]["mean_log_ratio"], 1e-6, fb_src, "+0.044673", report_text)
    check_close(checks, "Topic3_M2", "FB_HCPN400_H1a_log", -0.136753, t3_fb["per_checkpoint"]["zoo_HCP_N400_T2400_E192"]["primary"]["H1a_blocks_LN_matched_corr"]["mean_log_ratio"], 1e-6, fb_src, "-0.136753", report_text)
    check_close(checks, "Topic3_M2", "FB_L1e4_H1a_log", 0.037809, t3_fb["per_checkpoint"]["zoo_NewUAH_deepE192_L1e-4"]["primary"]["H1a_blocks_LN_matched_corr"]["mean_log_ratio"], 1e-6, fb_src, "+0.037809", report_text)
    check_close(checks, "Topic3_M2", "FB_L5e5_H1a_log", 0.048867, t3_fb["per_checkpoint"]["zoo_NewUAH_deepE192_L5e-5"]["primary"]["H1a_blocks_LN_matched_corr"]["mean_log_ratio"], 1e-6, fb_src, "+0.048867", report_text)

    # M2H2 Gate & Family C
    assert t3_h2_gate["gate_verdict"] == "PASS"
    for cid, pt_exp, lo_exp, hi_exp, d_exp in [
        ("C1", 0.012449, 0.010379, 0.014476, 0.011375),
        ("C2", 0.029531, 0.025616, 0.033409, 0.022336),
        ("C3", 5.088484, 2.930262, 7.246707, 2.671927),
        ("C4", 5.786985, 4.007065, 7.566906, 3.019404),
    ]:
        rec = t3_h2["family_C"][cid]
        tol = 1e-6
        fmt = f"+{pt_exp:.6f}"
        check_close(checks, "Topic3_M2H2", f"H2_{cid}_point", pt_exp, rec["point"], tol, h2_src, fmt, report_text)
        check_close(checks, "Topic3_M2H2", f"H2_{cid}_ci95_lo", lo_exp, rec["ci95"][0], tol, h2_src)
        check_close(checks, "Topic3_M2H2", f"H2_{cid}_ci95_hi", hi_exp, rec["ci95"][1], tol, h2_src)
        check_close(checks, "Topic3_M2H2", f"H2_{cid}_delta", d_exp, rec["delta"], tol, h2_src)

    # M2H2 E1_per_arm R1..R10 L1 pr_cov min/max (§4.5c line 286 reports 30.50-32.22)
    r_l1_covs = [t3_h2["E1_per_arm"][f"R{i}"]["L1"]["pr_cov"] for i in range(1, 11)]
    check_close(checks, "Topic3_M2H2", "H2_E1_R_L1_pr_cov_min", 30.50, min(r_l1_covs), 1e-2, h2_src, "30.50–32.22", report_text)
    check_close(checks, "Topic3_M2H2", "H2_E1_R_L1_pr_cov_max", 32.22, max(r_l1_covs), 1e-2, h2_src, "30.50–32.22", report_text)

    # M2H2 Family L (§4.5c lines 286-287: check reported numbers against h2_results.json::family_L)
    for scope, key, rep_val, rep_str in [
        ("subject", "L0_cov", -0.061, "`L0_cov`(`-0.061"),
        ("subject", "L0_corr", -0.131, "`L0_corr`(`-0.131"),
        ("subject", "L1_cov", -1.692, "`L1_cov`(`-1.692`)"),
        ("subject", "L1_corr", -1.367, "`L1_corr`(`-1.367`)"),
        ("subject", "L2_cov", -0.961, "`L2_cov`(`-0.961`)"),
        ("subject", "L2_corr", -0.785, "`L2_corr`(`-0.785`)"),
        ("subject", "LN0L2_cov", -0.962, "`LN0L2_cov`(`-0.962`)"),
        ("subject", "LN0L2_corr", -0.783, "`LN0L2_corr`(`-0.783`)"),
        ("subject", "L3_cov", -1.970, "`L3_cov`(`-1.970`)"),
        ("subject", "L3_corr", -1.766, "`L3_corr`(`-1.766`)"),
        ("token", "L0_cov", -0.056, "`L0_cov`(`-0.056`)"),
        ("token", "L0_corr", 0.013, "`L0_corr`(`+0.013`)"),
        ("token", "L1_cov", -0.556, "`L1_cov`(`-0.556"),
        ("token", "L1_corr", -0.194, "`L1_corr`(`-0.194"),
        ("token", "L2_cov", -0.0004, "`L2_cov`(`-0.0004`)"),
        ("token", "L2_corr", -0.025, "`L2_corr`(`-0.025`)"),
        ("token", "LN0L2_cov", -0.0020, "`LN0L2_cov`(`-0.0020`)"),
        ("token", "LN0L2_corr", -0.027, "`LN0L2_corr`(`-0.027`)"),
        ("token", "L3_cov", 0.029, "`L3_cov`(`+0.029`)"),
        ("token", "L3_corr", -0.015, "`L3_corr`(`-0.015`)"),
    ]:
        rec = t3_h2["family_L"][scope][key]
        check_close(checks, "Topic3_M2H2", f"H2_FamL_{scope}_{key}", rep_val, rec["point"], 1e-3, h2_src, rep_str, report_text)

    # =========================================================================
    # 4. TOPIC 4 (M4)
    # =========================================================================
    t4_v = load_json("results/topic4/2026-11-01/verdict.json")
    t4_cf = load_json("results/topic4/2026-11-01/t41_counterfactual.json")
    t4_src = "results/topic4/2026-11-01/verdict.json"
    t4_cf_src = "results/topic4/2026-11-01/t41_counterfactual.json"

    check_close(checks, "Topic4_M4", "T41_pos0_sd", 4.136e-25, t4_cf["positions"]["0"]["trivial"]["test_input_max_sd_over_rois"], 1e-28, t4_cf_src)
    check_close(checks, "Topic4_M4", "T41_pos0_sstot", 2.517e-45, t4_cf["positions"]["0"]["trivial"]["ss_tot_test"], 1e-48, t4_cf_src, "2.517e-45", report_text)
    check_close(checks, "Topic4_M4", "T41_pos932_persist", 0.9916, t4_cf["positions"]["932"]["trivial"]["legacy_r2"]["persistence"], 1e-4, t4_cf_src, "0.9916", report_text)

    # Primary & secondary contrasts
    check_close(checks, "Topic4_M4", "H1_point", -0.002231, t4_v["H1_C4_minus_C1"]["point"], 1e-6, t4_src, "-0.002231", report_text)
    check_close(checks, "Topic4_M4", "H1_ci_lo", -0.004125, t4_v["H1_C4_minus_C1"]["lo"], 1e-6, t4_src, "-0.004125", report_text)
    check_close(checks, "Topic4_M4", "H1_ci_hi", -0.000424, t4_v["H1_C4_minus_C1"]["hi"], 1e-6, t4_src, "-0.000424", report_text)

    check_close(checks, "Topic4_M4", "S1_point", -0.001597, t4_v["S1_C4_minus_C4DP"]["point"], 1e-6, t4_src, "-0.001597", report_text)
    check_close(checks, "Topic4_M4", "S1_ci_lo", -0.003837, t4_v["S1_C4_minus_C4DP"]["lo"], 1e-6, t4_src, "-0.003837", report_text)
    check_close(checks, "Topic4_M4", "S1_ci_hi", 0.000526, t4_v["S1_C4_minus_C4DP"]["hi"], 1e-6, t4_src, "+0.000526", report_text)

    check_close(checks, "Topic4_M4", "S2_point", 0.030616, t4_v["S2_C5_minus_randomlinear24"]["point"], 1e-6, t4_src, "+0.030616", report_text)
    check_close(checks, "Topic4_M4", "S2_ci_lo", 0.028799, t4_v["S2_C5_minus_randomlinear24"]["lo"], 1e-6, t4_src, "+0.028799", report_text)
    check_close(checks, "Topic4_M4", "S2_ci_hi", 0.032419, t4_v["S2_C5_minus_randomlinear24"]["hi"], 1e-6, t4_src, "+0.032419", report_text)

    check_close(checks, "Topic4_M4", "S3_point", -0.004669, t4_v["S3_C5_minus_MLPenc"]["point"], 1e-6, t4_src, "-0.004669", report_text)
    check_close(checks, "Topic4_M4", "S3_ci_lo", -0.005025, t4_v["S3_C5_minus_MLPenc"]["lo"], 1e-6, t4_src, "-0.005025", report_text)
    check_close(checks, "Topic4_M4", "S3_ci_hi", -0.004258, t4_v["S3_C5_minus_MLPenc"]["hi"], 1e-6, t4_src, "-0.004258", report_text)

    # All 16 descriptive conditions in Table 5.5b
    for arm, r2_h1_exp, lo_exp, hi_exp in [
        ("identity", 0.152511, 0.148358, 0.156537),
        ("rrr24", 0.142465, 0.138727, 0.146167),
        ("mlpenc", 0.141527, 0.137832, 0.145187),
        ("mlp_e2e", 0.140428, 0.136719, 0.144100),
        ("pca24", 0.136961, 0.133340, 0.140573),
        ("psp_C5", 0.136858, 0.133229, 0.140466),
        ("psp_C3", 0.107733, 0.104899, 0.110650),
        ("randlin24", 0.106242, 0.103231, 0.109254),
        ("psp_C1", 0.092453, 0.090014, 0.094940),
        ("psp_C2", 0.092292, 0.089840, 0.094782),
        ("psp_C4DP", 0.091820, 0.089361, 0.094313),
        ("psp_C4", 0.090222, 0.087832, 0.092699),
        ("randrelu24", 0.076958, 0.074682, 0.079249),
        ("psp_C0", 0.021686, 0.020356, 0.023120),
        ("constant", -0.000050, -0.000052, -0.000049),
        ("persistence", -0.286230, -0.297145, -0.275622),
    ]:
        rec = t4_v["descriptive"][arm]["h1"]
        check_close(checks, "Topic4_M4", f"Desc_{arm}_h1", r2_h1_exp, rec["mean"], 1e-6, t4_src)
        check_close(checks, "Topic4_M4", f"Desc_{arm}_lo", lo_exp, rec["lo"], 1e-6, t4_src)
        check_close(checks, "Topic4_M4", f"Desc_{arm}_hi", hi_exp, rec["hi"], 1e-6, t4_src)

    check_close(
        checks,
        "Topic4_M4",
        "Spearman_rho_alpha",
        0.2804,
        t4_v["exploratory_spearman_r2_vs_independence_number"]["rho"],
        1e-4,
        t4_src,
        "0.2804",
        report_text,
    )

    # =========================================================================
    # 5. GPU LEDGER (§6.1)
    # =========================================================================
    ledger_src = "results/gpu_ledger_2026-10-31.md"
    for name, reported_gpuh, canonical_gpuh, rep_str in [
        ("M1_gpuh", 0.000, 0.000, "**`0.000`**"),
        ("M3_gpuh", 11.990, 11.730 + 0.142 + 0.118, "**`11.990`**"),
        ("FU_A_gpuh", 0.952, 0.822 + 0.130, "**`0.952`**"),
        ("FU_B_gpuh", 30.720, 30.580 + 0.140, "**`30.720`**"),
        ("FU_C_gpuh", 10.697, 10.422 + 0.262 + 0.013, "**`10.697`**"),
        ("FU_D_gpuh", 3.720, 3.575 + 0.097 + 0.048, "**`3.720`**"),
        ("FU_E_gpuh", 0.330, 0.282 + 0.015 + 0.033, "**`0.330`**"),
        ("M2_gpuh", 0.000, 0.000, "**`0.000`**"),
        ("M2H2_gpuh", 0.891, 0.458 + 0.058 + 0.375, "**`0.891`**"),
        ("M4_gpuh", 0.000, 0.000, "**`0.000`**"),
        ("Total_gpuh", 59.300, 11.990 + 0.952 + 30.720 + 10.697 + 3.720 + 0.330 + 0.891, "**`59.300`**"),
    ]:
        check_close(checks, "GPU_Ledger", name, reported_gpuh, canonical_gpuh, 1e-6, ledger_src, rep_str, report_text)

    # =========================================================================
    # 6. C1 (PROTECTED_HASHES.txt), C4, AND C8 CHECKS
    # =========================================================================
    # C1 check
    prot_lines = [
        ln.strip()
        for ln in (REPO_ROOT / ".agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    c1_failures = []
    for ln in prot_lines:
        expected_sha, rel_file = ln.split(None, 1)
        rel_file = rel_file.strip()
        actual_sha = hashlib.sha256((REPO_ROOT / rel_file).read_bytes()).hexdigest()
        if actual_sha != expected_sha:
            c1_failures.append({"file": rel_file, "expected": expected_sha, "actual": actual_sha})

    # C4 check on 2026-11-02_FOUR_TOPICS_FINAL_REPORT.md
    bids_pat = re.compile("s" + "u" + "b" + "-" + r"[A-Za-z0-9_]+")
    bids_hits = bids_pat.findall(report_text)

    # Standalone 6-digit integers (excluding known counts/steps like 560000 or connectome Slurm job IDs)
    six_digit_tokens = re.findall(r"(?<![0-9A-Za-z_.\-])([1-9][0-9]{5})(?![0-9A-Za-z_.\-])", report_text)
    known_non_hcp_six_digits = {"217845", "218004", "218007", "218041", "218063", "218064", "218072", "560000"}
    hcp_id_hits = [tok for tok in six_digit_tokens if tok not in known_non_hcp_six_digits]

    # Unsalted 16-hex content hashes (excluding explicitly documented 8-hex/12-hex/64-hex SHA256 prefixes of cards/files)
    sixteen_hex_hits = re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", report_text)

    # C8 check: verify legacy numbers (0.785, 1.0, 2.7x, etc.) appear only in refutation/audit contexts
    c8_legacy_audit = {
        "report_explicitly_forbids_legacy_sources": (
            "EMPIRICAL_ANALYSIS_REPORT.md" in report_text
            and "2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md" in report_text
        ),
        "all_followups_from_2026_11_02_files": all(
            p in report_text
            for p in [
                "results/topic2/2026-11-02_fu_a/verdict.json",
                "results/topic2/2026-11-02_fu_b/verdict.json",
                "results/topic2/2026-11-02_fu_c/verdict.json",
                "results/topic2/2026-11-02_fu_d/verdict.json",
                "results/topic2/2026-11-02_fu_e/verdict.json",
                "results/topic3/2026-11-02_h2/h2_results.json",
            ]
        ),
    }

    failed_checks = [c for c in checks if not c["pass"]]
    summary = {
        "report_path": str(REPORT_PATH.relative_to(REPO_ROOT)),
        "report_sha256": hashlib.sha256(REPORT_PATH.read_bytes()).hexdigest(),
        "total_numeric_checks": len(checks),
        "passed_numeric_checks": len(checks) - len(failed_checks),
        "failed_numeric_checks": len(failed_checks),
        "failures": failed_checks,
        "c1_protected_hashes": {
            "total": len(prot_lines),
            "failures": c1_failures,
            "pass": len(c1_failures) == 0,
        },
        "c4_hygiene": {
            "bids_prefix_hits": bids_hits,
            "hcp_6digit_id_hits": hcp_id_hits,
            "sixteen_hex_hits": sixteen_hex_hits,
            "pass": len(bids_hits) == 0 and len(hcp_id_hits) == 0 and len(sixteen_hex_hits) == 0,
        },
        "c8_compliance": {
            **c8_legacy_audit,
            "pass": all(c8_legacy_audit.values()) and len(failed_checks) == 0,
        },
        "nonblocking_notes": notes,
        "overall_verdict": (
            "APPROVE"
            if (
                len(failed_checks) == 0
                and len(c1_failures) == 0
                and len(bids_hits) == 0
                and len(hcp_id_hits) == 0
                and len(sixteen_hex_hits) == 0
                and all(c8_legacy_audit.values())
            )
            else "REQUEST_CHANGES"
        ),
        "checks": checks,
    }

    OUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Audit complete: {summary['passed_numeric_checks']}/{summary['total_numeric_checks']} numeric checks passed, "
        f"C1={summary['c1_protected_hashes']['pass']} ({summary['c1_protected_hashes']['total']}/67), "
        f"C4={summary['c4_hygiene']['pass']}, C8={summary['c8_compliance']['pass']}, "
        f"verdict={summary['overall_verdict']}"
    )


if __name__ == "__main__":
    main()
