# handoff — worker_M3_r3 (M3 Topic 2, iteration 3, ACCEPTANCE T2.4) — Hard handoff

## 1. Observation

Files created (nothing else changed; src/topic2_rgpool, scripts/topic2_*.py, the card, the 12 shipped test files
and every existing receipt untouched):
- `tests/topic2_rgpool/test_verdict_path_guards_r3.py` — 24 tests (new file).
- `docs/03_empirical_analysis/topic2/2026-11-02_topic2_addendum_06.md` — errata E1–E5, reading rule, shipped-verdict
  evidence, mutation table, salt containment, regression, carried-forward notes.
- `results/topic2/2026-11-01/addendum_06_sha256.txt` — 31 pinned files, 31/31 OK (receipt sha 4ac6d454…12fb).
- `verification/worker_M3_r3/` — m00 (verbatim spec builder), mutation_specs.json (24 specs), m01 harness,
  m01/m02/mA/mC outputs, m03 table, c00 connectome script, connectome/ (logs copied back), p01 errata probes,
  p02 W09 equivalence, s01 salt scan, r01–r04 regression/integrity/C4 attribution, prev_versions/ (failed s01 v1,
  pre-addendum s01 output).

Mutation evidence (verbatim specs: V01–V11 from challenger_M3_r2_2 p07_specs.json, cross-checked equal to its p05
MUT; 3 CTRL from p05; K1/K2 from challenger_M3_r2_1 run_mutants_c1.py; W04–W09, W12 from explorer_M3_r3_2 m03):
- Leg A (connectome srun debug, 12 shipped test files sha-checked 12/12 vs output_sha256_r2.txt, new file excluded):
  baseline 92 passed; all 20 non-control mutants SURVIVED; 3 CTRL KILLED; 0 INVALID.
- Leg B (local, new file only): baseline 24 passed; V01–V11, K1, K2, W04–W08, W12 KILLED with named tests (table in
  addendum_06 §4); W09 SURVIVED; CTRL_t_df_n and CTRL_boot survive (they are shipped-suite controls).
- Leg C (connectome, union): baseline 116 passed; 22/24 KILLED; only baseline and W09 survive; 0 INVALID.
- Leg D (local, mutated frozen script on shipped runs): baseline + 20 non-control mutants byte-identical to
  verdict.json (59af05e5…af68); 3 CTRL differ, still `stop`.
- W09 equivalence: analytic (lo ≤ m ≤ hi from t_interval) + p02: 0/1.2 M random and 0/1,440 grid disagreements;
  differs only on a malformed interval (mean > hi).
- connectome code sha 40/40 equal to local.

Errata probes (p01): 27 synthetic scenarios, frozen label vs card_reading differ in 12 (E1 2, E2 6, E3-strict 4);
E4 duplicate key: kept record = last in glob order (3/3 layouts); E5: plain rc 1 with the order message, `-O` rc 0
and writes `keep`. Shipped: 27 run.json, 27 distinct keys, all completed, 1 hcp test order, F+ pass (3.06 % /
2.93 %), F− pass (−1.74 %), hcp_complete, I1 t95 hi 0.361 % < δ 1 %, last F+ end 03:42:08Z < first hcp start
03:44:51Z, card_reading = stop.

Salt containment (s01, counts only, run after the addendum existed): sealed salt sha = root record 7e5434ab…d02e;
0400 / dir 0700 / parent 0700; not in a git work tree; old repo path absent. Salt needles (full, head12, tail12,
upper, base64, hex): 0 of 18,301 worktree files (2.31 GB), 0 of 1,730 blobs (3,212 objects, all objects).
Burned hashes: only 3 files in verification/explorer_M3_r1_1, 0 blobs. Recovery without sealed salt 0/5 over 8
variants; positive control 5/5. 0 name-hash windows (2 M windows). The statement "positions 0-4 of the sorted
listing" is in 7 worktree files (incl. addendum_06) and 4 blobs → positional residual, disclosed.

Regression (local unless noted): old 86 → 86 passed (r01); topic1_lagmotif 88 passed (r02); C1 67/67 rc 0;
code freeze 33/33; output_sha256_r2 156/156; c4_sanitized 19/19; c4_sealed_originals 19/19 vs
~/.local/share/00IITP-AI_sealed/topic2/sealed_c4_from_b300; old card pins fail exactly 2, old output pins exactly
16 (as disclosed in addendum_05). Full topic2 suite on connectome before addendum: 116 passed. Final r05 runs: see
§Verification / structured return.

**Foreign red test:** `tests/topic2_rgpool/test_outputs_no_ids.py::test_outputs_have_no_id_bearing_paths_and_only_manifest_pseudonyms`
FAILS locally because of `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md` (FU-B team's card,
created 2026-11-02 00:29 KST): the shipped BIDS-prefix detector fires once (r04_c4_attribution.out.json: that file is
the only flagged file; addendum_06 and the receipt have 0 hits). Not in my ownership; not edited.

## 2. Logic Chain

1. T2.4(1) needs attributable kills: each mutant must survive the shipped suite (leg A shows 20/20 survive with the
   12 pinned files, sha-verified) and be killed by the new file on its own (leg B), while the new file passes on frozen
   code (baseline legs B and C pass). Controls killed in A show A can detect changes.
2. Tests derive from card text (independent §8 oracle on an exhaustive grid, dyadic boundaries) rather than from the
   mutant list, so they guard the rule, not just the 11 edits; K1/K2/W-set added because other verifiers found them.
3. Errata E1–E3 cannot be asserted as card labels against frozen code; the [erratum] tests pin frozen labels and assert
   card_reading, keeping the deviation visible.
4. Shipped verdict: every errata precondition is false in the shipped records, and the mutated script reproduces the
   shipped verdict bytes under all 20 non-control mutants → `stop` unchanged; no real defect changes it.
5. Containment: zero salt/hash channel hits with a positive control → salted-hash route closed; positional route open
   (needs off-repo listing) → disclosed, not claimed closed.

## 3. Caveats

- E2/E3 are interpretive (card does not name a label for an uncomputed fixture gate); strict §5 reading adopted, narrow
  alternative stated. Root/PI may choose; only card_reading would change.
- Leg B ran locally on superclaude-env (numpy 2.3.5 / scipy 1.15.3); legs A/C on connectome torch 2.15.0+cpu env.
- Plain-text repo scan against the B300 HCP name list not re-run (needs B300 listing); last done by challenger_M3_r2_2.
- Not scanned: off-repo B300 /scratch copies, other sessions' /tmp scratch.
- The test_vendored_ver11 SwiFT_v2 upstream comparison skips on connectome (no SwiFT_v2 checkout there), as in r2.
- DISPATCH.md condenses the embedded explorer JSON (disclosed in its header).
- Two progress.md timestamps were estimates ahead of the clock; corrected by an appended line.

## 4. Conclusion

T2.4 closed for the enumerated set: V01–V11 (plus K1, K2, W04–W08, W12) are killed by the new additive test file with
attribution; W09 shown equivalent; addendum_06 records E1 (certain) and E2–E5 with an executable reading rule and
evidence that the shipped verdict `stop` is unaffected; dev-salt containment re-verified (salted-hash channel closed;
positional residual disclosed for a root/PI ruling). No regression attributable to M3. Root action: the FU-B card in
docs/03_empirical_analysis/topic2 trips the shipped C4 scanner (BIDS-prefix pattern) — the FU-B owner must reword it.

## 5. Verification Method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
grep -v '^#' results/topic2/2026-11-01/addendum_06_sha256.txt | LC_ALL=C sha256sum -c
LC_ALL=C sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt
grep -v '^#' results/topic2/2026-11-01/output_sha256_r2.txt | LC_ALL=C sha256sum -c
CUDA_VISIBLE_DEVICES="" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/juke/superclaude-env/bin/python3 -m pytest -p no:cacheprovider tests/topic2_rgpool/test_verdict_path_guards_r3.py -q
# attributable kills (new file alone; local, ~2.5 min):
python3 verification/worker_M3_r3/m01_mutants.py pytest $PWD verification/worker_M3_r3/mutation_specs.json <WORK> out.json --tests tests/topic2_rgpool/test_verdict_path_guards_r3.py
# shipped-only / union legs: verification/worker_M3_r3/c00_connectome_run.sh on connectome (srun -p debug)
```
Invalidation: any edit to src/topic2_rgpool, scripts/topic2_*.py or the shipped tests; a mutant anchor no longer unique.

## Addendum to Observation (final runs, after the receipt was written)
- r05 connectome final full suite (srun debug, CUDA hidden): (i) current docs dir incl. FU-B/FU-D cards: 115 passed,
  1 failed = test_outputs_no_ids (FU-B card, foreign); (ii) same tree with the 2026-11-02_topic2_fu_* cards left out
  of the docs copy: 116 passed. Logs: verification/worker_M3_r3/connectome/r05_final_suite_{i,ii}.log.
- r06 integrity (2026-11-01T15:57Z): C1 rc 0; code freeze 33; c4_sanitized 19; output_sha256_r2 156; addendum_06 31/31;
  old card pins 2 FAILED / 6 OK, old output pins 16 FAILED / 27 OK (expected); sealed originals 19/19.
- r07 old 86 rerun: 86 passed. r08 verdict-path files (new + test_stats + r2 guards): 38 passed.
- r09 whole-run audit_layout: rc 0, 0 findings.
- connectome work dir /storage/connectome1/iitp4_verify/worker_M3_r3 removed; no jobs or processes left; 0 GPU-h.
