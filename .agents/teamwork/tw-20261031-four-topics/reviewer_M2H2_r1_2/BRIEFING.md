# BRIEFING — 2026-11-01T17:10Z

## Mission
Independent review of milestone M2H2 (Topic 3 H2 random-init control) against ACCEPTANCE C1–C8 and H1′–H3′; verdict APPROVE / REQUEST_CHANGES.

## 🔒 My Identity
- Archetype: reviewer (roles: reviewer, critic)
- Host: claude-code (Opus 5.5); no nested spawning; structured return = final report
- Working directory: /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/reviewer_M2H2_r1_2/
- Probes: /home/juke/git/00IITP-AI/verification/reviewer_M2H2_r1_2/ ; connectome: /home/connectome/connectome1/iitp4_m2h2/reviewer_M2H2_r1_2/
- Original parent: root coordinator (Claude session 5fddb83e), workflow C
- Milestone: M2H2; Instance: reviewer 2 of the M2H2 r1 gate

## 🔒 Key Constraints
- Review-only: never edit production files (src/topic3_h2, tests/topic3_h2, scripts/topic3h2_*, results/topic3/2026-11-02_h2, docs)
- C1 protected hashes; receipts; frozen cards never edited; no participant IDs printed/written; no git writes; no installs on DGX-Spark; never read ~/.claude/settings.json
- ≤2 concurrent pytest, timeout 900, nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1
- Verifier GPU ≤1 GPU-h on connectome Slurm, ledgered (start + close rows under flock); frames stay on connectome
- No find/du/grep -r/ls -R over /storage or /scratch on connectome

## Current Parent
- root 5fddb83e; Updated: not yet

## Review Scope
- Files: src/topic3_h2/**, tests/topic3_h2/**, scripts/topic3h2_*.py, results/topic3/2026-11-02_h2/**, docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md + _h2_result_report.md, ledger rows
- Contracts: sentinel/ACCEPTANCE.md (H1′–H3′, C1–C8), PI_DECISIONS item 8, card §6
- Criteria: correctness, freeze-before-results, gate validity, integrity, governance

## Key Decisions Made
- Independent recompute of families C/L from returned aggregates with own arithmetic + own rule (frozen resampling primitives only)
- One verifier GPU rerun: random-init seed 3 (a C2-INC seed), job 218065, compare with shipped R3 aggregates
- Using worker venv read-only on connectome (no new 5 GB venv); recorded as deviation

## Review Checklist
- Items reviewed: addendum 07, result report, h2stats, compare, reduce, provenance, model, data, driver, both scripts, tests (decision_rule, endpoints, model_init, random_init_baseline)
- Verdict: pending (no blocking issue found so far)
- Unverified claims: seed-3 rerun (in flight); local seed-hash rebuild (in flight); test suites (running)

## Attack Surface
- Hypotheses tested: freeze before results (git commit 35d10a5 16:05Z < gate 16:22Z); vendored bytes = upstream commits; labels reproduce (24/24, diff 0); δ sensitivity; ID leak scan (0 real IDs)
- Vulnerabilities found: none blocking; minor report inaccuracies (C1 "on δ boundary" overstated; worker omitted code_sha256_at_freeze.txt pre-existing failure)
- Untested angles: G5 controls rerun; per-subject token PRs of random arms beyond seed 3

## Artifact Index
- verification/reviewer_M2H2_r1_2/recompute_h2.py + .out — independent recomputation
- verification/reviewer_M2H2_r1_2/c1_protected.log — C1 check
- verification/reviewer_M2H2_r1_2/pytest_*.log — suite runs
- verification/reviewer_M2H2_r1_2/seed_hash_check.py + .out — local CPU seed hashes
- verification/reviewer_M2H2_r1_2/rerun_seed3.sbatch — connectome rerun
