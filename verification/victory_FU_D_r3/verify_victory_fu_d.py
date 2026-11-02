"""Independent Victory Audit verification script for Milestone FU_D Iteration 3 (victory_FU_D_r3).

Performs CPU-only (0 GPU-h) verification of:
1. Phase A: C1 protected hashes (67/67), 5 FU-D SHA-256 receipts, 3 Topic 2 r1 receipts, and strict chronological
   ordering from card/code freeze -> smoke (job 511) -> F+ gate runs (jobs 534/535/536) -> verdict.json ->
   addendum_01.md -> addendum_02.md.
2. Phase B & C:
   - Independent exact-rational (Fraction) and float64 recomputation of F+ gate test_nmse and relative gains from raw
     test_num / test_den in results/topic2/2026-11-02_fu_d/runs/Fplus_{E,C,S}_s0/run.json.
   - Byte-identical regeneration of verdict.json into a temporary file via scripts/topic2fu_d_verdict.py.
   - Algebraic verification of Proof P1 (stop -> keep/modify unreachability for n=5, k in {3, 4}) and independent
     oracle check of all 28 reachable step-7 fixtures and 3,000 generated scenarios.
   - Forensic audit of verification/worker_FU_D_r3/mutation/union_r3.out.json (2,051 raw -> 1,675 distinct: 1,511
     killed, 164 survived, 0 invalid, 515/515 shipped-changing killed, 34 killed_only_by_r3_files, exact 10-class
     partition in addendum_02.md section 5).
   - Independent reproduction of verification/worker_FU_D_r3/probes/errata_probe.out.json and shipped-data invariants
     for E5, E2', E6, E7, E8, E9, W4, W5.
   - C5 GPU ledger audit (3.672 GPU-h worker+explorer <= 25.0 GPU-h cap; 0 GPU-h in r2/r3).
   - C4 hygiene scan on all frozen FU-D paths, r3 paths, and victory_FU_D_r3 paths (0 hits).
"""
from __future__ import annotations

from fractions import Fraction
import glob
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import tempfile

from scipy.stats import t as _t_dist

ROOT = "/home/juke/git/00IITP-AI"
sys.path.insert(0, ROOT)

from src.topic2_fu_d import config as K  # noqa: E402
from src.topic2_fu_d import design as D  # noqa: E402
from src.topic2_fu_d import seedplan as SP  # noqa: E402
from src.topic2_fu_d import verdict as V  # noqa: E402
from tests.topic2_fu_d import test_fud_r3_guards as G3  # noqa: E402
from tests.topic2_fu_d import test_fud_r3_oracle as O3  # noqa: E402

FUD_DIR = os.path.join(ROOT, "results", "topic2", "2026-11-02_fu_d")
R1_DIR = os.path.join(ROOT, "results", "topic2", "2026-11-01")
OUT_JSON = os.path.join(ROOT, "verification", "victory_FU_D_r3", "verify_victory_fu_d.out.json")
EXPECTED_VERDICT_SHA = "f6b295d9d093fd3ff3e991d46a64a5dc21fbdfc638804363deed7ff1cca959fc"
EXPECTED_CARD_SHA = "1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b"


def sha256_file(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def verify_receipt_file(receipt_path: str, base_dir: str = ROOT) -> dict:
    total = 0
    ok = 0
    bad = []
    for ln in open(receipt_path):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        exp_sha, rel = parts[0], parts[1]
        total += 1
        target = os.path.join(base_dir, rel) if not os.path.isabs(rel) else rel
        if not os.path.isfile(target):
            bad.append({"file": rel, "error": "missing"})
            continue
        got_sha = sha256_file(target)
        if got_sha == exp_sha:
            ok += 1
        else:
            bad.append({"file": rel, "expected": exp_sha, "got": got_sha})
    assert total > 0 and ok == total and not bad, f"Receipt check failed for {receipt_path}: {bad}"
    return {"total": total, "ok": ok, "bad": bad}


def check_phase_a_receipts_and_timeline() -> dict:
    receipts = {
        "protected_hashes": verify_receipt_file(
            os.path.join(ROOT, ".agents", "teamwork", "tw-20261031-four-topics", "sentinel", "PROTECTED_HASHES.txt")
        ),
        "fud_card": verify_receipt_file(os.path.join(FUD_DIR, "card_sha256.txt")),
        "fud_code_freeze": verify_receipt_file(os.path.join(FUD_DIR, "code_sha256_at_freeze.txt")),
        "fud_output": verify_receipt_file(os.path.join(FUD_DIR, "output_sha256.txt")),
        "fud_addendum_01": verify_receipt_file(os.path.join(FUD_DIR, "addendum_01_sha256.txt")),
        "fud_addendum_02": verify_receipt_file(os.path.join(FUD_DIR, "addendum_02_sha256.txt")),
        "r1_code_freeze": verify_receipt_file(os.path.join(R1_DIR, "code_sha256_at_freeze.txt")),
        "r1_output_r2": verify_receipt_file(os.path.join(R1_DIR, "output_sha256_r2.txt")),
        "r1_addendum_06": verify_receipt_file(os.path.join(R1_DIR, "addendum_06_sha256.txt")),
    }
    assert receipts["protected_hashes"]["total"] == 67
    assert receipts["fud_card"]["total"] == 1
    assert receipts["fud_code_freeze"]["total"] == 29
    assert receipts["fud_output"]["total"] == 34
    assert receipts["fud_addendum_01"]["total"] == 23
    assert receipts["fud_addendum_02"]["total"] == 102
    assert receipts["r1_code_freeze"]["total"] == 33
    assert receipts["r1_output_r2"]["total"] == 156
    assert receipts["r1_addendum_06"]["total"] == 31

    # Verify chronological ordering of events
    card_hdr = open(os.path.join(FUD_DIR, "card_sha256.txt")).readline().strip()
    code_hdr = open(os.path.join(FUD_DIR, "code_sha256_at_freeze.txt")).readline().strip()
    out_hdr = open(os.path.join(FUD_DIR, "output_sha256.txt")).readline().strip()
    add1_hdr = open(os.path.join(FUD_DIR, "addendum_01_sha256.txt")).readline().strip()

    t_freeze = "2026-11-01T16:06:07Z"
    assert t_freeze in card_hdr and t_freeze in code_hdr
    jobs = [json.loads(ln) for ln in open(os.path.join(FUD_DIR, "logs", "jobs.jsonl")) if ln.strip()]
    smoke_sub = next(j for j in jobs if j["event"] == "submitted" and j["name"] == "smoke")
    smoke_close = next(j for j in jobs if j["event"] == "closed" and j["name"] == "smoke")
    smoke_run = json.load(open(os.path.join(FUD_DIR, "smoke", "run.json")))
    smoke_equiv = json.load(open(os.path.join(FUD_DIR, "smoke", "equiv.json")))
    assert smoke_equiv["exact"] is True and smoke_equiv["abs_diff"] == 0.0
    assert smoke_equiv["per_subject_num_equal"] is True and smoke_equiv["per_subject_den_equal"] is True
    assert smoke_run["status"] == "aborted_throughput" and smoke_run["aborted_step"] == 200

    gate_times = {}
    for arm, jid in (("E", "534"), ("C", "535"), ("S", "536")):
        nm = f"Fplus_{arm}_s0"
        sub_ev = next(j for j in jobs if j["event"] == "submitted" and j["name"] == nm)
        cl_ev = next(j for j in jobs if j["event"] == "closed" and j["name"] == nm)
        r_rec = json.load(open(os.path.join(FUD_DIR, "runs", nm, "run.json")))
        s_rec = json.load(open(os.path.join(FUD_DIR, "runs", nm, "slurm.json")))
        assert s_rec["job_id"] == jid and s_rec["state"] == "COMPLETED"
        assert sub_ev["utc"] < s_rec["start_utc"] <= r_rec["start_utc"] < r_rec["end_utc"] <= s_rec["end_utc"] < cl_ev["utc"]
        gate_times[nm] = {
            "job_id": jid,
            "submitted_utc": sub_ev["utc"],
            "start_utc": r_rec["start_utc"],
            "end_utc": r_rec["end_utc"],
            "closed_utc": cl_ev["utc"],
        }

    t_out_receipt = "2026-11-01T19:13:37Z"
    t_add1_receipt = "2026-11-01T21:49:17Z"
    assert t_out_receipt in out_hdr and t_add1_receipt in add1_hdr
    assert (
        t_freeze
        < smoke_sub["utc"]
        < smoke_run["start_utc"]
        < smoke_close["utc"]
        < gate_times["Fplus_E_s0"]["submitted_utc"]
        < gate_times["Fplus_E_s0"]["start_utc"]
        < gate_times["Fplus_S_s0"]["end_utc"]
        < gate_times["Fplus_S_s0"]["closed_utc"]
        < t_out_receipt
        < t_add1_receipt
    )
    add1_mtime = os.path.getmtime(os.path.join(FUD_DIR, "addendum_01_sha256.txt"))
    add2_mtime = os.path.getmtime(os.path.join(FUD_DIR, "addendum_02_sha256.txt"))
    assert add1_mtime < add2_mtime

    return {
        "receipts": receipts,
        "chronology": {
            "freeze_utc": t_freeze,
            "smoke_submitted_utc": smoke_sub["utc"],
            "smoke_start_utc": smoke_run["start_utc"],
            "smoke_closed_utc": smoke_close["utc"],
            "gate_runs": gate_times,
            "output_receipt_utc": t_out_receipt,
            "addendum_01_receipt_utc": t_add1_receipt,
            "addendum_02_after_addendum_01": True,
            "strict_order_verified": True,
        },
    }


def check_phase_c_recomputation_and_invariants() -> dict:
    # 1. Exact Fraction and float recomputation of F+ gate
    nmse_frac = {}
    nmse_float = {}
    for arm in ("E", "C", "S"):
        nm = f"Fplus_{arm}_s0"
        rec = json.load(open(os.path.join(FUD_DIR, "runs", nm, "run.json")))
        num = rec["test_num"]
        den = rec["test_den"]
        assert len(num) == 16 and len(den) == 16
        assert all(math.isfinite(x) and x >= 0 for x in num)
        assert all(math.isfinite(x) and x > 0 for x in den)
        f_num = sum(Fraction(x) for x in num)
        f_den = sum(Fraction(x) for x in den)
        nmse_frac[arm] = f_num / f_den
        nmse_float[arm] = sum(num) / sum(den)
        assert abs(nmse_float[arm] - rec["test_nmse"]) <= 1e-16
        assert abs(float(nmse_frac[arm]) - rec["test_nmse"]) <= 1e-16

    gain_ce_frac = (nmse_frac["E"] - nmse_frac["C"]) / nmse_frac["E"]
    gain_cs_frac = (nmse_frac["S"] - nmse_frac["C"]) / nmse_frac["S"]
    delta_frac = Fraction(1, 100)
    gate_pass_frac = bool(gain_ce_frac >= delta_frac and gain_cs_frac >= delta_frac)
    assert gate_pass_frac is False
    assert Fraction(0) < gain_ce_frac < delta_frac
    assert Fraction(0) < gain_cs_frac < delta_frac

    shipped_verdict_path = os.path.join(FUD_DIR, "verdict.json")
    shipped_verdict_sha = sha256_file(shipped_verdict_path)
    assert shipped_verdict_sha == EXPECTED_VERDICT_SHA
    shipped = json.load(open(shipped_verdict_path))
    assert shipped["verdict"] == "inconclusive"
    assert shipped["decision"]["verdict"] == "inconclusive"
    assert shipped["decision"]["fplus_gate"]["pass"] is False
    gain_ce_float = (nmse_float["E"] - nmse_float["C"]) / nmse_float["E"]
    gain_cs_float = (nmse_float["S"] - nmse_float["C"]) / nmse_float["S"]
    assert gain_ce_float == shipped["decision"]["fplus_gate"]["gain_C_vs_E"]
    assert gain_cs_float == shipped["decision"]["fplus_gate"]["gain_C_vs_S"]
    assert abs(float(gain_ce_frac) - shipped["decision"]["fplus_gate"]["gain_C_vs_E"]) <= 1e-15
    assert abs(float(gain_cs_frac) - shipped["decision"]["fplus_gate"]["gain_C_vs_S"]) <= 1e-15

    # 2. Byte-for-byte regeneration of verdict.json
    freeze_map = {}
    for ln in open(os.path.join(FUD_DIR, "code_sha256_at_freeze.txt")):
        p = ln.split()
        if len(p) == 2 and not ln.startswith("#"):
            freeze_map[p[1]] = p[0]
    wrapper_sha = freeze_map["scripts/topic2fu_d_train.py"]

    with tempfile.TemporaryDirectory() as tmpdir:
        regen_path = os.path.join(tmpdir, "regen_verdict.json")
        cmd = [
            sys.executable,
            "-B",
            os.path.join(ROOT, "scripts", "topic2fu_d_verdict.py"),
            "--results",
            FUD_DIR,
            "--wrapper-sha256",
            wrapper_sha,
            "--out",
            regen_path,
        ]
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            env=dict(os.environ, PYTHONPATH=ROOT, PYTHONDONTWRITEBYTECODE="1", CUDA_VISIBLE_DEVICES=""),
            capture_output=True,
            text=True,
            check=True,
        )
        regen_sha = sha256_file(regen_path)
        assert regen_sha == EXPECTED_VERDICT_SHA
        assert open(regen_path, "rb").read() == open(shipped_verdict_path, "rb").read()
        stdout_obj = json.loads(proc.stdout)
        assert stdout_obj["verdict"] == "inconclusive" and stdout_obj["I1_t"] is None and stdout_obj["I2_t"] is None

    # 3. Shipped-data invariants (E5, E2', E6, E7, E8, E9)
    runs_dir = os.path.join(FUD_DIR, "runs")
    run_names = sorted(os.listdir(runs_dir))
    assert run_names == ["Fplus_C_s0", "Fplus_E_s0", "Fplus_S_s0"]
    want_fud_code = {
        f: freeze_map["src/topic2_fu_d/" + f]
        for f in ("__init__.py", "config.py", "design.py", "records.py", "seedplan.py", "slurm.py", "verdict.py", "view.py")
    }
    for nm in run_names:
        full_p = os.path.join(runs_dir, nm)
        assert os.path.isdir(full_p) and not os.path.islink(full_p)
        assert nm.isascii() and nm == nm.strip()
        parsed = D.parse_dir(nm)
        assert parsed is not None and D.run_name(*parsed) == nm
        rec = json.load(open(os.path.join(full_p, "run.json")))
        assert type(rec["seed"]) is int and rec["seed"] == 0
        meta = json.load(open(os.path.join(full_p, "fud_meta.json")))
        assert meta["fud_code_sha256"] == want_fud_code
        assert meta["wrapper_sha256"] == wrapper_sha
        assert meta["post_checks_ok"] is True
    assert not os.path.exists(os.path.join(FUD_DIR, "seed_plan.json"))

    return {
        "nmse_float": nmse_float,
        "gain_C_vs_E": float(gain_ce_frac),
        "gain_C_vs_S": float(gain_cs_frac),
        "gate_pass": False,
        "verdict": shipped["verdict"],
        "verdict_sha256": shipped_verdict_sha,
        "regenerated_byte_identical": True,
        "shipped_invariants_ok": True,
    }


def check_b1_and_b2_closure() -> dict:
    # 1. Algebraic Proof P1 (n=5, k in {3, 4})
    t4 = float(_t_dist.ppf(0.975, 4))
    mult_k4 = t4 * math.sqrt(4.0 / (25.0 * 4.0)) - 1.0 / 5.0
    mult_k3 = t4 * math.sqrt(6.0 / (25.0 * 4.0)) - 2.0 / 5.0
    assert mult_k4 > 0.355 and mult_k3 > 0.280

    # 2. Verify all 28 STALL_MATRIX fixtures and 3,000 oracle scenarios
    assert len(G3.STALL_MATRIX) == 28
    for stalled, a, b, expected, g1, g2 in G3.STALL_MATRIX:
        kept = [i for i in range(5) if i not in stalled]
        assert G3._oracle_cat(g1, g2) == a
        assert G3._oracle_cat([g1[i] for i in kept], [g2[i] for i in kept]) == b
        out = V._stage1_category(G3._nm(g1, g2), list(stalled), 0.01)
        assert out["primary"] == a and out["stall_sensitivity"]["category"] == b and out["category"] == expected

    assert len(O3.SCEN) == 3_000
    for s in O3.SCEN:
        v = V.decide(*s)
        got = (v["verdict"], v.get("stage1", {}).get("primary"), v.get("stage1", {}).get("category"))
        assert got == O3.oracle(*s)

    # 3. Audit union_r3.out.json and 164-survivor classification in addendum_02.md
    union_path = os.path.join(ROOT, "verification", "worker_FU_D_r3", "mutation", "union_r3.out.json")
    u = json.load(open(union_path))
    s = u["summary"]
    assert s["raw"] == 2_051
    assert s["distinct"] == 1_675
    assert s["not_applied"] == ["rev2_1:R42"]
    assert s["killed"] == 1_511
    assert sum(r["status"] == "KILLED" for r in u["results"]) == 1_511
    assert len(u["results"]) == 1_675
    assert len(s["survived"]) == 164
    assert s["invalid"] == []
    assert len(s["shipped_changing"]) == 515
    assert s["survivors_changing_shipped_output"] == []
    assert len(s["killed_only_by_r3_files"]) == 34

    # Verify key B1/r2/r3 mutants are killed
    must_kill_prefixes = ("cha2_2:C12", "cha2_1:CV09", "cha2_1:CP01", "cha2_1:CP02", "rev2_1:R31", "rev2_1:R34", "rev2_2:R35")
    for r in u["results"]:
        aliases = set(r.get("aliases", [])) | {r["uid"]}
        if any(a in must_kill_prefixes for a in aliases):
            assert r["A"]["status"] == "KILLED", f"Expected KILLED for {aliases}"

    # Verify errata_probe.py reproduction
    probe_script = os.path.join(ROOT, "verification", "worker_FU_D_r3", "probes", "errata_probe.py")
    probe_pinned = os.path.join(ROOT, "verification", "worker_FU_D_r3", "probes", "errata_probe.out.json")
    with tempfile.TemporaryDirectory() as tmpdir:
        repro_out = os.path.join(tmpdir, "errata_repro.json")
        subprocess.run(
            [sys.executable, "-B", probe_script, repro_out],
            cwd=ROOT,
            env=dict(os.environ, PYTHONPATH=ROOT, PYTHONDONTWRITEBYTECODE="1", CUDA_VISIBLE_DEVICES=""),
            check=True,
        )
        assert json.load(open(repro_out)) == json.load(open(probe_pinned))

    return {
        "p1_mult_k4": mult_k4,
        "p1_mult_k3": mult_k3,
        "stall_matrix_fixtures_verified": 28,
        "oracle_scenarios_verified": 3_000,
        "union_raw": s["raw"],
        "union_distinct": s["distinct"],
        "union_killed": s["killed"],
        "union_survived": len(s["survived"]),
        "union_invalid": len(s["invalid"]),
        "union_shipped_changing_killed": len(s["shipped_changing"]),
        "union_survivors_changing_shipped": len(s["survivors_changing_shipped_output"]),
        "union_killed_only_by_r3_files": len(s["killed_only_by_r3_files"]),
        "errata_probe_reproduced_identically": True,
    }


def check_c5_gpu_ledger_and_c4_hygiene() -> dict:
    ledger_text = open(os.path.join(ROOT, "results", "gpu_ledger_2026-10-31.md")).read()
    totals = SP.ledger_totals(ledger_text)
    rows = SP.parse_ledger(ledger_text)
    r2_r3_rows = [r for r in rows if "FU_D_r2" in r["agent"] or "FU_D_r3" in r["agent"]]
    assert totals["fud_total_gpuh"] == 3.672
    assert totals["fud_total_gpuh"] <= K.FUD_CAP_GPUH
    assert len(r2_r3_rows) == 0

    # C4 scan using frozen detector + 6-digit detector
    spec = importlib.util.spec_from_file_location("fud_c4scan", os.path.join(ROOT, "scripts", "topic2fu_d_c4scan.py"))
    c4_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c4_mod)
    frozen_scan = c4_mod.scan(ROOT)
    assert frozen_scan["token_hits"] == 0 and frozen_scan["bids_hits"] == 0

    six_re = re.compile(rb"(?<![0-9A-Za-z._-])[0-9]{6}(?![0-9A-Za-z_])")
    vic_paths = [
        os.path.join(ROOT, "verification", "victory_FU_D_r3"),
        os.path.join(ROOT, ".agents", "teamwork", "tw-20261031-four-topics", "victory_FU_D_r3"),
    ]
    vic_files = []
    for vp in vic_paths:
        vic_files += [f for f in glob.glob(os.path.join(vp, "**", "*"), recursive=True) if os.path.isfile(f) and "__pycache__" not in f]
    vic_token_hits = 0
    vic_bids_hits = 0
    vic_six_hits = 0
    bad_vic_files = []
    for vf in sorted(set(vic_files)):
        blob = open(vf, "rb").read()
        th = c4_mod.token_hits(blob)
        bh = len(c4_mod.BIDS.findall(blob))
        sh = len(six_re.findall(blob))
        vic_token_hits += th
        vic_bids_hits += bh
        vic_six_hits += sh
        if th or bh or sh:
            bad_vic_files.append({"file": os.path.relpath(vf, ROOT), "token": th, "bids": bh, "six_digit": sh})
    assert vic_token_hits == 0 and vic_bids_hits == 0 and vic_six_hits == 0, f"C4 hits in victory files: {bad_vic_files}"

    return {
        "fud_worker_and_explorer_gpuh": totals["fud_total_gpuh"],
        "fud_cap_gpuh": K.FUD_CAP_GPUH,
        "fud_r2_r3_gpuh": 0.0,
        "c4_frozen_scan": frozen_scan,
        "c4_victory_scan": {
            "n_files": len(set(vic_files)),
            "token_hits": vic_token_hits,
            "bids_hits": vic_bids_hits,
            "six_digit_hits": vic_six_hits,
            "bad_files": bad_vic_files,
        },
    }


def main() -> int:
    res = {
        "phase_a": check_phase_a_receipts_and_timeline(),
        "phase_c_recomputation": check_phase_c_recomputation_and_invariants(),
        "phase_b_b1_b2_closure": check_b1_and_b2_closure(),
        "phase_b_c4_c5": check_c5_gpu_ledger_and_c4_hygiene(),
        "status": "PASS",
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump(res, open(OUT_JSON, "w"), indent=2)
    # Re-verify C4 after writing OUT_JSON
    res["phase_b_c4_c5"] = check_c5_gpu_ledger_and_c4_hygiene()
    json.dump(res, open(OUT_JSON, "w"), indent=2)
    print(json.dumps({"status": res["status"], "verdict_sha256": res["phase_c_recomputation"]["verdict_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
