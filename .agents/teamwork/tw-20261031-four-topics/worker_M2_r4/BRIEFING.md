# BRIEFING — updated 2026-11-01T12:10Z

## Mission
M2 (Topic 3) final iteration 4, PI decision 6 fixed scope: close r3 blocking classes (a) Family A full-output regression, (b) token_job producer, (c) primary-side Holm vs Bonferroni (N01), (d) D1 corr-only branch, with ADDITIVE tests + addendum_06 + receipt. No src/scripts change, no production rerun, no new estimand.

## 🔒 My Identity
- Archetype: teamwork worker (General route)
- Roles: implementer (primary), qa, specialist (sci-pipeline methodology)
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/worker_M2_r4/
- Original parent: root coordinator (workflow harness; no native ID exposed to me)
- Milestone: M2 Topic 3, iteration 4 (final)
- Host: claude-code; nested spawning not available; structured return = final report

## 🔒 Key Constraints
- C1–C8; no participant IDs printed/written; no git writes; 0 GPU.
- Python /home/juke/superclaude-env/bin/python3, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=2, nice; <=2 concurrent pytest, each `timeout 900`; timeout/OOM = INVALID (rerun).
- Pinned (never edit): card, provenance, result report, addenda 01–05, *_sha256.txt receipts, existing tests/topic3_spectral/*.py, src/topic3_spectral/*, scripts/topic3_*.py.
- Never run scripts/topic3_*.py in production tree (topic3_common.py:12 OUT hardcoded); only in tmp_path / copied trees.
- Exclusive write: tests/topic3_spectral/test_regression_r4.py (+ at most one more test_*_r4.py), docs/03_empirical_analysis/topic3/2026-11-01_topic3_addendum_06.md, results/topic3/2026-10-31/addendum_06_sha256.txt, verification/worker_M2_r4/.
- Each new test must pass on shipped code; if not, STOP and report possible real defect.
- Unique log names; never overwrite.

## Current Parent
- Conversation ID: root coordinator (harness)
- Updated: not yet

## Task Summary
- What to build: 2 additive test files; named-mutant reproduction (verbatim from verifier harnesses) in copied trees; 151-patch union rerun; addendum_06 + receipt.
- Success criteria: named mutants (26 required) KILLED by r4 tests; union: only U127 survives; all suites pass; C1 + receipts OK; no new __pycache__ in src/ or scripts/.

## Key Decisions Made
- Two files: test_regression_r4.py (classes a, d: Family A / subject level) and test_token_level_r4.py (classes b, c: token level).
- Family A: real-data rerun in tmp_path (skip if any pinned VRABES input absent) + synthetic direct re-derivation of subject_level (VRABES-independent; kills FA11 dead-column floor which is invisible on real data).
- One mutant job runs the full suite (121 + r4) without -x: kill attributable to r4 iff failing tests are all in r4 files (pre-existing 121 all pass = survives shipped suite).
- Frozen r4 bytes (08:13:57Z): test_regression_r4.py ecceb134..., test_token_level_r4.py ab99b2b1... (17 tests; suite 138).
- Host memory pressure from other workloads: earlyoom SIGTERMed v1 jobs -> INVALID; runner v2 (memory gate 15.5 GiB, own session + group cleanup, INVALID auto-retry). Union kept in full (no -x) mode so per-job pre-existing failing sets can be compared with FULL_v2.

## Artifact Index
- verification/worker_M2_r4/logs/pyc_baseline_start.txt, pyc_list_start.txt — pycache baseline at start
- verification/worker_M2_r4/bin/ — make_tree.sh, named_specs.py, union_specs.py (byte copy), run_jobs.py (v1), run_jobs_v2.py, run_evidence*.sh, summarize.py, final_checks.sh
- verification/worker_M2_r4/runs/ — SMOKE_dev1_named*, EVID_named_r4.json.partial (v1, stopped), EVID_named_r4_v2b*, EVID_union_r4_v2b*, *_STOPPED_README.txt
- verification/worker_M2_r4/probes/ — seed_search_n01, margins_r4, addendum_numbers (+ .out.json)
- scratchpad addendum06_draft.md (+ sec4_method, sec5) — addendum draft (written to docs/ once, at the end)

## Change Tracker
- Files created (production): tests/topic3_spectral/test_regression_r4.py (ecceb134...), tests/topic3_spectral/test_token_level_r4.py (ab99b2b1...), docs/.../2026-11-01_topic3_addendum_06.md v2 (46527e6a...; v1 af805513... superseded, kept in verification/worker_M2_r4/superseded/), results/topic3/2026-10-31/addendum_06_sha256.txt v2 (db88f543...).
- Build status: final: topic3 138 passed (fc5), old suite 86 + topic1 88 + C1 67 + 6 receipts OK (fc4), pyc unchanged.
- Pending issues: none. Named 26/26 required killed (r4-only); union 150 KILLED / 1 SURVIVED (U127) = FULL_v2.

## Quality Status
- Build/test result: 138 passed (production), smoke 26/26 required ids killed
- Lint status: flake8 (max-line-length 120) + ruff clean on the two r4 files
- Tests added/modified: 17 new tests in 2 new files; nothing existing modified

## Loaded Skills
- Source: /home/juke/.claude/skills/sci-pipeline/SKILL.md (read in place; no local dump needed — methodology only)
- Core methodology: frozen card before results, synthetic ground-truth fixtures, run records, verdict taxonomy, independent review; tests added post-results are regression guards, not pre-registration.
