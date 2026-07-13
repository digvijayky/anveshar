# Anveshar architecture

Anveshar turns the reasoning a molecular tumor board does by hand into a reproducible, cited pipeline. This document describes the five stage pipeline, the module layout, the canonical schema, how the evidence connectors and external models plug in, and the cite or abstain discipline that binds all of it together.

## The five stage pipeline

The engine (`anveshar.engine.run`) orchestrates five stages. Given a cancer name and an optional patient profile, it always returns a validated `DiseaseReport`.

1. **Characterize.** Build a molecular picture of the cancer from primary literature (PubMed and preprints) and curated knowledge. This stage populates the report overview and the defining lesions of the disease.
2. **Extract targets.** Read druggable dependencies out of the disease biology and, when a profile is supplied, out of the patient's own variants and expression. Sequence alterations flow through `anveshar.variants`; expressed surface and pathway targets flow through `anveshar.expression`.
3. **Translate across conditions.** For each target, find therapies validated in other conditions that hit the same target or pathway, anchored on tissue agnostic precedent (MSI-H, NTRK, BRAF V600E, RET, HER2). This is `anveshar.translation`.
4. **Match trials.** Retrieve trials, favoring basket and tissue agnostic designs, via the ClinicalTrials.gov connector.
5. **Grade, personalize, and discover.** Tier every therapy against OncoKB, AMP/ASCO/CAP, and ESCAT; promote the options that apply to the patient's alterations and honestly exclude the ones that do not; and run the discovery layer to generate cross condition and advanced modality hypotheses. The report is validated (no fabricated entries, no em or en dashes) before it is returned.

`run(live=False)` assembles the report from curated and example knowledge for reproducibility; `run(live=True)` calls the evidence connectors for fresh data. Either way the output type is identical.

## Module layout

```
anveshar/
  schema.py            canonical types (variant classes, tiers, modalities, discovery)
  engine.py            the five stage pipeline orchestrator
  evidence/            PubMed, ClinicalTrials, ClinVar, Workbench connectors
  variants/            variant interpreter (classes, actionability, VUS, interpret)
  translation/         cross-condition engine + tissue-agnostic knowledge + discovery layer
  expression/          scRNA-seq druggable target extractor
  report/              HTML report template + renderer
```

Each module imports its types from `anveshar.schema` and implements the public functions defined in `docs/interfaces.md`. Dependencies are kept minimal: plain standard library plus `requests`, with `scanpy` and `anndata` imported lazily and only inside the expression module, so the core package imports without them.

## The schema (the build contract)

`anveshar.schema` is plain stdlib dataclasses, so any module can import it with no third party dependency. The load bearing types:

`Tier` grades evidence strength: T1 (FDA tissue agnostic approval that applies if the biomarker is present), T2 (approved in another tumor with the same target, or a basket signal here), T3 (mechanistic or preclinical rationale only), and DISCOVERY (a novel computationally generated hypothesis not yet tried in the target cancer).

`Modality` enumerates the therapeutic modality dimension: small molecule, antibody, antibody drug conjugate, bispecific T cell engager, cell therapy, gene therapy, antisense oligonucleotide, radioligand therapy, cytotoxic chemotherapy, and immune checkpoint inhibitor. This is what lets Anveshar nominate advanced modalities, not only small molecules (see `docs/gene_therapy.md`).

`VariantClass` covers the full range of alterations the interpreter routes on: SNV, indel, fusion, amplification, deletion, CNV, splice, epigenetic, signature, composite biomarker, expression, germline, and VUS.

`Alteration` is one molecular finding in a patient profile, carrying its variant class, an `Actionability` grade (OncoKB level, AMP/ASCO/CAP tier, ESCAT tier), a `pathogenicity` string with its source URL, a canonical `target` key for matching, and a `verified` flag that is set False when a finding is illustrative or model predicted rather than corroborated.

`Therapy` is one graded match: drug, target, tier, modality, where it is approved, development stage, a role specific `rationale` (patient, clinician, researcher), a `Citation`, and an optional trial.

`DiscoveryHypothesis` is the novelty layer's output type: the hypothesis text, the `shared_dependency` that licenses the analogy, the `source_condition` where the therapy is validated, the `proposed_modality`, a `rationale`, a `transferability` grade, a `supporting_citation` for the analogy, and a `testable_prediction` a lab could use to falsify it.

`DiseaseReport` aggregates everything (overview, targets, therapies, trials, precedents, discovery hypotheses, and the optional `PatientProfile`) and exposes `to_render_dict()` to flatten the rich model into the DATA dict the HTML report consumes.

## Evidence connectors and external models

`anveshar.evidence` is the boundary between the engine and the outside world. Every connector returns typed, cited data, times out on the network, and never raises to the caller (it returns an empty result on failure so the pipeline degrades gracefully).

The primary connectors are `pubmed` (NCBI E-utilities: esearch, esummary, efetch, returning pmid, title, journal, year, doi), `clinicaltrials` (ClinicalTrials.gov API v2, returning typed `Trial` objects and favoring basket designs), and `clinvar` (NCBI E-utilities db=clinvar, returning accession, significance, and URL, or an empty dict when nothing is found, never an invented classification).

`workbench.WorkbenchClient` is a thin adapter layer over the Claude Science / AI Workbench connectors. It exposes one method per data source: `uniprot(gene)`, `ensembl(gene_or_hgvs)`, `reactome(gene)`, `chembl(target)`, `evo2(hgvs)`, and `alphamissense(protein_change)`. Where a live Workbench connector is not available, the method falls back to the corresponding public REST API (UniProt, Ensembl REST, Reactome ContentService, ChEMBL). The two model connectors are handled explicitly: for Evo 2 and AlphaMissense the adapter returns `{"available": False, ...}` when the model is not reachable, so the caller can degrade rather than fabricate a score.

How the sources are used:

UniProt supplies canonical protein identity and function. Ensembl resolves gene coordinates and HGVS. Reactome places a gene in its pathway context, which is what lets the translation engine reason about pathway level analogies rather than only exact target matches. ChEMBL supplies drug to target relationships for candidate therapies. ClinVar corroborates named single variants and records the accession and clinical significance. GEO backs expression level target discovery with real datasets.

Evo 2 (Brixi, Durrant, Ku et al., 2025; peer reviewed in Nature 2026, PMID 41781614, [DOI](https://doi.org/10.1101/2025.02.18.638918)) is a DNA foundation model used strictly as method rationale to triage coding, noncoding, and splice region variants of uncertain significance. AlphaMissense (Cheng et al., Science 2023, PMID 37733863, [DOI](https://doi.org/10.1126/science.adg7492)) assigns calibrated per substitution pathogenicity to missense variants. Both are used only to raise or lower pre test suspicion on a VUS and route it to functional review; neither is ever converted into a clinical tier on a prediction alone, and no numeric model score is asserted for a case that has no published score (it is marked UNVERIFIED instead).

## Cite or abstain evidence discipline

The single rule that binds every module: every therapy claim, precedent, and discovery analogy carries a real citation (a PMID, DOI, or NCT), and where a claim cannot be verified Anveshar says so rather than inventing one. Named single variants are corroborated against ClinVar; predicted scores from sequence models are used as method rationale, never as fabricated numbers; and any value that could not be independently confirmed is marked UNVERIFIED inline. The engine enforces one output constraint mechanically: `assert_no_dashes` walks the entire report and raises if any string contains an em or en dash, so Anveshar never emits one. The variant interpretation frameworks and their sources are documented in `docs/variant_interpretation_methodology.md`.

## Data flow

```
  cancer name  ─┐
                ├─▶  [1 CHARACTERIZE]  ◀── PubMed, preprints, curated knowledge
patient profile ┘            │
                             ▼
                    [2 EXTRACT TARGETS]  ◀── variants/ (ClinVar, Evo2, AlphaMissense)
                             │                expression/ (GEO, scRNA-seq)
                             ▼
                    [3 TRANSLATE]  ◀── translation/ + tissue-agnostic precedents
                             │            Reactome (pathway), ChEMBL (drug-target),
                             │            UniProt / Ensembl (identity, coordinates)
                             ▼
                    [4 MATCH TRIALS]  ◀── ClinicalTrials.gov API v2 (basket-first)
                             │
                             ▼
       [5 GRADE + PERSONALIZE + DISCOVER]
        ├─ grade:      OncoKB / AMP-ASCO-CAP / ESCAT
        ├─ personalize: match / exclude vs patient alterations
        └─ discover:   DiscoveryHypothesis (Tier 0, novel, cited, falsifiable)
                             │
                             ▼
                    DiseaseReport ──▶ assert_no_dashes ──▶ report/ (HTML)
```

Every arrow into a stage is a cited data source; every box emits typed schema objects; and the final report passes the no dash and no fabrication checks before it is written.
