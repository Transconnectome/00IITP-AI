# progress — explorer_M2H2_r1_2
- 14:53Z dispatched; read role/runtime/authority docs; DISPATCH.md written.
- ~15:00Z read card/provenance/report/addenda 01-06; located VRABES/swift_extraction_code snapshot and perlmutter commit cd87338 in local SwiFT_v2 refs; ver11 at cd87338 != local HEAD (double MLP, RoPE).
- ~15:05Z connectome logistics: inputs, stored dumps, ckpt copies (labfind), Slurm/QoS (node1 8xA5000, limit_qos 4 GPU/user), node-local homes, internet OK.
- ~15:10-15:25Z CPU synthetic probes (probe_ver11_cpu, probe_ver11_localize, probe_fixtures_cpu); venv build on connectome (torch 2.4.1+cu121, ~25 min).
- ~15:28Z background-z aggregate probe on node2 (srun CPU): all 57 pass the minback contract.
- 15:31:30Z ledger start row; Slurm job 218041 (node1, 1 GPU) 15:31:31-15:32:45Z, 0.021 GPU-h; ledger closed; replication <= 7.8e-7 rel at 3 positions x 7 windows; stats rel <= 2.7e-8.
- ckpt sha256 5fd8a56c... (both copies), srun node2 CPU.
- ~15:37Z deleted probe venv/code on connectome; C1 + topic3 receipts verified rc 0.
- handoff.md written (Hard handoff).
Last visited: 2026-11-01T15:39:51Z
