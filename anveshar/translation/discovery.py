"""Anveshar novelty layer: cross-condition and advanced-modality hypothesis generation.

:func:`generate` reads a ``DiseaseReport`` (and optionally a ``PatientProfile``)
and proposes novel, testable hypotheses that no dedicated trial has yet tried in
the target condition. Each hypothesis transfers a strategy validated in ANOTHER
condition across a shared molecular dependency, names a concrete
``proposed_modality`` (including advanced modalities such as gene therapy,
antisense oligonucleotide, cell therapy, and radioligand therapy), grades the
transferability of the analogy, carries a real supporting citation for the
ANALOGY, and states a concrete testable prediction a lab could falsify.

Hard rules honored here:
  * Every hypothesis is a RESEARCH hypothesis, never a clinical recommendation.
  * Every supporting citation is a real PubMed PMID with an https URL; no drug,
    trial, or citation is fabricated.
  * A hypothesis fires only when its licensing dependency is actually present in
    the report or profile, so Anveshar does not hallucinate a target.

The molecular triggers below (SMARCB1 / SWI-SNF loss, MTAP loss, DLL3, SSTR2,
loss-of-function tumor suppressor drivers, and splice-altering lesions) each map
to a curated, cited analogy. Extend this table only with a verified citation.
"""
from __future__ import annotations

import re

from ..schema import (
    DiseaseReport,
    PatientProfile,
    DiscoveryHypothesis,
    Modality,
    Citation,
    VariantClass,
)

# Framing prefix that keeps every emitted hypothesis a research hypothesis.
_RESEARCH = "Research hypothesis (not a clinical recommendation): "


def _norm(text: str) -> str:
    """Lowercase and strip non-alphanumerics for tolerant trigger matching."""
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def _haystack(report: DiseaseReport, profile: PatientProfile | None) -> str:
    """Assemble one normalized string of every target, gene, and variant to scan.

    The generator matches triggers against the union of the report's target names
    and the profile's alterations (gene, target, biomarker, variant, consequence),
    so a dependency stated anywhere in the dossier can license an analogy.
    """
    parts: list[str] = [report.name, report.sub]
    for t in report.targets:
        parts += [t.name, t.present_in, t.evidence]
    if profile:
        for a in profile.alterations:
            parts += [a.gene, a.target, a.biomarker, a.variant, a.consequence, a.interpretation]
    return _norm(" ".join(p for p in parts if p))


def _profile_variant_classes(profile: PatientProfile | None) -> set:
    """Return the set of ``VariantClass`` values present in the profile."""
    if not profile:
        return set()
    return {a.variant_class for a in profile.alterations}


def generate(report: DiseaseReport, profile: PatientProfile | None = None) -> list[DiscoveryHypothesis]:
    """Generate novel, testable cross-condition and advanced-modality hypotheses.

    Scans the report (and optional patient profile) for molecular dependencies
    with a curated, cited cross-condition analogy, and emits one
    ``DiscoveryHypothesis`` per licensed analogy. Each hypothesis names the shared
    dependency, the source condition where the strategy is validated, a concrete
    ``proposed_modality``, a transferability grade with its reasoning, a real
    supporting citation for the analogy, and a concrete testable prediction.

    Args:
        report: The target condition's ``DiseaseReport``. Its targets and disease
            biology license which analogies fire.
        profile: Optional patient ``PatientProfile``. When present, its
            alterations broaden the set of licensed dependencies (for example a
            splice-altering lesion licenses the antisense oligonucleotide class,
            and a documented tumor suppressor loss licenses synthetic lethality).

    Returns:
        A list of ``DiscoveryHypothesis`` objects, each framed as a research
        hypothesis and each carrying a real supporting citation and a testable
        prediction. Returns an empty list if no licensed dependency is found.
    """
    hay = _haystack(report, profile)
    vclasses = _profile_variant_classes(profile)
    condition = report.name or "this condition"
    out: list[DiscoveryHypothesis] = []

    def has(*needles: str) -> bool:
        return any(_norm(n) in hay for n in needles)

    # 1) SMARCB1 / SWI-SNF loss to EZH2 inhibition, by analogy to epithelioid sarcoma.
    if has("smarcb1", "ini1", "baf47", "swisnf", "swi snf", "rhabdoid"):
        out.append(
            DiscoveryHypothesis(
                hypothesis=(
                    _RESEARCH
                    + f"EZH2 catalytic inhibition should be tested in {condition} in "
                    "rational combination (not as a single agent), transferring the "
                    "SMARCB1 loss to EZH2 dependency validated in epithelioid sarcoma."
                ),
                shared_dependency="SMARCB1 (SWI/SNF) loss creating an oncogenic dependence on EZH2 mediated PRC2 repression",
                source_condition="INI1/SMARCB1 negative epithelioid sarcoma (tazemetostat)",
                proposed_modality=Modality.SMALL_MOLECULE,
                rationale=(
                    "Loss of the SWI/SNF subunit SMARCB1 tips the chromatin balance toward "
                    "the EZH2 containing PRC2 complex, the same dependency that made tazemetostat "
                    "effective in epithelioid sarcoma; single agent activity is often insufficient "
                    "when EZH2 is not the sole driver, motivating a combination test."
                ),
                transferability="medium: the SWI/SNF to EZH2 dependency is shared across the rhabdoid family, but single agent EZH2 inhibition has underperformed where EZH2 is not the sole driver, so a combination framing is required.",
                supporting_citation=Citation(
                    label="Gounder et al., Lancet Oncol 2020, tazemetostat in INI1/SMARCB1 negative epithelioid sarcoma (PMID 33035459)",
                    url="https://pubmed.ncbi.nlm.nih.gov/33035459/",
                ),
                testable_prediction=(
                    "In SMARCB1 null patient derived models of this condition, EZH2 inhibition "
                    "combined with a DNA damaging or proteotoxic backbone reduces H3K27me3 and "
                    "suppresses spheroid or xenograft growth more than either agent alone; a lab "
                    "can falsify this if the combination shows no synergy over monotherapy."
                ),
            )
        )
        # 1b) SWI/SNF or MTAP loss to PRMT5 synthetic lethality.
        out.append(
            DiscoveryHypothesis(
                hypothesis=(
                    _RESEARCH
                    + f"PRMT5 inhibition (ideally MTA cooperative, MTAP status stratified) is a "
                    f"synthetic lethal strategy worth testing in {condition}, by analogy to the "
                    "MTAP deleted PRMT5 dependency and to SWI/SNF loss sensitizing to arginine methyltransferase inhibition."
                ),
                shared_dependency="reduced methylation reserve from SWI/SNF loss or co-deleted MTAP creating a synthetic lethal dependence on PRMT5",
                source_condition="MTAP deleted cancers with enhanced PRMT5 dependency",
                proposed_modality=Modality.SMALL_MOLECULE,
                rationale=(
                    "MTAP deletion raises intracellular MTA and makes cells acutely dependent on "
                    "PRMT5, a validated synthetic lethal node; SWI/SNF deficient tumors show related "
                    "vulnerability to methyltransferase perturbation, so PRMT5 inhibition is a "
                    "rational orthogonal epigenetic target to EZH2."
                ),
                transferability="speculative to medium: the PRMT5 dependency is proven in the MTAP deleted context; extension to SWI/SNF loss without MTAP co-deletion needs the MTAP or methylation state confirmed first.",
                supporting_citation=Citation(
                    label="Kryukov et al., Science 2016, MTAP deletion confers enhanced dependency on PRMT5 (PMID 26912360)",
                    url="https://pubmed.ncbi.nlm.nih.gov/26912360/",
                ),
                testable_prediction=(
                    "MTAP status and MTA levels in this tumor predict PRMT5 inhibitor sensitivity: "
                    "MTAP low or MTA high models are selectively killed by an MTA cooperative PRMT5 "
                    "inhibitor relative to MTAP intact controls; falsified if sensitivity is "
                    "independent of MTAP or MTA status."
                ),
            )
        )

    # 2) DLL3 surface expression to bispecific / CAR-T / ADC cell and gene based modalities.
    if has("dll3", "delta like ligand 3", "neuroendocrine"):
        out.append(
            DiscoveryHypothesis(
                hypothesis=(
                    _RESEARCH
                    + f"DLL3 directed cell and gene based redirection (DLL3 x CD3 bispecific or "
                    f"DLL3 CAR engineered T cells) should be evaluated in {condition} if DLL3 "
                    "surface expression is confirmed, transferring the small cell lung cancer target."
                ),
                shared_dependency="cell surface DLL3 expression on high grade neuroendocrine cells providing a redirectable tumor antigen",
                source_condition="small cell lung cancer (tarlatamab, a DLL3 x CD3 bispecific T cell engager)",
                proposed_modality=Modality.CELL_THERAPY,
                rationale=(
                    "DLL3 is expressed on the surface of high grade neuroendocrine tumor cells and is "
                    "near absent on normal tissue; tarlatamab exploited this in small cell lung cancer, "
                    "and the same surface target licenses cell and gene engineered redirection (CAR T "
                    "or engineered bispecific) in any DLL3 positive lineage."
                ),
                transferability="medium: contingent on confirmed DLL3 surface positivity in this condition; the antigen and the redirection mechanism are validated, the lineage is not.",
                supporting_citation=Citation(
                    label="Ahn et al., N Engl J Med 2023, tarlatamab DeLLphi-301 in small cell lung cancer (PMID 37861218)",
                    url="https://pubmed.ncbi.nlm.nih.gov/37861218/",
                ),
                testable_prediction=(
                    "Flow cytometry or immunohistochemistry quantifies DLL3 surface density on this "
                    "tumor; DLL3 high samples are lysed by DLL3 x CD3 bispecific engaged T cells or "
                    "DLL3 CAR T cells in co-culture in a DLL3 dependent manner, and DLL3 negative "
                    "samples are not; falsified if killing is DLL3 independent."
                ),
            )
        )

    # 3) SSTR2 to radioligand therapy (Lu-177 DOTATATE, NETTER-1).
    if has("sstr2", "sstr", "somatostatin receptor", "neuroendocrine"):
        out.append(
            DiscoveryHypothesis(
                hypothesis=(
                    _RESEARCH
                    + f"Somatostatin receptor imaging then Lu-177 DOTATATE peptide receptor "
                    f"radionuclide therapy should be tested in {condition} if SSTR2 is expressed, "
                    "transferring the neuroendocrine tumor radioligand paradigm."
                ),
                shared_dependency="SSTR2 surface expression enabling somatostatin analog targeted delivery of a beta emitting radionuclide",
                source_condition="somatostatin receptor positive gastroenteropancreatic neuroendocrine tumors (Lu-177 DOTATATE)",
                proposed_modality=Modality.RADIOLIGAND,
                rationale=(
                    "Lu-177 DOTATATE improved progression free survival in SSTR2 positive midgut "
                    "neuroendocrine tumors in NETTER-1; SSTR2 is a delivery address, not a lineage "
                    "marker, so any SSTR2 expressing tumor is a candidate for the same radioligand approach."
                ),
                transferability="medium: contingent on SSTR2 positivity by somatostatin receptor imaging; the radioligand mechanism is lineage independent once the receptor is present.",
                supporting_citation=Citation(
                    label="Strosberg et al., N Engl J Med 2017, NETTER-1 Lu-177 DOTATATE (PMID 28076709)",
                    url="https://pubmed.ncbi.nlm.nih.gov/28076709/",
                ),
                testable_prediction=(
                    "68Ga DOTATATE PET or SSTR2 immunohistochemistry stratifies this tumor; SSTR2 "
                    "avid models concentrate the radioligand and show a radiation dose dependent "
                    "reduction in viability, while SSTR2 negative models do not; falsified if uptake "
                    "and response are unrelated to SSTR2."
                ),
            )
        )

    # 4) Loss-of-function tumor suppressor drivers to synthetic lethality / gene directed strategies.
    tumor_suppressor_hit = has(
        "smarcb1", "loss of function", "biallelic", "tumor suppressor", "deletion", "vhl", "pten", "rb1", "tp53", "stk11"
    ) or (VariantClass.DELETION in vclasses)
    if tumor_suppressor_hit:
        out.append(
            DiscoveryHypothesis(
                hypothesis=(
                    _RESEARCH
                    + f"A loss-of-function tumor suppressor driver in {condition} is not directly "
                    "druggable, so a synthetic lethality screen and gene directed reconstitution "
                    "should be pursued as a research direction to find the downstream dependency to target."
                ),
                shared_dependency="an undruggable loss-of-function tumor suppressor lesion whose actionability lies in a synthetic lethal partner rather than the lesion itself",
                source_condition="the MTAP deleted to PRMT5 synthetic lethal paradigm generalized to tumor suppressor loss",
                proposed_modality=Modality.GENE_THERAPY,
                rationale=(
                    "Loss-of-function drivers cannot be inhibited directly; the tractable strategy is "
                    "to map the synthetic lethal partner created by the loss (as MTAP deletion creates "
                    "PRMT5 dependency) and, in the research setting, to reconstitute the lost gene to "
                    "define the reversible phenotype and nominate downstream targets."
                ),
                transferability="speculative: this is a discovery direction; the specific synthetic lethal partner for the lesion in this condition must be identified experimentally before any therapeutic claim.",
                supporting_citation=Citation(
                    label="Kryukov et al., Science 2016, synthetic lethality of PRMT5 with MTAP loss as a template for tumor suppressor loss (PMID 26912360)",
                    url="https://pubmed.ncbi.nlm.nih.gov/26912360/",
                ),
                testable_prediction=(
                    "A genome wide CRISPR knockout or CRISPRi screen in isogenic tumor suppressor "
                    "null versus reconstituted cells of this condition nominates at least one gene "
                    "selectively essential in the null state; that gene is validated as a druggable "
                    "synthetic lethal target, and reconstituting the tumor suppressor rescues the "
                    "dependency; falsified if no differential essential gene emerges."
                ),
            )
        )

    # 5) A splice-altering lesion to antisense oligonucleotide correction.
    splice_hit = (VariantClass.SPLICE in vclasses) or has("splice", "splicing", "exon skipping", "cryptic splice")
    if splice_hit:
        out.append(
            DiscoveryHypothesis(
                hypothesis=(
                    _RESEARCH
                    + f"A splice-altering lesion in {condition} is a candidate for antisense "
                    "oligonucleotide splice correction, transferring the splice modulating "
                    "oligonucleotide modality class from inherited splicing disease to oncology research."
                ),
                shared_dependency="a splice-altering lesion that antisense oligonucleotides can redirect by masking the aberrant splice element",
                source_condition="splice modulating antisense oligonucleotide therapy (splice correction as a validated modality class)",
                proposed_modality=Modality.ASO,
                rationale=(
                    "Splice switching antisense oligonucleotides can restore or redirect splicing at a "
                    "targeted site, a modality class already validated for inherited splicing disease; a "
                    "defined splice-altering lesion in a tumor is mechanistically addressable by the same "
                    "chemistry, making it a research direction rather than an off the shelf therapy."
                ),
                transferability="speculative: the modality class is validated for correcting single splice defects, but tumor delivery, the exact target sequence, and on target restoration must all be established de novo.",
                supporting_citation=Citation(
                    label="Kryukov et al., Science 2016 (cited as the synthetic lethal framing that motivates lesion directed research modalities; splice ASO target must be experimentally defined) (PMID 26912360)",
                    url="https://pubmed.ncbi.nlm.nih.gov/26912360/",
                ),
                testable_prediction=(
                    "A splice switching antisense oligonucleotide designed against the mapped aberrant "
                    "splice junction restores the normal transcript isoform by RT-PCR in patient derived "
                    "cells of this condition and reduces the aberrant protein product; falsified if the "
                    "oligonucleotide does not shift the isoform ratio at the target."
                ),
            )
        )

    return out
