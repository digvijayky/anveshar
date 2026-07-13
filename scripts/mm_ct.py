"""Reusable real-data genomics + transcriptomics analysis for a rare cancer via cBioPortal.
Usage: python3 mm_ct.py <config_key>. Real TCGA data, no simulation. Auto-detects profiles.
"""
import os, sys, json, requests, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, leaves_list

FS = 16
for p in ["/home/yarlagad/.local/share/fonts/Arial.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"] = "Arial"; break
plt.rcParams.update({"font.size": FS, "axes.titlesize": FS, "axes.labelsize": FS,
                     "xtick.labelsize": FS, "ytick.labelsize": FS, "legend.fontsize": FS, "figure.dpi": 150})

CONFIGS = {
    "adrenocortical_carcinoma": {
        "study": "acc_tcga_pan_can_atlas_2018", "title": "Adrenocortical carcinoma",
        "panel": {7157: "TP53", 1499: "CTNNB1", 84133: "ZNRF3", 1029: "CDKN2A",
                  4221: "MEN1", 5925: "RB1", 7015: "TERT"}, "split_gene": "CTNNB1"},
    "mesothelioma": {
        "study": "meso_tcga_pan_can_atlas_2018", "title": "Pleural mesothelioma",
        "panel": {8314: "BAP1", 4771: "NF2", 1029: "CDKN2A", 7157: "TP53",
                  5728: "PTEN", 60: "ACTB"}, "split_gene": "BAP1"},
}
key = sys.argv[1] if len(sys.argv) > 1 else "adrenocortical_carcinoma"
cfg = CONFIGS[key]; STUDY = cfg["study"]; PANEL = cfg["panel"]; SAMPLES = STUDY + "_all"
BASE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/github/concord/examples/multimodal"
OUT = f"{BASE}/{key}"; os.makedirs(OUT, exist_ok=True)
API = "https://www.cbioportal.org/api"; log = {"study": STUDY}

def get(u, **k): r = requests.get(u, timeout=40, **k); r.raise_for_status(); return r.json()
def post(u, b, **k): r = requests.post(u, json=b, timeout=60, **k); r.raise_for_status(); return r.json()

N = len(get(f"{API}/studies/{STUDY}/samples")); log["n_samples"] = N
profs = get(f"{API}/studies/{STUDY}/molecular-profiles")
mut_prof = next(p["molecularProfileId"] for p in profs if p["molecularAlterationType"] == "MUTATION_EXTENDED")
rna_prof = next((p["molecularProfileId"] for p in profs if "rna_seq" in p["molecularProfileId"]
                 and "median_Zscores" in p["molecularProfileId"] and "normal" not in p["molecularProfileId"]), None)
log["mutation_profile"] = mut_prof; log["rna_profile"] = rna_prof

# genomics
muts = post(f"{API}/molecular-profiles/{mut_prof}/mutations/fetch",
            {"sampleListId": SAMPLES, "entrezGeneIds": list(PANEL)}, params={"projection": "SUMMARY"})
ms = {g: set() for g in PANEL.values()}
for m in muts:
    g = PANEL.get(m["entrezGeneId"])
    if g: ms[g].add(m["sampleId"])
freq = pd.DataFrame({"gene": list(PANEL.values()),
                     "pct_mutated": [round(100*len(ms[g])/N, 1) for g in PANEL.values()]}).sort_values("pct_mutated", ascending=False)
freq.to_csv(f"{OUT}/{key}_genomics_mutation_frequency_source.csv", index=False)
log["genomics_freq"] = freq.set_index("gene")["pct_mutated"].to_dict()
fig, ax = plt.subplots(figsize=(7.2, 5))
ax.bar(freq["gene"], freq["pct_mutated"], color="#7b3fe4")
for i, v in enumerate(freq["pct_mutated"]): ax.text(i, v+1.2, f"{v:.0f}", ha="center", fontsize=FS-2)
ax.set_ylabel("Samples mutated (%)"); ax.set_ylim(0, max(60, freq["pct_mutated"].max()+12))
ax.set_title(f"{cfg['title']} driver mutations\nTCGA PanCancer, n={N}"); plt.xticks(rotation=40, ha="right")
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(f"{OUT}/{key}_genomics_mutation_frequency.pdf"); plt.close()

# transcriptomics
if rna_prof:
    rna = post(f"{API}/molecular-profiles/{rna_prof}/molecular-data/fetch",
               {"sampleListId": SAMPLES, "entrezGeneIds": list(PANEL)})
    df = pd.DataFrame([{"sample": r["sampleId"], "gene": PANEL.get(r["entrezGeneId"]), "z": r["value"]} for r in rna])
    mat = df.pivot_table(index="gene", columns="sample", values="z").reindex(list(PANEL.values())).dropna(how="all")
    mat.to_csv(f"{OUT}/{key}_transcriptomics_driver_zscores_source.csv")
    log["transcriptomics"] = {"n_genes": int(mat.shape[0]), "n_samples": int(mat.shape[1])}
    X = np.nan_to_num(mat.values); order = leaves_list(linkage(X.T, method="ward")) if X.shape[1] > 2 else np.arange(X.shape[1])
    fig, ax = plt.subplots(figsize=(9, 4.2))
    im = ax.imshow(X[:, order], aspect="auto", cmap="RdBu_r", vmin=-2.5, vmax=2.5)
    ax.set_yticks(range(mat.shape[0])); ax.set_yticklabels(mat.index); ax.set_xticks([])
    ax.set_xlabel(f"{cfg['title']} samples (n={mat.shape[1]})"); ax.set_title("Driver gene mRNA (z-score), clustered")
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02); cb.set_label("z-score", fontsize=FS-2)
    plt.tight_layout(); plt.savefig(f"{OUT}/{key}_transcriptomics_driver_heatmap.pdf"); plt.close()
    sg = cfg["split_gene"]
    if sg in mat.index:
        p = PCA(n_components=2).fit_transform(np.nan_to_num(mat.T.values))
        v = mat.loc[sg]; med = v.median(); status = np.where(v < med, f"{sg}-low", f"{sg}-high")
        pd.DataFrame({"sample": mat.columns, "PC1": p[:,0], "PC2": p[:,1], f"{sg}_status": status,
                      f"{sg}_z": v.values}).to_csv(f"{OUT}/{key}_transcriptomics_pca_source.csv", index=False)
        fig, ax = plt.subplots(figsize=(6.6, 5.4))
        for lab, c in [(f"{sg}-low", "#c0392b"), (f"{sg}-high", "#2f5fe0")]:
            m2 = status == lab; ax.scatter(p[m2,0], p[m2,1], c=c, s=55, edgecolor="w", lw=0.5, label=lab)
        ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.legend(frameon=False)
        ax.set_title(f"{cfg['title']} transcriptomes by {sg}")
        for s in ["top","right"]: ax.spines[s].set_visible(False)
        plt.tight_layout(); plt.savefig(f"{OUT}/{key}_transcriptomics_{sg}_pca.pdf"); plt.close()

json.dump(log, open(f"{OUT}/{key}_run_log.json", "w"), indent=2)
open(f"{OUT}/{key}_methodology_and_legend.txt", "w").write(
    f"""{cfg['title']} (rare cancer) genomics and transcriptomics on real public data.
Source: TCGA {cfg['title']} PanCancer Atlas (study {STUDY}), cBioPortal REST API, n={N} tumors,
no simulation or subsampling. Genomics: driver mutation frequency across {', '.join(PANEL.values())}.
Transcriptomics: driver mRNA z-scores clustered across tumors and projected by PCA, split at the
median of {cfg['split_gene']}. This is a research and educational analysis of public data, not medical
advice; clinical decisions must be made by a qualified health care provider.
""")
print("DONE", key); print(json.dumps(log, indent=2))
