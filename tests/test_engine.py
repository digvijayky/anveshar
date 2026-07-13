"""Engine tests: end to end assembly, discovery firing, personalization, honest failure."""
import os
import pytest
from anveshar.engine import run
from anveshar.schema import assert_no_dashes

PROFILES = os.path.join(os.path.dirname(__file__), "..", "examples", "profiles")


def test_unknown_condition_raises():
    with pytest.raises(ValueError):
        run("a condition concord has never heard of", discovery=True)


def test_run_rmc_assembles_with_discovery():
    data = run("renal medullary carcinoma", discovery=True)
    assert data["cancer"]["name"].lower().startswith("renal medullary")
    assert isinstance(data.get("therapies"), list) and data["therapies"]
    # SMARCB1 is a discovery trigger, so the novel hypothesis layer must fire and be well formed
    assert data.get("discovery"), "expected novel hypotheses for a SMARCB1 driven cancer"
    for h in data["discovery"]:
        assert h.get("prediction"), "every hypothesis needs a testable prediction"
        assert h.get("citation", {}).get("url", "").startswith("https://")
    assert_no_dashes(data)


def test_discovery_can_be_disabled():
    data = run("rmc", discovery=False)
    assert not data.get("discovery")


def test_run_with_patient_profile_personalizes():
    data = run("renal medullary carcinoma",
               profile=os.path.join(PROFILES, "pereira_msi_braf.json"), discovery=True)
    assert data.get("patient", {}).get("present") is True
    alts = data["patient"]["alterations"]
    assert alts and any("BRAF" in a.get("gene", "") for a in alts)
    assert_no_dashes(data)
