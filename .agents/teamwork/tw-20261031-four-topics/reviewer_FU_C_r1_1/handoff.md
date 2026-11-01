# Handoff (hard) — reviewer_FU_C_r1_1, milestone FU_C — 2026-11-01T20:06Z

## Review Summary
**Verdict: REQUEST_CHANGES** — one blocking C4 issue. The science, the freeze order, the verdict computation, compute and ledger all verify independently. No integrity violation was found. The FU-C verdict `stop` is reproduced exactly and is not affected by the blocking issue.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c .agents/.../sentinel/PROTECTED_HASHES.txt` → rc 0, 67/67 OK (`verification/reviewer_FU_C_r1_1/c1_check.out`).
- FU-C receipts, each rc 0 with 0 failures:
  - `card_sha256.txt` (36 lines);
  - `code_sha256_before_results.txt` (15);
  - `code_sha256_presentation_before_results.txt` (1);
  - `output_sha256.txt` (160).
- r1 receipts that FU-C relies on:
  - The 12 Fplus/Fminus fixture lines of `results/topic2/2026-11-01/output_sha256.txt` are 12/12 OK.
  - The failing hcp_* lines of that file (and 2 lines of the r1 `card_sha256.txt`) are the pre-sanitization pins. They were superseded by `output_sha256_r2.txt`, which passes (156/156).
  - `code_sha256_at_freeze.txt` passes 33/33.
- Tests:
  - tests/topic2_fu_c: 109 passed.
  - Old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`, STRICT_E2E=1): 86 passed.
  - tests/topic1_lagmotif: 88 passed.
  - tests/topic2_rgpool: 116 passed.
- Mutation harness: the worker's copy (sha 670a11e1…) was run with my own WORK and OUT on the pinned code.
  - Result: 55 entries; 51 KILLED; survivors baseline, V07c, V12 and F11; 0 INVALID.
  - Output: `verification/reviewer_FU_C_r1_1/mutants/worker_mutants_rerun.out.json`.
- Independent recomputation (`verification/reviewer_FU_C_r1_1/indep_recompute.py`; no FU-C or rgpool imports; card §3.3 pins re-typed from the card).
  - Inputs: the 24 records were read, and NMSE was recomputed as Σnum/Σden.
  - Provenance checked: settings, perm key, perm sha and perm file, split, code pins, h-token order, and start after 16:13:23Z.
  - Primary results:
    - I1 −0.113 % [−0.499 %, +0.272 %], df 7;
    - I2 +0.008 % [−0.520 %, +0.537 %];
    - verdict stop.
  - Stall analysis:
    - stalled runs: S_s15 and C_s16;
    - drop-stalled sensitivity (df 5): I1 +0.040 % [−0.213 %, +0.293 %];
    - pooled 13 seeds: I1 −0.013 % [−0.248 %, +0.222 %].
  - Every number equals the result report.
  - My only flag ("log ends at step 8700") is the frozen logging convention; r1 logs end identically.
- Verdict CLI rerun to `verification/reviewer_FU_C_r1_1/verdict_rerun.json`: byte-identical to `results/topic2/2026-11-02_fu_c/verdict.json` (sha 4d793102…f5).
- r1 gate recomputed from the 12 records: F+ gains +3.06 % / +2.93 % (pass); F− gain −1.74 % (pass).
- Freeze order.
  - Receipt headers: card frozen 16:13:23Z; code pinned 16:31:53Z.
  - All 15 code-pinned files have mtimes ≤ 16:31:41Z.
  - Host autocommit e5fa8de (16:20:26Z) already records "CARD FROZEN … sha fc2d0672…".
  - Autocommit cd1e43e (16:35:27Z) records the code pin at 16:31:53Z, with all jobs PENDING.
  - sacct: the earliest Stage-1 start is 16:35:09Z; run.json start_utc values run from 16:35:12Z to 19:08:03Z.
- B300 (read-only):
  - 48/48 run.json and train_log.jsonl files on B300 are identical to the repo copies.
  - Checkpoints exist, e.g. hcp_C_s16_a1/model_final.pt, 156 MB.
  - sacct: 25 fuc_* jobs, all COMPLETED, 1 GPU each, on b300-01.
  - ElapsedRaw sum is 37,520 s = 10.422 GPU-h, equal to the ledger: 50 worker rows, 25 jobs each with exactly 1 started and 1 closing row.
  - Explorers 0.262 → FU-C total 10.684 ≤ 13.
- Partitions:
  - perms_fu_c.npz E, C, group_mask and nvox are array-equal to r1 perms_hcp.npz.
  - The 8 new S surrogates are distinct from each other and from all r1 arrays.
  - C is a permutation of 4096 cells.
  - The card §3.3 shas reproduce from the array bytes.
- Command lines (`results/topic2/2026-11-02_fu_c/slurm/*.sbatch`) match card §4. No mask-seed overrides are passed; the frozen `scripts/topic2_train.py` defaults are 7001/7002 (lines 33–34).
- g3t rule: `scripts/topic2fu_c_slurm.py` cmd_submit runs `squeue` and `B.g3t_blocking` before admission and sbatch (lines 162–166; exit 3 if blocked).
- Layout lint: `audit_layout.py <run root>` → PASS, 552 files, 0 findings, rc 0.
- **C4 finding:**
  - Location: `tests/topic2_fu_c/test_gate_and_records.py` line 182, a negative fixture commented `# HCP-ID shape`.
  - It contains a 6-digit literal that **is a real HCP-YA subject ID**: it is a member of the 1,084 directory names in B300 `/scratch/data/hcp/download_HCP_REST1_filtered`.
  - Method: count-only membership test. The token was piped over stdin and never printed or written by me.
  - Every other 6-digit token in all tests/, src/ and scripts/ directories: 0 HCP-name hits. The perms_fu_c.json value 229304 is a voxel count and not an HCP name.
  - The file is untracked in git (not committed).

## 2. Logic Chain
1. **F1** (card frozen before results; states change, arms, seeds, budget, metric, δ and kill rule; reuses r1 machinery) holds.
   - The card text has §2 (the change), §4 (arms and seeds), §5 (metric, δ, rule) and §9 (budget).
   - The freeze time is corroborated by independent host commits and sacct (Obs. "Freeze order").
2. **F2** (own paths, synthetic fixtures, verdict code tested against the V06–V10 classes) holds.
   - The mutants V06–V10 are killed on the pinned code (Obs. mutation).
   - The 3 survivors are equivalent:
     - V07c: `gate_fixture` returns a Python bool, otherwise the decide() type guard would have produced no_verdict, not the shipped stop.
     - V12: that line is reached only when fplus_pass is True (verdict.py:286–288).
     - F11: two completed attempts hit `done[0] is not lst[-1]` (verdict.py:220).
3. **F3** holds:
   - runs via Slurm within the cap (sacct = ledger);
   - run records, ledger rows, the dated results dir;
   - the result report with the verdict and what it adds.
   - Numbers come from verdict.json (C8), which I reproduced independently.
4. **C2 and C3** hold (Obs. tests, freeze order, addendum 01). **C5 and C6** hold (Slurm only; HCP OA under PI decision 2). **C7 and C8** hold.
5. **C4 fails.** ACCEPTANCE C4 and the dispatch forbid writing participant IDs ("HCP 6-digit IDs"). A real HCP subject ID is written in a FU-C test file.
   - The chance that a random 6-digit number is one of the 1,084 names is about 0.12 %, so this is almost certainly a remembered or copied ID.
   - Neither of the worker's C4 checks covered tests/: the B300 scan covered the copy-back tree only, and the repo-side test covers the results dir only.
   - Run precedent: r1 failed its gate on recoverable HCP tokens, and root sealed even a salt. Under that strict standard this is blocking. It is not cheating, and it does not touch any number or the verdict.

## 3. Caveats
- I did not re-score a checkpoint on GPU (0 GPU-h used). Instead I rely on the B300 originals being sha-identical to the repo copies, on sacct, on internal num/den consistency, and on train logs that end at the frozen convention.
- I did not rerun the worker's B300 scan controls.
- Bitwise determinism was checked by the worker only to step 200 (anchor); I did not extend it.
- The rolling submission driver (`driver.sh`) lived in the worker's scratchpad, not the repo. A non-blocked g3t check is not logged per submission; the evidence is the code path plus progress notes. Both are minor provenance gaps.
- `squeue -o "%j"` name width was not tested on this Slurm version. No g3t job was reported at any time by other evidence.
- Scientific reading:
  - The stop is robust. Its upper bound is +0.27 % with the stalls and +0.29 % without them.
  - The report's claims "interval did not narrow" and "I2 not replicated" are descriptive and correctly labelled.

## 4. Conclusion
REQUEST_CHANGES. One blocking issue: the real HCP subject ID literal at `tests/topic2_fu_c/test_gate_and_records.py:182` (C4). Everything else meets C1–C8 and F1–F3 with evidence.

Suggested remediation, for root to decide. That file is pinned in `code_sha256_before_results.txt`, and `receipts.build_context` re-verifies that receipt, so a naive edit makes a verdict rerun return `no_verdict`. The steps:
1. Seal the original file bytes off-repo (e.g. under `~/.local/share/00IITP-AI_sealed/topic2/fu_c/`, 0400), as was done for the dev salt.
2. Replace the literal with a value that cannot be an HCP ID, e.g. `"000000"` (HCP IDs start 1–9). The test still exercises the HCP-ID-shape rejection.
3. Write a dated addendum 02 recording:
   - the old and new file sha;
   - that only that literal changed;
   - that the verdict-path files (verdict.py, logs.py, receipts.py, scripts/topic2fu_c_verdict.py) are unchanged;
   - that `verdict.json` (sha 4d793102…) was computed before the change.
   The original receipt is kept unedited. A supplementary post-result receipt is labelled as such.
4. Extend the repo-side C4 test to forbid standalone 6-digit literals in FU-C src/tests/scripts, with an explicit allowlist (e.g. the voxel count).
5. Rerun the suite and the mutation harness, then re-review.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256 code_sha256_before_results code_sha256_presentation_before_results output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_c/$f.txt | LC_ALL=C sha256sum -c --quiet; done
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
/home/juke/superclaude-env/bin/python3 -I -B verification/reviewer_FU_C_r1_1/indep_recompute.py /home/juke/git/00IITP-AI
/home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_verdict.py --out /tmp/x.json && cmp /tmp/x.json results/topic2/2026-11-02_fu_c/verdict.json
```
- C4 re-check: pipe all standalone 6-digit tokens from FU-C paths over stdin to B300 and count membership in `os.listdir('/scratch/data/hcp/download_HCP_REST1_filtered')`. Print counts only. Expected after the fix: 0.
- Invalidation: any change to the pinned files, the run records or verdict.json.
