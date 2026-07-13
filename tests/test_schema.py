"""Schema contract tests: the rich model maps to the report DATA dict and the
no-dash guard works. Runs fully offline."""
import pytest
from anveshar.schema import (
    DiseaseReport, Therapy, Tier, Modality, DiscoveryHypothesis, Citation,
    PatientProfile, Alteration, VariantClass, Actionability, Target, assert_no_dashes,
)


def sample_report():
    return DiseaseReport(
        name="Renal medullary carcinoma",
        sub="A SMARCB1 deficient rare kidney cancer.",
        chips=["SMARCB1 loss", "sickle cell trait", "aggressive"],
        overview={"patient": "<p>x</p>", "clinician": "<p>y</p>", "researcher": "<p>z</p>"},
        targets=[Target("SMARCB1 loss", "RMC", "loss of INI1 by IHC")],
        therapies=[Therapy(
            drug="Bortezomib", target="Proteasome", tier=Tier.T2,
            modality=Modality.SMALL_MOLECULE, approved_in="multiple myeloma",
            rationale={"patient": "a", "clinician": "b", "researcher": "c"},
            citation=Citation("Carden 2017", "https://pubmed.ncbi.nlm.nih.gov/28052556/"))],
        discovery=[DiscoveryHypothesis(
            hypothesis="Test EZH2 inhibition in SMARCB1 null RMC",
            shared_dependency="SWI/SNF loss creates a PRC2/EZH2 dependency",
            source_condition="epithelioid sarcoma",
            proposed_modality=Modality.SMALL_MOLECULE,
            transferability="medium, shared INI1 loss but negative RMC cohort",
            supporting_citation=Citation("Gounder 2020", "https://pubmed.ncbi.nlm.nih.gov/33035459/"),
            testable_prediction="EZH2 inhibition reduces viability in SMARCB1 null RMC organoids")],
        disclaimer="Decision support, not medical advice.")


def test_render_dict_shape():
    d = sample_report().to_render_dict()
    assert d["cancer"]["name"].startswith("Renal")
    assert d["therapies"][0]["tier"] == 2                    # Tier enum to int
    assert d["therapies"][0]["modality"] == "small molecule"  # modality string
    assert d["discovery"][0]["prediction"]                   # discovery carries a prediction
    assert len(d["discovery"]) == 1
    assert d["discovery"][0]["citation"]["url"].startswith("https://")


def test_patient_render_and_matching_fields():
    r = sample_report()
    r.patient = PatientProfile(
        present=True,
        source=Citation("case", "https://pubmed.ncbi.nlm.nih.gov/27048246/"),
        tumor_summary="high grade rectal NEC",
        alterations=[Alteration(gene="BRAF", variant_class=VariantClass.SNV, variant="V600E",
                                target="BRAF V600E", actionability=Actionability(oncokb_level="Level 1"))],
        excluded=[{"target": "MSI-H / dMMR", "reason": "microsatellite stable"}],
        summary={"patient": "a", "clinician": "b", "researcher": "c"})
    d = r.to_render_dict()
    assert d["patient"]["present"] is True
    assert d["patient"]["alterations"][0]["target"] == "BRAF V600E"
    assert "OncoKB Level 1" in d["patient"]["alterations"][0]["actionability"]
    assert d["patient"]["excluded"][0]["reason"] == "microsatellite stable"


def test_no_dash_guard():
    assert_no_dashes({"a": "clean comma, separated text"})
    with pytest.raises(ValueError):
        assert_no_dashes({"a": "bad — em dash"})
    with pytest.raises(ValueError):
        assert_no_dashes({"a": "bad – en dash"})


def test_full_report_has_no_dashes():
    assert_no_dashes(sample_report().to_render_dict())
