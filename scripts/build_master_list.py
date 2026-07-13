import json, re, glob, csv, os

def norm(s):
    s = s.lower().strip(); s = re.sub(r"\([^)]*\)", " ", s); s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(sorted(t for t in s.split() if t and t not in {"the","of","a","an","and","type","tumour","tumor","neoplasm"}))

SYS = {
 1:"Head, neck and thorax", 2:"Digestive system",
 3:"Genitourinary, gynecologic and gestational", 4:"Skin, melanoma and endocrine",
 5:"Soft tissue sarcoma", 6:"Bone sarcoma and pediatric embryonal",
 7:"Central nervous system", 8:"Hematologic",
}
# map each normalized name -> earliest family system
fam = {}
for fp in sorted(glob.glob("tmp/tmp/rarecancers_family_*.json")):
    n = int(re.search(r"_(\d+)\.json", fp).group(1))
    for r in json.load(open(fp)):
        k = norm(r.get("name",""))
        if k and k not in fam:
            fam[k] = n

cat = json.load(open("data/rare_conditions_catalog.json"))
cancers = [r for r in cat if r.get("category") == "rare cancer"]

groups = {v: [] for v in SYS.values()}
groups["Additional catalogued rare cancers"] = []
for r in cancers:
    sysname = SYS.get(fam.get(norm(r["name"])), "Additional catalogued rare cancers")
    groups[sysname].append(r)

order = list(SYS.values()) + ["Additional catalogued rare cancers"]
total = len(cancers)

# markdown grouped
md = [f"# Master list of rare cancers ({total} entities)\n",
      "Compiled for Anveshar from WHO Classification of Tumours (5th ed), Orphanet, the NCI rare cancers list, and RARECAREnet. Rare cancer defined as incidence below 6 per 100,000 per year. Grouped by organ system; a gene or molecular marker is shown where one defining driver exists.\n"]
for g in order:
    rows = sorted(groups[g], key=lambda x: x["name"].lower())
    if not rows: continue
    md.append(f"\n## {g} ({len(rows)})\n")
    for r in rows:
        gene = r.get("key_gene_or_marker","")
        al = ", ".join(r.get("aliases",[]) or [])
        line = r["name"]
        if gene: line += f"  [{gene}]"
        if al: line += f"  (aka {al})"
        cause = (r.get("causes") or "").strip()
        if cause:
            tag = "Cause" if r.get("cause_known") else "Cause (not established)"
            line += f"\n    {tag}: {cause}"
        md.append(line)
open("data/rare_cancers_master_list.md","w").write("\n".join(md)+"\n")

# flat csv
with open("data/rare_cancers_master_list.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["name","organ_system","key_gene_or_marker","aliases",
                                   "potential_causes","cause_established","source"])
    for g in order:
        for r in sorted(groups[g], key=lambda x: x["name"].lower()):
            w.writerow([r["name"], g, r.get("key_gene_or_marker",""),
                        "; ".join(r.get("aliases",[]) or []),
                        r.get("causes",""), "yes" if r.get("cause_known") else "no",
                        r.get("source","")])

print("total rare cancers:", total)
for g in order:
    if groups[g]: print(f"  {g}: {len(groups[g])}")
print("wrote data/rare_cancers_master_list.md and .csv")
