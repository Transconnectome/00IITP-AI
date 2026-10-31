"""Topic 3 Family A — subject-level rerun on the 7 pooled matrices (local CPU, frozen card §4).
Refuses to run unless the card hash verifies. Writes results/topic3/2026-10-31/family_A_subject_level.json.
Run: cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. OMP_NUM_THREADS=4 \
     nice -n 10 /home/juke/superclaude-env/bin/python3 scripts/topic3_subject_level.py
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.dont_write_bytecode = True

from topic3_common import dump, run_record, verify_card  # noqa: E402
from src.topic3_spectral import analysis, io_contract as io  # noqa: E402


def main():
    card = verify_card()
    t0 = time.time()
    rec = run_record(os.path.abspath(__file__))
    rec["card_sha256_verified"] = card
    rec["params"] = analysis.PARAMS
    mats = {k: io.load_pinned(k) for k in io.PINNED}
    rec["input_sha256"] = {k: v[1] for k, v in io.PINNED.items()}
    full = [(os.path.join(io.VRABES_RA, io.PINNED[k][0]), io.PINNED[k][1])
            for k in ("L0", "L1", "L2", "L3", "BrainLM", "BrainJEPA")]
    ns = (os.path.join(io.VRABES_RA, io.PINNED["NeuroSTORM"][0]), io.PINNED["NeuroSTORM"][1])
    align = io.positional_alignment(full, ns)
    if not align["same_order"]:
        sys.exit("row order differs across 57-row inputs: halt")
    rec["alignment"] = {"same_order": align["same_order"], "subset_in_increasing_order": align["subset_in_increasing_order"],
                        "n_subset": len(align["subset_positions"])}
    res = analysis.subject_level(mats, align["subset_positions"], analysis.PARAMS)
    rec["runtime_s"] = round(time.time() - t0, 1)
    print(dump({"run": rec, "results": res}, "family_A_subject_level.json"))


if __name__ == "__main__":
    main()
