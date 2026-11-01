# Handoff (hard) — challenger_FU_E_r1_1, milestone FU_E (Topic 2 follow-up E)

Verdict: **CONFIRMED**. The shipped FU-E result holds: `inconclusive` (synthetic F+ gate failed on hcp_S_s2), card frozen before any real-data result, numbers exact.
I did not break the shipped verdict. I found test-coverage gaps (12 of my 52 mutants survive; 2 are equivalent). All of them leave the shipped verdict unchanged. They are listed as nonblocking below.
Overall risk: **LOW**.

## 1. Observation

Commands were run from `/home/juke/git/00IITP-AI`. The probes live in `verification/challenger_FU_E_r1_1/`.

- **C1 and receipts.**
  - `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: 0 non-OK lines, at both start and end.
  - FU-E receipts: card 4/4 OK, code freeze 18/18 OK, outputs 12/12 OK.
  - r1 `results/topic2/2026-11-01/code_sha256_at_freeze.txt`: 0 non-OK.
- **Freeze timeline.**
  - `card_sha256.txt` says frozen 2026-11-01T16:22:56Z. The card mtime is 16:21:26Z.
  - The host autocommit `cd1e43e` (2026-11-01T16:35:27Z) holds the card with sha256 **072553b0…** (equal to the receipt).
  - The earlier autocommit `35d10a5` (16:05Z) differs only by 2 added lines, the smoke-499 disclosure.
  - Job 524 was submitted at 16:24:31Z (`main_submit.txt`). sacct shows it started at 17:03:57Z and ended at 17:20:40Z. `extract_log.jsonl` starts at 17:04:00Z.
  - The job log shows the FU-E src/scripts freeze check 10/10 OK on B300. The r1 rgpool freeze was checked for 14 of 14 rgpool files, which covers every imported rgpool module.
- **Independent recomputation** (`recompute/recompute.py`; imports neither src/topic2_fu_e nor src/topic2_rgpool; scipy t). Every governed number matches `verdict.json`, max abs diff 1.4e-14:
  - J1 0.08105 [−0.06603, +0.22814]; J2 0.15005 [+0.09796, +0.20213]; SD_seed(J1) 0.1185.
  - G2: every E and S seed above null; mean Idiff_E 61.07.
  - G3: 64.13 vs p95 5.91.
  - F+: the only failure is S_s2, Idiff 5.761 vs p95 10.586. Seed means are E 16.02, C 22.71, S 16.48.
  - F−: seed-mean Idiff vs seed-mean p95 is E −2.91 / 5.46, C −0.86 / 3.48, S −1.29 / 6.28.
- **Robustness of the decisive F+ failure** (S_s2):
  - Under 5 other null seeds, p95 is 10.28–11.07.
  - Under a derangement-only null (fixed points cannot carry true identity), p95 is 10.87.
  - A 20 000-draw Monte Carlo gives p = 0.189.
  - Top-1 accuracy is 0.0625 (chance about 0.04). Diagonal mean 0.038 vs off-diagonal −0.020.
  - So it is a real capacity failure, not an artefact of the null.
  - Note: E_s2 passes F+ only narrowly (11.29 vs 11.00).
- **Would-be step-4 verdict if F+ were ignored:** `inconclusive` (J1 straddles 0 and δ). The verdict is therefore overdetermined.
- **Verdict script rerun:** `scripts/topic2fu_e_verdict.py` run on `run_524/extract.json` gives byte-identical `verdict.json` and stdout (`rerun/`).
- **Report §2 descriptive table:** every cell was re-derived independently (`recompute/descriptives.out`) and matches. This includes the init twins 53.8/54.2/54.4, surrogate 3.9/7.3/6.5 (cell-FC 0.02), subjmask, TRAIN-64 70.4/73.2/65.1, training value E +7.25 / C +11.26 / S +2.47 with negatives E_s0, S_s0, S_s3, jackknife SE 0.0453, and without-seed-2 J1 [−0.126, +0.304] / J2 [+0.107, +0.219].
- **Shipped record integrity:**
  - All 6 conditions carry exactly the canonical positional labels (test:0–15, val:0–7; synth:0–23; train:0–63) for every model.
  - No duplicate model keys; all models `ok`.
  - G0 per checkpoint: all 15 have pin, completed, perm, strict and rescore true (max rel 0.0, 16 positions), and test order = split.
- **Tests:**
  - `tests/topic2_fu_e`: 71 passed (17.7 s).
  - Old suite (`STRICT_E2E=1 … tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed.
- **Mutation testing** (`mutants/`): 52 own mutants of ident, prep, readout, pipeline, synth, provenance and verdict, each run against the full `tests/topic2_fu_e` suite. Results: 40 killed, 12 survived (`mutants/results.txt`).
  - Survivors:
    - I05: null quantile 0.90.
    - I08: jackknife reversed (equivalent).
    - R03: cellfc without the mask multiply (equivalent; halves are already 0 outside the same mask).
    - PV02: perm_ok ignores the run.json perm_sha256.
    - PV03: rescore numerator tolerance absolute.
    - V05: F− bound uses the max of the null p95 values, not the mean.
    - V06: G3 ignores the cellfc status.
    - V07: G3 shape and finiteness unchecked.
    - V08: F+/F− gates on the `pooled` readout.
    - V09: primary contrasts and G2 on the `pooled` readout.
    - V11: PERM_SEED changed.
    - V12: N_PERM 100.
  - Each survivor applied to the shipped `extract.json` still gives `inconclusive (synthetic F+)` (`mutants/survivors_on_shipped.txt`). V09 moves J1 to [−0.050, +0.238].
  - Root cause of V08/V09 surviving: `tests/topic2_fu_e/helpers.record` puts the same matrix under `cov2` and `pooled`, so readout wiring is never exercised.
- **Adversarial records against the shipped verdict code** (`edge/edge_cases.out`):
  - A governed `main` pool whose labels are all `test:0`, reversed, or `train:k` (consistent across models) is classified **keep**, not no_verdict. The guard checks only cross-model consistency, not the card §4 split.json order.
  - Idiff_E,s0 = 0 exactly gives `inconclusive (G2)`. The card §8 table lists "contrasts not computable → no_verdict" at step 2, before step 3. Card §6 says G2 keeps the denominators away from 0, so the intent is ambiguous.
  - Neither applies to the shipped record.
- **C4:** a scan of the 50 FU-E files (results, docs, worker verification and metadata, src, tests, scripts) for six-digit tokens and `sub-` labels found 0 `sub-` labels. The 10 six-digit tokens are all `n_features`, `n_vox` or `n_common_mask_vox` counts in JSON. No identifier was printed or written.
- **GPU ledger:** the rows for jobs 499 (0.003) and 524 (0.279) are present and consistent with sacct (1003 s × 1 GPU = 0.2786 GPU-h, rounded up). With the explorers' 0.015 (407, 412, 420), the total is 0.297 of 1.5.
- **My B300 probe** (job 557):
  - Synthetic only: an independent F+ re-extraction for S_s2, E_s2 and C_s2, bf16 and fp32.
  - Submitted 17:44:14Z after the check `G3T_CHECK none`. A started ledger row was appended under flock.
  - It stayed PENDING on QOSMaxGRESPerUser behind about 11 higher-priority jobs.
  - I cancelled it myself while it was still PENDING (sacct: `CANCELLED by 1000`, Start None, ElapsedRaw 0; `b300/cancel557.txt`). A closing ledger row with 0 GPU-h was appended under flock.
  - **GPU use by this challenger: 0 GPU-h.**
  - The ssh master is closed and no processes are left behind.
  - Whole-run `audit_layout.py`: findings [], rc 0 (493 files). C1 at the end: 0 non-OK.

## 2. Logic Chain

1. The freeze precedes the results. The receipt time (16:22:56Z) and an independent daemon commit of the frozen bytes (16:35:27Z) both precede the only real-data job's start (17:03:57Z). The only pre-freeze card change was a disclosure line. (Obs: freeze timeline)
2. The numbers are what the card defines. A from-scratch implementation reproduces every governed value to 1e-14 and every descriptive value in the report. (Obs: recomputation)
3. The verdict follows the card. Card §8 step 1 does not apply: 15/15 checkpoints are present. Step 2 does not apply: G0 all true, freeze OK, extraction 15/15 ok at 24×24 in canonical order, all gates non-None, contrasts finite. At step 3, F+ is False, so the verdict is inconclusive. This is exactly what the code returned.
4. The F+ failure is not an artefact. It persists under alternative null seeds and a derangement null, and the accuracy is near chance. The card disclosed beforehand that S_s2 had stalled and fixed the rule as all-seeds. (Obs: robustness)
5. The verdict is overdetermined. Even with F+ ignored, the J1 interval [−0.066, +0.228] gives inconclusive at step 4. No surviving mutant changes the shipped verdict. (Obs: mutation, survivors on shipped)
6. Therefore the claim holds: CONFIRMED. The surviving mutants and the label-guard gap weaken the tests as a safety net, not this result. The independent recomputation already certifies the shipped computation.

## 3. Caveats

- **No GPU re-extraction completed.** That B300 job 557 sat PENDING (QOSMaxGRESPerUser; the user-wide 8-GPU limit was full with FU-B, FU-C, FU-D and other teams' jobs). The faithfulness of `extract.json` to the checkpoints therefore rests on:
  - the worker's B300 run and its G0 rescore (exact r1 reproduction, 15/15);
  - internal consistency (canonical labels, all-ok statuses, finite matrices);
  - not on my own forward pass.
- The probe script and sbatch are kept for reuse: `verification/challenger_FU_E_r1_1/b300/fplus_probe.py` and `probe.sbatch` (sha256 88d10e95… and cd9115f0…). Their copies on B300 are in `/scratch/iitp4/challenger_FU_E_r1_1/`.
- I did not re-run the B300 ID scan. The C4 check is a local token-shape scan of the copied-back files only.
- I did not verify the open-access label counts (card §10) or the explorer facts in card §0. They govern no decision.
- Mutation testing covers the FU-E Python modules only. `scripts/topic2fu_e_extract.py` (the GPU orchestration) has no CPU test. I reviewed it by reading: halves, surrogate seeds 9000 + 100·pos + half, positional labels, test-then-val order and the fixture seeds all match the card.

## 4. Conclusion

**CONFIRMED.** FU-E verdict `inconclusive (measurement capacity: synthetic F+ failed on hcp_S_s2)` is correct under the frozen card, reproducible from the saved raw record, and robust. The r1 stop verdict is unchanged, and the downstream question stays open.

Nonblocking items (an additive test addendum would close them; none changes the shipped verdict):
- (a) Use different matrices for `cov2` and `pooled` in the test helpers, so the readout wiring of the gates and the primary contrasts is tested (kills V08 and V09).
- (b) Pin the card constants PERM_SEED, N_PERM and the 0.95 quantile (I05, V11, V12).
- (c) Test F− seed-mean pooling of the null p95 (V05).
- (d) Test the G3 status, shape and finite guards (V06 and V07; near-equivalent given the producer).
- (e) Test the run.json perm leg and the relative numerator tolerance in G0 (PV02, PV03).
- (f) Check the governed main pool against the canonical split order (edge D/E/F).
- (g) A one-line erratum on the Idiff_E = 0 ordering ambiguity.
- (h) Report wording: "random-init twins identify every held-out subject (accuracy 1.00)" is a seed-mean rounded to 1.00. The minimum per model is 0.979 (0.977 on TRAIN-64).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # 0
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c
git show cd1e43e:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_card.md | sha256sum   # 072553b0...
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/challenger_FU_E_r1_1/recompute/recompute.py results/topic2/2026-11-02_fu_e/run_524/extract.json results/topic2/2026-11-02_fu_e/verdict.json
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/challenger_FU_E_r1_1/recompute/descriptives.py results/topic2/2026-11-02_fu_e/run_524/extract.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q   # 71 passed
verification/challenger_FU_E_r1_1/mutants/run_mutants.sh            # results.txt: 40 KILLED / 12 SURVIVED
verification/challenger_FU_E_r1_1/mutants/survivors_on_shipped.sh   # all 'inconclusive (synthetic F+)'
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_E_r1_1/edge/edge_cases.py
```

Invalidation conditions:
- any receipt or C1 mismatch;
- `extract.json` sha256 ≠ 1921b044…;
- a GPU re-extraction of the F+ fixture through hcp_S_s2 giving Idiff above its null p95. That would mean the saved record does not reflect the checkpoint.
