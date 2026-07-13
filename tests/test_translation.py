"""Offline tests for anveshar.translation (no network)."""
from anveshar.schema import (
    Tier, Modality, DiseaseReport, Therapy, PatientProfile, Alteration, VariantClass,
)
from anveshar.translation import (
    PRECEDENTS, for_biomarker, translate_targets, match,
)


def test_precedents_loads_and_nonempty():
    """PRECEDENTS loads from the JSON table and is a non-empty list of cited Precedents."""
    assert isinstance(PRECEDENTS, list)
    assert len(PRECEDENTS) >= 8
    for p in PRECEDENTS:
        assert p.biomarker and p.drug
        assert p.citation.url.startswith("https://")
        assert "pmid" not in p.citation.url.lower() or "pubmed" in p.citation.url.lower()


def test_for_biomarker_msih_returns_pembrolizumab():
    """for_biomarker('MSI-H') returns the tissue-agnostic pembrolizumab Tier 1 therapy."""
    th = for_biomarker("MSI-H")
    assert th is not None
    assert th.drug == "pembrolizumab"
    assert th.tier == Tier.T1
    assert th.citation.url.startswith("https://")


def test_for_biomarker_aliases_and_misses():
    """Aliases resolve (dMMR to pembrolizumab); unknown biomarkers return None, never a guess."""
    assert for_biomarker("dMMR").drug == "pembrolizumab"
    assert for_biomarker("BRAF V600E").drug == "dabrafenib plus trametinib"
    assert for_biomarker("HER2 IHC 3+").drug == "trastuzumab deruxtecan"
    assert for_biomarker("not a real biomarker") is None
    assert for_biomarker("") is None


def test_translate_targets_tiered():
    """translate_targets(['BRAF V600E','DLL3']) returns tiered, cited therapies (Tier 1 first)."""
    ths = translate_targets(["BRAF V600E", "DLL3"])
    assert ths, "expected at least one therapy"
    drugs = {t.drug for t in ths}
    assert "dabrafenib plus trametinib" in drugs   # Tier 1 tissue-agnostic
    assert "tarlatamab" in drugs                    # Tier 2 same-target-other-tumor (DLL3)
    tiers = [int(t.tier.value) for t in ths]
    assert tiers == sorted(tiers), "therapies must be ordered by ascending tier"
    for t in ths:
        assert t.citation.url.startswith("https://")


def test_translate_targets_no_fabrication():
    """A target with no cited option yields no therapy (no fabricated match)."""
    assert translate_targets(["ZZZ nonexistent target"]) == []


def test_match_matched_and_excluded():
    """match compares profile targets to report therapies, returning matched and excluded."""
    report = DiseaseReport(
        name="Test condition",
        therapies=[
            Therapy(drug="tarlatamab", target="DLL3", tier=Tier.T2, modality=Modality.BISPECIFIC),
            Therapy(drug="pembrolizumab", target="MSI-H / dMMR", tier=Tier.T1,
                    modality=Modality.IMMUNE_CHECKPOINT),
        ],
    )
    profile = PatientProfile(
        alterations=[
            Alteration(gene="DLL3", variant_class=VariantClass.EXPRESSION, target="DLL3"),
            Alteration(gene="SMARCB1", variant_class=VariantClass.DELETION, target="SMARCB1 loss"),
        ],
    )
    res = match(report, profile)
    assert "tarlatamab" in res["matched"]
    assert "pembrolizumab" not in res["matched"]
    excluded_targets = {e["target"] for e in res["excluded"]}
    assert "SMARCB1 loss" in excluded_targets
