# handoff — explorer_M3_r3_2 (M3 / Topic 2, iteration 3, explorer 2 of 3; lens: feasibility and failure modes). Hard handoff.

**Summary.** T2.4 can be closed cheaply. One new test file closes it with no rerun and no GPU:
- It kills all 11 challenger mutants V01–V11, and every kill is attributable: each mutant survives the shipped verdict-path tests and is killed by exactly the new tests named below.
- The shipped verdict (stop) is byte-identical under every mutant.

The dev-salt containment holds, by count-only scans of the working tree and the whole git object database.

Main risks:
1. A second card-vs-code defect (erratum D: missing F− counted as pass) that r2 did not disclose. The next round's challengers will find it if addendum_06 omits it.
2. Six further verdict-path mutants (W04–W08, W12) survive shipped plus V-tests unless guarded.
3. The shipped C4 scanners read every file in docs/03_empirical_analysis/topic2/, which FU-A..E also write into. One 16-hex sha prefix or the phrase "sub-labels" in any of those files turns the r3 regression suite red.

Probes: /home/juke/git/00IITP-AI/verification/explorer_M3_r3_2/. Proposals: …/proposed/test_verdict_path_guards_r3.py (sha 62874a14…1791, 20 tests) and …/proposed/proposed_2026-11-01_topic2_addendum_06.md. Both are drafts for the worker; I changed no production file.

## 1. Observation
- **O1 (gate record).** challenger_M3_r2_2 REFUTED, with 3 blocking items:
  - (a) dev-salt leak in verification/explorer_M3_r1_1;
  - (b) V01–V11 survive the full 92-test suite (connectome, p07);
  - (c) case A: F+ fails and Stage 1 is not run → the frozen script says no_verdict "Stage 1 incomplete", whereas card §7.2 says inconclusive.

  The other 4 verifiers APPROVE, CONFIRMED or CLEAN.
- **O2 (frozen code).** scripts/topic2_verdict.py:
  - Line 40: fixture gate computed only if all 6 runs are completed, else `pass: None`.
  - Line 48: hcp completeness.
  - Line 53: order assert.
  - Line 66: `S.verdict(ci1, ci2, a.delta, bool(fp), fm is not False)`. So a missing F+ gives False (inconclusive), while a missing F− gives True (counts as passed).
  - Lines 67–70: no_verdict whenever hcp is incomplete, which happens before the F+ gate is read (case A).

  src/topic2_rgpool/stats.py:verdict applies F+ first, then stop, keep, modify, inconclusive, then the F− downgrade of keep only.
- **O3 (card).** §7 heading: fixtures "must pass before any real-data number governs a decision". §7.2: "If F+ fails, Stage 1 is not run. The verdict is then inconclusive". §8: rules are applied "after the §7.2 gate"; inconclusive covers "the F+ gate failed, or keep with an F− failure"; no_verdict = "Stage 1 incomplete after one rerun".
- **O4 (integrity, 14:20Z).**
  - C1: 67/67, rc 0.
  - Code freeze: 33/33. output_sha256_r2: 156/156. c4_sanitized: 19/19.
  - c4_sealed_originals: 19/19 against root's durable copy ~/.local/share/00IITP-AI_sealed/topic2/sealed_c4_from_b300. In the repo it fails 19/19 by design.
  - Old card_sha256 fails on exactly 2 files and old output_sha256 on exactly 16, as disclosed in addendum_05.
  - Hashes of the shipped test files equal those the challenger tested (9a6db1f9…, cd80b075…, db0bc5f4…). So the p07 full-suite survival of V01–V11 still applies to the current tree.
- **O5 (m01, local, 2 pytest invocations per mutant, about 5 s each).**
  - Mutant texts were loaded verbatim from challenger p07_specs.json and cross-checked equal to p05 MUT.
  - Baseline: shipped files 14 passed; proposed file 20 passed.
  - V01–V11: every one SURVIVED the shipped verdict-path files and was KILLED by the proposed file. Killing tests:

    | mutant | killing test(s) |
    |---|---|
    | V01 | test_i1_lower_bound_must_be_strictly_positive |
    | V02 | test_i2_lower_bound_zero_gives_modify_not_keep |
    | V03 | test_i1_mean_equal_to_delta_survives |
    | V04 | test_fminus_gain_equal_to_delta_fails |
    | V05 | test_fplus_gains_equal_to_delta_pass |
    | V06 | test_fminus_failure_downgrades_only_keep |
    | V07 | test_script_missing_fplus_runs_is_not_a_pass; test_script_failed_fixture_run_is_not_counted[Fplus] |
    | V08 | test_script_failed_hcp_run_blocks_stage1 |
    | V09 | test_script_rejects_differing_test_subject_order |
    | V10 | test_script_failed_fixture_run_is_not_counted[Fplus] and [Fminus] |
    | V11 | test_fplus_failure_is_inconclusive_even_when_i1_excludes_delta; test_script_fplus_failure_with_stop_like_stage1_is_inconclusive |

  - Controls: CTRL_t_df_n, CTRL_boot_arm_draws, CTRL_hcp_4_seeds, V12 and V13 are all KILLED by the shipped files.
  - Output: m01_attributable_kills_v2.out.json.
- **O6 (m02).** The frozen script was run on the shipped runs under baseline and under each of V01–V11. 12/12 outputs are byte-identical to the pinned verdict.json (sha 59af05e5…af68), verdict stop.
- **O7 (gate evidence for the erratum).**
  - verdict.json: Fplus pass true (gains 0.03061 and 0.02935); Fminus pass true (gain −0.01737); hcp_complete true.
  - 27/27 run.json have status completed (6 F+, 6 F−, 15 hcp).
  - The F+ runs ended by 03:42:08Z and the first hcp run started at 03:44:51Z. addendum_02 line 19 records that Stage 1 was launched after the F+ gate was computed (pass).
- **O8 (m03 next-round sweep, against shipped plus proposed tests).**
  - First pass: W04, W05, W06, W07, W08, W09 and W12 survived.
  - After 6 small tests were added: only W09 survives, and it is equivalent (proof in L5).
  - Outputs: m03_next_round_sweep.out.json (before), _v2.out.json (after).
- **O9 (s01 salt containment, counts only).**
  - The sealed salt file's sha equals root's record 7e5434ab…d02e; permissions are 0400, directory 0700.
  - Salt hits: full salt, first 12 characters and last 12 characters each have 0 hits in 17,667 working-tree files (2.30 GB), and 0 of 1,568 blobs from `git cat-file --batch-all-objects` (all 2,944 objects, unreachable ones included) contain them.
  - The 5 burned hashes remain only in 3 files: verification/explorer_M3_r1_1/{*.md, *.log, *.json}. No git blob contains them.
  - Without the salt, sha256(name) and sha256(public split salt + name), each with and without a newline, recover 0 of 5 over all 10^6 six-digit names.
  - git: 0 tracked files under verification/explorer_M3_r1_1, not ignored.
- **O10 (C4 scanners).** tests/topic2_rgpool/test_c4_tokens_r2.py `_text_files` and test_outputs_no_ids.py `_files` read every file under results/topic2/2026-11-01 and docs/03_empirical_analysis/topic2.
  - The workflow C FU teams own docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_<x>_*.md (orchestrator/workflow_C_script.js.txt line 48).
  - c01 shows the scanners reject "sha 7e5434ab5a8c757e" (a 16-hex prefix) and "BIDS sub-labels"; they accept "sub- labels", 8-hex…4-hex abbreviations and 7-hex commit ids.
  - The draft addendum_06 and all 8 existing topic2 docs give 0 hits.
- **O11 (regression baseline and cost).**
  - Old 86: 86 passed in 32.6 s locally (STRICT_E2E=1).
  - Challenger's connectome data: uv venv build 76 s; full topic2 suite 92 passed in 107 s (srun -p debug, 4 CPU, 24 G); full-suite runs per mutant 76–157 s, 54 of them in 17.7 min at 8 parallel.
  - Local full suite: earlyoom killed test_partition.py and test_pipeline_guards_r2.py with about 13–14 GB available. 17 GB is available now, with up to 16 agents on the host.

## 2. Logic chain
- **L1.** O5 + O4 → each of V01–V11 survives the shipped tests: the light set here, and the full 92-test suite in p07, whose code and test bytes are unchanged. Each is killed by a named new test. The kills are attributable, so no mutant is equivalent: each kill is a distinguishing input.
- **L2.** O3 → V11 is on-card, not off-card. §8 applies the F+ gate first. The script reaches V11 whenever hcp runs exist beside a failed F+ gate (challenger p06 case B). Only the procedure (§7.2: do not run Stage 1) makes it unreachable.
- **L3.** O2 + O3 → case A is a mislabel. There is also a second, undisclosed deviation, D. `fm is not False` treats missing or failed F− runs as a pass and keeps `keep`, whereas §7 requires the fixtures to pass. challenger p06 case D showed `keep` but did not flag it. An r3 challenger will flag it unless addendum_06 records it. The W12 mutant (card-correct `bool(fm)`) survives everything unless a characterisation test pins the frozen behaviour.
- **L4.** O6 + O7 → neither erratum touches the shipped verdict. Both gates passed with real numbers, every run completed, and none of the boundary values coincides with the data. The mutant-invariance run (O6) is direct evidence, stronger than the argument alone.
- **L5.** W09 is equivalent. t_interval returns lo = m − q·se and hi = m + q·se with se ≥ 0 and q > 0 (df ≥ 1), so lo ≤ mean ≤ hi. I1_survives requires mean ≥ δ, hence hi ≥ δ, hence `hi < δ` and `I1_survives` are never both true. The added conjunct `not I1_survives` is therefore always true whenever `hi < δ`. W05 (median instead of mean) is equivalent only for 2 seeds. FU-C reuses the gate machinery with 8 seeds, so it is killed, not argued.
- **L6.** O9 → the repo alone cannot recover the 5 dev IDs. The 128-bit-class salt is absent from every working-tree file and every git object. The remaining hashes are not invertible without it.
- **L7.** O10 → the r3 regression run and every later gate depend on files that other teams write. Any FU doc with a 16-hex run turns test_no_subject_token_shape_in_any_topic2_text_output red, independent of r3's change. The worker must snapshot and attribute such failures, and root should warn the FU teams.
- **L8.** O11 → the full-suite evidence belongs on connectome, about 10 min including the venv rebuild (CPU only, 0 GPU-h, no ledger row). The local runs should cover the verdict-path files only; a full local suite risks earlyoom collateral kills, which challenger_M3_r2_2 caused.

## 3. Caveats
- My kill matrix ran the shipped verdict-path files (test_stats.py + test_verdict_path_guards_r2.py), not the full 92-test suite. The full-suite survival comes from challenger p07 (connectome, 10:20Z), valid because the code and test sha256 values are unchanged (O4). The worker should re-run the full suite with and without the new file on connectome for its own evidence.
- Local environment only: superclaude-env with DGX-Spark scipy. Float behaviour of the dyadic boundary tests is exact by construction and is asserted inside the tests.
- The salt scan covers the repo only. Session scratchpads, /tmp/claude-1000 and agent transcripts outside the repo were not scanned; the criterion is "repo content". The 0400 sealed salt on the same host still allows recovery by anyone with host access, by design.
- The [erratum] characterisation tests pin frozen behaviour that deviates from the card. That is intentional, so the deviation stays visible, and the names say so. The worker may choose to document D without a pinning test, but then W12 survives and must be listed as such.
- I did not read the other two r3 explorers' reports; this analysis is independent.

## 4. Conclusion (recommended fix strategy)
1. **Tests.** Add one new file, tests/topic2_rgpool/test_verdict_path_guards_r3.py; the proposal is in proposed/ (20 tests).
   - Do not edit test_stats.py (code-freeze pin) or test_verdict_path_guards_r2.py (r2 pin).
   - Call the script via helpers.ROOT, so that mirror-based mutation harnesses exercise the mutated copy.
   - Use dyadic values for the boundary cases.
2. **Mutation evidence.** Re-create V01–V11 verbatim from p07_specs.json, plus baseline and the p05 controls.
   - Run (a) the full shipped suite without the new file: all must survive.
   - Run (b) the new file alone: all must be killed, with the killing tests recorded.
   - Run (c) the full suite with the new file.
   - Use connectome `srun -p debug` (rebuild the venv with challenger connectome_build_and_test.sh; about 10 min, 0 GPU-h), or locally for (b) only.
   - Report W04–W08 and W12 as killed, and W09 as equivalent with the L5 proof.
3. **addendum_06.**
   - Erratum A, with the reading rule "Fplus.pass false → inconclusive".
   - Erratum D, with the reading rule "Fminus.pass null and verdict keep → inconclusive".
   - Note E: duplicate run key resolved by glob order.
   - Shipped-verdict evidence: O6 + O7.
   - Test closure table and salt-containment counts.
   - Add a new receipt results/topic2/2026-11-01/addendum_06_sha256.txt pinning the addendum and the new test file. Leave every existing receipt untouched.
   - Before finishing, run test_c4_tokens_r2 and test_outputs_no_ids over the final text: no 16-hex runs, and no "sub-" followed by a letter.
4. **Containment.** It is verified (O9); re-run s01 at gate time and report counts only.
5. **Regression.** Check C1; code freeze 33/33; r2 pins 156/156 and 19/19; old pins failing exactly the disclosed 2 and 16 files; sealed 19/19 against the durable copy; old 86; topic1; full topic2 suite on connectome; verdict.json byte-identical.
6. **Root.** Tell the FU teams that their docs in docs/03_empirical_analysis/topic2/ are scanned by the r1 C4 tests: no 16-hex runs, no "sub-<alnum>", no "<6 digits>/MNINonLinear". Attribute any red C4 test to the file that caused it.

## 5. Verification method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` → rc 0.
- `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_M3_r3_2/m01_attributable_kills.py $PWD $PWD/verification/explorer_M3_r3_2/proposed/test_verdict_path_guards_r3.py $PWD/verification/explorer_M3_r3_2/work OUT.json`
  - Expect: V01–V11 give A SURVIVED and B KILLED; baseline gives SURVIVED and SURVIVED. About 3 min.
- `… m02_shipped_verdict_invariance.py $PWD WORK OUT.json` → 12/12 byte_identical_to_pinned true.
- `… m03_next_round_sweep.py $PWD PROPOSED WORK OUT.json` → only W09 survives.
- `… -I s01_salt_containment_scan.py $PWD ~/.local/share/00IITP-AI_sealed/topic2/dev_subject_salt.txt OUT.json` → every salt count 0 and every recovered count 0.
- `PYTHONPATH=$PWD … c01_scanner_check.py <addendum>` → token_hits 0 and id_path_hits 0.
- **Invalidation conditions:**
  - any change to stats.py, topic2_verdict.py or the shipped test files (re-check the sha256 values in O4);
  - a new run directory in results/topic2/2026-11-01/runs;
  - an FU doc added to docs/03_empirical_analysis/topic2 that trips a scanner.

Run notes: 0 GPU-h, no ledger row; no git writes; no production file changed; no IDs, salt or hash values printed or written (counts only); ≤1 pytest at a time; work dir removed; no processes left; whole-run audit_layout rc 0, 0 findings (verification/explorer_M3_r3_2/c02_audit_layout.txt).
