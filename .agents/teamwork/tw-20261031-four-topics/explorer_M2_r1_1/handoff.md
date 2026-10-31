# explorer_M2_r1_1 — handoff (Hard). M2 Topic 3 strategy, T3.1–T3.4
Written 2026-10-31 (~17:45 KST). Read-only. No production code. Probes and outputs: /home/juke/git/00IITP-AI/verification/explorer_M2_r1_1/

**Summary.**
- The report numbers come exactly from the centered estimator in `src/empirical_connectome_ablation.py`. All 5 PR values and all 5 α values match at 4 decimal places. Every json PR value equals the uncentered `srg.compute_participation_ratio` output exactly.
- Four new findings change the survey plan:
  1. The old graph metrics (d_B, R_hub, r) are mean-dominated as well. Their inputs are uncentered cosine similarities with medians of 0.97–0.9995.
  2. The percentile subject bootstrap gives misplaced ΔPR intervals (coverage 0.06). Subsampling without replacement is valid.
  3. Both α estimators are biased at N=57 for shallow spectra.
  4. Token-level work must run on connectome, because transfer through the jump host is about 0.2 MB/s.

## Pre-card exposure disclosure (the card author must copy this into the card)
My probes computed these real-data quantities, which were not already public. The card author is therefore not blind to them:
- Centered α by the old estimator: layer 0 = 1.4717, layer 1 = 0.9887. The report shows PR 2.78 for these layers but not their α.
- For all 7 files: the energy fraction of the mean vector, uncentered cosine min/median/p80, and the Jaccard overlap between the uncentered and centered top-20% edge sets (O4).
- For one frame (subject position 0, frame 0) and a second frame (subject position 2, frame 3):
  - per-token channel std CV and absolute std/mean;
  - per-channel mean;
  - mean-token energy fraction.
- I computed no token-level PR or α and no cross-checkpoint values. I computed no matched-N value on real data and no centered-graph d_B, R_hub or r.

## 1. Observation
O1 **Exact provenance** (`probe_m2_provenance.py` → `.out.json`).
- `eca.estimate_powerlaw_alpha` (centered) on the 7 local npz files reproduces the report: L2 11.0202/1.598, L3 3.5786/1.8411, BrainLM 4.3188/1.458, BrainJEPA 11.7851/1.8807, NeuroSTORM 12.507/1.196. PR_match_4dp and alpha_match_4dp are both True for all 5.
- `srg.compute_participation_ratio` (uncentered) equals `empirical_results.json` `analysis_3…participation_ratio_PR` for all 7: 1.0014, 1.005, 1.0743, 1.0327, 1.0028, 1.0581, 1.0102.
- Energy fraction of the mean vector: 0.9992, 0.9973, 0.9645, 0.9832, 0.9985, 0.9721, 0.9948.

O2 **Input facts** (no IDs printed).
- Every npz has keys `['X','ids']`, float32, no non-finite values and no constant columns.
- ids are unique and sorted. The SwiFT L0–L3, BrainLM and BrainJEPA files share the same 57-id list in the same order. NeuroSTORM has 25 ids, all 25 inside the 57 (exact subset).
- sha256 prefixes: L0 ec2970e871b8b060, L1 2730359bfc0bd208, L2 ce55160669f77870, L3 f13ae7ba126bdc5a, BrainLM d0b90e46ec638d5c, BrainJEPA c9c550d73acb599c, NeuroSTORM 3d7b2c9630e773a1. The full hashes are in `.out.json`.
- The connectome copies in `/storage/bigdata/VRABES/05_pooled_embedding/` have identical sha256. connectome also holds a `layer_concat.npz` (1aac3773…).
- Producer: `VRABES/RemissionAnalysis/pool_E192_layersweep.py` (NERSC paths).
  - layers 0–2: `t.mean(dim=0)` over tokens;
  - layer_3: `t.mean(dim=(1,2,3,4))` over (D,H,W,T);
  - then the mean over the subject's frames.
- Extraction: `extract_vrabes_swift_E192.sh` runs the `SwiFT_v2_perlmutter` fork with `simmim_swin4d_ver11`. The checkpoint is `/pscratch/.../NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt` on NERSC.

O3 **Architecture, from the local SwiFT_v2 ver11** (`simmim_swin4d_transformer_ver11.py`).
- `PatchMergingV2.forward` (`:76-88`) = `reduction(norm(x))` with `norm = LayerNorm(8·dim)` (pre-norm, `use_post_norm=False` default `:56`). So the layer_0–2 dumps are raw Linear outputs.
- `forward` for embeddings (`:1402-1412`) applies `self.norm` (`:1095`) only to the last stage, then reshapes to (B,C,D,H,W,T). So layer_3 = stage-3 blocks + final LN, on the same 2³×20 grid.
- Empirical check (`probe_m2_ln_scale.out.json`): per-token channel std is
  - layer_3: 1.00557–1.00617, per-token |mean| ≤ 0.00023;
  - layer_2: 0.70–0.92;
  - layer_0: 0.28–0.72;
  - layer_1: 0.55–0.67.

  layer_3 tokens are therefore LayerNorm outputs whose affine leaves the per-token scale at about 1. The per-channel offset across tokens is still large (median |channel mean| 0.535), so β or γ structure is not excluded.

O4 **Old graph metrics are mean-dominated** (`.out.json` `old_graph_diagnostics`).
- `eca.run_analysis_3` (`:396-404`) builds the graph from the cosine of uncentered rows and keeps the top 20% (80th percentile).
- Uncentered cosine median: L0 0.99954, L1 0.99872, L2 0.96979, L3 0.98941, BrainLM 0.99889, BrainJEPA 0.97409, NeuroSTORM 0.99494.
- Jaccard overlap of the top-20% edge sets, uncentered vs centered: 0.26, 0.38, 0.46, 0.44, 0.36, 0.31, 0.36.

O5 **Token dumps on connectome** (`probe_m2_token_feasibility.out.json`).
- `/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES/`: 57 subject dirs, 399 `frame*.pt`, 8.1 GB, 21,628,616 bytes per file.
- Each file is a dict with layer_0 (10240,384), layer_1 (1280,768), layer_2 (160,1536) and layer_3 (1536,2,2,2,20), all float32.
- Centered rank bounds per window: 384, 768, 159 and 159. An eigendecomposition takes ≤ 0.15 s.
- Transfer of one file through ProxyJump dgx1 took 75 s and 98 s (about 0.2–0.3 MB/s), so the 8.1 GB would take about 8–10 h.
- Zoo `/storage/bigdata/VRABES/04_embedding/swift_zoo_ses-01/`: complete 399-frame sets with the same byte size as E192 exist for HCP_N400_T2400_E192, NewUAH_deepE192_L1e-4 and NewUAH_deepE192_L5e-5. NewUAH_E36 is also complete, at 4.06 MB per file. The sets for E96, NewUAH_E192 and HCP_N800 are incomplete.

O6 **connectome environment**
- System python 3.8, `import torch` → ModuleNotFoundError. `python3 -m venv` works and pip is 20.0.2.
- download.pytorch.org and pypi.org return HTTP 200. CUDA 11.1, 12 and 12.4 are in /usr/local. GPUs are A5000.
- Slurm: node4 idle, node1–2 mix, node3 down. /storage is 97% used, with 17 TB free.
- Raw frames `/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01` hold 57 subject dirs. dgx1: 8 V100 idle, no torch.

O7 **Local environment**: superclaude-env has torch 2.11.0.dev+cu130, numpy 2.3.5 and scipy 1.15.3; 20 CPUs.

O8 **Synthetic estimator properties** (`probe_m2_estimators.out.json`, `probe_m2_subsample_ci.out.json`; synthetic only, seeds 20261031 and 20261101).
- (a) Centered PR depends strongly on N for shallow spectra. For λ_n = n^-1 and D=1536, population PR is 38.1; the sample gives 14.7 at N=25, 22.6 at N=57 and 30.6 at N=160. For a = 1.5 the dependence is small (4.9, 5.2, 5.3; population 5.46). iid reference at the real shapes: 54.0 (57×1536), 52.1 (57×768), 48.8 (57×384), 22.1 (25×288).
- (a') Matched N: subsampling 25 of 57 rows gives 13.99, a fresh 25-row sample gives 13.82, and the full 57 rows give 20.32 (a=1, D=768). Comparing N=25 with N=57 directly inflates PR by about 1.5× before any model difference.
- (b) α estimators:
  - The Clauset MLE on iid Pareto eigenvalues recovers the density exponent. At n=383: 3.014±0.18 (true 3), 2.008±0.08 (2), 1.505±0.04 (1.5).
  - On sample-covariance eigenvalues at N=57 it is biased: 6.85 vs a true 3.0 (a=0.5), 2.45 vs 2.0 (a=1), 1.508 vs 1.5 (a=2).
  - The rank slope over all N−1 eigenvalues is biased as well: 0.30 vs 0.5, 0.76 vs 1.0, 2.11 vs 2.0. At N=160: 0.44, 0.89, 2.12.
- (c) Paired percentile subject bootstrap for ΔPR (N=57, D=768): null FPR 0.02, but coverage under the alternative is 0.06. The bootstrap center is 7.79 against a point estimate of 12.08, because duplicated rows shrink PR (19.55 → 14.72 in one sample).
- (c') m-out-of-n subsampling without replacement (m=28, S=400, sd scaled by sqrt(m/(N−m))) for the m-specific estimand ΔPR_28: null coverage 0.947 (FPR 0.053); alternative coverage 0.96, with the CI excluding 0 in 1.00 of runs.

O9 **Constraints observed**
- `src/spectral_rg_flow_diagnostic.py`, `src/empirical_connectome_ablation.py`, `src/run_all_empirical_experiments.py` and `docs/03_empirical_analysis/empirical_results.json` are all in PROTECTED_HASHES (67 lines).
- `tests/test_pilot_connectome.py:161` scans only `SRC_DIR.glob("*.py")` (non-recursive), so the new `src/topic3_spectral/` package is not scanned.
- Old-suite command (from the 10/30 victory auditor):
  `STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` → 86 passed.

O10 **Old claims to adjudicate** (EMPIRICAL_ANALYSIS_REPORT.md)
- L78–81: the layer-2 "critical expansion" (PR 2.78→11.02, d_B peak 2.80, r < 0 only at L2), and the layer-3 "Euclidean PatchMerging" collapse (PR 3.58, R_hub 4.62, r +0.343).
- L82: BrainJEPA and NeuroSTORM have PR more than 2.7× that of BrainLM and r < 0.
- L120: the L2→3 merging collapse used as the motivation for Topic 2.
- L126–129: the α∈[1.5,2] "critical regime" predicts transfer.
- Code labels: the HTSR regime table and `"optimal_ood_layer_identified": "SwiFT_E192_Layer2"` (srg `:262`).

## 2. Logic Chain
1. O1 → T3.1's "why PR≈1 in the json vs the report" is settled exactly: the report used centered covariance eigenvalues and the json used an uncentered SVD, on inputs whose mean vector holds 96–99.9% of the energy. The fixture needs only a rank-k matrix plus a large offset (survey 2 probe; T3.3).
2. O4 → survey 2's claim that d_B, R_hub and r are "centering-invariant" is wrong in substance. They do not differ between report and json only because both used the same uncentered cosine. With median cosines of 0.97–0.9995, the 80th-percentile graph thresholds tiny residual differences, and centering changes 54–74% of the edges. These columns are old claims that T3.4 must also adjudicate. They cannot carry over as correct.
3. O3 → "layer 3 PatchMerging collapse" (L81, L120) is false in code. L2→L3 is 2 Swin blocks plus the final LN, so any PR change mixes a block effect with an LN effect. The empirical LN signature (per-token std ≈ 1.006) makes a parameter-free per-token LN on layer_2 an approximately fair norm-matched control. The large per-channel offset means it is not exact, and β and γ from the checkpoint would settle it. The checkpoint is on NERSC and was not found locally.
4. O8(a), O8(a'), O2 → subject-level PR is an N-specific between-subject estimand. Cross-model comparison at 57 vs 25 is confounded by about 1.5×, and NeuroSTORM's 25 are an exact subset, so the matched comparison must use those 25 subjects for every model (or subsampling to 25). L82 is untestable as stated and must be re-estimated matched.
5. O8(c), O8(c') → a percentile bootstrap can be used as a sign test but not as an interval. Use m-out-of-n subsampling without replacement and freeze the estimand as ΔPR at m (e.g. 28), S, the seed and the FPC scaling.
6. O8(b) → no α estimator is unbiased at N=57 for shallow spectra. α therefore cannot carry a hypothesis or a threshold. Report it descriptively next to matched-N, matched-D iid and column-permutation references. The HTSR regime labels (rank slope ≠ density exponent; survey 2 O3.5) are dropped. The MLE code fixture uses iid Pareto draws, where recovery is clean. A finite-N bias table is kept as a regression guard and stated as a limitation.
7. O5, O6, O7 → the token-level analysis is the better test of the layerwise hypothesis.
   - It measures within-scan dimensionality, so each subject gives an independent paired Δ and ordinary across-subject inference applies with no rank-shrinkage problem.
   - layer_2 and layer_3 are both 160×1536, so the comparison is shape-matched.
   - It can only run on connectome, because transfer is about 10 h per checkpoint.
   - It needs a project-local CPU torch venv (allowed by C4, internet reachable), launched under Slurm on node4.
   - Three more complete E192 checkpoints give a CPU-only replication across checkpoints.
8. O9 → the old protected modules cannot be edited. "Remove the silent fallback" means the new `src/topic3_spectral` loader must raise on a missing file, with a fixture for it. srg.py is not patched.
9. T3.4's "GPU (B300) only if representations must be regenerated" cannot be used here: regenerating needs VRABES patient frames, which C6 and lab-only storage keep off B300. A random-init control would run on connectome or dgx1 with a GPU torch venv and the SwiFT code. The dumps came from the perlmutter fork, so local-ver11 architecture statements are provisional until that fork is diffed.

## 3. Caveats
- The architecture reading uses the local SwiFT_v2 ver11. The `SwiFT_v2_perlmutter` fork that produced the dumps was not inspected. The O3 LN signature is consistent with the local code but checks only the final norm.
- The LN-scale check covered 2 frames from 2 subjects. LN β and γ were not read; the checkpoint is not on connectome per my `find` at depth 3 in /storage/bigdata/VRABES.
- Throughput was measured twice, over the dgx1 jump. rsync with compression, or a direct route, might be faster; I did not try them.
- The synthetic covariances are Gaussian with power-law spectra. Real representations may have different tails. The bias tables are indicative, not calibration for the real data.
- The m-out-of-n coverage was tested for one D (768), one m (28), R=150. That gives an MC SE of about 0.018 on coverage.
- The frames→npz match (re-pooling frames and comparing to the local X) was NOT done. It needs torch on connectome.
- I did not check whether VRABES governance permits token dumps on DGX-Spark. The plan avoids the question by computing on connectome and returning eigen-spectra only.
- DISPATCH.md contains the dispatch's prompt text verbatim. The embedded raw survey JSON array is left out and referenced; it is identical to the three explorer_survey_* returns held by root.

## 4. Conclusion — recommended strategy for the M2 worker
Paths (PROJECT.md): `src/topic3_spectral/`, `tests/topic3_spectral/`, `scripts/topic3_*`, `results/topic3/2026-10-31/`, `docs/03_empirical_analysis/topic3/`. CPU only. GPU is used only for the optional random-init control, on connectome or dgx1, never B300.

**Step 0, pre-card (T3.1, label-free provenance, already-public numbers only)**
- Write `docs/.../topic3/2026-10-31_topic3_provenance.md` with the following:
  - input sha256 for the 7 npz files (O2) and the connectome copy identity;
  - the producer scripts and the ver11 line references;
  - the exact reproduction of the report table from eca centered, and of the json from srg uncentered (O1);
  - the pre-card exposure list (top of this file plus the survey 1/3 centered PR prints).
- Read npz files in place under hash pins. Do not copy `ids` into the project. If a copy is needed, write X-only plus positional index.

**Step 1, fixtures and estimator package (T3.3) before the card freeze**

`src/topic3_spectral/estimators.py`:
- `centered_pr(X)` via the Gram trick;
- `rank_slope(eigs, lo, hi)`;
- `clauset_mle(x)`;
- `subsample_delta_ci(XA, XB, m, S, seed)`;
- column-permutation and iid (Marchenko–Pastur) references;
- `load_npz(path, expected_sha)`, which raises on a missing file or a hash mismatch and never returns ids.

Tests:
- (i) rank-k (k = 1, 5, 20) + offset 10: centered PR within 10% of k (survey 2 gives 1.0/4.61/15.0); `srg.compute_participation_ratio` < 1.1. The second assertion shows the defect is caught.
- (ii) PR is invariant to row permutation and to the global mean offset.
- (iii) iid Pareto eigenvalues at n=383: MLE mean within 0.05 of 1+1/a for a ∈ {0.5, 1, 2} over ≥ 200 reps; exact power-law eigenvalues give rank slope = a to 1e-8.
- (iv) A finite-N bias guard reproducing O8(b) within MC error. This is a regression check, not an accuracy claim.
- (v) The subsampling CI has null coverage within 0.95 ± 2·MC SE (R ≥ 200). A test asserts that the percentile bootstrap undercovers, which documents why it is not used.
- (vi) A missing or wrong-hash file raises.
- (vii) Output contains no `ids`/`sub-` strings (grep the result json).
- (viii) The layer_3 token reshape `permute(4,1,2,3,0)` gives the (t,d,h,w) order matching the PatchMergingV2 flatten order, tested on a synthetic tensor.

**Step 2, frozen card (T3.2), sha256 recorded before any new real computation**

*Family A, subject-level, re-tests the old estimand (local, 7 npz files)*
- Centered PR and PR/(N−1) for L0–L3, BrainLM, BrainJEPA and NeuroSTORM. Each comes with:
  - iid references at matched N and D;
  - a column-permutation null (each column permuted independently, 1,000 draws, seed fixed);
  - the m=28 subsampling CI.
- A1: ΔPR(L2−L3) at m=28, CI excluding 0. A1 tests the old claim's direction, not "PatchMerging".
- A2: cross-model PR on the 25-subject intersection for every model. This reproduces L82 at matched N. The pooling per model is recorded (BrainLM CLS, BrainJEPA token mean, NeuroSTORM GAP, SwiFT token+frame mean), and the card says the result is confounded by pooling.
- A3: graph metrics. Either recompute d_B, R_hub and r on centered cosine with a stated null (degree-preserving rewiring, 1,000 draws), or declare them out of scope with O4 as the reason. Either way the old graph values are judged "not supported (artifact of uncentered cosine)".
- α is descriptive only: the rank slope over the pre-declared window [2, N−1] and the MLE, each beside matched references. No regimes, no OOD score.

*Family B, token-level (connectome, primary test of the layerwise hypothesis)*
- For each of 57 subjects × 7 windows: centered PR of the layer_0 to layer_3 token matrices, and of a parameter-free per-token LN of layer_2.
- Unit = subject, using the mean over windows.
- H1a (blocks effect): PR(L3) vs PR(LN(L2)).
- H1b (norm effect): PR(LN(L2)) vs PR(L2).
- Paired Wilcoxon or t across 57 subjects, Holm over the H1 family, effect size = median paired Δ with a bootstrap CI over subjects. Here the bootstrap is valid, because the per-subject statistic is computed within subject.
- Layer trajectory L0→L3: compare only after subsampling tokens to 160 rows, or as PR/min(n−1, D), because the bounds are 384/768/159/159.
- Replication: repeat on HCP_N400_T2400_E192, NewUAH_deepE192_L1e-4 and NewUAH_deepE192_L5e-5. A layer effect is "holds" only if its sign agrees in ≥ 3 of 4 checkpoints with each Holm p < 0.05.
- Kill rule: the "layer-2 expansion / layer-3 compression" story is killed if H1a is non-significant, or if its sign is not replicated across checkpoints.

*Family C (optional, time-boxed at 3 h of engineering): random-init ver11 forward pass*
- Same config, seed fixed, on the same VRABES frames, on connectome A5000 (node4) or dgx1 V100.
- It needs a GPU torch venv, the SwiFT code copied per C7, and the extraction windowing from `main_embedding_extraction.py`.
- If the time box is exceeded, record H2 as "untestable in this run" in the addendum.

*Decision table for T3.4.* Each old claim is labelled "holds", "fails", "not supported (artifact)" or "untestable". Expected labels:
- L81/L120 "PatchMerging collapse": fails (architecturally false). The PR change itself is tested by A1/H1a.
- Regime labels and the OOD layer: not supported (category error / hard-coded).
- L126–129 transfer: untestable (no transfer data).
- L78–80 and L82: decided by A1, A2, A3 and H1.

**Step 3, connectome execution for Family B (and the zoo)**
1. `python3 -m venv` in a project-local directory on connectome. Install pinned `torch==2.4.1+cpu` (cp38) and `numpy==1.24.4`, and record `pip freeze` and the wheel sha256.
2. Smoke-test: load 1 frame and print shapes only.
3. Re-pool all 399 frames exactly as `pool_E192_layersweep.py` does. Assert max|Δ| < 1e-5 against the local npz X, row by row, in sorted order. This proves frames→npz provenance and the positional ordering without IDs.
4. Run an sbatch array on node4 with nice. Each task writes per-window eigen-spectra plus PR, keyed by (subject position, window position), to `.npz`. The output contains no IDs and no paths.
5. Pull back only those small files (a few MB) into `results/topic3/2026-10-31/`.
6. Raw logs plus a params hash.

Rough cost: 399 frames × 4 layers × ≤ 0.15 s ≈ 4 min of compute per checkpoint. NFS read is about 8 GB per checkpoint.

**Step 4, run → results → report (T3.4)**
- Results go in `results/topic3/2026-10-31/`. The report is `docs/.../topic3/2026-10-31_topic3_result_report.md`. Any deviation goes in a dated addendum, never into an edit of the card.
- Rerun the old 86 tests, the topic1 tests, the new tests and C1 at the end.

## 5. Verification Method
- Reproduction: `cd /home/juke/git/00IITP-AI/verification/explorer_M2_r1_1 && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 probe_m2_provenance.py`. Expect PR_match_4dp and alpha_match_4dp True ×5, and json_PR == uncentered_srg_PR ×7.
- Synthetic: `probe_m2_estimators.py` (55 s) and `probe_m2_subsample_ci.py` (17 s), with the seeds fixed in the files. Expect O8 values within MC noise.
- Token feasibility (about 100 s each, needs connectome): `probe_m2_token_feasibility.py`, `probe_m2_ln_scale.py`.
- No IDs: `grep -l "sub-" verification/explorer_M2_r1_1/*.json verification/explorer_M2_r1_1/*.log` → no matches (rc 1, observed).
- C1: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` → rc 0, 67 OK (observed).
- Probe sha256 prefixes:
  - probe_m2_provenance.py 9b172664248bd7e3
  - probe_m2_estimators.py 5d6ba16f5258ef4f
  - probe_m2_subsample_ci.py 7f80d0e0fcd03765
  - probe_m2_token_feasibility.py d948b588a4592ac2
  - probe_m2_ln_scale.py 75220be5e7f4f66a
- Invalidation conditions:
  - the perlmutter fork's ver11 differs in where it applies the merge or norm;
  - the re-pooled frames do not match the npz X;
  - the npz hashes change;
  - connectome throughput or venv installation fails, in which case Family B is reported as not run and A1 carries the layer verdict alone.
