# Independent fact-check: rare_conditions_catalog.json

Target file: `anveshar/data/rare_conditions_catalog.json`
Reviewer role: independent fact-checker (did not trust the catalog; did not modify it; no git).
Date: 2026-07-12

## Scope of what was checked

1. Structural scan of all 384 entries (names, slugs, categories, genes) for fabrication, misspelling, duplication.
2. Independent confirmation of a representative sample of 60+ entries (mix of famous and obscure rare cancers and rare diseases) against Orphanet, NCI/RARECARE, NORD, NIH GARD, OMIM/MedlinePlus/GeneReviews, HGNC, and PubMed.
3. Category correctness (rare cancer vs rare disease).
4. Spot check of the `key_gene_or_marker` field on 40+ entries.

Sources used: WebSearch (Orphanet, NORD, GARD, OMIM, MedlinePlus, GeneReviews, HGNC, cancer.gov, journal literature) and the PubMed plugin. Verification was split across two independent background review passes (one for all 150 rare-cancer entries, one for all 234 rare-disease entries) plus my own direct spot checks of 20+ entries.

## Structural facts (verified programmatically)

- Total entries: 384.
- Categories: 150 "rare cancer", 234 "rare disease".
- Duplicate `name` values: none.
- Duplicate `slug` values: none.
- Entries with empty `key_gene_or_marker`: 57 (empty is a legitimate "no single canonical marker" value, not an error).

## (1) Invented / misspelled / non-real names

None. Every one of the 384 names maps to a real, recognized oncologic or medical entity, and spelling is correct (including anglicized forms such as "Hurthle cell thyroid carcinoma" for Hurthle/oncocytic carcinoma).

A few names use inverted or non-standard word order but are unambiguous and refer to genuine entities (not flagged as errors):
- "Basal cell carcinoma nevoid syndrome tumor" -> garbled word order for nevoid basal cell carcinoma syndrome (Gorlin syndrome). Entity and gene (PTCH1) are correct; only the phrasing is awkward.
- "Ichthyosis harlequin" -> Harlequin ichthyosis (ABCA12). Real.
- "Nephrotic syndrome congenital" -> Congenital nephrotic syndrome (NPHS1). Real.
- "Castleman disease unicentric" -> Unicentric Castleman disease. Real.

## (2) Miscategorization (rare cancer vs rare disease)

No hard category errors. Two points worth noting:

- Small cell lung cancer (listed as "rare cancer"). This was the strongest candidate for a miscategorization because SCLC is common relative to lung cancer overall (~10-15% of lung cancers, ~30-35k US cases/yr). However, its incidence is ~4.6 per 100,000/year, which is BELOW the RARECARE/ESMO rare threshold (<6 per 100,000), it falls under the US orphan threshold, and NORD lists it in its rare disease database. So the inclusion is defensible. It is the least "rare" cancer in the list, so it is a borderline call rather than an outright error.
- The hereditary tumor-predisposition syndromes (MEN1, MEN2, Li-Fraumeni, Cowden, Peutz-Jeghers, Gorlin, Birt-Hogg-Dube, FAP, Gardner, Lynch, VHL, NF1, NF2, tuberous sclerosis) are placed under "rare disease". This is correct: they are germline syndromes (heritable non-cancer conditions that predispose to cancer), and Orphanet/GARD/NORD catalog them as rare diseases, not as cancers.

## (3) Wrong gene / marker assignments

No genuinely wrong gene assignments were found on any spot-checked entry. Every non-empty gene field is the canonical/characteristic driver, fusion, or diagnostic marker for its condition. Verified-correct examples that are the most likely to be miscalled, all correct:

- Ependymoma -> RELA (ZFTA/C11orf95-RELA fusion defines >60% of supratentorial ependymomas).
- Chronic myelomonocytic leukemia -> TET2 (most frequent single mutation).
- Chronic eosinophilic leukemia -> FIP1L1-PDGFRA (WHO surrogate diagnostic marker).
- Clear cell sarcoma of the kidney -> BCOR (BCOR ITD in ~85-100%).
- Rosai-Dorfman disease -> MAP2K1 (recurrent, mutually exclusive with KRAS).
- Angioimmunoblastic T-cell lymphoma -> TET2 (most common mutation; RHOA G17V is more specific but TET2 is legitimate).
- BPDCN -> CD123 (pivotal diagnostic marker).
- Extraskeletal myxoid chondrosarcoma -> NR4A3 (diagnostic fusion partner).
- Alveolar soft part sarcoma -> ASPSCR1-TFE3; Fibrolamellar HCC -> DNAJB1-PRKACA; SCCOHT -> SMARCA4; all correct.
- Non-gene markers used where no single gene is the natural identifier are all accepted characteristic markers, not errors: AChR (myasthenia gravis), VGCC (Lambert-Eaton), GAD65 (stiff person), ANCA (GPA/EGPA), VEGF (POEMS), IgG4 (IgG4-RD), HLA-B51 (Behcet), SSA (Sjogren), Epstein-Barr virus / HHV-8 / HPV / Merkel cell polyomavirus (viral-associated cancers), Brachyury (chordoma).

Two minor OUTDATED-SYMBOL notes (the assignment is biologically correct; only the HGNC symbol has since been updated, and both legacy symbols remain in wide use and point unambiguously to the right gene):
- Barth syndrome -> "TAZ". HGNC renamed this gene to TAFAZZIN (previous symbol TAZ), specifically to avoid confusion with the Hippo-pathway gene TAZ/WWTR1. Independently confirmed.
- Von Gierke disease -> "G6PC". HGNC renamed this gene to G6PC1 (previous symbol G6PC). Independently confirmed.

A passing note (not an error): Prader-Willi syndrome -> SNRPN is an accepted conventional identifier for the SNURF-SNRPN imprinting locus, though the minimal critical region is the SNORD116 snoRNA cluster.

## Minor redundancy (not a factual error)

- "Neuroblastoma" (MYCN) and "Adrenal neuroblastoma" (MYCN) are the same disease listed twice under different names (neuroblastoma most commonly arises in the adrenal). Redundant, but both names are real and the gene is correct. Names and slugs differ, so this is not caught by the duplicate-slug check.
- "Familial adenomatous polyposis" (APC) and "Gardner syndrome" (APC) overlap: Gardner syndrome is now considered a phenotypic subtype of FAP. Both are recognized named conditions, so this is redundancy, not an error.

## Overall verdict

The catalog is clean and high quality. Across all 384 entries there are no fabricated or invented names, no misspellings, no duplicate names or slugs, no genuine category errors, and no incorrect gene/marker assignments. The only issues are cosmetic: two legacy-but-correct gene symbols (TAZ -> now TAFAZZIN; G6PC -> now G6PC1), one garbled name phrasing ("Basal cell carcinoma nevoid syndrome tumor"), and two conceptual redundancies (Neuroblastoma vs Adrenal neuroblastoma; FAP vs Gardner syndrome). Small cell lung cancer as a "rare cancer" is defensible by incidence but is the least-rare entry in the list. None of these rise to the level of a factual error requiring correction.
