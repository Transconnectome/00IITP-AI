# progress — explorer_FU_C_r1_2
Last visited: 2026-11-01T14:25Z
- 14:16Z dispatch saved; required docs read.
- 14:25Z code read: per-run wall 1544-1655 s (0.43-0.46 GPU-h); perms_hcp.npz has S_seed0..4 only (seeds 5+ need new surrogates); launch_wave.py is direct-launch (not allowed now); repo split.json is sanitized (h00..) and does not match B300 data dir names.
Last visited: 2026-11-01T15:05Z
- 14:35Z B300 facts: Slurm partitions gpu/interactive/debug; /scratch is node-local (md0 ext4); HCP raw + r1 preprocessed tensors exist ONLY on b300-01 (=.98), absent on b300-02/03/04; b300-01 has Weight=100 (least preferred) -> jobs must pin -w b300-01; QOS normal MaxTRESPerUser gres/gpu=8 for the shared 'connectome' user (also 'whole' QOS 32 GPUs allowed to the account).
- 14:48Z P3 (Slurm job 410, CPU only, 37 s): frozen build_partitions.hcp_mode with S_SEEDS overridden in memory reproduces FC sha and E,C,G,R,S_seed0..4 perm shas bit-exactly; fresh S_seed10..17 built (232 rows moved, dispersion 1.58-1.65 vs r1 1.56-1.67).
- 14:54Z P4 (Slurm job 414, debug, 2 GPU, 80 s, 0.05 GPU-h, ledgered open+close): frozen path under Slurm with r1 venv: step-100/200 losses BIT-IDENTICAL to r1 for E and C seed 0; 0.1747 s/step, projected 0.432 h/run, data load 22 s.
- P1 local: r1 I1 sd 0.173 %; 8-seed t half-width 0.144 % (5-seed 0.215 %); MC: verdict stop w.p. 1.0 unless true I1 >= ~0.9 %.
- P2 local: prototype verdict layer + 26 tests; 21 mutants (V01-V12 classes, case A, FU-C F01-F08): 20 killed, F08 equivalent (len check implied by set-size check), baseline survives.
- SSH to B300 intermittent (banner-exchange timeouts; mux stalls; stdin forwarding/scp hang; base64-in-argv works).
Last visited: 2026-11-01T15:20Z
- P5 stall sensitivity: 2 stalled E runs -> inconclusive 20 %; C/S stalls never change verdict. P6: frozen sanitizer import path reproduces 15/15 repo-sanitized run.json from sealed originals (in memory, booleans only).
- Hash checks (LC_ALL=C): C1 67/67, freeze 33/33, output_sha256_r2 156/156.
- Cleanup: rm of B300 /scratch/iitp4/explorer_FU_C_r1_2 (1.9 MB, no tokens) and local /tmp/fuc2cm DENIED by permission system -> left in place, reported. No processes/jobs left. SSH master closed.
- 15:20Z handoff.md written (Hard). DONE.
