"""Cross-condition analysis tests, run over the shipped curated knowledge."""
from anveshar import analysis


def test_load_all_nonempty():
    assert len(analysis.load_all()) >= 15


def test_translation_index_sorted_and_scored():
    idx = analysis.translation_index()
    assert idx
    assert idx[0]["pct"] >= idx[-1]["pct"]
    for r in idx[:5]:
        assert r["confidence"] and r["citation"].get("url", "").startswith("http")


def test_shared_drugs_finds_recurring():
    assert any(len(conds) >= 2 for _, conds in analysis.shared_drugs())


def test_summary_shape():
    s = analysis.summary()
    assert s["n_conditions"] >= 15 and s["n_translations"] > 0 and s["modalities"]


def test_driver_gene_extraction_filters_noise():
    g = analysis._driver_genes("SMARCB1 loss")
    assert "SMARCB1" in g and "LOSS" not in g
    # point-mutation notation is not a gene
    assert "D816V" not in analysis._driver_genes("KIT D816V")
    assert "KIT" in analysis._driver_genes("KIT D816V")


def test_catalog_shared_drivers_covers_many_cancers():
    rows = analysis.load_catalog()
    assert len(rows) >= 400
    shared = analysis.catalog_shared_drivers(rows)
    genes = {g for g, _ in shared}
    # well established multi-cancer drivers must cluster
    assert {"TP53", "EWSR1", "SMARCB1"} <= genes
    # every shared cluster has at least two distinct cancers
    assert all(len(cs) >= 2 for _, cs in shared)
    # SMARCB1 links renal medullary carcinoma to the rhabdoid family
    smarcb1 = dict(shared)["SMARCB1"]
    assert any("medullary" in c.lower() for c in smarcb1)


def test_catalog_summary_shape():
    s = analysis.catalog_summary()
    assert s["n_rare_cancers"] >= 400
    assert 0 < s["n_with_driver"] <= s["n_rare_cancers"]
    assert s["n_shared_drivers"] >= 30
    assert s["n_systems"] >= 8


def test_every_rare_cancer_has_causes():
    rows = analysis.load_catalog()
    for r in rows:
        assert r.get("causes"), f"missing causes: {r['name']}"
        assert isinstance(r.get("cause_known"), bool), f"missing cause_known: {r['name']}"
    # honest split: a real mix of established and not-established causes
    known = sum(1 for r in rows if r.get("cause_known"))
    assert 0 < known < len(rows)
    # renal medullary carcinoma cause is sickle cell trait, not MSI
    rmc = next(r for r in rows if r["name"] == "Renal medullary carcinoma")
    assert "sickle cell" in rmc["causes"].lower()


def test_actionable_drivers_all_cited():
    drivers = analysis.load_actionable()
    assert len(drivers) >= 15
    for g, e in drivers.items():
        assert e["citation"].get("url", "").startswith("http"), f"{g} missing citation"
        assert e["tier"] in (1, 2, 3)


def test_actionable_map_honest_tiers_and_confidence():
    am = analysis.actionable_map()
    assert 40 <= len(am) <= 200
    for a in am:
        # a gene-only translation is never asserted as a tissue-agnostic tier 1 unless the label is
        if not a["tissue_agnostic"]:
            assert a["best_tier"] >= 2, f"{a['name']} overstated as tier 1"
        assert a["confidence"]["pct"] <= 90
        assert a["matches"] and a["matches"][0]["citation"].get("url")
    # tissue-agnostic drivers (BRAF, NTRK, RET, HER2) do reach tier 1 High
    assert any(a["best_tier"] == 1 and a["confidence"]["label"] == "High" for a in am)


def test_actionability_summary_shape():
    s = analysis.actionability_summary()
    assert 0 < s["n_actionable"] < s["n_rare_cancers"]
    assert s["n_tissue_agnostic"] <= s["n_actionable"]
    assert s["top_drugs"]


def test_etiology_landscape_and_syndromes():
    e = analysis.etiology_landscape()
    assert e["Cause not established"]["count"] > 0
    assert e["Infectious"]["count"] > 0 and e["Hereditary syndrome"]["count"] > 0
    syn = analysis.hereditary_syndrome_map()
    names = {s for s, _ in syn}
    assert any("Li-Fraumeni" in n for n in names)
    # every syndrome links at least one real cancer
    assert all(len(cs) >= 1 for _, cs in syn)


def test_druggability_gap_is_honest():
    A = analysis
    gap = {g for g, _ in A.druggability_gap()}
    # genuinely undrugged high-value dependencies are in the gap
    assert {"TP53", "EWSR1", "CTNNB1"} <= gap
    # drivers we do have an approved drug for are NOT counted as unmet
    assert "BRAF" not in gap and "KRAS" not in gap and "ALK" not in gap
    s = A.druggability_summary()
    assert s["n_unmet_shared"] + s["n_druggable_shared"] == s["n_shared_drivers"]
    assert s["top_unmet"] and s["top_unmet"][0][1] >= 5


def test_induced_dependency_map_cited():
    ind = analysis.load_induced()
    assert {"SMARCB1", "ARID1A", "MTAP"} <= set(ind)
    for g, e in ind.items():
        assert e["dependency"] and e["citation"]["url"].startswith("http")
    # SMARCB1 loss induces an EZH2 dependency (the tazemetostat rationale)
    assert analysis.induced_for("SMARCB1")["dependency"] == "EZH2"
