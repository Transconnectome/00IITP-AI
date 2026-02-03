# 제1장: 듀얼 인코더 & Titans 통합 아키텍처 (Embodied Neuro-AI Architecture)

## 1.1 개요: 신체화된 신경 인공지능 (Embodied Neuro-AI)
본 제안서는 인간의 인지 과정이 뇌 내부 연산뿐만 아니라 신체(Body)와 환경(Environment)의 상호작용 속에서 발현된다는 **"Embodied AI"** 철학을 따름. 시각/청각 등 외부 감각(External Sense)과 뇌파/고유감각 등 내부 신호(Internal Signal)를 통합하여, 인간 수준의 적응성과 강건성을 갖춘 **"DIVER-Neuro 파운데이션 모델"**을 제안함.

![Dual Encoder Titans Architecture](../../05_figures/dual_encoder_titans_architecture.png)

## 1.2 듀얼 인코더 시스템 (Dual Encoders)
서로 다른 물리적 특성을 가진 두 가지 데이터 스트림 처리를 위해 특화된 **Dual Encoder** 구조를 채택함.

### 1.2.1 Sensory-Motor & Interoceptive Encoder (OmniField)
**OmniField** [@valencia2025omnifield]는 시각/청각뿐만 아니라 **내수용 감각(Interoception)** 신호를 통합하는 4D Neural Field입니다.
*   **External**: Camera(Ego-centric), Mic(Audio)의 비정형 데이터를 처리함.
*   **Internal (Allostasis)**: 위장 팽창(Gastric Distension)과 같은 생체 신호를 연속적인 **내부 상태 변수(Internal State Variable)**로 인코딩합니다.
    *   **Biological Grounding**: 김성연 교수팀[@kim2020neural]의 연구에 기반하여, **NTS $\rightarrow$ PVH $\rightarrow$ aIC** 신경 회로를 모사합니다. 위장 팽창 신호를 단순 자극이 아닌 '적분형(Slow Integrator)' 정보로 처리하여 행동 모드(Exploration vs. Exploitation) 전환의 기준점으로 삼습니다.
*   **Latent Sampler**: 연속적인 OmniField의 출력을 Titans가 처리 가능한 토큰($z_t$)으로 변환하기 위해, **좌표 기반 샘플링(Coordinate Sampling)** 층을 둠. 이 과정에서 Han et al.[@han2024simulated]의 **Simulated Annealing** 기법을 초기화 단계에 적용하여, 최적의 특징점(Feature Points)을 포착하고 Local Minima를 방지함.

### 1.2.2 Brain Spatiotemporal Encoder (뇌 시공간 인코더)
뇌 활동(EEG/iEEG)의 복잡한 시공간적 동역학(Spatiotemporal Dynamics)을 모델링함.
-   **Liquid Time-Constant (LTC) Networks**: 불규칙하고 연속적인 뇌 신호 처리를 위해, 입력에 따라 유동적으로 변하는 **Time-constant**를 가진 미분방정식 기반 **LTC (Neural ODE)**를 도입함[2].
-   **장점**: 노이즈가 많은 생체 신호 처리 시 기존 RNN/LSTM 대비 월등한 강건성을 보이며, 인과관계(Causality) 추론에 유리함.

## 1.3 Titans Memory: 통합과 선택적 주의 (The Integrator)
이종(Heterogeneous) 표상은 **Titans Memory Core**에서 통합됨.
-   **Neural Memory Module (MIRAS Framework)**: Google의 최신 **MIRAS (Memory as Context)** 프레임워크[@behrens2025titans]에 기반하여, 단순 저장이 아닌 **"Surprise Metric (놀라움 척도)"**과 **"Momentum (관성)"**을 이용해 능동적으로 중요 기억을 선별함.
-   **Global Neural Workspace (GNW)**: Dehaene 등[5]의 GNW 이론에 따라, Titans는 감각/뇌 정보가 경쟁·통합되는 "의식적 작업 공간" 역할을 수행함.
-   **Graph-Informed Reasoning**: Moontae Lee(LG AI Research) 심층 추론 방법론[@lee2024strategic]을 적용, Titans 메모리에 저장된 에피소드들을 그래프 구조로 연결하여 단순 회상(Recall)을 넘어선 **전략적 추론(Strategic Reasoning)**을 수행함.
-   **Tubular Manifold Alignment**: 통합 과정에서 모델은 Bertram 등[4]의 **"Tubularity(관형 구조)"**를 유지하도록 학습되어 강건성을 확보함.

## 1.4 결론 및 차별점
본 아키텍처는 단순 멀티모달 결합(Early Fusion)을 넘어, **LTC 기반 생물학적 동역학 모델링**과 **Titans 기반 능동적 메모리 관리**를 결합한 세계 최초 시도임. 이를 통해 IITP RFP가 요구하는 "인간 수준 인지 능력을 갖춘 뇌 내재화 모델"을 실현함.
