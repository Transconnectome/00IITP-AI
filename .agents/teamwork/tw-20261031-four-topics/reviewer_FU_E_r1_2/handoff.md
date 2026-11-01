# handoff — reviewer_FU_E_r1_2 (Hard) — milestone FU_E

## Review Summary
**Verdict: APPROVE.** Every criterion has evidence: C1–C8, F1–F3 and the FU-E milestone text ("frozen-encoder fingerprinting and/or age probe"). The shipped verdict **inconclusive** (F+ measurement-capacity gate failed on hcp_S_s2) follows exactly from the frozen card §7–8, and it reproduces in an independent reimplementation. It is also robust: if F+ had passed, J1 alone would still give inconclusive.

## 1. Observation
- **C1.** `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives 67 lines, 0 non-OK, rc 0. It was checked at the start and again at the end (17:47Z).
- **Receipts.**
  - `grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c`: 4/4 OK.
  - output_sha256.txt: 12/12 OK.
  - `LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt`: **17/17** OK. The worker reported "18/18", but the file has 17 entries.
  - The card's sha256 is 072553b0…6ddc36b88f, equal to its receipt.
  - The worker's handoff.md sha256 is 4eab162a…392938f, as claimed.
- **Timeline.**
  - Card frozen 2026-11-01T16:22:56Z (card file mtime 16:21Z).
  - Job 524: submitted 16:24:31Z, started 17:03:57Z, ended 17:20:40Z, COMPLETED 0:0, ElapsedRaw 1003 s. Source: sacct, re-queried read-only on B300.
  - Job 499 (smoke, synthetic only): 8 s, COMPLETED.
- **Tests** (my runs; logs in verification/reviewer_FU_E_r1_2/logs/):

  | suite | result |
  |---|---|
  | tests/topic2_fu_e | 71 passed |
  | old suite (test_empirical_four_topics, test_pilot_connectome, e2e; STRICT_E2E=1) | 86 passed |
  | tests/topic1_lagmotif | 88 passed |
  | tests/topic2_rgpool | 116 passed |

- **Independent recomputation** (verification/reviewer_FU_E_r1_2/indep_verdict.py). It uses numpy/scipy only and does not import src/topic2_fu_e.
  - Provenance 15/15 with all checks True; rescore max relative difference 0.0 over 16 positions; rgpool_freeze_ok (14 files); pins match.
  - The perm buffer is the same for every E seed, the same for every C seed, and distinct for each S seed. This is consistent with the arm identity.
  - **F+**: only S_s2 fails, with Idiff 5.761 vs p95 10.586. An alternative null that permutes rows instead (20,000 draws) gives 10.84, so the failure holds under it too. Seed means are E 16.02, C 22.71, S 16.48.
  - E_s2 passes only narrowly: 11.294 vs 11.001.
  - **F−**: seed means E −2.91, C −0.86, S −1.29, against bounds 5.46, 3.48 and 6.28. Pass.
  - **G2**: pass; seed-mean Idiff_E 61.07.
  - **G3**: cell-FC 64.13 vs p95 5.91. Pass.
  - **J1** [−0.066, +0.228] with SD 0.1185; **J2** [+0.098, +0.202].
  - Shipped Idiff and p95 values equal mine within 1.4e-14.
  - My verdict is inconclusive. The counterfactual with F+ passing is also inconclusive.
- **Report numbers audit.** Every result-report number in §0–§2 matches verdict.json: init twins, pooled, surrogate, subjmask, TRAIN-64, cell-FC per condition, training value, sensitivity without seed 2, init contrasts and jackknife SE. The only difference is pooled-E accuracy 0.475, which the report shows as 0.47.
- **B300**, read-only with no GPU:
  - The sha256 of `/scratch/iitp4/fu_e/main/extract.json` is 1921b044…, equal to the repo copy.
  - The B300 code copy (src/topic2_fu_e and the scripts) is byte-identical to the frozen repo code.
  - The hcp_S_s2 and hcp_C_s0 checkpoint sha256 values equal their pins.
  - No `g3t-G-E0-*` job ran 20:00–03:00 KST. Other `g3t-*` jobs did, e.g. fulltests 488, which overlapped smoke 499.
- **Code review.**
  - verdict.classify implements card §8 in order: lost → no_verdict → gate-missing → F+/G2/G3 inconclusive → stop/keep/modify/else → keep downgrade on F−.
  - Gates are tri-state, and None is never a pass.
  - model_table rejects duplicates, a failed status, a wrong subject order, and a non-24×24 or non-finite R.
  - The extraction script computes everything from data, with no hardcoded outcomes. The rescore uses the frozen r1 `train.evaluate_hcp`.
  - The job verified the frozen hashes on B300; slurm-524.out shows 10 OK.
- **My mutation probe** (verification/reviewer_FU_E_r1_2/run_mutants.py, 27 mutants, my own set): **24 KILLED**. Three survived:
  - R03, null quantile 0.95→0.90;
  - R10, F− bound mean→max of p95;
  - R15, rescore tolerance absolute instead of relative.
- **Ledger** (results/gpu_ledger_2026-10-31.md): started and completed rows exist for 407/412/420 (explorers, 0.015 GPU-h), 499 (0.003) and 524 (0.279). 1003 s × 1 GPU = 0.279. FU-E total 0.297 ≤ 1.5 cap.
- **C4.**
  - No `sub-` labels in FU-E results, docs, verification or metadata.
  - Every bare 6-digit token in those files is a count (n_features, n_vox) or a sha fragment. I inspected them with the digits masked.
  - The worker's B300 name-list scan found 0 hits.
- **Layout.** `audit_layout.py` on the whole run root: PASS, findings [], rc 0, 474 files.

## 2. Logic Chain
1. The card was frozen before any real-data statistic (§0 disclosure; freeze < submit < start). That gives **F1/C3**.
2. Synthetic fixtures fail on the targeted defects: test_fminus_with_subject_masks_shows_the_anatomy_confound, null iid noise, surrogate. Verdict-path tests kill 24/27 of my independent mutants, including the V06–V10-type classes: gate→inconclusive vs no_verdict, missing gate ≠ pass, order of rules, F− keep-only downgrade, subject order, size checks. That gives **F2**.
3. All GPU work went through Slurm on b300-01 within the cap, with ledger rows, run records (slurm out, sacct, jsonl log) and the dated results dir. That gives **F3/C5**.
4. HCP OA data stayed on B300, only aggregates with positional labels came back, and no ID shapes were found. That gives **C4/C6**. C8 holds: every report number traces to run_524 → verdict.json.
5. My recomputation matches every governed number, and the F+ failure is far from its boundary (5.76 vs 10.59 at p95; it also fails at p90, 8.43). The shipped **inconclusive** is therefore correct per the card and not fragile.
6. The three surviving mutants touch constants or paths that cannot change this shipped verdict: rescore was exactly 0.0, F− passes under either bound, and F+ fails under p90. They are test-gap notes, not defects.
7. The milestone says "fingerprinting and/or age probe". Fingerprinting was run and honestly labelled as within-run split-half identifiability. The age/sex probe is untestable at δ, with evidence: explorer_FU_E_r1_1 O6/O7 found 28/103 labelled subjects, and its power argument (AUC SD ≈ 0.05–0.1 ≫ 0.01) holds even with the full OA table. The criteria are met.

## 3. Caveats
- **No reviewer GPU re-execution of the R matrices.** The shared Slurm user had a long PENDING queue (FU-B/C/D, GARD, others) under its 8-GPU limit, and a probe would add contention for marginal value. Record integrity rests on the B300 sha match, sacct, the log timings and the exact r1 rescore. 0 GPU-h used by me.
- I did not rerun the worker's 29-mutant harness; I used my own 27 instead.
- I did not re-verify the explorer's label counts (28/103).
- The age probe is better described as "underpowered at δ" than strictly "untestable". A descriptive probe was possible but was omitted by card §10, which was frozen beforehand. This is acceptable.
- Interpretive limits, already disclosed in the report §5:
  - random-init twins already identify every subject (accuracy 1.00), so cov2 Idiff largely reflects input FC structure;
  - TRAIN-64 vs held-out Idiff compares pools of different N.
- DISPATCH.md summarises, rather than copies byte-for-byte, the worker JSON embedded in my dispatch. The authoritative copy is the worker's handoff.md, whose sha256 I verified.

## 4. Conclusion
APPROVE FU_E. Shipped verdict **inconclusive** (synthetic F+ capacity gate failed on hcp_S_s2); the r1 stop is unchanged and the downstream question stays open. No blocking issues.

Nonblocking:
- (a) The null quantile, the F− bound aggregation and the rescore relative-tolerance form are not pinned by tests (R03, R10, R15 survive). None affects the shipped verdict.
- (b) The worker's handoff says "code 18/18 OK"; the receipt has 17 entries, all OK.
- (c) The smoke job 499 B300-share squeue check failed on an ssh pipe before submission. This is disclosed. sacct confirms no `g3t-G-E0-*` job ran, though other SwiFT `g3t-*` jobs did.
- (d) The deviations are recorded in the dated result report §3 rather than a separate addendum. No post-freeze card change occurred, so no addendum was required.
- (e) `src/topic2_fu_e/__pycache__` was written 16:20:59Z, despite the PYTHONDONTWRITEBYTECODE instruction. It is gitignored and outside the .py-only receipts.
- (f) The E_s2 F+ pass is marginal (11.29 vs 11.00). Any future card should handle stalled or degenerate seeds a priori.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c             # 4/4
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt                   # 17/17
grep -v '^#' results/topic2/2026-11-02_fu_e/output_sha256.txt | LC_ALL=C sha256sum -c           # 12/12
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q   # 71 passed
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_FU_E_r1_2/indep_verdict.py results/topic2/2026-11-02_fu_e/run_524/extract.json results/topic2/2026-11-02_fu_e/verdict.json   # indep_verdict inconclusive
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/reviewer_FU_E_r1_2/run_mutants.py   # 24/27 killed
python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py .agents/teamwork/tw-20261031-four-topics   # PASS
```
Invalidation conditions:
- any receipt fails;
- extract.json changes from sha256 1921b044…;
- a real-data FU-E statistic predating 16:22:56Z is found;
- an ID token appears in FU-E outputs.
