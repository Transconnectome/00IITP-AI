"""C4 guard (post-results, added 2026-10-31 by worker_M2_r2): the ID scan of the Topic 3 outputs must
actually scan files. test_outputs_no_ids.py ends with `assert n >= 0`, which also passes on an empty tree;
this file is a NEW, stricter companion (the pinned test is not edited)."""
import glob
import os

from tests.topic3_spectral.helpers import ROOT

RESULTS = os.path.join(ROOT, "results", "topic3")
DOCS = os.path.join(ROOT, "docs", "03_empirical_analysis", "topic3")


def test_id_scan_covers_a_nonempty_results_tree_without_sub_prefix():
    files = [p for base in (RESULTS, DOCS) for p in glob.glob(os.path.join(base, "**", "*"), recursive=True)
             if os.path.isfile(p)]
    assert any(p.endswith("family_B_token_level.json") for p in files)
    assert sum(p.endswith(".npz") for p in files) >= 4
    n_text = 0
    for p in files:
        if p.endswith(".npz"):
            continue
        with open(p, "rb") as f:
            assert b"sub-" not in f.read(), p
        n_text += 1
    assert n_text > 0
