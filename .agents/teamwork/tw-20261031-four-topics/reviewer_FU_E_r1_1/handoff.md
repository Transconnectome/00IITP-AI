# Hard handoff — reviewer_FU_E_r1_1 (FU-E review). Verdict: APPROVE (nonblocking issues listed)

## 1. Observation
- C1: `LC_ALL=C sha256sum -c sentinel/PROTECTED_HASHES.txt` rc 0 before and after (verification/reviewer_FU_E_r1_1/c1_pre.txt, c1_post.txt).
- Tests (CPU, nice, OMP 2): tests/topic2_fu_e 71 passed; old suite (test_empirical_four_topics, test_pilot_connectome, e2e, STRICT_E2E=1) 86 passed; tests/topic1_lagmotif 88 passed; tests/topic2_rgpool 116 passed (logs pytest_*.txt).
- Receipts: FU-E card_sha256 4/4, code_sha256_at_freeze 18/18, output_sha256 12/12 OK; r1 code_sha256_at_freeze, output_sha256_r2, c4_sanitized, addendum_06 0 non-OK. (r1 card_sha256 2 and output_sha256 17 non-OK lines = files later sanitized in r2 and re-pinned in c4_sanitized_sha256.txt; pre-existing, not FU-E.)
- Freeze timeline: card frozen 2026-11-01T16:22:56Z; job 524 submitted 16:24:31Z (main_submit.txt "G3T_CHECK none"), started 17:03:57Z (sacct KST 02:03:57); code files untouched since freeze (18/18).
- `scripts/topic2fu_e_verdict.py run_524/extract.json` reproduces verdict.json and verdict_stdout.txt byte-identically.
- Independent re-implementation (verification/reviewer_FU_E_r1_1/probes/indep_recompute.py, no import of src/topic2_fu_e): provenance 15/15 all checks true, rescore max rel diff 0.0; F+ fails only on S_s2 (Idiff 5.761 vs p95 10.586; alt perm seed p95 10.967); seed means E 16.02 / C 22.71 / S 16.48; F− pass (E −2.91<5.46, C −0.86<3.48, S −1.29<6.28); G2 pass (mean E 61.07); G3 64.13 > 5.91; J1 0.0811 [−0.0660, 0.2281]; J2 0.1500 [0.0980, 0.2021]; verdict inconclusive; with F+ forced pass still inconclusive. Under the pooled readout (probes/indep_recompute_pooled.out) also inconclusive.
- Model input layout: r1 forward() permutes (B,1,D,H,W,T)->(B,1,T,D,H,W) before forward_encoder; FU-E prep.windows feeds (n,1,win,D,H,W) directly to forward_encoder — consistent; zero mask so mask layout irrelevant.
- B300 (read-only ssh, login node): sacct 499 debug gres/gpu=1 8 s; 524 gpu gres/gpu=1 16:43; 551 debug cpu=2 no gres (CPU-only). sha256 of hcp_S_s2, hcp_C_s3 checkpoints, split.json (c13b5f21…), perms_hcp.npz (ec05b796…) equal the pins. No FU-E job queued or running.
- Ledger rows: job 499 started/completed (0.003), job 524 started/completed (0.279), explorers 407/412/420. No row for 551 (CPU-only).
- Own mutants (probes/run_my_mutants.py, mutlogs/my_mutants.json): KILLED R03, R06, R07, R10, R11, R12, R13, R14, R15, R16, R17, R20; SURVIVED R01 primary readout cov2->pooled, R02 fixture readout cov2->pooled, R04 null quantile 0.95->0.99, R05 DELTA 0.01->0.02, R09 F− bound mean->max of p95, R18 rescore relative->absolute diff, R19 perm_ok ignores run.json perm_sha256, R21 t interval 95%->90%.
- audit_layout.py on whole run root: PASS, findings [], rc 0. Local C4 pattern scan of 50 FU-E files: 6-digit tokens only in count fields (n_features, n_vox, n_common_mask_vox); no sub- labels, no subject paths.

## 2. Logic Chain
1. F1: card is dated, frozen with receipt before any real-data FU-E result (timeline above), states change/arms/seeds/budget/metric/δ = 0.01/stop rule, reuses r1 t_interval and fixture generator. Met.
2. F2: code only in FU-E paths; synthetic fixtures fail on the targeted defects (subject-mask anatomy confound, iid null, surrogate); verdict tests cover V01–V11 analogues incl. V06–V10 classes (worker 29/29 and my 13 kills). Surviving mutants are outside V06–V10 (readout wiring, constants, provenance sub-checks) and none changes the shipped verdict: all 8 leave inconclusive (F+ S_s2 fails at any quantile ≥ 0.95; pooled computed numerically; provenance values are exact 0.0 / equal hashes). Shipped behaviour is pinned by the code freeze receipt and byte-identical verdict recomputation. → nonblocking regression-guard gaps.
3. F3: Slurm only, 0.297/1.5 GPU-h, ledgered, results in dated dir, report states verdict per card §8 and its effect on r1 stop (none governed). Met.
4. C1–C8: verified above; C5 B300-share check failed for smoke 499 (ssh broken pipe) but was disclosed with sacct evidence of no conflicting job → procedural deviation, nonblocking.
5. Verdict inconclusive is the correct card outcome and is robust to every counterfactual tested; no integrity violation found (no hardcoded results, verdict recomputed from raw record by independent code).

## 3. Caveats
- R matrices were not regenerated on GPU (decision value low: verdict inconclusive under all counterfactuals). B300 ID scan content not re-run (names exist only on B300).
- F+ strict per-encoder rule includes the known-stalled S_s2 (disclosed before freeze), so F+ failure was foreseeable; J1 alone would also be inconclusive.
- Random-init twins already identify every subject (acc 1.00, Idiff ~54); G2 therefore checks data capacity rather than learned capacity. Descriptive readings in report §2 are interpretive.

## 4. Conclusion
APPROVE FU-E: verdict `inconclusive` (F+ measurement-capacity gate failed on hcp_S_s2) is correctly derived, reproducible and independently confirmed; all ACCEPTANCE criteria met with evidence. Nonblocking: (a) 8 surviving mutants (test helpers set cov2 == pooled, hiding readout wiring; constants/CI level/rescore-abs/perm-run.json unguarded by tests); (b) card §3/§12 split.json/perms file sha are recorded in extract.json but not gated by verdict.evaluate (values match); (c) fixture conditions not size-checked (n_expected only for main; actual 24); (d) worker return claims a ledger row for CPU srun 551 — none exists, none needed; (e) smoke 499 submitted after a failed squeue check (disclosed); (f) stale src/topic2_fu_e/__pycache__ (pre-freeze, harmless).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-02_fu_e/card_sha256.txt | LC_ALL=C sha256sum -c
LC_ALL=C sha256sum -c results/topic2/2026-11-02_fu_e/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-02_fu_e/output_sha256.txt | LC_ALL=C sha256sum -c
/home/juke/superclaude-env/bin/python3 scripts/topic2fu_e_verdict.py results/topic2/2026-11-02_fu_e/run_524/extract.json /tmp/v.json && cmp /tmp/v.json results/topic2/2026-11-02_fu_e/verdict.json
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_FU_E_r1_1/probes/indep_recompute.py results/topic2/2026-11-02_fu_e/run_524/extract.json
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_fu_e -q
/home/juke/superclaude-env/bin/python3 -I verification/reviewer_FU_E_r1_1/probes/run_my_mutants.py   # uses mut_tree copy; recreate data symlinks first (results, docs, .agents, verification/worker_FU_E_r1)
```
Invalidation: any receipt mismatch, verdict.json not reproduced, or a mutant that flips the shipped verdict.
