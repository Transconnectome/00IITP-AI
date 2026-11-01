# Topic 2 (M3) result report: connectome box grouping at SwiFT ver11's first merge

Date: 2026-11-01. Author: worker_M3_r1, run tw-20261031-four-topics. Governing card: `2026-11-01_topic2_card.md` (sha256 `c9bfc60a…41f5`, frozen 03:14:34Z, before any real-data statistic). Deviations and post-freeze additions: `2026-11-01_topic2_addendum_01.md` and `_02.md`.
All numbers below come from this run's dated outputs in `results/topic2/2026-11-01/` (C8). None are taken from `EMPIRICAL_ANALYSIS_REPORT.md`.

## 0. Verdict

STAGE1_VERDICT_PLACEHOLDER

## 1. T2.1 — where ver11 merges space (code, not docs)

The full text is in `2026-11-01_topic2_architecture.md`; tests pin it.

**Three 2×2×2 spatial merges, none in time.**
- M0: 16³→8³ (12→24 mm cells).
- M1: 8³→4³.
- M2: 4³→2³.
- Each is `Linear(8C→2C)` after `LayerNorm(8C)`.

**There is no merge after stage 3.** `layer_2` (after M2) and `layer_3` (stage-3 blocks plus final LayerNorm) share the same 2³×20 grid. In E192 both are 1536-d. So the old premise, "Euclidean PatchMerging between layer_2 and layer_3, both 1536-d", is false.

**Decoder.** The SimMIM 'mlp' decoder rebuilds each 48³ octant per frame from that octant's one final token.

**Where the intervention goes.** M0 is the only merge with room to regroup. On this run's training-split group mask, 1,442 of 4,096 stage-0 cells touch the brain, 1,195 are signal cells, and 234 of 512 M0 blocks touch the brain and can be regrouped. C regroups 231 of them; S regroups 231–232.

**Other code facts.**
- `use_post_norm=True` crashes.
- The perlmutter fork of SwiFT was not inspected.

## 2. T2.2 — question, card, implementation, fixtures

**Question** (card §1). SwiFT ver11 is trained from scratch with SimMIM on HCP-YA REST1_LR. Does grouping 12 mm cells into connectome boxes at M0 lower the held-out masked in-brain NMSE?
- Comparison 1, the practical claim: against stock PatchMergingV2 (arm E).
- Comparison 2, the connectome-specific claim: against the same builder run on a distance-binned FC-shuffle surrogate (arm S).
- Everything else is matched: parameters, tokens, FLOPs, data order, masks, initial weights, budget and seeds.

**Implementation** (`src/topic2_rgpool/`).
- `ConnectomeRGBoxPooling` is a parameter-free per-frame gather π placed in front of an unchanged ver11 PatchMergingV2. It is injected through ver11's own `downsample` argument, and the vendored ver11 is byte-identical to the source.
- With π = identity it is bit-identical to PatchMergingV2, and the full E-arm model is bit-identical to stock ver11.
- For a given seed, every arm starts from bit-identical weights.

**Boxes.**
- Each box holds 8 cells and stays inside its octant.
- Boxes are placed on output cells by Hungarian matching of centroids; cells go to child slots by a canonical Hungarian slot order.
- C uses dense-core, mean-linkage balanced growth in correlation distance on the train-only group FC. This is a named deviation from Song 2005 box covering: a fixed size instead of a fixed diameter.

**Tests:** `tests/topic2_rgpool/`, TESTCOUNT_PLACEHOLDER tests.
- Shapes and stage table.
- Bijection and octant locality.
- Box content and slot order, permutation equivariance, time locality, gradient flow.
- Parameter and FLOP equality.
- Step-0 weight pairing across arms, E-arm bit identity, and decoder locality.
- Patch-embedding token order.
- A structural leakage test: perturbing val or test data leaves π unchanged; perturbing train data changes it.
- Data contract, split, masks and statistics rules.
- C4 output checks.

**Mutants: each check fails on its target defect.**

| check | mutants it rejects |
|---|---|
| box-content check | inverse permutation, silent identity, permute-after-merge, time-mixing |
| time-locality check | time-mixing |
| regroup check | silent identity |
| constructor | non-bijections (duplicate, short, out of range) |
| `validate_perm` | cross-octant and non-bijective π |
| F+ purity fixture | the defective periphery-seed / max-linkage growth rule (purity < 0.95; the correct rule reaches 1.00) |

### 2.1 CPU synthetic fixtures (card §7.1)

All boxes are built on fixture-train data and scored held-out; numbers from `verification/worker_M3_r1/probe_stage0_fixture_numbers.out.json`.

| fixture | E r / pca2 | C r / pca2 | G r / pca2 | R r / pca2 | pass rule | result |
|---|---|---|---|---|---|---|
| F+ planted networks | 0.092 / 0.434 | **0.428 / 0.582** (purity 1.00) | 0.075 / 0.360 | 0.034 / 0.333 | purity ≥ 0.95; r_C ≥ max(E,G) + 0.10 | pass |
| F− smooth field | **0.662 / 0.802** | 0.566 / 0.760 | 0.576 / 0.761 | 0.200 / 0.528 | r_C ≤ r_G + 0.02 and ≤ r_E + 0.02 | pass |
| NULL iid | −0.002 | 0.001 | 0.000 | −0.001 | \|r\| ≤ 0.02 | pass |

### 2.2 Training-loop gate (card §7.2): passed, so Stage 1 was run

Twelve runs on B300: arms E, C and S × seeds 0 and 1 × fixtures F+ and F−. Each used the full Stage-1 budget and settings: 8,750 steps at batch 16. Test NMSE was computed over 512 fixed synthetic windows. Run records are in `results/topic2/2026-11-01/runs/F*`; the gate is computed by `scripts/topic2_verdict.py`.

| fixture | E (s0, s1) | C (s0, s1) | S (s0, s1) | gain C vs E | gain C vs S | rule | result |
|---|---|---|---|---|---|---|---|
| F+ | 0.6769, 0.6803 | **0.6582, 0.6575** | 0.6778, 0.6776 | **+3.06 %** | **+2.93 %** | both ≥ δ = 1 % | **pass** |
| F− | **0.2379, 0.2408** | 0.2409, 0.2461 | 0.2397, 0.2478 | −1.74 % | +0.10 % | C vs E < δ | **pass** |

- **F+.** With FC that carries information beyond distance, connectome boxes lower the test NMSE by about 3 % against both PatchMergingV2 and the FC-shuffle null, in both seeds.
  - At this budget, the training loop and the box gather can therefore turn a strong planted grouping signal into a gain of at least δ.
  - That signal is defined at 12 mm cell level and carries about 42 % of each cell's variance.
  - **The gate says nothing about sensitivity on real 2 mm BOLD.** Voxel noise dominates the reconstruction target there (§3), and that gap is a limit of the G6 design.
- **F−.** With FC that is a function of distance only, connectome boxes do *worse* than PatchMergingV2's cubes, by 1.7 %, and tie with the null. The pipeline therefore does not manufacture an advantage for C.

STAGE1_PLACEHOLDER

## 4. Stage 0 (descriptive only; card §9, Option B)

This stage asks how much signal each partition keeps inside a box. The data are the 12 mm cell time series of the 16 TEST subjects. The PCA basis is fitted on the 64 TRAIN subjects. Output: `results/topic2/2026-11-01/stage0_hcp.json`.

| arm | held-out within-box r | pca2 (share of within-box variance kept by top-2 PCs) | box dispersion (cells) |
|---|---|---|---|
| E (cubes) | 0.257 | **0.530** | 0.78 |
| C (connectome) | **0.261** | 0.478 | 1.47 |
| S (FC-shuffle null, mean of 5 surrogates) | 0.189 | 0.447 | 1.56–1.67 |
| G (Euclidean growth) | 0.233 | 0.474 | 1.11 |
| R (random) | 0.132 | 0.400 | 2.46 |

Paired-subject bootstrap 95 % CIs (16 subjects):

| contrast | metric | difference | 95 % CI | subjects |
|---|---|---|---|---|
| C − S | r | +0.071 | [0.067, 0.076] | 16/16 |
| C − S | pca2 | +0.031 | [0.029, 0.034] | 16/16 |
| C − E | r | +0.004 | [0.0005, 0.0074] | 11/16 |
| C − E | pca2 | −0.052 | [−0.053, −0.050] | 0/16 |

**Reading.**
- The training-split FC carries real grouping information beyond distance decay, since C ≫ S on both metrics.
- At 12 mm, C does not exceed PatchMergingV2's compact cubes:
  - it is about equal on mean pairwise correlation;
  - it is clearly worse on the 2-component share, which is the quantity that a linear 8C→2C reduction can keep.
- Addendum 02 §1 records that the card names no governing Stage-0 metric, and that the two metrics disagree on C vs E.

## 5. Compute (C5)

**Hardware and environment.**
- All B300 work ran on node 61.107.201.98 only.
- nvidia-smi was checked immediately before every launch by `scripts/topic2_launch_wave.py`, and only idle GPUs were used.
- No other user's process was touched.
- The environment is project-local at `/scratch/iitp4/worker_M3_r1/venv`; recipe and lock: `scripts/b300_env/`.

**Ledger.** Every launch has a "started" and a "completed" row in `results/gpu_ledger_2026-10-31.md`. GPU_TOTAL_PLACEHOLDER

**Data movement.**
- HCP never left B300.
- Only aggregate results came back: run records with per-subject pseudonymous error terms, partitions, and Stage-0 summaries.
- No ENIGMA data or ENIGMA-derived file was used, and `~/enigma_ocd` was never listed or read.
- The B300 node-time comes out of the SwiFT-7T allocation.

## 6. Limitations and caveats

**C6 / HCP status.**
- HCP-YA Open Access is a public release under its Data Use Terms.
- It was already staged on B300 by another workstream and was used read-only.
- **PI confirmation is needed** that it counts as "public" under C6. The fallback is OpenNeuro ds000228 (PDDL), which needs its own token map.

**Effect size δ.** δ = 1 % relative NMSE was set by the worker, not the PI. The full intervals are given, so the PI can re-read the result at any δ.

**Low reconstruction ceiling.**
- At this budget the real-data models reconstruct very little of the masked per-voxel z-scored 2 mm BOLD; the val/test NMSE is near 1, see §3.
- A δ of 1 % relative NMSE is therefore of the same order as all the variance any arm explains. This was recorded before Stage 1 finished (addendum 02 §3).
- The verdict below is about this pilot's target and budget. It is not a general statement about connectome grouping.

**Single setting.**
- One small configuration was tested: E36, depths 2/2/6/2, 38.7 M parameters, of which 32 M sit in the decoder.
- Training was short: 140k samples, about 18 passes, with no tuning.
- The E192 / VRABES scale was not run.

**Splits.**
- HCP family structure is restricted data, so relatives may straddle splits.
- The 5 explorer development subjects are excluded.
- The 64/8/16 split is fixed by a salted hash of content pseudonyms.

**Not inspected / not done.**
- The perlmutter SwiFT fork.
- Downstream tasks (fingerprinting, phenotype prediction).
- Representation-level diagnostics of the trained models. Checkpoints are kept on B300 only.

## 7. Costed plan for a more sensitive follow-up (not run; needs PI decision)

GPU-hour estimates use the measured 0.43 GPU-h per E36 run of 140k samples at 91 samples/s on B300. The E192 rate is the explorer-measured 28.6 samples/s.

| option | what changes | runs | est. GPU-h |
|---|---|---|---|
| A. Lower-noise target | reconstruct 12 mm cell means, or spatially smoothed BOLD, instead of 2 mm voxels; same arms and seeds | 15 | ≈ 6.5 |
| B. Longer budget | 4× samples (560k) at E36 | 15 | ≈ 26 |
| C. More seeds | 8 seeds × 3 arms at E36, narrower t interval (df 7) | 24 | ≈ 10.5 |
| D. E192 scale | E192 d2-2-18-2, 140k samples | 15 | ≈ 20 (1.36 h per run) |
| E. Downstream value | frozen-encoder fingerprinting or age probe on the saved Stage-1 checkpoints | — | < 1 |

The card already contains the gate, nulls and verdict machinery; each option needs a new dated card before it is run.

## 8. Reproduce / verify

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-01/card_sha256.txt | sha256sum -c          # card + frozen inputs
sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt              # code unchanged since freeze
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool -q
/home/juke/superclaude-env/bin/python3 -B scripts/topic2_verdict.py results/topic2/2026-11-01/runs /tmp/verdict_check.json   # recomputes §2.2, §3, §0
```

On B300 (`/scratch/iitp4/worker_M3_r1`), the full pipeline is rebuilt from the repo copy of the code:
- `topic2_preprocess_hcp.py`
- `topic2_make_split.py`
- `topic2_build_partitions.py hcp`
- `topic2_stage0.py`
- `topic2_launch_wave.py`, run on `code/wave{1..4}_jobs.json` (copies in `verification/worker_M3_r1/`)
