# handoff — explorer_FU_C_r1_3 (FU_C, explorer 3 of 3, lens: adversarial pre-mortem)
Written 2026-11-01T15:05Z (UTC). Type: explorer analysis (Hard, 5 sections). Probes: /home/juke/git/00IITP-AI/verification/explorer_FU_C_r1_3/. GPU used: 0.14 GPU-h (Slurm job 398, ledgered start and end rows).

**Bottom line.** FU-C is cheap and feasible inside its 13 GPU-h cap if the worker trains **8 fresh seeds s = 5..12** (24 runs, about 10.6 GPU-h). It should reuse the pinned r1 fixture gate, backed by a bitwise-equivalence check, and use the r1 prepared HCP data through an **hNN-token data directory**, so run.json never carries content-hash tokens. Three ways the milestone could go wrong are the most dangerous:
- (1) A C4 regression, if the worker points `--data-dir` at the r1 directory. train.py then writes the unsalted content-hash tokens into every run.json, which is the r1 B1 defect again.
- (2) Seeds that are not actually fresh. Training is bitwise deterministic, so seeds 0..4 just reproduce the r1 runs.
- (3) Verdict wiring that repeats the r1 defect classes. The r1 script even treats a missing F− gate as a pass.

The verdict is almost certain before any run. With an r1-like effect, P(stop) ≈ 1. The card must say this, and it must frame FU-C's value as precision: the expected I1 half-width drops from 0.215 % to 0.144 %.

## 1. Observation

O1 (cost basis). Result report §7, option C: "8 seeds × 3 arms at E36 … 24 runs … ≈ 10.5". The measured rate is 0.43 GPU-h per run. The PI cap is 13 (PI_DECISIONS item 7). r1 runs took 1518–1572 s each with 8 running at once on one node (ledger rows 03:16Z–05:09Z).

O2 (frozen code that FU-C cannot use as is).
- `scripts/topic2_verdict.py` hardcodes `HCP_SEEDS = (0, 1, 2, 3, 4)`.
- `scripts/topic2_build_partitions.py` hardcodes `S_SEEDS_HCP = (0, 1, 2, 3, 4)`.
- `scripts/topic2_launch_wave.py` launches directly with an nvidia-smi idle check, which is forbidden under Slurm.
- In the verdict script, `fm is not False` treats a **missing** F− gate as passed. `S.verdict` returns `inconclusive` on F+ failure, but the script returns `no_verdict` "Stage 1 incomplete" when F+ fails and Stage 1 is not run (challenger_M3_r2_2 case A).

O3 (C4 source). `src/topic2_rgpool/train.py:245`: `rec["test_pseudonyms"] = list(te.pseudonyms)`. The pseudonyms are the subject directory names under `--data-dir/subjects/`. On B300 the r1 prepared dirs `/scratch/iitp4/worker_M3_r1/hcp/subjects/*` are named by the unsalted content-hash prefix. There are 88 of them, 126 GB in total (ls/du counts only).

O4 (Slurm and data locality, probed 14:2xZ).
- `sinfo`: partitions gpu, interactive and debug, with 4 idle nodes b300-[01-04].
- `/scratch` is node-local ext4 (`/dev/md0`, 28 T).
- The raw HCP directory (1,084 entries) and the r1 prepared data sit on 61.107.201.98, which is b300-01 (`/etc/hosts`: 192.168.0.2 b300-01 cloud-S1HDe3).
- Slurm is `select/cons_tres` with `CR_CORE_MEMORY` (memory is consumable). Accounting includes gres/gpu.
- `sacct` prints **KST** times. Job 398 shows Start `2026-11-01T23:37:41` for a 14:37:41Z start.
- The B300 sshd is slow: banner timeouts at ConnectTimeout 20 s, success at 120–150 s. A ControlMaster socket helps.

O5 (r1 artifacts on B300, read-only; first 16 hex characters shown).
- `code/split.json` c13b5f21… and `hcp/manifest.json` 26ba34a9… both equal the card pins.
- `partitions/fc_train_group.npy` and `partitions/perms_hcp.npz` ec05b796… are present.
- The venv is torch 2.15.0+cu134 / numpy 2.5.4 / scipy 1.18.1.
- 33 run directories with `model_final.pt` are present.

O6 (smoke, Slurm job 398: debug partition, `-w b300-01`, 1 GPU, `-c 8`, `--mem=200G`; ElapsedRaw 504 s = 0.14 GPU-h; outputs in `verification/explorer_FU_C_r1_3/b300_out/`):
- **(A) Synthetic Fplus_C_s0.** The frozen code copy (sha 15/15 OK) ran with the r1 venv under Slurm for ≤170 s. **9/9** logged `loss_mean_last100` values (steps 100–900) are **bitwise equal** to the r1 log (`out_A.json`, max_abs_diff 0.0).
- **(B) CPU checks, all true** (`out_B.json`):
  - The 88 dirs equal the original manifest order, and that order is sorted, so token hNN = position. This is the r2 sanitizer rule.
  - The repo sanitized split maps in order onto the original split, for train, val and test.
  - 88 hNN symlinks resolve.
  - The FC float32 sha equals `partitions_hcp.json` (e2912ee9…).
  - Rebuilding the C perm and **S_seed0..4** from that FC with the frozen `P.build_perm` gives arrays bitwise equal to `perms_hcp.npz`.
  - S_seed5 builds in 0.2 s and differs from every r1 surrogate (231 rows changed).
- **(C) Real-data r1 hcp_E_s0.** It was run through the hNN symlink dir plus the repo sanitized `split.json` (sha cc521b08…) for ≤330 s, with no test evaluation. **17/17** logged losses (steps 100–1700) are **bitwise equal** to the r1 log (`out_C.json`).
  - Data load took 20.0 s.
  - Peak GPU memory was 151,874 MiB of 275,040, so one run per GPU.
  - Host MaxRSS was 2.5 GB.
  - The throughput probe projected 0.44 h per run, while 3 other FU explorer smokes shared b300-01 (squeue: jobs 401, 402, 403).

O7 (r1 seed statistics; `verification/explorer_FU_C_r1_3/probe_power_oc.out.json`, from r1 verdict.json).
- I1: mean 0.147 %, sd 0.173 %.
- I2: sd 0.380 %, or 0.092 % without stalled seed 2.
- t975: 2.776 at df 4 and 2.365 at df 7. Expected I1 half-width: 0.215 % at n = 5 and **0.144 %** at n = 8.

O8 (operating characteristics of the frozen `S.verdict` at n = 8, r1 sd, 4,000 simulations each):

| true I1 | stop | keep | inconclusive |
|---|---|---|---|
| ≤ 0.5 % | 100 % | — | — |
| 0.75 % | 93 % | — | 7 % |
| 1.0 % | 2.7 % | 49 % | 48 % |
| ≥ 1.25 % | — | 100 % | — |

E-arm stall hazard, with a stalled E run giving I1_s ≈ +1.25 % at a true I1 of 0.15 %:

| stalled E seeds | verdict |
|---|---|
| 1 | stop |
| 2 | stop (99.98 %) |
| ≥ 3 | inconclusive (≥ 99.9 %) |

Two looks (r1's 5 seeds, then 8 pooled) against fresh 8, false keep/modify rate at true I1 = 0.9 δ: 4.9 % → **11.4 %**; at 0.8 δ: 0.04 % → 0.49 %.

O9 (pins and integrity, local).
- C1 `sha256sum -c PROTECTED_HASHES.txt`: rc 0.
- All 12 r1 fixture `run.json` files are pinned in `results/topic2/2026-11-01/output_sha256_r2.txt` (36 F lines; `-c` OK).
- The frozen code subset passes `sha256sum -c` locally and on B300.

O10 (other teams). Explorer dirs exist for FU_A..FU_E and M3_r3 (`ls` of the run root). The M3 r3 team owns `tests/topic2_rgpool` and addendum_06. Root's autocommit commits `docs/03_empirical_analysis/topic*/**` every 15 min (GATE_STATUS; explorer_M3_r2_2 O4).

O11 (r1 rules worth inheriting).
- A stalled run (`hcp_S_s2`, NMSE 1.0000) counted as valid (addendum 04).
- A software failure is a timeout, non-finite loss or crash. Its rerun is "identical command, once", and a second failure gives no_verdict (card §5).

## 2. Logic chain

L1 (fresh vs reuse). O6 A and C show bitwise-deterministic training under Slurm. "8 fresh seeds" therefore has to mean seeds **disjoint from 0..4**. Seeds 0..4 would reproduce r1 runs exactly, which is a disguised 5 + 3 pooling.
- The PI's costing (O1: 24 runs ≈ 10.5) also implies 24 new runs.
- Pooling with r1 re-reads already-verdicted data and more than doubles false positives near the boundary (O8: 4.9 → 11.4 %). It also imports the stalled S_s2 tail (O7).
- So: **seeds 5..12**. Their seed streams (weights s, order 1000+s, masks 2000+s) do not collide with r1's {0..4, 1000..1004, 2000..2004}, with fixture 3000+s, or with eval masks 7001/7002.
- A 13-seed pooled analysis may be pre-specified as descriptive only.

L2 (budget).
- 24 × 0.44 = 10.6 GPU-h, plus two partial equivalence reruns (≈0.2) = 10.8, leaving ≈2.2 for reruns (≥4 at 0.45).
- Rerunning the F+ gate (6 × 0.44 = 2.6) would push the plan to ≈13.4, over the cap. So the gate must be **reused** from the pinned r1 records.
- That reuse is legitimate only because the code, env and budget are unchanged and O6A shows bitwise reproduction. The card must say so, and the worker must repeat the equivalence check in its own env before Stage 1.

L3 (C4). Per O3, the tokens written to run.json are the directory names. O6B and O6C show that an hNN-named directory plus the repo sanitized split gives:
- identical training data order, with bitwise-equal losses;
- only h-tokens in the outputs;
- inherited dev-subject exclusion (the 88 already exclude the 5), so the sealed dev salt is not needed.

L4 (partitions). C does not depend on the seed, so it equals the r1 perm. S needs new surrogates S_seed5..12. O6B shows that the r1 float32 FC plus frozen `P.build_perm` reproduces r1's C and S_seed0..4 bitwise. This makes the new surrogates verifiable without rereading subjects. The build sees no outcome, so it may precede the freeze, and its sha values can then be pinned in the card.

L5 (node). Per O4, data and r1 prepared files exist only on b300-01's local /scratch. Every FU-C job needs `-w b300-01`, otherwise it crashes at load. The other FU teams contend for the same 8 GPUs (O6C: 4 smokes at once). Throughput was unaffected at that load.

L6 (verdict code). O2 lists inherited wiring defects. FU-C needs its own wiring around the imported `S.*` functions, with mutation-tested guards (§4.6).

L7 (interpretation). O8 implies stop is near-certain unless the r1 effect estimate was badly off. FU-C's contribution is a tighter bound: at the r1 mean, the expected upper bound is ≈ 0.29 %. A non-stop result is plausible only through artefacts (O8 stall row, L1 pooling). Those must be pre-specified away now, not explained later.

## 3. Caveats

- I measured determinism only up to step 1700 (hcp) and 900 (synthetic). I did not test full 8,750-step bitwise reproduction or test-NMSE reproduction. r1 verifiers had already shown checkpoint re-evaluation to be bit-identical (ledger rows 05:52Z–06:09Z).
- Determinism held on b300-01 with the r1 venv. A freshly built venv, even from lock.txt, or another node is unverified. That is why §4.3 requires the worker to repeat it.
- My smoke used the r1 venv at `/scratch/iitp4/worker_M3_r1/venv` and the r1 prepared data **read-only**. Both belong to the retired worker_M3_r1, not to any active FU team. Root may prefer that the worker builds its own venv.
- Probe C trained on real HCP data. It ran the already-reported r1 configuration (arm E, seed 0) and stopped before evaluation. It produced no new seed and no FU-C-governed number, but the FU-C card §0 must disclose it.
- The stall rate is estimated from 1 in 15 r1 runs, so it is very uncertain.
- The OC simulation assumes normal seed noise at the r1 sd.
- I did not check FU-A..E plans for b300-01 contention beyond one squeue snapshot.
- I did not read the peer FU_C explorers' work, which was empty at the time, by design.
- C4 adjudication of my own outputs:
  - `b300_out/out_B.json` contains one quoted 16-hex string, `orig_split_sha256_prefix`. It is the first 16 hex characters of the r1 split **file** hash c13b5f21b67f456f…, which is already quoted in full in card §4. It is not a subject token.
  - The 6-digit numbers in `slurm-398.out` are GPU MiB and RSS values.
- My B300 probe dir has been removed. Local copies of the probe scripts and outputs remain in verification/explorer_FU_C_r1_3/.

## 4. Conclusion — strategy for worker_FU_C (recommendation; covers F1, F2, F3, C1–C8)

### 4.1 Paths (no collisions with M3 r3 or FU-A/B/D/E)
- Card: `docs/03_empirical_analysis/topic2/<UTC-date>_topic2_fuC_card.md`.
- Addenda: `…_topic2_fuC_addendum_NN.md`.
- Report: `…_topic2_fuC_result_report.md`.
- Results: `results/topic2/<UTC-date>_fuC/`, containing `card_sha256.txt`, `code_sha256_at_freeze.txt`, `partitions/`, `runs/`, `verdict.json`, `id_scan_b300.json` and `gpu_hours_fuC.txt`.
- Code: `scripts/topic2_fuC_*.py`. Do not edit any frozen `scripts/topic2_*.py` or `src/topic2_rgpool`.
- Tests: `tests/topic2_fuC/` with an `__init__.py` and unique basenames. Never touch `tests/topic2_rgpool`.
- B300: `/scratch/iitp4/worker_FU_C_r1/` only.

### 4.2 Card content (freeze before any FU-C Stage-1 run; F1)
- **§0 disclosure:**
  - r1 results are known.
  - The predicted outcome is `stop` (O8).
  - Explorer probes ran (O6), including the real-data partial replication of r1 hcp_E_s0.
  - Perms built pre-freeze (if done).
- **Factor, arms, metric, δ:** identical to r1, with δ = 0.01 (PI decision 3).
- **Seeds:** s = 5..12, fresh, 24 runs. State "the 5 r1 seeds are NOT reused".
- **Pre-specified descriptive analyses** (never verdict-bearing):
  - 13-seed pooled r1 + FU-C;
  - FU-C without stalled runs.
- **Gate:** the r1 §7.2 gate is reused, computed by FU-C code from the 12 pinned r1 fixture run.json files. Its validity condition is E0 below (bitwise). Pre-specified fallback if E0 is not bitwise:
  - rerun F+ only, 6 runs ≈ 2.6 GPU-h;
  - if the plan then exceeds the cap, stop and report rather than launch.
- **Data:**
  - the r1 88 prepared subjects through an hNN-token directory;
  - the repo sanitized split (sha cc521b08…), whose mapping to r1's c13b5f21… is proven on B300 by booleans only;
  - the dev-subject exclusion is inherited.
  - Limitation: the 16 test subjects and the eval masks (7002) are the same as r1. FU-C replicates across training seeds, not across subjects.
- **Perms:**
  - E is the identity;
  - C must equal r1's C (sha 21e4e239…);
  - S_seed5..12 come from the r1 FC (sha e2912ee9…) through frozen `P.build_perm`;
  - the sha of every perm is pinned.
- **Run integrity:**
  - Stall = valid run (r1 rule), plus a stall flag (descriptive).
  - Software failure = Slurm time limit, OOM, crash, non-finite loss, or throughput abort. Rerun once with the identical command under a new attempt directory. A second failure leaves that seed missing and gives **no_verdict**.
  - The card notes that a deterministic failure will repeat. There is **no seed substitution**.
- **Verdict:** card §8 rules verbatim, with explicit semantics for missing gates:
  - F+ missing, failed or unverifiable → `inconclusive` (measurement capacity);
  - F− missing or failed → `keep` downgraded to `inconclusive`;
  - `modify` is never downgraded;
  - stop iff hi < δ, strictly.
- **Reading against r1:** fixed in the card. FU-C stands alone and r1 stays as recorded. Give a 2×N table of r1 `stop` × FU-C {stop, inconclusive, modify, keep} with the pre-written reading for each cell.
- **Compute:**
  - cap 13;
  - per-run `-t 00:40:00`;
  - the launch rule in §4.4;
  - GPU-h from sacct ElapsedRaw × GPUs.

### 4.3 Order of work
1. **E0 equivalence, ≤0.25 GPU-h, one Slurm job.** In the worker's own env, rerun ≤1700 steps of r1 `Fplus_C_s0` and `hcp_E_s0` (through the hNN dir) and compare every logged `loss_mean_last100` with the r1 logs for bitwise equality. The probe scripts `verification/explorer_FU_C_r1_3/b300/{job.sbatch, probe_map.py, compare_logs.py}` are a template: copy and adapt them, do not import them.
2. Build `perms_fuC.npz` (E, C, S_seed5..12). First assert that C and S_seed0..4 rebuild bitwise against r1, then pin the sha values.
3. Write the code and tests (§4.6), pin the code, then freeze the card. Record the card sha, and later the `git log` commit time of the card, read-only, made by the autocommit.
4. Launch Stage 1 in waves of ≤8 jobs, one GPU each, with the cap rule. Use `--save-model`, on B300 only: it enables cheap verifier re-evaluation (r1 precedent ≈0.01–0.03 GPU-h).
5. Copy back run.json, train_log and stdout. Run the count-only C4 scan on B300 over all FU-C outputs, then the verdict, then the report.

### 4.4 Slurm and ledger recipe
- Job settings:
  - `sbatch -p gpu -w b300-01 --gres=gpu:1 -c 8 --mem=64G -t 00:40:00`;
  - measured MaxRSS was 2.5 GB and peak GPU memory 152 GB, so one run per GPU.
- One job per (arm, seed, attempt), with the run dir `runs/hcp_<arm>_s<seed>_a<k>`. The job id goes in the ledger row and in a side record. The run.json schema is frozen code, so do not add fields there.
- Ledger: a "started" row at submit and a "completed" row from `sacct -X -j ID -o ElapsedRaw,AllocTRES`. Convert KST → UTC. Use `scripts/topic2_ledger.py --agent worker_FU_C_r1` (it uses flock).
- Cap rule before each submit:

  `used_closed_FU-C + 0.667 × (open jobs) + 0.667 ≤ 13`

  - 0.667 is the -t 40 min worst case.
  - The plan totals 10.8.
  - Worst case for the last wave: 16 × 0.44 + 8 × 0.667 = 12.4, which is ≤ 13.
- Never use `topic2_launch_wave.py`. Never ssh-launch on a GPU.

### 4.5 Pre-mortem: hazards, ranked (what verifiers will attack)

| # | hazard | consequence | prevention / test |
|---|---|---|---|
| H1 | `--data-dir` set to the r1 dir | run.json `test_pseudonyms` = unsalted content-hash tokens → C4 fail (the r1 B1 class) | hNN dir. Verdict asserts every token matches `^h\d{2}$` and equals sanitized split `test`. C4 scan of FU-C outputs. |
| H2 | "fresh" seeds overlap 0..4 | bitwise r1 replicas → hidden pooling, df overstated | SEEDS = 5..12 constant. Verdict errors if any seed ∉ SEEDS, or if a seed is missing or extra. |
| H3 | pooling with r1 chosen after seeing r1 | two-look inflation (O8); stalled S_s2 enters | fresh design. Pooled analysis is descriptive only. |
| H4 | gate not rerun | "no G6 gate for this experiment" | E0 bitwise. r1 fixture shas verified in code. Fallback pre-specified. |
| H5 | missing gate = pass (V07); r1 script also passes a missing F− | false keep | tests: F+ missing → inconclusive; F− missing → keep→inconclusive; modify unchanged (V06). |
| H6 | failed or duplicate attempts counted (V08/V10, p06-E) | software failure read as science | select only `status == completed`; exactly one completed attempt per (arm, seed), else error. Any seed without one → no_verdict (test). |
| H7 | E-arm stalls | ≥3 stalls flip stop → inconclusive (O8) | valid-run rule fixed in the card. Stall flag and sensitivity descriptive only. No reruns of stalls. |
| H8 | rerun of a deterministic failure "succeeds" only through a changed command | silent protocol change | identical command enforced (args recorded). No seed substitution. |
| H9 | job not pinned to b300-01 | crash at load, budget burn | `-w b300-01` in the launcher; a test checks the generated sbatch text. |
| H10 | sacct KST vs UTC | ledger/run.json time mismatch; freeze order disputed | convert; freeze anchor = card receipt time < first FU-C hcp run `start_utc` (verdict asserts it). |
| H11 | cap overrun at 3300 s worst case | F3 fail | -t 40 min plus the cap rule; abort-before-launch path reported. |
| H12 | card-vs-code mismatch (F+ fail → no_verdict) | V-class erratum again | one table in the card mirrored by parametrised tests over every branch. |
| H13 | boundary operators (V01–V05) | silent misclassification at ties | exact-boundary tests on both sides for stop (hi = δ), keep (mean = δ, lo = 0, I2 lo = 0) and F+ (gain = δ). |
| H14 | wrong perm per run (e.g. S_seed0 for all seeds, or C run with E perm) | arms not as specified | verdict checks each run.json `perm_sha256` against the pinned `(arm, seed)` table and `code_sha256` against the freeze pins. |
| H15 | test-order assertion dropped (V09) | subject misalignment in the bootstrap | assert one identical order across all 24 runs (test kills a removal mutant). |
| H16 | outcome predetermined | over-reading of "stop again" | card §0 prediction. Report precision gain (0.215 → 0.144 % half-width), not a new discovery. |
| H17 | shared test set with r1 | "independent replication" overclaim | stated limitation. |
| H18 | r1 dirs on volatile /scratch, owned by a retired worker | mid-campaign crash if wiped | hardlinks (`ln`, same ext4) into own dir instead of symlinks; or own venv via `build_env.sh` + `pip freeze` diff vs lock.txt, then rerun E0. |
| H19 | writing in `tests/topic2_rgpool` or addendum_06, or shared docs names | clobbering M3 r3 / other FU | §4.1 paths only. |
| H20 | anything token-bearing in docs/topic2 | autocommitted to git (C4) | docs carry aggregates only; scan before writing. |
| H21 | multiplicity over FU-A..E | a lone keep over-read | report at option level; note no cross-option correction. |

### 4.6 Verdict code and tests (F2; each test must kill its mutant)
- Import `S.t_interval`, `S.relative_gain`, `S.hierarchical_bootstrap`, `S.gate_fixture` and `S.verdict` (frozen, pinned). Put the wiring in `scripts/topic2_fuC_verdict.py`.
- Expect df = 7 and t_crit 2.3646.
- Mutation harness, analogous to challenger_M3_r2_2's V01–V11, plus new FU-C mutants:

| mutant class | mutants |
|---|---|
| V01–V11 analogues | missing F+ = pass; failed run counted; extra attempt counted; F− downgrades modify; `>=` vs `>` at each of the 5 boundaries; order assert removed; stop kept on F+ fail; F+ fail → no_verdict |
| new FU-C mutants | seed set includes 0..4; extra seed silently used; missing seed tolerated; perm-sha check removed; code-sha check removed; token-shape check removed; r1-fixture-sha check removed; df hardcoded 4; I1 against S; pooled-13 analysis feeds the verdict |

- Report survivors honestly, with equivalence proofs where they apply.
- Synthetic fixture runs for the verdict path: fabricated run.json sets in `tmp_path`, never real data.

## 5. Verification method

- **Smoke evidence:**
  - `cat verification/explorer_FU_C_r1_3/b300_out/{slurm-398.out,out_A.json,out_B.json,out_C.json}`. Expect `n_bitwise_equal` 9/9 and 17/17, and every boolean true.
  - Ledger: `grep "Slurm job 398" results/gpu_ledger_2026-10-31.md` shows a started and a completed row, 0.14 GPU-h.
  - Slurm: `sacct -j 398 -X -o ElapsedRaw,AllocTRES` (on B300) gives 504 s with gres/gpu = 1.
- **OC numbers:** `cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_C_r1_3/probe_power_oc.py results/topic2/2026-11-01/verdict.json /tmp/oc.json`. The RNG is seeded (12345), so the numbers are reproducible.
- **Defects O2/O3:**
  - `grep -n "HCP_SEEDS\|fm is not False" scripts/topic2_verdict.py`
  - `grep -n S_SEEDS_HCP scripts/topic2_build_partitions.py`
  - `grep -n test_pseudonyms src/topic2_rgpool/train.py`
- **Integrity:** C1 rc 0. Fixture pins: `sha256sum -c <(grep "runs/F.*run.json" results/topic2/2026-11-01/output_sha256_r2.txt)`.
- **Invalidation conditions.** Any one of these voids the recommendation:
  - E0 not bitwise in the worker env → gate reuse is void, use the fallback;
  - `dirs_eq_manifest` or `split_*_maps_in_order` false → the hNN mapping is invalid, stop;
  - r1 FC/perm rebuild not bitwise → S_seed5..12 are unverifiable, stop and report;
  - measured per-run GPU-h > 0.5 → re-cost against the cap before Stage 1.
