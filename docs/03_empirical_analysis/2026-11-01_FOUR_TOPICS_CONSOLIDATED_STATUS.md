# Consolidated Status Report: 4 Empirical Studies (`tw-20261031-four-topics`)

- **Date**: 2026-11-01 KST
- **Repository**: `/home/juke/git/00IITP-AI` (Branch: `feature/topic1-lag-motif-v2`)
- **Governing Run**: `.agents/teamwork/tw-20261031-four-topics/`
- **Protected Hashes**: Verified 67/67 intact (`.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`) and 43/43 pinned Topic 3 outputs/code intact (`results/topic3/2026-10-31/output_sha256.txt`, `addendum_02_sha256.txt`).

---

## 1. Executive Summary Across the 4 Empirical Studies

| Milestone | Study Topic | Primary Code / Scripts | Current Status & Verdict |
| :--- | :--- | :--- | :--- |
| **M1 (Topic 1)** | `ENIGMA-OCD` Directed Lag Motif ($\vec{SP}$) & Multiband Hub Repulsion ($N=1,706$, 23 sites) | `src/topic1_lagmotif/`, `scripts/topic1_run_cohort.py`, `scripts/topic1_cohort_stats.py`, `tests/topic1_lagmotif/` | **Full Cohort Completed (`n=1,706`) — Pre-registered Verdict: `KILLED` (`stop`)**<br>• Primary unit `broadband@0.10`: **E1 ($Z_{030C}$)** $d = 0.113$, $p_{\text{FL}} = 0.0223$, $p_{\text{Holm}} = 0.0446$ (passes Holm $\alpha=0.05$ but fails pre-registered effect-size bar $\|d\| \ge 0.15$).<br>• **E2 ($Z_{030C} - Z_{030T}$)** $d = 0.038$, $p_{\text{Holm}} = 0.4416$ (fails both).<br>• 0% degeneracy at primary unit; 23/23 extract & 24/24 stats mutants killed.<br>• Site-held-out LOGO AUROC: Lag motif `0.516` vs static FC `0.563`.<br>• Gate status: worker r1 & verifiers r1 passed; `victory_M1` audit was in flight when weekly quota paused the run. |
| **M2 (Topic 3)** | Brain Foundation Model Layerwise RG Flow & Heavy-Tailed Spectrum Diagnostics (`SwiFT`, `BrainLM`, `BrainJEPA`, `NeuroSTORM`) | `src/topic3_spectral/`, `scripts/topic3_*.py`, `tests/topic3_spectral/` | **Rerun & Addenda 01–03 Completed**<br>• **Family A (Subject-level, $n=57$)**: L2 $\to$ L3 drop is robust ($\Delta\text{covPR}_{28} = +5.34$, $\Delta\text{corrPR}_{28} = +6.04$) and replicates across all 4 LN-matched checkpoints (`A1b`), **refuting** per-channel LayerNorm scale as the cause.<br>• **Mechanism Check (`R2`)**: `ver11` has **no `PatchMerging` between `layer_2` and `layer_3`**; the drop occurs in between-subject pooled means across stage-3 Swin blocks, not token-level collapse.<br>• **Family B (Token-level)**: Effective rank ceiling at L2/LN0L2/L3 is **7** (8 near-static spatial cells minus 1, carrying $\ge 99.994\%$ variance). `H1a` holds in 2 deep NewUAH checkpoints ($+2\text{--}5\%$) but reverses in depth-matched `HCP_N400` ($-13\%$).<br>• **Guard Tests**: `test_verdict_rules.py` (30 tests) and `test_outputs_scanned_nonempty.py` added in Addendum 03. |
| **M3 (Topic 2)** | `a-SwiFT` / `SwiFT v3` Connectome Box-Covering RG Pooling ($\mathcal{R}_{l_B}$) | `src/rg_box_pooling.py`, `tests/test_empirical_four_topics.py` | **Pilot Verified (`86/86` baseline suite PASS) — Full Redesign Deferred to Workflow B**<br>• Pilot on `ENIGMA-OCD` 304-ROI ($304 \to 76$) reduces spectral exponent distortion $\|\Delta \alpha\|$ by 32.6% ($0.0739 \to 0.0498$) vs Euclidean contiguous merging.<br>• Full architecture training (`T2.1–T2.3`) queued for Workflow B (remote GPU / B300) after M1/M2 gate closure. |
| **M4 (Topic 4)** | Neuromorphic Backprop-Free Fractal-Motif ReSU (`FM-ReSU`) | `src/fractal_motif_resu.py`, `src/local_learning_engine.py`, `tests/test_pilot_connectome.py` | **Pilot Verified (`86/86` baseline suite PASS) — Full Redesign Deferred to Workflow B**<br>• 6-topology control at 25% wiring density shows Mode II Bio-Connectome (`C4`, $R_{\text{hub}}=0.0$ + cFFL delay bank) achieves `0.7242` RF orthogonality (96.1% of dense all-to-all) and `2.3280` PR per 100 synapses (2.45× Rich-Club `C3`).<br>• Full benchmark (`T4.1–T4.3`) queued for Workflow B after M1/M2 gate closure. |

---

## 2. Immediate Next Steps for Continuation

1. **Close M1 & M2 Verification Gates (`tw-20261031-four-topics`)**:
   - Complete the interrupted `victory_M1` audit on Topic 1 (`docs/03_empirical_analysis/topic1/2026-10-31_topic1_result_report.md`).
   - Run the r2 verifier pass on Topic 3 with the newly added 31 verdict-logic guard tests (`tests/topic3_spectral/test_verdict_rules.py`, `tests/topic3_spectral/test_outputs_scanned_nonempty.py`).
2. **Launch Workflow B (`M3` Topic 2 & `M4` Topic 4)**:
   - Dispatch heavy GPU training/sweeps to `connectome` (Slurm) / `dgx1` / `B300` per repository governance (`can_push: false` locally).
