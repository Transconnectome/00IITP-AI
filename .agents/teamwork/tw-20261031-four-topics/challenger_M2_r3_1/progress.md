# progress — challenger_M2_r3_1

Last visited: 2026-11-01T06:40Z

- 06:25Z DISPATCH.md written; read role/runtime adapters, ORIGINAL_REQUEST, ACCEPTANCE, RESUME, PI_DECISIONS, GATE_STATUS, r2b gate record, sci-pipeline skill.
- 06:30Z BRIEFING.md written. Read card, analysis/resampling/estimators/token_job, driver scripts, all topic3 tests incl. r3 files, addendum_05 §1–§4, result report.
- 06:31Z Built copied tree verification/challenger_M2_r3_1/tree_base (121 files, manifest = production). pyc baseline recorded (53 .pyc under src/scripts/tests).
- 06:32Z Control in copied tree: 121 passed in 64.6 s, rc 0, no __pycache__ created.
- 06:38Z Wrote 14 own mutants (mutants/specs.py), none in worker's 151-patch union; each old string occurs once.
- Next: mutation runner (2 concurrent, timeout 900), Family A reruns for number-changing mutants, token-job counterfactuals from pinned npz, recompute headline/addendum numbers.

Last visited: 2026-11-01T06:53Z
- 06:36–06:47Z RUN1 own mutants: 11 SURVIVED / 3 KILLED / 0 INVALID (logs/RUN1_own.json). T01, T02 and A01–A09 survive the full 121 suite.
- 06:40–06:46Z Family A unmutated rerun reproduces 300/300 pinned leaves; A01–A09 reruns move Family A numbers (logs/famA_*.json).
- 06:44Z Family B counterfactual: T02 flips H1b to 'holds' (L3 lower 3/3); T01 reverses H1a direction (logs/famB_counterfactual.json); mapping validated on synthetic frames.
- 06:46Z Independent Family B recompute: exact match with code seeds; same verdicts with independent seeds (recompute/famB_independent.json). Addendum 05 §5 corrections all verified. Card in git 24fe976 at 08:46:25Z before results.
- 06:47Z C1 rc 0 (67 OK); receipts 42/1/3/2/3 OK.
- 06:48Z RUN2 union reproduction started: U057 KILLED, U072 KILLED; U091/U118/U127 running.
- handoff.md drafted (verdict REFUTED); O12 pending RUN2.

Last visited: 2026-11-01T06:55:53Z
- 06:54Z RUN2 union repro done: U057/U072/U091/U118 KILLED, U127 SURVIVED (equivalent); matches worker FULL_v2.
- 06:56Z End hygiene: tree_base manifest OK, pyc diff empty, no job trees/orphans, C1 rc 0 (67), receipts OK, audit_layout rc 0 findings [].
- handoff.md final (REFUTED).
