# handoff — explorer_M3_r3_1 (M3 Topic 2, iteration 3 / T2.4), Hard handoff, 2026-11-01T14:30Z

**Summary.** Every r2 blocking item can be closed without touching src/, the frozen scripts or the card. A proposed additive
test file, written from the card text, kills all 11 challenger mutants V01–V11 plus the two same-class survivors K1 and K2
found by other verifiers. Each kill is attributable: each mutant survives the shipped tests and is killed by the new file.
The frozen script diverges from the card in five places, not one; addendum_06 should list all five. None of them is
reachable with the shipped data: mutated scripts on the shipped runs give a byte-identical verdict.json (14/14). The
dev-salt containment holds: the salt is in 0 repo files and 0 git objects, and no scheme computable from repo content
recovers an ID. No regression: topic2 92 passed, old 86 passed, topic1 88 passed, C1 67/67, receipts unchanged.

## 1. Observation
- Gate record `orchestrator/M3_r2_gate_record.json`, challenger_M3_r2_2 blocking items:
  - (a) dev-salt C4 leak;
  - (b) V01–V11 survive the 92-test suite (connectome p07, 54 srun steps, 0 INVALID);
  - (c) case A: card §7.2 says inconclusive, the frozen script says `no_verdict` "Stage 1 incomplete".
  - Other verifiers found same-class survivors: K1 (F− uses (S−C)/S), K2/R1 (keep uses the I2 mean), K3 = V04, K4 = V03, K9 = V09 (challenger_M3_r2_1 `run_mutants_c1.py:20-21`; reviewer_M3_r2_1 N5).
- Frozen code:
  - `src/topic2_rgpool/stats.py:57-75`: `verdict`; F+ is checked first, then stop, keep, modify. F− downgrades only keep.
  - `stats.py:78-90`: `gate_fixture`.
  - `scripts/topic2_verdict.py`:
    - `load()` keys on (source, arm, seed); the last record in glob order wins.
    - Gates are `None` when any run is missing or failed.
    - Stage 1 runs only if `hcp_complete`. If not, the output is `no_verdict` "Stage 1 incomplete", whatever the gates say.
    - The order guard is a bare `assert`.
    - `S.verdict(..., bool(fp), fm is not False)`: a missing F+ counts as a fail, a missing F− counts as a pass.
- Card:
  - §5 run integrity: "A second failure leaves the seed missing and the verdict becomes `no_verdict`".
  - §7 heading: fixtures "must pass before any real-data number governs a decision".
  - §7.2: "If F+ fails, Stage 1 is not run. The verdict is then `inconclusive` (measurement capacity)". "If F− fails, a would-be `keep` is downgraded".
  - §8 table, "applied in this order after the §7.2 gate". Inconclusive covers "the F+ gate failed, or keep with an F− failure". no_verdict = "Stage 1 incomplete after one rerun".
- Only `test_stats.py` and `test_verdict_path_guards_r2.py` import stats or the verdict script. No test hashes `stats.py` or `topic2_verdict.py`; the only hash checks are of vendored files (`test_leakage_and_provenance.py:60,64`) and compare two in-test runs (`:89-91`). The other 12 files therefore cannot observe these mutants, which matches p07's full-suite survival.
- Shipped preconditions (counted from `results/topic2/2026-11-01`):
  - 27 run.json, 27 distinct keys, all `completed`, 1 distinct HCP test order.
  - F+ pass with gains 3.061 % and 2.935 %. F− pass with gain −1.737 %.
  - `hcp_complete` true. I1 hi = 0.3614 % < δ = 1 %. I2 lo = +9.8e-6 (+0.001 %), so `I2_lower_gt_0: true` by a hair.
- My probes, in `verification/explorer_M3_r3_1/`:
  - **p01** (`p01_attributable_kills.py` → `.out.json`, sha 181ef41a…2d27):
    - Mutants: V01–V11 verbatim from `challenger_M3_r2_2/p07_specs.json`, and K1/K2 verbatim from challenger_M3_r2_1.
    - The baseline passes both the shipped tests and the proposed file.
    - All 13 mutants: SURVIVED the shipped tests, KILLED by `proposed/test_verdict_path_guards_r3.py` (sha e6291010…2031); the per-mutant failing tests are in the out.json.
    - The mutated `topic2_verdict.py` on the shipped runs gives verdict.json byte-identical in 14/14 cases (baseline and the 13 mutants).
  - **p02** (`p02_salt_containment_scan.py` → `.out.json`, counts only):
    - The repo salt file is absent.
    - The sealed copy matches root's sha 7e5434ab…d02e. Mode 0400, directory 0700, parent 0700, not inside a git repo. Salt length 32.
    - Salt bytes: 0 hits in 17,770 working-tree files (2.30 GB) and 0 hits in all 1,568 git blobs (`--batch-all-objects`, so unreachable objects are included).
    - The 5 burned hashes are recovered 5/5 only with the sealed salt, and 0/5 with no salt or with the public split salt.
    - Unsalted sha256, sha1 and md5 of all 10^6 six-digit strings, and sha256 with the public split salt in both orders (5,000,000 16-hex prefixes, any window, case-folded): 0 hits in the working tree and 0 in git objects.
    - **p02b** positive controls detect planted values (full64, prefix16, uppercase, mid-run, salt needle).
  - **p03** regression (`p03_regression.log`, `p03b_pipeline_guards_rerun.log`):
    - tests/topic2_rgpool, per file: 8+7+3+3+16+7+3+11+19+4+1+10 = 92 passed.
    - `test_pipeline_guards_r2.py` was first SIGTERMed (rc 143, earlyoom; that run is INVALID). Rerun alone: 19 passed, rc 0.
    - old 86: 86 passed. topic1_lagmotif: 88 passed.
  - **Receipts (final check, 14:28Z):**
    - C1 67/67; code freeze 33/33; output_r2 156/156; c4_sanitized 19/19.
    - card_sha256: 6 OK, 2 FAILED (hcp_manifest, split). output_sha256: 16 FAILED (stage0 and 15 hcp run.json). Both sets were disclosed in addendum_05.
- Per-test card citations are in the proposed file. The `card_verdict` oracle is coded from the §8 table text in rule order.

## 2. Logic Chain
1. **Why r2 failed (design lens).**
   - r2 wrote tests to kill an enumerated mutant list, not to cover the card's decision table.
   - Each new verifier then found untested cells: boundaries, the I2 lower bound vs mean, F− scope, and run-integrity guards. That is the same whack-a-mole as M2 r1–r3.
   - The fix is tests derived from the specification. One exhaustive boundary-grid test against an oracle coded from §8 alone kills V01, V02, V03, V06, V11 and K2 (p01 `failed` lists).
2. **Attributable kills.**
   - (a) Every mutant survives the shipped files that can observe it (p01) and the full 92-test suite (challenger p07; the other 12 files cannot observe stats or verdict edits, per the grep in Observation).
   - (b) Every mutant is killed by the new file alone (p01).
   - (c) The new file passes on frozen code (p01 baseline).
   - None of the 13 is equivalent: each has a concrete distinguishing input, the assertion that fails.
3. **Card-vs-code errata.** The script conflates "gate not computed" with "gate computed and failed", in both directions:
   - **E1 (certain, case A).** F+ failed and Stage 1 not run (exactly what §7.2 prescribes) gives `no_verdict` "Stage 1 incomplete". The card says `inconclusive`. A capacity failure is labelled a software failure (G8).
   - **E2 (interpretive, case C).** F+ runs missing or failed give `pass: None`. `bool(None)` makes the verdict `inconclusive`, with the reason "measurement-capacity gate failed". Under §5 a seed missing after one rerun is `no_verdict`, so a software failure is labelled a capacity failure: the mirror of E1.
   - **E3 (interpretive, case D; upgrades addendum_05 item 8).** A missing F− counts as a pass, so a would-be keep stays keep. That contradicts the §7 heading "must pass before any real-data number governs".
   - **E4 (case E).** Duplicate (source, arm, seed) records are resolved by glob order, which depends on the filesystem. §5 keeps failures "in the ledger", so a failed attempt left in RUNS_DIR could shadow the rerun.
   - **E5.** The paired-subject order guard is an `assert`, which `python -O` or `PYTHONOPTIMIZE` removes. The t-interval uses per-run `test_nmse` and does not depend on order. The secondary hierarchical bootstrap pairs subjects by index, so it would silently mis-pair.
4. **The shipped verdict is unaffected.**
   - Each erratum's precondition is false in the shipped data: gates computed and passed with margin of at least 2δ, Stage 1 complete, no duplicates, one order, run without -O (result report line 261).
   - Direct evidence: all 13 mutated scripts reproduce verdict.json byte for byte on the shipped runs.
   - stop is decided only by I1 hi = 0.36 % against δ = 1 % (challenger p01: leave-one-seed-out hi ≤ 0.47 %).
   - Caveat for the reader: `I2_lower_gt_0: true` is non-governing, sits at +0.001 %, and is confounded with compactness (addendum_05 item 4). It must not be cited as FC-specificity evidence.
5. **Making the erratum checkable.**
   - A prose erratum alone is unfalsifiable. addendum_06 should state a reading rule (table below), and the test should implement it as `card_reading`.
   - The test pins the frozen labels for cases A, C and D (characterisation) and asserts the card reading. Asserting card labels against frozen code would fail and is forbidden.
   - On the shipped verdict.json, `card_reading` gives `stop`, the same as the script.
6. **Containment.**
   - The criterion "no repo content lets HCP IDs be recovered" holds for the salt route (p02) and for unsalted or public-salt hash routes over the full 6-digit space.
   - The remaining linkage routes all need off-repo data: positional rank = content-hash rank, and the preprocess.log completion order needs the staged listing. Subject selection depended on another workstream's partial rsync, so it is not derivable from public lists. These routes stay root/PI rulings and nonblocking for T2.4.

## 3. Caveats
- E2 and E3 are interpretive. The card does not say how a missing fixture gate is labelled. I propose `no_verdict` for "not computed" (§5) and keep E1 as the only certain erratum. The worker or root may choose `inconclusive` for E2 and E3; the test must then change in `card_reading` only.
- The attributable-kill full-suite leg rests on challenger p07 (connectome) plus the import/hash grep. I re-ran the two observing files locally, not the full 92 per mutant.
- Local host memory: earlyoom SIGTERMed one test file once (rc 143, INVALID, rerun passed). Rerun locally, or use connectome srun.
- Not scanned:
  - the B300 off-repo salt copy at /scratch/iitp4/worker_M3_r1/code/scripts/ (reported by reviewers; off-repo, volatile);
  - the /tmp/claude-1000 scratch of other sessions;
  - files inside compressed containers;
  - salted schemes with unknown salts (impossible by construction).
- I read the sealed salt into memory only, for counting, and never printed or copied it.
- The proposed test is a probe. The worker should adopt it as `tests/topic2_rgpool/test_verdict_path_guards_r3.py` and adjust its wording; the logic and values are validated.
- No GPU used (0 GPU-h, no ledger row). No git writes. No processes left; the mutant mirrors were removed.

## 4. Conclusion (recommended fix strategy for worker_M3_r3)
1. Add `tests/topic2_rgpool/test_verdict_path_guards_r3.py` from `verification/explorer_M3_r3_1/proposed/` (15 tests). Keep every expectation cited to card text; no src or scripts change.
2. Report the mutation evidence: re-run `p01_attributable_kills.py`, or its full-suite variant on connectome srun with the 54-spec pattern of challenger p07. Table each mutant as shipped SURVIVED / new KILLED / shipdata byte-identical. Claim only the enumerated set; never write "all mutants".
3. Write `docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_06.md` with:
   - (i) errata E1–E5, each with its card citation;
   - (ii) the reading rule:

     | F+ pass | Stage 1 complete | script verdict | card reading |
     |---|---|---|---|
     | False | any | any | inconclusive |
     | None | any | any | no_verdict |
     | True | False | any | no_verdict |
     | True | True | keep, F− None | no_verdict |
     | True | True | keep, F− False | inconclusive (already in the code) |
     | True | True | otherwise | the script verdict |

   - (iii) the precondition table with the shipped values and the p01 byte-identity evidence;
   - (iv) the statement that the shipped verdict stays **stop**;
   - (v) the I2-boundary caveat;
   - (vi) housekeeping errata from the other verifiers: split.json is not re-derivable from repo tokens (challenger_M3_r2_1 N3); "103" should be 102; swapped pin suffixes.
4. Pin addendum_06 and the new test file in a NEW receipt, for example `results/topic2/2026-11-01/addendum_06_sha256.txt`. Never edit the old pin files.
5. Gate step for containment: re-run p02 (counts only) as the gate artefact. Optionally extend the scope of `test_c4_tokens_r2` to `verification/` and `.agents/` (reviewer N6); this is nonblocking.
6. Ask root for a fixed gate scope, like PI decision 6 for M2:
   - blocking = these 13 mutants killed, addendum_06 E1 present and correct, containment re-verified, no regression;
   - new mutants outside this class are nonblocking.
7. Forward, for FU-A..E (F2):
   - Do NOT reuse the frozen `topic2_verdict.py` unchanged. Each option's own verdict script should implement the reading rule natively: explicit computed/failed/missing gate states, `raise` instead of `assert`, an error on duplicate keys, and F+ failure → inconclusive without Stage 1.
   - Test it with the same oracle grid.
   - FU-A and FU-D change the target or scale, so an F+ failure is reachable there and E1 would bite.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI/verification/explorer_M3_r3_1
OMP_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 nice /home/juke/superclaude-env/bin/python3 -B p01_attributable_kills.py /home/juke/git/00IITP-AI $PWD/mut /tmp/p01.json   # ~2.5 min; expect 13 attributable, baseline_ok, shipdata byte-identical
nice /home/juke/superclaude-env/bin/python3 -B p02_salt_containment_scan.py /home/juke/git/00IITP-AI /tmp/p02.json        # ~35 s; counts only
/home/juke/superclaude-env/bin/python3 -B p02b_scanner_positive_control.py
./p03_regression.sh   # rc 143 = INVALID -> rerun that file alone
cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c
```
Invalidation conditions:
- a baseline failure of the proposed file on frozen code;
- any mutant SURVIVING the proposed file;
- shipdata not byte-identical;
- any salt or unsalted hit greater than 0;
- a change to code_sha256_at_freeze.
