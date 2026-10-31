# Handoff — explorer_survey_3 (run tw-20261031-four-topics, survey)
Written 2026-10-31T07:50Z. Type: explorer analysis report. Read-only; no production code changed.
All real-data numbers below are feasibility probes on ≤5 ENIGMA subjects (positions 0–4) or on existing VRABES pooled files. They govern no result (C3/C8). The probe subjects are DEVELOPMENT subjects: a confirmatory card must exclude them or declare them.

**Summary.** Topic 4's forecast R²=1.0 for every condition is a deterministic 0/0 artefact. The chronological test split (rows 324–463 of the 464-row VMD cache) is 100% zero padding for subjects with valid_T=177, so target and prediction are both ≈0. ss_tot (≈1e-45) is clamped to 1e-8, ss_res≈0, and R²≡1 for any encoder. Two further defects sit under it: the ReSU engine collapses to a rank-1 representation, and the IMF1 input is so smooth that persistence scores R²≈0.96 after trimming. B300 has 32/32 GPUs idle but no torch, no pip/ensurepip and no staged data. A project-local env via the existing `~/.local/bin/uv` is feasible. M4 needs no GPU.

---

## 1. Observation

### M4 / Topic 4
| # | Observation | Evidence |
|---|---|---|
| O1 | Input = `vmd_cache_4ch_464_head.mmap[i, 0]` (IMF1, band-passed + z-scored per ROI, zero-padded to 464 at the tail); 48 ROIs by `linspace(0,303,48)` | src/fractal_motif_resu.py:457-467; enigma datasets.py:102-108, 285-317 (`F.pad(..., (0,pad))`) |
| O2 | Positions 0–4: valid_T=177/464, test rows valid = 0/139, ss_tot_test ≈ 2e-45…6e-45 | verification/explorer_survey_3/probe_t4_data.log |
| O3 | After z-scoring over all 464 rows the padded rows are ≈3e-9 (column mean ≈0 because IMF1 was already z-scored on the valid part) | probe_t4_repro.log ("padded rows after z-score: max\|x\|=2.74e-09") |
| O4 | R² = `1 - ss_res/max(ss_tot,1e-8)`, clipped at −1; the target uses SVD on the full stream incl. test; online local training also runs over the full stream incl. test | fractal_motif_resu.py:330-332, 349-356, 375-383 |
| O5 | Reproduced: padded stream → R²=1.0 for C0–C5 on all 3 subjects. Padding stripped → R² from −1.0 to −0.42 (all ≤ train-mean baseline). Persistence on the trimmed IMF1 = 0.946–0.983; ridge on raw p_t = 0.75–0.87 | probe_t4_repro.log |
| O6 | Representation collapse: effective_dim_PR 1.00–2.06 and RF orthogonality 0.0002–0.35 (most ≈0.001) even on trimmed data. The old JSON has PR 1.003–1.015 and orth 0.0008–0.006 for all conditions | probe_t4_repro.log; empirical_results.json topic4 |
| O7 | The W update is single-unit semi-implicit Oja (denominator `1+eta_w*y_i^2`, no `Σ_j y_j W_j` term), so each unit converges to the top PC unless the lateral M breaks symmetry. For C0, M_mask=0 means no decorrelation at all. The M update is clipped and rescaled to ρ<0.98 through `M_hier` (lower-tri + 0.25 upper-tri) | fractal_motif_resu.py:281-302 |
| O8 | PR estimator is UNCENTERED (`svd(X)` without mean removal); for non-negative ReLU outputs the mean vector dominates, which biases PR toward 1 | src/spectral_rg_flow_diagnostic.py:55-64 (also used by Topic 4 at :362-363) |
| O9 | Confound: `use_cffl = "Bio_Fractal" in name` gives ONLY C4 the extra W_d delay-bank input (4 exponential filters). So C4 vs C1–C3 is not topology-only. Probe 2 used the module default (C4 has cFFL); probes 3–4 set `use_cffl_boxes=False` for all | fractal_motif_resu.py:337; probe_t4_rawtask.py / probe_t4_pooled.py |
| O10 | Topologies: C1–C4 each have 69 undirected edges (matched). C4 has 0 edges among its designated hubs {0,6,12,18}, but the code's own metric `compute_hub_repulsion_ratio(hub_frac=0.33)` gives C4 R=1.857, higher than C1 (1.571). The docstring claims R_hub=0.0 | probe_t4_topologies.log; fractal_motif_resu.py:58-59 |
| O11 | Two different `ReSULocalEngine` classes exist: local_learning_engine.py:173 (Oja-subspace `(yy^T)W` term, used by pilot) and fractal_motif_resu.py:221 (single-unit semi-implicit Oja). The Topic-4 result used the latter | both files |
| O12 | Raw full-band series (npy dir, positions 0–4, head trim 20, trailing zeros stripped): T=177, lag-1 autocorr 0.50–0.66. Per-subject 70/30 forecasting is unstable (h=1 persistence 0.04–0.43; everything negative at h≥2) | probe_t4_rawtask.log |
| O13 | Pooled leave-one-subject-out (4 train / 1 test, PCs and encoders fitted on the train subjects only), h=1 LOSO R² mean (sd): identity ridge on p_t **0.362 (0.068)** > persistence 0.297 (0.109) > ReSU-C4(no cFFL) 0.220 (0.044) > random ReLU-24 0.185 (0.046) > ReSU-C0 0.174 (0.038) > backprop MLP 48→24→8 −0.123 (0.130). At h=2 all are ≈0 (−0.29 to +0.06), except the MLP at −0.67 | probe_t4_pooled.log |
| O14 | The backprop MLP in O13 is an UNTUNED probe: full-batch Adam, 1500 steps, wd 1e-3, no early stopping, no validation subject. Its negative R² shows overfitting, not that "backprop loses" | probe_t4_pooled.py:mlp_bp |
| O15 | The mmap subject order equals the sorted npy-dir order (boolean check only: `full_order_identical True`), so probes 1–2 and 3–4 used the same 5 subjects | probe_order_and_mutants.log |
| O16 | The old suite's AST audit scans `SRC_DIR.glob("*.py")` (top level only) and fails on any `backward()`, `torch.autograd` or torch import there (excluding titans_demo.py and rg_box_pooling.py) | tests/test_pilot_connectome.py:160-185 |

### B300 (read-only; 0 GPU-h used; nothing installed or started)
| # | Observation | Evidence |
|---|---|---|
| B1 | .99 (`cloud-yPw2G7`): 8× B300 SXM6 (275,040 MiB each), 0 MiB used, 0% util, 0 compute processes, load 0.10. Nodes .98/.101/.103 also have 8/8 GPUs at 0 MiB/0% with 0 processes → **32/32 idle** at 07:36Z | b300_99_readonly.log, b300_other_nodes_readonly.log |
| B2 | Driver 580.196.07, CUDA 13.0 driver API; no nvcc; /usr/local/cuda-13.0 present; no Slurm (`sbatch`/`squeue` absent) | b300_99_readonly.log |
| B3 | System python 3.12.3; no torch; **no pip, no ensurepip** (python3-venv not installed), so `python3 -m venv` would fail at the ensurepip step. `uv 0.13.6` is at `~/.local/bin/uv`; internet works (pypi.org and download.pytorch.org return HTTP 200) | b300_99_readonly.log |
| B4 | Another project's env `~/envs/swiftllm` (6.2 GB, torch 2.15.0+cu134, CUDA 13.4, numpy 2.5.4, scipy 1.18.1) exists on all 4 nodes. `/scratch/tmp/gpu_verify.out` shows `GPU_VERIFY PASS ... 2.15.0+cu134 n=8`. It belongs to SwiFT-LLM, so it is NOT project-local under C5 | b300_99_readonly.log |
| B5 | /scratch = RAID0 over 8 local NVMe, 28 TB, ~1% used. `~/envs/setup_node.sh` says "A VM stop blanks the disks". `/scratch/iitp4` does not exist yet | b300_99_readonly.log |
| B6 | `/scratch/data/hcp` and `/scratch/data/ukb_raw` are EMPTY (4.0K each). No public or UKB data is staged | b300_99_readonly.log |
| B7 | 224 CPUs, 2.1 TB RAM on .99 | b300_99_readonly.log |

### M2 / Topic 3
| # | Observation | Evidence |
|---|---|---|
| T3a | Real inputs exist locally: VRABES/RemissionAnalysis/pooled_E192_layers/layer_{0..3}.npz (57×384, 57×768, 57×1536, 57×1536), pooled_{brainlm,brainjepa}_matrix.npz (57×768), pooled_neurostorm_matrix.npz (25×288). **Every file has an `ids` key** | probe_t3_pr.log |
| T3b | Uncentered PR = 1.001–1.074 (reproduces the JSON). Centered PR: L0 2.78, L1 2.78, L2 11.02, L3 3.58, BrainLM 4.32, BrainJEPA 11.79, NeuroSTORM 12.51. Column means are 3–30 column-SDs | probe_t3_pr.log |
| T3c | Estimand: one mean vector per subject (tokens, then 7 frames averaged), so PR measures between-subject spread with centered PR ≤ n−1 = 56 (NeuroSTORM ≤ 24). layer_3 is pooled over (D,H,W,T) from a 5-D tensor; layers 0–2 over tokens (L,C). Original per-frame embeddings are on NERSC /pscratch (not local) | VRABES/RemissionAnalysis/pool_E192_layersweep.py:1-30 |
| T3d | When files are missing, the old code silently substitutes `rng.randn` synthetic matrices | spectral_rg_flow_diagnostic.py:229-240 |

### M3 / Topic 2
| # | Observation | Evidence |
|---|---|---|
| T2a | E192 embeddings were extracted with `simmim_swin4d_ver11, embed_dim 192, depth 2 2 18 2`, and layer_3 is (1536, 2,2,2,20) | VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh:17-22, 82 |
| T2b | The local SwiFT_v2 (commit f0dc7aca) `simmim_swin4d_transformer_ver11.py` PatchMergingV2 merges 2×2×2 SPATIAL neighbours only (`x[:, :, i::2, j::2, k::2, :]`, `Linear(8*dim, 2*dim)`); downsample is applied at the end of stages 0–2 and `None` for the last stage | ver11.py:41, 72, 81, 1068 |
| T2c | (Contrast) ver10 PatchMergingV2 concatenates over d,h,w AND t (`Linear(16*dim, …)`) despite its comment "Skip dimension reduction on the temporal dimension" | simmim_swin4d_transformer_ver10.py:384-400 |
| T2d | Token counts in the extraction docstring: layer_0 (10240 = 8³·20, 384), layer_1 (1280 = 4³·20, 768), layer_2 (160 = 2³·20, 1536), layer_3 (2³·20, 1536). So the extracted layers are POST-merge. Spatial merges: 16³→8³ (before layer_0), 8³→4³ (layer_0→layer_1), 4³→2³ (layer_1→layer_2), **none between layer_2 and layer_3** | pool_E192_layersweep.py:3 |

### M1 / Topic 1
| # | Observation | Evidence |
|---|---|---|
| T1a | Surviving mutants (rc==0, control excluded): mutants.py → `roi_subsample_80`; mutants_extra.py → `curl_returns_F`, `seeds_ignore_position`, `sp_not_normalised`, `extract_subject_drops_valid_T` | probe_order_and_mutants.log |
| T1b | Both scripts hardcode outputs into `verification/victory_auditor_1/mutation_results*.json` and `rmtree` their BASE dir `verification/victory_auditor_1/mut/<name>` before rebuilding. They copy src/tests into that BASE (they do not mutate the repo src) | verification/victory_auditor_1/mutants.py:6-7, 45-68, 89-90; mutants_extra.py:16 |
| T1c | Protected hashes: `LC_ALL=C sha256sum -c …/PROTECTED_HASHES.txt` → **rc=0**, 67 lines, 0 non-OK (07:42Z) | own run |

### Housekeeping
- `verification/explorer_survey_3/` already held 9 probe files plus `__pycache__` from the **2026-10-30** run's explorer_survey_3 (mtimes 2026-10-30 20:14–20:24). My files use different names; nothing was overwritten. I did not delete theirs.
- No background processes were started; `ps` shows 0 probe processes.

## 2. Logic Chain
1. O1+O2: the 70/30 chronological split at index 324 falls entirely in the zero padding for valid_T=177 subjects, so the test targets are the padded rows.
2. O3+O4: padded rows ≈0 after z-scoring → Z_true(test) ≈ 0 → ss_tot ≈ 1e-45, clamped to 1e-8. Every encoder maps ≈0 input to ≈0 output (ReLU of W·0; C0 has no lateral drive), so ridge predicts ≈0 and ss_res ≪ 1e-12 → R² = 1.0000 after rounding, independent of topology. This explains "all conditions incl. C0 = 1.0, std 0.0". It is a bug (padding not stripped) plus an unsafe R² floor, not an easy task or a leak per se.
3. O5: removing the bug exposes that the ReSU encoders are worse than the train mean (R² ≤ −0.42) on IMF1, while persistence ≈0.96. So the IMF1 1-step task would saturate the trivial baseline anyway. IMF1 is the wrong input for a forecasting test.
4. O6+O7+O8: PR≈1 has two causes. (a) Real collapse: orthogonality ≈0 means parallel receptive fields, which follows from single-unit Oja without effective competition. (b) The uncentered PR estimator inflates the collapse. The engine-level defect must be fixed (or a canonical similarity-matching/PSP network used) before any topology comparison means anything.
5. O9+O10: even with a working engine, the old C4 differs from C1–C3 in input (cFFL delay bank) and does not satisfy its own hub-repulsion claim under the code's metric. So "C4 is best" could never have been attributed to topology.
6. O12–O14: on raw full-band BOLD with pooled LOSO training, h=1 is far from saturation (0.17–0.36) and has spread between methods. The trivial identity-ridge baseline currently beats all ReSU variants. Single-subject forecasting is too short (T≈177) to be stable. So a pooled cross-subject design with matched-capacity controls is the testable form.
7. B1–B7: B300 is idle and usable, but the env must be built project-locally with uv (venv/pip are missing). The data dirs are empty, and /scratch is ephemeral. M4 uses ENIGMA (C6 forbids B300) and runs on CPU in about a minute per 5-subject LOSO, so M4 should stay local/connectome on CPU. M3 on B300 is blocked until a permitted dataset (UKB derivatives / public) is staged.
8. T3a–T3d: the "PR≈1" in empirical_results.json is the uncentered estimator (T3b), so the earlier "rank collapse" regime labels are artefacts. The centered values make layer_2 the most spread (11.0) and layer_3 contract (3.6). But the estimand is between-subject spread at n=57 (T3c), not within-layer representational dimensionality, and the α fits have ≤56 eigenvalues.
9. T2a–T2d: the premise "PatchMerging between layer_2 and layer_3, both 1536-d" is false for ver11. The last stage has no downsample; layer_2 is already post-merge (4³→2³). With only 2³ spatial cells left at layer_2/3, box pooling has nothing meaningful to act on there. The only scientifically meaningful insertion points are the 16³→8³ and 8³→4³ merges.
10. T1a+T1b: T1.1 must kill 5 named survivors. Rerunning the auditor scripts in place would overwrite the 2026-10-30 receipts and rmtree inside another agent's verification folder, so M1 must run an adapted copy with BASE and output in its own verification dir.

## 3. Caveats
- n=5 (Topic 4) and n=57 (Topic 3) development probes only; no inference. The 5 ENIGMA subjects all had T=177 and probably share one site/TR; TR was not checked. Horizons were stated in samples, not seconds.
- I did not compute the full-cohort valid_T/TR distribution (dispatch limit ≤5 subjects). How many subjects have >324 valid rows is unknown; Topic 1's T1.3 manifest will produce it.
- I did not test whether the local_learning_engine.py variant (Oja-subspace) also collapses on real data. Its `(yy^T)W` term is non-local (unit i's update reads W_j of other units), which matters for a "strictly local" claim.
- The SwiFT architecture was read from the local SwiFT_v2 checkout. The extraction ran on the NERSC perlmutter fork (`/pscratch/.../SwiFT_v2_perlmutter`), which was not inspected and could differ.
- B300 snapshot at 07:36–07:38Z only; occupancy may change. I did not check `uv venv` creation, CUDA init, or that pip can reach the cu134 index from inside a fresh env.
- The backprop baseline in O13 is untuned (O14); its number must not be cited.
- My earlier progress.md heartbeat timestamps (07:45Z/07:52Z) were guesses and were corrected.

## 4. Conclusion (recommendations; not implemented)

### M4 — Topic 4 redesign
**T4.1 diagnosis (evidence complete):** the root cause is zero padding in the test split plus the `max(ss_tot,1e-8)` floor → 0/0 → R²≡1 (O1–O5). Contributing defects:
- full-stream SVD, z-scoring and online training all touch the test rows (leak);
- IMF1 narrowband input makes persistence ≈0.96;
- the ReSU engine collapses (single-unit Oja, C0 has no competition);
- the PR is uncentered;
- C4 has a cFFL input confound and fails its own R_hub claim.

Required fixtures:
- (a) a padded synthetic stream must trigger a hard error or be stripped, and must never produce R²=1;
- (b) R² must raise when ss_tot < ε instead of clamping;
- (c) a constant-predictor encoder must give R²≤0 on a non-degenerate test.

**T4.2 proposed non-saturating task:**
- **Data:** raw full-band ROI series (npy dir), trailing zeros stripped with the Topic 1 loader (`src/topic1_lagmotif/data.py: valid_portion/prepare_series`), head trim in seconds, 48 ROIs (or a Schaefer-like subset). Exclude development positions 0–4 from the confirmatory set.
- **Split:** subject-level (participant-disjoint), site-stratified, train/val/test, e.g. 60/20/20. All z-scoring, PCs and encoder learning on TRAIN subjects only; per-subject z-scoring within subject is allowed.
- **Target:** top-8 train-PC scores at horizon h; primary h ≈ 2 s (1 sample at TR=2 s; define h in seconds and resample or restrict to one TR). Secondary h ≈ 4–6 s.
- **Metric:** held-out-subject R² and skill = 1 − MSE/MSE_persistence, with subject-level bootstrap CI.
- **Conditions (equal width 24, same readout = ridge with λ chosen on val):**
  - identity ridge on p_t (the trivial baseline that currently wins);
  - persistence;
  - **PCA-24 + ridge** (the key control: a working similarity-matching network converges to the PCA subspace, so ReSU ≈ PCA means topology has nothing to act on);
  - fixed random ReLU-24 (reservoir control);
  - ReSU with each topology C0–C5 **with the cFFL input identical across conditions** (all off, or all on);
  - backprop baselines.
- **Backprop baselines:**
  - (i) end-to-end MLP 48→24 (ReLU)→8 trained by Adam/SGD with early stopping on the val subjects and a small weight-decay grid;
  - (ii) linear 48→24→8 bottleneck by backprop (≈ reduced-rank regression, an analytic check).
  Same width, data and seeds as ReSU.
- **Kill rule (example):** the topology hypothesis is killed if the best ReSU topology does not beat both PCA-24 and identity ridge on held-out skill (CI excludes 0), or if C4 does not beat C1/C2 (matched edges) by a pre-registered margin.
- **Engine precondition:** before any topology comparison, a synthetic planted-subspace fixture must show the local rule recovers the top-k subspace (principal-angle alignment ≥ threshold), with the representation not collapsed (centered PR ≥ k−ε). Prefer the canonical Pehlevan–Sengupta–Chklovskii PSP rules (ΔW ∝ yxᵀ−W, ΔM ∝ yyᵀ−M with M including the diagonal, y = M⁻¹Wx), all strictly local. A second fixture: VAR(1) synthetic with known Bayes-optimal R² at h, so the ceiling is known and not saturated (e.g. Bayes R² 0.3–0.6).
- **Topology fixture:** equal edge counts across C1–C4, plus a stated, consistent hub definition (designated hubs vs top-degree) with the R_hub value the card claims.

**T4.3 placement and safety:**
- Put the code in `src/topic4_resu/`, not `src/*.py`. Otherwise a torch-based backprop baseline breaks the old AST audit (O16) and C2's 86-pass suite.
- Give the local-learning module its own test proving no autograd path: AST scan of that module plus a runtime check that it runs with torch absent from `sys.modules`, or under `torch.no_grad` with every tensor `requires_grad=False`.
- Add a spectral-radius fixture ρ(M∘mask) < 1 after every update.
- Run on CPU locally (nice, ≤16 procs) or on connectome. **Not on B300** (ENIGMA data, C6). The GPU is unnecessary.
- Name explicitly which `ReSULocalEngine` is used.

### B300 readiness (for M3, and M2 only if regeneration is needed)
- **Usable now:** 32 idle B300 GPUs; driver 580; uv 0.13.6; internet works; 28 TB /scratch.
- **Env recipe (project-local, C5):**
  ```
  UV_CACHE_DIR=/scratch/iitp4/uvcache ~/.local/bin/uv venv --python 3.12 --seed /scratch/iitp4/venv
  uv pip install --python /scratch/iitp4/venv/bin/python torch==2.15.0+cu134 --index-url https://download.pytorch.org/whl/cu134 (+ numpy/scipy)
  ```
  Pin the hashes, using the torch line from `/scratch/tmp/requirements.lock` as a reference for the known-good B300 build. Do not reuse `~/envs/swiftllm`.
- **Ephemeral disk:** /scratch is wiped on VM stop. Keep the env recipe and lock in the repo (e.g. `scripts/b300_env/`), and copy results back to lab storage after each run.
- **Blocker:** no permitted data is staged on B300 (B6). M3 needs UKB derivatives or public data copied there first, and that copy must not include ENIGMA or VRABES files with `ids`.
- **Ledger:** `results/gpu_ledger_2026-10-31.md` does not need a survey entry (0 GPU-h used).

### M2 — Topic 3
- Resolve PR≈1 with a fixture: a rank-k matrix plus a large constant offset gives uncentered PR≈1 and centered PR≈k.
- The card must state the estimand honestly (between-subject spread, n=57, PR ≤ 56) and note that NeuroSTORM (n=25) is not comparable.
- Remove the silent synthetic fallback (T3d) and fail hard instead.
- α estimator: report its method and the ≤56-eigenvalue limit.
- Never print or copy `ids`; keep the files local (no GPU is needed).
- A token-level, within-subject layerwise PR requires the NERSC frame embeddings or regeneration (a GPU job; the data are VRABES participants, so a lab machine, not B300, unless de-identified representations are approved).

### M3 — Topic 2
- Document T2b–T2d. The defensible redesign replaces the 8³→4³ (and/or 16³→8³) PatchMergingV2 with box pooling, keeping parameters and token counts matched.
- Check the perlmutter fork's ver11 before claiming equivalence.
- Without staged data on B300, deliver the card, implementation and a costed plan (T2.3 escape clause).

### M1 — Topic 1
- Kill the 5 survivors (T1a).
- Rerun them from a copy of mutants.py/mutants_extra.py with `REPO` read-only and `BASE` and the output JSON under `verification/<m1-worker>/`. Never overwrite `verification/victory_auditor_1/*`.
- Protected hashes are currently rc=0.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
PY=/home/juke/superclaude-env/bin/python3; export PYTHONDONTWRITEBYTECODE=1
$PY verification/explorer_survey_3/probe_t4_data.py      # valid_T=177, test_valid_rows=0/139, ss_tot≈1e-45
$PY verification/explorer_survey_3/probe_t4_repro.py     # padded R2=1.0 all; trimmed ≤ -0.42; persistence ≈0.95-0.98
$PY verification/explorer_survey_3/probe_t4_pooled.py    # LOSO h=1: raw_p 0.362 > persist 0.297 > resuC4 0.220 …  (~1 min CPU)
$PY verification/explorer_survey_3/probe_t3_pr.py        # uncentered ≈1.0x vs centered 2.8–12.5
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt; echo rc=$?   # expect 0
ssh connectome@61.107.201.99 'nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv; python3 -c "import torch"; ls /scratch/data/*; ~/.local/bin/uv --version'
grep -n "x\[:, :, i::2, j::2, k::2" /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py
```
**Invalidation conditions:**
- the diagnosis is wrong if a subject with valid_T > 324 also gives R²=1.0 for all conditions after stripping;
- the B300 status is stale if nvidia-smi shows processes or /scratch/data gets populated;
- the Topic 2 claim depends on the perlmutter fork matching local ver11.
