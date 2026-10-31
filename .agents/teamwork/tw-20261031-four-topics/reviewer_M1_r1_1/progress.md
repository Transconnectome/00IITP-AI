# progress — reviewer_M1_r1_1
Last visited: 2026-10-31T11:35:59Z
- started; metadata created
Last visited: 2026-10-31T11:50:57Z
- C1 rc 0 (67 lines); card §12 10/10; RESULTS_SHA256SUMS rc 0; tests topic1 88 passed; old suite 86 passed
- independent stats recompute: exact match (beta, t, d, p_FL same seed, Holm, fam2/3); other seed p 0.0209/0.4508
- analyze rerun on copy: identical except elapsed_s
- re-extract 10 positions: all bit-identical (json + FC rows)
- auditor mutants rerun (reviewer copy): with new tests 0 survivors (19/19 + 4/4); without: 5 survivors reproduced
- ID scan: 0 true-ID hits (6 false hits = site-name prefixes from splitext)
- layout lint PASS (81 files)
- running: probe_null_fpr (S1 B=9999 R=1200; S5 B=999 R=2000; planted d=0.15 R=600)
Last visited: 2026-10-31T11:54:23Z
- null probe done (S1 0.0558, S5 0.044, planted 0.1464); planted FE R=20000 unbiased; Trinity bundle clean; cleanup done; handoff written; verdict APPROVE
