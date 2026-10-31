"""Topic 3 Family B — token-level spectra on SwiFT E192 frame dumps, run IN PLACE on connectome
(system python 3.8 + numpy; no torch) under Slurm. Ships as code only; data never leave connectome
except the position-keyed summaries written to --out-dir.

Contract (halts with a non-zero exit and writes NO spectra if any check fails):
  1. subject directories are listed in sorted order and mapped to positions in memory only;
  2. --reference-root: the subject-directory list equals the primary checkpoint's (boolean only);
  3. --check-npz-root: the pooled layer npz files there match the sha256 pins and their row order
     equals the sorted directory order (boolean only); after the pass, every subject's re-pooled
     L0..L3 vector equals its npz row (allclose atol=rtol=1e-5; max |diff| recorded);
  4. every subject has exactly 7 frames with the expected shapes.
Outputs: <out-dir>/<label>_token_spectra.npz (positions + arrays) and <label>_token_job.json.
Never prints or writes subject directory names.

Usage (on connectome, from the shipped code root):
  python3 scripts/topic3_token_job.py --frames-root <dir> --label <label> --out-dir <dir> \
      [--reference-root <dir>] [--check-npz-root <dir>] [--workers 12]
"""
import argparse
import glob
import hashlib
import json
import multiprocessing as mp
import os
import platform
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

from src.topic3_spectral import io_contract as io  # noqa: E402
from src.topic3_spectral.token_job import VARIANTS, pack_summaries, subject_summary  # noqa: E402

SEED = 20261031
LAYER_PINS = ("L0", "L1", "L2", "L3")


def list_subjects(root):
    return sorted(d for d in os.listdir(root) if d.startswith("sub-") and os.path.isdir(os.path.join(root, d)))


def _work(args):
    root, name, pos = args
    frames = sorted(glob.glob(os.path.join(root, name, "frame*.pt")))
    loaded = [io.load_pt_numpy(f) for f in frames]
    return subject_summary(loaded, pos, SEED)


def code_hashes():
    files = sorted(glob.glob(os.path.join(ROOT, "src", "topic3_spectral", "*.py"))) + [os.path.abspath(__file__)]
    return {os.path.relpath(f, ROOT): io.sha256_file(f) for f in files}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames-root", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--reference-root", default=None)
    ap.add_argument("--check-npz-root", default=None)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    t0 = time.time()
    rec = {"label": a.label, "python": platform.python_version(), "numpy": np.__version__,
           "host": platform.node(), "seed": SEED, "code_sha256": code_hashes(), "checks": {}}
    names = list_subjects(a.frames_root)
    rec["n_subjects"] = len(names)
    halt = []
    if a.reference_root:
        same = names == list_subjects(a.reference_root)
        rec["checks"]["same_subject_set_as_reference"] = bool(same)
        if not same:
            halt.append("subject set differs from reference")
    npz_X = None
    if a.check_npz_root:
        npz_X = {}
        for k in LAYER_PINS:
            fname = os.path.basename(io.PINNED[k][0])
            path = os.path.join(a.check_npz_root, fname)
            try:
                npz_X[k] = io.load_X(path, io.PINNED[k][1])
                rec["checks"]["pin_ok_" + k] = True
            except (FileNotFoundError, ValueError):
                rec["checks"]["pin_ok_" + k] = False
                halt.append("pinned npz check failed for " + k)
        if not halt:
            ok = io.ids_order_matches_names(os.path.join(a.check_npz_root, "layer_0.npz"), io.PINNED["L0"][1], names)
            rec["checks"]["npz_row_order_equals_sorted_dirs"] = ok
            if not ok:
                halt.append("npz row order differs")
    nfr = [len(glob.glob(os.path.join(a.frames_root, n, "frame*.pt"))) for n in names]
    rec["checks"]["frames_per_subject_min_max"] = [int(min(nfr)), int(max(nfr))] if nfr else [0, 0]
    if not nfr or min(nfr) != 7 or max(nfr) != 7:
        halt.append("frame count != 7")
    os.makedirs(a.out_dir, exist_ok=True)
    jpath = os.path.join(a.out_dir, "%s_token_job.json" % a.label)
    if halt:
        rec["halted"] = halt
        json.dump(rec, open(jpath, "w"), indent=1)
        print(json.dumps({"halted": halt}))
        sys.exit(2)
    with mp.Pool(a.workers) as pool:
        sums = pool.map(_work, [(a.frames_root, n, i) for i, n in enumerate(names)], chunksize=1)
    del names
    rec["compute_seconds"] = round(time.time() - t0, 1)
    if npz_X is not None:
        diffs = {}
        allok = True
        for k, v in zip(LAYER_PINS, ("L0", "L1", "L2", "L3")):
            P = np.stack([s["pooled"][v] for s in sorted(sums, key=lambda s: s["position"])])
            diffs[k] = float(np.max(np.abs(P - npz_X[k])))
            allok &= bool(np.allclose(P, npz_X[k], atol=1e-5, rtol=1e-5))
        rec["checks"]["repool_max_abs_diff"] = diffs
        rec["checks"]["repool_allclose_all_subjects"] = bool(allok)
        if not allok:
            rec["halted"] = ["re-pooled vectors differ from npz"]
            json.dump(rec, open(jpath, "w"), indent=1)
            print(json.dumps({"halted": rec["halted"]}))
            sys.exit(3)
    arrs = pack_summaries(sums, VARIANTS)
    npath = os.path.join(a.out_dir, "%s_token_spectra.npz" % a.label)
    np.savez(npath, **arrs)
    h = hashlib.sha256(open(npath, "rb").read()).hexdigest()
    rec["outputs"] = {"spectra_npz": os.path.basename(npath), "spectra_sha256": h}
    rec["runtime_s"] = round(time.time() - t0, 1)
    json.dump(rec, open(jpath, "w"), indent=1)
    print(json.dumps({"label": a.label, "n_subjects": rec["n_subjects"], "checks": rec["checks"],
                      "runtime_s": rec["runtime_s"]}))


if __name__ == "__main__":
    main()
