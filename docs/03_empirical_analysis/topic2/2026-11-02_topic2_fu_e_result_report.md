# Topic 2 follow-up E (FU-E) result report: frozen-encoder within-run identifiability

Author: worker_FU_E_r1, run tw-20261031-four-topics, workflow C (PI decision 7, option E). Written 2026-11-01 ~17:4x UTC.
Card: `2026-11-02_topic2_fu_e_card.md`, frozen 2026-11-01T16:22:56Z (sha256 `072553b0912a86ee786e82f13d9fdc873a6681c9ba6feb5ffc5d8e0ddc36b88f`, receipt `results/topic2/2026-11-02_fu_e/card_sha256.txt`). Every real-data number below comes from Slurm job 524, which started after the freeze, at 17:03:57Z.
Canonical outputs:
- `results/topic2/2026-11-02_fu_e/run_524/extract.json`: aggregate record, positional labels only;
- `results/topic2/2026-11-02_fu_e/verdict.json`: produced by the frozen `scripts/topic2fu_e_verdict.py`.

## 0. Verdict

**`inconclusive` (measurement capacity, card §7–8 step 3).**

The synthetic F+ gate failed for one of its 15 encoder slots. The failing slot is **hcp_S_s2**, the r1 run that stayed at the trivial solution (r1 addendum 04):
- Its F+ Idiff was 5.76, which does not exceed its permutation-null p95 of 10.59.
- The other 14 encoders were above their nulls.
- The seed-mean F+ Idiff was E 16.0, C 22.7 and S 16.5, all above the floor of 2.0.

The card requires every (arm, seed) to pass, and F+ failure maps to inconclusive. The verdict is therefore inconclusive, whatever the contrasts say.

All other gates passed:

| gate | result | numbers |
|---|---|---|
| G0 provenance | pass | 15/15 checkpoints present, sha256 = pins, run.json completed, perm buffer = run.json = perms_hcp.npz, strict load; the rescore of 16 TEST positions × 15 checkpoints reproduced the r1 test_num/test_den with max relative difference **0.0**; r1 code freeze OK |
| F+ synthetic capacity | **FAIL** | S_s2 5.76 ≤ p95 10.59; the 14 others above their nulls; seed means E 16.0 / C 22.7 / S 16.5 |
| F− anatomy only | pass | seed-mean Idiff E −2.9, C −0.9, S −1.3, each below the seed-mean null p95 (5.5 / 3.5 / 6.3) |
| G2 real capacity | pass | every E and S seed above its null; seed-mean Idiff_E 61.1 ≥ 2.0 |
| G3 raw cell-FC | pass | Idiff 64.1 > p95 5.9; identification 1.00 |

**What this adds to the r1 stop verdict.**
- Nothing governed. The downstream question, whether connectome grouping at M0 changes the identifiability of the frozen representations, **stays open**.
- The r1 `stop` (reconstruction) is unchanged.

## 1. Primary contrasts (computed; not decision-bearing because F+ failed)

Main condition: 24 held-out subjects, cov2 readout, trained encoders.

| seed | Idiff_E | Idiff_C | Idiff_S | J1 = (C−E)/E | J2 = (C−S)/S |
|---|---|---|---|---|---|
| 0 | 50.5 | 64.7 | 55.8 | +0.279 | +0.159 |
| 1 | 63.0 | 68.7 | 60.6 | +0.092 | +0.135 |
| 2 | 58.1 | 60.9 | 55.5 | +0.048 | +0.099 |
| 3 | 66.6 | 65.8 | 54.2 | −0.012 | +0.214 |
| 4 | 67.1 | 67.0 | 58.5 | −0.002 | +0.144 |

Interval estimates (t, df 4):
- **J1**: mean +0.081, 95 % t interval **[−0.066, +0.228]**.
- **J2**: mean +0.150, 95 % t interval **[+0.098, +0.202]**.

**Reading** (descriptive, not governed):
- Even if F+ had passed, J1 would map to `inconclusive` under card §8. Its interval straddles both 0 and δ = 0.01, with between-seed SD 0.118, against the about 0.008 that card §6 says `stop` would need.
- J2 is positive with its lower bound above 0: C encoders identify held-out subjects better than S encoders.
- Because J1 is undetermined, card §8 gives J2 no verdict on its own.

## 2. Descriptive outputs (card §9; no decision rides on them)

| condition / readout | E | C | S | note |
|---|---|---|---|---|
| main, trained, cov2 Idiff (top-1 acc) | 61.1 (0.59) | 65.4 (0.71) | 56.9 (0.51) | primary readout |
| main, **random-init twins**, cov2 Idiff (acc) | 53.8 (1.00) | 54.2 (1.00) | 54.4 (1.00) | init J1 [−0.003, +0.016], init J2 [−0.012, +0.002] |
| main, trained, pooled Idiff (acc) | 61.2 (0.47) | 66.2 (0.49) | 59.2 (0.38) | first-order readout |
| surrogate (per-voxel circular shift), trained cov2 | 3.9 (0.09) | 7.3 (0.13) | 6.5 (0.08) | cell-FC 0.02 (0.08) |
| subjmask (own mask, anatomy confound), trained cov2 | 66.1 (0.69) | 67.8 (0.76) | 59.7 (0.55) | cell-FC 65.6 (1.00) |
| TRAIN-64 (memorisation reading), trained cov2 | 70.4 (0.64) | 73.2 (0.75) | 65.1 (0.53) | init 49.2–49.7 (1.00); cell-FC 62.5 (1.00); all 64 done |

Arm values are seed means; accuracy is chance at about 0.04 (N = 24) or 0.016 (N = 64).

**Other descriptives.**
- **Sensitivity without seed 2** (df 3): J1 [−0.126, +0.304] and J2 [+0.107, +0.219].
- **Subject jackknife of the seed-mean J1**: SE 0.045. It is about the same size as the between-seed SE (0.053).
- **Training value** (trained − init cov2 Idiff): E +7.3, C +11.3, S +2.5 (seed means). E seed 0 (−5.1) and S seeds 0 and 3 (−0.7, −3.8) are negative.

**Reading** (descriptive):
1. **Training changes the readout, not identification as such.**
   - Random-init twins already identify every held-out subject (accuracy 1.00).
   - The trained encoders have higher Idiff but lower top-1 accuracy (0.5–0.7).
   - Training therefore spreads the similarity distribution rather than sharpening the match.
2. **The init contrasts are near 0.** With identical weights the permutation π alone changes Idiff by less than 2 %, so the trained C − S difference is acquired in training.
3. **The surrogate removes almost all identity.** Raw cell-FC falls to chance and encoder Idiff to 4–7. The real-data identity is therefore carried by cross-voxel structure (FC), not by single-voxel spectra.
4. **The anatomy confound is small at the encoder level.** Keeping subject masks raises encoder Idiff by about 2–5 points. The common mask is the governed input.
5. **TRAIN subjects are not more identifiable than held-out subjects** beyond about 9 points (70 vs 61). The memorisation reading is modest.

## 3. Deviations and incidents

1. **The B300 sharing rule was not confirmed for smoke job 499.**
   - The command chain that submitted the synthetic-only smoke job (15:56:21Z) also ran the `squeue` check for `g3t-G-E0-*` jobs. That check failed on an ssh broken pipe, and the chain went on to submit anyway.
   - sacct later showed no `g3t-G-E0-*` job since 23:00 KST, so there was no conflict.
   - Job 524 was then submitted with the check and the submit in one idempotent remote command (`verification/worker_FU_E_r1/b300/main_submit.txt`: "G3T_CHECK none 2026-11-01T16:24:31Z").
2. **The F− gate rule was changed before freezing** (card §0): from |Idiff| < 1.0 to one-sided below its null p95, after a tiny-model synthetic probe. No real data were involved.
3. **DISPATCH.md** does not copy the explorer-strategy JSON byte for byte; it points to the explorers' handoff files.
4. **One FU-E verification file was redacted.** A queue listing in `verification/worker_FU_E_r1/b300/queue_check.txt` held another team's 16-hex Slurm job tag. It was redacted, and the FU-E C4 detector stayed strict.
5. **No real-data rerun; one Slurm job each.** Job 524 COMPLETED with exit 0 and no failed extraction (all 30 encoders × 6 conditions `ok`).

## 4. Compute (C5)

| job | partition | elapsed | GPU-h |
|---|---|---|---|
| 499 smoke (synthetic) | debug | 8 s | 0.003 |
| 524 main | gpu | 1003 s (queued 39 min on QOSMaxGRESPerUser) | 0.279 |
| explorers (earlier) | debug | — | 0.015 |
| **FU-E total** | | | **0.297 of the 1.5 cap** |

- Both jobs ran on b300-01, 1 GPU each; peak GPU memory 59.6 GB in job 524.
- Ledger rows are written in `results/gpu_ledger_2026-10-31.md` under flock: a started and a completed row for each job.

**Data movement.**
- HCP data never left B300.
- Only the aggregate record (similarity matrices indexed by `test:k`, `val:k`, `train:k` and `synth:k`, plus provenance and timings) was copied back.
- Code and outputs on B300 are only under `/scratch/iitp4/fu_e/`.

## 5. Limitations

- **This is within-run split-half identifiability.** Only REST1_LR is staged, and the halves share session state. It is not test–retest fingerprinting, and the values are not comparable with literature numbers.
- **The encoders barely learned their pretext task** (r1 test NMSE 0.986–1.000), and extraction uses a zero mask while SimMIM training used 60 % masking.
- **N = 24 held-out subjects.** Relatives may straddle splits.
- **No age or sex probe was run** (card §10: labels for 28 staged subjects, ≤ 7 held out). Precise age is restricted.
- **The F+ rule is strict by design.** The gate requires every one of the 15 encoders to beat its null. It failed on the one run the r1 analysis had already flagged as stalled. A rule using seed-mean only, or dropping seed 2, would be a post hoc change and is not applied. The descriptive J1 interval would not support a decision either way.

## 6. Reproduce / verify

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-02_fu_e/output_sha256.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 scripts/topic2fu_e_verdict.py results/topic2/2026-11-02_fu_e/run_524/extract.json /tmp/fue_verdict_check.json   # recomputes verdict.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q
```

On B300, the job is `verification/worker_FU_E_r1/b300/fue_main.sbatch`: code in `/scratch/iitp4/fu_e/code`, r1 venv used read-only.
