# handoff — reviewer_M3_r2_2 (M3 / Topic 2, gate round r2, reviewer 2 of 2) — HARD, 2026-11-01T10:40Z

**Verdict: APPROVE.** There is no blocking issue.
- B1, the r1 C4 blocker, is closed. The fix matches the remedy that reviewer_M3_r1_1 set out.
- I re-ran the checks myself. C1–C8 and T2.1–T2.3 hold.
- No governed number moved. The card verdict is still **stop (killed)**, and verdict.json reproduces byte for byte.
- I found no integrity violation.
- Five items need root action. They are non-blocking for this deliverable, but N1 and N2 are time-critical (§4).

All probes and outputs are under `/home/juke/git/00IITP-AI/verification/reviewer_M3_r2_2/`. I changed no production file.

## 1. Observation

### Re-run checks (my own runs)

| check | result | evidence |
|---|---|---|
| C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` | rc 0, 67/67 OK, incl. `src/rg_box_pooling.py` | `c1_protected_hash_check.txt` (09:30Z), re-run at close, see §5 |
| code freeze `code_sha256_at_freeze.txt` | rc 0, 33/33 | `pin_checks.txt` |
| `output_sha256_r2.txt` | rc 0, 156/156 | `pin_checks.txt` |
| `c4_sanitized_sha256.txt` | rc 0, 19/19 | `pin_checks.txt` |
| old `card_sha256.txt` | fails exactly `hcp_manifest.json`, `split.json`; the other 6 OK | `pin_checks.txt` |
| old `output_sha256.txt` | fails exactly `stage0_hcp.json` + the 15 `runs/hcp_*/run.json`; the other 27 OK | `pin_checks.txt` |
| `scripts/topic2_c4_seal_check.py repo` | all_ok; R1 19/19, R2 33 pass + 18 expected, R3, R4 (88 tokens, fields T/pseudonym/qc), R5 156 | `seal_check_repo.json` |
| `tests/topic2_rgpool`, connectome Slurm job 217939, node4, CPU only (torch 2.15.0+cpu, numpy 2.5.4, scipy 1.18.1, pytest 8.4.2) | **92 passed, 0 skipped**, rc 0, 86 s; code sha of the 39 shipped files = local repo | `connectome_suite_topic2_rgpool.log`, `connectome_code.sha`, `connectome_storage_code.sha`, `connectome_venv_lock.txt`, `connectome_slurm_records.txt` |
| old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`), local | 86 passed, rc 0 | `tests_old86.txt` |
| `tests/topic1_lagmotif`, local | 88 passed, rc 0 | `tests_topic1_lagmotif.txt` |
| frozen `scripts/topic2_verdict.py` on the sanitized runs, local superclaude-env | verdict.json **byte-identical** (sha 59af05e5…caf68); stdout byte-identical to `logs/verdict_stdout.txt` | `verdict_repro/` |
| whole-run `audit_layout.py` | rc 0, 264 files, 0 findings (09:55Z), re-run at close | `audit_layout_whole_run.txt` |

- **Local suite.** My local `tests/topic2_rgpool` run was SIGTERMed by earlyoom after 64 s (journal: host memory at 10 %, swap 100 %). earlyoom killed an `ollama` process first. I did not run heavy tests locally after that, so as not to hurt other workloads. The full suite went to connectome (C5).
- **Verdict.** stop, because the upper bound of I1 is below δ = 1 %. Values: I1 mean +0.1468 %, t95 [−0.0677 %, +0.3614 %], df 4; I2 t95 [+0.00098 %, +0.9455 %]. F+ gate passes (+3.061 % vs E, +2.935 % vs S). F− gate passes (−1.737 %).

### Independent check of the remediation against the sealed originals
I ran `b300_seal_probe.py` on B300 .98 with the system python3, CPU only, standard library. It ran in seconds in my own dir `/scratch/iitp4/reviewer_M3_r2_2` (now removed). Output: `b300_seal_probe.out.txt`. It reads `/scratch/iitp4/worker_M3_r2/sealed_c4` read-only.
- **P1.** The 19 sealed files equal `c4_sealed_originals_sha256.txt`, 19/19.
- **P2.** The 18 old r1 pin lines pass on the sealed root, 18/18.
- **P4: my own token map** (position in the original manifest list), independent of the worker's sanitizer:
  - The original subjects are sorted by content sha256, and pseudonym = hash prefix.
  - The sanitized manifest is exactly {pseudonym: hNN, qc, T}. The other 8 top-level keys are equal, and only `c4_sanitized` is added.
  - `split.json`, `stage0_hcp.json` and the 15 hcp `run.json`, after my token swap, equal the repo copies as JSON, 17/17.
  - Every leaf path is the same, and every numeric leaf is identical in value and position. So no per-subject array was reordered and no number changed.
  - `preprocess.log` changed only in its 88 subject lines.
- **P5.** No original pseudonym or content hash appears in any sanitized file. The only hex runs with letters are 64-hex file and code hashes.
- **P6.** Re-running the repo sanitizer on the sealed originals reproduces the repo bytes, 19/19.
- **P7: provenance of the seal.** All 19 sealed files are byte-equal to the original working copies that worker_M3_r1 left in `/scratch/iitp4/worker_M3_r1/`.
- **P8.** Seal permissions are 700 on directories and 400 on files: 21 files, i.e. the 19 originals plus 2 old pin files.
- **Git anchor.** The manifest and split hashes in `c4_sealed_originals_sha256.txt` equal the values quoted in the card text committed in 51609c1 (26ba34a9…, c13b5f21…). `git show 51609c1:<card> | sha256sum` gives c9bfc60a…41f5, the same as the current card.
- **The other outputs are untouched.** I compared 92 file hashes with the B300 originals: the 27 `train_log.jsonl` / `stdout.log` files, `logs/build_partitions_hcp.log`, `logs/stage0.log`, `partitions_hcp.json`, `perms_hcp.npz` and the 12 fixture `run.json`. All equal. Only the 15 hcp `run.json` differ, as expected; 7 files are not on B300 and are covered by the old pins instead. So r2 changed exactly the 19 files.

### C4 leak scans (count-only)
- **Method.** Tokens and IDs were streamed by ssh pipe from the sealed manifest and the HCP directory listing into local memory. They were never written or printed. Outputs: `local_token_scan.out.json`, `local_history_numeric_scan.out.json`, `local_history_numeric_scan_control.txt`.
- **Working tree.** 15,592 text files (whole repo except `.git`/binaries):
  - 0 files hold any of the 176 hex tokens (88 pseudonyms + 88 content hashes);
  - 0 hold any of the 88 file sizes;
  - 0 hold any of the 87 voxel counts.
  - The 1084 HCP IDs: 3 hits, all `results/topic1/2026-10-31/extract_primary.jsonl` and two verifier copies of it. In each case the match is the integer part of a float (`"###C": ######.###`), i.e. a coincidence in Topic 1 data, not an identifier and not M3.
- **Git history** (`rev-list --all --since=2026-10-30`):
  - hex tokens: 56 revisions, 0 file hits; positive control 43;
  - IDs, sizes and voxel counts: 59 revisions, 0 candidate blobs. The positive control (a known tracked value hidden among 1258 decoys, the same code path) hits 7 files in the latest revision, including the card.

### Other verified claims
- **Pre-freeze PI decisions.** PI decisions 2–3 were first committed in a06f435 at 03:01:27Z, and the card in 51609c1 at 03:16:27Z (addendum_05 erratum 1 is correct).
- **Errata numbers recomputed:**
  - per-seed I1 +0.235 / +0.069 / +0.403 / −0.035 / +0.062 %;
  - dispersion E 0.784, G 1.112, C 1.469, S 1.557–1.674, R 2.457;
  - the ver11 'mlp' decoder branch (lines 1118–1149) has `decoder_spatial_expand` Linear(in → 48³);
  - merges only for `i_layer < num_layers − 1` (line 1068).
- **Vendored files.** ver11 and `patchembedding.py` are byte-identical to `git show f0dc7aca:…` (de132387…, c889eebb…). The SwiFT_v2 working file is clean (C7).
- **Frozen documents unchanged:** card, architecture note, result report and addenda 01–04 (hashes equal the r1 pins). addendum_05 on disk is aa07dd54…c6e5, as pinned. The HEAD-committed copy is an earlier daemon snapshot.
- **GPU ledger.**
  - 36 lines. Its first 35 lines hash to auditor_M3_r1_1's 06:15Z snapshot (0e1b3f7f…), so the file was only appended to.
  - 0 worker_M3_r2 rows, consistent with 0 GPU-h.
  - Completed total 11.99 GPU-h, under the 64 cap.
- **Git and installs.** The git reflog shows only the 15-minute host checkpoint commits. No new files in superclaude-env site-packages since 2026-11-01.
- **Tests are genuine.** I read all three new files. They assert on behaviour against hand-built or oracle values. The shipped-verdict test recomputes verdict.json from the run records rather than embedding numbers. None skips under CUDA-hidden runs.

### Independent mutation spot-check
I designed these 12 mutants myself, separate from the worker and r1 lists (`rv_mutants.py`). They ran as Slurm job 217940, CPU only (`rv_mutants.out.json`).
- The baseline passed: 92.
- **12/12 KILLED**, 0 survived, 0 invalid.

| mutant | killed by |
|---|---|
| keep rule uses the I2 upper bound | `test_stats::test_verdict_mapping` |
| t interval uses ddof 0 | `test_stats::test_t_interval_matches_hand_computation` |
| normal quantile instead of t | `test_stats::test_t_interval_matches_hand_computation` |
| verdict script drops seed 4 | `test_verdict_script_reproduces_the_shipped_verdict` |
| bootstrap draws subjects separately per arm | `test_stats::test_hierarchical_bootstrap_null_and_planted` |
| salt placed after the pseudonym in the split hash | `test_assign_split_takes_test_then_val_from_the_front_of_the_salted_order` |
| S surrogate ignores distance bins | `test_partition::test_s_surrogate_keeps_distance_bins_and_varies_with_seed` |
| merge gathers by the inverse permutation | `test_merge::test_box_content_and_canonical_slots` |
| F− downgrades modify instead of keep | `test_stats::test_verdict_mapping` |
| SimMIM mask one unit short | `test_data::test_simmim_masks_exact_ratio_and_two_frame_units` |
| last window dropped | `test_data::test_windows` |
| I2 computed against the wrong reference | `test_verdict_script_wires_I1_I2_and_both_fixture_gates` |

## 2. Logic Chain

1. **B1 is closed.** The r1 remedy had four parts:
   - no unsalted content-hash token, full content hash or file size in any repo file;
   - frozen-input hashes still verifiable against retained originals;
   - a dated addendum;
   - a new output-hash file and a guard test.

   How each is met:
   - The scans show 0 tokens, 0 content hashes, 0 sizes and 0 voxel counts in the working tree and in git history.
   - The seal passes the old pins (P1, P2). The sealed bytes are the r1 governed originals (P7), anchored to the committed card.
   - addendum_05 is written.
   - `output_sha256_r2.txt` and `test_c4_tokens_r2.py` exist.
2. **No governed computation changed.**
   - My independent token swap shows that the sanitized JSON equals the originals up to token values, with every numeric leaf in place (P4c, P4d).
   - The frozen verdict script reproduces verdict.json byte for byte.
   - The code freeze passes 33/33.
   - Every other output equals its B300 original.
   - So the r1 gate's scientific findings (T2.1–T2.3, stop) carry over unchanged. Four r1 verifiers reproduced them, including a bit-exact checkpoint re-evaluation.
3. **C4 letter.** Positional indices are named explicitly in C4. The residual linkage by someone who holds the 88 staged files (hash and sort; match `test_den`) is disclosed in addendum_05 §3. It is the same property as M1's accepted positional scheme. Choosing a stricter scheme is a root/PI policy decision, not a defect.
4. **C2 holds.** 86 + 88 locally, and 92/92 for the milestone suite in an environment that matches the B300 one that ran the governed jobs. Verdict byte-identity was checked in the original local environment. The new guards are substantive: 12/12 of my own mutants were killed, by tests across the old and new files.
5. **C3, C5–C8.**
   - The card is untouched. The deviation is recorded in a dated addendum, never by editing the card.
   - r2 used 0 GPU-h. The ledger is append-only and under the cap.
   - HCP-YA OA is PI-approved; there is no ENIGMA path.
   - SwiFT_v2 is read-only, and the vendored files are byte-identical.
   - addendum_05 cites only this run's outputs (0 mentions of EMPIRICAL_ANALYSIS_REPORT).
   - The worker's C5 CPU placement on B300 is a disclosed, irreversible deviation that used no GPU (N3). My connectome Slurm re-run now gives a C5-placed reproduction of the suite.
6. **Severity rule.** A blocking issue is a remediable defect in the reviewed deliverable that fails a criterion's letter. None of the items in §4 meets that rule.

## 3. Caveats

- **Worker mutation tables not re-run.** I did not re-run the worker's 102-mutant v2/v3 tables. My 12 independent mutants replace that check. A survivor would only be a coverage gap, because the code is hash-frozen and the outputs reproduce.
- **No GPU re-evaluation.** I did no checkpoint re-evaluation (0 GPU-h). B300 .98 had all 8 GPUs busy with other teams at 09:32Z. r1 verifiers had already re-evaluated checkpoints bit-exactly, and r2 changed no checkpoint or run.
- **Full suite never green on DGX-Spark.** The full topic2 suite has not passed in the local superclaude-env, because of earlyoom. It passed on connectome (torch 2.15.0+cpu) and, per the worker, on B300.
- **Print incidents not verifiable.** The C4 print incidents (worker_M3_r1, explorer_M3_r2_1, worker_M3_r2) are tool-output events. Only their absence from files can be verified, and I verified that.
- **My own B300 CPU use.** It was two short stdlib probe runs on .98, outside Slurm, CPU only, seconds each, plus read-only `ls`/`sinfo`/`nvidia-smi`. They were needed because the sealed originals exist only there. Disclosed for C5. No GPU, no ledger row needed.
- **Probe edited in place.** `local_history_numeric_scan.py` v1 was edited in place after it hung in `pipe_write` (the per-user pipe quota shrank the pipe buffer below the pattern size). It produced no output, and the fix is commented in the file. The thread count was limited and binaries are skipped (`-I`). Only the v2 output is used.
- **DISPATCH.md.** The first section of my DISPATCH.md summarised the worker JSON. I appended a byte-exact section extracted from my transcript, with sha256 values, and kept the first section.
- **ENIGMA.** I never listed or read `~/enigma_ocd` on B300.
- **Not examined.** The perlmutter SwiFT fork and HCP family structure (an r1 limitation).

## 4. Conclusion

**APPROVE.** No blocking issue. Non-blocking items, most important first:

| # | item | owner | action |
|---|---|---|---|
| N1 | **Explorer salt in the repo working tree.** `verification/explorer_M3_r1_1/dev_subject_salt.txt` sits next to salted hashes of 5 HCP dev-subject IDs. The ID space is 6-digit, so anyone with repo access can brute-force them. It is untracked and was never committed (`git log --all` and `git ls-files` are empty), but it is not ignored, so a checkpoint job could pick it up. It is outside worker ownership. | root | **Required before M3 closes**: move the salt off-repo, or delete the salted hashes; then re-scan |
| N2 | **The sealed originals exist only on ephemeral B300 /scratch.** They are in `/scratch/iitp4/worker_M3_r2/sealed_c4` and also in `/scratch/iitp4/worker_M3_r1/`, both wiped on VM stop. If they are lost, the 18 old pin lines can no longer be byte-verified; their hashes stay anchored in the committed card and metadata. | root | **Time-critical**: durable copy outside every git repo |
| N3 | **C5 CPU-placement deviation.** worker_M3_r2 ran mutation v2/v3, the 92-test suite and scans on B300 .98 CPU outside Slurm, with up to 6 processes for about 16 min or more. Its progress log puts the start of the B300 CPU work (08:14Z) before its own connectome attempt (~08:5xZ). connectome Slurm was reachable at 09:33Z. Disclosed in addendum_05 §7; no GPU used. | root | Record it. Future CPU verification goes to connectome Slurm (shared `/storage`, since home is node-local) |
| N4 | **Residual linkage of positional tokens** for anyone holding the staged HCP files (addendum_05 §3). | root/PI | Rule on positional vs secret reorder vs aggregate-only |
| N5 | **Guard weaker than its docstring.** `test_c4_tokens_r2.py` says "no stray 64-hex hash" in docs, but the docs `.md` files are only checked for 16-hex shapes. In results JSON, any 64-hex value under a key containing "sha256" passes. So a re-inserted full content hash in a doc, or under a `*_sha256` key, would not be caught. The current state is clean (my scans). | worker/next iteration | Optional: add a 64-hex allow-list against the pin files |
| N6 | The sanitizer and the seal checker have no synthetic unit test in the suite. They are verified only by the B300 sealed-mode run and my P4/P6. | worker | Optional fixture test |
| N7 | **Hash-suffix typo in the worker's prose handoff.** The `c4_sealed_originals` and `c4_sanitized` suffixes are swapped ("18d661bf…7570", "7a4cceab…b87ca"). The frozen_artifacts list is correct: 18d661bf…6b87ca and 7a4cceab…2d7570. | worker | Cosmetic |
| N8 | **Latent default.** `fm is not False` at `scripts/topic2_verdict.py:66` (a missing F− gate counts as a pass). No effect in this run. | — | Documented in addendum_05 |
| N9 | **Root actions from the worker:** record the print incidents; clean up `/scratch/iitp4/worker_M3_r1` (142 G) once the checkpoints and seal decisions are made. | root | — |

**Scientific reading.** Unchanged from r1: stop at E36 / 140k samples; I2 > 0 is confounded with compactness; there is a low reconstruction ceiling. The verdict follows card §8 exactly. The T2.3 escape clause correctly was not invoked.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt          # 67 OK
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                           # 33 OK
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c                 # 156 OK
python3 scripts/topic2_c4_seal_check.py repo                                                          # all_ok
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -B scripts/topic2_verdict.py results/topic2/2026-11-01/runs /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-01/verdict.json
# full suite without local memory: copy src/topic2_rgpool tests/__init__.py tests/topic2_rgpool scripts/topic2_*.py scripts/b300_env
#   results/topic2/2026-11-01 docs/03_empirical_analysis/topic2 to connectome /storage, build the venv with
#   verification/reviewer_M3_r2_2/connectome_build_env_storage.sh, sbatch connectome_run_suite.sh  -> 92 passed
# sealed side (B300 .98, stdlib): python3 -I -B verification/reviewer_M3_r2_2/b300_seal_probe.py BUNDLE /scratch/iitp4/worker_M3_r2/sealed_c4 /scratch/iitp4/worker_M3_r1 OUT
python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py .agents/teamwork/tw-20261031-four-topics
```

- **Remote state.**
  - connectome `/storage/connectome/00IITP-AI_verification/reviewer_M3_r2_2/` keeps the venv, pythons, scripts and logs. The repo and mutation copies were removed.
  - The node-local `~/iitp4_reviewer_M3_r2_2` was removed.
  - `/scratch/iitp4/reviewer_M3_r2_2` on B300 was removed.
  - No job or process of mine remains. Job 217936 is the other reviewer's and was not touched.
- **This review is invalid if any of the following holds:**
  - any of the hashes above changes;
  - `sealed_c4` changes or disappears before a durable copy exists;
  - a token, size, voxel count or ID scan over new commits finds a hit in an M3 file;
  - the PI rules the positional scheme insufficient under C4.
