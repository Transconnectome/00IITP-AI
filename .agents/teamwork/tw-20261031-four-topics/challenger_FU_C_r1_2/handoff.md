# Hard handoff — challenger_FU_C_r1_2 (milestone FU_C), 2026-11-01T20:3xZ

Verdict: **REFUTED, for one C4 compliance defect only.** Everything scientific is CONFIRMED by independent recomputation: the numbers, the `stop` verdict, the freeze order, the gate, the ledger and the provenance.

## 1. Observation

**Headline numbers.** I recomputed them with my own code. The script does not import `src/topic2_fu_c` or the frozen stats. Script: `verification/challenger_FU_C_r1_2/recompute/recompute.py`; output: `recompute.out.json`.
- Per-record test_nmse = Σnum/Σden: maximum relative error 0 across all 24 records.
- I1 = −0.1132 % [−0.4985 %, +0.2721 %], df 7.
- I2 = +0.0083 % [−0.5200 %, +0.5366 %].
- The card rule gives `stop`, with the qualifier "sign unresolved".
- Stalls (loss_mean_last100 never below 0.995): exactly C_s16 and S_s15.
- Drop-stalled sensitivity: I1 +0.040 % [−0.213 %, +0.293 %], df 5.
- Pooled 13 seeds: I1 −0.013 % [−0.248 %, +0.222 %], df 12.
- r1 gate from the 12 sha-checked fixture records: F+ +3.061 % / +2.935 %, F− −1.737 %. Both pass.
- Hierarchical bootstrap (my own implementation): I1 [−0.450 %, +0.143 %], I2 [−0.422 %, +0.437 %].
- All of these equal `verdict.json` to full precision.
- Rerunning `scripts/topic2fu_c_verdict.py --out verification/.../verdict_rerun.json` gave output that is `cmp`-identical to the shipped `verdict.json`.

**Provenance.** Script: `recompute/provenance.py`. All 24 records pass every check:
- arm and seed match the directory;
- the r1 settings;
- perm_key, and perm_sha256 against the card §3.3 table parsed from the card text;
- the perm file sha f9e32ab7…;
- code_sha256 equals the r1 freeze pins;
- the split sha cc521b08…;
- 16 h\d{2} tokens in the split's test order;
- start_utc after the card freeze and after the code receipt.

The split has 64/8/16 subjects with 0 overlap.
- perms_fu_c.npz: E and C are array-equal to r1 perms_hcp.npz, as are nvox and group_mask.
- The 8 new S perms are valid permutations, distinct from each other and from r1 S0..4.

**B300 (CPU only, no GPU used).**
- The 48 B300 `run.json` and `train_log.jsonl` files are sha-identical to the repo copies (0 failures).
- `sacct` lists 29 FU-C-named jobs. These are the 4 explorer jobs (398, 401, 410 CPU, 414), the anchor 501 and exactly 24 Stage-1 jobs (512–562). There are no hidden or extra attempts.
- Every Stage-1 run.json was last modified 1–2 s before its Slurm End time, so the jobs wrote them and nobody edited them afterwards.
- The B300 code tree matches the 15 r1 freeze pins (src/topic2_rgpool + scripts/topic2_train.py; 0 failures). Its last src mtime is 00:33 KST (15:33Z), before every run.
- On B300, `inputs/split.json` sha = cc521b08….
- All 24 sbatch files use the same argument set as card §4.
- `sacct` shows 0 `g3t-G-E0` jobs in the window.

**Freeze order.**
| event | time (UTC) | source |
|---|---|---|
| card receipt | 16:13:23Z | `# frozen_utc` |
| card sha prefix `fc2d0672` and its freeze time | 16:20:26Z | daemon commit e5fa8de, which contains worker_FU_C_r1/progress.md |
| verdict-code receipt | 16:31:53Z | receipt (verdict.py mtime 16:31:25Z) |
| first job start | 16:35:09Z (sacct) / 16:35:12Z (run.json) | sacct, run.json |
| verdict.json | 19:39:53Z | file mtime |

**Anchor.** I checked 6/6 step-100/200 losses: they are bitwise equal to the r1 logs. The anchor logs contain no val or test events.

**Ledger.** FU-C closing rows sum to 10.684 GPU-h (explorers 0.262, worker 10.422). Every started row is closed. sacct elapsed sums to 10.666 h (the ledger rounds up). The cap is 13.

**Mutants.**
- The worker's own harness, rerun on the current code (verification/challenger_FU_C_r1_2/mutants/worker_rerun.out.json), reproduces 51/54 killed with the same 3 survivors. I checked that V07c, V12 and F11 are equivalent.
- My 40 additional mutants (`my_mutants.py`, `my_mutants.out.json`): 21 killed, 19 survived (see §2).
- **C4 (blocking).** I compared every 6-digit digit run in the worker's 171 deliverable files with the 1,084 HCP directory names on B300. This was a count-only scan through stdin; the name list was held only in /dev/shm on B300 and was removed. Exactly **1 hit**: `tests/topic2_fu_c/test_gate_and_records.py` line 182, the parametrized fixture commented "# HCP-ID shape". It is a real HCP-YA participant ID present in the project's B300 HCP download; it is the subject HCP's own documentation uses as its example. No other worker file contains a real ID. A derived copy exists in another agent's dir: `verification/reviewer_FU_C_r1_2/mut_work/x/m/tests/topic2_fu_c/test_gate_and_records.py`.
- **Freeze-time guard (nonblocking).** `adversarial/adv.py` ran the shipped `evaluate` on copied trees. A record with `start_utc = "2026-11-02T01:00:00+09:00"` (= 16:00Z, before the freeze) still gets `stop`. The cause is that `check_record` compares the ISO strings lexicographically (`not st > fz`). The other adversarial cases are all correctly `no_verdict`: seed field ≠ directory, test_nmse tampered by 0.05 %, a negative num term, token "h"+6 digits, an extra `*.bak` dir, a duplicate completed a2, and a failed a2 after a completed a1.

**Other checks.**
- C1 rc 0. FU-C receipts: card, code and output all pass with 0 failures.
- `tests/topic2_fu_c`: 109 passed.
- Whole-run layout lint: 0 findings, rc 0.

## 2. Logic chain

1. Independent arithmetic, provenance, B300 byte-identity, sacct, mtimes and the bitwise verdict rerun all agree, so the reported numbers are what the frozen code produced from untampered records.
2. Card §5: hi = 0.272 % < δ = 1 %, so `stop`. lo < 0 < hi, so the qualifier is "sign unresolved". The F+/F− gate verifies from the pinned records. So the verdict follows the card.
3. Third-party timestamps (the daemon git commit, sacct) put the card freeze, and the verdict-code pin, before any run started. The result-access rule could not have been broken: no result existed before 16:35Z.
4. The cap and ledger hold.
5. C4 forbids writing HCP 6-digit IDs in any form. The test fixture writes a real one, in a production test file owned by the worker. So the deliverable violates C4 as written, whatever the intent was ("shape" test). The worker's C4 checks covered only the copy-back tree and `results/`, so they could not catch it.
6. My 19 surviving mutants fall into two groups.
   - Equivalent or measure-zero: X02, X03, X21, X25, X32, X33, X35, partly X36.
   - Guards that the shipped code implements correctly but that no test pins: X04/X05 (den/num validity), X06 (nmse tolerance), X20 (seed field vs directory), X22 (receipt order), X24 (stats.py pin), X28 (the token regex length and anchor, itself a C4 guard), X31 (required code pins), and the descriptive X10/X14/X15.
   - None can change the shipped verdict, because the shipped data pass every guard independently (step 1).

## 3. Caveats

- I did not re-score any checkpoint on GPU. The B300 queue was saturated (≥20 jobs PENDING from other teams), and the mtime and sacct evidence plus the explorer's earlier bit-identical re-score of r1 checkpoints make the marginal value low. 0 GPU-h used; no ledger rows.
- The verdict-code receipt hash has no third-party anchor before the results. Only file mtimes and the worker's committed progress note (commit cd1e43e, 16:35:27Z) state the pin time; neither carries the hash. The card hash is anchored by a prefix only.
- I did not rebuild the S surrogates independently. They need the train FC on B300. I relied on the 25/25 self-check, and I checked the arrays for validity and distinctness.
- Whether a well-known public example ID is "blocking" is a root/PI policy call. I classify it by the literal C4 text and by the M3 r1 precedent (that gate failed on recoverable tokens).
- **Remediation is not trivial.** The test file is pinned in `code_sha256_before_results.txt`, and `receipts.build_context` verifies every entry in that receipt. Editing the file therefore makes a verdict rerun return `no_verdict` unless a dated addendum adds a superseding receipt, or the root seals the original as it did for the dev salt.

## 4. Conclusion

- **CONFIRMED:** FU-C verdict `stop` ("gain below δ, sign unresolved") on seeds 10..17; I1 −0.113 % [−0.499 %, +0.272 %], df 7; I2 +0.008 % [−0.520 %, +0.537 %]; gate pass; freeze before results; 10.684 GPU-h of the 13 cap.
- **REFUTED (blocking, C4):** a real HCP participant ID is written at `tests/topic2_fu_c/test_gate_and_records.py:182`.
- **Fix:** replace it with a non-ID string such as `"h1234567"` or `"0000000"`, after checking it against the HCP name list count-only. Record the change in an addendum with a superseding test receipt, and contain the derived copy in `verification/reviewer_FU_C_r1_2/mut_work/`.
- **Nonblocking:**
  - the lexicographic `start_utc` guard;
  - the unpinned guards listed in §2.6;
  - the report §2.2 overstates the stall explanation: without the C s16 stall the I1 sd is still 0.220 % against 0.173 % in r1, so the half-width (0.204 %, df 6) is still above the predicted 0.144 %.

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_C_r1_2/recompute/recompute.py /tmp/x.json   # numbers
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 verification/challenger_FU_C_r1_2/recompute/provenance.py               # provenance
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_C_r1_2/adversarial/adv.py                 # guards
python3 -B verification/challenger_FU_C_r1_2/mutants/my_mutants.py $PWD <work> <out.json>                                                # mutants
```
C4 check (count-only; never print the token): extract the token on line 182 and pipe it over ssh to B300 for `grep -cxF` against `ls /scratch/data/hcp/download_HCP_REST1_filtered`. Expected: 1.

This conclusion is invalidated if line 182 changes, or if the B300 name list does not contain the token.
