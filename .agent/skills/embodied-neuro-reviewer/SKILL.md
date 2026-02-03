---
name: embodied-neuro-reviewer
description: Reviews proposal drafts for strict adherence to Embodied Neuro-AI (Proprioception, LTC) and RFP constraints.
---

# Skill: Embodied Neuro Reviewer

## Goal
Ensure every draft section is scientifically rigorous, novel, and compliant closer to "Rejection-Proof" status.

## Checklist (Pass/Fail)
1.  **Embodiment Check**: Does the text mention *how* Proprioception or Tactile data is encoded? (Pass if yes).
2.  **Algorithm Check**: Does it use "Liquid Time-Constant" or "Neural ODE"? (Fail if it says generic CNN/RNN).
3.  **Application Check**: Is the "Wellness" concept framed as "**Predictive Allostasis**"? (Fail if "Happy App").
4.  **Novelty Check**: Is "Tubular Manifold" or "Manifold Alignment" mentioned in the methodology?
5.  **Reference Check**: Are citations [1]-[5] used correctly?

## Process
1.  **Read Draft**: Read the target file.
2.  **Apply Logic**: Run the checklist.
3.  **Critique**: Generate a report `docs/99_reviews/review_partX.md`.
4.  **Verdict**: ACCEPT or REVISE.
