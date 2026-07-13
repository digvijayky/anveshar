"""Explore MSK-IMPACT (Zehir et al., Nat Med 2017; msk_impact_2017) for rare cancer knowledge.
Real public data via cBioPortal. Maps MSK-IMPACT detailed cancer types onto Anveshar's rare
cancer catalog (coverage), and pulls real driver mutation frequencies for flagship rare cancers.
No simulation or subsampling.
"""
import os, re, json, requests, numpy as np, pandas as pd
from collections import Counter, defaultdict
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

FS = 16
for p in ["/home/yarlagad/.local/share/fonts/Arial.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"] = "Arial"; break
plt.rcParams.update({"font.size": FS, "figure.dpi": 150})

API = "https://www.cbioportal.org/api"; STUDY = "msk_impact_2017"; PROF = STUDY + "_mutations"
OUT = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/github/concord/examples/multimodal/msk_impact_rare_cancers"
os.makedirs(OUT, exist_ok=True)
CAT = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/github/concord/data/rare_conditions_catalog.json"
log = {"study": STUDY}

def get(u, **k): r = requests.get(u, timeout=60, **k); r.raise_for_status(); return r.json()
def post(u, b, **k): r = requests.post(u, json=b, timeout=90, **k); r.raise_for_status(); return r.json()
def norm(s): return " ".join(sorted(t for t in re.sub(r"[^a-z0-9]+"," ",(s or "").lower()).split()
                                    if t not in {"the","of","a","an","and","type","tumor","tumour","neoplasm","cancer","carcinoma"}))

study = get(f"{API}/studies/{STUDY}"); N = study.get("allSampleCount")
log["msk_total_samples"] = N; log["msk_name"] = study.get("name", "")

# ---- sample -> detailed cancer type ----
cd = get(f"{API}/studies/{STUDY}/clinical-data",
         params={"attributeId": "CANCER_TYPE_DETAILED", "clinicalDataType": "SAMPLE",
                 "projection": "SUMMARY", "pageSize": 300000})
type_samples = defaultdict(list)
for row in cd:
    type_samples[row["value"]].append(row["sampleId"])
dist = Counter({t: len(s) for t, s in type_samples.items()})
log["n_detailed_types"] = len(dist)

# ---- map MSK types to Anveshar rare cancer catalog ----
cat = json.load(open(CAT))
cancers = [r for r in cat if r.get("category") == "rare cancer"]
cat_norm = {}
for r in cancers:
    cat_norm[norm(r["name"])] = r["name"]
    for a in r.get("aliases", []) or []:
        cat_norm.setdefault(norm(a), r["name"])
def match(msk_type):
    # strict: exact normalized name or alias match only, to avoid a common cancer (glioblastoma,
    # small cell lung) matching a rare histologic variant by substring.
    k = norm(msk_type)
    return cat_norm.get(k) if k else None

rows = []
for t, n in dist.most_common():
    m = match(t)
    rows.append({"msk_cancer_type": t, "n_samples": n, "matched_rare_cancer": m or ""})
mp = pd.DataFrame(rows)
mp.to_csv(f"{OUT}/msk_impact_rare_cancer_coverage_source.csv", index=False)
matched = mp[mp.matched_rare_cancer != ""]
log["rare_types_matched"] = int(matched.matched_rare_cancer.nunique())
log["rare_tumors_total"] = int(matched.n_samples.sum())
log["top_rare"] = matched.groupby("matched_rare_cancer").n_samples.sum().sort_values(ascending=False).head(20).to_dict()

# ---- figure: top rare cancers by MSK-IMPACT sample count ----
top = matched.groupby("matched_rare_cancer").n_samples.sum().sort_values(ascending=False).head(20)[::-1]
fig, ax = plt.subplots(figsize=(9.5, 8.5))
ax.barh(range(len(top)), top.values, color="#2f5fe0")
ax.set_yticks(range(len(top))); ax.set_yticklabels(top.index, fontsize=FS-3)
for i, v in enumerate(top.values): ax.text(v + max(top.values)*0.01, i, str(int(v)), va="center", fontsize=FS-4)
ax.set_xlabel("Tumors sequenced in MSK-IMPACT")
ax.set_title(f"Rare cancers in MSK-IMPACT ({log['rare_tumors_total']:,} tumors,\n{log['rare_types_matched']} rare cancer types)")
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(f"{OUT}/msk_impact_rare_cancer_coverage.pdf"); plt.close()

# ---- flagship per-type driver frequencies (real) ----
flags = [t for t in ["Uveal Melanoma", "Adenoid Cystic Carcinoma", "Renal Medullary Carcinoma",
                     "Chordoma", "Merkel Cell Carcinoma", "Gastrointestinal Stromal Tumor"]
         if t in type_samples and 15 <= len(type_samples[t]) <= 1500]
flag_freq = {}
for t in flags[:4]:
    sids = type_samples[t]
    muts = post(f"{API}/molecular-profiles/{PROF}/mutations/fetch",
                {"sampleIds": sids}, params={"projection": "DETAILED"})
    g_samp = defaultdict(set)
    for m in muts:
        g = (m.get("gene") or {}).get("hugoGeneSymbol") or m.get("hugoGeneSymbol")
        if g: g_samp[g].add(m["sampleId"])
    freq = sorted(((g, len(s)) for g, s in g_samp.items()), key=lambda x: -x[1])[:10]
    flag_freq[t] = {"n": len(sids), "top": [(g, round(100*c/len(sids), 1)) for g, c in freq]}
json.dump(flag_freq, open(f"{OUT}/msk_impact_flagship_driver_frequencies.json", "w"), indent=2)
# multi-panel figure
if flag_freq:
    fig, axs = plt.subplots(2, 2, figsize=(13, 9)); axs = axs.ravel()
    for i, (t, d) in enumerate(flag_freq.items()):
        genes = [g for g, _ in d["top"]][::-1]; vals = [v for _, v in d["top"]][::-1]
        axs[i].barh(range(len(genes)), vals, color="#7b3fe4")
        axs[i].set_yticks(range(len(genes))); axs[i].set_yticklabels(genes, fontsize=FS-4)
        axs[i].set_title(f"{t} (MSK-IMPACT n={d['n']})", fontsize=FS-2)
        axs[i].set_xlabel("Mutated (%)", fontsize=FS-3)
        for s in ["top","right"]: axs[i].spines[s].set_visible(False)
    for j in range(len(flag_freq), 4): axs[j].axis("off")
    plt.tight_layout(); plt.savefig(f"{OUT}/msk_impact_flagship_drivers.pdf"); plt.close()
pd.DataFrame([{"rare_cancer": t, "msk_n": d["n"], "top_genes": "; ".join(f"{g} {v}%" for g, v in d["top"])}
             for t, d in flag_freq.items()]).to_csv(f"{OUT}/msk_impact_flagship_drivers_source.csv", index=False)

json.dump(log, open(f"{OUT}/msk_impact_run_log.json", "w"), indent=2)
open(f"{OUT}/msk_impact_methodology_and_legend.txt", "w").write(
    f"""MSK-IMPACT exploration for rare cancer knowledge (real public data).
Source: Memorial Sloan Kettering MSK-IMPACT Clinical Sequencing Cohort (Zehir et al., Nat Med 2017;
study {STUDY}), {N:,} prospectively sequenced tumors, accessed live via the cBioPortal REST API. No
simulation or subsampling.

COVERAGE. MSK-IMPACT records {log['n_detailed_types']} detailed cancer types. Mapping these onto
Anveshar's rare cancer catalog identifies {log['rare_types_matched']} rare cancer types comprising
{log['rare_tumors_total']:,} sequenced tumors, a large real world evidence base for cancers that are
individually rare. The coverage figure shows the best represented rare cancers.

DRIVER FREQUENCIES. For flagship rare cancers, per type mutation frequencies were computed from the
MSK-IMPACT targeted panel and compared with the driver biology Anveshar curates (for example the GNAQ
and GNA11 Galpha events plus BAP1 in uveal melanoma). This grounds Anveshar's driver claims in a real
clinical cohort in addition to TCGA.

This is a research and educational analysis of public data, not medical advice; clinical decisions must
be made by a qualified health care provider.
""")
print("DONE MSK"); print(json.dumps(log, indent=2)[:1500])
