# handoff — worker_FU_B_r1 (FU-B, Topic 2 follow-up B) — HARD handoff, 2026-11-02T03:45Z

Milestone FU_B (4× training budget, `35,000 × 16 = 560,000` samples at SwiFT ver11 E36, arms E/C/S, 5 seeds) is complete. **The governed card verdict is `stop` (killed; rule 4: upper 95 % t bound of I1 < δ = 1.00 %).**

- **Result report:** `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md`
- **Governing card:** `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md` (v2 sha256 `994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae`, frozen at `2026-11-01T16:20:25Z` in `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt` with `2026-11-02_topic2_fu_b_addendum_01.md` before the first gate task `509_0` started at `16:20:41Z`; v1 frozen at `16:05:18Z` in `card_sha256.txt`, bytes preserved at `verification/worker_FU_B_r1/card_v1_frozen_20261101T160518Z.md.txt`).
- **Official verdict file:** `results/topic2/2026-11-02_fu_b/verdict.json`
- **Output receipt:** `results/topic2/2026-11-02_fu_b/output_sha256.txt`

---

## 1. Observation

1. **Card freeze and provenance.**
   - All 21 FU-B code and test files (`src/topic2_fu_b/*.py`, `scripts/topic2fu_b_*.py`, `tests/topic2_fu_b/*.py`), 8 pinned r1/env inputs, and the card were frozen in `card_sha256.txt` (`16:05:18Z`) and `card_sha256_v2.txt` (`16:20:25Z`) before the first post-freeze GPU task started (`509_0` at `16:20:41Z`).
   - All 13 Python files of the frozen `src/topic2_rgpool` package match `results/topic2/2026-11-01/code_sha256_at_freeze.txt` on disk and in every `run.json["code_sha256"]`.
2. **Pre-freeze smoke (`Slurm job 490`, 0.07 GPU-h, `results/topic2/2026-11-02_fu_b/b300/smoke_result.json`).**
   - Positional view check (`view_check.json`): 88 subjects, 176 hard links (`h00..h87`), train/val/test (`64/8/16`) exact order match to sanitized `split.json`, 0 r1 files modified after cut, 0 link conflicts.
   - Test denominators on 16 test subjects match r1 exactly (`max_rel_diff = 0.0`); 201-step anchors (`hcp_E_s0`, `hcp_C_s0`, `Fplus_E_s0`) at the r1 8,750-step schedule reproduce r1 loss lines at steps 100 and 200 bit-identically (`max_abs_loss_diff = 0.0`).
3. **4× F+ measurement-capacity gate (`Slurm job 509`, tasks `509_0..2`, 5.07 GPU-h, `results/topic2/2026-11-02_fu_b/gate_4x.json`).**
   - Seed 0, 35,000 steps × batch 16 on synthetic F+ stream: test NMSE `E = 0.65510` (`0.655099`), `C = 0.63069` (`0.630692`), `S = 0.65491` (`0.654914`).
   - Relative gains: C vs E = **+3.73 %** (`+3.726 %`), C vs S = **+3.70 %** (`+3.699 %`), both ≥ δ = `1.00 %` → **`state: "pass"`**.
   - Inherited 1× F− bias gate (`fminus_inherited` from sha-pinned r1 `verdict.json`): `sha_ok = true`, `pass = true`.
4. **Stage-1 4× budget HCP experiment (`Slurm job 516`, tasks `516_0..14`, 25.44 GPU-h, `verdict.json`).**
   - All 15 runs (`hcp_{E,C,S}_s{0..4}_a1`) completed on attempt 1 and passed all validity checks (`missing: []`, `errors: []`, `order_ok: true`).
   - Per-seed test NMSE (16 test subjects × 60 windows, eval seed 7002):
     - Seed 0: `E = 1.00000`, `C = 0.99416`, `S = 0.98601` (`I1 = +0.58 %`, `I2 = −0.83 %`; `E_s0` stalled)
     - Seed 1: `E = 0.98507`, `C = 0.98559`, `S = 0.98558` (`I1 = −0.05 %`, `I2 = −0.00 %`)
     - Seed 2: `E = 0.98555`, `C = 0.98611`, `S = 0.99000` (`I1 = −0.06 %`, `I2 = +0.39 %`)
     - Seed 3: `E = 0.98508`, `C = 0.98590`, `S = 0.98571` (`I1 = −0.08 %`, `I2 = −0.02 %`)
     - Seed 4: `E = 0.98486`, `C = 0.98560`, `S = 0.98551` (`I1 = −0.08 %`, `I2 = −0.01 %`)
     - 5-seed mean: `E = 0.98811`, `C = 0.98747`, `S = 0.98656` (`E − C = +0.00064`, `S − C = −0.00091`).
   - Primary 95 % t intervals (df = 4):
     - **I1 (C vs E): +0.06 % [−0.30 %, +0.42 %]** (`+0.063 % [−0.299 %, +0.425 %]`, SE `0.130 %`).
     - **I2 (C vs S): −0.09 % [−0.65 %, +0.46 %]** (`−0.092 % [−0.646 %, +0.461 %]`, SE `0.199 %`).
   - Secondary hierarchical bootstrap (B = 10,000, seed 0):
     - **I1:** `[−0.08 %, +0.34 %]` (`[−0.078 %, +0.338 %]`, median `+0.060 %`).
     - **I2:** `[−0.50 %, +0.23 %]` (`[−0.496 %, +0.228 %]`, median `−0.087 %`).
   - Stalls and sensitivity (`stall_flags`, `stall_sensitivity`): 1/15 runs stalled (`E_s0`). Dropping seed 0 (`seeds_kept = [1, 2, 3, 4]`, df = 3) gives **I1 = −0.07 % [−0.09 %, −0.04 %]** (`−0.067 % [−0.091 %, −0.043 %]`) and **I2 = +0.09 % [−0.23 %, +0.41 %]**, `verdict_if_governing = "stop"`.
   - Paired comparison with r1 (`r1_pairing`): `same_test_order_as_r1 = true`; manipulation check `E_seed_mean_r1 = 0.98892` → `E_seed_mean_fub = 0.98811` (`E_improved = true`); 4× budget lowered test NMSE on **13 of 15** `(arm, seed)` pairs (all 12 pairs on seeds 1–4 across arms E/C/S plus `S_s0`; only `E_s0` `+0.00913` and `C_s0` `+0.00562` were higher due to seed-0 plateau retention under the 1,750-step warmup). `delta_I1_by_seed` is `[+0.35 %, −0.12 %, −0.46 %, −0.05 %, −0.14 %]`.
5. **Compute and governance.**
   - Total FU-B GPU-h: **30.72 GPU-h** ≤ 33.0 GPU-h cap (explorers `0.14` + smoke `0.07` + gate `5.07` + Stage 1 `25.44`). All 18 tasks in `results/topic2/2026-11-02_fu_b/slurm/jobs.json` are closed in `results/gpu_ledger_2026-10-31.md`.
   - B300 C4 scan (`results/topic2/2026-11-02_fu_b/b300/c4_scan_b300.json`): 176 manifest tokens in memory, 108 text files scanned, **`n_hits = 0`, `n_files_with_hits = 0`**.
   - Test suites: `tests/topic2_fu_b` (128) + `tests/topic2_rgpool` (116) = **244 passed**; `test_empirical_four_topics.py` + `test_pilot_connectome.py` + `tests/e2e` = **86 passed**; mutation suite = **44/44 mutants killed** (`verification/worker_FU_B_r1/mutation/mutants_v2.out.json`); `PROTECTED_HASHES.txt` = **67/67 OK**.

---

## 2. Logic Chain

1. To test whether the r1 null (`stop` at 140k samples) was caused by under-training, FU-B scaled the training budget 4× to 560k samples (`35,000 × 16`) while holding the architecture (`E36_d2262`), target (2 mm voxel z-scored BOLD), partitions, split, data order, masks, and optimizer recipe fixed.
2. Because arm E's dense `Linear(8C→2C)` merge could in principle catch up to arm C on a planted grouping signal given 4× more samples, a new 4× F+ measurement-capacity gate (`job 509`, seed 0) was required before Stage 1 could govern. The 4× F+ gate passed with `+3.73 %` (C vs E) and `+3.70 %` (C vs S), larger than r1's 1× gains (`+3.06 %` and `+2.93 %`), proving that 4× training strengthens rather than erodes sensitivity to a true cell-level grouping signal.
3. On real HCP-YA data (`job 516`), 4× training improved reconstruction on 13 of 15 `(arm, seed)` pairs and passed the arm-E manipulation check (`E_improved = true`).
4. However, once arms E and S escaped the trivial plateau on seeds 1–4, arm E consistently achieved slightly lower test NMSE than arm C (`I1` between `−0.05 %` and `−0.08 %` on all 4 non-stalled seeds). Only on seed 0—where `E_s0` stalled at `1.00000` and `C_s0` escaped late to `0.99416`—was `I1` positive (`+0.58 %`).
5. Consequently, the primary 5-seed 95 % t interval for `I1` is `[−0.30 %, +0.42 %]` (df = 4). Because its upper bound (`+0.425 %`) is strictly below `δ = 1.00 %`, precedence rule 4 yields **`stop` (killed)**—and the non-governing stall-free sensitivity analysis (`[−0.09 %, −0.04 %]`, df = 3) concurs.

---

## 3. Caveats

- **Un-retuned learning-rate schedule (card §2, §13):** Stretching the 5 % linear warmup from 438 steps (r1) to 1,750 steps (FU-B) kept the recipe identical except for `steps = 35000`, but caused `E_s0` to remain trapped on the trivial plateau (`1.00000`) and `C_s0` to escape only after step 26,250 (`0.99416` vs `0.98855` in r1). Thus on 2 of 15 `(arm, seed)` pairs (`E_s0`, `C_s0`), FU-B had higher test NMSE than r1, even though 13 of 15 pairs and the 5-seed arm-E mean improved.
- **Single-seed 4× F+ gate and inherited 1× F− gate (card §7):** Chosen to fit within the 33.0 GPU-h budget (`30.72 GPU-h` used). Because the verdict is `stop`, the inherited 1× F− gate does not affect the outcome.
- **Scope and target noise (card §13):** Five seeds (`df = 4`), 64 training subjects (≈ 73.5 passes at 560k samples), one model scale (`E36_d2262`), and the high-noise 2 mm voxel target (where models explain ~1.0–1.5 % of masked voxel variance).
- **Administrative hold and session resume:** Tasks `516_[12-14]` were held by root (`JobHeldAdmin`) from `2026-11-01T22:52:35Z` to `23:57Z` under the B300-share rule while `g3t-G-E0` jobs ran on `b300-04`, and the worker session was resumed after an API rate limit at `2026-11-02T01:55:36Z`. Neither event affected any training task (`516_12..14` completed normally by `02:08:39Z`).
- **Diagnostic regex note:** `scripts/topic2fu_b_slurm.py sync` reports `standalone_16hex_strings: 7448` because its unquoted regex `[0-9a-f]{16}` matches 16-digit decimal fractional parts of floats in `train_log.jsonl` and `run.json`. Both `c4_scan_b300.json` (`n_hits: 0`) and `test_outputs_no_ids.py` confirm zero identifier or content-hash leaks.

---

## 4. Conclusion

Milestone FU_B is delivered and verified under its frozen card (`2026-11-02_topic2_fu_b_card.md` + `addendum_01.md`):
- **Verdict:** **`stop` (killed)** (`I1 = +0.06 % [−0.30 %, +0.42 %] < δ = 1.00 %`; non-stalled sensitivity `I1 = −0.07 % [−0.09 %, −0.04 %]`).
- **Scientific takeaway:** Increasing the SwiFT ver11 E36 training budget 4× from 140k to 560k samples improves both synthetic F+ capacity (`+3.73 %` C vs E) and real-data baseline reconstruction (`E_improved = true`, 13/15 pairs lower NMSE), and eliminates the small 1× plateau-escape advantage of connectome boxes over PatchMergingV2 on non-stalled seeds. The r1 null is not explained by under-training up to 560k samples.

---

## 5. Verification Method

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_b/card_sha256_v2.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_b/output_sha256.txt
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_b_verdict.py results/topic2/2026-11-02_fu_b/b300/runs /tmp/fub_verdict_check.json
cmp -s results/topic2/2026-11-02_fu_b/verdict.json /tmp/fub_verdict_check.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_b tests/topic2_rgpool -q
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
```
