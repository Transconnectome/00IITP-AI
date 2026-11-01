# handoff — reviewer_M3_r3_2 (M3 Topic 2, iteration 3, ACCEPTANCE T2.4) — Hard handoff

## Review Summary
**Verdict: APPROVE.** Every T2.4 item and C1–C8 is met with evidence I reproduced myself. No blocking issues. Nonblocking notes are listed in §4.

## 1. Observation
Evidence is in /home/juke/git/00IITP-AI/verification/reviewer_M3_r3_2/. I used my own harness (v02_mutants.py), not the worker's m01.

**Integrity**
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives 67/67 OK, rc 0. Checked at about 16:00Z and again at 16:41Z.
- Receipts:
  - addendum_06_sha256.txt 31/31
  - code_sha256_at_freeze.txt 33/33
  - output_sha256_r2.txt 156/156
  - c4_sanitized 19/19
  - c4_sealed_originals 19/19, checked against the durable sealed copy
  - old card_sha256 fails on 2 lines and old output_sha256 on 16. This is the expected set, disclosed in addendum_05.
- The 12 shipped test files match their pins in output_sha256_r2.
- Pinned hashes:
  - receipt sha 4ac6d454…12fb
  - verdict.json 59af05e5…af68
  - card c9bfc60a…41f5

**Tests**
- New file test_verdict_path_guards_r3.py: 24 passed.
- Full tests/topic2_rgpool, local, CUDA hidden:
  - 16:0xZ: 115 passed, 1 failed. The failure is test_outputs_no_ids. The only file it flags is the FU-B card, where the BIDS-prefix regex matched a word fragment; no other file was flagged.
  - 16:41Z: 116 passed, 0 skipped. The FU-B team had edited its card at 16:20Z and added fu_b_addendum_01 (v09).
- test_c4_tokens_r2 + test_outputs_no_ids: 11 passed (v07, after the FU-B edit).
- Old 86 suite (STRICT_E2E=1): 86 passed (v06).
- tests/topic1_lagmotif: 88 passed (v08).

**Mutation legs** (worker's 24 verbatim specs). I checked that V01–V11 are byte-equal to challenger_M3_r2_2 p07_specs.json (sha de8f2de1…ea4e).
- **A, 12 shipped files only** (fu_* cards left out of the mirror docs): baseline 92 passed. All 20 non-control mutants SURVIVED. The 3 CTRL were KILLED. 0 INVALID.
- **B, new file only:** 20 KILLED (V01–V11, K1, K2, W04–W08, W12, CTRL_hcp_4_seeds). SURVIVED: baseline, W09, CTRL_t_df_n, CTRL_boot.
- **A ∪ B kill sets:** 22/24 killed; only the baseline and W09 survive. This matches the worker's leg C. I did not run C as one combined pytest.
- **D, mutated frozen script on the shipped runs:** baseline + 20 mutants byte-identical to verdict.json. The 3 CTRL differ and still give stop.
- **My 8 extra adversarial mutants** (v03_extra_specs.json):
  - fixture gate uses the first seed only
  - stop rule also requires a negative lower bound
  - script default δ = 0.02
  - 90 % t interval
  - I2 computed against E
  - F+ False ignored
  - F+ gate uses `or`
  - seed order reversed in I1

  The shipped suite kills all 8; the new file alone kills 2. The shipped verdict is unchanged in D for all 8 (still stop).

**Code and card checks**
- E1: `scripts/topic2_verdict.py` has `else: no_verdict "Stage 1 incomplete"`, while card §7.2 says "If F+ fails, Stage 1 is not run. The verdict is then `inconclusive`". Confirmed.
- E2: `bool(fp)` with fp = None counts a missing F+ gate as an F+ failure, giving inconclusive. Confirmed.
- E3: `fm is not False` counts a missing F− gate as a pass. Confirmed.
- E4: `load()` keeps the last record in glob order. Confirmed.
- E5: the test-order guard is an `assert`. Confirmed.
- The `card_verdict` oracle matches the card §8 table and its order (stop first).

**Shipped facts** (recomputed from verdict.json and run.json)
- verdict stop; F+ 3.06 % / 2.93 %; F− −1.74 %
- I1 mean 0.147 %, CI [−0.068 %, +0.361 %]; I2 lower bound 9.8e-6
- last F+ end_utc 03:42:08Z < first hcp start_utc 03:44:51Z
- the frozen script rerun locally writes byte-identical verdict.json

**Salt containment** (v05, counts only)
- Sealed salt sha = 7e5434ab…d02e, mode 0400/0700/0700. The old repo path is gone.
- 6 needle variants: 0 hits in 19,560 working-tree files (2.33 GB) and 0 in 3,278 git objects.
- 2,427,711 hex 16-windows from the working tree and blobs, checked against every window of sha256, sha1, md5, and sha256 with the public split salt as prefix or suffix, over all 10^6 six-digit names: 0 hits.

## 2. Logic Chain
1. T2.4(1), attributable kills: each of V01–V11 survives the 12 pinned shipped files (A), and the new file alone kills it (B). The new file passes on frozen code, and the controls show leg A can detect changes. So the kills are attributable to the additive tests.
2. W09 equivalence: hi = m + q·se with q > 0 and se ≥ 0. IEEE rounding is monotone, so hi ≥ m. hi < δ then implies m < δ, so i1_survives is false and W09 matches the original. NaN gives false in both. The governed caller passes only t_interval outputs. The proof holds, and leg B and the worker's p02 agree.
3. T2.4(2), erratum: E1 is a true card-vs-code defect, read straight from the code and the card. addendum_06 records it without editing the frozen script. The [erratum] tests pin the frozen label and assert the card reading.
4. T2.4(3), containment: my independent scan agrees with the worker's s01. The salted-hash and unsalted-hash routes are closed.
   - The positional statement plus the off-repo B300 listing remains a route. C4 explicitly sanctions positional indices, so this is inherent to the approved scheme, not a violation. It is properly left for a PI ruling.
5. No regression: C1, all receipts, old 86, topic1 and the full topic2 suite are green now (116). The interim red test was caused by another team's file, now fixed by that team.
6. The shipped verdict is unchanged: every erratum precondition is false, and D is byte-identical for all non-control mutants.
7. No integrity violation:
   - no hardcoded outcomes in src; the tests derive from card text;
   - the mutant specs were read verbatim from source;
   - the logs I reproduced agree with the worker's claims.

## 3. Caveats
- I derived leg C as the union of A and B; I did not run it as one combined pytest.
- I did not rerun anything on connectome; all legs ran locally (numpy 2.3.5, scipy 1.15.3, torch 2.11 dev, CPU).
- I did not reproduce the positive-control recovery of the 5 burned hashes. I chose not to rebuild dev IDs in memory.
- I did not scan the repo against the B300 HCP name list, because it needs B300.
- E2/E3 are interpretive; I agree they are labelled so.

## 4. Conclusion and nonblocking findings
APPROVE M3 r3 for T2.4. Nonblocking:
- N1 (Minor): addendum_06 §6 says "`test_c4_tokens_r2.py` + `test_outputs_no_ids.py` 11 passed with this addendum present", but no log in verification/worker_M3_r3 backs it.
  - The worker's own progress note at 15:50Z shows test_outputs_no_ids failing while the addendum existed. The FU-B card tripped it from at least 15:29Z to 16:20Z.
  - The claim is true now: I got 11 passed at about 16:40Z.
  - Suggestion: a one-line dated note in a later addendum. Do not edit the pinned file.
- N2: the "ROOT ACTION" in the worker handoff (the FU-B card trips C4) is stale. The FU-B card was edited at 16:20Z, and the suite now gives 116 passed.
- N3: root/PI ruling still needed on the positional dev-subject residual, and on the strict vs narrow reading of E2/E3.
- N4: the new file is not a standalone guard for the whole verdict path. 6 of my 8 extra mutants survive it alone, though the shipped suite kills them. The union is what matters; this is noted for the FU-A..E verdict scripts.
- N5: carried forward, as in addendum_06 §7: split.json re-derivation, the 103-vs-102 count, CUDA-visible skips, the C4 test scope gap, and untested sanitize/seal scripts.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q tests/topic2_rgpool
P=/home/juke/superclaude-env/bin/python3; V=verification/reviewer_M3_r3_2
$P $V/v02_mutants.py $PWD verification/worker_M3_r3/mutation_specs.json $V/work out.json A --jobs 2   # also B, D
$P $V/v02_mutants.py $PWD $V/v03_extra_specs.json $V/work outx.json B --jobs 2
$P $V/v05_salt_scan.py $PWD ~/.local/share/00IITP-AI_sealed/topic2/dev_subject_salt.txt out_salt.json
```
Invalidation: any edit to src/topic2_rgpool, scripts/topic2_*.py, the shipped tests or the r3 file; any new docs file in docs/03_empirical_analysis/topic2 that trips the C4 scanners.
Compute: 0 GPU-h, no ledger row. Local CPU only, at most 2 concurrent pytest, nice. No processes left; the mirror work dir has been removed.
