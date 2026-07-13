"""LLM live-assembly tests: prompt building, JSON extraction, and synthesis with an
injected fake client. Fully offline, no anthropic install and no network required."""
from anveshar import llm


class _Block:
    type = "text"

    def __init__(self, t):
        self.text = t


class _Msg:
    def __init__(self, t):
        self.content = [_Block(t)]


class _Messages:
    def __init__(self, t):
        self._t = t

    def create(self, **kwargs):
        return _Msg(self._t)


class _FakeClient:
    def __init__(self, t):
        self.messages = _Messages(t)


def test_build_prompt_has_condition_and_evidence():
    p = llm._build_prompt("renal medullary carcinoma", {
        "pubmed": [{"pmid": "1", "title": "A study", "journal": "J", "year": "2020"}],
        "trials": [{"nct": "NCT1", "title": "A trial"}]})
    assert "renal medullary carcinoma" in p
    assert "PMID 1" in p and "NCT1" in p
    assert "—" not in p and "–" not in p


def test_extract_json_pulls_first_object():
    d = llm._extract_json('noise {"a": 1, "b": {"c": 2}} trailing')
    assert d["a"] == 1 and d["b"]["c"] == 2


def test_extract_json_handles_braces_in_strings():
    d = llm._extract_json('{"s": "a } b { c", "n": 3}')
    assert d["s"] == "a } b { c" and d["n"] == 3


def test_synthesize_parses_and_validates():
    canned = '{"cancer": {"name": "Test condition"}, "therapies": [], "disclaimer": "ok"}'
    d = llm.synthesize_report("Test condition", {"pubmed": [], "trials": []}, client=_FakeClient(canned))
    assert d["cancer"]["name"] == "Test condition"


def test_synthesize_scrubs_dashes():
    canned = '{"cancer": {"name": "A \\u2014 B"}, "disclaimer": "x"}'
    d = llm.synthesize_report("A", {"pubmed": [], "trials": []}, client=_FakeClient(canned))
    assert "—" not in d["cancer"]["name"] and "–" not in d["cancer"]["name"]
