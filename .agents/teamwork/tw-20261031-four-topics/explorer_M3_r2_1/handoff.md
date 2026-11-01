# Handoff — explorer_M3_r2_1 (M3 / Topic 2, iteration 2, explorer 1 of 2)

Type: Hard handoff (fix strategy for the last M3 iteration). Written 2026-11-01 ~07:30Z.
Probes and outputs: `/home/juke/git/00IITP-AI/verification/explorer_M3_r2_1/`. GPU used: 0. Git writes: none. Installs: none.

**Summary.** The r1 gate failed for one reason: reviewer_M3_r1_1's blocking issue B1 (C4). The repo-side subject tokens are unsalted content-hash prefixes, stored next to full content hashes, unique file sizes and (not noticed in r1) per-subject brain-voxel counts. All other r1 verifiers passed, and the science (STOP verdict) reproduced several times. The fix needs no GPU, no retraining and no change to any frozen file. My probe shows that relabeling the tokens to positional `h00..h87` in manifest order works: the frozen `scripts/topic2_verdict.py` run on the relabeled run records reproduces `verdict.json` **byte for byte**, and the frozen C4 test still passes. M3 is at MAX_ITER = 2 (`workflows/scripts/teamwork-four-topics-b-wf_5bb8fefb-ae0.js:10`). r2 is therefore the last iteration: one non-pass verdict from any of the 5 verifiers sends M3 to the PI. The worker should also close the cheap non-blocking findings, above all the surviving verdict-path mutants that failed M2 twice.

## 1. Observation

**Gate record (in my DISPATCH.md, verbatim).** Gate = `FAIL (reviewer_M3_r1_1 REQUEST_CHANGES)`; reviewer_M3_r1_2 APPROVE, both challengers CONFIRMED, auditor CLEAN. B1 text: "data.pseudonym() is an unsalted sha256(NIfTI bytes)[:16] … hcp_manifest.json also stores … the full 64-hex content_sha256 and the exact file_bytes … Anyone with the lab-staged HCP directory on B300 or an HCP-OA file listing can map every token to an HCP subject ID, from file size alone or by hashing." The reviewer's own fix: positional indices or an HMAC under an off-repo key; drop content_sha256 and file_bytes; originals kept off-repo with their sha256 so the frozen pins stay verifiable; a dated addendum and a new dated pin file without overwriting `output_sha256.txt`; a test that rejects such tokens. "If root or the PI rules that HCP-OA ID linkage is acceptable … APPROVE."

**O1 Code.**
- `src/topic2_rgpool/data.py:84-85`: `def pseudonym(content_sha256): return content_sha256[:16]`.
- `data.py:88-89`: `split_order` sorts by `sha256(split_salt + p)`. The salt is public: `scripts/topic2_make_split.py:20` default `"topic2-m3-split-2026-11-01"`, and the card §4 states it.
- `scripts/topic2_preprocess_hcp.py:35`: `rec.update(content_sha256=sha, pseudonym=D.pseudonym(sha), file_bytes=os.path.getsize(path))`; `:47`: `n_brain_vox=int(mask.sum())`; `:79`: `recs.sort(key=content_sha256)`.

**O2 Card (frozen).** `docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md:81` "Subjects are identified only by the first 16 hex characters of the sha256 of the file content." `:73` "Only aggregate results, partitions and pseudonymous per-subject error terms leave B300." The identification rule is itself what B1 objects to, so the remediation is a deviation from card §4 and must go in an addendum.

**O3 Structure** (`probe_structure.py`; every string masked).
- Manifest `subjects` is 88 entries of `{content_sha256 (64 hex), pseudonym (16 hex), file_bytes, qc, n_brain_vox, T, sec}`.
- split.json holds `train/val/test` lists of 16-hex tokens plus `manifest_sha256` and `salt`.
- stage0_hcp.json has `test_pseudonyms_order` (16 entries) plus per-subject `r_mean`/`pca2` arrays.
- Each HCP run.json has `test_pseudonyms`, `test_num`, `test_den` (16 entries each) and `split_file_sha256`.
- verdict.json has no tokens but holds `stage1.per_subject_nmse_seedmean` (16 entries per arm).

**O4 Count-only token scan** (`probe_token_scan.py` v2 → `probe_token_scan.out.json`). Tokens are held in memory only. 16,427 files scanned; 26 have hits.
- The 19 files reviewer_1 listed, all in `results/topic2/2026-11-01/`:
  - hcp_manifest.json: 88 full hashes, 88 pseudonyms, 88 file_bytes values, 88 n_brain_vox values;
  - split.json: 88;
  - stage0_hcp.json: 16;
  - logs/preprocess.log: 88;
  - the 15 runs/hcp_*/run.json: 16 each.
- **n_brain_vox is a further per-file fingerprint** that r1 did not flag: 87 distinct values over 88 subjects.
- explorer_M3_r1_1's `dev_subject_salt.txt`: the salt, 1 occurrence. Its `dev_subjects_BURNED.md`, `probe_stage0_hcp_dev.log` and `probe_stage0_hcp_dev.out.json` each hold the 5 burned salted hashes. The salt string appears nowhere else in the repo tree.
- Three numeric coincidences matching an n_brain_vox value occur in Topic 4 files (`results/topic4/2026-11-01/confirm/fold4_psp_C0.json`, plus copies under `verification/{victory_M4,auditor_M4_r1_1}`). These are unrelated numbers, not tokens.
- No hit in any `.agents/teamwork` metadata file or any `docs/` file.

**O5 Git history.** `git grep -c -F -f <(tokens) $(git rev-list --all --since=2026-10-30)` over 44 revisions (88 pseudonyms + 5 burned hashes + salt; patterns piped, never written): rc 1, 0 hits. A positive control on the split-salt string finds the card. `git ls-files results/topic2 …` gives 0 tracked files; `*.log` is gitignored (`.gitignore:27`).

**O6 Auto-commit scope.**
- The root checkpoint job (`/tmp/claude-1000/-home-juke/1157b38c-…/scratchpad/autocommit/autocommit.sh`) commits `docs/03_empirical_analysis/topic*/**` and `.agents/teamwork/tw-…-four-topics/**/*.md` (`.md`/`.txt`) every 15 min. Its guard greps an ID list (`ids.txt`); pseudonyms are not on that list. Commits continue (latest a910c53 at 06:31Z), and my own DISPATCH.md is already at HEAD.
- `chavis-autocommit` currently logs "Skipping repo 00IITP-AI due to external collision (autocommit.sh)". If the root job stops, chavis-autocommit's own allowlist would apply.

**O7 Ordering invariants (booleans only).**
- The manifest is sorted by pseudonym, and all split lists are sorted.
- All 15 run test orders equal `split.test`, and the stage0 order also equals `split.test`.
- `test_den` is identical across the 15 runs, with 16 distinct per-subject values.
- `split.manifest_sha256` equals sha256(manifest file), and every run's `split_file_sha256` equals sha256(split.json).

**O8 R1 feasibility** (`probe_sanitize_r1.py` → `.out.json`). I built a relabeled mirror in a throw-away scratchpad directory, now deleted.
- Token map `h%02d` = index in the content-hash-sorted manifest. Manifest entries became `{pseudonym, qc, T, sec}`; the other files got a textual replacement of each quoted token.
- Results:
  - frozen verdict script: rc 0, output **byte-identical** to `verdict.json` (sha prefix 59af05e53239 = pinned 59af05e5…);
  - frozen `test_outputs_no_ids` functions: pass;
  - variant without the `pseudonym` key: `FAIL KeyError` (`tests/topic2_rgpool/test_outputs_no_ids.py:32` builds `known = {s["pseudonym"] …}`);
  - residual token scan of the mirror: none.
- `scripts/topic2_verdict.py:59` uses `test_pseudonyms` only for an equality assertion. `stats.hierarchical_bootstrap` (`src/topic2_rgpool/stats.py:32-54`) depends on subject order, so any reordering would change the bootstrap numbers.

**O9 Pins.**
- `card_sha256.txt` pins hcp_manifest.json and split.json. `output_sha256.txt` pins stage0_hcp.json and the 15 HCP run.json. `logs/preprocess.log` is pinned nowhere.
- The hashes of the original manifest (26ba34a9…), split (c13b5f21…), stage0 (61da22af…), verdict (59af05e5…), card_sha256.txt (167b9191…) and output_sha256.txt (5ae1bc38…) already sit in committed metadata at HEAD (`git grep -l` finds 2–6 committed `.agents` files each).

**O10 Frozen test scope.** The frozen C4 test (`test_outputs_no_ids.py`) checks only `"pseudonym": "<16hex>"` values, ID-path regexes and npz dtypes. It never inspects `test_pseudonyms` lists, content hashes or file sizes, which is why it could not catch B1. Its ID_PATHS regexes (`:17-18`) also scan `docs/03_empirical_analysis/topic2/`.

**O11 Workflow facts** (`teamwork-four-topics-b-wf_5bb8fefb-ae0.js`).
- `MAX_ITER = 2` (`:10`).
- The gate passes only if the auditor is CLEAN, both reviewers APPROVE, both challengers CONFIRMED and the worker is DONE (`:96-106`).
- The r2 worker is told: "Previous worker output exists in these paths; you own them now. Preserve prior bytes of anything you change in verification/worker_M3_r2/prev_snapshot/" (`:79`). That path is inside the repo.
- M3 ownership includes `results/topic2/2026-11-01/`, `docs/…/topic2/`, `scripts/topic2_*.py`, `tests/topic2_rgpool/`, `src/topic2_rgpool/` and B300 `/scratch/iitp4/` (`:43`). It does **not** include `verification/explorer_M3_r1_1/` or any location outside the repo on DGX-Spark.

**O12 B300 (read-only, `ssh connectome@61.107.201.98`).**
- The salt has a copy at `/scratch/iitp4/worker_M3_r1/code/scripts/dev_subject_salt.txt`.
- `/scratch/iitp4` holds worker_M3_r1 142 G, explorer_M3_r1_1 5.5 G, explorer_M3_r1_2 5.5 G and small verifier dirs. The original runs exist at `/scratch/iitp4/worker_M3_r1/runs/`.
- Slurm is present (`sinfo`: gpu/interactive/debug, 3 nodes mixed, 1 allocated).

**O13 Salt.** `dev_subject_salt.txt` is 32 hex characters (128 bits). Without it the 5 salted hashes cannot be brute-forced.

**O14 PI decisions predate the freeze.** PI_DECISIONS items 2 (HCP-OA public under C6) and 3 (δ = 1 % for M3) were first committed in a06f435 at 03:01:27Z. The card was frozen at 03:14:34Z (committed 51609c1, 03:16:27Z). Yet card §4/§8 (`:75`, `:161`) and report §0/§6 (`result_report.md:12`, `:216`, `:218`) say "pending PI" or "set by the worker".

**O15 M1 precedent.** `scripts/topic1_run_cohort.py:10`: "subjects are positional indices into sorted(os.listdir(npy_dir))". The M1 manifest has 1706 rows keyed by `position`, each with site, TR and lengths. M1 passed its 5-verifier gate and the victory audit (VERIFIED_COMPLETE, GATE_STATUS.md). Positional indices whose order anyone holding the data can recompute are therefore the C4 standard this run has already accepted.

**O16 Surviving mutants** from r1, collected from `verification/challenger_M3_r1_1/mutation/mutants.out.json`, `verification/challenger_M3_r1_2/mutation_results.json` and `verification/auditor_M3_r1_1/mut/mutants_result.json` (names as in those files):

| Path | Survivors |
|---|---|
| `stats.py` (verdict path) | stats_stop_uses_mean (kill rule tested on the mean instead of the upper bound); stats_stop_le_boundary; m08 / stats_gain_sign_flip / relative_gain_sign_flip; stats_gain_div_arm; stats_gate_first_seed_only; stats_boot_no_seed_resampling |
| `scripts/topic2_verdict.py` | m29 / script_verdict_I1_swapped; m30 / script_verdict_ignores_fminus |
| `metrics.py` | m20 den unmasked; m21 num includes visible voxels; metrics_no_brain_weight; metrics_no_mask_weight; nmse_ignores_mask; metrics_stage0_pca_insample |
| `train.py` | m22 / train_loss_all_brain_voxels / train_loss_ignores_mask; m23 data order arm-dependent; m24 / train_mask_seed_differs_by_arm; train_eval_masks_same_for_every_subject; train_test_uses_val_mask_seed; eval_mask_seed_per_run; m32 val used for test |
| `make_split` | m31 split overlap; split_test_from_end |
| `partition.py` | m15 octant check skipped (the shipped test passes for the wrong reason); m18 random seed rule; part_mean_link_becomes_max; part_signal_threshold_ignored; part_no_box_placement_matching; m19 / part_no_slot_matching |

The frozen verdict script also has a latent defect: `S.verdict(..., fm is not False)` (`scripts/topic2_verdict.py:73`) treats a missing F− gate as a pass. It has no effect in this run: both gates were computed, and F− affects only a would-be "keep".

## 2. Logic Chain

1. Only B1 blocked (gate record), and every other verifier reproduced the verdict. Iteration 2 must therefore remove the linkage without changing any governed computation (C3/C8). Retraining, rerunning Stage 0 and GPU are all unnecessary (O8).
2. The linkable material is wider than B1 listed. Besides `content_sha256` and `file_bytes`, `n_brain_vox` (O4) is computable by anyone holding a file, and per-subject processing `sec` tracks file size. All four must leave the repo copies. Keeping one would let a fresh reviewer reopen B1 on the same argument.
3. Positional tokens in manifest order (= content-hash-sorted order) keep every list's sort order (O7). Relabeling is therefore a pure renaming: the frozen verdict script reproduces `verdict.json` byte for byte, and the frozen C4 test passes (O8). No pinned governed output changes.
4. A residual channel remains, and B1's wording ("by hashing") reaches it. Someone holding the 88 staged files can hash them, sort, and map rows to IDs. `test_den` (O7) is a second data-derived fingerprint. Closing this needs either a secret reordering of every per-subject array or an aggregate-only repo. A reordering changes the bootstrap (O8) and leaves `verdict.json`'s per-subject list in hash order, so it gains nothing. An aggregate-only repo (R2) rewrites `verdict.json` (the governed output), stops the frozen verdict script from running on repo copies, and pulls in other agents' verification outputs.
   - The residual is exactly the M1 design (O15), which passed its gate and victory audit. It satisfies the C4 letter ("positional index").
   - The only people who can exploit it already hold the data, whose directory names are the IDs.
   - Recommendation: **R1 with the residual argued explicitly in the addendum**, with R2 as root's alternative.
5. The originals must survive for the frozen pins (C3) and must leave the repo for C4. The workflow's prev_snapshot instruction points inside the repo (O11). Copying token-bearing originals there would recreate B1, so their prior bytes go to a sealed location instead, with a pointer in prev_snapshot.
   - Inside the worker's ownership, the only off-repo place is B300 `/scratch/iitp4/`, which is ephemeral but sits next to the data the files describe.
   - A durable copy needs a root-granted, lab-only directory outside every git repo. `~/.agents` is a git repo, so it cannot be used.
   - The commit-anchored hashes (O9) let any later verifier confirm the sealed bytes.
6. After relabeling, an in-repo `sha256sum -c` of the old pin files fails on exactly 18 files (2 in card_sha256.txt, 16 in output_sha256.txt), and `preprocess.log` is unpinned (O9). Unless this is stated beforehand with a sealed-root check, a fresh verifier could misread it as a C3 break.
7. The frozen test needs the manifest's `pseudonym` key (O8), and the frozen verdict script needs `test_pseudonyms`, `test_num` and `test_den`. The relabeled format must keep these keys.
8. r2 is the last iteration (O11). M2's gates failed twice on "verdict-path guards missing"; M3 r1 has a surviving kill-rule mutant (stats_stop_uses_mean) and an untested verdict script (O16). A fresh challenger could return REFUTED on these alone. Additive tests that kill the O16 list are cheap (CPU) and lower the gate risk.
9. Tests must pass on frozen code, because C2 requires the suite to pass. The `fm is not False` defect therefore cannot get a failing test; it goes into the addendum. A sibling test (F− present and failing turns a would-be keep into inconclusive) plus an end-to-end test of the verdict script still kill m29/m30.
10. The stale "pending PI" statements (O14) are factually wrong, and the truth strengthens G5: δ was fixed by the PI before freeze. The correction belongs in an addendum, because the card and report are frozen or pinned.
11. The explorer salt (O12–O13) is a separate C4 hazard outside the worker's repo ownership. Sealing only the 128-bit salt defeats brute force, so the 5 hashes can stay. The B300 copy is inside `/scratch/iitp4/` (worker ownership).

## 3. Caveats

- **My own C4 incident.** While checking JSON formatting, I ran a `head -c` peek that cut through hex strings. That printed a 6-hex-character partial prefix of one pseudonym and a 4-hex partial prefix of one content hash in my local tool output; my ≥12-hex mask did not catch them. I wrote neither to any file, but the agent transcript on disk contains them. Root should record this next to worker_M3_r1's self-disclosed print. Rule for everyone: mask hex runs of ≥4 characters when peeking into token-bearing files, or print structure only.
- I did not run R2. Its costs are reasoned from O3, O8 and `scripts/topic2_verdict.py`.
- I did not test mutants. The O16 list comes from the r1 harness outputs; I did not re-execute them.
- I did not inspect HCP data on B300 (no data read). My B300 actions were `find`, `du`, `sinfo` and `ls`.
- I did not inspect chavis-autocommit's own allowlist (O6). The worker should simply finish the sanitization early.
- The residual order and `test_den` channels are documented, not closed. Whether they are acceptable is a judgement; I base it on the C4 letter, the M1 precedent and reviewer_1's explicit fix list. A strict fresh reviewer could still argue otherwise. Root can remove that risk with a written ruling (§4, R-a).
- The I2-compactness dispersion figures (S 1.56–1.67 vs C 1.47 cells) are reviewer_M3_r1_2's numbers. The worker should recompute them from `partitions/partitions_hcp.json` before quoting them.
- I worked independently and did not read explorer_M3_r2_2's outputs or transcript.

## 4. Conclusion — fix strategy for worker_M3_r2

**Hard rules for the whole iteration.**
- 0 GPU-h: no B300 GPU job and no retraining. If anything ever needs a B300 GPU, it goes through Slurm only (RESUME addendum 3).
- No edits to: the card, the report, addenda 01–04, `src/topic2_rgpool/**`, frozen `scripts/topic2_*.py`, frozen tests, `vendor_swift_ver11/SOURCE.md`.
- Every command runs with `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 CUDA_VISIBLE_DEVICES="" nice`, `python -B`, at most 4 processes, `timeout`.
- Never write a real token into any file other than the sealed copies. That includes `.md` files, which are auto-committed every 15 min. Never peek at raw bytes of token-bearing files without masking hex runs of ≥4 characters.
- First, read `orchestrator/` (RESUME, PI_DECISIONS, GATE_STATUS) for a root ruling on R1/R2 and on a durable sealed location. If none exists, use R1 with the B300 sealed copy.

**Step 1 — Seal the originals.**
- Record the sha256 of the 19 token-bearing files. Check the 18 pinned ones against card_sha256.txt and output_sha256.txt; record preprocess.log new.
- Copy the 19 byte-identically (verify by sha256) to B300 `/scratch/iitp4/worker_M3_r2/sealed_c4/<repo-relative path>` (chmod 700), and also to root's durable location if one has been provided.
- Write a pointer file in `verification/worker_M3_r2/prev_snapshot/` (paths, sha256, sealed locations), never the files themselves. State the C4 reason for this departure from the snapshot instruction.
- Remove the B300 salt copy `/scratch/iitp4/worker_M3_r1/code/scripts/dev_subject_salt.txt` only after a sealed copy of it exists, with its sha256 recorded.

**Step 2 — Relabel deterministically.** Write a new `scripts/topic2_c4_sanitize.py` that reads the sealed originals and writes the repo copies. Its rules:
- Token map `tok[p] = "h%02d" % i` over the manifest `subjects` order. Assert the order is sorted, so lexicographic token order equals the old order.
- `hcp_manifest.json`: each subject becomes `{"pseudonym": tok, "qc", "T"}`. Keep the `pseudonym` key (the frozen test needs it). Drop `content_sha256`, `file_bytes`, `n_brain_vox` and `sec`. Keep the top-level counts and `elapsed_sec`. Add a `c4_sanitized` block (original sha256, rule, dropped fields, "originals sealed off-repo"). Write with `json.dump(indent=1)`.
- `split.json`, `stage0_hcp.json` and the 15 `runs/hcp_*/run.json`: replace each quoted token `"<16hex>"` with `"h##"` and change no other byte. Leave `split.manifest_sha256` and `run.split_file_sha256` as they are; they refer to the sealed originals, and the addendum says so.
- `logs/preprocess.log`: replace the tokens and drop the per-line `"sec"`.
- Leave every other file byte-identical, in particular `verdict.json`, posthoc, partitions/perms, fixture runs, other logs, `id_scan_b300.json`, all docs and both old pin files.
- Re-run the frozen `scripts/topic2_verdict.py` on the relabeled runs into a scratch path and assert the output is byte-identical to `verdict.json` (my probe shows it is).

**Step 3 — New pins and a seal checker** (new dated files only).
- `results/topic2/2026-11-01/c4_sealed_originals_sha256.txt`: the 19 originals; these must equal the old pins for 18.
- `results/topic2/2026-11-01/output_sha256_r2.txt`: everything current, including the relabeled 19, new scripts/tests and addendum_05.
- A new `scripts/topic2_c4_seal_check.py --sealed DIR` that verifies:
  1. in the repo, the old pins fail on exactly the expected 18 paths and pass on all others;
  2. on the sealed root, the old pins pass, and preprocess.log matches the new file;
  3. re-running the sanitizer on the sealed originals reproduces the repo bytes exactly;
  4. the repo matches `output_sha256_r2.txt`.
- Cite the commit-anchored hashes (O9) in the addendum.

**Step 4 — C4 guard test** (new file `tests/topic2_rgpool/test_c4_tokens_r2.py`; synthetic tokens only inside the test). It asserts:
- manifest subject keys ⊆ {pseudonym, qc, T}, with `pseudonym == "h%02d" % i`;
- no key named `content_sha256`, `file_bytes`, `n_brain_vox` or `sec` inside any subject or log record under `results/topic2/2026-11-01`;
- no 16-hex token in results/topic2 or docs/topic2 text. Use a precise detector, because a naive `[0-9a-f]{16}` matches the decimal digits of floats; it produced thousands of false hits in train_log.jsonl, verdict.json and others. The detector flags:
  - (i) any quoted string equal to `^[0-9a-f]{16}$`, which also catches an all-digit token;
  - (ii) any unquoted 16-hex run that contains at least one letter a–f and is not adjacent to `.`, a letter or a digit (regex `(?<![0-9a-zA-Z.])(?=[0-9a-f]{0,15}[a-f])[0-9a-f]{16}(?![0-9a-zA-Z])`).
  
  On the current tree this detector flags exactly the 19 known files, with 0 other hits. 64-hex runs are allowed only as values of keys containing `sha256`, or in `*sha256*.txt` pin files;
- every list under `train/val/test/test_pseudonyms/test_pseudonyms_order` matches `^h\d{2}$`, is a subset of the manifest tokens, and every run's test list equals `split.test`.

Show that the test fails when, in a temporary copy, (a) a synthetic 16-hex token is reinserted, (b) `file_bytes` or `n_brain_vox` is re-added, or (c) one run's test list is altered. Scope numeric checks by key, not by bare numbers, because of the Topic 4 coincidences (O4).

**Step 5 — Verdict-path guard tests** (additive; no src change; each must pass on frozen code and fail on its mutant).
- Kill every O16 survivor. Order of priority:
  1. the governing path: `stats.verdict` upper bound vs mean, the `<` boundary, `relative_gain` sign and denominator, `gate_fixture` seed averaging, bootstrap seed resampling, and an end-to-end test that `scripts/topic2_verdict.py` on the shipped run records reproduces `verdict.json` (kills m29);
  2. F− present and failing turns a would-be keep into `inconclusive` (kills m30 / script_verdict_ignores_fminus);
  3. a hand-computed `metrics.masked_sq_terms` check on mask and brain weighting, plus the Stage-0 PCA basis fitted on train only;
  4. the train.py loss mask, data, mask and eval-mask-seed pairing across arms, and test ≠ val masks/subjects (tiny CPU configs);
  5. split: disjointness, test taken first in salted order;
  6. partition: a cross-octant swap of two **signal** cells is rejected (fixes m15's wrong-reason pass), the dense-core seed rule, mean linkage, signal threshold, and a Hungarian placement/slot-order oracle.
- Rerun the three r1 harnesses as adapted copies in `verification/worker_M3_r2/` (never the originals' write paths), with `CUDA_VISIBLE_DEVICES=""`. Report a mutant table where every target is KILLED. A timeout or OOM counts as INVALID, not as a kill.
- Write no test for "missing F− counts as a pass"; it would fail on frozen code. Put that defect in the addendum.

**Step 6 — Addendum** `docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_05.md` (dated; pinned in `output_sha256_r2.txt`; never write the HCP staging directory name followed by a slash and a name, six digits followed by `/MNINonLinear`, or a BIDS subject label (the word "sub", a hyphen, then a letter or digit). The frozen ID_PATHS regexes in `test_outputs_no_ids.py:17-18` scan docs for all three). Contents:
- **(a)** The r1 gate outcome and B1.
- **(b)** The remediation: rule, files, sealed locations, hashes, checker. State that this departs from card §4 line 81 and that no governed computation changed (the verdict script output is byte-identical).
- **(c)** The residual channels (hash-and-sort by a data holder, `test_den`, Stage-0 per-subject values). Why they are accepted: the C4 letter, the M1 precedent at `scripts/topic1_run_cohort.py:10`, and the fact that only data holders, who already hold the IDs, can exploit them. Name R2 as the stricter alternative.
- **(d)** Corrections:
  - PI items 2 and 3 predate freeze (a06f435 03:01:27Z vs 03:14:34Z), so "pending PI" and "set by the worker" in card §4/§8 and report §0/§6 are superseded, and δ = 1 % was PI-fixed before any result;
  - SOURCE.md cites `test_vendor_provenance.py`; the real check is `test_leakage_and_provenance.py::test_vendored_ver11_is_byte_identical_to_recorded_source`;
  - addendum_04's loss range: the logged 100-step means are 1.0561 at step 100, then 0.9978–1.0036;
  - the I2 compactness qualifier, with dispersion recomputed;
  - the per-seed I1 escape-timing driver (descriptive, post hoc);
  - report §3.4 is non-governing;
  - the rank-288 decoder bottleneck as a consideration for the costed follow-ups;
  - the latent `fm is not False`;
  - the r1 CPU smoke ran on the local GB10 when CUDA was visible;
  - the r1 handoff timestamps (N3).
- **(e)** C4 incidents for root's record (worker_M3_r1's hand-typed example ID print; this explorer's partial-prefix print).
- **(f)** The r1 waves were launched directly, before the Slurm rule existed.

**Step 7 — Final checks** (record outputs in `verification/worker_M3_r2/final_*.txt`):
- C1 PROTECTED_HASHES rc 0;
- the old 86, `tests/topic2_rgpool` (55 + new) and `tests/topic1_lagmotif` (88) suites, all with `CUDA_VISIBLE_DEVICES=""`;
- `code_sha256_at_freeze.txt` rc 0 (the frozen 33 unchanged);
- the seal checker, all four parts;
- `output_sha256_r2.txt` rc 0;
- a count-only token scan of the whole repo working tree, with tokens loaded from the sealed manifest in memory. Expected: 0 hits, except the explorer_M3_r1_1 files until root acts (R-c);
- the git history scan still at 0;
- `audit_layout.py` PASS;
- ledger unchanged (0 GPU-h).

**Root decisions and actions** (outside worker ownership; ideally before the worker starts, recorded in `orchestrator/`, e.g. RESUME addendum 4, which every r2 agent reads):
- **R-a** Rule R1 (recommended) or R2. R2 means: repo copies keep only aggregates (run.json sums plus test_nmse, Stage-0 means/contrasts, `verdict.json` without `per_subject_nmse_seedmean`, split counts). Per-subject arrays and the r1 verifier outputs that carry them (e.g. `verification/challenger_M3_r1_2/b300_outputs/`) are sealed, `verdict.json` gets a sealed original plus a new pin, and the frozen verdict script then runs only on the sealed copies.
- **R-b** Provide a durable lab-only directory outside every git repo (not `~/.agents`, which is a repo), e.g. `/home/juke/sealed/00IITP-AI/topic2_2026-11-01/` chmod 700. Grant the worker ownership of it, or copy the B300 `sealed_c4` there yourself with sha256 verification, before the B300 VM stops.
- **R-c** Move `verification/explorer_M3_r1_1/dev_subject_salt.txt` to that sealed location and record its sha256. The 5 salted hashes may stay (128-bit salt, O13).
- **R-d** Tell the r2 verifiers, in that orchestrator note: the expected 18 in-repo pin failures, the seal-check command, the R1/R2 ruling, that no GPU is needed, and that GPU use is Slurm-only.
- **R-e** Record the C4 print incidents (Caveats).
- **R-f** Decide on B300 `/scratch/iitp4` cleanup: worker_M3_r1 is 142 G; keep the 15 checkpoints if follow-up option E is wanted.

GPU: about 12.0 of 64 GPU-h used so far in the ledger. r2 needs 0.

## 5. Verification Method

All commands run from `/home/juke/git/00IITP-AI`, with `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 CUDA_VISIBLE_DEVICES="" nice`.

- Structure: `python -B -I verification/explorer_M3_r2_1/probe_structure.py results/topic2/2026-11-01/{hcp_manifest.json,split.json,stage0_hcp.json,runs/hcp_C_s0/run.json,verdict.json}`.
- Exposure: `python -B -I verification/explorer_M3_r2_1/probe_token_scan.py /home/juke/git/00IITP-AI`. Expected now: the 19 results files plus 4 explorer_M3_r1_1 files (and 3 Topic 4 numeric coincidences). Expected after the r2 fix plus R-c: Topic 4 coincidences only. After relabeling, this probe needs the sealed manifest: point it at a sealed copy.
- R1 feasibility: `python -B verification/explorer_M3_r2_1/probe_sanitize_r1.py /home/juke/git/00IITP-AI <scratch dir outside repo>` → `verdict_bytes_identical: true`, `frozen_c4_tests_pass_on_sanitized: true`, `frozen_test_passes_without_pseudonym_key: FAIL KeyError`, residual `{}`. Delete the scratch dir afterwards.
- Git history: `git grep -c -F -f <(tokens…) $(git rev-list --all --since=2026-10-30) --` → rc 1. Positive control on the split salt.
- `MAX_ITER`: `grep -n MAX_ITER ~/.claude/projects/-home-juke/d5bff6c5-d355-47e4-94ae-f598f75c884a/workflows/scripts/teamwork-four-topics-b-wf_5bb8fefb-ae0.js`.
- M1 precedent: `sed -n 8,14p scripts/topic1_run_cohort.py`.
- PI timing: `git log --format='%h %cI' -- .agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md | tail -1` and the same command for the card.

**This report is invalidated if:**
- any of the 19 files changes before sealing (check against the old pins);
- a commit containing tokens appears (rerun the history scan);
- root rules R2;
- the frozen verdict script, the test, or the `stats.py` hash changes;
- the workflow's MAX_ITER for M3 differs from 2.
