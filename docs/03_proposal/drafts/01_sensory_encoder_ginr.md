# Section 2-1: The "Neuro-GINR" Sensory Encoder (Part 1)

## 1. 기술적 개요: "Liquid Time to Liquid Space-Time"
기존의 **LTC (Liquid Time-Constant)** 네트워크는 시간적(Time) 연속성을 다루는 데 탁월했으나, 공간적(Space) 불변성을 확보하지 못했습니다. 본 연구는 LTC의 개념을 **시공간(Space-Time)**으로 확장하여, 입자 물리학의 **GINR (Geometry-Invariant Neural Representation)** 기술을 뇌과학에 도입합니다. 이를 통해 **"좌표 독립적인(Coordinate-Independent)"** 차세대 센서리 인코더를 제안합니다.

## 2. 핵심 기술: Continuous Neural Field Modeling
- **Universal Field**: 뇌 활동을 이산적인(Discrete) 픽셀이 아닌, 연속적인(Continuous) 함수 $f(x, t)$로 모델링합니다. 이는 **LTC의 시간적 유동성**과 **Neural Field의 공간적 유연성**을 결합한 것입니다.
- **Micro-to-Macro Bridge**: GINR 인코더는 마이크로 스케일의 스파이크(Spike) 데이터와 매크로 스케일의 뇌영상(fMRI) 데이터를 동일한 **"Invariant Latent Manifold"**상에 매핑합니다.
- **Uncertainty-Aware**: 단순히 특징값(Mean)만 추출하는 것이 아니라, 데이터의 신뢰도(Variance, $\sigma^2$)를 함께 추론하여, 후단의 Part 2(GNW)가 "정보의 확실성"에 따라 가중치를 조절할 수 있도록 지원합니다.

## 3. 차별성 (vs 기존 LLM)
- **Robustness**: 기존 LLM이 텍스트(1D) 토큰화에 의존하는 반면, Neuro-GINR은 **"위상학적 불변량(Topological Invariants)"**을 학습하여 센서가 누실되거나(Missing) 위치가 바뀌어도(Shift) 강건한 성능을 유지합니다.
- **Micro-Efficiency**: 모든 데이터를 고밀도로 처리하지 않고, 필요한 시공간 좌표만 선별적으로 쿼리(Query)하여 연산 효율을 극대화하는 **"Sparse Processing"**이 가능합니다. 이는 저전력 엣지 디바이스 탑재(On-Device AI)에 최적화된 특성입니다.
