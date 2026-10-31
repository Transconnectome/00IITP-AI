"""Site -> repetition time (TR, seconds) for the ENIGMA-OCD cohort.

Source (copied, not imported, so that importing this package never writes
bytecode into the read-only external repo):
    /home/juke/git/enigma_ocd_mbbn/time_series_utils.py:5-79, ``repetition_time(site)``.

The source function is an ordered chain of *substring* tests and raises on an
unknown site.  It has an ordering defect: ``'Chiba-CHB' in 'Chiba-CHBSRPB'`` is
true, so Chiba-CHBSRPB returns 2.3 instead of the listed 2.5 (and Chiba-CHBC
returns 2.3, which happens to equal its listed value).  Likewise
'Braga-UMinho-Braga-1.5T' shadows '-1.5T-act' (both 2.0, harmless).  None of
the Chiba / Kyoto-1.5T / Seoul / Shanghai sites have data on disk.

This module reproduces the source behaviour exactly (``repetition_time``),
including its first-match semantics, so that a test can assert equality with
the original function for every on-disk site.  The analysis pipeline uses
``analysis_tr`` which additionally refuses TR > 2.0 s (the common 2.0 s grid
cannot represent slower sampling without up-sampling, and no such site is on
disk).
"""
from __future__ import annotations

# Ordered exactly as in time_series_utils.py:7-76 (substring, TR).
_ORDERED_SUBSTRING_TR: tuple[tuple[str, float], ...] = (
    ("Amsterdam-AMC", 2.375),
    ("Amsterdam-VUmc", 1.8),
    ("Barcelona-HCPB", 2.0),
    ("Bergen", 1.8),
    ("Braga-UMinho-Braga-1.5T", 2.0),
    ("Braga-UMinho-Braga-1.5T-act", 2.0),
    ("Braga-UMinho-Braga-3T", 1.0),
    ("Brazil", 2.0),
    ("Cape-Town-UCT-Allegra", 1.6),
    ("Cape-Town-UCT-Skyra", 1.73),
    ("Chiba-CHB", 2.3),
    ("Chiba-CHBC", 2.3),
    ("Chiba-CHBSRPB", 2.5),
    ("Dresden", 0.8),
    ("Kyoto-KPU-Kyoto1.5T", 2.411),
    ("Kyoto-KPU-Kyoto3T", 2.0),
    ("Kyushu", 2.5),
    ("Milan-HSR", 2.0),
    ("New-York", 1.0),
    ("NYSPI-Columbia-Adults", 0.85),
    ("NYSPI-Columbia-Pediatric", 0.85),
    ("Yale-Pittinger-HCP-Prisma", 0.8),
    ("Yale-Pittinger-HCP-Trio", 0.7),
    ("Yale-Pittinger-Yale-2014", 2.0),
    ("Bangalore-NIMHANS", 2.0),
    ("Barcelone-Bellvitge-ANTIGA-1.5T", 2.0),
    ("Barcelone-Bellvitge-COMPULSE-3T", 2.0),
    ("Barcelone-Bellvitge-PROV-1.5T", 2.0),
    ("Barcelone-Bellvitge-RESP-CBT-3T", 2.0),
    ("Seoul-SNU", 3.5),
    ("Shanghai-SMCH", 3.0),
    ("UCLA", 2.0),
    ("Vancouver-BCCHR", 2.0),
    ("Yale-Gruner", 2.0),
)

MAX_ANALYSIS_TR = 2.0


class UnknownSiteError(ValueError):
    """Raised when a site has no TR entry."""


class UnsupportedTRError(ValueError):
    """Raised when a site's TR exceeds the common 2.0 s analysis grid."""


def repetition_time(site: str) -> float:
    """Exact re-implementation of enigma ``repetition_time`` (first substring match)."""
    for key, tr in _ORDERED_SUBSTRING_TR:
        if key in site:
            return float(tr)
    raise UnknownSiteError(f"Site '{site}' has no TR entry")


def analysis_tr(site: str) -> float:
    """TR used by the v2 pipeline; raises for TR > 2.0 s."""
    tr = repetition_time(site)
    if tr > MAX_ANALYSIS_TR + 1e-12:
        raise UnsupportedTRError(f"Site '{site}' TR={tr} s exceeds {MAX_ANALYSIS_TR} s grid")
    return tr
