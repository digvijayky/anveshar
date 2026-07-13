"""Regression tests for the code-review fixes (findings 1-6 and 12).

Offline and deterministic; no network is touched. Each test pins a specific defect
found in the review so it cannot silently return.
"""
import importlib.util
import os

import pytest
import pandas as pd

from anveshar import pipeline, score
from anveshar.variants import classify
from anveshar.variants._knowledge import lookup
from anveshar.schema import VariantClass


# Finding 1: gene matching must be exact or a numbered family member, never a
# coincidental substring, so unrelated genes do not inherit an actionability grade.
def test_gene_match_rejects_coincidental_substrings():
    assert lookup("NTRK1", "fusion") is not None
    assert lookup("NTRK3", "fusion").oncokb_level == "Level 1"
    assert lookup("ALKBH5", "fusion") is None      # not ALK
    assert lookup("METTL3", "amplification") is None  # not MET
    assert lookup("KRASP1", "g12c") is None         # pseudogene, not KRAS
    assert lookup("RETSAT", "fusion") is None       # not RET


# Finding 2: no empty-pattern EGFR catch-all, so a resistance / non-classical EGFR
# variant does not inherit the Level 1 sensitizing grade, while real ones still do.
def test_egfr_resistance_variant_not_level1():
    assert lookup("EGFR", "exon 19 deletion").oncokb_level == "Level 1"
    assert lookup("EGFR", "L858R").oncokb_level == "Level 1"
    assert lookup("EGFR", "C797S") is None


# Finding 3: _find must not resolve a generic substring to the wrong disease.
def test_find_no_substring_misresolution():
    rows = [
        {"name": "Signet ring cell carcinoma of the colon and rectum", "aliases": []},
        {"name": "Renal medullary carcinoma", "aliases": []},
        {"name": "Paraganglioma", "aliases": []},
    ]
    assert pipeline._find("NET", rows) is None
    assert pipeline._find("glioma", rows) is None
    assert pipeline._find("renal medullary", rows)["name"] == "Renal medullary carcinoma"
    assert pipeline._find("Paraganglioma", rows)["name"] == "Paraganglioma"


# Finding 4: therapy_confidence must accept string tiers ("1"/"2"/"3"), not collapse
# them to Low via an int-keyed lookup miss.
def test_therapy_confidence_string_tier():
    assert score.therapy_confidence({"tier": "1", "citation": {"url": "x"}})["label"] == "High"
    assert score.therapy_confidence({"tier": "2", "citation": {"url": "x"}})["pct"] == 68
    assert score.therapy_confidence({"tier": "foo", "citation": {"url": "x"}})["label"] == "Low"


# Finding 5: an exon-level deletion is a coding indel, not a copy-number deletion.
def test_exon_deletion_is_indel():
    assert classify({"gene": "EGFR", "variant": "exon 19 deletion"}) == VariantClass.INDEL
    assert classify({"gene": "MET", "variant": "exon 14 skipping"}) == VariantClass.SPLICE
    assert classify({"gene": "CDKN2A", "variant": "deep deletion"}) == VariantClass.DELETION


# Finding 12: loss of heterozygosity is a composite / CNV biomarker, not a focal deletion.
def test_loh_is_composite():
    assert classify({"consequence": "loss of heterozygosity"}) == VariantClass.COMPOSITE


# Finding 6: the uveal melanoma high-risk class label must never be assigned by an
# arbitrary tie-break when the monosomy-3 data is empty or equally split.
def _uvm_lib():
    p = os.path.join(os.path.dirname(__file__), "..", "examples", "multimodal",
                     "uveal_melanoma_integrative", "uvm_lib.py")
    spec = importlib.util.spec_from_file_location("uvm_lib", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_high_risk_class_guards():
    lib = _uvm_lib()
    cls = pd.Series([1, 1, 2, 2], index=["a", "b", "c", "d"])
    assert lib.high_risk_class(cls, {"c", "d"}) == 2
    with pytest.raises(ValueError):
        lib.high_risk_class(cls, set())
    with pytest.raises(ValueError):
        lib.high_risk_class(cls, {"a", "c"})
