# Handoff (hard) — challenger_FU_A_r1_1, milestone FU_A, 2026-11-01T17:2xZ

**Verdict: CONFIRMED.** The FU-A deliverable holds under empirical attack. The shipped verdict `inconclusive` (measurement capacity) follows from the frozen card §8.3 step 2. The card was frozen before any FU-A result. The headline numbers recompute exactly from the raw records. No blocking defect was found. Three nonblocking issues are listed in §4: a factual error in the frozen card and the report (fixture noise share), an overstated sentence in the report, and five surviving verdict-code mutants that do not touch the shipped path.

Overall risk: LOW.

## 1. Observation

**Integrity and timeline**
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` gave rc 0, 67/67 OK (checked at the start and again at the end).
- FU-A receipts: `card_sha256.txt` 8/8, `code_sha256_at_freeze.txt` 21/21, `output_sha256.txt` 21/21 OK. r1 `code_sha256_at_freeze.txt` 33/33 OK.
- On B300 `/scratch/iitp4/fu_a/code`, the same FU-A receipts verify 21/21 and 8/8, so the code that ran is the frozen code.
- Independent freeze timestamp: host autocommit `35d10a5` at 2026-11-01T16:05:25Z holds the card with sha256 `72be3e83…18fb`. That is the same hash as the receipt, written before the first run started.
- sacct for job 507: tasks ran 16:12:31Z to 16:37:11Z / 16:37:10Z, ElapsedRaw 1480 s + 1479 s.
- `run.json` `fua_code_sha256` and `code_sha256` equal the frozen FU-A and r1 pins (19/19 per run).

**Raw outputs**
- The B300 originals of `runs/Fplus_{E,C}_s0/{run.json,train_log.jsonl}` are byte-identical to the repo copies (4/4 sha256).
- Recomputed Σtest_num/Σtest_den: E 0.7746782345624923, C 0.7704092658872178. Both equal the recorded `test_nmse`.
- `test_den` is identical across the two arms (paired evaluation).
- Gain (E−C)/E = 0.005510634589708632 < 0.01.
- C is lower than E in 16/16 evaluation groups; per-group gains range from 0.42 % to 0.69 % (`logs/probe_target.json`).

**Fixture partitions**
- `scripts/topic2fu_a_build_fixture_perms.py --sigma-v 6.545925453832064` rerun locally into `verification/challenger_FU_A_r1_1/rebuild/` (143 s).
- `perms_fua_Fplus.npz` sha `629a699b…` and `perms_fua_Fminus.npz` sha `2e96493b…` came out byte-identical. `fixture_build.json` differs only in `sec`. C purity 1.0.
- The F+ labels equal r1's `perms_Fplus.npz` labels.

**Constants** (independent numpy, `logs/probe_calib.json`)
- κ = 1/√Q = 5.699891773354029 and σ_v = √(NF·n̄/(1−NF)) = 6.545925453832064 (n̄ = 162.655, 1136 in-brain cells). Both match the frozen constants.

**Target code** (`logs/probe_target.json`)
- `target.cell_mean_field` / `block_mean_volume` against a loop-based numpy reference: max absolute error 2.6e-6 on adversarial masks (empty cell, single-voxel cell, densities 2–100 %).
- Outside the brain the field is exactly 0. Within-cell spread is 0.
- Voxel NMSE equals the n_c-weighted cell NMSE (difference 0.0). NMSE is invariant to κ (difference 0.0).
- `CellHCPSource.batch` on an HCP-format fake subject: relative error 8e-8.

**Verdict code**
- Independent oracle written from the card §8.3 text (`oracle_fuzz.py`, no import of verdict.py or stats.py inside the oracle), compared against `verdict.decide`.
- 60,000 random record sets (seeds 1 and 2): **0 disagreements**. Oracle categories: inconclusive 34,190; no_verdict 23,673; stop 1,403; modify 676; keep 58.

**Mutation testing**
- 22 new one-line mutants of verdict.py (X01–X22, disjoint from the worker's M01–M31), run against the shipped `tests/topic2_fu_a/test_verdict.py` in an isolated copy (`mutation/run_mutants_x.py`). The control passes; 17/22 are killed.
- Survivors: X05 (isfinite guard removed), X06 (F+ S-arm incomplete treated as not_run), X07 (num/den consistency rtol 1e-9 → 1e-2), X11 (stall-sensitivity recompute skips the step-5 bias gates), X16 (stall threshold 0.999 → 0.99).
- The oracle disagrees with these mutants on 10,000 cases (`logs/oracle_vs_mutants.txt`): X06 8, X07 296, X11 29, X16 25. So these four are not equivalent mutants. X05 differs only for +inf NMSE, which the fuzzer does not generate.
- The mutants that touch the shipped gate-fail path are all killed: X21 (F+ fail no longer short-circuits), X09 (gate seed), X18 (status), and the worker's M08.
- Note: the oracle column in `mutation/results.json` is void. It loaded the production module; v2 in `oracle_vs_mutants.py` loads each mutant by path.

**Fixture noise share** (`logs/probe_noise_share_by_kind.json`, through the frozen build path `fua_cells`, seeds 41/42)
- F+: Q = 1.1972, signal mean square 0.934, noise share **0.220**.
- F−: Q = 0.930, noise share 0.283.
- Pooled F+/F− gives Q_fix = 1.061 and noise share 0.248, which are the numbers in the card.
- The run's own log confirms this independently: train_loss_last100 / final VAL NMSE = 1.1282 (E) and 1.1278 (C). That equals κ_fix²·Q_F+ = 0.94253 × 1.1972 = 1.1284. If the F+ target were at the pooled Q, the ratio would be 1.000.

**Test suites and C4**
- `tests/topic2_fu_a`: 69 passed, 1 skipped (Stage-1 scan; by design).
- Old suite (`STRICT_E2E=1 tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed.
- `tests/topic2_rgpool/test_outputs_no_ids.py`: 3 passed now. The worker's reported FU-B-card failure no longer reproduces.
- The ledger has start and closing rows for job 507 (0.822 GPU-h) and for the explorer smokes 403 (199 s) and 427 (266 s). Total 0.952 GPU-h, which matches.
- C4: run records hold h-tokens only (Fixture runs hold none). The B300 data view is positional hNN symlinks; the h00 mtime 16:13:32Z is the post-freeze reproduction job 510.

## 2. Logic chain

1. The card is frozen before the results. The sha in the independent git autocommit at 16:05:25Z equals the receipt, the first run started at 16:12:31Z, and the code that ran equals the frozen receipts locally and on B300. So C3/F1 hold.
2. The gate result is genuine. The records are byte-identical to B300, internally consistent (num/den and the loss/VAL ratio), and paired on an identical evaluation set. The cell-mean path ran with noise: spread 0, and the loss ratio matches the noisy F+ Q.
3. The verdict follows the card. Step 2 (F+ completed and gain < δ) gives inconclusive. The code agrees with a text-derived oracle on 60k cases, and every mutant on that path is killed.
4. The surviving mutants (X05/X06/X07/X11/X16) live only in Stage-1 / keep / stall paths that were never reached. They cannot change the shipped verdict, so they are nonblocking test-adequacy gaps for any future Stage 1 under this card.
5. The noise-share misstatement goes in the "fixtures less noisy than stated" direction: 0.220 for F+, still above NF 0.209. The card's "conservative for F+" holds and the gate failure is, if anything, more robust. It is a factual error in descriptive text, not in a governed computation.

## 3. Caveats

- I did not rerun the GPU gate. At check time the B300 Slurm queue had 25+ pending GPU jobs (fuc/fub/fud/t3/gard/nhpfull), and no checkpoint was saved, so there was nothing to re-evaluate. Reproducibility of the record is established by byte identity with B300 and internal consistency, not by an independent rerun. 0 GPU-h used and no ledger row.
- TRAIN design statistics (Q, NF) were not recomputed from HCP data. I verified only the formulas, and that the B300 receipts and the frozen-script reproduction (job 510 log) agree.
- The fuzzer generates few keep cases (58 of 60k) and no ±inf/NaN NMSE.
- Single-seed gate: the r1 per-seed F+ gains were 2.765 % and 3.353 %, so the seed SD of the gain is ≈ 0.42 pp. FU-A's 0.551 % lies about 1.1 SD below δ.

## 4. Conclusion

CONFIRMED: FU-A verdict `inconclusive` (measurement capacity) under card 72be3e83, Stage 1 correctly not run, r1 `stop` unchanged. No blocking issues.

Nonblocking, recommended for a dated addendum or erratum (the frozen card must not be edited):

- **N1.** The card §7.1 and report §3/§4/§5.1 say the realized fixture noise share is 0.248 and the signal variance 0.80. For the F+ gate the values are 0.220 and 0.934; 0.248/0.80 are the pooled F+/F− values. Report §4's "≈ 30 % of predictable energy" becomes ≈ 28.9 %.
- **N2.** Report §8 says "a second seed is very unlikely to reach δ". This is not supported: with seed SD ≈ 0.42 pp (from 2 r1 seeds), P ≈ 0.14 under a normal model, and higher with df 1. Reword it. Option A′1 is informative for exactly this reason.
- **N3.** Five verdict.py mutants survive the shipped tests (X05, X06, X07, X11, X16). Add tests before any Stage 1 runs under this card:
  - +inf `test_nmse`;
  - Fplus S started-not-completed with a keep-like Stage 1 → no_verdict;
  - num/den inconsistency of about 1e-6 relative;
  - stall sensitivity where the bias gates change the recomputed category;
  - a stall threshold test at 0.995.
  The card line "Boundaries … stall at ≥ 0.999 pinned by tests" is only half-pinned: X16 survives.
- **N4.** The worker's open issue (rgpool `test_outputs_no_ids` failing on the FU-B card) no longer reproduces: 3 passed.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
git show 35d10a5:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md | sha256sum   # 72be3e83…
P=/home/juke/superclaude-env/bin/python3; export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2
cd verification/challenger_FU_A_r1_1
$P -B oracle_fuzz.py 20000 1 /tmp/x.json                    # 0 disagreements
$P -B probe_noise_share_by_kind.py                         # Fplus noise_share 0.220
$P -B probe_target.py                                      # max err ~2.6e-6; 16/16 groups
$P -B mutation/run_mutants_x.py                            # 17/22 killed; survivors X05 X06 X07 X11 X16
cd mutation && $P -B oracle_vs_mutants.py 10000            # survivors disagree with oracle
```

Invalidation: any change to the card sha, a run record or verdict.py; a GPU rerun of Fplus_C_s0 / Fplus_E_s0 that gives a gain ≥ 1 % would not change the verdict (the rule is frozen on these records), but it would bear on N2.
