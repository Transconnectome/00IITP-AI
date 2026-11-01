# Handoff — reviewer_M3_r3_1 (M3 Topic 2, iteration 3, ACCEPTANCE T2.4) — Hard handoff, 2026-11-01T16:50Z

## Review Summary
**Verdict: APPROVE.** T2.4 is met with independently reproduced evidence, and C1–C8 hold for M3 r3's own changes. Nonblocking items are listed at the end.

## 1. Observation
All evidence is under /home/juke/git/00IITP-AI/verification/reviewer_M3_r3_1/.

**Integrity checks**
- C1 PROTECTED_HASHES: 67/67 OK, rc 0. Checked twice, the last time at 16:48Z (c1_protected.txt).
- Receipts (rc_*.txt):
  - addendum_06_sha256: 31/31
  - code_sha256_at_freeze: 33/33
  - output_sha256_r2: 156/156
  - c4_sanitized_sha256: 19/19
  - c4_sealed_originals: 19/19. Checked as a hash-set match against the durable sealed copy; no names were printed and nothing was copied.
  - The old card_sha256 fails exactly 2 lines (hcp_manifest.json, split.json) and the old output_sha256 fails exactly 16 lines (stage0_hcp.json + 15 hcp run.json). This is the set already disclosed from r2.
- The 12 shipped test files, helpers.py and __init__.py are each pinned once in output_sha256_r2, and that check passes. So the shipped files are unchanged.
- The new file sha is 40149a12…808a. Frozen code: scripts/topic2_verdict.py 6695c2ea…6a42, src/topic2_rgpool/stats.py c77d42d2…922a. Both are inside code_sha256_at_freeze 33/33.

**Specs**
- All 24 entries in verification/worker_M3_r3/mutation_specs.json equal their sources field for field:
  - V01–V11 against challenger_M3_r2_2/p07_specs.json (sha de8f2de1…ea4e);
  - the 3 controls against p05_mutants.py;
  - K1 and K2 against challenger_M3_r2_1/run_mutants_c1.py;
  - W04–W09 and W12 against explorer_M3_r3_2/m03_next_round_sweep.py (W12 compared by eye).
- Each old-string occurs exactly once in the frozen code.

**Tests**
- New file on frozen code: 24 passed (t02).
- Full tests/topic2_rgpool on the real tree, CUDA hidden: 115 passed, 1 failed (t01). The failure is test_outputs_no_ids.
  - Count-only attribution: the only flagged file is docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md (BIDS-prefix pattern, 1 hit).
  - addendum_06, the new test file and the receipt have 0 hits.
  - All 13 six-digit runs in the receipt sit inside 64-hex hashes.
- Old 86 with STRICT_E2E=1 and PYTHONPATH=repo root (as dispatched to the worker): 86 passed (t03b).
  - Without PYTHONPATH it gives 85 passed + 1 failed (t03): tests/e2e test_pilot_python_module_cli_execution fails with "No module named 'src'". This is an environment artefact.
- tests/topic1_lagmotif: 88 passed (t04).

**My own mutation harness** (h01_mutation_harness.py; a fresh mirror per mutant; FU cards left out of the mirror docs; rc 0 = SURVIVED, rc 1 = KILLED, anything else = INVALID)
- Leg A, 12 shipped files (h01_shipped.out.json):
  - baseline 92 passed;
  - all 20 non-control mutants SURVIVED;
  - CTRL_t_df_n, CTRL_boot_arm_draws and CTRL_hcp_4_seeds KILLED;
  - V05 was INVALID once (rc −15, an external SIGTERM at 114 s, not the timeout). The rerun (h03_rerun_v05) SURVIVED.
- Leg B, new file only (h01_new.out.json): V01–V11, K1, K2, W04–W08, W12 and CTRL_hcp_4_seeds KILLED. The killing tests match the addendum_06 §4 table exactly. W09, CTRL_t_df_n and CTRL_boot_arm_draws survive.
- Leg D, mutated frozen script on the shipped runs (h01_verdict.out.json): the baseline and all 20 non-control mutants are byte-identical to verdict.json (59af05e5…af68), verdict stop. The 3 controls change the bytes and still give stop.
- Leg C, union: implied by A plus B. The union baseline is 116 passed (seen in h02 and h03).
- Extra critic mutants X01–X15 (h02_extra_specs.json; mine, beyond scope) on the union: all 15 KILLED (X08 after one INVALID rerun, h03_rerun_x08). Among them:
  - F+ "and"→"or" and F+ without the S condition;
  - script ignores F+; script swaps the F+/F− gates;
  - order check on the E arm only;
  - α 0.10; stop with `<=`;
  - default δ 2 %; fixture gates on seed 0 only;
  - fixture or hcp "need" without arm S;
  - I2 computed against E;
  - keep without the I1 lower-bound condition;
  - F− downgrade removed;
  - bootstrap seed 1.

**Independent recomputation from the 27 run.json files** (aggregates only)
- 27 distinct keys, all completed.
- F+ gains C vs E 3.0607 %, C vs S 2.9347 % (pass). F− gain C vs E −1.7373 % (pass).
- I1 mean 0.1468 %, 95 % t [−0.0677 %, +0.3614 %]. I2 lower bound +0.0010 %.
- Last F+ end 03:42:08Z, before the first hcp start at 03:44:51Z.
- All of these equal addendum_06 §3.

**Salt containment** (s02, counts only; salt kept in memory)
- The sealed salt sha matches root's prefix 7e5434ab. The file is mode 0400; its directory and the parent are 0700; it is not in a git work tree.
- 7 salt variants: 0 of 19,392 working-tree files (2.33 GB) and 0 occurrences in `git cat-file --batch-all-objects` (0.84 GB).

**Other checks**
- Whole-run audit_layout.py: PASS, 405 files, 0 findings, rc 0 (a01).
- Addendum §6 cites `r05_connectome_final_suite.log`. The actual files are `verification/worker_M3_r3/connectome/r05_final_suite_{i,ii}.log`: 116 passed with the FU cards left out, and 1 failed + 115 passed with them.

## 2. Logic Chain
1. T2.4(a) asks that V01–V11 be killed by additive tests while src and scripts stay frozen.
   - Leg A shows all of them survive the shipped 12 files; leg B shows each is killed by the new file; the frozen code passes the new file.
   - So the kills are attributable to the new file, and the frozen code is untouched (receipts).
   - K1, K2, W04–W08 and W12 are also closed.
2. W09 is argued to be equivalent. t_interval returns hi = m + q·se with q > 0 and se ≥ 0, and under IEEE monotone rounding m + (non-negative) ≥ m. Then hi < δ implies m < δ, which implies not I1_survives, so the two conditions agree on every value t_interval can produce. NaN is false in both versions.
   - stats.verdict receives only t_interval outputs from the script, so the proof is valid on the reachable domain. I agree with it.
3. T2.4(b) asks for an erratum. Addendum_06 E1 quotes card §7.2 and the script's `else` branch correctly; I verified this against scripts/topic2_verdict.py lines 47–70.
   - E2–E5 are real code behaviours, verified by reading the code. E2 and E3 are interpretive and say so.
   - My hand enumeration of the 27-scenario grid gives 6 (E2) + 4 (E3 strict) + 2 (E1) = 12 differences, matching p01.
   - The frozen script and card were not edited (receipts).
4. T2.4(c) asks to confirm dev-salt containment. The salt and its variants appear in 0 working-tree files and 0 git objects, and the salt is sealed with tight permissions.
   - The 5 salted hashes therefore cannot be inverted from repo content.
   - The positional statement ("positions 0-4 of the sorted listing") is a C4-sanctioned positional index. It needs off-repo HCP data to resolve, so it is disclosed, not hidden.
5. T2.4(d) asks for no regression.
   - C1 and every existing receipt are unchanged.
   - Old 86, topic1 88 and the new suite all pass. The shipped topic2 suite is green with the FU cards left out.
   - The single red test is caused by another team's file (FU-B), not by any M3 r3 file.
   - The shipped verdict stays stop and is byte-identical under every non-control mutant.
6. Integrity: there are no hardcoded expected outputs in production code (production is frozen). The tests' expectations quote card text. The pinned frozen labels are marked [erratum] and paired with card_reading. The worker's claims matched my independent reruns in every leg. I found no fabrication.

## 3. Caveats
- I did not rerun the worker's connectome legs. I reran all legs locally on DGX-Spark (superclaude-env: torch 2.11 dev, numpy 2.3.5, scipy 1.15.3), which differs from the worker's connectome venv. The results agree, including the byte-identical verdict.json.
- Leg C was not run separately for the 24 specs. It is implied: A ∪ B kills, plus the union baseline passing.
- I edited h01_mutation_harness.py while leg A was running, to add an optional spec-file argument. Behaviour for the 2-argument call is unchanged; the edit is disclosed here.
- I did not reproduce the worker's 10⁶-name brute force or its 16-hex-window scan. My salt scan covers the variant channel only.
- The plain-text scan against the B300 HCP listing was not re-run (it needs B300; the worker discloses the same gap).
- Coverage is the enumerated set plus my 15 extras. This is not a proof against every possible verdict-path mutant.
- I did not read other r3 verifiers' folders (independence).

## 4. Conclusion
APPROVE M3 r3 for T2.4. Nonblocking items:
- N1 (ROOT ACTION, not M3): docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md makes the shipped C4 test test_outputs_no_ids red (current real tree: 115 passed + 1 failed). The FU-B owner must reword it before any FU-B or R1 gate.
- N2 (PI ruling): the positional dev-subject residual. Addendum_06 §5 itself restates the positional sentence, which adds one more doc copy that host daemons will commit. A pointer would have sufficed.
- N3: addendum_06 §6 names a non-existent log file. The real files are connectome/r05_final_suite_{i,ii}.log. Correct it in a later dated note, since the addendum is pinned.
- N4: the old-86 command needs PYTHONPATH=repo root. Without it one e2e test fails. Future dispatches should state this.
- N5: card_reading (E1–E3) lives only in a test file. Readers and the R1 report must apply it by hand. The E2/E3 reading choice (strict vs narrow) is for the PI.
- N6: E1–E5 become reachable in FU verdict code (§8 advice). FU verifiers should check that the FU scripts do not reuse the frozen script.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt   # 67 OK rc 0
grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c          # 31 OK
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic2_rgpool/test_verdict_path_guards_r3.py   # 24 passed
cd verification/reviewer_M3_r3_1 && /home/juke/superclaude-env/bin/python3 -B h01_mutation_harness.py new /tmp/x.json   # V01-V11 KILLED
```
This review is invalidated if any of the following changes: the new test file sha 40149a12…, addendum_06 b9176ad6…, the receipt 4ac6d454…, frozen stats.py c77d42d2… or topic2_verdict.py 6695c2ea…, or the verdict.json bytes 59af05e5….

Messaging: SendMessage was not used. The dispatch says nested spawning is unavailable and the structured return is the final report; the parent is a workflow script.
