# Handoff (Hard) — explorer_FU_E_r1_2, milestone FU_E (Topic 2 follow-up E), lens: feasibility and failure modes

**Summary.** FU-E can be run. All 15 r1 Stage-1 checkpoints exist on b300-01, and the frozen evaluation path reproduces their recorded per-subject test terms exactly. Embedding costs about 0.004 s per 20-TR window per model, so the full plan needs ≤ 0.6 GPU-h (cap 1.5). Three limits change the design:
- B300 holds **REST1_LR only**, so cross-session fingerprinting cannot be tested.
- Open-access age/sex labels exist for **only 28** of the staged subjects, and ≤ 11 of those are held out from encoder training. A powered age/sex probe is therefore not possible.
- The checkpoints were trained on the 64 TRAIN subjects' full runs, so a fingerprint on TRAIN subjects measures memorisation.

Recommended primary: within-session split-half fingerprinting with a temporal gap, on the 34 subjects that no encoder saw. Verdict rules and gates mirror the r1 card, δ = 0.01 absolute on top-1 accuracy. Age/sex is declared untestable (labels), with an optional descriptive probe only.

GPU used by me: 0.010 GPU-h (Slurm jobs 412 = 0.003, failed in my own probe code; 420 = 0.007). Both are ledgered with start and completed rows. The B300 dir /scratch/iitp4/explorer_FU_E_r1_2 has been removed, no job of mine is queued, there were no git writes and no installs.

## 1. Observation

**O1. r1 checkpoints exist and are intact.**
- B300 b300-01 (61.107.201.98) holds `/scratch/iitp4/worker_M3_r1/runs/hcp_{E,C,S}_s{0..4}/model_final.pt`: 15 files, 156,184,449 B each, mtimes 2026-11-01 13:10–14:09 KST.
- Waves 3–4 passed `--save-model` (`verification/worker_M3_r1/wave3_jobs.json`, `wave4_jobs.json`; `src/topic2_rgpool/train.py:253-254`).
- Slurm job 420 (`verification/explorer_FU_E_r1_2/b300/fue2_smoke.out.json`, sha256 52d571a4…9782):
  - every checkpoint has 309 tensors and one buffer `layers.0.downsample.perm`;
  - perm buffer sha256 == run.json `perm_sha256` for 15/15;
  - status completed for 15/15.
- The 15 file sha256 values agree 15/15 with explorer_FU_E_r1_1's independent smoke (`verification/explorer_FU_E_r1_1/smoke_out.json`).

**O2. Reproduction anchor.**
- The frozen `train.evaluate_hcp` (eval mask seed 7002) re-scored TEST positions 0 and 1 for hcp_E_s0 and hcp_C_s0.
- Relative error vs recorded `test_num` / `test_den` = 0.0 in all 8 terms (`B_anchor`).

**O3. Loader failure mode.**
- `build_stock` with `load_state_dict(strict=False)` on a C checkpoint gives 3 missing / 4 unexpected keys.
- Its num drifts by 1.9 % / 0.98 % from the recorded value (`C_stock_strictFalse`).
- `strict=True` raises RuntimeError.
- The perm is a persistent buffer (`merge.py:28`), so `build_simmim` + `strict=True` restores each arm's π automatically.

**O4. Embedding API reality** (`vendor_swift_ver11/simmim_swin4d_transformer_ver11.py:1382-1415`).
- `_forward_hook_embedding(x)` takes the same (B,1,96,96,96,20) input as `forward` and applies no mask.
- layer_0–2 come back as token sequences (B, L, C): (10240, 72), (1280, 144), (160, 288).
- Only layer_3 is 6-D: (B, 288, 2, 2, 2, 20).
- layer_0 is already after M0, so its token index means a C box in arm C and a cube in arm E.
- `forward_encoder` expects a pre-permuted (B, C, T, D, H, W) input and applies the mask token.
- My first smoke (job 412) crashed on this; it is ledgered as a failed attempt.
- The model prints `img_size:` / `patch_size:` lines to stdout, which corrupted my first JSON parse on CPU and on B300.

**O5. Cost** (job 420, 1 B300 GPU, bf16, batch 16).
- 0.00403 s per window per model; 60 windows = 0.242 s.
- 20 models (15 trained + 5 random-init), 1 subject, all layers: 4.74 s.
- Peak GPU memory 12.84 GB.
- np.load of one subject (1.51 GB fp16): 0.16 s, possibly page-cached.
- Whole job: 23 s.

**O6. Data staging** (count-only probes; no ID printed or written).
- `/scratch/data/hcp/download_HCP_REST1_filtered` has 1084 dirs.
- Under MNINonLinear/Results the only run name is `rfMRI_REST1_LR`: no REST2 and no RL.
- 103 complete `rfMRI_REST1_LR_hp2000_clean.nii.gz` files:
  - 88 = the r1 set (size match; sizes are unique, fraction 1.0);
  - 5 pre-date the r1 manifest (ctime < 2026-11-01T02:29:25Z), are not in r1, and equal the r1 `n_burned_excluded` = 5;
  - 10 arrived after the manifest.
- 250 REST1_LR dirs are still empty and 2 rsync processes are running, so the set is growing.
- There is no behavioural CSV under /scratch/data on B300.

**O7. Labels.**
- The only open-access behavioural file found is local: `/home/juke/data/veritas-class/week05-connectivity/hcp-fc/unrestricted_behav_data_n337.csv`.
  - It comes from the Finn-lab CPM tutorial (README) and has 582 HCP unrestricted columns, including `Gender` and binned `Age` (22-25: 73, 26-30: 153, 31-35: 109, 36+: 2).
  - There is no Family_ID or other restricted field. N = 337 (the Finn 2015 unrelated set).
- In-memory overlap with the staged files (IDs sent over ssh stdin, counts printed only) is 28.
- r1 split overlap (by size match): TEST 5, VAL 2, TRAIN 17. New files: ≤ 4, including possibly burned ones.

**O8. Receipts.**
- C1: 67/67 OK, rc 0. Code freeze: 33/33 OK.
- `card_sha256.txt` now FAILS on exactly 2 lines (hcp_manifest.json, split.json). These are superseded by `c4_sanitized_sha256.txt` (19/19 OK; addendum 05).
- The repo split.json holds positional tokens (h00…). B300 `/scratch/iitp4/worker_M3_r1/code/split.json` holds content pseudonyms.
- Layout lint on the run root: 0 findings over 365 files.

**O9. CPU synthetic probe P1** (`verification/explorer_FU_E_r1_2/cpu/p1_mask_confound_and_id_machinery.py`, outputs `p1.out.json`, `p1_spatial.out.json`; tiny_test cfg, random-init, 12 subjects, chance 0.083).
- Pure-noise subjects that differ only in brain mask:
  - spatial-token (time-mean) features identify 0.33 with per-subject masks and 0.00 with the group mask;
  - global mean-pooled features give 0.00 / 0.17.
- With a planted subject-specific FC:
  - the cell-FC baseline reaches 1.00 (Idiff ≈ 78);
  - the random-init first-order embeddings stay at 0.125.
- Shuffled session pairing gives chance or below.

**O10. CPU probe P3** (`verification/explorer_FU_E_r1_2/cpu/p3_verdict_mutants.py`, `p3.out.json`).
- A reference FU-E verdict function was run against 10 mutants: V01–V04 boundaries, V06 F− downgrades modify, V07 missing gate = pass, V08 failed runs counted, V11 stop kept on F+ fail, case A (F+ fail → no_verdict), and X1 integrity ignored.
- All 10 are killed by 15 fixtures, and the baseline is clean.
- Boundary fixtures built through the t-interval arithmetic were fragile: 3 of 4 gave the wrong expected label on the CORRECT code. Only exact-interval injection made them valid.

## 2. Logic chain
1. O1 + O2 → the checkpoints are not lost and the evaluation path is bit-faithful, so retraining is unnecessary and the "untestable: checkpoints lost" branch is only a guard. /scratch can still be wiped (dispatch), so the card pins the 15 sha256 values (O1) and keeps that branch.
2. O3 → a loader that uses `strict=False` or the stock builder runs silently with a wrong M0, so the card requires strict loading, the perm-buffer check and the anchor as integrity gates (→ no_verdict).
3. O6 → REST2 is not staged; fetching it needs HCP credentials and a new download, which are outside this option. Cross-session fingerprinting is therefore untestable, and the only identity probe available is within REST1_LR (split-half).
   - Adjacent windows and the full-run z-score couple the two halves. A gap is needed, and the result must be labelled within-session; it is not Finn-style cross-session.
4. Stage-1 trained on TRAIN subjects' full runs (card §4/§5). Identification there could come from memorisation, so the primary pool is subjects no encoder saw: TEST 16 + VAL 8 + 10 new = 34.
   - The 5 burned subjects are excluded by the ctime rule in O6, cross-checked against count = 5, or by the sealed salt held in memory only.
   - The set must be pinned at freeze because the rsync keeps adding files.
5. O7 → at most 11 held-out labelled subjects, binary sex or 3 effective age bins. Any classifier contrast between arms at δ = 0.01 is unpowered, so age/sex cannot carry a verdict. The card should state "untestable: labels"; at most a descriptive LOSO probe on all 28, flagged as including SSL-seen subjects.
6. O9 → spatial features can identify subjects from mask shape alone, so an anatomy control is required (mask-only input; intersection-masked sensitivity). First-order random embeddings carry no FC identity while cell-FC does, so the real-data capacity gate uses the cell-FC baseline, and "training value" is tested against exact seed- and arm-matched random-init encoders (`build_simmim(cfg, perm, seed)` reproduces the step-0 weights by construction; test_model_pairing).
7. Top-1 accuracy is bounded and needs no division. Idiff_E may be ≈ 0 for weak encoders, which would make a relative contrast unstable. So J = acc_C − acc_E with δ = 0.01 absolute, which matches the PI label "1% / 0.01" in decision 3.
8. O10 → verdict code must keep classification separate from interval arithmetic, and boundary tests must inject exact numbers. Every named defect class can then be killed cheaply.
9. O5 → for 30 models × 3 input conditions × 98 subjects × 60 windows, the upper bound is 0.0040 × 30 × 3 × 98 × 60 / 3600 ≈ 0.59 GPU-h. Held-out only is ≈ 0.2 GPU-h. Both fit inside the 1.5 cap with margin.

## 3. Caveats
- The cost was measured on 1 subject; I/O for uncached subjects may be slower. 0.16 s may reflect page cache, and r1 preprocessing logged 160 s for 88 subjects with 16 workers (~29 s per subject per worker).
- The CPM CSV is a row subset redistributed by a third party (Finn lab). The full ConnectomeDB unrestricted file was not found. If the PI supplies it, labelled N rises to ≤ 98, which is still underpowered for arm contrasts.
- Seed-level variance of identification accuracy is unknown, so no power number is given for J1. With df 4, intervals may be wide.
- The anatomy probe P1 is a tiny CPU model with N = 12. It shows that the confound exists, not how large it is on real data.
- I did not run a fingerprint or probe statistic on real data: no card is frozen yet. The anchor only reproduced numbers that r1 had already recorded.
- The overlap counts of the r1 88 with the CSV rely on size matching (sizes are unique). The new-file overlap (≤ 4) may include burned subjects.

## 4. Conclusion (recommended strategy for the FU-E worker)

**Card** (new, dated, frozen with sha256 receipt in `results/topic2/2026-11-0X_fuE/` before any real-data statistic). It states:
- **(i) Data.** REST1_LR only, so cross-session is untestable. Probe pool = TEST + VAL + post-manifest new subjects; burned exclusion rule; pinned count and positional/HMAC manifest. TRAIN is a secondary memorisation reading.
- **(ii) Encoders.** 15 checkpoints with pinned sha256 (O1 list) + 15 exact random-init twins `build_simmim(cfg, perm_arm, seed)`.
- **(iii) Features.**
  - Primary: layer_3, time-mean over each window's 20 frames, 288 × 8 = 2304-d.
  - Descriptive: global mean of layers 0–3.
  - Native input is primary; mask-only and intersection-masked inputs are controls.
- **(iv) Metric.**
  - Single-window top-1 identification: reference = mean embedding of windows 0–24, queries = windows 35–59 (gap 10 windows = 200 TR), Pearson similarity, both directions averaged.
  - Secondary: Idiff.
- **(v) Contrasts.** J1 = acc_C − acc_E and J2 = acc_C − acc_S per seed; t95 df 4; δ = 0.01 absolute.
- **(vi) Rules, in order.**
  1. Any checkpoint missing → `untestable_checkpoints_lost`.
  2. Integrity failure (sha, perm, anchor ≥ 2 TEST positions exact, strict load), any extraction failed after one rerun, or a gate result missing → `no_verdict`.
  3. F+ synthetic machinery fail, or real capacity gate fail (half-run cell-FC identification ≤ pre-set threshold) → `inconclusive`.
  4. stop: upper < δ. keep: mean ≥ δ ∧ lower > 0 ∧ lower(J2) > 0. modify: mean ≥ δ ∧ lower > 0 ∧ lower(J2) ≤ 0. Anything else: inconclusive. An F− failure downgrades keep only, stated and tested.
- **(vii) Descriptives.** Training value acc_trained − acc_init per arm and seed; cell-FC baseline; TRAIN reading; anatomy controls (if the intersection-mask sensitivity changes the verdict category, report both).
- **(viii) Age/sex.** Untestable (labels: ≤ 11 held-out labelled). An optional descriptive LOSO probe on 28 subjects, with no verdict.

**Implementation** (own paths, e.g. `src/topic2_fuE/`, `scripts/topic2_fuE_*.py`, `tests/topic2_fuE/`).
- Import the frozen r1 modules. `HCPSource.batch` plus a subject-outer / model-inner loop.
- Preprocess the 10 new subjects with imported `D.preprocess_run` / `D.cell_means` into the worker's own /scratch/iitp4 dir, never the r1 dir.
- Every B300 step via sbatch (CPU preprocessing too); ledger start and completed rows.
- Run soon (/scratch wipe risk), in ≤ 2 GPU jobs, ≤ 0.75 GPU-h planned, cap 1.5.

**Tests and fixtures that must fail on the targeted defect.**
- (a) strict=False / stock builder → anchor test fails.
- (b) wrong layer shape handling (layers 0–2 are B, L, C).
- (c) no gap between halves, or overlapping reference/query windows → leakage fixture with an AR(1) synthetic signal fails.
- (d) per-subject-mask anatomy fixture (P1) must flag the defect when the anatomy control is skipped.
- (e) a planted-identity F+ that must be recovered; a shuffled-pairing F− that must sit at chance.
- (f) V01–V11, case A, lost/integrity branches via exact-interval injection (P3 pattern).
- (g) TRAIN-subject leakage guard: the primary pool must exclude every subject in split["train"], tested.
- (h) no pseudonym or 6-digit ID in any repo output (reuse the topic2_id_scan pattern).
- (i) model stdout prints must not break JSON outputs.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                       # 33 OK
LC_ALL=C sha256sum -c results/topic2/2026-11-01/c4_sanitized_sha256.txt                         # 19 OK
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_E_r1_2/cpu/p3_verdict_mutants.py   # n_survivors 0, baseline_failures []
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_E_r1_2/cpu/p1_mask_confound_and_id_machinery.py spatial   # stdout has model prints before the JSON
cat verification/explorer_FU_E_r1_2/b300/fue2_smoke.out.json      # integrity, anchor, cost
grep explorer_FU_E_r1_2 results/gpu_ledger_2026-10-31.md          # 4 rows: 2 started, 2 completed (0.003 + 0.007)
```

On B300 (read-only), re-hash the 15 checkpoints (`sha256sum /scratch/iitp4/worker_M3_r1/runs/hcp_*/model_final.pt`) and compare with O1 / explorer_FU_E_r1_1. Re-run the O6 counts by size/ctime only.

**Invalidation.**
- Any checkpoint sha differs → re-establish provenance before the card.
- REST2 becomes staged → cross-session becomes testable and the primary should switch, by card.
- The full unrestricted CSV is supplied → re-cost the label probe.
- The rsync adds held-out subjects before freeze → pin the larger pool.
