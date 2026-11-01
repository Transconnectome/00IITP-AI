# progress — challenger_M4_r1_2
Last visited: 2026-11-01T03:08:46Z
- 02:33Z dispatch received; metadata + probe dirs created; role/runtime/acceptance/resume/sci-pipeline read.
- 02:40Z C1 recompute from saved outputs done: split rule rederived 0 mismatches, points exact, CIs within 0.2 boot-SD, verdicts match.
- 02:54Z C2 independent pipeline fold0 (refs 1e-15, PSP C0/C1/C4/C4DP/C5 <=3e-11; C3_g1 0.005 diff) ; C3 full independent H1/S1/S2 all folds match <=7e-13; MLP diag ok (no epoch cap hits); C4 T4.1 positions 0-11 all padded. Running C5 mutants + C6 C3 conditioning.
- 03:03Z c5 mutants: 7 killed / 10 survived (control 66 pass); c6: prod fold0 C3/C1 bit-identical to saved, C3 perturbation-sensitive; c7: analysis-script mutants leave verdicts unchanged, topology invariants ok, ID scan 0 hits; tests 67 + 86 pass, C1 rc 0, lint 0 findings; output_sha256 analyze.log empty-hash defect. handoff.md written. Verdict CONFIRMED (non-blocking gaps).
- 03:08Z c8: spectral-rescale mutant killed by 18 tests without -x; analyze crashes (ValueError) when all runs of a class fail in a fold; pycache self-incident repaired (C1 rc 0, freeze ok). handoff updated + read back.
