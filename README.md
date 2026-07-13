# Anveshar

**A translational molecular board for rare cancers, built to find therapies that already exist somewhere else.**

Rare cancers rarely get their own clinical trials, so the patients who need answers most are the ones the evidence base serves least. Anveshar attacks that gap directly. Given a rare cancer, and optionally a patient's own molecular profile, it finds therapies that are approved or in trials in *other* conditions that share the same molecular dependency, grades every match by strength of evidence, and, where the evidence runs out, it proposes novel testable hypotheses instead of stopping.

Anveshar is built on the Claude Science / AI Workbench idea of a research environment wired to curated scientific databases, and it turns the reasoning a molecular tumor board does by hand into something reproducible and cited.

**Live demonstration:** https://claude.ai/code/artifact/21b36179-57ef-416b-840d-9937c86ddb54 (the hub links four cited reports and this codebase).

## What it does

1. **Characterize** the cancer from primary literature (PubMed, preprints).
2. **Extract targets** from the disease biology and, when provided, from the patient's own variants and expression.
3. **Translate across conditions**: for each target, find drugs validated in other tumors that hit the same target or pathway, anchored on tissue-agnostic FDA precedent (MSI-H, NTRK, BRAF V600E, RET, HER2).
4. **Match trials**, favoring basket and tissue-agnostic designs.
5. **Grade and personalize**: every recommendation is tiered (OncoKB, AMP/ASCO/CAP, ESCAT), and a patient's alterations promote the options that actually apply to them while honestly excluding the ones that do not.

Every therapy claim carries a real citation (PMID, DOI, or NCT). Where a claim cannot be verified, Anveshar says so rather than inventing one. It never emits an em dash, and it never fabricates a variant, a drug, or a trial.

## The novelty: a discovery engine, not a lookup table

Anveshar does not only retrieve known matches. Its discovery layer reasons over shared molecular dependencies to **generate hypotheses that no dedicated trial has yet tested in the target cancer**, ranked by how well the analogy should transfer and framed as falsifiable predictions a lab can test:

- **Cross-condition analogy.** A SMARCB1-deficient rare kidney cancer shares a SWI/SNF loss dependency with epithelioid sarcoma and rhabdoid tumors, which nominates EZH2 and PRMT5 directed strategies as testable leads.
- **Advanced modalities, including gene therapy.** For loss-of-function tumor suppressor drivers and lineage-defined surface antigens, Anveshar flags candidate approaches beyond small molecules: antisense oligonucleotides for splice lesions, bispecific and cell therapies for lineage antigens such as DLL3, radioligand therapy for receptor-positive disease, and gene directed strategies (gene replacement, base and prime editing, synthetic lethality) as research directions.
- **Every hypothesis is labeled a hypothesis.** The discovery tier is visually and semantically separate from approved options, with a mechanistic rationale, a transferability grade, and the experiment that would confirm or kill it.

This is the part that turns Anveshar from a report into an engine that can surface non-obvious, novel therapeutic directions for cancers that have almost none.

## Beyond cancer: all rare diseases

The core abstraction, a molecular lesion mapped through its mechanism to a therapy validated in a mechanistically related condition, is not specific to cancer. The same engine generalizes to the roughly 7,000 rare Mendelian and genetic diseases, where cross-condition borrowing (a therapy proven in one channelopathy, lysosomal disorder, or repair syndrome applied to a mechanistically adjacent one) and gene directed modalities are often the only realistic path. Anveshar is architected so the cancer knowledge bases are one instance of a general rare-disease translation framework (see `docs/rare_disease_expansion.md`).

## Install

```bash
pip install -e .            # core
pip install -e ".[scrna]"   # add the single-cell target extractor
pip install -e ".[dev]"     # tests
```

## Use

```bash
anveshar list                                              # every condition Anveshar covers
anveshar run --cancer "rectal neuroendocrine tumor" --out report.html
anveshar run --cancer "rectal neuroendocrine tumor" --profile examples/profiles/pereira_msi_braf.json --out report.html
anveshar run --cancer "renal medullary carcinoma" --discovery --out report.html
anveshar run --cancer "a condition with no curated file" --live   # assembled via the Claude API
```

## Layout

```
anveshar/
  schema.py            canonical types (variant classes, tiers, modalities, discovery)
  engine.py            the five stage pipeline orchestrator
  evidence/            PubMed, ClinicalTrials, ClinVar, Workbench connectors
  variants/            sophisticated variant interpreter (classes, actionability, VUS, interpret)
  translation/         cross-condition engine + tissue-agnostic knowledge + discovery layer
  expression/          scRNA-seq druggable target extractor
  report/              HTML report template + renderer
examples/              real, cited disease reports and patient profiles
docs/                  methodology, architecture, novelty, rare-disease expansion
tests/                 unit tests for every module
```

## Honesty and safety

Anveshar is decision support, not medical advice. It grades evidence, links every claim to its source, separates approved options from research hypotheses, and defers all treatment decisions to a qualified clinical team and a molecular tumor board.

## Author

Developed by Dig Vijay Kumar Yarlagadda, digvijayky.com. Built with Claude for the Life Sciences Hackathon 2026.
