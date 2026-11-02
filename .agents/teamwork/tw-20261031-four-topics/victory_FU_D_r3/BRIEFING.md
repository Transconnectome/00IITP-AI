# BRIEFING — victory_FU_D_r3

## Context
Milestone `FU_D` evaluates connectome box grouping at stage-0 merge (`M0`) at SwiFT ver11 `E192_d22182` scale (`474,226,176` parameters, `140k` training samples = `8,750` steps x batch `16`, arms `E`/`C`/`S`, up to `5` seeds, cap `25.0 GPU-h`). At seed 0, the synthetic `F+` measurement-capacity gate yielded relative test NMSE gains `g(C vs E) = 0.363%` and `g(C vs S) = 0.655%`, both strictly below `delta = 1.0%` (`0.01`). Per card §7.1 and §8 step 2, Stage 1 on HCP was not launched and the confirmatory verdict is `inconclusive` (measurement capacity at E192), leaving the r1 E36 `stop` verdict standing alone.

Iteration 2 failed the 5-verifier gate because Challenger 2 (`challenger_FU_D_r2_2`) identified two blocking items:
- `B1` (`C12` / `CV09` and sibling class): `src/topic2_fu_d/verdict.py::_stage1_category` line 96 (`if c2 != cat:`) mutated to `if c2 != cat and c2 != "inconclusive":` survived the 195-test r2 suite, and script-level stall wiring was tested only in arm `S` at a single seed (`CP01`, `CP02`).
- `B2` (alias run directories): `design.DIR_RE` and `int()` accept non-canonical directory aliases (zero-padded, Unicode digits, trailing newline) that can overwrite canonical records in `records.load_runs`, which was omitted from `addendum_01` errata.

In Iteration 3 (`worker_FU_D_r3`), three additive test files (`test_fud_r3_guards.py`, `test_fud_r3_oracle.py`, `test_fud_r3_full_output.py`; +194 tests, 389 total), `2026-11-02_topic2_fu_d_addendum_02.md`, `addendum_02_sha256.txt` (102 entries), `union_r3.out.json` (1,675 distinct mutants: 1,511 killed, 164 classified equivalent/decision-invariant survivors, 0 output-changing survivors), and `errata_probe.out.json` were delivered with 0 edits to frozen files and 0 GPU-h. All 5 Iteration 3 verifiers (`reviewer_FU_D_r3_1`, `reviewer_FU_D_r3_2`, `challenger_FU_D_r3_1`, `challenger_FU_D_r3_2`, `auditor_FU_D_r3_1`) passed (`APPROVE` x2, `CONFIRMED` x2, `CLEAN` x1).

## Scope
- **Phase A (Timeline & Provenance)**: Verify `PROTECTED_HASHES.txt` (67/67), all 5 FU-D receipts (`card_sha256.txt`, `code_sha256_at_freeze.txt`, `output_sha256.txt`, `addendum_01_sha256.txt`, `addendum_02_sha256.txt`), all 3 Topic 2 r1 receipts (`code_sha256_at_freeze.txt`, `output_sha256_r2.txt`, `addendum_06_sha256.txt`), and strict chronological ordering from card freeze -> smoke -> F+ gate runs (Slurm 534/535/536) -> `verdict.json` -> `addendum_01.md` -> `addendum_02.md`.
- **Phase B (Forensic Integrity Check)**: Verify genuine implementation in `src/topic2_fu_d/`, `scripts/topic2fu_d_*.py`, and `tests/topic2_fu_d/test_fud_r3_{guards,oracle,full_output}.py`; complete closure of `B1` (including algebraic proof P1, 28 reachable step-7 fixtures, 16-pair table, 3,000 oracle scenarios, 1,675-mutant union) and `B2` (`addendum_02.md` §3 errata `E5`, `E2'`, `E6`–`E9`, `W4`–`W5`, `errata_probe.out.json`, shipped-data invariants); C4 hygiene (0 hits); C5 GPU budget (`3.672 GPU-h <= 25.0 GPU-h`, `0 GPU-h` in r2/r3); and C8 report accuracy.
- **Phase C (Independent Test & Recomputation Execution)**: Write and execute `verification/victory_FU_D_r3/verify_victory_fu_d.py`, run `pytest` sequentially on `tests/topic2_fu_d` (389 tests) and the old 86-test suite (`STRICT_E2E=1`), and run `audit_layout.py`.

## Constraints
- Zero git writes (`git add`, `git commit`, `git push`, `git reset`, `git checkout` forbidden).
- Read-only on all frozen/production files (`src/`, `scripts/`, `tests/`, `results/`, `docs/`, `PROTECTED_HASHES.txt`).
- Never read `~/.claude/settings.json`, `~/.codex/config.toml`, or `~/.agents/memory/sycophancy/`.
- Strict C4 hygiene: never print or write any BIDS subject prefix substring (including hyphenated English words starting with those 4 characters), 6-digit HCP IDs, or 16-hex content hashes.
- CPU-only (`0 GPU-h`), at most 1 pytest process at a time (`CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2`).
- Write only inside `.agents/teamwork/tw-20261031-four-topics/victory_FU_D_r3/` and `verification/victory_FU_D_r3/`.
