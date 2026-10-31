# handoff — auditor_M2_r1_1 (forensic integrity audit, M2 Topic 3)

Written 2026-10-31T11:37Z. Dispatch received 11:17:13Z (re-dispatch "3번. A"). Profile: General Project. Integrity mode: Development. ORIGINAL_REQUEST.md has no "from scratch" or "do not delegate" constraint.

## Forensic Audit Report

**Work Product**: M2 Topic 3 rerun.
- `src/topic3_spectral/`, `tests/topic3_spectral/`, `scripts/topic3_*.py`
- `results/topic3/2026-10-31/`
- `docs/03_empirical_analysis/topic3/`, including addendum 02

**Verdict**: **CLEAN** for the M2 work product. There is one run-level C4 item that is not attributable to M2 (see Caveats §1).

### Phase Results

**Hardcoded output detection: PASS.**
- No expected results are embedded in the code.
- `REPORT_TABLE` in `scripts/topic3_provenance_repro.py` is labelled as a transcription of the claims under test. It matches EMPIRICAL_ANALYSIS_REPORT.md lines 68–74.
- The json values are read from `empirical_results.json`.
- The "reproduced" flags are computed from the old protected functions run on real data.

**Facade detection: PASS.**
- Estimators, resampling, verdict logic and the token job all contain real computation.
- The tests use analytic ground truth: an exact prescribed spectrum giving PR = k, and the Wishart moment formula. They are not self-certifying.

**Pre-populated or fabricated artifacts: PASS.**
- Slurm `sacct` for job 217845 shows 4 array tasks on node2, COMPLETED, exit 0. Times were 17:51:32–17:58:52 KST, and they match the .out logs.
- AllocTRES was cpu=12, mem=40G, with no GPU gres.
- On connectome node2, the npz and code hashes match the local copies and the job JSON. Remote mtimes match.

**Card frozen before results (C3): PASS, independently corroborated.**
- Git commit 24fe976 (2026-10-31 17:46:25 KST = 08:46:25Z) contains the card. Its blob sha256 is 683374565d80…8e0, which equals card_sha256.txt.
- That is earlier than Family A run start (08:49:18Z), the Slurm job (08:51:32Z) and Family B (09:01:59Z).
- The code hashes in the run records equal `code_sha256_at_freeze.txt`.
- Pre-card real-data exposure is disclosed in card §11.
- I checked the explorer probes that touched real data. They are structural measurements or reproductions of already-published numbers, as disclosed. The corrPR and subsampling probes are synthetic.

**Build and test: PASS.**
- All runs below used a copy of the tree.
- topic3: 54 passed.
- Old suite (STRICT_E2E=1): 86 passed.
- C1: rc 0 with 67 lines. I reran it at the end of the audit and it still returns rc 0.
- output_sha256.txt: rc 0.
- addendum_02_sha256.txt: rc 0.
- code_sha256_at_freeze.txt: only `scripts/topic3_launch_connectome.py` differs, which addendum 01 item 2 discloses. That launcher computes nothing.

**Output verification: PASS.**
- I ran Family A, Family B, T3.1 and the α calibration in a copied tree. Compared with the pinned JSONs, all values are identical; only absolute-path fields and run timestamps differ.
- Independent recomputation with my own code:
  - L1 jackknife SE = 3.577, matching the frozen output.
  - H1a and H1b mean log ratios, computed from the stored eigenvalues: +0.0228 / +0.0447 (primary), −0.1368 / −0.1130 (HCP_N400), +0.0378 / −0.0330 and +0.0489 / +0.0792 (deep). These match.
- Applying the card rules by hand:
  - D1: cov lo 3.22 > 0 and corr lo 4.28 > 0, so "robust, not per-channel".
  - H1a: the primary CI excludes 0 and 2 of 3 zoo checkpoints agree, so "holds".
  - H1b: 1 of 3 agree, so "not replicated".
  - These equal the coded verdicts.

**Tests can fail (mutation): PASS, with coverage gaps (non-blocking).**
- The control passes.
- Worker mutants M1–M9: 9 of 9 killed when I reran them.
- My 16 new mutants: 12 killed and 4 survived. The 4 survivors are below; none hides a defect in the real outputs.
  - **X13** (uniform iid reference): near-equivalent. Centered PR of isotropic iid columns does not depend on the distribution.
  - **X09** (jackknife factor): a real gap. The shipped value is verified independently (3.577).
  - **X06** (D1 ignores corr) and **X12** (verdict ignores primary CI): verdict-logic gaps. The hand-applied rules give the same verdicts as the code.
- `test_outputs_no_ids` ends with `assert n >= 0`, which is vacuous on an empty tree. Minor.

**Participant IDs (C4): PASS.**
- IDs have the form `sub-` + 4 digits; there are 57.
- Scan scope: 189 files in the M2 code, results and docs, all run metadata, and the worker and explorer verification directories.
- Full-ID hits: 0. Standalone 4-digit core hits: 0.
- A first naive pass showed 25 files with "hits". Those were 4-digit runs inside floats and hashes.
- `sub-` strings occur only as synthetic `sub-SYN…` in the tests and in the code literal prefix.

**Data governance and compute (C5/C6): PASS.**
- No B300 or GPU references in the M2 code, and Slurm shows no GPU.
- Frames stayed on connectome; only position-keyed summaries came back.
- `results/gpu_ledger_2026-10-31.md` does not exist. M2's total is 0 GPU-h.

**External repos read-only (C7): PASS.** The VRABES `git status` is clean, and no VRABES file was modified today.

**Silent fallbacks: PASS.**
- A missing input, a hash mismatch or a contract violation halts the run.
- The α estimator returns NaN on failure, and the descriptive token α medians use nanmedian. This is descriptive only. Minor note.

### Evidence
- Probe dir `/home/juke/git/00IITP-AI/verification/auditor_M2_r1_1/`:
  - `auditor_mutants.py`, `auditor_mutants.out.json`, `auditor_mutants.log`;
  - `compare_json.py`;
  - `frozen_copy/` (copies of the pinned JSONs; hashes equal the pins);
  - `rerun_outputs/` (rerun JSONs plus famA, famB, t31, alpha and pytest logs);
  - `sha256_auditor_artifacts.txt`.
- I deleted the copied tree after the reruns.
- The first T3.1 rerun returned rc 1 because my copy lacked `docs/03_empirical_analysis/empirical_results.json`. That was my setup error, not a product defect. After I copied the protected background docs, it reproduced exactly.

## 1. Observation
Covered in the Phase Results above. The key independent anchors are:
- the git blob of the card at 08:46:25Z;
- Slurm accounting for job 217845;
- hashes on the remote node2;
- value-identical reruns.

## 2. Logic chain
1. The card bytes were fixed before any governed real-data run (git timestamp, plus run-record start times and Slurm).
2. The code used equals the freeze record (hashes match at freeze, in the run records and on remote node2).
3. The outputs are reproducible from that code and the pinned inputs (0 value diffs).
4. The tests detect the targeted defects (21 of 25 mutants killed; the survivors do not affect the real outputs).
5. Therefore there is no fabrication, facade, hardcoding or result-before-card.

## 3. Caveats
1. **Run-level C4 item (root's responsibility, not the M2 worker's).**
   - An automatic background checkpoint has committed every 15 minutes on branch feature/topic1-lag-motif-v2: 12 commits today, the latest 12ab7d1 at 20:31:25 KST.
   - The commits are authored with the root session's attribution. The commit message reads "Automatic background checkpoint… Code, data and results are not included."
   - Their contents are docs and teamwork metadata only. No src, scripts, tests or results are included, and neither are HANDOFF.md, 그랜트아이디어.md or 아이디어.txt.
   - They include the M2 card, provenance note, report and addenda. They also include the protected Topic 1 docs; committing does not change bytes, so C1 still holds.
   - `git ls-remote snuprivate` shows `refs/heads/feature/topic1-lag-motif-v2` = 3bdbc9c (20:01:25 KST), so a push to the private remote happened. origin has no such branch.
   - ACCEPTANCE C4 says "No git commit/push". The relayed human choice "3번" is described by the worker as the push-to-private-repo option, but I did not verify the option text.
   - Root must reconcile these commits and the push with the human before any victory audit. They do not affect the integrity of the M2 work product.
2. The 4 surviving mutants are test-coverage gaps. They do not affect correctness here, but future verdicts depend on untested D1 and primary-CI branches.
3. Not re-executed: the connectome token job itself (corroborated by sacct and remote hashes instead), and H2 (untested by design).
4. Zoo depth and LR attributions in addendum 02 match the VRABES scripts. I did not examine the NERSC logs.

## 4. Conclusion
**CLEAN** for M2. I found no integrity violation. Root should handle the C4 commit and push item separately.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic3/2026-10-31/output_sha256.txt
git show 24fe976:docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md | sha256sum   # 683374565d80…
ssh connectome "sacct -j 217845 -X --format=JobID,NodeList,Start,End,State,AllocTRES%60"
python3 -I verification/auditor_M2_r1_1/compare_json.py verification/auditor_M2_r1_1/frozen_copy verification/auditor_M2_r1_1/rerun_outputs family_A_subject_level.json family_B_token_level.json
cat verification/auditor_M2_r1_1/auditor_mutants.out.json
```
No orphan processes: `ps -p 1370169` returned no process.
