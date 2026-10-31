"""End-to-end check of scripts/topic3_token_job.py on synthetic frames with the REAL dump shapes:
halts on contract violations, writes position-keyed outputs only, never the directory names."""
import json
import os
import subprocess
import sys

import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "topic3_token_job.py")


def _make_root(tmp, torch, names, seed):
    g = torch.Generator().manual_seed(seed)
    for n in names:
        os.makedirs(os.path.join(tmp, n))
        for f in range(7):
            d = {"layer_0": torch.randn(10240, 384, generator=g), "layer_1": torch.randn(1280, 768, generator=g),
                 "layer_2": torch.randn(160, 1536, generator=g), "layer_3": torch.randn(1536, 2, 2, 2, 20, generator=g)}
            torch.save(d, os.path.join(tmp, n, "frame%02d.pt" % f))


def _run(args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="2")
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, env=env, cwd=ROOT)


@pytest.fixture(scope="module")
def roots(tmp_path_factory):
    torch = pytest.importorskip("torch")
    base = tmp_path_factory.mktemp("frames")
    a = str(base / "ckptA")
    b = str(base / "ckptB")
    _make_root(a, torch, ["sub-SYNA01", "sub-SYNA02"], 0)
    _make_root(b, torch, ["sub-SYNB01", "sub-SYNA02"], 1)
    return a, b, str(base)


def test_driver_writes_position_keyed_outputs_without_names(roots):
    a, _, base = roots
    out = os.path.join(base, "out_ok")
    r = _run(["--frames-root", a, "--label", "syn", "--out-dir", out, "--workers", "2"])
    assert r.returncode == 0, r.stderr
    assert "sub-" not in r.stdout + r.stderr
    for fn in os.listdir(out):
        assert b"sub-" not in open(os.path.join(out, fn), "rb").read()
    z = np.load(os.path.join(out, "syn_token_spectra.npz"), allow_pickle=False)
    np.testing.assert_array_equal(z["positions"], [0, 1])
    assert z["cat_corr_eigs__L3"].shape == (2, 1119) and z["cat_cov_eigs__L0"].shape == (2, 384)
    assert z["sub_covpr__L0"].shape == (2, 7)
    rec = json.load(open(os.path.join(out, "syn_token_job.json")))
    assert rec["n_subjects"] == 2 and "outputs" in rec


def test_driver_halts_on_reference_mismatch_and_bad_pins(roots, tmp_path):
    a, b, _ = roots
    r = _run(["--frames-root", b, "--label", "x", "--out-dir", str(tmp_path / "o1"), "--reference-root", a])
    assert r.returncode == 2 and not os.path.exists(str(tmp_path / "o1" / "x_token_spectra.npz"))
    bad = tmp_path / "npz"
    bad.mkdir()
    for k in range(4):
        np.savez(str(bad / ("layer_%d.npz" % k)), X=np.zeros((2, 3)), ids=np.array(["q", "r"]))
    r = _run(["--frames-root", a, "--label", "y", "--out-dir", str(tmp_path / "o2"), "--check-npz-root", str(bad)])
    assert r.returncode == 2
    rec = json.load(open(str(tmp_path / "o2" / "y_token_job.json")))
    assert rec["checks"]["pin_ok_L0"] is False and "halted" in rec
