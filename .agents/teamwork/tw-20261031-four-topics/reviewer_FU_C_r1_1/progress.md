# progress — reviewer_FU_C_r1_1
Last visited: 2026-11-01T20:07Z

- 19:49Z read role/adapters, ORIGINAL_REQUEST, ACCEPTANCE (+addenda), PI_DECISIONS, GATE_STATUS, RESUME, sci-pipeline; DISPATCH.md written.
- C1 rc 0 (67 lines); FU-C receipts card/code/presentation/output all rc 0; r1 fixture pins 12/12 OK (r1 output_sha256.txt hcp_* lines fail = pre-sanitization pins superseded by output_sha256_r2.txt, which passes).
- Tests: topic2_fu_c 109 passed; old 86 passed; topic1_lagmotif 88 passed; topic2_rgpool 116 passed.
- Mutation harness (worker copy, my WORK/OUT): 51 killed / 3 survivors (V07c, V12, F11) / 0 invalid on the pinned code; equivalence arguments checked.
- Independent recompute (own script, no FU-C imports): all per-seed NMSE, I1/I2, t df7, stop, stalls, sensitivity, pooled match; verdict CLI rerun byte-identical to verdict.json.
- B300: 48/48 run.json+train_log identical to repo copies; sacct 25 fuc jobs COMPLETED, 1 GPU, 37,520 s = 10.422 GPU-h = ledger; + explorers 0.262 = 10.684 <= 13.
- FINDING (C4): tests/topic2_fu_c/test_gate_and_records.py line 182 negative fixture literal equals a real HCP subject ID (count-only membership vs B300 name list; token never printed). Confined to FU-C (all tests/src/scripts scanned).
- Next: g3t/command-line evidence, layout lint, BRIEFING, handoff.
- 20:05Z g3t/command-line/mask-default checks OK; partitions equal r1; layout lint PASS (552 files, 0 findings); own outputs C4-clean (count-only).
- 20:07Z BRIEFING.md + handoff.md written. Verdict REQUEST_CHANGES (1 blocking: C4 HCP-ID literal in FU-C test). DONE.
