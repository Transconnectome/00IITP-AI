# 이메일 분석 기반 제안서 전략 및 인사이트 (2026.01.28)

**분석 대상**: `email1.pdf` ~ `email4.pdf` (홍석준 교수님 및 참여 연구진 간 서신)

---

## 1. 프로젝트 개요 및 핵심 전략

- **과제명**: 인간 인지 기반 인공지능 (Robust and Efficient Multisensory Integrated Intelligence)
- **핵심 목표**: 다중 감각(Multisensory)을 효율적으로 통합하고 처리하는 강건한 AI 모델 개발
- **기술적 아키텍처 (The "Two-Part" Model)**
    1. **Part 1: 단일 감각 처리 (Sensory Encoder)**
        - 알고리즘: Predictive Coding, Clockwork VAE, JEPA (Joint Embedding Predictive Architecture)
        - 특징: Top-down context 전달이 가능한 Encoder-Decoder 구조
    2. **Part 2: 다중 감각 통합 및 메모리 (Integration & Memory)**
        - **핵심 모델: Titans (Neural Memory)**
        - 구조: Bayesian Surprisal 기반 장/단기 기억 State Space Model (SSM)
        - 원리: 예측 불가능한(Surprisal 높은) 정보는 장기 기억으로, 예측 가능한 정보는 망각.

---

## 2. 교수님별 R&R (Role & Responsibilities)

### 🎯 차지욱 (User) & 김병훈 교수님

- **핵심 역할**: **Multimodal SSM의 대규모화 (Scaling) 및 확장**
- **세부 주제**:
  - Vision, Language, Action을 아우르는 Multimodal SSM 연구
  - 기존 수행하던 Large Brain Model / Foundation Model 연구를 SSM 기반으로 확장
- **Action Item**: 기존 연구 방향(대규모 모델링)을 유지하되, **Titans / SSM** 키워드와의 연계성 강조 필요.

### 🧪 실험 및 데이터 수집 (Data Providers)

| 연구자 | 감각 모달리티 | 뇌 영역 / 대상 | 비고 |
| :--- | :--- | :--- | :--- |
| **이준열** | 시각(Visual) + 청각(Audio) | 인간 / 영장류 | 통합 기전 모델링(Precision/Reliability based Weighted Sum) 검증 |
| **손한샘** | 시각 + ? | 설치류 | 데이터를 기반으로 홍석준 교수와 계산 모델링(Fitting) 수행 |
| **김성연** | 후각 + 촉각 (공격행동)<br>내수용 + 고유감각 (삼킴/갈증) | 시상하부 (Hypothalamus) 등 | 스트레스 지속 상태(Recurrent Excitatory Circuit) 모델링 제안됨 |
| **최명환** | 외부 후각 + 내부 후각 (Taste/Smell) | Mediodorsal Thalamus, Insular | 미각-후각-호흡 통합 기전 |
| **유승범** | 시청각 or 시각-촉각 | 인간 SEEG | Multimodal SSM 연계 |

### 🧠 모델링 및 심리학적 검증

- **홍석준 (PI)**: 전체 아키텍처(Titans) 설계, Memory Model 총괄
- **강민석**: Titans 모델(Surprise 기반 망각/기억)의 **심리학적 타당성 검증** 및 개선점 도출

### ⚙️ 응용 및 검증 (Application)

- **ETRI (김성환, 원희선)**: 시뮬레이션-실제 환경(Sim-to-Real) 검증, 로봇 팔/드론 제어 응용. (모델 학습보다는 활용에 초점)
- **뇌연구원 (김기범)**: 1/28(수) 오전 중 역할 확정 예정.

---

## 3. 일정 및 마일스톤

- **전체 미팅**: **2026년 1월 28일 (수) 오후 8:00 (오늘 밤)**
- **장소**: Zoom (링크 이메일 참조)
- **Job Description 배포**: 1/27(화) 배포됨. 각 연구자별 할당된 주제 확인 및 회신 필요.

## 4. 차지욱 교수님을 위한 제언 (Insight)

1. **연구의 연속성**: 홍석준 교수님은 차교수님이 **"기존 연구(대규모 모델)"를 크게 바꾸지 않고** 참여하기를 원함. 즉, 새로운 실험을 기획하기보다 **Existing Large Models를 SSM/Titans 프레임워크로 해석하거나 확장**하는 제안이 유리함.
2. **핵심 키워드 장착**: 제안서 작성 시 **"Titans"**, **"State Space Model (SSM)"**, **"Bayesian Surprisal"** 용어를 적극 차용하여 본인의 대규모 모델링 기술과 연결해야 함.
3. **오늘 미팅 준비**: 오늘 밤 8시 미팅에서 "Vision-Language-Action을 통합하는 Large-scale SSM"에 대한 대략적인 구상을 공유할 준비 필요.
