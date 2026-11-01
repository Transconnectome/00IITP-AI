# Handoff (Hard) — worker_FU_C_r3, FU_C iteration 3 (final)

Scope: additive-only hardening after root's C4 containment. Verdict `stop` unchanged and reproduced byte for byte.
0 GPU-h, no ledger rows, no git writes, no file pinned by any earlier receipt was edited, nothing copied from the
sealed store. No literal, digit, position, shape, loop counter or timing of the retired literal is written anywhere.
The r2 gate record is summarised in DISPATCH.md, not re-typed (root rule).

## 1. Observation
- Root containment present: GATE_STATUS "FU_C r2 near-copy containment (~06:45 KST)"; peer dirs
  verification/explorer_FU_C_r2_2 and verification/auditor_FU_C_r2_1/probes hold only small probe files; sealed store
  ~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02/ has 302 files, 0 not 0400, 0 dirs not 0700.
- Baseline before any r3 write: C1 rc 0; check_receipts_r2 ok (card 36/0, code 15/2, pres 1/0, output 160/3, r2 27/0);
  tests/topic2_fu_c 180 passed; old suite 86 passed.
- scripts/topic2fu_c_check_c4_r3.py --b300 (verification/worker_FU_C_r3/probes/c4_check_r3_pre.out.json): ok true.
  Working tree 23,434 files and 2,174 git blobs: identifier-context hits 0, near-copies 0, named copies 0, offset
  statements 0, digest hits 0; sealed original matches its pin; retired path absent; 3 files over 50 MB not
  content-scanned (presentation.mp4, a docs/raw zip, a Topic 1 .npy). B300 count-only membership: production 199
  files / 118 runs, verification 339 / 88, metadata 87 / 8 -> 0 member hits each; controls pos 1, neg 0 (valid).
- c4scan_strict over the real FU-C scope: 2 shape hits before classification (allowlisted mask voxel count; one
  8-hex prefix of the shipped verdict.json digest in addendum 02), 0 after classification.
- verdict_r2 --out verification/worker_FU_C_r3/verdict_r2_repro.json: rc 0, context_problems [], byte_identical true,
  cmp identical (sha 4d7931025c4fb9a2b6605394c7e47125cf472bf6b4e85f045a10c373ae4780f5). Frozen CLI --out:
  no_verdict with exactly the 2 declared superseded pins.
- Mutation harness verification/worker_FU_C_r3/mutants/run_mutants_r3.py (mutants_r3.out.json): 222 entries
  (W 54, C1 33, C2 40, R2 22, CR1 28, CR2 25, R3 19), 217 killed, 0 invalid, 5 deselected (baseline 205 passed);
  survivors baseline, W:V07c, W:V12, W:F11, CR2:C10. All 26 r2-challenger behavioural survivors killed.
  Run 1 (mutants_r3_run1_superseded.*) left R3:R05 alive; the short-prefix test case was wrong (not a prefix of a
  known digest); fixed, then run 2.
- Suites before receipt: FU-C 210 passed; old 86 passed; topic2_rgpool 116 passed with CUDA_VISIBLE_DEVICES=''
  (113 passed + 3 skipped without it: CPU-only training-loop guards); topic1_lagmotif 88 passed; flake8 clean.
- output_sha256_r3.txt: 20 pins, 0 failures, chmod a-w; check_receipts_r2 after it: ok, r3 20/0, declared failing
  set unchanged (code 13, 16; output 141, 162, 164).

## 2. Logic chain
1. The only r2 blocker (peer near-copy + unchanged pin -> recoverable literal) was outside my ownership; root moved
   it off-repo. My count-only sweep (worktree and git blobs, raw and JSON-escaped) finds no near-copy, no named copy,
   no offset statement, no digest and no identifier-context occurrence, so the literal is not recoverable from repo
   content by the known classes.
2. Editing any r2-pinned file would break output_sha256_r2.txt and cascade into supersession.py; so every r3 change is a
   new file, pinned in a new output_sha256_r3.txt that check_receipts picks up automatically and must fully verify.
3. r2 surfaces were guarded only by hash pins; the new tests exercise them behaviourally on tmp roots (drivers loaded
   via importlib/runpy with ROOT at a tmp root, never real results/ paths). The harness shows every named survivor
   killed with the hash tests deselected (count checked), so kills are behavioural.
4. The two c4scan blind spots are real; c4scan.py stays unedited (documented limits, plus a test pinning the '.'
   behaviour), and c4scan_strict.py closes them with controls and a meaning-classified real-repo scan.
5. The verdict path is untouched (verdict.py, receipts.py, logs.py, design.py, CLI, card byte-unchanged), and the
   reproduction is byte-identical, so the scientific result is unaffected.

## 3. Caveats
- Near-copy detection uses long-line overlap; a reformatted or encoded copy would escape. B300 membership checks only
  the 1,084 staged names. Agent transcripts and /tmp are out of repo scope. Three >50 MB files not content-scanned.
- Committed r1/r2 handoffs describe the literal in words (residual, pending PI per GATE_STATUS); I repeat none.
- The dispatch prompt itself embedded the r2 gate record with positional wording; I did not write it anywhere.
- scripts/topic2fu_c_check_c4_r3.py's network part (B300) is not unit-tested; its pure functions are.
- The first-failing test per mutant comes from pytest -x; several mutants are killed by a sibling test of the
  intended class (e.g. SS04/SS05/S03 by the passing-world test asserting the undeclared receipt is checked).

## 4. Conclusion
FU_C r3 complete: containment confirmed count-only; r2-surface survivors closed behaviourally; strict scanner and
C4 check added; addendum 03 records containment, the r2-headline erratum, the git freeze anchor and residuals; verdict
`stop` byte-identical; no regression. Status DONE.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_check_receipts_r2.py      # ok; r3 20/0
grep -v '^#' results/topic2/2026-11-02_fu_c/output_sha256_r3.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B scripts/topic2fu_c_verdict_r2.py --out <tmp>.json   # byte_identical true
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -p no:cacheprovider tests/topic2_fu_c -q   # 210 passed
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/topic2fu_c_check_c4_r3.py --out <tmp>.json --b300     # ok true
python3 -B verification/worker_FU_C_r3/mutants/run_mutants_r3.py REPO <work outside c4 scope or removed after> OUT 2
```
Invalidation: any near-copy or offset/digest file reappearing; any change to an r2- or r3-pinned file; byte_identical
false. Do not run the FU-C suite while a mutation work dir exists under verification/worker_FU_C_r* (c4scan walks it).

## 6. Post-receipt final checks
Run after output_sha256_r3.txt was written (about 22:28–22:33Z):
- scripts/topic2fu_c_check_c4_r3.py --b300 -> verification/worker_FU_C_r3/probes/c4_check_r3_final.out.json: ok true.
  Working tree 27,031 files and 2,189 git blobs: all exposure counts 0, no near-copy. B300: production 216 files /
  128 runs, verification 353 / 88, metadata 88 / 8 -> 0 member hits; controls valid (pos 1, neg 0).
- check_receipts_r2 -> verification/worker_FU_C_r3/check_receipts_after_r3.out.json: ok; r3 20/0; r2 27/0; declared set unchanged.
- tests/topic2_fu_c 210 passed; old suite 86 passed; topic2_rgpool 116 passed (CUDA_VISIBLE_DEVICES=''); topic1_lagmotif 88 passed.
- verdict_r2 --out (scratchpad) byte_identical true, cmp OK. C1 rc 0. audit_layout on the run root: 0 findings, rc 0.
