# BRIEFING — writer_report

## Mission
Write the canonical integrated four-topic report `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` (`ACCEPTANCE.md` `R1`) after all 10 milestones (`M1`, `M2`, `M2H2`, `M3`, `FU_A`, `FU_B`, `FU_C`, `FU_D`, `FU_E`, `M4`) have achieved 5-verifier strict gate `PASS` and `VERIFIED_COMPLETE` victory audit.

## Identity & Ownership
- Role: `writer_report` (worker)
- Run: `tw-20261031-four-topics` (Workflow C, Phase `Report`)
- Exclusive write targets:
  - `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md`
  - `/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/writer_report/{DISPATCH.md,BRIEFING.md,progress.md,handoff.md}`

## Key Constraints
- **C1–C8 Compliance**:
  - `C1`: Do not touch any file in `PROTECTED_HASHES.txt` (`67/67 OK`).
  - `C4`: Zero participant IDs (`BIDS` prefix, 6-digit HCP IDs, 16-hex content hashes).
  - `C5`: State every card verdict verbatim (`KILLED`, `stop`, `inconclusive`, `keep`, `supported`, `non-inferior`, `TE+`, `EQ`, `INC`); never reframe a killed or inconclusive result as success.
  - `C8`: Every result number is traced to a dated artifact produced in this run (`results/...` or `docs/03_empirical_analysis/topic*/2026-11-0[12]_*.md`). Zero numbers cited from `EMPIRICAL_ANALYSIS_REPORT.md` or `2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md`.
- **Genre & Honorific**: Korean, objective third-person institutional report voice (no `나는`/`저는`/`생각한다`/`믿는다`); refer to the proposer as `손운규 교수님`.
