# progress — challenger_FU_C_r1_2
Last visited: 2026-11-01T19:50:34Z
- read role/runtime/run docs, card, verdict.py
Last visited: 2026-11-01T20:04:39Z
- C1 rc0; FU-C receipts OK; 109 tests passed
- independent recompute: all headline numbers equal verdict.json; verdict rerun cmp-identical
- provenance 24/24 OK; B300 48 files sha-identical; sacct 24 stage-1 jobs, no extras; run.json mtimes within 1-2 s of job end
- worker mutants reproduced 51/54; my 40 mutants: 21 killed, 19 survived (classified)
- adversarial: lexicographic start_utc guard fails open on +09:00 offset (nonblocking)
- C4: real HCP ID at tests/topic2_fu_c/test_gate_and_records.py:182 (count-only B300 check: 1 hit) -> BLOCKING
- GPU: 0 GPU-h (queue saturated; re-score judged low value)
- handoff.md written; verdict REFUTED (C4 only), science CONFIRMED
