"""Parse a raw patient profile dict into a fully typed PatientProfile.

interpret_profile() is the module entry point. It accepts a raw dict shaped like the
files in examples/profiles/ and returns a schema.PatientProfile in which every
alteration has been classified (anveshar.variants.classes.classify), graded
(anveshar.variants.actionability.grade), and, where the class is VUS, triaged
(anveshar.variants.vus.reclassify).

It tolerates BOTH raw alteration shapes:

  Rich agent schema:
    {gene, class, variant, consequence, biomarker,
     actionability: {oncokb_level, amp_asco_cap, escat, note},
     evidence, maps_to_target, interpretation_note, pathogenicity, pathoUrl}

  Report schema (as in examples/profiles/*.json):
    {gene, cls, variant, actionability: "<free text string>", target,
     note, pathogenicity, pathoUrl}

The parser reads whichever fields are present. A curated actionability grade from
the rule table is preferred; when the rule table has nothing, any actionability text
already present in the raw record is preserved (never discarded, never invented).
"""
from __future__ import annotations
from ..schema import (
    PatientProfile, Alteration, Actionability, Citation, VariantClass,
)
from .classes import classify
from .actionability import grade
from .vus import reclassify


def _first(d: dict, *keys, default=""):
    """Return the first present, truthy value among keys, else default."""
    for k in keys:
        v = d.get(k)
        if v:
            return v
    return default


def _actionability_from_raw(raw_alt: dict) -> Actionability:
    """Build an Actionability from whatever actionability field the raw record carries.

    Handles the two shapes: a nested dict (rich agent schema) or a free text string
    (report schema). Nothing is invented; missing fields stay empty. If the raw text
    is a single string it is preserved in the note so it is not lost, but it is not
    parsed into tiers (tiers only come from the curated rule table).
    """
    a = raw_alt.get("actionability")
    if isinstance(a, dict):
        return Actionability(
            oncokb_level=a.get("oncokb_level", "") or "",
            amp_asco_cap=a.get("amp_asco_cap", "") or "",
            escat=a.get("escat", "") or "",
            note=a.get("note", "") or "",
        )
    if isinstance(a, str) and a.strip():
        return Actionability(note=a.strip())
    return Actionability()


def _parse_alteration(raw_alt: dict) -> Alteration:
    """Turn one raw alteration record (either shape) into a typed Alteration.

    Steps: classify the variant class, read gene, variant, biomarker, target, and
    interpretation from whichever keys are present, grade with the curated rule
    table, and fall back to the raw actionability text when the table has no match.
    If the resulting class is VUS, the alteration is routed through vus.reclassify so
    it is flagged unverified with in silico triage rationale and no clinical tier.
    """
    vclass = classify(raw_alt)
    gene = raw_alt.get("gene", "") or ""
    variant = raw_alt.get("variant", "") or ""
    consequence = raw_alt.get("consequence", "") or ""
    biomarker = _first(raw_alt, "biomarker")
    target = _first(raw_alt, "maps_to_target", "target")
    interp = _first(raw_alt, "interpretation_note", "note", "interpretation")
    patho = raw_alt.get("pathogenicity", "") or ""
    patho_url = _first(raw_alt, "pathoUrl", "pathogenicity_url")

    # If no explicit biomarker field, use the target text as the biomarker signal for
    # composite genome wide findings (for example "MSI-H / dMMR"), which lets the rule
    # table grade them.
    biomarker_for_grade = biomarker or (target if vclass == VariantClass.COMPOSITE else "")

    graded = grade(gene, variant, biomarker_for_grade)
    raw_action = _actionability_from_raw(raw_alt)
    # Prefer the curated, cited grade; preserve raw text when the table has no match.
    if graded.oncokb_level or graded.amp_asco_cap or graded.escat:
        action = graded
        if raw_action.note and raw_action.note not in action.note:
            action.note = (action.note + " Report note: " + raw_action.note).strip()
    else:
        action = raw_action

    alt = Alteration(
        gene=gene,
        variant_class=vclass,
        variant=variant,
        consequence=consequence,
        biomarker=biomarker,
        actionability=action,
        pathogenicity=patho,
        pathogenicity_url=patho_url,
        target=target,
        interpretation=interp,
        verified=True,
    )
    if vclass == VariantClass.VUS:
        alt = reclassify(alt)
    return alt


def interpret_profile(raw: dict) -> PatientProfile:
    """Parse a raw profile dict into a typed, classified, graded PatientProfile.

    Accepts a dict shaped like examples/profiles/pereira_msi_braf.json or
    examples/profiles/klempner_braf.json. Reads the source citation, tumor summary,
    per persona summary, excluded targets, and the list of alterations. Each raw
    alteration is classified, graded against the curated rule table, and VUS triaged.
    Both the rich agent alteration shape and the terse report shape are accepted.

    Args:
        raw: the raw profile dict. Recognized top level keys: present, source
            ({label, url}), tumor ({summary}) or tumor_summary, summary
            ({patient, clinician, researcher}), alterations (list), excluded (list).

    Returns:
        A schema.PatientProfile with typed alterations. Never fabricates an
        alteration; only what is present in the input is parsed.
    """
    if not isinstance(raw, dict):
        raise TypeError("interpret_profile expects a dict profile")

    src = raw.get("source") or {}
    source = Citation(label=src.get("label", "") or "", url=src.get("url", "") or "")

    tumor = raw.get("tumor") or {}
    tumor_summary = tumor.get("summary", "") if isinstance(tumor, dict) else ""
    tumor_summary = tumor_summary or raw.get("tumor_summary", "") or ""

    alterations = [_parse_alteration(a) for a in (raw.get("alterations") or []) if isinstance(a, dict)]

    return PatientProfile(
        present=bool(raw.get("present", True)),
        source=source,
        tumor_summary=tumor_summary,
        alterations=alterations,
        excluded=list(raw.get("excluded") or []),
        summary=dict(raw.get("summary") or {}),
    )
