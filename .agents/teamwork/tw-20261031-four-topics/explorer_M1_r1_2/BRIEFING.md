# BRIEFING — 2026-10-31 17:10 KST

## Mission
M1 (Topic 1 hardening + full-cohort step 5, ACCEPTANCE T1.1–T1.5): recommend a concrete, verifiable worker strategy with cheap-probe evidence. Do not implement production code.

## 🔒 My Identity
- Archetype: explorer (Teamwork, General route), explorer 2 of 3 for M1 round 1
- Roles: read-only investigation, probes only under /home/juke/git/00IITP-AI/verification/explorer_M1_r1_2/
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M1_r1_2/
- Original parent: root coordinator (no native ID supplied in dispatch); host=claude-code; nested spawning not available
- Milestone: M1

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code
- C1 protected hashes; card §12 code hashes (src/topic1_lagmotif/*.py, scripts/topic1_timing.py) must not change
- C4 no IDs printed/written, no git writes, no installs; C6 no ENIGMA to B300; C7 external repos read-only
- Metadata only in this folder; final report = StructuredOutput return

## Current Parent
- Conversation ID: root coordinator (ID not given)
- Updated: not yet

## Investigation State
- Explored: card, OPEN_ISSUES(+r2), GATE_STATUS, victory audit handoff, survey_1 handoff, pipeline/data/motifs/flow/preprocess, existing tests, mutant harnesses
- Key findings: (1) proposed contract tests kill 5/5 survivors, 0 survivors over 19+4 mutants; (2) Mundlak β equality 4e-13 even at re_var=0 / non-converged fits; (3) FPR cannot detect across-site permutation or dx-permutation defects on this design -> need oracle fixtures; (4) survey's 200 s truncation reading gives 101 grid samples at 4 TRs; (5) §7 variants must run at the post-fallback primary density; (6) FL validation at B=9999,R=2000 costs ~0.9 CPU-h per scenario
- Unexplored: real degeneracy rate (needs cohort extraction), connectome/dgx1 env (survey covered)

## Key Decisions Made
- Probes use synthetic outcomes on the real design (metadata + npy headers only), aggregate output only

## Artifact Index
- verification/explorer_M1_r1_2/proposed_tests/test_extract_contract.py — proposed T1.1 test file
- verification/explorer_M1_r1_2/mut_harness/ — adapted harness copies + logs + results JSON
- verification/explorer_M1_r1_2/probe_stats_design.py/.out.json — design + FL/Mundlak probe
- verification/explorer_M1_r1_2/probe_fl_across_adversarial.py/.out.json — across-site permutation detectability
- verification/explorer_M1_r1_2/probe_trunc200_lengths.log — 200 s truncation grid lengths
