# Handoff (Hard) — reviewer_FU_D_r1_2, milestone FU_D (Topic 2 follow-up D, SwiFT ver11 E192)

**Verdict: APPROVE.**
- No blocking issue. No integrity violation found.
- 4 minor, nonblocking findings.
- No git writes, no installs, no IDs printed, no GPU used by me.

## 1. Observation

| id | what I ran / read | result |
|---|---|---|
| O1 | `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` (start and end) | 67 lines, 0 non-OK, rc 0 |
| O2 | `grep -v '^#' results/topic2/2026-11-02_fu_d/{card,code_sha256_at_freeze,output}_sha256.txt \| sha256sum -c`; `sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt` | 1/1, 29/29, 34/34 OK; r1 33/33 OK |
| O3 | `pytest tests/topic2_fu_d -q` (STRICT_E2E=1) | 129 passed, rc 0 (`verification/reviewer_FU_D_r1_2/pytest_fud.out`) |
| O4 | `pytest tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q` | 86 passed, rc 0 (`pytest_old.out`) |
| O5 | recomputed the gate from per-subject `test_num`/`test_den` (`recompute.py`) | pooled NMSE equals the stored values exactly: E 0.6558495, C 0.6534679, S 0.6577737; (E−C)/E 0.0036313, (S−C)/S 0.0065460; fails δ = 0.01. C < E and C < S on 16/16 groups. C < E < S at every validation step. |
| O6 | r1 E36 F+ seed 0/1 (`results/topic2/2026-11-01/runs/Fplus_*`) | seed 0: I1 +2.772 %, I2 +2.900 %; seed 1: I1 +3.348 %, I2 +2.970 %. The perm sha256, perm file and eval denominators are identical to FU-D. |
| O7 | `scripts/topic2fu_d_verdict.py` rerun → `verification/reviewer_FU_D_r1_2/verdict_rerun.json` | identical dict to the shipped `verdict.json`: `inconclusive`, "measurement-capacity gate failed (F+ fixture at E192); Stage 1 not read" |
| O8 | B300 `sacct -X -S 2026-11-01` | FU-D GPU jobs: 396, 404, 418 (FAILED, 1 s), 430, 511, 534, 535, 536. All are in the ledger; jobs 393–395 and 415 are CPU-only. No FU-D job is pending or running. ElapsedRaw 4230/4248/4246 matches `slurm.json` and the ledger. |
| O9 | sha256 of B300 `/scratch/iitp4/fu_d/runs/*/{run.json,train_log.jsonl,fud_meta.json,slurm.json}` against the repo copies | 12/12 identical. The three `model_final.pt` (1,898,355,817 B each) are kept. |
| O10 | `fud_meta.json` for the 3 gate runs and the smoke | wrapper sha `d598989b…` and all 8 `src/topic2_fu_d` hashes equal the freeze receipt. The frozen train script `05f08f7c…` equals the r1 freeze. post_checks all true. argv carries val/test mask seeds 7001/7002. |
| O11 | freeze timing | card mtime 15:40:57Z; receipts 16:06:07Z; git autosnapshot `34f4b30` (2026-11-01T15:50:24Z) contains the card with sha 1b7fee6c…; view 16:11:26Z; first post-freeze GPU job submitted 16:13:50Z. The venv (15:28Z, data-free) and explorer smokes (synthetic) predate the freeze; both are disclosed in card §0. |
| O12 | B300-share rule | B300 sacct since 2026-11-01 contains no job named `g3t-G-E0-*` at all, so no FU-D submission (01:13:50 / 01:39:57–01:41:11 KST) coincided with one |
| O13 | ledger sum | FU-D closing rows = 3.672 GPU-h exactly (explorers 0.097 + worker 3.575); ≤ cap 25 |
| O14 | C4 | `scripts/topic2fu_d_c4scan.py`: 76 files, 0 token, 0 BIDS hits. My count-only scan (`c4count.py`) of the FU-D outputs, code, worker metadata and verification: 0 six-digit, 0 `sub-` hits. |
| O15 | own mutant set A01–A19 (`verification/reviewer_FU_D_r1_2/mutation/run_mutants_rev.py`, disjoint from the worker's 62) | 18/19 killed. **A04 `DELTA = 0.01 → 0.003` in config.py SURVIVES** (124 passed). With δ 0.003 the shipped gate would pass, and the verdict would become `no_verdict` (seed plan missing). |
| O16 | `audit_layout.py` on the whole run metadata root | PASS, 514 files, 0 findings |
| O17 | report numbers | all match the files: −3.1 %/−0.7 % cube/box change, 0.4962 s/step, 1.213 h, val table, 4×32 / 16×32 windows, 42 % (r1 report line 110), option costs 14+72 = 86 |

## 2. Logic Chain

1. **C1–C2.** O1, O2, O3 and O4 pass.
2. **C3 / F1.** The card names:
   - the single change (scale), the arms (byte-identical r1 partitions), the seeds and the budget (8,750 × 16);
   - the metric, δ = 1 %, the stop rule, the gates and the verdict table.

   It reuses the r1 machinery (frozen `stats.t_interval`/`relative_gain`/`verdict`, asserted on every call). O11 shows it was frozen before any FU-D real-data number. The only post-freeze HCP touches were the pre-registered §10.1 smoke (an r1 checkpoint re-score and a 200-step cost probe with no evaluation).
3. **F2.**
   - The code lives only in FU-D paths, and the frozen r1 code is unchanged (O2, O10).
   - The verdict path is tested: the worker's 62 mutants are killed, including analogues of all V01–V11 classes (missing gate ≠ pass, F− only for keep, failed runs not counted, order guard, F+ fail → inconclusive). My 19 independent mutants show 18 killed (O15).
   - The surviving A04 cannot have affected the shipped verdict: config.py is pinned in the verified freeze receipt (O2), and verdict.json records `delta: 0.01`.
4. **F3.**
   - Runs went through Slurm on b300-01 only (O8), within the cap (O13), with started and completed ledger rows.
   - Run records are byte-identical to B300 (O9), and results are in the dated dir.
   - The result report gives the card verdict, what it adds to r1 (no decision; descriptive shrinkage of the planted-signal gain, 2.77 % → 0.36 %), and costed options (§5).
5. **Verdict correctness.**
   - O5 reproduces the gate independently from the per-subject terms.
   - Card §7.1 / §8 step 2 says that an F+ gate that is computed and fails gives `inconclusive`, with Stage 1 not run. O7 shows the script does exactly this, and no hcp_* records exist.
   - The outcome is an "untestable within this setting" escape. It is evidenced (gate records, sacct, checkpoints kept) and costed (report §5). This meets the dispatch's approval condition.
6. **C4–C7.** C4: O14, and no git writes by the worker were observed. C5: O8, O12, O13. C6: HCP-YA OA counts as public under PI decision 2; data stayed on b300-01. C7: no external repo was touched. C8: the report cites only dated FU-D and r1 outputs.

## 3. Caveats

- **No GPU re-evaluation of the checkpoints by me.** At 19:29Z three other FU-D verifier re-evals (`aud-fud-reeval`, `chfud-reeval`, `chFUD2-reeval`) were pending under QOSMaxGRESPerUser, and the 8-GPU user QoS was saturated (FU-B 4, FU-C 3, other 1). A fourth duplicate would only add queue pressure. My anti-fabrication evidence is instead:
  - B300 records byte-identical to the repo copies;
  - sacct durations consistent with 8,750 steps at about 0.48 s/step;
  - the code hashes in the sidecars;
  - the smoke equivalence check;
  - 1.9 GB checkpoints present.
- **Minor findings (nonblocking).**
  - (a) A04: no test pins `config.DELTA == 0.01`. The tests pass δ explicitly. It is guarded only by the freeze receipt.
  - (b) `records.validate_completed` does not check the eval mask seeds. They are not in run.json; the sidecar argv has them, and the identical denominators across arms and r1 show the same eval masks were used.
  - (c) Card §7.1 quotes the E36 margins "+3.06 % / +2.93 %". These are the 2-seed means of I1 and I2, not per-seed values. The wording is ambiguous but the numbers are correct.
  - (d) The report's run-ledger total of 30.665 GPU-h depends on the cut-off: my sum of rows ending ≤ 19:03:29Z is 29.33, and the total now is 32.39. Either way it is far below 95.
- One F+ seed only. This was pre-registered for cost, and the report states it.
- `/scratch/iitp4/fu_d` (3 × 1.9 GB) remains on b300-01. Root should clean it up after all audits.

## 4. Conclusion

**APPROVE.** FU-D meets C1–C8 and F1–F3. The verdict `inconclusive` (measurement capacity at E192, F+ gate +0.36 % / +0.65 % < δ 1 %) is reproduced independently and follows the frozen card. The r1 E36 `stop` stands alone. The FU-D cost is 3.672 of 25 GPU-h. The minor items (a)–(d) need no rerun; (a) could be closed with a one-line test in any later FU-D iteration.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # 0
for f in card_sha256.txt code_sha256_at_freeze.txt output_sha256.txt; do grep -v '^#' results/topic2/2026-11-02_fu_d/$f | LC_ALL=C sha256sum -c | grep -vc ': OK$'; done   # 0 0 0
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_d -q   # 129 passed
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_FU_D_r1_2/recompute.py   # gains 0.00363 / 0.00655, pass False
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_FU_D_r1_2/mutation/run_mutants_rev.py $PWD verification/reviewer_FU_D_r1_2/mutation/scratch /tmp/m.json   # 18/19, A04 survives
git show 34f4b30:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md | sha256sum   # 1b7fee6c…
```

Invalidation conditions:
- any FU-D receipt fails;
- a checkpoint re-evaluation by another verifier differs from the run.json test NMSE;
- a FU-D GPU job appears in B300 sacct without a ledger row.
