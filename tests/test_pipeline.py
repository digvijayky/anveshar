"""Pipeline harness tests. Offline and deterministic: no network is touched (live=False)."""
from anveshar import pipeline


def test_resolves_and_translates_flagship():
    d = pipeline.run("renal medullary carcinoma", live=False)
    assert d["resolved"] and d["condition"] == "Renal medullary carcinoma"
    assert "SMARCB1" in d["drivers"]
    # borrowable therapy is cited and confidence scored, and is a cross tumor translation (tier >= 2)
    act = d["translation"]["actionable"]
    assert act and act[0]["citation"]["url"].startswith("http")
    assert d["summary"]["best_confidence"]["pct"] <= 90
    # SMARCB1 links the rhabdoid family as cross condition candidates
    assert d["summary"]["n_cross_condition"] >= 3


def test_tissue_agnostic_reaches_high_confidence():
    d = pipeline.run("anaplastic thyroid carcinoma", live=False)
    assert any(m["tissue_agnostic"] for m in d["translation"]["actionable"])
    assert d["summary"]["best_confidence"]["label"] == "High"


def test_offline_marks_database_stage_skipped():
    d = pipeline.run("gastrointestinal stromal tumor", live=False)
    dbstage = [p for p in d["provenance"] if p["stage"] == "databases"][0]
    assert "offline" in dbstage["note"]
    assert d["mode"] == "offline"
    assert d["databases"] == {}


def test_unresolved_is_graceful_and_carries_disclaimer():
    d = pipeline.run("not a real condition zzz", live=False)
    assert d["resolved"] is False
    assert "not medical advice" in d["disclaimer"]
    assert any(p["stage"] == "resolve" and p["n"] == 0 for p in d["provenance"])


def test_every_run_has_provenance_and_disclaimer():
    d = pipeline.run("gastrointestinal stromal tumor", live=False)
    stages = [p["stage"] for p in d["provenance"]]
    assert stages[:4] == ["resolve", "databases", "validation", "translate"]
    assert d["disclaimer"] and "health care provider" in d["disclaimer"]
    # no em or en dashes anywhere in the emitted dossier
    import json
    blob = json.dumps(d)
    assert "—" not in blob and "–" not in blob


class _FakeVClient:
    """Fake WorkbenchClient returning a canned Open Targets target profile for validation tests."""
    def __init__(self, profile):
        self._p = profile
    def opentargets(self, gene):
        return {}
    def ensembl(self, gene):
        return {}
    def chembl(self, gene):
        return {}
    def opentargets_target_profile(self, gene):
        return dict(self._p, approvedSymbol=gene, ensemblId="ENSG_TEST")


def test_target_validation_offline_skipped():
    prov = []
    out = pipeline.target_validation(["KIT"], live=False, prov=prov)
    assert out == {}
    assert prov and "offline" in prov[0]["note"]


def test_target_validation_scores_a_validated_target():
    prof = {"isEssential": False,
            "tractability": [{"label": "Approved Drug", "modality": "SM", "value": True},
                             {"label": "Phase 1 Clinical", "modality": "AB", "value": True}],
            "depMapEssentiality": [{"tissueName": "kidney", "screens": [
                {"cellLineName": "A", "geneEffect": -1.2}, {"cellLineName": "B", "geneEffect": -0.1}]}],
            "safetyLiabilities": []}
    out = pipeline.target_validation(["KIT"], live=True, client=_FakeVClient(prof))
    v = out["KIT"]
    assert v["available"] and v["tractable"] and v["selective_dependency"]
    assert v["verdict"] == "Validated, tractable target"
    assert v["score"] > 0 and v["source"]["url"].startswith("https://platform.opentargets.org")


def test_target_validation_flags_common_essential():
    prof = {"isEssential": True,
            "tractability": [{"label": "Structure with Ligand", "modality": "SM", "value": True}],
            "depMapEssentiality": [{"screens": [{"geneEffect": -2.4}]}], "safetyLiabilities": []}
    out = pipeline.target_validation(["POLR2A"], live=True, client=_FakeVClient(prof))
    assert "selectivity risk" in out["POLR2A"]["verdict"]
