# DISPATCH — numbers_audit_report

- **Agent ID**: `numbers_audit_report`
- **Role**: `paper-numbers-auditor`
- **Run**: `tw-20261031-four-topics` (General route, Workflow C, Phase `Report`)
- **Workspace**: `/home/juke/git/00IITP-AI`

## Task Specification (`workflow_C_script.js.txt`, line 149)
> "Read-only numbers audit of `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md`. Extract every result number and check it against the dated result files under `/home/juke/git/00IITP-AI/results/` and `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic*/` that the report cites. List each unsupported, mismatched or C8-forbidden number (anything from `EMPIRICAL_ANALYSIS_REPORT.md` or the `2026-11-01` consolidated status). APPROVE only if none; else REQUEST_CHANGES with the list in `blocking_issues`."
