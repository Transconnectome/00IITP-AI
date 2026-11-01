# Topic 2 card — addendum 06 (2026-11-02 KST = 2026-11-01 ~15:xxZ, worker_M3_r3, written AFTER all results)

Everything below is post hoc. No governed computation changed: no training, Stage 0, preprocessing, partition or
verdict computation was rerun to produce a new governed output, and no frozen file was edited (card, architecture
note, result report, addenda 01–05, `src/topic2_rgpool/**`, `scripts/topic2_*.py`, the 12 shipped test files and
every existing receipt; `code_sha256_at_freeze.txt` 33/33, `output_sha256_r2.txt` 156/156). The card verdict stays
**stop** (`results/topic2/2026-11-01/verdict.json`, sha256 59af05e5…af68, unchanged). GPU used: 0 GPU-h.

## 1. Why this addendum exists: the r2 gate

The M3 r2 gate failed because challenger_M3_r2_2 REFUTED (record: `.agents/teamwork/tw-20261031-four-topics/
orchestrator/M3_r2_gate_record.json`). It raised three blocking items; the other four verifiers passed and every
verifier reproduced the verdict.
1. A C4 leak: a 32-character dev-subject salt sat in `verification/explorer_M3_r1_1/` beside 5 salted hashes of
   burned HCP dev subjects. Root moved the salt off-repo (~19:3x KST); §5 re-verifies that containment.
2. Eleven verdict-path mutants (V01–V11) survived the full 92-test suite. §4 adds a test file that kills them.
3. An undisclosed card-vs-code defect (erratum E1 below).
None of the three changes the shipped verdict.

## 2. Errata: where the frozen verdict code departs from the card

The card governs. `scripts/topic2_verdict.py` and `src/topic2_rgpool/stats.py` are frozen and are not edited; a
reader applies the reading rule in §2.6 to any `verdict.json` the frozen script writes.

**E1 (certain). F+ fails, Stage 1 not run → script says `no_verdict`, card says `inconclusive`.** Card §7.2: "If F+
fails, Stage 1 is not run. The verdict is then `inconclusive` (measurement capacity)". The frozen script computes
the verdict only when all 15 hcp runs are complete; otherwise it returns `no_verdict`, reason "Stage 1 incomplete"
(`scripts/topic2_verdict.py`, the `else` branch of `if ok:`). Following the card therefore makes the script label a
measurement-capacity failure as a software failure, which sci-pipeline G8 forbids ("software failure ≠ scientific
null"). Pinned by `test_erratum_e1_fplus_failure_without_stage1`.

**E2 (interpretive). Missing or failed F+ runs → script says `inconclusive` ("measurement-capacity gate failed").**
When an F+ run is missing or failed the gate is not computed (`pass` null) and `bool(None)` is False, so
`stats.verdict` reports an F+ failure. Card §5: a run that fails twice "leaves the seed missing and the verdict
becomes `no_verdict`". E2 is the mirror image of E1: a software failure labelled as a capacity failure. The card
does not name the label for a missing fixture gate; this addendum reads §5 as governing (no_verdict).
Pinned by `test_script_missing_fplus_runs_do_not_count_as_a_pass` (V07) and
`test_script_failed_fixture_run_is_not_counted[Fplus]` (V10).

**E3 (interpretive; supersedes addendum_05 §4 item 8). Missing or failed F− runs count as an F− pass.**
`scripts/topic2_verdict.py` passes `fm is not False`, so an F− gate that was not computed (`pass` null) lets a
would-be `keep` stay `keep`. Card §7 heading: the fixtures "must pass before any real-data number governs a
decision"; card §5: missing runs → `no_verdict`. Strict reading (adopted in §2.6): any missing or failed F− run →
`no_verdict`. Narrow alternative (F− matters only for `keep`): a `keep` with an uncomputed F− gate → `inconclusive`;
`stop` and `modify` stand. Under both readings the frozen `keep` is wrong. Pinned by
`test_erratum_e3_missing_fminus_runs_leave_keep` and `test_script_failed_fixture_run_is_not_counted[Fminus]`.

**E4 (latent). Duplicate (source, arm, seed) records are resolved by filesystem order.** `load()` keeps the record
that comes last in `glob.glob` order, which is directory order, not sorted order. With a completed run and a failed
rerun under the same key, the verdict is `keep` or `no_verdict` depending on which directory the filesystem lists
last (probe B: 3 layouts, the rule held in all 3). Card §5 has a rerun replace a failed run; it does not say how to
pick between two records.

**E5 (latent). The test-order guard is an `assert`.** Under `python -O` (or `PYTHONOPTIMIZE`) the check "test
subject order differs between runs" is removed. Probe C: on the same mis-ordered records the plain script exits 1
with that message; with `-O` it exits 0 and writes a `keep` verdict, so the hierarchical bootstrap would pair
different subjects without any error. The new V09 test strips `PYTHONOPTIMIZE` before it runs the script.

### 2.6 Reading rule (executable)

`card_reading(v)` in `tests/topic2_rgpool/test_verdict_path_guards_r3.py`, applied to a `verdict.json` `v`:
1. `fixture_gates.Fplus.pass` or `fixture_gates.Fminus.pass` is null (runs missing or failed) → **no_verdict** (§5; E2, E3);
2. else `Fplus.pass` is false → **inconclusive** (§7.2; E1);
3. else `hcp_complete` is false → **no_verdict** (§8);
4. else the script's verdict (which already downgrades `keep` on an F− failure).
It is the identity whenever both gates were computed and passed and Stage 1 is complete. Over 27 synthetic
scenarios (F+ ∈ {pass, fail, missing} × F− ∈ {pass, fail, missing} × Stage 1 ∈ {keep-like, stop-like, absent};
`verification/worker_M3_r3/p01_errata_probes.out.json`) the rule differs from the frozen label in 12: 2 by E1 (F+ failed, Stage 1 absent), 6 by E2 (F+ runs missing),
4 by E3 under the strict reading (F− runs missing; in 2 of them F+ also failed). Under the narrow E3 reading only
1 of those 4 differs (a `keep` with F− missing).

## 3. The shipped verdict is unaffected

Every precondition of E1–E5 is false in the shipped records (`p01_errata_probes.out.json` §D, aggregates only):

| precondition | needed for | shipped value |
|---|---|---|
| F+ gate failed | E1 | F+ pass = true; gains C vs E 3.06 %, C vs S 2.93 % (≥ δ = 1 %) |
| F+ runs missing or failed | E2 | 6/6 F+ runs completed |
| F− runs missing or failed | E3 | 6/6 F− runs completed; F− pass = true, gain C vs E −1.74 % (< δ) |
| two records with one key | E4 | 27 run.json, 27 distinct keys |
| differing test order / `-O` | E5 | 1 test order over the 15 hcp runs; the report ran the script without `-O` |
| Stage 1 incomplete | E1, §2.6 step 3 | 15/15 hcp runs completed; `hcp_complete` = true |

Order of events: the last F+ run ended at 03:42:08Z and the first hcp run started at 03:44:51Z, consistent with
addendum_02 ("Stage 1 launched only after all 6 F+ runs completed and the F+ gate was computed").
`stop` rests on one number: the upper 95 % bound of I1 is 0.361 % (I1 mean +0.147 %, t95 [−0.068 %, +0.361 %]),
below δ = 1 %. `card_reading(verdict.json)` = `stop` (asserted by
`test_shipped_records_meet_no_erratum_precondition_and_read_unchanged`).
The frozen script, mutated by each of the 20 non-control mutants of §4, rewrites `verdict.json` byte-identical
on the shipped records (sha256 59af05e5…af68; the unmutated script too; the 3 positive controls change bytes and
still give `stop`; `verification/worker_M3_r3/m02_shipped_verdict_invariance.out.json`).

Caveat for readers: `I2_lower_gt_0` = true in `verdict.json` has a lower bound of +0.001 % (9.8e-6). It governs
nothing (stop is decided first) and is confounded with box compactness (addendum_05 §4 item 4). It must not be
cited as evidence of FC specificity.

## 4. New tests and mutation evidence

New file `tests/topic2_rgpool/test_verdict_path_guards_r3.py` (24 tests, additive; the 12 shipped test files are
unchanged). Expectations come from the card text (§5, §7.2, §8), quoted in each docstring:
- `card_verdict`, an independent coding of the card §8 table, is compared with `stats.verdict` on an exhaustive
  grid of 4,320 cases at, just below and just above δ and 0 (dyadic δ = 2⁻⁷, so equality boundaries are exact);
- one-rule-per-test boundary checks for keep / modify / stop, the F+ and F− gates at equality, the F− contrast;
- the frozen script end to end on synthetic run records: missing F+ runs, a failed hcp run, failed fixture runs, a
  mis-ordered test list, F+ failed beside a stop-like Stage 1;
- [erratum] tests that pin the frozen labels for E1, E2 and E3 and assert the card reading through `card_reading`;
- the shipped-precondition test of §3.
The script is invoked through `helpers.ROOT`, so a mirrored tree tests its own (mutated) copy.

Mutants (24 specs, read verbatim by `verification/worker_M3_r3/m00_build_specs.py`, never retyped):
V01–V11 from `verification/challenger_M3_r2_2/p07_specs.json`; the 3 positive controls from its `p05_mutants.py`;
K1 (F− gate uses C vs S) and K2 (keep uses the I2 mean; = reviewer_M3_r2_1 R1) from
`verification/challenger_M3_r2_1/run_mutants_c1.py`; W04–W09 and W12 from
`verification/explorer_M3_r3_2/m03_next_round_sweep.py`. Harness `verification/worker_M3_r3/m01_mutants.py`: one
exact edit per mutant in a fresh mirror; rc 0 = survived, rc 1 = killed, anything else = INVALID (never a kill).

Legs:
- **A, shipped only**: the 12 shipped test files (sha-checked against `output_sha256_r2.txt` first, new file
  excluded), connectome `srun -p debug`, project-local CPU venv (torch 2.15.0+cpu, numpy 2.5.4, scipy 1.18.1).
- **B, new file only**: local DGX-Spark, one pytest at a time.
- **C, union**: shipped + new, connectome as in A.

<<MUTATION_TABLE>>

**W09 is equivalent** on the reachable domain. W09 changes the stop rule to `hi < δ and not I1_survives`.
`t_interval` returns lo = m − q·se and hi = m + q·se with se ≥ 0 and q > 0, so lo ≤ m ≤ hi (or NaN, where every
comparison is false in both versions). I1_survives needs m ≥ δ, hence hi ≥ δ; so when hi < δ, I1_survives is false
and the two conditions agree. `scripts/topic2_verdict.py` passes only `t_interval` outputs. Check
(`p02_w09_equivalence.out.json`): 0 disagreements in 1.2 M cases of random `t_interval` outputs and 0 in 1,440
grid cases; the two differ only on a malformed interval with mean > hi, which `t_interval` cannot produce.

Scope of the claim: the mutants listed above are killed or shown equivalent. This is not a claim that every
possible verdict-path mutant is killed.

## 5. Dev-salt containment (root, ~19:3x KST), re-verified — counts only

`verification/worker_M3_r3/s01_salt_containment_scan.out.json` (no salt, hash, ID or preimage printed or written):
- The sealed salt `~/.local/share/00IITP-AI_sealed/topic2/dev_subject_salt.txt` matches root's recorded sha256
  (7e5434ab…d02e); mode 0400, directory 0700, parent 0700; not inside any git work tree. The old repo path is gone.
- The salt, its first and last 12 characters, its upper-case form, base64 and hex encodings: 0 hits in
  <<N_FILES>> working-tree files (<<N_GB>> GB) and 0 hits in all <<N_BLOBS>> git blobs (`git cat-file --batch-all-objects`,
  <<N_OBJ>> objects, unreachable ones included).
- The 5 burned hashes occur only in 3 files under `verification/explorer_M3_r1_1/` and in 0 git blobs.
- Without the sealed salt, 0 of the 5 are recovered over all 10⁶ six-digit names (sha256, sha1, md5 of the bare
  name; sha256 with the public split salt as prefix or suffix, with or without a newline). Positive control: the
  frozen scheme with the sealed salt recovers 5 of 5, so the loop and the hash list are right.
- No 16-hex window of sha256(name) or sha256(public salt + name), for any six-digit name, occurs in any
  working-tree file or git blob (0 hits).

So the salted-hash channel is closed: no repo content lets the 5 dev-subject IDs be recovered through the salt or
through unsalted or public-salt hashes of six-digit names.

**Residual, disclosed, not closed.** `verification/explorer_M3_r1_1/dev_subjects_BURNED.md` states that the 5 dev
subjects are "positions 0-4 of the sorted listing" of the B300 staging directory. That statement occurs in
<<N_POS_FILES>> working-tree files and in <<N_POS_BLOBS>> committed git blobs. Anyone holding the B300 HCP directory listing can
therefore name the 5 dev subjects without any salt (explorer_M3_r3_3 checked this on B300, in memory). This needs
off-repo data, as does the positional-token residual of addendum_05 §3 (and the preprocess.log line-order route
raised by reviewer_M3_r2_1 N2 and auditor_M3_r2_1 N2). It cannot be removed from history without a forbidden git
rewrite. It is recorded here for a root/PI ruling; this addendum does not claim that HCP IDs are unrecoverable by
every route. A plain-text scan of the repo against the B300 HCP name list was not re-run in r3 (the last one,
challenger_M3_r2_2 p03, found only numeric coincidences).

## 6. No regression

<<REGRESSION>>

## 7. Carried forward from the r2 verifiers (nonblocking, not changed here)

- challenger_M3_r2_1 N3: after relabelling, the repo `split.json` cannot be re-derived from the repo manifest by
  the card §4 rule; it reproduces only from the sealed originals (addendum_05 S5).
- addendum_05 §5 says "all 103 mutants"; the count is 102 plus the baseline (challenger_M3_r2_1 N4,
  auditor_M3_r2_1 N5).
- auditor_M3_r2_1 N3: three training-loop guard tests in `test_pipeline_guards_r2.py` skip when CUDA is visible.
  Every r3 suite run here hid CUDA.
- reviewer_M3_r2_1 N6 / challenger_M3_r2_2: `test_c4_tokens_r2.py` scans only `results/topic2/2026-11-01` and this
  directory, not `verification/` or the run metadata; the whole-tree count scan of §5 stands in for it.
- `scripts/topic2_c4_sanitize.py` and `scripts/topic2_c4_seal_check.py` are not run by any test.

## 8. For the follow-up cards FU-A..FU-E (advice, not a rule of this card)

The errata become reachable when an F+ gate can fail (options A and D) or when more seeds and reruns are run.
A follow-up verdict script should keep explicit computed / failed / missing gate states, raise instead of `assert`,
reject duplicate run keys, return `inconclusive` when F+ fails and Stage 1 is not run, and be tested with an
independent card oracle on a boundary grid. Docs in this directory are scanned by the shipped C4 tests: no 16-hex
runs (abbreviate hashes as 8 hex…4 hex), no BIDS-style subject prefix, no six digits followed by `/MNINonLinear`.

## 9. Compute and deviations of this iteration

- 0 GPU-h; no ledger row. CPU only: connectome Slurm `srun -p debug` (legs A, C and the full suite), local
  DGX-Spark for leg B, the probes and the old suites (at most 2 concurrent pytest processes).
- `DISPATCH.md` of worker_M3_r3 reproduces the dispatch verbatim except the embedded explorer-strategy JSON, which is
  referenced by path (each explorer's handoff holds it).
- The first connectome launch ran an empty script (a backgrounded `cat` read /dev/null) and did nothing; it was
  relaunched. The first s01 version stopped on a syntax error before scanning; it is kept in
  `verification/worker_M3_r3/prev_versions/`.

## 10. Receipt

`results/topic2/2026-11-01/addendum_06_sha256.txt` pins this addendum, the new test file and the r3 evidence
scripts and outputs. Verify: `cd /home/juke/git/00IITP-AI && grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c`.
