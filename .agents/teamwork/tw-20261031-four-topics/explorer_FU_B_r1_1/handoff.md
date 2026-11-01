# Handoff (Hard) — explorer_FU_B_r1_1, milestone FU_B (Topic 2 follow-up B: 4x budget)

**Summary.** FU-B can be run as a clean, falsifiable new experiment that reuses the frozen r1 code without any edit. Pass `--steps 35000` to the frozen `scripts/topic2_train.py` and everything else stays as in r1. A Slurm smoke on b300-01 (job 413, 0.065 GPU-h) reproduced r1's training losses bit for bit and projected 1.694 h per 35k-step run. The plan is a new 4x-budget F+ gate (seed 0, arms E/C/S), then 15 Stage-1 runs: about 31.3 GPU-h against the 33 cap, which leaves room for one rerun. Two things must not be reused unchanged:
- the frozen `scripts/topic2_verdict.py`: on the FU-B layout it returns the wrong verdict in 3 of 4 synthetic scenarios;
- the r1 symlink-free data path: the B300 tensors are named by the old content-hash tokens, so a positional view is needed.

## 1. Observation

**O1 Code path (frozen, read-only).**
- `src/topic2_rgpool/train.py` `lr_at(step, steps, peak, warmup_frac)` (lines 44-48) scales warmup and cosine to `a.steps`.
- Validation runs at `round(steps*f)` for f in (0.25, 0.5, 0.75, 1.0) (line `eval_steps = ...`).
- Weights are saved only at the end with `--save-model`. There is no intermediate checkpoint and no resume.
- The throughput probe (`--probe-steps`, `--max-run-hours`) aborts with status `aborted_throughput`.
- The run record stores `test_pseudonyms` as the data-dir subject names.
- `scripts/topic2_train.py` exposes `--steps` (default 8750) and `--max-run-hours` (default 0.75).

**O2 Frozen verdict script.**
- `scripts/topic2_verdict.py` hard-codes `FIX_SEEDS = (0, 1)` and requires both F+ and F−.
- Line 66 is `S.verdict(ci1, ci2, a.delta, bool(fp), fm is not False)`, so a missing F− counts as a pass.
- If Stage 1 is incomplete it returns `no_verdict` regardless of the gate.
- Probe `verification/explorer_FU_B_r1_1/probe_frozen_verdict_on_fub_layout.py` (.out.json), FU-B layout (F+ s0 only, no F−):

  | scenario | FU-B requires | frozen script returns |
  |---|---|---|
  | gate pass, stop | stop | inconclusive |
  | gate pass, keep | keep | inconclusive |
  | gate fail, Stage 1 not run | inconclusive | no_verdict (case A) |
  | one Stage-1 run failed | no_verdict | no_verdict |

**O3 Frozen `stats.verdict` itself is correct.**
- Rule order: F+ guard first, strict `hi < delta`, `mean >= delta and lo > 0`, `i2 lo > 0`, and F− downgrades only keep.
- Probe `probe_fub_verdict_reference.py` (.out.json): a reference wrapper reusing `stats.py` by import, with 24 scenario cases and 8 exact-value boundary cases. Baseline all pass.
- 18 of 19 mutants were killed: V01, V02, V04 and V05 boundaries, the F− `<=` boundary, stop `<=`, stop-on-mean, F− downgrading modify (in stats and in the wrapper), V07 (missing gate counts as pass), case A, V08/V10 (failed or non-completed runs counted), wrong `steps` counted, duplicate run key last-wins, V09 (no test-order check), V03 (I1 against S), and missing F− counts as pass.
- V11 (Stage 1 read after a gate failure) is an equivalent mutant only because the wrapper passes the real gate value to `stats.verdict`, whose first line returns inconclusive.
- First probe version: a boundary case built through an NMSE round trip failed, because (e − e(1−a))/e ≠ a in floating point. Boundary tests must use exact interval dicts or exactly representable gains (δ = 0.25, E = 1.0, C = 0.75).

**O4 B300 (read-only probes, counts only).**
- Slurm partitions: `gpu` (2 days), `interactive` (4 h), `debug` (30 min), on b300-[01-04] with 8 GPUs each.
- 61.107.201.98 = b300-01 (NodeHostName cloud-S1HDe3, Weight 100). `/scratch` is a node-local md0 ext4.
- r1 tensors: `/scratch/iitp4/worker_M3_r1/hcp/subjects` holds 88 dirs (bold_z_fp16.npy, cellmeans.npy, mask.npy), 126G. The r1 venv is torch 2.15.0+cu134, numpy 2.5.4, scipy 1.18.1.
- The positional order of the sealed original manifest (`/scratch/iitp4/worker_M3_r2/sealed_c4/.../hcp_manifest.json`, sorted by content sha256: asserted True) maps the sealed split to positional lists. Their JSON hashes equal the repo `split.json` lists: train 936ce8d88dfd, val e58fea61cda9, test 83456e9bf63f (count/hash only, no token printed).
- ssh to B300 through dgx1→connectome is intermittent ("Connection timed out during banner exchange"; ControlMaster died twice). Each step needed ConnectTimeout ≥150 s and retries.

**O5 Slurm smoke, job 413.**
- Settings: debug, `-w b300-01`, 1 GPU, `-c 8`, `--mem 96G`. Ran 14:50:02–14:53:53Z, Elapsed 00:03:51, MaxRSS 1.9 GB.
- Ledger rows: started and completed, 0.065 GPU-h.
- Setup: frozen code copy, the repo sanitized split (sha256 cc521b08…) and a positional symlink view hNN → r1 dirs.
- Results:
  - `anchor_E_s0_8750` and `anchor_C_s0_8750`: `loss_mean_last100` and lr at steps 100 and 200 are bit-identical (difference 0.0) to r1 `hcp_{E,C}_s0/train_log.jsonl`; `perm_sha256`, `code_sha256`, `n_params` 38,712,096 and `n_train_windows` 7,616 are equal; throughput 92.3 samples/s.
  - `proj_E_s0_35000`: lr at step 100 is 1.142857e-05 (= 2e-4·100/1750), and `projected_run_hours` is **1.694**.
- Logs: `verification/explorer_FU_B_r1_1/smoke_413/`. The B300 dir was removed afterwards (only symlinks, code and logs).

**O6 r1 numbers** (dated r1 outputs, used only as a noise scale and as the comparator).
- r1 runs took 1544–1655 s at 8750 steps; projection and wall time agree within 1 %.
- Seed-level SD: I1 0.173 %; I2 0.380 % (0.092 % without the stalled seed 2).
- `hcp_S_s2` stalled at NMSE 1.0. Four other runs sat at about 1.0003 at step 2188.
- Addendum 05 #5: per-seed I1 tracks E's plateau-escape timing.
- Addendum 05 #7: the 288-d → 48³ decoder bottleneck. B is the least direct option.
- r1 F+ gain: seed 0 C-vs-E 2.77 %, C-vs-S 2.90 % (seed mean 3.06 / 2.93 %). F− pass at gain −1.74 % (verdict.json sha 59af05e5…).

**O7 Operating characteristic.** Probe `probe_operating_characteristic.py` (5 seeds, t df 4, δ 1 %):
- At r1 seed SD, the I1 half-width is 0.215 %. P(stop) is 1.00 for true I1 ≤ 0.15 %, 0.996 at 0.5 % and 0.68 at 0.75 %. P(keep) is 0.50 at 1.0 % and 1.00 at ≥ 1.25 %.
- At 3× SD, P(stop | I1 = 0) is 0.89; at 5× SD it is 0.51.
- Stall scenarios on r1-scale numbers:
  - C stalling in 1–3 seeds forces `stop`.
  - E stalling in 2–3 seeds gives `inconclusive`.
  - S stalls leave `stop` but move I2's lower bound.

**O8 Integrity.**
- C1 rc 0. `code_sha256_at_freeze.txt` has 0 failures. `output_sha256_r2.txt` all OK.
- No git writes, no frozen file edited, no IDs printed.

## 2. Logic chain

1. From O1 and O5: `--steps 35000` on the unchanged frozen CLI gives the only change FU-B needs: a 4x budget and a schedule stretched by its fraction (warmup 5 % = 1750 steps, cosine to 0 at 35,000, peak 2e-4, wd 0.05, clip 1.0, batch 16).
   - The window-order (1000+s), mask (2000+s) and init (s) streams do not depend on LR. So each FU-B run sees exactly r1's first 140k samples and masks, then more. This gives a clean paired budget contrast against r1.
2. From O1: the checkpoint cadence is fixed by the frozen loop: val at 8750/17500/26250/35000, final weights only, no resume.
   - Adding resume would change the training path. So any interruption is a software failure → rerun once from scratch.
   - From O5, reruns are deterministic (bit-identical losses), so a rerun is not a new random draw. There is no selection-on-outcome risk.
3. From O6/O7: the r1 F+ advantage could be a sample-efficiency effect. At E36 the M0 Linear 288→72 can in principle carry 8 cells' signals, so E might catch up with 4x training. The 1x gate therefore does not certify 4x capacity, and a 4x F+ gate is needed.
   - From O5: one seed × 3 arms costs about 5.1 GPU-h.
   - r1 seed gains (2.8–3.4 %) are far above δ with small spread, so one seed is adequate.
   - F− at 4x does not fit the cap. It is inherited from r1 (1x), a stated limitation that affects only keep.
4. Budget from O5:
   - 18 runs × 1.70 h ≈ 30.6, plus about 0.5 of Slurm/eval overhead, plus smokes of about 0.17 → **≈ 31.3 of 33**.
   - The reserve of ≈ 1.7 equals one rerun. A deterministic budget guard is mandatory, and the card must say that a rerun blocked by the cap leaves the seed missing → `no_verdict`.
5. From O2/O3: the worker must write a new FU-B verdict script that reuses `stats.t_interval`, `relative_gain`, `hierarchical_bootstrap`, `gate_fixture` and `verdict` by import. It must add explicit tri-state gate handling and Stage-1 integrity checks. The probe's 24+8 case table is the minimum test set (it kills every listed defect class).
6. From O4: data lives only on b300-01's local `/scratch`. The run record writes data-dir names into `test_pseudonyms`, and the r1 dirs carry old re-identifiable tokens. So the worker needs a positional view built in its own `/scratch/iitp4/<worker>` dir from the sealed manifest order (verified equal to the repo split). It must not use symlinks to `worker_M3_r1`, whose cleanup is a pending root action: hard links on the same ext4, or a copy.
7. From O7: with 5 seeds at r1 noise, FU-B is decisive (stop or keep) unless the true I1 lies in roughly 0.75–1.0 % or the seed SD grows ≥ 3×. That is a falsifiable design. Stalls are the main threat to interpretation, so they get a pre-registered definition and a sensitivity line.

## 3. Caveats

- The per-run cost is a 300-step projection on an idle node. r1 wall times varied +6 %; at 1.80 h/run the plan totals about 33.1 and no rerun fits.
- b300-01 is the only node holding the tensors. Other FU teams will likely contend for its 8 GPUs, so wall time could reach 2–3 waves of 1.75 h.
  - Mitigation: copy the 126 GB to another B300 node's `/scratch/iitp4/<worker>/`. It stays inside B300, so C6 still holds; verify with sha256 per file.
- The F− gate is not rerun at 4x. If FU-B yields keep, F− rests on 1x evidence only.
- I did not read the other FU-B explorers' reports (independence). I did not test a 4x-schedule run beyond 300 steps.
- A longer warmup changes early plateau dynamics, so the stall risk at 4x is unknown.
- The 4x schedule's peak LR is untuned (by design: comparability and no result-dependent tuning).
- Reusing the r1 venv worked. The worker may build its own from `scripts/b300_env/build_env.sh` + `lock.txt`; the 300-step anchor then re-verifies identity at about 0.03 GPU-h.
- The ssh path to B300 is flaky. Use sbatch (detached) and short polls, not long-lived ssh sessions.
- I chose the FU-B paths (`docs/.../2026-11-02_topic2_fuB_*`, `results/topic2/2026-11-02_fuB/`, `scripts/topic2_fuB_*`, `tests/topic2_fuB/`). Root's naming wins.

## 4. Conclusion (recommended strategy for worker_FU_B)

**Card (new, dated, frozen before ANY governed run, F+ gate included).**
- Location: `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fuB_card.md`, sha256 in `results/topic2/2026-11-02_fuB/card_sha256.txt`, plus `code_sha256_at_freeze.txt` (new FU-B code + the 33 r1 pins).
- §0 disclosure:
  - r1 stop (I1 +0.147 % [−0.068 %, +0.361 %]), r1 val curves and addendum 05 #5/#7 are known.
  - The explorer smoke produced no outcome number (300-step losses only).
  - The prior expectation is stop.
- Question: does the r1 stop survive a 4x budget, i.e. is the r1 null explained by under-training?
- Estimands, arms and δ are identical to r1: I1 = (E−C)/E, I2 = (S−C)/S, δ = 1 % (PI decision 3). Unit = seed, s = 0..4, same seed streams.
- Single manipulated factor within FU-B: the M0 permutation. The change relative to r1 is the budget: 35,000 × 16 = 560,000 samples, about 73.5 passes.
- LR schedule: frozen `lr_at` with steps = 35000: warmup round(0.05·35000) = 1750, cosine to 0, peak 2e-4, no retuning (stated limitation).
- Checkpoint cadence: val NMSE at steps 8750/17500/26250/35000 (8 VAL subjects, health only; the 8750 point is not comparable to r1's final because the LR is not annealed). Final weights saved with `--save-model` (B300 only). No intermediate checkpoints, no resume. Test NMSE once at step 35000.
- Data and split:
  - HCP-YA OA r1 tensors (b300-01) through the positional view; the repo `split.json` (sanitized, sha256 cc521b08…) is the split file.
  - 64/8/16, the 5 burned dev subjects already excluded (88-file manifest). No re-preprocessing; the sealed salt is not needed.
  - The card records the positional-map equality (train/val/test list hashes, O4).
- Gates:
  - F+ at 4x budget: Fplus × E/C/S × seed 0, `perms_Fplus.npz` (E, C, S_seed0), pass iff (E−C)/E ≥ δ and (S−C)/S ≥ δ on seed-0 test NMSE. Stage 1 is launched only after it is computed and passes.
  - F− is inherited from the r1 `verdict.json` (sha-verified; `fixture_gates.Fminus.pass` must be literal `true`).
- Verdict order:
  1. A missing or failed F+ gate after its rerun → `no_verdict`.
  2. F+ fail → `inconclusive` (measurement capacity) + costed plan; Stage 1 is never launched or read.
  3. Stage 1 incomplete or failing integrity (status, steps == 35000, finite NMSE, unique (arm, seed), code/perm/split hashes, identical test order) → `no_verdict`.
  4. Otherwise frozen `stats.verdict(I1_t, I2_t, δ, gate_pass, fminus is True)`: stop iff I1 hi < δ (kill rule); keep / modify / inconclusive exactly as r1 §8; F− only downgrades keep.
- Failure policy:
  - Software failure (crash, non-finite loss, Slurm timeout or node failure, throughput abort at `--max-run-hours 2.0`, Slurm `--time 02:15:00`) → one identical rerun into a new dir. The failed record is kept under `failures/`, never in the verdict input.
  - A second failure, or a rerun the cap does not admit → that seed is missing → `no_verdict`.
  - A stall (status completed, val NMSE ≥ 0.999 at all 4 checkpoints) is a valid run, not rerun (r1 rule). The card pre-registers a stall-sensitivity line: the verdict with stalled seeds dropped pairwise, shown beside the primary result and never overriding it, with the label "stall-sensitive" if the category differs.
- Budget guard (C5, cap 33): the ledger sum of FU-B rows plus the projected hours of jobs about to launch must be ≤ 33.
  - Projection per run = max(1.70, observed max of completed FU-B runs).
  - Launch order: worker smoke/anchor (≤0.1) → F+ wave (3 jobs) → Stage 1 (15 jobs) → at most 1 rerun.
  - Slurm: `-p gpu -w b300-01 --gres=gpu:1 -c 8 --mem=32G`. Ledger start and close rows with the job id; GPU-h from sacct Elapsed.
- Secondary (descriptive; no decision rides on them):
  - hierarchical bootstrap;
  - paired budget effects: per (arm, seed) NMSE_FUB − NMSE_r1, and ΔI1_s = I1_FUB,s − I1_r1,s with a t interval;
  - manipulation check: E's seed-mean test NMSE below r1's 0.98892;
  - plateau-escape step per run (first 100-step loss mean < 0.995) against per-seed I1;
  - val curves.
- Pre-registered readings:
  - stop → "under-training within 4x does not explain the r1 stop";
  - keep/modify → "a gain emerges with budget"; the r1 verdict stays as recorded for its budget;
  - inconclusive (gate) → "at 4x the pipeline cannot show a planted grouping advantage";
  - no_verdict → software.
- Implementation (new paths only):
  - `scripts/topic2_fuB_make_view.py` (B300: positional hard-link view from the sealed manifest; prints counts only);
  - `scripts/topic2_fuB_sbatch.sh` / launcher;
  - `scripts/topic2_fuB_verdict.py` (imports frozen stats);
  - `tests/topic2_fuB/`: the probe's scenario and boundary table, at least 24+8 cases, kills O3's 18 mutants; C4 token tests on the FU-B outputs.
  - `tests/topic2_rgpool` and `src/topic2_rgpool` are not touched.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt          # rc 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                             # 33 OK
cd verification/explorer_FU_B_r1_1
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" /home/juke/superclaude-env/bin/python3 -B probe_frozen_verdict_on_fub_layout.py /tmp/x1.json   # 3/4 disagree
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" /home/juke/superclaude-env/bin/python3 -B probe_fub_verdict_reference.py /tmp/x2.json          # baseline True; killed 18/19 (V11 equivalent)
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" /home/juke/superclaude-env/bin/python3 -B probe_operating_characteristic.py /tmp/x3.json
diff <(grep '"train"' smoke_413/runs/anchor_E_s0_8750/train_log.jsonl | cut -d, -f2-4) <(grep '"train"' ../../results/topic2/2026-11-01/runs/hcp_E_s0/train_log.jsonl | head -2 | cut -d, -f2-4)   # empty diff
grep explorer_FU_B_r1_1 ../../results/gpu_ledger_2026-10-31.md      # 2 rows, 0.065 GPU-h, Slurm job 413
```

Invalidation conditions:
- an FU-B run whose `projected_run_hours` is above 1.80;
- the 300-step anchor in the worker's env not bit-identical to r1 (then report the env difference before any governed run);
- the positional-view list hashes not equal to O4's;
- B300 `/scratch` of b300-01 wiped (the r1 tensors are gone; re-preprocessing then needs the sealed salt and a re-costed plan).
