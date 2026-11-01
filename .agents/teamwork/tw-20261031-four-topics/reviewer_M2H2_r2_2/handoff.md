# Handoff (Hard) — reviewer_M2H2_r2_2, M2H2 r2 gate (Topic 3 H2 random-init control, iteration 2)
Written 2026-11-01T20:46Z. **Verdict: APPROVE**, with nothing blocking. Five findings are nonblocking: three new surviving mutants on guard variants that only see corrupted inputs, an overstated coverage sentence, and the errata's location and discoverability. PI items stay open: δ and the r2 gate scope.

## 1. Observation
All my probes and logs are in `/home/juke/git/00IITP-AI/verification/reviewer_M2H2_r2_2/`.

O1 **C1 and receipts.**
- PROTECTED_HASHES rc 0 at the start (20:03Z, `logs/c1_start.log`) and at the end (20:44Z, `logs/c1_end.log`).
- `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries), `addendum_07_sha256.txt` and `r2/addendum_08_sha256.txt` (5 entries) are each rc 0, at the start and the end.
- In `results/topic3/2026-10-31`, the receipts addendum_02–06 and output_sha256 are rc 0. `card_sha256.txt` is rc 1 because of its trailing "frozen …" token; the hash `683374565d80…` is right. `code_sha256_at_freeze.txt` is rc 1 only on `scripts/topic3_launch_connectome.py`, the change disclosed in addendum 01. Both failures predate this run.

O2 **Nothing pinned was changed or added.**
- Every file under `src/topic3_h2` (excluding `__pycache__`) and every `scripts/topic3h2_*` file is listed in output_sha256.txt, and the list has no extras.
- Every `tests/topic3_h2/*.py` is in output_sha256.txt or the addendum 08 receipt.
- The newest `scripts/topic3_*` mtime is 2026-10-31T08:51Z.
- No file in src/topic3_spectral or tests/topic3_spectral is newer than addendum 07.
- My own test runs wrote no file into src/tests/scripts/results (checked with `find -newer`). The only new files found belong to other teams' topic2_fu_c paths.

O3 **Test suites, rerun by me.**
- `tests/topic3_h2`: 167 passed in 174.9 s.
- `tests/topic3_spectral`: 138 passed.
- `tests/topic1_lagmotif`: 88 passed.
- Old suite (STRICT_E2E=1: test_empirical_four_topics, test_pilot_connectome, e2e): 86 passed.
- All rc 0. Logs: `logs/pytest_*.log`.

O4 **The four new tests are real tests, not facades.** I read all four files.
- The regression test copies the unmodified script, code and inputs into tmp_path. It runs `gate` and `final` as subprocesses and compares every output leaf except `run`, with floats at rel 1e-12. That makes it a golden regression against the shipped JSON, and the file says so.
- The guards test corrupts one input per case. Each case must give the guard's own SystemExit message, or FAIL on exactly that check.
- The oracle test builds K = 10 synthetic seeds that differ by construction and checks them against an independent numpy oracle. It uses only the frozen resampling primitives. Its hard-coded labels belong to the synthetic fixture (INC, TE+, INC, TE+), not to the real result.
- The gate-components test has offline fakes for the driver paths.
- No expected real-data number is embedded in src.
- Test-file mtimes are 18:00–18:05Z. The union harness started at 18:07:06Z, and its `new_tests_sha256` equals the receipt.

O5 **The r1 blocking class is closed.** I re-ran four r1 survivor edits in my own copied tree, taking the old/new strings from `union_mutants.out.json` (`mut/recheck_r1_survivors.py` and `.out.json`):

| Edit | Shipped 8 files | 4 new files alone | Extended suite |
|---|---|---|---|
| N26 (family C token arm = seed 1) | rc 0, SURVIVED | rc 1, KILLED | rc 1, KILLED |
| N53 (final reads R1 scalars for all seeds) | rc 0, SURVIVED | rc 1, KILLED | rc 1, KILLED |
| N50 (final ignores a gate FAIL) | not run | KILLED | KILLED |
| W4 (T arm replaced by R0) | not run | KILLED | KILLED |

So the worker's claim holds: these r1 survivors survive the shipped suite and are killed by the four new files alone. In `union_mutants.out.json` the summary reads 115 applied, 0 not applied, `extended_full_survivors: []`, and both copied-tree baselines are green. The per-mutant records have plausible timings and failing test ids.

O6 **My own new mutants** (`mut/fresh_mutants.py`, `mut/fresh_mutants.out.json`). I wrote 15 new edits on the verdict and guard paths. The copied-tree baseline was 167 passed, every mutated file was restored byte-identically, and the shipped `h2_results.json` and `gate_decision.json` are unchanged.
- **12 KILLED**:
  - F04: T-A1 reproduction tolerance loosened to 0.5.
  - F06: `p_holm <= α`.
  - F07: Z90 = 1.64.
  - F08: subject-level seed effects pooled.
  - F10: stats_match no longer checks positions.
  - F11: gate accepts ≥ 342 windows.
  - F16: family C Holm replaced by Bonferroni.
  - F17: family L Holm replaced by Bonferroni.
  - F18: TE+ seed condition on the mean seed effect.
  - F19: EQ seed condition on |mean|.
  - F20: CI90 computed at the 95% level.
  - F21: R1 secondary reversed.
- **3 SURVIVED.** None can change a shipped number or label, because on the real inputs every guard passes and the regression test pins the whole output:
  - **F03**: in `cmd_gate`, a missing `G2` in gate_record defaults to `{"ok": True}`. GATE_CASES tests `G5_missing` but not `G2_missing`.
  - **F05**: the BIDS-prefix refusal in `_dump` is disabled (`if b"sub-" in raw and False`). No test makes the script try to write a `sub-` string. The C4 governance of the shipped outputs is still enforced by `test_provenance_governance.py`, which scans the outputs.
  - **F12**: the seed check in `final` compares only the count (`len(seeds) != len(prov.SEEDS)`). The guard tests use a missing seed and an added seed, which both change the count. A substituted seed label is not tested.

O7 **Errata reproduced independently** (`probes/errata_check.py`, `.out.txt`). It uses my own transcription of the §6 rule and my own single-seed arithmetic.
- **E1** boundaries:
  - C1: TE+ below f = 0.1576, EQ from 1.0176.
  - C2: 0.4581 and 1.1115.
  - C3: 0.5484 and 1.2912.
  - C4: 0.6636 and 1.2057.
  - These match addendum 08 within the 1e-4 grid step.
- **E2**: R1 is −1.607 [−3.769, +0.555] (cov) and −0.736 [−3.181, +1.709] (corr).
- **E3**: L0 subject-level is INC for both estimators: cov −0.061 [−0.330, +0.208], corr −0.131 [−0.396, +0.134].
- **E8** single-seed C1: EQ for seeds 1, 5, 8; INC for 2, 3, 6; TE+ for 4, 7, 9, 10. C2 is TE+ for 4, 5, 7, 9, 10. C3 and C4 are TE+ for every seed.
- All of these match addendum 08.

O8 **Ledger.**
- `verification/worker_M2H2_r2/prev_snapshot/gpu_ledger_2026-10-31.md.before_r2_append` (sha `9f9843eb…`, 55 484 B) is a byte prefix of the current ledger (`cmp -n`). So the ledger was only appended to.
- Correction rows 142–143 (218063, 218064) say 0 GPU-h and state that the original rows' hours are already counted.
- The M2H2 GPU-h total is 0.058 (explorers) + 0.458 (worker) + 0.303 (verifiers) = 0.819 of the 6 GPU-h cap.
- No M2H2 GPU row was added in r2.

O9 **IDs and layout.**
- There are 0 `sub-` bytes in `results/topic3/2026-11-02_h2/**`, including r2/.
- The new tests contain only the synthetic `sub-SYN%02d` string, which is built in memory.
- Worker verification files have 0 `sub-` hits.
- The six-digit numbers in addendum 08 are Slurm job ids and hash fragments.
- Whole-run `audit_layout.py`: PASS, findings [], 571 files (`logs/audit_layout.log`).

O10 **Disclosures and coverage of r1 nonblocking items.** Addendum 08 covers:
- reviewer_r1_1 items 1–5 (δ table, R1 wording, R0-as-trained, ledger KST, X04/X09/X14/X15);
- reviewer_r1_2 N1–N6;
- auditor N1 (remote code dir overwrite, as D1), N2 (A05), N4 (E5) and N5 (δ).

It does not mention **auditor N6**: the lab bundle's `--random_init` "TSO probe", which means the exposure claim in addendum 07 §10 can be vouched for only for this run's agents. Rechecking the report numbers is outside r2's scope, and five r1 verifiers had already reproduced them.

## 2. Logic Chain
1. O1 and O2: no pinned or protected byte changed, and r2 only added files. So C1, C3 (frozen card unedited, deviations in a dated addendum) and the PINNED rule hold.
2. O3: there is no regression in any suite. C2 holds.
3. O4 and O5: the r1 REFUTED class was C1-flipping wiring mutants and untested stats-script guards. My own copied-tree runs confirm it is closed: N26 and N53 survive the shipped files and die under the new files. The worker's 115/115 record is consistent with this.
4. O6: on the verdict computation itself, every new mutant I wrote was killed (Holm/Bonferroni, CI levels, Z, seed conditions, seed-effect wiring, secondary wiring). The three survivors are weaker variants of guards that fire only on corrupted or adversarial records. They cannot alter any shipped output. This is the class PI decision 6 treated as nonblocking for M2 r4, and addendum 08 §7 proposes the same scope here. So they do not reopen the r1 class. They do show that the sentence "every guard in the stats script is now tested" (worker headline, addendum 08 §3) is overstated.
5. O7 and O8: the errata are numerically right, and the ledger is correct and append-only. H3′ (report states the verdict and its effect on R1–R3) holds once read together with the E1–E8 errata. H1′ and H2′ were already established in r1 by five independent verifiers, and r2 reran nothing.
6. O9 and the 0 GPU-h of r2: C4, C5, C6 and C7 hold. C8 holds because no EMPIRICAL_ANALYSIS_REPORT number is cited.
7. So every criterion is met with evidence, and the remaining items are nonblocking or are PI decisions.

## 3. Caveats
- I did not rerun any GPU job, recheck the r1-verified report numbers, or redo the full 115-mutant union harness. I reran 4 of its edits, and its record is internally consistent.
- My fresh mutants are a sample of 15, not an exhaustive search of `driver.py`, `data.py` or `model.py`.
- δ (0.5 × |trained effect|, log 1.10) and K = 10 were chosen by the worker, which addendum 08 §8 discloses. Under sci-pipeline, δ is a PI choice. C3's TE+ holds only for f ≤ 0.548.
- My APPROVE is a recommendation. The gate decision belongs to root and the PI (sci-pipeline G9).
- A `__pycache__` folder was created in my own `verification/reviewer_M2H2_r2_2/mut/` because my recheck launch omitted PYTHONDONTWRITEBYTECODE. The permission system refused my attempt to delete it. It is harmless and outside production paths.

## 4. Conclusion
**APPROVE M2H2 r2.** Blocking issues: none.

Nonblocking, for root:
1. Three guard-variant survivors: **F03** (missing G2 record defaults to ok), **F05** (`_dump` BIDS refusal untested) and **F12** (seed identity checked only by count). If wanted, add tests in a new file, e.g. a gate case with `G2` popped, a `_dump` call on a payload containing `sub-`, and a case with seed 10 relabelled 12. These are not gate failures.
2. Correct the wording "every guard in the stats script is now tested" (worker handoff and addendum 08 §3) to "every guard named in r1".
3. Addendum 08, the only record of errata E1–E8 to the pinned report, sits in `results/…/r2/`. Copy it byte-identically next to the report in `docs/03_empirical_analysis/topic3/` (its receipt still applies), and make the integrated R1 report quote E1–E4.
4. Record auditor N6 (exposure claim scope) in a later addendum or in the R1 report.
5. PI: δ, K = 10 and the r2 gate scope (addendum 08 §7–§8). After the victory audit, the connectome leftovers under `/home/connectome/connectome1/iitp4_m2h2/` need cleanup by root.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in results/topic3/2026-11-02_h2/output_sha256.txt results/topic3/2026-11-02_h2/addendum_07_sha256.txt results/topic3/2026-11-02_h2/r2/addendum_08_sha256.txt; do LC_ALL=C sha256sum -c --quiet $f; echo $f $?; done
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. nice timeout 900 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic3_h2   # 167 passed
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M2H2_r2_2/probes/errata_check.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 setsid nohup nice /home/juke/superclaude-env/bin/python3 verification/reviewer_M2H2_r2_2/mut/fresh_mutants.py > /tmp/x.log 2>&1 &   # ~45 min; F03/F05/F12 survive
cmp -n 55484 verification/worker_M2H2_r2/prev_snapshot/gpu_ledger_2026-10-31.md.before_r2_append results/gpu_ledger_2026-10-31.md
```
This verdict is invalidated if any receipt or C1 check fails, if any of N26/N53/N50/W4 survives the extended suite, or if a mutant changes a shipped label while the suite stays green.
Artifact hashes: `fresh_mutants.out.json` 746fc124…8767, `recheck_r1_survivors.out.json` 4b5b606f…15a0, `errata_check.out.txt` 12072813…bcd.
