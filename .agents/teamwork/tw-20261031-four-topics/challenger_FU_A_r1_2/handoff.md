# Handoff (hard) — challenger_FU_A_r1_2, milestone FU_A, 2026-11-01T17:5xZ

**Verdict: CONFIRMED.** The shipped FU-A verdict `inconclusive` (measurement capacity) holds. I reproduced it independently and it follows the frozen card.

Nothing I found blocks the result. There are nonblocking findings: verdict and calibration guards that no test covers, and a descriptive error in the card and the report about the F+ noise share.

GPU use: 0 GPU-h. B300 work was read-only checks plus one CPU-only Slurm step (job 540, debug partition, b300-01, no GPU).

## 1. Observation

**Integrity and receipts**
- C1 holds at start and at end: `sha256sum -c sentinel/PROTECTED_HASHES.txt` returned rc 0 with 67/67 OK (`verification/challenger_FU_A_r1_2/c1_start.txt`, `c1_end.txt`).
- All FU-A receipts verify: `card_sha256.txt` 8/8, `code_sha256_at_freeze.txt` 21/21, `output_sha256.txt` 21/21.
- The r1 `code_sha256_at_freeze.txt` verifies 33/33.

**Card frozen before results**
- `git log` (read-only) shows the host autocommit 35d10a5 at 2026-11-01T16:05:25Z already contains the card, with sha256 72be3e83…18fb.
- That commit is earlier than the job 507 tasks, which started at 16:12:31Z (`sacct`) / 16:12:33Z (`run.json` start_utc).
- `freeze_time.json` gives 16:06:01Z.

**Provenance on B300 (read-only)**
- The `run.json` and `train_log.jsonl` files for Fplus_{E,C}_s0 in /scratch/iitp4/fu_a/runs are byte-identical to the repo copies.
- The B300 code tree (src/topic2_fu_a/*.py, scripts/topic2fu_a_train.py) equals the repo.
- The `fua_code_sha256` and r1 `code_sha256` values in the run records match the pinned freeze receipts.
- `sacct -j 507`: b300-01, gres/gpu=1 per task, ElapsedRaw 1480 s and 1479 s, both COMPLETED.

**p01 — headline numbers recomputed from raw records**
- Σnum/Σden equals the recorded value exactly: E 0.7746782345624923, C 0.7704092658872178.
- Gain (E−C)/E = 0.005511, which is below δ = 0.01.
- E and C have identical denominators, so they were evaluated on the same windows.
- Per-group gain over the 16 groups: mean 0.551 %, sd 0.071 %, range 0.42–0.69 %. No group reaches 1 %.
- r1 gate recomputed: F+ gain C vs E is 2.77 % (seed 0) and 3.35 % (seed 1); the seed-mean NMSE gain is 3.06 %, which matches the report.

**p02 — fixture path used by the gate**
- The perm sha256 in each `run.json` equals the corresponding key in perms_fua_Fplus.npz.
- The labels equal the r1 labels and equal a regeneration with seed 31.
- σ_v, κ and κ_fix in the run records equal the frozen constants.
- My own formulas reproduce κ = 1/√Q = 5.699892 and σ_v = √(NF·n̄/(1−NF)) = 6.545925, with n̄ = 162.655 over 1,136 in-brain fixture cells.
- The actual training class `make_cell_fixture_source(...)` matches my numpy reimplementation to within 1.2e-6.
- The empirical voxel noise sd is 6.5447.
- Held-out within-box r of the training-stream cell series: E 0.073, C 0.335, S0 0.036, G 0.060. This matches the worker's Stage-0 numbers (0.071, 0.338, 0.059).
- C purity is 1.00 and E purity is 0.311.

**p05 — independent TRAIN design statistics on B300**
- CPU-only Slurm step 540, with my own code, aggregates only.
- Q = 0.03077986997, κ = 5.69989177, NF = 0.20850750, lag-1 median 0.2531 and mean 0.3133. All are identical to design_stats_train.json.
- Pad alignment: under the r1 pad, the cells with zero brain voxels have zero mean in 64/64 subjects. Under a shifted pad, all 64 subjects violate this.

**Verdict checks**
- p03: my own card-derived verdict (written from card §7.3/§8, with a scipy t interval) agrees with `decide()` on 20,000 randomized adversarial record sets. There were 0 disagreements. The outcomes covered were inconclusive 16,160, no_verdict 2,428, stop 849, modify 482 and keep 81.
- p03: both implementations give `inconclusive` on the shipped records.
- Rerunning `scripts/topic2fu_a_verdict.py` gives a verdict.json identical to the shipped one.

**Tests**
- FU-A suite: 69 passed, 1 skipped (the by-design Stage-1 scan).
- Old suite (STRICT_E2E): 86 passed.

**Independent mutation harness** (47 mutants different from the worker's M01–M31; `verification/challenger_FU_A_r1_2/mutation/results.json`)
- It runs the shipped tests but excludes `test_receipts_and_c4.py`, whose hash check would otherwise kill every src mutant trivially.
- Control passes. 35/47 mutants were killed.
- Every data-path mutant (target, sources, run, train CLI) was killed: T01–T06, S01–S07, R01–R04, P01.
- Survivors: X01, X02, X08, X09, X10, X18, X23, X24, C01, C02, C03, C04.
- p06: no verdict mutant changes the shipped verdict.

**p04 — C4 scan of all FU-A outputs, docs, code, tests and the worker's verification and metadata (96 files)**
- No HCP-shaped 6-digit IDs and no hex subject tokens. The only hits are synthetic test strings and float-exponent false positives.
- The 2 "sub-o…" hits are quotes of FU-B's word (not IDs).
- Nothing was printed.

## 2. Logic Chain

1. The card was frozen before the first gate run (receipt plus an external git timestamp), and no FU-A code changed after the freeze (receipts, and B300 copies identical). Therefore C3 and F1 hold.
2. The records come from the frozen code on a B300 GPU under Slurm. They are byte-identical on B300 and in the repo, and they carry the correct perms and constants (p02). The headline numbers recompute exactly from the raw num/den (p01). Therefore the gate numbers are genuine.
3. The gate trained on what the card specifies:
   - the noise level equals σ_v (p02);
   - the target is the cell-mean field (p02 reimplementation; spread check 0.0);
   - the C boxes align with the planted networks and are recoverable at Stage 0 in the training stream (p02).

   Therefore the small gain is not a wiring defect in the source, the partition or the cell ordering. Mutants T05 (cell order) and T02 (h/w swap) are caught by the tests, and S01 (r1 noise) is caught too.
4. The calibration inputs Q and NF are reproduced from the raw TRAIN data by independent code (p05). Therefore σ_v is not a computational error.
5. Card §8.3 step 2: F+ completed and the gain 0.0055 < 0.01, so the verdict is `inconclusive` whatever Stage 1 shows. My independent decider and `decide()` agree, here and on 20k adversarial cases (p03). Therefore the verdict follows the card.
6. The survivors are untested guards, not wrong verdicts:
   - X01 is equivalent: NaN > 0 is False, so NaN is still rejected.
   - X02 needs a negative NMSE, which is physically impossible.
   - X08, X09, X10 and X18 sit on the Stage-1 path, which was not reached.
   - X23 (F+ gate at any seed) and X24 (F+ passes when C-vs-S passes) are non-equivalent. Witness for X24: F+ C-vs-E gain 0.5 % with S worse gives no_verdict under the mutant against inconclusive in the original (p06). Neither applies to the shipped records, which have seed 0 only and no S run.
   - C01–C04 (the calib.py formulas for σ_v, NF and κ) have no hand-value test. The shipped values are nonetheless correct by independent recomputation (steps 4 and p02).

   Therefore none of the survivors is blocking.

## 3. Caveats

- **No GPU reproduction.** I did not rerun a gate run on GPU, so seed-0 determinism and seed variance are untested by me. The B300 gpu queue had many pending jobs from other teams. A seed-1 rerun is the worker's costed option A′1 and needs a PI decision.
- **The F+ noise share in the card and report is the pooled value, not the F+ value.**
  - Card §7.1 and report §3/§4/§5 say the realized fixture noise share is 0.248 with signal variance 0.80.
  - Those are the F+/F− pooled values. For F+, the only gate fixture run, the in-brain signal variance is about 0.93–0.94 and the realized noise share is about 0.219 (p02 measured 0.2194; noise term σ_v²·N/Σn = 0.2634).
  - F− is about 0.29 (signal variance 0.66).
  - Report §4's "Arm E captures ≈ 30 %" becomes ≈ 29 %.
  - This is descriptive only and changes no governed number. It slightly strengthens the "at realistic noise" reading, because F+ sits near NF 0.209 rather than above it. A dated erratum addendum is needed, since the card is frozen.
  - Because κ_fix is pooled, the F+ target mean square is about 1.13 rather than 1. This is NMSE-invariant, and the training loss of 0.874 against NMSE 0.775 is consistent with it.
- **The gate result depends on the calibration choice.**
  - The verdict depends on the pre-registered calibration that matches the cell-mean noise share (σ_v 6.55).
  - explorer_FU_A_r1_1/3 had proposed a voxel-R² calibration (σ ≈ 4.5–4.7, about half the noise variance).
  - Under that alternative the gate might pass. This is not tested, and it is a robustness limitation, not a defect. The worker's choice matches the quantity the FU-A target actually sees.
- **Single-seed gate.** The report's "a second seed is very unlikely to reach δ" is stronger than the evidence:
  - the within-run VAL gains swing between 1.14 %, 0.09 %, 0.41 % and 0.46 %;
  - r1's seed spread was about 0.6 pp.

  "Unlikely" is supportable; "very unlikely" is not demonstrated. This governs nothing.
- **Report §5.1 is an inference.** The statement that the r1 `stop` should be read as "capacity at real noise not established" is labelled an inference by the report itself. The integrated report should carry it as a scope caveat, not as a finding.

## 4. Conclusion

CONFIRMED. The FU-A card was frozen before results. The gate numbers are genuine and recompute exactly. The gate trained the specified noisy cell-mean F+ fixture with correctly aligned planted boxes. The verdict `inconclusive` (measurement capacity) follows card §8.3 step 2, and the r1 `stop` is untouched.

Nonblocking items for root or a later iteration:
- (a) Add tests for X23/X24 (F+ gate fixed to C-vs-E at seed 0), for C01–C04 (hand values for σ_v, NF and κ), and for the Stage-1 num/den, length and empty-order guards (X08–X10).
- (b) Write a dated erratum addendum: the F+ realized noise share is about 0.22 (0.248 is the F+/F− pool), and E captures ≈ 29 %.
- (c) Soften "very unlikely" in report §8.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in results/topic2/2026-11-02_fu_a/{card_sha256,code_sha256_at_freeze,output_sha256}.txt; do grep -v '^#' $f | LC_ALL=C sha256sum -c --quiet; done
git show 35d10a5:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md | sha256sum   # 72be3e83…
cd verification/challenger_FU_A_r1_2
python3 -I probes/p01_recompute_headline.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 probes/p02_fixture_path.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 probes/p03_differential_verdict.py
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 probes/p06_survivor_witnesses.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 mutation/run_mutants.py   # ~45 min under load; 35/47 killed
# B300 (CPU only): ./b3.sh 'srun -p debug -w b300-01 -c 2 --mem=16G -t 00:10:00 /scratch/iitp4/fu_a/env/venv/bin/python -B -' < probes/p05_b300_design_stats.py
```

**Invalidation conditions.** Any of the following would invalidate this conclusion:
- any receipt or C1 failure;
- a `run.json` that differs from the B300 original;
- a change to `verdict.py`, `sources.py` or `target.py` after 16:06:01Z;
- p02/p05 numbers that no longer match the frozen constants.
