# Content Refinement (Camera-Ready)

## 1. Abstract (Rewritten for Impact)

**Current Critique**: Good, but passive. "We present..." is okay, but can be stronger. The logic flow is slightly cluttered.
**Refined Version**:
> **Early detection of youth depression is critical for altering adverse developmental trajectories, yet current predictive markers remain clinically insufficient.** While genetic predispositions and brain structure individually contribute to depression risk, their combined predictive power has remained elusive. **Here, we demonstrate a novel deep learning framework that bridges this gap.** By pretraining a 3D convolutional neural network (CNN) to learn gene–brain associations (using polygenic scores [PGS] and diffusion MRI) in a multi-ethnic cohort (ABCD Study, N=4,741), we successfully transferred this "neurogenetic" knowledge to the task of depression prediction. **Our PGS-pretrained model significantly outperformed** unimodal baselines, improving prediction accuracy by **24% over genetics-only** and **5.8% over imaging-only** models (AUC=0.62–0.66). Notably, the model achieved **cross-ethnic generalization** in an independent Korean cohort (AUC=0.67) and zero-shot prediction of future suicidality. Explainable AI identified the **superior longitudinal fasciculus and cingulum** as key neurogenetic vulnerabilities. These findings establish a scalable, biologically ground framework regarding **"neuroimaging-genomics"** for precision psychiatry.

## 2. Introduction (Funnel Refinement)

**Current Critique**: Paragraph 3 and 4 are a bit repetitive regarding "gaps".
**Refined "Gap" Paragraph**:
> Despite the promise of biological markers, **a critical translational gap remains**: genetic and neuroimaging factors are typically modeled in isolation or as simple linear combinations. This "unimodal silo" approach limits predictive accuracy, as it fails to capture the complex, non-linear latent space where genetic liabilities shape neurodevelopmental architecture. While deep learning offers a solution for multi-modal integration, its application in youth psychiatry is often stifled by the "small data" problem—labeled clinical datasets are rarely large enough to train high-dimensional models from scratch without overfitting.

**Refined "Solution" Paragraph**:
> **To overcome the data scarcity bottleneck, we propose a "Gene-Informed Pretraining" strategy.** Instead of training on depression labels directly (which are scarce), we first train our neural network to solve a "proxy task": mapping brain structure to polygenic risk (which is abundant). This allows the model to learn a **generalizable "neurogenetic foundation"**—a representation of how genetic risk manifests in white matter microstructure—before fine-tuning it for the specific clinical task of depression prediction.

## 3. Discussion (First Paragraph Refinement)

**Current Critique**: Starts with "This study demonstrates..." (generic).
**Refined Version**:
> **We show that the non-linear integration of polygenic risk and white matter microstructure unlocks predictive utility that neither modality possesses alone.** By embedding genetic liability into the representation learning process, our PGS-pretrained framework not only achieved superior classification of youth depression compared to unimodal baselines but also demonstrated **robust cross-ethnic generalizability**. This challenges the prevailing "univariate" view of biomarkers, suggesting that the path from genetic risk to clinical phenotype is mediated by **whole-brain structural configurations**—specifically in the superior longitudinal fasciculus and cingulum—rather than isolated local abnormalities. These findings provide a proof-of-principle for **transfer learning** as a mechanism to scale precision psychiatry models across diverse populations.
