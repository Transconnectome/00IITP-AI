# reviewer_M2_r3_2 — handoff (Hard, DRAFT until §4 is final), M2 Topic 3 iteration-3 gate, 2026-11-01

Verdict: PENDING (mutation batch in progress; this draft is written for durability).

Evidence: /home/juke/git/00IITP-AI/verification/reviewer_M2_r3_2/ (logs/, runs/, probes/).

## 1. Observation (verified so far)

- C1: `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` gives 67 OK, rc 0 (logs/c1_pre.log).
- Receipts: output 42 OK, addendum_02 1, addendum_03 3, addendum_04 2, addendum_05 3, all rc 0 (logs/receipt_*_pre.log).
- addendum_05_sha256.txt pins addendum_05 a4001f09…, test_verdict_rules_r3.py 58c64ccb… and test_token_stats_wiring_r3.py b091b0b8…; the receipt itself is 1e542da7….
- code_sha256_at_freeze.txt: 26 of 27 OK. The exception is scripts/topic3_launch_connectome.py, changed after freeze, disclosed in addendum 01 item 2, with its current hash pinned in output_sha256.txt:27. So no src/ or scripts/ change in iteration 3.
- Production reruns (PYTHONDONTWRITEBYTECODE=1, -p no:cacheprovider, timeout 900, nice):
  - tests/topic3_spectral: 121 passed, 0 skipped, 60 s;
  - old suite (STRICT_E2E=1): 86 passed;
  - tests/topic1_lagmotif: 88 passed (logs/prod_*.log).
- The .pyc listing of src/ scripts/ tests/ is identical before and after my runs (logs/pyc_before.txt, logs/pyc_after.txt).
- Layout lint, audit_layout.py on the whole run metadata root: PASS, 234 files, findings [] (logs/audit_layout.log).
- ID scan: no `sub-` token in the two r3 tests, addendum 05 or its receipt. Hits in verification/worker_M2_r3 are the bare literal `sub-` or synthetic `sub-SYN…` names.
- Addendum 05 numbers, re-derived from the pinned family_B JSON, all match:
  - H1b: HCP −10.7%, L1e-4 −3.2%, primary +4.6%, L5e-5 +8.2%;
  - H1a: −12.8%, +2.3%, +3.9%, +5.0%;
  - CI half-widths 0.00203–0.01442;
  - fixture values: raw 0.0326, Holm 0.0652, CI [0.0007, 0.0103]; skewed Holm 0.0321/0.0308, lower bound −0.00144/−0.00142;
  - 508 non-run leaves.
- Independent reimplementations, with no src/ import except the hash-checked loader and positions:
  - Family B primary mean, CI, sign-flip p and Holm for all 4 checkpoints: max abs diff 0.0 vs pinned;
  - Family A D1 cov/corr and D3 intervals, the 7 A2 m12/iid(12, D) ratios, and all E1 reported columns (covPR, /(n−1), iid mean and q2.5, covPR/iid, null mean and q2.5, p_low, jackknife SE): max rel diff ≤ 1.4e-14 (logs/indep_familyA*.log).
- Worker evidence integrity: the S88_v2.json, FULL_v2.json and MUTANTS_SUMMARY.json hashes are as claimed, and 302 of 302 raw-log sha256 match. Controls passed at start and end (88/88, 121/121, 0 skipped). Spot-checked raw logs are genuine pytest output.
- Git, read-only: addendum 03's history is 4ce1917 (blob 725d5077…) then ef27b71, and 0db0336 does not touch it, as addendum 05 §5 says. HEAD now holds the final addendum 05 (a4001f09, root checkpoint commit a910c53 at 06:31:28Z), so the worker's "modified vs HEAD" note is stale. This was not a worker git write.
- Own mutation run, s88 (shipped 88 tests), with my own runner and mutant text: CONTROL 88 passed. All 10 r2b-class mutants SURVIVE: V01, P03, P01, P02, V05, A01, V28, V26, X02, X01. This reproduces the r2b gate independently.

## 2–5. (to be completed after the FULL batch)
