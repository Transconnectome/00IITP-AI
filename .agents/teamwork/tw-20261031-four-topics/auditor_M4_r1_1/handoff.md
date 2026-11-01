# Handoff — auditor_M4_r1_1 (forensic integrity audit, M4 / Topic 4 redesign). Hard handoff, 2026-11-01T03:10Z

## Forensic Audit Report
**Work Product**: worker_M4_r1 deliverables: src/topic4_resu/, tests/topic4_resu/, scripts/topic4_*.py, results/topic4/2026-11-01/, docs/03_empirical_analysis/topic4/, verification/worker_M4_r1/
**Profile**: General Project. **Integrity mode**: Development. ORIGINAL_REQUEST.md has no "from scratch" or "do not delegate" constraint, so this mode was inferred.
**Verdict**: **CLEAN**. No blocking finding. Eight nonblocking findings are listed in section 4.

## 1. Observation (Phase 1, mode-agnostic; every item measured by me)
O1. **C1 protected hashes** (`LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`, 67 lines): rc 0 at 02:36Z and again at 03:05Z.

O2. **Freeze hashes**.
- `card_sha256.txt`, `code_sha256_at_freeze.txt` and `docs_sha256.txt`: all OK.
- `split_manifest_sha256.txt` (run from the results dir): OK.
- The frozen code list equals the current set of `*.py` files in src/topic4_resu, tests/topic4_resu and scripts/topic4_*.
- Card sha256 is 2b535c39…5934. It is read-only (mode 0444).

O3. **Timeline** (file mtimes, KST−9 = UTC; run_ledger; Bash tool_use commands in the worker transcript; tool outputs and reasoning were not read):

| time (UTC) | event |
|---|---|
| 01:34:30Z | src last written |
| 01:35:14Z | qualify script written, once; run 01:35:24Z; output 01:38:51Z (synthetic; the script never references ENIGMA) |
| 01:36:46Z | T4.1 counterfactual on positions 0 and 932 |
| 01:52:11Z | build_split (lengths and metadata only) |
| 01:55:20Z | synthetic smoke |
| 02:03:56Z | card written by a single Write |
| 02:04:41Z | card_sha256.txt |
| 02:04:49.9Z | first `--stage tuning` command |
| 02:04:52Z | ledger tuning_start, recording card sha 2b535c39… |
| 02:07:42Z | confirm launched; tasks run 02:07:43–02:14:21Z |

- Ledger: 58 rows, with exactly one tuning_start and one confirm_start. 55/55 task rows are ok, and every row's output_sha256 matches the current confirm file.
- Scan for writes to frozen paths after 02:04:41Z: 3 regex hits, all false positives (a metadata edit, a `sha256sum | tee` into the scratchpad, a DISPATCH.md append).
- Real-data execution before the freeze: only the T4.1 script (positions 0 and 932) and build_split (lengths). This matches card §0.

O4. **Cache lead tested and refuted.** The worker's tuning window (02:04:52Z → tuning.json 02:05:08Z, elapsed 15.3 s) seemed to leave no time for a fresh cache build. In my rerun the cache was built from scratch in about 1.6 s (cache file 02:40:05.59Z, ledger 02:40:04Z). The original window is therefore consistent with a fresh cache; nothing suggests a pre-existing one.

O5. **Full independent rerun from raw ENIGMA npy on DGX-Spark CPU.**
- Setup: copy dir `verification/auditor_M4_r1_1/rerun/r` (outputs stripped first), fresh cache in the scratchpad (deleted afterwards), `--procs 4`, nice.
- tuning.json is identical to production in every field except elapsed_s.
- **All 55 confirm/*.json files are byte-identical to production.** Max |Δ| in R²/MSE is 0; there are no engine or MLP digest mismatches.
- **verdict.json is byte-identical** (sha 437161ed…5c22).
- Hashes: `verification/auditor_M4_r1_1/rerun/rerun_outputs_sha256.txt`.

O6. **Independent recompute** (`verification/auditor_M4_r1_1/probes/recompute_verdicts.py`). It does not import `stats`, `topic4_analyze` or any worker script, and uses its own bootstrap with RandomState(777).
- Point estimates equal verdict.json exactly:
  - H1 −0.0022309;
  - S1 −0.0015974;
  - S2 +0.0306165;
  - S3 −0.0046691.
- CIs agree within Monte Carlo error. H1 95% CI: mine [−0.00414, −0.00032], theirs [−0.00413, −0.00042].
- The verdicts are re-derived from the card text: stop / killed / supported / non-inferior. All four agree.
- Execution-integrity counts are identical (C3 10/50; every other class 0).
- Structural checks:
  - 1014 test subjects, each tested once;
  - the confirm set equals the manifest's;
  - fold membership matches;
  - no tuning subject is tested;
  - unstable runs carry no scores and stable runs have finite scores;
  - the constant predictor is ≤ 0 for every subject.

O7. **Independent population and split check** (`probes/check_population_split.py`). It uses the M1 TR table loaded from file, my own valid_T computation and my own salted-hash rule written from the card text.
- 1195 TR = 2.0 subjects, 0 short, 0 internal-zero.
- The primary set, sites, valid_T and raw_valid_T all equal the manifest.
- No burned position is in the primary set.
- The role and fold assignment matches exactly: 181 tuning, 1014 confirm.
- Manifest keys: position, site, valid_T, raw_valid_T, role, fold, position_hash. There are no IDs.

O8. **T4.1 counterfactual rerun** to `verification/auditor_M4_r1_1/t41/`: byte-identical to production.
- Position 932: protected-function R² is 0.040, 0.053, 0.051, −0.082, 0.024, 0.024; ss_tot 5331; persistence 0.9916.
- The cited legacy lines are confirmed: `src/fractal_motif_resu.py` :417 split, :425 `max(ss_tot,1e-8)`, :349–352 global eigen-rescale, :544 hard-coded `zero_torch_autograd_confirmed: True`.

O9. **Qualification rerun** to `verification/auditor_M4_r1_1/qual/`: identical to production except elapsed_s. Q1–Q6 pass at η0 = 0.02.

O10. **Tests** (my runs; logs in `verification/auditor_M4_r1_1/logs/`):
- tests/topic4_resu: 67 passed in 26 s;
- old suite (STRICT_E2E=1): 86 passed;
- tests/topic1_lagmotif: 88 passed.

O11. **Mutation, worker harness replayed.** I ran an unmodified copy (sha 89e2307…) in `verification/auditor_M4_r1_1/worker_mutants_replay/`.
- Control rc 0, "63 passed". The harness deselects `test_tuned_mlp_encoder_reaches_rrr24`, which together with the narrower control file set explains 63 versus 67.
- The kill map is identical to the worker's receipt: 17 killed, and the CONTROL_targets_wired_but_unused mutant survives as designed.

O12. **Mutation, my own 8 mutants** (`probes/run_auditor_mutants.py`, output `auditor_mutants.out.json`). Control passed.
- Killed (6):
  - facade engine with no learning;
  - transform replaced by PCA (facade);
  - sign flip in the lateral Hebbian rule;
  - stability monitor that always returns ok;
  - λ chosen on test subjects;
  - PSP fitted on train + test.
- **Survived (2):**
  - `split_ignores_site_strata`: test_split derives "site" from the output of the code under test;
  - `bootstrap_fixed_width_facade` (point ± 0.004): test_stats checks only coverage and width < 0.01.
- An extra mutant changing a TR-table entry (Bangalore 2.0 → 1.8) is killed by `test_vendored_tr_table_equals_live_topic1`, so addendum_01 item 7 holds.

O13. **No-backprop proof (code read).**
- local/ imports only numpy and hashlib.
- The AST test forbids torch, importlib, `__import__`, eig and svd, and the rule function contains no calls.
- Runtime subprocess test with autograd frameworks blocked.
- Target-invariance digest test.
- `np.linalg.solve` is used for the steady state; this is disclosed, and the relaxation-equality fixture passes.
- `MaskedPSP.fit(X, monitor)` takes no targets.

O14. **Participant IDs.** I scanned for full directory names and for 1316 distinctive digit-bearing tokens (`probes/id_leak_scan.py`).
- Scope: 374 files across all M4 code, results, docs, worker verification and metadata, both explorers' verification dirs, and the scratchpad `det` copy.
- 0 hits; only counts were printed.
- Confirm outputs store test positions only.

O15. **Compute, B300 and env.**
- gpu_ledger has no M4 rows (M3 explorer rows only, 0.142 GPU-h in total).
- The worker transcript contains no ssh, scp or rsync, no 61.107 address or /scratch path, no pip/uv/conda install, and no reference to envs/swiftllm.
- The Python used is /home/juke/superclaude-env, the env the dispatch designates.
- No M4 artefact was found to have reached B300. I did not contact B300 myself.

O16. **Git.**
- The worker transcript contains no git add, commit, push, stash, reset, checkout, restore, rm, mv, tag, merge or rebase.
- M4 code, tests, scripts and results are untracked.
- The card, docs and worker metadata appear in commits c967f7c (11:16:27 KST) and 471f8e8 (11:31:27 KST). These are "Automatic background checkpoint" commits on an exact 15-minute cadence carrying a different Claude-Session footer: the root-session job, not the worker.

O17. **Code reading** (no hardcoded results, no facades).
- `stats.py` verdict functions implement card §6 exactly.
- The tuning gate `G_c_guard_never_fired = {"pass": True}` is set only when no `DegenerateTargetError` was raised. Otherwise the except branch sets it false, and `all_gates_pass` requires all 3 gates. It is a real gate, not a hardcoded pass.
- `verify_integrity` in `topic4_run.py` checks the card, code and manifest hashes, and also checks that the assignment equals the split rule.

O18. **Layout lint** (`audit_layout.py` on the run metadata root): PASS, 183 files, 0 findings.

O19. **Post-audit production state**:
- C1 rc 0;
- card, code and docs hash files rc 0;
- split manifest OK;
- `output_sha256.txt`: 72/73 OK. The failing entry is `logs/analyze.log`, recorded as e3b0c442… (the sha256 of an empty file). The script hashed its own stdout log while that log was open and still empty. The current log content matches verdict.json.

## 2. Logic Chain
1. O5 rules out fabricated or non-reproducible outputs. An independent rerun from raw data, on a fresh cache and with outputs stripped, reproduces every confirm file and verdict.json byte for byte.
2. O6 rules out an analysis facade or a hardcoded verdict. Separate code and a separate RNG give the same point estimates and verdicts, and CIs within Monte Carlo error.
3. Three sources together show the card was frozen before any primary-population outcome:
   - O3: the transcript order, plus the ledger row that records the card sha at tuning start;
   - O2: hashes unchanged;
   - O4: the cache timing lead was refuted.

   The T4.1 data (positions 0 and 932) and the build_split lengths were accessed before the freeze. Card §0 discloses both, and neither is in, nor an outcome on, the TR = 2.0 population (O7).
4. O7 and O6 rule out split leakage or contamination of the confirm set.
5. O10–O13 show the tests are substantive and can fail on targeted defects (6/6 of my facade and leak mutants killed; the worker's 17 replayed). The two survivors are coverage gaps. Their production behaviour is independently verified by O7 (stratification) and O6 (bootstrap), so they hide no defect in the shipped results.
6. O14–O16 show no ID leakage, no B300 or GPU use, no other project's env, and no git writes by the agent.
7. Every observation that could map to a Development-mode flag (hardcoded results, facade, fabricated verification) was checked and none holds. **CLEAN.**

## 3. Phase 2 — Development-mode flagging
| Observation | Development | Finding |
|---|---|---|
| Hardcoded test results | FLAG if present | none (O12, O17) |
| Facade implementation | FLAG if present | none: the engine and analysis facade mutants were killed, and the outputs reproduce (O5, O6, O12) |
| Fabricated verification output | FLAG if present | none: confirm, verdict, t41, qualification and mutation receipts all reproduce (O5, O8, O9, O11) |
| Library reuse (numpy, scipy, torch for the baseline) | OK | permitted |

### Dispatch checklist: one line per named category
| Category (dispatch) | Determination | Evidence |
|---|---|---|
| Hardcoded results | PASS | O17 (the G_c `{"pass": True}` is set only when no exception was raised); O5 and O6 |
| Facades | PASS | O12 (engine and PCA facade mutants killed); O5 and O6 |
| Tests that cannot fail | PASS (these are coverage gaps, not a violation) | Three leads, each corroborated. (a) The vacuous hash test was disclosed by the worker (addendum item 7), and the real guard kills TR drift (O12). (b) The stratification test reads "site" from `assign()`'s own output, so its mutant survives; the production split is reproduced independently (O7). (c) The fixed-width bootstrap facade survives `test_stats`; the production CIs are reproduced by an independent bootstrap (O6). No claim rests on these tests. |
| Fabricated or non-reproducible logs | PASS | Byte-identical reruns of the confirm and verdict files (O5), T4.1 (O8) and qualification (O9); replayed mutation receipts (O11). Benign defect: the analyze.log self-hash (O19). |
| Results before the card freeze | PASS | O3, O4: transcript and ledger order; the only pre-freeze real-data runs are T4.1 (positions 0 and 932) and the build_split lengths, both disclosed in card §0 |
| Silent fallbacks | PASS (latent only) | `topic4_analyze.py` would NaN-fill a missing arm or fold without reading task statuses. This was never exercised: 55/55 tasks ok in the ledger, and the rerun is byte-identical (O3, O5). Recorded as nonblocking 6. |
| Participant-ID leakage | PASS | O14 (0 hits in 374 files); positions only in outputs |
| Writes to protected or external paths | PASS | O1 and O19 (C1 rc 0 before and after); the enigma_ocd_mbbn files modified today are logs of another workstream, and the worker transcript shows no writes there |
| ENIGMA-derived file on B300 | PASS (as far as the evidence reaches) | O15: no ssh, scp or rsync and no /scratch path in the worker transcript; B300 nodes themselves were not inspected |
| GPU use against the ledger and cap | PASS | O15: no M4 ledger rows and no B300 contact; `backprop.py` and the scripts never call cuda, .to() or device, so local GB10 GPU use is also 0 |
| Another project's env | PASS | O15: only /home/juke/superclaude-env (designated); no envs/swiftllm |
| Git writes by agents | PASS | O16: no git write commands in the worker transcript; the M4 commits are the root's automatic 15-minute checkpoints |

## 4. Caveats
Nonblocking findings, which do not change the verdict:
1. `tests/topic4_resu/test_split.py` cannot detect loss of site stratification: the mutant survives because the test reads "site" back from `assign()`'s output. Production is independently verified (O7).
2. `tests/topic4_resu/test_stats.py` cannot detect a fixed-width CI facade: it checks coverage and width < 0.01 only. Production CIs were independently reproduced (O6).
3. `test_vendored_source_hashes_recorded` is vacuous. The worker disclosed this (addendum_01 item 7), and the behavioural-equality test does kill TR drift.
4. `results/topic4/2026-11-01/output_sha256.txt` is not self-consistent: its analyze.log entry is the empty-file hash. Fix: exclude logs/ or hash after the stdout log is closed.
5. Card §8 says the torch version is recorded in the ledger. The ledger env rows contain only python, numpy, platform and omp_threads.
6. `topic4_analyze.py` does not consult `confirm_summary.json` or ledger statuses. A missing or halted task would silently become NaN for that arm in that fold; class_scores would raise only if every instance were missing. This did not occur (55/55 ok).
7. `__pycache__/*.pyc` appeared under `src/topic4_resu/` and `src/topic4_resu/local/` at 02:41:39Z and 02:51:22Z.
   - This is after worker_M4_r1 finished (02:33Z) and after my 02:36Z `find` showed none.
   - My non-`-I` runs set PYTHONDONTWRITEBYTECODE. Of my `-I` probes, only `check_population_split.py` loads anything from src: it loads `src/topic1_lagmotif/tr_table.py` via `spec_from_file_location`, and `-I` ignores PYTHONDONTWRITEBYTECODE. That `.pyc` kept its 08:29:58 KST mtime and lies outside topic4_resu, so the stray topic4 files are not mine.
   - The likely writers are the concurrent M4 challenger and reviewer agents. Not deleted, since they are not mine.
   - The `*.py` freeze hashes are unaffected.
8. The protocol was not committed before the results (G5 wording): the card entered git at 11:16 KST through the root checkpoint, after confirm. C4 forbids agent git writes, so freeze provenance rests on mtimes, the ledger and the transcript (O3).

My own deviations and limits:
- **CPU.** My full rerun took 14 min wall and about 80 CPU-minutes (51 user + 29 sys, inflated by host load ≈ 20). This exceeds the dispatch's "<20 min CPU" condition for verifier reruns, although it stayed within the cap of 4 processes and ran under nice.
- **Process count.** During the overlapping mutant, T4.1 and qualification launches I ran at most 4 Python processes, at the cap.
- **ENIGMA-derived files.** `verification/auditor_M4_r1_1/rerun/r/` holds ENIGMA-derived per-subject scores (by position only, byte-identical to production). They must stay off B300. The auditor cache was deleted.
- **Transcript use.** I read the worker's subagent transcript, restricted to Bash/Write/Edit tool_use inputs matched by regex, to corroborate timeline, git, ssh and install claims. I did not read its reasoning or tool outputs.
- **DISPATCH.md.** The instruction text is verbatim; the embedded worker JSON was condensed.
- **Not checked.** I did not contact B300 nodes. I did not review scientific adequacy beyond integrity (the analyst-set δ and the 6000-update budget are methodological choices the PI must confirm).

## 5. Conclusion
**CLEAN.** The M4 results are genuine and reproducible from raw data. The verdicts follow the frozen card's rules, which were frozen before any primary-population outcome. There are no ID leaks, no B300 or GPU use, no other project's env and no agent git writes. Addressing nonblocking items 1, 2, 4 and 6 would harden the suite for future runs. The scientific gate (δ and the PI decision) is outside this audit.

## 6. Verification Method
```
cd /home/juke/git/00IITP-AI && export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=.
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?          # 0
LC_ALL=C sha256sum -c results/topic4/2026-11-01/{card_sha256.txt,code_sha256_at_freeze.txt,docs_sha256.txt} | grep -vc ': OK'   # 0
/home/juke/superclaude-env/bin/python3 -I verification/auditor_M4_r1_1/probes/recompute_verdicts.py results/topic4/2026-11-01 results/topic4/2026-11-01/verdict.json
/home/juke/superclaude-env/bin/python3 -I verification/auditor_M4_r1_1/probes/check_population_split.py
diff <(cd verification/auditor_M4_r1_1/rerun/r/confirm && sha256sum *) <(cd results/topic4/2026-11-01/confirm && sha256sum *)   # empty
# Full rerun, copy-first. Do NOT run rerun/run_rerun.sh in place: it would overwrite the evidence in rerun/r.
N=verification/<new_owner_dir>/rerun; mkdir -p $N && cp -r results/topic4/2026-11-01 $N/r && \
  (cd $N/r && rm -rf confirm run_ledger.jsonl* tuning.json verdict.json output_sha256.txt confirm_summary.json logs docs_sha256.txt)
cp verification/auditor_M4_r1_1/rerun/run_rerun.sh $N/   # then edit two lines by hand: V=<abs path of $N/..>, CACHE=<new scratchpad dir>
bash $N/run_rerun.sh    # ~7-14 min wall, 4 procs; then: diff <(cd $N/r/confirm && sha256sum *) <(cd results/topic4/2026-11-01/confirm && sha256sum *)
```
The conclusion is invalidated if any of the following holds:
- a confirm file differs from the rerun;
- the recompute verdicts differ;
- the card, code or docs hashes fail;
- a transcript or ledger record shows a TR = 2.0 forecasting run before 02:04:41Z.
