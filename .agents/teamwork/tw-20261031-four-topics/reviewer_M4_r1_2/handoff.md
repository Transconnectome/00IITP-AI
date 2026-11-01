# Handoff — reviewer_M4_r1_2 (M4 / Topic 4 independent review), Hard handoff, 2026-11-01

Verdict: **APPROVE** (no blocking issue; 6 non-blocking issues listed in section 4). Reviewer verdicts are advisory; the gate decision belongs to the PI (sci-pipeline section 2/6).

## 1. Observation
All commands were run by this reviewer from 02:35Z to 02:55Z. Logs and probe outputs are in `/home/juke/git/00IITP-AI/verification/reviewer_M4_r1_2/`.

**C1 protected hashes.** `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gave rc 0 with 67/67 OK at 02:35Z (`c1_protected_start.log`) and again at the end (`c1_protected_end.log`).

**Freeze hashes.** `sha256sum -c` passes for:
- `results/topic4/2026-11-01/card_sha256.txt` (1 entry);
- `code_sha256_at_freeze.txt` (36 entries);
- `docs_sha256.txt` (13 entries);
- `split_manifest_sha256.txt` (run from `results/topic4/2026-11-01/`, because the path is relative).

The card is mode `-r--r--r--`. The committed copy of the card in root checkpoint `c967f7c` (02:16Z) hashes to the frozen value 2b535c39…5934, and the card is absent from the 02:01Z checkpoint `fa84b7d`. The freeze list covers all 33 files under `src/topic4_resu`, `tests/topic4_resu` and `scripts/topic4_*.py`, plus qualification, t41 and the manifest.

**`results/topic4/2026-11-01/output_sha256.txt` fails `sha256sum -c` (rc 1).**
- Only `logs/analyze.log` fails. Its pinned value is e3b0c442…b855, the SHA-256 of an empty file.
- mtimes: `output_sha256.txt` 11:15:04.998 KST, then `analyze.log` 11:15:05.006 KST.
- The log content equals the H1–S3 block of `verdict.json`.
- The other 72 entries verify.

**Tests (my runs):**
- `pytest -p no:cacheprovider -q tests/topic4_resu`: 67 passed, 0 skipped (`tests_topic4.log`);
- `STRICT_E2E=1 pytest -q tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`: 86 passed (`tests_old86.log`);
- `pytest -q tests/topic1_lagmotif`: 88 passed (`tests_topic1_lagmotif.log`).

**T4.1.** Every legacy line the diagnosis cites matches the protected source:
- `src/fractal_motif_resu.py` :301–302, :347, :349–352, :371, :377, :417, :425, :432, :480 and :544;
- `src/run_all_empirical_experiments.py:47` (`n_subjects_t4 = 10`);
- `src/rg_box_pooling.py:26` (`import torch`).

My own count of VMD-cache valid rows for burned positions 0–11 gives 177 valid rows each, with 0 test-target rows inside the valid portion at split 324 (`t41_positions_0_11_padding.out.json`, counts only). This closes the "every legacy subject" claim, which the counterfactual itself showed only for positions 0 and 932. `results/topic4/2026-11-01/t41_counterfactual.json` matches the diagnosis table: pos 0 R² is 1.0 for all six conditions with ss_tot 2.5e-45; pos 932 R² runs from −0.082 to 0.053 and persistence scores 0.992.

**Access history.**
- Explorer probes touched real data only at positions 0 and 932: `probe_c_real.py` uses `POSITIONS = {0: 1.8, 932: 1.0}`, and `probe_a_t41_counterfactual.py` uses `[0, 932]`.
- The survey touched positions 0–4.
- The worker probes 1 and 2 and the smoke run are synthetic.
- None of these positions has TR 2.0. The manifest has `burned_positions_in_primary = []`.

**Split.** I re-derived the split with my own code from the card rule (salted sha256 rank within site, 15% tuning, round-robin folds, burned positions excluded). The result equals the manifest. Every `position_hash` matches. The confirm files' test positions equal the manifest folds. All 1014 confirm subjects are tested exactly once, and no tuning subject appears in any test fold (`indep_verdict_recompute.out.json`).

**Ledger.** `run_ledger.jsonl` has 58 rows: tuning_start, tuning ok, confirm_start, and 55 tasks, all ok. Every task's `output_sha256` matches its file. tuning_start (02:04:52Z) comes 11 s after the freeze (02:04:41Z), and both start rows record the frozen card, code-list and manifest sha. Only C3 has unstable runs: 10/50, at first-failure steps 45–465 with ρ 1.02–1.56.

**Independent verdict recompute.** `indep_verdict_recompute.py` imports neither `src.topic4_resu` nor the analysis script, and uses its own crossed bootstrap with seed 777 and B = 4000. All four point estimates match `verdict.json` to < 1e-12, and all four verdicts are the same:

| contrast | point | my CI | worker CI | verdict |
|---|---|---|---|---|
| H1 | −0.00223 | [−0.00415, −0.00040] | [−0.00413, −0.00042] | stop |
| S1 | −0.00160 | [−0.00364, 0.00055] | [−0.00384, 0.00053] | killed |
| S2 | 0.03062 | [0.02883, 0.03241] | [0.0288, 0.03242] | supported |
| S3 | −0.00467 | [−0.00502, −0.00428] | [−0.00503, −0.00426] | non-inferior |

The descriptive class means match to 0.0. 87.7% of subjects have C4 < C1, and 12 of 13 sites have a negative mean difference.

**Analysis determinism.** `scripts/topic4_analyze.py --outdir <scratch copy>` (7 s) gives a byte-identical `verdict.json` (437161ed…5c22).

**Fold-0 rerun from production code** (`rerun_fold0.py`; data in memory only, nothing written to results/, 1 process, OMP_NUM_THREADS = 2). Every R² array, engine digest and stability flag is bit-identical to the stored fold-0 confirm files:
- refs: 30/30;
- C0: 20/20;
- C1: 60/60;
- C2: 60/60;
- C3: 16/16, and its 2 unstable runs reproduce as unstable;
- C4: 60/60;
- C4DP: 60/60;
- C5: 20/20;
- MLP seeds 0, 1 and 2: 3/3 each, with the same digests and the same grid selection.

`all_bit_identical` is true, max |Δ| is 0, every λ choice matches, and the run took 736 s (`rerun_fold0.out.json`).

**Mutation harness.** I reran the worker harness from a byte-identical copy (sha 89e23077…c9e3) in `verification/reviewer_M4_r1_2/mutants_rerun/`. The control passes 63 tests. All 17 mutants are killed, and the negative control `CONTROL_targets_wired_but_unused` survives as designed. Each log shows a targeted assertion failure rather than an import or setup error.

**My extra mutants** (`my_mutants.py`, applied to copies):

| mutant | result | caught by |
|---|---|---|
| `lambda_selected_on_test` | KILLED | `test_train_only` |
| `engine_fit_on_train_plus_test` | KILLED | `test_train_only` |
| `failed_runs_imputed_zero` | KILLED | `test_stats` |
| `global_frobenius_rescale_in_fit` (W ← W / max(1, ‖W‖_F / 3) inside `MaskedPSP.fit`) | **SURVIVED** (25 passed) | — |

The control passes 26 tests.

**Participant IDs.** My scan (`id_scan.py`) loaded the 1706 directory names into memory only and checked 315 files: src, tests and scripts for Topic 4, `results/topic4`, `docs/topic4`, the worker, explorer and reviewer verification dirs, and the M4 metadata dirs. It found 0 ID hits. The two `sub-` hits are the scanner's own pattern literal and a prose sentence in `explorer_M4_r1_2/handoff.md`.

**Compute and data governance.**
- `results/gpu_ledger_2026-10-31.md` has M3 rows only, no M4 rows, so 0 GPU-h for M4.
- M4 code contains no `ssh`, `scp`, `rsync` or B300 address.
- No `*.dist-info` in `superclaude-env` is newer than the run start, so nothing was installed.
- No file under `enigma_ocd_mbbn/data` changed since 09:00 KST. The only newer files in that repo are `experiments/.job_status`, `logs/coordinator.log` and `.git`, which belong to another workstream. M4 code opens that data read-only (`np.load(mmap_mode="r")`, `memmap mode="r"`, `pandas.read_csv`).

## 2. Logic Chain
1. C1: rc 0 at the start and the end, so no protected file changed.
2. C2: 86, 88 and 67 tests pass on my runs.
3. C3: the card was frozen at 02:04:41Z.
   - The sidecar, the chmod, the ledger start rows and the root checkpoint bytes agree.
   - All code is in the freeze list, and its files are older than the freeze.
   - The first real-data run of the card's population is tuning at 02:04:52Z.
   - Pre-freeze real-data touches were at non-TR-2.0 burned positions only.
   - The synthetic fixtures fail on the targeted defects: the worker's 17 mutants and my 3 extra kills.
   - Raw logs are present. Deviations are in a dated addendum, and the card is unedited (sha matches).
4. C4: 0 ID hits, no installs, and no git writes by me (only `git --no-optional-locks log` and `show`, which are reads).
5. C5: 0 GPU-h, local CPU only, and no ledger rows needed.
6. C6: no B300 path in the code; ENIGMA data used on DGX-Spark only.
7. C7: no changes in external repos attributable to M4.
8. C8: the result report takes numbers only from `results/topic4/2026-11-01`; the legacy numbers appear only in the T4.1 diagnosis, as the artefact being explained.
9. T4.1 is met:
   - the counterfactual uses the unmodified protected function;
   - my count shows that all positions 0–11 have a fully padded test window;
   - the mechanism is the `max(ss_tot, 1e-8)` floor at :425, with a falsification at pos 932;
   - there are fixtures F1–F4 with killed mutants.
10. T4.2 is met:
    - the task does not saturate (persistence −0.286, identity ridge 0.153 on confirm; tuning gate G-b passed);
    - the card fixes the conditions C0–C5 and C4DP, a backprop MLP-24 baseline with grid and seeds, the per-subject guarded R² metric, the seeds, B = 2000, and the kill rules with δ.
11. T4.3 is met:
    - stability ρ(I − D⁻¹M) < 1, equivalent to λ_min(M) > 0 for symmetric M with positive D, is monitored after every update and has fixtures;
    - no autograd: the AST check, the torch/jax runtime block and target invariance each pass and each kills its mutant;
    - the CPU run completed 55/55;
    - the verdicts follow the card rules, as two independent recomputes show;
    - the stored outputs are reproduced bit-for-bit from code and data for fold 0.
12. No integrity violation: there are no hard-coded results, no facade implementation and no fabricated receipts. The receipts reproduce from code and data.

## 3. Caveats
- **Fold 0 only.** I reran only fold 0, the 11 tasks that cover every arm group, not folds 1–4. Folds 1–4 are covered by the ledger output hashes and the consistent statistics, not by a re-execution.
- **B300 not checked from B300.** Absence of B300 contact rests on the code paths and the GPU ledger.
- **No sci-pipeline `pipeline-reviewer` agent.** Nested spawning was unavailable. This review uses the sci-pipeline gate list directly.
- **Scientific scope.** The "Mode II" hypothesis is tested only under one linear PSP rule with a 6000-update budget; the engine is not fully converged (median relative ΔW 0.03). With this engine, the topology effect largely tracks the rank of the learned map. The kill applies to this operationalisation, as card sections 7 and 9 state.
- **δ = 0.01 is analyst-set.**
  - H1 is stop for any δ > −0.0004.
  - S1 stays "killed" only for δ > 0.0005.
  - S3 is "non-inferior" only for δ > 0.0050.

## 4. Conclusion
**APPROVE M4.** T4.1, T4.2, T4.3 and C1–C8 are met with evidence.

Non-blocking issues, all recommended for a dated addendum_02 (none changes a verdict):
1. **`output_sha256.txt` fails verification.** The `logs/analyze.log` entry is the empty-file hash, from a race between the shell redirect and the hash step. This was not disclosed, and the worker's verification method never checked this file. Fix: note it in an addendum and write a new pin file. Do not overwrite the existing one.
2. **Locality guard gap.** The "no global step" claim is enforced only inside `hebbian_update`; a global rescale in `MaskedPSP.fit` passes every test. The no-autograd proof (the T4.3 requirement) is unaffected, and I confirmed by reading `psp.py:99–132` that the current code has no global step. Fix: extend the AST check to `fit()`, allowlisting the post-loop convergence `norm`.
3. **Contract handling differs from the card wording.**
   - `scripts/topic4_build_split.py` excludes and counts contract violations instead of halting.
   - A firing R² guard halts only its task (`status halt_degenerate_target`), not the whole run.
   - Both are moot here, since there were 0 contract errors and the guard never fired. The card's wording "halts, never repairs" should match the code.
4. **Vacuous test.** `test_vendored_source_hashes_recorded` is vacuous; this was already disclosed in addendum_01 item 7.
5. **`split_manifest_sha256.txt` path.** It uses a path relative to the results dir, unlike the other pin files, which are relative to the repo root. `sha256sum -c` must be run from `results/topic4/2026-11-01/`.
6. **No pre-result commit.** No commit made before the results captured the card; agents may not commit, and the root checkpoint captured it after confirm. The freeze evidence is the sidecar, the chmod, the ledger and the later commit with identical bytes. The PI may want a protocol-before-results commit policy for future cards.

Items for the PI (not T-criteria):
- confirm δ;
- make the gate decision;
- note that S3 "non-inferior" does not mean equivalent: backprop is significantly better, by 0.0047.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?          # 0
LC_ALL=C sha256sum -c results/topic4/2026-11-01/{card_sha256.txt,code_sha256_at_freeze.txt,docs_sha256.txt} | grep -vc ': OK$'   # 0
(cd results/topic4/2026-11-01 && LC_ALL=C sha256sum -c split_manifest_sha256.txt)                                          # OK
LC_ALL=C sha256sum -c results/topic4/2026-11-01/output_sha256.txt | grep -v ': OK$'                                        # analyze.log FAILED (non-blocking 1)
/home/juke/superclaude-env/bin/python3 -B verification/reviewer_M4_r1_2/indep_verdict_recompute.py                          # all_verdicts_match true
/home/juke/superclaude-env/bin/python3 -B verification/reviewer_M4_r1_2/rerun_fold0.py                                     # all_bit_identical true (~11 min, 1 proc)
cd verification/reviewer_M4_r1_2 && /home/juke/superclaude-env/bin/python3 -B my_mutants.py                                # global_frobenius_rescale_in_fit survives
```
The conclusion is invalidated if any of the following holds:
- any hash check above other than `output_sha256.txt` fails;
- `rerun_fold0.out.json` reports `all_bit_identical` false;
- any card, code or result file changes after this review (re-review required).
