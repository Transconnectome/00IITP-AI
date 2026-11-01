# handoff — worker_M3_r1 (M3 / Topic 2) — PARTIAL, interim checkpoint 2026-11-01T03:57Z

Interim checkpoint written while Stage 1 runs on B300. Superseded by the final Hard handoff once the verdict is written.

## Remaining Work (if this agent stops here)
1. Wait for the B300 runs `/scratch/iitp4/worker_M3_r1/runs/{Fminus_*,hcp_*}` (waves 2–4; the job lists are `code/wave{2,3,4}_jobs.json`).
   - Launch each wave with `venv/bin/python -B code/scripts/topic2_launch_wave.py code/waveN_jobs.json runs/waveN --timeout-sec 3300`, run from `/scratch/iitp4/worker_M3_r1`.
   - Write a ledger row before and after each wave with `scripts/topic2_ledger.py`.
2. Copy the runs back, excluding `model_final.pt`:
   `rsync -a --exclude model_final.pt connectome@61.107.201.98:/scratch/iitp4/worker_M3_r1/runs/{F,h}* results/topic2/2026-11-01/runs/`
3. Compute the verdict: `scripts/topic2_verdict.py results/topic2/2026-11-01/runs results/topic2/2026-11-01/verdict.json`.
4. Fill the placeholders in `docs/03_empirical_analysis/topic2/2026-11-01_topic2_result_report.md`.
5. Run the ID scan on B300 with `scripts/topic2_id_scan.py`.
6. Run the final tests, the C1 check and the layout lint.

## State at checkpoint
- The card was frozen at 03:14:34Z (sha `c9bfc60a…41f5`).
- The F+ training-loop gate passed: C vs E +3.07 %, C vs S +2.94 %.
- Stage 0 (descriptive) is done.
- GPU use so far: 0.04 + 3.41 GPU-h, plus wave 2 in progress.
