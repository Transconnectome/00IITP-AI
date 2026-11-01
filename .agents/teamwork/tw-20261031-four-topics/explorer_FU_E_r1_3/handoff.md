# explorer_FU_E_r1_3 handoff (FU-E, adversarial pre-mortem). Written 2026-11-01 ~15:00Z.

**Summary.** All 15 r1 Stage-1 checkpoints still exist on B300, so option E is testable. Only REST1_LR is staged (no REST2), and no HCP open-access behavioral CSV exists on B300 or in the project. Fingerprinting therefore has to be within-run split-half, and the age probe is untestable unless the PI supplies the open-access CSV.

Two CPU synthetic probes found that the naive split-half fingerprint is invalid under the r1 preprocessing:
- The full-run per-voxel z-score makes the two half means exact negatives of each other. With |r| similarity, pure iid noise is identified at 100 %.
- Subject-specific brain-mask outlines give 94–98 % identification with the readout that does detect planted FC.

Per-half re-z-scoring plus one common mask removes both artifacts, and the planted-FC positive control still passes (100 %). The worker's card must build these in, use a continuous metric (Idiff), not accuracy (accuracy steps are 2.1 % > δ 1 %), and gate on checkpoint provenance.

## 1. Observation

| # | Observation | Source |
|---|---|---|
| O1 | The 15 `model_final.pt` files exist, 156,184,449 B each, in `/scratch/iitp4/worker_M3_r1/runs/hcp_{E,C,S}_s{0..4}/`. ls times 13:10–14:09 node-local (KST) = 04:10–05:09Z, which matches run.json `end_utc` (e.g. hcp_C_s0 04:11:06Z). | ssh .98 at 14:37Z |
| O2 | r1 run.json records **no checkpoint sha256**. It does record `perm_sha256`, `perm_file_sha256` and per-subject `test_num`/`test_den` (16 TEST positions). | results/topic2/2026-11-01/runs/hcp_C_s0/run.json |
| O3 | The checkpoint is `model.state_dict()` (train.py:253-254). π is a **persistent buffer** `layers.0.downsample.perm` (merge.py:27). A strict load of a C-arm state_dict into an identity-built model silently becomes the C arm (probe P2: `perm == C perm: True`). | src/topic2_rgpool/merge.py, train.py; verification/explorer_FU_E_r1_3/probe_hook_equiv.out |
| O4 | `_forward_hook_embedding` final layer equals `forward_encoder(x, zero mask)` exactly (max abs diff 0.0, E and permuted arm). Layers 0..n-2 are returned as (B, L, C) tokens *after* each layer's downsample; the last layer is normed and reshaped to (B, C, d, h, w, t). | vendor ver11 lines 1311-1334, 1383-1415; P2 |
| O5 | HCP on B300 .98: `/scratch/data/hcp/download_HCP_REST1_filtered` has 1084 entries and **103** REST1_LR hp2000_clean files. The only .nii.gz type is REST1_LR: no REST1_RL, no REST2, nothing named REST2 under /scratch/data. The manifest used 93 (88 QC + 5 burned dev), so 10 files are new and never QC'd. .103 has no /scratch/data/hcp. .99 and .101 timed out on ssh. | ssh count-only |
| O6 | No open-access behavioral CSV was found: none on B300 `/scratch/data` (maxdepth 4) and none in the SwiFT repos. SwiFT_v2 code reads `metadata/HCP_1200_precise_age.csv` and `HCP_1200_all.csv`. Precise age is HCP **restricted** data. | grep SwiFT_v2/project/module/utils/data_module.py:165-167 |
| O7 | Preprocessed data: `/scratch/iitp4/worker_M3_r1/hcp/subjects` holds 88 dirs (126 G), **named by the original unsalted content-hash pseudonyms** (the r1 B1 C4 class). Positional token `h%02d` = index in the manifest's sorted subject list (addendum_05 §token map; topic2_c4_sanitize.py docstring), so `sorted(os.listdir(subjects))[i]` ↔ `h%02d`. | ssh; addendum_05 l.26 |
| O8 | r1 `HCPSource(pseudonyms=…)` uses the dir names, and `train.run` writes `rec["test_pseudonyms"] = list(te.pseudonyms)`. Reusing that path with real dir names re-creates B1 in any copied-back record. | train.py:61-69, 236 |
| O9 | Probe P1 (synthetic, tiny_test ver11, random init, 2 seeds, N = 24, 8 windows/half). Its readouts are the final-layer mean over tokens ("pooled"), the spatial map, and the channel×channel correlation across tokens ("cov2"). | verification/explorer_FU_E_r1_3/probe_mask_confound.out |

P1 results:

| condition | pooled acc / \|r\| acc | cov2 acc | cov2 Idiff×100 |
|---|---|---|---|
| A1 subject masks, iid noise, full-run z (r1 recipe) | 0.00 / **1.00** (Idiff −77..−80) | **0.96–0.98** | +9 |
| A2 subject masks, iid noise, per-half z | 0.02–0.10 | **0.94–0.98** | +8..+10 |
| B common mask, iid noise, per-half z | 0.02–0.08 | 0.00–0.08 | ≈0 |
| C common mask, planted subject FC, per-half z | 0.02–0.04 | **1.00** | +47 |

Chance = 0.042. One identification flip in one direction = 0.0208 absolute accuracy.

Further observations:
- **O10.** Receipts:
  - C1 rc 0.
  - code_sha256_at_freeze 33/33 and c4_sanitized 19/19 pass, as does output_sha256_r2 (156 lines checked, 0 not OK).
  - card_sha256 has 2 FAILED lines (manifest, split) and output_sha256 has 16. Those are the 18 lines superseded by design (addendum_05), and c4_sealed_originals (19) verifies only on the sealed root.
  - A naive "all receipts pass" check fails by design. The FU-E worker and verifiers must cite addendum_05.
- **O11.** The existing C4 tests scan only `results/topic2/2026-11-01` and `docs/03_empirical_analysis/topic2` (helpers.py:8-9).
  - test_c4_tokens_r2 fails on any quoted or unquoted 16-hex shape in those docs.
  - test_outputs_no_ids fails on `download_HCP_REST1_filtered/` followed by an alphanumeric character.
  - So the FU-E card placed in docs/…/topic2 can break the C2 suite.
  - A new FU-E results dir is **not** scanned by any existing test.
- **O12.** Ledger: explorer_FU_E_r1_1 (Slurm 407: 15/15 strict-load and perm-buffer match; encoder-only throughput 268 windows/s at batch 16) and explorer_FU_E_r1_2 (re-scores 2 TEST positions vs the recorded num/den) already used Slurm smoke time. Slurm/sacct clocks are KST. I did not verify their outputs and launched no GPU job (0 GPU-h).
- **O13.** sinfo: gpu/interactive/debug partitions on b300-[01-04], with 01 mixed and 02-04 idle at 14:3xZ. ssh through dgx1→connectome ProxyJump often fails with "banner exchange" timeouts; 3 of 7 attempts failed.

## 2. Logic chain
1. O1+O2 → the checkpoints exist, but nothing pins their bytes. Provenance must come from the facts below, measured after the card is frozen:
   - sha256 recorded now, at card freeze;
   - perm buffer hash == run.json `perm_sha256` (O3);
   - re-scoring the 16 TEST positions with the frozen `evaluate_hcp` (eval seed 7002, generator seed 7002·1000003 + test-list position) reproduces run.json `test_num`/`test_den` within a tolerance fixed in the card. This also proves the h-index↔dir map (O7).
2. O3 → arm mislabel is invisible to `load_state_dict`. Per-checkpoint perm-hash checks against the arm's run.json are the only arm-identity guard.
3. O5 → no REST2. Fingerprinting = within-run split-half (same session). This is not Finn-2015 test–retest and is inflated by shared session state. It is a named limitation, and the numbers must not be compared with literature values.
4. O9 A1 → under the full-run z-score, any sign-insensitive similarity (|r|, distance, a learned probe) identifies pure noise perfectly. Signed Pearson gives large negative Idiff. Either way, a naive verdict is driven by normalisation, not representation. → re-z-score each half separately (affine per voxel, so it equals z-scoring the raw halves).
5. O9 A2 vs B → the readout that detects FC identity (cov2) also detects brain-mask outline (r1 mask = mean>0 & sd>0 per subject). → apply one common mask (AND over the 88 subject masks) to every probe input. Report the subject-mask variant as a confound control.
6. O9 C → the first-order pooled readout misses planted FC identity (floor). A pooled primary risks an "inconclusive" floor for every arm. The readout was chosen on synthetic evidence before any real embedding, so a second-order primary is legitimate if the card says so.
7. Accuracy granularity 0.0208 > δ 0.01 → δ cannot be applied to accuracy. Use Idiff (continuous) as the primary, with relative contrast to keep the PI's "δ = 1 % relative" semantics (decision 3). The ratio needs a floor gate on Idiff_E.
8. The encoders barely learned (r1 test NMSE 0.986–1.000). A random-init encoder with the same π is the necessary decomposition: random-init features alone can fingerprint, and π changes what a random network pools. Without it, "C is more identifiable" cannot be attributed to training.
9. O6 → open-access "Age" is binned (22–25/26–30/31–35/36+) and "Gender" is open access, but the file is absent. N held-out = 24. An age probe is untestable and a sex probe would be descriptive at best. A lab copy of precise age is restricted, so using it violates the dispatch.
10. O7+O8+O11 → the main C4 risk is copy-back of dir names, not 6-digit IDs. The fix: a positional symlink view plus an FU-E-specific token scan of its own results/docs/verification/metadata paths.

## 3. Caveats
- The P1 encoder is tiny_test with random init and ±2-voxel ellipsoid jitter at 48³. Real HCP masks (MNI-registered) differ less, and the real encoders are E36 trained. P1 shows that the hazard mechanisms exist, not their size on real data.
- I did not check .99/.101 (ssh timeouts), B300 home or other persistent storage, or whether an open-access CSV exists in the PI's ConnectomeDB account.
- I did not verify the peer explorers' Slurm smoke outputs. The G0 tolerance (bf16 + flash SDP nondeterminism) is still unmeasured by me.
- I did not estimate seed-level SD of Idiff, so power against δ is unknown. "inconclusive" is a plausible honest outcome.
- I printed 3 original content-hash dir names (r1 B1 class) to tool output only once (ls head). I redacted them in the session's task-output file. They were never written to the repo or metadata. Disclosed as an incident.

## 4. Conclusion: recommended FU-E strategy (worker)

**Paths.**
- Code in `src/topic2_fu_e/`; tests in `tests/topic2_fu_e/`; scripts as `scripts/topic2_fu_e_*.py`.
- Card `docs/03_empirical_analysis/topic2/<date>_topic2_fuE_card.md`; results in `results/topic2/<date>_fuE/` (new). On B300: `/scratch/iitp4/worker_FU_E_r1/` (700).
- Import `src/topic2_rgpool` unchanged; nothing new under it (its `code_hashes()` walks that dir).

**Card (F1) contents, frozen with a sha256 receipt in the results dir before any real-data FU-E statistic.**

§0 data seen:
- r1 everything;
- peer explorer smoke tests: random-noise windows and the 2-position re-score;
- P1/P2 synthetic results that chose the readout.

§1 Question: do the r1 C-arm encoders carry more subject-specific information than E (and than S) at matched training?
- This is a different estimand from r1, so the r1 stop verdict stands either way.

§2 Data:
- Only the manifest's 88 subjects. The 10 new files are excluded: never QC'd, dev-exclusion is unverifiable without sealed material.
- Primary set = r1 TEST 16 + VAL 8 = 24 never-trained subjects.
- Secondary (descriptive) = TRAIN 64, seen during SSL.

§3 Input per subject:
- bold_z_fp16 × common mask (AND over the 88 masks);
- halves = TR 0–579 and 620–1199, with a 40-TR gap against autocorrelation leakage, each re-z-scored per voxel;
- 29 non-overlapping 20-TR windows per half.

§4 Readout (primary, fixed):
- final-layer (normed) tokens per window;
- channel×channel Pearson correlation across the 160 tokens, upper triangle, in fp32;
- averaged over windows per half.

§5 Metric:
- R_ij = Pearson(half1_i, half2_j);
- Idiff = 100·(mean diag − mean off-diag).
- Primary contrasts per seed: J1_s = (Idiff_C − Idiff_E)/Idiff_E and J2_s = (Idiff_C − Idiff_S)/Idiff_S.
- Two-sided 95 % t, df 4, paired by seed (r1 machinery `stats.t_interval`). δ = 0.01.

§6 Gates, in order:
- **G0 provenance**:
  - 15 sha256 at freeze;
  - strict load;
  - perm buffer hash == run.json perm_sha256;
  - re-score of all 16 TEST positions within the frozen tolerance.
  - Failure or a missing checkpoint → `no_verdict`. Checkpoints gone → `untestable: checkpoints lost`, because a retrain is 6.5 GPU-h > cap 1.5.
- **G1 synthetic** (CPU tests must pass before launch):
  - A1/A2/B nulls at chance;
  - C planted recovered;
  - verdict truth table.
- **G2 capacity**:
  - Idiff_E,s > the 95th percentile of a 1000-permutation half-2 relabel null for every seed;
  - seed-mean Idiff_E ≥ a frozen floor.
  - Failure → `inconclusive (measurement capacity)` in both card and code.
- **G3 data positive control**: raw 12 mm cell-mean FC Idiff (same halves and mask) > its permutation null. Failure → `inconclusive (data)`.

§7 Verdict, after gates:
- stop: hi(J1) < δ;
- keep: mean J1 ≥ δ ∧ lo(J1) > 0 ∧ lo(J2) > 0;
- modify: mean J1 ≥ δ ∧ lo(J1) > 0 ∧ lo(J2) ≤ 0;
- else inconclusive.

§8 Descriptive, with a reading table and no decision:
- random-init (r1 step-0 weights via `build_simmim(cfg, π_arm,s, seed=s)`) Idiff and J1_rand;
- trained − random per arm;
- identification accuracy;
- layers 0–2;
- pooled readout;
- subject-mask variant (confound size);
- TRAIN-64;
- subject jackknife SE.
- Any bootstrap must exclude copy-of-same-subject pairs from "other".

§9 Age/sex:
- not run, with the reasons (O6, N);
- precise-age or "_all" files are forbidden;
- if the PI supplies the open-access CSV before freeze: sex only, 88 subjects, subject-level stratified CV, descriptive, aggregate output only.

§10 Compute: est. < 0.15 GPU-h. 30 encoders × 24 subj × 58 windows ≈ 42k windows ≈ 3 min at 268 w/s (peer measurement), plus re-score and load. Planned ≤ 0.5 GPU-h, abort at 1.2.

**Implementation hazards to test (F2).**
- Mutant-killing tests:
  - per-half z skipped;
  - common mask skipped;
  - |r| similarity;
  - half-2 order shuffled or misaligned;
  - arm/checkpoint swap (perm hash);
  - test-list position vs h-index in the eval generator seed.
- Verdict code: a missing gate (None) is never a pass; status≠completed or a duplicate (arm, seed) record → no_verdict; the capacity-gate fail → inconclusive, not no_verdict; strict boundaries for every comparison (≥ vs >) with exact-boundary tests; the bias-flag downgrade only where the card says.
- C4:
  - a positional symlink view `view/h00..h87` in the worker's own B300 dir;
  - code never sees or writes dir names;
  - a new scan test for 16-hex shapes, 6-digit ID shapes, `sub-` and the HCP-root path over `results/topic2/<date>_fuE`, the FU-E docs, `verification/worker_FU_E*` and the FU-E metadata;
  - the card text itself must contain no 16-hex shape and no HCP-root path followed by a name (O11).

**Runs (F3).**
- sbatch only (debug or gpu, 1 GPU, `-t` ≤ 60 min), with started/closed ledger rows under flock (sacct KST → UTC).
- One job for G0 + features, so the data are loaded once. Features and aggregates are copied back; embeddings and per-subject matrices stay on B300 or are reduced to aggregates.
- Retry ssh on banner timeout (this is not a run failure).
- Record the 15 checkpoint hashes immediately: /scratch can be wiped.

## 5. Verification method
- `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/explorer_FU_E_r1_3/probe_mask_confound.py` (CPU, about 1–2 min). Expect the P1 table above: A1 \|r\| acc 1.00, A2 cov2 ≥ 0.9, B ≈ chance, C cov2 1.00.
- `… python3 verification/explorer_FU_E_r1_3/probe_hook_equiv.py`. Expect max diff 0.0 and `perm == C perm: True`.
- B300 (count-only): `ls /scratch/iitp4/worker_M3_r1/runs/hcp_*/model_final.pt | wc -l` should be 15; `ls /scratch/data/hcp/download_HCP_REST1_filtered/*/MNINonLinear/Results/ | sort | uniq -c` shows REST1_LR only; `ls /scratch/iitp4/worker_M3_r1/hcp/subjects | wc -l` should be 88.
- C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` rc 0. For the receipts, expect exactly 2+16 superseded FAILED lines (addendum_05).
- Invalidated if: the checkpoints vanish; REST2 or an open-access CSV is later staged (redesign to test–retest / allow a sex probe); or a real-data mask-only control shows a negligible confound (the common mask then costs little but is still harmless).
