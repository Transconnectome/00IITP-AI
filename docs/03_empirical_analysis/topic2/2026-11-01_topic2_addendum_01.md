# Topic 2 card — addendum 01 (2026-11-01): additions after the freeze

The frozen card is `2026-11-01_topic2_card.md`, sha256 `c9bfc60a…41f5`, frozen at 03:14:34Z. This addendum does not edit it. It records every file that was added or changed after the freeze, and why.

| time (UTC) | file | change | effect on governed computations |
|---|---|---|---|
| ~03:20Z | `scripts/topic2_id_scan.py` | new: C4 leak scan, run on B300 with the HCP directory names held in memory | none: reads copies of the outputs only |
| ~03:20Z | `tests/topic2_rgpool/test_outputs_no_ids.py` | new: local C4 checks of the outputs, plus a check of the B300 scan result | none |
| ~04:22Z | `scripts/topic2_id_scan.py`, `tests/topic2_rgpool/test_outputs_no_ids.py` | scan also records the masked 8 characters after each hit. The adjudication rule (`is_coincidence`: a hit may be dismissed only if it is part of a decimal number or the value of a listed JSON count field) was fixed **before the first B300 scan was run** | none |
| ~03:30Z | `tests/topic2_rgpool/test_token_order.py` (probe: `verification/worker_M3_r1/probe_token_order.py`) | new: confirms that ver11's patch-embedding token order equals the partition's cell index (d·16+h)·16+w on the input's (D,H,W) voxel blocks | none: a read-only check of an assumption the frozen code already makes; it passed with no change |

All code that the governed runs execute was unchanged after the freeze: `src/topic2_rgpool/*`, `scripts/topic2_train.py`, `topic2_build_partitions.py`, `topic2_stage0.py`, `topic2_verdict.py` and `topic2_launch_wave.py`. The hash check `sha256sum -c` against `results/topic2/2026-11-01/code_sha256_at_freeze.txt` must still pass for those files, and the final report includes its output.

Each run also records the sha256 of every module it imported in `run.json` (`code_sha256`).
