"""Renderer tests: a DATA dict injects into the template, discovery renders, no dashes leak."""
import os
import tempfile
from anveshar.report import render


def _sample_data():
    return {
        "cancer": {"name": "Renal medullary carcinoma", "sub": "test", "chips": ["a", "b"]},
        "overview": {"patient": "<p>x</p>", "clinician": "<p>y</p>", "researcher": "<p>z</p>"},
        "targets": [{"name": "SMARCB1 loss", "present_in": "RMC", "evidence": "IHC"}],
        "therapies": [{"drug": "Bortezomib", "target": "Proteasome", "tier": 2,
                       "modality": "small molecule", "approved_in": "myeloma", "dev_stage": "",
                       "rationale": {"patient": "a", "clinician": "b", "researcher": "c"},
                       "citation": {"label": "Carden 2017", "url": "PMID:28052556"}}],
        "trials": [],
        "precedents": [],
        "discovery": [{"hypothesis": "Test EZH2 inhibition", "shared": "SWI/SNF loss",
                       "source": "epithelioid sarcoma", "modality": "small molecule",
                       "transferability": "medium", "prediction": "reduces viability in organoids",
                       "citation": {"label": "Gounder 2020", "url": "PMID:33035459"}}],
        "disclaimer": "Decision support, not medical advice.",
    }


def test_render_data_writes_html():
    data = _sample_data()
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "report.html")
        render.render_data(data, out)
        html = open(out, encoding="utf-8").read()
    assert "Bortezomib" in html
    assert "Test EZH2 inhibition" in html
    assert "—" not in html and "–" not in html
    # citation shorthand expanded to a real URL
    assert "https://pubmed.ncbi.nlm.nih.gov/33035459/" in html


def test_render_report_from_object():
    from anveshar.schema import DiseaseReport, Therapy, Tier, Modality, Citation
    rep = DiseaseReport(
        name="Test cancer", disclaimer="x",
        overview={"patient": "a", "clinician": "b", "researcher": "c"},
        therapies=[Therapy(drug="DrugX", target="TargetY", tier=Tier.T1, modality=Modality.GENE_THERAPY,
                           citation=Citation("ref", "https://pubmed.ncbi.nlm.nih.gov/1/"))])
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "r.html")
        render.render_report(rep, out)
        html = open(out, encoding="utf-8").read()
    assert "DrugX" in html and "gene therapy" in html
