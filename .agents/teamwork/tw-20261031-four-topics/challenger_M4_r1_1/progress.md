# progress — challenger_M4_r1_1
Last visited: 2026-11-01T02:42Z
- 02:33Z dispatch received; DISPATCH.md, BRIEFING.md written; role/runtime/ACCEPTANCE/ORIGINAL_REQUEST/RESUME/sci-pipeline read.
- 02:38Z read card, src/topic4_resu (all), scripts topic4_run/analyze, key tests, worker handoff + mutation list.
- 02:40Z chronology: card birth 02:03:57Z (never modified), card/code hashes 02:04:41Z, ledger tuning_start 02:04:52Z, confirm_start 02:07:43Z; all freeze/doc hash files verify (sha256sum -c, 0 non-OK). Git has no pre-result commit (checkpoints 11:16/11:31 KST are post-result).
- Next: plan -> advisor -> independent recompute, data-path re-implementation, targeted rerun, new mutants, analyze adversarial inputs, T4.1 re-check.
- 02:45Z hygiene before: git status snapshot (55 lines) in verification/challenger_M4_r1_1/git_status_before.txt; PROTECTED_HASHES rc 0.
- 02:46Z ledger output_sha256 of 55 confirm files all match; confirm mtimes 02:08:14–02:14:21Z. FINDING (low): output_sha256.txt records logs/analyze.log as the EMPTY-file hash (hashed before stdout flush) -> `sha256sum -c output_sha256.txt` fails on that one line.
- 02:47Z indep_refs.py (own loader/detrend/split/ridge/R2, no topic4 import): population, sites, valid_T, split all equal; constant/persistence/identity/PCA24 per-subject R2 match saved to <=1e-14 (h=1,2); no lambda mismatch. Per-site lag-1 autocorr 0.15–0.48, no outlier.
- 02:49Z indep_stats.py (own bootstrap B=4000, card rules re-typed): points exact; CIs within <=2.1e-4; verdicts H1 stop, S1 killed, S2 supported, S3 non-inferior all agree; H1 per-fold all negative (-0.0015..-0.0028); C4>C1 in 12.3% of subjects; C3 10/50 unstable.
- 02:58Z rerun_subset.py (worker code, own outdir/cache): 14 tasks (C1,C4 x5 folds; C3 f2; C4DP f0; mlp:0 f0; refs f0) byte-IDENTICAL to saved; C3 unstable at identical steps.
- 03:00Z indep_psp.py (own PSP via Cholesky, protected generator, own data path): C1/C4/C5 instances in folds 0,2,3 match saved per-subject R2 <=4e-11; lambda and rank identical.
Last visited: 2026-11-01T03:01Z
