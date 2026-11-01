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

## 2026-11-01T15:30Z–15:55Z
- B300: venv built under Slurm (srun job 489, CPU, b300-01) at /scratch/iitp4/fu_a/env/venv from scripts/b300_env/build_env.sh
  (torch 2.15.0+cu134, numpy 2.5.4, scipy 1.18.1).
- Positional data view + TRAIN design stats (srun job 492, CPU): checks all true (88 subjects, manifest order == sorted dirs,
  5 burned excluded, repo split == mapped r1 split, 64/8/16 disjoint). Copied to results/topic2/2026-11-02_fu_a/design_stats_train.json
  (copy-back attempt hung; re-copy pending -- local file was 0 bytes at 15:40Z).
  Q 0.030780, kappa 5.6999, NF 0.20851, sigma_v 6.54593, cell lag-1 AC median 0.253 / mean 0.313.
- Code written: src/topic2_fu_a/{__init__,target,sources,run,calib,verdict}.py; scripts/topic2fu_a_{prepare_b300,train,
  build_fixture_perms,verdict,submit,token_scan}.py; tests/topic2_fu_a/{helpers,test_target,test_sources,test_run,
  test_verdict,test_fixture_stage0}.py.
- Tests so far: test_target 6/6, test_sources 9/9, test_run 6/6, test_verdict 33/33.
- Mutation harness verification/worker_FU_A_r1/mutation/run_mutants.py: 31/31 verdict mutants killed, control passes.
- B300 ssh: banner-exchange timeouts at the final hop since ~15:40Z (dgx1 and node1 reachable; B300 port 22 open);
  retry loop running. Fixture-perm build moved to local CPU (synthetic only), started 15:54Z.
Last visited: 2026-11-01T15:56Z
