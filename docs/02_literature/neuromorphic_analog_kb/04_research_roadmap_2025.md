# Research Roadmap 2025: Neuro-Analog for AI

**Proposal Strategy for "Brain Foundation Models & Digital Twin Brain"**

## 1. Vision

To build a **"Physically Isomorphic Brain Foundation Model"** that bridges the gap between the algorithmic power of modern AI (Transformers/Mamba) and the energy efficiency of biological intelligence, implemented on next-generation Analog Neuromorphic hardware.

## 2. Research Tracks (answering DOE Workshop Needs)

### Track A: The "Brain Foundation Model" (Algorithm-Hardware Co-Design)

* **Goal**: Train a BFM that is "Analog-Ready".
* **Approach**:
  * **Phase 1 (Year 1)**: Develop a "Noise-Injection Training" pipeline. Train 1B-parameter BFMs on GPUs with simulated analog noise (drift, variability).
  * **Phase 2 (Year 2)**: Quantize BFM weights to low-precision memristive states (4-bit).
  * **Phase 3 (Year 3)**: Deploy the BFM on a prototype Analog NPU (collaboration with K-Neuro chips) for real-time biological signal decoding.
* **Key Reference**: *IBM Analog Foundation Models (2025)*.

### Track B: The "Digital Twin Brain" (Scalable Simulation)

* **Goal**: A localized "Hippocampal Digital Twin" for memory restoration experiments.
* **Approach**:
  * **Phase 1**: Build a high-fidelity biological model of the CA1-CA3 hippocampal circuit using the GPU-HPC platform (14k GPU scale).
  * **Phase 2**: Map this biological model to "Neuromorphic Primitives" (LIF Neurons + Plastic Synapses).
  * **Phase 3**: Run the "Twin" in parallel with real neural data recording, using the BFM to align the latent states.

### Track C: Neuromorphic Primitives (Basic Research)

* **Goal**: Design the "Active Dendrite" circuit.
* **Focus**: Move beyond point-neurons. Design a sub-threshold analog circuit that allows non-linear dendritic integration, increasing the computational capacity of a single silicon neuron by $10\sim100\times$.

## 3. Evaluation Metrics (How to measure success?)

The proposal must include these KPIs to score "Max Points":

1. **Energy Efficiency**: Target **< 10 pJ per synaptic op** (compare to 1-10 nJ on GPU).
2. **Isomorphism Score**: Correlation between the "Digital Twin's" spike trains and biological "Ground Truth" data (using Representational Similarity Analysis).
3. **Real-Time Latency**: < 5ms inference delay (critically important for closed-loop neuro-stimulation).

## 4. Why This Wins

This roadmap directly addresses the "Hardware-Software Co-Design" gap. Most proposals focus only on the AI (BFM) or only on the Chip (Neuromorphic). We propose a **unified stack**:

* **BFM as the Operating System.**
* **Digital Twin as the Application.**
* **Analog Neuromorphic as the Hardware.**

This holistic approach aligns perfectly with the "Neuro for AI" and "AI for Neuro" virtue cycle.
