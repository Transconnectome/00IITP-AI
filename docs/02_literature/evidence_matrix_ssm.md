# Evidence Matrix: Core Strategy vs. Neuro-GINR Solution

This matrix validates that **Neuro-GINR** is not just an alternative, but the **mathematically superior realization** of the Core Strategy's requirements (RFP).

## 1. Micro-Scale: Continuous Dynamics
| Core Strategy Req | Conventional Approach | **Neuro-GINR Solution** | **Why It Wins (Evidence)** |
| :--- | :--- | :--- | :--- |
| **LTC (Liquid Time Constants)** | ODE-based RNNs (e.g., Liquid Networks) | **GINR (Geometry-Invariant Neural Field)** | **Generality**: LTC is continuous in *Time*. GINR is continuous in **Space & Time**. <br> **Evidence**: `FM4NPP` (2025) shows fields generalize ODEs for irregular grids. |
| **Irregular Sampling** | Interpolation / Imputation | **Continuous Function Query** | **Zero-Shot**: GINR can be queried at *any* coordinate $(x,t)$, handling missing sensors natively without retraining. |

## 2. Macro-Scale: Global Integration
| Core Strategy Req | Conventional Approach | **Neuro-GINR Solution** | **Why It Wins (Evidence)** |
| :--- | :--- | :--- | :--- |
| **GNW (Global Workspace)** | Transformer (Cross-Attention) | **Titans-Mamba (SSM)** | **Scalability**: Transformers are $O(N^2)$ (too slow for 24h). Mamba is **$O(N)$ (Linear)**. <br> **Evidence**: `Mamba-GINR` (2025) proves linear scaling for long-context physiology. |
| **Broadcasting** | All-to-All Attention | **Bayesian Surprisal Gate** | **Efficiency**: Only "Surprising" (High Error) info enters the Global Workspace (Titans memory), mimicking efficient brain ignition. |

## 3. Motivation: Selective Attention
| Core Strategy Req | Conventional Approach | **Neuro-GINR Solution** | **Why It Wins (Evidence)** |
| :--- | :--- | :--- | :--- |
| **Concept-Driven Attention** | Text/Class-based Attention | **Interoceptive Priority** | **Biomimicry**: Attention is driven by **Homeostasis** (Insula). <br> **Evidence**: `IMAC Model` links Interoception to Prediction Error minimization (Cornell et al.). |
| **Alostasis** | Rule-based Logic | **Generative Biofeedback** | **Active Inference**: The model *generates* actions to minimize internal surprisal (maintain safety). |

## 4. Key References (Synthesized)
- **Titans (2024)**: "Learning to Memorize at Test Time" - Basis for the Memory Module.
- **Mamba (2023)**: "Linear-Time Sequence Modeling" - Enabler of 24h GNW.
- **GINR (2025)**: "Geometry-Invariant Neural Representations" - The bridge for Physics-AI.
