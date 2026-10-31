"""Shared helpers for topic1_lagmotif tests (plain module, not a pytest conftest)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

ENIGMA = "/home/juke/git/enigma_ocd_mbbn"
NPY_DIR = os.path.join(ENIGMA, "data", "MBBN_data_304_ROIs_0.25")
META_CSV = os.path.join(ENIGMA, "data", "metadata", "ENIGMA_QC_final_subject_list.csv")
