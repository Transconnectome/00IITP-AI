# DISPATCH — explorer_FU_C_r3_1

## 2026-11-01T21:38:00Z (received from workflow C script, root 5fddb83e)

Verbatim prompt header and task (identity, role/adapter paths, required reads, metadata/probe paths, Python/host rules, C1–C8 restatement, B300/connectome compute rules, GPU caps) as computed by
`.agents/teamwork/tw-20261031-four-topics/orchestrator/workflow_C_script.js.txt` lines 11–20 (COMMON) with id=explorer_FU_C_r3_1, role=explorer, plus lines 76–79 (explorer task) with mk=FU_C, it=3, e=1:

> Task: milestone FU_C: Topic 2 follow-up C: 8 seeds × 3 arms at E36, 140k samples, narrower t interval (df 7) (§7 ≈10.5 GPU-h; cap 13). Analyze the previous failure and recommend a fix strategy. Explorer 1 of 3 — primary lens: scientific design and falsifiability (card, controls, kill criterion, permitted data). Recommend; do NOT implement production code. Work independently.
> Milestone order of work: FU_COMMON (script line 47) + Option C text (script line 62).

The prompt then embeds "PREVIOUS ITERATION FAILURE" = the full FU_C iteration-2 gate record JSON (3 explorers, worker_FU_C_r2, 5 verifiers; gate FAIL: auditor INTEGRITY_VIOLATION; reviewer_FU_C_r2_1 REQUEST_CHANGES; reviewer_FU_C_r2_2 REQUEST_CHANGES; challenger_FU_C_r2_1 REFUTED; challenger_FU_C_r2_2 REFUTED).

## Deviation (recorded deliberately)
The embedded gate-record JSON is NOT re-typed here. Reason (C4): one verifier entry in it describes, for the retired real HCP-YA ID literal, which byte positions differ from an all-zero placeholder. That is partial identifier information. This .md file is committed to git by the host/root daemons, so copying it here would make that information permanent history. The same precedent was used by explorer_FU_C_r2_3 and worker_FU_C_r1 (gate records summarised, not re-typed). The verbatim gate-record content is available to root in the workflow harness journal; per-verifier reports are in each verifier's own handoff.md under this run directory.
