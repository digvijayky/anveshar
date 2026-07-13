"""Cross-condition analyses over Anveshar's curated knowledge.

These aggregate every shipped condition to answer questions a single report cannot:
which therapies recur across conditions (the strongest translation signal), how the full
set of translations ranks by confidence, and how the therapy modalities distribute. Every
row keeps its citation so nothing is asserted without a source.
"""
import os
import re
import json
import glob
from collections import defaultdict, Counter

from .score import therapy_confidence

EX = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")
_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CATALOG = os.path.join(_DATA, "rare_conditions_catalog.json")
ACTIONABLE = os.path.join(_DATA, "actionable_drivers.json")
INDUCED = os.path.join(_DATA, "induced_dependencies.json")

# tokens that appear in a marker string but are not gene symbols
_MARKER_STOP = {
    "LOSS", "GAIN", "AMP", "DEL", "MUT", "MUTATION", "MUTANT", "FUSION", "HIGH", "LOW", "WT",
    "POSITIVE", "NEGATIVE", "IHC", "DELETION", "AMPLIFICATION", "REARRANGEMENT", "TYPE",
    "AND", "OR", "THE", "VARIANT", "EXPRESSION", "OVEREXPRESSION", "STATUS", "PATHWAY",
    "SIGNALING", "INACTIVATION", "DEFICIENT", "DEFICIENCY", "BIALLELIC", "GERMLINE", "SOMATIC",
    "DNA", "RNA", "CNS", "NOS",
}
_MUT_NOTATION = re.compile(r"^[A-Z]\d+[A-Z]?$")   # e.g. D816V, V600E, R132, G12C


def _driver_genes(marker: str) -> set:
    """Extract gene or fusion-partner symbols from a marker string.

    Splits on non-alphanumerics and keeps uppercase symbols of length 2 or more,
    dropping generic words and point-mutation notation (D816V, V600E) so cancers
    that share the same underlying gene cluster together even across fusions.
    """
    out = set()
    for t in re.split(r"[^A-Za-z0-9]+", marker or ""):
        if len(t) >= 2 and re.fullmatch(r"[A-Z0-9]+", t) and not t.isdigit() \
                and t not in _MARKER_STOP and not _MUT_NOTATION.match(t):
            out.add(t)
    return out


def load_catalog(cancers_only: bool = True):
    """Return catalog rows; rare cancers only by default."""
    rows = json.load(open(CATALOG, encoding="utf-8"))
    return [r for r in rows if r.get("category") == "rare cancer"] if cancers_only else rows


def catalog_shared_drivers(rows=None):
    """Group rare cancers by a shared driver gene or marker across the whole catalog.

    Returns [(gene, [cancer names])] for every gene present in more than one rare
    cancer, most shared first. This is the cross-condition translation map at catalog
    scale: two cancers under the same gene are candidates to borrow each other's therapies.
    """
    rows = rows if rows is not None else load_catalog()
    m = defaultdict(set)
    for r in rows:
        for g in _driver_genes(r.get("key_gene_or_marker", "")):
            m[g].add(r["name"])
    return sorted([(g, sorted(v)) for g, v in m.items() if len(v) > 1],
                  key=lambda x: (-len(x[1]), x[0]))


def catalog_by_system(rows=None):
    """Return {organ_system: [cancer names]} across the rare cancer catalog."""
    rows = rows if rows is not None else load_catalog()
    m = defaultdict(list)
    for r in rows:
        m[r.get("organ_system", "Additional catalogued rare cancers")].append(r["name"])
    return {k: sorted(v) for k, v in sorted(m.items(), key=lambda x: -len(x[1]))}


def catalog_summary(rows=None):
    """Headline counts for the full rare cancer catalog."""
    rows = rows if rows is not None else load_catalog()
    shared = catalog_shared_drivers(rows)
    with_driver = [r for r in rows if _driver_genes(r.get("key_gene_or_marker", ""))]
    return {
        "n_rare_cancers": len(rows),
        "n_with_driver": len(with_driver),
        "n_shared_drivers": len(shared),
        "n_systems": len(catalog_by_system(rows)),
        "top_shared": [(g, len(v)) for g, v in shared[:12]],
    }


def load_actionable():
    """Return the curated driver -> approved therapy map ({gene: entry})."""
    return json.load(open(ACTIONABLE, encoding="utf-8")).get("drivers", {})


def load_induced():
    """Return the synthetic lethal induced dependency map ({lost_gene: entry})."""
    return json.load(open(INDUCED, encoding="utf-8")).get("induced", {})


def induced_for(gene, induced=None):
    """Return the induced dependency entry for a lost tumor suppressor, or None."""
    induced = induced if induced is not None else load_induced()
    return induced.get(gene)


def druggability_gap(rows=None, drivers=None):
    """Shared dependencies that drive multiple rare cancers yet have no approved drug.

    Returns [(gene, [cancer names])] for driver genes present in more than one rare cancer
    that are NOT in the actionable driver map, most cancers first. This is the unmet need map:
    where a single undrugged dependency, if made tractable, would help many rare cancers at once.
    """
    rows = rows if rows is not None else load_catalog()
    drivers = drivers if drivers is not None else load_actionable()
    shared = catalog_shared_drivers(rows)
    return [(g, cs) for g, cs in shared if g not in drivers]


def druggability_summary(rows=None):
    """Counts for the druggability gap over the shared dependency map."""
    rows = rows if rows is not None else load_catalog()
    shared = catalog_shared_drivers(rows)
    gap = druggability_gap(rows)
    return {
        "n_shared_drivers": len(shared),
        "n_druggable_shared": len(shared) - len(gap),
        "n_unmet_shared": len(gap),
        "top_unmet": [(g, len(cs)) for g, cs in gap[:12]],
    }


def actionable_map(rows=None, drivers=None):
    """For each rare cancer, cross reference its driver genes with the actionable driver
    map and attach the best borrowable approved therapy with a confidence score.

    Returns [{name, system, matches:[{gene, drug, approved_in, tier, tissue_agnostic,
    citation}], best_tier, confidence}] for cancers that carry at least one actionable driver.
    Confidence reuses the transparent tier plus citation rule from score.therapy_confidence.
    """
    rows = rows if rows is not None else load_catalog()
    drivers = drivers if drivers is not None else load_actionable()
    out = []
    for r in rows:
        genes = _driver_genes(r.get("key_gene_or_marker", ""))
        matches = []
        for g in sorted(genes):
            e = drivers.get(g)
            if e:
                # effective translation tier: only a tissue agnostic label applies to this
                # cancer as tier 1; a drug approved for the same gene in another disease is a
                # tier 2 cross condition translation here, never an on label tier 1 claim.
                eff = 1 if e.get("tissue_agnostic") else max(2, e["tier"])
                matches.append({"gene": g, "drug": e["drug"], "approved_in": e["approved_in"],
                                "tier": eff, "dev_tier": e["tier"],
                                "tissue_agnostic": e.get("tissue_agnostic", False),
                                "moa": e.get("moa", ""), "caveat": e.get("caveat", ""),
                                "citation": e.get("citation", {})})
        if not matches:
            continue
        best = min(matches, key=lambda m: m["tier"])
        conf = therapy_confidence({"tier": best["tier"], "citation": best["citation"]})
        out.append({"name": r["name"], "system": r.get("organ_system", ""),
                    "matches": matches, "best_tier": best["tier"], "best_drug": best["drug"],
                    "tissue_agnostic": best["tissue_agnostic"], "confidence": conf})
    out.sort(key=lambda x: (x["best_tier"], -len(x["matches"]), x["name"]))
    return out


def actionability_summary(rows=None):
    """Headline counts for the actionability analysis over the rare cancer catalog."""
    rows = rows if rows is not None else load_catalog()
    amap = actionable_map(rows)
    ta = [a for a in amap if a["tissue_agnostic"]]
    from collections import Counter as _C
    by_drug = _C(a["best_drug"] for a in amap)
    return {
        "n_rare_cancers": len(rows),
        "n_actionable": len(amap),
        "n_tissue_agnostic": len(ta),
        "pct_actionable": round(100 * len(amap) / max(1, len(rows))),
        "top_drugs": by_drug.most_common(10),
    }


_ETIOLOGY = [
    ("Infectious", ["virus", "viral", "hpv", "epstein", "ebv", "hhv-8", "hhv 8", "kshv",
                    "htlv", "polyomavirus", "helicobacter", "fluke", "hepatitis", "malaria"]),
    ("Environmental or carcinogen", ["asbestos", "radiation", "ultraviolet", "uv ", "uv-",
                    "vinyl chloride", "thorotrast", "benzene", "tobacco", "smoking", "lymphedema",
                    "implant", "diethylstilbestrol", "arsenic", "sun exposure"]),
    ("Hereditary syndrome", ["germline", "inherited", "hereditary", "li-fraumeni", "li fraumeni",
                    "neurofibromatosis", "von hippel", "multiple endocrine neoplasia", "men1", "men2",
                    "lynch", "familial adenomatous", "beckwith", "gorlin", "carney", "tuberous sclerosis",
                    "rhabdoid tumor predisposition", "familial", "sdh", "vhl", "rb1", "dicer1",
                    "birt-hogg", "predisposition syndrome"]),
    ("Precursor lesion or transformation", ["precursor", "arises from", "pre-existing", "preexisting",
                    "transformation", "arising in", "chronic inflammation", "sclerosing cholangitis",
                    "atrophic gastritis", "molar pregnancy", "enchondroma", "osteochondroma", "paget"]),
]


def etiology_landscape(rows=None):
    """Categorize rare cancers by the type of cause, with counts and examples.

    Categories are Infectious, Environmental or carcinogen, Hereditary syndrome,
    Precursor lesion or transformation, and Cause not established. A cancer can carry
    more than one category. Returns {category: {count, examples}} plus n_unknown.
    """
    rows = rows if rows is not None else load_catalog()
    buckets = {name: [] for name, _ in _ETIOLOGY}
    unknown = []
    for r in rows:
        txt = (r.get("causes", "") or "").lower()
        hit = False
        if r.get("cause_known"):
            for name, kws in _ETIOLOGY:
                if any(k in txt for k in kws):
                    buckets[name].append(r["name"]); hit = True
        if not r.get("cause_known") or (r.get("cause_known") and not hit):
            if not r.get("cause_known"):
                unknown.append(r["name"])
    out = {name: {"count": len(v), "examples": sorted(v)[:8]} for name, v in buckets.items()}
    out["Cause not established"] = {"count": len(unknown), "examples": sorted(unknown)[:8]}
    return out


_SYNDROMES = [
    ("Li-Fraumeni syndrome (TP53)", ["li-fraumeni", "li fraumeni"]),
    ("Neurofibromatosis type 1 (NF1)", ["neurofibromatosis type 1", "nf1"]),
    ("von Hippel-Lindau (VHL)", ["von hippel", "vhl"]),
    ("Multiple endocrine neoplasia (MEN)", ["multiple endocrine neoplasia", "men1", "men2", "men 1", "men 2"]),
    ("Lynch syndrome (mismatch repair)", ["lynch"]),
    ("Familial adenomatous polyposis (APC)", ["familial adenomatous", "fap ", "apc"]),
    ("Beckwith-Wiedemann syndrome", ["beckwith"]),
    ("Rhabdoid tumor predisposition (SMARCB1)", ["rhabdoid tumor predisposition"]),
    ("Retinoblastoma predisposition (RB1)", ["germline rb1", "retinoblastoma predisposition", "hereditary retinoblastoma"]),
    ("Tuberous sclerosis complex", ["tuberous sclerosis"]),
    ("Gorlin syndrome (PTCH1)", ["gorlin"]),
    ("Succinate dehydrogenase deficiency (SDHx)", ["sdhx", "sdhb", "sdh "]),
]


def hereditary_syndrome_map(rows=None):
    """Map inherited cancer predisposition syndromes to the rare cancers they cause.

    Returns [(syndrome, [cancer names])] for syndromes linked to at least one rare cancer,
    read from the cited causes field, most linked first.
    """
    rows = rows if rows is not None else load_catalog()
    m = defaultdict(set)
    for r in rows:
        txt = (r.get("causes", "") or "").lower()
        for name, kws in _SYNDROMES:
            if any(k in txt for k in kws):
                m[name].add(r["name"])
    return sorted([(k, sorted(v)) for k, v in m.items() if v], key=lambda x: (-len(x[1]), x[0]))


def load_all():
    """Return [(filename, DATA dict)] for every curated condition."""
    out = []
    for p in sorted(glob.glob(os.path.join(EX, "*.json")) +
                    glob.glob(os.path.join(EX, "rare_disease", "*.json"))):
        out.append((os.path.basename(p), json.load(open(p, encoding="utf-8"))))
    return out


def translation_index(conditions=None):
    """Every (condition, therapy) with confidence, sorted by confidence descending."""
    rows = []
    for _, d in (conditions or load_all()):
        cond = d.get("cancer", {}).get("name", "")
        for t in d.get("therapies", []):
            c = therapy_confidence(t)
            rows.append({
                "condition": cond, "drug": t.get("drug", ""), "target": t.get("target", ""),
                "tier": t.get("tier", 3), "modality": t.get("modality", "other"),
                "confidence": c["label"], "pct": c["pct"], "basis": c["basis"],
                "approved_in": t.get("approved_in", ""), "citation": t.get("citation", {}) or {},
            })
    rows.sort(key=lambda r: -r["pct"])
    return rows


def shared_drugs(conditions=None):
    """Drugs (or drug classes) that recur across more than one condition."""
    m = defaultdict(set)
    for _, d in (conditions or load_all()):
        cond = d.get("cancer", {}).get("name", "")
        for t in d.get("therapies", []):
            drug = (t.get("drug") or "").strip()
            if drug:
                m[drug].add(cond)
    return sorted([(k, sorted(v)) for k, v in m.items() if len(v) > 1],
                  key=lambda x: (-len(x[1]), x[0]))


_MECH_KEYWORDS = [
    "EZH2", "PRMT5", "VEGFR", "MET", "DLL3", "PD-1", "PD-L1", "checkpoint", "BRAF", "NOTCH",
    "MYB", "TFE3", "SMARCB1", "SWI/SNF", "mTOR", "BET", "IGF1R", "PARP", "proteasome",
    "gene therapy", "antisense", "RNAi", "CAR", "fusion", "SSTR2", "HER2", "NTRK",
]


def shared_mechanisms(conditions=None):
    """Group conditions by a shared mechanism keyword, the real cross-condition translation
    signal (a therapy borrows across conditions that share the same dependency)."""
    m = defaultdict(set)
    for _, d in (conditions or load_all()):
        cond = d.get("cancer", {}).get("name", "")
        blob = " ".join((t.get("target", "") + " " + t.get("drug", "") + " " + t.get("modality", ""))
                        for t in d.get("therapies", [])).lower()
        blob += " " + " ".join(t.get("name", "") for t in d.get("targets", [])).lower()
        for kw in _MECH_KEYWORDS:
            if kw.lower() in blob:
                m[kw].add(cond)
    return sorted([(k, sorted(v)) for k, v in m.items() if len(v) > 1],
                  key=lambda x: (-len(x[1]), x[0]))


def modality_counts(conditions=None):
    """Count of therapies by modality across all conditions."""
    c = Counter()
    for _, d in (conditions or load_all()):
        for t in d.get("therapies", []):
            c[t.get("modality", "other")] += 1
    return c.most_common()


def summary(conditions=None):
    conds = conditions or load_all()
    idx = translation_index(conds)
    return {
        "n_conditions": len(conds),
        "n_translations": len(idx),
        "n_shared_drugs": len(shared_drugs(conds)),
        "modalities": modality_counts(conds),
    }
