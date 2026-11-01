# handoff — auditor_M3_r3_1 (forensic integrity audit of worker_M3_r3, M3 Topic 2 r3 / T2.4) — Hard handoff

## Forensic Audit Report
**Work Product**: tests/topic2_rgpool/test_verdict_path_guards_r3.py (sha 40149a12…808a), docs/03_empirical_analysis/topic2/2026-11-02_topic2_addendum_06.md (b9176ad6…dab2), results/topic2/2026-11-01/addendum_06_sha256.txt (4ac6d454…12fb), verification/worker_M3_r3/
**Profile**: General Project; integrity mode Development (ORIGINAL_REQUEST has no from-scratch constraint); C1–C8 applied as hard constraints
**Verdict**: CLEAN

## 1. Observation
All probes and outputs are in /home/juke/git/00IITP-AI/verification/auditor_M3_r3_1/ (my own harness, not worker code).
- C1 PROTECTED_HASHES 67/67 rc 0 (start and end, 16:56Z). Receipts: addendum_06 31/31, code_sha256_at_freeze 33/33, output_sha256_r2 156/156, c4_sanitized 19/19, c4_sealed_originals 19/19 vs ~/.local/share/00IITP-AI_sealed/topic2/sealed_c4_from_b300. The old card pins fail exactly 2 and the old output pins exactly 16 (the r2 set disclosed in addendum_05 §2; those files' mtimes are r2, 2026-11-01 16:33 KST). verdict.json 59af05e5…af68 unchanged.
- Frozen code: every src/topic2_rgpool and scripts/topic2_*.py file is pinned (code freeze, or for the r2 c4 helpers output_sha256_r2), all OK. The 14 shipped test-dir files are pinned in output_sha256_r2, all OK. The only file newer than that pin in tests/topic2_rgpool is the new r3 file.
- Ownership: in the M3 paths, the only files modified since dispatch (14:58Z) are the 3 owned files. Other new files are FU-A..E and topic3_h2 paths (other teams). The sealed store is untouched (0 files newer than dispatch).
- Test source review: an independent card-§8 oracle (`card_verdict`) on a dyadic grid; one-rule boundary tests; end-to-end runs of the frozen script on synthetic records through helpers.ROOT; [erratum] tests pin the frozen labels and assert `card_reading`. No hardcoded pass strings and no self-certifying constants. The shipped-record test reads results/ and asserts preconditions that can fail.
- a01 spec provenance: the 23 specs are byte-identical (file/old/new) to the declared sources (p07_specs.json; p05 MUT; run_mutants_c1 CODE; m03 MUT), read by AST. Source shas match, every anchor occurs once in the frozen file, V01–V11 are complete, and p05 V equals p07 V. mutation_specs.json sha c10e4f3a… is identical to my copy.
- Independent mutation legs (local, ≤2 pytest, nice, timeout 900, FU cards excluded from the docs copy):
  - Leg A (12 shipped files): baseline 92 passed; 20 non-control mutants SURVIVED; 3 controls KILLED.
  - Leg B (new file only): baseline 24 passed; 19 KILLED (V01–V11, K1, K2, W04–W08, W12); W09 SURVIVED; CTRL_t_df_n and CTRL_boot SURVIVED; CTRL_hcp KILLED.
  - Leg C (union): baseline 116 passed; 22 KILLED; baseline and W09 survive. V06 was first INVALID (rc −15, external SIGTERM on a shared host); the rerun gave KILLED (2 failed).
  - a12: 72/72 per-leg rows agree with the worker's mA/m01/mC outputs, including the killing-test names.
- Leg D (a08): the baseline and the 20 non-control mutants rewrite verdict.json byte-identical (59af05e5); the 3 controls differ (4d062c7e, fdbf65ee, 9cd248a6) and all give `stop`.
- W09: stats.t_interval returns hi = m + q·se with q > 0 and se ≥ 0, so hi ≥ m. Hence hi < δ ⇒ m < δ ⇒ not i1_survives, and the W09 condition equals the original on all t_interval outputs: equivalent.
- Errata: E1 (else branch of `if ok:`), E2 (`bool(fp)` with None), E3 (`fm is not False`), E4 (dict overwrite in glob order) and E5 (`assert`) are present in the frozen code. The card §7.2/§5/§8 quotes are verbatim. a10 reproduces E4 (the failed rerun last in glob order gives no_verdict) and E5 (plain rc 1 with the order message; `-O` rc 0 and `keep`). Shipped preconditions: F+ 3.061/2.935 %, F− −1.737 %, I1 +0.147 % [−0.068, +0.361] %, last F+ end 03:42:08Z < first hcp start 03:44:51Z.
- Leakage (a06/a06b, counts only), scope = the 51 worker files (test, addendum, receipt, verification/worker_M3_r3/**, worker metadata):
  - 0 hits for: salt variants, the 5 burned hashes, the 5 dev IDs (recovered in memory with the sealed salt: 5/5), the 88 original pseudonyms, the 88 content sha256, the 88 exact file sizes, and the 1,084 B300 HCP six-digit names streamed in memory.
  - The 50 six-digit runs all sit inside sha256 file digests. The 8 hex16 hits are float digit strings and synthetic fixture tokens.
  - The 2 `sub-` hits are pytest output quoting "sub-optimal" from the FU-B card.
  - Repo-wide: salt variants in 0/19,891 tree files and 0 in all git objects (840 MB batch); burned hashes in 0 git objects.
  - Sealed salt: sha = root record; 0400/0700/0700; not in a git tree; the old repo path is absent.
- Git: commits since dispatch are only "Chavis Autocommit docs(auto)" (host daemon) plus one root checkpoint at 15:01Z. addendum_06 was auto-committed at 15:35Z as a draft with `<<MUTATION_TABLE>>`/`<<N_FILES>>`/`<<REGRESSION>>` placeholders (c234f01) and as final at 15:50Z (34f4b30 = current bytes). So the results were filled in after the runs, not written in advance. No stash, and the reflog shows commits only.
- Compute: connectome sacct shows 51 worker jobs (1 wM3r3_suite, 48 wM3r3mut, 2 wM3r3_final), all CPU (cpu/mem TRES, no gres/gpu). 25 mutant jobs FAILED (= 3 leg-A control kills + 22 leg-C kills) and wM3r3_final i FAILED (115+1). These counts match the worker's legs. /storage/connectome1/iitp4_verify/worker_M3_r3 is absent, squeue is empty, there is no ledger row and 0 GPU-h. The connectome code.sha checks 40/40 against local.
- Regression (mine): old 86 passed (STRICT_E2E=1); topic1_lagmotif 88 passed; the new file in the repo 24 passed. Full topic2 suite: current docs give 115 passed + 1 failed (test_outputs_no_ids, caused by the FU-B card's "sub-optimal"); FU cards excluded give 116 passed. C4 pair with FU cards excluded: 11 passed. Whole-run audit_layout: PASS, 405 files, 0 findings.

## 2. Logic Chain
1. Frozen code, tests and receipts are unchanged (C1, pins) → the new tests run against the real frozen implementation.
2. The specs are verbatim from independent verifiers (a01) and my harness reproduces every status and killing test (a12) → the kill evidence is real, attributable and not fabricated.
3. The controls are killed in A and change bytes in D → legs A and D can detect changes, so the survivals in A and the byte-identity in D are meaningful.
4. The W09 equivalence holds analytically from t_interval's code.
5. The errata are real code-vs-card departures, documented in an addendum without editing frozen files. The shipped preconditions rule them out → the `stop` verdict is unchanged.
6. No identifier, salt or pseudonym is in the worker outputs, and no salt is in the repo or git → no C4 violation by the worker. The positional residual is pre-existing and honestly disclosed.
7. No GPU, no git writes by an agent, no writes outside ownership, nothing left running → no compute or process violations.

## 3. Caveats
- Nonblocking N1: addendum_06 §6 says "test_c4_tokens_r2.py + test_outputs_no_ids.py 11 passed with this addendum present", but no log is retained. The worker's progress.md (15:50Z) records test_outputs_no_ids failing on the FU-B card. I reproduced 11 passed only with the FU cards excluded. The statement omits that condition. The handoff and the structured return disclose the 115+1 red state correctly.
- Nonblocking N2: the current full topic2 suite is red (115+1) because of the FU-B card (another team's file). It is not an M3 defect, but the T2.4 "no regression: all suites" item is not green on the current tree until the FU-B owner rewords "sub-optimal" (root action).
- Nonblocking N3: the positional dev-subject residual ("positions 0-4 of the sorted listing") is pre-existing and in committed blobs. addendum_06 repeats it as a disclosure. T2.4's "no repo content lets HCP IDs be recovered" holds only for the salted-hash channel; the positional channel needs off-repo B300 data. PI ruling pending.
- I did not rerun the legs on connectome; my local legs used superclaude-env (torch 2.11 dev, numpy 2.3.5, scipy 1.15.3).
- Worker progress.md timestamps were partly estimated, as disclosed. The test file mtime (15:04Z) is earlier than the logged 15:07Z. This is cosmetic.
- Leftover: my mirror copies (verification/auditor_M3_r3_1/mirror_*, a08_outputs, a10_work; 13 MB total) could not be deleted because the harness denied `rm -rf`. They are copies of repo files only (sanitized results, no sealed material) and can be removed by root.

## 4. Conclusion
CLEAN. No hardcoded results, facades, tests that cannot fail, fabricated logs, pre-freeze results, silent fallbacks, ID leakage, protected-path writes, GPU use or git writes were found. The worker's T2.4 claims (attributable kills of V01–V11 plus K1, K2, W04–W08 and W12, W09 equivalent, errata E1–E5, the shipped `stop` unchanged, salted-hash containment) reproduce independently. Nonblocking: N1 (unlogged "11 passed" claim lacking its condition), N2 (the FU-B card turns the shipped C4 test red), N3 (positional residual for a PI ruling).

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c
V=verification/auditor_M3_r3_1
python3 $V/a01_spec_provenance.py $PWD /tmp/x.json
python3 $V/a02_mutation_harness.py build $PWD <NEWMIRROR> --exclude-fu
python3 $V/a02_mutation_harness.py run <NEWMIRROR> $V/specs_all.json out.json {A|B|C}
python3 $V/a08_verdict_invariance.py <NEWMIRROR> $V/specs_all.json <OUTDIR> out.json
python3 verification/auditor_M3_r3_1/a12_compare.py   # run from verification/
```
Invalidation: any change to src/topic2_rgpool, scripts/topic2_*.py, the shipped tests, the new file, addendum_06 or its receipt.
