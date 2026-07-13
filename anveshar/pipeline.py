"""Anveshar analysis pipeline: a reproducible, provenance tracked comp-bio harness.

Given a rare cancer name, the pipeline chains local curated knowledge with live biomedical
databases to produce a cited, confidence scored cross condition translation dossier. Every
stage appends a provenance record (source, query, count, note) so a run is auditable end to
end and reproducible. It degrades gracefully with no network: offline runs use the local
catalog and actionable driver map and mark live database stages as skipped.

Stages
  1 resolve      map the condition to its catalog row, driver genes, causes
  2 databases    query Open Targets, Ensembl, ChEMBL, PubMed, ClinicalTrials (live only)
  3 translate    borrowable approved therapies (cited, confidence scored) + shared driver
                 cross condition candidates
  4 assemble     confidence summary, full provenance, and a health provider disclaimer

Run:  python3 -m anveshar.pipeline "renal medullary carcinoma" [--live]
This is research decision support, not medical advice.
"""
from __future__ import annotations
import re, json, sys

from . import analysis, workflow
from .evidence import pubmed, clinicaltrials
from .evidence.workbench import WorkbenchClient

DISCLAIMER = ("This dossier is automatically generated research and educational decision "
              "support compiled from public biomedical databases and the peer reviewed "
              "literature. It is not medical advice. A gene level driver match is a "
              "translation hypothesis, not a guarantee that a specific variant is drug "
              "sensitive. Every treatment decision must be made by a qualified health care "
              "provider, ideally within a clinical trial.")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _contig(a, b):
    """True if list A appears as a contiguous run of whole tokens inside list B."""
    if not a or len(a) > len(b):
        return False
    return any(b[i:i + len(a)] == a for i in range(len(b) - len(a) + 1))


def _find(name: str, rows):
    """Resolve a condition name to a catalog row by exact, alias, or normalized match."""
    key = _norm(name)
    for r in rows:
        if _norm(r["name"]) == key or r.get("slug") == name:
            return r
    for r in rows:
        if key in {_norm(a) for a in (r.get("aliases") or [])}:
            return r
    kt = key.split()                     # last resort: whole-token contiguous match,
    if len(kt) >= 2:                     # multi-word queries only, either direction, so
        for r in rows:                   # "NET" no longer resolves to "signet ring ..."
            nt = _norm(r["name"]).split()
            if _contig(kt, nt) or _contig(nt, kt):
                return r
    return None


def resolve(name: str, rows=None, prov=None):
    """Stage 1: resolve the condition to its driver genes and etiology from the catalog."""
    rows = rows if rows is not None else analysis.load_catalog()
    r = _find(name, rows)
    if not r:
        if prov is not None:
            prov.append({"stage": "resolve", "source": "Anveshar catalog", "query": name,
                         "n": 0, "note": "no matching rare cancer in catalog"})
        return None
    genes = sorted(analysis._driver_genes(r.get("key_gene_or_marker", "")))
    induced = {g: analysis.induced_for(g) for g in genes if analysis.induced_for(g)}
    if prov is not None:
        note = f"matched {r['name']}; drivers {', '.join(genes) or 'none catalogued'}"
        if induced:
            note += "; induced dependency " + ", ".join(f"{g} to {e['dependency']}" for g, e in induced.items())
        prov.append({"stage": "resolve", "source": "Anveshar catalog", "query": name, "n": len(genes), "note": note})
    return {"name": r["name"], "system": r.get("organ_system", ""),
            "marker": r.get("key_gene_or_marker", ""), "genes": genes, "induced": induced,
            "causes": r.get("causes", ""), "cause_known": bool(r.get("cause_known")),
            "cause_source": r.get("cause_source", ""), "_row": r}


def databases(genes, live=False, prov=None, client=None):
    """Stage 2: query molecular databases for each driver gene. Live only; offline is skipped.

    Returns {gene: {opentargets, ensembl, chembl}} for whatever resolved. Every call appends a
    provenance record. Network failures degrade to empty results (never raise)."""
    out = {}
    if not live:
        if prov is not None:
            prov.append({"stage": "databases", "source": "Open Targets, Ensembl, ChEMBL",
                         "query": ", ".join(genes), "n": 0,
                         "note": "offline mode: live database stage skipped"})
        return out
    client = client or WorkbenchClient()
    for g in genes:
        ot = client.opentargets(g)
        target = (ot or {}).get("target", {}) if isinstance(ot, dict) else {}
        drugs = (target.get("drugAndClinicalCandidates") or {}).get("rows", []) if target else []
        diseases = (target.get("associatedDiseases") or {}).get("rows", []) if target else []
        ens = client.ensembl(g)
        ch = client.chembl(g)
        out[g] = {
            "opentargets_symbol": target.get("approvedSymbol", ""),
            "opentargets_drugs": sorted({d.get("drug", {}).get("name", "") for d in drugs if d.get("drug")}),
            "opentargets_diseases": [d.get("disease", {}).get("name", "") for d in diseases[:6]],
            "ensembl_id": (ens or {}).get("id", ""),
            "chembl_targets": (ch or {}).get("page_meta", {}).get("total_count") if isinstance(ch, dict) else None,
        }
        if prov is not None:
            prov.append({"stage": "databases", "source": "Open Targets Platform (GraphQL)",
                         "query": g, "n": len(out[g]["opentargets_drugs"]),
                         "note": f"{g} -> drugs {', '.join(out[g]['opentargets_drugs'][:4]) or 'none'}"})
    return out


_SM_RANK = {"Approved Drug": 10, "Advanced Clinical": 9, "Phase 1 Clinical": 8,
            "Structure with Ligand": 6, "High-Quality Ligand": 5, "High-Quality Pocket": 4,
            "Med-Quality Pocket": 3, "Druggable Family": 2}
_AB_RANK = {"Approved Drug": 10, "Advanced Clinical": 9, "Phase 1 Clinical": 8,
            "UniProt loc high conf": 5, "GO CC high conf": 5, "UniProt SigP or TMHMM": 4,
            "Human Protein Atlas loc": 4}


def _essentiality(dep):
    effs = [sc["geneEffect"] for t in (dep or []) for sc in (t.get("screens") or [])
            if isinstance(sc.get("geneEffect"), (int, float))]
    if not effs:
        return None
    return {"n": len(effs), "min": round(min(effs), 3), "mean": round(sum(effs) / len(effs), 3)}


def target_validation(genes, live=False, prov=None, client=None):
    """Stage: functional genomics validation of each driver gene from Open Targets and DepMap.

    Scores druggability tractability, whether the gene is a selective dependency (essential in
    some lineages but not a common essential gene), and known safety liabilities, then returns a
    verdict per gene. Live only; offline is skipped with a provenance note."""
    if not live:
        if prov is not None:
            prov.append({"stage": "validation", "source": "Open Targets tractability, DepMap essentiality",
                         "query": ", ".join(genes), "n": 0, "note": "offline mode: target validation skipped"})
        return {}
    client = client or WorkbenchClient()
    out = {}
    for g in genes:
        t = client.opentargets_target_profile(g)
        if not t:
            out[g] = {"available": False}
            if prov is not None:
                prov.append({"stage": "validation", "source": "Open Targets Platform", "query": g,
                             "n": 0, "note": f"{g}: no target profile returned"})
            continue
        tract = t.get("tractability") or []
        sm = max((_SM_RANK.get(x.get("label"), 0) for x in tract if x.get("modality") == "SM" and x.get("value")), default=0)
        ab = max((_AB_RANK.get(x.get("label"), 0) for x in tract if x.get("modality") == "AB" and x.get("value")), default=0)
        ess = _essentiality(t.get("depMapEssentiality"))
        common = bool(t.get("isEssential"))
        safety = len(t.get("safetyLiabilities") or [])
        tractable = sm >= 5 or ab >= 4
        selective = bool(ess and ess["min"] < -0.5 and not common)
        if common:
            verdict = "Common essential gene, selectivity risk for a systemic drug"
        elif tractable and (sm >= 8 or selective):
            verdict = "Validated, tractable target"
        elif tractable:
            verdict = "Tractable, dependency not yet established in this lineage"
        else:
            verdict = "Poorly tractable, may need new chemistry or a different modality"
        score = int(min(100, max(0, sm * 7 + (25 if selective else 0) - safety * 4 + (8 if ab >= 8 else 0))))
        out[g] = {"available": True, "symbol": t.get("approvedSymbol", ""), "ensembl": t.get("ensemblId", ""),
                  "sm_tractability": sm, "ab_tractability": ab, "tractable": tractable,
                  "common_essential": common, "selective_dependency": selective,
                  "essentiality": ess, "safety_liabilities": safety, "verdict": verdict, "score": score,
                  "source": {"label": "Open Targets Platform (tractability, DepMap essentiality, safety)",
                             "url": "https://platform.opentargets.org/target/" + (t.get("ensemblId") or "")}}
        if prov is not None:
            prov.append({"stage": "validation", "source": "Open Targets Platform, DepMap", "query": g,
                         "n": score, "note": f"{g}: {verdict} (SM tractability {sm}, "
                                             f"{'selective dependency' if selective else 'not a selective dependency'})"})
    return out


def translate(resolved, rows=None, drivers=None, prov=None):
    """Stage 3: borrowable approved therapies (cited, scored) and shared driver candidates."""
    rows = rows if rows is not None else analysis.load_catalog()
    drivers = drivers if drivers is not None else analysis.load_actionable()
    row = resolved["_row"]
    amap = {a["name"]: a for a in analysis.actionable_map([row], drivers)}
    actionable = amap.get(row["name"], {}).get("matches", [])
    best = amap.get(row["name"])
    # shared driver cross condition candidates from the whole catalog
    shared = dict(analysis.catalog_shared_drivers(rows))
    cross = {}
    for g in resolved["genes"]:
        others = [c for c in shared.get(g, []) if c != row["name"]]
        if others:
            cross[g] = others
    if prov is not None:
        prov.append({"stage": "translate", "source": "Anveshar actionable driver map",
                     "query": ", ".join(resolved["genes"]), "n": len(actionable),
                     "note": f"{len(actionable)} borrowable approved therapies, "
                             f"{sum(len(v) for v in cross.values())} shared driver candidates"})
    return {"actionable": actionable,
            "best_confidence": best.get("confidence") if best else None,
            "cross_condition": cross}


def run(name: str, live: bool = False, client=None) -> dict:
    """Run the full pipeline and return a dossier dict with provenance and a disclaimer."""
    rows = analysis.load_catalog()
    drivers = analysis.load_actionable()
    prov = []
    resolved = resolve(name, rows, prov)
    if not resolved:
        return {"condition": name, "resolved": False, "provenance": prov, "disclaimer": DISCLAIMER}
    db = databases(resolved["genes"], live=live, prov=prov, client=client)
    # validate the driver genes and, for loss drivers, the druggable induced dependency
    val_genes = list(resolved["genes"]) + [e["dependency"] for e in resolved.get("induced", {}).values()
                                           if e["dependency"] not in resolved["genes"]]
    val = target_validation(val_genes, live=live, prov=prov, client=client)
    tr = translate(resolved, rows, drivers, prov)
    lit = {}
    if live:
        for g in resolved["genes"][:3]:
            hits = pubmed.search(f'{resolved["name"]} {g} therapy', retmax=5)
            lit[g] = hits
            prov.append({"stage": "literature", "source": "PubMed (NCBI E utilities)",
                         "query": f'{resolved["name"]} {g} therapy', "n": len(hits),
                         "note": f"{len(hits)} PubMed records"})
    n_ta = sum(1 for m in tr["actionable"] if m.get("tissue_agnostic"))
    wf = workflow.generate(resolved, tr)
    prov.append({"stage": "workflow", "source": "Anveshar workflow generator", "query": resolved["name"],
                 "n": len(wf["steps"]), "note": f"{wf['driver_class']} class; {len(wf['steps'])} stage comp-bio workflow"})
    return {
        "condition": resolved["name"], "resolved": True, "system": resolved["system"],
        "drivers": resolved["genes"], "marker": resolved["marker"],
        "etiology": {"causes": resolved["causes"], "established": resolved["cause_known"],
                     "source": resolved["cause_source"]},
        "databases": db, "target_validation": val, "induced_dependencies": resolved.get("induced", {}),
        "literature": lit, "translation": tr, "workflow": wf,
        "summary": {"n_actionable": len(tr["actionable"]), "n_tissue_agnostic": n_ta,
                    "n_cross_condition": sum(len(v) for v in tr["cross_condition"].values()),
                    "best_confidence": tr["best_confidence"]},
        "provenance": prov, "mode": "live" if live else "offline", "disclaimer": DISCLAIMER,
    }


def main():
    args = sys.argv[1:]
    live = "--live" in args
    names = [a for a in args if not a.startswith("--")]
    if not names:
        print('usage: python3 -m anveshar.pipeline "<rare cancer>" [--live]'); return
    d = run(" ".join(names), live=live)
    print(json.dumps(d, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
