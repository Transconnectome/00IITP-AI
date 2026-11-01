# progress — worker_M2H2_r1
Last visited: 2026-11-01T16:12Z

- 15:41Z start; read role/runtime/ORIGINAL_REQUEST/ACCEPTANCE/PI_DECISIONS/GATE_STATUS/RESUME, card, provenance, report, addenda 01-06, explorer handoffs.
- 16:00Z vendored fork ver11 (5bc44469), patchembedding (c889eebb), snapshot datasets.py (74316574) into src/topic3_h2/vendor/.
- 16:05Z wrote scripts/topic3h2_connectome.py, src/topic3_h2/provenance.py; launched venv build on connectome node1 (/home/connectome/connectome1/iitp4_m2h2/worker_M2H2_r1).
- next: write addendum_07 (H2 rule) + freeze receipt BEFORE any random-init forward on real frames.
- 15:57:40Z addendum_07 FROZEN: sha256 09b45220205bce814c4e07d4494d586b95f63f97dbfcddeb716fafcdc5edd84b (receipt results/topic3/2026-11-02_h2/addendum_07_sha256.txt). No random-init forward on real frames before this.
- 16:00-16:20Z wrote model/data/compare/reduce/driver/h2stats, scripts/topic3h2_connectome.py + topic3h2_stats.py; tests (43 pass). venv built (torch 2.4.0+cu121, numpy 1.24.4).
- ssh note: explicit ProxyCommand stalls uploads >160 KB; default ProxyJump with ControlMaster=no works. Submit filter: max 12 CPUs per GPU.
- 16:22:19Z gate job 218063 submitted (ledger start row). random submit correctly refused (no gate PASS record).
Last visited: 2026-11-01T16:23Z
- 16:30:24Z gate job 218063 COMPLETED (485 s, 0.135 GPU-h, ledger closed). In-job verdict PASS; local `topic3h2_stats.py gate` → gate_decision.json PASS (G1 max rel_fro 7.8e-7 all 399×4; G2 repool max 7.0e-7; G3 max rel 7.3e-8; G4 ckpt sha ok, 0 missing encoder keys, unexpected = augment_comp.smooth_kernel; G5 all 3 controls fail G1 (min rel_fro 4.6e-4 .. 2.1)).
- 16:32:19Z random job 218064 submitted (R1..R10), ledger start row.
Last visited: 2026-11-01T16:33Z
