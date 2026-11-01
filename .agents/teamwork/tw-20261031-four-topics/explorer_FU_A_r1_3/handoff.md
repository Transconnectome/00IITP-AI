# handoff — explorer_FU_A_r1_3 (FU-A, explorer 3 of 3, adversarial pre-mortem) — 2026-11-01 ~14:55Z

**Summary.** FU-A can be run and verified only if three things are fixed before the card is frozen. (1) **Cost:** the §7 estimate of 6.5 GPU-h covers Stage 1 only. The r1-style fixture gate adds about 5.2 GPU-h, so the full design comes to about 11.7 GPU-h against a cap of 8. Packing runs onto one GPU does not close the gap: measured aggregate gain is 1.08×. (2) **C4:** the HCP data on B300 sit in directories named by the unsalted content-hash tokens, and frozen `train.run` writes those names into `run.json`. Without a positional data directory, the r1 B1 leak comes back. (3) **Verdict code:** the frozen r1 verdict logic has a defect that was never listed. With no F− runs at all, it issues `keep` (probe p02 case B). With F+ failed and Stage 1 not run, it issues `no_verdict` (case A). Recommended target: the 12 mm cell mean per frame, weighted by n_c, with the input left unchanged. Do not use smoothed BOLD.

## 1. Observation

O1 — Cost. r1 run walls (`results/topic2/2026-11-01/runs/*/run.json` `wall_sec`):
- Fixture runs took 1506–1541 s and HCP runs 1544–1655 s, so one E36 140k-sample run ≈ 0.433 GPU-h.
- r1 used 12 fixture-gate runs (5.2 GPU-h) plus 15 Stage-1 runs (6.5 GPU-h).
- Result report §7 row A says "15 runs ≈ 6.5"; PI decision 7 sets the cap at 1.25 × 6.5 = 8.

O2 — Smoke test, Slurm job 403 (b300-01, debug partition, 1 GPU, 199 s, 0.056 GPU-h, ledgered start and close). Synthetic data only. Log: `verification/explorer_FU_A_r1_3/p03_b300_smoke_job403.log`.

| mode | sec/step | samples/s | peak memory | loss, first 10 → last 10 of 200 steps |
|---|---|---|---|---|
| voxel loss, noise 4.5 | 0.1809 | 88.5 | 20.8 GiB | 21.26 → 21.19 (flat) |
| cell-mean loss, noise 4.5 | 0.1802 | 88.8 | 18.3 GiB | 1.055 → 0.916 (already learning) |
| 3 processes on one GPU | 0.501 each | 95.8 aggregate | — | aggregate gain 1.08× |

Memory: r1 `HCPSource` keeps all 88 subjects on the GPU, 1.51 GB each ≈ 133 GB. So two HCP runs cannot share one GPU.

O3 — CPU probe p01 (`verification/explorer_FU_A_r1_3/p01_target_identities.out.json`; frozen code imported; synthetic data):
- (a) The ver11 voxel mask is constant inside every 6³-cell × 2-frame unit and equals the token mask. A masked cell has no visible voxel in that frame.
- (b) The decomposition Σ_v(x̂−x)² = Σ_c n_c(p_c−m_c)² + within-cell term holds exactly (relative error 0).
- (c) Cell NMSE weighted by n_c equals the voxel NMSE of the cell-mean-broadcast fields (relative difference 1.2e-7). Predicting 0 gives exactly 1.
- (d) Means pooled on the GPU grid equal the frozen `data.cell_means` (maximum absolute difference 1.5e-8).
- (e) Voxel R² on its own cell mean:

  | voxel noise | r1 F+ | r1 F− |
  |---|---|---|
  | 0.1 (r1 setting) | 0.989 | 0.984 |
  | 4.5 | 0.049 | 0.035 |
  | 4.0 | — | 0.042 |

  The noise σ needed for R² = 0.047 is ≈ 4.5 for F+ (cell variance 0.92) and ≈ 3.8 for F− (cell variance 0.62).

O4 — Real-data figures that already exist and must be disclosed in the new card §0 (they were not produced by this probe):
- `verification/challenger_M3_r1_2/b300_outputs/signal_check.json`, 4 TRAIN subjects: voxel R² on own cell mean 0.047, voxel lag-1 autocorrelation 0.043, cell-mean lag-1 autocorrelation 0.33.
- r1 Stage 0 on TEST cell means (`stage0_hcp.json`): C−E r = +0.004, pca2 = −0.052. This is real-data structure of exactly this target, and it predicts C ≤ E.

O5 — CPU probe p02: the frozen `scripts/topic2_verdict.py` run on fabricated run records (`verification/explorer_FU_A_r1_3/p02_frozen_verdict_edge_cases.out.json`):

| case | situation | frozen output |
|---|---|---|
| A | F+ failed, no Stage 1 | `no_verdict` "Stage 1 incomplete" (the card says inconclusive) |
| B | no F− runs at all | **`keep`**, because `fm is not False` treats a missing gate as a pass. Not among V01–V11. |
| C | one failed hcp run | `no_verdict` |
| D | F− failed, modify-like Stage 1 | `modify` (the r1 card downgrades only keep) |
| E | one stalled E seed | no stall guard in the logic |

O6 — B300 state, observed 14:23–14:50Z:
- Slurm partitions gpu/interactive/debug, nodes b300-01..04. The debug partition MaxTime is 30 min.
- The preprocessed HCP data exist only on **b300-01** (= .98), at `/scratch/iitp4/worker_M3_r1/hcp/subjects/<16-hex content token>/{bold_z_fp16.npy, mask.npy, cellmeans.npy}`: 88 directories, 126 GB.
- b300-02 has neither this directory nor the raw staging directory.
- B300 manifest (count-only check): n_burned_excluded = 5, n_qc_pass = 88, subjects sorted by content sha256 (True), pseudonym = sha prefix (True). So hNN = list position, as in addendum 05.
- At 14:38Z, FU-B, FU-C and FU-D smoke jobs were all on b300-01, so 15+ FU-A runs will queue against the other teams for 8 GPUs.

O7 — Frozen code facts:
- `train.run` puts the voxel loss inline (`loss = (((rec_x.float()-x)**2)*w).sum()/w.sum()`, `train.py` ~L205), so the target cannot be changed by import or monkeypatch.
- `run.json` stores `test_pseudonyms = list(te.pseudonyms)`, which are the data-directory names, and `code_sha256` covers only `src/topic2_rgpool`.
- `stats.verdict(..., fplus_gate_pass, fminus_gate_pass)` is called by the script as `bool(fp), fm is not False`.

O8 — Run ceiling: 11.73 already used + caps A 8 + B 33 + C 13 + D 25 + E 1.5 + H2 6 = 98.2 GPU-h. That is above the 95 ceiling before any verifier probe is counted.

O9 — Integrity:
- C1 rc 0. Code freeze 33/33. `c4_sanitized_sha256.txt` 19/19. `output_sha256_r2.txt` 0 failures. Card sha c9bfc60a… unchanged.
- I wrote nothing to any frozen or protected file. No git writes.
- My B300 directory was removed after the log was copied back.
- Disclosure: one `ls | head` call showed 2 of the 88 unsalted content-hash tokens in my tool output. They were not written to any file and are not repeated here. Same class as r2's N4.

## 2. Logic chain

L1 (O1, O2) — Per-run GPU time is fixed at about 0.43 GPU-h and packing gains only 8 %. So the cap allows Stage 1 (6.5) plus at most about 1.4 GPU-h for gate, smoke and reruns.

| gate design | runs | GPU-h | total with Stage 1 | fits 8? |
|---|---|---|---|---|
| G1: r1 gate (2 seeds × E/C/S × F+/F−, full budget) | 12 | 5.2 | 11.7 | no |
| G2: 1 seed, full budget, F+ E/C/S + F− E/C | 5 | 2.2 | 8.7 | no |
| G3: same at ½ budget | 5 | 1.1 | 7.6 | barely, no rerun reserve |
| G4: same at ¼ budget (2,188 steps) | 5 | ≈0.55–0.6 | ≈7.1 | yes, with 0.43 reserve for one rerun and ≈0.06 smoke |

The F− rule uses only (E−C)/E, so F− needs no S run. Before freezing, the worker should send one line to root: "FU-A full gate needs ≈11.7 (cap 8); choose G4 or a cap of ≥10 for G2." Root decides, or asks the PI. O8 shows there is no slack at run level. If root keeps 8, freeze G4 and name it a deviation from r1 §7.2: a reduced-budget, single-seed capacity check.

L2 (O3, O4) — Why the cell-mean target:
- Real voxels carry only ≈5 % cell-shared variance, which fits r1's NMSE ≈ 0.99.
- The cell mean averages 216 voxels, and its lag-1 autocorrelation is 0.33 against 0.04 for voxels. It is far less noise-dominated, and O2 shows it trains under heavy noise where the voxel loss stays flat.
- It is aligned with the tokens and mask units, so it never mixes visible and hidden voxels (p01 a). It has no free parameter. The frozen `data.cell_means` already defines it.

L3 — Why not smoothed BOLD:
- Smoothing the input lets a hidden cell's signal spill into visible neighbours.
- Smoothing only the target mixes visible neighbour voxels into the hidden cell's target.
- Either way the task becomes local interpolation. F− showed that this favours compact cubes, so the comparison is confounded.
- It also adds an FWHM choice, a forking path. Freeze ONE target; never run both and pick one.

L4 — Exact target to freeze:
- For each masked (cell c, frame t) of subject i with n_c ≥ 1 subject-brain voxels: m = mean over brain voxels of x (per-voxel z-scored 2 mm BOLD, r1 preprocessing), and p = the same mean over the decoder output x̂.
- Weight n_c. NMSE_cell = Σ n_c(p−m)² / Σ n_c m², pooled per seed exactly as r1 §6.
- Training loss: Σ n_c(p−m)² / Σ n_c over masked units.
- Pooling is done in fp32 after `rec.float()`, with subject brain masks, not the group mask.
- Input, model, mask ratio, mask unit, seeds, budget, lr schedule, windows, split and eval seeds 7001/7002: all identical to r1.

L5 (O7) — Code path:
- New code goes only in own paths: a training loop that imports `HCPSource`, `FixtureSource`, `build_simmim`, `lr_at`, `simmim_masks` and `code_hashes` and adds a `target ∈ {voxel, cell}` switch.
- Must-pass test: in voxel mode on the CPU tiny config, the loop gives losses and `test_num`/`test_den` bit-identical to frozen `train.run`.
- In cell mode, the per-run target equals `cellmeans.npy` within 1e-5. Run this check on B300 on TRAIN subjects only, reporting a boolean.
- `run.json` must add `target`, the FU-A card sha, and hashes of the new modules.

L6 (O6, O7) — C4:
- Build, on B300 only, a directory `/scratch/iitp4/<fu-a worker>/hcp_pos/subjects/hNN` → the r1 subject directories, with h = position in the original manifest list (sorted by sha, O6).
- Use the repo's sanitized `split.json` (pinned in `c4_sanitized_sha256.txt`) as `--split-file`. `run.json` then carries only hNN tokens, and `split_file_sha256` can be verified from the repo.
- Verify on B300, count-only: (i) the hNN train/val/test sets mapped through the symlinks equal the sealed original split; (ii) the 88 content tokens appear 0 times in FU-A results, logs and metadata.
- Never `ls -l` or log symlink targets. Write no per-subject n_c, voxel count or timing.
- Do NOT rerun preprocessing: the 5-subject dev exclusion is already in the 88 (O6), so the sealed salt is not needed.
- Stay on b300-01 with `-w b300-01`. If the data must be copied to another B300 node, state that in the card (it stays on B300).

L7 (O5) — The FU-A verdict code must be new and table-driven, with the gate evaluated FIRST:

| state | verdict |
|---|---|
| any gate run software-failed after one rerun | no_verdict |
| F+ completed and failed | inconclusive (capacity), Stage 1 not launched |
| F− missing | never counts as pass: keep and modify are impossible → inconclusive |
| F− failed | downgrade keep — and, recommended, also modify (justify as a deviation), or keep the r1 rule; either way, code = card |

Boundaries, each tested exactly at and off the boundary:
- stop iff hi < δ;
- keep iff mean ≥ δ and lo > 0 and I2 lo > 0;
- F+ passes iff both gains ≥ δ;
- F− passes iff gain < δ.

Assertions the script must make:
- `target == "cell"` and the card sha in every `run.json`, so r1 voxel runs named `hcp_E_s0` can never be mixed in;
- identical test order across arms;
- NMSE = Σnum / Σden equals `test_nmse`.

Mutants to kill: V01–V11 plus N-B (missing F− = pass), N-A (F+ fail → no_verdict), N-T (wrong target accepted) and N-Z (stall clause removed).

L8 (r1 addendum 04 + O2) — Stall clause:
- A stalled run in E would fake a C win; a stalled run in C would fake a stop.
- Pre-register: a stall is final val NMSE ≥ 0.999. It is a valid run (as in r1). The verdict is recomputed with that seed dropped from all arms; if the two verdicts differ, the result is inconclusive.

L9 (O3e) — Gate adaptation:
- Use the r1 fixture generators with voxel noise σ calibrated per fixture so that voxel R² on own cell mean ≈ 0.047 (σ ≈ 4.5 for F+, ≈ 3.8 for F−). Report that cell-target noise is about σ²/216.
- Reuse the r1 fixture perms (pinned) only after a CPU check that FC from the noisy fixture's cell means still gives C purity ≥ 0.95. Otherwise rebuild with the frozen builder.
- Pass rules are unchanged; the eval metric is the cell NMSE.

L10 (O4, C3) — Freeze order and disclosure:
- Allowed before the card sha receipt: synthetic data only. No r1 checkpoint scored on the cell metric, and no real-data cell-target number.
- If other FU teams' probes (e.g. FU-C re-scoring r1 checkpoints) produce such a number first, disclose it in §0.
- Scoring the r1 E/C/S checkpoints with the cell metric (eval-only, ≈0.03 GPU-h) is useful as a pre-registered DESCRIPTIVE secondary: it separates the effect of the metric from the effect of training. Report voxel NMSE of the FU-A runs too (descriptive). Report absolute ΔNMSE and explained-variance units, because relative NMSE on a smaller denominator mechanically enlarges relative gains.

## 3. Caveats
- The G4 cost assumes fixture runs scale linearly with steps (≈0.18 s/step + eval). Not measured beyond 200 steps.
- A ¼-budget gate may fail where full budget would pass. That gives an honest but lost "inconclusive". I did not run a gate pilot; that would cost more than this probe's budget.
- Whether explorer and verifier smokes count against the FU-A 8 GPU-h is unspecified. With 3 explorers at ≤0.25 each, the G4 margin narrows to about 0.
- Stall rate under the cell loss is unknown; 200 steps say nothing about it.
- I did not check other teams' code paths. FU-C also builds an hNN data directory, and a shared one would need root coordination.
- The 0.047 figure comes from 4 TRAIN subjects and 20k sampled voxels, by another agent.

## 4. Conclusion
Recommend this order:
1. Raise the cost decision to root; default G4 if the cap stays at 8.
2. Freeze a card with the L4 target, the L8 stall clause, the L7 verdict table, the L9 gate and §0 disclosures (O4, plus any FU-C real-data numbers).
3. Write the sha receipt in `results/topic2/<date>_fu_a/`.
4. Run the gate on b300-01 via sbatch; launch Stage 1 only if the gate passes, with ledger rows carrying Slurm job ids and sacct Elapsed.
5. Compute the verdict, run the C4 scan, then write the report.

The r1 stop verdict stays untouched; FU-A speaks only to the 12 mm cell target. Root should also forward O5 case B (missing F− → keep in the frozen r1 script) to the M3 r3 gate-repair team as an erratum candidate.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_A_r1_3/p01_target_identities.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_A_r1_3/p02_frozen_verdict_edge_cases.py   # case B must print keep
cat verification/explorer_FU_A_r1_3/p03_b300_smoke_job403.log ; grep explorer_FU_A_r1_3 results/gpu_ledger_2026-10-31.md
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | grep -c ': OK'   # 33
```
Any of the following would invalidate parts of this report:
- the per-run wall time changes by more than 20 % under Slurm or contention;
- root changes the cap;
- the r1 HCP directory on b300-01 is deleted or wiped (then use the sealed-manifest-based reselection on fresh preprocessing).
