"""ClinVar connector via NCBI E-utilities (db=clinvar esearch and esummary).

Endpoints (see https://www.ncbi.nlm.nih.gov/books/NBK25501/):
  esearch:  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
  esummary: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi

``lookup`` returns ``{accession, significance, url}`` for the top ClinVar hit,
or an empty dict if nothing is found. Clinical significance is only ever read
back from ClinVar, never invented: if the record has no significance the field
is left as an empty string. All network access uses a short timeout and
degrades to an empty dict on failure. The pure parser ``_parse_clinvar`` turns
a raw esummary payload into the result dict and can be unit tested offline.
"""
from __future__ import annotations
import requests

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RECORD_URL = "https://www.ncbi.nlm.nih.gov/clinvar/variation/"
TIMEOUT = 8


def _extract_significance(doc: dict) -> str:
    """Read the clinical significance description from a ClinVar esummary doc.

    Handles both the ``germline_classification`` and legacy
    ``clinical_significance`` shapes. Returns an empty string when absent, so a
    significance is never fabricated.
    """
    gc = doc.get("germline_classification")
    if isinstance(gc, dict):
        desc = (gc.get("description") or "").strip()
        if desc:
            return desc
    cs = doc.get("clinical_significance")
    if isinstance(cs, dict):
        desc = (cs.get("description") or "").strip()
        if desc:
            return desc
    return ""


def _parse_clinvar(payload: dict) -> dict:
    """Turn a ClinVar esummary JSON payload into ``{accession, significance, url}``.

    Uses the first uid in the ``result`` object. Returns an empty dict if the
    payload has no usable record. ``significance`` may be an empty string but is
    never guessed.
    """
    try:
        result = payload.get("result", {})
        uids = result.get("uids", [])
        if not uids:
            return {}
        uid = str(uids[0])
        doc = result.get(uid, {})
        if not isinstance(doc, dict):
            return {}
        accession = (doc.get("accession") or "").strip()
        significance = _extract_significance(doc)
        url = f"{RECORD_URL}{uid}/" if uid else ""
        if not accession and not url:
            return {}
        return {"accession": accession, "significance": significance, "url": url}
    except (AttributeError, TypeError, IndexError):
        return {}


def lookup(term: str) -> dict:
    """Look up a ClinVar variant by free text ``term``.

    Runs esearch (db=clinvar) to find the top variation id, then esummary to
    resolve ``{accession, significance, url}``. Returns an empty dict if nothing
    is found or on any network error, timeout, or unparseable response. Clinical
    significance is read from ClinVar only and never invented.
    """
    if not term or not str(term).strip():
        return {}
    try:
        r = requests.get(
            f"{EUTILS}/esearch.fcgi",
            params={"db": "clinvar", "term": term, "retmax": 1, "retmode": "json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
    except (requests.RequestException, ValueError, AttributeError):
        return {}
    if not ids:
        return {}
    try:
        r = requests.get(
            f"{EUTILS}/esummary.fcgi",
            params={"db": "clinvar", "id": str(ids[0]), "retmode": "json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return _parse_clinvar(r.json())
    except (requests.RequestException, ValueError):
        return {}
