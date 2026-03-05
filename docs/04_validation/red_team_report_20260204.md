# 🕵️‍♂️ Red Team Report: Proposal Validity Check

**Date**: 2026-02-04
**Reviewer**: AI Agent (NotebookLM Integration)
**Target**: `docs/03_proposal/drafts/01_architecture.md`
**Ground Truth**: `docs/04_validation/sota_benchmarks.md` (Titans 2025, BrainMamba 2024, LTC Theory)

---

## 🧐 Executive Summary (요약)

현재 제안서의 아키텍처는 Titans(2025)의 **"Surprise (놀라움)"** 메커니즘을 완벽하게 수용하고 있어 이론적 타당성이 매우 높습니다.
다만, **Brain Encoder**에서 **LTC (Liquid Time-Constant)**만을 강조할 경우, 최신 **BrainMamba (SSM)**의 효율성(O(N)) 주장에 취약할 수 있습니다.
따라서, LTC의 **"연속 시간 인과성(Continuous Causality)"**과 Mamba의 **"장기 시계열 효율성(Long-term Efficiency)"**을 결합한 **하이브리드 전략**으로 논리를 보강해야 합니다.

---

## 🔍 Detailed Analysis (상세 분석)

| Component | Proposal Claim | NotebookLM SOTA Evidence | Verdict |
| :--- | :--- | :--- | :--- |
| **Memory Core** | **"Surprise Metric"**을 이용해 능동적으로 중요 기억을 선별함. | Titans는 **'놀라움(Surprise)'**을 게이트로 사용하여 불일치 정보만 저장함. | ✅ **PERFECT MATCH**<br>Titans의 핵심 철학 관통. |
| **Brain Encoder** | **LTC (Neural ODE)**를 사용하여 불규칙한 시계열과 인과관계를 모델링함. | BrainMamba는 **SSM(Mamba)**의 선형 복잡도(O(N))와 노이즈 필터링이 우월하다고 주장함. | ⚠️ **ATTACK VECTOR**<br>"왜 느린 RNN/ODE를 쓰는가?"라는 공격 가능. |
| **LTC Defense** | (Current Draft: Implicit) | **LTC**는 **비정기적 샘플링(Irregular Sampling)**을 이산화 오차 없이 처리하며, **인과성(Causality)** 설명력이 Mamba보다 우수함. | 🛡️ **DEFENSE FOUND**<br>생체 신호의 본질(Continuous)에 집중해야 함. |

---

## 🛡️ Defense Strategy: The "Hybrid Liquid-SSM" Narrative

단순히 Mamba가 더 좋다는 주장에 맞서지 말고, **역할 분담(Division of Labor)** 논리를 사용하십시오.

1. **Micro-Dynamics (미시적 동역학)**: 개별 뉴런/시냅스 수준의 불규칙한 스파이킹과 인과관계를 해석하기 위해 **LTC**가 필수적임. (Mamba는 이를 이산화하면서 정보를 놓칠 수 있음)
2. **Macro-Context (거시적 문맥)**: 뇌 전체의 장기간(Long-range) 상태 변화를 추적하기 위해 **Titans/Mamba**의 효율성이 필요함.

---

## 🛠️ Actionable Suggestions (수정 제안)

### 1. Brain Encoder 섹션 전면 수정 (Critical)

**[Suggested Rewrite for Overleaf]**
> "본 연구는 생체 신호의 이중적 특성을 반영한 **'Hybrid Liquid-SSM Architecture'**를 제안한다.
>
> 1) **Local Encoder (LTC)**: 불규칙한 샘플링(Irregular Sampling)과 인과적 상호작용(Causal Interaction)이 지배적인 미시적 뇌 신호 처리를 위해, 연속 시간 미분방정식 기반의 **Liquid Time-Constant (LTC) Network**를 적용한다. 이는 기존 이산형(Discrete) 모델인 Transformer나 Mamba가 놓칠 수 있는 미세한 시간적 동역학을 포착한다.
> 2) **Global Memory (Titans/SSM)**: 추출된 로컬 특징들의 장기적 의존성(Long-term Dependency)을 효율적으로 처리하기 위해, 선형 복잡도(O(N))를 가지는 **Titans Memory Module**을 결합하여 계산 효율성과 확장성을 동시에 확보한다."

### 2. "Why Not Just Mamba?" 방어 논리 추가
>
> "BrainMamba[@brainmamba2024] 등 최신 연구가 SSM의 효율성을 입증하였으나, 생물학적 뉴런의 '적응적 시상수(Adaptive Time Constant)'를 통한 **설명 가능한 AI(XAI)** 구현에는 한계가 있다. 본 제안서는 LTC를 통해 이 문제를 해결한다."

---

## 📝 Next Steps for User

1. **Overleaf 수정**: 위 [Suggested Rewrite]를 `sections/01_architecture.tex`에 반영.
2. **용어 통일**: "Liquid-SSM" 또는 "Continuous-Discrete Hybrid" 용어 사용.
