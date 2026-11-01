# Handoff (Hard) — explorer_FU_D_r1_2, milestone FU_D (Topic 2 follow-up D, E192 d2-2-18-2)

Written 2026-11-01T15:0xZ (2026-11-02 KST). Lens: feasibility and failure modes. Explorer 2 of 3. Recommendation only; I wrote no production code.

**Summary.** FU-D is feasible within the 25 GPU-h cap only with a smaller gate than r1. I measured the real cost: one E192 run at batch 16 costs about 1.20 GPU-h (0.481 s/step). It fits in memory with all 88 HCP subjects on the GPU (peak 198 GiB of 268 GiB). The frozen code accepts E192 unchanged at M0. Three things must be designed in from the start, or FU-D fails on logistics or verdict code rather than on science:
1. Run the F+ gate with seed 0 only. Run F− only on E and C, and only if Stage 1 would otherwise be `keep`.
2. The worker needs its own verdict script. The frozen `scripts/topic2_verdict.py` gives the wrong label in all four of the reduced-design scenarios I tested.
3. All HCP data sit on b300-01 only. Every FU team that needs HCP will compete for those 8 GPUs.

## 1. Observation

| # | Observation | Evidence |
|---|---|---|
| O1 | The E192 config registers from outside `src/` with no edit. `train.CONFIGS is model.CONFIGS` (the same dict object), so `train.run` sees a key added by a wrapper. Geometry matches E36 exactly: `m0_grid` 16, `octant_edge` 8, 4 stages. | `verification/explorer_FU_D_r1_2/probe_e192_cpu.py` → `probe_e192_cpu.out.json` (P1, P2), rc 0, 22.6 s on CPU |
| O2 | At E192, M0 = `ConnectomeRGBoxPooling(PatchMergingV2)` with `LayerNorm(1536)` and `Linear(1536→384)`, input resolution (20,16,16,16). M1 (3072→768) and M2 (6144→1536) are stock PatchMergingV2, and stage 3 has no merge. The gather is channel-agnostic: `index_select` on the cell axis (`src/topic2_rgpool/merge.py` lines 30–33). | probe P3; P5: gather == reorder followed by stock PatchMergingV2 at dim 192, bit-exact in fp32 |
| O3 | The r1 C perm gives 474,226,176 parameters for both E and C, and the step-0 weights of E and C are bit-identical (seed 0, every state key except the `perm` buffer). | probe P4 |
| O4 | E192 config used (VRABES `extract_vrabes_swift_E192.sh` lines 81–85): embed 192, depths 2 2 18 2, heads 6 12 24 48, window 4 4 4 10, patch 6 6 6 1, img 96³×20, c_multiplier 2. VRABES itself used mask_ratio 0.8, lr 7e-5 and `last_layer_full_MSA`; ver11 swallows that last flag through `**kwargs`. | read-only file read; `simmim_swin4d_transformer_ver11.py` lines 934–1018 |
| O5 | **Measured cost** (Slurm job 396, b300-01, debug partition, 1 GPU; synthetic data only; 4 other FU smokes on the same node at the same time). With a GPU-resident dummy of the exact HCPSource footprint (88×1200×78×96×84 fp16 = 124.83 GiB) on the frozen `HCPSource.batch` path at batch 16: **0.4814 s/step = 33.24 samples/s**. All losses finite at constant lr 2e-4 with no warmup. **Peak 198.05 GiB** allocated (210.89 reserved) of 267.7 GiB. Fixture path: 0.4815 s/step, peak 74.2 GiB, F+ loss 1.55→0.96 within 25 steps. Frozen `evaluate_hcp`: 1.18 s per subject, about 57 s per run (4×8 val + 16 test). **Projected run = 1.20 h**: 4212 s train + 57 s eval + 21 s load (r1 measured) + 30 s. | `verification/explorer_FU_D_r1_2/smoke_fud.json` (sha256 bc429d9f…b0ec), `slurm-396.out` (d1b77e14…6bd2), `smoke_fud_b300.py`, `sbatch_smoke_fud.sh`; sacct 396 COMPLETED, ElapsedRaw 97 s, `gres/gpu=1` |
| O6 | Ledger: started row at 14:37:50Z (job submitted `--hold`, so the row carries the job ID before release), closing row 0.03 GPU-h. FU-D explorers so far: me 0.03, explorer_FU_D_r1_1 0.03. Whole-run total at 15:0xZ = **12.451 GPU-h** of the 95 ceiling. | `results/gpu_ledger_2026-10-31.md` (last rows); summed by a script over the "completed" rows |
| O7 | B300 Slurm. Partitions: gpu (default 4 h, max 2 d), interactive (max 4 h), debug (max 30 min); OverSubscribe=NO; 4 nodes × 8 GPUs, all idle at 14:2xZ. b300-01 = .98 (cloud-S1HDe3); .99/.101/.103 = b300-02/03/04. **sacct prints KST**, so convert to UTC for the ledger. | `sinfo`, `scontrol show partition`, `getent hosts`, `sacct -j 396` |
| O8 | **Data location.** `/scratch` is a node-local md0 RAID (28 T); `/home` is node-local vda1. **Only b300-01** has `/scratch/iitp4` and the raw HCP (`/scratch/data/hcp/download_HCP_REST1_filtered`, 1084 dirs, counted only). b300-02/03/04 have neither. Preprocessed data sit at `/scratch/iitp4/worker_M3_r1/hcp` (manifest.json, 88 subject dirs, 126 G). The original (unsanitized) split is at `/scratch/iitp4/worker_M3_r1/code/split.json`, sha256 **c13b5f21…0262** = card §4. `partitions/perms_hcp.npz` on B300 = repo copy = ec05b796…2b34; `perms_Fplus` and `perms_Fminus` also match. The r1 venv `/scratch/iitp4/worker_M3_r1/venv` has torch 2.15.0+cu134, numpy 2.5.4, scipy 1.18.1. | ssh probes (counts and hashes only) |
| O9 | The repo `results/topic2/2026-11-01/split.json` is the C4-sanitized version (positional `h%02d` tokens). It cannot drive `HCPSource`, because B300 subject dirs are named by the original pseudonyms. As disclosed, `card_sha256.txt` fails only on `hcp_manifest.json` and `split.json`. | `sha256sum -c` output; `scripts/topic2_c4_sanitize.py` lines 1–20 |
| O10 | The frozen `train.run` writes `rec["test_pseudonyms"] = list(te.pseudonyms)` (`src/topic2_rgpool/train.py` line 245), i.e. the original unsalted 16-hex content pseudonyms. Copied back unsanitized, these recreate the r1 B1 C4 blocker. | code read |
| O11 | `scripts/topic2_train.py` defaults to `--cfg E36_d2262` and `--max-run-hours 0.75`, with `--probe-steps 200`. An E192 run (projected about 1.2 h) launched without overriding `--max-run-hours` aborts at step 200 as `aborted_throughput`. Calling `topic2_train.py --cfg E192…` directly gives a KeyError, because the key is not in the frozen CONFIGS. | `scripts/topic2_train.py` lines 22–38; `train.py` lines 196–207 |
| O12 | **The frozen verdict script cannot be reused** (synthetic records, frozen `scripts/topic2_verdict.py`):<br>• A: F+ on seed 0 only, which passes, plus a keep-sized effect → `inconclusive` "measurement-capacity gate failed". A missing seed is reported as a gate failure.<br>• B: F+ s0,s1 pass, F− not run → **`keep`**. A missing F− counts as a pass.<br>• C: gates pass, 4 HCP seeds → `no_verdict`.<br>• D: F+ fails, Stage 1 not run → `no_verdict`, where the card says inconclusive (case A defect). | `verification/explorer_FU_D_r1_2/probe_frozen_verdict_reuse.py` → `.out.json`; `HCP_SEEDS`/`FIX_SEEDS` hard-coded at lines 16–17; `fm is not False` at line 66 |
| O13 | `stats.verdict` itself follows card §8: stop iff hi < δ; keep iff mean ≥ δ, lo > 0 and I2 lo > 0; F− failure downgrades only keep. `stats.gate_fixture` uses ≥ δ for F+ and < δ for F−. `t_interval` needs n ≥ 2. These functions can be imported. The defects are in the orchestration in `topic2_verdict.py` and in untested boundaries (V01–V11, `M3_r2_gate_record.json`). | `src/topic2_rgpool/stats.py` |
| O14 | r1 timing: E36 data load 21.3 s; the step-200 projection of 0.431 h matched the actual wall time of 1572.7 s. r1 per-seed I1 = +0.23, +0.07, +0.40, −0.03, +0.06 %, so the seed sd is about 0.17 % and the t half-width (df 4) about 0.21 %. One S run (S_s2) stalled at the trivial solution (NMSE 1.0000) and was counted as valid. | `results/topic2/2026-11-01/runs/hcp_C_s0/train_log.jsonl`, result report §3.1 |
| O15 | C1 rc 0. `code_sha256_at_freeze.txt` rc 0. `output_sha256_r2.txt` rc 0. My B300 dir `/scratch/iitp4/explorer_FU_D_r1_2` was removed after copy-back; the copied files match the remote sha256 values. No job of mine is in the queue. | commands in §5 |

## 2. Logic chain

1. **Model.** O1–O3: E192 has the same stage-0 grid, octant size and stage count as E36. So the r1 partitions (`perms_hcp.npz` E/C/S_seed0..4; `perms_F*.npz`) stay valid, and ConnectomeRGBoxPooling applies unchanged. Only the channel width of M0 changes (192 → 8·192 = 1536 → 384). Reusing the r1 perms, split, masks and seeds makes model scale the single changed factor relative to r1.
2. **Cost.** O5: about 1.20 GPU-h per run (§7 assumed 1.36 at bs 4). r1's full gate machinery (12 fixture runs) plus 15 Stage-1 runs is 27 × 1.20 = 32.4 GPU-h, over the 25 cap. Even F+ with 2 seeds (6 runs) + 15 + F− on E and C = 23 runs = 27.6 is over. Feasible: F+ on seed 0 (3 runs) + 15 Stage-1 = 18 runs = 21.6 GPU-h, plus 2 conditional F− runs = 24.0 worst case. Margin is about 1 GPU-h after the explorers' 0.06.
3. **F− can be conditional without changing any verdict.** Under card §8 (O13), F− only touches `keep`. Running F− (E and C, seed 0) only when Stage 1 gives a would-be `keep` yields the same verdict in every branch and saves 2.4 GPU-h in the likely stop / inconclusive outcomes. F− is synthetic and its rule is frozen in advance, so running it after Stage 1 adds no analyst freedom. It does change how F− results are reported: in a stop outcome there is no E192 F− number.
4. **One F+ seed is defensible.** The r1 per-seed F+ gains (2.8–3.4 % C vs E, about 2.9 % C vs S) are far above δ, and the seed-to-seed spread is about 0.5 %. This must be disclosed as a deviation from r1's 2-seed gate.
5. **A seed fallback must be pre-registered and cost-only.** Five seeds need about 1.245 GPU-h per run or less (0.1 + 3h + 15h + 2h ≤ 25). If the real per-run cost from the gate runs' sacct comes out higher, 4 seeds (0–3) fit up to about 1.46 (0.1 + 3h + 12h + 2h ≤ 25). Four seeds widen the t half-width by about 1.28× (t3/√4 against t4/√5). With r1's sd (O14) that is 0.27 % against 0.21 %, which barely affects a stop decision, which needs an upper bound below 1 %.
6. **Verdict code.** O12 shows the frozen script mislabels every reduced design: a missing gate becomes a fail or a pass, 4 seeds become no_verdict, and an F+ failure becomes no_verdict. So FU-D needs its own verdict orchestration with tri-state gates. It can import `stats.t_interval`, `relative_gain`, `hierarchical_bootstrap` and `gate_fixture`, and it must be tested on the V01–V11 classes plus the FU-D-specific traps in §4.
7. **Logistics.** O8 shows that HCP runs can only run on b300-01 unless the data are replicated. The F+/F− fixture runs need no HCP, so they can run on b300-02..04 once a venv and the code are present there. O11 shows the defaults abort or crash E192 runs, so the worker needs a wrapper that sets the config and the flags. O9 and O10 show that the original split must come from B300 and that `run.json` must be sanitized before copy-back.
8. **Memory.** 198 GiB peak of 268 GiB (O5) means one HCP-resident E192 job fits per GPU, with about 70 GiB to spare. No gradient checkpointing is needed, so the frozen step stays unchanged.

## 3. Caveats

- The smoke used synthetic data and a dummy HCP tensor. Real data take the same `batch()` path and have the same shapes, so the cost should transfer, but whether training learns, stalls or diverges on real HCP at E192 is untested. The fixture-loss decrease and the finite losses at constant peak lr are only weak evidence against divergence.
- Four other FU smokes shared b300-01 during my measurement. Eight concurrent E192 jobs on one node (CPU-side `simmim_masks` argsort and page-cache reads) could be slower. The step-200 throughput probe in the frozen code is the guard (§4 F3).
- I did not run the topic2 test suite or the mutation harness. I recommend tests; I did not write them.
- Whether the PI-specified "arms E/C/S" permits a conditional F− is a root/PI reading. A conditional S arm (Alternative B in §4) would deviate further and needs explicit approval.
- Replicating HCP across B300 nodes stays on B300 and is not redistribution in my reading, but root must decide it, because other teams share the data.
- The r1 data dir `/scratch/iitp4/worker_M3_r1/hcp` belongs to a finished r1 worker. It is ephemeral: it is lost if the VM stops or someone cleans it up, and so is the raw HCP, which is also on `/scratch`. If it disappears, Topic 2 follow-ups are blocked until preprocessing is redone with the off-repo burned salt.
- The other FU teams' caps (A 8 + B 33 + C 13 + D 25 + E 1.5) plus M2-H2 6 add up to 86.5, while 95 − 12.45 = 82.55 GPU-h remain. **The run ceiling, not FU-D's cap, may bind first.**

## 4. Conclusion — strategy for the FU-D worker (covers F1–F3, C1–C8)

Suggested own paths, disjoint from M3 r3 (`tests/topic2_rgpool`, addendum_06) and from the other FUs; root may rename them:
- card: `docs/03_empirical_analysis/topic2/<date>_topic2_fuD_card.md`
- results: `results/topic2/<date>_fuD/`
- code: `src/topic2_fud/`, `scripts/topic2_fud_*.py`
- tests: `tests/topic2_fud/`
- B300: `/scratch/iitp4/worker_FU_D/`

### F1 — card (frozen and sha-receipted before the F+ gate and any HCP run)

**Single change.** Config `E192_d22182` = {img (96,96,96,20), in_chans 1, embed 192, window (4,4,4,10), patch (6,6,6,1), depths (2,2,18,2), heads (6,12,24,48), c_multiplier 2}, with 474,226,176 parameters. Everything else is r1 §5 verbatim:
- SimMIM mask 0.6, unit 1 cell × 2 frames;
- AdamW lr 2e-4, wd 0.05, warmup 5 %, cosine, clip 1.0, bf16, flash SDP;
- 8,750 steps × batch 16 = 140k samples;
- seeds s / 1000+s / 2000+s; evaluation masks 7001 / 7002; `use_post_norm=False`.

Do not adopt VRABES's mask 0.8 or lr 7e-5: that would be a second factor.

**Inputs reused by sha:**
- split = the B300 original c13b5f21…;
- perms_hcp ec05b796…, perms_Fplus b288a5ad…, perms_Fminus b044266e…;
- data = `/scratch/iitp4/worker_M3_r1/hcp`, with a combined digest pinned before Stage 1 and rechecked after the last run: the sha256 over the per-file sha256 of `bold_z_fp16.npy` and `mask.npy`, in split order. Only the combined digest goes in the repo.

The same 64/8/16 subjects and the same dev-subject exclusion as r1 follow automatically.

**Arms and runs.**
- Gate: F+ E, C, S, seed 0 (3 runs) at full budget, before Stage 1.
- Stage 1: E, C, S × seeds 0..n−1.
- F−: E and C, seed 0, **iff** the Stage-1 primary rule yields keep.

**δ.** 1 % (PI decision 3).

**Metrics and inference.** I1 and I2 as in r1 §6 and §8: t95 over seeds, and the hierarchical bootstrap as secondary.

**Verdict table.** As in r1 §8, with these FU-D rules:
- F+ fail → `inconclusive` (measurement capacity), Stage 1 not run (fixes case A).
- F+ missing after one rerun, or Stage 1 incomplete after one rerun per seed → `no_verdict`.
- F− fail or F− missing → a would-be keep becomes `inconclusive`. F− never changes modify, stop or inconclusive.

**Pre-registered, cost-only seed rule.** Evaluate once, after the gate wave and before any HCP launch.
- Inputs:
  - h\* = max over the 3 gate runs of sacct ElapsedRaw·GPUs/3600;
  - U = FU-D ledger GPU-h so far (explorers + gate + aborts);
  - G = 95 − whole-ledger total.
- n = 5 if U + 15h\* + 2h\* ≤ min(25, U + G). Otherwise n = 4 if U + 12h\* + 2h\* ≤ that bound. Otherwise do not launch Stage 1, and report T2.3-style "not testable within cap", with card, code, gate result and a costed plan.
- Seeds are always 0..n−1. One rerun per failed run only if it fits under the same bound. Otherwise that seed stays missing → `no_verdict` (r1 rule).

**Run-level guards.** `--max-run-hours 1.30` with `--probe-steps 200`: an aborted run counts as a software failure, is rerun once and is ledgered. Inner `timeout 5400`; Slurm `--time=01:45:00`.

**Trivial-solution runs** (any test NMSE ≥ 0.9999) are valid, as in r1. A leave-that-seed-out sensitivity analysis is pre-declared as descriptive only.

**Joint reading with r1 (pre-declared).**
- E192 stop → the r1 kill holds from 38.7 M to 474 M parameters at fixed budget and target.
- E192 keep or modify → the r1 stop is scale-limited.
- inconclusive or no_verdict → no update.

The card should also say up front that r1 and the dev-subject evidence predict stop.

**Alternative B (only with root/PI approval).** Make the S arm conditional on I1 surviving (mean ≥ δ and lo > 0): expected 13 runs ≈ 15.6 GPU-h. This leaves I2 unmeasured in a stop outcome.

### F2 — implementation and tests (own paths; import `src/topic2_rgpool`, never edit it)

**`topic2_fud_train.py` (wrapper).**
- Assert that the key is absent or equal, then insert the E192 dict into `src.topic2_rgpool.model.CONFIGS`.
- Force `--cfg E192_d22182 --max-run-hours 1.30 --save-model`, then call the frozen `scripts/topic2_train.py` `main` / `train.run`.
- Write a sidecar `fud_meta.json` with the wrapper sha, the config dict and the slurm job id. The frozen `code_sha256` covers only `src/topic2_rgpool`.

**Job generator / sbatch script.**
- Stage-1 jobs: `--nodelist=b300-01 --gres=gpu:1 -p gpu --cpus-per-task 8 --mem 64G`, `OMP_NUM_THREADS=4`, `PYTHONDONTWRITEBYTECODE=1`.
- Fixture gate jobs may run on b300-02..04 once `scripts/b300_env/build_env.sh` has built a venv there under `/scratch/iitp4/worker_FU_D/`.
- Submit with `--hold`, write the ledger "started" row with the job id, then `scontrol release`. This is the pattern I used.
- Perm-key map: E→E, C→C, S→S_seed{s}.

**C4 sanitizer, run on B300 before copy-back.**
- Map `test_pseudonyms` to `h%02d` using `token_map` from `scripts/topic2_c4_sanitize.py` (import it, do not copy it), applied to the B300 original manifest. Verify that manifest's sha against card §4 26ba34a9…, by hash only.
- Copy back only the sanitized `run.json`, `train_log.jsonl` and `stdout.log`. Run `scripts/topic2_id_scan.py` on B300 over the FU-D outputs before the handoff.

**`topic2_fud_verdict.py`.**
- Tri-state gates: pass / fail / missing.
- Trap: frozen `stats.gate_fixture` always reads `m["S"]` (`stats.py`, the `g_cs` line), so a 2-arm F− (E and C only) raises KeyError. Implement F− pass = (E−C)/E < δ in FU-D code, and test it against `gate_fixture` on 3-arm inputs. Otherwise run F− S as well, which takes the worst case to 25.2 GPU-h and over the cap.
- Reads the frozen seed plan, `cost_plan.json`, which is written by the seed rule before Stage 1.
- Imports `stats` helpers; writes `verdict.json`.

**Tests in `tests/topic2_fud/`.** Each must fail on its target defect. Pair each with a mutant in a mutation harness that the suite must kill; the baseline must survive.

1. **Verdict boundaries and branches:**
   - V01: hi == δ → not stop.
   - V02: mean == δ → keep or modify eligible.
   - V03: lo == 0 → not keep or modify.
   - V04: I2 lo == 0 → modify.
   - V05: F+ gain == δ → pass; F− gain == δ → fail.
   - V06: F− fail on modify → stays modify.
   - V07: F+ missing → no_verdict, never pass.
   - V08/V10: a run whose status is not "completed" (failed_nonfinite_loss, aborted_throughput) but which carries a `test_nmse` is never used → no_verdict.
   - V09: test-token order mismatch → error.
   - V11: F+ fail with Stage-1 records present → inconclusive.
   - Case A: F+ fail with no Stage 1 → inconclusive.
   - Scenarios A–D of O12, each expecting the correct FU-D label: A inconclusive only if F+ s0 fails, else proceed; B keep only with an F− pass; C a valid 4-seed verdict when the plan says 4; D inconclusive.
2. **Record guards**, to stop r1 or wrong records mixing in:
   - every run must have cfg `E192_d22182`, `n_params` 474,226,176, steps 8750, batch 16, the expected split sha c13b5f21…, and the expected `perm_sha256` per (arm, seed);
   - pointing the FU-D verdict at `results/topic2/2026-11-01/runs` must raise;
   - seeds beyond the plan (e.g. s4 under a 4-seed plan) must raise, so seeds cannot be shopped;
   - two attempts for one (arm, seed) → use the completed one; both failed → missing.
3. **Cost planner:**
   - it is a pure function of (h\*, U, G) with no outcome input;
   - boundary tests at exact equality for 5→4→stop;
   - it refuses when the global ceiling G binds.
4. **Wrapper (CPU, about 25–40 s, 2–4 GB RAM):**
   - registration is idempotent and leaves E36 untouched;
   - n_params 474,226,176;
   - M0 type and shapes as in O2;
   - the C-arm forward differs from E;
   - step-0 weights bit-identical for E, C and S at E192 (as probe P4);
   - a mutant that falls back to E36 or the identity perm must fail.
5. **C4:**
   - the FU-D results tree has no quoted 16-hex token (regex as in `tests/topic2_rgpool/test_c4_tokens_r2.py`);
   - tokens equal the repo `split.json["test"]` and their order is the same across runs;
   - a sanitizer mutant that skips replacement must fail.

**Freeze.** Write `code_sha256_at_freeze.txt` for the FU-D code + tests, plus `card_sha256.txt`, in the results dir before the gate wave.

### F3 — runs, ledger, report

**Sequence:**
1. Optionally your own smoke (≤ 0.25 GPU-h). My O5 numbers can be cited.
2. Card and code freeze.
3. Gate wave: 3 runs, about 3.6 GPU-h, preferably on b300-02..04.
4. Evaluate the seed rule; write `cost_plan.json`, and pin its sha.
5. Stage 1: 15 runs on b300-01, as 2 waves if 8 GPUs are free, about 2.4 h wall; more under contention.
6. Run F− only if the result is a would-be keep.

**Ledger.** One started row and one completed row per job, with node, GPU, Slurm job id, UTC start and end (sacct is in KST), GPU-h from sacct ElapsedRaw × GPUs, purpose and agent id, under flock via `scripts/topic2_ledger.py --agent …`. Before every wave, check the FU-D total ≤ 25 and the whole-ledger total ≤ 95.

**Report.**
- The verdict per the FU-D card, with full intervals at δ = 1 %.
- The comparison with the r1 E36 numbers (cited from `results/topic2/2026-11-01/`), labelled as across-experiment and descriptive.
- Deviations from r1 in a dated FU-D addendum: 1-seed F+, conditional F−, any seed fallback.
- Checkpoints stay on B300 only.

**C1–C8 checklist:**
- C1 and all receipts rc 0 before handoff.
- No git writes.
- No installs on DGX-Spark; the B300 venv goes under `/scratch/iitp4/worker_FU_D`.
- HCP never leaves B300; only aggregates and sanitized records come back.
- No ENIGMA.
- No numbers from `EMPIRICAL_ANALYSIS_REPORT.md`.

**Root-level decisions to raise:**
- (a) Let FU teams share b300-01 fairly, or approve replicating `/scratch/iitp4/worker_M3_r1/hcp` (126 G) to b300-02 for FU-D Stage 1.
- (b) Declare `/scratch/iitp4/worker_M3_r1/{hcp,code/split.json,venv}` read-only and do-not-delete until every FU is done.
- (c) The run ceiling (82.55 GPU-h remaining) is below the sum of the remaining caps (86.5).

## 5. Verification method

```
cd /home/juke/git/00IITP-AI
LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt >/dev/null; echo $?        # 0
sha256sum -c results/topic2/2026-11-01/code_sha256_at_freeze.txt >/dev/null; echo $?                                   # 0
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_D_r1_2/probe_e192_cpu.py       # P1–P5 true, 474226176
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_FU_D_r1_2/probe_frozen_verdict_reuse.py   # A inconclusive, B keep, C no_verdict, D no_verdict
sha256sum verification/explorer_FU_D_r1_2/smoke_fud.json        # bc429d9f42d3c46299ebd01958e305faed37d0ebc35f827b8873e07297c1b0ec
grep explorer_FU_D_r1_2 results/gpu_ledger_2026-10-31.md        # started 14:37:50Z + completed 0.03 (Slurm job 396)
ssh connectome@61.107.201.98 'sacct -j 396 -X --format=JobID,State,ElapsedRaw,AllocTRES -P'   # COMPLETED 97 s gpu=1
ssh connectome@61.107.201.98 'sha256sum /scratch/iitp4/worker_M3_r1/code/split.json /scratch/iitp4/worker_M3_r1/partitions/perms_hcp.npz; ls /scratch/iitp4/worker_M3_r1/hcp/subjects | wc -l'   # c13b5f21…, ec05b796…, 88
for h in .99 .101 .103; do ssh connectome@61.107.201$h 'ls -d /scratch/iitp4; ls /scratch/data/hcp 2>/dev/null | wc -l'; done   # absent, 0
PYTHONDONTWRITEBYTECODE=1 /home/juke/superclaude-env/bin/python3 -B -c "import sys;sys.path.insert(0,'.');from src.topic2_rgpool import stats as S;S.gate_fixture({'E':[0.6],'C':[0.61]},0.01,'Fminus')"   # KeyError 'S' (2-arm F- trap)
```

To re-measure the cost, rerun `sbatch_smoke_fud.sh` with `smoke_fud_b300.py` and the code copy, about 97 s and 0.03 GPU-h, and ledger it.

**Invalidation conditions:**
- any change to `src/topic2_rgpool` (freeze pin);
- a different B300 torch or driver;
- the r1 data dir or the split being missing or changed;
- the measured gate h\* > 1.245 GPU-h (→ 4 seeds) or > 1.46 (→ stop and report).
