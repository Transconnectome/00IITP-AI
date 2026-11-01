# Handoff: worker_FU_E_r1 (FU-E, Topic 2 follow-up E). Type: Hard (task complete)

Parent: root coordinator, session 5fddb83e (workflow C). Host: claude-code subagent. No nested agents were spawned.

## 1. Observation

**B300 state and checkpoints** (2026-11-01, counts only, read over ssh to connectome@61.107.201.98 = b300-01)
- All 15 r1 checkpoints exist at `/scratch/iitp4/worker_M3_r1/runs/hcp_{E,C,S}_s{0..4}/model_final.pt`, 156,184,449 B each.
- Their sha256 values, recomputed at 15:36:36Z, equal explorer_FU_E_r1_1's Slurm-407 values for all 15.
- Pins: `results/topic2/2026-11-02_fu_e/checkpoint_sha256_pins.txt`.
- The B300 `perms_hcp.npz` equals the repo copy (sha256 ec05b796…). The original split.json is c13b5f21… (64/8/16).
- **The "checkpoints lost" branch does not apply.**

**Code written (new paths only; r1 code imported, not edited)**
- `src/topic2_fu_e/`, 8 files: `prep` (halves 0–579 / 620–1199, per-half z, common mask, surrogate), `readout` (cov2, pooled, cellfc), `ident` (similarity, Idiff, null, accuracy, jackknife), `synth` (F+ / F− fixtures on top of r1 fixtures), `provenance` (G0), `pipeline` (subject-outer loop, one rerun on non-finite), `verdict` (gates, contrasts, classify, evaluate).
- `scripts/topic2fu_e_extract.py` (B300 job, plus a `--smoke` synthetic-only mode) and `scripts/topic2fu_e_verdict.py`.
- `tests/topic2_fu_e/`, 7 files, 71 tests.

**Card**
- `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_card.md`, frozen 2026-11-01T16:22:56Z.
- Receipt `results/topic2/2026-11-02_fu_e/card_sha256.txt`: card 072553b0912a86ee786e82f13d9fdc873a6681c9ba6feb5ffc5d8e0ddc36b88f, plus the pins, the code receipt (18 files) and the smoke sbatch.
- The first real-data job started at 17:03:57Z, after the freeze.

**Slurm jobs** (sacct, times converted from KST)
- 499 smoke: debug partition, synthetic only, COMPLETED, 8 s, 0.003 GPU-h.
- 524 main: gpu partition, -w b300-01, 1 GPU, COMPLETED 0:0, ElapsedRaw 1003 s, 0.279 GPU-h. Submitted 16:24:31Z; ran 17:03:57–17:20:40Z.
- Ledger: a started and a completed row for each job.
- **FU-E total 0.297 GPU-h**, including the explorers' 0.015 (cap 1.5).

**Run log** `results/topic2/2026-11-02_fu_e/run_524/extract_log.jsonl`
- rescored ok ×15;
- fixtures done with `failed: []`;
- heldout_done at 569.6 s;
- train64_done with `stopped_at: null`.

**Verdict** `results/topic2/2026-11-02_fu_e/verdict.json`, from the frozen script and reproduced byte-identically
- **`inconclusive`: "measurement-capacity gate failed (synthetic F+)"**.
- F+ failed only on S_s2: Idiff 5.761 ≤ null p95 10.586. The 14 others were above their nulls; seed means E 16.0, C 22.7, S 16.5.
- F− pass, G2 pass (seed-mean Idiff_E 61.07), G3 pass (cell-FC 64.1 vs p95 5.9), G0 pass (rescore max relative difference 0.0 on 16 positions × 15 checkpoints).
- Non-governed contrasts: J1 mean +0.081, t95 [−0.066, +0.228]; J2 mean +0.150, [+0.098, +0.202].

**Tests and checks** (final run, see §5)
- tests/topic2_fu_e: 71 passed.
- Old 86: 86 passed.
- tests/topic2_rgpool: 116 passed on the final run (with `CUDA_VISIBLE_DEVICES=`). Two earlier failures were not caused by FU-E. `test_outputs_no_ids` had flagged a BIDS-label-like token in the FU-B team's card `docs/.../2026-11-02_topic2_fu_b_card.md`; it passed on the final run. `test_training_loop_cpu_smoke` had hit a CUDA OOM on the shared local GPU; it passes on CPU.
- C1: 0 non-OK. r1 code freeze: 0 non-OK.
- Verdict mutants: 29/29 killed (`verification/worker_FU_E_r1/mutants/mutants_v2.json`).
- B300 ID scan (r1 `scripts/topic2_id_scan.py`, 1084 names held in memory): 0 hits. The scan results are listed in §5.

## 2. Logic chain

1. The checkpoints exist and are verified (O1), so the option is testable without retraining. Retraining would have cost about 6.5 GPU-h against the 1.5 cap.
2. REST2 and RL runs are not staged, so cross-session fingerprinting cannot be done. The card defines within-run split-half identifiability and names it as such.
3. Explorer probes showed two artefacts:
   - the full-run z-score creates anti-correlated half-means;
   - subject masks identify subjects.

   The pipeline therefore re-z-scores each half and applies the common AND mask. My tiny-model probe and the G6 tests confirm both controls: F− under the common mask is at chance, and the subject-mask mutant gives spurious identity (Idiff about 48).
4. The age/sex labels cover 28 staged subjects, at most 7 of them held out. The probe is declared untestable and not run (card §10).
5. The card froze δ, the gates, the verdict order and the code before job 524.
6. The frozen rule says F+ needs every (arm, seed) above its null. S_s2, the stalled r1 run, failed. Card step 3 then gives inconclusive, and the code agrees.
7. Even ignoring F+, J1's interval straddles 0 and δ (between-seed SD 0.118 ≫ 0.008). That would also be inconclusive, so the outcome does not hinge on a single gate slot. This reading is descriptive only.

## 3. Caveats

**Deviations**
- **Smoke 499 C5 share-rule gap.** The g3t-G-E0 squeue check in its command chain failed on an ssh broken pipe, and the chain still submitted. sacct later showed no g3t-G-E0 job, so there was no conflict. Job 524 used an idempotent remote check-and-submit.
- **DISPATCH.md** does not copy the explorer JSON verbatim; it points to the handoffs.
- **The F− rule was changed before freezing**, after a synthetic tiny-model probe (card §0).
- **The main sbatch** `verification/worker_FU_E_r1/b300/fue_main.sbatch` was written after the freeze. Its sha256 is in output_sha256.txt. It only invokes the frozen script, and the job verified the frozen src/scripts hashes on B300 (slurm-524.out shows OK ×10).

**Limits of the result**
- The extraction reused the r1 venv `/scratch/iitp4/worker_M3_r1/venv` read-only. No new env was built.
- Within-run halves are not test–retest. The encoders barely learned their pretext task, and a zero mask is a distribution shift from SimMIM training.
- Random-init twins already reach 100 % identification. The meaning of encoder identifiability is therefore limited.
- **B300 copies remain** at `/scratch/iitp4/fu_e/` (code, smoke, main, idscan copies). They are volatile, and the aggregates are in the repo.
- The earlier r1-suite hit on the FU-B card belonged to the FU-B team; FU-E did not touch it.

## 4. Conclusion

**FU-E is complete under its frozen card. Verdict: `inconclusive` (measurement capacity, synthetic F+ failed on the stalled S_s2 encoder).**
- The r1 `stop` verdict is unchanged.
- The downstream identifiability question stays open.
- Descriptively, J1 (C vs E) is undetermined, [−6.6 %, +22.8 %], while C beats S, J2 [+9.8 %, +20.2 %].
- Any further work needs a new card. Possible changes: drop or handle the stalled run a priori, use more seeds (FU-C checkpoints, if saved), or use real test–retest sessions.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'   # 0
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-02_fu_e/output_sha256.txt | LC_ALL=C sha256sum -c
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 scripts/topic2fu_e_verdict.py results/topic2/2026-11-02_fu_e/run_524/extract.json /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-02_fu_e/verdict.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
/home/juke/superclaude-env/bin/python3 verification/worker_FU_E_r1/mutants/run_mutants.py /tmp/m.json   # 29 KILLED
```

**Invalidation conditions**
- Any change to a pinned file.
- Any checkpoint sha mismatch on B300.
- Any ID-scan hit.
