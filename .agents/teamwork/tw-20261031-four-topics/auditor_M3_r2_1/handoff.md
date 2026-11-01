# handoff — auditor_M3_r2_1 (forensic integrity audit, M3 / Topic 2, iteration r2) — HARD, 2026-11-01T10:30Z

## Forensic Audit Report

**Work Product**: worker_M3_r2's deliverables. These are the 19 sanitized result files, the three new pin files, `scripts/topic2_c4_sanitize.py`, `scripts/topic2_c4_seal_check.py`, `scripts/b300_env/mutation_pytest_pydeps.sh`, three new test files, `addendum_05`, `verification/worker_M3_r2/` and B300 `.98:/scratch/iitp4/worker_M3_r2/`. Milestone-level M3 invariants were re-checked too.
**Profile**: General Project. Integrity mode is **Development**: ORIGINAL_REQUEST has no "from scratch" or "no delegation" constraint, and C7 allows copying.
**Verdict**: **CLEAN**. The r2 work product shows no integrity violation.

There is one open C4 item at milestone level, outside r2's ownership, which root must resolve before closing M3: the explorer salt (§3, item N1).

### Phase Results

- **C1 protected hashes: PASS.** 67/67, rc 0 (`verification/auditor_M3_r2_1/c1_protected.txt`).
- **Freeze: PASS.**
  - The card sha is c9bfc60a…41f5, unchanged.
  - `code_sha256_at_freeze.txt`: 33/33.
  - Between 07:00Z and 09:30Z, the repo files outside `.agents/` and `verification/` that changed are exactly the worker's own paths, plus two `tests/topic3_spectral/*_r4.py` files that belong to worker_M2_r4. No frozen or protected file changed.
- **Pins: PASS.**
  - `output_sha256_r2.txt`: 156/156. It covers every file in the topic2 tree except itself.
  - The old pins fail on exactly 18 lines: `hcp_manifest.json`, `split.json`, `stage0_hcp.json` and the 15 hcp `run.json`.
  - All 14 claimed artifact hashes match the files on disk (`claimed_hashes_now.txt`).
- **Sealed originals vs pins: PASS.** I wrote my own probe, `probe_sealed_and_scan.py`. It streams the sealed tar from B300 into memory only.
  - 19/19 originals equal `c4_sealed_originals_sha256.txt`.
  - All 18 failing old-pin lines equal the sealed-original hashes; 0 failures are unexplained.
  - The sealed copies of `card_sha256.txt` and `output_sha256.txt` are byte-identical to the repo copies.
- **Sanitization is pure relabelling: PASS.** My probe built its own token map in original manifest order.
  - The original manifest is sorted by content hash, and each pseudonym is a 16-hex prefix of its content hash.
  - `split.json`, `stage0_hcp.json` and the 15 `run.json` (17 files) are **byte-identical** to the originals once each quoted token is replaced. No token occurs unquoted.
  - Manifest: only `content_sha256`, `file_bytes`, `n_brain_vox` and `sec` are dropped. Every other value is equal, and the `c4_sanitized.original_file_sha256` field equals the sealed hash.
  - `preprocess.log`: 88/88 subject lines equal the original minus `sec`, with the token relabelled; the 2 other lines are identical.
  - Provenance: `split.manifest_sha256`, all 15 `run.split_file_sha256` values, and the split hash quoted in both the partitions JSON and its log equal the sealed originals.
  - I recomputed the split from the original manifest with my own code. The test, val and train sets (16/8/64) match and are disjoint.
- **Verdict reproduction: PASS.**
  - The frozen `scripts/topic2_verdict.py`, run on the relabelled runs, gives `verdict.json` byte-identical (59af05e5…caf68), and its stdout is byte-identical to `logs/verdict_stdout.txt`.
  - My independent t-interval: I1 = +0.1468 % [−0.0677 %, +0.3614 %] and I2 = +0.4733 % [+0.0010 %, +0.9455 %]. The I1 upper bound is below δ = 1 %, so the verdict is **stop**.
  - Σnum/Σden equals `test_nmse` in 15/15 runs.
- **Tests: PASS.**
  - **Local:** the light files gave 25 passed, and seven heavier files gave 48 passed.
  - **Local failure (not a test failure):** `test_pipeline_guards_r2.py` was SIGTERMed by earlyoom (host memory).
  - **Full suite, independent run:** in my own Slurm CPU-only job 346 on b300-01, the result was **92 passed, 0 skipped**, rc 0.
    - The job requested no GPU and hid CUDA. `cpu=6,mem=40G`, 10:14:09–10:21:09Z.
    - It ran on my own tokenless bundle (sha c78aac5e…), with code hashes equal to the repo.
    - 0 skipped matters: the training-loop guards skip whenever CUDA is visible, so they really ran.
  - **Old 86 and topic1_lagmotif:** not re-run by me, to avoid more earlyoom collateral. The worker's logs show 86 and 88 passed. r2 changed none of their inputs (C1 67/67).
- **Mutation: PASS.**
  - The worker's v2 and v3 JSON files are consistent: every kill has rc 1 and a named first failing test.
  - The B300 copy of the v2 JSON is byte-identical to the local copy (f59d4f2a…).
  - I spot-checked 3 per-mutant logs; each matches its JSON entry.
  - **13 independent mutants, written by me:** relative_gain sign and denominator; NMSE ignoring the mask; NMSE den using rec; split taking test from the end; HCP eval mask identical for every subject; train loss ignoring the mask; test pass using the val seed; verdict I1 against S; verdict I2 against E; F− ignored; `<=` boundary; stop on the mean. **13/13 KILLED** (`b300_job/spot_mutants.out.json`).
- **Hardcoded results, facades, vacuous tests: PASS.**
  - New tests compute independent oracles (synthetic tensors, Hungarian, PCA, salted order) or end-to-end script runs on synthetic records.
  - The provenance test is self-referential, comparing pins from the same worker. My probe verified those pins independently.
  - The sanitizer and the checker are genuine (S1–S5 and R1–R5 logic was read; the repo mode re-ran all_ok).
- **C4 IDs and tokens: PASS (for r2).**
  - **What was scanned** (count-only, using the 88 tokens, 88 content hashes and 1,084 B300 HCP names, held in memory only):
    - the working tree: 16,353 files, 2.47 GB, including `.agents/` and all of `verification/`;
    - all 2,743 git objects, unreachable ones included (766 MB);
    - `/tmp/claude-1000`: 796,622 files.
  - **Tokens and hashes:** 0 hits anywhere.
  - **HCP-name pattern hits in the working tree and in git objects** are numeric coincidences only:
    - PDF stream lengths and binary streams;
    - one junit timestamp microsecond field;
    - 42 Topic-1 triad-motif counts (`021C`, `021U` and `021D` values, on ENIGMA-derived features).
  - **Scratch:** this session's scratch (d5bff6c5) has 0 hits of any class.
    - 1,078 files in OTHER sessions' scratch dirs have HCP-pattern hits. One session alone has 17,396.
    - I did **not** classify these. They are out of scope and not attributable to this run, so this is an unclassified observation only, recorded for root.
  - **Not content-scanned:**
    - files over 64 MB: 2 in the working tree (the topic1 `static_fc_upper_f32.npy` and an RFP `.zip`), 1 git blob, and 129 scratch files;
    - the contents of compressed containers (zip, compressed PDF streams), which a byte scan cannot see.
  - My own outputs: 0/0 hits on the closing rescan (`probe_selfscan_final.out.json`), run after the last metadata write.
- **GPU and ledger: PASS.**
  - The ledger has been unchanged since 06:12Z: 14 completed rows, 11.99 GPU-h, below the cap of 64.
  - B300 `sacct -a`, 16:00–18:45 KST, shows no job by this run. Every job belongs to eocd, p101, g3t, gard or nhp.
  - The worker's final suite had 0 skipped, which corroborates that CUDA was hidden.
  - My job 346 requested no GPU, so it used 0 GPU-h and needs no ledger row.
- **Env: PASS.**
  - The worker used the run's project-local venv (`/scratch/iitp4/worker_M3_r1/venv`) with `include-system-site-packages=false`. pytest exists only in `/scratch/iitp4/worker_M3_r2/pydeps`.
  - The only write into the venv after r1 is 411 pip `__pycache__` files at 08:04Z, a side effect of `pip install --target`. No package was added.
  - `~/envs/swiftllm` is untouched (mtime Oct 30), and nothing in `~/.local` changed.
- **Git writes: PASS.** The reflog shows only checkpoint commits, on the 15-minute cadence at +28 s. There is no stash. `results/topic2/` and `verification/` are untracked.
- **ENIGMA: PASS.** There is no ENIGMA file under `/scratch/iitp4`. PI decision 5 relaxed C6 in any case.
- **Orphans: PASS.**
  - No worker process remains on B300 or locally. The one matching local shell belongs to reviewer_M3_r2_2.
  - My own B300 dir was removed after copy-back; job 346 completed.
- **Layout: PASS.** Whole-run `audit_layout.py`: rc 0, 0 findings. The closing re-run after the last metadata write is `audit_layout_whole_run_final.txt`.
- **Closing checks** (after the last write): C1, r2 pins, layout and self-scan were re-run; the outputs are `*_final.*` in `verification/auditor_M3_r2_1/`.

## 1. Observation
- `probe_sealed_and_scan.stdout` / `.out.json`. Key fields: `sealed_vs_c4_sealed_pins_match` 19, `old_pins_failing_that_equal_sealed_original` 18, `old_pins_failing_unexplained` [], `swap_all_byte_identical` true, `preprocess_log.subject_lines_ok` 88, `split_recompute.*.set_equal` true, git `hits` hcp_id only, and `explorer_salt_check` {5 hashes, 5 recoverable}.
- `b300_job/suite.log`: "92 passed, 26 warnings in 62.01s", rc=0. `b300_job/spot_mutants.out.json`: baseline 92 passed; 13/13 KILLED, all with rc 1.
- `scripts/topic2_preprocess_hcp.py:67,81-83`: `names = sorted(os.listdir(a.src))`; subject lines are printed in `pool.imap_unordered` completion order.
- `tests/topic2_rgpool/test_pipeline_guards_r2.py:119-120,219-220`: `if torch.cuda.is_available(): pytest.skip(...)`.

## 2. Logic Chain
1. Fabrication of the remediation would show in three ways: the originals would not match the old pins, the sanitized files would differ from the originals by more than the relabelling, or the verdict would not reproduce. All three were checked independently (streamed originals; byte-level relabel identity; byte-identical verdict). None occurred.
2. Residual tokens would show in the working tree, in any git object or in this session's scratch. 0 token or hash hits; the HCP-pattern hits are numeric coincidences by key and context.
3. Fake test or mutation evidence would show in an independent run. My Slurm run reproduced 92 passed, 0 skipped. My own 13 mutants, written independently, were all killed. The worker's B300 artifacts are byte-identical to the local copies.
4. Hidden GPU use would show in the ledger, in sacct, or in skip behaviour. The ledger is unchanged, sacct holds no job from this run, and the guards would have skipped had CUDA been visible.

## 3. Caveats
- **N1 (open C4 item for root; outside r2 ownership, flagged before by auditor_M3_r1_1 and the worker).** `verification/explorer_M3_r1_1/dev_subject_salt.txt` sits next to `dev_subjects_BURNED.md`.
  - From the two files plus the HCP name list, 5/5 burned HCP subject IDs can be recovered. My computation was count-only.
  - The files are untracked and not in git history. A broad `git add` would commit them.
  - Root should resolve this before declaring M3 complete: move or seal the salt off-repo, or delete it after recording the hashes.
- **N2 (disclosure gap, for root/PI).** Addendum_05 §3 names hashing of the staged files as the relink route. There is a second channel:
  - the order of `preprocess.log` subject lines is `imap_unordered` completion order over sorted HCP directory names, so it approximates each token's HCP-ID rank. This is inferred **from code reading** only (`scripts/topic2_preprocess_hcp.py:67,81-83`); I did not measure how closely the order tracks the rank;
  - relinking this way needs only the staged directory listing, not hashing;
  - it still requires B300 or data-holder access;
  - option: reorder or drop the log lines (`preprocess.log` is non-governing).
- **N3.** The CUDA-visible skip in 3 training-loop guards means those tests cannot fail in a CUDA-visible env, such as the default on DGX-Spark. The worker documents `CUDA_VISIBLE_DEVICES=""`. Recommend failing instead of skipping.
- **N4 (C5 placement, self-disclosed by the worker).**
  - The worker's CPU work ran directly on .98, outside Slurm.
  - I could not verify the claimed connectome timeout: connectome answered me at 09:51Z. However, its system python is 3.8 without torch, which supports "cannot run these jobs as is".
  - My own job also ran on B300 CPU, but through Slurm and with no GPU, because local earlyoom made the full suite impossible. That is also a C5 placement deviation.
- **N5 (errata, trivial):**
  - the full_handoff text swaps the suffixes of the two c4 pin hashes;
  - addendum §5 says "103 mutants" (it is 102 plus the baseline);
  - the recipe header says "no change to any venv", but pip bytecode was written;
  - the handoff says the addendum was edited at "~09:20Z"; its mtime is 09:17:26Z, before the r2 pins at 09:17:26.5Z.
- **My own incidents:**
  - probe v1 was too slow; I stopped it by its own PID and preserved it (`probe_sealed_and_scan.py.v1_stopped_too_slow`);
  - local pytest runs (1.1 GB, then 4.4 GB RSS) were SIGTERMed by earlyoom at 09:51Z and 10:01:19Z. In the same second earlyoom also SIGTERMed other processes, one of them `ollama` (uid 996). My process may have contributed to that memory pressure.
- **Not done:**
  - I did not re-run old86 or topic1_lagmotif;
  - I did not re-run the worker's 102-mutant harness, only my 13;
  - I did not inspect transcripts, so the print incidents rest on self-disclosure.

## 4. Conclusion
**CLEAN.** The C4 remediation is a verified pure relabelling:
- the sealed originals equal every old pin;
- the verdict, **stop**, is reproduced byte for byte;
- no token or content hash exists in the working tree or in any git object;
- the new guard tests are genuine and kill independent mutants;
- 0 GPU-h, no git writes, no foreign env.

Open for root: N1 (must be resolved before M3 closure); N2 and N3 (recommended).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c
/home/juke/superclaude-env/bin/python3 -I verification/auditor_M3_r2_1/probe_sealed_and_scan.py $PWD /tmp/out.json   # ~15 min, count-only
PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -B scripts/topic2_verdict.py results/topic2/2026-11-01/runs /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-01/verdict.json
# B300 (CPU-only Slurm, no GPU): copy verification/auditor_M3_r2_1/b300_job/{job.sh,spot_mutants.py} + a tokenless bundle to /scratch/iitp4/<id>/, then
#   sbatch -p interactive --nodelist=b300-01 -c 6 --mem=40G -t 00:50:00 job.sh
```
**Invalidation conditions:** this audit is invalid if any of the following happens:
- any pin or the sealed tree changes;
- a token appears in a new commit;
- the explorer salt is committed.
