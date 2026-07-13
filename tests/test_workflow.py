"""Tests for the bespoke comp-bio workflow generator."""
from anveshar import workflow, pipeline


def test_driver_class_detection():
    assert workflow.driver_class("EWSR1::FLI1 fusion") == "fusion"
    assert workflow.driver_class("SMARCB1 loss") == "loss_or_epigenetic"
    assert workflow.driver_class("BRAF V600E mutation") == "activating_mutation"
    assert workflow.driver_class("MDM2 amplification") == "amplification"
    assert workflow.driver_class("") == "unknown"


def test_generate_shape_and_tailoring():
    d = pipeline.run("renal medullary carcinoma", live=False)
    w = d["workflow"]
    assert w["driver_class"] == "loss_or_epigenetic"
    assert len(w["steps"]) == 7
    for s in w["steps"]:
        assert s["title"] and s["what"] and s["tools"] and s["outputs"]
    # names real databases and skills across the plan
    blob = " ".join(s["tools"] for s in w["steps"]).lower()
    for tok in ["open targets", "depmap", "chembl", "clinical-trial-protocol", "deep-research", "pubmed"]:
        assert tok in blob, tok
    assert w["how_to_run"].startswith("python3 -m anveshar.cli analyze")
    assert "—" not in str(w) and "–" not in str(w)


def test_workflow_differs_by_driver_class():
    a = pipeline.run("renal medullary carcinoma", live=False)["workflow"]      # loss
    b = pipeline.run("dedifferentiated liposarcoma", live=False)["workflow"]   # amplification
    assert a["driver_class"] != b["driver_class"]
    assert a["steps"][0]["title"] != b["steps"][0]["title"]


def test_actionable_condition_names_the_drug_in_its_drug_stage():
    d = pipeline.run("gastrointestinal stromal tumor", live=False)
    drug_stage = d["workflow"]["steps"][4]
    assert "Imatinib" in drug_stage["what"] or "imatinib" in drug_stage["what"].lower()


def test_loss_driver_pivots_to_induced_dependency():
    d = pipeline.run("renal medullary carcinoma", live=False)
    assert d["induced_dependencies"].get("SMARCB1", {}).get("dependency") == "EZH2"
    stage1 = d["workflow"]["steps"][0]
    assert "EZH2" in stage1["title"] and "EZH2" in stage1["what"]
    # the lost tumor suppressor is named as not directly druggable
    assert "cannot be drugged directly" in stage1["what"]
