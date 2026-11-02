# Handoff — writer_report (Integrated Four-Topic Final Report)

## 1. Observation
- All 10 milestones across `tw-20261031-four-topics` (`M1`, `M2`, `M2H2`, `M3`, `FU_A`, `FU_B`, `FU_C`, `FU_D`, `FU_E`, `M4`) have passed their 5-verifier strict gate and received `VERIFIED_COMPLETE` from their independent victory auditors (`victory_M1_b`, `victory_M2`, `victory_M2H2_r2`, `victory_M3_r3`, `victory_FU_A_r1`, `victory_FU_B_r1`, `victory_FU_C_r3`, `victory_FU_D_r3`, `victory_FU_E_r1`, `victory_M4`).
- Created `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` satisfying `ACCEPTANCE.md` `R1` and `C1–C8`:
  - **§1 (1-Page Executive Summary Table)**: Summarizes all 10 milestones (`M1`, `M3`, `FU_A`, `FU_B`, `FU_C`, `FU_D`, `FU_E`, `M2`, `M2H2`, `M4`) with exact card verdicts, primary headline statistics and 95% CIs, GPU-h used vs cap, 5-verifier gate + victory audit status, and source paths.
  - **§2 (Topic 1 — `M1`, ENIGMA-OCD Directed Lag Motifs)**: Documents the research question (손운규 교수님 proposal), pre-freeze card rule (`|d| >= 0.15` and `p_Holm < 0.05` on at least one of `E1`, `E2`), data/compute (`N=514`, `248 OCD / 266 HC`, `10` sites, `0.000 GPU-h`), verdict **`KILLED`** (`E1`: `d = 0.113`, `p_FL = 0.0223`, `p_Holm = 0.0446 < 0.05` fails `|d| >= 0.15`; `E2`: `d = 0.038`, `p_Holm = 0.4416`), `S1–S4` and `C1–C4` secondary/control metrics, Addendum 01 deviations (`D1–D4`), and untested/follow-up requirements.
  - **§3 (Topic 2 — `M3` + `FU-A..FU-E`, SwiFT Connectome Box Pooling at `M0`)**: Documents `M3` r1/r3 (`stop (killed)`, `I1 = +0.147% [-0.068%, +0.361%]`) and all five PI Decision 7 follow-up options on NIPA B300 Slurm: `FU_A` (`inconclusive (measurement capacity)`, `F+` `+0.5511% < 1%`), `FU_B` (`stop (killed)`, `I1 = +0.063% [-0.299%, +0.425%]`), `FU_C` (`stop (killed)`, `I1 = -0.113% [-0.499%, +0.272%]`), `FU_D` (`inconclusive (measurement capacity)`, `F+` `+0.3631%` and `+0.6546% < 1%`), and `FU_E` (`inconclusive (measurement capacity)`, `S_s2` failed synthetic `F+` `5.76 <= 10.59`, counterfactual `J1 = +8.11% [-6.60%, +22.81%]` also `inconclusive`), along with all addenda (`addendum_01`–`addendum_06` for `M3`, and per-option addenda).
  - **§4 (Topic 3 — `M2` + `M2H2`, Layerwise PR/Spectra & Random-Init Control)**: Documents `M2` (`J1` fails -> `stop`, `R1` `inconclusive`, `R2` `stop`, `D1` `keep`, `H1a` holds in opposite direction `L3 > L2` under ceiling `<= 7`, `H1b` `not replicated`, `D3` matched-`n=25` `keep`, `R4/R6` `stop`, `R5` `untestable`, `R7` `not comparable`) and `M2H2` (`C1/C2 = INC` for token-level `H1a`, `C3/C4 = TE+` confirming the subject-level `L1 -> L2` drop `D1` is 100% learned, `L0` subject-level `INC`, `L1` `EQ`, `L2/L3` `TE+`, plus Addendum 03 and Addendum 08 `E1–E8` errata and the `victory_M2H2_r2` `31.0–34.0` rounding correction).
  - **§5 (Topic 4 — `M4`, Backprop-Free Local Learning)**: Documents `T4.1` root-cause proof (`position 0` tail padding after `max_T = 364` on `T = 176` sequences), `H1` (`C4 - C1` = `-0.0022 [-0.0041, -0.0004]`, **`stop (killed)`**), `S1` (`C4 - C4DP` = `-0.0016 [-0.0038, +0.0005]`, **`killed`**), `S2` (`C5 - randlin24` = `+0.0306 [+0.0288, +0.0324]`, **`supported`**), `S3` (`C5 - MLPenc` = `-0.0047 [-0.0050, -0.0043] > -0.01`, **`non-inferior`**), and `C3` (`10/50 = 20% > 10%` unstable, **`inconclusive (execution integrity)`**).
  - **§6 (Compute Ledger & Governance)**: Documents the full run GPU usage (`59.300 GPU-h` <= `95.0 GPU-h` ceiling; `47.570 GPU-h` in Workflow C across B300 and connectome; `0.000 GPU-h` on local DGX-Spark GB10) and `C1–C8` compliance.

## 2. Logic Chain
1. Every number in `2026-11-02_FOUR_TOPICS_FINAL_REPORT.md` was extracted directly from the dated JSON/TSV/CSV artifacts in `results/` and cross-checked against the dated result reports and addenda in `docs/03_empirical_analysis/topic{1,2,3,4}/` and the 10 `victory_*/handoff.md` files.
2. Specific known rounding/prose errata identified during milestone gates and victory audits (`M2` Addendum 03 §5 `+3.22` and `-3.28`; `M2H2` Addendum 08 §5 `E1–E8` including `C3` closest to boundary, `R1` descriptive `-1.61 [-3.77, +0.56]`, `L0` subject-level `INC`, and `victory_M2H2_r2` `31.0–34.0`) were incorporated directly so the final report is consistent with both raw JSONs and addenda.
3. No numbers were taken from `EMPIRICAL_ANALYSIS_REPORT.md` or `2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md` (`C8`).

## 3. Caveats
- Subject to independent verification by `numbers_audit_report` (`paper-numbers-auditor`) and `claim_audit_report` (`critic`).

## 4. Conclusion
- Status: **`DONE`**
- Deliverable: `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md`

## 5. Verification Method
- Run `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` (`67/67 OK`).
- Run `numbers_audit_report` and `claim_audit_report` against `/home/juke/git/00IITP-AI/docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md`.
