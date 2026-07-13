"""Molecular workbench connectors (UniProt, Ensembl, Reactome, ChEMBL) plus
graceful stubs for the Claude Science model connectors (Evo 2, AlphaMissense).

``WorkbenchClient`` is a thin, best effort adapter. Each REST method calls a
real public endpoint with a short timeout and returns an empty dict on any
failure, so a caller never has to handle exceptions. The two model connector
methods, ``evo2`` and ``alphamissense``, wrap Claude Science / model services
that may not be reachable from every environment; when no live connector is
wired in they return ``{"available": False, "note": ...}`` so downstream code
degrades gracefully instead of guessing a prediction.

Endpoint URLs:
  uniprot:       https://rest.uniprot.org/uniprotkb/search
  ensembl:       https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}
  reactome:      https://reactome.org/ContentService/search/query
  chembl:        https://www.ebi.ac.uk/chembl/api/data/target/search.json
  opentargets:   https://api.platform.opentargets.org/api/v4/graphql (public GraphQL)
  adisinsight:   Claude plugin connector (not a fixed public REST URL)
  cortellis:     authenticated Claude plugin connector (not a fixed public REST URL)
  evo2:          Claude Science / model connector (not a fixed REST URL)
  alphamissense: Claude Science / model connector (not a fixed REST URL)
"""
from __future__ import annotations
import requests

TIMEOUT = 8


class WorkbenchClient:
    """Best effort client over public molecular REST APIs and model connectors.

    Every method returns a plain dict. Live REST methods return an empty dict on
    any network error or timeout; the model connector methods return a dict with
    ``available`` set to False when no live connector is configured.
    """

    def __init__(self, timeout: int = TIMEOUT, session: requests.Session | None = None):
        """Create a client.

        ``timeout`` is the per request timeout in seconds. ``session`` lets a
        caller pass a preconfigured ``requests.Session`` (else a fresh one is
        used per call).
        """
        self.timeout = timeout
        self._session = session

    def _get(self, url: str, params: dict | None = None) -> dict:
        """GET ``url`` and return parsed JSON, or an empty dict on any failure."""
        try:
            get = self._session.get if self._session is not None else requests.get
            r = get(url, params=params or {}, timeout=self.timeout,
                    headers={"Accept": "application/json"})
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, dict) else {"results": data}
        except (requests.RequestException, ValueError):
            return {}

    def _post_json(self, url: str, payload: dict) -> dict:
        """POST a JSON ``payload`` to ``url`` and return parsed JSON, or {} on any failure."""
        try:
            post = self._session.post if self._session is not None else requests.post
            r = post(url, json=payload, timeout=self.timeout,
                     headers={"Accept": "application/json", "Content-Type": "application/json"})
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, dict) else {"results": data}
        except (requests.RequestException, ValueError):
            return {}

    def uniprot(self, gene: str) -> dict:
        """Look up a human gene in UniProtKB.

        Endpoint: https://rest.uniprot.org/uniprotkb/search
        Returns the parsed JSON search response, or an empty dict on failure.
        """
        if not gene or not str(gene).strip():
            return {}
        return self._get(
            "https://rest.uniprot.org/uniprotkb/search",
            {"query": f"gene:{gene} AND organism_id:9606", "format": "json", "size": 1},
        )

    def ensembl(self, gene_or_hgvs: str) -> dict:
        """Look up a human gene symbol in the Ensembl REST API.

        Endpoint: https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}
        Returns the parsed JSON lookup, or an empty dict on failure.
        """
        if not gene_or_hgvs or not str(gene_or_hgvs).strip():
            return {}
        symbol = str(gene_or_hgvs).strip()
        return self._get(
            f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}",
            {"content-type": "application/json"},
        )

    def reactome(self, gene: str) -> dict:
        """Search Reactome ContentService for pathways touching ``gene``.

        Endpoint: https://reactome.org/ContentService/search/query
        Returns the parsed JSON search response, or an empty dict on failure.
        """
        if not gene or not str(gene).strip():
            return {}
        return self._get(
            "https://reactome.org/ContentService/search/query",
            {"query": gene, "species": "Homo sapiens", "cluster": "true"},
        )

    def chembl(self, target: str) -> dict:
        """Search ChEMBL for a drug target by name or symbol.

        Endpoint: https://www.ebi.ac.uk/chembl/api/data/target/search.json
        Returns the parsed JSON search response, or an empty dict on failure.
        """
        if not target or not str(target).strip():
            return {}
        return self._get(
            "https://www.ebi.ac.uk/chembl/api/data/target/search.json",
            {"q": target},
        )

    def opentargets(self, gene: str) -> dict:
        """Query Open Targets Platform for a target's disease associations and known drugs.

        Endpoint: https://api.platform.opentargets.org/api/v4/graphql (public GraphQL).
        Resolves the Ensembl gene id for ``gene`` then pulls the top associated diseases
        and known drugs. Returns the parsed ``data`` object, or an empty dict on failure.
        """
        if not gene or not str(gene).strip():
            return {}
        url = "https://api.platform.opentargets.org/api/v4/graphql"
        sym = str(gene).strip()
        hit = self._post_json(url, {
            "query": "query($q:String!){search(queryString:$q,entityNames:[\"target\"]){hits{id name entity}}}",
            "variables": {"q": sym},
        })
        ensg = ""
        for h in (((hit.get("data") or {}).get("search") or {}).get("hits") or []):
            if h.get("entity") == "target" and str(h.get("id", "")).startswith("ENSG"):
                ensg = h["id"]
                break
        if not ensg:
            return hit.get("data", {}) if isinstance(hit, dict) else {}
        q = ("query($id:String!){target(ensemblId:$id){approvedSymbol "
             "associatedDiseases(page:{index:0,size:10}){rows{score disease{id name}}} "
             "drugAndClinicalCandidates{count rows{drug{id name} maxClinicalStage}}}}")
        res = self._post_json(url, {"query": q, "variables": {"id": ensg}})
        return (res.get("data") or {}) if isinstance(res, dict) else {}

    def opentargets_target_profile(self, gene: str) -> dict:
        """Functional genomics profile for a target from Open Targets: druggability tractability,
        DepMap gene essentiality, and known safety liabilities.

        Resolves the Ensembl id for ``gene`` then returns the ``target`` object with
        ``tractability`` buckets, ``isEssential`` (common essential flag), per tissue
        ``depMapEssentiality``, and ``safetyLiabilities``. Empty dict on any failure.
        """
        if not gene or not str(gene).strip():
            return {}
        url = "https://api.platform.opentargets.org/api/v4/graphql"
        hit = self._post_json(url, {
            "query": "query($q:String!){search(queryString:$q,entityNames:[\"target\"]){hits{id entity}}}",
            "variables": {"q": str(gene).strip()},
        })
        ensg = ""
        for h in (((hit.get("data") or {}).get("search") or {}).get("hits") or []):
            if h.get("entity") == "target" and str(h.get("id", "")).startswith("ENSG"):
                ensg = h["id"]; break
        if not ensg:
            return {}
        q = ("query($id:String!){target(ensemblId:$id){approvedSymbol isEssential "
             "tractability{label modality value} "
             "depMapEssentiality{tissueName screens{cellLineName geneEffect}} "
             "safetyLiabilities{event datasource}}}")
        res = self._post_json(url, {"query": q, "variables": {"id": ensg}})
        t = ((res.get("data") or {}).get("target") or {}) if isinstance(res, dict) else {}
        if t:
            t["ensemblId"] = ensg
        return t

    def adisinsight(self, drug: str) -> dict:
        """Look up a drug's development pipeline in AdisInsight (Claude plugin connector).

        AdisInsight is a proprietary drug intelligence database exposed through a Claude
        plugin connector rather than a fixed public REST URL. When no live connector is
        configured (for example before the plugin is reloaded) this returns
        ``{"available": False, "note": ...}`` so callers degrade gracefully instead of
        guessing a development stage.
        """
        return {
            "available": False,
            "connector": "adisinsight",
            "query": str(drug) if drug else "",
            "note": "AdisInsight is a Claude plugin connector; no live connector is configured in this environment, so no pipeline record is returned.",
        }

    def cortellis(self, drug_or_target: str) -> dict:
        """Look up drug or target intelligence in Cortellis (Claude plugin connector).

        Cortellis is a proprietary competitive intelligence database exposed through a
        Claude plugin connector that requires interactive authentication. When no live
        connector is configured this returns ``{"available": False, "note": ...}`` so
        callers never fabricate a competitive intelligence record.
        """
        return {
            "available": False,
            "connector": "cortellis",
            "query": str(drug_or_target) if drug_or_target else "",
            "note": "Cortellis is an authenticated Claude plugin connector; no live connector is configured in this environment, so no record is returned.",
        }

    def evo2(self, hgvs: str) -> dict:
        """Score a variant with Evo 2 (Claude Science / model connector).

        Evo 2 is a genomic language model exposed through a model connector
        rather than a fixed public REST URL. When no live connector is wired
        into this environment the method returns
        ``{"available": False, "note": ...}`` so callers degrade gracefully and
        never treat a missing prediction as a result.
        """
        return {
            "available": False,
            "connector": "evo2",
            "query": str(hgvs) if hgvs else "",
            "note": "Evo 2 is a Claude Science model connector interface; no live connector is configured in this environment, so no score is returned.",
        }

    def alphamissense(self, protein_change: str) -> dict:
        """Score a missense change with AlphaMissense (Claude Science connector).

        AlphaMissense pathogenicity is exposed through a model connector rather
        than a fixed public REST URL. When no live connector is available the
        method returns ``{"available": False, "note": ...}`` so callers degrade
        gracefully and never fabricate a pathogenicity call.
        """
        return {
            "available": False,
            "connector": "alphamissense",
            "query": str(protein_change) if protein_change else "",
            "note": "AlphaMissense is a Claude Science model connector interface; no live connector is configured in this environment, so no pathogenicity score is returned.",
        }
