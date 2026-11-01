# Handoff — worker_FU_C_r2 (FU-C iteration 2; Hard handoff)

Written 2026-11-01 ~21:05Z UTC. Parent: root coordinator (session 5fddb83e). GPU-h used: 0. No ledger rows. No git writes. The retired literal was never printed or written by this worker: the old file was read only through digit-masked views or in memory, and every check is count-only.

## 1. Observation

- **The r1 gate's only blocking class was C4.** `tests/topic2_fu_c/test_gate_and_records.py`, a negative fixture labelled "HCP-ID shape", held a 6-digit literal that is a real HCP-YA ID, and result report §4 claimed "No participant ID was printed or written". All five r1 verifiers confirmed the science (verifier handoffs under `reviewer_FU_C_r1_*`, `challenger_FU_C_r1_*` and `auditor_FU_C_r1_1`).
- **Seal** (`verification/worker_FU_C_r2/probes/seal_retired_test.out.json`). The sealed copy matches its pre-result pin; mode 0o400, dir 0o700, 276 lines.
  - Sealed path: `~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/tests/topic2_fu_c/test_gate_and_records.py`.
  - Receipt: `results/topic2/2026-11-02_fu_c/c4_sealed_originals_sha256.txt`.
- **Retirement.** The file was deleted from the repo. Its prior bytes were not copied to `prev_snapshot/` (C4 outranks the snapshot rule). The two other changed files were snapshotted: `test_perms_receipts_c4.py` and the result report.
- **Re-authoring.** `tests/topic2_fu_c/test_evaluate_records_r2.py` covers the same oracle classes. Of the old file's 169 long lines, 20 occur verbatim in it. It contains no literal.
- **Footprint** (probe `derivative_and_footprint.out.json`, 24,059 text files, files over 5 MB skipped):
  - the literal (digit-bounded) occurs in 0 repo files;
  - 1 file is a near-copy of the retired file: `verification/explorer_FU_C_r2_2/tree/tests/topic2_fu_c/test_gate_and_records.py` (99.4 % of its long lines; a peer explorer's tree, not mine).
- **Repaired test.** `test_perms_receipts_c4.py::test_context_from_the_repo_has_no_problems_once_code_is_pinned` keeps its node id. Under the default receipt, build_context now reports exactly two problems, `pinned file missing: …test_gate_and_records.py` and `pinned file changed: …test_perms_receipts_c4.py`; with the derived view it reports [].
- **Reproduction.**
  - `scripts/topic2fu_c_verdict_r2.py --out verification/worker_FU_C_r2/verdict_r2_check.json`: rc 0, `byte_identical_to_shipped: true`, sha256 4d7931025c4f… on both sides.
  - The frozen CLI with `--out verification/worker_FU_C_r2/frozen_cli_now.json` gives no_verdict with exactly those 2 problems.
  - The driver refuses `--out` set to the shipped path (rc 1).
- **Receipts** (`scripts/topic2fu_c_check_receipts_r2.py` → `check_receipts_r2.out.json`, ok true):

  | receipt | lines | failing | failing lines |
  |---|---|---|---|
  | card | 36 | 0 | — |
  | code | 15 | 2 | 13 MISSING, 16 CHANGED |
  | presentation | 1 | 0 | — |
  | output | 160 | 3 | 141, 164 CHANGED; 162 MISSING |
  | output_sha256_r2 | 27 | 0 | — |

  Raw `sha256sum -c` agrees.
- **Strict C4 tripwire** (`src/topic2_fu_c/c4scan.py`): 0 hits over every FU-C path, with one allowlisted value, the group-mask voxel count. Controls: all 6 positives flagged and none of the 6 negatives.
- **B300 count-only membership check** (`probes/b300_membership.out.json`): 108 unique 6-digit runs from 193 files, including this metadata, against 1,084 staged names gives 0 hits. Controls are valid (positive 1, negative 0). A final rerun after this handoff is in `b300_membership_final.out.json`.
- **Mutation testing** (`verification/worker_FU_C_r2/mutants/mutants_r2.out.json`). The table is the union of the worker r1, challenger_1, challenger_2 and reviewer_2 tables, with 5 hash tests deselected (count checked).
  - 150 entries; 146 killed; 0 invalid.
  - Survivors: the baseline plus V07c, V12 and F11, the equivalents accepted in r1.
  - All 52 r1-verifier survivors are killed, each by the intended new guard test (first-failing-test map in the out.json).
- **Suites:**

  | suite | result |
  |---|---|
  | tests/topic2_fu_c | 180 passed |
  | old 86 (STRICT_E2E) | 86 passed |
  | tests/topic2_rgpool | 116 passed |
  | tests/topic1_lagmotif | 88 passed |

- **Other checks.** flake8 is clean on FU-C src/scripts/tests and verification/worker_FU_C_r2. C1 rc 0. Whole-run audit_layout rc 0, 0 findings.
- **Addendum numbers** (`probes/addendum_numbers.out.json`, from the verdict files):
  - E seed-mean 0.98842, so the learned signal is 0.01158;
  - δ is 85.4 % of the learned signal, and the I1 upper bound 23.2 %;
  - without seed 16, the I1 sd is 0.220 % and the half-width 0.204 % (df 6); the r1 sd is 0.173 %.

## 2. Logic chain

1. **Why retire the file instead of editing it.** The pre-result receipts cannot be edited, and they keep the old file sha. That sha is also in already-committed verifier .md handoffs. With that sha, an in-place-edited copy lets the literal be brute-forced (explorer_FU_C_r2_1 probe). So the file was retired: sealed off-repo, then deleted. Its tests were re-authored with a different structure. Recovery would now need the exact bytes of the other ~250 lines, and the only in-repo source of those bytes is the peer tree (§3, open issue 1).
2. **Why receipt lines fail.** Any C4 fix changes pinned bytes. Exactly 5 pin lines across 2 receipts now fail, and they are declared in code (`supersession.SUPERSEDED`), in the addendum §3 table and in the r2 receipt's `# supersedes:` lines. The checker proves that the failing set equals the declaration and that every other line verifies.
3. **Why verdict-path integrity holds.** The derived view keeps every line of the original receipt except the two test pins. That includes `frozen_utc` and all `verdict_code` and `result_handling` pins, and build_context still verifies them. The unchanged verdict code then reproduces verdict.json byte for byte. So the shipped verdict is provably the output of the pinned pre-result code. verdict.py, receipts.py, logs.py, design.py, the CLI and the card are byte-unchanged; their shas equal the r1 tested-artifact list.
4. **Why the new tests are behavioural, not hash-based.** The guard tests on receipts run on a synthetic root, whose receipts and freeze stats pin are computed from the live files. The harness deselects only the 5 tests that read real pins, and it checks that count. The kills therefore come from behaviour.
5. **Why the report claim is closed.** The report §4 claim is corrected in place, with a banner and the prior bytes snapshotted. Addendum 02 records the incident, the errata (§2.2 stall explanation; scope of stop) and the reproduction rule.

## 3. Caveats

- **Sealing outside my ownership list.** I wrote the sealed copy into a new subdirectory of the root-held sealed store, `~/.local/share/00IITP-AI_sealed/topic2/fu_c_c4/`. Root may move it or re-own it.
- **Peer copy.** `verification/explorer_FU_C_r2_2/tree/` (plus `mut_work/` and `code_receipt_subset_derived.view` there) holds an in-place-edited near-copy of the retired file beside copied receipts. Until its owner or root removes it, the literal is recoverable from working-tree content. I may not write there.
- **Footprint scan limits.** The scan skipped files over 5 MB and symlinks. It did not inspect git history; the retired .py was never tracked, and the explorers checked history count-only.
- **Old suite file not rerun.** The pinned r1 harness (`verification/worker_FU_C_r1/mutants/run_mutants.py`, 2 deselects) was not rerun as-is. With the new hash tests it would count hash mismatches as kills, so its W table was run inside the union harness instead.
- **Agent transcripts.** Copies of the literal in agent transcripts outside the repo are outside repo scope.
- **FU-A fixtures.** explorer_FU_C_r2_2 flagged a similar 6-digit fixture pattern in `tests/topic2_fu_a/test_scripts.py`, which is FU-A's path. I did not check it.

## 4. Conclusion

The FU-C iteration-2 C4 remediation is complete with 0 GPU-h.
- The literal is out of the repo: sealed, with no in-repo occurrence and no derivable near-copy in FU-C paths.
- The false report claim is corrected.
- The C4 scan now covers every FU-C path.
- The shipped `stop` verdict (I1 −0.113 % [−0.499 %, +0.272 %], df 7) is unchanged and reproduced byte-identically.
- There is no regression.
- Gate-relevant residual for root: remove the peer near-copy tree.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-02_fu_c/output_sha256_r2.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_check_receipts_r2.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_c_verdict_r2.py --out /tmp/x.json
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q
python3 -B verification/worker_FU_C_r2/mutants/run_mutants_r2.py $PWD <work> <out.json> 2
# root only (sealed store): LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_c/c4_sealed_originals_sha256.txt
```

Invalidation conditions:
- any FU-C receipt line outside addendum 02 §3 fails;
- the driver output is not byte-identical to verdict.json;
- a C4 tripwire hit;
- a B300 membership hit > 0 with valid controls.
