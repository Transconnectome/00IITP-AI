# Handoff (Hard): explorer_M2H2_r1_2, milestone M2H2 (Topic 3 random-init control H2)
Written 2026-11-01 ~15:45Z (UTC). Lens: feasibility and failure modes. Recommendations only; no production code written.

**Summary.** H2 is testable within the cap. The VRABES SwiFT E192 extraction can be replicated on connectome to ~1e-6. That requires the perlmutter-commit ver11 (SwiFT_v2 commit `cd87338`, file sha256 prefix `5bc44469`), not local SwiFT_v2 HEAD. A full 57-subject pass costs about 0.06-0.1 GPU-h. The main risks are not compute. They are: (1) silently using the wrong ver11; (2) copying per-subject pooled vectors back from connectome; (3) a decision rule that is trivially "significant" at n = 57; (4) the 8-cell ceiling at L2/L3, which random-init already reaches on synthetic static input.

## 1. Observation

### 1.1 Code reality

**Extraction script.** `/home/juke/git/VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` runs `project/main_embedding_extraction.py` in `/pscratch/sd/s/seungju/SwiFT_v2_perlmutter` (NERSC). Arguments:
- `--model simmim_swin4d_ver11 --embed_dim 192 --depth 2 2 18 2 --num_heads 6 12 24 48 --patch_size 6 6 6 1`
- `--window_size 4 4 4 10 --first_window_size 4 4 4 10 --img_size 96 96 96 20 --c_multiplier 2 --last_layer_full_MSA True`
- `--input_scaling_method znorm_minback --precision 32 --eval_batch_size 1 --seed 1 --load_ds_ckpt_manually`

**Snapshot of the code actually used.** `/home/juke/git/VRABES/swift_extraction_code/` (README: copied from SwiFT_v2_perlmutter/project). It contains:
- `main_embedding_extraction.py`;
- `module/utils/data_preprocess_and_load/datasets.py` (`class VRABES` at line 887, with pad `(2,3,0,0,2,3)` and an H centre-crop);
- the data modules.

It does NOT contain the model (`ver11`) or `pl_classifier_extraction.py`.

**The perlmutter commit.** The perlmutter branch tip is in the local SwiFT_v2 refs: `cd87338ea1597a3056c9cdaa6cd93a3c2db6f784` (`origin/seungju_perlmutter`, 2026-10-19). The EMBARC provenance `/storage/bigdata/EMBARC_new/provenance/git.txt` (connectome) records this same HEAD and marks ver11 as locally modified (`M`) at 2026-10-25. ver11 was last committed on that branch on 2025-12-17 (186871c4). `git show cd87338:project/module/models/simmim_swin4d_transformer_ver11.py | sha256sum` gives `5bc444690490dbbe…`. Local HEAD ver11 gives `de132387…`, the file the provenance note cites.

**cd87338 vs local HEAD ver11** (`diff`, 267 lines):
- cd87338 applies the MLP twice in every block (lines 799-800: `x = x + drop_path_mlp(mlp(norm2(x)))`, then the same with `ls_mlp`). HEAD runs the first call only when `legacy_double_mlp=True`.
- RoPE: cd87338 sums the D/H/W angles. HEAD splits the axes unless `legacy_rope_sum=True`.
- HEAD added these flags in 6061dc6d (2026-10-18, "SwiFT-Reasoner … P0 code audit and fix").

**Random-init behaviour** (CPU probe, synthetic input, same random weights loaded into each model: `verification/explorer_M2H2_r1_2/probes/probe_fixtures_cpu.out.json`, `probe_ver11_localize.out.txt`). Relative Frobenius difference of the layer outputs:
- HEAD with default flags vs cd87338: 0.11 (L0) to 0.68 (L3);
- HEAD with both legacy flags vs cd87338: 3.4e-4 (L0), 1.7e-3, 6.3e-3, 9.3e-3 (L3). The difference starts inside the first block's attention: patch_embed diff = 0, block-0 norm2 input diff 4.4e-3 abs.

**Checkpoint.** `/storage/connectome/jubin/260225_newmodel/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt` (7,260,249,428 B) has sha256 `5fd8a56c83aa074c6ff2783747a49214d261ddb5ce448ec50dc894ac33862355`. The copy at `/storage/bigdata/MDD_treatment_response/migration_20260722/pretrained/…/best.pt` has the same hash.
- Loading it with the extraction's key filter gives 568 encoder tensors loaded, missing 17, unexpected 1. All 17 missing keys are decoder/mask_token (smoke JSON `missing_all_decoder_or_mask: true`). The CPU probe counts 567 encoder keys and 17 decoder/mask keys in the model.
- So the trained extraction has no random-init residue. The NERSC log `/storage/bigdata/EMBARC_new/provenance/run_logs/logs/pla_extract/model_NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4.try1.out` shows the same "loaded 568 | missing=17 unexpected=1".

**Random-init code.** `Simmim_RoPE4DSwinTransformer.__init__` ends with `self.apply(self._init_weights)` (cd87338 lines 1183-1193):
- Linear layers: `trunc_normal_` with std 0.02 and bias 0;
- LayerNorm: weight 1, bias 0;
- LayerScale constants: `ls_t` 0.9, `ls_s` 0.1, `ls_mlp` 1.0;
- `mask_token`: trunc_normal_.

The decoder is built before `apply`, so the RNG stream depends on the constructor arguments. `torch.manual_seed(s)` followed by a CPU build is bitwise reproducible: `rebuild_same_seed` gives 0.0 on all layers. Seed 1 vs seed 2 gives rel 1.40.

**Sizes and speed (CPU).** Encoder: 264,412,320 params. Forward on CPU: 7.3 s per window (2 threads). Dump shapes: layer_0 (10240,384), layer_1 (1280,768), layer_2 (160,1536), layer_3 (1536,2,2,2,20), matching `src/topic3_spectral/token_job.py:18`.

### 1.2 Data and logistics on connectome (all read-only; IDs masked in every command)

**Inputs.** `/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01/img/` holds 57 subjects. A probe on node2 (`probes/probe_bgz_connectome.out.txt`, srun CPU, aggregates only) found:
- 150 frames each, plus `global_stats.pt` with keys global_max / global_mean / global_std / valid_voxels;
- frame_0 is float32 with shape (91,109,91,1);
- background z = −mean/std lies in [−4.63, −2.95]. No subject is above the snapshot's −0.5 `_check_minback_contract`, so nothing raises;
- the first voxel is exactly 0 in 57/57 subjects, so the pad value is the background.

**Stored dumps.** `/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES/<57 dirs>/frame{0,20,…,120}.pt`, 21.6 MB each, mtime 2026-08-10. Pinned pooled npz: `/storage/bigdata/VRABES/05_pooled_embedding/pooled_E192_layers/`.

**Slurm.**
- node1 = 8× RTX A5000 24 GB (driver 550.144, so CUDA ≤ 12.4). node3 (gpu:7) is `down*`. node2/node4 are CPU only.
- `limit_qos` caps a user at gres/gpu = 4 and 25 jobs. The user connectome1 is shared with other agents: 8 M3 jobs were running at 15:30Z.
- GPU jobs need `-w node1` with `--gres=gpu:1`. The submit filter rejects CPU-only jobs on node1/node3 (addendum 01).
- `/home/connectome/connectome1` is node-local (root fs, 910 GB free). `/storage` is NFS at 97% (15 TB free). There is internet access (pypi and download.pytorch.org answer 200).
- System python is 3.8 only. User-level `~/.local/bin/uv` 0.9.8 exists.

**Peer smokes (ledger rows, read only).** explorer_M2H2_r1_1 job 218004: bundle ver11 `5bc44469` reproduces position 0 / window 0 to rel_fro ≤ 7.8e-7 with TF32 off. TF32 on gives about 6e-4. minmax scaling or a 1-voxel shift gives 0.12-2.2. explorer_M2H2_r1_3 is also on record. Neither ran random-init on real data.

### 1.3 My GPU smoke

Slurm job 218041, node1, 1 GPU, ElapsedRaw 74 s, 0.021 GPU-h; ledger rows opened and closed under flock. Venv: torch 2.4.1+cu121, py3.12, monai 1.3.2, numpy 1.26.4 (recipe `verification/explorer_M2H2_r1_2/smoke/build_env_connectome.sh`, about 25 min to build). Output `verification/explorer_M2H2_r1_2/smoke/smoke_218041.json`: 0 occurrences of `sub-`, and the job's .out/.err on connectome also had 0.

Trained checkpoint, positions 1, 28 and 56, 7 windows each (21 frames), through the snapshot `VRABES` Dataset and a DataLoader (4 workers):

| Check | Result |
|---|---|
| Dump vs stored dump, max rel_fro | L0 6.5e-7, L1 7.4e-7, L2 7.7e-7, L3 7.0e-7 |
| Dump vs stored dump, max abs | ≤ 5.1e-6 |
| `allclose(1e-5, 1e-5)` | all 21 frames × 4 layers |
| Frozen `subject_summary` cat_covpr / cat_corrpr vs pinned `E192_primary_token_spectra.npz` | max rel diff 2.7e-8 (all 5 variants) |
| Pooled vectors vs pinned connectome npz rows | max abs 7.0e-7 (the frozen repool check is 1e-5) |
| Time per window | 0.41 s DataLoader wait (NFS-bound) + 0.155 s GPU forward |
| Peak GPU memory | 3.45 GB |
| Checkpoint load | 3.7 s (warm cache) |
| Random init, synthetic iid input only | build 5.7 s on CPU, 0.149 s per window |

### 1.4 Synthetic random-init PR (CPU; `probes/probe_ver11_cpu.out.json`)

Single-window token PR, seeds 1 and 2:

| Input | L0 | L1 | L2 | L3 | Time-variance share |
|---|---|---|---|---|---|
| iid N(0,1), covPR | 232-251 | 364-367 | 131.6-131.7 | 120.4-120.7 | ≈ 0.94 |
| Time-static brain-like blob (background −3), covPR | 1.63-1.64 | 2.91 | 5.84-5.91 | 5.92-6.05 | ~1e-12 |
| Time-static blob, corrPR | — | — | 6.29-6.30 | 6.28-6.36 | — |
| Same blob + iid 0.2 noise in the mask, covPR | — | — | 6.4-6.6 | 6.5-6.7 | ≈ 0.05 |

The iid reference (frozen `resampling.iid_reference`, 3 reps) is 160×1536: 143.95; 1120×1536: 646.98; 1280×768: 479.35; 10240×384: 370.13. Random-init / iid is therefore 0.91 (L2), 0.84 (L3), 0.76 (L1) and 0.63-0.68 (L0).

### 1.5 Frozen pipeline facts

- `scripts/topic3_token_job.py` takes `--frames-root`, `--label`, `--out-dir`, `[--reference-root]` and `[--check-npz-root]`, and does not check the card. It can be reused unmodified on new dumps.
- Its npz output (`pack_summaries`, `src/topic3_spectral/token_job.py:106-120`) contains `pooled__<variant>` arrays (57×D per-subject pooled vectors) and per-subject eigenvalues. The pinned r1 npz in the repo already holds these for the trained primary.
- Frames are read in `sorted(glob('frame*.pt'))` order, which is lexicographic: frame0, frame100, frame120, frame20, …. The H4 subsample seed `(20261031, position, frame index)` depends on that order. Concatenated PRs do not.
- `scripts/topic3_common.py:12` hard-codes the output directory `results/topic3/2026-10-31` (addendum 02 §2).
- Frozen numpy-only functions that are reusable: `analysis.paired_log_contrast`, `analysis.token_level_checkpoint`, `analysis.replication_verdict`, `resampling.paired_subsample_delta`, `resampling.subsample_indices`, `resampling.holm`, `analysis.describe_matrix`.

### 1.6 Integrity checks I ran

- C1 `sha256sum -c PROTECTED_HASHES.txt`: rc 0.
- results/topic3/2026-10-31 `output_sha256.txt` and addendum_02 to addendum_06 receipts: rc 0.
- `card_sha256.txt`: the hash matches. `-c` fails only on the trailing "frozen …" token in that file.
- `code_sha256_at_freeze.txt`: only `scripts/topic3_launch_connectome.py` differs, as documented in addendum 01.

## 2. Logic chain

1. **Code choice.** The stored dumps are reproduced to ≤ 7.8e-7 by cd87338 ver11 (§1.3, at 4 positions across 3 independent smokes). Local HEAD ver11 differs by 3e-4 to 0.7 depending on flags (§1.1). So the "model's own init code" and the replication code must be cd87338's ver11 + patchembedding, imported from `git archive cd87338` (a read-only git operation), not SwiFT_v2 HEAD. If HEAD with legacy flags were used, random-init outputs would come from a different function, about 1e-2 rel at L3, which an O(1) tolerance check would not catch.
2. **No random-init residue in the trained network.** All 567 encoder tensors load from the checkpoint (§1.1), so trained outputs do not depend on the seed. The replication check therefore needs no RNG matching. For random init, `torch.manual_seed(s)` plus a CPU build with fixed constructor arguments is bitwise reproducible (§1.1).
3. **Tolerance.** Measured replication error is ≤ 7.8e-7 rel and ≤ 5.1e-6 abs (§1.3). The smallest code or preprocessing defects measured are HEAD+legacy (3.4e-4 at L0), TF32-on (about 6e-4, peer) and 1e-3 input noise (about 1e-3). A pre-stated tolerance of rel_fro ≤ 1e-5 per frame and layer, plus the frozen repool `allclose(1e-5)`, separates them by ≥ 13× below and ≥ 30× above. Stats level: cat PR rel ≤ 1e-6 (measured 2.7e-8).
4. **Blind spot.** A pure ×1.01 input scaling changes random-init outputs by only 2.7e-6, because PatchEmbed's LayerNorm makes the zero-bias random network nearly scale-invariant. A scale-only perturbation is therefore not a valid must-fail fixture for random init. Use shifts, a background-fill change or a code variant instead (§1.4).
5. **Cost.** A full pass is 399 windows × (0.41 + 0.155) s ≈ 3.8 min with 4 loader workers, I/O-bound. Add the checkpoint load and about 2 min of frozen token job CPU. That is about 0.06-0.1 GPU-h per pass if dumps are written and the token job runs in the same allocation. Replication plus K = 20 seeds is about 1.3-2.1 GPU-h. K = 39 is about 2.5-4 GPU-h. The cap is 6 GPU-h minus about 0.06 already used by the three explorers' smokes.
   - A shared-loader driver (load each window once, forward through k ≤ 10 models per GPU: 3.45 GB activations + about 1.06 GB per model in fp32) reduces K = 40 to under 1 GPU-h.
6. **Data-governance trap.** The frozen token-job npz contains per-subject pooled vectors (§1.5). Copying it back, as r1 did, would break the H2 rule that per-subject representations never leave connectome. Family A for random init needs these pooled 57×D matrices, so it must run on connectome. Only aggregate JSON and per-subject scalar statistics without IDs may come back. Whether per-subject eigenvalue arrays count as "aggregate spectra" is for root to decide (§3).
7. **Ceiling confound.** At L2/L3 the token PR ceiling is 7 (addendum 03 item 1). Random init on a time-static synthetic input already gives covPR 5.8-6.1 and corrPR 6.3 (§1.4), the same range as the trained primary's real medians (report §3: covPR 5.41 / 5.67, corrPR 5.88 / 6.14). A token-level H2 at L2/L3 is therefore expected to be bounded and close.
   - With n = 57 and per-subject log-ratio CIs of about ±0.002 (addendum 03 item 3), any systematic trained-vs-random difference will be "significant". The decision rule needs a pre-stated minimum meaningful effect δ, plus a seed-distribution criterion. Otherwise H2 is trivially "differs".
8. **Replication unit.** Seed-to-seed variation of random-init PR on synthetic input is about 1-2% (L2/L3 covPR) to 12% (L0 corrPR) (§1.4). That is comparable to the H1a effects (2-5%). Seeds are therefore the replicate unit for the random side, as checkpoints were for the trained side (addendum 03 item 3), and K must be large enough for a rank criterion.

## 3. Caveats

- I did not read the peer explorers' handoffs, to keep my work independent. I used only their ledger rows. My smoke tested positions 1, 28 and 56. The full 57×7 replication remains the worker's H2′ gate.
- The perlmutter working tree had uncommitted ver11 changes (`M`, a backup dated 2026-05-30). The extraction ran on 2026-08-10 with them. Three smokes show that cd87338 reproduces the dumps, so any uncommitted change did not touch the encoder forward path on these inputs. This is empirical, not proven from source.
- The checkpoint load time (3.7 s) was measured on a warm page cache. A cold 7.26 GB NFS read may take minutes (adds < 0.05 GPU-h).
- Whether per-subject eigenvalue spectra (57 × ≤1119 per variant) may leave connectome is a governance call. I recommend keeping them on connectome unless root approves, and bringing back only per-subject scalar PRs (positions only) and aggregates.
- The δ and K recommendations below are my proposal. The design explorer may propose a different rule; root and the PI decide. The PI chose δ only for M3 and M4 (decision 3).
- Synthetic random-init PR values (§1.4) are now an exposure: synthetic only, no real data. addendum_07 should list them, and the peers' synthetic and replication numbers, in its exposure log.
- Deep-architecture (2 2 42 4) random init was not probed. Cost is about 2× forward per seed, still I/O-bound.

## 4. Conclusion: recommended strategy for the worker

### Step 0. Paths and identity
- `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07.md`, receipt `results/topic3/2026-11-02_h2/addendum_07_sha256.txt`, outputs `results/topic3/2026-11-02_h2/`.
- New scripts `scripts/topic3_h2_*.py` and `src/topic3_h2/` (new code only). Tests in `tests/topic3_h2/`.
- Never call `scripts/topic3_common.py` output helpers, and never rerun `scripts/topic3_*.py` in place.

### Step 1 (H1′). Freeze addendum_07 before any random-init forward on real data
It must state:

**Hypothesis.** "At the card's layers (L0, L1, L2, LN0L2, L3) and on the same 57 subjects, the trained E192 primary differs from random-init networks of the same architecture" on:
- (a) Family A E1 covPR and corrPR per layer, plus the D1 drop as a difference-in-differences [Δ28(L2−L3)]_trained − [Δ28(L2−L3)]_random, on shared index sets;
- (b) Family B per-subject cat covPR and corrPR per variant, and the H1a/H1b contrasts as trained-minus-random differences.

**Random init.**
- Code: cd87338 ver11 + patchembedding via `git archive cd87338 project/module/models` (sha `5bc44469…`), with the exact constructor arguments of the shell script.
- Build: `torch.manual_seed(s)`, then build on CPU (`self.apply(self._init_weights)`), then move to `.cuda().eval()`.
- Seeds: s = 1…K, with K fixed in the addendum from the replication-run cost (≥ 20; ≥ 40 if the shared-loader driver is used).
- Record the sha256 of each seed's state-dict bytes.

**Estimators.** Frozen `src/topic3_spectral` imported unchanged: `subject_summary` and `pack_summaries` through the unmodified `scripts/topic3_token_job.py`; `paired_log_contrast`, `paired_subsample_delta` and `holm` with the frozen PARAMS and seed 20261031.

**Decision rule** (proposal; per endpoint, Holm within the H2 family). "Training effect" iff all three hold:
- (i) the subject-paired interval for trained − seed-mean random excludes 0;
- (ii) the trained statistic lies outside all K seed statistics (rank p ≤ 2/(K+1));
- (iii) |effect| ≥ δ. The proposed δ is a 10% ratio (|mean log ratio| ≥ log 1.1). Root or the PI must confirm δ before the freeze.

"No training effect" iff the interval lies inside ±δ. Otherwise "inconclusive". At L2/L3, state the ceiling of 7 next to every token-level verdict.

**Exposure log.** Synthetic-only random-init numbers (this handoff, peers); trained replication diffs only.

**Tolerance, stated before Step 3.**
- Dumps: per frame and layer rel_fro ≤ 1e-5 and the frozen repool `allclose(atol=rtol=1e-5)`.
- Statistics: cat PR rel ≤ 1e-6.
- TF32 off (`torch.backends.cuda.matmul.allow_tf32 = torch.backends.cudnn.allow_tf32 = False`).
- `--precision 32` semantics: no autocast.

### Step 2 (H2′ env)
Build the worker's own venv on node1 with the recipe in `verification/explorer_M2H2_r1_2/smoke/build_env_connectome.sh` (copy it into the repo under `scripts/topic3_h2_env/`). Take the snapshot `datasets.py` from `VRABES/swift_extraction_code` and the cd87338 models dir. Do not ship `project/module/__init__.py`, which imports everything; use namespace packages.

### Step 3 (H2′ replication gate; run before any random-init job)
1. The driver (a thin version of the smoke `verification/explorer_M2H2_r1_2/smoke/h2x2_smoke.py`) extracts all 57×7 windows with the trained checkpoint (sha `5fd8a56c…`). It uses the snapshot `VRABES` class with the data-module params and a DataLoader with batch 1 and shuffle False, and writes `frame{TR}.pt` dumps under a node1-local dir (`/home/connectome/connectome1/iitp4_m2h2/worker…/dumps/trained`).
2. Compare every frame with the stored dump.
3. Run the unmodified `scripts/topic3_token_job.py --frames-root <new> --reference-root <stored> --check-npz-root /storage/bigdata/VRABES/05_pooled_embedding/pooled_E192_layers` with `/usr/bin/python3` (3.8, numpy 1.22.3, the original versions) inside the same node1 GPU allocation.
4. Compare its spectra with the pinned `E192_primary_token_spectra.npz` (all arrays, including the H4 sub_* values).

If any check fails: stop and report H2 = untestable with the failing numbers. Do not try further code variants without a dated addendum naming them before they are run.

### Step 4 (random-init runs)
- One Slurm job per seed or per seed block on `-w node1 --gres=gpu:1`, at most 2 concurrent GPUs (the connectome1 QoS of 4 is shared).
- Dumps go to node1-local disk and are deleted after the frozen token job has run on them. Or use a shared-loader in-memory driver, but only after a fixture proves it gives arrays identical to the dump + frozen-script path on the trained run.
- Family A (random-init pooled matrices) and all paired statistics run ON connectome with the frozen numpy functions.
- Copy back only aggregate JSON plus per-subject scalar PRs keyed by position. Never the `pooled__*` arrays. Eigenvalue arrays only if root approves.
- Before every copy-back: `grep -c 'sub-'` = 0 on logs and outputs. The snapshot `VRABES.__getitem__` prints the subject name on NaN/Inf.
- Ledger start and close rows under flock for every job.

### Step 5 (H3′ fixtures and tests)
These must fail on the targeted defect; margins were measured on CPU in `probes/probe_fixtures_cpu.out.json`.
- (a) **Code-identity fixture:** the ver11 used has sha `5bc44469…`, and on fixed synthetic input with fixed random weights its outputs differ from HEAD-default and HEAD-legacy by > 1e-5 rel (measured ≥ 3.4e-4).
- (b) **Replication-check fixture:** the comparison function passes on identical dumps. It fails on dumps from shifted input (1 voxel: 0.32-0.36; 1 TR: 0.21-0.27), a zero background fill (1.1-1.2) or 1e-3 additive noise (about 1e-3). Do NOT use pure input scaling, which gives 2.7e-6 and is invariant.
- (c) **Near-isotropic baseline:** random init on iid N(0,1) synthetic input gives token covPR / iid-reference ≥ 0.8 at L2/L3 and ≥ 0.6 at L0/L1 (measured 0.91 / 0.84 / 0.76 / 0.63).
- (d) **Ceiling fixture:** random init on a time-static synthetic input gives L2/L3 token PR ≤ 7. A wrong token permute or layout should break this.
- (e) **Seed fixture:** same seed gives bitwise-equal state dicts; different seeds differ.
- (f) **Decision-rule fixtures** on synthetic PR tables:
  - planted trained = random × 1.2 in all seeds → "training effect";
  - equal → "no training effect";
  - × 1.03 (< δ) → not "effect";
  - trained inside the seed range → not "effect";
  - Holm boundary.
- (g) **Governance fixture:** the copy-back reducer drops every `pooled__*` key, and the output scan finds 0 `sub-` tokens.
- (h) **Lexicographic frame-order fixture** (H4 parity).

### Step 6 (report)
Write `docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md` with the H2 verdict per endpoint and its consequence for the readings:
- R1 (whether L2 > L1 is a training effect);
- R2 (whether the subject-level L3 drop and the H1a direction are training-induced or architectural/input-driven);
- R3 (a random-init control only for SwiFT: BrainLM/BrainJEPA/NeuroSTORM have no random init here, so D3 attribution stays untestable).

Optional, descriptive only: random init for the 2 2 42 4 architecture vs the 2 deep zoo checkpoints, at K = 5, if budget remains.

## 5. Verification method

- **Replication numbers:** `cat /home/juke/git/00IITP-AI/verification/explorer_M2H2_r1_2/smoke/smoke_218041.json`, and the ledger rows for job 218041 in `/home/juke/git/00IITP-AI/results/gpu_ledger_2026-10-31.md`. On connectome: `sacct -j 218041 -X -o JobID,State,ElapsedRaw`.
- **Code identity:**
  - `git -C /home/juke/git/SwiFT_v2 show cd87338:project/module/models/simmim_swin4d_transformer_ver11.py | sha256sum` gives `5bc44469…`.
  - `diff` against `/home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py` shows the double-MLP hunk at 799.
- **CPU probes (synthetic):**
  ```
  cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/explorer_M2H2_r1_2/probes/probe_fixtures_cpu.py
  ```
  About 3 min. Also `probe_ver11_cpu.py` (about 2 min) and `probe_ver11_localize.py` (about 1 min).
- **Checkpoint hash:** on connectome, `sha256sum /storage/connectome/jubin/260225_newmodel/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt` gives `5fd8a56c…` (run on node2 via srun).
- **Integrity:** `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` (rc 0 at 15:40Z).
- **Invalidation conditions:**
  - the full 57×7 replication exceeds 1e-5 rel at any frame;
  - the connectome inputs or stored dumps change (re-hash);
  - root rules that per-subject scalar PRs may not leave connectome either;
  - a peer shows that cd87338 fails at other positions.

## Workspace state left behind

- Local: `verification/explorer_M2H2_r1_2/` (probes, smoke code/JSON, the cd87338 models archive under `probe_pkg/`, which includes the committed `__pycache__` that ships in that git tree).
- Connectome: `/home/connectome/connectome1/iitp4_m2h2/explorer_M2H2_r1_2/` now holds only `build_env.sh` and `logs/` (36 KB). The venv, python and code bundle were deleted.
- No orphan processes. Total GPU: 0.021 GPU-h (job 218041).
