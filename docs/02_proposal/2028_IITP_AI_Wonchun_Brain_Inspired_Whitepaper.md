# 2028 IITP AI 원천 연구개발 기획서 및 아키텍처 백서
## 뇌 구조적 커넥톰 재규격화군 동역학 및 국소 학습 기반 차세대 뉴로모픽 파운데이션 아키텍처 연구

- **과제 기획명**: 2028 IITP AI원천연구개발사업 — 비역전파 국소 동역학 및 구조적 커넥톰 기반 초저전력 지능 아키텍처 개발
- **주관 및 기획 기관**: 서울대학교 산학협력단 / 초연결 뇌지능 연구실 (Transconnectome Consortium)
- **문서 번호**: `IITP-2028-AI-WONCHUN-WP-01`
- **기획 버전**: Version 1.0 (최종 기획본)
- **일자**: 2026년 10월 29일

---

## 1. 추진 배경 및 개요 (Executive Summary)

### 1.1 패러다임 전환: "Outside-In Tabula Rasa"에서 "Inside-Out Brain-Inspired"로
현재 생성형 AI 및 대규모 언어 모델(LLM)을 지배하는 딥러닝 패러다임은 외부 세계의 데이터를 백지 상태(Tabula Rasa)의 인공신경망에 대량 주입하여 전역 역전파(Global Backpropagation Through Time, BPTT)를 통해 가중치를 갱신하는 **"Outside-In (외인성 수동 표상)"** 모델에 갇혀 있다.

그러나 폰 노이만-역전파 기반 심층 신경망은 다음과 같은 5대 근본적 물리적·계산적 한계에 봉착하였다:
1. **역전파 연산 병목 (BPTT Scaling Bottleneck)**: 시간 축 시퀀스 처리를 위해 과거 활성화 텐서를 메모리에 유지해야 하므로, 시퀀스 길이 $T$에 비례하여 $O(T)$의 메모리 폭증과 역방향 그래디언트 소실/폭발이 발생한다.
2. **가중치 전송 문제 (Weight Transport Problem)**: 하위 계층의 가중치 갱신을 위해 상위 계층의 전치 행렬 $W^T$를 정확히 알아야 하는 비물리적 가정이 강제된다.
3. **전역 그래디언트 동기화 잠금 (Global Gradient Locking)**: 순방향 연산이 끝날 때까지 역방향 연산이 대기해야 하고, 전체 계층이 순차적으로 그래디언트를 역전파해야 하므로 비동기 분산 가속이 원천적으로 제한된다.
4. **파괴적 망각 (Catastrophic Forgetting)**: 새로운 데이터 분포 학습 시 기존 지식이 전역 그래디언트에 의해 무차별 덮어씌워지는 안정성-가소성 딜레마(Stability-Plasticity Dilemma)를 해결하지 못한다.
5. **극단적 전력 소모 (Energy Dissipation Crisis)**: 메가와트(MW) 급 하이퍼스케일 데이터센터 전력 소비는 지능 확장의 물리적 한계선에 도달한 반면, 생체 뇌는 불과 20W 내외의 에너지로 평생 학습과 복합 인지 추론을 수행한다.

본 기획 과제는 헝가리-미국 뇌과학자 **죄르지 부자키(György Buzsáki)**의 **"Inside-Out (내인성 자율 동역학)"** 뇌과학 이론과 **제프리 셰인라인(Jeffrey Shainline)**의 **초전도 광전자 신경망(SOENs) 연속 라그랑지안 신경동역학**, 그리고 **드미트리 클로콥스키(Dmitri Chklovskii)**의 **정류 스펙트럼 유닛(ReSU) 비역전파 국소 학습 이론**을 융합한다. 

외부 입력을 수동으로 분류하는 백지 신경망을 탈피하여, **모티프 제약 및 허브 반발(Hub Repulsion) 기반 프랙탈 재규격화군 커넥톰 구조**와 **국소 Hebbian/Anti-Hebbian 최소극대화 동역학**을 결합함으로써, 전역 역전파 없이 지속적으로 환경과 상호작용하는 차세대 두뇌 모사 원천 AI 아키텍처를 창출하고자 한다.

---

## 2. 딥러닝의 핵심 과학적·공학적 한계 분석

```
========================================================================================
                          DEEP LEARNING CRITICAL BOTTLENECK
========================================================================================
1. Weight Transport:       Delta W_l = f(W_{l+1}^T)  ---> Non-local, physically impossible
2. Gradient Locking:       Layer l updates locked until Layer L completes forward & backward
3. BPTT Memory Footprint:  Memory ~ O(T * Layers)   ---> Context length hard-capped
4. Catastrophic Collapse:  Tabula Rasa plasticity   ---> Rapid overwriting of prior skills
5. Energy Catastrophe:     Continuous matrix-MACs   ---> Mega-Watt datacenter footprint
========================================================================================
                                         ||
                               TRANSFORMATION VECTOR
                                         \/
========================================================================================
                     INSIDE-OUT NEUROMORPHIC PARADIGM
========================================================================================
1. Local Minimax Duality:  Delta W ~ y * x^T - W, Delta M ~ y * y^T - M (Purely Local)
2. Asynchronous Streaming: Fast recurrent inference (tau_y) + Slow synaptic update (tau_w)
3. Space-Lag Embedding:    Past vector p_t converts temporal dynamics to spatial similarity
4. Heavy-Tailed Manifold:  Log-normal Oligarchic (Stable) + Precision (Plastic) Reservoir
5. Bounded Dissipation:    Continuous Lagrangian dynamics E = 0.5 * beta * s^2 <= D_max
========================================================================================
```

### 2.1 가중치 전송 및 그래디언트 잠금의 계산 복잡도
인공신경망의 계층 $l$에서 가중치 $W_l \in \mathbb{R}^{d_{l} \times d_{l-1}}$에 대한 역전파 갱신 규칙은:
$$\Delta W_l = -\eta \cdot \mathbf{\delta}_l \mathbf{h}_{l-1}^T$$
여기서 오차 그래디언트 벡터 $\mathbf{\delta}_l$은 상위 계층 $l+1$의 가중치 전치 행렬 $W_{l+1}^T$를 경유하여 재귀적으로 전달된다:
$$\mathbf{\delta}_l = \left( W_{l+1}^T \mathbf{\delta}_{l+1} \right) \odot \sigma'(\mathbf{a}_l)$$
이 수식은 두 가지 치명적 비물리적 제약을 내포한다:
1. 계층 $l$의 시냅스는 상위 계층 $l+1$의 시냅스 연결 강도 $W_{l+1}$의 정확한 전치(Transpose) 값을 실시간으로 물리적으로 전송받아야 한다.
2. 전체 네트워크의 순방향 전파가 완료되어 최종 출력 오차 $\mathbf{\delta}_L$이 계산될 때까지 모든 중간 계층의 가중치 갱신은 정지(Locking)된다.

### 2.2 연속 물리 기판과의 비호환성
생체 뉴런 및 차세대 아날로그/초전도 뉴로모픽 하드웨어는 미분방정식으로 기술되는 연속 시간 물리 매체이다. 폰 노이만 아키텍처의 인위적인 이산 동기화 클록 및 비연속적인 "If-스파이크" 임계값 검사는 하드웨어의 자연스러운 정상 상태 이완(Equilibrium Relaxation)을 단절시키고 과도한 동기화 오버헤드를 유발한다.

---

## 3. 뇌 모사 및 뉴로모픽 핵심 아키텍처 설계 원리

본 과제는 기존 인공지능의 공학적 왜곡을 극복하기 위해 생물학적 뇌의 3대 핵심 작동 원리를 아키텍처의 수학적 토대로 채택한다.

### 3.1 죄르지 부자키(György Buzsáki)의 Inside-Out 인지 아키텍처

#### 1. 관찰자의 부호책 함정(Observer's Codebook Trap) 극복
신경세포는 외부 세계의 물체나 의미를 직접 볼 수 없다. 피질 뉴런이 인지하는 것은 상위 시냅스로부터 전달되는 활동 전위뿐이다. 외부 자극과 뇌 활동을 동시에 관찰하는 실험자가 자의적으로 외부 자극의 라벨을 뇌 활동에 대응시키는 "Outside-In 관찰자의 부호책" 방식은 근본적인 범주 착오이다. 지능은 뇌 내부에서 자생적으로 발생한 자발적 진동 패턴을 행동을 통해 외부 세계와 조율(Calibration)할 때 비로소 발현된다.

#### 2. 사전 구성된 두뇌와 "무의미 사전 (Nonsensical Dictionary)"
생체 뇌는 백지(Tabula Rasa) 상태로 태어나지 않는다. 출생 이전 발생 과정에서 이미 풍부하고 복잡한 시공간적 신경 궤적 풀(Repertoire)이 사전 구성(Preconfigured)된다 (해마의 Pre-play 현상: 동물이 새로운 미로에 들어가기 전에 이미 해당 경로를 표현하는 신경 발화 시퀀스가 자발적으로 발화함; Dragoi & Tonegawa, 2011).
이러한 자생적 시공간 발화 패턴은 일종의 **"무의미 사전(Nonsensical Dictionary)"**으로 작동한다. 학습은 새로운 단어를 백지에 쓰는 것이 아니라, 이미 내재된 신경 궤적 단어 중 외부 환경의 사건과 일치하는 궤적을 **선택(Selection)하고 조율(Matching)**하는 과정이다.

#### 3. 왜도된 로그-정규 분포 (Log-Normal Dynamics): 과두제 회로 vs. 정밀 회로
피질 및 해마의 신경 발화율과 시냅스 연결 강도는 정규분포(가우시안)가 아닌 극단적인 **로그-정규(Log-Normal) 분포**를 따른다 (Buzsáki & Mizuseki, 2014):
- **과두제 회로 (Oligarchic Circuit, 상위 10~20%)**: 발화율이 매우 높고 강하게 결합된 소수의 허브 뉴런 군집. 외부 자극에 대해 즉각적이고 견고한 "최선의 추측(Best-guess)" 일반화 표상을 제공하며, 네트워크의 거시적 안정성을 수호한다.
- **정밀 회로 (Precision Circuit, 하위 80%)**: 평상시 침묵(발화율 < 0.1Hz)하며 약한 시냅스로 결합된 대다수의 가소성 뉴런 군집. 새로운 자극의 미세한 차이를 정밀하게 구별하고 평생 학습을 담당한다.

```
       LOG-NORMAL SYNAPTIC & FIRING DISTRIBUTION
  P(x)
   ^
   |  *  <-- Oligarchic Hubs (Fast generalization, rigid stability)
   |  **
   |  ***
   |  *****
   |  *******
   |  ***************** <-- Precision Reservoir (Silent, highly plastic)
   +---------------------------------------------> x (Firing rate / Synaptic weight)
      0.01      0.1       1.0       10.0    100.0 (Log scale)
```

#### 4. 원인 방전(Corollary Discharge)과 감각 귀환(Reafference)의 의미 접지
내부 신경 궤적이 물리적 의미를 획득하기 위해서는 반드시 운동 작용과 결합되어야 한다:
$$\text{운동 명령 } \mathbf{a}_t \implies \text{원인 방전 (Efference Copy) } \mathbf{c}_t = g(\mathbf{a}_t)$$
운동 피질은 근육으로 명령을 보냄과 동시에 감각 피질로 예측 복사본 $\mathbf{c}_t$를 송신한다. 행동에 의해 환경이 변화하여 감각 입력(감각 귀환 신호 $\mathbf{s}_{t+1}$)이 되돌아오면, 감각 비교기(Comparator)는 원인 방전과 감각 귀환의 불일치를 계산한다:
$$\mathbf{\varepsilon}_t = \mathbf{s}_{t+1} - \mathbf{c}_t$$
이 오차 신호가 최소화되는 닫힌 루프(Closed-loop)를 통해서만 기호와 세계 사이의 **의미 접지(Symbol Grounding)**가 완성된다.

---

### 3.2 제프리 셰인라인(Jeffrey Shainline)의 초전도 광전자 신경망(SOENs) 연속 라그랑지안 신경동역학

#### 1. 연속 라그랑지안 동역학 ($\mathcal{L} = T - V$)
미국 국립표준기술연구원(NIST)의 Shainline 연구팀이 제안한 초전도 광전자 신경망(SOENs)은 조셉슨 접합(Josephson Junction)과 초전도 단일광자 검출기(SNSPD)를 결합하여 물리 법칙 자체가 직접 신경 연산을 수행하도록 설계된다:
$$\mathcal{L} = T(\dot{\mathbf{\phi}}) - V(\mathbf{\phi})$$
- 운동 에너지: $T = \frac{1}{2} C \dot{\phi}^2$ (접합 커패시터 정전 에너지)
- 위치 에너지: $V(\phi) = -E_J \cos(2\pi \phi / \Phi_0) + \frac{1}{2L} (\phi - \phi_{\text{ext}})^2$ (조셉슨 세탁판 퍼텐셜)

레일리 소산 함수 $\mathcal{R} = \frac{1}{2R} \dot{\phi}^2$를 포함한 오일러-라그랑주 운동 방정식은 불연속적인 스파이크 판정 조건문('If' condition) 없이 **완전 연속적이고 미분 가능한 전류/자속 동역학**을 산출한다.

#### 2. 수상돌기 누설 적분기 루프 (Dendritic Leaky-Integrator Loop)
초전도 인덕터 루프 내에서 순환하는 초전류 자속 상태 변수 $s(t)$는 비선형 포화 1계 상미분방정식을 만족한다:
$$\frac{ds}{dt} = \gamma \cdot g(\phi_{\text{in}}, s) - \frac{s}{\tau}$$
- $\gamma$: 광학 검출기로부터의 결합 이득
- $\tau = L/R$: 인덕터-저항 물리적 시상수
- $g(\phi_{\text{in}}, s)$: SQUID 전달 함수에 의해 자연적으로 유도되는 매끄러운 포화 비선형성

#### 3. 물리적 저장 에너지와 기계학습 손실 함수의 동등성
초전도 수상돌기 루프에 저장된 물리적 자기 에너지는:
$$E_{\text{phys}} = \frac{1}{2} L I_{\text{loop}}^2 = \frac{1}{2} \beta s^2$$
이는 예측 부호화 및 신경 유사도 일치(Similarity Matching)에서 최소화하고자 하는 2차 손실 함수와 수학적으로 완전히 일치한다. 하드웨어가 해밀턴의 최소 작용 원리($\delta \int \mathcal{L} dt = 0$)에 따라 물리적으로 에너지를 최소화하는 정상 상태에 도달할 때, **물리 기판 자체가 기계학습 최적화 알고리즘을 즉각 실행**한다.

---

### 3.3 Titans 장기 메모리 및 항체형 항상성 강화학습 (HRRL)

#### 1. Titans: 추론 시점 놀람 기반 신경 메모리 (Learning to Memorize at Test Time)
기존 트랜스포머의 주의집중(Attention) 메커니즘은 문맥 길이에 따라 연산량이 $O(N^2)$으로 증가한다. 본 아키텍처는 Behrouz et al. (2024/2025)의 **Titans 신경 장기 기억 모듈**을 도입하여, 추론 시점(Test Time)에 즉각적인 그래디언트 예측 오차에 기반한 동적 연관 행렬 $M_t$를 갱신한다:
$$M_t = (1 - \alpha_t) M_{t-1} + S_t$$
$$S_t = \eta_t \nabla_{\theta_t} \mathcal{L}_{\text{test}}(x_t)$$
여기서 놀람도(Surprisal) $S_t$는 환경의 예상치 못한 변화율에 비례하며, 불필요한 반복 자극은 망각 인수 $(1 - \alpha_t)$에 의해 소거되어 메모리 오염을 원천 차단한다.

#### 2. 항체형 항상성 강화학습 (Homeostatic Recurrent RL, HRRL)
내부 생리적 상태 벡터 $\mathbf{H}_t \in \mathbb{R}^m$와 항상성 기준점(Setpoint) $\mathbf{H}^*$ 사이의 거리를 구동력(Drive)으로 정의한다 (Keramati & Gutkin, *eLife* 2014, 2025):
$$D(\mathbf{H}_t) = \left( \sum_{i=1}^m |H_i^* - H_{i,t}|^p \right)^{\frac{1}{p}}$$
기본적 1차 보상은 항상성 구동력의 감소량으로 부여된다:
$$R_t^{\text{homeo}} = D(\mathbf{H}_{t-1}) - D(\mathbf{H}_t)$$
환경 자극이 항상성을 위협할 때만 고도의 놀람 신호가 유발되어 Titans 장기 메모리에 기록되며, 일상적 평형 상태에서는 시냅스 가소성 에너지를 보존한다.

---

## 4. 제안하는 원천 핵심 빌딩 블록 (Wonchun Building Blocks)

```
========================================================================================
                          WONCHUN ARCHITECTURE PIPELINE
========================================================================================
Sensory Input Stream x_t  ---> [Past-Lag Buffer: p_t in R^{d * L}]
                                           |
                                           v
[Multi-Scale Fractal Connectome Scaffold] (Song 2005/2006, Milo 2002/2004)
  * Superfamily 2 Motif Profile (cFFL noise filters, iFFL pulse generators, Bi-fans)
  * Hub Repulsion Lateral Mask: M_mask (Disassortativity R(k,k) << 1)
  * Extended Griffiths Criticality (Delta lambda_GP)
                                           |
                                           v
[ReSU Local Learning Engine] (Chklovskii et al. AAAI 2026)
  * Fast Equilibrium:  tau_y * dy/dt = -y + W * p_t - (M (x) M_mask) * y
  * ON/OFF Channel:    y^(ON) = [y^*]_+,  y^(OFF) = [-y^*]_+
  * Slow Plasticity:   Delta W_ij = eta_w * (y_i * p_j - W_ij)    [Hebbian]
                       Delta M_ij = eta_m * (y_i * y_j - M_ij)    [Anti-Hebbian]
                                           |
                                           v
[Action-Perception & Homeostatic Memory] (Buzsáki 2019, Titans + HRRL)
  * Motor Action a_t ---> Efference Copy c_t ---> Grounding Error: eps_t = s_{t+1} - c_t
  * Surprise-Gated Memory: M_t = (1 - alpha_t) M_{t-1} + eta * grad L(x_t)
  * Homeostatic Drive Minimization: R_t = D(H_{t-1}) - D(H_t)
========================================================================================
```

### 4.1 다중 스케일 프랙탈 커넥톰 위상 마스크 ($\mathcal{M}_{\text{mask}}$)
1. **박스 커버링 스케일링**: 미세 피질 칼럼에서 거시 영역으로 이어지는 신경망을 $N_B \sim l_B^{-d_B}$ 지수로 설계하여 계층별 고유 시상수 $\tau(l) = \tau_0 \cdot l_B^{z \cdot l}$를 부여.
2. **허브 반발 제약**: 상호 억제 시냅스 연결 행렬 $M$에 희소 마스크 $\mathcal{M}_{\text{mask}}$를 적용하여 차수 높은 허브 뉴런 간 직접 결합을 엄격히 배제 ($R(k_{hub}, k_{hub}) \ll 1, k_{nn}(k) \sim k^{-\mu}$). 이를 통해 간질 발작형 폭주 발화를 차단하고 넓은 그리피스 상($\Delta \lambda_{GP}$)을 확보.
3. **모티프 서명 준수**: 삼원자 모티프 프로파일 $\vec{SP}$를 Superfamily 2(시냅스 커넥톰 군집)로 보정하여 cFFL(잡음 필터)과 상호 순환 고리(작동 기억 유지)의 최적 균형을 달성.

### 4.2 정류 스펙트럼 유닛 (ReSU) 국소 신경동역학
1. **시공간 지연 임베딩**: 시간 축 정보를 역전파로 풀지 않고, 국소 버퍼 $\mathbf{p}_t = [\mathbf{x}_t^T, \dots, \mathbf{x}_{t-L+1}^T]^T$에 임베딩하여 공간 정준 상관 분석(CCA)으로 변환.
2. **2-시상수 수렴 역학**:
   $$\tau_y \frac{d\mathbf{y}_t}{d\tau} = -\mathbf{y}_t + W \mathbf{p}_t - (M \odot \mathcal{M}_{\text{mask}}) \mathbf{y}_t$$
   $$\mathbf{y}_t^* = \max\left(0, (I + M \odot \mathcal{M}_{\text{mask}})^{-1} W \mathbf{p}_t\right)$$
3. **완전 국소 가소성**:
   $$\Delta W_{ij} = \eta_w \left( y_{i,t}^* p_{j,t} - W_{ij} \right) \quad \text{(시냅스 전후 활성만으로 결정)}$$
   $$\Delta M_{ij} = \eta_m \left( y_{i,t}^* y_{j,t}^* - M_{ij} \right) \odot \mathcal{M}_{\text{mask}} \quad \text{(측두 억제 직교화)}$$

### 4.3 하드웨어-소프트웨어 통합 (Co-Design)
- 미분방정식 수렴 동역학을 초전도 자속 양자 회로 및 차세대 PIM(Processing-In-Memory) 아날로그 저항 변화 메모리(ReRAM) 크로스바 어레이에 1:1 직접 매핑.
- 각 크로스바 교차점에서 국소 전류 승산 및 누설 감쇄가 물리적으로 동시 수행되어 전송 대역폭 병목($O(1)$ 연산)을 완전 해소.

---

## 5. 기대 성과 및 과학기술·경제적 파급 효과

### 5.1 과학기술적 기대 성과
1. **역전파 의존 탈피 및 비역전파 학습 이론 정립**: 1986년 Rumelhart의 역전파 제안 이후 인공지능을 구속해온 가중치 전송 및 그래디언트 잠금 문제를 순수 국소 동역학으로 해결하는 원천 이론 구축.
2. **뇌 구조-기능-물리 삼위일체 융합**: Milo의 모티프, Song의 프랙탈 재규격화군, Chklovskii의 ReSU, Buzsáki의 Inside-Out, Shainline의 SOENs를 단일한 수학적 체계로 통합한 세계 최초의 연구 선도.
3. **차세대 AI 원천 특허 및 글로벌 표준 선점**: 2028년 이후 도래할 뉴로모픽 파운데이션 하드웨어 시장에서 대한민국 원천 기술 IP 확보.

### 5.2 경제·산업적 파급 효과
1. **데이터센터 전력 소모 1,000배 이상 절감**: 초저전력 국소 학습 칩 개발로 기가와트 급 AI 데이터센터의 전력 위기를 획기적으로 완화 (Synaptic event당 $< 10^{-15}\text{ J}$).
2. **엣지 디바이스 평생 온디바이스 학습(Continual On-Device AI) 실현**: 클라우드 통신 및 재학습 인프라 없이도 로봇, 자율주행, 국방, 우주 환경에서 스스로 환경에 적응하며 파괴적 망각 없이 지능을 진화시키는 독립형 뉴로모픽 프로세서 상용화.

---

## 6. 결론

본 2028 IITP AI 원천 연구개발 기획서는 딥러닝의 막다른 골목을 돌파할 진정한 뇌 모사 지능의 수학적 청사진을 제공한다. 구조적 커넥톰의 프랙탈 재규격화군 원리와 비역전파 국소 스펙트럼 학습의 융합은 지능 시스템의 전력 효율과 학습 능력을 생물학적 뇌의 수준으로 격상시키는 결정적 도약대가 될 것이다.
