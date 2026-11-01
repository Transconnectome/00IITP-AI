# reviewer_M2_r3_1 — handoff (Hard), M2 Topic 3 iteration 3, 2026-11-01T07:15Z

Verdict: **REQUEST_CHANGES**. There is one blocking issue, and it is small and additive (B1 below). Everything else that the r1 and r2b gates required is closed, and I re-verified it independently.

Evidence: `/home/juke/git/00IITP-AI/verification/reviewer_M2_r3_1/`. I made no production write, no git write and used 0 GPU.

## Review Summary

| Area | Result |
|---|---|
| C1 | 67 OK, before and after my work |
| Receipts | output 42 / ad02 1 / ad03 3 / ad04 2 / ad05 3 OK |
| C2 | topic3 121 passed (0 skipped), topic1 88, old suite (STRICT_E2E) 86 — all run by me on production |
| C3 / C4 / C5 / C7 / C8 | met |
| T3.1–T3.4 | met; unchanged since iteration 1, and every pin verifies |
| r2b blocking classes 1–5 | closed. My own 13 rewritten patches, in my own byte-copy tree with my own runner: 12/13 survive the shipped 88, 13/13 are killed by 88 + r3, and each kill is a defect-specific assertion |
| r1 blockers | N05/N06/N08–N11 are killed in both of the worker's union passes, and the estimand wording was corrected in addendum 03 and not reintroduced |

**Blocking: the class-1 guard is one-sided.** Novel probe N01 changes the primary significance test to `min(1, 2*p_signflip) < 0.05` (Bonferroni) instead of `p_holm < 0.05`.
- It survives the full 121-test suite.
- It is reachable through the shipped producer at B = 9999 and flips the verdict from holds to killed.

## Findings

### [Major — blocking] B1: no test separates Holm from Bonferroni on the primary side
- **What.** `src/topic3_spectral/analysis.py:191`, `prim_ok = prim["p_holm"] < params["holm_alpha"]`. Mutant N01 rewrites it as `prim_ok = min(1.0, 2 * prim["p_signflip"]) < params["holm_alpha"]`.
  - It SURVIVED the full 88 + 33 suite: `MY_MUTANTS_run2.json`, job `N01_primary_bonferroni_consumer__full`, rc 0, 121 passed.
- **Why it matters.**
  - The r3 class-1 tests only check that the rule is no more liberal than Holm (raw < 0.05 ≤ Holm must be non-significant).
  - With k = 2, Holm differs from Bonferroni only for the LARGER raw p. There Holm p = max(2 p_min, p_max) = p_max.
  - No test has a primary with Holm p = raw p in [0.025, 0.05) that must count as significant. Every computed primary test uses p at the 1e-4 floor.
- **Reachable and verdict-changing** (`probes/witness_N01_N02.out.json`):
  - Setup: shipped `token_level_checkpoint` at card B = 9999, synthetic per-subject log ratios, seeds 2000–2002, three strongly agreeing zoo checkpoints.
  - H1b raw p equals Holm p, at 0.0347 / 0.0381 / 0.0364, and the CI excludes 0 (lower bounds 0.0006 / 0.0007 / 0.0005).
  - Shipped verdict: "holds". N01 verdict: "killed (primary CI includes 0)".
- **Real data are not affected.** Every real primary has raw p 1e-4 and Holm p 2e-4, so 2 × 1e-4 < 0.05. No reported verdict is wrong.
- **Precedent.** This is the same severity profile the r2b gate called blocking for V01 (reachable, verdict-flipping on card-procedure inputs, shipped code correct). V05 (a stricter-than-card zoo condition) was likewise blocking.
- **The zoo-side twin N02 is KILLED**, by `test_computed_zoo_with_ci_covering_zero_counts_end_to_end`, whose skewed checkpoint has Holm p = raw p = 0.032 / 0.031.
- **Suggestion (additive; no src/, scripts/ or rerun).** Add a primary-side test where the key contrast is the larger p:
  - hand-built: Holm p = raw p = 0.04, other primary at 1e-4, CI (0.005, 0.055), 3 agreeing zoo checkpoints → `primary_significant` True and "holds";
  - plus the computed version at seed 2000.
  - A ready demo is `verification/reviewer_M2_r3_1/proposed_tests/test_reviewer_demo_primary_holm_not_bonferroni.py`. It passes 3/3 on the shipped code (`logs/demo_demo_shipped.log`) and fails 3/3 under N01 (`logs/demo_demo_N01.log`).
  - Pin its sha256 in a dated addendum receipt.

### [Minor — nonblocking] N1: Family A descriptive numbers have no output replay
N03 and N04 survive. Neither is on a verdict path.
- **N03:** the A2 D-calibration iid reference is computed at (25, D) instead of the card's (12, D).
- **N04:** the E1 iid 2.5% quantile is moved to 5%.

Both change reported Family A descriptive numbers, so they meet the dispatch's necessary condition for blocking. I still class them nonblocking, by the r2b precedent:
- These descriptive survivors were classed nonblocking there: A21 (A1b orientation, up to a 15.3 shift after a rerun), T01 (H4 never subsamples), and the PARAMS mutants V15–V19 / A09–A13.
- A01 blocked only because it feeds the D3 verdict.

N01 blocks and N03/N04 do not because N01 is on the verdict path.

addendum_05 §6 discloses that Family A is not re-derived. Suggestion: add a Family A replay regression like the Family B one (it would need the 7 pinned npz; I did not measure its runtime).

Related: N02 (the zoo-side Bonferroni twin) is killed only incidentally, by the skewed V05 fixture. A deliberate zoo-side Holm = raw case could go in the same additive file as B1's fix.

### [Minor — nonblocking] N2: Family A card §2 halts are untested
N06 (`if not align["same_order"]` → `if False`) and N12 (BrainJEPA left out of the order check) survive in `scripts/topic3_subject_level.py`. Both are equivalent on valid inputs. This is the same class as r2b S05–S07, which iteration 3 closed for `topic3_token_stats.py` only.

### [Minor — nonblocking] N3: the "killed" label for one case is a misnomer
A primary with Holm p ≥ 0.05 and a CI that excludes 0 gets "killed (primary CI includes 0)".
- addendum_05 §5 discloses this, and the r3 test deliberately asserts only "not holds".
- It is a src label issue; it cannot be fixed in this iteration (no src change).

### [Info] Other notes
- **Git state.** The worker's "addendum_05 modified vs HEAD" is now stale: root checkpoint commit a910c53 (06:31Z) carries the final bytes a4001f09. The root checkpoint commits may also include this reviewer's metadata. Neither is my git write.
- **U127 / A15 equivalence: I agree.** A zero mean gives sign-flip p = 1, so the verdict is "killed" either way, and only the undefined direction label differs.

## Verified Claims

| Claim | How I verified it | Result |
|---|---|---|
| C1 67 OK; receipts 42/1/3/2/3 OK | `sha256sum -c`, before and after my work | pass |
| No src/scripts change | `code_sha256_at_freeze.txt`: all OK except `scripts/topic3_launch_connectome.py` (pre-existing, addendum 01 item 2, pinned in `output_sha256.txt`) | pass |
| Every pre-existing topic3 test is pinned and unedited | each file is listed in a receipt that verifies | pass |
| topic3 121 / topic1 88 / old suite 86 | I ran them on production, with no bytecode written and no production file written (`logs/prod_*.log`, `pyc_*`, find-newer) | pass |
| 27 + 6 = 33 new tests | the full control has 121 tests and the s88 control has 88 | pass |
| Worker evidence is authentic | every log_sha256 and junit_sha256 in S88_v2/FULL_v2 matches the files; junit failures parse and match the KILLED rows; the survivor junit counts are 88/121 with 0 failures | pass |
| Blocking classes 1–5 closed | own patches B01–B13. B04 (default level in resampling.py) is killed even by the shipped 88 suite, a different site from the worker's call-site V08 | pass |
| Addendum 05 numbers | recomputed from the pinned JSON/npz: H1b gm−1 HCP −10.7%, L1e-4 −3.2%, primary +4.6%, L5e-5 +8.2%; H1a −12.8 / +2.3 / +3.9 / +5.0%; half-widths 0.00203–0.01442; `cat_cov_eigs__L0` 57×384; H4 L0 max 3.18; fixture numbers raw 0.0326 / Holm 0.0652 / CI lo 0.0007 and skewed Holm 0.0321 / 0.0308, lo −0.0014; 508 non-run leaves | pass |
| Addendum 05 git claims | `GIT_OPTIONAL_LOCKS=0 git log --follow`: addendum 03 commits are 4ce1917, then ef27b71; 0db0336 adds only the two iteration-2 tests; 4ce1917 blob is 725d5077 | pass |
| Verdicts unchanged | pinned JSON: H1a holds 2/3 L3 higher; H1b not replicated 1/3; D1 "drop robust and not a per-channel-scale effect"; D3 True | pass |
| C4 | 57 real row IDs loaded in memory only; 0 of 1631 scanned files contain one; the only BIDS-prefix tokens are the synthetic names in the shipped `test_token_job_driver.py` and its byte copies | pass |
| Layout | `audit_layout.py` on the whole run root: PASS, 234 files, findings [] | pass |
| C5 | no M2 rows in `results/gpu_ledger_2026-10-31.md` | pass |
| C7 | VRABES `git status` clean; no file newer than the card | pass |
| C8 | addendum 05 and the r3 tests cite no EMPIRICAL_ANALYSIS_REPORT or json numbers | pass |

## Coverage Gaps

- Family A full replay: not run by me (optional; src unchanged and hash-verified; r1 challenger recomputed Family A independently). Risk: low.
- I re-ran only 13 rewritten blocking-class patches, not all 151 of the worker's union patches. The rest rest on the worker's evidence, which I checked for internal consistency and file hashes. Risk: low.

## 1. Observation

**O1. Production checks.**
- C1 `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: rc 0 with 67 OK, both before and after (`c1_pre.log`, `c1_post.log`).
- The five receipts: rc 0.
- pytest, with `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`:
  - topic3: "121 passed in 59.90s", no skips;
  - topic1: "88 passed";
  - old suite: "86 passed, 7 warnings".

**O2. Worker evidence.**
- Hashes equal the claimed ones: MUTANTS_SUMMARY fa7017ac…, S88_v2 34da3012…, FULL_v2 e222e7f2…, union_specs 706ef81b…, run_union 369b62e8…, S88 runner snapshot 6614112d….
- 0 log/junit hash mismatches; no KILLED row lacks a failure.

**O3. My run 2** (`MY_MUTANTS_run2.json`): `{"CONTROL_OK": 4, "KILLED": 21, "SURVIVED": 17}`.
- Controls: 88/121/88/121 tests, 0 skipped, imported from the job copy.
- K00 (canary) is killed by both suites.
- B01–B13:
  - s88: B04 KILLED, the other 12 SURVIVED;
  - full: all 13 KILLED, with failures such as "assert True is False", "assert 1 == 2" and the verdict dict diff.
- Novel probes (full suite):
  - SURVIVED: N01, N03, N04, N06, N12;
  - KILLED: N02, N05, N09, N10, N11.
- Run 1 was INVALID (my tree lacked `src/spectral_rg_flow_diagnostic.py` and `src/empirical_connectome_ablation.py`). It is preserved in `run1_INVALID/` with a README.

**O4. Witness.** `probes/witness_N01_N02.out.json` (quoted above).

**O5. Demo test.** "3 passed" on the shipped code; "3 failed" under N01.

## 2. Logic Chain

1. O1 and O2 show the production state is as the worker claims and that its evidence files are genuine.
2. O3's B-series is independent of the worker's runner, trees and patch bytes. It reproduces each r2b blocking defect (survives s88) and shows the r3 tests kill it with defect-specific assertions. So classes 1–5 are closed as the r2b gate specified them.
3. N01 survives the full suite (O3). By O4 it is reachable through the shipped card-parameter producer and flips "holds" to "killed". By the dispatch rule and the r2b precedent (V01, V05), it blocks.
4. The fix is one additive test (O5) and changes no src/, scripts/ or real verdict.
5. N03, N04, N06 and N12 are descriptive-only or equivalent on valid inputs. Under r2b practice they are nonblocking.

## 3. Caveats

- N01 is a reviewer-designed mutant, not a defect in the shipped code. The shipped rule is correct, and no real verdict changes.
- Whether one more iteration is warranted for a single additive test is a PI/root decision. My verdict is advisory (sci-pipeline §2).
- Disclosure: at about 06:29Z I ran one plain `git status --porcelain` (redacted output kept in `git_status_before.txt`), which can refresh `.git/index` stat data. The index was rewritten afterwards by root checkpoint a910c53 at 06:31:28Z. I made no content change; all later git reads used `GIT_OPTIONAL_LOCKS=0`.
- `tree_base` (19 MB) is kept in my verification folder for reproducibility.

## 4. Conclusion

**REQUEST_CHANGES**, with a single blocking item: B1, an additive primary-side Holm-vs-Bonferroni guard plus a receipt.

Everything else (C1–C8, T3.1–T3.4, r1 and r2b blocking classes) is met with evidence.

## 5. Verification Method

**Run provenance.** Run 2 was produced by runner sha256 `b73d414f9d75653f29da239cbc0eaadb79c265052819f636275dd863eaba1809` (`run2_runner_snapshot.py`). The specs are `run2_specs_snapshot.py` (17a30dca…) and the tree manifest is `tree_base.manifest_sha256.txt` (c4185539…).

`run_my_mutants.py` is now v2 (31210647…). It writes logs to `<out>_logs` and refuses to overwrite existing evidence, so a rerun never touches run 2's `mutant_logs/`.

**Evidence hashes.** Every evidence file is in `verification/reviewer_M2_r3_1/EVIDENCE_MANIFEST_sha256.txt` (138 files, self-check 0 failures). The key ones:

| File | sha256 |
|---|---|
| `MY_MUTANTS_run2.json` | 0bf5f647621bf8f9f404b284bcde8c4a36f50e4b9ef0ec4726771580cb2a1c05 |
| `probes/witness_N01_N02.py` | 0a81beb6a76f347e2deb1a3d28089af49f3471f73eef5632f889591b2f7972bf |
| `probes/witness_N01_N02.out.json` | 205dc86e94aa113f7551145929bb24fdc41fd734e4005bf9bf75d41692b7b931 |
| `proposed_tests/test_reviewer_demo_primary_holm_not_bonferroni.py` | e09ff20c09d8abd90447a138e5b6dc9d2b0043e6ba7692008a262379ffab2519 |
| `probes/check_fixture_numbers.out.json` | 77de1fcb6beaa8bdd101317df8b87d288655728b061d83c76d8ce69440f6af65 |

**Reviewed deliverables (unchanged during my review).**

| File | sha256 |
|---|---|
| `test_verdict_rules_r3.py` | 58c64ccbc66e825b5e66e4322894e61d02ea5bddad8c3029c3be480dd0acd80b |
| `test_token_stats_wiring_r3.py` | b091b0b861dc212d2972ed5a9bb64cfe42d41361e1bd6bde05f9476681ac6a1c |
| addendum_05 | a4001f09ff7d8ccb401e5015ade37e887fbad5e3f17a15019a9c3d8695163bd1 |
| `addendum_05_sha256.txt` | 1e542da7705d78000961faca75c11f8236473442e9fecaf9e181056c8e2905d6 |

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
V=verification/reviewer_M2_r3_1
cd $V && LC_ALL=C sha256sum -c EVIDENCE_MANIFEST_sha256.txt                     # evidence intact
/home/juke/superclaude-env/bin/python3 -I -B run_my_mutants.py $PWD/CHECK_$(date +%s).json N01_primary_bonferroni_consumer,B01_V01_primary_raw_p --jobs 2
#   fresh output name (v2 refuses to overwrite); expect N01 full SURVIVED; B01 s88 SURVIVED / full KILLED
cd probes && /home/juke/superclaude-env/bin/python3 -I -B witness_N01_N02.py     # shipped 'holds' vs N01 'killed'
```

**Invalidation conditions.**
- A test that passes on the shipped code and fails under N01 already exists in `tests/topic3_spectral`.
- Or the witness seeds no longer give raw p in [0.025, 0.05) with a CI excluding 0.
