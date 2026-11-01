# progress — explorer_M2H2_r1_1
Last visited: 2026-11-01T14:39:04Z
- [x] read role/runtime, ORIGINAL_REQUEST, ACCEPTANCE, PI_DECISIONS, GATE_STATUS, RESUME
- [ ] read topic3 card/provenance/report/addenda

Last visited: 2026-11-01T14:59:02Z
- [x] read card, provenance, report, addenda 01-06, topic3_spectral code
- [x] located on connectome: inputs 03_MNI_to_TRs/ses-01/img (57 subj x 150 frames + global_stats), trained dumps 04_embedding/swift_E192 (57 x 7), ckpt /storage/connectome/jubin/260225_newmodel/.../best.pt (sha 5fd8a56c...)
- [x] ckpt structure probe (585 flat keys, _forward_module.model. prefix, 568 encoder tensors)
- [x] found ver11 code divergence: local SwiFT_v2 (de132387) vs connectome bundle (5bc44469): RoPE axis-split default vs sum
- [~] building explorer venv on connectome (detached)
Last visited: 2026-11-01T15:14:49Z
- [x] venv built on connectome node1 (torch 2.4.0+cu121, py3.8) 15:01-15:05Z
- [x] Slurm smoke job 218004 COMPLETED (66 s, 0.02 GPU-h, ledger start+close rows): bundle ver11 reproduces stored trained dump rel_fro<=7.7e-7; local SwiFT_v2 ver11 fails; TF32 6e-4; perturbations 0.12-2.2
- [x] C1 rc0, receipts OK, layout lint no findings, ID scan clean (placeholders only)
- [x] handoff.md written; DONE
