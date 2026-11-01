# Handoff (hard) — reviewer_FU_C_r1_2, milestone FU_C, 2026-11-01T20:04Z

## Review Summary

**Verdict: REQUEST_CHANGES.** There is one blocking item, a C4 literal (B1 below). The science is independently confirmed: verdict `stop`, I1 = −0.113 % [−0.499 %, +0.272 %] (t, df 7), I2 = +0.008 % [−0.520 %, +0.537 %], and the r1 gate F+/F− passes. None of the findings changes the shipped verdict.

## 1. Observation

**C1 and receipts**
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0 (67 lines, 0 failures).
- These receipts verify with rc 0: `card_sha256.txt` (41 lines), `code_sha256_before_results.txt` (21), `code_sha256_presentation_before_results.txt` (5), `output_sha256.txt` (166).
- Current sha256 values: card `fc2d0672…4ecb`, verdict.json `4d793102…80f5`, result report `36290855…313a`, verdict.py `9a1425b6…3060`.

**Tests** (I reran all of them)
- tests/topic2_fu_c: 109 passed.
- Old suite (STRICT_E2E=1): 86 passed.
- tests/topic2_rgpool: 116 passed.
- tests/topic1_lagmotif: 88 passed.
- flake8 (max line 120) is clean.
- `audit_layout.py` on the run root: 0 findings, rc 0, 545 files.

**Independent recomputation** (`verification/reviewer_FU_C_r1_2/recompute.py`; numpy/scipy only, no FU-C or rgpool import)
- Provenance problems found: 0. The script checked:
  - all 24 records present, `status` completed, r1 settings;
  - perm_key, and perm_sha256 against arrays hashed directly from `perms_fu_c.npz`;
  - npz file sha, code_sha256 against the r1 freeze pins, split sha;
  - test order against the split, h-token format, Σnum/Σden;
  - start_utc later than both the card freeze and the code pin.
- Result: I1 and I2 equal verdict.json exactly (max abs diff 0.0). Verdict `stop`.
- Gate from the 12 pinned r1 fixture records: F+ +3.061 % / +2.935 % (pass), F− −1.737 % (pass).
- Stalls: C_s16 (min loss 0.99824) and S_s15 (0.99803).
- Drop-stalled-seed sensitivity: I1 +0.040 % [−0.213 %, +0.293 %], df 5.
- Pooled 13-seed I1: −0.013 % [−0.248 %, +0.222 %].

**Shipped verdict script and report**
- Rerunning `scripts/topic2fu_c_verdict.py --out <mine>` gives JSON identical to the shipped verdict.json.
- The report tables, re-rendered with `scripts/topic2fu_c_report_tables.py`, match the report line for line. Only the subsection headings differ (the report renumbers them as "### 1.").
- The r1 numbers cited in the report match `results/topic2/2026-11-01/verdict.json` (I1 +0.147 [−0.068, +0.361], I2 +0.473 [+0.001, +0.946]) and r1 addendum 04 line 23.

**B300 (read-only ssh; no GPU used)**
- `sacct` for the 25 FU-C jobs (501, 512…562) shows every job COMPLETED on b300-01, gres/gpu=1, ExitCode 0:0. The ElapsedRaw and Start/Submit values match `slurm/jobs.json`.
- There are exactly 25 FU-C job names, so no `_a2` attempts.
- `sha256sum */run.json */train_log.jsonl` on `/scratch/iitp4/fu_c/runs` is identical to the repo copies (48 lines; `b300_run_sha.txt` vs `repo_run_sha.txt`).
- The 16 run-path code files in `/scratch/iitp4/fu_c/code` (14 in src/topic2_rgpool, plus scripts/topic2_train.py and topic2_build_partitions.py) are OK against the r1 freeze pins.
- The B300 npz and split sha equal the pins.
- `sacct -a` for 2026-11-01 13:00Z–21:00Z shows 0 jobs named `g3t-G-E0-*`, so the B300 share rule was satisfied.

**GPU**
- Total in jobs.json: 10.422. Adding the explorer ledger rows (0.14 + 0.072 + 0.05 = 0.262) gives 10.684, within the 13 GPU-h cap.
- The ledger has 50 worker_FU_C_r1 rows: a started row and a closing row for each of the 25 jobs.
- Every admission projection is ≤ 12.957 ≤ 13.

**Freeze order**
- Card frozen 16:13:23Z; card mtime 01:13 KST.
- Anchor job 501 ran 16:04:53–16:08:23Z, before the card freeze. This is disclosed in card §0/§3.5, and no val/test outcome was computed.
- The first submission (16:13:51Z) came after the card freeze.
- Verdict code and tests were pinned at 16:31:53Z.
- The first run started at 16:35:09Z (sacct) / 16:35:12Z (run.json). The first run ended at 17:01:08Z, so no Stage-1 result existed before the code pin.
- Copy-back: directory mtime 04:39:26 KST.

**Partitions**
- E, C, group_mask and nvox in `perms_fu_c.npz` are array-equal to r1 `perms_hcp.npz`.
- All perms are valid permutations of 4096.
- The 8 new S surrogates differ from each other and from r1 S_seed0..4.

**Anchor**
- I read the anchor `train_log.jsonl` against the r1 `train_log.jsonl` directly: steps 100 and 200 are bitwise equal for hcp_E_s0, hcp_C_s0 and Fplus_C_s0.

**Mutation testing**
- The worker harness, rerun by me (`worker_mutants_rerun.out.json`), gives 55 entries, 51 killed, and the same 3 survivors (V07c, V12, F11). I checked their equivalence arguments and they hold:
  - V07c: `gate_fixture` returns `bool(ok)`.
  - V12: that line is reached only when fplus_pass is True.
  - F11: two completed attempts are still caught by "attempt follows a completed run".
- My 22 extra mutants (`extra_mutants.out.json`): 9 killed, **13 survive**. The survivors are X02, X04, X05, X06, X07, X11, X12, X13, X14, X15, X16, X21, X22 (see Minor M1).

**C4 count-only scan**
- I scanned 171 FU-C files: results, src, tests, verification/worker_FU_C_r1, the worker metadata, the FU-C docs and the scripts.
- `tests/topic2_fu_c/test_gate_and_records.py` line 182 has a 6-digit literal, used as the "HCP-ID shape" negative case: `{"test_pseudonyms": ["<6-digit>"] + H.TEST_LIST[1:]}`.
- I classified it without printing it. It is a **real HCP-YA S1200 participant ID**, namely the subject used throughout the public HCP documentation and tutorials.
- No other FU-C file contains a 6-digit ID-like token. The only other 6-digit hit is `n_group_mask_voxels`.
- The file is untracked in git (`?? tests/topic2_fu_c/`). The root checkpoint loop commits only .md and .txt files, so the literal is not in git history.
- `results/topic2/2026-11-02_fu_c/c4_scan_b300.json` shows 0 hits for the 72 copied files. That scan, and the repo test `test_fu_c_results_carry_no_subject_identifiers`, cover only the results tree, not tests/.

## 2. Logic chain

1. **F1 is met.** The dated card was frozen and receipted (16:13:23Z) before any FU-C real-data result. No Stage-1 run had started before 16:35Z, and none had finished before 17:01Z. The card states:
   - the change (seeds 10..17 only);
   - arms E, C, S, and seeds;
   - the budget (8,750 × 16 = 140k samples);
   - the metric (masked NMSE), δ = 1 % (decision 3), and the stop/keep/modify/inconclusive rule;
   - reuse of the r1 gate and verdict machinery.

   The anchor before the freeze is disclosed and produced no outcome.
2. **F2 is met on the verdict path, with one gap.**
   - The code sits in its own paths, and no frozen file changed (C1 rc 0; r1 code pins OK).
   - The synthetic fixtures carry planted effects.
   - The V06–V10 classes are killed (V06, V07, V07b, V08, V09, V10 KILLED in my rerun).
   - The 13 surviving extra mutants are guards whose removal does not change the shipped verdict. Several are also masked by sha pins (M1).
3. **F3 is met.**
   - All runs went through Slurm on B300 (sacct). Every job has a ledger started row and a closing row.
   - 10.684 GPU-h is within the 13 GPU-h cap.
   - Results are in the dated dir. The repo copies are byte-identical to B300.
   - The result report gives the verdict per card §5 and the reading per §11, and says what FU-C adds to r1.
4. **The verdict is correct.**
   - My independent recomputation reproduces every primary and sensitivity number, and the real data are far from every boundary: hi 0.27 % vs δ 1 %.
   - The rules match card §5: strict hi < δ; the F− failure downgrades keep only; the F+ failure leads to inconclusive.
5. **No integrity violation.**
   - The records on B300 are identical to the repo, and Slurm accounting confirms real ~1,550 s training jobs.
   - No hardcoded results were found in src (the verdict is computed from the records).
   - The mutation outputs reproduce.
6. **C2, C3, C5, C6, C7 and C8 are met.**
   - C2: the suites pass.
   - C3: card before results, fixtures, raw logs, dated paths, deviations in addendum 01.
   - C5: Slurm only; cap; ledger; g3t rule.
   - C6: HCP OA on B300 under decision 2; checkpoints stay on B300.
   - C7: external repos are not touched.
   - C8: the numbers come from verdict.json and r1 dated files.
7. **C4 is not met by its letter.**
   - The dispatch rule is explicit: "no participant IDs printed or written (HCP 6-digit IDs…)". A real HCP subject ID is written into a repo test file, so the criterion fails.
   - Its harm is low. The ID is publicly documented by HCP, it is not linked to any data or token in this repo, and it is not in git history.
   - Even so, APPROVE requires every criterion to be met, so this is blocking.

## 3. Findings

### [Blocking / Major, C4] B1: a real HCP participant ID literal in a test file
- **What:** `tests/topic2_fu_c/test_gate_and_records.py:182` uses a real HCP-YA subject ID as the "HCP-ID shape" negative case in `test_I_V09_test_order_mismatch_is_no_verdict_not_exception` (parametrized list at lines 181–182).
- **Why it matters:** ACCEPTANCE C4 and the dispatch forbid writing HCP 6-digit IDs, and the worker's handoff states "No participant ID was printed or written". The worker's C4 scans covered only results/.
- **Fix:**
  - Replace the literal with a 6-digit string that cannot be an HCP ID. HCP IDs never start with 0, so "000000" works, or the test can generate one at runtime, e.g. `"%06d" % 0`.
  - The file is pinned in `code_sha256_before_results.txt`, and `receipts.build_context` re-verifies every entry of that receipt. A plain edit therefore turns a re-run of `scripts/topic2fu_c_verdict.py` into `no_verdict`. The edit needs:
    - a dated addendum 02 recording the change (test-only, after results, no verdict-path change);
    - a supplementary receipt for the new test file, leaving the historical receipt untouched;
    - a documented way to rerun the verdict, e.g. verifying the historical receipt against the preserved original bytes stored off-repo, or a receipt-chain rule.
  - Alternatively, root or the PI may record a de-minimis exception in an addendum, on the grounds that the ID is a public documentation example. Either way, extend the repo C4 test to scan tests/ and src/ for the FU-C package.
- Membership of this ID in the 88-subject cohort was not checked; that would need the sealed list, which I did not read.

### [Minor] M1: 13 reviewer extra mutants survive the suite (none changes the shipped verdict)
- **Fail-closed on real data** (the real-repo verdict run would show no_verdict): X05, where gate_pins is filtered to Fplus only.
- **Redundant under sha pins:**
  - X06: the split-sha check in receipts is removed, but the split is a governing pin and check_record compares the record split sha.
  - X14 and X15: gate-record seed and source are not checked, but the records are sha-pinned to r1 output_sha256.
- **Receipt guards, fail-open but covered externally by `sha256sum -c`:**
  - X02: the code receipt may predate the card freeze.
  - X04: the stats.py pin check is removed.
  - X21: a receipt line outside a section is accepted.
- **Robustness and boundaries:**
  - X07: negative per-subject num is allowed.
  - X11: the NMSE consistency tolerance is loosened from 1e-9 to 1e-3.
  - X12: bool counts as finite.
  - X13: a regular file named like an attempt is accepted.
  - X16: start_utc == freeze is accepted.
  - X22: the qualifier at hi == 0 says "C worse".
- **Suggestion:** add tests for the guards. Of these, X02, X04 and X07 matter most.

### [Minor] M2: the report omits the r1 scope caveat on reconstruction headroom
- Every arm's test NMSE is 0.9867–1.0000, so the models reconstruct about 1 % of the masked variance. The r1 report (line 24) states this and limits "stop" to that setting.
- At this headroom, δ = 1 % relative NMSE means C must roughly double the variance the model learns. The FU-C report §0 and §5 should restate this so that the replicated stop is not read as a general null.

### [Minor] M3: all report subsection headings are "### 1."
- This is cosmetic. It comes from the renderer's headings being prefixed with "1." in the report.

### [Info] I1: checkpoint re-scoring was not performed by this reviewer
- I used no GPU: the B300 queue held many PENDING jobs from other teams. Record integrity was established through B300 and repo sha identity and through sacct.

### [Info] I2: disclosed limitations are accurate
- The precision prediction failed (half-width 0.386 % against the predicted 0.144 %).
- The gate was reused by reference.
- Determinism was verified only to step 200.
- The same 16 test subjects were used.
- The 2/24 stalls are counted in the primary analysis per card §6.

## 4. Caveats
- I did not read the sealed salt or the original token list, so cohort membership of the B1 ID is unknown.
- I did not re-score test NMSE from checkpoints, and did not re-run any training.
- "No Stage-1 number read before copy-back" is bounded only by timing: the verdict code was pinned before the first run ended. The worker's monitoring behaviour between 17:01Z and 19:39Z cannot be audited beyond its scripts. The governing code was pinned earlier, so this cannot have changed the verdict.
- The other verification/* mutant mirrors (reviewer_FU_C_r1_1, auditor_FU_C_r1_1, challenger_FU_C_r1_2) contained transient copies of the same test file while those agents ran. They are not mine, and I did not touch them.

## 5. Conclusion
- FU-C's scientific result and verdict (`stop`, r1 stop replicated on 8 fresh seeds) are correct, reproducible, and properly frozen, computed, ledgered and capped.
- REQUEST_CHANGES rests solely on B1 (C4 literal). After B1 is fixed or a recorded exception is in place, and the C4 scan is extended to tests/, this milestone would pass this review. M1–M3 are nonblocking.

## 6. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256 code_sha256_before_results code_sha256_presentation_before_results output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_c/$f.txt | LC_ALL=C sha256sum -c --quiet; done
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_FU_C_r1_2/recompute.py    # independent verdict
/home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_C_r1_2/extra_mutants.py $PWD <work> <out.json>
# B1 (count only, prints nothing sensitive):
python3 -c "import re;t=open('tests/topic2_fu_c/test_gate_and_records.py').read();print(len(re.findall(r'(?<![0-9A-Za-z.])[1-9]\d{5}(?![0-9A-Za-z.])',t)))"   # expect 0 after fix
```
Invalidation conditions:
- Any receipt check fails.
- recompute.py reports problems or a different verdict.
- The B300 record sha values differ from the repo.
