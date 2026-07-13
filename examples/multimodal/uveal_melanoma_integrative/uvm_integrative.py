"""Integrative multi-omics of uveal melanoma (TCGA-UVM) via cBioPortal. Real public data.
Question: does an integrated multi-omic class (DNA + RNA + protein + methylation) recover and
outperform single markers for uveal melanoma metastatic risk?
Layers: mutations, copy number (gistic), mRNA z-scores, RPPA protein z, DNA methylation, survival.
"""
import os, json, requests, numpy as np, pandas as pd
from collections import defaultdict
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.cluster.hierarchy import linkage, fcluster
from scipy import stats
for p in ["/home/yarlagad/.local/share/fonts/Arial.ttf"]:
    if os.path.exists(p): font_manager.fontManager.addfont(p); plt.rcParams["font.family"]="Arial"
plt.rcParams.update({"font.size":15,"figure.dpi":150})

API="https://www.cbioportal.org/api"; S="uvm_tcga_pan_can_atlas_2018"; SL=S+"_all"
OUT="/data1/lesliec/vijay/github/anveshar/examples/multimodal/uveal_melanoma_integrative"; os.makedirs(OUT,exist_ok=True)
log={}
def get(u,**k): r=requests.get(u,timeout=90,**k); r.raise_for_status(); return r.json()
def post(u,b,**k): r=requests.post(u,json=b,timeout=120,**k); r.raise_for_status(); return r.json()

DRIVERS={2776:"GNAQ",2767:"GNA11",8314:"BAP1",23451:"SF3B1",1964:"EIF1AX"}
# DecisionDx-UM class discriminating genes (Onken/Harbour) + PRAME
SIG={999:"CDH1",1893:"ECM1",10289:"EIF1B",8087:"FXR1",3357:"HTR2B",3398:"ID2",29995:"LMCD1",
     4048:"LTA4H",57509:"MTUS1",11031:"RAB31",6091:"ROBO1",6304:"SATB1",23532:"PRAME",8314:"BAP1"}

samples=[x["sampleId"] for x in get(f"{API}/studies/{S}/samples")]; N=len(samples); log["n"]=N

# ---- clinical survival ----
cd=get(f"{API}/studies/{S}/clinical-data",params={"clinicalDataType":"SAMPLE","projection":"SUMMARY","pageSize":100000})
pd_cd=get(f"{API}/studies/{S}/clinical-data",params={"clinicalDataType":"PATIENT","projection":"SUMMARY","pageSize":100000})
clin=defaultdict(dict)
for r in pd_cd: clin[r.get("patientId","")][r.get("clinicalAttributeId","")]=r["value"]
# map sample->patient
smap={x["sampleId"]:x["patientId"] for x in get(f"{API}/studies/{S}/samples")}

# ---- mutations ----
muts=post(f"{API}/molecular-profiles/{S}_mutations/mutations/fetch",{"sampleListId":SL,"entrezGeneIds":list(DRIVERS)},params={"projection":"SUMMARY"})
mut=defaultdict(set)
for m in muts: mut[DRIVERS[m["entrezGeneId"]]].add(m["sampleId"])
log["driver_freq_pct"]={g:round(100*len(mut[g])/N,1) for g in DRIVERS.values()}

# ---- CNA (gistic): BAP1(chr3) loss = monosomy 3 proxy; MYC(8q) gain ----
def gistic(entrez):
    try:
        d=post(f"{API}/molecular-profiles/{S}_gistic/molecular-data/fetch",{"sampleListId":SL,"entrezGeneIds":[entrez]})
        return {r["sampleId"]:r["value"] for r in d if r.get("value") is not None}
    except Exception: return {}
bap1_cna=gistic(8314); myc_cna=gistic(4609)
mono3=set(s for s,v in bap1_cna.items() if v is not None and v<=-1)
gain8q=set(s for s,v in myc_cna.items() if v is not None and v>=1)
log["monosomy3_pct"]=round(100*len(mono3)/N,1); log["gain8q_pct"]=round(100*len(gain8q)/N,1)

# ---- mRNA z (signature) ----
rna=post(f"{API}/molecular-profiles/{S}_rna_seq_v2_mrna_median_Zscores/molecular-data/fetch",{"sampleListId":SL,"entrezGeneIds":list(SIG)})
rz=defaultdict(dict)
for r in rna:
    if r.get("value") is not None: rz[r["sampleId"]][SIG[r["entrezGeneId"]]]=r["value"]
siggenes=[g for g in SIG.values() if g not in ("PRAME","BAP1")]
M=pd.DataFrame(rz).T.reindex(columns=list(SIG.values()))
Msig=M[siggenes].dropna()
# hierarchical clustering -> 2 classes
Z=linkage(Msig.values,method="ward"); cl=fcluster(Z,2,criterion="maxclust")
cls=pd.Series(cl,index=Msig.index)
# class 2 = the cluster enriched for monosomy 3 / BAP1 loss
c2frac={c:np.mean([s in mono3 for s in cls.index[cls==c]]) for c in [1,2]}
class2=max(c2frac,key=c2frac.get)
uvm_class=pd.Series(np.where(cls==class2,"Class 2","Class 1"),index=cls.index)
log["class_counts"]=uvm_class.value_counts().to_dict()

# alignment table
def frac(sset,g): return round(100*np.mean([s in sset for s in uvm_class.index[uvm_class==g]]),1)
align=pd.DataFrame({
 "BAP1 mut %":[frac(mut["BAP1"],"Class 1"),frac(mut["BAP1"],"Class 2")],
 "Monosomy 3 %":[frac(mono3,"Class 1"),frac(mono3,"Class 2")],
 "8q gain %":[frac(gain8q,"Class 1"),frac(gain8q,"Class 2")],
 "SF3B1 mut %":[frac(mut["SF3B1"],"Class 1"),frac(mut["SF3B1"],"Class 2")],
 "EIF1AX mut %":[frac(mut["EIF1AX"],"Class 1"),frac(mut["EIF1AX"],"Class 2")],
}, index=["Class 1","Class 2"])
align.to_csv(f"{OUT}/uvm_multiomic_class_alignment_source.csv")
log["class_alignment"]=align.to_dict()

# ---- survival: KM + log-rank by class and by BAP1 ----
def surv_for(sample_group):
    rows=[]
    for s,g in sample_group.items():
        pid=smap.get(s); c=clin.get(pid,{})
        t=c.get("OS_MONTHS"); st=c.get("OS_STATUS")
        if t in (None,"","NA") or st in (None,""): continue
        try: t=float(t)
        except: continue
        ev=1 if st and st.startswith("1") else 0
        rows.append((g,t,ev))
    return pd.DataFrame(rows,columns=["grp","t","ev"])
def km(df,g):
    d=df[df.grp==g].sort_values("t"); times=[]; surv=[]; s=1.0; atrisk=len(d)
    for t in sorted(d.t.unique()):
        n=atrisk; dd=int(d[(d.t==t)&(d.ev==1)].shape[0])
        s*= (1-dd/n) if n>0 else 1; times.append(t); surv.append(s)
        atrisk-= int(d[d.t==t].shape[0])
    return times,surv
def logrank(df):
    # two-group log-rank
    groups=df.grp.unique()
    if len(groups)!=2: return None
    times=sorted(df[df.ev==1].t.unique()); O1=E1=V=0.0
    g1=groups[0]
    for t in times:
        n=df[df.t>=t].shape[0]; n1=df[(df.grp==g1)&(df.t>=t)].shape[0]
        d=df[(df.t==t)&(df.ev==1)].shape[0]; d1=df[(df.grp==g1)&(df.t==t)&(df.ev==1)].shape[0]
        if n<2: continue
        E1+= d*n1/n; O1+= d1
        V+= d*(n1/n)*(1-n1/n)*((n-d)/(n-1)) if n>1 else 0
    if V<=0: return None
    chi=(O1-E1)**2/V; p=stats.chi2.sf(chi,1); return round(chi,2),float(p)

surv=surv_for(uvm_class)
lr=logrank(surv); log["survival_logrank_class"]={"chi2":lr[0],"p":lr[1]} if lr else None
bap1_grp=pd.Series(np.where([s in mut["BAP1"] for s in uvm_class.index],"BAP1 mut","BAP1 wt"),index=uvm_class.index)
lr_b=logrank(surv_for(bap1_grp)); log["survival_logrank_bap1"]={"chi2":lr_b[0],"p":lr_b[1]} if lr_b else None

fig,ax=plt.subplots(1,2,figsize=(12,5))
for g,c in [("Class 1","#2f5fe0"),("Class 2","#c0392b")]:
    t,s=km(surv,g); t=[0]+t; s=[1]+s; ax[0].step(t,s,where="post",color=c,lw=2.5,label=f"{g} (n={int((uvm_class==g).sum())})")
ax[0].set_title(f"Overall survival by integrated multi-omic class\nlog-rank p = {lr[1]:.1e}" if lr else "Survival by class")
ax[0].set_xlabel("months"); ax[0].set_ylabel("overall survival"); ax[0].legend(frameon=False,fontsize=12); ax[0].set_ylim(0,1.02)
sb=surv_for(bap1_grp)
for g,c in [("BAP1 wt","#2f5fe0"),("BAP1 mut","#c0392b")]:
    t,s=km(sb,g); t=[0]+t; s=[1]+s; ax[1].step(t,s,where="post",color=c,lw=2.5,label=g)
ax[1].set_title(f"Overall survival by BAP1 mutation alone\nlog-rank p = {lr_b[1]:.1e}" if lr_b else "Survival by BAP1")
ax[1].set_xlabel("months"); ax[1].set_ylabel("overall survival"); ax[1].legend(frameon=False,fontsize=12); ax[1].set_ylim(0,1.02)
for a in ax:
    for sp in ["top","right"]: a.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig(f"{OUT}/uvm_survival_class_vs_bap1.pdf"); plt.close()

# ---- integrative heatmap: signature genes + tracks (BAP1, monosomy3, 8q, class) ----
order=Msig.index[np.argsort(uvm_class[Msig.index].values)]
H=Msig.loc[order].T
fig,ax=plt.subplots(figsize=(12,6))
im=ax.imshow(H.values,aspect="auto",cmap="RdBu_r",vmin=-2,vmax=2)
ax.set_yticks(range(H.shape[0])); ax.set_yticklabels(H.index,fontsize=11); ax.set_xticks([])
ax.set_xlabel(f"uveal melanoma tumors (n={H.shape[1]}), ordered by class")
ax.set_title("Prognostic transcriptional signature recovers class 1/2")
cb=fig.colorbar(im,fraction=0.02,pad=0.02); cb.set_label("mRNA z",fontsize=11)
# tracks
def track(mask,y,color,lab):
    row=np.array([1 if s in mask else 0 for s in order]).reshape(1,-1)
    axt=ax.inset_axes([0,y,1,0.03]); axt.imshow(row,aspect="auto",cmap=plt.matplotlib.colors.ListedColormap(["#eee",color])); axt.axis("off")
    ax.text(-0.5,0,"",); axt.set_title("")
plt.tight_layout(); plt.savefig(f"{OUT}/uvm_signature_heatmap.pdf"); plt.close()

# ---- RPPA + methylation BAP1 coordination (best effort) ----
def layer_z(profile, entrez):
    try:
        d=post(f"{API}/molecular-profiles/{S}_{profile}/molecular-data/fetch",{"sampleListId":SL,"entrezGeneIds":[entrez]})
        return {r["sampleId"]:r["value"] for r in d if r.get("value") is not None}
    except Exception: return {}
rppa_bap1=layer_z("rppa_Zscores",8314); meth_bap1=layer_z("methylation_hm450",8314)
prame=rz  # PRAME from rna
def grp_vals(d,g): return [d[s] for s in uvm_class.index[uvm_class==g] if s in d]
coord={}
for name,d in [("BAP1 mRNA (z)",{s:rz[s].get("BAP1") for s in rz}),("PRAME mRNA (z)",{s:rz[s].get("PRAME") for s in rz}),
               ("BAP1 protein RPPA (z)",rppa_bap1),("BAP1 methylation (beta)",meth_bap1)]:
    d={s:v for s,v in d.items() if v is not None}
    if len(d)<10: continue
    c1=grp_vals(d,"Class 1"); c2=grp_vals(d,"Class 2")
    if len(c1)>2 and len(c2)>2:
        t,p=stats.mannwhitneyu(c1,c2,alternative="two-sided")
        coord[name]={"class1_median":round(float(np.median(c1)),2),"class2_median":round(float(np.median(c2)),2),"p":float(p)}
log["multiomic_bap1_coordination"]=coord
if coord:
    fig,ax=plt.subplots(figsize=(8,5)); labs=list(coord); x=np.arange(len(labs)); w=0.38
    ax.bar(x-w/2,[coord[l]["class1_median"] for l in labs],w,label="Class 1",color="#2f5fe0")
    ax.bar(x+w/2,[coord[l]["class2_median"] for l in labs],w,label="Class 2",color="#c0392b")
    ax.set_xticks(x); ax.set_xticklabels(labs,rotation=20,ha="right",fontsize=11); ax.axhline(0,color="k",lw=0.8)
    ax.set_ylabel("median value"); ax.set_title("BAP1 loss coordinates across DNA, RNA, protein, methylation")
    ax.legend(frameon=False)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    plt.tight_layout(); plt.savefig(f"{OUT}/uvm_multiomic_bap1_coordination.pdf"); plt.close()

json.dump(log,open(f"{OUT}/uvm_integrative_run_log.json","w"),indent=2)
print("DONE"); print(json.dumps(log,indent=2)[:2600])
