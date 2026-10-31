# Topic 3 result report: layerwise PR and spectral diagnostics rerun (2026-10-31)

**Governing card.** `2026-10-31_topic3_analysis_card.md`, sha256 683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0, frozen 2026-10-31T08:48:29Z. Every script that produces a new real-data quantity verifies this hash before running and refuses on a mismatch: `topic3_subject_level.py` and `topic3_token_stats.py`. The connectome token job was gated by the same check in `topic3_launch_connectome.py submit`; the job itself does not re-check the card. `topic3_provenance_repro.py` ran before the freeze. It only reproduces already-public numbers and checks no card.

**Deviations.** `2026-10-31_topic3_addendum.md`. They cover host placement and a launcher fix only; no estimand changed.

**Evidence.** Every number below comes from this run's dated outputs in `results/topic3/2026-10-31/`:
- `t3_1_provenance_repro.json` (reproduction)
- `alpha_calibration_synthetic.json` (synthetic)
- `family_A_subject_level.json`
- `token_job/*_token_job.json`
- `family_B_token_level.json`

Numbers in EMPIRICAL_ANALYSIS_REPORT.md are cited only as the claims under test (C8).

**Compute.** CPU only.
- Family A ran locally in 26 s.
- The token job ran on connectome node2 under Slurm (job 217845) in about 2 min per checkpoint.
- Family B statistics took 24 s.
- GPU: 0 h. Nothing was sent to B300.

**Mode.** REPLICATION for the old numbers. PRE-SPECIFIED, not blind, for everything new; the exposure list is in card §11.

## 1. Data contract and provenance

- **Pinned inputs.** All 7 pooled matrices matched their sha256 pins. The six 57-row files share one row order. The 25 NeuroSTORM rows sit at increasing positions inside it.
- **Frames are the source of the npz.** On connectome:
  - the npz copies matched the pins;
  - npz row order equalled the sorted frame-directory order;
  - every one of the 57 subjects re-pooled from its 7 frame dumps to its npz row, for all four layers. The max |Δ| was 9.9e-8 (L0), 1.7e-7 (L1), 1.7e-7 (L2) and 4.8e-7 (L3), with allclose at 1e-5.

  This closes the explorers' position-0-only check.
- **Zoo checkpoints.** All three zoo checkpoints have the same subject set as the primary, and every subject has exactly 7 frames.
- **Dead channels.** No column fell under the corrPR dead-channel floor in any token matrix (max dropped = 0).

## 2. Family A: subject level (pooled vectors, n = 57)

| Input | n×D | covPR | corrPR | jackknife SE | iid reference mean | covPR / iid | column-permutation null q2.5 | D2 |
|---|---|---|---|---|---|---|---|---|
| L0 | 57×384 | 2.777 | 4.792 | 0.276 | 48.77 | 0.057 | 44.77 | yes (p = 0.001) |
| L1 | 57×768 | 2.778 | 5.235 | **3.577** | 52.14 | 0.053 | 49.30 | yes |
| L2 | 57×1536 | 11.020 | 13.188 | 1.296 | 54.00 | 0.204 | 53.61 | yes |
| L3 | 57×1536 | 3.579 | 4.779 | 0.286 | 53.99 | 0.066 | 52.97 | yes |
| BrainLM | 57×768 | 4.319 | 6.513 | 0.767 | 52.14 | 0.083 | 43.92 | yes |
| BrainJEPA | 57×768 | 11.785 | 13.930 | 0.767 | 52.13 | 0.226 | 50.25 | yes |
| NeuroSTORM | 25×288 | 12.507 | 13.981 | 1.067 | 22.09 | 0.566 | 21.67 | yes |

- **Every matrix is far below its iid reference and below its column-permutation null.** PR is not "collapsed to 1", and it is not noise-level either.
- **The L1 jackknife SE (3.58) is large.** L1's subject-level PR is driven by a few subjects. On the 25-row subset it is 5.10, against 2.78 on all 57.

**A1: paired subsampling stability intervals, ΔPR at m = 28 (S = 2000).**

| Contrast | covPR Δ [95% interval] | corrPR Δ [95% interval] |
|---|---|---|
| L2 − L3 | +5.34 [+3.23, +7.46] | +6.04 [+4.28, +7.80] |
| L2 − L1 | +4.67 [+2.96, +6.39] | +4.39 [+1.85, +6.93] |
| L1 − L0 | +1.24 [−2.20, +4.68] | +1.59 [−2.17, +5.35] |

**D1 verdict:** "drop robust and not a per-channel-scale effect". The final LayerNorm's gain and bias cannot explain the subject-level L2 → L3 drop, because corrPR removes them exactly and the drop survives.

**A1b: the LN-matched subject-level contrast.** This compares pooled L3 with the pooled per-token LN0(L2), both re-pooled on connectome.

| Checkpoint | corrPR L3 / LN0L2 | ΔcorrPR [95% interval] | ΔcovPR [95% interval] |
|---|---|---|---|
| E192 primary | 4.78 / 13.22 | −6.08 [−7.98, −4.18] | −5.34 [−7.61, −3.07] |
| zoo HCP_N400_T2400_E192 | 4.57 / 15.16 | −7.64 [−8.55, −6.72] | −7.41 [−8.90, −5.91] |
| zoo NewUAH_deepE192_L1e-4 | 4.13 / 5.71 | −1.36 [−2.18, −0.53] | −1.68 [−2.96, −0.40] |
| zoo NewUAH_deepE192_L5e-5 | 2.70 / 6.46 | −3.29 [−4.09, −2.48] | −2.77 [−3.72, −1.83] |

- The subject-level drop from the 2 stage-3 blocks, with the normalization matched, is present in all 4 checkpoints.
- Its size varies about 5× across checkpoints.
- This contrast is descriptive by the card. The verdict-bearing replication rule belongs to Family B.

**A2: cross-model comparison at matched n = 25 (the NeuroSTORM positions).**

| Model | covPR | corrPR | m = 12 mean covPR / iid(12, D) |
|---|---|---|---|
| BrainLM | 5.36 | 7.45 | 0.406 |
| BrainJEPA | 9.66 | 11.39 | 0.598 |
| NeuroSTORM | 12.51 | 13.98 | 0.734 |

Paired differences at m = 12:

| Contrast | covPR Δ [95% interval] | corrPR Δ [95% interval] |
|---|---|---|
| BrainJEPA − BrainLM | +2.08 [+0.77, +3.40] | +1.73 [+0.62, +2.83] |
| NeuroSTORM − BrainLM | +3.36 [+1.72, +5.01] | +2.72 [+1.45, +4.00] |

**D3: the ordering reproduces.** The ratios at matched n are about 1.8× and 2.3×. These are descriptive; the card makes no magnitude verdict. The old 2.7× compared NeuroSTORM at n = 25 with BrainLM at n = 57.

**Subject-level α.** Not reported. In the synthetic calibration, both estimators miss the 0.15 tolerance at every subject-level shape. For example, at 57×1536 with a = 0.5, the Clauset bias is +3.40 and the rank-slope bias is −0.29.

## 3. Family B: token level (within subject, 7 frames concatenated, subject = unit, n = 57 per checkpoint)

**Median per-subject PR in the primary checkpoint.**

| Layer | L0 | L1 | L2 | LN0(L2) | L3 |
|---|---|---|---|---|---|
| covPR | 2.36 | 3.23 | 5.41 | 5.54 | 5.67 |
| corrPR | 4.75 | 5.15 | 5.88 | 5.99 | 6.14 |

Within-window token representations are very low-dimensional: about 6 of a possible 1119. The dynamic-range fixture shows that corrPR at this shape can resolve planted ranks of 3, 12 and 40.

**Primary contrasts.** Each cell is the mean log ratio, the geometric-mean ratio and the 95% subject-bootstrap CI. Every Holm-adjusted sign-flip p-value is 0.0002. That is the permutation floor, 2 × 1/(B+1) with B = 9999, not a measured value: no permutation reached the observed |mean|.

| Checkpoint | H1a: corrPR L3 vs LN0(L2) | H1b: covPR L3 vs L2 |
|---|---|---|
| E192 primary | +0.023 (×1.023) [+0.021, +0.025] | +0.045 (×1.046) [+0.041, +0.048] |
| zoo HCP_N400_T2400_E192 | −0.137 (×0.872) [−0.141, −0.132] | −0.113 (×0.893) [−0.120, −0.105] |
| zoo NewUAH_deepE192_L1e-4 | +0.038 (×1.039) [+0.028, +0.047] | −0.033 (×0.968) [−0.048, −0.020] |
| zoo NewUAH_deepE192_L5e-5 | +0.049 (×1.050) [+0.043, +0.055] | +0.079 (×1.082) [+0.072, +0.087] |

**Replication rule (card §5).**
- **H1a "holds", in the direction L3 *higher*.** The primary is significant and 2 of 3 zoo checkpoints agree; HCP_N400 goes the other way. The replicated effect is a 2–5% *increase* in within-window dimensionality through the stage-3 blocks, with the norm matched.
- **H1b is "not replicated".** Only 1 of 3 zoo checkpoints shares the primary's sign.

**Secondary contrasts in the primary checkpoint.**
- H1c, the per-token norm effect: ×1.019.
- H1d: ×1.042.
- H1e: ×1.021.

All are small.

**H4: descriptive profile with 160 tokens per frame, mean covPR from L0 to L3.**

| Checkpoint | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| E192 primary | 2.35 | 3.20 | 5.41 | 5.66 |
| HCP_N400 | 2.41 | 2.72 | 5.58 | 4.99 |
| deepE192 L1e-4 | 1.24 | 1.30 | 3.33 | 3.22 |
| deepE192 L5e-5 | 2.33 | 5.30 | 4.43 | 4.79 |

L1 → L2 increases in 3 of 4 checkpoints.

**Token-level α (descriptive; no regime labels).** Values are the median over subjects.

| Checkpoint | L0 rank slope / Clauset | L1 rank slope / Clauset | L2 rank slope | L3 rank slope |
|---|---|---|---|---|
| Primary | 2.12 / 1.81 | 4.03 / 1.77 | 3.07 | 2.94 |
| HCP_N400 | 2.23 / 1.69 | 3.81 / 1.83 | 2.64 | 2.61 |
| deepE192 L1e-4 | 2.74 / 1.49 | 5.94 / 1.23 | 11.15 | 8.92 |
| deepE192 L5e-5 | 2.24 / 1.70 | 4.25 / 1.87 | 8.86 | 6.49 |

- Clauset is not estimable at 1120×1536.
- The synthetic calibration used iid rows, whereas real tokens are spatially and temporally correlated.
- These exponents depend strongly on the checkpoint, and nothing in this run licenses reading them as criticality.

## 4. Verdicts on the earlier claims

| # | Earlier claim | Verdict | Basis |
|---|---|---|---|
| J1 | json PR ≈ 1 for every model, "Over-compressed (Rank Collapse)" | **FAILS (estimator artefact).** | The old uncentered SVD is dominated by the mean vector, which carries 96–99.9% of the energy. The centering fixture reproduces the defect (old function < 1.1 on rank-k + offset). Centered PR is 2.8–12.5. |
| R1 | L2 PR "expands 4×" (2.78 → 11.02) | **REPRODUCES DESCRIPTIVELY; no verdict (D-confounded per card §4).** | ΔPR₂₈(L2 − L1) = +4.67 [+2.96, +6.39], and corrPR +4.39. Card §4 makes L2−L1 descriptive because D differs (768 vs 1536). Explorer probes show that D shifts sample PR for structured spectra: at a = 1, 17.9 at D = 384 vs 22.8 at D = 1536. So the D confound is not excluded. The "4×" also rests on an unstable L1 (jackknife SE 3.58). At token level, L1 → L2 rises in 3 of 4 checkpoints (descriptive). |
| R2 | L3 "collapse" 11.02 → 3.58 **caused by Euclidean PatchMerging** | **The mechanism FAILS. The subject-level drop HOLDS. A token-level collapse FAILS.** | **Mechanism:** ver11 has no merge between layer_2 and layer_3; layer_3 is 2 Swin blocks plus the final LayerNorm. **Subject level:** the drop is not a gain or bias effect (D1, corrPR) and survives LN matching in all 4 checkpoints (A1b). **Token level:** the within-window dimension does not drop; the replicated H1a effect is +2–5%, the opposite sign. So stage 3 shrinks the dimension of *between-subject differences in pooled means*, not the dimensionality of the token representation. |
| R3 | BrainJEPA / NeuroSTORM PR "≥ 2.7×" BrainLM; "self-supervised prediction" keeps dimension high | **Ordering HOLDS at matched n = 25 (D3). Attribution is UNTESTABLE.** | Both D3 intervals exclude 0. The matched-n ratios (about 1.8× and 2.3×) are descriptive; the card's rules do not adjudicate the old "2.7×" magnitude. Note that the old figure compared NeuroSTORM at n = 25 against BrainLM at n = 57. Pooling (CLS vs token mean vs GAP), D (768 vs 288) and training data all differ. |
| R4 | HTSR regimes ("critical 1.5–2.0", "rank collapse") from α | **NOT SUPPORTED (category error).** | Subject-level α is not estimable: synthetic Clauset bias reaches +3.4, and, in the explorer probes, the old fit labels iid noise "rank collapse" (α 0.22–0.46). HTSR thresholds concern weight-matrix spectra, not representation covariances. |
| R5 | "Optimal OOD layer = L2" and the OOD suitability score | **UNTESTABLE.** | No transfer data. The old value is hard-coded. |
| R6 | d_B, R_hub, assortativity r of similarity graphs, including "L2 disassortative" and "L3 hub crowding" | **NOT SUPPORTED (out of scope; not re-estimated).** | They were built on uncentered cosines with medians of 0.97–0.9995. Iid noise and a rank-3 + mean synthetic reproduce the same ranges (explorer evidence, card §8). |
| R7 | SwiFT-LLM NeuroPrior 450-ROI row in the same table | **Not comparable.** | Its rows are ROIs, so it measures a different estimand. |
| H2 | Trained vs random-init difference | **UNTESTED.** | Deferred by the card (§6): it needs a torch venv on connectome and an exact replication of the extraction preprocessing. |

## 5. Limitations

**What subject-level PR measures.** At n = 57 it measures between-subject spread, with a ceiling of 56. It depends on n, D and spectrum shape, which is why every comparison here is paired at a fixed m or at matched n. The intervals are stability intervals for Δ_m, not population CIs.

**Token-level PR is descriptive within a window.** Tokens are spatially and temporally correlated. Statistical inference uses subjects as the unit. The effects are very precise (CIs of about ±0.003 in log ratio) but small, and their sign is checkpoint-dependent. One of the four checkpoints (HCP_N400) reverses both H1 contrasts.

**Exposure.** The direction of the subject-level L2 > L3 contrast was known before the card (§11). D1 and A1b are therefore pre-specified tests of a seen pattern. The token-level and LN-matched results were not seen before the card.

**Unverified items:**
- The NERSC extraction fork was not diffed against local ver11; the re-pool proof ties the dumps to the npz.
- The LN γ/β values were not read; corrPR makes them irrelevant.
- The random-init control was not run.

## 6. Reproduction

```
cd /home/juke/git/00IITP-AI
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic3_provenance_repro.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=8 /home/juke/superclaude-env/bin/python3 scripts/topic3_alpha_calibration.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=4 /home/juke/superclaude-env/bin/python3 scripts/topic3_subject_level.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic3_launch_connectome.py submit   # then: collect
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=4 /home/juke/superclaude-env/bin/python3 scripts/topic3_token_stats.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_spectral -q
```
