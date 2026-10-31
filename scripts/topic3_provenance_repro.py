"""Topic 3 T3.1 — input provenance + exact REPRODUCTION of the already-public old numbers.

This is a reproduction of numbers that were already published in
docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md (centered PR / old alpha) and
docs/03_empirical_analysis/empirical_results.json (uncentered PR / HTSR alpha). It computes no new
estimand. Old functions are imported read-only from the protected modules.

Writes results/topic3/2026-10-31/t3_1_provenance_repro.json (no identifiers; positions only).
Run: cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
     /home/juke/superclaude-env/bin/python3 scripts/topic3_provenance_repro.py
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

from src.topic3_spectral import io_contract as io  # noqa: E402
from src.topic3_spectral.estimators import mean_energy_fraction  # noqa: E402

OUT_DIR = os.path.join(ROOT, "results", "topic3", "2026-10-31")
JSON_KEYS = {"L0": "SwiFT_E192_Layer0", "L1": "SwiFT_E192_Layer1", "L2": "SwiFT_E192_Layer2",
             "L3": "SwiFT_E192_Layer3", "BrainLM": "BrainLM_Pooled", "BrainJEPA": "BrainJEPA_Pooled",
             "NeuroSTORM": "NeuroSTORM_Pooled"}
# Report table (EMPIRICAL_ANALYSIS_REPORT.md lines 68-74): (PR, alpha), transcribed for comparison only.
REPORT_TABLE = {"L0": (2.7773, 1.4717), "L1": (2.7782, 0.9887), "L2": (11.0202, 1.5980),
                "L3": (3.5786, 1.8411), "BrainLM": (4.3188, 1.4580), "BrainJEPA": (11.7851, 1.8807),
                "NeuroSTORM": (12.5070, 1.1960)}
EXTRA_HASHES = {
    "ver11_model": "/home/juke/git/SwiFT_v2/project/module/models/simmim_swin4d_transformer_ver11.py",
    "pool_E192_layersweep": "/home/juke/git/VRABES/RemissionAnalysis/pool_E192_layersweep.py",
    "extract_vrabes_swift_E192_sh": "/home/juke/git/VRABES/RemissionAnalysis/extract_vrabes_swift_E192.sh",
    "extract_brainlm": "/home/juke/git/VRABES/RemissionAnalysis/extract_brainlm_embeddings.py",
    "extract_brainjepa": "/home/juke/git/VRABES/RemissionAnalysis/extract_brainjepa_embeddings.py",
    "extract_neurostorm": "/home/juke/git/VRABES/RemissionAnalysis/extract_neurostorm_embeddings.py",
    "protected_srg": os.path.join(ROOT, "src", "spectral_rg_flow_diagnostic.py"),
    "protected_eca": os.path.join(ROOT, "src", "empirical_connectome_ablation.py"),
    "protected_json": os.path.join(ROOT, "docs", "03_empirical_analysis", "empirical_results.json"),
}


def main():
    from src.empirical_connectome_ablation import estimate_powerlaw_alpha  # centered (report)
    from src.spectral_rg_flow_diagnostic import (compute_participation_ratio,  # uncentered (json)
                                                 fit_htsr_powerlaw_alpha)
    t0 = time.time()
    old_json = json.load(open(os.path.join(ROOT, "docs", "03_empirical_analysis", "empirical_results.json")))
    q = old_json["analysis_3_foundation_model_rg_flow"]
    inputs, repro = {}, {}
    for name, (rel, sha) in io.PINNED.items():
        path = os.path.join(io.VRABES_RA, rel)
        X = io.load_pinned(name)          # raises on missing file / hash mismatch
        z = np.load(path, allow_pickle=False)
        keys = sorted(z.files)
        dtype = str(z["X"].dtype)
        z.close()
        inputs[name] = {"path": path, "sha256": sha, "sha256_verified": True, "keys": keys,
                        "X_dtype": dtype, "shape": list(X.shape),
                        "n_constant_columns": int(np.sum(X.std(axis=0) < 1e-12))}
        alpha_c, pr_c = estimate_powerlaw_alpha(X)
        pr_u = compute_participation_ratio(X)
        alpha_u, r2_u = fit_htsr_powerlaw_alpha(X)
        jk = q[JSON_KEYS[name]]
        rep_pr, rep_alpha = REPORT_TABLE[name]
        repro[name] = {
            "centered_pr_old_eca": round(pr_c, 4), "old_alpha_eca": round(alpha_c, 4),
            "report_pr": rep_pr, "report_alpha": rep_alpha,
            "report_pr_matches_4dp": abs(round(pr_c, 4) - rep_pr) < 1e-4,
            "report_alpha_matches_4dp": abs(round(alpha_c, 4) - rep_alpha) < 1.5e-4,
            "uncentered_pr_old_srg": round(pr_u, 4), "json_pr": jk["participation_ratio_PR"],
            "json_pr_matches_4dp": abs(round(pr_u, 4) - jk["participation_ratio_PR"]) < 1e-4,
            "uncentered_htsr_alpha_old_srg": round(alpha_u, 4), "json_alpha": jk["spectral_powerlaw_alpha"],
            "json_alpha_matches_4dp": abs(round(alpha_u, 4) - jk["spectral_powerlaw_alpha"]) < 1e-4,
            "mean_vector_energy_fraction": round(mean_energy_fraction(X), 4),
        }
    full = [(os.path.join(io.VRABES_RA, io.PINNED[k][0]), io.PINNED[k][1])
            for k in ("L0", "L1", "L2", "L3", "BrainLM", "BrainJEPA")]
    ns = (os.path.join(io.VRABES_RA, io.PINNED["NeuroSTORM"][0]), io.PINNED["NeuroSTORM"][1])
    align = io.positional_alignment(full, ns)
    extra = {k: {"path": p, "sha256": io.sha256_file(p)} for k, p in EXTRA_HASHES.items() if os.path.isfile(p)}
    missing_extra = [k for k, p in EXTRA_HASHES.items() if not os.path.isfile(p)]
    out = {
        "label": "T3.1 provenance + REPRODUCTION of already-public numbers (not a new result)",
        "inputs": inputs, "reproduction": repro, "alignment": align,
        "producer_and_code_hashes": extra, "missing_producer_files": missing_extra,
        "all_report_numbers_reproduced": all(r["report_pr_matches_4dp"] and r["report_alpha_matches_4dp"] for r in repro.values()),
        "all_json_numbers_reproduced": all(r["json_pr_matches_4dp"] and r["json_alpha_matches_4dp"] for r in repro.values()),
        "numpy": np.__version__, "python": sys.version.split()[0], "runtime_s": round(time.time() - t0, 2),
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "t3_1_provenance_repro.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"report_reproduced": out["all_report_numbers_reproduced"],
                      "json_reproduced": out["all_json_numbers_reproduced"],
                      "same_order": align["same_order"], "subset_increasing": align["subset_in_increasing_order"],
                      "out": path}))


if __name__ == "__main__":
    main()
