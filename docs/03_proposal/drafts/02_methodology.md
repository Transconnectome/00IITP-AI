# 제2장: 검증 및 방법론 (Validation & Methodology)

## 2.1 Tubularity & Manifold Alignment (검증 지표)
본 연구는 AI 모델이 단순한 패턴 매칭을 넘어, 인간 뇌와 유사한 **"Neural Manifold(신경 다양체)"**를 형성하는지 검증하기 위해 Bertram et al.[4]이 제안한 혁신적 지표인 **"Tubularity"**를 도입함.

### 2.1.1 Neural Manifold Alignment
이종(Heterogeneous) 데이터(시각, 언어, 뇌파)가 통합될 때, 각 모달리티의 잠재 공간(Latent Space)이 서로 엉키지 않고 매끄럽게 정렬되어야 강건한 추론이 가능함.
-   **Tubularity Metric**: 학습된 궤적(Trajectory)이 국소적으로 원통형(Tubular) 구조를 유지하는지 측정함. 이는 모델이 노이즈에 얼마나 강건한지(Robustness)를 나타내는 핵심 지표임.
-   **검증 목표**: DIVER-Neuro 모델의 Tubularity Score가 기존 Transformer 기반 모델 대비 30% 이상 향상됨을 입증함.

### 2.1.2 Untangling Fraction
복잡하게 얽힌 뇌 신호 데이터를 모델이 얼마나 효과적으로 풀어서(Untangle) 선형적으로 분리 가능한 상태로 만드는지 평가함.
-   **DiCarlo 방법론 적용**: 영장류 시각 피질 연구(DiCarlo et al.)에서 사용된 Object Manifold Untangling 지표를 AI 모델 평가에 차용함.

## 2.2 Titans Memory Mechanism (메모리 방법론)
장기 의존성(Long-term Dependency) 문제 해결을 위해 Google의 최신 아키텍처인 **Titans**[1]를 본 과제에 맞게 최적화함.

### 2.2.1 Surprise-based Memory Update (MIRAS & Allostasis)
모든 정보를 저장하는 것은 비효율적임. Google Titans의 **MIRAS 프레임워크**를 적용하여 다음 두 가지 원칙에 따라 메모리를 갱신함.
1.  **Surprise Metric vs Free Energy**: MIRAS의 Surprise Metric(예측 오차)은 Friston[@friston2010free]의 **자유 에너지(Free Energy) 최소화** 원리와 수학적으로 동등함. 즉, 모델은 "예측 불가능한(High Surprise)" 정보만을 장기 기억에 저장하여, 미래의 불확실성을 최소화하는 방향으로 학습됨.
2.  **Momentum & Forgetting**: 과거 맥락의 관성(Momentum)을 유지하되, 적응형 감쇠(Adaptive Decay)를 통해 불필요한 정보는망각(Forgetting)하여 메모리 효율을 극대화함.

### 2.2.2 Dual Memory System
-   **Short-term (Core)**: 현재 작업(Task) 수행을 위한 빠른 주의(Attention) 매커니즘.
-   **Long-term (Neural Memory)**: 심층 신경망 가중치(Weights) 형태로 저장되는 암묵적 기억(Implicit Memory). SSM(State Space Model)을 통해 수천 스텝 이전의 정보도 손실 없이 인출함[3].

### 2.3 Brain-Tuning: Semantic Alignment
DIVER의 fMRI 데이터를 사용하여 Titans의 상위 레벨 표상을 의미론적으로 정렬합니다 [@benara2025braintuning].

### 2.4 Biological Validation: Gastric Interoception (Murine Data)
Titans의 기억 메커니즘이 실제 생물학적 회로와 유사하게 작동하는지 검증하기 위해, **김성연 교수팀의 동물 실험 데이터**를 활용합니다 [@kim2020neural].
*   **Data Source**: 생쥐(Mouse)의 **PB Pdyn 뉴런 Two-photon Calcium Imaging** 데이터 (위장 팽창 시의 단일 뉴런 활성).
*   **Hypothesis**: Titans의 **Surprise Metric**은 생쥐의 PB Pdyn 뉴런이 보여주는 **Sustained Activity (Integrator)** 패턴과 높은 상관관계를 보여야 합니다.
*   **Validation**: 위장 팽창(Gastric Distension) 시뮬레이션 환경에서, Titans의 Memory State 변화가 실제 신경 데이터의 역동성과 일치하는지 정량적으로 분석합니다. 이는 AI가 단순한 정보 저장이 아닌, 생체와 유사한 **'내부 상태 적분(Internal State Integration)'**을 수행함을 증명합니다.

## 2.5 실험 및 검증 계획 (Validation Plan)
-   **Phase 1**: Toy Dataset(Moving MNIST + Synthetic EEG)을 이용한 개념 증명.
-   **Phase 2**: BCM-V(뇌-컴퓨터 인터페이스) 데이터셋을 활용한 대규모 학습 및 Tubularity 측정.
