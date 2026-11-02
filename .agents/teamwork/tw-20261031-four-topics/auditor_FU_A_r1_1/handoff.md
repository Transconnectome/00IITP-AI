# Handoff (hard) — auditor_FU_A_r1_1, milestone FU_A — 2026-11-01T17:05Z

## Forensic Audit Report
**Work Product**: FU-A (Topic 2 follow-up A, worker_FU_A_r1): src/topic2_fu_a, tests/topic2_fu_a, scripts/topic2fu_a_*.py, results/topic2/2026-11-02_fu_a, docs 2026-11-02_topic2_fu_a_{card,result_report}.md, ledger rows, B300 /scratch/iitp4/fu_a
**Profile**: General Project. Integrity mode: Development (ORIGINAL_REQUEST has no from-scratch / no-delegation constraint). C1–C8 + addenda applied in full.
**Verdict**: CLEAN

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0, 67/67 OK (start and end: verification/auditor_FU_A_r1_1/c1.txt, c1_final.txt).
- FU-A receipts: card_sha256.txt 8/8, code_sha256_at_freeze.txt 21/21, output_sha256.txt 21/21 OK. r1 receipts code_sha256_at_freeze, output_sha256_r2, c4_sanitized_sha256, addendum_06_sha256: 0 failures.
- Freeze order: the host autocommit 35d10a5 (2026-11-01T16:05:25Z) contains the card with sha 72be3e83…18fb; freeze_time 16:06:01Z; sacct job 507 start 16:12:31Z (01:12:31 KST). All src/tests/scripts mtimes ≤ 16:04Z. Run records embed fua_card_sha256 = 72be3e83…, fua_code_sha256 equal to the current (= frozen) FU-A files, r1 code_sha256 equal to all 13 r1 pins, perm_file_sha256 629a699b… = pinned perms_fua_Fplus.npz.
- Run records: Σtest_num/Σtest_den = test_nmse exactly (E 0.7746782345624923, C 0.7704092658872178); identical test_den between arms; gain (E−C)/E = 0.005510634589708632 < 0.01. train_log.jsonl 93 lines each, utc stamps 16:12:54Z…16:37:09Z consistent with sacct ElapsedRaw 1480/1479 s.
- Verdict recomputed: `scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs …/verdict_rerun.json` → identical to results/…/verdict.json (inconclusive, measurement capacity).
- Tests: tests/topic2_fu_a 69 passed, 1 skipped (skip = token_scan_b300_stage1.json absent; Stage 1 not run — legitimate); old suite (STRICT_E2E=1, test_empirical_four_topics + test_pilot_connectome + tests/e2e) 86 passed.
- Independent mutation probe (12 mutants of my own across verdict.py, run.py, sources.py, target.py; full FU-A suite): control passes, 12/12 killed, survivors [] (verification/auditor_FU_A_r1_1/mut/results.json). Includes F+ gain sign flip, F+ fail falling through, δ/2, fixture source not rebound, κ ignored, brain mask dropped, wrong cell mean, r1 noise 0.1, card sha unchecked, token regex opened, sources not restored.
- Fixture partitions rebuilt independently on local CPU with the frozen script: perms_fua_Fplus.npz / perms_fua_Fminus.npz byte-identical (629a699b…, 2e96493b…); fixture_build.json equal except runtime.
- Calibration recomputed: σ_v = 6.545925453832064 from NF 0.20850750121592257 and the fixture ellipsoid (nbar 162.655); κ = 1/√Q = 5.699891773354029. Matches constants.
- B300 (sacct, user connectome): FU-A jobs 403 (GPU, 199 s), 427 (GPU, 266 s), 489/492/510 (CPU), 507_0/507_1 (gpu partition, gres/gpu=1 each, 1480/1479 s, COMPLETED). Ledger rows: start+closing rows for 403, 427, 507 with matching GPU-h (0.056, 0.074, 0.822); FU-A total 0.952 ≤ cap 8. No g3t-G-E0-* job exists in sacct since 2026-11-01T11:00Z → sharing rule satisfied at submission.
- B300 hashes of runs/* and logs/* (15 files) equal the repo copies / output_sha256.txt; frozen code tree on B300 equals receipts; B300 design_stats.json sha 694c31ca… = repo design_stats_train.json. /scratch/iitp4/fu_a/runs contains only Fplus_E_s0, Fplus_C_s0. Data view = 88 hNN symlinks into the r1 subject store (IDs not printed: redacted in b300_hashes.txt).
- C4: count-only scan streamed from the repo to B300 (names of the 88 r1 token dirs + HCP directory names, 1,172 in memory, nothing written on B300) over 132 FU-A text files (results, src, tests, scripts, docs, ledger, worker/explorer verification and metadata dirs): 0 hits. Positive control on B300: 3/3 detected.
- Git: since 14:00Z only `Chavis Autocommit` and root checkpoint (`docs(iitp): checkpoint …`) commits; no agent git writes found. No tracked non-metadata file modified.
- No orphan worker processes or ssh masters on DGX-Spark (worker's /tmp/fua_b3_cm absent).

## 2. Logic Chain
1. Results after freeze: independent autocommit timestamp (16:05:25Z) + sacct start (16:12:31Z) + embedded hashes → the governing card and code were fixed before any FU-A run; no real-data FU-A model exists (pre-freeze real-data exposure = TRAIN design stats + explorer arm-independent probe, both disclosed in card §0).
2. Fabrication: run records are Slurm products on B300 (sacct COMPLETED, byte-identical copies, internally consistent num/den, timing matches), partitions reproduce byte-for-byte, verdict recomputes identically → no fabricated or hand-edited outputs.
3. Facades/self-certifying tests: code performs real computation (block means, broadcast, rebinding into the pinned r1 loop); 12 independent mutants plus the worker's 31 are all killed → tests can fail on the targeted defects.
4. Compute/data governance: all GPU use in Slurm, ledgered, under cap; project-local venv under /scratch/iitp4/fu_a; HCP per-subject data stayed on B300; 0 ID hits with a working detector.
5. Hence no prohibited pattern under any mode → CLEAN.

## 3. Caveats
- Absence of GPU use outside Slurm cannot be proven exhaustively; sacct and the run records (CUDA_VISIBLE_DEVICES, timing) are consistent with Slurm-only use.
- I did not rerun a GPU gate seed (not needed: records Slurm-backed and consistent; 0 GPU-h used by this auditor).
- Scientific (non-integrity) notes, nonblocking: (a) the realized fixture noise share 0.248 exceeds the calibrated 0.209, making F+ harder than the calibration target; it is disclosed pre-freeze in card §7.1 (the card calls this "conservative", which it is only in the sense of a stricter gate). (b) The gate is single-seed F+ E/C only (declared pre-run deviation). (c) Report §5.1 "a voxel-level F+ gate at HCP noise would almost certainly fail" is labelled as an untested inference.
- Cross-team: worker reports tests/topic2_rgpool/test_outputs_no_ids.py failing on FU-B's card; not FU-A's file; not re-run here.

## 4. Conclusion
FU-A is CLEAN: no hardcoded results, facades, fabricated logs, pre-freeze results, ID leakage, protected-file writes, out-of-Slurm/unledgered/over-cap GPU use, foreign env use, or agent git writes found. The shipped verdict `inconclusive` (measurement capacity; F+ gain 0.551 % < δ 1 %) is reproduced from the records by the frozen code.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
for f in card_sha256 code_sha256_at_freeze output_sha256; do grep -v '^#' results/topic2/2026-11-02_fu_a/$f.txt | LC_ALL=C sha256sum -c; done
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_a -q
/home/juke/superclaude-env/bin/python3 scripts/topic2fu_a_verdict.py results/topic2/2026-11-02_fu_a/runs /tmp/x.json
/home/juke/superclaude-env/bin/python3 verification/auditor_FU_A_r1_1/mut/run_aud_mutants.py
ssh connectome@61.107.201.98 'sacct -j 507 -o JobID,NodeList,AllocTRES%45,State,ElapsedRaw'
```
Invalidation: any receipt mismatch, a surviving mutant, a non-identical B300/repo hash, or a nonzero ID count.
