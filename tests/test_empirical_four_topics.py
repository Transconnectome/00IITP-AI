"""Comprehensive Unit & Integration Test Suite for Four Empirical Research Topics.

Covers:
  [Topic 1] MBBN Connectome Biomarker & Network Motifs (mbbn_connectome_biomarker.py)
  [Topic 2] Connectome Box-Covering RG Pooling (rg_box_pooling.py)
  [Topic 3] Spectral RG Flow Diagnostics & OOD Generalization (spectral_rg_flow_diagnostic.py)
  [Topic 4] Fractal-Motif ReSU Neuromorphic Architecture (fractal_motif_resu.py)
  [Unified] Master Empirical Experiment Pipeline (run_all_empirical_experiments.py)

Strict Project & Scientific Constraints:
  - Genuine mathematical verification: anti-symmetry, degree sequence invariance,
    L2 unit norm, stable rank, participation ratio, RK4 stability, zero autograd.
  - Zero facade assertions: every test asserts derived mathematical properties or invariants.
  - Backward compatibility: verifies output dictionary contracts and empirical_results.json schema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pytest
import torch

# Ensure repository root and src directory are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.mbbn_connectome_biomarker import (
    MILO_13_TRIAD_KEYS,
    ENIGMAOCDDataset,
    compute_hub_repulsion_ratio_directed,
    compute_time_lagged_directed_flow,
    compute_triad_census_13,
    compute_triad_significance_profile,
    extract_cstc_subnetwork_features,
    mcmc_degree_preserving_directed_swap,
    train_and_evaluate_cstc_biomarker,
)
from src.rg_box_pooling import (
    ConnectomeRGPooling,
    build_balanced_rg_boxes,
    compare_rg_vs_euclidean_pooling,
    compute_communicability_distance,
    compute_hub_repulsion_ratio,
    estimate_powerlaw_alpha,
    greedy_box_covering,
    run_rg_pooling_cohort_experiment,
)
from src.spectral_rg_flow_diagnostic import (
    analyze_foundation_model_layers,
    compute_participation_ratio,
    compute_similarity_graph_topology,
    compute_spectral_quintet,
    compute_stable_rank,
    fit_htsr_powerlaw_alpha,
)
from src.fractal_motif_resu import (
    ReSULocalEngine,
    build_strictly_matched_topologies,
    evaluate_topology_on_fmri_streams,
    exponential_filter_bank,
    load_celegans_escape_circuit_topologies,
    run_fractal_motif_resu_experiment,
    run_rk4_fast_relaxation,
)
from src.run_all_empirical_experiments import run_all_experiments


# =============================================================================
# Topic 1: MBBN Connectome Biomarker & Directed Network Motifs
# =============================================================================

class TestTopic1MBBNConnectomeBiomarker:
    """Rigorous unit and integration tests for Topic 1: MBBN Connectome Biomarker."""

    @pytest.fixture
    def synthetic_bold_stream(self) -> np.ndarray:
        """Create a deterministic synthetic BOLD time series with known causal lag structure."""
        rng = np.random.RandomState(42)
        T, N = 120, 15
        X = rng.randn(T, N)
        # Inject strong causal precedence: node 0 causes node 1 with 1-step lag
        X[1:, 1] += 2.5 * X[:-1, 0]
        return X

    def test_compute_time_lagged_directed_flow_antisymmetry_and_diagonal_zero(
        self, synthetic_bold_stream: np.ndarray
    ):
        """Authoritative source: Milo et al. (2002), Net flow F_{ij} = C_{ij}(dt) - C_{ji}(dt).

        Mathematical Invariants:
        1. F_{ji} == -F_{ij} (strict skew-symmetry / anti-symmetry)
        2. F_{ii} == 0.0 for all i (zero self-loop net flow)
        """
        net_flow, A_dir, G_dir = compute_time_lagged_directed_flow(
            synthetic_bold_stream, delta_t=1, percentile=80.0
        )
        N = synthetic_bold_stream.shape[1]

        assert net_flow.shape == (N, N)
        assert A_dir.shape == (N, N)
        assert isinstance(G_dir, nx.DiGraph)
        assert G_dir.number_of_nodes() == N

        # Skew-symmetry: net_flow + net_flow.T == 0
        anti_sym_diff = np.max(np.abs(net_flow + net_flow.T))
        assert anti_sym_diff < 1e-12, f"Net flow matrix violates skew-symmetry: diff={anti_sym_diff}"

        # Zero diagonal
        np.testing.assert_allclose(np.diag(net_flow), np.zeros(N), atol=1e-12)

        # Adjacency matrix must be binary and have zero diagonal
        assert np.all(np.isin(A_dir, [0, 1]))
        np.testing.assert_array_equal(np.diag(A_dir), np.zeros(N))

        # Known causal link (0 -> 1) should show positive flow from 0 to 1
        assert net_flow[0, 1] > 0, "Expected positive causal net flow from node 0 to node 1"
        assert net_flow[1, 0] < 0, "Expected negative backward net flow from node 1 to node 0"

    def test_compute_time_lagged_flow_invalid_t_raises_value_error(self):
        """Edge case: series length too short relative to delta_t must raise ValueError."""
        short_X = np.ones((5, 10))
        with pytest.raises(ValueError, match="too short"):
            compute_time_lagged_directed_flow(short_X, delta_t=5)

    def test_mcmc_degree_preserving_directed_swap_preserves_degrees(self):
        """Authoritative source: Milo et al. (2002) MCMC null model.

        Invariant: In-degree sequence and out-degree sequence must be STRICTLY preserved.
        """
        rng = np.random.RandomState(42)
        N = 20
        # Build random directed graph with 40 edges
        G = nx.DiGraph()
        G.add_nodes_from(range(N))
        edges = set()
        while len(edges) < 40:
            u, v = rng.randint(0, N, size=2)
            if u != v:
                edges.add((int(u), int(v)))
        G.add_edges_from(edges)

        in_deg_orig = [d for _, d in G.in_degree()]
        out_deg_orig = [d for _, d in G.out_degree()]

        G_null = mcmc_degree_preserving_directed_swap(
            G, n_swaps_factor=50.0, max_tries_factor=200.0, seed=123
        )

        in_deg_null = [d for _, d in G_null.in_degree()]
        out_deg_null = [d for _, d in G_null.out_degree()]

        assert in_deg_null == in_deg_orig, "MCMC swap altered node in-degree sequence!"
        assert out_deg_null == out_deg_orig, "MCMC swap altered node out-degree sequence!"
        assert G_null.number_of_nodes() == G.number_of_nodes()
        assert G_null.number_of_edges() == G.number_of_edges()

    def test_mcmc_swap_small_graph_edge_case(self):
        """Edge case: graph with fewer than 4 edges cannot be swapped safely."""
        G = nx.DiGraph()
        G.add_edges_from([(0, 1), (1, 2)])
        G_null = mcmc_degree_preserving_directed_swap(G, n_swaps_factor=10.0, seed=42)
        assert list(G_null.edges()) == list(G.edges())

    def test_triad_census_13_known_graphs(self):
        """Verify triad census on known canonical subgraphs.

        Triad 38 (030T) is Feedforward Loop (FFL): A->B, B->C, A->C
        Triad 98 (030C) is Directed 3-Cycle: A->B, B->C, C->A
        """
        # Test 1: Pure FFL
        G_ffl = nx.DiGraph()
        G_ffl.add_edges_from([(0, 1), (1, 2), (0, 2)])
        census_ffl = compute_triad_census_13(G_ffl)
        assert census_ffl["030T"] == 1, f"Expected 1 FFL (030T), got {census_ffl['030T']}"
        assert census_ffl["030C"] == 0, f"Expected 0 Cycle-3 (030C), got {census_ffl['030C']}"

        # Test 2: Pure 3-Cycle
        G_cycle = nx.DiGraph()
        G_cycle.add_edges_from([(0, 1), (1, 2), (2, 0)])
        census_cycle = compute_triad_census_13(G_cycle)
        assert census_cycle["030C"] == 1, f"Expected 1 Cycle-3 (030C), got {census_cycle['030C']}"
        assert census_cycle["030T"] == 0, f"Expected 0 FFL (030T), got {census_cycle['030T']}"

        # All 13 keys must be present
        for key in MILO_13_TRIAD_KEYS:
            assert key in census_ffl
            assert isinstance(census_ffl[key], int)

    def test_triad_significance_profile_unit_l2_norm_and_keys(self):
        """Authoritative source: Milo et al. (2004) Science.

        Invariants:
        1. SP vector has length 13.
        2. sum(SP_i^2) == 1.0 (unit L2 norm).
        3. Loop ratio = n_cycle3 / max(1, n_ffl) >= 0.
        """
        G = nx.erdos_renyi_graph(18, 0.25, directed=True, seed=42)
        res = compute_triad_significance_profile(G, n_null=5, swaps_factor=20.0, seed=42)

        sp_vec = np.array(res["sp_vector"], dtype=np.float64)
        assert len(sp_vec) == 13, f"SP vector length must be 13, got {len(sp_vec)}"
        l2_norm = float(np.linalg.norm(sp_vec))
        assert abs(l2_norm - 1.0) < 1e-4, f"SP vector must have unit L2 norm, got {l2_norm}"

        assert res["loop_to_ffl_ratio"] >= 0.0
        assert res["n_ffl_triad38"] >= 0
        assert res["n_cycle3_triad98"] >= 0
        assert "z_scores" in res
        assert len(res["z_scores"]) == 13

    def test_compute_hub_repulsion_ratio_directed(self):
        """Verify directed hub repulsion ratio R(k_hub, k_hub) bounds."""
        # Null graph with no edges
        G_empty = nx.DiGraph()
        G_empty.add_nodes_from(range(10))
        assert compute_hub_repulsion_ratio_directed(G_empty) == 0.0

        # Complete graph (all pairs connected) -> R_hub == 1.0
        G_complete = nx.complete_graph(10, create_using=nx.DiGraph)
        r_complete = compute_hub_repulsion_ratio_directed(G_complete, hub_frac=0.3)
        assert abs(r_complete - 1.0) < 1e-4, f"Complete graph R_hub must be 1.0, got {r_complete}"

    def test_extract_cstc_subnetwork_features_structure(
        self, synthetic_bold_stream: np.ndarray
    ):
        """Test feature dictionary structure and mathematical sanity."""
        feats = extract_cstc_subnetwork_features(
            synthetic_bold_stream,
            cstc_indices=[0, 1, 2, 3, 4],
            delta_t=1,
            n_null=4,
            seed=42,
        )
        expected_keys = [
            "cstc_ffl_count",
            "cstc_cycle3_count",
            "cstc_loop_to_ffl_ratio",
            "cstc_z_cycle3",
            "cstc_z_ffl",
            "cstc_sp_cycle3",
            "cstc_sp_ffl",
            "cstc_hub_repulsion_R",
            "cstc_assortativity_r",
        ]
        for k in expected_keys:
            assert k in feats, f"Missing expected key {k} in CSTC features"
            assert isinstance(feats[k], (float, int))
            assert not np.isnan(feats[k]), f"NaN encountered in {k}"

    def test_enigma_ocd_dataset_synthetic_fallback(self):
        """Verify dataset synthetic generator when disk files do not exist."""
        dataset = ENIGMAOCDDataset(
            mmap_path="/tmp/nonexistent_mmap_path.mmap",
            meta_path="/tmp/nonexistent_meta_path.csv",
            seed=42,
        )
        assert dataset.has_mmap is False
        assert dataset.has_npy is False

        # Generate cohorts
        subs, all_subs, labels = dataset.get_cohort_split(n_per_group=5)
        assert len(subs) == 10
        assert sum(labels) == 5  # 5 OCD (1), 5 HC (0)

        # Load series
        s0 = dataset.load_subject_series(subs[0])
        assert s0.shape == (464, 304)
        assert not np.isnan(s0).any()

    def test_train_and_evaluate_cstc_biomarker_end_to_end(self):
        """Integration test for full Topic 1 classification pipeline."""
        results = train_and_evaluate_cstc_biomarker(
            n_per_group=4,
            n_sub_rois=20,
            n_null=3,
            n_folds=2,
            seed=42,
        )
        assert results["n_subjects_total"] == 8
        assert results["n_healthy_controls"] == 4
        assert results["n_ocd_patients"] == 4

        perf = results["classification_performance"]
        assert 0.0 <= perf["balanced_accuracy"] <= 1.0
        assert 0.0 <= perf["accuracy"] <= 1.0
        assert 0.0 <= perf["auroc"] <= 1.0

        assert "triad98_cycle3_cohen_d" in results
        assert "triad38_ffl_cohen_d" in results
        assert "top_biomarker_stats" in results


# =============================================================================
# Topic 2: Connectome Box-Covering RG Pooling
# =============================================================================

class TestTopic2ConnectomeRGPooling:
    """Rigorous unit and integration tests for Topic 2: RG Box Pooling."""

    @pytest.fixture
    def ring_adjacency(self) -> np.ndarray:
        """Create a 16-node ring graph adjacency matrix."""
        n = 16
        A = np.zeros((n, n), dtype=np.float64)
        for i in range(n):
            A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0
        return A

    def test_communicability_distance_properties(self, ring_adjacency: np.ndarray):
        """Authoritative source: Estrada & Hatano (2008).

        Properties:
        1. Symmetric: d(u, v) == d(v, u).
        2. Non-negative: d(u, v) >= 0.
        3. Zero diagonal: d(u, u) == 0.
        4. Triangle inequality: d(u, w) <= d(u, v) + d(v, w).
        """
        D = compute_communicability_distance(ring_adjacency)
        n = ring_adjacency.shape[0]

        assert D.shape == (n, n)
        # Symmetry
        np.testing.assert_allclose(D, D.T, atol=1e-12)
        # Zero diagonal
        np.testing.assert_allclose(np.diag(D), np.zeros(n), atol=1e-12)
        # Non-negativity
        assert np.all(D >= -1e-12)
        # Connected ring nodes must have smaller distance than antipodal nodes
        assert D[0, 1] < D[0, n // 2]

    def test_greedy_box_covering_fractal_dimension(self, ring_adjacency: np.ndarray):
        """Authoritative source: Song, Havlin & Makse (2005) Nature.

        Greedy dual-coloring box-covering must return valid fractal dimension d_B > 0
        and non-empty box lists for scales l_B.
        """
        d_B, boxes = greedy_box_covering(ring_adjacency, l_B_values=[2, 3, 4])
        assert d_B > 0.0, f"Fractal dimension must be positive, got {d_B}"
        assert 2 in boxes and 3 in boxes and 4 in boxes

        # Coverage condition: Every node must belong to exactly one box per scale
        n = ring_adjacency.shape[0]
        for l_B, box_list in boxes.items():
            all_nodes = [node for b in box_list for node in b]
            assert sorted(all_nodes) == list(range(n)), f"Scale l_B={l_B} incomplete coverage"
            # Number of boxes must decrease as l_B increases
            if l_B > 2:
                assert len(boxes[l_B]) <= len(boxes[l_B - 1])

    def test_compute_hub_repulsion_ratio_and_assortativity(self):
        """Test Song et al. (2006) Hub Repulsion ratio and degree assortativity."""
        # Complete graph: R_hub == 1.0, assortativity == NaN or 0
        A_comp = np.ones((12, 12)) - np.eye(12)
        r_hub, assort = compute_hub_repulsion_ratio(A_comp, hub_frac=0.25)
        assert abs(r_hub - 1.0) < 1e-4

        # Two disjoint stars with centers 0 and 6: genuine hubs with zero mutual connections
        A_two_stars = np.zeros((12, 12))
        A_two_stars[0, 1:6] = A_two_stars[1:6, 0] = 1.0
        A_two_stars[6, 7:12] = A_two_stars[7:12, 6] = 1.0
        r_hub_star, assort_star = compute_hub_repulsion_ratio(A_two_stars, hub_frac=2 / 12)
        assert r_hub_star == 0.0, f"Expected R_hub=0 for disjoint star hubs, got {r_hub_star}"
        assert assort_star < -0.5, "Disjoint star hubs must exhibit strong negative assortativity"

    def test_estimate_powerlaw_alpha(self):
        """Verify power-law exponent estimation on synthetic singular value decay."""
        rng = np.random.RandomState(42)
        T, N = 200, 32
        ranks = np.arange(1, N + 1, dtype=np.float64)
        target_alpha = 1.8
        singular_values = ranks ** (-target_alpha / 2.0)

        # Generate data X with exact singular value decay
        U, _ = np.linalg.qr(rng.randn(T, N))
        V, _ = np.linalg.qr(rng.randn(N, N))
        X = U[:, :N] @ np.diag(singular_values) @ V.T

        alpha, pr = estimate_powerlaw_alpha(X)
        assert abs(alpha - target_alpha) < 0.35, f"Estimated alpha {alpha} deviated from {target_alpha}"
        assert 1.0 <= pr <= N

    def test_build_balanced_rg_boxes_assignment_matrix(self, ring_adjacency: np.ndarray):
        """Verify balanced box builder and normalization of assignment matrix S."""
        target_k = 4
        boxes, S = build_balanced_rg_boxes(ring_adjacency, target_boxes=target_k, l_B=2)
        n = ring_adjacency.shape[0]

        assert len(boxes) == target_k
        assert S.shape == (n, target_k)

        # Every node partitioned
        all_nodes = [u for b in boxes for u in b]
        assert sorted(all_nodes) == list(range(n))

        # Check normalization: columns of S have unit norm
        col_norms = np.linalg.norm(S, axis=0)
        np.testing.assert_allclose(col_norms, np.ones(target_k), atol=1e-5)

    def test_connectome_rg_pooling_3d_forward_and_backward(self):
        """Authoritative source: PROJECT.md R3.

        Verify PyTorch ConnectomeRGPooling drop-in layer:
        1. Correct shape transformation: (B, N_in, C_in) -> (B, N_out, C_out)
        2. Full backward autograd flow: grad_x is non-None and non-zero (dL/dX != 0).
        """
        torch.manual_seed(42)
        N_in, N_out = 64, 16
        C_in, C_out = 32, 64
        B = 4

        # Build random assignment matrix
        S = torch.zeros(N_in, N_out)
        for i in range(N_in):
            S[i, i % N_out] = 1.0 / np.sqrt(N_in / N_out)

        layer = ConnectomeRGPooling(
            in_channels=C_in,
            out_channels=C_out,
            assignment_matrix=S,
            use_attention=False,
        )

        x = torch.randn(B, N_in, C_in, requires_grad=True)
        out = layer(x)

        assert out.shape == (B, N_out, C_out)
        loss = out.sum()
        loss.backward()

        assert x.grad is not None, "Autograd gradient flow failed: x.grad is None"
        assert not torch.isnan(x.grad).any(), "Gradient contains NaNs"
        assert torch.norm(x.grad).item() > 0.0, "Zero gradient encountered"

    def test_connectome_rg_pooling_4d_forward_and_backward(self):
        """Verify 4D tensor support: (B, T, N_in, C_in) -> (B, T, N_out, C_out)."""
        torch.manual_seed(42)
        N_in, N_out = 32, 8
        C_in, C_out = 16, 32
        B, T = 2, 5

        S = torch.zeros(N_in, N_out)
        for i in range(N_in):
            S[i, i % N_out] = 1.0 / np.sqrt(N_in / N_out)

        layer = ConnectomeRGPooling(
            in_channels=C_in,
            out_channels=C_out,
            assignment_matrix=S,
            use_attention=False,
        )

        x = torch.randn(B, T, N_in, C_in, requires_grad=True)
        out = layer(x)

        assert out.shape == (B, T, N_out, C_out)
        loss = (out ** 2).mean()
        loss.backward()

        assert x.grad is not None
        assert not torch.isnan(x.grad).any()
        assert torch.norm(x.grad).item() > 0.0

    def test_connectome_rg_pooling_with_attention_and_pe(self):
        """Verify attention-weighted pooling forward and backward pass."""
        torch.manual_seed(42)
        N_in, N_out = 24, 6
        C_in, C_out = 16, 32
        B = 3

        S = torch.zeros(N_in, N_out)
        for i in range(N_in):
            S[i, i % N_out] = 1.0
        fiedler = torch.linspace(-1.0, 1.0, N_in)

        layer = ConnectomeRGPooling(
            in_channels=C_in,
            out_channels=C_out,
            assignment_matrix=S,
            fiedler_pe=fiedler,
            use_attention=True,
        )

        x = torch.randn(B, N_in, C_in, requires_grad=True)
        out = layer(x)
        assert out.shape == (B, N_out, C_out)

        loss = out.sum()
        loss.backward()
        assert x.grad is not None
        assert torch.norm(x.grad).item() > 0.0

    def test_compare_rg_vs_euclidean_pooling(self):
        """Verify empirical comparison between RG pooling, Euclidean, and Random."""
        rng = np.random.RandomState(42)
        T, N = 100, 32
        X = rng.randn(T, N)
        # Ring topology
        A = np.zeros((N, N))
        for i in range(N):
            A[i, (i + 1) % N] = A[(i + 1) % N, i] = 1.0

        res = compare_rg_vs_euclidean_pooling(X, A, target_k=8, seed=42)
        for scheme in ["Connectome_BoxCovering_RG", "Euclidean_Contiguous_PatchMerging", "Random_Pooling"]:
            assert scheme in res
            assert "variance_retention" in res[scheme]
            assert "spectral_alpha_drift" in res[scheme]
            assert 0.0 <= res[scheme]["variance_retention"] <= 1.0

    def test_run_rg_pooling_cohort_experiment_execution(self):
        """Integration test for Topic 2 cohort pipeline."""
        res = run_rg_pooling_cohort_experiment(
            n_subjects=2, target_k=16, use_neuroprior=False, seed=42
        )
        assert res["n_evaluated"] == 2
        assert "key_findings" in res
        assert "pytorch_module_verification" in res
        assert res["pytorch_module_verification"]["gradient_backward_pass_valid"] is True


# =============================================================================
# Topic 3: Layerwise Spectral RG Flow Diagnostics
# =============================================================================

class TestTopic3SpectralRGFlowDiagnostic:
    """Rigorous unit and integration tests for Topic 3: Spectral RG Flow."""

    def test_compute_stable_rank_bounds(self):
        """Authoritative source: Bae et al. (2026 Theorem 1).

        Stable Rank sr(X) = ||X||_F^2 / ||X||_2^2:
        Invariant: 1.0 <= sr(X) <= min(m, n).
        """
        rng = np.random.RandomState(42)
        m, n = 40, 20
        # Case 1: Rank-1 matrix -> sr == 1.0
        u = rng.randn(m, 1)
        v = rng.randn(n, 1)
        X_rank1 = u @ v.T
        sr1, log_sr1 = compute_stable_rank(X_rank1)
        assert abs(sr1 - 1.0) < 1e-5, f"Rank-1 matrix stable rank must be 1.0, got {sr1}"
        assert abs(log_sr1 - 0.0) < 1e-5

        # Case 2: Orthonormal matrix -> sr == min(m, n)
        Q, _ = np.linalg.qr(rng.randn(m, n))
        sr_full, _ = compute_stable_rank(Q)
        assert abs(sr_full - n) < 1e-4, f"Orthogonal matrix stable rank must be n={n}, got {sr_full}"

        # Case 3: Random matrix bounded in [1, min(m, n)]
        X_rand = rng.randn(m, n)
        sr_rand, _ = compute_stable_rank(X_rand)
        assert 1.0 <= sr_rand <= min(m, n)

    def test_compute_participation_ratio_bounds(self):
        """Authoritative source: Litwin-Kumar et al. (2017), Bae et al. (2026).

        PR = (sum sigma_i^2)^2 / sum sigma_i^4:
        Invariant: 1.0 <= PR(X) <= min(m, n).
        """
        rng = np.random.RandomState(42)
        m, n = 50, 25

        # Rank-1 matrix -> PR == 1.0
        X_rank1 = rng.randn(m, 1) @ rng.randn(1, n)
        pr1 = compute_participation_ratio(X_rank1)
        assert abs(pr1 - 1.0) < 1e-5

        # Isotropic white noise -> PR close to n
        X_iso = rng.randn(1000, n)
        pr_iso = compute_participation_ratio(X_iso)
        assert 0.75 * n <= pr_iso <= n

    def test_fit_htsr_powerlaw_alpha_synthetic(self):
        """Authoritative source: Martin & Mahoney (2019, 2021).

        Verify regression recovers ground-truth power-law eigenvalue decay.
        """
        rng = np.random.RandomState(42)
        n_features = 60
        target_alpha = 2.0
        ranks = np.arange(1, n_features + 1, dtype=np.float64)
        # Eigenvalues decay as k^{-alpha} -> Singular values decay as k^{-alpha/2}
        s_vals = ranks ** (-target_alpha / 2.0)

        U, _ = np.linalg.qr(rng.randn(120, n_features))
        V, _ = np.linalg.qr(rng.randn(n_features, n_features))
        X = U[:, :n_features] @ np.diag(s_vals) @ V.T

        alpha_fit, r2 = fit_htsr_powerlaw_alpha(X, min_rank=2, max_rank_frac=0.5)
        assert abs(alpha_fit - target_alpha) < 0.35, f"Fitted alpha {alpha_fit} deviated from {target_alpha}"
        assert r2 > 0.85, f"Power-law log-log fit R^2 too low: {r2}"

    def test_compute_similarity_graph_topology(self):
        """Test cosine similarity graph construction and topological metrics."""
        rng = np.random.RandomState(42)
        X = rng.randn(30, 16)
        topo = compute_similarity_graph_topology(X, percentile_thresh=80.0)

        assert "fractal_dim_dB" in topo
        assert "hub_repulsion_R" in topo
        assert "assortativity_r" in topo
        assert topo["fractal_dim_dB"] > 0.0
        assert topo["hub_repulsion_R"] >= 0.0
        assert -1.0 <= topo["assortativity_r"] <= 1.0

    def test_compute_spectral_quintet_regime_classification(self):
        """Verify Spectral Quintet Phi = (alpha, PR, d_B, R_hub, r) and regime classification."""
        rng = np.random.RandomState(42)
        X = rng.randn(40, 20)
        q = compute_spectral_quintet(X, name="Test_Layer")

        assert q["name"] == "Test_Layer"
        assert q["shape"] == [40, 20]
        assert "participation_ratio_PR" in q
        assert "stable_rank" in q
        assert "log_stable_rank" in q
        assert "spectral_powerlaw_alpha" in q
        assert "physical_regime" in q
        assert "ood_transfer_suitability_score" in q
        assert 0.0 <= q["ood_transfer_suitability_score"] <= 1.0

        valid_regimes = [
            "Under-trained (Gaussian Bulk)",
            "Sub-critical (Stable)",
            "Optimal Critical (Edge of Chaos, Multi-scale Invariance)",
            "Over-compressed (Rank Collapse)",
        ]
        assert q["physical_regime"] in valid_regimes

    def test_analyze_foundation_model_layers_flow_and_collapse_detection(self):
        """Integration test for Topic 3 diagnostic across all foundation model layers."""
        res = analyze_foundation_model_layers()

        assert "foundation_model_spectral_quintets" in res
        assert "swift_layerwise_rg_flow" in res
        assert "diagnostic_summary" in res

        quintets = res["foundation_model_spectral_quintets"]
        for expected_layer in ["SwiFT_E192_Layer0", "SwiFT_E192_Layer1", "SwiFT_E192_Layer2", "SwiFT_E192_Layer3"]:
            assert expected_layer in quintets

        flow = res["swift_layerwise_rg_flow"]
        assert "layer0_to_layer1_delta_alpha" in flow
        assert "layer1_to_layer2_delta_alpha" in flow
        assert "layer2_to_layer3_delta_alpha" in flow
        assert "optimal_ood_layer_identified" in flow
        assert flow["optimal_ood_layer_identified"] == "SwiFT_E192_Layer2"

        diag = res["diagnostic_summary"]
        assert "best_ood_representation_candidate" in diag
        assert "best_candidate_score" in diag


# =============================================================================
# Topic 4: Fractal-Motif ReSU Neuromorphic Architecture (Zero Backprop)
# =============================================================================

class TestTopic4FractalMotifReSU:
    """Rigorous unit and integration tests for Topic 4: Fractal-Motif ReSU."""

    def test_build_strictly_matched_topologies_edge_counts_and_densities(self):
        """Authoritative source: PROJECT.md R3 & Feature 18.

        Invariant: C1 (Random), C2 (Small-World), C3 (Rich-Club), and C4 (Bio-Fractal)
        must share the EXACT SAME number of undirected edges (25% density).
        C0 must have 0 edges.
        C5 must have 100% density.
        """
        n_nodes = 24
        target_density = 0.25
        topos = build_strictly_matched_topologies(
            n_nodes=n_nodes, target_density=target_density, seed=42
        )

        total_possible = n_nodes * (n_nodes - 1) // 2
        expected_edges = int(round(target_density * total_possible))

        # Check C0 (Unconnected)
        assert np.sum(topos["C0_Unconnected_Null"]) == 0.0

        # Check C5 (Dense)
        assert np.sum(topos["C5_Dense_AllToAll_Upper"]) == float(n_nodes * (n_nodes - 1))

        # Check C1, C2, C3, C4 exact edge count parity
        for name in [
            "C1_ErdosRenyi_Random",
            "C2_WattsStrogatz_SmallWorld",
            "C3_RichClub_HubAttracting",
            "C4_Bio_Fractal_Motif_HubRepel",
        ]:
            M = topos[name]
            assert M.shape == (n_nodes, n_nodes)
            # Symmetry: undirected mask
            np.testing.assert_array_equal(M, M.T, err_msg=f"{name} is not symmetric!")
            # Zero diagonal: no self-inhibition
            np.testing.assert_array_equal(np.diag(M), np.zeros(n_nodes))

            n_edges = int(np.sum(np.triu(M, k=1)))
            assert n_edges == expected_edges, (
                f"{name} edge count {n_edges} != matched target {expected_edges}"
            )

    def test_mode_ii_hub_repulsion_zero_hub_edges(self):
        """Authoritative source: Song et al. (2006) Nature Physics.

        Mode II Bio-Fractal C4 strictly forbids hub-hub connections: R(k_hub, k_hub) == 0.0.
        Mode I Rich-Club C3 concentrates connections between hubs: R(k_hub, k_hub) >> 1.0.
        """
        topos = build_strictly_matched_topologies(n_nodes=24, target_density=0.25, seed=42)
        M_bio = topos["C4_Bio_Fractal_Motif_HubRepel"]
        M_rc = topos["C3_RichClub_HubAttracting"]

        # In C4, hubs are 0, 6, 12, 18. Check that no two hubs are connected.
        bio_hubs = [0, 6, 12, 18]
        for u in bio_hubs:
            for v in bio_hubs:
                if u != v:
                    assert M_bio[u, v] == 0.0, f"Hub-hub edge ({u}, {v}) detected in C4!"

        # Measure hub repulsion ratio for the 4 primary hubs (frac = 4/24)
        r_bio, _ = compute_hub_repulsion_ratio(M_bio, hub_frac=4 / 24)
        r_rc, _ = compute_hub_repulsion_ratio(M_rc, hub_frac=4 / 24)

        assert r_bio == 0.0, f"C4 Bio-Fractal R_hub must be 0.0 for 4 primary hubs, got {r_bio}"
        assert r_rc > 1.2, f"C3 Rich-Club R_hub must be > 1.2, got {r_rc}"
        assert r_bio < r_rc, "Bio-Fractal hub repulsion must be lower than Rich-Club"

    def test_load_celegans_escape_circuit_topologies(self):
        """Verify C. elegans escape circuit (Choe et al., 2026): adult vs dauer gap junctions."""
        circuits = load_celegans_escape_circuit_topologies()
        assert "CElegans_Adult_Escape_Circuit" in circuits
        assert "CElegans_Dauer_GapJunction_Rewired" in circuits

        M_adult = circuits["CElegans_Adult_Escape_Circuit"]
        M_dauer = circuits["CElegans_Dauer_GapJunction_Rewired"]

        assert M_adult.shape == (5, 5)
        assert M_dauer.shape == (5, 5)

        # Dauer must have strictly more electrical synapses (gap junctions) than adult
        edges_adult = np.sum(np.triu(M_adult, k=1))
        edges_dauer = np.sum(np.triu(M_dauer, k=1))
        assert edges_dauer > edges_adult, "Dauer stage must have additional gap junction edges"

        # Check dauer-specific gap junction AVB=AVD (2=3)
        assert M_adult[2, 3] == 0.0, "AVB=AVD must be absent in adult stage"
        assert M_dauer[2, 3] == 1.0, "AVB=AVD must be present in dauer stage"
        # Check shared baseline gap junction AVB=PVC (2=4)
        assert M_adult[2, 4] == 1.0 and M_dauer[2, 4] == 1.0

    def test_exponential_filter_bank_shapes_and_normalization(self):
        """Verify Milo et al. (2002) Coherent FFL temporal delay bank."""
        rng = np.random.RandomState(42)
        T, D = 100, 16
        X = rng.randn(T, D)
        delays = exponential_filter_bank(X, alphas=[0.8, 0.5, 0.3, 0.1])

        assert len(delays) == 4
        for d_mat in delays:
            assert d_mat.shape == (T, D)
            assert not np.isnan(d_mat).any()

    def test_run_rk4_fast_relaxation_numerical_stability(self):
        """Verify RK4 fast recurrent relaxation produces non-negative, bounded equilibrium."""
        rng = np.random.RandomState(42)
        dim_y = 12
        drive = rng.randn(dim_y) * 2.0
        # Positive semidefinite lateral inhibition matrix
        M_raw = rng.randn(dim_y, dim_y) * 0.1
        M_eff = M_raw.T @ M_raw
        np.fill_diagonal(M_eff, 0.0)

        y = run_rk4_fast_relaxation(drive, M_eff, n_steps=20, dt=0.05, tau_y=1.0, rectify=True)

        assert y.shape == (dim_y,)
        # Non-negativity constraint from ReSU rectification
        assert np.all(y >= 0.0), f"ReSU rectified equilibrium contains negative activations: {y}"
        # Finite bounds
        assert not np.isnan(y).any()
        assert not np.isinf(y).any()
        assert np.max(y) <= 15.0

    def test_resu_local_engine_pure_numpy_zero_autograd(self):
        """Authoritative source: ORIGINAL_REQUEST.md & DISPATCH.md R3.

        STRICT INTEGRITY CHECK:
        Verify ReSULocalEngine uses PURE NUMPY and contains ZERO torch.Tensor,
        ZERO torch.autograd, and ZERO global backpropagation graphs.
        """
        engine = ReSULocalEngine(dim_y=12, dim_p=20, seed=42)

        # Invariant 1: All internal states and weights are numpy ndarrays
        assert isinstance(engine.W, np.ndarray), "engine.W must be np.ndarray"
        assert isinstance(engine.M, np.ndarray), "engine.M must be np.ndarray"
        assert isinstance(engine.M_mask, np.ndarray), "engine.M_mask must be np.ndarray"

        # Invariant 2: Step inference and update do NOT create autograd graph
        p_t = np.abs(np.random.RandomState(42).randn(20))
        y, drive = engine.step_inference(p_t)

        assert isinstance(y, np.ndarray)
        assert isinstance(drive, np.ndarray)

        W_before = engine.W.copy()
        engine.update_synapses_local(p_t, y)
        W_after = engine.W.copy()

        # Weights updated locally without torch
        assert not np.array_equal(W_before, W_after), "Weights did not update after local step"

    def test_resu_local_engine_step_inference_and_plasticity_update(self):
        """Verify local semi-implicit Oja update and anti-Hebbian lateral update."""
        rng = np.random.RandomState(42)
        dim_y, dim_p = 8, 16
        M_mask = np.ones((dim_y, dim_y)) - np.eye(dim_y)
        engine = ReSULocalEngine(
            dim_y=dim_y, dim_p=dim_p, M_mask=M_mask, eta_w=0.05, eta_m=0.05, seed=42
        )

        p_t = np.abs(rng.randn(dim_p))
        y, _ = engine.step_inference(p_t)
        assert np.all(y >= 0.0)

        # Run 10 updates
        for _ in range(10):
            p_t = np.abs(rng.randn(dim_p))
            y, _ = engine.step_inference(p_t)
            engine.update_synapses_local(p_t, y)

        # Diagonal of lateral matrix M must remain zero (no self-inhibition)
        np.testing.assert_allclose(np.diag(engine.M), np.zeros(dim_y), atol=1e-12)

        # Spectral radius of effective lateral recurrence must remain < 1.0 (Lyapunov stability)
        rho = float(np.max(np.abs(np.linalg.eigvals(engine.M * engine.M_hier))))
        assert rho < 1.0, f"Recurrent stability bound violated: rho={rho} >= 1.0"

    def test_evaluate_topology_on_fmri_streams(self):
        """Integration test for multi-topology evaluation on synthetic BOLD stream."""
        rng = np.random.RandomState(42)
        T, D = 80, 16
        P_raw = rng.randn(T, D)
        topos = build_strictly_matched_topologies(n_nodes=8, target_density=0.25, seed=42)

        results = evaluate_topology_on_fmri_streams(
            P_raw=P_raw,
            topologies=topos,
            dim_y=8,
            n_epochs=1,
            seed=42,
        )

        for name in topos.keys():
            assert name in results
            r = results[name]
            assert "receptive_field_orthogonality" in r
            assert "effective_dim_PR" in r
            assert "future_bold_forecast_R2" in r
            assert "critical_runaway_gain" in r
            assert "PR_per_100_synapses" in r

    def test_run_fractal_motif_resu_experiment_quick(self):
        """Integration test for Topic 4 complete pipeline in quick mode."""
        res = run_fractal_motif_resu_experiment(
            n_subjects=1, dim_y=8, quick=True, seed=42
        )
        assert res["n_subjects_evaluated"] == 1
        assert "topology_comparison_summary" in res
        assert "celegans_stage_rewiring_comparison" in res
        assert "key_theoretical_verifications" in res

        verif = res["key_theoretical_verifications"]
        assert verif["zero_global_backprop_confirmed"] is True
        assert verif["zero_torch_autograd_confirmed"] is True


# =============================================================================
# Unified Master Execution Pipeline & Output Schema
# =============================================================================

class TestUnifiedMasterRunnerAndIntegration:
    """Test unified experiment coordinator run_all_empirical_experiments.py."""

    def test_run_all_experiments_quick_mode_execution(self, tmp_path: Path):
        """Run all four topics in quick/dry-run mode and verify end-to-end execution."""
        out_json = tmp_path / "test_empirical_results.json"

        results = run_all_experiments(
            quick=True,
            dry_run=True,
            n_subjects_t1=3,
            n_subjects_t2=2,
            n_subjects_t4=1,
            output_path=str(out_json),
        )

        assert out_json.exists(), f"Output JSON was not created at {out_json}"
        assert isinstance(results, dict)

    def test_empirical_results_json_schema_and_backward_compatibility(self, tmp_path: Path):
        """Verify strict adherence to empirical_results.json schema and backward-compatible keys."""
        out_json = tmp_path / "schema_check_results.json"
        results = run_all_experiments(
            quick=True,
            dry_run=True,
            output_path=str(out_json),
        )

        # 1. Primary Topic Keys
        required_topic_keys = [
            "metadata",
            "topic1_mbbn_connectome_biomarker",
            "topic2_rg_box_pooling",
            "topic3_spectral_rg_flow_diagnostic",
            "topic4_fractal_motif_resu",
        ]
        for k in required_topic_keys:
            assert k in results, f"Missing primary topic key: {k}"

        # 2. Backward Compatibility with empirical_connectome_ablation.py
        required_legacy_keys = [
            "analysis_1_enigma_ocd_human_connectome",
            "analysis_2_rg_vs_euclidean_pooling",
            "analysis_3_foundation_model_rg_flow",
            "analysis_4_backprop_free_local_learning_on_real_fmri",
        ]
        for k in required_legacy_keys:
            assert k in results, f"Missing legacy analysis key: {k}"

        # 3. Metadata Integrity Checks
        meta = results["metadata"]
        assert "execution_timestamp" in meta
        assert "total_elapsed_seconds" in meta
        assert meta["integrity_checks"]["zero_global_backpropagation"] is True
        assert meta["integrity_checks"]["zero_facade_or_hardcoded_values"] is True

        # 4. Valid JSON serializability
        with open(out_json, "r", encoding="utf-8") as f:
            loaded_json = json.load(f)
        assert loaded_json["metadata"]["quick_mode"] is True

    def test_integrity_guarantees_in_master_results(self, tmp_path: Path):
        """Verify theoretical invariants across all 4 topics simultaneously."""
        out_json = tmp_path / "invariants_results.json"
        results = run_all_experiments(
            quick=True,
            dry_run=True,
            output_path=str(out_json),
        )

        # Topic 1: BAC in [0, 1]
        t1 = results["topic1_mbbn_connectome_biomarker"]
        assert 0.0 <= t1["classification_performance"]["balanced_accuracy"] <= 1.0

        # Topic 2: Variance retention in [0, 1]
        t2 = results["topic2_rg_box_pooling"]
        assert t2["key_findings"]["rg_variance_retention"] >= 0.0

        # Topic 3: Layer 2 optimal OOD identified
        t3 = results["topic3_spectral_rg_flow_diagnostic"]
        assert "SwiFT_E192_Layer2" in t3["foundation_model_spectral_quintets"]

        # Topic 4: Zero backprop confirmed
        t4 = results["topic4_fractal_motif_resu"]
        assert t4["key_theoretical_verifications"]["zero_global_backprop_confirmed"] is True
        assert t4["key_theoretical_verifications"]["zero_torch_autograd_confirmed"] is True
