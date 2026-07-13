"""PubMed connector via NCBI E-utilities (esearch and esummary).

Endpoints (see https://www.ncbi.nlm.nih.gov/books/NBK25501/):
  esearch:  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
  esummary: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi

Public functions return a normalized record shape
``{pmid, title, journal, year, doi}``. All network access uses a short timeout
and degrades to an empty result ([] or {}) on any failure, never raising to the
caller. The payload parsers ``_parse_esearch`` and ``_parse_esummary`` are pure
and can be unit tested offline.
"""
from __future__ import annotations
import requests

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TIMEOUT = 8


def _parse_esearch(payload: dict) -> list[str]:
    """Extract the list of PMID strings from an esearch JSON payload.

    Returns an empty list if the payload has no id list.
    """
    try:
        ids = payload.get("esearchresult", {}).get("idlist", [])
        return [str(i) for i in ids if str(i).strip()]
    except (AttributeError, TypeError):
        return []


def _doc_to_record(doc: dict) -> dict:
    """Map one esummary document object to ``{pmid, title, journal, year, doi}``."""
    if not isinstance(doc, dict):
        return {}
    pmid = str(doc.get("uid", "") or "").strip()
    title = (doc.get("title") or "").strip()
    journal = (doc.get("fulljournalname") or doc.get("source") or "").strip()
    pubdate = (doc.get("pubdate") or doc.get("sortpubdate") or "").strip()
    year = ""
    for token in pubdate.replace("/", " ").split():
        if len(token) == 4 and token.isdigit():
            year = token
            break
    doi = ""
    for aid in doc.get("articleids", []) or []:
        if isinstance(aid, dict) and aid.get("idtype") == "doi":
            doi = (aid.get("value") or "").strip()
            break
    if not doi:
        doi = (doc.get("elocationid") or "").replace("doi:", "").strip()
    return {"pmid": pmid, "title": title, "journal": journal, "year": year, "doi": doi}


def _parse_esummary(payload: dict) -> list[dict]:
    """Turn an esummary JSON payload into a list of normalized records.

    Iterates the ``result`` object in the order given by its ``uids`` list and
    returns one ``{pmid, title, journal, year, doi}`` dict per document. Returns
    an empty list on a malformed payload.
    """
    try:
        result = payload.get("result", {})
        uids = result.get("uids", [])
        out = []
        for uid in uids:
            doc = result.get(str(uid))
            rec = _doc_to_record(doc)
            if rec.get("pmid"):
                out.append(rec)
        return out
    except (AttributeError, TypeError):
        return []


def search(query: str, retmax: int = 20) -> list[dict]:
    """Search PubMed for ``query`` and return up to ``retmax`` article records.

    Runs esearch to collect PMIDs, then esummary to resolve each to a
    ``{pmid, title, journal, year, doi}`` dict. Returns an empty list on any
    network error, timeout, or unparseable response.
    """
    if not query or not str(query).strip():
        return []
    try:
        r = requests.get(
            f"{EUTILS}/esearch.fcgi",
            params={"db": "pubmed", "term": query, "retmax": int(retmax), "retmode": "json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        pmids = _parse_esearch(r.json())
    except (requests.RequestException, ValueError):
        return []
    if not pmids:
        return []
    try:
        r = requests.get(
            f"{EUTILS}/esummary.fcgi",
            params={"db": "pubmed", "id": ",".join(pmids), "retmode": "json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return _parse_esummary(r.json())
    except (requests.RequestException, ValueError):
        return []


def fetch(pmid: str) -> dict:
    """Fetch one PubMed record by ``pmid`` as ``{pmid, title, journal, year, doi}``.

    Returns an empty dict if ``pmid`` is blank, the record is not found, or the
    request fails.
    """
    if not pmid or not str(pmid).strip():
        return {}
    try:
        r = requests.get(
            f"{EUTILS}/esummary.fcgi",
            params={"db": "pubmed", "id": str(pmid).strip(), "retmode": "json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        records = _parse_esummary(r.json())
    except (requests.RequestException, ValueError):
        return {}
    return records[0] if records else {}
