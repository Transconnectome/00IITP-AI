# Handoff — challenger_FU_D_r1_2 (milestone FU_D), Hard handoff, 2026-11-01T19:38Z

**Verdict: CONFIRMED.** The FU-D verdict holds: `inconclusive` (measurement capacity), card §8 step 2.
- The headline numbers reproduce exactly, both from the saved per-group terms and from the saved checkpoints.
- The card was frozen before any FU-D result.
- The verdict follows the card's rules.
- There are 3 nonblocking test-coverage gaps (one of them shows that δ is not pinned by any test) and 2 small robustness gaps in the record and verdict code. None of them changes the shipped verdict.

## Challenge summary
Overall risk assessment: **LOW** for the shipped verdict. **MEDIUM** for how well the test suite guards future runs of the verdict script, because of M19.

## 1. Observation

**Integrity and receipts**
- C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives 0 non-OK lines and rc 0, both at the start and at the end of my work.
- FU-D receipts (`grep -v '^#' … | sha256sum -c`): card 1/1, code 29/29 and outputs 34/34 are OK. The r1 freeze `results/topic2/2026-11-01/code_sha256_at_freeze.txt` gives rc 0.

**Freeze before results**
- Git commit `34f4b303` (2026-11-02T00:50:24+09:00 = 15:50:24Z, host autocommit) contains the card. Its blob hashes to `1b7fee6c…6001b`, which is the frozen sha.
- The receipt says 16:06:07Z.
- After both of these come, in order: the view build (`logs/view_check.json`, 16:11:26Z), the first FU-D Slurm submission (job 511, 16:13:50Z per `logs/jobs.jsonl`) and the gate jobs 534/535/536 (submitted 16:39–16:41Z, started 17:46–17:52Z).
- The worker's mutation r2 run finished at 16:05:29Z, before the freeze.
- sacct on B300 (all FU-D-named jobs since 11-01) shows only 393–395 and 415 (CPU-only, 0 s), 396/404/418/430 (explorer synthetic smokes), 511 and 534–536.
  - `/scratch/iitp4/fu_d/runs` holds only `Fplus_{E,C,S}_s0`.
  - So there are no hidden reruns, no extra gate seeds and no Stage-1 runs.

**Recomputation from saved records** (`verification/challenger_FU_D_r1_2/recompute.py`)
- Σnum/Σden over the 16 groups reproduces test NMSE E 0.6558494816918741, C 0.653467876277415 and S 0.6577736746995909 with a difference of 0.0.
- Gains: (E−C)/E = 0.0036313292621888414 and (S−C)/S = 0.006546018163682844, so pass = False. These equal `verdict.json`.
- The denominators are identical across arms and identical to the r1 E36 `Fplus_E_s0`, so the test windows and masks are the same as r1.
- The perm keys, perm sha (E b83e23eb…, C 72f72d1e…, S_seed0 d540c76a…), cells moved (0/1324/1287), cfg E192_d22182, 474,226,176 parameters, 8750×16 budget and hyperparameters all match the card.
- The frozen r1 code hashes in the run records match the r1 receipt, and the FU-D code and wrapper hashes in `fud_meta.json` match the FU-D freeze receipt.

**Independent GPU re-evaluation** (Slurm job 574, b300-01, debug partition)
- Ledger rows are written (started 19:25:24Z; completed 19:31:26–19:32:16Z, 0.014 GPU-h). The squeue `g3t-G-E0-*` check was 0 before submission.
- I loaded each `model_final.pt`:
  - each perm buffer `layers.0.downsample.perm` equals its pinned npz key;
  - the frozen `evaluate_fixture` (eval seed 7002) reproduces test NMSE **bit-exactly** for all 3 arms (max relative num difference 0.0, den equal).
- Perm-swap probe: with the wrong gather the NMSE rises to 1.124 (E with the C perm), 1.102 (C with identity) and 1.106 (S with identity). So the M0 gather is live in the E192 forward pass, and the small gate gain is not caused by the permutation being ignored.
- Output: `verification/challenger_FU_D_r1_2/b300/reeval_fplus.json`.

**Verdict oracle** (`verdict_oracle.py`)
- I wrote my own implementation of the card §8 table from the card text alone.
- Over 40,000 random cases (all gate, plan, Stage-1, stall and F− states) it shows **0 mismatches** against `V.decide`.
- The shipped inputs give `inconclusive` from both.
- The δ boundary is right: gain exactly 0.01 passes, and 0.0099999999 fails.

**Adversarial end-to-end runs of `scripts/topic2fu_d_verdict.py`** on copies of the shipped records (`script_adversarial.py`)
- 22 of the 24 cases behave as the card requires:
  - Slurm TIMEOUT or a missing `slurm.json` gives no_verdict;
  - a failed C run gives no_verdict;
  - a failed run followed by a completed `_a1` is read;
  - a rerun of a completed run gives a RecordError;
  - a missing C run gives no_verdict;
  - tampered test_nmse, perm key or sha swaps, cfg E36, steps 4375, arm mismatch, post_checks false, a foreign wrapper sha, a changed r1 code hash, 15 terms, or a missing val step each give a RecordError;
  - an `hcp_` dir with a failed gate is flagged and not read;
  - a gate pass with no plan gives no_verdict.
- Two gaps:
  - **G1:** `test_nmse = NaN` with finite num/den is accepted (`abs(pooled - nan) > tol` is False in `records.validate_completed`). The gate then reads it as a computed fail (`inconclusive`) instead of raising a protocol error.
  - **G2:** when the gate fails or is incomplete, the gate is loaded with `strict=False`, so unplanned directories (`Fplus_C_s1`, `junk`) are silently ignored. Card §8 says unplanned directories are protocol errors that stop the script. Only `hcp_*` dirs raise a flag.

**My own mutation set** (29 mutants, independent of the worker's 62; `mut/run_mutants.py`, `mut/mutants.out.json`, suite in a copied tree, e192 model test deselected; the baseline suite in that tree passes 129/129)
- 26 are killed and **3 survive**:
  - **M19** `DELTA = 0.01` → `0.003` in `src/topic2_fu_d/config.py`: the suite stays green. Run on the shipped records, the script then gives gate pass = True and verdict `no_verdict` ("seed plan missing") instead of `inconclusive` (`mut/m19_verdict.json`). The tests pass `D = 0.01` explicitly to the functions, and no test asserts `K.DELTA == 0.01` or re-derives the shipped verdict.
  - **M12:** the test_nmse consistency tolerance 1e-12 → 1e-3 survives.
  - **M21:** the "exactly 16 terms" check removed survives.

**Suites**
- `tests/topic2_fu_d`: 129 passed.
- Old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed.

**Other checks**
- `audit_layout.py` on the whole run metadata root gives findings [] (519 files).
- C4: a scan of 76 FU-D files for standalone 6-digit numbers and BIDS `sub-` labels found 0 IDs. The only 6-digit hit is the prefix of the merge.py hash `971376c6…`. The B300 output of my own probe also has 0 hits.

**Other numbers**
- The ledger rows for jobs 511, 534, 535 and 536 equal sacct ElapsedRaw/3600, rounded up (0.040, 1.175, 1.180, 1.180).
- The explorer total is 0.03 + 0.03 + 0.001 + 0.036 = 0.097.
- The E36 r1 descriptive numbers in report §2 and §5 are right: seed 0 gives 2.772 % / 2.900 %, and seed 1 gives 3.348 %.
- The val curves and the C < E < S ordering at every step are as reported.

## 2. Logic chain
1. The card bytes existed in git at 15:50Z and the receipt is dated 16:06Z, while every FU-D GPU job and the view build came later (Obs. freeze). So the card and code were frozen before any FU-D real-data or gate result.
2. The test NMSEs are reproduced from the per-group terms and, independently, from the checkpoints on the GPU. The checkpoints hold the pinned permutations, and those permutations change the output strongly. So the gate numbers are real outputs of correctly configured E192 E/C/S models.
3. The gains of 0.363 % and 0.655 % are both below δ = 1 %. Card §7.1 and §8 step 2 then give `inconclusive` (measurement capacity) with Stage 1 not run. My oracle and the shipped code agree on this and on 40k other cases.
4. sacct and the directory listings show no extra or hidden runs, so the result is not a selection among attempts.
5. The surviving mutants (M19, M12, M21) and gaps (G1, G2) are weaknesses in the code's self-protection. They do not affect the shipped verdict: config.py is pinned by the freeze receipt (964a5ade…, verified), `verdict.json` records delta 0.01, every shipped record is finite with 16 terms, and the runs dir holds only the 3 planned dirs. They are therefore nonblocking. M19 is the most important of them, because it is a verdict-flipping mutant that a green suite does not detect.

## 3. Caveats
- I did not re-run training (forbidden: full option). The bit-exact re-evaluation covers the evaluation path, not training determinism.
- One F+ seed at E192 is pre-registered (card §7.1). The "gain shrinks with scale" reading (report §0 and §2) rests on n = 1 seed per scale with no interval. The report labels it descriptive, but "closes it further" generalises beyond what n = 1 shows.
- Card §7.1 wording: "+3.06 % / +2.93 %" are the r1 seed-mean C-vs-E and C-vs-S gains, not per-seed values (the seeds give 2.77 % and 3.35 %). This is a wording slip in the frozen card and does not affect any decision. Card §0 lists explorer jobs 396/404/430 but its 0.097 total also includes job 418 (0.001).
- I did not re-verify the HCP smoke (equiv) beyond the recorded flags, because `smoke/equiv.json` stores flags, not terms. It is a precondition only.
- The e192 model test was deselected in my mutation runs (CPU build cost). None of my mutants touched model code.

## 4. Conclusion
**CONFIRMED.** The FU-D result (`inconclusive`, measurement capacity at E192; Stage 1 correctly not run; r1 E36 stop stands alone) is supported:
- independent recomputation and GPU re-evaluation reproduce it;
- freeze ordering is evidenced;
- the verdict mapping is correct.

Nonblocking recommendations, all additive tests or an addendum, with no change to frozen code:
- (a) a test asserting `K.DELTA == 0.01`, plus a script-level test with gate gains between 0.003 and 0.01 that must give `inconclusive` (kills M19);
- (b) tests that a 1e-6 tamper of test_nmse and a non-16 term count are rejected (kills M12 and M21);
- (c) record G1 (NaN test_nmse) and G2 (unplanned dirs ignored when the gate fails) in a dated addendum as known code-vs-card gaps.

GPU use: 0.014 GPU-h (job 574).

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # 0
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c --quiet && echo $f OK; done
git show 34f4b303:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md | sha256sum   # 1b7fee6c…
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r1_2/recompute.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r1_2/verdict_oracle.py      # 0 mismatches
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r1_2/script_adversarial.py  # nan + unplanned-dir gaps
cd verification/challenger_FU_D_r1_2/mut/tree && /home/juke/superclaude-env/bin/python3 ../run_mutants.py               # 26 killed, M12/M19/M21 survive
cat verification/challenger_FU_D_r1_2/b300/reeval_fplus.json                                                              # bit-exact re-eval, perm-swap
grep challenger_FU_D_r1_2 results/gpu_ledger_2026-10-31.md
```
Invalidation conditions:
- any FU-D receipt fails;
- `/scratch/iitp4/fu_d/runs` gains directories;
- `src/topic2_fu_d/config.py` hash ≠ 964a5ade…;
- the re-evaluation is not reproducible.
