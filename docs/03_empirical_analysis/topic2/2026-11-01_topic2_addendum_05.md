# Topic 2 card — addendum 05 (2026-11-01, worker_M3_r2, written ~08:20Z, AFTER all results)

Everything below is post hoc. No governed computation changed: no training, no Stage 0, no preprocessing and no
partition was rerun, no frozen file was edited (card, architecture note, result report, addenda 01–04,
`src/topic2_rgpool/**`, frozen `scripts/topic2_*.py`, frozen tests, `vendor_swift_ver11/SOURCE.md`;
`code_sha256_at_freeze.txt` still 33/33). The card verdict stays **stop** (`results/topic2/2026-11-01/verdict.json`,
sha256 59af05e5…caf68, unchanged). GPU used by this iteration: 0 GPU-h.

## 1. Why this addendum exists: the r1 gate

The M3 r1 gate failed on one blocking issue, B1 (ACCEPTANCE C4), raised by reviewer_M3_r1_1; the other four
verifiers (reviewer_M3_r1_2, both challengers, the auditor) passed and reproduced the verdict. B1: the repo copies
of the results identified subjects by an unsalted content-hash prefix (`src/topic2_rgpool/data.py` `pseudonym()`),
and `hcp_manifest.json` also stored each file's full content sha256 and exact size. Anyone holding the staged HCP
files or an HCP file listing could map every token to an HCP subject ID by hashing or by size. C4 asks for a
positional index or a salted hash. A further per-file fingerprint that r1 did not list was also present: the
per-subject brain-voxel count (87 distinct values over 88 subjects), plus the per-file processing time.

## 2. Remediation (a deviation from card §4, line 81)

Card §4 line 81 says subjects are identified by the first 16 hex characters of the file-content sha256. That rule
is withdrawn for every repo copy. The originals are kept, sealed off-repo, so the card's frozen-input pins stay
verifiable.

**Rule** (`scripts/topic2_c4_sanitize.py`, new, standard library only, non-governing):
- Token map: subject at position i of the original manifest's `subjects` list → `h%02d` (h00 … h87). That list is
  sorted by content sha256 (asserted), so every list that was sorted by the old token keeps its order. Per-subject
  arrays are not reordered: the hierarchical bootstrap in `verdict.json` depends on subject order.
- `hcp_manifest.json`: each subject becomes `{pseudonym, qc, T}`; `content_sha256`, `file_bytes`, `n_brain_vox`
  and `sec` are dropped; a `c4_sanitized` block records the rule and the original file's sha256.
- `split.json`, `stage0_hcp.json` and the 15 `runs/hcp_{E,C,S}_s{0..4}/run.json`: only the quoted token values are
  replaced (checked by re-parsing); no key and no other value changes.
- `logs/preprocess.log`: per-subject lines keep `done`, `of`, `qc` and the new token; the per-file `sec` is dropped.
- Kept on purpose: the embedded FILE hashes `split.json` `manifest_sha256`, every hcp `run.json`
  `split_file_sha256`, and the split hash quoted in `partitions/partitions_hcp.json` and
  `logs/build_partitions_hcp.log`. They record what the governed runs read, so they now verify against the sealed
  originals, not against the sanitized repo copies.
- Every other file is byte-identical, including `verdict.json`, `posthoc_sensitivity_without_seed2.json`, the
  partitions, all fixture runs, the other logs, `id_scan_b300.json` and both old pin files.

**Sealed originals.** The 19 original files are on B300 node 61.107.201.98 at
`/scratch/iitp4/worker_M3_r2/sealed_c4/<repo-relative path>` (directories 700, files 400), copied ~07:28Z by tar
over ssh. Their sha256 values are in `results/topic2/2026-11-01/c4_sealed_originals_sha256.txt` (file hashes, no
subject token). 18 of them equal the old pins; `logs/preprocess.log` was pinned nowhere before and is recorded
there for the first time. The original hashes are also anchored in committed run metadata (for example manifest
26ba34a9…, split c13b5f21…, stage0 61da22af…, `card_sha256.txt` 167b9191…, `output_sha256.txt` 5ae1bc38…, all
quoted in r1 verifier dispatches at HEAD). /scratch is wiped when the VM stops: a durable copy outside every git
repository is a root action (§7).

The workflow asked for prior bytes of changed files in `verification/worker_M3_r2/prev_snapshot/`. That directory
is inside the repository, and copying the token-bearing originals there would recreate B1, so it holds only a
pointer file (`POINTER_sealed_originals.md`). C4 outranks that instruction; this is a recorded deviation.

**What the old pins now show.** In the repo, `card_sha256.txt` fails on exactly 2 lines (`hcp_manifest.json`,
`split.json`) and `output_sha256.txt` on exactly 16 (`stage0_hcp.json` and the 15 hcp `run.json`). This is by
design: those 18 pinned hashes equal the sealed originals, and they pass on the sealed root. The report's §8 card
check (`grep -v '^#' card_sha256.txt | sha256sum -c`) therefore fails on those 2 lines in the repo; use the checker
below. New pin files (dated, additive): `c4_sealed_originals_sha256.txt` (19 originals), `c4_sanitized_sha256.txt`
(19 sanitized copies) and `output_sha256_r2.txt` (complete current state of the Topic 2 outputs, new scripts, new
tests and this addendum).

r1 verifier receipts that compared the repo run records with the B300 copies, or the repo files with the old
pins (for example "27/27 B300 run.json == repo copies"), now hold against the sealed originals only; the B300 copies
under `/scratch/iitp4/worker_M3_r1/` equal the sealed originals, not the sanitized repo copies.

**Checks run** (outputs in `verification/worker_M3_r2/`):
- `scripts/topic2_c4_seal_check.py repo`: R1 sanitized copies = pins (19/19); R2 old pins: 33 lines pass, exactly
  the 18 expected lines fail and each equals its sealed-original hash; R3 embedded provenance = sealed originals;
  R4 tokens consistent across manifest, split, runs, Stage 0 and log, no fingerprint field; R5
  `output_sha256_r2.txt` passes.
- On B300 with the system python (standard library only), `scripts/topic2_c4_seal_check.py sealed`: S1 sealed
  files = `c4_sealed_originals_sha256.txt` (19/19); S2 the 18 old pin lines pass on the sealed root; S3 re-running
  the sanitizer on the sealed originals reproduces `c4_sanitized_sha256.txt` exactly (19/19); S4 the originals'
  embedded provenance is self-consistent; S5 the split recomputed from the original manifest with the public salt
  equals the sealed `split.json` (64/8/16).
- The frozen `scripts/topic2_verdict.py` run on the relabelled run records reproduces `verdict.json` byte for byte
  in the environment that wrote it (DGX-Spark superclaude-env: numpy 2.3.5, scipy 1.15.3). In the B300 venv
  (scipy 1.18.1) the only difference is the t quantile and the interval ends, at ≤ 9e-13 relative; the new test
  therefore compares numbers to 1e-9 relative and the verdict exactly.
- The 55 shipped tests pass on the relabelled outputs; the frozen `test_outputs_no_ids.py` passes (it never checked
  the run lists, content hashes or sizes, which is why it could not catch B1).
- Count-only token scans (tokens held in memory only): before the change exactly the 19 files carried tokens (plus
  three unrelated numeric coincidences in Topic 4 files); after it, 0 files in the working tree. Git history since
  2026-10-30: 0 commits with a token.

**Commands.**
```
cd /home/juke/git/00IITP-AI
python3 scripts/topic2_c4_seal_check.py repo
LC_ALL=C sha256sum -c results/topic2/2026-11-01/c4_sanitized_sha256.txt
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c
# on B300 61.107.201.98, with the four pin files copied to PINS (no token in any of them):
python3 scripts/topic2_c4_seal_check.py sealed --sealed /scratch/iitp4/worker_M3_r2/sealed_c4 --pins PINS
cd /scratch/iitp4/worker_M3_r2/sealed_c4 && (grep -v '^#' PINS/card_sha256.txt; grep -v '^#' PINS/output_sha256.txt) | sha256sum -c --ignore-missing
```

## 3. Residual linkage (disclosed, not closed)

After the change the repo holds no content hash, size, voxel count or timing of any subject file. A data holder
can still re-link positions to subjects: hashing the 88 staged files and sorting gives the manifest order (= the
token numbers); the public split salt gives the split; and the per-subject values (`test_den`, the Stage-0
per-subject arrays, `per_subject_nmse_seedmean` in `verdict.json`) can be matched by rerunning the pipeline. This
needs the exact staged file set, which exists on B300, where the HCP directory names already are the IDs. It is
inherent to publishing per-subject results of a reproducible public-data analysis. The scheme meets the letter
of C4 (positional index) and is the scheme this run already accepted for M1 (`scripts/topic1_run_cohort.py:10`,
"subjects are positional indices into sorted(os.listdir(npy_dir))"; M1 passed its gate and victory audit).

A keyed token (HMAC under an off-repo key; explorer_M3_r2_2's proposal) leaves the same residual, because the
split lists and the run test lists keep their old order, which a data holder can recompute; it also needs a key
store outside every git repository. Stricter options, for root or the PI to choose: reorder every per-subject array
under a secret key (this changes the bootstrap bytes of `verdict.json`, i.e. a new governed output) or keep only
aggregates in the repo and the per-subject records off-repo.

## 4. Corrections to frozen or pinned documents (errata; the documents themselves are not edited)

1. **PI decisions predate the freeze.** PI decisions 2 (HCP-YA Open Access counts as public under C6, subject to the
   HCP Data Use Terms) and 3 (δ = 1 % relative held-out masked NMSE for M3) were first committed in a06f435 at
   03:01:27Z; the card was frozen at 03:14:34Z (first committed in 51609c1 at 03:16:27Z). The statements "pending
   PI confirmation" / "set by the worker" in card §4 (line 75) and §8 (line 161) and in the result report (lines
   12, 216, 218) are superseded: δ and the C6 status were fixed by the PI before any governed result.
2. **Provenance test name.** `vendor_swift_ver11/SOURCE.md` line 12 cites `tests/topic2_rgpool/test_vendor_provenance.py`,
   which does not exist. The check is
   `tests/topic2_rgpool/test_leakage_and_provenance.py::test_vendored_ver11_is_byte_identical_to_recorded_source`.
3. **Addendum 04, stalled run.** "Training loss stayed between 0.9997 and 1.0018 for all 8,750 steps" is wrong.
   The logged 100-step means of `hcp_S_s2` are 1.0561 at step 100 and 0.9978–1.0036 from step 200 on. The val and
   test statements there are correct.
4. **I2 is not purely "connectome-specific".** The S boxes are less compact than the C boxes (mean distance of a
   box's signal cells to its centroid: E 0.784, G 1.112, C 1.469, S 1.557–1.674 over seeds 0–4, R 2.457 cells;
   recomputed from `partitions/perms_hcp.npz` with `metrics.dispersion`, equal to `partitions_hcp.json`). Stage-1
   I2 > 0 is therefore confounded with compactness and cannot be credited to FC specificity alone. Stage 0's C − G
   r contrast (G more compact than C) does support FC information beyond distance at the cell level.
5. **Per-seed I1 tracks plateau-escape timing** (descriptive, post hoc). First step whose 100-step training-loss
   mean fell below 0.995: E 3100 / 1800 / 2800 / 1600 / 1100, C 1900 / 1400 / 2300 / 1700 / 1100 for seeds 0–4.
   Per-seed I1: +0.235 %, +0.069 %, +0.403 %, −0.035 %, +0.062 %. The two largest I1 values are the seeds where E
   left the predict-zero plateau last (0 and 2). This is consistent with `stop` and does not change it.
6. **Report §3.4** ("+13.1 % of E's explained variance") is a post hoc re-expression and governs nothing; the
   governed quantity is relative NMSE.
7. **Reconstruction ceiling.** In E36 each final token is 288-d and `decoder_spatial_expand` is
   Linear(288 → 48³) (vendored ver11 lines 1135–1148), so each octant-frame is decoded from one 288-d
   vector. This is a plausible contributor to the ~1 % explained variance of every arm; report §7 options A (lower-
   noise target), D (E192) and E (probe on the saved checkpoints) address it more directly than B (longer budget).
8. **Latent default in the verdict script.** `scripts/topic2_verdict.py:66` passes `fm is not False`, so a MISSING
   F− gate would count as a pass. In this run both gates were computed (F− pass = true), so nothing changes. The
   frozen script is not edited and no test asserts the opposite (it would fail on frozen code).
9. **CUDA visibility in r1 test commands.** `train.run` uses CUDA whenever it is visible, so an r1 "CPU smoke" run
   with the local GB10 visible used the GPU. Every r2 test command sets `CUDA_VISIBLE_DEVICES=""`.
10. **r1 handoff timestamps.** worker_M3_r1's final check files are dated 05:30–05:34Z and its DISPATCH.md 05:37Z;
    the "re-check ~05:42Z" and "correction 05:40Z" times in its handoff are later than the files.

## 5. New guard tests (additive; every one passes on the frozen code)

- `tests/topic2_rgpool/test_c4_tokens_r2.py` (8): positional tokens consistent across all files; no fingerprint
  field; no 16-hex token shape and no stray 64-hex hash in `results/topic2` or `docs/03_empirical_analysis/topic2`
  (a precise detector: a naive `[0-9a-f]{16}` matches the digits of every float); embedded provenance equals the
  sealed-original hashes.
- `tests/topic2_rgpool/test_verdict_path_guards_r2.py` (10): kill rule on the upper bound with a strict boundary;
  `relative_gain` sign and denominator; fixture-gate seed averaging; bootstrap seed resampling; the verdict script
  end to end (I1/I2 roles, both fixture gates, keep/stop paths, the shipped verdict reproduced). Four of these and
  the NMSE-weighting test below are adopted from `verification/explorer_M3_r2_2/proposed/test_verdict_path_guards_r2.py`.
- `tests/topic2_rgpool/test_pipeline_guards_r2.py` (19): masked in-brain weighting of the NMSE terms; Stage-0 PCA
  basis; the SimMIM loss mask; identical training data and masks across arms; per-subject evaluation-mask seeds;
  test pass on the test subjects with the test mask seed; split order and disjointness; the octant check on a
  swap of signal cells; the default growth rule of both `build_perm` and `build_boxes` (dense-core seed, mean
  linkage, seed-independent C and G) and an independent reference implementation of it; the signal threshold;
  Hungarian optimality of box placement and child-slot order.

Mutation testing (`verification/worker_M3_r2/mutation/`, all 103 mutants of the three r1 harnesses, explorer_M3_r2_2
and 7 data mutants for the C4 guard, CPU only on B300 .98 with CUDA hidden): see §5a.

### 5a. Mutation table

Harness `verification/worker_M3_r2/mutation/run_mutants_r2.py` (an adapted copy; the r1 harnesses were not re-run in
place). Each mutant: one exact text edit in a fresh mirror outside the repository, the full current
`tests/topic2_rgpool` suite with `-x`; rc 1/2 = killed, rc 0 = survived, timeout or signal = INVALID (never a kill).
- v1, local DGX-Spark, 4 jobs: INVALID. The host was out of memory (other workloads); earlyoom sent SIGTERM to
  the test processes, the unmutated baseline included. Kept in `mutation/v1_local_earlyoom/`.
- v2, B300 .98 CPU (project-local venv: torch 2.15.0, numpy 2.5.4, scipy 1.18.1; pytest 8.4.2 in
  `/scratch/iitp4/worker_M3_r2/pydeps`), 6 jobs: baseline passes (91 tests); 101 of 102 mutants killed, 0 INVALID,
  0 malformed. The one survivor, c1:m18 (default growth rule of `build_boxes` switched to random), changed only the
  default of `build_boxes`, which the governed path never uses (`build_perm` passes `algo` explicitly).
- v3, same node, after adding `test_build_boxes_default_is_the_deterministic_dense_mean_rule`: baseline passes
  (92 tests) and c1:m18 is killed. A mutant killed by a suite stays killed when tests are added, so all 102 are
  killed.

All 42 mutants that survived in r1 (or in explorer_M3_r2_2's probe) are now killed; the killing test is the first
failure under `-x`:

| mutant (r1 harness) | killed by |
|---|---|
| stats_stop_uses_mean, e2 M1 | test_kill_rule_uses_the_upper_bound_not_the_mean |
| stats_stop_le_boundary | test_kill_rule_boundary_is_strict |
| m08, stats_gain_sign_flip, stats_gain_div_arm, au relative_gain_sign_flip, e2 M2 | test_relative_gain_sign_and_reference_denominator |
| stats_gate_first_seed_only | test_fixture_gates_average_over_seeds |
| stats_boot_no_seed_resampling | test_hierarchical_bootstrap_resamples_seeds |
| m29, script_verdict_I1_swapped, e2 M3 | test_verdict_script_wires_I1_I2_and_both_fixture_gates[keep] |
| m30, script_verdict_ignores_fminus, e2 M4 | test_verdict_script_wires_I1_I2_and_both_fixture_gates[fminus_bias_downgrades_keep] |
| m20, m21, metrics_no_brain_weight, metrics_no_mask_weight, au nmse_ignores_mask, e2 M5 | test_masked_sq_terms_counts_only_masked_brain_voxels |
| metrics_stage0_pca_insample | test_stage0_retention_uses_the_supplied_train_basis |
| m22, train_loss_all_brain_voxels, au train_loss_ignores_mask | test_training_loss_is_masked_in_brain_mse |
| m23, m24, train_mask_seed_differs_by_arm | test_arms_share_training_data_and_masks_for_a_seed |
| train_eval_masks_same_for_every_subject, au eval_mask_seed_per_run | test_evaluation_masks_are_seeded_per_subject_position |
| m32, train_test_uses_val_mask_seed | test_test_pass_uses_test_subjects_and_test_mask_seed |
| m31 | test_split_script_writes_disjoint_lists |
| au split_test_from_end | test_assign_split_takes_test_then_val_from_the_front_of_the_salted_order |
| m15 | test_validate_perm_rejects_a_cross_octant_swap_of_signal_cells |
| m18 | test_build_boxes_default_is_the_deterministic_dense_mean_rule (v3) |
| part_mean_link_becomes_max | test_default_growth_rule_is_dense_core_with_mean_linkage |
| part_signal_threshold_ignored | test_octant_cells_split_signal_and_filler_by_threshold |
| m19, part_no_slot_matching, part_no_box_placement_matching | test_box_placement_and_child_slots_are_hungarian_optimal[C] |

Data mutants D1–D7 (a synthetic 16-hex token in a run record or in a docs file; `file_bytes`, `n_brain_vox` or
`content_sha256` re-added to a manifest subject; `sec` re-added to a log line; one run's test order altered) are
all killed by `test_c4_tokens_r2.py`.

## 6. C4 print incidents (for root's record; nothing was written to any file)

- worker_M3_r1 (~03:32Z): one hand-typed public-documentation example HCP ID in local tool output (self-disclosed).
- explorer_M3_r2_1: a `head -c` peek printed a 6-hex partial prefix of one old token and a 4-hex partial prefix of
  one content hash in local tool output (self-disclosed).
- worker_M3_r2 (~07:27Z): a structure probe of `logs/preprocess.log` masked digits before hex runs, so one masked
  line showed the letter positions (6 of 16 characters) of one old token in local tool output.

## 7. Compute, and items for root

- r1's four training waves (03:16–05:09Z, 11.7 GPU-h) were launched directly on idle GPUs before B300 ran Slurm
  (RESUME addendum 3). r2 used 0 GPU-h; B300 CPU was used for the sealed-root check and the mutation run (CUDA
  hidden, nice, 6 processes on a 224-core node).
- Root actions: (1) a durable copy of `/scratch/iitp4/worker_M3_r2/sealed_c4` outside every git repository before
  the VM stops; (2) the explorer salt `verification/explorer_M3_r1_1/dev_subject_salt.txt` (outside this worker's
  ownership, untouched; a copy also sits in `/scratch/iitp4/worker_M3_r1/code/scripts/`); (3) a ruling on this
  positional scheme versus the stricter options in §3; (4) the print incidents above; (5) B300 cleanup of
  `/scratch/iitp4/worker_M3_r1` (keep the 15 checkpoints if option E is wanted).
