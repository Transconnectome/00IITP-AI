# handoff — explorer_FU_C_r2_3 (FU_C iteration 2, explorer 3 of 3; lens: adversarial pre-mortem)
Written 2026-11-01T21:10Z. Hard handoff. 0 GPU-h. No git writes. The C4 literal was never printed or written by me (every probe reads it into memory and prints counts and booleans only).

**Summary.** The r1 science stands. The only blocking class is C4: a real HCP ID is written as a literal at `tests/topic2_fu_c/test_gate_and_records.py:182`, and report §4 says no ID was written. The fix is to edit one line. It is dangerous for a procedural reason: the file is pinned in two receipts that must stay unedited, and `receipts.build_context` re-verifies every pinned test. So the natural edit has four effects:
- the shipped verdict CLI returns `no_verdict`;
- the CLI's default `--out` overwrites the shipped `verdict.json`;
- one suite test fails;
- the receipt checks fail.

I tested the safe path in a mirror. A supplementary receipt makes the verdict identical except for one timestamp leaf. Details follow.

## 1. Observation

O1. The receipt chain re-verifies tests. `src/topic2_fu_c/receipts.py:83-88` builds `code = {k: v for sec in cc["sections"].values() ...}` and then runs `probs += verify_entries(root, code)` over **all** sections of `code_sha256_before_results.txt`. That includes `# section: tests`, line `3af2eb8c…  tests/topic2_fu_c/test_gate_and_records.py`. Any problem turns the verdict into no_verdict (verdict.py `F16` path). `build_context(root, card_receipt=None, code_receipt=None)` already accepts an alternative code receipt (line 72). `scripts/topic2fu_c_verdict.py` has no flag for it and always calls `RC.build_context(ROOT)`.

O2. The CLI overwrites by default. `scripts/topic2fu_c_verdict.py` declares `ap.add_argument("--out", default=os.path.join(ROOT, RC.FUC, "verdict.json"))`, so a bare rerun overwrites the shipped verdict.

O3. One test depends on the repo receipt being clean. `tests/topic2_fu_c/test_perms_receipts_c4.py::test_context_from_the_repo_has_no_problems_once_code_is_pinned` asserts `RC.build_context(D.REPO)["problems"] == []`.

O4. The file is pinned twice. `results/topic2/2026-11-02_fu_c/output_sha256.txt` line 162 pins the test file, line 164 pins `test_perms_receipts_c4.py`, and the `docs` section pins the result report. The report's §6 "Reproduce / verify" runs `grep -v '^#' code_sha256_before_results.txt | sha256sum -c` and the verdict CLI (with `--out /tmp/...`).

O5. Mirror prototype (`verification/explorer_FU_C_r2_3/probes/p6_fix_path_prototype.py` → `.out.json`). The literal on line 182 was replaced by `"000000"` during the copy. Results:
- 277/277 lines, exactly 1 line differs, and the old content matches the pin 3af2eb8c.
- The new file sha is **7b915eb7f19605c75903fb8da928a56381dc7781973e30edb2950097d2c078a4**.
- The suite in the mirror gives `1 failed, 108 passed`. The failure is exactly O3.
- With the original receipt: problems `["pinned file changed: tests/topic2_fu_c/test_gate_and_records.py"]` → `no_verdict`.
- With a supplementary receipt (all original lines, new sha for that one file), problems are `[]`. `evaluate` then gives 475/475 leaves, and the only differing leaf is `/receipts/code_receipt_utc`.
- The shipped verdict.json sha is still 4d793102…. The mirror was removed.

O6. Footprint of the literal (`p1_literal_footprint.out.json`, count-only):
- Across 31,912 worktree files, it occurs standalone only in the test file, in `results/topic1/2026-10-31/extract_primary.jsonl`, and in 2 verifier copies of that Topic 1 file.
- The Topic 1 occurrence is the integer part of a `null_mean` float (`p3_context_class.out.json`: previous char space, next char `.`). It is a numeric coincidence, not an ID.
- Git history (182 revisions, `git grep -F` over `rev-list --all`): no text hit. The only hit is a substring inside a binary PDF.
- The derived copy that challenger_FU_C_r1_2 reported (`verification/reviewer_FU_C_r1_2/mut_work/...`) no longer exists.
- explorer_FU_C_r2_2's `tree/` and `mut_work/` copies contain 0 occurrences (`p4_count_in.py`).

O7. B300, count-only, ssh as connectome, no GPU:
- 1,084 staged names, all 6-digit. 0 start with `0`.
- `000000`, `999999` and `123456` are each absent.
- There is no copy of `test_gate_and_records.py` under `/scratch/iitp4/fu_c` or `/scratch/iitp4/explorer_FU_C_r1_2`; `fu_c/code` holds only `lock.txt, scripts, src, topic2fu_c_build_env.py`.

O8. The shipped C4 tripwire leaks (`p5_tripwire_design.out.json`).
- `SIXDIGIT = (?<![0-9A-Za-z._-])[1-9][0-9]{5}(?![0-9A-Za-z._])` in test_perms_receipts_c4.py misses an HCP-filename shape (`NNNNNN_3T_rfMRI…`) and a BIDS shape (`sub-NNNNNN`).
- Its escape `re.search(r"(ElapsedRaw|sec|_s\b|bytes|n_|\d\.\d)", ctx)` passes any 6-digit number within 30 characters of any float.
- A stricter pattern finds only the literal and the `nvox` voxel count in `perms_fu_c.json` across the 166 FU-C deliverable files. That pattern masks hex runs of 16 or more characters, then applies `(?<![0-9.])[1-9][0-9]{5}(?![0-9])`.

O9. Recoverability residual (`p2_recoverability_synthetic.out.json`, synthetic number only). If the old sha stays published and the new file differs only by a 6-digit literal, the old literal is recovered by brute force in 1.6 s (594,039 candidates). The old sha 3af2eb8c… is in two receipts that may not be edited, so after any minimal, verifiable fix the repo still lets the literal be recovered by a deliberate brute force.

O10. The freeze guard compares strings: `verdict.py:257-258` uses `not st > fz`. All 24 shipped `start_utc` values match `\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ`, ranging from 16:35:12Z to 19:08:03Z. The fail-open case (+09:00 offsets) therefore does not affect the shipped data.

O11. The mutation harness (`verification/worker_FU_C_r1/mutants/run_mutants.py`, pinned under `result_handling`) mirrors `tests/topic2_fu_c` and deselects two named receipt tests, including the O3 test. Every other test under `tests/topic2_fu_c` runs against mutated code. Survivors in `mutants_r2.out.json`: baseline, V07c, V12 and F11. F13 (token shape) is killed by a different test than the line-182 row; the row is also caught by the order check.

## 2. Logic chain

L1 (O1, O3, O4). Every in-place edit of the test file has three consequences:
- (a) a shipped-CLI rerun returns `no_verdict`;
- (b) one FU-C test fails, which breaks C2;
- (c) `code_sha256_before_results.txt` and `output_sha256.txt` fail `sha256sum -c` on the edited lines, which breaks the dispatch rule "all existing *_sha256.txt receipts".

None of these may be fixed by editing receipts, by skipping or xfailing the test, or by changing `receipts.py`/`verdict.py`. Those files are verdict-path code, pinned before results.

L2 (O1, O5). `build_context` already takes `code_receipt=`. A supplementary receipt plus a new thin wrapper therefore restores a reproducible verdict without touching verdict-path code. The prototype shows the result is identical except `/receipts/code_receipt_utc`.

L3 (O2, O4). The highest-impact accident is a bare `scripts/topic2fu_c_verdict.py` run after the fix. It writes a `no_verdict` JSON over the shipped `verdict.json` (4d793102…), which destroys the governed output and breaks `output_sha256.txt`. Verifiers in r1 did run this CLI, with `--out`. A careless r2 run or verifier would not.

L4 (O3, O11). The O3 test must change: it is a pinned test, so this is a second superseded line. It must keep its name, because the harness deselects it by nodeid. A new receipt or supersession test placed inside `tests/topic2_fu_c` would run in mutation mirrors and fail for every mutant, producing spurious kills. New receipt-sensitive tests therefore belong in a separate directory.

L5 (O6, O7). `"000000"` cannot be an HCP ID: no staged name starts with 0. It still fails `^h\d{2}$`, so the row's meaning is unchanged. The live footprint is that single line. A repo-wide 6-digit tripwire would raise a false alarm on Topic 1 floats, so the extended scan should cover FU-C paths, with membership against the 1,084 names as the decisive count-only check.

L6 (O8). Extending the shipped `SIXDIGIT` test to `tests/` and `src/` would inherit two leaks: HCP-filename and BIDS shapes, and the float-proximity escape. The extension needs the stricter pattern with an exact allowlist keyed by path and JSON key, not by context.

L7 (O9). There is a trade-off between verifiability and containment. A minimal, documented edit (verifiable) leaves the literal recoverable from the immutable receipt sha. An undocumented large rewrite would hide it, but then the change could not be verified, which is worse. The residual is unavoidable and needs an explicit root/PI record:
- verifiers r1 call it the public HCP-documentation example subject;
- it is not in the 88-subject cohort;
- it is linked to no record.

L8 (L1–L7). Sealing the original bytes off-repo (reviewer_FU_C_r1_1's suggestion) keeps a copy of the ID for no benefit. The pin plus a per-line proof already verifies the edit. Root may still decide otherwise.

L9 (O10, card §14). Fixing nonblocking verdict-code issues, such as the lexicographic `start_utc` guard, would mean editing `verdict.py` after the results were seen, which is a forking path. It must be recorded, not fixed. Additive guard tests are allowed only in a new directory, labelled post-result. If one fails on the current code, that is a finding to report with its effect on the shipped data, not a reason to change `verdict.py`.

## 3. Caveats

- I did not read the other r2 explorers' reports (to keep this independent). I only counted occurrences of the literal in explorer_FU_C_r2_2's copies.
- "Public HCP documentation example subject" comes from reviewer_FU_C_r1_2 and auditor_FU_C_r1_1. I did not verify it, because verifying would mean revealing the ID.
- Membership was checked only against the 1,084 staged names, not the full S1200 list.
- Agent transcripts (off-repo session logs of every agent that read the file unmasked) contain the literal. I cannot assess or clean them; root's call.
- The p6 prototype did not edit `test_perms_receipts_c4.py`. Its failure is the predicted O3 test, and the fix shape is in Conclusion step 3.
- `verification/explorer_FU_C_r2_3/probes/p6_supp_receipt_probe.txt` is a probe file with a synthetic `2099` time. It is labelled PROBE ONLY and is not a project receipt.

## 4. Conclusion: recommended fix strategy, ordered so that the first steps protect the outputs

1. **Protect first.**
   - Record the sha of verdict.json and of the 4 FU-C receipts.
   - Run `chmod a-w` on `results/topic2/2026-11-02_fu_c/{verdict.json,*sha256*.txt}`.
   - Never run `scripts/topic2fu_c_verdict.py` without `--out <verification path>`.
   - Run no mutation harness and make no mirrors before step 2: they would re-copy the literal.
2. **Edit by script, not by the Edit or Read tool**, since both print the literal into the transcript.
   - Use a python script that asserts the whole file has exactly one quoted `[1-9]\d{5}` literal, located on line 182.
   - Before writing, record per-line sha256 values of all lines except 182, plus the line count.
   - Replace with `"000000"`, write the file, and assert `new sha == 7b915eb7f19605c75903fb8da928a56381dc7781973e30edb2950097d2c078a4` (O5 prediction).
   - Do not seal a copy (L8).
3. **Fix the O3 test in place, keeping its name.** It calls `RC.build_context(D.REPO, code_receipt=<supplementary>)` and asserts:
   - the supplementary receipt's `verdict_code` and `result_handling` lines are byte-identical to the original;
   - the original receipt fails exactly on `{test_gate_and_records.py, test_perms_receipts_c4.py}`.
4. **Supplementary receipts** (new files; the old ones stay unedited):
   - `results/topic2/2026-11-02_fu_c/code_sha256_r2_c4fix.txt`, with a real current `# frozen_utc:` (never backdated), a `# supersedes:` header naming the 2 lines, and post-result labelling.
   - `output_sha256_r2.txt` for the changed docs and tests plus addendum 02.
   - A checker in a NEW test dir (e.g. `tests/topic2_fu_c_r2/`) that asserts, for each old receipt, that the set of failing lines equals the declared superseded set and that the new receipts fully verify.
5. **Verdict re-check without touching verdict code.**
   - Add a new wrapper, e.g. `scripts/topic2fu_c_verdict_r2check.py`, that passes `code_receipt=` and writes to `results/.../verdict_r2_recheck.json`. Never write to verdict.json.
   - Pre-declare in addendum 02 that the only leaf allowed to differ is `/receipts/code_receipt_utc`.
   - Confirm that verdict.json stays 4d793102….
6. **C4 scan extension** in the new test dir, covering:
   - `src/topic2_fu_c`, `tests/topic2_fu_c*`, `scripts/topic2fu_c_*`, `docs/.../2026-11-02_topic2_fu_c_*`, `results/topic2/2026-11-02_fu_c`, `verification/worker_FU_C_r*`.

   Requirements:
   - Hex-masked strict pattern (O8).
   - Exact allowlist: `perms_fu_c.json` key `nvox` only.
   - Synthetic positive controls built at runtime (e.g. `"9" * 6`, `"sub-" + "9" * 6`, `"9" * 6 + "_3T"`; 999999 is confirmed absent on B300), so the test file holds no 6-digit literal.
   - Plus a count-only B300 membership pass (stdin → `grep -cxF` against the 1,084 names) over every FU-C file and the worker's own metadata, with 0 hits required.
7. **Addendum 02** (`docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_addendum_02.md`). It must never quote the literal or the old line: `.md` files are auto-committed. It records:
   - the defect and why the r1 scans missed it;
   - old and new shas of the 2 test files;
   - that verdict-path files are unchanged, listing their shas;
   - that verdict.json predates the change and is unchanged;
   - the report §4 erratum;
   - the new reproduce commands;
   - the residual recoverability (L7) for root/PI to accept;
   - the transcript residual.

   Edit the result report minimally: a revision banner, the §4 sentence and the §6 reproduce block. Pin the result in output_sha256_r2. Put interpretive notes (the §2.2 stall overstatement, the NMSE ≈ 0.99 headroom caveat) in addendum 02, not as rewrites.
8. **Rerun.**
   - The full suites (FU-C, old 86, topic2_rgpool, topic1_lagmotif), C1, and all receipts with the declared supersessions.
   - The pinned mutation harness with OUT at a new path. Expect 55 / 51 killed / survivors baseline, V07c, V12, F11, as in r1.
   - The count-only git-history check (p1 method) once more.
   - 0 GPU-h.
9. **Scope.** Blocking class only, plus the scan extension. Optional nonblocking guard tests (X30 heterogeneous subjects; shape-only token test with `test_list` set to the bad tokens; receipt guards) go in the new dir. `verdict.py`, `receipts.py`, `logs.py`, the CLI and the card are not edited.

## 5. Verification method

- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` → rc 0.
- Prototype: `PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/explorer_FU_C_r2_3/probes/p6_fix_path_prototype.py $PWD /tmp/<x>/mirror <out.json>`. It must report `differing_leaves == ["/receipts/code_receipt_utc"]`, a single failing test (O3) and new sha 7b915eb7…. It is valid only while the repo test file is unedited; after the r2 edit, line 182 holds `000000` and the script's assert will stop it.
- After r2:
  - `sha256sum results/topic2/2026-11-02_fu_c/verdict.json` → 4d793102…;
  - the test file sha → 7b915eb7…;
  - the original code receipt fails on exactly the 2 declared lines;
  - p1 rerun → 0 standalone hits in FU-C paths.
- Invalidation: any change to the shas of `src/topic2_fu_c/{verdict,receipts,logs}.py` or `scripts/topic2fu_c_verdict.py`; any new or rewritten `verdict.json`; any `.md` or `.txt` containing a `[1-9]\d{5}` token that is a member of the B300 list.
