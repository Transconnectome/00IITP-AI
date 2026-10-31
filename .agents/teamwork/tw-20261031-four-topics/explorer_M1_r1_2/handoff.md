# explorer_M1_r1_2 — handoff (run tw-20261031-four-topics, M1, explorer 2 of 3)

**Summary.**
- **T1.1 is solved with tests only.** I wrote a proposed test file and ran the adapted mutant harnesses against it. All 5 victory-audit survivors are killed: 0 survivors over 19 + 4 mutants, and the control passes 59.
- **Two of survey_1's T1.2 defect fixtures cannot work as FPR fixtures** on this design. A cross-site Freedman–Lane permutation and a dx permutation both give a nominal FPR. They need structural oracle tests instead.
- **The Mundlak stop check passes even when the fit fails to converge**, so it does not guard d's denominator.
- **The 200 s truncation has to be floor(200/TR) native samples, not ceil.** Only floor gives the card's "first 100 grid samples" at all 7 TRs.
- **The §7 extraction variants must run at the post-fallback primary density.**

## 1. Observation

**State at start (2026-10-31 ~16:55 KST)**
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0, with 67 lines.
- The card §12 hashes match 10/10 (re-checked at the end).
- `results/topic1/2026-10-30/test_hashes_r2.txt` is all OK, so the existing 7 test files are byte-identical to the reviewed r2 bytes.
- PROTECTED_HASHES does **not** list `src/topic1_lagmotif/*`, `scripts/topic1_timing.py` or `tests/topic1_lagmotif/*`. Card §12 still binds the first two.
- `tests/topic1_lagmotif/` holds 7 files (`mut_harness/repo_tests_listing.txt`).

**O1. Frozen API facts used by the plan**
- `pipeline.extract_subject(series, params=PARAMS, **kw)` goes through `flow_features(..., channels, densities, n_null, attempts_factor)`.
- A §7 variant can therefore be run without editing src:
  - DCT 128 s: pass a params *copy* with `highpass_cutoff_s=128`. This gives a new `params_sha256`, while the seeds stay the same because they come from `base_seed`.
  - Attempts factor 40: pass `attempts_factor=40`.
- `motif_statistics` returns `null_sd` for all 5 classes, so a near-degenerate flag can be computed in scripts.
- `acceptance_mean` comes out of the numba `_run_chain` and counts 2-swap no-ops (addendum item 31).
- `degenerate` covers 030T and 030C only, and means sd == 0 exactly.

**O2. T1.1 probe.** `verification/explorer_M1_r1_2/proposed_tests/test_extract_contract.py` (sha256 `9d7121e4…1ad2`) has 5 tests.
- **Fixture.** TR 0.8 with n_trim 50, 400 native samples and 37 trailing zero rows. A shared slow driver with per-ROI latency gives a gradient share above 0.2. Position 7 is used, with n_null 12 and attempts factor 2.
- **Oracles** come from the card text, in numpy:
  - k = round(d·46,056);
  - valid_T = raw_valid_T − ceil(40/TR);
  - curl = F − (p_i − p_j), with p the row mean;
  - seeds = SeedSequence([20261030, pos, ch, round(1000d)]);
  - SP = Z/‖Z‖.
- **On production:** 5 passed in 2.08 s.
- **Harness.** Copies of `victory_auditor_1/mutants.py` and `mutants_extra.py` are in `mut_harness/`, with `BASE` and both output paths changed to my folder, plus an opt-in `WITH_PROPOSED=1` copy step. The diff is 3 hunks; see `mut_harness/` and the `diff` in my transcript.
  - Without the proposed file, the control and all 5 survivors give rc=0 with "54 passed" (`run_without.log`). This reproduces the audit.
  - With the proposed file (`run_with.log`):
    - control: 59 passed;
    - all 19 `mutants.py` mutants: rc=1 (`roi_subsample_80`: 4 failed);
    - `curl_returns_F`: 2 failed;
    - `seeds_ignore_position`: 2 failed;
    - `sp_not_normalised`: 1 failed;
    - `extract_subject_drops_valid_T`: 1 failed.
  - The auditor's receipts are unchanged (`mut_harness/source_hashes_before.txt` checks OK after the runs). The mirrors under `mut_harness/mut/` were deleted after the run; the harness rebuilds them.

**O3. Design facts.** `probe_stats_design.py` → `.out.json`. Inputs were metadata columns plus npy *headers* only (shape, no values). Nothing per subject was written.
- n = 1706, 23 sites, and every file has 304 ROIs.
- 7 sites have more than one native T. The distinct-T-per-site histogram is {1: 16, 2: 3, 3: 3, 6: 1}.
- Approximate minimum duration (assuming no trailing padding) is 200.0 s, in 2 sites. No subject is under 200 s, and the minimum grid length is 100.
- The full site-FE design [1, age, sex, logdur, site dummies] + dx has rank 27/27, with condition number 1.5e3. The Y-BOCS subset has rank 26/26 (n 856, 23 sites). The medication subset has rank 15/15: n = 301 in 11 sites, 180 with code 1 and 121 with code 2.

**O4. Freedman–Lane engine (vectorized; the reduced-model QR projects out ŷ_r exactly).** Synthetic H0 on the real design:
- Setup: site effect aligned with site OCD fraction at ICC 0.3; noise SD differing by site; half the reps with t(4) noise.
- R = 400, B = 999:

  | Variant | FPR | MC SE |
  |---|---|---|
  | FL within site | 0.0425 | 0.011 |
  | FL across sites (R = 200) | 0.035 | — |
  | dx permuted within site (R = 200) | 0.040 | — |
  | Welch | 1.000 | — |

- Cost: 0.09 s per rep at B = 999, and 1.65 s for one B = 9,999 analysis.

**O5. Adversarial across-site scenario** (`probe_fl_across_adversarial`, R = 300, B = 999). Balanced-dx sites get a residual SD 3× or 6× that of imbalanced sites.

| SD ratio | FPR within | FPR across | MC SE |
|---|---|---|---|
| 3 | 0.043 | 0.060 | 0.0126 |
| 6 | 0.047 | 0.053 | 0.0126 |

**O6. MixedLM ML + Mundlak**
- **Aligned scenario** (`probe_stats_design`, 20 fits):
  - max |β_LMM − β_FE|/SE = 4.3e-13;
  - 2 of 20 fits not converged, with ConvergenceWarning and UserWarning;
  - min re_var = 0.0 (m_dx absorbs the site effect);
  - 0.075 s per fit.
- **Independent site intercepts** (`probe_mixedlm_re_path`, 60 fits per ICC):

  | | ICC 0.1 | ICC 0.3 |
  |---|---|---|
  | max β ratio | 6.5e-14 | 3.6e-14 |
  | fits not converged | 1/60 | 1/60 |
  | mean re_var | 0.079 | 0.320 |
  | min re_var | 0.034 | 0.151 |
  | scale / (FE RSS/(n−p)) | 0.9965–0.9981 | 0.9948–0.9978 |
  | d̂ = β/√scale at true 0 / 0.15 / 0.30 (MC SE 0.011) | −0.031 / 0.142 / 0.293 | −0.031 / 0.142 / 0.293 |
  | total-SD defect β/√(scale + re_var) at true 0.30 | 0.283 | 0.257 |

  The two ICC blocks share the noise draws, so they are not independent replicates.

**O7. 200 s truncation**, using the frozen `preprocess()` on synthetic arrays.
- `probe_trunc200_lengths.log`, native ceil(200/TR): 101 grid samples at TR 0.7, 0.85, 1.73 and 1.8, and 100 at the others.
- `probe_trunc200_lengths_floor.log`, native floor(200/TR) (199.0–200 s): **100 at all 7 TRs**.

**O8. Housekeeping**
- The ID scan with `victory_auditor_1/probe_id_scan3_noboundary.py`, in both strict and all modes, over `verification/explorer_M1_r1_2` and this metadata folder, finds 0 files with hits.
- No bytecode written. No process of mine is left running. The `explorer_M1_r1_3` and `enigma_ocd_mbbn-palm` processes seen in `pgrep` are not mine.

## 2. Logic Chain

1. **T1.1** (O1, O2):
   - The 5 survivors are output-contract gaps, so assertions made through `extract_subject` against card-text oracles kill them without touching src.
   - Shown empirically: 0 survivors, and the earlier 19 kills are kept.
   - Installing the file byte-for-byte into `tests/topic1_lagmotif/` makes the plain repointed harness pick it up, with no `WITH_PROPOSED` needed. Expected control: 59 passed.
2. **FPR fixtures** (O4, O5):
   - With C(site) in the reduced model, cross-site FL and dx-permutation stay near nominal, even with variance tied to dx balance.
   - So "permuting across sites must make an FPR fixture fail" cannot be met; it would come out as a false PASS or an unfalsifiable gate.
   - Those defects have to be caught structurally:
     - every P[b, i] lies in site(i);
     - the vectorized t* equals a statsmodels OLS refit on y* = ŷ_r + P e_r with the full site-FE design;
     - the reduced design has no dx column. Under dx-permutation, y* never changes and t* ≠ refit.
   - Welch fails by FPR (1.0), so its FPR fixture is valid.
3. **σ defect** (O6):
   - In the aligned scenario re_var = 0, so the defects "σ from the total SD" and "√(scale + re_var)" cannot be seen there.
   - With independent intercepts at ICC 0.3, the defect shifts d̂ at 0.30 by about 0.036. That is 3 MC SE at 20 reps and about 10 MC SE at 200 reps.
   - So the σ fixture must use independent intercepts at ICC ≥ 0.3 and ≥ 200 reps.
4. **Convergence** (O6):
   - The 0.01·SE check passes at 1e-13 whether or not the fit converged.
   - It therefore does not guard `fit.scale`, which is d's denominator.
   - The scale stays within 0.5% of the FE residual variance, so a cross-check of scale against the FE value is a usable guard.
5. **Truncation** (O7). The card says "first 100 grid samples after the head trim". Only floor(200/TR) gives exactly 100 at all TRs with the frozen chain. Survey_1's ceil rule does not.
6. **Fallback sequencing** (card §3, §7). §7 applies to the primary density, which is 15% if the fallback triggers. The fallback is label-free. So: extract the 6 carded units → decide the fallback (hash it) → run the §7 extraction variants only at the chosen density. This avoids paying about 9 CPU-h twice, and avoids a label-dependent compute fork.
7. **Validation cost** (O4). FL validity does not depend on B. R = 2,000 at B = 999 costs about 3 CPU-min per scenario. At B = 9,999 it costs about 0.9 CPU-h per scenario. So: B = 999 for the FPR grid, a small B = 9,999 confirmation, and B = 9,999 for the real analysis, as the card requires.

## 3. Caveats

- **Design probes:**
  - They used npy headers and assume no trailing zero padding. The true valid_T comes from the T1.3 pass.
  - Durations are approximate. The 200 s minimum could be lower if some files have trailing zeros.
- **Real-data degeneracy rate** at 10% is known only from the 5 A3 subjects, all non-degenerate at 10%. Whether the fallback triggers is unknown until extraction runs.
- **Small d̂ cells** (20 reps): the d = 0 cell mean of −0.031 is −2.8 MC SE. That is likely chance, since the noise is shared across ICC blocks and 3 cells were inspected, but it is not resolved. The worker's R ≥ 200 recovery runs decide it.
- **Harness copies** are probes in my folder. The worker should make its own copies.
- **Not investigated:** connectome, dgx1 and B300 environments (survey_1 covers connectome), and the LOGO classification and static-FC code paths.
- **Unrelated process seen.** Another workstream, `enigma_ocd_mbbn-palm` b300-migration, was running ssh to a B300 node during my session. This relates to survey_2's C6 escalation. I did not inspect it further.

## 4. Conclusion (recommended M1 strategy)

**Phase 1, label-free (parallel)**

**A. T1.1**
- Install `verification/explorer_M1_r1_2/proposed_tests/test_extract_contract.py` byte-for-byte as `tests/topic1_lagmotif/test_extract_contract.py`, or an independently reviewed equivalent. Leave the 7 existing files untouched: test_hashes_r2 binds them.
- Copy both harnesses to `verification/<worker>/`, change `BASE` and the 2 output paths, and run `mutants.py`, then `mutants_extra.py`. Run them sequentially, because both build a `control` mirror under the same BASE.
- Expected: control 59 passed; 19/19 and 4/4 rc=1.
- Copy the results JSON into `results/topic1/2026-10-31/`.

**B. T1.3: `scripts/topic1_manifest.py`**
- Record count 1706 and a salted digest of the sorted names.
- Per position, record site, TR, raw_valid_T, n_trim, valid_T, grid length and duration_s, from the frozen `NpyCohort.load`.
- Floor: grid length ≥ 100 (200 s), recorded in the pre-label addendum. Current approximate data show nobody below it.
- The extractor asserts the manifest before it starts.

**C. T1.4a: `scripts/topic1_cohort_extract.py`**
- Run local, detached (`setsid nohup nice -n 10`), with 12–14 processes and the thread env set before Python starts.
- One `extract_subject` call per subject covers all 6 units, about 26 s per subject (추정 from A3): about 12.5–13 CPU-h, under 1 h wall.
- Store per subject: Z, null_sd, degenerate flags, acceptance, gradient share, valid_T, and `params_sha256` plus the code hashes in the header. Use resumable JSONL with positions only.
- Then make the label-free fallback decision: the share of subjects degenerate for E1 (030C) or E2 (030C or 030T) at 0.10, with a denominator equal to the subjects that pass the data contract. Write it to a dated addendum and record its sha256.
- Then run the §7 extraction variants at the chosen primary density only:
  - DCT 128 s (params copy);
  - factor 40 (kw);
  - 200 s truncation: native[:floor(200/TR)] → frozen `preprocess` → `lagged_net_flow(·, 1)` → frozen `flow_features`.

  Each variant gets its own params hash and a fixture showing 100 grid samples at all 7 TRs.

**D. T1.2: `scripts/topic1_cohort_stats.py` plus tests**
- **Card §4–§6 exactly:**
  - FE-OLS t for dx;
  - FL with reduced-model residuals permuted within site, B = 9,999, seed 20261031, p = (1 + #)/(B + 1);
  - MixedLM ML with Mundlak means and the 0.01·SE stop;
  - d = β/√scale;
  - Holm over E1 and E2;
  - survive iff p_Holm < 0.05 and |d| ≥ 0.15; killed iff neither survives;
  - §6 secondaries with BH within each family;
  - raw d and Welch, labelled descriptive.
- **Fixtures:**
  - **Structural oracles:**
    - permutations stay within site;
    - vectorized t* equals the statsmodels refit on y* = ŷ_r + P e_r (atol 1e-8) for 20 draws;
    - the reduced design excludes dx;
    - on a tiny design, the p from full enumeration of within-site permutations equals a brute-force refit.
  - **FPR,** R ≥ 2,000 at B = 999, |FPR − 0.05| ≤ 2·√(0.05·0.95/R), in 4 scenarios:
    - aligned site effects;
    - independent intercepts at ICC 0.3;
    - site-heteroscedastic noise;
    - t(4) noise.
  - **Welch must fail its FPR fixture.**
  - **Planted d = 0.15 and 0.30 in σ_ε units**, with independent intercepts at ICC 0.3 and ≥ 200 reps. Mean d̂ must be within 2 MC SE, and the "√(scale + re_var)" and "total SD" variants must fail.
  - **Deterministic unit tests:** Holm, the sign (OCD − HC), the fallback at 9% vs 11%, and the kill boundary at |d| = 0.1499 / 0.1501 and p_Holm 0.0499 / 0.0501.
- **Guards:** log `converged` and re_var for each fit, and require scale/(FE RSS/(n−p)) to fall in [0.98, 1.0].
- **Pre-label addendum.** It settles survey_1's gaps (a)–(i), with (g) = floor. It also states the non-convergence rule: refit with another optimizer (`method=['lbfgs', 'powell']`); if the fit still fails, use the FE β with σ̂ from FE RSS/n, flagged.
- After independent review, record the script sha256.

**Phase 2, serial**
1. Review, then record the script sha.
2. Write the pre-label addendum, with its sha.
3. Join the labels.
4. Run the stats.
5. Report:
   - rates by group and site: degeneracy, near-degenerate (null_sd < 1, descriptive only), and acceptance (stated to include no-ops; do not re-implement the numba chain);
   - the verdict for each endpoint per the card, next to the spurious-direction limitation and the degeneracy rates;
   - an addendum for any deviation (T1.5).

## 5. Verification Method

- **T1.1 probe:**
  ```
  cd /home/juke/git/00IITP-AI && PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider -q verification/explorer_M1_r1_2/proposed_tests/test_extract_contract.py
  ```
  Expected: 5 passed.
- **Mutants:**
  ```
  cd verification/explorer_M1_r1_2/mut_harness && TAG=x WITH_PROPOSED=1 python -B mutants.py && TAG=x WITH_PROPOSED=1 python -B mutants_extra.py
  ```
  Expected: control 59 passed and every mutant rc=1. Compare with `mutation_results_with.json` and `mutation_results_extra_with.json`.
- **Stats probes:**
  ```
  R=400 B=999 python -B probe_stats_design.py
  python -B probe_fl_across_adversarial.py
  python -B probe_mixedlm_re_path.py
  ```
  Expected: matches the `.out.json` files. The seeds are fixed, but BLAS threading may change the last digits.
- **Truncation:** rerun the two heredoc probes; their logs are `probe_trunc200_lengths*.log`.
- **Integrity:** the PROTECTED_HASHES check gives rc 0, and the card §12 hashes match 10/10.
- **Invalidation conditions:**
  - any card §12 file changes;
  - the npy listing count or digest changes;
  - real valid_T shows trailing padding that brings durations below 200 s;
  - statsmodels changes from 0.14.6.
