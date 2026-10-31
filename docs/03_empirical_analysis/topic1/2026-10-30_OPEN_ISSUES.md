# Topic 1: open issues (recorded in run tw-20261030-topic1, not fixed here)

The frozen card `2026-10-30_topic1_analysis_card.md` has sha256 `1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`. It was frozen at 2026-10-30T12:12Z and made read-only. The same hash is in `results/topic1/2026-10-30/card_sha256.txt`.

## A. Document and record discrepancies

1. **Report vs JSON.** `docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md` (mtime 15:50) contradicts `empirical_results.json` (mtime 18:40). This is from sentinel/APPROVED_PROPOSAL.md and was not re-verified in this run.
   - T1: z_cycle3 d = 0.08 (p = 0.76) and AUROC 0.476 in the JSON, against d = +0.354 (raw counts) in the report.
   - T2: R² = 1.0 for all methods.
   - T3: participation ratio (PR) uncentered 1.00–1.07 vs centered 2.78–12.5.
   - T4: forecast R² = 1.0 everywhere.
   - Report numbers must not be cited until the analyses are rerun.
2. **Cohort counts.** The CSV gives OCD = 1: 869 and HC = 2: 837 for the 1,706 on-disk subjects (verified). The enigma manuscript and LOCAL_REPO_INTEGRATION_SPEC say 833/873. Y-BOCS non-null counts (856 code-1 vs 123 code-2) support 1 = OCD.
3. **Medication coding contradiction (new in this run).**
   - `enigma_ocd_mbbn/post_hoc_analyses/medication_confound_analysis.py:23` says 1 = medicated, 2 = unmedicated, 3 = unknown.
   - `post_hoc_analyses/site_driver_analysis.py:239` says 1 = drug-free, 2 = medicated, 3 = unknown.
   - HC counts are 1: 405, 2: 177, NaN: 255. They are implausible under the first coding and more plausible under the second.
   - The codebook must be confirmed with the data owner. Until then, medication results are reported only as "code 1 vs code 2".
4. **Sex coding.** 1 = male rests only on a code comment (`site_driver_analysis.py:237`). No codebook was found.
5. **Baseline "MBBN AUROC ≈ 0.63"** (APPROVED_PROPOSAL) matches no main-cohort file. File-backed values: 0.6512 ± 0.0318, from 26 evaluated rows plus 4 `checkpoint_missing` (the survey's "22/154" is not what the file shows); 0.6606 ± 0.0262; Linear SVM static FC 0.6420 ± 0.0125; and LOSO per-site mean 0.6519 (notebook-sourced, pre-remediation). Exact paths are in card §6.
6. **LOCAL_REPO_INTEGRATION_SPEC.md errors** (survey):
   - cache shape 1664 (actual 1706);
   - channel map wrong (the channels are IMF1–4 low→high plus a mask; there is no broadband channel);
   - unsupported "subcortical" atlas claim;
   - "30 sites" (actual 23 on disk).
7. **site_characteristics.csv** has a wrong TR column for 17 sites (survey). Use `repetition_time` / `tr_table`.
8. **enigma `repetition_time` substring-order defect.** 'Chiba-CHB' matches first, so Chiba-CHBSRPB returns 2.3 instead of 2.5. It has no effect on the on-disk sites; `tr_table` reproduces it on purpose and `analysis_tr` rejects TR > 2 s.
9. **One Vancouver-BCCHR subject** (TR 2.0) is in the metadata but absent from disk, for an unknown reason.

## B. v1 extractor defects (src/mbbn_connectome_biomarker.py; left untouched, protected)

10. The null swap (lines 150–169) rejects only existing (u,z)/(w,v) and so creates mutual edges. This is re-implemented and detected in `tests/topic1_lagmotif/test_null_and_census.py::test_invariant_checker_flags_reciprocal_edges_from_a_v1_style_swap`.
11. Zero padding is fed into the correlations; there is a silent synthetic fallback seeded by hash(sub_id); SYNTH_* cohorts; "channel 0 broadband" is actually IMF1; ROIs are subsampled to 80; DEFAULT_CSTC_ROIS has no source; CV is StratifiedKFold, not site-held-out.

## C. Limitations of v2 found or quantified in this run

12. **Spurious direction without neural coupling.** Source: `results/topic1/2026-10-30/spurious_direction.json` (N = 60, T = 200 at 2 s, 12 seeds, 300 nulls). Values at the primary density 10%, as mean ± SE:
    - Heterogeneous AR(1), φ ~ U(0.1, 0.9): Z030C −0.38 ± 0.35 (calibrated); Z030T +0.82; E2 −1.20. There is a residual feed-forward shift. The fixture tolerance is 3·1.5/√16 = 1.125.
    - Shared driver with per-ROI latency SD 1 s: Z030C −0.31 ± 0.05; Z030T −7.57; E2 +7.26 (2/12 degenerate); gradient share 0.84.
    - Latency SD 2 s: Z030C −1.86 ± 0.11; Z030T −8.76; E2 +6.91.
    - Curl-only does not remove it: curl Z030C is −5.09 at 1 s and −4.69 at 2 s.
    - HRF peak-shift SD 1 s and shared zero-lag signal (60% shared): 11/12 and 10/12 degenerate nulls at 10%.
    - Positive control, 20 planted recursive 3-cycles (g = 0.8): Z030C +9.63 ± 0.22. White-noise control: +0.24 ± 0.27.
    - The oriented degree-preserving null calibrates autocorrelation mismatch for 030C. It does **not** control hemodynamic latency or global-signal structure, and neither does curl-only. Autocorrelation-matched or IAAFT surrogates cannot remove latency bias (survey).
    - **This is reported as a limitation. A group difference in regional HRF latency, slice timing or global-signal amplitude could produce an E1/E2 group effect.**
13. **Degenerate nulls** (null SD = 0) occur for gradient- or global-dominated graphs, more often at lower density: 12/12 at 5% for shared zero-lag at N = 60. One of the 5 real A3 subjects (position 1578, TR 0.7) was degenerate at 5% but not at 10% or 15%. That same subject had a low acceptance rate at the primary unit (0.074 vs 0.62–0.75). The card's fallback rule is §3.
14. **Null irreducibility not established.**
    - 2-swap-only is reducible: `test_rotation_move_reaches_both_orientations_of_an_isolated_triangle`.
    - The 2-swap + 3-edge rotation set leaves 60 of 12,382 N = 5 degree classes reducible (explorer enumeration).
    - Uniformity on a fully reachable N = 5 class is verified by χ² (`test_null_is_uniform_over_reachable_class_lazy_chain`), but only with enough attempts. With 6·m attempts the visit frequencies were strongly non-uniform (χ² p ≈ 7e-181), so short chains are biased. The frozen 20·m was checked only on the 5 A3 subjects: |ΔZ030C| vs 40·m was 0.04–0.33.
15. **Per-subject Z is overdispersed** under the null, so it is not a calibrated z-score. Never threshold it at 1.96.
16. **npy preprocessing provenance unknown.** GSR, nuisance regression, slice-timing correction and filter type are unverified. The data are already low-passed near 0.25 Hz, and 5–13% of their power lies below 0.01 Hz (survey).
17. **No FD/motion data**, so motion cannot be controlled.
18. **ROI identity unknown.** There is no 304-ROI label table, so CSTC is dropped.
19. **Duration/TR collinear with site.** TR is constant within site, and T takes 1–6 values per site.
20. **Time reversal is exact only at TR 2.0.** At resampled TRs it holds only approximately (corr > 0.999 tested), because the resampled grid is not reversal-symmetric.
21. **Detrend before resample is required.** Resampling raw-scale data (mean about 1.15e4) with zero padding destroys F; `test_resampling_raw_scale_without_detrend_fails_offset_criterion` shows corr < 0.99.
22. **Bytecode.** `python -I` ignores PYTHONDONTWRITEBYTECODE. Use `-B` or the environment variable. The tests load enigma `time_series_utils` with `sys.dont_write_bytecode=True`.
23. **Old-suite command.** The dispatched command has no PYTHONDONTWRITEBYTECODE. In this run it was executed with `PYTHONDONTWRITEBYTECODE=1 ... -p no:cacheprovider` so that no bytecode was written. The tests and results are unchanged by this.
24. **The cohort-level statistics script** (card §4–§6) is not written yet. It needs independent review before step 5. Step 5, the connectome Slurm job, still requires separate approval.
