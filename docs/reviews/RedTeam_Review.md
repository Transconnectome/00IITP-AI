# Red Team Review Simulation

**Target Journal Tier**: Nature Medicine, JAMA Psychiatry, NeurIPS
**Persona**: Senior Reviewer (Methodology & Psychiatric Genomics)

## 🚨 Critical Vulnerabilities (Fatal Flaws)

### 1. The "Robustness" Claim vs. Modest Effect Sizes

- **Critique**: The manuscript repeatedly describes performance as "robust" (Abstract, Intro, Discussion). However, an AUC of **0.62 (cross-sectional)** and **0.61-0.66 (longitudinal)** is locally considered "poor" to "fair" in vigorous machine learning contexts, even if it is "state-of-the-art" for this specific difficult task.
- **The Attack**: "The authors claim 'robust predictive performance,' yet an AUC of 0.62 implies the model has limited clinical sensitivity/specificity. Comparing Cohen's d to ENIGMA (univariate) is valid, but claiming 'high clinical utility' based on these numbers is an overreach."
- **Defense Strategy**:
  - **Retreat**: Downgrade "robust" to "statistically significant and generalizing."
  - **Pivot**: Focus entirely on the **Delta ($\Delta$)**. The absolute AUC (0.62) matters less than the **gain over the baseline** (+24% vs PGS-only, +5.8% vs Brain-only).
  - **Reframe**: Explicitly state that *no current biological marker* exceeds this range for widespread screening, and thus the value is in the *increment* over standard care limits.

### 2. The "Black Box" of Pretraining Specificity

- **Critique**: Why does PGS pretraining work? The paper argues it learns "gene-brain associations." A skeptic would ask: "Did the model just learn to predict age/sex/motion better because PGS is correlated with them?" or "Did it just learn a better denoise filter?"
- **The Attack**: "The specificity of the 'gene-informed' features is unproven. The authors show it beats 'family history' pretraining, but does it beat a simple Autoencoder (unsupervised pretraining)?"
- **Defense Strategy**:
  - If you haven't compared against a standard Autoencoder (reconstruction loss) or Contrastive Learning (SimCLR) baseline, this is a major exposure.
  - **Mitigation (Textual)**: Emphasize the **Interpretability** results (Fig 3). If the saliency maps align with *specific* tracts known to be heritable (SLF, Cingulum), argue that the pretraining learned *biologically relevant* features, not just noise.

### 3. Generalizability Limitations (Korean Cohort)

- **Critique**: The Korean cohort (N=108) is small. The AUC jump to 0.67 could be variance/luck.
- **The Attack**: "The validation sample is too small to claim 'cross-ethnic scalability' definitively. The confidence intervals on that 0.67 are likely huge."
- **Defense Strategy**:
  - **Transparency**: Report confidence intervals (CIs) prominently for the Korean set.
  - **Humble Brag**: "Despite the modest sample size, the *transfer learning* effect (pretraining on US → fine-tuning on KR) showing positive gain is the key finding, irrespective of the absolute AUC."

## 🛡️ Strategic Revisions for Rebuttal/Revision

| Section | Weakness | Suggested Fix |
| :--- | :--- | :--- |
| **Abstract** | "Robust predictive performance" | Change to "Statistically significant improvement over unimodal baselines" |
| **Discussion** | Comparison to ENIGMA (Cohen's d) | Keep this, it's your strongest defense. Expand on *why* multivariate > univariate. |
| **Methods** | Composite PGS construction | Clarify *explicitly* that the pretraining set used to optimize Composite PGS weights was fully disjoint from the fine-tuning set. (You did this, but make it bold). |

## ❓ Anticipated Reviewer Questions

1. "Can you report the False Positive Rate at high sensitivity (e.g., 80%)? An AUC of 0.62 often implies many false alarms."
2. "Did you control for population stratification in the PGS pretraining beyond standard PCs?"
3. "Why did you choose TW-FA specifically? Did you try conventional FA maps?" (Answer: Sensitivity to crossing fibers, cite Calamante 2017 strongly).
