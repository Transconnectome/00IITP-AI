# Handoff — challenger_FU_D_r2_2 (FU_D iteration-2 gate). Type: Hard. Verdict: REFUTED

The shipped result holds: verdict `inconclusive` (measurement capacity at E192), the F+ gains 0.363 % / 0.655 % < δ, the card freeze, the provenance and C4 were all independently reproduced. The REFUTED verdict is about the r2 repair claims, not the shipped verdict:
- (B1) A new non-equivalent verdict-path mutant survives the whole 195-test suite. It flips a Stage-1 verdict from `inconclusive` (card §8 step 7) to `stop (killed)`. This refutes "0 non-equivalent survivors remain" and the F2 requirement "verdict code tested".
- (B2) The frozen loader silently accepts aliased duplicate run directories and lets them override the canonical record. This is a card §8 departure that is missing from the addendum_01 errata E1–E4, and it can turn a failing F+ gate into a passing one.

Neither B1 nor B2 changes the shipped verdict.

## 1. Observation

**Integrity (all reproduced, 2026-11-01 ~22:00–22:40Z):**
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gives rc 0, 67/67, both at the start and at the end.
- FU-D receipts: addendum_01 23/23, card 1/1, code_sha256_at_freeze 29/29, output 34/34.
- r1 receipts: code 33/33, output_sha256_r2 156/156, addendum_06 31/31.
- r1 `card_sha256.txt` is 6/8 and `output_sha256.txt` 27/43 (hcp_manifest.json and split.json FAILED). These are pre-existing r1 receipts superseded by the C4 sanitisation (c4_sanitized 19/19). They are not FU-D files and the worker did not claim them.
- `verdict.json` sha256 f6b295d9…59fc is unchanged.

**Freeze timing:**
- The card file mtime is 2026-11-01T15:40:57Z.
- It was first committed by the host daemon in 34f4b30 (2026-11-02T00:50:24+09:00 = 15:50Z) with the same sha 1b7fee6c…001b.
- The receipt is dated 16:06:07Z.
- The first post-freeze GPU job (511) was submitted at 16:13:50Z, and the first result file (smoke/equiv.json) was written at 16:35Z.
- The gate jobs 534/535/536 started at 17:46Z. So the card was frozen before any FU-D result.

**Headline recomputation** (`verification/challenger_FU_D_r2_2/probes/recompute.py`, exact Fractions from raw `test_num`/`test_den`, no project imports):
- E 0.6558494816918741, C 0.653467876277415, S 0.6577736746995909. Each equals Σnum/Σden exactly (absdiff 0).
- gain_C_vs_E = 0.003631329262188746 and gain_C_vs_S = 0.00654601816368273. Both are < 1/100, so the gate fails. This matches verdict.json to within 1e-15.
- The r1 E36 F+ gains reproduce: C-vs-E 2.772 % / 3.348 % and C-vs-S 2.900 % / 2.970 %. Their means, 3.06 % / 2.935 %, confirm erratum W1.

**Provenance** (`probes/provenance.py`), for all 3 gate runs:
- argv arm, seed 0, perm key, perm file Fplus, steps 8750, mask seeds 7001/7002 (confirms E3).
- Wrapper sha = the freeze receipt d598989b…; all 8 FU-D module shas = the freeze receipt; frozen r1 train script and 13 rgpool shas = the r1 receipt.
- Slurm 534/535/536 COMPLETED, post_checks_ok true.
- `test_den` is identical to r1 `Fplus_*_s0` (same windows and masks).
- The smoke equivalence value (0.9908706340280367) equals r1 hcp_E_s0.

**Other checks:**
- Ledger: FU-D worker+explorer GPU-h = 3.672, and FU-D verifiers 0.048 (r1). The cumulative ledger at the Fplus_S closing row (line 156) is 30.665 GPU-h, which confirms the report's "30.665".
- C4: the frozen `scripts/topic2fu_d_c4scan.py --out <mine>` gives 79 files, 0 token hits, 0 BIDS hits. My own count-only scan for 6-digit ID-shaped integers and `sub-` labels over the FU-D results, src, tests, docs, scripts, worker_FU_D_r2 verification and metadata found 96 files and 0 hits.
- Suites: tests/topic2_fu_d 195 passed; old 86 passed; tests/topic1_lagmotif 88 passed; tests/topic2_rgpool 113 passed, 3 skipped.

**Worker's 8 equivalence claims, each checked against the code:**
- S023/S025: the "(keep pending F-)" reason is set only in the s1-keep branch, and with F− missing a keep always yields it, so the three conjuncts imply each other.
- S160: attempts are keyed 0/1 per key in a dict.
- S181: only `!= "completed"` is consumed, and the state is not written.
- S207/Q19: per-record token order equals the split.
- Q08: dead store.
- Q21: `rec` is None for unchosen attempts.

All 8 are equivalent. I agree.

**My mutation run** (`verification/challenger_FU_D_r2_2/mut/`; 62 independently designed mutants + control; copied trees; tests/topic2_fu_d minus the E192 build and the belt test; at most 2 at a time):
- Control: 189 passed.
- 53 killed, 9 survived, 0 invalid. Survivors: C12, C23, R04, R07, S05, S07, S08, S09, S11. None changes the shipped verdict.json.
- Run 2: X45r (δ=0.0036), X45u (δ=0.0066) and X22r (joint-reading text) are all killed. The r1 blocking classes are closed.

**B1 witness** (`witness/witness.py` → `witness_C12.out.json`):
- Mutant C12, in `src/topic2_fu_d/verdict.py::_stage1_category`, changes `if c2 != cat:` to `if c2 != cat and c2 != "inconclusive":`.
- Input: Stage-1 n = 5, seed 4 stalled with I1 = 0, other seed gains [0, 0.9 %, 0.1 %, 0.8 %].
- Frozen code: `inconclusive`, reason "stall-sensitive: category stop with all seeds, inconclusive without stalled seeds".
- Mutant: `stop`, reason "upper 95% bound of I1 < delta … (killed)".
- The suite stays green (189 passed). The only step-7 flip test, `test_verdict.py::test_stall_that_flips_the_category_gives_inconclusive`, covers the inconclusive→stop direction (sensitivity category `stop`), never stop→inconclusive.

**B2 witness** (`probes/adversarial.py` → `adversarial.out.json`; synthetic records only):
- `design.DIR_RE = r"^(hcp|Fplus|Fminus)_([ECS])_s(\d+)(_a1)?$"`, and `int()` accepts zero-padded and Unicode digits. So `Fplus_C_s00` and `Fplus_C_s٠٠` both parse to the planned key ('Fplus','C',0), attempt 0.
- `records.load_runs` does `found.setdefault(key, {})[att] = …`, so the later-sorted alias silently overwrites the canonical directory, even under `strict=True`.
- P1b: the canonical `Fplus_C_s0` has a gate-failing C = 0.699 (gain 0.14 %), and an alias `Fplus_C_s00` holds C = 0.60. The script exits rc 0 with `fplus_gate.pass = true` (gain 14.3 %) and `used_dir = "Fplus_C_s00"`. A failed gate becomes a pass with no protocol error.
- P1c: same with Unicode digits.
- Card §8 says "duplicate or mismatching records … are protocol errors (the verdict script stops)". Addendum_01 E1 covers only unplanned directories skipped when the gate fails. This alias case is accepted when the gate passes, in strict mode, and is not listed.
- The shipped data are protected: `test_fud_r2_guards.py::test_shipped_runs_dir_is_exactly_the_planned_gate_and_loads_strictly` pins `sorted(os.listdir(runs)) == the 3 names`.

**Other survivors and probes (nonblocking), all with witnesses in `witness/witness_script.out.json` or by inspection:**
- R07 (`post_checks_ok is not True` → `is False`): a sidecar without the key is accepted (the frozen code raises).
- S11 (gate-incomplete branch dropped): the mutant crashes with KeyError 'stage1' where the frozen code gives `no_verdict`.
- S05: no `protocol_flag_fminus` for F− records that are failed rather than completed.
- C23: the floor early-return is removed; the category is unchanged and only a stall_sensitivity entry is added.
- S07/S08/S09: hierarchical bootstrap seed 0→1, B 10,000→1,000, and per-subject mean axis. These are card §8 secondary pins with no test (descriptive, Stage 1 only).
- R04: equivalent, because the split tokens are all hNN and the order check enforces equality.
- Probes:
  - P2: NaN test_nmse gives `inconclusive` (confirms E2).
  - P3: an inf denominator with test_nmse 0 is accepted and the gate passes. The E2 reading rule "any non-finite error term" covers this, but the E2 headline names only NaN test_nmse.
  - P4: negative NMSE is accepted.
  - P5: `seed_plan.json` with n_seeds 5 and seeds [0,1,2] is accepted.

## 2. Logic Chain
1. The receipts, the freeze order and the raw-record recomputation agree with verdict.json, so the shipped verdict follows card §8 step 2 (F+ computed and failed → inconclusive; Stage 1 not read). The headline is CONFIRMED.
2. ACCEPTANCE F2 requires "verdict code tested (avoid the V06–V10 defect classes)", that is, verdict-path changes that flip a category with the suite green. The worker's r2 claim is "0 non-equivalent survivors remain".
3. C12 is a one-line verdict-path change. The witness shows it changes a pre-registered card rule (step 7) outcome from inconclusive to stop, a kill verdict, with all 195 tests green. So the claim in step 2 is false and F2 is not met for step 7. This is the same "flip if code changed" class that failed the r1 gate (X45/X22), and the class the M3 r2 gate treated as REFUTED even though no shipped verdict changed.
4. B2 is a reachable defect in the frozen loader that contradicts card §8 and can invert the gate decision. Addendum_01 presents E1–E4 as "where the frozen code or text departs from the card", but this departure is missing. Its reading rules (E1 checks for directories "outside the plan") arguably cover a zero-padded name, but E1 is stated only for the failed-gate path.
5. Neither B1 nor B2 is reachable on the shipped data: Stage 1 was not run, and the runs directory listing is pinned to the 3 exact names. So the shipped verdict stands, and both fixes are additive.

## 3. Caveats
- No GPU used (0 GPU-h, no ledger row). I did not re-score the B300 checkpoints. Three r1 verifiers did so bit-exactly (ledger jobs 574/575/576); I relied on raw records plus provenance instead.
- I did not rerun the worker's 423-mutant union; I checked its 8 equivalence claims by reading the code. My 62 mutants were designed independently; some overlap the worker's sweep (those were killed in both).
- Whether B1/B2 are blocking for this fixed-scope r2 gate is a root/PI decision. Neither affects the shipped verdict, and FU-D Stage 1 will never run under this card. The risk is reuse of this verdict code by a future card (report §5: D′, D-gate-seeds, D-mid, D-long).
- `verification/challenger_FU_D_r2_2/mut/work` is an empty leftover directory. A cleanup `rm` was denied by the harness and I did not work around it.

## 4. Conclusion
**REFUTED** for the r2 gate claims, with the shipped result CONFIRMED.

Blocking:
- **B1:** add a test where the all-seed category is `stop` (or `keep`) and the stall-dropped category is `inconclusive`, and assert `inconclusive (stall-sensitive)`. This kills C12.
- **B2:** record the alias/duplicate-directory acceptance as erratum E5 with a reading rule (a run directory whose name is not exactly `run_name(key, att)` is a protocol error). The existing listing test already covers the shipped data. Optionally add a test that documents the shipped invariant.

Nonblocking:
- Tests for R07 (sidecar without `post_checks_ok`), S11 (gate incomplete with Stage-1 records → `no_verdict` and Stage 1 unread), S05 (failed F− records flagged), and S07/S08 (B = 10,000, seed 0).
- Broaden the E2 headline to non-finite error terms (P3).
- P4 and P5 as notes.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/challenger_FU_D_r2_2/probes/recompute.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r2_2/probes/adversarial.py   # P1b: pass=true, used_dir Fplus_C_s00
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r2_2/witness/witness.py       # cases 3,4: frozen inconclusive, C12 stop
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_D_r2_2/mut/run_mut.py C12       # survives (suite green)
```
Invalidation conditions:
- B1 is closed when `run_mut.py C12` reports it killed.
- B2 is closed when an addendum records E5, or when `adversarial.py` P1b raises a RecordError (that would need a code change and a new card).

Artifact sha256: `verification/challenger_FU_D_r2_2/logs/artifact_sha256.txt`.
