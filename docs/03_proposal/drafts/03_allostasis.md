# 내수용 감각장 및 알로스태틱 뉴로트윈 (Allostatic Neuro-Twin)

## 개요: 예측적 생존 본능 (Predictive Allostasis)
기존의 AI 에이전트나 웰니스 앱은 문제가 발생한 후 반응하는 **Homeostasis(항상성, Reactive)** 모델에 그쳤음. 본 과제는 시스템이 변화하는 미래 환경을 예측하고 사전에 에너지를 조절하는 **Allostasis(알로스태시스, Predictive Regulation)** 개념을 도입하여, 에이전트의 생존성을 극대화함.

![Interoceptive Allostasis vs Homeostasis](../../05_figures/allostasis_vs_homeostasis_diagram.png)

## 시스템 구조: Neuro-Twin Loop
사용자의 신체 및 환경 데이터를 실시간으로 미러링하는 **"Digital Neuro-Twin"**을 구축함.

### Ubiquitous & Visceral Sensing (입력)
-   **Visceral Interoception**: 김성연 교수팀[@kim2020neural]의 연구에 기반하여, 위장 팽창(Gastric Distension)과 같은 내부 장기 신호를 **NTS $\rightarrow$ PVH $\rightarrow$ aIC** 경로를 통해 실시간으로 추적함. 이는 단순한 포만감을 넘어, 에이전트의 **기초 에너지 수준(Basal Energy Level)**을 정의하는 핵심 변수로 작용함.
-   **Passive Sensing**: 스마트워치/글래스 등 웨어러블 기기를 통해 심박 변이도(HRV), 피부 전도도(EDA) 등 자율신경계 신호를 수동적으로 수집함.
-   **Neural Proxy based on Gastric State**: 위장 상태(Gastric State)가 뇌의 각성(Arousal) 및 행동 모드(Exploration vs. Exploitation)를 조절한다는 이론[@berntson2021neural]을 적용하여, 내장 신호로부터 뇌의 거시적 상태를 역추론함.

### Energy Landscape Inference (처리)
뇌 상태를 고차원 **"Energy Landscape(에너지 지형)"** 상의 좌표로 매핑함.
-   **Pathological Attractor**: 우울, 불안, 또는 시스템 과부하 상태를 '빠져나오기 힘든 깊은 골짜기(Attractor)'로 정의함.
-   **Allostatic Load**: 현재 상태가 지속될 경우 시스템에 가해질 누적 부하(Load)를 예측 시뮬레이션함.

### Predictive Nudge (개입)
시스템이나 사용자가 병리적 끌개(Attractor)로 진입하기 전, 선제적으로 개입함.
-   **Intervention**: 조명, 온도 조절 또는 사용자에게 알림(Nudge)을 제공하여, 에너지 지형 상의 '안전 지대'로 궤적을 수정함[Psychology Today 2025].

## 기대 효과
단순한 헬스케어를 넘어, 극한 환경(재난, 우주 등)에서 인간과 AI 시스템의 공생(Symbiosis)을 가능케 하는 **"Energy-Efficient Robust Intelligence"**를 구현함.
