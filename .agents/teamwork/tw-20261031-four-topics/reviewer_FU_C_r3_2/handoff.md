# Handoff (hard) — reviewer_FU_C_r3_2, milestone FU_C iteration 3

## Review Summary
**Verdict: APPROVE.** I found no blocking issue and no sign of an integrity violation. GPU use was 0 GPU-h. I made no git writes and did not edit any production file.

## 1. Observation
All probe outputs are in /home/juke/git/00IITP-AI/verification/reviewer_FU_C_r3_2/.
- C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: rc 0 at 22:36Z and at 22:44Z, 67/67 OK (c1_check.log, c1_check_final.log).
- All 14 sha256 values the worker claimed for frozen artifacts verify OK (claimed_sha.txt). This covers card fc2d0672…, verdict.json 4d793102…, verdict.py, receipts.py, c4scan.py, supersession.py, output_sha256_r3.txt, addendum_03, c4scan_strict.py, test_r3_guards.py, check_c4_r3.py, write_receipt_r3.py, run_mutants_r3.py and mutants_r3.out.json.
- `scripts/topic2fu_c_check_receipts_r2.py`: rc 0, ok true. Per receipt (lines/failing):
  - card 36/0, presentation 1/0, output_sha256_r2 27/0, output_sha256_r3 20/0;
  - code receipt 15/2: line 13 MISSING, line 16 CHANGED;
  - output receipt 160/3: lines 141, 162 and 164;
  - every receipt has failing_equals_declared true. The r3 receipt verifies directly too: 20 lines, 0 failures (check_receipts.out).
- Suites:
  - tests/topic2_fu_c: 210 passed (fuc_suite.log);
  - old suite (STRICT_E2E=1): 86 passed (old86.log);
  - tests/topic2_rgpool with CUDA_VISIBLE_DEVICES='': 116 passed (rgpool.log);
  - tests/topic1_lagmotif: 88 passed (lagmotif.log).
- `scripts/topic2fu_c_verdict_r2.py --out <mine>`: rc 0, context_problems []. `cmp` against the shipped verdict.json is IDENTICAL.
- `scripts/topic2fu_c_verdict.py --out <mine>`: no_verdict, with exactly 2 problems: retired test pin missing and changed test pin. This is by design per addendum 02 §4.
- Independent recompute from the 24 run.json files (probes/recompute_i1.py):
  - I1 = −0.1132 % [−0.4985 %, +0.2721 %], df 7, so stop. lo > 0 is false and hi < 0 is false, which gives the qualifier "sign unresolved".
  - I2 = +0.0083 % [−0.5200 %, +0.5366 %].
  - Stalled runs: (C,16) and (S,15). The stall-drop sensitivity over seeds 10–14 and 17 at df 5 gives I1 +0.040 % [−0.213, +0.293] and I2 +0.022 % [−0.091, +0.135]. This matches the result report.
  - Provenance problems 0: perm key/sha against the card table, perm file sha f9e32ab7…, split sha cc521b08…, test order, settings, Σnum/Σden. Every start_utc is after the card freeze (16:13:23Z). All 13 code_sha256 entries equal the r1 freeze pins.
- GPU ledger: FU-C closing rows total 10.697 GPU-h, which is ≤ 13. There are no r3 rows. Of this, worker_FU_C_r1 used 10.422, the explorers 0.262 and challenger_FU_C_r1_1 0.013.
- I reran the worker's C4 script `scripts/topic2fu_c_check_c4_r3.py --out <mine> --b300`: rc 0, ok true (probes/c4_check_rerun.out.json).
  - Sealed copy matches its pin; retired path is absent.
  - Working tree: 26,324 items. Git blobs: 2,199. Identifier, near-copy, named-copy, offset and digest counts are all 0.
  - B300 membership: production 217 files, verification 409, metadata 103, with 0 hits in each. Controls were 1/0 and valid.
- My extended count-only C4 probe (probes/c4_extended.py → c4_extended.out.json): ok true.
  - Git: 2,206 blobs in the object DB, of which 7 are not reachable from refs. Those 7 had 0 identifier, 0 near-copy and 0 digest-prefix hits.
  - Working tree: 26,335 files, 0 files holding an 8-or-more-character hex prefix of a sha256/sha1/md5/blake2b/sha512 digest of the literal or its variants or lines.
  - Archives: 338 opened, 8,728 members, 0 identifier hits and 0 near-copies.
- My git-history membership probe (probes/history_membership.py): 133 historical blob versions of FU-C paths across all refs and the reflog hold 9 unique maximal 6-digit runs. B300 member hits: 0. Controls: positive 1, negative 0.
- The git freeze anchor in addendum 03 §9 checks out:
  - e5fa8de (2026-11-01T16:20:26Z) adds the "16:13:23Z CARD FROZEN … fc2d0672…" line;
  - cd1e43e (16:35:27Z) adds the "16:31:53Z verdict code + tests pinned … No Stage-1 job had started" line.
- Additivity:
  - Every FU-C file changed after the r3 dispatch (21:55Z) is new in r3: c4scan_strict.py, test_r3_guards.py, check_c4_r3.py, write_receipt_r3.py, addendum_03 and output_sha256_r3.txt.
  - addendum_02 and output_sha256_r2.txt were last modified at 21:00Z, before r3.
  - Git commits since 21:50Z are only `docs(auto)` daemon snapshots. There are 0 stashes.
- Mutation evidence (mutants_r3.out.json summary): 222 entries, 217 killed, 0 invalid, 5 deselected, baseline 205 passed. The survivors are the baseline, W:V07c, W:V12, W:F11 and CR2:C10.
- audit_layout.py on the whole run metadata root: rc 0, 680 files, findings [].

## 2. Logic Chain
1. C1 and every earlier receipt are unchanged (Obs C1, receipts). The only failing receipt lines are the 5 already declared in r2. So r3 broke no pin and edited no frozen card. This meets C1, C3 and the "frozen cards never edited" rule.
2. The verdict reproduces byte for byte, and my own recompute from raw run files agrees on I1, I2, the qualifier and the sensitivity. So F3 holds: the verdict follows card §5 and is stated with its §11 reading. The shipped science did not change in r3.
3. C2 holds: all suites pass, and the new tests are behaviour tests on synthetic tmp roots. I read lines 52–440, and the controls are built at run time with no hardcoded pass values. Mutation evidence shows they kill the 26 r2-challenger survivors. CR2:C10 is equivalent: an all-digit run of 8 or more characters cannot contain a 6-digit run bounded by non-digits, so SIX is unaffected, and HEX16 reads unmasked text.
4. C4 was the r2 blocking class. Containment is confirmed three ways: the worker's own check rerun by me, my extended probe and my git-history membership probe. The extended and history probes close coverage gaps in the worker's script: unreachable objects, short digest prefixes, archives, and membership of historical FU-C blobs. With all counts 0, I found no repo content that lets the literal be recovered.
5. C5: r3 used 0 GPU-h, and the FU-C total of 10.697 is under the 13 cap. C6, C7 and C8 show no change in r3. The result report cites only verdict.json.
6. So every criterion in scope is met with evidence, and the verdict is APPROVE.

## 3. Caveats
- B300 membership checks only against the 1,084 staged names. Matching nothing there does not prove a token is not an HCP ID. The worker discloses this too.
- Near-copy detection compares long lines. A reformatted or encoded copy (base64, other compression) would escape it. Three working-tree files over 50 MB, none of them FU-C files, were not content-scanned.
- I did not rerun the mutation harness. A peer challenger (challenger_FU_C_r3_2) is running independent mutants. I checked the harness output, the test bodies and the C10 equivalence argument.
- The committed r1/r2 FU-C handoffs that describe the literal in words are pending a PI decision in GATE_STATUS, owned by root. Because of the containment rule I did not assess whether they narrow the value.
- My DISPATCH.md summarises the worker's embedded JSON blob instead of copying it, as a containment precaution.

## 4. Conclusion
APPROVE for FU_C iteration 3. None of the issues below blocks the gate:
1. Documentation: addendum 03 §3 says the final rerun numbers are in §8, but §8 defers them to the worker handoff. The §3 table shows the pre-run counts (23,434 files / 2,174 blobs), while the final run had 27,031 / 2,189.
2. The worker's C4 script has coverage gaps:
   - `rev-list --all` skips unreachable objects;
   - the digest check covers only full digests and 16-character prefixes, although 8–15 character prefixes of sha(literal) would also act as an oracle;
   - it does not decompress archives;
   - B300 membership covers only the current working tree, not the git history of FU-C paths.
   My probes found 0 in each case. The fix is to fold these checks into the script in a future iteration if one happens.
3. The B300 network part of the check script is not unit-tested (worker disclosed).
4. The PI decision on the committed handoff descriptions is still open, owned by root.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json && cmp /tmp/x.json results/topic2/2026-11-02_fu_c/verdict.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
python3 -B verification/reviewer_FU_C_r3_2/probes/recompute_i1.py
python3 -B verification/reviewer_FU_C_r3_2/probes/c4_extended.py
python3 -B verification/reviewer_FU_C_r3_2/probes/history_membership.py
```
This approval becomes invalid if any of these happens:
- a pinned file changes;
- a near-copy or recoverable file appears in the repo or its git objects;
- the receipt failing set changes;
- verdict_r2 output stops being byte-identical.
