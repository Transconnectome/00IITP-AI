# Handoff (Hard): challenger_M3_r1_2, M3 / Topic 2, 2026-11-01

**Verdict: CONFIRMED.** worker_M3_r1's claim holds: the frozen card gives **stop (killed)**. I could not refute it.
- All headline numbers trace back to the saved, trained checkpoints, with the correct arm permutations.
- The card was frozen before any real-data result.
- The verdict follows card §8 and does not depend on any single seed.

There are no blocking issues. The test suite has coverage gaps, and some documents are stale or contain small inaccuracies (§4).

All probes and outputs are in `/home/juke/git/00IITP-AI/verification/challenger_M3_r1_2/`. On B300 they are in `/scratch/iitp4/challenger_M3_r1_2/`. I modified no production file.

## 1. Observation

### Gates, run locally

| check | result | log |
|---|---|---|
| C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` | rc 0, 67/67 | `logs/c1_protected.txt` |
| `code_sha256_at_freeze.txt` | rc 0 | `logs/code_freeze.txt` |
| card pin | rc 0, 8/8 | `logs/card.txt` |
| output pin | rc 0, 43/43 | `logs/output_pin.txt` |
| `pytest tests/topic2_rgpool` | 55 passed | `logs/tests_topic2.txt` |
| old suite (`tests/test_empirical_four_topics.py`, `tests/test_pilot_connectome.py`, `tests/e2e`) | 86 passed | `logs/tests_old86.txt` |
| `audit_layout.py` on the run root | 212 files, 0 findings | |

Files present but not in the freeze list are exactly the three disclosed in addendum 01: `scripts/topic2_id_scan.py`, `tests/topic2_rgpool/test_outputs_no_ids.py` and `tests/topic2_rgpool/test_token_order.py`.

### Vendored code

`git -C SwiFT_v2 show f0dc7aca:project/module/models/<f> | sha256sum` equals the vendored file for both files:
- `simmim_swin4d_transformer_ver11.py`: de132387…052a
- `patchembedding.py`: c889eebb…a7ca7

### Freeze ordering, from third-party commits by the root checkpoint job (read-only `git log` / `git show`)

| file | first commit | commit time (UTC) | `git show` sha256 | compared with |
|---|---|---|---|---|
| card | 51609c1 | 03:16:27Z | c9bfc60a…41f5 (= frozen) | first HCP launch 03:44:37Z; partitions_hcp mtime ~03:20Z |
| addendum 02 | c67403f | 04:01:27Z | 4a7e6f6c… (= current) | first HCP run end 04:11:06Z |
| addendum 03 | 55ba1e0 | 04:46:28Z | 8e80dd43… | wave 4 end 05:09Z |
| `PI_DECISIONS_2026-11-01.md` | a06f435 | 03:01:27Z | — | card freeze; already contains δ = 1% (M3) and "HCP-YA OA counts as public" |

- The card's "frozen" content was in a commit before any real-data result.
- Addendum 02 was committed before any Stage-1 test number existed.
- The result report in c67403f was a template: `STAGE1_VERDICT_PLACEHOLDER`.

### Independent recomputation from the raw `run.json` files (`recompute_from_runs.py`, which does not import `src/topic2_rgpool`)

All 314 checks pass (`recompute_from_runs.out.json`).
- **Per run:** Σnum/Σden equals `test_nmse` exactly. Arm, perm key, perm sha256 and perm file sha256 all match the pinned npz. `code_sha256` equals the frozen pins. Status, budget (8750×16, lr 2e-4, wd 0.05, warmup 0.05, mask 0.6, E36) and split sha all match. Every start is after 03:14:34Z, and every `cuda_visible` equals the GPU in `launched.json`.
- **Pairing:** the test subject order is identical in all 15 HCP runs. `test_den` is identical across all 15 runs (maximum relative spread 0.0), so evaluation data and masks are identical. C uses one perm at every seed. Each S seed has a distinct perm, none equal to C.
- **Primary contrasts:**
  - I1 = +0.1468 %, t95 [−0.0677 %, +0.3614 %], df 4, q 2.7764.
  - I2 = +0.4733 %, [+0.00098 %, +0.9455 %].
  - Both equal `verdict.json` to within 1e-12.
- **Fixture gates:**
  - F+ C vs E +3.061 % and C vs S +2.935 %. Per seed: s0 +2.77 % / +2.90 %; s1 +3.35 % / +2.97 %.
  - F− C vs E −1.737 %.
  - Both gates pass.
- **Card §8, applied by hand:** `stop`.
- **Robustness:**
  - The largest I1 upper bound over all leave-one-seed-out sets is 0.474 %, still < δ.
  - Even with C and E swapped, the upper bound would be 0.068 %.
  - The margin to δ is 0.64 percentage points.
- **Post hoc without seed 2:** reproduces addendum 04.
- **My own paired hierarchical bootstrap** (different RNG and seed): I1 [+0.024 %, +0.291 %] against the worker's [+0.025 %, +0.292 %]; I2 [+0.254 %, +0.825 %] against [+0.256 %, +0.825 %].
- **Ledger:** recomputed from launch and end times as 11.677 GPU-h for the waves, plus 0.04 for smoke. This matches the reported 11.73 (rounded up per wave).

### Permutation properties (`perm_properties.py`)

My own child-slot geometry comes from ver11's `x[:, :, i::2, j::2, k::2]` slicing of an index volume. Every perm in `perms_hcp`, `perms_Fplus` and `perms_Fminus` (E, C, S_seed*, G, R):
- is a bijection;
- is octant-local;
- leaves untouched blocks as the identity;
- has a Hungarian-optimal box placement and a Hungarian-optimal child-slot order.

The report's counts are confirmed: 1442 cells touching the brain, 1195 signal cells, 234 touching blocks, C regroups 231 blocks, S regroups 231–232.

### B300, node .98 (worker venv used read-only; outputs copied to `b300_outputs/`)

- **Part A (CPU):**
  - The B300 code copy matches the frozen pins (22/22).
  - B300 `run.json` equals the repo copies (27/27).
  - `perms_hcp.npz` on B300 has sha ec05b796… (= pin).
  - In every one of the 15 `model_final.pt`, the persistent `perm` buffer equals `perms_hcp.npz[perm_key]` for its run and no other key. So no arm labels are swapped.
- **Part B (GPU 7, 06:06:51–06:08:36Z, 0.03 GPU-h, ledger rows started and completed under flock):**
  - I re-scored all 15 checkpoints on the 16 TEST subjects with my own code for windowing, padding, voxel-mask expansion and NMSE.
  - My mask generator is asserted equal to the frozen one, and the model's voxel mask is asserted equal to my expansion.
  - Per-subject numerator and denominator agree with `run.json` within 7.5e-8 relative.
  - The re-scored I1 is [−0.0677 %, +0.3614 %] and I2 [+0.00098 %, +0.9455 %], identical to 1e-8.
- **Part C (same GPU):** a one-parameter trivial baseline (copy the nearest unmasked frame of the same voxel; β = 0.0356 fitted on 4 TRAIN subjects) gives test NMSE **0.9984** on the identical masks. All models (0.986–0.993) beat it. S_s2 (1.000) does not.
- **CPU, 4 TRAIN subjects:**
  - Voxel lag-1 / lag-2 autocorrelation is 0.043 / 0.044.
  - The lag-1 autocorrelation of 12 mm cell means is 0.33.
  - The R² of a voxel on its own 12 mm cell mean is 0.047.
  - So the time axis is intact, and only about 4–5 % of the variance of a per-voxel z-scored 2 mm voxel is temporally or spatially predictable.

### Mutation testing (`mutation_harness.py`, `mutation_results.json`)

Setup: 47 mutants of my own, none from the worker's list. Each ran on a mirror copy with the full 55-test suite. The unmutated mirror passes 55/55.

**28 killed.**

**19 survived:**
- Verdict and contrast logic:
  - `stats_stop_uses_mean`: the kill rule "mean < δ" instead of "upper bound < δ" passes every test;
  - `stats_gain_sign_flip` and `stats_gain_div_arm`: the I1/I2 direction and denominator are untested;
  - `script_verdict_I1_swapped` and `script_verdict_ignores_fminus`: `topic2_verdict.py` is untested;
  - `stats_gate_first_seed_only`, `stats_boot_no_seed_resampling`, and the boundary mutant `stats_stop_le_boundary`.
- Primary metric and training loop (the GPU path is untested on CPU):
  - `metrics_no_mask_weight` and `metrics_no_brain_weight`;
  - `train_loss_all_brain_voxels`, `train_eval_masks_same_for_every_subject`, `train_test_uses_val_mask_seed`, `train_mask_seed_differs_by_arm`.
- Partition:
  - `part_no_slot_matching` and `part_no_box_placement_matching`: canonical slot order and placement are untested;
  - `part_mean_link_becomes_max`, `part_signal_threshold_ignored`;
  - `metrics_stage0_pca_insample` (Stage 0 basis fitted in sample).

### Other observations

- **I1 and early stalls.** The positive I1 sits in the seeds where E escaped the trivial plateau late:
  - E's validation NMSE at step 2188 was ≥ 1.0 at seeds 0 and 2;
  - the first step with train loss < 0.995 is 3100/2800 for E against 1900/2300 for C;
  - I1 is 0.235 % and 0.403 % at those seeds;
  - the mean I1 at seeds 1, 3 and 4 is 0.032 %, and at seed 3 C is worse in 0/16 subjects.
- **Addendum 04 loss range.** It says the `hcp_S_s2` train loss "stayed between 0.9997 and 1.0018 for all 8,750 steps". The logged 100-step means after step 100 range from 0.9978 to 1.0036 (1.0561 at step 100).
- **Stale PI decisions.** The card, report and handoff call δ and "HCP counts as public under C6" pending PI decisions. Both were already decided in `PI_DECISIONS` (committed 03:01Z, before the freeze).
- **Missing test file.** `vendor_swift_ver11/SOURCE.md` cites `tests/topic2_rgpool/test_vendor_provenance.py`, which does not exist. The check is in `test_leakage_and_provenance.py::test_vendored_ver11_is_byte_identical_to_recorded_source`.
- **Pseudonyms.** They are `sha256(file content)[:16]` (`data.pseudonym`) of a public HCP file, with no salt.
- **C4 scan.** Worker files edited after the final B300 ID scan contain 0 standalone 6-digit tokens.
  - I also scanned all 83 files under my verification and metadata directories. They contain none of the 88 pseudonyms.
  - That scan found 3 standalone 6-digit tokens. All three equal 50·70·70 or 50·70·70 + 1: the voxel count of a synthetic test volume, printed as an array shape in a mutant's pytest failure log. I give the product rather than the literal, so that future 6-digit ID scans do not flag it.

### Re-checks after all probes (~06:20Z)

| check | result |
|---|---|
| C1 | rc 0, 67/67 |
| code freeze | rc 0, 33/33 |
| card pin | rc 0, 8/8 |
| output pin | rc 0, 43/43 |
| `tests/topic1_lagmotif` (rest of C2; the worker did not run it) | 88 passed |

`git status --porcelain` shows no modification to tracked files under the Topic 2 paths. The docs are tracked and clean. src, tests, scripts and results are untracked, so only the hash pins above cover them. Logs are `logs/*_post.txt` and `logs/tests_topic1_lagmotif.txt`.

### DISPATCH.md

It now contains the verbatim worker JSON, under a dated correction header (06:20Z).

## 2. Logic Chain

1. **The numbers come from real trained models with the claimed perms.** Each checkpoint's `perm` buffer equals its labelled arm's perm (Part A), and re-scoring each checkpoint with independent code reproduces the per-subject numerator and denominator to 1e-7 (Part B). This also rules out swapped arms and missing masks or brain weights in the recorded values. The mutation gaps in the metric and loss code therefore do not affect these results.
2. **Pairing holds.** The denominators are identical across all 15 runs and the subject order is identical, so all arms were evaluated on the same data and masks. The step-0 weight pairing is tested, and the mutant `model_arm_consumes_rng` is killed. Training-mask pairing is not tested (a mutant survives), but the frozen code fixes it to 2000+seed, and every `run.json` carries the frozen code hash.
3. **The freeze predates results.** Third-party commits contain the frozen card bytes at 03:16:27Z, before any HCP training or test number. The partitions date from 03:20Z and the first HCP launch from 03:44Z. Addendum 02 was committed before the first HCP test value. The wave 2–4 job files have mtime ~03:27Z, so the seeds and arms were planned before results.
4. **The verdict follows card §8.** The F+ gate passes. The I1 upper bound is 0.36 % < δ = 1 %, so the rule gives `stop`, and that is robust to dropping any seed or swapping C and E. δ = 1 % was PI-approved before the freeze, which makes the verdict stronger than the worker's "pending" wording suggests.
5. **What "stop" means.** The measuring instrument works: the models beat a trivial baseline (0.9984), and the data's time structure is intact. But only about 4–5 % of voxel variance is predictable (lag autocorrelation 0.043; R² on the cell mean 0.047). E captures about 1.1 % and C about 1.25 %, so δ = 1 % relative NMSE is roughly a quarter of the remaining headroom. "stop" is therefore a kill at this noise-dominated target and budget, as the worker states. It is not evidence against connectome grouping in general. The F+ gate (a planted signal at about 42 % of cell variance) does not certify sensitivity at this operating point. The report says so too (§2.2).
6. **The small sub-δ positive I1 is fragile.** It is concentrated in the two seeds where E stalled early. A plateau-escape effect of optimisation explains it as well as better grouping does. The hierarchical bootstrap's positive lower bound, with only 5 seeds resampled, should not be read as resolving a representational gain.
7. **The survivors are coverage findings, not errors in this result.** Independent recomputation (steps 1–4) covers each surviving mutant's effect on the governed numbers. Several survivors sit in the decision path: the kill rule, the contrast direction and the verdict script. They would let a future defect pass silently.

## 3. Caveats

- **Stage 0** was not recomputed from data. I only checked `stage0_hcp.json` against the report, and both are descriptive.
- **Preprocessing** (crop, pad, z-score) was not rerun from raw NIfTI. Its tests kill my crop/pad/z-score/cell-mean mutants, and the time structure and masks are consistent.
- **Leakage** was checked by reading `topic2_build_partitions.py`. FC and the group mask use `split["train"]` only, and the mutant `script_partitions_fc_uses_all_subjects` is killed. FC was not recomputed.
- **The 5 burned explorer subjects:** I did not verify their exclusion; that would need IDs.
- **No retraining was done**, so the stall in `hcp_S_s2` was not reproduced. It cannot change `stop`.
- **The headroom figure is approximate.** It comes from 4 subjects and 20,000 voxels each, and finer-scale shared signal could add somewhat to the "~4–5 %".
- **Shared B300 GPU 7.** Another verifier used GPU 7 starting at 06:08:54Z, after my job ended at 06:08:36Z. Its ledger row is not mine.
- **The worker's own mutants were not re-mutated.** These are the inverse permutation, silent identity, permute-after-merge, time-mixing and non-bijection mutants. I relied on their tests in `test_merge.py`, which pass, and I wrote 47 new mutants of my own.
- **Worker venv.** I used `/scratch/iitp4/worker_M3_r1/venv/bin/python` on B300 read-only, with no installs. My own B300 files are in `/scratch/iitp4/challenger_M3_r1_2/` (small scripts and JSON; I left them for traceability).

## 4. Conclusion

**CONFIRMED.**
- **T2.1:** the code facts are verified by reading the vendored ver11 and by the passing tests.
- **T2.2:** the card was frozen before results. The implementation's invariants hold on the saved perms. The fixtures pass.
- **T2.3:** the verdict `stop (killed)` follows the card. The headline numbers reproduce from the raw records and from the saved checkpoints.

### Non-blocking issues, most important first

1. **Test-suite gaps in the decision path.** Mutants survive for the kill rule (mean vs upper bound), the I1/I2 direction and denominator, `topic2_verdict.py`, the masked in-brain metric weighting, training/evaluation mask pairing, and canonical slot order and placement. The fix is to add `S.verdict(_ci(0.005, -0.005, 0.015), …) == "inconclusive"`, a `relative_gain` direction test, an end-to-end test of `topic2_verdict.py` on synthetic `run.json` files, a `masked_sq_terms` hand-check, and a slot-order/placement oracle.
2. **The sub-δ positive I1 comes from early-plateau seeds** (0 and 2). This needs a caveat beside the bootstrap "resolves a positive gain" sentence.
3. **The headroom gives δ context.** Only about 4–5 % of voxel variance is predictable, so δ = 1 % ≈ a quarter of the headroom. The report should give this context. Option A in report §7 (a lower-noise target) is the natural follow-up.
4. **Stale "pending PI" statements** on δ and on HCP under C6, in the card (frozen, so correct via addendum), the report and the handoff. The PI decided both before the freeze.
5. **Pseudonyms are unsalted content hashes of public files.** Anyone with HCP OA access can recompute the mapping to HCP subject IDs. C4 asks for a "positional index or salted hash", so this needs a root/PI decision.
6. **Small inaccuracies:** the addendum 04 S_s2 loss range, and the test file path cited in SOURCE.md.

None of these changes the verdict.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/challenger_M3_r1_2/recompute_from_runs.py $PWD /tmp/x.json   # expect checks_failed []
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/challenger_M3_r1_2/perm_properties.py $PWD /tmp/y.json
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/challenger_M3_r1_2/mutation_harness.py $PWD /tmp/mut /tmp/m.json --jobs 4   # 28 killed / 19 survived
git show 51609c1:docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md | sha256sum   # c9bfc60a...
# B300 (.98): /scratch/iitp4/challenger_M3_r1_2/b300_reeval.py WORKER_DIR frozen_pins.txt repo_runs_sha.txt OUT.json (1 idle GPU, ~2 min)
```

The verdict is invalidated if any of these happen:
- a `model_final.pt` perm buffer differs from its label;
- re-scoring departs from `run.json` by more than 1e-6 relative;
- a card commit earlier than 51609c1 has different bytes;
- `PROTECTED_HASHES` fails.

The SHA-256 hashes of everything tested are in `verification/challenger_M3_r1_2/logs/tested_artifact_sha256.txt`.
