import torch
import torch.nn as nn
import torch.nn.functional as F

# 🧠 Toy Model for Phase 4: Scientific Validation
# Architecture: Dual Encoder (Visual + Brain) -> Manifold -> Titans Memory

class VisualEncoder(nn.Module):
    """Encodes (B, C, H, W) images into latent vector."""
    def __init__(self, latent_dim=128):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, stride=2, padding=1), # 28 -> 14
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), # 14 -> 7
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, latent_dim)
        )
    def forward(self, x):
        return self.conv(x)

class BrainEncoder(nn.Module):
    """Encodes (B, T, Channels) brain signals into latent vector using RNN/LTC."""
    def __init__(self, input_dim=10, hidden_dim=64, latent_dim=128):
        super().__init__()
        # Using GRU as a proxy for LTC in this toy model
        self.rnn = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.proj = nn.Linear(hidden_dim, latent_dim)
        
    def forward(self, x):
        # x: (B, T, C)
        _, h_n = self.rnn(x) # h_n: (1, B, H)
        return self.proj(h_n.squeeze(0))

class TitansMemory(nn.Module):
    """Simplified Titans Memory Module (Neural Memory)."""
    def __init__(self, dim, memory_size=512):
        super().__init__()
        self.dim = dim
        self.memory_size = memory_size
        
        # Neural Memory (Key-Value Store approximation)
        self.memory_k = nn.Linear(dim, memory_size)
        self.memory_v = nn.Linear(dim, memory_size)
        
        # Gating for Surprise (Forget Gate)
        self.surprise_gate = nn.Sequential(
            nn.Linear(dim, 1),
            nn.Sigmoid()
        )

    def forward(self, z):
        # z: (B, dim) - Combined Latent
        
        # 1. Calc Surprise (Simulation)
        surprise = self.surprise_gate(z) # (B, 1) High = Novel
        
        # 2. Memory Update (Simplified)
        # In real Titans, this involves complex gradients. 
        # Here we just project for demo.
        mem_read = F.relu(self.memory_v(z))
        
        return mem_read, surprise

class EmbodiedNeuroAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.visual = VisualEncoder()
        self.brain = BrainEncoder()
        
        # Shared Latent Manifold Projection
        self.projector = nn.Linear(128*2, 256)
        
        # Core Memory
        self.titans = TitansMemory(256)
        
        # Decoder (Action/Reconstruction)
        self.decoder = nn.Linear(512, 10) # Dummy Output class

    def forward(self, img, brain_sig):
        v_lat = self.visual(img)
        b_lat = self.brain(brain_sig)
        
        # Joint Embedding
        z = torch.cat([v_lat, b_lat], dim=1)
        z = self.projector(z)
        
        # Memory Access
        mem_out, surprise = self.titans(z)
        
        # Final decision
        out = self.decoder(mem_out)
        return out, surprise

if __name__ == "__main__":
    print("🚀 Initializing Toy Model...")
    model = EmbodiedNeuroAI()
    
    # Dummy Data
    img = torch.randn(8, 1, 28, 28) # Fake MNIST
    brain = torch.randn(8, 50, 10)  # Fake EEG (Batch, Time, Chan)
    
    output, surprise = model(img, brain)
    print(f"✅ Output Shape: {output.shape}")
    print(f"✅ Surprise Level: {surprise.mean().item():.4f}")
    print(">> Student Task: Replace Dummy Data with Real Moving MNIST & Train Loop.")
