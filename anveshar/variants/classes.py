"""Map a raw alteration record to a VariantClass.

The classifier is deliberately keyword driven and order sensitive so it works over
the several raw shapes Anveshar ingests: the rich agent schema (fields "class",
"consequence", "biomarker"), the report schema (field "cls"), and terse free text.
It reads gene, variant, consequence, and biomarker text together and returns the
most specific VariantClass it can justify. When nothing specific matches it falls
back to SNV rather than guessing an exotic class.

Variant classes are defined in docs/variant_interpretation_methodology.md Part A2.
"""
from __future__ import annotations
from ..schema import VariantClass

# Explicit spellings a raw record may already carry in a class or cls field, mapped
# to the canonical enum. Keys are normalized (lowercase, dashes and underscores to
# spaces).
_EXPLICIT = {
    "snv": VariantClass.SNV,
    "snv hotspot": VariantClass.SNV,
    "snv, hotspot": VariantClass.SNV,
    "point mutation": VariantClass.SNV,
    "missense": VariantClass.SNV,
    "indel": VariantClass.INDEL,
    "insertion": VariantClass.INDEL,
    "deletion mutation": VariantClass.INDEL,
    "frameshift": VariantClass.INDEL,
    "fusion": VariantClass.FUSION,
    "rearrangement": VariantClass.FUSION,
    "gene fusion": VariantClass.FUSION,
    "amplification": VariantClass.AMPLIFICATION,
    "copy number amplification": VariantClass.AMPLIFICATION,
    "deletion": VariantClass.DELETION,
    "deep deletion": VariantClass.DELETION,
    "homozygous deletion": VariantClass.DELETION,
    "loss": VariantClass.DELETION,
    "cnv": VariantClass.CNV,
    "copy number": VariantClass.CNV,
    "splice": VariantClass.SPLICE,
    "splice variant": VariantClass.SPLICE,
    "splicing": VariantClass.SPLICE,
    "epigenetic": VariantClass.EPIGENETIC,
    "epigenetic silencing": VariantClass.EPIGENETIC,
    "methylation": VariantClass.EPIGENETIC,
    "promoter methylation": VariantClass.EPIGENETIC,
    "signature": VariantClass.SIGNATURE,
    "mutational signature": VariantClass.SIGNATURE,
    "composite biomarker": VariantClass.COMPOSITE,
    "composite": VariantClass.COMPOSITE,
    "expression": VariantClass.EXPRESSION,
    "overexpression": VariantClass.EXPRESSION,
    "germline": VariantClass.GERMLINE,
    "vus": VariantClass.VUS,
    "vus workflow": VariantClass.VUS,
    "variant of uncertain significance": VariantClass.VUS,
    "variant of unknown significance": VariantClass.VUS,
    "uncertain significance": VariantClass.VUS,
}


def _norm(text) -> str:
    """Lowercase, replace dashes and underscores with spaces, collapse whitespace."""
    s = str(text or "").lower()
    for ch in ("-", "_", "/"):
        s = s.replace(ch, " ")
    return " ".join(s.split())


def classify(raw: dict) -> VariantClass:
    """Classify one raw alteration record into a VariantClass.

    The function reads, in this order of trust:
      1. An explicit class field ("class", "cls", "variant_class", or "type"),
         matched against a canonical spelling table.
      2. The combined free text of gene, variant, consequence, and biomarker,
         scanned for keyword signatures (fusion, amplification, deletion, splice,
         epigenetic silencing, composite biomarker, expression, signature, VUS).

    VUS is detected first so an "uncertain significance" record is never mislabeled
    as a bare SNV. Composite genomic biomarkers (MSI-H, dMMR, TMB, HRD) are detected
    before single locus classes because they are genome wide features. When nothing
    specific matches, the default is SNV, the most common single locus class.

    Args:
        raw: a dict describing one alteration. Recognized keys include gene, variant,
            class or cls or variant_class or type, consequence, and biomarker.

    Returns:
        A VariantClass enum value.
    """
    explicit = raw.get("class") or raw.get("cls") or raw.get("variant_class") or raw.get("type") or ""
    ex = _norm(explicit)
    if ex:
        if ex in _EXPLICIT:
            return _EXPLICIT[ex]
        # Substring pass over explicit label, longest key first for specificity.
        for key in sorted(_EXPLICIT, key=len, reverse=True):
            if key in ex:
                return _EXPLICIT[key]

    gene = _norm(raw.get("gene"))
    variant = _norm(raw.get("variant"))
    consequence = _norm(raw.get("consequence"))
    biomarker = _norm(raw.get("biomarker"))
    text = " ".join([gene, variant, consequence, biomarker]).strip()

    # 1. VUS first: an uncertain significance flag overrides a bare hotspot read.
    if any(k in text for k in ("uncertain significance", "unknown significance", "vus")):
        return VariantClass.VUS

    # 2. Composite genomic biomarkers (genome wide features).
    if any(k in text for k in ("msi h", "msi high", "dmmr", "microsatellite instab",
                               "mismatch repair defic", "tmb high", "high tmb",
                               "tumor mutational burden", "hrd", "homologous recombination defic",
                               "loh", "composite")):
        return VariantClass.COMPOSITE

    # 3. Mutational signature.
    if "signature" in text or "sbs" in text or "apobec" in text:
        return VariantClass.SIGNATURE

    # 4. Epigenetic silencing (promoter methylation), before generic loss.
    if any(k in text for k in ("methylat", "epigenetic", "silenc", "hypermethyl")):
        return VariantClass.EPIGENETIC

    # 5. Fusion or rearrangement.
    if any(k in text for k in ("fusion", "rearrange", "translocation", "::", " fus ")):
        return VariantClass.FUSION

    # 6. Splice events (MET exon 14 skipping and other splice changes).
    if any(k in text for k in ("splice", "splicing", "skip", "exon 14")):
        return VariantClass.SPLICE

    # 7. Copy number: amplification then deletion, then generic CNV.
    if any(k in text for k in ("amplif", "amp ", " amp", "copy gain")):
        return VariantClass.AMPLIFICATION
    if any(k in text for k in ("deep deletion", "homozygous deletion", "biallelic loss",
                               "loss of", "loss ", "deletion", "deleted")):
        # Distinguish a coding indel deletion from a copy number deletion by wording.
        if any(k in text for k in ("frameshift", "inframe", "c.", "p.", "indel")):
            return VariantClass.INDEL
        return VariantClass.DELETION
    if "copy number" in text or "cnv" in text:
        return VariantClass.CNV

    # 8. Expression (protein or RNA level readout, no sequence change).
    if any(k in text for k in ("overexpress", "expression", "protein level", "ihc positive",
                               "positive by ihc", "upregulat")):
        return VariantClass.EXPRESSION

    # 9. Germline.
    if "germline" in text:
        return VariantClass.GERMLINE

    # 10. Indel by wording.
    if any(k in text for k in ("frameshift", "insertion", "duplication", "indel", "del ins", "delins")):
        return VariantClass.INDEL

    # 11. Default: single nucleotide variant (the common hotspot case).
    return VariantClass.SNV
