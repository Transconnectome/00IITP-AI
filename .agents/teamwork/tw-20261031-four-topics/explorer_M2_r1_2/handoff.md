# explorer_M2_r1_2 — handoff (M2 Topic 3, strategy for T3.1–T3.4)
Written 2026-10-31 (UTC ~08:50). Read-only investigation. Probes: /home/juke/git/00IITP-AI/verification/explorer_M2_r1_2/ (probe_a … probe_i, each with its .out file).

**Summary.** The public report numbers reproduce exactly with the centered estimator, and the json's PR≈1 is the uncentered SVD. Most of the survey's estimator and control choices fail at the real shapes, though:
- **Clauset α:** at N=57 the MLE is biased (true 2.0 → 2.54; noise → 10).
- **"LN-matched" comparison:** the survey's version (parameter-free LN on layer_2) is not matched. Covariance PR moves 1.07 → 37.9 → 15.0 depending on the LN affine; only correlation-PR is invariant.
- **Row bootstrap:** it biases PR downward by up to 44%.
- **Column-permutation null:** it rejects everything, so it decides nothing.
- **Graph metrics:** d_B, R_hub and r track effective rank and sit inside the noise range.

What does work:
- **Matched comparisons need tokens.** A matched layer-2 vs layer-3 comparison requires the token-level frame dumps on connectome. Those exist for 4 E192-family checkpoints with the same 57 subjects.
- **The random-init control is cheap on CPU.** A random-init ver11 E192 forward pass takes 4.4 s per window on local CPU, with shapes identical to the dumps.

## 1. Observation

O1 Inputs (probe_a; ID arrays read into memory only, never printed). The sha256 values:

| File (VRABES/RemissionAnalysis/) | sha256 | X shape |
|---|---|---|
| pooled_E192_layers/layer_0.npz | ec2970e871b8b060d24db177d8b7f45ad6302f9ee57f8c6c0e6b9a8a6627e584 | 57×384 |
| pooled_E192_layers/layer_1.npz | 2730359bfc0bd208c9c6e43ebbbc7ceccf657a55005934e5e4511a3dbaa5be4d | 57×768 |
| pooled_E192_layers/layer_2.npz | ce55160669f77870c11ead261e5c061680791a4c755e8ea7d0db58c957828eab | 57×1536 |
| pooled_E192_layers/layer_3.npz | f13ae7ba126bdc5a2c17efc0cb032910c07b7e14411aeb9546deb9d68dadc8eb | 57×1536 |
| pooled_brainlm_matrix.npz | d0b90e46ec638d5c00e0d6c0747030ef2b5b3788f097c5585e60c71e5085a80a | 57×768 |
| pooled_brainjepa_matrix.npz | c9c550d73acb599cc646fd5d9902e36c839e504b4a7e1983ed4a491509a4df87 | 57×768 |
| pooled_neurostorm_matrix.npz | 3d7b2c9630e773a1f720c9731856bea6cba9ae27232b01a47afcdf29edd2f4da | 25×288 |

- **`ids` arrays.** In every file `ids` is `<U8`, so it loads with `allow_pickle=False`.
- **Subject order.** All six 57-row files have identical subject order.
- **NeuroSTORM rows.** The 25 NeuroSTORM rows are a subset of those 57. Their positions in the 57-row order are increasing, so a matched 25-row subset can be built by position alone, without IDs.
- **Duplicate file.** `pooled_E192/whole_brain_layer3_matrix.npz` is byte-for-byte equal in X to `layer_3.npz`.

O2 Reproduction of already-public numbers (probe_a). The verbatim logic of `src/empirical_connectome_ablation.py:143-160` gives the following centered PRs. These match the EMPIRICAL_ANALYSIS_REPORT table exactly:

| Input | Centered PR |
|---|---|
| L0 | 2.7773 |
| L1 | 2.7782 |
| L2 | 11.0202 |
| L3 | 3.5786 |
| BrainLM | 4.3188 |
| BrainJEPA | 11.7851 |
| NeuroSTORM | 12.507 |

- Centered α for L2 is 1.598.
- Uncentered PR gives 1.0014 / 1.0050 / 1.0743 / 1.0327 / 1.0028 / 1.0581 / 1.0102, matching the json.
- The mean vector carries 96.5–99.9% of the energy. The median |column mean|/SD is 1.6–26.7.
- The old α fit (`ranks 2..max(10,D//2)`) actually uses all 55 non-zero eigenvalues, so it runs into the rank-cutoff tail.

O3 Synthetic estimator behaviour at the real shapes (probe_b). Eigenvalues were set to λ_i = i^(−a), so the true density exponent is 1 + 1/a.
- **Exact population spectra.** Rank-slope and the Clauset KS-xmin MLE both recover the truth to within 0.03. This shows the code is correct. It is not a valid sampling fixture.
- **Sampled data at N=57, D=1536:**

| Quantity | Truth | Estimate |
|---|---|---|
| Density exponent, a=1 | 2.0 | MLE 2.54 |
| Density exponent, a=0.5 | 3.0 | MLE 6.88 |
| Rank slope, a=1 | 1.0 | 0.725 |
| PR, a=1 | 38.1 | 21.6 |
| PR, a=0.5 | 748 | 52.1 |

- **Steep spectra (a=2)** are recovered: PR 2.73 against 2.50, MLE 1.524 against 1.5.
- **Recovery becomes acceptable only at N ≥ ~1280.** At N1280/D768, a=1 gives MLE 2.068. At N10240/D384 it gives 2.011.
- **N=25 vs N=57 have different biases:** at a=1 the sample PR is 11.6 at N25/D288 and 21.3 at N57/D768.
- **Pure iid noise:**

| Shape | PR | PR/(N−1) | Old ablation α | MLE |
|---|---|---|---|---|
| N57/D1536 | 54.0 | 0.964 | 0.22 | 10.3 |
| N57/D384 | 48.7 | — | 0.46 | 5.5 |
| N25/D288 | 22.1 | — | 0.40 | 5.2 |

O4 The old similarity-graph metrics (probe_d) were computed with functions imported read-only from `src/empirical_connectome_ablation.py`, 20 reps each, N=57.

| Input | d_B | R_hub | r |
|---|---|---|---|
| iid noise, 57×1536 | 4.05 ± 0.22 | 1.83 ± 0.39 | −0.028, range −0.115..0.073 |
| rank-3 + common mean | 1.32 | 4.33 | +0.31 |
| rank-11 + common mean | 2.28 | 4.21 | −0.04 |

- The report gives L3 R_hub = 4.62 with r = +0.343, and L2 r = −0.0652.
- It gives BrainJEPA r = −0.0826. NeuroSTORM r = −0.1923 is at N=25.

O5 LayerNorm (probe_f, synthetic 160×1536).
- Correlation-matrix PR is invariant to a per-dimension affine (γ with random sign and scale, β). The difference between corrPR(LN0(X)) and corrPR(LN0(X)·γ+β) was 2.8e−14.
- Covariance PR is not invariant: raw 1.067, LN0 37.9, LN with affine 15.0.
- Token-level PR ceilings per frame are min(n_tok − 1, D): L0 384, L1 768, L2 and L3 159. At a flat a=0.5 spectrum, sample PR is 213 / 306 / 131 / 131 against population 218 / 404 / 748 / 748.

O6 Bootstrap (probe_i, synthetic N=57, D=1536).

| Spectrum | Full-sample PR | Row bootstrap with replacement | Subsample 40 | Jackknife |
|---|---|---|---|---|
| a=0.7 | 45.6 | 25.5 | 33.7 | 44.9 |
| a=1.0 | 20.7 | 15.4 | 18.0 | 20.6 |
| a=1.5 | 4.84 | 4.51 | — | 4.83 |

O7 Frame dumps on connectome (probe_c streamed one frame per checkpoint into memory, so nothing was stored at rest; probe_e).

| Checkpoint | Frames | Size | Layer tensors |
|---|---|---|---|
| `/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES/` | 57 subject dirs, 399 frame*.pt | 8.1 GB | layer_0 (10240,384), layer_1 (1280,768), layer_2 (160,1536), layer_3 (1536,2,2,2,20), float32 |
| swift_zoo_ses-01 HCP_N400_T2400_E192 | 399 | — | same shapes |
| swift_zoo_ses-01 NewUAH_deepE192_L1e-4 | 399 | — | same shapes |
| swift_zoo_ses-01 NewUAH_deepE192_L5e-5 | 399 | — | same shapes |
| swift_zoo_ses-01 NewUAH_E36 | 399 | — | dims 72 / 144 / 288 / 288 |

- All four zoo directories have the **same subject-directory set** as the primary (md5 of the sorted listing).
- Other zoo dirs are incomplete: E96 287, E192 147, E96_SL60 114, HCP_N800 34, and two dirs with 0.
- connectome system python 3.8 has no torch, and no conda or venv was found. Local superclaude-env has torch 2.11.0.dev+cu130, monai 1.5.1, scipy 1.15.3 and sklearn 1.7.2. The `powerlaw` package is not installed.

O8 Random-init feasibility (probe_h). Setup:
- I loaded `SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py` read-only through importlib with bytecode writing disabled.
- I built `Simmim_RoPE4DSwinTransformer` with the VRABES E192 config: img 96³×20, patch 6,6,6,1, window 4,4,4,10, depths 2,2,18,2, heads 6,12,24,48, c_multiplier 2, mergingv2.
- I called `_forward_hook_embedding` on a synthetic (1,1,96,96,96,20) tensor.

Result:
- Build time was 5.9 s and the model has 474.23 M parameters.
- **One CPU forward pass took 4.4 s with 8 threads.**
- The output shapes are identical to the dumps.

The real input frames, 03_MNI_to_TRs (55 GB of patient images), exist only on connectome.

O9 Throughput from DGX-Spark to connectome over ssh (probe_g): one 21.6 MB frame took 48.7 s end to end. That figure includes `ls` and `sort` on the remote side. Splitting connection latency from bandwidth is in `probe_g_throughput.out.txt`, if it completed before this handoff (see Caveats).

O10 Architecture (confirmed from the code, consistent with survey 2):
- ver11 `_forward_hook_embedding` (lines 1382-1412) records layer_i after stage i. The stage includes the PatchMergingV2 merge (pre-norm LN(8C) followed by Linear) for i < 3.
- Only layer_3 gets the final `self.norm`. It is then reshaped to (C,D,H,W,T).
- layer_2 and layer_3 share the same 2³×20 grid at 1536-d. No merge sits between them.
- The pooling script `pool_E192_layersweep.py` takes the token mean for layers 0–2 and the mean over (D,H,W,T) for layer_3. Both are means over 160 positions for L2 and L3, then a mean over the 7 frames.

O11 Protected files: `src/spectral_rg_flow_diagnostic.py` (71536af2…) and `src/empirical_connectome_ablation.py` (d49105794…) are listed in PROTECTED_HASHES. Survey 1's must_fix "replace the silent fallback at spectral_rg_flow_diagnostic.py:229-239 with an error" would therefore break C1.

## 2. Logic Chain

1. **T3.1 provenance.** O2 shows the report used the centered estimator and the json the uncentered one. The fixture is a rank-k matrix plus a large offset. The protected old `compute_participation_ratio` must return ≈1 on it (assert < 1.5), and the new estimator must return ≈k. This catches the defect without editing protected code.
2. **Subject-level PR.** At N=57 it measures between-subject spread with a ceiling of 56, and its sample bias depends on N, D and spectrum shape (O3). Comparisons across N (NeuroSTORM 25) or D (L0 384 vs L2 1536) are therefore confounded unless they are calibrated against matched synthetic data. L2 vs L3 shares N and D, but differs by the final LN (O5, O10).
3. **The LN confound.** LN changes covariance PR by an order of magnitude (O5). A comparison that accounts for LN therefore needs per-token LN0 on L2 tokens, followed by corrPR, compared against corrPR of L3 tokens. LN is per-token, so it cannot be applied to the pooled vectors. The frame dumps are required (O7).
4. **α.** The MLE and the rank slope are only trustworthy where N ≫ the number of eigenvalues fitted (O3). At subject level α is not estimable to a useful accuracy. At token level the per-frame counts are L0 10240×384 and L1 1280×768, both acceptable. L2 and L3 have 160×1536 per frame, so the 7 frames of a subject must be concatenated to 1120×1536, or α must be reported only against a matched synthetic calibration. The fixture must sample data at the exact (N,D); exact-spectrum fixtures cannot fail on sampling bias.
5. **Uncertainty.** Row bootstrap inside a PR computation biases it downward (O6). For subject-level PR use the jackknife. For token-level per-subject PRs the subject is the unit, so an ordinary paired subject bootstrap or sign-flip test of the per-subject differences is valid.
6. **Nulls.** The column-permutation and iid null gives PR/(N−1) ≈ 0.96 (O3), and every real PR of 2.8–12.5 is far below it. It is a sanity check, not a discriminating control. The discriminating controls are:
   - random-init weights on the same frames, which O8 shows is feasible on CPU (399 × 4.4 s ≈ 30 min per seed);
   - the three other trained E192 checkpoints on the same subjects and frames (O7), which give a replication across training runs at zero GPU cost;
   - paired comparisons across layers within subject.
7. **Graph metrics.** Probe D (O4) shows they follow effective rank. A low-rank synthetic with a common mean reproduces the report's L3 pattern, and the L2 and BrainJEPA "disassortativity" falls inside the iid-noise range. The old graph claims are therefore unsupported by the data as analysed. The card should either drop them or test them against the same random-init and checkpoint controls.
8. **Old claims to adjudicate in T3.4.** The likely status of each:

| # | Old claim | Likely status |
|---|---|---|
| a | PR≈1, "rank collapse" (json) | Artefact; fixture-demonstrated |
| b | "Layer-2 PR expansion 2.78→11.02" | Reproduces numerically at subject level. Its meaning depends on token-level, LN-matched and random-init results |
| c | "Layer-3 Euclidean PatchMerging collapse" | Mechanism false (O10). Whether the drop survives LN matching is an open empirical question |
| d | Graph metrics | Unsupported (O4) |
| e | "JEPA/NeuroSTORM 2.7× BrainLM" | Confounded by N, D and pooling (CLS vs mean). Test it at matched 25 with D-calibration, or label it not comparable |
| f | HTSR regimes (α 1.5–2 "critical") | Category error. Noise gets labelled "rank collapse" |
| g | "Optimal OOD layer = L2" | Hard-coded; untestable (no OOD data) |

## 3. Caveats

- Probe A computed real-data values, limited to exact reproduction of numbers already published in the report and json. I computed no token-level PR, no corrPR, no α under the new estimators and no null values on real data.
- **The re-pooling provenance check (probe_e) is not complete.** The first run was killed by its 300 s timeout. A second run (`probe_e_repool_run2.out.json`) may or may not have finished when this handoff was written; see progress.md. Until frames are shown to re-pool to npz row 0 within allclose, the link between the connectome dumps and the local npz (made at the NERSC path) is inferred from identical shapes, subject sets and checkpoint names. The worker must run this check first.
- Throughput is the main logistics risk. The first measurement is ≈0.44 MB/s end to end. If bandwidth really is that low, 8.1 GB takes about 5 h per checkpoint. The fallback is a project-local CPU venv on connectome node4. C4 permits this, but torch and monai on py3.8 are unverified. I did not create it.
- The random-init forward pass was timed only on synthetic input with 8 threads. Real windows also need the VRABES dataloader's normalization, which I did not inspect. The worker must replicate the extraction script's input preprocessing (`VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` and its python entry point).
  - The random-init weights use the model's own initializer at a fixed seed.
  - The 474 M parameter count looks large for E192. I did not reconcile it with the trained checkpoint, and the trained checkpoint itself was not checked.
- dgx1 was not checked.
- swift_zoo_ses-02 contents were not checked.
- Within-frame tokens are spatially and temporally correlated, so token-level PR is a descriptive within-window statistic, not an iid-sample estimate.
- The direction of the hypotheses (L2 > L3) was suggested by data already seen, so the rerun is REPLICATION or pre-specified-but-not-blind, not confirmatory discovery.

## 4. Conclusion — recommended worker strategy

**Mode.** Two modes, each declared in the card:
- REPLICATION for the subject-level numbers.
- PRE-SPECIFIED for the new estimators and controls. These were frozen before computation, but their direction was suggested by data already seen.

**Layout** (PROJECT.md):
- src/topic3_spectral/: estimators.py, nulls.py, io_frames.py
- tests/topic3_spectral/
- scripts/topic3_*.py
- results/topic3/2026-10-31/
- docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md, plus the result report and any addendum

Never edit old src/*.py. Import them read-only only inside fixtures.

**Step 0 (T3.1, before the card):**
- Write a provenance doc with the sha256 table from O1, the producers (pool_E192_layersweep.py, extract_*), the pooling per model, the N per model and the ver11 layer semantics (O10).
- Run the exact-reproduction script for the public numbers, labelled as already public.
- Run the re-pooling check on frames from positions 0–2.

**Step 1: tests first (T3.3).** Every fixture must fail on the defect it targets.
- F1 (centering): a rank-k matrix plus offset 10·SD, for k ∈ {1, 5, 20}. New centered PR within 10% of the analytic sample value. Old protected `compute_participation_ratio` returns < 1.5. Old uncentered result ≠ new.
- F2 (PR on known spectra): sampled at each real (N,D) in {(57,384), (57,768), (57,1536), (25,288), (160,1536), (1280,768), (10240,384), (1120,1536)}. Assert agreement with the precomputed expected sample PR within a Monte-Carlo tolerance, not with the population PR.
- F3 (α):
  - Exact-spectrum recovery within 0.05 checks the code.
  - Sampled-data recovery at each shape where α will be reported: pass if |bias| ≤ 0.15 in density exponent at a ∈ {0.5, 1, 2}.
  - A shape that fails is marked "α not estimable" in the card, which forbids reporting α there.
  - Expected from O3: N ≥ ~1000 passes and N = 57 fails.
- F4 (LN invariance): corrPR(LN0(X)) == corrPR(LN0(X)·γ+β) within 1e-10. Covariance PR differs.
- F5 (data contract):
  - a missing file, a sha256 mismatch, or `ids` access via `allow_pickle=True` raises;
  - the loader never returns `ids`;
  - no silent synthetic fallback.
- F6 (uncertainty): show that the row bootstrap is biased on synthetic data, and that the jackknife is used for subject-level PR.
- F7 (orientation): the layer_3 reshape from (C,D,H,W,T) to (DHWT, C) gives 160×1536.

**Step 2: freeze the card (T3.2) and record its sha256 before any new real-data computation.**
- Estimands:
  - E1: subject-level centered PR (N=57, and the matched 25 for cross-model), with jackknife SE, reported as PR, PR/(N−1) and the ratio to a matched-shape synthetic calibration.
  - E2 (primary): token-level PR per (subject, frame, layer), averaged over 7 frames, for covPR and corrPR.
  - E3: α only at the shapes that pass F3, using the Clauset KS-xmin MLE on eigenvalues. The method, xmin rule and minimum tail size are stated in the card. The rank slope is secondary over a fixed window [2, 50].
- Hypotheses:
  - H1 (primary, LN-matched): mean over subjects of log corrPR(L3 tokens) − log corrPR(LN0(L2 tokens)) < 0. Paired sign-flip permutation (B = 9,999, seed fixed) plus a subject-bootstrap 95% CI on the mean log ratio.
  - H2: the trained − random-init difference in the H1 contrast is ≠ 0. Random-init uses ≥ 3 seeds, the model's default initializer and the same frames.
  - H3: the sign of the H1 effect replicates in ≥ 2 of the 3 other E192 checkpoints (HCP_N400, deepE192 L1e-4, deepE192 L5e-5).
  - H4 (descriptive): the L0→L1→L2 profile, with tokens subsampled to a common n_tok = 160 per frame and seeded. This removes the N-dependence in O5.
  - H5 (cross-model): only at matched 25 subjects, with D-calibration. Otherwise "not comparable". The pooling differences are recorded.
- Multiplicity: Holm over H1–H3.
- Kill rules:
  - "Layer-3 compression" is killed if H1's CI includes 0, or if H2 shows random-init with the same sign and |diff| within the trained CI, or if H3 fails.
  - Graph metrics are out of scope, and the report says they are unsupported per O4. Alternatively the card requires the same H2/H3 controls for them.
  - No HTSR regime labels, no OOD score.
- State that the direction was suggested by data already seen.

**Step 3: data path.**
- Stream frames from connectome into memory on DGX-Spark, with nothing written at rest. Map subject dirs to sorted positions in memory and check that the order equals the npz order.
- Store only per-(position, frame, layer) eigenvalue spectra and summaries in results/topic3/2026-10-31.
- If O9 bandwidth makes streaming infeasible, set up a project-local CPU venv on connectome node4 under the project's own directory. Never write to B300; C6 rules it out because these are patient-derived.

**Step 4: random-init.**
- Model built as in probe_h. Inputs: the same VRABES windows, preprocessed exactly as the extraction script does.
- Run on connectome CPU (node4, 96 cores) with a venv, or stream input windows to DGX-Spark CPU. The local GPU is last resort, and no GPU is actually needed: ≈30 CPU-min per seed.
- If the preprocessing cannot be replicated, H2 is declared inconclusive in an addendum. Do not substitute synthetic input.

**Step 5 (T3.4).** Run the analysis. Results go in results/topic3/2026-10-31/: raw log, params hash, input hashes, card hash. The dated report gives the claim table a–g with a verdict for each (holds / fails / untestable / not comparable) and the deviations addendum. Do not cite EMPIRICAL_ANALYSIS_REPORT numbers as results (C8). The reproduction is labelled as a reproduction.

## 5. Verification Method

- Rerun the probes. Each prints only shapes, booleans or synthetic values:

  ```
  cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_M2_r1_2/probe_a_inputs_repro.py
  PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_M2_r1_2/probe_b_estimator_behaviour.py
  PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_M2_r1_2/probe_d_graph_metrics_null.py
  PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_M2_r1_2/probe_f_ln_invariance.py
  PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/explorer_M2_r1_2/probe_i_bootstrap_bias.py
  PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/explorer_M2_r1_2/probe_h_randinit_cpu.py
  ```

  Probe_h takes about 15 s.
- C1: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` must give rc 0.
- Invalidation conditions:
  - frames do not re-pool to npz rows;
  - any VRABES npz sha256 differs from O1;
  - the zoo subject sets differ;
  - the random-init output shapes differ from the dumps.
