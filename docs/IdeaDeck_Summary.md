# IdeaDeck Research Summary: Robust and Efficient Multisensory Integrated Intelligence

This document summarizes the core research ideas extracted from `IdeaDeck.pptx`.

## 1. Core Objective

**"강건하고 효율적인 다중감각 통합 지능: 예측적 잠재표상 주도의 선택적 주의 지각 모사 접근법"**
(Robust and Efficient Multisensory Integrated Intelligence: A Predictive Latent Representation-Driven Selective Attention Approach for Biomimetic Perception)

The goal is to develop a "brain-faithful yet engineering-robust" AI that:

1. Integrates **Exteroception** (external), **Proprioception** (self), and **Interoception** (internal) signals.
2. Uses **Selective Attention** based on goals.
3. Creates a **Consistent Latent Representation** (Platonic Representation) of the world.
4. **Self-restores** sensory deficits in uncertain environments.

## 2. Key Architectural Components

### A. Multiscale Modeling Primitives

- **Microscale (Neuron-level):** Uses **Liquid Time-Constant (LTC)** Neural Networks / Neural ODEs as the "Sweet Spot" between biological realism (SNN) and learning efficiency (Standard RNN).
- **Mesoscale (Circuit-level):** Modularized blocks for each modality with feedback-enabled RNN structures.
- **Macroscale (Whole-brain):** **Global Neural Workspace (GNW)** theory-based multimodal self-supervised learning. Centralizes abstract representations into a common latent space.

### B. Memory and Attention

- **Titans (Learning to Memorize at Test Time):** Utilizes long-term memory State-Space Models (SSM) and Bayesian surprisal to selectively store "surprising" sensory information that deviates from context/memory.

### C. Multisensory Synchronization

- **Asynchronous Integration:** Addresses "Sensory Silo" and "Overconfident AI" issues by combining continuous-time inference (ODE) for single modalities with discrete-time SSM for integration.
- Hardware-level precision (<1ms) and PTP (Precision Time Protocol) are visualized for the Data Acquisition System (Slide 8).

## 3. Digital Brain Twin & World Model

- The proposed system functions as a **Multimodal World Model** that understands both internal and external environments.
- Visualized in Slide 13 as a generative process (similar to Dreamer or World Models) where context input leads to open-loop predictions.

## 4. Evaluation Framework

- **Engineering Perspective:** Focus on robustness, resilience, and "survival/mission completion" in physical environments.
- **Brain Science Perspective:** Cognitive validity, evaluating how well the AI mimics human/animal perception principles (Predictive Coding, Active Inference).

## 5. Team Strengths

- Expertise in diverse modalities (Visual, Auditory, Olfactory, Tactile, Proprioceptive, Interoceptive).
- Strong modeling capabilities at the circuit level and integration at the wholistic level.
- High-impact research track record and international collaboration.
