# Handoff (Hard) — explorer_FU_D_r1_1, milestone FU_D (Topic 2 follow-up D: SwiFT ver11 E192 scale)
Written 2026-11-01 ~15:05Z. Lens: scientific design and falsifiability. No production code written; no git writes.

**Summary.** FU_D can run inside its 25 GPU-h cap, but only with a smaller fixture gate than r1. An E192 run measured 1.23 GPU-h (HCP path) and 1.20 GPU-h (fixture path), and it fits in one B300 GPU (peak 198 GiB). The §7 figure "≈20 GPU-h" counted only the 15 Stage-1 runs. An r1-style 12-run fixture gate at E192 adds 14.4 GPU-h, which brings the total to 32.9 > 25. The recommended design has five parts:
- an F+ gate at E192 with one seed (3 runs);
- a seed-count rule frozen in the card before any run (n = 5, otherwise 4, otherwise do not launch);
- an F− check run only if the result would be `keep`;
- a new FU_D verdict script;
- run records that carry positional tokens through a symlinked data view on b300-01.

## 1. Observation

| id | observation | evidence |
|---|---|---|
| O1 | Section 7 option D reads "E192 d2-2-18-2, 140k samples, 15 runs, ≈ 20 (1.36 h per run)". The 1.36 h comes from 140,000 / 28.6 samples/s, a batch-4 random-tensor smoke run. It covers no fixture gate. | `docs/03_empirical_analysis/topic2/2026-11-01_topic2_result_report.md` §7; `verification/explorer_M3_r1_1/smoke_b300_steptime.log:33` |
| O2 | r1 card §7.2: the training-loop gate is 12 runs (E/C/S × seeds {0,1} × F+, F−) at the full §5 budget. F+ fail → Stage 1 is not run → `inconclusive`. F− fail → `keep` is downgraded. | `2026-11-01_topic2_card.md` §7.2 |
| O3 | **My Slurm smoke** (job 404, b300-01, 1 GPU, 92 s, 0.03 GPU-h, ledger rows 14:40:35Z / 14:42:07Z). Synthetic tensors only: 64/8/16 GPU-resident HCP-format subjects (123.8 GiB), frozen `build_simmim` with E192 and the r1 C permutation, the r1 training step.<br>• 0.491 s/step at batch 16 (32.6 samples/s).<br>• Arm E 0.490 s/step, so the gather adds no cost.<br>• F+ stream 0.489 s/step.<br>• Peak memory 198.3 GiB allocated, 222.9 GiB reserved, of 268.6 GiB per GPU.<br>• Evaluation 1.35 s per HCP subject.<br>• Projected cost 1.229 GPU-h per HCP run and 1.202 GPU-h per fixture run. Loss finite. | `verification/explorer_FU_D_r1_1/smoke_e192.out.json`, `smoke_404.log`, `smoke_e192.py`, `smoke_e192.sbatch` |
| O4 | r1 calibration: at E36, the r1 worker's synthetic smoke gave 0.18 s/step and real runs 0.1757 s/step. Real wall time was 1544–1655 s against 0.434 h projected, i.e. up to +6 % with 8 jobs per node. | `results/topic2/2026-11-01/runs/hcp_*/run.json`, `train_log.jsonl`; ledger row 03:06:13Z |
| O5 | **Where M0 sits at E192** (CPU probe, no forward pass):<br>• m0_grid 16, octant edge 8.<br>• Stage-0 downsample = `ConnectomeRGBoxPooling` wrapping PatchMergingV2 with input (20,16,16,16), Linear 1536→384, LN 1536, 592,896 parameters; its perm equals the r1 C perm.<br>• M1 and M2 are stock (3072→768, 6144→1536). Stage 3 has no merge.<br>• 474,226,176 parameters.<br>• Arm C's initial weights are bit-identical to stock ver11 (perm buffer excluded). | `verification/explorer_FU_D_r1_1/probe_e192_structure.py` / `.out.json` |
| O6 | The partitions depend only on grid g=16 and octant edge 8, not on model width. The keys in `perms_hcp.npz` are E, C, S_seed0..4, G, R, nvox and group_mask. `perms_Fplus.npz` holds E, C, S_seed0..1 and labels. So the r1 permutations apply to E192 unchanged. | `results/topic2/2026-11-01/partitions/`; `partitions_hcp.json` (per-key perm sha256) |
| O7 | `train.run` reads `cfg = CONFIGS[a.cfg]`, and `CONFIGS` has only E36_d2262 and tiny_test. `train.CONFIGS is model.CONFIGS` → True. A new wrapper can therefore register an E192 config without editing `src/`. `run.json` `code_sha256` covers `src/topic2_rgpool` only. | `src/topic2_rgpool/model.py:16-23`, `train.py:144`; local check |
| O8 | `train.run` aborts at step 200 if the projected time exceeds `--max-run-hours`. The default is 0.75 h; E192 projects 1.23 h. That abort status (`aborted_throughput`) is not among the r1 card §5 software failures (timeout / non-finite / crash). | `train.py:205-214`, `scripts/topic2_train.py:36` |
| O9 | **The frozen `scripts/topic2_verdict.py` misfits FU_D** (synthetic run records):<br>• (1) F+ with 1 seed passing, n=4, a clear stop → `no_verdict` "Stage 1 incomplete", and the F+ pass is reported as None, because `FIX_SEEDS=(0,1)` and `HCP_SEEDS=(0..4)` are hard-coded.<br>• (2) F+ fails and Stage 1 is not run → `no_verdict`, where the card says `inconclusive`. This is challenger_M3_r2_2's case-A defect, reproduced.<br>• (3) F+ passes with 1 seed, n=5, a clear keep → `inconclusive` with the reason "F+ failed", which is false.<br>• Also, line 66 `fm is not False` counts a missing F− as a pass (addendum 05 §4.8). | `verification/explorer_FU_D_r1_1/probe_frozen_verdict_misfit.py` / `.out.json` |
| O10 | **B300 data.**<br>• Slurm partitions gpu/interactive/debug on b300-[01-04]. b300-01 = 61.107.201.98.<br>• `/scratch` is node-local md0.<br>• The r1 preprocessed HCP data exist only on b300-01: `/scratch/iitp4/worker_M3_r1/hcp/subjects`, 88 directories, both arrays present, 132.8 GB, one file size.<br>• .99 has no HCP data; .101 and .103 did not answer in time.<br>• The subject directories carry the old unsalted tokens. | ssh/srun outputs (counts only) |
| O11 | A positional view is feasible. Mapping sealed manifest order to `h%02d` makes the sealed split equal to the repo's sanitized `split.json` exactly (train/val/test True, 64/8/16). CPU srun on b300-01, stdlib only, counts and booleans printed. | `verification/explorer_FU_D_r1_1/probe_b300_posmap.py` |
| O12 | **Power simulation** of the card §8 rules, seed-level I1 ~ N(μ, sd):<br>• At the r1 sd (0.173 %), n=4 is about as decisive as n=5: true I1 = 0.5 % gives P(stop) 0.957 vs 0.996.<br>• With an inflated sd of 0.5 % (one stalled run), n=4 gives P(stop | μ=0) = 0.76 vs 0.91 at n=5, and n=3 gives 0.47.<br>• So n=3 is too weak. | `verification/explorer_FU_D_r1_1/power_seed_rule.py` / `.out.json` |
| O13 | VRABES E192 used embed 192, depth 2 2 18 2, heads 6 12 24 48, window 4,4,4,10, patch 6,6,6,1, c_multiplier 2, mask_ratio 0.8 and `last_layer_full_MSA True`. ver11 has no such argument, so it is swallowed by `**kwargs`, and the stage-3 window already spans the whole 2³ grid. | `/home/juke/git/VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh:82-88`; vendored ver11 constructor |
| O14 | **Run ceiling arithmetic.** 11.73 used + caps A8 + B33 + C13 + D25 + E1.5 + H2 6 = 98.23 > 95, before counting verifiers. The ledger total of completed rows was 11.99 before my 0.03. | ACCEPTANCE addendum; ledger |
| O15 | C1 rc 0 (no non-OK line). Code freeze 33/33 OK. The B300 copy of `src/topic2_rgpool/*.py` equals `code_sha256_at_freeze.txt`. | commands in §5 |

## 2. Logic Chain

1. **Budget (O1–O4).** The cost is 15 Stage-1 runs × 1.23 = 18.4 GPU-h, plus whatever gate is run.
   - The r1 12-run gate costs 14.4 → 32.9 > 25.
   - A single-seed F+ gate (3 runs, 3.6) gives 22.0 at n = 5, or 23.4 with the +6 % contention seen in r1.
   - That leaves about 1.3–2.9 GPU-h for one rerun or for the F− check (2 runs ≈ 2.4), not both.
   - So the gate must be reduced and the seed count must follow a rule fixed in advance (dispatch: "reduce seeds only by a pre-registered rule").
2. **Why F+ must be rerun at E192 rather than inherited from E36 (O5, card §7.2).**
   - F+ is the measurement-capacity check: can the training loop turn a planted grouping signal into ≥ δ?
   - At E192 the M0 Linear is 5.3× wider (1536→384 vs 288→72), with 18 global-attention stage-2 blocks and a 1536-d final token. A larger model might make token grouping irrelevant.
   - Without an E192 F+ pass, a D `stop` cannot be read as "grouping is worth < δ at E192".
   - F+ is synthetic, so running it first and gating Stage 1 on it costs only 3.6 GPU-h if it fails.
3. **Why F− can be conditional.** In r1, F− only downgrades `keep` (card §8; `stats.verdict`).
   - Its rule needs E and C only: (E−C)/E < δ.
   - Running it only when Stage 1 would give `keep` is a sequential rule fixed in advance. F− is synthetic, so knowing that Stage 1 points to keep gives nothing to tune.
   - A missing F− must never count as a pass, which is the defect class in O9.
4. **Single manipulated factor (O5–O7).**
   - Reuse the r1 permutations byte-identically (sha256-pinned).
   - Keep the r1 data, split, masks, seeds, optimiser, schedule, budget (8,750 × 16) and mask ratio 0.6.
   - Then FU_D differs from r1 only in model scale (E36 d2262 → E192 d22182).
   - Do not adopt VRABES mask_ratio 0.8 or its LR (O13): that would add a second factor.
5. **Verdict code (O9).** The frozen script cannot express a 1-seed gate, n = 4, a conditional F−, or "F+ failed → inconclusive". A new FU_D verdict script is required. It reuses the frozen `stats.t_interval`, `relative_gain`, `hierarchical_bootstrap` and `gate_fixture` by import and owns the decision mapping. Its tests must target the V06–V11 classes.
6. **C4 (O10–O11).**
   - `train.run` writes `te.pseudonyms` into `run.json`.
   - Pointing it at the old-token directories would write unsalted tokens into the copied-back records, recreating r1 B1.
   - A symlink view `hNN → old directory`, built on b300-01 from the sealed manifest, together with the repo's sanitized split, makes every record positional from the start, with no sanitising afterwards.
7. **Seed rule (O12).** The rule is n = 5, else n = 4. n = 3 is excluded because its operating characteristics collapse when variance is inflated.

## 3. Caveats

- **Smoke conditions.** The smoke used synthetic tensors on one otherwise idle GPU. Real runs on a crowded b300-01, where FU-A/B/C/E also need the node-local HCP copy, may be slower: r1 saw +6 %. The seed rule therefore uses the measured wall time of the real F+ gate jobs, not my smoke.
- **No real-data numbers were produced.** Stall risk at E192 with lr 2e-4 and no tuning is unknown; r1 had one stalled S run. Whether 140k samples lets a 474 M-parameter model leave the predict-zero plateau is also unknown.
- **.101 and .103 were not inspected.** They timed out. Copying the 132.8 GB preprocessed arrays to other B300 nodes, to spread the load, is a root decision. It stays on B300, so it is not redistribution, but no one has ruled on it.
- **Shared ceiling.** O14 means FU_D may not get its full 25 GPU-h if other options use their full caps; root must arbitrate.
- **Other explorers.** I did not read the outputs of the other two FU_D explorers (independent work). One of them had a held smoke job (396) in the queue.
- **Tests not run.** I did not run the r1 test suites (no code change). C1 and the code freeze were checked.
- **B300 venv.** `/scratch/iitp4/worker_M3_r1/venv` was used read-only for my smoke. The worker should build its own env with `scripts/b300_env/build_env.sh` under `/scratch/iitp4/worker_FU_D/` or state the read-only reuse.

## 4. Conclusion — recommended strategy for worker_FU_D

**A. Card** (new, dated, e.g. `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fuD_card.md`). Frozen with a sha256 receipt in `results/topic2/2026-11-02_fuD/card_sha256.txt` **before any FU_D run, including the F+ gate**. It contains:
- **§0 Disclosure.** Every r1 result is known: I1 +0.147 % [−0.068, +0.361], per-seed values, a stalled S seed 2, the Stage-0 numbers. The prior expectation is `stop`. My synthetic smoke and probes are listed. No FU_D real-data number exists.
- **§1 Question.**
  - The E36 null might reflect model capacity: 288-d final token, about 1 % explained variance (addendum 05 §4.7).
  - Test: at E192 d2-2-18-2 (474,226,176 parameters, final token 1536-d), trained from scratch with SimMIM on the same data and budget, do connectome boxes at M0 lower held-out masked NMSE by ≥ δ = 1 % (decision 3)?
  - I1 = (E−C)/E and I2 = (S−C)/S, unit = seed, exactly as r1 §1 and §6.
- **§2 Single change from r1.** E192 cfg = `dict(img_size=(96,96,96,20), in_chans=1, embed_dim=192, window_size=(4,4,4,10), patch_size=(6,6,6,1), depths=(2,2,18,2), num_heads=(6,12,24,48), c_multiplier=2)`.
  - Every other setting is the r1 §5 value: lr 2e-4, wd 0.05, warmup 5 %, cosine, clip 1.0, bf16, batch 16, 8,750 steps, mask 0.6, seeds 1000+s / 2000+s / 3000+s, eval masks 7001/7002, val at 2188/4375/6562/8750, test once.
  - VRABES mask 0.8 is *not* adopted (it would be a second factor). Stated as a limitation: no tuning at E192.
  - M0 location and gather applicability are pinned by O5.
- **§3 Arms.** E, C, S with the r1 partitions byte-identical: `perms_hcp.npz` (file sha256, plus the per-key perm sha256 from `partitions_hcp.json`) and `perms_Fplus.npz` / `perms_Fminus.npz`. The S surrogate seed equals the training seed. No rebuild, so the train-only FC and Stage 0 are unchanged. Stage 0 is not rerun; r1 Stage 0 is cited as r1 output.
- **§4 Data.**
  - HCP-YA OA REST1_LR, the same 88-subject manifest (dev subjects already excluded) and the same split (64/8/16; sealed original sha c13b5f21…, sanitized repo copy).
  - Data stay on b300-01.
  - Only aggregates and per-subject num/den keyed by positional tokens leave B300.
  - Checkpoints (if saved) stay on B300.
  - No ENIGMA data. Residual linkage as disclosed in addendum 05 §3.
- **§5 Order and gate.**
  - (1) F+ gate at E192: E, C, S × seed 0, Fplus stream, full budget. Pass iff (E−C)/E ≥ δ **and** (S−C)/S ≥ δ, from the seed-0 values.
  - (2) If F+ fails → verdict `inconclusive` (measurement capacity); Stage 1 is not run.
  - (3) If F+ passes → seed plan (§10) → Stage 1.
  - (4) F− (E, C × seed 0) only if the Stage-1 rule outputs `keep` and 2c ≤ remaining cap. Pass iff (E−C)/E < δ.
- **§8 Verdict table**, applied in order:

  | condition | verdict |
  |---|---|
  | any planned run (gate or Stage 1) not `completed` after one rerun | `no_verdict` (software) |
  | F+ computed and failed | `inconclusive` (capacity), whether or not Stage-1 records exist |
  | F+ record missing while Stage-1 records exist | `no_verdict` (protocol), never a pass |
  | hi(I1) < δ (strict) | `stop` |
  | mean ≥ δ, lo(I1) > 0, lo(I2) > 0 | `keep` |
  | mean ≥ δ, lo(I1) > 0, lo(I2) ≤ 0 | `modify` |
  | anything else | `inconclusive` |
  | would-be `keep` with F− failed | `inconclusive` (bias flag) |
  | would-be `keep` with F− not run (cap) | `inconclusive` (keep pending F−) |

  F− never affects `modify` or `stop`. The kill criterion is the `stop` rule.
- **§9 Readings fixed in advance.** None of these changes the category.
  - (a) Scale manipulation check: if seed-mean NMSE_E(E192) ≥ 0.98892 (r1 E36 E mean), add the qualifier "scale did not raise the reconstruction ceiling".
  - (b) Stall = final val NMSE ≥ 0.999 and test NMSE ≥ 0.999. Valid run, counted per arm. Sensitivity analysis drops stalled seeds from all arms.
  - (c) Joint reading with r1:
    - stop/stop → null replicates at 12× parameters;
    - stop/keep → scale-dependent, connectome-specific gain;
    - stop/modify → scale-dependent gain, not FC-specific (compactness confound, addendum 05 §4.4).
  - (d) No pooling of r1 and FU_D seeds.
- **§10 Seed rule** (data-independent; computed by a tested script that writes `seed_plan.json` plus its sha256 before any Stage-1 launch):
  - c = 1.05 × max sacct Elapsed (h) of the 3 F+ jobs.
  - U = FU_D ledger GPU-h consumed so far (smokes and gate). R = 25 − U.
  - n = 5 if 16c ≤ R. Otherwise n = 4 if 13c ≤ R, using seeds {0,1,2,3}. Otherwise Stage 1 is not launched: verdict `not_run (cap)` plus a costed plan.
  - With the measured c ≈ 1.26 and U ≈ 3.9, R ≈ 21.1 and 16c = 20.2, so n = 5.
- **§10 Failures.** Software failures are a non-finite loss, a crash, `aborted_throughput`, Slurm TIMEOUT / NODE_FAIL / OOM, or a missing `run.json`. Each is rerun once with the identical command and stays in the ledger. Settings: `--max-run-hours 1.6`, Slurm `--time 02:00:00`.

**B. Code.** Only in FU_D's own paths, e.g. `scripts/topic2_fud_*.py` and `tests/topic2_fud/`.
- `topic2_fud_train.py`: registers the E192 cfg in `model.CONFIGS` at import (no `src` edit; O7), then calls the frozen `train.run`. It writes a sidecar `run_meta.json` with the wrapper sha256, the cfg dict, the Slurm job id and the node.
- `topic2_fud_posview.py` (stdlib, runs on b300-01): builds `/scratch/iitp4/worker_FU_D/hcp_pos/subjects/hNN` symlinks from the sealed manifest. It prints counts only and asserts that the sealed split maps exactly onto the sanitized split (O11).
- `topic2_fud_seed_plan.py`: implements §10.
- `topic2_fud_verdict.py`: reuses the frozen `stats` helpers and has its own decision function. The planned seeds come from `seed_plan.json`, never from the runs found. The loader raises an error on duplicate completed records for the same key, and asserts the same test-token order and `^h\d\d$` tokens.
- Slurm launcher: one sbatch per run, `--gres=gpu:1 --nodelist=b300-01 -p gpu`. Ledger rows (started and completed, with job id, GPU-h from sacct) go through `scripts/topic2_ledger.py --agent worker_FU_D`. Never use `topic2_launch_wave.py` (direct launch).

**C. Tests** (synthetic fixtures, CPU; each must fail on its defect). Verdict mutants:
- missing F+ counted as pass;
- failed or aborted runs counted;
- F− failure downgrading `modify`;
- F− not run counted as pass;
- boundaries hi == δ, lo == 0, mean == δ, F+ gain == δ, F− gain == δ;
- F+ fail with Stage 1 absent → `inconclusive`, not `no_verdict`;
- n read from the runs found instead of the plan;
- extra seed-4 runs used when n = 4;
- I1 and I2 denominators swapped;
- test-order assertion removed;
- duplicate run records.

Seed-plan rule tests at exact equality (16c == R → n = 5). Wrapper tests:
- the E192 stage table and parameter count;
- E init bit-identical to stock;
- C/S/E inits identical apart from the perm. Memory-heavy, so run them on connectome/B300 via srun, or pin O5's probe output.

C4 test: no 16-hex token or stray 64-hex digest under the FU_D results, docs and verification dirs. Run a mutation harness on the verdict and seed-plan scripts and require 0 survivors.

**D. Budget plan.**

| item | runs | GPU-h |
|---|---|---|
| explorer smokes | — | ≈ 0.03 + others |
| F+ gate | 3 | 3.6 |
| Stage 1, n = 5 | 15 | 18.4 |
| one rerun reserve | 1 | 1.23 |
| total | | ≈ 23.3 ≤ 25 |

The conditional F− (2.4) fits only if no rerun was needed; otherwise the pre-registered "keep pending F−" applies. Root must confirm that FU_D's 25 GPU-h is actually available under the 95 GPU-h ceiling (O14).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK'   # expect 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | grep -c ': OK'                      # expect 33
cat verification/explorer_FU_D_r1_1/smoke_e192.out.json        # 0.491 s/step, peak 198.27 GiB, proj 1.229 / 1.202 h
grep explorer_FU_D_r1_1 results/gpu_ledger_2026-10-31.md        # started + completed rows, Slurm job 404, 0.03 GPU-h
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B \
  verification/explorer_FU_D_r1_1/probe_e192_structure.py . results/topic2/2026-11-01/partitions/perms_hcp.npz /tmp/x.json   # ~4 GB RAM
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_D_r1_1/probe_frozen_verdict_misfit.py .
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_D_r1_1/power_seed_rule.py results/topic2/2026-11-01/verdict.json /tmp/p.json
# B300 (stdlib, CPU srun, counts only):
#   srun -p debug --nodelist=b300-01 -n1 -c2 --mem=4G python3 probe_b300_posmap.py /scratch/iitp4/worker_M3_r2/sealed_c4 <sanitized split.json> /scratch/iitp4/worker_M3_r1/hcp/subjects
```

Conditions that would overturn these conclusions:
- real F+ gate jobs take more than 1.5 h each (then n = 4 or not_run);
- an E192 job OOMs with other processes on the GPU (Slurm gres should prevent this);
- `/scratch/iitp4/worker_M3_r1/hcp` or `worker_M3_r2/sealed_c4` is removed (then re-preprocess with the frozen script and the sealed salt, under a new costed plan);
- root reassigns the 95 GPU-h ceiling.
