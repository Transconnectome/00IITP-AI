# BRIEFING — numbers_audit_report

## Context
Milestone `Report` (`R1` of `ACCEPTANCE.md`) produces the final integrated four-topic report `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` covering all 10 milestones across Topic 1 (`M1`), Topic 2 (`M3`, `FU_A`, `FU_B`, `FU_C`, `FU_D`, `FU_E`), Topic 3 (`M2`, `M2H2`), Topic 4 (`M4`), and the overall GPU ledger (`results/gpu_ledger_2026-10-31.md`).

## Scope
1. Read `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` in full.
2. Programmatically extract and verify every result number, confidence interval, p-value, sample size, test count, mutation count, SHA256 prefix, and GPU-hour figure in `2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` against the canonical dated result files under `results/topic{1,2,3,4}/`, `docs/03_empirical_analysis/topic{1,2,3,4}/`, `results/gpu_ledger_2026-10-31.md`, and `.agents/teamwork/tw-20261031-four-topics/victory_*/` via `/home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers.py` -> `/home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers.out.json`.
3. Verify C8 compliance: zero numbers cited as results from `EMPIRICAL_ANALYSIS_REPORT.md` or `2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md` (legacy artifacts `PR ≈ 1.001–1.074` in Topic 3 `J1` and `R^2 = 1.0` / `PR ≈ 1.005` in Topic 4 `T4.1` are explicitly diagnosed and refuted from `t3_1_provenance_repro.json` and `t41_counterfactual.json`).
4. Verify C1 (`PROTECTED_HASHES.txt`) and C4 hygiene (zero BIDS subject prefixes, 6-digit HCP IDs, or unsalted 16-hex content hashes in `2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` and in our audit artifacts).

## Constraints
- Strictly read-only on `docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` and all production files.
- Write metadata only to `.agents/teamwork/tw-20261031-four-topics/numbers_audit_report/` and verification script/JSON only to `verification/numbers_audit_report/`.
- Zero git writes; strict C4 hygiene.
