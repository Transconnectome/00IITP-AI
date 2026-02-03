---
name: embodied-neuro-proposal-writer
description: Writes high-fidelity proposal drafts focusing on Embodied Neuro-AI (Dual Encoders, LTC, Titans) and Allostasis.
---

# Skill: Embodied Neuro Proposal Writer

## Goal
Generate "Nature-style" scientific proposal text that aligns strictly with `docs/03_proposal/PROPOSAL_PLAN.md`.

## Context & Constraints
1.  **Source of Truth**: Always read `docs/03_proposal/PROPOSAL_PLAN.md` first.
2.  **Key Terminology**:
    -   **DO NOT USE**: "VAE", "Simple CNN", "Wellness App".
    -   **MUST USE**: "Liquid Time-Constant (LTC)", "Neural ODE", "Proprioception", "Top-down Selective Attention", "Predictive Allostasis", "Tubular Manifold".
3.  **Tone**: Academic, Authoritative, persuasive, yet novel.

## Process
1.  **Input Analysis**: Identify the target section (e.g., Part 1, Part 3).
2.  **Reference Loading**: Check `## 5. Bibliography` in PROPOSAL_PLAN.md.
3.  **Drafting**:
    -   Structure: Definition -> Mechanism -> Novelty -> Validation.
    -   Citation: Use [1], [2], etc. correctly.
4.  **Self-Correction**:
    -   Did I mention "Proprioception" in the Encoder section?
    -   Did I mention "Energy Efficiency" in the Wellness section?

## Output
-   Write to: `docs/03_proposal/drafts/partX_keyword.md`.
