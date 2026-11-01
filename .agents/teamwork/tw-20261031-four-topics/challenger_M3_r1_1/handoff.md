# handoff — challenger_M3_r1_1 (M3 / Topic 2) — HARD, 2026-11-01T06:20Z

**Verdict: CONFIRMED.** I tried to break the M3 delivery and could not break any governed claim.
- The card was frozen and committed before any real-data number.
- Every headline number reproduces from the raw run records, and also from the saved checkpoints.
- The verdict `stop` follows the card's §8 rules.
- The T2.1 architecture facts hold.

The findings are test-coverage gaps, stale statements in the report, and hygiene notes. None of them leaves a shipped artifact unverified, and none changes the verdict.

All of my probes and outputs are under `/home/juke/git/00IITP-AI/verification/challenger_M3_r1_1/`.

## Challenge Summary

**Overall risk assessment: LOW.** That covers the verdict and the numbers. Test coverage of the outcome path is MEDIUM: 14 of 32 mutants survive the shipped suite.

## 1. Observation

**Freeze before results.**
- Hash checks:
  - `card_sha256.txt`: rc 0, 8 files.
  - `code_sha256_at_freeze.txt`: rc 0, 33 files.
  - `output_sha256.txt`: rc 0, 43 files.
  - C1 `PROTECTED_HASHES.txt`: rc 0, 67 files.
- Git history of the card:
  - The card is committed once, in 51609c1 at 2026-11-01T03:16:27Z, and that blob's sha256 is c9bfc60a…41f5, the frozen value.
  - It has never changed since.
- `results/topic2/` is untracked by git. So the hash files in it are anchored only by mtimes. Two things anchor the freeze independently:
  - the card blob in git;
  - the fact that all 27 run.json files carry one identical `code_sha256` dict, including the wave-1 fixture runs launched at 03:16:15Z, before any outcome existed (`recompute_verdict.py`).
- Order of events:

  | event | time (UTC) |
  |---|---|
  | card frozen | 03:14:34Z |
  | card committed | 03:16:27Z |
  | partitions_hcp built | 03:20Z |
  | stage0 | 03:24Z |
  | latest F+ gate run ended | 03:42:08Z |
  | first hcp run launched | 03:44:49Z |
  | addendum 02 committed (c67403f, blob unchanged since) | 04:01:27Z |
  | earliest hcp test result (hcp_E_s0) | 04:10:48Z |

- So the F+ gate finished before Stage 1 started, and addendum 02 really was written before any Stage-1 test number existed.
- The first committed draft of the report (c67403f) had `STAGE1_VERDICT_PLACEHOLDER`, so the conclusion was not written in advance.
- No file that governs a computation changed after the freeze. The only files newer than the freeze are `test_token_order.py`, `scripts/topic2_id_scan.py` and `test_outputs_no_ids.py`, which matches addendum 01.

**Independent recomputation** (`recompute_verdict.py`, which does not import `src.topic2_rgpool`; output in `recompute_verdict.out.json`).
- 27 runs, 0 findings. Every run checks out:
  - card §5 hyperparameters;
  - status `completed`;
  - start after the freeze;
  - per-module code hashes equal the freeze list;
  - perm file sha and key are right; E is the identity; C is the same across seeds; S is distinct per seed;
  - all runs share the split sha and the test order;
  - test_nmse = Σnum/Σden.
- The gates and the I1/I2 t intervals match `verdict.json` exactly (difference 0.0):
  - F+: +3.0607 % (C vs E) and +2.9347 % (C vs S): pass.
  - F−: −1.737 %: pass.
  - I1: mean +0.1468 %, [−0.0677 %, +0.3614 %].
  - I2: mean +0.4733 %, [+0.00098 %, +0.9455 %].
- My own hierarchical bootstrap (20k draws, different RNG) gives I1 [+0.024 %, +0.291 %] and I2 [+0.254 %, +0.827 %], within Monte Carlo error of the worker's.
- The post hoc analysis without seed 2 matches exactly.
- My re-implementation of card §8 gives **stop**. Stop holds for any δ above 0.361 %.

**Split and manifest.**
- `split.json` reproduces from the manifest with my own sha256(salt + pseudonym) ordering: 16 test / 8 val / 64 train, disjoint, and the manifest sha matches.

**Permutations** (`check_perms_structure.py`, my own geometry).
- Every key of `perms_{hcp,Fplus,Fminus}.npz` is a bijection, keeps every box inside its octant, and leaves untouched blocks as the identity: **0 violations**.
- hcp: C regroups 231 of 234 touching blocks (dispersion 1.469); S regroups 231–232 (1.557–1.674); E has dispersion 0.784.
- F+: C purity 1.0, against 0.25–0.31 for the other arms.

**B300 probe 1** (node .98, GPU 7, 05:52:26–05:54:14Z, 0.031 GPU-h, ledgered; `b300/reeval_ckpt.py`, output `b300/reeval_ckpt.json`).
- The persistent M0 `perm` buffer in every one of the 15 Stage-1 checkpoints equals the run.json `perm_sha256` and the matching `perms_hcp.npz` key. So each trained model really used its own grouping.
- I re-evaluated all 15 checkpoints on the 16 TEST subjects with my own num/den loop, and my own token-to-voxel mask upsampling (0 mismatches against the model's mask). Test NMSE matches run.json to at most 3e-7 relative; den matches to 2.4e-8.
- Perm-swap on seed 0: forcing a different grouping onto a trained model always hurts.

  | model | own perm | swapped perm |
  |---|---|---|
  | C | 0.98855 | identity π: 0.98950; S0 π: 0.99045 |
  | E | 0.99087 | C π: 0.99138 |
  | S0 | 0.99096 | C π: 0.99153 |

**B300 probe 2** (GPU 7, 06:08:54–06:09:56Z, 0.017 GPU-h; `b300/swap_all_seeds.json`).
- With identity π, every C checkpoint gets worse: by +0.10 %, +0.13 %, +0.15 %, +0.15 % and +0.13 % for seeds 0–4.
- With the C π, every E checkpoint gets worse: by +0.05 %, +0.12 %, +0.02 %, +0.13 % and +0.13 %.
- C evaluated with identity π, compared with E evaluated normally:
  - It still beats E in seeds 0 and 2 (0.98950 vs 0.99087; 0.99008 vs 0.99262).
  - It does not in seeds 1, 3 and 4.
  - Seeds 0 and 2 are exactly the seeds where E was still at about 1.0003 val NMSE at step 2188, i.e. it left the trivial solution late.
  - Per-seed I1 in the remaining seeds (1, 3, 4) is +0.07 %, −0.03 % and +0.06 %.

**B300 CPU probe** (`b300/repro_partitions.py`, output `b300/repro_partitions.out.json`).
- I recomputed, with my own code, the train-only group FC (Fisher-z mean over the 64 TRAIN subjects) and the ≥50 % group mask. The FC float32 sha, nvox and group mask equal the worker's.
- Rebuilding with the frozen builder from my FC reproduces C and S_seed0–4 exactly.
- Each S surrogate preserves the multiset of FC values in every (octant, exact squared distance) bin: 0 violations over 2,275 bins and 465,895 changed pairs.
- Within-box mean train FC, signal-cell-weighted (`b300/within_box_train_fc.out.json`): C 0.2303, E 0.2236, S0 0.1588, G 0.1993, R 0.1013.

**Tests.**
- `tests/topic2_rgpool`: 55 passed (`tests_topic2.txt`).
- Old suite, on CPU: 86 passed (`tests_old86.txt`).
- Whole-run `audit_layout.py`: rc 0, 209 files, 0 findings (`audit_layout_run_root.txt`).

**Mutation** (`mutation/run_mutants.py` v2, CPU only, 32 mutants plus 1 baseline, each on a fresh mirror copy; `mutation/mutants.out.json`, logs in `mutation/logs/`).
- The baseline passes 55/55. 18 mutants are killed and 14 survive.
- An earlier v1 run was aborted because the local GB10 ran out of memory under 4 parallel suites. It is preserved unmodified in `mutation/v1_gpu_oom/`; its m02 "kill" there was environmental.

**Isolation probe** (`probe_octant_check_isolation.py`).
- Production `validate_perm` rejects a cross-octant swap of two signal cells in touching blocks.
- Mutant m15, with the octant rule disabled, accepts that swap.
- The shipped test swaps cells 0 and 4095. Both sit in **untouched** blocks, so the test still raises under m15, via the "untouched block regrouped" branch.

**C4 scans** (counts only; no digits printed).
- Over 185 M3 files, every standalone 6-digit token is a count field (n_brain_vox, etc.) or a code constant.
- My own outputs contain 0 manifest pseudonyms, and their only 6-digit tokens are an array shape and a count.

## 2. Logic Chain

1. The card blob is committed at 03:16:27Z, the code hashes are identical in every run.json, and the earliest real-data outcome comes later. So the protocol came before the results (G5).
2. Recomputing from run.json, independently of `stats.py` and `topic2_verdict.py`, gives exactly the shipped gates, intervals and verdict. So the verdict follows the card: I1 hi = 0.361 % < δ = 1 % → **stop**.
3. The run.json values themselves are faithful. Re-evaluating the saved checkpoints with an independent loop reproduces them to ~1e-7 relative. That covers the mutants that touch the metric or the test set (m20, m21, m32) for the shipped artifacts.
4. The arms really differ in the intended factor only:
   - each checkpoint's perm buffer equals its declared partition;
   - perm-swap degrades every trained model, so the trained weights depend on their grouping;
   - E is the identity; S preserves the distance bins;
   - partitions reproduce from train-only data.
5. The survivors leave no shipped artifact unverified. Each one maps to an independent check:

   | survivor | covering check |
   |---|---|
   | m08, m29, m30 | `recompute_verdict.py` |
   | m15 | `check_perms_structure.py` |
   | m20, m21, m32 | B300 re-evaluation |
   | m31 | split reproduced (the script's runtime assert would also fire) |
   | m18, m19 | partition reproduction and structural audit (reproducibility, not "canonical slot order") |
   | m22, m23, m24 | **code reading plus the frozen hash only** |

6. The interpretation holds up. The tiny positive I1 point estimate sits mostly in seeds where E escaped the trivial solution late. C models stripped of their grouping at test time still beat E in those seeds. That is consistent with stop and further weakens attributing even +0.15 % to grouping.

## 3. Caveats

- **No retraining.** Retraining is forbidden: no full pilot repeat, and the cap is 1 GPU-h. So I did not independently reproduce the training dynamics, such as the F+ gate margins or the S_s2 stall. The F+/F− checkpoints were not saved, so the gate numbers were checked only from run.json.
- **Three survivors rest on code reading.** m22 (loss mask), m23 (fixture stream pairing) and m24 (mask stream pairing) are covered only by reading the frozen code (`w = mv * brain`; generators seeded 1000/2000/3000 + seed only) and by its hash.
- **The perm-swap reading is descriptive and post hoc.** n = 5 seeds.
- **Peer reports not read.** I did not read the peer challenger, reviewer or auditor folders, to keep my review independent.

## 4. Conclusion

**CONFIRMED.** T2.1, T2.2 and T2.3 hold as claimed, and the card verdict `stop` is correct and robust. Nonblocking issues for root and the PI:

1. **Coverage gaps, MEDIUM.** The shipped tests do not pin these:
   - the primary NMSE metric (m20, m21);
   - the SimMIM loss mask (m22);
   - arm pairing of the training data and mask streams (m23, m24);
   - the governing `scripts/topic2_verdict.py` (m29, m30);
   - the sign of `relative_gain` (m08);
   - octant locality in isolation (m15: the test passes for the wrong reason);
   - the canonical slot order (m19).
2. **Latent bug, LOW.** `topic2_verdict.py` passes `fm is not False`, so a missing F− gate counts as a pass. No effect here: F− is complete.
3. **Stale statements in the report and handoff, LOW.** They still list δ = 1 % and HCP-as-public as pending PI decisions. `orchestrator/PI_DECISIONS_2026-11-01.md` resolves both: δ = 1 %, and HCP-YA Open Access counts as public. On timing, the file's text says ~11:2x KST, but its mtime is 14:42 KST. Either way stop holds for any δ > 0.361 %.
4. **Readability, LOW.** Report §3.4 ("+13.1 % of E's explained variance") is a post-hoc framing that a reader could take as a positive result.
5. **C4, LOW; needs a PI/root decision.**
   - `hcp_manifest.json` stores the full **unsalted** content_sha256 of public HCP files. Anyone with HCP Open Access can map a pseudonym to an HCP subject ID by hashing the files. C4 asks for a positional index or a salted hash.
   - The explorer salt-adjacency issue the worker flagged is confirmed present: `verification/explorer_M3_r1_1/dev_subject_salt.txt` sits next to `dev_subjects_BURNED.md`. I did not open the hashes or try to brute-force them.
6. **Local GPU, LOW.**
   - `train.run` picks CUDA whenever it is visible. So the "CPU smoke" test ran on the local GB10 (in my first suite run and in mutation v1).
   - The worker's "local CPU only" statement is likely inaccurate for the same reason.
   - Suggest `CUDA_VISIBLE_DEVICES=""` in the test commands.
7. **Addendum 03 timing, LOW; not verifiable.**
   - The file's mtime is 04:42:58Z. The wave-3 runs had ended on B300 at 04:40–04:41Z.
   - The addendum says only the wave-2 values were visible.
   - The local copies keep the remote mtimes, so I cannot tell when the worker copied them.
   - The addendum is declared not pre-registered and changes no rule.
8. **Doc reference, trivial.** `vendor_swift_ver11/SOURCE.md` cites `tests/topic2_rgpool/test_vendor_provenance.py`, which does not exist. The check lives in `test_leakage_and_provenance.py`.
9. **Interpretive.** On its own training FC, the C builder beats the cubes only slightly (signal-weighted within-box r 0.230 vs 0.224), and Euclidean greedy growth (G) is worse than the cubes. The kill applies to this builder, target and budget, which is how the worker already scopes it.

**Compute.** 0.048 GPU-h on B300 .98, GPU 7, two evaluation-only probes, both ledgered. My B300 dir `/scratch/iitp4/challenger_M3_r1_1` was removed after the outputs were copied back. No processes of mine remain on B300 or locally.

**Hygiene.** No git writes, no installs, and `~/enigma_ocd` was not touched. No production file was modified: all mutants ran on mirror copies, which were deleted.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
P=/home/juke/superclaude-env/bin/python3
$P -B verification/challenger_M3_r1_1/recompute_verdict.py results/topic2/2026-11-01 /tmp/rv.json      # expect findings [] and verdict stop
$P -B verification/challenger_M3_r1_1/check_perms_structure.py results/topic2/2026-11-01 | tail -1      # STRUCTURAL_VIOLATIONS []
CUDA_VISIBLE_DEVICES="" $P -B verification/challenger_M3_r1_1/probe_octant_check_isolation.py          # m15 accepts, production rejects
cd verification/challenger_M3_r1_1/mutation && $P -B run_mutants.py /tmp/mut.json --jobs 4               # 18 killed / 14 survived (CPU only)
git -C /home/juke/git/00IITP-AI show 51609c1:docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md | sha256sum   # c9bfc60a…41f5
```

To rerun the B300 checks on node .98, use `b300/reeval_ckpt.py`, `b300/swap_all_seeds.py` and `b300/repro_partitions.py`, each with the argument lists recorded in this handoff's commands. They need the worker's `/scratch/iitp4/worker_M3_r1` (checkpoints, hcp/, venv), which is ephemeral.

**This report is invalid if** any of these holds:
- any hash check fails;
- a rerun of `recompute_verdict.py` reports findings;
- a checkpoint perm buffer differs from its run.json;
- the frozen code under `src/topic2_rgpool` or `scripts/topic2_*.py` changes.

## Addendum: final re-checks after my last writes (06:24Z)

- **C2.** `tests/topic1_lagmotif`, run on CPU: 88 passed (`verification/challenger_M3_r1_1/tests_topic1_lagmotif.txt`).
- **Hash checks.** All rc 0: C1, card, code-freeze and output. So my review left every file it touched unchanged.
- **Layout lint.** Whole-run `audit_layout.py`: rc 0, 212 files, 0 findings (`audit_layout_run_root_final.txt`).
- **C4 scan of my own outputs.** 69 files: 0 unexplained 6-digit tokens and 0 manifest pseudonyms.
- **Ledger erratum.** My probe-2 "started" row gives its start as "06:1xZ", which is wrong. The matching "completed" row gives the exact launch time, 06:08:54Z. My total is 0.048 GPU-h.
