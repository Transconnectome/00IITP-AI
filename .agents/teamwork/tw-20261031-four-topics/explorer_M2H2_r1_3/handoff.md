# Handoff (Hard) — explorer_M2H2_r1_3, milestone M2H2 (Topic 3 random-init control H2)
Written 2026-11-01T15:50Z. Lens: adversarial pre-mortem. Recommendation only; no production code written.

**Top line.** H2 is testable within the cap. My own reassembly of the extraction network (SwiFT_v2 fork commit 63367643, ver11 sha 5bc44469…, plus the VRABES snapshot preprocessing) reproduces the stored trained dumps on connectome to rel_fro ≤ 7.8e-7. The local SwiFT_v2 ver11 (sha de132387…) with default flags does not: rel_fro 0.05–0.51. The biggest hazards are four:
1. building the random-init arm from the wrong code;
2. a replication tolerance set at the statistic level, which would accept a misaligned window;
3. no δ, so "differs" is guaranteed;
4. shipping per-subject pooled vectors back through the frozen token job.

## 1. Observation
- **Extraction provenance.**
  - `VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh` ran at NERSC. Its settings are `SWIFT=/pscratch/…/SwiFT_v2_perlmutter`, env `swift_PTL2`, `--model simmim_swin4d_ver11 --depth 2 2 18 2 … --input_scaling_method znorm_minback --seed 1 --precision 32`. It calls `trainer.predict` three times (train, val and test, all 57 subjects).
  - The fork branch is `origin/seungju_perlmutter`. It has no commits between 2026-01-29 (`63367643`) and 2026-10-16, so the committed ver11 at extraction time (2026-08-10) is `5bc44469…`. It is the same at `cd87338e` (the 10-19 HEAD recorded in `/storage/bigdata/EMBARC_new/provenance/git.txt` on connectome).
  - The committed fork `class VRABES` pads with `(23,24,4,4,10,11)`. The snapshot `VRABES/swift_extraction_code/.../datasets.py` uses `(2,3,0,0,2,3)` plus a centre crop, and only that variant reproduces the dumps (below). The snapshot's BaseDataset also carries code "ported … 2026-10-17", after the extraction date.
- **Fork ver11 vs local ver11.** In the fork, each FactorizedSwinTransformerBlock applies the MLP twice (`x = x + mlp(norm2(x))`, then `x = x + ls_mlp(mlp(norm2(x)))`) and sums the 3-axis RoPE angles. Local ver11 makes both behaviours opt-in (`legacy_double_mlp`, `legacy_rope_sum`, default False). Fork init is `self.apply(_init_weights)`: trunc_normal std 0.02 for Linear, bias 0, LN 1/0, LayerScale constants 0.9/0.1/1.0. `use_MuTransfer` defaults to False.
- **Inputs on connectome.** No find/du was used.
  - Input frames: `/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01/img`, 57 subject dirs, 150 frames each. The frame shape is (1,91,109,91,1) after unsqueeze, with `global_stats.pt`. This directory list equals the dump directory list (boolean only).
  - Trained checkpoint (via labfind): `/storage/connectome/jubin/260225_newmodel/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/best.pt`, 7,260,249,428 B, mtime 2026-02-25, readable. A second copy in the stellasybae scratch is listed by labfind but absent.
  - Hardware and software: node1 has 8×A5000 24 GB, driver 550.144. System python is 3.8.10; internet is reachable.
  - `/storage/bigdata/VRABES/06_reprocess_20261018/env` is another project's env and must not be used.
- **Smoke job 218007.** Slurm, node1, 1 GPU, 61 s, 0.017 GPU-h, ledgered (start and close rows). Aggregates are in `verification/explorer_M2H2_r1_3/probe_smoke/returned/code/out/smoke_out.json`. The probe used the peer probe venv `explorer_M2H2_r1_1/venv` read-only: torch 2.4.0+cu121, numpy 1.24.4, monai 1.3.2.
  - **Checkpoint load:** 568 encoder tensors, missing 17 (all decoder; non-decoder missing = []), unexpected 1 (`augment_comp.smooth_kernel`). This matches EXPERIMENT_LOG "missing=17".
  - **A: trained replication** at positions {0, 28} × windows {0, 60}, all 4 layers. max|Δ| ≤ 4.5e-6, rel_fro 6.5e-7–7.8e-7, allclose(1e-5) True everywhere, token covPR/corrPR relative Δ ≤ 2e-8. Forward takes 0.18–0.24 s per window; peak memory 3.45 GB.
  - **B1: scaling 'none'.** rel_fro 1.5–2.1, covPR rel 0.28–0.40. FAILS.
  - **B2: window +1 TR.** rel_fro 6.2e-4 (L3) to 4.6e-3 (L0), so allclose fails. But the statistic-level covPR rel Δ is only 4.8e-6–2.1e-5, and the pooled max|Δ| is 1.7e-5 (L0) to 4.8e-4 (L3).
  - **B3: local ver11, default flags, same weights.** rel_fro 0.050 / 0.29 / 0.42 / 0.51; covPR rel up to 0.15. FAILS.
  - **B4: local ver11 with `legacy_double_mlp=True, legacy_rope_sum=True`.** Numbers identical to the fork.
  - **C: random init on synthetic iid N(0,1) input only**, seeds 1 and 2 under `torch.manual_seed`. Token covPR by layer:
    - L0 (10240×384): 231 vs 251;
    - L1 (1280×768): 363 vs 368;
    - L2 (160×1536): 132 vs 132;
    - L3 (160×1536): 121 vs 122.

    corrPR is stable across the two seeds (251.7 / 251.8 at L0).
  - No random-init forward was run on real frames. The remote probe dir was deleted after copy-back; the local copies are kept.
- **Local synthetic probe.** `verification/explorer_M2H2_r1_3/probe_local/out/fixture_theory.json`, using the frozen estimators. For a random linear map, population PR ≈ d_in·d_out/(d_in+d_out+1) (192×192: theory 95.75, sample 95.56). At 1120×1536 the sample covPR is 454 and at 160×1536 it is 131.5 (ceilings 1119 / 159). A smoothed input collapses PR from 190 to 10.5.
- **Frozen code and guard tests.**
  - `scripts/topic3_token_job.py` returns `pooled__*` arrays (57×D per-subject vectors) in `*_token_spectra.npz`; verified on the pinned primary npz, keys include `pooled`.
  - `scripts/topic3_common.py:12` hard-codes OUT = `results/topic3/2026-10-31` (addendum 02 §2).
  - `tests/topic3_spectral/test_outputs_no_ids.py` fails on the byte string "sub-" in any file under `results/topic3/**` or `docs/03_empirical_analysis/topic3/**`. This already bit worker_M2_r4 (addendum 06 §7).
  - `sha256sum -c` prints Korean "성공" unless LC_ALL=C is set.
  - C1 rc 0. All 7 topic3 receipts are 0-fail under LC_ALL=C.

## 2. Logic chain
1. Fork ver11 plus snapshot preprocessing gives a stored-dump match at about 1e-6, while the local default ver11 misses by 5–51% (A vs B3). So "the model's own init code" must be the fork file 5bc44469…. A random-init arm built from local defaults would be a different network: single MLP, split RoPE. It would also differ from the trained arm in architecture, which silently invalidates H2. B4 shows that local ver11 with the two legacy flags is forward-equivalent for trained weights. The init RNG order may still differ, so the fork file is safer.
2. B2 shows that a +1 TR window error moves the elements by ≥ 6e-4 relative, but moves token PR by only ~1e-5 relative. Any tolerance stated on PR or pooled statistics, such as "within 1%" or even 1e-4, would pass a misaligned pipeline. The replication gate must therefore be element-wise per frame. rel_fro ≤ 1e-5 sits ≥ 13× above the observed error and ≥ 60× below B2. TF32-on (rel ~6e-4 per the public ledger row of explorer_1) would also fail, which is wanted.
3. Token-level CIs in Family B were about ±0.003 in log ratio, with every p at the 2/(B+1) floor (result report §3). Without a pre-stated δ, "trained ≠ random-init" is certain and uninformative. The decision rule needs an equivalence band and a seed-replication rule. Two seeds already differ by 8% in covPR at L0 on iid input (C), so the seed-to-seed spread is not negligible.
4. "Near-isotropic baseline" is false as a fixture expectation. A random linear map gives population PR ≈ D/2, and sample PR is limited by n (C and the local probe). Fixtures must use the closed form or the MP-limited value, not PR ≈ D.
5. The frozen token job ships `pooled__*` per-subject vectors. For the random-init arms these are new per-subject representations. Returning them violates the dispatch rule ("per-subject representations never leave connectome"). Family A on random-init must be computed on connectome, or the npz stripped of `pooled__*` before copy-back.
6. GPU cost is small. One arm is 57×7 forwards at about 0.2 s plus about 29 GB of frame I/O, so a few minutes, about 0.1–0.2 GPU-h. Replication, 3 negative controls on a subset and 5 seeds come to roughly ≤ 1.5 GPU-h, well under the 6 GPU-h cap. Cost is not a reason for "untestable"; only a failed replication gate is.

## 3. Caveats
- Only 4 of 399 frames were replicated. The full 399-frame gate is the worker's job.
- The probe used a minimal harness (direct model forward with the snapshot preprocessing re-typed), not the PTL/deepspeed entrypoint. Equivalence is shown only through the output match.
- torch 2.4.0 on py3.8 is not the NERSC env (py3.12, unknown torch). It matched anyway at about 1e-6.
- Seed semantics in my probe (`torch.manual_seed` just before construction) differ from the pipeline (`pl.seed_everything`, then DataModule, then LitClassifier). Both are draws from the same init law; the addendum must fix one.
- The NERSC checkpoint hash is unknown. Size and mtime agree, and the dump match is the identity evidence.
- I read the public ledger row of explorer_M2H2_r1_1 (required for ledger appends). I did not read the peers' handoffs. Their row agrees with mine (rel_fro ≤ 7.8e-7; local fails; TF32-on about 6e-4).
- The δ values proposed below are mine and need root/PI confirmation, as with PI decision 3.

## 4. Conclusion: recommended worker strategy
**H1′ (freeze addendum_07 before any random-init forward on real frames).** File: `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07.md`, receipt `results/topic3/2026-11-02_h2/addendum_07_sha256.txt`. It must fix the following.
- **(a) Code identity.**
  - Fork ver11 sha 5bc44469… and patchembedding.py c889eebb… are extracted by `git show 63367643:…` into the project, under scripts/ or a new `src/topic3_h2/vendor`, not under `results/topic3`.
  - Preprocessing mirrors snapshot `VRABES.__getitem__` + `scale_input` (znorm_minback): `(y−mean)/std` from `global_stats.pt`; background = first voxel; pad `(2,3,0,0,2,3)`; centre crop of H to 96.
  - Windows start at 0, 20, …, 120 (7 per subject); fp32; `torch.backends.cuda.matmul.allow_tf32 = torch.backends.cudnn.allow_tf32 = False`; eval mode; no state loaded for random-init.
- **(b) Seeds and init.** S = 5 seeds {1,2,3,4,5}, fixed, with no additions after results. Seed s means `torch.manual_seed(s)` on CPU immediately before `Simmim_RoPE4DSwinTransformer(**KW)`, with the extraction CLI values (img 96³×20, embed 192, depths 2-2-18-2, heads 6-12-24-48, patch 6-6-6-1, window 4-4-4-10, c_mult 2, last_layer_full_MSA True, drop 0). Record the sha256 of the encoder parameter bytes per seed and assert it ≠ the trained hash.
- **(c) Replication gate R** (run after the freeze, before any random seed). Reproduce all 57×7 trained frames and all three checks must hold:
  - R1: per frame and layer, rel_fro ≤ 1e-5 AND allclose(atol = rtol = 1e-4).
  - R2: frozen `scripts/topic3_token_job.py --check-npz-root` gives `repool_allclose_all_subjects = True`.
  - R3: per-subject cat_covpr / cat_corrpr for L0, L1, L2, LN0L2, L3 equal the pinned `token_job/E192_primary_token_spectra.npz` at rel ≤ 1e-6.

  Gate PASS is written as a JSON record with hashes. The random-init launcher refuses to run unless the addendum receipt verifies and the gate record says PASS.
- **(d) Endpoints, all with the frozen estimators imported from `src/topic3_spectral`.**
  - **Token level (primary; subject = unit; n = 57).** For v ∈ {L0, L1, L2, LN0L2, L3} × {covPR, corrPR}:

    d_i = log PR_trained,i − mean_s log PR_rand,s,i.

    Test: sign-flip (B = 9999) plus subject bootstrap CI (B = 9999), with Holm over the 10 tests.
  - **Contrast-at-init (bears on R2).** The card's H1a and H1b statistics computed on each random-init arm. The learned component is

    DiD_i = [log corrPR_tr(L3) − log corrPR_tr(LN0L2)] − mean_s[same on random-init],

    with the same test.
  - **Subject level (bears on R1/R2; computed ON CONNECTOME).**
    - D1 on each random-init arm (L2−L3 at m = 28);
    - paired ΔPR_28(trained − random) per layer (same D) via `paired_subsample_delta`;
    - (L2−L1) per arm as the D-matched descriptive for R1.
- **(e) Decision rule with δ.** Proposed δ_level = log 1.10 for trained-vs-random levels and δ_DiD = 0.01 for the H1a/H1b DiD (about half the primary H1a effect). Both need root/PI confirmation.

  | Verdict | Conditions |
  |---|---|
  | **"differs"** | Holm p < 0.05, AND the CI lies wholly outside [−δ, δ], AND ≥ 4/5 seeds individually give the same sign with \|mean\| > δ |
  | **"equivalent"** | CI ⊂ (−δ, δ) |
  | otherwise **"inconclusive"** | — |

  Write the full truth table, including the zero-mean and CI-touching-δ cells, so that no cell is unnamed (the r3 "killed (primary CI includes 0)" lesson).
- **(f) Pre-registered consequence map.**
  - **R2 subject-level drop:** "architectural, present at init" if D1 is robust in ≥ 4/5 seeds and the DiD CI includes 0; otherwise "learned".
  - **R2 token H1a:** the same rule with δ_DiD.
  - **R1:** descriptive, D-matched.
  - **R3:** not addressed (no random-init of BrainLM / BrainJEPA / NeuroSTORM), so the attribution stays untestable.
  - Map all labels to G8 keep / stop / inconclusive as in addendum 03 §6.
- **(g) Exposure list.** Explorer smokes: trained replication values; random-init on synthetic only. None on real frames.
- **(h) Erratum to provenance §2.** Ver11 was cited from local de132387; the extraction code is fork 5bc44469 (double MLP, summed RoPE). The structural claims (no merge between layer_2 and layer_3; final LN) are unchanged.

**H2′ (connectome).**
- Build a project-local venv under node1 home `~/iitp4_m2h2/worker_*`, using the recipe py3.8 + torch 2.4.0 cu121 + numpy 1.24.4 + einops 0.8.0 + monai 1.3.2 (proven to reproduce). Keep the recipe in the repo.
- Homes are node-local: run the GPU forward and the numpy summaries in the same node1 job.
- Run the replication gate first. Then 3 negative controls on 3 subjects × 7 windows (scaling none, +1 TR, local default ver11); each must FAIL R1, and is recorded.
- Then the 5 seeds, one arm per job, with ledger start/close rows.
- Dumps go to a 0700 node1 dir and are deleted after the summaries. Only statistics come back: positions, no `pooled__*`. Strip the pooled keys on connectome before copy-back.

**H3′ (tests; synthetic and never skipping).**
1. A random linear map gives PR within MC error of d_in·d_out/(d_in+d_out+1) (pop) and of the sample value at n = 160 / 1120.
2. A harness-preprocessing vs snapshot-class equality test on synthetic subject dirs (CPU), which fails on pad (23,24,…) and on scaling none.
3. A replication-gate function that fails on a +1 TR synthetic shift and passes at 1e-6 noise.
4. Verdict-function truth-table tests, plus mutants of the new verdict code: bounds swapped, ≥ vs >, raw vs Holm, seed-count off-by-one, label-by-order, δ sign.
5. An output-schema test: no `pooled`/`ids` keys and no "sub-" bytes in `results/topic3/2026-11-02_h2/**`.
6. A test that `results/topic3/2026-10-31` stays byte-identical (output_sha256 rc 0 under LC_ALL=C).

The result report goes in `docs/03_empirical_analysis/topic3/2026-11-02_topic3_h2_result_report.md`.

**Fallback.** If gate R fails on any frame after the pre-stated retries (env pin, TF32 off), H2 = untestable, with the failing frames counted (positions only). No random-init run and no approximate substitute.

## 5. Verification method
- Re-read `verification/explorer_M2H2_r1_3/probe_smoke/returned/code/out/smoke_out.json` and the sacct record of job 218007 (`sacct -j 218007 -X -o JobID,State,ElapsedRaw,Start,End`; times print in KST).
- Ledger: two rows by explorer_M2H2_r1_3 in `results/gpu_ledger_2026-10-31.md` (start 15:19:13Z; close 0.017 GPU-h).
- Rerun the local probe:

  ```
  cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 nice /home/juke/superclaude-env/bin/python3 -B verification/explorer_M2H2_r1_3/probe_local/probe_fixture_theory.py
  ```
- Code identity:

  ```
  git -C /home/juke/git/SwiFT_v2 show 63367643:project/module/models/simmim_swin4d_transformer_ver11.py | sha256sum   # expect 5bc44469…
  sha256sum /home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py   # expect de132387…
  ```
- Integrity:

  ```
  cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt
  ```

  The same applies to each `results/topic3/2026-10-31/*_sha256.txt`.
- Layout lint (`audit_layout.py` on the run root) gave 382 files, 0 findings, rc 0 at about 15:45Z.
- **Invalidation conditions.**
  - The full-cohort replication shows any frame with rel_fro > 1e-5 under TF32 off.
  - The fork branch history shows a commit to ver11 between 2026-01-29 and 2026-08-10. This was checked: none on origin/seungju_perlmutter.
  - Evidence appears that the stored dumps came from a different split pass with different content.
