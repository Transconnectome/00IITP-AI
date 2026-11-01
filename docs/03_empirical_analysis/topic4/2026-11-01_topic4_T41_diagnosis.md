# Topic 4 · T4.1 diagnosis (2026-11-01): why every legacy condition, including C0, scored forecast R² = 1.0

Author: worker_M4_r1 (run tw-20261031-four-topics, M4). Evidence files are under `results/topic4/2026-11-01/`. Legacy numbers below are reproduced only to explain the artefact. Per C8 they are not results.

## Verdict
The R² = 1.0 for all six conditions is a measurement artefact. Every subject the legacy run used has a chronological test window made entirely of zero padding. The legacy formula floors the resulting ss_tot ≈ 1e-45 at 1e-8, so any predictor that outputs ≈ 0 scores 1.0. Persistence scores 1.0 too.

On a full-length subject, the same unmodified code gives R² between −0.08 and +0.05. Five further defects (section 3) would have made the comparison uninterpretable even without the padding.

## 1. Mechanism with counterfactual (decisive evidence)
Source: `results/topic4/2026-11-01/t41_counterfactual.json`, produced by `scripts/topic4_t41_counterfactual.py`. The script reruns the protected `src/fractal_motif_resu.py::evaluate_topology_on_fmri_streams` exactly as the legacy run fed it: VMD cache row, IMF1 channel, 48 ROIs by linspace, z-score over all 464 rows, legacy topologies with seed 42, n_epochs 2. It uses only positions that earlier probes had already touched.

| quantity | position 0 (legacy-run subject; TR 1.8) | position 932 (full-length counterfactual; TR 1.0) |
|---|---|---|
| raw valid samples in npy / valid rows of the 464-row cache | 197 / 177 | 720 / 464 |
| chronological split index `int(0.7·(T−1))` | 324 | 324 |
| test-target rows inside the valid portion | **0 of 139** | 139 of 139 |
| test-window input SD (max over ROIs) | 4.1e-25 | 1.42 |
| ss_tot of the test target (top-8 PCs) | **2.5e-45** | 5331 |
| protected function forecast R², C0 / C1 / C2 / C3 / C4 / C5 | **1.0 / 1.0 / 1.0 / 1.0 / 1.0 / 1.0** | 0.040 / 0.053 / 0.051 / −0.082 / 0.024 / 0.024 |
| legacy formula, persistence / train mean / zero predictor | 1.0 / −1.0 / 0.99999983 | 0.992 / −0.179 / −0.088 |
| guarded metric (this redesign) | **raises `DegenerateTargetError`** (ratio 2.9e-49 < 1e-3) | finite, same values as the legacy formula |

Mechanism, step by step:
1. The legacy run used positions 0–9 (`src/run_all_empirical_experiments.py:47`, `n_subjects_t4 = 10`). The legacy report says n = 12; that is a documentation mismatch. All of those subjects are Amsterdam-VUmc, TR 1.8, with 197 raw samples. The cache keeps 177 valid rows and zero-pads to 464.
2. The split at row 324 (`fractal_motif_resu.py:417`) places the entire test window in the padding.
3. After the full-stream z-score (`:480`), the padding becomes a constant row. The target is the top-8 PCs of that stream (`:371`), so the test target is constant and ss_tot ≈ 1e-45.
4. `max(ss_tot, 1e-8)` (`:425`) turns ≈ 0/1e-8 into R² = 1.0 for every encoder, C0 included. The clip at −1 turns a constant offset into −1.0 instead.
5. Falsification check: a subject with no padding in the test window, under identical code, gives R² ≈ 0. The cause is therefore the padding plus the floor, not "the task is easy" and not leakage alone.

## 2. Fixtures that catch it (fail on the defect, pass on the redesign)
Mutation evidence: `verification/worker_M4_r1/mutants/mutation_results.json`. All 17 mutants were killed and the unmutated copy passes 63/63.

| ID | fixture (tests/topic4_resu/) | what it catches | mutant killed |
|---|---|---|---|
| F1 | `test_t41_metric.py::test_F1_*`, `test_t41_legacy_characterisation.py` | The legacy formula and the unmodified protected function return 1.0 on a centred-then-padded stream and do not on an unpadded one. Fixture trap: an uncentred stream gives −1.0, so a "never 1.0" test written against it would pass on the defect | (characterisation) |
| F2 | `test_F2_*` | `guarded_r2` raises when ss_tot < 1e-3 · n · Σ var_train. It is scale-relative, with no floor and no clip | `r2_floor_instead_of_raise` |
| F3 | `test_F3_*`, `test_data.py` | The loader strips trailing padding (`valid_portion`) or halts; a padded stream never scores 1 | `padding_not_stripped` |
| F4 | `test_F4_constant_predictor_r2_is_never_positive` | The reference mean is the subject's own test mean, so any constant predictor scores ≤ 0 (property test, 200 draws) | `r2_reference_mean_zero` |
| F-fold | `test_train_only.py` | Every fitted state (PCA, RRR, local engine, MLP, every ridge readout) is bit-identical when test subjects are perturbed | `full_stream_pca_fit`, `readout_fit_includes_test` |
| F6-VAR | `test_var_fixture.py` | VAR(1) analytic Bayes R² is reproduced; no causal arm exceeds it; an acausal input exceeds it | `off_by_one_target_in_input` |

## 3. Further defects under the artefact (each removed in the redesign)
| # | defect | evidence | redesign |
|---|---|---|---|
| D1 | Test rows are touched by full-stream z-scoring (`:480`), full-stream SVD target (`:371`), online plasticity over all T rows (`:389–395`) and filter-bank normalisation (`:211`) | code; explorer_M4_r1_1 probe A (fitting these on train rows moves ridge R² 0.958 → 0.898 and engine R² by up to 0.34) | Everything is fitted on training subjects only (fixture F-fold); targets are raw ROIs with no fitted transform |
| D2 | The IMF1 input saturates trivial baselines: on position 932 persistence scores 0.992 (table above) | `t41_counterfactual.json` | Raw full-band npy series at TR = 2.0, horizon stated in seconds (2 s). On the tuning set persistence is −0.31 and identity ridge 0.146 at 2 s (`tuning.json`, gate G-b) |
| D3 | The legacy engine is non-local and collapses. Stability is a global eigenvalue rescale (`:349–352`); the M diagonal is zeroed (`:347`); `M_hier` is asymmetric (`:302`); there is a gain ramp (`:301`); it is not permutation-equivariant. On a planted 24-d subspace its dense decode R² is 0.33, against 0.97 for the canonical rule | `qualification.json` Q2 `legacy_dense`; `test_psp_engine.py::test_legacy_engine_fails_the_planted_fixture` | Masked-lateral PSP with strictly local updates; stability monitored (ρ(I − D⁻¹M) < 1), never enforced |
| D4 | Not a ReSU: arXiv:2512.23146 defines ReSU as batch past–future CCA with ON/OFF rectification and no lateral connections or local rule | primary source (read by explorer_M4_r1_1) | The engine is named "masked-lateral PSP similarity matching" |
| D5 | "Zero torch" is hard-coded (`:544`), yet the evaluation path imports `src.rg_box_pooling`, which imports torch (`:432` → `rg_box_pooling.py:26`). The old AST audit skips that file (`tests/test_pilot_connectome.py:165`) and scans only top-level `src/*.py` (`:161`) | `test_no_backprop.py::test_runtime_block_catches_the_legacy_topic4_path` | Three-part no-backprop proof for `src/topic4_resu/local/` (AST, runtime import block, target invariance); each part kills its own mutant (`nobackprop_matrix.json`) |
| D6 | The PR is uncentred (`spectral_rg_flow_diagnostic.py:55–64`), which biases non-negative codes towards 1 | code | Centred PR (`diagnostics.centred_pr`) |
| D7 | Only C4 receives the cFFL delay bank (`:377`); there is one graph per class (seed 42) | code | cFFL is off for every class; 30 graph instances per random class plus a degree-preserving C4 sham |
| D8 | The "R_hub = 0.0" claim for C4 holds only for the designated hubs {0, 6, 12, 18}. Under the code's own top-degree definition it is > 0.5 at every seed tested | `test_topologies.py::test_c4_has_zero_designated_hub_edges_but_nonzero_top_degree_rhub` | The card states "0 designated-hub edges" |

## 4. Reproduce
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
nice /home/juke/superclaude-env/bin/python3 scripts/topic4_t41_counterfactual.py --out /tmp/t41_check.json   # compare with results/topic4/2026-11-01/t41_counterfactual.json
/home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic4_resu/test_t41_metric.py tests/topic4_resu/test_t41_legacy_characterisation.py
/home/juke/superclaude-env/bin/python3 verification/worker_M4_r1/mutants/run_mutants.py   # writes mutation_results.json in that folder
```
