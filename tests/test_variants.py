"""Offline tests for anveshar.variants (no network).

Exercises classify, grade, reclassify, and interpret_profile, including both real
example profiles in examples/profiles/. All data is local; nothing here calls out
to a network service.
"""
import json
import os

from anveshar.schema import (
    VariantClass, Alteration, Actionability, PatientProfile,
)
from anveshar.variants import classify, grade, reclassify, interpret_profile

HERE = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(HERE, "..", "examples", "profiles")


def _load(name):
    with open(os.path.join(PROFILE_DIR, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


# ----------------------------- classify -----------------------------

def test_classify_explicit_report_schema_labels():
    assert classify({"cls": "SNV, hotspot"}) == VariantClass.SNV
    assert classify({"cls": "Composite biomarker"}) == VariantClass.COMPOSITE
    assert classify({"cls": "Epigenetic silencing"}) == VariantClass.EPIGENETIC
    assert classify({"cls": "VUS workflow"}) == VariantClass.VUS


def test_classify_rich_agent_schema_class_field():
    assert classify({"class": "fusion"}) == VariantClass.FUSION
    assert classify({"class": "amplification"}) == VariantClass.AMPLIFICATION


def test_classify_from_free_text():
    assert classify({"gene": "NTRK1", "variant": "NTRK1-ETV6 fusion"}) == VariantClass.FUSION
    assert classify({"gene": "ERBB2", "variant": "amplification"}) == VariantClass.AMPLIFICATION
    assert classify({"gene": "MET", "variant": "exon 14 skipping"}) == VariantClass.SPLICE
    assert classify({"gene": "MLH1", "variant": "promoter hypermethylation"}) == VariantClass.EPIGENETIC
    assert classify({"gene": "CDKN2A", "variant": "deep deletion"}) == VariantClass.DELETION
    assert classify({"biomarker": "MSI-H / dMMR"}) == VariantClass.COMPOSITE
    assert classify({"biomarker": "TMB-high"}) == VariantClass.COMPOSITE
    assert classify({"gene": "SSTR2", "variant": "overexpression"}) == VariantClass.EXPRESSION
    assert classify({"gene": "BRAF", "variant": "rare missense of uncertain significance"}) == VariantClass.VUS


def test_classify_defaults_to_snv():
    assert classify({"gene": "BRAF", "variant": "V600E"}) == VariantClass.SNV


# ----------------------------- grade -----------------------------

def test_grade_braf_v600e_is_tier_i_level_1():
    a = grade("BRAF", "V600E")
    assert a.oncokb_level == "Level 1"
    assert a.amp_asco_cap == "Tier I"
    assert a.escat.startswith("I")
    assert "35662396" in a.note or "31566309" in a.note  # real PMIDs present


def test_grade_msi_high_is_tumor_agnostic_level_1():
    a = grade("", "", "MSI-H / dMMR")
    assert a.oncokb_level == "Level 1"
    assert a.amp_asco_cap == "Tier I"
    assert a.escat == "I-C"
    assert "31682550" in a.note  # KEYNOTE-158 PMID


def test_grade_known_targets():
    assert grade("KRAS", "G12C").oncokb_level == "Level 1"
    assert grade("MET", "exon 14 skipping").oncokb_level == "Level 1"
    assert grade("NTRK1", "NTRK1 fusion").escat == "I-C"
    assert grade("ERBB2", "amplification").oncokb_level == "Level 1"
    assert grade("IDH1", "R132H").oncokb_level == "Level 1"
    assert grade("", "", "TMB-high").oncokb_level == "Level 1"


def test_grade_unknown_returns_empty_never_guesses():
    a = grade("ZZZ9", "p.Q999Q")
    assert a.oncokb_level == "" and a.amp_asco_cap == "" and a.escat == "" and a.note == ""


# ----------------------------- reclassify (VUS) -----------------------------

def test_reclassify_vus_stays_unverified_and_untiered():
    vus = Alteration(gene="BRAF", variant_class=VariantClass.VUS,
                     variant="p.Gly466Val", consequence="missense")
    out = reclassify(vus)
    assert out.verified is False
    assert out.actionability.oncokb_level == ""
    assert out.actionability.amp_asco_cap == ""
    assert out.actionability.escat == ""
    assert "AlphaMissense" in out.interpretation
    assert "37733863" in out.interpretation  # AlphaMissense PMID


def test_reclassify_splice_vus_routes_to_evo2():
    vus = Alteration(gene="MET", variant_class=VariantClass.VUS,
                     variant="c.3028+1G>A", consequence="splice region variant")
    out = reclassify(vus)
    assert out.verified is False
    assert "Evo 2" in out.interpretation
    assert "41781614" in out.interpretation  # Evo 2 Nature PMID


def test_reclassify_non_vus_is_unchanged():
    snv = Alteration(gene="BRAF", variant_class=VariantClass.SNV, variant="V600E",
                     verified=True)
    out = reclassify(snv)
    assert out is snv or (out.verified is True and out.variant_class == VariantClass.SNV)


class _FakeUnavailableClient:
    """Offline stand in for WorkbenchClient whose model connectors are unavailable."""
    def alphamissense(self, protein_change):
        return {"available": False}

    def evo2(self, hgvs):
        return {"available": False}


def test_reclassify_with_unavailable_client_asserts_no_number():
    vus = Alteration(gene="BRAF", variant_class=VariantClass.VUS,
                     variant="p.Gly466Val", consequence="missense")
    out = reclassify(vus, client=_FakeUnavailableClient())
    assert out.verified is False
    assert "no numeric prediction" in out.interpretation.lower()


# ----------------------------- interpret_profile -----------------------------

def test_interpret_pereira_profile_msi_braf():
    raw = _load("pereira_msi_braf.json")
    prof = interpret_profile(raw)
    assert isinstance(prof, PatientProfile)
    assert prof.present is True
    assert "36840617" in prof.source.url or "36840617" in prof.source.label
    assert len(prof.alterations) == len(raw["alterations"])

    by_gene = {a.gene: a for a in prof.alterations}

    # BRAF V600E grades to Tier I / Level 1.
    braf = by_gene["BRAF"]
    assert braf.variant_class == VariantClass.SNV
    assert braf.actionability.oncokb_level == "Level 1"
    assert braf.actionability.amp_asco_cap == "Tier I"

    # The composite MSI-H / dMMR biomarker grades to tumor agnostic Level 1.
    comp = [a for a in prof.alterations if a.variant_class == VariantClass.COMPOSITE]
    assert comp, "expected a composite MSI-H / dMMR alteration"
    assert comp[0].actionability.oncokb_level == "Level 1"
    assert comp[0].actionability.escat == "I-C"

    # The MLH1 loss is epigenetic silencing.
    assert by_gene["MLH1"].variant_class == VariantClass.EPIGENETIC

    # The illustrative VUS stays unverified and carries no clinical tier.
    vus = [a for a in prof.alterations if a.variant_class == VariantClass.VUS]
    assert vus, "expected the illustrative VUS alteration"
    assert vus[0].verified is False
    assert vus[0].actionability.oncokb_level == ""
    assert vus[0].actionability.amp_asco_cap == ""


def test_interpret_klempner_profile_braf_only():
    raw = _load("klempner_braf.json")
    prof = interpret_profile(raw)
    assert prof.present is True
    assert "27048246" in prof.source.url or "27048246" in prof.source.label
    assert len(prof.alterations) == 1

    braf = prof.alterations[0]
    assert braf.gene == "BRAF"
    assert braf.variant_class == VariantClass.SNV
    assert braf.actionability.oncokb_level == "Level 1"
    assert braf.actionability.amp_asco_cap == "Tier I"
    assert braf.actionability.escat.startswith("I")

    # Excluded targets are carried through verbatim.
    excluded_targets = {e["target"] for e in prof.excluded}
    assert "MSI-H / dMMR" in excluded_targets
    assert "High TMB" in excluded_targets


def test_interpret_tolerates_rich_agent_schema():
    """The rich agent alteration shape parses too (class, nested actionability, notes)."""
    raw = {
        "present": True,
        "source": {"label": "synthetic", "url": ""},
        "alterations": [
            {
                "gene": "BRAF",
                "class": "SNV, hotspot",
                "variant": "V600E",
                "consequence": "missense",
                "biomarker": "",
                "actionability": {"oncokb_level": "Level 1", "amp_asco_cap": "Tier I",
                                  "escat": "I-A", "note": "prior grade"},
                "maps_to_target": "BRAF V600E",
                "interpretation_note": "activating MAPK driver",
            }
        ],
    }
    prof = interpret_profile(raw)
    assert len(prof.alterations) == 1
    a = prof.alterations[0]
    assert a.variant_class == VariantClass.SNV
    assert a.target == "BRAF V600E"
    assert a.interpretation == "activating MAPK driver"
    # Curated grade is Level 1 / Tier I.
    assert a.actionability.oncokb_level == "Level 1"
    assert a.actionability.amp_asco_cap == "Tier I"


# ----------------------------- no dashes anywhere -----------------------------

def test_no_em_or_en_dashes_in_outputs():
    from anveshar.schema import assert_no_dashes
    for name in ("pereira_msi_braf.json", "klempner_braf.json"):
        prof = interpret_profile(_load(name))
        # Validate the fields this module produces (not the raw example prose,
        # which may legitimately contain punctuation from the source paper).
        for a in prof.alterations:
            assert_no_dashes({
                "action_note": a.actionability.note,
                "oncokb": a.actionability.oncokb_level,
                "amp": a.actionability.amp_asco_cap,
                "escat": a.actionability.escat,
            })
    # The reclassify rationale must also be dash free.
    vus = Alteration(gene="MET", variant_class=VariantClass.VUS,
                     variant="c.3028+1G>A", consequence="splice region variant")
    assert_no_dashes({"interp": reclassify(vus).interpretation})
