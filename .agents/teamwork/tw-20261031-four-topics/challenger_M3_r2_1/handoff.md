# handoff — challenger_M3_r2_1 (M3 / Topic 2, iteration 2 gate) — Hard

Written 2026-11-01 ~10:15Z. Parent: root coordinator (workflow B). Host: Claude Code subagent (Opus 5.5), no nested spawning.
GPU used: 0 GPU-h (no ledger row). Git writes: none. Installs: none. Production files: not modified.
No HCP ID, old subject token, content hash, file size, voxel count or salt is printed or written by me: every scan is count-only;
fingerprint patterns were streamed from B300 through a pipe and held in memory only. I did not read the other r2 verifiers' folders.

**Verdict: CONFIRMED.** The C4 remediation is a pure relabelling (byte-level token substitution plus the declared field drops),
the sealed originals verify the 18 old pins, no fingerprint remains in the working tree or in git history, and the card verdict
`stop` follows from the saved run records by an independent recomputation. Nonblocking findings N1–N7 below (new mutation
survivors in branches that cannot change this verdict, C4-guard gaps, one undisclosed split-reproducibility erratum, minor errata).

## 1. Observation

All probe outputs: `/home/juke/git/00IITP-AI/verification/challenger_M3_r2_1/`.

**Baseline (09:3xZ, local).**
- C1 `LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`: 67 OK, rc 0 (`c1_protected.txt`).
- `code_sha256_at_freeze.txt`: 33 OK, rc 0 (`code_freeze.txt`). `output_sha256_r2.txt`: 156 OK, rc 0 (`r2_pins.txt`).
- Old pins: `card_sha256.txt` fails exactly hcp_manifest.json + split.json; `output_sha256.txt` 27 OK and fails exactly
  stage0_hcp.json + the 15 `runs/hcp_*/run.json` (`old_card_pins.txt`, `old_output_pins.txt`).
- sha256 of verdict.json (59af05e5…caf68), card (c9bfc60a…41f5), addendum_05 (aa07dd54…c6e5), both new scripts, the three new
  tests and the three new pin files equal the worker's `frozen_artifacts_sha256` list.

**Independent verdict recomputation** (`recompute_verdict_indep.py`, imports neither `src/` nor `scripts/`; t quantile from the
closed-form df-4 Student-t CDF by bisection = 2.7764451051977934 vs scipy 2.7764451051977987) → `recompute_verdict_indep.out.json`:
- NMSE = Σnum/Σden equals the stored `test_nmse` in all 27 runs (rel ≤ 1e-12).
- I1 = +0.001468, t95 [−0.000677, +0.003614]; I2 = +0.004733, t95 [+9.8e−6, +0.009455]. Upper bound of I1 < δ = 0.01 → **stop**.
- F+ gate: gain C vs E 0.03061, C vs S 0.02935 (both ≥ δ, pass). F− gate: gain C vs E −0.01737 (< δ, pass).
- Differences to verdict.json: per-seed I1/I2 0.0 relative; interval ends ≤ 9e-18 absolute; gates 0.0; per-subject seed means 0.0.
- Bootstrap re-implemented with a different seed (12345, 4,000 draws): I1 [0.000238, 0.002902] vs shipped [0.000245, 0.002920].
- Run integrity: 27/27 completed; every `code_sha256` entry in every run.json equals the freeze list (0 mismatches);
  hcp `split_file_sha256` = card split c13b5f21…; perm-file hashes equal the current npz files; test order identical across
  the 15 hcp runs and equal to split.json TEST (16).

**Freeze timeline.** `card_sha256.txt` and `code_sha256_at_freeze.txt` mtime 03:14:34Z; card first committed in 51609c1 at
03:16:27Z (single commit, never changed); `perms_hcp.npz`/`partitions_hcp.json` 03:17:08–09Z and Stage 0 03:24:55Z (after the
freeze, consistent with card §0); earliest run start 03:16:17Z; earliest result (fixture run end) 03:41:34Z; earliest HCP
result 04:10:48Z. Result report and addenda 01–04 last committed ≤ 05:46Z and still pass their old pins.

**Sealed vs sanitized, independent check on B300 .98** (`b300_seal_equivalence.py`, standard library, written by me; it neither
imports nor reads the worker's sanitizer or seal checker) → `b300_seal_equivalence_v2.out.json` (all_ok true):
- 19/19 sealed originals = `c4_sealed_originals_sha256.txt`; 19/19 sanitized copies = `c4_sanitized_sha256.txt`;
  18/18 originals = the old pin lines.
- Original manifest is sorted by content sha256 and each old token is its 16-hex prefix; the map to h00..h87 is positional.
- 17 of 19 files are byte-identical after substituting old→new tokens (all 15 hcp run.json, split.json, stage0_hcp.json);
  520 token leaves mapped, 1,021 float leaves bit-equal, 0 value/type/length mismatches.
- hcp_manifest.json drops exactly `content_sha256`, `file_bytes`, `n_brain_vox`, `sec` (88 each) and adds `c4_sanitized`;
  preprocess.log drops exactly `sec` on 88 lines (90 lines both sides). No old token or content sha in any sanitized file.
- 15/15 runs: `test_num`/`test_den` identical and in the same order; `test_pseudonyms` = mapped original list.
- Card §4 split rule recomputed from the original tokens: TEST, VAL, TRAIN sets equal the sealed split.json; stored lists are
  sorted by token (as `topic2_make_split.py` writes them).
- G4: the 5 burned dev subjects are found 5/5 by the documented salted hash; none of their REST1_LR file sizes occurs among the
  88 manifest sizes, so none is in the manifest. They are still positions 0–4 of the sorted listing (1,084 dirs).
- v1 of this probe had my own bug (compared hash-order lists with the stored sorted lists); preserved with provenance in
  `prev_versions/` (v1 sha 35c0e7b9… equals the copy that ran on B300).

**Fingerprint scans** (count-only; positive controls on the sealed root: old tokens 19 files, full content sha / file sizes /
voxel counts 1 file each):
- Working tree, 13,808 text files: 0 files for old tokens (substring, so 64-hex shas are covered), 0 for full content sha,
  0 for file sizes (word), 0 for voxel counts (word). HCP directory names (1,084, word-bounded): 2 files, both numeric
  coincidences — a microsecond timestamp in an M2 junit xml and integer parts of floats in Topic 1 `extract_primary.jsonl`
  (masked context in my transcript only); 0 real IDs.
- `git log -p --all`, all 141 commits: 0 lines for all five classes; positive control string 4 lines.
- Second HCP-name scan with digit-only boundaries (`(?<![0-9])ID(?![0-9])`, so `<ID>_3T…`, `subj<ID>` and IDs in paths are
  caught; `scan_names_digit_boundary.py` → `.out.json`; v1 kept in `prev_versions/`): working-tree file PATHS 0 hits;
  `git log --all --name-only` paths 0; `git log -p --all` content (457,355 lines) 0. Working-tree contents (14,673 text files):
  142 hits in 19 files, all coincidences by masked context — 72 integer parts of floats, 1 fractional part, 15 digit runs inside
  hex hashes (M2 mutant JSONs, M4 split manifests), and 54 JSON integer count values (`"…D"/"…U"/"…C"/"…T"`, `"observed"`)
  in Topic 1 `extract_primary.jsonl` and its two verification copies (the classifier's json-integer class missed them because
  of a `re.match` anchoring slip in my probe; all 54 contexts were inspected masked). No file under Topic 2 has a hit.
- Self-check after writing this handoff: my 38 verification/metadata files hold 0 old tokens and 0 HCP names.
- `partitions/*.npz`: int64/bool arrays only, no string arrays, 0 token bytes in the zip members (`npz_inspection.json`).

**Tests.**
- B300 .98 CPU, CUDA hidden, nice, 1 process, a copy of the current repo subset (code-hash bundle equal to local):
  `pytest tests/topic2_rgpool` → 92 passed, rc 0, 73 s (`b300_full_topic2_suite.log`; its only 16-hex strings are the two
  synthetic literals of `test_detector_catches_a_reinserted_token`; 0 old tokens).
- Local under `systemd-run --user --scope -p MemoryMax=2500M`: old explicit list 86 passed (`tests_old86.txt`);
  `tests/topic1_lagmotif` 88 passed (`tests_topic1_lagmotif.txt`).
- Worker mutation outputs re-counted: v2 101 KILLED (all rc 1, no collection errors) + 1 SURVIVED (c1:m18); v3 m18 KILLED.

**New mutants** (`run_mutants_c1.py` → `mutants_c1.out.json`; mirror outside the repo; for code mutants the two test files that
are, by grep, the only callers of the verdict functions; for data mutants the three files that read results/docs; baselines
14 and 21 passed):

| mutant | outcome |
|---|---|
| K1 F− gate computed on (S−C)/S instead of (E−C)/E | **SURVIVED** |
| K2 keep rule uses I2 mean instead of I2 lower bound | **SURVIVED** |
| K3 F− boundary `<` → `<=` | **SURVIVED** |
| K4 keep boundary `mean >= δ` → `mean > δ` | **SURVIVED** |
| K5 t df n instead of n−1 | KILLED (test_t_interval_matches_hand_computation) |
| K6 bootstrap subject draw not shared across arms | KILLED (test_hierarchical_bootstrap_null_and_planted) |
| K7 keep never downgraded by F− | KILLED (test_verdict_mapping) |
| K8 verdict script uses final val NMSE instead of test NMSE | KILLED (wiring test) |
| K9 verdict script drops the test-order consistency assert | **SURVIVED** |
| K10 default δ 0.02 / K11 gates on one seed / K12 HCP seeds 0–3 | KILLED (shipped-verdict reproduction) |
| X1 run.json re-adds 16 synthetic full 64-hex "content file sha256" values under a key containing `sha256` | **SURVIVED** |
| X2 run.json re-adds synthetic file sizes under a new key | **SURVIVED** |
| X3 run.json adds uppercase 16-hex tokens | **SURVIVED** |
| X4 stage0_hcp.json re-adds synthetic voxel counts | **SURVIVED** |
| X5 one run's subject order permuted (num/den) | KILLED (shipped-verdict reproduction) |
| X6 docs prose gets a synthetic 64-hex "subject content sha256" | **SURVIVED** |
| X7 preprocess.log gets a 64-hex hash in text | KILLED (test_no_forbidden_subject_key_and_64hex_only_as_sha256_provenance) |
| X8 manifest top-level list of synthetic sizes | **SURVIVED** |

**Split reproducibility.** The frozen `scripts/topic2_make_split.py` run on the sanitized repo manifest (output to my dir only)
gives a different split: TEST overlap 2/16, VAL 0/8, TRAIN 45/64 (`split_reproducibility_check.json`).

**Minor text errata.** worker handoff.md line 25 (and the structured text) abbreviates the new pins as `18d661bf…7570` and
`7a4cceab…b87ca`; the actual hashes are 18d661bf…b87ca (sealed originals) and 7a4cceab…7570 (sanitized). addendum_05 line 167
says "all 103 mutants"; the harness count is 102 (32+47+11+5+7).

**Other.** No worker_M3_r2 process remains on B300 .98. The GPU ledger (last modified 06:12Z) has no r2 row. No conftest.py;
the new tests monkeypatch only through pytest fixtures. No test imports or runs `topic2_c4_sanitize.py` or `topic2_c4_seal_check.py`.

## 2. Logic Chain

1. B1's resolution criterion (reviewer_M3_r1_1 handoff §5: no unsalted tokens, full content hashes or file sizes in any repo
   file; frozen-input hashes verifiable against retained originals) is met: value scans over the tree and all of git history find
   0 tokens, 0 full shas, 0 sizes, 0 voxel counts; the sealed originals pass the 18 old pin lines and their own new pins.
2. "No governed computation changed" holds: 17 files are byte-identical after token substitution and the other two lose only the
   declared fields; every per-subject numeric array is bit-identical and in the same order, so verdict.json is reproducible.
3. The verdict follows the card: my code, independent of the frozen modules, gives I1 hi = 0.0036 < δ = 0.01 → stop, after both
   fixture gates pass; the numbers equal verdict.json to floating-point noise.
4. The freeze precedes every result: card hash file 03:14:34Z and commit 03:16:27Z vs first result 03:41:34Z; partitions and
   Stage 0 (the first FC/box computations) are after the freeze, as card §0 states.
5. The test suite passes on the current bytes (92 on B300 CPU), and C2's old suites pass locally.
6. The surviving mutants K1–K4 and K9 sit in branches that cannot change this run's verdict: stop depends only on I1's upper
   bound, the t interval, δ and the I1 wiring, all of which are killed (K5, K8, K10–K12 and the worker's 102). F− only
   downgrades a would-be keep; keep-vs-modify and boundaries are unreachable at I1 hi = 0.0036; test orders are identical
   (checked). They refute only the generalised headline "All verdict-path … mutants are now killed", not the enumerated 102/102.
7. The surviving data mutants show that test_c4_tokens_r2 guards field names and the 16-hex shape, not fingerprint values;
   because the current state is clean by value scans, this is a regression-guard gap, not a present C4 violation.

## 3. Caveats

- I did not re-run the worker's 102 mutants (heavy suite; host memory); I re-counted their saved outputs.
- My mutants ran against the subset of test files that, by static grep, call the mutated functions or read results/docs; a
  heavier test could in principle also kill a survivor, but none of the other files references stats/verdict functions or results.
- C5 placement deviation (mine): the equivalence check (seconds) and the full 92-test suite (73 s) ran on B300 .98 CPU, nice,
  1 process, CUDA hidden, no Slurm job, 0 GPU-h, using worker_M3_r1's project-local venv and worker_M3_r2's pydeps read-only.
  Reasons: the originals must not leave B300; the local host is at the earlyoom threshold (journal: SIGTERM to another
  python3 at 10:01Z), so a local full suite could kill other teams' processes.
- The burned-subject check used the in-repo salt to locate the 5 dev directories in memory on B300 (the documented
  identification method); only counts were output.
- The two HCP-name hits were classified from masked context in my tool output only.
- Linkage by a data holder (positional order = content-hash rank) was not attempted, by design.
- Not re-attacked in this round (r2 changed no code): T2.1 (where SwiFT ver11 merges), the validity of the T2.2 synthetic
  fixtures beyond rerunning the suite, and GPU re-evaluation of checkpoints (reviewer_M3_r1_1 did it in r1).

## 4. Conclusion

CONFIRMED: B1 is remediated, the sealed originals verify, no fingerprint remains in the tree or history, and the card verdict
**stop** (I1 t95 upper bound 0.36 % < δ = 1 %, both fixture gates pass) is reproduced independently. Nonblocking:

- **N1** New verdict-path survivors: K1, K2, K3, K4 and K9. They cannot change this verdict. Suggested additive tests: an F− case
  where (E−C)/E and (S−C)/S disagree; a modify case with I2 mean > 0 and lower bound ≤ 0; δ boundary cases for F− and keep;
  the verdict script on runs with permuted test order, expecting a failure. The headline "all verdict-path mutants are killed"
  overstates; "102/102 of the listed set" is accurate. Unlike M2's V01 (raw p instead of Holm p on the branch that produced
  the M2 verdict), none of these survivors sits on the branch that produced this verdict: `stop` depends only on I1's upper
  bound against δ, and every mutant of that branch tried here or by the worker (bound, boundary, df, gain sign/denominator,
  I1 wiring, δ default, seed sets, NMSE source) is killed.
- **N2** C4-guard gaps: X1, X2, X3, X4, X6 and X8 pass the suite. The phrase "no stray 64-hex hash in results or docs topic2"
  overstates the test (docs are not checked for 64-hex at all; results accept a 64-hex value under any key containing
  `sha256`). Suggested: a key allowlist for run.json/stage0/manifest, or a B300-side value scan against the sealed
  fingerprints as a recorded gate.
- **N3** Undisclosed erratum: repo `split.json` cannot be re-derived from the repo manifest by the card §4 rule after
  relabelling (TEST overlap 2/16). It is reproducible only from the sealed originals (worker S5, my E5). Record it in an addendum.
- **N4** Text errata: swapped hash suffixes in the worker handoff (line 25); "103 mutants" in addendum_05 line 167.
- **N5** Residual linkage (disclosed by the worker; root/PI ruling). The burned-subject salt beside its salted hashes gives no
  protection beyond positional indexing (BURNED.md names positions 0–4; my E6 matched 5/5). Root item 2 of the worker.
- **N6** The sanitizer and seal checker are not exercised by any test. Their claims are reproduced by my independent check, but
  they are not regression-guarded.
- **N7** My C5 CPU-placement deviation (above). The r2 worker's same deviation is disclosed in addendum_05 §7.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt        # 67 OK
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt                           # 33 OK
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c                 # 156 OK
/home/juke/superclaude-env/bin/python3 -I verification/challenger_M3_r2_1/recompute_verdict_indep.py $PWD /tmp/x.json   # verdict_indep stop
/home/juke/superclaude-env/bin/python3 -B verification/challenger_M3_r2_1/run_mutants_c1.py $PWD <scratch dir> <out.json>  # K1-K4,K9,X1-X4,X6,X8 survive
PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -B scripts/topic2_make_split.py results/topic2/2026-11-01/hcp_manifest.json <scratch>/s.json  # != split.json
# B300 61.107.201.98: upload verification/challenger_M3_r2_1/b300_seal_equivalence.py plus the 19 sanitized files and 4 pin files, then
#   python3 -B b300_seal_equivalence.py /scratch/iitp4/worker_M3_r2/sealed_c4 SAN PINS OUT.json /scratch/data/hcp/download_HCP_REST1_filtered
#   with stdin {"salt":..., "burned":[...]} built from verification/explorer_M3_r1_1 (never written)            # all_ok true
# Fingerprint scans: patterns from b300_patterns.py {tok,sha,bytes,vox,names} streamed by ssh into grep -F -f <(...) over the tree and
#   `git log -p --all` (count only).
```

Invalidation: any change to a pinned hash; any sanitized file differing from `c4_sanitized_sha256.txt`; loss of
`/scratch/iitp4/worker_M3_r2/sealed_c4` before a durable copy exists (the old pins could then no longer be byte-verified).
B300 leftovers of mine: `/scratch/iitp4/challenger_M3_r2_1/` holds only my two scripts and tokenless outputs (copies removed).
