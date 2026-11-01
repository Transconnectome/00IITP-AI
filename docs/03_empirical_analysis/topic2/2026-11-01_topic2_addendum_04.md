# Topic 2 card — addendum 04 (2026-11-01, written ~05:20Z, AFTER all Stage-1 results)

Everything below is post hoc. It does not change the card verdict, which is `stop` (see `results/topic2/2026-11-01/verdict.json`).

## 1. One Stage-1 run stayed at the trivial solution

`hcp_S_s2` (arm S, seed 2) behaved as follows:
- Training loss stayed between 0.9997 and 1.0018 for all 8,750 steps.
- Val NMSE was 1.0003, 1.0001, 1.0000 and 1.0000 at the four checkpoints.
- Test NMSE was 1.0000014.

The model never left the "predict ≈ 0" solution. Every other Stage-1 run, all 14 of them, left it by step 4375 at the latest.

Card §5 counts only a timeout, a non-finite loss or a crash as a software failure. This run had none of those and finished with status `completed`, so it **counts as a valid run and is not rerun**. Rerunning it, or dropping it from the primary analysis, would have been an unregistered, result-dependent change.

## 2. Effect on the two claims (post hoc sensitivity)

`verification/worker_M3_r1/posthoc_sensitivity_seed2.py` recomputes the contrasts with seed 2 dropped; output in `results/topic2/2026-11-01/posthoc_sensitivity_without_seed2.json`.

| contrast | all 5 seeds (governed) | without seed 2 (post hoc, df 3) |
|---|---|---|
| I1 (C vs E) | +0.15 % [−0.07 %, +0.36 %] | +0.08 % [−0.10 %, +0.26 %] |
| I2 (C vs S) | +0.47 % [+0.001 %, +0.95 %] | +0.31 % [+0.16 %, +0.45 %] |
| card verdict rule | stop | stop |

**Reading.**
- The practical claim is excluded at δ = 1 % either way.
- The connectome-specific contrast is positive either way. With all 5 seeds its governed lower bound is only just above 0, because the stalled S run inflates the spread.
- No conclusion here rests on the stalled run.

## 3. No other deviation

- All 27 governed runs completed under the frozen code. Each `run.json` records the `code_sha256` of every module, and these equal `results/topic2/2026-11-01/code_sha256_at_freeze.txt`.
- No run was rerun or excluded.
