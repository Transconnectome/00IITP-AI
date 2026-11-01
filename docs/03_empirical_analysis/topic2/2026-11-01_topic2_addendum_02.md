# Topic 2 card — addendum 02 (2026-11-01, written ~03:56Z, before any Stage-1 test number existed)

The frozen card is `2026-11-01_topic2_card.md` (sha256 `c9bfc60a…41f5`). This addendum records under-specifications found while executing it, and how each is handled. None of them changes a governed decision.

## 1. Stage-0 joint reading: the card names no governing metric

Card §9 says "joint reading of Stage 0 vs Stage 1 (C vs E)" but does not say whether pca2 or r decides "Stage 0 C > E". The Stage-0 run (`results/topic2/2026-11-01/stage0_hcp.json`, computed 03:3xZ after the freeze; descriptive only) gives opposite signs:
- **pca2:** C − E = −0.052 [−0.053, −0.050]. C is lower in 16/16 test subjects.
- **r:** C − E = +0.004 [+0.0005, +0.0074]. C is higher in 11/16.

Handling: the result report gives the joint reading under **both** metrics and chooses neither. The Stage-0 result stays descriptive, as the card requires (Option B). It cannot change the Stage-1 verdict.

## 2. Things the card left implicit and the code fixed at freeze

| item | value used (frozen code) |
|---|---|
| fixture training stream seed | 3000 + s (`train.py`); fixture validation 4 × 32 windows (seed 7001), test 16 × 32 windows (seed 7002) |
| `--save-model` for HCP runs | final weights are saved on B300 only (`/scratch/iitp4/worker_M3_r1/runs/hcp_*/model_final.pt`) for possible later secondary analyses; not copied off B300 and not used by this card |
| wave scheduling | wave 1: 6 F+ runs + 2 F− runs; Stage 1 launched only after all 6 F+ runs completed and the F+ gate was computed (pass, §7.2) |

## 3. Observation before the end of Stage 1, recorded so it cannot be read as post hoc

At the first validation checkpoint (step 2188), the four running HCP runs had val NMSE between 0.994 and 1.000. So, early in training, the models reconstruct under 1 % of the masked in-brain variance of per-voxel z-scored 2 mm BOLD.

The card's δ = 1 % relative NMSE is therefore of the same order as the total variance explained at this budget. The δ and the rules stay as frozen; the full intervals are reported so that the PI can re-read them at any δ.
