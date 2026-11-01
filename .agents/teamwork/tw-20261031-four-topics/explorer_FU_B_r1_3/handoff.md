# handoff — explorer_FU_B_r1_3 (FU-B, explorer 3 of 3, lens: adversarial pre-mortem)

Type: Hard. Written 2026-11-01 ~15:1xZ. Recommendation only; no production code written. Probes: `/home/juke/git/00IITP-AI/verification/explorer_FU_B_r1_3/probes/`.

**Summary.** FU-B is runnable inside its 33 GPU-h cap only if the r1 training-loop fixture gate (card §7.2) is inherited rather than rerun at 4x (rerunning the 12 fixture runs at 560k costs ~21 GPU-h, total ~47). Under the frozen r1 code, three settings silently break a 4x run: the throughput probe aborts every run (default `--max-run-hours 0.75`, projected ~1.71 h), the r1 hard timeout (3300 s) is shorter than a 4x run, and the B300 data tree is keyed by the old unsalted tokens, so using r1's original split would put C4-breaching tokens back into every copied-back `run.json`. The frozen verdict script, if reused as is, also accepts wrong-budget records, lets a duplicate rerun record win by glob order, counts a missing F- gate as a pass, and returns `no_verdict` where the card says `inconclusive` (probe P1).

## 1. Observation

O1. Frozen training loop (`src/topic2_rgpool/train.py`):
- L44-48 `lr_at`: warmup = round(warmup_frac*steps), then cosine to 0 over the rest. With `--steps 35000`, warmup is 1750 steps and LR at step 8750 is 1.789e-4. At the end of r1 (step 8750) it was 0 (P2).
- L183 `eval_steps` = quartiles of `steps`, which gives val at 8750/17500/26250/35000. Test runs once, at the end (L218-222).
- L211-220 throughput probe: at `probe_steps` it projects the run length and returns `aborted_throughput` if the projection exceeds `max_run_hours`. `scripts/topic2_train.py:36` default is 0.75 h. P2: the projected time for 35000 steps is about 1.71 h, so every FU-B run would abort at step 200 unless the flag is raised.
- There is no checkpoint and no resume. Only `--save-model` writes `model_final.pt`, at the end (L226-227).
- `run.json` records no hostname, Slurm job id or GPU UUID. It records `cuda_visible`, `device` and `code_sha256`.
- `run.json` keeps `status: "started"` if the process is killed (L124).

O2. Frozen launcher `scripts/topic2_launch_wave.py`: direct `setsid timeout 3300` launches on idle GPUs (L41, L56). Since RESUME addendum 3 this is forbidden: B300 GPU use must go through Slurm.

O3. r1 timing (`results/topic2/2026-11-01/runs/hcp_*/run.json`, P2):
- `wall_sec` 1544-1655. Data load 21.2 s; 0.1757 s/step (91 samples/s).
- 4x per-run estimate 1.72-1.84 GPU-h (mean 1.75).
- 15 Stage-1 runs ≈ 26.3 GPU-h. Adding the 12 fixture-gate runs at 4x gives ≈ 47.4 > 33.
- Any 3 extra 4x runs: 31.6 GPU-h (slack 1.4, less than one rerun). 6 extra runs: 36.8 > 33.

O4. Frozen verdict path (`scripts/topic2_verdict.py`, `src/topic2_rgpool/stats.py`). P1 ran the frozen script on synthetic run dirs (`p1_verdict_hazards.out.txt`):
- H1: F- gate missing, keep-shaped data → `keep` (L66 `fm is not False`).
- H2: the 5 C runs recorded at `steps 8750`, the rest at 35000 → `keep`. No check on budget or config.
- H3: F+ not run and Stage 1 not run → `no_verdict, "Stage 1 incomplete"`. Card §7.2 says `inconclusive`.
- H4: an extra `hcp_C_s0_rerun/run.json` with the same (source, arm, seed) key flips `keep` → `inconclusive`. The `load()` dict is overwritten in glob order (L23-27).
- H5: a stalled E run (`completed`, NMSE 1.0) is counted as valid → `keep`. This matches the r1 card rule, but it shows a stall can create a keep-shaped result.
- `stats.verdict` (L52-72): stop iff hi < δ; keep iff mean ≥ δ and lo > 0 and I2 lo > 0. The F- downgrade applies to keep only. An F+ failure returns `inconclusive` before stop is considered.

O5. Data and C4 on B300:
- HCP data and the r1 preprocessed tree exist only on b300-01 (= 61.107.201.98, `cloud-S1HDe3`).
  - `/scratch/iitp4/worker_M3_r1/hcp/subjects` holds 88 subject dirs; `/scratch/data/hcp/download_HCP_REST1_filtered` holds 1084 entries (counts only).
  - b300-03 and b300-04 have neither, and no `/scratch/iitp4` (counts 0/0).
  - `/scratch` is a node-local md0 ext4 array (`df`/`mount`).
- The B300 subject dirs are named by the old unsalted content-hash tokens. The repo `split.json` and `hcp_manifest.json` are sanitized to `h00`..`h87` (addendum 05 §2).
  - `train.HCPSource` opens `data_dir/subjects/<token>/` (L56-63) and writes `test_pseudonyms` into `run.json` (L220).
  - So with the r1 original split, every FU-B `run.json` carries the old tokens, which recreates B1 when the file is copied back.
  - With the repo split, the data dir must be re-keyed positionally.
- r1 jobs used `--split-file code/split.json --data-dir hcp --perm-file partitions/perms_hcp.npz` (`verification/worker_M3_r1/wave2_jobs.json`). The S-arm key is `S_seed{s}`: the npz keys are E, C, S_seed0..S_seed4, G, R, nvox, group_mask.
- `/scratch/iitp4/worker_M3_r1/code/split.json` shows mtime `Nov 1 11:56` in `ls`. B300 local time is evidently KST (sacct prints 23:55:49 for 14:55:49Z), so this is 02:56Z, during r1's own split creation, not a later write. P3 confirms the content is r1's original-token split and maps exactly to the repo split, and 0 of 176 data files changed after 03:10Z.
- All 15 r1 hcp runs have identical `test_den` (max rel diff 0.0) and identical test order (P2). den depends only on the data, the eval masks and the brain mask, not on the weights, so it is a free data-identity check.

O6. Slurm on B300 (`sinfo`, `scontrol`, `sacctmgr`, 14:2xZ):
- Partitions: gpu (default 4 h, max 2 d), interactive (4 h), debug (30 min). PreemptMode OFF.
- QoS `normal`: MaxTRESPerUser gres/gpu=8. User `connectome` has `normal,whole`; `whole` allows 32.
- Every FU team runs as unix user `connectome`, so all of them share 8 concurrent GPUs under `normal`.
- Jobs seen: `fuE2_smoke` running on b300-01, `fuA_e2_envbuild` on b300-02, `fud3_ls` (FU-D), plus other users.

O7. Current state:
- C1 PROTECTED_HASHES 0 failures.
- `code_sha256_at_freeze.txt` 33/33 OK.
- `output_sha256_r2.txt` passes.
- `tests/topic2_rgpool`: 92 passed (local, CUDA hidden, 79.7 s; the M3 r3 team may be adding tests).
- The r1 worker computed an interim verdict mid-run (`verification/worker_M3_r1/verdict_partial_after_wave2.json`).
- Addendum 05 §4.5: per-seed I1 tracks when E left the predict-zero plateau.
- Addendum 04: `hcp_S_s2` stalled at NMSE 1.0000.

O8. P3 B300 Slurm smoke (job 419): mapping, den identity (max rel diff 0.0), throughput 1.711 h/run, peak 144.6 GiB; details §6.

## 2. Logic chain

L1 (O3). The cap forces a gate decision. Stage 1 alone (26.3) fits under 33 with about 3.8 reruns of slack. No 4x gate that keeps the r1 gate rule (F+ needs E, C, S) fits with any rerun margin. So the card must declare the governing gate to be the inherited r1 §7.2 result: F+ pass, F- pass at 140k, pinned by `output_sha256.txt` / `c4_sanitized_sha256.txt`. It must state the G6 limitation openly: capacity is certified at 140k, not at 560k. Verifiers will attack this, so it has to be written in the card and not discovered later.

L2 (O1, O2). Under Slurm, the r1 abort and timeout settings are wrong for 4x and must be stated as FU-B values:
- `--max-run-hours 2.6`, so a slow node aborts at step 200 after about 40 s of GPU time;
- Slurm `--time=03:00:00`;
- no `topic2_launch_wave.py`.
Nothing in `src/` changes: everything is set through flags of the frozen `scripts/topic2_train.py`. The LR handling is then fixed by code: `--steps 35000 --warmup-frac 0.05`, cosine to 0 over 35000, peak 2e-4, batch 16. The schedule shape is r1's, stretched, so budget is the only factor that changes.

L3 (O1). Checkpoint cadence: the frozen loop cannot resume. A resumable loop would be new training code, which breaks "reuse frozen code by import" and needs its own equivalence proof (RNG state of g_order/g_mask/torch, optimizer state). With PreemptMode OFF and runs of about 1.75 h against a 2-day MaxTime, the cheaper and verifiable policy is:
- val at the 4 quartiles;
- final weights only (`--save-model`, kept on B300);
- no mid-run checkpoint and no resume;
- a failed run is rerun once from scratch.

L4 (O5). The C4-safe data path is a positional hard-link farm under the FU-B B300 dir: `subjects/hNN/{bold_z_fp16.npy,mask.npy}`, hard-linked (`os.link`) to r1's files.
- The mapping is built in memory on B300 from r1's original manifest order, which is sorted by content hash, exactly as addendum 05 defines h-numbers.
- Hard links rather than symlinks: an `ls -l` of the farm then shows no old token, and deleting r1's dir (root action §7(5)) cannot break a running job.
- Runs use the repo's sanitized `split.json`, so every `run.json` carries only positional tokens. The verdict code can then require `split_file_sha256` = the sanitized split hash.

L5 (O5). Data integrity must be proven, not assumed, because r1's B300 tree was written after the governed runs. FU-B's first job should check that the test den through the farm equals r1's `test_den` (O5 last bullet). That proves the mapping, the split order, the eval masks and the data bytes of the 16 TEST subjects in one comparison, with no outcome seen. P3 does this.

L6 (O4). The FU-B verdict code must not reuse `scripts/topic2_verdict.py`. A new script in FU-B's own path may import `stats.t_interval`, `relative_gain`, `hierarchical_bootstrap` and `verdict`, but it must add its own record validation. H1-H4 are exactly the defect classes listed for M3_r2 (V07, V08/V10, V06, case A) plus two new ones: budget/config mismatch and duplicate records.

L7 (O6). Scheduling:
- Data exists only on b300-01, so jobs must be pinned (`-w b300-01`) or the farm replicated.
- The 8-GPU per-user QoS is shared with FU-A/C/D/E. If FU-B queues 15 jobs at once, it holds most of the user's GPU slots for about 3.5 h of wall time, blocks other teams and can starve FU-B's own reruns.
- A throttled job array (`--array=0-14%4`) or explicit waves keeps the ledger honest and the cap check meaningful.
- `--qos=whole` only helps if the farm is replicated to another node (copying within B300 is not off-B300 and is allowed under the r1 C6 statement; the card must say so).

L8 (O7). Stalls and plateau timing are real at this setting, and the 4x run warms up 4x longer (1750 steps). The card should pre-register:
- a stall definition: final val NMSE ≥ 0.999 and last-100 train loss ≥ 0.999;
- that a stalled run is valid (the r1 rule, so FU-B stays comparable);
- a sensitivity analysis that drops the whole seed triple, reported beside the primary result and never governing.
It should also forbid interim verdict computation, or declare it non-decisional: all 15 runs launch regardless.

## 3. Caveats

- I did not read the other two FU-B explorers (independence). Their recommendations may differ on the gate question.
- The 4x GPU-h estimate scales r1's wall time on an idle node launched directly. Under Slurm, with up to 8 concurrent jobs reading about 133 GB each into GPU memory, wall time could be higher. P3 measures one job, not 8 concurrent.
- P3 used r1's venv (`/scratch/iitp4/worker_M3_r1/venv`, read-only, `PYTHONDONTWRITEBYTECODE`) and did not rebuild the env. The worker should build its own with `scripts/b300_env/build_env.sh`. Note that `scipy` is unpinned in that recipe: t-quantile drift was about 1e-12 between envs (addendum 05).
- The inherited gate is a scientific limitation I cannot remove within the cap. If root prefers a 4x gate, it needs a cap change (PI) or a different gate rule (for example F+ C vs E only at 1 seed, 3.5 GPU-h), which departs from r1's gate and must be argued in the card.
- I checked no families or HCP restricted data. The test set is the same 16 subjects as r1. It was opened in r1, without model selection, and the card must disclose this.
- Five follow-ups each test at δ = 1 %. There is no multiplicity rule across FU-A..E (PI decision 7 is silent).

## 4. Conclusion (recommended FU-B strategy)

The card is frozen with a sha256 receipt in `results/topic2/<date>_fu_b/` before any FU-B real-data run. The P3 smoke saw no outcome and is disclosed in card §0.

1. **Design (card).**
   - Same split, partitions (`perms_hcp.npz`, keys E / C / S_seed{s}), arms, seeds 0-4, masks, model E36_d2262, target, metric, δ = 1 %, verdict table and t/df4 + bootstrap as r1.
   - The only change: `--steps 35000` (560k samples, about 73.5 passes).
   - LR: `--warmup-frac 0.05` (1750 steps), cosine to 0 over 35000, peak 2e-4.
   - Val at 8750/17500/26250/35000, descriptive only. It is not a 140k replication: at step 8750 the LR is still 1.79e-4.
   - Test at the end only. Final weights saved on B300 only.
2. **Gate.** Governing = r1 §7.2 F+/F- result (pinned files), named as an inherited gate with the 140k limitation. The FU-B verdict code reads it from the pinned r1 `verdict.json` and checks its sha256. If the file is missing, unreadable or mismatched, the gate is unknown: F+ unknown → `inconclusive`, F- unknown → treated as failed (keep → inconclusive). Unknown is never counted as a pass.
3. **Failure policy.**
   - Software failure = crash, non-finite loss, `aborted_throughput`, Slurm TIMEOUT / NODE_FAIL / OOM / CANCELLED, `run.json` status ≠ completed or unparsable, or a config-validation failure.
   - On a software failure, rerun that (arm, seed) once with the identical command into a new dir `..._try2`. Both attempts are recorded.
   - A second failure leaves the seed missing → `no_verdict` (software, not a scientific null).
   - If the cap would be exceeded before Stage 1 is complete, the remaining runs are not launched → `no_verdict` (cap), with a costed plan.
   - `inconclusive` is reserved for the card's scientific branches: the interval straddles δ / 0, F+ unknown, or keep with an F- failure.
   - A stalled-but-completed run is valid (r1 rule), plus a pre-registered descriptive sensitivity.
4. **Compute.**
   - Jobs: Slurm `sbatch -p gpu -w b300-01 --gres=gpu:1 --time=03:00:00 --array=0-14%4` (or waves of ≤ 4), with frozen `scripts/topic2_train.py --max-run-hours 2.6 --save-model`.
   - Env: project-local under `/scratch/iitp4/<FU-B worker>/`.
   - Cap check before every submit: Σ completed actual + Σ running × 1.84 + new × 1.84 ≤ 33.
   - Ledger: a started row at submit and a completed row from `sacct` (Start, End, Elapsed × AllocTRES gpu), with the Slurm job id in the purpose text.
   - Copy back `run.json` / `train_log.jsonl` / `stdout.log` after each job, not at the end (/scratch can be wiped).
   - A sidecar `job_meta.json` (written by FU-B's own wrapper) holds hostname, job id, GPU UUID and sacct state.
5. **C4 and C6.**
   - Use the positional hard-link farm (L4). Never use r1's `code/split.json` or `hcp/manifest.json`, and never copy them back.
   - Never run `ls -l` on any r1 or farm path. Print counts only.
   - Before any file enters the repo, run the `test_c4_tokens_r2.py`-style detector on the FU-B results dir.
   - Weights and per-subject data stay on B300. Only `run.json` (positional tokens, `test_num` / `test_den`) and aggregates come back.
   - Do not touch the dev salt or the sealed originals.
6. **Verdict code (new file in FU-B's path, tested).** Validate every record before counting it:
   - `source == hcp`, `cfg`, `steps == 35000`, `batch == 16`, `lr`, `warmup_frac`, `mask_ratio`, `wd`;
   - `perm_sha256` equals the r1 run's `perm_sha256` for the same (arm, seed);
   - `split_file_sha256` equals the sanitized split sha;
   - `code_sha256` equals `code_sha256_at_freeze` for `src/topic2_rgpool`;
   - `n_test == 16`, identical test order, finite `test_nmse`.

   Then resolve attempts explicitly: exactly one completed attempt per key, otherwise error or `no_verdict`. Never rely on glob order. After that, call `stats.verdict`.

   Tests: each of H1-H5 and V01-V11 as synthetic cases, with each boundary at equality (hi == δ → not stop; mean == δ, lo == 0 → not keep/modify; I2 lo == 0 → modify not keep). Also: F- failure must NOT downgrade modify (card r1 rule), F+ failure must return `inconclusive` even if Stage 1 is absent, and the shipped r1 `verdict.json` must be reproduced from r1 records when the budget check is parameterised to 8750.
7. **Report.**
   - The FU-B verdict stands beside r1's stop, never in place of it.
   - A per-seed pairing with r1 (same init, order and mask seeds) is allowed as descriptive "budget effect" only.
   - Add a multiplicity note: 5 follow-ups at δ = 1 %; a 99 % t interval (0.05/5) is reported descriptively.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # expect 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | grep -c ': OK$'                     # expect 33
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_B_r1_3/probes/p1_verdict_hazards.py   # H1 keep, H2 keep, H3 no_verdict, H4 inconclusive, H5 keep
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_B_r1_3/probes/p2_budget_schedule.py    # warmup 1750; probe abort=True; 26.3 / 47.4 GPU-h
grep -n "max-run-hours" scripts/topic2_train.py; grep -n "timeout-sec" scripts/topic2_launch_wave.py
```
Invalidation conditions:
- the P3 den comparison is not ≈ 0;
- `M_split_lists_match` is false;
- `M_farm_complete` ≠ 88;
- the 35000-step projection is > 2.6 h;
- peak GPU memory is near the device total.
Any of these changes §4 items 4 and 5.

## 6. P3 — B300 Slurm smoke (job 419, debug, b300-01, 1 GPU, COMPLETED, 52 s, 0.015 GPU-h, ledger rows started + completed)

`verification/explorer_FU_B_r1_3/probes/p3_result.json` (no token; 0 matches for a 16-hex pattern), `p3_sacct_419.txt`, script `p3_b300_smoke.py` / `p3_job.sbatch`.
- M (mapping): r1 B300 manifest has 88 subjects, sorted by content hash = True. The repo sanitized manifest equals that positional order = True. r1 `code/split.json` still holds the ORIGINAL tokens (its `ls` mtime 11:56 is KST = 02:56Z, r1's own write), and the content maps exactly. Mapped train/val/test lists equal the repo sanitized split = True/True/True (64/8/16, disjoint). r1 data files modified after 03:10Z: 0 of 176. Farm complete 88/88 (hard links).
- D (data identity): frozen `evaluate_hcp` through the farm, untrained E model, eval seed 7002, 16 TEST subjects → per-subject den max relative difference vs r1 `test_den` = **0.0** (9.4 s). Mapping, split order, masks and data bytes are confirmed. No outcome (num) was recorded.
- T (throughput): frozen `train.run`, `--steps 35000`, aborted at step 99 by the frozen probe (`aborted_throughput`, as predicted). 0.1754 s/step, 91.22 samples/s, **projected 1.711 h per run** (matches r1). Peak GPU memory 144.6 / 267.7 GiB, so one run per GPU. The log holds only `data_loaded`, `throughput_probe`, and no loss line. `run.json` has no `test_pseudonyms`.
- Cleanup: `/scratch/iitp4/explorer_FU_B_r1_3` removed (unlinking the hard links left r1's 88 subject dirs intact, 88 before and after). No job left in squeue.

New hazard found by P3: `sacct` prints Start/End in **KST** (23:55:49 for 14:55:49Z). A worker who copies sacct times into the ledger's "UTC" columns is off by 9 h. Use `sacct -o start,end` together with `TZ=UTC sacct ...`, or `date -u` at submit and at end.

## 7. What verifiers will attack (pre-mortem list for the FU-B worker)

| # | attack | defence the card or code must carry |
|---|---|---|
| A1 | "Gate not run at 560k (G6)" | the inherited gate is explicit in card §7; a cap table proves a 4x gate is unaffordable; limitation in the report |
| A2 | runs silently aborted or truncated (`aborted_throughput` at 0.75 h; r1 timeout 3300 s) | `--max-run-hours 2.6`; Slurm `--time 03:00:00`; verdict code requires `steps == 35000` and `status == completed` |
| A3 | wrong-budget or wrong-perm record counted (H2) | per-record validation against r1 `perm_sha256` per (arm, seed), sanitized split sha, frozen code sha |
| A4 | duplicate attempts resolved by glob order (H4) | explicit attempt resolution, exactly one completed per key |
| A5 | missing gate = pass (H1, V07) | unknown gate never passes; tests |
| A6 | F+ failure / no Stage 1 → `no_verdict` instead of `inconclusive` (H3) | FU-B code returns `inconclusive` when the gate fails, whether or not Stage 1 exists; test |
| A7 | F- failure downgrading modify (V06) / boundaries ≥ vs > (V01-V05) | tests at equality; card states that F- affects keep only |
| A8 | C4: old tokens in copied-back `run.json` | positional hard-link farm + repo split; token detector run on the results dir before copy-back |
| A9 | data drift in r1's B300 tree | den-identity check as the first FU-B job step (P3 recipe) |
| A10 | interim peeking / result-dependent reruns (stall) | all 15 launched regardless; no interim verdict; stall = valid + pre-registered sensitivity |
| A11 | GPU-h over cap, or ledger in the wrong time zone | cap check before every submit with 1.84 GPU-h per run reserved; ledger times in UTC; Slurm job id in each row |
| A12 | 4x budget read as a reversal of r1 stop | report: FU-B verdict beside r1, descriptive per-seed pairing only; multiplicity note across FU-A..E |
