"""Data-contract fixtures: missing file / hash mismatch raise (no silent fallback), allow_pickle=False,
X only, in-memory alignment returns no identifiers, restricted torch-free .pt reader."""
import os
import pickle
import zipfile

import numpy as np
import pytest

from tests.topic3_spectral.helpers import ROOT  # noqa: F401
from src.topic3_spectral import io_contract as io


def _npz(tmp_path, name, X, ids):
    p = str(tmp_path / name)
    np.savez(p, X=X, ids=np.array(ids))
    return p, io.sha256_file(p)


def test_missing_file_raises_no_fallback(tmp_path):
    with pytest.raises(FileNotFoundError):
        io.load_X(str(tmp_path / "absent.npz"), "0" * 64)


def test_hash_mismatch_raises(tmp_path):
    p, sha = _npz(tmp_path, "a.npz", np.ones((3, 2)), ["r0", "r1", "r2"])
    with pytest.raises(ValueError):
        io.load_X(p, "f" * 64)
    X = io.load_X(p, sha)
    assert isinstance(X, np.ndarray) and X.dtype == np.float64 and X.shape == (3, 2)


def test_object_arrays_refused_allow_pickle_false(tmp_path):
    p = str(tmp_path / "obj.npz")
    np.savez(p, X=np.array([{"a": 1}], dtype=object))
    with pytest.raises(ValueError):
        io.load_X(p, io.sha256_file(p))


def test_non_finite_X_raises(tmp_path):
    p, sha = _npz(tmp_path, "nan.npz", np.array([[np.nan, 1.0], [0.0, 1.0]]), ["a", "b"])
    with pytest.raises(ValueError):
        io.load_X(p, sha)


def test_positional_alignment_returns_positions_only(tmp_path):
    names = ["p%02d" % i for i in range(10)]
    a = _npz(tmp_path, "a.npz", np.zeros((10, 2)), names)
    b = _npz(tmp_path, "b.npz", np.zeros((10, 3)), names)
    s = _npz(tmp_path, "s.npz", np.zeros((4, 2)), [names[i] for i in (1, 4, 6, 9)])
    out = io.positional_alignment([a, b], s)
    assert out == {"same_order": True, "n_rows": 10, "subset_positions": [1, 4, 6, 9],
                   "subset_in_increasing_order": True}
    flat = repr(out)
    assert not any(n in flat for n in names)
    c = _npz(tmp_path, "c.npz", np.zeros((10, 2)), names[::-1])
    assert io.positional_alignment([a, c])["same_order"] is False


def test_restricted_unpickler_blocks_arbitrary_classes(tmp_path):
    p = str(tmp_path / "evil.pt")

    class Evil(object):
        def __reduce__(self):
            return (os.system, ("true",))
    with zipfile.ZipFile(p, "w") as zf:
        zf.writestr("archive/data.pkl", pickle.dumps({"x": Evil()}, protocol=2))
    with pytest.raises(pickle.UnpicklingError):
        io.load_pt_numpy(p)


def test_numpy_pt_reader_equals_torch_load(tmp_path):
    torch = pytest.importorskip("torch")
    g = torch.Generator().manual_seed(0)
    d = {"layer_0": torch.randn(64, 12, generator=g), "layer_2": torch.randn(16, 24, generator=g),
         "layer_3": torch.randn(24, 20, 2, 2, 2, generator=g).permute(0, 2, 3, 4, 1),   # non-contiguous view
         "nc": torch.randn(24, 16, generator=g).T}
    p = str(tmp_path / "frame0.pt")
    torch.save(d, p)
    got = io.load_pt_numpy(p)
    for k, v in d.items():
        np.testing.assert_array_equal(got[k], v.numpy())
        assert got[k].shape == tuple(v.shape)


def test_pinned_real_inputs_load_X_only():
    if not os.path.isdir(io.VRABES_RA):
        pytest.skip("VRABES checkout absent")
    X = io.load_pinned("L3")
    assert X.shape == (57, 1536)
    assert X.dtype == np.float64
