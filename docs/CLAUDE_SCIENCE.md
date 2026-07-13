# Anveshar inside Claude Science

Anveshar is built to run from inside Claude Science, the agentic life sciences environment
(Claude with its research skills and connected scientific databases). Almost every Anveshar
capability is either a call to a connected database or a Claude skill, so the whole workflow
can be driven by asking Claude, and reproduced by anyone with the same tools.

This document maps each capability to the Claude Science tool that runs it, and marks whether
it is runnable from inside Claude Science today.

## Capability to tool map

| Anveshar capability | Claude Science tool | Runnable from inside |
|---|---|---|
| Choose and vet a model or target for a task | deep-research skill (fan-out search, adversarial verification) | Yes |
| Resolve a rare cancer to its driver genes and etiology | Anveshar catalog and pipeline (`anveshar/pipeline.py`) | Yes |
| Molecular target evidence: tractability, associated diseases, drugs, DepMap essentiality | Open Targets connector (GraphQL) | Yes |
| Cohort genomics: mutations, copy number, expression, survival | cBioPortal REST (used in the pipeline and notebooks 03, 05, 07, 08) | Yes |
| Labeled variants and clinical significance | ClinVar connector (used in notebook 10 to build the training set) | Yes |
| Clinical trials for a target or condition | ClinicalTrials.gov connector | Yes |
| Pathway context | Reactome connector | Yes |
| Literature validation of every claim | PubMed, Consensus, and Paperclip search | Yes |
| Sequence model inference: zero-shot variant effect, embeddings, constraint maps | notebook 09 (transformers, ESM-2) | Yes |
| Training and fine-tuning sequence models on rare-cancer labels | notebook 10 (transformers, a trained head or LoRA) | Yes |
| Single-cell integration, label transfer, and fine-tuning | scvi-tools and single-cell-rna-qc skills; scGPT and Geneformer | Yes |
| Raw sequencing to counts or variant calls | nextflow-development skill (nf-core pipelines) | Yes |
| Interactive exploration of cancers, genes, tasks, and models | Atlas Explorer artifact | Yes, to view |
| Clinical trial protocol drafting | clinical-trial-protocol skill | Yes |

## What is live linked versus framework

To be transparent about integrity: the connectors above are live network calls made by the
code and reproducible by anyone. OncoKB is used only as a tier and level framework (the labels
Level 1 to 4, and the AMP/ASCO/CAP and ESCAT tiers), not as a live API call, because that needs
a token; the actionability evidence itself comes from the live Open Targets and cBioPortal calls
and from cited primary literature. The single-cell foundation model claims carry the published
caveat that they do not reliably beat simple baselines zero-shot, so the scvi-tools baseline is
always run alongside them.

## How to run a full analysis from inside Claude Science

A typical rare-cancer analysis, driven by asking Claude:

1. Ask the deep-research skill which model fits the task and to verify it against primary sources.
2. Ask Claude to pull the labeled data from the ClinVar and cBioPortal connectors for the driver genes.
3. If starting from raw reads, ask the nextflow-development skill to run the nf-core pipeline to features.
4. Open notebook 09 to score variants zero-shot, or notebook 10 to train a supervised layer.
5. For single-cell data, ask the scvi-tools skill for a scVI or scANVI baseline and fine-tune scGPT or
   Geneformer against it.
6. Ask PubMed, Consensus, and Paperclip to validate the result against the literature.

Every step is cited, reproducible, and research use only, not medical advice.

Developer: [digvijayky](https://digvijayky.com)
