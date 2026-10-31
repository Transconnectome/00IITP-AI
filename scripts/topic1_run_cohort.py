#!/usr/bin/env python3
"""Topic 1 step 5: pinned manifest + label-free full-cohort feature extraction.

Governing documents (read-only):
  docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md      (frozen card, sha256 1e589f0b...75aa)
  docs/03_empirical_analysis/topic1/2026-10-31_topic1_prelabel_addendum.md  (manifest floor, variant definitions)

This script never reads a diagnosis or any other phenotype.  It reads the metadata only through
``NpyCohort.from_metadata`` (columns Unique_ID and Sample), and it never writes or prints a participant ID:
subjects are positional indices into sorted(os.listdir(npy_dir)); the name list is represented only by one
cohort-level salted sha256 digest.

Subcommands
  manifest   per-position site/TR/lengths/grid length/contract status + cohort digest  -> manifest.json
  extract    frozen-parameter extraction (resumable JSONL), one variant per call      -> extract_<variant>.jsonl
  status     progress of an extraction file

Variants (pre-label addendum section V; each is a full PARAMS dict, so its params_sha256 differs from the
frozen primary hash; restrictions on channels/densities and the truncation rule enter ``variant_sha``):
  primary   frozen PARAMS, extract_subject() with NO keyword overrides (all 2 channels x 3 densities)
            + static FC (upper-triangle Pearson of the same preprocessed 2 s series, card section 6 family 1)
  dct128    {**PARAMS, highpass_cutoff_s: 128.0}, broadband at --density
  af40      {**PARAMS, attempts_factor: 40},     broadband at --density
  trunc200  frozen PARAMS on the head-trimmed native series cut to floor(200/TR + 1e-9) samples
            (exactly 100 grid samples at every on-disk TR; asserted), broadband at --density

Usage (from the repo root):
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/topic1_run_cohort.py manifest --outdir results/topic1/2026-10-31
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/topic1_run_cohort.py extract --variant primary --workers 14 \
      --outdir results/topic1/2026-10-31 --fc-out <path outside git>/static_fc_upper_f32.npy
"""
import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import dataclasses  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import platform  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.topic1_lagmotif.data import NpyCohort  # noqa: E402
from src.topic1_lagmotif.pipeline import PARAMS, extract_subject, params_sha256  # noqa: E402
from src.topic1_lagmotif.preprocess import preprocess  # noqa: E402

ENIGMA = "/home/juke/git/enigma_ocd_mbbn"
NPY_DIR = os.path.join(ENIGMA, "data", "MBBN_data_304_ROIs_0.25")
META = os.path.join(ENIGMA, "data", "metadata", "ENIGMA_QC_final_subject_list.csv")
CARD = os.path.join(ROOT, "docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md")
CARD_SHA256 = "1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa"
FROZEN_PARAMS_SHA256 = "86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6"
N_COHORT = 1706
SALT = b"topic1-manifest-salt-2026-10-31:"   # public constant; the digest is cohort-level only
MIN_GRID_LEN = 100                            # = 200 s on the 2.0 s grid (pre-label addendum M2)
TRUNC_S = 200.0
VARIANTS = ("primary", "dct128", "af40", "trunc200")


# ----------------------------------------------------------------------------------------------- integrity
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_frozen_code() -> dict:
    """Card sha256 and the card section 12 code hashes must be unchanged; stop otherwise."""
    if sha256_file(CARD) != CARD_SHA256:
        raise SystemExit("frozen card hash mismatch: stop")
    pinned = {}
    with open(CARD) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and len(parts[0]) == 64 and all(c in "0123456789abcdef" for c in parts[0]):
                pinned[parts[1]] = parts[0]
    if len(pinned) != 10:
        raise SystemExit(f"expected 10 pinned code hashes in card section 12, found {len(pinned)}")
    for rel, h in pinned.items():
        if sha256_file(os.path.join(ROOT, rel)) != h:
            raise SystemExit(f"code hash mismatch for {rel}: stop")
    if params_sha256(PARAMS) != FROZEN_PARAMS_SHA256:
        raise SystemExit("PARAMS hash differs from the card: stop")
    return pinned


def cohort_digest(names) -> str:
    return hashlib.sha256(SALT + "\n".join(names).encode()).hexdigest()


def open_cohort() -> NpyCohort:
    return NpyCohort.from_metadata(NPY_DIR, META, trim_s=PARAMS["head_trim_s"])


def check_manifest(manifest: dict) -> None:
    names = sorted(os.listdir(NPY_DIR))
    if len(names) != manifest["n"] or len(names) != N_COHORT:
        raise SystemExit(f"cohort size changed: {len(names)} on disk vs {manifest['n']} in manifest")
    if cohort_digest(names) != manifest["cohort_digest"]:
        raise SystemExit("cohort name digest changed: positions/seeds would be remapped; stop")


# ----------------------------------------------------------------------------------------------- variants
def trunc_samples(tr: float) -> int:
    return int(math.floor(TRUNC_S / tr + 1e-9))


def variant_spec(variant: str, density: float | None) -> dict:
    if variant == "primary":
        return {"params": dict(PARAMS), "kw": {}, "truncate_native_s": None}
    if density is None:
        raise SystemExit(f"variant {variant} needs --density (the decided primary density)")
    kw = {"channels": ["broadband"], "densities": [float(density)]}
    if variant == "dct128":
        return {"params": {**PARAMS, "highpass_cutoff_s": 128.0}, "kw": kw, "truncate_native_s": None}
    if variant == "af40":
        return {"params": {**PARAMS, "attempts_factor": 40}, "kw": kw, "truncate_native_s": None}
    if variant == "trunc200":
        return {"params": dict(PARAMS), "kw": kw, "truncate_native_s": TRUNC_S}
    raise SystemExit(f"unknown variant {variant}")


def variant_sha(variant: str, spec: dict) -> str:
    blob = {"variant": variant, "params_sha256": params_sha256(spec["params"]), "kw": spec["kw"],
            "truncate_native_s": spec["truncate_native_s"],
            "truncation_rule": "floor(200/TR+1e-9) native samples after head trim" if spec["truncate_native_s"] else None}
    return hashlib.sha256(json.dumps(blob, sort_keys=True).encode()).hexdigest()


def grid_series(s, params) -> np.ndarray:
    return preprocess(s.X, s.tr, detrend_type=params["detrend"], padtype=params["padtype"],
                      highpass_cutoff_s=params["highpass_cutoff_s"], grid_dt=params["grid_dt_s"])


# ----------------------------------------------------------------------------------------------- manifest
def cmd_manifest(a):
    pinned = verify_frozen_code()
    t0 = time.time()
    names = sorted(os.listdir(NPY_DIR))
    coh = open_cohort()
    if len(coh) != len(names):
        raise SystemExit("cohort/listing mismatch")
    rows = []
    for pos in range(len(coh)):
        row = {"position": pos}
        try:
            site = coh.site(pos)
            row["site"] = site
            row["tr"] = coh.tr(pos)
            s = coh.load(pos)
            Z = grid_series(s, PARAMS)
            row.update({"raw_valid_T": s.raw_valid_T, "n_trim": s.n_trim, "valid_T": s.valid_T,
                        "duration_s": s.duration_s, "grid_len": int(Z.shape[0]), "contract_ok": True,
                        "error_class": None})
        except Exception as exc:  # noqa: BLE001 - class name only; messages could in principle carry paths
            row.update({"contract_ok": False, "error_class": type(exc).__name__})
        row["included"] = bool(row.get("contract_ok") and row.get("grid_len", 0) >= MIN_GRID_LEN)
        rows.append(row)
    ok = [r for r in rows if r["contract_ok"]]
    gl = np.array([r["grid_len"] for r in ok])
    man = {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "script": "scripts/topic1_run_cohort.py", "script_sha256": sha256_file(os.path.abspath(__file__)),
        "card_sha256": CARD_SHA256, "params_sha256": params_sha256(PARAMS), "card_s12_code_hashes": pinned,
        "n": len(names), "cohort_digest": cohort_digest(names),
        "cohort_digest_rule": "sha256(SALT + '\\n'.join(sorted(os.listdir(npy_dir)))) with the public SALT in this script",
        "min_grid_len": MIN_GRID_LEN, "min_grid_len_rule": "grid_len >= 100 (200 s on the 2.0 s grid)",
        "n_contract_ok": len(ok), "n_contract_errors": len(rows) - len(ok), "n_included": sum(r["included"] for r in rows),
        "n_below_floor": sum(1 for r in ok if r["grid_len"] < MIN_GRID_LEN),
        "grid_len_summary": {"min": int(gl.min()), "median": float(np.median(gl)), "max": int(gl.max())},
        "elapsed_s": round(time.time() - t0, 1), "rows": rows,
    }
    os.makedirs(a.outdir, exist_ok=True)
    out = os.path.join(a.outdir, "manifest.json")
    with open(out, "w") as f:
        json.dump(man, f, indent=1)
    print(json.dumps({k: v for k, v in man.items() if k not in ("rows", "card_s12_code_hashes")}, indent=1))
    print("sha256", sha256_file(out))


# ----------------------------------------------------------------------------------------------- extraction
_COH = None
_SPEC = None
_VARIANT = None


def _init(variant, density):
    global _COH, _SPEC, _VARIANT
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    _COH = open_cohort()
    _SPEC = variant_spec(variant, density)
    _VARIANT = variant


UNIT_KEYS = ("observed", "null_mean", "null_sd", "Z", "SP", "E1_Z030C", "E2_Z030C_minus_Z030T", "log_ratio_030C",
             "degenerate", "acceptance_mean", "n_attempts", "m", "n_null")


def _work(pos):
    t0 = time.time()
    try:
        s = _COH.load(pos)
        params = _SPEC["params"]
        if _SPEC["truncate_native_s"]:
            L = trunc_samples(s.tr)
            if s.valid_T < L:
                raise ValueError("series shorter than the truncation length")
            s = dataclasses.replace(s, X=np.ascontiguousarray(s.X[:L]), valid_T=L, duration_s=float(L * s.tr))
        Zg = grid_series(s, params)
        grid_len = int(Zg.shape[0])
        if _SPEC["truncate_native_s"] and grid_len != 100:
            raise AssertionError(f"truncation gave {grid_len} grid samples, expected 100")
        feats = extract_subject(s, params, **_SPEC["kw"])
        fc = None
        if _VARIANT == "primary":
            if feats["params_sha256"] != FROZEN_PARAMS_SHA256:
                raise AssertionError("primary row params hash differs from the frozen hash")
            C = (Zg.T @ Zg) / Zg.shape[0]          # z-scored with ddof=0 -> exact Pearson correlation
            iu = np.triu_indices(C.shape[0], 1)
            fc = C[iu].astype(np.float32)
        rec = {"position": int(pos), "variant": _VARIANT, "params_sha256": feats["params_sha256"],
               "site": s.site, "tr": s.tr, "raw_valid_T": s.raw_valid_T, "n_trim": s.n_trim, "valid_T": s.valid_T,
               "duration_s": s.duration_s, "grid_len": grid_len, "gradient_share": feats["gradient_share"],
               "units": {k: {kk: r[kk] for kk in UNIT_KEYS} for k, r in feats["results"].items()},
               "ok": True, "elapsed_s": round(time.time() - t0, 2)}
        return rec, fc
    except Exception as exc:  # noqa: BLE001 - record class only (no message), the run continues
        return {"position": int(pos), "variant": _VARIANT, "ok": False, "error_class": type(exc).__name__,
                "elapsed_s": round(time.time() - t0, 2)}, None


def _done_positions(path):
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    done.add(json.loads(line)["position"])
    return done


def cmd_extract(a):
    import multiprocessing as mp
    pinned = verify_frozen_code()
    man = json.load(open(os.path.join(a.outdir, "manifest.json")))
    check_manifest(man)
    spec = variant_spec(a.variant, a.density)
    vsha = variant_sha(a.variant, spec)
    positions = [r["position"] for r in man["rows"] if r["included"]]
    if a.limit:
        positions = positions[: a.limit]
    tag = a.variant if a.variant == "primary" else f"{a.variant}_d{int(round(a.density * 1000)):03d}"
    jl = os.path.join(a.outdir, f"extract_{tag}.jsonl")
    log_path = os.path.join(a.outdir, f"extract_{tag}.log")
    done = _done_positions(jl)
    todo = [p for p in positions if p not in done]
    header = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "variant": a.variant,
              "density": a.density, "variant_sha": vsha, "params": spec["params"],
              "params_sha256": params_sha256(spec["params"]), "kw": spec["kw"],
              "truncate_native_s": spec["truncate_native_s"], "card_sha256": CARD_SHA256,
              "card_s12_code_hashes": pinned, "script_sha256": sha256_file(os.path.abspath(__file__)),
              "manifest_sha256": sha256_file(os.path.join(a.outdir, "manifest.json")),
              "cohort_digest": man["cohort_digest"], "n_positions": len(positions), "n_already_done": len(done),
              "workers": a.workers, "host": platform.node(), "cpus": os.cpu_count(),
              "python": platform.python_version(), "numpy": np.__version__, "pid": os.getpid()}
    with open(os.path.join(a.outdir, f"extract_{tag}_header_{int(time.time())}.json"), "w") as f:
        json.dump(header, f, indent=1)
    logf = open(log_path, "a")

    def log(msg):
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
        logf.write(line + "\n")
        logf.flush()
        print(line, flush=True)

    log(f"start variant={a.variant} tag={tag} variant_sha={vsha} params_sha256={header['params_sha256']} "
        f"todo={len(todo)} done={len(done)} workers={a.workers}")
    fc = None
    if a.variant == "primary" and a.fc_out:
        from numpy.lib.format import open_memmap
        n_feat = 304 * 303 // 2
        if os.path.exists(a.fc_out):
            fc = open_memmap(a.fc_out, mode="r+")
        else:
            fc = open_memmap(a.fc_out, mode="w+", dtype=np.float32, shape=(man["n"], n_feat))
            fc[:] = np.nan
        log(f"static FC memmap {a.fc_out} shape={fc.shape}")
    t0 = time.time()
    n_ok = n_err = 0
    with mp.get_context("fork").Pool(a.workers, initializer=_init, initargs=(a.variant, a.density)) as pool, \
            open(jl, "a") as out:
        for i, (rec, vec) in enumerate(pool.imap_unordered(_work, todo, chunksize=1), 1):
            if vec is not None and fc is not None:
                fc[rec["position"]] = vec
                fc.flush()
            out.write(json.dumps(rec) + "\n")
            out.flush()
            n_ok += rec["ok"]
            n_err += not rec["ok"]
            if i % 25 == 0 or i == len(todo):
                el = time.time() - t0
                log(f"progress {i}/{len(todo)} ok={n_ok} err={n_err} elapsed_s={el:.0f} "
                    f"eta_s={el / i * (len(todo) - i):.0f}")
    log(f"finished ok={n_ok} err={n_err} elapsed_s={time.time() - t0:.0f} jsonl_sha256={sha256_file(jl)}")
    if fc is not None:
        del fc
        log(f"static FC sha256={sha256_file(a.fc_out)}")


def cmd_status(a):
    tag = a.variant if a.variant == "primary" else f"{a.variant}_d{int(round(a.density * 1000)):03d}"
    jl = os.path.join(a.outdir, f"extract_{tag}.jsonl")
    done = _done_positions(jl)
    print(json.dumps({"file": jl, "n_done": len(done)}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("manifest")
    m.add_argument("--outdir", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--outdir", required=True)
    e.add_argument("--variant", choices=VARIANTS, required=True)
    e.add_argument("--density", type=float, default=None)
    e.add_argument("--workers", type=int, default=14)
    e.add_argument("--limit", type=int, default=0, help="first N included positions only (smoke test)")
    e.add_argument("--fc-out", default=None)
    s = sub.add_parser("status")
    s.add_argument("--outdir", required=True)
    s.add_argument("--variant", choices=VARIANTS, required=True)
    s.add_argument("--density", type=float, default=None)
    a = ap.parse_args()
    if a.workers if hasattr(a, "workers") else 0:
        if not 1 <= a.workers <= 16:
            raise SystemExit("workers must be in 1..16 (C5)")
    {"manifest": cmd_manifest, "extract": cmd_extract, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
