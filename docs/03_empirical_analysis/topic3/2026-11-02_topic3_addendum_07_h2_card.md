# Topic 3 addendum 07: the H2 random-init control — frozen hypothesis, protocol, estimators, replication gate and decision rule (2026-11-02)

**Status.** FROZEN when its sha256 is written to `results/topic3/2026-11-02_h2/addendum_07_sha256.txt`. It is written, and frozen, **before any random-init forward pass on real VRABES frames**. Later changes go into a new dated addendum; this file is never edited after freezing.

**Author.** worker_M2H2_r1 (run tw-20261031-four-topics, workflow C).

**Authority.** Card §6 pre-specified H2 but deferred it and gave no decision rule. PI decision 8 (2026-11-01, "H2 실행 (권장)") asks for this addendum to freeze H2's hypothesis, estimator, random-init protocol, comparison and decision rule before any random-init result.

**Relation to the frozen files.** This addendum is additive. The card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report and addenda 01–06 are unchanged, and all their receipts in `results/topic3/2026-10-31/` stay valid. None of the 2026-10-31 verdicts is re-read here. H2 adds new estimands and gives them their own rule.

## 1. Question and mode

**Question.** On the same 57 subjects, the same 7 windows per subject, the same layers (L0, L1, L2, LN0L2, L3) and the same preprocessing, do the card's participation-ratio endpoints of the trained E192 primary checkpoint differ from those of the same network at its default initialization? In particular, are the card's verdict-bearing layer contrasts (the subject-level L2 → L3 drop D1, and the token-level H1a / H1b contrasts) produced by training, or are they already present in an untrained network fed the same input?

**Mode.** PRE-SPECIFIED, not blind. The trained values are known (result report §2–§3). No random-init statistic on real frames has been computed by anyone (exposure list, §10).

## 2. Arms

| Arm | What | Role |
|---|---|---|
| T | The pinned trained values of 2026-10-31: per-subject `cat_covpr` / `cat_corrpr` of `results/topic3/2026-10-31/token_job/E192_primary_token_spectra.npz` (sha256 `be7039eb…cc7a5`); pooled L0–L3 matrices from the pinned npz files (`src/topic3_spectral/io_contract.py::PINNED`) and pooled LN0L2 from that spectra npz (`pooled__LN0L2`). | The trained side of every H2 comparison |
| R0 | The trained checkpoint re-extracted through the replicated pipeline (§3) | Replication gate G (§4) only; reported, never substituted for T |
| R1 … R10 | Random initialization, seeds s = 1, …, 10 (K = 10, fixed; no seed is added, dropped or replaced after results) | The untrained side |

## 3. Pipeline and code identity

**Model code.** The SwiFT_v2 fork that produced the stored dumps, not the local SwiFT_v2 HEAD:
- `simmim_swin4d_transformer_ver11.py`, sha256 `5bc444690490dbbed27b43382c0621b869b80bfa305232273c030b4798752d3b`;
- `patchembedding.py`, sha256 `c889eebb6da13cdc4393a9f1d5d341077c7af5a2e0a28108a3ec2ca5dbab7ca7`.

Both are byte copies of `git -C /home/juke/git/SwiFT_v2 show cd87338:project/module/models/<file>` (the `origin/seungju_perlmutter` tip; the same bytes at commit 63367643, the last commit before the 2026-08-10 extraction that touched the branch). They are vendored under `src/topic3_h2/vendor/swift_cd87338_models/`, and `src/topic3_h2/model.py` verifies both hashes before it builds anything.

**Constructor arguments**, from `VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` (sha256 `b979a682…d8b5`) lines 76–82 through `load_model` of the same commit: `img_size [96, 96, 96, 20]`, `in_chans 1`, `embed_dim 192`, `window_size [4, 4, 4, 10]`, `first_window_size [4, 4, 4, 10]`, `patch_size [6, 6, 6, 1]`, `depths [2, 2, 18, 2]`, `num_heads [6, 12, 24, 48]`, `c_multiplier 2`, `last_layer_full_MSA True`, `to_float True` (precision 32), `drop_rate 0`, `drop_path_rate 0`, `attn_drop_rate 0`, `use_MuTransfer None`, `use_flashattn None`, `use_post_norm None`. The built model must have depths `[2, 2, 18, 2]` (guards the `--depth` / `--depths` abbreviation).

**Preprocessing.** The snapshot `datasets.py` of `VRABES/swift_extraction_code` (VRABES commit 94c2bf4; sha256 `743165743e505707615705763b54f026459c4b09b7ae1c817906534f95da758a`), vendored byte-identical under `src/topic3_h2/vendor/vrabes_snapshot/` and used **unmodified**: class `VRABES`, root `/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01`, all 57 subject directories in sorted order, `sequence_length 20`, `stride_between_seq 1.0`, `stride_within_seq 1`, `input_scaling_method znorm_minback` (global mean / SD from `global_stats.pt`), pad `(2, 3, 0, 0, 2, 3)` with the first-voxel background value and the H-axis centre crop to 96. This gives windows starting at frames 0, 20, …, 120 (7 per subject). DataLoader batch size 1, no shuffling.

**Forward.** `model._forward_hook_embedding(x)` in `eval()` mode under `torch.inference_mode()`, fp32, with `torch.backends.cuda.matmul.allow_tf32 = False` and `torch.backends.cudnn.allow_tf32 = False`. Each window yields `layer_0` (10240, 384), `layer_1` (1280, 768), `layer_2` (160, 1536), `layer_3` (1536, 2, 2, 2, 20) as float32, the stored-dump layout.

**Per-subject statistics.** The frozen `src.topic3_spectral.token_job.subject_summary(frames, position, 20261031)`, imported unchanged. Frames are passed in the order the frozen token job uses, the lexicographic order of the dump names `frame{TR}.pt`: TR 0, 100, 120, 20, 40, 60, 80. (Concatenated PRs do not depend on this order; the H4 subsample seeds do.)

**Trained checkpoint (R0 only).** `/storage/connectome/jubin/260225_newmodel/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt`, sha256 `5fd8a56c83aa074c6ff2783747a49214d261ddb5ce448ec50dc894ac33862355` (hashed in the job). Keys are filtered as in `main_embedding_extraction.py` (skip keys containing `decoder`, `mask_token` or `output_head`; strip the `_forward_module.` and `model.` prefixes) and loaded with `strict=False`. Required: no missing encoder key (every missing key contains `decoder` or `mask_token`), and the unexpected keys are exactly `augment_comp.smooth_kernel`.

**Random initialization (R1–R10).** For seed s: `random.seed(s)`, `numpy.random.seed(s)`, `torch.manual_seed(s)` immediately before `Simmim_RoPE4DSwinTransformer(**arguments above)` is built on the CPU. The weights are those of the constructor's own init code: `self.apply(self._init_weights)` (Linear weights `trunc_normal_` with std 0.02 and bias 0; LayerNorm weight 1 and bias 0), the constructor's LayerScale constants (0.9 / 0.1 / 1.0), its own random-number draws during construction and PyTorch defaults for any other module. No state is loaded. The model is then moved to the GPU in `eval()` mode. The sha256 of each seed's encoder state-dict bytes is recorded; every seed's hash must differ from the others and from the trained encoder hash, and rebuilding with the same seed must give the same hash. Seed s is **not** claimed to be the training run's initial weights, whose init law (muP or not) and seed are unknown. H2 compares the trained network with the extraction constructor's default initialization.

**Deviation from the PL entry point.** A thin driver (`src/topic3_h2/driver.py`) replaces `main_embedding_extraction.py` (PyTorch Lightning 1.9.5, deepspeed, a neptune logger). Its equivalence rests on gate G (§4), which compares every window of the trained re-extraction with the stored dumps element-wise.

## 4. Replication gate G (a hard precondition for any random-init job)

Bitwise identity is not achievable on A5000 / torch 2.4 (the explorer smokes measured a floor of 6.5e-7 to 7.8e-7 relative), so the tolerances are stated now:

| Check | Pass condition |
|---|---|
| G1 element-wise | For all 57 × 7 windows and all 4 layers: rel_fro = ‖a − b‖_F / ‖b‖_F ≤ 1e-5 **and** max\|a − b\| ≤ 1e-4, where a is the R0 output and b the stored dump at `/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES` |
| G2 re-pool | The frozen card §2 check on R0: the connectome npz copies (`/storage/bigdata/VRABES/05_pooled_embedding/pooled_E192_layers`) match their pins, their row order equals the sorted directory order, and every R0 re-pooled L0–L3 vector equals its npz row (allclose atol = rtol = 1e-5) |
| G3 statistics | For all 57 subjects and all 5 variants, R0's `cat_covpr`, `cat_corrpr`, `frame_covpr`, `frame_corrpr`, `sub_covpr` and `sub_corrpr` are within relative 1e-6 of the pinned T values, and `cat_corr_dropped` is equal. The frozen `paired_log_contrast` on R0 gives H1a and H1b the same sign and the same "CI excludes 0" status as T |
| G4 identity | Checkpoint sha256 as above; key hygiene as above; input and stored-dump subject lists equal; 57 subjects × 7 windows; dump shapes as listed |
| G5 negative controls | On subject positions 0, 28 and 56 (7 windows each), three perturbed pipelines must each **fail** G1 in at least one window and layer: (a) every window shifted by +1 frame; (b) the pad value set to 0 instead of the background value; (c) `input_scaling_method none`. A control that passes G1 means the gate does not discriminate, and the gate fails |

**Gate verdict.** PASS iff G1–G5 all hold. The result is written to `results/topic3/2026-11-02_h2/gate/gate_record.json`. The random-init launcher (`scripts/topic3h2_connectome.py submit --arm random`) refuses to run unless this addendum's receipt verifies and that record says PASS. If the gate fails, **H2 = untestable** with the failing counts reported by position; no random-init job runs and nothing is substituted. Trying further code variants would need a new dated addendum written before they are run.

## 5. Endpoints and estimators

Notation. Arms a ∈ {T, 1, …, 10}. x_{a,i}(v, e) is subject i's concatenated token PR for variant v ∈ {L0, L1, L2, LN0L2, L3} and estimator e ∈ {cov, corr} (`cat_covpr`, `cat_corrpr`). P_a(v) is arm a's 57 × D pooled matrix. J is the card's A1 index-set family, `subsample_indices(57, 28, 2000, 20261031 + 100)` (frozen `resampling`), so T's subject-level values equal the pinned Family A ones. PR estimators are the frozen `pr_cov` and `pr_corr(·, 1e-3)`. All resampling functions are the frozen ones (`sign_flip_test`, `subject_bootstrap_ci`, `holm`, `subsample_indices`), imported unchanged; only the arithmetic that combines arms is new (`src/topic3_h2/h2stats.py`).

**Interval types.**
- *Token (subject = unit).* Per-subject value d_i. Point = mean d. p = frozen `sign_flip_test(d, 9999, seed)`. CI95 and CI90 = frozen `subject_bootstrap_ci(d, 9999, seed + 1, level)` at levels 0.95 and 0.90 (same resamples).
- *Subject level (index set = unit).* Per-index-set value g_j, j ∈ J. Point = mean g. SE = sd(g) · √(m / (n − m)) with m = 28, n = 57 (the card §3 stability interval). CI95 = point ± 1.96 SE; CI90 = point ± 1.645 SE. No p-value.

**Per-seed effects.** For every endpoint, e_s is the same point estimate with the seed mean replaced by seed s alone (s = 1, …, 10).

### 5.1 Family C — contrast differences (primary; decides the R2 consequences)

| Id | Card contrast | Per-unit value | δ (= 0.5 × \|pinned trained effect\|) | Test seed |
|---|---|---|---|---|
| C1 | H1a: log corrPR(L3) − log corrPR(LN0L2), token | c_{a,i} = log x_{a,i}(L3, corr) − log x_{a,i}(LN0L2, corr); d_i = c_{T,i} − (1/K) Σ_s c_{s,i} | 0.5 × 0.022750675828012934 = 0.011375337914006467 | 20268031 |
| C2 | H1b: log covPR(L3) − log covPR(L2), token | same with (L3, cov) and (L2, cov) | 0.5 × 0.04467252495320163 = 0.022336262476600815 | 20268041 |
| C3 | D1 cov: Δ28 covPR(L2) − covPR(L3), subject level | Δ_{a,j} = pr_cov(P_a(L2)[j]) − pr_cov(P_a(L3)[j]); g_j = Δ_{T,j} − (1/K) Σ_s Δ_{s,j} | 0.5 × 5.343854531110546 = 2.671927265555273 | — |
| C4 | D1 corr: same with corrPR | same with `pr_corr` | 0.5 × 6.038808669990018 = 3.019404334995009 | — |

The pinned trained effects are read from `results/topic3/2026-10-31/family_B_token_level.json` (`per_checkpoint/E192_primary/primary/*/mean_log_ratio`) and `family_A_subject_level.json` (`results/A1_swift_pairs/L2_minus_L3/{cov,corr}/point`), whose sha256 are pinned in `output_sha256.txt`. The stats script recomputes δ from those files and halts if it differs from the numbers above by more than 1e-12. Holm (frozen `holm`) is applied over {C1, C2}. C3 and C4 have no p-value.

**Why δ = half the trained effect.** H2 asks whether training is needed for the contrast. If the trained-minus-init difference is less than half the trained contrast, most of the contrast is already there at init. If it is more than half, training produces most of it. The value is fixed from known trained numbers, before any random-init number exists.

### 5.2 Family L — levels (verdict-bearing for "trained differs from init at layer v")

- **L-tok(v, e)**, 10 endpoints (5 variants × 2 estimators): d_i = log x_{T,i}(v, e) − (1/K) Σ_s log x_{s,i}(v, e) (log before the seed mean). Holm over the 10. Test seeds 20268131 + 10k for k = 0, …, 9 in the order (L0 cov, L0 corr, L1 cov, L1 corr, L2 cov, L2 corr, LN0L2 cov, LN0L2 corr, L3 cov, L3 corr).
- **L-subj(v, e)**, 10 endpoints: g_j = log PR_e(P_T(v)[j]) − (1/K) Σ_s log PR_e(P_s(v)[j]). No p-value.
- δ_L = log 1.10 = 0.09531017980432493 (a 10% ratio) for all 20.

### 5.3 Secondary (reported, no verdict)

- **R1 context (D-confounded, descriptive whatever it shows).** Subject-level Δ28 of L2 − L1 for cov and corr, T minus seed mean, as in C3.
- **A1b context.** Subject-level Δ28 of L3 − LN0L2 for cov and corr, T minus seed mean.
- **The card's own rules applied to each random arm.** D1 (frozen rule: interval lo > 0) from that arm's A1 L2 − L3 intervals; the frozen `token_level_checkpoint` (seed 20261031) on that arm's per-subject values, i.e. H1a / H1b means, CIs and Holm p, plus the H1c–H1e secondaries and the H4 profile.
- **R0 vs T at subject level.** The maximum relative difference between R0's and T's per-index-set PR values (reported, not a gate condition; G2 already bounds the pooled vectors).
- **E1 per arm** at n = 57: `pr_cov` and `pr_corr` of each pooled matrix.
- **Token α (rank slope only)** per arm and variant: median and quartiles over subjects of the frozen `rank_slope` of `cat_cov_eigs`. Descriptive only, as in card §5; no regime labels.
- **Ceiling.** Every L2 / LN0L2 / L3 token-level H2 statement carries the note that the effective token PR ceiling there is 7 (addendum 03 item 1).

## 6. Decision rule (every endpoint of families C and L)

Inputs: point; CI95 = [lo95, hi95]; CI90 = [lo90, hi90]; p_holm (token endpoints only; a subject-level endpoint has no test, so this condition is treated as met); per-seed effects e_1, …, e_10; δ > 0. All inequalities are strict.

| Label | Condition |
|---|---|
| **TE+** training effect, trained > init | lo95 > δ **and** p_holm < 0.05 **and** min_s e_s > δ |
| **TE−** training effect, trained < init | hi95 < −δ **and** p_holm < 0.05 **and** max_s e_s < −δ |
| **EQ** no training effect (equivalent within ±δ) | lo90 > −δ **and** hi90 < δ **and** max_s \|e_s\| < δ |
| **INC** inconclusive | every other case |

The labels are mutually exclusive: TE+ needs lo95 > δ, which puts lo90 ≥ lo95 > δ, so CI90 is not inside (−δ, δ); TE− likewise. TE+ and TE− cannot both hold. INC is the complement, so every input has exactly one label.

Truth table of the named INC cells (the mirror cells for the negative side are the same with signs reversed):

| CI95 vs δ | p_holm < 0.05 | Seeds | CI90 inside (−δ, δ) | Label |
|---|---|---|---|---|
| lo95 > δ | yes | all e_s > δ | (impossible) | TE+ |
| lo95 > δ | yes | some e_s ≤ δ | (impossible) | INC (seed-inconsistent) |
| lo95 > δ | no | any | (impossible) | INC (not significant after Holm) |
| 0 < lo95 ≤ δ (excludes 0, not δ) | any | all \|e_s\| < δ | yes | EQ (significant but below δ) |
| CI90 inside (−δ, δ) | any | some \|e_s\| ≥ δ | yes | INC (seed spread reaches δ) |
| CI straddles δ or −δ | any | any | no | INC (interval too wide) |
| lo95 ≤ 0 ≤ hi95 and CI90 inside (−δ, δ) | any | all \|e_s\| < δ | yes | EQ |
| point exactly 0, CI90 wider than ±δ | any | any | no | INC |
| lo95 = δ exactly | any | any | no (lo90 ≥ δ) | INC (strict inequality) |

**G8 mapping** (sci-pipeline): TE+ / TE− → keep (the effect needs training); EQ → stop for "training produces it" (the contrast is architecture- and input-borne); INC → inconclusive.

## 7. Consequences fixed in advance (R1–R3)

| Earlier reading (report §4) | H2 outcome | Consequence |
|---|---|---|
| R2, subject-level drop holds (D1) | C3 = TE+ | The L2 → L3 between-subject drop is produced by training (more than half of it is absent at init). |
| | C3 = EQ | The drop is already present in the untrained network on the same input: it is architecture- and input-borne, not learned. The D1 verdict stands as a description of the trained network, but cannot be read as a learned property. |
| | C3 = TE− | Training reduces a larger drop that is present at init. |
| | C3 = INC | Unresolved: the drop's training dependence is not determined. |
| | C4 | The same reading for the per-channel-scale-free (corr) version of the drop. If C3 and C4 disagree, both are reported, and the C4 label governs the "not a per-channel-scale effect" part. |
| R2, token H1a holds (direction L3 higher) | C1 = TE+ / EQ / TE− / INC | The primary checkpoint's +2.3% isotropy increase of the spatial-cell vectors through stage 3 (norm matched) is learned / present at init / larger at init / unresolved. The ceiling of 7 is stated next to it. The replication-rule verdict "H1a holds" is not changed by H2. |
| R2, H1b not replicated | C2 | Reported as context for the primary checkpoint's H1b effect only. It does not change "not replicated". |
| R2, mechanism fails (no PatchMerging between layer_2 and layer_3) | any | Unchanged: it is a code fact, checked again in the fork file (§11). |
| R1, L2 > L1 descriptive only | any | Stays descriptive: the D confound (768 vs 1536) depends on spectrum shape, which a random-init DiD does not remove. The L2 − L1 DiD is reported descriptively. |
| R3, cross-model ordering holds, attribution untestable | any | Unaffected. H2 has no random init of BrainLM, BrainJEPA or NeuroSTORM, so the attribution stays untestable. |
| Family L | per endpoint | States at which layers and estimators the trained network's PR differs from init by more than 10%, is within 10% of it, or is unresolved. |

## 8. Data governance and outputs

- Frames, dumps, pooled vectors and eigenvalue spectra of every arm stay on connectome, in a 0700 node1-local work directory under `/home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/`, and are deleted at the end of each job.
- Returned (copied to `results/topic3/2026-11-02_h2/<arm>/` after an ID scan): per-arm tables of per-subject scalar PRs keyed by position only (the `cat_*`, `frame_*` and `sub_*` scalars and the dropped-column counts); per-index-set PR vectors (2000 values per arm, variant and estimator, each pooling 28 subjects); gate comparison aggregates; seed hashes; run records. No `pooled__*` array, no eigenvalue array, no subject name.
- Nothing is written through `scripts/topic3_common.OUT`, and no `scripts/topic3_*.py` file is rerun in place.
- Every file under `results/topic3/2026-11-02_h2/` must contain zero occurrences of the BIDS subject prefix; the Slurm logs are filtered and scanned before copy-back.

## 9. Compute

connectome node1, Slurm (`-p debug -w node1 --gres=gpu:1`), project-local venv (python 3.8.10, torch 2.4.0+cu121, numpy 1.24.4, einops 0.8.0, monai 1.3.2, plus the snapshot's imports nibabel / pandas / scikit-learn / nilearn), recipe in `scripts/topic3h2_connectome.py::ENV_RECIPE`. Two jobs: the gate job (R0 + negative controls), then one random-init job (all 10 seeds, sharing each window's input read). Every GPU job gets a start and a closing row in `results/gpu_ledger_2026-10-31.md` under flock. The M2-H2 cap is 6 GPU-h; a job that would exceed the remaining cap is not launched. Expected use ≤ 1.5 GPU-h.

## 10. Exposure before this freeze (real-data quantities seen)

- **Explorers M2H2_r1_1/2/3** (Slurm smokes 218004, 218041, 218007): trained-checkpoint re-extraction differences against the stored dumps at subject positions 0, 1, 28 and 56 (rel_fro 6.5e-7 to 7.8e-7; per-subject PR relative differences ≤ 2.7e-8); perturbation magnitudes for TF32 on (about 6e-4), minmax / none scaling (1.4–2.2), a 1-voxel pad shift (0.12–0.36) and a +1 TR shift (6e-4 to 4.6e-3). Random-init forwards on **synthetic** input only (iid N(0, 1) and a time-static synthetic blob); for example token covPR on iid input L0 231–251, L1 363–368, L2 about 132, L3 about 121; on the static blob L2 / L3 covPR 5.8–6.1, corrPR about 6.3. All three explorer handoffs state that no random-init forward on real frames was run.
- **This worker:** no real-data quantity. One CPU probe on the constructor only (attention scale with `use_MuTransfer None` vs `False`: both 32^−0.5).
- The trained values T are known from the 2026-10-31 run (card §11, addendum 03 §7).

## 11. Erratum to the provenance note §2 (text only; the pinned note is not edited)

The provenance note cites `/home/juke/git/SwiFT_v2/.../simmim_swin4d_transformer_ver11.py` (sha256 `de132387…052a`, local HEAD) as the architecture source. The code that produced the stored dumps is the fork file `5bc44469…752d3b` (commit cd87338 / 63367643). The two differ in the encoder forward path: the fork applies the MLP twice per block (lines 799–800, `x = x + drop_path_mlp(mlp(norm2(x)))` followed by the same with `ls_mlp`) and sums the D/H/W RoPE angles (line 328); local HEAD makes both opt-in (`legacy_double_mlp`, `legacy_rope_sum`, default False). The structural facts used by the R2 mechanism verdict hold in the fork file: the last stage has no downsample (line 1048, `downsample=... if (i_layer < self.num_layers - 1) else None`), and `self.norm` (line 1073) is applied only after the last stage in `_forward_hook_embedding`. The R2 mechanism verdict is unchanged.

## 12. Deviations from the card for H2 (recorded before running)

1. **Python stack.** In-job statistics run in the project venv (python 3.8.10, numpy 1.24.4) instead of the system python 3.8 with numpy 1.22.3. The frozen functions are numpy-only; G3 checks that the outputs agree.
2. **No dumps read through the restricted unpickler.** Frames come from the in-memory forward. G1 and G3 on R0 test the equivalence.
3. **Re-pool halt.** The card §2 "re-pooled vector equals npz row" halt applies to R0 only. All other card §2 halts (pins, row order, 7 frames, shapes) apply to every arm.
4. **GPU.** Card §2 says no GPU is used. That line governed the token job; PI decision 8 makes a connectome GPU run part of H2.
5. **Entry point.** A thin driver replaces the PL `main_embedding_extraction.py` (§3).
