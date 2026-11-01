# Handoff (Hard): reviewer_M2H2_r1_1, milestone M2H2 (Topic 3 random-init control H2)

**Verdict: APPROVE.** H1′, H2′, H3′ and C1–C8 are met, with evidence. There are no blocking issues. There are 7 nonblocking issues; the first one needs a PI decision.

## 1. Observation

- **C1.** `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` returns rc 0 on all 67 entries, at 17:0xZ and again at 17:18Z (`verification/reviewer_M2H2_r1_1/c1_protected.log`).
- **Receipts.**
  - `results/topic3/2026-11-02_h2/output_sha256.txt`: 61/61 OK.
  - `addendum_07_sha256.txt`: OK.
  - `results/topic3/2026-10-31/` addendum_02…06 and output_sha256: rc 0.
  - `card_sha256.txt` returns rc 1 because of its trailing "frozen …" token. This is pre-existing. The hash itself, 683374565d80…, matches the card.
- **Freeze ordering.**
  - The addendum 07 sha is 09b45220…dd84b. Its mtime is 15:57:27Z; the receipt time is 15:57:40Z.
  - Independent evidence: autosnapshot commit 35d10a5 (2026-11-01T16:05:25Z) contains the same bytes (checked with `git show`).
  - Gate job 218063 started 16:22:20Z and gate_decision PASS was written 16:31:46Z. Random job 218064 was submitted 16:32:19Z and started 16:32:21Z.
- **Code identity.** The `code_sha256` maps in gate_record.json and random_record.json (20 files each) equal the current repo bytes. All 24 returned files on connectome (`returned_gate_218063`, `returned_random_218064`) are byte-identical to the local results.
- **Independent recomputation.** `verification/reviewer_M2H2_r1_1/recompute_h2.py` uses its own PR estimators, its own arithmetic for combining arms and its own decision rule; it reuses only the frozen sign_flip / bootstrap / holm. Results:
  - The δ values equal the card.
  - T's A1 L2−L3 reproduces the pinned Family A: point 5.343854531111 / 6.038808669990; SE 1.081055126275 / 0.899082569300.
  - All 24 endpoints (C1–C4, 10 L-tok, 10 L-sub) match the shipped point, CI95 and CI90 within 1e-6, and match the labels. Mismatches: [] (`recompute_h2.out`).
- **Independent connectome rerun.** Slurm job 218066 ran on node1 debug, 1 GPU, 234 s, 0.065 GPU-h, with start and closing ledger rows under flock.
  - It used a code bundle I built (sha bb28fd39…) in my own dir `/home/connectome/connectome1/iitp4_m2h2/reviewer_M2H2_r1_1/`, with the worker venv used read-only.
  - It ran seed 7 alone, so the RNG state is not shared with the other seeds.
  - Its R7_scalars.npz and R7_subsets.npz are **bitwise identical** to the shipped files (equal sha256). The seed 7 encoder hash e64602ca… is equal, the rebuild of the same seed is identical, and the index sets are equal.
- **Tests.**
  - `tests/topic3_h2`: 71 passed (rc 0).
  - Old suite (STRICT_E2E): 86 passed.
  - `tests/topic3_spectral`: 138 passed.
  - `tests/topic1_lagmotif`: 88 passed.
- **Mutation.**
  - The worker's 32 mutants are recorded as all KILLED (`verification/worker_M2H2_r1/mutants.out.json`).
  - My 12 extra mutants (`rev_mutants.py`, copied tree, clean baseline 47 passed): 8 KILLED (X01, X02, X03, X05, X07, X08, X11, X13) and 4 SURVIVED:
    - X04: `topic3h2_stats.py final` ignores a gate FAIL;
    - X09: the descriptive per-seed D1 rule;
    - X14: the index-set seed +100 → +101;
    - X15: the strict TE− seed boundary.
- **Data governance.**
  - No "sub-" bytes in any file under results/topic3/2026-11-02_h2 or in the H2 docs.
  - No string arrays in the npz files.
  - The returned npz files hold position-keyed scalars and per-index-set PRs only.
  - No `work_*` dir remains on connectome; the remote dir is mode 700.
- **Gate details** (gate_record.json):
  - G1: 399 windows, 0 failing cells; max rel_fro 6.5e-7 / 7.4e-7 / 7.8e-7 / 7.3e-7.
  - G2: re-pool max 7.0e-7; pins OK; row order OK.
  - G3: max relative difference 7.3e-8; dropped counts equal; H1a/H1b sign and CI status equal.
  - G4: checkpoint sha OK; 0 missing encoder keys; the only unexpected key is augment_comp.smooth_kernel.
  - G5: all 3 controls fail in 84/84 cells (min rel_fro 4.6e-4 to 1.5).
- **Ledger.** It has start and closing rows for 218063 and 218064 (0.135 and 0.323 GPU-h). Their closing rows record sacct KST times, labelled KST, in the UTC column.
- **Layout lint.** `audit_layout.py` on the run root returns PASS: 447 files, findings [].
- **δ sensitivity**, computed from h2_results.json. TE+ holds iff δ < min(lo95, min seed effect):

| Endpoint | TE+ holds while δ is below | As a fraction of the trained effect |
|---|---|---|
| C1 | 0.00358 | 0.158 |
| C2 | 0.02046 | 0.458 |
| C3 | 2.930 | 0.548 |
| C4 | 4.007 | 0.664 |

## 2. Logic chain

1. **H1′ is met.** Addendum 07 freezes the hypothesis, the arms, K=10 seeds, the init law, the frozen estimators (imported unchanged; code hashes are equal), interval types, δ, the decision rule and its truth table, and the consequences. Its sha was committed by an independent daemon at 16:05Z, before any random-init forward (16:32Z). (Observations: freeze ordering, code identity.)
2. **H2′ is met.**
   - The replication gate ran on all 57×7 windows element-wise before the random arm. The launcher refuses `--arm random` without a PASS record (scripts/topic3h2_connectome.py lines 158–165).
   - The 3 negative controls fail by margins 46× to more than 10⁵× the tolerance.
   - The pipeline runs in a project-local venv under Slurm on connectome, and frames stayed there.
   - My bitwise seed-7 rerun shows the random-arm aggregates are genuine, deterministic outputs of the repo code. This excludes fabrication or hand-editing.
3. **H3′ is met.** There are 71 tests, with fixtures on the real network (a closed-form PR, the iid and static-input ceilings, comparator perturbations, frame order) and decision-rule cells. Results are in the dated dir. The report states the H2 labels and maps each of R1–R3 through the frozen consequence table. My recomputation reproduces every label.
4. **C2–C8 are met.**
   - C2: all suites pass.
   - C3: the card was frozen before results, there are synthetic fixtures and raw redacted logs, and the pre-run deviations are in addendum 07 §12.
   - C4: no IDs.
   - C5: ledgered, 0.581 of the 6 GPU-h cap including my 0.065.
   - C6: connectome only.
   - C7: vendored byte copies; external repos untouched.
   - C8: only dated outputs are cited.
5. **The surviving mutants do not change the verdict.** My independent recomputation fixes the shipped labels. X14 is also caught at runtime by the stats script's T-A1 halt and the in-job index-set equality. X04 is moot because the gate passed.
6. **δ needs PI confirmation, but it does not block.** δ was frozen before results, and PI decision 8 delegated the rule to the addendum. sci-pipeline (SKILL.md line 67) names δ as a PI-only choice, though. Three of the four primary labels change within δ ∈ [0.46, 0.55]× the trained effect, so this is the most important item for the PI. The report's limitation item 1 says only that C1 and C2 would change, which understates how much the labels depend on δ.

## 3. Caveats

- I did not rerun the gate job (R0 + controls). G1, G2, G4 and G5 rest on in-job records. They are consistent with the explorer smokes, with the local G3 recheck (5.6e-8), and with my R0-vs-T subset check (6.4e-7). My seed-7 rerun shows the pipeline is deterministic.
- I reran only one random seed. The other nine are trusted through the identical code hashes and the bitwise match for seed 7.
- My rerun used the worker's venv read-only, so it is an independent code and run path but not an independent environment.
- I cannot fully prove the absence of git writes by the worker. I saw no evidence of any.
- The mutant subset excludes the slow driver/model tests.

## 4. Conclusion

**APPROVE M2H2.** Blocking issues: none.

Nonblocking issues, with recommended actions:

1. **(PI decision) δ.** The worker set δ, and sci-pipeline treats it as PI-only. The labels depend on it: C2 is TE+ for δ < 0.458×, C3 flips to INC for δ ≥ 0.548×, C4 flips for δ ≥ 0.664×, and C1 is TE+ only for δ < 0.158×. Bring this table to the PI with the δ question. Record the full sensitivity in a new dated addendum or in the integrated report (R1). Do not edit addendum 07.
2. **Report §5, R1 row.** It says the "expansion cannot be read as a training product". The trained−init difference is −1.61 [−3.77, +0.56] (cov) and −0.74 [−3.18, +1.71] (corr). This goes beyond the frozen "stays descriptive" consequence. Reword it as descriptive, with the CI.
3. **Report §3 and §4 call R0 values "trained"** (E1 2.78 / 11.02 / 3.58; α medians), while card §2 says R0 is never substituted for T. The numerical effect is ≤ 6.4e-7. Relabel the values as R0, or use the pinned T values.
4. **Ledger closing rows 218063 and 218064** carry KST times in the UTC columns (labelled KST). Append correction rows; do not edit the existing rows.
5. **Test gaps (X04, X09, X14, X15 survive).** Add tests for: `final` refusing a gate FAIL; the strict TE− seed boundary; the card's index-set seed; and the per-seed D1 rule.
6. **Connectome cleanup after audit.**
   - `/home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/` (venv about 5 GB);
   - `explorer_M2H2_r1_1/` and `_2/`;
   - my dir `/home/connectome/connectome1/iitp4_m2h2/reviewer_M2H2_r1_1/` (code bundle including the pinned trained spectra npz, logs and returned aggregates; no work dir).
7. **Pre-existing:** the card_sha256.txt format returns rc 1.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/addendum_07_sha256.txt
git show 35d10a5:docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md | sha256sum   # 09b45220…
cd verification/reviewer_M2H2_r1_1 && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=/home/juke/git/00IITP-AI nice /home/juke/superclaude-env/bin/python3 recompute_h2.py   # MISMATCHES: []
sha256sum verification/reviewer_M2H2_r1_1/connectome_seed7/returned/R7_*.npz results/topic3/2026-11-02_h2/random/R7_*.npz   # pairs equal
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_h2 -q   # 71 passed
cd verification/reviewer_M2H2_r1_1 && /home/juke/superclaude-env/bin/python3 -I rev_mutants.py   # 8 killed / 4 survived
```

The approval is invalidated if any of the following happens: addendum 07 or any receipt fails; a random-arm npz differs from a rerun; recompute_h2.py reports a mismatch; or the PI sets a δ that moves a label, which would need a new dated addendum and would then be reported alongside the current labels.
