# 🧑‍💻 학생 연구원 과제: Toy Model 구현 가이드
**목표**: 제안서 4장(`docs/03_proposal/drafts/04_validation.md`)에 기술된 **"Dual Encoder + Titans Memory"** 아키텍처가 실제로 작동함을 검증하십시오.

## 1. 구현 목표 (Objective)
다음 요소가 포함된 최소 기능 제품(MVP) 형태의 코드를 작성해야 합니다:
1.  **Dual Input (이중 입력)**: 시각 데이터(CNN) + 뇌 신호 데이터(LTC/RNN)를 동시에 처리.
2.  **Memory (기억 모듈)**: **Titans Memory** (또는 유사한 Memory Augmented NN)를 사용하여 과거 정보를 장기 기억.
3.  **Surprise (놀람/예측 오차)**: 새로운 데이터가 들어왔을 때 Prediction Error가 급증하는지 시각화.

## 2. 데이터셋 (Dataset) - 단순화 가능
-   **Visual**: Moving MNIST (인터넷에서 다운로드 가능).
-   **Brain**: Synthetic Data (단순한 Sine Wave + Noise로 대체 가능).
    -   *목표*: 복잡한 실제 뇌파 데이터 대신, 시계열 동역학(Dynamics)을 가진 가상 데이터를 사용해 모델의 학습 능력만 검증하면 됨.

## 3. 아키텍처 예시 (Pseudo Code)
```python
class ToyTitans(nn.Module):
    def __init__(self):
        # 시각 정보 인코더
        self.visual_encoder = Conv2D(...) 
        # 뇌 신호(시계열) 인코더 (Neural ODE 또는 LTC 권장)
        self.brain_encoder = LTC(...) 
        # 핵심: Titans Memory 모듈
        self.memory = TitansMemory(...) 
        
    def forward(self, v, b):
        # 1. 두 정보를 Latent Space로 인코딩
        v_enc = self.visual_encoder(v)
        b_enc = self.brain_encoder(b)
        
        # 2. 결합 (Concatenation)
        z = torch.cat([v_enc, b_enc], dim=1)
        
        # 3. 메모리 업데이트 및 예측
        mem_out = self.memory(z)
        return mem_out
```

## 4. 제출 산출물 (Deliverables)
1.  **작동 가능한 코드**: 이 `src/` 폴더 내에 Python 파일 업로드.
2.  **Loss Curve**: 학습이 진행됨에 따라 Loss가 떨어지는 그래프.
3.  **Surprise Plot**: 학습하지 않은 패턴(Novel Data)이 들어왔을 때, 모델의 **Surprise(Loss)**가 튀는지 보여주는 그래프.

---
**문의**: 이슈가 생기면 PI(교수님) 또는 AI 에이전트(Repo Issues)에 문의하세요.
