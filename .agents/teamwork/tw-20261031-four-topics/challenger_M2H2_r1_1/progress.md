# progress — challenger_M2H2_r1_1
Last visited: 2026-11-01T17:50Z
- [x] Read role, adapters, ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME, sci-pipeline
- [x] Card addendum_07 sha256 matches receipt; freeze 15:57:40Z < gate 16:22:19Z < random 16:32:19Z; in-job code hashes = repo
- [x] Explorer exposure: synthetic-only random init (handoffs + ledger)
- [x] Independent recomputation of families C/L from npz: labels identical, max rel diff 2.7e-14
- [x] Report numbers audit: all match
- [x] tests/topic3_h2 71 passed; tests/topic3_spectral 138 passed; C1 rc 0; receipts ok (2 pre-existing 10-31 exceptions)
- [x] connectome job 218069 COMPLETED 107 s, 0.03 GPU-h, ledger start+close rows; R0 G1 recheck 7.65e-7 0/84 fail; seeds 4,1 hash = shipped, scalars bitwise; remote dir removed
- [x] Script-wiring mutants v2 (with copied-tree baseline): W3 (all arms read R1) and W6 (skip gate check) survive behaviourally; W3 writes C1 EQ (+4 L flips). v1 run stopped by me (no baseline).
- [x] delta sensitivity: C3 TE+ only for delta/|T|<=0.548; C2 TE+ <=0.458; C1 INC 0.158-1.017
- [x] ID scan with real labels (boundary-aware): 0 hits in 97 files
- [x] Layout lint whole run root: PASS, 452 files, 0 findings
- [x] handoff.md written; verdict CONFIRMED with 2 nonblocking findings
