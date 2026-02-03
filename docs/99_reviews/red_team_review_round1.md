# Red Team Review (Round 1)
**Date**: 2026-02-03
**Target**: `docs/03_proposal/PROPOSAL_PLAN.md`
**Reviewer Persona**: Senior IITP Project Manager / Skeptical Neuroscientist

## 1. Overall Verdict: **CONDITIONAL REJECT (Significant Gaps Detected)**
While the inclusion of the "Titans" architecture and "Tubularity" (2601.21508) provides strong mathematical novelty, the current plan **fails to fully address the specific requirements of the IITP RFP (2026-AI-010~014)** and deviates partly from the core **IdeaDeck** strategy. The "Wellness Agent" application feels disconnected from the "Foundation Model" gravity.

## 2. Key Deficiencies (Gap Analysis)

### A. Missing "Embodiment" & "Physical Senses" (RFP-013 Critical)
-   **Critique**: The RFP explicitly demands "Physical Sensations (Tactile, Proprioception, Vestibular)" integration. The current plan focuses heavily on Visual, Audio, and Text (standard Multimodal LLM scope) + Brain.
-   **Risk**: Without Proprioception/Tactile, this is just a "Brain-aligned LLM," not a "Sensorimotor Foundation Model."
-   **Requirement**: Must integrate **Proprioception (Body Position)** and **Tactile** data into the Dual Encoder architecture.

### B. "Wellness" vs "Allostasis" (Framing Issue)
-   **Critique**: "Wellness Agent" sounds like a simplistic commercial application (Mental Health App). The RFP (011) asks for "Biological Learning Principles" and "Energy Efficiency."
-   **Idea Deck Alignment**: IdeaDeck emphasizes "Self-restoration" and "Interoception" for *system robustness*, not just user happiness.
-   **Requirement**: Reframe "Wellness" as **"Allostatic Regulation of the Agent-Human System."** The goal is not just 'happiness' but **'Homeostatis & Predictive Energy Management'** (Scientific terminology).

### C. Missing "Selective Attention" & "Meta-Cognition" (RFP-010/014)
-   **Critique**: The plan mentions "Titans Memory," but misses the **"Top-down Selective Attention"** mechanism required by RFP 014 (Data Semanticization). How does the agent *choose* what to encode?
-   **Requirement**: Explicitly define the "Attention Controller" or "Goal-driven Gating" in the architecture.

### D. Idea Deck Misalignment (LTC/Neural ODE)
-   **Critique**: The Idea Deck explicitly highlights **Liquid Time-Constant (LTC)** networks and **Neural ODEs** as the "Microscale" primitive. The current plan focuses generic "Spiking/CNN".
-   **Requirement**: Reintroduce **LTC/Neural ODE components** into the "Brain Spatiotemporal Encoder" description.

## 3. Action Items for Revision
1.  **Expand Encoders**: Add **Proprioception/Tactile** to the Sensory Encoder block.
2.  **Reframe Application**: Rename "Wellness Agent" to **"Allostatic Neuro-Twin Agent"**. Focus on "Energy-constrained Predictive Regulation."
3.  **Refine Architecture**: Add **"Top-down Selective Attention"** arrows in the diagram description.
4.  **Tech Stack Update**: Explicitly mention **LTC/Neural ODE** for time-series encoding.
