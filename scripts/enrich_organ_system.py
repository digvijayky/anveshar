"""Persist organ_system onto each rare-cancer catalog entry (idempotent).

Organ system is taken from the family compilation files in tmp/tmp when available;
once written to the catalog it survives even if those temp files are cleaned.
"""
import json, re, glob, os, shutil

CAT = "data/rare_conditions_catalog.json"
SYS = {1:"Head, neck and thorax", 2:"Digestive system",
       3:"Genitourinary, gynecologic and gestational", 4:"Skin, melanoma and endocrine",
       5:"Soft tissue sarcoma", 6:"Bone sarcoma and pediatric embryonal",
       7:"Central nervous system", 8:"Hematologic"}

def norm(s):
    s = (s or "").lower().strip(); s = re.sub(r"\([^)]*\)", " ", s); s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(sorted(t for t in s.split() if t and t not in {"the","of","a","an","and","type","tumour","tumor","neoplasm"}))

fam = {}
for fp in sorted(glob.glob("tmp/tmp/rarecancers_family_*.json")):
    n = int(re.search(r"_(\d+)\.json", fp).group(1))
    for r in json.load(open(fp)):
        k = norm(r.get("name",""))
        if k and k not in fam:
            fam[k] = n

cat = json.load(open(CAT))
shutil.copy2(CAT, CAT + ".bak_organ")
changed = 0
for r in cat:
    if r.get("category") != "rare cancer":
        continue
    sysname = SYS.get(fam.get(norm(r["name"])), "Additional catalogued rare cancers")
    if r.get("organ_system") != sysname:
        r["organ_system"] = sysname; changed += 1
json.dump(cat, open(CAT, "w"), indent=2, ensure_ascii=False)

from collections import Counter
c = Counter(r.get("organ_system") for r in cat if r.get("category")=="rare cancer")
print("updated organ_system on", changed, "rare cancers")
for k, v in c.most_common():
    print(f"  {k}: {v}")
