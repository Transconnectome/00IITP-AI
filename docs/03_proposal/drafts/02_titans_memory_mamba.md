# Section 2-2: Titans-Mamba Neural Memory (Part 2)

## 1. 기술적 개요: "Linear Global Workspace"
**Global Neural Workspace (GNW)** 이론은 의식이 정보를 "Broadcasting"한다고 설명하지만, 이를 기존 Transformer($O(N^2)$)로 구현하기에는 계산 복잡도가 너무 높습니다.
본 연구는 **Mamba (SSM, $O(N)$)**를 도입하여, 24시간 동안의 긴 문맥(Context)을 끊김 없이 유지하는 **"Scalable Global Workspace"**를 실제로 구현합니다.

## 2. 핵심 기술: Linear Scaling & Surprisal Gating
- **Titans Backbone (GNW Memory)**: "Titans"는 단기 기억(Mamba)과 장기 기억(Neural Memory)을 결합하여, GNW의 **"Ignition (점화)"** 현상을 공학적으로 모사합니다.
- **Surprisal-Based Update**: Part 1(Neuro-GINR)에서 전달된 예측 오차(Surprisal)가 임계치를 넘을 때만, Mamba의 Hidden State를 장기 기억소에 기록합니다. 이는 불필요한 정보는 버리고 **"Concept-Driven"**하게 중요한 정보만 선택하는 **Selective Attention**의 핵심입니다.

## 3. 통합(Integration) 전략: "Cognitive Economy"
- **Precision-Weighted Fusion**: 시각, 청각, 뇌파 등 이질적인 데이터가 Part 1에서 넘어올 때, 각 데이터의 **신뢰도(Precision, $1/\sigma^2$)**를 가중치로 사용하여 Global Workspace의 상태(State)를 업데이트합니다.
- **Energy-Efficient Computing**: 노이즈가 심하거나 중요도가 낮은 정보는 GNW에 진입하기 전에 필터링(Gating)됨으로써, 불필요한 연산을 방지하고 뇌의 **"에너지 최적화(Metabolic Efficiency)"** 원리를 따릅니다.
