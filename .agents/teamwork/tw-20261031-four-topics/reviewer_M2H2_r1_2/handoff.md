# Handoff (Hard): reviewer_M2H2_r1_2, M2H2 (Topic 3 H2 random-init control), 2026-11-01T17:26Z

**Verdict: APPROVE.** Every ACCEPTANCE criterion that applies (H1′, H2′, H3′, C1–C8) is met, and I checked each one myself. Nothing blocks. Seven nonblocking items are listed in §4.

## 1. Observation

- **C1.** `LC_ALL=C sha256sum -c .agents/.../sentinel/PROTECTED_HASHES.txt` gives rc 0 (67 OK). Log: `verification/reviewer_M2H2_r1_2/c1_protected.log`.
- **Receipts.**
  - `results/topic3/2026-11-02_h2/addendum_07_sha256.txt`: rc 0.
  - `results/topic3/2026-11-02_h2/output_sha256.txt`: rc 0 (61 files).
  - The `results/topic3/2026-10-31/` receipts pass except two:
    - `card_sha256.txt` fails on format only. Its trailing "frozen" token trips `sha256sum -c`; the card's actual sha `683374565d80…` matches.
    - `code_sha256_at_freeze.txt` fails for `scripts/topic3_launch_connectome.py`. That file's mtime is 2026-10-31 17:51 KST, the change is disclosed in addendum 01 item 2 and addendum 06 l.179, and it predates M2H2. The worker's handoff did not mention this failure.
- **Freeze before results.**
  - The addendum 07 sha `09b45220…` is in host daemon commit 35d10a5, 2026-11-01 16:05:25Z.
  - The receipt says 15:57:40Z; the file is chmod a-w.
  - Gate job 218063 ran 16:22:21–16:30:24Z. The local `gate_decision.json` was written at 16:31:46Z. Random job 218064 was submitted at 16:32:19Z and ran 16:32:21–16:51:38Z.
  - `h2stats.py` (mtime 16:05:52Z) and `scripts/topic3h2_stats.py` (16:06:28Z) were last changed before any real-data job.
  - The code hashes recorded in `gate_record.json`, `random_record.json`, `gate_decision.json` and `h2_results.json` all equal the current files.
- **Code identity.**
  - The vendored ver11 (`5bc44469…`) and patchembedding (`c889eebb…`) equal `git -C SwiFT_v2 show cd87338:` and `63367643:` byte for byte.
  - `datasets.py` (`74316574…`) equals VRABES 94c2bf4 and the working copy.
  - The constructor arguments in `provenance.MODEL_KW` equal `VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` (sha `b979a682…`) lines 76–82.
  - The ship manifest's 20 `src` entries equal the current files.
- **Tests (mine).** Logs are in `verification/reviewer_M2H2_r1_2/`.
  - `tests/topic3_h2`: 71 passed (328.8 s), `pytest_topic3_h2.log`.
  - `tests/topic3_spectral`: 138 passed.
  - The old suite (`STRICT_E2E=1`, test_empirical_four_topics + test_pilot_connectome + e2e): 86 passed.
  - `tests/topic1_lagmotif`: 88 passed.
- **Independent recomputation** (`recompute_h2.py`, output in `recompute_h2.out`).
  - My own arithmetic and my own decision rule, written from the addendum 07 text. Only the frozen resampling and PR primitives are imported.
  - Result: 24/24 Family C and L labels equal `h2_results.json`, and every point, CI and Holm p differs by 0.
  - δ recomputes from the pinned JSON. T's A1 L2 − L3 reproduces pinned Family A exactly (5.343854531110546 / SE 1.0810551262749508).
  - R0 vs T: per-index-set PR rel 6.35e-7; per-subject rel 7.25e-8.
  - My independent SVD PR agrees with the frozen `pr_cov` to 2.4e-15.
- **δ sensitivity** (label as δ varies, given as a fraction of the trained effect):
  - C1 is INC at every fraction from 0.25 to 0.75, because seed 4's per-seed effect is 0.0036.
  - C2 is TE+ at 0.45 or less, INC at 0.5.
  - C3 is TE+ up to 0.5, INC from 0.55.
  - C4 is TE+ up to 0.6, INC at 0.75.
- **Report numbers.** I audited §2, §3 (E1 ranges, seed ranges, the L2-cov seed −0.079) and §4 (R1 −1.61 / −0.74, A1b, per-seed D1 points 0.06–0.42 and robust seeds 5 / 7 / 10, seed-4 H1a −0.0004 with p_holm 0.52, α medians). All match `h2_results.json`.
- **GPU rerun** (connectome Slurm job 218065, node1, 239 s, 0.067 GPU-h, ledger rows 113 and 124).
  - I shipped my own bundle of the repo code (sha `c3c2fb55…`). Its index-set sha `cd020fe8…` equals the job's.
  - Seed 3 ran alone; in the original job it was the 3rd of 10 encoders sharing each window.
  - Result: its R3 per-subject scalars and per-index-set PRs equal the shipped `random/R3_*.npz` **bitwise** (max rel diff 0), the encoder sha is equal, and E1 L3 cov is 32.047059 in both.
  - For reference, R3 vs R8 differs by 5.9%, so the comparison discriminates.
  - Copied back after an ID scan to `verification/reviewer_M2H2_r1_2/returned_seed3/`; the work dir was deleted by the driver.
- **Gate records.**
  - G1: 399 windows, 0 failing cells, max rel_fro 7.78e-7, max |Δ| 6.7e-6.
  - G4: 568 tensors loaded, 0 missing encoder keys, unexpected = [`augment_comp.smooth_kernel`], checkpoint sha OK, TF32 off, vendor OK.
  - G5: each of the 3 controls fails 84/84 cells; the smallest rel_fro is 4.6e-4.
  - Seeds: hashes distinct; rebuild identical; none equals the trained hash `8240f839…`.
- **IDs.** I scanned 82 H2-related files against the 57 pinned VRABES labels, with and without the prefix.
  - 0 real labels found.
  - The 4-digit bare hits are all decimal fragments (`0.0002` p values, `0.0005` rounding).
  - `sub-` hits appear only in placeholders: synthetic `sub-SYN…`, the words "sub-modules" and "sub-sequences", and `sub-XX`.
  - `results/` has 0 `sub-X` bytes.
- **Extra mutants** (`extra_mutants.py`, results in `extra_mutants.out.json`; copied tree; fast H2 tests): 9 of 14 killed.
  - Killed: X01 (C4 uses cov), X02 (ci90 seed), X03 (L seed offset), X04 (non-strict EQ), X05 (δ check off), X07 (addendum verify off), X08 (vendor verify off), X09 (load hygiene), X12 (random submit without gate).
  - **Survived:**
    - X06: `compare.stats_match` with absolute instead of relative tolerance.
    - X10: `topic3h2_stats.py gate` keeps the in-job G3 only and drops the local recheck.
    - X11: `final` ignores a gate FAIL.
    - X13: the driver's G3 ignores the H1a/H1b contrast-status condition.
    - X14: `final` seed-set check disabled.
- **Layout lint** on the whole run root: PASS, 445 files, 0 findings.
- **Local CPU seed rebuild** (torch 2.11-dev vs the job's 2.4): the hashes differ. That is inconclusive (different RNG paths) and is not used as evidence.

## 2. Logic Chain

1. **H1′.** Addendum 07 freezes the hypothesis, estimators (frozen `src/topic3_spectral`, imported), init protocol (constructor init, seeds 1–10), gate, comparison and decision rule. Its hash was committed (35d10a5, 16:05Z) before the first real-data forward (16:22Z gate) and before any random-init forward (16:32Z). So H1′ is met (§1 freeze, receipts).
2. **H2′.**
   - The replicated pipeline reproduces the stored trained dumps element-wise on every window (7.8e-7 against a 1e-5 tolerance), the pinned statistics (7.3e-8), and the H1a/H1b status.
   - Three perturbations, each well above tolerance, fail the gate, so it discriminates.
   - The gate decision was written before the random job was submitted.
   - Frames stayed on connectome, the job ran under Slurm in a project-local venv, and the ledger has both rows.
   - So H2′ is met.
3. **H3′.**
   - The tests include closed-form and planted fixtures, a test that the comparator rejects the perturbations, a random-init isotropy fixture, and full truth-table and symmetry tests of the rule. They pass in my own runs.
   - Results are in `results/topic3/2026-11-02_h2/`.
   - The report states the H2 verdict and the R1–R3 consequences exactly as frozen in addendum 07 §7.
   - GPU use is 0.458 + 0.058 + my 0.067 GPU-h, far under the 6 GPU-h cap.
4. **Integrity.**
   - My recomputation, which shares no code with `h2stats.py`, reproduces every label and number (diff 0).
   - The GPU rerun of seed 3 reproduces the shipped random arm bitwise.
   - So the numbers come from the stated code and data, and there is no hardcoding, facade or fabrication.
   - The bitwise match from a single-encoder job also excludes cross-encoder contamination in the 10-encoder job.
5. **C4.** No IDs, no git writes by me. C6/C7: external repos were only read, through `git show` and `sha256sum`.
6. **The 5 surviving mutants are nonblocking.**
   - All of them weaken gate and precondition plumbing in a one-shot pipeline that has already run.
   - Their real inputs are independently confirmed: R0 vs T 7.25e-8, contrast mean log ratios equal, seeds 1–10 present, gate PASS.
   - None changes a shipped number or label.
   - The verdict math itself is mutation-guarded: worker 32/32, plus my X01–X05.
   - No criterion (H1′–H3′, C1–C8) requires a mutation-adequate gate harness for M2H2. F2's verdict-code clause applies to the FU options.

## 3. Caveats

- I reran one seed only (seed 3), not the gate job or the G5 controls. Gate evidence is the job record plus my local recheck of R0 vs T.
- I used the worker's connectome venv (`.../worker_M2H2_r1/venv`) read-only, to avoid a second 5 GB venv. My code bundle was separate.
- The run has precedent: the M2 r2b and r3 gates failed on surviving verdict-path guard mutants. My survivors are gate/precondition guards, not verdict arithmetic. If the root applies the stricter r2b standard to the gate plumbing as well, X06/X10/X11/X13/X14 become the items to close, with additive tests only.
- **Cleanup was denied by the permission system** and I did not work around it. Two things remain:
  - connectome `/home/connectome/connectome1/iitp4_m2h2/reviewer_M2H2_r1_2/` (code bundle incl. a copy of the pinned trained spectra npz, logs, returned aggregates; no frames);
  - local `verification/reviewer_M2H2_r1_2/ship/` (bundle copy of repo files).
- δ is a PI-only choice under sci-pipeline. Labels are recommendations (G9).

## 4. Conclusion

APPROVE M2H2. The H2 verdict holds as shipped:
- C3 and C4 are TE+: the subject-level L2 → L3 drop is learned.
- C1 and C2 are INC.
- Family L is as reported.
- Consequences: R2 subject-level drop learned; R2 token H1a unresolved; R1 descriptive; R3 unaffected.

Nonblocking, recommended to the root and PI:
- (N1) Add tests that kill X06, X10, X11, X13 and X14. These are additive new test files; addendum 07 is not edited.
- (N2) The PI should confirm δ and K = 10. The report's §6.1 claim that "a different δ would change C1" is overstated: C1 stays INC for any δ ≥ 0.0036 (≈0.16 × the trained effect). C2 does depend on δ (TE+ at δ ≤ 0.45 ×).
- (N3) The worker's integrity summary omitted the pre-existing `code_sha256_at_freeze.txt` failure.
- (N4) The ledger closing rows for 218063 and 218064 give their times in KST, while the start rows use UTC. They are labelled, so they are not ambiguous.
- (N5) Connectome leftovers can be deleted after the victory audit: the worker venv (~5 GB), the explorer_M2H2_r1_1 venv, and my reviewer dir.
- (N6) Scope limits, all disclosed: the constructor default init only, the primary checkpoint only, and CIs that ignore seed variance.
- (N7) Every number I audited in the report matches `h2_results.json`.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/addendum_07_sha256.txt results/topic3/2026-11-02_h2/output_sha256.txt
git log --format='%h %ci' -- docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md   # 35d10a5 01:05:25 KST
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 -I verification/reviewer_M2H2_r1_2/recompute_h2.py   # MISMATCHES: []
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/reviewer_M2H2_r1_2/compare_seed3.py                     # SEED3_REPRODUCED
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -I verification/reviewer_M2H2_r1_2/extra_mutants.py  # 9 killed / 5 survived
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_h2 tests/topic3_spectral -q
```

This review is invalidated if any of these happens:
- a vendored or pinned hash changes;
- `h2_results.json` changes from sha `356e178e…`;
- the PI sets a different δ (then C2 and possibly C3 change; a new dated addendum is needed);
- a gate rerun exceeds tolerance.
