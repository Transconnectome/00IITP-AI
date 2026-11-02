# BRIEFING — `reviewer_FU_B_r1_1`

- **Run**: `tw-20261031-four-topics` (General route, workflow C)
- **Milestone**: `FU_B` (`Topic 2 follow-up B: 4× training budget (560k samples) at E36, arms E/C/S, 5 seeds (§7 ≈26 GPU-h; cap 33)`)
- **Role**: Independent Reviewer 1 of 2 (`reviewer_FU_B_r1_1`)
- **Verdict**: `APPROVE` (0 blocking issues, 2 minor non-blocking documentation observations, 0 uncovered requirements)

## Completed Checks
1. **Hash & Provenance Receipts**:
   - `PROTECTED_HASHES.txt`: 67/67 OK (`rc 0`).
   - `results/topic2/2026-11-01/code_sha256_at_freeze.txt`: 33/33 OK (`rc 0`).
   - `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt`: 31/31 OK (`rc 0`), signed `2026-11-01T16:20:25Z` strictly before the first post-freeze GPU run started (`2026-11-01T16:20:41Z`).
   - `results/topic2/2026-11-02_fu_b/output_sha256.txt`: 50/50 OK (`rc 0`).
2. **Test Suites (Sequential, CPU-only)**:
   - `tests/topic2_fu_b`: 128 passed in 4.96s.
   - `tests/topic2_rgpool`: 116 passed in 158.57s.
   - Old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`): 86 passed in 43.49s.
   - `tests/topic1_lagmotif`: 88 passed in 9.13s.
3. **Independent Statistical & Adversarial Verification**:
   - `verification/reviewer_FU_B_r1_1/verify_fub_independent.py` (`rc 0`): 0.0 difference on all gate gains, `I1`/`I2` 95% t-intervals, hierarchical bootstrap (B=10,000, seed 0), stall sensitivity, and r1 pairing; `scripts/topic2fu_b_verdict.py` reproduces `verdict.json` byte-identically.
   - `verification/reviewer_FU_B_r1_1/adversarial_probe.py` (`rc 0`): 10/10 independent adversarial/boundary probes (`A1`–`A10`) passed.
   - C4 hygiene scan: 0 hits across 159 worker and reviewer files.
