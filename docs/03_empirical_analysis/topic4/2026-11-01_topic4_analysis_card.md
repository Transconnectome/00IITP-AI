# Topic 4 analysis card (2026-11-01): topology of a backprop-free local learner for 2-s-ahead BOLD forecasting

Status: FROZEN once, before any Topic 4 real-data outcome on the primary population was computed. The sha256 of this file is in `results/topic4/2026-11-01/card_sha256.txt`. The run script refuses to start if this file, the code hashes in `results/topic4/2026-11-01/code_sha256_at_freeze.txt`, or the split manifest differ from what was recorded at freeze. Deviations go in dated addenda (`2026-11-01_topic4_addendum_NN.md`); this file is never edited.
Author: worker_M4_r1 (Teamwork run tw-20261031-four-topics, milestone M4). Mode: CONFIRMATORY on the confirm set; the tuning stage is EXPLORATORY and governed by the rules in section 5.

## 0. Access history (what was seen before freezing)
- Legacy Topic 4 numbers (R² = 1.0 for every condition, PR ≈ 1, "R_hub = 0.0", "PR per 100 synapses") are artefacts (T4.1 diagnosis, `2026-11-01_topic4_T41_diagnosis.md`) and are not cited as results (C8).
- Real ENIGMA subjects touched for Topic 4 before freeze: positions 0–11 (legacy run and survey, TR 1.8) and 932 (explorer probes, TR 1.0). None of them is in the primary population (TR = 2.0). The T4.1 counterfactual (`results/topic4/2026-11-01/t41_counterfactual.json`) reran the protected legacy function on positions 0 and 932 only.
- The split manifest was built from metadata (site → TR) and series lengths after the data contract only. No forecasting quantity was computed on any TR = 2.0 subject before freeze.
- Topic 1 (M1) used every subject for lag-motif features and diagnosis statistics. That is a different endpoint; it does not touch forecasting outcomes and diagnosis labels are not used here.
- The engine and baselines were qualified on synthetic data only (`results/topic4/2026-11-01/qualification.json`, all Q1–Q6 passed; section 7).

## 1. Question, estimand, unit, baseline (G1)
Primary question: under a strictly local, backprop-free similarity-matching learning rule with a 24-unit lateral connectivity mask at matched edge count (69 of 276 pairs), does the "Mode II" hub-repelling fractal topology (C4) give a better 2-s-ahead BOLD forecasting code than an Erdős–Rényi random topology (C1)?
- Estimand Δ1 = mean over confirm subjects s of [S_C4(s) − S_C1(s)]. S_c(s) is subject s's per-subject R² (section 6) for class c, averaged over that class's successfully trained instances.
- Independent unit: subject (test subjects of the cross-fitting). Graph instances are a second random factor (crossed bootstrap).
- Baseline for H1: C1 at the same edge count. Persistence, identity ridge, PCA-24, RRR-24 and random features are references only. They are never kill comparators because a 24-d linear code below full-input ridge is fixed by construction.

## 2. Data and data contract (G2)
- Source: ENIGMA-OCD raw ROI series, `/home/juke/git/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25/<ID>/<ID>.npy` (T × 304, float64), read-only, positional access only, DGX-Spark CPU only (C6). Never the VMD cache (IMF1 saturates persistence at R² ≈ 0.99; padding).
- Loader: `src/topic4_resu/data.py`, vendored from `src/topic1_lagmotif/data.py` (sha d320bfe4…95e9) and `tr_table.py` (sha a3837b15…6b8d), with behavioural-equality tests.
- Primary population: sites with TR = 2.0 s exactly (no resampling; one sample = 2.0 s). Split-manifest facts: 1195 subjects, 13 sites, valid_T 100–286 (median 133), 191,209 samples, 0 contract errors, 0 burned positions.
- Contract (halts, never repairs):
  - trailing all-zero rows are stripped;
  - an internal all-zero row, non-finite values or an all-zero series raise;
  - head trim 40 s (20 samples);
  - valid_T ≥ 100;
  - an R² guard firing on a real subject (section 6) is a contract violation and halts the run.
- Preprocessing per subject (identical for every arm): per-ROI linear detrend, then z-score (ddof 0) over the subject's own valid series, then the fixed ROI subset `np.linspace(0, 303, 48, dtype=int)`. Declared limitation: the within-subject detrend and z-score and the upstream ≈0.25 Hz low-pass are acausal and shared by every arm, so absolute skill is optimistic and only contrasts are interpreted.
- Split manifest: `results/topic4/2026-11-01/split_manifest.json`, sha256 `3e56210febd5b05de6ca2c5d750af58de96fef7a79b3fba08393d078680a0436`.

## 3. Split and sealing (G3, G4)
- Salted-hash rank within site (`src/topic4_resu/split.py`). Burned positions {0–11, 932} are excluded first; none is TR = 2.0.
- Tuning set: round(0.15 · n_site) per site, 181 subjects. Within it, tune-train 145 and tune-val 36 (inner salt).
- Confirm set: 1014 subjects, folds 0–4 round-robin in rank order within site (207/206/204/201/196). Each confirm subject is tested exactly once.
- Inside each training fold, inner-val is the lowest 10% by inner-salt rank (λ choice and MLP early stopping); the rest is inner-train.
- Everything fitted uses training subjects only. That covers the PCA basis, RRR, local-engine weights, MLP weights, ridge readouts and λ, and the guard's train-variance scale. The final readout is refit on inner-train + inner-val. Fixture F-fold (`tests/topic4_resu/test_train_only.py`) proves that perturbing test subjects leaves every fitted state bit-identical; overlap audits run in the tests and in the manifest builder.
- The confirm set is opened once, by the confirm stage (section 5).

## 4. Task and arms
- Task: predict x_{t+h} (48 z-scored ROIs) from x_t, over all valid (t, t+h) pairs within a subject. Primary horizon h = 1 sample = 2 s; secondary h = 2 samples = 4 s (descriptive). For the secondary horizon, encoders trained at 2 s are reused and only the readout is refit; RRR is refit per horizon.
- Common readout for every encoder: ridge with intercept on centred codes. Penalty λ·n·I, λ ∈ {1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1}, chosen by inner-val MSE, then refit on inner-train + inner-val.
- References:
  - constant (training mean);
  - persistence (x̂_{t+h} = x_t);
  - identity ridge (VAR(1), 48 → 48);
  - PCA-24 + ridge;
  - RRR-24 (supervised linear 24-d optimum);
  - random-linear-24 and random-ReLU-24, seeds 0–4, untrained.
- Local engine (the only engine): masked-lateral principal-subspace-projection similarity matching (Pehlevan, Sengupta & Chklovskii 2018, Neural Comput. 30:84–124). It is not a ReSU (arXiv:2512.23146 defines ReSU as batch past–future CCA with ON/OFF rectification and no lateral connections or local rule) and is named accordingly.
  - Steady state y* = M⁻¹Wx of the neuron-local dynamics τ_i dy_i/dt = Σ_j W_ij x_j − Σ_j M_ij y_j.
  - Plasticity per minibatch of 64 samples: ΔW_ij = η(⟨y_i x_j⟩ − W_ij), ΔM_ij = (η/τ)(⟨y_i y_j⟩ − M_ij)·A_ij with A = mask + I.
  - k = 24, τ = 0.5, η_t = η0/(1 + t/2000), 6000 updates, W0 ~ N(0, 1/48), M0 = I. Init seed = instance index; sample order from seed + 7919.
  - Learning uses inputs only (`fit(X)` takes no targets). There is no global step: no eigendecomposition, rescale, projection or normalisation over units.
  - Stability is monitored after every update, never enforced: ρ(I − D⁻¹M) < 1 with D = diag(Σ_j |M_ij|), equivalently λ_min(M) > 0. A violation or a non-finite value ends the run as FAILED; it is counted and never dropped.
- Topology classes (vendored generator, equal to the protected `build_strictly_matched_topologies`), cFFL / delay-bank input off for every class:
  - C0: no lateral edges;
  - C1: Erdős–Rényi (69 edges);
  - C2: Watts–Strogatz ring with 15% rewiring (69);
  - C3: rich club (69);
  - C4: Mode II, 4 boxes, 0 edges among the designated hubs {0, 6, 12, 18} (69). Under the top-degree hub definition its R_hub is not 0; the claim used is "0 designated-hub edges";
  - C4DP: degree-preserving double-edge-swap rewiring of C4 (69, the same degree sequence);
  - C5: dense (276).
  - Instances: C1, C2, C4 and C4DP use graph seeds 0–29, so 30 graphs each; C4DP instance g rewires C4 instance g. C0, C3 and C5 are single graphs, each with init seeds 0–9.
- Backprop baseline (matched width): MLP 48 → 24 (ReLU) → 48, trained on the 2-s forecasting MSE.
  - Adam, batch 256, ≤ 100 epochs, early stopping on inner-val subjects (patience 8, best epoch restored).
  - Grid lr ∈ {1e-3, 3e-3} × weight decay ∈ {0, 1e-4}, all four trained per seed; the lowest inner-val MSE is kept.
  - Seeds 0–2 per fold.
  - Primary form: encoder-then-common-ridge (MLPenc: the hidden layer frozen, the common readout refit). End-to-end is secondary.
  - Adequacy was verified on synthetic data (Q5; fixture F11).

## 5. Stages, gates and halts
- G-a (before freeze): the fixtures are green and qualification Q1–Q6 passed. Evidence: `results/topic4/2026-11-01/logs/tests_topic4_prefreeze.log` (67 passed) and `qualification.json`. Mutation evidence: `verification/worker_M4_r1/mutants/mutation_results.json` (17/17 killed, the control passes) and `nobackprop_matrix.json`.
- Tuning stage (tuning set only, `scripts/topic4_run.py --stage tuning`):
  - η0 is the largest value in the ladder (0.02, 0.01, 0.005) for which all 7 classes × instances 0–2 are stable on tune-train. The choice uses stability only, never forecast skill, because skill rewards unconverged sparse engines.
  - G-b non-saturation: tune-val mean per-subject R² at 2 s < 0.9 for both identity ridge and persistence.
  - G-c: the R² guard never fires.
  - G-d: some η0 in the ladder is stable.
- If any of G-b, G-c or G-d fails, the confirm stage is refused and the card verdict is no_candidate / halted (a software or data result, not a scientific null).
- Confirm stage: 5-fold cross-fitting with every arm above at the selected η0. All tasks, including failures, are logged in `run_ledger.jsonl`.

## 6. Metric, uncertainty, hypotheses and decision rules (G5, G8)
- Metric: per-subject R² over that subject's test pairs and the 48 ROIs, R² = 1 − Σ(z − ẑ)²/Σ(z − z̄_s)², where z̄_s is the subject's own test mean. There is no floor and no clip. It raises if Σ(z − z̄_s)² < 1e-3 · n · Σ_j var_train,j. Any constant predictor scores ≤ 0.
- Class score per subject: the mean over the class's successful instances.
- Smallest effect of interest: δ = 0.01 R². This value is analyst-set and PI confirmation is pending. All CIs are reported so the PI can apply another δ; a different δ is recorded as an addendum.
- Primary CI: crossed bootstrap, B = 2000, seed 20261101. Each draw resamples confirm subjects with replacement within site strata and, independently per class, instances with replacement; the interval is the percentile interval.
- H1 (primary, 95% two-sided): Δ1 = S_C4 − S_C1.
  - keep: CI_lo > 0 and Δ1 ≥ δ and S1.CI_lo > 0;
  - modify: the keep conditions hold except S1.CI_lo ≤ 0, so the effect is attributable to the degree sequence rather than the Mode II arrangement;
  - stop (killed): CI_hi < δ;
  - inconclusive: otherwise.
- Secondary family (Bonferroni, each CI at 1 − 0.05/3 = 98.33%):
  - S1, arrangement beyond degrees: S_C4 − S_C4DP. Supported if CI_lo > 0 and point ≥ δ; killed if CI_hi < δ; else inconclusive.
  - S2, learning value: S_C5 − S_randlin24 (seeds as instances). The same three rules.
  - S3, local versus backprop: S_C5 − S_MLPenc (seeds as instances). Non-inferior if CI_lo > −δ; inferior if CI_hi < −δ; else inconclusive.
- Execution integrity: if more than 10% of a class's confirm runs are unstable or failed, every contrast that uses the class is "inconclusive (execution integrity)". Failed runs are excluded from class means and reported with counts.
- Sensitivity (reported, not decisive):
  - H1 with a subject-only bootstrap (instances fixed);
  - a site-cluster bootstrap of the per-subject difference;
  - H1 at 4 s;
  - H1 on skill against persistence (1 − MSE/MSE_persistence).
- Descriptive: the mean per-subject R² of every arm with a subject-bootstrap 95% CI, plus centred PR of the test codes, rank of the learned map, max ρ, and convergence (relative W change over the last 10% of updates).
- Exploratory (no verdict): Spearman correlation between instance-mean R² and the graph's independence number across sparse instances.
- Statistics code: `scripts/topic4_analyze.py` with `src/topic4_resu/stats.py`, hashed at freeze.

## 7. Expected outcomes, written before any real-data result
These come from synthetic qualification and are not forecasts of the real effect.
- On both structured VARs:
  - C4 ≈ C1 ≈ C4DP within about 0.002 R²;
  - C0 (collapse to rank 1) is lowest;
  - C5 ≈ PCA-24 < RRR-24 ≤ identity ridge;
  - C5 − random-linear-24 ≈ +0.06 to +0.09;
  - MLPenc ≈ RRR-24.
- Expected verdicts: H1 stop or inconclusive; S1 killed or inconclusive; S2 supported; S3 inferior or inconclusive. A null H1 is a valid result. The topology effect in the synthetic runs follows the rank of the learned map, which is set by how many mutually unconnected units collapse onto the same direction, not by hub repulsion.

## 8. Seeds, budget, environment (G7)
- Seeds: listed in sections 3–6, with no seed selection.
- Runs per fold: 150 local-engine runs (4 classes × 30 graph instances + 3 classes × 10 init seeds), 3 MLP seeds × 4 grid configurations, and the reference arms. 5 folds in total.
- Estimated wall time: under 1 h on ≤ 4 local processes (nice, OMP_NUM_THREADS = 2). 0 GPU-h; B300 is excluded (C6).
- Environment: /home/juke/superclaude-env (python 3.12, numpy 2.3.5, torch 2.11 CPU) is recorded in the ledger.
- The preprocessed cache lives outside the repository (scratchpad) and is deleted after the run.

## 9. Declared limitations
- The within-subject acausal preprocessing is shared by every arm (section 2).
- Only TR = 2.0 sites are used, so generalisation to other TRs is untested.
- Family structure is unknown, so subjects are assumed independent.
- The cross-fitted CIs do not include training-set variability across overlapping folds, which makes them somewhat anti-conservative.
- There is one learning rule (linear PSP), so a rectified or NSM rule could behave differently.
- The synthetic qualification uses isotropic noise.
- "Topology effect" means the effect of the mask under this rule and this budget (6000 updates).

## 10. Deviations from the dispatch text (recorded before results)
- 5-fold subject cross-fitting replaces the "pooled leave-one-subject-out" example. Per-fold retraining of ≈1200 × 150 engines is infeasible, and cross-fitting tests every subject exactly once.
- δ is fixed at 0.01, pending PI confirmation, so the card can be frozen strictly.
- A single engine (PSP) is used; NSM is omitted.
- MLP uses 3 seeds.

## 11. Frozen artefacts (sha256 at freeze)
- Code: `results/topic4/2026-11-01/code_sha256_at_freeze.txt`. It lists every file in src/topic4_resu, scripts/topic4_*.py and tests/topic4_resu.
- Qualification: `results/topic4/2026-11-01/qualification.json`, listed in the same file.
- Split manifest: section 2.
