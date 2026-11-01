# Handoff (Hard) — explorer_FU_C_r3_1, FU_C iteration 3, lens: scientific design and falsifiability

**Summary (updated 21:46Z).** Root has contained both exposures, and the p1 re-scan gives n_recoverable = 0 (O7). The original summary follows.

**Original summary.** The FU-C science is closed and reproduces: `stop`, byte-identical verdict. The r2 gate failed on one C4 item that the worker could not reach: a peer near-copy of the retired test file. That item is still present at 21:40Z. I also found a second, previously unflagged C4 exposure in a verifier's probe output. Both need root containment. Because r3 is the LAST FU_C iteration (workflow script MAX_ITER = 3), r3 fails exactly as r2 did unless root acts before the r3 verifiers run. No new card, rerun, GPU or verdict-path change is needed.

## 1. Observation
- O1. `orchestrator/workflow_C_script.js.txt` line 10: `const MAX_ITER = 3`. FU_C has startIt 1 (line 62), so r3 is the final iteration. The gate (lines 104–116) needs worker DONE, 2 APPROVE, 2 CONFIRMED and auditor CLEAN. Worker ownership is `fuOwn('c')` (line 48): FU-C paths only, which excludes `verification/explorer_FU_C_r2_2/` and `verification/auditor_FU_C_r2_1/`.
- O2. Probe `verification/explorer_FU_C_r3_1/probes/p1_nearcopy_scan.py`, which works count-only. It loads the sealed original in memory and checks it against code-receipt line 13 (true). Over 20,773 working-tree text files at 21:40:07Z it found exactly one file with ≥30 % of the reference's 135 long lines: `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py`. That file has overlap 0.993, the same length, and differs only inside one 6-digit window. It is `recoverable_with_repo_pin: true`. Output: `probes/p1_nearcopy_scan.out.json`.
- O3. NEW. `verification/auditor_FU_C_r2_1/probes/nearcopy_recover.out.json` has a field listing positional differences. The near-copy's placeholder is all zeros, so this field gives the literal's digit shape: which positions are zero and which are not. Probe `probes/p2_zero_pattern_b300.py` built the shape in memory and sent it only over ssh stdin. It then counted staged HCP names on B300 that match the shape: **4 of 1,084**. Controls: the literal fits the shape (true); positive member 1; negative 0. Output: `probes/p2_zero_pattern_b300.out.json`.
- O4. The same disclosure appears in prose in the auditor's entry of the r2 gate record, which the script embeds verbatim in every r3 FU_C prompt. The COMMON prompt tells each agent to write "DISPATCH.md (this prompt verbatim)". The host and root daemons commit `.agents/**.md`. At 21:42Z, `grep -rl -e "offsets 0" -e <positional-diff field name> .agents` (search simplified here) found 0 files. Neither exposure file has ever been committed (`git log --all` on both paths is empty) or ignored.
- O5. Committed handoffs describe the literal by what it is: 7 mentions across 5 FU-C r1/r2 handoffs (auditor_FU_C_r1_1 ×2, auditor_FU_C_r2_1, explorer_FU_C_r2_2, reviewer_FU_C_r1_2, explorer_FU_C_r2_3 ×2) call it HCP's documented or example subject. That is already in git history and cannot be undone without git writes, which C4 forbids.
- O6. Baselines (my runs):
  - C1 rc 0.
  - `output_sha256_r2.txt` passes `sha256sum -c` with rc 0.
  - `scripts/topic2fu_c_check_receipts_r2.py` rc 0.
  - `scripts/topic2fu_c_verdict_r2.py --out verification/explorer_FU_C_r3_1/verdict_r2_repro.json` rc 0. `cmp` against the shipped `verdict.json` matches byte for byte (sha 4d793102…).
  - Card fc2d0672…, verdict.py 9a1425b6… and receipts.py 7ee0856a… are unchanged.
  - verdict.json: `stop`, "gain below delta, sign unresolved (interval contains 0)", "r1 stop replicated on 8 independent training seeds".

- O7. POST-CONTAINMENT (root message, ~21:44Z: 302 files moved to `~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02/` with MANIFEST.sha256; ACCEPTANCE.md rule (b) added). I re-ran p1 at 21:44:22Z: 20,498 text files scanned, near_copies_ge_0.30 = 0, n_recoverable = 0, and the sealed copy still matches pin line 13. Output: `verification/explorer_FU_C_r3_1/probes/p1_nearcopy_scan_after_containment.out.json`. The four paths are absent. A working-tree grep for the positional-diff field name and wording found only this handoff, where the name has since been neutralised. C1 rc 0.

## 2. Logic Chain
1. All 5 r2 verifiers confirmed the science and every worker claim. Their only blocking item is O2, and the worker had disclosed it as outside its ownership (gate record). O6 shows nothing in the FU-C deliverables has drifted since then.
2. The exposure needs both the near-copy and the old sha. The old sha is in pre-result receipts that may not be edited, and an 8-hex prefix of it is in committed .md handoffs. So the only remedy that does not falsify a receipt is to remove the near-copy (O2). The r3 worker cannot do that (O1); root can, as it did for the dev-salt at 19:3x KST (GATE_STATUS).
3. O3 is the same defect class in a weaker form. Even without the near-copy, the shape cuts the literal to 4 staged candidates. With any sha prefix plus the re-authored-file context it is not brute-forceable, but together with O5's descriptive mentions it effectively singles the ID out. A strict r3 auditor applying "no repo content lets HCP IDs be recovered" (T2.4 wording, applied to FU-C in r2) can block on it. Again only root or the owner can remove it.
4. O4 is a live hazard. If r3 agents follow "verbatim" literally, the disclosure enters permanent git history at the next daemon commit. This is the same class as the prev_snapshot hazard explorer_FU_C_r2_2 found in r2.
5. Scientific design: no rule, interval or reading depends on the test file. The verdict path imports neither the retired file nor the new r2 modules, and reproduction is byte-identical (O6). So r3 must not reopen the card, δ, arms, seeds or the reading; doing so would be a forking path after the results. The errata already in addendum 02 §6 cover the r1 nonblocking interpretive items: §2.2 stall overstatement, the precision prediction that failed, and the scope of `stop` relative to the learned signal. The one new correction is that the r2 headline "closes the C4 blocking class" overstated the state (challenger_FU_C_r2_2), which belongs in a dated addendum 03.
6. Without root action before the r3 verifiers run, r3 repeats the r2 outcome. FU_C then ends INCOMPLETE and needs a PI decision, although nothing scientific is wrong.

## 3. Caveats
- I did not read the r3_2/r3_3 explorers' outputs, the M3 r3 team, or the harness journal outside the repo.
- Membership was checked only against the 1,084 staged names, not the full HCP-YA list.
- Agent transcripts, including those of r2 verifiers and this session, are off-repo and out of scope.
- My p1 probe first printed a total elapsed time. A short-circuit time is a weak side channel on the value. I removed it from the output file and the script within a minute; it appeared only in this session's transcript.
- Whether the committed descriptive mentions (O5) breach C4 is root's or the PI's call. They are permanent history and need a recorded residual, not a fix.
- Root was messaged at about 21:43Z (SendMessage to main). Whether it acts is outside my control.

## 4. Conclusion (recommendation R3-C: contain, re-verify, record; 0 GPU-h)
- **Root, before the r3 verifiers run (ideally before the worker finishes):**
  - Seal off-repo (0700/0400, under `~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/peer_copies/`), then remove `verification/explorer_FU_C_r2_2/{tree,mut_work,code_receipt_subset_derived.view}` and `verification/auditor_FU_C_r2_1/probes/nearcopy_recover.out.json`.
  - Log the containment in GATE_STATUS with UTC time and sha256 (the near-copy's sha 7b915eb7… is safe to record, because the preimage is gone once it is removed).
  - Tell the r3 FU_C agents to summarise the r2 gate record in DISPATCH.md, not re-type it.
  - Before each daemon commit, grep `.agents/` for the disclosure wording.
- **Worker r3 (own paths only), in order:**
  1. Read-only: confirm containment with a near-copy and recoverability scan over the whole working tree, which must find 0, and a shape-disclosure scan.
  2. Add `scripts/topic2fu_c_check_c4_r3.py`. It reads the sealed original in memory, and reports booleans and counts only, with no timing. It checks for 0 near-copies ≥ 0.30 and 0 recoverable files, then runs a count-only B300 membership pass over FU-C paths, all `verification/*FU_C*` folders and all FU-C metadata.
  3. Optional nonblocking hardening (additive, `tests/topic2_fu_c/`, labelled post-result):
     - a synthetic-root test of `supersession.check_receipts`, covering SS01–SS05, SS12 and CK01;
     - a test of the r2 driver's fail-closed path and its refusal to overwrite the shipped verdict (D01/D02, S07);
     - c4scan controls for a 6-digit run starting with 1, a '.'-left context, letter-led `sub-`, and the hex-mask threshold (C413, C409, C404, C02).
     If any new test is hash-dependent, add it to DESELECT and check the count.
  4. Write dated addendum 03:
     - root's containment (who, when, which files, shas, sealed path);
     - the corrected r2 headline;
     - the residuals (O5 descriptive mentions in git history; transcripts), for root/PI acceptance;
     - "verdict unchanged, byte-identical".
     Pin it and the new files in `output_sha256_r3.txt`. Leave every older receipt untouched; the declared failing set stays exactly the 5 r2 lines, and the r2 checker must stay ok.
  5. Rerun: FU-C suite, old 86, topic2_rgpool, topic1_lagmotif, C1, the r2 checker, the r2 driver with `--out`, and the union mutation harness (expect 146 killed, survivors baseline/V07c/V12/F11, 0 invalid).
  6. If containment has not happened by the end, return status BLOCKED, not DONE, naming the exact root action. Never work around ownership.
- **Do not:** edit the card, the r1/r2 receipts, verdict.py/receipts.py/logs.py, the CLI, or any other agent's folder; rerun training; change δ or the reading; write the literal, its digits, shape, positions, a counter or timing into any file.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && /home/juke/superclaude-env/bin/python3 -I verification/explorer_FU_C_r3_1/probes/p1_nearcopy_scan.py $PWD ~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/test_gate_and_records.py /tmp/x.json`: expect `n_recoverable: 0` and an empty `near_copies_ge_0.30` after containment. Currently it returns 1.
- `test ! -e verification/auditor_FU_C_r2_1/probes/nearcopy_recover.out.json && grep -rlI <positional-diff field name> --exclude-dir=.git . | grep -v '\.py$'`: expect no output after containment.
- `grep -rl -e <auditor positional-diff wording> -e <positional-diff field name> .agents/`: expect none.
- `scripts/topic2fu_c_verdict_r2.py --out <path>` then `cmp` against `results/topic2/2026-11-02_fu_c/verdict.json`: expect identical. Run C1 and `scripts/topic2fu_c_check_receipts_r2.py`: expect rc 0.
- Invalidation: if any FU-C deliverable sha differs from the r2 list, or another near-copy appears (for example a verifier mirror built from sealed bytes), this conclusion must be re-examined.
