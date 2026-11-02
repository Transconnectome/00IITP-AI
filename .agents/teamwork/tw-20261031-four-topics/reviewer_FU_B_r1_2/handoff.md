# Handoff Report — reviewer_FU_B_r1_2 (Milestone FU_B_r1 — Post-Fix Re-Verification)

- **Reviewer**: `reviewer_FU_B_r1_2` (Reviewer 2 of 2 for Milestone `FU_B_r1`)
- **Run**: `tw-20261031-four-topics` (Workflow C)
- **Milestone**: `FU_B` (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds (§7 ≈26 GPU-h; cap 33)`)
- **Verdict**: **`APPROVE`** (Blocking issue `[B1]` and Challenger 1's `[NB1]` resolved and verified)

---

## 1. Observation

1. **Resolution of `[B1]` (and `[NB1]`) in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` (sha256 `809c64826a0e0f385be1266d13409480a11bfbb4f0a15539b9da0bd69e779247`)**:
   - In our initial pass, we flagged `[B1]`: 14 of the 15 `final train loss (last 100)` cells in Report §2.3 (`Per-run validation NMSE curves`, lines 97–110) did not match `results/topic2/2026-11-02_fu_b/b300/runs/hcp_*_a1/run.json["train_loss_last100"]`.
   - `worker_FU_B_r1` updated all 14 cells in `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` lines 97–110 (and updated `verification/worker_FU_B_r1/report_numbers.py` to read `run.json["train_loss_last100"]` and r1 `Fplus` reference runs directly), resolved `[NB1]` in Table 1.1 lines 44–45 (`r1 1× F+ (seed 0, ref.)`: `0.67693 / 0.65817 / 0.67783 / +2.77 % / +2.90 %`; `r1 1× F+ (seeds 0–1 mean, ref.)`: `0.67862 / 0.65785 / 0.67774 / +3.06 % / +2.93 %`), refreshed `results/topic2/2026-11-02_fu_b/output_sha256.txt` (sha256 `eb860d47923b28f702a53c6e8fb49478008a2d56afcde384e767f66ff4a0d138`), and archived the pre-revision snapshot under `verification/worker_FU_B_r1/prev_snapshot/`.
   - Re-running `/home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/reviewer_FU_B_r1_2/audit_fu_b.py` confirms **15/15 exact matches (`train_loss_mismatch_count: 0`, `val_and_stall_mismatches: 0`)** in Table 2.3:
     - `hcp_E_s0_a1`: `1.00174` (`1.0017449480295182`)
     - `hcp_E_s1_a1`: `0.97599` (`0.9759852230548859`)
     - `hcp_E_s2_a1`: `0.98167` (`0.9816657078266143`)
     - `hcp_E_s3_a1`: `0.97612` (`0.9761151486635208`)
     - `hcp_E_s4_a1`: `0.97295` (`0.9729466259479522`)
     - `hcp_C_s0_a1`: `0.99702` (`0.9970223551988602`)
     - `hcp_C_s1_a1`: `0.97737` (`0.9773704206943512`)
     - `hcp_C_s2_a1`: `0.98083` (`0.9808264034986496`)
     - `hcp_C_s3_a1`: `0.97580` (`0.9758018970489502`)
     - `hcp_C_s4_a1`: `0.97535` (`0.9753484839200973`)
     - `hcp_S_s0_a1`: `0.97802` (`0.9780160409212112`)
     - `hcp_S_s1_a1`: `0.98260` (`0.9826025176048279`)
     - `hcp_S_s2_a1`: `0.98776` (`0.9877595144510269`)
     - `hcp_S_s3_a1`: `0.97970` (`0.9796951019763946`)
     - `hcp_S_s4_a1`: `0.97796` (`0.9779608297348023`)

2. **All Acceptance Criteria (C1–C8) and Milestone Criteria (F1–F3) Verified**:
   - **F1 (Pre-registration & Freeze)**: `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md` (v2 sha256 `994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae`) and `2026-11-02_topic2_fu_b_addendum_01.md` (`4acafa5b5746d1771d85d8403727d58ff6ecc2d27475f5d5b8ec7534edd80817`) were frozen in `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt` at `2026-11-01T16:20:25Z` (v1 at `16:05:18Z`), before the first gate task `509_0` started at `2026-11-01T16:20:41Z`. All 31 entries in `card_sha256_v2.txt`, all 50 entries in `output_sha256.txt`, and all 29 entries in `results/topic2/2026-11-01/code_sha256_at_freeze.txt` pass `sha256sum -c`.
   - **F2 (Verdict & Record Validation Code)**: `src/topic2_fu_b/{design,records,verdict,budget,slurm,view}.py` and `scripts/topic2fu_b_*.py` implement card §7–§9 rules (`no_verdict` on missing/invalid gate, `inconclusive` on failed gate without reading Stage 1, `no_verdict` on incomplete/invalid Stage 1 or `order_ok == False`, sha-verified `fminus_inherited` literal `True` only downgrading `keep`, and exact boundary operators `hi < delta` for `stop`, `mean >= delta` and `lo > 0` for `keep`/`modify`).
   - **F3 (Execution, Independent Verdict Re-Execution, & Report Provenance)**: Re-running `scripts/topic2fu_b_verdict.py results/topic2/2026-11-02_fu_b/b300/runs verification/reviewer_FU_B_r1_2/verdict_recheck.json` produces byte-for-byte identical output to `results/topic2/2026-11-02_fu_b/verdict.json` (`sha256 = 262b9c793af333af1658f95dfc96de3769c95d3fdddc300dd667813ee5f1e142`), and `verdict.json["fplus_gate_4x"]` equals `gate_4x.json`. Every number across all sections and tables of `2026-11-02_topic2_fu_b_result_report.md` matches the frozen JSON artifacts and ledger.
   - **C1–C8**:
     - C1: `PROTECTED_HASHES.txt` 67/67 OK.
     - C2: `tests/topic2_fu_b` + `tests/topic2_rgpool` (`244 passed`), `STRICT_E2E=1 tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` (`86 passed`), `tests/topic1_lagmotif` (`88 passed`).
     - C4/C6: Zero 6-digit HCP IDs, zero BIDS prefixes, and zero 16-hex content hashes across all 143 scanned FU-B files (`tests/topic2_rgpool/test_outputs_no_ids.py`: `3 passed`). Positional hard-link view `/scratch/iitp4/fu_b/hcp/subjects/hNN/` (`176` links, `88` subjects) and B300 scan (`c4_scan_b300.json`: `108` files, `0` hits) verified.
     - C5: All 22 FU-B Slurm tasks (`413`, `402`, `419`, `490`, `509_0..2`, `516_0..14`) are logged in `results/gpu_ledger_2026-10-31.md` with exact `TZ=UTC sacct` `ElapsedRaw` ceiling rounding to `0.01 GPU-h`, totaling `0.140` (explorers) + `30.580` (worker) = **`30.720 GPU-h` ≤ `33.0 GPU-h` cap**.

---

## 2. Logic Chain

1. All pre-registered card rules (`2026-11-02_topic2_fu_b_card.md` + `addendum_01.md`) were frozen prior to GPU job execution (`card_sha256_v2.txt` 31/31 OK) and are accurately implemented in `src/topic2_fu_b/` and tested by 128 unit tests + 44/44 killed mutants.
2. Independent re-execution of `scripts/topic2fu_b_verdict.py` reproduces `results/topic2/2026-11-02_fu_b/verdict.json` byte-for-byte (`stop` under precedence rule 4: `I1_t` mean `+0.063 %`, 95 % t CI `[−0.299 %, +0.425 %]`, upper bound `< δ = 1.00 %`; 4× `Fplus` gate `pass` with `+3.726 %` C vs E and `+3.699 %` C vs S).
3. Following the worker's fix to `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` (sha256 `809c64826a0e0f385be1266d13409480a11bfbb4f0a15539b9da0bd69e779247`) and `results/topic2/2026-11-02_fu_b/output_sha256.txt` (sha256 `eb860d47923b28f702a53c6e8fb49478008a2d56afcde384e767f66ff4a0d138`), every number and table in the result report matches `verdict.json`, `gate_4x.json`, `b300/runs/*/run.json`, r1 artifacts, and `results/gpu_ledger_2026-10-31.md` with zero discrepancies.
4. Therefore, Milestone `FU_B_r1` satisfies all requirements C1–C8 and F1–F3 and merits **`APPROVE`**.

---

## 3. Caveats

- Scientific scope limitations are transparently documented in card §13 and report §6.2: the optimizer/schedule hyperparameters (`peak_lr = 2e-4`, 5 % warmup = 1,750 steps, cosine decay) were held fixed from r1 rather than re-tuned for 4× (`E_s0` stalled at `1.00000` and `C_s0` escaped late at `0.99416`, though pre-registered seed-0-dropped sensitivity `df = 3` also yields `I1 = −0.067 % [−0.091 %, −0.043 %]` and `stop`), and `fminus_inherited` was inherited from r1 at 1× budget to stay within the 33.0 GPU-h cap (`30.720 GPU-h` used).

---

## 4. Conclusion (`APPROVE`)

- **Verdict**: **`APPROVE`**
- Zero blocking issues and zero non-blocking issues remain.

---

## 5. Verification Method

```bash
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-02_fu_b/card_sha256_v2.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_b/output_sha256.txt | LC_ALL=C sha256sum -c
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 /home/juke/git/00IITP-AI/verification/reviewer_FU_B_r1_2/audit_fu_b.py
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_b tests/topic2_rgpool -q
```
