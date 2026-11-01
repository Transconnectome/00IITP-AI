# Handoff — explorer_M3_r2_2 (M3 / Topic 2, iteration 2, explorer 2 of 2) — Hard

Written 2026-11-01 ~07:00Z. Read-only investigation; no production file was changed. GPU use 0 GPU-h (no ledger row).
Probes and raw outputs: /home/juke/git/00IITP-AI/verification/explorer_M3_r2_2/ . No subject token, content hash,
file size, salt or HCP ID is printed or written in any of my files (all scans are count-only; throw-away copies
lived in my private scratchpad outside the repo and were deleted, `*_deleted: true` in each output).

## 1. Observation

O1 Gate record: the r1 gate failed only on reviewer_M3_r1_1 REQUEST_CHANGES, B1 (C4). The other 4 verifiers were
APPROVE / CONFIRMED / CONFIRMED / CLEAN with no blocking issue; the science (T2.1–T2.3, verdict `stop`) reproduced
in all 5 reports. B1 resolution criterion, verbatim (reviewer_M3_r1_1/handoff.md §5): "B1 is resolved when no repo
file carries the unsalted content-hash tokens, full content hashes or file sizes, and the card's frozen-input
hashes remain verifiable against the retained originals."

O2 Code (frozen, in results/topic2/2026-11-01/code_sha256_at_freeze.txt, 33 files):
- src/topic2_rgpool/data.py:84-85 `pseudonym(content_sha256) -> content_sha256[:16]` (unsalted).
- data.py:88-89 split order = sorted by sha256(split_salt + pseudonym); scripts/topic2_make_split.py:19 default
  salt "topic2-m3-split-2026-11-01" (also printed in split.json "salt" and in card §4). So the test/val/train
  order is a public function of the content hashes of the exact 88 files.
- scripts/topic2_preprocess_hcp.py:35 writes content_sha256, pseudonym, file_bytes; :47 n_brain_vox; :85 manifest
  subjects sorted by content_sha256; :86-90 manifest has created_utc / elapsed_sec / per-file sec, so the manifest
  is NOT regenerable byte-identically (originals must be retained, not re-derived).
- scripts/topic2_verdict.py:59 reads `recs[k]["test_pseudonyms"]` (asserts one test order across runs);
  :71 `S.verdict(..., bool(fp), fm is not False)` (a missing F- gate counts as pass; latent, no effect here).
- tests/topic2_rgpool/test_outputs_no_ids.py (post-freeze, not in the freeze list) reads
  RESULTS/hcp_manifest.json `subjects[].pseudonym` and checks only `"pseudonym": "<16 hex>"` patterns.

O3 Count-only token scan (probe_token_scan.py → token_scan.out.json; 15,664 working-tree files, 44 commits since
2026-10-31 on all refs; token file in my scratchpad, mode 600, deleted):
- Exactly 19 repo files carry content-hash pseudonyms (P), all under results/topic2/2026-11-01/:
  hcp_manifest.json (88 full hashes H, 88 P, 88 exact file sizes B, 88 n_brain_vox V), logs/preprocess.log (88 P),
  split.json (88 P), stage0_hcp.json (16 P), runs/hcp_{E,C,S}_s{0..4}/run.json (16 P each). Same 19 as the
  reviewer's 06:09Z list; no new file since (verifier dirs written after 06:09Z: 0 hits).
- explorer_M3_r1_1's dev-subject salt (dev_subject_salt.txt) sits in the same folder as the 5 salted dev hashes,
  which appear in 3 files: dev_subjects_BURNED.md, probe_stage0_hcp_dev.log, probe_stage0_hcp_dev.out.json.
- 3 single V hits in Topic 4 files (results/topic4/..., verification/auditor_M4_r1_1/..., verification/victory_M4/...)
  are coincidental numbers in another topic (not HCP files).
- Git history: 0 hits in 44 commits. `git ls-files results/topic2 verification` = 0 tracked files.

O4 Commit scope: the root checkpoint loop /tmp/claude-1000/-home-juke/1157b38c-…/scratchpad/autocommit/autocommit.sh
(PID 3270989, 900 s) commits `docs/03_empirical_analysis/topic*/**` (all file types) and
`.agents/teamwork/tw-20261031-four-topics/**/*.md`, guarded only by a literal-ID list. The host chavis-autocommit
daemon delegates 00IITP-AI to that script (~/.agents/registry/governance.json "delegate_or_skip"). Last 3 commits
(a910c53, b91143c, 08f7b6f) touched only .agents/teamwork and docs/03_empirical_analysis. results/ and
verification/ are never committed by it.

O5 Pins: card_sha256.txt (8 lines) pins hcp_manifest.json and split.json; output_sha256.txt (43 lines) pins
stage0_hcp.json and the 15 hcp run.json; preprocess.log is not pinned anywhere. Current state (06:58Z):
card 8/8 OK, output 43/43 OK, code freeze 33/33 OK, C1 67/67 rc 0 (pins_pre_redaction_check.txt, c1_check.txt).

O6 Redaction invariance (probe_redaction_invariance.py → redaction_invariance.out.json): replacing only the
`test_pseudonyms` values of the 15 hcp run.json by HMAC tokens (same keys, same order) and running the FROZEN
scripts/topic2_verdict.py gives verdict bytes identical to the pinned verdict.json (sha 59af05e5…caf68), rc 0.

O7 Full redaction prototype on a throw-away mirror (probe_redaction_prototype.py → redaction_prototype.out.json):
19 files rewritten; 0 H/P/B/V tokens left; every subject token matches ^hk_[0-9a-f]{16}$; split union = manifest
tokens; every run's test order = split test list = stage0 order; manifest subjects carry only {pseudonym, qc, T};
85 other result files byte-identical; frozen verdict script reproduces pinned verdict.json bytes; shipped
tests/topic2_rgpool 55 passed with results/ = the redacted copy. Pins superseded by the redaction (sha256sum -c in
the mirror): card_sha256.txt exactly 2 lines (hcp_manifest.json, split.json); output_sha256.txt exactly 16 lines
(stage0_hcp.json + 15 hcp run.json); code_sha256_at_freeze.txt 0 lines. All original files are written as
json.dumps(indent=1) without trailing newline (checked), so a structured rewrite is byte-deterministic.

O8 Verdict-path mutants (probe_mutants.py → mutants.out.json; mirrors under scratch, CUDA hidden):
| mutant | shipped 55 tests | proposed guards (verification/explorer_M3_r2_2/proposed/test_verdict_path_guards_r2.py) |
|---|---|---|
| control | 55 passed | 5 passed |
| M1 stats.verdict stop rule on mean instead of upper bound | 55 passed (survives) | killed |
| M2 stats.relative_gain sign flipped | 55 passed (survives) | killed (3 tests) |
| M3 topic2_verdict.py I1 computed against S | 55 passed (survives) | killed |
| M4 topic2_verdict.py ignores the F- bias flag | 55 passed (survives) | killed |
| M5 metrics.masked_sq_terms drops the SimMIM mask weight | 55 passed (survives) | killed |
No shipped test references relative_gain, masked_sq_terms or scripts/topic2_verdict.py (grep). Baseline shipped
suite on CPU: 55 passed in 95.6 s (baseline_tests_topic2.txt).

O9 PI decisions: orchestrator/PI_DECISIONS_2026-11-01.md items 2 (HCP-YA OA public under C6, subject to DUT: no
redistribution, no re-identification) and 3 (δ = 1 % for M3) are in commit a06f435 at 2026-11-01T03:01:27Z, i.e.
before the card freeze at 03:14:34Z. Card §4 and §8 line 161 and report line 216 still say "pending PI".
src/topic2_rgpool/vendor_swift_ver11/SOURCE.md:12 names tests/topic2_rgpool/test_vendor_provenance.py, which does
not exist (SOURCE.md is in the code freeze list).

O10 Environment: B300 .98 reachable; /scratch/iitp4/worker_M3_r1 exists (142 GB: code, hcp, runs incl.
checkpoints, logs, venv) and holds the original token-bearing copies; Slurm is installed (sinfo: b300-01 alloc,
b300-02/03 mix, b300-04 idle), matching RESUME addendum 3 (all further B300 GPU use via Slurm). GPU ledger total
≈11.99 GPU-h of 64. ~/.agents is a git work tree and ~/.agents/private is not git-ignored there; /home/juke is not
a git work tree.

## 2. Logic Chain

L1 (O1) Only B1 blocks; fixing B1 cleanly turns the r1 REQUEST_CHANGES into APPROVE by its own stated criterion.
Nothing scientific needs to change: no rerun, no GPU.
L2 (O2, O5) data.py, preprocess and make_split are frozen code; editing them breaks the 33-file code-freeze pin.
So the fix is a NEW post-freeze, non-governing redaction script applied to repo copies of outputs.
L3 (O2, O7) The frozen verdict script and the shipped C4 test read the keys `test_pseudonyms` and
`subjects[].pseudonym`; keeping key names and list order and replacing only the values keeps both working
(O6, O7: verdict bytes identical, 55 passed). Renaming keys or reordering arrays would break the frozen script or
change the hierarchical-bootstrap bytes in verdict.json.
L4 (O2) Positional indices in manifest order (sorted by content hash) or split order (public salt) would be
recomputable from the files, i.e. not a fix. Keyed tokens (HMAC under an off-repo key) meet C4's "salted hash"
letter; a visibly different format (`hk_` + 16 hex) lets tests assert positively and avoids confusion with content
pseudonyms. n_brain_vox and per-file sizes are exact per-subject fingerprints and serve no repo-side check, so the
repo manifest should drop them.
L5 (O2 manifest not regenerable, O5, O7) The 18 superseded pin lines can only verify against retained originals.
So the originals (and preprocess.log, which no pin covers) must be copied byte-identically, sha-verified BEFORE the
in-repo overwrite, into a durable lab-only store outside any git work tree; B300 /scratch is wiped on VM stop and
~/.agents/private is inside a git tree (O10). Mirroring the repo-relative paths in the store lets the existing pin
files verify there with plain `sha256sum -c`.
L6 (O4) The commit loop picks up anything in docs/03_empirical_analysis/topic*/ and any .md in the run metadata;
its guard does not know tokens. So no token, token map, key or salt may be written there (addendum, handoffs).
L7 (O3) The explorer salt next to the 5 salted dev hashes makes those hashes brute-forceable (6-digit HCP ID space).
Moving the salt off-repo makes the 3 hash-bearing files keyed hashes; it is one file but lives in explorer_M3_r1_1's
folder, so root must do it or assign it. A fresh strict r2 reviewer applying B1's own logic would likely block on it.
L8 (O8) Five verdict-path mutants survive the shipped suite. In r1 this was non-blocking only because verifiers
recomputed independently; M2's gate history shows fresh challengers REFUTE on exactly this class. Additive guard
tests (no src/scripts change) kill all five on CPU in ~6 s.
L9 (O2, O7) Residual after redaction: per-subject outcome arrays stay in split order; anyone holding the exact
B300-staged HCP files can recompute pseudonyms → public-salt order → which position is which subject, or match
per-subject values by rerunning the pipeline. This needs the staged file set (B300, where HCP IDs are already
directory names) and is inherent to publishing per-subject results of a reproducible public-data analysis. It
must be disclosed, not described as "unlinkable".

## 3. Caveats

- I did not implement the fix; the prototype ran on throw-away copies with a discarded random key.
- Linkage was argued, not performed (by design). I did not inspect B300-side files beyond a directory listing.
- I did not read ~/enigma_ocd; I did not rerun GPU checks; r1 verifiers re-evaluated checkpoints 4 times.
- The off-repo path I suggest is a proposal; root/PI may choose another location meeting L5.
- The residual in L9 is a judgement call under C4; I recommend disclosure plus an optional one-line PI ruling.
- Only 5 mutants were tested; challengers reported more survivors (canonical slot order, dense-core seed rule,
  Hungarian placement, train.py loss/eval/mask pairing, gate averaging, bootstrap seed resampling). Their exact
  diffs are in verification/challenger_M3_r1_1/mutation/ and verification/challenger_M3_r1_2/.
- Independence: I read the r1 gate record and the reviewer_M3_r1_1 handoff (they are in my dispatch); I did not read
  explorer_M3_r2_1's outputs.

## 4. Conclusion — strategy for worker_M3_r2 (0 GPU-h, no rerun, CPU ≈ 45 min)

Step 0 Preflight, save outputs: C1; code freeze; card and output pins (all OK now); token scan baseline (copy and
adapt probe_token_scan.py into the worker's own verification dir, loading tokens from the repo manifest now and
from the off-repo originals afterwards).

Step 1 Off-repo store R, e.g. /home/juke/offrepo_private/00IITP-AI/topic2_2026-11-01 (mode 700). Assert
`git -C R rev-parse` fails. Not under ~/git, not ~/.agents, not only B300 /scratch. Optional second durable copy
on connectome lab storage (mode 700).

Step 2 Copy the 19 originals into R at their repo-relative paths (cp -p), then verify: the 18 pinned ones against
card_sha256.txt / output_sha256.txt run inside R; record preprocess.log sha. Fail closed on any mismatch.

Step 3 Key: 32 random bytes written directly to R/keys/…key (0600), never printed; token map token↔pseudonym
stored only in R. Record only a key fingerprint (e.g. sha256(key)[:16]) in the repo.

Step 4 New script scripts/topic2_redact_subject_tokens.py (post-freeze, non-governing):
token(p) = "hk_" + HMAC-SHA256(key, p).hexdigest()[:16]; manifest subjects → {pseudonym: token, qc, T}, sorted by
token, top-level counts kept, plus a "redaction" note; split.json / stage0_hcp.json / 15 hcp run.json: same keys
and order, values swapped; preprocess.log: per-line JSON, pseudonym values swapped; json.dumps(indent=1), no
trailing newline; write via temp file + os.replace only after the R copy's sha is verified; refuse a key path inside
the repo or any git work tree. Blueprint: verification/explorer_M3_r2_2/probe_redaction_prototype.py.
Write results/topic2/2026-11-01/redaction_2026-11-01/redaction_record.json (per path: original sha = old pin,
redacted sha, removed fields, method, key fingerprint, R path; no tokens, no map) and a new complete pin file
results/topic2/2026-11-01/redaction_2026-11-01/output_sha256_post_redaction.txt. Never edit card_sha256.txt,
output_sha256.txt, the card, the report or any frozen file.

Step 5 Explorer salt (needs root ownership assignment): copy verification/explorer_M3_r1_1/dev_subject_salt.txt to
R (sha verified), remove the repo copy, leave dev_subject_salt.MOVED.md (sha of the salt, R path, date, mover).

Step 6 New scripts/topic2_verify_redaction.py: repo mode (post-redaction pins, positive token-format assertions,
cross-file consistency, frozen verdict regenerates pinned verdict.json bytes) and `--offrepo R` mode (the 18 old
pins verify in R; recomputing the redaction from R originals + key reproduces the repo bytes; salt moved). Counts
only on stdout.

Step 7 New tests (additive): tests/topic2_rgpool/test_redaction_r2.py — every subject-token field matches
^hk_[0-9a-f]{16}$; no 64-hex content hash, no content_sha256 / file_bytes / n_brain_vox key anywhere under
results/topic2/2026-11-01; manifest/split/run/stage0 token sets consistent; frozen verdict script on the repo runs
reproduces verdict.json bytes; synthetic unit tests that the redaction output never equals sha256(bytes)[:16],
depends on the key, and refuses an in-repo key. Adopt verification/explorer_M3_r2_2/proposed/
test_verdict_path_guards_r2.py as tests/topic2_rgpool/test_verdict_path_guards_r2.py (kills M1–M5). Leave
test_outputs_no_ids.py unchanged (it passes but is vacuous for hk_ tokens; the new test covers it positively).

Step 8 Addendum 05 (docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_05.md, written after Step 4, no
tokens): (a) the B1 redaction, why, the 19 files with original/redacted file sha256, which 18 old pin lines now
verify only in R and the exact commands; that every governed number and the verdict are unchanged (verdict bytes
reproduce); (b) residual linkage L9, stated plainly; (c) N1: δ = 1 % and HCP-as-public were decided by the PI before
the freeze (commit a06f435, 03:01:27Z); (d) SOURCE.md test-name error (frozen, corrected here only);
(e) addendum 04 loss range correction (per reviewer_M3_r1_2 / challenger_M3_r1_2: 100-step means 1.0561 at step 100, then 0.9978–1.0036; re-read train_log before writing); (f) I2 is confounded (per reviewer_M3_r1_2: S box dispersion 1.56–1.67 vs C 1.47 cells)
with box compactness (S less compact than C), so "connectome-specific" is qualified; (g) report §3.4 is post hoc,
not a headline; (h) per-seed I1 tracks plateau-escape timing (E_s0, E_s2 escaped last); rank-288 decoder bottleneck
as a ceiling cause, so follow-up options A/D/E before B; (i) topic2_verdict.py `fm is not False` latent defect,
documented, script unchanged; (j) test commands must set CUDA_VISIBLE_DEVICES="" (the smoke test used the local GB10
when visible); (k) worker_M3_r1 timestamp corrections (05:42Z/05:40Z claims vs 05:30–05:37Z files).

Step 9 Final checks: C1 rc 0; tests/topic2_rgpool all pass (55 + new) with CUDA hidden; old 86; topic1_lagmotif;
code freeze 33/33; card pins 6/8 OK in repo with the 2 named lines superseded and 2/2 OK in R; output pins 27/43 in
repo with the 16 named lines superseded and 16/16 in R; post-redaction pins rc 0; verify_redaction both modes;
token scan → 0 hits in the working tree and in git history; ID scan of new/changed files with B300 names held in
memory → 0; whole-run audit_layout PASS; mutant demo (copy of probe_mutants.py) → M1–M5 killed.

For root: (1) assign the explorer salt path to the worker or move it yourself; (2) record N4 (worker's printed
example ID, tool output only); (3) optionally ask the PI one yes/no line: "accept the disclosed residual (per-subject
values in a split order recomputable from the B300-staged HCP files) under decision 2 (recommended: accept)";
(4) in r2 verifier dispatches: Slurm-only for any B300 GPU use (none needed), give the R path for off-repo checks,
CUDA_VISIBLE_DEVICES="" for local tests; (5) B300 /scratch/iitp4/worker_M3_r1 (142 GB, original copies +
checkpoints) cleanup is a root/PI decision; keep it if follow-up option E is wanted.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI/verification/explorer_M3_r2_2
S=<private scratch dir outside the repo>
/home/juke/superclaude-env/bin/python3 -B probe_token_scan.py /home/juke/git/00IITP-AI $S /tmp/ts.json       # 19 results files + 4 explorer_M3_r1_1 files; 0 commits
/home/juke/superclaude-env/bin/python3 -B probe_redaction_invariance.py /home/juke/git/00IITP-AI $S /tmp/ri.json # byte_identical true
/home/juke/superclaude-env/bin/python3 -B probe_redaction_prototype.py /home/juke/git/00IITP-AI $S /tmp/rp.json  # 55 passed; 2 + 16 pins superseded
/home/juke/superclaude-env/bin/python3 -B probe_mutants.py /home/juke/git/00IITP-AI $S /tmp/mu.json              # M1..M5 survive shipped, killed by proposed
grep -n "def pseudonym" -A1 /home/juke/git/00IITP-AI/src/topic2_rgpool/data.py
grep -n "test_pseudonyms\|fm is not False" /home/juke/git/00IITP-AI/scripts/topic2_verdict.py
git -C /home/juke/git/00IITP-AI log --format='%h %cI' -- .agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md
```
Invalidated if: any results/topic2 file or pin changes before the fix; frozen code changes; the commit loop's scope
changes to include results/ or verification/; a commit containing the tokens appears; the frozen verdict script no
longer reproduces verdict.json from token-swapped records.
