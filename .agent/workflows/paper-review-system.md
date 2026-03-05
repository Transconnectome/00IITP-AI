---
description: Automated Paper Review & Refinement System Workflow
---

# Paper Review System Workflow

Follow this guide to analyze a paper, download its references, critique it, and refine the content using NotebookLM.

## 1. Setup & Ingestion

### Step 1.1: Download References

Run the extraction script to download referenced papers from arXiv. This builds your context library.

```bash
# Usage: python3 scripts/download_references.py <path_to_main_paper_pdf> <output_dir>
python3 scripts/download_references.py "papers/MyPaper.pdf" "references/MyPaper_Refs"
```

### Step 1.2: Prepare Files for NotebookLM

1. Upload the `references/MyPaper_Refs` folder to NotebookLM as a source.
2. Upload your Main Paper PDF as a source.
3. Upload your Rebuttal Letter (if applicable).

## 2. Review Process

### Step 2.1: Analyze Rebuttal Letter (If revising)

Run the script to structure the rebuttal.

```bash
python3 scripts/analyze_rebuttal.py "papers/Rebuttal.pdf"
```

*Output*: A Markdown file `papers/Rebuttal_analysis.md`. Upload this to NotebookLM too.

### Step 2.2: Verify Rebuttal Coverage (In NotebookLM)

Use the following prompt in NotebookLM:

> **Prompt**: "Based on the uploaded 'Rebuttal_analysis.md' and the 'Main Paper', check if every reviewer comment has been addressed in the main text. Identify any missing points or weak responses where the changes in the paper do not match the promise in the rebuttal."

### Step 2.3: Red Team Review (Simulation)

Ask NotebookLM to act as a critical reviewer.

> **Prompt**: "Act as a strict, critical reviewer for a top-tier glossy journal (e.g., Nature Medicine, JAMA Psychiatry, NeurIPS). Your goal is to identify fatal flaws that would lead to rejection.
>
> 1. **Conceptual Novelty**: Does this paper simply apply a known method to a new dataset, or is there genuine methodological or conceptual innovation? Compare against the key references I provided.
> 2. **Methodological Rigor**: Scrutinize the data partitioning description in the methods/supplementary. Is there any possibility of data leakage? Are the baselines (e.g., symptom-based models) fair?
> 3. **Overclaiming**: Identifying any causal claims made from observational/cross-sectional data.
> 4. **Output**: List the 3 most damaging criticisms a hostile reviewer could make, and for each, draft a paragraph that the authors *should* have written to preempt this critique."

## 3. Content Refinement (Camera-Ready)

### Step 3.1: Abstract Refinement
>
> **Prompt**: "Act as a professional scientific editor. Rewrite the **Abstract** to be punchy, precise, and impactful (Camera-Ready Quality).
>
> - **Constraint 1**: Strictly follow the structure: Background (1 sentence) -> Gap/Problem (1 sentence) -> Method (1-2 sentences) -> Key Results (Quantified, 2-3 sentences) -> Implication (1 sentence).
> - **Constraint 2**: Remove passive voice. Use strong verbs (e.g., 'We demonstrate,' 'Our model outperforms').
> - **Constraint 3**: Ensure the 'hook' in the first sentence immediately grabs the reader's attention regarding the urgency of youth depression prediction."

### Step 3.2: Introduction Refinement
>
> **Prompt**: "Critique and rewrite the **Introduction**.
>
> - **Flow**: Ensure a perfect funnel shape: Broad Clinical Problem -> Specific Scientific Gap (what is missing in current literature?) -> Our Solution (The 'Titans' component logic).
> - **Citations**: Ensure that when you mention 'Previous studies have shown...', you explicitly check the uploaded references to ensure the citation actually supports the claim.
> - **Tone**: Authoritative yet humble. Avoid distinct 'selling' language; let the logic sell the work."

### Step 3.3: Discussion (First Paragraph)
>
> **Prompt**: "Rewrite the **first paragraph of the Discussion**.
>
> - **Rule**: Do NOT just repeat the results.
> - **Task**: Synthesize the *meaning* of the results. Start with the 'Headline' finding. Then, immediately connect this finding to the broader 'Biological Vulnerability vs. Symptom-based Prediction' debate found in the literature/references.
> - **Style**: Use 'We show that...' instead of 'The results showed that...'."

## 4. Final Polish

Use the `multi_replace_file_content` tool (via Agent) or manually apply the changes suggested by NotebookLM to your LaTeX/Word source.
