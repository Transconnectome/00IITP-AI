# Hard handoff — auditor_FU_C_r2_1 (forensic integrity audit, milestone FU_C, iteration 2)

Written 2026-11-01T21:25Z. Host claude-code (Opus 5.5), no nested spawning. Integrity mode: Development (ORIGINAL_REQUEST.md has no "from scratch" / "must not delegate" constraint). Profile: General Project.

## Forensic Audit Report

**Work Product**: FU-C iteration 2 (worker_FU_C_r2 C4 remediation), plus the FU-C r2 working-tree artifacts under verification/.
**Verdict**: INTEGRITY VIOLATION. It is narrow, and the worker's own deliverables are not its source.
- The violation is one C4 item. A real HCP-YA participant ID can still be recovered from repo working-tree content, through a peer explorer's near-copy plus the in-repo pre-result pin.
- worker_FU_C_r2 flagged this itself as GATE-RELEVANT. It is outside the worker's ownership and is still present.
- Every check on the worker's own product passes.

### Phase Results
- **C1 protected hashes: PASS.** rc 0 at the start and at the end.
- **FU-C receipts: PASS (declared supersession only).**
  - These verify completely: card 36/0, presentation 1/0, output_sha256_r2 27/0, c4_sealed_originals 1/0.
  - The code receipt fails exactly on lines 13 (MISSING, the retired test) and 16 (CHANGED, the repaired test).
  - The output receipt fails exactly on lines 141 (report), 162 (MISSING) and 164.
  - Both sets equal `supersession.SUPERSEDED` and addendum 02 §3. No receipt bytes were changed; only modes (a-w) were.
- **Verdict reproduction: PASS.**
  - `scripts/topic2fu_c_verdict_r2.py --out` gives rc 0, `stop`, no context problems, and output byte-identical to the shipped verdict.json (sha 4d7931025c4f…80f5).
  - The frozen CLI gives `no_verdict`, with exactly the 2 superseded test-pin problems.
  - The derived view only drops `tests`-section pins. `build_context` uses pins for verification only, so dropping them cannot change the computation.
  - verdict.py, logs.py, receipts.py, design.py, the CLI and the card are byte-equal to their pins. No verdict-path file imports supersession.py or c4scan.py.
- **Hardcoding / facades: PASS.**
  - supersession.py, check_receipts_r2 and verdict_r2 compute everything from the files.
  - The repaired test is stricter than before: it now asserts the exact two-item problem list. It was not weakened.
- **Addendum 02 numbers: PASS.** I recomputed them independently with scipy from verdict.json:
  - I1 −0.1132 % [−0.4985 %, +0.2721 %];
  - without seed 16: sd 0.2205 %, half-width 0.2039 %;
  - r1 sd 0.1728 %;
  - E mean NMSE 0.98842, learned signal 0.01158, δ_abs 0.00988 (85.4 %), upper-bound share 23.2 %.
- **Result report edit: PASS.**
  - The diff against prev_snapshot contains only the r2 banner, the §4 bullet and the §6 reproduce block.
  - The prev_snapshot sha equals pin line 141.
- **Tests: PASS.** tests/topic2_fu_c 180, old suite 86, topic2_rgpool 116, topic1_lagmotif 88.
- **Mutation union harness: PASS.** I reran a byte-identical copy (sha 3e8652c2…) of the worker's harness:
  - 150 entries, 146 killed, 0 invalid; 5 tests deselected (count checked);
  - survivors baseline, V07c, V12, F11, the equivalents accepted in r1;
  - 0 status disagreements with the worker's table;
  - all 52 r1-verifier survivors (C1 20, C2 19, R2 13), extracted by me from their out files, are KILLED.
- **Compute: PASS.**
  - B300 sacct since 04:30 KST shows no FU-C job after 577 (r1 challenger, 20:03Z). The worker r2 window started at 20:32Z.
  - There are no new ledger rows for r2, and no new files under /scratch/iitp4/fu_c since 20:15Z.
  - The membership probe sends tokens over ssh stdin and reads back counts only; nothing is written on B300.
- **Git writes by agents: PASS.**
  - Commits since 20:00Z are all by Chavis Autocommit.
  - There are 0 stashes, and no FU-C path is tracked.
- **Layout: PASS.** Whole-run `audit_layout.py` gives rc 0 with 0 findings.
- **Sealed store: PASS.** The 0700/0400 modes are in place, the sha equals the old pin, and no copy is in the repo.
- **C4, literal in repo bytes: PASS.**
  - Count-only scan of 26,683 working-tree files (binaries included), gz/zip members, and all 3,913 git objects (`cat-file --batch-all-objects`).
  - The literal appears in 0 FU-C files and 0 git objects.
  - The one tree hit is a coincidental float in `results/topic1/2026-10-31/extract_primary.jsonl` (masked context `######.###`), not an ID.
  - 0 digest hits (sha256/sha1/md5/blake2b/sha512 of the literal and variants).
  - The AST constant fold over 37 FU-C and worker .py files found 0 expressions that evaluate to the literal.
  - Controls: positive true, negative false.
- **C4, recoverability: FAIL.** Details below.

### C4 finding (the violation)
- **The near-copy.** `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` (sha 7b915eb7…78a4, mtime 2026-11-01T20:16:50Z) has the same length as the sealed original (12,889 bytes). It differs in only 3 bytes, all inside the literal's 6-byte span.
- **The pin.** The old file sha 3af2eb8c…be81c is in repo files: `results/topic2/2026-11-02_fu_c/code_sha256_before_results.txt` l.13, `output_sha256.txt` l.162 and `c4_sealed_originals_sha256.txt`. It is also in copied receipts in explorer_FU_C_r2_2/tree and challenger_FU_C_r2_2/tree.
- **Recovery.** `probes/nearcopy_recover.py` brute-forces 10^6 candidates at the literal's offset. It returned `recoverable_from_candidate_plus_repo_pin: true, recovered_equals_literal: true` in seconds, using repo content only. Nothing was printed.
- **Rule broken.** The dispatch counts "participant-ID leakage (incl. recoverable hashes)". C4 says no participant IDs written, and allows only a positional index or a salted hash.
- **Scope.**
  - The near-copy is untracked, is not gitignored, is not in git history, and is not the worker's file.
  - No other copy exists: a re-scan of verification/ at 21:13Z found 1 named or equal-length copy, and it is this one.
- **Severity: low.** The ID is HCP's publicly documented example subject, and it is not linked to any record.
- **Remedy (root or owner).** Remove `verification/explorer_FU_C_r2_2/tree/`, or at least that one file. Then rerun `probes/rescan_verification.py`, expecting `named_copies: []`. No change to FU-C code, results or receipts is needed.

## 1. Observation
Commands and raw outputs are in `/home/juke/git/00IITP-AI/verification/auditor_FU_C_r2_1/`:

| file | content |
|---|---|
| `probes/literal_footprint.out.json` | full-tree and git scan |
| `probes/nearcopy_recover.out.json` | recovery proof |
| `probes/rescan_verification.out.json` | re-scan of verification/ |
| `probes/ast_fold_literal.out.json` | AST constant fold |
| `verdict_r2_auditor.json/.out`, `frozen_cli_auditor.json/.out` | verdict reproductions |
| `pytest_*.out` | test runs |
| `mutants/mutants_auditor.out.json/.log`, `mutants/r1_survivors.json` | mutation rerun and r1 survivor lists |
| `sacct_since_r1.txt` | B300 sacct |
| `audit_layout.out` | layout lint |

No file of mine contains the literal (self-scan: 0).

## 2. Logic Chain
1. The receipts fail only on declared lines, and the verdict path is byte-pinned. The verdict is reproduced byte-identically, and the addendum numbers reproduce independently. So the remediation did not alter science or results, and there is no fabrication or hardcoding.
2. The mutation rerun matches the worker exactly and kills every r1 survivor. So the new tests are not tests that cannot fail.
3. There was no GPU, B300 write, ledger change or agent git write in r2. So compute and git are clean.
4. The literal is absent from all repo bytes and git objects. But an equal-length near-copy plus the in-repo old pin recovers it in seconds (demonstrated). That is recoverable participant-ID leakage under C4 and the dispatch. One failure means INTEGRITY VIOLATION, scoped to that artifact.

## 3. Caveats
- The /tmp search for other copies timed out at 120 s. Copies outside the repo (and agent transcripts) are out of repo scope.
- Concurrent r2 verifiers may create new copies after 21:13Z. Re-scan before the gate.
- **Out-of-scope leads, not FU-C:** some non-FU-C receipts fail. None of the failing targets changed after 20:15Z, so none is attributable to iteration 2. The ones to check:
  - `results/topic2/2026-11-02_fu_b/card_sha256.txt` has 1 CHANGED line: the FU-B card differs from its pin. FU-B's auditor should check this.
  - The others are cwd/format differences or earlier declared C4 supersessions (topic2 r1, topic3, topic4, topic1).
- I did not re-verify the r1-audited science (records vs B300, ledger vs sacct for r1 jobs). The output-receipt pins for all 24 records still verify, so the records are unchanged since that audit.

## 4. Conclusion
- worker_FU_C_r2's deliverables are clean.
- The milestone is not CLEAN while `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` exists. Remove it and re-scan; the only remaining finding then closes.
- The verdict `stop` (I1 −0.113 % [−0.499 %, +0.272 %], df 7, δ 1 %) is unaffected.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
python3 -B scripts/topic2fu_c_check_receipts_r2.py
python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json
python3 -I verification/auditor_FU_C_r2_1/probes/rescan_verification.py ~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/test_gate_and_records.py verification
```
- The last command must show `named_copies: []` and `literal_hits: []`. That rescan brute-forces any equal-length copy.
- Invalidation: any new equal-length or near copy of the retired file anywhere in the repo, or the literal appearing in any file.
