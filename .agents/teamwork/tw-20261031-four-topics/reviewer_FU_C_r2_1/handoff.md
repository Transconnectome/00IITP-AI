# Handoff (hard) — reviewer_FU_C_r2_1, FU-C gate round r2

**Verdict: REQUEST_CHANGES.** There is one blocking issue, and it needs a root/owner action outside the worker's paths. Everything the worker delivered checks out independently. Written 2026-11-01T21:22Z. No GPU was used, no ledger rows were added, and no git writes were made.

## 1. Observation

All commands were run from `/home/juke/git/00IITP-AI`. Logs and probes are in `verification/reviewer_FU_C_r2_1/`.

**C1 and test suites**
- C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` returned rc 0 (67/67 OK) at both the start and the end (`c1_check.log`).
- FU-C receipts, checked with `grep -v '^#' <r> | LC_ALL=C sha256sum -c`:

  | receipt | OK / total |
  |---|---|
  | card_sha256.txt | 36 / 36 |
  | code_sha256_presentation_before_results.txt | 1 / 1 |
  | output_sha256_r2.txt | 27 / 27 |
  | code_sha256_before_results.txt | 13 / 15 |
  | output_sha256.txt | 157 / 160 |

  The failures are exactly the declared lines: code 13 (missing) and 16 (changed); output 141 and 164 (changed) and 162 (missing). `scripts/topic2fu_c_check_receipts_r2.py` returned rc 0, with `failing_equals_declared` true for every receipt (`check_receipts_r2.json`).
- pytest (timeout 900, nice, at most 2 at a time):

  | suite | result | log |
  |---|---|---|
  | tests/topic2_fu_c | 180 passed | pytest_fu_c.log |
  | old suite (STRICT_E2E=1) | 86 passed | pytest_old.log |
  | tests/topic2_rgpool | 116 passed | pytest_topic2_rgpool.log |
  | tests/topic1_lagmotif | 88 passed | pytest_topic1_lagmotif.log |

**Verdict reproduction**
- `scripts/topic2fu_c_verdict_r2.py --out verification/reviewer_FU_C_r2_1/verdict_r2_repro.json` returned rc 0, `context_problems: []`, and output byte-identical to the shipped `verdict.json` (`cmp` OK; sha 4d7931025c4f…80f5).
- The frozen CLI with `--out` into my directory returns `no_verdict` with exactly the 2 declared problems (`frozen_cli_now.json`). This is the declared, by-design behaviour.
- I recomputed the statistics independently from the raw `runs/hcp_*_a1/run.json` files, without importing FU-C code (`probes/indep_stats.py` and `.out.json`):
  - provenance: 24/24 completed; 24/24 test tokens of the form `h\d{2}`; 24/24 test_nmse equal to Σnum/Σden; 24/24 start_utc after the card freeze;
  - I1 = −0.1132 % [−0.4985 %, +0.2721 %], df 7, so `stop`, qualifier "sign unresolved";
  - I2 = +0.0083 % [−0.520 %, +0.5366 %];
  - stall-dropped sensitivity: I1 +0.040 % [−0.2126 %, +0.2925 %].
  All of these equal `verdict.json`.
- The addendum 02 §6 numbers reproduce:
  - without seed 16: sd 0.220 % and half-width 0.204 %;
  - δ is 85.4 % of the learned signal 0.01158, and the I1 upper bound is 23.2 % of it.

**Mutation union and own mutant**
- The union harness, rerun into my directory, gave 150 entries, 146 KILLED, 0 INVALID and 5 deselected. The survivors are the baseline, V07c, V12 and F11 (`mutants_rerun.out.json`), the same as the worker's result.
- My own mutant, `check_receipts` ignoring the declared-vs-failing comparison, is killed only by the r2 hash pin on `supersession.py`, not by behaviour (it was run in mirrors, which I have since removed).

**C4**
- The retired file is absent from the repo, and its path occurs in 0 git commits (`git log --all -- <path>`).
- I recovered the literal in memory, from in-repo content only. It occurs in 0 of 2,091 reachable git blobs (`probes/literal_footprint.out.json`).
  - In the working tree it occurs in 3 untracked Topic-1 `.jsonl` files, as the integer part of a float measurement value: the window is `"dddU": <LIT>.ddd`, with digits masked (`probes/literal_context.out.json`). This is a numeric coincidence, not an identifier context.
- Broad B300 membership check (`probes/membership_broad.out.json`): every maximal 6-digit run in the FU-C production paths (170 files), all `verification/*FU_C*` directories (912 files) and all `*FU_C*` metadata (65 files) was checked against the 1,084 staged HCP-YA names. It found 0 member hits in each scope. The controls were valid (positive 1, negative 0). Tokens went over ssh stdin only, and only counts were printed.
- **Blocking:**
  - The file `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` is still present at 21:21Z. It is untracked and was never committed.
  - It has 1 six-digit slot. Substituting values into that slot until the sha256 equals the pin in `code_sha256_before_results.txt` line 13 recovers the original bytes, and so the real HCP-YA ID, in well under 1 s (`probes/recoverability.out.json`: `recovered_original_bytes: true`).
  - No other working-tree file shares ≥ 30 % of its 169 long lines (`probes/near_copies.out.json`, 27,021 files).
- The sealed store is mode 0700 (directories) and 0400 (file); I checked metadata only. `c4_sealed_originals_sha256.txt` verifies (1/1).

**Other checks**
- Ledger: the FU-C worker plus explorers total 10.684 GPU-h (cap 13), and there are 0 rows from r2.
- `audit_layout.py` on the whole run root returned rc 0 with 0 findings (`audit_layout.log`), and flake8 is clean.

## 2. Logic Chain

1. The verdict-path files (`verdict.py`, `logs.py`, `receipts.py`, the CLI) still match their pre-result pins (13 OK lines of the code receipt include all `verdict_code` and `result_handling` pins). The card and its governing inputs verify (36/36).
   - The derived view removes only two `tests`-section pins and reproduces `verdict.json` byte-for-byte. My code-independent recomputation gives the same numbers.
   - So the scientific verdict `stop` (F3) is unchanged and correctly reproduced. The supersession is declared, mechanically checked and not hidden.
2. The r1 blocking class was a real HCP ID literal in `tests/`. The worker's handling of the production paths is complete:
   - the literal is in 0 git blobs;
   - there are 0 HCP-ID members in any FU-C scope;
   - the file is retired and sealed;
   - the report claim is corrected;
   - a strict tripwire with run-time controls exists.
3. The worker chose to retire the file instead of editing it in place for one reason: an in-place-edited copy plus the old sha (kept in receipts that may not be edited) lets the literal be brute-forced.
   - The peer near-copy is exactly that. My attacker-model probe recovered the bytes from in-repo content alone.
   - Run precedent counts recoverability as a C4 failure: the M3 r1 gate failed on recoverable tokens, and the M3 r2 gate failed on the dev-salt in an explorer `verification/` directory, with T2.4 requiring that "no repo content lets HCP IDs be recovered".
   - So C4 is not yet met for the FU-C footprint, although the cause is outside the worker's ownership.
4. Every other criterion is met with evidence (C1, C2, C3 via addenda without card edits, C5, C6, C7, C8 with numbers from `verdict.json` only, F1–F3). The single blocker is therefore narrow, and closing it is cheap.

## 3. Caveats

- I did not rerun any GPU work or re-evaluate checkpoints. The r1 verifiers did that (for example challenger_FU_C_r1_1's job 577), and r2 changed no science.
- I read no sealed-store content. I recovered the literal in memory from the in-repo near-copy, which is the attacker model under test.
- **Self-incident (disclosed).** My first recoverability probe printed a loop counter that, with a single slot, encodes the value. It appeared once in this session's tool transcript and in `verification/reviewer_FU_C_r2_1/probes/recoverability.out.json` for about 1 minute. That file was then rewritten without the field (`grep -c '"n_tried"'` gives 0) and the script was fixed.
  - The file is an untracked `.json`, and the daemons commit `.md` and `.txt` only.
  - The transcript copy is outside repo scope, in the same class as the worker's residual 3.
  - No value is restated anywhere.
- The worker's "literal in 0 repo files (24,059 text files)" differs slightly from my 3 working-tree hits. Theirs is a narrower scan; mine counts any digit-bounded occurrence. The 3 hits are coincidental float values, not IDs.
- `c4scan` limits (nonblocking):
  - SIX skips a 6-digit run preceded by `.`, so a shape like `x.NNNNNN` is missed;
  - an ID inside a hex run of 8 or more characters that contains a letter is masked.
  The broad membership check covers both gaps for current content.

## 4. Conclusion

**REQUEST_CHANGES.**

**Blocking B1 (root or owner action; no worker code change):**
- Remove or seal `verification/explorer_FU_C_r2_2/tree/` (at least `tests/topic2_fu_c/test_gate_and_records.py`), preferably the whole tree plus `mut_work/` and `code_receipt_subset_derived.view`.
- Seal it off-repo first if its bytes are needed as evidence.
- Then rerun the closure check in §5.

**Nonblocking:**
- N1: `supersession.check_receipts`' comparison has no behavioural test on a synthetic root with an undeclared failing line; only the r2 hash pin guards it.
- N2: the `c4scan` shape gaps listed in §3.
- N3: three untracked Topic-1 `.jsonl` files contain the same digit string as a float's integer part. This is coincidental; for the record only.
- N4: result report §2 item 2 still carries the overstated stall explanation. It is corrected in addendum 02 §6.2 and the banner points there, which is acceptable.

Everything else (verdict `stop`, receipts supersession, tests, mutation evidence, compute, documentation) is verified and can be approved once B1 is closed.

## 5. Verification Method

- Closure of B1: `test ! -e verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py`. Then rerun `python3 -I verification/reviewer_FU_C_r2_1/probes/near_copies.py <REPO> <reference>`, using as the reference a copy that root holds off-repo (the sealed file, read in memory). The expected result is no near-copies.
- Also run `find verification .agents -name 'test_gate_and_records.py*'`; the expected result is empty.
- Regression: rerun every command in §1. Expected: C1 rc 0; 180/86/116/88 passed; `check_receipts_r2` ok; `verdict_r2` byte-identical; mutation union 146 killed with 3 equivalent survivors.
- Invalidation conditions:
  - any change to `verdict.json`, the card, the verdict-path files or the pre-result receipts;
  - any FU-C scope membership hit greater than 0;
  - any new near-copy of the retired file.
