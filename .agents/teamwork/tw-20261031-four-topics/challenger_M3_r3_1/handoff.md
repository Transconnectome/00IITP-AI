# handoff — challenger_M3_r3_1 (M3 Topic 2, r3 gate, ACCEPTANCE T2.4) — Hard handoff

**Verdict: CONFIRMED.** I reproduced every T2.4 claim that worker_M3_r3 made with my own harnesses. I found no defect that blocks the gate and nothing that changes the shipped verdict `stop`. There are six nonblocking findings (N1–N6). N1 and N2 need root or PI attention.

Evidence directory: /home/juke/git/00IITP-AI/verification/challenger_M3_r3_1/ (scripts, specs, outputs, logs). GPU use: 0 GPU-h, no ledger row. All work ran on local CPU with at most 2 concurrent pytest processes, under nice. I made no git writes and edited no production file.

## 1. Observation

**Integrity** (checked at 16:00Z, rechecked at about 16:52Z)
- C1 PROTECTED_HASHES: 67/67, rc 0.
- Receipts:
  - addendum_06_sha256.txt: 31/31; the receipt's own sha is 4ac6d454…12fb.
  - code_sha256_at_freeze: 33/33.
  - output_sha256_r2: 156/156. This includes the 12 shipped test files.
  - c4_sanitized: 19/19.
  - Old card_sha256: exactly 2 FAILED, as already disclosed.
- verdict.json sha is 59af05e5…af68 and the card sha is c9bfc60a…41f5. Neither changed.
- Card freeze happened before the results:
  - card_sha256.txt was written at 03:14:34Z and the card was committed at 03:16:27Z.
  - The first fixture run started at 03:16:17Z.
  - The first real-data (hcp) run started at 03:44:51Z.

**Mutation testing.** I wrote my own harness (h01_mutate.py); I did not reuse the worker's m01. It applies one exact replacement per mirror and requires the target string to occur exactly once.
- Specs: V01–V11 were read from challenger_M3_r2_2/p07_specs.json (keys `new:V..`) and all 11 are identical to the worker's specs. The K and W specs match their source files.
- Leg A (12 shipped files, FU cards left out of the docs copy):
  - The baseline gives 92 passed.
  - All 20 non-control mutants SURVIVED.
  - The 3 positive controls were KILLED.
  - One run (W07) was INVALID: rc −15, an external SIGTERM. I reran it and it SURVIVED.
- Leg B (new file only):
  - The baseline gives 24 passed.
  - V01–V11, K1, K2, W04–W08 and W12 were KILLED, by exactly the tests named in the addendum_06 §4 table.
  - W09 survived.
- Leg D (p09, mutated script on the shipped runs):
  - The baseline and all 20 non-control mutants produce bytes identical to verdict.json.
  - The 3 controls change the bytes but still give `stop`.

**Fresh mutants.** These 24 mutants (X01–X24) are my own and outside the enumerated set. I ran them against the union of shipped and new tests:
- 22 KILLED. This includes X01, which was INVALID once (rc −15) and was KILLED on rerun.
- 2 SURVIVED:
  - **X02**: the F+ gate becomes `ok = g_cs >= delta`, so the C-vs-E contrast is dropped. Shipped verdict bytes stay identical.
  - **X23**: the status test becomes `startswith("complete")`. This is equivalent: train.py only ever writes the statuses started, failed_nonfinite_loss, aborted_throughput and completed.

**Headline numbers** (p01): I recomputed them from the raw run.json files with my own t quantile (incomplete beta plus bisection).
- I1 = +0.1468 %, 95 % t interval [−0.0677 %, +0.3614 %].
- I2 lower bound = 9.8e−6.
- F+ gains: 3.0607 % (C vs E) and 2.9347 % (C vs S). F− gain: −1.7373 %.
- Differences from verdict.json are at most 8e−15.
- 27 records, 0 duplicate keys, all `completed`, 1 test order.
- My own coding of card §8 gives `stop`.

**Errata probes** (p02, p03; frozen script, my own synthetic records)
- E1: F+ fails and Stage 1 is absent → no_verdict, "Stage 1 incomplete". Confirmed.
- E2: F+ runs missing → inconclusive, with the F+-failure reason; also for a stop-like Stage 1. Confirmed.
- E3: F− runs missing → keep. As a control, a failed F− gives inconclusive. Confirmed.
- E4: the same records give keep or no_verdict depending only on directory names. The last record in glob order wins in 14/14 layouts, and I observed both outcomes. Confirmed.
- E5: run plainly, the script exits rc 1 with the order message; under `-O` it exits rc 0 and writes keep. Confirmed.
- On the 27-scenario grid (p08), the frozen label and card_reading differ in 12 cells, as the addendum states.

**W09** (p07): 0 disagreements in 1.8 M adversarial t_interval cases. The cases include subnormals, ±1.7e308, ±inf, nan, near-ties, n = 2..7, and δ values including 0 and negative ones.

**Salt containment** (p04; counts only, nothing printed or written)
- The sealed salt's raw bytes match root's sha 7e5434ab…d02e. Modes are 0400 / 0700 / 0700; the file is outside the repo and the old repo path is gone.
- I searched for 10 needles derived from the salt (full, head12, tail12, mid12, upper, reversed, b64, hex, b64-of-bytes, utf16 head12):
  - 0 hits in 19,808 working-tree files (2.33 GB);
  - 0 hits in 3,278 git objects (all objects, all types);
  - 0 hits in the 37 raw non-object files under .git.
- The 5 burned prefixes occur only in 3 files under verification/explorer_M3_r1_1 and in 0 git objects.
- Without the salt, 0 of 5 are recovered over 10⁶ names under 8 schemes. The positive control with the sealed salt recovers 5 of 5.

**Positional route** (p05; coarse facts only, no names): all 5 recovered dev names are below 101100 and lie within a span of 800.

**C4 scan** (p06) of addendum_06, the r3 test file, the receipt, verification/worker_M3_r3 and the worker's metadata found no ID token. The pattern hits are:
- the quoted FU-B "sub-o" false positive inside test logs;
- one loop count of 200000;
- 16-hex runs that are float digits or synthetic constants from test_c4_tokens_r2.py.

**Suites**
- Full tests/topic2_rgpool, local, current tree: 115 passed, 1 failed. The failure is test_outputs_no_ids, triggered by the match `sub-o` in docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md, which is the FU-B team's file.
- Union baseline with the FU cards left out: 116 passed.
- Old 86: 86 passed with PYTHONPATH=repo. Without PYTHONPATH, 1 e2e subprocess test fails with `No module named 'src'`, an environment issue (N5).
- tests/topic1_lagmotif: 88 passed.
- audit_layout on the whole run: rc 0, 0 findings.

## 2. Logic Chain

1. Leg A shows that each enumerated mutant survives the pinned shipped suite. Leg B shows the new file alone kills it. Together these give attribution of every V01–V11 kill to the new file. Both legs use my own harness, with specs re-read from the r2 source. The worker's attributable-kills claim is therefore reproduced.
2. W09 is equivalent in practice. t_interval always gives lo ≤ mean ≤ hi under IEEE rounding, because hi = m + q·se with q·se ≥ 0 and nan compares false in both versions. Hence hi < δ implies mean < δ, which implies not I1_survives. I checked this adversarially in p07.
3. E1 is a certain card-vs-code deviation (card §7.2 says inconclusive; the code says no_verdict). E2 to E5 behave exactly as described. The shipped records meet none of their preconditions (p01), and leg D gives identical bytes. So the shipped `stop` stands, and I reached it independently.
4. Salt containment: zero hits across the worktree, all git objects and .git, plus a positive control, means the salted-hash route is closed.
5. T2.4 asks for V01–V11 to be killed, the erratum to be recorded, salt containment and no regression. All four hold. The fresh survivor X02 and the positional route are outside what T2.4 enumerates, and the worker scoped its claim explicitly. So they are nonblocking. N1 and N2 still matter for the FU cards and for C4.

## 3. Caveats and nonblocking findings

- **N1 (medium; FU risk): the F+ gate's C-vs-E half is untested.**
  - Mutant X02 (`ok = g_cs >= delta`) survives all 116 tests.
  - No test has C beating S by at least δ while beating E by less than δ.
  - The F+ gate tests at equality (r3) use equal gains, and test_stats line 39 covers only the opposite direction (the W10 direction).
  - There is no shipped impact, since both gains are about 3 %.
  - FU-A..E reuse gate_fixture (F2), so they should add the fixture `{"E":[1,1],"C":[1,1],"S":[1.25,1.25]}` → `Fplus pass False`.
- **N2 (C4 ruling for root/PI): the positional residual is broader than addendum_06 §5 says.**
  - §5 says recovering the 5 dev IDs "needs off-repo data" (the B300 listing).
  - p05 shows all 5 dev names are numerically the very lowest HCP-YA names (all below 101100, span 800).
  - So the repo statement "positions 0-4 of the sorted listing", combined with the public HCP-YA subject list, very likely names them without B300 access. I did not verify this against the public list: doing so would mean handling IDs.
  - No ID is written anywhere. The re-identification value is negligible, because HCP IDs are public pseudonyms. This is still a disclosure-accuracy issue that the PI should rule on.
- **N3 (low, interpretive): the reading-rule precedence is not argued.**
  - card_reading checks for a missing F− before checking F+ failed.
  - In the cell "F+ failed and F− missing", it gives no_verdict where card §7.2 explicitly says inconclusive. In 2 of those cells the frozen script was card-consistent; in the third (Stage 1 absent) E1 is left uncorrected (p08).
  - Root/PI choosing between the E2 and E3 readings should also choose this precedence.
- **N4 (foreign, confirmed): the FU-B card makes the shipped C4 test fail.** The match is "sub-o", a false positive, not an ID. The FU-B owner must reword it.
- **N5 (environment, pre-existing): the old 86 suite needs PYTHONPATH=repo.** Without it, test_pilot_python_module_cli_execution fails.
- **N6: two INVALID runs (W07 in leg A, X01 in leg C) ended with rc −15, an external SIGTERM** from a source outside this agent. Both were rerun once and are valid. I disclose this because something on the host sends SIGTERM to long pytest processes.
- **Not done:**
  - I did not run legs A and C on connectome; I ran them locally with the same specs.
  - I did not do a plain-text scan against the B300 HCP name list (I have no B300 access in this task).
  - I did not scan off-repo channels where the salt may appear: the explorer's agent transcripts and shell history, since the salt was passed on argv. These are out of repo scope.
  - The fresh mutant set is not exhaustive.

## 4. Conclusion

CONFIRMED for T2.4:
- V01–V11 are killed with attribution by tests/topic2_rgpool/test_verdict_path_guards_r3.py, and so are K1, K2, W04–W08 and W12. W09 is equivalent.
- The E1 erratum and E2–E5 are recorded accurately in addendum_06.
- The salted-hash channel is closed.
- There is no regression attributable to M3.
- The shipped verdict `stop` is unchanged and independently recomputed.

Recommended before the FU verdicts: fix N1 (F+ gate fixture), and have root/PI rule on N2 and on the N3 precedence.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c
V=verification/challenger_M3_r3_1; PY=/home/juke/superclaude-env/bin/python3
PYTHONDONTWRITEBYTECODE=1 $PY $V/h00_build_specs.py      # (run from $V) rebuilds specs_enumerated.json / specs_fresh.json
$PY $V/h01_mutate.py $V/specs_fresh.json $V/work $V/out.json --jobs 2 --tests tests/topic2_rgpool   # X02 survives
$PY $V/p01_recompute_headline.py /tmp/p01.json; $PY $V/p08_reading_rule_grid.py $V/w8 /tmp/p08.json
```
Invalidation: any edit to src/topic2_rgpool, scripts/topic2_*.py, the 12 shipped test files or the r3 test file, or any change to results/topic2/2026-11-01/runs.
