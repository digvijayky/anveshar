# Anveshar engine: dossier build prompt (parameterized)

Reusable instruction for the Anveshar evidence agent. Fill `{CANCER}` and optional
`{PATIENT_PROFILE}` (variants / expression targets), then run as a research subagent.
The agent MUST cite every non-trivial claim with a real PMID, DOI, or NCT and mark
anything it cannot verify as UNVERIFIED. No fabrication. No git writes. No em dashes.

## Workbench data sources to use (Claude Science / AI Workbench)
Literature: PubMed, Consensus, Paperclip, journals/preprints.
Variants/clinical: ClinVar (pathogenicity), Ensembl (gene/variant annotation), Evo 2 (variant effect).
Protein/pathway: UniProt, Reactome, PDB / OpenFold3 (target structure).
Drug/target: ChEMBL (compound-target), Cortellis (pipeline).
Expression: GEO (reference scRNA-seq/bulk).
Trials: ClinicalTrials.gov API v2.
(Load MCP schemas via ToolSearch; use WebSearch/WebFetch for FDA/registry.)

## Evidence tiers (assign to every therapy)
Tier 1 = FDA tissue-agnostic approval, applies if the biomarker is present.
Tier 2 = approved in another tumor with the same validated target present, or a positive basket/prospective signal in this cancer.
Tier 3 = mechanistic/preclinical rationale only.

## Output: a DATA json exactly matching this schema, written to the given path.
Each of the three voice keys (patient/clinician/researcher) is an audience-tuned string.
Every citation.url is a real https link (PubMed / ClinicalTrials / DOI / FDA). No em/en dashes.

```json
{
  "cancer": {"name": "", "sub": "", "chips": ["", "", ""]},
  "voiceNote": {"patient": "", "clinician": "", "researcher": ""},
  "overview": {"patient": "<p>..</p>", "clinician": "<p>..</p>", "researcher": "<p>..</p>"},
  "targetsIntro": {"patient": "", "clinician": "", "researcher": ""},
  "targets": [{"name": "", "present_in": "", "evidence": ""}],
  "therapiesIntro": {"patient": "", "clinician": "", "researcher": ""},
  "therapies": [{"drug": "", "target": "", "tier": 1, "approved_in": "", "dev_stage": "",
    "rationale": {"patient": "", "clinician": "", "researcher": ""},
    "citation": {"label": "", "url": "https://pubmed.ncbi.nlm.nih.gov/NNNN/"},
    "trial": {"nct": "NCTxx…", "url": "https://clinicaltrials.gov/study/NCTxx…"}}],
  "trials": [{"nct": "", "title": "", "phase": "", "intervention": "", "eligibility": "", "url": ""}],
  "precedentIntro": {"patient": "", "clinician": "", "researcher": ""},
  "precedents": [{"biomarker": "", "drug": "", "year": "", "citation": {"label": "", "url": ""}}],
  "disclaimer": "<b>This is decision support, not medical advice.</b> …"
}
```

If `{PATIENT_PROFILE}` is provided, add a `patientMatch` array marking which targets are
present in THIS patient (source: variant / expression), each `{target, source, finding, actionable_tier}`,
and foreground those therapies. Render (`render_report.py`) injects the json into the report template.
