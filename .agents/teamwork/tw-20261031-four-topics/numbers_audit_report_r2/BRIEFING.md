# BRIEFING — `numbers_audit_report_r2` (`paper-numbers-auditor`)

## Scope
1. Execute `/home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers_r2.py` against the revised `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` (`sha256 = 1e73544577244cbe72e222eab9ee422a3911c31e396ff9061404fe5a121f6be1`).
2. Save output to `/home/juke/git/00IITP-AI/verification/numbers_audit_report/audit_numbers_r2.out.json`.
3. Verify resolution of Round 1 `BLOCKING-1`..`BLOCKING-4` and check whether any residual numeric discrepancy remains.
4. Return `APPROVE` only if zero discrepancies remain; otherwise `REQUEST_CHANGES` with exact replacement text.
