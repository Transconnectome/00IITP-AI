# progress — worker_FU_D_r1
Last visited: 2026-11-01T15:31Z

- 15:23Z DISPATCH.md written; read role/runtime adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addenda incl. B300-share rule), PI decisions, GATE_STATUS, RESUME, r1 card, result report, explorer_FU_D_r1_1 handoff, frozen train/model/stats/verdict/ledger.
- 15:27Z B300 status: b300-01 idle (8 GPU), r1 HCP data present (88 subjects), squeue shows nhpfull-* pipeline (other session), no g3t-G-E0-* jobs.
- 15:28Z started own venv build on b300-01 (/scratch/iitp4/fu_d/venv from r1 lock; detached; log /scratch/iitp4/fu_d/build_env.log).
- Next: write src/topic2_fu_d + scripts + tests + card (local, CPU).
- 15:29Z venv build done: freeze identical to r1 lock (env_check identical=True, torch 2.15.0+cu134).
- 15:35-15:55Z wrote src/topic2_fu_d (config, design, seedplan, records, verdict, view, slurm), scripts/topic2fu_d_{build_env,train,make_view,b300_scan,equiv,slurm,seed_plan,verdict,c4scan}.py, tests/topic2_fu_d (8 files, 128 tests pass), card draft docs/.../2026-11-02_topic2_fu_d_card.md (NOT yet frozen).
- 15:56Z mutation harness running (verification/worker_FU_D_r1/mutation/); B300 code sync + positional view build running.
- 16:00Z mutation harness pre-freeze run 1: 60/62 killed (R03, R15 survived) -> added 2 tests; run 2: 62/62 killed (verification/worker_FU_D_r1/mutation/mutants_prefreeze_r2.out.json).
- 16:06:07Z CARD + CODE FROZEN: results/topic2/2026-11-02_fu_d/card_sha256.txt (card 1b7fee6c…001b), code_sha256_at_freeze.txt (29 files). Old 86 tests pass, C1 rc 0, r1 code freeze 33/33 OK (checked 15:58Z).
- 16:0xZ B300 ssh outage ~10 min (banner timeouts via dgx1 jump); recovered.
- 16:11Z code synced (39 files, 0 mismatch); positional view built: 88 subjects, 176 hard links, all same inode, split check train/val/test/disjoint true.
- 16:13:50Z share-check clean (no g3t-G-E0-*); smoke job 511 submitted (debug; equiv check + E192 HCP cost probe), ledger started row written.
Last visited: 2026-11-01T16:14Z
- 16:35-16:37Z smoke job 511 ran (waited ~21 min in queue: QOSMaxGRESPerUser, 8-GPU user cap). Closed 0.04 GPU-h. Equivalence: r1 hcp_E_s0 test NMSE reproduced EXACTLY through FU-D view (per-subject num/den equal, order equal). E192 HCP cost probe: 0.4962 s/step, projected 1.213 h/run. B300 C4 scan 0 hits before copy-back.
- 16:39-16:41Z share-check clean; F+ gate jobs submitted: Fplus_E_s0=534, Fplus_C_s0=535, Fplus_S_s0=536 (cost guard c=1.31).
Last visited: 2026-11-01T16:42Z
Last visited: 2026-11-01T17:04:20Z (F+ gate jobs queued, QOSMaxGRESPerUser)
Last visited: 2026-11-01T17:36:48Z (F+ gate queued)
- 17:45Z gate jobs 534 (Fplus_E_s0), 535 (Fplus_C_s0) RUNNING after ~65 min queue; 536 pending (QOSMaxGRESPerUser). No g3t-G-E0 jobs seen. Last visited: 2026-11-01T17:47:53Z
