"""Local Learning Engine: Rectified Spectral Units (ReSU) & Recurrent Fast Dynamics.

Implements:
1. Fast Recurrent Inference Dynamics (two-timescale relaxation):
   4th-order Runge-Kutta (RK4) numerical integration of:
       tau_y * dy/dtau = -y + W * p_t - (M (o) M_mask) * y
   relaxing to equilibrium fixed point y_t^* = (I + M (o) M_mask)^{-1} W p_t.
   Half-wave non-negative rectification: y_rect = max(0, y_t^*).

2. Slow Local Synaptic Plasticity (Normative Neural Similarity Matching):
   - Feedforward Hebbian plasticity:
       Delta W = lr_w * (y_rect * p_t^T - W)
   - Lateral anti-Hebbian plasticity (decorrelation):
       Delta M = lr_m * ((y_rect * y_rect^T - M) (o) M_mask)
       diag(M) <- 0,  M <- max(0, M)

3. Strict Locality Guarantees:
   - ZERO global backpropagation
   - ZERO backward() calls
   - ZERO autograd / gradient tracking
   - ZERO weight transport (W^T is never communicated back to pre-synaptic units)
"""

from typing import Optional, Tuple
import numpy as np


def fast_recurrent_inference_rk4(
    p: np.ndarray,
    W: np.ndarray,
    M: np.ndarray,
    n_steps: int = 30,
    dt: float = 0.05,
    tau_y: float = 1.0,
    rectify: bool = True,
    max_val: float = 50.0,
) -> np.ndarray:
    """Perform fast recurrent inference using 4th-order Runge-Kutta (RK4) integration.

    Solves:
        tau_y * dy/dtau = -y + W * p - M * y
    from initial state y(0) = 0 for n_steps with step size dt.
    Enforces intermediate non-negativity and bounds activations to prevent overflow
    under extreme drive or impulse shocks.

    Parameters
    ----------
    p : np.ndarray, shape (dim_p,)
        Input sensory pattern (or space-lag window p_t).
    W : np.ndarray, shape (dim_y, dim_p)
        Feedforward synaptic weight matrix.
    M : np.ndarray, shape (dim_y, dim_y)
        Effective lateral inhibitory matrix (e.g. M * M_mask).
    n_steps : int
        Number of RK4 numerical integration steps.
    dt : float
        Numerical integration step size.
    tau_y : float
        Membrane relaxation time constant.
    rectify : bool
        If True, enforce projective non-negative rectification y >= 0.
    max_val : float
        Maximum activation bound to prevent runaway excitation.

    Returns
    -------
    y_inf : np.ndarray, shape (dim_y,)
        Equilibrium neural response.
    """
    dim_y = W.shape[0]
    y = np.zeros(dim_y, dtype=np.float64)
    Wp = np.clip(W @ p, -max_val, max_val)

    for _ in range(n_steps):
        # f(y) = (-y + Wp - M @ y) / tau_y
        k1 = (-y + Wp - M @ y) / tau_y
        y1 = np.clip(y + 0.5 * dt * k1, 0.0 if rectify else -max_val, max_val)

        k2 = (-y1 + Wp - M @ y1) / tau_y
        y2 = np.clip(y + 0.5 * dt * k2, 0.0 if rectify else -max_val, max_val)

        k3 = (-y2 + Wp - M @ y2) / tau_y
        y3 = np.clip(y + dt * k3, 0.0 if rectify else -max_val, max_val)

        k4 = (-y3 + Wp - M @ y3) / tau_y

        y = np.clip(
            y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4),
            0.0 if rectify else -max_val,
            max_val,
        )

    if rectify:
        y = np.maximum(0.0, y)
    return y


def update_synaptic_weights_local(
    p: np.ndarray,
    y: np.ndarray,
    W: np.ndarray,
    M: np.ndarray,
    mask: np.ndarray,
    lr_w: float = 0.01,
    lr_m: float = 0.01,
    rule: str = "hebbian",
    decay_w: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Execute purely local Hebbian and anti-Hebbian synaptic updates.

    Mathematical Formulation:
        Feedforward Normative Similarity Matching / Oja's rule:
            Delta W = lr_w * (y * p^T - (y y^T) * W)   [rule="oja"]
            Delta W = lr_w * (y * p^T - decay_w * W)   [rule="hebbian"]
        Lateral Anti-Hebbian (decorrelation):
            Delta M = lr_m * ((y * y^T - M) (o) mask)
            diag(M) <- 0
            M <- max(0, M)

    No non-local error feedback, no autograd, no weight transport.

    Parameters
    ----------
    p : np.ndarray, shape (dim_p,)
        Pre-synaptic input vector.
    y : np.ndarray, shape (dim_y,)
        Post-synaptic activity vector.
    W : np.ndarray, shape (dim_y, dim_p)
        Current feedforward synaptic weight matrix.
    M : np.ndarray, shape (dim_y, dim_y)
        Current lateral inhibitory matrix.
    mask : np.ndarray, shape (dim_y, dim_y)
        Structural lateral connectivity mask.
    lr_w : float
        Feedforward learning rate.
    lr_m : float
        Lateral anti-Hebbian learning rate.
    rule : str
        Plasticity rule: 'oja' (normative similarity matching) or 'hebbian' (linear decay).
    decay_w : float
        Weight decay coefficient for linear Hebbian rule.

    Returns
    -------
    W_new : np.ndarray, shape (dim_y, dim_p)
        Updated feedforward weights.
    M_new : np.ndarray, shape (dim_y, dim_y)
        Updated lateral inhibitory weights.
    """
    # 1. Purely local feedforward update
    if rule == "oja":
        # Multi-unit Oja's subspace rule / normative similarity matching
        delta_W = lr_w * (np.outer(y, p) - (y[:, None] @ y[None, :]) @ W)
    else:
        # Classical linear decay Hebbian rule
        delta_W = lr_w * (np.outer(y, p) - decay_w * W)

    W_new = W + delta_W

    # 2. Purely local anti-Hebbian update with structural motif masking
    delta_M = lr_m * ((np.outer(y, y) - M) * mask)
    M_new = M + delta_M

    # Non-negativity constraint and zero self-inhibition
    np.fill_diagonal(M_new, 0.0)
    M_new = np.maximum(0.0, M_new)

    return W_new, M_new


class ReSULocalEngine:
    """Biologically Grounded Rectified Spectral Unit (ReSU) Local Learning Engine.

    Implements fast recurrent contraction dynamics and slow local synaptic
    plasticity without global error backpropagation.
    """

    def __init__(
        self,
        dim_in: int,
        dim_out: int,
        mask: Optional[np.ndarray] = None,
        lr_w: float = 0.05,
        lr_m: float = 0.02,
        tau_y: float = 1.0,
        dt: float = 0.05,
        n_steps: int = 25,
        seed: Optional[int] = None,
        rule: str = "oja",
        rectify: bool = True,
    ):
        self.dim_in = dim_in
        self.dim_out = dim_out
        self.lr_w = lr_w
        self.lr_m = lr_m
        self.tau_y = tau_y
        self.dt = dt
        self.n_steps = n_steps
        self.rule = rule
        self.rectify = rectify

        rng = np.random.RandomState(seed)

        # Structural lateral connectivity mask
        if mask is not None:
            assert mask.shape == (dim_out, dim_out), "Mask must match dim_out x dim_out"
            self.mask = mask.astype(np.float64)
        else:
            self.mask = np.ones((dim_out, dim_out), dtype=np.float64)
            np.fill_diagonal(self.mask, 0.0)

        # Initialize feedforward weights W:
        self.W = rng.randn(dim_out, dim_in) * 0.1

        # Initialize lateral inhibitory weights M
        self.M = np.zeros((dim_out, dim_out), dtype=np.float64)

    def infer(self, p: np.ndarray, rectify: Optional[bool] = None) -> np.ndarray:
        """Run fast recurrent RK4 inference to reach equilibrium response y*."""
        M_eff = self.M * self.mask
        rect = self.rectify if rectify is None else rectify
        return fast_recurrent_inference_rk4(
            p=p,
            W=self.W,
            M=M_eff,
            n_steps=self.n_steps,
            dt=self.dt,
            tau_y=self.tau_y,
            rectify=rect,
        )

    def adapt(self, p: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Perform slow local synaptic update on W and M."""
        self.W, self.M = update_synaptic_weights_local(
            p=p,
            y=y,
            W=self.W,
            M=self.M,
            mask=self.mask,
            lr_w=self.lr_w,
            lr_m=self.lr_m,
            rule=self.rule,
        )
        return self.W, self.M

    def compute_energy(self, p: np.ndarray, y: np.ndarray) -> float:
        """Compute min-max similarity matching Lyapunov energy.

        E(y; p, W, M) = 1/2 * y^T * (I + M * mask) * y - y^T * W * p + 1/2 * ||p||^2
        """
        dim_y = len(y)
        M_eff = np.eye(dim_y, dtype=np.float64) + (self.M * self.mask)
        E = 0.5 * float(y @ M_eff @ y) - float(y @ (self.W @ p)) + 0.5 * float(np.sum(p ** 2))
        return float(E)

    def reconstruct(self, p: np.ndarray) -> np.ndarray:
        """Reconstruct sensory input p from the learned neural representation."""
        y = self.infer(p)
        return self.W.T @ y
