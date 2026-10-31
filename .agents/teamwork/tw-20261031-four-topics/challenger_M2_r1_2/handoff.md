# Handoff: challenger_M2_r1_2 (M2, Topic 3), 2026-10-31

Type: **Hard**. The review is complete.
Verdict: **CONFIRMED.** I found no recomputation mismatch, no misapplied rule, no ordering or exposure violation, and no badly anti-conservative interval. I did find one substantive interpretation defect in Family B (N1 below). It does not change any rule outcome, but the report needs an addendum. I rate it nonblocking for the card verdicts and high priority for how the result can be read.

All probes are in `/home/juke/git/00IITP-AI/verification/challenger_M2_r1_2/`:
- `probes/` holds the scripts and their outputs.
- `tree/` is a copy of the M2 tree. Every rerun ran there; nothing ran in place.

## 1. Observation

**O1. Hashes and C1.**
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gave rc 0 with 0 non-OK lines, before and after my work.
- `output_sha256.txt`: all OK. `addendum_02_sha256.txt`: OK.
- `code_sha256_at_freeze.txt`: all OK except `scripts/topic3_launch_connectome.py`, which addendum 01 item 2 already discloses.
- Every production M2 path was recorded before and after (`prod_baseline_before.txt` and `prod_baseline_after.txt`, 60 files, sha256 + mtime). The two lists are identical.

**O2. Freeze order.** `card_sha256.txt` says frozen 2026-10-31T08:48:29Z (file mtime 17:48:29 KST). Everything that governs or uses real data came after it:

| Event | Time (UTC) | Source |
|---|---|---|
| Card frozen | 08:48:29 | `card_sha256.txt` |
| Family A `run.started_utc` | 08:49:18 | card hash verified in the run record |
| Slurm task 0 start (job 217845) | 08:51:32 | `logs/connectome/logs/t3_tokspec_217845_0.out` |
| Slurm task 3 end | 08:58:52 | same folder |
| Family B `run.started_utc` | 09:01:59 | card hash verified in the run record |

Only two outputs predate the card:
- `t3_1_provenance_repro.json` (08:31Z). It reproduces already-public numbers.
- `alpha_calibration_synthetic.json` (08:40Z). The script contains no VRABES, `npz`, `load_pinned` or `storage` reference (grep rc 1).

**O3. Exposure audit.** I listed every file under `verification/explorer_M2_r1_*`, `explorer_survey_*` and `worker_M2_r1` with an mtime before the freeze and read the headers of each real-data probe:
- `probe_m2_subsample_ci`, `probe_k_corrpr_range`, `probe_i_bootstrap_bias` and `probe_m2_estimators` are synthetic only.
- `probe_m2_token_feasibility` and `probe_m2_ln_scale` use one frame and report "No PR values".
- `probe_a_real_structure` and `probe_d_colscale` report reproductions and column-SD quantiles.

All of this matches card §11. I found no pre-freeze corrPR, subsampling or token-PR computation on real data.

**O4. Family B, independently recomputed** (`probes/p1_familyB_indep.py`; it does not import `topic3_spectral` and uses its own RNG streams).
- PR recomputed from the saved float32 eigenvalues matches the saved PRs to ≤ 5.2e-8 relative.
- The traces of the corr eigenvalues equal D (384 / 768 / 1536 ± 5e-5), so no column was dropped.
- Mean log ratios match the worker's to 0.0. CI endpoints match to ≤ 5e-4, which is Monte Carlo noise.
- My sign-flip p is 1e-4 and Holm p is 2e-4 for all 8 contrasts.
- Replication rule, computed independently: H1a primary significant with 2/3 zoo agreeing → **holds**. H1b with 1/3 agreeing → **not replicated**. Both equal the worker's verdicts.
- Per-subject sign counts for H1a: primary 57/57 positive; HCP_N400 0/57; deep L1e-4 51/57; deep L5e-5 54/57.

**O5. Reruns in the copied tree.** `topic3_subject_level.py` and `topic3_token_stats.py` both exited rc 0. Diffing their JSON against the pinned outputs, ignoring timing and host, gave **0 differing leaves** for each (`probes/p3_jsondiff.py`). `topic3_provenance_repro.py` fails in the copy only because the copy does not contain the protected `empirical_results.json`. I checked T3.1 separately (O7).

**O6. Family A, independently recomputed** (`probes/p4_familyA_indep.out.json`). Method: SVD for covPR, `np.corrcoef` for corrPR, my own loader, and my own subsampler with different seeds and S = 4000.
- All 7 covPR and corrPR values match to ≤ 7e-14.
- L1 jackknife SE = 3.5767 (report 3.577). L1 on the 25-row subset = 5.101 (report 5.10).

| Contrast | Mine (own seeds) | Report |
|---|---|---|
| L2−L3 cov | +5.42 [3.26, 7.58] | +5.34 [3.23, 7.46] |
| L2−L3 corr | +6.10 [4.30, 7.89] | +6.04 [4.28, 7.80] |
| JEPA−LM cov | +2.10 [0.78, 3.42] | +2.08 [0.77, 3.40] |
| NeuroSTORM−LM cov | +3.38 [1.70, 5.05] | +3.36 [1.72, 5.01] |

D1 and D3 do not depend on the seed.

**O7. T3.1.** I copied the protected uncentered `compute_participation_ratio` verbatim, without importing the module. On the 7 pinned npz files it reproduces every `empirical_results.json` `participation_ratio_PR` value to 4 dp (1.0014, 1.005, 1.0743, 1.0327, 1.0028, 1.0581, 1.0102; `probes/p7_t31_and_affine.out.json`).

**O8. Interval calibration** (`probes/p5_interval_calibration.out.json`). Setup:
- True Δ = 0: A and B come from the same distribution, with randomly rotated power-law spectra.
- 400 reps and S = 400 per cell.
- Scenarios: independent, correlated (ρ = 0.8) and heavy row scales.

FPR of "interval excludes 0":

| Shape | Independent | Correlated | Heavy rows |
|---|---|---|---|
| n = 25, m = 12, D = 768 | 0.035 / 0.030 | 0.0225 / 0.0125 | 0.0375 / 0.0225 |
| n = 57, m = 28, D = 1536 | 0.050 / 0.035 | 0.025 / 0.0375 | 0.0425 / 0.0425 |

(Each cell gives decay 1 / decay 2. MC SE is 0.011.) The interval is at or below nominal. It is not anti-conservative.

**O9. Torch-free `.pt` reader** (`probes/p2_loader.py`, local torch 2.11). I saved adversarial tensors with torch: a non-contiguous permuted (C, D, H, W, T), a storage-offset slice and a transposed matrix. `load_pt_numpy` reproduces each one exactly. A random layer_3 tensor gives a token-matrix rank of 159.

**O10. Token spectra have rank 7 at L2 and L3, set by the spatial grid** (`probes/p1d_spectrum.py`, `p1b_frames.py`, `p1c_between.py`). Outputs: `p1b_frames.out.txt`, `p1c_between.out.txt`, `p1d_spectrum.out.txt`.
- Energy in the top 7 eigenvalues of the concatenated 1120×1536 token covariance:
  - L2 and L3: ≥ 0.99994 in every subject of every checkpoint.
  - Median of e[7]/e[0]: 2e-7 to 6e-6.
- L1 has 63 effective dimensions and L0 has 511. These equal (number of spatial positions) − 1: L0 is 8³ × 20 T, L1 is 4³ × 20, and L2 and L3 are 2³ × 20 tokens.
- Tokens are therefore almost invariant over the 20 time steps and over the 7 frames.
- Per-frame PR varies across a subject's 7 frames with SD of about 2e-4. Across subjects the SD is 0.06–0.29, a ratio of 150–540×.
- The concatenated PR equals the mean per-frame PR to within 1e-6 to 3e-5.

**O11. Affine invariance of corrPR.** It is exact up to a gain spread of 1e4 (`p7`). At a spread of 1e6, the 1e-3·median floor drops 7 columns and corrPR moves by 0.02. The real data never reach that regime: 0 columns were dropped in every token matrix.

**O12. Spot-checked report tables.** Family A E1, A1, A1b, A2, D1 and D3, plus Family B medians, secondary contrasts, H4 and α medians, all match the JSON. There are two rounding slips of 0.005:
- A1 L2−L3 cov lo is 3.2250, reported as +3.23.
- A1b L5e-5 corr is −3.2849, reported as −3.29.

**O13. Mutants** (`probes/p6_mutants.py` / `.out.json`, 24 mutants of my own; each was applied to a fresh copy and the full topic3 suite was run). **17 of 24 were killed.**

Killed (17):
- M01 no centering
- M02 with-replacement subsampling
- M03 Holm without adjustment
- M04 zoo agreement 1
- M05 a/b swapped
- M06 direction label inverted
- M07 CI `or` → `and`
- M08 layer3 reshape without transpose
- M09 Clauset off by 1
- M11 one-sided sign flip
- M12 variance floor 0.1
- M16 LN0 on the wrong axis
- M17 primary counted as zoo
- M19 corr without scaling
- M21 concatenation uses frame 0 only
- M23 eig rank cap removed
- M24 pooled = last frame only

**Survivors (7):**

| Mutant | Path | Assessment |
|---|---|---|
| M10 `rank_slope` kmax = r instead of r // 2 | descriptive token α only | fixture gap |
| M13 jackknife factor 1/n instead of (n−1)/n | descriptive SE only | fixture gap |
| M14 subsample SE without √(m/(n−m)) | **D1/D3 interval path** | near-equivalent at m ≈ n/2 (factor 0.98 / 0.96); no test pins the formula |
| M15 LN eps = 0 | LN0L2 | near-equivalent numerically |
| M18 sign-flip p without +1 | Holm p | floor 0.0002 → 0; verdict unchanged |
| M20 D1 uses point > 0 instead of lo > 0 | **D1 verdict rule** | no test exercises the D1 logic |
| M22 D3 uses any() instead of all() | **D3 verdict rule** | no test exercises the D3 logic |

On the real data, M20 and M22 cannot change D1 or D3: both lower bounds of each pair are > 0 (O6), so point / lo and any / all give the same answer. I read the code and it implements `lo > 0` and `all(...)` as the card says. The rule outcomes are correct, but the tests do not pin them.

**O14. Addendum 02 claims.**
- `extract_vrabes_swift_zoo.sh` gives the deep checkpoints depth `2 2 42 4` and HCP_N400_T2400_E192 depth `2 2 18 2` (last.pt, L2e-5).
- `extract_vrabes_swift_E192.sh:82` gives `--depth 2 2 18 2`.
- ver11 (`simmim_swin4d_transformer_ver11.py:1068`) has `downsample=... if (i_layer < self.num_layers - 1) else None`, so the merge sits at the end of stage 2, inside the `layer_2` dump. Stage 3 has none. The dump shapes, 160×1536 in and 1536×(2·2·2·20) out, confirm this independently.

**O15. IDs.** I loaded the 57 ids in memory and searched 94 files for them: all M2 outputs, docs, src, tests, scripts, the worker's probes and metadata, and my own probes and metadata. **0 files** contain an ID, and no npz holds a string array.

**O16. GPU ledger.** `results/gpu_ledger_2026-10-31.md` does not exist. M2 used 0 GPU-h, and so did I.

## 2. Logic Chain

1. O2 and O3 show the card was frozen before any governed real-data quantity existed, and that the exposure list is accurate. C3's order requirement holds.
2. O4, O5, O6 and O7 show every headline number reproduces. Three independent routes agree: a bit-exact rerun, an independent reimplementation, and independent seeds. T3.1 reproduces to 4 dp. T3.1 and T3.4 hold numerically.
3. O4 applies the card §5 rule independently and gets the same H1a and H1b verdicts. O6 gives the same D1 and D3 outcomes under different seeds. O8 shows the interval behind D1 and D3 is not anti-conservative, so D3's closest lower bound (+0.77) is not an FPR artefact. The verdicts follow the card.
4. O9 rules out the loader as the cause of O10, and the re-pool proof ties the frames to the npz. O10 is therefore a property of the data.
5. O10 means the token-level analysis measures how 8 spatial-position vectors spread at L2 and L3, with a ceiling of 7. It does not measure "within-window dimensionality" against 1119. Several statements do not hold as written:
   - "about 6 of a possible 1119" and "very low-dimensional" (report §3): against the effective ceiling, PR 5.4–6.1 is 77–87% of the maximum.
   - The dynamic-range fixture claim "can resolve planted ranks 3, 12, 40" does not apply here.
   - Concatenating 7 frames adds nothing beyond one frame.
   - H1a "+2–5% within-window dimensionality" is really a change in the spatial spread of 8 vectors.
   - The R2 phrase "token-level collapse FAILS" rests on a contrast whose room to move is set by 8 positions.

   The rule outcomes (holds / not replicated) are unaffected, because the card defined H1a/H1b as those exact contrasts.
6. O13 measures how well the fixtures cover the code. Survivors on descriptive-only quantities are fixture gaps, not verdict defects. A survivor on a verdict path is discussed in Caveats.

## 3. Caveats

- I did not rerun the connectome token job. I read no frames and ran nothing on connectome. Family B was checked from the saved spectra and the re-pool receipts only.
- O10's mapping from rank to "spatial positions" is inferred from the exact match of counts (511 / 63 / 7) across all 4 checkpoints. I did not reshape real tokens to confirm it. Two causes are possible: the input fMRI intensities barely change over time, or the model discards temporal variation. I cannot tell which.
- M14 (SE without the √(m/(n−m)) factor) survives. At m ≈ n/2 the factor is 0.98 (57/28) or 0.96 (25/12), so this mutant is nearly equivalent at the card's parameters. It does sit on the D1/D3 path, though, and no test pins the formula.
- The calibration covers Gaussian rotated power-law spectra only. Real spectra (O10) may behave differently.
- H2 (random-init) remains untested, as the card defers it.
- `verification/challenger_M2_r1_2/tree/` holds **non-authoritative copies** of the M2 code, of the pinned outputs plus my rerun JSONs, and of protected `src/*.py`. They are kept only as rerun evidence. It is not a source; the production paths are canonical. Deleting it is optional.
- ID scan, rerun over all of `verification/challenger_M2_r1_2/` (tree, logs and baselines included) plus the M2 production paths: 1110 files, 0 contain an ID.
- No orphan processes of mine remain. The pytest and tail processes still running on the host belong to other sessions.

## 4. Conclusion

**CONFIRMED for M2.**
- Card before results: confirmed.
- Every headline number reproduces through 3 routes.
- The verdicts follow the card's rules: H1a holds, H1b not replicated, D1, D3 and J1.
- T3.1 reproduces to 4 dp.
- No IDs leaked, C1 is OK, 0 GPU-h.

Nonblocking items, by priority:
- **N1 (high).** Token-level PR at L2/L3 has an effective ceiling of 7. ≥ 99.994% of the variance lies in 7 dimensions, because tokens barely vary over time or frames. The report's "about 6 of a possible 1119", "very low-dimensional", "within-window dimensionality" and the dynamic-range-fixture remark should be corrected in an addendum, and the R2 "token-level collapse FAILS" wording should be qualified.
- **N2 (medium).** Fixture gaps (O13). 7 of 24 mutants survive.
  - The D1 and D3 decision logic (M20, M22) and the subsampling SE formula (M14) have no tests, even though they are on verdict paths. On the real data the outcomes were checked independently and are correct.
  - Suggested fix: add tests that assert the D1/D3 rules on synthetic deltas whose lower bound and point estimate disagree, and a test that pins the SE factor at m ≠ n/2.
  - This does not contradict the worker's 9/9: they killed their own 9 mutants, and my set is a different one that complements theirs. It found 7 gaps their set did not probe.
  - Why this is nonblocking although it touches verdict code: I read the code and it implements `lo > 0` and `all(...)` as card §4 specifies, and O6 reproduces D1 and D3 with independent seeds.
- **N3.** Two rounding slips (O12).
- **N4.** The GPU ledger file is missing (0 GPU-h used).
- **N5.** The "exact" affine invariance of corrPR holds only for gain spreads below 1/floor, i.e. below 1e3 relative to the median (not reached in the data).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
sha256sum -c results/topic3/2026-10-31/output_sha256.txt
P=verification/challenger_M2_r1_2/probes; PY=/home/juke/superclaude-env/bin/python3
PYTHONDONTWRITEBYTECODE=1 $PY -I $P/p1_familyB_indep.py      # verdicts + diff vs worker
PYTHONDONTWRITEBYTECODE=1 $PY -I $P/p1d_spectrum.py          # N1: energy in top n_spatial-1 eigs
PYTHONDONTWRITEBYTECODE=1 $PY -I $P/p4_familyA_indep.py      # ~8 min
PYTHONDONTWRITEBYTECODE=1 $PY $P/p6_mutants.py M14_subsample_se_unscaled   # one survivor
```

This conclusion is invalidated if any of the following happens:
- a pinned output hash changes;
- `p1_familyB_indep` gives a different verdict;
- a frame-level reshape of real tokens shows temporal variance above about 1e-4 of the total, which would contradict O10.
