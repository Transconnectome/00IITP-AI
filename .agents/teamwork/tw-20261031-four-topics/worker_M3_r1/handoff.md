# handoff — worker_M3_r1 (M3 / Topic 2) — HARD, 2026-11-01T05:35Z

T2.1, T2.2 and T2.3 are complete. **The card's verdict is `stop` (killed).** Both fixture gates passed.
- Primary report: `docs/03_empirical_analysis/topic2/2026-11-01_topic2_result_report.md`.
- Card: `docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md` (sha256 c9bfc60af87f45d4541f10b1f5e074215e235d3e4fd99f001f69f8d8585c41f5), frozen at 03:14:34Z before any real-data statistic.
- Addenda 01–04 sit next to it.

## 1. Observation

**T2.1 (code).** The vendored ver11 is byte-identical to SwiFT_v2 f0dc7aca (sha256 de132387…052a).
- `PatchMergingV2` (lines 41–88) concatenates 8 children in slot order `product(range(2),repeat=3)` (line 81), then applies LN(8C) and Linear(8C→2C) (lines 72 and 85).
- A merge sits at the end of stages 0–2 only (line 1068), so there is no merge between `layer_2` and `layer_3`.
- Per-stage input resolution (lines 1042–1049): E36 runs 20×16³ → 8³ → 4³ → 2³ at widths 36/72/144/288.
- The decoder is hard-coded `'mlp'` (line 1112) and is per-token. Each final token decodes only its own 48³ octant (test).
- `use_post_norm=True` crashes (test).
- Patch-embedding token order equals the cell index (d·16+h)·16+w (test and probe `verification/worker_M3_r1/probe_token_order.out.json`).

**T2.2 (implementation).** Package `src/topic2_rgpool/` with modules `grid`, `partition`, `merge`, `model`, `data`, `fixtures`, `metrics`, `stats` and `train`, plus `vendor_swift_ver11/` with `SOURCE.md`.
- `ConnectomeRGBoxPooling` is a parameter-free per-frame gather in front of stock PatchMergingV2, injected through ver11's `downsample` callable.
- Arms:
  - E: identity.
  - C: octant-local size-8 dense-core, mean-linkage growth on the train group FC in correlation distance.
  - S: the same builder on an FC permuted within distance bins inside each octant, one surrogate per seed.
  - G, R: descriptive only.
- Placement uses Hungarian matching of centroids, with a canonical Hungarian slot order.
- Tests: `tests/topic2_rgpool/`, 55 tests, final run `55 passed` (`verification/worker_M3_r1/final_tests_topic2.txt`).

**Data.** HCP-YA S1200 open access REST1_LR hp2000_clean on B300 .98, read-only.
- 93 files found; 5 burned dev subjects excluded in memory; 88 passed QC, 0 failed.
- Manifest sha 26ba34a9…96d5. Split 64 train / 8 val / 16 test, `split.json` sha c13b5f21…0262.
- Preprocessing follows SwiFT S1200: crop and pad, then a per-voxel z-score.
- Subjects are identified only by a file-content sha256 prefix.

**Train-only partitions** (`results/topic2/2026-11-01/partitions/partitions_hcp.json`): 1,195 signal cells and 234 touching M0 blocks. C regroups 231 blocks (dispersion 1.47 cells), S 231–232 (1.56–1.67), E 0.

**Fixture gates** (B300, 12 runs, full budget).

| fixture | E | C | S | gain C vs E | gain C vs S | result |
|---|---|---|---|---|---|---|
| F+ | 0.6786 | 0.6578 | 0.6777 | +3.06 % | +2.93 % | PASS |
| F− | 0.2393 | 0.2435 | 0.2437 | −1.74 % | — | PASS (C not better) |

CPU Stage-0 fixtures: on F+ the C purity is 1.00, and the periphery/max growth rule fails the purity test as required. F− and NULL pass.

**Stage 1** (15 runs; `results/topic2/2026-11-01/verdict.json`).
- Seed-mean test NMSE: E 0.98892, C 0.98747, S 0.99218.
- I1 = +0.15 %, 95 % t interval [−0.07 %, +0.36 %] (df 4); bootstrap [+0.02 %, +0.29 %].
- I2 = +0.47 %, interval [+0.001 %, +0.95 %]; bootstrap [+0.26 %, +0.82 %].
- Rule applied: **stop**, because the upper bound of I1 is below δ = 1 %.
- Run `hcp_S_s2` stayed at the trivial solution (test NMSE 1.0000). It counts as valid under card §5. A post hoc rerun of the analysis without seed 2 gives I1 [−0.10 %, +0.26 %] and I2 [+0.16 %, +0.45 %]; still stop (addendum 04).

**Stage 0** (descriptive, `results/topic2/2026-11-01/stage0_hcp.json`):
- C − S: r +0.071, pca2 +0.031, both in 16/16 subjects.
- C − E: r +0.004 [0.0005, 0.0074], higher in 11/16 subjects.
- C − E: pca2 −0.052, lower in 16/16 subjects.

**GPU.** worker_M3_r1 used 11.73 GPU-h on node .98: smoke 0.04, then waves of 3.41, 3.43, 3.50 and 1.35. Every launch has a started and a completed ledger row in `results/gpu_ledger_2026-10-31.md`. Run-wide total from completed ledger rows: 11.872 GPU-h.

**Checks at 05:3xZ** (outputs in `verification/worker_M3_r1/final_*.txt`):
- old suite: 86 passed;
- new suite: 55 passed;
- C1 `sha256sum -c` PROTECTED_HASHES: rc 0, 67/67 OK;
- code-freeze check: rc 0, all 33 files;
- card and frozen-input check: rc 0;
- B300 ID scan: 175 text files, 0 hits (`results/topic2/2026-11-01/id_scan_b300.json`);
- whole-run `audit_layout.py`: PASS, 192 files inspected, 0 findings, rc 0.

**Hygiene.**
- No `topic2_*` process remains on B300, and all 8 GPUs were idle at the final check.
- No git writes.
- No installs on DGX-Spark.
- `~/enigma_ocd` was never listed or read, and `~/envs/swiftllm` was not used.

## 2. Logic Chain

1. Stages 1–3 need a regular token grid, and M0 is the only merge with room to regroup. So the redesign regroups cells at M0 with a gather. Bit-identity with PatchMergingV2 under the identity π makes E the exact stock baseline. Parameters, tokens, FLOPs and initial weights are equal by construction and by test. The single manipulated factor is π.
2. The decoder and the M1/M2 merges are organised by octant, so boxes must stay inside one octant, or connectivity would be confounded with architectural penalties.
3. Distance decay is part of FC. The S null keeps distance decay and destroys FC specificity, so I2 isolates the connectome-specific contribution.
4. G6: the F+ gate shows that the loop and gather turn a strong planted grouping into a gain of at least δ at this budget. The F− gate shows no spurious C advantage. Running Stage 1 was therefore warranted under the card.
5. Stage 1: I1's upper bound (+0.36 %) is below δ (1 %), so card §8 gives `stop`. I2's lower bound is above 0, so C is better than the **distance-matched null** S. The size is tiny, about 0.3–0.5 % NMSE.
   - This is not a gain beyond E: the seed-mean S NMSE (0.99218) is worse than E's (0.98892).
   - So I2 > 0 mostly reflects C avoiding the cost that non-compact, FC-uninformed grouping imposes. That matches Stage 0, where C is about equal to E and well above S.
6. Every arm sits at NMSE ≈ 0.987–0.992. This was noted in addendum 02 before Stage 1 ended. So the kill holds for this target and budget. It is not a general negative about connectome grouping.

## 3. Caveats

- **C6 / HCP.** It needs **PI confirmation** that HCP-YA Open Access counts as "public". The data were staged by another workstream, used read-only, and no HCP data left B300. The fallback is ds000228.
- **δ = 1 %** was set by the worker, not the PI. Full intervals are reported so the result can be re-read.
- **Low reconstruction ceiling.** The models explain about 1 % of the masked per-voxel variance. The F+ gate tests sensitivity on a synthetic signal at 12 mm cell level, not on voxel-noise-dominated BOLD.
- **Single setting.** One small configuration (E36, 140k samples, no tuning). No E192 run, no downstream task.
- **Stalled run.** One S run stalled (addendum 04). It is valid per the card; both claims are robust to dropping it.
- **Card ambiguity.** The §9 joint reading had two ambiguities (addenda 02 and 03). All four combinations are reported, and none is chosen.
- **Splits.** HCP family structure is unavailable, so relatives may straddle splits.
- **C4 disclosure.** My regex self-check (about 03:32Z, right after the token-order test was added; local tool output only) printed one real-format HCP example ID literal: a well-known example from public HCP documentation, typed by hand and not derived from data. It was not written to any file, and the B300 ID scan of all outputs found 0 hits.
- **Post-scan edits.** The final B300 ID scan (05:2xZ) ran before the last edits to `handoff.md`, `BRIEFING.md`, `progress.md`, `DISPATCH.md` and the result report (I2 scope sentence). Those files were checked locally for any standalone 6-digit token. The only hit was `ds000228`, the OpenNeuro dataset accession, which is not a participant ID.
- **Explorer salt.** explorer_M3_r1_1's salt file still sits next to its salted dev-subject hashes in `verification/explorer_M3_r1_1/`, and HCP IDs can be brute-forced. I did not propagate those hashes. Root should decide whether to move the salt.
- **Left on B300** `/scratch/iitp4/worker_M3_r1/`, which is ephemeral and wiped on VM stop: about 133 GB of preprocessed HCP (`hcp/`), 15 Stage-1 checkpoints (`runs/hcp_*/model_final.pt`), the group FC (`partitions/fc_train_group.npy`), the venv, smoke synthetic data and the ID-scan copies. Remove with `rm -rf /scratch/iitp4/worker_M3_r1` once no longer needed. I did not delete them.
- **SSH.** The ProxyJump to B300 was intermittently flaky (broken pipe or banner timeout). It affected only polling; all copies were verified by `run.json` status and hashes.
- **Not inspected.** The perlmutter SwiFT fork.

## 4. Conclusion

M3 is delivered. T2.1 is documented from code: three 2×2×2 merges, none after stage 3, so the old premise is false.

T2.2 consists of:
- a frozen card;
- a matched `ConnectomeRGBoxPooling` implementation;
- 55 tests, with mutants;
- fixtures where RG should help (F+) and where it should not (F−).

T2.3 was run on B300 within the cap (11.73 GPU-h). Verdict per the card: **stop**. At ver11 E36 / 140k samples on HCP-YA, connectome boxes at M0 give no practically relevant (≥ 1 %) NMSE gain over PatchMergingV2: +0.15 % [−0.07, +0.36]. They do beat a distance-preserving FC-shuffle null by a small margin: +0.47 % [+0.001, +0.95].

The escape clause was not needed. Costed options for a more sensitive follow-up are in report §7; they need a PI decision and a new card.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
grep -v '^#' results/topic2/2026-11-01/card_sha256.txt | sha256sum -c
sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool -q
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q
/home/juke/superclaude-env/bin/python3 -B scripts/topic2_verdict.py results/topic2/2026-11-01/runs /tmp/v.json   # recomputes gates + verdict
python3 /home/juke/git/chavis/skills/teamwork/scripts/audit_layout.py .agents/teamwork/tw-20261031-four-topics
```

- **Inspect.** The `results/topic2/2026-11-01/runs/*/run.json` files: 27 governed runs. Each records `code_sha256`, which equals the freeze list, and `perm_sha256`.
- **Ledger.** The worker_M3_r1 rows in `results/gpu_ledger_2026-10-31.md`.
- **This handoff is invalid if** any of the following holds:
  - any of the hash checks fails;
  - a run's `code_sha256` differs from the freeze list;
  - `verdict.json`, recomputed, differs;
  - the ID scan, rerun on B300 with `scripts/topic2_id_scan.py`, finds a hit;
  - the PI rules that HCP Open Access is not "public" under C6.
- **Layout lint.** Whole-run `audit_layout.py` at 05:3xZ: PASS, 192 files inspected, 0 findings, rc 0 (`verification/worker_M3_r1/final_audit_layout.txt`).
