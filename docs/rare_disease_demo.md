# Anveshar beyond cancer: spinal muscular atrophy demonstration

## What this demo shows

Anveshar matches a condition, and optionally a patient's own molecular profile, to therapies validated in other conditions that share the same molecular dependency, grades the evidence, and generates cross condition hypotheses. The engine, the schema, and the renderer are condition agnostic. This demonstration proves that by pointing the same machinery at a canonical rare Mendelian disease, spinal muscular atrophy (SMA), where the story is gene directed therapy and cross condition modality borrowing rather than oncology.

The report at `examples/rare_disease/spinal_muscular_atrophy.json` was produced with the exact same Anveshar render schema (`anveshar/schema.py`, `DiseaseReport.to_render_dict()`) and the same HTML renderer as the cancer reports (`examples/renal_medullary.json`, `examples/rectal_net.json`). Only the knowledge base changed. Every key in the DATA dict is identical in name and shape. Note that the top level key is still literally `cancer`; it holds the condition name and the schema is intentionally condition agnostic, so no code change was needed to render a non cancer disease.

## Same schema, only the knowledge changed

The SMA DATA dict carries the same sections as the cancer examples: `cancer` (name, sub, chips), `voiceNote`, `overview` (patient, clinician, researcher), `targetsIntro`, `targets`, `therapiesIntro`, `therapies`, `trials`, `precedentIntro`, `precedents`, `discoveryIntro`, `discovery`, and `disclaimer`. Therapies carry a `modality` string drawn from the `Modality` enum in `anveshar/schema.py`, and discovery entries carry `shared`, `source`, `modality`, `transferability`, `prediction`, and a real `citation`, exactly as the cancer reports do. The file parses as valid JSON, contains no em or en dash, and every modality string validates against the enum.

The disease biology in one line: SMA is caused by biallelic loss of function of SMN1, and severity is modified by SMN2 copy number because the SMN2 c.840C>T variant biases exon 7 exclusion. The two Anveshar targets are SMN protein restoration (SMN1 replacement) and SMN2 splicing modulation (exon 7 inclusion). Three approved disease modifying therapies act on those targets.

## Modalities covered

The three approved SMA therapies span three distinct advanced modalities, which is the point of the demonstration: one molecular dependency (SMN insufficiency) drugged three different ways.

| Therapy | Modality string (enum value) | Mechanism | Primary citation |
| --- | --- | --- | --- |
| Nusinersen | `antisense oligonucleotide` | Splice switching ASO at the SMN2 intron 7 ISS-N1 site, promotes exon 7 inclusion | Finkel et al., N Engl J Med 2017 (ENDEAR), PMID 29091570, [DOI](https://doi.org/10.1056/NEJMoa1702752) |
| Onasemnogene abeparvovec | `gene therapy` | One time intravenous AAV9 delivery of a functional SMN1 transgene | Mendell et al., N Engl J Med 2017, PMID 29091557, [DOI](https://doi.org/10.1056/NEJMoa1706198) |
| Risdiplam | `small molecule` | Oral SMN2 pre mRNA splicing modifier, raises full length SMN | Baranello et al., N Engl J Med 2021 (FIREFISH), PMID 33626251, [DOI](https://doi.org/10.1056/NEJMoa2009965); Mercuri et al., Lancet Neurol 2022 (SUNFISH Part 2), PMID 34942136, [DOI](https://doi.org/10.1016/S1474-4422(21)00367-7) |

The discovery layer adds four more modality strings across its research hypotheses: `antisense oligonucleotide`, `gene therapy`, `other` (used for RNA interference, which has no dedicated enum member), and `cell therapy` (used for CRISPR edited autologous hematopoietic stem cells).

## Precedents: why cross condition borrowing is legitimate

The precedent section lists landmark rare disease approvals that establish each advanced modality as real and regulator approved, so that transferring a modality across conditions is grounded rather than speculative.

| Modality validated | Approval | Citation |
| --- | --- | --- |
| Antisense oligonucleotide (splice correction) | Nusinersen for SMA, 2016 to 2017 | Finkel et al., N Engl J Med 2017, PMID 29091570, [DOI](https://doi.org/10.1056/NEJMoa1702752) |
| AAV gene replacement | Onasemnogene abeparvovec for SMA, 2019 | Mendell et al., N Engl J Med 2017, PMID 29091557, [DOI](https://doi.org/10.1056/NEJMoa1706198) |
| RNA interference (transcript knockdown) | Patisiran for hereditary transthyretin amyloidosis, 2018 | Adams et al., N Engl J Med 2018, PMID 29972753, [DOI](https://doi.org/10.1056/NEJMoa1716153) |
| CRISPR-Cas9 gene editing | Exagamglogene autotemcel for sickle cell disease and beta thalassemia, approved 2023 | Frangoul et al., N Engl J Med 2021, PMID 33283989, [DOI](https://doi.org/10.1056/NEJMoa2031054) |

## Discovery hypotheses (research directions, not clinical recommendations)

The discovery layer proposes four cross condition hypotheses, each prefixed "Research hypothesis (not a clinical recommendation)", each transferring a validated modality over a shared molecular dependency with a graded transferability and a falsifiable prediction:

1. ASO splice correction transferred to another splice altering monogenic disease, supported by the milasen individualized ASO precedent (Kim et al., N Engl J Med 2019, PMID 31597037, [DOI](https://doi.org/10.1056/NEJMoa1813279)).
2. One time AAV gene replacement transferred to another recessive loss of function disease with a compact transgene, supported by the onasemnogene precedent (PMID 29091557).
3. RNA interference knockdown transferred to a monogenic disease driven by a toxic or excess transcript, supported by the patisiran precedent (PMID 29972753).
4. CRISPR based ex vivo editing of autologous hematopoietic stem cells transferred to another correctable hematologic monogenic disease, supported by the exagamglogene precedent (PMID 33283989).

## Trials

The `trials` list is intentionally empty. No recruiting SMA trial was verified on ClinicalTrials.gov for this static demonstration file, and per the Anveshar rule no NCT number is ever invented. The pivotal registration trials for the three approved therapies are still cited on their therapy cards via their real NCT identifiers (NCT02193074 ENDEAR, NCT02122952 for the AAV9 phase 1 study, NCT02913482 FIREFISH).

## Verification

According to PubMed, all citations in `examples/rare_disease/spinal_muscular_atrophy.json` were confirmed by direct metadata lookup (title, journal, year, DOI, first author). The JSON was validated to parse cleanly, to contain no em or en dash, to include every required schema key, and to use only valid `Modality` enum strings. There are no UNVERIFIED items in this report.

## Attribution

Citation metadata in this demonstration was retrieved from PubMed. DOI links: [10.1056/NEJMoa1702752](https://doi.org/10.1056/NEJMoa1702752), [10.1056/NEJMoa1706198](https://doi.org/10.1056/NEJMoa1706198), [10.1056/NEJMoa2009965](https://doi.org/10.1056/NEJMoa2009965), [10.1016/S1474-4422(21)00367-7](https://doi.org/10.1016/S1474-4422(21)00367-7), [10.1056/NEJMoa1716153](https://doi.org/10.1056/NEJMoa1716153), [10.1056/NEJMoa2031054](https://doi.org/10.1056/NEJMoa2031054), [10.1056/NEJMoa1813279](https://doi.org/10.1056/NEJMoa1813279).
