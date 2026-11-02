# Topic 3 H2 result report: trained E192 vs random initialization of the same network (2026-11-02)

**Governing rule.** `2026-11-02_topic3_addendum_07_h2_card.md`, sha256 `09b45220205bce814c4e07d4494d586b95f63f97dbfcddeb716fafcdc5edd84b`, frozen 2026-11-01T15:57:40Z (`results/topic3/2026-11-02_h2/addendum_07_sha256.txt`, `addendum_07_frozen_utc.txt`). The first random-init forward pass on real frames ran in Slurm job 218064, which started at 2026-11-01T16:32:19Z, 34.6 minutes after the freeze. Every script that touches H2 data verifies this hash and refuses on a mismatch (`scripts/topic3h2_connectome.py submit`, `scripts/topic3h2_stats.py gate|final`). The frozen card of 2026-10-31 and addenda 01–06 are unchanged, and no 2026-10-31 verdict is re-read here.

**Evidence.** Every number below comes from this run's dated outputs in `results/topic3/2026-11-02_h2/`: `gate/gate_record.json` (job record), `gate/gate_decision.json` (local gate decision), `random/random_record.json`, the returned per-arm `*_scalars.npz` / `*_subsets.npz`, and `h2_results.json` (sha256 `356e178e…47e2`). Hashes of all outputs are in `results/topic3/2026-11-02_h2/output_sha256.txt`. Numbers in EMPIRICAL_ANALYSIS_REPORT.md are not cited (C8). The trained values T are the pinned 2026-10-31 outputs.

**Compute.** connectome node1, Slurm `debug`, 1 × RTX A5000 per job, project-local venv (python 3.8.10, torch 2.4.0+cu121, numpy 1.24.4) under `/home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/`.

| Job | What | Elapsed | GPU-h |
|---|---|---|---|
| 218063 | gate: R0 (trained) on all 57 × 7 windows + 3 negative controls | 485 s | 0.135 |
| 218064 | random init R1–R10, one shared read of each window | 1160 s | 0.323 |

Total for this worker: 0.458 GPU-h. With the three explorer smokes (0.058 GPU-h) the M2-H2 total is 0.516 of the 6 GPU-h cap. Both jobs have start and closing rows in `results/gpu_ledger_2026-10-31.md`. Frames, dumps, pooled vectors and eigenvalue spectra stayed on connectome; each job deleted its work directory (`work_dir_deleted: true`). Only position-keyed scalars, per-index-set PRs and aggregates came back, after an ID scan.

**Mode.** PRE-SPECIFIED, not blind (addendum 07 §1). Nobody had computed a random-init statistic on real frames before the freeze (addendum 07 §10).

## 1. Replication gate G (addendum 07 §4): PASS

| Check | Result |
|---|---|
| G1 element-wise, 399 windows × 4 layers | All pass. Maximum rel_fro: L0 6.5e-7, L1 7.4e-7, L2 7.8e-7, L3 7.3e-7 (tolerance 1e-5). Maximum \|Δ\|: 6.7e-6 (tolerance 1e-4) |
| G2 re-pool | The connectome npz copies match their pins and their row order equals the sorted directory order. Maximum \|re-pooled − npz row\|: 2.3e-7 (L0), 2.6e-7, 3.8e-7, 7.0e-7 (L3); allclose 1e-5 holds for all 57 |
| G3 statistics | The largest relative difference between R0's and the pinned T per-subject statistics (cat, frame and H4 sub values, 5 variants) is 7.3e-8 (tolerance 1e-6). Dropped-column counts are equal. H1a and H1b on R0 have the same sign and CI status as on T (R0 mean log ratios 0.0227507 and 0.0446725; T 0.0227507 and 0.0446725). The local recheck of the returned R0 scalars gives the same result |
| G4 identity | Checkpoint sha256 `5fd8a56c…2355` verified in the job. 568 tensors loaded; 17 missing keys, none of them encoder keys; the only unexpected key is `augment_comp.smooth_kernel`. The input and stored-dump subject lists are equal; 57 × 7 windows; TF32 off for both matmul and cuDNN; vendored code hashes verified |
| G5 negative controls, positions 0 / 28 / 56 | Each control fails G1 in all 21 windows and all 4 layers. Smallest rel_fro per control: +1 frame 4.6e-4 (L3); pad value 0 0.42 (L0); no input scaling 1.5 or more |

Not bitwise, as expected (addendum 07 §4): the replication floor is about 7.8e-7 relative, 13 times below the tolerance. The +1-frame shift, the smallest perturbation, is 46 times above it. R0's per-index-set subject-level PRs match T's to a relative 6.4e-7 or better (reported only). T's subject-level L2 − L3 intervals reproduce the pinned Family A values exactly (cov point 5.343854531110546, SE 1.0810551262749508; corr 6.038808669990018, 0.8990825692997121), which shows that the index sets and inputs are identical.

Seed hygiene for R1–R10: rebuilding seed 1 gives a bitwise-identical encoder hash; the 10 seed hashes are distinct and none equals the trained encoder hash (`8240f839…`); the card's index sets generated in the job equal the shipped ones.

## 2. Family C: are the card's layer contrasts produced by training? (primary)

Each row is trained minus the mean of the 10 random-init seeds, on the same subjects (C1, C2) or the same 2000 index sets (C3, C4). δ = 0.5 × the pinned trained effect. The Holm correction for C1 and C2 is over those two. Labels follow addendum 07 §6.

| Id | Card contrast | Trained | Random mean | Difference [95%] | 90% | Holm p | Per-seed range | δ | Label |
|---|---|---|---|---|---|---|---|---|---|
| C1 | H1a, token, log corrPR L3 − LN0(L2) | +0.0228 | +0.0103 | +0.0124 [+0.0104, +0.0145] | [+0.0107, +0.0141] | 0.0002 | +0.0036 … +0.0231 | 0.0114 | **INC** (the interval reaches δ) |
| C2 | H1b, token, log covPR L3 − L2 | +0.0447 | +0.0151 | +0.0295 [+0.0256, +0.0334] | [+0.0262, +0.0328] | 0.0002 | +0.0205 … +0.0497 | 0.0223 | **INC** (two seeds' effects, +0.0205 and +0.0212, are ≤ δ) |
| C3 | D1 cov, subject level, Δ28 covPR L2 − L3 | +5.34 | +0.26 | +5.09 [+2.93, +7.25] | [+3.28, +6.90] | — | +4.93 … +5.29 | 2.67 | **TE+** |
| C4 | D1 corr, subject level, Δ28 corrPR L2 − L3 | +6.04 | +0.25 | +5.79 [+4.01, +7.57] | [+4.29, +7.28] | — | +5.54 … +5.94 | 3.02 | **TE+** |

The Holm p of 0.0002 is the permutation floor, 2/(B + 1) with B = 9999. The L2 / LN0L2 / L3 token-level values carry the ceiling note of addendum 03: the effective token PR ceiling there is 7.

**Reading.**
- **The subject-level L2 → L3 drop is produced by training (C3, C4 TE+).** In the untrained network on the same input, the drop is about 0.25 (cov and corr). In the trained network it is 5.3–6.0. Every seed gives a difference above δ.
- **H1a is about half present at init (C1 INC).** The random-init network already shows the H1a direction: +1.0% on average, which is 45% of the trained +2.3%. Applied to each seed on its own, the card's token rule finds H1a significant and positive in 9 of 10 seeds; seed 4 gives −0.04%, p_holm 0.52. The training-specific part, +1.24%, has a 95% interval of [+1.04%, +1.45%], which straddles δ = 1.14%. The rule therefore leaves its training dependence unresolved.
- **H1b is mostly, but not consistently, training-specific (C2 INC).** The trained H1b of +4.5% is larger than the init mean of +1.5%, and the pooled interval lies above δ. Two seeds (seed 8, init H1b +2.4%, and seed 3, +2.3%) leave a training-specific part of only +2.05% and +2.12%, below δ = 2.23%, so the seed condition fails.

## 3. Family L: per-layer PR levels, trained vs init (δ = log 1.10)

Token level: per-subject log concatenated PR, trained minus the seed mean; Holm over 10. Subject level: log PR over the 2000 index sets of 28 subjects. A ratio is exp(difference).

| Variant | Token cov | Token corr | Subject-level cov | Subject-level corr |
|---|---|---|---|---|
| L0 | ×0.946, INC | ×0.991, INC | ×0.941, INC | ×0.877, INC |
| L1 | ×0.758, **TE−** | ×0.737, **TE−** | ×0.241, **TE−** | ×0.350, **TE−** |
| L2 | ×0.905, INC | ×0.928, **EQ** | ×0.419, **TE−** | ×0.494, **TE−** |
| LN0L2 | ×0.927, INC | ×0.946, **EQ** | ×0.418, **TE−** | ×0.495, **TE−** |
| L3 | ×0.932, **EQ** | ×0.958, **EQ** | ×0.159, **TE−** | ×0.213, **TE−** |

All token-level Holm p values are ≤ 0.015. Every token-level INC comes from the seed condition: at L0 (cov, corr) and LN0L2 cov the 90% interval is inside ±log 1.10 but some seed's effect is not (L0 seed effects range from −0.19 to +0.07 in log units), and at L2 cov the 95% interval is beyond −log 1.10 but one seed's effect (−0.079) is not. The two subject-level INC cells (L0) have intervals that reach ±log 1.10.

**Reading.**
- **Between subjects (pooled vectors), the trained network is much lower-dimensional than the untrained one at L1, L2 and L3** (2–6 times lower PR on the 28-subject subsets). At full n = 57, the untrained network's subject-level covPR is 17.6–20.9 at L1 and 30.9–34.0 at L2 / L3 across the 10 seeds; the trained network's is 2.78, 11.02 and 3.58. At L0 the untrained network is already as low as the trained one (2.6–3.2 vs 2.78): the L0 between-subject PR is set by the input and the patch embedding, not by training.
- **Within a window (tokens), the untrained network already sits near the same ceiling-limited values at L2 / L3.** Its median covPR at L2 / L3 is 5.85–6.22 across seeds, against the trained 5.41 / 5.67. The trained network is within 10% of init for corrPR at L2, LN0L2 and L3 and for covPR at L3. At L1 it is 24–26% lower.

## 4. Secondary (descriptive, no verdict)

- **R1 context (L2 − L1 at subject level).** Trained +4.67 (cov) / +4.39 (corr); untrained seed mean +6.28 / +5.12. Trained minus init: −1.61 [−3.77, +0.56] (cov), −0.74 [−3.18, +1.71] (corr). The between-subject L1 → L2 rise is at least as large in the untrained network.
- **A1b context (L3 − LN0(L2) at subject level).** Trained −5.34 / −6.08; untrained −0.26 / −0.26. The norm-matched subject-level drop through the stage-3 blocks is absent at init, consistent with C3 / C4.
- **The card's D1 rule applied to each random seed.** The covPR drop is small in every seed, with point +0.06 to +0.42. Its interval lower bound is above 0 in 3 seeds (5, 7, 10; lower bounds +0.002, +0.034, +0.061), so the card's D1 rule would call even this tiny drop "robust" there. That illustrates why H2 needs δ and not just an interval that excludes 0.
- **Token α (rank slope, median over subjects).** Trained L0 2.12, L1 4.03, L2 3.07, L3 2.94; untrained 2.33–2.37, 3.74–3.76, 2.47–2.50 and 2.49–2.51. These are descriptive only, with no regime labels (card §5).
- **Per-seed spread.** Seed-to-seed variation is small relative to the trained-vs-init differences at subject level (e.g. C3 per-seed effects 4.93–5.29), but comparable to the H1a / H1b effects at token level.

## 5. Consequences for the earlier readings (addendum 07 §7, applied as frozen)

| Reading (report 2026-10-31 §4) | H2 outcome | Consequence |
|---|---|---|
| R2: the subject-level drop holds (D1, A1b) | C3 TE+, C4 TE+ | **The L2 → L3 between-subject drop is produced by training.** More than half of it is absent in the untrained network on the same input. It is not an architecture or input artefact. G8: keep |
| R2: the token-level H1a holds (L3 higher) | C1 INC | **Unresolved.** About half of the +2.3% (spread of the 8 spatial-cell vectors, norm matched) is already present at init. Whether training adds more than half is not determined. The ceiling of 7 applies. "H1a holds" (replication rule) is unchanged. G8: inconclusive |
| R2: H1b not replicated | C2 INC | Context only: the primary checkpoint's H1b exceeds init by more than δ in 8 of 10 seeds, not in all 10. "Not replicated" is unchanged |
| R2: the mechanism fails (no PatchMerging between layer_2 and layer_3) | — | Unchanged. The same code facts hold in the fork file that produced the dumps (addendum 07 §11) |
| R1: L2 > L1 descriptive only | — | Stays descriptive (the D confound is not removed by a random-init difference). Descriptively, the untrained network shows an equal or larger subject-level L1 → L2 rise, so the "expansion" cannot be read as a training product |
| R3: cross-model ordering holds, attribution untestable | — | Unaffected. No random init of BrainLM, BrainJEPA or NeuroSTORM was run; the attribution stays untestable |
| H2 itself | — | **Tested.** The trained network differs from init where it matters for R2's subject-level reading (Family C C3 / C4; Family L subject level L1–L3, all TE−). It is close to init on the ceiling-limited within-window token PR at L2 / L3 (Family L token EQ / INC) |

## 6. Deviations and limitations

1. **δ was set by the worker, not confirmed by the PI.** PI decision 8 delegated the H2 rule to this addendum, and δ was frozen before any random-init number existed. A different δ would change C1 and C2: both differences have intervals above 0. The label for C1 sits on the δ boundary.
2. **"Random init" means the extraction constructor's default init** (`self.apply(_init_weights)`, seeds 1–10). It is not the training run's own initialization, whose law and seed are unknown.
3. **Thin driver instead of the PL entry point** (addendum 07 §3, §12 item 5). Its equivalence rests on gate G: element-wise agreement on all 399 windows within 7.8e-7.
4. **Only the primary checkpoint.** The zoo checkpoints, including the deep `2 2 42 4` ones, have no random-init counterpart here.
5. **Token-level precision.** CIs of about ±0.002 are subject-sampling intervals given the 10 seeds; seed variation enters through the per-seed condition, not the interval.
6. **The gate is a tolerance gate,** not bitwise identity (A5000 / torch 2.4 vs NERSC).
7. **Recommendation, not a decision.** Per sci-pipeline G9, this report's gate PASS and labels are the worker's recommendation; the PI decides.

## 7. Reproduction

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/addendum_07_sha256.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 scripts/topic3h2_stats.py gate    # rewrites gate_decision.json (run fields change)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 scripts/topic3h2_stats.py final   # rewrites h2_results.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_h2 -q
```

The two stats commands rewrite their outputs. Their result values reproduce, but the `run` fields change the file hashes, so run them in a copied tree to compare JSON values (as in addendum 02 §2). Re-running the connectome jobs needs `scripts/topic3h2_connectome.py build-env`, `ship`, `submit --arm gate` and `collect`, then `submit --arm random` (refused without a gate PASS) and `collect`.
