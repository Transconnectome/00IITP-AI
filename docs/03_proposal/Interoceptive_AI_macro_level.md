# Active Mamba APC Architecture for EVAAA
**Active Mamba APC Architecture for EVAAA**는 현대 뇌과학의 핵심 이론인 **Active Inference**과 최신 딥러닝 아키텍처인 **Mamba**를 결합하여, 기존 강화학습(RL) 에이전트의 한계를 극복하려는 연구 방향입니다.

---

## 1. Lee et al. (2026) EVAAA의 강화학습 에이전트: 작동 원리와 한계
<img width="1100" height="834" alt="image" src="https://github.com/user-attachments/assets/640e91cd-6e01-47d3-a32e-9f71c75d827c" />

**EVAAA**(**Essential Variables in Autonomous and Adaptive Agents**)는 단순한 점수 획득이 아니라, 생존을 위한 **Homeostasis** 유지를 목표로 하는 가상 환경입니다.

* **작동 원리 (Mechanism):**
* **내부 상태(Interoception):** 에이전트는 시각 정보(Exteroception) 외에 배고픔(Hunger), 목마름(Thirst), 체온(Body Temperature) 등의 **Essential Variables** (EVs)를 관측값(Observation)으로 받습니다.
* **보상 함수(Reward Function):** 기존 RL(PPO, DQN 등)은 에이전트가 생존한 시간(Time steps)에 비례하여 보상을 줍니다. 즉, EVs가 임계값(0)으로 떨어지지 않도록 행동을 학습합니다.
* **동적 환경 적응:** 환경 내 자원(음식, 물)은 고갈되거나 위치가 변하며, 에이전트는 자신의 현재 내부 상태(가장 급한 욕구)에 따라 행동 우선순위를 실시간으로 변경해야 합니다.


* **기존 RL의 한계 (Why Change?):**
* **희소 보상(Sparse Reward):** 생존 보상은 너무 늦게 주어집니다. 예를 들어, 지금 물을 마신 행동이 1000 스텝 뒤의 생존에 기여했다는 인과관계를 기존 RL이 학습하기는 매우 어렵습니다 (Credit Assignment Problem).
* **반응적 행동:** 기존 RL은 현재 상태에 대한 '반응'으로 행동을 매핑합니다. 하지만 생물학적 항상성은 미래의 고갈을 **예측**하고 미리 조절하는 **Allostasis** 능력이 필수적인데, 표준 RL은 이를 구현하기 어렵습니다.



## 2. Rao et al. (2023)의 Active Predictive Coding (APC) 통합: 이유와 방법
<img width="678" height="865" alt="image" src="https://github.com/user-attachments/assets/9f5c1db3-ee01-495d-b973-7efa2c11a97c" />
<img width="807" height="826" alt="image" src="https://github.com/user-attachments/assets/acdfb1ef-b249-4955-a405-6c16db82afdd" />

**APC**를 도입하는 핵심 이유는 에이전트의 목표를 '보상 최대화'에서 **'예측 오차 최소화(Minimizing Prediction Error)'**로 재정의하기 위함입니다. 이는 뇌과학의 **Free Energy Principle**를 구현하는 것입니다.

* **통합의 이유 (Why?):**
* **항상성 = 예측:** 생물에게 "건강한 상태(예: 혈당 100)"는 일종의 강력한 **Prior Belief**입니다. 에이전트가 배가 고파지는 것은 "나는 배가 부르다"는 예측과 실제 감각 입력(배고픔) 사이의 **Prediction Error**가 발생하는 상황입니다.
* **Active Inference:** APC 에이전트는 이 prediction error를 줄이기 위해 두 가지를 할 수 있습니다. (1) 내부 모델을 수정하거나(지각 학습), (2) **행동(Action)을 취해 외부 세계를 변화시켜(음식 섭취)** 감각 입력을 예측(배부름)과 일치시킵니다. 이것이 바로 항상성 유지 행동입니다.


* **통합 방법 (How?):**
* **계층적 계획(Hierarchical Planning):** Rao의 모델처럼 상위 레벨에서는 "갈증 해소"라는 장기 목표(State Prediction)를 생성하고, 하위 레벨에서는 이를 달성하기 위한 구체적인 움직임(Motor Command)을 생성합니다.
* **Hypernetworks (Context Switching):** EVAAA 환경은 상황(Context)이 급변합니다. 배고플 때와 추울 때의 행동 전략은 완전히 달라야 합니다. APC의 **하이퍼네트워크Hypernetwork**는 현재의 내부 상태(Interoception)에 따라 에이전트의 "뇌(신경망 가중치)"를 동적으로 재구성하여 즉각적인 태세 전환(Mode Switching)을 가능하게 합니다.



## 3. RNN 대신 Mamba 알고리즘 사용: 이유와 방법

Rao et al. (2023)의 원본 모델은 RNN을 사용하지만, **Mamba**로 교체하는 것은 생리학적 데이터 처리에 있어 결정적인 이점을 제공합니다.

* **교체 이유 (Why Mamba?):**
* **장기 의존성(Long-term Dependencies):** 생리학적 신호는 타임스케일이 깁니다. 지금 먹은 음식이 혈당에 영향을 주기까지는 시간이 걸리며, 에이전트는 수천 스텝 전의 행동 결과를 기억해야 합니다. RNN은 시간이 지날수록 정보를 잊어버리는(Vanishing Gradient) 반면, Mamba는 선형 시간 복잡도로 무한에 가까운 컨텍스트를 효율적으로 유지합니다.
* **선택적 정보 처리(Selectivity):** 신체 신호에는 노이즈(심박 변이 등)가 많습니다. Mamba의 **Selection Mechanism**은 입력에 따라 정보를 "기억할지" 혹은 "망각할지"를 동적으로 결정하므로, 중요한 생체 신호 변화는 포착하고 노이즈는 무시하는 데 탁월합니다.


* **구현 방법 (How?):**
* APC의 상태 전이 함수()와 행동 정책 함수()를 기존 RNN 셀에서 **Mamba Block**으로 대체합니다.
* 특히 **하이퍼네트워크**가 Mamba의 핵심 파라미터인 **(Discretization step),** 행렬을 직접 변조(Modulation)하도록 설계하여, 내부 상태의 급격한 변화(예: 갑작스러운 통증)에 민감하게 반응하도록 만듭니다.



## 4. EVAAA RL Agent with Active Mamba APC Architecture: 작동 메커니즘

최종적으로 제안하는 **Active Mamba APC 에이전트**는 다음과 같은 루프를 통해 작동합니다.
<img width="800" height="437" alt="image" src="https://github.com/user-attachments/assets/57e6a5c3-9eb3-403a-a571-0b1a6939b23b" />

1. **다중 감각 통합 (Sensory Fusion):**
* Unity 3D 화면(시각)과 Essential Variables(내부 감각)이 **Multi-modal Encoder**를 통해 하나의 잠재 상태 벡터(Latent State)로 통합됩니다.


2. **계층적 Mamba 월드 모델 (Hierarchical World Model):**
* **하위 레벨 (Somatic Mamba):** 빠른 감각-운동 역학을 예측합니다 (예: "앞으로 가면 벽에 부딪힌다").
* **상위 레벨 (Visceral Mamba):** 느린 생리학적 변화를 예측합니다 (예: "이 속도로 달리면 5분 뒤에 탈진한다"). Mamba의 긴 메모리가 여기서 빛을 발합니다.


3. **하이퍼네트워크에 의한 컨텍스트 조절 (Allostatic Control):**
* 현재 내부 상태(예: 갈증 심각)가 감지되면, 하이퍼네트워크가 상위 레벨 Mamba의 파라미터를 조절하여 "물 찾기"와 관련된 기억과 예측을 강화합니다 (Attention Modulation).


4. **능동적 추론 및 행동 (Active Inference):**
* 에이전트는 단순히 보상을 쫓는 것이 아니라, "나의 미래 상태는 건강하다(EVs = 100%)"라는 사전 믿음(Prior)을 가지고 있습니다.
* 현재 상태와의 괴리(예: 현재 수분 = 20%)가 발생하면 거대한 예측 오차(Free Energy)가 발생합니다.
* 에이전트는 시뮬레이션(Planning)을 통해 이 오차를 가장 빠르게 줄일 수 있는 행동 시퀀스(물가로 이동 -> 마시기)를 선택하고 실행합니다.


이 아키텍처는 생물학적 뇌의 작동 방식(Predictive Processing)을 수학적으로 가장 정교하게 모사한 모델이 될 것이며, EVAAA와 같은 복잡한 생존 환경에서 기존 RL을 능가하는 적응력과 견고함을 보여줄 것입니다.


## References
* Rao, R. P. N., Gklezakos, D. C., & Sathish, V. (2023). Active Predictive Coding: A Unifying Neural Model for Active Perception, Compositional Learning, and Hierarchical Planning. _Neural Computation_, 36(1), 1–32. DOI:10.1162/neco_a_01627 https://doi.org/10.1162/neco_a_01563
* Lee, S., Lee, J., Kim, S., Yoon, H., Park, S., Park, J., Bae, J., Hong, S.-J., & Woo, C.-W. (2026). EVAAA: A Virtual Environment Platform for Essential Variables in Autonomous and Adaptive Agents. _The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track._
