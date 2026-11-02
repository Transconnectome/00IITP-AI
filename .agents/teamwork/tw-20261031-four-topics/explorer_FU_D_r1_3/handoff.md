# handoff — explorer_FU_D_r1_3 (FU-D, Topic 2 follow-up D: E192 scale) — Hard handoff, 2026-11-01 ~15:25Z

**Summary.** The r1 design as written does not fit the 25 GPU-h cap at E192. That design is a 12-run training-loop fixture gate plus 15 Stage-1 runs, and the §7 estimate of about 20 GPU-h left out the gate. My Slurm smoke (synthetic only) measured E192 at batch 16 at 0.4776 s/step (33.5 samples/s), projecting about 1.19–1.22 GPU-h per run. Twelve gate runs plus 15 Stage-1 runs come to about 33 GPU-h. With a 1-seed F+ gate, 5 Stage-1 seeds, no F− unless needed, and one rerun in reserve, the total is about 23 GPU-h, which fits. The frozen r1 code applies unchanged at M0, the r1 partitions and split can be reused, and the frozen verdict script must not be reused as is.

## 1. Observation

| # | observation | evidence |
|---|---|---|
| O1 | M0 is `layers.0.downsample`. At E192 it is the only ConnectomeRGBoxPooling, with input_resolution (20,16,16,16) and Linear 1536→384 (LN 1536). The M0 grid is 16 and the octant edge 8, both the same as E36, so the r1 partitions `perms_hcp.npz` / `perms_F*.npz` (4096-long π) apply unchanged. Total parameters are 474,226,176; the decoder holds 210,110,976 of them (`decoder_spatial_expand` 1536→110,592). For seed 0, the parameter digests of arms E/C/S_seed0 are identical, and their state_dicts differ only in `layers.0.downsample.perm`. | `verification/explorer_FU_D_r1_3/p1_e192_build_pairing.py` → `.out.json` (local CPU, torch 2.11 dev) |
| O2 | `src/topic2_rgpool/model.py` CONFIGS has no E192 entry. The frozen `train.run` does `cfg = CONFIGS[a.cfg]`. Adding a key to `model.CONFIGS` at runtime is visible to train.run (same dict object), with no file edit. `run.json` stores only the cfg *name*, and `code_hashes()` covers only `src/topic2_rgpool/*.py`. | p1 `a_injected_visible_to_train: true`; train.py lines `cfg = CONFIGS[a.cfg]`, `code_hashes()` |
| O3 | The VRABES E192 extraction used embed 192, depth 2 2 18 2, heads 6 12 24 48, window 4 4 4 10, patch 6 6 6 1 and c_multiplier 2, **mask_ratio 0.8** and `last_layer_full_MSA True`. The vendored ver11 has no `last_layer_full_MSA` (an ignored kwarg). | `/home/juke/git/VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` lines 82–86; `grep` of the vendored file |
| O4 | Smoke, Slurm job 430 on b300-01, synthetic only. A random fp16 tensor of the r1 HCPSource shape (88×1200×78×96×84 = 123.8 GiB) was resident on the GPU, with frozen build_simmim + C perm + flash + bf16 + AdamW + clip, batch 16. Results: median 0.4776 s/step (p90 0.4778), 33.5 samples/s, peak 198.3 GiB of 267.7 GiB, eval 0.0104 s/window, projected 1.186 h for 8,750 steps + 2,880 eval windows + 60 s. Job Elapsed was 00:02:09. | `verification/explorer_FU_D_r1_3/p3_smoke_430.log`; ledger rows of explorer_FU_D_r1_3 |
| O5 | B300 /scratch is node-local (`/dev/md0 ext4`). The r1 preprocessed HCP (88 subjects, 126 G) exists only on b300-01 (= 61.107.201.98) at `/scratch/iitp4/worker_M3_r1/hcp`. b300-02/03/04 have 0 files in `/scratch/data/hcp/download_HCP_REST1_filtered` and no `/scratch/iitp4`. My first smoke (job 418), without `--nodelist`, was placed on b300-02 and FAILED in 1 s (directory missing). At 14:40Z, 6 FU smoke jobs were all running on b300-01. | srun `fud3_ls` jobs 393–395; sacct 418/430; squeue snapshot |
| O6 | The frozen `train.run` writes `rec["test_pseudonyms"] = list(te.pseudonyms)` into run.json. The B300 data dirs under `hcp/subjects/` are named by the ORIGINAL unsalted content-hash tokens (C4 B1 class). The repo `split.json` is sanitized (h00…h87; 64/8/16), and its lists are in the same order as r1 (`runs/hcp_E_s0/run.json` test list == split test). | train.py; `results/topic2/2026-11-01/split.json` check; addendum 05 §2 |
| O7 | The frozen `train.run` aborts at `--probe-steps` if the projected run hours exceed `--max-run-hours` (default **0.75**, from scripts/topic2_train.py). At E192, every run would abort at step 200 with status `aborted_throughput`. `scripts/topic2_launch_wave.py` launches directly on idle GPUs, with BASE hard-coded to `/scratch/iitp4/worker_M3_r1` and timeout 3300 s, so it is unusable under Slurm. | scripts/topic2_train.py, topic2_launch_wave.py |
| O8 | The frozen `scripts/topic2_verdict.py` on synthetic records (p2): 3 Stage-1 seeds → `no_verdict` (HCP_SEEDS hard-coded 0..4); F+ computed FAIL and no Stage 1 → `no_verdict "Stage 1 incomplete"` (card says inconclusive); F− runs absent and keep data → **keep** (`fm is not False`); one `aborted_throughput` → no_verdict; stale duplicate records with the same (source, arm, seed) in extra dirs → the verdict flips from what would be **stop** to **inconclusive** (the loader keeps the last glob-order record). | `verification/explorer_FU_D_r1_3/p2_frozen_verdict_hazards.py` → `.out.json` |
| O9 | r1 stall: `hcp_S_s2` stayed at the trivial solution (test NMSE 1.0000014), which counts as a valid run under card §5. Per-seed I1 tracks plateau-escape timing (addendum 05 item 5). The r1 per-seed I1 sd is 0.173 %, giving t half-widths of 0.430 / 0.275 / 0.215 % for n = 3 / 4 / 5 seeds. In the smoke, the synthetic training loss was still ≈1.001 at step 240. | addenda 04, 05; my computation |
| O10 | The r1 F+ gate passed by a wide margin in both seeds: E 0.6769/0.6803, C 0.6582/0.6575, S 0.6778/0.6776, so per-seed C-vs-E is about 2.8–3.4 % and C-vs-S about 2.9–3.0 %, against δ 1 %. | result report §2.2 |
| O11 | All 15 r1 E36 Stage-1 checkpoints (`model_final.pt`) are still on b300-01. The sealed original split is at `/scratch/iitp4/worker_M3_r2/sealed_c4/...` and the r1 original manifest at `/scratch/iitp4/worker_M3_r1/hcp/manifest.json`; I checked existence only and read neither. GATE_STATUS lists cleanup of `/scratch/iitp4/worker_M3_r1` as a pending root action. | ssh existence checks |
| O12 | C1 rc 0; code_sha256_at_freeze rc 0; output_sha256_r2 all OK; c4_sanitized 19/19; whole-run audit_layout findings []. | commands in §5 |
| O13 | Infrastructure: B300 sshd intermittently times out at banner exchange or drops mux connections. One sbatch was silently not submitted twice. A detached remote `setsid … sbatch > jobid.txt` and `ControlMaster=no` worked. | session log |

## 2. Logic chain

1. Cost (O4): c ≈ 1.19 h of train+eval at 33.5 samples/s, plus about 20 s of real data load and Slurm/startup, so c ≈ 1.20–1.25 GPU-h. The §7 figure of 1.36 h came from 28.6 samples/s at bs4; bs16 is about 17 % faster.
2. The r1 machinery has 12 gate runs and 15 Stage-1 runs: 27 × 1.22 ≈ 33 GPU-h, more than the 25 cap. **§7's "≈20 GPU-h" excludes the gate.** F1 requires the r1 gates "where applicable". A stop at E192 is only interpretable if the E192 model/budget can convert a planted grouping into ≥ δ (otherwise it is a false kill). So F+ must be re-run at E192, and the card has to cut the cost elsewhere.
3. F− only downgrades keep (S.verdict). r1 makes keep unlikely, so F− can be conditional. F+ passed by about 3× δ in each r1 seed (O10), so a 1-seed F+ gate is reasonably powered. The gate's noise is smaller than the Stage-1 seed noise that sets the primary interval (O9: n 5→4 widens the half-width by 28 %).
4. Recommended arithmetic at c = 1.22: F+ (E, C, S × seed 0) = 3 runs; Stage 1 = 15; reserve 1 rerun; smoke 0.25. That is 19 × 1.22 + 0.25 = 23.4 ≤ 25. A seed-reduction formula is needed in case c is higher (the table in §4).
5. O1 means the intervention is truly unchanged at E192: same π, same box gather and same pairing; only width, depth and heads differ. So the option's single change is scale, and the r1 Stage-0 and partitions need no recomputation.
6. O5 + O6 together create a C4 trap. To use the only copy of the data, the worker must map h-tokens to the original-token dirs on B300. If it passes the original tokens to train.run, every run.json carries B1-class tokens. A positional symlink tree is needed, plus a pre-copy scan.
7. O7: unless max_run_hours, sbatch --time and the launcher are re-specified in the card, every run fails, and the failure becomes no_verdict.
8. O8 means FU-D needs its own verdict orchestration, and must test it against the listed defect classes. The 5 classes named in the dispatch, plus the seed-set and duplicate-record classes, are all observable today on the frozen script.
9. O9: at 474 M parameters, plateau risk is plausible. A stalled E inflates I1 and a stalled C deflates it, and if all arms stall the result is a tight "stop" that only reflects measurement incapacity. A pre-registered real-data capacity floor and a stall-robustness rule are required before any result.

## 3. Caveats

- The smoke used synthetic random tensors. The real per-run cost adds data load from disk (r1: 21 s for 133 GB), validation and test on real data, and Python startup. Contention from co-scheduled jobs on b300-01 (shared PCIe/host) was not measured. My 1.19 h figure is a projection from 240 steps, not a full run.
- Peak memory was 198 GiB of 268 GiB. A co-tenant job on the same GPU, which Slurm prevents with `--gres=gpu:1`, or any extra resident tensor, could cause an OOM.
- I did not read the other FU-D explorers' outputs, by design. Job 404 `fuD_e192_smoke` and job 396 `fud_smoke_expl2` belong to them, so their numbers may differ.
- Power: the r1 sd is E36. E192 seed variance is unknown, and could be larger if plateau escape varies.
- I did not verify that the r1 preprocessed arrays are byte-unchanged since r1. I propose a checkpoint re-evaluation check for that (§4 E below).
- The local torch (2.11 dev) differs from B300 (2.15). Bit-identity across arms holds within either version; I checked it on CPU only.
- The C4 residual linkage of positional tokens (addendum 05 §3) also applies to FU-D per-subject arrays. It is disclosed, not solved.
- B300 ssh flakiness is real and may cost the worker time (O13).

## 4. Conclusion — recommended worker strategy (FU-D), in order

**A. Paths (new code only in own paths).**
- `src/topic2_fud/` (or `scripts/topic2_fu_d/`, a directory, so the r1 `scripts/topic2_*.py` glob is not polluted), `tests/topic2_fud/`, `results/topic2_fud/2026-11-0X/`, `docs/03_empirical_analysis/topic2/2026-11-0X_topic2_fud_card.md`.
- Import `src.topic2_rgpool` read-only. Never add to `tests/topic2_rgpool` (the M3 r3 team owns it).

**B. Card (freeze with a sha256 receipt in its results dir BEFORE any E192 training run, gate runs included).** State:
- **Change:** CONFIGS key `E192_d22182` = embed 192, depths (2,2,18,2), heads (6,12,24,48), window (4,4,4,10), patch (6,6,6,1), c_multiplier 2, img 96³×20. Expected n_params 474,226,176. **Everything else stays at r1 values:** mask 0.6 (not VRABES 0.8; no last_layer_full_MSA), lr 2e-4, wd 0.05, warmup 5 %, cosine, clip 1.0, bf16, 8,750 steps × batch 16 = 140k samples, seeds and eval masks as r1.
- **Data:** the r1 split (repo sanitized `split.json`, sha pinned in `c4_sanitized_sha256.txt`), the r1 manifest (dev subjects already excluded; do NOT rerun preprocessing and do NOT touch the sealed salt), and the r1 partitions `perms_hcp.npz` (ec05b796…) and `perms_Fplus.npz` / `perms_Fminus.npz`, all verified by sha before use.
- **Disclosures (card §0):** D was chosen after the r1 result was known. The test set is the same 16 subjects as r1, so this is not an independent replication. I2 is confounded with box compactness (addendum 05 item 4).
- **Gate:** F+ = E, C, S × seed 0 at the full budget. Pass iff (E−C)/E ≥ δ **and** (S−C)/S ≥ δ. If F+ is computed and fails, verdict = **inconclusive (measurement capacity)** and Stage 1 is not run. If an F+ run fails twice, verdict = no_verdict. Stage 1 starts only after F+ passes.
- **F− (conditional, pre-registered):** run only if the Stage-1 primary rule yields keep and the remaining FU-D budget is ≥ 3c (E, C, S × seed 0). If F− fails, keep → inconclusive. If keep and F− cannot be run, verdict = **inconclusive (bias gate not run)**. F− never affects modify, stop or inconclusive.
- **Seed rule (pre-registered; uses only measured cost):**
  - c = mean sacct GPU-h of the completed F+ gate runs, × 1.02 (margin for the real-data load).
  - Spent = all FU-D ledger GPU-h so far, including the smoke.
  - n = the largest n ∈ {5, 4, 3} with spent + 3n·c + c (one rerun reserve) ≤ 25.
  - Seeds are {0..n−1}, with S surrogate key `S_seed{s}`.
  - If n < 3, Stage 1 is not launched; deliver the card, code, gate and a costed plan, and report.
  - Record c, spent and n in a dated receipt before the first Stage-1 submit.
  - Expected at c ≈ 1.22: n = 5.

  | c (GPU-h per run) | total with n = 5 | n chosen |
  |---|---|---|
  | 1.20 | 23.1 | 5 |
  | 1.30 | 24.9 | 5 |
  | 1.36 | — | 4 (22.0) |
  | 1.60 | — | 3 (21.1) |
- **Capacity floor and stall rules (pre-registered):**
  - A run is stalled iff its final val NMSE is ≥ 0.999 and its last-100 train loss is ≥ 0.999.
  - Stalled runs are valid (as in r1).
  - Verdict = inconclusive (measurement capacity, real data) if (a) the seed-mean E NMSE is ≥ 0.999, or (b) more than 1 of the 3n Stage-1 runs is stalled, or (c) the verdict category changes when the seeds containing a stalled run are dropped. Rule (c) is reported, not applied, if fewer than 3 seeds would remain.
- **Run integrity:**
  - `--max-run-hours 1.8`, probe at step 200.
  - sbatch `--time=02:30:00 --nodelist=b300-01 --gres=gpu:1 --mem≥96G --exclusive` is optional but must be stated.
  - Software failure = any status other than completed (crash, nonfinite, aborted_throughput, Slurm TIMEOUT/OOM/NODE_FAIL, run.json still "started"). A failed run is rerun once in a new dir with an `_a1` suffix, and both runs are kept in the ledger. A second failure → no_verdict.
- **Inference and verdict:** identical to r1 card §8 (t over seeds with df n−1, δ = 0.01 per PI decision 3, stop iff hi < δ strictly, keep/modify/inconclusive as r1). The hierarchical bootstrap is secondary.

**C. Launcher and provenance (new code).**
- The sbatch wrapper imports the frozen `train.run`, injects the E192 config, and passes the card hyperparameters explicitly.
- Before the run it writes a sidecar `fud_meta.json` with: the cfg dict; the sha256 of the wrapper, sbatch file and split, perm and fixture files; the Slurm job id and node; `CUDA_VISIBLE_DEVICES`.
- After the run it asserts `run.json n_params == 474226176` and that code_sha256 equals the r1 freeze list.
- Pin all FU-D code in its own `code_sha256_at_freeze.txt` at card freeze.

**D. C4 data path (critical).**
- On b300-01, in memory only, build the h-token ↔ original-dir map from the original r1 manifest order (h%02d = index in the content-hash-sorted list; check against addendum 05 §2 and the sealed split zip).
- Create `/scratch/iitp4/<worker>/hcp_pos/subjects/hNN → …/worker_M3_r1/hcp/subjects/<orig>` symlinks. Never `ls -l`, print or copy that tree's targets.
- Run train.run with `--data-dir hcp_pos --split-file <repo sanitized split.json>`. run.json then carries h-tokens and `split_file_sha256` = the sanitized pin.
- Before any copy back to the repo, run a count-only scan on B300 for the original tokens, the HCP directory names and the content hashes (held in memory). Then run the local FU-D guard test: the r2 `test_c4_tokens_r2` detector logic applied to `results/topic2_fud`, the FU-D verification dir and the FU-D metadata.
- Because `/scratch/iitp4/worker_M3_r1` may be cleaned by root (O11), ask root to hold that cleanup until FU-D finishes, or copy the 126 G to the worker's own b300-01 dir with a per-file sha256 check kept on B300.
- **Never** copy the original manifest, the sealed split or the salt into the repo.

**E. Data/pipeline-equivalence check (cheap, ≤ 0.05 GPU-h, before the gate).**
- Re-evaluate one r1 E36 checkpoint (for example `hcp_E_s0/model_final.pt`) through the FU-D positional data tree with frozen `evaluate_hcp` on TEST with seed 7002.
- It must reproduce r1 `test_nmse` 0.9908706340280367 exactly (the r1 auditor got bit-identical results).
- This proves that the positional tree = the r1 data and order, and that eval is unchanged. It is not an E192 result, and it should go in the card's §0 as a pre-freeze check, or be done right after the freeze.

**F. FU-D verdict code (own path; reuses `S.t_interval`, `S.relative_gain`, `S.hierarchical_bootstrap`, `S.gate_fixture`, `S.verdict` by import).** Required behaviour, each with a synthetic test and a mutant that the test kills:
1. The required run set comes from the frozen card config and the n receipt, not from a glob. Unknown dirs and duplicate (source, arm, seed) records are errors. Reruns resolve only per rule B (O8 S5).
2. Software-failure statuses count as failed (never as completed) → rerun → no_verdict (V08/V10).
3. F+ missing or failed-run → no_verdict. F+ computed fail → inconclusive, and Stage 1 is not read (V07, case A).
4. F− only touches keep. If F− is absent and the result is keep → inconclusive "bias gate not run". F− never touches modify (V06; O8 S3).
5. Boundaries: stop iff hi < δ; keep/modify iff mean ≥ δ and lo > 0; I2 lo > 0 is strict; F+ gains ≥ δ (V01–V05).
6. Test order equal across runs (V09).
7. NMSE is recomputed from Σnum/Σden and cross-checked against `test_nmse`.
8. The n_params / cfg sidecar assert.
9. The stall/floor rules of B.
10. Seed counts of 3/4/5 give t df 2/3/4.

Also run the frozen r1 verdict on r1 data as a regression (verdict.json reproduced).

**G. Execution order.**
1. Card + code + tests.
2. Freeze and pin.
3. The E check.
4. F+ gate (3 jobs in parallel, ledger start/close rows with job ids; GPU-h from `sacct Elapsed × AllocTRES gpu`).
5. Compute the gate; write the c/n receipt.
6. Stage 1, with 3n jobs pinned to b300-01, the arms of one seed submitted together.
7. Copy back after each wave (scratch is volatile).
8. C4 scans.
9. Verdict.
10. Result report: verdict per FU-D card, stated as adding to (not re-reading) the r1 stop; the scale-robustness reading; deviations in dated addenda.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?   # 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | tail -1                               # all OK
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_D_r1_3/p1_e192_build_pairing.py /tmp/p1.json   # n_params 474226176, digests equal, only perm differs
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_D_r1_3/p2_frozen_verdict_hazards.py /tmp/p2.json   # S1 no_verdict, S2 no_verdict, S3 keep, S4 no_verdict, S5 inconclusive
grep explorer_FU_D_r1_3 results/gpu_ledger_2026-10-31.md                                                          # 4 rows, 0.037 GPU-h total
# on B300: sacct -j 418,430 -X -o JobID,State,Elapsed,NodeList ; my /scratch/iitp4/explorer_FU_D_r1_3 was removed after the smoke
```

Invalidation:
- A worker smoke with real data loading showing c > 1.30, which changes n (the rule handles it).
- Any change to src/topic2_rgpool, which breaks the code pin.
- Root cleaning `/scratch/iitp4/worker_M3_r1` before FU-D copies or uses the data.
- HCP data appearing on other nodes, which would remove the b300-01 queue bottleneck.
