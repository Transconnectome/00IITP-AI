"""A1/A2: closed-form census == networkx; null invariants on every null; rank-2 SP identity;
move-set reachability and uniformity (lazy chain counted by attempts)."""
import itertools

import networkx as nx
import numpy as np
import pytest

import tests.topic1_lagmotif.conftest_helpers  # noqa: F401
from src.topic1_lagmotif import motifs
from src.topic1_lagmotif.flow import lagged_net_flow, oriented_topk_graph


def _random_oriented(N, density, seed):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((200, N))
    return oriented_topk_graph(lagged_net_flow((X - X.mean(0)) / X.std(0), 1), density)


@pytest.mark.parametrize("N,density,seed", [(30, 0.2, 0), (60, 0.1, 1), (120, 0.15, 2), (304, 0.05, 3)])
def test_closed_form_census_matches_networkx(N, density, seed):
    A = _random_oriented(N, density, seed)
    G = nx.DiGraph(); G.add_nodes_from(range(N)); G.add_edges_from(zip(*np.nonzero(A)))
    tc = nx.triadic_census(G)
    c = motifs.census(A)
    for k in motifs.CLASSES:
        assert c[k] == tc[k], k
    mutual_classes = ("111D", "111U", "201", "120D", "120U", "120C", "210", "300")
    assert all(tc[k] == 0 for k in mutual_classes)


def test_every_null_graph_preserves_degrees_and_has_no_mutual_edges_or_self_loops():
    A = _random_oriented(60, 0.15, 7)
    kin, kout = A.sum(0), A.sum(1)
    for seed in range(40):
        Ag = motifs.sample_null_graph(A, 20, 0.2, seed)
        assert int((Ag.astype(np.int64) * Ag.T).sum()) == 0
        assert int(np.trace(Ag)) == 0
        assert np.array_equal(Ag.sum(0), kin) and np.array_equal(Ag.sum(1), kout)
        assert int(Ag.sum()) == int(A.sum())
        assert not np.array_equal(Ag, A)  # the chain actually moves


def test_rank_two_identity_holds_exactly():
    A = _random_oriented(80, 0.12, 9)
    r = motifs.motif_statistics(A, 200, 20, 0.2, np.arange(200))
    Z = r["Z"]
    assert abs(Z["021D"] + Z["030T"]) < 1e-9
    assert abs(Z["021U"] + Z["030T"]) < 1e-9
    assert r["acceptance_mean"] > 0.1


def test_invariant_checker_flags_reciprocal_edges_from_a_v1_style_swap():
    """The v1 swap (src/mbbn_connectome_biomarker.py:150-169) only rejects existing (u,z)/(w,v);
    re-implemented here, it creates mutual edges, which the per-null checker must catch."""
    A = _random_oriented(60, 0.15, 8).astype(np.int8)
    rng = np.random.default_rng(0)
    B = A.copy()
    src, dst = [list(x) for x in np.nonzero(B)]
    for _ in range(10 * len(src)):
        i, j = rng.integers(len(src), size=2)
        u, v, w, z = src[i], dst[i], src[j], dst[j]
        if len({u, v, w, z}) < 4 or B[u, z] or B[w, v]:
            continue
        B[u, v] = B[w, z] = 0; B[u, z] = B[w, v] = 1
        dst[i], dst[j] = z, v
    kin0 = A.astype(np.int64).sum(0); kout0 = A.astype(np.int64).sum(1)
    flag = motifs._check_invariants(B, np.array(src, np.int64), np.array(dst, np.int64), kin0, kout0, len(src))
    assert int((B.astype(np.int64) * B.T).sum()) > 0
    assert flag == 3


def test_rotation_move_reaches_both_orientations_of_an_isolated_triangle():
    """3-cycle + isolated node: the only other graph with this degree sequence is the reversed
    triangle. 2-swaps alone can never reach it (reducible); the rotation move can."""
    A = np.zeros((4, 4), np.int8); A[0, 1] = A[1, 2] = A[2, 0] = 1
    seen_swap = {motifs.sample_null_graph(A, 20, 0.0, s).tobytes() for s in range(50)}
    seen_mixed = [motifs.sample_null_graph(A, 20, 0.2, s).tobytes() for s in range(400)]
    assert len(seen_swap) == 1
    assert len(set(seen_mixed)) == 2
    frac = seen_mixed.count(A.tobytes()) / len(seen_mixed)
    assert 0.4 < frac < 0.6


def _degree_class(A):
    """Brute-force all oriented graphs on N<=5 nodes with A's in/out degrees."""
    N = A.shape[0]
    pairs = list(itertools.combinations(range(N), 2))
    kin, kout = A.sum(0), A.sum(1)
    out = []
    for states in itertools.product((0, 1, 2), repeat=len(pairs)):
        B = np.zeros((N, N), np.int8)
        for (i, j), s in zip(pairs, states):
            if s == 1:
                B[i, j] = 1
            elif s == 2:
                B[j, i] = 1
        if np.array_equal(B.sum(0), kin) and np.array_equal(B.sum(1), kout):
            out.append(B.tobytes())
    return out


def test_null_is_uniform_over_reachable_class_lazy_chain():
    from scipy.stats import chisquare
    A = np.zeros((5, 5), np.int8)
    for i, j in [(0, 1), (1, 2), (2, 3), (0, 3), (4, 0), (2, 4)]:
        A[i, j] = 1
    cls = _degree_class(A)
    assert len(cls) >= 5
    samples = [motifs.sample_null_graph(A, 200, 0.2, s).tobytes() for s in range(3000)]
    assert set(samples) <= set(cls)
    reach = sorted(set(samples))
    counts = np.array([samples.count(r) for r in reach])
    assert len(reach) == len(cls)  # this class is fully reached
    assert chisquare(counts).pvalue > 0.001
