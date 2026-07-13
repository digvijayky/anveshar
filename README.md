# Anveshar

A method for rare cancer and rare disease research. Given a rare cancer, and optionally a
patient's molecular profile, Anveshar identifies the cancer's molecular dependencies and
retrieves therapies that have been studied against the same dependencies in other conditions,
with a citation and an evidence tier for each. Where no established therapy fits, it lists
testable hypotheses, kept separate from established options.

Rare cancers usually lack dedicated clinical trials. Oncology increasingly assigns therapies by
molecular marker rather than tissue of origin, for example pembrolizumab for MSI-high tumors,
larotrectinib for NTRK fusions, and dabrafenib plus trametinib for BRAF V600E solid tumors.
Anveshar makes that cross-condition reasoning reproducible and traceable to sources.

Live pages: https://claude.ai/code/artifact/21dd72b9-0696-4402-a72a-9a365b3094d6 (a landing page
that links the atlas, the analyses, the multi-modal analysis, a pipeline run, and example reports).

## What it does

Given a rare cancer, and optionally patient variants and expression:

1. Characterize the cancer from the literature (PubMed, preprints).
2. Extract molecular targets from the disease biology and, when provided, from the patient's variants and expression.
3. Retrieve therapies studied against the same target or pathway in other conditions, referencing tissue-agnostic approvals (MSI-H, NTRK, BRAF V600E, RET, HER2) where they exist.
4. Match open trials, including basket and tissue-agnostic designs.
5. Assign an evidence tier (OncoKB, AMP/ASCO/CAP, ESCAT) and a confidence score to each option; the patient's alterations promote options that apply and exclude those that do not.

Each therapy links to a PMID, DOI, or NCT. Claims that cannot be verified are marked unverified
rather than asserted, and the tool does not fabricate a variant, drug, or trial.

## Hypotheses

When no established therapy fits, Anveshar lists candidate directions derived from shared
molecular dependencies. Each carries a mechanistic rationale, a transferability grade, and a
prediction that would confirm or reject it, and is labeled as a hypothesis, separate from
approved options. For example, a SMARCB1-deficient rare kidney cancer shares a SWI/SNF loss
dependency with epithelioid sarcoma and rhabdoid tumors, which points to EZH2 and PRMT5 directed
strategies as testable leads. It also notes therapy modalities beyond small molecules where they
apply: antibody drug conjugates, bispecifics and cell therapy for surface antigens such as DLL3,
radioligand therapy for receptor-positive disease, antisense oligonucleotides for splice lesions,
and gene directed approaches.

## Functional genomics and real data

The analysis pipeline validates each candidate target with Open Targets tractability and DepMap
CRISPR gene essentiality, and for a loss-of-function driver it considers the induced synthetic
lethal dependency (for example SMARCB1 loss and EZH2). It has been run on public data: TCGA
uveal melanoma and adrenocortical carcinoma across genomics, transcriptomics, and imaging, and the
MSK-IMPACT cohort of 10,945 tumors mapped onto the rare cancer catalog. See `notebooks/` for six
runnable Jupyter notebooks and `examples/multimodal/` for the SLURM scripts, source data, and figures.

## Beyond cancer

The same mapping, a molecular lesion through its mechanism to a therapy studied in a
mechanistically related condition, also applies to rare Mendelian and genetic diseases. The cancer
knowledge base is one instance of a general rare-disease framework (see `docs/rare_disease_expansion.md`).

## Install

```bash
pip install -e .            # core
pip install -e ".[scrna]"   # single-cell target extractor
pip install -e ".[dev]"     # tests
```

## Use

```bash
anveshar list                                              # conditions with curated knowledge
anveshar run --cancer "rectal neuroendocrine tumor" --out report.html
anveshar run --cancer "renal medullary carcinoma" --out report.html
anveshar analyze --cancer "renal medullary carcinoma" --live   # run the pipeline with live databases
python3 -m anveshar.pipeline "gastrointestinal stromal tumor"   # same, from Python
```

## Layout

```
anveshar/
  schema.py            canonical types (variant classes, tiers, modalities, discovery)
  engine.py            report pipeline orchestrator
  pipeline.py          reproducible analysis harness (resolve, databases, validation, translate)
  workflow.py          per-condition comp-bio workflow generator
  analysis.py          catalog-wide analyses (actionability, shared drivers, etiology, druggability)
  evidence/            PubMed, ClinicalTrials, ClinVar, and molecular database connectors
  variants/            variant interpreter (classes, actionability, VUS, interpret)
  translation/         cross-condition engine, tissue-agnostic knowledge, hypothesis layer
  expression/          scRNA-seq target extractor
  report/              HTML report template and renderer
data/                  rare conditions catalog, actionable drivers, induced dependencies
examples/              cited disease reports, patient profiles, and multi-modal analyses
notebooks/             six runnable analysis notebooks
docs/                  methodology, workflow, and expansion notes
tests/                 unit tests (offline and deterministic)
```

## Scope and safety

Anveshar is decision support for research and education, not medical advice. It grades evidence,
links each claim to a source, separates established options from research hypotheses, and reports
what it cannot verify. Confidence and validation scores summarize evidence strength, not the
probability of benefit for any individual. A driver-gene match is a translation hypothesis, and
variant context and tumor biology can change whether a therapy applies. Every diagnostic and
treatment decision must be made by a qualified health care provider, ideally within a clinical trial.

## Author

Developed by Dig Vijay Kumar Yarlagadda, digvijayky.com.
