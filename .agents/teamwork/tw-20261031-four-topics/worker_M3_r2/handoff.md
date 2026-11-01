# handoff — worker_M3_r2 (M3 / Topic 2, iteration 2 = last iteration) — Hard

Written 2026-11-01 ~09:00Z. Parent: root coordinator. Host: claude-code subagent (agent id a1d166b45da8b59da,
workflow wf_5bb8fefb-ae0). GPU used: 0 GPU-h (no ledger row). Git writes: none. Installs on DGX-Spark: none.
No subject token, content hash, file size, salt or HCP ID is written in any file of mine (count-only scans).

## 1. Observation

- **r1 gate blocker B1 (C4)** reproduced as described: 19 files under `results/topic2/2026-11-01/` carried unsalted
  content-hash subject tokens (+ full content sha256, exact file size, per-subject n_brain_vox and sec in the
  manifest). Positive-control count-only scan (`verification/worker_M3_r2/preflight_token_scan.json`): exactly those
  19 files; the precise pattern detector flagged exactly the same 19 files; 3 unrelated numeric coincidences in
  Topic 4 files.
- **Preflight** (07:21Z): C1 67/67 rc 0; card pins 8/8; output pins 43/43; code freeze 33/33
  (`verification/worker_M3_r2/preflight_*.txt`). PROTECTED_HASHES lists no topic2 file.
- **Seal** (07:28Z): the 19 originals were copied by tar over ssh to B300 61.107.201.98
  `/scratch/iitp4/worker_M3_r2/sealed_c4/<repo-relative path>` (dirs 700, files 400); 19/19 sha OK there; the 18 old
  pin lines pass there (`sha256sum -c --ignore-missing`). preprocess.log was unpinned before; now recorded.
- **Sanitize** (new `scripts/topic2_c4_sanitize.py`, stdlib only): tokens → `h00..h87` in original manifest order
  (asserted sorted by content hash); manifest subjects → {pseudonym, qc, T}; quoted-token value swap only in
  split/stage0/15 hcp run.json (re-parse check); per-line sec dropped from preprocess.log; 520 replacements.
  Before overwriting: in a scratchpad mirror the frozen `scripts/topic2_verdict.py` reproduced `verdict.json`
  byte-identically (59af05e5…caf68) and stdout = `logs/verdict_stdout.txt`; the 55 shipped tests passed.
- **Replace** (07:33Z) via same-dir temp + `os.replace`. New pins `results/topic2/2026-11-01/c4_sealed_originals_sha256.txt`
  (sha 18d661bf…7570), `c4_sanitized_sha256.txt` (7a4cceab…b87ca), `output_sha256_r2.txt` (f463fbe7…0876, 156 lines).
- **Seal checker** `scripts/topic2_c4_seal_check.py`: repo mode all_ok (R1 19/19; R2 33 old-pin lines pass, exactly 18
  fail and each equals its sealed-original hash; R3 embedded provenance = originals; R4 tokens consistent, manifest
  fields [T, pseudonym, qc]; R5 output_sha256_r2 passes) → `verification/worker_M3_r2/final_seal_check_repo.json`.
  Sealed mode on B300 with system python3 3.12.3: S1 19/19, S2 18/18, S3 re-sanitize reproduces 19/19, S4, S5 split
  64/8/16 → `verification/worker_M3_r2/seal_check_sealed_b300_1.json`.
- **Post scans**: working tree 15,876 files, 0 files with an original token, pattern detector 0
  (`post_token_scan.json`; only the same 3 Topic 4 numeric coincidences). Git history: 50 revisions since
  2026-10-30, 176 patterns fed through a pipe, 0 hits (rc 1); positive control 33 hits (`git_history_token_scan.txt`).
- **Verdict reproduction on the repo runs** (08:45Z, DGX-Spark superclaude-env): byte-identical verdict.json and
  stdout (`final_verdict_reproduction.txt`). In the B300 venv (scipy 1.18.1 vs 1.15.3) only t_crit and the interval
  ends differ, ≤ 9e-13 relative.
- **New tests** (all pass on frozen code): `tests/topic2_rgpool/test_c4_tokens_r2.py` (8),
  `test_verdict_path_guards_r2.py` (10; 4 adopted from explorer_M3_r2_2), `test_pipeline_guards_r2.py` (19).
  Suite now 92 tests.
- **Mutation** (`verification/worker_M3_r2/mutation/`): v1 local INVALID (earlyoom SIGTERM, host memory ~91 %, other
  workloads); v2 B300 .98 CPU, 6 jobs, CUDA hidden: baseline 91 passed, 101/102 killed, 0 INVALID, 0 malformed,
  survivor c1:m18 only; v3 after adding `test_build_boxes_default_is_the_deterministic_dense_mean_rule`: baseline 92
  passed, m18 killed. All 42 r1/explorer survivors and the 7 C4 data mutants are killed (table in addendum_05 §5a).
- **Final checks**: C1 67/67 rc 0 (`final_protected_hash_check.txt`); code freeze 33/33 (`final_code_freeze_check.txt`);
  old 86: 86 passed (`final_tests_old86.txt`, CUDA hidden); topic1_lagmotif 88 passed (`final_tests_topic1_lagmotif.txt`);
  output_sha256_r2 rc 0 (`final_output_r2_pins.txt`); old pins in repo fail exactly 2 + 16 lines as designed
  (`final_old_card_pins_in_repo.txt`, `final_old_output_pins_in_repo.txt`); whole-run audit_layout PASS, 249 files,
  0 findings (`final_audit_layout.txt`).
- **Local topic2 suite could not run to completion** on DGX-Spark at 08:3x–08:5xZ: earlyoom SIGTERM (rc 143) under
  host memory pressure from other workloads (`local_topic2_suite_attempt2_earlyoom.txt`,
  `local_topic2_suite_earlyoom_journal.txt`, `final_tests_topic2_per_file.txt`: the light files pass, the heavier
  ones are killed at start). The same files passed locally earlier (55 shipped on the sanitized mirror 07:30Z; the
  new 28 at 07:45Z; C4 tests at 08:3xZ). The full 92-test suite passes on B300 .98 CPU (v3 baseline log
  `mutation/v3_b300_baseline_suite.log`: "92 passed"); see §5 for the final B300 run.
- **Addendum** `docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_05.md` (pinned in output_sha256_r2.txt).
- Facts used in it, re-measured: PI_DECISIONS first commit a06f435 2026-11-01T03:01:27Z; card first commit 51609c1
  03:16:27Z (freeze 03:14:34Z); SOURCE.md:12 cites a nonexistent test; hcp_S_s2 100-step loss means 1.0561 at step
  100, 0.9978–1.0036 after; dispersion E 0.784, G 1.112, C 1.469, S 1.557–1.674, R 2.457 (recomputed = json);
  plateau escape steps and per-seed I1 from train logs / verdict.json; decoder Linear(288→48³) at vendored lines
  1135–1148; `fm is not False` at `scripts/topic2_verdict.py:66`; r1 final files 05:30–05:34Z, DISPATCH 05:37Z.

## 2. Logic Chain

1. Only B1 blocked r1; the science reproduced in all five reports. So the fix must remove the linkage without
   changing any governed computation (no rerun, no GPU, no frozen-file edit).
2. Positional tokens in manifest (content-hash) order are a pure renaming of every sorted list, so the frozen
   verdict script reproduces verdict.json byte for byte and the frozen C4 test still passes (both shown).
3. Keyed HMAC tokens keep the same list-order residual and need a key store outside every git repo, which is
   outside my ownership. Positional indices are the C4 letter and the M1 precedent; the stricter options (secret
   reordering, aggregate-only repo) change governed outputs → root/PI choice, disclosed in addendum §3.
4. The originals must survive for the card's frozen-input pins and must leave the repo for C4 → sealed on B300
   (the only off-repo place in my ownership). The prev_snapshot instruction points inside the repo; copying the
   originals there would recreate B1 → pointer file only (deviation).
5. Old pins therefore fail on exactly 18 lines in the repo by design; the checker proves each of those 18 equals
   the sealed-original hash and passes on the sealed root, and that the sanitizer is a reproducible function of
   the originals (S3).
6. r2 is the last iteration and M2 failed twice on verdict-path survivors → additive tests that pass on frozen
   code and kill every r1 survivor; the harness run proves it (102/102 killed after v3).

## 3. Caveats

- **Sealed originals are on ephemeral B300 /scratch only.** A durable copy outside every git repository is a root
  action. If the VM stops first, the 18 old pin lines and preprocess.log can no longer be verified byte-wise
  (their hashes remain in committed metadata).
- **Residual linkage remains** (addendum §3): a holder of the exact staged files can recompute order and match
  per-subject values. Not "unlinkable".
- **Local full topic2 suite not completed on DGX-Spark** in the final window (host memory; earlyoom). Evidence of a
  full pass is from B300 CPU (torch 2.15 / numpy 2.5.4 / scipy 1.18.1) plus earlier local partial runs.
- **Mutation runs used the B300 venv**, not superclaude-env (numerical differences are ≤1e-12; the shipped-verdict
  test compares to 1e-9 for this reason).
- **C4 print incident (mine, ~07:27Z):** a probe of `logs/preprocess.log` masked digits before hex runs, so one
  line showed the letter positions (6 of 16 characters) of one old token in local tool output. Not written to any
  file; disclosed in addendum §6.
- **pkill self-match (mine, ~07:31Z):** `pkill -f` on the scan matched my own shell; only my own shell and scan
  were terminated (exit 143/144), nothing else.
- The explorer salt (`verification/explorer_M3_r1_1/dev_subject_salt.txt`, and its B300 copy under
  `/scratch/iitp4/worker_M3_r1/code/scripts/`) is outside my ownership/scope and untouched.
- B300 CPU use (sealed check, mutation run v2/v3, final suite + ID scan) was direct, niced, CUDA hidden, ≤ 6
  processes on a 224-core node; no GPU, no Slurm job (RESUME addendum 3 restricts GPU use only).

## 4. Conclusion

B1 is remediated: no repo file carries an original token, content hash, file size, voxel count or per-file time;
the card's frozen-input hashes verify against the sealed originals (S1/S2) and the remediation is a reproducible
function of them (S3); every governed number and the verdict (stop) are unchanged (byte-identical verdict.json).
The verdict path and pipeline are now guarded: 102/102 mutants killed. Addendum 05 records the deviation, the
residual, ten errata (incl. the PI decisions predating the freeze) and the print incidents. M3 needs from root:
(1) durable copy of `/scratch/iitp4/worker_M3_r2/sealed_c4`; (2) explorer salt; (3) ruling on the positional
scheme vs the stricter options; (4) record the print incidents; (5) B300 cleanup.

**For r2 verifiers:** expect in the repo exactly 2 failing lines of `card_sha256.txt` (hcp_manifest.json,
split.json) and 16 of `output_sha256.txt` (stage0_hcp.json, 15 hcp run.json). Use
`python3 scripts/topic2_c4_seal_check.py repo` locally and the sealed mode on B300 (§5). Hide CUDA in every test
command. Any B300 GPU use must go through Slurm (none is needed).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt         # 67 OK
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                            # 33 OK
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c                  # 156 OK
python3 scripts/topic2_c4_seal_check.py repo                                                         # all_ok true
CUDA_VISIBLE_DEVICES="" STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/juke/superclaude-env/bin/python3 -B -m pytest -p no:cacheprovider tests/topic2_rgpool -q      # 92 passed (needs ~5 GB free RAM)
CUDA_VISIBLE_DEVICES="" STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 \
  -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q   # 86 passed
/home/juke/superclaude-env/bin/python3 -B scripts/topic2_verdict.py results/topic2/2026-11-01/runs /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-01/verdict.json
# B300 61.107.201.98 (pins are tokenless; copies are in /scratch/iitp4/worker_M3_r2/check/pins):
cd /scratch/iitp4/worker_M3_r2/check && python3 -B scripts/topic2_c4_seal_check.py sealed --sealed /scratch/iitp4/worker_M3_r2/sealed_c4 --pins pins
# mutation (CPU, B300): scripts/b300_env/mutation_pytest_pydeps.sh, then verification/worker_M3_r2/mutation/run_mutants_r2.py
```
Invalidated if: any of the 19 sanitized files, the new pins, the frozen code or verdict.json changes; the sealed
files on B300 change or disappear; a commit containing an original token appears.
