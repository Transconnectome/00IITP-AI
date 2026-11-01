# Topic 2 follow-up C (FU-C) result report: 8 fresh training seeds at the r1 setting

Date: 2026-11-02 KST (runs 2026-11-01 16:35–19:38 UTC). Author: worker_FU_C_r1, run tw-20261031-four-topics, workflow C (PI decision 7; r1 result report §7, option C).

**Governing card.** `2026-11-02_topic2_fu_c_card.md`, sha256 `fc2d0672de2bb3163f80b06079ad973c7332cd8b46808bdd59c6456164944ecb`, frozen 2026-11-01T16:13:23Z (`results/topic2/2026-11-02_fu_c/card_sha256.txt`).
- Freeze order: the card was frozen before the first Stage-1 submission (16:13:51Z) and before the first run started (16:35:12Z).
- The verdict code and tests were pinned at 16:31:53Z (`code_sha256_before_results.txt`).
- No Stage-1 number was read before the copy-back at 19:39:46Z.
- Deviations and operational notes are in addendum 01; none changes a governed decision.

**Sources (C8).** Every number below comes from `results/topic2/2026-11-02_fu_c/verdict.json`. The tables are rendered by `scripts/topic2fu_c_report_tables.py`, and the run records are in `runs/hcp_*_a1/`. No number is taken from `EMPIRICAL_ANALYSIS_REPORT.md` or the consolidated status note.

**r1 is unchanged.** The r1 verdict (`stop`; I1 +0.147 % [−0.068 %, +0.361 %], df 4) stays as recorded. FU-C is a new experiment and does not re-read it.

## 0. Verdict

**`stop` (killed) under the FU-C card: the r1 stop is replicated on 8 independent training seeds (10..17).**
- At SwiFT ver11 E36, trained from scratch with SimMIM on HCP-YA REST1_LR (140k samples), M0 connectome boxes do not lower held-out masked NMSE by δ = 1 % or more against PatchMergingV2's cubes.
- I1 = −0.113 %, 95 % t interval [−0.499 %, +0.272 %] (df 7). The upper bound is far below δ. The interval contains 0, so the pre-worded qualifier applies: "stop; gain below δ, sign unresolved".
- The r1 training-loop gate, recomputed from its 12 pinned records, passes (F+ and F−).
- The verdict follows the card in both readings of the stalled runs:
  - including them, as the card requires;
  - in the pre-registered descriptive sensitivity analysis without them.

## 1. Results (rendered from verdict.json)

### 1. Verdict

`stop` — upper 95% bound of I1 < delta: practical gain over PatchMergingV2 excluded (killed)
Qualifier: stop; gain below delta, sign unresolved (interval contains 0).
Reading next to r1: r1 stop replicated on 8 independent training seeds.

### 1. r1 training-loop gate (recomputed from the 12 pinned r1 fixture records)

| fixture | seed-mean NMSE E / C / S | gain C vs E | gain C vs S | pass |
|---|---|---|---|---|
| Fplus | 0.6786 / 0.6578 / 0.6777 | +3.06 % | +2.93 % | True |
| Fminus | 0.2393 / 0.2435 / 0.2437 | -1.74 % | +0.10 % | True |

### 1. Per-seed test NMSE (16 test subjects x 60 windows, fixed masks)

| seed | E | C | S | I1 = (E-C)/E | I2 = (S-C)/S | stalled (E/C/S) |
|---|---|---|---|---|---|---|
| 10 | 0.98742 | 0.98996 | 0.98826 | -0.257 % | -0.172 % | n/n/n |
| 11 | 0.98675 | 0.98682 | 0.98729 | -0.007 % | +0.048 % | n/n/n |
| 12 | 0.98848 | 0.98676 | 0.98825 | +0.174 % | +0.151 % | n/n/n |
| 13 | 0.98672 | 0.98724 | 0.98794 | -0.052 % | +0.072 % | n/n/n |
| 14 | 0.99329 | 0.98889 | 0.98893 | +0.443 % | +0.004 % | n/n/n |
| 15 | 0.98855 | 0.98864 | 1.00000 | -0.010 % | +1.136 % | n/n/y |
| 16 | 0.98877 | 1.00000 | 0.98813 | -1.136 % | -1.202 % | n/y/n |
| 17 | 0.98740 | 0.98799 | 0.98829 | -0.061 % | +0.030 % | n/n/n |
| mean | 0.98842 | 0.98954 | 0.98964 | -0.113 % | +0.008 % | |

### 1. Primary intervals (t, df 7) and secondary bootstrap

| contrast | mean [95 % t interval] | hierarchical bootstrap 95 % | delta |
|---|---|---|---|
| I1 (C vs E) | -0.113 % [-0.499 %, +0.272 %] | [-0.450 %, +0.143 %] | +1.000 % |
| I2 (C vs S) | +0.008 % [-0.520 %, +0.537 %] | [-0.422 %, +0.437 %] | > 0 |

Absolute seed-mean differences: E - C = -0.00112; S - C = +0.00010.

### 1. Stalls (descriptive)

Stall table by arm: {"E": 0, "C": 1, "S": 1}.
Without seeds that have a stalled run (kept [10, 11, 12, 13, 14, 17], df 5): I1 +0.040 % [-0.213 %, +0.293 %]; I2 +0.022 % [-0.091 %, +0.135 %]; rule category stop (descriptive, non-governing).

### 1. Plateau escape vs I1 (descriptive)

| seed | E escape step | C escape step | I1 |
|---|---|---|---|
| 10 | 1500 | 4900 | -0.257 % |
| 11 | 1500 | 1700 | -0.007 % |
| 12 | 1800 | 1700 | +0.174 % |
| 13 | 1300 | 1300 | -0.052 % |
| 14 | 6100 | 2500 | +0.443 % |
| 15 | 1800 | 1700 | -0.010 % |
| 16 | 1800 | None | -1.136 % |
| 17 | 1600 | 1600 | -0.061 % |

### 1. Pooled 13 seeds (r1 0..4 + FU-C; includes already-seen data; never governs)

I1 -0.013 % [-0.248 %, +0.222 %]; I2 +0.187 % [-0.163 %, +0.538 %] (df 12).

## 2. What FU-C adds to the r1 stop

| | r1 (seeds 0..4, df 4) | FU-C (seeds 10..17, df 7) | FU-C without stalled seeds (df 5, descriptive) |
|---|---|---|---|
| I1 mean [95 % t] | +0.147 % [−0.068 %, +0.361 %] | −0.113 % [−0.499 %, +0.272 %] | +0.040 % [−0.213 %, +0.293 %] |
| I2 mean [95 % t] | +0.473 % [+0.001 %, +0.946 %] | +0.008 % [−0.520 %, +0.537 %] | +0.022 % [−0.091 %, +0.135 %] |
| stalled runs | 1/15 (S s2) | 2/24 (C s16, S s15) | — |
| verdict | stop | **stop** (replicated) | stop (descriptive) |

**1. Replication.** The practical claim is excluded again, on seeds that share nothing with r1 except the data, the split and the code. The upper bound is +0.27 %, against δ = 1 %. Every FU-C reading is consistent with no practically relevant effect.
- The governed interval contains 0.
- The stall-free interval is centred near 0.
- The pooled 13-seed interval, I1 −0.013 % [−0.248 %, +0.222 %], is descriptive and includes the already-seen r1 data.

**2. The I1 interval did not narrow.** The card predicted a half-width of about 0.144 % (§12). The observed half-width is 0.386 % (0.253 % without stalled seeds), compared with 0.215 % in r1.
- The cause is the stalls: C s16 never left the predict-zero plateau. That is the C-arm stall the card §12 simulation already listed as a threat to precision.
- Even so, the upper bound stays far below δ. The "positive but sub-δ" gain that the r1 bootstrap hinted at (r1 report §0) is **not** reproduced: the FU-C point estimate is ≤ 0 with stalls and +0.04 % without them.

**3. The surrogate contrast I2 is not replicated.** r1's I2 lower bound was barely above 0 (+0.001 %), and it was +0.31 % [+0.16 %, +0.45 %] without the stalled r1 seed (r1 addendum 04). In FU-C, I2 is +0.008 % [−0.520 %, +0.537 %], and +0.022 % [−0.091 %, +0.135 %] without the stalled seeds.
- At the seed level, FU-C gives no evidence that FC-informed boxes beat the distance-binned FC-shuffle boxes.
- Caveats on reading I2:
  - I2 is confounded with box compactness (card §1). The S dispersions are 1.58–1.65 cells, against C 1.47 (card §3.3).
  - I2 governs only keep versus modify, which the stop verdict makes moot.
  - This is a descriptive observation, not a verdict on the r1 Stage-0 cell-level finding (C − S r > 0), which FU-C did not re-test.

**4. Plateau escape.** As in r1 (addendum 05 item 5), the largest positive I1 comes from the seed whose E run left the plateau last: seed 14, E escape at step 6,100, I1 +0.443 %. The most negative I1 comes from the seed whose C run never left it: seed 16. Per-seed I1 therefore tracks training-dynamics timing more than any stable grouping benefit. This reading is descriptive.

## 3. Implementation (F2) and checks

**New code.** Everything is in FU-C-owned paths; no existing file was edited.
- `src/topic2_fu_c/`:
  - `design.py`: seeds 10..17, δ, df 7, r1 settings and pins.
  - `perms.py`: self-check of the frozen builder's rebuild.
  - `logs.py`: anchor comparison and stall flag.
  - `budget.py`: ledger, cap rule, sacct parsing and sbatch text.
  - `verdict.py`: the fail-closed verdict layer.
  - `receipts.py`: receipt verification and the verdict context.
- `scripts/topic2fu_c_*.py`:
  - `build_env`, `make_datadir`, `build_perms`, `anchor`, `slurm`, `freeze`, `scan_b300`, `copyback`, `verdict`, `report_tables`.

**Reuse of frozen r1 code.**
- The training path is the frozen r1 code, unchanged: 16/16 files equal `code_sha256_at_freeze.txt` on B300.
- The verdict imports only the frozen `stats.t_interval`, `relative_gain`, `hierarchical_bootstrap` and `gate_fixture`. The frozen `scripts/topic2_verdict.py` is not used.

**Tests.** `tests/topic2_fu_c/` has 109 tests. Their inputs are synthetic records with known ground truth: planted effects at 6 points recover the card category, and noise-free planted contrasts are recovered to 1e-12. The defect classes they cover:
- the r1 wrapper oracle rows A–I;
- every rule boundary on both sides;
- F+ failure → inconclusive, with or without Stage 1;
- a missing or non-boolean gate → no_verdict;
- F− failure downgrades keep only;
- failed, duplicate, unexpected and renumbered attempts;
- test-order mismatch → no_verdict (not an exception);
- token shape, partition, code, split, settings and freeze-time provenance;
- df 7, checked against an independent t quantile;
- the stall flag, validated on the real r1 logs (it reproduces r1 addenda 04/05 exactly);
- the cap rule, KST→UTC conversion and the g3t rule;
- receipts, partitions, and C4 on the results dir.

**Mutation testing** (`verification/worker_FU_C_r1/mutants/mutants_r2.out.json`). Of 54 mutants (the baseline survives), **51 are killed**. They cover V01–V14 (including the frozen stats boundaries and the t level and df), F01–F23, and the stall, anchor, budget, partition and receipt checks. The 3 survivors are equivalent on every reachable state:
- V07c (`is not True` → `is False`): the gate flag is always boolean once the evidence verifies.
- V12 (F+ forced True at the final decision): that line is reached only when F+ is True.
- F11 (duplicate check removed): two completed attempts are still rejected as "attempt follows a completed run", and more than 2 attempts as "more than one rerun".

## 4. Compute (C5) and data (C4, C6)

**Placement and scheduling.**
- B300 b300-01, via Slurm only; there were no direct GPU launches.
- 1 anchor job and 24 Stage-1 jobs, each 1 GPU, `-p gpu -w b300-01 -t 00:36:00`.
- All 25 finished COMPLETED, and all 24 records have `status: completed`. There were no reruns.
- Each job was held until its ledger `started` row existed, then released. Each was closed from `sacct` ElapsedRaw.

**FU-C GPU use: 10.684 GPU-h of the 13 GPU-h cap.**
- Explorers: 0.262.
- Anchor: 0.058.
- Stage 1: 10.364 (0.429–0.434 per run).

**B300 sharing rule.** No `g3t-G-E0-*` job was pending or running at any of the 25 submissions. Up to 11 FU-C jobs were queued at once (waves of 8 and 3, then one per closed job, as the cap rule admitted); the shared 8-GPU per-user QoS decided how many ran (at most 7 FU-C runs at once, from sacct start/end).

**Data (C6).** HCP-YA Open Access (PI decision 2), read-only, on b300-01. The data never left B300, and the checkpoints stay on B300.

**C4.**
- The repo holds only positional h-tokens: the data view is positional and the split is the sanitized one.
- The B300 scan of the copy-back tree found 0 hits for HCP names and original tokens.
- Repo-side C4 tests pass.
- No participant ID was printed or written.

## 5. Limitations

- The same 16 test subjects and evaluation masks as r1 were used. FU-C replicates over training seeds, not over subjects.
- The r1 training-loop gate was reused by reference, not rerun. The justification is code pins, lock identity and a bitwise anchor to step 200.
- The stall rate is 2/24 in FU-C and 1/15 in r1. Stalls dominate the seed-level spread at this budget, so a narrower interval would need a stall-free training recipe; that would be a new card.
- FU-C tests nothing beyond the r1 setting: not the target, budget or scale (options A, B, D), and not downstream value (option E).
- I2 is not read as FC specificity.

## 6. Reproduce / verify

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-02_fu_c/card_sha256.txt | LC_ALL=C sha256sum -c                 # card + governing inputs
grep -v '^#' results/topic2/2026-11-02_fu_c/code_sha256_before_results.txt | LC_ALL=C sha256sum -c  # verdict code + tests
grep -v '^#' results/topic2/2026-11-02_fu_c/output_sha256.txt | LC_ALL=C sha256sum -c               # outputs
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES="" PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_verdict.py --out /tmp/fuc_verdict_check.json   # recomputes the verdict
```
