# Handoff — explorer_FU_C_r2_2 (FU_C iteration 2; lens: feasibility and failure modes)
Written 2026-11-01T20:30Z. Type: Hard handoff (recommendation only; no production file touched).

**Summary.** The r1 gate failed on one thing: a real HCP-YA ID used as a 6-digit literal in a test fixture (`tests/topic2_fu_c/test_gate_and_records.py:182`), plus the report's false "no ID written" sentence. The science passed every check. Swapping the literal for `"000000"` is behaviour-neutral: the kill matrix is identical and the verdict reproduces byte for byte. But a plain edit has three side effects that would fail the r2 gate:
1. The FU-C suite goes red: 108 of 109 pass.
2. The default verdict command returns `no_verdict` and, with its default `--out`, would overwrite the shipped verdict.json.
3. Two pinned receipts get failing lines.

The workflow's own `prev_snapshot` rule would also copy the literal back into the repo. The fix needs a supersession design, set out below. Cost is 0 GPU-h.

## 1. Observation

| # | What | Evidence |
|---|---|---|
| O1 | `build_context` checks every entry of `code_sha256_before_results.txt`, all sections merged, including the `tests` section | `src/topic2_fu_c/receipts.py` lines 76–79 (`code = {k: v for sec in cc["sections"].values() ...}`; `verify_entries(root, code)`). The receipt pins `tests/topic2_fu_c/test_gate_and_records.py` (sha 3af2eb8c…) in `# section: tests`. `output_sha256.txt` line 162 pins it too. |
| O2 | A real-repo test asserts `build_context(D.REPO)["problems"] == []` | `tests/topic2_fu_c/test_perms_receipts_c4.py:95-101` (`test_context_from_the_repo_has_no_problems_once_code_is_pinned`) |
| O3 | Probe tree (`verification/explorer_FU_C_r2_2/tree`, made by an in-stream copy so the original literal was never written there). Line 182's literal was replaced with `"000000"`. **FU-C suite: 1 failed, 108 passed.** The failing test is O2's, with `'pinned file changed: tests/topic2_fu_c/test_gate_and_records.py'`. | pytest run in the tree |
| O4 | In the same tree, `scripts/topic2fu_c_verdict.py` gives `no_verdict` ("card receipt or pinned inputs do not verify"), with that single problem. Its default `--out` is `results/topic2/2026-11-02_fu_c/verdict.json`, so a run without `--out` overwrites the shipped verdict. | `verification/explorer_FU_C_r2_2/verdict_naive_edit.json`; `scripts/topic2fu_c_verdict.py:22` |
| O5 | **Reproduction path works.** `build_context(tree, code_receipt=V)`, where V is the original pre-result receipt minus only that one test line (frozen_utc unchanged), gives problems `[]`. The pinned `evaluate` then gives verdict `stop`, and its output is **byte-identical to the shipped verdict.json** (sha 4d7931025c4f…). | `probe_subset_receipt.py` → `verdict_subset_receipt.json` |
| O6 | Worker mutation harness (`verification/worker_FU_C_r1/mutants/run_mutants.py`) rerun on the edited tree: 55 entries, 51 killed, survivors baseline/V07c/V12/F11, 0 invalid. Outcome and pass/fail counts per mutant are identical to the shipped `mutants_r2.out.json`. The harness deselects the 2 receipt-hash tests **by name** (lines 79–80). | `mutants_after_edit.out.json` |
| O7 | New sha of the edited test file (only the literal on line 182 → `"000000"`): **7b915eb7f19605c75903fb8da928a56381dc7781973e30edb2950097d2c078a4**. Anyone holding the original bytes can recompute this. | probe output |
| O8 | Count-only literal scan of the whole worktree: only 2 files. One is the FU-C test. The other is `results/topic1/2026-10-31/extract_primary.jsonl`, where it is the integer part of a float (`"999U": 999999.999`; a numeric coincidence). The git index has 0. In git history the only hit is a 2026-01-26 literature PDF (`docs/02_literature/.../mamba_foundation_2024.pdf`, binary, pre-run). The derived copy that challenger_FU_C_r1_2 reported under `verification/reviewer_FU_C_r1_2/mut_work` no longer exists. No other `test_gate_and_records.py` copy exists in `verification/`. | `scan_literal.py` |
| O9 | B300 count-only membership check (tokens piped over ssh stdin; CPU only; nothing printed). FU-C literal in the 1,084 staged HCP dirs: 1. FU-A `tests/topic2_fu_a/test_scripts.py` 6-digit fixtures: 0/3. FU-B: 0/1. Staged dir names starting with 0: 0, so `"000000"` cannot be a staged HCP ID. `/scratch/iitp4/fu_c` holds no copy of the test file. `squeue` g3t-G-E0: 0. | ssh output (counts only) |
| O10 | The shipped C4 rules (`SIXDIGIT = (?<![0-9A-Za-z._-])[1-9][0-9]{5}…`, TOKEN16) applied to FU-C src/tests/scripts/fu_c docs:<br>• before the edit: 1 SIXDIGIT flag (line 182) and 1 TOKEN16 (line 181, the synthetic `0123456789abcdef`);<br>• after the edit: 0 SIXDIGIT, with the same TOKEN16.<br>The shipped repo-side C4 test scans only `results/topic2/2026-11-02_fu_c`. | `probe_c4_scope.py`; `test_perms_receipts_c4.py:110-129` |
| O11 | All 24 FU-C `start_utc`/`end_utc` values are 20-character `…Z` strings. The frozen writer always uses `time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())` (`src/topic2_rgpool/train.py:168,251`), so the lexicographic freeze check (`verdict.py:257-259`, challenger_FU_C_r1_2 nonblocking #1) is chronological for every record this pipeline can produce. | probe output |
| O12 | The workflow's r2 worker prompt says: "Preserve prior bytes of anything you change in verification/worker_FU_C_r2/prev_snapshot/". Done for the test file, that would write the literal back into the repo. | `orchestrator/workflow_C_script.js.txt` (worker template) |
| O13 | The result report and addendum_01 are git-tracked (autocommit daemon commits .md/.txt every 15 min). The FU-C .py files and the results dir are untracked. Result report §6 tells readers to run the code receipt, output receipt and verdict CLI; after the fix those steps show failures or `no_verdict`. §4 contains the false C4 bullet. | `git ls-files`; report lines 165–169, 179–187 |
| O14 | `budget.FU_C_AGENTS` hard-codes r1 agent ids (`src/topic2_fu_c/budget.py:16`), so any r2 GPU use would not be counted by `test_real_ledger_fu_c_usage_is_within_cap`. | source |
| O15 | Baseline state: C1 rc 0; all 4 FU-C receipts 0 failures; live suite 109 passed; my dirs contain 0 copies of the literal. | commands in §5 |

## 2. Logic chain

1. Every byte change to the test file changes a sha pinned in 2 receipts (O1). Any real C4 fix therefore breaks exactly those pins. "All existing receipts pass" cannot hold after the fix. The honest route is documented supersession, which the M3 r2 sanitization already used (`output_sha256_r2.txt` superseding `output_sha256.txt`). Root should expect, and tell verifiers to expect, the precise failing lines.
2. Because of O2, the edit turns the suite red (O3), which fails C2. `test_perms_receipts_c4.py` must change too, which is a second superseded pin. Keep the test's **name** (O6 deselect list) and change only its assertion.
3. Because of O4, the default verdict command fails closed. That is correct behaviour. It must not be "fixed" by editing `receipts.py`/`verdict.py`: that would break the "verdict code pinned before results" chain, which the gate credited. Reproduction should use O5's derived view: a deterministic filter of the authentic pre-result receipt, built in a temp dir at run time and never stored as a receipt. Never back-date a new receipt.
4. O5 and O6 show the change is behaviour-neutral on both the shipped verdict and the fixture kill matrix. The new sha O7 is an independent anchor for "only the literal changed".
5. O12 and O13 show the two ways the fix can recreate the violation:
   - (a) prev_snapshot copies the original bytes into the repo;
   - (b) any .md/.txt that contains the literal, a partial description of it, or a byte-diff count is committed by the daemon into permanent git history, and agents cannot remove it.
   The original bytes belong only in the sealed off-repo dir, which already exists (`~/.local/share/00IITP-AI_sealed/topic2`, 0700). Writing there is outside the worker's ownership list, so root should seal it, or grant the write explicitly.
6. O10: extending the existing rules unchanged to FU-C src/tests/scripts/docs is enough to catch this defect class. It needs a one-item TOKEN16 allowlist and runtime-constructed positive controls, so that no new literal appears in the source.
7. O11: the start_utc fail-open cannot affect any record of this pipeline. Fixing it would mean a post-result change to verdict-path code (point 3). A data-precondition test plus an addendum note is the safe response.
8. O9: FU-A uses the same fixture pattern. Its tokens are not in the staged list, but staged = 1,084 of the HCP-YA cohort, so they are not proven safe. This is for root, not FU-C.

## 3. Caveats

- I did not see the original bytes outside their repo location. I recomputed O7 in memory only, and I did not seal anything.
- O9 checks membership against the 1,084 staged names only, not the full HCP-YA cohort. For `"000000"` the leading-zero argument is complete.
- The FU-A finding is shape plus staged-list only, and I did not read FU-A's handoffs.
- I did not run the old suite, topic2_rgpool or topic1 suites. The verifiers ran them at r1, and the fix touches only FU-C tests.
- 0 GPU-h used; no ledger rows.
- My probe tree (`verification/explorer_FU_C_r2_2/tree`, about 5 MB of sanitized copies plus the edited test file) is kept as evidence. My derived receipt view is named `.view` so the daemon does not commit it as a receipt-like .txt.
- I did not read the other r2 explorers' outputs.

## 4. Conclusion: recommended r2 plan (0 GPU-h; about 30 min of CPU)

**S0 Containment, before any edit (root, or the worker with explicit root grant).**
- Copy the original test file to `~/.local/share/00IITP-AI_sealed/topic2/fu_c_r1/test_gate_and_records.py`: mode 0400, dir 0700, sha must equal 3af2eb8c….
- `verification/worker_FU_C_r2/prev_snapshot/` gets **no copy** of this file. It gets a note with the old sha, the sealed path, and the new sha.
- `test_perms_receipts_c4.py` and the result report can be snapshotted normally, since they contain no ID.

**S1 Edit one token.** Line 182: replace the quoted literal with `"000000"` (same length; HCP IDs never start with 0; O9). The resulting file sha must be **7b915eb7…c078a4** (O7). Any other sha means more changed than the literal.

**S2 Second pinned change.** In `test_context_from_the_repo_has_no_problems_once_code_is_pinned`, keep the name and the other asserts.
- Replace `problems == []` with two checks:
  - (a) the default context's problems equal exactly `["pinned file changed: " + p for p in SUPERSEDED]`;
  - (b) a context built from the derived view in `tmp_path` has `problems == []`.
- SUPERSEDED is the two test files, read from the new supersession receipt.

**S3 New additive test file** (e.g. `tests/topic2_fu_c/test_r2_c4_supersession.py`):
- Reproduction: derived view → `build_context` → `evaluate(n_boot=10000)` → add the `receipts` field as the CLI does → compare against the shipped verdict.json bytes (O5 shows equality).
- The superseded set is a subset of the `tests` section, and disjoint from `REQUIRED_CODE`, `verdict_code` and `result_handling`.
- C4 scope test with the shipped SIXDIGIT/TOKEN16/`sub-` rules over:
  - `src/topic2_fu_c`, `tests/topic2_fu_c`, `scripts/topic2fu_c_*.py`, `docs/.../2026-11-02_topic2_fu_c_*.md`, `results/topic2/2026-11-02_fu_c`;
  - TOKEN16 allowlist: exactly `0123456789abcdef`.
- Positive control: a token of the `[1-9]\d{5}` shape built at run time and written only under `tmp_path` must be flagged. Negative controls: `"0"*6` and a float must not be flagged. No 6-digit literal may appear in the source.
- Precondition test (O11): every shipped `start_utc` matches `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$`, and the frozen writer's format string is the `%SZ` gmtime form.
- Optional additive gap tests from the r1 challengers, each passing on the shipped code: X30 heterogeneous subjects (pooled Σnum/Σden), den ≤ 0 / num < 0, nmse tolerance, gate source/seed, TOKEN_RE anchor, and receipt guards on synthetic receipts. If one fails on shipped code, report it as a real defect. Do not change verdict code silently.

**S4 Receipts.** Leave every old receipt untouched. Add `results/topic2/2026-11-02_fu_c/supersession_r2_sha256.txt`:
- `# frozen_utc: <r2 time>`;
- comment lines listing each superseded `old_sha path`, with the receipt file and line number (expected: code receipt lines for the 2 tests; output receipt lines 162 and 164, plus the result-report line if S6a is chosen);
- verifiable lines for every changed or new file and addendum_02.

Also add a small checker, `scripts/topic2fu_c_check_receipts_r2.py`. It runs `sha256sum -c` on all FU-C receipts and asserts that the failing set **equals** the listed superseded set, no more and no less.

**S5 Addendum 02** (`docs/.../2026-11-02_topic2_fu_c_addendum_02.md`) records:
- the defect and how it was found (count-only);
- the exact changes;
- the behaviour-neutrality evidence (O5, O6, O7);
- the superseded lines;
- the sealed location;
- the C4 scope extension;
- the corrected reproduce commands;
- dispositions of the r1 nonblocking items: start_utc precondition; report §2.2 stall wording, since the sd without the stall is still 0.220 %; the ~1 % learned-signal scope caveat.

It must **never** contain the literal, any of its digits, a changed-byte count, or a description that singles it out (for example "the HCP documentation example subject"). Call it only "a 6-digit literal that is a real HCP-YA ID".

**S6 Result report.** Either:
- (a) **preferred:** an in-place minimal erratum. Replace the false §4 bullet with a pointer to addendum_02, and replace §6 with the new reproduce block. Snapshot the previous bytes; supersede `output_sha256.txt`'s report line in S4. Or:
- (b) leave the report untouched and supersede §4/§6 in addendum_02 only. A fresh auditor may then re-flag the stale sentence.

**S7 Verify.**
- The FU-C suite: 109 shipped tests plus the new ones.
- The old suite (86), topic2_rgpool (116), and C1.
- The S4 checker.
- A copy of the r1 harness in `verification/worker_FU_C_r2/`, with DESELECT extended by every new hash-dependent test (otherwise kills come from hashes, not behaviour). Expect 51/3/0 on the r1 mutants, plus kills for any new mutants.
- A repo-wide count-only literal scan: only the O8 coincidences (float, pre-run PDF) remain.
- A B300 count-only membership check of every 6-digit token in the FU-C deliverables: 0. Pipe over ssh stdin; never put tokens, base64 or hashes of them in command arguments.
- Always pass `--out` to the verdict CLI, and `chmod a-w` the shipped verdict.json and receipts before testing.

**Raise to root.**
1. The C4 fix necessarily leaves 2 failing lines in each of 2 old receipts. Brief verifiers that this supersession is expected.
2. The S0 sealing, or an ownership grant for it.
3. The workflow's prev_snapshot rule conflicts with C4 for this file.
4. FU-A `tests/topic2_fu_a/test_scripts.py` lines 57/59/67 use the same 6-digit HCP-shape fixture pattern. They are 0/3 in the staged list, but not provably non-IDs.
5. FU-C r2 should use 0 GPU-h; `budget.FU_C_AGENTS` would not count r2 agents anyway.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?   # 0
for f in card_sha256 code_sha256_before_results code_sha256_presentation_before_results output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_c/$f.txt | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done   # 0 each (pre-fix)
P=verification/explorer_FU_C_r2_2
(cd $P/tree && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q)   # 1 failed, 108 passed (O3)
python3 -I -B $P/probe_subset_receipt.py $P/tree $P    # problems [] ; stop ; byte-identical True (O5)
sha256sum $P/tree/tests/topic2_fu_c/test_gate_and_records.py   # 7b915eb7... (O7)
python3 -I $P/scan_literal.py /home/juke/git/00IITP-AI      # count-only; prints paths, never the literal (O8)
python3 -I $P/probe_c4_scope.py /home/juke/git/00IITP-AI    # 1 SIXDIGIT flag, masked (O10)
```

The conclusion is wrong if any of these hold:
- the edited file's sha is not 7b915eb7…;
- the derived-view verdict is not byte-identical to 4d793102…;
- the r2 harness kill matrix differs from mutants_r2.out.json;
- the S4 checker's failing set differs from the superseded list.

Probe file shas:
- `probe_subset_receipt.py` f27cac62… (final; output renamed to `.view`)
- `scan_literal.py` d28dc16a…
- `probe_c4_scope.py` 27075e13…
- `verdict_subset_receipt.json` 4d793102…
- `mutants_after_edit.out.json` cbd1ce44…
