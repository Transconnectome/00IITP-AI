# Topic 2 follow-up D (FU-D) result report: E192 scale, connectome box grouping at M0

Date: 2026-11-02 (KST). Author: worker_FU_D_r1, run tw-20261031-four-topics, milestone FU_D (PI decision 7, r1 result report §7 option D).
Governing card: `2026-11-02_topic2_fu_d_card.md`, sha256 `1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b`, frozen 2026-11-01T16:06:07Z (`results/topic2/2026-11-02_fu_d/card_sha256.txt`), before any FU-D run. FU-D code frozen at the same time (`code_sha256_at_freeze.txt`, 29 files).
All numbers below come from this run's dated outputs in `results/topic2/2026-11-02_fu_d/` (C8), or, where marked "r1", from the frozen r1 outputs in `results/topic2/2026-11-01/`. Nothing is taken from `EMPIRICAL_ANALYSIS_REPORT.md`.

## 0. Verdict

**`inconclusive` (measurement capacity) under the frozen FU-D card, §8 step 2.** At SwiFT ver11 E192 d2-2-18-2 (474,226,176 parameters) and the r1 budget (8,750 × 16 = 140k samples), the F+ training-loop gate failed: on the synthetic stream with strong planted, spatially scattered 8-cell networks, connectome boxes at M0 lowered the test NMSE by only **0.36 %** against PatchMergingV2 cubes and **0.65 %** against the FC-shuffle null, both below δ = 1 %.

- **Stage 1 (HCP) was not run**, as the card requires. No E192 model was trained or evaluated on HCP data, and no seed plan was written (the seed rule applies only after an F+ pass).
- **What it means.** At E192 and this budget, the training loop cannot turn even a strong, known grouping signal into a gain of δ. A Stage-1 `stop` at E192 would therefore have been uninterpretable (it could be a false kill caused by measurement incapacity), so FU-D makes no claim about real-data grouping at E192.
- **What it adds to the r1 verdict.** The r1 E36 `stop` (I1 +0.147 % [−0.068 %, +0.361 %] < δ) stands as recorded and alone (card §9 c: "E192 adds no decision"). FU-D does add one descriptive fact about the measurement apparatus: the gain from M0 grouping on the planted F+ signal **shrinks with scale**, from +2.77 % (r1 E36, seed 0) to +0.36 % (E192, seed 0) against cubes (§2). Within this architecture family and budget, a larger model therefore does not open a window in which M0 grouping becomes testable; it closes it further.
- GPU use: 3.575 GPU-h by this worker (smoke 0.040 + gate 3.535), 3.672 GPU-h for FU-D including the explorers' 0.097, against the 25 GPU-h cap.

## 1. What was run (card §10.1, §7.1)

| step | job | what | result |
|---|---|---|---|
| env | — (CPU, login shell) | own venv `/scratch/iitp4/fu_d/venv` from the r1 lock | `pip freeze` identical to `scripts/b300_env/lock.txt` (`logs/env_check.json`) |
| view | — (CPU) | positional hard-link view of the r1 preprocessed HCP arrays | manifest, original split and sanitized split sha256 as pinned; mapped split = sanitized split (train/val/test, order); 88 subjects, 176 links, all sharing the r1 inodes (`logs/view_check.json`) |
| smoke (i) | Slurm 511, debug | frozen `evaluate_hcp` of the r1 `hcp_E_s0` E36 checkpoint through the FU-D view | test NMSE 0.9908706340280367 reproduced **exactly**; per-subject num/den equal; test order equal (`smoke/equiv.json`) |
| smoke (ii) | Slurm 511 | E192 HCP training loop, arm C seed 0, aborted by the throughput probe at step 200 (no evaluation) | 0.4962 s/step (32.25 samples/s), data load 20 s, projected 1.213 h per run (`smoke/run.json`) |
| F+ gate | Slurm 534, 535, 536, gpu | E, C, S × seed 0, synthetic F+ stream, full budget | all `completed`, Slurm COMPLETED, wrapper post-checks pass (cfg E192, 474,226,176 parameters, frozen r1 code hashes); 1.175 / 1.180 / 1.180 GPU-h |

Every job ran on b300-01 through `sbatch` (`scripts/topic2fu_d_slurm.py`): B300-share check before each submission (no `g3t-G-E0-*` job was pending or running at any submission), cost guard, held submission, ledger "started" row with the job id, release; "completed" rows with sacct ElapsedRaw × GPUs (rounded up, KST converted to UTC). Every copy-back passed the B300 count-only C4 scan with 0 hits (`logs/scan/`).

## 2. F+ gate at E192 (card §7.1)

Test NMSE over 16 × 32 fixed synthetic windows (eval seed 7002), seed 0 (`runs/Fplus_*_s0/run.json`; gate computed by `scripts/topic2fu_d_verdict.py`, cross-checked with the frozen r1 `stats.gate_fixture`, which gives the same values and `pass: False`).

| scale | E (cubes) | C (connectome boxes) | S (FC-shuffle null) | (E−C)/E | (S−C)/S | rule (both ≥ δ = 1 %) |
|---|---|---|---|---|---|---|
| **E192 (FU-D)** | 0.65585 | 0.65347 | 0.65777 | **+0.36 %** | **+0.65 %** | **fail** |
| E36 (r1, seed 0, descriptive) | 0.67693 | 0.65817 | 0.67783 | +2.77 % | +2.90 % | pass |

Validation NMSE (4 groups × 32 synthetic windows, eval seed 7001):

| step | 2188 | 4375 | 6562 | 8750 |
|---|---|---|---|---|
| E | 0.6913 | 0.6715 | 0.6604 | 0.6565 |
| C | 0.6867 | 0.6672 | 0.6579 | 0.6543 |
| S | 0.6925 | 0.6739 | 0.6625 | 0.6583 |

Reading (descriptive, no decision rides on it):
- The ordering C < E < S holds at every validation step and on test, so the box gather still carries the planted structure in the right direction; its size is what fails.
- Most of the change is on the cube side: E192 with cubes reconstructs the F+ stream better than E36 with cubes (0.6558 vs 0.6769, −3.1 %), while E192 with connectome boxes is only slightly better than E36 with boxes (0.6535 vs 0.6582, −0.7 %). A plausible reading — not tested here — is that the wider M0 projection (1536→384) and the 18 stage-2 blocks recover much of the scattered-network structure after a compact merge, so the grouping choice at M0 matters less.
- Training losses (last 100 steps) E 0.6190, C 0.6170, S 0.6207; all runs finite, none near the predict-zero solution.

## 3. Verdict mapping applied (card §8)

`results/topic2/2026-11-02_fu_d/verdict.json` (`scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989b…b84e`):
- Step 1: all three F+ runs `completed` (no rerun needed).
- Step 2: F+ computed and failed → **`inconclusive`**, reason "measurement-capacity gate failed (F+ fixture at E192); Stage 1 not read". No Stage-1 record exists (`protocol_flag` absent); `needs_fminus` false; no F− run.
- Joint reading with r1 (card §9 c): "E192 adds no decision; the r1 E36 stop stands alone".

## 4. Compute (C5)

| item | Slurm job | GPU-h (sacct) |
|---|---|---|
| explorers (synthetic smokes, before the card) | 396, 404, 418, 430 | 0.097 |
| smoke (equivalence + cost probe) | 511 | 0.040 |
| F+ gate E / C / S | 534 / 535 / 536 | 1.175 / 1.180 / 1.180 |
| **FU-D total** | | **3.672 of 25** |

Run ledger total at the gate's close: 30.665 GPU-h of the 95 GPU-h ceiling (all teams). Queue: each FU-D job waited 21–71 min in `QOSMaxGRESPerUser` (the 8-GPU limit of the shared Slurm user); wall-clock is not a failure under the B300-share rule. Real per-run cost at E192 (1.18 GPU-h) agrees with the explorers' synthetic projection (1.19–1.23).

## 5. Costed options (not run; any of them needs a new dated card and a PI decision)

| option | what | runs | est. GPU-h |
|---|---|---|---|
| D′ (as planned) | run Stage 1 at E192 anyway | 15 (+1 rerun) | ≈ 19–20 |
| D-gate-seeds | F+ at E192 with seeds 1, 2 to check whether the 0.36 % is seed noise | 6 | ≈ 7.1 |
| D-mid | intermediate scale (e.g. E96, same depths) to locate where F+ stops passing | 3 (gate) + 15 | ≈ 2 + ≈ 9–10 |
| D-long | E192 at 4× budget (560k samples) | 3 (gate) + 15 | ≈ 14 + ≈ 72 |

- D′ is **not recommended**: under the frozen card a Stage-1 result at E192 cannot be read without an F+ pass.
- D-gate-seeds is unlikely to change the decision: at E36 the two F+ seeds gave C-vs-E gains of +2.77 % and +3.35 % (a 0.58-point spread), while the E192 seed-0 gain is 0.64 points below δ, so two more seeds would have to average about +1.3 % to pass. It is still the cheapest way to make the gate failure more robust.
- D-long exceeds the FU-D cap and, with FU-B, the run ceiling.
- Lowering δ (PI decision 3) would be a change of the decision criterion, not of the experiment, and would have to be decided before any Stage-1 number.

## 6. Limitations

- One F+ seed (card §7.1, cost; pre-registered). The decision is categorical under the card; the margin to δ is large (0.36 % vs 1 %).
- The gate is synthetic (12 mm planted networks, about 42 % of cell variance, r1 fixture generator). It bounds measurement capacity for a strong signal; it says nothing direct about HCP BOLD.
- Untuned E192 at the r1 budget; VRABES's mask ratio and learning rate were not adopted (card §2), to keep scale the only change.
- The real-data cost probe trained 200 steps on HCP data after the freeze (projection only, no evaluation, no decision).

## 7. Reproduce / verify

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_d/card_sha256.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_d/output_sha256.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic2fu_d_verdict.py \
    --wrapper-sha256 $(grep topic2fu_d_train.py results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt | cut -d' ' -f1) \
    --out /tmp/fud_verdict_check.json      # verdict inconclusive, gate gains 0.00363 / 0.00655
grep worker_FU_D_r1 results/gpu_ledger_2026-10-31.md
```

Checkpoints of the three F+ runs (`model_final.pt`, 1.9 GB each) and the positional view stay on B300 b300-01 under `/scratch/iitp4/fu_d/` (node-local; may be wiped on VM stop).
