# reviewer_M2_r2b_1 — handoff (Hard), M2 Topic 3 iteration 2 (r2b gate), 2026-11-01T02:05Z

Probes, logs and evidence: `/home/juke/git/00IITP-AI/verification/reviewer_M2_r2b_1/`. No production file was written. I made no git write of any kind. GPU use was 0. The copied trees were deleted after use; `make_tree.sh` rebuilds them.

## Review Summary

**Verdict: REQUEST_CHANGES (Major, not Critical; no integrity violation).**

- **Finding (i), the Family B estimand, is CLOSED.** Addendum 03 items 1–2 correct the estimand. I recomputed the numbers independently.
- **Finding (ii), the verdict logic unguarded by tests, is closed only for the mutants that were named.**
  - All of challenger_M2_r1_1's survivors are now killed. I replayed them verbatim myself.
  - Independent decision-path mutants of the **same defect classes** still survive the final 88-test suite. One class is Holm vs raw p, here on the primary side. The other is the primary CI being ignored, here at the call site that computes it.
  - Addendum 03 §4 claims the tests pin "Holm p is used, not raw p" for the card §5 rule. That is false for the primary checkpoint.
- **No surviving mutant changes a real verdict.** The scientific results reproduce exactly and stand.
- **The fix is small and additive:** about 4 tests plus an addendum 05 that records their hashes. No rerun is needed.

## 1. Observation

**O1. Integrity, before and after my work**
- C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: rc 0, 67 OK, identical before and after (`baseline/c1_before.log`, `final/c1_after.log`).
- `output_sha256.txt` (42), `addendum_02`, `addendum_03` (3) and `addendum_04` (2) receipts all give rc 0.
- The card hash is `683374565d80…`, equal to `card_sha256.txt`.
- `code_sha256_at_freeze.txt`: 26 OK, and only `scripts/topic3_launch_connectome.py` FAILED (pre-existing, disclosed in addendum 01).

**O2. Suites on the production tree** (`tests/`)

| Suite | Result |
|---|---|
| topic3 | 88 passed |
| old suite, STRICT_E2E=1, explicit list | 86 passed |
| topic1 | 88 passed |

**O3. Reproduction of T3.4** (`rerun/compare_reruns.out.json`)
- Copied-tree reruns of `scripts/topic3_subject_level.py` and `scripts/topic3_token_stats.py` (about 1 min CPU) reproduce `results` in `family_A_subject_level.json` and `family_B_token_level.json` exactly.
- Values that differ: 0. Key mismatches: 0.
- The run-record `code_sha256` maps equal the pinned run records.

**O4. Finding (i), independent recomputation from the pinned token npz** (`probes/probe_estimand_and_alignment.out.json`; all 4 npz match their pins)
- At L2/LN0L2/L3 in every subject and checkpoint:
  - the top-7 eigenvalues carry ≥ 0.99994266 of the variance;
  - the median count above 1e-5×max is 7, with a maximum of 7 (primary and L5e-5 at L2/LN0L2) and 8–10 elsewhere;
  - max |log cat − log mean-frame covPR| = 1.13e-4;
  - the 160-token H4 subsample equals the frame exactly.
- Primary medians: covPR 5.41/5.67, corrPR 5.88/6.14.
- L1 top-63 minimum is 0.99993998 (HCP), which matches addendum 04's correction of addendum 03's "≥ 0.99994".
- Variance ratio of checkpoint means (ddof 1): 13.36 for H1a and 5.84 for H1b.
- CI half-widths: 0.0020–0.0144, which matches addendum 04's correction of "±0.002".
- Addendum 03 §2 supersedes every mis-description I can find: card lines 80 and 98, and report lines 102, 114 and 154 (grep for 1119, within-window, dimensionality, low-dimensional).
- Minor leftovers:
  - report §5 line 166, "CIs of about ±0.003", is covered in substance by addendum 03 item 3 and addendum 04 §6;
  - my within/between SD ratio is 0.0030–0.0055 against the printed 0.003–0.005. The difference is a matter of definition, and the reading is unchanged.

**O5. Worker receipts** (`verification/worker_M2_r2b/mutants/`)
- Run-1 logs: 0 of 69 match the hashes recorded in `MUTANTS_RUN1.json`. This is the overwrite incident, which is disclosed.
- Run 2 and run 3: 69 of 69 match.
- The runner snapshots' sha256 (e186bb75…, 971cdcd6…, c04f9b81…) equal the recorded `runner_sha256`.
- MM 06 log tails: run 3 shipped gives "85 passed" (survived); run 2 with the r2b test gives "2 failed, 86 passed".
- I see no fabrication.

**O6. My independent mutant set: run 1** (`mutants/run_my_mutants.py`, `MY_MUTANTS_RUN1.json`, `logs_run1/`)
- 36 mutants designed by me. Each runs the full suite with no -x, in a fresh copy of a byte-verified tree of 118 files. All 36 applied exactly once.
- Survivors on the final 88-test suite:

  | Mutant | Change |
  |---|---|
  | **V01** | primary significance uses `p_signflip` instead of `p_holm` |
  | **P01** | CI computed on exp(d), so it always excludes 0 |
  | **P02** | the call site requests a 50% CI |
  | **P03** | `ci95` stored as [hi, lo] |
  | **A01** | A2/D3 restricts the 57-row matrices to rows 0–24 instead of the NeuroSTORM positions |
  | V10 | zoo agreement additionally requires the zoo CI to exclude 0 (stricter than the card) |
  | A04 | D2 threshold 0.05 instead of 0.025 |
  | V03/V04/A02/A03/V09 | `>=`/`<=` equality boundaries on continuous statistics |
  | S01 | sign-flip ties excluded |
  | P04 | sign-flip on ratio − 1 |
  | V12 | primary taken as the first dict key |
  | A05, J02 | descriptive only |
  | **X01/X02** | `scripts/topic3_token_stats.py` drops a zoo checkpoint or passes a zoo checkpoint as primary; no test imports this script |

- Killed: V02, V05–V08, V11, V13, P05, K01, K02, A06, E01 (the uncentered T3.1 defect), E02, E03, J01, J03.

**O7. My run 2** (`run_my_mutants_run2.py`, `MY_MUTANTS_RUN2.json`, concurrency 3)
- Controls: 88 passed at start and at end.
- **Verbatim replay of challenger_M2_r1_1's iteration-1 survivors.** The strings were copied from `mutants_challenger.py` lines 25–45. N02, N05, N06, N08, N09, N10, N11 and N17 are **all KILLED**.
- The challenger's N08 patched only the zoo line, `and r["primary"][k]["p_holm"] < …]`, so V01 is not covered by it.
- **Repeat:** V01, P01, P02, P03, A01, V10, A04 and V04 survive again.
- **Demo:** `proposed_tests/test_reviewer_demo_guards.py` has 4 tests and passes on the shipped code (`demo_on_shipped_code.log`: 4 passed). Added to a copy of the shipped tree (92 tests, control 92 passed), it **kills V01, P01, P02, P03 and A01**. V10 and A04 still survive; it was not designed for them.

**O8. Real-data impact of the survivors**
- V01, P01, P02, P03: none. Every pinned primary and zoo raw p is 0.0001, every Holm p is 0.0002, and every CI excludes 0.
- A01: 16 of the 25 NeuroSTORM positions are ≥ 25 (positions only were inspected). A copied-tree real-data rerun of Family A with A01 silently changes 78 reported A2 numbers:
  - BrainJEPA−BrainLM ΔPR₁₂ goes from +2.08 [0.77, 3.40] to +2.96 [1.32, 4.59];
  - NeuroSTORM−BrainLM goes from +3.36 [1.72, 5.01] to +4.57 [3.01, 6.14].
- The D3 verdict stays true, and D1 is unchanged.

**O9. Incident** (`incidents/driver_deadlock_run1.txt`)
- At 10:31:47–48 KST, earlyoom sent SIGTERM to `python3` processes while host free memory was under 10%. Three of my first-wave jobs then hung for about 11 min inside `test_token_job_driver`:
  - the start control;
  - V04;
  - V05.
- The cause: a `multiprocessing.Pool` worker was killed and replaced, and `pool.map` waits forever. The test and the driver have no timeout.
- I killed only my own hung driver and worker PIDs, recorded them, and reran the three jobs in run 2: the control passed, V04 survived and V05 was killed.
- The run-1 entries for these three jobs are contaminated and are superseded by run 2.

**O10. Hygiene and context**
- `audit_layout.py` on the run root: PASS, 154 files, findings [] (`audit_layout_run_root.log`).
- ID grep (`sub-[A-Za-z0-9]`) returns rc 1 (no hits) on:
  - addendum 04, the r2b test and its pin;
  - `verification/worker_M2_r2b` and the worker metadata;
  - all of my outputs.
- HEAD `7430043` (2026-11-01 10:16 KST, "docs(iitp): checkpoint four-topics teamwork documents") holds the final addendum 04 (a1828b38…). The worker's "working copy differs from HEAD" issue is now moot.
- Git context:
  - Commits after ef27b71 that touch Topic 3 paths are e8c795e and 7430043. Both are 15-minute checkpoint commits that change only addendum 04, consistent with the root checkpoint job or chavis-autocommit.
  - No commit touches `src/` or `tests/` after 0db0336.
  - The pinned `results/topic3/2026-10-31/*` outputs are untracked in git; only `addendum_03_sha256.txt` is committed.
- `src/topic3_spectral/__pycache__/{__init__,estimators,resampling}.cpython-312.pyc` was written in the production tree at 2026-11-01T00:39:14Z. That is the same second worker_M2_r2b's MUTANTS_RUN1.json was finalized. It is gitignored and its writer is not confirmed. It is a lead, not a C violation.
- `results/gpu_ledger_2026-10-31.md` now exists (another team's; no M2 entry). `nvidia-smi` shows no compute apps.

## 2. Logic Chain

1. **C1–C2 are met** (O1, O2).
2. **T3.1–T3.4 and C3 card order are met.**
   - The card is unchanged and frozen before results, and the reruns reproduce the pinned outputs exactly with the frozen code hashes (O1, O3).
   - Deviations are recorded only in addenda.
   - H2 (random-init) is disclosed as untested. The column-permutation and iid nulls supply the "shuffled" control that T3.2 asks for.
3. **Finding (i) is closed.** O4 shows that the addendum 03 estimand statements are numerically right (apart from the 3 wording slips addendum 04 already records) and that its supersession table covers the mis-described passages.
4. **Finding (ii) is closed as the challenger defined it.** O7 shows that all named survivors are killed, which meets the challenger's stated invalidation condition.
5. **But as a property, "the verdict logic is guarded by tests" is still not true.**
   - V01 is a reachable, non-equivalent change to the card §5 rule. For example, a primary with raw p 0.03 has Holm p 0.06 and must not be significant. The shipped suite does not detect V01.
   - P01 and P03 disable the "primary CI includes 0 → killed" outcome through its input, which has the same effect as the iteration-1 blocker N06. The shipped N06 test passes hand-built CIs and never checks what `paired_log_contrast` actually produces.
   - A01 silently changes reported Family A numbers (O8).
   - All of this is the iteration-1 defect class, found by an independent mutant set rather than the named one (O6, O7).
6. **The deliverables overstate.** Addendum 03 §4 states that the pinned rule tests check that "Holm p is used, not raw p". That holds only on the zoo side (O7: the N08 patch is zoo-only; V01 survives).
7. **Severity.**
   - No real verdict changes (O8). C3's "fixtures that fail on the targeted defect" is unmet for the primary Holm component and the CI input of the card §5 rule.
   - O7 shows four small fixtures suffice, so the fix is cheap, additive and needs no rerun. That makes it Major and blocking, not Critical.
   - The equality-boundary survivors (V03, V04, A02, A03, V09) need exact equality of continuous statistics, unlike MM 06, which arises from discrete permutation p. They are near-equivalent and not blocking.
8. **No integrity violation.**
   - Receipts are consistent (O5).
   - The regression tests that read pinned JSON are disclosed as post hoc guards.
   - No hardcoded outputs are in the source.

## 3. Caveats

- My mutant set is my own design and has 36 + 8 (replay) mutants. It is not exhaustive.
- I did not rerun the other iteration-1 verifiers' full harnesses beyond the challenger replay.
- The connectome token job was not rerun; it is remote and already independently checked in iteration 1. Family B statistics were rerun locally from the pinned npz.
- The earlyoom incident shows that host memory pressure can hang the shipped driver test. Run times under load (about 100 s per suite) are not representative.
- The pycache writer is unattributed.
- Commit 7430043 is attributed by pattern (15-minute checkpoint) only.
- My demo tests are a feasibility proof, not reviewed production tests. The owning worker should write its own and pin them.

## 4. Conclusion

**REQUEST_CHANGES.**

Blocking (additive; no rerun; no change to src/scripts):
- **B1.** Add a guard that the primary significance in `replication_verdict` uses the Holm p, not the raw p (kills V01).
- **B2.** Add guards that `paired_log_contrast` returns the 95% percentile CI of the log ratios in [lo, hi] order (kills P01, P02, P03). Also add an end-to-end fixture where the primary p is small, the computed CI straddles 0, and the verdict is "killed".
- **B3.** Add a guard that Family A A2/D3 uses the NeuroSTORM positions, not the first 25 rows (kills A01).
- **B4.** Write an addendum 05 that records the new test hashes and corrects addendum 03 §4's "Holm p is used, not raw p" claim, which held only for the zoo side when written.

Non-blocking:
- V10 and A04 rule-threshold guards.
- Driver-script wiring (X01/X02) is guarded only by the code-hash pins.
- `test_token_job_driver` can hang forever when a pool worker is killed; add a timeout.
- The `__pycache__` in the production `src/topic3_spectral`.
- Report §5 line 166 "±0.003".
- Addendum 03's "written about 12:30Z" header against the root-reported 12:17:16Z.

The scientific outcome stands. These are its verdicts:
- H1a holds, read as the spread of 8 spatial-cell vectors;
- H1b not replicated;
- D1 robust;
- D3 ordering reproduces;
- J1 artefact;
- H2 untested.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt     # rc 0, 67 OK
for f in output addendum_02 addendum_03 addendum_04; do LC_ALL=C sha256sum -c results/topic3/2026-10-31/${f}_sha256.txt; done
V=verification/reviewer_M2_r2b_1
bash $V/make_tree.sh $V/tree_base          # byte-verified copy
python3 $V/mutants/run_my_mutants.py $V/tree_base $V/mutants/logs_NEW $V/mutants/NEW.json 3
#   expect V01, P01, P02, P03, A01 (and others listed in O6) SURVIVED; controls 88 passed
python3 $V/mutants/run_my_mutants_run2.py $V/tree_base $V/tree_demo $V/mutants/logs_NEW2 $V/mutants/demo_NEW2/logs $V/mutants/NEW2.json 3
#   needs tree_demo = make_tree + cp $V/proposed_tests/test_reviewer_demo_guards.py tests/topic3_spectral/
#   expect challenger N02 N05 N06 N08-N11 N17 KILLED; demo kills V01 P01 P02 P03 A01
python3 $V/probes/probe_estimand_and_alignment.py      # finding (i) numbers; NeuroSTORM positions != range(25)
python3 $V/rerun/compare_reruns.py                     # after rerunning the two scripts in copied trees (see O3)
```

All runs use `/home/juke/superclaude-env/bin/python3` with `PYTHONDONTWRITEBYTECODE=1` and `nice`.

**Invalidation conditions:**
- If new shipped tests kill V01, P01, P02, P03 and A01, and an addendum pins them and corrects the addendum 03 §4 claim, the blocking issues are closed.
- If someone shows V01 to be unreachable under the card, B1 is withdrawn. It is reachable: a primary raw p in [0.025, 0.05) gives a Holm p ≥ 0.05 whenever the other primary p is larger.
