# Anveshar module interfaces (the build contract)

Every module imports types from `anveshar.schema` and implements the public functions
below exactly. Rules for all modules: plain stdlib plus the package's declared deps
(`requests`; `scanpy`/`anndata` only under the `expression` module); NEVER emit an em
dash or en dash (use commas, parentheses, or the word "to"); cite real sources; never
fabricate a variant, drug, or trial (raise or mark UNVERIFIED instead); every public
function has a docstring and a unit test under `tests/`.

## anveshar.evidence
- `pubmed.search(query: str, retmax: int = 20) -> list[dict]` and `pubmed.fetch(pmid: str) -> dict`
  via NCBI E-utilities (esearch/esummary/efetch). Return {pmid, title, journal, year, doi}.
- `clinicaltrials.search(condition: str, status: str = "RECRUITING", intervention: str | None = None) -> list[Trial]`
  via ClinicalTrials.gov API v2 (https://clinicaltrials.gov/api/v2/studies). Return `Trial` objects.
- `clinvar.lookup(term: str) -> dict` via NCBI E-utilities db=clinvar. Return
  {accession, significance, url}. Empty dict if not found (never invent).
- `workbench.WorkbenchClient`: thin adapters to the Claude Science connectors, each a method:
  `uniprot(gene)`, `ensembl(gene_or_hgvs)`, `reactome(gene)`, `chembl(target)`,
  `evo2(hgvs)`, `alphamissense(protein_change)`. Where a live connector is not available,
  the method calls the corresponding public REST API (UniProt, Ensembl REST, Reactome
  ContentService, ChEMBL) and clearly returns `{"available": False, ...}` for the model
  connectors (Evo 2, AlphaMissense) so the caller degrades gracefully. Network calls must
  time out and never raise to the caller (return {} on failure).

## anveshar.variants
- `classes.classify(raw: dict) -> VariantClass` maps a raw alteration record to a `VariantClass`.
- `actionability.grade(gene: str, variant: str, biomarker: str = "", condition: str = "") -> Actionability`
  returns OncoKB / AMP-ASCO-CAP / ESCAT tiers from a curated, cited rule table
  (`anveshar/variants/_knowledge.py` or `data/`). Unknown => empty tiers, not a guess.
- `vus.reclassify(alt: Alteration, client=None) -> Alteration` adds AlphaMissense / Evo 2
  rationale for a VUS; sets `verified=False` and never promotes a VUS to a clinical tier
  on a prediction alone.
- `interpret.interpret_profile(raw: dict) -> PatientProfile` is the entry point: takes a raw
  profile (as in `examples/profiles/*.json`) and returns a fully typed `PatientProfile`
  with classified, graded, VUS-triaged alterations.

## anveshar.translation
- `tissue_agnostic.PRECEDENTS: list[Precedent]` a curated, cited list of tissue-agnostic /
  basket approvals; `tissue_agnostic.for_biomarker(biomarker: str) -> Therapy | None`.
- `translate.translate_targets(targets: list[str], condition: str = "") -> list[Therapy]`
  maps molecular targets to therapies validated in other conditions, tiered and cited.
- `translate.match(report: DiseaseReport, profile: PatientProfile) -> dict` returns
  {matched: [drug], excluded: [{target, reason}]} by comparing profile targets to therapies.
- `discovery.generate(report: DiseaseReport, profile: PatientProfile | None = None) -> list[DiscoveryHypothesis]`
  THE NOVELTY LAYER: proposes cross-condition and advanced-modality hypotheses
  (gene therapy, ASO, cell therapy, synthetic lethality) with shared_dependency,
  transferability grade, a supporting citation for the analogy, and a testable_prediction.

## anveshar.expression
- `scrna.extract_targets(h5ad_path: str, tumor_label: str | None = None) -> list[Alteration]`
  loads an AnnData, runs light QC, identifies the tumor cells, and reads out expressed
  druggable targets (e.g. SSTR2, DLL3, ERBB2, MET) as `Alteration(variant_class=EXPRESSION)`.
  Import scanpy lazily inside the function so the core package imports without it.

## anveshar.report
- `render.render(base_html, data_json, out_html, patient_json=None)` (already present as
  `render.py`) injects a DATA dict into `template.html`. Add `render_report(report: DiseaseReport, out_html: str)`
  that calls `report.to_render_dict()` and writes the HTML.

## anveshar.engine
- `engine.run(cancer: str, profile: PatientProfile | None = None, scrna: str | None = None,
  discovery: bool = True, live: bool = False) -> DiseaseReport` orchestrates the five stages.
  With `live=False` it assembles from curated/example knowledge; with `live=True` it calls
  the evidence connectors. Always returns a validated `DiseaseReport` (calls `assert_no_dashes`).

## anveshar.cli
- `cli.main()` exposes `anveshar run --cancer ... [--profile f.json] [--scrna f.h5ad] [--discovery] --out report.html`.
