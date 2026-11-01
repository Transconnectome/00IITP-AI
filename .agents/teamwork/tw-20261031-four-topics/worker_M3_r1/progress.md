# progress — worker_M3_r1
Last visited: 2026-11-01T02:21Z
- 02:10Z DISPATCH.md written; read role/runtime/acceptance/resume/sci-pipeline; explorer probes reviewed.
- 02:18Z B300 .98: 8/8 GPUs idle, 224 cores, 2.1 TB RAM, /scratch 28T free; HCP REST1_LR complete files = 92 (rsync still active). Env build launched (/scratch/iitp4/worker_M3_r1/logs/build_env.log).
- next: advisor check on design; T2.1 doc; implementation + tests.
- 02:29Z B300 QC+preprocess done: 93 dirs with REST1_LR, 5 burned excluded in memory, 88 QC pass / 0 fail; manifest sha 26ba34a9…96d5 copied to results/topic2/2026-11-01/hcp_manifest.json. Env lock copied to scripts/b300_env/lock.txt.
- 02:5xZ src/topic2_rgpool (grid, partition, merge, model, data, fixtures, metrics, stats, train) + scripts (preprocess, make_split, build_partitions, train) written; fixture partitions built locally (F+ C purity 1.00).
- 03:0xZ tests/topic2_rgpool: 48 passed (merge/partition/model pairing/data/stats/stage-0 fixtures).
Last visited: 2026-11-01T03:05Z
- 03:06Z synthetic smoke on B300 GPUs 0,1 (0.04 GPU-h): 0.18 s/step at batch 16 -> ~0.45 GPU-h per 8750-step run.
- 03:14:34Z CARD FROZEN: docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md sha c9bfc60a…41f5; results/topic2/2026-11-01/card_sha256.txt + code_sha256_at_freeze.txt (33 files). 51 new tests passed at freeze.
- 03:16Z wave 1 (fixture gate: 6 Fplus + 2 Fminus) launched on .98 GPUs 0-7; HCP train-only partition build running on B300 CPU.
Last visited: 2026-11-01T03:18Z
- 03:3xZ HCP partitions built (64 train subj, 1195 signal cells; C disp 1.47, S 1.56-1.67, E 0.78); Stage 0 descriptive done (pca2 C<E all 16; r C~E; C>>S) copied to results/topic2/2026-11-01/stage0_hcp.json. Old 86 tests pass; C1 rc 0 (mid-run). Last visited: 2026-11-01T03:25:15Z
- 03:42Z wave 1 done (3.41 GPU-h). F+ gate PASS: seed-mean test NMSE E 0.6786, C 0.6578, S 0.6777 -> C vs E +3.07%, C vs S +2.94% (>= delta 1%). Fminus s0: E 0.2379, C 0.2409. 03:44Z wave 2 launched (4 Fminus + hcp E,C,S s0 + E s1). Last visited: 2026-11-01T03:45:08Z
- 03:5xZ wave 2 running (HCP val@2188 0.994-1.000; Fminus ok). addendum_02 written (Stage-0 metric ambiguity; implicit settings; early near-floor NMSE observation). Mid-run layout lint rc 0 (191 files, 0 findings). Last visited: 2026-11-01T03:55:59Z
- 04:11Z wave 2 done (3.43 GPU-h); F- gate computable: E 0.2393, C 0.2435, S 0.2437 (C not better: pass). 04:14:54Z wave 3 launched (8 hcp runs). Last visited: 2026-11-01T04:15:22Z
