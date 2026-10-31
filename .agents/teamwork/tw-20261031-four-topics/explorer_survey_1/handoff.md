# explorer_survey_1 — handoff (run tw-20261031-four-topics, survey; lens M1)

**Summary.**
- **Where to run.** Run M1 on the local DGX-Spark CPU, not on connectome. Connectome has no numba and no statsmodels, and its Python is 3.8.
- **What to do first.**
  - T1.1 changes tests only.
  - New logic goes in `scripts/topic1_*`; `src/topic1_lagmotif/*` must stay byte-identical, because the card's §12 hashes cover it.
  - The degeneracy fallback is decided label-free, and before any label join.
- **Compute budget (추정).** All carded units plus the extraction-level sensitivities come to about 20–22 CPU-h, which is 1.5–2 h of wall time on 12–14 nice processes.
- **Secondary topics.**
  - T3: PR ≈ 1 comes from uncentered SVD. The mean vector holds 96–99.9% of the energy. This is confirmed.
  - T4: in 5 of 5 probed subjects, the R² = 1.0 test window is 100% padding. The mechanism is a hypothesis.
  - T2: in SwiFT_v2 ver7 the last stage has no PatchMerging. Whether that explains the 1536/1536 shapes is not verified.

## 1. Observation

### 1a. Frozen state (verified 2026-10-31 ~07:30Z)
- **Card.** `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md`, sha256 `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`. It is in PROTECTED_HASHES.
- **Frozen code (card §12).** The card hashes 10 code files: `src/topic1_lagmotif/{__init__,data,flow,motifs,pipeline,preprocess,spurious,synthetic,tr_table}.py` and `scripts/topic1_timing.py`.
  - These files are **not** in this run's PROTECTED_HASHES.
  - Editing any of them would still invalidate the card, which says "Any change … requires a new dated card".
  - The run layout in `orchestrator/PROJECT.md` gives M1 these paths: `tests/topic1_lagmotif` (additive), `scripts/topic1_*`, `results/topic1/2026-10-31` and `docs/.../topic1/2026-10-31_*`. It does not give M1 `src/topic1_lagmotif`.
- **`pipeline.extract_subject`, lines 87–95.** It returns `gradient_share`, `results[f"{ch}@{d:.2f}"]` (each from `motif_statistics`) and `position, tr, valid_T, n_trim, duration_s, raw_valid_T, params_sha256`.
- **`motifs.motif_statistics`, lines 244–264.**
  - `degenerate` holds the flags `{030T, 030C}`, each meaning `sd == 0` exactly.
  - Near-degenerate nulls, where sd is tiny but not zero, are not flagged.
  - `acceptance_mean` counts 2-swap no-ops as accepted moves (addendum item 31).
- **Victory audit survivors.** These mutants survive all 53 tests (`verification/victory_auditor_1/mutation_results*.json`; extra results: all rc=0, "54 passed"):
  - `roi_subsample_80`;
  - `curl_returns_F`;
  - `seeds_ignore_position`;
  - `sp_not_normalised`;
  - `extract_subject_drops_valid_T`.
- **The mutant harnesses write over the auditor's own receipts.**
  - `verification/victory_auditor_1/mutants.py:7` hardcodes `BASE = …/verification/victory_auditor_1/mut`.
  - `mutants.py:66` writes `verification/victory_auditor_1/mutation_results.json`.
  - `mutants_extra.py` imports `mutants` and writes `…/mutation_results_extra.json`.
  - The mirrors copy `tests/topic1_lagmotif` (`mutants.py` `build()`), so new tests added there are picked up.

### 1b. Compute environment (read-only probes)

**Local DGX-Spark**
- 20 CPUs, load average about 7, 60 GB available.
- `mutagen-agent` uses about 131% CPU.
- `/home/juke/superclaude-env`: numpy 2.3.5, scipy 1.15.3, numba 0.62.1, statsmodels 0.14.6, sklearn 1.7.2, pandas 2.3.3, networkx 3.4.2.

**connectome** (`ssh connectome`, 16:31 KST)
- Slurm view: node1 is mixed (20 of 96 CPUs allocated, 88 GB free); node2 is mixed (2 of 96, only 6 GB free); node3 is down; node4 is idle (96 CPUs, 506 GB free).
- 14 jobs in the queue, several of them PENDING.
- `/usr/bin/python3` is 3.8.10, with numpy 1.22.3, scipy 1.8.0 and sklearn 1.1.0.
- **numba and statsmodels are both `ModuleNotFoundError`.**
- No conda or uv was found, and `module` is not available.
- `/storage` is 465 T in total, 97% used, with 17 T free.

**ENIGMA data already on lab servers.** Nothing was copied.
- Two copies hold 1,706 npy files each: `/storage/connectome/ic_loss_work/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25` and `/storage/connectome/<lab-user>/ENIGMA_OCD_MBBN/MBBN_data_304_ROIs_0.25`.
- The sorted list of "relative-path size" lines has the same sha256 prefix, `da24bc10dc0febfd`, locally and in both remote copies. This is a list-level digest only: the file contents were not hashed.
- The metadata CSV has the same sha256 prefix, `f7c21d7af784af08`, locally and in the ic_loss_work copy.
- dgx1 and B300 were **not** checked.

### 1c. Cohort design (metadata only; counts, no IDs)
- **Completeness.** 1,706 rows on disk, no duplicate IDs. Age has 0 NaN and Sex has 0 NaN. Y-BOCS has 727 NaN, Medication 262 NaN.
- **Sites.** All 23 sites contain both diagnoses, so no site is single-dx.
- **Site OCD fraction.** It ranges from 0.175 (Bellvitge-RESP-CBT-3T, 10/57) to 0.817 (New-York, 49/60).
- **Under-18 participants.** 192 in total, concentrated in Barcelona-HCPB (52), Vancouver-BCCHR (41), NYSPI-Pediatric (33), Dresden (32) and Yale-Gruner (29).
- **Medication codes 1 and 2 within OCD.** 11 sites have both codes, with **n = 301** in those sites. The card's overall counts are 203 and 212.
- **Shortest durations.** These were derived from the prior survey's per-site `T_npy` (`verification/explorer_survey_1/probe_data_survey.out.json`) with the card's head trim of ceil(40/TR) samples, assuming no trailing padding.
  - Shortest: about **200 s, roughly 100 grid samples**, at Bellvitge-ANTIGA and Bellvitge-PROV (T_npy 120 at TR 2.0).
  - Next: Brazil at 220 s and Bergen at 246.6 s.
  - TR 0.7 (Yale-HCP-Trio): 309 s.
- **SE of d.** Design-only probe `verification/explorer_survey_1/2026-10-31/probe_se_d_design.log`:
  - SE(d) in σ_ε units under the site-FE + age + sex design is 0.0502, against the simple sqrt(1/n1 + 1/n2) = 0.0484 (ratio 1.037).
  - |d| needed for p < 0.025 is 0.113, so the card's |d| ≥ 0.15 bar remains binding.
  - Analytic: a true d of 0.15 gives P(|d̂| ≥ 0.15) = 0.50, and a true d of 0.20 gives 0.84.

### 1d. Secondary topics
- **T3.** `src/spectral_rg_flow_diagnostic.py:55-64` computes PR from `np.linalg.svd(X)` with no centering. `compute_spectral_quintet`, lines 153–160, passes raw X to it.
  - Lines 229–239 contain a silent synthetic fallback: if a file is missing, the code uses `rng.randn` data.
  - Probe `verification/explorer_survey_1/2026-10-31/probe_t3_pr_centering.log`:

    | Input | n × dim | PR uncentered | PR centered | Mean-energy fraction |
    |---|---|---|---|---|
    | L0 | 57 × 384 | 1.0014 | 2.777 | 0.9992 |
    | L1 | 57 × 768 | 1.0050 | 2.778 | 0.9973 |
    | L2 | 57 × 1536 | 1.0743 | 11.020 | 0.9645 |
    | L3 | 57 × 1536 | 1.0327 | 3.579 | 0.9832 |
    | BrainLM | 57 × 768 | 1.0028 | 4.319 | — |
    | BrainJEPA | 57 × 768 | 1.0581 | 11.785 | — |
    | NeuroSTORM | 25 × 288 | 1.0102 | 12.507 | — |

  - L2 and L3 are not identical: max |diff| is 3.17.
  - The npz files contain an `ids` key. M2 must never print it.
- **T4.** In `src/fractal_motif_resu.py:463-481`, channel 0 of `vmd_cache_4ch_464_head.mmap` (1706×5×464×304) is z-scored per ROI, including the padding rows.
  - The forecast test window is rows `split+1:` with `split = int(0.7·463) = 324` (lines 419–425). `ss_tot` is floored at 1e-8.
  - Probe `verification/explorer_survey_1/2026-10-31/probe_t4_padding.log`, positions 0–4: 177 nonzero rows, test window **100% padding**, training window 45% padding.
- **T2.** In `SwiFT_v2/project/module/models/swin4d_transformer_ver7.py`:
  - `PatchMergingV2` (lines 319–356) merges 2×2×2 spatially, not in time. It maps `Linear(8·dim → c_multiplier·dim)`.
  - Stages 0 to L−2 have `downsample` (lines 724 and 743). The last stage has `downsample=None` (lines 761 and 789).
  - The same class also appears in `simmim_swin4d_transformer_ver9.py` and `swin_transformer.py`.

## 2. Logic Chain

1. **Why T1.1 is tests only.** Editing `src/topic1_lagmotif` breaks card §12 (1a), and PROJECT.md does not assign that path to M1. So T1.1 must be tests only, and any new logic goes in `scripts/topic1_*`, importing the frozen modules unchanged. That logic includes the manifest check, a near-degenerate flag, counting accepted moves without no-ops, and the cohort runner.
2. **Which assertion kills each survivor.** Each must be made through `extract_subject`:
   - `roi_subsample_80`: assert `results["broadband@0.10"]["m"] == 4606` for a 304-ROI input. 80 ROIs give k = round(0.1·3160) = 316. Also assert that Z equals `flow_features(subject_flow(s), s.position)`.
   - `extract_subject_drops_valid_T`: assert `out["valid_T"] == out["raw_valid_T"] - out["n_trim"] == s.valid_T`. Use a TR where n_trim > 0, so every on-disk TR works.
   - `curl_returns_F`: assert that `results["curl@d"]` equals `motif_statistics(oriented_topk_graph(curl_component(F), d), …, null_seeds(…, "curl", d, …))`. Also assert that its observed census differs from broadband, on a signal with a substantial gradient share.
   - `seeds_ignore_position`: use a position other than 0, because the mutant hard-codes 0. Assert equality with an independent oracle, `SeedSequence([20261030, p, 1 if curl else 0, round(d·1000)]).generate_state(n, uint32)`, and assert that two positions give different null moments.
   - `sp_not_normalised`: assert that Σ SP² over the finite entries equals 1 (rtol 1e-12), and that SP = Z/‖Z‖.
3. **How to rerun the harnesses.** Running `mutants.py` or `mutants_extra.py` in place overwrites the auditor's receipts (1a), and runtime.md forbids overwriting prior receipts. The M1 worker must copy both into `verification/<own-id>/` and change `BASE` and the two output paths. The control count will rise above 54.
4. **Use local CPU, not connectome.**
   - The frozen code was validated on numpy 2.3 / scipy 1.15 / numba 0.62, and A3 was reproduced bit-identically there.
   - A project-local venv on connectome's Python 3.8 caps out at numba ≤ 0.58 and numpy ≤ 1.24. Outputs would need fresh reproduction checks against A3.
   - The local job is small (point 5), and C5 permits local CPU at ≤ 16 nice processes.
   - So: local is primary. connectome node4 (idle, 96 CPUs) is a fallback only if local load stays above about 14, and it needs a venv and an A3 re-check.
   - The lab data copies match only at name+size level (1b). Before any remote run, compare content hashes, computed and compared on the server side with digests only.
5. **Compute budget (추정).** From A3: 2.4 s per subject at 5%, 4.8 s at 10% and 5.9 s at 15%, single thread, 1,000 nulls.
   - **Primary.** broadband@0.10 alone is about 2.3 CPU-h.
   - **Fallback.** broadband@0.15 is needed in every case, because the fallback cannot be ruled out in advance: about 2.8 CPU-h.
   - **All 6 carded units.** About 12.5–13.1 CPU-h.
   - **§7 extraction-level sensitivities.** About 9 CPU-h for broadband@0.10: DCT 128 s high-pass and 200 s truncation (2.3 each), plus attempts factor 40 (about 4.6).
   - **Total.** About 20–22 CPU-h, i.e. 1.5–2 h wall on 12–14 processes with `nice -n 10`. Cap at 12–14 because of the current load and the parallel M2.
   - **Static-FC comparator (§6).** Recompute it in a second pass, at about 0.01 s per subject for load and preprocessing, so there is no 630 MB store.
   - **Statistics.** FL with B = 9,999 takes seconds when vectorized: t* = (dx̃·P e_r)/‖dx̃‖², and ‖M_r v‖² = ‖v‖² − ‖Qᵀv‖² with the QR of the reduced design.
6. **Statistics: what to implement and what not to reuse.**
   - Card §4–§5 specify Freedman–Lane: reduced-model residuals permuted within site, then t of dx in the site-FE OLS. The fit is MixedLM ML with Mundlak means, and d = β̂/σ̂_ε with the level-1 residual SD.
   - `verification/explorer_r1_3/probe_d_p_calibration.py` differs on all three: it permutes dx within site, uses REML, and defines d with the pooled raw SD. It must not be copied as the implementation.
   - The Mundlak equality holds algebraically, even for unbalanced sites. The within-transformed regressor is orthogonal to every site-constant column, whatever θ_i. So the |β_LMM − β_FE| < 0.01·SE check should pass to optimizer precision, and a failure signals a bug.
7. **The fallback decision is label-free.**
   - The rule (§3) is: more than 10% of subjects degenerate for E1 or E2 at 10% switches the primary to 15%. E1 is degenerate when 030C sd = 0; E2 when either 030C or 030T sd = 0.
   - The rule needs only extraction outputs, so decide it and record it (dated addendum + hash) **before** any label join.
   - Rates by group and site (addendum F.35) need dx and come after the stats-script sha is recorded.
8. **Minimum-length floor (addendum F.36).**
   - Any floor above 200 s (100 grid samples) on the current data excludes whole sites (Bellvitge-ANTIGA/PROV), which would be informative exclusion.
   - So a floor of 200 s keeps everyone and guards against defective series. It also matches the card's §7 "200 s truncation".
   - Choosing it is a post-freeze addendum item.

## 3. Caveats
- **Durations.** They are derived from the prior survey's per-site `T_npy` and assume no trailing zero padding. The exact valid_T comes from T1.3's label-free pass.
- **Remote data.** Content identity of the lab copies is not verified, and dgx1/B300 were not probed. Slurm PENDING reasons were not inspected.
- **T4.** That R² = 1.0 follows from a constant test window is an inferred mechanism. The padded rows become a constant after per-ROI z-scoring, ss_tot ≈ 0 is floored to 1e-8, and the prediction is near-constant too. It is not reproduced: M4 should log ss_res/ss_tot for one subject. Only positions 0–4 were checked, and the original run used 10.
- **T2.** That `layer_2` = stage-2 output after its merge (1536) and `layer_3` = the last stage without a merge (1536) is an inference from shapes plus code. The VRABES extraction hook and the model file that produced E192 (ver7 or ver9) are not verified.
- **T3.** Centered PR at n = 57 is capped at 56, and at 24 for NeuroSTORM (n = 25). Cross-model PR needs matched n, or subsampling.
- **Card ambiguities the stats worker must resolve in the pre-label addendum.** The card does not specify these:
  - (a) what happens if 15% is also more than 10% degenerate;
  - (b) whether the §6 secondaries stay at broadband@0.10 after a fallback (the card's literal text says 0.10);
  - (c) whether E1 and E2 share one permutation stream (their N differ after exclusions); recommendation: a fresh `default_rng(20261031)` per analysis, documented;
  - (d) how rank-deficient designs are handled (log duration is constant within most sites, and the subsets for Y-BOCS and medication may be rank-deficient); use a deterministic QR rank rule and log it;
  - (e) the standardized-β definition for Y-BOCS;
  - (f) the BH family 1 has no p-value defined (AUROC CI only);
  - (g) how the 200 s truncation is done: recommended is truncation of the native series to ceil(200/TR) samples after the head trim, then the frozen chain;
  - (h) complete-case handling for LOGO, using the same subjects for the comparator.
- **Prior exposure, disclosed.** In this survey I read metadata labels for design counts only, never joined to features. I read npy headers indirectly only through the prior survey file. I read 5 subjects' VMD-cache rows for padding fractions only (T4). No ID was printed or written.

## 4. Conclusion (recommended M1 plan)

The plan has a parallel phase and a serial phase.

**Phase 1: parallel, label-free.**
- **T1.1, tests only, in `tests/topic1_lagmotif/test_extract_contract.py`.** Make the 5 assertions in 2.2. Rerun copies of both harnesses from your own dir. Expected result: 0 survivors (19/19 + 4/4 killed, plus the earlier 23/23).
- **T1.3, `scripts/topic1_manifest.py`.**
  - Record count = 1706 and a salted list digest of the sorted names. Store the salt with the manifest, and never write per-subject unsalted hashes.
  - Record per position: site, TR, raw_valid_T, n_trim, valid_T, grid length and duration_s.
  - Check the floor of 200 s (= 100 grid samples), recorded in the dated addendum.
  - The runner asserts the count and digest before extraction.
- **T1.4a, `scripts/topic1_cohort_extract.py`.** Detached via `setsid nohup nice -n 10`, with a pool of 12–14 processes and 1 thread each.
  - It writes resumable per-subject JSON lines, a progress log, the params hash and the code hashes.
  - It extracts all 6 carded units. A second job covers the 3 §7 variants, each with its own params hash.
  - Output goes to `results/topic1/2026-10-31/`. Positions only.

**Phase 1': in parallel with Phase 1.**
- **T1.2, `scripts/topic1_cohort_stats.py` plus tests**, implementing exactly:
  - (i) site-FE OLS t for dx, with Y ~ dx + age + C(sex) + log dur + C(site);
  - (ii) the FL within-site residual permutation, B = 9,999, seed 20261031, p = (1 + #{|t*| ≥ |t|})/(B + 1);
  - (iii) MixedLM ML with a site random intercept and Mundlak site means of dx, age, sex and log dur;
  - (iv) d = β̂_LMM/√scale, and a stop if |β_LMM − β_FE| ≥ 0.01·SE;
  - (v) Holm over E1 and E2;
  - (vi) survive iff p_Holm < 0.05 and |d| ≥ 0.15, and killed iff neither survives;
  - (vii) the degeneracy fallback;
  - (viii) the §6 secondaries: LOGO-23 L2-LR (C = 1) on [Z030C, Z030T, gradient share], with in-fold scaling, pooled OOF AUROC, a site bootstrap of 2,000 resamples with seed 20261032, the per-site mean, and a static-FC PCA50 comparator on the same folds; Y-BOCS within OCD (n = 856) with an FL p; and medication codes 1 vs 2 in the 11 both-code sites (n = 301) with site FE; BH within each family;
  - (ix) raw d and Welch, labelled descriptive.

**Synthetic validation.** Use the real site×dx, age and sex design held in memory, with synthetic outcomes.
- **H0 scenarios:**
  - site effects aligned with site OCD fraction, ICC 0.1 and 0.3;
  - site-heteroscedastic noise;
  - t(4) or overdispersed noise;
  - exclusion correlated with site and group.
- **H0 acceptance.** With R ≥ 2,000 at B = 9,999, require |FPR − 0.05| ≤ 2·sqrt(0.05·0.95/R), which is ±0.0097 at R = 2,000.
- **Planted effects** of d = 0.15 and 0.30 in **σ_ε units**:
  - mean d̂ within 2 MC SE;
  - report P(|d̂| ≥ 0.15) and the joint survival rate (analytic expectation 0.50 at 0.15);
  - run the Mundlak stop check on ≥ 200 reps.
- **Defect fixtures that must fail:**
  - permuting across sites;
  - raw pooled d or Welch;
  - Holm omitted;
  - σ from the total SD;
  - sign flip (HC − OCD);
  - fallback threshold off by one, using the 9% vs 11% fixture;
  - kill-rule boundary.
- Each fixture must be shown to fail on its defect.

**Record the stats-script sha256** in `results/topic1/2026-10-31/` and in the dated addendum, after independent review.

**Phase 2: serial.** This phase starts only after the review.
1. Label-free QC: overall degeneracy and acceptance rates, and the fallback decision. Record it with a hash.
2. Join the labels.
3. Run the stats.
4. Report rates by group and site (F.34–F.35) and near-degenerate counts.
5. Give the verdict per endpoint (killed or survives), with the spurious-direction limitation (card §9) and the degeneracy rates beside it.
6. Write the result report to `docs/03_empirical_analysis/topic1/2026-10-31_*`.

**Secondary topics: M2–M4.**
- **M2.** Use centered PR. Remove or raise on the synthetic fallback. Put the centering defect in a fixture (a rank-1 + mean matrix gives uncentered PR ≈ 1). Use matched n. Never print `ids`.
- **M4.** First log ss_tot/ss_res, and restrict to valid rows (exclude the padding) before the R² diagnosis. A trivial persistence baseline is the needed comparator.
- **M3.** Verify which module output the `layer_i` files came from before redesigning. In code, the merge follows stages 0..L−2 and the last stage has none. ENIGMA cannot go to B300 (C6).

## 5. Verification Method
- Frozen code is unchanged:
  ```
  cd /home/juke/git/00IITP-AI && sha256sum src/topic1_lagmotif/*.py scripts/topic1_timing.py
  ```
  Compare against card §12. Expected: 10/10 match.
- Protected files:
  ```
  LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
  ```
  Expected: rc 0.
- Connectome environment:
  ```
  ssh connectome 'python3 -c "import numba"'
  ```
  Expected: `ModuleNotFoundError`. Same for statsmodels.
- Probes:
  ```
  PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/explorer_survey_1/2026-10-31/<probe>.py
  ```
  for `probe_t3_pr_centering`, `probe_t4_padding` and `probe_se_d_design`. Compare with the `.log` files next to them.
- Harness overwrite: `grep -n "victory_auditor_1" verification/victory_auditor_1/mutants.py` shows the hardcoded BASE and output paths.
- Invalidation: this survey's M1 plan is void if card §12 files change, if the npy directory count or listing digest changes, or if connectome gains numba and statsmodels in a comparable version.
