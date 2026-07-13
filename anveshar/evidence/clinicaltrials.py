"""ClinicalTrials.gov connector via the public API v2.

Endpoint (see https://clinicaltrials.gov/data-api/api):
  studies: https://clinicaltrials.gov/api/v2/studies

Query parameters used:
  query.cond            free text condition search
  query.intr            free text intervention search (optional)
  filter.overallStatus  study status, e.g. RECRUITING

``search`` returns a list of ``anveshar.schema.Trial`` objects. All network
access uses a short timeout and degrades to an empty list on any failure. The
pure parser ``_parse_studies`` turns a raw API v2 JSON payload into Trials and
can be unit tested offline.
"""
from __future__ import annotations
import requests
from ..schema import Trial

API = "https://clinicaltrials.gov/api/v2/studies"
STUDY_URL = "https://clinicaltrials.gov/study/"
TIMEOUT = 8


def _study_to_trial(study: dict) -> Trial:
    """Map one API v2 ``study`` object to a ``Trial``.

    Reads the ``protocolSection`` modules for the NCT id, title, phase,
    intervention names, and eligibility text. Returns a ``Trial`` with a blank
    ``nct`` if the id is missing (callers filter these out).
    """
    if not isinstance(study, dict):
        return Trial(nct="")
    proto = study.get("protocolSection", {}) or {}
    ident = proto.get("identificationModule", {}) or {}
    nct = (ident.get("nctId") or "").strip()
    title = (ident.get("briefTitle") or ident.get("officialTitle") or "").strip()

    design = proto.get("designModule", {}) or {}
    phases = design.get("phases", []) or []
    phase = ", ".join(p for p in phases if p) if phases else ""

    arms = proto.get("armsInterventionsModule", {}) or {}
    names = []
    for iv in arms.get("interventions", []) or []:
        nm = (iv.get("name") or "").strip()
        if nm:
            names.append(nm)
    intervention = "; ".join(names)

    elig = proto.get("eligibilityModule", {}) or {}
    eligibility = (elig.get("eligibilityCriteria") or "").strip()

    url = STUDY_URL + nct if nct else ""
    return Trial(nct=nct, title=title, phase=phase, intervention=intervention,
                 eligibility=eligibility, url=url)


def _parse_studies(payload: dict) -> list[Trial]:
    """Turn an API v2 studies JSON payload into a list of ``Trial`` objects.

    Iterates ``payload['studies']`` and drops any study with no NCT id. Returns
    an empty list on a malformed payload.
    """
    try:
        studies = payload.get("studies", [])
        out = []
        for s in studies:
            t = _study_to_trial(s)
            if t.nct:
                out.append(t)
        return out
    except (AttributeError, TypeError):
        return []


def search(condition: str, status: str = "RECRUITING", intervention: str | None = None) -> list[Trial]:
    """Search ClinicalTrials.gov for trials matching ``condition``.

    ``status`` is passed as ``filter.overallStatus`` (e.g. RECRUITING) and
    ``intervention``, when given, as ``query.intr``. Returns a list of ``Trial``
    objects, or an empty list on any network error, timeout, or unparseable
    response.
    """
    if not condition or not str(condition).strip():
        return []
    params = {"query.cond": condition, "pageSize": 50, "format": "json"}
    if status:
        params["filter.overallStatus"] = status
    if intervention:
        params["query.intr"] = intervention
    try:
        r = requests.get(API, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return _parse_studies(r.json())
    except (requests.RequestException, ValueError):
        return []
