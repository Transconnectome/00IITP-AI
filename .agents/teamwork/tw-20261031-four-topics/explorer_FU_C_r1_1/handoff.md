# handoff — explorer_FU_C_r1_1 (FU-C, Topic 2 follow-up C), Hard handoff, 2026-11-01 ~15:05Z

**Summary.** Train **8 fresh seeds (s = 5..12) × arms E, C, S** at the r1 settings, with the r1 split, eval masks and E/C partitions held fixed. Reuse the r1 F+/F− training-loop gate by hash-verified reference; the cap cannot pay for a re-run (12 runs ≈ 5.2 GPU-h). The verdict rules are the r1 §8 rules with df 7, behind a new fail-closed wrapper. Cost: 24 runs ≈ 10.6 GPU-h, inside the 13 GPU-h cap. Do NOT reuse the 5 r1 seeds as the primary analysis. A Slurm smoke on b300-01 (0.072 GPU-h) shows that the r1 pipeline reproduces **bit for bit** under Slurm. The rebuilt partitions reproduce r1 exactly, and the 8 fresh S surrogates build cleanly.

## 1. Observation

O1. r1 facts. Source: verdict.json and run.json under `results/topic2/2026-11-01/`.
- Per-seed I1 = +0.235, +0.069, +0.403, −0.035, +0.062 % (sd 0.173 %).
- I1 t95 (df 4) = [−0.068, +0.361] %. I2 = +0.47 % [+0.001, +0.95] %.
- 1 of 15 HCP runs stalled (hcp_S_s2, test NMSE 1.0000; addendum 04).
- HCP run wall time 0.429–0.460 h (from run.json `wall_sec`).
- Per-seed I1 tracks when E leaves the predict-zero plateau (addendum 05 item 5).
- I2 is confounded with box compactness (addendum 05 item 4).

O2. The frozen wrapper `scripts/topic2_verdict.py` hard-codes `HCP_SEEDS = (0..4)` and `FIX_SEEDS = (0, 1)`. Line 66 has `fm is not False`, and the test-order check is a bare `assert`. The frozen rule function `src/topic2_rgpool/stats.verdict` matches card §8 at every boundary.

O3. Synthetic power and stall probe. Files: `verification/explorer_FU_C_r1_1/probe_power/probe_power_stall.py` and `.out.json`; 20,000 simulations per cell. It imports the frozen `stats`, and its nuisance scales come from r1 aggregates only.

| design | truth I1 | stalls | P(stop) | P(keep) | median I1 CI width |
|---|---|---|---|---|---|
| D8F (8 fresh seeds, df 7) | 0.15 % (r1 mean) | none | 1.00 | 0 | 0.27 % |
| D8F | 1.0 % (= δ) | none | 0.024 | 0.50 | 0.28 % |
| D8F | 1.5 % | none | 0 | 1.00 | 0.28 % |
| D8F | 0.15 % | r1 rate (1/15) | 0.975 | 0 | 0.70 % |
| D8F | 1.5 % | r1 rate | 0 | 0.39 (+0.52 modify) | 0.85 % |
| D5+3 (5 r1 + 3 new, df 7) | 1.5 % | none | 0.001 | **0** (0.999 inconclusive) | 1.20 % |
| D5+3 | 1.0 % | none | **0.96** | 0 | 0.79 % |

- Expected half-width: 0.144 % at df 7, against 0.215 % in r1.
- P(at least one stalled E or C run among 16) = 0.67 at the r1 rate. The Wilson 95 % interval for that rate is [1.2 %, 29.8 %].
- In D5+3, 5/8 of the pooled mean is data already seen.

O4. Slurm smoke, job 401, b300-01, 1 GPU. sacct shows COMPLETED, 258 s, 0.072 GPU-h; the started and closed ledger rows are both appended. Outputs are in `verification/explorer_FU_C_r1_1/smoke/b300_out/smoke_out.json`.
- **P1.** The r1 B300 manifest matches its pin 26ba34a9…, and the split matches c13b5f21…. Relabelling the original split positionally (manifest order) equals the repo's sanitized `split.json` (sha cc521b08…) for train, val and test (64/8/16).
- **P2.** A positional data dir (symlinks h00..h87 to r1 preprocessed arrays) is complete: 88/88.
- **P3.** The train group FC matches its pin e2912ee9…. The frozen `arms()` rebuilds E, C, G, R and S_seed0..4, each **array-equal** to r1 `perms_hcp.npz` (sha ec05b796…, the same as the repo copy). Build time 1.9 s.
  - Fresh S_seed5..12 are valid: 231–232 rows changed, 1497–1572 cells moved, dispersion 1.58–1.63 (r1 S: 1.56–1.67). None equals an r1 surrogate.
  - Their perm sha256 values are listed in smoke_out.json, starting S_seed5 6ea71dea….
- **P4.** Eval-only re-scoring of the r1 checkpoints hcp_E_s0, C_s0 and S_s0 on the positional TEST set with seed 7002 gives num/den max relative difference **0.0** against the repo run.json, in the same subject order.
- **P5.** `topic2_train.py`, run for 300 steps under Slurm (steps = 8750 schedule):
  - The E s0 and C s0 losses at steps 100 and 200 equal the r1 train_log **exactly** (abs diff 0.0).
  - S s5 runs.
  - Projected 0.429–0.433 h per run (≈ 91–92 samples/s).

O5. B300 layout, read-only: `/scratch` is a node-local ext4 md0.
- HCP raw (1084 dirs) and the r1 preprocessed data (`/scratch/iitp4/worker_M3_r1/hcp`, 126 G, 88 subjects) exist **only on b300-01**. Counts on b300-02/03/04 are 0.
- Slurm 23.11.4 with cons_tres; partitions gpu (2 days), interactive (4 h), debug (30 min).
- Other FU explorers were already queueing debug and gpu jobs on b300-01.

O6. Verdict defect probe: `verification/explorer_FU_C_r1_1/verdict_probe/probe_verdict_defects.py` and `.out.json`, with synthetic records run through the frozen wrapper.

| case | frozen wrapper result | correct result |
|---|---|---|
| F+ fails and Stage 1 is not run | `no_verdict` | `inconclusive` (card §7.2) |
| F− records missing, would-be keep | `keep` | — |
| test order differs | AssertionError crash | — |
| F+ missing | `inconclusive` | — |
| F− fail with modify | modify (correct) | modify |
| failed run | no_verdict (correct) | no_verdict |
| stalled run | counted (correct) | counted |

The frozen rule function is right at each boundary:
- hi == δ is not stop;
- mean == δ with lo > 0 is keep;
- I2 lo == 0 is modify;
- I1 lo == 0 is not keep;
- an F+ gain exactly δ passes, and an F− gain exactly δ fails;
- n = 8 gives df 7.

O7. Integrity at ~15:00Z:
- C1: rc 0 (67/67).
- `code_sha256_at_freeze.txt`: 33/33. `c4_sanitized_sha256.txt`: 19/19. `output_sha256_r2.txt`: 0 failures.
- Whole-run `audit_layout.py`: no findings.
- Count-only token scan of the copied-back files: 0 token fields. The only hits are float digits and code-hash digits.
- The B300 dir `/scratch/iitp4/explorer_FU_C_r1_1` was removed (r1 data still 88/88), and no job is left in the queue.

## 2. Logic chain

L1. **Fresh seeds, not reuse** (O3).
- D5+3 is mostly determined by already-seen r1 values. At a true I1 of 1.5 % it never returns keep, and at a true I1 of δ it returns stop 96 % of the time. That makes it a continuation of r1, not a new test of the stop verdict.
- D8F is calibrated (P(stop | I1 = δ) = 2.4 %, nominal 2.5 %), has full power at 1.5 %, and is independent of r1.
- The §7 option's "df 7" is met by n = 8 fresh seeds. Its cost fits (L5).
- The pooled 13-seed analysis (5 r1 + 8 fresh, df 12) is allowed only as a labelled descriptive secondary.

L2. **The gate transfers by reference; a re-run is unaffordable** (O4, O7).
- The r1 F+/F− gate measures what the pipeline can detect at this budget, not anything about seeds 5..12.
- P3–P5 show that the FU-C pipeline is the r1 pipeline: identical partitions, bit-identical evaluation, bit-identical training trajectory, and code pins 33/33.
- Re-running the gate costs 12 × 0.43 ≈ 5.2 GPU-h, so gate plus Stage 1 ≈ 15.8 > 13.
- The wrapper must therefore load the 12 r1 fixture run.json files and check each sha256 against `results/topic2/2026-11-01/output_sha256.txt`, failing closed.

L3. **Stalls are the main threat to the "narrower interval" aim** (O1, O3).
- At the r1 stall rate, 2 in 3 designs contain a stalled E or C run, and the median I1 width grows from 0.27 % to 0.70 %. The verdict still almost certainly stays stop under r1-like truth.
- Training is bit-deterministic (P5), so rerunning a stalled seed with the same command would reproduce the stall. A stall is a property of (arm, seed), not a software failure.
- So the r1 rule stands: a stall is a valid run in the primary analysis ("same verdict rules"), with a pre-registered stall definition and sensitivity analysis.

L4. **Data and C4.**
- The positional data dir plus the repo's sanitized split gives the same training stream, masks and test order (P1, P4, P5). Every run.json written then carries only h-tokens, so no relabelling is needed on copy-back.
- The data stay on b300-01, so jobs need `--nodelist=b300-01`.
- Use hardlinks (or a full copy) into the worker's own dir. Symlinks into `worker_M3_r1` would break if root cleans that dir (addendum 05 §7 item 5).

L5. **Cost.**
- 24 runs × ~0.44 h ≈ 10.6 GPU-h (r1 measured; O4 projects 0.43 h under Slurm).
- The 13 cap must also cover the FU-C explorers' smokes (this one is 0.072; ≤ 0.75 in total), a worker anchor of ≈ 0.07, and reruns. That leaves about 1.5 GPU-h, roughly 3 reruns.
- The r1 hard timeout of 3300 s (0.92 h per run) makes a worst-case reservation exceed the cap, so a tighter per-run bound plus a cumulative guard is needed (M6).

L6. **What FU-C can and cannot change.**
- It can replicate or fail to replicate the r1 stop on independent seeds, tighten I1, and possibly resolve I1 > 0 (P = 0.55 at the r1 mean with no stalls). The last would be the qualifier "positive but sub-δ", which must be pre-worded.
- It cannot attribute I2 to FC specificity (compactness confound, no G arm), test generalisation over subjects (same 16 test subjects), or change the r1 verdict.

## 3. Caveats

- The power simulation uses a normal seed effect with sd estimated from 5 seeds (df 4), a stall model of independent runs at 1/15 per run with NMSE 1.0, and S drawn relative to C. The true seed sd and stall rate could be several times larger, which would widen intervals and raise P(inconclusive).
- P5 checks determinism only to step 200. The full 8750-step determinism and the timing under contention with other FU jobs on b300-01 are not measured.
- I ran the probe with the r1 venv, read-only. The worker must build its own lock-identical env and repeat P4/P5.
- I did not inspect the parallel teams' outputs: FU-C explorers 2/3, M3 r3, or the addendum 06 erratum wording.
- The proposal to treat missing gate evidence as no_verdict is my design choice; the card must pin it. r1's code (bool(None)) gives inconclusive.
- Whether the explorers' smokes count toward the FU-C 13 GPU-h cap is a root call; I assumed they do.
- Hardlinking into `worker_M3_r1` changes link counts only, but root may prefer a full copy.

## 4. Conclusion: strategy for the worker

**Mode and question.**
- CONFIRMATORY replication. Does C reduce held-out masked NMSE against E by ≥ δ = 1 % over 8 independent training seeds?
- I1 and I2 keep the r1 definitions. The card's §0 must disclose that every r1 number is known, and give the O3 operating characteristics as the prediction: P(stop) ≈ 1.00 under r1-like truth, 0.975 at the r1 stall rate.
- **Falsification statement:** the r1 stop is *not replicated* if FU-C returns keep, modify, or an I1 upper bound ≥ δ.

**Card contents.** New dated card, e.g. `docs/03_empirical_analysis/topic2/2026-11-0X_topic2_fuC_card.md`. Its sha256 goes in `results/topic2/<date>_fuC/card_sha256.txt` before the first Stage-1 sbatch. That receipt also pins:
- the sanitized split cc521b08…;
- r1 `perms_hcp.npz` ec05b796… for E and C, plus a new `perms_S_seed5_12.npz` (expected sha values in O4/P3);
- the 12 r1 fixture run.json sha values;
- `lock.txt` ae664dc9…, the code freeze list, and the new FU-C code.

Card §0 must also say that the partitions were built before freezing, from train-only data (no outcome).

**Design.**
- Seeds s = 5..12 for weight init, window order 1000 + s, train mask 2000 + s, and S surrogate seed s. Eval masks 7001/7002.
- Same split (dev subjects excluded), E36_d2262, 8,750 × 16 samples, and all other r1 §5 settings.
- Verdict rules = r1 §8 with a t95 interval at df 7:
  - stop iff I1 hi < δ;
  - keep iff mean ≥ δ, lo > 0 and I2 lo > 0;
  - modify iff mean ≥ δ and lo > 0 but I2 lo ≤ 0;
  - otherwise inconclusive;
  - an F− failure downgrades keep only;
  - an F+ failure gives inconclusive, even when no Stage-1 run exists;
  - missing or hash-mismatched gate evidence, any Stage-1 run not completed after one rerun, an unexpected or duplicate (arm, seed) record, or a test-order mismatch gives no_verdict, through code paths and never `assert`.
- Pre-worded qualifier: "stop; gain positive but below δ" when lo > 0 and hi < δ.

**Secondary analyses** (pre-registered, never decision-making):
- hierarchical bootstrap;
- stall table: stalled = 100-step training-loss mean never < 0.995;
- stall-excluded sensitivity, dropping whole seed triplets;
- pooled 13-seed analysis (5 r1 + 8 fresh, df 12), labelled as including seen data;
- I1_s against E's plateau-escape step;
- I2 read with the compactness confound stated.

**Must-fix items M1–M8 are in the structured return.** In short:
- fail-closed wrapper and tests for each defect class (O6 table as the oracle);
- reference gate with hash pins;
- fresh seeds only in the primary analysis;
- stalls valid, with pre-registered sensitivity;
- positional data dir under the worker's own `/scratch/iitp4` dir, `--nodelist=b300-01`, own lock-identical env plus a repeat of the P4/P5 anchors before freezing;
- cap guard: `--max-run-hours 0.5`, Slurm `--time 00:36:00`, and launch only if ledger FU-C used + in-flight × 0.6 + remaining × 0.46 ≤ 13;
- a C4 test over the new results dir;
- record `sacct` Start of every job, to prove the card freeze came before the first result.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                     # 33 OK
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_C_r1_1/probe_power/probe_power_stall.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_C_r1_1/verdict_probe/probe_verdict_defects.py
cat verification/explorer_FU_C_r1_1/smoke/b300_out/smoke_out.json; cat verification/explorer_FU_C_r1_1/smoke/sacct_401.txt
grep explorer_FU_C_r1_1 results/gpu_ledger_2026-10-31.md   # 2 rows: started + completed 0.072
```

On B300: resubmit `verification/explorer_FU_C_r1_1/smoke/smoke.sbatch` together with `probe_smoke_b300.py`, after staging the code and inputs as described in the probe docstring. Then check P1 = all true, P3 `reproduces_r1` = all true, P4 relative difference 0.0, and P5 abs diff 0.0.

These conclusions are invalidated by any of the following:
- a change to `src/topic2_rgpool` or to the frozen scripts (code pin failure);
- a worker env whose pip freeze differs from `lock.txt`;
- the P4/P5 anchors failing in the worker env (then the gate cannot be reused by reference, and the card must say so and cost a gate re-run);
- removal of the r1 data on b300-01 before the worker makes its own hardlinks or copy.
