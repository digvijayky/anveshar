# Anveshar examples

Curated, cited knowledge bases and patient profiles that ship with Anveshar. Every claim
carries a real PMID, DOI, or NCT. Render them all with `python3 scripts/render_demos.py`.

## Disease reports (render-dict shape, consumed by the report template)

| File | Condition | Notes |
|---|---|---|
| `rectal_net.json` | Rectal neuroendocrine tumor | The cross-condition translation engine end to end, 12 tiered therapies. |
| `renal_medullary.json` | Renal medullary carcinoma | A SMARCB1 driven cancer with no tissue-agnostic option; discovery layer proposes EZH2, PRMT5, and gene directed hypotheses. |
| `rare_disease/spinal_muscular_atrophy.json` | Spinal muscular atrophy | Shows the same engine generalizes beyond cancer, with antisense, gene therapy, and small molecule modalities. |

## Patient profiles (personalize any report)

| File | Case | Actionable finding |
|---|---|---|
| `profiles/klempner_braf.json` | Klempner et al., Cancer Discovery 2016, PMID 27048246 | BRAF V600E in an MSI-stable rectal NEC; immunotherapy correctly excluded. |
| `profiles/pereira_msi_braf.json` | Pereira et al., Cancer Control 2023, PMID 36840617 | MSI-H plus BRAF V600E across four variant classes, including a VUS reclassification workflow. |

These example files are the outputs of the Anveshar evidence agents and are the same data
that drives the live reports linked from the project hub.
