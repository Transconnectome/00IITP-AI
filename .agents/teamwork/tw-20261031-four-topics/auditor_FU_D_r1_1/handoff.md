# Handoff (Hard) — auditor_FU_D_r1_1, forensic integrity audit of milestone FU_D (worker_FU_D_r1)
Written 2026-11-01T19:37Z. Profile: General Project. Integrity mode: Development. ORIGINAL_REQUEST.md has no "from scratch" or "must not delegate" constraint. The ACCEPTANCE C1–C8 rules are enforced as integrity rules.

## Forensic Audit Report

**Work Product**: FU-D (Topic 2 follow-up D, SwiFT ver11 E192). Paths: src/topic2_fu_d/, tests/topic2_fu_d/, scripts/topic2fu_d_*.py, results/topic2/2026-11-02_fu_d/, docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_{card,result_report}.md, B300 /scratch/iitp4/fu_d/, ledger rows.
**Profile**: General Project
**Verdict**: CLEAN

### Phase Results
- Hardcoded output detection: **PASS**.
  - Read verdict.py, records.py, seedplan.py, design.py, config.py, view.py, slurm.py and scripts topic2fu_d_{train,verdict,equiv,make_view,build_env,c4scan}.py.
  - The gate gains are computed from run.json test_nmse values. Nowhere does the code return a constant verdict.
- Facade detection: **PASS**.
  - The wrapper calls the frozen scripts/topic2_train.py main(). The run records carry the real n_params (474,226,176, counted from the built model) and the frozen r1 code hashes.
- Results recomputed by the auditor: **PASS**.
  - My own Slurm job 576 loaded the three saved checkpoints on B300 and re-scored them with the frozen evaluate_fixture.
  - It reproduced every test NMSE bit-exactly: E 0.6558494816918741, C 0.653467876277415, S 0.6577736746995909. The per-group num/den terms are also identical.
  - The F+ test_den vectors equal the r1 E36 F+ test_den exactly, so the same synthetic evaluation stream and masks were used.
- Pre-populated or fabricated artifacts: **PASS**.
  - Every output file has an mtime after the 16:06:07Z freeze, and every code file has an mtime before it.
  - The B300 originals are sha256-identical to the local copies (run.json, fud_meta.json, train_log.jsonl, slurm.json, smoke files, code).
  - Train logs: 87 monotone train events, the val events equal val_nmse_curve, and every timestamp falls inside its Slurm job window.
  - sacct: jobs 511/534/535/536 are COMPLETED with ElapsedRaw 144/4230/4248/4246 s. These equal the ledger and slurm.json values.
- Card frozen before results: **PASS**.
  - card_sha256.txt 1/1, code_sha256_at_freeze.txt 29/29 (same file set as on disk) and output_sha256.txt 34/34 all pass.
  - The card has exactly one version in git: daemon commit 34f4b30 at 15:50:24Z, before the freeze and before any FU-D job. Its sha256 equals 1b7fee6c…001b.
  - Before the freeze, only data-free work ran: the CPU venv build and the explorers' synthetic smokes, which the card discloses in §0.
- Build and tests: **PASS**.
  - tests/topic2_fu_d: 129 passed (88 s).
  - Old suite (tests/test_empirical_four_topics.py, tests/test_pilot_connectome.py, tests/e2e): 86 passed.
  - The suite contains no skip or xfail marker.
- Verdict reproduction: **PASS**.
  - Re-running scripts/topic2fu_d_verdict.py gives JSON identical to the shipped verdict.json (`inconclusive`).
  - The frozen r1 stats.gate_fixture(…, 0.01, "Fplus") gives the same gains and pass=False.
  - The card §8 step 2 mapping is applied correctly.
- Tests that cannot fail (held-out mutants): **PASS with nonblocking gaps**.
  - I ran 13 mutants that are not among the worker's 62: 9 were killed and 4 survived (A02, A05, A11, A13). Details are under Caveats.
  - None of the 4 survivors changes the shipped verdict under the frozen code.
- Silent fallbacks: **PASS**.
  - precheck refuses unpinned inputs.
  - records.load_runs rejects unplanned directories and non-COMPLETED Slurm states.
  - A missing gate gives `no_verdict`, never a pass.
  - The smoke's `; true` is deliberate (an abort is expected), and its record has status aborted_throughput with no evaluation.
- C4 (participant IDs): **PASS**.
  - Across 76 FU-D files there are 0 standalone 6-digit integers, 0 BIDS labels and 0 16-hex tokens. Every hex-shaped hit was a float mantissa or exponent.
  - Explorer and verification dirs: the only 6-digit numbers are shapes, MiB values and n_params.
  - HCP run records would carry only positional hNN tokens. In this run only the smoke touched HCP, and its record holds no subject tokens.
  - The positional view stays on B300. Its build prints and writes only counts.
  - No reference to the sealed dir or the salt appears in any FU-D output.
- C5 (GPU through Slurm, ledger, cap): **PASS**.
  - The only FU-D GPU jobs in sacct are 511, 534, 535 and 536 (worker) and 396, 404, 418, 430 (explorers). All are ledgered.
  - FU-D total is 3.672 GPU-h (3.696 including verifiers) against the 25 cap. The run total is 32.866 against the 95 ceiling.
  - sacct shows no `g3t-G-E0-*` job at all since 2026-11-01, so the B300-share rule was never triggered.
  - The CPU venv build and the view build ran by ssh with no GPU use.
- Envs and installs: **PASS**.
  - The worker used its own venv /scratch/iitp4/fu_d/venv, built from the r1 lock (freeze identical).
  - No superclaude-env site-packages entry is newer than 15:20Z.
- Writes to protected, pinned or external paths: **PASS**.
  - C1: 67/67 OK, rc 0.
  - The r1 code freeze is 33/33 OK.
  - Nothing in results/topic2/2026-11-01 or the frozen r1 code changed after 15:20Z, except addendum_06_sha256.txt, which worker_M3_r3 wrote (header shows 15:43:46Z).
  - The failing r1 receipt lines point at files whose mtime is 2026-11-01 16:33 KST (07:33Z). That is the r2 sanitization, before FU-D.
  - The hard links add directory entries under fu_d/hcp only; the r1 bytes are unchanged.
- Git writes by agents: **PASS**. Every commit since 15:00Z is by "Chavis Autocommit" (the host daemon) or the earlier root checkpoint. No commit touches FU-D .py files.
- Layout (audit_layout.py on the whole run root): **PASS**, 514 files, findings [].

## 1. Observation
- C1: `LC_ALL=C sha256sum -c …/PROTECTED_HASHES.txt` gives rc 0, with 0 non-OK of 67. Re-checked at 19:35Z with the same result.
- Receipts: card 1/1, code 29/29, outputs 34/34 (0 non-OK each, re-checked at 19:35Z). The file set under the freeze equals the set on disk.
- Tests: `verification/auditor_FU_D_r1_1/pytest_fud.out` shows "129 passed … rc=0"; `pytest_old.out` shows "86 passed … rc=0".
- My probe job 576 on b300-01 (debug, 1 GPU, ElapsedRaw 33 s, 0.010 GPU-h) has ledger started and completed rows. Its output `verification/auditor_FU_D_r1_1/reeval_fplus.json` shows exact=true, den_equal=true and num_max_rel_diff=0.0 for E, C and S, n_params 474226176, gains 0.0036313292621888414 and 0.006546018163682844.
- sacct output is in `verification/auditor_FU_D_r1_1/sacct_b300.out` and `sacct_window.out`. Other sessions' pipeline hashes in job names are redacted there.
- Verdict re-run: `verification/auditor_FU_D_r1_1/verdict_rerun.json` is identical to the shipped verdict.json.
- Held-out mutants: `verification/auditor_FU_D_r1_1/heldout_mutants.out.json` gives n=13, killed 9, survived [A02, A05, A11, A13].
- Smoke equivalence (`smoke/equiv.json`): the r1 hcp_E_s0 test NMSE 0.9908706340280367 is reproduced exactly, with num/den/order equal. The smoke HCP cost probe aborted at step 200; run.json has no val or test fields.
- Report numbers checked against files:
  - r1 seed 0 gains (E−C)/E 2.772 % and (S−C)/S 2.900 %; seed 1 gains 3.348 % and 2.970 %.
  - The card's "+3.06 % / +2.93 %" are the seed means of these.
  - E192 cubes are −3.1 % against E36 cubes; E192 boxes are −0.7 % against E36 boxes.
  - The train losses match run.json.

## 2. Logic Chain
1. The card and code were frozen before any FU-D job ran (sacct's earliest FU-D worker job is 511, submitted 16:13:47Z; the freeze was 16:06:07Z), and both are unchanged. So no result could have shaped the card.
2. The gate numbers re-derive bit-exactly from the saved checkpoints through frozen code in my own Slurm job. Their evaluation denominators equal r1's, and the B300 originals hash-match the repo copies. So the results are neither fabricated nor edited after the runs.
3. The verdict follows mechanically from those numbers: both gains are below δ = 0.01, so card §8 step 2 gives `inconclusive`. Two independent paths (FU-D verdict.py and frozen r1 gate_fixture) reproduce it.
4. Every GPU-h used is in sacct, the ledger and the run records, inside the cap and through Slurm only. No IDs, git writes, installs or external writes were found.
5. Hence no prohibited pattern was observed: the verdict is CLEAN.

## 3. Caveats
Nonblocking test-coverage gaps. None changes the shipped verdict, because the code is frozen and receipted:
- **A02**: `config.DELTA = 0.01 → 0.003` survives every FU-D test. No test pins the δ constant, and at δ = 0.003 the gate would pass.
  - It is protected only by the code freeze receipt and by verdict.json reporting `"delta": 0.01`.
  - A future edit should add a test that pins `config.DELTA == 0.01` (card §8, PI decision 3).
- **A05**: removing the `"worker_M3_r1" in dd` clause is near-equivalent, because the `realpath(dd) != realpath(BASE/hcp)` clause still guards.
- **A11**: `len(num) != 16 → < 1` survives. No fixture supplies a record with a wrong term count. The shipped records have 16 terms each.
- **A13**: the joint-reading text for `inconclusive` is unpinned. The shipped text matches card §9(c) verbatim.

Other caveats:
- Run-level nondeterminism: training was not re-run (cap rule). Only the evaluation was reproduced.
- What I did not verify:
  - the worker's historical squeue checks at submit time (the sacct history shows no g3t-G-E0 job ever existed, so the rule could not have bitten);
  - the explorers' audit.
- Both DISPATCH.md files (the worker's and mine) summarise the inline worker or explorer JSON instead of re-typing it. That is a metadata convention, not an integrity issue.
- `/scratch/iitp4/auditor_FU_D_r1_1/` on b300-01 holds my probe script, sbatch file, Slurm log and JSON (a few KB) and can be removed by root.

## 4. Conclusion
**CLEAN.** The FU-D work product is authentic. The shipped verdict `inconclusive (measurement capacity at E192)` is reproduced from the saved checkpoints and the frozen code, the card was frozen before any result, and C1–C8 were respected. Recommended nonblocking follow-up: pin `config.DELTA` in a test if the FU-D code is ever revised (with a dated addendum, not an edit of the frozen files).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # 0
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done   # 0 0 0
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q   # 129 passed
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic2fu_d_verdict.py --wrapper-sha256 d598989bd93666c36b821448bbde0cbbb10b5eb822b454a4ff90b9a03185b84e --out <tmp>.json   # identical to verdict.json
cat verification/auditor_FU_D_r1_1/reeval_fplus.json          # exact re-score of 3 checkpoints (Slurm 576)
/home/juke/superclaude-env/bin/python3 verification/auditor_FU_D_r1_1/heldout_mutants.py REPO SCRATCH OUT.json   # 9/13 killed; A02/A05/A11/A13 survive
```
This verdict becomes invalid if:
- any FU-D receipt fails;
- the B300 checkpoints no longer re-score to the recorded values;
- a FU-D GPU job appears in sacct that is not in the ledger.
