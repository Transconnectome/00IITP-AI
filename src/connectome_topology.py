"""Connectome Topology Generation with Network Motifs & Hub Repulsion.

Provides:
- Graph generation for directed connectome networks with embedded network motifs:
  - Feedforward loops (FFL, Triad 38 from Milo et al. 2002)
  - Bi-fan motifs (Milo et al. 2002)
- Fractal growth and hub repulsion disassortativity (Song et al. 2005, 2006):
  High-degree hub nodes avoid direct mutual connections (R(k_hub, k_hub) << 1,
  k_nn(k) ~ k^{-mu}), suppressing runaway excitation and ensuring dynamical stability.
- Lateral structural connectivity mask M_mask in {0, 1}^{k x k} constraining
  lateral inhibitory synapses in local learning engines (ReSU / NSM).
"""

from typing import Dict, List, Optional, Tuple
import networkx as nx
import numpy as np


def generate_motif_lateral_mask(
    num_units: int,
    motif_type: str = "bifan_hub_repelling",
    hub_repulsion: bool = True,
    seed: Optional[int] = None,
) -> np.ndarray:
    """Generate binary structural mask M_mask in {0, 1}^{k x k} for lateral inhibition.

    Diagonal elements are strictly zero (M_ii = 0; no self-inhibition).
    Hub units avoid mutual inhibitory links when hub_repulsion is True.
    """
    _, mask = build_connectome_topology(
        n_nodes=num_units,
        motif_type=motif_type,
        hub_repulsion=hub_repulsion,
        seed=seed,
    )
    return mask


def build_connectome_topology(
    n_nodes: int = 20,
    motif_type: str = "bifan_hub_repelling",
    hub_repulsion: bool = True,
    seed: Optional[int] = None,
) -> Tuple[nx.DiGraph, np.ndarray]:
    """Build directed connectome graph and its lateral inhibition structural mask.

    Parameters
    ----------
    n_nodes : int
        Number of neural units (connectome nodes).
    motif_type : str
        Type of network motif embedding ('bifan_hub_repelling', 'ffl', 'bifan').
    hub_repulsion : bool
        If True, enforce disassortative hub-repulsion (hubs do not link directly).
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    graph : nx.DiGraph
        Directed connectome graph with embedded motifs.
    mask : np.ndarray
        Binary lateral inhibition mask of shape (n_nodes, n_nodes) with zero diagonal.
    """
    if n_nodes <= 0:
        raise ValueError(f"n_nodes must be positive, got {n_nodes}")

    valid_motifs = {"bifan_hub_repelling", "ffl", "bifan"}
    if motif_type not in valid_motifs:
        raise ValueError(f"Unknown motif_type '{motif_type}', must be one of {valid_motifs}")

    rng = np.random.RandomState(seed)
    graph = nx.DiGraph()
    graph.add_nodes_from(range(n_nodes))

    if n_nodes < 3:
        mask = np.zeros((n_nodes, n_nodes), dtype=np.float64)
        return graph, mask

    # 1. Designate hub units (top ~15-20% nodes, 1 if n_nodes < 10, >=2 if n_nodes >= 10)
    n_hubs = max(1, int(0.18 * n_nodes)) if n_nodes < 10 else max(2, int(0.18 * n_nodes))
    hub_nodes = set(range(n_hubs))
    non_hub_nodes = [i for i in range(n_nodes) if i not in hub_nodes]
    graph.graph["hub_nodes"] = list(hub_nodes)
    graph.graph["hub_repulsion"] = hub_repulsion

    # 2. Embed Feedforward Loops (FFLs: Triad 38: u -> v, v -> w, u -> w)
    # Milo et al. (2002) Science
    if motif_type in ("bifan_hub_repelling", "ffl"):
        n_ffl = max(2, n_nodes // 3)
        for _ in range(n_ffl):
            # Pick 3 distinct nodes
            triad = rng.choice(n_nodes, size=3, replace=False)
            u, v, w = triad[0], triad[1], triad[2]

            if hub_repulsion and (u in hub_nodes and w in hub_nodes):
                # Divert through non-hub to preserve hub repulsion without creating self-loops
                cand_w = [n for n in non_hub_nodes if n not in (u, v)]
                if cand_w:
                    w = rng.choice(cand_w)

            graph.add_edge(u, v)
            graph.add_edge(v, w)
            graph.add_edge(u, w)

    # 3. Embed Bi-fan Motifs (2 sources u1, u2 -> 2 targets v1, v2)
    # Milo et al. (2002)
    if motif_type in ("bifan_hub_repelling", "bifan") and n_nodes >= 4:
        n_bifans = max(2, n_nodes // 4)
        for _ in range(n_bifans):
            cand = rng.choice(n_nodes, size=4, replace=False)
            u1, u2 = cand[0], cand[1]
            v1, v2 = cand[2], cand[3]

            # Hub repulsion: sources u1, u2 and targets v1, v2 avoid hub-hub crosslinks
            if hub_repulsion:
                if u1 in hub_nodes and u2 in hub_nodes:
                    cand_u2 = [n for n in non_hub_nodes if n not in (u1, v1, v2)]
                    if cand_u2:
                        u2 = rng.choice(cand_u2)
                if v1 in hub_nodes and v2 in hub_nodes:
                    cand_v2 = [n for n in non_hub_nodes if n not in (u1, u2, v1)]
                    if cand_v2:
                        v2 = rng.choice(cand_v2)

            graph.add_edge(u1, v1)
            graph.add_edge(u1, v2)
            graph.add_edge(u2, v1)
            graph.add_edge(u2, v2)

    # 4. Connect hubs to peripheral non-hub nodes (radiating hub-periphery architecture)
    for hub in hub_nodes:
        if non_hub_nodes:
            n_connect = min(len(non_hub_nodes), max(2, len(non_hub_nodes) // 3))
            targets = rng.choice(non_hub_nodes, size=n_connect, replace=False)
            for tgt in targets:
                graph.add_edge(hub, tgt)

    for node in non_hub_nodes:
        if graph.in_degree(node) == 0 and graph.out_degree(node) == 0:
            target_hub = rng.choice(list(hub_nodes))
            graph.add_edge(target_hub, node)

    # 5. Enforce Hub Repulsion: High-degree hubs avoid direct mutual connections
    # Song, Havlin & Makse (2006) Nature Physics: R(k_hub, k_hub) << 1
    if hub_repulsion:
        for h1 in hub_nodes:
            for h2 in hub_nodes:
                if h1 != h2:
                    if graph.has_edge(h1, h2):
                        graph.remove_edge(h1, h2)
                    if graph.has_edge(h2, h1):
                        graph.remove_edge(h2, h1)
    else:
        # Without hub repulsion (rich-club / assortative Mode I), hubs link mutually
        for h1 in hub_nodes:
            for h2 in hub_nodes:
                if h1 != h2 and rng.rand() < 0.7:
                    graph.add_edge(h1, h2)

    # Remove any potential self-loops as strict safeguard
    graph.remove_edges_from(nx.selfloop_edges(graph))

    # 6. Build lateral structural mask M_mask:
    # In cortical and neuromorphic circuits, lateral inhibition mediates competition
    # between units receiving convergent inputs (bi-fan / shared targets) or reciprocal links.
    adj = nx.to_numpy_array(graph, nodelist=range(n_nodes), dtype=np.float64)

    # Co-target lateral inhibition: units that share upstream inputs inhibit each other
    shared_input_inhibition = adj.T @ adj  # (i, j) > 0 if i and j receive input from same u

    # Combine direct reciprocal links and co-target inhibitory competition
    mask = ((adj + adj.T + shared_input_inhibition) > 0).astype(np.float64)

    if hub_repulsion:
        for h1 in hub_nodes:
            for h2 in hub_nodes:
                if h1 != h2:
                    mask[h1, h2] = 0.0
                    mask[h2, h1] = 0.0

    # Ensure zero self-inhibition
    np.fill_diagonal(mask, 0.0)

    # Ensure non-trivial connectivity: if mask is too sparse, add random non-hub links
    if np.sum(mask) < n_nodes:
        for i in non_hub_nodes:
            j = rng.choice(non_hub_nodes)
            if i != j:
                mask[i, j] = 1.0
                mask[j, i] = 1.0
        np.fill_diagonal(mask, 0.0)

    return graph, mask


def detect_motifs(graph: nx.DiGraph) -> Dict[str, int]:
    """Detect and count feedforward loops (FFL, Triad 38) and bi-fan motifs on distinct nodes."""
    ffl_count = 0
    nodes = list(graph.nodes())

    # Count Triad 38 (FFL): u -> v, v -> w, u -> w strictly on distinct nodes u != v != w
    for u in nodes:
        out_u = set(graph.successors(u))
        for v in out_u:
            if v == u:
                continue
            out_v = set(graph.successors(v))
            common_w = (out_u & out_v) - {u, v}
            ffl_count += len(common_w)

    # Count Bi-fan motifs: u1, u2 -> v1, v2 on distinct nodes
    bifan_count = 0
    n = len(nodes)
    for i in range(n):
        for j in range(i + 1, n):
            u1, u2 = nodes[i], nodes[j]
            targets_u1 = set(graph.successors(u1))
            targets_u2 = set(graph.successors(u2))
            shared = (targets_u1 & targets_u2) - {u1, u2}
            if len(shared) >= 2:
                bifan_count += len(shared) * (len(shared) - 1) // 2

    return {
        "feedforward_loops": ffl_count,
        "bifan_motifs": bifan_count,
    }


def compute_hub_repulsion_ratio(
    graph: nx.DiGraph,
    hub_percentile: float = 80.0,
    hub_nodes: Optional[List[int]] = None,
) -> float:
    """Compute hub-hub connection ratio R(k_hub, k_hub) from Song et al. (2006).

    Values << 1.0 indicate strong disassortative hub repulsion.
    """
    if graph.number_of_nodes() == 0:
        return 0.0

    if hub_nodes is not None:
        hubs = list(hub_nodes)
    elif "hub_nodes" in graph.graph:
        hubs = list(graph.graph["hub_nodes"])
    else:
        degrees = dict(graph.degree())
        if not degrees:
            return 0.0
        thresh = np.percentile(list(degrees.values()), hub_percentile)
        hubs = [n for n, d in degrees.items() if d >= thresh]

    if len(hubs) < 2:
        return 0.0

    possible_hub_edges = len(hubs) * (len(hubs) - 1)
    actual_hub_edges = 0
    for h1 in hubs:
        for h2 in hubs:
            if h1 != h2 and graph.has_edge(h1, h2):
                actual_hub_edges += 1

    total_possible_edges = len(graph) * (len(graph) - 1)
    total_edges = graph.number_of_edges()
    expected_hub_edges = possible_hub_edges * (total_edges / max(1, total_possible_edges))

    if expected_hub_edges == 0:
        return 0.0
    return float(actual_hub_edges / expected_hub_edges)

