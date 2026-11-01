# Handoff — worker_M4_r1 (M4 / Topic 4 redesign), Hard handoff, 2026-11-01T02:30Z

## 1. Observation
- **T4.1** (`results/topic4/2026-11-01/t41_counterfactual.json`, produced by `scripts/topic4_t41_counterfactual.py`). This is the protected `evaluate_topology_on_fmri_streams`, unmodified, run on burned positions only.
  - pos 0 (TR 1.8, 197 raw samples, 177 valid cache rows): 0 of 139 test-target rows lie inside the valid portion; test ss_tot = 2.5e-45; all six conditions give R² 1.0; the legacy formula gives persistence 1.0 and train-mean −1.0; the guarded metric raises DegenerateTargetError.
  - pos 932 (TR 1.0, 464/464 valid rows): ss_tot 5331. R² is C0 0.040, C1 0.053, C2 0.051, C3 −0.082, C4 0.024, C5 0.024. Persistence on IMF1 scores 0.992, which is the saturation.
  - Code lines: `src/fractal_motif_resu.py`
    - :417 split
    - :425 `max(ss_tot,1e-8)`
    - :371 full-stream SVD
    - :480 full-stream z-score
    - :349–352 global rescale
    - :347 diag zeroed
    - :301–302 gain ramp and asymmetric M_hier
    - :377 cFFL only for C4
    - :432 lazy rg_box_pooling, which imports torch at rg_box_pooling.py:26
    - :544 hard-coded zero_torch.
  - `src/run_all_empirical_experiments.py:47` sets n_subjects_t4 = 10.
- **Engine probes** (`verification/worker_M4_r1/probe_1.out.json`, `probe_2.out.json`; synthetic):
  - minibatch-64 masked PSP is stable on every mask at η0 ≤ 0.02, and C3 diverges at 0.05;
  - a neuron-local diagonal-dominance guard binds about 42k times on C5 and destroys dense recovery (PR 16 → 5);
  - sparse-mask R² rises as η falls because the engine is less converged (C0 rank 4 at η 0.005 versus rank 1 at 0.02).
- **Qualification** (`results/topic4/2026-11-01/qualification.json`, synthetic, thresholds declared in the script header before the run): all of Q1–Q6 pass at η0 = 0.02.
  - Q1: 0/84 unstable at each ladder η, and 60 unstable at stress η 0.2.
  - Q2: C5 alignment 0.9999/0.9994; C0 PR 1.00; legacy dense decode 0.33, below the 0.92 threshold.
  - Q3: C5 − randlin = +0.09/+0.06.
  - Q4: C5 − C0 = +0.23/+0.15.
  - Q5: MLPenc 0.297 versus RRR 0.299.
  - Q6: oracle 0.3616 versus Bayes 0.3598, SE 0.0023.
- **Mutation** (`verification/worker_M4_r1/mutants/mutation_results.json`): 17/17 mutants killed; the negative control (targets wired but unused) survives, as expected; the control copy passes 63/63.
  - No-backprop matrix (`nobackprop_matrix.json`): the import, importlib and `__import__` mutants are caught by AST and the runtime block; the numpy error signal is caught only by target invariance; the global eig rescale only by AST.
- **Split** (`split_manifest.json`, sha 3e56210f…0436): 1195 TR = 2.0 subjects, 13 sites, 0 contract errors, 0 burned positions in the primary set; 181 tuning (145/36) and 1014 confirm (folds 207/206/204/201/196); overlap 0.
- **Freeze**: card `docs/03_empirical_analysis/topic4/2026-11-01_topic4_analysis_card.md`, sha 2b535c39…5934, frozen 02:04:41Z and chmod a-w. Code hashes (36 files plus qualification, t41 and manifest) are in `code_sha256_at_freeze.txt` (sha 3b061f00…83b2). Both still verify at 02:29Z.
- **Tuning** (`tuning.json`): η0 = 0.02 with all 21 runs stable and max ρ 0.934. G-b: identity 0.146 and persistence −0.308 at 2 s. G-c and G-d pass.
- **Confirm**: 55/55 tasks ok (`confirm_summary.json`, `run_ledger.jsonl`), 02:07:43–02:14:21Z, 4 processes, 0 GPU-h.
  - C3: 10/50 runs unstable (20%, steps 45–466). Every other class: 0 unstable.
- **Verdicts** (`verdict.json`, `scripts/topic4_analyze.py`, B = 2000, seed 20261101):
  - H1 C4 − C1 = −0.0022, 95% [−0.0041, −0.0004]: **stop**.
  - S1 C4 − C4DP = −0.0016 [−0.0038, 0.0005]: **killed**.
  - S2 C5 − randlin24 = +0.0306 [0.0288, 0.0324]: **supported**.
  - S3 C5 − MLPenc = −0.0047 [−0.0050, −0.0043]: **non-inferior at margin 0.01**, with backprop better by 0.005.
  - The H1 sensitivity analyses all lie below 0.
  - Descriptive R² at 2 s: identity 0.1525, RRR 0.1425, MLPenc 0.1415, PCA 0.1370, C5 0.1369, C3 0.1077, randlin 0.1062, C1 0.0925, C2 0.0923, C4DP 0.0918, C4 0.0902, randReLU 0.0770, C0 0.0217, persistence −0.2862.
- **Post-run checks**:
  - `topic4_analyze.py` rerun on a copy gives a byte-identical `verdict.json` (sha 437161ed…5c22);
  - `verification/worker_M4_r1/independent_recompute.py` (imports neither `stats` nor `analyze`) reproduces the H1, S1, S2 and S3 points and the C1, C4, C4DP and C5 class means to ≤ 1.4e-17, and the failure counts exactly (`independent_recompute.out.json`, all_match true);
  - `tests/topic1_lagmotif`: 88 passed;
  - a participant-ID scan of 234 files (code, outputs, verification, metadata) found 0 hits.
- **Tests**:
  - `tests/topic4_resu`: 67 passed (`logs/tests_topic4_final.log`);
  - old suite: 86 passed (`logs/tests_old86_final.log`);
  - C1 `sha256sum -c PROTECTED_HASHES.txt`: rc 0 at start (01:13Z) and end (02:29Z);
  - layout lint on the run metadata root: 161 files, 0 findings.

## 2. Logic Chain
1. pos 0's test window is all padding and pos 932's has none. The same code gives 1.0 versus ≈ 0. So padding plus the floor causes R² = 1.0. Fixtures F1–F4, F-fold and F6-VAR catch this artefact and its relatives, and each has a killed mutant.
2. The legacy engine fails planted recovery and is non-local (Q2, D3). It cannot carry a topology test, so it was replaced with masked PSP, which passes Q1–Q6.
3. Selecting η by forecast skill would favour unconverged sparse engines (probe 2). η was therefore selected by stability only, on the tuning set, before confirm.
4. The card was frozen with code hashes and the split hash before any primary-population outcome. The run script refuses to start on any hash mismatch, and the hashes still verify. So the confirm results are governed by the frozen rules.
5. Under those rules H1's CI_hi (−0.0004) is below δ (0.01), so the verdict is stop. It would be stop for any positive δ. The robustness analyses agree.

## 3. Caveats
- δ = 0.01 is analyst-set; PI confirmation is pending. Every CI is reported.
- C3 failed execution integrity (20% unstable runs). Its contrasts are inconclusive and the exploratory Spearman (+0.28) is driven by C3. No verdict uses C3.
- The engine is near but not at a fixed point: the relative W change over the last 10% of updates is 0.03.
- There is one linear local rule. NSM and rectified rules were not run.
- The within-subject preprocessing is acausal; only TR = 2.0 sites are used; family structure is unknown; the cross-fitted CIs omit training variability.
- 5-fold cross-fitting replaced the LOSO example; this is recorded in card section 10.
- The 4-s descriptive values have no CI (addendum 01).
- No independent pipeline review has been run (sci-pipeline section 6); the gate decision rests with the PI.
- `test_vendored_source_hashes_recorded` is vacuous; the behavioural-equality tests are the real guard (addendum 01, item 7).
- The mutation evidence and the post-freeze documents are pinned in `docs_sha256.txt`, not in the freeze file (addendum 01, item 8).

## 4. Conclusion
M4 is delivered.
- T4.1: diagnosed with a counterfactual, with fixtures and mutation evidence.
- T4.2: a non-saturating redesigned task with a frozen card, a matched backprop baseline, subject-level CIs, seeds and a kill rule.
- T4.3: a local engine with a three-part no-autograd proof, stability, planted-subspace and VAR fixtures, a CPU run, and a verdict per card.

The core Topic 4 claim (Mode II fractal lateral topology helps a local learner) is **killed**. Local learning beats random features. Backprop is slightly better than local learning but within the margin.

## 5. Verification Method
Never rerun a check in place: the analysis and the mutation harness overwrite their receipts. Run on copies.
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?   # 0
LC_ALL=C sha256sum -c results/topic4/2026-11-01/card_sha256.txt results/topic4/2026-11-01/code_sha256_at_freeze.txt results/topic4/2026-11-01/docs_sha256.txt | grep -vc ': OK'   # 0
/home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic4_resu          # 67 passed
STRICT_E2E=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e   # 86 passed
T=$(mktemp -d); cp -r results/topic4/2026-11-01 $T/r
/home/juke/superclaude-env/bin/python3 scripts/topic4_analyze.py --outdir $T/r && cmp $T/r/verdict.json results/topic4/2026-11-01/verdict.json   # identical
/home/juke/superclaude-env/bin/python3 verification/worker_M4_r1/independent_recompute.py $T/r            # all_match true, rc 0
M=$(mktemp -d); cp -r verification/worker_M4_r1/mutants/run_mutants.py $M/ && sed -i "s#^HERE = .*#HERE = '$M'#" $M/run_mutants.py && /home/juke/superclaude-env/bin/python3 $M/run_mutants.py   # 17 killed, CONTROL survives (writes only to $M)
```
The conclusion is invalidated if any of the following holds:
- the card, code or docs hashes fail;
- a confirm subject appears in two folds;
- any confirm task in `run_ledger.jsonl` has a non-ok status;
- rerunning `topic4_analyze.py` on a copy gives a different H1 CI;
- `independent_recompute.py` reports all_match false.
