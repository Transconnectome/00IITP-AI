# handoff — worker_FU_A_r1 (FU-A, Topic 2 follow-up A) — HARD handoff, 2026-11-01T16:55Z

## 1. Observation

**Card.** `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md` is FROZEN.
- sha256 `72be3e83c43f17990d6ed4ab8e2f254894c083f697dfe18557866866623618fb`, frozen at 2026-11-01T16:06:01Z.
- Receipts: `results/topic2/2026-11-02_fu_a/card_sha256.txt` (8 lines), `code_sha256_at_freeze.txt` (21 files), `freeze_time.json`.
- The first FU-A run started at 16:12:33Z.

**Target.** y = κ · (mean of the r1 per-voxel z-scored BOLD over the subject's brain voxels in each 6³ cell), broadcast to those voxels.
- κ = 5.699892, a single global value from TRAIN (Q 0.030780).
- y is both input and target. Everything else is the frozen r1 `train.run`, unchanged.

**TRAIN design statistics** (Slurm job 492, CPU; `design_stats_train.json` sha `694c31ca…`, equal to the B300 original):
- NF 0.20851, which gives fixture voxel noise σ_v 6.545925.
- A post-freeze rerun with the frozen script gave identical values.

**Fixtures** (CPU, synthetic, built locally before the freeze):
- κ_fix 0.970840; F+ C purity 1.00.
- Stage-0 tests at σ_v pass 4/4: F+ r C 0.338 vs E 0.071 / G 0.059; F− C 0.416 ≤ E 0.486, G 0.421; NULL; premise.

**Gate** (Slurm job 507, b300-01, gpu partition, 2 × 1 GPU, 16:12:31–16:37:11Z, sacct 1480 s and 1479 s):
- Fplus_E_s0 test NMSE 0.774678; Fplus_C_s0 0.770409; gain +0.551 % < δ 1 %, so **F+ FAIL**.
- `scripts/topic2fu_a_verdict.py` gives `inconclusive`, reason "measurement-capacity gate failed (F+ fixture gain C vs E < delta)" (`results/topic2/2026-11-02_fu_a/verdict.json`).
- Stage 1 (HCP) was not run, per card §7.3.

**GPU.** worker 0.822 GPU-h + FU-A explorer smokes 0.130 = 0.952 of the 8 GPU-h cap. The ledger has start and closing rows.

**C4.**
- The B300 count-only scan held 1,172 names in memory (88 r1 tokens and 1,084 HCP directory names) and found 0 hits in 14 files.
- Copy-back: 14 of 14 files byte-identical.
- `tests/topic2_fu_a/test_receipts_and_c4.py` passes on every FU-A output.

**Tests.**
- `tests/topic2_fu_a`: 69 passed, 1 skipped (the Stage-1 scan, because no Stage 1 ran).
- Old suite: 86 passed (the dispatch command).
- C1: rc 0, 67/67 OK.
- r1 `code_sha256_at_freeze.txt` 33/33; `output_sha256_r2.txt`, `c4_sanitized_sha256.txt` and `addendum_06_sha256.txt` all pass. The failing lines of the old r1 pins (card 2, output 16, sealed 19) are expected, per addendum 05.
- Verdict mutation: 31 of 31 killed, control passes (`verification/worker_FU_A_r1/mutation/results.json`).
- flake8 (120 columns) is clean.

**Cross-team observation, not mine to fix.** `tests/topic2_rgpool/test_outputs_no_ids.py` now fails: it scans all of `docs/03_empirical_analysis/topic2/`, and FU-B's `2026-11-02_topic2_fu_b_card.md` contains a "sub-o…" word that matches its BIDS regex. The FU-A docs pass the same regexes.

## 2. Logic Chain

1. The explorers' must-fix list (the cost conflict, C4 tokens, no smoothing, calibrated fixtures, full-budget gates, the verdict defect classes, M, stall, disclosure) shaped the card.
2. The 8 GPU-h cap together with the measured 0.42–0.45 GPU-h per run allows 17 runs at most. So the gate is F+ E/C seed 0 (declared deviation), and keep/modify are made unreachable without the unfunded gates.
3. Fixture noise was calibrated to the TRAIN noise share before freezing. Stage-0 shows the planted structure is recoverable at that noise level.
4. The frozen gate rule (gain ≥ δ) was applied to the completed runs: 0.551 % < 1 %. Verdict step 2 makes this `inconclusive` whatever Stage 1 would show, and card §7.3 says Stage 1 is not run.
5. The verdict code has no override, and 31 of 31 mutants were killed, so the label is the frozen rule's, not a judgement call.
6. Scope: no HCP outcome exists, so the r1 stop is unchanged. FU-A adds that the r1-style gate's sensitivity does not transfer to realistic noise.

## 3. Caveats

- The gate used a single seed, a deviation declared in the card. r1's seed spread was about ±0.3 %, so a second seed is unlikely to reach δ, but this is not tested.
- The noise calibration assumes independent unit-variance voxel noise. The realized fixture noise share is 0.248, against 0.209 targeted, because the fixture signal variance came out at 0.80. Both make the fixture slightly harsher than the calibration target.
- The fixture planted-signal strength is inherited from r1; a stronger planting would pass more easily, but would answer a less realistic question.
- The F+ S arm and the F− gate were not run, by design.
- B300 ssh had banner-exchange timeouts from about 15:40 to 16:03Z. This only affected where the synthetic fixture build ran (locally instead of on B300).
- B300 `/scratch/iitp4/fu_a` (venv, frozen code, positional symlink view, gate runs, logs) is kept for verifiers. It can be wiped on VM stop; everything needed is in the repo.

## 4. Conclusion

FU-A is complete under its frozen card, with verdict **`inconclusive` (measurement capacity)**. At E36 and 140k samples, on the 12 mm cell-mean target with HCP-calibrated noise, a planted connectome signal gives only a +0.55 % NMSE gain (r1's near-noise-free gate gave +3.06 %), below δ = 1 %. HCP Stage 1 was correctly not run.

The r1 `stop` stays as recorded. Its practical reading should note that measurement capacity at real noise levels was not established.

A costed plan for the next steps is in result report §9: replicate the gate on seed 1 (0.84 GPU-h); 4× budget (3.4 + 25.5); E192 (2.5–2.7 + 18–20). Each needs a new card and a PI decision; about 7.0 GPU-h of the FU-A cap remain.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_a/card_sha256.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_a/code_sha256_at_freeze.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-02_fu_a/output_sha256.txt | LC_ALL=C sha256sum -c
cat results/topic2/2026-11-02_fu_a/freeze_time.json; grep start_utc results/topic2/2026-11-02_fu_a/runs/*/run.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_a -q
/home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs /tmp/v.json
/home/juke/superclaude-env/bin/python3 -B verification/worker_FU_A_r1/mutation/run_mutants.py
grep worker_FU_A_r1 results/gpu_ledger_2026-10-31.md
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
```

The verdict is invalidated if any receipt fails, if a run's `start_utc` precedes `card_frozen_utc`, if `fua_checks` shows a non-zero within-cell spread, or if the verdict script returns something other than `inconclusive` on the copied records.
