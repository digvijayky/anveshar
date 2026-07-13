# Anveshar: a translational molecular board for rare cancers

Built with Claude, Life Sciences Hackathon 2026.

## The problem

A rare cancer rarely gets its own clinical trial, so the patients who need answers most
are served by the evidence base least. Yet oncology increasingly approves drugs by a
tumor's molecular marker rather than where it started: pembrolizumab for any MSI-high
tumor, larotrectinib for any NTRK fusion, dabrafenib plus trametinib for any BRAF V600E
solid tumor. For a rare cancer, borrowing a proven therapy across tumor types is often
the best available option, and today that reasoning happens by hand, if at all.

## What Anveshar does

Given a rare cancer, and optionally a patient's own molecular profile, Anveshar:

1. characterizes the cancer from primary literature,
2. interprets the patient's variants and expression across every variant class, graded
   by OncoKB, AMP/ASCO/CAP, and ESCAT,
3. translates each target to therapies validated in other cancers, anchored on
   tissue-agnostic FDA precedent,
4. matches open trials, favoring basket designs,
5. grades and personalizes: every option is tiered and cited, and the patient's own
   alterations promote what applies to them while honestly excluding what does not.

Every therapy claim links to a real PMID, DOI, or NCT. Where a claim cannot be verified,
Anveshar marks it unverified rather than inventing one. It never emits an em dash and never
fabricates a variant, drug, or trial.

## What is novel

Anveshar is a discovery engine, not a lookup table. Its discovery layer reasons over shared
molecular dependencies to generate hypotheses that no dedicated trial has yet tested in the
target cancer, each with a mechanistic rationale, a transferability grade, and a falsifiable
prediction, kept visually and semantically separate from approved options.

It reasons across therapy modalities, not just small molecules: it flags cell therapy for
lineage antigens such as DLL3, radioligand therapy for receptor positive disease, antisense
oligonucleotides for splice lesions, and gene directed strategies (gene replacement, base
and prime editing, synthetic lethality) for loss of function drivers.

The same lesion to mechanism to cross-condition therapy abstraction generalizes beyond
cancer to the roughly 7,000 rare Mendelian diseases, where borrowing across mechanistically
related conditions and gene directed modalities are often the only realistic path. The
engine is condition agnostic; only the knowledge bases change.

## Live demonstrations

The hub links eighteen cited condition reports (ten rare cancers, eight rare diseases), an
interactive shared-dependency network, and the codebase:

    Hub:                 https://claude.ai/code/artifact/21b36179-57ef-416b-840d-9937c86ddb54
    Dependency network:  https://claude.ai/code/artifact/b1d576d4-88e2-423a-bb77-d7490e822cb2

- Rectal neuroendocrine tumor: the cross-cancer translation engine end to end.
- Renal medullary carcinoma: a SMARCB1 cancer with no tissue-agnostic option, where
  Anveshar shows disciplined restraint and proposes novel hypotheses to test instead.
- A real BRAF V600E rectal case: the mutation promotes the matched Tier 1 therapy while
  immunotherapy is correctly excluded on MSI-stable status.
- A sophisticated four-class case: an MSI-high, BRAF mutant tumor read across an SNV, an
  epigenetic MLH1 silencing event, a composite biomarker, and a VUS reclassification workflow.

## The codebase

Anveshar is an installable Python package with unit tests:

    anveshar/schema.py         canonical types (variant classes, tiers, modalities, discovery)
    anveshar/engine.py         the five stage pipeline
    anveshar/evidence/         PubMed, ClinicalTrials, ClinVar, and Claude Science Workbench connectors
    anveshar/variants/         classes, actionability frameworks, VUS reclassification, interpret
    anveshar/translation/      cross-condition engine, tissue-agnostic knowledge, discovery layer
    anveshar/expression/       scRNA-seq druggable target extractor
    anveshar/report/           HTML report template and renderer

Run it:

    pip install -e ".[scrna,live]"
    anveshar list
    anveshar run --cancer "renal medullary carcinoma" --discovery --out report.html
    anveshar run --cancer "rectal neuroendocrine tumor" --profile examples/profiles/pereira_msi_braf.json --out report.html
    anveshar run --cancer "a condition with no curated file" --live   # assembled via the Claude API

## Built on Claude Science

Anveshar maps onto the Claude Science / AI Workbench idea of a research environment wired to
curated databases: PubMed and preprints for the literature, ClinVar and Ensembl for variants,
Evo 2 and AlphaMissense for variant effect prediction, UniProt and Reactome for mechanism,
ChEMBL for compound to target links, GEO for reference expression, and a reviewer style cite
or abstain discipline enforced in code. The reports and a deep translational dive on renal
medullary carcinoma (docs/deep_dive_renal_medullary.md) were assembled using the broader tool
ecosystem in practice, PubMed, Consensus, Paperclip full text, ClinicalTrials.gov, and web
search, and a live-assembly path in the package calls the Claude API to draft a report for a
condition that has no curated file yet.

## Honesty and safety

Anveshar is decision support for research use, not medical advice, and not a medical device.
Every match and every hypothesis is for discussion by a qualified clinical team and a
molecular tumor board, who make all treatment decisions.
