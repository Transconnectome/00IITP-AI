# Handoff — reviewer_M2_r1_2 (Hard handoff, 2026-10-31T11:30Z)

## Review Summary
**Verdict: APPROVE.** M2 (Topic 3, T3.1–T3.4) meets C1–C8 with independent evidence. One Major finding is non-blocking: a test-coverage gap in the verdict-bearing replication rule. Two Minor findings and a run-level C4 observation go to root.

Probe dir: /home/juke/git/00IITP-AI/verification/reviewer_M2_r1_2/r2_1117/

## 1. Observation
- **C1.** `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: rc 0, 67 OK, 0 non-OK, both at start (c1_start.log) and at end (c1_end.log).
- **Pins.**
  - `output_sha256.txt`: rc 0, 42 entries OK, at the end, after the in-tree pytest runs.
  - `addendum_02_sha256.txt`: OK.
  - `code_sha256_at_freeze.txt`: all OK except `scripts/topic3_launch_connectome.py`, which is disclosed in addendum 01 item 2.
  - Card sha256 683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0 equals card_sha256.txt (frozen 08:48:29Z).
- **Tests** (PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=repo):
  - tests/topic3_spectral: **54 passed** in 571 s.
  - C2 explicit list (tests/test_empirical_four_topics.py, tests/test_pilot_connectome.py, tests/e2e; STRICT_E2E=1): **86 passed**.
  - tests/topic1_lagmotif: **88 passed**.
  - Logs: pytest_*.log.
- **Freeze before results (C3).**
  - Run records: family_A started_utc 08:49:18Z; token job task 0 started 08:51:32Z; family_B 09:01:59Z. All are after the freeze at 08:48:29Z.
  - Family A and B run records carry card_sha256_verified = 683374565d….
  - t3_1_provenance_repro (pre-card) reproduces only published numbers; card §1 and §11 disclose this.
  - alpha calibration is synthetic only.
- **Frozen code produced the outputs.**
  - The code_sha256 maps in family_A and family_B (8 files each) and in all 4 token_job JSONs (7 files each) match code_sha256_at_freeze.txt, with 0 mismatches.
  - Token job seed is 20261031.
  - The sbatch runs the frozen `scripts/topic3_token_job.py` on the 4 card-listed frame roots, with --check-npz-root for the primary.
- **Full independent rerun** in a copied tree (each <2.5 min CPU): alpha calibration, Family A, Family B and provenance repro.
  - Compared with compare.py (skips timing and host fields).
  - Result: **0 value diffs** for all four. Provenance differs only in 3 absolute-path strings. all_report_numbers_reproduced = all_json_numbers_reproduced = True.
  - Saved in rerun_outputs/.
- **Remote spectra internal consistency** (npz_consistency.py). Per-subject covPR recomputed from the stored cat_cov_eigs equals the stored cat_covpr. Max relative error is ≤ 4.3e-8 across all 4 checkpoints × 5 variants.
- **Verdict logic vs card §4–§5** (read analysis.py and resampling.py; extracted from the JSON):
  - D1: cov [3.22, 7.46], corr [4.28, 7.80], i.e. "robust and not per-channel scale".
  - D3: both intervals have lo > 0.
  - H1a: primary +0.023 [0.021, 0.025], Holm 0.0002. Zoo: HCP −0.137, L1e-4 +0.038, L5e-5 +0.049, all Holm 0.0002. So 2 of 3 zoo agree, and H1a **holds**.
  - H1b: primary +0.045. Zoo: −0.113, −0.033, +0.079. Only 1 of 3 agrees, so H1b is **not replicated**.
  - A1b: all 4 checkpoints have hi < 0.
- **Mechanism claim (R2)** in ver11 (sha de132387…052a):
  - BasicLayer.forward (914–923) runs the blocks, then downsample.
  - Line 1068 sets downsample=None for the last stage.
  - The hook (1382–1412) applies self.norm only after the last stage.
  - So no merge sits between the layer_2 and layer_3 dumps. Verified.
- **Addendum 02 zoo table.**
  - VRABES extract_vrabes_swift_zoo.sh line 48: HCP_N400_T2400_E192 is `2 2 18 2`, last.pt, L2e-5.
  - Lines 54–55: deepE192 is `2 2 42 4`, EP10.pt / best.pt.
  - extract_vrabes_swift_E192.sh line 35 (ckpt) and line 82: `--depth 2 2 18 2`.
  - Verified.
- **Old PR function.** src/spectral_rg_flow_diagnostic.py:55–64 takes the SVD of the uncentered X. Verified.
- **C4 IDs.** I loaded the 57 real IDs in memory (shape aaa-####, never printed) and scanned 997 files: results/topic3, docs/topic3, src/tests/scripts, verification/worker_M2_r1 and the worker metadata.
  - Full-form hits: **0**.
  - The 4-digit stripped forms hit only inside floats and hashes (masked context shown in id_scan2 output), so they are false positives.
- **Mutants** (reviewer, on the copy):
  - R1 replication-ignores-sign: **SURVIVED** (5 passed).
  - R2 sign-flip one-sided: killed.
  - R3 Clauset missing +1: killed.
  - R4 subsample SE shrunk to sd/√S: killed.
  - The worker's own 9 mutants: all killed (verification/worker_M2_r1/mutants.out.json).
- **Git.** HEAD 7497e6a at 2026-10-31 20:16:25 +0900, "docs(iitp): checkpoint four-topics teamwork documents (16 files) — Automatic background checkpoint". Commits come at a 15-min cadence (17:46, 18:01, 18:16, 20:01, 20:16 KST). The committed addendum_02 equals the working copy.
- **VRABES.** `git status --porcelain` is empty, and no files in VRABES or SwiFT_v2 are newer than run start.
- **GPU.** No GPU use; `results/gpu_ledger_2026-10-31.md` does not exist.

## 2. Logic Chain
1. **T3.1.** Inputs are located and pinned; provenance is documented (provenance note plus ver11 lines I verified). The PR≈1 artefact is reproduced to 4 decimals and explained by the uncentered SVD I verified. The centering fixture fails on the old function. **Met.**
2. **T3.2.** The card holds hypotheses, estimators (centered covPR/corrPR, α_rank and Clauset with method and citation), controls (iid reference, column-permutation null, checkpoint replication; random-init pre-specified but deferred) and decision rules. It was frozen before every governed real-data quantity (run-record timestamps and card hash). **Met.**
3. **T3.3.** Fixtures cover:
   - known rank → PR = k to 1e-9, plus analytic unequal spectra;
   - α_rank exact on exact laws, Clauset recovering a Pareto exponent within 0.05;
   - centering defect caught (old function < 1.1).
   Mutants of these are killed (worker M1/M5/M8; reviewer R3). **Met.**
4. **T3.4.** The rerun on real representations reproduces bit-for-bit in value from the pinned inputs. Dated outputs and the report exist. Each old claim J1 and R1–R7 has a verdict that follows the frozen rule (checked against the JSON). No GPU was needed. **Met.**
5. **Remaining C criteria.**
   - C2: met (86 / 88 / 54).
   - C4: met for IDs and for no M2 commits. The background commits come from the root session, not from M2.
   - C5: met (0 GPU-h).
   - C6: met (nothing to B300; ENIGMA unused; frames stayed on connectome).
   - C7: met (VRABES clean).
   - C8: met (the report cites old numbers only as claims under test).
6. **R1 survival.** The verdict-bearing sign condition is untested. On the real data, a regression that dropped it would turn H1b into "holds" (3 of 3 zoo significant, 2 of them with the opposite sign) without any test failing. The shipped code is correct and the outputs reproduce, so this is not a wrong result. It is Major and non-blocking.

## 3. Caveats
- I did not recompute the token spectra on connectome from the raw frames. Remote correctness rests on three things: (a) frozen code hashes in the job records; (b) the job's own re-pool provenance check (max |Δ| 4.8e-7); (c) my check that covPR is internally consistent with the stored eigenvalues.
- Zoo depth, LR and file attributions come from VRABES scripts, not from NERSC logs (as addendum 02 says).
- The subsampling SE sd·√(m/(n−m)) is a card-fixed heuristic. It is conservative here (≈0.98 sd at m = 28, n = 57), and the card labels the result a stability interval, not a CI.
- H2 (random-init) is untested, as disclosed. The 7 pytest warnings in the old suite were not inspected; they are pre-existing.
- I ran one `git show --name-only` piped to grep topic3. It printed only one topic3 doc path. I will not repeat it, given the repo rule on participant-ID paths.

## 4. Conclusion
**APPROVE M2.** Non-blocking items for root:
- **(Major)** Add a replication-rule fixture with significant opposite-sign zoo checkpoints. As a new test file it does not touch pinned files; record it in a dated addendum.
- **(Minor)** Addendum 02's safe-reproduction copy list omits `docs/03_empirical_analysis/empirical_results.json` and `tests/__init__.py`. provenance_repro fails in a copy without the first.
- **(Minor)** The GPU ledger file is absent. M2 = 0 GPU-h; the ledger owner should record it.
- **(Observation, run-level C4)** Automatic 15-min background git commits from the root session (latest 7497e6a, 20:16 KST) conflict with the C4 "no git commit" text. Root should confirm that authority. This is not an M2 defect.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # rc 0, 67 OK
sha256sum -c results/topic3/2026-10-31/output_sha256.txt                                       # rc 0
sha256sum -c results/topic3/2026-10-31/code_sha256_at_freeze.txt                               # only launcher differs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_spectral -q
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_M2_r1_2/r2_1117/npz_consistency.py
# Rerun: copy src/ scripts/ tests/{__init__.py,topic3_spectral} docs/03_empirical_analysis/{topic3,empirical_results.json} results/topic3/2026-10-31
# to a temp tree, run scripts/topic3_*.py there (not the launcher), compare with verification/reviewer_M2_r1_2/r2_1117/compare.py.
# Mutants: mutants_rev.py expects that tree at ./tree (removed after use).
```
**Invalidation conditions:**
- any pinned hash fails;
- a rerun gives value diffs;
- a full-form ID appears in outputs;
- the card hash changes.
