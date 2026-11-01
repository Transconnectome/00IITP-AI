# Hard handoff — challenger_FU_C_r1_1 (milestone FU_C), 2026-11-01T20:15Z

**Verdict: CONFIRMED.** The FU-C `stop` follows the frozen card. Every headline number was rebuilt from the raw records and from the saved checkpoints. The freeze order holds. No claim in the worker's handoff turned out false.

One finding is nonblocking but real: 20 of my 33 new mutants of the verdict and receipt layer survive the 109-test suite. None of them changes the shipped verdict. One, X30, would change a verdict on heterogeneous inputs.

Overall risk: LOW for the shipped verdict; MEDIUM for test coverage of the verdict layer.

## 1. Observation

### C1, receipts and test suites
- C1 `sha256sum -c PROTECTED_HASHES.txt`: rc 0.
- The FU-C receipts (card_sha256.txt 36 lines, code_sha256_before_results.txt 15, code_sha256_presentation_before_results.txt 1, output_sha256.txt 160) have 0 failures each.
- Pre-existing failures in r1 receipts, not caused by FU-C:
  - `results/topic2/2026-11-01/output_sha256.txt` has 16 failures, `card_sha256.txt` 2 and `c4_sealed_originals_sha256.txt` 19. These are the hcp records, split and manifest that M3 r2 sanitized; they are superseded by `output_sha256_r2.txt` and `c4_sanitized_sha256.txt`, which have 0 failures.
  - The 12 F+/F− fixture pins that FU-C uses all verify.
- Test suites:
  - `tests/topic2_fu_c`: 109 passed.
  - Old suite (STRICT_E2E=1): 86 passed.
  - `tests/topic2_rgpool`: 116 passed.

### Independent recomputation from raw `runs/hcp_*_a1/run.json`
Script: `verification/challenger_FU_C_r1_1/recompute/recompute.py`. It uses scipy directly and imports nothing from `src/`.
- I1 = −0.1132 % [−0.4985 %, +0.2721 %], df 7.
- I2 = +0.0083 % [−0.5200 %, +0.5366 %].
- Verdict `stop`, qualifier "sign unresolved".
- Stalled runs: C16 and S15.
- Drop-stalled sensitivity (seeds 10–14 and 17): I1 +0.040 % [−0.213 %, +0.293 %].
- Pooled 13 seeds: I1 −0.013 % [−0.248 %, +0.222 %].
- r1 gate: F+ gains +3.061 % / +2.935 %; F− −1.737 %.
- All of these equal `verdict.json` to full precision.
- Re-running `scripts/topic2fu_c_verdict.py` gives a byte-identical verdict.json (sha 4d793102…).

### Provenance, checked independently for all 24 records
- Every record:
  - has the card's settings;
  - its perm_sha256 equals the sha of the npz array bytes;
  - its perm file is f9e32ab7…, its split is cc521b08…, and its code_sha256 equals the r1 freeze pins;
  - its test order equals the split's test order;
  - starts after the code pin.
- The E and C arrays equal the r1 perms_hcp.npz arrays, and all 10 keys are bijections that match the card table. The 8 new S surrogates are distinct from each other and from r1 S0..4.
- The 24 sbatch commands are identical apart from arm, seed and perm key, and each matches its run name.
- Every FU-C record has `test_den` bitwise equal to the r1 `hcp_E_s0` record (maximum relative difference 0). So the test subjects, their order, the masks and the data are all identical to r1.

### B300 (read-only)
- Code: the 16 files in `/scratch/iitp4/fu_c/code` that are pinned in r1 `code_sha256_at_freeze.txt` all match.
- Records: the 48 run.json and train_log.jsonl files on B300 equal the repo copies. No `_a2` attempt exists.
- `copyback/final/runs.tgz` sha is 5f3593ef…aec74, as addendum 01 states.

### Checkpoint re-evaluation (Slurm job 577)
- Debug partition, b300-01, 46 s, 0.013 GPU-h, ledgered with started and closing rows. The `squeue` check showed 0 g3t-G-E0 jobs.
- I re-scored 6 checkpoints on TEST with the frozen `evaluate_hcp`: C s16, S s15, E s14, C s14, E s10, C s10. For all 6, the per-subject num and den are bitwise equal to run.json.
- The planned negative control was void. I scored the C s14 weights with the E partition, but `perm` is a persistent buffer, so `load_state_dict` restored the C partition.
- I replaced that control with a CPU-only check of all 24 checkpoints (`ckpt_perm_check.out.json`). Each holds exactly 1 `perm` buffer equal to its record's partition. The 8 E checkpoints hold E; the 16 C and S checkpoints hold their own partition, not E.

### Other checks
- Anchor: the training losses at steps 100 and 200 equal r1 bitwise for hcp_E_s0, hcp_C_s0 and Fplus_C_s0. The anchor records contain no val or test keys.
- Timeline (UTC): anchor 16:04:53 → card frozen 16:13:23 → first submission 16:13:51 → code and tests pinned 16:31:53 → first run start 16:35:09 → last run end 19:33:54 → copy-back 19:39:46.
- Ledger: 25 started and 25 closing rows for 25 jobs; the closing rows sum to 10.422. Adding the explorers' 0.262 gives 10.684 GPU-h, under the 13 cap. At most 7 FU-C jobs ran at once.
- C4: a count-only scan of the FU-C results, the docs and the worker verification dirs found one 6-digit hit outside hex and floats: the voxel count 229304 in perms_fu_c.json, which is not an ID. No `sub-` labels.

### Mutation testing (my own harness, 33 new mutants plus a baseline)
- 13 killed: X04, X06, X07, X08, X12, X13, X14, X16, X20, X22, X23, X31, X32.
- 20 survived:

| mutant | what it breaks | classification |
|---|---|---|
| X30 | evaluate uses the mean of per-subject ratios instead of pooled Σnum/Σden | real gap; can flip a verdict (P7 below) |
| X09 | NMSE-consistency tolerance 1e-9 → 1e-2 | real gap; P3 (0.5 % tamper) is no_verdict in production |
| X01 | den ≤ 0 accepted | real gap; P1 |
| X02 | num < 0 accepted | real gap; P2 |
| X10 | gate record `source` not checked | real gap; P4 (sha pins mitigate) |
| X11 | gate record `seed` not checked | real gap; P5 (sha pins mitigate) |
| X26 | token regex `^h\d{2}$` → `^h\d+` | real gap in a C4 shape guard; P6, h + 6 digits |
| X03 | run start equal to the freeze time accepted | boundary; P8 |
| X05 | qualifier `hi < 0` → `<= 0` | boundary, wording only |
| X27 | bool accepted as a finite number | near-equivalent; P9 |
| X15 | "code receipt predates card freeze" check removed | receipt guard tested only by the 2 real-repo tests |
| X17 | frozen stats.py pin check removed | receipt guard tested only by the 2 real-repo tests |
| X21 | required verdict-code entries check removed | receipt guard tested only by the 2 real-repo tests |
| X28 | receipt without frozen_utc accepted | receipt guard; also fail-closed through the start-time check |
| X18 | split sha check removed | redundant: the governing pin also checks it |
| X19 | test list read from `val` | fail-closed on real data |
| X25 | `$` removed from the attempt regex | fail-closed through the numbering check |
| X29 | gate pins taken from any directory | equivalent |
| X33 | record section treated as governing | stricter; harmless |
| X24 | test-order check removed from the r1 records in the pooled analysis | descriptive analysis only |

- The 2 real-repo tests are `test_card_receipt_verifies_and_pins_every_required_governing_file` and `test_context_from_the_repo_has_no_problems_once_code_is_pinned`. They are deselected in mutation runs, as in the worker's harness.
- The worker's 3 equivalent survivors (V07c, V12, F11): I re-traced each and agree they are equivalent.

### Adversarial inputs against the production code
`verification/challenger_FU_C_r1_1/adversarial/probe_adversarial.out.json`. Every crafted input is handled correctly:
- P1–P6, P8 and P9 return no_verdict with the right problem.
- P7 has heterogeneous subjects. Production pools and returns `stop` (I1 0.19 %). The X30 mutant would see about 9.6 % and return keep or modify.

## 2. Logic chain
1. The verdict code was pinned at 16:31:53Z, before the first Stage-1 job started at 16:35:09Z. So the verdict rules could not have been tuned to the results.
2. The card was frozen at 16:13:23Z, before any submission. The pinned code's rules match card §5. I checked this by reading verdict.py and by my own implementation, which reaches the same category.
3. The records are genuine:
   - re-scoring the checkpoints reproduces num and den bitwise;
   - every checkpoint carries its declared partition;
   - the data, subjects and masks are identical to r1, from the bitwise test_den;
   - the code equals the freeze pins on B300.
   So the inputs to the verdict are the declared experiment.
4. On these inputs, I1's upper bound (+0.272 %) is below δ (1 %), so the result is `stop`. The conclusion survives three alternatives:
   - dropping the stalled seeds (+0.293 %);
   - the alternative mean-of-ratios estimator (+0.273 %);
   - replacing the C s16 stall with no effect (+0.200 %).
5. The mutation survivors are gaps in the tests, not bugs in the code. Production rejects every adversarial input. Because the shipped verdict.py is pinned and independently reproduced, these gaps cannot affect this verdict. They matter only for future edits or reuse of the layer.

## 3. Caveats
- **Measurement capacity (r1 design; interpretive, nonblocking).** Seed-mean test NMSE is about 0.988–0.990, so the models learn about 1.1–1.3 % below the predict-zero level. δ = 1 % relative is therefore close to the whole learned signal at this budget.
  - The F+ gate shows that the loop can detect about 3 % on the synthetic fixture, where NMSE is about 0.66. It does not show this on HCP.
  - The report states the stop literally and correctly. A reader should not take it as "box pooling cannot matter"; FU-A and FU-B target this.
- **Unverified by me:**
  - that the explorers never trained seeds 10–17 (I checked only the ledger purposes and the handoffs);
  - the squeue check at each of the 25 worker submissions (it was not logged per submission in a form I could check);
  - the worker's statement that it read only the `status` field before the copy-back. This is self-attested; step 1 of the logic chain makes it immaterial to the verdict.
- I did not rebuild the S surrogates with the frozen builder, because the train FC lives on B300. I relied on the recorded 25/25 self-check and on my own check that the surrogates are distinct bijections.
- The r1 gate is reused by reference, as pre-registered. The anchor proves bitwise determinism only to step 200.

## 4. Conclusion
- **CONFIRMED.** The FU-C verdict `stop` ("gain below δ, sign unresolved"), all headline numbers, the freeze order, the provenance, the GPU accounting (10.684 of 13) and C4 hold under independent re-implementation and re-scoring of the checkpoints.
- **Nonblocking recommendation.** Add additive tests (new files only; the pinned files stay unchanged) that kill X30, X09, X01/X02, X10/X11, X26, X15/X17/X21 and X03/X05. At minimum add a heterogeneous-subject fixture for X30 and a synthetic-receipt test for each receipt guard.
- Root decides whether this is gate-relevant, following the T2.4 precedent.

## 5. Verification method
```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
/home/juke/superclaude-env/bin/python3 -I verification/challenger_FU_C_r1_1/recompute/recompute.py      # compare with verdict.json
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_C_r1_1/mutants/run_mutants_ch.py $PWD /tmp/chm out.json
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B verification/challenger_FU_C_r1_1/adversarial/probe_adversarial.py
```
B300 probes: `verification/challenger_FU_C_r1_1/b300_reeval/` (`reeval_fuc.py` + `reeval.sbatch` under Slurm; `ckpt_perm_check.py` is CPU only).

This conclusion is invalidated if any FU-C receipt fails, if a run.json or checkpoint on B300 changes, or if a test-gap mutant is shown to be reachable in the pinned code path for the shipped inputs.
