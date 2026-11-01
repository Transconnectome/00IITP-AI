# Handoff — explorer_M4_r1_1 (M4 / Topic 4 FM-ReSU redesign; lens: scientific design)
Written 2026-11-01T01:15Z. Type: **Hard** (explorer analysis complete). Read-only; no production code, tests, docs or results written.
Probes live only in `/home/juke/git/00IITP-AI/verification/explorer_M4_r1_1/` (hashes in its `SHA256SUMS.txt`).
Real data touched: **2 ENIGMA subjects, read-only**: position 0 (already burned by survey) and position 932 (newly burned, site#09, TR 1.0). Both are **outside** the recommended primary population (TR = 2.0 s sites). Every real-subject number below is a dev feasibility probe and governs no result (C3/C8). GPU: **0 GPU-h, no B300 contact** (no ledger entry needed).

**Summary.** T4.1 is closed by counterfactual. Every subject the old run could have used (positions 0–11) has its whole test split in zero padding. One full-length subject (pos 932, 464/464 valid rows) gives R² −0.08…+0.05 for all six conditions under the unmodified protected function, never 1.0. Under it sit five further defects: leakage, saturated IMF1 input, a collapsing non-local engine that is not ReSU, an uncentered PR, and a cFFL confound with one graph instance per class.

For T4.2/T4.3 I recommend the following, all on CPU:
- **Primary population:** TR = 2.0 s sites only (1195 subjects, 13 sites; no resampling, so h = 1 step is exactly 2 s).
- **Design:** a two-stage dev/sealed-confirm design.
- **Engine:** a canonical masked-lateral PSP similarity-matching engine, named as such and not as ReSU. It passes the planted-subspace fixture; the legacy engine fails it.
- **Topology:** 30 graph instances per random class, plus a degree-preserving C4 sham.
- **Backprop baseline:** a tuned, early-stopped MLP-24 evaluated encoder-then-common-ridge. It passes an adequacy gate on a VAR(1) fixture with known Bayes R².
- **Card:** frozen with expected outcomes written in.

The main risk for the PI: synthetic probes predict H1 (C4 > C1 at matched edges) to be **≈ null**. Representation dimension tracks the graph's independence number (r = −0.96), not hub repulsion.

---

## 1. Observation

### 1a. T4.1 evidence (probe A + manifest aggregates; positions only)
| # | Observation | Evidence |
|---|---|---|
| A1 | Manifest rows 0–11: all site#00, TR 1.8, raw_valid_T 197 → VMD-cache valid rows 177; split index 324 ⇒ 0 valid test rows for every subject the old 10-subject run (and the report's "n=12") could have used | `results/topic1/2026-10-31/manifest.json` (aggregated); `probe_a_t41_counterfactual.out.json` pos0: `mask_valid_rows 177, split_index 324, valid_rows_in_test 0` |
| A2 | n mismatch: `empirical_results.json` topic4 `n_subjects_evaluated: 10`; `EMPIRICAL_ANALYSIS_REPORT.md:88` says n=12 | both files (protected, read only) |
| A3 | pos0 (padded): ss_tot = 2.5e-45 for every variant → `max(ss_tot,1e-8)` → R² = 1.0 for C0, C1, C4, C5, identity ridge AND persistence. The train-mean constant gets −1.0, because the clip at −1 is reached | probe A `pos0.variants` |
| A4 | **Counterfactual** pos 932 (site#09 TR 1.0; first position with TR<2.0 and raw_valid_T ≥ 484; mask 464/464 valid, 139 valid test rows). The **unmodified protected** `evaluate_topology_on_fmri_streams` gives R² C0 0.040, C1 0.053, C2 0.051, C3 −0.082, C4 0.024, C5 0.024; uncentered PR 1.0000–1.0007. My replica matches it to 4 dp | probe A `pos932.protected_function_R2`, `replica_vs_protected_R2` |
| A5 | Leak toggles on pos 932, all fit on train rows (z-score / target SVD / online plasticity). Identity ridge: 0.958 (legacy full-stream) → 0.898 (all train-only), so ΔR² = 0.06. Legacy-engine R² moves by up to 0.34 with the z-scope toggle (C5: 0.024 → −0.319) | probe A `pos932.variants` |
| A6 | IMF1 input saturates the trivial baseline even when fixed: persistence R² 0.991–0.992 in every variant on pos 932 | probe A |
| A7 | Legacy engine code: W update is semi-implicit single-unit Oja (`fractal_motif_resu.py:335-336`). M has its diagonal zeroed (`:347`) and is weighted asymmetrically by `M_hier` = lower-tri + 0.25·upper-tri (`:302, :323`). Stability is a **global** eigenvalue rescale `if rho>=0.98: M*=0.95/rho` (`:349-352`), which is a non-local step. cFFL is given only to C4 (`:377`). One graph per class, seed=42 (`:468`) | source (protected) |
| A8 | ReSU primary source (arXiv:2512.23146, Qin, …, Sengupta, Chklovskii): each unit is a rectified (ON/OFF) projection of a past-input window onto a **past–future CCA** direction, computed in **batch** by SVD. The paper has **no lateral connections and no local learning rule**; it names local CCA (citing Lipshutz et al. 2021) as future work. I read only the first ~100k chars of the HTML (no supplement). The legacy engine therefore is not ReSU, nor canonical PSP/NSM | WebFetch arxiv.org/html/2512.23146v1; WebSearch |

### 1b. Cohort facts (manifest aggregates; no IDs)
- n = 1706, 23 sites; TR counts 0.7 (43), 0.8 (96), 0.85 (104), 1.0 (119), 1.73 (39), 1.8 (110), **2.0 (1195, 13 sites)**.
- grid_len on the 2-s grid: min 100 / median 160 / max 340. Within TR = 2.0: min 100 / median 133 / max 286, 191,209 samples in total.
- `src/topic1_lagmotif/preprocess.py:33-34` does not resample when TR = 2.0. Other TRs use `scipy.signal.resample_poly`, an acausal FIR. Upstream the raw npy are already low-passed near 0.25 Hz (`preprocess.py` docstring).
- The positions burned so far (0–11; 932) are all **outside** the TR = 2.0 population.

### 1c. Engine and topology (probe B, synthetic planted subspace)
Setup: d = 48, k = 24 planted dims with λ_i = 4·0.9^i, plus noise 0.05. 1e5 training samples (the real-data scale), 5 graph seeds, minibatch-64 local updates, no global rescale.

The analytic PR of the planted spectrum is ≈ 16.2.

| engine | C0 | C1 ER | C2 WS | C3 rich-club | C4 Mode-II | C4DP (deg-preserving C4) | C5 dense |
|---|---|---|---|---|---|---|---|
| PSP centered PR(Y) | 1.27±0.07 | 3.59±0.20 | 4.19±0.20 | 1.93±0.15 | 3.78±0.19 | 3.80±0.22 | **16.51±0.04** |
| PSP decode R²(x\|y) | 0.614 | 0.729 | 0.745 | 0.688 | 0.739 | 0.748 | **0.969** |
| NSM centered PR | 2.04 | 3.94 | 4.79 | 2.75 | 4.26 | 4.32 | 17.41 |
| **legacy** centered PR | 1.65±0.57 | 3.69 | 4.21 | 1.88 | 4.49 | 3.96 | **2.61±0.63** |
| **legacy** decode R² | 0.277 | 0.395 | 0.404 | 0.342 | 0.412 | 0.414 | **0.423** |

- Paired by graph seed, PSP: C4−C1 ΔPR +0.19 (sd 0.31), Δdecode +0.0096 (sd 0.036); C4−C4DP ΔPR −0.01 (sd 0.40); C4−C3 +1.86 (sd 0.14).
- Across all 25 sparse instances, corr(PR, independence number α(G)) = **−0.959** and corr(PR, greedy colours) = −0.846.
- All PSP/NSM runs were stable (λ_min(M) > 0 at every update; minimum λ_min 0.13 for C5).
- Graph facts (`summarize_b.out.txt`):
  - Every C1–C4/C4DP instance has **69 edges**.
  - C4 has 0 edges among designated hubs {0,6,12,18} at all 5 seeds.
  - Under the code's top-degree metric (`rg_box_pooling.compute_hub_repulsion_ratio`, hub_frac 0.33), C4 gives R_hub 1.43–1.86 and C1 gives 1.29–2.14. So **C4's "R_hub = 0.0" holds only for designated hubs**.
  - C3 has α(G) = 17 (16 mutually unconnected satellites), which explains its collapse.
  - Assortativity: C4 −0.12…−0.27, C1 −0.01…−0.18.

### 1d. VAR(1) fixture (probe C, synthetic)
Setup: A = V diag(a) Vᵀ (8 slow modes 0.92→0.75, 40 modes 0.55→0), Σ_ε = I. 600 train / 100 val / 200 test "subjects", T = 160.
- Analytic Bayes R²: h=1 **0.3598**, h=2 0.2306. Analytic persistence: h=1 0.0327, h=2 −0.280.
- Empirical: oracle per-subject 0.3622 ± 0.002 (SE); pooled oracle 0.3635; identity ridge 0.3631; persistence 0.038; train-mean constant −0.0003; zero constant 0.0.
- Guards:
  - the legacy R² formula on an all-padding test returns **1.0**;
  - the guarded R² **raises**;
  - an acausal input (centred 3-tap smooth) scores **0.536 > Bayes**, so the leak detector fires.
- Encoders, each with the same ridge readout and λ chosen on val subjects (per-subject R²):

| encoder | per-subject R² |
|---|---|
| identity-48 | 0.362 |
| PCA-24 | 0.349 |
| PSP-C5 | 0.347 |
| PSP-C4 | 0.3057 ± 0.0013 |
| PSP-C1 | 0.3055 ± 0.0017 |
| PSP-C3 | 0.296 |
| PSP-C0 | 0.221 |
| NSM-C5 | 0.263 |
| NSM sparse | 0.177–0.195 |
| random-ReLU-24 | 0.18 |

  Skill vs persistence follows the same order.

### 1e. Backprop baseline adequacy and timing (probe E, VAR fixture, torch CPU, 2 threads)
- RRR-24 closed form gives 0.3498.
- MLP 48→24(ReLU)→48 with Adam and early stopping (patience 8) on val subjects, grid lr {1e-3, 3e-3} × wd {0, 1e-4} × seeds {0,1,2}:
  - end-to-end mean 0.3432 (min 0.3401);
  - **encoder-then-common-ridge** mean 0.3450;
  - 24–48 epochs, **~6 s per fit** on 95k pairs.
- An untuned configuration (full-batch 1500 steps) gives 0.333.
- With only **4 training subjects**: tuned MLP 0.227, untuned 0.224, identity ridge 0.304. The survey's real-data MLP −0.12 (4 training subjects, untuned) is therefore a small-data / tuning artefact, not evidence that "backprop loses".
- Timing for the canonical engines on 1e5 samples: PSP fit ≈ 0.1 s, NSM ≈ 0.8 s. The legacy engine runs per sample at ≈ 10 s per 20k samples.

### 1f. Layout and env
- Both old AST audits scan only `SRC_DIR.glob("*.py")` (`tests/test_pilot_connectome.py:161`, `tests/e2e/test_pilot_simulation_e2e.py:97`).
- No test recurses into `src/` (`rglob`/`os.walk` grep is empty). A torch module under `src/topic4_resu/` therefore does not break the 86-pass suite.
- Local env: numpy 2.3.5, scipy 1.15.3, sklearn 1.7.2, torch 2.11 (dev, CPU usable), networkx 3.4.2. Host load average 12–17 on 20 cores.
- C1 `sha256sum -c` gives rc 0 (start and end of my work).

## 2. Logic Chain
1. A1+A3: the whole test window is padding, so ss_tot is ≈1e-45, the floor 1e-8 applies, and R² = 1 − ~0/1e-8 = 1.0 for any predictor, including persistence. This explains "all conditions incl. C0 = 1.0, std 0".
2. A4 is the falsification test survey_3 proposed. A full-length subject gives R² ≈ 0 under the identical unmodified code, so padding plus the floor is the cause. The leak alone cannot produce 1.0.
3. A5: the leaks are real but second order (≈0.06 for ridge). For the legacy engine they dominate its own R² (shifts up to 0.34), which on clean data is ≈ train-mean level. Fixing padding alone would not give a valid task.
4. A6: IMF1 makes persistence ≈ 0.99, so the input must change to raw full-band BOLD. Survey O12–O13 found persistence 0.30 and identity ridge 0.36 at h=1 on raw npy, native TR 1.8, which is not saturated.
5. A7+A8+1c (legacy rows): the legacy engine collapses even when dense (PR 2.6 vs the planted 16.2). It is asymmetric and non-local, and it is not ReSU. Any topology comparison on it is uninterpretable. The canonical masked PSP recovers the planted spectrum when dense (16.5) and collapses with no lateral mask (1.27). So F5 discriminates the defect, and PSP is a valid engine for the topology question.
6. 1c: at matched density the measurement does respond to topology (C3 ≪ C1 ≈ C4 ≈ C4DP < C2 ≪ C5). The response is explained by α(G) (r = −0.96), and C4 equals its degree-preserving sham. The mechanistic prior for H1 (C4 > C1) is therefore ≈ 0. Graph-instance SD (PR 0.2–0.3) is the dominant variance, so a class-level contrast needs many instances, with instance as a resampling unit.
7. 1d: the evaluation stack can be validated against a known ceiling. It also shows where encoders must land by construction: PSP-C5 ≈ PCA-24 < identity ridge. Using identity ridge or PCA-24 as kill comparators would predetermine the verdict; they must be references only.
8. 1e: a matched-capacity backprop encoder reaches the linear ceiling with a modest grid and early stopping in seconds. An adequacy gate on the VAR fixture prevents the survey's under-tuned-baseline failure mode.
9. 1b: TR = 2.0 sites avoid resampling, so h = 1 step = 2 s exactly, with no `resample_poly` acausal mixing. They hold 70 % of the cohort and none of the burned positions. The 0.25 Hz upstream filtering and whole-series per-subject detrend/z-score are acausal for everyone (1d shows how acausality inflates R²). So only contrasts, not absolute skill, are interpretable.
10. Compute (1e): the whole confirmatory design costs < 1 CPU-hour locally. B300 is not needed, and C6 forbids it for ENIGMA anyway.

## 3. Caveats
- Synthetic probes (B, C, E) inform engine validity, measurement capacity and baseline adequacy only. They do **not** forecast the real-data effect (sci-pipeline G6), and their numbers must not seed δ.
- Probe B used isotropic-noise planted data and 5 graph seeds; probe C used 3. Real BOLD covariance is structured, and topology effects there could differ in sign or size.
- I ran no real-data dev LOSO with the new engine. Survey_3 already showed non-saturation on raw npy (native TR 1.8, positions 0–4), and running more would burn subjects. The worker's dev stage does this on the TR = 2.0 dev split.
- The ReSU paper was read to ~100k of 172k characters; I did not read the supplement. A local past–future CCA rule (Lipshutz et al. 2021) was not probed.
- The NSM engine uses damped Jacobi (60 iterations) without a convergence check, so NSM numbers are indicative.
- The independence-number correlation (r = −0.96) is over 25 instances of 5 classes. It is a pre-registrable hypothesis, not an established law.
- Positions used by peer explorer_M4_r1_2 are unknown to me (independence). Root must take the union of burned positions.
- The topic3 `__pycache__` files newer than my dispatch (09:39 KST) were not created by me; I never imported `src.topic3_spectral`.

## 4. Conclusion — recommended strategy for the M4 worker

### 4.0 Placement (exclusive M4 paths)
- `src/topic4_resu/`: `data.py` wraps `src/topic1_lagmotif` by import (positions only); `split.py`; `metrics.py`; `topologies.py`; `local/psp.py` and `local/nsm.py` (numpy only); `baselines/linear.py`; `baselines/backprop.py` (torch, outside `local/`); `run.py`.
- `tests/topic4_resu/`, `scripts/topic4_*`, `results/topic4/2026-11-01/`, `docs/03_empirical_analysis/topic4/2026-11-01_topic4_{analysis_card,addendum_NN,result_report}.md`.
- Do not edit `src/fractal_motif_resu.py`; it is protected. Import it read-only only for the T4.1 regression fixtures and the topology generator.

### 4.1 T4.1 — diagnosis report and fixtures (each must FAIL on the legacy path and PASS on the new one)
- **F1 padding:** a stream with ≥ 50 % trailing zero rows. The loader must strip it or raise. The evaluator must raise on an all-zero test window. The legacy formula returns 1.0 there (probe C).
- **F2 degenerate target:** R² raises if ss_tot < ε·n·var_train, with ε = 1e-6. No floor.
- **F3 constant predictor:** on a non-degenerate VAR test, the train-mean constant gives R² ≤ 0 + 3 SE. The R² reference mean must be declared and used consistently. I recommend 0, since series are per-subject z-scored; with the test-window mean, any constant gives ≤ 0 exactly.
- **F4 VAR(1) Bayes:**
  - the oracle is within 3 SE of the analytic Bayes R² (0.3598);
  - persistence is within 3 SE of its analytic value;
  - no production feature path exceeds Bayes + 3 SE;
  - an acausal-feature mutant MUST exceed it (detector sanity: 0.536).
- **F-fold:** perturbing test subjects' data leaves every train-fitted quantity bit-identical (z-stats if pooled, PCA, encoder W/M, ridge, MLP).
- **Report:** the diagnosis report lists A1–A8 with the counterfactual (A4) as the decisive evidence and the leak sizes (A5). The n mismatch (A2) is recorded as a documentation defect.

### 4.2 T4.2 — task, population, split, conditions, metric

**Data**
- Permitted: ENIGMA-OCD raw npy `MBBN_data_304_ROIs_0.25`, read-only, on DGX-Spark CPU (or connectome). Never on B300 (C6).
- Not usable:
  - the VMD cache (IMF1 saturation, padding);
  - UKB ROI series (the only copy seen is under `~/enigma_ocd/data` on B300, which is off-limits; no lab copy verified);
  - B300 HCP raw NIfTI (needs parcellation; another workstream).
- Synthetic VAR/planted data are fixtures only.

**Population**
- Primary: **TR = 2.0 sites** (1195 subjects, 13 sites).
- Exclude burned positions: 0–11 (old run and survey), 932 (this probe), and the peer's probe positions. None of 0–11 or 932 is in the TR = 2.0 population.
- Sensitivity only: all 1706 subjects resampled to the 2-s grid.

**Preprocessing**
- Topic 1 loader and rules: strip trailing zeros, raise on internal zero rows, 40-s head trim (20 samples).
- Per-ROI linear detrend and per-subject z-score (whole series). Declare this as a shared, within-subject acausal step.
- Optional sensitivity: causal z-scoring from a 40-s calibration window excluded from scoring.
- 48 ROIs by the fixed rule `linspace(0,303,48)`, with no fitting.

**Task**
- Predict x_{t+h} (48-d) from features of x_t.
- **h = 1 step = 2 s (primary).** Secondary h = 4 s and 6 s, declared possibly inconclusive.
- Secondary target: top-8 train-fold PCs, for continuity with the old design.

**Split**
- Salted-sha256(position) rank, site-stratified.
- **Dev 20 % (~240 subjects; EXPLORATORY)**, used to fix hyperparameters, check stability and non-saturation, and measure variance components that ground δ.
- **Confirm 80 % (~955; CONFIRMATORY, sealed).** Record the confirm-manifest sha256 before the dev stage starts and open it once.
- Within confirm: 5-fold subject-disjoint, site-stratified CV, with an inner 20 % validation split of each training fold for λ and early stopping. Each confirm subject is tested exactly once.
- Run `group_overlap_audit.py` and record its output.

**Conditions**
All conditions use the same input, width 24, the same ridge readout (λ from a fixed grid, chosen on inner-val), and cFFL **off for all**.
- References (never kill comparators): persistence; identity ridge (VAR(1)); ridge VAR(2); train-mean.
- Linear anchors: PCA-24 + ridge; RRR-24.
- Untrained: random-ReLU-24, 3 seeds.
- **Local family, primary engine = masked PSP** (Pehlevan, Sengupta & Chklovskii 2018):
  - y = M⁻¹Wx, with M = diagonal plus masked off-diagonals;
  - ΔW = η(⟨yxᵀ⟩−W), ΔM = (η/τ)(⟨yyᵀ⟩−M)∘(mask+I);
  - minibatch-averaged local updates, η 0.02→0.002, τ 0.5, 1–3 epochs fixed on dev;
  - classes C0, C1, C2, C3, C4, **C4DP** (degree-preserving double-edge-swap of C4: the most dangerous sham) and C5;
  - **G = 30 graph instances** per random class (C1, C2, C4, C4DP), seeds 0–29; C0, C3 and C5 are deterministic graphs with 30 init seeds; init seed = graph seed.
- Secondary engine: masked NSM (rectified), same grid.
- **Backprop baseline:**
  - MLP 48→24(ReLU)→48, Adam, lr {1e-3, 3e-3} × wd {0, 1e-4}, batch 256, ≤ 100 epochs, early-stopping patience 8 on inner-val subjects, 10 seeds;
  - the configuration is chosen per fold by inner-val MSE, and every configuration counts in the search budget;
  - primary contrast form: **encoder-then-common-ridge** (freeze the hidden layer, refit the same ridge), so only the learning rule differs;
  - end-to-end as a secondary.
- Optional non-local reference "ReSU-batch" (the paper's method): past–future CCA on the train fold, window [x_t, x_{t−1}], 12 ON + 12 OFF units. It is labelled non-local and excluded from all hypothesis families.
- Name the engine "masked-lateral similarity-matching (PSP/NSM)". It is not ReSU.

**Metric**
- **Primary:** per-confirm-subject skill S = 1 − MSE_model/MSE_persistence, over all valid (t, t+h) pairs and 48 ROIs. At h = 1 every TR = 2.0 subject has ≥ 99 pairs.
- S is averaged over the 30 runs within subject, then over subjects.
- Secondary: per-subject R² with reference mean 0; centered PR(Y) on test subjects; RF orthogonality; distinct filters. Drop "PR per 100 synapses" (C0 is 0 by construction).

**Uncertainty**
- Crossed bootstrap: resample confirm subjects (site-stratified) and graph instances independently within each class. B = 2000, seed 20261101.
- Also report the subject-only CI and a 13-site cluster bootstrap as sensitivities.

**Stability rule**
- A run is unstable if λ_min(M) ≤ 0 at any update or any value is non-finite.
- An unstable run is a failure counted in its condition and reported, not dropped. More than 10 % unstable in a condition makes that condition inconclusive (execution integrity).

### 4.3 Card (dated, frozen once, after the dev stage and before opening confirm; sha256 in `results/topic4/<date>/card_sha256.txt`)
- **Mode:** CONFIRMATORY on the confirm split; dev-stage results are EXPLORATORY and declared as seen.
- **H1 (primary, the original core claim):**
  - Statement: at 69/276 lateral edges, C4 gives higher S than C1. Estimand Δ₁ = S̄_C4 − S̄_C1 (class means over instances and subjects). One-sided, with a two-sided 95 % CI.
  - Verdicts:
    - **keep** if CI_low(Δ₁) > 0, Δ₁ ≥ δ and CI_low(S_C4 − S_C4DP) > 0;
    - **modify** if H1 passes but C4 − C4DP does not (the effect comes from the degree sequence, not the Mode-II arrangement);
    - **stop (killed)** if CI_high(Δ₁) < δ;
    - **inconclusive** otherwise;
    - **no_candidate / software failure** if a pre-confirm gate fails (below).
- **Pre-confirm gates (stop before confirmation; not a science verdict):**
  - (G-a) frozen-code PSP passes F5 and F6–F8;
  - (G-b) non-saturation on dev: identity-ridge R² < 0.9 and persistence R² < 0.9 at h = 2 s;
  - (G-c) MLP adequacy F11 passes;
  - (G-d) no ID strings in outputs.
- **Secondary family (Holm):**
  - C4−C4DP; C4−C2; C4−C3; best-sparse − C0; C5 − best-sparse;
  - best-local − random-ReLU;
  - MLP-enc vs PSP-C5 non-inferiority (margin δ_NI = δ);
  - mechanistic **H-α**: Spearman ρ(S, α(G)) < 0 across all sparse instances (instance bootstrap).
- **Expected outcomes, written into the card before results (from synthetic probes; not forecasts):**
  - Δ₁ ≈ 0 within instance SD; C3 < C1; C0 lowest; PSP-C5 ≈ PCA-24 < identity ridge, by construction of a 24-d code;
  - MLP-enc ≈ RRR-24 ≥ PSP-C5; H-α negative.
  - The PI should expect H1 to end "stop" or "inconclusive". That is a valid result.
- **δ (MEI): UNSET until the dev stage, for PI acceptance.** Proposed rule: δ = max(0.005, 0.10·(S_C5 − S_C0)) measured on the dev split. Do not copy the synthetic value (probe C would give 0.013).
- **Seeds and budget:**
  - local seeds 0–29; MLP seeds 0–9; MLP grid of 4 configurations × 10 seeds × 5 folds; bootstrap seed 20261101;
  - no seed selection;
  - all runs, including failed ones, go in a run ledger with code, config and input hashes.
- **Compute:** CPU only, local nice ≤ 4 processes. Estimated < 1 CPU-hour: local family ~1.5k fits × ≤ 1 s, MLP 200 fits × ~6 s. 0 GPU-h.

### 4.4 T4.3 — implementation fixtures, beyond 4.1 (ID / defect / pass criterion)
- **F5 planted subspace:**
  - PSP-C5 centered PR within 10 % of the planted-spectrum PR and decode R² ≥ 0.95; C0 PR < 1.5;
  - the **legacy engine must fail it** (dense PR 2.6, decode 0.42);
  - test at 3 or more sample sizes / spectra.
- **F6 stability, local:**
  - assert λ_min(M) > 0 after every update;
  - the update function contains no `eig`/`eigvals`/`svd`/global rescale (AST check);
  - mutants that freeze the M diagonal, or use an η large enough to break the condition, must raise;
  - if the rectified dynamics y = [Wx − M_off y]₊ are used, check ρ(D⁻¹M_off) < 1. Any bound must be per-neuron (Gershgorin row sum), not a global projection.
- **F7 no-autograd:**
  - AST scan of `src/topic4_resu/local/`: no `torch`/`jax`/`tensorflow`/`autograd` imports; no `.backward`, `.grad` or `torch.func`;
  - runtime: run the local `fit` in a subprocess with a `sys.meta_path` finder that raises on `import torch`;
  - the API takes no targets;
  - a mutant importing torch in `local/` must fail.
- **F8 locality:**
  - ΔW_ij and ΔM_ij equal the elementwise formula from (x, y, own weight);
  - non-edges stay exactly 0 for all updates.
- **F9 topology:**
  - 69 edges for C1–C4DP at every seed;
  - C4 designated-hub edges = 0;
  - the C4DP degree sequence equals C4's;
  - R_hub reported under both hub definitions, with the card stating which one the claim uses.
- **F10 split:**
  - subject-disjoint (`group_overlap_audit`);
  - burned positions excluded;
  - confirm-manifest hash verified.
- **F11 MLP adequacy:** on the VAR fixture, tuned MLP-enc ≥ RRR-24 − 0.01 (probe E: 0.3450 vs 0.3498).
- **F12 no IDs:** scan outputs (pattern list as in `tests/topic3_spectral/test_outputs_no_ids.py`).

### 4.5 Risky choices (flag to root/PI)
- **R1:** H1 has a near-null prior (probe B/C). Freezing it as primary keeps the core goal (sci-pipeline §3.0), but the PI should accept the likely negative verdict. The alternative is to promote H-α to primary; that is a PI decision.
- **R2:** graph-instance variance dominates. With one instance per class (legacy) the class effect is unidentifiable. Use G = 30 and resample instances.
- **R3:** do not reuse or rename the legacy engine. It is non-local (global rescale), asymmetric, collapses and is not ReSU.
- **R4:** whole-series detrend/z-score and the upstream 0.25 Hz filtering are acausal and shared. Claims are contrasts only.
- **R5:** resampled TR sites carry `resample_poly` acausal mixing, so they are sensitivity only.
- **R6:** the survey's backprop number must not be cited (small data, untuned; probe E).
- **R7:** δ needs PI acceptance after the dev stage. Until then the card cannot be frozen with `--strict`.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2; PY=/home/juke/superclaude-env/bin/python3
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo rc=$?     # expect 0
cd verification/explorer_M4_r1_1 && sha256sum -c SHA256SUMS.txt                                                       # probe bytes
nice $PY probe_a_t41_counterfactual.py | python3 -c 'import json,sys;r=json.load(sys.stdin);print(r["pos0"]["protected_function_R2"],r["pos932"]["protected_function_R2"])'   # pos0 all 1.0; pos932 −0.08..0.05 (~20 s; reads 2 subjects)
$PY summarize_b.py                                                                 # reads the saved probe_b_*.out.json: PSP C5 PR≈16.5, C0≈1.3, sparse 1.9–4.2; corr(PR,indep)≈−0.96
nice $PY probe_b_topology_engine.py psp > rerun_b_psp.json 2>/dev/null             # independent rerun to a NEW file (never overwrite receipts); compare centered_PR_Y per run (~5 s, deterministic seeds)
nice $PY probe_c_var1_fixture.py | grep -E "bayes_R2_h1|acausal"                   # 0.3598; acausal 0.536 > Bayes (~25 s)
nice $PY probe_e_backprop_baseline.py | grep -E "RRR24|tuned_es"                   # RRR 0.3498; tuned ≈0.344 (~95 s)
```
**This report is invalidated if any of the following holds:**
- the unmodified protected function returns 1.0 on a subject with ≥ 1 valid test row;
- the canonical PSP fails F5 at the full mask on other spectra;
- C4 beats C4DP and C1 by more than the instance SD on synthetic data with structured covariance (a test I did not run);
- the TR column in the Topic 1 manifest is wrong for the TR = 2.0 sites;
- the peer explorer's burned positions intersect the TR = 2.0 confirm set and are not excluded.
