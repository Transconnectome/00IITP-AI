# Handoff (hard) — challenger_FU_C_r3_1, FU_C iteration 3

**Verdict: CONFIRMED.** The worker's claims hold when I run them myself. Nothing I found changes the shipped verdict or the C4 counts. Several findings are nonblocking and are listed under Caveats and Conclusion.

0 GPU-h used, no ledger rows, no git writes, no production file touched. Evidence is in `/home/juke/git/00IITP-AI/verification/challenger_FU_C_r3_1/`.

## Challenge summary

Overall risk: **LOW**.
- The verdict is robust: I recomputed it independently and got a byte-identical result.
- C4 holds by count-only checks.
- The r3 test surfaces still have behavioural gaps. They are in post-result, non-governing tools, and they hide nothing in the current tree.

## 1. Observation

1. **C1.** `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gave rc 0 (67 lines) at the start and again at the end.
2. **Receipts.** `scripts/topic2fu_c_check_receipts_r2.py` gave ok true, rc 0:
   - card 36/0, code 15/2, presentation 1/0, output 160/3, `output_sha256_r2` 27/0, `output_sha256_r3` 20/0;
   - the failing lines are exactly code 13 and 16, and output 141, 162 and 164.

   The 14 artifact shas the worker claimed all verify (`worker_claimed_shas.txt`, 0 failures).
3. **Independent recomputation.** I wrote `probes/recompute.py` with no project imports: scipy t quantile, NMSE as Σnum/Σden, and my own stall parser, gate, provenance and freeze checks. Output: `probes/recompute.out.json`.
   - I1 = −0.1132 % [−0.4985 %, +0.2721 %] and I2 = +0.0083 % [−0.5200 %, +0.5366 %], df 7. The difference from `verdict.json` is 0.0 for every field.
   - Rule gives `stop`, with the qualifier "sign unresolved".
   - Stalled runs are {C_s16, S_s15}. Dropping their seeds leaves 10, 11, 12, 13, 14, 17; the df 5 interval still gives `stop`.
   - r1 gate: F+ E−C +3.06 % and S−C +2.93 % (pass); F− E−C −1.74 % (pass).
   - Provenance: the perm sha of all 10 keys equals the card §3.3 table, both from the array bytes and from the run.json files. The npz and split shas match. Settings match. There is one test order, and it equals the split.
   - Freeze order: first start 16:35:12Z and last start 19:08:03Z, both after the card freeze (16:13:23Z) and after the code pin (16:31:53Z). First end is 17:01:06Z.
   - The per-seed rows of the result report table match the run records, and the r1 I1 citation matches the r1 `verdict.json`.
4. **Verdict reproduction.** `scripts/topic2fu_c_verdict_r2.py --out probes/verdict_r2_repro.json` gave rc 0, byte-identical (cmp), sha 4d793102…80f5. The frozen CLI `--out` gave `no_verdict` with exactly the 2 declared superseded test pins.
5. **Git freeze anchor.**
   - `e5fa8de` (2026-11-02T01:20:26+09:00 = 16:20:26Z) contains the line "16:13:23Z CARD FROZEN … sha fc2d0672…".
   - `cd1e43e` (16:35:27Z) contains "16:31:53Z verdict code + tests pinned … No Stage-1 job had started".
   - Both match addendum 03 §9.
6. **Suites.** tests/topic2_fu_c 210 passed; old suite (STRICT_E2E=1) 86 passed; topic2_rgpool 116 passed (CUDA_VISIBLE_DEVICES=''); topic1_lagmotif 88 passed. Logs are `suite_*.log`.
7. **Worker mutation harness rerun** (`worker_harness_rerun/`): 222 entries, 217 killed, 0 invalid. The survivors are the baseline, V07c, V12, F11 and CR2:C10, which reproduces the claim. All 26 named r2-challenger survivors are KILLED.
   - I checked the CR2:C10 equivalence argument and agree: masking an all-digit run of 8 or more characters cannot change the one-character lookarounds of a bounded 6-digit run.
8. **My own mutants** (`mutants/run_mutants_c1.py`, 19 mutants, baseline 205 passed with 5 deselected): 7 killed, 12 survived, 0 invalid. Survivors:
   - `c4scan_strict`:
     - X01: the prefix allow matches only the first 8 characters of the run;
     - X02: the allowlist matches by value instead of by (path, token);
     - X03: the sha512 alternative is not masked;
     - X04: comma-adjacent runs are treated as decimals, which hides `[1,<id>]`;
     - X05: the right boundary of DIGEST is dropped.
   - `check_c4_r3`:
     - Y01: git blobs are taken from HEAD only, not `--all`;
     - Y02: the B300 controls are ignored in `ok`;
     - Y03: `recoverable` tests only the first 6-digit run;
     - Y05: MAX_BYTES is lowered to 1 MB;
     - Y06: `retired_literal_among_runs` is ignored in `ok`.
   - `verdict.py`:
     - W04: the descriptive `I2_lower_gt_0` flag uses ≥;
     - W08: the gate code pins are compared as a subset, so extra keys are accepted.

   `probes/scanner_adversarial.py` runs on the unmutated code and shows that X01, X02, X04 and Y03 are behaviourally real, not equivalent. Each mutant would accept or hide an input that the shipped code flags.
9. **Adversarial shapes on the shipped scanners.**
   - The strict scanner misses five shapes: a 6-digit run after "digit.", such as `rest1.<id>`; full-width digits; an ID split by a newline; base64; and an ID padded by hex to exactly 64 or 128 characters.
   - c4scan additionally misses runs next to hex letters and the exponent form. These are the blind spots the strict scanner was added to close.
10. **C4 rerun.** I reran the worker's `scripts/topic2fu_c_check_c4_r3.py --b300` (`c4/c4_check_rerun.out.json`): ok true.
    - Working tree: 26,324 items, of which 3 were skipped as large. Git blobs: 2,199. Every exposure count is 0, and there are no near-copies.
    - B300: 0 member hits in each of the three groups (production: 217 files, 128 runs; verification: 409, 113; metadata: 103, 8). Controls: 1084 names, positive 1, negative 0.
11. **Blind spot of the literal check.** `identifier_context_count` skips by design any occurrence next to a '.' that has a digit on its other side. I ran count-only probes:
    - `c4/decimal_context_count.out.json`: the literal is bounded in 1 working-tree file, in exactly such a context, and in 0 git blobs. Unbounded substrings occur in 31 files, which is within the range of 40 random control values (13–68, median 24; `c4/decimal_context_classify.out.json`).
    - That file is outside every FU-C path and not tracked in git.
    - `c4/description_recoverability.out.json`: among all values in that file that the same check excludes, more than one is a staged HCP-YA name (controls valid). So that file plus the staged list does not single out the literal.
12. **Ledger and layout.**
    - FU-C completed GPU-h = 10.697 (cap 13), and there is no r3 row.
    - `audit_layout.py` over the whole run gives PASS with 0 findings.
    - A strict scan of my own two folders finds 0 hits. They hold 6 unique 6-digit runs, all inside full digests, with 0 B300 member hits.

## 2. Logic chain

1. Obs 3 and 4 show that the shipped numbers and verdict follow from the raw records through the card's §5 rules.
   - My code shares no line with the project's statistics, so a shared bug is unlikely.
   - The upper bound of +0.272 % is far below δ = 1 %, so `stop` does not hinge on a boundary.
   - The stall sensitivity agrees.

   The verdict is therefore CONFIRMED.
2. Obs 3 and 5 show that the card was frozen before any run started, and the code was pinned before any run ended or was read.
   - The receipts (Obs 2) still verify, apart from the declared supersession.
   - The git anchor gives a commit-time witness for both statements, but for the card only as a sha prefix.
3. Obs 7 reproduces the worker's mutation claim exactly.
4. Obs 8 shows that the r3 suite does not pin several rules of the new r3 tools.
   - These tools are post-result and non-governing. The C4 evidence is their count output, which I regenerated myself (Obs 10) and which is all zero.
   - The surviving mutants would mislead only on inputs that do not exist in the current tree.

   They are therefore nonblocking test-coverage gaps, not a C4 failure.
5. W08 is non-equivalent but has no effect: every real gate record carries exactly the pinned dict. W04 differs only when the I2 lower bound is exactly 0, a measure-zero case in a descriptive field.
6. Obs 11: the claim "0 identifier-context occurrences" is true as defined, but it is not "the literal is absent".
   - The literal occurs as a plain number in one non-FU-C, untracked file, at a rate consistent with chance, judged by the controls.
   - That file plus public membership does not single the value out, so no new repo-internal recovery path exists.
   - Root already records this class as the pending PI residual (committed r1/r2 handoff descriptions). I add only a count-only sharpening.

## 3. Caveats

- I did not test whether the committed r1/r2 descriptions, combined with public HCP documentation outside the repo, identify the value. Testing it would mean typing a candidate value. I leave this to root/PI under the pending residual.
- I read the sealed original into memory only, through the worker's own `sealed_original()` (in my count-only probes and in the rerun of the worker's check). I also ran `sha256sum -c` on `c4_sealed_originals_sha256.txt`, which reads the sealed file to hash it; the result was OK. Nothing from the sealed store was written to the repo.
- `probes/c4_decimal_context_classify.py` and its output were trimmed after the run: context-detail fields were removed as a C4 precaution, and the counts are unchanged. `c4_description_recoverability.py` was made context-generic and rerun; the output shown is from the rerun.
- Independence: while polling `ps`, I saw the command line of the peer challenger_FU_C_r3_2's mutant table. My table was planned beforehand. Overlap: my dropped X06 idea resembled their S07; X01–X05, Y01–Y06 and W01–W08 are mine.
- My suites ran while reviewer and peer C4 checks and mutation runs were active. That load caused no failures.
- I made no B300 GPU or Slurm use; the verdict is recomputable from the saved records. I did not re-evaluate any checkpoint.
- Addendum 03 §3 reports the pre-run counts (23,434 files, 2,174 blobs, 118 runs, 339 files) and says the final rerun is "in §8", but §8 does not give those numbers; they appear only in the worker handoff. This is a cosmetic documentation inconsistency.

## 4. Conclusion

**CONFIRMED.**
- FU-C verdict `stop`, I1 −0.113 % [−0.499 %, +0.272 %], df 7, δ 1 %. The qualifier "gain below delta, sign unresolved" is correct and reproduced byte for byte.
- The freeze order holds, receipts fail exactly as declared, C1 is rc 0, and all suites pass.
- The mutation claim is reproduced, and the C4 count-only containment holds on rerun.

Nonblocking, for root:
- (a) 10 surviving behavioural mutants on the r3 C4 tools (X01–X05, Y01–Y03, Y05, Y06), plus W04 and W08 on the verdict path. Recommended fix if FU-C is ever reopened: additive tests for the prefix-allow tail, allow-by-path, compact lists, sha512, the git `--all` scope, main() `ok` aggregation, and multi-run recoverability.
- (b) "0 identifier-context occurrences" should be read with its definition. One non-FU-C, untracked file holds the literal in a decimal-adjacent context. This is count-only, chance-level and not uniquely recoverable from repo content plus the staged list. It belongs to the existing pending PI residual.
- (c) Addendum 03 §3/§8 count wording.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py
PYTHONDONTWRITEBYTECODE=1 python3 -B verification/challenger_FU_C_r3_1/probes/recompute.py   # compare with recompute.out.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json   # rc 0, identical
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 python3 -B verification/challenger_FU_C_r3_1/mutants/run_mutants_c1.py $PWD <WORK> <OUT> 2   # 7 killed / 12 survived
PYTHONDONTWRITEBYTECODE=1 python3 -B verification/challenger_FU_C_r3_1/probes/scanner_adversarial.py
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/topic2fu_c_check_c4_r3.py --out /tmp/c4.json --b300   # ok true
```

What would invalidate these results:
- any change to `results/topic2/2026-11-02_fu_c/runs/*/run.json`, `verdict.json` or the card;
- a nonzero exposure count on a rerun;
- a new supersession.
