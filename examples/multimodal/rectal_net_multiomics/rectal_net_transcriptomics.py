import os, json, requests, numpy as np, pandas as pd
from collections import defaultdict
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
for p in ["/home/yarlagad/.local/share/fonts/Arial.ttf"]:
    if os.path.exists(p): font_manager.fontManager.addfont(p); plt.rcParams["font.family"]="Arial"
plt.rcParams.update({"font.size":16,"figure.dpi":150})
API="https://www.cbioportal.org/api"; OUT="/data1/lesliec/vijay/github/anveshar/examples/multimodal/rectal_net_multiomics"
NEMARK={1113:"CHGA",6855:"SYP",3642:"INSM1",6752:"SSTR2",429:"ASCL1",4760:"NEUROD1"}
def post(u,b,**k): r=requests.post(u,json=b,timeout=120,**k); r.raise_for_status(); return r.json()
def get(u,**k): r=requests.get(u,timeout=90,**k); r.raise_for_status(); return r.json()
# COADREAD neuroendocrine score per sample (valid within-study z)
study="coadread_tcga_pan_can_atlas_2018"
rp=next(p["molecularProfileId"] for p in get(f"{API}/studies/{study}/molecular-profiles")
        if "rna_seq" in p["molecularProfileId"] and "median_Zscores" in p["molecularProfileId"] and "normal" not in p["molecularProfileId"])
d=post(f"{API}/molecular-profiles/{rp}/molecular-data/fetch",{"sampleListId":study+"_all","entrezGeneIds":list(NEMARK)})
bysamp=defaultdict(dict)
for r in d:
    if r.get("value") is not None: bysamp[r["sampleId"]][NEMARK[r["entrezGeneId"]]]=r["value"]
rows=[np.mean(list(v.values())) for v in bysamp.values() if len(v)>=4]
ne=np.array(rows); N=len(ne); frac_hi=round(100*float((ne>1).mean()),1)
pd.DataFrame({"ne_score":ne}).to_csv(f"{OUT}/rectal_net_coadread_ne_score_source.csv",index=False)
fig,ax=plt.subplots(figsize=(7.5,5))
ax.hist(ne,bins=40,color="#2f5fe0",alpha=.85)
ax.axvline(1,color="#c0392b",lw=2,ls="--"); ax.text(1.05,ax.get_ylim()[1]*0.85,f"NE-high\n{frac_hi}% of tumors",color="#c0392b",fontsize=12)
ax.set_xlabel("neuroendocrine program score (mean z of CHGA, SYP, INSM1, SSTR2, ASCL1, NEUROD1)")
ax.set_ylabel("colorectal adenocarcinomas")
ax.set_title(f"The neuroendocrine program is absent from\ncolorectal adenocarcinoma (TCGA, n={N})",fontsize=15)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(f"{OUT}/rectal_net_transcriptomics_ne_score.pdf"); plt.close()
print("DONE coadread N=",N,"frac NE-high=",frac_hi)
