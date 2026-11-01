# Handoff: auditor_FU_E_r1_1 (forensic integrity audit, milestone FU_E). Type: Hard

## Forensic Audit Report

**Work product**: FU-E by worker_FU_E_r1. Covers src/topic2_fu_e/, tests/topic2_fu_e/, scripts/topic2fu_e_{extract,verdict}.py, results/topic2/2026-11-02_fu_e/, the docs card and result report, the ledger rows, and B300 /scratch/iitp4/fu_e/.
**Profile**: General Project. The integrity mode is Development, inferred because ORIGINAL_REQUEST has no from-scratch or no-delegation constraint. C1–C8 and the addenda apply.
**Verdict**: **CLEAN**

### Phase results
- C1 protected hashes: PASS. 67 lines, rc 0.
- FU-E receipts: PASS. card_sha256 4/4, code_sha256_at_freeze 18/18 and output_sha256 12/12 OK.
- r1 receipts:
  - PASS: code freeze 0 non-OK; output_sha256_r2, c4_sanitized and addendum_06 all 0 non-OK.
  - Pre-existing failures, not FU-E: r1 card_sha256 fails 2 lines (hcp_manifest.json and split.json, superseded by c4_sanitized), and the old output_sha256 and c4_sealed_originals fail too. They predate FU-E and were already disclosed by explorer_FU_E_r1_2 O8.
- Card frozen before results: PASS.
  - The receipt says the freeze was at 16:22:56Z.
  - The third-party autocommit cd1e43e (16:35Z) holds bytes with sha 072553b0…, identical to the frozen card.
  - Draft 35d10a5 (16:05Z) differs only by the 2-line smoke-499 disclosure.
  - Job 524 was submitted at 16:24:31Z and started at 17:03:57Z (sacct).
  - Explorer real-data reads before the freeze reproduced r1 numbers only (job 420, 2 TEST positions). They are disclosed in card §0.
- Hardcoded results / facades: PASS.
  - verdict.py, ident.py, readout.py, prep.py, pipeline.py, provenance.py and synth.py compute every value from inputs.
  - No literal result values were found. The only constants are card constants: δ, the floors, the seeds and the rtol.
- Output authenticity: PASS.
  - B300 /scratch/iitp4/fu_e/main/{extract.json, extract_log.jsonl, slurm-524.out} have the same sha256 as the repo copies. The extract.json mtime (02:20:39 KST) falls inside job 524 (02:03:57–02:20:40 KST).
  - **Independent CPU recomputation on B300** (my Slurm job 556, CPU only, frozen code, no encoder) recomputed the real held-out raw cell-FC similarity matrices. Compared with the shipped extract.json, the max abs diff was 4.5e-9 (main), 1.4e-9 (surrogate) and 3.6e-9 (subjmask). Idiff, accuracy, n_features (502,503) and the common mask (190,382 voxels, 1,003 cells) are all equal.
- Verdict reproduction: PASS.
  - The frozen verdict script, rerun locally, wrote verdict.json and its stdout byte-identically.
  - My own reimplementation (probes/reimpl_verdict.py, which does not import src/topic2_fu_e) gives 0 mismatches on every Idiff, accuracy and J1/J2 interval.
  - With 3 independent null seeds, F+ fails only on S_s2 (p95 11.1–12.3 vs Idiff 5.76). With the card seed 20261102 the p95 is 10.586, as reported.
  - The verdict is inconclusive. It stays inconclusive even if every gate is forced to pass, because J1 [−0.066, +0.228] straddles 0 and δ.
- Result report numbers: PASS. Every table value was recomputed from verdict.json and matches.
- Tests can fail: PASS.
  - tests/topic2_fu_e: 71 passed.
  - I ran 20 independent mutants of my own (not the worker's set) over ident, prep, readout, pipeline, provenance, synth and verdict: 16 KILLED, 4 survived.
  - 3 of the 4 survivors are equivalent:
    - A03: a row+column permutation has the same null distribution.
    - A05: a no-op mutant I wrote.
    - A20: the cell-mean scale is invariant under Pearson.
  - 1 is a real but nonblocking gap: A04, null quantile 0.95 → 0.90, is untested. The shipped verdict is unchanged under it (S_s2 p90 = 8.43 > 5.76, so it still fails).
- Old suite: PASS, 86 passed (STRICT_E2E).
- Participant-ID leakage: PASS.
  - Every subject label is positional (test:k / val:k / train:k / synth:k).
  - My local scan of 83 FU-E and explorer files found no BIDS sub- labels and no ID paths. The only 16-hex token with letters is a sha256 prefix of a CSV in an explorer handoff.
  - All 6-digit tokens in the outputs are counts (n_features, n_vox). I checked them against the 1,084 B300 HCP names, held in memory on B300: 0 hits.
  - No per-subject hashes are present. The file hashes are of checkpoints, perms and the split file, so they are not reversible to IDs.
  - The worker's B300 ID scan record has the same sha as B300 idscan_result_final.json, and sacct confirms job 551.
- GPU via Slurm, ledgered, within cap: PASS.
  - sacct shows that every FU-E GPU job ran under Slurm on b300-01: 407, 412 and 420 (explorers), 499 and 524 (worker). 549 and 551 were CPU-only.
  - The ledger has started and completed rows for each GPU job. The total is 0.005+0.003+0.007+0.003+0.279 = 0.297 of 1.5 GPU-h.
  - When 499 started, 3 GPU jobs were running for the user, below the 8-GPU share limit.
- Env: PASS.
  - The worker used the r1 venv of the same project (/scratch/iitp4/worker_M3_r1/venv) read-only. It has 0 files newer than 2026-11-02 00:00 KST, and its newest site-packages entry is from 2026-11-01 17:04 KST, before FU-E.
  - There were no installs on DGX-Spark.
- Git writes by agents: PASS. Since 15:00Z, all commits are from "Chavis Autocommit" or root checkpoints. The reflog contains only commits; there is no stash and no checkout.
- Writes outside ownership / protected paths: PASS. No FU-E file is outside the owned paths, and the r1 src/results receipts are intact.
- Layout lint (whole run root): PASS. 485 files, findings [], rc 0.

## 1. Observation
- Commands and raw outputs are in /home/juke/git/00IITP-AI/verification/auditor_FU_E_r1_1/:
  - probes/: reimpl_verdict.{py,out}, verdict_rerun.json (cmp-identical), pytest_fu_e.out (71 passed), pytest_old86.out (86 passed), aud_mutants.{py,json,log}, audit_layout.out, six_tokens.txt (counts only; 0 hits against the HCP names);
  - b300/: cpu_repro_probe.py, cpu_repro.sbatch, cpu_repro_out.json, slurm-556.out, sacct_556.txt, code_check.txt (24 frozen files, 24/24 OK on the B300 copy).
- sacct (KST):
  - 499 debug gres/gpu=1, 01:04:04–01:04:12, 8 s;
  - 524 gpu gres/gpu=1, submitted 01:24:31, ran 02:03:57–02:20:40, 1003 s;
  - 549 and 551: debug, CPU only, 2 s;
  - g3t-G-E0 jobs since 2026-11-01 20:00 KST: 0.
- extract_log.jsonl has 33 timestamped events, each stage in order (G0 → F+ → F− → 24 held-out → TRAIN-64). Their timings are consistent with the sacct window.

## 2. Logic chain
1. The frozen bytes predate job 524 by an external clock (the autocommit), and the code receipts hold on both the repo and the B300 copies. So the governed analysis used pre-registered code and rules.
2. The shipped record is byte-identical on B300 and in the repo, and it was written inside the Slurm job's window. Its real-data cell-FC matrices were independently recomputed to within 5e-9. So the record is not fabricated.
3. The verdict follows from the record by the frozen script (byte-identical) and by my independent reimplementation. The F+ failure is robust to the null seed. So the verdict is not hardcoded.
4. Of my 17 non-equivalent mutants the tests kill 16; the survivor, A04, is a test gap with no effect on the verdict. So the tests can fail.
5. No ID-shaped content is present, all GPU use was via Slurm and ledgered within cap, no installs were made, and there were no agent git writes. So C1–C8 hold.

## 3. Caveats
- **No GPU re-run of the encoder paths.** The user-wide normal QoS was at 8/8 GPUs with 37 jobs pending. The debug QoS has no per-user cap, so a debug job would have exceeded the C5 "≤8 concurrent GPUs" share rule.
  - b300/repro_probe.py and repro.sbatch were therefore written but **not submitted**.
  - The encoder-derived matrices (cov2/pooled), the G0 rescore exactness and the F+ S_s2 value are verified only by their internal consistency, the B300 hashes and the Slurm timing. They were not recomputed.
- I re-hashed the checkpoints on B300 (15/15 = pins) but did not reload them.
- **Nonblocking process notes** (none is an integrity violation):
  - (a) Smoke 499 was submitted while its g3t-G-E0 check had failed (an ssh broken pipe). This is self-disclosed, and no g3t-G-E0 job ever existed.
  - (b) The ledger's started row for 499 says submit 15:56:21Z, "queued 8 min". sacct shows Submit = Start = 16:04:04Z, so the 8 minutes were ssh retries, not queueing. This is a record inaccuracy.
  - (c) The worker's return says the CPU-only srun 551 is "in place" alongside the ledger rows. There is no ledger row for 549 or 551, but they are CPU-only, so none is needed.
  - (d) The worker's progress shows "72 passed" at 15:45Z, while the frozen tests give 71. The test files' mtimes predate 15:45Z, and the cause is not determined.
  - (e) src/topic2_fu_e/__pycache__ (2 .pyc, 16:20Z) exists locally despite PYTHONDONTWRITEBYTECODE. This is hygiene only.
  - (f) Mutant A04 (null quantile) survives.
- Explorer_FU_E_r1_2 sent HCP IDs from a local open-access CSV over ssh stdin for an in-memory overlap count. This was out of the worker's scope and nothing was written. It is noted only.
- My DISPATCH.md abbreviates the worker JSON blob; it points to the worker handoff instead.

## 4. Conclusion
**CLEAN.**
- FU-E's shipped verdict, `inconclusive` (measurement capacity, synthetic F+ failed on hcp_S_s2), is authentic, reproducible from the record, and governed by a card frozen before any real-data FU-E statistic.
- No hardcoding, facade, fabricated log, ID leakage, out-of-Slurm GPU use, cap breach, foreign env or agent git write was found.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt | grep -vc ': OK$'      # 0
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c; LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt
git show cd1e43e:docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_card.md | sha256sum      # 072553b0…
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/auditor_FU_E_r1_1/probes/reimpl_verdict.py results/topic2/2026-11-02_fu_e/run_524/extract.json results/topic2/2026-11-02_fu_e/verdict.json   # n_mismatch 0
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 scripts/topic2fu_e_verdict.py results/topic2/2026-11-02_fu_e/run_524/extract.json /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-02_fu_e/verdict.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q   # 71 passed
```
- B300 (CPU only, via sbatch): verification/auditor_FU_E_r1_1/b300/cpu_repro.sbatch, with the frozen code copy at /scratch/iitp4/auditor_FU_E_r1_1/code. That copy has been removed; recreate it from /scratch/iitp4/fu_e/code and check it with code_check.txt.
- Invalidation: any receipt mismatch; a B300 extract.json sha different from 1921b044…; a cell-FC recomputation diff > 1e-6; any ID-scan hit.
