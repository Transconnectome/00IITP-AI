# Handoff (Hard) — explorer_FU_A_r1_1, milestone FU_A (Topic 2 follow-up A), 2026-11-01 ~15:00Z

**Summary.**
- Target: use the 12 mm cell mean of r1's per-voxel z-scored BOLD (exactly r1's `D.cell_means`, already stored as `cellmeans.npy` on b300-01) as both SimMIM input and target. Scale it by one global TRAIN-only constant.
- Reject Gaussian-smoothed BOLD. Under a pure null it creates a cube advantage and leaks masked content (p02).
- Keep everything else from r1 byte-identical: perms, split, seeds, masks, budget, E36.
- Add a pre-registered premise check: a `stop` needs seed-mean VAL NMSE_E ≤ 1/(1+10δ) = 0.909.
- **Blocking cost problem.** Full-budget fixture gates plus 15 Stage-1 runs need about 11–12 GPU-h, and the FU-A cap is 8. Reduced-budget gates are not valid (r1 learning curves). Root must choose a pre-registered tier (below) before the card is frozen.
- GPU used by me: 0 GPU-h (no ledger row). explorer_FU_A_r1_3 holds the FU-A Slurm smoke (job 403).

## 1. Observation

O1. **r1 per-run cost.**
- 27 r1 runs took 1506–1655 s wall each (`results/topic2/2026-11-01/runs/*/run.json` `wall_sec`; ledger rows: wave1 3.41 GPU-h / 8 runs, wave4 1.35 / 3).
- That is ≈ 0.43–0.45 GPU-h per E36 140k-sample run.
- Data load is only 21 s (`runs/hcp_E_s0/train_log.jsonl` `data_loaded sec 21.2`). Steps take 0.175 s (`throughput_probe`).
- So a lighter cell-mean data path does not lower the per-run cost.

O2. **Packing headroom is small.** explorer_M3_r1_1 smoke (`verification/explorer_M3_r1_1/smoke_b300_steptime.log`): E36 at bs 8 gives 90.9 samples/s and 10.1 GiB; at bs 16, 100.6 samples/s and 19.7 GiB. Doubling the batch adds only ~10 % throughput, so the GPU is close to saturated. explorer_FU_A_r1_3's ledgered smoke (job 403) measures 3 processes per GPU directly.

O3. **r1 fixture learning curves** (seed means, from the run.json `val_nmse_curve`):

| step | F+ (E−C)/E | F+ (S−C)/S | F− (E−C)/E |
|---|---|---|---|
| 2188 | +2.09 % | +1.18 % | −5.49 % |
| 4375 | +2.61 % | +2.03 % | −2.91 % |
| 6562 | +2.87 % | +2.71 % | −2.10 % |
| 8750 | +2.92 % | +2.81 % | −1.73 % |

The F+ separation grows with training. The F− bias shrinks toward 0.

O4. **TRAIN-only real-data design statistics already seen** (`verification/challenger_M3_r1_2/b300_outputs/signal_check.json`, 4 TRAIN subjects): voxel lag-1 AC 0.043, 12 mm cell-mean lag-1 AC 0.331, voxel R² on its own cell mean 0.047. reviewer_M3_r1_1 also measured a voxel-target temporal-interpolation baseline on TEST: NMSE 1.312 (`verification/reviewer_M3_r1_1/b300_gpu_check.json`).

O5. **r1 Stage 0 already scored this exact target domain** (12 mm cell series of the same 16 TEST subjects; result report §4):
- C − E: r +0.004 [0.0005, 0.0074]; pca2 −0.052 [−0.053, −0.050], 0/16 subjects.
- C − S: r +0.071.

O6. **ver11 masking.** SimMIM replaces masked tokens after patch embedding (`vendor_swift_ver11/simmim_swin4d_transformer_ver11.py:1319-1321`, `x = x*(1-w) + mask_token*w`). One token = one 6³ cell × 1 frame, and the mask unit is 1 cell × 2 frames (`train.py` T_UNIT=2). `D.cell_means` pads to 96³ and averages exactly the 6³ patch cells (`data.py:57-69`).

O7. **p01, B300 read-only, stdlib, booleans only.** The original r1 split on b300-01 (`/scratch/iitp4/worker_M3_r1/code/split.json`, 16-hex tokens) maps exactly onto the repo's sanitized split by rank: h-token = "h%02d" % rank in the sorted 88 pseudonyms.
- train, val and test each map: true.
- All 88 subjects have `cellmeans.npy` and `mask.npy`.
- The pseudonyms are also the subject directory names under `/scratch/iitp4/worker_M3_r1/hcp/subjects/`.
- .98 = b300-01 (192.168.0.2). `/scratch` is node-local md0 ext4. Slurm partitions gpu/interactive/debug (debug MaxTime 30 min); all 4 nodes idle at ~14:2xZ.

O8. **p02 (CPU, synthetic iid voxel noise on the r1 TRAIN group mask with the r1 E/C/S perms; `verification/explorer_FU_A_r1_1/out/p02_smoothing_bias.json`, T=150).**

| target construction | r_E − r_C (null) | r_C − r_S | leak corr (masked cell → processed neighbour) |
|---|---|---|---|
| 12 mm block mean | −0.0007 | −0.0001 | −0.003 |
| Gaussian FWHM 6 mm, then block mean | **+0.043** | +0.009 | **0.085** |
| Gaussian FWHM 12 mm, then block mean | **+0.128** | +0.025 | **0.186** |

O9. **p03 (CPU, synthetic; `out/p03_calibrated_fixture.json`).**
- Voxel noise is calibrated to ρ = 0.047: σ_v² = (1−ρ)/(ρ − 1/n̄), with n̄ = 216, gives σ_v = 4.74.

| fixture, level | C purity | r: E / C / G / S | r_C − max(E,G) |
|---|---|---|---|
| F+ noise-free | 1.00 | 0.090 / 0.425 / 0.073 / 0.043 | +0.335 |
| F+ 12 mm cell mean, calibrated | **1.00** | 0.078 / 0.375 / 0.063 / 0.039 | **+0.297** |
| F+ single voxel, calibrated | 0.77 | 0.005 / 0.011 / 0.003 / 0.000 | **+0.006** |
| F− 12 mm cell mean, calibrated | — | 0.550 / 0.470 / 0.479 / 0.469 | −0.080 |
| F− single voxel, calibrated | — | 0.022 / 0.013 / 0.017 / 0.013 | −0.009 |

O10. **p04.** `verification/explorer_FU_A_r1_1/proposed_fu_a_verdict_sketch.py` (proposal, not production) passes a 22-case truth table. It kills all 15 one-line mutants in `out/p04_sketch_mutants.json`: V07 analog, case A, V08/V09 analogs, every boundary, F− missing, F− ignored, the r1 keep-only downgrade, and the premise mutants.

O11. **Integrity.**
- C1 rc 0. `code_sha256_at_freeze.txt` 33/33 OK. `output_sha256_r2.txt` 156/156 OK.
- No production file changed and no git writes.
- B300 probe dir `/scratch/iitp4/explorer_FU_A_r1_1` and the `/tmp` copies are removed.

O12. **Ledger.** 11.99 GPU-h completed at ~14:40Z. Caps: 11.73 + A 8 + B 33 + C 13 + D 25 + E 1.5 + H2 6 = 98.2 GPU-h, which is above the 95 GPU-h run ceiling.

## 2. Logic Chain

L1 (O6, O8). **Choose 12 mm block means, not Gaussian smoothing.**
- Patch-aligned block averaging mixes nothing across cell boundaries, so no masked content reaches visible tokens. Gaussian smoothing does both: it leaks (O8 leak 0.085 / 0.186), and it injects distance-decaying correlation that favours compact cubes even under a null (+0.043 / +0.128).
- For scale, the whole real C-vs-E Stage-0 difference is +0.004 (O5).
- So smoothing would bias the comparison toward a `stop` by construction.

L2 (O6). **Use the cell mean as both input and target (SimMIM reconstructs its own input).**
- This keeps FU-A a single-factor change relative to r1: the spatial resolution of the data.
- The alternative, 2 mm input with a 12 mm target, changes two things (adds a denoising objective) and is rejected.
- The target is `κ · cm_{i,c,t}`:
  - `cm = D.cell_means` (stored `cellmeans.npy`, mean over the subject's brain voxels of each 6³ cell);
  - broadcast to the cell's brain voxels;
  - κ = 1 / RMS over TRAIN subjects × group signal cells (nvox ≥ 54) × all TRs, one global constant frozen before any result.
- κ restores r1's input scale. NMSE is computed the same way as r1: frozen `metrics.masked_sq_terms` against this target, voxel-weighted, masked in-brain.
- No per-cell z-score: that would up-weight low-coherence, noise-rich cells, which works against the option's purpose.

L3 (O7). **Reuse r1's data and arms unchanged.**
- The r1 preprocessed cell means are the target. Keep:
  - `perms_hcp.npz` (sha ec05b796…, built from TRAIN 12 mm cell FC);
  - the split (64/8/16, dev-5 already excluded from the 88);
  - seeds (weights s, order 1000+s, train masks 2000+s, eval 7001/7002) and E36 at 8,750 × 16.
- The only changed factor is then the target, and the FU-A runs are seed- and mask-paired with r1.
- No new subjects: that would add preprocessing and the dev-salt exclusion path.

L4 (O7). **C4 hazard.** The B300 subject directories are named by the old unsalted 16-hex pseudonyms. Copying frozen `train.run` would write `rec["test_pseudonyms"] = te.pseudonyms` into run.json, which is the r1 B1 defect again. The rank map in p01 gives a verified fix: the worker builds a data dir of positional h-token symlinks (or maps in memory) and never copies the original split or manifest.

L5 (O4, O9). **The fixtures must be noise-calibrated to test the option-A premise.**
- At real voxel noise (σ_v ≈ 4.7) the planted F+ grouping is invisible at single-voxel level (+0.006, purity 0.77) but intact at 12 mm (+0.297, purity 1.00).
- So an F+ gate with calibrated voxel noise, run through the FU-A block-mean code path, checks three things:
  - that the new target code really averages (a voxel target leaking through would collapse the signal);
  - alignment (an off-by-pad average would smear cells);
  - perm wiring.
- r1's fixtures (noise 0.1) could not check these.
- F− stays a valid bias check: C never beats the cubes there.
- Caveat: the planted F+ effect is much stronger than in real data (planted within-network r 0.42). Passing it shows capacity for a strong signal only.

L6 (O3). **Reduced-budget gates are invalid.**
- At step 2188, F+ C-vs-S is +1.18 %, barely above δ. A quarter-budget F+ gate would be falsely pessimistic.
- F− bias moves toward 0 with training, so a short F− gate would be anti-conservative.
- Therefore the gates need the full Stage-1 budget.

L7 (O1–O3, O12). **Cost against the cap** (0.44 GPU-h per full run):

| plan | runs | GPU-h |
|---|---|---|
| r1-equivalent gates (F+ E/C/S ×2, F− E/C/S ×2) + Stage 1 | 27 | ≈ 11.9 |
| minimal sound: F+ E/C/S ×2, F− E/C ×2 (S is not used by the F− rule) + Stage 1 | 25 | ≈ 11.0 (+ one rerun reserve 0.44) |
| 1-seed gates: F+ E/C/S s0 + F− E/C s0 + Stage 1 | 20 | ≈ 8.8 |
| F+ s0 only (F− evidence carried over from r1's full-budget F−) + Stage 1 | 18 | ≈ 7.9 |

- Only the last plan fits in 8, with no rerun margin.
- Packing factor f (aggregate throughput of k processes on one GPU, divided by one process) changes this: the 20-run plan fits if f ≥ 1.12, and the 25-run plan if f ≥ 1.40. O2 suggests f is small.
- §7's 6.5 GPU-h estimate omitted the mandatory new-target gates, and the run ceiling is already over-allocated (O12).

L8 (O5). **Pre-registered prediction, disclosed honestly.** Stage-0 pca2 for C is below E in 16/16 TEST subjects on the very FU-A target. This predicts that the linear 8C→2C merge keeps less for C, so the expected outcome is stop or inconclusive. The card must state this prediction before freezing, so that a keep would contradict the a-priori evidence.

L9 (O4). **Premise check.**
- The option-A question needs a target that is not noise-dominated. If it is still noise-dominated, a `stop` is uninformative, as in r1 (addendum 02 §3).
- The threshold comes from δ: a 1 % relative gain should be ≤ 10 % of arm E's explained variance. That gives 1 − N ≥ 10·δ·N, i.e. N ≤ 1/(1+10δ) = 0.9091.
- The check is applied to VAL, not TEST.
- It is asymmetric: the premise is needed only to claim a null (`stop`). A detected effect (keep/modify) is guarded by F+/F− instead.

L10 (O10). **Verdict ordering.** It closes every named r1 defect class:
- a missing gate or a failed run is no_verdict;
- a completed F+ that fails gives inconclusive, whatever Stage-1 data exist (case A, V11);
- a missing F− is not a pass (r1's `fm is not False` treats None as pass, another instance of the same class);
- every boundary is pinned;
- F− failure downgrades keep **and** modify. This deviates from r1 §7.2 on purpose: both claim C > E, which is exactly what F− tests. The card must say it explicitly, and a test must pin it.

## 3. Caveats

- I computed no real-data outcome. κ, the 64-subject ρ, and every real NMSE are left to the worker. ρ = 0.047 comes from 4 TRAIN subjects (challenger_M3_r1_2); the worker should recompute it on all 64 TRAIN subjects before freezing and disclose it in card §0.
- Packing factor f is not measured by me. Use explorer_FU_A_r1_3's job-403 numbers.
- p03 simulates cell means analytically, using block mean of iid noise = N(0, σ²/n). It is not a full voxel-volume pass through the GPU path.
- The calibrated fixture is matched at voxel level only. Real cell means may also carry cell-coherent noise that the fixture lacks, so the fixture SNR at 12 mm is probably optimistic.
- The 0.909 premise threshold is a derived convention, not an empirical constant. If it fails, the result is "inconclusive (premise)" and it points to option B or D.
- The FU-A TEST subjects were already seen at the 12 mm level by r1 Stage 0. No FU-A tuning uses them. A fresh test set was considered and rejected (new preprocessing, dev-salt path, breaks the r1 pairing). Disclose instead.
- Whether explorer smokes count against the FU-A 8 GPU-h cap is unstated. I assumed they might.
- Not inspected: peer FU-A explorers' folders (kept independent); challenger_M3_r1_2's nearest-unmasked-frame baseline values (the card should disclose that they exist).

## 4. Conclusion — strategy for the FU-A worker

**S0. Root decision first (blocking).** Pick the compute tier before writing the card's §10:

| tier | gates | when it applies |
|---|---|---|
| T1 (preferred) | F+cal E/C/S × s{0,1} + F−cal E/C × s{0,1}, full budget, + Stage 1 15 + one rerun reserve ≈ 11.5 GPU-h | cap raised to ~12 (e.g. from FU-C slack if FU-C reuses r1 seeds 0–4), or measured f ≥ 1.40 |
| T2 | F+cal E/C/S s0 + F−cal E/C s0 | f ≥ 1.12 |
| T3 (fits 8 at f = 1, zero rerun margin) | F+cal E/C/S s0 only, F− bias evidence carried over from r1's full-budget F− (−1.73 %) as a declared deviation | otherwise |

- If even T3 cannot be launched within the cap: deliver card + implementation + fixtures + costed plan (T2.3 escape) and run nothing on real data.
- Never use reduced-step gates (L6).

**S1. New dated card**, `docs/03_empirical_analysis/topic2/2026-11-0X_topic2_fuA_card.md`. Freeze it with a sha256 receipt in `results/topic2/2026-11-0X_fuA/card_sha256.txt` before any real-data result. It must contain:
- (a) Target, exactly as in L2. The primary metric is NMSE_12mm.
- (b) The single changed factor versus r1, and everything kept identical (L3), with hashes:
  - perms_hcp.npz ec05b796…;
  - split.json c13b5f21… (sealed original; the repo copy is sanitized);
  - code_sha256_at_freeze, card c9bfc60a….
- (c) Arms E / C / S_seed{s}, 5 seeds, δ = 1 % (decision 3), primary 95 % t on seed contrasts (df 4); secondary hierarchical bootstrap.
- (d) Fixture gates F+cal and F−cal through the same block-mean code:
  - voxel noise σ_v² = (1−ρ)/(ρ − 1/216), with ρ from all 64 TRAIN subjects;
  - fixture C/S perms rebuilt from block-averaged noisy fixture-train data, F+ purity ≥ 0.95 required;
  - r1 §7.1/§7.2 pass rules unchanged; seeds and runs per the chosen tier.
- (e) Premise check M: seed-mean final VAL NMSE_E ≤ 1/(1+10δ).
- (f) The verdict ordering of L10 / `proposed_fu_a_verdict_sketch.py`:
  - **stop** = hi(I1) < δ and M passes; hi(I1) < δ with M failing = inconclusive (premise);
  - **keep** = mean ≥ δ, lo(I1) > 0, lo(I2) > 0;
  - **modify** = mean ≥ δ and lo(I1) > 0, with lo(I2) ≤ 0;
  - F− fail → keep/modify become inconclusive;
  - missing or failed runs → no_verdict; a completed F+ that fails → inconclusive.
- (g) Stalled runs (val NMSE ≥ 0.999 throughout) are valid runs. Pre-register a drop-stalled-seed sensitivity as secondary.
- (h) The §0 disclosure list: O4, O5, r1 verdict/NMSEs, verifier baselines, explorer smokes, this report's p02/p03.
- (i) The pre-registered prediction of L8.
- (j) A joint-reading table with r1:

| r1 | FU-A | reading |
|---|---|---|
| stop | stop | the r1 null is not a 2 mm-noise artefact |
| stop | keep | noise masked an FC-specific gain; scope 12 mm |
| stop | modify | a non-compact-grouping gain, not FC-specific |
| stop | inconclusive (premise) | next lever is B/D |
| stop | inconclusive (straddle) | next lever is C |
| stop | inconclusive (F+) | measurement capacity |
| stop | no_verdict | software |

  In every row the r1 verdict stays as recorded.
- (k) Descriptive TEST baselines, computed after the freeze: predict-0, and same-cell nearest/linear temporal interpolation on the same masks.

**S2. Implementation** only in the worker's own paths (e.g. `src/topic2_fuA/`, `scripts/topic2_fuA_*.py`, `tests/topic2_fuA/`), importing r1 modules read-only:
- one `block_mean_volume(x, brain)` used by both the HCP and the fixture paths;
- an HCP source that reads only `cellmeans.npy` + `mask.npy`;
- a new train loop that passes the target explicitly and writes positional tokens only (L4);
- its own verdict script.

Tests (CPU):
- `block_mean_volume` equals the broadcast of `D.cell_means` on HCP-format arrays (pad and axis alignment), and returns piecewise-constant values exactly;
- calibrated §7.1-style fixtures as in O9: F+ purity ≥ 0.95 and r_C ≥ max(E,G) + 0.10 at 12 mm; F− r_C ≤ r_G + 0.02 and ≤ r_E + 0.02; NULL |r| ≤ 0.02; single-voxel F+ advantage < 0.10, recorded as the premise fixture;
- a target-leak test: perturbing a masked cell's voxels leaves every visible token's input unchanged;
- the verdict truth table (p04 style) plus a mutation run with 0 survivors;
- the run.json token test: no 16-hex pseudonym can be written.

**S3. Runs** on b300-01 via sbatch (node-local data: use `-w b300-01`), one ledger row per job under flock, gates first.
- Stage 1 starts only after the F+ gate has been computed and has passed.
- Before copying anything back: frozen `scripts/topic2_id_scan.py` on B300, plus a count-only scan for the 88 original tokens.
- Results go in `results/topic2/2026-11-0X_fuA/`, followed by a result report giving the verdict per the card and the joint reading with r1.

## 5. Verification Method

- Rerun the probes (CPU, synthetic, a few minutes each), from `cd /home/juke/git/00IITP-AI/verification/explorer_FU_A_r1_1`:
  - `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B p02_smoothing_bias_probe.py`, expecting block E−C ≈ 0 and Gaussian E−C > 0.03 with leak > 0.05;
  - `... -B p03_calibrated_fixture_probe.py`, expecting σ_v ≈ 4.74, F+ 12 mm purity 1.0 and +0.30, single-voxel +0.006;
  - `... -B proposed_fu_a_verdict_sketch.py` (rc 0, 22/22) and `... -B p04_mutate_sketch.py` (15/15 killed).
- Rerun p01 on b300-01: copy `p01_split_map_check.py` and `results/topic2/2026-11-01/split.json` into a scratch dir and run `python3 p01_split_map_check.py split.json`. All values should be true, and the script prints booleans only.
- Cost numbers: the `wall_sec` of `results/topic2/2026-11-01/runs/*/run.json`, plus `results/gpu_ledger_2026-10-31.md` (job 403 for f).
- Learning curves: `val_nmse_curve` of the `runs/F*` records (the snippet in progress.md reproduces O3).
- Integrity:
  - `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` (rc 0);
  - `grep -v '^#' results/topic2/2026-11-01/code_sha256_at_freeze.txt | sha256sum -c` (33 OK).
- What would invalidate this report:
  - f measured ≥ 1.4 (then T1 fits without a cap change);
  - ρ on 64 TRAIN subjects far from 0.047 (recompute σ_v);
  - frozen r1 modules changed (the code-freeze pin fails).
