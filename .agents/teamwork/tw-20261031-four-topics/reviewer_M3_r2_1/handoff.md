# handoff — reviewer_M3_r2_1 (M3 / Topic 2, gate r2) — HARD, 2026-11-01T10:00Z

**Verdict: APPROVE.** B1 is closed. B1 was the C4 issue that alone failed the r1 gate.
- I re-checked C1–C8 and T2.1–T2.3 myself, with my own probes. Every criterion is met with evidence.
- The card verdict **stop (killed)** reproduces byte for byte. It also reproduces independently, without importing the package.
- No integrity violation was found.
- Two run-level C4 items remain for root (§4, N1–N2). They are not in the worker's ownership and do not block this gate. **N1 blocks M3 closure** (victory audit) until root rules on it.

All my outputs are in `/home/juke/git/00IITP-AI/verification/reviewer_M3_r2_1/`.

## 1. Observation

### Hash checks (09:30Z; final re-check §5)
| check | result | file |
|---|---|---|
| C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` | rc 0, 67/67 OK | `c1_protected_hash_check.txt` |
| code freeze `code_sha256_at_freeze.txt` | rc 0, 33/33 | `code_freeze_check.txt` |
| `output_sha256_r2.txt` (156 lines) | rc 0, 156/156 | `output_r2_pins.txt` |
| `c4_sanitized_sha256.txt` | rc 0, 19/19 | `c4_sanitized_pins.txt` |
| old `card_sha256.txt` | 6 OK, FAILED on exactly `hcp_manifest.json` and `split.json` (as designed) | `old_card_pins.txt` |
| old `output_sha256.txt` | 27 OK, FAILED on exactly `stage0_hcp.json` and the 15 `runs/hcp_*/run.json` (as designed) | `old_output_pins.txt` |
| key artifact hashes | equal to every hash the worker claims (verdict.json 59af05e5…caf68, card c9bfc60a…41f5, addendum_05 aa07dd54…c6e5, new scripts and tests) | `key_artifact_sha256.txt` |

`output_sha256_r2.txt` covers every file under `results/topic2/2026-11-01` except itself (107 files). It also covers `docs/.../topic2`, `src/topic2_rgpool`, `tests/topic2_rgpool`, `scripts/topic2_*.py` and `scripts/b300_env`.

### Tests (C2)
| suite | where | result | file |
|---|---|---|---|
| old suite (explicit 3 paths) | local, nice, CUDA hidden | **86 passed**, rc 0 | `tests_old86.txt` |
| `tests/topic1_lagmotif` | local | **88 passed**, rc 0 | `tests_topic1_lagmotif.txt` |
| `tests/topic2_rgpool` full | local | **INVALID**: rc 143, earlyoom SIGTERM (host at about 90 % memory, 4.5 GB RSS killed) | `tests_topic2_rgpool.INVALID_earlyoom_rc143.txt`, `local_topic2_suite_earlyoom_journal.txt` |
| `tests/topic2_rgpool` full | connectome node4, Slurm job 217934, 4 CPU, project-local venv on /storage (torch 2.15.0+cpu, numpy 2.5.4, scipy 1.18.1, pytest 8.4.2) | **92 passed**, rc 0, 86 s | `connectome_topic2_suite.log` |

- The connectome copy is byte-identical to the repo. I checked all 40 code and test files against their sha256 (`connectome_copy_{local,remote}.sha256`).
- The env recipe is `connectome_build_env.sh`.
- The test-file counts are 8 + 10 + 21, which equals the 37 tests the worker claims to have added (55 + 37 = 92).

### C4 remediation (B1), independently checked
- **Repo-mode seal check.** `scripts/topic2_c4_seal_check.py repo` gives all_ok, R1–R5 (`seal_check_repo.json`).
- **My own stdlib checker.** I ran `indep_seal_compare.py` on B300 .98, next to the sealed originals. It does not import the worker's sanitizer. Output: `indep_seal_compare_b300.out.json`.
  - The sealed files equal `c4_sealed_originals_sha256.txt` (19/19) and the old pin lines (18/18).
  - **All 19 sealed files are byte-identical to r1's B300 originals** under `/scratch/iitp4/worker_M3_r1/` (runs, `hcp/manifest.json`, `code/split.json`, `partitions/stage0_hcp.json`, `logs/preprocess.log`).
  - I rebuilt the token map from the sealed manifest. That manifest is sorted by content hash, and each pseudonym is the hash prefix.
  - Each sanitized repo file equals its original after token mapping: **0 differing JSON leaves**. In the manifest only pseudonym, qc and T are kept; in the log only `sec` is dropped. `test_num` and `test_den` are identical in all 15 runs.
  - **0 occurrences** of any of the 264 original strings in the sanitized copies: 88 pseudonyms, 88 content hashes and 88 file sizes.
- **External anchors.** The original manifest and split hashes appear in commit 51609c1 (03:16:27Z, same commit as the card). The old pin-file hashes appear in 5125526 (05:46Z).
- **Manifest content.** The manifest now holds only `{pseudonym h00..h87, qc "pass", T 1200}` for all 88 subjects, so it carries no per-subject fingerprint.
- **Count-only scans.** The tokens were streamed from the B300 sealed manifest through an ssh pipe and never printed or written.
  - Working tree, 16,265 files: **0** files with a pseudonym or content hash, **0** with a file size (word match), and **0** paths containing a token. Positive control on the sealed root: 19 files (`token_scan_worktree.txt`).
  - Git history, 57 commits (all refs plus reflog since 2026-10-30), 264 patterns: **0** hits. With a marker string added as positive control: 101 hits (`token_scan_git_history_v2.txt`). The one commit made after the scan (09:46Z) also has 0 hits.
  - Session temp dir: 0 files.
  - HCP-ID scan v2: 1,084 names streamed from B300 `ls /scratch/data/hcp/download_HCP_REST1_filtered`, 716 files in M3 scope (topic2 results, docs, src, tests and scripts, b300_env, every `verification/*M3*` and `.agents/*M3*`, the ledger). **0** word hits, **0** strict hits (`hcp_id_scan_m3_paths_v2.txt`). My first attempt listed the wrong directory depth (1 name). I kept it, labelled INVALID (`hcp_id_scan_m3_paths.INVALID_wrong_depth.txt`).

### Verdict (T2.3)
- **Frozen script rerun.** I ran the frozen `scripts/topic2_verdict.py` on the relabelled runs, writing to my own directory. `verdict.json` and stdout are **byte-identical** to the shipped files (sha 59af05e5…caf68): `verdict_rerun.json`, `verdict_rerun_stdout.txt`.
- **Independent recompute.** `recompute_verdict_indep.py` uses no package import (`recompute_verdict_indep.out.json`).
  - 27 runs, all completed, `test_nmse` = Σnum/Σden.
  - The HCP test lists and `test_den` are identical across all 15 runs and equal `split.test`.
  - F+ gate: +3.061 % / +2.935 %, pass. F− gate: −1.737 %, pass.
  - I1 t95 [−0.0677 %, +0.3614 %]; I2 [+0.00098 %, +0.9455 %].
  - **stop**, with 0.0 difference from the shipped values.

### Mutation spot-check (my own 7 mutants, not the worker's list)
Run as Slurm job 217936 on connectome, each in a fresh copy with the full suite and `-x` (`rv_mutants.out.json`, `rv_mutants_connectome.log`). The baseline gave 92 passed.

| mutant | result | killed by |
|---|---|---|
| R2: t df n instead of n−1 | KILLED | `test_stats::test_t_interval_matches_hand_computation` |
| R3: script swaps I1/I2 in the verdict | KILLED | `test_verdict_script_reproduces_the_shipped_verdict` |
| R4: manifest re-adds `n_brain_vox` | KILLED | test_c4 manifest test |
| R5: two per-subject `test_num` swapped in one run | KILLED | shipped-verdict test (bootstrap) |
| R6: one run's test token changed | KILLED | test_c4 consistency test |
| R7: per-subject seed-mean taken on the wrong axis | KILLED | shipped-verdict test |
| **R1: keep rule uses I2 mean instead of I2 lower bound** | **SURVIVED** | — |

R1 is non-equivalent. With I1 (0.02, 0.01, 0.03) and I2 (0.003, −0.001, 0.007), the frozen code gives `modify` and the mutant gives `keep` (`R1_nonequivalence.txt`). The only modify test, at `test_stats.py:24`, uses I2 mean = 0, so it cannot tell the two rules apart.

The worker's mutation receipts match its claims:
- v2: baseline 91 passed, 101 of 102 killed, `c1:m18` survived;
- v3: baseline 92 passed, m18 killed (`verification/worker_M3_r2/mutation/v{2,3}_b300_mutants.out.json`, `v3_b300_baseline_suite.log`).

### Other checks
- **Ledger.** 30 data rows; the 14 completed rows total **11.99 GPU-h**. Last modified 06:12Z, before r2 started at 07:15Z, so r2 added no row, consistent with 0 GPU-h. I added no row: I used no GPU.
- **C7.** The vendored ver11 file equals `git show f0dc7aca:project/module/models/simmim_swin4d_transformer_ver11.py` (de132387…). The SwiFT_v2 working copy of that file is unmodified.
- **T2.1.** Merges occur only for `i_layer < num_layers − 1` (vendored line 1068).
- **Layout lint, whole run.** rc 0, 0 findings (`audit_layout_whole_run.txt`).
- **Git.** Every commit since 07:00Z is a 15-minute "docs(iitp): checkpoint" commit from the root session, so none is a worker git write. `results/` and `verification/` are untracked.
- **Explorer salt** (count-only, `explorer_salt_exposure_check.txt`).
  - `verification/explorer_M3_r1_1/dev_subject_salt.txt` holds a 32-character salt. It sits next to `dev_subjects_BURNED.md`, which holds 5 values of the form `sha256(salt + HCP dir name)[:16]` (formula at `scripts/topic2_preprocess_hcp.py:71`). Those 5 values also appear in `probe_stage0_hcp_dev.out.json`.
  - With the salt and the 1,084-name listing, or any 6-digit brute force, all 5 can be reversed. I did not perform this linkage.
  - Neither the salt nor any of the 5 values appears in any of the 143 commits (all refs plus reflog). The directory is untracked.
  - A B300 copy of the salt exists at `/scratch/iitp4/worker_M3_r1/code/scripts/dev_subject_salt.txt`.
- **Preprocess-log order.** `logs/preprocess.log` keeps per-subject lines in `imap_unordered` completion order over `sorted(os.listdir(src))` (`scripts/topic2_preprocess_hcp.py:67,81`). So the line order of h-tokens roughly follows sorted HCP-ID order. Anyone holding the B300 listing can use it to re-link tokens without hashing files. Addendum_05 §3 does not mention this route.
- **B300 Slurm state** (09:32Z). b300-01 (.98, 192.168.0.2) has 192 of 192 effective CPUs allocated to job 221, `eocd_m2_s3_p1`, from another team. That job started at about 06:30Z, before the worker's direct CPU runs there (07:28–09:01Z).
  - At 09:33Z, connectome was reachable, and node4 was idle and accepted my CPU Slurm jobs.

## 2. Logic Chain

1. **C1.** 67/67, rc 0. **C2.** 86, 88 and the new topic2 suite of 92 all pass in my own runs.
2. **C3.**
   - The card is unchanged (pin OK); the deviation is recorded in a dated addendum (addendum_05 §2).
   - The new pins are written to new files; the old pins are not overwritten.
   - All governed outputs are unchanged except the token relabel: 0 differing leaves after mapping, and the verdict is byte-identical.
   - So pre-registration still holds as r1's five verifiers established it.
3. **C4 (B1).**
   - The repo now uses a positional index, which is the C4 letter and r1's requested remedy.
   - The per-file fingerprints are removed: content hash, size, voxel count and timing.
   - The originals are sealed off-repo, verifiably genuine (byte-equal to the r1 B300 outputs and to the externally committed pins) and verifiably the source of the sanitized copies.
   - No token or ID exists in the working tree or git history.
   - So B1 is closed.
4. **Residual linkage.** A B300 data holder can re-link positions, by hashing or by log order. This is inherent to publishing per-subject results of public-data analyses. It is disclosed (except the log-order route), and it is not a C4-letter violation. → non-blocking, for root/PI to rule.
5. **The explorer salt** is a run-level C4-spirit exposure: a salted hash whose salt is stored beside it.
   - It is not in git history and not in the worker's ownership, and every r1 verifier treated it as non-blocking.
   - So it does not block this gate on the r2 deliverable.
   - It must be closed before M3 is declared complete, because the values are reversible in the working tree and on B300.
6. **T2.1–T2.3.** No governed file changed: code freeze 33/33, card and architecture pins OK. The verdict reproduces byte-identically and independently (stop: I1 upper bound 0.361 % < δ = 1 %). So the r1 findings for T2.1–T2.3 stand. δ and HCP-OA-as-public were PI decisions made before the freeze.
7. **C5.**
   - GPU: 0 GPU-h in r2; the ledger is unchanged at 11.99 of 64.
   - CPU: the worker's direct B300 CPU runs depart from the letter of C5 (CPU work goes to local or connectome). Its stated reason that connectome was unavailable did not hold at 09:33Z. The impact is small: nice, 6 processes, CPU only. → non-blocking, recorded.
8. **C6/C7/C8.**
   - C6: HCP-YA OA is public per the PI; no ENIGMA path.
   - C7: SwiFT_v2 is untouched.
   - C8: no old report numbers are cited as results.
9. **Tests are substantive.**
   - They use hand-computed oracles.
   - 6 of my 7 independent mutants are killed.
   - The worker's own 102-mutant receipts match its claims.
   - The one survivor (R1) sits on a branch that this run's data cannot reach (stop is decided first), so it is a coverage gap, not a defect in the result.

## 3. Caveats
- I did not repeat a GPU check. r1 verifiers re-evaluated checkpoints bit-exactly, and r2 changed no model or checkpoint. 0 GPU-h used by me.
- I did not reverse the explorer's 5 salted hashes, and I did not perform any positional re-linkage. Both are argued from code and formulas.
- The sealed originals live on B300 /scratch, which is wiped on VM stop. Their hashes are externally anchored in git, but the bytes are not durable yet (root action).
- **My own off-Slurm use of b300-01.** About 09:32–09:56Z, I ran a few seconds of stdlib python (`indep_seal_compare.py`), streaming `python3 -c`/`ls` calls for the scans, `sinfo`/`squeue`/`nvidia-smi` reads, and `rm` of my own directory. No GPU was used.
- **connectome footprint.** I created `/storage/connectome/00IITP-AI_verification/reviewer_M3_r2_1` (env, repo copy, logs) and removed it after copying the logs back. The parent directory now holds reviewer_M3_r2_2's directory, so I left it.
- **Read-only boundary.** I did not read other r2 verifiers' folders. I did not read `~/enigma_ocd` on B300.
- **DISPATCH.md** was first abridged (the worker JSON) and then restored verbatim at about 09:58Z (disclosed in the file).

## 4. Conclusion

**APPROVE** the M3 r2 work product. No blocking issue.

Non-blocking items for root/PI (rank order):

| # | item | action |
|---|---|---|
| N1 | **Blocks M3 closure.** The explorer salt `verification/explorer_M3_r1_1/dev_subject_salt.txt` sits next to 5 reversible dev-subject hashes (`dev_subjects_BURNED.md`, `probe_stage0_hcp_dev.out.json`). A B300 copy is at `/scratch/iitp4/worker_M3_r1/code/scripts/`. These are not in git history, but untracked and in the working tree. | Root: move the salt off-repo (or delete it) before any commit picks it up, and before the victory audit. |
| N2 | Positional residual linkage. The addendum misses one route: the `preprocess.log` line order ≈ sorted HCP-ID order. | Root/PI: rule on the positional scheme. If a stricter option is chosen, also drop or shuffle the log's per-subject order. |
| N3 | Sealed originals sit only on B300 /scratch. | Root: make a durable copy outside every git repository before the VM stops. |
| N4 | C5 CPU placement. The worker ran directly on b300-01 while that node was fully allocated to another team's Slurm job. Connectome was usable (my 2 Slurm jobs ran there). | Record the deviation. Future CPU verification should go to connectome Slurm with a /storage venv (`connectome_build_env.sh`). |
| N5 | Mutant R1 survives: the keep/modify boundary on the I2 lower bound is untested. | Add `S.verdict(I1=(0.02,0.01,0.03), I2=(0.003,-0.001,0.007)) == "modify"`. No effect on `stop`. |
| N6 | `test_c4_tokens_r2` scans only `results/topic2` and `docs/.../topic2`. It does not scan `.agents/**` (auto-committed) or `verification/`. | Extend the detector scope, or keep the whole-tree count scan as a gate step. |
| N7 | Already disclosed by the worker; carried forward: the latent `fm is not False` at `scripts/topic2_verdict.py:66`, and the C4 print incidents in addendum_05 §6. | Root records them. |

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt          # 67/67
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                             # 33/33
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c                   # 156/156
python3 scripts/topic2_c4_seal_check.py repo                                                          # all_ok
CUDA_VISIBLE_DEVICES="" PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -B scripts/topic2_verdict.py results/topic2/2026-11-01/runs /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-01/verdict.json
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_M3_r2_1/recompute_verdict_indep.py results/topic2/2026-11-01 /tmp/r.json   # stop, diff 0.0
```
- **Full topic2 suite.** The local host is memory-starved (earlyoom), so build `verification/reviewer_M3_r2_1/connectome_build_env.sh <BASE on /storage>` and run `connectome_run_topic2_suite.sh` through `sbatch -p debug -w node4 -c 4`. Expect 92 passed.
- **B300 independent seal compare.** `python3 -I indep_seal_compare.py /scratch/iitp4/worker_M3_r2/sealed_c4 <sanitized copy root> <pins dir> /scratch/iitp4/worker_M3_r1 out.json`. Expect all_ok.
- **Invalidation.** This review no longer holds if any of the following happens:
  - any pinned hash above changes;
  - a token or ID count scan returns > 0;
  - the sealed originals stop matching their pins;
  - any file under `results/topic2/2026-11-01` changes without a new dated pin.
- **Cleanup.** I left no processes on B300, connectome or locally. `/scratch/iitp4/reviewer_M3_r2_1` is removed. My connectome directory is removed. I added no ledger row (0 GPU-h).
