# handoff — victory_M2H2_r2 (victory audit of M2H2, Topic 3 random-init control H2)

Written 2026-11-01T22:1xZ. Verdict: **VERIFIED_COMPLETE (VICTORY CONFIRMED)**. Full report is in the structured return.

## Observation
- Card addendum 07 sha256 09b45220…dd84b verifies; frozen 2026-11-01T15:57:40Z; committed by the snapshot daemon 35d10a5 at 16:05:25Z. connectome sacct: no GPU job between the freeze and gate job 218063 (16:22:19–16:30:24Z); local gate PASS written 16:31:46Z; random job 218064 submitted 16:32:19Z. Pre-freeze explorer smokes (218004/218007/218041) used random init only on synthetic iid input (scripts read).
- C1 rc 0 (67 files); results/topic3/2026-11-02_h2/output_sha256.txt (61) rc 0; addendum_07 and addendum_08 receipts OK; 2026-10-31 receipts as before (only the 2 known disclosed failures). No change to pinned src/topic3_spectral, tests/topic3_spectral, scripts/topic3_*.py; no new scripts/topic3_ file.
- Tests (my runs): tests/topic3_h2 167 passed; tests/topic3_spectral 138 passed; old suite (STRICT_E2E=1) 86 passed; tests/topic1_lagmotif 88 passed.
- Independent recomputation (own SVD PR estimators, own resampling and decision rule; verification/victory_M2H2_r2/indep_recompute.py): 24/24 labels equal to shipped (C1 INC, C2 INC, C3 TE+, C4 TE+; 20 Family L), worst relative numeric difference 8.3e-16, Holm p and seed effects exact; T reproduces pinned Family A A1 (5.343854531110546 / 6.038808669990018).
- GPU rerun (Slurm 218072, own venv and dir /home/connectome/connectome1/iitp4_m2h2/victory_M2H2_r2, repo-identical 20-file code manifest): seeds 5 and 10 reproduce shipped R5/R10 npz bitwise; encoder hashes equal; 0.072 GPU-h, ledger start + closing rows under flock.
- Novel mutants (12, copied tree): 10 killed; V07 (subset_prs corr floor 1e-3 -> 1e-2) survives, equivalent on shipped data (min column SD / median 0.36); V12 no-op control survives as expected.
- ID scan on connectome with the 57 real directory names: 0 full IDs, 0 bare tails in any H2 artifact; no "sub-" in results. Returned npz hold only position-keyed scalars and per-index-set PRs.
- Vendored code byte-identical to SwiFT_v2 cd87338 / 63367643 and VRABES 94c2bf4.

## Logic chain
Freeze precedes every random-init forward on real frames (H1'); gate G (element-wise ≤ 7.8e-7, re-pool, statistics ≤ 7.3e-8, identity, negative controls) passed before the random job was even submitted (H2'); tests + fixtures exist and pass, results are in the dated dir, report states the H2 verdict and its R1–R3 consequences (H3'); the shipped numbers are reproduced by independent code and by an independent GPU rerun of two seeds; M2H2 GPU use 0.891 of 6 GPU-h.

## Caveats (nonblocking; human must know)
δ set by the worker (PI question in addendum 08 §8; C3 TE+ holds only for δ ≤ 0.548 × trained effect); report errata E1–E8 live only in addendum 08 (results/…/r2/), so the integrated report must use corrected readings; "random init" = extraction constructor default init (not the training init); V07 latent test gap; report §3 prints 30.9 where 31.0 is correct; worker's connectome code dir partially overwritten (addendum 08 D1) — do not reuse without re-ship; cleanup of connectome dirs (incl. mine, 5.3 GB venv) and verification/victory_M2H2_r2/tree (22 MB copied tree) left to root.

## Conclusion
M2H2 meets H1'–H3', C1–C8 and PI decision 8. VERIFIED_COMPLETE.

## Verification method
Commands and outputs are listed in the structured return (commands_run_and_results); probes in /home/juke/git/00IITP-AI/verification/victory_M2H2_r2/.
