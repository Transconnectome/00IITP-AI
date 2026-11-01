# Handoff (Hard) — reviewer_FU_C_r3_1, FU_C iteration-3 gate

**Verdict: APPROVE.** Written 2026-11-01T22:55Z. 0 GPU-h, no ledger rows, no git writes, no production file touched,
nothing read from or copied out of the sealed store by me (the C4 check script reads the sealed original in memory
and emits counts only). The r2 gate record is not reproduced here; no literal, digit, offset or shape is written.

## 1. Observation (my own runs; evidence in verification/reviewer_FU_C_r3_1/)
- C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: rc 0 at start (c1_start.log, 67 OK) and at end (c1_end.log).
- Suites: tests/topic2_fu_c 210 passed (fuc_suite.log); old suite STRICT_E2E=1 86 passed (old86.log);
  tests/topic2_rgpool 116 passed with CUDA_VISIBLE_DEVICES='' (rgpool.log); tests/topic1_lagmotif 88 passed. No
  mutation work dir existed under verification/worker_FU_C_r* when the FU-C suite ran.
- scripts/topic2fu_c_check_receipts_r2.py: ok true; card 36/0, code 15/2, presentation 1/0, output 160/3,
  output_sha256_r2 27/0, output_sha256_r3 20/0; failing lines = exactly the r2-declared set (code 13, 16; output
  141, 162, 164). `grep -v '^#' output_sha256_r3.txt | sha256sum -c`: 0 failures.
- verdict_r2 --out: rc 0, context_problems [], byte_identical_to_shipped true, `cmp` identical (4d793102…80f5).
  Frozen CLI --out: rc 0 (no_verdict by design, addendum 02 §4).
- Independent recomputation without importing src/topic2_fu_c (independent_recompute.txt): from the 24 run.json
  test_num/test_den sums, paired by seed, df 7: I1 −0.1132 % [−0.4985 %, +0.2721 %], I2 +0.0083 %
  [−0.5200 %, +0.5366 %]; upper bound < δ = 1 % → stop; qualifier "sign unresolved". All 24 status completed;
  test pseudonym lists identical across arms (16). Matches verdict.json and result report §0.
- Hashes equal the worker's claims: card fc2d0672…, verdict.json 4d793102…, verdict.py 9a1425b6…, receipts.py
  7ee0856a…, c4scan.py 242ead4e…, supersession.py 5c9823d7…, c4scan_strict.py d52c2aec…, test_r3_guards.py
  59b5fb41…, check_c4_r3.py e8f6de08…, write_receipt_r3.py 94ce2671…, addendum_03 84f7a98f…, output_sha256_r3
  5512a190…, run_mutants_r3.py 1a65dbf8…, mutants_r3.out.json 72df86b6….
- C4 re-run by me: `scripts/topic2fu_c_check_c4_r3.py --b300` → c4_check_r3_reviewer.out.json, ok true. Working tree
  26,325 files (3 >50 MB skipped), git blobs 2,199: identifier-context 0, near-copies 0, named copies 0, offset
  statements 0, digest hits 0; sealed original matches its pin; retired path absent. B300 count-only membership
  (CPU, no Slurm/GPU): production 217 files/128 runs, verification 409/113, metadata 103/8 → 0 member hits each;
  controls pos 1, neg 0 over 1,084 staged names (valid). I read the script first: output is booleans/counts only.
- Freeze order: git commit e5fa8de (2026-11-01T16:20:26Z) holds the worker_FU_C_r1 "16:13:23Z CARD FROZEN … fc2d0672…"
  line; cd1e43e (16:35:27Z) holds "16:31:53Z verdict code + tests pinned … No Stage-1 job had started". run.json:
  first start 16:35:12Z, first end 17:01:06Z, last end 19:33:54Z. Card receipt frozen_utc 16:13:23Z.
- GPU ledger: FU-C completed rows sum 10.697 GPU-h (worker 10.422, verifiers 0.275) ≤ cap 13; run total 40.6 ≤ 95;
  0 rows by any FU_C r3 agent. worker_FU_C_r1 progress records the squeue g3t-G-E0-* check before each submission.
- Worker harness: mutants_r3.out.json summary 222 entries, 217 killed, 0 invalid, 5 deselected, baseline 205;
  survivors baseline, W:V07c, W:V12, W:F11, CR2:C10; all 26 named r2-challenger mutants (CR1 15, CR2 11) KILLED.
  Run 1 vs run 2 differ only in R3:R05 (SURVIVED→KILLED), consistent with the disclosed single test fix; mtimes
  (run1 07:15:16, test fix 07:15:47, run2 07:24:42 KST) consistent. Harness edits copies; collection errors are
  INVALID, not kills.
- My own 13 mutants (mut/run_reviewer_mutants.py, mut/reviewer_mutants.out.json; same mirror/deselect method):
  baseline 205 passed; KILLED RV03 (no sha1 mask), RV08, RV10, RV12, RV16; SURVIVED RV01 (strict: no right
  extension of the enclosing hex run), RV02 (no sha512 mask), RV05 (check: md5 dropped), RV06 (check: sha256 dropped),
  RV07 (recoverability space upper bound cut), RV13 (main() ok ignores git-blob near-copies), RV14 (B300 controls
  always valid), RV17 (strict allowlist by value).
- flake8 --max-line-length 120 on the 4 new .py: clean. audit_layout.py on the run root: 0 findings, rc 0.

## 2. Logic chain
1. The r2 gate's only blocker (peer near-copy + unchanged pin → recoverable literal) was outside the worker; root
   sealed it. My independent count-only re-run finds every exposure class at 0 in tree and history and 0 B300
   membership hits with valid controls → C4 closed in repo content for the known classes.
2. r3 changes are new files only; every earlier receipt verifies except the r2-declared 5 lines; the new receipt
   verifies 20/20 → no regression of pins; C1 rc 0.
3. Verdict path untouched (hashes) and the shipped verdict is reproduced byte-for-byte and by my own independent
   computation → the scientific result `stop` stands.
4. F1 (card before results) holds via receipts plus an independent git anchor; F3 compute within cap via Slurm,
   ledgered; C8 report sources only verdict.json.
5. My surviving mutants all sit in post-result, non-governing C4 evidence tools. The C4 conclusion rests on running
   the unmutated code, which I read (it does compute sha256, sha1 and md5 digests and full/16-char prefixes) and
   re-ran; so the survivors are test-coverage gaps, not wrong results → nonblocking.

## 3. Caveats
- C7 (external repos read-only) and the r1/r2 science were not re-audited beyond the verdict recomputation; earlier
  gates covered them. No GPU re-evaluation of checkpoints was done (not needed; r2 challenger did one).
- The C4 near-copy test is line-overlap based; reformatted/encoded copies would escape (worker disclosed). B300
  membership is against 1,084 staged names only.
- Residual pending PI (GATE_STATUS): committed r1/r2 FU_C handoffs describe the literal in words; outside r3 scope.

## 4. Conclusion
APPROVE. Every C1–C8 and F1–F3 item for FU_C is met with evidence I reproduced; the r2 blocker is closed; verdict
`stop` (I1 −0.113 % [−0.499 %, +0.272 %], df 7, δ 1 %) reproduced byte-identically and independently.
Nonblocking: (a) 8 of my 13 independent mutants survive in the r3 C4 evidence tools (RV05/RV06 digest-type coverage
is the most relevant: only a sha1 prefix is exercised); the worker's "4 survivors, all equivalent" is relative to its
own tables; (b) supersession.check_receipts compares the failing line set, not MISSING vs CHANGED status (a
re-created retired file with other content would pass it; check_c4_r3's retired_path_absent covers this);
(c) the worker's "about 17 minutes per run" for the harness does not match file times (~6–9 min); presentation only,
not in repo docs; (d) the PI-pending committed-handoff residual.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_verdict_r2.py --out <tmp>.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q   # 210
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/topic2fu_c_check_c4_r3.py --out <tmp>.json --b300   # ok true
python3 -B verification/reviewer_FU_C_r3_1/mut/run_reviewer_mutants.py $PWD <work dir outside worker_FU_C_r*> <out>.json
```
Invalidation: any r2/r3-pinned file changing; byte_identical false; any non-zero C4 count; a mutation work dir
under verification/worker_FU_C_r* while the FU-C suite runs.
