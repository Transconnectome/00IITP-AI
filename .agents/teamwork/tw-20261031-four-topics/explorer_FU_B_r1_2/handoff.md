# handoff — explorer_FU_B_r1_2 (FU-B: Topic 2, 4x budget, E36, arms E/C/S, 5 seeds; cap 33 GPU-h)

**Summary.** FU-B fits the cap, but only with a resumable training loop or without a 4x fixture gate. The frozen r1 code at `--steps 35000` projects **1.703 GPU-h per run** (measured on Slurm, b300-01, job 402). So the 15 Stage-1 runs cost ≈ 25.8 GPU-h. A 4x F+ gate on seed 0 (arms E/C/S) adds 5.2 GPU-h, which leaves ≈ 1.5 GPU-h: enough for about 11 resumes from checkpoints, but not for one restart from scratch. The frozen `scripts/topic2_verdict.py` cannot be reused for FU-B. On FU-B-shaped trees it reports a missing gate as a failed gate, and it gives no_verdict where the card says inconclusive (p02).

Lens: feasibility and failure modes. I wrote no production code and made no git writes. GPU use: 0.06 GPU-h, ledgered (Slurm job 402).

## 1. Observation

| id | observation | evidence |
|---|---|---|
| O1 | Frozen loop `src/topic2_rgpool/train.py` `run()` has **no checkpoint or resume**. It saves only `model_final.pt` (with `--save-model`) at the end. The RNG and order state lives in local variables: `g_order` (1000+s), `g_mask` (2000+s), `g_fix` (3000+s, device), `order`, `pos`, `run_loss`. | train.py:176-215 |
| O2 | The LR schedule stretches with `--steps`: `lr_at(step, steps, peak, warmup_frac)`. Eval steps = round(steps·{.25,.5,.75,1}). At 35,000 steps: warmup ends at 1,750; val at 8,750/17,500/26,250/35,000. lr at 8,750 = 1.789e-4, whereas r1 ended at 8,750 with lr 0. | train.py:46-50,180; p01.out.json c_schedule_35000; smoke log A: lr at step 100 = 1.1429e-05 |
| O3 | **Measured on Slurm (job 402, debug, -w b300-01, 1 GPU, frozen code, real HCP view):** 0.1745 s/step (91.7 samples/s); projected run 1.703 h for 35,000 steps; data load 19.4 s; val pass ≈ 2–3 s; test pass ≈ 5 s; host RSS 2.4 GB; **peak GPU memory 151,874 MiB** of 275,040; checkpoint (model + AdamW + RNG) 466,132,855 B, save 0.43 s, load 0.21 s, round-trip equal. sacct ElapsedRaw 198 s → 0.06 GPU-h. | verification/explorer_FU_B_r1_2/b300_smoke/out/{logs/smoke_402.out, runs/A_proj35k_C_s0/train_log.jsonl, runs/B_full400_C_s0/train_log.jsonl}; ledger rows 40, 44 |
| O4 | r1 per-run wall time: hcp 1,544–1,656 s, fixture 1,507–1,541 s at 8,750 steps. With 8 concurrent jobs on .98 the rate was 0.1757 s/step, so co-location costs about 1 %. Fixture runs cost as much as HCP runs. | results/topic2/2026-11-01/runs/*/run.json, hcp_E_s0/train_log.jsonl |
| O5 | The frozen loop is **bit-deterministic on CPU** (tiny_test, Fplus stream): test_num, test_den, test_nmse, val curve and train loss are all equal over 2 runs, at 5.3 s per run. A naive resume that re-seeds `g_mask` gives different masks. Restoring the generator state gives identical masks. | p01.out.json a_*, b_* |
| O6 | HCP-YA OA **raw and preprocessed data exist only on b300-01** (= 61.107.201.98 = cloud-S1HDe3 = 192.168.0.2). Raw is in /scratch/data/hcp/download_HCP_REST1_filtered (1,084 dirs). The r1 preprocessed set is in /scratch/iitp4/worker_M3_r1/hcp (88 subject dirs, 126 GB, 1.51 GB bold_z_fp16.npy each). b300-02/03/04 have neither /scratch/data/hcp nor /scratch/iitp4. /scratch is a node-local md0 ext4 with 24–28 TB free. | ssh probes 14:2x–14:3xZ |
| O7 | Slurm: PreemptMode OFF. gpu partition MaxTime 2 d, default 4 h. interactive 4 h. debug 30 min. DefMemPerCPU 9,500 MB. select/cons_tres CR_CORE_MEMORY. **QoS normal MaxTRESPU gres/gpu=8 for user connectome**, shared by IITP, GARD and SwiFT; a `whole` QoS (32 GPUs) exists. sacct prints KST. ACCEPTANCE addendum ~23:3x: run squeue before every submission; do not submit while any `g3t-G-E0-*` job is PENDING or RUNNING. | sinfo/scontrol/sacctmgr output; ACCEPTANCE.md tail |
| O8 | Positional-token view check on B300: mapping the r1 original split through t(p) = 'h%02d' % (position in the r1 manifest subject list) reproduces the repo's sanitized `split.json` exactly (train/val/test: True/True/True; 64/8/16). The manifest list is sorted, unique, 16-hex and equal to the subject dirs. The run.json of the 400-step run has test tokens all of the form `^h\d\d$`, equal to the split test list. Copied-back records contain 0 16-hex strings. | b300_smoke/out/token_check.txt; make_token_dir.py stdout in transcript |
| O9 | The frozen verdict script hard-codes `FIX_SEEDS = (0, 1)` and both gates. On FU-B-shaped synthetic trees: K1 (F+ at 4x, seed 0 only, passing) → `inconclusive`, reason "gate failed": a missing gate is reported as a failure. K3 (no fixture runs) → the same. K4 (F+ fails, no Stage 1) → `no_verdict`, but card §7.2 says inconclusive (case A). The script also has `fm is not False`, so a missing F− counts as a pass (case D in challenger_M3_r2_2). | p02.out.json; scripts/topic2_verdict.py:18,46-62,66 |
| O10 | `stats.verdict()` maps correctly when it gets correct booleans: stop if hi < δ; keep/modify need mean ≥ δ and lo > 0; keep needs I2 lo > 0; an F− failure downgrades only keep. The r1 defects are in the script's wiring. | src/topic2_rgpool/stats.py:59-79 |
| O11 | perms_hcp.npz sha ec05b796… (pinned in output_sha256_r2.txt:26) has keys E, C and S_seed0–4 (+G, R, nvox, group_mask). The r1 runs used perm_key E/C/S_seed{s} with perm sha prefixes b83e23eb/21e4e239/(01db6af0, 480b16bb, a6dbf915, 82d004cc, 54027260). The sanitized split sha is cc521b08… (pinned). | p-run inspection above |
| O12 | r1 learning dynamics: train loss stays ≈ 1.0 until about step 4,000 of 8,750, then falls in the low-LR phase. hcp_S_s2 never left the trivial solution (test NMSE 1.0000015). | runs/hcp_*_s*/train_log.jsonl |
| O13 | Local checks: C1 PROTECTED_HASHES rc 0. code_sha256_at_freeze.txt 33/33 OK. The 15 frozen files in my B300 bundle match the freeze hashes, and the bundle sha is identical on B300. | transcript |
| O14 | ssh to .98 failed at banner exchange 4 times between 14:45 and 15:00Z, while TCP 22 was open from connectome. .99 worked, and `srun -p debug -w b300-01` from .99 worked (CPU cleanup step). | transcript |
| O15 | Ledger: other FU-B explorers used Slurm job 413 (0.065) and job 419 (cap 0.25). Completed rows across the run sum to 12.45 GPU-h before job 419 closed. | results/gpu_ledger_2026-10-31.md rows 49-57 |

## 2. Logic chain

1. From O3/O4, per-run cost ≈ 1.70–1.72 GPU-h. Stage 1 (15 runs) ≈ 25.8. A full r1-style gate at 4x (12 runs) adds 20.6, for 46.4 in total, above 33. So the r1 gate design cannot be copied at 4x.
2. Explorer probes take ≤ 0.375. A worker GPU resume smoke takes ≈ 0.15. With a 4x F+ gate (seed 0, E/C/S: 5.16), the total is ≈ 31.5 and the headroom ≈ 1.5 GPU-h. That is less than one from-scratch rerun (1.72). The gate is therefore affordable only if failures are recovered by **resume from checkpoint**. With a 2,500-step cadence (O3: 466 MB, 0.43 s per save), one failure costs at most 0.12 GPU-h of lost steps plus 20 s of reload.
3. From O1, resume needs a new loop in FU-B's own path; the frozen `run()` cannot be patched. From O5, a CPU tiny fixture can prove two things bit-exactly: the new loop with no interruption equals the frozen `train.run`, and interrupt plus resume equals the continuous run. Each test costs about 5 s. The defect "RNG/order state not restored" is detectable (O5 b).
4. From O2, `--steps 35000` with the frozen `lr_at` already gives the natural 4x recipe: one cosine over 35k with 5 % warmup, same peak and no restart. Intermediate val points are not replicates of r1's endpoint, because the LR has not annealed there.
5. From O6/O8, FU-B can reuse the r1 preprocessed set, which already excludes the 5 burned dev subjects, through a positional-token view (h00–h87). That view reproduces the repo's sanitized split exactly. Run records then carry only positional tokens. There is no need to re-run preprocessing, which would need the sealed salt and would recreate unsalted pseudonyms.
6. From O6/O7, every HCP job must be pinned to b300-01 (`-w b300-01`), one run per GPU (O3: 148 GiB). The QoS limit of 8 GPUs per user is shared by three projects, plus the g3t-G-E0 rule. Wall-clock time is therefore the binding resource, not GPU-h.
7. From O9/O10, FU-B needs its own verdict wiring with tri-state gates (pass / fail / missing) and explicit precedence. It can import `stats.t_interval`, `relative_gain`, `hierarchical_bootstrap` and `verdict`, but must not use `scripts/topic2_verdict.py`.
8. From O12, the 4x run has a longer high-LR phase. Stalls like hcp_S_s2 can recur. The card must fix their treatment in advance: a valid outcome, a descriptive stall flag, and a non-governing sensitivity analysis, with no rerun.

## 3. Caveats

- GPU determinism of training was not measured. A resumed GPU run is expected to be statistically equivalent, not bit-identical. Only the CPU equivalence is proven (O5).
- Throughput was measured with 1 job on an idle node. r1 data suggest about 1 % slowdown at 8 concurrent jobs (O4); not re-measured under GARD/SwiFT co-location.
- I did not check `~/.local/bin/uv` and network access for a fresh env build on b300-01. I used the r1 venv read-only (`-B`) for the smoke. The worker should build its own env.
- I did not measure whether 4x training changes the F+ fixture margin (+3.06 % at 1x). That is exactly what the 4x F+ gate measures.
- I cannot judge whether a pending job array submitted before a `g3t-G-E0-*` job appears violates the sharing rule. Root should decide.
- Peer explorers' reports were not read, by design (independent work).
- The B300 sshd on .98 is flaky (O14). Use .99 as the login node, or one ControlMaster session.

## 4. Conclusion: recommended strategy for worker_FU_B

### 4.1 Card: docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md

Freeze the card, with sha256 in results/topic2/2026-11-02_fu_b/card_sha256.txt and code_sha256_at_freeze.txt, before any real-data FU-B number. It must state:

- **Change.** steps 8,750 → 35,000 (batch 16, 560k samples, ≈ 73.5 passes over the 7,616 training windows vs 18.4).
- **Identical to r1.** Model E36_d2262; arms E/C/S with perm keys E/C/S_seed{s} from perms_hcp.npz (sha ec05b796…); seeds 0–4 (init s, order 1000+s, mask 2000+s); eval masks 7001/7002; peak LR 2e-4, AdamW, wd 0.05, clip 1.0, bf16, mask ratio 0.6; data = r1 88-subject preprocessed set with sanitized split (sha cc521b08…), so dev-subject exclusion is inherited. No early stopping, no model selection.
- **LR schedule.** One cosine over 35,000 steps through the frozen `lr_at`: linear warmup over 5 % (1,750 steps), decay to 0 at step 35,000, no restart, peak not tuned. Record lr at steps 1/1750/8750/17500/26250/35000 in run.json. State that the val points at 8,750 etc. are not r1 replicates.
- **Checkpoint cadence.** Full training state (model, AdamW, step, order, pos, g_order/g_mask/g_fix states, run_loss tail, val curve so far, lineage keys) every 2,500 steps, plus at the final step. Atomic write (tmp + os.replace + sha256 sidecar). Keep the last 2. Final `model_final.pt` kept on B300.
- **Gate (§7.2 analogue at the 4x budget).** F+ fixture, seed 0, arms E/C/S, same 35k recipe, run first. Rule as r1: (E−C)/E ≥ δ AND (S−C)/S ≥ δ. If F+ fails → `inconclusive` (measurement capacity at 4x); Stage 1 is not launched; costed plan. If the F+ runs are incomplete after failure handling → `no_verdict`. **F− at 4x is not run within the cap.** A would-be `keep` is reported as `inconclusive` (bias check at 4x not done, fail closed). The 1x F− pass of r1 is cited beside it, and the 5.2 GPU-h F− check is requested from the PI. `modify` and `stop` are not affected by F−.
- **Metric and verdict.** As r1 §6/§8: δ = 0.01 (PI decision 3); t(df 4) is primary, hierarchical bootstrap secondary. Precedence: (1) F+ missing → no_verdict; (2) F+ fail → inconclusive; (3) any of the 15 hcp runs missing or failed → no_verdict; (4) stop if I1.hi < δ (strict); keep if I1.mean ≥ δ and I1.lo > 0 and I2.lo > 0; modify if I1 survives and I2.lo ≤ 0; otherwise inconclusive; (5) keep without a 4x F− pass → inconclusive.
- **Failure handling.** A software failure is any of: Slurm FAILED / TIMEOUT / NODE_FAIL / OUT_OF_MEMORY / unexpected CANCELLED; non-finite loss; throughput abort (projected > 2.2 h at step 300); GPU-busy pre-check abort. Response: resume from the latest valid checkpoint, at most 2 resumes per run. If no valid checkpoint exists, restart from scratch once, only if ledger plus projection stays ≤ 33. Otherwise the run is missing → `no_verdict`. Never `inconclusive` for a software failure, and never a verdict on partial seeds.
- **Stalls.** A completed run with test NMSE ≥ 0.9995 is a valid outcome and is counted. A non-governing sensitivity analysis drops seeds with any stalled arm. Stalls never trigger reruns.
- **Cap rules.** Before every submission, check: FU-B ledger sum + Σ projected for remaining runs ≤ 33, and run total ≤ 95. Otherwise do not launch → no_verdict + costed plan.
- **VM stop / scratch wipe.** Incomplete seeds → no_verdict unless the data are re-staged within the cap.
- **Joint reading vs r1 (descriptive only).** Per-seed paired I1(4x) − I1(1x) (same seeds and inits). A table of readings for stop/stop, keep/stop and so on, stated before results.

### 4.2 Code (own paths only; frozen code imported, never edited)

- `src/topic2_fu_b/train_resumable.py`: imports `HCPSource`, `FixtureSource`, `evaluate_hcp`, `evaluate_fixture`, `lr_at`, `build_simmim`, `D.simmim_masks` and `masked_sq_terms` from src/topic2_rgpool. It reproduces the frozen `run()` order of RNG calls exactly, and adds checkpoint/resume plus run.json fields (`code_sha256` of both packages, `resume_events`, `slurm_job_ids`, `lr_trace`, `attempt`).
- `src/topic2_fu_b/verdict.py`: tri-state gate loader. Reject duplicate (source, arm, seed) keys. Use only `status == "completed"`. Assert identical test-token order equal to split.test. Wire into `stats.verdict` with `fminus_gate_pass = (fminus_status == "pass")`.
- `scripts/topic2_fu_b_train.py`, `scripts/topic2_fu_b_verdict.py`, `scripts/topic2_fu_b_make_view.py` (B300, stdlib: hard-links `os.link` named h00–h87 into /scratch/iitp4/worker_FU_B_r1/hcp_view; prints counts only; template = verification/explorer_FU_B_r1_2/b300_smoke/make_token_dir.py, but with hard links instead of symlinks), `scripts/topic2_fu_b_submit.py` (squeue g3t-G-E0 guard + cap guard + ledger start row), `scripts/topic2_fu_b_close.py` (sacct ElapsedRaw × gres/gpu → closing ledger row, UTC converted from KST).
- Env: `bash scripts/b300_env/build_env.sh /scratch/iitp4/worker_FU_B_r1`, then `diff` of pip freeze against scripts/b300_env/lock.txt must be empty.

### 4.3 Fixtures that must fail on the targeted defect (tests/topic2_fu_b/, CPU, tiny_test)

| id | targeted defect | fixture / pass rule |
|---|---|---|
| T1 | new loop ≠ frozen loop | `train_resumable.run(ckpt_every=0)` vs frozen `train.run`, Fplus and fake-HCP (pattern: tests/topic2_rgpool/test_pipeline_guards_r2.py `_args`, `_tiny_perm_file`, fake HCPSource): test_num/test_den/val curve/train loss bit-equal |
| T2 | g_mask not restored | interrupt at step k (exception after the checkpoint) → resume → bit-equal to continuous (O5 shows a reseed differs) |
| T3 | g_order/order/pos not restored | as T2, with k chosen to straddle an epoch boundary (len(pairs)/batch steps) |
| T4 | g_fix (device generator) not restored | as T2 on the Fplus source |
| T5 | AdamW state not restored | as T2: compare final params |
| T6 | schedule restarted at resume / hard-coded 8,750 | lr_trace equals `lr_at(s, steps, …)`; warmup end = round(0.05·steps) |
| T7 | val entries lost or duplicated at resume | curve keys == frozen eval steps exactly |
| T8 | wrong-lineage checkpoint accepted | a checkpoint whose arm/seed/perm_sha/cfg/steps differ → refuse |
| T9 | truncated/partial checkpoint loaded | a truncated latest file → sha mismatch → fall back to the previous one or refuse; never load it |
| T10 | resume after the final step re-evaluates or overwrites | status stays completed; test eval runs once |
| V1–V5 | boundaries (>= vs >) | dyadic values (δ = 0.0625, E = 1.0, C = 0.9375) and interval dicts with exact lo/hi/mean at δ or 0: stop needs hi < δ; survive needs mean ≥ δ and lo > 0; keep needs I2.lo > 0; F+ ≥ δ passes; F− < δ passes |
| V6 | F− failure downgrades modify | modify pattern + F− fail → modify |
| V7 | missing F+ counted as pass | F+ runs absent → no_verdict (not keep/stop) |
| V7b | missing F+ reported as failed | F+ absent → reason says missing, verdict no_verdict (kills the p02 K1/K3 behaviour) |
| V8/V10 | failed runs counted | one hcp or F+ run with status ≠ completed → no_verdict |
| V9 | test-order check removed | permuted test tokens in one run → error / no_verdict |
| V11 | stop kept when F+ fails | F+ fail + Stage-1 stop pattern → inconclusive |
| VA | case A | F+ fail, no hcp → inconclusive (not no_verdict) |
| VD | case D | F− absent + keep pattern → inconclusive |
| VE | duplicate run dirs | two records with the same key → refuse |
| VS | stalled run dropped | a completed run with NMSE 1.0 is counted in the primary |
| D1/D2 | token leak | view build reproduces the sanitized split; every run.json test token matches `^h\d\d$` and equals split.test; no `[0-9a-f]{16}` in any FU-B output |
| L1/L2/L3 | ledger/cap/sharing | GPU-h from sacct; submission refused if cap would be exceeded; submission refused if a fake squeue shows `g3t-G-E0-x PENDING` |

Run a mutation harness over its own verdict and resume modules (text-edit mutants, one per row). It needs 0 survivors or a written equivalence proof. At most 2 pytest processes, timeout 900.

### 4.4 Slurm and logistics

- Login via .99 when .98 is flaky.
- Jobs: `-p gpu -w b300-01 --gres=gpu:1 -c 4 --mem=64G --time=02:30:00`. In-job pre-check: the allocated GPU must show 0 compute apps and < 1 GiB used (O3: a run needs 148 GiB).
- Order:
  1. one worker GPU smoke on the debug partition, ≤ 0.15 GPU-h (600-step run, kill at about 450, resume, and compare with an uninterrupted run);
  2. F+ gate, 3 jobs;
  3. after the gate passes, 15 Stage-1 jobs, throttled to the GPUs left under the 8-GPU user QoS (e.g. 3–5).
- Copy each completed run.json and train_log back to results/topic2/2026-11-02_fu_b/runs/ right away. HCP never leaves B300.
- Run the C4 scan (scripts/topic2_id_scan.py logic, HCP names held in memory on B300) over all FU-B outputs before the report.
- Wall-clock: gate ≈ 1.75 h, then ceil(15/k) × 1.72 h. With k = 4 that is ≈ 7 h before g3t-G-E0 waits.

### 4.5 Budget (GPU-h; cap 33)

explorers ≤ 0.375 + worker smoke 0.15 + F+ gate 5.16 + Stage 1 25.8 = **31.5**; headroom ≈ 1.5 (resumes only).

Fallback (decide before freezing; never after results): use the frozen `scripts/topic2_train.py --steps 35000 --max-run-hours 2.2` unchanged, with no resume. The gate is then inherited from the r1 1x pass and declared a limitation ("F+ capacity at 4x not measured"). Total ≈ 26.3, with a reserve of 3 full reruns.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt            # rc 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | grep -vc ': OK$'              # 0
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice timeout 900 /home/juke/superclaude-env/bin/python3 -B \
  verification/explorer_FU_B_r1_2/p01_cpu_determinism_and_schedule.py $PWD /tmp/p01.json                 # a_* all true; b naive false / restored true; warmup 1750
PYTHONDONTWRITEBYTECODE=1 nice timeout 600 /home/juke/superclaude-env/bin/python3 -B \
  verification/explorer_FU_B_r1_2/p02_frozen_verdict_on_fub_layout.py $PWD /tmp/p02.json                 # K1/K3 inconclusive "gate failed"; K4 no_verdict
cat verification/explorer_FU_B_r1_2/b300_smoke/out/runs/A_proj35k_C_s0/train_log.jsonl                  # projected_run_hours 1.703
grep -n "explorer_FU_B_r1_2" results/gpu_ledger_2026-10-31.md                                           # started + completed rows, 0.06
```

Invalidation conditions:
- any edit to src/topic2_rgpool or scripts/topic2_*.py;
- a change of perms_hcp.npz or the sanitized split;
- B300 /scratch wiped (the r1 preprocessed set gone);
- the throughput under co-location turning out > 10 % slower (then re-cost: 15 × 1.9 = 28.5 leaves no gate room).
