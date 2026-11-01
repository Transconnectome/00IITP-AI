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

**Where the intervention goes.** M0 is the only merge with room to regroup. On this run's training-split group mask, 1,442 of 4,096 stage-0 cells touch the brain, 1,195 are signal cells, and 232 of 512 M0 blocks can be regrouped.

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

FIXTURE_GATE_PLACEHOLDER

STAGE1_PLACEHOLDER
