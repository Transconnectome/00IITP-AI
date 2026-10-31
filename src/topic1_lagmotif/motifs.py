"""Oriented triad census and an orientation- and degree-preserving null model.

Oriented graphs (no mutual edges, no self-loops) can only contain the triad
classes 003, 012, 021D, 021U, 021C, 030T, 030C.  The significance profile is
therefore computed over the five *connected* oriented classes
``CLASSES = (021D, 021U, 021C, 030T, 030C)``; the 8 classes needing a mutual
edge (111D, 111U, 201, 120D, 120U, 120C, 210, 300) are structurally zero in
both the observed and every null graph and are excluded.

Closed-form census (A = adjacency, no mutual edges):
  030C = tr(A^3)/3,  030T = sum(A o A^2),
  021D = sum C(k_out, 2) - 030T,  021U = sum C(k_in, 2) - 030T,
  021C = sum k_in k_out - 3*030C - 030T.
Because the null preserves every in/out degree, 021D, 021U and 021C are affine
in (030T, 030C) across nulls, hence exactly Z(021D) = Z(021U) = -Z(030T) and
the 5-class SP has rank 2.  Only Z(030C) and Z(030T) are free.

Null chain (numba, nopython, cache=False so nothing is written to disk):
  * state = labelled edge list (src[e], dst[e]) + dense int8 adjacency;
  * each ATTEMPT (rejections count as steps; lazy chain) picks, with
    probability 1 - p_rot, an ordered pair of edge slots (u->v, w->z) and
    proposes (u->z, w->v) [2-swap]; with probability p_rot an ordered triple
    (u1->v1, u2->v2, u3->v3) and proposes (u1->v2, u2->v3, u3->v1)
    [3-edge target rotation, which contains directed-triangle reversal and the
    path move a->b->c->d => a->c->b->d];
  * a proposal is accepted iff, after removing the old edges, every new edge
    is not a self-loop and is absent IN EITHER DIRECTION and the new edges are
    pairwise neither equal nor reversed.  Both proposals are symmetric
    (the inverse move is drawn with the same probability), so the uniform
    distribution over oriented graphs with the observed in/out degree sequence
    is stationary on the component reachable from the observed graph.
    Irreducibility of this move set on oriented graphs is NOT established
    (exhaustive N=5 enumeration by explorers leaves 60/12,382 degree classes
    reducible); this is recorded as an open limitation.
  * each null is an independent restart from the observed graph with
    ``attempts_factor * m`` attempts and its own seed;
  * every null graph is checked in int64 for: identical in/out degrees, zero
    self-loops, zero mutual edges, edge count m, and edge-list/adjacency
    consistency.  Any violation raises ``NullInvariantError``.
"""
from __future__ import annotations

import numpy as np
from numba import njit

CLASSES = ("021D", "021U", "021C", "030T", "030C")


class NullInvariantError(AssertionError):
    pass


def census(A: np.ndarray) -> dict[str, int]:
    A64 = np.asarray(A, dtype=np.int64)
    if np.any(np.diag(A64)) or np.any(A64 * A64.T):
        raise ValueError("census requires an oriented graph (no self-loops, no mutual edges)")
    kout = A64.sum(axis=1)
    kin = A64.sum(axis=0)
    A2 = A64 @ A64
    c030C = int(np.trace(A2 @ A64)) // 3
    c030T = int(np.sum(A2 * A64))
    s_out = int(np.sum(kout * (kout - 1) // 2))
    s_in = int(np.sum(kin * (kin - 1) // 2))
    p2 = int(np.sum(kin * kout))
    return {"021D": s_out - c030T, "021U": s_in - c030T, "021C": p2 - 3 * c030C - c030T,
            "030T": c030T, "030C": c030C}


@njit(cache=False)
def _new_edges_ok(A, a, b, n):
    # a, b: arrays of length n with new edges a[i] -> b[i]; old edges already removed from A
    for i in range(n):
        if a[i] == b[i]:
            return False
        if A[a[i], b[i]] != 0 or A[b[i], a[i]] != 0:
            return False
        for j in range(i + 1, n):
            if a[i] == a[j] and b[i] == b[j]:
                return False
            if a[i] == b[j] and b[i] == a[j]:
                return False
    return True


@njit(cache=False)
def _run_chain(A, src, dst, n_attempts, p_rot):
    m = src.shape[0]
    na = np.empty(3, dtype=np.int64)
    nb = np.empty(3, dtype=np.int64)
    accepted = 0
    for _ in range(n_attempts):
        if np.random.random() < p_rot:
            i = np.random.randint(m)
            j = np.random.randint(m)
            k = np.random.randint(m)
            if i == j or j == k or i == k:
                continue
            u1 = src[i]; v1 = dst[i]; u2 = src[j]; v2 = dst[j]; u3 = src[k]; v3 = dst[k]
            A[u1, v1] = 0; A[u2, v2] = 0; A[u3, v3] = 0
            na[0] = u1; nb[0] = v2; na[1] = u2; nb[1] = v3; na[2] = u3; nb[2] = v1
            if _new_edges_ok(A, na, nb, 3):
                A[u1, v2] = 1; A[u2, v3] = 1; A[u3, v1] = 1
                dst[i] = v2; dst[j] = v3; dst[k] = v1
                accepted += 1
            else:
                A[u1, v1] = 1; A[u2, v2] = 1; A[u3, v3] = 1
        else:
            i = np.random.randint(m)
            j = np.random.randint(m)
            if i == j:
                continue
            u = src[i]; v = dst[i]; w = src[j]; z = dst[j]
            A[u, v] = 0; A[w, z] = 0
            na[0] = u; nb[0] = z; na[1] = w; nb[1] = v
            if _new_edges_ok(A, na, nb, 2):
                A[u, z] = 1; A[w, v] = 1
                dst[i] = z; dst[j] = v
                accepted += 1
            else:
                A[u, v] = 1; A[w, z] = 1
    return accepted


@njit(cache=False)
def _check_invariants(A, src, dst, kin0, kout0, m):
    """0 = ok; 1 degree; 2 self-loop; 3 mutual; 4 edge count; 5 list/adjacency mismatch."""
    N = A.shape[0]
    total = 0
    for i in range(N):
        if A[i, i] != 0:
            return 2
        ko = 0
        for j in range(N):
            a = np.int64(A[i, j])
            if a != 0 and a != 1:
                return 5
            ko += a
            if a != 0 and A[j, i] != 0:
                return 3
        if ko != kout0[i]:
            return 1
        total += ko
    for j in range(N):
        ki = 0
        for i in range(N):
            ki += np.int64(A[i, j])
        if ki != kin0[j]:
            return 1
    if total != m:
        return 4
    for e in range(m):
        if A[src[e], dst[e]] != 1:
            return 5
    return 0


@njit(cache=False)
def _count_030(A, src, dst):
    N = A.shape[0]
    m = src.shape[0]
    c = np.int64(0)
    t = np.int64(0)
    for e in range(m):
        u = src[e]; v = dst[e]
        for w in range(N):
            if A[v, w] != 0:
                if A[w, u] != 0:
                    c += 1
                if A[u, w] != 0:
                    t += 1
    return t, c // 3


@njit(cache=False)
def _null_ensemble(A0, src0, dst0, kin0, kout0, n_attempts, p_rot, seeds):
    n = seeds.shape[0]
    m = src0.shape[0]
    out_t = np.empty(n, dtype=np.int64)
    out_c = np.empty(n, dtype=np.int64)
    acc = np.empty(n, dtype=np.int64)
    flags = np.empty(n, dtype=np.int64)
    for r in range(n):
        np.random.seed(seeds[r])
        A = A0.copy(); src = src0.copy(); dst = dst0.copy()
        acc[r] = _run_chain(A, src, dst, n_attempts, p_rot)
        flags[r] = _check_invariants(A, src, dst, kin0, kout0, m)
        t, c = _count_030(A, src, dst)
        out_t[r] = t; out_c[r] = c
    return out_t, out_c, acc, flags


def _edge_list(A: np.ndarray):
    A8 = np.ascontiguousarray(A, dtype=np.int8)
    src, dst = np.nonzero(A8)
    return A8, src.astype(np.int64), dst.astype(np.int64)


_FLAG_TEXT = {1: "degree sequence changed", 2: "self-loop", 3: "mutual edge", 4: "edge count changed",
              5: "edge list / adjacency mismatch"}


def sample_null_graph(A: np.ndarray, attempts_factor: float, p_rot: float, seed: int) -> np.ndarray:
    """One null graph (for tests / inspection); invariants checked."""
    A8, src, dst = _edge_list(A)
    A64 = A8.astype(np.int64)
    kin0, kout0 = A64.sum(axis=0), A64.sum(axis=1)
    Aw, sw, dw = A8.copy(), src.copy(), dst.copy()
    _seed_numba(int(seed))
    _run_chain(Aw, sw, dw, int(round(attempts_factor * len(src))), float(p_rot))
    flag = _check_invariants(Aw, sw, dw, kin0, kout0, len(src))
    if flag:
        raise NullInvariantError(_FLAG_TEXT[int(flag)])
    return Aw


@njit(cache=False)
def _seed_numba(seed):
    np.random.seed(seed)


def null_counts(A: np.ndarray, n_null: int, attempts_factor: float, p_rot: float,
                seeds: np.ndarray) -> dict[str, np.ndarray]:
    """Run ``n_null`` independent restarts; return per-null 030T/030C and acceptance rates.
    Raises NullInvariantError if any null violates an invariant."""
    A8, src, dst = _edge_list(A)
    m = len(src)
    A64 = A8.astype(np.int64)
    kin0, kout0 = A64.sum(axis=0), A64.sum(axis=1)
    seeds = np.asarray(seeds, dtype=np.int64)
    if seeds.shape[0] != n_null:
        raise ValueError("need one seed per null")
    n_attempts = int(round(attempts_factor * m))
    t, c, acc, flags = _null_ensemble(A8, src, dst, kin0, kout0, n_attempts, float(p_rot), seeds)
    bad = np.flatnonzero(flags)
    if bad.size:
        raise NullInvariantError(f"null {int(bad[0])}: {_FLAG_TEXT[int(flags[bad[0]])]}")
    return {"030T": t, "030C": c, "acceptance": acc / max(n_attempts, 1), "n_attempts": n_attempts,
            "m": m, "s_out": int(np.sum(kout0 * (kout0 - 1) // 2)),
            "s_in": int(np.sum(kin0 * (kin0 - 1) // 2)), "p2": int(np.sum(kin0 * kout0))}


def motif_statistics(A: np.ndarray, n_null: int, attempts_factor: float, p_rot: float,
                     seeds: np.ndarray) -> dict:
    """Observed census, null moments, Z (NaN + flag if null SD == 0), SP over CLASSES,
    endpoints E1 = Z030C, E2 = Z030C - Z030T, and degeneracy-safe log ratio for 030C."""
    obs = census(A)
    nc = null_counts(A, n_null, attempts_factor, p_rot, seeds)
    t, c = nc["030T"].astype(np.float64), nc["030C"].astype(np.float64)
    null = {"030T": t, "030C": c, "021D": nc["s_out"] - t, "021U": nc["s_in"] - t,
            "021C": nc["p2"] - 3.0 * c - t}
    mean = {k: float(np.mean(null[k])) for k in CLASSES}
    sd = {k: float(np.std(null[k], ddof=1)) for k in CLASSES}
    Z = {k: ((obs[k] - mean[k]) / sd[k]) if sd[k] > 0 else float("nan") for k in CLASSES}
    zv = np.array([Z[k] for k in CLASSES])
    norm = float(np.sqrt(np.nansum(zv ** 2)))
    SP = {k: (Z[k] / norm if (norm > 0 and np.isfinite(Z[k])) else float("nan")) for k in CLASSES}
    return {
        "observed": obs, "null_mean": mean, "null_sd": sd, "Z": Z, "SP": SP,
        "E1_Z030C": Z["030C"], "E2_Z030C_minus_Z030T": Z["030C"] - Z["030T"],
        "log_ratio_030C": float(np.log((obs["030C"] + 1.0) / (mean["030C"] + 1.0))),
        "degenerate": {k: bool(sd[k] == 0) for k in ("030T", "030C")},
        "acceptance_mean": float(np.mean(nc["acceptance"])), "n_attempts": nc["n_attempts"],
        "m": nc["m"], "n_null": int(n_null),
    }
