# Handoff Report — victory_FU_B_r1 (Victory Audit of Milestone FU_B)

## 1. Observation

1. **Governance & Freeze Receipts (Phase A — Timeline & Provenance, C1, C3, F1):**
   - `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` returned `rc=0` (`67/67 OK`).
   - `grep -v '^#' results/topic2/2026-11-01/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c` returned `rc=0` (`33/33 OK`, including all 13 Python modules of `src/topic2_rgpool/`).
   - `grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c` returned `rc=0` (`31/31 OK`).
   - `grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256.txt | LC_ALL=C sha256sum -c` verified `28/29 OK`; the single difference is `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md`, whose v1 bytes are preserved in `verification/worker_FU_B_r1/card_v1_frozen_20261101T160518Z.md.txt` (`sha256=a9c4cab03ac99305e44b0aa2ab550fbe402f7f4b74ac3c239d082021e76e0726`). `diff -u` confirmed that only line 41 changed before any run started (replacing one hyphenated English word that tripped the frozen r1 BIDS-prefix regex with `"not be optimal"`, recorded in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_addendum_01.md`, `sha256=4acafa5b5746d1771d85d8403727d58ff6ecc2d27475f5d5b8ec7534edd80817`).
   - `grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c` returned `rc=0` (`50/50 OK`).
   - Timeline verified across all 18 `results/topic2/2026-11-02_fu_b/b300/runs/*/job_meta.json` and `run.json` files:
     - Card v1 frozen: `2026-11-01T16:05:18Z`
     - Card v2 re-frozen: `2026-11-01T16:20:25Z`
     - 4× F+ gate (`Fplus_{E,C,S}_s0_a1`, Slurm job `509_0..2`): earliest start `2026-11-01T16:20:41Z`, latest end `2026-11-01T18:16:16Z`.
     - Stage 1 (`hcp_{E,C,S}_s{0..4}_a1`, Slurm job `516_0..14`): earliest start `2026-11-01T19:19:08Z` (every task verified `gate_state_at_start == "pass"`), latest end `2026-11-02T02:08:39Z`.

2. **Forensic Code & Artifact Audit (Phase B — Integrity Check, C4–C8, F2–F3):**
   - `src/topic2_fu_b/{__init__,budget,design,records,slurm,verdict,view}.py` and `scripts/topic2fu_b_{c4scan,make_view,run,slurm,smoke,verdict}.py` contain genuine logic with zero hardcoded outputs, facade functions, or fabricated artifacts.
   - `src/topic2_fu_b/verdict.py` and `src/topic2_fu_b/records.py` reuse the frozen `src/topic2_rgpool/stats.py` functions (`t_interval`, `relative_gain`, `hierarchical_bootstrap`, `gate_fixture`, `verdict`) and close the `challenger_M3_r2_2` V01–V11 verdict-path defect classes (missing/invalid F+ gate → `no_verdict`; failed F+ gate → `inconclusive` without reading Stage 1; incomplete/failed/duplicate/wrong-budget/order-mismatched Stage-1 records → `no_verdict`; sha-verified literal `True` inherited F− only downgrades `keep`; strict card boundaries).
   - Every one of the 18 `b300/runs/*/run.json` records has `status == "completed"`, `cfg == "E36_d2262"`, `steps == 35000`, `batch == 16`, `lr == 0.0002`, `wd == 0.05`, `warmup_frac == 0.05`, `mask_ratio == 0.6`, `n_params == 38712096`, `code_sha256` matching all 13 `src/topic2_rgpool/*.py` freeze pins, `perm_file_sha256` and `perm_sha256` matching `perms_hcp.npz` / `perms_Fplus.npz`, `test_nmse == sum(test_num)/sum(test_den)` to float64 precision (`<= 1e-15`), `val_nmse_curve` at steps `(8750, 17500, 26250, 35000)` matching `train_log.jsonl` (350 train events + 4 val events + 1 done event per run), and for HCP `split_file_sha256 == cc521b087a97a6669fe6f94041dac2c2c0c0987741ac698203309af1ced2c75a`, `n_train_windows == 7616`, and identical positional `test_pseudonyms` (`h13..h85`).
   - **C4 & C6 compliance:** `results/topic2/2026-11-02_fu_b/b300/view_check.json` confirms 88 subjects mapped to positional `h00..h87` hard links (`176` links, `0` conflicts, `0` r1 files modified after cut, exact `64/8/16` split match). `results/topic2/2026-11-02_fu_b/b300/c4_scan_b300.json` reports `0` hits across `108` text files against `176` in-memory r1 tokens. Independent repo scan in `verification/victory_FU_B_r1/verify_victory_fu_b.py` and `tests/topic2_rgpool/test_outputs_no_ids.py` found `0` BIDS prefix strings or HCP ID leaks. No `.pt` checkpoints or subject tensors were copied off B300.
   - **C5 & B300-share compliance:** `results/gpu_ledger_2026-10-31.md` logs all 22 FU-B Slurm tasks on `b300-01`: explorers (`413`, `402`, `419`: `0.140 GPU-h`), worker smoke (`490`: `0.070 GPU-h`), 4× F+ gate (`509_0..2`: `5.070 GPU-h`), and Stage 1 (`516_0..14`: `25.440 GPU-h`), totaling **`30.720 GPU-h` ≤ `33.0 GPU-h` cap** (and run total `59.279 GPU-h` ≤ `95.0 GPU-h` ceiling). `slurm/jobs.json` confirms `g3t_blockers: []` before each submission, and `GATE_STATUS.md` documents the root administrative hold/release on `516_[12-14]` during the `g3t-G-E0` window.
   - **C8 compliance:** Every number in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` matches `verdict.json`, `gate_4x.json`, `b300/runs/*/run.json`, and `results/gpu_ledger_2026-10-31.md`.

3. **Independent Recomputation & Test Execution (Phase C — C2, F2, F3):**
   - `verification/victory_FU_B_r1/verify_victory_fu_b.py` independently recomputed all gate and Stage-1 statistics from raw `b300/runs/*/run.json` (`rc=0`, output saved to `verification/victory_FU_B_r1/audit_summary.json` and `verification/victory_FU_B_r1/recomputed_verdict.json`):
     - **4× F+ gate (`gate_4x.json`):** `NMSE_E = 0.655098810312623`, `NMSE_C = 0.6306915097462201`, `NMSE_S = 0.6549144352138989`, `gain_C_vs_E = +0.0372574338133133` (`+3.73%`), `gain_C_vs_S = +0.03698639725320368` (`+3.70%`), `pass = True`, `state = "pass"`.
     - **Primary Stage-1 `I1 = (NMSE_E - NMSE_C)/NMSE_E`:** mean `+0.0006313784156132732` (`+0.063%`), SE `0.0013032022866913341` (`0.130%`), 95% t-CI (df=4) `[-0.00298689119435346, +0.004249648025580007]` (`[-0.30%, +0.42%]`). Since `hi = +0.425% < delta = 1.00%`, `verdict = "stop"` (rule 4, `I1_survives = False`).
     - **Primary Stage-1 `I2 = (NMSE_S - NMSE_C)/NMSE_S`:** mean `-0.0009249384123596362` (`-0.092%`), SE `0.0019948155459632256` (`0.199%`), 95% t-CI (df=4) `[-0.006463434270721709, +0.004613557446002436]` (`[-0.65%, +0.46%]`, `I2_lower_gt_0 = False`).
     - **Hierarchical bootstrap (`B=10,000, seed=0`):** `I1` median `+0.0006046689828177655`, 95% CI `[-0.0007790313382843394, +0.003376018815709519]`; `I2` median `-0.0008721202746176466`, 95% CI `[-0.004963178577478175, +0.0022808422639509366]`.
     - **Stall sensitivity (non-governing, dropping stalled `E_s0` → seeds 1–4, df=3):** `I1` mean `-0.0006705352632213122` (`-0.067%`), 95% t-CI `[-0.0009085804351286117, -0.0004324900913140127]` (`[-0.09%, -0.04%]`), `verdict_if_governing = "stop"`.
     - **Manipulation check (`r1_pairing`):** `E_seed_mean_r1 = 0.9889222408071936` → `E_seed_mean_fub = 0.9881109156858525` (`E_improved = True`), with 13/15 `(arm, seed)` runs achieving lower test NMSE at 4× than at 1×.
     - `recomputed_verdict.json` is byte-for-byte identical to `results/topic2/2026-11-02_fu_b/verdict.json` (`sha256 = 262b9c793af333af1658f95dfc96de3769c95d3fdddc300dd667813ee5f1e142`).
   - **Pytest suites executed sequentially on CPU (`CUDA_VISIBLE_DEVICES=""`):**
     - `tests/topic2_fu_b` + `tests/topic2_rgpool`: `244 passed, 24 warnings in 111.04s` (`tests/topic2_fu_b` alone: `128 passed in 5.23s`).
     - Old 86-test suite (`tests/e2e/test_full_system_scenarios.py tests/e2e/test_pilot_simulation_e2e.py tests/e2e/test_repository_integrity.py tests/e2e/test_theoretical_whitepaper_contract.py tests/test_empirical_four_topics.py tests/test_pilot_connectome.py`): `86 passed`.

## 2. Logic Chain

1. Because all 67 entries in `PROTECTED_HASHES.txt` and all 33 entries in `results/topic2/2026-11-01/code_sha256_at_freeze.txt` pass `sha256sum -c` (`Observation 1`), C1 and frozen r1 code preservation hold without modification.
2. Because `card_sha256_v2.txt` (`2026-11-01T16:20:25Z`) precedes the earliest B300 gate job start (`2026-11-01T16:20:41Z`), the gate completion (`2026-11-01T18:16:16Z`) precedes the earliest Stage-1 job start (`2026-11-01T19:19:08Z`), and the v1→v2 card diff is a single pre-run wording fix documented in `addendum_01.md` (`Observation 1`), C3 and F1 hold.
3. Because the FU-B implementation lives exclusively in its designated paths (`src/topic2_fu_b/`, `scripts/topic2fu_b_*.py`, `tests/topic2_fu_b/`), passes all 128 unit tests (and 44/44 mutations in `mutants_v2.out.json`), and closes V01–V11 (`Observation 2, 3`), C2 and F2 hold.
4. Because all 18 post-freeze training runs executed on B300 via Slurm within the 33.0 GPU-h budget (`30.720 GPU-h` used), used only the positional `hNN` hard-link view (`0` C4 hits), and our independent recomputation in `verify_victory_fu_b.py` reproduced `gate_4x.json`, `verdict.json`, and every reported table number identically (`Observation 2, 3`), C4, C5, C6, C8, and F3 hold.

## 3. Caveats

- **Pre-registered design limitations (nonblocking, disclosed in card §2/§7/§13 and result report §6.2):**
  1. The learning-rate schedule (`lr=2e-4`, 5% warmup = 1,750 steps, cosine decay over 35,000 steps) was stretched without hyperparameter re-tuning to isolate the 4× sample budget; on seed 0, `hcp_E_s0_a1` stalled (`test_nmse = 1.000000`) while `hcp_C_s0_a1` escaped late (`0.994161`), whereas on all four non-stalled seeds (seeds 1–4) arm E slightly outperformed arm C (`stall_sensitivity` `I1 = -0.07% [-0.09%, -0.04%]`, also `stop`).
  2. To fit within the 33.0 GPU-h cap, the 4× F+ gate used 1 seed (`seed 0`) and the F− bias gate was inherited from the 1× r1 run (`sha256`-verified `True`; only affects `keep`, never `stop`).
  3. Evaluation is on B300 copied-back run records and logs; raw subject tensors and `.pt` checkpoints remain on `b300-01` per C4/C6.

## 4. Conclusion

**Verdict: `VERIFIED_COMPLETE` (`VICTORY CONFIRMED`).**
Milestone `FU_B` (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds`) is genuinely, accurately, and reproducibly completed in full compliance with `ORIGINAL_REQUEST.md`, `ACCEPTANCE.md` (C1–C8, F1–F3), and PI decisions 1–8. Its confirmatory verdict is **`stop` (killed)**: at 560,000 training samples (`35,000 × 16`), `I1 = +0.06%` (`95% t-CI [-0.30%, +0.42%] < δ = 1.00%`) and `I2 = -0.09%` (`95% t-CI [-0.65%, +0.46%]`), ruling out a ≥ 1% practical gain of connectome box-pooling over PatchMergingV2 at 4× budget.

## 5. Verification Method

Run the following commands from `/home/juke/git/00IITP-AI`:

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/victory_FU_B_r1/verify_victory_fu_b.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_b tests/topic2_rgpool -q
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/e2e/test_full_system_scenarios.py tests/e2e/test_pilot_simulation_e2e.py tests/e2e/test_repository_integrity.py tests/e2e/test_theoretical_whitepaper_contract.py tests/test_empirical_four_topics.py tests/test_pilot_connectome.py -q
```
