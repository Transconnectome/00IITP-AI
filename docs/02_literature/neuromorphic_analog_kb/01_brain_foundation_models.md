# Brain Foundation Models (BFMs) & Analog Implementations

## 1. The Rise of Brain Foundation Models (2024-2025)

**Reference**: *Zhou, X., Liu, C., et al. "A Survey on Brain Foundation Models." arXiv preprint, March 2025.*

Brain Foundation Models (BFMs) represent a paradigm shift from task-specific decoding to general-purpose neural representation learning. Unlike traditional BCI decoders trained on small, subject-specific datasets, BFMs are pre-trained on massive corpora of neural data (fMRI, EEG, iEEG, Spikes).

### Key Characteristics

* **Cross-Modal Generalization**: Ability to align latent spaces across different modalities (e.g., aligning fMRI BOLD signals with EEG transients).
* **Few-Shot Adaptation**: Fine-tuning for specific subjects or clinical tasks (e.g., paralysis restoration) with minimal new data.
* **Self-Supervised Learning**: Utilizing masked autoencoders (MAE) and contrastive learning on temporal neural signals to learn robust dynamics.

## 2. Analog Foundation Models: The Hardware Connection

**Reference**: *IBM Research. "Analog Foundation Models for NeurIPS 2025." December 2025.*

As BFMs grow in size (billions of parameters), their inference cost on digital hardware (GPUs) becomes prohibitive for implantable or edge applications. Analog In-Memory Computing (AIMC) offers a solution.

### Theory of Analog BFM Inference

* **Matrix-Vector Multiplication (MVM)**: BFMs, being Transformer or State-Space (Mamba) based, rely heavily on MVM. Analog arrays perform this in $O(1)$ time complexity with respect to matrix row size, using Ohm's law ($I = G \cdot V$) and Kirchhoff's current law ($\sum I$).
* **Noise-Aware Training**: Analog devices are noisy and have limited precision (e.g., 4-8 bits equivalent). 2025 research demonstrates that *noise-aware training* (injecting noise during the digital pre-training phase) allows the BFM to be robust to the physical imperfections of analog phase-change memory (PCM) or ReRAM devices.
* **Energy Efficiency**: Potential for $>100 \times$ improvement in TOPS/W compared to digital accelerators, crucial for "Digital Twin" implants.

## 3. Neuro-Symbolic Integration in Neuromorphic BFMs

**Reference**: *Kudithipudi, D., et al. "Neuromorphic Computing 2025: Current SotA."*

A key frontier is combining the statistical power of BFMs with the symbolic reasoning of "Neuro-Symbolic" AI, implemented on neuromorphic hardware.

* **Hybrid Architecture**: Using analog SNNs for the fast, intuitive perception (System 1) and digital cores for slow, deliberative reasoning (System 2).
* **Use Case**: A Digital Twin Brain that not only simulates neural activity but can "reason" about the outcome of a simulated drug intervention.

## 4. Key Takeaways for Grant Proposal

1. **Proposal Angle**: We will develop a **"Hardware-Aware Brain Foundation Model"** specifically designed to be deployable on Korea's next-gen neuromorphic chips (K-Neuro/NPU).
2. **Innovation**: We will not just train a BFM; we will demonstrate its "Physical Isomorphism" by mapping its weights to analog conductance states, validating the "Neuro for AI" loop.
3. **Feasibility**: Citing IBM's 2025 Analog Foundation Model work proves that deploying Transformers on analog hardware is no longer theoretical but practically achievable with noise-aware training.

## References

* [Zhou et al. (2025) - Brain Foundation Models](./pdfs/zhou_2025_brain_foundation_models.pdf)
* [IBM (2025) - Analog Foundation Models](./pdfs/ibm_2025_analog_foundation_models.pdf)
