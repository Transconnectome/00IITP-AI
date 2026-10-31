"""Read-only loader for the ENIGMA-OCD raw ROI time series (npy directory).

Layout (verified 2026-10-30): ``<npy_dir>/<UID>/<UID>.npy``, 1,706 subject
directories, each holding one float64 array of shape (T, 304), time x ROI,
unpadded, raw scale.  Directory and file names are participant IDs, so this
module exposes subjects ONLY by positional index into ``sorted(os.listdir)``
(which equals the row order of the VMD mmap cache) and never puts a name or a
path into an exception message or return value.

Valid portion rule (documented, frozen in pipeline.PARAMS):
  1. Trailing all-zero time rows are padding and are stripped (``raw_valid_T``).
  2. Any all-zero row *inside* the valid portion, any NaN/inf, or any ROI with
     zero variance raises ``InvalidSeriesError`` (no repair, no fallback).
  3. The first ``n_trim = ceil(trim_s / TR)`` samples are removed
     (lead-in / filter transient).  ``valid_T = raw_valid_T - n_trim``.
There is no synthetic fallback anywhere: a missing subject raises
``MissingSubjectError`` naming only the positional index.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass

import numpy as np

from .tr_table import analysis_tr


class MissingSubjectError(LookupError):
    """A requested subject (by position) has no readable series."""


class InvalidSeriesError(ValueError):
    """A subject's series violates the data contract."""


@dataclass(frozen=True)
class SubjectSeries:
    position: int
    site: str
    tr: float
    X: np.ndarray            # (valid_T, n_roi) float64, head-trimmed valid portion
    raw_valid_T: int         # samples before head trim (after stripping trailing zero rows)
    n_trim: int
    valid_T: int
    duration_s: float        # valid_T * tr


def valid_portion(arr: np.ndarray, position: int | str = "?") -> tuple[np.ndarray, int]:
    """Strip trailing all-zero rows; validate. Returns (array, raw_valid_T)."""
    a = np.asarray(arr, dtype=np.float64)
    if a.ndim != 2:
        raise InvalidSeriesError(f"position {position}: expected 2-D (T, ROI) array, got ndim={a.ndim}")
    if not np.all(np.isfinite(a)):
        raise InvalidSeriesError(f"position {position}: non-finite values")
    nonzero_rows = np.any(a != 0.0, axis=1)
    if not nonzero_rows.any():
        raise InvalidSeriesError(f"position {position}: all rows are zero")
    last = int(np.flatnonzero(nonzero_rows)[-1]) + 1
    a = a[:last]
    if not nonzero_rows[:last].all():
        raise InvalidSeriesError(f"position {position}: all-zero row inside valid portion")
    return a, last


def head_trim_samples(tr: float, trim_s: float) -> int:
    return int(math.ceil(trim_s / tr - 1e-9))


def prepare_series(arr: np.ndarray, tr: float, trim_s: float, position: int | str = "?",
                   site: str = "") -> SubjectSeries:
    a, raw_T = valid_portion(arr, position)
    n_trim = head_trim_samples(tr, trim_s)
    X = a[n_trim:]
    if X.shape[0] < 20:
        raise InvalidSeriesError(f"position {position}: only {X.shape[0]} samples after head trim")
    sd = X.std(axis=0)
    if np.any(sd <= 0):
        raise InvalidSeriesError(f"position {position}: zero-variance ROI(s)")
    pos = int(position) if isinstance(position, (int, np.integer)) else -1
    return SubjectSeries(position=pos, site=site, tr=float(tr), X=np.ascontiguousarray(X),
                         raw_valid_T=raw_T, n_trim=n_trim, valid_T=int(X.shape[0]),
                         duration_s=float(X.shape[0] * tr))


class NpyCohort:
    """Positional, read-only access to the npy directory plus site lookup.

    ``site_of`` maps a directory name (participant ID) to its acquisition site;
    it is supplied by ``from_metadata`` and kept private.  No diagnosis or other
    phenotype is loaded here.
    """

    def __init__(self, npy_dir: str, site_by_name: dict[str, str], trim_s: float):
        if not os.path.isdir(npy_dir):
            raise MissingSubjectError("npy directory not found")
        self._dir = npy_dir
        self._names = sorted(os.listdir(npy_dir))
        self._site = site_by_name
        self.trim_s = float(trim_s)

    @classmethod
    def from_metadata(cls, npy_dir: str, metadata_csv: str, trim_s: float) -> "NpyCohort":
        import pandas as pd
        meta = pd.read_csv(metadata_csv, usecols=["Unique_ID", "Sample"])
        site_by_name = dict(zip(meta["Unique_ID"].astype(str), meta["Sample"].astype(str)))
        return cls(npy_dir, site_by_name, trim_s)

    def __len__(self) -> int:
        return len(self._names)

    def site(self, position: int) -> str:
        name = self._name(position)
        if name not in self._site:
            raise MissingSubjectError(f"position {position}: no metadata row")
        return self._site[name]

    def tr(self, position: int) -> float:
        return analysis_tr(self.site(position))

    def _name(self, position: int) -> str:
        if not isinstance(position, (int, np.integer)) or position < 0 or position >= len(self._names):
            raise MissingSubjectError(f"position {position}: out of range (n={len(self._names)})")
        return self._names[int(position)]

    def load(self, position: int) -> SubjectSeries:
        name = self._name(position)
        site = self.site(position)
        tr = analysis_tr(site)
        path = os.path.join(self._dir, name, name + ".npy")
        if not os.path.isfile(path):
            raise MissingSubjectError(f"position {position}: series file missing")
        try:
            arr = np.load(path, mmap_mode="r", allow_pickle=False)
            arr = np.array(arr, dtype=np.float64, copy=True)
        except (OSError, ValueError) as exc:  # unreadable/corrupt file
            raise MissingSubjectError(f"position {position}: series unreadable ({type(exc).__name__})") from None
        return prepare_series(arr, tr, self.trim_s, position=int(position), site=site)
