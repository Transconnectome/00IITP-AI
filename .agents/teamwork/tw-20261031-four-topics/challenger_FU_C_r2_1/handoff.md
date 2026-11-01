# Handoff — challenger_FU_C_r2_1 (FU-C iteration 2; Hard handoff)

Written 2026-11-01T21:35Z. Parent: root coordinator (session 5fddb83e). Verdict: **REFUTED** on one item: the repo still lets the retired HCP-YA ID be recovered. The worker cannot fix it; root can, by removing a peer directory. Every other claim is CONFIRMED by independent evidence.

Housekeeping: GPU-h used 0, no ledger rows, no git writes, no production file touched. All probes are in `verification/challenger_FU_C_r2_1/`.

## Challenge summary

**Overall risk: MEDIUM.**
- The science and the verdict are robust.
- The C4 class that failed r1 is not yet closed at repo level.
- The new r2 tooling has untested logic (nonblocking).

## 1. Observation

### C1 and receipts
- `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` returned rc 0, at start and at end.
- Raw `sha256sum -c` per FU-C receipt:
  - `card_sha256.txt`: 36 lines, 0 failing.
  - `code_sha256_before_results.txt`: fails on `test_gate_and_records.py` (missing, line 13) and `test_perms_receipts_c4.py` (line 16).
  - `code_sha256_presentation_before_results.txt`: 1 line, 0 failing.
  - `output_sha256.txt`: fails on the result report (141), the retired test (162) and the repaired test (164).
  - `output_sha256_r2.txt`: 27 lines, all OK.
- `scripts/topic2fu_c_check_receipts_r2.py` gives the same failing set, and ok is true (`check_receipts_r2.out.json`).

### Suites
Logs are in `logs/`.

| suite | result |
|---|---|
| `tests/topic2_fu_c` | 180 passed |
| old 86 (STRICT_E2E) | 86 passed |
| `tests/topic2_rgpool` | 116 passed |
| `tests/topic1_lagmotif` | 88 passed |

`audit_layout.py` over the whole run root: rc 0, 610 files, 0 findings.

### Independent verdict recomputation
`recompute_verdict.py` does not import `src/topic2_fu_c` or `topic2_rgpool`; its output is `recompute_verdict.out.json`.
- Provenance checks over all 24 records found 0 problems:
  - every perm sha matches the card §3.3 table;
  - the perm-file and split shas match;
  - code shas equal the r1 freeze pins;
  - tokens are `^h\d{2}$` and in the split's test order;
  - test_nmse equals Σnum/Σden;
  - every `start_utc`, parsed as a datetime, is later than both freeze times.
- I1 = −0.1132 %, sd 0.4609 %, t(7) 2.3646, interval [−0.4985 %, +0.2721 %]. I2 = +0.0083 % [−0.5200 %, +0.5366 %].
- Result: `stop`, qualifier "sign unresolved".
- The F+ gate passes (+3.061 % / +2.935 %) and the F− gate passes (−1.737 %).
- Stalled seeds are {15, 16}. The sensitivity analysis gives `stop` with I1 [−0.2126 %, +0.2925 %], and the pooled 13-seed I1 is [−0.2482 %, +0.2218 %].
- Every number differs from `verdict.json` by 0, or by 4e-19 for one sensitivity bound.
- The addendum 02 numbers reproduce:
  - E seed-mean is 0.98842;
  - δ is 85.37 % of the learned signal, and the I1 upper bound 23.23 %;
  - without seed 16, the sd is 0.2205 % and the half-width 0.2039 %;
  - the r1 sd is 0.1728 %.

### Freeze order
| event | time (UTC) | evidence |
|---|---|---|
| card mtime | 16:13:03 | file timestamp |
| card receipt | 16:13:23 | `frozen_utc` |
| code receipt | 16:31:53 | `frozen_utc`; `verdict.py` mtime 16:31:25 |
| first Stage-1 start | 16:35:12 | run.json |
| earliest Stage-1 end | 17:01 | run.json |
| `verdict.json` written | 19:39:53 | file timestamp |

So no Stage-1 result existed before the verdict code was pinned. The card and receipts are untracked in git, so file timestamps and receipts are the only time evidence.

### Reproduction
- `scripts/topic2fu_c_verdict_r2.py --out …/verdict_r2_repro.json`: rc 0, byte-identical to the shipped file, sha 4d7931025c4f… on both sides.
- The frozen CLI with `--out …/frozen_cli_now.json` gives `no_verdict`, with exactly the 2 declared problems.

### Mutation testing
- The worker's union harness, rerun by me (`union_rerun/`): 150 entries, 146 killed, 0 invalid. Survivors are the baseline, V07c, V12 and F11.
- All 52 mutants that survived in the r1 verifiers' harnesses are now KILLED: 20 from challenger_1, 19 from challenger_2 and 13 from reviewer_2.

### C4 (count-only; no ID ever printed, written or held on this host)
- **Literal recoverable (`probe_nearcopy_recoverability.out.json`).**
  - `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` still exists. It is 12,889 bytes with exactly one `000000` placeholder.
  - Substituting each of the 10^6 six-digit values and hashing gives **1 match** to the pre-result pin 3af2eb8c… in 6.4 s.
  - So the retired real HCP-YA ID is recoverable from current repo working-tree content.
  - It is the only near-copy: a repo-wide grep for a distinctive test name finds only this file.
- **No other ID in FU-C material (`probe_b300_membership_broad.out.json`).**
  - Input: 599 unique maximal 6-digit runs from 1,781 files plus 5.7 MB of git-history patches since 10-31.
  - Scope: FU-C src, tests, scripts, docs and results, every `verification/*FU_C*` dir, and the whole run metadata dir.
  - Against the 1,084 staged B300 names: **0 hits**. Controls are valid: negative 0, and positive 1, using a B300-side name, so no ID reached this host.
  - The 63,413 six-digit windows inside longer digit runs gave 68 hits against 68.7 expected by chance.
- **Run-time test values.** The values the r2 tests build at run time (`999999`, `411111`) are 0 of the 1,084 staged names.
- **Sealed copy.** `c4_sealed_originals_sha256.txt` verifies OK; the file is mode 0400 and its directory 0700.

### Own mutants on the r2-added surfaces
`mutants_r2_surfaces.py` covers `supersession.py`, `c4scan.py`, the r2 driver and the r2 checker: 28 mutants, 0 invalid.
- In behaviour-only mode (the 5 hash tests deselected), **15 survive**.
- In full-suite mode all 28 are killed, but 14 of those 15 are killed only by the `output_sha256_r2.txt` hash pin. The exception is SS07, which the byte-identity test also kills.
- Survivors:
  - **check_receipts logic:** SS02 MISSING→OK; SS03 `failing_equals_declared` always True; SS04 receipts without a declaration skipped; SS05 r2 receipt treated as off-repo; SS12 missing-declared-receipt ignored; CK01 checker exit always 0.
  - **Driver:** DR01 refusal to overwrite verdict.json removed; DR02 byte-identical claim always True.
  - **c4scan:** C401 and C402 drop scope entries (`verification/worker_FU_C_r*`, `scripts/topic2fu_c_*.py`); C404 SUB weakened to `sub-[0-9]`; C405 hex-mask threshold 6; C409 the `.` lookbehind removed; **C413 SIX `[1-9]`→`[2-9]`, which would miss every 6-digit ID starting with 1**.

## 2. Logic chain

1. **The science holds.** The verdict follows the card: hi 0.00272 < δ 0.01 gives `stop`, and lo < 0 < hi gives the "sign unresolved" qualifier. F+ passes, so card §5 item 3 does not apply. My recomputation does not share code with the pipeline and agrees to 0 difference.
2. **The verdict comes from pinned pre-result code.** The derived view keeps every verdict_code, result_handling and frozen_utc line. The unchanged code reproduces `verdict.json` byte for byte. The verdict-path shas are unchanged.
3. **Supersession is exact.** Exactly 5 declared lines fail, and every other line verifies. I checked this with raw `sha256sum -c`, not only with the worker's checker.
4. **C4 inside FU-C paths is clean.** There is 0 membership in a scope much broader than the worker's, including git history.
5. **C4 at repo level is not closed.** The pinned hash is in pre-result receipts, which cannot be edited, and in committed handoffs. Together with the peer near-copy, which differs only at the placeholder, it recovers the ID in seconds (observed: 1 match). This is the defect class that failed r1, and the same class as M3's dev-salt failure, where the peer-dir leak was treated as blocking until root contained it. The worker disclosed it as open issue 1 but could not act on it: it is outside the worker's ownership.
6. **The r2 tooling gaps are nonblocking.** The check_receipts, driver and c4scan logic is guarded only incidentally, by the hash pin of the file itself. A later edit that also re-pins the r2 receipt would pass silently. The facts these tools assert are independently verified here, so no result is affected. C413 shows that the tripwire's positive controls (`999999`-style) never exercise the leading digit 1.

## 3. Caveats

- Membership was checked against the 1,084 staged names only, not the full HCP-YA cohort.
- I did not read the sealed file. Recoverability was shown as a match count only, and the loop value was discarded.
- I did not rerun any GPU job or re-evaluate checkpoints. One r1 challenger did so (job 577).
- I took the r1 gate records as pinned and did not retrain them.
- File mtimes can be forged. No git anchor exists for the card, which is untracked.
- I did not inspect FU-A's 6-digit fixtures (out of scope; explorer_FU_C_r2_2 says 0 of 3 are staged).
- The empty dir `verification/challenger_FU_C_r2_1/union_rerun/work` and `surf_work` remain (mirrors were removed). There are no orphan processes.

## 4. Conclusion

**REFUTED**, on one blocking item.
- **What fails.** The retired literal is recoverable from repo working-tree content via `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` plus the pinned sha.
- **How to close it.**
  - The fix belongs to the owner of that directory, or to root. Seal or remove `verification/explorer_FU_C_r2_2/tree/` (also `mut_work/` and `code_receipt_subset_derived.view`).
  - No worker code change is needed.
  - Then rerun `probe_nearcopy_recoverability.py`. The expected result is no candidates.
- **What is confirmed.** All other claims hold:
  - verdict `stop`, I1 −0.113 % [−0.499 %, +0.272 %], df 7;
  - byte-identical reproduction;
  - 5 declared receipt failures and nothing else;
  - 146 of 149 mutants killed, and all 52 r1 survivors killed;
  - suites green, C1 rc 0, ledger FU-C 10.697 GPU-h ≤ 13.

Nonblocking items:
1. Add behavioural tests for `check_receipts` on a synthetic root, for the driver refusal and identity, and for the c4scan scope entries.
2. Add a leading-1 positive control and a letter-led `sub-` control.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI; V=verification/challenger_FU_C_r2_1
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
/home/juke/superclaude-env/bin/python3 -I $V/recompute_verdict.py $PWD /tmp/rv.json
/home/juke/superclaude-env/bin/python3 -I $V/probe_nearcopy_recoverability.py $PWD /tmp/nc.json   # matches must be 0 / no candidates after containment
/home/juke/superclaude-env/bin/python3 -I $V/probe_b300_membership_broad.py $PWD /tmp/mb.json      # controls_valid true, cat1_member_hits 0
/home/juke/superclaude-env/bin/python3 -B $V/mutants_r2_surfaces.py $PWD $V/surf_work /tmp/ms.json
```

Invalidation conditions:
- a recoverability match after containment;
- a cat1 membership hit with valid controls;
- any recomputed number differing from `verdict.json`.
