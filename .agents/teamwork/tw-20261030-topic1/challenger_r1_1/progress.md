# progress — challenger_r1_1
Last visited: 2026-10-30T12:33Z

- [x] Read role/runtime, request, proposal, acceptance, PROJECT.md, all production source + tests
- [x] Protected hashes 44/44 OK at start; production artifact hashes recorded (verification/challenger_r1_1/prod_hashes_before.txt)
- [x] P1 census vs networkx + brute force; production-path null equivalence (0 mismatches)
- [x] P2/P2b mixing sweeps at N=304 (means stable across 5..400 m; near-potential graphs structurally degenerate)
- [x] P3 positional stability (cache order == sorted listdir; silent shift if a dir disappears)
- [x] P4 mutation testing: 24 killed, 6 survived (3 pipeline lag-in-seconds, null 021C, head trim, NaN rule)
- [x] P5 full chain at all on-disk TRs (direction/magnitude consistent)
- [x] P6 planted cycles at N=304 (detected; 5% > 10% > 15% sensitivity)
- [x] P7 spurious_direction.json 5 keys reproduced exactly; params sha, card sha, card §12 hashes OK
- [x] P8 white-noise calibration at N=304 (calibrated, no T trend)
- [x] P9 timing rerun: 0 deterministic mismatches, time ratio 1.00-1.05
- [x] P10 uniformity: 1 small class slow-mixing at 100m (ok at 1000m)
- [x] handoff.md written
