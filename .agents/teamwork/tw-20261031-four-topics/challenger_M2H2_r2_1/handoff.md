# Handoff — challenger_M2H2_r2_1 (M2H2 r2 gate, Topic 3 H2 random-init control) — HARD

Verdict: **CONFIRMED**. Nothing blocking. There are 3 nonblocking findings (N1–N3 below).
Agent: challenger_M2H2_r2_1. Host: claude-code. Parent: root 5fddb83e (workflow C). Timeframe: 2026-11-01 20:03Z to 21:40Z. GPU use: 0 GPU-h. I made no connectome access, no git writes, no installs, and no production edits.

## 1. Observation

**Integrity**
- C1 `PROTECTED_HASHES.txt`: rc 0, checked at 20:10Z and again at 21:38Z.
- `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries): rc 0.
- `addendum_07_sha256.txt` and `r2/addendum_08_sha256.txt`: rc 0.
- 2026-10-31 receipts: `addendum_02`–`06` and `output_sha256` rc 0. `card_sha256.txt` and `code_sha256_at_freeze.txt` give rc 1, as known before this run.
- Every sha256 in the worker's `frozen_artifacts_sha256` list matches the file on disk.
- Of the files under src/topic3_h2, scripts/topic3h2_* and tests/topic3_h2, the only ones not pinned in output_sha256 are the 4 new r2 test files. No pinned file is missing.

**Freeze timing**
- Addendum 07 was frozen at 15:57:40Z (`addendum_07_frozen_utc.txt`).
- The host autocommit `35d10a5` contains it at 2026-11-02T01:05:25+09:00 (16:05:25Z), with the same sha `09b45220…`.
- The gate job 218063 was submitted at 16:22:19Z. The random job 218064 started at 16:32:19Z (logs and records).
- The code hashes recorded by both jobs (20 files) equal the current repo files.

**Independent recomputation** (`verification/challenger_M2H2_r2_1/independent_recompute.py`)
- Written with my own PR estimators, index sets, sign-flip test, bootstrap, Holm and decision rule. Inputs are only the pinned T arrays, the returned R1–R10 npz files and the pinned family JSONs.
- All 24 labels match, with every point, CI, Holm p and seed-effect within 1e-12 (`diffs_vs_shipped: []`):
  - Family C: C1 INC, C2 INC, C3 TE+, C4 TE+.
  - Family L token: L1 cov/corr TE−; L2 corr, LN0L2 corr, L3 cov and L3 corr EQ; the rest INC.
  - Family L subject: L1, L2, LN0L2 and L3 TE− for both estimators; L0 INC.
- δ recomputed from the raw T arrays equals the frozen values. For example, the H1a mean log ratio is 0.022750675828012934 and D1 cov is 5.343854531110546 with SE 1.081055126274951.
- My card index-set hash `cd020fe8…` equals the `index_sets_sha256` recorded by both jobs.
- R0 subsets match my T subsets to a relative 6.35e-7 or better.
- Seed arms really differ: the minimum pairwise max-abs difference of `cat_covpr__L3` across seeds is 0.164.
- All R arrays are finite and dropped-column counts are 0.

**Report numbers**: checked against `h2_results.json` and `gate_record.json`. They match:
- the §1 G1–G5 values;
- the §2 table;
- the §3 ratios, max token p_holm 0.0149, the seed ranges and the −0.079 value;
- the §3 E1 ranges (17.6–20.9, 30.9–34.0, R0 2.78 / 11.02 / 3.58);
- the §4 R1/A1b values, the per-seed D1 seeds (5, 7, 10 at +0.002 / +0.034 / +0.061) and the α medians;
- per-seed H1a: 9 of 10 seeds significant; seed 4 −0.0004, p_holm 0.5217.

**Errata check** (`single_seed_and_delta.py`)
- E8 single-seed labels match exactly:
  - C1: EQ for seeds 1, 5, 8; TE+ for 4, 7, 9, 10; INC for 2, 3, 6.
  - C2: TE+ for 4, 5, 7, 9, 10.
  - C3 and C4: TE+ for every seed.
- E1 boundaries match: C1 0.1575 / 1.0175; C2 0.4580 / 1.1115; C3 0.5483 / 1.2912; C4 0.6636 / 1.2057.
- Distance from f = 0.5 to the nearest label flip: C2 0.0420, C3 0.0483, C4 0.164, C1 0.342.

**Fresh mutation harness** (`fresh_mutants.py`; outputs `fresh_mutants_shard{0,1}.out.json`; logs `logs/fresh_mutants_shard*.log`)
- Ran in 2 copied trees. Both baselines: 167 passed.
- 45 new mutants, none of them in the r1/r2 union list: 20 KILLED and 25 SURVIVED.
- 0 invalid runs and 0 not applied. Every mutated file was restored byte-identically.
- **Killed**, including every new decision-rule and verdict-wiring mutant:
  - F01 (seed dropped), F02 (Holm reversed), F03 (EQ by midpoint), F04 (δ guard);
  - F23, F25, F31, F33, F35, F50, F51, F52, F57, F71, F72, F75, F86, F87, F91.
- **Survived** (full suite, rc 0):
  - stats script: F20 `_dump` ID guard off; F21 pinned-T positions guard off; F22 T-A1 tolerance 1e-3; F24 gate G2-missing defaults ok.
  - h2stats: F06 and F07 shape guards off.
  - compare: F30 rel_fro normalised by ‖a‖; F32 gate_verdict treats a missing "ok" as pass; F34 G1 summary ignores the first window.
  - reduce: F41 α q25 level; F42 E1 corr computed as cov.
  - driver: F53, F54, F55, F56, F59, F60, F61, F62.
  - model: F73, F74.
  - provenance: F80.
  - data: F85.
  - launcher: F90, F92, F93.

**Sample re-check of the r1 survivors**: N26, N53, N11, X09, N59 and W4, using the definitions from the worker's union file. All 6 SURVIVE the shipped 8 test files in full, and all 6 are KILLED by the 4 new files alone. The first failure each time is `test_final_command_reproduces_every_shipped_h2_result_value`.

**Guard probe** (`guard_probe_index_sets.py`, in a copied tree): `topic3h2_stats.py final` ran with rc 0 and wrote labels both when `random_record.json` said that a different index-set file was used (flag False, hash zeros) and when the R subsets were permuted (index-set pairing broken).

**Production-tree suites**
- tests/topic3_h2: 167 passed.
- tests/topic3_spectral: 138 passed.
- `git status --porcelain` on the relevant paths is identical before and after; output_sha256 rc 0; C1 rc 0.

**Ledger**
- The current ledger's first 55484 bytes have sha `9f9843eb…`, equal to the worker's pre-append snapshot, so the file was only appended to.
- M2H2 GPU-h sum: explorers 0.058 + worker 0.458 + verifiers 0.303 = 0.819. Every started row has a completed row.

**Other checks**
- No `sub-` bytes in `results/topic3/2026-11-02_h2` (including inside the npz members), in the H2 docs, or in `verification/worker_M2H2_r2`.
- My probe files contain the prefix only as code literals (mutant strings).
- `audit_layout.py` on the whole run root: findings [] (613 files), rc 0.

## 2. Logic Chain

1. The hashes and the timestamps show that addendum 07 existed, frozen and committed, before any random-init forward pass on real frames. They also show that the code that ran is the code in the repo. So H1′ holds.
2. An independent reimplementation reproduces every label and number from the saved raw arrays. The verdict therefore follows addendum 07 §6 exactly, and the report numbers are correct. H3′ holds for the result. I did not rerun the H2′ replication gate myself: its record values are consistent, and r1 verifiers reran 5 seeds on GPU (for example, `verification/auditor_M2H2_r1_1/seed3_rerun_compare.txt` shows a max relative difference of 0).
3. The r2 claim is that the r1 survivor classes are closed. In my sample, 6 of 6 r1 survivors are killed only by the new files. All 4 new decision-rule mutants and the new verdict-wiring mutants are killed, because the full-output regression test reacts to any change in a shipped value. So the class that failed r1 (label-flipping edits of the verdict path) is closed. CONFIRMED.
4. The 25 survivors all sit in places the golden-master test cannot see:
   - refusal guards for malformed inputs;
   - in-job (connectome) reductions and flags that are never recomputed locally;
   - governance filters of the launcher and collect step.
   None of them can change a shipped number: the shipped code is unmutated and I recomputed the outputs independently. They are coverage gaps beyond the r1 classes, so they are nonblocking under the scope proposed in addendum 08 §7, which follows the PI decision 6 precedent. Two of them, however, contradict the worker's sentence "every guard in the stats script is now tested" (N1).
5. In the E1 erratum, the sentence that names C3 as the label closest to the frozen δ is contradicted by the addendum's own table: C2's boundary (0.458) is nearer to 0.5 than C3's (0.5483). That is N2.
6. The missing index-set guard (N3) is real, but the shipped records carry the card hash. So no result is affected.

## 3. Caveats

- I used no GPU. I did not rerun any seed on connectome. Seeds 2, 5, 6, 9 and 10 have no GPU rerun by any verifier I know of; seeds 1, 3, 4, 7 and 8 were rerun in r1 (I checked only the auditor's seed-3 comparison file).
- I did not rerun the old 86 suite or tests/topic1_lagmotif, because production code is unchanged and C1 rc is 0.
- I did not rerun the worker's 6265 s union harness; I re-checked 6 of its 37 r1 survivors.
- My bootstrap and sign-flip code uses the same RNG algorithm as the frozen primitives, so that exact comparison is possible. An error shared by both in that algorithm would not be visible to me.
- I did not measure the effect of the trunc_normal −2.0 clamp (disclosure D2). The tight per-seed spread at subject level (C3 4.93–5.29) suggests it is small, but this is untested.
- To keep independence, I did not read the r2 peer verifiers' outputs.
- The dispatch makes my structured return the final report, so I sent no SendMessage.

## 4. Conclusion

**CONFIRMED.**
- Gate PASS and the labels (C1 INC, C2 INC, C3 TE+, C4 TE+, Family L as shipped) are correct under addendum 07.
- The card was frozen before the results.
- The numbers reproduce.
- The r1 blocking class is closed.

Nonblocking, for root and the integrated report:
- **N1 — test coverage. Two stats-script guards are still untested, so "every guard tested" is an overclaim.**
  - F20: the `_dump` refusal on BIDS-prefix bytes.
  - F24: `cmd_gate` default `g["G2"] = rec.get("G2", {"ok": False})`. A record without G2 currently gives FAIL, but no test checks this; the G5-missing case is tested.
  - F21 is equivalent, because `verify_pinned` hashes the file first.
  - Also untested: F22 (tolerance), and the job-side and launcher guards (F53–F62, F73, F74, F80, F85, F90, F92, F93). For these, the stats script trusts in-job flags such as `seed_hashes_distinct` without recomputing them.
  - Suggested fix (additive tests only): G2-missing and G1-missing cases in `test_h2r2_stats_guards`; a `_dump` refusal test; local recomputation, in `final`, of hash distinctness from `seed_encoder_sha256`.
- **N2 — erratum precision.** Addendum 08 E1, and the worker's headline, say "the label closest to the frozen δ is C3". By their own table C2 is closer: f 0.458, distance 0.042, against C3 at 0.548, distance 0.048. C3 remains the closest label whose flip would change a verdict-bearing consequence (the R2 "learned" reading). The integrated R1 report should word it that way.
- **N3 — missing guard.** `final` does not check that the random job used the card's index sets (`index_sets_equal_job_generated` or `index_sets_sha256`); I demonstrated this in a copied tree. The shipped hash equals the card J (`cd020fe8…`), so there is no effect on results.

## 5. Verification Method

All commands below use `cd /home/juke/git/00IITP-AI` and the environment `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice`.
- Recompute the labels: `/home/juke/superclaude-env/bin/python3 -I verification/challenger_M2H2_r2_1/independent_recompute.py`. It should print `diffs_vs_shipped: []` and the 24 labels.
- Errata check: `/home/juke/superclaude-env/bin/python3 verification/challenger_M2H2_r2_1/single_seed_and_delta.py` (prints `delta_bounds` and `single_seed_labels`).
- Mutants: first rebuild a copied tree containing src/topic3_h2, src/topic3_spectral, scripts/topic3h2_*.py, scripts/topic3_*.py, tests/__init__.py, tests/topic3_h2, tests/topic3_spectral, results/topic3/{2026-10-31, 2026-11-02_h2} and docs/03_empirical_analysis/topic3. Then run `python3 verification/challenger_M2H2_r2_1/fresh_mutants.py <tree> <0|1> <out.json>`. The trees were deleted after the run.
- Receipts: `LC_ALL=C sha256sum -c` on `results/topic3/2026-11-02_h2/output_sha256.txt`, `addendum_07_sha256.txt`, `r2/addendum_08_sha256.txt` and the C1 file.
- Probe hashes are in `verification/challenger_M2H2_r2_1/logs/probe_sha256.txt`.
- Invalidation: this review is invalid if any pinned output hash, the addendum 07 hash, or the job-recorded code hashes change.
