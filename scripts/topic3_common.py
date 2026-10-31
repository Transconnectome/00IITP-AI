"""Shared run-record helpers for the Topic 3 scripts (card verification, hashing, logging)."""
import hashlib
import json
import os
import platform
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD = os.path.join(ROOT, "docs", "03_empirical_analysis", "topic3", "2026-10-31_topic3_analysis_card.md")
CARD_SHA_FILE = os.path.join(ROOT, "results", "topic3", "2026-10-31", "card_sha256.txt")
OUT = os.path.join(ROOT, "results", "topic3", "2026-10-31")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def verify_card():
    """Halt unless the card on disk equals the recorded frozen hash."""
    if not os.path.isfile(CARD_SHA_FILE):
        sys.exit("card hash record missing: card not frozen; refusing to run on real data")
    expected = open(CARD_SHA_FILE).read().split()[0]
    got = sha256(CARD)
    if got != expected:
        sys.exit("card sha256 mismatch (%s != %s); refusing to run" % (got, expected))
    return got


def run_record(script_path, extra_files=()):
    files = [script_path, os.path.join(ROOT, "scripts", "topic3_common.py")] + list(extra_files)
    pkg = os.path.join(ROOT, "src", "topic3_spectral")
    files += sorted(os.path.join(pkg, f) for f in os.listdir(pkg) if f.endswith(".py"))
    import numpy as np
    return {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "python": platform.python_version(),
            "numpy": np.__version__, "host": platform.node(),
            "code_sha256": {os.path.relpath(f, ROOT): sha256(f) for f in files}}


def dump(obj, name):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)
    return path
