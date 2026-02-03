# IITP 인공지능 제안서 전체 계획 (2026-014)

## 핵심 전략: "DIVER-Neuro" 파운데이션 모델
우리는 다중감각 데이터(시각, 청각)와 뇌 신호(EEG/iEEG)를 정렬하여 인지의 "Ground Truth"를 학습하는 **뇌-감각 파운데이션 모델**을 구축합니다.
**핵심 전환점**: **Bertram et al. (2026)** ("How ‘Neural’ is a Neural Foundation Model?")을 검증의 이론적 배경으로 삼아 **"Tubularity(관형 구조)"**와 **"Neural Manifold Alignment(신경 다양체 정렬)"**에 집중합니다.

![DIVER-Neuro Overview](../05_figures/diver_neuro_overview.png)
*(그림 1: DIVER-Neuro 아키텍처 및 뇌-디지털 데이터 통합 개념도)*

## 문서 구조 및 상태

## **제1장: 듀얼 인코더 & Titans 통합 아키텍처 (Integrated Architecture)**
-   **핵심 개념**: **"Embodied Neuro-AI Foundation"** (신체화된 뇌-인공지능 파운데이션).
-   **구조**: 외부(Visual/Text), 내부(Brain), 그리고 **신체(Proprioception)** 데이터를 통합하여 **Top-down Attention** 기반의 능동적 추론 수행.

### **1.1. 듀얼 인코더 (Dual Encoders)**
1.  **Sensory-Motor Encoder (감각-운동 정보)**:
    -   **Visual & Text**: ViT/LLM 기반 환경 및 의미 처리.
    -   **Proprioception & Tactile (신규)**: 신체 위치 및 촉각 정보 처리 (RFP-013 필수).
2.  **Brain Spatiotemporal Encoder (뇌 정보)**:
    -   **기술**: **Liquid Time-Constant (LTC) / Neural ODE** (IdeaDeck 핵심).
    -   **역할**: 연속적인(Continuous) 뇌파 동역학을 미분방정식 기반으로 정밀 모델링.

### **1.2. Titans Memory: 선택적 주의와 통합 (The Integrator)**
-   **역할**: **Global Neural Workspace (GNW)** 이론에 기반하여, 목표(Goal)에 관련된 정보만을 **"Selective Attention (선택적 주의)"** 메커니즘으로 선별하여 장기 기억에 저장 (RFP-010/014).
-   **공유 다양체**: 이종(Multimodal) 데이터가 **"Shared Latent Manifold"** 상에서 정렬됨.
-   **시각화**: 아래 그림은 Proprioception이 포함된 확장된 아키텍처를 보여줌.

![Dual Encoders & Titans](../05_figures/dual_encoder_titans_architecture.png)
*(그림 3: 감각-운동-뇌가 통합된 듀얼 인코더 및 Titans 구조)*

### **제2장: 검증 및 방법론 (Validation & Methodology)**
-   **Tubularity & Manifold Alignment**: (유지)

### **제3장: 내수용 감각장 및 알로스태틱 뉴로-트윈 (Allostatic Neuro-Twin)**
-   **핵심**: **Predictive Allostasis (예측적 알로스태시스)**를 통한 시스템 및 인간의 강건성(Robustness) 확보.
-   **전략**: **"Ubiquitous Sensing -> Neural Proxy -> Allostatic Regulation"**
    -   **입력**: 스마트워치/글래스(Passive) + **신체 움직임(Proprioception)**.
    -   **모델**: DIVER-Neuro가 뇌의 **"Energy Landscape"**를 추론.
    -   **개입**: 사용자의 상태가 "Pathological Attractor"로 빠지기 전에, 에이전트가 **"Nudge"**를 통해 에너지 효율적인 최적 상태(Homeostasis)로 복원.
-   **핵심 문헌**:
    -   *JMIR Mental Health (2025)*: Wearable-based Brain State Classification.
    -   *Psychology Today (2025)*: Agentic AI & Allostatic Regulation.
-   **시각화**: 아래 그림과 같이 다중 기기와 신체 신호를 통합한 루프.

![Wellness Agent Loop](../05_figures/wellness_agent_loop.png)
*(그림 2: 예측적 알로스태시스 조절 루프)*

### **제4장: 행동 및 디코딩 (Action & Decoding - 출력)**
-   **핵심**: 로봇 제어 또는 텍스트로의 Neural Decoding
-   **상태**: 계획 중
-   **주요 목표**: "Decoding Manifolds"를 통한 역매핑(Inverse Mapping).

## **5. 참고문헌 (Bibliography)**
1.  **Behrouz, A., Zhong, P. & Mirrokni, V.** Titans: Learning to Memorize at Test Time. *arXiv preprint arXiv:2501.00663* (2024).
2.  **Hasani, R. et al.** Liquid Time-constant Networks. *Proc. AAAI Conf. Artif. Intell.* **35**, 7657-7666 (2021).
3.  **Gu, A., Goel, K. & Ré, C.** Efficiently Modeling Long Sequences with Structured State Spaces. *Int. Conf. Learn. Represent.* (2022).
4.  **Bertram, J. et al.** How ‘Neural’ is a Neural Foundation Model? *arXiv preprint arXiv:2601.21508* (2026).
5.  **Dehaene, S. & Naccache, L.** Toward a cognitive neuroscience of consciousness. *Cognition* **79**, 1-37 (2001).

## **6. 다음 단계 (Student Action Plan)**
### **Phase 1: 이론 학습 (Theoretical Grounding)**
-   **Action**: 위 참고문헌 [1], [2], [4]를 정독하고 "Neural Manifold"와 "Memory Surprise"의 관계를 요약 발제.
-   **Goal**: 아키텍처의 각 블록이 *왜* 필요한지 이해 (예: 왜 LSTM 대신 LTC인가?).

### **Phase 2: 마이크로 구현 (Micro-Scale Replication)**
-   **Action**: `ncps` (Neural Circuit Policies) 라이브러리를 사용하여 간단한 시계열 데이터에 대해 LTC 모델 학습.
-   **Action**: `mamba-ssm` 또는 `s4` 코드를 돌려보며 State Space Model의 긴 시퀀스 처리 능력 확인.

### **Phase 3: 아키텍처 통합 (Macro-Scale Integration)**
-   **Action**: Visual Encoder (ViT)와 Brain Encoder (LTC)의 출력을 Concatenate하여 Titans 메모리에 입력하는 간단한 "Dual Input" 파이프라인 구축.
-   **Goal**: `dual_encoder_titans_architecture`의 축소판(Toy Model) 동작 확인.

### **Phase 4: 제안서 초안 작성 (Drafting)**
-   **Action**: 각 파트별로 할당된 내용을 `docs/03_proposal/drafts/` 폴더에 마크다운으로 작성.
-   **Requirement**: 모든 주장은 위 참고문헌에 근거해야 함.


