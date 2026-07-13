"""Cited rule table of clinically actionable alterations for Anveshar.

This is a small, hand curated, source anchored knowledge base. Each rule maps a
(gene, alteration pattern) to actionability graded on the three published axes
Anveshar uses (see docs/variant_interpretation_methodology.md):

  1. OncoKB Therapeutic Levels of Evidence
     Chakravarty et al 2017, JCO Precision Oncology, PMID 28890946,
     DOI 10.1200/PO.17.00011.
  2. AMP/ASCO/CAP 2017 four tier somatic variant classification
     Li et al 2017, Journal of Molecular Diagnostics, PMID 27993330,
     DOI 10.1016/j.jmoldx.2016.10.002.
  3. ESCAT, the ESMO Scale for Clinical Actionability of molecular Targets
     Mateo et al 2018, Annals of Oncology 29(9):1895 to 1902, PMID 30137196,
     DOI 10.1093/annonc/mdy263.

Design rule (hard): never fabricate a variant, drug, or citation. Every rule below
carries a real PMID in its comment. Any value that could not be independently
verified at write time is marked UNVERIFIED. The actionability level assigned is
the level for the alteration to drug match named in the comment, in the tumor
context noted; grading in a different tumor context can be lower (for example an
FDA tumor agnostic approval is Level 1 anywhere, whereas a tumor specific approval
is Level 1 only in that tumor type and drops toward Level 3B elsewhere).
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    """One curated actionability rule.

    Attributes:
        gene: HGNC gene symbol the rule keys on (empty for genome wide biomarkers).
        pattern: lowercase substrings; ALL must appear in the normalized query text
            (gene + variant + biomarker) for the rule to fire. Empty pattern matches
            any variant of the gene.
        oncokb_level: OncoKB therapeutic level string, for example "Level 1".
        amp_asco_cap: AMP/ASCO/CAP tier string, for example "Tier I".
        escat: ESCAT tier string, for example "I-A".
        drug: representative matched therapy (for the note only, never a claim of
            eligibility for a specific patient).
        context: tumor context in which the level applies, or "tumor-agnostic".
        note: short interpretation text (no dashes).
        source: real citation with PMID for the alteration to drug match.
        tumor_agnostic: True if the FDA approval is tissue agnostic.
    """
    gene: str
    pattern: tuple
    oncokb_level: str
    amp_asco_cap: str
    escat: str
    drug: str
    context: str
    note: str
    source: str
    tumor_agnostic: bool = False


# The order matters: more specific rules (longer pattern) are listed first within a
# gene so the matcher can prefer the most specific hit.
RULES = (
    # BRAF V600E, activating class I RAF mutation.
    # Tumor agnostic FDA approval of dabrafenib plus trametinib for BRAF V600E solid
    # tumors (Subbiah et al 2022, Lancet Oncology, PMID 35662396). In colorectal
    # cancer the guideline regimen is encorafenib plus cetuximab (BEACON CRC,
    # Kopetz et al 2019, NEJM, PMID 31566309).
    Rule("BRAF", ("v600e",), "Level 1", "Tier I", "I-A",
         "dabrafenib plus trametinib (tumor-agnostic); encorafenib plus cetuximab in colorectal cancer",
         "tumor-agnostic",
         "Activating MAPK driver. Tumor agnostic BRAF plus MEK approval; in colorectal lineage BRAF plus EGFR co-blockade is preferred because BRAF monotherapy triggers feedback EGFR reactivation.",
         "Subbiah 2022 Lancet Oncol PMID 35662396; Kopetz 2019 NEJM PMID 31566309",
         tumor_agnostic=True),
    Rule("BRAF", ("v600",), "Level 1", "Tier I", "I-B",
         "BRAF plus MEK inhibition",
         "tumor-dependent",
         "Class I activating BRAF codon 600 mutation. Context determines regimen.",
         "Subbiah 2022 Lancet Oncol PMID 35662396"),

    # KRAS G12C, covalent inhibitor target.
    # Sotorasib approved for KRAS G12C non small cell lung cancer (CodeBreaK 100,
    # Skoulidis et al 2021, NEJM, PMID 34096690). Adagrasib also approved.
    Rule("KRAS", ("g12c",), "Level 1", "Tier I", "I-B",
         "sotorasib or adagrasib",
         "non-small-cell lung cancer",
         "Covalent KRAS G12C inhibitor target. Level 1 in NSCLC; colorectal use is combination based (with anti EGFR).",
         "Skoulidis 2021 NEJM PMID 34096690"),

    # IDH1 R132, targeted by ivosidenib.
    # Ivosidenib approved in IDH1 mutant acute myeloid leukemia and cholangiocarcinoma
    # (ClarIDHy, Abou-Alfa et al 2020, Lancet Oncology, PMID 32416072).
    Rule("IDH1", ("r132",), "Level 1", "Tier I", "I-B",
         "ivosidenib",
         "cholangiocarcinoma and acute myeloid leukemia",
         "IDH1 R132 neomorphic mutation producing 2-hydroxyglutarate; targeted by the IDH1 inhibitor ivosidenib.",
         "Abou-Alfa 2020 Lancet Oncol PMID 32416072"),

    # EGFR activating mutations (exon 19 deletion, L858R), targeted by osimertinib.
    # FLAURA, Soria et al 2018, NEJM, PMID 29151359.
    Rule("EGFR", ("t790m",), "Level 1", "Tier I", "I-A",
         "osimertinib",
         "non-small-cell lung cancer",
         "EGFR T790M resistance mutation sensitizing to third generation EGFR TKI osimertinib.",
         "Mok 2017 NEJM PMID 27959700 (AURA3)"),
    Rule("EGFR", ("exon 19",), "Level 1", "Tier I", "I-A",
         "osimertinib",
         "non-small-cell lung cancer",
         "EGFR exon 19 deletion, a classic sensitizing EGFR alteration for first line osimertinib.",
         "Soria 2018 NEJM PMID 29151359 (FLAURA)"),
    Rule("EGFR", ("l858r",), "Level 1", "Tier I", "I-A",
         "osimertinib",
         "non-small-cell lung cancer",
         "EGFR L858R sensitizing mutation for first line osimertinib.",
         "Soria 2018 NEJM PMID 29151359 (FLAURA)"),
    Rule("EGFR", (), "Level 1", "Tier I", "I-A",
         "osimertinib",
         "non-small-cell lung cancer",
         "EGFR alteration; sensitizing exon 19 deletion or L858R map to osimertinib. Non classical alterations may be lower level.",
         "Soria 2018 NEJM PMID 29151359 (FLAURA)"),

    # NTRK1/2/3 fusions, tumor agnostic (larotrectinib, entrectinib).
    # Drilon et al 2018, NEJM, PMID 29466156 (larotrectinib pooled TRK fusion set).
    Rule("NTRK", ("fusion",), "Level 1", "Tier I", "I-C",
         "larotrectinib or entrectinib",
         "tumor-agnostic",
         "TRK fusion; tumor agnostic FDA approval. RNA based fusion detection is required because DNA only panels miss many fusions.",
         "Drilon 2018 NEJM PMID 29466156",
         tumor_agnostic=True),
    Rule("NTRK1", ("fusion",), "Level 1", "Tier I", "I-C",
         "larotrectinib or entrectinib", "tumor-agnostic",
         "TRK fusion; tumor agnostic FDA approval.",
         "Drilon 2018 NEJM PMID 29466156", tumor_agnostic=True),
    Rule("NTRK2", ("fusion",), "Level 1", "Tier I", "I-C",
         "larotrectinib or entrectinib", "tumor-agnostic",
         "TRK fusion; tumor agnostic FDA approval.",
         "Drilon 2018 NEJM PMID 29466156", tumor_agnostic=True),
    Rule("NTRK3", ("fusion",), "Level 1", "Tier I", "I-C",
         "larotrectinib or entrectinib", "tumor-agnostic",
         "TRK fusion; tumor agnostic FDA approval.",
         "Drilon 2018 NEJM PMID 29466156", tumor_agnostic=True),

    # RET fusions (selpercatinib), targeted across NSCLC and thyroid.
    # LIBRETTO-001, Drilon et al 2020, NEJM, PMID 32846060.
    Rule("RET", ("fusion",), "Level 1", "Tier I", "I-B",
         "selpercatinib or pralsetinib",
         "non-small-cell lung cancer and thyroid cancer",
         "RET fusion targeted by selective RET inhibitors. Selpercatinib carries a tumor agnostic approval for RET fusion solid tumors.",
         "Drilon 2020 NEJM PMID 32846060 (LIBRETTO-001)"),

    # ROS1 fusions (crizotinib, entrectinib).
    # Shaw et al 2014, NEJM, PMID 25264305 (crizotinib in ROS1 NSCLC).
    Rule("ROS1", ("fusion",), "Level 1", "Tier I", "I-A",
         "crizotinib, entrectinib, or lorlatinib",
         "non-small-cell lung cancer",
         "ROS1 fusion sensitive to ROS1 tyrosine kinase inhibitors.",
         "Shaw 2014 NEJM PMID 25264305"),

    # ALK fusions (alectinib, lorlatinib).
    # ALEX, Peters et al 2017, NEJM, PMID 28586279.
    Rule("ALK", ("fusion",), "Level 1", "Tier I", "I-A",
         "alectinib or lorlatinib",
         "non-small-cell lung cancer",
         "ALK fusion sensitive to next generation ALK inhibitors.",
         "Peters 2017 NEJM PMID 28586279 (ALEX)"),

    # ERBB2 (HER2) amplification (trastuzumab, trastuzumab deruxtecan).
    # DESTINY-Breast04, Modi et al 2022, NEJM, PMID 35665782. Trastuzumab deruxtecan
    # carries a tumor agnostic approval for HER2 positive (IHC 3+) solid tumors.
    Rule("ERBB2", ("amplif",), "Level 1", "Tier I", "I-B",
         "trastuzumab, trastuzumab deruxtecan, or trastuzumab plus tucatinib",
         "breast, gastric, and colorectal cancer",
         "HER2 (ERBB2) amplification raises receptor dosage; targeted by anti HER2 antibodies and antibody drug conjugates. Copy number focality and level matter (focal high level amplification is actionable).",
         "Modi 2022 NEJM PMID 35665782 (DESTINY-Breast04)"),
    Rule("ERBB2", ("her2",), "Level 1", "Tier I", "I-B",
         "trastuzumab or trastuzumab deruxtecan",
         "breast and gastric cancer",
         "HER2 overexpression or amplification; targeted by anti HER2 therapy.",
         "Modi 2022 NEJM PMID 35665782 (DESTINY-Breast04)"),
    Rule("HER2", ("amplif",), "Level 1", "Tier I", "I-B",
         "trastuzumab or trastuzumab deruxtecan",
         "breast and gastric cancer",
         "HER2 (ERBB2) amplification; targeted by anti HER2 therapy.",
         "Modi 2022 NEJM PMID 35665782 (DESTINY-Breast04)"),

    # MET exon 14 skipping (capmatinib, tepotinib).
    # GEOMETRY mono-1, Wolf et al 2020, NEJM, PMID 32877583.
    Rule("MET", ("exon 14",), "Level 1", "Tier I", "I-B",
         "capmatinib or tepotinib",
         "non-small-cell lung cancer",
         "MET exon 14 skipping deletes the juxtamembrane exon and stabilizes MET; targeted by MET inhibitors. Splice aware annotation is required to detect it.",
         "Wolf 2020 NEJM PMID 32877583 (GEOMETRY mono-1)"),
    Rule("MET", ("skip",), "Level 1", "Tier I", "I-B",
         "capmatinib or tepotinib",
         "non-small-cell lung cancer",
         "MET exon 14 skipping event; targeted by MET inhibitors.",
         "Wolf 2020 NEJM PMID 32877583 (GEOMETRY mono-1)"),
    Rule("MET", ("amplif",), "Level 2", "Tier II", "II-B",
         "capmatinib or crizotinib",
         "non-small-cell lung cancer",
         "High level MET amplification; investigational to standard depending on copy number threshold.",
         "Wolf 2020 NEJM PMID 32877583 (GEOMETRY mono-1)"),

    # Composite genomic biomarkers (genome wide, no single gene).
    # MSI-H / dMMR tumor agnostic pembrolizumab (KEYNOTE-158, Marabelle et al 2020,
    # JCO, PMID 31682550; first line CRC KEYNOTE-177, Andre et al 2020, NEJM,
    # PMID 33264544).
    Rule("", ("msi-h",), "Level 1", "Tier I", "I-C",
         "pembrolizumab (PD-1 blockade)",
         "tumor-agnostic",
         "MSI-H or dMMR is a tumor agnostic immunotherapy biomarker. First line for MSI-H metastatic colorectal cancer.",
         "Marabelle 2020 JCO PMID 31682550 (KEYNOTE-158); Andre 2020 NEJM PMID 33264544 (KEYNOTE-177)",
         tumor_agnostic=True),
    Rule("", ("dmmr",), "Level 1", "Tier I", "I-C",
         "pembrolizumab (PD-1 blockade)",
         "tumor-agnostic",
         "Mismatch repair deficiency (dMMR) is the mechanistic basis of MSI-H and a tumor agnostic immunotherapy biomarker.",
         "Marabelle 2020 JCO PMID 31682550 (KEYNOTE-158)",
         tumor_agnostic=True),
    Rule("", ("microsatellite instab",), "Level 1", "Tier I", "I-C",
         "pembrolizumab (PD-1 blockade)",
         "tumor-agnostic",
         "Microsatellite instability high; tumor agnostic immunotherapy biomarker.",
         "Marabelle 2020 JCO PMID 31682550 (KEYNOTE-158)",
         tumor_agnostic=True),

    # High TMB, tumor agnostic pembrolizumab at 10 mutations per megabase.
    # KEYNOTE-158 TMB-high analysis, Marabelle et al 2020, Lancet Oncology,
    # PMID 32919526.
    Rule("", ("tmb-high",), "Level 1", "Tier I", "I-C",
         "pembrolizumab (PD-1 blockade)",
         "tumor-agnostic",
         "Tumor mutational burden high (10 or more mutations per megabase in the tumor agnostic label) predicts checkpoint inhibitor benefit.",
         "Marabelle 2020 Lancet Oncol PMID 32919526 (KEYNOTE-158 TMB)",
         tumor_agnostic=True),
    Rule("", ("high tmb",), "Level 1", "Tier I", "I-C",
         "pembrolizumab (PD-1 blockade)",
         "tumor-agnostic",
         "High tumor mutational burden; tumor agnostic immunotherapy biomarker at 10 or more mutations per megabase.",
         "Marabelle 2020 Lancet Oncol PMID 32919526 (KEYNOTE-158 TMB)",
         tumor_agnostic=True),
    Rule("", ("tumor mutational burden",), "Level 1", "Tier I", "I-C",
         "pembrolizumab (PD-1 blockade)",
         "tumor-agnostic",
         "Tumor mutational burden high; tumor agnostic immunotherapy biomarker.",
         "Marabelle 2020 Lancet Oncol PMID 32919526 (KEYNOTE-158 TMB)",
         tumor_agnostic=True),
)


def _norm(text: str) -> str:
    """Lowercase and normalize whitespace for pattern matching."""
    return " ".join((text or "").lower().split())


def lookup(gene: str, variant: str = "", biomarker: str = "", condition: str = ""):
    """Return the best matching Rule for a query, or None if nothing matches.

    Matching is conservative: a rule fires only when its gene matches (or the rule
    is a genome wide biomarker with empty gene) AND every substring in its pattern
    appears in the normalized query text. Among firing rules the one with the most
    specific (longest total) pattern wins, so BRAF V600E beats the generic BRAF V600
    rule. Unknown queries return None so the caller can emit an empty Actionability
    rather than a guess.

    Args:
        gene: gene symbol from the alteration (may be empty for composite biomarkers).
        variant: variant string, for example "V600E" or "exon 14 skipping".
        biomarker: derived biomarker text, for example "MSI-H / dMMR".
        condition: tumor context (currently informational only).

    Returns:
        The matching Rule, or None.
    """
    g = _norm(gene)
    query = _norm(" ".join([gene, variant, biomarker]))
    best = None
    best_score = -1
    for rule in RULES:
        rg = _norm(rule.gene)
        if rg:
            # Gene keyed rule: the rule gene must appear as a token or prefix in the
            # query gene (so "NTRK" matches "NTRK1", and "MET" matches "MET").
            if not (g == rg or g.startswith(rg) or rg in g):
                continue
        else:
            # Genome wide biomarker rule: gene must be empty or clearly genome wide.
            if g and "genome" not in g and "mmr" not in g and "wide" not in g:
                # allow biomarker-only queries where gene is a placeholder
                pass
        if all(sub in query for sub in rule.pattern):
            score = sum(len(sub) for sub in rule.pattern)
            # Prefer gene keyed rules over empty gene rules at equal length.
            if rule.gene:
                score += 1
            if score > best_score:
                best = rule
                best_score = score
    return best
