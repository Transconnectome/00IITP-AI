# Topic 3 addendum — deviations from the frozen card (2026-10-31)

Frozen card: `2026-10-31_topic3_analysis_card.md`, sha256 683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0, frozen 2026-10-31T08:48:29Z (`results/topic3/2026-10-31/card_sha256.txt`). The card file has not been edited since. `topic3_subject_level.py` and `topic3_token_stats.py` verify this hash before reading real data. The connectome job was gated by `verify_card()` in `topic3_launch_connectome.py submit`.

| # | Card section | Deviation | Reason | Effect on estimands / verdicts |
|---|---|---|---|---|
| 1 | §9 step 2 (node1) | Token job ran on **node2**, not node1. The array concurrency went from `%2` to `%1`. Code and output directories were staged onto node2's local home through `srun` stdin. | sbatch refused node1 with "node1, node3 are for GPU jobs. CPU-only -> node2, node4". node4 has no numpy, and home directories are node-local. | None. The job script, the package and the analysis are unchanged; only the host placement changed. The job JSON (`token_job/*_token_job.json`) records python 3.8.10 and numpy 1.22.3 on host node2. These are the same versions under which the synthetic compatibility check ran, but that check ran on node1, the login host (`verification/worker_M2_r1/py38_compat_connectome.out.json`). |
| 2 | §9 (launcher) | `scripts/topic3_launch_connectome.py` changed after freezing. Two changes: the `%` in `--array=0-3%2` was escaped (the first submission crashed with `ValueError: unsupported format character`), and the node2 staging from #1 was added. Its sha256 now differs from `code_sha256_at_freeze.txt`. | Fixes to a launcher bug and to placement. | None. The launcher only ships code and submits the job. It computes nothing. All analysis code is byte-identical to the freeze record, and that can be checked against `code_sha256_at_freeze.txt`. |

No other deviation.

**Failed submission receipts.** Three submit attempts failed before any computation ran. The first was run from the wrong working directory (`can't open file '/home/juke/git/snu-psych-chair/private/dash/scripts/topic3_launch_connectome.py'`). The next two are below. Their error text is quoted verbatim below, copied from the session output.

1. Launcher crash, local, before ssh: `ValueError: unsupported format character '?' (0xa) at index 202`
2. sbatch refusal on connectome: `sbatch: error: FAILED: node1, node3 are for GPU jobs. CPU-only -> node2, node4.` followed by `sbatch: error: Batch job submission failed: Job is no longer pending execution`

`results/topic3/2026-10-31/logs/connectome_submit.log` was overwritten by each retry. It now holds only the final successful submission ("Submitted batch job 217845"). The sbatch refusal was only ever shown on screen and was never saved to a file. Disclosed here per the runtime adapter rule on overwritten receipts.
