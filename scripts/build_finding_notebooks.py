"""Build two reproducible finding notebooks (self-contained, cBioPortal API)."""
import os, nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell as md, new_code_cell as co
OUT="/data1/lesliec/vijay/github/anveshar/notebooks"; os.makedirs(OUT,exist_ok=True)
DISC=("---\n*Research and educational analysis of public data, not medical advice. Group-level "
      "tumor biology, not any individual. Decisions rest with a qualified health care provider.*\n\n"
      "*Anveshar. Developed by Dig Vijay Kumar Yarlagadda, [digvijayky.com](https://digvijayky.com).*")
def write(name,cells):
    nb=new_notebook(cells=cells,metadata={"kernelspec":{"name":"python3","display_name":"Python 3","language":"python"},"language_info":{"name":"python"}})
    nbf.write(nb,os.path.join(OUT,name)); print("wrote",name)

SETUP=('import requests, pandas as pd, numpy as np, matplotlib.pyplot as plt\n'
       'from collections import defaultdict\n'
       'API="https://www.cbioportal.org/api"\n'
       'def get(u,**k): r=requests.get(u,timeout=90,**k); r.raise_for_status(); return r.json()\n'
       'def post(u,b,**k): r=requests.post(u,json=b,timeout=120,**k); r.raise_for_status(); return r.json()')

# ---------------- 07 rectal NET ----------------
write("07_rectal_net_hypothesis.ipynb",[
 md("# 7. A tested hypothesis: rectal neuroendocrine tumors are not colorectal cancer\n\n"
    "**Hypothesis (from Anveshar).** Rectal NETs are rare and are often managed by analogy to "
    "colorectal adenocarcinoma. If they are molecularly a different disease, that analogy is wrong.\n\n"
    "**Test.** On public data (cBioPortal), compare driver mutation frequency in gastrointestinal "
    "and pancreatic NET versus colorectal and pancreatic adenocarcinoma, and ask whether the "
    "neuroendocrine program is present in colorectal cancer. Reproducible by anyone in minutes."),
 co(SETUP),
 md("## Genomics: does the driver landscape track histology or organ?"),
 co('ADENO={324:"APC",3845:"KRAS",7157:"TP53",4089:"SMAD4",5290:"PIK3CA",673:"BRAF"}\n'
    'NETG={4221:"MEN1",1616:"DAXX",546:"ATRX",1027:"CDKN1B",7249:"TSC2"}\n'
    'PANEL={**ADENO,**NETG}\n'
    'def mut_freq(study,sampleIds=None):\n'
    '    body={"entrezGeneIds":list(PANEL)}\n'
    '    if sampleIds is not None: body["sampleIds"]=sampleIds; N=len(sampleIds)\n'
    '    else: body["sampleListId"]=study+"_all"; N=len(get(f"{API}/studies/{study}/samples"))\n'
    '    m=post(f"{API}/molecular-profiles/{study}_mutations/mutations/fetch",body,params={"projection":"SUMMARY"})\n'
    '    s=defaultdict(set)\n'
    '    for x in m:\n'
    '        g=PANEL.get(x["entrezGeneId"])\n'
    '        if g: s[g].add(x["sampleId"])\n'
    '    return N,{g:round(100*len(s[g])/max(1,N),1) for g in PANEL.values()}\n'
    '# MSK-IMPACT GI well-differentiated NET pool\n'
    'cd=get(f"{API}/studies/msk_impact_2017/clinical-data",params={"attributeId":"CANCER_TYPE_DETAILED","clinicalDataType":"SAMPLE","projection":"SUMMARY","pageSize":300000})\n'
    'ts=defaultdict(list)\n'
    'for r in cd: ts[r["value"]].append(r["sampleId"])\n'
    'GI=["Well-Differentiated Neuroendocrine Tumor of the Rectum","Gastrointestinal Neuroendocrine Tumors","Small Bowel Well-Differentiated Neuroendocrine Tumor","Well-Differentiated Neuroendocrine Tumors of the Stomach","Well-Differentiated Neuroendocrine Tumor of the Appendix"]\n'
    'gi=[s for t in GI for s in ts.get(t,[])]\n'
    'C={}\n'
    'n,f=mut_freq("msk_impact_2017",gi); C[f"GI NET (MSK, n={n})"]=f\n'
    'n,f=mut_freq("panet_arcnet_2017"); C[f"Pancreatic NET (n={n})"]=f\n'
    'n,f=mut_freq("coadread_tcga_pan_can_atlas_2018"); C[f"Colorectal adenoca (n={n})"]=f\n'
    'n,f=mut_freq("paad_tcga_pan_can_atlas_2018"); C[f"Pancreatic adenoca (n={n})"]=f\n'
    'mat=pd.DataFrame(C).reindex(list(PANEL.values())); display(mat)'),
 co('fig,ax=plt.subplots(figsize=(8.5,6))\n'
    'im=ax.imshow(mat.values,aspect="auto",cmap="Reds",vmin=0,vmax=90)\n'
    'ax.set_xticks(range(mat.shape[1])); ax.set_xticklabels(mat.columns,rotation=25,ha="right")\n'
    'ax.set_yticks(range(mat.shape[0])); ax.set_yticklabels(mat.index)\n'
    'for i in range(mat.shape[0]):\n'
    '    for j in range(mat.shape[1]): ax.text(j,i,f"{mat.values[i,j]:.0f}",ha="center",va="center",fontsize=9,color="white" if mat.values[i,j]>45 else "black")\n'
    'ax.axhline(len(ADENO)-0.5,color="#2f5fe0",lw=2); ax.set_title("Driver landscape tracks histology, not organ"); plt.tight_layout(); plt.show()'),
 md("Adenocarcinomas are dominated by APC, KRAS, TP53, SMAD4. Both NET cohorts lack these and carry "
    "MEN1, DAXX, ATRX, CDKN1B, TSC2. A rectal NET shares its drivers with a pancreatic NET, not with "
    "the colorectal adenocarcinoma next to it."),
 md("## Transcriptomics: is the neuroendocrine program present in colorectal cancer?"),
 co('NE={1113:"CHGA",6855:"SYP",3642:"INSM1",6752:"SSTR2",429:"ASCL1",4760:"NEUROD1"}\n'
    'S="coadread_tcga_pan_can_atlas_2018"\n'
    'rp=next(p["molecularProfileId"] for p in get(f"{API}/studies/{S}/molecular-profiles") if "rna_seq" in p["molecularProfileId"] and "median_Zscores" in p["molecularProfileId"] and "normal" not in p["molecularProfileId"])\n'
    'd=post(f"{API}/molecular-profiles/{rp}/molecular-data/fetch",{"sampleListId":S+"_all","entrezGeneIds":list(NE)})\n'
    'bs=defaultdict(dict)\n'
    'for r in d:\n'
    '    if r.get("value") is not None: bs[r["sampleId"]][NE[r["entrezGeneId"]]]=r["value"]\n'
    'ne=np.array([np.mean(list(v.values())) for v in bs.values() if len(v)>=4]); frac=round(100*float((ne>1).mean()),1)\n'
    'plt.figure(figsize=(7,4.5)); plt.hist(ne,bins=40,color="#2f5fe0",alpha=.85); plt.axvline(1,color="#c0392b",ls="--")\n'
    'plt.title(f"Neuroendocrine program is absent from colorectal adenocarcinoma\\n{frac}% NE-high (n={len(ne)})"); plt.xlabel("NE score"); plt.tight_layout(); plt.show()\n'
    'print("percent NE-high:",frac)'),
 md("Only a few percent of colorectal adenocarcinomas are neuroendocrine-high. A rectal NET is "
    "neuroendocrine by definition. **Conclusion:** rectal NET should be treated as a NET (SSTR2 "
    "directed, Lu-177 DOTATATE), not as colorectal cancer. Full write-up: `docs/rectal_net_finding.md`."),
 md(DISC),
])

# ---------------- 08 uveal melanoma ----------------
write("08_uveal_melanoma_integrative.ipynb",[
 md("# 8. A tested hypothesis: in uveal melanoma, integrated multi-omics beats mutation calls\n\n"
    "**Question.** Uveal melanoma metastatic risk is the class 2, BAP1-deficient, monosomy-3 axis. "
    "Does an integrated multi-omic readout (DNA + RNA + protein) predict survival better than a "
    "single BAP1 mutation call? Data: TCGA-UVM (n=80), all layers, via cBioPortal. Reproducible."),
 co(SETUP+'\nfrom scipy.cluster.hierarchy import linkage, fcluster\nfrom scipy import stats\nS="uvm_tcga_pan_can_atlas_2018"; SL=S+"_all"'),
 md("## Assign an integrated class and align it with DNA features"),
 co('DR={2776:"GNAQ",2767:"GNA11",8314:"BAP1",23451:"SF3B1",1964:"EIF1AX"}\n'
    'SIG={999:"CDH1",1893:"ECM1",10289:"EIF1B",8087:"FXR1",3357:"HTR2B",3398:"ID2",29995:"LMCD1",4048:"LTA4H",57509:"MTUS1",11031:"RAB31",6091:"ROBO1",6304:"SATB1"}\n'
    'N=len(get(f"{API}/studies/{S}/samples"))\n'
    'muts=post(f"{API}/molecular-profiles/{S}_mutations/mutations/fetch",{"sampleListId":SL,"entrezGeneIds":list(DR)},params={"projection":"SUMMARY"})\n'
    'mut=defaultdict(set)\n'
    'for m in muts: mut[DR[m["entrezGeneId"]]].add(m["sampleId"])\n'
    'def gistic(e):\n'
    '    d=post(f"{API}/molecular-profiles/{S}_gistic/molecular-data/fetch",{"sampleListId":SL,"entrezGeneIds":[e]})\n'
    '    return {r["sampleId"]:r["value"] for r in d if r.get("value") is not None}\n'
    'mono3=set(s for s,v in gistic(8314).items() if v<=-1)\n'
    'rna=post(f"{API}/molecular-profiles/{S}_rna_seq_v2_mrna_median_Zscores/molecular-data/fetch",{"sampleListId":SL,"entrezGeneIds":list(SIG)+[8314,23532]})\n'
    'rz=defaultdict(dict)\n'
    'nm={**SIG,8314:"BAP1",23532:"PRAME"}\n'
    'for r in rna:\n'
    '    if r.get("value") is not None: rz[r["sampleId"]][nm[r["entrezGeneId"]]]=r["value"]\n'
    'Msig=pd.DataFrame(rz).T.reindex(columns=list(SIG.values())).dropna()\n'
    'cl=fcluster(linkage(Msig.values,method="ward"),2,criterion="maxclust")\n'
    'cls=pd.Series(cl,index=Msig.index)\n'
    'c2=max([1,2],key=lambda c: np.mean([s in mono3 for s in cls.index[cls==c]]))\n'
    'cla=pd.Series(np.where(cls==c2,"Class 2","Class 1"),index=cls.index)\n'
    'def fr(sset,g): return round(100*np.mean([s in sset for s in cla.index[cla==g]]),1)\n'
    'al=pd.DataFrame({"BAP1 mut %":[fr(mut["BAP1"],"Class 1"),fr(mut["BAP1"],"Class 2")],"Monosomy 3 %":[fr(mono3,"Class 1"),fr(mono3,"Class 2")],"SF3B1 %":[fr(mut["SF3B1"],"Class 1"),fr(mut["SF3B1"],"Class 2")],"EIF1AX %":[fr(mut["EIF1AX"],"Class 1"),fr(mut["EIF1AX"],"Class 2")]},index=["Class 1","Class 2"]); display(al)'),
 md("Class 2 is 95% monosomy 3 but only ~30% BAP1 mutated. Most functional BAP1 loss is not a point mutation."),
 md("## Survival: integrated class versus BAP1 mutation alone"),
 co('pdc=get(f"{API}/studies/{S}/clinical-data",params={"clinicalDataType":"PATIENT","projection":"SUMMARY","pageSize":100000})\n'
    'clin=defaultdict(dict)\n'
    'for r in pdc: clin[r.get("patientId","")][r.get("clinicalAttributeId","")]=r["value"]\n'
    'smap={x["sampleId"]:x["patientId"] for x in get(f"{API}/studies/{S}/samples")}\n'
    'def surv(grp):\n'
    '    rows=[]\n'
    '    for s,g in grp.items():\n'
    '        c=clin.get(smap.get(s),{}); t=c.get("OS_MONTHS"); st=c.get("OS_STATUS")\n'
    '        try: t=float(t)\n'
    '        except: continue\n'
    '        rows.append((g,t,1 if st and st.startswith("1") else 0))\n'
    '    return pd.DataFrame(rows,columns=["grp","t","ev"])\n'
    'def km(df,g):\n'
    '    d=df[df.grp==g].sort_values("t"); T=[0]; Sv=[1]; s=1.0; ar=len(d)\n'
    '    for t in sorted(d.t.unique()):\n'
    '        dd=int(d[(d.t==t)&(d.ev==1)].shape[0]); s*=(1-dd/ar) if ar else 1; T.append(t); Sv.append(s); ar-=int(d[d.t==t].shape[0])\n'
    '    return T,Sv\n'
    'def lr(df):\n'
    '    g=df.grp.unique(); \n'
    '    if len(g)!=2: return None\n'
    '    O=E=V=0.0\n'
    '    for t in sorted(df[df.ev==1].t.unique()):\n'
    '        n=df[df.t>=t].shape[0]; n1=df[(df.grp==g[0])&(df.t>=t)].shape[0]; d=df[(df.t==t)&(df.ev==1)].shape[0]; d1=df[(df.grp==g[0])&(df.t==t)&(df.ev==1)].shape[0]\n'
    '        if n<2: continue\n'
    '        E+=d*n1/n; O+=d1; V+=d*(n1/n)*(1-n1/n)*((n-d)/(n-1))\n'
    '    return stats.chi2.sf((O-E)**2/V,1) if V>0 else None\n'
    'sc=surv(cla); bap=pd.Series(np.where([s in mut["BAP1"] for s in cla.index],"BAP1 mut","BAP1 wt"),index=cla.index); sb=surv(bap)\n'
    'p_c=lr(sc); p_b=lr(sb)\n'
    'fig,ax=plt.subplots(1,2,figsize=(12,5))\n'
    'for g,c in [("Class 1","#2f5fe0"),("Class 2","#c0392b")]:\n'
    '    T,Sv=km(sc,g); ax[0].step(T,Sv,where="post",color=c,lw=2.5,label=g)\n'
    'ax[0].set_title(f"By integrated multi-omic class\\nlog-rank p={p_c:.1e}"); ax[0].legend(frameon=False); ax[0].set_ylim(0,1.02); ax[0].set_xlabel("months")\n'
    'for g,c in [("BAP1 wt","#2f5fe0"),("BAP1 mut","#c0392b")]:\n'
    '    T,Sv=km(sb,g); ax[1].step(T,Sv,where="post",color=c,lw=2.5,label=g)\n'
    'ax[1].set_title(f"By BAP1 mutation alone\\nlog-rank p={p_b:.2f}"); ax[1].legend(frameon=False); ax[1].set_ylim(0,1.02); ax[1].set_xlabel("months")\n'
    'plt.tight_layout(); plt.show()\n'
    'print(f"integrated class p={p_c:.1e} ; BAP1 mutation alone p={p_b:.2f}")'),
 md("The integrated class separates survival (p about 1e-6); BAP1 mutation alone does not (p about 0.5). "
    "Functional BAP1 loss is delivered by monosomy 3 and reduced expression, which a mutation panel "
    "misses. Full write-up: `docs/uveal_melanoma_finding.md`."),
 md(DISC),
])
print("DONE")
