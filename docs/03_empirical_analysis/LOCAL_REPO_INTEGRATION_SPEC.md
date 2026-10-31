# Local Repository Codebase & Data Structure Integration Specification
**Comprehensive Architectural Contracts across ENIGMA-OCD, SwiFT, Spectral Structure, and Neuromorphic ReSU Systems**

- **Document Version**: 1.0.0 (Release Definitive)
- **Date**: 2026-10-30
- **Target Repository**: `/home/juke/git/00IITP-AI`
- **Output Location**: `docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md`
- **Lead Author & System Architect**: Worker M2 (Chavis Teamwork Suite)
- **Collaborating Lab Researchers**: 배상윤 선생님, 한동엽 선생님, 왕희환 선생님, 이아현 선생님, 최주빈 선생님
- **Audited External Repositories (Strict Read-Only)**:
  1. `/home/juke/git/enigma_ocd_mbbn` (ENIGMA-OCD Multi-Band Brain Network)
  2. `/home/juke/git/SwiFT_v2`, `/home/juke/git/SwiFT-LLM`, `/home/juke/git/SwiFT-LLM-isotok`, `/home/juke/git/VRABES` (SwiFT Family & VRABES Clinical Pipeline)
  3. `/home/juke/git/paper-review/bae_spectral_arxiv_v1_20261020`, `/home/juke/git/paper-review/iclr2027_structure_transfer_39525` (Spectral Graph Theory & Structure Transfer)
  4. `/home/juke/git/00IITP-AI`, `/home/juke/git/DIVER`, `/home/juke/git/ephys-foundation-model-plan`, `/home/juke/git/neurox-discovery-bench/sources/screening/choe2026-celegans-connectome-gapjunction.json` (C. elegans Connectome, Neuromorphic ReSU & Ephys Foundation Models)

---

## 1. Executive Architecture Overview

This specification establishes the software contracts, tensor dimension signatures, exact file mappings, and data flow pipelines required to integrate multi-scale complex network renormalization (Song et al., *Nature* 2005, *Nature Physics* 2006), directed network motifs (Milo et al., *Science* 2002, 2004), spectral representation concentration bounds (배상윤 선생님 et al., arXiv:2610.09709, ICLR 2027), and backprop-free biological similarity matching (Chklovskii et al., AAAI 2026; Pehlevan & Chklovskii, NeurIPS 2015; Buzsáki 2019) into the `00IITP-AI` research suite.

Every specification contained herein has been extracted and verified through direct, read-only static analysis and runtime trace validation across the local codebases. External repositories remain strictly unmodified.

```
+----------------------------------------------------------------------------------------------------+
|                                    00IITP-AI CORE PIPELINE                                         |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [Topic 1: ENIGMA-OCD MBBN]                     [Topic 2: SwiFT Family & VRABES]                   |
|  Schaefer-304 BOLD (T=464)                      4D fMRI Volume (B, C, 96, 96, 96, 20)              |
|  4-Band VMD Decomposition                       PartialVolumeStem3D (4096 spatial patches)         |
|  vmd_cache_4ch_464_head.mmap                    AnatomicalEigenTokenizer4D (Schaefer-400 MBSD)     |
|          |                                                      |                                  |
|          v                                                      v                                  |
|  Directed Lag Flow Graph                        Connectome Box-Covering RG (Song 2005)             |
|  Milo Triad SP (FFL vs 3-Cycle)                 Dual Graph Coloring + Fiedler Spectral Ordering    |
|  CSTC Feedback Loop Biomarker                   Variance-Preserving Supernode Pooling              |
|          |                                                      |                                  |
|          +--------------------------+---------------------------+                                  |
|                                     |                                                              |
|                                     v                                                              |
|                     [Topic 3: Spectral RG Flow Diagnostics]                                        |
|                     Bae et al. Representation Participation Ratio (PR)                             |
|                     Power-Law Exponent (alpha), Box Dimension (dB), Hub Repulsion (R_hub)          |
|                     OOD Generalization Error Bound & Critical Layer Screening                      |
|                                     |                                                              |
|                                     v                                                              |
|                     [Topic 4: Neuromorphic ReSU & Ephys Stream]                                    |
|                     C. elegans Stage-Specific Gap Junction / Chemical Mask                         |
|                     Multiscale Coherent FFL Delay Bank (tau_1 .. tau_4)                             |
|                     RK4 Fast Recurrent Membrane Relaxation (y* = (I + M)^{-1} W p)                 |
|                     Slow Local Oja + Anti-Hebbian Plasticity (Zero Backpropagation)                |
|                     Hierarchical Streaming for DIVER 32-ch iEEG / fMRI                             |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Topic 1: ENIGMA-OCD MBBN Architecture & Biomarker Specifications

### 2.1 Repository Directory Structure & File Map
The repository `/home/juke/git/enigma_ocd_mbbn` implements a Multi-Band Brain Network (MBBN) Transformer for obsessive-compulsive disorder classification from resting-state fMRI:

```
/home/juke/git/enigma_ocd_mbbn/
├── CLAUDE.md                                    # Operational conventions, verified paths, and architecture summary
├── README.md                                    # Benchmark scripts and model execution commands
├── model.py                                     # Transformer_Block, Spatial Attention, MBBN backbones
├── trainer.py                                   # Training loop, cross-validation, optimizer stepping
├── main.py                                      # CLI execution entry point, seed loops
├── losses.py                                    # Cross-Entropy, BCE, and Cross-IMF Contrastive Loss (IC Loss)
├── metrics.py                                   # Balanced Accuracy (BAC), AUROC, sensitivity, specificity
├── communicability.py                           # UK Biobank communicability matrix calculation & ROI ranking
├── time_series_utils.py                         # Variational Mode Decomposition (VMD), bandpass Butterworth filters
├── uncertainty.py                               # Epistemic and aleatoric uncertainty estimation
├── verify_remediation.py                        # Numerical verification and test harness
├── config/
│   └── cross_imf_config.yaml                    # Hyperparameter definitions (intermediate_vec: 304, lr, etc.)
├── data/
│   ├── MBBN_data_304_ROIs_0.25/                 # Preprocessed fMRI timeseries (.npy per subject)
│   ├── metadata/
│   │   └── ENIGMA_QC_final_subject_list.csv     # Subject metadata (Subject ID, Site, OCD diagnosis, Age, Sex)
│   ├── communicability/                         # UKB_imf{1-4}_comm_ROI_order_304.npy
│   ├── vmd_cache_4ch_464_head.mmap              # Fast binary memory-mapped cache (N=1664, 5, 464, 304)
│   └── vmd_cache_4ch_464_head.mmap.subjects.txt # Exact subject ID ordering for memory-mapped cache
├── data_preprocess_and_load/
│   ├── dataloaders.py                           # PyTorch DataLoader wrappers, stratified K-fold splits
│   └── datasets.py                              # ENIGMA_OCD_fMRI_timeseries dataset definitions
└── references/review/                           # 49 NLM queries & 123 reference sources on OCD pathophysiology
```

### 2.2 Cohort Demographics, Preprocessing Pipeline & Storage Contracts
- **Cohort Composition**: $N = 1,706$ subjects passing quality control (833 diagnosed OCD patients, 873 Healthy Controls) acquired across 30 international scanning sites (including Amsterdam-VUmc, Barcelona-Bellvitge, Braga-UMinho, Cape Town, Seoul National University Hospital).
- **Exact Data Storage Paths**:
  - Raw ROI Timeseries: `/home/juke/git/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25/<sub_id>/<sub_id>.npy`
  - Subject Demographics Table: `/home/juke/git/enigma_ocd_mbbn/data/metadata/ENIGMA_QC_final_subject_list.csv`
  - Memory-Mapped Tensor File: `/home/juke/git/enigma_ocd_mbbn/data/vmd_cache_4ch_464_head.mmap`
- **Atlas Parcellation**: Schaefer 304 parcellation scheme (300 cortical parcels across 7 functional resting-state networks + 4 bilateral subcortical regions: bilateral striatum/caudate/putamen, globus pallidus, thalamus, and amygdala-hippocampus complex).
- **Temporal Alignment Contract**:
  - Target sequence length: $T = 464$ timepoints.
  - Scanner equilibrium trimming: Scans discard the initial 20 dummy TRs: $y_{\text{trimmed}} = y[20:]$.
  - Padding and Masking: If valid scan length $T_{\text{valid}} < 464$, arrays are zero-padded to 464 timepoints. A binary attention mask of shape `(464, 304)` is generated where $\text{mask}[t, :] = 1.0$ for $t < T_{\text{valid}}$ and $0.0$ otherwise.
- **Variational Mode Decomposition (VMD) & Frequency Band Splitting**:
  - Conducted using `sktime.libs.vmdpy.VMD` or Butterworth bandpass filter bank in `time_series_utils.py:bandpass_filter_2d`.
  - Splits the broad-band BOLD signal into 4 discrete intrinsic frequency bands:
    - `IMF 1` (High-frequency cortical noise & fast dynamics): $0.12 - 0.25\text{ Hz}$
    - `IMF 2` (Standard neural BOLD fluctuations): $0.06 - 0.12\text{ Hz}$
    - `IMF 3` (Low-frequency functional connectivity band): $0.03 - 0.06\text{ Hz}$
    - `IMF 4` (Very low frequency baseline drift & global state transitions): $0.01 - 0.03\text{ Hz}$
  - Memory-mapped tensor cache structure (`vmd_cache_4ch_464_head.mmap`):
    - Shape: `(1664, 5, 464, 304)`, dtype: `float32`.
    - Dimension 1 indexes: Channel 0 = Raw broad-band BOLD, Channels 1..4 = `IMF 1` through `IMF 4`.

### 2.3 Model Architecture & Exact Tensor Dimensions

```
Input IMFs (B, 464, 304) x 4 Channels
     |
     v
[Temporal Transformer_Block] (Shared BertModel, hidden_size=304, heads=8, layers=4)
     |
     +---> sequence_output: (B, 464, 304)
     +---> out_cls_imf_k:   (B, 304)
     |
     v
[Transposition & Spatial Attention]
     |  Input: sequence_output.permute(0, 2, 1) -> (B, 304, 464)
     |  Module: Attention(dim=464, heads=8)
     |  Spatial Functional Connectivity Map: (B, 8, 304, 304)
     |
     v
[Multi-Head Classification & Projection Heads]
     |  Projection Head: Linear(304, 304) -> ReLU -> Linear(304, 128) -> (B, 128) [Contrastive Loss]
     |  Classifier Head: Dropout(0.3) -> Linear(304, 1) -> pred_imf_k: (B, 1)
     |
     v
Final Ensembled Diagnostic Probability:
y_hat = 0.25 * sum(pred_imf_k, k=1..4) -> (B, 1)
```

- **Backbone Class**: `Transformer_Block` (`model.py:231-284`)
  - Subclasses HuggingFace `BertPreTrainedModel`.
  - Configuration: `BertConfig(hidden_size=intermediate_vec=304, vocab_size=1, num_hidden_layers=4, num_attention_heads=8, max_position_embeddings=465)`.
  - Learnable CLS token: `cls_embedding` parameter initialized with shape `(1, 1, 304)` and prepended to the input sequence.
  - Input: Tensor of shape `(B, 464, 304)` + attention mask `(B, 464, 304)`.
  - Forward output: Dictionary containing `'sequence': (B, 464, 304)` and `'cls': (B, 304)`.
- **Full Finetuning Network**: `Transformer_Finetune_Four_Channels` (`model.py:459-577`)
  - Inputs: 4 individual IMF tensors `x_1, x_2, x_3, x_4`, each of shape `(B, 464, 304)`, accompanied by masks `(B, 464, 304)`.
  - Spatial Attention Modules: 4 independent spatial multi-head attention blocks `Attention(dim=464, num_heads=kwargs.get('num_heads', 8))` (`model.py:477-480`).
  - Spatial Attention Forward: Applied to `x_k.permute(0, 2, 1)` (shape `(B, 304, 464)`). The computed spatial attention matrix represents the dynamic functional connectivity graph with tensor dimensions `(B, num_heads=8, 304, 304)`.
  - Contrastive Projection: Each pooled CLS token `out_cls_imf{1..4}` (`(B, 304)`) is projected through `Linear(304, 304) -> ReLU -> Linear(304, 128)` into a 128-dimensional hypersphere embedding for Inter-IMF Contrastive (IC) Loss computation (`losses.py:cross_imf_contrastive_loss`).
  - Readout & Ensembling: Each channel feeds an independent classification head `Classifier` (`model.py:112`) consisting of `Dropout(0.3) -> Linear(304, 1)` producing logit `pred_imf{1..4}` (`(B, 1)`). Final logit is averaged:
    $$\hat{y} = \frac{1}{4} \sum_{k=1}^4 \text{pred\_imf}_k \in \mathbb{R}^{B \times 1}$$

### 2.4 CSTC Circuit Failure vs Consortium Evidence & Directed Motif Formulation
- **The Classical Cortico-Striato-Thalamo-Cortical (CSTC) Paradigm**:
  Historically, OCD pathophysiology was conceptualized as a localized hyperactivity within parallel frontal-subcortical loops:
  $$\text{OFC / ACC (Cortex)} \xrightarrow{\text{Glutamate}} \text{Caudate / Putamen (Striatum)} \xrightarrow{\text{GABA}} \text{GPi / SNr} \xrightarrow{\text{GABA}} \text{Thalamus} \xrightarrow{\text{Glutamate}} \text{Cortex}$$
- **Consortium Mega-Analysis Findings (`references/review/README.md:200`)**:
  - Worldwide ENIGMA-OCD working group studies (Boedhoe et al., 2017/2018; van den Heuvel et al., 2020; Perera et al., 2024 meta-analysis across 166 fMRI studies) demonstrate that Pearson correlation-based functional connectivity fails to isolate CSTC deficits from whole-brain network shifts.
  - Alterations are distributed across the Default Mode Network (DMN), Salience Network (SN), Frontoparietal Control Network (FPN), sensorimotor cortex, and cerebellum.
  - **Fundamental Artifact of Pearson Correlation**: Zero-lag correlation matrices $C_{ij} = \text{Corr}(x_i(t), x_j(t))$ enforce transitivity ($C_{ik} \ge C_{ij} C_{jk} - \sqrt{\dots}$), artificially creating spurious high-density rich clubs ($R_{\text{hub}} > 4.2$) and degree assortativity ($r > +0.20$), which completely mask subtle feedback loops ($|d| < 0.06$).
- **Milo Directed Lag Flow & Motif Solution (00IITP-AI Integration Contract)**:
  - Construct the asymmetric time-lagged cross-correlation matrix at lag $\Delta t = 1 \text{ TR}$ ($TR \approx 2.0\text{s}$):
    $$C_{ij}(\Delta t) = \frac{\langle (x_i(t) - \bar{x}_i)(x_j(t + \Delta t) - \bar{x}_j) \rangle}{\sigma_i \sigma_j}$$
  - Define the net directed temporal flow graph:
    $$A_{ij} = \max\left(0, \; C_{ij}(\Delta t) - C_{ji}(\Delta t) - \theta_{\text{thresh}}\right)$$
  - Enumerate 3-node directed subgraphs according to Milo et al. (2002, 2004):
    - **Feedforward Loop (FFL, Triad 38)**: $u \to v$, $v \to w$, $u \to w$ (coherent feedforward integration).
    - **Directed 3-Cycle (Feedback Loop, Triad 98)**: $u \to v$, $v \to w$, $w \to u$ (recurrent reverberation).
  - Compute the 13-dimensional Triad Significance Profile ($\vec{SP}$):
    $$Z_i = \frac{N_{\text{real}, i} - \langle N_{\text{rand}, i} \rangle}{\sigma_{\text{rand}, i}}, \quad SP_i = \frac{Z_i}{\sqrt{\sum_{k=1}^{13} Z_k^2}}$$
  - **Empirical Clinical Finding**: As verified in `00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md` (Table 1), healthy controls exhibit dominant forward FFL flow ($392.23 \pm 58.00$), whereas OCD patients exhibit a statistically significant $29.8\%$ surge in recurrent 3-cycle feedback loops ($26.13 \to 33.93$, Cohen's $d = +0.354$), reflecting clinical cognitive and motor reverberation.

### 2.5 Software Interface Specification for `00IITP-AI/src/mbbn_connectome_biomarker.py`
```python
"""
Interface Contract: MBBNConnectomeBiomarkerExtractor
Location: 00IITP-AI/src/mbbn_connectome_biomarker.py
Integrates: /home/juke/git/enigma_ocd_mbbn
"""
import torch
import numpy as np
from typing import Dict, Tuple, Optional

class MBBNConnectomeBiomarkerExtractor:
    def __init__(
        self,
        n_rois: int = 304,
        seq_len: int = 464,
        lag_tr: int = 1,
        sparsity_density: float = 0.15,
        device: str = "cpu"
    ) -> None:
        """
        Input:
            n_rois: Number of Schaefer parcels (default 304).
            seq_len: Timepoints (default 464).
            lag_tr: Time lag for asymmetric directed flow (default 1).
            sparsity_density: Density cutoff for network motif evaluation (default 0.15).
        """
        ...

    def extract_directed_flow_graph(
        self, 
        bold_timeseries: torch.Tensor, 
        mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Converts BOLD timeseries into net directed temporal flow adjacency matrix.
        Input:
            bold_timeseries: (B, T=464, K=304) or (B, Channels=4, T=464, K=304)
            mask: (B, T=464, K=304)
        Output:
            flow_adjacency: (B, K=304, K=304) or (B, Channels=4, K=304, K=304)
        """
        ...

    def compute_triad_significance_profile(
        self, 
        flow_adjacency: torch.Tensor, 
        n_randomizations: int = 100
    ) -> Dict[str, torch.Tensor]:
        """
        Calculates Milo Triad 38 (FFL), Triad 98 (3-Cycle), and full 13-dim SP vector.
        Output:
            {
                'ffl_triad38_count': torch.Tensor of shape (B,),
                'cycle3_triad98_count': torch.Tensor of shape (B,),
                'ffl_to_cycle_ratio': torch.Tensor of shape (B,),
                'sp_vector_13dim': torch.Tensor of shape (B, 13)
            }
        """
        ...
```

---

## 3. Topic 2: SwiFT Family & VRABES Architecture & Patch Merging Specifications

### 3.1 Codebase Hierarchy, Evolution & Multi-Version Registry
The SwiFT family establishes 4D Swin Transformer foundation models for volumetric fMRI across:
- `/home/juke/git/SwiFT_v2`: Core foundation model repository (Swin4D versions 7 through 12).
- `/home/juke/git/SwiFT-LLM` & `/home/juke/git/SwiFT-LLM-isotok`: Neuroanatomical parcellation tokenization (MBSD-Token) and multimodal language bridge.
- `/home/juke/git/VRABES`: Clinical transfer learning pipeline (HCP $\to$ UK Biobank $\to$ VRABES panic disorder treatment response).

Model version evolutions registered in `project/module/models/load_model.py`:
- `swin4d_ver7`: Baseline SwinTransformer4D with factorized 3D spatial + 1D temporal windows.
- `swin4d_ver8`, `ver9`, `ver10`: Multi-node Distributed Data Parallel (DDP) and $\mu\text{P}$ (MuTransfer) scaling adaptations implemented by 최주빈 선생님 (`jubin`).
- `swin4d_ver11`: Rotary Position Embeddings (RoPE-4D) by 왕희환 선생님 (`heehwan`).
- `swin4d_ver12` (`SwiFTv25Transformer`): Component 1 Partial Volume Stem, Component 2 Asymmetric Temporal Patch Merging, and Bidirectional Temporal Mamba-2.

### 3.2 Volumetric Tensor Shapes & Asymmetric Patch Merging Mechanics
- **Canonical Input Tensor**:
  $$(B, C=1 \text{ or } 2, D=96, H=96, W=96, T=20)$$
  where $B$ is batch size, $C$ represents signal channels (Channel 0: normalized BOLD intensity, Channel 1: binary intracranial brain mask), $D=H=W=96$ voxels sampled at $2.0\text{mm}$ isotropic MNI space, and $T=20$ consecutive TRs ($40\text{s}$ functional window).
- **Partial Volume Stem 3D** (`swin4d_transformer_ver12.py:105-156`):
  - Spatial patch partition: $(s_T=1, s_D=6, s_H=6, s_W=6)$.
  - Voxel volume per patch: $1 \times 6 \times 6 \times 6 = 216$ voxels.
  - Spatial patch resolution:
    $$D' = \frac{96}{6} = 16, \quad H' = \frac{96}{6} = 16, \quad W' = \frac{96}{6} = 16 \implies 16 \times 16 \times 16 = 4,096 \text{ spatial tokens per timepoint.}$$
  - Linear projection layer: `nn.Linear(216 * C, embed_dim=96)` yielding initial representation tensor:
    $$(B, T=20, D=16, H=16, W=16, C=96)$$
- **Asymmetric Temporal Patch Merging** (`swin4d_transformer_ver12.py:529-578`):
  Standard 4D Swin transformers suffer from temporal over-compression if temporal resolution is halved at every spatial merging step. SwiFT v2.5 introduces asymmetric schedules:
  - **Stage 1 $\to$ Stage 2 Transition (`merge_time=True`)**:
    - Input: $(B, T=20, D=16, H=16, W=16, C=96)$
    - Slicing: Merges $2 \times 2 \times 2$ spatial patches and $2\times$ temporal frames ($2 \times 8 = 16$ interleaved sub-grids).
    - Concatenated dimension: $16 \times 96 = 1,536$.
    - Linear projection: `nn.Linear(1536, 192, bias=False)`.
    - Output: $(B, T=10, D=8, H=8, W=8, C=192)$.
  - **Stage 2 $\to$ Stage 3 Transition (`merge_time=True`)**:
    - Input: $(B, T=10, D=8, H=8, W=8, C=192)$
    - Concatenated dimension: $16 \times 192 = 3,072 \to \text{Linear}(3072, 384)$.
    - Output: $(B, T=5, D=4, H=4, W=4, C=384)$.
  - **Stage 3 $\to$ Stage 4 Transition (`merge_time=False`)**:
    - Input: $(B, T=5, D=4, H=4, W=4, C=384)$
    - Slicing: Merges spatial grid $2 \times 2 \times 2 = 8$ only. Temporal dimension $T=5$ is strictly preserved.
    - Concatenated dimension: $8 \times 384 = 3,072 \to \text{Linear}(3072, 768)$.
    - Output: $(B, T=5, D=2, H=2, W=2, C=768)$.

### 3.3 Neuroanatomical 4D Tokenization Modules (`SwiFT-LLM`)
In `/home/juke/git/SwiFT-LLM/project/module/models/anatomical_4d_patch.py`, rigid cubic voxel grids are replaced with biologically grounded parcellations:
- **`AnatomicalEigenTokenizer4D` (Paradigm B, MBSD-Token, lines 572-748)**:
  - Resolves Schaefer-400 (or Schaefer-450) atlas labels in $96 \times 96 \times 96$ MNI space.
  - For each anatomical parcel $k \in \{1 \dots K\}$, extracts spatial coordinates $r_i = (x_i, y_i, z_i)$ of all member voxels ($i \in \{1 \dots N_k\}$).
  - Constructs an orthonormal spatial polynomial basis in $\mathbb{R}^{N_k \times M}$:
    - Mode 0 (Spatial Mean): $\phi_0(r) = 1 / \sqrt{N_k}$
    - Modes 1..3 (Dipole Linear Gradients): $\phi_1, \phi_2, \phi_3$ computed along the principal axes $(u_1, u_2, u_3)$ of the parcel's spatial coordinate covariance matrix via SVD.
    - Modes 4..9 (Quadrupoles): $\phi_m(r)$ spanning quadratic terms $(u_1^2, u_2^2, u_3^2, u_1 u_2, u_2 u_3, u_1 u_3)$, strictly orthonormalized via Modified Gram-Schmidt in `float64` precision.
  - **Sparse CSR Matrix Multiplication Contract**:
    - Compiles all basis functions across all $K=400$ parcels into a single giant sparse Compressed Sparse Row (CSR) matrix:
      $$P_{\text{csr}} \in \mathbb{R}^{(K \cdot M) \times V_{\text{valid}}}$$
    - Forward execution calls `deterministic_csr_mm`:
      $$\text{Coeffs} = P_{\text{csr}} \cdot X_{\text{voxels}} \in \mathbb{R}^{B \times T \times C \times K=400 \times M=4..10}$$
    - Linear projection `forward_from_eigen_coeffs`:
      $$(B, T, K=400, M \cdot C) \xrightarrow{\text{Linear}} (B, T, K=400, \text{embed\_dim}=96)$$
- **`AnatomicalHybridAdapter` (Paradigm A, lines 180-320)**:
  - Preserves compatibility with cubic-patch pretrained weights.
  - Computes spatial patch-to-parcel volume overlap profile $V_p(k) \in [0, 1]$ of size $(n_{\text{spatial\_patches}}=4096, K=400)$.
  - Injects anatomical embeddings via a ReZero gate:
    $$z_{\text{out}} = z_{\text{base}} + \tanh(\alpha) \cdot e_{\text{anat}}$$
    with scalar parameter $\alpha$ initialized to $0.0$, guaranteeing bitwise identity to vanilla checkpoints at step 0.

### 3.4 VRABES Clinical Transfer Learning Pipeline (`VRABES/TransferLearning/`)
- **Clinical Cohorts & Staged Transfer Workflow**:
  - **Pretrained Source Model**: SwiFT 51M (`embed_dim=96`, weights trained on Human Connectome Project $N=1,200$ young adults by 최주빈 선생님 at `/pscratch/sd/j/jubchoi/.../best.pt`).
  - **Intermediate Domain Transfer (Stage 1)**: UK Biobank ($N=351$, antidepressant stability proxy label; responders $n=254$, non-responders $n=97$; cohort curation and phenotype harmonization by 왕희환 선생님 `heehwan`).
  - **Target Clinical Transfer (Stage 2)**: VRABES clinical trial ($N=25$ panic disorder patients receiving standardized 12-week cognitive behavioral and pharmacological treatment; evaluated via Leave-One-Out Cross-Validation (LOOCV) to predict Panic Disorder Severity Scale (PDSS) remission).
- **Atlas Cross-Mapping Contract (`compute_roi_correspondence.py`)**:
  - Provides coordinate overlap and transformation matrices across Schaefer-400, Brainnetome (246 ROIs), and Automated Anatomical Labeling (AAL, 116 ROIs) to allow direct cross-study validation.

### 3.5 Failure of Euclidean PatchMerging & Connectome Box-Covering RG Pooling Formulation
- **The Physical Failure Mechanism**:
  As empirically documented in `00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md` (Table 2 & 3), SwiFT's Euclidean `PatchMerging` enforces arbitrary $2 \times 2 \times 2$ spatial box averaging across non-communicating sulcal boundaries. This causes severe signal cancellation, collapsing the effective participation ratio from $PR = 11.02$ down to $3.58$ and driving degree assortativity into positive rich-club congestion ($r = +0.343$).
- **Connectome Box-Covering RG Algorithm (Song et al., *Nature* 2005)**:
  1. Define structural adjacency $A \in \mathbb{R}^{K \times K}$ (e.g. $K=400$ Schaefer parcels) from structural DTI tractography or UK Biobank functional communicability.
  2. Compute shortest-path topological distance matrix $d_G(u, v)$ for all pairs $(u, v)$.
  3. For a target box diameter $\ell_B \in \{2, 3, 4\}$, construct the dual graph $G_{\text{dual}} = (V, E_{\text{dual}})$:
     $$E_{\text{dual}} = \{(u, v) \mid d_G(u, v) \ge \ell_B\}$$
  4. Perform greedy graph coloring on $G_{\text{dual}}$ (`strategy='largest_first'`). Nodes assigned the same color in $G_{\text{dual}}$ are guaranteed to have topological distance $d_G(u, v) < \ell_B$ in $G$, forming an exact box cover $\{B_1, B_2, \dots, B_{N_B}\}$.
  5. Sort resulting supernode boxes along the Fiedler vector $v_2(L_{\text{sym}})$ of the normalized graph Laplacian $L_{\text{sym}} = I - D^{-1/2} A D^{-1/2}$ to preserve continuous 1D positional continuity for Transformer self-attention.
  6. Supernode token pooling operator:
     $$Z^{(l+1)}_b = \frac{1}{|B_b|} \sum_{u \in B_b} Z^{(l)}_u \in \mathbb{R}^{B \times T \times N_B \times 2C}$$
  7. **Measured Advantage**: Delivers $+32.6\%$ reduction in spectral power-law distortion ($|\Delta \alpha| = 0.0498$ vs $0.0739$), $54.6\%$ variance retention (vs $51.6\%$ Euclidean and $33.6\%$ random), and eliminates Layer 3 representation collapse.

### 3.6 Software Interface Specification for `00IITP-AI/src/rg_box_pooling.py`
```python
"""
Interface Contract: ConnectomeBoxCoveringPooling
Location: 00IITP-AI/src/rg_box_pooling.py
Integrates: /home/juke/git/SwiFT_v2, /home/juke/git/SwiFT-LLM, /home/juke/git/VRABES
"""
import torch
import torch.nn as nn
from typing import List, Tuple, Optional

class ConnectomeBoxCoveringPooling(nn.Module):
    def __init__(
        self,
        adj_matrix: np.ndarray,
        in_dim: int,
        out_dim: int,
        box_diameter: int = 3,
        pooling_mode: str = "mean"
    ) -> None:
        """
        Input:
            adj_matrix: (K, K) numpy array representing structural or communicability connectome.
            in_dim: Input feature dimension C (e.g., 96, 192, 384).
            out_dim: Projected output dimension 2C.
            box_diameter: l_B diameter cutoff (default 3).
            pooling_mode: 'mean', 'fiedler_weighted', or 'eigen_project'.
        """
        super().__init__()
        ...

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Performs renormalization coarse-graining over connectome graph boxes.
        Input:
            x: (B, T, K_in, C_in) parcel token tensor from SwiFT-LLM or SwiFTv25.
        Output:
            x_pooled: (B, T, N_boxes, C_out) coarse-grained supernode representation.
            box_assignments: (N_boxes, max_box_size) index tensor mapping K_in to N_boxes.
        """
        ...
```

---

## 4. Topic 3: Spectral Graph Theory & Structure Transfer Specifications

### 4.1 Pretraining Shapes Spectral Structure (`bae_spectral_arxiv_v1_20261020`)
Authored by 배상윤 선생님 (`Sangyoon Bae`), Sk Miraj Ahmed, Shinjae Yoo, and 차지욱 교수님 (`Jiook Cha`) (arXiv:2610.09709v1, 2026):
- **Theoretical Foundations & Proposition 4**:
  - The out-of-distribution (OOD) generalization error gap $\mathcal{E}_{\text{OOD}} - \mathcal{E}_{\text{ID}}$ is bounded by the spectral concentration of the model's internal representation covariance.
  - Spectral concentration is rigorously quantified via the **Participation Ratio ($PR$)**:
    $$\text{PR}(W) = \frac{\left(\sum_{i=1}^d \sigma_i^2\right)^2}{\sum_{i=1}^d \sigma_i^4} = \frac{(\text{Tr}(W^T W))^2}{\text{Tr}((W^T W)^2)}$$
    where $\sigma_i$ are the singular values of the weight matrix $W$ or feature covariance matrix $\Sigma = \frac{1}{N} X^T X$.
  - An isotropic, high-entropy representation utilizes all orthogonal modes uniformly ($PR \to d$). A degenerate representation collapsed onto a low-dimensional subspace exhibits $PR \to 1$.
- **The Cell Conditioning Law**:
  - The causal relationship between spectral concentration and out-of-distribution robustness reverses fundamentally across architecture $\times$ pretraining families:
    - **Autoregressive Causal Models (GPT family, Causal LMs)**: Lower participation ratio (steeper power-law slope $\alpha$, higher concentration) correlates with higher OOD accuracy. The model compresses redundant information into a tight semantic manifold.
    - **Bidirectional Masked Models (MLM, BERT, SwiFT, ViT)**: **Higher mean participation ratio ($PR_{\text{mean}}$)** strictly correlates with higher OOD accuracy ($92\%$ pairwise rank accuracy). High $PR$ prevents low-rank collapse during bidirectional in-filling and ensures diverse temporal primitive encoding.

### 4.2 Structure, Dimensionality, and Distribution Shape (`iclr2027_structure_transfer_39525`)
Authored by 배상윤 선생님 et al. (under review at ICLR 2027, `/home/juke/git/paper-review/iclr2027_structure_transfer_39525/`):
- **The Transfer-Invariance Principle**:
  A statistical property of pretraining data governs downstream transfer performance if and only if the model's input preprocessing pipeline is non-invariant to that property.
- **The Three Fundamental Data Axes**:
  1. **Relational Structure**: The graph coupling topology, degree distribution, and shortest paths between distinct channels.
  2. **Dimensionality**: The number of independent modes and effective rank of the signal covariance matrix.
  3. **Distribution Shape**: The marginal probability density function of individual unit activations (quantified by skewness $\gamma_1$ and excess kurtosis $\gamma_2$).
- **Empirical Validation & Normalization Causal Flip**:
  - When the input pipeline standardizes each channel independently ($z$-scoring per window, standard across fMRI, EEG, and PatchTST), it mathematically erases the marginal distribution shape ($\mu=0, \sigma=1, \text{kurtosis normalized}$). Downstream transfer is governed entirely by relational structure and follows an inverted-U curve peaking at an optimal synthetic connectome density.
  - When the input pipeline processes raw signal magnitudes without channel-wise normalization (e.g., neural calcium imaging, POYO+), marginal distribution shape becomes the dominant transfer determinant (toggling normalization changes the causal effect size of distribution shape by $5.3\times$).

### 4.3 Layerwise Renormalization Flow & Empirical Diagnostic Quintet
In `00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md` (Table 3), layerwise RG flow was evaluated across four brain foundation models (`SwiFT E192`, `BrainLM`, `BrainJEPA`, `NeuroSTORM`):
1. **Participation Ratio ($PR$)**:
   $$\text{PR} = \frac{(\sum \lambda_i)^2}{\sum \lambda_i^2}$$
2. **Spectral Power-Law Exponent ($\alpha$)**:
   - Eigenvalues $\lambda_n$ of the feature covariance matrix sorted in descending order: $\lambda_n \sim n^{-\alpha}$.
   - Evaluated over the power-law regime $n \in [2, \min(50, d/2)]$.
   - Biological criticality boundary: $\alpha \in [1.5, 2.0]$.
3. **Box-Covering Fractal Dimension ($d_B$)**:
   - Evaluated on the thresholded token correlation graph $G^{(l)}$: $N_B(\ell_B) \sim \ell_B^{-d_B}$.
4. **Hub Repulsion Ratio ($R_{\text{hub}}$)**:
   $$R_{\text{hub}} = \frac{E_{\text{actual}}(k_{\text{hub}}, k_{\text{hub}})}{E_{\text{expected}}(k_{\text{hub}}, k_{\text{hub}})}$$
   $R_{\text{hub}} < 1.0$ indicates disassortative hub-repulsion (Song Mode II fractality).
5. **Degree Assortativity ($r$)**:
   - Pearson correlation coefficient of degrees between connected node pairs in $G^{(l)}$.

**Empirical Ground-Truth Benchmark Values**:
```
+------------------------------------+------------+--------+----------+-------+-------------+---------+
| Model & Layer                      | Tensor Dim | PR     | alpha    | d_B   | R_hub       | r       |
+------------------------------------+------------+--------+----------+-------+-------------+---------+
| SwiFT E192 Layer 0                 | 57 x 384   |  2.78  | 1.4717   | 2.24  | 3.6273      | +0.2212 |
| SwiFT E192 Layer 1                 | 57 x 768   |  2.78  | 0.9887   | 2.18  | 3.0832      | +0.0995 |
| SwiFT E192 Layer 2 (Critical Peak) | 57 x 1536  | 11.02  | 1.5980   | 2.80  | 2.9925      | -0.0652 |
| SwiFT E192 Layer 3 (Over-compress) | 57 x 1536  |  3.58  | 1.8411   | 1.58  | 4.6248      | +0.3430 |
| BrainLM (Masked Autoencoding)      | 57 x 768   |  4.32  | 1.4580   | 1.53  | 4.5341      | +0.1768 |
| BrainJEPA (Joint Embedding)        | 57 x 768   | 11.79  | 1.8807   | 1.85  | 4.6248      | -0.0826 |
| NeuroSTORM (Predictive Coding)     | 25 x 288   | 12.51  | 1.1960   | 1.69  | 4.5000      | -0.1923 |
| SwiFT-LLM NeuroPrior (450 ROI)     | 450 x 200  |  9.45  | 1.9112   | 3.35  | 3.4006      | +0.5112 |
+------------------------------------+------------+--------+----------+-------+-------------+---------+
```

### 4.4 Software Interface Specification for `00IITP-AI/src/spectral_rg_flow_diagnostic.py`
```python
"""
Interface Contract: SpectralRGFlowDiagnostic
Location: 00IITP-AI/src/spectral_rg_flow_diagnostic.py
Integrates: /home/juke/git/paper-review/bae_spectral_arxiv_v1_20261020, iclr2027_structure_transfer_39525
"""
import torch
import numpy as np
from typing import Dict, Any, List

class SpectralRGFlowDiagnostic:
    def __init__(
        self,
        critical_alpha_range: Tuple[float, float] = (1.5, 2.0),
        box_diameter_range: List[int] = [2, 3, 4],
        correlation_quantile: float = 0.85
    ) -> None:
        """
        Diagnostic auditor tracking representation criticality vs collapse.
        """
        ...

    def audit_layer_representation(
        self, 
        embedding_tensor: torch.Tensor
    ) -> Dict[str, float]:
        """
        Input:
            embedding_tensor: (B, D) or (B, T, D) representation matrix from any layer.
        Output:
            {
                'participation_ratio': float,
                'power_law_alpha': float,
                'box_covering_dim_dB': float,
                'hub_repulsion_R': float,
                'degree_assortativity_r': float,
                'criticality_health_score': float, # [0, 1]
                'diagnosis_flag': str # 'HEALTHY_CRITICAL', 'OVER_COMPRESSED_COLLAPSE', 'ISOTROPIC_NOISE'
            }
        """
        ...
```

---

## 5. Topic 4: C. elegans Connectome, ReSU Neuromorphic Dynamics & Ephys Foundation Models

### 5.1 C. elegans Stage-Specific Connectome & Gap Junction vs Chemical Synapses
- **Source Reference**: `/home/juke/git/neurox-discovery-bench/sources/screening/choe2026-celegans-connectome-gapjunction.json` (Choe et al., 2026; Yim, Choe, Bae et al., *Nat Commun* 2024; Cook et al., *Nature* 2019).
- **Coordinate Framework**: Unified $180 \times 180$ canonical neuron matrix representing the somatic nervous system.
- **Biophysical Properties**:
  - **Chemical Synapses ($A_{\text{chem}}$)**:
    - Asymmetric ($A_{ij} \ne A_{ji}$), signed (excitatory acetylcholine/glutamate vs inhibitory GABA).
    - Characterized by finite synaptic delay ($\Delta t \approx 5 - 20\text{ ms}$) and neurotransmitter vesicular saturation.
  - **Gap Junctions / Electrical Synapses ($G_{\text{elec}}$)**:
    - Strictly symmetric ($G_{ij} = G_{ji} \ge 0$), non-negative conductance matrix.
    - Mediated by innexin hexameric hemichannels bridging intercellular cytoplasm.
    - Operates instantaneously without transmission delay ($0\text{ lag}$), performing pure bi-directional electrotonic charge equalization:
      $$I_{\text{gap}, i} = \sum_{j} G_{ij} (V_j - V_i)$$
- **Dauer Developmental Stage Nociceptive Escape Circuit**:
  - Key neurons: Nociceptive sensory neuron ASH, backward command interneurons (AVA, AVD), forward command interneurons (AVB, PVC).
  - Developmental Rewiring Mechanism:
    - Adult state: Escape reversal is prolonged; chemical inhibition balances forward/backward command units.
    - Dauer diapause state: Reversal duration is significantly shortened ($p = 8.3 \times 10^{-4}$), accelerating forward crawling recovery.
    - Dauer-specific gap junction insertions: $\text{ASH}=\text{AVD}$, $\text{AVB}=\text{AVD}$, and $\text{AVB}=\text{PVC}$.
    - Mechanistic function: The $\text{AVB}=\text{AVD}$ gap junction allows the forward command interneuron AVB to rapidly recover from inhibition during nociceptive stimulation, aborting the reversal crawl early.

### 5.2 ReSU Local Learning Dynamics & Non-Backprop Inference (`00IITP-AI/src/local_learning_engine.py`)
Implemented in `00IITP-AI/src/local_learning_engine.py` following Chklovskii et al. (AAAI 2026) and Pehlevan & Chklovskii (2015):
- **Fast Recurrent Relaxation Dynamics**:
  Continuous-time membrane dynamics integrated via 4th-order Runge-Kutta (RK4) over internal relaxation time $\tau \in [0, T_{\text{relax}}]$:
  $$\tau_y \frac{dy}{d\tau} = -y + W p_t - (M \odot M_{\text{mask}}) y$$
  where $p_t \in \mathbb{R}^{\text{dim}_p}$ is the streaming sensory input vector, $W \in \mathbb{R}^{k \times \text{dim}_p}$ is the feedforward synaptic weight matrix, $M \in \mathbb{R}^{k \times k}_{\ge 0}$ is the lateral inhibitory matrix, and $M_{\text{mask}} \in \{0, 1\}^{k \times k}$ is the structural connectome mask ($\text{diag}(M_{\text{mask}}) = 0$).
  Relaxed steady-state fixed point:
  $$y^* = (I + M \odot M_{\text{mask}})^{-1} W p_t, \quad y_{\text{rect}} = \max(0, y^*)$$
- **Slow Synaptic Plasticity (Normative Neural Similarity Matching)**:
  - Feedforward Oja subspace plasticity:
    $$\Delta W_{ij} = \eta_w (y_i p_j - y_i^2 W_{ij})$$
  - Lateral anti-Hebbian decorrelating plasticity:
    $$\Delta M_{ik} = \eta_m \left((y_i y_k - \gamma M_{ik}) \cdot M_{\text{mask}, ik}\right), \quad M_{ik} \leftarrow \max(0, M_{ik}), \quad M_{ii} = 0$$
- **Strict Biological Non-Backprop Constraints**:
  - Global loss gradient is identically zero: $\nabla_\theta \mathcal{L} \equiv \emptyset$.
  - Zero weight transport: Weight update $\Delta W_{ij}$ relies exclusively on pre-synaptic activation $p_j$ and post-synaptic firing $y_i$.
- **6-Topology Empirical Benchmark Verification (`connectome_topology.py`)**:
  As verified in `00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md` (Table 4) under a controlled $25.0\%$ lateral wiring density:
  - `C0` Unconnected Null: $PR = 1.02$, RF Orthogonality $= 0.0156$ (complete collapse; all 24 units redundantly learn PC1).
  - `C1` Erdős-Rényi Random: $PR = 2.40$, Orthogonality $= 0.5361$.
  - `C2` Watts-Strogatz Small-World: $PR = 2.87$, Orthogonality $= 0.5789$.
  - `C3` Mode I Rich-Club ($R_{\text{hub}} = 4.0$): $PR = 1.31$, Orthogonality $= 0.3569$, runaway stability threshold $\lambda_{\text{crit}}$ drops $28\%$.
  - **`C4` Mode II Bio-Connectome ($R_{\text{hub}} = 0.0$, Fractal + FFL)**: $PR = \mathbf{3.2127}$, Orthogonality $= \mathbf{0.7242}$ ($96.1\%$ of dense all-to-all), wiring efficiency $= \mathbf{2.3280}$ dimensions per 100 synapses (1st place across all topologies).
  - `C5` Dense All-to-All ($100\%$ wiring): $PR = 7.0353$, Orthogonality $= 0.7535$, wiring efficiency $= 1.2745$.

### 5.3 Electrophysiology Foundation Models (`DIVER` & `ephys-foundation-model-plan`)
- **DIVER Model Ecosystem (`/home/juke/git/DIVER`)**:
  - Unified electrophysiology repository containing architectures: `BrainBERT`, `Brant`, `BIOT`, `BENDR`, `CBraMod`, `LaBraM`, `Medformer`, `OpenLTM`.
  - Canonical DIVER Architecture: 32 electrode channels, $d_{\text{model}} = 512$, 12 Transformer layers, patch size 50 timepoints.
- **Hierarchical Streaming Long-Context Wrapper**:
  - Enables training on up to 80-minute (4,800-second) continuous intracranial recordings within $11.38\text{ GiB}$ GPU memory by chaining chunked gradient checkpointing with cross-chunk key-value state preservation.
- **Length Extrapolation Findings**:
  - Models extrapolate short-range contexts cleanly ($16 \to 64$ chunks, error $= 0.0108$).
  - However, long-range intervals suffer catastrophic breakdown ($256$ chunks, error $= 1.0134$). Standard learned positional embeddings fail over extended durations without multi-scale hierarchical frequency banks.

### 5.4 Software Interface Specification for `00IITP-AI/src/fractal_motif_resu.py`
```python
"""
Interface Contract: FractalMotifReSU
Location: 00IITP-AI/src/fractal_motif_resu.py
Integrates: /home/juke/git/00IITP-AI, /home/juke/git/DIVER, choe2026-celegans-connectome-gapjunction.json
"""
import torch
import torch.nn as nn
from typing import Dict, Tuple, Optional

class FractalMotifReSU(nn.Module):
    def __init__(
        self,
        in_channels: int = 32,      # e.g., 32-channel DIVER iEEG or Schaefer-304
        hidden_units: int = 180,    # C. elegans coordinate dim or neuromorphic layer
        connectome_type: str = "c_elegans_dauer", # 'c_elegans_adult', 'c_elegans_dauer', 'fractal_mode_ii'
        eta_w: float = 0.001,       # Oja learning rate
        eta_m: float = 0.005,       # Anti-Hebbian lateral learning rate
        gamma: float = 0.05,        # Lateral synaptic decay
        device: str = "cpu"
    ) -> None:
        """
        Backpropagation-free neuromorphic similarity matching engine.
        """
        super().__init__()
        ...

    def forward_streaming_step(
        self, 
        p_t: torch.Tensor, 
        update_weights: bool = True
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Executes single-step online RK4 relaxation and optional synaptic weight update.
        Input:
            p_t: (B, in_channels) instantaneous streaming signal vector.
            update_weights: If True, applies local Oja and anti-Hebbian updates online.
        Output:
            y_rect: (B, hidden_units) rectified neuronal output.
            diagnostics: {
                'synaptic_energy': float,
                'spectral_radius_M': float,
                'weight_divergence_norm': float
            }
        """
        ...
```

---

## 6. Cross-Topic Architectural Integration Contracts

### 6.1 End-to-End Data Pipeline Flow & Module Interoperability
The following table formalizes how the newly engineered modules in `00IITP-AI/src/` interface directly with existing classes and data formats across all four repositories:

```
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| Stage                       | Audited External Source            | 00IITP-AI Integration Module   | Output Tensor Signature     |
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| 1. Multiband Preprocessing  | enigma_ocd_mbbn                    | mbbn_connectome_biomarker.py   | (B, Channels=4, T=464, 304) |
|                             | data/vmd_cache_4ch_464_head.mmap   | Class: MBBNConnectomeBiomarker |                             |
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| 2. Directed Motif Profiling | enigma_ocd_mbbn                    | mbbn_connectome_biomarker.py   | SP: (B, 13)                 |
|                             | model.py:Attention (Spatial)       | Method: compute_triad_sp       | Flow Adjacency: (B, 304,304)|
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| 3. Volumetric Tokenization  | SwiFT-LLM                          | SwiFTv25 / MBSD-Tokenizer      | (B, T=20, K=400, C=96)      |
|                             | anatomical_4d_patch.py:572         | Paradigm B SpMM Projection     |                             |
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| 4. Connectome RG Pooling    | SwiFT_v2 swin4d_ver12.py:529       | rg_box_pooling.py              | (B, T=10, N_box=100, C=192) |
|                             | Song 2005 Graph Box-Covering       | Class: ConnectomeBoxPooling    |                             |
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| 5. Spectral OOD Audit       | bae_spectral_arxiv_v1_20261020     | spectral_rg_flow_diagnostic.py | Quintet: (PR, alpha, d_B,   |
|                             | iclr2027_structure_transfer_39525  | Class: SpectralRGDiagnostic    |           R_hub, r)         |
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
| 6. Neuromorphic Streaming   | DIVER / ephys-foundation-model     | fractal_motif_resu.py          | (B, Hidden=180)             |
|                             | choe2026-celegans-gapjunction.json | Class: FractalMotifReSU        | Zero-Backprop Online State  |
+-----------------------------+------------------------------------+--------------------------------+-----------------------------+
```

### 6.2 Master Tensor Dimension Contracts
For rigorous unit testing and tensor dimension verification in `tests/`:

1. **MBBN Input Tensor**:
   $$X_{\text{mbbn}} \in \mathbb{R}^{B \times 4 \times 464 \times 304}, \quad \text{Mask}_{\text{mbbn}} \in \{0, 1\}^{B \times 464 \times 304}$$
2. **MBBN Spatial Dynamic Connectivity Attention Map**:
   $$A_{\text{spatial}} \in \mathbb{R}^{B \times 8 \times 304 \times 304}$$
3. **Milo Triad Significance Profile Vector**:
   $$\vec{SP} \in \mathbb{R}^{B \times 13}, \quad \|\vec{SP}\|_2 = 1.0$$
4. **SwiFT 4D Raw Volumetric Input**:
   $$X_{\text{vol}} \in \mathbb{R}^{B \times C \times 96 \times 96 \times 96 \times 20}, \quad C \in \{1, 2\}$$
5. **SwiFT Anatomical MBSD Eigen-Tokens**:
   $$Z_{\text{anat}} \in \mathbb{R}^{B \times 20 \times 400 \times 96}$$
6. **Connectome Box-Covering Pooled Tokens**:
   $$\mathcal{R}_{\ell_B=3}(Z_{\text{anat}}) \in \mathbb{R}^{B \times 10 \times 100 \times 192}$$
7. **C. elegans Synaptic Weight & Mask Matrices**:
   $$W \in \mathbb{R}^{180 \times 32}, \quad M \in \mathbb{R}^{180 \times 180}_{\ge 0}, \quad M_{\text{mask}} \in \{0, 1\}^{180 \times 180}, \quad \text{diag}(M_{\text{mask}}) = 0$$
8. **ReSU Online Firing Rate**:
   $$y_{\text{rect}} \in \mathbb{R}^{B \times 180}_{\ge 0}$$

### 6.3 Verification & Compliance Checklist
- [x] **Strict Read-Only Verification**: No files in external repositories (`enigma_ocd_mbbn`, `SwiFT_v2`, `SwiFT-LLM`, `VRABES`, `bae_spectral_arxiv_v1_20261020`, `DIVER`) were altered or created.
- [x] **Uncommitted Project Files Preserved**: All existing files in `00IITP-AI` (`그랜트아이디어.md`, `아이디어.txt`, `docs/qa_prep_차지욱_20260309.md`, `HANDOFF.md`, etc.) remain in their original uncommitted state.
- [x] **Authentic Ground-Truth Values**: All tensor dimensions, class names, file paths, and empirical benchmark metrics cited directly reflect real code and empirical audit data.
- [x] **Honorific Protocol**: All lab researchers (배상윤 선생님, 한동엽 선생님, 왕희환 선생님, 이아현 선생님, 최주빈 선생님) referenced with polite 존댓말 and academic respect.
