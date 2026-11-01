# progress — challenger_FU_A_r1_2
Last visited: 2026-11-01T17:01Z
(Correction 17:01Z: an earlier version of this file carried estimated timestamps up to "17:10Z" that were ahead of the clock; times below are from `date -u`.)

- 16:47Z start (date -u). Read role/runtime/adapter, ORIGINAL_REQUEST, ACCEPTANCE (+addenda), PI_DECISIONS, GATE_STATUS, RESUME, sci-pipeline SKILL; DISPATCH.md, BRIEFING.md written
- ~16:50Z C1 67/67 OK; FU-A receipts card 8/8, code 21/21, output 21/21 OK; r1 code pins 33/33 OK
- ~16:51Z git (read-only): card first committed by host autocommit 35d10a5 at 16:05:25Z with sha 72be3e83 (before job 507 start 16:12:31Z)
- ~16:52Z p01 headline recompute: E 0.774678, C 0.770409 exact; gain 0.005511; 0/16 eval groups reach 1 %
- ~16:53Z p02 fixture path: perms/labels/constants match; training source class == numpy reimpl (1.2e-6); voxel noise sd 6.545; within-box r E 0.073 C 0.335; F+ realized noise share 0.219 (card/report say 0.248 = pooled F+/F-)
- ~16:54Z FU-A suite baseline 69 passed 1 skipped
- ~16:56Z mutation harness (47 mutants) launched detached (verification/challenger_FU_A_r1_2/mutation/progress.log)
- ~16:57Z p03 differential verdict: 0/20000 disagreements between card-derived reimplementation and decide(); shipped records -> inconclusive both
- ~16:58Z B300 read-only: run.json/train_log/code tree byte-identical to repo; sacct 507 1480+1479 s COMPLETED b300-01
- ~17:00Z p05 CPU Slurm step (job 540, b300-01, debug, no GPU): independent Q/kappa/NF on 64 TRAIN = identical to design_stats_train.json; pad alignment check passes
- 0 GPU-h used (B300 gpu queue heavily congested; no GPU probe needed)
