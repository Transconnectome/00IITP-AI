# 📝 Overleaf Revision Action Plan: Hybrid Liquid-SSM Strategy

**Date**: 2026-02-04
**Objective**: Fortify the "Brain Encoder" and "Memory" sections against SOTA critiques (Mamba efficiency) by adopting a specialized Hybrid architecture.

---

## 📍 Action 1: Transform "Brain Encoder" into "Hybrid Liquid-SSM"

**Target File**: `sections/01_architecture.tex` (or `docs/03_proposal/drafts/01_architecture.md`)
**Location**: `### Brain Spatiotemporal Encoder` section

| Current Text (Weakness) | **New Text (Winning Strategy)** | Rationale |
| :--- | :--- | :--- |
| "불규칙하고 연속적인 뇌 신호 처리를 위해 ... **LTC (Neural ODE)**를 도입함." | "본 연구는 생체 신호의 이중적 특성(Micro-Causality vs Macro-Context)을 반영한 **'Hybrid Liquid-SSM Architecture'**를 제안한다.<br><br>1. **Local Micro-Dynamics (LTC)**: 미세한 뉴런 단위의 **불규칙한 스파이킹(Irregular Spiking)**과 **인과성(Causality)**을 보존하기 위해, 이산화 오차가 없는 연속 시간 모델인 **Liquid Time-Constant (LTC) Network**를 적용한다.<br>2. **Global Macro-Dynamics (SSM)**: 뇌 전체의 장기적 상태 변화(Long-range Dependencies)는 선형 복잡도($O(N)$)를 가진 **State Space Model (Mamba)** 메커니즘으로 처리하여 연산 효율성을 극대화한다." | **"Mamba가 더 빠르다"는 공격을 원천 봉쇄.**<br>LTC는 '정확성/인과성'용, SSM은 '효율성/확장성'용으로 역할 분담(Division of Labor)을 명시함. |

---

## 📍 Action 2: Explicitly Claim "Test-Time Training" for Titans

**Location**: `## Titans Memory` $\rightarrow$ `Neural Memory Module` bullet point

| Current Text | **New Text (Add TTT)** | Rationale |
| :--- | :--- | :--- |
| "...단순 저장이 아닌 **"Surprise Metric"**과 **"Momentum"**을 이용해 능동적으로 중요 기억을 선별함." | "...단순 저장이 아닌 **"Surprise Metric"**을 이용해 능동적으로 기억을 선별하며, 특히 학습 종료 후에도 추론 단계에서 실시간으로 학습하는 **Test-Time Training (TTT)**을 수행하여 급변하는 생체 리듬에 즉각 적응함." | Titans 논문의 가장 강력한 차별점인 **TTT**를 명시하여, 정적인(Static) 모델들과의 격차를 벌림. |

---

## 📍 Action 3: Strengthen Conclusion with "XAI" Argument

**Location**: `## 결론 및 차별점`

| Current Text | **New Text (Add XAI)** | Rationale |
| :--- | :--- | :--- |
| "...LTC 기반 생물학적 동역학 모델링과 Titans 기반 능동적 메모리 관리를 결합한..." | "...**LTC의 설명 가능한 인과성(Explainable Causality)**과 **Titans/SSM의 대규모 연산 효율성**을 결합한 **'Hybrid Liquid-SSM'** 아키텍처는..." | 효율성뿐만 아니라 **'설명 가능성(XAI)'**까지 확보했음을 강조하여 심사위원에게 강력한 인상을 남김. |

---

## 🚀 Execution Checklist

1. [ ] Copy the **New Text** from Action 1.
2. [ ] Paste into Overleaf `sections/01_architecture.tex`.
3. [ ] Add Citations: `\cite{brainmamba2024}`, `\cite{titans2025}`.
4. [ ] Verify compilation.
