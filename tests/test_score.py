"""Confidence scoring tests: tiers map to labels, missing citations lower confidence,
hypotheses are capped below High, and score_report attaches confidence in place."""
from anveshar import score


def test_therapy_confidence_by_tier():
    assert score.therapy_confidence({"tier": 1, "citation": {"url": "x"}})["label"] == "High"
    assert score.therapy_confidence({"tier": 2, "citation": {"url": "x"}})["label"] == "Moderate"
    assert score.therapy_confidence({"tier": 3, "citation": {"url": "x"}})["label"] == "Low"


def test_missing_citation_lowers_confidence():
    c = score.therapy_confidence({"tier": 1})
    assert c["label"] == "Low" and c["pct"] < 90 and "citation missing" in c["basis"]


def test_hypothesis_capped_below_high():
    assert score.hypothesis_confidence({"transferability": "high", "citation": {"url": "x"}})["label"] == "Moderate"
    assert score.hypothesis_confidence({"transferability": "speculative"})["label"] == "Speculative"


def test_score_report_attaches_confidence():
    d = {"therapies": [{"tier": 1, "citation": {"url": "x"}}],
         "discovery": [{"transferability": "medium", "citation": {"url": "y"}}]}
    score.score_report(d)
    assert d["therapies"][0]["confidence"]["label"] == "High"
    assert "confidence" in d["discovery"][0] and d["discovery"][0]["confidence"]["pct"] > 0
