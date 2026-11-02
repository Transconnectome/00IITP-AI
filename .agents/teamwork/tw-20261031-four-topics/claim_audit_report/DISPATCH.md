# DISPATCH — claim_audit_report

## 2026-11-02T06:11:13Z (received from parent 322896b4-0224-4073-8928-08430357fda3; verbatim)

You are `claim_audit_report` (`critic`) in Teamwork run `tw-20261031-four-topics` (General route, Workflow C, Phase `Report`), working in `/home/juke/git/00IITP-AI`.

### Your Task
Perform an adversarial claim audit of `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` as specified in `/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/workflow_C_script.js.txt` (line 150):
> "Adversarial claim audit of `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` against the governing cards and victory reports (`/home/juke/git/00IITP-AI/docs/03_empirical_analysis/topic*/`, `/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/victory_*/`, `/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md`). Find overclaims, verdicts that do not follow the card rule, killed results framed as success, missing untested items, gate/victory status misstated, and any participant ID. APPROVE or REQUEST_CHANGES with `blocking_issues`."

### Step-by-Step Instructions
1. Read `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` completely.
2. Cross-examine every claim, verdict, caveat, addendum disclosure, untested item, follow-up requirement, and gate/victory status against:
   - `.agents/teamwork/tw-20261031-four-topics/sentinel/ACCEPTANCE.md` (especially `R1` and `C1–C8`)
   - `.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md` and `PI_DECISIONS_2026-11-01.md`
   - All 10 victory reports: `.agents/teamwork/tw-20261031-four-topics/victory_{M1_b,M2,M2H2_r2,M3_r3,M4,FU_A_r1,FU_B_r1,FU_C_r3,FU_D_r3,FU_E_r1}/handoff.md`
   - The governing cards, result reports, and addenda under `docs/03_empirical_analysis/topic{1,2,3,4}/`.
3. Specifically check and verify via a script `/home/juke/git/00IITP-AI/verification/claim_audit_report/audit_claims.py` (saving `/home/juke/git/00IITP-AI/verification/claim_audit_report/audit_claims.out.json`):
   - **Genre & Voice**: Korean, objective third-person report voice (zero occurrences of first-person `나는`, `내가`, `저는`, `생각한다`, `믿는다`), and proper honorific `손운규 교수님`.
   - **Verdict Fidelity (`C5`)**: Every killed/stop verdict (`M1` `KILLED`, `M3` `stop`, `FU_B` `stop`, `FU_C` `stop`, `M2` `J1`/`R2`/`R4`/`R6` `stop`, `M4` `H1`/`S1` `stop`/`killed`) is stated as killed/stop and NEVER reframed as a partial success, "trend", or "promising signal". Every `inconclusive` verdict (`FU_A`, `FU_D`, `FU_E`, `M2` `R1`, `M2H2` `C1/C2`/`L0`, `M4` `C3`) is stated as `inconclusive` with its exact card/addendum reason.
   - **Card Rule Completeness**: Each of the 4 topics includes: (1) research question, (2) frozen card rule, (3) data and compute, (4) verdict exactly as the card's rule gives it, (5) key numbers with intervals, (6) gate + victory status, (7) deviations/addenda, (8) what remains untested, and (9) what a follow-up would need, plus a 1-page summary table first.
   - **Addenda & Victory Caveat Alignment**:
     - `M2` Addendum 03 §5 errata (`D1` cov lower bound `+3.22`, `deepE192 L5e-5` `A1b` corr `-3.28`)
     - `M2H2` Addendum 08 §5 `E1–E8` (`C3` closest to boundary `f <= 0.5483`, `R1` descriptive `-1.61 [-3.77, +0.56]`, `L0` subject-level `INC`, and `victory_M2H2_r2` untrained `pr_cov` at L2/L3 `31.0–34.0`)
     - `M3` Addendum 06 (`V01–V11` and `F+` failure card-vs-code erratum)
     - `FU_C` Addendum 01 & 02 (`E1–E12`), `FU_D` Addendum 01 & 02 (`E1–E9`, `W1–W5`, `P1`), `FU_E` Addendum 01 (counterfactual `J1 = +8.11% [-6.60%, +22.81%]` still `inconclusive`).
   - **C4 Participant-ID Hygiene & C1 Protected Hashes**: Scan `2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` for BIDS `s-u-b-` prefix, 6-digit HCP IDs, ENIGMA IDs, and 16-hex content hashes; verify `PROTECTED_HASHES.txt` (`67/67 OK`).
4. Write your exclusive metadata directory `/home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/claim_audit_report/`:
   - `DISPATCH.md`
   - `BRIEFING.md`
   - `progress.md`
   - `handoff.md` (5-section format + `VERDICT_SCHEMA` JSON block at the bottom).
   - **CRITICAL**: Do NOT put any `.py`, `.sh`, or `.csv` files inside `.agents/teamwork/...` (put scripts/outputs only in `/home/juke/git/00IITP-AI/verification/claim_audit_report/`).
5. Do NOT modify `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` or any file outside `.agents/teamwork/tw-20261031-four-topics/claim_audit_report/` and `verification/claim_audit_report/`.
6. When finished, send your full verdict and JSON summary back to your parent agent using `send_message`.
