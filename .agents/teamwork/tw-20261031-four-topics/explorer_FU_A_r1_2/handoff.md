# Handoff — explorer_FU_A_r1_2 (FU-A, Topic 2 follow-up A; explorer 2 of 3; lens: feasibility and failure modes)
Written 2026-11-01 ~15:20Z. Type: explorer analysis (recommendation only; no production code written, no git writes).

**Summary.**
FU-A is feasible and cheap to engineer. Use the 12 mm cell means as both input and target, stored as a compact cell store (0.9 GB in place of 133 GB), so the run can go on any B300 node. Training goes through the frozen r1 `train.run` with no change to the loop.

The plan does **not fit the 8 GPU-h cap** once the fixture gate is counted. §7's 6.5 GPU-h covers Stage 1 only. The cheapest faithful plan costs 10.8 GPU-h (10 gate runs + 15 Stage-1 runs × 0.43). The smoke test shows co-locating runs on one GPU saves at most 4 %. Recommendation: freeze the card, run the gate wave (4.3 GPU-h, inside the cap), and have root ask the PI for a FU-A cap of 12 GPU-h before Stage 1.

## 1. Observation

**Code reality (frozen r1, read-only; `code_sha256_at_freeze.txt` 33/33 OK, C1 0 non-OK lines)**
- O1 `src/topic2_rgpool/train.py` `run()`: the loss is `(((rec_x.float() - x) ** 2) * w)` with `x` returned by `tr.batch()`, the same tensor that is fed as input. Evaluation (`evaluate_hcp`, `evaluate_fixture` → `masked_sq_terms(rec, x, ...)`) does the same. Input = target is hard-wired.
- O2 `run()` looks up the module globals `HCPSource` and `FixtureSource` at call time. A wrapper that rebinds `train.HCPSource` / `train.FixtureSource` reuses the whole pinned loop without editing it.
- O3 `HCPSource` puts every subject on the GPU as (N, 1200, 78, 96, 84) fp16. For 88 subjects that is ≈133 GB, and on B300 that data sits only in `b300-01:/scratch/iitp4/worker_M3_r1/hcp/subjects/<pseudonym>/` (126 GB).
- O4 `scripts/topic2_preprocess_hcp.py` already saved `cellmeans.npy` (4096 × 1200 float32 = mean over the subject's brain voxels of each padded 6³ cell, `data.cell_means`) and `mask.npy` per subject.
- O5 The repo `results/topic2/2026-11-01/split.json` is C4-sanitized:
  - tokens h00..h87 = position in the original manifest's `subjects` list, which is sorted by content sha256 (addendum 05 §2);
  - the original split and manifest exist only off-repo / on B300 (`worker_M3_r1/hcp/manifest.json`, `worker_M3_r2/sealed_c4`).
- O6 `run()` writes `rec["test_pseudonyms"] = list(te.pseudonyms)`, i.e. the subject-directory names, into `run.json`.
- O7 `scripts/topic2_launch_wave.py` launches directly via setsid on idle GPUs. That path is forbidden now that B300 runs Slurm.
- O8 `scripts/topic2_verdict.py` + `stats.verdict`:
  - `bool(fp)` / `fm is not False` mean a missing F− counts as a pass;
  - F+ failure with no Stage 1 returns `no_verdict`, while the card says inconclusive (challenger_M3_r2_2 case A);
  - `--delta` is a CLI default.
- O9 `perms_hcp.npz` keys: E, C, S_seed0..4, G, R, nvox, group_mask (sha ec05b796…2b34, equal to `perm_file_sha256` in r1 `runs/hcp_*/run.json`). `perms_Fplus.npz` has `labels`; F+ and F− have S_seed0/1.

**Measured cost**
- O10 The 27 r1 runs (12 fixture + 15 hcp) each took 1506–1655 s wall on one B300 GPU, about 0.43 GPU-h per run (`results/topic2/2026-11-01/runs/*/run.json` `wall_sec`; ledger waves 3.41/3.43/3.50/1.35).
  - HCP data loading took 21–29 s; the throughput probe at step 200 measured 0.176–0.186 s/step.
- O11 GPU smoke, Slurm job 427, b300-02, debug partition, 1 GPU, 266 s = 0.074 GPU-h, ledgered (start and close rows). Synthetic random cell store only. Log: `verification/explorer_FU_A_r1_2/b300_smoke_427.log`.

  | co-located processes | aggregate samples/s | per-process median s/step |
  |---|---|---|
  | 1 | 94.6 | 0.169 |
  | 2 | 97.6 | 0.328 |
  | 3 | 98.6 | 0.487 |

  - The GPU is saturated: co-location gains ≤ 4 %.
  - Peak memory is 22.0 GiB per process with the compact store.
  - The cell-store broadcast costs 2.3 ms per batch.
  - An earlier explorer_M3_r1_1 smoke log shows the same saturation: bs 8 → 16 raised samples/s only from 91.7 to 100.6.

**Data probe: B300 CPU, Slurm job 405 on b300-01, 0 GPU, 8 TRAIN subjects by the public split rule, aggregates only**
- O12 `verification/explorer_FU_A_r1_2/b300_probe_cellmean_predictability.out.json`. The target is per-cell re-standardised cell means; the NMSE is weighted by brain-voxel count, under r1 SimMIM masks (1 cell × 2 frames, ratio 0.6).

  | quantity | value |
  |---|---|
  | median raw cell-mean SD, signal cells (voxel z units) | 0.136 |
  | median lag-1 autocorrelation, cell target | 0.243 |
  | median lag-1 autocorrelation, 2 mm voxel | 0.018 |
  | NMSE, zero predictor | 1.000 |
  | NMSE, temporal copy of nearest visible frame | 1.488 |
  | NMSE, mean of visible face neighbours | 1.106 |
  | NMSE, 2-feature least squares (fit on one half of subjects, scored on the other) | 0.864 / 0.875 |
  | NMSE, 2 mm voxel temporal copy (comparison) | 1.904 |

**Local CPU probes (synthetic only)**
- O13 `verification/explorer_FU_A_r1_2/probe_target_alignment.py` → `.out.json`:
  - P1 idempotence `cell_means(broadcast(u)) == u`: max error 9.8e-4 (fp16). The pad-offset mutant gives error 4.4–4.7 → killed.
  - P2 patch-constant target: range 0.0. The mutant gives 5.0–5.8 → killed.
  - P3 a compact `CellStoreSource.batch()` is bit-identical (max |Δ| 0.0, equal brain masks) to frozen `train.HCPSource.batch()` on materialised data.
  - P4 per-cell SD is 1 ± 1e-7, and the zero predictor gives NMSE 1.0.
  - Storage per subject: 9.8 MB compact fp16 vs 1.51 GB materialised.
- O14 `verification/explorer_FU_A_r1_2/probe_verdict_mutants.py` → `.out.json`: the proposed verdict (`proposed_verdict_fua.py`) passes all 16 guards, and **13/13 mutants are killed**:
  - V01–V11;
  - case A (F+ fail → no_verdict);
  - δ changed from 0.01.
  - First attempt: with boundary fixtures 1.0 vs 0.99, the four ≥/> mutants V01, V02, V04 and V05 **survived**, because (1.0 − 0.99)/1.0 = 0.010000000000000009 > 0.01. With 100.0 vs 99.0 (exactly 0.01) they are killed.

**B300 / Slurm logistics**
- O15 sinfo shows partitions gpu (2 d), interactive (4 h) and debug (30 min, default 15 min), b300-[01-04], 8 GPUs each, DefCpuPerGPU 24. /etc/hosts maps b300-01 = cloud-S1HDe3 = 61.107.201.98.
- O16 b300-02..04 have no `/scratch/iitp4` and no `/scratch/data/hcp`. /scratch and /home are node-local (md0 / vda1); there is no shared filesystem. Slurm `-o` logs land on the compute node.
- O17 `scripts/b300_env/build_env.sh` built a working venv on b300-02 in under 1 min (srun, CPU): torch 2.15.0+cu134, numpy 2.5.4, scipy 1.18.1, nibabel 5.4.2, einops 0.8.2, monai 1.6.1, the same pins as `lock.txt`.
- O18 Transfers:
  - Piping stdin through the ssh mux, or `srun ... < file`, produced 0-byte files twice.
  - `scp` with the ControlMaster, and inter-node `srun -w b300-02 scp b300-01:<file>`, worked (sha256 verified).
- O19 ssh:
  - The configured `ProxyJump dgx1,connectome` times out during banner exchange.
  - `-J connectome` works. A ControlMaster needs a short socket path (< ~100 chars) and still broke three times; long commands should be detached.
  - sacct prints KST, which must be converted to UTC for the ledger.
- O20 During this probe, 6+ GPU smokes from the other FU teams ran on b300-01, because the HCP data is only there.

**r1 learning curves on fixtures (`runs/F*/run.json`)**
- O21 The F+ gain grows with budget. At step 2188 (val): C vs E +2.1 %, C vs S +1.2 %. At step 8750 (test): +3.06 % / +2.93 %. The per-seed test gains are 2.76 % / 3.35 % (C vs E) and 2.89 % / 2.97 % (C vs S).

**r1 Stage 0 used the same 12 mm cell series as the FU-A target**
- O22 `stage0_hcp.json` reports C vs E: r +0.004 [0.0005, 0.0074], pca2 −0.052 [−0.053, −0.050].

## 2. Logic chain

1. The target type. From O1 and O2, the only way to reuse the pinned loop unchanged is input = target = a transformed volume. A "2 mm input, 12 mm target" design would need a forked training loop, which is new governed code with divergence risk. **Recommend input = target = 12 mm cell signal.**
2. Which 12 mm signal.
   - From O4, the cell means already exist, and they are the same series on which the C/S partitions were built (card §3) and Stage 0 was computed (O22). Using them isolates the target change while keeping the partitions identical (reuse the pinned perms, O9).
   - Smoothed BOLD would need about 126 GB of new derived data, which could live only on b300-01 (O3, O16). It would also add free choices (FWHM, masked smoothing at the brain edge) and would not match the partition's FC. Reject it, and record the rejection in the card (no forking).
3. Re-standardisation. Raw cell means have SD ≈ 0.136 (O12), so without rescaling the loss scale drops about 50× versus r1, which changes the untuned dynamics. Partial edge cells would also keep voxel-scale variance and dominate the NMSE. A per-cell temporal z-score over the full run gives unit variance per cell and voxel-count weighting, and keeps all r1 hyperparameters meaningful (P4).
4. The question is now meaningful. A trivial 2-feature linear predictor reaches NMSE ≈ 0.87 on the cell target, against ≥ 1.0 for every trivial predictor at 2 mm (O12) and ≈ 0.99 for the r1 models.
   - The raw SD implies a mean within-cell voxel correlation of only ≈ (0.136² − 1/216)/(1 − 1/216) ≈ 0.014: 2 mm z-voxels are ≈ 99 % unshared variance. This explains the r1 NMSE ≈ 0.99 quantitatively.
   - δ = 1 % relative is then about 0.008–0.009 absolute NMSE, a sizeable share of the learnable variance. The FU-A test is therefore not noise-dominated.
5. Engineering of the cell store.
   - From O3 and O13 (P3), the compact store gives bit-identical batches at 1/150 of the memory. Data can be copied to b300-02..04 (≈ 0.9 GB total; O18), each node needs a 1-minute venv (O17), and the runs avoid the b300-01 contention (O20).
   - From O5 and O6, naming the derived subject directories by the positional token (h00..h87) makes `test_pseudonyms` positional by construction (C4), and lets the sanitized repo `split.json` be the split file directly.
6. Cost.
   - O10 and O11 give 0.42–0.43 GPU-h per full-budget run, and co-location cannot reduce it (≤ 4 %).
   - Gate options:
     - the full r1-shaped gate (12 runs) + Stage 1 (15) = 27 runs = 11.6 GPU-h;
     - the minimal faithful gate keeps the r1 two-seed rule but drops F−/S, which the F− rule never uses: 10 + 15 = 25 runs = 10.8 GPU-h;
     - a 1-seed gate: 5 + 15 = 20 runs = 8.6 GPU-h.
   - A shortened gate is weaker and could fail spuriously: C vs S is only +1.2 % at 1/4 budget (O21). **No faithful design fits 8 GPU-h.**
   - The gate is needed under every option, and an F+ failure ends FU-A inside the cap. So gate first, then a cap decision for Stage 1.
7. Verdict code. The O8 defect classes are reachable in r1-style code; O14 shows a precedence that kills all of them. Boundary fixtures must use exactly representable values, or ≥/> mutants survive (an observed failure of a test design).
8. Fixture adaptation.
   - The r1 fixture volumes are cell signal + 0.1 voxel noise (1 % of variance). The FU-A transform T (block mean over each padded 6³ patch's in-mask voxels, broadcast) removes that noise.
   - The adapted gate is therefore close to the r1 gate. Expect it to pass with margin (per-seed gains ≥ 2.76 % at full budget, O21), but it must still be run, because T is new code.
   - A silently unapplied T (wrapper not rebinding `train.FixtureSource`) would train on almost identical data and pass unnoticed. It needs a patch-constancy check (P2) on a sampled batch in every run, logged in the run record.
9. Prior expectation, to be disclosed in card §0.
   - r1 Stage 0 on exactly this series: pca2 C < E in 16/16 subjects (O22).
   - A linear 8C→2C merge keeps less of a C box than of a cube.
   - So the r1 evidence predicts stop or inconclusive for FU-A too. The card is confirmatory, and this prior must be stated before freezing.

## 3. Caveats

- The predictability probe used 8 TRAIN subjects (arm-independent, no partition, no model). It is real-data exposure before the card and must be disclosed in card §0. No test or val subject was read.
- The probe's "voxel-count weight" ignores the partial-cell asymmetry between subjects. The within-cell correlation estimate (0.014) is approximate because cells hold < 216 brain voxels.
- The smoke used a random cell store and an ellipsoid mask, not HCP masks, and ran 250 steps (full runs: 8750 steps + 4 val evals + test eval). Per-run cost is taken from the 27 measured r1 runs, not from the smoke. The compact store looked about 4 % faster per step (0.169 vs 0.176 s), which I did not count as savings.
- I did not test the full wrapper (monkeypatched `train.run`) end-to-end on GPU. P3 tests only `batch()` equivalence on CPU.
- I did not check FU-B's "positional hard-link farm" (seen in a ledger row). If both teams derive h-token directories, they should agree on the same token map (manifest order). Coordinate only via root.
- The run ceiling: 11.73 + FU caps (A 8, B 33, C 13, D 25, E 1.5) = 92.2 GPU-h. A FU-A raise to 12 gives 96.2 > 95 unless another FU underspends; FU-C can reuse the r1 gate (same target and budget) and save about 5 GPU-h. That is root's / the PI's call.
- Residual state, not cleaned (`rm -rf` was denied by the permission classifier). `/scratch/iitp4/explorer_FU_A_r1_2/` exists on b300-01 (code copy, `code.tar`, logs, `smoke.sbatch`, an empty `build_env.sh`) and on b300-02 (`venv`, `uvcache`, `code`, `smoke_427.log`). Neither holds HCP data, subject tokens or IDs. Root may remove them, or the worker may reuse the b300-02 venv (built from the repo recipe).
- No processes or Slurm jobs of mine remain: jobs 405, 409, 427 and the srun steps all ended.

## 4. Conclusion: recommended strategy for the FU-A worker

**Paths.** All new, none overlapping M3 r3:
- `src/topic2_fua/` (`target.py`, `sources.py`, `verdict.py`);
- `scripts/topic2_fua_{build_cells,train,verdict,sbatch}.py|.sh`;
- `tests/topic2_fua/`;
- `docs/03_empirical_analysis/topic2/2026-11-0X_topic2_fua_card.md` (+ addenda);
- `results/topic2/2026-11-0X_fua/`.

Import `src/topic2_rgpool` read-only and never touch `tests/topic2_rgpool` (owned by M3 r3).

**A. Card (F1).** Write it, run the CPU fixtures, pin `card_sha256.txt` + `code_sha256_at_freeze.txt` + perms/split shas in the FU-A results dir, all BEFORE the first HCP training step.

The target:
- u_i,c,t = (m_i,c,t − mean_t m_i,c) / sd_t(m_i,c), where m = r1 `cellmeans.npy` (mean over subject i's brain voxels of padded 6³ cell c of the r1 per-voxel z-scored BOLD; full 1200-TR run);
- cells with no brain voxel, or with sd = 0, are 0;
- input = target = u broadcast to the cell's brain voxels in the padded 96³ grid (stored fp16);
- NMSE = r1 §6 formula on this target, i.e. a cell-level NMSE weighted by brain-voxel count.

Fixture transform T: block mean of the r1 generator volume over each patch's in-mask voxels, broadcast and masked. There is no re-z, because the r1 cell signals already have unit variance by construction.

Everything else is r1-identical and stated as such:
- E36_d2262;
- 8,750 × 16;
- lr 2e-4, warmup 5 %, cosine, wd 0.05, bf16, clip 1.0;
- seeds s, 1000+s, 2000+s, 3000+s; eval masks 7001/7002;
- arms E / C / S_seed{s} from the pinned `perms_hcp.npz`;
- the sanitized 64/8/16 split (dev exclusion inherited);
- δ = 0.01 frozen;
- I1, I2, t95 df 4, hierarchical bootstrap secondary.

§0 discloses:
- this probe (8 TRAIN subjects, arm-independent);
- the r1 results, including the Stage-0 pca2 prior that predicts stop;
- the r1 fixture results.

**B. Verdict precedence.** Copy it from `verification/explorer_FU_A_r1_2/proposed_verdict_fua.py` and freeze it in the card:
1. gate incomplete after one rerun → no_verdict;
2. F+ fail → inconclusive, with no Stage-1 dependence;
3. Stage 1 incomplete after one rerun → no_verdict;
4. test-order mismatch → raise;
5. stop iff hi(I1) < δ; keep iff mean ≥ δ ∧ lo(I1) > 0 ∧ lo(I2) > 0; modify iff mean ≥ δ ∧ lo(I1) > 0 ∧ lo(I2) ≤ 0; else inconclusive;
6. F− fail downgrades keep only.

Also pre-register these descriptive items, none of which changes the category:
- premise flag P: seed-mean NMSE_E ≤ 0.95;
- stall: final val NMSE ≥ 0.999. A stalled run is valid, as in r1, with a pre-specified sensitivity analysis without stalled seeds;
- the label `not_run_budget` if Stage 1 cannot be launched within the approved cap.

**C. Gate (F2/F3).** 10 runs at full budget:
- F+ E, C, S_seed{s} and F− E, C;
- s ∈ {0, 1};
- the r1 rule on the seed mean: F+ passes iff both gains ≥ δ; F− passes iff the C vs E gain < δ.

Do not shorten the budget (O21).

**D. Tests that must fail on the targeted defect.** Prototypes are in `verification/explorer_FU_A_r1_2/`.
- T1 idempotence + patch constancy (pad-offset mutant killed).
- T2 compact `CellStoreSource.batch()` bit-identical to `train.HCPSource.batch()` on materialised data.
- T3 unit SD per cell (no-re-z mutant killed).
- T4 the wrapper's rebinding is effective:
  - a tiny-config CPU `train.run` with `--source Fplus` whose sampled batches are patch-constant;
  - the run record carries `fua_target="cell12_restd"` + FU-A code hashes;
  - a mutant that skips the rebinding must fail.
- T5 C4: every token in `run.json` matches `^h\d\d$`; the h-token map equals the manifest-order rule (checked on B300 in memory, booleans only).
- T6 perm provenance: each FU-A run's `perm_sha256` equals the r1 `run.json` `perm_sha256` of the same arm/seed.
- T7 verdict guards g01–g16 with exactly representable boundaries (100 vs 99); 13 named mutants killed.
- T8 no regression: r1 33/33 freeze, C1, all receipts.

**E. B300 logistics.**
1. CPU srun on b300-01 builds `fua_cells/subjects/hNN/{cells_fp16.npy (1200 × 4096), mask.npy}` (≈ 0.9 GB) from the r1 cellmeans. Directory names are positional, derived in memory from the manifest order, and no name is printed.
2. Pull the store to b300-02/03/04 by `srun -w <node> scp b300-01:…`, and verify sha256.
3. Build the venv with `scripts/b300_env/build_env.sh` on each node (< 1 min).
4. Run `sbatch --array` on partition **gpu** (debug is capped at 30 min, too tight for a 26–28 min run):
   - `--gres=gpu:1 -c 8 --mem=64G -t 01:00:00`;
   - inner hard timeout 3300 s; keep the r1 throughput abort (0.75 h at step 200);
   - pin `-w` to nodes that hold the store.
5. Ledger rows: a "started" row at submit; a close row from sacct ElapsedRaw (KST→UTC).
6. Copy back only `run.json` / `train_log.jsonl` / aggregates after every wave (/scratch can be wiped). HCP stays on B300.
7. Use `ssh -J connectome` with a ControlMaster at a short path; use scp, not stdin pipes; detach long jobs.

**F. Sequencing and cap.**
- Wave 1 = the gate (10 runs ≈ 4.3 GPU-h, inside cap 8).
- If F+ fails → verdict inconclusive, and FU-A is done inside the cap.
- If F+ passes → Stage 1 needs 6.5 GPU-h more (total ≈ 10.8). **Do not launch** it unless root/PI has raised the FU-A cap. Recommended: 12 GPU-h (10.8 + one rerun 0.43 + margin).
- If the cap is not raised → deliver card + implementation + gate + costed plan, label `not_run_budget` (T2.3-style escape).

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # expect 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | grep -c ': OK$'                       # expect 33
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_A_r1_2/probe_target_alignment.py   # verdict: all true
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_A_r1_2/probe_verdict_mutants.py    # baseline_all_pass true, n_killed 13/13
python3 -c "import json,glob;print(sorted(json.load(open(p))['wall_sec'] for p in glob.glob('results/topic2/2026-11-01/runs/*/run.json')))"  # 27 runs, 1506-1655 s
grep explorer_FU_A_r1_2 results/gpu_ledger_2026-10-31.md      # 2 rows: started 15:02:50Z, completed 0.074 GPU-h (job 427)
```

On B300 (`ssh -J connectome connectome@61.107.201.98`):
- `sacct -j 405,427 -X -o JobID,State,ElapsedRaw,NodeList,AllocTRES`;
- `sinfo`;
- the b300-02..04 checks: `srun -p debug -w b300-0N ls /scratch/iitp4` → absent.

Invalidation conditions:
- Any frozen r1 file changes.
- B300 gains a shared filesystem, or HCP is staged on other nodes.
- The PI changes the FU-A cap.
- An HCP mask/cell difference makes P3 fail on real data. The worker must rerun T2 on one real subject inside a B300 CPU job.
