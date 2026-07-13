"""Transparent confidence scoring for Anveshar.

Confidence is a rule based summary of how much weight to place on a match or a hypothesis.
It is deliberately simple and auditable: it is a function of the evidence tier and whether a
real citation is attached, and every score carries a plain basis string so a clinician can
check the reasoning. Confidence is NOT a probability of benefit for an individual patient.
"""

_TIER_BASE = {1: ("High", 90), 2: ("Moderate", 68), 3: ("Low", 42)}
_TIER_BASIS = {
    1: "FDA tissue agnostic approval on this biomarker",
    2: "approved in another condition on a shared target, or a prospective basket signal",
    3: "mechanistic or preclinical rationale only",
}


def therapy_confidence(therapy: dict) -> dict:
    """Confidence for a cross-condition therapy match: {label, pct, basis}."""
    tier = therapy.get("tier", 3)
    cited = bool((therapy.get("citation") or {}).get("url"))
    label, pct = _TIER_BASE.get(tier, ("Low", 42))
    if not cited:
        pct = max(15, pct - 20)
        label = "Low"
    basis = _TIER_BASIS.get(tier, _TIER_BASIS[3])
    basis += ", with a linked citation" if cited else ", citation missing so treat with caution"
    return {"label": label, "pct": pct, "basis": basis}


def hypothesis_confidence(hyp: dict) -> dict:
    """Confidence for a discovery hypothesis. Capped below High because it is untested here."""
    tr = (hyp.get("transferability") or "").lower()
    cited = bool((hyp.get("citation") or {}).get("url"))
    if "high" in tr:
        label, pct = "Moderate", 55
    elif "medium" in tr or "moderate" in tr:
        label, pct = "Low to moderate", 42
    else:
        label, pct = "Speculative", 26
    if not cited:
        pct = max(12, pct - 12)
    basis = ("research hypothesis not yet tested in this condition; transferability "
             + (hyp.get("transferability") or "unrated"))
    return {"label": label, "pct": pct, "basis": basis}


def score_report(data: dict) -> dict:
    """Attach a confidence object to every therapy and discovery hypothesis in a DATA dict."""
    for t in data.get("therapies", []) or []:
        t["confidence"] = therapy_confidence(t)
    for h in data.get("discovery", []) or []:
        h["confidence"] = hypothesis_confidence(h)
    return data
