# handoff — explorer_FU_C_r1_2 (FU-C, explorer 2 of 3; lens: feasibility and failure modes). Hard handoff.

**Summary.** FU-C is feasible inside its 13 GPU-h cap as **8 fresh seeds (10–17) × 3 arms = 24 runs, about 10.6–11.0 GPU-h**, with no fixture-gate rerun. The probes showed three things:
- The frozen r1 training path is **bit-reproducible under Slurm**.
- Surrogates for new seeds can be built by the **identical frozen pipeline**, which self-checks against the r1 pins.
- The C4 copy-back path works by importing the frozen sanitizer.

The main logistics risks:
- HCP data exist only on b300-01.
- Slurm prefers the other nodes, so every job must pin `-w b300-01`.
- QOS caps the shared `connectome` user at 8 GPUs, across all FU teams.
- SSH to B300 drops intermittently.

The expected scientific outcome is `stop` again. FU-C adds precision, not a new category. A stalled run in arm E is the one realistic way to get `inconclusive`.

## 1. Observation

All GPU use was ledgered. Mine was 0.05 GPU-h. C1 67/67, code freeze 33/33 and output_sha256_r2 156/156 all pass (`LC_ALL=C`, rc 0).

| # | what | evidence |
|---|---|---|
| O1 | Stage-1 runs take 1544–1655 s each (0.43–0.46 GPU-h launch-to-end). Data load 21–29 s. | `results/topic2/2026-11-01/runs/hcp_*/run.json`, `train_log.jsonl` |
| O2 | `perms_hcp.npz` holds only S_seed0..4. `S_SEEDS_HCP = (0,1,2,3,4)` is hard-coded in the frozen `scripts/topic2_build_partitions.py:30`. | npz keys; source |
| O3 | The repo `split.json` is sanitized (h00..h87). B300 data directories use the original tokens. The original split (sha c13b5f21…) and manifest (26ba34a9…) are at `/scratch/iitp4/worker_M3_r1/code/split.json` and `.../hcp/manifest.json`; 88 subject dirs; `fc_train_group.npy` float32 sha e2912ee9… matches the pin. | sha256sum on B300 |
| O4 | The frozen `train.run` writes `test_pseudonyms` (original tokens) into `run.json`. `scripts/topic2_launch_wave.py` launches directly with setsid on idle GPUs, which is now forbidden. | `src/topic2_rgpool/train.py`; source |
| O5 | Slurm: partitions gpu (QOS normal, MaxTRESPerUser gres/gpu=8), interactive (4 h), debug (30 min). The account also has QOS `whole` (32 GPUs). `/scratch` is node-local (md0 ext4). b300-01 = .98 = 192.168.0.2, with `Weight=100`, so it is the least preferred node. HCP raw data and `/scratch/iitp4` exist only on b300-01; they are absent on b300-02/03/04. DefCpuPerGPU 24, DefMemPerCPU 9500. `sacct` prints KST. | `/etc/slurm/slurm.conf`, `sacctmgr`, `/etc/hosts` |
| O6 | P3 (Slurm job 410, CPU only, 37 s, 0 GPU-h) imported the frozen `topic2_build_partitions` and set `S_SEEDS_HCP` in memory only.<br>- `hcp_mode` reproduced the FC sha, the split sha, n_signal 1195, n_mask_vox 229304, and the E, C, G, R and S_seed0..4 perm shas, all bit-exactly.<br>- It built S_seed10..17: 232 rows moved each, dispersion 1.58–1.65 (r1: 1.56–1.67), all distinct. | `verification/explorer_FU_C_r1_2/b300/p03_410.out`, `p03_surrogate_repro.py` |
| O7 | P4 (Slurm job 414, debug, gres gpu:2, 80 s, 0.05 GPU-h, ledger rows opened and closed) ran the r1 venv read-only with a code copy whose 16 files equal the freeze pins.<br>- hcp E and C at seed 0 used the full 8750-step schedule and were aborted by the frozen throughput probe at step 300.<br>- Step-100 and step-200 `loss_mean_last100` are **bit-identical to r1**: E 1.0545948070287705 / 1.0033420294523239; C 1.0544316393136979 / 1.003328688144684.<br>- 0.1747 s/step, projected 0.432 h/run, load 22.1 s, MaxRSS 3.35 GB for both processes. | `b300/p04_414_logs.txt`, `b300_code_sha256.txt`, ledger |
| O8 | P1 used the r1 seed contrasts: I1 sd 0.173 %, I2 sd 0.380 % (0.092 % without the stalled seed 2).<br>- Expected I1 t half-width: 0.215 % at n=5, 0.144 % at n=8 (df 7), 0.104 % at n=13.<br>- Monte Carlo over the card §8 rule at n=8: P(stop) = 1.00 for a true I1 ≤ 0.5 %. At a true I1 = 1 %: keep 0.50, inconclusive 0.47, stop 0.03. | `local/p01_precision.out.json` |
| O9 | P5 placed k stalled runs (NMSE = 1, like r1 `hcp_S_s2`) in 8 seeds.<br>- 1 stalled E: stop 0.997.<br>- **2 stalled E: stop 0.80, inconclusive 0.20.**<br>- Stalls in C or S never change the verdict.<br>- If the r1 stall rate of 1/15 holds, P(≥1 stall among 24 runs) = 0.81. | `local/p05_stall_sensitivity.out.json`, `p01` |
| O10 | P2: a prototype verdict layer plus 26 tests; 21 mutants run.<br>- Baseline survives.<br>- Killed: V01, V02, V03, stop `<=`, V06, V07 (missing, truthy and missing-F− variants), V08, V09, V11/V12, case A (F+ fail → no_verdict), F01 (df), F02 (first 5 seeds only), F03 (I1 against S), F04 (sign), F05 (seed overlap with r1), F06 (code pin ignored), F07 (S perm key not tied to its seed).<br>- F08 (no length check) survives and is **equivalent**: the `len(set(seeds)) != 8` check implies it. | `local/proto_fuc_verdict.py`, `test_proto_fuc_verdict.py`, `p02_mutants.out.json` |
| O11 | P6 imported the frozen sanitizer's `token_map` and `replace_quoted_tokens` and applied them to the 15 sealed original hcp `run.json` files: all 15 are byte-equal to the repo's sanitized copies, with 16 tokens replaced in each. `token_map` needs the ORIGINAL manifest (content_sha256 fields). | `local/p06_sanitize_path.out.json` |
| O12 | SSH to B300 failed in several ways:<br>- "Connection timed out during banner exchange" on most first attempts;<br>- the mux master stalled twice ("read from master failed: Broken pipe");<br>- `ssh … < file`, scp and tar over ssh hung in this environment;<br>- base64 inside argv, with `-n` and under 128 KB, worked;<br>- remote→local stdout worked;<br>- `squeue`/`scontrol` sometimes hung for more than 30 s, while `sacct` and file reads worked. | this session |

## 2. Logic chain
1. Bit-identical early losses under Slurm (O7) plus the frozen per-seed RNG streams (`train.py`: init s, order 1000+s, masks 2000+s) mean that seeds 0–4 rerun under FU-C would duplicate r1, not replicate it. Fresh seeds must therefore be disjoint from 0–4; I recommend 10–17.
2. The same determinism (O7), with code identical to the freeze, makes a rerun of the §7.2 fixture gate redundant: it would reproduce the r1 numbers. Rerunning it would add about 5.2 GPU-h (12 runs) and push FU-C to about 15.8 GPU-h, over the 13 cap. So the card must reuse the r1 gate, and must justify that reuse with O7.
3. Cost of 8 fresh seeds: 24 × 0.44–0.46 ≈ 10.6–11.0 GPU-h (O1, O7). Margin to 13 is about 2 GPU-h, roughly 4 reruns.
   - Reuse (seeds 0–4 plus 5–7) is 9 runs ≈ 4.1 GPU-h.
   - Reuse is cheaper, but it adds seeds after the r1 `stop` was seen (optional continuation), and it pools runs that the r1 direct-launch made.
   - Fresh gives a clean fixed-n df-7 replication. A 13-seed pool can still be reported as descriptive only.
4. New S surrogates are only trustworthy if they come from the identical builder. O6 shows the frozen `hcp_mode` can be driven by import with a seed-list override, and it self-verifies against every r1 perm pin in the same call.
5. The data exist only on b300-01, and Slurm prefers the other nodes (O5). Unpinned jobs would land on b300-02/03/04 and crash on missing files. A crash is a software failure: it costs a rerun, and two crashes give no_verdict. So `-w b300-01` is mandatory.
   - The 8-GPU per-user QOS is shared by every FU team and by other sessions on the same account (O5).
   - Wall time is therefore set by contention, not by FU-C's own 1.5 h (3 waves × 28 min).
6. C4: new `run.json` files carry original tokens (O4). The import path in O11 relabels them to the r1 h-tokens on B300 before copy-back. FU-C and r1 then share the same test order and the same tokens, which the descriptive pooled analysis needs.
7. Scientific yield (O8): with r1's spread, 8 seeds give `stop` unless the true I1 is at least about 0.9 %. FU-C narrows I1 to about ±0.14 % and tests whether I2 > 0 holds without the stalled seed. The only realistic route to a different category is stalled E runs (O9). Stall handling must be pre-specified, staying identical to r1 for the primary.
8. Verdict-code defects (O10): r1's verdict layer was frozen and defective (V07, case A and others). FU-C must not reuse `S.verdict`/`gate_fixture` as the gate logic. It should import only `t_interval`, `relative_gain` and `hierarchical_bootstrap`, and write its own tested layer.

## 3. Caveats
- Bit-identity was shown for 300 steps, two arms, one seed, in the r1 venv. A rebuilt venv was not tested, and a full 8750-step run was not repeated. The worker's env gate (S3 below) covers this.
- The stall rate is estimated from 1 event in 15 runs, and the stall mechanism is unknown. Because runs are deterministic, a rerun of a stalled or NaN run would reproduce it. "Rerun once" therefore cures only transient failures (node, OOM, preemption).
- Contention with the other FU teams is projected from QOS limits, not measured. At 14:50Z only my jobs and two other short jobs (413 fub_e1_smoke, 411 ibrain cpu) were present.
- The size of the preprocessed tensors (about 88 × 1.51 GB ≈ 133 GB) is arithmetic, not a `du` measurement.
- I did not read the other FU-C explorers' outputs (independence).
- The removal of my B300 dir `/scratch/iitp4/explorer_FU_C_r1_2` (1.9 MB: code copy, probe scripts, P3 perms and P4 aborted runs; no subject tokens, no checkpoints) **was denied by the permission system**, so it remains. The local `/tmp/fuc2cm` (one check file) also remains for the same reason. Root may remove both. No processes or jobs of mine are left.
- `squeue` sometimes hung, so the worker should poll with `sacct` and output files.

## 4. Conclusion: recommended worker strategy (covers F1–F3, C1–C8)

**S0 Preflight (local, 0 GPU).**
- `LC_ALL=C` hash checks (the Korean locale prints "완료" instead of OK and breaks greps).
- C1, freeze 33/33, output_sha256_r2.
- Read the r1 `verdict.json` fixture_gates.

**S1 Card (F1).** Write `docs/03_empirical_analysis/topic2/<date>_topic2_fuC_card.md` and freeze it with a sha256 in `results/topic2/<date>_fuC/card_sha256.txt` before S5. It must state:

- **§0 Disclosure.** All r1 numbers were seen. Prediction: `stop` (P ≈ 1 unless the true I1 is at least about 0.9 %). FU-C's value is precision on I1 and I2.
- **Design.** Fresh seeds 10–17; the 5 r1 seeds are not reused. Seed streams are init s, order 1000+s, masks 2000+s, S surrogate seed = s; eval masks 7001/7002 unchanged.
- **Data.** The same data, split, 64/8/16 and dev exclusion as r1, by reading the r1 preprocessed tensors and original split on b300-01 (pins c13b5f21 and 26ba34a9).
- **Arms.**
  - E and C perms are pinned to the r1 shas b83e23eb… and 21e4e239….
  - S_seed10..17 come from the frozen builder by import, with an in-call self-check of every r1 perm sha.
  - The new perm file sha is pinned.
- **Budget, config and hyperparameters.** Identical to r1: E36_d2262, 8750 × 16, `--save-model`.
- **Gate.** The r1 §7.2 gate is reused (both pass), justified by identical code and bit-reproducibility. A missing or non-boolean gate record gives no_verdict. F+ False gives inconclusive.
- **Primary.** A two-sided 95 % t interval with df 7 over the 8 paired seed contrasts. δ = 1 % (PI decision 3, no longer "pending"). The card §8 rules are copied verbatim, with boundaries spelled out:
  - stop iff hi < δ;
  - survive iff mean ≥ δ and lo > 0;
  - keep needs I2 lo > 0;
  - an F− failure downgrades keep only.
- **Failures and stalls.**
  - Software failure: rerun once; still missing → no_verdict.
  - A stalled run is valid for the primary. Flag it by an objective rule, e.g. all four val NMSE ≥ 0.9995 and test NMSE ≥ 0.9995.
  - Pre-specify a descriptive sensitivity analysis that drops every seed with a stalled run.
- **Secondary.** The hierarchical bootstrap (frozen function), and a descriptive 13-seed pool of r1 seeds 0–4 with 10–17 (df 12). Neither ever governs.
- **Cap rule.** If spent + remaining × 0.75 GPU-h would exceed 13, do not launch, and report a partial / no_verdict.

**S2 Code (F2).** New paths only, e.g. `scripts/topic2_fuC_*.py` and `tests/topic2_fuC/`. Do not use `tests/topic2_rgpool`: the M3 r3 team owns it.
- Perm builder: imports `scripts.topic2_build_partitions` and sets `S_SEEDS_HCP` in memory only.
- Verdict layer: imports only `t_interval`, `relative_gain` and `hierarchical_bootstrap`.
- Slurm launcher/array script and copy-back sanitizer: the sanitizer imports `token_map` and `replace_quoted_tokens` and runs on B300 with the stdlib (system python).
- Tests must kill V01–V12, case A and F01–F07. The template is `verification/explorer_FU_C_r1_2/local/`. Add a check that E and C `perm_sha256` equal the r1 pins and that each S key equals `S_seed<seed>`.

**S3 Env gate (≤ 0.1 GPU-h, ledgered).**
- Use your own venv (`bash scripts/b300_env/build_env.sh /scratch/iitp4/<worker>` + lock), or the r1 venv read-only with `-B`.
- Repeat P4 (E and C at seed 0, `--probe-steps 300 --max-run-hours 0.001`, debug partition, `-w b300-01`).
- The step-100/200 losses must equal r1 bit-for-bit. If they do not, stop: the gate reuse is then unjustified.

**S4 Perms (CPU Slurm job, 0 GPU).** Run the S2 builder. The self-check must pass.

**S5 Runs (F3).**
- Command: `sbatch --hold --array=0-23%8 -p gpu -w b300-01 --gres=gpu:1 -c 8 --mem=32G -t 00:45:00`, with an inner `timeout 2700`. Use `cwd` = your own dir; outputs go to your own dir, never to worker_M3_r1.
- Write the ledger "started" row with the job id (flock, `scripts/topic2_ledger.py --agent <id>`), then `scontrol release`.
- Close the row with `sacct ElapsedRaw × gres/gpu`. sacct prints KST: convert to UTC.
- After each completed batch: copy aggregates back (O12 workarounds), then re-check the cap rule.

**S6 C4 copy-back.**
- Sanitize on B300 with the ORIGINAL manifest.
- Run `scripts/topic2_id_scan.py --names-dir /scratch/data/hcp/download_HCP_REST1_filtered` on the sanitized tree: 0 hits.
- Copy back with `ssh … cat` to a local file, or with base64. Pin the output sha256.
- Checkpoints stay on B300.

**S7 Outputs.** Verdict json, a result report with the verdict per the card and what FU-C adds to r1, and an addendum for any deviation.

**Decisions to raise to root.** This is an 8-GPU per-user QOS shared by all FU teams, on the one data node. The options are:
- (a) serialize the FU teams on b300-01;
- (b) authorize `--qos=whole` and replicate the 133 GB of tensors to b300-02..04 inside B300; this needs a root/PI decision under the HCP DUT.

**Cost table (GPU-h).**

| plan | runs | estimate | vs cap 13 |
|---|---|---|---|
| fresh 10–17 (recommended) | 24 | 10.6–11.0 + env gate 0.05 | margin ≈ 2 (≈ 4 reruns) |
| reuse r1 0–4 + new 5–7 | 9 | 4.1 | margin 8.9, but optional-continuation design |
| fresh + fixture-gate rerun | 36 | ≈ 15.8 | **over cap → not launchable** |

## 5. Verification method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives rc 0 (67/67).
- `PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q verification/explorer_FU_C_r1_2/local/test_proto_fuc_verdict.py` gives 26 passed.
- `… python3 -B verification/explorer_FU_C_r1_2/local/p02_mutants.py /tmp/x.json`: 20 KILLED, baseline and F08 SURVIVED.
- `… python3 -B verification/explorer_FU_C_r1_2/local/p01_precision.py results/topic2/2026-11-01/verdict.json /tmp/p1.json` and `p05_stall_sensitivity.py`, same arguments.
- The ledger rows for Slurm job 414 (started 14:53:25Z, completed 0.05 GPU-h). On B300: `sacct -j 410,414 -X -P -o JobID,State,ElapsedRaw,AllocTRES`.
- Compare `verification/explorer_FU_C_r1_2/b300/p04_414_logs.txt` step-100/200 losses with `results/topic2/2026-11-01/runs/hcp_{E,C}_s0/train_log.jsonl`.
- These conclusions are wrong if:
  - a rebuilt venv or a full-length rerun is not bit-identical (then the gate reuse needs re-justifying, and a gate rerun does not fit the cap);
  - the r1 tensors on b300-01 are gone (VM stop) — then the raw data on `/scratch` are gone too, and FU-C is blocked pending re-staging;
  - the per-run cost under contention exceeds about 0.54 GPU-h (24 runs would then exceed 13).
