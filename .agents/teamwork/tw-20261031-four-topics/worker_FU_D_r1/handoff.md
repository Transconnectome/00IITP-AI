# Handoff (Hard) — worker_FU_D_r1, milestone FU_D (Topic 2 follow-up D, SwiFT ver11 E192 scale)
Written 2026-11-01 ~19:25Z. No git writes. No installs on DGX-Spark. No participant IDs printed or written.

**Result.** The FU-D verdict under its frozen card is **`inconclusive` (measurement capacity)**. The F+ training-loop gate at E192 (E/C/S × seed 0, full budget, synthetic) gave (E−C)/E = **+0.363 %** and (S−C)/S = **+0.655 %**. Both are below δ = 1 %, so the card's step 2 applies and Stage 1 (HCP) was not run. The r1 E36 `stop` stands alone. Descriptively, the M0 grouping gain on the planted signal shrinks with scale: +2.77 % at E36 (r1, seed 0) against +0.36 % at E192. FU-D used 3.672 GPU-h in total: 3.575 by me plus 0.097 by the explorers. The cap was 25.

## 1. Observation

| id | observation | evidence |
|---|---|---|
| O1 | The card was frozen at 2026-11-01T16:06:07Z, before any FU-D job. Card sha256 is `1b7fee6c…001b`. The code freeze covers 29 files. | `results/topic2/2026-11-02_fu_d/card_sha256.txt`, `code_sha256_at_freeze.txt` (both rc 0) |
| O2 | Mutation harness, run before the freeze: run 1 killed 60/62 mutants, with R03 and R15 surviving. I added two tests, then run 2 killed 62/62. | `verification/worker_FU_D_r1/mutation/mutants_prefreeze.out.json`, `mutants_prefreeze_r2.out.json`, `run_mutants.py` |
| O3 | The venv `/scratch/iitp4/fu_d/venv` was installed from the r1 lock. Its freeze matches the lock exactly (identical=True; torch 2.15.0+cu134). | `results/topic2/2026-11-02_fu_d/logs/env_check.json` |
| O4 | Positional view: 88 subjects and 176 hard links, all on the same inodes. The manifest, original split and sanitized split sha256 match the pins. The mapped split equals the sanitized split in train, val and test, order included. | `logs/view_check.json` |
| O5 | Smoke, Slurm job 511 (0.040 GPU-h). The r1 `hcp_E_s0` test NMSE 0.9908706340280367 was reproduced exactly through the view, with per-subject num/den and test order equal. The E192 HCP cost probe ran at 0.4962 s/step, projecting 1.213 h per run. | `smoke/equiv.json`, `smoke/run.json`, `smoke/train_log.jsonl` |
| O6 | F+ gate, Slurm jobs 534/535/536 on b300-01. All three finished `completed` / Slurm COMPLETED with post-checks passing (cfg E192, 474,226,176 parameters, frozen r1 code). Cost was 1.175 / 1.180 / 1.180 GPU-h. Test NMSE: E 0.6558495, C 0.6534679, S 0.6577737. | `runs/Fplus_{E,C,S}_s0/{run.json,fud_meta.json,slurm.json,train_log.jsonl}`, `logs/slurm/`, ledger |
| O7 | The verdict script returned `inconclusive`, reason "measurement-capacity gate failed (F+ fixture at E192); Stage 1 not read", with needs_fminus false. The frozen r1 `stats.gate_fixture` on the same numbers gives the same gains and pass=False. | `verdict.json` |
| O8 | Every copy-back passed the B300 count-only C4 scan with 0 hits. The local scan covered 73 FU-D files with 0 token and 0 BIDS hits. | `logs/scan/*.json`, `logs/c4scan_local.json` |
| O9 | B300-share rule: before every submission (511, 534, 535, 536) squeue showed no `g3t-G-E0-*` job pending or running. Queue waits of 21–71 min were QOSMaxGRESPerUser (the 8-GPU user cap). | `progress.md`; the share check is built into `scripts/topic2fu_d_slurm.py submit` |

## 2. Logic Chain

1. The card (§7.1, §8 step 2) says that if F+ is computed and fails, the verdict is `inconclusive` and Stage 1 is not run (O1). O6 and O7 show F+ was computed from three completed runs, and both gains are below δ. So the verdict is `inconclusive`, and Stage 1, the seed plan and F− are not run. That is why `seed_plan.json` does not exist.
2. The gate is valid, not a software artefact:
   - all post-checks pass, and arms differ only in the pinned permutation (O6);
   - the E192 model structure is pinned by `tests/topic2_fu_d/test_e192_model.py`: M0 is the only box gather, Linear 1536→384, and the initial weights are bit-identical across arms;
   - the C < E < S ordering holds at every validation step, so the gather carries the planted structure in the right direction; only the effect size fails.
3. The r1 reading in card §9(c) is fixed in advance as "E192 adds no decision". The r1 stop is unchanged.

## 3. Caveats

- **One F+ seed** (pre-registered, for cost). At E36 the per-seed gains were +2.77 % and +3.35 %. A seeds-1–2 check would cost about 7.1 GPU-h (report §5) and is unlikely to change the decision.
- **Explanation not tested.** The suggestion that the wider M0 and the 18 stage-2 blocks recover the scattered networks after a compact merge is a plausible reading only.
- **Pre-existing receipt failures, not caused by me.** I checked every `results/**/*sha256*.txt`. The real failures are all outside my paths:
  - r1 topic2 `card_sha256.txt` / `output_sha256.txt` / `c4_sealed_originals_sha256.txt` lines superseded by the r2 C4 sanitization (documented in addendum 05);
  - `fu_b/card_sha256.txt` (FU-B's own; they have a v2);
  - `fu_e/checkpoint_sha256_pins.txt` and `topic3/2026-11-02_h2/logs/ship_manifest_sha256.txt` (relative or remote paths);
  - `topic3/2026-10-31/code_sha256_at_freeze.txt` for `scripts/topic3_launch_connectome.py` (mtime 10-31 17:51);
  - `topic4/2026-11-01/output_sha256.txt` for `logs/analyze.log` (mtime 11-01 11:15).

  The topic1 and topic3/topic4 card lines that "fail" are format artefacts of my generic loop (trailing text after the path). C1 itself is rc 0.
- **B300 state.** `/scratch/iitp4/fu_d/` is kept: the venv, the view (hard links into the r1 data, no extra bytes), and the 3 gate checkpoints (1.9 GB each) for verifiers. `/scratch` is node-local and may be wiped.
- The checker `scripts/topic2fu_d_slurm.py close` writes `slurm.json` into the B300 run dir before copy-back.

## 4. Conclusion

FU-D is complete under its card. The verdict is **inconclusive (measurement capacity at E192)**: no Stage 1, no F−, 3.672 / 25 GPU-h. Deliverables:
- card (frozen);
- code: `src/topic2_fu_d/` (8 files), `scripts/topic2fu_d_*.py` (9 files), `tests/topic2_fu_d/` (11 files, 129 tests);
- results in `results/topic2/2026-11-02_fu_d/` (receipts `card_sha256.txt`, `code_sha256_at_freeze.txt`, `output_sha256.txt`);
- result report `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_result_report.md` with costed options.

No addendum was needed: the execution followed the card, and there are no deviations. For root:
- 21.3 GPU-h of the FU-D cap is unused, and can be released to the run ceiling.
- Any further E192 work needs a new card and a PI decision (report §5).

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'      # 0
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done   # 0 0 0
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt | grep -c ': OK$'                         # 33
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q   # 129 passed (~1.5 min, ~4 GB RAM)
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q   # 86 passed
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic2fu_d_verdict.py --wrapper-sha256 $(grep topic2fu_d_train.py results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt | cut -d' ' -f1) --out /tmp/v.json   # inconclusive
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 scripts/topic2fu_d_c4scan.py                     # 0 hits
grep worker_FU_D_r1 results/gpu_ledger_2026-10-31.md                                                               # 4 started + 4 completed rows (511, 534-536)
# mutation: verification/worker_FU_D_r1/mutation/run_mutants.py REPO SCRATCH OUT.json -> 62/62 killed
# B300: ssh connectome@61.107.201.98 'sacct -X -j 511,534,535,536 -o JobID,State,ElapsedRaw,NodeList'
```

Invalidation conditions:
- any FU-D receipt fails;
- a gate run record fails `records.validate_completed`;
- the ledger shows FU-D GPU use not listed here.
