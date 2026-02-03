---
description: High-fidelity proposal drafting loop using Embodied Neuro Skills.
---

# Workflow: Proposal Drafting (Embodied Neuro-AI)

## Prerequisites
-   `docs/03_proposal/PROPOSAL_PLAN.md` must be finalized.
-   Skills `embodied-neuro-proposal-writer` and `embodied-neuro-reviewer` must exist.

## Steps

### Part 1: Architecture
1.  **Read Skill**: `view_file .agent/skills/embodied-neuro-proposal-writer/SKILL.md`
2.  **Draft**: Generate `docs/03_proposal/drafts/01_architecture.md`.
    -   *Constraint*: Must mention "Proprioception" and "LTC".
3.  **Review**: Run `embodied-neuro-reviewer` on the draft.
4.  **Refine**: Apply fixes if Reviewer fails.

### Part 2: Methodology
1.  **Draft**: Generate `docs/03_proposal/drafts/02_methodology.md`.
    -   *Constraint*: Must mention "Tubular Manifold" and "Bertram 2026".

### Part 3: Allostasis
1.  **Draft**: Generate `docs/03_proposal/drafts/03_allostasis.md`.
    -   *Constraint*: Must mention "Predictive Allostasis" and "Energy Efficiency".

## Execution
Use `task_boundary` to track progress per Part.
