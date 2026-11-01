# Hard handoff — reviewer_FU_C_r2_2 (FU-C iteration-2 gate review), 2026-11-01T21:27Z

## Review Summary
**Verdict: REQUEST_CHANGES** — one blocking C4 item, and it needs a root/owner-side fix, not a new worker iteration. Everything worker_FU_C_r2 claimed was independently reproduced.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0, 67/67 OK, at start (21:05Z) and at end (21:26Z) (`verification/reviewer_FU_C_r2_2/c1_{start,end}.out`).
- Tests: `tests/topic2_fu_c` 180 passed; old suite (STRICT_E2E=1, 3 targets) 86 passed; `tests/topic2_rgpool tests/topic1_lagmotif` 204 passed (=116+88); flake8 clean; `audit_layout.py` on the run root: 0 findings, rc 0.
- Hashes of the card (fc2d0672…), verdict.json (4d793102…), verdict.py, receipts.py, addendum_02 (59e7205d…), result report (bb30a79c…), new src/tests and output_sha256_r2.txt (a1e317c7…) all equal the worker's claims.
- `scripts/topic2fu_c_verdict_r2.py --out verification/reviewer_FU_C_r2_2/verdict_r2.json`: rc 0, `cmp` byte-identical to the shipped verdict.json. `supersession.reproduce_verdict` calls the unchanged `receipts.build_context` and `verdict.evaluate` on the real run records; nothing is hardcoded.
- The frozen CLI (`--out`, into my dir) returns `no_verdict`, with exactly 2 problems: test_gate_and_records.py missing, test_perms_receipts_c4.py changed.
- `sha256sum -c` per receipt: card 36/36; code 13 OK + 2 FAIL (the declared lines 13 and 16); presentation 1/1; output 157 OK + 3 FAIL (the declared lines 141, 162, 164); output_sha256_r2 27/27. `check_receipts_r2.py` ok true.
- Seal: `c4_sealed_originals_sha256.txt` verifies (OK); sealed dir 0700, file 0400.
- Independent recompute from the 24 `runs/hcp_*_a1/run.json` (all `completed`):
  - I1 −0.113 % [−0.499 %, +0.272 %], df 7; I2 +0.008 % [−0.520 %, +0.537 %]. The upper bound is below δ, so the verdict is `stop`.
  - Addendum 02 numbers: sd without s16 0.220 %, half-width 0.204 %; δ/learned signal 85.4 %, I1 upper bound / learned signal 23.2 %.
  - All 24 `start_utc` values are 20-character `Z` strings. Every number matches.
- Mutation union rerun (worker harness, sha in `mutants/harness_sha256.txt`; outputs in `verification/reviewer_FU_C_r2_2/mutants/`):
  - 150 entries, 5 deselected (baseline-checked), 146 killed, 0 invalid. Survivors: the baseline and the r1-accepted equivalents V07c, V12 and F11.
  - The status of every mutant equals the worker's table. All 149 mutants target copied `src/` files, so production files were never touched.
- C4 sweeps (all boolean or count-only):
  - Near-copy sweep of 23,156 working-tree text files (`probes/nearcopy_sweep.out.json`): exactly one file shares ≥50 % of the retired file's long lines: `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` (overlap 1.0). Its `recoverable_by_single_6digit_substitution` is **true** against the old pin on code receipt line 13. The re-authored r2 tests are not near-copies.
  - Wide B300 membership (`probes/b300_membership_wide.out.json`, v2): 1,313 files under all `verification/*FU_C*` dirs, FU-C metadata dirs and FU-C production paths hold 279 unique 6-digit runs. **0** are among the 1,084 staged HCP names; the remote positive control is valid and the negative control is 0. (The v1 run is INVALID: its positive control failed because of a pipeline bug. It is kept as `*_v1_INVALID.out.json`.)
  - Git history (`probes/b300_membership_githistory.out.json`): 115 commits, 6.3 MB of patch text over FU-C paths, `verification/` and the run metadata, 354 unique 6-digit runs, **0** members; controls valid. Neither the retired file nor the explorer tree was ever committed.
- GPU ledger: 58 FU-C rows summing to 10.697 GPU-h. That is the worker's 10.684 plus the challenger_FU_C_r1_1 verifier probe (job 577, 0.013). No worker_FU_C_r2 rows. Under the 13 GPU-h cap.

## 2. Logic Chain
1. The worker's remediation does what it claims: the seal, the retirement, the re-authored tests, the declared supersession, the byte-identical reproduction, the mutation evidence and the corrected report §4 (Observation 1–7). No integrity violation was found: the verdict is computed from records, not echoed, and the tests use synthetic roots and run-time controls.
2. C4 requires that no participant ID be printed or written. The M3 r1 gate precedent, carried into the T2.4 wording, also treats repo content from which an ID can be recovered as a C4 failure.
3. The old file sha stays in a pre-result receipt that may not be edited. The explorer tree holds an in-place-edited near-copy of the retired file. Together they recover the real HCP-YA ID with a single 6-digit substitution (Observation, near-copy sweep). That file is in the repo working tree, in a FU-C milestone verification dir.
4. So C4 is not met for milestone FU-C as it stands, although the worker could not fix it (not its path) and disclosed it as GATE-RELEVANT.
5. Every other criterion (C1, C2, C3 incl. the frozen card and addenda, C5 cap and ledger, C6, C7, C8 sources, F1–F3) is met with evidence.

## 3. Caveats
- **Self-incident (disclose to root).** The first stdout of my probe `probes/recoverability_nearcopy.py` printed a substitution try counter from which the literal can be derived. It appeared in this agent's transcript only, outside the repo.
  - I removed the counter from the output file within about a minute and from the probe code. The rewritten `.out.json` carries a note.
  - No repo file holds the counter or the value; the wide and git-history membership checks were run after this and found 0 hits.
  - Transcript copies are outside repo scope, the same class as the worker's open issue 3.
- I did not inspect B300 `/scratch/iitp4/fu_c` for copies of the test file (explorer_FU_C_r2_2 reports none; it is not repo content). No GPU used, no ledger rows, no git writes, no production file touched.
- The c4scan SCOPES cover `verification/worker_FU_C_r*` only. Even within scope, a literal-shape scanner cannot detect a recoverable near-copy, so this residual class has no automated guard.

## 4. Conclusion
- **Blocking (C4):** `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` plus the old pin on code receipt line 13 let the real HCP-YA ID be recovered from repo content.
  - Remedy, by root or the owner: seal off-repo, then remove `verification/explorer_FU_C_r2_2/tree/`, `mut_work/` and `code_receipt_subset_derived.view`.
  - Then rerun the near-copy sweep below and expect 0 recoverable files.
  - No worker code change and no re-verification of the science are needed. With that removal confirmed, I would APPROVE.
- **Nonblocking:**
  - Extend the C4 tripwire scope to all `verification/*FU_C*` dirs, or add a near-copy/recoverability guard.
  - Result report §3 test and mutant counts are r1 numbers (declared in the banner).
  - The §1 headings are all numbered "### 1." (declared cosmetic).
  - The ledger total including verifier probes is 10.697 GPU-h.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 timeout 900 nice /home/juke/superclaude-env/bin/python3 -I verification/reviewer_FU_C_r2_2/probes/nearcopy_sweep.py $PWD /tmp/sweep.json   # expect near_copies == [] after remediation
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/v.json   # byte-identical
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_check_receipts_r2.py   # ok true
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. timeout 900 nice /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q   # 180 passed
```
Invalidation: any change to verdict.py, receipts.py, the card or the run records; a new near-copy anywhere in the repo.
