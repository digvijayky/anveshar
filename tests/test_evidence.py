"""Offline tests for anveshar.evidence connectors.

No test hits the network. Each test feeds a small embedded JSON payload (the
shape returned by NCBI E-utilities or the ClinicalTrials.gov API v2) directly
into a pure parse function and asserts the normalized output. WorkbenchClient's
model connector methods are checked for their graceful available False shape.
"""
from anveshar.evidence import pubmed, clinicaltrials, clinvar
from anveshar.evidence.workbench import WorkbenchClient
from anveshar.schema import Trial


# ---------------------------------------------------------------- pubmed

ESEARCH_PAYLOAD = {
    "esearchresult": {"count": "2", "retmax": "2", "idlist": ["30000001", "30000002"]}
}

ESUMMARY_PAYLOAD = {
    "result": {
        "uids": ["30000001", "30000002"],
        "30000001": {
            "uid": "30000001",
            "title": "A translational board for rare cancers",
            "fulljournalname": "Cancer Cell",
            "pubdate": "2024 Mar 15",
            "articleids": [
                {"idtype": "pubmed", "value": "30000001"},
                {"idtype": "doi", "value": "10.1016/j.ccell.2024.01.001"},
            ],
        },
        "30000002": {
            "uid": "30000002",
            "title": "Cross condition therapy matching",
            "source": "Nature",
            "sortpubdate": "2023/07/01 00:00",
            "elocationid": "doi: 10.1038/s41586-023-00002-2",
            "articleids": [{"idtype": "pubmed", "value": "30000002"}],
        },
    }
}


def test_parse_esearch_returns_pmids():
    assert pubmed._parse_esearch(ESEARCH_PAYLOAD) == ["30000001", "30000002"]


def test_parse_esearch_empty_on_junk():
    assert pubmed._parse_esearch({}) == []
    assert pubmed._parse_esearch({"esearchresult": {}}) == []


def test_parse_esummary_normalizes_records():
    recs = pubmed._parse_esummary(ESUMMARY_PAYLOAD)
    assert len(recs) == 2
    assert recs[0] == {
        "pmid": "30000001",
        "title": "A translational board for rare cancers",
        "journal": "Cancer Cell",
        "year": "2024",
        "doi": "10.1016/j.ccell.2024.01.001",
    }
    # second record: journal falls back to source, year from sortpubdate, doi from elocationid
    assert recs[1]["pmid"] == "30000002"
    assert recs[1]["journal"] == "Nature"
    assert recs[1]["year"] == "2023"
    assert recs[1]["doi"] == "10.1038/s41586-023-00002-2"


def test_parse_esummary_empty_on_junk():
    assert pubmed._parse_esummary({}) == []
    assert pubmed._parse_esummary({"result": {"uids": []}}) == []


def test_parse_esummary_record_keys_exact():
    rec = pubmed._parse_esummary(ESUMMARY_PAYLOAD)[0]
    assert set(rec.keys()) == {"pmid", "title", "journal", "year", "doi"}


# ------------------------------------------------------- clinicaltrials

STUDIES_PAYLOAD = {
    "studies": [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT01234567",
                    "briefTitle": "Belzutifan in rare renal cancer",
                },
                "designModule": {"phases": ["PHASE1", "PHASE2"]},
                "armsInterventionsModule": {
                    "interventions": [
                        {"name": "Belzutifan"},
                        {"name": "Placebo"},
                    ]
                },
                "eligibilityModule": {"eligibilityCriteria": "Adults with advanced disease."},
            }
        },
        {
            # missing nctId -> should be dropped
            "protocolSection": {
                "identificationModule": {"briefTitle": "No id study"},
            }
        },
    ]
}


def test_parse_studies_maps_to_trial():
    trials = clinicaltrials._parse_studies(STUDIES_PAYLOAD)
    assert len(trials) == 1
    t = trials[0]
    assert isinstance(t, Trial)
    assert t.nct == "NCT01234567"
    assert t.title == "Belzutifan in rare renal cancer"
    assert t.phase == "PHASE1, PHASE2"
    assert t.intervention == "Belzutifan; Placebo"
    assert t.eligibility == "Adults with advanced disease."
    assert t.url == "https://clinicaltrials.gov/study/NCT01234567"


def test_parse_studies_drops_studies_without_nct():
    # payload had 2 studies, only 1 has an nctId
    assert len(clinicaltrials._parse_studies(STUDIES_PAYLOAD)) == 1


def test_parse_studies_empty_on_junk():
    assert clinicaltrials._parse_studies({}) == []
    assert clinicaltrials._parse_studies({"studies": []}) == []


# --------------------------------------------------------------- clinvar

CLINVAR_PAYLOAD = {
    "result": {
        "uids": ["13961"],
        "13961": {
            "uid": "13961",
            "accession": "VCV000013961",
            "germline_classification": {"description": "Pathogenic"},
        },
    }
}

CLINVAR_NO_SIG_PAYLOAD = {
    "result": {
        "uids": ["999"],
        "999": {"uid": "999", "accession": "VCV000000999"},
    }
}


def test_parse_clinvar_reads_significance():
    out = clinvar._parse_clinvar(CLINVAR_PAYLOAD)
    assert out == {
        "accession": "VCV000013961",
        "significance": "Pathogenic",
        "url": "https://www.ncbi.nlm.nih.gov/clinvar/variation/13961/",
    }


def test_parse_clinvar_never_invents_significance():
    out = clinvar._parse_clinvar(CLINVAR_NO_SIG_PAYLOAD)
    assert out["accession"] == "VCV000000999"
    assert out["significance"] == ""  # absent, not guessed


def test_parse_clinvar_empty_on_junk():
    assert clinvar._parse_clinvar({}) == {}
    assert clinvar._parse_clinvar({"result": {"uids": []}}) == {}


# ------------------------------------------------------------- workbench

def test_evo2_returns_available_false():
    c = WorkbenchClient()
    out = c.evo2("NM_000551.3:c.292T>C")
    assert out["available"] is False
    assert out["connector"] == "evo2"
    assert "connector interface" in out["note"]


def test_alphamissense_returns_available_false():
    c = WorkbenchClient()
    out = c.alphamissense("p.Ser65Leu")
    assert out["available"] is False
    assert out["connector"] == "alphamissense"
    assert out["query"] == "p.Ser65Leu"


def test_workbench_rest_methods_empty_on_blank_input():
    c = WorkbenchClient()
    # blank input never touches the network and returns {}
    assert c.uniprot("") == {}
    assert c.ensembl("") == {}
    assert c.reactome("") == {}
    assert c.chembl("") == {}
    assert c.opentargets("") == {}


def test_adisinsight_and_cortellis_return_available_false():
    c = WorkbenchClient()
    a = c.adisinsight("bortezomib")
    assert a["available"] is False and a["connector"] == "adisinsight"
    assert a["query"] == "bortezomib"
    o = c.cortellis("EZH2")
    assert o["available"] is False and o["connector"] == "cortellis"


class _FakeResp:
    def __init__(self, payload):
        self._p = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._p


class _FakeSession:
    """Records POST calls and returns canned Open Targets GraphQL payloads in order."""
    def __init__(self, payloads):
        self._payloads = list(payloads)
        self.calls = []

    def post(self, url, json=None, timeout=None, headers=None):
        self.calls.append(json)
        return _FakeResp(self._payloads.pop(0))


def test_opentargets_resolves_ensembl_then_target():
    search = {"data": {"search": {"hits": [
        {"id": "ENSG00000106462", "name": "EZH2", "entity": "target"}]}}}
    detail = {"data": {"target": {
        "approvedSymbol": "EZH2",
        "associatedDiseases": {"rows": [{"score": 0.7, "disease": {"id": "EFO_1", "name": "follicular lymphoma"}}]},
        "drugAndClinicalCandidates": {"count": 1, "rows": [{"drug": {"id": "CHEMBL1", "name": "TAZEMETOSTAT"}, "maxClinicalStage": 4}]}}}}
    sess = _FakeSession([search, detail])
    out = WorkbenchClient(session=sess).opentargets("EZH2")
    assert out["target"]["approvedSymbol"] == "EZH2"
    # second POST carried the resolved Ensembl id
    assert sess.calls[1]["variables"]["id"] == "ENSG00000106462"
    drugs = out["target"]["drugAndClinicalCandidates"]["rows"]
    assert drugs[0]["drug"]["name"] == "TAZEMETOSTAT"


# --------------------------------------------------------- no dash rule

def test_no_dashes_in_any_module_output():
    from anveshar.schema import NO_DASH
    payloads = [
        pubmed._parse_esummary(ESUMMARY_PAYLOAD),
        clinvar._parse_clinvar(CLINVAR_PAYLOAD),
        WorkbenchClient().evo2("x"),
        WorkbenchClient().alphamissense("y"),
        WorkbenchClient().adisinsight("z"),
        WorkbenchClient().cortellis("w"),
    ]
    blob = repr(payloads)
    for dash in NO_DASH:
        assert dash not in blob
