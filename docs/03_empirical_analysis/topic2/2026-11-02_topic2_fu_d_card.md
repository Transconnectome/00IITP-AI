# Topic 2 follow-up D (FU-D) analysis card: connectome box grouping at M0 at SwiFT ver11 E192 scale

Status: **FROZEN** when its sha256 is written to `results/topic2/2026-11-02_fu_d/card_sha256.txt`. Later changes go in dated addenda (`2026-11-02_topic2_fu_d_addendum_NN.md`); this file is never edited.
Author: worker_FU_D_r1, run tw-20261031-four-topics, milestone FU_D (PI decision 7, result report §7 option D), 2026-11-02 (KST).
Mode: **CONFIRMATORY.** One manipulated factor relative to the r1 experiment (model scale). The decisions in §7–§10 are fixed before any FU-D real-data number exists.
Parent experiment: `2026-11-01_topic2_card.md` (r1, frozen, sha256 receipt `results/topic2/2026-11-01/card_sha256.txt`). The r1 verdict (`stop`; I1 +0.147 % [−0.068 %, +0.361 %] < δ) stands as recorded. FU-D is a new experiment; its result is reported **beside** the r1 verdict, never as a re-reading of it.

## 0. What was known before freezing (disclosure)

- **All r1 results are known**: per-seed test NMSE, I1 and I2 intervals, the stalled `hcp_S_s2` run, the Stage-0 numbers, the F± gate values at E36 (result report §0–§4, addenda 01–05). Option D was chosen by the PI **after** the r1 stop, from the costed list in result report §7. The expected outcome, given r1 and the dev-subject exploration in r1 card §0, is `stop`.
- **No FU-D real-data number exists.** No E192 model has been trained or evaluated on HCP data. The three FU-D explorers ran synthetic-only Slurm smokes (jobs 396, 404, 430; 0.097 GPU-h in total): E192 at batch 16 takes 0.478–0.491 s/step (32.6–33.5 samples/s), peak GPU memory 198 GiB of 268 GiB with all 88 subjects GPU-resident, projected 1.19–1.23 GPU-h per run. They also probed (CPU) where M0 sits at E192 and that the frozen r1 verdict script cannot express a reduced gate (§12).
- The real-data cost smoke and the data-view equivalence check of §10.1 run **after** this card is frozen.
- **Same test set as r1.** The 16 TEST subjects are the r1 TEST subjects; r1 test numbers at E36 are known. This is disclosed, not corrected: changing the split would add a second factor.

## 1. Question, estimand, unit

**Q.** r1 found no practically relevant gain at E36 (38.7 M parameters, 288-d final token, every arm reconstructing ≈1 % of the masked variance). Could the null reflect model capacity? At SwiFT ver11 **E192 d2-2-18-2** (474,226,176 parameters, 1536-d final token), trained from scratch with SimMIM on the same HCP-YA data, split, masks, seeds and budget, does grouping the 12 mm stage-0 cells into connectome boxes at M0 (16³→8³) instead of PatchMergingV2's 2×2×2 cubes lower the held-out masked in-brain NMSE by at least δ = 1 % (PI decision 3)?

- **Practical claim (C vs E).** I1 = (NMSE_E − NMSE_C) / NMSE_E.
- **Connectome-specific claim (C vs S).** I2 = (NMSE_S − NMSE_C) / NMSE_S.
- **Unit of inference.** The training seed, exactly as r1 §1 and §6. Baseline = arm E = stock ver11 E192 (bit-identical forward).

## 2. The single change from r1: model scale

**Configuration** `E192_d22182` (VRABES `extract_vrabes_swift_E192.sh` architecture on the r1 input geometry):
`dict(img_size=(96,96,96,20), in_chans=1, embed_dim=192, window_size=(4,4,4,10), patch_size=(6,6,6,1), depths=(2,2,18,2), num_heads=(6,12,24,48), c_multiplier=2)`; 474,226,176 parameters.

- It is registered at runtime into the frozen `src.topic2_rgpool.model.CONFIGS` dict by `src/topic2_fu_d/config.py` (`train.CONFIGS` is the same object). No frozen file is edited.
- **Where M0 sits (from code; pinned by `tests/topic2_fu_d/test_e192_model.py`).** The stage-0 grid is 16³×20 (96/6), the octant edge is 8 (4 stages), exactly as at E36. M0 = `layers[0].downsample` = `ConnectomeRGBoxPooling` wrapping an unchanged PatchMergingV2 with `LayerNorm(1536)` and `Linear(1536→384)` (8C→2C, C = 192). M1 and M2 are stock PatchMergingV2; stage 3 has no merge. So the r1 gather applies unchanged; only its channel width differs (5.3× wider than E36's 288→72).
- **Not adopted from VRABES:** mask ratio 0.8 and its learning rate, which would be second and third manipulated factors; `last_layer_full_MSA` is not a ver11 argument (it is swallowed by `**kwargs`) and the stage-3 window already covers the whole 2³ grid. Consequence: no hyperparameter is tuned for E192 (limitation §11).

## 3. Arms (unchanged r1 partitions, byte-identical)

| arm | M0 permutation | file (sha256) |
|---|---|---|
| E | identity (stock PatchMergingV2) — baseline | `perms_hcp.npz` key `E` |
| C | balanced connectome boxes on the train-only group FC (r1 §3) | `perms_hcp.npz` key `C` |
| S | same builder on the distance-binned FC surrogate, surrogate seed = training seed | `perms_hcp.npz` key `S_seed{s}` |

- `results/topic2/2026-11-01/partitions/perms_hcp.npz` sha256 `ec05b796a450d78b646172cb84031f04758fef6965e085db87a75c6b620f2b34`; fixtures `perms_Fplus.npz` `b288a5ad262b5693ed0f98e8cca57bc536ce60f621ee3a5862f1249ca8ac796b`, `perms_Fminus.npz` `b044266eceae820ad023aa54ef616886ec0289b0ae5a112de486565a79270d9d`; per-key perm sha256 as in `partitions_hcp.json` / `partitions_fixtures.json`. They depend only on the grid (16) and octant edge (8), so they apply to E192 unchanged. **No partition is rebuilt**; Stage 0 is not rerun (its r1 output stays the descriptive reference).

## 4. Data contract and split (C4, C6)

- **Data.** HCP-YA S1200 open access REST1_LR, the r1 preprocessed arrays on B300 b300-01 (`/scratch/iitp4/worker_M3_r1/hcp`, 88 subjects; r1 manifest sha256 `26ba34a9…f96d5`, dev subjects already excluded). HCP-YA OA counts as public under C6 (PI decision 2); no redistribution, no re-identification. Data never leave b300-01; only run records with positional tokens, per-subject error terms and aggregates are copied back. No preprocessing is rerun (it would need the sealed dev salt).
- **Positional view (C4).** FU-D reads the arrays only through hard links `/scratch/iitp4/fu_d/hcp/subjects/hNN/`, hNN = position in the r1 original manifest (the frozen r2 sanitizer rule, `scripts/topic2_c4_sanitize.py` `token_map`), built by `scripts/topic2fu_d_make_view.py`. The build refuses to link unless the original manifest and split match their card sha256 and the positionally mapped original split equals the repo's sanitized split exactly (list order included). Hard links share the r1 inodes (same bytes, no copy). Every run uses `--split-file` = the repo's sanitized `results/topic2/2026-11-01/split.json` (sha256 `cc521b087a97a6669fe6f94041dac2c2c0c0987741ac698203309af1ced2c75a`), so every run.json carries positional tokens only.
- **Split.** The r1 split, unchanged: 64 TRAIN / 8 VAL / 16 TEST, same order. Val: health check and learning curve only; no model selection, no early stopping. HCP family structure is unavailable (r1 limitation, unchanged).
- **C4 scans.** Before every copy-back a B300-side count-only scan (`scripts/topic2fu_d_b300_scan.py`) checks the files for any original token, content hash or staged HCP subject ID; a hit blocks the copy. Locally `scripts/topic2fu_d_c4scan.py` and `tests/topic2_fu_d/test_c4_outputs.py` scan every FU-D text output.

## 5. Model and training (identical to r1 §5 except the configuration)

SimMIM, mask unit 1 cell × 2 frames, mask ratio 0.6; loss = MSE over masked in-brain voxels; AdamW (0.9/0.999), weight decay 0.05, peak lr 2e-4, linear warmup 5 %, cosine to 0, gradient clip 1.0, bf16 autocast, flash SDP; **8,750 steps × batch 16 = 140,000 samples**; weight-init seed s, window-order seed 1000+s, training-mask seed 2000+s, fixture-stream seed 3000+s; evaluation masks 7001 (val) / 7002 (test); val NMSE at steps 2188/4375/6562/8750; test once at 8750. All values are passed explicitly by `scripts/topic2fu_d_train.py` (from `src/topic2_fu_d/config.py`) to the frozen `scripts/topic2_train.py` / `src/topic2_rgpool/train.py`. Checkpoints are saved on B300 only.

## 6. Primary outcome

As r1 §6: NMSE_arm,s = Σ_i num_i / Σ_i den_i over the 16 TEST subjects × 60 non-overlapping windows, masked in-brain voxels, fixed masks.

## 7. Gates (synthetic, full budget, at E192)

**7.1 F+ measurement-capacity gate (run first).** Arms E, C, S × **seed 0** on the r1 F+ generator stream (`perms_Fplus.npz`, S surrogate seed 0), full §5 budget; outcome = test NMSE over 16 × 32 fixed synthetic windows (eval seed 7002). **Passes iff (E−C)/E ≥ δ and (S−C)/S ≥ δ.**
- F+ computed and failed → verdict `inconclusive` (measurement capacity at E192); Stage 1 is **not run**, and if Stage-1 records exist they are not read.
- A gate run that is not completed after its one rerun → `no_verdict`. A missing gate is never a pass.
- Why one seed: the r1 gate (12 runs) at E192 would cost ≈ 14.4 GPU-h and, with Stage 1, exceed the 25 GPU-h cap (§10). At E36 both F+ seeds gave the same decision with large margins (+3.06 % / +2.93 %); the gate is re-run at E192 because a wider M0 and a 474 M-parameter model might make token grouping irrelevant, and a D `stop` would be uninterpretable without it.

**7.2 F− bias check (conditional).** Arms E and C × seed 0 on the r1 F− stream (`perms_Fminus.npz`), full budget, run **only if** steps 1–7 of §8 give `keep` and the cost guard (§10) allows 2 runs. **Passes iff (E−C)/E < δ.** It can only downgrade a would-be `keep` (§8 step 8). F− never changes `stop`, `modify` or `inconclusive`. The rule is a pre-registered sequential design: F− is synthetic, so knowing that Stage 1 points to keep gives nothing to tune.

## 8. Inference and verdict (`src/topic2_fu_d/verdict.py`, `scripts/topic2fu_d_verdict.py`)

δ = 0.01 (1 % relative NMSE). Primary: two-sided 95 % t interval (df n−1) over the n seed-level contrasts I1_s and I2_s, paired by seed (frozen `stats.t_interval`, `stats.relative_gain`). Secondary (descriptive, never overrides): hierarchical bootstrap (frozen `stats.hierarchical_bootstrap`, B = 10,000, seed 0).

The planned run set comes from the design, `seed_plan.json` (seeds 0..n−1) and the F− condition — never from whatever runs exist. Unplanned directories, duplicate or mismatching records, records violating the pins of §2–§5, or a rerun of a completed run are protocol errors (the verdict script stops). Rules, in this order:

| step | condition | verdict |
|---|---|---|
| 1 | an F+ gate run not completed after its one rerun | `no_verdict` (software) |
| 1 | F+ gate runs absent | `no_verdict` (protocol; never a pass) |
| 2 | F+ computed and failed | `inconclusive` (measurement capacity); Stage 1 not read |
| 3 | seed plan absent | `no_verdict` |
| 3 | seed plan n = 0 (cost) | `no_verdict` (Stage 1 not launched: cost cap), with a costed plan |
| 4 | any planned Stage-1 run not completed after its one rerun | `no_verdict` (software) |
| 5 | hi(I1) < δ (strict) | **stop (killed)** |
| 5 | mean(I1) ≥ δ and lo(I1) > 0 and lo(I2) > 0 | keep |
| 5 | mean(I1) ≥ δ and lo(I1) > 0 and lo(I2) ≤ 0 | modify |
| 5 | anything else | inconclusive |
| 6 | seed-mean test NMSE of arm E ≥ 0.999 (baseline never left the predict-zero solution) | inconclusive (real-data capacity floor) |
| 7 | some Stage-1 run stalled (§9) and the step-5 category recomputed without every seed containing a stalled run differs, or fewer than 2 such seeds remain | inconclusive (stall-sensitive) |
| 8 | would-be keep: F− passed | keep |
| 8 | would-be keep: F− failed | inconclusive (bias flag) |
| 8 | would-be keep: F− run failed after its rerun | no_verdict |
| 8 | would-be keep: F− not run (cost guard) | inconclusive (keep pending F−) |

The kill criterion is the **stop** rule. Step-5 rules are the r1 card §8 rules; the code asserts that they agree with the frozen `stats.verdict` on every call. Steps 6–7 are new, pre-registered guards (§12).

## 9. Readings fixed in advance (none changes the category)

- **(a) Stall.** A run is stalled iff its final val NMSE ≥ 0.999 and its test NMSE ≥ 0.999. Stalled runs are valid runs (not software failures) and stay in the primary analysis; step 7 is their only effect on the category. The stall sensitivity (category and intervals without stalled seeds) is reported.
- **(b) Scale manipulation check.** If the seed-mean test NMSE of arm E at E192 is ≥ the r1 E36 value (0.98892, read from `results/topic2/2026-11-01/verdict.json`), the report adds "scale did not raise the reconstruction ceiling".
- **(c) Joint reading with r1 (r1 = stop).** FU-D stop → the null replicates at ≈12× parameters. FU-D keep → a scale-dependent, connectome-specific gain. FU-D modify → a scale-dependent gain not attributable to FC specificity (I2 is confounded with box compactness, addendum 05). FU-D inconclusive / no_verdict → FU-D adds no decision; the r1 stop stands alone.
- **(d)** r1 and FU-D seeds are never pooled. Validation learning curves are descriptive.

## 10. Compute, cost-only seed rule and run integrity (C5)

**Hardware.** B300 b300-01 only (the HCP arrays and the FU-D venv exist only there), every job via `sbatch` (`scripts/topic2fu_d_slurm.py`): partition gpu (smoke: debug), `--nodelist=b300-01 --gres=gpu:1`, `--time 02:00:00` per training run. Before **every** submission: the B300-share rule (no submission while a `g3t-G-E0-*` job is pending or running; waits logged) and the cost guard. Jobs are submitted held, the ledger "started" row is written with the job id, then released; the "completed"/"failed" row carries GPU-h = sacct ElapsedRaw × GPUs, rounded up (sacct prints KST; converted to UTC). Env: own venv `/scratch/iitp4/fu_d/venv` installed from the r1 lock (`scripts/b300_env/lock.txt`, sha256 `ae664dc9…31a2`; freeze identical, `scripts/topic2fu_d_build_env.py`).

**10.1 After freeze, before the gate (one ledgered smoke job, ≤ 0.1 GPU-h).** (i) Data-view equivalence: the frozen `evaluate_hcp` re-scores the r1 `hcp_E_s0` E36 checkpoint through the FU-D positional view; it must reproduce the r1 recorded test NMSE and per-subject terms exactly (no FU-D model is evaluated). If not, FU-D stops and reports. (ii) Real E192 HCP cost: one frozen training loop (arm C, seed 0) aborted by the throughput probe at step 200; its `projected_run_hours` enters the seed rule. No evaluation is run.

**10.2 Seed rule (cost only; `src/topic2_fu_d/seedplan.py`, written once by `scripts/topic2fu_d_seed_plan.py` with a sha256 receipt, after the F+ gate and before any Stage-1 submission).**
c = 1.05 × max(max sacct GPU-h of the 3 completed F+ gate jobs, HCP smoke projected hours); B = min(25 − FU-D GPU-h used, 95 − run GPU-h used), both from the ledger at planning time (FU-D = worker_FU_D_* and explorer_FU_D_* rows).
- n = 5 if 16c ≤ B (15 runs + one rerun in reserve);
- otherwise n = 4 if 13c ≤ B (seeds 0–3);
- otherwise n = 0: Stage 1 is not launched (§8 step 3).
n = 3 is excluded: with one stalled run the n = 3 interval collapses (explorer power simulation). Seeds are always 0..n−1; the rule never sees an outcome.

**10.3 Cost guard (per submission).** A job is submitted only if (FU-D GPU-h completed) + c × (running FU-D jobs + 1) ≤ 25 and the same on the 95 GPU-h run ceiling. A run that cannot be launched under the guard is missing (§8).

**10.4 Run integrity.** A run is a software failure if its run.json status is not `completed` (non-finite loss, crash, `aborted_throughput` at the step-200 probe with projection > 1.6 h) or Slurm reports anything but COMPLETED (TIMEOUT, OUT_OF_MEMORY, NODE_FAIL, FAILED, CANCELLED). Each failed run is rerun **once** with the identical command in a new `<run>_a1` directory; both stay in the ledger. A second failure leaves the run missing (§8 step 1/4/8). The wrapper writes `fud_meta.json` (wrapper and FU-D code sha256, configuration dict, argv, Slurm job id, node) and re-checks the configuration name, the parameter count 474,226,176 and the frozen r1 code hashes after the run.

**Budget plan.** F+ gate 3 × ≈1.25 ≈ 3.8; Stage 1 (n = 5) 15 × ≈1.25 ≈ 18.8; one rerun ≈ 1.25; conditional F− 2 × ≈1.25 (only if no rerun was used and the guard allows). Explorers 0.097 already used. Total ≤ 25.

## 11. Limitations stated in advance

- Single additional setting: E192 at the r1 budget (140k samples, ≈18 passes), untuned; a 474 M-parameter model may be under-trained at this budget. A stop at E192 covers this setting only.
- One-seed F+ gate (power at E192 unknown; at E36 the margins were ≈3×δ).
- Same TEST subjects as r1; HCP relatives may straddle splits.
- I2 is confounded with box compactness (addendum 05).
- B300 is shared (≤ 8 GPUs for the Slurm user): wall-clock is not controlled; contention can raise per-run cost (seed rule, §10).

## 12. Deviations from r1 (named)

1. Model scale E36 d2262 → E192 d22182 (the manipulated factor).
2. Gate reduced to F+ E/C/S × seed 0; F− reduced to E/C × seed 0 and run only for a would-be keep (cost).
3. Seed count by the cost-only rule of §10.2 (5 or 4) instead of fixed 5.
4. New pre-registered guards: capacity floor (§8 step 6) and stall robustness (§8 step 7).
5. Throughput abort threshold 1.6 h (r1 0.75 h) and Slurm limit 2 h (r1 hard timeout 3300 s), because an E192 run takes ≈1.2 h; `aborted_throughput` and Slurm failure states are named software failures.
6. Data read through the positional hard-link view with the sanitized split (C4); same bytes and order, checked by §10.1(i).
7. Own verdict code: the frozen `scripts/topic2_verdict.py` hard-codes FIX_SEEDS = (0, 1) and HCP_SEEDS = (0..4), maps an F+ failure to `no_verdict` where the r1 card says `inconclusive`, and counts a missing F− as a pass; it cannot express this design and is not used.

## 13. Frozen inputs

- This card: sha256 in `results/topic2/2026-11-02_fu_d/card_sha256.txt`.
- FU-D code at freeze: sha256 of every file under `src/topic2_fu_d/`, `scripts/topic2fu_d_*.py` and `tests/topic2_fu_d/` in `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`.
- Frozen r1 code: `results/topic2/2026-11-01/code_sha256_at_freeze.txt` (checked in every run record).
- r1 inputs: the sha256 values in §3 and §4.
