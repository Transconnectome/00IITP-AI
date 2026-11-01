# progress — worker_FU_A_r1

Last visited: 2026-11-01T15:32Z

## 2026-11-01T15:14Z–15:30Z
- Read role/runtime/adapter, ORIGINAL_REQUEST, ACCEPTANCE (+addenda), PI decisions 1–8, GATE_STATUS, RESUME, sci-pipeline,
  r1 card, result report §7, addendum 05, r1 code (train/data/metrics/fixtures/stats/model), r1 scripts, ledger tail.
- B300 reachable via `ssh -J dgx1,node1 -o ControlMaster=no -o ControlPath=none` (configured route fails). Login node = b300-01.
  squeue empty at 15:18Z; all 4 nodes idle. r1 data: /scratch/iitp4/worker_M3_r1/hcp/subjects (88 dirs, each
  bold_z_fp16.npy, cellmeans.npy float32 4096x1200, mask.npy).

## Pre-registered design-statistic formulas (written 15:32Z, BEFORE computing any of them on TRAIN)
TRAIN = the 64 subjects of results/topic2/2026-11-01/split.json "train". m_ict = r1 cellmeans.npy (cell c, frame t),
n_ic = subject i's brain voxels in padded cell c (pad96(mask.npy) reshaped 16x6 per axis). T = 1200.
- Q = sum_i sum_c n_ic sum_t m_ict^2 / (sum_i sum_c n_ic * T)      (voxel-weighted mean square of the cell-mean field)
- kappa = 1 / sqrt(Q)                                              (global target scale; NMSE is invariant to it)
- NF = sum_i #{c : n_ic > 0} / (sum_i sum_c n_ic * Q_i-weighted...) defined exactly as
  NF = sum_i N_i * T / sum_i sum_c n_ic sum_t m_ict^2, N_i = #{c: n_ic > 0}
  (share of the target's voxel-weighted energy that independent unit-variance voxel noise would contribute)
- Fixture voxel noise: sigma_v^2 = NF * nbar_fix / (1 - NF), nbar_fix = sum_c nvox_c / #{c: nvox_c > 0} on the fixture
  ellipsoid (g=16, patch 6); one sigma_v for F+ and F-. Fixture target scale kappa_fix = 1/sqrt(Q_fix) from a seeded
  fixture-train sample. If NF >= 1 the calibration is undefined -> stop and report (no tuning).
- Descriptive only (not used for any decision): median and mean over cells of lag-1 autocorrelation of m (TRAIN).
