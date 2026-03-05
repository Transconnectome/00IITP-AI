# SOTA Benchmarks (NotebookLM)

## Query 1: Explain the 'Surprise' mechanism in Titans (2025) and how it differs from standard Transformers memory

**NotebookLM Response:**

구글이 2025년 발표한 'Titans' 아키텍처의 '놀라움(Surprise)' 메커니즘은 인간의 뇌가 새로운 정보를 학습하고 기억하는 방식에서 영감을 받은 핵심 기술입니다. 이 메커니즘은 기존 트랜스포머(Transformer)가 겪는 '기억력의 한계'와 '연산 비효율성'을 극복하기 위해 설계되었습니다.

### 1. Titans의 '놀라움(Surprise)' 메커니즘이란?

* **선택적 기억 형성**: 인간은 일상의 모든 순간을 기억하지 않습니다. 대신 예상치 못한 사건이나 기존의 믿음과 불일치하는 정보(즉, '놀라운' 정보)를 만났을 때 이를 강하게 기억합니다. Titans는 이 원리를 차용하여, 매 순간 입력되는 데이터가 현재 모델이 가진 맥락이나 기억과 얼마나 불일치하는지를 측정합니다.
* **Bayesian Surprisal 기반 학습**: 구체적으로는 입력 데이터가 현재의 잠재 상태(Latent State)나 기억을 바탕으로 예측한 결과와 얼마나 다른지를 수학적으로 계산합니다. 예측 오차가 클수록 '놀라움'의 값이 커지며, 이 값이 높은 정보만이 선별적으로 장기 기억 모듈로 전송되어 영구적인 기억(가중치 업데이트 등)으로 남게 됩니다.
* **테스트 타임 학습 (Test Time Training)**: Titans는 학습이 끝난 후 추론(Inference) 단계인 '테스트 타임'에서도 이 메커니즘을 통해 실시간으로 중요한 정보를 선별하여 기억을 업데이트합니다.

### 2. 기존 트랜스포머 메모리와의 차이점

* **메모리 구조**: (Transformer) Attention 기반 KV Cache vs (Titans) 이원화된 메모리 (Short-term + Long-term Neural Memory).
* **정보 처리**: (Transformer) 모든 토큰 O(N^2) 처리 vs (Titans) '놀라움' 기반 선택적(Selective) 처리.
* **확장성**: (Transformer) 길이 제한 vs (Titans) 무한에 가까운 문맥.

---

## Query 2: How does BrainMamba argue for State Space Models (SSM) superiority over Transformers in EEG/neuroimaging tasks?

**NotebookLM Response:**

BrainMamba와 같은 상태 공간 모델(State Space Models, SSM) 기반의 접근법들이 EEG 및 신경영상(Neuroimaging) 작업에서 트랜스포머(Transformer)보다 우월하다고 주장하는 핵심 논거는 **'계산 효율성(Computational Efficiency)'**과 **'장기 시계열 처리 능력(Long-range Modeling)'**에 있습니다.

### 1. 선형 복잡도 vs. 2차 복잡도 (Linear vs. Quadratic Complexity)

* **트랜스포머의 한계**: Self-Attention은 시퀀스 길이의 제곱(O(N^2))에 비례하는 연산량을 가집니다. fMRI나 고해상도 EEG 같은 긴 시퀀스(Long Sequence) 처리 시 메모리 부족 및 병목 현상이 발생합니다.
* **Mamba(SSM)의 우위**: 시퀀스 길이에 대해 **선형적인(O(N)) 시간 복잡도**를 가집니다. 수천~수백만 타임스텝의 긴 뇌신호 데이터를 효율적으로 처리할 수 있습니다.

### 2. 선택적 정보 처리와 노이즈 필터링 (Selectivity & Noise Filtering)

* **선택적 메커니즘 (Selection Mechanism)**: Mamba는 입력 데이터에 따라 파라미터가 변하는 '입력 의존적' 선택 메커니즘을 도입했습니다.
* **노이즈 제거**: 중요한 신경 활동 정보는 기억하고(Remember), 불필요한 노이즈는 동적으로 필터링(Forget)합니다.

### 3. 추론 속도 및 하드웨어 최적화

* **고속 추론**: 추론 시 RNN처럼 이전 상태(State)만을 갱신하며 상수 시간(O(1))에 예측합니다.
* **GPU 효율성**: IO-aware 알고리즘을 사용하여 HBM-SRAM 간 데이터 이동을 최소화합니다.

---

## Query 3: (Agent Synthesis) Defense of LTC vs Mamba for Biological Signals

**Analysis based on Theoretical Properties (LTC vs. Discrete SSMs):**

노트북LM 검색 결과를 보완하기 위해, Agent가 이론적 배경 지식을 바탕으로 LTC(Liquid Time-Constant)의 고유한 장점을 합성하였습니다.

### 1. 연속 시간(Continuous-Time) vs. 이산 시간(Discrete-Time)

* **Mamba (SSM)**: 기본적으로 이산화(Discretization) 단계를 거쳐야 하는 모델입니다. 샘플링 간격이 일정하지 않거나(Irregularly sampled), 데이터가 누락된 경우(Missing values) 정보 손실이 발생할 수 있습니다.
* **LTC (Noble)**: 미분방정식(ODEs)을 기반으로 하여 **시간(Time)**을 연속적인 변수로 다룹니다. 따라서 **비정기적 샘플링(Irregular Sampling)**이 빈번한 생체 신호(Spiking data, EEG events)를 별도의 전처리나 이산화 오차 없이 **'있는 그대로(Natively)'** 처리할 수 있습니다.

### 2. 인과성(Causality)과 해석 가능성(Interpretability)

* **Mamba**: 효율적인 '필터'로서 작동하지만, 내부 상태(State)의 물리적 의미를 해석하기 어렵습니다 (Black-box nature).
* **LTC**: 시냅스 전달 과정(Synaptic Transmission)을 모사하여, 입력 신호에 따라 **시상수(Time Constant, τ)**가 동적으로 변합니다. 이는 신경망이 특정 입력에 *왜* 빠르게 반응했는지, 또는 *왜* 오랫동안 정보를 유지했는지를 생물학적 메커니즘으로 설명할 수 있게 해줍니다. 즉, **"White-box"**에 가까운 인과적 모델링이 가능합니다.

### 3. 결론: 하이브리드 전략의 타당성

* **Local Dynamics (Brain Encoder)**: 미시적인 생체 신호의 불규칙성과 인과성을 포착하기 위해 **LTC**가 필수적입니다.
* **Global Context (Titans Memory)**: 거시적인 장기 문맥과 대규모 데이터 처리를 위해 **Mamba/Titans**의 효율성이 필요합니다.
* 따라서, 두 모델은 경쟁 관계가 아닌 **상호 보완적(Complementary)** 관계입니다.
