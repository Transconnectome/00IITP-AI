# 🧑‍💻 Student Task: Toy Model Implementation
**Goal**: Verify the "Dual Encoder + Titans Memory" architecture described in `docs/03_proposal/drafts/04_validation.md`.

## 1. Objective
Implement a minimal working example (Toy Model) that demonstrates:
1.  **Dual Input**: Visual (CNN) + Brain (LTC/RNN) inputs.
2.  **Memory**: Integration via a Memory Module (Simulated Titans or LSTM).
3.  **Surprise**: Detection of "novel" inputs (High prediction error).

## 2. Dataset (Simple)
-   **Visual**: Moving MNIST (Download from internet).
-   **Brain**: Synthetic Time-series (Sine wave with noise is fine for now).

## 3. Architecture
```python
class ToyTitans(nn.Module):
    def __init__(self):
        self.visual_encoder = Conv2D(...)
        self.brain_encoder = LTC(...) # or GRU
        self.memory = TitansMemory(...) # Key Component
        
    def forward(self, v, b):
        # Concatenate encoded features
        z = torch.cat([v_enc, b_enc], dim=1)
        # Update memory
        mem_out = self.memory(z)
        return mem_out
```

## 4. Deliverables
-   Complete this `src/` folder with working PyTorch code.
-   Generate a `loss_curve.png` showing convergence.
-   Generate a `surprise_plot.png` showing memory activation on novel data.
