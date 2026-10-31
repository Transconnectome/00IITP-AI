# handoff — explorer_M2_r1_3 (M2 / Topic 3), 2026-10-31

**Summary.** The core of T3.1–T3.4 fits in CPU-seconds on the 7 local pooled matrices. No B300, no GPU and no regeneration are needed. The real risks are about how to read the numbers, not about compute:
- (i) the centered PR values were already seen (they are in the old report and in this run's probes), so they cannot be confirmatory;
- (ii) sample PR at n = 57 is a biased, n- and D-dependent statistic;
- (iii) a naive bootstrap biases PR downward;
- (iv) per-channel scale (the final LayerNorm gain in layer_3) can move PR_cov, while PR_corr is exactly invariant to it;
- (v) the old rank-slope α is biased at n = 57, and Clauset/Hill on 56 eigenvalues is biased too.

Probes, all reproducible: `verification/explorer_M2_r1_3/probe_{a,b,c,d}_*.py` and their `.log` files.

## 1. Observation

O1. Old estimators (PROTECTED; must not be edited, see C1).
- `src/spectral_rg_flow_diagnostic.py:55-64` computes PR from the SVD of uncentered X.
  - `:84-106` fits the rank slope on uncentered eigenvalues.
  - `:164-172` assigns HTSR regime labels.
  - `:179-183` computes an ad-hoc OOD score.
  - `:229-243` silently substitutes `rng.randn` matrices when a file is missing.
  - `:279` hard-codes `"optimal_ood_layer_identified": "SwiFT_E192_Layer2"`.
- `src/empirical_connectome_ablation.py:143-159` is centered: `Xc = X - mean`, eigvalsh of Xc'Xc/n, and a rank slope over ranks 2..k_max with eigenvalues > 1e-10.
- `src/run_all_empirical_experiments.py:153` writes the uncentered `t3_results` under `analysis_3_foundation_model_rg_flow`.
- All of these are in PROTECTED_HASHES (lines 51, 57, 58 and 66). The protected-hash check gives rc 0 (run at 08:2xZ).

O2. Reproduction (probe A, real data, already-public numbers only).

| Matrix | Uncentered PR (the json) | Centered PR (the report) | Old centered α |
|---|---|---|---|
| L0 | 1.0014 | 2.7773 | 1.4717 |
| L1 | 1.0050 | 2.7782 | 0.9887 |
| L2 | 1.0743 | 11.0202 | 1.5980 |
| L3 | 1.0327 | 3.5786 | 1.8411 |
| BrainLM | 1.0028 | 4.3188 | 1.4580 |
| BrainJEPA | 1.0581 | 11.7851 | 1.8807 |
| NeuroSTORM | 1.0102 | 12.5070 | 1.1960 |

- Every value matches the json and the report table to 4 decimals.
- The old α fit uses 55 eigenvalues (ranks 2..56) at n = 57, and 23 at n = 25. It includes the noisiest tail.

O3. Structure (probe A and probe D).
- All matrices are finite.
- Centered rank is n−1: 56 for the files with 57 rows, 24 for NeuroSTORM.
- Median |column mean|/SD by file: L0 26.7, L1 14.4, L2 3.6, L3 5.9, BrainLM 11.6, BrainJEPA 1.6, NeuroSTORM 10.6.
- Uncentered row cosine ranges are [0.993, 0.9999] for L0 and [0.79, 0.998] for L3. These cosines are the input to the old graph metrics (d_B, R_hub, r).
- Centered cosines span about [−0.9, 0.9].
- Column SD relative to the median runs from 0.29 to 7.0, and no channel is near-constant. PR_corr is therefore numerically safe.

O4. Provenance.
- Hashes are in the table at the end; first 16 hex characters here.
  - layer_0 ec2970e8…
  - layer_1 2730359b…
  - layer_2 ce551606…
  - layer_3 f13ae7ba…
  - BrainLM d0b90e46…
  - BrainJEPA c9c550d7…
  - NeuroSTORM 3d7b2c96…
- The copies on connectome in `/storage/bigdata/VRABES/05_pooled_embedding/` have the same leading hashes for L0–L3, BrainLM and BrainJEPA.
- `RemissionAnalysis/pool_E192_layersweep.py:10-30` builds each layer as the mean over all tokens (and space × time for layer_3), then the mean over 7 frames. It saves `ids` and `X`.
- Extraction is described in `extract_vrabes_swift_E192.sh`:
  - ran on NERSC with the `SwiFT_v2_perlmutter` fork;
  - checkpoint `NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt`;
  - frozen forward pass only.
- In the local ver11 code:
  - `simmim_swin4d_transformer_ver11.py:914-923` runs the downsample at the end of each BasicLayer.
  - `:1068` sets `downsample=None` for the last stage.
  - `:1403-1411` applies `self.norm` and a channel-first reshape to the last layer only. That matches the stored layer_3 shape (1536,2,2,2,20), while layers 0–2 are token-major (L,C).
  - So layer_2 is the output of the stage-2 PatchMerging Linear (8C→2C). layer_3 is the 2 stage-3 blocks plus the final LayerNorm on the same 2³×20 grid.
- BrainLM uses the CLS token (`extract_brainlm_embeddings.py:7`). BrainJEPA uses the token mean (`:8`, `:108`). NeuroSTORM uses global average pooling, then the mean over segments (`extract_neurostorm_embeddings.py:15-16`).
- Row-order checks:
  - All 57 ids are in the same order across L0–L3, BrainLM and BrainJEPA.
  - All 25 NeuroSTORM ids are among the 57.
  - The NeuroSTORM n = 25 is the labelled-remission subset (`probe_neurostorm.py:14`).
  - Connectome holds NeuroSTORM `.pt` files for all 57 subjects (`04_embedding/neurostorm`, 57 files, 688 KB). The extraction log shows 57/57 done with segments of shape (7, 288).

O5. Token-level dumps on connectome (counts only).
- `04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES` holds 57 subjects and 399 frame files, 8.1 GB. Other checkpoints sit under `swift_zoo_ses-01`: deepE192 ×2 with 57 subjects each, E36 with 57, and others with partial counts.
- Raw frames are in `03_MNI_to_TRs`.
- Connectome has no torch: neither the system python3.8 nor the `06_reprocess_20261018/env` cpython-3.12 has it.
- I found no E192 checkpoint on connectome (`swift_v2_downstream/pretrained_ckpts` has only external_baselines) or locally. Local superclaude-env has torch 2.11.

O6. Synthetic estimator behaviour (probe B), at n = 57.

| Population spectrum | Population PR | Sample PR at D = 1536 | Sample PR at D = 384 |
|---|---|---|---|
| a = 2 | 2.50 | 2.49±0.30 | — |
| a = 1.5 | 5.46 | 5.15±0.51 | — |
| a = 1 | 38.1 | 22.8±2.3 | 17.9±1.7 (population 26.0) |

- iid Gaussian: PR is 53.98±0.07 at 57×1536, 52.18 at 57×768, 48.69 at 57×384 and 22.11±0.13 at 25×288.
- Independent columns with lognormal column SD (sdlog 1.0 / 2.0) already give PR 29.9 / 4.9, with no correlation at all.
- n-matching (a = 1, D = 1536): PR is 22.7 at n = 57 and 14.8 at n = 25. Normalising does not equalise them: PR/(n−1) is 0.41 vs 0.62.
- Bootstrap with replacement: on average only 36.3 of 57 rows are unique, so PR is biased down, 18.2±1.7 against a sampling distribution of 22.9±2.5. Subsampling 40 rows without replacement gives 22.2±1.1.

O7. α estimators (probes B and C), n = 57, D = 1536.

| True a | Old slope 2..56 | Window 2..28 |
|---|---|---|
| 0.6 | 0.36 | 0.27 |
| 1.0 | 0.76 | 0.72 |
| 1.4 | 1.30 | 1.27 |
| 2.0 | 2.11 | 2.03 |
| 3.0 | 3.34 | 3.15 |

- On iid data the old slope gives 0.22–0.46. The old code labels that "Over-compressed (Rank Collapse)".
- E[slope | a] is monotone. A simulation-calibrated inversion of the 2..28 slope recovers a = 1.3 → 1.308±0.023 and a = 2.1 → 2.092±0.037.
- Deterministic eigenvalue lists λ_k = k^(−a) give slope = a exactly.
- Hill MLE (k = 20) on Pareto samples (56 points) recovers the density exponent: 2.10±0.25 for target 2.
- On sample eigenvalues Hill is biased: 2.59 for target 1+1/a = 2.0.
- Clauset KS-xmin MLE on sample eigenvalues gives 2.46±0.06 for target 2.0 (a = 1), 1.75 vs 1.667 (a = 1.5) and 1.51 vs 1.50 (a = 2).

O8. Per-channel affine (probe C1). X = m·γ + β, which is algebraically the pooled-LayerNorm form: the mean of (γ⊙n + β) is γ⊙mean(n) + β.
- PR_corr stays at exactly 14.665 for every γ spread.
- PR_cov falls from 10.21 to 4.62 as the γ spread grows (sdlog 0 → 1.5).
- A column shuffle tracks the scale contribution: PR_cov(shuffle) falls from 53.7 to 6.7, while PR_corr(shuffle) stays about 54.

O9. Existing tests.
- `tests/test_empirical_four_topics.py:562-579` tests PR only on zero-mean random matrices, so it cannot catch the centering defect.
- The old AST audits (`tests/test_pilot_connectome.py:161` and `tests/e2e/test_pilot_simulation_e2e.py:97`) scan only `src/*.py` at the top level. A subpackage `src/topic3_spectral/` is outside their scope.

O10. Peers' probes (explorer_M2_r1_1 and r1_2) are synthetic-only for PR and graph metrics; I checked their imports. explorer_M2_r1_2 also has `probe_a_inputs_repro` and `probe_e_provenance`, which read the real files. An iid-noise graph-metric null exists in `explorer_M2_r1_2/probe_d_graph_metrics_null.out.json`: d_B ≈ 4.05, R_hub ≈ 1.83, r ≈ −0.03 at 57×1536.

## 2. Logic chain

L1 (T3.1, PR ≈ 1 vs report). From O1 and O2:
- The json path (spectral_rg_flow_diagnostic) never subtracts the mean. With column means 1.6–27 SD (O3), the first singular direction is the mean vector, so PR is about 1.
- The report used the centered estimator from empirical_connectome_ablation.
- The d_B, R_hub and r columns agree because cosine similarity does not depend on centering in either code path.
- A deterministic fixture (O1, probe B1) separates the two exactly: centered PR = k to 1e-6, uncentered about 1.002 for every k.
- T3.1 is therefore resolved without any new real-data quantity.

L2 (exposure). The point values of centered PR and old-centered α for all 7 matrices were published and have been recomputed here (O2). They cannot be "tested" by a card frozen now.
- The card must declare mode REPLICATION for these values and EXPLORATORY for the rest.
- Decision rules must apply only to quantities that no one in this run has computed on real data:
  - PR_corr
  - column-shuffle and iid nulls on real matrices
  - paired subsampling distributions
  - calibrated α
  - centered-cosine graph metrics
  - matched-n cross-model comparisons, including NeuroSTORM at n = 57

L3 (estimand). Each row is one subject's mean vector, so PR measures how spread out subjects are from one another (rank ≤ n−1). It is not the dimensionality of a layer's representation (O3, O6).
- Sample PR is biased toward the n−1 ceiling, and that bias depends on D (O6). Comparisons are fair only at equal n, and they are clean only when PR ≪ n−1.
- Real values are 2.8–12.5, the low regime where the bias is small at D = 1536 (a = 1.5: 5.46 → 5.15). L2 vs L3, both 57×1536, is the cleanest comparison.
- Comparing L0 (D = 384) with L2 (D = 1536) also mixes in the D-dependence of the ceiling.

L4 (L2 → L3 drop). By architecture (O4) there is no PatchMerging between L2 and L3, so the old causal claim fails whatever the numbers show.
- The final LayerNorm's per-channel γ acts on pooled L3 exactly as γ⊙m + β (O8).
- PR_corr is exactly invariant to it, and needs no checkpoint (none was found, O5).
- So PR_corr(L2) vs PR_corr(L3) separates the per-channel-gain part of the drop from the rest. It does not cover the nonlinear per-token normalisation, which needs token-level data.

L5 (uncertainty). A bootstrap with replacement duplicates rows, which lowers the rank and biases PR down by about 20% (O6).
- Use paired subsampling without replacement (same subject subset for every representation, m = 40) to measure stability of the differences. Label this a stability interval, not a population CI.
- For inference about structure, use nulls at matched shape.

L6 (α). No estimator recovers the population exponent unbiasedly at n = 57 without a model (O7).
- The rank slope is monotone in a, so it can be calibrated against Gaussian power-law simulations at the same (n, D, window). The probe recovered a within ±0.04.
- Density-tail MLEs on 56 sample eigenvalues are biased (Hill 2.59 and Clauset 2.46 for target 2.0) and should be secondary.
- HTSR thresholds are for weight-matrix spectral densities. iid noise gets "rank collapse" (O7), so the labels must go.
- The fixture for "α recovers known tail index" therefore has two tiers:
  - an estimator-level exact or MC check (deterministic eigenvalue list; Pareto samples);
  - an end-to-end calibrated check at the real shapes.

L7 (cross-model). n and D differ (25×288 vs 57×768, O6), and pooling differs (CLS vs mean, O4).
- Matched-n comparison is possible two ways:
  - (a) restrict all models to the 25 NeuroSTORM subjects (all are in the 57, O4);
  - (b) build NeuroSTORM at n = 57 from the connectome `.pt` "mean" fields (O4), after checking that its 25 overlapping rows equal pooled_neurostorm rows.
- No "architecture causes PR" claim can be made from 3 models.

L8 (graph metrics). Uncentered cosines are compressed into [0.79, 0.9999] (O3). The top-20% threshold is then set by tiny differences driven by norm and mean direction.
- Box covering with l_B ∈ {2,3,4} on 57 nodes fits d_B from 3 points.
- At most these belong in the secondary tier: centered cosine, with iid and column-shuffle nulls (O10).

L9 (compute and placement). Everything core is NumPy SVDs on matrices of at most 57×1536: seconds on the local CPU (probes ran in 2–6 s).
- C6 does not list VRABES participant data as allowed on B300, and nothing needs regeneration. So B300 is not used: 0 GPU-h.
- The old top-level AST audits do not scan subpackages (O9). torch is used only to load NeuroSTORM `.pt` files, and that loader belongs in `scripts/topic3_*`, never in `src/*.py` at the top level.

## 3. Caveats

- I did not inspect the perlmutter fork. The layer_3 = final-LayerNorm conclusion rests on the local ver11 code plus the matching stored shapes (O4). The card should state it as "per local ver11; fork unverified".
- I did not open the token-level dumps or the E192 checkpoint. The checkpoint was not found locally or on connectome; it may exist only on NERSC.
- I did not check that NeuroSTORM `.pt` "mean" equals the pooled rows. The worker must do that.
- Calibrated α assumes a Gaussian, rotation-invariant population with a pure power law. Real spectra may be neither, so present it with that assumption.
- The column-SD probe (O3, D) and the cosine ranges are mildly descriptive of the real data. They do not touch any card decision quantity, but the exposure log should list them.
- I did not read explorer_M2_r1_1 or r1_2's handoffs, to stay independent. I looked only at their probe file names and output headers.
- The advisor tool was rate-limited, so this report has not had an outside review.

## 4. Conclusion: recommended strategy for the M2 worker

**Layout** (orchestrator PROJECT.md; do not touch old files):
- `src/topic3_spectral/{estimators.py, nulls.py, io_contract.py}`, NumPy only
- `tests/topic3_spectral/`
- `scripts/topic3_rerun.py`, plus `scripts/topic3_load_neurostorm57.py` if route (b) is used; this is the only file that uses torch
- `results/topic3/2026-10-31/`
- `docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md`, plus `_addendum.md` and `_result_report.md`

**Step 1. T3.1 provenance and diagnosis**
- Data contract in `io_contract.py`:
  - full sha256 of the 7 files (table below);
  - shapes and finiteness;
  - identical id order across the 57-row files, checked in memory;
  - NeuroSTORM rows mapped to positional indices among the 57;
  - halt on any mismatch;
  - `FileNotFoundError` on a missing file; no fallback.
- `ids` are never printed or written; outputs use positional indices only.
- Reproduction table: the old json values via the uncentered function, imported read-only, and the old report values via `estimate_powerlaw_alpha`, imported read-only. Assert equality to 1e-4 with the published numbers.
- Provenance section: NERSC extraction, checkpoint name, pooling per model, n = 25 = the labelled subset, connectome byte-identity, and the ver11 line references.

**Step 2. T3.2 card**, frozen with sha256 before any new real-data quantity. Fields:
- Mode: REPLICATION for the O2 values; EXPLORATORY for everything else.
- Exposure log: what this run has already computed on real data (O2, O3; probe paths). Peers' and survey probes are included.
- Estimand: between-subject spread of pooled representations. n = 57, PR ≤ 56; n = 25 → 24.
- Estimators:
  - PR_cov, centered, eigenvalues of Xc'Xc/(n−1). ddof cancels in PR, but state it.
  - PR_corr, column-standardised.
  - α_slope: OLS of log λ_k on log k over k = 2..⌊(n−1)/2⌋ (2..28 at n = 57; 2..12 at n = 25).
  - α_cal: inversion of E[α_slope | a, n, D] on a grid a ∈ [0.6, 3.0] in 0.1 steps, R = 200 Gaussian simulations per grid point, seed fixed. If the observed value is outside the grid's range, report "not identifiable".
  - Secondary α_density: Clauset KS-xmin MLE, with its measured bias stated.
  - No HTSR regime labels and no OOD score.
- Nulls and controls per matrix:
  - iid Gaussian at the same (n, D), R = 1000;
  - column-wise permutation across subjects, B = 1000. It keeps each column's marginal and destroys correlation.
  - Report each observed value with its null's 2.5–97.5% range.
- Stability: paired subsampling, m = 40 without replacement, B = 2000, seed 20261031 (the same subject subsets for every representation).
- Matched-n comparison:
  - primary: all representations on the 25 NeuroSTORM subjects;
  - secondary: NeuroSTORM n = 57 via route (b), only if the provenance check passes, else marked untested.
- Decision rules (pre-specified; apply to unseen quantities):
  - **D1 (L2 > L3 robust):** at least 97.5% of paired subsamples have ΔPR_cov(L2 − L3) > 0. "Robust and not channel-scale" additionally needs at least 97.5% with ΔPR_corr > 0. If ΔPR_cov is robust but ΔPR_corr is not, the drop is "attributable to per-channel scale (consistent with final-LN γ)".
  - **D2 (structure beyond independent columns):** PR_cov is below the 2.5th percentile of the column-shuffle null.
  - **D3 (cross-model order):** a pairwise ordering is "stable" if at least 97.5% of paired m = 20 subsamples agree at n = 25 (m = 40 at n = 57). Otherwise it is "not resolved".
  - **D4 (α change across layers):** report only if |Δα_cal| exceeds the 95% subsampling stability range. Never interpret it as criticality.
- Verdict mapping for the old claims:

| Old claim | Expected verdict |
|---|---|
| J1: "PR≈1 / rank collapse everywhere" | FAIL (estimator artifact) |
| R1: "L2 PR expands 4×" | descriptive; D1/D2 decide "robust" vs "not robust" |
| R2: "L3 collapse caused by Euclidean PatchMerging" | FAIL (architecture) whatever the numbers. The PR drop itself is judged by D1. |
| R3: "BrainJEPA and NeuroSTORM have PR 2.7× BrainLM" | judged by D3 at matched n. The architectural attribution is untestable. |
| R4: HTSR regimes and "critical α" | FAIL / not applicable |
| R5: "optimal OOD layer = L2" and the OOD score | UNTESTABLE (hard-coded; no OOD data) |
| R6: d_B, r and R_hub patterns | secondary, centered cosine vs nulls; low identifiability |
| R7: NeuroPrior 450-ROI row | out of scope (rows are ROIs of a PCA-200 matrix; a different estimand); reproduction only |

**Step 3. T3.3 fixtures** in `tests/topic3_spectral/`. Write them first and see each one fail on its target defect before the implementation passes:
- **F1 centering:** a rank-k exact construction (k ∈ {1, 5, 20, 56}, U ⟂ 1) plus a 30-SD mean offset gives PR_cov == k to 1e-9.
  - The same fixture applied to the old `compute_participation_ratio` must give < 1.01. The test asserts this, which proves the fixture catches the defect.
  - A mutant with centering removed must fail F1.
- **F2 known PR:** prescribed singular values s give PR == (Σs²)²/Σs⁴ exactly. Also test invariance to row permutation, orthogonal rotation and translation, and PR ≤ n−1.
- **F3 PR_corr:** exactly invariant to per-column affine (γ, β) to 1e-10 (O8). A column-shuffle helper must preserve each column's multiset.
- **F4 α estimator level:**
  - λ_k = k^(−a) gives α_slope == a to 1e-10 for a ∈ {0.5, 1, 2};
  - Pareto(α_d) samples give Clauset/Hill within 3 MC SE (O7 numbers).
- **F5 α end to end:** α_cal on fresh Gaussian draws at 57×1536 recovers a ∈ {1.3, 2.1} within ±0.1 (probe SD ≤ 0.04).
- **F6 nulls:** iid 57×1536 PR_cov within 53.98 ± 0.5, and 25×288 within 22.11 ± 0.5.
- **F7 uncertainty:** the stability routine samples without replacement; assert the number of unique rows == m. A with-replacement mutant must fail.
- **F8 I/O:**
  - a missing file raises (no synthetic fallback);
  - a mismatched id order halts;
  - result files contain no `sub-` substring and no `ids` key.
- Rerun C2 (old 86 tests plus tests/topic1_lagmotif) unchanged.

**Step 4. T3.4 rerun**
- Run `scripts/topic3_rerun.py` locally on CPU with nice and OMP_NUM_THREADS ≤ 4. Expected time is under 5 minutes, including the α_cal grid of 25 × 200 SVDs at 57×1536.
- Run record: input sha256s, code and test sha256s, card sha256 (verified before the run), seeds and numpy version.
- Write the outputs to `results/topic3/2026-10-31/` as JSON plus the raw log.
- The result report gives a verdict for each claim (R1–R7, J1) by the card's rules. It keeps REPLICATION and EXPLORATORY separate and states the estimand caveat (between-subject spread, n = 57).
- No B300 and 0 GPU-h. Add a line to `results/gpu_ledger_2026-10-31.md` only if the root asks for one.

**Optional (only if pre-specified in the card; otherwise list as untested):**
- (a) Token-level within-frame PR on connectome:
  - Read the 399 `.pt` files streamed over ssh into memory, so no ID filenames are written locally.
  - Apply parameter-free per-token LayerNorm to layer_2 tokens, then pool, then compare with layer_3. This tests the nonlinear part of L4.
  - 8.1 GB; CPU only.
- (b) Random-initialisation ver11 forward on connectome GPU with VRABES frames:
  - It needs a project-local torch venv on connectome, a check that the perlmutter-fork code is equivalent to local ver11, and about 1 GPU-h on a node1 RTX.
  - It must never run on B300 (C6).

## 5. Verification method

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
PY=/home/juke/superclaude-env/bin/python3; export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4
$PY verification/explorer_M2_r1_3/probe_a_real_structure.py      # O2/O3/O4 numbers; prints no ids
$PY verification/explorer_M2_r1_3/probe_b_synthetic_estimators.py # O6/O7 (seeded 20261031)
$PY verification/explorer_M2_r1_3/probe_c_controls_synthetic.py   # O7/O8 (seeded 7)
$PY verification/explorer_M2_r1_3/probe_d_colscale.py             # O3 column-scale spread
grep -l "sub-" verification/explorer_M2_r1_3/*   # expect no output (rc 1)
sed -n 1403,1411p /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py  # final norm on last layer only
```

What would invalidate this report:
- the input hashes differ from the table below;
- the perlmutter fork turns out to differ from local ver11 in `_forward_hook_embedding`;
- NeuroSTORM `.pt` "mean" rows do not match pooled_neurostorm, which kills route (b);
- someone in the run has already computed PR_corr, column-shuffle nulls or subsampling on the real matrices, which must then go into the exposure log and out of the decision rules.

Full input sha256:

| File | sha256 |
|---|---|
| layer_0 | ec2970e871b8b060d24db177d8b7f45ad6302f9ee57f8c6c0e6b9a8a6627e584 |
| layer_1 | 2730359bfc0bd208c9c6e43ebbbc7ceccf657a55005934e5e4511a3dbaa5be4d |
| layer_2 | ce55160669f77870c11ead261e5c061680791a4c755e8ea7d0db58c957828eab |
| layer_3 | f13ae7ba126bdc5a2c17efc0cb032910c07b7e14411aeb9546deb9d68dadc8eb |
| BrainLM | d0b90e46ec638d5c00e0d6c0747030ef2b5b3788f097c5585e60c71e5085a80a |
| BrainJEPA | c9c550d73acb599cc646fd5d9902e36c839e504b4a7e1983ed4a491509a4df87 |
| NeuroSTORM | 3d7b2c9630e773a1f720c9731856bea6cba9ae27232b01a47afcdf29edd2f4da |
| ver11 model file | de132387f64d98cbe9b15876351a7b33f9bec112df3df8f4718327d06e95052a |
| pool_E192_layersweep.py | 0e408552317007416a0f2b7fc779c5ab2dc250369da8c006be9adb9d70b30fbb |
