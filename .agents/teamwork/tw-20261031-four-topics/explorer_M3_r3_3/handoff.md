# explorer_M3_r3_3 — Hard handoff (M3 Topic 2, r3 gate repair, T2.4; lens: adversarial pre-mortem)
Written 2026-11-01 ~14:55Z. Probes: /home/juke/git/00IITP-AI/verification/explorer_M3_r3_3/. 0 GPU-h, no git writes,
no production file changed, no ID/salt/hash printed or written (counts and positional indices only).

**Summary.** T2.4 can be closed with one additive test file and one addendum, with no rerun. I prototyped the test file
(`verification/explorer_M3_r3_3/proposed/test_verdict_path_guards_r3.py`). It kills all 11 verbatim V01–V11 mutants,
each by its named test, and passes on the frozen code. The real risk is overclaiming in addendum_06. The salted-hash
channel is closed (the salt is in 0 of 17,697 worktree files and 0 of 2,944 git objects). A positional channel remains,
and it is already in committed git history: "positions 0–4 of the sorted listing" recovers the 5 dev subjects from the
B300 listing, with no salt needed (p01 confirms 5/5). addendum_06 must disclose this, not claim "no repo content lets
IDs be recovered". Two more card-vs-code divergences (case D: a missing F− is treated as a pass; the `assert` order
guard) belong in the same erratum. Concurrent FU teams write into the DOCS directory that the shipped C4 tests scan,
which is a likely source of false regressions.

## 1. Observation
- O1 Gate record (`orchestrator/M3_r2_gate_record.json`). challenger_M3_r2_2 is REFUTED, with three blocking items:
  (a) the dev-salt C4 leak, which root has since contained;
  (b) V01–V11 survive the full 92-test suite (connectome p07: baseline "92 passed", 11 SURVIVED, 42/42 r1 survivors KILLED);
  (c) case A, where F+ fails and no hcp runs exist: the frozen script returns no_verdict "Stage 1 incomplete", but card §7.2 says inconclusive.
  The other 4 verifiers APPROVE, CONFIRMED or CLEAN.
- O2 Frozen code. `scripts/topic2_verdict.py`:
  - `out["verdict"] = S.verdict(ci1, ci2, a.delta, bool(fp), fm is not False)`. A missing F− counts as a pass (case D).
  - The order guard is `assert len(orders) == 1, ...`, which `python -O` strips.
  - The else branch returns no_verdict whatever the F+ state (case A).
  `src/topic2_rgpool/stats.py:57-90` holds verdict() and gate_fixture(). Every V-mutant anchor occurs exactly once (checked).
- O3 Baseline now:
  - C1 rc 0, 0 non-OK.
  - code_sha256_at_freeze, output_sha256_r2 and c4_sanitized all pass.
  - Old card_sha256 fails exactly 2 (manifest, split); old output_sha256 fails exactly 16 (stage0 + 15 hcp run.json). All were disclosed in addendum_05.
  - test_stats.py + test_verdict_path_guards_r2.py: 14 passed locally.
- O4 Shipped verdict evidence (`results/topic2/2026-11-01/verdict.json`):
  - Fixture gates: Fplus pass=True (gain C vs E 0.0306, C vs S 0.0293); Fminus pass=True (−0.0174).
  - Stage 1: hcp_complete=True. I1_t hi=0.003614 < δ=0.01, so the verdict is stop, I1_survives False.
  - Runs: 27 run.json files, 27 unique (source, arm, seed) keys, 0 duplicates, all "completed" (15 hcp, 6 F+, 6 F−). The 4 other entries in runs/ are wave*_launched.json.
- O5 p03 (`p03_kill_check.py` → `.out.json`, `.log`). Mutants were read verbatim from `challenger_M3_r2_2/p07_specs.json` (sha256 de8f2de1…a4e).
  - Each ran in a fresh mirror against the proposed file only.
  - Baseline: SURVIVED, "14 passed".
  - 11/11 KILLED. Each is killed by its named test, and V07 also by the V10 test.
- O6 p02 (`p02_salt_scan.out.json`, count-only).
  - The sealed salt is 32 hex characters, 128 bits.
  - Searches: the raw salt, upper and lower case, base64, hex encoding, and its 12-character prefix and suffix.
  - Worktree: 0 hits in 17,697 files (2.30 GB).
  - Git: 0 hits in the full `git cat-file --batch-all-objects` stream, 839.5 MB, equal to the 2,944-object total incl. unreachable objects.
- O7 p01 (`p01_dev_positional_recovery.out.json`). The B300 .98 listing of directories that hold the REST1_LR file was streamed into memory and never printed.
  - It now has 103 entries; the manifest says 93 at preprocessing time, so the staged set has grown.
  - The burned hashes sit at positions [0,1,2,3,4], and first5_are_exactly_the_burned_set is true.
  - `verification/explorer_M3_r1_1/dev_subjects_BURNED.md` says "5 HCP REST1_LR subjects = positions 0-4 of the sorted listing of B300 .98 …".
  - The same fact is in committed metadata: `challenger_M3_r2_1/handoff.md:54` ("still positions 0–4 of the sorted listing") and `auditor_M3_r1_1/handoff.md:77`. `git log -G"sorted listing"` gives 2 commits.
  - verification/ itself was never committed (0 commits).
- O8 C4 tests scan `DOCS = docs/03_empirical_analysis/topic2` (the whole directory, `helpers.py:9`).
  - `test_c4_tokens_r2.py` UNQUOTED16 flags any 16-hex run that contains a–f and is not inside a longer alphanumeric run. a 16-hex prefix such as "0123456789abcdef…" would be flagged; an 8-character prefix…suffix form or a full 64-hex hash is not.
  - `test_outputs_no_ids.py` flags `download_HCP_REST1_filtered/<alnum>`, `NNNNNN/MNINonLinear` and `sub-<alnum>`.
  - The workflow C script puts the FU cards in that same directory (`docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_<x>_*.md`) and FU results in `results/topic2/2026-11-02_fu_<x>/`, outside RESULTS. Those results are therefore not covered by any C4 test.
- O9 The old 86 = `tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e` (challenger c04_full_suite.sh).
  - Locally, earlyoom killed test_partition.py and test_pipeline_guards_r2.py in r2.
  - The full suite was green only on connectome (uv venv, torch 2.15.0+cpu). That venv was removed, and `connectome_build_and_test.sh` rebuilds it.

## 2. Logic Chain
1. O5 shows a test set that kills each V-mutant semantically: every record carries every field, so the mutants compute a wrong verdict instead of crashing. O1/p07 shows the same mutants survive the shipped full suite. Together these give attributable kills, so no equivalence proof is needed.
   - None is equivalent. V11 is reachable through `S.verdict` directly, and through the script when Stage 1 runs after an F+ failure (p06 case B).
2. Attribution breaks if the shipped-suite run includes the new file, or if FU tests land in tests/topic2_rgpool mid-run. So "shipped suite" must be the 14 files pinned in output_sha256_r2.txt, checked by sha before the run.
3. From O4, the shipped data sit in the cell F+ pass=True, Stage 1 complete. The stop branch (I1 hi < δ) fires before keep, modify and the F− downgrade. Cases A and D need F+ ≠ pass or F− missing, so neither can change the shipped verdict.
   - The reproduction test `test_verdict_script_reproduces_the_shipped_verdict` passes, so the shipped verdict holds.
4. The salted-hash channel is closed: the 5 hashes are irreversible without a 128-bit salt that is absent from all repo content (O6).
   - The positional channel (O7) needs only the B300 listing, where directory names are IDs. That is the same threat model as r1 B1 and the residual disclosed in addendum_05 §3.
   - It sits in git history, which no-git-writes forbids rewriting.
   - It therefore cannot be "contained"; it can only be disclosed and ruled on. C4's letter permits positional indices, and M1 is the precedent.
5. FU work in DOCS, plus any FU result that reuses the frozen `data.pseudonym()` (unsalted content-hash), could break shipped C4 tests or re-create B1 outside their scope (O8).

## 3. Caveats
- The kill check ran the proposed file alone, locally. I did not re-run the full shipped suite or the union suite, for memory reasons (O9). Survival rests on the challenger's p07 on byte-identical code (output_sha256_r2 156/156 OK now).
- I did not check whether the salt or the burned hashes exist on B300 /scratch/iitp4, or in /tmp/claude-1000 scratchpads of other sessions. Neither is repo content.
- p01 used a direct ssh listing on B300 .98: no GPU, about 1 s of CPU, outside Slurm. This is the same class of deviation as challenger p02.
- The positional-channel severity is a judgement call (positional index is allowed under C4). I rate it nonblocking if disclosed, and blocking if addendum_06 claims absolute non-recoverability.

## 4. Conclusion (recommendations; the worker implements)
- R1 Ship the proposed tests as `tests/topic2_rgpool/test_verdict_path_guards_r3.py`. The case-A characterization test is optional: it documents a defect and does not endorse it.
  - Mutation evidence: three runs per mutant on connectome `srun -p debug`, re-using p07 with the specs read verbatim:
    (a) the 14 pinned shipped files → SURVIVED;
    (b) the new file only → KILLED by the named test;
    (c) shipped + new → KILLED.
  - Plus a baseline that must pass and the 3 p05 positive controls.
- R2 addendum_06 (`docs/03_empirical_analysis/topic2/2026-11-02_topic2_addendum_06.md`, receipt `results/topic2/2026-11-01/addendum_06_sha256.txt`):
  - Content: a table of F+ ∈ {pass, fail, missing} × Stage 1 ∈ {complete, incomplete}, giving the frozen-script output, the card reading, and which cell the shipped data occupy.
    - Case A erratum: F+ fail with Stage 1 not run → card inconclusive.
    - Case D: F− missing → a would-be keep is inconclusive under §7 "must pass".
    - Nonbinding notes: the `assert` guard under -O; case E, where duplicate keys resolve by glob order (0 duplicates shipped); "after one rerun" is not modelled.
    - The O4 evidence; the salt-containment result with exact counts; and the positional residual, disclosed with file:line references.
  - Wording to avoid: no 16-hex runs (cite hashes as full 64-hex or as 8…4 short forms), no HCP path or sub- patterns, and no claim of absolute non-recoverability.
  - Re-run test_c4_tokens_r2 and test_outputs_no_ids after writing the addendum.
- R3 Root actions:
  - Reserve the addendum_06 filename against FU teams.
  - Tell FU teams that DOCS is scanned by the shipped C4 tests.
  - FU results must not carry `data.pseudonym()` tokens: reuse h-tokens or positional ones, and add their own C4 guard.
  - Optionally move dev_subjects_BURNED.md and the 2 hash-bearing probe files to the sealed directory. This reduces exposure but does not close the history channel.
  - Get the PI or root to rule on the positional residual.
- R4 No-regression set:
  - C1;
  - code_sha256_at_freeze, output_sha256_r2 and c4_sanitized (old pins fail exactly 2 + 16, as disclosed);
  - all addendum receipts;
  - the full tests/topic2_rgpool suite on connectome, plus old 86 and topic1_lagmotif;
  - `cmp` of the verdict regenerated against verdict.json.
  The shipped verdict stays stop.

## 5. Verification Method
- `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`
- `python3 -B verification/explorer_M3_r3_3/p03_kill_check.py <repo> verification/challenger_M3_r2_2/p07_specs.json verification/explorer_M3_r3_3/proposed/test_verdict_path_guards_r3.py <scratch> out.json`. Expected: baseline SURVIVED, 11 KILLED.
- `git cat-file --batch-all-objects --batch | python3 -I verification/explorer_M3_r3_3/p02_salt_scan.py <repo> <sealed salt>`. Expected: all hits 0.
- `git log --all -G"sorted listing" --oneline | wc -l` gives 2 (the positional fact is in history).
- Invalidation: any change to frozen code or pins, or a V-mutant anchor count ≠ 1.
