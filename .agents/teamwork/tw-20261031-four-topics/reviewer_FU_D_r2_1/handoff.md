# Handoff — reviewer_FU_D_r2_1 (FU_D iteration 2 gate) — Hard handoff

## Review Summary
**Verdict: APPROVE.** The r1 blocking classes X45 (δ not pinned) and X22 (joint reading not pinned) are closed with additive tests only. No frozen file, receipt or shipped output changed. The verdict `inconclusive` (measurement capacity at E192) reproduces exactly. 0 GPU-h used by this review.

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0, 67/67 OK. Checked at the start and the end (`verification/reviewer_FU_D_r2_1/c1.out`).
- FU-D receipts, 0 non-OK each: card 1/1, code_sha256_at_freeze 29/29, output_sha256 34/34, addendum_01_sha256 23/23.
- r1 receipts: code 33/33, output_sha256_r2 156/156, addendum_06 31/31 OK.
  - The older r1 `output_sha256.txt` (17 FAILED), `card_sha256.txt` (2 FAILED: hcp_manifest.json, split.json) and the sealed-originals receipt fail. These are the documented M3 r2 C4 sanitisation, superseded by output_sha256_r2. They are not FU-D files.
- Tests, rerun by me (logs in `verification/reviewer_FU_D_r2_1/`):
  - tests/topic2_fu_d: 195 passed.
  - Old suite: 86 passed.
  - tests/topic2_rgpool: 113 passed, 3 skipped.
  - tests/topic1_lagmotif: 88 passed.
- Card freeze: receipt 2026-11-01T16:06:07Z. Autocommit 34f4b30 (2026-11-01T15:50:24Z) holds the card with sha 1b7fee6c…. The first real-data job (511) was submitted at 16:13:50Z. F+ gate jobs 534/535/536 ran at 17:46–19:03Z and closed at 1.175/1.180/1.180 GPU-h. FU-D total is 3.672 of 25 GPU-h.
- Independent exact-Fraction oracle on `runs/Fplus_*_s0/run.json`:
  - NMSE: E 0.6558494816918741, C 0.653467876277415, S 0.6577736746995909.
  - Gains: 0.0036313 and 0.0065460, both < 1/100, so the gate fails → `inconclusive`.
  - Regenerating verdict.json in a copied tree is byte-identical (`cmp`).
- Own independent mutation harness: `verification/reviewer_FU_D_r2_1/mut/{mutants.py,run.py,out.json,run.log}`.
  - Written from the code, not from the worker's lists. Fresh copied tree for each mutant. Run against tests/topic2_fu_d minus the E192 build test and the belt hash test.
  - Control: 189 passed, shipped output unchanged.
  - 44 mutants: 38 killed, 5 survived, 1 not applied (R42, which I wrote incorrectly).
  - Every mutant that changes a shipped output is killed: R01–R05, R10, R13, R25, R32, R41. This includes δ 0.0036 / 0.007 / 0.015, the inconclusive joint text, the hardcoded joint key, the gate-fail mapping, and δ at the script call site.
  - Survivors:
    - R36 (orders guard weakened), R40 (r1 verdict hardcoded "stop") and R43 (needs_fminus broadened): equivalent on the pinned inputs. They have the same reasoning as Q19/S207 and S023/S025.
    - R31: the script's `if gate_failed or gst != "completed"` reduced to `if gate_failed`. Non-equivalent but harmless to the verdict; see the nonblocking findings.
    - R34: hierarchical bootstrap seed 0→1. Changes a secondary, descriptive output only.
- Worker evidence spot-check (`verification/worker_FU_D_r2/mutation/union.out.json`): 423 results; A-status 404 KILLED / 19 SURVIVED; shipped.changed True for 121, all KILLED. This matches the claims. The survivor rerun log shows 11 killed and 8 survived.
- Equivalence proofs re-checked by reading the code (addendum §4): Q08, Q19/S207, Q21, S023/S025, S160 and S181 all hold. For S181, `records.py` attempts are processed in sorted order, and `decide` only tests `state != "completed"`.
- C4: count-only scan of 87 FU-D files (results, src, tests, card, addendum, report, verification/worker_FU_D_r2, worker metadata) found 0 bare 6-digit tokens and 0 `sub-` labels.
- audit_layout on the whole run: rc 0, PASS, 646 files, findings [].
- No skip or xfail in the new test file. Tests use card literals and run the script with `--out` in tmp_path.

## 2. Logic Chain
1. The receipts and C1 are intact, so the r2 change set is additive (new test file, addendum, new receipt), as required.
2. X45 and X22, plus my own δ and joint-reading variants, are killed. So the blocking classes of the r1 gate are closed (F2: verdict code tested).
3. The oracle and the byte-identical regeneration show the shipped verdict follows card §8 step 2. Card frozen before results (F1/C3); Slurm, ledger and caps OK (F3/C5).
4. The `inconclusive` outcome is a pre-registered escape outcome. Result report §5 costs the further options, and the addendum states what remains untested. That meets the "untestable/escape outcome properly evidenced and costed" clause.
5. The remaining survivors (R31, R34) are on paths that cannot be reached with the shipped data, and none can flip a verdict category. So they are nonblocking.

## 3. Caveats
- I did not use B300. Three r1 verifiers already re-scored the checkpoints bit-exactly on B300, and r2 changed no data.
- My mutant set (44) is smaller than the worker's union (423). It was designed independently.
- The single-seed F+ gate is pre-registered (card §7.1). Its robustness to seed noise is not tested; the costed option D-gate-seeds is about 7.1 GPU-h.
- While I reviewed, another verifier's harness processes were running (auditor_FU_D_r2_1). They are not orphans of the worker.

## 4. Conclusion
APPROVE. Nonblocking findings:
- N1 (R31): no script-level test covers an incomplete or failed gate combined with stray or unplanned directories or Stage-1 records. The mutant swaps a `no_verdict` output for a RecordError stop. Either way there is no verdict, and the RecordError stop is arguably closer to card §8 (E1). The shipped data lie outside this path, pinned by a test.
- N2 (R34): the secondary hierarchical-bootstrap seed (card §8: seed 0) is not pinned. This is descriptive only, and Stage 1 was not run.
- N3: when the gate passes, a seed plan exists and Stage 1 was never launched (cost guard), `decide` gives `no_verdict` with the reason "Stage 1 incomplete after one rerun (software failure)". The card treats this case as cost/missing. The category is unchanged and the case is unreachable now.
- N4: the worker's process deviations (3 concurrent pytest processes for about 4 s; DISPATCH JSON referenced by path) are disclosed and minor.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt addendum_01_sha256.txt; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done   # 0 each
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q   # 195 passed
cd verification/reviewer_FU_D_r2_1/mut && PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 run.py /tmp/out.json R01 R04 R31 R34   # R01/R04 killed; R31/R34 survive
```
Invalidation: any change to verdict.json, a frozen FU-D file or a receipt, or a mutant that flips the shipped verdict while surviving.
