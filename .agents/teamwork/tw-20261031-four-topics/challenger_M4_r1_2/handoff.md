# Handoff — challenger_M4_r1_2 (M4 / Topic 4), Hard handoff, 2026-11-01T03:03Z

Verdict: **CONFIRMED**. T4.1–T4.3 hold under independent re-implementation, recomputation from raw outputs, a
production bit-identity rerun of fold 0 C3/C1, freeze-timeline forensics and new mutants. There are no blocking
findings. The non-blocking findings are fixture gaps and record defects (section 4). None of them changes a number
or a verdict, because each affected quantity was verified independently.

All probes are in `/home/juke/git/00IITP-AI/verification/challenger_M4_r1_2/` (c1–c8 `.py` / `.out.json` / `.log`, plus `mut_logs/`).
All of them are read-only on production paths. 0 GPU-h; no B300 contact; ENIGMA data read on DGX-Spark CPU only.

## 1. Observation
- **Hashes.** Measured at 02:36Z and again at 03:00Z:
  - C1 `sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0;
  - `card_sha256.txt`, `code_sha256_at_freeze.txt` and `docs_sha256.txt` all verify;
  - card sha 2b535c39…5934, code-hash file 3b061f00…83b2, split 3e56210f…0436, verdict.json 437161ed…5c22.
- **Freeze timeline.** Kernel timestamps (`stat` %w / %y / %z, UTC):
  - card birth 02:03:57, mtime 02:03:57, ctime 02:04:41 (the chmod);
  - every frozen code, test and script file has ctime ≤ 01:54:29;
  - `run_ledger.jsonl` rows:
    - `tuning_start` at 02:04:52Z with card sha 2b535c39, split 3e56210f and code file 3b061f00;
    - `confirm_start` at 02:07:43Z with the same three hashes;
    - 55 task rows, all `ok`, running 02:07:43–02:14:21Z; every `output_sha256` matches the current confirm file;
  - the first real-data outcome file is `tuning.json`, born 02:05:08.
  - Git checkpoint fa84b7d (02:01:27Z) has no card. c967f7c (02:16:27Z) is the first commit containing it, and its blob sha equals 2b535c39.
  - Real-data probes before the freeze (explorer `probe_a`, explorer `probe_c_real`, `t41_counterfactual`) touch only positions 0 and 932 (not TR 2.0). The split builder reads only metadata and lengths.
- **c1** (recompute from `confirm/*.json`; imports nothing from src or scripts):
  - split rule re-derived from salted sha256: 0 mismatches; each of the 1014 confirm positions is tested exactly once, in its manifest fold;
  - per subject, (1−R²)/MSE agrees across all arms with a relative spread ≤ 4.5e-16, so every arm was scored on the same targets; constant R² ≤ −4e-6;
  - points match: H1 −0.0022309 (|Δ| 4e-19), S1 −0.0015974, S2 +0.0306165, S3 −0.0046691;
  - own crossed bootstrap (PCG64 seed 777, B 4000): H1 [−0.00415, −0.00039], S1 [−0.00374, +0.00043], S2 [0.02870, 0.03228], S3 [−0.00505, −0.00428]. The shipped CI endpoints are within 0.03–0.18 bootstrap SD of these;
  - verdicts re-derived from the card section 6 rules on both CI sets: stop / killed / supported / non-inferior, matching;
  - integrity: C3 10/50 unstable, at (fold, init) (0,0) (0,9) (1,2) (1,3) (2,2) (2,4) (2,6) (3,5) (4,0) (4,9); every other class 0 unstable;
  - sensitivity: subject-only, site-cluster, 4-s and skill intervals all lie below 0 and match the shipped ones.
- **c2** (own loader with least-squares detrend, own inner split, own ridge and λ rule, own PSP from the card section 4 text; only the vendored mask generator imported):
  - valid_T and raw_valid_T of all 1195 subjects equal the manifest;
  - fold 0, constant / persistence / identity / PCA-24 at 2 s and 4 s: max |ΔR²| ≤ 5e-15;
  - PSP runs C0 g0, C1 g0, C4 g0, C4DP g0 and C5 g0 match to ≤ 3e-11, with the same rank_F and min λ(M);
  - C3 g0 fails at step 75, the same step as saved;
  - C3 g1 differs by 0.0049 (see c6).
- **c3** (full independent rerun, all 5 folds, 450 PSP runs for C1/C4/C4DP/C5 plus 25 random-linear runs):
  - H1 −0.0022308996 (|Δ| 7e-13), S1 |Δ| 3e-13, S2 |Δ| 0;
  - 0 instabilities;
  - 12 of 13 sites have H1 < 0; 10 of 30 C4 graphs score above the C1 mean.
- **c4** (VMD cache rows 0–11, burned positions):
  - every row is Amsterdam-VUmc, with raw_valid_T 197 and 177 valid cache rows;
  - test rows 325–463 inside the valid portion: 0 of 139 for every row; `all_rows_0_9_test_window_fully_padded` is true;
  - cache row i maps to npy position i, with best head offset 20 and correlation 0.71–0.94 for every row.
- **c5** (17 new mutants on tree copies; whole `tests/topic4_resu` suite except the output scan; the control copy passes 66; run with `-x`):
  - KILLED (7): `lambda_selected_on_test`, `data_no_detrend`, `data_trim_20s`, `c4dp_is_c4`, `rho_relaxed`, `no_instance_resampling`, `spectral_rescale_via_norm2`;
  - `spectral_rescale_via_norm2`: the first failure under `-x` was an incidental `KeyError: engine_digest` (the engine went unstable). Rerun without `-x` (c8a), 18 tests fail, including the stability, planted-subspace, relaxation and equivariance tests. It is a genuine behavioural kill, but no AST locality check catches it;
  - SURVIVED (10): `pipeline_psp_monitor_dropped`, `pipeline_mlp_early_stop_on_train`, `pipeline_h2_test_pairs_at_h1`, `split_tuning_frac_030`, `split_burned_positions_ignored`, `stats_no_site_strata`, `stats_level_ignored`, `psp_global_frobenius_W_normalisation`, `psp_inverse_lateral_via_solve` (codes y = Wx, with the lateral network ignored), `backprop_hidden_48`.
- **c6** (production code, fold 0):
  - the production MaskedPSP plus monitor, on the production loader, reproduces the saved engine digests bit-identically for C3 g0–g9 and C1 g0–g2, including the C3 failures at steps 75 and 111;
  - my input differs by ≤ 1.1e-12. With it, the C3 g1, g2 and g4 trajectories diverge (final min λ moves by 0.005–0.02), while C1 g0–g2 stay within ~1e-15;
  - adding N(0, 1e-24) noise to the input over 5 seeds:
    - C3 fold 0 unstable count is 2, 2, 2, 2, 3 (g6 flips once);
    - C3 min-λ spread reaches 0.055;
    - C1 shows 0 flips and 0 spread.
- **c8** (adversarial inputs to the UNMODIFIED `scripts/topic4_analyze.py`, run on results copies):
  - (b1) every C3 run in fold 0 marked unstable → rc 1, `ValueError: a subject has no successful run in this class`;
  - (b2) every C4 run in fold 0 marked unstable (30/150 = 20% > 10%) → the same crash, where the card requires "inconclusive (execution integrity)" for H1 and S1;
  - (b3) one C4 run marked unstable (below the limit) → runs, excludes it, verdicts unchanged.
- **Self-incident (disclosed, repaired).** My `-I` runs of c2 and c6 ignored `PYTHONDONTWRITEBYTECODE`. They created bytecode caches `src/topic4_resu/__pycache__/` (born 02:41:39Z, 5 .pyc) and `src/topic4_resu/local/__pycache__/` (born 02:51:22Z, 2 .pyc), plus one in my probe directory. I removed all three directories at 03:07Z (their birth times fall inside my runs). No `.py` file changed: C1 rc 0 and the freeze hashes verify at 03:07Z.
- **c7**:
  - **Analysis-script mutants.** No test references `scripts/topic4_analyze.py`. On copies, I changed the integrity limit (UNSTABLE_MAX 0.25), the S level (LEVEL_S 0.95), the H1 direction (C1 − C4), the S3 direction (MLP − C5) and the H1 horizon (4 s). None of these changes any verdict. δ = 0 changes S1 to inconclusive and S3 to inferior. The unmutated copy gives a byte-identical verdict.json.
  - **Topology invariants.** No violations for any instance used:
    - C1–C4DP all have 69 edges, and C5 has 276;
    - C4 has 0 designated-hub edges;
    - C4DP has the same degree sequence as C4, differs from C4, and keeps 25–41% of C4's edges;
    - C1 and C4 each have 30 distinct graphs.
  - **ID scan.** 241 files scanned, with 0 participant-name hits. The only BIDS-prefix occurrence is the scanner literal in my own c7 script.
- **Tests (mine).**
  - `tests/topic4_resu`: 67 passed;
  - old suite (`STRICT_E2E=1`, 3 paths): 86 passed;
  - C1 rc 0 afterwards;
  - layout lint on the run root: 182 files, 0 findings.
- **MLP diagnostics** (15 selected fits, 60 grid fits):
  - selected lr is always 1e-3, the lower of the two grid values;
  - best epoch is 14–48, and no fit reaches the 100-epoch cap;
  - `epochs_run` − `best_epoch` = 8, the patience, i.e. early stopping fired.
- **output_sha256.txt.** `sha256sum -c` fails on `logs/analyze.log`. The recorded hash is e3b0c442…, the empty-file hash: the script hashed its own stdout log before writing to it.

## 2. Logic Chain
1. Card ctime 02:04:41 < tuning_start 02:04:52 < first outcome file 02:05:08, and code ctimes ≤ 01:54:29. Both ledger start rows carry the frozen hashes, and `topic4_run.py` refuses to start on a mismatch. So the card and code governing the confirm results were fixed before any TR = 2.0 outcome existed. ctime cannot be set by user tools.
2. c3 re-derives H1/S1/S2 from raw npy with independently written loader, split, engine and readout, and matches to ≤ 7e-13. c1 re-derives every point, CI and verdict from the saved outputs. So the headline numbers are what the card's procedure gives on these data, not an artefact of `stats.py` or `analyze.py`.
3. My engine is written from the card text: a target-free local rule with steady state M⁻¹Wx and no global step. It reproduces the saved C0/C1/C4/C4DP/C5 outputs to ~1e-11. This is direct empirical evidence that the runs governing the verdicts used only the local, target-free rule (T4.3 "no autograd backprop"). It complements the worker's AST, import-block and target-invariance proof.
4. The H1 CI_hi (−0.0004) is below δ = 0.01 by about 40 bootstrap SD, so "stop" is insensitive to the bootstrap details (my CI, and c7's mutants of the level and direction). The same holds for S1 "killed", S2 "supported" and S3 "non-inferior".
5. T4.1: c4 shows that every legacy row 0–9 has a fully padded test window, so the "every subject" claim holds. Combined with the floor at `fractal_motif_resu.py:425` (verified), the mechanism is established.
6. The surviving mutants mean the frozen tests do not guard several card rules: the pipeline-level stability monitor, the steady state in `transform`, global normalisation outside `hebbian_update`, bootstrap strata and level, split constants, MLP selection and width, and the 4-s test pairs. The verdict-relevant analysis script has no tests at all. The shipped run did not have these defects, for the following reasons:
   - **Monitor, `transform` steady state, global normalisation, 4-s pairs:** excluded by c2 and c3, where my strictly local M⁻¹Wx engine and correct 4-s pairs reproduce the saved values, and by c6, where the saved monitor results, including the C3 failure steps, are bit-identical.
   - **Bootstrap strata and level:** excluded by c1's independent bootstrap.
   - **Split constants:** excluded by c1's re-derivation and by the run-time `assign` equality check in `topic4_run.py`.
   - **MLP early-stop data and width:** not re-implemented by me. They are protected only by the frozen-code chain:
     - the `confirm_start` ledger row records code-file sha 3b061f00;
     - `verify_integrity` refuses to run on a mismatch;
     - the hashed `pipeline.py` passes inner-val to `train_mlp_selected`, and `backprop.py` has hidden = 24;
     - the MLP diagnostics show early stopping fired at the patience limit.
   
   So the gaps concern future regressions, not these results. c8 adds a concrete robustness bug: if every run of a class fails within one fold, the analysis crashes instead of applying the card's integrity rule. It fails safe (no false verdict) but does not implement the rule.
7. c6: C3 is numerically ill-conditioned near the stability boundary. Its saved results are bit-reproducible on this host, but sub-ULP-scale input changes can flip runs. A count of 10/50 needs at least 5 flips to fall to the 10% limit, and 1 flip was seen in 5 perturbations. So the C3 "inconclusive (execution integrity)" conclusion is robust in direction, while the exact count is platform-sensitive. No verdict uses C3.

## 3. Caveats
- I did not rerun the confirm stage end to end through `scripts/topic4_run.py`; `auditor_M4_r1_1` was doing that. My substitutes:
  - a full independent rerun of the H1/S1/S2 arms (c3);
  - a production bit-identity rerun of fold 0 for C3 and C1 (c6).
- The MLP and S3 were not re-implemented. S3 is checked from saved outputs (c1) and the MLP diagnostics. RRR-24 is the linear rank-24 optimum, and MLPenc ≈ RRR-24.
- The T4.1 counterfactual for position 932 was not rerun. Explorer `probe_c_real` independently gives the same numbers.
- δ = 0.01 is analyst-set; PI confirmation is pending. The H1 rule gives "stop" for either sign of an effect smaller than δ; this is by design (c7).
- My DISPATCH.md condenses the worker JSON that was embedded in the dispatch; every other line is verbatim.

## 4. Conclusion
**CONFIRMED**:
- T4.1 diagnosis;
- T4.2 frozen card before results (forensically supported), with the redesign non-saturating;
- T4.3 local engine with no backprop, a stable monitor and the verdicts H1 stop, S1 killed, S2 supported, S3 non-inferior with backprop better by 0.0047, and C3 inconclusive.

Non-blocking, recommended for the PI or a later iteration (all in new dated paths, never by editing frozen files):
- **(a)** Add fixtures that kill the 10 survivors from c5, and a test of `topic4_analyze.py`'s semantics: contrast direction, levels, integrity limit and horizon.
- **(a2)** Make `class_scores` and the descriptive loop tolerate an all-failed class in a fold, and route it to "inconclusive (execution integrity)" (c8 b1/b2).
- **(b)** Report that the C3 failure count is perturbation-sensitive.
- **(c)** Regenerate the output hash manifest so that it excludes the script's own stdout log, and note this in an addendum.
- **(d)** Pre-results provenance currently rests on filesystem ctime and the ledger. Committing the card before the run would give an independent attestation in a future run.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?          # 0
TZ=UTC stat -c '%w | %z | %n' docs/03_empirical_analysis/topic4/2026-11-01_topic4_analysis_card.md results/topic4/2026-11-01/tuning.json
V=verification/challenger_M4_r1_2; PY=/home/juke/superclaude-env/bin/python3
nice $PY -I $V/c1_recompute_from_outputs.py results/topic4/2026-11-01        # verdicts_match true (writes only $V/c1_*.out.json)
nice $PY -I $V/c3_full_independent_h1.py results/topic4/2026-11-01           # ~6 min, 4 procs; abs_diff <= 1e-12
nice $PY -I $V/c6_c3_conditioning.py results/topic4/2026-11-01               # saved_digest_match_prod true for every run
nice $PY -I $V/c5_mutants.py 3                                               # control passes; survivors listed (copies only)
nice $PY -I $V/c8_adversarial_analysis_inputs.py <scratch dir>                # b1/b2 rc 1 ValueError; b3 rc 0
# note: -I ignores PYTHONDONTWRITEBYTECODE; remove any __pycache__ created under src/topic4_resu afterwards
LC_ALL=C sha256sum -c results/topic4/2026-11-01/output_sha256.txt | grep -v ': OK'   # analyze.log FAILED (empty-file hash)
```
The conclusion is invalidated if any of the following holds:
- a frozen-file hash fails;
- c1 `verdicts_match` is false;
- c3 `abs_diff` exceeds 1e-9;
- c6 reports a digest mismatch with the saved outputs;
- a later rerun gives a different H1 CI_hi sign relative to δ.
