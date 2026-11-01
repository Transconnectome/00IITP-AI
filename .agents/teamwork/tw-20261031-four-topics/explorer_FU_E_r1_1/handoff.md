# handoff — explorer_FU_E_r1_1 (FU-E, Topic 2 follow-up E; explorer 1 of 3, lens: scientific design / falsifiability)
Written 2026-11-01 ~14:55Z. Type: recommendation (no production code). GPU used: 0.005 GPU-h (Slurm job 407).

**Summary.** FU-E is testable within its cap: all 15 r1 Stage-1 checkpoints exist on B300 b300-01 (=.98), load strictly with the frozen code, and the encoders run at 268 windows/s, so the full plan costs about 0.1–0.3 GPU-h of the 1.5 cap. Cross-session fingerprinting (REST1 vs REST2) is **untestable**: only REST1_LR is staged. The age/sex probe is **underpowered**: only 28 of the 103 staged subjects have open-access labels. The recommended primary outcome is anatomy-controlled **within-run split-half functional identifiability** on the 24 held-out subjects, with r1's C-vs-E / C-vs-S paired-by-seed verdict machinery. At the absolute δ = 0.01 an honest prior expectation is `inconclusive` unless between-seed SD of the contrast is ≤ ~0.005.

## 1. Observation

| # | Observation | Evidence |
|---|---|---|
| O1 | The 15 checkpoints exist: `/scratch/iitp4/worker_M3_r1/runs/hcp_{E,C,S}_s{0..4}/model_final.pt`, 156,184,449 B each, mtimes 13:10–14:09 KST 11-01 | ssh `stat`, 14:23Z; addendum 02 §2 says final weights saved there |
| O2 | Slurm: partitions gpu/interactive/debug, 4 nodes idle. `b300-01` = NodeHostName cloud-S1HDe3 = 61.107.201.98. `/scratch` is a node-local `/dev/md0` ext4 (28 T), so jobs needing checkpoints/data must use `-w b300-01` | `sinfo`, `scontrol show node`, `df`/`mount` |
| O3 | HCP staged at `/scratch/data/hcp/download_HCP_REST1_filtered`: 1084 dirs; REST1_LR present for **103**; REST1_RL, REST2_LR, REST2_RL = **0** | count-only ls glob |
| O4 | r1 preprocessed data: `/scratch/iitp4/worker_M3_r1/hcp/subjects/` 88 dirs (126 G) with `bold_z_fp16.npy`, `mask.npy`, `cellmeans.npy`; split at `/scratch/iitp4/worker_M3_r1/code/split.json` (original tokens) | ssh ls (counts/filenames only) |
| O5 | r1 venv `/scratch/iitp4/worker_M3_r1/venv`: torch 2.15.0+cu134, numpy 2.5.4, scipy 1.18.1, **no sklearn** | ssh python import |
| O6 | No behavioral CSV on B300. Locally the only HCP open-access behavioral file is `/home/juke/data/veritas-class/week05-connectivity/hcp-fc/unrestricted_behav_data_n337.csv` (sha256 prefix f64a692fc1f8ad9d; identical copy under `.../cpm_tutorial_337/source/`), 337 **unrelated** subjects, columns incl. Subject, Release, Acquisition, Gender, Age (banded); no restricted columns (no Age_in_Yrs, Family/Mother/Father ID, handedness, race) | header grep; DataDictionary says Age = banded, Age_in_Yrs separate |
| O7 | In-memory join on B300 (IDs streamed via stdin, nothing written): 337/337 labelled subjects have a dir, but only **28** of the 103 REST1_LR subjects are labelled (13 M / 15 F; age 22–25: 4, 26–30: 12, 31–35: 12). Whether they fall in TRAIN/VAL/TEST was not computed (it needs content hashing of the NIfTI files) | output of my ssh probe, masked |
| O8 | Smoke, Slurm job 407 (debug, b300-01, 1 GPU, 15 s, COMPLETED, ledger rows 14:41:10Z / 14:41:13–28Z, 0.005 GPU-h). It read no subject data. 15/15 checkpoints `load_state_dict(strict=True)` into `build_simmim(E36_d2262, perm, seed=s)`; one persistent buffer `layers.0.downsample.perm` per checkpoint and it equals `perms_hcp.npz[E|C|S_seed{s}]`; 284/308 float tensors differ from the seed-s init (also for the stalled S_s2). Per-checkpoint sha256 values are recorded in `verification/explorer_FU_E_r1_1/smoke_out.json` (e.g. hcp_E_s0 e6705307…a635, hcp_C_s0 1fdf0ea9…d4e4, hcp_S_s2 44cd1a14…0f8d) | `smoke_out.json`, `smoke_slurm407.log` |
| O9 | `forward_encoder(x.permute(0,1,5,2,3,4), mask.permute(0,4,1,2,3))` with zero mask gives (B, 288, 2, 2, 2, 20). The mean over frames is 2304-d. Throughput is 268 windows/s at batch 16 (bf16 autocast, flash SDP), with 7.9 GB peak, the same for trained and init. A per-voxel circular shift of a (600, 78, 96, 84) tensor costs 0.026 s and preserves each voxel's values | `smoke_out.json` S2/S3; vendored ver11 lines 1311–1334, 1362–1380 |
| O10 | Copied code on B300 equals `code_sha256_at_freeze.txt` (14 src files + perms_hcp.npz: 15/15 OK). The repo freeze receipt passes 33/33 under `LC_ALL=C` (the Korean locale prints "성공", not "OK") | `sha256sum -c` |
| O11 | Synthetic design probe (`verification/explorer_FU_E_r1_1/probe_design_sim.py`, `.out.json`, seed 0, N = 24, p = 2304): (a) null Idiff 0.0003 ± 0.0043; top-1 accuracy saturates at 0.97 at moderate signal while Idiff keeps rising (0.022/0.081/0.261); (b) an anatomy-only component gives Idiff 0.26 and top-1 = 1.00 in BOTH real and shuffled inputs, and Idiff_real − Idiff_shuf = 0.0005 ± 0.005 (null) vs 0.047 with a planted functional part; (c) for 5 seeds and r1's t rule at δ = 0.01 with true contrast 0, P(stop) = 1.00/0.91/0.57/0.41/0.14 for seed SD 0.002/0.005/0.008/0.010/0.020; (d) AUC sampling SD 0.105/0.088/0.073/0.050 at N = 24/34/50/98 | `probe_design_sim.out.json` |
| O12 | The r1 verdict code has defect classes (record `orchestrator/M3_r2_gate_record.json`, challenger_M3_r2_2): V07 missing F+ gate counted as pass; V08/V10 failed runs counted; V06 F− also downgrading modify; V01–V05 ≥ vs >; V09 subject-order assertion; case A (F+ fail → script says no_verdict, card says inconclusive). In `scripts/topic2_verdict.py`, `fm is not False` treats a missing F− gate as a pass | gate record; verdict script lines ~62–64 |

## 2. Logic chain

1. O1 + O8: the "checkpoints lost" branch does not apply today. The checkpoints are on volatile node-local /scratch (O2) and could vanish on a VM stop. The card must therefore pin the 15 sha256 values (O8) and add a rule: if any pinned checkpoint is missing or mismatched at run time → `untestable: checkpoints lost`. Retraining would cost 15 × 0.43 ≈ 6.5 GPU-h, which exceeds the 1.5 cap (O-r1 report §7), so retraining is not an FU-E option.
2. O3: the dispatch requires REST1 vs REST2 for fingerprinting, and no second session is staged. Cross-session fingerprinting is therefore untestable on the staged data, and the card must say so. The available label-free identity measure is **within-run split-half identifiability**: TRs 0–599 vs 600–1199, 30 non-overlapping 20-TR windows per half. It must be named as such, not as "fingerprinting" in the trait sense: within-run halves share session state, the full-run z-scoring and the mask.
3. O11(b): any encoder sees each subject's own brain mask as background zeros. Identity can then be read from anatomy alone, giving top-1 = 1.0 in both real and shuffled inputs. A raw identifiability number would measure head shape. The primary must therefore be **functional identifiability** F = Idiff(real) − Idiff(surrogate). The surrogate is a per-voxel random circular time shift within each half, which keeps the mask, every voxel's marginal and its autocorrelation and destroys cross-voxel covariance (O9 S3, cheap). The same surrogate input feeds every encoder, so arms are paired.
4. O11(a): top-1 accuracy is ceiling-prone, while Idiff is continuous and its null is centred at 0. Idiff is the primary statistic and top-1 is descriptive.
5. δ: decision 3 gives "1 % / 0.01", and F1 needs δ = 1 %. A relative δ on F is unusable, because F_E may be near 0 and the ratio then explodes. Idiff is conventionally reported ×100 in %, so **δ = 0.01 absolute Idiff (1 Idiff point)** satisfies "1 % / 0.01". The card must state this mapping explicitly and report relative values beside it.
6. O7 + O11(d): with 28 labelled subjects, scattered over TRAIN/VAL/TEST, the AUC SD is ≈ 0.09–0.10 ≫ δ = 0.01. Even 98 subjects with the full OA CSV give SD ≈ 0.05 > δ. An age probe is weaker still: 22–37-year bands, 4/12/12 counts. The age/sex probe therefore cannot carry a verdict; the card declares it `untestable at δ: labels for 28/103 subjects` and either omits it or runs it as frozen descriptive only. "fingerprinting and/or age probe" (§7) permits identifiability alone.
7. The unit of inference is the training seed, as in r1, so r1's machinery transfers directly: P1_s = F_C,s − F_E,s (practical; mirrors I1) and P2_s = F_C,s − F_S,s (connectome-specific; mirrors I2), each with a two-sided 95 % t interval (df 4) over seeds paired by seed. The subject set and surrogate are fixed, so subject sampling is shared across arms.
8. O11(c): `stop` is likely at true 0 only if between-seed SD(P1) ≲ 0.005; at SD ≥ 0.01 `inconclusive` is the modal outcome. The card must state this expected-power statement before any result, so that an `inconclusive` cannot later be read as a surprise or as evidence for C.
9. Held-out subjects: the 24 TEST + VAL subjects of the r1 split. The encoders never trained on them, and VAL served only as a health check, with no selection (card §4). TRAIN subjects are excluded from the primary because SimMIM saw their exact windows (memorisation confound). The 5 burned dev subjects stay excluded. The 10 subjects staged after the r1 manifest (O3: 103 − 93) are optional. Adding them gives N = 34 and cuts subject-sampling SD by √(24/34) ≈ 0.84. The price is preprocessing with the frozen script into the worker's own dir, new positional tokens and an ID scan. Decide before freeze.
10. Identification has no learned parameters. The only fitted step is feature z-scoring across the held-out set's own 2N half-embeddings, applied equally to both halves, so there is nothing to cross-validate (dispatch: "probes cross-validated at subject level"). Any learned secondary probe (labels) must use subject-level K-fold with every fit (z-scoring, λ) inside folds.
11. Capacity gate: r1 G6 required a positive control that can show the pipeline can detect the effect. Here that is a synthetic F+ fixture through the **trained** encoders. Subjects share ONE common ellipsoid mask (`fixtures.ellipsoid_mask`), so no anatomy is present. Each synthetic subject has its own planted network structure (`fixtures.plant_networks(seed = subject)`), stable across halves, with independent latent time series per half, so identity sits in FC structure only. The matching F−: identical network labels for every subject, but subject-specific masks (radius jitter), so only anatomy is present. If the trained E encoders cannot reach F ≥ 2δ on F+, a real-data null is uninformative and the verdict is `inconclusive (measurement capacity)`.
12. O12: the verdict code must use tri-state gates (True/False/None, where None is never a pass) and count only `completed` extractions. Boundaries must be exactly as written (`hi < δ` strict, `mean ≥ δ`, `lo > 0` strict). The F− scope must match the card in both directions. A gate failure maps to `inconclusive` and a software failure to `no_verdict`. Gates are applied before `stop`.
13. Cost (O9): primary = 30 encoders (15 trained + 15 init) × 24 subjects × 60 windows × 2 (real + surrogate) = 86,400 windows ≈ 5.4 min. Capacity gate = 15 trained × 2 fixtures × 24 × 60 × 2 = 86,400 ≈ 5.4 min. Adding data loading (24 × 1.5 GB from NVMe) and overhead gives ≈ 0.25 GPU-h; with a ×2 safety margin, ≤ 0.5 GPU-h of the 1.5 cap. One GPU on b300-01 is enough.

## 3. Caveats
- I did not compute any real-data embedding statistic, by design: it would contaminate the card. The only real-data facts seen are counts: 103/88/28, sex 13/15, age-band counts. The card's §0 disclosure must list them.
- It is unknown how the 28 labelled subjects split over TRAIN/VAL/TEST, and whether any of them is burned.
- Within-run split-half identifiability is not trait fingerprinting. Shared full-run z-scoring, scanner/session state and slow drift inflate it equally for every arm, and the surrogate cancels only the per-voxel-marginal, autocorrelation and mask parts.
- The circular-shift surrogate keeps each voxel's spectrum, so it removes only cross-voxel (FC) identity. An encoder could still identify subjects from voxel-wise spectra, and that part is counted as "anatomy/nuisance". The card should state this definition.
- The extraction uses mask = 0 (no SimMIM masking), which is a distribution shift from training (60 % masked). This is a design choice to freeze, not a defect.
- The stalled `hcp_S_s2` (r1 addendum 04) stays a valid run, as in r1. The card must pre-declare the without-seed-2 sensitivity as secondary.
- The synthetic power probe uses a Gaussian toy model. It measures subject-sampling noise only and says nothing about real between-seed variance, so it is an expectation, not a forecast of the result.
- The B300 two-hop proxy is flaky: several ssh calls timed out at banner exchange. Every remote step needs retries and a sacct check before resubmitting, to avoid double submission.
- I used the r1 venv read-only. It has no sklearn; label probes, if run, can be done in numpy/scipy (closed-form ridge / L2-logistic via scipy.optimize) or in a new project-local venv under /scratch/iitp4/<worker>.

## 4. Conclusion — recommended FU-E strategy (card skeleton the worker should freeze)

**Card** `docs/03_empirical_analysis/topic2/<date>_topic2_FU_E_card.md`, receipt `results/topic2/<date>_FU_E/card_sha256.txt` (card + pinned inputs: the 15 checkpoint sha256 values from O8, perms_hcp.npz, original split sha c13b5f21…, frozen-code receipt, the worker's new code files). Freeze it before any real-data embedding is computed.

- **§0 Disclosure:** the r1 results; this explorer's counts (O3, O7) and smoke (O8/O9); no real-data embedding seen by anyone.
- **§1 Question:** do the frozen r1 Stage-1 encoders of arm C carry more anatomy-controlled subject-specific functional information than arm E (P1, practical) and arm S (P2, connectome-specific)? The measure is within-run split-half identifiability on 24 held-out HCP-YA subjects. The manipulated factor is unchanged (r1 M0 grouping); FU-E changes the outcome only. Unit = training seed (5), paired.
- **§2 Encoders:** 15 pinned checkpoints, loaded strictly into `build_simmim(CONFIGS["E36_d2262"], perms_hcp[key], seed=s)`, with an assertion that the perm buffer equals the key. Init control: the same call without loading, i.e. bit-identical step-0 weights (`tests/topic2_rgpool/test_model_pairing.py`).
- **§3 Data and features:**
  - Data: r1 preprocessed REST1_LR, read-only, on b300-01. Held-out = r1 TEST 16 + VAL 8, in split order (optional pre-freeze extension: +10 new subjects).
  - Halves h1 = TR 0–599 and h2 = TR 600–1199; 30 non-overlapping 20-TR windows each.
  - Embedding: `forward_encoder` with zero mask, bf16 autocast, flash on, eval, no_grad; mean over the 20 frames, then over the 30 windows; 2304-d per half.
  - Surrogate: per-voxel circular shift within each half, offsets drawn from a CPU `torch.Generator` seeded by 9000 + 100·position + half. The surrogate is identical for every encoder, and its sha256 is recorded per subject-half.
- **§4 Statistic:**
  - Features z-scored across the 2N half-embeddings, then each row standardised; R = A·Bᵀ/p.
  - Idiff = mean diag(R) − mean off-diag(R), averaged over both directions where asymmetric.
  - F = Idiff_real − Idiff_surr. Top-1 (both directions) is descriptive.
- **§5 Gates** (synthetic; must pass before real data governs a decision):
  - G-A CPU tests. **F+**: trained E encoders, seed mean F_E ≥ 0.02 and t lower bound > 0. Fail → **inconclusive (measurement capacity)** and no real-data primary is computed (code must not return no_verdict here — r1 case A).
  - **F−**: |seed-mean P1| < δ and each arm |F| < δ. Fail → a would-be keep **and** modify become inconclusive (bias flag). State both in the card and test both directions so neither the V06 mutant nor its inverse survives.
  - Use 2–3 planted strengths (G6 "multiple points").
- **§6 Verdict, in this order:**
  1. All 15 pinned checkpoints present and matching; otherwise `untestable: checkpoints lost`.
  2. All 30 real-data extractions + gate extractions `completed` and finite; otherwise one rerun, then `no_verdict`.
  3. F+ gate: True required; False → inconclusive; None → no_verdict if caused by a software failure, otherwise inconclusive.
  4. **stop** iff hi(P1) < δ (kill criterion).
  5. **keep** iff mean P1 ≥ δ, lo(P1) > 0 and lo(P2) > 0.
  6. **modify** iff mean P1 ≥ δ, lo(P1) > 0 and lo(P2) ≤ 0.
  7. Otherwise **inconclusive**.
  8. F− fail downgrades keep/modify.
  - δ = 0.01 absolute Idiff, with relative values reported.
  - Pre-declared expectation: stop needs between-seed SD(P1) ≲ 0.005; otherwise inconclusive is likely.
- **§7 Secondary (no decision):**
  - T1: training value, F_arm(trained) − F_arm(init) per seed, t interval.
  - T2: without-seed-2 sensitivity.
  - T3: hierarchical bootstrap (seeds, then subjects). Duplicate-aware Idiff: pairs of copies of the same original subject are excluded from "other" and are not counted as self-matches.
  - T4: raw 12 mm cell-FC split-half Idiff baseline (CPU, `cellmeans.npy`).
  - T5: Idiff_real, Idiff_surr and top-1 per arm.
- **Label probe:** `untestable at δ (labels for 28/103 staged subjects; AUC SD ≈ 0.1 ≫ 0.01)`. Optional descriptive sex AUC only if frozen with subject-level stratified 5-fold × 20 repeats, fold seeds shared across arms, all fitting inside folds, and a brain-volume baseline. Labels come only from the OA n337 file (or a PI-supplied full OA unrestricted CSV); the join happens in memory on B300; only aggregates leave B300.
- **§8 Compute:** a single sbatch on `-p gpu -w b300-01 --gres=gpu:1`, time limit ≤ 60 min (reservation ≤ 1.0 GPU-h ≤ cap 1.5), ledger rows under flock, outputs under `/scratch/iitp4/<FU-E worker>/` only. Read-only use of `/scratch/iitp4/worker_M3_r1/{runs,hcp,code/split.json,venv}`.
- **C4:** per-subject rows are keyed only by position within the r1 TEST/VAL lists. No pseudonym, path or ID is printed or written. ID scan before copy-back.

**Tests the worker should write** (CPU, tiny_test config; `tests/topic2_FU_E/` or the worker's own path):
- Extraction shape, determinism, no_grad/eval, zero mask; init equals `build_simmim(seed)`; perm-buffer-vs-key assert, including an S_seed{s} swap mutant.
- Surrogate: marginals and autocorrelation preserved; planted cross-voxel correlation 0.8 → |r| < 0.05; identical across arms.
- Idiff: hand-computed 3×3 value; null ≈ 0; monotone in planted strength; anatomy-only fixture gives F ≈ 0 with top-1 = 1.
- Bootstrap duplicate handling.
- Sign of P1 (C − E) and absolute-vs-relative δ.
- Verdict mutants V01–V11 analogues plus case A, each killed by a named test, and an all-arms-same-subject-order assertion.

**What it adds to r1:** r1 = stop on NMSE at δ 1 %. FU-E `stop` → the M0 grouping also gives no downstream identifiability value; r1 is strengthened. `keep`/`modify` → the grouping changes representation content despite equal NMSE, reported as a new card result, never as a re-reading of r1. `inconclusive` → the downstream question stays open at this N and seed count.

## 5. Verification method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` (rc 0) and `grep -v '^#' results/topic2/2026-11-01/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c` (33 OK).
- Reproduce the synthetic probe: `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_E_r1_1/probe_design_sim.py 0`; it must reproduce `probe_design_sim.out.json` exactly (numpy default_rng seed 0).
- Re-run checkpoint existence/sha: Slurm job with `verification/explorer_FU_E_r1_1/smoke_ckpt_encoder.py` (see `smoke.sbatch`); compare the sha256 values with `smoke_out.json`. Invalidation: any mismatch or a missing file → the card's "checkpoints lost" branch.
- Staging check: count-only `ls .../download_HCP_REST1_filtered/*/MNINonLinear/Results/rfMRI_REST2_LR/*.nii.gz | wc -l`. A non-zero count invalidates conclusion 2 (cross-session fingerprinting becomes possible).
- Ledger: `grep explorer_FU_E_r1_1 results/gpu_ledger_2026-10-31.md` → one started + one completed row, 0.005 GPU-h, Slurm job 407.
