# challenger_M2_r2b_1 — handoff (Hard), M2 Topic 3, gate r2b, 2026-11-01 ~02:10Z

Probes, logs and receipts: `/home/juke/git/00IITP-AI/verification/challenger_M2_r2b_1/` (V below). No production file was written (68 topic3 production files byte-identical to my 01:29Z snapshot, `V/final/production_topic3_vs_base_manifest.log`). No git write. 0 GPU. No processes left running.

## Challenge Summary

**Verdict: REFUTED (scoped).** Overall risk: MEDIUM. Results and verdicts are not at risk; the test-coverage claim is.

What holds (CONFIRMED):
- The card was frozen before every real-data result. Hashes and timestamps agree, and git gives an independent anchor.
- Every headline number reproduces. Family B replays the frozen JSON exactly (|Δ| = 0). Family A matches to ≤ 1.2e-14. A full copied-tree rerun gives 0 value differences.
- Both verdicts follow the card. With my own implementation of card §5: H1a "holds" (2/3 zoo agree) and H1b "not replicated" (1/3). D1 and D3 also follow §4.
- Addendum 03 now describes Family B correctly. Finding (i) of iteration 1 is closed, apart from one non-blocking numeric slip (H4 ceilings).
- The worker's mutation claims hold. I reran the 8 iteration-1 survivors independently and all are killed. MM 06 (my V33, the identical patch) is killed by the r2b tests. The worker's run-2 and run-3 log hashes match (69/69 each).

What is refuted:
- The claim that iteration 2 makes the **verdict logic test-guarded** (finding (ii)). It holds for the 67 assigned mutants only.
- My own verdict-path mutants V01, V05, V06, V07, V08 and V26 survive the shipped 88-test suite. Each one changes a verdict on reachable inputs (synthetic for V01/V05–V08, real for V26).
- V01 is the primary-side twin of iteration-1 N08. V06–V08 disable the card's "killed" outcome through the statistic the rule reads. V26 flips the real H1a verdict from "holds" to "not replicated".

## 1. Observation

**O1. Integrity**
- Before and after my work:
  - C1: rc 0, 67 OK, identical (`V/baseline/c1_before.log`, `V/final/c1_after.log`).
  - `output_sha256`, `addendum_02/03/04_sha256`: rc 0.
  - `code_sha256_at_freeze.txt`: only `scripts/topic3_launch_connectome.py` FAILED, as disclosed in addendum 01 #2 (`V/baseline/pins_before.log` = `V/final/pins_after.log`).
- ID grep `sub-[A-Za-z0-9]` over V and my metadata: rc 1, no hits.
- `audit_layout.py` on the run root: PASS, findings [] (`V/final/audit_layout_before_handoff.log`).

**O2. Freeze order (T3.2 / C3)**

| Event | Time (UTC) | Source |
|---|---|---|
| card mtime | 2026-10-31T08:43:40Z | file mtime |
| card committed | 08:46:25Z (git `24fe976`) | blob sha256 = `683374565d80…b1e0`, same as `card_sha256.txt` and the current file; the card's only commit |
| card hash recorded | 08:48:29Z | `card_sha256.txt` |
| Family A | started_utc 08:49:18Z | run record |
| token jobs | 08:53–08:58Z | job JSON mtimes |
| Family B | started_utc 09:01:59Z | run record |

- Both run records carry `card_sha256_verified` = 68337456….
- Synthetic alpha calibration (08:40Z) and the T3.1 reproduction (08:31Z) ran before the freeze. Card §4 and §11 disclose this.

**O3. Family B recomputation** (`V/probes/probe_family_B_indep.py`, `.log`, `.out.json`)
- Inputs:
  - all 4 spectra npz match the `output_sha256` pins;
  - PR recomputed from the stored eigenvalues matches the stored scalars (max relative difference 5.2e-8).
- Exact replay of the package's seed schedule with my own code: Δ = 0 for mean, raw p, Holm p and both CI bounds, for every checkpoint × {H1a, H1b}.
- Independent seeds (B = 99999) with my card-§5 rule written from the card text:
  - H1a holds, with agreement from the two deep NewUAH checkpoints;
  - H1b not replicated, with agreement from L5e-5 only.
- The smallest |z| among the checkpoints is 7.6 (H1a) and 4.5 (H1b).

**O4. Family A recomputation** (`V/probes/probe_family_A_indep.py`, …)
- Pins: 7/7 sha OK. Row order is the same across the six 57-row files. The NeuroSTORM positions are increasing (n = 25).
- E1 covPR and corrPR match the frozen values to ≤ 1.2e-14.
- Replaying the A1/A2 index sets matches to ≤ 1.8e-15.
- With my own subsets (seeds 4242/4343), D1 = both lower bounds > 0 and D3 = true. Same verdicts as frozen.

**O5. Report tables** (`V/probes/probe_report_tables.log`)
- 142 printed values checked: report §2 A1/A1b/A2, report §3 H1 table, the secondary ratios, H4, the medians, the verdict strings, and the addendum 03 item-3 L1 jackknife numbers.
- 140 OK, 2 MISMATCH. The two mismatches are exactly addendum 03 item 5's errata (+3.23 → 3.2249865; −3.29 → −3.2848924).

**O6. Full copied-tree rerun** (`V/rerun/compare_tree_rerun_vs_frozen.log`)
- I ran all four scripts: provenance_repro, alpha_calibration, subject_level and token_stats.
- The JSON values have 0 differences from the frozen outputs.
- The only differences are 3 absolute-path strings in `t3_1_provenance_repro.json`, from the copied-tree location.
- CPU time was about 3 min.

**O7. Own mutants**
- Files: `V/mutants/mutant_specs.py`, `run_mutants.py`, `MUTANTS_run2.json`, `logs_run2/`.
- Setup: 29 patches, each applied exactly once, on fresh copies; the full 88-test suite, no `-x`.
- Controls passed at the start and the end: 88 passed.
- 28 of the 29 differ from every worker patch. The exception is V33, my control, which equals MM 06 (`compare_with_worker_set.log`).
- Killed (6): V02 (primary Holm `<=`), V09, V10 (control), V23, V30, V33 (MM 06 control, killed by both r2b tests).
- Survived (23):

  | Class | Mutants |
  |---|---|
  | rule | V01 primary uses raw p instead of Holm p; V03/V04 primary CI `>= 0` / `<= 0`; V05 zoo additionally requires the CI to exclude 0; V11 D1 `lo >= 0`; V12 D3 `lo >= 0`; V14 D2 threshold 0.05; V26 `topic3_token_stats.py` passes ZOO[0] as primary; V29 the zoo tuple drops one checkpoint |
  | input | V06 ci95 = [hi, lo] in `paired_log_contrast`; V07 CI of exp(d); V08 50% CI; V13 A2 uses the first 25 rows instead of the NeuroSTORM positions; V21 bootstrap never draws the last subject; V22 sign-flip tie tolerance 1e-3; V28 subject script passes `range(25)` |
  | param | V15 m57 = 29; V16 bootstrap B = 999; V17 S = 200; V18 seed; V19 m25 = 13 |
  | gate | V25 `verify_card` bypassed; V27 re-pool halt removed |

**O8. Reachability of the surviving rule mutants** (`V/probes/probe_reachability.py`, sha256 `3bfb69ea…9246`; outputs in `V/probes/reach_final/`, earlier identical runs in `reach_initial/`)
- Setup: synthetic per-subject PR arrays, n = 57, card B = 9999, run through the full `token_level_checkpoint` → `replication_verdict` path of the shipped tree and of each patched copy.
- **V01**, seeds 1000–1002. Primary H1a has raw p 0.031–0.033, Holm p 0.061–0.065 and a CI that excludes 0; 3 zoo checkpoints agree.
  - Shipped: "killed (primary CI includes 0)". This is the label addendum 03 item 3 calls unreachable; it is reached here.
  - V01: **"holds"**.
- **V06 / V07 / V08**, seeds 50001–50003 (skewed log ratios). Holm p is 0.034–0.039 and the 95% percentile CI lower bound is between −0.0020 and −0.0016; 3 zoo checkpoints agree.
  - Shipped: "killed".
  - V06, V07 and V08: **"holds"**.
- **V05**, scenario C, same seeds. The discordant data sits in zoo slot z2: Holm p 0.034–0.039, CI covering 0, same sign as the primary. z1 agrees and z3 has the opposite sign.
  - Shipped: **"holds" (2/3)**, because card §5 counts z2.
  - V05: **"not replicated" (1/3)**.

**O9. Real-data impact** (`V/rerun/summary_reruns.json`, `outputs/`, `reruns.progress.log`)

| Mutant | Real-data result |
|---|---|
| **V26** | H1a "holds (2/3, L3 higher)" → **"not replicated (0/3, L3 lower)"**; the suite still passes 88 |
| V29 | H1a "holds (2/2)": "≥ 2 of 3" silently becomes "2 of 2" |
| V13 / V28 | NeuroSTORM − BrainLM covPR Δ12 3.36 [1.72, 5.01] → 4.57 [3.01, 6.14]; D3 is unchanged |
| V15–V19 | numbers shift; every verdict is unchanged |

Gates (`V/rerun/gate_probes.log`):
- The shipped `verify_card` refuses an edited card (rc 1); V25 runs.
- The shipped re-pool halt refuses (rc 1); V27 runs.
- No test exercises either refusal.

**O10. Why the shipped suite misses these**
- The rule tests feed hand-built records to `replication_verdict`. In `test_verdict_rules.py::_rec`, `p_signflip` defaults to `p_holm`, so primary raw p = Holm p in every primary case.
- No test compares `paired_log_contrast`'s `ci95` with the data.
- The real-data regression `test_frozen_family_b_verdicts_recomputed_from_saved_per_checkpoint_results` replays the rule on the saved JSON `per_checkpoint`. It does not recompute from the saved npz and does not run `topic3_token_stats.py` or `topic3_subject_level.py`.
- `analysis.PARAMS` is pinned by tests only for `signflip_B`, `holm_alpha` and `replication_min_zoo_agree`.

**O11. Addendum 03 / 04 Family B description** (checked against O3)
- Verified:
  - top-7 energy at L2/LN0L2/L3: min 0.999942;
  - eigenvalue count above 1e-5 × max: median 7, max 7 in the primary, up to 8–10 in the zoo checkpoints;
  - |log concatenated − log mean per-frame covPR| ≤ 1.125e-4;
  - H4 160-token / per-frame ratio exactly 1 at L2/LN0L2/L3;
  - checkpoint-variance ratio 13.36 (H1a) and 5.84 (H1b), with ddof 1;
  - the primary medians and their fractions of 7;
  - L1 counts 29–60 and L0 counts 64–209;
  - the L1 jackknife items: 2.78, 3.58, 6.39, 2.84, 2.75, 0.149.
- I confirm the worker's two numeric mismatches: L1 top-63 min = 0.99993998; CI half-widths 0.0020–0.0144.
- **New error (not caught by addendum 04 §6, which checked only "77–88%" from item 2):** addendum 03 §2, H4 row, says "effective ceilings of 383 (D-limited), 63, 7 and 7". H4 PR is computed per frame on 160 subsampled tokens (`token_job.py:82-86`), so `centered_eigs` returns min(159, D) values.
  - The L0 H4 ceiling is **159**.
  - Even the concatenated L0 matrix stores **384** eigenvalues (`cat_cov_eigs_n_values`), not 383.
  - The conclusion (H4 cannot be read as dimensionality changing with depth) stands.
- "Within/between SD 0.003–0.005" holds with the median within-subject SD, the definition the worker's probe used. With the mean it is 0.0032–0.0059. Addendum 03 does not state which definition it uses.

**O12. Provenance details**
- Addendum 03 first entered git in root checkpoint `4ce1917` (2026-10-31T12:31:25Z), as blob 725d5077, the same blob as in `0db0336`.
- This gives a file-based upper bound for the root-reported 12:17:16Z write. Addendum 04 §1 says that write time could not be checked from files.
- Addendum 04 §1 also cites `0db0336` as the commit that "includes" addendum 03. `git log` on that path shows `4ce1917` and `ef27b71` only.
- The pre-edit addendum 03 contains 1 literal BIDS-prefix token; the post-edit version and addendum 04 contain 0. This confirms the worker's ID-scan explanation.
- A newer checkpoint commit, `7430043` (11-01 10:16:26 KST), holds the final addendum 04 (a1828b38). Its pattern matches the root checkpoint job. Reported as context.

**O13. Test-infrastructure hazard**
- In my first mutant run, 3 jobs hung for more than 240 s inside `test_token_job_driver`. The `topic3_token_job.py` `mp.Pool` children were stuck: one in `futex_wait_queue`, one in `pipe_read`, at 0% CPU, under host load 25–49 on 20 cores, with 2 BLAS threads.
- I then SIGKILLed the hung processes. That made 3 false "kills". The run is preserved and marked ABORTED (`V/mutants/run1_ABORTED_README.txt`).
- Run 2 used 1 BLAS thread and per-job timeouts. It had 0 hangs.
- `src/topic3_spectral/__pycache__` (09:39 KST) predates my work and is not mine.

## 2. Logic Chain

1. **Freeze, numbers, verdicts.** O2–O6 show the card governed every real-data result and the numbers reproduce exactly. O3 and O4 apply the card rules from the card text and reproduce every verdict. Those parts are CONFIRMED.
2. **Iteration-1 finding (ii)** was that the tests do not guard the verdict logic (C3/T3.3: "fixtures that fail on the targeted defect").
   - Iteration 2 kills every assigned mutant. I independently confirmed the iteration-1 survivors are killed.
   - But my non-equivalent rule mutants survive (O7), and on reachable inputs they turn a card "killed" or "not significant" primary into "holds" (O8).
   - V01 has the same structure as N08, which the r1 gate treated as blocking: Holm vs raw p, on the other side of the rule.
   - V06–V08 achieve N06's effect ("primary CI ignored") through the statistic instead of the rule line.
   - So finding (ii) is not closed for the verdict logic as such.
3. **Verdict wiring in the scripts (V26, V29)** is guarded only by file hashes, not by tests. V26 flips the real H1a verdict (O9). Because the frozen outputs were produced by hash-verified code (O2, and iteration-1 O6), this does not threaten the current result. It does mean a regression in the real-data verdict path would pass the suite.
4. **Finding (i).** Every Family B number in addendum 03 that I checked reproduces, except the H4-ceiling sentence and the two slips the worker already found (O11). The core restatement holds: the ceiling is 7, the 8 spatial cells are near-static, and replication rests on n = 3 confounded checkpoints. Finding (i) is closed.
5. **Severity.** No real verdict or number changes. The blocking items are a coverage gap in exactly the area the r1 gate failed on, and they are fixable additively: 2–3 new tests, no `src/` change.

## 3. Caveats

- Reachability for V01 and V06–V08 is shown on synthetic arrays, not real data. On the real data every Holm p is 0.0002 and every CI excludes 0, so these mutants cannot change the current verdicts.
- The boundary siblings (V03, V04, V11, V12) need an exact 0.0 bound. That is effectively unreachable for continuous statistics, so I rate them low.
- The parameter mutants (V15–V19) and gate mutants (V25, V27) are protected by `code_sha256_at_freeze.txt` and run-record hashes. Their survival is a test-coverage gap only.
- I did not rerun the connectome token job; I used the saved spectra. I did not rerun the worker's full 67-mutant set; I reran the 8 iteration-1 survivors and checked the receipts of their run 2/run 3 logs.
- Two of my own receipt incidents are disclosed:
  - `V/mutants/run1_ABORTED_README.txt`: false kills caused by my SIGKILL;
  - `V/rerun/CLEANUP_INCIDENT.txt`: `rm -rf rerun/V*` also deleted the stdout logs of the mutant reruns. Their rc lines survive in `reruns.progress.log` and `gate_probes.log`, and their outputs in `outputs/`.
- The M1 and M4 teams were working in parallel. Only topic4 files changed in production during my work.

## 4. Conclusion

**REFUTED (scoped).**

Confirmed:
- T3.2: the card was frozen before results.
- T3.4: numbers and verdicts. H1a "holds" (2/3, both deep NewUAH checkpoints, L3 higher). H1b "not replicated" (1/3). D1 "drop robust and not a per-channel-scale effect". D3 true.
- Finding (i): closed.
- The worker's claims about its own 67-mutant set.

Refuted:
- "Verdict logic now guarded by tests". V01 and V05–V08 survive and change verdicts on reachable inputs. V26 survives and flips the real H1a verdict.

Additive fixes recommended. None needs a `src/` edit or a re-freeze; each is a new test file whose hash is recorded in a new addendum:
- (a) A primary record with raw p < 0.05 but Holm p ≥ 0.05 must not be significant. This kills V01.
- (b) An end-to-end rule test through `paired_log_contrast`/`token_level_checkpoint` on skewed data where Holm p < 0.05 but the 95% CI covers 0. The verdict must be "killed". This kills V06, V07 and V08. Add a zoo variant expecting agreement to count; this kills V05. The seeds in `probe_reachability.py` give such data.
- (c) A regression that recomputes `token_level_checkpoint` and `replication_verdict` from the 4 saved npz, with `PRIMARY` and `ZOO` taken from `topic3_token_stats.py`, and compares them with the frozen JSON. This kills V26, V29, V21/V22, V16 and V18.
- (d) Optionally:
  - pin `analysis.PARAMS` to the card values (V15–V19);
  - a refusal test for `verify_card` and the re-pool halt (V25, V27);
  - correct the H4 ceiling (159, not 383) in the next addendum.

The PI decides the gate; this is the challenger's evidence.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI; V=verification/challenger_M2_r2b_1; PY=/home/juke/superclaude-env/bin/python3
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt            # rc 0, 67 OK
git show 24fe976:docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md | sha256sum        # 68337456…b1e0
PYTHONDONTWRITEBYTECODE=1 $PY $V/probes/probe_family_B_indep.py      # replay_vs_frozen all 0; verdicts holds / not replicated
PYTHONDONTWRITEBYTECODE=1 $PY $V/probes/probe_family_A_indep.py      # max_abs_replay_minus_frozen ~1.8e-15; D1/D3 true
PYTHONDONTWRITEBYTECODE=1 $PY $V/probes/probe_report_tables.py       # 140 OK, 2 MISMATCH (= addendum 03 item 5)
bash $V/make_tree.sh $V/tree_base                                     # copied tree + manifest check
cd $V/mutants && PYTHONDONTWRITEBYTECODE=1 $PY run_mutants.py ../tree_base runX --jobs 4   # expect survivors incl. V01 V05-V08 V26
PYTHONDONTWRITEBYTECODE=1 $PY make_patched_tree.py V01_primary_uses_raw_p ../reach/V01 && \
  PYTHONPATH=$PWD/../reach/V01 OPENBLAS_NUM_THREADS=1 $PY ../probes/probe_reachability.py A   # verdict "holds" (shipped tree: "killed …")
```

Invalidation conditions:
- If a test is added that kills V01, V05, V06, V07, V08 and V26, the refuted part is closed.
- If someone shows that the inputs in O8 cannot arise from `sign_flip_test`/`subject_bootstrap_ci` at the card's B, the reachability claim is withdrawn. These inputs were produced by those functions themselves.
