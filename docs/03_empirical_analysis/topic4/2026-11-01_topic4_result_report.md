# Topic 4 result report (2026-11-01): lateral topology of a backprop-free local learner, 2-s-ahead BOLD forecasting

Governing card: `2026-11-01_topic4_analysis_card.md` (sha256 2b535c3978094bee65e95978ff9d1f93beb440309297265bc278f5cb60695934, frozen 2026-11-01T02:04:41Z, before any primary-population outcome). Deviations: `2026-11-01_topic4_addendum_01.md`. Numbers come only from `results/topic4/2026-11-01/` (`verdict.json`, `tuning.json`, `confirm/`, `run_ledger.jsonl`). Legacy Topic 4 numbers are artefacts (T4.1) and are not cited.
Population: ENIGMA-OCD, TR = 2.0 s sites. 1195 subjects at 13 sites: 181 tuning, 1014 confirm, tested once each in 5-fold subject cross-fitting. CPU only, 0 GPU-h.

## 1. Verdicts (card section 6; δ = 0.01 R², analyst-set, PI confirmation pending)
| hypothesis | contrast (per-subject R² at 2 s) | estimate | CI | rule | verdict |
|---|---|---|---|---|---|
| **H1 (primary)** | Mode II fractal C4 − Erdős–Rényi C1 (69 edges each; 30 graphs each) | **−0.0022** | 95% [−0.0041, −0.0004] | stop if CI_hi < δ | **stop (killed)** |
| S1 | C4 − degree-preserving sham C4DP | −0.0016 | 98.33% [−0.0038, +0.0005] | killed if CI_hi < δ | **killed** |
| S2 | dense local PSP C5 − untrained random-linear-24 (learning value) | **+0.0306** | 98.33% [+0.0288, +0.0324] | supported if CI_lo > 0 and point ≥ δ | **supported** |
| S3 | dense local PSP C5 − backprop MLP-24 encoder (local versus backprop) | −0.0047 | 98.33% [−0.0050, −0.0043] | non-inferior if CI_lo > −δ | **non-inferior at margin 0.01**; backprop is nonetheless better by 0.0047 (the CI excludes 0) |

Execution integrity:
- C3 (rich club) had 10 of 50 confirm runs unstable (20%). The first failing update fell between steps 45 and 466, every fold had failures, and ρ(I − D⁻¹M) reached 1.02–1.56. Because 20% exceeds the card's 10% limit, every C3 contrast is "inconclusive (execution integrity)". No primary or secondary contrast uses C3.
- Every other class had 0 unstable runs: C0 0/50, C1 0/150, C2 0/150, C4 0/150, C4DP 0/150, C5 0/50.
- The tuning stage (C3 init seeds 0–2, 145 training subjects) showed no instability. In confirm, seeds that had been stable in tuning also failed: g0 in folds 0 and 4, g2 in folds 1 and 2. The failures therefore arose on the larger confirm training sets and their different sample sequences, not only on the additional seeds 3–9.

Robustness of H1 (sensitivity, not decisive). Every interval lies wholly below 0, as does the primary CI:
- subject-only bootstrap: [−0.0023, −0.0021];
- site-cluster bootstrap: [−0.0028, −0.0017];
- 4-s horizon: −0.0006 [−0.0011, −0.0001];
- skill against persistence: −0.0020 [−0.0037, −0.0004].

## 2. What the numbers say
- **The core Topic 4 claim fails.** Under a strictly local similarity-matching rule, the hub-repelling "Mode II" lateral topology does not give a better forecasting code than a random graph with the same number of edges. It is slightly worse, by 0.002 R², and also not better than a sham with C4's exact degree sequence. The pre-registered expectation (card section 7) was a null. The observed small negative difference is a "stop" verdict under the card's rule and lies far below the smallest effect of interest.
- **Local learning has value.** The local rule learns more than random features. Dense PSP (C5) reaches 0.137, the same as PCA-24 (0.137), against 0.106 for an untrained random linear 24-d code. So the rule recovers the principal subspace on real BOLD.
- **Backprop is better than local learning, but only slightly.** The backprop encoder (0.1415 ≈ RRR-24, 0.1425) beats dense local PSP by 0.005 R². That gap is inside the pre-set non-inferiority margin.
- **Every 24-d code stays below full-input ridge** (0.1525). This is fixed by construction.
- **What topology does change is the rank of the learned code.** Mutually unconnected units collapse onto the same direction:
  - C0 (no lateral edges) collapses to rank 1 (R² 0.022);
  - the 69-edge sparse classes reach rank ≈ 4.5–4.9 (R² 0.090–0.093);
  - dense C5 reaches rank 24 (R² 0.137).
- **Exploratory only:** across 130 sparse instances, Spearman ρ(instance R², independence number) = +0.28. C3 (α = 17, rank 8, R² 0.108) drives it, and C3 failed the integrity rule, so no verdict rests on this.
- **The redesigned task does not saturate.** At 2 s, persistence scores −0.286 and identity ridge 0.153 (tuning set 0.146; gate G-b < 0.9 passed). At 4 s every arm scores ≤ 0.04.

## 3. Descriptive table (confirm set, n = 1014; per-subject R², subject-bootstrap 95% CI at 2 s; 4-s values are point means)
| arm | R² at 2 s | 95% CI | R² at 4 s | notes |
|---|---|---|---|---|
| constant (train mean) | −0.0001 | [−0.0001, −0.0000] | −0.0001 | ≤ 0 by construction |
| persistence | −0.2862 | [−0.2971, −0.2756] | −0.6557 | |
| identity ridge (48 → 48) | 0.1525 | [0.1484, 0.1565] | 0.0403 | full-input linear ceiling |
| RRR-24 (supervised linear) | 0.1425 | [0.1387, 0.1462] | 0.0390 | |
| PCA-24 | 0.1370 | [0.1333, 0.1406] | 0.0379 | |
| MLP-24 encoder + common ridge (3 seeds) | 0.1415 | [0.1378, 0.1452] | 0.0389 | backprop, early stopped on inner-val |
| MLP-24 end-to-end (3 seeds) | 0.1404 | [0.1367, 0.1441] | — | |
| random-linear-24 (5 seeds) | 0.1062 | [0.1032, 0.1093] | 0.0293 | untrained |
| random-ReLU-24 (5 seeds) | 0.0770 | [0.0747, 0.0792] | 0.0217 | untrained |
| PSP C5 dense (10 seeds) | 0.1369 | [0.1332, 0.1405] | 0.0379 | rank 24, centred PR 14.0, max ρ 0.934 |
| PSP C3 rich club (10 seeds; 20% failed) | 0.1077 | [0.1049, 0.1106] | 0.0319 | rank 8, PR 1.29, α 17. **Integrity failed** |
| PSP C1 Erdős–Rényi (30 graphs) | 0.0925 | [0.0900, 0.0949] | 0.0280 | rank 4.9, PR 2.60, α 8–11 |
| PSP C2 Watts–Strogatz (30 graphs) | 0.0923 | [0.0898, 0.0948] | 0.0279 | rank 4.9, PR 3.00 |
| PSP C4DP degree-preserving sham (30) | 0.0918 | [0.0894, 0.0943] | 0.0278 | rank 4.8, PR 2.64 |
| PSP C4 Mode II fractal (30 graphs) | 0.0902 | [0.0878, 0.0927] | 0.0273 | rank 4.5, PR 2.81, α 8 |
| PSP C0 no lateral (10 seeds) | 0.0217 | [0.0204, 0.0231] | 0.0070 | rank 1 (collapse), PR 1.00 |

- Graph-instance SD of the class mean R² is 0.003–0.004 for the 30-graph classes.
- The median relative change of W over the last 10% of updates was 0.03 for every class. The engine is near, but not at, a fixed point within the frozen 6000-update budget.

## 4. Status of earlier claims
- "All conditions reach forecast R² = 1.0": **false**. This is a padding and floor artefact; see `2026-11-01_topic4_T41_diagnosis.md`.
- "The Mode II fractal topology is the most efficient local architecture (C4 beats C1–C3)": **not supported**. On the matched-edge contrast it is killed (H1 stop), and it is not distinguishable from its degree-preserving sham (S1 killed).
- "Backprop-free local learning matches backprop": **partly supported**. The local code is non-inferior at the 0.01 margin, but backprop is measurably better (by 0.005).
- "Strictly local, zero torch autograd": **now true for the redesigned path**, with a proof in three parts and mutants. The legacy path imported torch at evaluation time.

## 5. Evidence status (sci-pipeline G9)
- Synthetic qualification (Q1–Q6) passed.
- Implementation fixtures: 67 tests, with 17 of 17 mutants killed.
- Real-data effect: this run.
- External replication: none.
- Clinical utility: not addressed.

Limitations are listed in card section 9:
- within-subject acausal preprocessing, so only contrasts are interpreted;
- TR = 2.0 sites only;
- family structure unknown;
- cross-fitted CIs omit training-set variability;
- one linear local rule;
- a fixed 6000-update budget.

The run has not been independently reviewed (sci-pipeline section 6). The gate decision rests with the PI.

## 6. Reproduce
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
LC_ALL=C sha256sum -c results/topic4/2026-11-01/card_sha256.txt results/topic4/2026-11-01/code_sha256_at_freeze.txt
nice /home/juke/superclaude-env/bin/python3 scripts/topic4_run.py --stage tuning  --outdir <new dir with copies of card_sha256.txt, code_sha256_at_freeze.txt, split_manifest*.json>
nice /home/juke/superclaude-env/bin/python3 scripts/topic4_run.py --stage confirm --outdir <same> --procs 4     # ~7 min wall
nice /home/juke/superclaude-env/bin/python3 scripts/topic4_analyze.py --outdir <same>
```
