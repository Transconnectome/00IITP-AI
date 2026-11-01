# Hard handoff — auditor_FU_C_r3_1 (forensic integrity audit, milestone FU_C, iteration 3)

## Forensic Audit Report

**Work Product**: FU_C (Topic 2 follow-up C, 8 seeds × 3 arms at E36), iteration 3 as handed off by worker_FU_C_r3, plus the r1/r2 artifacts it builds on.
**Profile**: General Project. Mode: Development. ORIGINAL_REQUEST has no "from scratch" or "do not delegate" constraint.
**Verdict**: **CLEAN**

Audit window: 2026-11-01T22:35Z to 23:00Z. I used 0 GPU-h and added no ledger rows. I made no git writes. I edited no production file. All probes are under `/home/juke/git/00IITP-AI/verification/auditor_FU_C_r3_1/`.

### Phase results
- **C1 protected hashes**: PASS. rc 0 at start and at end, 67/67 OK (`probes/c1_start.log`, `probes/c1_end.log`).
- **FU-C receipts**: PASS.
  - card 36/0, presentation 1/0, output_r2 27/0, output_r3 20/0.
  - code fails on 2 lines (13, 16) and output fails on 3 lines (141, 162, 164). This is exactly the set declared in addendum 02. `check_receipts_r2.py` reports ok true and failing_equals_declared on every receipt (`probes/check_receipts.out.json`).
  - c4_sealed_originals verifies.
- **Claimed artifact hashes**: PASS. All 14 sha256 values in the worker's frozen_artifacts list match the files on disk.
- **Card frozen before results**: PASS.
  - The card receipt has frozen_utc 16:13:23Z.
  - The first Stage-1 Slurm start is 16:35:09Z (sacct). The first start_utc in a run.json is 16:35:12Z.
  - All 24 run.json files have start_utc later than the freeze. My own script checked this.
  - Git anchor e5fa8de (committed 16:20:26Z) carries the progress line "16:13:23Z CARD FROZEN … sha fc2d0672…". The current card sha starts with fc2d0672.
  - Git anchor cd1e43e (committed 16:35:27Z) carries the code-pin line. It precedes the first job end at 17:01:06Z.
- **Hardcoded results / facades**: PASS.
  - The verdict path contains no literal result numbers.
  - `verdict.evaluate` computes from the run.json records.
  - My independent re-implementation (`scripts/indep_verdict.py`) used numpy/scipy only and none of the project modules. From the 24 raw records it gives: I1 −0.1132 % [−0.4985 %, +0.2721 %], df 7, so `stop` with the qualifier "sign unresolved"; I2 +0.008 % [−0.520 %, +0.537 %].
  - It found 0 provenance issues: perm keys and shas, perm file, split sha, code pins against the r1 freeze list, h-token shape and test order, finite num/den, and test_nmse = Σnum/Σden.
- **Records genuine, not fabricated**: PASS.
  - B300 `sacct` lists jobs 398, 401, 410 (CPU), 414, 501, 512–562 and 577. Their start and end times and ElapsedRaw values match the ledger rows exactly.
  - All 48 repo run.json and train_log.jsonl sha256 values are found in `/scratch/iitp4/fu_c/` on B300.
  - The B300 run.json mtimes equal the Slurm end times. A model_final.pt exists for every run.
- **Stalls**: PASS. C s16 and S s15 never fall below 0.995, so they are stalled runs. Card §6 counts them as valid primary runs, and both are included.
- **GPU use**: PASS.
  - Every FU-C job ran through Slurm and has paired start and close ledger rows.
  - The FU-C total is 10.697 GPU-h against a 13 GPU-h cap.
  - B300 shows no FU-C job after job 577 (05:03 KST). The r2 and r3 iterations used 0 GPU-h.
- **Verdict reproduction**: PASS.
  - `topic2fu_c_verdict_r2.py --out` exits rc 0, and its output is byte-identical to the shipped verdict.json (`cmp` OK, sha 4d793102…).
  - The frozen CLI with `--out` returns `no_verdict` with exactly the 2 declared problems.
- **Tests run and can fail**: PASS.
  - Suites: FU-C 210 passed, old 86 passed (STRICT_E2E=1), topic2_rgpool 116 passed (CUDA hidden), topic1_lagmotif 88 passed.
  - I ran my own mutation spot-check on a fully copied mirror with no symlinks into the repo. It covered 85 mutants: all 19 of R3, 28 of CR1, 25 of CR2, and 13 W verdict mutants (V01–V12, F11).
  - 81 were killed and 0 were invalid. The 4 survivors are exactly the claimed equivalents: V07c, V12, F11 and CR2:C10. I checked V12 and V07c against `verdict.evaluate`: the decide line runs only when `fplus_pass is True`.
- **C4 participant IDs**: PASS within FU-C scope. I matched every maximal 6-digit run against the 1,084 staged HCP names on B300 and returned only counts.

  | scope | unique runs | HCP hits |
  |---|---|---|
  | FU-C production paths (177 files) | 128 | 0 |
  | `verification/*FU_C*` (412 files) | 113 | 0 |
  | FU-C metadata (103 files) | 8 | 0 |
  | Git-history blobs of FU-C/topic2 paths (354) | 106 | 0 |
  | Git-history blobs of the whole run metadata (1,206) | 210 | 0 |
  | My own outputs | 51 | 0 |

  - Controls: the positive control (the first staged name, checked on the B300 side only) gives 1, and the negative control gives 0.
  - Retired file: 0 exact copies by sha256 in the worktree (files of 50 MB or less) and 0 among the 2,201 git blobs. The retired path never appears in `git log --all`. 0 tracked files exist under `verification/`.
- **Writes to protected or external paths**: PASS.
  - C1 holds, and pre-result receipts are byte-unchanged. The only declared failures are the r2 supersession of 2 test pins and the result report, recorded in addendum 02.
  - r3 adds new files only. Every new file is pinned in output_sha256_r3.txt, which is 0444.
- **Git writes by agents**: PASS. Since 2026-11-01T14:00Z the only commits are 31 "Chavis Autocommit" daemon snapshots and 5 root "checkpoint four-topics teamwork documents" commits. Both are documented in GATE_STATUS. No stash exists, and no agent wrote to the reflog.
- **Another project's env / installs**: PASS. The project-local venv is `/scratch/iitp4/fu_c/venv` (card §3.4). Run.json shows torch 2.15.0+cu134, which matches the lock.
- **Layout**: PASS. `audit_layout.py` on the whole run root gives rc 0, 684 files, 0 findings.

## 1. Observation
- Receipt failing lines: `sha256sum -c` printed FAILED only for `tests/topic2_fu_c/test_gate_and_records.py` (missing) and `tests/topic2_fu_c/test_perms_receipts_c4.py` in the code receipt. In the output receipt it also printed FAILED for `docs/…_fu_c_result_report.md`. These are lines 13 and 16, and 141, 162 and 164.
- `probes/indep_verdict.out.json`: `'I1': [-0.001132077587216562, -0.0049852598634198214, 0.002721104688986698, 7]`, `'verdict_indep': 'stop'`, `'issues': []`.
- sacct, for example: `512|fuc_hcp_E_s10_a1|gpu|b300-01|…gres/gpu=1…|2026-11-02T01:35:09|2026-11-02T02:01:08|1559|COMPLETED` (KST). The matching ledger row: `Slurm job 512 … 2026-11-01T16:35:09Z | 2026-11-01T17:01:08Z | 0.433`.
- Hash comparison: `comm -23 repo_hashes b300_hashes | wc -l` → 0, with 48 repo hashes.
- `probes/spot_mutants.out.json`: `{"n": 86, "killed": 81, "survived": ["baseline", "CR2:C10_mask_all_hexruns", "W:V07c…", "W:V12…", "W:F11…"], "invalid": []}`.
- `probes/c4_membership.out.json`: every FU-C group has member_hits 0. whole_worktree has member_hits 49 over 17,804 unique runs; see Caveats.

## 2. Logic Chain
1. The card was frozen (receipt and git anchor) before any Stage-1 job started (sacct), and the code was pinned before any job ended. C3 freeze order holds.
2. The 24 records exist on B300 with identical bytes, inside the Slurm job windows of ledgered jobs. The records are therefore real outputs, not fabrications.
3. A re-implementation that shares no code with the project gives the same I1, I2 and verdict from those records. The shipped verdict.json is reproduced byte for byte. The verdict is therefore computed, not hardcoded.
4. A separate mirror and runner kill every non-equivalent mutant I sampled. The 4 survivors are provably unreachable states. The tests can therefore fail on the targeted defects.
5. Counted against the actual staged HCP names, the FU-C repo paths, verification folders, metadata and their git history hold 0 HCP IDs. The retired file has no exact copy anywhere in the worktree or git history. Within FU-C, C4 holds.
6. GPU use is all through Slurm, ledgered and under cap. There are no agent git writes and no protected-file changes. No check failed, so the verdict is CLEAN.

## 3. Caveats
- **Near-copies.** I did not repeat the near-copy (≥30 % long-line overlap) test against the sealed original, because I chose not to read the sealed store. Exact-copy absence (sha256) and 0 HCP members among all bounded 6-digit runs in the FU-C scopes and their git history do cover the recovery risk in FU-C scope. A reformatted near-copy with the literal removed cannot be excluded by my checks.
- **Membership coverage.** Membership was tested only against the 1,084 staged names, so a 0 is not proof that a token is not an HCP ID. Runs inside longer digit strings were not tested.
- **Leads outside FU-C scope** (not FU-C violations; for root or the owning milestone's auditor). The whole worktree has 60 (group, token) member pairs:
  - 36 in `results/topic1/2026-10-31`. That data is ENIGMA, so these are probably numeric coincidences: 7,622 runs give about 9 expected hits under a uniform assumption, and HCP IDs are not uniform.
  - PDFs in `tmp/` and the repo root, and `docs/02_literature`, `docs/03_proposal/references`, `docs/reviews/references`.
  - M2 and M4 mutants and reruns, and a sha manifest.
  - 1 in `results/topic2/2026-11-02_fu_e/card_sha256.txt`. By masked context it sits inside a sha256 digest, so it is benign.
  - 2 in `verification/challenger_M3_r3_1/p06_c4_scan_r3_outputs.py`. Masked context shows that the two "HCP range" bounds written in that probe (lines 22–23) are themselves staged HCP subject IDs. This is an M3-scope C4 lead for root.
- **Accepted residuals.** The r1/r2 handoffs committed to git describe the literal in words. GATE_STATUS lists this as pending a PI decision, and I did not re-evaluate it. Agent transcripts are out of repo scope.
- **Run 1 of my spot-check was invalid**: its mirror lacked the GPU ledger file, so the baseline failed. I stopped my own process and kept its log as `probes/spot_mutants_run1_invalid_baseline.log`. The reported evidence is run 2.
- **GPU re-evaluation not repeated.** I did not re-evaluate a checkpoint on GPU. challenger_FU_C_r1_1 did so (job 577). Data integrity rests on sacct, B300 hashes and mtimes, and the independent recomputation.
- **DISPATCH.md** summarises the worker JSON embedded in the dispatch rather than copying it verbatim. I did this out of caution under the containment rule.

## 4. Conclusion
**CLEAN.** I found no hardcoded results, facades, fabricated logs, tests that cannot fail, pre-freeze results, silent fallbacks, participant-ID leakage in FU-C scope, protected-path writes, unledgered, non-Slurm or over-cap GPU use, use of another project's env, or agent git writes. The FU-C verdict `stop` (I1 −0.113 % [−0.499 %, +0.272 %], df 7) is genuine and reproducible. Separately, root should look at the M3 lead `verification/challenger_M3_r3_1/p06_c4_scan_r3_outputs.py` (lines 22–23).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py
python3 -I verification/auditor_FU_C_r3_1/scripts/indep_verdict.py          # independent I1/I2/verdict
python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json && cmp /tmp/x.json results/topic2/2026-11-02_fu_c/verdict.json
python3 -I verification/auditor_FU_C_r3_1/scripts/c4_membership.py          # count-only, needs ssh to B300
python3 -I verification/auditor_FU_C_r3_1/scripts/c4_gitblobs.py
python3 -B verification/auditor_FU_C_r3_1/scripts/spot_mutants.py OUT.json 2   # ~6 min
ssh connectome@61.107.201.98 'sacct -X -n -P -S 2026-11-01T00:00 -o JobID,JobName%40,Start,End,ElapsedRaw,State | grep -i fuc'
```
The audit becomes invalid if any of the following happens:
- any FU-C receipt fails on a line outside the declared 5;
- membership hits appear in FU-C scope;
- a B300 FU-C job is found that is not in the ledger;
- the independent recomputation disagrees with verdict.json.
