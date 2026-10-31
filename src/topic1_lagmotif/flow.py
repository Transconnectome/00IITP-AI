"""Lagged net flow, oriented fixed-density graph, Hodge gradient share.

Convention: C[i, j] = mean_t z_i(t) z_j(t + lag) (lag in grid samples; with the
2.0 s grid, lag 1 = 2 s).  F = C - C^T is antisymmetric; F[i, j] > 0 means "i
leads j" and becomes the directed edge i -> j.  Reversing time gives exactly
F -> -F (C_rev = C^T).
"""
from __future__ import annotations

import numpy as np


def lagged_net_flow(Z: np.ndarray, lag_samples: int = 1) -> np.ndarray:
    if lag_samples < 1 or Z.shape[0] <= lag_samples + 1:
        raise ValueError("series too short for the requested lag")
    T = Z.shape[0]
    C = Z[:-lag_samples].T @ Z[lag_samples:] / float(T - lag_samples)
    F = C - C.T
    np.fill_diagonal(F, 0.0)
    return F


def lag_seconds_to_samples(lag_s: float, grid_dt: float) -> int:
    k = lag_s / grid_dt
    if abs(k - round(k)) > 1e-9 or round(k) < 1:
        raise ValueError(f"lag {lag_s} s is not a positive multiple of the {grid_dt} s grid")
    return int(round(k))


def n_edges_for_density(n_nodes: int, density: float) -> int:
    """Exact edge count: round(density * N(N-1)/2) (density over unordered pairs)."""
    return int(round(density * n_nodes * (n_nodes - 1) / 2))


def oriented_topk_graph(F: np.ndarray, density: float) -> np.ndarray:
    """Keep the k = round(density*N(N-1)/2) pairs with largest |F| (stable order),
    oriented by sign(F). Returns an int8 adjacency with no mutual edges / self-loops."""
    N = F.shape[0]
    iu, ju = np.triu_indices(N, 1)
    vals = F[iu, ju]
    k = n_edges_for_density(N, density)
    if k < 1 or k > vals.size:
        raise ValueError("density gives an invalid edge count")
    order = np.argsort(-np.abs(vals), kind="stable")[:k]
    if not np.all(np.abs(vals[order]) > 0):
        raise ValueError("selected pair with F == 0 (orientation undefined)")
    i, j, v = iu[order], ju[order], vals[order]
    pos = v > 0
    src = np.where(pos, i, j)
    dst = np.where(pos, j, i)
    A = np.zeros((N, N), dtype=np.int8)
    A[src, dst] = 1
    return A


def gradient_component(F: np.ndarray) -> np.ndarray:
    """Least-squares gradient (Hodge) part of an antisymmetric flow on the complete graph:
    potential p_i = mean_j F[i, j]; G[i, j] = p_i - p_j."""
    p = F.mean(axis=1)
    G = p[:, None] - p[None, :]
    np.fill_diagonal(G, 0.0)
    return G


def gradient_share(F: np.ndarray) -> float:
    G = gradient_component(F)
    denom = float(np.sum(F * F))
    return float(np.sum(G * G) / denom) if denom > 0 else float("nan")


def curl_component(F: np.ndarray) -> np.ndarray:
    return F - gradient_component(F)
