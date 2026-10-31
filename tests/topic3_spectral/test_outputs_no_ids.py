"""C4: no participant identifiers in any Topic 3 output (results tree and topic3 docs)."""
import glob
import os
import zipfile

import numpy as np

from tests.topic3_spectral.helpers import ROOT

SCAN = [os.path.join(ROOT, "results", "topic3"), os.path.join(ROOT, "docs", "03_empirical_analysis", "topic3")]


def _files():
    for base in SCAN:
        for p in glob.glob(os.path.join(base, "**", "*"), recursive=True):
            if os.path.isfile(p):
                yield p


def test_no_sub_prefix_strings_and_no_ids_arrays():
    n = 0
    for p in _files():
        n += 1
        if p.endswith(".npz"):
            with zipfile.ZipFile(p) as zf:
                assert not any(x.startswith("ids") for x in zf.namelist()), p
            z = np.load(p, allow_pickle=False)
            for k in z.files:
                assert z[k].dtype.kind in "fiub", (p, k)
            continue
        with open(p, "rb") as f:
            assert b"sub-" not in f.read(), p
    assert n >= 0
