# worker_M2_r1 — handoff (Hard), M2 Topic 3 (T3.1–T3.4)

## 1. Observation

**Code.** All of it is new and lives in paths I own.
- `src/topic3_spectral/{__init__,estimators,resampling,io_contract,token_job,analysis}.py` — numpy only, Python 3.8-compatible.
- `scripts/topic3_{provenance_repro,alpha_calibration,common,subject_level,token_job,launch_connectome,token_stats}.py`
- `tests/topic3_spectral/` — 11 files, 54 tests.
- Probes: `verification/worker_M2_r1/{mutants.py, mutants.out.json, py38_compat_check.py, py38_compat_{local,connectome}.out.json, syn_tiny.pt, syn_tiny_ref.npz}`.

**Docs** (`docs/03_empirical_analysis/topic3/`):
- `2026-10-31_topic3_provenance.md` (T3.1)
- `2026-10-31_topic3_analysis_card.md` — FROZEN, sha256 `683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`, at 2026-10-31T08:48:29Z
- `2026-10-31_topic3_addendum.md` (2 deviations + failed-submission receipts; submit log overwritten, disclosed)
- `2026-10-31_topic3_result_report.md`

**Results** (`results/topic3/2026-10-31/`):
- `card_sha256.txt`, `code_sha256_at_freeze.txt`, `output_sha256.txt`
- `t3_1_provenance_repro.json`, `alpha_calibration_synthetic.json`
- `family_A_subject_level.json`, `family_B_token_level.json`
- `token_job/` — 4 checkpoints × {npz, json}
- `logs/`

**Order of work.** Provenance reproduction ran first; it used only already-public numbers. Then the synthetic calibration, then the fixtures. The card was frozen at 08:48:29Z. Family A started after that and finished in 26 s. Slurm job 217845 then ran on connectome node2, about 2 min per checkpoint. Family B statistics ran last.

**T3.1 reproduction.** Every number in the report table and the json reproduces to 4 dp. The report used the centered `eca.estimate_powerlaw_alpha`; the json used the uncentered `srg.compute_participation_ratio`. The mean vector holds 96.45–99.92% of the energy. Fixture: rank-k plus a 30-SD offset gives new PR = k (1e-9), while the old uncentered estimator gives < 1.1.

**Contract checks on connectome.** All passed:
- the npz copies match the pins;
- the npz row order equals the sorted frame directories;
- all 57 subjects re-pool to their npz rows, with max |Δ| ≤ 4.8e-7;
- the 3 zoo subject sets equal the primary's;
- every subject has 7 frames.

**Family A (subject level).**
- ΔPR₂₈(L2−L3): cov +5.34 [3.23, 7.46], corr +6.04 [4.28, 7.80]. D1 = "drop robust, not a per-channel-scale effect".
- A1b, the LN-matched subject-level contrast (pooled L3 vs pooled LN0(L2)), is negative in all 4 checkpoints (corr −6.08, −7.64, −1.36, −3.29).
- D3: ordering at matched n = 25 reproduces. The ratios are about 1.8× and 2.3× (descriptive; the card makes no magnitude verdict).
- Subject-level α is not estimable: synthetic Clauset bias reaches +3.4.

**Family B (token level, subject = unit).** Mean log ratios for H1a, corrPR(L3) vs corrPR(LN0 L2):

| Checkpoint | H1a mean log ratio |
|---|---|
| primary | +0.023 |
| HCP_N400 | −0.137 |
| deep L1e-4 | +0.038 |
| deep L5e-5 | +0.049 |

All Holm p = 0.0002, which is the permutation floor 2/(B+1). The rule gives "holds", direction "L3 higher".

H1b, covPR(L3) vs covPR(L2), is "not replicated": +0.045 / −0.113 / −0.033 / +0.079.

Token PR is about 6 of a 1119 ceiling.

**Final checks:**
- topic3 tests: 54 passed.
- Old suite: 86 passed (170 s).
- topic1: 84 passed.
- Mutants: 9/9 killed, with the control passing.
- C1: `sha256sum -c` rc 0.
- Layout lint: findings [].
- `grep` for the subject-ID prefix over outputs, docs and probes: no hits. The only hit is the subject-directory prefix literal in the code of `scripts/topic3_token_job.py`.
- No running processes or jobs.
- GPU-h: 0. Nothing sent to B300.

## 2. Logic Chain

1. The json's PR ≈ 1 comes from the uncentered SVD (O: reproduction + mean-energy fraction + fixture), so J1 is an artefact.
2. The re-pool equality for all 57 subjects proves the frames are the npz source and that the positions align, so token results can be attributed to the same subjects.
3. The subject-level L2 > L3 survives corrPR (gain and bias removed) and LN matching in 4/4 checkpoints. So the drop is real at between-subject level and is caused by the stage-3 blocks, not the final LN gain. PatchMerging cannot be the cause, because ver11 has no merge there.
4. Token-level within-window dimensionality does not drop. H1a replicates in sign for 3/4 checkpoints as a +2–5% *increase*. So the "collapse" is not a loss of token-representation dimension. It is a reduction in the dimensionality of between-subject differences of pooled means.
5. The cross-model ordering holds at matched n, but its size was inflated by comparing n = 25 against n = 57, and its attribution is confounded by pooling, D and training data.

## 3. Caveats

**Deviations.** Placement moved from node1 to node2 because of cluster policy, and the launcher got a `%`-escape fix after the freeze. Both are in the addendum. No analysis code changed: `code_sha256_at_freeze.txt` verifies everything except the launcher.

**Exposure.** The subject-level direction was seen before the card, so it is pre-specified, not blind.

**Not done:**
- Random-init H2 is untested; the card deferred it.
- Graph metrics are out of scope.
- The NERSC fork was not diffed.
- LN γ/β were not read.

**Interpretation limits.** Token-level effects are tiny and their sign depends on the checkpoint (HCP_N400 reverses both). The synthetic α calibration uses iid rows, which real tokens are not.

**Leftovers on connectome:**
- node1 `~/iitp4_topic3_m2_20261031/` holds the code from the refused first submission plus the sbatch file.
- node2 `~/iitp4_topic3_m2_20261031/{code,logs,out}` holds outputs that are byte-identical to the copies collected locally.
- I left both for audit. They contain code and position-keyed summaries only.

**Metadata.** DISPATCH.md omits the ~25 KB explorer JSON array and points to the three explorer handoffs instead.

## 4. Conclusion

M2 T3.1–T3.4 are delivered.

| Claim | Verdict |
|---|---|
| J1 | Fails (artefact) |
| R1 | Reproduces descriptively; no verdict (D-confounded per card §4) |
| R2 | Mechanism fails; subject-level drop holds; token-level collapse fails (opposite sign, small) |
| R3 | Ordering holds at matched n (ratios about 1.8×/2.3×, descriptive); attribution untestable |
| R4 | Not supported (category error) |
| R5 | Untestable |
| R6 | Not supported, out of scope |
| R7 | Not comparable |
| H2 | Untested |

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # rc 0
sha256sum -c results/topic3/2026-10-31/code_sha256_at_freeze.txt     # only scripts/topic3_launch_connectome.py differs (addendum #2)
sha256sum docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md                      # 683374565d80…
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_spectral -q   # 54 passed
STRICT_E2E=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e -q   # 86 passed
TMPDIR=<scratch> PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/worker_M2_r1/mutants.py   # survivors []
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 scripts/topic3_subject_level.py && …/topic3_token_stats.py   # deterministic seeds: result values match; file hashes differ because of the started_utc/runtime fields
```

**Invalidation conditions:**
- the card hash changes;
- any input pin fails;
- the re-pool check fails on a rerun of the token job;
- a mutant survives.
