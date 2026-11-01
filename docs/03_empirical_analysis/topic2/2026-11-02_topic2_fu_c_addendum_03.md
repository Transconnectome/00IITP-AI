# Topic 2 FU-C — addendum 03 (iteration 3): C4 containment record, erratum, additive guards

Dated 2026-11-02 (KST); written by worker_FU_C_r3 (run tw-20261031-four-topics, workflow C). Post-result and
non-governing. It changes no rule, number, verdict or reading. The frozen card
(`2026-11-02_topic2_fu_c_card.md`), the result report, addenda 01–02, every pre-result receipt,
`output_sha256_r2.txt` and every file they pin are byte-unchanged. New files only; they are pinned in
`results/topic2/2026-11-02_fu_c/output_sha256_r3.txt`.

## 0. Verdict (unchanged)

Card §5 verdict: **stop**. I1 = −0.113 % [−0.499 %, +0.272 %], t interval with df 7, δ = 1 %. Qualifier: "gain below
delta, sign unresolved". Card §11 reading: the r1 stop is replicated on 8 independent training seeds.

Reproduced in iteration 3 with `scripts/topic2fu_c_verdict_r2.py --out verification/worker_FU_C_r3/verdict_r2_repro.json`:
rc 0, `context_problems` [], output byte-identical to the shipped `verdict.json`
(sha256 4d7931025c4fb9a2b6605394c7e47125cf472bf6b4e85f045a10c373ae4780f5; `cmp` identical). The frozen CLI
(`scripts/topic2fu_c_verdict.py --out verification/worker_FU_C_r3/frozen_cli_now.json`) still returns `no_verdict`
with exactly the two declared superseded test pins, by design (addendum 02 §4). 0 GPU-h were used in iteration 3 and
no ledger row was added.

## 1. What failed at the iteration-2 gate

All five r2 verifiers confirmed the worker's iteration-2 deliverables and failed the gate on one item outside the
worker's paths: a peer explorer's in-place-edited near-copy of the retired test file sat in that explorer's
verification folder. Together with the unchanged pre-result pin of the retired file (code receipt line 13, output
receipt line 162), it let the retired literal be recovered from repo content (C4). One r2 verifier probe output
also carried information about the literal; it was contained with the near-copy (§2). The gate record itself is
not reproduced here (root rule, ACCEPTANCE addendum "FU_C r2 near-copy containment").

## 2. Containment by root (record)

- Who and when: the root coordinator (Claude session 5fddb83e), 2026-11-02 about 06:43–06:45 KST
  (2026-11-01 about 21:43Z); recorded in `orchestrator/GATE_STATUS.md` ("FU_C r2 near-copy containment") and in the
  ACCEPTANCE addendum of the same name.
- What: `verification/explorer_FU_C_r2_2/{tree, mut_work, code_receipt_subset_derived.view}` and one probe output
  file in `verification/auditor_FU_C_r2_1/probes/`; 302 files in all, moved (not deleted). None was tracked or in git
  history (root's pre-move check).
- Where: `~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02/`, listed in its `MANIFEST.sha256`
  (302 lines; the manifest file's sha256 is
  5d907c38335f68176c8dfa7ea3cb1f13d8c7db98c595eb8a49e697044a595c1d at 2026-11-01T22:3xZ).
- Permissions, checked by this worker (metadata only): 302 files, 0 not mode 0400, 0 directories not mode 0700.
  This worker did not open, copy, mirror, diff or hash any sealed file other than the manifest itself.

## 3. Containment confirmed by this worker (count-only)

`scripts/topic2fu_c_check_c4_r3.py --b300` (output `verification/worker_FU_C_r3/probes/c4_check_r3_pre.out.json`,
rerun after all iteration-3 writes as `c4_check_r3_final.out.json`) reads the sealed original of the retired file
(the r2 seal at `~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/`) into memory only. It writes booleans and counts
only: no literal, digit, position, loop counter or timing.

| check | working tree (23,434 files, .git excluded) | git blobs (2,174, all refs) |
|---|---|---|
| sealed original matches its pre-result pin | true | — |
| retired path absent | true | — |
| files with the literal in an identifier context (digit-bounded, not part of a decimal number) | 0 | 0 |
| near-copies (≥ 30 % of the 160 long lines, raw or JSON-escaped) | 0 | 0 |
| files named after the retired file | 0 | — |
| files stating digit offsets of the literal (key or prose form followed by numbers) | 0 | 0 |
| files holding a sha256/sha1/md5 digest (full or 16-character prefix) of the literal or of a line containing it | 0 | 0 |

Three working-tree files larger than 50 MB were not content-scanned (a presentation video in the repo root, a zip
archive in `docs/00_task_description/raw/`, a Topic 1 derived `.npy` array); none is an FU-C file or a text file.

B300 count-only membership pass (CPU only, no Slurm, no GPU; tokens over ssh stdin, a count back): every maximal
6-digit run in the FU-C production paths (199 files, 118 unique runs), every `verification/*FU_C*` folder (339
files, 88 runs) and every FU-C agent metadata folder (87 files, 8 runs) against the 1,084 staged HCP-YA names:
0 member hits in each group; positive control 1, negative control 0 (valid). The final rerun after all r3 writes is
in §8.

## 4. Erratum to the iteration-2 headline

The iteration-2 worker headline said iteration 2 "closes the C4 blocking class". That overstated the state at the
time: the class was closed in the worker's own paths, but the peer near-copy (§1) still made the literal
recoverable until root's containment (§2). The class is closed in the repo working tree from 2026-11-01 about
21:43Z, as confirmed in §3. The iteration-2 worker did disclose the near-copy as a gate-relevant open issue.

## 5. Additive iteration-3 files

| file | role |
|---|---|
| `src/topic2_fu_c/c4scan_strict.py` | stricter shape scanner (§6); not imported by the verdict path |
| `tests/topic2_fu_c/test_r3_guards.py` | 30 behaviour-only tests on synthetic tmp roots, plus one content-only strict scan of the real FU-C scope |
| `scripts/topic2fu_c_check_c4_r3.py` | count-only containment check of §3 |
| `scripts/topic2fu_c_write_receipt_r3.py` | writes `output_sha256_r3.txt` |
| `verification/worker_FU_C_r3/` | evidence: mutation harness and outputs, C4 check outputs, verdict reproduction, test logs |

The new tests close the iteration-2 surfaces that r2 challengers showed were guarded only by hash pins:
`supersession.line_status` and `check_receipts` (OK/CHANGED/MISSING statuses; failing set equal to, not a subset
of, the declaration; undeclared failing lines and undeclared receipts fail; an absent declared receipt fails; only
the named off-repo receipt is skipped; the declaration equals the addendum 02 §3 table; the checker's exit code),
`reproduce_verdict` (feeds the derived view, not the default receipt; fails closed to `no_verdict` with the
problems kept when the context has a problem), the r2 driver loaded with `ROOT` at a tmp root (refuses the shipped
path and a symlink alias to it without computing; `byte_identical_to_shipped` and the exit code follow the bytes),
and `c4scan` controls built at run time (every leading digit 1–9, letter-led BIDS-style labels, the 8-character
hex-mask threshold, every declared scope including nested folders, and the documented '.'-preceded limit). They
also test the pure functions of the §3 check script (decimal-context exclusion, raw and JSON-escaped overlap, a
full-space recoverability test, and every exposure count of the sweep).

## 6. c4scan limits and the strict scanner

`c4scan.py` is pinned in `output_sha256_r2.txt` and is not edited. Its two blind spots stay as documented limits:
a 6-digit run preceded by '.' is read as a decimal fraction even when the '.' is a separator, and a 6-digit run
inside a hex run of 8 or more characters that contains a letter is masked as a hash. `c4scan_strict.py` closes
both: a '.'-preceded run is a fraction only when a digit precedes the '.', and only complete digest tokens (32, 40,
64 or 128 hex characters) are masked. Its false positives inside short sha prefixes are classified by meaning:
`sha_prefix_allow` accepts digits whose enclosing hex run (8 or more characters) is a prefix of a digest pinned in
an FU-C or r1 receipt. Over the real FU-C scope it finds exactly two shape hits before classification, the
allowlisted group-mask voxel count and one written prefix of the shipped `verdict.json` digest in addendum 02, and 0
after classification (`test_strict_scan_of_every_fu_c_path_finds_only_classified_tokens`). The count-only B300
membership pass over maximal digit runs (§3) remains the catch-all for both scanners.

## 7. Mutation evidence

MUTATION_SECTION

## 8. Receipts, suites and final checks

FINAL_SECTION

## 9. Freeze-order git anchor

The card and receipts are untracked, so r2 verifiers noted that the freeze order rested on receipts and mtimes
only. Daemon commits of agent progress notes give an independent git anchor:
- commit `e5fa8de` (committed 2026-11-01T16:20:26Z) contains the worker_FU_C_r1 progress line "16:13:23Z CARD
  FROZEN … sha fc2d0672…", before the first Stage-1 start (16:35:12Z);
- commit `cd1e43e` (committed 2026-11-01T16:35:27Z) contains the line "16:31:53Z verdict code + tests pinned …
  No Stage-1 job had started", before the first Stage-1 end (17:01:06Z).
The full `verdict.py` sha first appears in git only after the results; the anchor covers the card's sha prefix and
the code-pin statement, not the full code pins.

## 10. Residuals for root or PI acceptance

1. Committed FU-C r1/r2 agent handoffs describe the literal in words that narrow which public value it is. They
   state no value or digit, and removing them needs a git history rewrite; GATE_STATUS records this as pending a PI
   decision. Iteration 3 repeats none of those descriptions.
2. Copies of the literal in agent transcripts outside the repo are outside repo scope.
3. The near-copy test compares long lines; a reformatted or encoded copy would escape it. Membership was checked only
   against the 1,084 staged names, which is not proof that a token is not an HCP ID.
4. Mutants that survive are listed in §7 with their equivalence argument.

## 11. Reproduce

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py
grep -v '^#' results/topic2/2026-11-02_fu_c/output_sha256_r3.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/fu_c_verdict_check.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/topic2fu_c_check_c4_r3.py --out /tmp/fu_c_c4.json --b300
```
Never run `scripts/topic2fu_c_verdict.py` or `scripts/topic2fu_c_verdict_r2.py` without `--out`.
