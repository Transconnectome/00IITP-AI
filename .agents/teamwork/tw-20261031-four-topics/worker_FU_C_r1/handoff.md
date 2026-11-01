# handoff — worker_FU_C_r1 (FU-C, Topic 2 follow-up C). Hard handoff, 2026-11-01 ~19:55Z

**Summary.** FU-C ran 8 fresh training seeds (10..17) × arms E, C, S at the r1 setting: 24 Slurm runs on B300 b300-01, all completed, no reruns. The card was frozen before any run, and the verdict code was pinned before any run started.
- **Verdict per card: `stop`. The r1 stop is replicated.**
  - I1 = −0.113 % [−0.499 %, +0.272 %] (t, df 7), δ = 1 %. Qualifier: "gain below δ, sign unresolved".
  - I2 = +0.008 % [−0.520 %, +0.537 %].
  - The r1 gate, recomputed from its 12 pinned records, passes.
- 2/24 runs stalled (C s16, S s15). Both count as valid runs; the stall-free sensitivity analysis also gives stop.
- FU-C used 10.684 of its 13 GPU-h cap.

## 1. Observation
- **Card.** `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_card.md`, sha `fc2d0672…4ecb`.
  - Receipt `results/topic2/2026-11-02_fu_c/card_sha256.txt` (`# frozen_utc: 2026-11-01T16:13:23Z`), 0 failures.
  - First submission 16:13:51Z. Verdict code receipt `code_sha256_before_results.txt` at 16:31:53Z. First run start 16:35:12Z (run.json). Copy-back 19:39:46Z.
- **Environment.** `/scratch/iitp4/fu_c/venv`, built from the r1 lock; freeze == lock (sha ae664dc9…, 38/38; `env/env_check.json`).
- **Positional data view.** Hard links; 88/88 positions; the relabelled r1 split equals the sanitized split (`env/datadir_check.json`).
- **Partitions.** `perms_fu_c.npz` sha `f9e32ab7…`. Self-check 25/25: FC sha; E, C, G, R and S0..4 equal r1 by sha and by array.
- **Anchor.** Slurm job 501: 6/6 loss comparisons bitwise equal to r1; no val/test computed (`anchor/anchor.json`).
- **Stage 1.** Slurm jobs 512–515, 517–520, 526–528, plus 13 rolling jobs. All 25 jobs COMPLETED, and 24/24 run.json have `status: completed`. Wall time 1,546–1,562 s; at most 7 concurrent runs. Ledger: 25 started rows and 25 closing rows (agent worker_FU_C_r1).
- **Verdict.** `scripts/topic2fu_c_verdict.py` → `results/topic2/2026-11-02_fu_c/verdict.json` (sha 4d793102…):

  ```
  "verdict": "stop", "qualifier": "stop; gain below delta, sign unresolved (interval contains 0)",
  "replication_reading": "r1 stop replicated on 8 independent training seeds"
  ```

  - Gate: F+ gains +3.06 % / +2.93 % (pass); F− gain −1.74 % (pass).
- **Secondary (descriptive).**
  - Bootstrap: I1 [−0.450 %, +0.143 %].
  - Stall table: E 0, C 1, S 1.
  - Drop-stalled sensitivity (seeds 15 and 16 removed, df 5): I1 +0.040 % [−0.213 %, +0.293 %], I2 +0.022 % [−0.091 %, +0.135 %], stop.
  - Pooled 13 seeds (includes seen data): I1 −0.013 % [−0.248 %, +0.222 %].
- **C4 scan.** B300 scan of the 72 copied files: 0 hits (`c4_scan_b300.json`). Scanner controls: positive 2/2 detected, negative 0.
- **Tests.**
  - `tests/topic2_fu_c`: 109 passed.
  - Old 86 (STRICT_E2E): 86 passed.
  - `tests/topic2_rgpool`: 116 passed (read-only regression).
  - flake8 (max line length 120) clean.
- **Mutants.** `verification/worker_FU_C_r1/mutants/mutants_r2.out.json`: 51/54 killed; 3 equivalent (V07c, V12, F11; reasons in the report §3).
- **Integrity.**
  - C1 rc 0.
  - `code_sha256_at_freeze` 0 failures; `c4_sanitized` 0; `output_sha256_r2` 0.
  - FU-C card, code, presentation and output receipts: 0 failures each.
  - Whole-run `audit_layout`: 0 findings.

## 2. Logic chain
1. **Seeds.** Training is bitwise deterministic per seed (anchor), so r1 seeds 0..4 would duplicate r1. explorer_FU_C_r1_1 had trained seed 5 for 300 steps. The card therefore uses 10..17, which had never been trained. The 13-seed pool is descriptive only.
2. **Gate reuse.** The gate is reused by reference, with sha-verified records. The justification: identical frozen code (16/16 pins), lock-identical env, and a bitwise anchor. A rerun (≈5.2 GPU-h) does not fit the cap.
3. **Fail-closed verdict layer.** The frozen r1 wrapper is not used. The new layer covers the r1 defect classes (V01–V12) with tests and mutants.
4. **Verdict.** All provenance checks pass and I1 hi = +0.272 % < δ, so the result is stop per card §5. Stalls are valid runs (§6), and the sensitivity analysis agrees.

## 3. Caveats
- **Precision.** The I1 interval did not narrow as predicted: half-width 0.386 % against a predicted ≈ 0.144 %. The C-arm stall (s16) dominates the spread.
- **I2.** The r1 I2 > 0 is not replicated; this is descriptive, and I2 is confounded with compactness.
- **Data scope.** The test subjects and masks are the same as in r1. The gate was not rerun. Determinism was checked only to step 200.
- **B300 state.**
  - `/scratch/iitp4/fu_c`: du 135 G. This is mostly hard links shared with `worker_M3_r1`; the venv and 24 checkpoints are about 9 G.
  - The leftover `/scratch/iitp4/explorer_FU_C_r1_2` is not mine.
- **Ledger.** Closing rows have short purpose text (addendum 01 §2.5).

## 4. Conclusion
FU-C (F1–F3) is complete. The verdict is stop, so the r1 stop is replicated on independent seeds. FU-C adds two things beyond r1:
- the practical gain is excluded at δ on 8 new seeds;
- the "positive but sub-δ" hint and the I2 > 0 contrast from r1 do not reproduce.

The r1 verdict is unchanged.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256 code_sha256_before_results code_sha256_presentation_before_results output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_c/$f.txt | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_verdict.py --out /tmp/v.json   # must reproduce verdict.json numbers
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/worker_FU_C_r1/mutants/run_mutants.py $PWD /tmp/mutwork /tmp/mut.json
grep worker_FU_C_r1 results/gpu_ledger_2026-10-31.md | wc -l    # 50 rows (25 started + 25 closing)
```

These results are invalidated by any of the following:
- a change to any governing file pinned in `card_sha256.txt`;
- a run start earlier than the freeze;
- a non-h token in `runs/*/run.json`.
