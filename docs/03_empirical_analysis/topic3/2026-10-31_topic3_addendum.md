# Topic 3 addendum — deviations from the frozen card (2026-10-31)

Frozen card: `2026-10-31_topic3_analysis_card.md`, sha256 683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0, frozen 2026-10-31T08:48:29Z (`results/topic3/2026-10-31/card_sha256.txt`). The card file has not been edited since; every run script verified this hash before touching real data.

| # | Card section | Deviation | Reason | Effect on estimands / verdicts |
|---|---|---|---|---|
| 1 | §9 step 2 (node1) | Token job ran on **node2**, not node1. The array concurrency went from `%2` to `%1`. Code and output directories were staged onto node2's local home through `srun` stdin. | sbatch refused node1 with "node1, node3 are for GPU jobs. CPU-only -> node2, node4". node4 has no numpy, and home directories are node-local. | None. The job script, the package and the analysis are unchanged; only the host placement changed. node2 runs python 3.8.10 with numpy 1.22.3, the same versions as the synthetic compatibility check (`verification/worker_M2_r1/py38_compat_connectome.out.json`). |
| 2 | §9 (launcher) | `scripts/topic3_launch_connectome.py` changed after freezing. Two changes: the `%` in `--array=0-3%2` was escaped (the first submission crashed with `ValueError: unsupported format character`), and the node2 staging from #1 was added. Its sha256 now differs from `code_sha256_at_freeze.txt`. | Fixes to a launcher bug and to placement. | None. The launcher only ships code and submits the job. It computes nothing. All analysis code is byte-identical to the freeze record, and that can be checked against `code_sha256_at_freeze.txt`. |

No other deviation. Both failed submission attempts are kept in the logs: the format error, and the sbatch refusal shown in the session as `sbatch: error: FAILED: node1, node3 are for GPU jobs`. Neither ran any computation.
