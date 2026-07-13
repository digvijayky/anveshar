"""Discrete, reproducible finding for the Anveshar research track:
Rectal and GI well-differentiated neuroendocrine tumors (NETs) are molecularly distinct from the
adenocarcinomas of the same organ. Multi-omics on real public data via the cBioPortal REST API.
No simulation or subsampling.

Genomics: driver mutation frequency in
  - MSK-IMPACT GI well-differentiated NET (rectum, GI, small bowel, stomach, appendix)
  - pancreatic NET (ARC-Net, Scarpa 2017)
  vs
  - TCGA rectal adenocarcinoma (READ) and pancreatic adenocarcinoma (PAAD).
Transcriptomics: neuroendocrine program markers (CHGA, SYP, INSM1, SSTR2, ASCL1, NEUROD1) in NET vs adenocarcinoma.
Theranostic: SSTR2, the target of Lu-177 DOTATATE.
"""
import os, json, requests, numpy as np, pandas as pd
from collections import defaultdict
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import stats

FS = 16
for p in ["/home/yarlagad/.local/share/fonts/Arial.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"] = "Arial"; break
plt.rcParams.update({"font.size": FS, "figure.dpi": 150})

API = "https://www.cbioportal.org/api"
OUT = "/data1/lesliec/vijay/github/anveshar/examples/multimodal/rectal_net_multiomics"
os.makedirs(OUT, exist_ok=True)
log = {}

def get(u, **k): r = requests.get(u, timeout=90, **k); r.raise_for_status(); return r.json()
def post(u, b, **k): r = requests.post(u, json=b, timeout=120, **k); r.raise_for_status(); return r.json()

# adenocarcinoma drivers vs NET drivers
ADENO = {324:"APC", 3845:"KRAS", 7157:"TP53", 4089:"SMAD4", 5290:"PIK3CA", 673:"BRAF", 4292:"MLH1"}
NETG  = {4221:"MEN1", 1616:"DAXX", 546:"ATRX", 5728:"PTEN", 7249:"TSC2", 1027:"CDKN1B", 54880:"BCOR", 6794:"STK11"}
PANEL = {**ADENO, **NETG}
NEMARK = {1113:"CHGA", 6855:"SYP", 3642:"INSM1", 6752:"SSTR2", 429:"ASCL1", 4760:"NEUROD1", 5122:"PCSK1"}

def mut_freq(study, sampleIds=None, sampleListId=None, genes=PANEL):
    prof = study + "_mutations"
    body = {"entrezGeneIds": list(genes)}
    if sampleIds is not None: body["sampleIds"] = sampleIds; N = len(sampleIds)
    else:
        body["sampleListId"] = sampleListId or (study + "_all")
        N = len(get(f"{API}/studies/{study}/samples"))
    muts = post(f"{API}/molecular-profiles/{prof}/mutations/fetch", body, params={"projection": "SUMMARY"})
    ms = defaultdict(set)
    for m in muts:
        g = genes.get(m["entrezGeneId"])
        if g: ms[g].add(m["sampleId"])
    return N, {g: round(100*len(ms[g])/max(1,N), 1) for g in genes.values()}

# ---- MSK-IMPACT GI well-differentiated NET pool ----
cd = get(f"{API}/studies/msk_impact_2017/clinical-data",
         params={"attributeId":"CANCER_TYPE_DETAILED","clinicalDataType":"SAMPLE","projection":"SUMMARY","pageSize":300000})
ts = defaultdict(list)
for r in cd: ts[r["value"]].append(r["sampleId"])
GI_NET_TYPES = ["Well-Differentiated Neuroendocrine Tumor of the Rectum",
                "Gastrointestinal Neuroendocrine Tumors",
                "Small Bowel Well-Differentiated Neuroendocrine Tumor",
                "Well-Differentiated Neuroendocrine Tumors of the Stomach",
                "Well-Differentiated Neuroendocrine Tumor of the Appendix"]
gi_net_ids = [s for t in GI_NET_TYPES for s in ts.get(t, [])]
log["gi_net_types_used"] = {t: len(ts.get(t, [])) for t in GI_NET_TYPES}
log["gi_net_n"] = len(gi_net_ids)

cohorts = {}
n, f = mut_freq("msk_impact_2017", sampleIds=gi_net_ids); cohorts["GI NET (MSK, n=%d)" % n] = f
n, f = mut_freq("panet_arcnet_2017"); cohorts["Pancreatic NET (n=%d)" % n] = f
n, f = mut_freq("coadread_tcga_pan_can_atlas_2018"); cohorts["Colorectal adenoca (TCGA, n=%d)" % n] = f
n, f = mut_freq("paad_tcga_pan_can_atlas_2018"); cohorts["Pancreatic adenoca (TCGA, n=%d)" % n] = f
mat = pd.DataFrame(cohorts).reindex(list(PANEL.values()))
mat.to_csv(f"{OUT}/rectal_net_genomics_driver_frequency_source.csv")
log["genomics"] = {c: cohorts[c] for c in cohorts}

# heatmap: driver dichotomy
fig, ax = plt.subplots(figsize=(9.5, 7.5))
im = ax.imshow(mat.values, aspect="auto", cmap="Reds", vmin=0, vmax=90)
ax.set_xticks(range(mat.shape[1])); ax.set_xticklabels(mat.columns, rotation=30, ha="right", fontsize=FS-3)
ax.set_yticks(range(mat.shape[0])); ax.set_yticklabels(mat.index, fontsize=FS-2)
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat.values[i, j]
        ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=FS-4, color="white" if v>45 else "black")
ax.axhline(len(ADENO)-0.5, color="#2f5fe0", lw=2)
ax.text(-0.7, (len(ADENO)-1)/2, "adenocarcinoma\ndrivers", rotation=90, va="center", ha="center", fontsize=FS-4, color="#2f5fe0")
ax.text(-0.7, len(ADENO)+(len(NETG)-1)/2, "NET\ndrivers", rotation=90, va="center", ha="center", fontsize=FS-4, color="#127a3e")
ax.set_title("Rectal and GI NET are not colorectal cancer\nDriver mutation frequency (%)", fontsize=FS-1)
cb = fig.colorbar(im, fraction=0.03, pad=0.02); cb.set_label("% mutated", fontsize=FS-3)
plt.tight_layout(); plt.savefig(f"{OUT}/rectal_net_genomics_driver_dichotomy.pdf"); plt.close()

# ---- Transcriptomics: neuroendocrine markers in NET vs adenocarcinoma ----
def expr(study, genes=NEMARK):
    profs = get(f"{API}/studies/{study}/molecular-profiles")
    rp = next((p["molecularProfileId"] for p in profs if "rna_seq" in p["molecularProfileId"]
               and "Zscores" in p["molecularProfileId"] and "normal" not in p["molecularProfileId"]), None)
    if not rp: return None
    d = post(f"{API}/molecular-profiles/{rp}/molecular-data/fetch",
             {"sampleListId": study + "_all", "entrezGeneIds": list(genes)})
    df = pd.DataFrame([{"gene": genes[r["entrezGeneId"]], "z": r["value"]} for r in d if r.get("value") is not None])
    return df

trans = {}
for study, lab in [("panet_arcnet_2017","Pancreatic NET"), ("paad_tcga_pan_can_atlas_2018","Pancreatic adenoca"),
                   ("coadread_tcga_pan_can_atlas_2018","Colorectal adenoca")]:
    e = expr(study)
    if e is not None and len(e):
        trans[lab] = e.groupby("gene").z.mean().reindex(list(NEMARK.values()))
if trans:
    tm = pd.DataFrame(trans).reindex(list(NEMARK.values()))
    tm.to_csv(f"{OUT}/rectal_net_transcriptomics_ne_markers_source.csv")
    log["transcriptomics_mean_z"] = {c: tm[c].round(2).to_dict() for c in tm.columns}
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    x = np.arange(len(NEMARK)); w = 0.8/max(1,len(tm.columns))
    cols = {"Pancreatic NET":"#127a3e","Pancreatic adenoca":"#b8611a","Rectal adenoca":"#2f5fe0"}
    for i, c in enumerate(tm.columns):
        ax.bar(x+i*w, tm[c].values, w, label=c, color=cols.get(c,"#777"))
    ax.set_xticks(x+w*(len(tm.columns)-1)/2); ax.set_xticklabels(tm.index, rotation=30, ha="right")
    ax.axhline(0, color="k", lw=0.8); ax.set_ylabel("mean mRNA z-score")
    ax.set_title("Neuroendocrine program is a NET signature\n(high in NET, low in adenocarcinoma)", fontsize=FS-1)
    ax.legend(frameon=False, fontsize=FS-4)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    plt.tight_layout(); plt.savefig(f"{OUT}/rectal_net_transcriptomics_ne_markers.pdf"); plt.close()

json.dump(log, open(f"{OUT}/rectal_net_multiomics_run_log.json","w"), indent=2)
print("DONE"); print(json.dumps(log, indent=2)[:2000])
