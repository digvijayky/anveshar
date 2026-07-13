"""Grade an alteration for therapeutic actionability from the curated rule table.

grade() is a thin, deterministic lookup over anveshar.variants._knowledge.RULES. It
returns an Actionability graded on the three published axes (OncoKB level,
AMP/ASCO/CAP tier, ESCAT tier). It NEVER guesses: if no curated rule matches the
query, it returns an empty Actionability so the caller can present the alteration as
not yet graded rather than inventing evidence.

Frameworks (see docs/variant_interpretation_methodology.md):
  OncoKB, Chakravarty et al 2017, PMID 28890946.
  AMP/ASCO/CAP, Li et al 2017, PMID 27993330.
  ESCAT, Mateo et al 2018, PMID 30137196.
"""
from __future__ import annotations
from ..schema import Actionability
from . import _knowledge


def grade(gene: str, variant: str, biomarker: str = "", condition: str = "") -> Actionability:
    """Return an Actionability for a (gene, variant, biomarker) query.

    Looks up the most specific matching rule in the curated table. If found, the
    returned Actionability carries the OncoKB level, AMP/ASCO/CAP tier, and ESCAT
    tier for the alteration to drug match named in the rule, plus a note that names
    the representative drug, the tumor context in which the level applies, and the
    real source citation (with PMID). If nothing matches, an empty Actionability is
    returned (every field blank), which the caller must treat as not graded, not as
    a negative result.

    The clinical tier is never elevated by this function beyond what the curated
    rule states, and a query that matches no rule is never assigned a tier.

    Args:
        gene: gene symbol, for example "BRAF". Empty for genome wide biomarkers.
        variant: variant string, for example "V600E" or "exon 14 skipping".
        biomarker: derived biomarker text, for example "MSI-H / dMMR" or "TMB-high".
        condition: tumor context (used for the note, not to fabricate a tier).

    Returns:
        A schema.Actionability. Empty when no curated rule applies.
    """
    rule = _knowledge.lookup(gene, variant, biomarker, condition)
    if rule is None:
        return Actionability()
    context = rule.context
    note_bits = [rule.note]
    if context:
        note_bits.append(f"Level applies in context: {context}.")
    note_bits.append(f"Representative therapy: {rule.drug}.")
    note_bits.append(f"Source: {rule.source}.")
    if rule.tumor_agnostic:
        note_bits.insert(1, "Tumor agnostic (tissue agnostic) approval.")
    return Actionability(
        oncokb_level=rule.oncokb_level,
        amp_asco_cap=rule.amp_asco_cap,
        escat=rule.escat,
        note=" ".join(note_bits),
    )
