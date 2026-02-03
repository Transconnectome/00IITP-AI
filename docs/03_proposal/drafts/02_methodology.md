# 제2장: 검증 및 방법론 (Validation & Methodology)

## 2.1 Tubularity & Manifold Alignment (검증 지표)
본 연구는 AI 모델이 단순한 패턴 매칭을 넘어, 인간 뇌와 유사한 **"Neural Manifold(신경 다양체)"**를 형성하는지 검증하기 위해 Bertram et al.[4]이 제안한 혁신적 지표인 **"Tubularity"**를 도입함.

### 2.1.1 Neural Manifold Alignment
이종(Heterogeneous) 데이터(시각, 언어, 뇌파)가 통합될 때, 각 모달리티의 잠재 공간(Latent Space)이 서로 엉키지 않고 매끄럽게 정렬되어야 강건한 추론이 가능함.
-   **Tubularity Metric**: 학습된 궤적(Trajectory)이 국소적으로 원통형(Tubular) 구조를 유지하는지 측정함. 이는 모델이 노이즈에 얼마나 강건한지(Robustness)를 나타내는 핵심 지표임.
-   **검증 목표**: DIVER-Neuro 모델의 Tubularity Score가 기존 Transformer 기반 모델 대비 30% 이상 향상됨을 입증함.

# 실험 및 검증 방법론 (Methodology)

## 데이터셋 구축 (Dataset Construction)
본 연구는 뇌 활동(Brain)과 외부 환경(Vision)을 동시에 포함하는 멀티모달 데이터셋을 활용함.

### Toy Dataset: Moving MNIST + Synthetic EEG
-   **Visual**: $28 \times 28$ Moving MNIST (2 digits).
-   **Brain (Synthetic)**: 비선형 Izhikevich 뉴런 모델을 사용하여, Visual Stimulus의 속도와 위치에 반응하는 가상의 EEG 생성.
-   **목적**: Dual Encoder의 기본 동작 및 Latent Alignment 검증.

### Main Dataset: BCM-V (Brain-Computer Interface Multimodal Video)
-   **구성**: 피험자가 1인칭 시점(Ego-centric) 영상을 시청할 때 측정된 128채널 EEG 및 Eye-tracking 데이터.
-   **특징**: 자연스러운 환경에서의 시각-뇌 활동 상관관계를 포함.

## 학습 전략 (Training Strategy)

### Phase 1: Pre-training (Brain-Visual Alignment)
-   **Contrastive Learning (CLIP Style)**: OmniField(Visual)와 Brain Encoder(LTC)의 Latent Vector $z_v, z_b$ 간의 코사인 유사도를 최대화함.
-   **Masked Modeling (MAE Style)**: Brain Encoder의 일부 타임스텝을 마스킹하고 복원하도록 학습하여 시간적 문맥(Temporal Context) 학습.

### Phase 2: Titans Memory Integration
-   **Surprise-based Update**: 정렬된 Latent Vector를 Titans에 입력. 예측 오차(Prediction Error)가 높은 "놀라운(Surprising)" 정보만 Long-term Memory에 저장.
-   **Free Energy Minimization**: MIRAS의 **Surprise Metric**은 수학적으로 Friston의 **Free Energy(예측 불확실성)**와 동등함[@friston2010free]. Titans는 이 Free Energy를 최소화하는 방향으로 메모리를 갱신함으로써, 생물학적 항상성(Homeostasis) 원리를 구현함.

### Brain-Tuning: Semantic Alignment
DIVER의 fMRI 데이터를 사용하여 Titans의 상위 레벨 표상을 의미론적으로 정렬합니다 [@benara2025braintuning].

### Biological Validation: Gastric Interoception (Murine Data)
Titans의 기억 메커니즘이 실제 생물학적 회로와 유사하게 작동하는지 검증하기 위해, **김성연 교수팀의 동물 실험 데이터**를 활용합니다 [@kim2020neural].
*   **Data Source**: 생쥐(Mouse)의 **PB Pdyn 뉴런 Two-photon Calcium Imaging** 데이터 (위장 팽창 시의 단일 뉴런 활성).
*   **Hypothesis**: Titans의 **Surprise Metric**은 생쥐의 PB Pdyn 뉴런이 보여주는 **Sustained Activity (Integrator)** 패턴과 높은 상관관계를 보여야 합니다.
*   **Validation**: 위장 팽창(Gastric Distension) 시뮬레이션 환경에서, Titans의 Memory State 변화가 실제 신경 데이터의 역동성과 일치하는지 정량적으로 분석합니다. 이는 AI가 단순한 정보 저장이 아닌, 생체와 유사한 **'내부 상태 적분(Internal State Integration)'**을 수행함을 증명합니다.

## 실험 및 검증 계획 (Validation Plan)
-   **Phase 1**: Toy Dataset(Moving MNIST + Synthetic EEG)을 이용한 개념 증명.
-   **Phase 2**: BCM-V(뇌-컴퓨터 인터페이스) 데이터셋을 활용한 대규모 학습 및 Tubularity 측정.
