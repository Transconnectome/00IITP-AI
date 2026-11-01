# BRIEFING — 2026-11-01T00:40Z

## Mission
Complete M2 iteration 2 (Topic 3): run the shipped 85-test topic3 suite against the control and every mutant from challenger_M2_r1_1 (N01–N28 run; dispatch names N01–N19) + explorer_M2_r2_2 mini_mutants (18) + explorer_M2_r2_3 kill_demo (21), on copied trees; handle survivors (equivalence or new test file); check addendum_03 items 1/3/5 numbers; write addendum_04 + its sha receipt.

## 🔒 My Identity
- Archetype: worker (Teamwork General route)
- Roles: implementer, qa
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2_r2b/
- Original parent: root coordinator (workflow harness, resumed 2026-11-01); host=claude-code; nested spawning NOT available; structured return = final report
- Milestone: M2 Topic 3 (T3.1–T3.4), iteration 2 (resumed after worker_M2_r2 interruption)

## 🔒 Key Constraints
- C1–C8 (sentinel/ACCEPTANCE.md). No git writes of any kind. No installs. No IDs printed/written. 0 GPU, nothing to B300, no ENIGMA data anywhere.
- Read-only: everything except my owned paths. Never mutate the production tree; mutants only in copied trees under verification/worker_M2_r2b/.
- Owned writes: verification/worker_M2_r2b/ ; docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_04.md (new) ; results/topic3/2026-10-31/addendum_04_sha256.txt (new) ; tests/topic3_spectral/test_verdict_rules_r2b.py (new) ONLY IF a non-equivalent verdict-path mutant survives.
- Do not edit addendum_03 or any pinned file. If a new test fails on shipped code: STOP and report; never change src/ or scripts/.
- Files under docs/03_empirical_analysis/topic3 and results/topic3 are scanned by the ID tests for the literal BIDS prefix token: never write it there.
- Python /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1, nice; long jobs detached with progress log; no orphans.
- Other team works on M1 in parallel; do not touch their paths.

## Current Parent
- root coordinator; Updated: not yet

## Task Summary
- What to build: mutant harness + MUTANTS_SUMMARY.json + raw logs; (maybe) test_verdict_rules_r2b.py; number-check probe; addendum_04; addendum_04_sha256.txt.
- Success: control 85 passed; every survivor killed by a new test (rerun shows kill) or shown equivalent; new tests pass on shipped code; all pins + C1 OK; suites pass.

## Key Decisions Made
- Copy scripts/ WITHOUT scripts/chrome_user_data* (gitignored browser profiles, credential-bearing, not code) and without __pycache__.
- Run challenger N01–N28 (superset of dispatch's N01–N19).
- Run full suite per mutant without -x so every killing test is recorded.
- Extract mutant specs from source harness files via AST (verbatim), hashes recorded.

## Artifact Index
- DISPATCH.md — verbatim dispatch
- /home/juke/git/00IITP-AI/verification/worker_M2_r2b/baseline/ — C1 and pin checks before work

## Change Tracker
- Files modified: none yet (production)
- Build status: baseline C1 rc0 (67 OK); output/addendum_02/addendum_03 pins rc0; card OK (format-stripped); freeze list only launcher differs (disclosed)
- Pending issues: none

## Quality Status
- Build/test result: not yet run
- Lint status: n/a
- Tests added/modified: none yet

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (methodology reference named by dispatch; not yet dumped locally)
- Core methodology: frozen card before results, synthetic ground-truth fixtures, run records, verdict taxonomy, independent review.
