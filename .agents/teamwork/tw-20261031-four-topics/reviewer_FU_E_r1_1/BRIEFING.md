# BRIEFING — reviewer_FU_E_r1_1

- Identity: reviewer_FU_E_r1_1 (roles reviewer + critic), run tw-20261031-four-topics, workflow C, General route.
- Host: claude-code (Claude Opus 5.5 subagent spawned by workflow orchestration script). Parent: root coordinator (session 5fddb83e). No nested spawning; SendMessage not used (final report = structured return).
- Ownership: this metadata folder (DISPATCH/BRIEFING/progress/handoff); probes only under /home/juke/git/00IITP-AI/verification/reviewer_FU_E_r1_1/. Read-only on production files. No git writes, no installs, no settings/secrets reads.
- Immutable constraints: ACCEPTANCE C1–C8 + 2026-11-01 addendum (F1–F3, C5 B300 Slurm/ledger/caps, B300-share squeue rule); PI decisions 1–8; C8 (no numbers from EMPIRICAL_ANALYSIS_REPORT.md / consolidated status).
- Milestone under review: FU_E (Topic 2 follow-up E, frozen-encoder within-run identifiability; cap 1.5 GPU-h).
- Phase: review complete (see progress.md / handoff.md).

## Review Checklist
- Items reviewed: card (frozen, sha 072553b0…), result report, src/topic2_fu_e/* (8 files), scripts/topic2fu_e_{extract,verdict}.py, tests/topic2_fu_e/* (7 files), results/topic2/2026-11-02_fu_e/* (receipts, extract.json, verdict.json, sacct, slurm log, id scan), ledger rows, worker metadata, B300 sacct/pins (read-only ssh).
- Verdict: see handoff.md.
- Unverified claims: B300 extraction numerics themselves (R matrices) were not re-generated on GPU (decision value low: verdict is inconclusive under every counterfactual tested); B300 ID scan content (names held on B300 only).

## Attack Surface
- Hypotheses tested: verdict reproducibility (byte-identical); independent re-implementation of Idiff/null/t-interval/gate/verdict logic (agrees; robust to perm seed); counterfactual F+ pass (still inconclusive); counterfactual pooled readout (still inconclusive); model input layout vs r1 training layout (consistent: forward_encoder takes B,C,T,D,H,W); checkpoint/split/perms pins on B300 (match); C4 local pattern scan (only count fields); freeze timeline (card 16:22:56Z < job 524 submit 16:24:31Z); 21 independent mutants.
- Vulnerabilities found: see handoff.md (readout-wiring and constant mutants survive; split/perms file sha recorded but not gated; fixture conditions not size-checked).
- Untested angles: GPU re-extraction; F+ fixture generator equivalence with r1 beyond code reading.
