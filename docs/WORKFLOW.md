# Anveshar comp-bio workflow and harness

Anveshar is not only a set of reports. It ships a reproducible, provenance tracked pipeline that
turns a rare cancer into a cited, confidence scored cross condition translation dossier by
chaining local curated knowledge with live biomedical databases. A scientist can run it from
the command line, from Python, or inside Claude Science, and audit every claim to its source.

## The harness

`anveshar/pipeline.py` runs five auditable stages. Each stage appends a provenance record
(source, query, count, note), and the run degrades gracefully with no network.

1. Resolve. Map the condition to its catalog row, driver genes, and cited etiology.
2. Databases (live). Query Open Targets Platform (target to disease associations and known
   drugs, via GraphQL), Ensembl (gene identity), ChEMBL and UniProt (druggable target lookup),
   PubMed (E utilities), and ClinicalTrials.gov (API v2). Offline runs skip this stage and say so.
3. Target validation (live). Pull druggability tractability, DepMap CRISPR gene essentiality,
   and known safety liabilities from Open Targets for each driver, and score a verdict: a
   validated target is tractable and a selective dependency, while a common essential gene is
   flagged for systemic selectivity risk. This is executed functional genomics, not a description.
4. Translate. Cross reference the driver genes with a curated, cited actionable driver map to
   surface borrowable approved therapies, and with the catalog wide shared driver graph to
   surface cross condition candidates (other rare cancers that share the dependency).
5. Assemble. Attach a transparent confidence score to the best therapy (tissue agnostic label
   to High, cross tumor translation to Moderate, mechanistic to Low, minus a penalty when no
   citation is attached), emit the full provenance, and append a health provider disclaimer.

## Tools, databases, and skills it composes

Databases and REST or GraphQL services: Open Targets Platform, Ensembl, ChEMBL, UniProt,
Reactome, PubMed (NCBI E utilities), ClinicalTrials.gov v2, ClinVar. The report layer also
draws on Consensus and Paperclip full text retrieval, and models AdisInsight, Cortellis, Evo 2,
and AlphaMissense as connectors that activate when credentialed.

Skills that extend the pipeline downstream: the deep-research skill for adversarially verified
evidence synthesis, and the clinical-trial-protocol skill for turning a Anveshar discovery
hypothesis into a trial protocol synopsis (see `docs/protocols/`).

Every therapy and hypothesis carries a resolvable citation (PMID, DOI, or NCT), and every
confidence score carries a plain basis string, so nothing is asserted without a source.

## How to run it

Command line, offline (deterministic, no network):

    python3 -m anveshar.cli analyze --cancer "renal medullary carcinoma"

Command line, live (adds Open Targets and PubMed):

    python3 -m anveshar.cli analyze --cancer "gastrointestinal stromal tumor" --live --out gist.json

Python:

    from anveshar.pipeline import run
    dossier = run("anaplastic thyroid carcinoma", live=True)   # BRAF V600E to dabrafenib plus trametinib, tissue agnostic, High confidence

Catalog wide analyses (over all 504 rare cancers):

    from anveshar import analysis
    analysis.actionability_summary()      # how many rare cancers have a borrowable approved therapy
    analysis.catalog_shared_drivers()     # dependencies shared across cancers (the translation map)
    analysis.etiology_landscape()         # causes grouped as infectious, environmental, hereditary, precursor, or not established
    analysis.hereditary_syndrome_map()    # inherited syndromes to the rare cancers they cause

Render a full cited report for a curated condition:

    python3 -m anveshar.cli run --cancer "renal medullary carcinoma" --out report.html

## Reproducibility

Offline runs are deterministic and fully covered by the test suite (`tests/test_pipeline.py`,
`tests/test_analysis.py`). Live runs record every database query in the provenance list so a
result can be traced and rerun. The pipeline never raises on a network failure; a missing
database degrades to an empty result with a provenance note rather than a fabricated value.

## Disclaimer

This workflow produces research and educational decision support, not medical advice. A gene
level driver match is a translation hypothesis, not a guarantee that a specific variant is drug
sensitive. Confidence scores summarize evidence strength, not the probability of benefit for an
individual patient. Every diagnostic and treatment decision must be made by a qualified health
care provider, ideally within a clinical trial.

Developer: [digvijayky](https://digvijayky.com)
