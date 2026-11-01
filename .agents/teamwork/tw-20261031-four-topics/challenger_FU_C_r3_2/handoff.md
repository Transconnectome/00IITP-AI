# Hard handoff — challenger_FU_C_r3_2 (FU_C iteration 3), 2026-11-01T23:15Z

Verdict: **CONFIRMED**. The FU-C headline, the freeze order, the verdict rule, the receipts and the C4 containment all hold under independent recomputation. No blocking defect. Nonblocking test gaps in the post-result C4 tooling are listed in §4.

## 1. Observation

- **Headline recomputed independently.** `verification/challenger_FU_C_r3_2/probes/recompute_verdict.py` uses numpy and scipy only, with no project imports. Over the 24 `runs/hcp_*_a1/run.json` files:
  - every pooled NMSE (Σnum/Σden) equals `test_nmse` to within 1e-12;
  - I1 = −0.1132 % [−0.4985 %, +0.2721 %] and I2 = +0.0083 % [−0.5200 %, +0.5366 %], df 7. The maximum absolute difference from the shipped `verdict.json` is 0.0 for both;
  - the rule gives `stop` with the qualifier "sign unresolved". The stalled runs (100-step loss never < 0.995) are C_s16 and S_s15, which matches the shipped stall table E0/C1/S1;
  - the sensitivity analysis keeps seeds 10–14 and 17 (df 5) and equals the shipped values.
- **Gate and pooled secondary.** `probes/gate_pool_recompute.out.json`:
  - all 12 r1 fixture run.json match their card-receipt pins;
  - F+ gains are +3.061 % and +2.935 %, so it passes; F− gain is −1.737 %, so it passes;
  - the pooled 13-seed I1 (df 12) equals the shipped value exactly.
- **Freeze order:**
  - card receipt `# frozen_utc: 2026-11-01T16:13:23Z`; card file mtime 16:13:03Z; card sha is `fc2d0672…cb` and still verifies;
  - `slurm/jobs.json`: the only job submitted before the freeze is the disclosed anchor job 501 at 16:04:50Z. The first Stage-1 submission was 16:13:51Z;
  - the earliest run `start_utc` is 16:35:12Z;
  - the code receipt `frozen_utc` is 16:31:53Z, before the first run end at 17:01:06Z (run.json mtimes are preserved);
  - git `e5fa8de` (16:20:26Z) holds the worker_FU_C_r1 progress line "CARD FROZEN … fc2d0672…". The card bytes themselves were never committed (`git log --all` on the card path is empty).
- **Verdict reproduction:**
  - `scripts/topic2fu_c_verdict_r2.py --out verification/challenger_FU_C_r3_2/probes/verdict_r2_repro.json` returns rc 0, byte-identical (`cmp`), sha 4d7931025c4fb9a2b6605394c7e47125cf472bf6b4e85f045a10c373ae4780f5;
  - the frozen CLI returns `no_verdict` with exactly two problems, the retired pin (missing) and the repaired pin (changed).
- **Receipts.** `scripts/topic2fu_c_check_receipts_r2.py` gives ok true:
  - card 36/0, code 15/2 (lines 13 and 16), presentation 1/0, output 160/3 (lines 141, 162 and 164), r2 27/0, r3 20/0;
  - every `failing_equals_declared` is true;
  - `sha256sum -c` gives 0 failures on output_sha256_r2 and output_sha256_r3.
- **C1.** rc 0, 67 OK.
- **Suites:**
  - tests/topic2_fu_c: 210 passed;
  - old suite (STRICT_E2E=1): 86 passed;
  - tests/topic2_rgpool (CUDA hidden): 116 passed;
  - tests/topic1_lagmotif: 88 passed.
- **Layout.** `audit_layout.py` on the run root gives rc 0, 685 files, 0 findings.
- **Ledger.** The completed FU-C rows sum to 10.697 GPU-h (worker_FU_C_r1 10.422, explorers 0.262, challenger_r1_1 0.013), within the 13 GPU-h cap.
- **r3 artifact shas.** All 9 I checked equal the worker's claims: c4scan_strict d52c2aec…, test_r3_guards 59b5fb41…, check_c4_r3 e8f6de08…, write_receipt_r3 94ce2671…, addendum_03 84f7a98f…, output_sha256_r3 5512a190…, card, verdict.json, verdict.py.
- **C4, independent count-only recount.** `probes/independent_c4_count.py` is my own code. It reads the sealed original into memory only and prints counts and booleans only.
  - The sealed sha matches the seal receipt, and the retired path is absent.
  - Working tree (26,173 files): identifier-context hits 0; near-copies at ≥ 20 % and ≥ 30 % line overlap: 0.
  - Near-copies at ≥ 10 %: 3 files. These are tests/topic2_fu_c/test_evaluate_records_r2.py (a sibling test sharing boilerplate) and two auditor mutant copies of it. None holds the literal.
  - Any-context occurrences: 1 file. It is outside every FU-C path and holds 0 identifier-context occurrences. This is consistent with the residual already pending in GATE_STATUS.
  - Git blobs (2,224): every count is 0.
- **C4, rerun of the worker's check script.** `scripts/topic2fu_c_check_c4_r3.py --b300` now gives rc 0, ok true.
  - Worktree 25,442 files and blobs 2,222: every exposure count is 0.
  - B300 membership: production 217 files / 128 runs, verification 477 / 113 (includes my folder and the peers' folders), metadata 106 / 8. Every group has 0 member hits.
  - Controls: positive 1, negative 0, 1,084 names.
- **No exposure paths in the FU-C scope:**
  - 0 FU-C path components contain a 6-digit run (262 scope paths; 555 verification and metadata FU_C paths);
  - 0 repo symlinks resolve into the sealed store;
  - 0 files with NUL bytes;
  - the only skipped binary is perms_fu_c.npz, which holds int64/bool arrays, 0 string arrays and 0 ASCII 6-digit runs.
- **Own mutation harness.** `verification/challenger_FU_C_r3_2/mutants/run_mutants_ch2.py` uses 38 fresh mutants that I wrote, not taken from the worker's tables. It deselects the same 5 hash tests (baseline 205 passed). Results are in `mutants_ch2.out.json`: 26 killed, 12 survived, 0 invalid.
  - verdict.py V01–V10 (df check, strict stop bound, qualifier bound, attempts, negative num, nmse tolerance, gate seed, freeze-order comparison, sensitivity n, pooled r1 seeds): all killed.
  - supersession and the r2 driver P01–P03 and D01: all killed.
  - Survivors: S05 (digest left bound dropped), S06 (mask with digits), S07 (hex run not extended right), S09 (line text from masked source), S10 (strict line number off by one), K02 (`after[1:].isdigit()` dropped), K07 (≥ NEAR → > NEAR), K08 (main ok ignores the exposure counts), K09 (main ok ignores blob near-copies), K10 (B300 metadata group emptied), K11 (worktree walk skips verification/), V11 (duplicate-completed check loosened).
- **Scanner attacks.** `probes/strict_scanner_attacks.py` builds a synthetic token at run time and outputs booleans only.
  - Strict flags both c4scan blind spots: a '.'-preceded run after a letter, and a run inside a 20-hex string.
  - Neither scanner flags:
    - a run after a digit + '.' (as in v1.TOKEN);
    - a run inside a 32-, 40- or 64-hex token;
    - full-width digits, digits separated by spaces, commas or underscores, \u escapes, HTML entities, base64 or hex encoding;
    - UTF-16 files and .gz files;
    - a token that appears only in a file NAME;
    - files under a symlinked subdirectory.

## 2. Logic chain

1. The primary is recomputed from raw per-subject num/den with independent code and agrees to 0.0. So the shipped numbers are not an artefact of `src/topic2_rgpool/stats` or of the verdict layer (Obs 1).
2. The card §5 rule with upper bound +0.272 % < δ 1 % gives `stop`. The lower bound is ≤ 0 and the upper bound is ≥ 0, so the qualifier "sign unresolved" is correct. The F+ gate passes, so `inconclusive` does not apply. Stalls are valid runs in the primary (§6), and the sensitivity analysis is descriptive only. So the verdict follows the card (Obs 1–2).
3. The card freeze precedes every Stage-1 submission except the disclosed anchor. The code pin precedes every run end, and run.json mtimes are later than the code pin. So the result-access rule of §8 is not contradicted by the timestamps. The independent git anchor covers only an 8-hex prefix in a progress note, not the card bytes; addendum 03 §9 states this limit correctly (Obs 3).
4. Receipts fail on exactly the 5 declared lines, and r3 adds no supersession. So iteration 3 is additive, as claimed (Obs 4).
5. My own C4 recount and the rerun of the worker's script both give 0 identifier-context exposures and 0 recoverable near-copies in the working tree and git, and 0 B300 member hits including my own files. So containment holds now (Obs 5–6).
6. All 10 non-equivalent verdict-path mutants I wrote are killed. So the F2 verdict-code testing requirement holds for fresh mutants as well as for the worker's union table. V11 is equivalent: with two completed attempts, `done[0] is not lst[-1]` still raises "an attempt follows a completed run".
7. The survivors are confined to post-result, non-governing C4 tooling. Their failure modes cannot change the verdict. They can only weaken a future C4 check, and the current output counts were checked independently (step 5). So they are nonblocking test gaps, not defects in shipped results.

## 3. Caveats

- I did not re-evaluate checkpoints on B300; I used 0 GPU-h. challenger_FU_C_r1_1 did this earlier (job 577, 6/6 bitwise). My recompute starts from the saved run.json files, not from model weights.
- I did not compare `/scratch/iitp4/fu_c` on B300 against the repo copies.
- The independent recount uses the sealed original in memory (the same input as the worker's script). Any C4 recount necessarily depends on it.
- The 10 % near-copy threshold is my own sensitivity choice. The ≥ 10 % hits are boilerplate in a sibling test.
- Equivalence arguments for S06, S09, S10 and K07 are by reasoning, not proof. S06: an all-'1' run of 32 or more digits cannot hold a bounded 6-digit run. K07 differs only at exactly 30 %.
- **Deviations:**
  - DISPATCH.md summarises the worker's embedded handoff JSON rather than copying it verbatim. It points to the worker's own handoff.md.
  - The mutant mirrors ran in the session scratchpad (`…/scratchpad/ch2_work`, removed after the run), not under verification/challenger_FU_C_r3_2/. They held copies of code and tests only, and results/docs were symlinked.
  - My first background launch of the C4 rerun exited without output. I reran it in the foreground task (rc 0).

## 4. Conclusion

**CONFIRMED.** FU-C card §5 verdict `stop`, I1 −0.113 % [−0.499 %, +0.272 %], df 7, δ 1 %, qualifier "gain below δ, sign unresolved", reading "r1 stop replicated on 8 independent training seeds". It is reproduced from raw outputs by independent code, follows the card rules, and was frozen and pinned before any result. Iteration 3 is additive. C4 containment holds, with 0 exposures confirmed by an independent recount.

Nonblocking items, for root and the next maintainer:
1. **Untested aggregation in `scripts/topic2fu_c_check_c4_r3.py`.**
   - `main()`'s `ok` and exit code ignore the exposure counts when they are mutated (K08, K09), and `worktree_files` scope is untested (K11, skipping verification/ survives). This matters because the near-copy lived in verification/.
   - The handoff's "rc 0, ok true" evidence therefore rests on the printed counts, which I verified, not on a tested exit-code rule.
   - Mitigation: a tmp-root test that plants an exposure and asserts rc 1, and a walk test over a nested verification/ dir.
2. **K02.** A sentence-final '.' after the literal is not pinned as identifier context by any test. The current code is correct. Mitigation: add a case of TOKEN followed by '.' and a space.
3. **S05/S07 (strict scanner).** No test covers a hex run longer than a digest, or an enclosing hex run that continues past a matching prefix. Add both.
4. **Scanner scope limits, now confirmed empirically:**
   - file and directory names are never scanned by c4scan or c4scan_strict, and check_c4_r3 checks only the retired stem;
   - symlinked subdirectories are not walked;
   - UTF-16 and .gz content is not read;
   - digest-shaped tokens and digit-'.' separators are skipped.
   The current FU-C scope has 0 such paths and files, but a future name-only leak would go undetected. Addendum 03 §10 item 3 covers encodings but not file names or symlinks.
5. **Addendum 03 counts.** The §3 table gives pre-run counts (23,434 files / 2,174 blobs; 199 files / 118 runs), while the handoff gives final counts (27,031 / 2,189; 128 runs). §3 says the final rerun "is in §8", but §8 gives no counts and only points to the handoff. This is a documentation inconsistency only.
6. **Freeze-order git anchor.** The card bytes were never in git. The anchor is a 32-bit sha prefix inside a daemon-committed progress note. That is weak against deliberate forgery but consistent with every timestamp. Addendum 03 §9 states the limit.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 python3 -B verification/challenger_FU_C_r3_2/probes/recompute_verdict.py $PWD      # diff vs shipped 0.0
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py                   # ok true
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json         # byte_identical true
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. timeout 900 python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q   # 210 passed
PYTHONDONTWRITEBYTECODE=1 python3 -B verification/challenger_FU_C_r3_2/mutants/run_mutants_ch2.py $PWD <work-dir-outside-verification/worker_FU_C_r*> out.json 2
PYTHONDONTWRITEBYTECODE=1 python3 -B verification/challenger_FU_C_r3_2/probes/strict_scanner_attacks.py $PWD
```

Invalidation: any change to a run.json, verdict.json, the card or a receipt; a nonzero exposure count in a rerun of `independent_c4_count.py` or `topic2fu_c_check_c4_r3.py`; or a killed-mutant count that falls below 26 with this harness.

Evidence files: `verification/challenger_FU_C_r3_2/{probes/*, mutants/{run_mutants_ch2.py, mutants_ch2.out.json, mutants_ch2.log}, logs/*}`.
