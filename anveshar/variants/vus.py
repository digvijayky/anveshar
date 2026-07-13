"""Reclassify a variant of uncertain significance (VUS) with sequence models.

reclassify() takes an Alteration whose variant_class is VUS and attaches method
rationale for in silico triage, strictly as rationale and never as a fabricated
number or a promoted clinical tier. Two predictors are referenced:

  1. AlphaMissense, Cheng et al 2023, Science, PMID 37733863,
     DOI 10.1126/science.adg7492. Scores every possible human missense substitution
     as likely benign, ambiguous, or likely pathogenic. Applies only to missense
     substitutions.
  2. Evo 2, Brixi, Durrant, Ku et al 2025, bioRxiv DOI 10.1101/2025.02.18.638918;
     peer reviewed version Nature 2026, PMID 41781614. A DNA foundation model that
     scores coding, noncoding, and splice affecting variants zero shot, so it covers
     the cases AlphaMissense cannot.

Interpretation rule (docs/variant_interpretation_methodology.md Part A2 h): a
damaging or likely pathogenic prediction raises pre test suspicion and routes the
variant to functional confirmation. It is always labeled a computational prediction
and is NEVER by itself converted into a clinical tier. reclassify sets verified to
False on the returned Alteration.
"""
from __future__ import annotations
from dataclasses import replace
from ..schema import Alteration, VariantClass, Actionability

_ALPHAMISSENSE = "AlphaMissense (Cheng et al 2023, Science, PMID 37733863)"
_EVO2 = "Evo 2 (Brixi et al 2025, bioRxiv 10.1101/2025.02.18.638918; Nature 2026, PMID 41781614)"


def _looks_missense(alt: Alteration) -> bool:
    """Heuristic: does this VUS look like a single missense substitution.

    A missense change is a coding single amino acid substitution, for example V600E
    or R132H. Splice, noncoding, frameshift, and multi residue changes are routed to
    Evo 2 instead. This is a conservative text heuristic, not a sequence parse.
    """
    text = " ".join([alt.variant, alt.consequence]).lower()
    if any(k in text for k in ("splice", "noncoding", "non coding", "intron", "utr",
                               "frameshift", "fs", "promoter", "exon 14", "skip")):
        return False
    # A canonical missense token like p.Val600Glu or V600E: a letter, digits, a letter.
    import re
    if re.search(r"[a-z]\d+[a-z]", text):
        return True
    if "missense" in text:
        return True
    return False


def reclassify(alt: Alteration, client=None) -> Alteration:
    """Attach in silico triage rationale to a VUS and return an updated Alteration.

    Only VUS class alterations are reclassified; any other class is returned
    unchanged. For a VUS, the function chooses AlphaMissense for an apparent missense
    substitution and Evo 2 for splice, noncoding, or otherwise non missense changes,
    and writes a rationale sentence into the interpretation field. If a client is
    supplied (a WorkbenchClient exposing alphamissense or evo2 methods) the function
    records that the predictor was queried, but it does NOT fabricate a score: when
    the connector reports it is unavailable, the text says so. The clinical tier is
    left empty (the alteration is not promoted on a prediction alone) and verified is
    set to False so downstream rendering flags the alteration as unverified.

    Args:
        alt: the Alteration to triage. Must have variant_class VUS to be acted on.
        client: optional object with alphamissense(protein_change) and evo2(hgvs)
            methods (for example anveshar.evidence.workbench.WorkbenchClient). Network
            calls must degrade gracefully and never raise to this function.

    Returns:
        A new Alteration (the input is not mutated) with interpretation rationale
        appended, actionability left empty, and verified set to False. Non VUS input
        is returned unchanged.
    """
    if alt.variant_class != VariantClass.VUS:
        return alt

    use_missense = _looks_missense(alt)
    predictor = _ALPHAMISSENSE if use_missense else _EVO2
    scope = ("missense substitution" if use_missense
             else "coding, noncoding, or splice affecting change")

    queried = ""
    if client is not None:
        try:
            if use_missense and hasattr(client, "alphamissense"):
                res = client.alphamissense(alt.variant) or {}
            elif hasattr(client, "evo2"):
                res = client.evo2(alt.variant) or {}
            else:
                res = {}
            if isinstance(res, dict) and res.get("available") is False:
                queried = " The connector reported no live score available, so no numeric prediction is asserted."
            elif res:
                # A live result is treated as rationale only; the raw payload is not
                # converted into a clinical tier here.
                queried = " A computational prediction was retrieved and recorded as method rationale only."
        except Exception:
            # Per the interface contract, connector failures never raise to the caller.
            queried = ""

    rationale = (
        f"Variant of uncertain significance ({scope}). "
        f"Routed to {predictor} for in silico triage. "
        "A likely pathogenic or damaging prediction raises pre test suspicion and routes the variant to functional confirmation; "
        "it is method rationale only and is not promoted to a clinical tier on a prediction alone." + queried
    )

    existing = alt.interpretation.strip()
    new_interp = (existing + " " + rationale).strip() if existing else rationale

    return replace(
        alt,
        interpretation=new_interp,
        actionability=Actionability(),   # never assign a tier from a prediction alone
        verified=False,                  # flag as UNVERIFIED / illustrative
    )
