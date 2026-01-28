---
name: draft-writer-neurox
description: Writes draft sections for the proposal, focusing on the Two-Part Model and Team R&R.
---

# Skill: Draft Writer (NeuroX)

## Goal

Generate high-quality, government-style text for specific sections of the proposal.

## Implementation

1. **Context**: Load `docs/01_project_planning/outline_iitp_v1.md` and `docs/01_project_planning/email_analysis_and_insights.md`.
2. **Style**: Apply `/.agent/rules/02_style.md` (Short sentences, bold KPIs).
3. **Drafting**:
    - **Part 1 (Encoder)**: Focus on Predictive Coding, VAE.
    - **Part 2 (Titans)**: Focus on Neural Memory, Surprisal, Forgetting.
4. **Verification**: Check against `01_citations.md`.

## Output

- `docs/03_proposal/drafts/section_XX_draft.md`
