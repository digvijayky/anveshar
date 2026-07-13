"""Data-integrity tests for the shipped example knowledge bases.

Every disease report example parses, has the required report keys, uses integer tiers and
known modalities, cites a real URL per therapy, and contains no em/en dashes. Every patient
profile parses and carries alterations. Runs fully offline.
"""
import os
import glob
import json
import pytest
from anveshar.schema import assert_no_dashes, Modality

ROOT = os.path.join(os.path.dirname(__file__), "..")
EX = os.path.join(ROOT, "examples")
REPORTS = sorted(glob.glob(os.path.join(EX, "*.json")) +
                 glob.glob(os.path.join(EX, "rare_disease", "*.json")))
PROFILES = sorted(glob.glob(os.path.join(EX, "profiles", "*.json")))
REQUIRED = ["cancer", "overview", "targets", "therapies", "disclaimer"]
MODS = {m.value for m in Modality}


@pytest.mark.parametrize("path", REPORTS, ids=[os.path.basename(p) for p in REPORTS])
def test_report_example_valid(path):
    d = json.load(open(path, encoding="utf-8"))
    for k in REQUIRED:
        assert k in d, f"{os.path.basename(path)} missing key {k}"
    assert d["cancer"].get("name"), "condition name is required"
    for t in d["therapies"]:
        assert isinstance(t.get("tier"), int), "tier must be an integer"
        if t.get("modality"):
            assert t["modality"] in MODS, f"unknown modality {t['modality']}"
        assert t.get("citation", {}).get("url", "").startswith("http"), "therapy needs a real citation url"
    assert_no_dashes(d)


@pytest.mark.parametrize("path", PROFILES, ids=[os.path.basename(p) for p in PROFILES])
def test_profile_example_valid(path):
    d = json.load(open(path, encoding="utf-8"))
    assert d.get("alterations"), "a profile needs alterations"
    assert_no_dashes(d)
