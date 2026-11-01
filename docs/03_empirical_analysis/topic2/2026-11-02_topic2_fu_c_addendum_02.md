# Topic 2 FU-C card — addendum 02 (worker_FU_C_r2; written 2026-11-01 ~21:00Z UTC, AFTER all FU-C results)

Post-result and non-governing. The frozen card (`2026-11-02_topic2_fu_c_card.md`, sha256 `fc2d0672…4ecb`, frozen 16:13:23Z) is not edited. This addendum records the iteration-2 C4 remediation and a provenance repair that follows from it. **No run, rule, verdict-path file, card or historical receipt was changed, and no GPU was used.** The FU-C verdict stays `stop` (`results/topic2/2026-11-02_fu_c/verdict.json`, sha256 `4d793102…80f5`, unchanged).

## 1. Incident (r1 gate, C4)

- The r1 verifiers found, with count-only checks, that one negative fixture of the FU-C test suite (the token-shape case labelled "HCP-ID shape" in `tests/topic2_fu_c/test_gate_and_records.py`) used a 6-digit literal that is a real HCP-YA ID.
- The literal was not linked to any record, token or result. The file was never tracked by git.
- Result report §4 stated "No participant ID was printed or written". That was false for `tests/`.
- Why the r1 checks missed it: the card §10 C4 scans covered only `results/topic2/2026-11-02_fu_c/` (repo test) and the B300 copy-back tree.
- This addendum refers to the literal only in these terms. No value, digit, position or description that singles it out is written anywhere in iteration 2.

## 2. What iteration 2 did

1. **Sealed.** Before any change, the file's original bytes were copied byte-exact to the off-repo sealed store, `~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/` (directory 0700, file 0400). The sealed copy matches its pre-result pin (code receipt line 13), checked count-only (`verification/worker_FU_C_r2/probes/seal_retired_test.out.json`). Its hash and sealed path are in `results/topic2/2026-11-02_fu_c/c4_sealed_originals_sha256.txt`; only someone with access to the sealed store can verify it. The sealed copy must never be copied back into the repo.
2. **Retired.** The file was deleted from the repo. It was not edited in place.
   - Reason: the pre-result receipts, which may not be edited, keep the old file hash. With the old hash and an in-place-edited copy, the literal is recovered by trying all 900,000 six-digit values in seconds (explorer_FU_C_r2_1, `verification/explorer_FU_C_r2_1/probe_bruteforce_recoverability.out.json`). That is the defect class of the r1 M3 gate failure (hashes recoverable to IDs).
   - With the file retired, recovery would need the exact bytes of all of its other lines. No in-repo file is a near-copy of it except one peer probe tree (§7).
3. **Re-authored.** The retired file's behavioural cases are re-authored in `tests/topic2_fu_c/test_evaluate_records_r2.py`, with a new structure and with every identifier-shaped input built at run time (`"0" * 6`, `"h" + "0" * 6`, format strings). Of the old file's 169 lines of 25 or more characters, 20 occur verbatim in the new file (imports and generic assertions). The new file contains no 6-digit literal (`verification/worker_FU_C_r2/probes/derivative_and_footprint.out.json`).
4. **Repaired in place.** `tests/topic2_fu_c/test_perms_receipts_c4.py::test_context_from_the_repo_has_no_problems_once_code_is_pinned` keeps its node id, which the mutation harness deselects. It used to assert that the repo context has no problem. It now asserts two things:
   - the original code receipt fails on exactly the two superseded test pins (§3);
   - the derived view (§4) gives no problem.
   Nothing else in that file changed. The prior bytes are in `verification/worker_FU_C_r2/prev_snapshot/`.
5. **New code** (post-result, non-governing; not imported by the verdict path):
   - `src/topic2_fu_c/supersession.py`: the superseded-line declaration, the receipt checker and the derived view;
   - `src/topic2_fu_c/c4scan.py`: the strict C4 tripwire;
   - `scripts/topic2fu_c_verdict_r2.py`: the verdict reproduction driver;
   - `scripts/topic2fu_c_check_receipts_r2.py`: the receipt checker CLI;
   - `scripts/topic2fu_c_write_receipt_r2.py`: writes the r2 receipt.
6. **New tests:**
   - `tests/topic2_fu_c/test_c4_and_guards_r2.py`: the strict C4 tripwire with run-time positive and negative controls, the data-level freeze-time precondition, and guard tests for the checks the r1 verifiers' mutants showed were implemented but untested (§6);
   - `tests/topic2_fu_c/test_supersession_r2.py`: receipt supersession, byte-identical verdict reproduction, and the derived-view builder.
7. **Result report.** Minimal in-place correction: a revision banner, the §4 C4 bullet, and the §6 reproduce block. The prior bytes are in `verification/worker_FU_C_r2/prev_snapshot/`. No number, table or reading changed.

Unchanged: `src/topic2_fu_c/verdict.py`, `logs.py`, `receipts.py`, `design.py`, `scripts/topic2fu_c_verdict.py`, the card, `verdict.json`, every run record, and every pre-existing `*_sha256.txt`.

## 3. Receipt lines that fail by design

The pre-result receipts are not edited. Exactly these pin lines fail `sha256sum -c`:

| receipt (in `results/topic2/2026-11-02_fu_c/`) | line | pinned path | state |
|---|---|---|---|
| `code_sha256_before_results.txt` | 13 | `tests/topic2_fu_c/test_gate_and_records.py` | missing (retired, sealed) |
| `code_sha256_before_results.txt` | 16 | `tests/topic2_fu_c/test_perms_receipts_c4.py` | changed (one test repaired) |
| `output_sha256.txt` | 141 | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_result_report.md` | changed (§2 item 7) |
| `output_sha256.txt` | 162 | `tests/topic2_fu_c/test_gate_and_records.py` | missing (retired, sealed) |
| `output_sha256.txt` | 164 | `tests/topic2_fu_c/test_perms_receipts_c4.py` | changed |

- Every other line of every FU-C receipt verifies: `card_sha256.txt`, `code_sha256_presentation_before_results.txt`, and the other lines of the two receipts above.
- The new receipt `output_sha256_r2.txt` pins every file changed or added in iteration 2 and verifies completely.
- `scripts/topic2fu_c_check_receipts_r2.py` checks mechanically that the failing set equals this table. `tests/topic2_fu_c/test_supersession_r2.py` asserts the same.
- None of the superseded paths is a verdict-code, result-handling or governing file. The four `verdict_code` pins and the `result_handling` pins of the code receipt all still verify.

## 4. Reproduction rule

- **The frozen CLI now returns `no_verdict` by design.** `scripts/topic2fu_c_verdict.py` reads the code receipt by default, and that receipt now fails on the two superseded test pins. Never run the CLI without `--out`: its default target is the shipped `verdict.json`. The shipped `verdict.json` and the pre-result receipts were made read-only in iteration 2.
- **The shipped verdict is reproduced by `scripts/topic2fu_c_verdict_r2.py --out <path>`.**
  - At run time it builds a derived view of the ORIGINAL code receipt: the receipt minus its lines 13 and 16, with every other line byte-identical (header, `frozen_utc` 16:31:53Z, the `verdict_code` and `result_handling` pins).
  - It passes the view to the unchanged `receipts.build_context(code_receipt=…)` and `verdict.evaluate`, and serialises the result as the CLI does.
  - The output is byte-identical to the shipped `verdict.json`.
- The view is not a receipt. It is never stored, and it asserts no new pin time.

## 5. C4 scope extension

- The card §10 repo test scanned `results/` only.
- `src/topic2_fu_c/c4scan.py` and its test now scan every FU-C path: `src/topic2_fu_c/`, `tests/topic2_fu_c/`, `scripts/topic2fu_c_*.py`, `docs/…/2026-11-02_topic2_fu_c_*.md`, `results/topic2/2026-11-02_fu_c/` and `verification/worker_FU_C_r*`.
- The scan applies three rules:
  - a standalone 6-digit number with a leading 1–9 that is not part of a decimal fraction (letters may be adjacent, so file-name and label shapes are caught);
  - a `sub-` label containing a digit;
  - a standalone 16-hex token.
  Hash runs are masked first, and hits are reported without the matched text.
- The allowlist has one entry, defined by its meaning: the group brain-mask voxel count in `partitions/perms_fu_c.json`. The test derives that value from the mask array itself.
- Positive and negative controls are built at run time in a temporary directory.
- A count-only B300 membership check of every maximal 6-digit run in the FU-C files and in this worker's metadata against the 1,084 staged HCP names is recorded in `verification/worker_FU_C_r2/probes/b300_membership.out.json` (§7).

## 6. Errata and interpretive notes (no rule change)

1. **Result report §4.** The bullet "No participant ID was printed or written" was false for `tests/`. It is corrected in place (§2 item 7).
2. **Result report §2 item 2 overstates the stall explanation** for the wide I1 interval.
   - Without the C s16 stall (7 seeds, df 6), the I1 sd is 0.220 % (r1, 5 seeds: 0.173 %) and the half-width is 0.204 %.
   - Both are still above the card §12 prediction of about 0.144 %. The prediction failed also because the 5-seed r1 sd underestimated the seed-to-seed spread, not only because of the stalls.
   - Source: `verification/worker_FU_C_r2/probes/addendum_numbers.out.json`, computed from `verdict.json` and the r1 `verdict.json`.
3. **Scope of `stop`.**
   - The E arm's seed-mean test NMSE is 0.98842, so the learned signal is 0.01158 below the predict-zero level (NMSE 1).
   - δ = 1 % relative is 0.00988 in absolute terms, 85.4 % of that learned signal. The I1 upper bound (+0.272 %) is 23.2 % of it.
   - `stop` therefore excludes a practical gain ≥ δ at this budget and target. It does not show that grouping cannot matter; options A and B address target noise and budget.
   - The F+ capacity gate was shown on a synthetic fixture (NMSE ≈ 0.66), not on HCP.
4. **Freeze-time guard.** `verdict.check_record` compares `start_utc > frozen_utc` as strings. That equals time order only for one fixed UTC `Z` format; an offset such as `+09:00` would pass wrongly.
   - All 24 shipped `start_utc` values, the card `frozen_utc` and the code `frozen_utc` are 20-character `Z` strings. `test_c4_and_guards_r2.py` asserts this and checks the time order with parsed datetimes.
   - The guard is not changed, because verdict-path code was pinned before results.
5. **Cosmetic.** Every subsection heading in the result report §1 is numbered "### 1.". This is left unchanged so that the correction stays minimal.

## 7. Evidence and residuals

- **Mutation evidence:** `verification/worker_FU_C_r2/mutants/mutants_r2.out.json` (harness `run_mutants_r2.py`). It covers the union of the worker r1, challenger_FU_C_r1_1, challenger_FU_C_r1_2 and reviewer_FU_C_r1_2 mutant tables, run on the current tree with every hash-dependent test deselected; the deselect count (5) is checked against the baseline.
  - 150 entries: 149 mutants plus the baseline. 146 are killed, 0 are invalid, and the baseline survives.
  - The 3 survivors are V07c, V12 and F11, the same equivalent survivors the r1 verifiers accepted.
  - All 52 mutants that survived the r1 suite in the verifiers' harnesses (challenger_FU_C_r1_1: 20, challenger_FU_C_r1_2: 19, reviewer_FU_C_r1_2: 13) are now killed by the guard tests of §2 item 6.
- **Residuals for root/PI:**
  1. `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` is a peer probe copy of the retired file, edited in place. It sits beside copied receipts, so from working-tree content it is a ≥ 99 % near-copy (probe above), and with the old hash it lets the literal be recovered. Its owner or root should remove that tree (and `mut_work/`). The worker may not write there.
  2. The old file hash remains in the pre-result receipts and in verifier handoffs that are already committed. Without a near-copy of the rest of the file, it does not identify the literal.
  3. Copies of the literal in agent transcripts outside the repo are outside repo scope.
  4. The sealed copy was written by the worker into a new subdirectory of the root-held sealed store. Root may move or re-own it.
