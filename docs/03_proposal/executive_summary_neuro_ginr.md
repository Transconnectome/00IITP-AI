# Executive Summary: "Inside-Out" 뇌 파운데이션 모델 (Neural Memory-Interoception)

## 📌 비전: 신체 감각(Interoception)이 이끄는 능동적 지능 (Inside-Out AI)
본 연구단은 기존 AI가 외부 데이터를 수동적으로 학습하는 **"Outside-In (Stateless)"** 방식의 한계를 극복하고, 생존 본능을 가진 생명체처럼 **'내부 상태(Homeostatic State)'와 '신체적 욕구(IVS)'**를 통해 스스로 정보를 선별하고 학습하는 **"Inside-Out" 패러다임의 차세대 뇌 파운데이션 모델(Neural Memory-Interoception)**을 제안한다.

특히, 김성연 교수팀의 **"위장 팽창(Gastric Distension) 기반 내수용감각 신호"**를 단순한 입력 데이터가 아닌, AI의 **학습 속도와 기억 형성(Consolidation)을 조절하는 핵심 변수(Gating Factor)**로 활용하여 **"스스로 학습의 이유를 아는 AI"**를 구현한다.

---

## 🏗️ 핵심 아키텍처: The "Interoceptive Loop" (Three-Part Model)

우리는 생물학적 뇌의 **"감각-기억-동기"** 루프를 수학적으로 정식화(Operationalize)한 3단계 아키텍처를 제시한다.

### Part 1. Interoceptive Sensory Encoder (Body-Brain Bridge)
> **"Neuro-GINR: 신체와 뇌를 잇는 '연속적 신경장(Continuous Neural Fields)'"**
*   **Core Tech (Neuro-GINR)**: 입자 물리학에서 검증된 **Generalized Implicit Neural Representation (GINR)** 기술을 뇌신경 데이터에 최초로 적용한다.
    *   **연속성(Continuity)**: 뇌 활동을 이산적(Discrete) 토큰이 아닌, 시공간 상의 **연속 함수 $f(x,t)$**로 모델링하여, 서로 다른 해상도(Spike vs fMRI)와 스케일(뇌파 vs 위장 팽창)을 단일한 수학적 공간인 **'Manifold'**에 통합한다.
*   **Interoceptive Embedding**: 이 연속장 위에 **IVS (Interoceptive Valence Signal)**를 추가 차원으로 매핑하여, 외부 감각(Vision)이 내부 상태(Gastric)의 좌표계 내에서 해석되는 **"Context-Dependent Perception"**을 구현한다.

### Part 2. Homeostatic Neural Memory (Continuous State Core)
> **"Transformer는 리셋되지만, 생명은 지속된다. (Life doesn't reset.)"**
*   **Backbone**: 연속적인 시간(Continuous Time)과 상태(State)를 유지할 수 있는 유일한 아키텍처인 **Neural Memory SSM (Mamba-based)**을 채택.
*   **Mechanism**: **항상성 강화학습(HRRL)** 원리를 기억 갱신 공식에 직접 반영. 
    $$
    h_{t+1} = (1 - g_t) h_t + g_t \cdot \text{Input}
    $$
    > ($g_t$: **IVS**에 의해 결정되는 **Neural Gate**. 욕구 해소에 도움이 되는 정보만 $h_t$에 'Lasering' 하여 저장.)

### Part 3. Generative Replay & Allostasis (Sleep & Dream)
> **"꿈(Dream)은 환각이 아니라, 생존을 위한 최적화 과정이다."**

![Figure 1. The Inside-Out Loop: 신체 신호가 뇌(AI)의 기억 Gate를 조절하는 구조](../05_figures/interoceptive_allostasis_diagram.png)
*Figure 1. The Inside-Out Loop: 신체 신호가 뇌(AI)의 기억 Gate를 조절하는 구조*

*   **Generative Replay (SWR)**: 낮(Awake) 동안 수집된 **High-Valence 정보**를 밤(Sleep)이나 휴식기에 **10배속으로 고속 재생(Replay)**하여 재학습. 이는 **Catastrophic Forgetting(망각)**을 방지하는 생물학적 **Continual Learning**의 핵심 기술임.

---

## 🎯 최종 목표: Embodied Brain Foundation Engine
우리는 단순히 '성능 좋은 모델'이 아니라, **"항상성(Homeostasis)을 가진 인공 생명"**의 청사진을 제시한다.

*   **Input**: 멀티모달 뇌파, IVS(위장/혈당), 환경 데이터.
*   **Output**: 내적 동기에 기반한 행동(Action) 및 적응형 인지 상태.
*   **Impact**: 외부 보상 함수 없이도 **"스스로 에너지를 관리하고 생존하는 자율 에이전트"** (Robotics, Autonomous Systems)의 원천 기술 확보.

![Figure 2. Neural Memory-Interoception 아키텍처: Homeostasis가 이끄는 "Inside-Out" 인지 모델](../05_figures/titans_interoception_arch.png)
*Figure 2. Neural Memory-Interoception 아키텍처: Homeostasis가 이끄는 "Inside-Out" 인지 모델*
