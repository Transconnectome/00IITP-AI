# Handoff — challenger_M2H2_r2_2 (M2H2 r2 gate, Topic 3 H2 random-init control)

Type: Hard (task complete). Written 2026-11-01T21:30Z. Parent: root coordinator (session 5fddb83e).
Verdict: **CONFIRMED**. The verdict follows the frozen card, every shipped number reproduces independently, and the card was frozen before any result. Overall risk: LOW. Some new nonblocking coverage gaps were found. One of them contradicts the worker's wording "every guard in the stats script is now tested".

## 1. Observation

Commands were run from /home/juke/git/00IITP-AI on local DGX-Spark CPU, with nice, OMP_NUM_THREADS=2 and PYTHONDONTWRITEBYTECODE=1. GPU use was 0 GPU-h and nothing on connectome or B300 was touched.

- **Integrity.**
  - C1 `sha256sum -c sentinel/PROTECTED_HASHES.txt` gave rc 0 at 20:05Z and again at 21:26Z.
  - `results/topic3/2026-11-02_h2/output_sha256.txt` (61 entries), `addendum_07_sha256.txt` and `r2/addendum_08_sha256.txt` each gave rc 0 at the start and at the end.
- **Freeze order.**
  - Addendum 07 sha256 is `09b45220…edd84b`, as given in its receipt; the receipt mtime and the `frozen_utc` file both say 2026-11-01T15:57:40Z.
  - `git show 35d10a5:<card>` has the same hash. That commit is dated 2026-11-01T16:05:25Z, i.e. the card was in git before the gate job started (gate_record `started_utc` 16:22:21Z) and before the first random-init forward (random_record `started_utc` 16:32:21Z).
  - `gate_decision.json` (PASS) has mtime 16:31:46Z, before the random submit at 16:32:19Z.
  - The `code_sha256` in both job records (20 files, including vendor) equals the current repo code byte for byte, so the code that ran is the code under test.
- **Suites (mine).**
  - tests/topic3_h2: 167 passed, 0 skipped (185.8 s).
  - tests/topic3_spectral: 138 passed.
  - Old suite (STRICT_E2E=1, 3 paths): 86 passed.
  - tests/topic1_lagmotif: 88 passed.
  - Logs are in `verification/challenger_M2H2_r2_2/logs/`.
- **Independent recomputation** (`verification/challenger_M2H2_r2_2/recompute_independent.py`). It imports nothing from src/topic3_h2 or the stats script. It has its own pr_cov/pr_corr (SVD), index sets, sign-flip, bootstrap, Holm and decision rule, all written from addendum 07 §5–§6. It reads the sha-pinned T inputs and the shipped R1–R10 npz.
  - T A1 L2−L3 equals pinned Family A: cov 5.343854531110546 / SE 1.081055126274951; corr 6.038808669990018 / SE 0.899082569299712.
  - All 24 C+L labels match the shipped ones, with 0 mismatches. The largest absolute difference over points, CIs, seed effects and Holm p is 1.8e-15. The deltas are identical.
  - C1 INC: point 0.012449, CI95 [0.010379, 0.014476], p_holm 0.0002, δ 0.011375.
  - C2 INC: point 0.029531, CI95 [0.025616, 0.033409].
  - C3 TE+: point 5.088484, CI95 [2.930262, 7.246707], δ 2.671927.
  - C4 TE+: point 5.786985, CI95 [4.007065, 7.566906].
  - Family L token: L1 TE− for cov and corr; L2 corr, LN0L2 corr, L3 cov and L3 corr EQ; the rest INC.
  - Family L subject: L1 to L3 TE− for both estimators; L0 INC.
  - R0 vs my T per-index-set PR: max rel diff 6.35e-7.
- **Errata in addendum 08, recomputed independently.**
  - E1 δ-sensitivity transitions on a grid of step 1e-4: C1 0.1576 / 1.0176, C2 0.4581 / 1.1115, C3 0.5484 / 1.2912, C4 0.6636 / 1.2057. These agree with the addendum to the grid step.
  - E8 single-seed labels: C1 EQ for seeds {1, 5, 8}, TE+ for {4, 7, 9, 10}, INC for {2, 3, 6}; C2 TE+ for {4, 5, 7, 9, 10}; C3 and C4 TE+ for all seeds. These match.
  - E2 R1: −1.6067 [−3.7690, +0.5555] (cov) and −0.7363 [−3.1814, +1.7087] (corr). These match.
  - E3 L0 subject: cov −0.0608, 95% [−0.3297, 0.208], 90% [−0.2865, 0.1648]; corr −0.1307, 95% [−0.3958, 0.1345], 90% [−0.3532, 0.0918]. These match.
- **Report claims spot-checked.**
  - Confirmed: C2's seeds 3 and 8 fall at or below δ (effects 0.0212 and 0.0205). The per-seed H1a under the card rule is significant and positive in 9 of 10 seeds, while seed 4 gives −0.0004 with p_holm 0.5217. Per-seed D1 cov is robust for seeds 5, 7 and 10. Token-level Holm p values are all at most 0.0149.
  - **Not confirmed (new):** report §3 says that at L2 cov token level "one seed's effect (−0.079)" fails the seed condition. In fact the effects of five seeds lie at or above −log 1.10 = −0.0953: seeds 1, 2, 3, 6 and 7, with −0.0790, −0.0923, −0.0832, −0.0931 and −0.0786. The label (INC) is unaffected. This error is not among errata E1–E8.
- **decide() fuzz** (`fuzz_decide.py`). It compares the shipped `decide` with an independent 3-predicate oracle. Run 1 used 200k centred cases, run 2 used 200k shifted cases (TE+ 420, TE− 474, EQ 16727), and values were snapped to ±δ and their float neighbours. There were 0 mismatches. Only the run-2 version of the script is kept; the run-1 output is in logs/fuzz_decide.log.
- **Gate record values** (gate_decision.json):
  - G1: 399 windows, max rel_fro 7.78e-7 (tolerance 1e-5), max |Δ| 6.7e-6.
  - G2 re-pool: max diff 7.0e-7.
  - G3 local: max rel 7.25e-8.
  - G4: 568 tensors loaded, 0 missing encoder keys, the only unexpected key is `augment_comp.smooth_kernel`.
  - G5: every control fails in all 84 cells; the smallest rel_fro is 4.6e-4.
  - The index-set sha `cd020fe8…` is the same in both jobs.
- **Mutation harness of new mutants** (`new_mutants.py` → `new_mutants.out.json`, sha256 96f7f796…). It used 44 mutants, none among the 115 r1-union edits (checked by string), plus 6 oracle mutations. Two copied trees were used and both baselines gave 167 passed. Runtime was 4424 s. Every mutant applied exactly once, there were 0 invalid runs, every restore was byte-identical, and the production outputs are unchanged.
  - **KILLED (25):** S1, S3, S5, S7, S9, H1, H4, H5, H6, H7, H13, C2, C4, C5, D1, D6, D7, D9, D13, Mo3, Mo5, Mo6, Mo7, Da2, Da3.
  - **Oracle mutations (test the test), 6 of 6 KILLED** by the regression test with the receipt test excluded: a C1 label changed to EQ; one float of the Family L subject L0_cov CI90 changed by a relative 1e-9; a dropped key; one extra list element; a G3 local-recheck value in gate_decision; a flipped per-seed corr-robust flag. So the leaf comparator can tell these changes apart.
  - **SURVIVED (19), outside the r1 classes:**
    - Stats script (`scripts/topic3h2_stats.py`):
      - S2: `rec.get("G2", {"ok": False})` → `{"ok": True}`. A gate record with no G2 entry would give gate PASS.
      - S4: `_dump`'s BIDS-prefix refusal disabled.
      - S6: `vendor_ok is True` → truthy. This is practically equivalent, because verify_vendor returns True or raises.
    - Provenance: P3, the hash check of `verify_pinned` disabled. The script then reads the T inputs without checking them; other receipts still cover those files.
    - Comparator:
      - C1: a stored dump layer with zero norm gives rel_fro 0 instead of inf.
      - C3: a shape mismatch in `stats_match` does not set ok = False.
    - In-job driver, which only offline tests can reach:
      - D2: G4 ignores `load["ok"]`.
      - D3: the checkpoint sha is always ok.
      - D4: `seed_hashes_distinct` always True.
      - D5: `rebuild_same_seed_identical` always True.
      - D8: the pinned-spectra hash is not checked.
      - D10: the input-contract halt checks only the subject count.
      - D11: G2 ignores row order.
      - D12: a failed G2 pin is ignored.
    - Model and data:
      - Mo2: the depth guard is off.
      - Da1: the subject dirs are not sorted.
    - Launcher `collect`:
      - L1: the forbidden-file check (pooled, .pt) is off.
      - L2: the log ID scan is off.
      - L3: the remote ID grep is off.
- **ID scan.** No `sub-` bytes appear in results/topic3/2026-11-02_h2/**. The single `sub-` in test_h2r2_gate_components.py is the synthetic format string `"sub-SYN%02d"`. In my own files, `sub-` appears only inside mutant code strings. I printed or wrote no identifier.
- **Ledger.** The worker's prev_snapshot (sha 9f9843eb…) is an exact byte prefix of the current ledger, so the file was only appended to. Correction rows for 218063 and 218064 are at lines 142–143.

## 2. Logic Chain

1. The card was frozen before any result. The receipt time, the git commit at 16:05:25Z and the job start times (16:22Z, 16:32Z) put the freeze before the gate job and before the first random-init forward. G1 says "the gate PASS record exists before random launch", and the launcher code requires that record; this holds.
2. The verdict follows the card's rules.
   - The independent code has no shared code path with h2stats and gives the same 24 labels and numbers to 1.8e-15 (Obs. recomputation).
   - The shipped `decide` agrees with an independent reading of the §6 table on 400k boundary-heavy cases.
   - So the labels do not depend on a defect in the shipped stats code.
3. The shipped random-arm aggregates are the job outputs of the code under test: the job records' code hashes equal the repo code. r1 verifiers reran seeds 1, 3, 4, 7 and 8 on GPU, bitwise or within 2.3e-15 (addendum 08 §2, prior evidence). Iteration 2 changed no code or data. A further GPU rerun would therefore test nothing new, so I spent 0 of my 1 GPU-h.
4. The worker's closure claim for the 37 named r1 survivors fits its harness output: 37 are shipped_full SURVIVED and both new_only and extended KILLED, and 78 others are KILLED. My own harness was green on baseline with the same extended suite. The regression comparator kills all 6 oracle corruptions, including a 1e-9 relative float change. So the regression test is not vacuous.
5. 19 new mutants survive.
   - None changes a shipped number or label. The code that ran is the unmutated repo code (point 3), and the job records show each guarded quantity with its passing value: G2 present and ok, load ok, ckpt ok, hashes distinct, rebuild identical, 57 × 7, row order True. The ID scan of the outputs is clean.
   - So these are regression-protection gaps, not result defects.
   - S2 and S4 (and P3, reached through the stats script) do contradict the worker's sentence "the verdict path and every guard in the stats script are now tested". S2 is in the same family as the r1 cmd_gate survivors N55–N57: the local gate decision depends on an untested branch. It is not among the named classes that addendum 08 §7 proposes as the r2 gate scope.
6. Under the proposed fixed scope (named r1 classes closed, no regression, integrity) every gate criterion holds. That gives CONFIRMED, with S2 and S4 and the report §3 seed-count error flagged as nonblocking for root to decide.

## 3. Caveats

- I did not rerun the worker's 115-edit union harness. I checked only its output's internal consistency and ran my own 44-plus-6 set.
- There was no GPU or connectome rerun (reason in Logic step 3). The equivalence of the random arms rests on r1 reruns plus the code-hash match.
- My recomputation uses the same documented RNG algorithms as the frozen resampling functions (needed for exact p and CI equality), so it does not test the soundness of those primitives. They are pinned M2 code that was verified earlier.
- The mutant classification "outside the r1 classes" is by string identity against the union file and by meaning. Root or the PI decides whether S2 or S4 count as the r1 class "guards of scripts/topic3h2_stats.py".
- δ (0.5 × the trained effect) is still a worker choice awaiting the PI (addendum 08 §8). C3 TE+ holds only for f ≤ 0.548, which I reproduced.
- Host load was high (about 30 pytest processes from other agents). Survivor runs took 200–590 s, but none timed out.

## 4. Conclusion

**CONFIRMED.**
- The H2 verdict stands: gate G PASS; C1 INC, C2 INC, C3 TE+, C4 TE+; Family L as shipped. It follows addendum 07 §6 exactly, reproduces independently to 1.8e-15, and was produced after the card was frozen and committed.
- Errata E1, E2, E3 and E8 of addendum 08 are numerically correct.
- The new tests are real regression guards: 25 of 44 new mutants and 6 of 6 oracle corruptions are killed.
- Nonblocking issues for root:
  - (a) Mutant S2 (gate PASS when the in-job record lacks G2) and S4 (output ID guard) survive. The worker's claim "every guard in the stats script is now tested" is therefore inaccurate. Suggested fix: two more guard tests in a new additive file — G2 key missing, and a payload containing the BIDS prefix — no code change.
  - (b) 17 in-job, launcher, model and comparator guards are untested (D2–D5, D8, D10–D12, Mo2, Da1, C1, C3, P3, L1–L3). None has an effect on the shipped results.
  - (c) Report §3 erratum: at L2 cov token level, 5 seeds (1, 2, 3, 6, 7) fail the seed condition, not one. The integrated R1 report should quote it correctly.
  - (d) The δ PI decision is still owed.

## 5. Verification Method

- `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -I verification/challenger_M2H2_r2_2/recompute_independent.py` takes about 1 min and must print `label mismatches []`.
- `… python3 verification/challenger_M2H2_r2_2/fuzz_decide.py` must print `mismatches 0`.
- `… setsid nohup nice python3 verification/challenger_M2H2_r2_2/new_mutants.py > verification/challenger_M2H2_r2_2/logs/new_mutants.log 2>&1 &` takes about 75 min; compare the result with `new_mutants.out.json`. It is invalidated if any file under src/topic3_h2, scripts/topic3h2_* or tests/topic3_h2 changes.
- Quick S2 check, done in memory at 21:3xZ: with the shipped default `rec.get("G2", {"ok": False})`, `compare.gate_verdict` gives ('FAIL', ['G2']) when G2 is missing; with the S2 default it gives ('PASS', []). So the shipped code is correct and only its test is missing. With S2 applied, the extended suite stays green (new_mutants.out.json).
- Integrity: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`, plus the three H2 receipts.
- My artifact hashes:
  - recompute_independent.py eeeb8d31…
  - recompute_independent.out.json bec96c2a…
  - new_mutants.py ee1367b3…
  - new_mutants.out.json 96f7f796…
  - fuzz_decide.py b4e3fdf6…
