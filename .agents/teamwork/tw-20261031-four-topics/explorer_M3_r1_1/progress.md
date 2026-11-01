# progress — explorer_M3_r1_1

Last visited: 2026-11-01T00:40Z

- 00:36Z DISPATCH.md written (verbatim).
- 00:40Z Read runtime.md, claude-code.md, explorer.md, ORIGINAL_REQUEST, ACCEPTANCE, RESUME_2026-11-01, sci-pipeline SKILL, survey handoffs 1–3. BRIEFING created.
- Next: verify SwiFT ver11 architecture from code (T2.1); B300 read-only checks; data provenance.

Last visited: 2026-11-01T01:05Z
- 00:45Z T2.1 verified from code by CPU probe verification/explorer_M3_r1_1/probe_t21_shapes.py (.out.json): merges M0 16^3->8^3 (192->384), M1 8^3->4^3, M2 4^3->2^3; none after stage 3; time never merged; use_post_norm=True crashes.
- 00:50Z B300 read-only: 32/32 idle; .98 /scratch/data/hcp = 88 HCP REST1_LR hp2000_clean (one download in progress); .101 OpenNeuro fmriprep ds000001/114/228; no UKB fMRI outside ~/enigma_ocd (not touched).
- 00:55Z connectome: HCP S1200 REST1 1084 subj, REST2 1206, HCP-MMP1 ROI series 1088x(1200x360)x2 runs; no HCP family/restricted csv found (bounded search). Killed my own 2 leftover remote find/python procs only.
- 00:58Z advisor consulted.
- 01:05Z A PRIORI (before any real-data number): exploratory dev probe on 5 HCP REST1_LR subjects = positions 0-4 of sorted connectome listing (BURNED for confirmatory use). Merge point fixed on architecture grounds = M0 (16^3->8^3) with octant-locality (boxes within one final-token octant = stage-1 window); M1 computed alongside only as a count/descriptive comparison. Arms E (2x2x2), C (balanced min-diameter growth in correlation distance on train group FC), G (same algorithm on distance-only surrogate graph), R (random balanced octant-local). Stats: held-out mean within-box correlation, top-2 PCA retention (train-fit basis), in-sample vs held-out gap. Train subj 0-2, held-out 3-4 + leave-one-out rotations. These numbers govern NO verdict.
