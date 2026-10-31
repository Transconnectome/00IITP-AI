"""Unit Tests for Milestone M4: Connectome Dynamics & Local Learning Pilot Simulation.

Verifies:
1. Connectome motif topology generation and hub repulsion lateral mask properties.
2. 4th-order Runge-Kutta (RK4) fast recurrent inference stability & non-negativity.
3. Purely local Hebbian & anti-Hebbian synaptic weight plasticity updates.
4. Static AST audit strictly asserting complete absence of autograd & backward() calls.
5. End-to-end convergence: subspace alignment >= 0.85, reconstruction error < 0.25,
   Lyapunov energy descent (energy_drift < 0.0), and zero backprop usage.
"""

import ast
from pathlib import Path
import pytest
import numpy as np

from src.connectome_topology import (
    build_connectome_topology,
    generate_motif_lateral_mask,
    detect_motifs,
    compute_hub_repulsion_ratio,
)
from src.local_learning_engine import (
    fast_recurrent_inference_rk4,
    update_synaptic_weights_local,
    ReSULocalEngine,
)
from src.pilot_local_learning_connectome import (
    generate_spatiotemporal_stream,
    run_simulation,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"


class TestConnectomeTopology:
    """Unit tests for structural motifs and hub repulsion lateral masks."""

    def test_build_topology_mask_shape_and_zero_diagonal(self):
        n_nodes = 20
        graph, mask = build_connectome_topology(n_nodes=n_nodes, seed=42)

        assert mask.shape == (n_nodes, n_nodes)
        assert np.all(np.diag(mask) == 0.0), "Diagonal of lateral mask must be strictly zero (no self-inhibition)"
        assert np.all((mask == 0.0) | (mask == 1.0)), "Mask entries must be binary {0, 1}"
        assert graph.number_of_nodes() == n_nodes

    def test_generate_motif_lateral_mask_direct_call(self):
        n_units = 16
        mask = generate_motif_lateral_mask(num_units=n_units, motif_type="bifan_hub_repelling", seed=123)

        assert mask.shape == (n_units, n_units)
        assert np.all(np.diag(mask) == 0.0)
        assert np.sum(mask) > 0, "Lateral mask must contain active inhibitory connections"

    def test_motif_detection_counts(self):
        graph, _ = build_connectome_topology(n_nodes=24, seed=303)
        motifs = detect_motifs(graph)

        assert "feedforward_loops" in motifs
        assert "bifan_motifs" in motifs
        assert motifs["feedforward_loops"] > 0, "Graph must embed feedforward loops (Triad 38)"
        assert motifs["bifan_motifs"] > 0, "Graph must embed bi-fan motifs"

    def test_hub_repulsion_disassortativity_property(self):
        graph, mask = build_connectome_topology(n_nodes=20, hub_repulsion=True, seed=42)
        hubs = graph.graph.get("hub_nodes", [0, 1, 2, 3])

        # In hub-repelling networks, top hubs must not connect mutually
        for h1 in hubs:
            for h2 in hubs:
                if h1 != h2:
                    assert not graph.has_edge(h1, h2), f"Hub edge ({h1}, {h2}) violates hub repulsion!"
                    assert mask[h1, h2] == 0.0, f"Lateral mask ({h1}, {h2}) violates hub repulsion!"


class TestLocalLearningEngine:
    """Unit tests for RK4 fast inference and local Hebbian/anti-Hebbian plasticity."""

    def test_rk4_fast_relaxation_stability_and_non_negativity(self):
        dim_p = 10
        dim_y = 6
        p = np.random.randn(dim_p)
        W = np.random.randn(dim_y, dim_p) * 0.1
        M = np.eye(dim_y) * 0.3
        np.fill_diagonal(M, 0.0)

        y = fast_recurrent_inference_rk4(p=p, W=W, M=M, n_steps=30, dt=0.05)

        assert not np.isnan(y).any(), "RK4 fast inference produced NaN values"
        assert not np.isinf(y).any(), "RK4 fast inference produced Inf values"
        assert np.all(y >= 0.0), "Rectified Spectral Unit must satisfy non-negativity constraint y >= 0"

    def test_rk4_persistence_under_strong_drive(self):
        dim_p = 8
        dim_y = 12
        p = np.ones(dim_p) * 5.0  # High drive
        W = np.random.randn(dim_y, dim_p) * 0.1
        mask = np.ones((dim_y, dim_y))
        np.fill_diagonal(mask, 0.0)
        M = (np.eye(dim_y) + 0.2 * np.random.rand(dim_y, dim_y)) * mask

        y = fast_recurrent_inference_rk4(p=p, W=W, M=M, n_steps=50, dt=0.02)

        assert not np.isnan(y).any()
        assert not np.isinf(y).any()
        assert np.max(y) < 50.0, f"Runaway excitation detected: max={np.max(y)}"

    def test_local_synaptic_weight_update_exact_formula(self):
        dim_p = 8
        dim_y = 4
        p = np.random.randn(dim_p)
        y = np.maximum(0.0, np.random.randn(dim_y))
        W = np.random.randn(dim_y, dim_p) * 0.1
        M = np.eye(dim_y) * 0.2
        np.fill_diagonal(M, 0.0)
        mask = np.ones((dim_y, dim_y))
        np.fill_diagonal(mask, 0.0)

        lr_w = 0.05
        lr_m = 0.02

        W_new, M_new = update_synaptic_weights_local(
            p=p, y=y, W=W, M=M, mask=mask, lr_w=lr_w, lr_m=lr_m
        )

        expected_delta_W = lr_w * (np.outer(y, p) - W)
        actual_delta_W = W_new - W
        np.testing.assert_allclose(actual_delta_W, expected_delta_W, rtol=1e-5, atol=1e-6)

        assert np.all(np.diag(M_new) == 0.0), "M_new diagonal must remain 0"
        assert np.all(M_new >= 0.0), "M_new entries must be non-negative"

    def test_resu_local_engine_class_methods(self):
        engine = ReSULocalEngine(dim_in=12, dim_out=6, seed=42)
        rng = np.random.RandomState(42)
        p = rng.randn(12)

        y = engine.infer(p)
        assert y.shape == (6,)
        assert np.all(y >= 0.0)

        E = engine.compute_energy(p, y)
        assert isinstance(E, float)
        assert not np.isnan(E)

        W_old = engine.W.copy()
        engine.adapt(p, y)
        assert not np.allclose(engine.W, W_old), "Weights should update after adapt()"

        p_rec = engine.reconstruct(p)
        assert p_rec.shape == (12,)
        assert not np.isnan(p_rec).any()


class TestStaticASTNonBackpropagation:
    """Static AST audit asserting complete absence of autograd / backpropagation calls."""

    def test_forbid_backward_and_autograd_in_src(self):
        py_files = list(SRC_DIR.glob("*.py"))
        assert len(py_files) > 0, "src directory must contain Python files"

        for py_file in py_files:
            if py_file.name in ("titans_demo.py", "rg_box_pooling.py"):
                continue

            code = py_file.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=str(py_file))

            for node in ast.walk(tree):
                # Assert no call to backward()
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and node.func.attr == "backward":
                        pytest.fail(f"Illegal backward() call in {py_file.name} line {node.lineno}")
                    if isinstance(node.func, ast.Attribute) and node.func.attr == "grad":
                        if isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "autograd":
                            pytest.fail(f"Illegal torch.autograd.grad in {py_file.name} line {node.lineno}")

                # Assert no import of torch.autograd
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert "torch" not in alias.name, f"Illegal torch import in {py_file.name}"
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        assert "torch" not in node.module, f"Illegal torch import in {py_file.name}"


class TestConvergenceAndMetrics:
    """End-to-end convergence and quantitative contract validation."""

    def test_simulation_convergence_contract_thresholds(self):
        results = run_simulation(steps=500, seed=42)

        assert results["global_backprop_used"] is False
        assert results["subspace_alignment"] >= 0.85, (
            f"Subspace alignment {results['subspace_alignment']:.4f} < 0.85"
        )
        assert results["relative_reconstruction_error"] < 0.25, (
            f"Reconstruction error {results['relative_reconstruction_error']:.4f} >= 0.25"
        )
        assert results["energy_drift"] < 0.0, (
            f"Energy drift {results['energy_drift']:.6f} >= 0.0"
        )

    def test_spatiotemporal_stream_generation_shape(self):
        P = generate_spatiotemporal_stream(steps=100, dim_p=20, dim_y=6, seed=42)
        assert P.shape == (100, 20)
        assert not np.isnan(P).any()
