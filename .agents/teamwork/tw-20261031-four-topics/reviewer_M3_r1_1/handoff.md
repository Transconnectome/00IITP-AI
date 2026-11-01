# handoff — reviewer_M3_r1_1 (M3 / Topic 2) — HARD, 2026-11-01T06:08Z

**Verdict: REQUEST_CHANGES.** There is one blocking issue, C4 pseudonym linkability (B1).
- Everything else I checked holds: T2.1–T2.3, C1–C3 and C5–C8.
- The scientific result is reproduced independently. The frozen card gives `stop`; both fixture gates pass.
- I found no integrity violation. The saved checkpoints re-evaluate to the reported test NMSE bit-for-bit.

## 1. Observation

### Re-run checks
All outputs are in `/home/juke/git/00IITP-AI/verification/reviewer_M3_r1_1/`.

| check | result | output file |
|---|---|---|
| C1 `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` | rc 0, 67/67 OK (includes `src/rg_box_pooling.py` and the old tests) | `c1_protected_hash_check.txt` |
| new suite `tests/topic2_rgpool` | 55 passed, rc 0 | `tests_topic2_rgpool.txt` |
| old suite (explicit list of 3) | 86 passed, rc 0 | `tests_old86.txt` |
| `tests/topic1_lagmotif` (C2) | 88 passed, rc 0 | `tests_topic1_lagmotif.txt` |
| card plus frozen inputs | rc 0, 8 files | `card_check.txt` |
| code freeze | rc 0, 33/33 | `code_freeze_check.txt` |
| output pins | rc 0, 43 files | `output_check.txt` |

The only files present now but absent from the freeze list are the 3 disclosed in addendum 01: `scripts/topic2_id_scan.py`, `tests/topic2_rgpool/test_outputs_no_ids.py` and `test_token_order.py`.

### Pre-registration timeline (G5)
- The card is frozen at sha `c9bfc60a…41f5`. Host checkpoint commit `51609c1` (2026-11-01T03:16:27Z, not a run agent) holds the card with the same bytes. That is an external timestamp for the freeze.
- All 27 `run.json` files have `start_utc` after 03:14:34Z.
- Addendum 02 is first in commit `c67403f` at 04:01:27Z, with its current bytes. That is before the first Stage-1 test numbers (wave 2 ended 04:11Z).
- The earliest committed report has `STAGE1_VERDICT_PLACEHOLDER` in §0. No verdict was written before the data existed.
- `PI_DECISIONS_2026-11-01.md` (mtime 02:55Z, before the freeze) already fixes δ = 1 % for M3 and HCP-YA OA as public under C6.

### Independent recomputation
`recompute_verdict.py` does not import the package and runs 197 checks, 0 failed (`recompute_verdict.out.json`). It confirms:
- every run is `completed`;
- `code_sha256` equals the freeze list;
- `test_nmse == Σnum/Σden`;
- the budget is 8750×16, lr 2e-4, mask 0.6;
- the HCP test order equals the `split.json` test list.

It reproduces the gates and the verdict exactly:

| quantity | value |
|---|---|
| F+ gate | +3.061 % / +2.935 % → pass |
| F− gate | −1.737 % → pass |
| I1 | mean +0.1468 %, t95 [−0.0677 %, +0.3614 %] |
| I2 | mean +0.4733 %, t95 [+0.00098 %, +0.9455 %] |
| verdict | **stop** |

The t quantiles were also checked against scipy.

### Pairing evidence
- `test_den` is bit-identical across all 15 HCP runs, across the 6 F+ runs and across the 6 F− runs. So the evaluation masks and test data were the same in every arm.
- Job args in `verification/worker_M3_r1/wave{1..4}_jobs.json` differ only in arm, seed and perm-key.
- The defaults in `scripts/topic2_train.py` are wd 0.05, warmup 0.05, eval seeds 7001/7002, probe 200 steps and 0.75 h.

### Permutations
`check_perms.py` uses numpy only (`check_perms.out.json`). Every shipped π:
- is a bijection;
- is octant-local under ver11's gather semantics;
- leaves untouched blocks as identity.

Every run uses the expected key: E, C, or `S_seed{s}`.

### B300 integrity
- CPU only, no GPU (`b300_cpu_check.json`). Each of the 15 `model_final.pt` holds `layers.0.downsample.perm`, and its int64 sha equals the run's `perm_sha256`. E is arange; C and S are not. The checkpoints are 15 distinct files, and all 27 B300 `run.json` match the repo copies byte for byte.
- GPU 5 for 24 s, 0.01 GPU-h, logged (`b300_gpu_check.json`). I rebuilt hcp_E_s2, hcp_C_s2 and hcp_S_s2 with the frozen code and re-evaluated them. Test NMSE matches `run.json` bit-exactly: rel diff 0.0, per-subject num identical, den identical.
- A first launch on GPU 7 was aborted because GPU 7 became busy between my check and the launch. It is logged as 0 GPU-h.

### Other findings
- **Vendored ver11.** It is byte-identical to `git show f0dc7aca:project/module/models/…ver11.py` (de132387…) and to patchembedding (c889eebb…). The SwiFT_v2 ver11 working file is clean. No SwiFT_v2 file changed between 02:00Z and 05:40Z (C7).
- **T2.1 line citations** match the vendored file: 41–88, 72, 73, 81, 85, 717, 868, 1036, 1068 and 1112. `forward_encoder` replaces masked tokens with the mask token (lines 1319–1321).
- **Reviewer mutants.** These are mine, separate from the worker's list (`mutant_*.diff`; isolated copies, now deleted). The control passed 12/12. Each mutant was killed:
  - FC from train+val+test → `test_partition_ignores_val_and_test_subjects` FAILS;
  - stop rule on the lower bound instead of the upper bound → `test_verdict_mapping` FAILS;
  - arm-dependent init seed → `test_step0_weights_identical_across_arms_tiny` FAILS.
- **C4 scan.** I re-ran the frozen `scripts/topic2_id_scan.py` on B300 over 208 current text files, including post-scan edits and my own files: 0 hits.
- **Ledger.** Total completed is 11.943 GPU-h, of which worker_M3_r1 is 11.73. All 32 lines are well formed.
- **Training dynamics** (`train_log.jsonl`). Every HCP run sits on the predict-zero plateau (loss < 0.995 only after step 1,100–4,200). hcp_S_s2 never leaves it. In fixture runs, the loss falls from the first logs.
- **Descriptive reviewer baseline** on the same test masks: mean of unmasked same-voxel frames within ±3 gives NMSE 1.312, worse than predicting 0. Its denominator equals the runs' Σden exactly.

### C4 evidence (blocking)
- `src/topic2_rgpool/data.py` `pseudonym()` returns `content_sha256[:16]`. That is an unsalted sha256 of the raw NIfTI bytes.
- `results/topic2/2026-11-01/hcp_manifest.json` stores, for all 88 subjects:
  - the full 64-hex `content_sha256`;
  - the exact `file_bytes` (88/88 unique).
- These tokens key per-subject results in:
  - `split.json`;
  - all 15 HCP `run.json` (`test_pseudonyms`);
  - `stage0_hcp.json` (`test_pseudonyms_order`, `per_subject`).
- The `"salt"` in `split.json` is only the public split-ordering string.
- **Complete affected-file list** (06:09Z). I ran a count-only `grep -rlF -f` with the 176 tokens (88 pseudonyms + 88 full hashes). The token file was kept in the scratchpad and deleted afterwards. Scope: `results/`, `docs/03_empirical_analysis/`, `verification/`, the run metadata root, `src/`, `tests/` and `scripts/`. Exactly 19 files hit, all under `results/topic2/2026-11-01/`:

  | file | token count |
  |---|---|
  | `hcp_manifest.json` | 176 |
  | `logs/preprocess.log` | 88 |
  | `split.json` | 88 |
  | `stage0_hcp.json` | 16 |
  | the 15 `runs/hcp_*/run.json` | 16 each |

  There are no hits in `verification/`, docs, metadata, code or tests.
- **Git history** (06:09Z). `git grep -lF -f` over every commit since 2026-10-31 (42 commits, all refs) on docs, .agents, results, verification, src, tests and scripts found 0 hits. `results/topic2/` has 0 tracked files. So no committed file carries the tokens, and history needs no handling as of 06:09Z. The host autocommit daemon could still pick up `results/` later.
- **Final hash checks** (06:10:11Z, after my last write): C1 rc 0 (67/67), output pins rc 0, code freeze rc 0 (`c1_final_check.txt`).

## 2. Logic Chain

1. **T2.1 is met.** The cited lines show merges only at the end of stages 0–2 and none after stage 3. So the old premise ("PatchMerging between layer_2 and layer_3") is false, as documented.
2. **T2.2 is met.**
   - The card is frozen before every governed computation, with an external timestamp.
   - There is a single manipulated factor π. It is parameter-free and bit-identical to PatchMergingV2 at identity, with matched init, data, masks and budget (tests plus my den check).
   - The kill rule is stated.
   - Fixtures exist both where RG should help (F+) and where it should not (F−), at the CPU and training-loop levels.
   - The tests are substantive: my 3 extra mutants are each killed.
3. **T2.3 is met.**
   - The pilot ran on B300 within the cap: 11.73 of the 14 sub-cap and the 64 run cap.
   - The data are HCP-YA OA, PI-confirmed public under C6, with no ENIGMA path.
   - The verdict follows the card. I recompute it independently and get `stop`, because I1's upper bound of 0.36 % is below δ = 1 %. The escape clause correctly was not needed.
4. **Integrity.**
   - The checkpoints carry the claimed π and re-evaluate to the reported numbers bit-exactly.
   - The repo `run.json` files equal the B300 originals.
   - The verdict was a placeholder before the data. So the results are not fabricated, and the verdict was not pre-written.
5. **C4 is not met as written.**
   - C4 permits "positional index or salted hash". The shipped tokens are neither. They are deterministic public functions of each subject's file, stored next to the exact file sizes.
   - Anyone with the lab-staged HCP directory on B300, or an HCP OA file listing, can map all 88 tokens to HCP subject IDs. File size alone is enough (`stat`/`ls -l`); hashing also works.
   - This is the same recoverability the worker flagged for explorer_M3_r1_1's salt file.
   - The ID scan cannot detect it, because it searches only for literal IDs.
   - The dispatch requires C1–C8 strictly, so this blocks APPROVE. It does not touch the scientific verdict.
6. **The low-sensitivity regime is consistent with "stop".**
   - E explains about 1.1 % of the masked variance, and a simple temporal baseline is worse than 0. So voxel noise dominates the target, as the worker said; it is not a pipeline bug.
   - In this regime δ = 1 % NMSE is about the size of all explained variance. Per-seed I1 also follows plateau-escape timing: E_s0 and E_s2 escaped last (steps 3,100 and 2,800) and give the two largest I1 values.
   - "Stop" is therefore correct under the PI-fixed δ but not very informative. The worker already scopes it this way (report §0, §6, addendum 02 §3). This is not grounds to override the card.

## 3. Caveats

- **Ownership.** I did not read the other M3 verifiers' folders (`challenger_M3_r1_1`, `reviewer_M3_r1_2`, `auditor_M3_r1_1`), locally or on B300.
- **Linkage shown in principle only.** I did not perform the linkage, by design. The "file size → ID" route is argued from `file_bytes` uniqueness and a standard directory listing, not executed.
- **Interpretation of C4.** If the root or PI rules that linkage to HCP OA subject IDs is acceptable (those IDs are public inside HCP OA, and the HCP DUT forbids re-identifying people, not this linkage), B1 can be downgraded. Then the verdict would be APPROVE with the non-blocking items below.
- **No full rerun.** I re-evaluated only seed 2 (E, C, S) on GPU. The other 12 checkpoints were checked only for perm and hash.
- **ENIGMA access.** I cannot prove that `~/enigma_ocd` on B300 was never read. No M3 code, script or verification file references ENIGMA.
- **My ledger appends.** I used `flock` on the ledger file itself. `scripts/topic2_ledger.py` locks `results/gpu_ledger_2026-10-31.md.lock`, so my lock did not serialise against that script. Each of my rows was a single small O_APPEND write, and all 32 lines are well formed afterwards.
- **Baseline scope.** The temporal-interpolation baseline is a reviewer descriptive probe. It is not a governed result and must not be cited as a Topic 2 result.

## 4. Conclusion

**REQUEST_CHANGES. Blocking:**

**B1 (C4).** Replace the repo-side subject tokens with positional indices, or with an HMAC-SHA256 under an off-repo key held on B300 or lab-only.
- Affected files, from the count-only scan (19 in total, all under `results/topic2/2026-11-01/`): `split.json`, `hcp_manifest.json`, `logs/preprocess.log`, the 15 `runs/hcp_*/run.json` and `stage0_hcp.json`.
- Drop the full `content_sha256` and `file_bytes` from repo copies.
- Keep the originals off-repo, with their sha256 recorded, so the card's frozen-input pins stay verifiable.
- Record this in a dated addendum, write a new dated output-hash file (do not overwrite `output_sha256.txt`), and add a test that rejects unsalted content-hash tokens.
- As of 06:09Z no commit contains the tokens, so git history needs no handling. Fix this before the host autocommit daemon or a checkpoint job stages `results/topic2/`.

**Non-blocking. Fix them in the same pass:**

| # | finding | where | action |
|---|---|---|---|
| N1 | Stale "PI confirmation pending" statements on δ and HCP/C6 | report §0/§6, handoff, card §4/§8 (card frozen: correct by addendum only) | Note in an addendum that the PI decided both before the freeze (`PI_DECISIONS` 02:55Z) |
| N2 | `SOURCE.md` names a nonexistent `tests/topic2_rgpool/test_vendor_provenance.py`; the check lives in `test_leakage_and_provenance.py` | `vendor_swift_ver11/SOURCE.md` | Correct the test name |
| N3 | Worker timestamps "re-check ~05:42Z" and "correction 05:40Z" are later than the files: `final_*` at 05:30–05:34Z, DISPATCH.md mtime 05:37Z, handoff delivered before my 05:39:41Z dispatch | worker metadata | Correct to actual times |
| N4 | Disclosed C4 incident: the worker printed one real-format HCP example ID in tool output (not files) | worker tool output | Root records it |
| N5 | The report does not name the rank-288 decoder bottleneck, per octant per frame in E36, as a ceiling cause | report §7 | Reorder the costed plan: options A, D and E before B |
| N6 | Plateau-escape timing confound on per-seed I1 | report | Add one line |

The scientific deliverable (T2.1–T2.3, verdict `stop`) is sound and reproducible.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool -q
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_M3_r1_1/recompute_verdict.py $PWD /tmp/rv.json   # expect n_failed 0, verdict stop
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_M3_r1_1/check_perms.py $PWD /tmp/cp.json
/home/juke/superclaude-env/bin/python3 -I -c "import json;m=json.load(open('results/topic2/2026-11-01/hcp_manifest.json'));print(len({s['file_bytes'] for s in m['subjects']}), all(s['pseudonym']==s['content_sha256'][:16] for s in m['subjects']))"   # B1 evidence: 88 True
```

- **B300.** Run `/scratch/iitp4/reviewer_M3_r1_1/b300_check.py cpu|gpu` with the worker's venv. Its outputs are copied to `verification/reviewer_M3_r1_1/b300_{cpu,gpu}_check.json`.
- **Invalidation.** This review is invalid if any of the following happens:
  - any pinned hash changes;
  - `recompute_verdict.py` reports a failure;
  - a checkpoint's perm differs from its run.

  B1 is resolved when no repo file carries the unsalted content-hash tokens, full content hashes or file sizes, and the card's frozen-input hashes remain verifiable against the retained originals.
- **GPU use.** reviewer_M3_r1_1 used 0.01 GPU-h on B300 .98 GPU 5. The aborted GPU 7 attempt counts as 0. Both are in `results/gpu_ledger_2026-10-31.md`. No reviewer process remains on B300.
- **What stays on B300.** `/scratch/iitp4/reviewer_M3_r1_1/` holds only `b300_check.py` and small JSON/stdout results. The code copy and ID-scan copy were deleted at 06:07Z, and no HCP data was copied there.
- **Whole-run layout lint.** `audit_layout.py` gave rc 0 with 0 findings (`verification/reviewer_M3_r1_1/audit_layout_whole_run.txt`).
