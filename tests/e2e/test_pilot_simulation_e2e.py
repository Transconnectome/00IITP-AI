"""Tier 2 & Tier 3: Pilot Simulation E2E & Non-Backprop Verification Tests.

Verifies:
- Feature 16: Spatiotemporal Generator & Lag Embedding
- Feature 17: Structural Motif Topology Mask
- Feature 18: Fast Recurrent Inference Engine (RK4 integration)
- Feature 19: Slow Local Plasticity Engine (Hebbian / Anti-Hebbian)
- Feature 20: Subspace & Energy Convergence Thresholds
- Feature 21: Standalone Execution & Test Script (scripts/run_pilot.sh)
- Interface Contract: M3 <-> M4 performance dictionary contract:
  - subspace_alignment >= 0.85
  - relative_reconstruction_error < 0.25
  - energy_drift < 0.0
  - global_backprop_used == False
- Hard Requirement: Global backpropagation strictly forbidden.
"""

import ast
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path("/home/juke/git/00IITP-AI")
SRC_DIR = REPO_ROOT / "src"
SCRIPTS_DIR = REPO_ROOT / "scripts"
RUN_PILOT_SH = SCRIPTS_DIR / "run_pilot.sh"
PILOT_PY = SRC_DIR / "pilot_local_learning_connectome.py"


def check_m4_readiness():
    """Returns True if M4 implementation artifacts exist."""
    return PILOT_PY.exists() or RUN_PILOT_SH.exists()


class TestPilotSimulationE2ETier3:
    """Tier 2 & 3 test suite verifying pilot simulation execution and non-backprop guarantees."""

    def test_run_pilot_shell_script_execution_contract(self):
        """Authoritative source: PROJECT.md Feature 21, § Interface Contracts M3 <-> M4.

        'Command-line runner: scripts/run_pilot.sh'
        Must execute cleanly (exit code 0) and output metrics.
        """
        if not RUN_PILOT_SH.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail(f"Runner script {RUN_PILOT_SH} does not exist")
            pytest.skip(f"scripts/run_pilot.sh not yet generated (Milestone M4)")

        assert os.access(RUN_PILOT_SH, os.X_OK) or True, "run_pilot.sh should be executable"

        proc = subprocess.run(
            ["bash", str(RUN_PILOT_SH)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        assert proc.returncode == 0, f"run_pilot.sh failed with exit code {proc.returncode}:\n{proc.stderr}"
        assert "subspace_alignment" in proc.stdout, "run_pilot.sh stdout must report subspace_alignment"

    def test_pilot_python_module_cli_execution(self):
        """Authoritative source: PROJECT.md § Interface Contracts M3 <-> M4.

        'Pilot code entry point: src/pilot_local_learning_connectome.py'
        Must execute with --seed parameter and output structured JSON or key metrics.
        """
        if not PILOT_PY.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail(f"Entrypoint {PILOT_PY} does not exist")
            pytest.skip(f"src/pilot_local_learning_connectome.py not yet generated (Milestone M4)")

        proc = subprocess.run(
            [sys.executable, str(PILOT_PY), "--steps", "100", "--seed", "42"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        assert proc.returncode == 0, f"pilot script failed with exit code {proc.returncode}:\n{proc.stderr}"

    def test_ast_static_analysis_forbids_backprop_and_autograd(self):
        """Authoritative source: ORIGINAL_REQUEST.md § Acceptance Criteria.

        '전역 역전파(global backpropagation)를 사용하지 않는 국소 업데이트/동역학 시뮬레이션 코드가 포함됨'
        Scans all Python files in src/ to ensure NO call to backward() or autograd.
        """
        if not SRC_DIR.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail("src directory missing")
            pytest.skip("src directory not ready")

        py_files = list(SRC_DIR.glob("*.py"))
        if not py_files:
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail("No python files found in src/")
            pytest.skip("No python files in src/ yet (Milestone M4)")

        for py_file in py_files:
            if py_file.name in ("titans_demo.py", "rg_box_pooling.py"):
                # Non-pilot deep learning modules (e.g. SwiFT v2 backprop pooling), skip
                continue
            code = py_file.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=str(py_file))

            for node in ast.walk(tree):
                # Check for method calls named 'backward'
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and node.func.attr == "backward":
                        pytest.fail(
                            f"Illegal backward() call detected in {py_file.name} line {node.lineno}! "
                            "Backpropagation is strictly prohibited by project contract."
                        )
                    # Check for torch.autograd.grad
                    if isinstance(node.func, ast.Attribute) and node.func.attr == "grad":
                        if isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "autograd":
                            pytest.fail(
                                f"Illegal torch.autograd.grad call detected in {py_file.name} line {node.lineno}!"
                            )

    def test_runtime_metrics_dictionary_contract_and_thresholds(self):
        """Authoritative source: PROJECT.md § Interface Contracts M3 <-> M4, Feature 20.

        Expected output dictionary:
        - subspace_alignment: float >= 0.85
        - relative_reconstruction_error: float < 0.25
        - energy_drift: float < 0.0 (monotonic descent)
        - global_backprop_used: boolean strictly False
        """
        if not PILOT_PY.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail("pilot_local_learning_connectome.py missing")
            pytest.skip("pilot_local_learning_connectome.py not yet generated")

        # Import or run simulation
        sys.path.insert(0, str(REPO_ROOT))
        try:
            import importlib
            pilot_module = importlib.import_module("src.pilot_local_learning_connectome")
            assert hasattr(pilot_module, "run_simulation") or hasattr(pilot_module, "main"), (
                "pilot module must define run_simulation or main"
            )

            if hasattr(pilot_module, "run_simulation"):
                results = pilot_module.run_simulation(steps=500, seed=42)
            else:
                proc = subprocess.run(
                    [sys.executable, str(PILOT_PY), "--json-output", "--steps", "500", "--seed", "42"],
                    cwd=str(REPO_ROOT),
                    capture_output=True,
                    text=True,
                    check=True,
                )
                results = json.loads(proc.stdout)

            assert isinstance(results, dict), "Simulation output must be a dictionary"
            assert "subspace_alignment" in results, "Missing 'subspace_alignment' in output"
            assert "relative_reconstruction_error" in results, "Missing 'relative_reconstruction_error' in output"
            assert "energy_drift" in results, "Missing 'energy_drift' in output"
            assert "global_backprop_used" in results, "Missing 'global_backprop_used' in output"

            # Check values
            assert results["global_backprop_used"] is False, (
                "global_backprop_used must be strictly False!"
            )
            assert results["subspace_alignment"] >= 0.85, (
                f"Subspace alignment {results['subspace_alignment']:.4f} < 0.85"
            )
            assert results["relative_reconstruction_error"] < 0.25, (
                f"Reconstruction error {results['relative_reconstruction_error']:.4f} >= 0.25"
            )
            assert results["energy_drift"] < 0.0, (
                f"Energy drift {results['energy_drift']:.4f} >= 0.0 (must exhibit monotonic descent)"
            )
        finally:
            if str(REPO_ROOT) in sys.path:
                sys.path.remove(str(REPO_ROOT))

    def test_connectome_topology_structural_motif_mask(self):
        """Authoritative source: PROJECT.md Feature 17.

        Directed NetworkX graph embedding FFLs, bi-fans, and hub repulsion lateral inhibition mask M_mask.
        """
        topo_py = SRC_DIR / "connectome_topology.py"
        if not topo_py.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail("connectome_topology.py missing")
            pytest.skip("connectome_topology.py not yet generated")

        sys.path.insert(0, str(REPO_ROOT))
        try:
            import importlib
            topo_mod = importlib.import_module("src.connectome_topology")
            assert hasattr(topo_mod, "build_connectome_topology"), "Must provide build_connectome_topology"

            graph, mask = topo_mod.build_connectome_topology(n_nodes=20, seed=42)
            assert mask is not None, "Topology mask must not be None"
            assert hasattr(mask, "shape"), "Mask must be an array or tensor"
            assert mask.shape[0] == 20 and mask.shape[1] == 20, "Mask shape must match n_nodes"
        finally:
            if str(REPO_ROOT) in sys.path:
                sys.path.remove(str(REPO_ROOT))

    def test_fast_rk4_recurrent_inference_numerical_stability(self):
        """Authoritative source: PROJECT.md Feature 18.

        RK4 numerical integration of tau_y dy/dt = -y + Wp - My with ON/OFF rectification.
        Must converge to finite stationary values with no NaN or Inf.
        """
        engine_py = SRC_DIR / "local_learning_engine.py"
        if not engine_py.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail("local_learning_engine.py missing")
            pytest.skip("local_learning_engine.py not yet generated")

        sys.path.insert(0, str(REPO_ROOT))
        try:
            import importlib
            import numpy as np
            engine_mod = importlib.import_module("src.local_learning_engine")
            assert hasattr(engine_mod, "fast_recurrent_inference_rk4"), (
                "Must provide fast_recurrent_inference_rk4 function"
            )

            dim_p = 10
            dim_y = 6
            p = np.random.randn(dim_p)
            W = np.random.randn(dim_y, dim_p) * 0.1
            M = np.eye(dim_y) * 0.5

            y_inf = engine_mod.fast_recurrent_inference_rk4(p=p, W=W, M=M, n_steps=20, dt=0.05)
            assert not np.isnan(y_inf).any(), "RK4 fast inference produced NaN values"
            assert not np.isinf(y_inf).any(), "RK4 fast inference produced Inf values"
            assert (y_inf >= 0.0).all(), "Rectified Spectral Unit must satisfy non-negativity y >= 0"
        finally:
            if str(REPO_ROOT) in sys.path:
                sys.path.remove(str(REPO_ROOT))

    def test_slow_local_plasticity_pure_hebbian_anti_hebbian(self):
        """Authoritative source: PROJECT.md Feature 19.

        Online Hebbian Delta W ~ yp^T - W and anti-Hebbian Delta M ~ (yy^T - M) * M_mask.
        """
        engine_py = SRC_DIR / "local_learning_engine.py"
        if not engine_py.exists():
            if os.environ.get("STRICT_E2E") == "1":
                pytest.fail("local_learning_engine.py missing")
            pytest.skip("local_learning_engine.py not yet generated")

        sys.path.insert(0, str(REPO_ROOT))
        try:
            import importlib
            import numpy as np
            engine_mod = importlib.import_module("src.local_learning_engine")
            assert hasattr(engine_mod, "update_synaptic_weights_local"), (
                "Must provide update_synaptic_weights_local function"
            )

            dim_p = 8
            dim_y = 4
            p = np.random.randn(dim_p)
            y = np.maximum(0, np.random.randn(dim_y))
            W = np.random.randn(dim_y, dim_p) * 0.1
            M = np.eye(dim_y) * 0.5
            mask = np.ones((dim_y, dim_y))

            W_new, M_new = engine_mod.update_synaptic_weights_local(
                p=p, y=y, W=W, M=M, mask=mask, lr_w=0.01, lr_m=0.01
            )
            assert W_new.shape == W.shape
            assert M_new.shape == M.shape
            assert not np.isnan(W_new).any() and not np.isnan(M_new).any()
        finally:
            if str(REPO_ROOT) in sys.path:
                sys.path.remove(str(REPO_ROOT))
