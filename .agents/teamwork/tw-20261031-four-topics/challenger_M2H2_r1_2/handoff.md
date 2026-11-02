# Handoff — challenger_M2H2_r1_2 (M2H2, Topic 3 H2 random-init control) — Hard handoff, 2026-11-01T17:40Z

**Verdict: REFUTED, on test coverage only.** The shipped numbers and labels hold. I reproduced them two independent ways: from the saved outputs, and by a GPU rerun of seed 8. The freeze came before any results, and the labels follow addendum 07 §6. What fails is the claim that the tests guard the verdict path. The 71-test suite stays green under mutants that change a primary label: 26 of my 53 new mutants survive, and 2 of the survivors flip C1 from INC to EQ.

## 1. Observation

All probes are in `/home/juke/git/00IITP-AI/verification/challenger_M2H2_r1_2/`.

**O1. Freeze came before results.**
- Addendum 07 sha256 is `09b45220…d84b`, and the receipt verifies. The file's mtime is 15:57:27Z and the receipt's is 15:57:40Z.
- The checkpoint commit `35d10a5` (2026-11-01T16:05:25Z) already holds this file with the same sha256. That is before gate job 218063 (submitted 16:22:19Z, record started 16:22:21Z) and random job 218064 (submitted 16:32:19Z).
- The JSON files from the three explorer smokes (218004, 218041, 218007) contain random-init results on synthetic iid input only.

**O2. Independent recomputation** (`recompute.py`, output in `recompute.out.txt`).
- It does not import `src.topic3_h2` or `src.topic3_spectral`. It uses its own SVD-based PR, its own corr standardisation, its own index sets J, and its own sign-flip, bootstrap, Holm and decision rule.
- Inputs: the sha-checked pinned T files and the shipped `R1..R10_*.npz`.
- Result: all 24 family C/L labels match. The largest numeric difference from `h2_results.json` is 1.8e-15.
- T's subject-level A1 equals the pinned Family A exactly (cov 5.343854531110546 / SE 1.0810551262749508; corr 6.038808669990018 / 0.8990825692997121).
- The δ values match.
- Random-arm mean D1 is 0.255 (cov) and 0.252 (corr).

**O3. Independent GPU rerun of seed 8.** Connectome Slurm job 218068: node1, 1× A5000, 274 s, 0.077 GPU-h, with a start row and a closing row in the ledger.
- Code: the fork ver11, patchembedding and datasets taken directly from `git show` (SwiFT_v2 cd87338, VRABES 94c2bf4). Their sha256 equal the vendored pins. PR code is my own numpy; my own driver; the worker venv was used read-only.
- Result (`gpu_probe/probe_seed8_218068.json`): 399 windows and 57 subjects. Per-subject cat_covpr and cat_corrpr, and all 10 per-index-set arrays, match the shipped `R8_*` to a relative 2.3e-15 or better.
- The encoder hash equals `random_record.json` seed 8. Rebuilding the seed gives the same hash, and seed 9 gives a different one.
- My dir `/home/connectome/connectome1/iitp4_m2h2/challenger_M2H2_r1_2/` was deleted after copy-back. No frames left connectome.

**O4. Decision-rule fuzz** (`fuzz_decide.py`): 200 000 cases, including exact ±δ boundaries and p values of 0.05 and 0.049999. There are 0 mismatches between the shipped `decide()` and an independent transcription of §6.

**O5. Test suite.** `pytest tests/topic3_h2 -q` gives 71 passed in 375 s on a host at load average about 70 (`pytest_topic3_h2.out.txt`). C1 PROTECTED_HASHES rc 0 (`c1_check.out.txt`, rechecked at the end). `output_sha256.txt` rc 0. The 2026-10-31 receipts pass, except `card_sha256.txt` rc 1. That is a known format issue: a trailing "frozen" token. The hash matches 683374565d80….

**O6. Mutation run** (`mutants_ch2.py`, `mutants_ch2.log`, `mutants_ch2.out.json`).
- Setup: 53 new mutants that are not in the worker's list. Each runs in a copied tree; the baseline is 71 passed. Outcome: 27 killed, 26 survived.
- Survivors that change shipped labels on the real data (`survivor_impact.out.txt`):
  - **N26** `family_c` uses seed 1's token values for all K: **C1 INC → EQ**.
  - **N53** `topic3h2_stats.py final` loads `R1_scalars.npz` for every seed: **C1 INC → EQ**, and 7 of 10 Family L token labels change, e.g. L0_cov INC → EQ, L2_cov INC → EQ.
  - **N27** subject-side analogue of N26: same class, but no label change on the real data.
- Cause: the family C tests build K random arms that are near-identical around one base, so collapsing to one seed is not detected. No test runs `cmd_final` or `cmd_gate`. The Family L analogues (N24, N25) are killed.
- Other survivors:
  - Stats-script guards N50–N59 (gate-PASS refusal, seed hygiene, T-A1 reproduction check, check_deltas, local G3, tf32/vendor, window count, trained-hash, addendum check).
  - Comparator N30, N31, N32, N33, N35, N38.
  - Reduce N40 (index-set seed) and N41 (subset corr computed as cov). Both are caught at runtime only by the untested T-A1 check.
  - N42: equivalent (dead check).
  - Driver job paths N71–N74: untestable offline.
  - N11: Family L seed-assignment order.

**O7. Report claims.** I checked these in the result report against `h2_results.json` and the npz files, and all match: §2 table, §3 ratios and E1 ranges (17.6–20.9 and 30.9–34.0; trained 2.78, 11.02, 3.58), §4 per-seed D1 robust seeds 5, 7, 10, H1a 9 of 10 (seed 4 −0.0004, p_holm 0.52), R1/A1b, the medians 5.85–6.22 vs 5.41/5.67, and α.

**O8. δ sensitivity**, from the shipped intervals and seed effects:
- C2 becomes TE+ if δ < 0.458 × the trained effect.
- C1 becomes TE+ only if δ < 0.157 × the trained effect.
- **C3 stays TE+ only if δ < 0.548 × the trained effect** (lo95 2.93 against a trained 5.34).
- C4 stays TE+ only if δ < 0.664 × the trained effect.
- Report §6 item 1 names only C1 and C2 as δ-sensitive.

**O9. Ceiling check.** Random-arm subject-level PR on 28-subject sets is about 20 at L2/L3, against an n−1 ceiling of 27. That is not saturated, so C3/C4 are not a ceiling artefact.

## 2. Logic Chain
1. O1 → H1′ holds: the rule was frozen and committed before any random-init forward on real frames.
2. O3 and the gate record → H2′ holds. The replicated pipeline reproduces the trained statistics, as the worker's gate shows. My code-independent seed-8 rerun reproduces the shipped random arm bit-for-bit to float64 round-off, so the random arms are what they claim to be.
3. O2 and O4 → the shipped labels follow from the saved outputs under the frozen rule: C1 INC, C2 INC, C3 TE+, C4 TE+, and Family L as shipped.
4. O6 → the suite does not guard the family C seed wiring or the stats-script arm loading. A plausible wiring error flips the primary C1 label with 71/71 green. This is the same class as the earlier M2 gate failures: verdict-path wiring and full-output regression unguarded, real verdict unchanged. So the claim "verdict path mutation-tested (32/32 killed)" is incomplete, and it is refuted as a coverage claim.
5. O8 → the δ caveat in the report is incomplete. The C3 TE+ label, which carries the main R2 consequence, has only about a 10% margin on δ, and δ has not been confirmed by the PI.

## 3. Caveats
- I did not rerun the gate (R0). The G1–G5 values come from the in-job record. The worker's gate, three explorer smokes and my seed-8 rerun all point to a deterministic pipeline. Reviewers/auditor reran seeds 3 and 7 (ledger rows 218065–218067); I have not read their results.
- Driver mutants N71–N74 need GPU and real frames, so offline tests cannot be expected to kill them. I list them as nonblocking.
- N42 is equivalent; N11 changes p values and CIs slightly but no label, as far as I checked.
- A `__pycache__` exists in `src/topic3_h2/vendor/swift_cd87338_models/` (created 17:08:20Z, origin not determined), and one is in my own verification dir. Deleting mine was refused by the permission system; it is harmless.

## 4. Conclusion
- **The results are CONFIRMED.**
  - Gate: PASS, as recorded.
  - Family C: C1 INC, C2 INC, C3 TE+, C4 TE+.
  - Family L: as shipped.
  - Consequences: the R2 subject-level drop is produced by training; R2 token H1a is unresolved; R1 and R3 are unchanged.
- **Blocking issue (tests only): the H2 verdict path is not fully guarded.**
  - Fix: add tests, with no src change and no rerun:
    - (a) a full-output regression that runs `scripts/topic3h2_stats.py final` (and `gate`) in a tmp copy and compares every label and number with the shipped `h2_results.json` / `gate_decision.json`. This kills N50–N59 and N53.
    - (b) a synthetic family C test whose K seeds differ enough that using one seed changes a label or the seed_effects. This kills N26 and N27.
    - (c) a test pinning the J seed and that the corr subsets use pr_corr (N40, N41), plus comparator boundary tests (N30–N33, N35, N38).
- **Nonblocking:**
  - Report §6 should state that C3 and C4 are δ-sensitive too: TE+ needs δ < 0.548× and 0.664× the trained effect.
  - δ needs PI confirmation.
  - Fix the `card_sha256.txt` receipt format.

## 5. Verification Method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -I verification/challenger_M2H2_r1_2/recompute.py   # 0 label mismatches
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 verification/challenger_M2H2_r1_2/fuzz_decide.py      # 0 mismatches
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 setsid nohup nice /home/juke/superclaude-env/bin/python3 verification/challenger_M2H2_r1_2/mutants_ch2.py > verification/challenger_M2H2_r1_2/mutants_ch2.log 2>&1 &   # N26/N27/N53/N50-N59 survive
cat verification/challenger_M2H2_r1_2/survivor_impact.out.txt   # N26/N53 flip C1 INC->EQ on real data
cat verification/challenger_M2H2_r1_2/gpu_probe/probe_seed8_218068.json   # seed-8 rerun maxrel <= 2.3e-15
```
Invalidation: the finding is closed when new tests kill N26, N27, N53 and N50–N59 (rerun `mutants_ch2.py`) and the shipped `h2_results.json` is unchanged.
