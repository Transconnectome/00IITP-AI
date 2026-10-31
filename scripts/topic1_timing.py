#!/usr/bin/env python3
"""A3 timing: Topic 1 lag-motif extractor v2 on 5 real subjects, local CPU only.

Subject selection rule (stated before running): for each TR group in
(0.7, 0.85, 1.0, 1.8, 2.0) s, the lowest positional index (into
sorted(os.listdir(npy_dir))) whose site has that TR.  Only Unique_ID->Sample is
read from the metadata (no diagnosis or other phenotype).  Outputs contain
positional indices, TR, valid length and computational quantities only: no
participant IDs, no paths, no feature values (Z/SP/raw counts), no group
statistics.  Feature values are computed (that is what is being timed) but
discarded; only |dZ| between two null settings of the same subject is logged
as a Monte-Carlo/mixing diagnostic.

Usage:
  PYTHONDONTWRITEBYTECODE=1 python scripts/topic1_timing.py --outdir results/topic1/2026-10-30
"""
import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import platform  # noqa: E402
import resource  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.topic1_lagmotif import motifs  # noqa: E402
from src.topic1_lagmotif.data import NpyCohort  # noqa: E402
from src.topic1_lagmotif.flow import curl_component, gradient_share, oriented_topk_graph  # noqa: E402
from src.topic1_lagmotif.pipeline import PARAMS, null_seeds, params_sha256, subject_flow  # noqa: E402

ENIGMA = "/home/juke/git/enigma_ocd_mbbn"
NPY_DIR = os.path.join(ENIGMA, "data", "MBBN_data_304_ROIs_0.25")
META = os.path.join(ENIGMA, "data", "metadata", "ENIGMA_QC_final_subject_list.csv")
TR_GROUPS = (0.7, 0.85, 1.0, 1.8, 2.0)
N_COHORT = 1706


def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def select_positions(coh):
    chosen = {}
    for i in range(len(coh)):
        tr = coh.tr(i)
        if tr in TR_GROUPS and tr not in chosen:
            chosen[tr] = i
        if len(chosen) == len(TR_GROUPS):
            break
    return [chosen[t] for t in TR_GROUPS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--alt-attempts-factor", type=float, default=40.0)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    log_path = os.path.join(a.outdir, "a3_timing_raw.log")
    logf = open(log_path, "w")

    def log(msg):
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())}Z {msg}"
        print(line, flush=True)
        logf.write(line + "\n"); logf.flush()

    log(f"host={platform.node()} cpus={os.cpu_count()} python={platform.python_version()} "
        f"numpy={np.__version__} threads_pinned=1 params_sha256={params_sha256()}")
    n_null, af, p_rot = PARAMS["n_null"], PARAMS["attempts_factor"], PARAMS["p_rot"]
    densities = [PARAMS["density_primary"]] + list(PARAMS["density_sensitivity"])
    channels = list(PARAMS["channels"])

    # numba compile time, measured separately on a tiny synthetic graph
    t0 = time.perf_counter()
    A_tiny = np.zeros((4, 4), np.int8); A_tiny[0, 1] = A_tiny[1, 2] = A_tiny[2, 0] = 1
    motifs.motif_statistics(A_tiny, 3, 2, 0.2, np.arange(3))
    compile_s = time.perf_counter() - t0
    log(f"numba_compile_s={compile_s:.3f}")

    t0 = time.perf_counter()
    coh = NpyCohort.from_metadata(NPY_DIR, META, trim_s=PARAMS["head_trim_s"])
    positions = select_positions(coh)
    log(f"metadata_and_selection_s={time.perf_counter() - t0:.3f} n_cohort={len(coh)} positions={positions}")

    subjects = []
    for pos in positions:
        rec = {"position": pos, "stages_s": {}, "units": {}}
        t0 = time.perf_counter(); s = coh.load(pos); rec["stages_s"]["load"] = time.perf_counter() - t0
        rec.update({"tr": s.tr, "raw_valid_T": s.raw_valid_T, "n_trim": s.n_trim, "valid_T": s.valid_T,
                    "duration_s": s.duration_s})
        t0 = time.perf_counter(); F = subject_flow(s); rec["stages_s"]["preprocess_flow"] = time.perf_counter() - t0
        t0 = time.perf_counter(); gradient_share(F); Fcurl = curl_component(F)
        rec["stages_s"]["hodge"] = time.perf_counter() - t0
        for ch in channels:
            Fc = F if ch == "broadband" else Fcurl
            for d in densities:
                key = f"{ch}@{d:.2f}"
                t0 = time.perf_counter(); A = oriented_topk_graph(Fc, d); tg = time.perf_counter() - t0
                seeds = null_seeds(PARAMS["base_seed"], pos, ch, d, n_null)
                t0 = time.perf_counter()
                r = motifs.motif_statistics(A, n_null, af, p_rot, seeds)
                tn = time.perf_counter() - t0
                u = {"graph_s": tg, "nulls_s": tn, "n_null": n_null, "attempts_factor": af, "m": r["m"],
                     "acceptance": r["acceptance_mean"], "degenerate_030C": r["degenerate"]["030C"],
                     "degenerate_030T": r["degenerate"]["030T"]}
                if ch == "broadband" and d == PARAMS["density_primary"]:
                    # mixing / MC diagnostics on the primary unit only (differences, not values)
                    half = n_null // 2
                    ra = motifs.motif_statistics(A, half, af, p_rot, seeds[:half])
                    rb = motifs.motif_statistics(A, half, af, p_rot, seeds[half:])
                    u["abs_dZ030C_split_half"] = abs(ra["Z"]["030C"] - rb["Z"]["030C"])
                    t0 = time.perf_counter()
                    r2 = motifs.motif_statistics(A, n_null, a.alt_attempts_factor, p_rot, seeds)
                    u["nulls_s_alt_factor"] = time.perf_counter() - t0
                    u["alt_attempts_factor"] = a.alt_attempts_factor
                    u["abs_dZ030C_factor"] = abs(r2["Z"]["030C"] - r["Z"]["030C"])
                    u["abs_dZ030T_factor"] = abs(r2["Z"]["030T"] - r["Z"]["030T"])
                    del ra, rb, r2
                del r
                rec["units"][key] = u
                log(f"pos={pos} tr={s.tr} valid_T={s.valid_T} unit={key} m={u['m']} graph_s={tg:.3f} "
                    f"nulls_s={tn:.3f} acc={u['acceptance']:.3f} degenerate={u['degenerate_030C'] or u['degenerate_030T']}"
                    + (f" alt_factor_nulls_s={u['nulls_s_alt_factor']:.3f} |dZ030C|_factor={u['abs_dZ030C_factor']:.3f}"
                       f" |dZ030C|_splithalf={u['abs_dZ030C_split_half']:.3f}" if 'nulls_s_alt_factor' in u else ""))
        planned = (rec["stages_s"]["load"] + rec["stages_s"]["preprocess_flow"] + rec["stages_s"]["hodge"]
                   + sum(v["graph_s"] + v["nulls_s"] for v in rec["units"].values()))
        rec["planned_total_s"] = planned
        rec["peak_rss_mb_after"] = peak_rss_mb()
        log(f"pos={pos} planned_total_s={planned:.2f} peak_rss_mb={rec['peak_rss_mb_after']:.1f}")
        subjects.append(rec)

    per_unit = np.mean([[v["graph_s"] + v["nulls_s"] for v in r["units"].values()] for r in subjects], axis=0)
    mean_total = float(np.mean([r["planned_total_s"] for r in subjects]))
    overhead = float(np.mean([r["stages_s"]["load"] + r["stages_s"]["preprocess_flow"] + r["stages_s"]["hodge"]
                              for r in subjects]))
    primary_unit = float(np.mean([r["units"][f"broadband@{PARAMS['density_primary']:.2f}"]["graph_s"]
                                  + r["units"][f"broadband@{PARAMS['density_primary']:.2f}"]["nulls_s"]
                                  for r in subjects]))
    summary = {
        "label": "추정 (extrapolated from 5 subjects; single core; excludes numba compile per process)",
        "n_units_per_subject": len(channels) * len(densities),
        "mean_subject_total_s_all_units": mean_total,
        "mean_overhead_s_load_preprocess_hodge": overhead,
        "mean_unit_s": float(per_unit.mean()),
        "cpu_h_full_cohort_all_units_추정": mean_total * N_COHORT / 3600.0,
        "cpu_h_full_cohort_primary_unit_only_추정": (overhead + primary_unit) * N_COHORT / 3600.0,
        "cpu_h_per_unit_channel_density_추정": float(per_unit.mean()) * N_COHORT / 3600.0,
        "wall_h_on_16_cores_all_units_추정": mean_total * N_COHORT / 3600.0 / 16,
        "peak_rss_mb": peak_rss_mb(),
        "numba_compile_s": compile_s,
    }
    out = {"run": "tw-20261030-topic1 A3", "params": PARAMS, "params_sha256": params_sha256(),
           "selection_rule": "lowest positional index per TR group (0.7, 0.85, 1.0, 1.8, 2.0)",
           "subjects": subjects, "summary": summary,
           "privacy": "positional indices only; no IDs, paths, diagnosis labels, feature values or group statistics"}
    with open(os.path.join(a.outdir, "a3_timing.json"), "w") as f:
        json.dump(out, f, indent=1)
    log("summary " + json.dumps(summary, ensure_ascii=False))
    logf.close()


if __name__ == "__main__":
    main()
