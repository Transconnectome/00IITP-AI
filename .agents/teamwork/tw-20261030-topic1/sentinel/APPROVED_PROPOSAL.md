# Approved proposal (ASSISTANT-AUTHORED, approved by user follow-up "워크플로 이용해서 진행 /teamwork")

Provenance: written by the root assistant in the previous turn of this session, after reading the four
handoff documents and inspecting data/code. It is not the human's text; the human approved steps 0–4.

## Observed facts at proposal time (root inspection, 2026-10-30)
- docs/03_empirical_analysis/empirical_results.json (mtime 18:40) contradicts EMPIRICAL_ANALYSIS_REPORT.md (mtime 15:50):
  T1 z_cycle3 d=0.08 (p=0.76), AUROC 0.476 vs report d=+0.354 (raw counts);
  T2 reconstruction_R2=1.0 for all methods; T3 PR 1.00–1.07 (uncentered) vs report (centered) 2.78–12.5;
  T4 forecast R2=1.0 in all conditions incl. C0. Report numbers must not be cited until rerun.
- ENIGMA data on disk: 1,706 subjects (cache /home/juke/git/enigma_ocd_mbbn/data/vmd_cache_4ch_464_head.mmap,
  shape (1706,5,464,304) float32, subjects list .mmap.subjects.txt; npy dir MBBN_data_304_ROIs_0.25 with 1,706 dirs).
  Metadata CSV has 2,095 rows; 389 absent, 388 of them from 6 sites with TR>2.0 s. OCD=1: 869, HC=2: 837; Y-BOCS non-null in OCD: 856.
- Valid length: random 200 subjects → median 167 TR, 80.5% zero-padded to 464.
- Cache TR distribution (via enigma time_series_utils.repetition_time): 0.7 s:43, 0.8:96, 0.85:104, 1.0:119, 1.73:39, 1.8:110, 2.0:1195.
- Medication coding per enigma_ocd_mbbn/post_hoc_analyses/medication_confound_analysis.py:23 → 1=medicated, 2=unmedicated, 3=unknown.
  In cache OCD: 1:203, 2:212, 3:447, nan:7. HC: 1:405, 2:177, nan:255 (HC coding implausible → unreliable).
- Existing extractor src/mbbn_connectome_biomarker.py: lag-1 net flow graph has no reciprocal edges by construction;
  null swap (lines 150–169) does not forbid creating reciprocal edges; ROIs subsampled by np.linspace(0,303,80);
  loader passes zero padding into correlations; DEFAULT_CSTC_ROIS indices unverified (no label table found).
- Existing test suite: 86 passed (root rerun, 60.9 s).

## Approved steps (0–4)
0. Feature branch (created: feature/topic1-lag-motif-v2). New dated files for outputs; do not edit previous reports.
1. Extractor fixes: (a) truncate to valid length and expose valid T as covariate; (b) null swaps that never create reciprocal
   edges, SP restricted to oriented connected triads; (c) lag defined in seconds (common-TR resampling or equivalent);
   (d) use all 304 ROIs.
2. Synthetic ground-truth fixtures (local): injected lagged 3-cycle detected; time reversal flips net-flow sign; null graphs
   contain zero reciprocal edges; spurious-direction control for autocorrelation/HRF differences (autocorrelation-matched surrogates).
3. Time 5 real subjects locally; estimate full-cohort cost (label 추정).
4. Freeze analysis card before any results: primary metric null-corrected Z/SP (not raw counts); OCD vs HC with site-held-out CV;
   kill criterion |d|<0.15; baselines static FC + existing MBBN AUROC≈0.63 (enigma HANDOFF); Y-BOCS regression; medication only
   within OCD (203 vs 212) after coding confirmation.
5. NOT APPROVED in this run: connectome CPU Slurm array job (needs separate approval after timing).
