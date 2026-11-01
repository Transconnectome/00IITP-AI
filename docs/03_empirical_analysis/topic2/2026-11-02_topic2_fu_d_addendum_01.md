# Topic 2 follow-up D (FU-D) — addendum 01 (2026-11-02 KST = 2026-11-01 ~21Z, worker_FU_D_r2, written AFTER all FU-D results)

Everything below is post hoc. No governed computation changed: no training, evaluation, seed plan or verdict
computation was rerun to produce a new governed output, and no frozen file was edited. Untouched: the FU-D card
(`2026-11-02_topic2_fu_d_card.md`, sha256 1b7fee6c…001b), the 29 files of `results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`
(`src/topic2_fu_d/*`, `scripts/topic2fu_d_*.py`, the 12 shipped `tests/topic2_fu_d` files), the runs, `verdict.json`
(sha256 f6b295d9…59fc), the result report and every existing receipt. The FU-D verdict stays **`inconclusive`
(measurement capacity at E192)**: F+ gate gains (E−C)/E = 0.363 % and (S−C)/S = 0.655 %, both < δ = 1 %; Stage 1
not run; the r1 E36 `stop` stands alone. GPU used for this addendum: 0 GPU-h.

## 1. Why this addendum exists: the FU-D r1 gate

The FU-D r1 gate failed because challenger_FU_D_r1_1 returned REFUTED on two blocking items; the other four verifiers
passed (reviewer ×2 APPROVE, challenger_FU_D_r1_2 CONFIRMED, auditor CLEAN), and every verifier reproduced the shipped
verdict (three of them re-scored the saved gate checkpoints bit-exactly on B300).

1. **X45.** Changing `DELTA = 0.01` in `src/topic2_fu_d/config.py` to 0.0036 (or 0.003: Q09, M19, A02, A04) flips
   the shipped verdict from `inconclusive` to `no_verdict` while the whole suite stays green. No test pinned δ.
2. **X22.** Changing the `inconclusive` entry of `JOINT_READING` in `scripts/topic2fu_d_verdict.py` makes the shipped
   joint reading say "null replicates at E192" with the suite green (Q20, A13). No test pinned the table or the
   shipped verdict.

Both are test-coverage gaps in the "flip if code changed" class; the shipped code is the freeze-receipt code (29/29
OK) and the shipped verdict was recomputed with δ = 0.01. They are closed here by an additive test file (§3).

## 2. Errata: where the frozen code or text departs from the card

The card governs. The frozen code is not edited; the reading rules below apply to any `verdict.json` the frozen
script writes. Each item states why the shipped verdict is not affected, and §3 group 4 pins that evidence as tests.

**E1 (G2). Unplanned run directories are skipped, not rejected, when the F+ gate fails or is incomplete.** Card §8:
"Unplanned directories, duplicate or mismatching records … are protocol errors (the verdict script stops)." The
script first reads the gate with `R.load_runs(rdir, GATE_RUNS, exp, strict=False)`; if the gate failed or is
incomplete it never makes a strict load, so a directory such as `Fplus_C_s1` or `junk_dir` is ignored (only `hcp_*`
directories raise `protocol_flag`). When the gate passes, the strict load raises `RecordError` as the card says. The
shipped test `test_records.py::test_non_strict_skips_unplanned_dirs` encodes the loader option, not the card rule.
*Reading rule:* a verdict from a runs directory that holds any directory outside the plan is a protocol error
(`no_verdict`, protocol), whatever the script wrote; check the directory listing. *Shipped:* `runs/` holds exactly
`Fplus_C_s0`, `Fplus_E_s0`, `Fplus_S_s0`, no `seed_plan.json`, and a strict load over every possible run key succeeds.

**E2 (G1). A NaN `test_nmse` is accepted.** `records.validate_completed` rejects a record when
`not math.isfinite(pooled) or abs(pooled - rec["test_nmse"]) > tol`; with finite num/den and `test_nmse = NaN` the
difference is NaN, the comparison is False, and the record passes. The gate then compares NaN gains with δ, fails,
and the script reports the shipped category `inconclusive` instead of a protocol error. *Reading rule:* a record with
a non-finite `test_nmse` (or any non-finite error term) is a protocol error and voids the verdict. *Shipped:* every
gate record has 16 finite error terms, finite validation values, and `test_nmse == Σnum/Σden` exactly.

**E3. The evaluation mask seeds are not record-validated.** `records.HP_FIELDS` checks steps, batch, lr, wd, warmup
and mask ratio, not the validation/test mask seeds 7001/7002. *Reading rule:* the mask seeds are read from the
sidecar argv. *Shipped:* each gate sidecar argv carries `--val-mask-seed 7001 --test-mask-seed 7002 --steps 8750`,
and each gate record's `test_den` equals the r1 E36 `Fplus_*_s0` denominators exactly (same windows and masks).

**E4. The wrapper check is optional.** `records.validate_completed` compares the sidecar wrapper sha256 only when the
script is given `--wrapper-sha256`. *Reading rule:* a FU-D verdict is valid only when produced with the wrapper sha256
of `code_sha256_at_freeze.txt` (d598989b…b84e). *Shipped:* the shipped `verdict.json` regenerates byte for byte with
that value (§3 group 3), and every gate sidecar carries it.

**Wording errata (no effect on any category).**
- **W1, card §7.1.** "+3.06 % / +2.93 %" are the r1 E36 two-seed means of the C-vs-E and C-vs-S F+ gate gains, not
  the values of the two seeds. Per seed: C-vs-E 2.772 % (seed 0) and 3.348 % (seed 1); C-vs-S 2.900 % and 2.970 %.
- **W2, card §0.** The explorer job list names jobs 396, 404 and 430; the stated total of 0.097 GPU-h also counts job
  418 (0.001 GPU-h; placed on b300-02 by Slurm, failed after 1 s, nothing ran).
- **W3, result report §0 and §2.** "shrinks with scale", "closes it further" and "the box gather still carries the
  planted structure in the right direction" rest on one seed per scale with no interval. The E192 C-vs-E gain
  (+0.36 %) is smaller than the r1 between-seed difference of the same gain (2.772 % vs 3.348 %, 0.58 points).
  *Reading rule:* these sentences are descriptive, one seed per scale, no interval; no scale trend is claimed.

## 3. Added tests: `tests/topic2_fu_d/test_fud_r2_guards.py` (new file, 50 tests, CPU, about 2 s)

Card values are written as literals (δ = 0.01, the five §9 (c) reading strings, the shipped reason and gains, the
freeze-receipt wrapper sha256); no test compares the code with itself. The verdict script is always run with `--out`
in `tmp_path`. No test asserts the fixed behaviour of E1/E2 (that test would fail on frozen code; marking it skip or
xfail would hide a defect); the shipped inputs are pinned to lie outside them instead.

| group | what it pins | r1/r2 mutants it kills |
|---|---|---|
| 1 δ | `K.DELTA == 0.01` and the card text "δ = 0.01"; the δ default of `fplus_gate`, `fminus_gate`, `primary_category`, `decide`, `needs_fminus`; default-δ bands (F+ gains 0, 0.36 %, 0.5 %, 0.99 % fail, 1.01 % and 2 % pass; both contrasts needed; F− 0.99 % passes, 1.01 % fails); `decide` and `primary_category` at default δ; script runs with gate gains of 0.5 % (inconclusive), 0.5 % plus stray `hcp_*` records (inconclusive and `protocol_flag`), 1.01 % (gate passes, `no_verdict` "seed plan missing") | X45, Q09, M19, A02, A04, D1/X45b, D2, D3, D4, D5, upward δ |
| 2 joint reading | the five-entry `JOINT_READING` table equals the card §9 (c) literals; each literal tied to its frozen card clause; `inconclusive` and `no_verdict` say "adds no decision … r1 E36 stop stands alone" and never "replicates" | X22, Q20, A13, J1, J2, J4 |
| 3 shipped verdict | inputs and `verdict.json` match `output_sha256.txt`; regeneration into `tmp_path` is byte-identical and leaves `results/` unchanged; a run on a copy of the shipped runs deep-equals the pinned JSON, with exact verdict, reason, δ, gate gains, joint reading, run states, no seed plan, no Stage 1, no protocol flags; an exact-fraction oracle (δ = Fraction(1, 100)) from the per-group num/den puts both gains strictly in (0, δ) | X22, J3, R1, any flip of a shipped decision output |
| 4 shipped invariants | runs dir exactly the three planned gate dirs, no seed plan, strict load succeeds (E1); every record finite, 16 terms, `test_nmse == Σnum/Σden`, validates with the freeze wrapper sha (E2, E4); sidecar argv 7001/7002/8750/16/0.6/E192 and `test_den` equal to r1 (E3); card §5 constants | (E1–E4 evidence) |
| 5 record guards | wrong permutation-file sha; 15, 17 and 1 error terms; `test_nmse` off by 1e-9 and 1e-3 relative; missing or wrong validation step; sidecar with the right config name but a wrong config dict | X35/Q16, X37, Q14/M21/A11, M12, A05 (reviewer_FU_D_r1_2), Q15, Q17 |
| 6 verdict internals | seed-mean NMSE is a mean, not a median; a monkeypatched disagreement of the frozen `stats.verdict` raises `AssertionError` | Q03, X49/Q05 |
| 7 wrapper | the positional-view check accepts a base outside and refuses a base inside a `worker_M3_r1` tree; `main()` returns 3 when post-checks fail and 0 when they pass (fake frozen trainer, pass-through monkeypatch) | A05 (auditor), Q24 |
| 8 belt | the 29 frozen FU-D files and the card match their freeze receipts | every code change (excluded from the semantic mutation run, §4) |

**File set.** The card §13 freeze set lists 12 files under `tests/topic2_fu_d/`; with this addendum the directory
holds exactly those 12 plus `test_fud_r2_guards.py` (pinned in `results/topic2/2026-11-02_fu_d/addendum_01_sha256.txt`).

## 4. Mutation evidence

MUTATION_SECTION_PENDING

## 5. No-regression evidence

NOREGRESSION_SECTION_PENDING

## 6. What this addendum does not do

- It does not rerun or extend the F+ gate (seeds 1–2 ≈ 7.1 GPU-h) or run Stage 1. After a failed gate that would be an
  outcome-dependent extension with no pre-registered combination rule; it needs a new card and a PI decision.
- It does not upgrade `inconclusive (measurement capacity)` into a mechanistic claim: the F+ gate cannot tell
  "the apparatus cannot detect δ at E192" from "M0 grouping stops mattering at E192".
- It does not re-label the r1 E36 `stop` or pool r1 and FU-D seeds (card §9 (d)).
