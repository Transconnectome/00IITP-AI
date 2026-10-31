# Topic 1: deviations addendum for the full-cohort run (T1.5)

- Date: 2026-10-31. Run tw-20261031-four-topics, worker_M1_r1.
- Written **after** `analyze` ran (2026-10-31T11:15Z). It adds to the frozen card `2026-10-30_topic1_analysis_card.md` (sha256 `1e589f0b…75aa`, unchanged) and to the frozen pre-label addendum `2026-10-31_topic1_prelabel_addendum.md` (sha256 `7ccb983e…e90e`, unchanged, read-only). It changes neither file.
- Result report: `2026-10-31_topic1_result_report.md`.

## 1. Degeneracy fallback (card §3): not triggered

- `fallback_decision.json` was written at 11:14:54Z, before any label was read, from the primary extraction alone. Its sha256 is `be784654…18df`.
- At broadband@0.10, 0 of 1,706 subjects were degenerate for E1 and 0 for E2. The rule is "> 10 % for E1 or E2", so the primary density stays **0.10**.
- No second density is therefore reported as primary.
- Other units:
  - broadband@0.05: 2 of 1,706 degenerate for both E1 and E2 (0.12 %);
  - broadband@0.15 and curl at all three densities: 0.

## 2. Deviations from the card or from the planned order

Each item is either disclosed in the pre-label addendum (cited) or is new here.

| # | Deviation | Where recorded | Effect on the verdict |
|---|---|---|---|
| 1 | **Review route.** Card §12 requires an independent review of the cohort script before execution. The available review was a Trinity code review: codex failed, and the saved log is cut off partway through round 1. No fresh native agent reviewed the script, because the worker cannot spawn one. The script was instead validated on the real design with synthetic outcomes, and mutation-tested (24/24 mutants killed). | pre-label D4 | None on the computation. The review requirement is only **partly met**; a native independent audit is still owed. |
| 2 | **Order.** The label-free primary extraction started (08:16Z) before the stats script was final. No label was read by the extraction, and no feature value was inspected before the freeze. | pre-label D1 | None |
| 3 | **Validation read the real design.** The real dx, age, sex and site design and the manifest durations were combined with synthetic outcomes. A labels-only count probe was also run. | pre-label D2 | None |
| 4 | **Two validation runs.** Run 2 bound bytes `f2589105…`. After the review amendments the final bytes `33e27576…` were validated again. Every validation number is identical except the timings. | pre-label D4; `stats_script_sha256.txt` | None |
| 5 | **Card gaps settled by the addendum:** (a)–(h), the grid floor, P14–P17 and V1–V4. Family 1 has no p-value (gap f), so BH is applied only in families 2 and 3. | pre-label P/V/G | None |
| 6 | **New descriptive number.** The approximate Wald 95 % interval for d in the result report is a derived quantity that neither the card nor the addendum names (`report_derived_numbers.json`). | here | None. It is descriptive only. |
| 7 | **No §7 extraction variants were run** (DCT 128, 200 s truncation, attempts factor 40), and no §7 row was computed. This follows card §5/§7, because no endpoint survived; `stats_sensitivity.json` says so. | card §7 | None. This is the rule. |

- `src/topic1_lagmotif/` and `scripts/topic1_timing.py` were not changed: the card §12 hashes match 10 of 10.
- No frozen parameter was changed after any result. All 1,706 primary rows carry params_sha256 `86863ffa…`.

## 3. Disclosed post-freeze analysis

- The acceptance-stratified refit (pre-label P10, post-freeze by design) was run, and is descriptive.
- It cannot change the verdict.
