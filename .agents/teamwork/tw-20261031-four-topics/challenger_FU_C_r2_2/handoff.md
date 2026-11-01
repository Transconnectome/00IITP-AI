# Handoff — challenger_FU_C_r2_2 (FU-C iteration 2, C4 remediation) — HARD
Written 2026-11-01T21:40Z. Verdict: **REFUTED (narrow: one C4 containment residual outside the worker's paths; root action, no worker change needed)**. Everything the worker claims about its own product reproduces.

## 1. Observation
All probes and outputs are in /home/juke/git/00IITP-AI/verification/challenger_FU_C_r2_2/ (probes/, mutants/, out/). Every identifier check is count-only; no value was printed or written.
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0, at the start and at the end.
- Receipts, my own per-line checker: the failing lines are exactly code 13 and 16, output 141, 162 and 164. card, presentation and output_sha256_r2 verify fully. `scripts/topic2fu_c_check_receipts_r2.py` returns ok true (card 36/0, code 15/2, pres 1/0, output 160/3, r2 27/0).
- Suites: `tests/topic2_fu_c` 180 passed; old suite (STRICT_E2E=1) 86 passed; `tests/topic2_rgpool` 116 passed; `tests/topic1_lagmotif` 88 passed.
- Verdict: `scripts/topic2fu_c_verdict_r2.py --out out/verdict_r2_repro.json` gives rc 0, and `cmp` with the shipped verdict.json is byte-identical (sha 4d793102…).
  - Derived view = original code receipt minus lines 13 and 16, verified exactly (21 → 19 lines).
- Independent recomputation (`probes/recompute_verdict.py`, no src/topic2_fu_c import) from the 24 raw run.json records:
  - I1 = −0.1132 % [−0.4985 %, +0.2721 %], df 7; I2 = +0.0083 % [−0.520 %, +0.537 %].
  - Exactly equal to the shipped values (|diff| < 1e-15). Verdict `stop`, qualifier "gain below delta, sign unresolved".
  - E seed-mean NMSE is 0.9884. δ/learned signal = 85.4 %; I1 upper bound/learned signal = 23.2 %.
- Erratum numbers: dropping C s16 (7 seeds) gives sd 0.2205 % and half-width 0.2039 %; r1 sd is 0.1728 %; the card §12 prediction is 0.144 %. All match addendum 02 §6.2. Stalled runs: C s16 and S s15.
- Freeze order (receipts and mtimes): card frozen 16:13:23Z < code receipt 16:31:53Z < first run start 16:35:12Z (last 19:08:03Z; 24 runs, all Z strings).
- Result report vs prev_snapshot: the snapshot sha equals output_sha256.txt line 141. The diff is limited to the banner, the §4 bullet and the §6 block.
- C4 literal footprint (`probes/c4_literal_footprint.py`; the sealed copy is read in memory and its sha equals pin line 13):
  - Working tree: 1 of 26,194 files contains the literal digits, in results/topic3-style `extract_primary.jsonl`. `probes/hit_context.py` shows this is the integer part of a float value (`"…U": <digits>.##`), a coincidence and not an ID.
  - Git: 0 of 2,098 blobs contain the literal.
- **Near-copy (`probes/near_copy_scan.py`): exactly 1 file in the repo has ≥ 50 % of the retired file's 169 long lines.** It is `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` (99.4 %). With the old pinned sha, a 6-digit brute force recovers the original: `recoverable: true`, checked now. It is still present at 21:35Z. The re-authored file shares 20 of 169 long lines.
- B300 copies: `find /scratch/iitp4 -name 'test_gate_and_records*'` returns 0 (ls-only).
- Wide B300 membership check (`probes/b300_membership_ctx.py`, one ssh call, bits only, CPU):
  - Scope: 864 FU-C-related working-tree files (all *FU_C* agent folders, orchestrator, verification/*FU_C*) plus 355 git blobs on project research/agent paths. 508 unique maximal 6-digit runs.
  - **0 members** of the 1,084 staged HCP names. Controls are valid (positive yes, negatives no).
  - A first attempt (`b300_membership_ctx.INVALID_controls_failed.out.json`) failed its negative control (awk method) and is INVALID, not evidence.
- Mutation:
  - Worker union harness rerun on my copied tree: 150 entries, 146 KILLED, survivors baseline/V07c/V12/F11, 0 INVALID, 5 deselected.
  - V12 is equivalent: verdict.py:286 returns early when fplus_pass is not True. F11 is equivalent: duplicates are caught by `done[0] is not lst[-1]`.
- My mutants of the r2 code (`mutants/run_r2code_mutants*.py`; 25 mutants):
  - Full suite: 25/25 killed. Most kills come from the hash test, because the r2 files are pinned in output_sha256_r2.txt.
  - With only the real-receipt test deselected, 11 survive. In supersession: S01 (subset instead of equality), S02, S03, S08, S11 and S07 (ctx problems cleared in reproduce_verdict). In c4scan: C02, C03, C08 and C10 (equivalent). D01 and D02 cover the driver script.
- Fail-closed scenarios for the unmutated r2 driver, on the copied tree:

| scenario | result |
|---|---|
| verdict.py changed | no_verdict, rc 1 |
| pinned helpers.py changed | no_verdict, rc 1 |
| result_handling script changed | no_verdict, rc 1 |
| frozen stats.py changed | no_verdict, rc 1 |
| retired path re-created | still stop, rc 0 (by design: the pin was dropped) |

- c4scan edge cases (`out/c4scan_edge_cases.txt`; run-time synthetic `"9"*6`) that are NOT flagged:
  - `fe`+ID: 8+ hex chars, so it is masked as a hash;
  - `Ab`+ID+`c`;
  - `run.`+ID+`_3T`: a dot on the left.

## 2. Logic Chain
1. The worker's product claims hold. The receipts, verdict reproduction, independent numbers, errata, suites, mutation counts, hashes and the B300 0-hit check are all reproduced (§1).
2. The worker retired the file because "with the old hash and an in-place-edited copy, the literal is recovered". That condition exists in the repo now: the peer near-copy plus the pin in the receipts makes it recoverable, verified empirically.
3. So the C4 blocking class (no repo content lets an HCP ID be recovered) is not yet closed in the repo. The headline "closes the C4 blocking class" overstates the current state. The worker disclosed this honestly as an open issue for root.
4. The defect is outside worker_FU_C_r2's ownership. It matches the M3 r2 dev-salt case, which a challenger REFUTED and root contained. So the fix is root containment, not a new worker iteration.
5. The rest are test gaps in post-result, non-governing code (§1 survivors, tripwire blind spots). They do not affect the verdict, and the driver fails closed empirically → nonblocking.

## 3. Caveats
- I treat "repo content" as the working tree, including untracked verification/ trees, consistent with the M3 dev-salt precedent. The near-copy `.py` is untracked, and the daemons commit only .md/.txt.
- Git does not independently timestamp the card freeze: the first commit of the card is the daemon snapshot at 19:50Z, after the results. The freeze evidence is receipts + mtimes + run start times, as the r1 verifiers accepted.
- Transcripts and anything outside the repo and B300 /scratch/iitp4 were not scanned. The wide membership check excludes unrelated binary blobs (PDFs, chrome cache) in git.
- GPU: 0 GPU-h used, no ledger rows, no Slurm. B300 was used only for ls/find and the python3 membership call over ssh.

## 4. Conclusion
**REFUTED**, narrowly. The FU-C iteration-2 work product is correct, and verdict `stop` (I1 −0.113 % [−0.499 %, +0.272 %], df 7) is confirmed independently. But C4 is not closed in the repo while `verification/explorer_FU_C_r2_2/tree/` exists, because it allows recovery of a real HCP-YA ID.

Required action (root or the owner): remove, or seal off-repo, `verification/explorer_FU_C_r2_2/{tree,mut_work,code_receipt_subset_derived.view}`. Then rerun `probes/near_copy_scan.py`, which must report 0 near-copies. With that done this becomes CONFIRMED, and no worker change is needed.

Nonblocking (§1): add synthetic tests for check_receipts and for reproduce_verdict fail-closed (S07); test the r2 driver; close the c4scan blind spots ('.'-left; ≥2 hex letters adjacent).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_check_receipts_r2.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json
/home/juke/superclaude-env/bin/python3 -I -B verification/challenger_FU_C_r2_2/probes/recompute_verdict.py $PWD
PIN=$(sed -n 13p results/topic2/2026-11-02_fu_c/code_sha256_before_results.txt | cut -d' ' -f1)
/home/juke/superclaude-env/bin/python3 -I -B verification/challenger_FU_C_r2_2/probes/near_copy_scan.py $PWD ~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/test_gate_and_records.py $PIN   # must list 0 near-copies after containment
```
Invalidation: any change to verdict.json, the receipts, the verdict-path pins, or the runs; any new near-copy; any B300 membership hit.
