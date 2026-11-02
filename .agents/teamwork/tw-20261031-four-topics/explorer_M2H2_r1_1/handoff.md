# Handoff — explorer_M2H2_r1_1 (M2H2, Topic 3 random-init control H2), 2026-11-01T15:25Z

**Summary.** H2 is testable within the 6 GPU-h connectome cap. A 0.02 GPU-h Slurm smoke (job 218004) showed that the connectome extraction bundle's ver11 code plus the VRABES preprocessing reproduces a stored trained E192 frame dump to rel. Frobenius error 6.5e-7 to 7.7e-7 on all four layers (float32 round-off; not bitwise). The local `/home/juke/git/SwiFT_v2` ver11 that the frozen provenance note describes does NOT reproduce it (rel. error 0.05 to 1.1). So the worker must use the bundle code. It must also pre-state a 1e-5 tolerance with TF32 off, not a bitwise criterion.

## 1. Observation

O1. **Inputs on connectome** (single-level `ls` only, names redacted):
- `/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01/img/`: 57 subject dirs, each with 150 `frame_k.pt` and a `global_stats.pt`.
- `/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES/`: 57 dirs with 7 dumps each (`frame0,20,…,120.pt`, about 21.6 MB, dated Aug 10).
- The sorted input and dump subject lists are equal (smoke: `subject_lists_equal: true`).

O2. **Checkpoint.** `labfind` found `/storage/connectome/jubin/260225_newmodel/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt` (7,260,249,428 B, sha256 `5fd8a56c83aa074c6ff2783747a49214d261ddb5ce448ec50dc894ac33862355`). A second listed copy under `/scratch/connectome/stellasybae/…` is not reachable from node1.
- A torch-free probe (`verification/explorer_M2H2_r1_1/probes/ckpt_keys_probe.{py,out}`) found a flat dict of 585 tensors, all prefixed `_forward_module.model.`. After the extraction's decoder/mask_token/output_head skip, 568 encoder tensors remain. The dict includes the attention-mask buffers.

O3. **Code copies.**
- `extract_vrabes_swift_E192.sh` ran at NERSC with `/pscratch/sd/s/seungju/SwiFT_v2_perlmutter`, which is not available.
- `/home/juke/git/VRABES/swift_extraction_code/` (commit 94c2bf4, 2026-10-18) holds the dataset/data-module/entry-point snapshot but no models. Its `datasets.py` was modified on 2026-10-17 (`_check_minback_contract`, after the Aug-10 extraction). The VRABES pad/crop is at lines 908-919.
- labfind found `/storage/connectome/swift_v2_extraction_bundle/project/` (ver11 sha `5bc44469…752d3b`, `main_embedding_extraction.py` sha `43627486…222e`, `pl_classifier_extraction.py`, `load_model.py`). The bundle has no VRABES dataset class.
- Local `/home/juke/git/SwiFT_v2/…/simmim_swin4d_transformer_ver11.py` has sha `de132387…052a`, the file the frozen provenance note §2 used.

O4. **diff local vs bundle ver11**, in the encoder path:
- 3D RoPE: local splits frequency pairs across the D/H/W axes by default (`legacy_rope_sum=False`); the bundle sums the axis angles.
- Block MLP: the bundle has two residual MLP updates per block (`x = x + mlp(norm2(x))` and then `x = x + ls_mlp(mlp(norm2(x)))`, bundle lines 799-800). Local runs the first one only under `legacy_double_mlp=True` (default False).
- No merge in the last stage: the same in both (bundle line 1048 `downsample=… if (i_layer < self.num_layers - 1) else None`). The hook applies `self.norm` only after the last stage (bundle lines 1437-1444).

O5. **Venv.** Built on connectome node1, `/home/connectome/connectome1/iitp4_m2h2/explorer_M2H2_r1_1/venv`. It is node-local, under the explorer's own dir; the connectome user is connectome1.
- Stack: python3.8 venv, torch 2.4.0+cu121, numpy 1.24.4, einops 0.8.0, monai 1.3.2.
- Built in about 4 min (detached, 15:01Z to 15:05Z).
- Freeze in `verification/explorer_M2H2_r1_1/probes/venv_freeze_connectome.txt`.

O6. **Smoke**, Slurm job 218004: debug partition, `-w node1`, 1 RTX A5000, COMPLETED, ElapsedRaw 66 s, 0.02 GPU-h, ledgered with start and closing rows.
- Driver: `verification/explorer_M2H2_r1_1/probes/smoke_replicate.py`. Shipped bytes: `probes/ship_sha256.txt`.
- Output: `probes/smoke_out_218004.json`. Log: `probes/smoke_218004.log.txt` (names redacted).
- Inputs: subject position 0, window 0. Preprocessing = znorm_minback then pad (2,3,0,0,2,3) then center-crop dim3, as in the snapshot. Checkpoint loaded as in `main_embedding_extraction.py` 286-319.

| variant | layer_0 | layer_1 | layer_2 | layer_3 | allclose(1e-5) |
|---|---|---|---|---|---|
| bundle ver11, TF32 off | 6.5e-7 | 7.4e-7 | 7.7e-7 | 6.8e-7 | yes, all 4 |
| local ver11, default RoPE | 5.0e-2 | 2.9e-1 | 6.1e-1 | 1.10 | no |
| local ver11, legacy_rope_sum=True | 5.0e-2 | 2.9e-1 | 5.9e-1 | 1.05 | no |
| bundle, TF32 on | 5.0e-4 | 6.1e-4 | 6.0e-4 | 5.9e-4 | no |
| bundle, minmax scaling (perturbed) | 2.15 | 1.38 | 1.44 | 1.51 | no |
| bundle, pad shifted 1 voxel (perturbed) | 0.18 | 0.14 | 0.13 | 0.12 | no |

Cells are the relative Frobenius error against the stored trained dump.
- **Bundle, TF32 off:** per-frame covPR and corrPR relative differences ≤ 2e-8, pooled-vector differences ≤ 3e-7.
- **Checkpoint load:** missing encoder keys 0 (17 missing keys in total; the encoder filter leaves none) and 1 unexpected key, whose name was not recorded.
- **Cost:** forward 0.13-0.27 s per window, peak 3.43 GB, checkpoint read 7.8 s.

O7. **Random init on synthetic iid N(0,1) input only.** One window; bundle ver11 constructor under `torch.manual_seed(1)`, no checkpoint. Token covPR per layer:

| layer | shape | random-init covPR | iid reference (n−1)D/(n−1+D) | ratio |
|---|---|---|---|---|
| L0 | 10240×384 | 232.1 | 370.1 | 0.63 |
| L1 | 1280×768 | 363.2 | 479.9 | 0.76 |
| L2 | 160×1536 | 132.0 | 144.1 | 0.92 |
| L3 | 160×1536 | 121.0 | 144.1 | 0.84 |

- The iid reference formula was checked locally with the frozen `pr_cov` at all four shapes plus 1120×1536 (Monte-Carlo means 144.0 / 479.4 / 370.1 / 647.1 vs formula 144.1 / 479.9 / 370.1 / 647.4).
- **No real-data random-init quantity was computed by this explorer.**

O8. **Card and code facts the design must respect:**
- Card §6 defers H2 and gives no decision rule. PI decision 8 requires a dated addendum that freezes H2 before any random-init result.
- The frozen functions are `src/topic3_spectral/token_job.subject_summary/pack_summaries`, `estimators.pr_cov/pr_corr/layernorm0/layer3_tokens`, `resampling.subsample_indices/paired_subsample_delta/sign_flip_test/subject_bootstrap_ci/holm`, and `analysis.paired_log_contrast`.
- The token job's card §2 halt "re-pooled vector equals npz row" cannot apply to random-init arms.
- `scripts/topic3_common.py:12` hard-codes `results/topic3/2026-10-31` (addendum 02 §2), so the H2 scripts must not reuse it for output.

O9. **Environment.**
- Slurm GRES: node1 `gpu:rtx:8`; node3 is down. CPU-only jobs go to node2/node4 (addendum 01). Home directories are node-local.
- `/storage` is 97% full (15 TB free). Internet works on node1 (pypi, download.pytorch.org).

O10. **Checks.**
- C1: `LC_ALL=C sha256sum -c …/sentinel/PROTECTED_HASHES.txt`: 0 non-OK lines.
- All `results/topic3/2026-10-31/*_sha256.txt` receipts OK.
- Layout lint (`audit_layout.py` on the run metadata root): `findings: []`.
- ID scan of my dirs: only the placeholder `sub-XX` and the word "sub-sequences" remain, in copied third-party code. One copied file containing a public-dataset example label was deleted after hashing (`probes/bundle_copy_manifest_sha256.txt`). Smoke JSON: 0 hits.

## 2. Logic chain

L1. From O3, O4 and O6, the code that produced the stored trained dumps is, to float32 round-off, the bundle's ver11 forward plus the snapshot's VRABES preprocessing. The local SwiFT_v2 ver11 is a different network (double MLP plus summed RoPE are missing). The frozen provenance §2 cites the local file, so a dated erratum is needed. The structural facts the R2 verdict uses still hold in the bundle: no merge before stage 3, final LN only after stage 3, 1536-d on the same grid (O4).

L2. Bitwise replication is not achievable: the A5000/torch 2.4 numerics differ from NERSC (O6, `bitwise: false`). The observed floor is about 8e-7, so a tolerance of 1e-5 has about 13× margin. It still rejects TF32 (6e-4), a 1-voxel shift (0.12) and a wrong scaling (1.4) by at least 60×. The replication check can therefore be pre-stated now with evidence, and it discriminates by more than four orders of magnitude.

L3. H2 must be defined as trained vs default initialization of the same constructor (O2, O8). The training run's own initial weights are unrecoverable, and its init scheme (muP or not) is unknown. Seeds are just seeds of `self.apply(self._init_weights)` (trunc-normal std 0.02 for Linear, LN 1/0; PyTorch defaults elsewhere; constructor layer-scale values).

L4. The scientifically load-bearing question is whether the card's verdict-bearing layer contrasts need training. Those contrasts are D1 (subject-level L2−L3, cov and corr) and H1a/H1b (token level). So the primary H2 statistic is a difference-in-differences: the trained contrast minus the seed-averaged random-init contrast, on the same subjects, windows and index sets. Per-layer PR levels (trained vs random) are secondary and decide nothing. A rule must allow three outcomes (training-dependent / architecture-explained / inconclusive), with an equivalence margin fixed now from the pinned trained effects (known values, so δ is a number, not a choice made after seeing random-init results).

L5. From O6 and O9, one full arm is 399 windows: about 108 s of forward plus I/O, plus in-job CPU summaries. That is about 0.2-0.35 GPU-h, so R0 plus 5 seeds plus one synthetic arm comes to about 2.5 GPU-h at the upper estimate, under the 6 GPU-h cap. Memory (3.4 GB) is no constraint.

L6. From O7, a random-init ver11 on iid input is high-dimensional but not isotropic: 0.63-0.92 of the iid reference. A fixture asserting "≈ isotropic" would be wrong. A fixture asserting "> 0.5× the iid reference at every layer, and ≥ 10× the trained real-data token PR" is defensible. That still needs no real-data random-init number.

L7. Card §2 halts must be kept for R0 (npz pins, order, 7 frames, shapes, re-pool = npz rows) and for the random arms, minus the re-pool equality. The frozen functions are imported, not edited. New code is limited to I/O, a DiD statistic and verdict mapping, each with fixtures.

## 3. Caveats

- Only one subject × one window was replicated. Full replication across 57×7 windows is the worker's gate. The input frames could differ for other subjects (e.g. reprocessing).
- The name of the 1 unexpected checkpoint key was not recorded. The worker must log it and show it is not an encoder weight.
- I did not run the PL `main_embedding_extraction.py` path: it needs PL 1.9.5, deepspeed and a neptune logger. The recommended minimal driver bypasses the PL wrapper. Its equivalence rests on the element-wise replication gate, not on code identity. Record this as a deviation in addendum 07.
- Card §2's "connectome token job with system python3.8 + numpy" becomes "the venv's python3.8 + numpy 1.24.4" for in-stream summaries. The frozen functions are py3.8/numpy-only, so this should not matter, but G-R3 checks it anyway.
- δ = 0.5×|trained effect| is my recommendation. It is a choice (0.25 would be stricter, with more inconclusive outcomes), and it must be frozen before the random-init results.
- The zoo checkpoints are not covered. The deep `2 2 42 4` checkpoints have a different architecture. HCP_N400 has the primary's architecture, but its extraction args were not verified.
- My explorer venv (5.0 GB) remains in connectome1's node1 home. Deleting it is safe; the recipe is in O5.
- I did not read the other M2H2 explorers' reports. The worker must check whether any of them computed real-data random-init quantities, which would have to be logged as exposure.

## 4. Conclusion: recommended worker strategy

**H1′ — freeze `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07.md` first.** Put its sha256 in `results/topic3/2026-11-02_h2/addendum_07_sha256.txt` before any random-init forward on real data. Content:

1. **Hypothesis H2.** The verdict-bearing layer contrasts of trained E192 (primary checkpoint) differ from those of the same architecture at its default initialization, on the same 57 subjects × 7 windows (start frames 0..120, stride 20), same layers (L0, L1, L2, LN0(L2), L3) and same preprocessing. Mode: PRE-SPECIFIED, not blind (the trained values are known).
2. **Arms.**
   - T: pinned trained values, i.e. the `token_job/*primary*` npz and the 57-row pooled npz.
   - R0: re-extracted trained values, used for the gate and as a sensitivity arm.
   - R1..R5: random init, seeds k = 1..5.
   - Code: bundle ver11 `Simmim_RoPE4DSwinTransformer`, copied into the project at its sha `5bc44469…`, together with `patchembedding.py` (`c889eebb…`). Args verbatim from `extract_vrabes_swift_E192.sh` lines 76-82 (`img_size 96 96 96 20`, `embed_dim 192`, `depth 2 2 18 2`, `heads 6 12 24 48`, `patch 6 6 6 1`, `window 4 4 4 10`, `c_multiplier 2`, `last_layer_full_MSA True`, precision 32, so `to_float=True`, drop rates 0).
   - Init: `random.seed(k)`, `np.random.seed(k)`, `torch.manual_seed(k)` and `torch.cuda.manual_seed_all(k)` immediately before construction; no checkpoint load; `eval()`; `no_grad`; `torch.backends.cuda.matmul.allow_tf32 = torch.backends.cudnn.allow_tf32 = False`.
   - Do not claim that seed 1 equals the trained run's initial weights.
3. **Estimators.** Only the frozen functions, imported (`subject_summary`, `pack_summaries`, `pr_cov`, `pr_corr`, `layernorm0`, `layer3_tokens`, `subsample_indices` with seed 20261031, m=28, S=2000, `sign_flip_test` B=9999, `subject_bootstrap_ci` B=9999, `holm`).
4. **Primary endpoints** (seed-averaged random term).
   - **Token family, Holm over 2.**
     - Hypotheses:
       - DiD-H1a_i = [log corrPR(L3) − log corrPR(LN0L2)]_T,i − mean_k[…]_Rk,i;
       - DiD-H1b_i = [log covPR(L3) − log covPR(L2)]_T,i − mean_k[…]_Rk,i.
     - Test: two-sided sign-flip on mean DiD, with a subject-bootstrap 95% CI and a 90% CI for equivalence.
   - **Subject-level D1.** DiD_A1 = mean over the same 2000 index sets of [(PR_T(L2) − PR_T(L3)) − mean_k (PR_Rk(L2) − PR_Rk(L3))], computed separately for covPR and corrPR. Interval = point ± 1.96·sd·√(m/(n−m)) (card §3 formula) for 95%, and ± 1.645·… for 90%.
5. **Decision rule** (per endpoint; the card's labels mapped to G8 in brackets):
   - **"training-dependent" [keep]** iff all of:
     - the 95% CI excludes 0 (strict inequality);
     - for token endpoints, Holm p < 0.05;
     - all 5 seed-wise DiD point estimates have the pooled sign.
     For D1, report "training-dependent and not per-channel-scale" only if both cov and corr qualify.
   - **"architecture-explained" [stop for the learned-pattern reading]** iff the 90% CI lies strictly inside ±δ, with δ = 0.5×|pinned trained effect|. Fix the numbers in the addendum from the pinned files: H1a primary mean log ratio +0.023 gives δ ≈ 0.0115; H1b +0.045 gives δ ≈ 0.0225; D1 cov +5.34 gives 2.67; D1 corr +6.04 gives 3.02. Copy exact values from `family_B_token_level.json` / `family_A_subject_level.json`, not from this note.
   - **"inconclusive"** otherwise, including the seed-sign rule failing.
6. **Secondary, reported, no verdict.**
   - Per-layer token log PR (cov, corr) for T vs random (Holm over 10, descriptive).
   - Subject-level per-layer PR_28 for T vs each Rk.
   - The card's own rules applied to each random arm alone (D1 interval, H1a/H1b sign-flip): does the architecture alone show the pattern?
   - The L1→L2 profile, T vs random, labelled D-confounded (the D bias depends on spectrum shape, so random init does not remove it).
   - Random-init cat_corr_dropped counts. If > 10% of the channels of a variant are dead, that endpoint is "not estimable".
7. **Consequences, fixed in advance.**
   - **R2.** The subject-level drop gets "training-dependent" or "architecture-explained (+input)" from D1-DiD. The token-level H1a reading gets the same from H1a-DiD. The mechanism verdict (no PatchMerging) is unchanged.
   - **R1.** Stays descriptive: the random-init profile is shown beside it, with no verdict.
   - **R3.** Unaffected: a random-init SwiFT does not bear on the BrainLM/BrainJEPA/NeuroSTORM ordering, and the attribution stays untestable.
   - **J1, R4–R7.** Unaffected.
   - **H2 row of report §4.** "untested" is replaced by the H2 verdicts, in a new dated result report. Frozen files are not edited.
8. **Replication gate G-R** (pre-stated; it must pass for R0 before any Rk runs; if it fails, H2 = UNTESTABLE with evidence and no substitute):
   - **G-R1.** Every one of 57×7×4 tensors has rel Frobenius error ≤ 1e-5 and max|Δ| ≤ 1e-4 against the stored dump (computed in-stream on node1).
   - **G-R2.** The R0 re-pooled 57×D matrices match the pinned npz rows (allclose 1e-5).
   - **G-R3.** The R0 `subject_summary` cat_covpr and cat_corrpr for all 5 variants are within rel 1e-6 of the pinned token_job npz. The Family B primary H1a/H1b means are within 1e-5, with identical verdicts.
   - **G-R4.** Checkpoint sha `5fd8a56c…`, 0 missing encoder keys, the unexpected key named, and freshly constructed attention-mask buffers equal to the checkpoint buffers bitwise.
   - Also pin the input-frame bytes: hash the 57×150 inputs on connectome and keep only the hash of the manifest.
9. **Provenance erratum.** The dumps were produced by the bundle-equivalent ver11 (double MLP, summed RoPE), not by the local de132387 file. The R2 structural facts still hold.
10. **Exposure list.**
    - This explorer's smoke: the trained replication numbers and random-init PR on iid noise only (O7).
    - Any other M2H2 explorer's quantities.
    - A statement that no real-data random-init quantity exists before the freeze.

**H2′ — execution.**
- Env: project-local python3.8 venv on connectome node1 (`-w node1`, because home is node-local; or put it under `/storage/connectome/connectome1/…`). Keep the recipe as a repo script (pins as in O5).
- Driver: a minimal script that imports the copied bundle ver11 and reimplements the snapshot's `load_sequence`, `scale_input(znorm_minback)` and `VRABES.__getitem__` verbatim. These must be unit-tested against the snapshot code on synthetic volumes.
- Each arm is one Slurm job (1 GPU) that runs, per subject, 7 windows, then the frozen `subject_summary` in-stream, and writes only position-keyed npz/json. R0 additionally compares in-stream with the stored dumps.
- No new frame dumps need to be written. If dumps are written for audit, they stay on connectome.
- Order: R0 → gate → R1..R5 (one job array) → copy back aggregates only to `results/topic3/2026-11-02_h2/` → local CPU stats script (card-hash and addendum_07-hash check, own output dir).
- Ledger start and closing rows for every job. Stop if the projected total exceeds 6 GPU-h; the expected total is about 1.5-2.5.

**H3′ — tests and fixtures** (in `tests/topic3_h2/`; each must fail on its targeted defect):
1. Replication comparator: accepts identical inputs and ±1e-7 noise; rejects 1e-3 noise, a swapped layer key, a 1-voxel pad shift, minmax scaling and TF32-sized (6e-4) noise on synthetic frames.
2. Preprocessing: a marker voxel on a synthetic 91×109×91×20 volume lands at the expected (96³) coordinate; the znorm formula; the background fill equals the first voxel.
3. Init: same seed gives bitwise-equal weights; different seeds differ; Linear weights are trunc-normal(0, 0.02) (KS test) and LN weights are (1, 0); the random-arm path never calls the checkpoint loader.
4. Random-network baseline: on iid input, a random Gaussian map has covPR equal to the independent iid formula (±2%). The random-init ver11 on iid noise gives > 0.5× the iid reference per layer (GPU, synthetic; O7 shows 0.63-0.92).
5. DiD statistic: planted shifts are recovered; on null synthetic arms the FPR is within Monte-Carlo error of 0.05; the equivalence branch fires on a zero shift with small noise; one opposite-sign seed blocks "training-dependent".
6. Verdict-path mutation tests: strict vs non-strict inequalities, Holm vs raw p, CI orientation, arm order (T − R vs R − T), averaging seeds before vs after the log ratio, δ values pinned to the addendum, 95% vs 90% CI used in the wrong branch, and primary-checkpoint selection by label.
7. C4 scan of every new output and doc: no BIDS prefix followed by alphanumerics, and no 6-digit HCP-like IDs.

## 5. Verification method

- Re-run the smoke (≤ 0.05 GPU-h, ledgered): `sbatch` `verification/explorer_M2H2_r1_1/ship/smoke.sbatch` on connectome, after copying `ship/` to an owned dir and adapting `R=`. Compare against `probes/smoke_out_218004.json`. Bundle TF32-off rel_fro should be ≤ 1e-6 on all layers; the local-ver11 rows should be ≥ 1e-2.
- `ssh connectome sha256sum /storage/connectome/swift_v2_extraction_bundle/project/module/models/simmim_swin4d_transformer_ver11.py` gives `5bc44469…`. The local file gives `de132387…`.
- `diff /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py verification/explorer_M2H2_r1_1/copied/bundle_ver11/simmim_swin4d_transformer_ver11.py` (RoPE at 306-330, MLP at 808-810 vs 799-800).
- `sha256sum` of `best.pt` on connectome gives `5fd8a56c…` (about 30 s on NFS).
- Ledger: the two `explorer_M2H2_r1_1` rows in `results/gpu_ledger_2026-10-31.md`; `sacct -j 218004`.
- **Invalidation conditions:**
  - full 57×7 replication fails G-R1;
  - the unexpected checkpoint key turns out to be an encoder weight;
  - a real-data random-init quantity was computed before the addendum_07 freeze, which changes the mode from pre-specified to exposed and must be disclosed.
