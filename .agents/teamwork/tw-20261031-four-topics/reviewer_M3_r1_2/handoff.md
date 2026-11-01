# handoff — reviewer_M3_r1_2 (M3 / Topic 2, round r1) — HARD, 2026-11-01T06:10Z

**Verdict: APPROVE** (no blocking issue). Every ACCEPTANCE criterion C1–C8 and T2.1–T2.3 is met with evidence I produced myself. 11 non-blocking findings for root are in §4.

## 1. Observation

All probe outputs are in `/home/juke/git/00IITP-AI/verification/reviewer_M3_r1_2/`.

**C1 protected hashes.**
- `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` → rc 0, 67/67 OK (`c1_protected_hash_check.txt`, 05:41Z).

**C2 tests** (05:41–05:43Z, nice, OMP 2):

| suite | result | output |
|---|---|---|
| `tests/topic2_rgpool` | 55 passed, rc 0 | `tests_topic2.txt` |
| old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`) | 86 passed, rc 0 | `tests_old86.txt` |
| `tests/topic1_lagmotif` | 88 passed, rc 0 | `tests_topic1.txt` |

**Pins, checked with LC_ALL=C.**
- `code_sha256_at_freeze.txt`: 33/33 OK, rc 0.
- `card_sha256.txt`: 8/8 OK, rc 0. The card hash is c9bfc60a…41f5.
- `output_sha256.txt`: 43/43 OK, rc 0.
- Outputs: `code_freeze_check_C.txt`, `card_check_C.txt`, `output_pin_check_C.txt`.
- Git history: the daemon commit 51609c1 (03:16:27Z) holds the card with the same sha c9bfc60a. It is the card's only commit, so the card has not changed since it was frozen.

**Timeline (C3).**
- From B300 file mtimes (UTC):
  - preprocess and cellmeans 02:27–02:29Z (disclosed in card §0);
  - split.json 02:56Z;
  - **card freeze 03:14:34Z**;
  - fc_train_group.npy and perms_hcp.npz 03:17Z;
  - stage0 03:24Z.
- From `run.json` and launched.json:
  - first run starts 03:16:17Z;
  - last F+ run ends 03:42:08Z;
  - first HCP run starts 03:44:51Z.
- So every real-data statistic comes after the freeze, and Stage 1 started only after the F+ gate.

**Independent verdict recompute** (`recompute_verdict.py`, which does not import the worker's stats.py; output `recompute_verdict.out.json`). It covers 27 run dirs and found 0 problems. For every run:
- status is completed;
- the code hashes of all 13 modules equal the freeze list;
- `perm_sha256` and `perm_file_sha256` equal the shipped npz;
- hyperparameters match card §5;
- n_params = 38,712,096;
- test_nmse = Σnum/Σden;
- the HCP test list equals split.json `test`.

Two further results:
- `test_den` is bit-identical across all 15 HCP runs, all 6 F+ runs and all 6 F− runs, which shows the data and eval masks were identical.
- The recomputed figures equal verdict.json:
  - gates F+ +3.061 % / +2.935 % (pass) and F− −1.737 % (pass);
  - I1 mean +0.1468 %, t95 [−0.0677 %, +0.3614 %];
  - I2 [+0.00098 %, +0.9455 %];
  - verdict **stop**.

**B300 checkpoint re-evaluation** (GPU 7, idle-checked immediately before launch, 05:58:01–05:58:26Z, 0.01 GPU-h; ledger started and completed rows under flock with agent id reviewer_M3_r1_2). Script `b300_ckpt_reeval.py`, output `b300_ckpt_reeval.out.txt`, comparison `compare_reeval.out.json`.
- I declared the tolerance before running it.
- For hcp_E_s2, hcp_C_s2 and hcp_S_s2, each checkpoint's own `layers.0.downsample.perm` buffer hashes to that run.json's `perm_sha256` (E 0, C 1,512 and S 1,574 cells moved).
- The recomputed test NMSE matches run.json within 1.2e-8 absolute. Per-subject num and den match within 7.5e-8 relative.
- The script used the worker's code copy on B300, which matches the local freeze hashes for all 24 files I hashed, and the worker's venv. Nothing was written on B300.

**B300 partition rebuild** (CPU only; `b300_rebuild_partitions.py`, output `b300_rebuild_partitions.out.txt`).
- The group FC, recomputed from the 64 TRAIN subjects only, has the same float32 sha as the shipped one (e2912ee9…).
- nvox and group_mask are equal to the shipped files.
- C and S_seed0–4 rebuilt with the frozen code are identical to perms_hcp.npz.
- The shipped C placement is a Hungarian optimum in every octant (cost gap 0.0).

**C4.**
- My B300 scan streamed a tar of the files over stdin and held the 1,084 HCP directory names in memory only. It covered 274 text files with 0 hits (`id_scan_b300_reviewer.json`). The scope was:
  - results/topic2, the ledger and docs/topic2;
  - verification/worker_M3_r1, explorer_M3_r1_1, explorer_M3_r1_2 and reviewer_M3_r1_2;
  - the metadata of worker_M3_r1, explorer_M3_r1_1, explorer_M3_r1_2 and reviewer_M3_r1_2;
  - the topic2 src, tests and scripts, and b300_env.
- No git commits other than the root and daemon checkpoints.
- `verification/` is untracked and was never committed.
- `superclaude-env` site-packages has no entries newer than the run start.

**C5.**
- Ledger completed rows: 11.872 GPU-h before my row, plus my 0.01.
- Launch-to-end sums from the run records give 11.678 GPU-h for the waves; the ledger has 11.69 for the waves plus 0.04 for smoke.
- Env: project-local `/scratch/iitp4/worker_M3_r1/venv` (`scripts/b300_env/build_env.sh` and `lock.txt`, torch 2.15.0+cu134).
- No topic2 process remains on B300.
- At 05:45Z GPUs 0–3, and at 05:54Z GPU 2, were in use by other teams. They were not touched.

**C6.** PI_DECISIONS_2026-11-01 item 2 says HCP-YA Open Access counts as public. /scratch/iitp4 holds only explorer_M3_r1_1, explorer_M3_r1_2 and worker_M3_r1, all Topic 2 material. I did not access ~/enigma_ocd.

I grepped for "enigma" (case-insensitive) and for "304" near "ROI" in two places:
- every path I streamed to B300;
- `/scratch/iitp4` on B300, excluding the venv, the uv cache and the hcp directory.

Every hit is prose: instructions, disclaimers, or the quoted old premise. No data file anywhere is ENIGMA-derived. The data files under /scratch/iitp4 are:
- HCP pseudonym directories;
- the train FC;
- permutations;
- 15 checkpoints;
- synthetic fake00–05.

**C7.** SwiFT_v2 HEAD is f0dc7aca. The vendored ver11 (de132387…) and patchembedding (c889eebb…) are byte-identical to the HEAD files. No file in SwiFT_v2 has an mtime after 2026-10-31 16:00 KST.

**C8.** All numbers in the report match verdict.json, stage0_hcp.json and the post hoc JSON. Old EMPIRICAL_ANALYSIS numbers appear only as the quoted, refuted premise in the architecture doc.

**T2.1.** I checked the vendored file at the cited lines:
- 41: PatchMergingV2;
- 72: Linear(8C→2C);
- 73: post-norm LN(2C), which is why it crashes;
- 81: product slot order;
- 85;
- 904 and 1036: callable downsample;
- 1068: no merge after the last stage;
- 1112: hard-coded 'mlp'.

The tests pin the stage table, the decoder octant locality and the token order.

**Layout.** Whole-run `audit_layout.py`: PASS, 207 files, 0 findings, rc 0 (`audit_layout.txt`).

## 2. Logic Chain

1. C1, C2: the hash and test reruns above pass.
2. C3, card before results:
   - The card hash was pinned at 03:14:34Z and committed unchanged at 03:16:27Z.
   - Every outcome-bearing artifact (FC, partitions, Stage 0, all 27 runs) has a later timestamp, and the code that ran equals the freeze list.
   - The fixtures fail on their targeted defects: F+ purity rejects periphery/max, and the test_merge mutants are caught.
   - Raw logs are present (per-run train_log.jsonl and stdout.log).
   - Deviations sit in addenda 01–04 and the card is unedited.
3. Integrity. The reported numbers are tied to real computation in three independent ways:
   - the identical-den invariant across runs;
   - the checkpoint re-evaluation, with each perm buffer tied to its arm and NMSE reproduced within 1e-8;
   - the partition rebuild from TRAIN-only FC.

   I found no hardcoded results, facades or self-certification.
4. T2.2:
   - The comparison is matched: same constructor, bit-identical step-0 weights, an E-arm that is bit-identical to stock ver11, equal parameters, FLOPs, data, masks and budget.
   - The tests cover shape, bijection and octant invariants, slot assignment and gradient flow.
   - F+ is a fixture where grouping should help and F− one where it should not, at both CPU and training-loop level.
5. T2.3: the pilot ran within the cap (11.73 of 64 GPU-h) on PI-approved data, and the card §8 rule mechanically gives stop: the I1 upper bound of 0.36 % is below δ = 1 %.

## 3. Caveats

- I did not run a mutation pass of my own. One gap: no unit test pins the centroid placement of non-E boxes. I covered it by checking the shipped C permutation directly (Hungarian gap 0).
- ~/enigma_ocd was deliberately not inspected. "No other process was touched" rests on the absence of contrary evidence.
- The re-evaluation covered seed 2 only (E, C and S); the other 12 HCP runs rely on the den invariant and the code and perm hashes.
- My DISPATCH.md abbreviates the embedded worker JSON instead of copying it byte for byte, and flags this.
- A parallel verifier, reviewer/auditor M3, re-evaluated the same three checkpoints on GPU 5 at 05:58:02Z (its own ledger row).

## 4. Conclusion

**APPROVE.** None of the findings below is blocking. They are listed most important first, with the owner who should act.

1. **Stale "pending PI" wording** (root).
   - Report §0 and §6, card §8 and the worker handoff say that δ = 1 % and the HCP C6 status await PI confirmation.
   - PI_DECISIONS items 2 and 3 already settled both before the freeze.
   - Record the closure in a dated addendum or coordination note. The card cannot be edited.
2. **I2 is confounded with compactness** (worker or root).
   - The "connectome-specific" label for I2 does not hold cleanly: the S boxes are less compact than C (dispersion 1.56–1.67 vs 1.47 cells).
   - So Stage-1 I2 > 0 cannot be attributed to FC specificity alone.
   - Stage 0 does support FC information beyond distance: C − G r +0.028 in 16/16 subjects, with G more compact (1.11).
   - The report should qualify the I2 wording.
3. **Optimisation dynamics** (report).
   - The per-seed I1 is driven largely by how late E runs leave the trivial predict-0 basin. At step 2188, E_s0 and E_s2 had val NMSE ≈ 1.0003 and gave I1 +0.23 % and +0.40 %; every C run had already left the basin by then.
   - Every arm sits at NMSE ≈ 0.99.
   - The report states that "stop" is scoped to this target and budget. It does not mention the escape-timing driver; adding it would sharpen the reading.
4. **Addendum 04 loss range.**
   - It says the hcp_S_s2 training loss stayed "between 0.9997 and 1.0018 for all 8,750 steps".
   - The logged 100-step means are 1.0561 at step 100 and 0.9978–1.0036 afterwards.
   - The val and test claims are correct.
5. **Wrong test file name** (via addendum).
   - `vendor_swift_ver11/SOURCE.md` cites `tests/topic2_rgpool/test_vendor_provenance.py`, which does not exist.
   - The check is `test_leakage_and_provenance.py::test_vendored_ver11_is_byte_identical_to_recorded_source`.
   - SOURCE.md is in the freeze list, so correct it by addendum.
6. **Explorer salt: REQUIRED ROOT ACTION BEFORE M3 CLOSES** (root).
   - `verification/explorer_M3_r1_1/dev_subject_salt.txt` sits next to `dev_subjects_BURNED.md`, which holds sha256(salt+dir name)[:16] for 5 dev subjects.
   - With the salt in the repo, anyone with repo access can recover those 5 HCP IDs by brute-forcing the 6-digit space, without B300 access. That is strictly more exposure than the positional index in the same file, which can only be reversed with the B300 listing.
   - It is non-blocking for this review for four reasons:
     - C4's letter ("salted hash") is met;
     - the files lie outside worker_M3_r1's ownership, so the worker could not fix them;
     - the worker already escalated the issue;
     - the files are untracked and were never committed.
   - Root must move the salt off the repo or delete the hash list before any autocommit picks up `verification/`. A copy of the salt exists on B300 at `code/scripts/dev_subject_salt.txt`.
7. **Disclosed tool-output incident** (root).
   - The worker self-disclosed one hand-typed public-documentation HCP example ID in local tool output. It was not written to any file.
   - My scan found 0 hits. Root should adjudicate and record the incident.
8. **Linkable content pseudonyms.**
   - The pseudonyms are unsalted sha256 prefixes of public HCP files, so anyone with HCP OA access can link them to HCP IDs.
   - This is acceptable under the letter of C4 and PI decision 2 (no re-identification of individuals), but it should be noted.
9. **Untested placement.**
   - No unit test pins the centroid placement of non-E boxes, so a mutant that drops the Hungarian placement would pass the suite.
   - The shipped artifact was verified directly (gap 0).
10. **Cleanup on B300** (root, PI).
    - About 126 GB of preprocessed HCP, 15 checkpoints and the FC remain in `/scratch/iitp4/worker_M3_r1`.
    - Decide whether to delete them. Keep the checkpoints if option E (downstream probe) is wanted.
11. **Post hoc headline** (report).
    - Report §3.4 re-expresses the result in explained-variance units ("+13.1 % of E's explained variance").
    - It is labelled post hoc and non-governing, but it should not be quoted as a headline.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-01/card_sha256.txt | LC_ALL=C sha256sum -c
grep -v '^#' results/topic2/2026-11-01/output_sha256.txt | LC_ALL=C sha256sum -c
bash verification/reviewer_M3_r1_2/run_tests.sh      # 55 / 86 / 88 passed
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/reviewer_M3_r1_2/recompute_verdict.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/reviewer_M3_r1_2/compare_reeval.py
python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py .agents/teamwork/tw-20261031-four-topics
```

To rerun the B300 checks:
- The re-evaluation and partition rebuild run via stdin to `/scratch/iitp4/worker_M3_r1/venv/bin/python -B -` with `PYTHONPATH=/scratch/iitp4/worker_M3_r1/code`.
- For the re-evaluation, use an idle-checked GPU and log the ledger rows.

**This review is invalidated by** any of:
- a change to any pinned file;
- a run.json whose code hash differs from the freeze list;
- a B300 re-evaluation outside the declared tolerance;
- a PI reversal of decision 2 or 3.
