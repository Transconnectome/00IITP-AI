# BRIEFING — 2026-11-01T20:05Z

## Mission
Independent review of milestone FU_C (Topic 2 follow-up C: 8 fresh seeds x 3 arms at E36) against ACCEPTANCE C1–C8 and F1–F3; verdict APPROVE / REQUEST_CHANGES.

## 🔒 My Identity
- Archetype: reviewer (roles: reviewer, critic)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_FU_C_r1_1/
- Original parent: root coordinator, Claude session 5fddb83e (workflow C)
- Milestone: FU_C
- Instance: reviewer_FU_C_r1_1 (r1, reviewer 1)
- Host: claude-code 2.1.316; no nested spawning; final report = structured return

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code, results, docs, ledger
- Probes only under /home/juke/git/00IITP-AI/verification/reviewer_FU_C_r1_1/
- No participant IDs printed or written; no git writes; no installs; no settings/secrets reads; sealed material not copied
- B300 GPU only via Slurm, <=1 GPU-h (none used); squeue g3t rule before any submission

## Current Parent
- Conversation ID: root 5fddb83e
- Updated: not yet

## Review Scope
- Files: src/topic2_fu_c/, tests/topic2_fu_c/, scripts/topic2fu_c_*.py, results/topic2/2026-11-02_fu_c/, docs/.../2026-11-02_topic2_fu_c_{card,addendum_01,result_report}.md, ledger rows; B300 /scratch/iitp4/fu_c (read-only)
- Contracts: sentinel/ACCEPTANCE.md, PI_DECISIONS 1–8, FU-C card sha fc2d0672…4ecb
- Criteria: correctness, completeness, C1–C8, F1–F3, integrity

## Key Decisions Made
- GPU re-scoring not done: B300 originals sha-identical to repo copies + sacct independently confirm the runs; cost not justified.
- C4 HCP-ID literal in a FU-C test = blocking (strict C4, run precedent of r1 C4 gate failure); not an integrity violation; verdict unaffected.

## Review Checklist
- Items reviewed: card, addendum 01, result report, verdict.py, receipts.py, design.py, logs.py, slurm.py submit path, budget g3t, tests (spot), receipts, ledger, sacct, B300 hashes, partitions
- Verdict: REQUEST_CHANGES (1 blocking: C4)
- Unverified claims: B300 copy-back scan controls (not rerun); full bitwise determinism beyond step 200 (worker also says unverified)

## Attack Surface
- Hypotheses tested: freeze-before-results (receipts + autocommit 16:20:26Z/16:35:27Z + mtimes + sacct starts); fabricated records (B300 sha 48/48, sacct 25 jobs = ledger 10.422 GPU-h); verdict correctness (independent recompute, byte-identical CLI rerun); mutation evidence on pinned code (51/3/0 reproduced); equivalence of 3 survivors (argued from code); C4 (count-only membership vs 1,084 HCP names).
- Vulnerabilities found: real HCP subject ID literal at tests/topic2_fu_c/test_gate_and_records.py:182; worker C4 scans did not cover tests/.
- Untested angles: re-scoring a checkpoint on GPU; Slurm %j truncation behaviour for g3t names (not observed to matter).

## Artifact Index
- verification/reviewer_FU_C_r1_1/indep_recompute.py (+ .out.json) — independent recomputation
- verification/reviewer_FU_C_r1_1/mutants/worker_mutants_rerun.out.json — harness rerun
- verification/reviewer_FU_C_r1_1/verdict_rerun.json — CLI rerun (byte-identical)
- verification/reviewer_FU_C_r1_1/b300_snapshot.txt, b300_run_sha.txt, repo_run_sha.txt — B300 cross-check
- verification/reviewer_FU_C_r1_1/c1_check.out, audit_layout.out, pytest_*.out
