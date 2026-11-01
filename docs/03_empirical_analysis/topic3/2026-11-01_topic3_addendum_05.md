# Topic 3 addendum 05: M2 iteration 3 — guard tests for the blocking classes of the r2b gate, union mutation run, corrections to addenda 03/04 and the report (2026-11-01)

Written 2026-11-01 (UTC) by worker_M2_r3, the iteration-3 worker of M2. The PI approved iteration 3 on 2026-11-01 (`.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md`, decision 1). This addendum is additive. The frozen card (sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`), the provenance note, the result report and addenda 01–04 are unchanged. They stay pinned in `results/topic3/2026-10-31/output_sha256.txt` and `addendum_02/03/04_sha256.txt`, and all four receipts verify (§7). The sha256 of this file and of the two new test files is in `results/topic3/2026-10-31/addendum_05_sha256.txt`.

**No verdict changes.**
- No file in `src/` or `scripts/` was changed. No card was re-frozen. No new real-data estimand was computed.
- No real-data analysis was rerun to produce a result. One new test re-derives the pinned Family B output inside pytest's temporary directory and compares it with the pinned file (§2, class 5). That output is discarded with the temporary directory, and nothing is written to the production tree.
- The verdicts in report §4 stand: H1a holds, H1b not replicated, D1 robust and not a per-channel-scale effect, D3 ordering reproduces, J1 artefact, H2 untested.

## 1. Outcome of the r2b gate (iteration 2)

Source: `.agents/teamwork/tw-20261031-four-topics/orchestrator/M2_r2b_gate_record.json` and each agent's `handoff.md`.

| Agent | Verdict | Blocking items |
|---|---|---|
| worker_M2_r2b | DONE | none (its claim: 67 of 67 assigned mutants killed after adding `test_verdict_rules_r2b.py`) |
| reviewer_M2_r2b_1 | REQUEST_CHANGES | B1 primary uses raw p (V01); B2 the CI produced by `paired_log_contrast` is untested (P01 ratio scale, P02 50% level, P03 [hi, lo]); B3 A2/D3 rows (A01); B4 addendum 03 §4 overstates "Holm p is used, not raw p" |
| reviewer_M2_r2b_2 | REQUEST_CHANGES | V01 |
| challenger_M2_r2b_1 | REFUTED | V01; V06/V07/V08 (CI [hi, lo], ratio scale, 50%); V05 (zoo also needs its CI to exclude 0); V26 (`topic3_token_stats.py` passes a zoo checkpoint as the primary; flips the real H1a with the suite green) and V29 (one zoo checkpoint dropped) |
| challenger_M2_r2b_2 | REFUTED | A07 (ci95 stored as [hi, lo]) |
| auditor_M2_r2b_1 | CLEAN | none |

The gate failed. MAX_ITER = 2 had been reached, so the root stopped for the PI. The PI's decision 1 allows iteration 3: additive guard tests and this addendum, with no `src/` or `scripts/` change and no rerun, followed by a 5-verifier gate and the victory audit.

[[SECTIONS_2_TO_4]]

## 5. Corrections found by the r2b verifiers in addenda 03/04 and the report

The pinned files are not edited. The superseded readings are listed here.

| Location | Pinned text | Correction | Found by / evidence |
|---|---|---|---|
| Addendum 03 §4, list of what `test_verdict_rules.py` pins | "Holm p is used, not raw p" | True only for the **zoo** checkpoints (`test_zoo_agreement_uses_holm_not_raw_p`). No test separated raw from Holm p on the **primary** side, because the iteration-2 helper `_rec` sets `p_signflip = p_holm` by default. The primary side is now guarded (§2, class 1). | reviewer_M2_r2b_1 B4, reviewer_M2_r2b_2, challenger_M2_r2b_1 |
| Addendum 03 §2, R2 row | "No reduction in the spread of the spatial-cell vectors at token level (3 of 4 checkpoints; the depth-matched HCP_N400 reduces it by 13% …)" | Holds for the norm-matched **H1a** (log corrPR(L3) − log corrPR(LN0 L2)) only. Under **H1b** (log covPR(L3) − log covPR(L2)), 2 of 4 checkpoints reduce it: HCP_N400 by 10.7% and NewUAH L1e-4 by 3.2% (geometric-mean ratio − 1 from the pinned `family_B_token_level.json`; primary +4.6%, L5e-5 +8.2%). For H1a the figures are HCP_N400 −12.8%, primary +2.3%, L1e-4 +3.9%, L5e-5 +5.0%. | reviewer_M2_r2b_2 (b); recomputed in `verification/worker_M2_r3/probes/check_corrections.out.json` |
| Addendum 03 §2, H4 row | "effective ceilings of 383 (D-limited), 63, 7 and 7" | At L0 the H4 value is computed per frame on 160 subsampled tokens (`src/topic3_spectral/token_job.py` lines 82–86), so it has at most **159** eigenvalues: the ceiling is n-limited, not D-limited. The concatenated L0 matrix stores 384 eigenvalues, not 383 (`cat_cov_eigs__L0` has 384 columns). The reading ("cannot be read as dimensionality changing with depth") stands. challenger_M2_r2b_2 adds that, if the cells are near-static, a 160-token draw covers on average about 138 of the 512 L0 cells and 59.6 of the 64 L1 cells. | challenger_M2_r2b_1 (H4 row), challenger_M2_r2b_2 R-2; `check_corrections.out.json` (`centered_eigs` on 160 × 384 returns 159 values) |
| Addendum 03 header | "Written 2026-10-31 at about 12:30Z" | Written at **12:17:16Z** (the native transcript has the single Write at 12:17:16.770Z, 10 s before the interruption at 12:17:26Z). Git gives an independent upper bound: the file first entered git in root checkpoint `4ce1917` (2026-10-31T12:31:25Z). | auditor_M2_r2b_1 O2 and L1; reviewer_M2_r2b_1/2; challenger_M2_r2b_1 O12 |
| Addendum 03 §3, heading "Label for one unreachable case" | the "killed (primary CI includes 0)" label given to a primary with Holm p ≥ 0.05 and a CI that excludes 0 | The case is reachable on synthetic inputs at the card's B = 9999: `test_primary_holm_rule_end_to_end_at_card_resolution` builds one (raw p 0.0326, Holm p 0.0652, CI [0.0007, 0.0103]). It does not arise in the real data, where every primary Holm p is 0.0002. The code is not changed, and the r3 test asserts only "not holds". | challenger_M2_r2b_1 O8 |
| Report §5, line 166 | "very precise (CIs of about ±0.003 in log ratio)" | The CI half-widths of the primary contrasts are **0.0020–0.0144** across the 4 checkpoints (H1a 0.0020–0.0096, H1b 0.0039–0.0144). Addendum 04 §6 already corrected addendum 03's "about ±0.002"; the report line had not been corrected. | reviewer_M2_r2b_1, challenger_M2_r2b_2; `check_corrections.out.json` |
| Addendum 04 §1, row "23:32:58 … root session commit `0db0336` (69 files) includes addendum 03 and both new tests" (also §2, table row "as written by worker_M2_r2 (in `0db0336`)") | | `0db0336` adds the two iteration-2 test files but does not touch addendum 03. `git log` on addendum 03 lists only `4ce1917` (2026-10-31T12:31:25Z, a root checkpoint commit, which first added it) and `ef27b71` (the root's one-line edit). The pre-edit bytes `725d5077…` are the blob first committed in `4ce1917`; `0db0336` only carries it unchanged. | challenger_M2_r2b_1 O12; re-checked read-only with `git log` and `git show <commit>:<path> \| sha256sum` |

Two further context items from the verifiers, recorded here for completeness:
- worker_M2_r2b's handoff (not addendum 04) attributes checkpoint commits `a18006d` and `bd1f991` to addendum 04. Only `e8c795e` and `7430043` touch it (challenger_M2_r2b_2 O11).
- **Stray bytecode from iteration 2.** `src/topic3_spectral/__pycache__/{__init__,estimators,resampling}.cpython-312.pyc` was written into the production tree at 2026-11-01T00:39:14Z, when worker_M2_r2b imported `src.topic3_spectral` from the project root without `PYTHONDONTWRITEBYTECODE` (auditor_M2_r2b_1 N1; reviewer_M2_r2b_1 and _2 saw the same files). These are git-ignored bytecode with no content effect. This worker did not create or remove them; it is the owner's decision whether to delete them. Iteration 3 wrote no bytecode under `src/` or `scripts/` (§7).

## 6. Limits of these tests

- All 30 tests were written **after** the real-data results existed. They are regression guards for the shipped code, not a pre-registration.
- The closed-boundary tests (§3) reach an end point of exactly 0 only with constructed inputs: hand-built records for the primary CI, identical matrices for D1/D3. For real continuous bootstrap or subsampling bounds an exact 0.0 is practically unreachable. The tests pin the card's rule ("excluding 0", "lo > 0", "< 0.025") at the boundary; they say nothing about how often the boundary occurs.
- The D2 threshold test replaces the column-permutation null with one of chosen size and count (so p_low is exactly 0.02, 0.03 or 0.025). A second test checks, on a real seeded null, that p_low is computed by the card formula.
- The exact-replay tests (`_card_bootstrap_ci`, `_card_signflip_p`, the H4 subsample) pin the frozen seed schedule and draw order, not just the statistics' definitions. A future change of seeds or draw order would fail them even if the statistics stayed correct; that is intended while the card is frozen.
- The Family B wiring test needs the pinned VRABES `layer_3.npz` (read-only, sha256-pinned) to identify the primary from the data, and it skips if the VRABES checkout is absent, like the existing `test_io_contract.py`. It adds about 17 s, and the three refusal tests about 20 s, to the suite.
- The Family A script (`topic3_subject_level.py`) is not rerun. Its wiring is checked in-process with synthetic stand-ins for the two pinned loaders, so that test reads no real data. Family A numbers other than the A2 row identity are not re-derived by the r3 tests; the card parameters that define them are pinned by `test_params_equal_frozen_card`.
- H2 (random-init control) remains untested, as card §6 pre-specified.

[[SECTION_7]]
