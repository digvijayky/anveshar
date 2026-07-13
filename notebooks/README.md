# Anveshar notebooks for computational biologists

Runnable Jupyter notebooks covering every kind of analysis Anveshar supports. Each notebook is
self-contained, uses real public data or the local knowledge base, and runs top to bottom. The
notebooks in this directory have been executed end to end (via `nbconvert --execute`) so their
outputs and figures are already rendered.

| Notebook | What it does | Data / tools |
|---|---|---|
| `01_pipeline_harness.ipynb` | Run the five-stage harness on a rare cancer; inspect provenance, cited therapies with confidence, and the bespoke workflow | concord.pipeline; Open Targets, DepMap, PubMed (live cell optional) |
| `02_catalog_analyses.ipynb` | Actionability, shared dependencies, druggability gap, etiology landscape, hereditary syndrome map over all rare cancers | concord.analysis |
| `03_genomics_transcriptomics_cbioportal.ipynb` | Driver mutation frequency and BAP1-split transcriptomes for uveal melanoma | TCGA via cBioPortal REST API |
| `04_imaging_he_analysis.ipynb` | H&E color deconvolution and watershed nuclei segmentation | CC BY 4.0 histopathology; scikit-image |
| `05_msk_impact_rare_cancers.ipynb` | Map MSK-IMPACT (10,945 tumors) onto the rare cancer catalog; per-type driver frequencies | MSK-IMPACT via cBioPortal |
| `06_target_validation_functional_genomics.ipynb` | Score druggability tractability and DepMap essentiality; pivot a loss driver to its induced dependency | Open Targets, DepMap |

## Setup

From the repository root:

    pip install -e .            # or add the repo to PYTHONPATH
    pip install jupyter scikit-image scikit-learn pillow requests pandas matplotlib scipy

Each notebook's first code cell locates the repository and imports `concord`, so the notebooks
run without an editable install as long as they are launched from inside the repo.

## Run

    jupyter lab                 # then open a notebook and Run All

or headless:

    jupyter nbconvert --to notebook --execute --inplace notebooks/02_catalog_analyses.ipynb

Notebooks 3, 4, 5, and the optional live cells in 1 and 6 require internet (Open Targets,
cBioPortal, and one image download). Notebook 2 and the offline part of notebook 1 are fully
deterministic and need no network.

## Note

These notebooks produce research and educational analysis of public data, not medical advice.
Confidence and validation scores summarize evidence strength, not the probability of benefit for
any individual. Every clinical decision must be made by a qualified health care provider.

Developed by Dig Vijay Kumar Yarlagadda, digvijayky.com
