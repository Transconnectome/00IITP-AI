# Handoff (Hard): worker_M2H2_r1, milestone M2H2 (Topic 3 random-init control H2)
Written 2026-11-01 ~17:10Z (UTC). Status: DONE. H2 tested; replication gate PASS.

## 1. Observation

- **H1′ freeze.** `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md` has sha256 `09b45220205bce814c4e07d4494d586b95f63f97dbfcddeb716fafcdc5edd84b`.
  - Receipt: `results/topic3/2026-11-02_h2/addendum_07_sha256.txt`, frozen 2026-11-01T15:57:40Z (`addendum_07_frozen_utc.txt`). The file is read-only (chmod a-w).
  - The first random-init forward on real frames was Slurm job 218064, started 16:32:19Z.
  - The addendum freezes:
    - code identity: fork ver11 `5bc44469…`, patchembedding `c889eebb…`, snapshot `datasets.py` `74316574…`, all vendored byte-identical in `src/topic3_h2/vendor/`;
    - the constructor arguments;
    - the init (seeded `self.apply(_init_weights)`, K = 10 seeds, 1–10);
    - the gate G1–G5 and its tolerances;
    - the endpoint families C and L and the secondaries;
    - δ (0.5 × the pinned trained effect for C1–C4; log 1.10 for levels);
    - the decision rule with its truth table;
    - the consequence map for R1–R3, governance, exposure, the erratum to provenance §2, and the deviations.
- **H2′ connectome.**
  - venv: `/home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1/venv` on node1 (py3.8.10, torch 2.4.0+cu121, numpy 1.24.4, einops 0.8.0, monai 1.3.2, plus nibabel / pandas / sklearn / nilearn). Recipe: `scripts/topic3h2_connectome.py::ENV_RECIPE`.
  - Gate job 218063: 485 s, 0.135 GPU-h. Verdict PASS (in the job and in the local `gate/gate_decision.json`).
    - G1: all 399 windows × 4 layers pass, max rel_fro 7.8e-7, max |Δ| 6.7e-6.
    - G2: re-pool max 7.0e-7, pins and row order OK.
    - G3: max rel 7.3e-8; H1a / H1b status equal.
    - G4: checkpoint sha OK; 568 loaded, 0 missing encoder keys, unexpected = [`augment_comp.smooth_kernel`].
    - G5: all 3 controls fail G1 in 84 / 84 cells; smallest rel_fro 4.6e-4 (+1 frame).
  - Random job 218064: 1160 s, 0.323 GPU-h. The 10 seed hashes are distinct, rebuilding seed 1 is identical, and the work dirs were deleted.
  - Ledger: start and closing rows for both jobs in `results/gpu_ledger_2026-10-31.md`. Total for this worker: 0.458 GPU-h.
- **Results** (`results/topic3/2026-11-02_h2/h2_results.json`, sha256 `356e178e…47e2`):

| Endpoint | Difference (trained − init) [95%] | Label |
|---|---|---|
| C1 H1a | +0.0124 [+0.0104, +0.0145], δ 0.0114; init H1a +0.0103 vs trained +0.0228 | INC |
| C2 H1b | +0.0295 [+0.0256, +0.0334], δ 0.0223; seeds 3 and 8 ≤ δ | INC |
| C3 D1 cov | +5.09 [+2.93, +7.25], δ 2.67; init drop 0.26 | TE+ |
| C4 D1 corr | +5.79 [+4.01, +7.57], δ 3.02 | TE+ |

  - Family L, subject level: TE− (trained lower) at L1 / L2 / LN0L2 / L3, ratios 0.16–0.50; L0 INC.
  - Family L, token level: L1 TE− (×0.74–0.76); EQ for corr at L2 / LN0L2 / L3 and for cov at L3; INC for L0 and for L2 / LN0L2 cov.
- **Tests.**
  - `tests/topic3_h2`: 8 files, 71 tests, all pass, including real-network CPU fixtures.
  - Old 86 pass; `tests/topic3_spectral` 138 pass; `tests/topic1_lagmotif` 88 pass.
  - Mutation run `verification/worker_M2H2_r1/mutants.py`: 32 / 32 verdict-path mutants killed (`mutants.out.json`).
- **Integrity.**
  - C1 rc 0. All `results/topic3/2026-10-31/*_sha256.txt` receipts pass except `card_sha256.txt`, the known case: its trailing "frozen" token trips `sha256sum -c`, but the hash matches.
  - New receipt `results/topic3/2026-11-02_h2/output_sha256.txt` (61 files) passes.
  - "sub-" scan of `results/topic3/2026-11-02_h2/**` and the 2026-11-02 docs: 0 hits. Layout lint: 0 findings.
  - No git writes. No edits to pinned files.

## 2. Logic chain

1. The stored trained dumps are reproduced by the fork code plus the snapshot preprocessing to 7.8e-7 on every window (G1–G3). So the replicated pipeline is the extraction pipeline within the pre-stated tolerance, and the same constructor with no checkpoint is "the model's own init".
2. G5 shows the gate discriminates: the smallest perturbation (+1 frame) is 46 times above the tolerance.
3. Family C was evaluated by the frozen rule, with δ fixed from the pinned trained effects before any random-init number existed.
   - C3 / C4 TE+: the subject-level drop needs training. At init it is about 0.25, against 5.3–6.0 trained.
   - C1: about half of H1a is present at init, and the training-specific part straddles δ, so INC.
   - C2: two seeds leave a part below δ, so INC.
4. These are read through the consequence map frozen in addendum 07 §7, giving report §5:
   - R2 subject-level drop: learned (keep).
   - R2 token H1a: unresolved.
   - R1 stays descriptive; at init the L1 → L2 rise is equal or larger.
   - R3 is unaffected.

## 3. Caveats

- **δ was chosen by the worker.** PI decision 8 delegated the rule; the PI did not confirm δ. Per sci-pipeline, δ is a PI-only choice. C1 sits on the δ boundary; C3 / C4 would be TE+ for any δ up to about 2.9 (cov) / 4.0 (corr).
- **What "random init" covers.** It is the extraction constructor's default init, not the training run's init (unknown). Only the primary checkpoint was tested; no zoo random init.
- **The thin driver** replaces the PL entry point; equivalence rests on gate G (tolerance, not bitwise).
- **Precision.** The token-level CIs are subject-sampling intervals; seed variation enters only through the per-seed condition.
- **Gate decision.** The gate PASS and the labels are the worker's recommendation; the PI decides (sci-pipeline G9).
- **DISPATCH.md** records the explorer JSON by reference to the three explorer handoffs, not verbatim.
- **Left on connectome:** the venv plus the code / logs / returned dirs (`returned_*` holds only the copied-back aggregates). There are no work dirs with representations. Safe to delete after audit.
- **Ship artifacts.** The scratchpad and /tmp ship staging were removed. The remote `logs/` keep the redacted Slurm output.

## 4. Conclusion

M2H2 is complete.
- H1′: addendum 07 was frozen before any random-init result.
- H2′: the replication gate passed on all 57 × 7 windows; the 10 random-init seeds were run via Slurm; frames and per-subject representations stayed on connectome.
- H3′: fixtures, tests and mutants are in place; the report is at `docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md`.
- Headline: the trained network's subject-level L2 → L3 drop (R2) is training-produced (C3 / C4 TE+). The token-level H1a / H1b training dependence is inconclusive (about half of H1a is present at init). Training lowers the between-subject PR at L1–L3 by 2–6 times; within-window token PR at L2 / L3 is ceiling-limited and close to init.
- Integrated-report input: M2 H2 = tested; R2 subject-level drop "learned"; R2 token H1a "unresolved by H2"; R1 / R3 unchanged.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/addendum_07_sha256.txt
LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_h2 tests/topic3_spectral -q
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 /home/juke/superclaude-env/bin/python3 verification/worker_M2H2_r1/mutants.py      # copied tree; ~3.5 min
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/worker_M2H2_r1/summarize_results.py              # report tables
```

- **Freeze before results:** compare `addendum_07_frozen_utc.txt` (15:57:40Z) with `sacct -j 218064 -X -o Start` on connectome (prints KST: 01:32:19).
- **Gate:** `results/topic3/2026-11-02_h2/gate/gate_record.json` and `gate_decision.json`.
- **Ledger:** the rows for jobs 218063 / 218064.
- **Invalidation conditions:**
  - any vendored file hash changes;
  - the pinned 2026-10-31 outputs change;
  - a rerun of the gate shows rel_fro > 1e-5;
  - the PI sets a different δ (then C1 / C2 must be re-labelled under a new dated addendum, never by editing addendum 07).
