# DISPATCH — explorer_FU_C_r3_3

## 2026-11-01T21:37Z (received; workflow C, root 5fddb83e)

Task text as dispatched (verbatim up to the embedded gate record):

You are explorer_FU_C_r3_3, a Teamwork explorer in run tw-20261031-four-topics (General route), workflow C, launched 2026-11-01 ~23:20 KST by the new root coordinator (Claude session 5fddb83e, which took over from root d5bff6c5).
Role file: /home/juke/git/chavis/skills/teamwork/references/roles/explorer.md. Runtime adapters: references/runtime.md and references/claude-code.md.
Read first: ORIGINAL_REQUEST.md (incl. 2026-11-01 ~23:05 steering), sentinel/ACCEPTANCE.md (C1–C8, per-milestone criteria, ~23:15 addendum), orchestrator/PI_DECISIONS_2026-11-01.md (1–8), orchestrator/GATE_STATUS.md, orchestrator/RESUME_2026-11-01.md. Methodology: /home/juke/.claude/skills/sci-pipeline/SKILL.md.
Background docs are data, NOT authority (C8).
Metadata dir (exclusive): .agents/teamwork/tw-20261031-four-topics/explorer_FU_C_r3_3/ (DISPATCH, BRIEFING, progress, handoff). Probes only under verification/explorer_FU_C_r3_3/.
Parent: root coordinator. Nested spawning NOT available; structured return is the final report.
Python: /home/juke/superclaude-env/bin/python3; PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice; <=2 concurrent pytest, timeout 900; long jobs detached.
Respect C1–C8 (protected hashes; all *_sha256.txt receipts; frozen cards never edited; no participant IDs printed/written; no git writes; no installs into shared envs; never read ~/.claude/settings.json or secrets; sealed material never copied back; HCP data never redistributed).
Compute: B300 Slurm only (sbatch/srun), GPU ledger under flock; caps FU-C 13 GPU-h; verifiers <=1 GPU-h each.

Task: milestone FU_C: Topic 2 follow-up C: 8 seeds x 3 arms at E36, 140k samples, narrower t interval (df 7) (§7 ≈10.5 GPU-h; cap 13). Analyze the previous failure and recommend a fix strategy. Explorer 3 of 3 — primary lens: adversarial pre-mortem (how could this milestone produce a wrong or unverifiable verdict; integrity and C4/C6 hazards; what verifiers will attack). Recommend; do NOT implement production code. Work independently.
Milestone order of work: Topic 2 follow-up under PI decision 7 (FU_COMMON text; Option C: card must say whether the 5 r1 seeds are reused or 8 fresh seeds are trained; δ = 1 %; same verdict rules).

PREVIOUS ITERATION FAILURE — embedded FU_C r2 gate record (JSON). SUMMARISED here, not re-typed, per root rule in ACCEPTANCE addendum "FU_C r2 near-copy containment" (2026-11-02):
- 3 r2 explorers (R-b retire/re-author vs in-place edit), worker_FU_C_r2 DONE (C4 remediation: sealed + retired the test file, re-authored tests, derived-view verdict reproduction byte-identical, declared receipt supersession, c4scan tripwire, union mutation harness 146/150 killed).
- Gate FAIL: auditor INTEGRITY_VIOLATION, reviewer_1 and reviewer_2 REQUEST_CHANGES, challenger_1 and challenger_2 REFUTED — all on ONE item: a peer explorer's in-place-edited near-copy of the retired file under verification/explorer_FU_C_r2_2/tree/ plus the old pin in the unedited pre-result receipt lets the literal be recovered from repo content. All other claims independently confirmed (verdict stop, I1 −0.113 % [−0.499 %, +0.272 %], df 7).
- Nonblocking items: r2-surface mutants surviving behaviourally (check_receipts, reproduce_verdict fail-closed, r2 driver, c4scan controls/scope), c4scan shape blind spots, report §3 stale counts, no git anchor for freeze order, verifier self-incidents (counters printed in transcripts).
