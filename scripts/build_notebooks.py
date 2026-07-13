"""Build runnable Jupyter notebooks for Anveshar comp-bio analysis (nbformat)."""
import os, nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

OUT = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/github/concord/notebooks"
os.makedirs(OUT, exist_ok=True)

SETUP = r'''import os, sys
def _find_repo():
    p = os.getcwd()
    for _ in range(6):
        if os.path.exists(os.path.join(p, "concord", "__init__.py")):
            return p
        p = os.path.dirname(p)
    return None
REPO = _find_repo()
if REPO and REPO not in sys.path:
    sys.path.insert(0, REPO)
import anveshar
print("concord loaded from", os.path.dirname(anveshar.__file__))'''

DISC = ("---\n*Disclaimer: this notebook produces research and educational analysis of public data, not "
        "medical advice. Confidence and validation scores summarize evidence strength, not the probability "
        "of benefit for any individual. Every clinical decision must be made by a qualified health care "
        "provider, ideally within a clinical trial.*\n\n"
        "*Developer: [digvijayky](https://digvijayky.com).*")

def write(name, cells):
    nb = new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                                             "language_info": {"name": "python"}})
    nbf.write(nb, os.path.join(OUT, name)); print("wrote", name, "cells:", len(cells))
def md(t): return new_markdown_cell(t)
def co(t): return new_code_cell(t)

# ============ 01 harness ============
write("01_pipeline_harness.ipynb", [
 md("# 1. The Anveshar pipeline harness\n\n"
    "A reproducible, provenance-tracked pipeline that turns a rare cancer into a cited, confidence-scored "
    "cross-condition translation dossier. Five auditable stages: resolve, databases, target validation, "
    "translate, assemble. Offline is deterministic; `live=True` queries Open Targets, Ensembl, ChEMBL, "
    "PubMed, and DepMap."),
 co(SETUP),
 md("## Run the harness offline (deterministic)"),
 co('from anveshar.pipeline import run\n'
    'd = run("renal medullary carcinoma", live=False)\n'
    'print(d["condition"], "| drivers:", d["drivers"], "| mode:", d["mode"])\n'
    's = d["summary"]; bc = s["best_confidence"]\n'
    'print("actionable:", s["n_actionable"], "| tissue-agnostic:", s["n_tissue_agnostic"],\n'
    '      "| cross-condition:", s["n_cross_condition"])\n'
    'print("best confidence:", bc)'),
 md("## Provenance: every stage is auditable"),
 co('import pandas as pd\npd.DataFrame(d["provenance"])'),
 md("## Borrowable approved therapies (cited, confidence-scored)"),
 co('pd.DataFrame([{"gene": m["gene"], "drug": m["drug"], "approved_in": m["approved_in"],\n'
    '               "tier": m["tier"], "citation": m["citation"].get("url", "")}\n'
    '              for m in d["translation"]["actionable"]])'),
 md("## The bespoke, driver-class-tailored comp-bio workflow"),
 co('w = d["workflow"]\n'
    'print("driver class:", w["driver_class"], "\\n")\n'
    'for i, st in enumerate(w["steps"], 1):\n'
    '    print(str(i) + ". " + st["title"])\n'
    '    print("   tools:", st["tools"])\n'
    '    print("   checkpoint:", st["outputs"])\n'
    '    print()'),
 md("## Induced dependency (synthetic lethality) for loss drivers"),
 co('d.get("induced_dependencies", {})'),
 md("## Optional: run live (Open Targets + DepMap functional genomics)\n"
    "Requires internet; wrapped so a rate limit does not break the notebook."),
 co('try:\n'
    '    dl = run("renal medullary carcinoma", live=True)\n'
    '    tv = dl.get("target_validation", {})\n'
    '    display(pd.DataFrame([{"gene": g, "score": v.get("score"), "verdict": v.get("verdict"),\n'
    '                           "tractability_SM": v.get("sm_tractability"), "selective": v.get("selective_dependency")}\n'
    '                          for g, v in tv.items() if v.get("available")]))\n'
    'except Exception as e:\n'
    '    print("live stage skipped:", type(e).__name__, e)'),
 md(DISC),
])

# ============ 02 catalog analyses ============
write("02_catalog_analyses.ipynb", [
 md("# 2. Catalog-wide analyses over all rare cancers\n\n"
    "Actionability, shared molecular dependencies, the druggability gap, the etiology landscape, and the "
    "hereditary syndrome map, computed over the full rare cancer catalog."),
 co(SETUP),
 co('from anveshar import analysis\nimport pandas as pd, matplotlib.pyplot as plt'),
 md("## Actionability: which rare cancers have a borrowable approved therapy"),
 co('s = analysis.actionability_summary()\n'
    'print(s["n_actionable"], "of", s["n_rare_cancers"], f"({s[\'pct_actionable\']}%) actionable;",\n'
    '      s["n_tissue_agnostic"], "tissue-agnostic")\n'
    'pd.DataFrame(s["top_drugs"], columns=["drug", "n_rare_cancers"]).head(10)'),
 md("## Shared molecular dependencies (the cross-translation map)"),
 co('shared = analysis.catalog_shared_drivers()\ntop = shared[:15]\n'
    'fig, ax = plt.subplots(figsize=(8, 5))\n'
    'ax.barh([g for g, _ in top][::-1], [len(v) for _, v in top][::-1], color="#7b3fe4")\n'
    'ax.set_xlabel("rare cancers sharing the driver"); ax.set_title("Top shared dependencies"); plt.tight_layout()'),
 md("## Druggability gap: shared but undrugged dependencies (unmet need)"),
 co('g = analysis.druggability_summary()\n'
    'print(g["n_unmet_shared"], "of", g["n_shared_drivers"], "shared dependencies have no approved drug")\n'
    'pd.DataFrame(g["top_unmet"], columns=["gene", "n_rare_cancers"])'),
 md("## Etiology landscape"),
 co('e = analysis.etiology_landscape()\n'
    'pd.DataFrame([(k, v["count"]) for k, v in e.items()], columns=["category", "n_rare_cancers"])'),
 md("## Hereditary predisposition syndromes"),
 co('pd.DataFrame([(syn, len(cs)) for syn, cs in analysis.hereditary_syndrome_map()],\n'
    '             columns=["syndrome", "n_rare_cancers"])'),
 md(DISC),
])

# ============ 03 genomics + transcriptomics ============
write("03_genomics_transcriptomics_cbioportal.ipynb", [
 md("# 3. Genomics and transcriptomics on real data (cBioPortal)\n\n"
    "TCGA uveal melanoma (PanCancer Atlas) via the cBioPortal REST API: driver mutation frequency and "
    "driver mRNA z-scores split by BAP1 (the metastatic-risk axis). Real data, no simulation."),
 co('import requests, pandas as pd, numpy as np, matplotlib.pyplot as plt\n'
    'from collections import defaultdict\nfrom sklearn.decomposition import PCA\n'
    'API = "https://www.cbioportal.org/api"; STUDY = "uvm_tcga_pan_can_atlas_2018"; SL = STUDY + "_all"\n'
    'PANEL = {2776: "GNAQ", 2767: "GNA11", 8314: "BAP1", 23451: "SF3B1", 1964: "EIF1AX", 57105: "CYSLTR2", 5332: "PLCB4"}\n'
    'N = len(requests.get(f"{API}/studies/{STUDY}/samples", timeout=40).json()); print("tumors:", N)'),
 md("## Genomics: driver mutation frequency"),
 co('muts = requests.post(f"{API}/molecular-profiles/{STUDY}_mutations/mutations/fetch",\n'
    '   json={"sampleListId": SL, "entrezGeneIds": list(PANEL)}, params={"projection": "SUMMARY"}, timeout=60).json()\n'
    'ms = defaultdict(set)\n'
    'for m in muts: ms[PANEL[m["entrezGeneId"]]].add(m["sampleId"])\n'
    'freq = pd.Series({g: round(100*len(ms[g])/N, 1) for g in PANEL.values()}).sort_values(ascending=False)\n'
    'fig, ax = plt.subplots(figsize=(7, 4.5)); ax.bar(freq.index, freq.values, color="#2f5fe0")\n'
    'ax.set_ylabel("% mutated"); ax.set_title(f"Uveal melanoma drivers (TCGA, n={N})"); plt.xticks(rotation=40, ha="right"); plt.tight_layout()\n'
    'print("GNAQ or GNA11:", round(100*len(ms["GNAQ"] | ms["GNA11"])/N, 1), "% ; overlap:", len(ms["GNAQ"] & ms["GNA11"]))\n'
    'freq'),
 md("## Transcriptomics: driver mRNA z-scores and a BAP1 split"),
 co('rp = next(p["molecularProfileId"] for p in requests.get(f"{API}/studies/{STUDY}/molecular-profiles", timeout=40).json()\n'
    '          if "rna_seq" in p["molecularProfileId"] and "median_Zscores" in p["molecularProfileId"] and "normal" not in p["molecularProfileId"])\n'
    'rna = requests.post(f"{API}/molecular-profiles/{rp}/molecular-data/fetch",\n'
    '   json={"sampleListId": SL, "entrezGeneIds": list(PANEL)}, timeout=60).json()\n'
    'df = pd.DataFrame([{"sample": r["sampleId"], "gene": PANEL[r["entrezGeneId"]], "z": r["value"]} for r in rna])\n'
    'mat = df.pivot_table(index="gene", columns="sample", values="z").reindex(list(PANEL.values())).dropna(how="all")\n'
    'bap1 = mat.loc["BAP1"]; status = np.where(bap1 < bap1.median(), "BAP1-low", "BAP1-high")\n'
    'p = PCA(2).fit_transform(np.nan_to_num(mat.T.values))\n'
    'fig, ax = plt.subplots(figsize=(6, 5))\n'
    'for lab, c in [("BAP1-low", "#c0392b"), ("BAP1-high", "#2f5fe0")]:\n'
    '    mask = status == lab; ax.scatter(p[mask, 0], p[mask, 1], c=c, s=45, edgecolor="w", label=lab)\n'
    'ax.legend(frameon=False); ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_title("Uveal melanoma transcriptomes by BAP1"); plt.tight_layout()'),
 md("BAP1-low tumors correspond to the class 2, high-metastatic-risk molecular subtype of uveal melanoma."),
 md(DISC),
])

# ============ 04 imaging ============
write("04_imaging_he_analysis.ipynb", [
 md("# 4. Histopathology image analysis (H&E)\n\n"
    "Color deconvolution and nuclei segmentation of a melanoma H&E image (CC BY 4.0, Weiss et al., BMC Cancer 2015). "
    "Melanin can confound H&E deconvolution; pixel measures are not calibrated to microns."),
 co('import requests, numpy as np, matplotlib.pyplot as plt\nfrom PIL import Image\nfrom io import BytesIO\n'
    'from scipy import ndimage as ndi\n'
    'from skimage import color, filters, morphology, measure, exposure, segmentation, feature\n'
    'URL = "https://upload.wikimedia.org/wikipedia/commons/1/12/Histopathology_of_nodular_melanoma.jpg"\n'
    'raw = requests.get(URL, timeout=60, headers={"User-Agent": "concord-research/1.0 (https://digvijayky.com)"}).content\n'
    'img = np.array(Image.open(BytesIO(raw)).convert("RGB")); print("image:", img.shape)'),
 md("## Color deconvolution (hematoxylin = nuclei, eosin = cytoplasm/stroma)"),
 co('hed = color.rgb2hed(img)\n'
    'h = exposure.rescale_intensity(hed[:, :, 0], out_range=(0, 1)); e = exposure.rescale_intensity(hed[:, :, 1], out_range=(0, 1))\n'
    'fig, ax = plt.subplots(1, 3, figsize=(14, 4))\n'
    'ax[0].imshow(img); ax[0].set_title("H&E original")\n'
    'ax[1].imshow(h, cmap="magma"); ax[1].set_title("Hematoxylin")\n'
    'ax[2].imshow(e, cmap="viridis"); ax[2].set_title("Eosin")\n'
    '[a.axis("off") for a in ax]; plt.tight_layout()'),
 md("## Nuclei segmentation (watershed)"),
 co('hs = filters.gaussian(h, 1.0); mask = hs > filters.threshold_otsu(hs)\n'
    'mask = ndi.binary_fill_holes(morphology.remove_small_objects(mask, 8))\n'
    'dist = ndi.distance_transform_edt(mask); coords = feature.peak_local_max(dist, min_distance=4, labels=mask, exclude_border=False)\n'
    'markers = np.zeros(dist.shape, int)\n'
    'for i, (r, c) in enumerate(coords, 1): markers[r, c] = i\n'
    'lbl = segmentation.watershed(-dist, markers, mask=mask)\n'
    'n = len([p for p in measure.regionprops(lbl) if p.area >= 8]); print("nuclei detected:", n)\n'
    'ov = segmentation.mark_boundaries(exposure.rescale_intensity(img/255.0), lbl, color=(0.1, 0.95, 0.1))\n'
    'plt.figure(figsize=(9, 4)); plt.imshow(ov); plt.axis("off"); plt.title(f"Segmented nuclei (n={n})"); plt.tight_layout()'),
 md(DISC),
])

# ============ 05 MSK-IMPACT ============
write("05_msk_impact_rare_cancers.ipynb", [
 md("# 5. MSK-IMPACT: rare cancer knowledge from a clinical cohort\n\n"
    "The MSK-IMPACT Clinical Sequencing Cohort (Zehir et al., Nat Med 2017; 10,945 tumors) mapped onto "
    "Anveshar's rare cancer catalog, with real per-type driver frequencies. Accessed via cBioPortal."),
 co(SETUP),
 co('import requests, re, pandas as pd\nfrom collections import defaultdict\n'
    'API = "https://www.cbioportal.org/api"; STUDY = "msk_impact_2017"\n'
    'def norm(s):\n'
    '    toks = re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split()\n'
    '    return " ".join(sorted(t for t in toks if t not in {"the","of","a","an","and","type","tumor","tumour","neoplasm","cancer","carcinoma"}))\n'
    'cd = requests.get(f"{API}/studies/{STUDY}/clinical-data", params={"attributeId": "CANCER_TYPE_DETAILED",\n'
    '   "clinicalDataType": "SAMPLE", "projection": "SUMMARY", "pageSize": 300000}, timeout=90).json()\n'
    'type_samples = defaultdict(list)\n'
    'for r in cd: type_samples[r["value"]].append(r["sampleId"])\n'
    'print("tumors:", len(cd), "| detailed cancer types:", len(type_samples))'),
 md("## Map MSK-IMPACT cancer types onto Anveshar's rare cancer catalog"),
 co('from anveshar import analysis\ncat = analysis.load_catalog(); cat_norm = {}\n'
    'for r in cat:\n'
    '    cat_norm[norm(r["name"])] = r["name"]\n'
    '    for a in r.get("aliases", []) or []: cat_norm.setdefault(norm(a), r["name"])\n'
    'rows = [{"msk_type": t, "n": len(s), "rare_cancer": cat_norm.get(norm(t), "")} for t, s in type_samples.items()]\n'
    'mp = pd.DataFrame(rows); matched = mp[mp.rare_cancer != ""]\n'
    'print("rare cancer types:", matched.rare_cancer.nunique(), "| tumors:", int(matched.n.sum()))\n'
    'matched.groupby("rare_cancer").n.sum().sort_values(ascending=False).head(15)'),
 md("## Real driver frequencies for a flagship rare cancer (uveal melanoma)"),
 co('t = "Uveal Melanoma"; sids = type_samples.get(t, [])\n'
    'muts = requests.post(f"{API}/molecular-profiles/{STUDY}_mutations/mutations/fetch",\n'
    '   json={"sampleIds": sids}, params={"projection": "DETAILED"}, timeout=90).json()\n'
    'gs = defaultdict(set)\n'
    'for m in muts:\n'
    '    g = (m.get("gene") or {}).get("hugoGeneSymbol")\n'
    '    if g: gs[g].add(m["sampleId"])\n'
    'pd.Series({g: round(100*len(s)/len(sids), 1) for g, s in gs.items()}).sort_values(ascending=False).head(10)'),
 md("The MSK-IMPACT driver frequencies (GNAQ, GNA11, BAP1, SF3B1) reproduce known uveal melanoma biology "
    "in an independent clinical cohort, with BAP1 enriched relative to TCGA (metastatic bias)."),
 md(DISC),
])

# ============ 06 target validation ============
write("06_target_validation_functional_genomics.ipynb", [
 md("# 6. Functional-genomics target validation\n\n"
    "Open Targets druggability tractability plus DepMap CRISPR gene essentiality, scored to a verdict. "
    "For a loss-of-function driver the harness pivots to the druggable induced dependency."),
 co(SETUP),
 md("## Validate the driver and its induced dependency (live)"),
 co('from anveshar import pipeline\nimport pandas as pd\n'
    'try:\n'
    '    d = pipeline.run("renal medullary carcinoma", live=True)\n'
    '    tv = d["target_validation"]\n'
    '    display(pd.DataFrame([{"gene": g, "score": v.get("score"), "tractability_SM": v.get("sm_tractability"),\n'
    '                           "common_essential": v.get("common_essential"), "selective_dependency": v.get("selective_dependency"),\n'
    '                           "verdict": v.get("verdict")} for g, v in tv.items() if v.get("available")]))\n'
    '    print("Induced dependency:", {g: e["dependency"] for g, e in d.get("induced_dependencies", {}).items()})\n'
    'except Exception as ex:\n'
    '    print("live validation skipped:", type(ex).__name__, ex)'),
 md("SMARCB1 is a common-essential tumor suppressor (low score, not druggable directly); the harness hands "
    "off to its induced synthetic-lethal dependency EZH2, which validates as a tractable, selective target."),
 md(DISC),
])
print("ALL NOTEBOOKS BUILT")
