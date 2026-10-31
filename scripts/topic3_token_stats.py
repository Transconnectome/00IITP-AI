"""Topic 3 Family B — statistics on the position-keyed token spectra returned from connectome
(frozen card §5). Refuses to run unless the card hash verifies and every job record passed its
contract checks. Writes results/topic3/2026-10-31/family_B_token_level.json.
Run: cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=4 \
     nice -n 10 /home/juke/superclaude-env/bin/python3 scripts/topic3_token_stats.py
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

from topic3_common import OUT, dump, run_record, sha256, verify_card  # noqa: E402
from src.topic3_spectral import analysis, io_contract as io  # noqa: E402

PRIMARY = "E192_primary"
ZOO = ("zoo_HCP_N400_T2400_E192", "zoo_NewUAH_deepE192_L1e-4", "zoo_NewUAH_deepE192_L5e-5")
TOKEN_DIR = os.path.join(OUT, "token_job")


def load_checkpoint(label):
    rec = json.load(open(os.path.join(TOKEN_DIR, "%s_token_job.json" % label)))
    if "halted" in rec or "outputs" not in rec:
        sys.exit("job %s halted or incomplete: refusing" % label)
    npz = os.path.join(TOKEN_DIR, rec["outputs"]["spectra_npz"])
    if sha256(npz) != rec["outputs"]["spectra_sha256"]:
        sys.exit("spectra hash mismatch for %s" % label)
    z = np.load(npz, allow_pickle=False)
    arrs = {k: z[k] for k in z.files}
    if not np.array_equal(arrs["positions"], np.arange(57)):
        sys.exit("positions incomplete for %s" % label)
    return rec, arrs


def main():
    card = verify_card()
    t0 = time.time()
    run = run_record(os.path.abspath(__file__))
    run["card_sha256_verified"] = card
    run["params"] = analysis.PARAMS
    calib = json.load(open(os.path.join(OUT, "alpha_calibration_synthetic.json")))
    alpha_ok = calib["token_variant_alpha_reportable"]
    per, jobs, a1b = {}, {}, {}
    for i, label in enumerate((PRIMARY,) + ZOO):
        rec, arrs = load_checkpoint(label)
        jobs[label] = {"checks": rec["checks"], "n_subjects": rec["n_subjects"], "spectra_sha256": rec["outputs"]["spectra_sha256"],
                       "python": rec["python"], "numpy": rec["numpy"], "runtime_s": rec.get("runtime_s")}
        per[label] = analysis.token_level_checkpoint(arrs, analysis.PARAMS["seed"] + 1000 * i, analysis.PARAMS, alpha_ok)
        a1b[label] = analysis.ln_matched_subject_level(arrs["pooled__L3"], arrs["pooled__LN0L2"], analysis.PARAMS)
        if label == PRIMARY:
            local_L3 = io.load_pinned("L3")
            jobs[label]["pooled_L3_equals_local_npz"] = bool(np.allclose(arrs["pooled__L3"], local_L3, atol=1e-5, rtol=1e-5))
            if not jobs[label]["pooled_L3_equals_local_npz"]:
                sys.exit("primary pooled L3 does not equal local npz: halt")
    if not jobs[PRIMARY]["checks"].get("repool_allclose_all_subjects"):
        sys.exit("primary re-pool provenance check missing or failed: halt")
    verdicts = analysis.replication_verdict(per, PRIMARY, analysis.PARAMS)
    run["runtime_s"] = round(time.time() - t0, 1)
    print(dump({"run": run, "jobs": jobs, "per_checkpoint": per, "A1b_ln_matched_subject_level": a1b,
                "H1_replication_verdicts": verdicts}, "family_B_token_level.json"))


if __name__ == "__main__":
    main()
