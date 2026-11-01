# Handoff — explorer_M4_r1_2 (M4 Topic 4, feasibility / failure-mode lens)
Written 2026-11-01T01:00Z. Type: explorer analysis report (read-only; no production code; no git writes).
Probes: /home/juke/git/00IITP-AI/verification/explorer_M4_r1_2/ (synthetic, plus 2 real ENIGMA positions on DGX-Spark only).
GPU: 0 GPU-h. B300 not contacted (M4 needs no GPU and its data are ENIGMA, C6). The 0.25 GPU-h smoke allowance was deliberately not spent because B300 time comes out of the SwiFT-7T allocation.
Numbers below are feasibility evidence and govern no result (C3/C8).

**Summary.** T4.1 is closed with a falsification. Positions 0–9 (all ten subjects of the old run) have raw_valid_T 197, so their whole old test window was padding. On a 464-row subject the unchanged old function gives R² −0.08…0.05 instead of 1.0.

Three choices decide whether the redesign is feasible:
1. **Primary set and horizon.** Use TR = 2.0 sites only (1195 subjects, 13 sites), with horizons stated in seconds. Fast-TR data are band-limited at 0.25 Hz, which gives a lag-1-sample persistence of 0.71 at TR 1.0 versus 0.15 at 2 s.
2. **Local engine.** It must be stable by construction for every mask *and* learn real structure:
   - the old engine is non-local, non-equivariant and imports torch at runtime;
   - masked canonical PSP loses positive definiteness depending on topology;
   - a rectified engine with a per-neuron contraction guard is stable on every mask, but fails planted recovery at m = k (0.79) and is no better than random ReLU features.
   - **No engine qualifies yet.** A synthetic engine-qualification gate must pass before the card is frozen. If no engine qualifies, the verdict is `no_candidate` and no real data are run.
3. **No-backprop proof.** It needs three checks (AST scan, a runtime import block, target invariance). Each catches a mutant that the others miss.

Compute is not a constraint: the whole design runs in about 2 h or less on 4 local CPU processes.

---

## 1. Observation

### Code reality (old Topic 4; files are C1-protected, read only)
| # | Observation | Evidence |
|---|---|---|
| O1 | Split `int(0.7*(T-1))`; `R² = max(-1, 1 - ss_res/max(ss_tot,1e-8))` | src/fractal_motif_resu.py:417-425 |
| O2 | The test rows are touched in four places: full-stream SVD target (:371-372), online training over all T rows (:389-395), per-ROI z-score over all 464 rows (:480), and filter-bank normalisation over the full stream (:211) | same file |
| O3 | The old run used `n_subjects_t4 = 10` (positions 0–9). M1 manifest: positions 0–9 are all Amsterdam-VUmc, TR 1.8, raw_valid_T 197. The VMD cache mask has 177 valid rows for pos 0 (= 197 − 20-sample head trim, applied whatever the TR, truncated at 464). The manifest's 174 uses ceil(40 s / 1.8 s) = 23 | src/run_all_empirical_experiments.py:47; results/topic1/2026-10-31/manifest.json (sha 063513c9…37f6); probe_c_real.out.json |
| O4 | **Real falsification.** pos 0: test ss_tot 2.5e-45, old R² = 1.0 for all 6 conditions. pos 932 (TR 1.0, 464/464 valid rows): ss_tot 5331, old R² C0 0.040, C1 0.053, C2 0.051, C3 −0.082, C4 0.024, C5 0.024 | probe_c_real.out.json |
| O5 | **Fixture trap.** On a synthetic padded stream, the old function gives 1.0 only if the valid part is centred before padding (as IMF1 was): ss_tot 1.5e-60, padded rows 1.4e-16 → R² 1.0 for C0/C4/C5. With an uncentred valid part it gives **−1.0** (ss_tot 5e-29). Unpadded control: 0.03 / 0.09. The guarded metric raised in every padded case (ss_tot/(n·Σvar_train) = 8.9e-34) | probe_a_metric_fixtures.out.json (A1); probe_a2_padding_realistic.out.json |
| O6 | VAR(1) with analytic Bayes R² (discrete Lyapunov), 300 synthetic subjects × 160 samples, subject split. h=1: Bayes 0.705, oracle 0.702 [0.696, 0.708], identity ridge 0.702, constant −0.006, off-by-one target leak **1.000** (above Bayes). Train-only invariance: perturbing only the test rows changes the old full-stream basis (True) but not a train-only basis (False). BOLD-like grid with A = aI + bR: (0.4, 0.2) Bayes 0.37 / persistence 0.17; (0.55, 0.1) 0.42 / 0.29; (0.4, 0.3) 0.51 / 0.32 | probe_a_metric_fixtures.out.json (A3, A4); probe_e_var_grid.out.json |
| O7 | Band limit and horizon (pos 932, TR 1.0, Nyquist 0.5 Hz): 0.99% of Welch power is above 0.25 Hz and 10.1% is in 0.20–0.25 Hz. Persistence on within-subject top-8 PCs: lag 1 sample (1 s) **0.714**, lag 2 s 0.146 (native) / 0.145 (2:1 decimated), lag 4 s −0.351. pos 0 (TR 1.8) at lag 1 sample (1.8 s): 0.299 | probe_c_real.out.json; directory name `MBBN_data_304_ROIs_0.25` |
| O8 | Cohort: 1706 subjects, 23 sites. TR counts 0.7:43, 0.8:96, 0.85:104, 1.0:119, 1.73:39, 1.8:110, 2.0:1195. **TR = 2.0: 1195 subjects, 13 sites** (Bangalore 358 = 30%), valid_T 100–286 (median 133), Σ = 191,209 samples. All 360 subjects with raw_valid_T > 464 have TR ≤ 1.0 | manifest.json (positions/site/TR only) |
| O9 | Planted 8-d subspace (d=48), principal-angle alignment (1 = perfect; random ≈ 0.167):<br>• old fractal engine C0: 0.762 (centred PR 1.07, mean \|cos W\| 0.957 → collapse)<br>• old fractal engine dense: 0.858 (PR 3.9)<br>• old local_learning_engine: 0.811<br>• **canonical PSP dense: 0.997** (PR 5.44)<br>• PSP diagonal-only: 0.872 (PR 1.0) | probe_b_engines.out.json B1 |
| O10 | The old ρ-rescale `M *= 0.95/ρ` (a global eigendecomposition, :350-352) fires on **57–79% of steps** (1705–2359 of 3000). Without it ρ reaches 9–37, but no y hits the clip (rectified inhibition stays bounded). PSP with η/τ = 1.2 → indefinite M and blow-up; η/τ = 0.02 → positive definite | probe_b_engines.out.json B2 |
| O11 | **Masked canonical PSP loses positive definiteness, and the loss depends on the topology:**<br>• η/τ = 0.02: C3 is non-PD on 10.9% of steps (planted data) / 52.8% (BOLD-like); C1, C2, C4 stay PD<br>• η/τ = 0.1: C1–C4 are non-PD on 76–97% of steps<br>• C0 and C5 are always PD (Hadamard product with I or with all-ones) | probe_b2_masked_psp_rk4.out.json |
| O12 | Old RK4 (15 × dt 0.1 = 1.5 τ) is not at equilibrium: relative deviation of y after 15 vs 500 steps is median 0–2.2%, p90 9.7–14.9% | same |
| O13 | Old engine is not permutation-equivariant (max deviation 4.73), because of `gain=linspace(1.3,0.7)` (:301) and `M_hier=tril+0.25·triu` (:302). PSP deviation: 4e-15 | probe_b_engines.out.json B3 |
| O14 | Cost per sample (load avg 16–17 on 20 cores):<br>• old engine: 0.281 ms train, 0.221 ms inference<br>• PSP: 0.012 ms<br>• guarded rectified engine (O18): 0.02–0.18 ms<br>• MLP 48→24→8 (1376 params): 0.28 s per epoch at 130k samples, 2 threads | probe_b, probe_f, probe_g outputs |
| O15 | **The no-backprop checks each catch different mutants:**<br>• the old-style AST audit (logic of tests/test_pilot_connectome.py:160-185) passes `importlib.import_module("torch")`, `__import__("torch")` and a hand-coded numpy error-signal mutant<br>• the runtime block (`sys.modules['torch']=None`, …) catches the two import mutants<br>• only target invariance catches the numpy error-signal mutant<br>• **the old Topic-4 path fails the runtime block** (ModuleNotFoundError): it imports `src.rg_box_pooling` lazily at :432, that file does `import torch` (rg_box_pooling.py:26), and the old audit skips it (test_pilot_connectome.py:165)<br>• `zero_torch_autograd_confirmed: True` is hard-coded (:543-544) | probe_d_nobackprop.out.json |
| O16 | Topologies at seed 42:<br>• C1–C4 have 69 undirected edges each<br>• C4 has 0 edges among its designated hubs {0,6,12,18}, but those hubs have degree 9, which is also the maximum degree<br>• the code's own `R_hub(hub_frac=0.33)` gives C1 1.571, C2 2.0, C3 4.0, **C4 1.857**<br>• so the "R_hub = 0.0" claim (docstring :58; consolidated status doc line 17) is false under the code's top-degree hub definition | probe_d_nobackprop.out.json |
| O17 | Only C4 gets the cFFL delay input (`use_cffl = "Bio_Fractal" in name`) | fractal_motif_resu.py:377 |
| O18 | **Candidate rectified local engine** (probe only): Jacobi y ← max(0, (Wx − Ly)/D) run to tolerance; local ΔW, ΔL (L ≥ 0, masked), ΔD; per-neuron guard κ_i = Σ_j L_ij / D_i ≤ 0.9 (postsynaptic-local scaling).<br>• **With guard:** non-convergence 0.0 on every mask and both η_L; equivariance deviation 4e-15; centred PR C0 1.0, C3 1.8–1.9, C1/C2/C4 4.7–6.3, C5 5.8–7.1<br>• **Mutant without guard:** non-convergence 0.03%–64% (C5 48–64%, C3 1.2–4.9%)<br>• **Rectification cost:** on a linear VAR, ridge on Y reaches h=1 R² 0.14–0.21, versus identity ridge 0.483, persistence 0.294, Bayes 0.506 | probe_f_rectified_local_engine.out.json |
| O18b | **Engine R does NOT qualify** (probe H, synthetic).<br>• Planted k=8 at dim_y = 8: W-row alignment C5 0.792, C4 0.792, C0 0.812, which is the same band as the old engines (0.76–0.86). Centred PR: C5 4.28 (old dense 3.91), C4 1.89. The fixture does not separate R from the old engine.<br>• At dim_y = 24 alignment is 0.98–0.99 even for C0 (0.993), so with m > k the alignment metric is not discriminative.<br>• VAR forecast h=1 (Bayes 0.506, identity ridge 0.483): random ReLU-24 0.184 (0.158–0.204 over 5 seeds) ≈ engine R C4 0.178 / C5 0.212. Engine R learns nothing beyond random features.<br>• Rectification cost, separately: PCA-24 linear 0.452 → PCA-24+ReLU 0.318; a ±-paired ReLU code of 12 PCA directions (24 units) recovers to 0.434.<br>• ON/OFF input split (96-d) with engine R collapses: PR 1.0, R² −0.002 | probe_h_engineR_planted_and_controls.out.json |
| O19 | Layout:<br>• the old AST audit globs `SRC_DIR.glob("*.py")` at top level only (:161), so a `src/topic4_resu/` subpackage is invisible to it<br>• hash-protected: fractal_motif_resu.py, local_learning_engine.py, rg_box_pooling.py, test_pilot_connectome.py, test_empirical_four_topics.py<br>• NOT protected (owned by other milestones, may change): src/topic1_lagmotif/data.py (d320bfe4…95e9), tr_table.py (a3837b15…6b8d), src/topic3_spectral/estimators.py (efc6f7ec…f7e9; has `centered_eigs`/`pr_cov`) | PROTECTED_HASHES.txt; sha256sum |
| O20 | connectome:<br>• Slurm up (debug/interactive/preemptable, 4 nodes, 18 jobs in queue); node1 has 96 cores<br>• system numpy 1.22.3 / scipy 1.8.0<br>• `/storage/bigdata/ENIGMA_unzip` has 27 entries (contents not inspected)<br>Local superclaude-env has torch, sklearn, scipy and networkx | ssh connectome (read-only) |

## 2. Logic Chain
1. O1 + O3 + O4: every subject in the old run had a pure-padding test window. On a subject whose test window is valid data, the same code gives R² ≈ 0. So R² = 1.0 is the padding artefact plus the 1e-8 floor. It is not "task too easy", and it is not the leak by itself. This answers survey_1's caveat that only positions 0–4 had been checked.
2. O5: a fixture that pads an uncentred synthetic stream gives −1.0 on the old code. A test "R² ≠ 1" would therefore pass against the defect, so the fixture would be vacuous. The fixture must centre the valid part before padding (RED = 1.0 on the old function). The ss_tot guard catches both the +1 and the −1 case.
3. O2 + O6 (A4): the leaks are structural and do not push R² above the Bayes ceiling, so they need a train-only invariance test. An alignment leak (off-by-one) does exceed Bayes (1.000 vs 0.705), so the VAR ceiling catches that class.
4. O7 + O8: the data are band-limited at about 0.25 Hz. At fast TR, "1 sample" ahead is trivial (persistence 0.71), while at a fixed 2 s horizon persistence is ≈0.15 on both the native and the decimated grid. Horizons must be stated in seconds. Restricting the primary set to TR = 2.0 (1195 subjects) avoids resampling, keeps the trivial baselines unsaturated (0.15–0.30 at 1.8–2 s), and excludes every subject touched by Topic 4 so far (positions 0–9 at TR 1.8, 932 at TR 1.0).
5. O9 + O10 + O13 + O15: the old fractal engine fails as a "strictly local" arm on four counts:
   - it fails planted-subspace recovery;
   - its stability depends on a global eigen-rescale active on most steps (non-local);
   - it is not permutation-equivariant, so topology effects are confounded with node index;
   - it imports torch at runtime.
6. O11: the canonical rule with sparse masks becomes unstable in a topology-dependent way (C3 first). Stability would then confound the topology comparison. Linear PSP is also weak on the science: with a linear readout and an 8-d target, a linear 24-d code cannot beat identity ridge in population, and dense PSP converges to PCA-24 (O9).
7. O18: a per-neuron contraction guard makes a rectified engine stable on every mask. It is equivariant, cheap and mutation-testable (non-convergence appears without it). **But O18b shows that stability is not enough:**
   - the probe-F engine fails planted-structure recovery at m = k, just like the old engines;
   - on the VAR its features are no better than random ReLU-24;
   - so its forecasting loss comes from two sources: unpaired rectification (0.45 → 0.32, recoverable with ±-paired units, 0.43) and a rule that learns nothing useful (0.18 ≈ random).
   **No candidate engine is qualified yet:**
   - Linear PSP passes the planted fixture (0.997), but needs the guard under masks (O11).
   - With a linear 24-d code and a linear readout, a masked-PSP fixed point still spans a C-invariant subspace (from W = FC ⇒ MF = FC). If that subspace is the top-24, topology cannot change the ridge forecast, so H1 would be null by construction.
   - A real-data run therefore only makes sense after an engine passes a synthetic qualification gate. Otherwise the verdict is `no_candidate` (sci-pipeline G8), not a scientific null.
8. O14 + O8: LOSO with per-fold retraining is infeasible (1195 folds × 60 runs). 5-fold subject cross-fitting is about 300 engine runs × ≤72 s ≈ 1.5 h on 4 processes, and the MLP adds minutes. This is local CPU work, so no B300 (C6) and no connectome (old numpy, and the ENIGMA npy would have to be moved).
9. Precision: survey_3 found a between-subject R² SD of ≈0.04–0.07 at n=5. A single 60/20/20 split (n_test ≈ 239) gives a CI half-width of ≈0.009 at worst, which is borderline for a SESOI of 0.01. Cross-fitting (n_eval ≈ 1016) gives ≈0.004.

## 3. Caveats
- **C4 note:** during orientation, one grep over enigma_ocd_mbbn markdown printed a line containing a participant-ID-shaped directory name to the tool console. It was written to no file. All probe outputs were scanned for `sub-`/`_sub` patterns: 0 matches. Probes use positions only.
- Real data: 2 subjects only, read on DGX-Spark.
  - pos 0 was already burned.
  - pos 932 (TR 1.0) is newly touched. It is outside the TR = 2.0 primary set; declare it as development.
  - The persistence numbers are within-subject and descriptive.
- Band limit: "1% above 0.25 Hz" is consistent with a 0.25 Hz low-pass, but natural BOLD spectra also fall off with frequency. The low-pass itself is supported only by the directory name and an enigma-repo audit note (secondary sources). The filter code that produced the npy files was not located.
- Probe F's engine is a sketch, run once on one seed of synthetic data:
  - its ΔW form (η(yxᵀ − W), not normalised by D) was not derived from an objective;
  - the guard check in the probe recorded κ before rescaling, so the fixture must assert κ after the update;
  - thresholds are not calibrated. Probe F supports feasibility only.
- MLP timing is from synthetic data. The between-subject SD used for precision comes from survey_3's n=5 probe.
- A subject bootstrap over cross-fitted predictions covers test-subject sampling. It does not cover training-set variability across overlapping folds, so the CI is somewhat anti-conservative. Seed averaging offsets this only partly. State this in the card.
- Probe H is one synthetic seed per configuration. The ON/OFF collapse may be fixable, for example with mean subtraction or homeostatic thresholds; that was not explored.
- Family or sibling structure in ENIGMA was not checked, so a subject-level split may not be family-disjoint. Diagnosis labels are not needed and were not read.
- The claim that macroscale resting BOLD is near-linear (which motivates expecting H2/H3 to be killed) comes from memory of the literature, e.g. Nozari et al. 2024 Nat Biomed Eng [확인 필요]. Do not cite it unverified.
- I did not read explorer_M4_r1_1's folder (independence).

## 4. Conclusion — recommended strategy (not implemented)

### T4.1 Diagnosis + fixtures (`docs/03_empirical_analysis/topic4/2026-11-01_topic4_T41_diagnosis.md`, `tests/topic4_resu/test_t41_*.py`)
**Mechanism (O1–O5).** The test window is padding, and the 1e-8 floor turns 0/0 into R² = 1. The falsification is O4.

**Contributing defects:**
- the O2 leaks;
- uncentred PR;
- the C4 cFFL confound (O17);
- the false R_hub claim (O16);
- engine collapse (O9);
- the non-local rescale (O10);
- non-equivariance (O13);
- the hard-coded "zero torch" claim versus the runtime import (O15).

**Fixtures.** Each fixture must be shown RED against the targeted defect:

| ID | Targets | Must fail on | Pass criterion |
|---|---|---|---|
| F1 | characterisation of the old artefact | — (documents it) | old `evaluate_topology_on_fmri_streams` on a synthetic **centred-then-padded** stream (197/464) returns 1.0 for C0, C4 and C5. Needs torch present (lazy import) |
| F2 | 1e-8 floor | old formula | new metric raises when ss_tot/(n·Σvar_train) < 1e-3, on the F1 stream and on a constant target |
| F3 | padding not stripped | new pipeline wired to old preprocessing | loader strips trailing zeros or raises; R² is never 1.0 |
| F4 | sign/definition bugs | e.g. ss_tot about the train mean | constant predictor ⇒ R² ≤ 0 (exact identity; property test) |
| F5 | test-touching leaks (O2) | full-stream SVD / z-score / online training (A4: True) | perturbing the test subjects leaves z-stats, PCA basis, encoder state and ridge weights bit-identical |
| F6 | alignment leaks, metric bugs | off-by-one (1.000 > Bayes) | VAR(1) at ≥2 points from probe E: the oracle's CI contains analytic Bayes, persistence matches its analytic value, and no method's CI lower bound is above Bayes |

### T4.2 Redesigned task + frozen card (CONFIRMATORY; card sha256 in `results/topic4/2026-11-01/card_sha256.txt` BEFORE any real-data run, tuning included)

**Data**
- Source: raw npy `MBBN_data_304_ROIs_0.25`, by position (sorted listdir).
- Site → TR from vendored copies of `tr_table.py` / `data.valid_portion`. Record the source sha256s from O19; do not import the M1-owned files live.
- **TR == 2.0 only** (1195 subjects, 13 sites). Trailing zeros stripped; head trim 40 s (20 samples); valid_T ≥ 100 (all pass).
- 48 ROIs at `linspace(0,303,48)`, declared.
- Per-subject, per-ROI z-score over the full valid series. This is a mild look-ahead shared by all arms; declare it.
- **Never use the VMD cache.**

**Split**
- Tuning set: 15% of subjects, site-stratified, fixed seed.
- The remaining ≈1016 subjects: 5-fold site-stratified subject cross-fitting. In each training fold, an inner 10% of subjects serves as validation for ridge λ and MLP early stopping.
- Split manifest: hashed positions plus sha256, and `group_overlap_audit.py`.
- Fallback: a single 60/20/20 split, accepting a CI half-width of ≈0.009.

**Target, horizon and metric**
- Target: top-8 PCs of the pooled training-fold data, Z = X·V_train.
- Horizons in seconds: primary h = 2 s (1 sample); secondary 4 s; 6 s exploratory.
- Metric: per-subject guarded R² (ss_tot about that subject's own test mean), averaged over subjects. Skill versus persistence is secondary.
- Paired subject bootstrap 95% CI (10k) for each contrast. Site-cluster bootstrap and a per-site table as sensitivity checks.

**Conditions**
- Baselines: constant; persistence; identity ridge (48→8); PCA-24 + ridge; random ReLU-24 (same init distribution, no lateral).
- Local engine arms: L-C0…L-C5, cFFL off for all.
- Backprop arm: BP-MLP 48→24 (ReLU)→8. Adam, early stopping on the inner validation subjects, weight decay chosen on the tuning set, 10 seeds. Plus BP-refit: frozen encoder with a ridge readout.
- Drop the linear 48→24→8 bottleneck. With an 8-d target it reduces to identity ridge.
- Capacity: MLP 1376 parameters versus about 1350–1500 for the engine arms (C1–C4) plus readout.

**Topology**
- C1/C2 graph realisation = run seed (10 realisations).
- Optional sharpest control: a degree-preserving rewire of C4.
- State C4's property as "0 designated-hub edges". Do not state it as R_hub, which is 1.857 under the code's own definition (O16).

**Engine: a qualification gate (synthetic only) before the card is frozen.** Name exactly one engine, and only after it passes every pre-declared criterion below. Set the thresholds before running, at ≥3 synthetic parameter points, and never loosen them.
- **Q1 stability for every mask at stress:** a postsynaptic-local guard checked after each update; non-convergence < 0.1%.
- **Q2 planted structure at m = k (not m > k; O18b) for the engine's own objective:**
  - for linear PSP: subspace alignment ≥ 0.95 (0.997 dense vs old 0.76–0.86);
  - for a rectified / NSM engine: recovery of planted non-negative sparse sources.
- **Q3 learning value:** on the BOLD-like VAR, the engine beats random ReLU-24 by a pre-set margin. Engine R currently does not (O18b).
- **Q4 topology can matter in principle:** the readout must not be invariant to the subspace rotations the masks induce. A ±-paired rectified output stage on top of guarded linear PSP is one candidate; it recovers 0.434 of 0.483 at fixed PCA directions (O18b).

**Decision if nothing qualifies within the milestone:**
- deliver the card, the implementation, the qualification report and verdict `no_candidate`;
- run no real data.

**Excluded engines:**
- the old fractal engine (O9/O10/O13/O15). At most it can appear as a labelled "legacy" arm.
- `local_learning_engine` (its (yyᵀ)W term is non-local).
- unguarded masked PSP (O11).
- the probe-F engine R as it stands (O18b).

**Tuning, seeds and hypotheses**
- Tuning: a grid of ≤6 configurations, with one configuration shared by all masks. Per-mask tuning could manufacture topology differences. The MLP gets the same budget.
- Seeds: 10, paired across conditions. Average per-subject R² over seeds before the bootstrap; report the seed SD.
- Hypotheses: Bonferroni over four contrasts, so each paired subject-bootstrap CI is at 1 − 0.05/4 = 98.75%. SESOI δ = 0.01 R² (**PI to confirm δ**).
  - H1 topology: Δ = L-C4 − ½(L-C1 + L-C2).
  - H2a learning value: L-best (chosen on the tuning set) − random ReLU-24.
  - H2b practical value: L-best − identity ridge.
  - H3: L-best − BP-MLP, one-sided "local beats backprop".
  - Decision rule for each: survives if CI_low > 0 and the point estimate ≥ δ; killed if CI_high < δ; otherwise inconclusive.
  - (If Holm is preferred, use one-sided bootstrap p-values with Holm and report CIs at the matched level. Do not mix Holm with CI rules.)
- State the expected outcome: H2b/H3 likely killed (O18b), H1 likely inconclusive. Nulls are results.

**Pre-test validity gates** (on the tuning set only, before cross-fitting):
1. Persistence and identity-ridge validation R² < 0.9.
2. The ss_tot guard never fires on a real subject. If it does, the data contract is violated: halt.
3. All fixtures are green.
4. Real-data non-convergence < 0.1% and the κ invariant holds.

### T4.3 Implementation + fixtures + run

**Layout**
- `src/topic4_resu/{data,metrics,split,topologies,baselines_linear}.py`
- `src/topic4_resu/local/engine.py`
- `src/topic4_resu/baselines_backprop.py`: torch; imported only by `scripts/topic4_run.py`.
- `tests/topic4_resu/`, `results/topic4/2026-11-01/`, `docs/03_empirical_analysis/topic4/`.
- Vendor the topology generator, with an equality test against the old function.

**Fixtures**
- **S1 contraction:** post-update κ_i ≤ κ_max for every mask at stress η_L = 0.1. The no-guard mutant must fail: non-convergence ≥ 1% on C5/C3 (O18).
- **S2 convergence:** the residual is below tolerance for ≥ 99.9% of samples.
- **S3 permutation equivariance:** deviation < 1e-10. A mutant with a gain ramp must fail (4.7, O13).
- **S4 planted structure.**
  - Linear dense reference: alignment ≥ 0.95 (0.997 vs old 0.76–0.86).
  - Rectified engine: non-collapse, centred PR(Y) ≥ threshold. C0 / no lateral must fail (PR 1.0).
  - Calibrate thresholds on ≥3 synthetic parameter points before freezing, and never loosen them afterwards.
- **S5:** F6 Bayes ceiling.
- **S6 no backprop**, three parts:
  - (a) AST scan of `src/topic4_resu/local/**` plus its in-repo transitive imports: forbid torch/jax/autograd/tensorflow/functorch imports, `importlib`/`__import__` calls, and imports of `baselines_backprop`.
  - (b) A subprocess with `sys.modules[m]=None` for those modules runs a full local training on synthetic data.
  - (c) Shuffling or zeroing the forecast targets leaves W, L and D bit-identical.
  - The mutants of O15 show each part is needed. The old Topic-4 path fails (b).
- **S7:** the engine state hash is unchanged by test inference.

**Run**
- Local CPU, nice, ≤4 processes, OMP = 2 each, detached with a progress log. Projected ≤2 h wall.
- Keep a run ledger that includes failed seeds, plus code, test and card hashes.
- Then give each hypothesis its verdict by the card's rules.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI/verification/explorer_M4_r1_2
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2; PY=/home/juke/superclaude-env/bin/python3
nice $PY probe_c_real.py                 # pos0: all 1.0, ss_tot~2.5e-45; pos932: R2 -0.08..0.05, ss_tot~5331; frac>0.25Hz ~0.01; persistence 1s 0.71 / 2s 0.15
nice $PY probe_a2_padding_realistic.py   # centred-then-padded -> 1.0; uncentred -> -1.0; unpadded 0.03/0.09
nice $PY probe_a_metric_fixtures.py      # guard raises; oracle~Bayes 0.705; off-by-one 1.000; A4 True/False
nice $PY probe_b_engines.py              # alignment PSP 0.997 vs old 0.76/0.86; rescale fires 57-79%; equivariance 4.7 vs 4e-15
nice $PY probe_b2_masked_psp_rk4.py      # masked PSP non-PD for C3 at eta/tau 0.02, C1-C4 at 0.1
nice $PY probe_d_nobackprop.py           # mutant matrix; old path fails torch block
nice $PY probe_f_rectified_local_engine.py  # guarded: nonconv 0 all masks; no-guard: up to 64%
nice $PY probe_h_engineR_planted_and_controls.py  # engine R m=8 alignment 0.79 (fails); VAR: R 0.18-0.21 ≈ random ReLU 0.18; PCA24 0.45 -> ReLU 0.32 -> ±paired 0.43
sed -n 417,425p;371,372p;350,352p;300,302p;377p;432p /home/juke/git/00IITP-AI/src/fractal_motif_resu.py
cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0 at 00:56Z
```
**Invalidation conditions:**
- a valid-window subject gives R² = 1.0 under the old code;
- TR = 2.0 identity-ridge validation R² ≥ 0.9;
- the guarded engine fails to converge on real tuning data;
- the vendored loader differs from Topic 1's at the pinned sha.
