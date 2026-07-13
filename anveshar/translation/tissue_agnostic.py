"""Tissue-agnostic (tumor-agnostic) FDA approval table for Anveshar.

This module loads the curated, cited approval list in
``data/tissue_agnostic_approvals.json`` into typed ``Precedent`` objects and
exposes a single lookup, :func:`for_biomarker`, that returns the Tier 1
``Therapy`` licensed by a biomarker if (and only if) that biomarker is present.

Every entry is anchored to a real PubMed PMID for the pivotal study. No drug,
trial, or citation here is fabricated; the JSON is the single source of truth,
so adding an approval means editing the JSON, not this code.
"""
from __future__ import annotations

import json
import os
import re

from ..schema import Precedent, Therapy, Tier, Modality, Citation

# Locate data/tissue_agnostic_approvals.json relative to the repo root
# (this file is concord/translation/tissue_agnostic.py, so go up three levels).
_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.normpath(os.path.join(_HERE, "..", "..", "data", "tissue_agnostic_approvals.json"))

_MODALITY_BY_VALUE = {m.value: m for m in Modality}


def _normalize(text: str) -> str:
    """Lowercase and strip punctuation and spacing so biomarker names match loosely.

    ``MSI-H / dMMR``, ``msi h``, and ``MSI H`` all collapse to ``msih``; this lets
    a caller pass a biomarker in any common surface form.
    """
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def _load_raw() -> list[dict]:
    """Read and return the raw approval records from the JSON data file."""
    with open(_DATA, "r", encoding="utf-8") as fh:
        return json.load(fh)["approvals"]


def _to_precedent(rec: dict) -> Precedent:
    """Convert one raw approval record into a typed, cited ``Precedent``."""
    label = (
        f"FDA tissue-agnostic approval ({rec['year']}): {rec['drug']} for "
        f"{rec['biomarker']} (PMID {rec['pmid']})"
    )
    return Precedent(
        biomarker=rec["biomarker"],
        drug=rec["drug"],
        year=str(rec["year"]),
        citation=Citation(label=label, url=rec["url"]),
    )


# Public, import-time constant: the curated tissue-agnostic precedent table.
PRECEDENTS: list[Precedent] = [_to_precedent(r) for r in _load_raw()]

# Parallel raw records kept so for_biomarker can recover modality and biomarker aliases.
_RAW: list[dict] = _load_raw()

# Biomarker aliases that should resolve to the same approval as the canonical name.
_ALIASES = {
    "dmmr": "MSI-H / dMMR",
    "mmrd": "MSI-H / dMMR",
    "msih": "MSI-H / dMMR",
    "msihigh": "MSI-H / dMMR",
    "microsatelliteinstabilityhigh": "MSI-H / dMMR",
    "tmbhigh": "TMB-high",
    "hightmb": "TMB-high",
    "her2ihc3": "HER2 IHC 3+",
    "her2ihc3plus": "HER2 IHC 3+",
    "ntrkfusion": "NTRK fusion",
    "ntrk": "NTRK fusion",
    "retfusion": "RET fusion",
    "ret": "RET fusion",
    "brafv600e": "BRAF V600E",
}


def for_biomarker(biomarker: str) -> Therapy | None:
    """Return the Tier 1 tissue-agnostic ``Therapy`` licensed by ``biomarker``.

    The lookup is tolerant of surface form (case, spacing, punctuation) and of a
    small set of aliases (for example ``dMMR`` maps to the MSI-H / dMMR approval).
    When a biomarker matches more than one approval (MSI-H / dMMR maps to both
    pembrolizumab and dostarlimab), the earliest, first-in-class approval is
    returned so the primary tissue-agnostic precedent is surfaced.

    Args:
        biomarker: A biomarker string such as ``"MSI-H"``, ``"BRAF V600E"``,
            ``"NTRK fusion"``, or ``"HER2 IHC 3+"``.

    Returns:
        A ``Therapy`` with ``tier=Tier.T1`` if the biomarker unlocks a
        tissue-agnostic approval, otherwise ``None``. Never a fabricated match.
    """
    if not biomarker:
        return None
    key = _normalize(biomarker)
    canonical = _ALIASES.get(key)

    matches = []
    for rec in _RAW:
        rec_key = _normalize(rec["biomarker"])
        if rec_key == key or (canonical and _normalize(canonical) == rec_key):
            matches.append(rec)
    if not matches:
        return None

    # Prefer the earliest approval year so the first-in-class precedent wins.
    rec = sorted(matches, key=lambda r: str(r["year"]))[0]
    modality = _MODALITY_BY_VALUE.get(rec.get("modality", ""), Modality.OTHER)
    label = (
        f"FDA tissue-agnostic approval ({rec['year']}): {rec['drug']} for "
        f"{rec['biomarker']} (PMID {rec['pmid']})"
    )
    return Therapy(
        drug=rec["drug"],
        target=rec["biomarker"],
        tier=Tier.T1,
        modality=modality,
        approved_in=f"tissue-agnostic ({rec['biomarker']}), FDA {rec['year']}",
        dev_stage="FDA approved (tissue-agnostic)",
        rationale={
            "clinician": (
                f"{rec['biomarker']} unlocks the tissue-agnostic {rec['drug']} approval "
                f"({rec['year']}); it applies to this condition only if the biomarker is "
                f"documented in this tumor."
            ),
        },
        citation=Citation(label=label, url=rec["url"]),
    )
