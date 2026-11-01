# handoff — auditor_M3_r1_1 (forensic integrity audit, milestone M3 / Topic 2) — HARD, 2026-11-01T06:20Z

## Forensic Audit Report

**Work Product**: worker_M3_r1 deliverables for M3. These are `src/topic2_rgpool/`, `tests/topic2_rgpool/`, `scripts/topic2_*.py`, `scripts/b300_env/`, `results/topic2/2026-11-01/`, `docs/03_empirical_analysis/topic2/`, the worker's ledger rows, and B300 .98 `/scratch/iitp4/worker_M3_r1/`.
**Profile**: General Project. Integrity mode is **Development**: ORIGINAL_REQUEST has no "from scratch" or "no delegation" constraint, and C7 explicitly allows copying external code.
**Verdict**: **CLEAN**

I found no hardcoded results, no facades, no fabricated or non-reproducible logs, and no result computed before the card freeze. There was no participant-ID leakage, no protected or external write, no ENIGMA-derived file on B300, no GPU use missing from the ledger or above the cap, no use of another project's env, and no git write by an agent.

There are four non-blocking findings (plus the C4-print ruling and the out-of-scope notes in §3):
- the test suite has coverage gaps (5 of 11 mutants survive);
- the docs are stale on the PI decisions;
- the subject pseudonyms are unsalted content hashes;
- one silent default in `topic2_verdict.py`.

### Phase Results
- **C1 protected hashes**: PASS. `sha256sum -c PROTECTED_HASHES.txt` rc 0, 67/67 OK (`verification/auditor_M3_r1_1/c1_protected.txt`).
- **Card frozen before results**: PASS.
  - `card_sha256.txt` check: rc 0, 8/8.
  - The host checkpoint commit `51609c1` (03:16:27Z, not an agent commit) holds the card with the same sha c9bfc60a…41f5. The card has not changed since.
  - Every governed run started after the freeze: the first started at 03:16:17Z. HCP partitions were built at 03:17:07Z and Stage 0 ran at 03:24:55Z (B300 mtimes).
  - The pre-result report versions (`c67403f` at 04:01Z, `b2334c5` at 04:31Z) contain `STAGE1_VERDICT_PLACEHOLDER`. No verdict was written in advance.
  - Addendum 02 was committed at 04:01:27Z, before the first HCP test value at 04:10:48Z. Addendum 03 was committed at 04:46Z, before wave 4 ended at 05:09Z.
- **Code frozen**: PASS.
  - `code_sha256_at_freeze.txt` check: rc 0, 33 files.
  - All 27 `run.json` `code_sha256` values equal the frozen src hashes.
  - The B300 code copy equals the frozen hashes for every src/script file. The one exception is `topic2_id_scan.py`, which was added after the freeze and is disclosed in addendum 01.
- **Output pins**: PASS. `output_sha256.txt`: 43/43 OK. It was re-pinned at 05:37:35Z, after the last report edit.
- **Run records genuine (not fabricated)**: PASS.
  - The 27 local `run.json` files are byte-identical to the B300 originals.
  - The 15 Stage-1 checkpoints exist on B300, with mtimes equal to their `run.json` mtimes.
  - **Independent re-evaluation** on idle GPU 7 (B300 .98), using the frozen code copy and the checkpoints, gave the following:
    - The saved `perm` buffer equals the claimed arm key in 15/15 checkpoints (E→E, C→C, S_s→S_seed{s}).
    - Test NMSE reproduced **bit-exactly** (|Δ| = 0.0, `den` and `num` max relative diff 0.0) for `hcp_E_s2`, `hcp_C_s2`, `hcp_S_s2` (the stalled run: 1.0000014706756435) and `hcp_C_s0`.
    - Facade control: the C weights with an identity gather give different reconstructions (max abs diff 2.61 and 1.84) and a worse NMSE (0.99008 vs 0.98862; 0.98950 vs 0.98855).
    - Output: `verification/auditor_M3_r1_1/reeval.out.json`.
- **Internal consistency** (`probe_runs.py`, 0 problems):
  - each `test_nmse` equals Σnum/Σden;
  - `val_nmse_curve` equals the `train_log` val events;
  - one `done` event per run, and train-log steps run continuously from 100 to 8700 (no hidden reruns);
  - the `stdout` final line matches;
  - perm sha, perm-file sha and split sha match;
  - settings are identical across all 27 runs;
  - the launched GPU equals `cuda_visible`;
  - `test_den` is identical across all 15 HCP runs, which confirms identical evaluation masks and data.
- **Verdict recomputation**: PASS. My independent scipy t-intervals give the following:
  - I1 = +0.1468 % [−0.0677 %, +0.3614 %];
  - I2 = +0.4733 % [+0.00098 %, +0.9455 %];
  - F+ gate: C vs E +3.06 %, C vs S +2.93 % (pass);
  - F− gate: −1.74 % (pass).
  - Applying the card §8 rules gives **stop**, identical to `verdict.json`.
- **Hardcoded / facade source scan**: PASS.
  - No outcome literals were found in src, tests or scripts. The only "stop" literals are the rule label in `stats.py` and the rule-mapping tests on synthetic intervals.
  - The only test that reads `results/` is the C4 ID check.
  - `fill_report.py` renders the report tables from `verdict.json` and `stage0_hcp.json` only.
- **Tests run by me**: PASS. `tests/topic2_rgpool`: 55 passed. Old suite (`test_empirical_four_topics`, `test_pilot_connectome`, `e2e`): 86 passed.
- **Vacuous or self-certifying tests**: PASS (none found). Every existing check fails on the defect it targets. The tests compute independent references, for example `m.reduction(m.norm(concat))` in `test_merge.py`, or use hand-checked inputs.
- **Coverage gaps** (non-blocking note, not a failed check): 11 mutants were applied to copies under `verification/auditor_M3_r1_1/mut/`; baseline is 52 passed (with `test_outputs_no_ids` excluded).
  - **Caught (6):** stop rule using `lo`; keep ignoring I2; merge ignoring perm; C arm using Euclidean distance; partition reading val/test subjects; S surrogate without shuffle.
  - **Survived (5):**
    - `relative_gain` sign flip;
    - NMSE metric ignoring the SimMIM mask;
    - training loss ignoring the mask;
    - split rule changed (test taken from the end);
    - HCP eval-mask seed randomised. The CPU suite exercises only `evaluate_fixture`.
  - Each survivor was checked directly instead:
    - code reading of `metrics.py:19`, `train.py:209` and `stats.py:29`;
    - independent recompute of I1 and I2;
    - independent split recompute from the manifest, which equals `split.json`;
    - identical `test_den` across runs.
  - These are coverage gaps, not facades. The worker's mutant claims are limited to merge and partition defects, and those claims are true.
- **Data / split / leakage**: PASS.
  - The split was recomputed from the manifest under the card §4 rule and is identical. Train, val and test are disjoint (64/8/16).
  - The structural leakage test kills the "partition reads test subjects" mutant.
  - On B300:
    - exactly 5 source dirs match the explorer's burned salted hashes, and they are the first 5 in sorted order;
    - their content pseudonyms are in neither the manifest nor the split;
    - 93 files existed before the manifest started, which explains the 10 later arrivals that were not used;
    - the manifest equals the split union.
- **C4 participant IDs**: PASS.
  - My local scan held the 1,084 B300 HCP directory names in memory only. It covered 282 text files across `results/topic2`, all of `docs/03_empirical_analysis/`, `verification/worker_M3_r1`, both explorers' verification and metadata dirs, worker metadata, code, tests, `scripts/topic2_*` and the ledger. Result: **0 hits** (`id_scan_local.out.txt`).
  - A re-run that includes my own outputs is recorded in progress.md.
- **C5 compute / ledger**: PASS.
  - Worker run GPU-h, recomputed launch-to-end from the `run.json` and `launched.json` files: 11.678. Adding smoke 0.035 gives 11.73, which matches the ledger.
  - Run-wide completed rows: 11.943 GPU-h, below the cap of 64. M3 sub-cap: 14.
  - Every B300 GPU job found (two smokes, 4 waves, both explorers' probes) has ledger rows. The explorers' Stage-0 dev probes were CPU-only.
  - Env: `/scratch/iitp4/worker_M3_r1/venv`, a uv venv with `include-system-site-packages = false`. `lock.txt` is identical to the repo copy. `~/envs/swiftllm` was not used.
- **C6 / ENIGMA**: PASS.
  - No ENIGMA name or reference appears in the worker code, logs or stdout, and no file under `/scratch/iitp4` has an ENIGMA name.
  - HCP use is covered by PI_DECISIONS item 2.
- **C7 external repos**: PASS.
  - The vendored ver11 and patchembedding are byte-identical to SwiFT_v2 `f0dc7aca` (`git show` sha256).
  - SwiFT_v2's uncommitted modifications date from 2026-10-21 and 2026-10-26, before this run.
  - Nothing was written into `/scratch/data/hcp`.
- **No installs on DGX-Spark**: PASS. No `superclaude-env` or `~/.local` site-packages entry is newer than 11:00 KST.
- **Git writes by agents**: PASS.
  - All commits 02:00Z–06:01Z fall on the host checkpoint cadence (:01, :16, :31, :46, at +26–28 s).
  - The reflog shows only those commits. There is no stash, reset or checkout.
  - The new M3 code is untracked.
- **Orphan processes**: PASS. No topic2 processes remain on B300, and `auto_wave4.sh` has finished locally.
  - The remaining local `ssh -J dgx1` processes are ControlPersist mux masters (`cm-eocd-*`) or belong to other live verifiers. None is a worker job.
- **Layout**: PASS. Whole-run `audit_layout.py`: rc 0, 207 files, 0 findings.

### Evidence
All raw outputs are in `/home/juke/git/00IITP-AI/verification/auditor_M3_r1_1/`:
- `c1_protected.txt`
- `probe_runs.py` and `probe_runs.out.json`
- `b300_inventory.sh` and `b300_inventory.out.txt`
- `b300_runjson_sha.txt`
- `b300_burned_check.py` and `b300_burned_check.out.json`
- `id_scan_local.py` and `id_scan_local.out.txt`
- `tests_topic2.txt` and `tests_old86.txt`
- `output_sha_check.txt`
- `reeval_ckpt.py`, `reeval.out.json` and `reeval.log`
- `mut/run_mutants.py`, `mut/run_mutants.log` and `mut/mutants_result.json`
- `audit_layout_whole_run.txt`

## 1. Observation
- `results/topic2/2026-11-01/runs/*/run.json` (27). The verdict inputs are reproduced in `probe_runs.out.json`. `verdict.json` gives `"verdict": "stop"`; its `I1_t.hi` = 0.003613539013171975 < δ 0.01.
- `reeval.out.json` (B300 .98 GPU 7, 05:56:43–05:57:26Z) gives `abs_diff_nmse` 0.0 for all 4 re-evaluated runs, and `equals_claimed` true for 15/15 perm buffers.
- `git log` shows card commit `51609c1` at 12:16:27 KST = 03:16:27Z. Every commit in the window carries the subject "docs(iitp): checkpoint four-topics teamwork documents".
- Mutation log: 6 caught, 5 survived (listed above).
- Ledger: my rows are at 05:56:27Z (started) and 05:57:26Z (completed, 0.02 GPU-h, auditor_M3_r1_1).

## 2. Logic Chain
1. Fabrication would require `run.json` values that the code and checkpoints cannot produce. The frozen code copy plus the saved weights reproduce the recorded test NMSE bit-exactly. The checkpoint perm buffers match the claimed arms. So the Stage-1 numbers come from real training runs of the claimed arms (Phase Results, re-evaluation).
2. Results-before-freeze would require a governed computation before 03:14:34Z. The run start times, the partition and Stage-0 mtimes on B300, and the host-committed card sha all place the freeze first. The only pre-freeze real-data step was QC and preprocessing, which the card §0 discloses.
3. Verdict manipulation would show as a mismatch between `verdict.json` and an independent computation. There is none: my scipy t-intervals and card-rule mapping give stop. The kill holds for either sign convention of the minor-effect contrasts.
4. A facade gather would show as identical outputs under different perms. The re-evaluation shows the C weights behave differently, and worse, under the identity gather, and the merge mutant is caught by tests.
5. Leakage or ID or C6 violations would show in the partition inputs, in the outputs, or on B300. The leakage mutant is caught, the split is reproduced, the burned subjects are excluded, the ID scan has 0 hits, and no ENIGMA file exists in M3 paths.
6. The surviving mutants show untested lines. In each case I verified the shipped line directly, and it is correct. They lower confidence in the suite's ability to catch future regressions, but they do not show a current defect. So: non-blocking.

## 3. Caveats
- I did not re-run the full pilot or any training; re-evaluation covered 4 of 15 Stage-1 checkpoints, and the perm buffers covered all 15. I did not re-evaluate the fixture runs: they have no saved checkpoints.
- **Ruling on the worker's self-disclosed C4 print** (non-blocking; for root or the PI to accept). At about 03:32Z the worker printed one real-format HCP ID literal in transient local tool output.
  - It was a publicly documented example, typed by hand and not derived from data.
  - The worker disclosed it itself.
  - No file contains it: 0 hits over 308 files, including my own outputs.
  - Concealment would be a violation; this was self-disclosed. I cannot verify the transcript itself.
- **My own DISPATCH.md format.** I kept the computed task text verbatim but moved the inline worker-handoff JSON into a separate verbatim section, leaving a pointer in its place. No content was abbreviated.
- I did not inspect the perlmutter SwiFT fork. I did not audit HCP family structure, which is unavailable.
- **Non-blocking findings:**
  - **(a) Test coverage gaps:** the 5 surviving mutants above.
  - **(b) Stale documentation.** The card, report §6 and the handoff say δ and HCP-as-public are "pending PI". `orchestrator/PI_DECISIONS_2026-11-01.md` items 2 and 3 already decide both: HCP counts as public, and δ = 1 % for M3. The values match, so nothing changes, but the report text is stale. Also, `vendor_swift_ver11/SOURCE.md` cites `tests/topic2_rgpool/test_vendor_provenance.py`, which does not exist; the check lives in `test_leakage_and_provenance.py::test_vendored_ver11_is_byte_identical_to_recorded_source`.
  - **(c) Unsalted pseudonyms.** The pseudonyms are unsalted sha256 prefixes of the HCP file content. `hcp_manifest.json` also stores the full `content_sha256`. Anyone holding the HCP release can map these to HCP subject IDs. These are pseudonymous codes, not persons, so this is not re-identification under the HCP DUT. C4, however, names "positional index or salted hash". Recommendation: salt them in any future card.
  - **(d) Silent default in `topic2_verdict.py`.** It passes `fm is not False`, so a *missing* F− gate counts as a pass. That did not matter here, because the F− gate was computed (pass = true).
- **Out of M3 scope, for root:**
  - Another workstream's ENIGMA-OCD mbbn/palm GPU jobs were running on .98 GPUs 0–3 from about 05:41Z. PI_DECISIONS item 5 (about 05:3xZ) records that the PI relaxed C6 for ENIGMA on B300. M3 ended at 05:09Z and has no ENIGMA files.
  - The explorer salt file sits next to the salted dev-subject hashes in `verification/explorer_M3_r1_1/`, so those hashes are brute-forceable. This is a C4 concern for root. The worker also copied that salt to the B300 code dir.
  - About 133 GB of preprocessed HCP, plus checkpoints, remain in `/scratch/iitp4/worker_M3_r1`, on ephemeral storage.

## 4. Conclusion
**CLEAN.** The M3 work product implements what it claims:
- the T2.1 architecture facts hold in the vendored code (three merges at stages 0–2, an `mlp` decoder);
- the frozen card preceded every governed computation;
- the reported Stage-1 numbers are reproduced from the checkpoints;
- the card's verdict, **stop**, follows from the run records.

Non-blocking items (a)–(d) should be fixed in a follow-up: add tests for the mask, sign and split rules, and update the report to cite PI_DECISIONS. None of them changes the verdict.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/card_sha256.txt | sha256sum -c
sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-01/output_sha256.txt | sha256sum -c
git show 51609c1:docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md | sha256sum   # c9bfc60a…41f5
/home/juke/superclaude-env/bin/python3 -I verification/auditor_M3_r1_1/probe_runs.py /home/juke/git/00IITP-AI   # N_PROBLEMS 0
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool -q
python3 -I verification/auditor_M3_r1_1/mut/run_mutants.py    # copies only; 6 caught / 5 survive
# B300 (≤0.05 GPU-h, ledger rows first): copy reeval_ckpt.py to an own /scratch/iitp4/<id>/ dir and run with the worker venv, python -B
```
**Invalidation conditions:** this audit is invalid if any of the following happens:
- any hash check above fails;
- a `run.json` or checkpoint on B300 changes;
- the re-evaluation gives |ΔNMSE| > 1e-4;
- `probe_runs.py` reports a problem;
- the PI reverses PI_DECISIONS items 2 or 3.
