# Handoff — explorer_FU_C_r2_1 (FU_C iteration 2, explorer 1 of 3; lens: scientific design and falsifiability)

Type: **Hard**. Written 2026-11-01T20:45Z. 0 GPU-h used, no ledger rows, no git writes, no participant token printed or written (every ID check was count-only).

**Summary.** The FU-C science is sound and needs no new card, no rerun and no GPU. The r2 work is a C4 remediation plus a provenance repair. The fix the r1 verifiers suggested, replacing the literal in place with "000000", does **not** close C4. The original receipts must stay unedited, and they keep the old file's sha. With that sha, the literal can be brute-forced from the edited file in 2.8 s. The recommended fix (R-b) has five parts:
- seal the original file off-repo;
- retire it from the repo and re-author its tests in a new file that cannot be derived from the old one;
- repair the one pinned real-repo test that any fix breaks;
- reproduce the verdict byte-for-byte from a verbatim verdict_code subset of the original receipt;
- record everything in addendum 02, with labelled post-result receipts.

## 1. Observation

O1. **Where the literal is** (count-only, boundary-aware regex `(?<![0-9A-Za-z.])<lit>(?![0-9])`):
- The only repo file that contains it is `tests/topic2_fu_c/test_gate_and_records.py:182`, in a parametrize case commented `# HCP-ID shape`.
- One other hit, in `results/topic1/2026-10-31/extract_primary.jsonl`, is a coincidence inside a float (`"021U": <LIT>.117`). It is not an ID.
- `git log --all -S` shows the literal in no FU-C commit. The only two hits are commits from January 2026 (`.obsidian` snapshot), and those match only as substrings.
- No file of that name exists under /tmp or on B300 `/scratch/iitp4` (name search, read-only ssh).
- On B300, I checked count-only against the 1,084 staged HCP names. The FU-C paths hold 7 unique standalone 6-digit tokens, and exactly 1 of them is a staged HCP name: the literal. "000000" and "h000000" are not HCP names.

O2. **Where the file is pinned.**
- `results/topic2/2026-11-02_fu_c/code_sha256_before_results.txt` line 13, `# section: tests`, frozen 16:31:53Z.
- `results/topic2/2026-11-02_fu_c/output_sha256.txt` line 162.
- It is not in PROTECTED_HASHES and not in the governing section of card_sha256.txt.
- Neither receipt is tracked by git. The old full sha, and also its 8-hex prefix, appear only in those two receipts and in `verification/explorer_FU_C_r2_2/tree/` (a copy of the receipts).

O3. **What the daemons commit.** The host and root daemons commit `.agents/**.md`/`.txt` and `docs/**`, judged from the last 40 commits; e.g. the FU-C result report and addendum_01 are tracked. `results/*.txt` and `*.py` are not committed.

O4. **Brute-force probe** (`verification/explorer_FU_C_r2_1/probe_bruteforce_recoverability.py`, `.out.json`).
- Setup, in memory only: the in-place fix `literal → "000000"`. The probe then uses only the edited bytes and the retained pinned sha, and tries all 900,000 values from 100000 to 999999.
- Result: `{"n_matches": 1, "elapsed_s": 2.78, "recovered_equals_real_literal": true}`.
- An 8-hex prefix alone would also identify it uniquely with probability about 0.9998.

O5. **The frozen verdict code** (`src/topic2_fu_c/receipts.py`, `verdict.py`, pinned and unchanged):
- `build_context(root, card_receipt=None, code_receipt=None)` verifies every entry in every section of the code receipt (`verify_entries`). A changed or missing test file therefore gives `ctx["problems"]`, and the verdict becomes `no_verdict`.
- `check_record` compares `start_utc` only with `ctx["frozen_utc"]`, the card freeze, never with `code_receipt_utc` (verdict.py:257–259). So a different code receipt passes as long as its `frozen_utc` ≥ the card freeze.
- `REQUIRED_CODE` = verdict.py, logs.py, receipts.py and scripts/topic2fu_c_verdict.py. These are exactly the `verdict_code` section, lines 4–8 of the original receipt.

O6. **Probe on a copied tree without the file** (`tree_retired`, since deleted). With every other pinned file present:
- `pytest tests/topic2_fu_c`: `1 failed, 58 passed`. The failure is `test_perms_receipts_c4.py::test_context_from_the_repo_has_no_problems_once_code_is_pinned`, a pinned test that calls `RC.build_context(D.REPO)` with the default receipt (line 98).
- Frozen CLI: `no_verdict` with problems `['pinned file missing: tests/topic2_fu_c/test_gate_and_records.py']` (`cli_on_retired_tree.json`).
- The same happens for an in-place edit, as "pinned file changed".

O7. **Subset-receipt probe** (`probe_subset_receipt_repro.py`, `.out.json`).
- A temporary verbatim subset of the original receipt: the header plus `# section: verdict_code`, 8 lines, original `frozen_utc` 16:31:53Z, no new pin.
- Passed to the frozen `build_context(code_receipt=...)`, it gives `problems []`.
- Frozen `evaluate`, serialised exactly as the CLI does, gives verdict `stop`, and the output is **byte-identical** to the shipped verdict.json (sha 4d7931025c4f…).

O8. **Mutation harness** (`verification/worker_FU_C_r1/mutants/run_mutants.py:79`). It deselects two real-repo receipt tests by node ID. pytest silently ignores a stale `--deselect` ID: in my test, 59 tests were collected, with rc 0 and no error. If the r2 worker renames `test_context_from_the_repo_has_no_problems_once_code_is_pinned`, that receipt test would run in every mutant and "kill" every src mutant through a hash mismatch, which inflates the evidence.

O9. **Peer exposure in the working tree right now.**
- `verification/explorer_FU_C_r2_2/tree/` and `.../mut_work/m/` each hold an in-place-edited copy of the test file that differs only on line 182, which now reads "000000".
- `tree/` also holds the old receipts. By O4, the literal is recoverable from working-tree content today.
- These are `.py` files and are not committed. I only compared them count-only and did not read their analysis.

O10. **Scope numbers from verdict.json** (recomputed):
- E seed-mean NMSE is 0.98842, so the learned signal is 0.01158 below predict-zero.
- δ = 1 % relative = 0.009884 absolute = **85.4 % of the learned signal**.
- The I1 upper bound +0.2721 % = 0.00269 absolute = **23.2 % of the learned signal**.
- Dropping only the C s16 stall: I1 sd 0.220 % (r1 0.173 %), half-width 0.204 % at df 6, against 0.144 % predicted (card §12). The result report §2.2 attributes the wide interval to the stalls alone.

O11. **Baseline now:**
- C1 rc 0.
- FU-C receipts (card / code / presentation / output): 0 failures.
- `tests/topic2_fu_c`: 109 passed.

## 2. Logic chain

L1. The C4 defect sits in a test-only file, outside the governing receipt section (O2, O5). It cannot have influenced any Stage-1 number or the verdict. The FU-C card, partitions, runs and verdict stay valid, so there is no new card, no rerun, 0 GPU-h, and the verdict and its reading are unchanged.

L2. The dispatch requires every existing receipt to be kept, and the M3 precedent (addendum_05) keeps them unedited. So the old sha stays readable in the working tree (O2). An in-place same-position edit leaves `old_bytes = f(new_bytes, 6 digits)`, which is brute-forceable in seconds (O4). That is the same class as the r1 M3 B1 C4 failure (unsalted hashes recoverable to HCP IDs). **R-a (in-place "000000") does not close C4.** A strict r2 auditor can reproduce O4 and re-block.

L3. Recoverability ends only if the old preimage cannot be derived from anything in the repo. That needs three things:
- the original bytes move to an off-repo seal;
- the file is retired from the repo;
- its tests are re-authored in a new file whose text is not a line-level derivative of the old file, so no "reinsert one line" or "replace 6 digits" hypothesis reproduces the old sha.
Then the old sha in the receipts pins an unavailable 12.9 KB document, just as the M3 receipts pin sealed originals. This is **R-b**.

L4. Any fix, R-a or R-b, breaks one pinned real-repo test and turns the frozen CLI into `no_verdict` (O6).
- The repair cannot touch receipts.py or verdict.py (verdict-path pins) or the historical receipts.
- So `test_perms_receipts_c4.py` must change in place (its old bytes hold no ID, so a plain diff and its old sha can be published).
- The repaired test should assert both of these:
  - the original receipt now yields exactly one problem, the retired file;
  - the verbatim verdict_code subset yields no problems.
- It must keep its node ID, or the mutation harness silently stops deselecting it (O8).

L5. Verdict reproducibility can be restored without a new pin and without a backdated time. The verdict_code subset of the original receipt reproduces verdict.json byte-identically (O7). It is better than a "supplementary receipt with a new frozen_utc", which would change `receipts.code_receipt_utc` in the CLI output and would assert a pin made after the results. The subset should be built in memory or in a tempfile by a small new driver script. If it is written to disk, it must carry a header saying it is a verbatim subset, not a new pin.

L6. The new and changed test files, the driver and the addendum are written after the results. They are pinned for the record in a separate, clearly labelled post-result receipt; they govern nothing, and C3 governs cards, not tests. The verdict-path files stay byte-identical to their pre-result pins, and that is the integrity claim the gate needs.

L7. The two historical receipts will then fail by design. Each fails on exactly one line for the retired file, and output_sha256 also fails on the edited `test_perms_receipts_c4.py` (its code-receipt line 16 fails too). The M3 precedent covers this:
- an additive check script asserts that exactly the expected lines fail and that all others pass;
- a root-run off-repo check confirms the sealed original equals the old pin (count-only "OK").
The dispatch rule "all existing receipts" conflicts with C4 here, and C4 outranks it (addendum_05 line 52 precedent). Root should authorize this explicitly in the r2 dispatch.

L8. On the daemon hazard (O3): under R-a, writing the old sha or its prefix into any `.md` would put the recovery key into git history permanently. Under R-b it is harmless, but the r1 reviewers' advice to "record old and new sha of the test file in the addendum" should still be avoided: reference the receipt line instead. That costs nothing and protects against a fallback to R-a.

L9. Falsifiability and scope (O10, nonblocking but reportable). With the same data and rules, the stop excludes relative gains ≥ 0.27 %, about 23 % of the E arm's learned signal. δ = 1 % corresponds to about 85 % of the learned signal.
- The verdict is correct under card §5.
- The addendum should state this scope so that "stop" is not read as "box pooling cannot matter".
- The card §12 precision prediction failed (0.386 % against 0.144 % half-width), and the cause is not only the stall: the seed sd was underestimated from 5 seeds.
These are errata and interpretive notes. They do not change any rule (PI decision 3 fixes δ).

## 3. Caveats

- I did not read the other r2 explorers' or the M3 r3 team's analyses (independence). I touched explorer_FU_C_r2_2's copied files only with a count-only cmp and a masked view of line 182.
- R-b's non-derivability can only be shown by the worker on the actual re-authored file, with a probe over the obvious reconstruction hypotheses. It cannot be proven in general. Copies of the old content outside the repo (agent transcripts under ~/.claude, other sessions' scratch) are outside repo scope, at the same level as the seal.
- Of the 6 other standalone 6-digit tokens in FU-C paths, none is among the 1,084 *staged* HCP names, but HCP-YA has about 1,200 subjects. A non-member is therefore not proven a non-ID, and the worker must classify each by meaning (e.g. `n_group_mask_voxels`).
- Whether a public, non-cohort example ID that can be recovered by hashing is a C4 violation is a judgement for root and the PI. The fallback, R-a plus a recorded de-minimis decision, is legitimate only if root or the PI signs it.
- Writing into `~/.local/share/00IITP-AI_sealed/` is root's convention. I did not test whether a worker may write there.
- My verification tree was deleted after the probes, so rerunning O6 and O7 requires rebuilding it (see §5).

## 4. Conclusion (recommended r2 scope; fixed, 0 GPU-h)

1. **Seal first** (root, or the worker if the dispatch authorizes it):
   - Copy `tests/topic2_fu_c/test_gate_and_records.py` byte-exact to `~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/` (dir 0700, file 0400).
   - Verify it count-only against code-receipt line 13.
   - Write an additive repo receipt `results/topic2/2026-11-02_fu_c/c4_sealed_originals_sha256.txt` with hash and path only.
2. **Retire and re-author.**
   - Remove the file from the repo.
   - Write `tests/topic2_fu_c/test_gate_and_records_r2.py` with the same behavioural cases. It must not be a line-level derivative of the old file, must contain no 6-digit literal, and must build the shape cases at runtime (`"0" * 6`, `"h" + "0" * 6`).
   - Show non-derivability with a probe: for each 6-digit position, and for reinsertion of a templated `# HCP-ID shape` case line at every line boundary, 0 candidates reproduce the old pin.
3. **Repair the pinned receipt test in place**, keeping its node ID: `test_perms_receipts_c4.py::test_context_from_the_repo_has_no_problems_once_code_is_pinned`. It asserts:
   - the original receipt yields exactly `["pinned file missing: tests/topic2_fu_c/test_gate_and_records.py"]`;
   - the verbatim verdict_code subset yields `[]`.
   Update nothing else in that file.
4. **Reproduction driver.** Write a new `scripts/topic2fu_c_verdict_subset_check.py` that:
   - builds the subset receipt in memory or a tempfile;
   - runs the frozen `build_context` and `evaluate`;
   - requires a byte-identical verdict.json.
   Verifiers are told to use it; the frozen CLI now returning `no_verdict` is documented, expected behaviour.
5. **C4 tripwire and a new guard-test file** (`tests/topic2_fu_c/test_c4_and_guards_r2.py`, additive):
   - **C4 scan.** Cover src/topic2_fu_c, tests/topic2_fu_c, scripts/topic2fu_c_*.py, docs/.../2026-11-02_topic2_fu_c_*.md, results/topic2/2026-11-02_fu_c and verification/worker_FU_C_r*. Flag standalone `[1-9]\d{5}` (letter/digit/dot-bounded), `sub-` and 16-hex tokens, with a documented, meaning-based allowlist.
   - **Recoverability.** No pinned old sha may have a derivable preimage in the repo.
   - **Kill tests** for the r1 challengers' survivors: X30 (heterogeneous per-subject NMSE: pooled Σnum/Σden vs mean of ratios), X01/X02 (den ≤ 0, num < 0), X09 (nmse tolerance), X03 (start == freeze), X10/X11 (gate record source and seed), X26/X28 (token regex anchor and length, h + 6 digits), and X15/X17/X21/X28 (receipt guards on synthetic receipts in tmp_path).
   - **start_utc format.** All shipped start_utc values and the card frozen_utc match `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$`. This makes the pinned lexicographic comparison chronological for the shipped data; the fail-open path on `+09:00` stays a documented limitation, with no code change.
   - Add any new real-repo receipt test to the harness DESELECT in a harness **copy** under verification/worker_FU_C_r2/.
6. **Evidence and mutation re-runs:**
   - Rerun the worker harness and both challengers' harnesses (copies, own output dir), proving: baseline survives, 51 or more killed, survivors ⊆ {V07c, V12, F11}, and the listed X survivors are killed. Count collected tests to show the deselect worked.
   - Run C1, the old suite (86), topic2_rgpool, topic1_lagmotif and the FU-C suite.
   - Run a B300 count-only membership scan of every r2-written file, `.md` metadata included.
7. **Addendum 02** (`docs/.../2026-11-02_topic2_fu_c_addendum_02.md`) records:
   - the C4 incident;
   - what was sealed, retired and re-authored;
   - receipt lines that fail by design, referenced by file and line number (**never quote the old sha or its prefix**);
   - the reproduction rule;
   - an erratum for result report §4 ("No participant ID…" was false for tests/), with the C4 scan scope widened beyond card §10;
   - an erratum for report §2.2 (sd without the stall 0.220 %, half-width 0.204 %, so the 5-seed sd was also underestimated; the card §12 prediction failed);
   - the scope statement (δ ≈ 85 % and the I1 upper bound ≈ 23 % of the learned signal);
   - the heading-numbering note.
   The result report and the frozen card stay byte-unchanged. Pin the addendum, the new and changed tests and the driver in `results/topic2/2026-11-02_fu_c/output_sha256_r2.txt` (post-result, labelled).
8. **Root cleanup:** remove the in-place-edited copies under `verification/explorer_FU_C_r2_2/{tree,mut_work}` (O9), or have their owner do it. Until then the literal can be recovered from working-tree content.

Fallback **R-a′**: in-place "000000" plus a root/PI-signed de-minimis record that residual hash-recoverability of a public, non-cohort HCP example ID is accepted. Use it only with that signature; otherwise it is likely to fail an r2 audit.

## 5. Verification method

- Footprint (count-only): `cd /home/juke/git/00IITP-AI && L=$(sed -n 182p tests/topic2_fu_c/test_gate_and_records.py | grep -oE '"[0-9]{6}"' | tr -d '"'); grep -rlP --exclude-dir=.git -- "(?<![0-9A-Za-z.])$L(?![0-9])" .` → today: the test file plus the topic1 float coincidence.
- Brute force: `python3 -I verification/explorer_FU_C_r2_1/probe_bruteforce_recoverability.py /home/juke/git/00IITP-AI OUT.json` → n_matches 1. It is applicable only while the file is unchanged; it asserts this.
- Retired-tree check: copy src/{__init__.py,topic2_rgpool,topic2_fu_c}, scripts/{topic2fu_c_verdict.py,topic2fu_c_copyback.py,topic2fu_c_scan_b300.py,b300_env/lock.txt}, tests/{__init__.py,topic2_fu_c minus the file}, results/{topic2/2026-11-01,topic2/2026-11-02_fu_c,gpu_ledger_2026-10-31.md}, verification/worker_FU_C_r1/mutants/{run_mutants.py,mutants_r2.out.json} and the FU-C card into TREE. Then:
  - `PYTHONPATH=TREE pytest TREE/tests/topic2_fu_c` → 1 failed (the receipt test);
  - `python3 -B TREE/scripts/topic2fu_c_verdict.py --out X` → no_verdict with one problem;
  - `python3 -B verification/explorer_FU_C_r2_1/probe_subset_receipt_repro.py TREE results/topic2/2026-11-02_fu_c/verdict.json OUT` → byte_identical true.
- Stale deselect: `pytest tests/topic2_fu_c -q --deselect tests/topic2_fu_c/test_perms_receipts_c4.py::does_not_exist` → rc 0, nothing deselected.
- Invalidation conditions:
  - if root decides the historical receipts may be sealed or replaced, L2 weakens;
  - if a verifier shows the old file bytes are derivable from repo content after R-b, R-b fails;
  - if verdict.py, receipts.py or logs.py change, the subset reproduction no longer applies.
