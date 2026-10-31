# Topic 1 result: ENIGMA-OCD directed lag-motif enrichment, full cohort (step 5)

- Date: 2026-10-31. Run tw-20261031-four-topics, worker_M1_r1.
- Governing documents:
  - the frozen card `2026-10-30_topic1_analysis_card.md` (sha256 `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`, unchanged);
  - the frozen pre-label addendum `2026-10-31_topic1_prelabel_addendum.md` (sha256 `7ccb983ed9dedd50d9c74b433e2578a7007b11ee5397a276832382a39f55e90e`);
  - the deviations addendum `2026-10-31_topic1_deviations_addendum.md`.
- Every number below comes from `results/topic1/2026-10-31/`. None is taken from `EMPIRICAL_ANALYSIS_REPORT.md` (C8).

## 1. Verdict (card §5, applied exactly)

**Topic 1 is KILLED: neither primary endpoint survives.**

The primary unit is broadband@0.10: n = 1,706 (869 OCD, 837 HC), 23 sites, 0 exclusions.
- d = β_LMM / σ_ε(LMM), with the sign OCD − HC.
- p is the Freedman–Lane p, within site, B = 9,999, seed 20261031.
- Holm is applied over E1 and E2.

| Endpoint | d | p_FL | p_Holm | Survives? | Reason |
|---|---|---|---|---|---|
| E1 = Z030C | **0.113** | 0.0223 | **0.0446** | no | \|d\| < 0.15 |
| E2 = Z030C − Z030T | 0.038 | 0.4416 | 0.4416 | no | p_Holm ≥ 0.05 and \|d\| < 0.15 |

**How to read E1.**
- E1 passes the Holm-corrected test (p_Holm = 0.0446) but fails the pre-registered effect-size bar (|d| ≥ 0.15). Card §5 named this case in advance: p_Holm < 0.05 corresponds to about |d| ≥ 0.11, so the d bar is the binding condition.
- The direction is OCD > HC in directed 3-cycle enrichment.
- The approximate Wald 95 % interval for d is [0.015, 0.212] (derived and descriptive; `report_derived_numbers.json`).
  - It excludes 0 and includes 0.15.
  - So the data neither exclude a small positive effect nor establish d ≥ 0.15.
- The kill is a decision under the pre-registered rule. **It is not evidence that the effect is absent.**

**Model checks (card §4 and addendum P5).**
- **E1:** |β_LMM − β_FE| = 1.3e-13·SE (the stop limit is 0.01·SE). MixedLM converged with 0 warnings. Scale ratio LMM/FE = 0.998. Site variance 1.67, with σ_ε = 4.85.
- **E2:** |β_LMM − β_FE| = 2.0e-13·SE. Converged with 0 warnings. Scale ratio 0.998.
- Applying the same rule with d_FE gives the same result: E1 d_FE = 0.113 and E2 d_FE = 0.038, so neither survives.

**Other numbers for the primary endpoints.**

| | E1 | E2 | Status |
|---|---|---|---|
| LMM Wald p (secondary) | 0.024 | 0.45 | secondary |
| Raw pooled Cohen d | 0.087 | 0.020 | descriptive only, miscalibrated under the site × dx imbalance |
| Raw Welch p | 0.072 | 0.68 | descriptive only, miscalibrated under the site × dx imbalance |

**Card §9 limitation, beside the verdict.** Directed lag motifs can arise without any neural coupling.
- In the frozen synthetic probes (`results/topic1/2026-10-30/spurious_direction.json`), a shared driver with per-ROI latency SD 1–2 s shifts Z030T by about −7.6 and E2 by about +7. With SD 2 s, Z030C ≈ −1.9.
- Neither the oriented null nor the curl channel removes this.
- So a group difference in regional hemodynamic latency, in global-signal amplitude, or in slice timing could produce an E1 or E2 group difference. No motion data exist to check this, and the npy preprocessing provenance (GSR, slice timing) is unverified.
- The gradient-share covariate row (§7) was not run, because no endpoint survived. Raw group means of gradient share are OCD 0.217 and HC 0.233 (descriptive).

**Degeneracy, beside the verdict.**
- At the primary unit, 0 of 1,706 are degenerate for E1 or E2: 0 % in each group and in each of the 23 sites.
- The fallback did not trigger (`fallback_decision.json`, written before any label read).
- broadband@0.05: 2 of 1,706 degenerate (0.12 %, OCD 0.115 % vs HC 0.119 %).
- broadband@0.15 and all curl units: 0.

## 2. Exclusions, acceptance and length (card §3; addendum P11 and P16)

**Exclusions.** At the primary unit there are 0 extraction failures, 0 missing covariates, 0 degenerate for E1 and 0 for E2, in total, by group, by site and by site × group (`stats_results.json` → `exclusions_primary_unit`).

**Acceptance.** Acceptance of the null chain (acceptance_mean) at the primary unit includes 2-swap no-ops (addendum r2 item 31).

| | Mean | 10th percentile |
|---|---|---|
| OCD | 0.632 | 0.484 |
| HC | 0.621 | 0.482 |

- Per-site means range from 0.484 (New-York) to 0.743 (Braga-UMinho-Braga-1.5T).
- All six units are reported by group in `descriptives_all_units`. Acceptance falls with density: broadband 0.718 at 5 %, 0.632 at 10 %, 0.560 at 15 % (OCD shown; HC 0.706, 0.621, 0.549).

**Grid length on the 2 s grid.**
- 100–340 samples, median 160, the same median in both groups.
- No subject is below the 100-sample (200 s) floor.
- The two Bellvitge 1.5T sites sit at the floor (median 100).

**Site × group cells.** There are 46 cells, ranging from 10 to 189 subjects.

## 3. Secondary analyses (card §6)

They cannot rescue a killed primary.

**Family 1: site-held-out classification.**
- Descriptive, no p-value (addendum P7).
- LeaveOneGroupOut over 23 sites, n = 1,706.
- 95 % CIs are site-level bootstrap, 2,000 resamples.

| Model | Pooled out-of-fold AUROC (95 % CI) | Mean per-site AUROC |
|---|---|---|
| Lag motif [Z030C, Z030T, gradient share] @0.10 | 0.516 [0.468, 0.560] | 0.555 |
| In-house static FC (PCA 50), same subjects and folds | 0.563 [0.524, 0.600] | 0.559 |

- The lag-motif features did not classify better than the static-FC comparator.
- The external file-backed baselines in card §6 (MBBN 0.65–0.66, random splits) use other folds and are **not comparable**.

**Family 2: Y-BOCS within OCD** (n = 856, 23 sites; site-FE OLS, Freedman–Lane p, BH over E1 and E2).

| Endpoint | Standardised β | p_FL | q_BH |
|---|---|---|---|
| E1 | 0.032 | 0.307 | 0.361 |
| E2 | 0.029 | 0.361 | 0.361 |

**Family 3: medication within OCD.**
- Code 1 (n = 180) vs code 2 (n = 121), in the 11 sites that have both codes, with site fixed effects.
- The coding direction is unconfirmed, so no medication interpretation is made.

| Endpoint | β (code 1 − code 2) | d_FE | p_FL | q_BH |
|---|---|---|---|---|
| E1 | −0.55 | −0.086 | 0.568 | 0.568 |
| E2 | −2.16 | −0.199 | 0.155 | 0.310 |

**No secondary family has a BH-significant result.**

**Degeneracy-safe secondary outcome (card §3).** The 030C log ratio gives d = 0.090, p_FL = 0.067.

**Post-freeze, descriptive (addendum P10).** After excluding subjects at or below the pooled 10th percentile of acceptance (0.484), n = 1,535:

| Endpoint | d | p_FL |
|---|---|---|
| E1 | 0.130 | 0.014 |
| E2 | 0.095 | 0.067 |

This cannot change the verdict.

## 4. Card §7 sensitivity analyses

They were **not run and are not interpreted**, because no endpoint survived (card §5/§7; `stats_sensitivity.json`). The §7 extraction variants (DCT 128 s, common 200 s truncation, attempts factor 40) were therefore not extracted.

## 5. How the result was produced (T1.1–T1.4)

**T1.1: tests for the extract_subject contract.**
- Added `tests/topic1_lagmotif/test_extract_contract.py` (sha `9d7121e4…`), with 5 tests:
  - m = round(d·46,056);
  - valid_T after the head trim;
  - curl = F minus its gradient part;
  - the SeedSequence rule per position, channel and density;
  - Σ SP² = 1.
- The victory-audit mutants were rerun on the final tree, from adapted copies (receipts in `results/topic1/2026-10-31/t1_1_mutation/v3_final_tree/`):

| | Control | Mutants killed |
|---|---|---|
| With the new tests | 89 passed | 19/19 (`mutants.py`), 4/4 (`mutants_extra.py`): **0 survivors** |
| Without them | — | the 5 audit survivors are reproduced |

- The auditor's original receipts are unchanged.

**T1.2: `scripts/topic1_cohort_stats.py`** (sha `33e27576…`, recorded before the label join).
- It was validated on the real 1,706-subject site × dx × age × sex × duration design with synthetic outcomes (`stats_validation_final.json`, all_pass):
  - the vectorised Freedman–Lane t equals a statsmodels refit to 2e-13;
  - every permutation stays within its site;
  - null FPR at R = 2,000 (B = 999) was 0.0545, 0.0525 and 0.0435 in three site structures, all inside the 3-SE band [0.035, 0.065];
  - at B = 9,999 (R = 300) it was 0.077, inside the band;
  - Welch was miscalibrated: FPR 0.9995 with aligned site effects;
  - planted d = 0, 0.15 and 0.30 were recovered as 0.0005, 0.143 and 0.303, each within 3 MC-SE;
  - the two wrong-σ definitions fall outside;
  - the Holm, kill-rule and fallback boundaries are correct.
- Stats mutants: 24/24 killed.
- It went through a Trinity code review, which is incomplete; see the deviations addendum, item 1.

**T1.3: pinned manifest** (`manifest.json`, sha `063513c9…`).
- 1,706 positions, each with site, TR, raw_valid_T, n_trim, valid_T, duration and grid length.
- One salted cohort-level digest; no per-position ID hashes.
- All 1,706 pass the data contract and the 100-sample floor.

**T1.4: extraction** (`extract_primary.log`, `extract_primary_header_1793434575.json`).
- Run on local CPU, 14 processes at nice 10, with the frozen PARAMS (params_sha256 `86863ffa…` on every row).
- The card §12 code hashes were verified at start.
- Results: 1,706 ok, 0 errors, 4,292 s wall.
- The JSONL sha256 is `948961c8…518e`.
- Statistics: `analyze.log`, and `stats_results.json` (sha `1713e370…f11d`).

No participant ID appears in any output; positions are indices into the manifest.

## 6. What this means for Topic 1

- Under its own pre-registered rule, Topic 1 is killed at the primary density.
- The one nominally detectable signal (E1, OCD > HC, d ≈ 0.11) is below the bar the card set in advance. It is also exposed to the latency and global-signal confound in §9, which this data set cannot rule out (no motion data, unknown preprocessing).
- Lag-motif features did not out-classify static FC in site-held-out classification.
- Any follow-up needs a new dated card, and should address the §9 confound first: latency mapping, a cohort with motion data, or HRF-deconvolved series.
