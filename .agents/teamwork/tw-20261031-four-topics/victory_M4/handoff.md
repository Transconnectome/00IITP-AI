# handoff — victory_M4 (M4 Topic 4 victory audit), 2026-11-01T03:38Z

Verdict: **VICTORY CONFIRMED → VERIFIED_COMPLETE**. Team handoff.md files were not read.

## Observation
- **Protected files and freeze state.**
  - C1 `sha256sum -c sentinel/PROTECTED_HASHES.txt` returned rc 0 (67/67), both at start and after all my tests.
  - The card sha `2b535c39…5934` equals card_sha256.txt.
  - `code_sha256_at_freeze.txt` (sha `3b061f00…83b2`) verifies with rc 0 for all 36 entries (33 code files + qualification, t41 and manifest). The current file list equals the frozen list.
- **Independent full rerun** (tuning → confirm → analyze; fresh cache, then deleted; 03:20–03:31Z, 3 procs, nice, OMP 2) into `verification/victory_M4/rerun/`.
  - All 55 confirm/*.json files are byte-identical to the originals.
  - `verdict.json` is identical (sha `437161ed…5c22`). `tuning.json` is equal apart from elapsed_s, and confirm_summary is identical.
- **Own recompute** (`recompute_victory.py`, which does not import stats/analyze) reproduces:
  - all four point estimates, the class means and the failure counts. Only C3 failed: 10/50 runs (20%), all others 0.
  - every confirm subject (1014) tested exactly once, in its manifest fold; 0 tuning subjects tested.
  - With its own bootstrap (seed 777), every CI lies within MC error of the published one and every verdict is unchanged:
    - H1 = −0.00223, CI [−0.00412, −0.00043] → stop;
    - S1 → killed;
    - S2 = +0.0306 → supported;
    - S3 = −0.00467, CI_lo −0.00504 > −0.01 → non-inferior.
- **Tests I ran** (nice, -p no:cacheprovider, PYTHONDONTWRITEBYTECODE=1):
  - old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed, both plain and with `STRICT_E2E=1`;
  - `tests/topic1_lagmotif`: 88 passed;
  - `tests/topic4_resu`: 67 passed, 0 skipped.
  - The tests/e2e files are all in PROTECTED_HASHES.
- **Mutation harness**, an adapted copy run in my own directory.
  - Control: 63 passed.
  - All 17 worker mutants were killed, and the negative control survived.
  - Of 8 new mutants, 6 were killed: margin widened, guard disabled, PSP fit on test inputs, MLP early stop on test, bootstrap instances not resampled, and C4 mask replaced by ER.
  - 2 survived: `run_psp` drops the monitor, and a global Frobenius rescale inside `fit()`. Both are untested paths; the actual code has neither defect (see Caveats).
- **T4.1.**
  - `topic4_t41_counterfactual.py` rerun output is byte-identical to the original (sha `a8492c8c…f513`).
  - For legacy positions 0–9, the VMD channel-0 cache has 177/464 non-zero rows each. The legacy test-target rows (≥ 325) are entirely padding for all 10.
- **Masks.**
  - C1/C2/C3/C4/C4DP have 69 edges, C5 has 276 and C0 has 0.
  - C4 has 0 designated-hub edges for all 30 seeds, while its top-degree R_hub is ≥ 1.29.
  - C4DP preserves C4's degree sequence and differs from C4 for every seed. The vendored generator equals the protected one.
- **Stability.**
  - All 740 stable PSP runs were monitored on every one of the 6000 updates, with max ρ < 1 (max 0.956) and λ_min > 0.
  - The 10 C3 failures have first-failure steps 45–465 and ρ 1.02–1.56.
  - η0 = 0.02 everywhere.
  - No MLP seed hit the 100-epoch cap: best epochs were 14–48.
- **Timeline.**
  - Manifest 01:52Z, qualification 01:38Z (synthetic), prefreeze tests 02:01Z, card mtime 02:03:57Z, card/code hash files 02:04:41Z.
  - Ledger tuning_start 02:04:52Z logs the card sha, then confirm 02:07–02:14Z, then docs 02:09–02:28Z.
  - Before the freeze, real data were touched only by explorer probes on burned positions 0 and 932 (not TR 2.0). Worker probes and the smoke run were synthetic.
  - No other real-data tuning or ledger file predates the freeze; the later ones are post-run reviewer/challenger copies.
- **C4–C8.**
  - Participant-ID scan: 0 name hits across 22 roots, including the scratchpad derived copies `det/` and `reviewer_M4_r1_1/`. The scan matched bytes only; it did not read the content of other agents' metadata or handoff files. These include results/topic4, docs topic4, every M4 verification directory and every M4 metadata directory.
  - No remote/B300 references in M4 code. No M4 rows in the GPU ledger: 0 GPU-h.
  - Real data are read through mmap/np.load read-only on DGX-Spark only.
  - The report cites legacy numbers only as artefacts.

## Logic chain
- Frozen code plus a frozen card, verified at run start, reproduce bit-identical outputs and verdicts in an independent run.
- My own recompute gives the same point estimates and failure counts and CIs within MC error, so the reported results are genuinely produced by the frozen pipeline.
- The verdict rules in stats.py and analyze.py match card §6 by reading, and their mutants are killed.
- T4.1 is reproduced and extended to all 10 legacy subjects.
- T4.2: the task does not saturate (persistence −0.29, identity ridge 0.15), and the card was frozen before any primary-population outcome.
- T4.3: implementation, fixtures, the stability monitor and the three-part no-autograd proof are all present, with mutants killed; the run and verdict reproduce.
- C1–C8 hold.

## Caveats (nonblocking)
1. **Freeze timing rests on file mtimes, the ledger's card sha at tuning_start, and bit-identical reproduction.** No commit predates the results: the first commit with the card is c967f7c at 02:16Z, after confirm, made by the root checkpoint job. results/topic4 is untracked. This follows from the C4 no-git rule.
2. **Two untested paths, found by surviving mutants.** In both cases the actual code is correct (checked by reading, and the run outputs prove the monitor was active).
   - `pipeline.run_psp` can drop the stability monitor without any test failing.
   - The "no global step" AST test covers only `hebbian_update`. A cross-unit normalisation added in `fit()` would pass.
3. **Stability criterion.** It is ρ(I − D⁻¹M) < 1 of the neuron-local relaxation, equivalent to M being positive definite. That is not literally "spectral radius of M < 1", which ACCEPTANCE gives as an example. The criterion is mathematically sound for symmetric M; I checked the derivation.
4. **Stale wording in the result report and addendum.**
   - δ is called "PI confirmation pending", but PI_DECISIONS item 3 confirms δ = 0.01.
   - The report says "not independently reviewed", but reviewer/auditor/challenger M4 gate agents ran afterwards.
5. **analyze.log hash.** In output_sha256.txt it is the empty-file hash, because the log is the analyze process's own stdout and was written after hashing. The other 72/72 entries verify.
6. **Science notes for the PI.**
   - H1 is a null/negative result ("stop"). C4 is 0.0022 R² worse than ER.
   - The sparse 69-edge classes collapse to rank ≈ 4.5–4.9, so H1 compares collapsed codes under a 6000-update budget that is not fully converged (median relative W change 0.03).
   - S3 is "non-inferior" at margin 0.01, but backprop is significantly better by 0.0047 R².
   - C3 is inconclusive (execution integrity: 20% unstable), although tuning had shown it stable.
   - All CIs omit training-set variability across folds and are anti-conservative; the card declares this.
   - Within-subject acausal preprocessing is shared by every arm, so absolute R² values are optimistic.
7. **Tuning-stage readouts are in-sample.** A gate reviewer reported this and I confirmed it by code reading.
   - `topic4_run.py:153–161` builds tuning sets with test = tune_val, then calls `run_references` / `run_psp` with the default `refit_on_val=True`. The final ridge is therefore refit on tune_train + tune_val and scored on tune_val.
   - The pipeline docstring says the tuning stage uses inner_train only.
   - The G-b values (identity 0.146, persistence −0.308) and the ladder R² are in-sample. The reviewer's clean identity value is 0.1406.
   - No gate, η0 or verdict changes: η0 is chosen by stability only, persistence has no readout, and the out-of-sample confirm identity ridge is 0.1525, far below 0.9.
   - It needs an addendum_02 correcting the "0.146" citations in report §2 and T41 diagnosis D2. None exists yet.
8. **Minor items.**
   - `test_vendored_source_hashes_recorded` is vacuous (disclosed in addendum 7).
   - The split builder skips contract-violating subjects with a count instead of halting. 0 occurred.
   - The src/topic4_resu and local directories have 12:08 KST mtimes, after the run. This is settled by evidence rather than guesswork: my rerun at 03:20Z (12:20 KST, after the 12:08 event) passed `verify_integrity` and reproduced every output byte-identically. The current code is therefore the frozen code. A gate reviewer reports a concurrent-agent `__pycache__`, which is absent now.
   - B300 node time used: 0.

## Claims comparison
After recording the verdict at 03:38Z, I read worker_M4_r1/progress.md and handoff.md and skimmed the M4 gate handoffs: reviewer ×2 APPROVE, auditor CLEAN, challenger ×2 CONFIRMED, with no blocking items. Every claimed number matches my independent results:
- tests: 67 / 86 / 88;
- mutants: 17/17 killed, control survives;
- verdicts and CIs;
- C3 10/50 unstable, steps 45–466;
- tuning max ρ 0.934 and η0 0.02;
- verdict.json sha 437161ed…;
- 0 GPU-h;
- positions touched before the freeze: 0 and 932 only.

## Verification method
Rerun with `verification/victory_M4/rerun_full.sh`, then:
- `cmp` the confirm files;
- `recompute_victory.py <dir> <out>`;
- `mutants/run_mutants_victory.py`;
- the pytest commands above;
- `t41_counterfactual` → cmp;
- `t41_positions_0_9.py`, `check_masks.py` and `id_scan.py`.

Logs and outputs are in `verification/victory_M4/`.
