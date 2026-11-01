# progress — explorer_M2H2_r1_3
Last visited: 2026-11-01T14:58Z
- 14:57Z DISPATCH.md, BRIEFING.md written. Governing docs read (ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME, role + adapters).
- Next: Topic 3 card §6, provenance, addenda, victory_M2, src/topic3_spectral.
Last visited: 2026-11-01T15:45Z
- Read card, provenance, result report, addenda 01-06, victory_M2 grep, src/topic3_spectral token_job, launcher.
- Key finds: (1) VRABES extraction ran at NERSC with SwiFT_v2_perlmutter (seungju_perlmutter, committed HEAD 63367643 during Aug-2026) + uncommitted VRABES wiring (snapshot in VRABES/swift_extraction_code, but its datasets.py carries Oct-17 ports). (2) Local SwiFT_v2 ver11 (de132387) != fork ver11 (5bc44469): double-MLP per block and summed 3D RoPE in fork; local defaults differ -> using local code would silently change the network. (3) connectome has inputs 03_MNI_to_TRs/ses-01/img (57 subj x 150 frames), trained ckpt best.pt (7260249428 B, mtime 2026-02-25) under /storage/connectome/jubin/260225_newmodel/, frame dumps in 04_embedding. 8x A5000 idle on node1; system python 3.8; internet ok.
- Next: minimal smoke probe (venv on connectome node1 home, 1 GPU Slurm job <=0.25 GPU-h, ledgered) to measure trained-forward replication error vs existing dumps and timing/memory.
Last visited: 2026-11-01T15:30Z
- (correction: the 15:45Z stamp above should read ~15:13Z; clock checked at 15:13:21Z)
- 15:19:13Z ledger started row; Slurm job 218007 (connectome node1, 1 GPU, -t 14 min) submitted: independent trained-replication smoke + perturbations + random-init on synthetic iid only.
- Local synthetic probe done: verification/explorer_M2H2_r1_3/probe_local/out/fixture_theory.json (random linear map PR ~ d_in d_out/(d_in+d_out+1), not isotropic; smoothing collapses PR).
- connectome ssh flaky (banner timeouts) since ~15:25Z; polling.
Last visited: 2026-11-01T15:52Z
- 15:20:18Z job 218007 COMPLETED (61 s, 0.017 GPU-h); ledger close row appended; aggregates copied back (no ID strings); remote probe dir removed.
- Layout lint whole run root: 382 files, 0 findings, rc 0.
- handoff.md written (Hard). DONE.
