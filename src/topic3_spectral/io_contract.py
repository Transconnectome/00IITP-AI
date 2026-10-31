"""Data contract for Topic 3 inputs (numpy only, Python 3.8 compatible).

- Pooled matrices are read in place from the read-only VRABES checkout, under sha256 pins.
  A missing file raises FileNotFoundError and a hash mismatch raises ValueError. There is
  NO synthetic fallback (contrast: protected src/spectral_rg_flow_diagnostic.py falls back
  to random data when a file is missing).
- npz files are opened with allow_pickle=False. Only X is ever returned. The `ids` array is
  used only in memory to check row order / subset positions and is never returned,
  printed or written.
- Frame dumps (torch zip format) are read without torch through a restricted unpickler
  that only allows tensor rebuilding, storage types and OrderedDict.
"""
import collections
import hashlib
import io
import os
import pickle
import zipfile

import numpy as np

VRABES_RA = "/home/juke/git/VRABES/RemissionAnalysis"

# sha256 pins recorded by explorer_M2_r1_2 (handoff O1) and re-verified by
# scripts/topic3_provenance_repro.py before the card was frozen.
PINNED = collections.OrderedDict([
    ("L0", ("pooled_E192_layers/layer_0.npz", "ec2970e871b8b060d24db177d8b7f45ad6302f9ee57f8c6c0e6b9a8a6627e584")),
    ("L1", ("pooled_E192_layers/layer_1.npz", "2730359bfc0bd208c9c6e43ebbbc7ceccf657a55005934e5e4511a3dbaa5be4d")),
    ("L2", ("pooled_E192_layers/layer_2.npz", "ce55160669f77870c11ead261e5c061680791a4c755e8ea7d0db58c957828eab")),
    ("L3", ("pooled_E192_layers/layer_3.npz", "f13ae7ba126bdc5a2c17efc0cb032910c07b7e14411aeb9546deb9d68dadc8eb")),
    ("BrainLM", ("pooled_brainlm_matrix.npz", "d0b90e46ec638d5c00e0d6c0747030ef2b5b3788f097c5585e60c71e5085a80a")),
    ("BrainJEPA", ("pooled_brainjepa_matrix.npz", "c9c550d73acb599cc646fd5d9902e36c839e504b4a7e1983ed4a491509a4df87")),
    ("NeuroSTORM", ("pooled_neurostorm_matrix.npz", "3d7b2c9630e773a1f720c9731856bea6cba9ae27232b01a47afcdf29edd2f4da")),
])


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _checked_npz(path, expected_sha256):
    if not os.path.isfile(path):
        raise FileNotFoundError("required input missing: %s (no synthetic fallback)" % path)
    got = sha256_file(path)
    if got != expected_sha256:
        raise ValueError("sha256 mismatch for %s: expected %s got %s" % (path, expected_sha256, got))
    return np.load(path, allow_pickle=False)


def load_X(path, expected_sha256):
    """Return only the float64 X matrix of a pinned npz. Raises on missing file / mismatch /
    non-finite values / non-2-D X."""
    z = _checked_npz(path, expected_sha256)
    try:
        X = np.asarray(z["X"], dtype=np.float64)
    finally:
        z.close()
    if X.ndim != 2:
        raise ValueError("X must be 2-D in %s" % path)
    if not np.all(np.isfinite(X)):
        raise ValueError("non-finite values in %s" % path)
    return X


def load_pinned(name, root=VRABES_RA, pins=PINNED):
    rel, sha = pins[name]
    return load_X(os.path.join(root, rel), sha)


def positional_alignment(paths_and_hashes, subset_path_and_hash=None):
    """Check, in memory only, that all full files share one row order, and locate the rows of
    an optional subset file inside that order.

    Returns dict(same_order=bool, n_rows=int, subset_positions=list[int] or None,
    subset_in_increasing_order=bool or None). Never returns or prints identifiers.
    """
    ref = None
    same = True
    for path, sha in paths_and_hashes:
        z = _checked_npz(path, sha)
        try:
            ids = np.asarray(z["ids"])
        finally:
            z.close()
        if ref is None:
            ref = ids
        elif ids.shape != ref.shape or not bool(np.all(ids == ref)):
            same = False
    out = {"same_order": bool(same), "n_rows": int(ref.shape[0]), "subset_positions": None,
           "subset_in_increasing_order": None}
    if subset_path_and_hash is not None:
        z = _checked_npz(*subset_path_and_hash)
        try:
            sub = np.asarray(z["ids"])
        finally:
            z.close()
        lookup = {}
        for i, v in enumerate(ref.tolist()):
            lookup[v] = i
        missing = [v for v in sub.tolist() if v not in lookup]
        if missing:
            raise ValueError("%d subset rows are not in the reference order" % len(missing))
        pos = [lookup[v] for v in sub.tolist()]
        out["subset_positions"] = [int(p) for p in pos]
        out["subset_in_increasing_order"] = bool(all(pos[i] < pos[i + 1] for i in range(len(pos) - 1)))
    del ref
    return out


def ids_order_matches_names(npz_path, expected_sha256, names):
    """True iff the npz ids equal `names` element-wise (in-memory comparison, boolean out)."""
    z = _checked_npz(npz_path, expected_sha256)
    try:
        ids = [str(v) for v in np.asarray(z["ids"]).tolist()]
    finally:
        z.close()
    return bool(ids == [str(v) for v in names])


# ---------------------------------------------------------------- .pt reader (no torch)
_STORAGE_DTYPES = {"FloatStorage": np.float32, "DoubleStorage": np.float64, "HalfStorage": np.float16}


class _StorageType(object):
    def __init__(self, name):
        self.name = name


def _rebuild_tensor_v2(storage, offset, size, stride, *unused):
    item = storage.dtype.itemsize
    if len(size) == 0:
        return storage[offset:offset + 1].reshape(()).copy()
    return np.lib.stride_tricks.as_strided(
        storage[offset:], shape=tuple(size), strides=tuple(s * item for s in stride)).copy()


class RestrictedUnpickler(pickle.Unpickler):
    """Allows only torch tensor rebuilding, storage types and OrderedDict; anything else raises
    pickle.UnpicklingError (no arbitrary code execution from .pt files)."""

    def __init__(self, fileobj, zf, prefix):
        pickle.Unpickler.__init__(self, fileobj)
        self._zf = zf
        self._prefix = prefix

    def find_class(self, module, name):
        if module == "torch._utils" and name == "_rebuild_tensor_v2":
            return _rebuild_tensor_v2
        if module == "torch" and name in _STORAGE_DTYPES:
            return _StorageType(name)
        if module == "collections" and name == "OrderedDict":
            return collections.OrderedDict
        raise pickle.UnpicklingError("blocked class %s.%s" % (module, name))

    def persistent_load(self, pid):
        if not (isinstance(pid, tuple) and len(pid) >= 5 and pid[0] == "storage"):
            raise pickle.UnpicklingError("unsupported persistent id")
        st, key = pid[1], pid[2]
        if not isinstance(st, _StorageType):
            raise pickle.UnpicklingError("unsupported storage type")
        raw = self._zf.read(("%s/data/%s" % (self._prefix, key)) if self._prefix else ("data/%s" % key))
        return np.frombuffer(raw, dtype=_STORAGE_DTYPES[st.name])


def load_pt_numpy(path):
    """Read a torch.save zip file holding a dict of float tensors into numpy arrays."""
    if not os.path.isfile(path):
        raise FileNotFoundError("frame missing: %s" % path)
    with zipfile.ZipFile(path) as zf:
        pkls = [n for n in zf.namelist() if n.endswith("/data.pkl") or n == "data.pkl"]
        if len(pkls) != 1:
            raise ValueError("not a torch zip archive (data.pkl count %d)" % len(pkls))
        prefix = pkls[0].rsplit("/", 1)[0] if "/" in pkls[0] else ""
        obj = RestrictedUnpickler(io.BytesIO(zf.read(pkls[0])), zf, prefix).load()
    return obj
