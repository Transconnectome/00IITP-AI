# handoff — reviewer_M2_r1_1 (M2 Topic 3), 2026-10-31T11:55Z — HARD handoff

## Review Summary
**Verdict: APPROVE** (no blocking issues; 7 non-blocking findings below, 1 Major).

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` → rc 0, 67/67 OK at start (verification/reviewer_M2_r1_1/c1_start.log) and after all test runs (c1_end.log).
- Pins: `sha256sum -c results/topic3/2026-10-31/output_sha256.txt` rc 0 (start and end, output_pins_end.log); `code_sha256_at_freeze.txt` all OK except `scripts/topic3_launch_connectome.py` (FAILED, disclosed in addendum 01 item 2); `addendum_02_sha256.txt` OK; card sha256 = 683374565d80…e0 = card_sha256.txt.
- C2: tests/topic3_spectral 54 passed rc 0 (pytest_topic3.log); tests/topic1_lagmotif 88 passed rc 0; STRICT_E2E=1 old suite (tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e) 86 passed, 7 warnings, rc 0.
- C3 order: card frozen 08:48:29Z; family_A run record started_utc 08:49:18Z, family_B 09:01:59Z, token jobs 08:53–08:58Z (file mtimes, KST+9); both scripts recorded `card_sha256_verified` = frozen hash; every code_sha256 in family_A/B run records and in all 4 connectome job records equals code_sha256_at_freeze.txt (0 mismatches). Pre-card files (t3_1_provenance_repro.json 08:31Z, alpha_calibration_synthetic.json 08:40Z) are reproduction/synthetic only; explorer probes listed in card §11 are synthetic or descriptive, consistent with the exposure statement.
- Independent recomputation (own SVD code, verification/reviewer_M2_r1_1/indep_recompute.py → .out.json): covPR, corrPR, uncentered PR of all 7 pinned matrices equal the JSON/report to 4 decimals (e.g. L2 11.0202/13.1879/1.0743, L3 3.5786/4.7793/1.0327); H1a/H1b mean log ratios for all 4 checkpoints equal JSON (+0.0228/+0.0447, −0.1368/−0.1130, +0.0378/−0.0330, +0.0489/+0.0792); my own 20 000-draw sign-flip gives 0 exceedances in all 8 cases; PR recomputed from stored float32 eigenvalues matches stored PR (max rel err 2.4e-8).
- Independent connectome spot check (own .pt reader + own estimators, srun node2, CPU, connectome_spotcheck.py/.out.txt): primary checkpoint positions 0 and 56: corrPR_L3, corrPR_LN0L2, covPR_L3, covPR_L2 = 6.149112/6.086166/5.693144/5.571642 and 6.143517/6.059468/5.677526/5.553756 — identical to 6 decimals with token_job/E192_primary_token_spectra.npz.
- Replication rule hand-applied to JSON: H1a primary sig, agreeing zoo = {deepE192_L1e-4, deepE192_L5e-5} → "holds"; H1b agreeing = {deepE192_L5e-5} → "not replicated". Matches H1_replication_verdicts.
- Architecture: ver11 sha de132387…052a; lines 914–923 (blocks then downsample), 1068 (`downsample=… if i_layer < num_layers-1 else None`), 1382–1412 (final `self.norm` only after last stage, permute to (C,D,H,W,T)) confirm no PatchMerging between layer_2 and layer_3. Zoo table `extract_vrabes_swift_zoo.sh` lines 48, 54–55 confirm addendum 02 depths (HCP_N400 `2 2 18 2` last.pt L2e-5; deep `2 2 42 4` EP10.pt / best.pt).
- Report tables (E1, A1, A1b, A2, H1, H1c–e, H4, α) all match the JSON; H4 "L1→L2 increases in 3 of 4" verified.
- C4 IDs: VRABES ids are `sub-` + 4 digits (format class only). Full-ID string scan over 141 M2 files (results/topic3, docs/topic3, src/tests topic3, scripts/topic3_*, worker/reviewer metadata, worker/explorer/reviewer probes): 0 hits. Boundary-delimited 4-digit matches only inside binary npz float bytes (noise).
- C7: VRABES `git status --porcelain` empty; no file under VRABES/RemissionAnalysis or SwiFT_v2 models newer than 2026-10-31 00:00.
- Own mutants (reviewer_mutants.py → reviewer_mutants.out.json, scratch copy only): killed R2 (zoo p ignored), R4 (SE √(m/n)·0.5), R5 (one-sided sign flip), R6 (D2 wrong tail), R10 (rank cap n), R11 (LN eps 0.1). **Survived: R1 replication ignores sign, R3 primary ignores CI, R7 jackknife missing (n−1) factor, R8 Holm threshold 0.5, R9 H1a pair swapped to (L3, L2).** Worker's own 9 mutants (verification/worker_M2_r1/mutants.out.json) all killed.
- git: 12 commits today on feature/topic1-lag-motif-v2, all "docs(iitp): checkpoint four-topics teamwork documents", automatic 15-min background checkpoint from the root session (message: "Code, data and results are not included").
- results/gpu_ledger_2026-10-31.md does not exist.
- git timing evidence: commit 24fe976 (2026-10-31 17:46:25 KST = 08:46:25Z) holds the card with sha256 683374565d80…, i.e. the frozen content existed in a timestamped commit before family A (08:49Z) and the token job; the card blob at HEAD 12ab7d1 is the same. Today's commits touching M2 paths (docs only): 24fe976 (card, provenance), 70d0ed6 (addendum 01, earlier wording), 01dfc76 (addendum 01 revised, result report), 7497e6a (addendum 02). Addendum 01 was revised between 18:01 and 18:07 KST to correct its own wording (job host vs compat-check host; full failed-submission receipts); it is not a frozen file.
- sci-pipeline SKILL.md G8/G9 read: G8 taxonomy keep/modify/stop/inconclusive/no_candidate + failure types; G9 state separation; reviewer verdict is advisory, PI decides gate passage.

## 2. Logic Chain
1. Protected files unchanged (C1) and all suites pass (C2) — observed directly.
2. The card governing new results was frozen before any governed real-data run, the scripts verified its hash, and the executed code is byte-identical to the frozen code (C3, T3.2) — run records + freeze record.
3. The numbers are real and correctly derived: own-code recomputation of subject-level values and token-level contrasts matches; an independent read of raw frames on connectome reproduces stored token spectra; the repool provenance check (max |Δ| ≤ 4.8e-7) ties frames to npz (T3.4).
4. T3.1 satisfied: inputs located read-only with sha pins and producer provenance; PR≈1 explained as the uncentered SVD (mean-energy 96–99.9%) with a fixture (old uncentered < 1.1, centered = k); reproduces public numbers to 4 dp.
5. T3.3 satisfied: known-rank fixtures (PR = k to 1e-9, analytic unequal spectrum), α fixtures (rank slope exact; Clauset recovers Pareto α within 0.05; finite-n bias guard), centering defect caught; worker mutants for these defects are killed.
6. Verdicts follow the card rules (hand-applied). Claims stated hold/fail per §7 with addendum 02 limiting H1a to "not replicated at matched architecture".
7. The surviving mutants show the verdict-rule code is not pinned by tests; one (R1) would flip H1b to "holds" on the real data. Because the code that actually ran is correct (read + hash-matched) and the verdicts were re-derived by hand, this is a test-coverage gap, not an incorrect result → Major, non-blocking.

## 3. Caveats
- I did not rerun the full scripts in a copied tree (values were instead recomputed with my own code and spot-checked on connectome; that is stronger for correctness, weaker as a byte-level reproduction of the run records).
- Spot check covers 2 of 57 subjects for 1 of 4 checkpoints; zoo checkpoints have no npz re-pool check (no pins exist for them), only a same-subject-set check.
- NERSC extraction fork not diffed against local ver11 (disclosed by worker); zoo training details come from VRABES scripts only.
- I did not read reviewer_M2_r1_2's handoff (kept independent).
- Card exposure statement (§11) checked against probe files on disk only; scratch computations outside the repo cannot be audited.

## 4. Conclusion
APPROVE M2. All of C1–C8 that apply to M2 and T3.1–T3.4 are met with evidence. Non-blocking:
1. [Major, test-coverage] 5 surviving verdict/inference mutants (R1, R3, R7, R8, R9). Add an additive test file (e.g. tests/topic3_spectral/test_verdict_rules.py) with: opposite-sign significant zoo checkpoints must not count; primary with CI spanning 0 → "killed"; Holm threshold; H1a pair identity; jackknife SE vs analytic SE of the mean. Do not edit pinned files.
2. [Minor] H2 random-init control untested (T3.2 lists random-init as an example; shuffled null present). Any training-vs-architecture reading of the subject-level drop remains unlicensed.
3. [Minor] Result report §6 reproduction commands overwrite pinned outputs; superseded by addendum 02 §2 — readers must be pointed at addendum 02.
4. [Minor] Result report R2 row says "token-level collapse FAILS" and "2 stage-3 blocks"; the only depth-matched zoo checkpoint (HCP_N400) shows a 13% token-level drop. Addendum 02 states this; any downstream summary must carry it.
5. [Minor, run-level, not M2] results/gpu_ledger_2026-10-31.md absent; M2's 0 GPU-h should be logged by the ledger owner.
6. [Run-level, not M2] C4 run-level violation unless the human authorised the background checkpoint: 12 automatic commits today from the root session (trailer carries the root Claude-Session URL), 4 of them touching M2 docs (24fe976, 70d0ed6, 01dfc76, 7497e6a). Root must confirm authorisation. No M2 agent committed, and none can undo it under the no-reset rule.
7. [Minor] verify_card() gating in scripts is not unit-tested (evidence of gating is only in run records).
8. [Minor, methodology] Card/report verdict labels (holds / not replicated / killed / FAILS / REPRODUCES DESCRIPTIVELY / UNTESTABLE / NOT SUPPORTED / not comparable) are not mapped to sci-pipeline G8 (keep/modify/stop/inconclusive/no_candidate). They map cleanly (holds→keep; not replicated→inconclusive; killed/FAILS→stop; UNTESTABLE/UNTESTED→inconclusive with failure type "measurement capability"; execution failures are kept separate per card §10), and the card froze them first, so non-blocking; a one-line mapping in a future addendum would close G8. G9 state separation is met (reproduction vs synthetic vs real-data effect stated separately; no clinical or external-replication claim).
9. [Minor] test_outputs_no_ids.py only scans for the b"sub-" prefix; a bare 4-digit ID would pass. My boundary-aware scan of the real ID set found none.
Emphasis on finding 1: test_token_contrast_and_replication_rule claims to test the replication rule but never checks sign; the R1 mutant flips H1b to "holds" on the real data. The APPROVE for the verdicts therefore rests on my hand derivation from the JSON plus reading the hash-matched shipped code, not on the test suite.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
sha256sum -c results/topic3/2026-10-31/output_sha256.txt
sha256sum -c results/topic3/2026-10-31/code_sha256_at_freeze.txt   # only topic3_launch_connectome.py fails (addendum 01)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic3_spectral -q
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -I verification/reviewer_M2_r1_1/indep_recompute.py
TMPDIR=<scratch> PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/reviewer_M2_r1_1/reviewer_mutants.py   # survivors listed
ssh connectome "srun -p debug -w node2 -c 2 -t 00:08:00 --nice=100 python3 -" < verification/reviewer_M2_r1_1/connectome_spotcheck.py
```
Invalidation: any change to the card hash, any pinned output, or any analysis-code hash; a survivor-killing test that reveals the shipped verdict logic differs from the card.
