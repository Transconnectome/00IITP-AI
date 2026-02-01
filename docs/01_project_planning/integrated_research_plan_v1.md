# [NeuroX] Integrated Research Plan: Inside-Out Multisensory Intelligence

## 1. 개요 (Vision)
본 연구 계획은 **Cha Jiook 교수(Scaling & Multimodal SSM)**의 차세대 AI 아키텍처와 **김성연 교수(Neuro-Mechanosensation)**의 내수용감각(Interoception) 연구를 결합하여, 단순히 데이터를 수동적으로 처리하는 인공지능이 아닌, **'생리적 동기(Drive)'와 '신체 감각 통합(Interoceptive Integration)'**을 통해 스스로 의미를 발견하고 행동을 조절하는 **"인사이드-아웃(Inside-Out) 멀티모달 지능"** 개발을 목표로 함.

## 2. 기존 연구와의 정합성 및 시너지 (Synergy Analysis)

### 2.1 Two-Part Model의 확장
현재의 **Sensory Encoder (Part 1) + Titans Memory (Part 2)** 구조를 교수님의 연구 아이디어와 결합하여 **"Three-Part Closing Loop"**로 진화시킴.

| 기존 아키텍처 (NeuroX) | 김성연 교수님 연구 (Interoception) | 통합 전략 (Integrated Plan) |
| :--- | :--- | :--- |
| **Part 1: Sensory Encoder** | Multisensory Data Integration (시각, 청각, 위장 팽창) | **Interoceptive-Modulated Encoder**: 외부 감각뿐만 아니라 위장 팽창과 같은 내부 Valence 신호를 함께 인코딩. |
| **Part 2: Titans Memory** | Slow Integrator / Homeostatic State Tracking | **Drive-Managed Titans Core**: Titans의 Memory 기능을 '항상성 편차(Drive)'에 따라 동적으로 조절하는 핵심 로직 구현. |
| **Output: Action Selection** | Exploration vs. Exploitation Trade-off | **Allostatic AI Loop**: AI가 자신의 에너지 상태(Virtual Stomach)를 고려하여 탐색률을 스스로 결정. |

## 3. 세부 연구 목표 및 로드맵 (Proposed Aims)

### Aim 1: 위장 팽창 신호 기반의 내수용감각 통합 인코더 개발
- **내용**: 시각/청각 신호와 교수님이 제시한 **위장 팽창(Gastric Distension)** 신호를 결합한 멀티모달 임베딩 공간 구축.
- **데이터**: 제공될 2-photon/fiber photometry (NE 신호) 데이터를 'Internal Ground Truth'로 활용하여 AI의 내부 상태 인코딩 성능 검증.

### Aim 2: 항상성 강화학습(HRRL) 기반 Titans Memory SSM 설계
- **내용**: Titans SSM의 히든 스테이트에 'Homeostatic Setpoint' 개념을 도입.
- **혁신성**: 외부 보상이 없어도 'Drive Reduction (불안정성 해소)' 자체가 보상이 되는 **Self-Motivated AI** 구현.

### Aim 3: Reafference(재입력) 기반의 정보 생성 및 근거 확보(Grounding)
- **내용**: 'Inside-Out' 패러다임에 따라, AI가 자신의 Action 출력이 감각 입력(입력의 변화)을 어떻게 바꿀지 예측하는 **Action-Centric Prediction** 수행.
- **검증**: 로봇 제어 또는 가상 환경 에이전트에서 '자기 행동에 의한 감각 변화'를 식별하는 능력 검증.

## 4. AI-CoScientist 활용 전략
- **Evidence Synthesis**: Keramati & Gutkin (2014) 논문과 김성연 교수님 논문의 수치적 모델 정합성 검증.
- **Red Team Review**: "동물의 multisensory 통합 기전이 실제 대규모 파라미터 AI에서도 scaling 될 수 있는지"에 대한 비판적 분석 수행.

---
**[NeuroX]** 본 계획은 "Multisensory Data Integration"이라는 초기 목표를 "Homeostasis-driven Intelligence"로 고도화하여 정부 과제로서의 **창의성 및 도전성**을 극대화함.
