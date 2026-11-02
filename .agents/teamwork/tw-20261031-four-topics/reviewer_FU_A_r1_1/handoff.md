# Handoff (hard) — reviewer_FU_A_r1_1, milestone FU_A (Topic 2 follow-up A), 2026-11-01T17:4xZ

## Review Summary
**Verdict: APPROVE.** Every FU-A criterion (F1–F3) and C1–C8 is met with evidence. The outcome is an escape: `inconclusive` (measurement capacity), because the frozen card's training-loop gate failed. That outcome follows the frozen card, is reproduced from the raw records, and the result report §9 costs the next steps. None of the issues below changes the verdict or blocks the milestone.

## 1. Observation
All commands ran from /home/juke/git/00IITP-AI. Logs are in verification/reviewer_FU_A_r1_1/.

**Integrity checks**
- C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gave rc 0, 67/67 OK (c1_check.txt).
- FU-A receipts (`grep -v '^#' … | sha256sum -c`): card_sha256 8/8, code_sha256_at_freeze 21/21, output_sha256 21/21, all OK.
- r1 receipts: code_sha256_at_freeze 33/33, output_sha256_r2 156/156, c4_sanitized 19/19, addendum_06 31/31, all OK.

**Tests**
- Old suite (`STRICT_E2E=1 … tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed (old_suite.txt).
- tests/topic2_fu_a: 69 passed, 1 skipped. The skip is the Stage-1 token scan: "scan not produced (wave not run)" (fua_tests.txt).
- tests/topic1_lagmotif: 88 passed.
- tests/topic2_rgpool: 116 passed, 0 failed. The FU-B-card failure the worker reported is gone now.

**Card before results**
- `git log` for the card: the host daemon commit 35d10a5 at 2026-11-02T01:05:25+09:00 (16:05:25Z) holds a card whose sha256 is 72be3e83…18fb. freeze_time.json says 16:06:01Z.
- The first run.json `start_utc` is 16:12:33Z.
- Both gate run.json files carry `fua_code_sha256` (6 files) and r1 `code_sha256` (13 files). All of them equal the freeze receipts.

**Gate records**
- run.json E: test_nmse 0.7746782345624923. run.json C: 0.7704092658872178.
- Σnum/Σden equals test_nmse in both. The test denominators are identical across arms.
- C is lower than E in 16/16 groups. Gain = 0.005510634589708632.
- Both runs: `fua_checks` max_within_cell_spread 0.0, `fua_rebound_sources_restored` true, and `fua_card_sha256` = 72be3e83….
- The training settings match the r1 Fplus_E_s0 record field by field: cfg, steps 8750, batch 16, lr, wd, warmup, mask 0.6, n_params 38712096.

**Verdict recompute**
- `scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs verification/reviewer_FU_A_r1_1/verdict_recomputed.json` reproduces the shipped verdict.json exactly (dict equality True): `inconclusive`.

**r1 comparison numbers**
- From results/topic2/2026-11-01/runs: F+ E 0.6769/0.6803, C 0.6582/0.6575, so the seed-mean gain is +3.06 %.
- The r1 VAL gain grew with training (seed 0: +1.4 % at step 2188, +2.6 % at 8750).
- These match report §4.

**B300 (read-only ssh, no GPU used)**
- sacct: 507_0 and 507_1 COMPLETED, ElapsedRaw 1480 and 1479 s, b300-01, gres/gpu=1 each. (1480+1479)/3600 = 0.822 GPU-h.
- The sha256 of the B300 runs/*/run.json and train_log.jsonl files equal the repo copies.
- /scratch/iitp4/fu_a/data/subjects has 88 entries, all matching `^h\d\d$`.
- No fua job is in squeue. No Stage-1 run directory exists.

**Ledger**
- Start and closing rows for job 507 (0.822 GPU-h) and explorer jobs 403 (0.056) and 427 (0.074). FU-A total is 0.952 of the 8 GPU-h cap.

**Code**
- The frozen loop `src/topic2_rgpool/train.py run()` looks up `HCPSource` and `FixtureSource` as module globals at call time (lines 174–176, 184).
- Training and both evaluations use that instance.
- So the rebinding in `src/topic2_fu_a/run.py fua_sources` takes effect, and it is restored in `finally`.

**Mutation testing**
- My rerun of the worker's harness (a byte-identical copy, sha256 bc17a2f1…) killed 31/31 verdict mutants, and the control passes (mutation_worker_copy/run.out).
- My own 16 extra mutants of target, sources, run and calib (mutation_extra/run_extra_mutants.py, whole tests/topic2_fu_a suite) killed 13/16, and the control passes.
- Survivors: X10 (wrong σ_v formula), X15 (wrong noise-share formula), X16 (NF floor counts empty cells). All three are in `src/topic2_fu_a/calib.py`. No test imports calib (grep finds 0 references).

**Fixture noise share (probe on the frozen generator at σ_v = 6.545925)**
- Voxel-weighted signal variance is 0.934 for F+ and 0.656 for F−. That gives a noise share of 0.220 for F+ and 0.287 for F−, at both T = 20 and T = 400.
- Card §7.1 and report §3/§4 state 0.248, using a "realized signal variance 0.80". That figure is the pooled F+/F− value, from Q_fix = 1.06097 in fixture_build.json: 0.2634 / 1.0610 = 0.248.
- I recomputed σ_v from NF with my own derivation: σ² = NF·n̄/(1−NF), giving 6.545925453832064, the same as the pinned value.

**C4 scan**
- 52 FU-A files (results, docs, src, scripts, tests, worker metadata): the only standalone 6-digit token is the synthetic sentinel "654321" in tests/topic2_fu_a/test_scripts.py:57–67. There are no `sub-` labels.
- token_scan_b300_gate.json: 1172 names, 14 files, 0 hits.

**Layout lint**
- audit_layout.py on the whole run root: PASS, 450 files, findings [] (layout_lint_run_root.txt).

## 2. Logic Chain
1. **F1.** The card is a new dated file. The daemon committed it with that exact sha before any run, and receipts pin it. It states the single change (target), the arms, seeds, budget, metric, δ = 1 %, the kill rule, and the gate rules. Gate deviations from r1 are declared in §7.3 before any run. → F1 met.
2. **F2.** The code lives only in the option's paths, and the r1 package is imported, not edited (r1 pins 33/33). The tests catch the targeted defects: a non-rebound source (X06, plus the dedicated test), the wrong cell order (X08, X09), a missing brain mask (X01, X02), the r1 voxel stream (X14), and the r1 verdict-defect classes (31/31). → F2 met. The calib gap is described under Caveats.
3. **F3.** The gate ran only via Slurm on b300-01 (sacct), within the cap (0.952/8), with ledger rows and run records. Results are in the dated dir. The report gives the verdict per card §8.3 step 2 and what it adds to r1 (§5). → F3 met.
4. **The escape outcome is correct by the card.** The F+ gain is 0.551 % < δ, so card §7.3 and §8.3 step 2 give `inconclusive`, and Stage 1 is not run. The recomputed verdict is identical. Costed options A′1–A′4 are in report §9. → It is "properly evidenced and costed".
5. **Integrity.** Results are not hardcoded: the verdict comes from the raw run records, and the B300 originals match by sha256. The gate used the frozen code (hashes in run.json), and the fixture stream really was the cell-constant field (spread 0.0, and the rebinding was traced in the code). The numbers are consistent with the physics: the noise floor, and the r1 low-noise gate at +3 %. I found no fabrication or facade.
6. **C1–C8 hold:** C1 rc 0; C2 suites green; C3 card first; C4 positional only, scan 0; C5 Slurm + ledger; C6 synthetic gate plus a public HCP view; C7 r1 is read-only; C8 the report cites only dated outputs.

## 3. Caveats (non-blocking issues, ranked)
- **N1 (minor, descriptive number):** The "realized noise share 0.248" in card §7.1 and report §3/§4 is the pooled F+/F− value. The F+ gate stream itself has ≈0.220 (F− ≈ 0.287). So the gate was closer to the TRAIN calibration (NF 0.209) than stated. That slightly strengthens the "realistic noise" reading.
  - The report's descriptive "E captures ≈30 % of the predictable energy" becomes ≈29 %.
  - The card cannot be edited. Fix: an erratum line in a dated FU-A addendum or a result-report note. No decision depends on it.
- **N2 (test-coverage gap):** `src/topic2_fu_a/calib.py` (Q, κ, NF, σ_v) has no tests, and mutants X10, X15 and X16 survive.
  - The shipped formulas are correct by derivation, and σ_v reproduces.
  - The frozen constants and code hashes guard reuse.
  - Any A′ card reusing σ_v should add a hand-computed calib test.
- **N3 (claim wording, G9):** Report §5.1 says a voxel-level gate at HCP noise "would almost certainly fail too". That is an untested inference, although it is labelled as such. Its "the r1 stop should be read as …" comes close to re-reading r1, which the steering forbids, although it is framed as scope and r1's own report already disclaims gate sensitivity. Suggest softening to "is expected to" or "suggests".
- **N4 (scope, for the PI):** By the frozen rule, FU-A produced no HCP evidence. Stage 1 (≈6.3 GPU-h, within cap) was gated out. The PI asked for "후속 A–E 전부"; A is completed as a gated `inconclusive`. A real-data reading needs A′2 or A′3 (new card plus PI decision).
- **N5:** It is a single-seed gate (declared). The capacity conclusion holds only for the inherited planted-effect strength and for E36/140k (report §8 acknowledges this).
- **N6:** κ_fix is pooled over F+ and F−, so the F+ target mean square is ≈1.13, not 1. NMSE is invariant; the effect on training scale is minor.
- **N7:** test_scripts.py uses the synthetic 6-digit sentinel "654321". It is presumably not a real HCP ID, but I did not check it against the subject list (a C4 count-only check could confirm).

**Not investigated:** I did not rerun NF/Q/κ on HCP TRAIN data, because that needs B300 CPU access to subject files, and the frozen-script repro log exists. I spent no GPU-h on a gate re-run: the records verify by sha256 against B300. I did not verify flock use on the ledger.

## 4. Conclusion
APPROVE FU_A. The verdict `inconclusive` (measurement capacity; F+ gain +0.551 % < δ 1 %) is correct under the frozen card 72be3e83…, Stage 1 correctly not run, r1 `stop` unchanged. N1 (erratum) and N3 (wording) are recommended doc fixes; N2 is a recommended test for any follow-up; none blocks.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # rc 0, 67 OK
for f in card_sha256 code_sha256_at_freeze output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_a/$f.txt | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done   # 0 0 0
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_a -q   # 69 passed 1 skipped
/home/juke/superclaude-env/bin/python3 -B scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs /tmp/x.json   # inconclusive
/home/juke/superclaude-env/bin/python3 -B verification/reviewer_FU_A_r1_1/mutation_extra/run_extra_mutants.py          # 13/16 killed; X10,X15,X16 survive
```
Invalidation: this review is void if any FU-A file hash above changes, if a Stage-1 or extra gate run.json appears in results/topic2/2026-11-02_fu_a/runs, or if the card sha differs from 72be3e83….
