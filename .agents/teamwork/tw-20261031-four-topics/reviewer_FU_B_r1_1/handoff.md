# Handoff — `reviewer_FU_B_r1_1` (Independent Review of Milestone `FU_B_r1`)

## 1. Observation

Milestone `FU_B` (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds (§7 ≈26 GPU-h; cap 33)`) was independently audited against `ACCEPTANCE.md` criteria `C1`–`C8` and follow-up criteria `F1`–`F3`.

- **Card & Code Freeze (`C1`, `C2`, `F1`)**:
  - `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md` defines a single 1-factor follow-up scaling training budget `4×` (`8,750 → 35,000` steps at batch `16` = `560,000` effective samples, validation at `8,750 / 17,500 / 26,250 / 35,000` steps) while holding fixed the frozen `src/topic2_rgpool` model/training code (`38,712,096` parameters), `E36` partition (`perms_hcp.npz`, `perms_Fplus.npz`), 64/8/16 HCP split (`split.json`), and RNG streams.
  - `results/topic2/2026-11-02_fu_b/card_sha256.txt` (`16:05:18Z`, 29 pins) and `card_sha256_v2.txt` (`16:20:25Z`, 31 pins, adding `2026-11-02_topic2_fu_b_addendum_01.md` after a 1-line C4 regex-text replacement at line 41 of the card) were both written strictly before the first post-freeze GPU run started (`Fplus_E_s0_a1` at `2026-11-01T16:20:41Z`).
  - `LC_ALL=C sha256sum -c` verified 31/31 pins in `card_sha256_v2.txt`, 50/50 pins in `output_sha256.txt`, 33/33 pins in `results/topic2/2026-11-01/code_sha256_at_freeze.txt`, and 67/67 pins in `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`.
- **Code & Test Suite (`C3`, `F2`)**:
  - All new code lives in `src/topic2_fu_b/` (7 files), `scripts/topic2fu_b_*.py` (6 files), and `tests/topic2_fu_b/` (6 files, 128 tests). Zero frozen r1 files were modified.
  - Sequential CPU-only pytest runs passed 100%: `tests/topic2_fu_b` (128 passed in 4.96s), `tests/topic2_rgpool` (116 passed in 158.57s), old suite 86 (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`, 86 passed in 43.49s), and `tests/topic1_lagmotif` (88 passed in 9.13s).
  - Independent adversarial probes (`verification/reviewer_FU_B_r1_1/adversarial_probe.py`, 10/10 passed) and worker mutation testing (`44/44` mutants killed in `mutants_v2.out.json`) confirm fail-closed handling of missing/failed F+ gates, incomplete/duplicate/tampered Stage-1 records, order mismatches, non-positional subject tokens, and inherited F− SHA/type verification.
- **Data Hygiene (`C4`)**:
  - `src/topic2_fu_b/view.py` and `scripts/topic2fu_b_make_view.py` created hard-linked positional directories `h00`..`h87` (`176` hard links verified in `b300/view_check.json`). Every HCP `run.json` contains only positional `hNN` tokens matching `split.json["test"]`.
  - Both `results/topic2/2026-11-02_fu_b/b300/c4_scan_b300.json` and our independent scan across 159 worker and reviewer files (`verify_fub_independent.py`) returned `0` hits for raw 6-digit IDs, BIDS prefixes, and non-synthetic 16-hex hashes.
- **Compute & Slurm Governance (`C5`)**:
  - All B300 GPU runs executed via Slurm (`job 505` smoke, `job 509` F+ gate array `0-2`, `job 516` Stage-1 array `0-14%4`) with pre-submission `squeue` checks confirming `0` active `g3t-G-E0-*` jobs (`slurm/jobs.json`).
  - Completed FU-B GPU usage in `results/gpu_ledger_2026-10-31.md` is `30.72 GPU-h` across 22 closing rows (`0.14` explorers + `30.58` worker) ≤ `33.0 GPU-h` cap; cumulative run total is `59.278 GPU-h` ≤ `95.0 GPU-h` ceiling.
- **Statistical Results & Verdict (`C6`, `C7`, `C8`, `F3`)**:
  - **4× F+ gate (`gate_4x.json`, seed 0)**: `NMSE_E = 0.655099`, `NMSE_C = 0.630692`, `NMSE_S = 0.654914`; relative gains `+3.726%` (`C vs E`) and `+3.699%` (`C vs S`), both ≥ `δ = 1.00%` → `pass = true` at `18:16:16Z`, over 1 hour before Stage 1 launched (`19:19:08Z`).
  - **Stage 1 (15 HCP runs, 5 seeds × arms E/C/S)**: 5-seed mean test NMSE `E = 0.988111`, `C = 0.987472`, `S = 0.986563`.
  - **Primary 95% t-intervals (df = 4)**:
    - `I1 (C vs E)`: mean `+0.063%` (`0.00063075`), SE `0.130%` (`0.00130195`), 95% CI `[−0.299%, +0.425%]` (`[−0.00298801, +0.00424551]`).
    - `I2 (C vs S)`: mean `−0.092%` (`−0.00092194`), SE `0.199%` (`0.00199184`), 95% CI `[−0.646%, +0.461%]` (`[−0.00645615, +0.00460827]`).
  - **Secondary hierarchical bootstrap (B = 10,000, seed 0)**: `I1` median `+0.060%` (`[−0.078%, +0.338%]`), `I2` median `−0.087%` (`[−0.496%, +0.228%]`).
  - **Governing Verdict**: Because `I1_t.hi = +0.425% < δ = +1.00%`, precedence rule 4 yields **`stop`** (`rule = 4`).
  - **Stall sensitivity (non-governing, card §9)**: Only `E_s0` stalled (`val_nmse >= 0.999` at all 4 checkpoints). Dropping seed 0 (`seeds_kept = [1, 2, 3, 4]`, df = 3) yields `I1 = −0.067% [−0.091%, −0.043%]`, `I2 = +0.091% [−0.229%, +0.412%]`, `verdict_if_governing = "stop"`.
  - **Manipulation check (`r1_pairing`)**: Seed-mean arm E test NMSE improved from `0.988922` (r1, 1×) to `0.988111` (FU-B, 4×) (`E_improved = true`), and 13/15 `(arm, seed)` pairs achieved lower test NMSE at 4× than at 1×.

---

## 2. Logic Chain

1. **Temporal & Cryptographic Integrity**: Every pre-registration pin in `card_sha256_v2.txt` (card, addendum, 21 FU-B source/script/test files, and 8 r1 inputs) matches its on-disk SHA-256 and predates the earliest GPU training timestamp (`16:20:25Z < 16:20:41Z`). Every output artifact in `output_sha256.txt` (50 files) and every protected file in `PROTECTED_HASHES.txt` (67 files) matches its SHA-256.
2. **Gate Precedence & Contract Compliance**: The 4× F+ gate completed and passed (`18:16:16Z`) before Stage 1 started (`19:19:08Z`). `src/topic2_fu_b/verdict.py` enforces the exact card §8 precedence (`missing F+ → no_verdict`, `failed F+ → inconclusive without reading Stage 1`, `incomplete/invalid Stage 1 → no_verdict`, `stats.verdict` with sha-verified inherited `F−` only able to downgrade `keep`).
3. **Exact Numerical Reproduction**: Independent recomputation from raw `run.json` and `train_log.jsonl` files (`verify_fub_independent.py`) reproduced every metric in `gate_4x.json` and `verdict.json` to `0.0` floating-point discrepancy, and re-running `scripts/topic2fu_b_verdict.py` produced a byte-identical `verdict.json`.
4. **Scientific Soundness of Verdict**: Because both the primary 5-seed t-interval (`[−0.30%, +0.42%]`), the secondary hierarchical bootstrap (`[−0.08%, +0.34%]`), and the 4-seed non-stalled sensitivity interval (`[−0.09%, −0.04%]`) lie strictly below `δ = +1.00%`, the `stop` verdict is unambiguous and robust.

---

## 3. Caveats

Two minor, strictly non-blocking documentation observations were identified (neither affects `verdict.json`, `gate_4x.json`, code, tests, or any governing/secondary inference):

1. **Descriptive column in `2026-11-02_topic2_fu_b_result_report.md` §2.3 (lines 96–110)**: In the per-run validation curve table, the 4 validation NMSE columns (`8,750`, `17,500`, `26,250`, `35,000`) and the `stalled` boolean column match `verdict.json` and `run.json` 100%, and the F+ gate `final train loss (last 100)` values in §1 (`0.61433`, `0.59195`, `0.61401`) also match `run.json["train_loss_last100"]` 100%. However, in the HCP table (§2.3 lines 96–110), the descriptive column `final train loss (last 100)` matches `run.json["train_loss_last100"]` (step 35,000 `loss_mean_last100`) only for `hcp_E_s0_a1` (`1.00174`), whereas for the other 14 runs it prints earlier-step training loss values around `0.9805–0.9926` instead of the step-35,000 values in `run.json["train_loss_last100"]` (`0.9730–0.9970`). Because `train_loss_last100` is not part of `verdict.json` and is not used by any gate, contrast, or stall rule (which uses `val_nmse_curve`), this is purely cosmetic.
2. **Minor path text in `worker_FU_B_r1/handoff.md` line 21**: Mentions `gate_4x.json` inside the `results/topic2/2026-11-02_fu_b/b300/` parenthetical list, whereas `gate_4x.json` lives at `results/topic2/2026-11-02_fu_b/gate_4x.json` (as accurately listed in `output_sha256.txt` and `2026-11-02_topic2_fu_b_result_report.md`).

---

## 4. Conclusion

**Verdict: `APPROVE`**. Milestone `FU_B` satisfies all requirements of `ACCEPTANCE.md` (`C1`–`C8`, `F1`–`F3`) with zero blocking issues and zero uncovered requirements.

---

## 5. Verification Method

All checks were executed CPU-only (`CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B`):

```bash
# 1. Protected & receipt SHA-256 verification
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_b/card_sha256_v2.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_b/output_sha256.txt

# 2. Sequential pytest execution (418 passed total)
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q tests/topic2_fu_b
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q tests/topic2_rgpool
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q tests/topic1_lagmotif

# 3. Independent statistical & adversarial probes
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_B_r1_1/verify_fub_independent.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_B_r1_1/adversarial_probe.py

# 4. Layout lint
/home/juke/superclaude-env/bin/python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics
```
