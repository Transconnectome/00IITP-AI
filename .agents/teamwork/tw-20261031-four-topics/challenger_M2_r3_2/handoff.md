# handoff — challenger_M2_r3_2 (M2 Topic 3, iteration-3 gate), DRAFT written 2026-11-01T07:02Z

Status: DRAFT while the last mutant jobs run; the final version replaces this file.

## Challenge Summary
Overall risk assessment: MEDIUM (no real-data verdict changes; two unguarded classes on the frozen decision/report path).
Verdict (dispatch criterion): REFUTED.

## 1. Observation
- Own byte-copy tree verification/challenger_M2_r3_2/tree_base (tools/make_tree.sh; manifest 84 files = production).
  Controls: shipped 121 suite 121 passed, 0 skipped (logs/ctrl_full.{log,xml}); shipped 88 suite 88 passed (logs/ctrl_s88.*).
- My own 36 mutants (mutants/my_specs.py, runner mutants/run_my_mutants.py, results mutants/RUN_full.json).
- D1 corr-only branch: VA01 and VA02 SURVIVE the 121 suite; witness (probes/witness_d1_corr_only.py) at card PARAMS
  gives cov lo -2.94 / corr lo +13.88 (D=64) and cov lo -3.84 / corr lo +20.73 (57x1536): shipped "drop not robust";
  VA01 "drop robust in cov only: attributable to per-channel gain (final LN)"; VA02 "drop robust and not a per-channel-scale effect".
- Family A reported numbers: FA01-FA08 (+FA09, FA10) SURVIVE the 121 suite; rerunning the mutated topic3_subject_level.py in a
  copied tree changes 7-56 of the 300 pinned leaves (reruns/famA_*.json), incl. report-cited values.
- Unmutated Family A rerun reproduces all 300 pinned leaves exactly (reruns/famA_CONTROL.json, max rel diff 0.0).
- Family B recomputed with my own code from the 4 pinned npz: 0 mismatches vs pinned; verdicts H1a holds, H1b not replicated,
  also with unrelated RNG seeds (probes/recompute_family_b.out.json).

## 2. Logic Chain
(final)

## 3. Caveats
(final)

## 4. Conclusion
(final)

## 5. Verification Method
(final)
