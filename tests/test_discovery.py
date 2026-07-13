"""Offline tests for the anveshar.translation.discovery novelty layer (no network)."""
from anveshar.schema import (
    DiseaseReport, Target, PatientProfile, Alteration, VariantClass, Modality,
    DiscoveryHypothesis,
)
from anveshar.translation import generate


def _smarcb1_report():
    """A minimal report whose biology names the SMARCB1 / SWI-SNF dependency."""
    return DiseaseReport(
        name="Renal Medullary Carcinoma",
        sub="SMARCB1 (INI1) deficient SWI/SNF rhabdoid family",
        targets=[
            Target(
                name="SMARCB1 (INI1) loss to EZH2 dependency",
                present_in="Universal (defining lesion)",
                evidence="SWI/SNF loss to PRC2 imbalance in the rhabdoid family",
            )
        ],
    )


def test_generate_smarcb1_yields_valid_hypotheses():
    """generate on a SMARCB1 report yields at least one DiscoveryHypothesis.

    Every hypothesis must carry a Modality proposed_modality, a real https
    supporting citation, and a non-empty testable_prediction.
    """
    report = _smarcb1_report()
    profile = PatientProfile(
        alterations=[
            Alteration(gene="SMARCB1", variant_class=VariantClass.DELETION,
                       target="SMARCB1 loss", biomarker="SMARCB1/INI1 loss")
        ]
    )
    hyps = generate(report, profile)
    assert len(hyps) >= 1
    for h in hyps:
        assert isinstance(h, DiscoveryHypothesis)
        assert isinstance(h.proposed_modality, Modality)
        assert h.supporting_citation.url.startswith("https://")
        assert h.testable_prediction, "every hypothesis must have a testable prediction"
        assert h.shared_dependency
        assert h.source_condition
        assert h.transferability
        # framed as a research hypothesis, never a clinical recommendation
        assert "not a clinical recommendation" in h.hypothesis.lower()


def test_generate_smarcb1_covers_ezh2_and_synthetic_lethality():
    """The SMARCB1 trigger produces both the EZH2 analogy and a synthetic lethal (PRMT5) analogy."""
    hyps = generate(_smarcb1_report())
    deps = " ".join(h.shared_dependency.lower() for h in hyps)
    assert "ezh2" in deps
    assert "prmt5" in deps
    # the tazemetostat / epithelioid sarcoma analogy citation must be present and real
    urls = {h.supporting_citation.url for h in hyps}
    assert "https://pubmed.ncbi.nlm.nih.gov/33035459/" in urls


def test_generate_advanced_modalities_present():
    """Discovery spans advanced modalities: DLL3 cell therapy, SSTR2 radioligand, splice ASO, gene therapy."""
    report = DiseaseReport(
        name="High grade neuroendocrine tumor",
        sub="DLL3 and SSTR2 positive",
        targets=[
            Target(name="DLL3 surface expression"),
            Target(name="SSTR2 surface expression"),
        ],
    )
    profile = PatientProfile(
        alterations=[
            Alteration(gene="RB1", variant_class=VariantClass.DELETION, target="RB1 loss"),
            Alteration(gene="MET", variant_class=VariantClass.SPLICE, target="MET exon 14 skipping",
                       consequence="splice"),
        ]
    )
    hyps = generate(report, profile)
    modalities = {h.proposed_modality for h in hyps}
    assert Modality.CELL_THERAPY in modalities      # DLL3
    assert Modality.RADIOLIGAND in modalities       # SSTR2
    assert Modality.ASO in modalities               # splice lesion
    assert Modality.GENE_THERAPY in modalities      # tumor suppressor loss
    for h in hyps:
        assert h.testable_prediction
        assert h.supporting_citation.url.startswith("https://")


def test_generate_empty_when_no_dependency():
    """No licensed dependency yields no hypotheses (Anveshar does not hallucinate a target)."""
    report = DiseaseReport(name="Bland condition", targets=[Target(name="no actionable biology")])
    assert generate(report, None) == []
