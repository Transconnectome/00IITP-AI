"""A1: TR table, read-only positional loader, valid-portion rule, explicit missing-subject errors."""
import importlib.util
import os
import sys

import numpy as np
import pytest

from tests.topic1_lagmotif.conftest_helpers import ENIGMA, META_CSV, NPY_DIR
from src.topic1_lagmotif import tr_table
from src.topic1_lagmotif.data import (InvalidSeriesError, MissingSubjectError, NpyCohort, head_trim_samples,
                                      prepare_series)


def _load_enigma_repetition_time():
    path = os.path.join(ENIGMA, "time_series_utils.py")
    if not os.path.isfile(path):
        pytest.skip("enigma repo not present")
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # never write __pycache__ into the read-only repo
    try:
        spec = importlib.util.spec_from_file_location("_enigma_tsu_readonly", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = old
    return mod.repetition_time


def test_tr_table_equals_enigma_for_every_table_entry_and_on_disk_site():
    rt = _load_enigma_repetition_time()
    import pandas as pd
    sites = set(pd.read_csv(META_CSV, usecols=["Sample"])["Sample"].astype(str))
    names = set(os.listdir(NPY_DIR))
    meta = pd.read_csv(META_CSV, usecols=["Unique_ID", "Sample"])
    on_disk = set(meta.loc[meta["Unique_ID"].astype(str).isin(names), "Sample"].astype(str))
    assert len(on_disk) == 23
    for s in sorted(sites | {k for k, _ in tr_table._ORDERED_SUBSTRING_TR}):
        assert tr_table.repetition_time(s) == pytest.approx(float(rt(s)), abs=0), s
    for s in on_disk:
        assert tr_table.analysis_tr(s) <= 2.0


def test_tr_table_reproduces_chiba_substring_order_defect_and_rejects_slow_or_unknown_sites():
    assert tr_table.repetition_time("Chiba-CHBSRPB") == 2.3  # source defect (listed 2.5)
    with pytest.raises(tr_table.UnsupportedTRError):
        tr_table.analysis_tr("Seoul-SNU")
    with pytest.raises(tr_table.UnknownSiteError):
        tr_table.repetition_time("Nowhere-Site")


def _fake_cohort(tmp_path, arrays, site="Yale-Gruner"):
    """Temporary npy dir with fake participant names; returns (cohort, names)."""
    d = tmp_path / "npy"
    d.mkdir()
    names = []
    for k, arr in enumerate(arrays):
        name = f"FAKEID{1000 + k}xq"
        names.append(name)
        (d / name).mkdir()
        if arr is not None:
            np.save(d / name / f"{name}.npy", arr)
    return NpyCohort(str(d), {n: site for n in names}, trim_s=40.0), names


def test_missing_subject_raises_without_participant_id(tmp_path):
    rng = np.random.default_rng(0)
    coh, names = _fake_cohort(tmp_path, [1e4 + rng.standard_normal((150, 8)), None])
    coh.load(0)
    with pytest.raises(MissingSubjectError) as ei:
        coh.load(1)
    assert names[1] not in str(ei.value) and "position 1" in str(ei.value)
    with pytest.raises(MissingSubjectError) as ei:
        coh.load(5)
    assert "FAKEID" not in str(ei.value)
    coh2 = NpyCohort(coh._dir, {}, trim_s=40.0)  # no metadata row -> explicit error, no fallback
    with pytest.raises(MissingSubjectError) as ei:
        coh2.load(0)
    assert names[0] not in str(ei.value)


def test_padding_rows_are_stripped_by_loader_and_features_identical(tmp_path):
    from src.topic1_lagmotif.pipeline import PARAMS, extract_subject, subject_flow
    rng = np.random.default_rng(1)
    base = 1.15e4 + 30 * rng.standard_normal((160, 12))
    padded = np.vstack([base, np.zeros((304 - 160, 12))])
    coh, _ = _fake_cohort(tmp_path, [base, padded])
    a, b = coh.load(0), coh.load(1)
    assert a.raw_valid_T == b.raw_valid_T == 160
    assert a.valid_T == b.valid_T == 160 - 20  # TR 2.0: ceil(40/2) = 20 trimmed
    assert np.array_equal(subject_flow(a), subject_flow(b))
    fa = extract_subject(a, densities=[0.10], channels=["broadband"], n_null=50)
    fb = extract_subject(b, densities=[0.10], channels=["broadband"], n_null=50)
    # positions differ -> different seeds; compare the deterministic parts
    ra, rb = fa["results"]["broadband@0.10"], fb["results"]["broadband@0.10"]
    assert ra["observed"] == rb["observed"]
    assert fa["gradient_share"] == fb["gradient_share"]
    assert PARAMS["head_trim_s"] == 40.0


def test_invalid_series_raise():
    rng = np.random.default_rng(2)
    x = rng.standard_normal((100, 5)) + 5
    bad = x.copy(); bad[50] = 0.0
    with pytest.raises(InvalidSeriesError):
        prepare_series(bad, 2.0, 40.0)
    nanx = x.copy(); nanx[3, 2] = np.nan
    with pytest.raises(InvalidSeriesError):
        prepare_series(nanx, 2.0, 40.0)
    const = x.copy(); const[:, 1] = 3.0
    with pytest.raises(InvalidSeriesError):
        prepare_series(const, 2.0, 40.0)


def test_head_trim_is_defined_in_seconds():
    assert head_trim_samples(2.0, 40.0) == 20
    assert head_trim_samples(0.7, 40.0) == 58
    assert head_trim_samples(1.73, 40.0) == 24
    assert head_trim_samples(0.8, 40.0) == 50


def test_real_npy_directory_is_positional_and_read_only():
    if not os.path.isdir(NPY_DIR):
        pytest.skip("real data not present")
    coh = NpyCohort.from_metadata(NPY_DIR, META_CSV, trim_s=40.0)
    assert len(coh) == 1706
    # metadata lookup only (no series loaded here; A3 timing loads <= 5 subjects)
    trs = {coh.tr(i) for i in (0, len(coh) - 1)}
    assert all(0.7 <= t <= 2.0 for t in trs)
