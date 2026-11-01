# progress — explorer_M4_r1_1

Last visited: 2026-11-01T00:46Z

- 00:36Z DISPATCH.md written; metadata + probe dirs created.
- 00:37–00:45Z orientation: C1 rc=0 (67 lines). Cohort manifest (Topic 1, aggregates only): n=1706, 23 sites, TR 0.7–2.0 s (1195 at 2.0 s), grid_len (2 s grid) min 100 / median 160 / max 340; raw_valid_T>325 for 362 subjects. Positions 0–4 all site#00, TR 1.8, raw_valid_T 197.
- Local env: numpy 2.3.5, scipy 1.15.3, sklearn 1.7.2, torch 2.11 dev (CPU usable), networkx 3.4.2. Load avg ~12–17 / 20 cores.
- ReSU primary source (arXiv:2512.23146 html via WebFetch): batch past–future CCA (SVD), rectified ON/OFF, no lateral connections, no local rule in the paper.
- Next: advisor call, then probes A (T4.1 diagnosis on 5 subjects), B (masked engine/topology synthetic), C (VAR(1) Bayes fixture), D (dev LOSO on 2 s grid).
