# Topic 3 analysis card — layerwise participation ratio / spectral diagnostics rerun (2026-10-31)

Status: FROZEN when its sha256 is written to `results/topic3/2026-10-31/card_sha256.txt`. Any later change goes in a dated addendum (`2026-10-31_topic3_addendum.md`); this file is never edited after freezing.
Author: worker_M2_r1 (run tw-20261031-four-topics). Provenance note: `2026-10-31_topic3_provenance.md`.

## 1. Question and research mode

Single question: **do the layerwise effective-dimension claims made for SwiFT E192 and the other brain foundation models in EMPIRICAL_ANALYSIS_REPORT.md §3 survive centered estimators, matched comparisons and controls?**

- **REPLICATION** for the already-public subject-level numbers (centered PR and old α of the 7 pooled matrices; the json's uncentered PR≈1). These were reproduced exactly before this card (T3.1) and cannot be confirmatory.
- **PRE-SPECIFIED (not blind)** for every new quantity: correlation PR, nulls, subsampling intervals, matched-n comparisons, token-level spectra, LN-matched contrasts, checkpoint replication, new α. Their direction (L2 > L3) was suggested by data already seen (§11), so a "holds" verdict is a pre-specified test of a seen pattern, not a discovery.

## 2. Inputs and data contract (halt on violation; no auto-correction, no synthetic fallback)

| Name | File (read in place, `/home/juke/git/VRABES/RemissionAnalysis/`) | sha256 | shape | pooling |
|---|---|---|---|---|
| L0 | pooled_E192_layers/layer_0.npz | ec2970e8…27e584 | 57×384 | SwiFT token mean, then mean over 7 frames |
| L1 | pooled_E192_layers/layer_1.npz | 2730359b…aa5be4d | 57×768 | same |
| L2 | pooled_E192_layers/layer_2.npz | ce551606…828eab | 57×1536 | same |
| L3 | pooled_E192_layers/layer_3.npz | f13ae7ba…dc8eb | 57×1536 | mean over (D,H,W,T) of the post-final-LayerNorm stage-3 output |
| BrainLM | pooled_brainlm_matrix.npz | d0b90e46…5a80a | 57×768 | CLS token |
| BrainJEPA | pooled_brainjepa_matrix.npz | c9c550d7…a4df87 | 57×768 | token mean |
| NeuroSTORM | pooled_neurostorm_matrix.npz | 3d7b2c96…f4da | 25×288 | global average pooling |

Full hashes: `src/topic3_spectral/io_contract.py::PINNED`.
- The loader returns X only and opens files with `allow_pickle=False`. A missing file raises; a hash mismatch raises.
- `ids` arrays are read only in memory, to check order and subset positions. They are never printed or written. All outputs are keyed by row position.
- **Halt conditions:**
  - the six 57-row files do not share one row order;
  - any NeuroSTORM row is absent from that order.
- **Token data.** Frame dumps live on connectome at `/storage/bigdata/VRABES/04_embedding/`:
  - primary `swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES`;
  - zoo `swift_zoo_ses-01/{HCP_N400_T2400_E192, NewUAH_deepE192_L1e-4, NewUAH_deepE192_L5e-5}/VRABES`.
- **Token computation** runs in place on connectome under Slurm with system python3.8 + numpy, using a restricted torch-free unpickler. Only position-keyed summaries come back. **Job halts if any of these fail:**
  - the zoo subject-directory list differs from the primary;
  - the connectome npz copies (`/storage/bigdata/VRABES/05_pooled_embedding/pooled_E192_layers`) differ from the pins;
  - npz row order differs from sorted directory order;
  - any subject has ≠ 7 frames or an unexpected shape;
  - the re-pooled L0–L3 vector of any of the 57 subjects differs from its npz row (allclose atol = rtol = 1e-5). This is the provenance proof that the frames are the source of the npz and that positions align.
- **Data governance.** Nothing goes to B300. No GPU is used.

## 3. Estimators (all centered)

| Symbol | Definition |
|---|---|
| covPR | (Σλ)²/Σλ², λ = eigenvalues of (1/n)XcᵀXc, Xc column-centered. Gram trick when n < D. At most min(n−1, D) eigenvalues. |
| corrPR | covPR of the column-standardized matrix. Columns with SD ≤ 1e-3 × median SD are dropped as dead; the count is reported. Exactly invariant to per-column affine maps, i.e. to LayerNorm gain γ and bias β on pooled vectors. |
| LN0 | parameter-free per-token LayerNorm (x − mean)/√(var + 1e-5). eps = 1e-5 is the torch nn.LayerNorm default used by ver11. |
| L3 tokens | dump (C,D,H,W,T) → permute(4,1,2,3,0) → (160·frames, C). |
| α_rank | −slope of OLS log λ_k on log k, k ∈ [2, ⌊r/2⌋], r = number of non-zero eigenvalues. |
| α_Clauset | continuous power-law MLE on eigenvalues with KS-chosen xmin and min tail 10 (Clauset, Shalizi & Newman 2009, doi:10.1137/070710111). This is a density exponent. |
| jackknife | leave-one-row-out SE for a single-matrix PR. **A with-replacement row bootstrap inside a PR is forbidden**, because duplicated rows lower the rank. |
| stability interval | paired m-out-of-n subsampling without replacement. The same index sets are used for every representation compared. point = mean Δ over S subsets; SE = sd·√(m/(n−m)); interval = point ± 1.96 SE. The estimand is Δ_m = E[PR_m(A)] − E[PR_m(B)]. |

## 4. Family A — subject level (local CPU, pooled npz)

Parameters (verbatim `src/topic3_spectral/analysis.py::PARAMS`): seed 20261031; iid_reps 1000; colperm_reps 1000; m = 28 of 57, m = 12 of 25; S = 2000; sign-flip B = 9999; bootstrap B = 9999; α bias tolerance 0.15 at rank exponents {0.5, 1, 2}; Holm α 0.05; replication needs ≥ 2 of 3 zoo checkpoints; H4 subsample 160 tokens per frame.

- **E1.** For each of the 7 matrices, at its own n:
  - covPR, corrPR, covPR/(n−1), jackknife SE;
  - iid-Gaussian reference at the same (n, D), with mean and 2.5/97.5%;
  - column-permutation null.
- **D2** "structure beyond independent columns": p_low = (1 + #{null ≤ obs})/(1 + B) < 0.025.
- **A1.** ΔPR_28 for L2−L3, L2−L1 and L1−L0, for covPR and corrPR.
  - **D1:** "L2 > L3 robust" iff the covPR interval lo > 0.
  - "and not a per-channel-scale effect" iff the corrPR interval lo > 0 as well.
  - If covPR passes and corrPR does not, the drop is attributed to per-channel gain, consistent with the final LayerNorm.
  - L2−L1 and L1−L0 compare different D (768 vs 1536, 384 vs 768) and are descriptive only.
- **A1b** (needs the connectome re-pool). Pooled L3 vs pooled per-token LN0(L2) (mean over tokens and frames of LN0(L2 tokens)), on the same 57 rows: ΔPR_28 for corrPR and covPR. This is the subject-level LN-matched contrast. It is descriptive and is replicated in each zoo checkpoint.
- **A2 (cross-model).** All 7 matrices restricted to the 25 NeuroSTORM positions:
  - E1 quantities at n = 25;
  - mean covPR at m = 12 divided by the iid reference at (12, D), as the D-calibration.
  - **D3:** "ordering reproduces" iff the covPR ΔPR_12 interval lo > 0 for both BrainJEPA − BrainLM and NeuroSTORM − BrainLM.
  - Attribution to "self-supervised prediction" is untestable whatever D3 shows, because pooling (CLS / token mean / GAP), D and training data all differ.
- **α at subject level** is NOT reported. Synthetic calibration (`results/topic3/2026-10-31/alpha_calibration_synthetic.json`, written before this card) fails the 0.15 tolerance at every subject-level shape for both estimators. The old α values are shown only as reproduction.

## 5. Family B — token level (connectome, primary layerwise test)

- **Unit.** The subject is the unit. Each subject's 7 frames are concatenated:
  - L2, LN0L2, L3: 1120×1536 (ceiling 1119);
  - L1: 8960×768;
  - L0: 71680×384.
- **Per-subject values.** covPR and corrPR of the concatenated matrix (primary). Per-frame values and the H4 subsampled values are secondary.
- **Primary family (Holm over the two, within each checkpoint).** For each, d_i = log PR(…) − log PR(…).
  - **H1a, blocks effect with the norm matched:** log corrPR(L3) − log corrPR(LN0(L2)).
  - **H1b, total stage-3 effect, replicating the old covariance claim:** log covPR(L3) − log covPR(L2).
- **Test.** Two-sided paired sign-flip permutation on mean d (B = 9999), plus a subject-bootstrap 95% CI of mean d (B = 9999). Resampling subjects is valid here because each subject contributes one scalar.
- **Replication rule (decides the verdict).** An H1 effect **HOLDS** iff:
  - the primary checkpoint has Holm p < 0.05 with its CI excluding 0; and
  - ≥ 2 of the 3 zoo checkpoints show the same sign with Holm p < 0.05.
- **Other outcomes:**
  - "not replicated": the primary is significant but the zoo agreement falls short;
  - "killed": the primary CI includes 0.
- **Secondary (reported, no verdict):**
  - H1c: log corrPR(LN0 L2) − log corrPR(L2), the per-token normalization effect;
  - H1d: log corrPR(L3) − log corrPR(L2);
  - H1e: log covPR(L3) − log covPR(LN0 L2).
- **H4 (descriptive).** L0→L1→L2→L3 profile using 160 tokens subsampled without replacement per frame. The seed is (20261031, position, frame), which removes the token-count dependence. Results are shown as a mean over frames and subjects.
- **α at token level** (descriptive only), by shape according to the synthetic calibration:
  - α_rank and α_Clauset for L0 and L1;
  - α_rank only for L2, LN0L2 and L3, because Clauset fails at 1120×1536.
  - Synthetic rows are iid, whereas real tokens are spatially and temporally correlated, so even "estimable" α carries that caveat.
- **Forbidden:** HTSR regime labels ("critical", "rank collapse", "edge of chaos"), α thresholds, any OOD or transfer score.

## 6. Controls

- **iid reference and column-permutation null** (Family A). These are sanity references: they show whether PR is below what independent columns give. They do not decide any layer claim.
- **Checkpoint replication** (Family B rule): the 3 zoo E192 checkpoints on the same subjects and frames.
- **Random-init control (H2).** Pre-specified but deferred. It needs a torch venv on connectome plus an exact replication of the VRABES extraction preprocessing (`extract_vrabes_swift_E192.sh` and its python entry point). Neither is done in this iteration, so H2 = **untested**. No synthetic input will substitute for it, and no frames leave connectome.

## 7. Old claims and the rule that decides each

| # | Old claim (EMPIRICAL_ANALYSIS_REPORT §3 / empirical_results.json) | Decided by |
|---|---|---|
| J1 | json PR ≈ 1 for every model, "rank collapse" | T3.1 fixture and reproduction (uncentered SVD artefact) |
| R1 | L2 PR "expands 4×" (2.78 → 11.02) | E1 + A1 (L2−L1, descriptive because D differs) + H4 |
| R2 | L3 "collapse" 11.02 → 3.58 **caused by Euclidean PatchMerging** | Mechanism: ver11 code (no merge between layer_2 and layer_3). The drop itself: D1, A1b, H1a/H1b with the replication rule |
| R3 | BrainJEPA / NeuroSTORM PR ≥ 2.7× BrainLM; "self-supervised prediction" explains it | D3 at matched n = 25; attribution untestable |
| R4 | HTSR regime labels from α | Not applicable (§5 forbids them); subject-level α not estimable (§4) |
| R5 | optimal OOD layer / OOD suitability score | Untestable: no transfer data, and the old value is hard-coded |
| R6 | d_B, R_hub, assortativity r of similarity graphs | Out of scope (§8) |
| R7 | SwiFT-LLM NeuroPrior 450-ROI row | Out of scope: its rows are ROIs, not subjects, so it is a different estimand |

## 8. Out of scope

- **Graph metrics (R6).** These were computed on uncentered row cosines whose medians are 0.97–0.9995. Explorer evidence:
  - the top-20% edge sets overlap the centered ones at Jaccard 0.26–0.46;
  - iid noise gives d_B ≈ 4.05, R_hub ≈ 1.83 and r ∈ [−0.12, 0.07];
  - a rank-3 + mean synthetic reproduces the L3 "hub crowding".
  They are reported as unsupported and are not re-estimated.
- **Transfer and OOD claims.**

## 9. Run plan and records

1. `scripts/topic3_subject_level.py` (local) → `family_A_subject_level.json`.
2. `scripts/topic3_token_job.py` on connectome. This is a Slurm array of 4 checkpoints on node1, nice, CPU only; node4 lacks numpy. Outputs go to `token_job/*_token_spectra.npz` and `*_token_job.json`, which are copied back.
3. `scripts/topic3_token_stats.py` (local) → `family_B_token_level.json`.

Each script refuses to run unless this card's sha256 equals `card_sha256.txt`. It records code, input and output hashes, python and numpy versions, and seeds. Raw logs go to `results/topic3/2026-10-31/logs/`. The code hashes at freeze time are in `code_sha256_at_freeze.txt`. GPU-hours: 0.

## 10. Deviations

Any deviation from §2–§9 is recorded in a dated addendum with its reason and both results where applicable. A failed contract check is reported as an execution failure, not as a scientific null.

## 11. Pre-card exposure (real-data quantities already seen in this run before freezing)

- **Surveys 1 and 3, and explorers M2_r1_1 / 2 / 3:**
  - centered covPR of all 7 pooled matrices (as published);
  - old α, including L0 1.4717 and L1 0.9887 (as published);
  - uncentered PR (as in the json).
- **explorer_M2_r1_1:**
  - mean-vector energy fraction 96.4–99.9%;
  - uncentered row-cosine medians 0.97–0.9995 and Jaccard 0.26–0.46 of the top-20% edges vs centered;
  - per-token LN statistics on 2 frames: layer_3 channel std ≈ 1.006, layer_2 0.70–0.92, per-channel offset median 0.535.
- **explorer_M2_r1_2:**
  - re-pool of subject position 0 against npz row 0 (max |Δ| ≤ 3.6e-7);
  - array-byte hashes of one real frame.
  No token PR values.
- **explorer_M2_r1_3:** column-SD quantiles (0.29–7× median) and the range of uncentered cosines [0.79, 0.9999].
- **worker_M2_r1 (this author):**
  - the T3.1 exact reproduction of the public numbers;
  - the mean-energy fraction (0.9645–0.9992).
  No corrPR, subsampling, null, token-level, matched-n or new-α value was computed on real data before freezing.
