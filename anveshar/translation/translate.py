"""Cross-condition therapy translation for Anveshar.

Given a list of molecular targets (or biomarkers) present in a condition, map
each to therapies validated elsewhere, tiered and cited:

    Tier 1  a tissue-agnostic FDA approval keyed on the biomarker;
    Tier 2  a drug approved in another tumor that carries the same target;
    Tier 3  mechanistic or preclinical rationale only.

Every therapy carries a real citation (PubMed PMID). Nothing is invented: a
target with no cited option produces no Tier 2 or Tier 3 therapy. The
same-target-other-tumor map below is small and hand-curated; extend it only
with a verified PMID.
"""
from __future__ import annotations

import re

from ..schema import Therapy, Tier, Modality, Citation, DiseaseReport, PatientProfile
from . import tissue_agnostic


def _norm(text: str) -> str:
    """Lowercase and strip non-alphanumerics for tolerant target matching."""
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


# Same-target-other-tumor options: a target present in the condition mapped to a
# therapy already validated against that target (or that biology) in a DIFFERENT
# tumor. Each option is Tier 2 (approved or positive prospective elsewhere) or
# Tier 3 (mechanistic). Every entry cites a real, verified PubMed PMID.
_TARGET_MAP: dict[str, list[dict]] = {
    "dll3": [
        {
            "drug": "tarlatamab",
            "tier": Tier.T2,
            "modality": Modality.BISPECIFIC,
            "approved_in": "small cell lung cancer (DLL3 x CD3 bispecific T cell engager)",
            "dev_stage": "FDA approved 2024 in previously treated small cell lung cancer",
            "rationale": "DLL3 is a Notch ligand expressed on the cell surface of high grade neuroendocrine tumors; tarlatamab redirects T cells to DLL3 and produced durable responses in small cell lung cancer, so a DLL3-positive condition shares the actionable surface target.",
            "citation": Citation(
                label="Ahn et al., N Engl J Med 2023, tarlatamab DeLLphi-301 (PMID 37861218)",
                url="https://pubmed.ncbi.nlm.nih.gov/37861218/",
            ),
        }
    ],
    # High grade neuroendocrine biology (a lineage biomarker rather than a single
    # protein): platinum-etoposide is the cross-condition standard borrowed from
    # high grade neuroendocrine carcinoma / small cell lung cancer.
    "neuroendocrinehighgrade": [
        {
            "drug": "platinum plus etoposide",
            "tier": Tier.T2,
            "modality": Modality.CHEMO,
            "approved_in": "high grade (WHO G3) gastroenteropancreatic neuroendocrine carcinoma and small cell lung cancer",
            "dev_stage": "established standard of care for high grade neuroendocrine carcinoma",
            "rationale": "Platinum-etoposide is the cross-lineage backbone for poorly differentiated high grade neuroendocrine carcinoma; the NORDIC NEC study established it as the reference first line regimen for WHO G3 disease irrespective of primary site.",
            "citation": Citation(
                label="Sorbye et al., Ann Oncol 2013, NORDIC NEC study (PMID 22967994)",
                url="https://pubmed.ncbi.nlm.nih.gov/22967994/",
            ),
        }
    ],
    "sstr2": [
        {
            "drug": "lutetium Lu 177 dotatate",
            "tier": Tier.T2,
            "modality": Modality.RADIOLIGAND,
            "approved_in": "somatostatin receptor positive gastroenteropancreatic neuroendocrine tumors",
            "dev_stage": "FDA approved 2018 (radioligand therapy)",
            "rationale": "SSTR2 surface expression is the target of Lu-177 DOTATATE peptide receptor radionuclide therapy, which improved progression free survival in the NETTER-1 trial; SSTR2-positive tumors of other lineages share the target.",
            "citation": Citation(
                label="Strosberg et al., N Engl J Med 2017, NETTER-1 (PMID 28076709)",
                url="https://pubmed.ncbi.nlm.nih.gov/28076709/",
            ),
        }
    ],
}

# Biomarker aliases so target strings resolve to _TARGET_MAP keys.
_TARGET_ALIASES = {
    "delta like ligand 3": "dll3",
    "sstr": "sstr2",
    "somatostatin receptor 2": "sstr2",
    "somatostatin receptor": "sstr2",
    "high grade neuroendocrine": "neuroendocrinehighgrade",
    "neuroendocrine carcinoma": "neuroendocrinehighgrade",
}


def _map_key(target: str) -> str | None:
    """Resolve a free-text target to a canonical ``_TARGET_MAP`` key, or None."""
    key = _norm(target)
    if key in _TARGET_MAP:
        return key
    for alias, canonical in _TARGET_ALIASES.items():
        if _norm(alias) == key or _norm(alias) in key:
            return canonical
    return None


def _therapy_from_map(target: str, rec: dict) -> Therapy:
    """Build a ``Therapy`` from a same-target-other-tumor map record."""
    return Therapy(
        drug=rec["drug"],
        target=target,
        tier=rec["tier"],
        modality=rec["modality"],
        approved_in=rec["approved_in"],
        dev_stage=rec["dev_stage"],
        rationale={"clinician": rec["rationale"]},
        citation=rec["citation"],
    )


def translate_targets(targets: list[str], condition: str = "") -> list[Therapy]:
    """Map molecular targets to therapies validated in other conditions, tiered.

    For each target the function first tries the tissue-agnostic table
    (Tier 1); if the target is also a biomarker with a tumor-agnostic approval
    it is surfaced as a Tier 1 ``Therapy``. It then adds any same-target-other-
    tumor options from the curated map (Tier 2 or Tier 3). Results are ordered
    by ascending tier value so the strongest evidence appears first. Targets
    with no cited option contribute nothing (no fabricated match).

    Args:
        targets: Free-text target or biomarker strings, for example
            ``["BRAF V600E", "DLL3", "SSTR2"]``.
        condition: Optional name of the target condition, used only for
            provenance in the therapy rationale; it never invents evidence.

    Returns:
        A list of cited ``Therapy`` objects sorted by tier (Tier 1 first).
    """
    therapies: list[Therapy] = []
    seen: set[tuple[str, str]] = set()

    for target in targets:
        # Tier 1: a tissue-agnostic approval keyed on this biomarker.
        t1 = tissue_agnostic.for_biomarker(target)
        if t1 is not None:
            keyid = (_norm(t1.drug), _norm(t1.target))
            if keyid not in seen:
                if condition:
                    t1.rationale.setdefault(
                        "researcher",
                        f"Applies to {condition} only if {target} is documented in this tumor.",
                    )
                therapies.append(t1)
                seen.add(keyid)

        # Tier 2 / Tier 3: same target validated in another tumor.
        mkey = _map_key(target)
        if mkey:
            for rec in _TARGET_MAP[mkey]:
                th = _therapy_from_map(target, rec)
                keyid = (_norm(th.drug), _norm(th.target))
                if keyid not in seen:
                    therapies.append(th)
                    seen.add(keyid)

    therapies.sort(key=lambda t: int(t.tier.value))
    return therapies


def match(report: DiseaseReport, profile: PatientProfile) -> dict:
    """Match a patient profile against a report's therapies by shared target.

    Compares the canonical ``target`` of each alteration in ``profile`` to the
    ``target`` of each therapy in ``report`` (tolerant, substring-aware
    matching). A therapy whose target is present in the profile is reported as
    matched; a profile alteration whose target has no therapy in the report, or
    that the profile itself already excluded, is reported as excluded with a
    reason. Nothing is invented: unmatched profile targets are simply not
    matched.

    Args:
        report: The condition's ``DiseaseReport`` (its ``therapies`` list is the
            candidate pool).
        profile: The patient's ``PatientProfile`` (its ``alterations`` supply the
            present targets; its ``excluded`` list is carried through).

    Returns:
        ``{"matched": [drug names], "excluded": [{"target", "reason"}]}``.
    """
    present = []
    for alt in profile.alterations:
        for token in (alt.target, alt.biomarker, alt.gene):
            if token:
                present.append(_norm(token))

    matched: list[str] = []
    matched_targets: set[str] = set()
    for th in report.therapies:
        th_key = _norm(th.target)
        if not th_key:
            continue
        hit = any(th_key == p or (p and (p in th_key or th_key in p)) for p in present)
        if hit and th.drug not in matched:
            matched.append(th.drug)
            matched_targets.add(th_key)

    # Carry through explicit profile exclusions, then flag present targets with no therapy.
    excluded: list[dict] = list(profile.excluded)
    excluded_keys = {_norm(e.get("target", "")) for e in excluded}
    report_target_keys = {_norm(th.target) for th in report.therapies if th.target}
    for alt in profile.alterations:
        akey = _norm(alt.target or alt.biomarker or alt.gene)
        if not akey:
            continue
        covered = any(akey == r or akey in r or r in akey for r in report_target_keys)
        if not covered and akey not in excluded_keys:
            excluded.append(
                {
                    "target": alt.target or alt.biomarker or alt.gene,
                    "reason": "no therapy in this report currently targets this alteration",
                }
            )
            excluded_keys.add(akey)

    return {"matched": matched, "excluded": excluded}
