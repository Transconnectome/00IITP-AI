# progress — reviewer_FU_A_r1_2
Last visited: 2026-11-01T17:08Z
- 16:48Z read role/runtime/claude-code adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addenda), PI_DECISIONS 1-8, GATE_STATUS, RESUME; created DISPATCH/BRIEFING.
- C1 rc 0 (67/67). FU-A receipts card 8/8, code 21/21, output 21/21 OK; r1 code pins 33/33 OK.
- pytest tests/topic2_fu_a: 69 passed 1 skipped (rc 0); old suite (STRICT_E2E=1) 86 passed.
- Run records: pooled num/den = test_nmse; gain 0.005511 recomputed; code hashes match freeze receipts; perm sha match fixture_build.json.
- Frozen r1 loop evaluation path uses the rebound FixtureSource (train.py run/evaluate_fixture) -> test NMSE is on the cell-mean field.
- Card bytes 72be3e83 present in host autocommit 35d10a5 at 16:05:25Z, before gate start 16:12:31Z.
- B300 read-only: run.json/train_log sha equal repo copies; sacct FU-A GPU jobs = 403, 427, 507 only (matches ledger).
- Next: r1 topic2_rgpool suite, independent mutants (copied tree), stress tests.
- 16:53Z mutation probe launched detached (verification/reviewer_FU_A_r1_2/mutants, 30 new mutants).
- tests/topic2_rgpool 116 passed (r1 suite; earlier FU-B-card failure no longer present).
- C4 count-only scan of FU-A paths: only synthetic test literals; sub- token is a 1-letter word.
- Calibration recomputed: kappa, sigma_v exact. F+-only realized noise share ≈0.22 (3 seeds, win 20), not 0.248 (0.248 is pooled F+/F- Q_fix) -> descriptive mislabel, nonblocking.
