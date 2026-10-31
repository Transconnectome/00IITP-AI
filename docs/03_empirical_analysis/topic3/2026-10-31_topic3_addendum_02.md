# Topic 3 addendum 02: zoo-checkpoint architecture and safe reproduction (2026-10-31)

Written 2026-10-31 at about 11:20Z by worker_M2_r1, after a workflow resume. It is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), addendum 01, the provenance note and the result report are unchanged. All four stay pinned in `results/topic3/2026-10-31/output_sha256.txt`. The sha256 of this file is in `results/topic3/2026-10-31/addendum_02_sha256.txt`.

No verdict changes. Nothing below is a deviation from the card. Item 1 limits how the H1a verdict may be read. Item 2 replaces the reproduction instructions.

## 1. The replication checkpoints are not architecture-matched

**Source.** The MODEL ZOO table in `VRABES/RemissionAnalysis/extract_vrabes_swift_zoo.sh` (variant lines 48 and 54–55) and the primary's extraction script `VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` (checkpoint line 35, model arguments line 82). The deep checkpoints' directory names contain `D2_2_42_4`, which agrees with the table. I did not see the NERSC training or extraction logs, so these attributions come from the scripts only.

| Checkpoint | Training family | Depth | Stage-3 blocks | File | LR | H1a mean log ratio | H1b mean log ratio |
|---|---|---|---|---|---|---|---|
| E192 primary | NewUAH | `2 2 18 2` | 2 | best.pt | 1e-4 | +0.023 | +0.045 |
| zoo HCP_N400_T2400_E192 | HCP | `2 2 18 2` | 2 | last.pt | 2e-5 | −0.137 | −0.113 |
| zoo NewUAH_deepE192_L1e-4 | NewUAH | `2 2 42 4` | 4 | EP10.pt | 1e-4 | +0.038 | −0.033 |
| zoo NewUAH_deepE192_L5e-5 | NewUAH | `2 2 42 4` | 4 | best.pt | 5e-5 | +0.049 | +0.079 |

The effect values are copied from `results/topic3/2026-10-31/family_B_token_level.json`, as reported in result report §3. None were recomputed here.

**Consequences.**
- **The H1a verdict "holds" still stands under card §5 as written.** The rule asks for ≥ 2 of the 3 zoo checkpoints with the primary's sign and Holm p < 0.05, and 2 of 3 meet it. The card did not require matched architecture. Changing the verdict now, after the results are known, would be post hoc.
- **How to read it.** The 2 agreeing checkpoints are deeper models (`2 2 42 4`) from the primary's own training family. The only checkpoint with the primary's depth (HCP_N400_T2400_E192, `2 2 18 2`) reverses H1a, and its effect is the largest of the four. It also reverses H1b. So H1a was replicated across depth and learning rate within one training family. It was **not** replicated at matched architecture: n = 1 matched checkpoint, and that one goes the other way. Training data (HCP vs NewUAH) and depth are confounded across the zoo, so the reversal cannot be assigned to either.
- **Scope of "2 stage-3 blocks".** The result report says "the 2 stage-3 blocks" (§2 after the A1b table; §3 replication rule) and "layer_3 is 2 Swin blocks plus the final LayerNorm" (§4, R2 row). The provenance note says the same. That count is true for the primary and HCP_N400 only. In the 2 deep checkpoints, stage 3 has 4 blocks. The structural point still holds for all four: ver11 has no PatchMerging between `layer_2` and `layer_3`, and both are 1536-d on the same token grid.
- **A1b is unaffected.** The LN-matched subject-level drop (pooled L3 vs pooled LN0(L2)) is negative in all 4 checkpoints, at both depths and in both families (result report §2).
- **Primary training data.** Whether the primary checkpoint was initialised from HCP pretraining is ambiguous: `VRABES/RemissionAnalysis/EXPERIMENT_LOG_E192_ROI.md:22` calls the NewUAH checkpoint "HCP 사전학습". This item does not resolve it.

## 2. Safe reproduction (replaces result report §6 and the 09:08Z worker handoff §5)

`scripts/topic3_common.py:12` hard-codes the output folder as `results/topic3/2026-10-31`. Rerunning any `scripts/topic3_*.py` from the project root therefore overwrites the frozen outputs. The result values reproduce, because all seeds are fixed. But the run records contain `started_utc` and `runtime_s`, so the file hashes change and `output_sha256.txt` fails.

Do not edit `scripts/topic3_common.py` to add an output argument. It is pinned in `code_sha256_at_freeze.txt`.

To reproduce:
1. Copy the tree (`src/`, `scripts/`, `tests/`, `docs/03_empirical_analysis/topic3/`, `results/topic3/2026-10-31/`) to a temporary directory.
2. Run the scripts there.
3. Compare JSON values, not file hashes, with the frozen outputs.

The read-only checks can run in place:
```
cd /home/juke/git/00IITP-AI
sha256sum -c results/topic3/2026-10-31/output_sha256.txt
sha256sum -c results/topic3/2026-10-31/code_sha256_at_freeze.txt   # only scripts/topic3_launch_connectome.py differs (addendum 01, item 2)
sha256sum -c results/topic3/2026-10-31/addendum_02_sha256.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_spectral -q
```

`verification/worker_M2_r1/mutants.py` writes `mutants.out.json` into its own folder. To rerun it without overwriting the original receipt, copy it to your own `verification/<id>/` folder, point its output path there, and run the copy.

## 3. Compute and data governance

- M2 used 0 GPU-hours.
- Nothing was sent to B300.
- VRABES frames stayed on connectome. Only position-keyed summaries were copied back.
- The run's GPU ledger (`results/gpu_ledger_2026-10-31.md`) does not exist yet and is not an M2 path. The 0 GPU-h figure is reported to the root coordinator instead.

## 4. Still open (unchanged)

- H2, the random-init control, is **untested** (card §6).
- The independent review of the M2 deliverable has not run yet. The 09:10Z reviewer, challenger and auditor dispatches left no handoffs.
