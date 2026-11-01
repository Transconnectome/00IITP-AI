# handoff — victory_M3_r3 (Hard handoff) — 2026-11-01T18:10Z

VERDICT: VERIFIED_COMPLETE (VICTORY CONFIRMED) for M3 (Topic 2) iteration-3 gate repair, ACCEPTANCE T2.4.
Evidence directory: /home/juke/git/00IITP-AI/verification/victory_M3_r3/ (probes, logs, outputs, connectome copies).
0 GPU-h used (CPU only: local DGX-Spark plus connectome Slurm debug jobs 218070, which failed at start because uv was missing on node2, and 218071, which completed). No ledger row needed.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt`: 67/67 OK, rc 0, checked at the start and again at the end.
- Receipts (results/topic2/2026-11-01): addendum_06 31/31, code_sha256_at_freeze 33/33, output_sha256_r2 156/156, c4_sanitized 19/19.
  The old card_sha256 fails on exactly 2 lines (hcp_manifest.json, split.json) and the old output_sha256 on exactly 16 (stage0_hcp.json plus 15 hcp run.json). This is the set expected from the r2 C4 sanitisation and disclosed in addendum_05 §2.
  output_sha256_r2.txt still has sha bc55fa0e…616d, the value recorded in M3_r2_gate_record.json.
- Frozen paths: every file in src/topic2_rgpool, scripts/topic2_*.py, scripts/b300_env and tests/topic2_rgpool is pinned, except one new file, tests/topic2_rgpool/test_verdict_path_guards_r3.py. The 12 shipped test files match output_sha256_r2.
- Full tests/topic2_rgpool suite:
  - local (CUDA hidden): 116 passed (logs/c1_full_topic2_suite.log);
  - connectome node2: 116 passed (connectome/s0_full_suite.log).
- Old suite 86 (tests/test_empirical_four_topics.py, tests/test_pilot_connectome.py, tests/e2e, STRICT_E2E=1, PYTHONPATH=repo): 86 passed. Without PYTHONPATH, 1 e2e subprocess test fails with `ModuleNotFoundError: src`; that is an environment issue, not a regression (prev_versions/c2_old86_without_PYTHONPATH_1failed.log). tests/topic1_lagmotif: 88 passed.
- Mutation testing used my own harness (v01_mutants.py; canary checks that the modules resolve inside the mirror) on 41 specs:
  - 24 inherited specs. V01–V11 were taken from challenger_M3_r2_2/p07_specs.json and are byte-identical to the worker's copies.
  - 17 new X mutants that I wrote.
  - Results:
    - Leg A (12 shipped files, connectome): V01–V11, K1, K2 and W04–W12 all SURVIVE; the 3 controls are KILLED.
    - Leg B (new file alone, local): V01–V11, K1, K2, W04–W08, W12 and CTRL_hcp_4_seeds are KILLED; W09 survives.
    - Leg C (union, connectome): 38 KILLED. Only 3 specs survive: the baseline, W09 and X18.
  - My results for all 24 inherited specs equal the worker's claims in every leg (status and, for leg B, the killing tests): 0 differences.
- Shipped verdict:
  - The frozen script rerun on the shipped runs is byte-identical to verdict.json (59af05e5…af68).
  - My own recomputation without project imports: I1 +0.147 % [−0.068 %, +0.361 %], below δ = 1 %, so **stop**. F+ gains are 3.06 % / 2.93 %, so F+ passes. F− gain is −1.74 %, so F− passes. The I2 lower bound is +0.001 %.
- Errata E1–E5 checked against the frozen code and card §5/§7.2/§8: each is described accurately. E1 is the defect the dispatch names (F+ fails and Stage 1 is absent → `no_verdict` in code, `inconclusive` in card §7.2).
- Dev-salt containment (v02_salt_scan.out.json, counts only):
  - The sealed salt sha256 equals root's record. Modes are 0400/0700/0700, the file is outside any git work tree, and the old repo path is gone.
  - 0 hits for the salt in 7 variants across 19,747 working-tree files (2.32 GB) and 3,434 git objects.
  - The 5 burned hashes occur only in 3 files under verification/explorer_M3_r1_1 and in 0 git objects.
  - Brute force over 10^6 six-digit names without the salt, using 7 schemes: 0/5 recovered. The positive control with the sealed salt recovers 5/5.
  - No 16-hex window anywhere in the repo equals an unsalted or public-salt hash prefix of a six-digit name.
- New r3 content (the test file, addendum_06, the receipt, verification/worker_M3_r3): 0 six-digit ID-like tokens apart from one numeric constant, and 0 BIDS labels. The only "sub-" hits are inside a pytest log that quotes the FU-B card.
- Whole-run audit_layout.py: 448 files, 0 findings, rc 0.

## 2. Logic Chain
1. T2.4 asks for new tests that kill V01–V11 while leaving src and the frozen scripts unchanged. The code pins are 33/33 and the only new test file is additive. Legs B and C kill all 11. Leg A shows they survived the shipped suite, so the new file is what closes the gap.
2. T2.4 asks for the card-vs-code defect to be recorded as an erratum. Addendum_06 E1 records exactly that defect without editing the script, and my code reading confirms it.
3. T2.4 asks for the dev-salt containment to be confirmed. My scan (step 1, last bullets) closes the salt route from repo content alone.
4. T2.4 asks for no regression. All suites pass, C1 and all receipts pass, and the verdict is byte-identical. The shipped `stop` is unchanged and none of the erratum preconditions holds in the shipped records.
5. Phase A and Phase B found no fabricated outputs. My independent rerun reproduces every claimed mutation status, so the result is VERIFIED_COMPLETE.

## 3. Caveats
- W09 is not killed. It is equivalent on the reachable domain: t_interval gives lo ≤ m ≤ hi, so `hi < δ` already implies `not I1_survives`. I checked the proof, not only the worker's sampling.
- X18 (my mutant: the first record wins on a duplicate key) survives every leg. It is equivalent whenever keys are unique, which they are in the shipped records (27/27). It is the E4 latent domain, and the card is silent on how to pick between two records.
- Nine of my X mutants survive the new file alone and are all killed by the shipped suite. X06 (F+ gate `and` → `or`) is one of them: the new file has no case where one F+ gain is ≥ δ and the other is < δ.
- I did not re-run a plain-text scan of the repo against the B300 HCP name list.
- The positional residual in addendum_06 §5 is still open for a PI ruling: the BURNED.md statement "positions 0-4 of the sorted listing" plus off-repo B300 access identifies the 5 dev subjects.
- card_reading is defined inside the test file, so the [erratum] assertions on it check a documented reading rule, not production code.
- I did not read team handoff.md files.
- Connectome leftovers: venv, uv binary and caches under /storage/connectome1/iitp4_verify/victory_M3_r3. The copied repo/data tree was deleted.

## 4. Conclusion
M3 iteration 3 (T2.4) is VERIFIED_COMPLETE. The Topic 2 card verdict stays **stop**; nothing in this iteration changes it.

## 5. Verification Method
- Integrity checks:
  - `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
  - `grep -v '^#' results/topic2/2026-11-01/{addendum_06,code_sha256_at_freeze,output_sha256_r2}*.txt | ...` (per file: `grep -v '^#' F | LC_ALL=C sha256sum -c`)
- Test suites:
  - `CUDA_VISIBLE_DEVICES= python -m pytest -q tests/topic2_rgpool` → 116 passed
  - old suite: `STRICT_E2E=1 PYTHONPATH=$PWD pytest -q tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` → 86
- Mutation legs:
  - `python verification/victory_M3_r3/v01_mutants.py REPO verification/victory_M3_r3/v00_specs.json WORK OUT --tests <files>`
  - legs A and C: verification/victory_M3_r3/v03_connectome_job.sh (sbatch on the debug partition)
- Salt containment: `python verification/victory_M3_r3/v02_salt_scan.py REPO OUT` (counts only).
- Invalidated by any change to src/topic2_rgpool, scripts/topic2_*.py, tests/topic2_rgpool, results/topic2/2026-11-01 or the receipts.
