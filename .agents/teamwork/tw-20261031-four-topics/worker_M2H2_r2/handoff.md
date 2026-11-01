# Handoff (Hard) — worker_M2H2_r2, M2H2 iteration 2 (Topic 3 H2 random-init control)
Written 2026-11-01T20:05Z. Parent: root coordinator 5fddb83e.

## 1. Observation
- r1 gate FAIL came from challenger_M2H2_r1_2 REFUTED on test coverage only (verdict-path wiring N26/N53 flip C1, every stats-script guard N50–N59 untested); the other four verifiers APPROVE/CONFIRMED/CLEAN and all five reproduced the shipped verdict.
- results/topic3/2026-11-02_h2/output_sha256.txt (61 entries) pins src/topic3_h2/**, scripts/topic3h2_*.py, the 8 shipped tests, addendum 07, the result report and all outputs -> nothing there may change.
- New files (only additions):
  - tests/topic3_h2/test_h2r2_stats_regression.py (6 tests; sha 3ac6331e…) — copied-tree subprocess regression of `gate` / `final` vs shipped JSON (all leaves except top-level `run`, floats rel 1e-12); modified-addendum refusal; output receipt entries verify.
  - tests/topic3_h2/test_h2r2_stats_guards.py (26; sha cedb50ea…) — in-process, OUT redirected to staging copy; one corrupted input per guard.
  - tests/topic3_h2/test_h2r2_family_oracle.py (11; sha 221cb3c7…) — heterogeneous K=10 seeds vs hand oracle (collapse to seed 1 changes C1/C3 INC->EQ); Family L key order/test seeds; per-seed D1 rule; strict ±δ seed boundaries.
  - tests/topic3_h2/test_h2r2_gate_components.py (53; sha 1f201b44…) — stats_match relative / 30 cells / dropped counts; contrast_status; negative control 0 windows; card index sets = job-recorded sha; subset_prs corr; forbidden-key guard via SCALAR_KEYS patch; driver gate_checks G2 tol and G3 contrast status (real-arithmetic construction); negative_controls all-vs-any; early duplicate window; _run with fake model module (seed hashes, checkpoint load).
  - results/topic3/2026-11-02_h2/r2/2026-11-02_topic3_h2_addendum_08_r2.md (sha 3bb27032…, read-only) + r2/addendum_08_sha256.txt (addendum + 4 tests; rc 0).
  - 2 UTC correction rows appended to results/gpu_ledger_2026-10-31.md (flock on .lock); prior ledger bytes in verification/worker_M2H2_r2/prev_snapshot/ (sha 9f9843eb…).
  - verification/worker_M2H2_r2/: union_mutants.py (+ .out.json sha 2f38f617…, logs/union_mutants.log), delta_sensitivity.py(.out.json), single_seed_labels.py(.out.json), trunc_normal_clamp_probe.py(.out.txt), logs/pytest_*_final.log.
- Union harness (verbatim mutant definitions from the 6 r1 harnesses): 125 definitions, 115 distinct edits; both copied-tree baselines green (shipped 71 passed, extended 167 passed); 115/115 killed by the extended suite; the 37 r1-survivor edits (incl. W3/W4/W7) each SURVIVED the shipped 8-file suite in FULL and were KILLED by the 4 new files alone; 0 invalid runs; 0 restore failures; shipped h2_results.json / gate_decision.json unchanged.
- Final checks: tests/topic3_h2 167 passed 0 skipped; tests/topic3_spectral 138 passed; old 86 passed (STRICT_E2E=1); tests/topic1_lagmotif 88 passed; C1 rc 0; H2 output_sha256 rc 0; addendum_07 receipt rc 0; addendum_08 receipt rc 0; 2026-10-31 receipts rc 0 except the two known cases (card_sha256.txt trailing token, hash 683374565d80… matches; code_sha256_at_freeze.txt launcher, addendum 01); ID-scan tests rerun after adding r2/ -> 17 passed; whole-run layout lint findings [].
- Descriptive probes: δ sensitivity C1 TE+ <0.1575 / INC <1.0175; C2 0.458 / 1.1115; C3 0.5483 / 1.2912; C4 0.6636 / 1.2057. Single-seed C1: EQ s1,5,8; TE+ s4,7,9,10; INC s2,3,6. trunc_normal: 23 of 4e8 draws exactly −2.0 (local torch 2.11).

## 2. Logic Chain
1. Failure class = coverage, not science (Obs 1) -> fix is additive tests; pinned files (Obs 2) forbid edits -> new files only + dated addendum + new receipt.
2. A full-output regression alone cannot see guards (all pass on real inputs) -> one-input corruption tests per guard; regression + hand oracle together avoid locking in current behaviour only.
3. Copied trees derived from Path(__file__).parents[2] -> inside a mutation tree the mutated code runs (no false survivors); code hashes not compared -> kills are behavioural.
4. Union harness shows every r1 survivor survives the shipped suite in full and is killed by the new files alone -> the r1 blocking classes are closed with attributable kills; no regression in the 78 previously killed edits.
5. Report wording errors identified by verifiers are real (verified against h2_results.json) but the report is pinned -> errata E1–E8 in addendum 08; no rule/label/number changes.

## 3. Caveats
- Tests were written after the results: regression guards, not pre-registration.
- Addendum 08 is in results/topic3/2026-11-02_h2/r2/ (owned path), not docs/03_empirical_analysis/topic3/ (not in my ownership list); root may copy it byte-identically.
- No new mutant search beyond the r1 union; a later verifier may find new ones (proposed nonblocking, root/PI to confirm).
- N42 is equivalent w.r.t. shipped constants; it is killed only via a SCALAR_KEYS monkeypatch.
- Driver tests use fakes; real GPU paths rest on r1 runtime evidence (G1 399 windows, seed-hash reruns).
- The trunc_normal count is from local torch 2.11 on a synthetic tensor, not the job's torch 2.4 network.
- No connectome access: remote dir overwrite (auditor N1) disclosed, not remediated; connectome dirs left for root.
- δ still owes PI confirmation (question in addendum 08 §8).

## 4. Conclusion
M2H2 iteration 2 DONE. The r1 gate's blocking class (verdict-path wiring and stats-script guards untested) is closed: 37/37 r1-survivor edits killed by the new files alone, 115/115 edits killed by the extended suite, no regressions, all receipts and C1 intact. The H2 verdict is unchanged: gate PASS; C1 INC, C2 INC, C3 TE+, C4 TE+; Family L as shipped. Integrated report must use addendum 08 errata (C3 is the δ-closest label at 0.548; R1 descriptive with DiD CIs; L0 unresolved; R0 values not "trained").

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/r2/addendum_08_sha256.txt && LC_ALL=C sha256sum -c results/topic3/2026-11-02_h2/output_sha256.txt && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 PYTHONPATH=. /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider -q -rs tests/topic3_h2` -> 167 passed.
- Mutation: `PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 setsid nohup nice /home/juke/superclaude-env/bin/python3 verification/worker_M2H2_r2/union_mutants.py > verification/worker_M2H2_r2/logs/union_mutants.log 2>&1 &` (~105 min; requires that verification/worker_M2H2_r2/trees does not exist; overwrites union_mutants.out.json — copy it first).
- Invalidation: any edit to a file in output_sha256.txt or addendum_08_sha256.txt; a mutant in the union list surviving the extended suite; a shipped JSON hash change.
