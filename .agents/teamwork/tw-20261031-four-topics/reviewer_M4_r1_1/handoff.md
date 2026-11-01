# Handoff — reviewer_M4_r1_1 (M4 / Topic 4 redesign review), Hard handoff, 2026-11-01T02:52Z

**Verdict: APPROVE** (every T4.1–T4.3 and C1–C8 item is met with evidence I produced myself; 7 non-blocking issues, one of which needs an addendum line before the PI quotes the tuning value). The PI makes the gate decision (sci-pipeline §2); this verdict is a recommendation.

## 1. Observation
All probes are in `/home/juke/git/00IITP-AI/verification/reviewer_M4_r1_1/`. All commands ran with PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2 and nice, on at most 4 local processes, using CPU only. I did not touch B300.

- **C1**: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` returned rc 0 at 02:37Z (`protected_hash_check_start.log`, 67 lines) and rc 0 at 02:50Z (`protected_hash_check_end.log`).
- **Freeze hashes**: `card_sha256.txt`, `code_sha256_at_freeze.txt` (36 code files + 3 data files) and `docs_sha256.txt` are all OK (`topic4_hash_check.log`). `split_manifest_sha256.txt` is OK when checked from the outdir. Every file in src/topic4_resu, tests/topic4_resu and scripts/topic4_*.py is in the freeze list, and no file is missing from it.
- **C2**:
  - `pytest tests/topic4_resu`: 67 passed (`tests_topic4_resu.log`);
  - `STRICT_E2E=1 pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`: 86 passed (`tests_old86.log`);
  - `pytest tests/topic1_lagmotif`: 88 passed (`tests_topic1_lagmotif.log`).
- **T4.1, all legacy subjects**: `probe_legacy_padding_positions.out.json`. VMD-cache rows 0–11 each have 177 non-zero rows, and the split row is 324, so 0 test-target rows are valid for every one of the 10 legacy subjects (`src/run_all_empirical_experiments.py:107` → `fractal_motif_resu.py:475` uses rows 0..9). `probe_cache_order.out.json`: cache row order equals npy positional order (0 mismatches in 1706), so the burned-position set {0–11, 932} is correct.
- **Authenticity (re-execution from raw npy)**: `probe_rerun_subset.out.json`.
  - I re-executed 9 confirm tasks from the raw ENIGMA npy with the frozen code: fold0 C1/C4, fold3 C1/C4, fold2 C3/C5/refs, fold1 mlp:0, and fold4 C4DP.
  - All 9 are **bit-identical** to the stored `confirm/*.json`: max |ΔR²| = 0, every engine and MLP digest equal, and the C3 failure pattern equal.
  - The manifest assignment equals `split.assign(...)`. All 1195 series reproduce the manifest's valid_T.
  - Tuning at η0 = 0.02: 21/21 stable (reproduced).
- **Independent verdicts**: `independent_verdicts.py/.out.json` imports neither stats nor analyze and uses its own bootstrap with seed 424242 and B = 4000.
  - Point estimates are exact for H1 −0.002231, S1 −0.001597, S2 +0.030616 and S3 −0.004669.
  - CIs agree within Monte Carlo error (|Δ| ≤ 2.0e-4). Example: H1 [−0.00413, −0.00022] versus the reported [−0.00413, −0.00042].
  - All four verdicts are identical: stop, killed, supported, non-inferior.
  - Failure counts per class are equal (C3 10/50; every other class 0).
- **Determinism**: `scripts/topic4_analyze.py` rerun on a scratch copy gives a byte-identical `verdict.json` (sha 437161ed…5c22). The worker's `independent_recompute.py` on that copy gives all_match true.
- **Mutation evidence**: rerun of the worker's harness on a copy (`mutants_rerun/mutation_results.json`, 02:45–02:48Z). 17/17 mutants killed; CONTROL_targets_wired_but_unused survives as designed; the control copy passes 63/63.
- **Freeze ordering**:
  - The run ledger's `tuning_start` line (02:04:52Z) records card sha 2b535c39…5934 and is the first real-data outcome line. `confirm_start` is at 02:07:43Z.
  - File mtimes: card 02:03:57Z, card_sha256.txt and code_sha256_at_freeze.txt 02:04:41Z, tuning.json 02:05:08Z, confirm files 02:08–02:14Z.
  - The pre-freeze outputs are synthetic (qualification 01:38Z, smoke 01:55–01:57Z, probes 01:17–01:32Z), burned positions only (t41 01:37Z), or contain no outcomes (manifest 01:52Z).
  - The card contains none of the post-run numbers (0.146, 0.31, 6.6, 20%, 0.0022, 10/50, 0.153, 0.0306, 0.0047).
  - The card in root checkpoint commit c967f7c has sha 2b535c39…. Only one confirm_start exists in the ledger, and the worker's `scratchpad/det` is a results copy, not a second opening.
- **C4**:
  - ID scan (`probe_id_scan.out.json`) held 1706 names in memory and scanned 235 files across src/tests/scripts/results/docs for Topic 4, verification/worker_M4_r1 and worker metadata: 0 hits.
  - The only "sub-" token is the scanner literal in `tests/topic4_resu/test_outputs_no_ids.py`.
  - Packages in the superclaude-env site-packages are dated 2026-10-30 or earlier (torch 2025-12-30), so nothing was installed by M4.
- **C5/C6**:
  - topic4 code has no B300 or /scratch references (the only hit is the DGX-local scratchpad DEFAULT_CACHE).
  - `results/gpu_ledger_2026-10-31.md` has 0 M4 or topic4 lines.
  - The worker cache `scratchpad/topic4_cache` no longer exists.
- **C7**: `enigma_ocd_mbbn/HANDOFF.md` mtime is 2026-10-21, outside the M4 window. The npy directory mtime is 2025-05-23 and the VMD cache mtime is 2026-10-18.
- **Layout lint**: `audit_layout.py <run root>` returned rc 0, 177 files, 0 findings (`audit_layout.log`).
- **Defect A, tuning in-sample readout**:
  - `scripts/topic4_run.py:153–154`. `_sets_for(groups, refit=False)` makes test = tune_val = val, and `pipeline.run_references(sets)` keeps the default `refit_on_val=True`. Line 161 `run_psp(...)` does the same.
  - The ridge readout is therefore refit on tune_train + tune_val and scored on tune_val.
  - `probe_tuning_refit.out.json` reproduces tuning.json exactly with refit=True (identity 0.14554, PCA 0.12909, RRR 0.13300). The clean, train-only fit gives identity 0.14060, PCA 0.12611 and RRR 0.12998. Persistence is unchanged at −0.30847.
  - This contradicts `pipeline.py:6` ("or on inner_train only (tuning stage)") and card §3 ("Everything fitted uses training subjects only").
- **Defect B, output receipt**: `results/topic4/2026-11-01/output_sha256.txt` lists `logs/analyze.log` with the empty-file hash e3b0c442…, because the file was hashed while stdout was being redirected into it. `sha256sum -c` fails on 1 of 73 lines; the other 72 are OK.
- **Concurrent-agent artefact, not the worker's and not mine**: `src/topic4_resu/__pycache__/{__init__,topologies}.cpython-312.pyc` appeared at 02:41:39Z.
  - Timing matches `verification/challenger_M4_r1_2/c2_independent_pipeline.py`, written at 02:41:16Z, which imports topic4_resu.topologies.
  - My probes all set PYTHONDONTWRITEBYTECODE, and an import from my probes would also have produced data/pipeline .pyc files.
  - The .py hashes are unaffected.
- **Other running processes**: auditor_M4_r1_1 is running `topic4_run.py --stage confirm --outdir verification/auditor_M4_r1_1/rerun/r` in its own directory. The production run_ledger was last modified at 02:14:21Z.

## 2. Logic Chain
1. **T4.1** (diagnose R² = 1.0):
   - Every legacy subject's test window is padding (observation T4.1); the floor `max(ss_tot, 1e-8)` turns ≈ 0/1e-8 into 1.0.
   - On a full-length subject the same unmodified function gives about 0.
   - Fixtures F1–F4, F-fold and F6-VAR each kill their mutant (my rerun).
   - So the cause is evidenced, not asserted. **Met.**
2. **T4.2** (non-saturating task + frozen card):
   - Out of sample on the confirm set, persistence scores −0.286 and identity ridge 0.153 (my recompute: −0.28623 and 0.15251). The clean tuning value is 0.1406 < 0.9.
   - The card fixes the conditions (C0–C5, C4DP, instances), the backprop baseline (MLP grid, 3 seeds, early stopping), the metric (guarded per-subject R²), the seeds, δ, and the kill and stop rules before any outcome (freeze-ordering observation). **Met.** δ is analyst-set and PI confirmation is pending; this is disclosed.
3. **T4.3** (implementation + fixtures + run + verdict):
   - Stability ρ(I − D⁻¹M) < 1 is monitored at every update; the fixture iff-PD test passes and the monitor mutant is killed.
   - The no-autograd proof has three parts, each killing its mutant.
   - The run is on CPU.
   - My independent re-derivation reproduces every verdict, and 9 tasks re-execute bit-identically from raw data, so the outputs are not fabricated. **Met.**
4. **C1–C8**: C1 rc 0 at both ends. C2: 86, 88 and 67 passed. C3: card first, fixtures, logs, dated paths, addendum_01. C4: 0 IDs and no installs. C5: 0 GPU-h, no ledger entry needed. C6: ENIGMA stayed on DGX-Spark. C7: external repo untouched. C8: legacy numbers appear only as labelled artefact explanation.
5. **Defect A** could change a decision only if the in-sample bias pushed a gate the wrong way or affected η0.
   - In-sample bias is upward, and the gate is "< 0.9". Passing in-sample therefore implies passing out of sample (0.1406, verified).
   - η0 is selected by stability only, which does not depend on the readout (21/21 reproduced).
   - So no verdict, gate or η0 changes. This is a documentation and accuracy defect, which is non-blocking. It does need an addendum entry, because the result report and the T41 diagnosis cite "identity ridge 0.146 on the tuning set" as evidence.
6. Defect B and the other items affect no number.

## 3. Caveats
- **Freeze-before-results evidence basis**: the ledger card-sha line written by the run script at tuning_start, file mtimes, and the absence of post-run numbers in the card. The root's first git commit of the card (02:16Z) came after confirm ended (02:14Z), so git cannot independently date the freeze. results/topic4 is untracked. An mtime-forging scenario would be needed to invalidate this; I found no sign of one.
- I did not re-execute all 55 confirm tasks (about 26 CPU-min, above the 20-min guidance). I re-executed 9 of them, covering 5 of 7 PSP classes, the refs, an MLP seed and 4 of 5 folds, and all 9 were bit-identical. auditor_M4_r1_1 is running a full rerun in its own directory.
- B300 non-contact is shown by code and ledger evidence only. I did not ssh to the B300 nodes to list /scratch.
- **Scope of "H1 killed" (critic)**: the verdict holds for one linear local rule (masked PSP), η0 = 0.02 and 6000 updates. Under that rule every 69-edge class collapses to rank about 4.5–4.9, and the engine is not at a fixed point (median relative ΔW over the last 10% is 0.03). The test was precise (95% CI width ≈ 0.004 < δ), so it could have detected δ = 0.01 under this rule. It says nothing about NSM, rectified or other local rules. Report §2 ("the core Topic 4 claim fails") should be read with that scope; the limitations section of the report does state it.
- The common readout is closed-form supervised ridge in every arm. "Backprop-free" holds; "local learning" describes the encoder only.
- Cross-fitted CIs omit training-set variability (declared, anti-conservative). Family structure is unknown (declared).
- I did not read the other M4 reviewers', challengers' or auditors' reports, to keep this review independent.

## 4. Conclusion
**APPROVE M4.** The T4.1 diagnosis is verified for all 10 legacy subjects. The redesigned task does not saturate. The card was frozen before any primary-population outcome. The implementation is local (proof in three parts) and stability-monitored. The outputs are authentic, verified by bit-identical re-execution from raw data. The verdicts are as the card dictates: H1 stop, S1 killed, S2 supported, S3 non-inferior at δ = 0.01 with backprop significantly better by 0.0047; C3 is integrity-failed.

Requested follow-ups, none of which requires a rerun:
1. **Addendum_02.** State that the tuning-stage reference and PSP tune-val R² values were computed with the readout refit on tune_train + tune_val (in-sample, `topic4_run.py:154,161`). Give the clean values: identity 0.1406, PCA-24 0.1261, RRR-24 0.1300, persistence −0.3085. State that the gate decision and η0 are unchanged. Correct the "0.146" citations in the result report §2 and T41 diagnosis D2 by addendum, not by editing.
2. Re-pin `output_sha256.txt` so that `logs/analyze.log` has its real hash, or note the empty-hash line in the addendum.
3. After all M4 agents finish, the coordinator removes the concurrent-agent `src/topic4_resu/__pycache__/`.
4. The PI confirms δ = 0.01. Report S3 as "non-inferior at 0.01, backprop better by 0.0047", never as "equivalent".

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?          # 0
LC_ALL=C sha256sum -c results/topic4/2026-11-01/{card_sha256.txt,code_sha256_at_freeze.txt,docs_sha256.txt} | grep -vc ': OK$'   # 0
nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic4_resu                      # 67 passed
nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M4_r1_1/probe_rerun_subset.py <scratch-cache-dir>   # all_tasks_bit_identical true (~4 min, 4 procs)
nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M4_r1_1/independent_verdicts.py                    # verdict_equal true x4
nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M4_r1_1/probe_tuning_refit.py                      # tuning_json_reproduced_by_refit_True true; clean identity 0.1406
nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M4_r1_1/probe_legacy_padding_positions.py          # all_legacy_0_9_test_window_fully_padded true
```
This review is invalidated if any of the following holds:
- a protected or freeze hash fails;
- any re-executed confirm task differs from its stored JSON;
- `independent_verdicts.py` reports a verdict mismatch;
- the card is shown to contain a post-run number;
- an earlier real-data tuning or confirm opening is found outside the ledger.
